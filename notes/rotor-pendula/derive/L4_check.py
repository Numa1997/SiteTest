"""L4: the numbers the notes quote for the geared generator, at the settings L4_scan.py chose in the full equation
(L4_full.py, version 3), recomputed with a finer step and a narrower smoothing band, and set beside the describing-function
formula (7.6)-(7.7) of L4_generator.py at the same settings.

Run: python3 -I L4_check.py [steps per turn] [band factor]   (defaults 2000 and 1e-3; band = factor x swing scale)
Writes L4_check_<steps>.json.  L4_converge.py compares the 2000- and 4000-step runs.

Jamming rests on a static argument, exact for a rod that starts at rest on the blade's line: if the friction torque exceeds
gravity's largest torque, N T0/eta > m g L, the rod never starts (the centrifugal torque is zero there).
"""
import glob, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import radau_step
from L4_generator import powers, KT, KE, RC, JM, T0, m, L, g, RATIOS
from L4_full import make_rhs

HERE = os.path.dirname(os.path.abspath(__file__))
nst = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
efac = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-3
gen = {(r['rpm'], r['frac']): r for r in json.load(open(os.path.join(HERE, 'L4_generator.json')))}
rows = sorted([x for p in glob.glob(os.path.join(HERE, 'L4_scan_[0-9].json')) for x in json.load(open(p))],
              key=lambda x: (x['wind'], x['frac']))
assert len(rows) == 9, len(rows)
n = len(rows)
Om = np.array([gen[(r['rpm'], r['frac'])]['Om'] for r in rows]); rp = np.array([gen[(r['rpm'], r['frac'])]['rp'] for r in rows])
R = rp/L; G = g/(Om**2*L); Nn = np.array([float(r['N']) for r in rows]); eta = np.array([r['eta'] for r in rows])
j = (JM + np.array([r['Jg'] for r in rows]))*Nn**2/(m*L**2)
ce = np.array([r['c_e'] for r in rows]); ke = ce/(m*L**2*Om); f0 = Nn*T0/(m*L**2*Om**2)
keep = 1 - ce/(Nn**2*KT*KE/RC); sc = np.array([max(r['Theta'], 1e-2) for r in rows])
F = make_rhs(R, G, j, f0, ke, eta, keep, efac*sc, efac*G*sc)
settle, meas = 100, 20
h = 2*math.pi/nst; Y = np.zeros((n, 5))
for k in range(nst*(settle + meas)):
    if k == nst*settle:
        Y0 = Y.copy(); thmax = np.zeros(n)
    Y, _ = radau_step(F, k*h, Y, h)
    if k >= nst*settle:
        thmax = np.maximum(thmax, np.abs(Y[:, 0]))
u = m*L**2*Om**3; T = 2*math.pi*meas
Pl = (Y[:, 2] - Y0[:, 2])/T*u; Pp = (Y[:, 3] - Y0[:, 3])/T*u; Pf = (Y[:, 4] - Y0[:, 4])/T*u
out = []
for i, r in enumerate(rows):
    fo = powers(Om[i], rp[i], r['N'], r['eta'], r['Jg'], r['c_e'])          # the formula (7.6)-(7.7) at the same setting
    out.append(dict(wind=r['wind'], rpm=r['rpm'], frac=r['frac'], N=r['N'], eta=r['eta'], c_e=r['c_e'], R_load=r['R_load'], Pstar=gen[(r['rpm'], r['frac'])]['Pstar'],
                    R=float(R[i]), j=float(j[i]), f_over_G=float(f0[i]/(eta[i]*G[i])), P_load=float(Pl[i]), P_paid=float(Pp[i]), P_fric=float(Pf[i]),
                    Theta=float(thmax[i]), P_load_formula=fo['P_load'], P_paid_formula=fo['P_paid'], Theta_formula=fo['Theta'],
                    P_load_scan=r['P_load']))
    print(f"{r['wind']:.0f} m/s {r['frac']*100:.0f} %, N {r['N']:3d}, R_L {r['R_load']:8.2f} ohm: load {Pl[i]*1e3:7.3f} mW (scan, 1000 steps: "
          f"{r['P_load']*1e3:7.3f}), paid {Pp[i]*1e3:7.2f} mW, friction {Pf[i]*1e3:6.2f} mW, swing {thmax[i]:.3f} rad; formula: load "
          f"{fo['P_load']*1e3:7.3f} mW ({(Pl[i]/fo['P_load'] - 1)*100 if fo['P_load'] > 0 else float('nan'):+.1f} %), swing {fo['Theta']:.3f} rad")
static = [(N, eta_, N*T0/eta_ > m*g*L) for N, eta_, _ in RATIOS]
print('jam (static argument, friction torque N T0/eta > m g L):', ', '.join(f'N = {N}: {"jams" if s else "does not jam"}' for N, _, s in static))
json.dump(out, open(os.path.join(HERE, f'L4_check_{nst}.json'), 'w'), indent=1)
used_jam = [r['N'] for r in rows if r['N']*T0/r['eta'] > m*g*L]
print(('PASS' if not used_jam else 'FAIL') + ' no ratio chosen for the table jams the rod' + (f' (jams: {used_jam})' if used_jam else ''))
sys.exit(0 if not used_jam else 1)
