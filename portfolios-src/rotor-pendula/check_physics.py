#!/usr/bin/env python3
"""Independent physics checks of the Rotor Pendula study.  Every constant is typed again here; nothing is imported from
the study's own scripts.  Run: python3 -I check_physics.py   (about a minute; exit 1 on any FAIL)

  1. SymPy: the pendulum on a turning blade from its Lagrangian -> equation (1.5) in blade-angle form; the small-swing
     solution, the best brake kappa* = |R - 1| (2.4), the 45 degree lag and P* (2.5); the trail identity (3.3).
  2. SciPy: the full single-pendulum equation re-integrated with solve_ivp (Radau, tight tolerances) at six of the nine
     mountings, at the stored brake, against the stored powers (data/L1_mountings.json, written by the notes' own engine).
  3. The generator: the brake constant from the circuit (7.1), the load share (7.2), the jamming ratio, and the full
     equation (7.8) re-integrated with solve_ivp at two mountings against data/L4_check_2000.json.
"""
import json, math, pathlib, sys
import numpy as np, sympy as sp
from scipy.integrate import solve_ivp

ROOT = pathlib.Path(__file__).resolve().parent
g = 9.80665; m = 0.5; L = 0.1                     # the single pendulum
LAM, RTIP = 7.55, 63.0                            # NREL 5 MW: tip-speed ratio of peak Cp, rotor radius
fails = []
def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what)
    if not ok: fails.append(what)

# ---- 1. SymPy -----------------------------------------------------------------------------------------------------
t = sp.symbols('t', real=True); M, l, rp, gg, W, c = sp.symbols('m L r_p g Omega c', positive=True)
th = sp.Function('theta')(t); phi = W*t
x = rp*sp.cos(phi) + l*sp.cos(phi + th); y = rp*sp.sin(phi) + l*sp.sin(phi + th)
Lag = M/2*(x.diff(t)**2 + y.diff(t)**2) - M*gg*y
EL = sp.diff(Lag.diff(th.diff(t)), t) - Lag.diff(th) + c*th.diff(t)          # Rayleigh brake c thetadot^2/2
eq = sp.simplify(EL/(M*l**2*W**2))
R, G, kap, tau = sp.symbols('R G kappa tau', positive=True)
q = sp.Function('q')
target = q(tau).diff(tau, 2) + kap*q(tau).diff(tau) + R*sp.sin(q(tau)) + G*sp.cos(tau + q(tau))
mine = eq.subs({th: q(W*t)}).doit()
mine = mine.subs(t, tau/W).doit()
mine = mine.subs({rp: R*l, gg: G*W**2*l, c: kap*M*l**2*W})
diff = sp.simplify(sp.expand_trig(mine.rewrite(sp.cos) - target.subs({}).rewrite(sp.cos)))
check(diff == 0, 'Lagrangian -> theta\'\' + kappa theta\' + R sin(theta) + G cos(phi + theta) = 0  (1.5)')
k_, R1 = sp.symbols('k s', positive=True)                                        # s = R - 1 > 0
P = k_*G**2/(2*(R1**2 + k_**2))
kstar = sp.solve(sp.diff(P, k_), k_)
check(kstar == [R1], 'best brake kappa* = R - 1  (2.4)')
A = -G/(R1 + sp.I*R1)                                                            # complex amplitude at the best brake
# theta = Re[A e^{i phi}] = -|A| cos(phi + arg(-A)), so (2.2)'s lag delta = -arg(-A)
check(abs(-float(sp.arg(-A.subs({G: 1, R1: 1}))) - math.pi/4) < 1e-12, 'lag delta = 45 degrees at the best brake')
Pstar = sp.simplify((M*l**2*W**3*P.subs(k_, R1)).subs({G: gg/(W**2*l), R1: rp/l - 1}))
check(sp.simplify(Pstar - M*l*gg**2/(4*W*(rp - l))) == 0, 'P* = m L g^2/(4 Omega (r_p - L))  (2.5)')
Th = G/sp.sqrt(R1**2 + k_**2); trail = -k_*Th**2/(2*(R1 + 1))                    # (3.2) with R = s + 1
Pbar = M*l**2*W**3*k_*Th**2/2
check(sp.simplify(Pbar + M*(R1 + 1)*l*l*W**3*trail) == 0, 'trail identity P = -m r_p L Omega^3 theta_bar  (3.3)')

