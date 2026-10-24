"""L4: choose the generator's settings in the full equation (L4_full.py, version 3: the gear loss goes with every power that
flows through the gearhead, the inertial one included).  For every mounting, the ratios 14, 33, 51 and 111 of the GP 32 C and
brakes c_e = factor x the formula's best c_e for that ratio (L4_generator.py), all in one batch, 1000 steps per turn, 100 turns
to settle and 20 to measure.  A setting counts only if the motion is steady (the two halves of the measuring window agree to
1 %), the swing stays below 0.5 rad and the motor stays below the gearhead's 8000 rpm input limit.
Writes L4_scan_<part>.json.  Run: python3 -I L4_scan.py [part] [parts]   (the mountings are split between processes)
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import radau_step
from L4_generator import powers, RATIOS, KT, KE, RC, JM, T0, m, L, g, TH_MAX
from L4_full import make_rhs
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
part = int(sys.argv[1]) if len(sys.argv) > 1 else 0; parts = int(sys.argv[2]) if len(sys.argv) > 2 else 1
res = json.load(open(os.path.join(HERE, 'L4_generator.json')))
FACT = [0.25, 0.35, 0.5, 0.7, 1.0, 1.4, 2.0, 2.8, 4.0]
gear = {N: (eta, Jg) for N, eta, Jg in RATIOS}
rows = []
for i, r in enumerate(res):
    if i % parts != part:
        continue
    for N in (14, 33, 51, 111):
        eta, Jg = gear[N]; c_sc = N**2*KT*KE/RC
        o = minimize_scalar(lambda lc: -powers(r['Om'], r['rp'], N, eta, Jg, math.exp(lc))['P_load'],
                            bounds=(math.log(c_sc) - 16, math.log(c_sc) - 1e-9), method='bounded', options={'xatol': 1e-7})
        c0 = math.exp(o.x); th0 = powers(r['Om'], r['rp'], N, eta, Jg, c0)['Theta']
        for k in FACT:
            rows.append(dict(i=i, N=N, eta=eta, Jg=Jg, c_e=min(k*c0, 0.98*c_sc), fac=k, Om=r['Om'], rp=r['rp'], th0=max(th0, 1e-2)))
n = len(rows)
Om = np.array([q['Om'] for q in rows]); R = np.array([q['rp']/L for q in rows]); G = g/(Om**2*L)
Nn = np.array([float(q['N']) for q in rows]); eta = np.array([q['eta'] for q in rows])
j = (JM + np.array([q['Jg'] for q in rows]))*Nn**2/(m*L**2)
ce = np.array([q['c_e'] for q in rows]); ke = ce/(m*L**2*Om); f0 = Nn*T0/(m*L**2*Om**2)
keep = 1 - ce/(Nn**2*KT*KE/RC); th0 = np.array([q['th0'] for q in rows])
F = make_rhs(R, G, j, f0, ke, eta, keep, 1e-3*th0, 1e-3*G*th0)

nst, settle, meas = 1000, 100, 20
h = 2*math.pi/nst; Y = np.zeros((n, 5))
for k in range(nst*(settle + meas)):
    if k == nst*settle:
        Y0 = Y.copy(); thmax = np.zeros(n); wmax = np.zeros(n)
    if k == nst*(settle + meas//2):
        Yh = Y.copy()
    Y, _ = radau_step(F, k*h, Y, h)
    if k >= nst*settle:
        thmax = np.maximum(thmax, np.abs(Y[:, 0])); wmax = np.maximum(wmax, np.abs(Y[:, 1]))
    if k % (nst*10) == 0:
        print(f'turn {k//nst}', flush=True)
u = m*L**2*Om**3; T = 2*math.pi*meas
Pl = (Y[:, 2] - Y0[:, 2])/T*u; Pp = (Y[:, 3] - Y0[:, 3])/T*u; Pf = (Y[:, 4] - Y0[:, 4])/T*u
Pl1 = (Yh[:, 2] - Y0[:, 2])/(T/2)*u; Pl2 = (Y[:, 2] - Yh[:, 2])/(T/2)*u
steady = np.abs(Pl1/np.maximum(Pl2, 1e-30) - 1) < 0.01
mrpm = wmax*Om*Nn*60/(2*math.pi)
ok = steady & (thmax <= TH_MAX) & (mrpm <= 8000) & (Pl > 0)
out = []
for i in sorted(set(q['i'] for q in rows)):
    r = res[i]; idx = [q for q in range(n) if rows[q]['i'] == i]
    good = [q for q in idx if ok[q]]
    b = max(good, key=lambda q: Pl[q])
    fq = next(q for q in idx if rows[q]['N'] == r['N'] and rows[q]['fac'] == 1.0)
    out.append(dict(rpm=r['rpm'], frac=r['frac'], N=rows[b]['N'], eta=rows[b]['eta'], Jg=rows[b]['Jg'], c_e=rows[b]['c_e'],
                    fac=rows[b]['fac'], R_load=rows[b]['N']**2*KT*KE/rows[b]['c_e'] - RC, P_load=float(Pl[b]), P_paid=float(Pp[b]),
                    P_fric=float(Pf[b]), Theta=float(thmax[b]), motor_rpm=float(mrpm[b]), th0=rows[b]['th0'],
                    P_load_formula_setting=float(Pl[fq]), edge=rows[b]['fac'] in (FACT[0], FACT[-1]),
                    rejected=[dict(N=rows[q]['N'], fac=rows[q]['fac'], P_load=float(Pl[q]), Theta=float(thmax[q]), motor_rpm=float(mrpm[q]),
                                   steady=bool(steady[q])) for q in idx if not ok[q] and Pl[q] > Pl[b]]))
    o = out[-1]
    print(f"{r['rpm']:3d} rpm {r['frac']*100:.0f} %: best N {o['N']}, factor {o['fac']}, R_L {o['R_load']:8.2f} ohm: load {o['P_load']*1e3:7.3f} mW, "
          f"paid {o['P_paid']*1e3:7.2f} mW (friction {o['P_fric']*1e3:6.2f}), swing {o['Theta']:.3f} rad, motor {o['motor_rpm']:5.0f} rpm"
          f"{' (edge of the scan)' if o['edge'] else ''}; at the formula's setting (N {r['N']}) {o['P_load_formula_setting']*1e3:7.3f} mW; "
          f"better but rejected: {len(o['rejected'])}")
json.dump(out, open(os.path.join(HERE, f'L4_scan_{part}.json'), 'w'), indent=1)
