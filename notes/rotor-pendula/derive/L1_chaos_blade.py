"""L1: is the second blade ever chaotic?  Its equation, theta'' + kappa theta' + R sin(theta) + G cos(phi + theta) = 0, is a
periodically driven, damped pendulum, which can be chaotic for some (R, G, kappa).  Largest Lyapunov exponent at the three winds
of setup.py, at the best brake kappa* and at kappa*/10 and kappa*/100, from 8 starting states each (rest on the blade's line, and 7
random angles in (-pi, pi] with random rates up to 2 Omega: some start tumbling).

Run: python3 -I L1_chaos_blade.py   (writes L1_chaos_blade.json; PASS/FAIL on the numerics only: regular or chaotic is a result)
Transient 100 turns, measured 100 turns; renormalisation every quarter turn; d0 = 1e-8 in (theta, theta'/Omega); 240 steps per turn
(and 480 for every cell, to see that the exponents do not depend on the step).  An exponent below 1e-3 per turn is regular.
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import RigidBlade, pendulum_rhs, integrate
import setup as S

m, l = S.M_B, S.L_B; I, mlc = m*l*l/3, m*l/2
rng = np.random.default_rng(7)
ic = np.zeros((8, 2)); ic[1:, 0] = rng.uniform(-math.pi, math.pi, 7); ic[1:, 1] = rng.uniform(-2, 2, 7)   # rates in units of Omega
out = []; fails = 0
TR, MEAS = 100, 100
for v, Om, rp in S.mountings():
    R = mlc*rp/I; G = mlc*S.G0/(I*Om**2); ks = R - 1
    for krel in (1.0, 0.1, 0.01):
        lyaps = {}
        for nst in (240, 480):
            c = krel*ks*I*Om; Tt = 2*math.pi/Om; h = Tt/nst
            F = pendulum_rhs(RigidBlade(m, l, rp, np.full(16, c)), Om=Om)
            Y0 = np.zeros((16, 3)); Y0[:8, 0] = ic[:, 0]; Y0[:8, 1] = ic[:, 1]*Om
            Y0[8:] = Y0[:8]; Y0[8:, 0] += 1e-8
            r = integrate(F, Y0, 0, (TR + MEAS)*Tt, h, lyap=(1e-8, nst//4, [0, 1], TR*Tt, [1.0, 1/Om]))
            lyaps[nst] = r['lyap']*Tt                      # per turn
            final = r['Y'][:8]
        lam = lyaps[240]; agree = np.max(np.abs(lyaps[240] - lyaps[480]))
        trail = final[:, 0]                                  # final angles, to see whether all starts end on the same motion
        same = np.ptp(np.mod(trail + math.pi, 2*math.pi)) < 1e-6
        kap = krel*ks; lin = 2*math.pi*max(np.roots([1, kap, R]).real)     # decay rate per turn of the small swing, s^2 + kappa s + R = 0
        out.append(dict(wind=v, R=R, G=G, krel=krel, kappa=kap, lyap=lam.tolist(), lyap480=lyaps[480].tolist(), same_end=bool(same), lin=lin))
        print(f'{v:.0f} m/s, R {R:.1f}, G {G:.2f}, kappa = {krel} kappa* = {krel*ks:.3f}: largest Lyapunov per turn {lam.max():+.2e} '
              f'(min {lam.min():+.2e}; small-swing decay {lin:+.2e}); 240 vs 480 steps differ by {agree:.1e}; all 8 starts end on one motion: {same}', flush=True)
regular = all(max(o['lyap']) < 1e-3 for o in out)
print('RESULT: ' + ('every start at every wind and brake ends on a regular motion (largest exponent < 1e-3 per turn)' if regular
                    else 'chaotic motion found: ' + ', '.join(f"{o['wind']:.0f} m/s kappa {o['krel']} kappa*" for o in out if max(o['lyap']) >= 1e-3)))
ok = all(abs(a - b) < 1e-2*(1 + abs(b)) for o in out for a, b in zip(o['lyap'], o['lyap480']))
print(('PASS' if ok else 'FAIL') + ' the exponents do not depend on the step (240 and 480 steps per turn agree within 1 % of the exponent, or 0.01 per turn near zero: enough to fix its sign and size)')
lin_ok = all(abs(max(o['lyap'])/o['lin'] - 1) < 0.05 for o in out)
print(('PASS' if lin_ok else 'FAIL') + ' the largest exponent is the decay rate of the small swing, max real part of the roots of s^2 + kappa s + R, within 5 %: '
      + ', '.join(f"{max(o['lyap'])/o['lin'] - 1:+.1%}" for o in out))
ok = ok and lin_ok
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L1_chaos_blade.json'), 'w'), indent=1)
raise SystemExit(0 if ok else 1)
