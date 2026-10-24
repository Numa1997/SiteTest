"""L0 derivation, single pendulum on a turning blade, rotor angle phi(t) left free.

Run: python3 -I L0_single.py   (prints PASS/FAIL lines; exit code 1 on any FAIL)
Bob of mass m on a massless rod of length L, pivot on the blade at radius r_p from the hub axis.
The rotor plane is vertical; gravity -g in y. theta is the rod angle measured from the blade's outward
radial direction, so the rod's absolute angle is phi + theta. The generator brakes the RELATIVE
rotation theta with torque -c*theta_dot (Rayleigh function F = c*theta_dot^2/2).
"""
import sys
import sympy as sp

t = sp.symbols('t', real=True)
m, L, rp, g, c = sp.symbols('m L r_p g c', positive=True)
phi = sp.Function('phi')(t)
th = sp.Function('theta')(t)
fails = 0
def check(name, expr):
    global fails
    ok = sp.simplify(expr) == 0
    fails += (not ok)
    print(('PASS ' if ok else 'FAIL ') + name)

# positions and energies
x = rp*sp.cos(phi) + L*sp.cos(phi + th)
y = rp*sp.sin(phi) + L*sp.sin(phi + th)
T = m/2*(sp.diff(x, t)**2 + sp.diff(y, t)**2)
V = m*g*y
Lag = T - V
F = c/2*sp.diff(th, t)**2

# Euler-Lagrange for theta with Rayleigh dissipation:  d/dt dL/dthdot - dL/dth + dF/dthdot = 0
thd = sp.diff(th, t)
EL_th = sp.diff(sp.diff(Lag, thd), t) - sp.diff(Lag, th) + sp.diff(F, thd)
phd, phdd, thdd = sp.diff(phi, t), sp.diff(phi, t, 2), sp.diff(th, t, 2)
expected = (m*L**2*thdd + m*L**2*phdd + m*rp*L*phdd*sp.cos(th)
            + m*rp*L*phd**2*sp.sin(th) + m*g*L*sp.cos(phi + th) + c*thd)
check('equation of motion (1): m L^2 (th\'\' + phi\'\') + m r_p L (phi\'\' cos th + phi\'^2 sin th) + m g L cos(phi+th) + c th\' = 0',
      sp.expand(sp.simplify(EL_th - expected)))
print('   kinetic energy T =', sp.simplify(sp.trigsimp(T)))

# torque the rotor must supply to impose phi(t): generalised force on phi (the generator torque is
# internal: it acts on theta, the relative coordinate, so it does not appear here)
tau_rot = sp.diff(sp.diff(Lag, phd), t) - sp.diff(Lag, phi)
# energy book: d(T+V)/dt = tau_rot*phi' - 2F  on solutions of (1)
dE = sp.diff(T + V, t)
thdd_sol = sp.solve(sp.Eq(expected, 0), thdd)[0]
book = (dE - (tau_rot*phd - 2*F)).subs(sp.diff(th, t, 2), thdd_sol)
check('energy book (2): d(T+V)/dt = tau_rot*phi_dot - c*theta_dot^2 (the rotor pays for every joule)', sp.expand(sp.simplify(book)))

# blade-angle form: phi' = W(t) > 0, use phi as the clock.  theta' = W th_p, theta'' = W^2 th_pp + Wdot th_p
W, Wd, a, ap, app = sp.symbols('Omega Omegadot theta theta_p theta_pp', real=True)
ph = sp.symbols('varphi', real=True)
R, G, kap, eps = sp.symbols('R G kappa epsilon', real=True)
eq = expected.subs({thdd: W**2*app + Wd*ap, thd: W*ap, phdd: Wd, phd: W}).subs({th: a, phi: ph})
eq_bl = sp.expand(eq/(m*L**2*W**2))
target = (app + eps*(ap + 1 + R*sp.cos(a)) + R*sp.sin(a) + G*sp.cos(ph + a) + kap*ap)
check('blade-angle form (3): th_pp + eps(th_p + 1 + R cos th) + R sin th + G cos(phi+th) + kappa th_p = 0, '
      'R=r_p/L, G=g/(Omega^2 L), kappa=c/(m L^2 Omega), eps=Omegadot/Omega^2',
      sp.simplify(eq_bl - target.subs({R: rp/L, G: g/(W**2*L), kap: c/(m*L**2*W), eps: Wd/W**2})))

# linear response at uniform rotation, small theta, gravity term to first order:
#   th_pp + kappa th_p + R th = -G cos(phi) + G th sin(phi);  drop the parametric term (relative size G/R = 1/Gamma)
A, B = sp.symbols('A B', real=True)
trial = A*sp.cos(ph) + B*sp.sin(ph)
lin = sp.diff(trial, ph, 2) + kap*sp.diff(trial, ph) + R*trial + G*sp.cos(ph)
sol = sp.solve([sp.expand(lin).coeff(sp.cos(ph)), sp.expand(lin).coeff(sp.sin(ph))], [A, B], dict=True)[0]
amp2 = sp.simplify(sol[A]**2 + sol[B]**2)
check('linear amplitude (4): Theta^2 = G^2/((R-1)^2 + kappa^2)', amp2 - G**2/((R - 1)**2 + kap**2))
# mean power  <c theta_dot^2> = c Omega^2 Theta^2 / 2 ;  in units of m L^2 Omega^3:  P_hat = kappa Theta^2 / 2
P_hat = kap*amp2/2
kstar = sp.solve(sp.diff(P_hat, kap), kap)
check('best damping (5): kappa* = |R-1| (taking R>1)', sp.simplify([k for k in kstar if k.subs({R: 3}) > 0][0] - (R - 1)))
Pstar = sp.simplify(P_hat.subs(kap, R - 1)*m*L**2*W**3)
check('best power (6): P* = m L g^2 / (4 Omega (r_p - L))', sp.simplify(Pstar.subs({G: g/(W**2*L), R: rp/L}) - m*L*g**2/(4*W*(rp - L))))

# the strongest mounting of the notes (setup.py: 6 m/s, pivot at 30 %) against the full nonlinear model (L1_mountings.json)
import json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import setup as S
v0, f0 = S.WINDS[0], S.FRACS[0]
num = {m: S.M, L: S.L, g: S.G0, W: S.omega(v0), rp: f0*S.R_ROT}
Pv = float((m*L*g**2/(4*W*(rp - L))).subs(num))
full = next(x['P_single'] for x in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L1_mountings.json')))
            if x['wind'] == v0 and x['pct'] == round(f0*100))
print(f'   P* at {v0:.0f} m/s, pivot at {f0*100:.0f} %: {Pv*1e3:.2f} mW; full model {full*1e3:.2f} mW')
ok = abs(Pv/full - 1) < 0.01
fails += (not ok); print(('PASS ' if ok else 'FAIL ') + 'closed form within 1 % of the full model at the strongest mounting')
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
