#!/usr/bin/env python3
"""Independent physics checks of the Rotor Pendula study: a second blade (a thin uniform rod, mass m, length l) hinged at the
63 m tip of the NREL 5 MW blade.  Every constant is typed again here; nothing is imported from the study's own scripts.
Run: python3 -I check_physics.py   (about two minutes; exit 1 on any FAIL)

  1. SymPy: the rod on a turning blade, from its Lagrangian integrated along the rod -> equation (1.5) in blade-angle form,
     with R = 3 r_p/(2 l), G = 3 g/(2 l Omega^2), kappa = c/(I Omega); the uneven-rotor term Omega' (I + (m l/2) r_p cos theta);
     the best brake kappa* = R - 1 (2.4), the 45 degree lag, P* (2.5), the generator's torque tau* = (m l/2) g/sqrt 2 and the
     trail identity (3.3).
  2. SciPy: the full equation re-integrated with solve_ivp (Radau, tight tolerances) at the nine stored runs (three winds, three
     brakes), against the powers the study's own engine wrote (data/L1_blade.json).
  3. The generator: the brake constant from the circuit (7.1), the load share (7.2), k_t against k_e, the jamming ratio, and
     the full equation (7.8) re-integrated with solve_ivp at two winds against data/L4_check_2000.json.
"""
import json, math, pathlib, sys
import numpy as np, sympy as sp
from scipy.integrate import solve_ivp

ROOT = pathlib.Path(__file__).resolve().parent
g = 9.80665; m = 1.0; l = 1.0; r_p = 63.0; lam = 7.55          # the second blade, the NREL 5 MW rotor and its tip-speed ratio
I = m*l*l/3; mlc = m*l/2
fails = []
def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what)
    if not ok: fails.append(what)

# ---- 1. SymPy -----------------------------------------------------------------------------------------------------
t, s = sp.symbols('t s', real=True)
M, L, rp, gg, c = sp.symbols('m l r_p g c', positive=True)
th = sp.Function('theta')(t); ph = sp.Function('varphi')(t)
x = rp*sp.cos(ph) + s*sp.cos(ph + th); y = rp*sp.sin(ph) + s*sp.sin(ph + th)        # a point at distance s from the hinge
lam_ = M/L                                                                           # mass per length
T = sp.integrate(lam_/2*(x.diff(t)**2 + y.diff(t)**2), (s, 0, L))
V = sp.integrate(lam_*gg*y, (s, 0, L))
Lag = T - V
EL = sp.diff(Lag.diff(th.diff(t)), t) - Lag.diff(th) + c*th.diff(t)                 # Rayleigh brake c thetadot^2/2
Ir, mlr = M*L**2/3, M*L/2
mine = sp.expand(sp.simplify(EL))
want = (Ir*(th.diff(t, 2) + ph.diff(t, 2)) + mlr*rp*(ph.diff(t, 2)*sp.cos(th) + ph.diff(t)**2*sp.sin(th))
        + mlr*gg*sp.cos(ph + th) + c*th.diff(t))
check(sp.simplify(mine - sp.expand(want)) == 0,
      'Lagrangian of the rod -> I(theta" + phi") + (m l/2) r_p (phi" cos theta + phi\'^2 sin theta) + (m l/2) g cos(phi + theta) + c theta\' = 0')
W = sp.symbols('Omega', positive=True)
const = sp.simplify(want.subs(ph, W*t).doit()/(Ir*W**2))
R, G, kap = sp.symbols('R G kappa', positive=True)
q = sp.Function('q')(t)
target = th.diff(t, 2)/W**2 + kap*th.diff(t)/W + R*sp.sin(th) + G*sp.cos(W*t + th)
check(sp.simplify(sp.expand(const - target.subs({R: 3*rp/(2*L), G: 3*gg/(2*L*W**2), kap: c/(Ir*W)}))) == 0,
      'steady rotor -> theta\'\' + kappa theta\' + R sin theta + G cos(phi + theta) = 0, R = 3 r_p/(2 l), G = 3 g/(2 l Omega^2)  (1.5)')
Wd = sp.symbols('Omegadot')
uneven = sp.expand(want.subs(ph.diff(t, 2), Wd) - want.subs(ph.diff(t, 2), 0))
check(sp.simplify(uneven - Wd*(Ir + mlr*rp*sp.cos(th))) == 0, "uneven rotor: the term Omega' (I + (m l/2) r_p cos theta)")
k_, R1 = sp.symbols('k s1', positive=True)                                        # s1 = R - 1 > 0
P = k_*G**2/(2*(R1**2 + k_**2))
check(sp.solve(sp.diff(P, k_), k_) == [R1], 'best brake kappa* = R - 1  (2.4)')
A = -G/(R1 + sp.I*R1)
check(abs(-float(sp.arg(-A.subs({G: 1, R1: 1}))) - math.pi/4) < 1e-12, 'lag delta = 45 degrees at the best brake')
Pst = sp.simplify((Ir*W**3*P.subs(k_, R1)).subs({G: 3*gg/(2*L*W**2), R1: 3*rp/(2*L) - 1}))
check(sp.simplify(Pst - M*gg**2*L/(8*W*(rp - sp.Rational(2, 3)*L))) == 0, 'P* = m g^2 l/(8 Omega (r_p - 2 l/3))  (2.5)')
Th = G/sp.sqrt(R1**2 + k_**2)
tau = (Ir*W**2*R1*Th.subs(k_, R1)).subs({G: 3*gg/(2*L*W**2)})                      # c* Omega Theta* = I Omega^2 kappa* Theta*
check(sp.simplify(tau - mlr*gg/sp.sqrt(2)) == 0, 'generator torque at the best brake tau* = (m l/2) g/sqrt 2')
trail = -k_*Th**2/(2*(R1 + 1))
Pbar = Ir*W**3*k_*Th**2/2
check(sp.simplify((Pbar + mlr*rp*W**3*trail).subs(R1 + 1, mlr*rp/Ir).subs(R1, mlr*rp/Ir - 1)) == 0,
      'trail identity P = -(m l/2) r_p Omega^3 theta_bar  (3.3)')

