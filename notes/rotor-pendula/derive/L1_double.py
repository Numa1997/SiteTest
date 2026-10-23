"""L1 derivation: double pendulum on a turning blade, rotor angle phi(t) left free, generators at pivot and hinge.

Run: python3 -I L1_double.py   (PASS/FAIL lines; exit 1 on any FAIL)

Route 1 (Lagrange, SymPy): inertial positions with the rotor angle phi(t); Rayleigh F = c0 q1dot^2/2 + c1 (q2dot - q1dot)^2/2.
Route 2 (Newton in the blade frame, numeric): fictitious forces (centrifugal, Coriolis, Euler) plus gravity seen from the blade,
projected on the virtual displacements (d'Alembert); independent of route 1. Both give the accelerations at random states.
Checks: route 1 = the blade-angle equations as written in the notes (eps = 0); route 1 = route 2 at random states with eps != 0; the energy book
d(T+V)/dt = tau_rot phidot - 2F; m2 -> 0 reduces to L0; the blade-angle form with eps = Omegadot/Omega^2.
q1, q2: rod angles measured from the blade's outward radial direction (relative angles to the blade, absolute angle phi + q_i).
"""
import sys
import numpy as np
import sympy as sp

fails = 0
def check(name, ok):
    global fails
    fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name)

t = sp.symbols('t', real=True)
m1, m2, l1, l2, rp, g, c0, c1 = sp.symbols('m1 m2 l1 l2 r_p g c0 c1', positive=True)
phi = sp.Function('phi')(t); q1 = sp.Function('q1')(t); q2 = sp.Function('q2')(t)
u = lambda a: sp.Matrix([sp.cos(a), sp.sin(a)])
P = rp*u(phi); x1 = P + l1*u(phi + q1); x2 = x1 + l2*u(phi + q2)
v1 = x1.diff(t); v2 = x2.diff(t)
T = sp.Rational(1, 2)*(m1*v1.dot(v1) + m2*v2.dot(v2))
V = g*(m1*x1[1] + m2*x2[1])
F = sp.Rational(1, 2)*c0*q1.diff(t)**2 + sp.Rational(1, 2)*c1*(q2.diff(t) - q1.diff(t))**2
Lag = T - V
qs = [q1, q2]
EL = [sp.diff(Lag.diff(q.diff(t)), t) - Lag.diff(q) + F.diff(q.diff(t)) for q in qs]

# --- the energy book: d(T+V)/dt = tau_rot*phidot - 2F, tau_rot = generalised force the rotor must supply on phi ---------
tau = sp.diff(Lag.diff(phi.diff(t)), t) - Lag.diff(phi)
qdd = sp.symbols('A1 A2')
sub_dd = {q1.diff(t, 2): qdd[0], q2.diff(t, 2): qdd[1]}
ELs = [sp.expand(e.subs(sub_dd)) for e in EL]
# EL_i = sum_j Mij A_j + h_i is linear in the accelerations: extract M and h symbolically (cheap), solve numerically
Mij = [[ELs[i].coeff(qdd[j]) for j in range(2)] for i in range(2)]
h = [sp.expand(ELs[i] - Mij[i][0]*qdd[0] - Mij[i][1]*qdd[1]) for i in range(2)]
book = (sp.diff(T + V, t) - tau*phi.diff(t) + 2*F).subs(sub_dd)
S = sp.symbols('ph php phpp a1 a2 w1 w2')
def num(expr, extra=()):
    e = expr
    for d_, s_ in ((phi.diff(t, 2), S[2]), (phi.diff(t), S[1]), (q1.diff(t), S[5]), (q2.diff(t), S[6])):
        e = e.subs(d_, s_)
    e = e.subs({phi: S[0], q1: S[3], q2: S[4]})
    return sp.lambdify((m1, m2, l1, l2, rp, g, c0, c1) + S + tuple(extra), e, 'numpy')
M_f = [[num(Mij[i][j]) for j in range(2)] for i in range(2)]
h_f = [num(h[i]) for i in range(2)]
book_f = num(book, qdd)
def acc_lagrange(pars, st):
    Mm = np.array([[M_f[i][j](*pars, *st) for j in range(2)] for i in range(2)], float)
    hh = np.array([h_f[i](*pars, *st) for i in range(2)], float)
    return np.linalg.solve(Mm, -hh)
rng = np.random.default_rng(3)
worst = 0
for _ in range(200):
    pars = rng.uniform(0.05, 2, 8); st = rng.uniform(-3, 3, 7)
    A = acc_lagrange(pars, st)
    worst = max(worst, abs(book_f(*pars, *st, *A)))
check(f'energy book d(T+V)/dt = tau_rot*phidot - c0 q1dot^2 - c1 (q2dot-q1dot)^2 on solutions (max residual {worst:.1e})', worst < 1e-9)

