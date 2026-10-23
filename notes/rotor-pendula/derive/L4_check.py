"""L4 second route: the full nonlinear pendulum with the gearbox's reflected inertia J N^2 added to m L^2 and the electrical
brake c, integrated with the Radau engine, against the linear formula used in L4_generator.py (R - 1 -> R - 1 - j).
Run: python3 -I L4_check.py   (PASS if within 1 % at the mountings where the swing is under 0.3 rad)"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import radau_step
g = 9.80665; m, L = 0.1, 0.2; J = 1.47e-6 + 0.7e-7
res = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L4_generator.json')))
fails = 0
for r in res:
    if r['Theta'] > 0.3 or r['rpm'] not in (200, 20, 8):
        continue
    Om = r['rpm']*2*math.pi/60; rp = r['frac']*56.0/Om; N = r['N']; c = r['c']; I = m*L**2 + J*N**2
    def F(t, Y):
        q, w = Y[:, 0], Y[:, 1]
        a = (-m*L*(Om**2*rp*np.sin(q) + g*np.cos(Om*t + q)) - c*w)/I
        return np.stack([w, a, c*w**2], axis=1)
    Tt = 2*math.pi/Om; h = Tt/200; Y = np.zeros((1, 3))
    for k in range(200*60):
        if k == 200*40: E0 = Y[0, 2]
        Y, _ = radau_step(F, k*h, Y, h)
    Pn = (Y[0, 2] - E0)/(20*Tt)
    ok = abs(Pn/r['P_pend'] - 1) < 0.01
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} {r['rpm']} rpm {r['frac']*100:.0f} %, N = {N}: nonlinear {Pn*1e3:.4f} mW, linear {r['P_pend']*1e3:.4f} mW "
          f"({(Pn/r['P_pend'] - 1)*100:+.2f} %)")
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
