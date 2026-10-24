"""L4: the accidental resonance at 400 rpm, pivot at 30 %, ratio 51 (j = 1.00 against R - 1 = 1.005).
Full equation, 2000 steps per turn, 200 turns to settle (a resonance settles slowly) and 40 to measure, with the gearhead's
inertial torque (a) passed without loss (version 2 of the model) and (b) charged with the gear loss like every other power
(version 3, L4_full.py), over a range of brakes; and in version 3, the pivot moved by -2 % to +2 % at its best brake.
Writes L4_resonance.json.   Run: python3 -I L4_resonance.py"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import radau_step
from L4_generator import KT, KE, RC, JM, T0, m, L, g
from L4_full import make_rhs, make_rhs_v2
HERE = os.path.dirname(os.path.abspath(__file__))
Om = 400*2*math.pi/60; rp0 = 0.3*56.0/Om; Nr, eta, Jg = 51, 0.70, 0.7e-7
c_sc = Nr**2*KT*KE/RC; Pstar = m*L*g**2/(4*Om*abs(rp0 - L))
j = (JM + Jg)*Nr**2/(m*L**2); G = g/(Om**2*L); f0 = Nr*T0/(m*L**2*Om**2)

def run(cs, rps, version, nst=2000, settle=200, meas=40):
    cs = np.asarray(cs, float); rps = np.asarray(rps, float); n = len(cs)
    R = rps/L; ke = cs/(m*L**2*Om); keep = 1 - cs/c_sc; e = np.full(n, eta)
    F = (make_rhs(R, G, j, f0, ke, e, keep, 3e-4, 3e-4*G*0.3) if version == 3 else make_rhs_v2(R, G, j, f0, ke, e, keep, 3e-4))
    h = 2*math.pi/nst; Y = np.zeros((n, 5)); u = m*L**2*Om**3
    for k in range(nst*(settle + meas)):
        if k == nst*settle:
            Y0 = Y.copy(); thmax = np.zeros(n)
        if k == nst*(settle + meas//2):
            Yh = Y.copy()
        Y, _ = radau_step(F, k*h, Y, h)
        if k >= nst*settle:
            thmax = np.maximum(thmax, np.abs(Y[:, 0]))
    T = 2*math.pi*meas
    Pl = (Y[:, 2] - Y0[:, 2])/T*u; Pp = (Y[:, 3] - Y0[:, 3])/T*u; P1 = (Yh[:, 2] - Y0[:, 2])/(T/2)*u
    return Pl, Pp, thmax, P1

fr_c = [0.0006, 0.0013, 0.002, 0.004, 0.01, 0.03, 0.1, 0.3]
print(f'400 rpm, 30 %, ratio 51: R - 1 = {rp0/L - 1:.4f}, j = {j:.4f}, net stiffness {rp0/L - 1 - j:+.4f}; P* = {Pstar*1e3:.2f} mW')
out = dict(R1=rp0/L - 1, j=j, Pstar=Pstar)
for v in (2, 3):
    Pl, Pp, th, P1 = run([x*c_sc for x in fr_c], [rp0]*len(fr_c), v)
    print(f'version {v}:')
    for x, a, b, t, c in zip(fr_c, Pl, Pp, th, P1):
        print(f'  c_e = {x:.4f} c_sc (R_L = {RC/x - RC:7.1f} ohm): load {a*1e3:7.2f} mW (first half {c*1e3:7.2f}), rotor pays {b*1e3:7.2f} mW, swing {t:.3f} rad')
    out[f'v{v}'] = [dict(frac=x, R_load=RC/x - RC, P_load=float(a), P_paid=float(b), Theta=float(t), steady=bool(abs(c/a - 1) < 0.01))
                    for x, a, b, t, c in zip(fr_c, Pl, Pp, th, P1)]
best = max(out['v3'], key=lambda q: q['P_load'] if q['Theta'] <= 0.5 else -1)
dr = [-0.02, -0.01, 0.0, 0.01, 0.02]
Pl2, Pp2, th2, P12 = run([best['frac']*c_sc]*len(dr), [rp0*(1 + d) for d in dr], 3)
print(f"version 3, best brake c_e = {best['frac']} c_sc; pivot moved:")
for d, a, b, t in zip(dr, Pl2, Pp2, th2):
    print(f'  {d*100:+.1f} % (net stiffness {rp0*(1 + d)/L - 1 - j:+.4f}): load {a*1e3:7.2f} mW, rotor pays {b*1e3:7.2f} mW, swing {t:.3f} rad')
out['pivot'] = [dict(d=d, s=rp0*(1 + d)/L - 1 - j, P_load=float(a), P_paid=float(b), Theta=float(t)) for d, a, b, t in zip(dr, Pl2, Pp2, th2)]
json.dump(out, open(os.path.join(HERE, 'L4_resonance.json'), 'w'), indent=1)
