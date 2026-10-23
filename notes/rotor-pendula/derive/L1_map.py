"""L1: where is the double pendulum chaotic?  Largest Lyapunov exponent and mean power over (R, G, kappa) with ensembles.

Run: python3 -I L1_map.py [--quick]   (writes L1_map.json; parallel over R with 3 processes)
Dimensionless units: M = 1, L = 1, Omega = 1, so m1 = m2 = 1/2, l1 = l2 = 1/2, r_p = R, g = G, c0 = c1 = kappa; times in
radians of blade angle, Lyapunov exponents per radian, power in units of M L^2 Omega^3.
kappa grid: (1, 0.3, 0.1, 0.03) x kappa_d*(R), the double's linear-optimal damping (LTI, both generators equal).
Initial conditions per cell: 8 (rest relative to the blade, and 7 random angle pairs in (-pi, pi]; seed 7).
Transient 100 turns, measured 100 turns; renormalisation every quarter turn; d0 = 1e-8 in (q1, q2, q1', q2').
Steps per turn n = max(100, ceil(6 sqrt(omega_fast^2 + 4 G_max))): the double's higher linear frequency per radian, raised for gravity.
Grid kept small on purpose (lecture note, one figure): R in {1, 2, 5, 20, 100, 300}, G in {0.1, 1, 3, 10, 70}, kappa x {1, 0.1}.
"""
import json, math, os, sys, time
import numpy as np
from multiprocessing import Pool
from scipy.optimize import minimize_scalar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Double, pendulum_rhs, integrate

QUICK = '--quick' in sys.argv
RS = [1, 2, 5, 20, 100, 300]
GS = [0.1, 1, 3, 10, 70]
KREL = [1.0, 0.1]
NIC = 8
TR, MEAS = (10, 20) if QUICK else (100, 100)

Mm = np.array([[0.25, 0.125], [0.125, 0.125]])
def lti_power_over_G2(R, k):
    K = np.array([[0.5*R + 0.125, -0.125], [-0.125, 0.25*R + 0.125]])
    C = k*np.array([[2.0, -1.0], [-1.0, 1.0]])
    f = -np.array([0.5, 0.25])
    z = np.linalg.solve(K - Mm + 1j*C, f)
    return 0.5*np.real(np.conj(z) @ C @ z)
def kappa_star(R):
    r = minimize_scalar(lambda lk: -lti_power_over_G2(R, math.exp(lk)), bounds=(-8, 8), method='bounded', options={'xatol': 1e-8})
    return math.exp(r.x)
def omega_fast(R):
    K = np.array([[0.5*R + 0.125, -0.125], [-0.125, 0.25*R + 0.125]])
    return math.sqrt(max(np.linalg.eigvals(np.linalg.solve(Mm, K)).real))

def run_R(R):
    t0 = time.time()
    ks = kappa_star(R)
    rng = np.random.default_rng(7)
    ic = np.zeros((NIC, 5)); ic[1:, 0:2] = rng.uniform(-math.pi, math.pi, (NIC - 1, 2))
    cells = [(G, kr) for G in GS for kr in KREL]
    Gv = np.repeat([c[0] for c in cells], NIC); kv = np.repeat([c[1]*ks for c in cells], NIC)
    Y0 = np.tile(ic, (len(cells), 1)); Nb = Y0.shape[0]
    Yp = Y0.copy(); Yp[:, 0] += 1e-8
    sysd = Double(0.5, 0.5, 0.5, 0.5, R, np.concatenate([kv, kv]), np.concatenate([kv, kv]), g=np.concatenate([Gv, Gv]))
    F = pendulum_rhs(sysd, Om=1.0)
    n = max(100, int(math.ceil(6*math.sqrt(omega_fast(R)**2 + 4*max(GS)))))
    n -= n % 4
    h = 2*math.pi/n
    r1 = integrate(F, np.concatenate([Y0, Yp]), 0, TR*2*math.pi, h, lyap=(1e-8, n//4, [0, 1, 2, 3], 1e30))
    E0 = r1['Y'][:Nb, 4].copy()
    r2 = integrate(F, r1['Y'], TR*2*math.pi, (TR + MEAS)*2*math.pi, h, lyap=(1e-8, n//4, [0, 1, 2, 3], 0.0))
    P = (r2['Y'][:Nb, 4] - E0)/(MEAS*2*math.pi)
    res = dict(R=R, kappa_star=ks, n_per_turn=n, members=[dict(G=float(Gv[i]), kappa=float(kv[i]), krel=float(kv[i]/ks),
               ic=int(i % NIC), P=float(P[i]), lyap=float(r2['lyap'][i])) for i in range(Nb)],
               seconds=time.time() - t0, maxit=max(r1['maxit'], r2['maxit']))
    print(f'R = {R}: kappa* = {ks:.4f}, {n} steps/turn, {Nb} members, {time.time() - t0:.0f} s, chaotic '
          f'{sum(m["lyap"] > 0.01 for m in res["members"])}', flush=True)
    return res

if __name__ == '__main__':
    t0 = time.time()
    with Pool(3) as pool:
        results = pool.map(run_R, sorted(RS, key=lambda r: -r))
    results.sort(key=lambda r: r['R'])
    out = dict(RS=RS, GS=GS, KREL=KREL, NIC=NIC, TR=TR, MEAS=MEAS, seed=7, quick=QUICK, groups=results)
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'L1_map_quick.json' if QUICK else 'L1_map.json'), 'w'))
    print(f'total {time.time() - t0:.0f} s')
