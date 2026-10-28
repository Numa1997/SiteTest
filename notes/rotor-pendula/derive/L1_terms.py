"""Which neglected term moves the harvested power, and by how much? The small-swing theory (2.1) against (1.6) with one
nonlinear piece switched on at a time, at the best brake kappa* = R - 1, in the rotor angle as the clock:
  param: + G theta sin(phi)          (the term section 2.1 drops)
  sin:   R sin(theta) for R theta     (the softer spring)
  grav:  G cos(phi + theta) whole     (gravity's push, both its terms)
  full:  all of it                    (1.6)
Each run: 60 turns from rest, the last 20 measured on 2000 points per turn; the power is kappa <theta'^2> (times I Omega^3).
Run: python3 -I L1_terms.py   (about three minutes; writes L1_terms.json)
"""
import json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import setup as S
g, rp, l = S.G0, S.R_ROT, S.L_B
R = 3*rp/(2*l); ks = R - 1
def run(G, kind, turns=60, meas=20):
    def f(p, y):
        th, w = y
        spring = R*math.sin(th) if kind in ('sin', 'full') else R*th
        if kind in ('grav', 'full'): push = -G*math.cos(p + th)
        elif kind == 'param': push = -G*math.cos(p) + G*th*math.sin(p)
        else: push = -G*math.cos(p)
        return [w, push - spring - ks*w]
    T0, T1 = 2*math.pi*(turns - meas), 2*math.pi*turns
    s = solve_ivp(f, [0, T1], [0, 0], method='Radau', rtol=1e-11, atol=1e-13, dense_output=True, max_step=0.05)
    p = np.linspace(T0, T1, meas*2000 + 1)[:-1]; y = s.sol(p)
    return float(np.mean(y[1]**2)), float(np.mean(y[0]))
out = []
for v, Om, _ in S.mountings():
    G = 3*g/(2*l*Om**2); base, _ = run(G, 'lin')
    row = dict(wind=v, G=G)
    for k in ('param', 'sin', 'grav', 'full'):
        P, mean = run(G, k); row[k] = P/base - 1; row[k + '_mean'] = mean
    out.append(row)
    print(f"{v:.0f} m/s: " + ', '.join(f"{k} {100*row[k]:+.3f} %" for k in ('param', 'sin', 'grav', 'full')), flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L1_terms.json'), 'w'), indent=1)
