"""L2: the single pendulum on the NREL 5-MW rotor in IEC class A turbulence at 8 m/s, against steady rotation.

Run: python3 -I L2_run.py   (writes L2_run.json; prints the decomposition and PASS/FAIL on the contract's predictions)
Records: 40 periodic 600 s rotor-effective wind records (turbulence.synth, seed 11); each run twice, the second pass measured.
Mountings: r_p = 18.9, 37.8, 56.7 m; m = 0.1 kg, L = 0.2 m; c fixed at the L0 optimum for the steady speed Omega0.
State per member: q, q', E (harvest), phi, Omega; Omega' from the one-state rotor; in-plane gravity g cos 5 deg.
Decomposition of 10-min mean power P_turb against steady rotation P(Omega0):
  (a) mean-speed shift      = P_unif(mean Omega of the record) - P(Omega0)
  (b) quasi-static wander   = P_turb(no Euler terms) - P_unif(mean Omega)
  (c) dynamic Euler terms   = P_turb - P_turb(no Euler terms)
"""
import json, math, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import turbulence as W
from engine import Single, radau_step

g = 9.80665*math.cos(math.radians(5.0))
m, L = 0.1, 0.2
LAW = sys.argv[1] if len(sys.argv) > 1 else 'nrel'
W.TORQUE_LAW = LAW
from scipy.optimize import brentq
OM0 = brentq(lambda O: W.q_aero(8.0, O) - W.gen_torque(O), 0.5, 1.5)   # steady speed at 8 m/s for this law
NREC = 40; DT = 0.1
rps = np.array([0.3, 0.6, 0.9])*63.0
c_opt = m*L**2*OM0*(rps/L - 1)

def make_F(sysobj, wind, euler):
    def F(t, Y):
        q = Y[:, 0:1]; w = Y[:, 1:2]; ph = Y[:, 3]; Om = Y[:, 4]
        v = wind(t)
        Od = W.rotor_accel(v, Om)
        a, P = sysobj.acc(q, w, ph, Om, Od*euler, 0.0)
        return np.stack([w[:, 0], a[:, 0], P, Om, Od], axis=1)
    return F

def run_turbulent(V, euler, h):
    n_rec = V.shape[0]
    wind_all = np.repeat(V, 3, axis=0)                     # member order: record-major, mounting-minor
    rp = np.tile(rps, n_rec); c = np.tile(c_opt, n_rec)
    sysobj = Single(m, L, rp, c, g=g)
    wind = W.WindInterp(wind_all, DT)
    F = make_F(sysobj, wind, euler)
    N = wind_all.shape[0]
    Y = np.zeros((N, 5)); Y[:, 4] = OM0
    nst = int(round(600.0/h)); Om_sum = np.zeros(N)
    for k in range(2*nst):
        if k == nst:
            E0 = Y[:, 2].copy(); Om_sum[:] = 0
        Y, _ = radau_step(F, k*h, Y, h)
        if k >= nst:
            Om_sum += Y[:, 4]
    return (Y[:, 2] - E0)/600.0, Om_sum/nst

def P_uniform(Om, rp, c):
    """steady-state single pendulum at uniform speed Om (arrays), 40 turns settle + 20 measured, 100 steps/turn"""
    sysobj = Single(m, L, rp, c, g=g)
    def F(t, Y):
        a, P = sysobj.acc(Y[:, 0:1], Y[:, 1:2], Om*t, Om, 0.0, 0.0)
        return np.stack([Y[:, 1], a[:, 0], P], axis=1)
    # integrate in blade-angle steps: common step in time would differ per member, so use the slowest turn
    Tt = 2*math.pi/np.min(Om); h = Tt/100
    Y = np.zeros((len(rp), 3))
    n1, n2 = 4000, 6000
    for k in range(n2):
        if k == n1: E0 = Y[:, 2].copy()
        Y, _ = radau_step(F, k*h, Y, h)
    return (Y[:, 2] - E0)/((n2 - n1)*h)

if __name__ == '__main__':
    t0 = time.time()
    print(f'torque law {LAW}: steady speed at 8 m/s {OM0:.4f} rad/s', flush=True)
    V = W.synth(8.0, W.iec_sigma(8.0), nrec=NREC, seed=11, rotor_eff=True)
    h = 2*math.pi/OM0/100
    Pt, Omb = run_turbulent(V, 1.0, h)
    Pn, _ = run_turbulent(V, 0.0, h)
    print(f'turbulent runs: {time.time() - t0:.0f} s', flush=True)
    rp_all = np.tile(rps, NREC); c_all = np.tile(c_opt, NREC)
    Pu = P_uniform(Omb, rp_all, c_all)
    P0 = P_uniform(np.full(3, OM0), rps, c_opt)
    fails = 0
    def check(name, ok):
        global fails
        fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name)
    out = dict(NREC=NREC, seed=11, Om0=OM0, rps=rps.tolist(), c=c_opt.tolist(), P0=P0.tolist(), mountings=[])
    se = lambda x: x.std(ddof=1)/math.sqrt(len(x))
    for j, rp in enumerate(rps):
        sl = slice(j, None, 3)
        pt, pn, pu = Pt[sl], Pn[sl], Pu[sl]
        a = (pu - P0[j])/P0[j]; b = (pn - pu)/P0[j]; cc = (pt - pn)/P0[j]; tot = (pt - P0[j])/P0[j]
        q05 = np.quantile(pt, 0.05)
        print(f'r_p = {rp:.1f} m: steady {P0[j]*1e3:.3f} mW; turbulent mean {pt.mean()*1e3:.3f} +- {se(pt)*1e3:.3f} mW, '
              f'5 % quantile {q05*1e3:.3f} mW')
        print(f'   change {tot.mean()*100:+.2f} %: (a) mean speed {a.mean()*100:+.2f} %, (b) wander {b.mean()*100:+.3f} +- '
              f'{se(b)*100:.3f} %, (c) Euler {cc.mean()*100:+.5f} +- {se(cc)*100:.5f} %')
        out['mountings'].append(dict(rp=rp, P0=P0[j], P_turb=pt.tolist(), P_noeuler=pn.tolist(), P_unif=pu.tolist(),
                                     Om_mean=Omb[sl].tolist()))
        check(f'P1 r_p = {rp:.1f}: |(b)+(c)| = {abs((b + cc).mean())*100:.3f} % < 1 % + 2 SE', abs((b + cc).mean()) < 0.01 + 2*se(b + cc))
        check(f'P2 r_p = {rp:.1f}: |(c)| = {abs(cc.mean()):.1e} < 1e-3', abs(cc.mean()) < 1e-3)
        check(f'P3 r_p = {rp:.1f}: total change {tot.mean()*100:+.2f} % between -3 % and -1 %', -0.03 < tot.mean() < -0.01)
    out['law'] = LAW
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'L2_run_{LAW}.json'), 'w'))
    print(f'({time.time() - t0:.0f} s)')
    print('ALL PASS' if fails == 0 else f'{fails} FAIL')