# --- route 2: Newton in the blade frame -------------------------------------------------------------------------------
def acc_newton(p, st):
    m1_, m2_, l1_, l2_, rp_, g_, c0_, c1_ = p
    ph, Om, Omd, a1, a2, w1, w2 = st
    e1 = np.array([np.cos(a1), np.sin(a1)]); n1 = np.array([-np.sin(a1), np.cos(a1)])
    e2 = np.array([np.cos(a2), np.sin(a2)]); n2 = np.array([-np.sin(a2), np.cos(a2)])
    r1 = np.array([rp_, 0.0]) + l1_*e1; r2 = r1 + l2_*e2                  # positions in the blade frame
    vr1 = l1_*w1*n1; vr2 = vr1 + l2_*w2*n2                                   # velocities relative to the blade
    J1 = np.array([l1_*n1, [0, 0]]).T; J2 = np.array([l1_*n1, l2_*n2]).T   # d r_i / d (q1, q2)
    Jd1q = -l1_*w1**2*e1; Jd2q = Jd1q - l2_*w2**2*e2                         # Jdot qdot (centripetal of relative motion)
    zx = lambda v: np.array([-v[1], v[0]])                                   # z cross v
    gb = g_*np.array([-np.sin(ph), -np.cos(ph)])                             # gravity (0,-g) seen in the blade frame
    def fict(m, r, v):                                                        # centrifugal + Coriolis + Euler + gravity
        return m*(Om**2*r - 2*Om*zx(v) - Omd*zx(r) + gb)
    f1 = fict(m1_, r1, vr1); f2 = fict(m2_, r2, vr2)
    M = m1_*J1.T@J1 + m2_*J2.T@J2
    rhs = J1.T@(f1 - m1_*Jd1q) + J2.T@(f2 - m2_*Jd2q)
    rhs = rhs - np.array([c0_*w1 - c1_*(w2 - w1), c1_*(w2 - w1)])
    return np.linalg.solve(M, rhs)
worst = 0
for _ in range(500):
    pars = rng.uniform(0.05, 2, 8); st = rng.uniform(-3, 3, 7)
    a_l = acc_lagrange(pars, st)
    a_n = acc_newton(pars, st)
    worst = max(worst, np.max(np.abs(a_l - a_n))/(1 + np.max(np.abs(a_n))))
check(f'route 1 (Lagrange) = route 2 (Newton in the blade frame, Coriolis and Euler forces) at 500 random states, '
      f'Omegadot != 0 (max rel diff {worst:.1e})', worst < 1e-10)

# --- blade-angle form, compare with the equations as written in the notes (eps = 0) and give the eps terms ----------------------------------
M_, L_ = sp.symbols('M L', positive=True)
s, Om, Omd = sp.symbols('s Omega Omegadot', real=True)
Q1, Q2, U1, U2, Q1pp, Q2pp = sp.symbols('Q1 Q2 U1 U2 Q1pp Q2pp', real=True)
R, G, k0, k1, eps = sp.symbols('R G kappa0 kappa1 epsilon', real=True)
def blade_form(expr):
    e = expr.subs(sub_dd)
    # q_i'' (blade angle) : qdd = Om^2 Q'' + Omd Q' ; qdot = Om Q'
    e = e.subs({qdd[0]: Om**2*Q1pp + Omd*U1, qdd[1]: Om**2*Q2pp + Omd*U2})
    e = e.subs({q1.diff(t): Om*U1, q2.diff(t): Om*U2, phi.diff(t, 2): Omd, phi.diff(t): Om})
    e = e.subs({q1: Q1, q2: Q2, phi: s})
    return sp.expand(e/(M_*L_**2*Om**2))
a, b, beta = l1/L_, l2/L_, m2/M_
Ad, Bd, Dd = a**2, beta*b**2, beta*a*b
d = Q1 - Q2
eq1 = Ad*Q1pp + Dd*sp.cos(d)*Q2pp + Dd*sp.sin(d)*(1 + U2)**2 + a*(R*sp.sin(Q1) + G*sp.cos(s + Q1)) + k0*U1 - k1*(U2 - U1)
eq2 = Bd*Q2pp + Dd*sp.cos(d)*Q1pp - Dd*sp.sin(d)*(1 + U1)**2 + beta*b*(R*sp.sin(Q2) + G*sp.cos(s + Q2)) + k1*(U2 - U1)
rep = {R: rp/L_, G: g/(Om**2*L_), k0: c0/(M_*L_**2*Om), k1: c1/(M_*L_**2*Om)}
mine = [blade_form(EL[0]), blade_form(EL[1])]
for i, (mi, so) in enumerate(zip(mine, (eq1, eq2))):
    diff = sp.simplify((mi - so.subs(rep)).subs(Omd, 0).subs(m1, M_ - m2))
    check(f"blade-angle equation {i+1} at uniform rotation = the notes' dimensionless equation {i+1}", diff == 0)
# the Euler (eps) terms: coefficient of Omegadot, written with eps = Omegadot/Omega^2
for i, mi in enumerate(mine):
    epsterm = sp.simplify(sp.expand(mi.subs(m1, M_ - m2)).coeff(Omd)*Om**2)
    print(f'   eps terms of equation {i+1}: eps * ({epsterm})')
# single-pendulum limit m2 -> 0: equation 1 becomes L0's blade-angle form with L = l1
e1s = sp.simplify(blade_form(EL[0]).subs({m2: 0, c1: 0}).subs(m1, M_)*M_*L_**2/(M_*l1**2))   # no second bob, no hinge generator
L0 = Q1pp + (Omd/Om**2)*(U1 + 1 + (rp/l1)*sp.cos(Q1)) + (rp/l1)*sp.sin(Q1) + g/(Om**2*l1)*sp.cos(s + Q1) + c0/(M_*l1**2*Om)*U1
print("   diff:", sp.simplify(e1s - L0)); check("m2 -> 0, c1 = 0: equation 1 reduces to the L0 single pendulum (with its Euler terms)", sp.simplify(e1s - L0) == 0)
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
