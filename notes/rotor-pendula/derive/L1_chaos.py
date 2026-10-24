"""L1: the chaos group at R = 1, as ensembles of initial conditions, with the largest Lyapunov exponent of every member.

Run: python3 -I L1_chaos.py [--quick]   (writes L1_chaos.json)
Group: the double pendulum of setup.py (M/2 on L/2, twice) at resonance, R = r_p/L = 1, with gravity's push G = g/(Omega^2 L) = 3,
brakes kappa = c/(M L^2 Omega) = 1.0, 1.4, 1.9, 2.8 at both joints (c0 = c1 = c).  Only R, G and kappa matter (chapter 1).
Each damping: 1 member from rest (q = 0, q' = 0) and 15 from random angles in (-pi, pi], at rest relative to the blade;
seed 2026.  Transient 100 turns, measured 200 turns.  Lyapunov exponent: Benettin,
d0 = 1e-8 in (q1, q2, q1'/Omega, q2'/Omega), renormalised every quarter turn, averaged over the measured turns, in 1/s.
"""
import json, math, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Double, pendulum_rhs, integrate
import setup as S

QUICK = '--quick' in sys.argv
M, L = S.M, S.L
R_GROUP, G_GROUP = 1.0, 3.0
KAPPAS = [1.0, 1.4, 1.9, 2.8]
Om = math.sqrt(S.G0/(G_GROUP*L)); rp = R_GROUP*L; Tt = 2*math.pi/Om
cs = [k*M*L**2*Om for k in KAPPAS]
NIC = 16
n_per_turn = 100
TR, MEAS = (20, 40) if QUICK else (100, 200)
rng = np.random.default_rng(2026)
ic = np.zeros((NIC, 5)); ic[1:, 0:2] = rng.uniform(-math.pi, math.pi, (NIC - 1, 2))
c_arr = np.repeat(cs, NIC); Y0 = np.tile(ic, (len(cs), 1))
Nb = Y0.shape[0]
sysd = Double(M/2, M/2, L/2, L/2, rp, np.concatenate([c_arr, c_arr]), np.concatenate([c_arr, c_arr]))
F = pendulum_rhs(sysd, Om=Om)
Yp = Y0.copy(); Yp[:, 0] += 1e-8
Y = np.concatenate([Y0, Yp])
t0 = time.time()
h = Tt/n_per_turn
W = [1, 1, 1/Om, 1/Om]                            # metric (q1, q2, q1'/Omega, q2'/Omega)
r1 = integrate(F, Y, 0, TR*Tt, h, lyap=(1e-8, n_per_turn//4, [0, 1, 2, 3], 1e30, W))
E0 = r1['Y'][:Nb, 4].copy()
r2 = integrate(F, r1['Y'], TR*Tt, (TR + MEAS)*Tt, h, lyap=(1e-8, n_per_turn//4, [0, 1, 2, 3], 0.0, W))
P = (r2['Y'][:Nb, 4] - E0)/(MEAS*Tt)
lam = r2['lyap']                                  # 1/s
print(f'({time.time() - t0:.0f} s, Newton iterations <= {max(r1["maxit"], r2["maxit"])})')
out = []
for k, c in enumerate(cs):
    sl = slice(k*NIC, (k + 1)*NIC)
    Pk, lk = P[sl], lam[sl]
    ch = lk > 0.01*Om
    print(f'kappa = {KAPPAS[k]:.1f} (c = {c:.4f} N m s): power {np.round(Pk*1e3, 1).tolist()} mW')
    print(f'        Lyapunov 1/s {np.round(lk, 3).tolist()}; chaotic members {ch.sum()}/{NIC}')
    out.append(dict(kappa=KAPPAS[k], c=c, P=Pk.tolist(), lyap=lk.tolist()))
json.dump(dict(Om=Om, rp=rp, R=R_GROUP, G=G_GROUP, M=M, L=L, TR=TR, MEAS=MEAS, n_per_turn=n_per_turn, seed=2026, groups=out),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L1_chaos.json'), 'w'), indent=1)
