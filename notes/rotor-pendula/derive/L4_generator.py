"""L4: from swing to watts with a real geared generator (maxon RE 25 24 V, part 339152, with a GP 32 C planetary gearhead;
numbers from dossier-generator.md: motor rows 3-16, gearhead rows 58-62, catalogue pages 153 and 430-431).

Run: python3 -I L4_generator.py   (writes L4_generator.json)

The second blade (rod of mass m, length l, I = m l^2/3, first moment m l/2) at the hinge radius r_p; motor angle N theta.
  motor:    torque constant k_t, back-EMF constant k_e, coil resistance R_c, load resistor R_L, inductance neglected
            (L/R = 0.12 ms, far below the swing period); current k_e N thetadot/(R_c + R_L).
  brake:    electrical torque at the hinge before gear loss: c_e thetadot, c_e = N^2 k_t k_e/(R_c + R_L) <= c_sc = N^2 k_t k_e/R_c.
  gearhead: backdriven, torque at the hinge = (motor-side torque) N/eta (eta = the sheet's maximum forward efficiency: an
            optimistic assumption, the sheet gives no backdriven efficiency); inertia reflected without loss.
  friction: motor friction T0 = k_t I0 (no-load current, at about 10 000 rpm: an estimate) as Coulomb friction T0 sgn(thetadot).
  equation (blade-angle form, tau = Omega t; the unit of torque is I Omega^2):
     (1 + j) theta'' + (kappa_e/eta) theta' + f sgn(theta') + R sin(theta) + G cos(tau + theta) = 0,
     j = J N^2/I,  kappa_e = c_e/(I Omega),  f = N T0/(eta I Omega^2),  R = (m l/2) r_p/I,  G = (m l/2) g/(I Omega^2).
  linear swing with the describing function of Coulomb friction (equivalent viscous term 4 f/(pi Theta)):
     Theta^2 (R - 1 - j)^2 + (kappa_e Theta/eta + 4 f/pi)^2 = G^2      (a quadratic in Theta; no swing if 4 f/pi >= G)
  powers (unit I Omega^3):  load  kappa_e (1 - c_e/c_sc) Theta^2/2;  paid by the rotor  (kappa_e/eta) Theta^2/2 + f (2/pi) Theta.
  For each catalogue ratio the load power is maximised over c_e in (0, c_sc) with the swing kept within 0.5 rad (the formula's
  range; best_brake). L4_check.py integrates the full nonlinear equation at the chosen settings.
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.optimize import minimize_scalar
import setup as S
g = S.G0
m, L = S.M_B, S.L_B                                                 # the second blade; design.py rebinds them while sizing
KT, KE, RC, JM, I0 = 0.0208, 0.02076, 1.53, 1.47e-6, 0.0402        # RE 25 24 V, part 339152 (dossier-generator.md rows 3-16)
T0 = KT*I0
# GP 32 C: ratio, maximum efficiency, gearhead inertia at the input (kg m^2): 1 stage 80 %, 2 stages 75 %, 3 stages 70 %, 4 stages 60 %
RATIOS = [(3.7, 0.80, 1.5e-7), (14, 0.75, 0.8e-7), (33, 0.75, 0.8e-7), (51, 0.70, 0.7e-7), (111, 0.70, 0.7e-7),
          (190, 0.70, 0.7e-7), (246, 0.60, 0.7e-7), (492, 0.60, 0.7e-7)]
TORQUE_CONT = {3.7: 1.0, 14: 3.0, 33: 3.0, 51: 6.0, 111: 6.0, 190: 6.0, 246: 6.0, 492: 6.0}   # N m, max. continuous output torque
TH_MAX = 0.5


def swing(R, G, j, ke_eta, f):
    """Linear swing amplitude from the describing-function quadratic; 0 if friction holds the blade."""
    D = (R - 1 - j)**2 + ke_eta**2
    a = 4*f/math.pi
    if a >= G:
        return 0.0
    return (-ke_eta*a + math.sqrt(ke_eta**2*a**2 - D*(a**2 - G**2)))/D


def powers(Om, rp, N, eta, Jg, ce):
    I, mlc = m*L**2/3, m*L/2
    R = mlc*rp/I; G = mlc*g/(I*Om**2); j = (JM + Jg)*N**2/I; u = I*Om**3
    ke = ce/(I*Om); f = N*T0/(eta*I*Om**2); c_sc = N**2*KT*KE/RC
    Th = swing(R, G, j, ke/eta, f)
    P_load = u*ke*(1 - ce/c_sc)*Th**2/2
    P_paid = u*((ke/eta)*Th**2/2 + f*(2/math.pi)*Th)
    return dict(P_load=P_load, P_paid=P_paid, Theta=Th, j=j, kappa_e=ke, f=f, G=G, R=R, c_sc=c_sc,
                torque_peak=(ce/eta)*Om*Th + N*T0/eta)                 # brake + friction torque at the hinge, N m (swing peak)


def best_brake(Om, rp, N, eta, Jg):
    """The brake c_e in (0, c_sc) that gives the load the most power with the swing kept within TH_MAX (the formula's range):
    a log grid over 16 e-folds below the short circuit, refined by a bounded search around the best admissible point."""
    c_sc = N**2*KT*KE/RC
    def score(lc):
        p = powers(Om, rp, N, eta, Jg, math.exp(lc))
        return p['P_load'] if 0 < p['Theta'] <= TH_MAX else -1.0
    grid = [math.log(c_sc) - 16 + 16*k/800 for k in range(800)]
    vals = [score(x) for x in grid]
    k = max(range(len(grid)), key=lambda i: vals[i])
    if vals[k] <= 0:
        return None
    lo, hi = grid[max(k - 1, 0)], min(grid[min(k + 1, len(grid) - 1)], math.log(c_sc) - 1e-9)
    r = minimize_scalar(lambda x: -score(x), bounds=(lo, hi), method='bounded', options={'xatol': 1e-9})
    return math.exp(r.x if -r.fun >= vals[k] else grid[k])


def best_for(Om, rp):
    """Every ratio at its best brake, and the best of them."""
    cands = []
    for N, eta, Jg in RATIOS:
        c_sc = N**2*KT*KE/RC
        ce = best_brake(Om, rp, N, eta, Jg)
        jammed = ce is None
        p = powers(Om, rp, N, eta, Jg, c_sc*0.5 if jammed else ce)
        if jammed:
            p['P_load'] = 0.0
        p.update(N=N, eta=eta, Jg=Jg, c_e=(c_sc*0.5 if jammed else ce), jammed=jammed, fric_torque=N*T0/eta)
        p.update(R_load=N**2*KT*KE/p['c_e'] - RC, at_short=p['c_e']/c_sc, within_rating=p['torque_peak'] <= TORQUE_CONT[N])
        cands.append(p)
    ok = [p for p in cands if 0 < p['Theta'] <= TH_MAX and p['P_load'] > 0 and p['within_rating']]
    return max(ok, key=lambda p: p['P_load']), cands


if __name__ == '__main__':
    out = []
    for v, Om, rp in S.mountings():
        best, cands = best_for(Om, rp)
        Pst = S.pstar(Om)
        best.update(wind=v, rpm=S.rpm(v), Pstar=Pst, Om=Om, rp=rp,
                    others={str(p['N']): dict(P_load=p['P_load'], Theta=p['Theta'], j=p['j'], jammed=p['jammed'],
                                              within_rating=p['within_rating']) for p in cands})
        out.append(best)
        print(f"{v:.0f} m/s ({S.rpm(v):.2f} rpm): best N {best['N']:>5}, R_load {best['R_load']:8.2f} ohm (c_e/c_sc {best['at_short']:.2f}), "
              f"load {best['P_load']*1e3:7.2f} mW of P* {Pst*1e3:7.2f} mW ({best['P_load']/Pst*100:4.1f} %), paid {best['P_paid']*1e3:7.2f} mW, "
              f"swing {best['Theta']:.3f} rad, peak hinge torque {best['torque_peak']:.2f} N m; j {best['j']:.2e} vs R-1 {best['R'] - 1:.2f}; f/G {best['f']/best['G']:.4f}")
    ok = all(p['within_rating'] for p in out) and all(p['P_load'] > 0 for p in out)
    print(('PASS' if ok else 'FAIL') + ' every wind has an admissible ratio within the gearhead\'s continuous torque')
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L4_generator.json'), 'w'), indent=1)
    raise SystemExit(0 if ok else 1)
