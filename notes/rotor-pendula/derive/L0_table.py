"""L0 at Sol's 18 mountings: the time-invariant linear theory (parametric term dropped, closed form) and the time-periodic
linear theory (parametric term kept, solved exactly by Hill's method), against Sol's stored runs.

Run: python3 -I L0_table.py   (PASS/FAIL lines; exit 1 on any FAIL)

Blade-angle form at uniform rotation, linearised in theta (L0_single.py, equation (3) with eps = 0):
    theta'' + kappa theta' + R theta - G theta sin(phi) = -G cos(phi)          (' = d/dphi)
LTI: drop G theta sin(phi):  theta = Re[A e^{i phi}],  A = -G/(R - 1 + i kappa),  P_hat = kappa <theta'^2> = kappa |A|^2/2
LTP (Hill): theta = sum_n a_n e^{i n phi},  (R - n^2 + i kappa n) a_n - (G/2i)(a_{n-1} - a_{n+1}) = -(G/2)(delta_{n,1} + delta_{n,-1})
            P_hat = kappa sum_n n^2 |a_n|^2.   Physical power P = m L^2 Omega^3 P_hat.
"""
import csv, math, os, sys
import numpy as np
from scipy.optimize import minimize_scalar

g, m, L = 9.80665, 0.1, 0.2      # standard gravity, as in Sol's study (his linear rows are 0.07 % below g = 9.81)
HERE = os.path.dirname(os.path.abspath(__file__))
SUMMARY = os.path.join(HERE, '../../../public/portfolios/rotor-pendula/study/data/summary.csv')

def P_hat_lti(R, G, k): return k*G**2/(2*((R - 1)**2 + k**2))

def P_hat_ltp(R, G, k, N=40):
    n = np.arange(-N, N + 1); K = len(n)
    A = np.zeros((K, K), complex); rhs = np.zeros(K, complex)
    for i, nn in enumerate(n):
        A[i, i] = R - nn**2 + 1j*k*nn
        if i > 0:     A[i, i - 1] = -G/(2j)        # a_{n-1}
        if i < K - 1: A[i, i + 1] = +G/(2j)        # a_{n+1}
        if abs(nn) == 1: rhs[i] = -G/2
    a = np.linalg.solve(A, rhs)
    return k*np.sum(n**2*np.abs(a)**2), a

fails = 0
def check(name, ok):
    global fails
    fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name)

rows = {r['name']: r for r in csv.DictReader(open(SUMMARY))}
print(f"{'mounting':>14} {'R':>7} {'1/Gam':>6} {'P*_LTI':>8} {'k*_LTI':>8} {'P*_LTP':>8} {'k*_LTP':>8} {'Sol_k':>8} "
      f"{'Sol_lin':>8} {'LTP@Sol':>8} {'Sol_NL':>8} {'Th*':>6} {'fric%':>6} {'share':>9}")
