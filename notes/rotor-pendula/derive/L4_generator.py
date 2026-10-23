"""L4: from swing to watts with a real geared generator (maxon RE 25 24 V, part 339152, with a GP 32 C planetary gearhead;
numbers from dossier-generator.md, maxon catalogue pages 153 and 430-431, stage data re-read from the GP 32 C PDF table).

Run: python3 -I L4_generator.py   (writes L4_generator.json)

Model (version 2, replaces the first-order version of commit 3f19ee0, which took the gear and friction losses off the power
after the swing was computed; here they act on the swing).  Pendulum angle theta, motor angle N theta.
  motor:    torque constant k_t, back-EMF constant k_e, coil resistance R_c, load resistor R_L, inductance neglected
            (L/R = 0.12 ms, far below the swing period); current I = k_e N thetadot/(R_c + R_L).
  brake:    electrical torque at the pendulum shaft before gear loss: c_e thetadot, c_e = N^2 k_t k_e/(R_c + R_L) <= c_sc = N^2 k_t k_e/R_c.
  gearhead: backdriven, torque at the pendulum = (motor-side torque) N/eta (eta = the sheet's maximum forward efficiency:
            an optimistic assumption, the sheet gives no backdriven efficiency); inertia reflected without loss.
  friction: motor friction T0 = k_t I0 (no-load current; at 10 000 rpm, an estimate) as Coulomb friction T0 sgn(thetadot).
  equation (blade-angle form, tau = Omega t):
     (1 + j) theta'' + (kappa_e/eta) theta' + f sgn(theta') + R sin(theta) + G cos(tau + theta) = 0,
     j = J N^2/(m L^2),  kappa_e = c_e/(m L^2 Omega),  f = N T0/(eta m L^2 Omega^2)  (friction torque / (m L^2 Omega^2); G is mgL in the same unit).
  linear swing with the describing function of Coulomb friction (equivalent viscous term 4 f/(pi Theta)):
     Theta^2 (R - 1 - j)^2 + (kappa_e Theta/eta + 4 f/pi)^2 = G^2      (a quadratic in Theta; no swing if 4 f/pi >= G)
  powers (unit m L^2 Omega^3):  load  kappa_e (1 - c_e/c_sc) Theta^2/2;  paid by the rotor  (kappa_e/eta) Theta^2/2 + f (2/pi) Theta.
  For each catalogue ratio the load power is maximised over c_e in (0, c_sc); settings that swing more than 0.5 rad are left out
  (beyond the linear model).  L4_check.py integrates the full nonlinear equation at the chosen settings.
"""
import json, math, os
from scipy.optimize import minimize_scalar
g = 9.80665; m, L = 0.1, 0.2
KT, KE, RC, JM, I0 = 0.0208, 0.02076, 1.53, 1.47e-6, 0.0402        # RE 25 24 V, part 339152 (catalogue lines 10, 12, 13, 16, 3)
T0 = KT*I0
# GP 32 C: ratio, maximum efficiency, gearhead inertia at the input (kg m^2): 1 stage 80 %, 2 stages 75 %, 3 stages 70 %, 4 stages 60 %
RATIOS = [(3.7, 0.80, 1.5e-7), (14, 0.75, 0.8e-7), (33, 0.75, 0.8e-7), (51, 0.70, 0.7e-7), (111, 0.70, 0.7e-7),
          (190, 0.70, 0.7e-7), (246, 0.60, 0.7e-7), (492, 0.60, 0.7e-7)]
TH_MAX = 0.5

def swing(R, G, j, ke_eta, f):
    """Linear swing amplitude from the describing-function quadratic; 0 if friction holds the pendulum."""
    D = (R - 1 - j)**2 + ke_eta**2
    a = 4*f/math.pi
    if a >= G:
        return 0.0
    return (-ke_eta*a + math.sqrt(ke_eta**2*a**2 - D*(a**2 - G**2)))/D

def powers(Om, rp, N, eta, Jg, ce):
    R = rp/L; G = g/(Om**2*L); j = (JM + Jg)*N**2/(m*L**2); u = m*L**2*Om**3
    ke = ce/(m*L**2*Om); f = N*T0/(eta*m*L**2*Om**2); c_sc = N**2*KT*KE/RC
    Th = swing(R, G, j, ke/eta, f)
    P_load = u*ke*(1 - ce/c_sc)*Th**2/2
    P_paid = u*((ke/eta)*Th**2/2 + f*(2/math.pi)*Th)
    return dict(P_load=P_load, P_paid=P_paid, Theta=Th, j=j, kappa_e=ke, f=f, G=G, R=R, c_sc=c_sc)

if __name__ == '__main__':
    mounts = [(rpm, fr) for rpm in (400, 200, 100, 20, 14, 8) for fr in (0.3, 0.6, 0.9)]
    out = []
    for rpm, fr in mounts:
        Om = rpm*2*math.pi/60; rp = fr*56.0/Om
        Pstar = m*L*g**2/(4*Om*abs(rp - L))
        cands = []
        for N, eta, Jg in RATIOS:
            c_sc = N**2*KT*KE/RC
            r = minimize_scalar(lambda lc: -powers(Om, rp, N, eta, Jg, math.exp(lc))['P_load'],
                                bounds=(math.log(c_sc) - 16, math.log(c_sc) - 1e-9), method='bounded', options={'xatol': 1e-7})
            ce = math.exp(r.x); p = powers(Om, rp, N, eta, Jg, ce)
            p.update(N=N, eta=eta, Jg=Jg, c_e=ce, R_load=N**2*KT*KE/ce - RC, fric_torque=N*T0/eta, at_short=ce/c_sc)
            cands.append(p)
        ok = [p for p in cands if p['Theta'] <= TH_MAX and p['P_load'] > 0]
        best = max(ok, key=lambda p: p['P_load'])
        best.update(rpm=rpm, frac=fr, Pstar=Pstar, Om=Om, rp=rp,
                    others={str(p['N']): dict(P_load=p['P_load'], Theta=p['Theta'], j=p['j'], jammed=p['Theta'] == 0.0)
                            for p in cands})
        out.append(best)
        jam = [str(p['N']) for p in cands if p['Theta'] == 0.0]
        print(f"{rpm:3d} rpm {fr*100:.0f} %: best N {best['N']:>5}, R_load {best['R_load']:8.2f} ohm (c_e/c_sc {best['at_short']:.2f}), "
              f"load {best['P_load']*1e3:6.2f} mW of P* {Pstar*1e3:6.2f} mW ({best['P_load']/Pstar*100:4.1f} %), paid {best['P_paid']*1e3:6.2f} mW, "
              f"swing {best['Theta']:.3f} rad; j {best['j']:.2f} vs R-1 {best['R'] - 1:.2f}; f/G {best['f']/best['G']:.2f}"
              + (f"; jammed: N = {', '.join(jam)}" if jam else ''))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L4_generator.json'), 'w'), indent=1)
