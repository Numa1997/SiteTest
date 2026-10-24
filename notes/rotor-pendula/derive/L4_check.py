"""L4: the second blade with the geared generator in the full equation (L4_full.py, version 3), at the settings the formula
(7.6)-(7.7) of L4_generator.py chose, at half and twice its brake, and at 8 m/s with every catalogue ratio at its own best brake.
The rotor's work is integrated too, so the energy book closes in Python: W = ΔE_kin + ΔE_pot + E_paid + ΔE_spin over the window.

Run: python3 -I L4_check.py [steps per turn] [band factor]   (defaults 2000 and 1e-3)   Writes L4_check_<steps>.json.
L4_converge.py compares the 2000- and 4000-step runs.
The smoothing bands: eps_w = band x swing scale; eps_p = band x (f0 + (kappa_e + j) x swing scale) x swing scale, the gear's own
power scale (a band on gravity's scale G was some thousand times too wide for this blade and made the paid power 16 % low).
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import radau_step
import setup as S
import L4_generator as Gm
from L4_full import make_rhs

HERE = os.path.dirname(os.path.abspath(__file__))
nst = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
efac = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-3
m, l, g = S.M_B, S.L_B, S.G0
I, mlc = m*l*l/3, m*l/2
rows = []
for v, Om, rp in S.mountings():
    best, cands = Gm.best_for(Om, rp)
    for mult in (0.5, 1.0, 2.0):
        ce = min(best['c_e']*mult, best['c_sc']*0.999)
        rows.append(dict(wind=v, Om=Om, rp=rp, N=best['N'], eta=best['eta'], Jg=best['Jg'], c_e=ce, mult=mult, kind='best'))
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
h = 2*math.pi/nst; Y = np.zeros((n, 6)); maxit = 0; ncap = 0; capErr = 0.0
def mech(t, Y):                                      # kinetic + potential energy of the blade, unit I Omega^2 (phi = t)
    th, w = Y[:, 0], Y[:, 1]
    T = 0.5*(1 + w)**2 + 0.5*m*rp**2/I + (mlc*rp/I)*(1 + w)*np.cos(th)
    V = Gp*np.sin(t) + G*np.sin(t + th)
    return T + V, 0.5*j*w**2                          # and the motor's spin energy
for k in range(nst*(settle + meas)):
    if k == nst*settle:
        Y0 = Y.copy(); thmax = np.zeros(n); E0, S0 = mech(k*h, Y)
    Y, it = radau_step(F, k*h, Y, h); maxit = max(maxit, it)
    if it == 12:
        ncap += 1; capErr = max(capErr, radau_step.last_err)
    if k >= nst*settle:
        thmax = np.maximum(thmax, np.abs(Y[:, 0]))
E1, S1 = mech(nst*(settle + meas)*h, Y)
u = I*Om**3; T = 2*math.pi*meas
Pl = (Y[:, 2] - Y0[:, 2])/T*u; Pp = (Y[:, 3] - Y0[:, 3])/T*u; Pf = (Y[:, 4] - Y0[:, 4])/T*u; Pw = (Y[:, 5] - Y0[:, 5])/T*u
book = ((E1 - E0) + (Y[:, 3] - Y0[:, 3]) - (Y[:, 5] - Y0[:, 5]))*I*Om**2     # paid includes the spin's change (k x theta')
out = []
for i, r in enumerate(rows):
    fo = form[i]
    out.append(dict(wind=r['wind'], N=r['N'], eta=r['eta'], c_e=r['c_e'], mult=r['mult'], kind=r['kind'], R_load=Nn[i]**2*Gm.KT*Gm.KE/ce[i] - Gm.RC,
                    Pstar=S.pstar(r['Om']), j=float(j[i]), f_over_G=float(f0[i]/(eta[i]*G[i])), P_load=float(Pl[i]), P_paid=float(Pp[i]),
                    P_fric=float(Pf[i]), P_rotor=float(Pw[i]), book_J=float(book[i]), Theta=float(thmax[i]), P_load_formula=fo['P_load'],
                    P_paid_formula=fo['P_paid'], Theta_formula=fo['Theta']))
    print(f"{r['wind']:.0f} m/s, N {r['N']:>5}, c_e x {r['mult']:.1f} ({r['kind']}): load {Pl[i]*1e3:8.3f} mW (formula {fo['P_load']*1e3:8.3f}, "
          f"{(Pl[i]/fo['P_load'] - 1)*100:+.1f} %), paid {Pp[i]*1e3:8.3f} mW, rotor {Pw[i]*1e3:8.3f} mW, friction {Pf[i]*1e3:7.3f} mW, "
          f"swing {thmax[i]:.3f} rad (formula {fo['Theta']:.3f}); book {book[i]:+.1e} J")
fails = 0
def check(name, ok):
    global fails
    fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name)
nsteps = nst*(settle + meas)
check(f'Newton converged to 1e-12 within 12 iterations, or, in the {ncap} of {nsteps} steps ({ncap/nsteps:.1e}) where it stopped at 12, its last '
      f'correction was {capErr:.1e} relative, below 1e-9; and such steps are fewer than 1 in 1000', ncap/nsteps < 1e-3 and capErr < 1e-9)
check('the energy book closes over the 20 measured turns at every setting (|residual| < 1e-6 J)', np.max(np.abs(book)) < 1e-6)
bst = [o for o in out if o['kind'] == 'best']
check('at every wind the formula\'s brake is within the full equation\'s best of the three brakes tried, or within 5 % of it',
      all(max(b['P_load'] for b in bst if b['wind'] == w)/next(b['P_load'] for b in bst if b['wind'] == w and b['mult'] == 1.0) < 1.05 for w in S.WINDS))
check('the formula (7.6)-(7.7) is within 10 % of the full equation at the chosen settings',
      all(abs(b['P_load']/b['P_load_formula'] - 1) < 0.10 for b in bst if b['mult'] == 1.0))
json.dump(out, open(os.path.join(HERE, f'L4_check_{nst}.json'), 'w'), indent=1)
raise SystemExit(1 if fails else 0)