worst_ltisol = 0; refined = []; ltp_err = []; worst_lin = 0; worst_k = 0; worst_lti_nl = 0; worst_ltp_nl = 0; Ps = []; shares = []; worst_conv = 0
for size, rpms in (('large', (20, 14, 8)), ('small', (400, 200, 100))):
    for rpm in rpms:
        Om = rpm*2*math.pi/60
        Rrot = 56.0/Om
        for pct in (30, 60, 90):
            rp = pct/100*Rrot; R = rp/L; G = g/(Om**2*L); unit = m*L**2*Om**3
            name = f'map_{size}_{rpm}_{pct}_single'
            sol_nl = float(rows[name]['mean_power_W']); sol_lin = float(rows[name + '_linear']['mean_power_W'])
            sol_c = float(rows[name]['c_N_m_s_per_rad']); sol_k = sol_c/(m*L**2*Om)
            kl = R - 1; Pl = P_hat_lti(R, G, kl)*unit
            opt = minimize_scalar(lambda k: -P_hat_ltp(R, G, k)[0], bounds=(0.2*kl, 2*kl), method='bounded',
                                  options={'xatol': 1e-9*kl})
            kp = opt.x; Pp = -opt.fun*unit
            Pp_sol = P_hat_ltp(R, G, sol_k)[0]*unit
            Pl_sol = P_hat_lti(R, G, sol_k)*unit
            worst_ltisol = max(worst_ltisol, abs(Pl_sol/sol_lin - 1))
            refined.append((rpm, pct)) if abs(sol_k/kl - 1) > 1e-4 else None
            ltp_err.append((Pp_sol/sol_nl - 1, rpm, pct))
            conv = abs(P_hat_ltp(R, G, sol_k, N=20)[0]/P_hat_ltp(R, G, sol_k, N=40)[0] - 1)
            worst_conv = max(worst_conv, conv)
            Th = G/(math.sqrt(2)*abs(R - 1))
            # ball-bearing friction (SKF approximation M = 0.5 mu F d, mu = 0.0015, bore 5 mm), rod tension m r_p Omega^2
            Tf = 0.5*0.0015*m*rp*Om**2*0.005
            fric = 4*math.sqrt(2)/math.pi*Tf/(m*g*L)
            Pturb = 0.5*1.225*math.pi*Rrot**2*8.0**3*0.45
            share = sol_nl/Pturb
            Ps.append(sol_nl); shares.append(share)
            worst_lin = max(worst_lin, abs(Pp_sol/sol_lin - 1)); worst_k = max(worst_k, abs(kp/sol_k - 1))
            worst_lti_nl = max(worst_lti_nl, abs(Pl/sol_nl - 1)); worst_ltp_nl = max(worst_ltp_nl, abs(Pp/sol_nl - 1))
            print(f"{rpm:>4} rpm {pct:>2} % {R:7.2f} {1/(rp*Om**2/g):6.3f} {Pl*1e3:8.3f} {kl:8.3f} {Pp*1e3:8.3f} {kp:8.3f} "
                  f"{sol_k:8.3f} {sol_lin*1e3:8.4f} {Pp_sol*1e3:8.4f} {sol_nl*1e3:8.4f} {Th:6.3f} {fric*100:6.3f} {share:9.2e}")
print(f"Sol's nonlinear single powers span {min(Ps)*1e3:.3f} .. {max(Ps)*1e3:.3f} mW; share of turbine output up to {max(shares):.2e}")
print(f"Hill truncation N=20 vs N=40: worst relative change {worst_conv:.1e}")
check(f"LTI closed form at Sol's damping reproduces Sol's stored linear rows (worst {worst_ltisol*100:.4f} %, < 0.01 %)",
      worst_ltisol < 1e-4)
check(f"Sol's damping is the LTI optimum kappa = R - 1 except where his report says he refined it nonlinearly: {refined}",
      refined == [(14, 30), (8, 30)])
check(f"LTI closed form P* within 1 % of Sol's nonlinear runs at all 18 mountings (worst {worst_lti_nl*100:.2f} %)", worst_lti_nl < 0.01)
e, r_, p_ = max(ltp_err)
print(f"FINDING  keeping the parametric term alone (Hill, LTP) at Sol's damping overshoots Sol's nonlinear power by up to "
      f"{e*100:.1f} % ({r_} rpm, {p_} %): its power correction is second order in 1/Gamma, the order of the theta^2 and theta^3 "
      f"terms it drops; the LTI closed form is the consistent first approximation")
check("Sol's span 9.55-57.1 mW", round(min(Ps)*1e3, 2) == 9.55 and round(max(Ps)*1e3, 1) == 57.1)
check("rotor share <= 7.2e-5", round(max(shares)*1e5, 1) == 7.2)
# the optimal generator torque amplitude is m g L / sqrt(2) at every mounting (LTI): c* Omega Theta* = m L^2 Omega^2 (R-1) G/(sqrt2 (R-1))
print(f"optimal generator torque amplitude (LTI) m g L / sqrt(2) = {m*g*L/math.sqrt(2):.4f} N m at every mounting")
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