# ---- 2. SciPy re-integration of the nine stored runs ------------------------------------------------------------------
for row in json.load(open(ROOT / 'data/L1_blade.json')):
    Om = lam*row['wind']/r_p; cc = row['c']
    Rr, Gg, kk = mlc*r_p/I, mlc*g/(I*Om**2), cc/(I*Om)
    f = lambda u, Y: [Y[1], -kk*Y[1] - Rr*math.sin(Y[0]) - Gg*math.cos(u + Y[0]), kk*Y[1]**2]
    n0, n1 = row['settle'], row['measure']
    sol = solve_ivp(f, (0, 2*math.pi*(n0 + n1)), [0, 0, 0], method='Radau', rtol=1e-12, atol=1e-14,
                    t_eval=[2*math.pi*n0, 2*math.pi*(n0 + n1)])
    Pm = (sol.y[2, 1] - sol.y[2, 0])/(2*math.pi*n1)*I*Om**3
    rel = Pm/row['P'] - 1
    check(abs(rel) < 1e-6, f"{row['wind']:.0f} m/s, brake x {row['mult']}: SciPy {Pm*1e3:.6f} mW against the study's {row['P']*1e3:.6f} mW ({rel:+.1e})")

# ---- 3. The generator ------------------------------------------------------------------------------------------------
kt, ke, Rc, Jm, I0 = 0.0208, 60/(2*math.pi*460), 1.53, 1.47e-6, 0.0402        # maxon RE 25, 24 V, part 339152
check(abs(kt/ke - 1) < 0.01, f'k_t = {kt} N m/A and k_e = {ke:.5f} V s agree (energy balance)')
N_, kT, kE, Rcs, RL, w = sp.symbols('N k_t k_e R_c R_L omega', positive=True)
Icur = kE*N_*w/(Rcs + RL); torque = N_*kT*Icur
check(sp.simplify(torque/w - N_**2*kT*kE/(Rcs + RL)) == 0, 'brake constant c_e = N^2 k_t k_e/(R_c + R_L)  (7.1)')
csc = N_**2*kT*kE/Rcs; ce_ = N_**2*kT*kE/(Rcs + RL)
check(sp.simplify((Icur**2*RL/(torque*w) - (1 - ce_/csc)).subs(kT, kE)) == 0, 'load share R_L/(R_c + R_L) = 1 - c_e/c_sc  (7.2)')
T0 = kt*I0; Njam = 0.60*mlc*g/T0
check(492 < Njam, f'jamming ratio eta (m l/2) g/T0 = {Njam:.0f} (four stages, 60 %): the largest catalogue ratio, 492, swings')
chk = [r for r in json.load(open(ROOT / 'data/L4_check_2000.json')) if r['kind'] == 'best' and r['mult'] == 1.0]
for r in [r for r in chk if r['wind'] in (6.0, 10.0)]:
    Om = lam*r['wind']/r_p; Nr = r['N']; eta = r['eta']
    Rr, Gg = mlc*r_p/I, mlc*g/(I*Om**2); j = (Jm + 0.7e-7)*Nr**2/I; kap = r['c_e']/(I*Om); f0 = Nr*T0/(I*Om**2)
    keep = 1 - r['c_e']/(Nr**2*kt*ke/Rc); sc = min(max(r['Theta_formula'], 1e-2), 0.5)
    ew = 1e-3*sc; ep = 1e-3*(f0 + (kap + j)*sc)*sc                                  # the study's smoothing bands
    def acc(u, th_, w_):
        D = Rr*math.sin(th_) + Gg*math.cos(u + th_); xr = f0*math.tanh(w_/ew) + kap*w_
        h = lambda a: a + D + (j*a + xr)*eta**(-math.tanh((j*a + xr)*w_/ep))
        lo, hi = -(abs(D) + abs(xr)/eta) - 1e-12, abs(D) + abs(xr)/eta + 1e-12
        for _ in range(80):
            mid = 0.5*(lo + hi)
            if h(mid) > 0: hi = mid
            else: lo = mid
        return 0.5*(lo + hi)
    def f(u, Y):
        a = acc(u, Y[0], Y[1]); return [Y[1], a, kap*keep*Y[1]**2]
    n0, n1 = 100, 20
    sol = solve_ivp(f, (0, 2*math.pi*(n0 + n1)), [0, 0, 0], method='LSODA', rtol=1e-8, atol=1e-11, max_step=2*math.pi/400,
                    t_eval=[2*math.pi*n0, 2*math.pi*(n0 + n1)])
    Pl = (sol.y[2, 1] - sol.y[2, 0])/(2*math.pi*n1)*I*Om**3
    rel = Pl/r['P_load'] - 1
    check(abs(rel) < 0.01, f'{r["wind"]:.0f} m/s, ratio {Nr}: load {Pl*1e3:.4f} mW by SciPy against {r["P_load"]*1e3:.4f} mW ({rel:+.1e})')

print('ALL PASS' if not fails else f'{len(fails)} FAIL'); sys.exit(1 if fails else 0)
