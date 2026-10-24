"""L4: does the Newton cap of 12 iterations in L4_check.py change the geared results?

L4_check.py at 2000 steps per turn stopped Newton at 12 iterations in 1939 of 240000 steps, with a last correction up to 1.6e-2.
This script reruns the same 16 settings with the same equation and bands, with the cap raised to 40 and Newton tracked per
setting: for each it counts the steps that needed more than 12 iterations, in the settle turns and in the measured turns, the
steps that still did not converge within 40, and compares the powers and the swing with L4_check_<steps>.json.
Run: python3 -I L4_newton.py [steps per turn]   (default 2000; about as long as L4_check.py)   Writes L4_newton_<steps>.json.
"""
import json, math, os, sys
import numpy as np
from engine import RA, RC
import setup as S
import L4_generator as Gm
from L4_full import make_rhs

HERE = os.path.dirname(os.path.abspath(__file__))
nst = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
efac = 1e-3 if nst == 2000 else 3e-4
TOL, CAP, OLD = 1e-12, 40, 12

def radau_step_each(F, t, Y, h, eps=1e-7):
    """radau_step of engine.py, with Newton continued until every member converges (or CAP); returns per-member iterations
    and per-member last correction."""
    N, d = Y.shape
    F0 = F(t, Y)
    J = np.empty((N, d, d))
    for j in range(d):
        dy = eps*np.maximum(1.0, np.abs(Y[:, j]))
        Yp = Y.copy(); Yp[:, j] += dy
        J[:, :, j] = (F(t, Yp) - F0)/dy[:, None]
    Mbig = np.zeros((N, 3*d, 3*d))
    for i in range(3):
        for k in range(3):
            Mbig[:, i*d:(i + 1)*d, k*d:(k + 1)*d] = (i == k)*np.eye(d) - h*RA[i, k]*J
    Minv = np.linalg.inv(Mbig)
    Z = (h*RC[None, :, None])*F0[:, None, :]
    its = np.zeros(N, int); done = np.zeros(N, bool); err = np.full(N, np.inf)
    for it in range(1, CAP + 1):
        Fz = np.stack([F(t + RC[i]*h, Y + Z[:, i]) for i in range(3)], axis=1)
        G = Z - h*np.einsum('ik,nkd->nid', RA, Fz)
        dZ = -np.einsum('nab,nb->na', Minv, G.reshape(N, 3*d)).reshape(N, 3, d)
        Z = Z + dZ
        e = np.max((np.abs(dZ)/(1.0 + np.abs(Z))).reshape(N, -1), axis=1)
        newly = (~done) & (e < TOL)
        its[newly] = it; done |= newly; err = np.where(done, err, e)
        if done.all():
            break
    its[~done] = CAP; err[done] = 0.0
    return Y + Z[:, 2], its, np.where(done, 0.0, e)

m, l, g = S.M_B, S.L_B, S.G0
I, mlc = m*l*l/3, m*l/2
rows = []
for v, Om, rp in S.mountings():
    best, cands = Gm.best_for(Om, rp)
    for mult in (0.5, 1.0, 2.0):
        rows.append(dict(wind=v, Om=Om, rp=rp, N=best['N'], eta=best['eta'], Jg=best['Jg'], c_e=min(best['c_e']*mult, best['c_sc']*0.999),
                         mult=mult, kind='best'))
    if v == 8.0:
        for p in cands:
            if p['N'] != best['N'] and not p['jammed']:
                rows.append(dict(wind=v, Om=Om, rp=rp, N=p['N'], eta=p['eta'], Jg=p['Jg'], c_e=p['c_e'], mult=1.0, kind='ratio'))
n = len(rows)
A = lambda k: np.array([r[k] for r in rows], float)
Om, rp, Nn, eta, Jg, ce = A('Om'), A('rp'), A('N'), A('eta'), A('Jg'), A('c_e')
R = mlc*rp/I; G = mlc*g/(I*Om**2); Gp = m*g*rp/(I*Om**2)
j = (Gm.JM + Jg)*Nn**2/I; ke = ce/(I*Om); f0 = Nn*Gm.T0/(I*Om**2); keep = 1 - ce/(Nn**2*Gm.KT*Gm.KE/Gm.RC)
form = [Gm.powers(r['Om'], r['rp'], r['N'], r['eta'], r['Jg'], r['c_e']) for r in rows]
sc = np.array([min(max(f['Theta'], 1e-2), 0.5) for f in form])
F = make_rhs(R, G, j, f0, ke, eta, keep, efac*sc, efac*(f0 + (ke + j)*sc)*sc, Gp=Gp)
settle, meas = 100, 20
h = 2*math.pi/nst; Y = np.zeros((n, 6))
over_settle = np.zeros(n, int); over_meas = np.zeros(n, int); capped = np.zeros(n, int); worst = np.zeros(n); maxits = np.zeros(n, int)
for k in range(nst*(settle + meas)):
    if k == nst*settle:
        Y0 = Y.copy()
    Y, its, e = radau_step_each(F, k*h, Y, h)
    (over_meas if k >= nst*settle else over_settle)[:] += its > OLD
    capped += its >= CAP; worst = np.maximum(worst, e); maxits = np.maximum(maxits, its)
u = I*Om**3; T = 2*math.pi*meas
Pl = (Y[:, 2] - Y0[:, 2])/T*u; Pp = (Y[:, 3] - Y0[:, 3])/T*u; Pf = (Y[:, 4] - Y0[:, 4])/T*u
ref = json.load(open(os.path.join(HERE, f'L4_check_{nst}.json')))
out = []; dmax = 0.0
for i, r in enumerate(rows):
    q = ref[i]
    assert q['wind'] == r['wind'] and q['N'] == r['N'] and q['mult'] == r['mult'], 'row order differs from L4_check'
    dl = Pl[i]/q['P_load'] - 1; dp = Pp[i]/q['P_paid'] - 1; dmax = max(dmax, abs(dl), abs(dp))
    out.append(dict(wind=r['wind'], N=r['N'], mult=r['mult'], kind=r['kind'], over12_settle=int(over_settle[i]), over12_measured=int(over_meas[i]),
                    capped40=int(capped[i]), max_its=int(maxits[i]), worst_unconverged=float(worst[i]), P_load=float(Pl[i]), P_paid=float(Pp[i]),
                    P_fric=float(Pf[i]), rel_load=float(dl), rel_paid=float(dp)))
    print(f"{r['wind']:.0f} m/s, N {r['N']:>5}, c_e x {r['mult']:.1f} ({r['kind']}): steps over 12 iterations {over_settle[i]} settling, "
          f"{over_meas[i]} measured; most {maxits[i]}; not converged in 40: {capped[i]}; load {Pl[i]*1e3:.4f} mW ({dl:+.1e} vs cap 12), "
          f"paid {Pp[i]*1e3:.4f} mW ({dp:+.1e})", flush=True)
json.dump(out, open(os.path.join(HERE, f'L4_newton_{nst}.json'), 'w'), indent=1)
ok = capped.sum() == 0
print(('PASS' if ok else 'FAIL') + f' with a cap of {CAP}, Newton converged to {TOL:g} in every step of every setting ({int(capped.sum())} steps did not)')
print(f'RESULT: the cap of 12 changed the load and paid powers by at most {dmax:.1e} relative')
raise SystemExit(0 if ok else 1)