# ---- 2. SciPy re-integration of the single pendulum --------------------------------------------------------------
mt = json.load(open(ROOT / 'data/L1_mountings.json'))
for row in [r for r in mt if (r['wind'], r['pct']) in ((6, 30), (6, 90), (8, 30), (8, 60), (10, 30), (10, 90))]:
    Om = LAM*row['wind']/RTIP; r_p = row['pct']/100*RTIP; cc = row['c_single']
    Rr, Gg, kk = r_p/L, g/(Om**2*L), cc/(m*L**2*Om)
    f = lambda s, Y: [Y[1], -kk*Y[1] - Rr*math.sin(Y[0]) - Gg*math.cos(s + Y[0]), kk*Y[1]**2]
    n0, n1 = 60, 40
    sol = solve_ivp(f, (0, 2*math.pi*(n0 + n1)), [0, 0, 0], method='Radau', rtol=1e-11, atol=1e-13,
                    t_eval=[2*math.pi*n0, 2*math.pi*(n0 + n1)])
    Pm = (sol.y[2, 1] - sol.y[2, 0])/(2*math.pi*n1)*m*L**2*Om**3
    rel = Pm/row['P_single'] - 1
    check(abs(rel) < 1e-5, f"{row['wind']} m/s {row['pct']} %: SciPy {Pm*1e3:.5f} mW against the study's {row['P_single']*1e3:.5f} mW ({rel:+.1e})")

# ---- 3. The generator ------------------------------------------------------------------------------------------------
kt, ke, Rc, Jm, I0 = 0.0208, 60/(2*math.pi*460), 1.53, 1.47e-6, 0.0402        # maxon RE 25, 24 V, part 339152
check(abs(kt/ke - 1) < 0.01, f'k_t = {kt} N m/A and k_e = {ke:.5f} V s agree (energy balance)')
N_, kT, kE, Rcs, RL, w = sp.symbols('N k_t k_e R_c R_L omega', positive=True)
I = kE*N_*w/(Rcs + RL); torque = N_*kT*I                                         # torque at the pendulum, w = thetadot
check(sp.simplify(torque/w - N_**2*kT*kE/(Rcs + RL)) == 0, 'brake constant c_e = N^2 k_t k_e/(R_c + R_L)  (7.1)')
csc = N_**2*kT*kE/Rcs; ce = N_**2*kT*kE/(Rcs + RL)
check(sp.simplify((I**2*RL/(torque*w) - (1 - ce/csc)).subs(kT, kE)) == 0, 'load share R_L/(R_c + R_L) = 1 - c_e/c_sc  (7.2)')
T0 = kt*I0; Njam = 0.70*m*g*L/T0
Njam4 = 0.60*m*g*L/T0
check(int(Njam) == 410 and 246 < Njam4 < 492, f'jamming ratio eta m g L/T0 = {Njam:.1f} (three stages, 70 %), {Njam4:.1f} (four stages, 60 %): 246 swings, 492 jams')
chk = {(r['wind'], r['frac']): r for r in json.load(open(ROOT / 'data/L4_check_2000.json'))}
for key in ((6, 0.3), (10, 0.9)):
    r = chk[key]; Om = LAM*key[0]/RTIP; r_p = key[1]*RTIP; Nr = r['N']; eta = r['eta']
    Rr, Gg = r_p/L, g/(Om**2*L); j = (Jm + 0.7e-7)*Nr**2/(m*L**2); kap = r['c_e']/(m*L**2*Om); f0 = Nr*T0/(m*L**2*Om**2)
    keep = 1 - r['c_e']/(Nr**2*kt*ke/Rc); ew = 1e-3*r['Theta']; ep = 1e-3*Gg*r['Theta']
    def acc(s, th_, w_):
        D = Rr*math.sin(th_) + Gg*math.cos(s + th_); xr = f0*math.tanh(w_/ew) + kap*w_
        h = lambda a: a + D + (j*a + xr)*eta**(-math.tanh((j*a + xr)*w_/ep))
        lo, hi = -(abs(D) + abs(xr)/eta) - 1e-12, abs(D) + abs(xr)/eta + 1e-12
        for _ in range(80):
            mid = 0.5*(lo + hi)
            if h(mid) > 0: hi = mid
            else: lo = mid
        return 0.5*(lo + hi)
    def f(s, Y):
        a = acc(s, Y[0], Y[1]); return [Y[1], a, kap*keep*Y[1]**2]
    n0, n1 = 100, 20
    sol = solve_ivp(f, (0, 2*math.pi*(n0 + n1)), [0, 0, 0], method='LSODA', rtol=1e-8, atol=1e-11, max_step=2*math.pi/400,
                    t_eval=[2*math.pi*n0, 2*math.pi*(n0 + n1)])
    Pl = (sol.y[2, 1] - sol.y[2, 0])/(2*math.pi*n1)*m*L**2*Om**3
    rel = Pl/r['P_load'] - 1
    check(abs(rel) < 0.01, f'{key[0]} m/s {key[1]*100:.0f} %, ratio {Nr}: load {Pl*1e3:.4f} mW by SciPy against {r["P_load"]*1e3:.4f} mW ({rel:+.1e})')

print('ALL PASS' if not fails else f'{len(fails)} FAIL'); sys.exit(1 if fails else 0)
