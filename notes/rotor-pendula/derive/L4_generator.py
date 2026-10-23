"""L4: from swing to watts with a real geared generator (maxon RE 25 24 V, part 339152, with a GP 32 C planetary gearhead;
numbers from dossier-generator.md, maxon catalogue pages 153 and 430-431). First-order model, linear swing.

Run: python3 -I L4_generator.py   (writes L4_generator.json)
  inertia: the motor rotor J seen through ratio N adds j = J N^2/(m L^2): (1 + j) theta'' + kappa theta' + R theta = -G cos(phi)
  brake:   c = N^2 k_t k_e/(R_c + R_L), at most the short-circuit value c_sc = N^2 k_t k_e/R_c
  power at the pendulum (2.3) with R - 1 replaced by R - 1 - j; gearhead passes eta_g of it (maximum efficiency, forward;
  backdriven efficiency is not given by the datasheet: an optimistic assumption); motor friction T0 = k_t I0 (no-load current)
  costs N T0 <|thetadot|> = N T0 (2/pi) Omega Theta; the coil keeps R_c/(R_c + R_L) of the rest.
  P_load = (eta_g P_pend - P_fric) (1 - c/c_sc), maximised over c in (0, c_sc) for each catalogue ratio; a ratio whose best
  setting swings more than 0.5 rad is excluded (linear model invalid there; j close to R - 1 is an accidental resonance).
"""
import json, math, os
import numpy as np
from scipy.optimize import minimize_scalar
g = 9.80665; m, L = 0.1, 0.2
KT, KE, RC, J, I0 = 0.0208, 0.02076, 1.53, 1.47e-6 + 0.7e-7, 0.0402      # motor + gearhead inertia (0.7 g cm^2)
T0 = KT*I0
RATIOS = [(51, 0.70), (111, 0.70), (190, 0.70), (246, 0.60), (492, 0.60)]  # ratio, max efficiency (3 or 4 stages)

def p_load(Om, rp, N, eta, c):
    R = rp/L; G = g/(Om**2*L); j = J*N**2/(m*L**2); kap = c/(m*L**2*Om)
    Th = G/math.sqrt((R - 1 - j)**2 + kap**2)
    P_pend = m*L**2*Om**3*kap*Th**2/2
    c_sc = N**2*KT*KE/RC
    P_fric = N*T0*(2/math.pi)*Om*Th
    return (eta*P_pend - P_fric)*(1 - c/c_sc), P_pend, Th, j

mounts = [(rpm, f) for rpm in (400, 200, 100, 20, 14, 8) for f in (0.3, 0.6, 0.9)]
out = []
for rpm, f in mounts:
    Om = rpm*2*math.pi/60; rp = f*56.0/Om
    Pstar = m*L*g**2/(4*Om*abs(rp - L))
    best = None
    for N, eta in RATIOS:
        c_sc = N**2*KT*KE/RC
        r = minimize_scalar(lambda lc: -p_load(Om, rp, N, eta, math.exp(lc))[0], bounds=(math.log(c_sc) - 14, math.log(c_sc) - 1e-9),
                            method='bounded', options={'xatol': 1e-6})
        c = math.exp(r.x); Pl, Pp, Th, j = p_load(Om, rp, N, eta, c)
        RL = N**2*KT*KE/c - RC
        cand = dict(N=N, eta=eta, c=c, R_load=RL, P_load=Pl, P_pend=Pp, Theta=Th, j=j, fric_torque=N*T0)
        if Th > 0.5:                      # beyond the linear model: an accidental resonance (j close to R - 1)
            continue
        if best is None or Pl > best['P_load']:
            best = cand
    best.update(rpm=rpm, frac=f, Pstar=Pstar, R=rp/L)
    out.append(best)
    print(f"{rpm:3d} rpm {f*100:.0f} %: best N {best['N']:3d}, R_load {best['R_load']:7.1f} ohm, load power {best['P_load']*1e3:7.2f} mW "
          f"of P* {Pstar*1e3:6.2f} mW, swing {best['Theta']:.3f} rad ({best['P_load']/Pstar*100:5.1f} %); j = {best['j']:.2f} vs R - 1 = {rp/L - 1:.2f}; "
          f"friction torque at the pendulum {best['fric_torque']:.3f} N m")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L4_generator.json'), 'w'), indent=1)
