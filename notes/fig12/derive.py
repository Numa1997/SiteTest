"""Fig. 12, the Furuta pendulum: every equation of the note, derived twice in SymPy.

Run: python3 notes/fig12/derive.py   (prints PASS/FAIL lines; exit 1 on any FAIL)

Coordinates: phi, the arm's angle about the vertical axis; alpha, the pendulum's angle from straight UP
(alpha = 0 upright, alpha = pi hanging), measured in the plane at right angles to the arm.
"""
import sys
import sympy as sp
from sympy.physics.mechanics import (ReferenceFrame, Point, RigidBody, inertia, LagrangesMethod,
                                     dynamicsymbols, Particle)

ok = True
def check(name, expr):
    global ok
    e = sp.simplify(expr)
    good = e.is_zero_matrix if isinstance(e, sp.MatrixBase) else e == 0
    ok &= good
    print(('PASS ' if good else 'FAIL ') + name + ('' if good else '   residual: ' + str(e)))

t = sp.symbols('t')
phi, al = dynamicsymbols('phi alpha')
phid, ald = sp.diff(phi, t), sp.diff(al, t)
Jr, mp, r, L, g, k, R, Lam, br, bp = sp.symbols('J_r m_p r L g k R Lambda b_r b_p', positive=True)
s = sp.symbols('s', positive=True)                      # distance along the pendulum rod from its hinge
V, I = sp.symbols('V I')

# ---------- (2) kinetic energy, route 1: vector kinematics of a rod element, integrated over the rod ----------
er = sp.Matrix([sp.cos(phi), sp.sin(phi), 0]); ep = sp.Matrix([-sp.sin(phi), sp.cos(phi), 0]); ez = sp.Matrix([0, 0, 1])
pos = r * er + s * (sp.sin(al) * ep + sp.cos(al) * ez)   # a point of the rod at distance s from the hinge
vel = sp.diff(pos, t)
v2 = sp.simplify(vel.dot(vel))
T_rod = sp.integrate((mp / L) * v2 / 2, (s, 0, L))
T1 = sp.Rational(1, 2) * Jr * phid**2 + T_rod
V1 = sp.integrate((mp / L) * g * (s * sp.cos(al)), (s, 0, L))  # height of each element above the hinge

J0, Jp, h, G = Jr + mp * r**2, mp * L**2 / 3, mp * r * L / 2, mp * g * L / 2
T_claim = sp.Rational(1, 2) * (J0 + Jp * sp.sin(al)**2) * phid**2 + h * sp.cos(al) * phid * ald + sp.Rational(1, 2) * Jp * ald**2
check('(2) T from integrating the rod element by element', T1 - T_claim)
check('(3) V = G cos(alpha), G = m_p g L/2', V1 - G * sp.cos(al))

# ---------- (2) route 2: sympy.physics.mechanics, a rigid arm and a thin rigid rod ----------
N = ReferenceFrame('N'); A = N.orientnew('A', 'Axis', [phi, N.z])            # A.x along the arm
B = A.orientnew('B', 'Axis', [-al, A.x])                                     # rotate about the arm; B.z along the rod
O = Point('O'); O.set_vel(N, 0)
P = O.locatenew('P', r * A.x); P.v2pt_theory(O, N, A)
Cp = P.locatenew('C', (L / 2) * B.z); Cp.v2pt_theory(P, N, B)
# check the rod direction: B.z expressed in A should be sin(al) A.y + cos(al) A.z
check('rod direction in the arm frame (y)', B.z.dot(A.y) - sp.sin(al))
check('rod direction in the arm frame (z)', B.z.dot(A.z) - sp.cos(al))
arm = RigidBody('arm', O, A, 0, (inertia(A, 0, 0, Jr), O))                   # all of the arm's inertia about the axis
Irod = mp * L**2 / 12
rod = RigidBody('rod', Cp, B, mp, (inertia(B, Irod, Irod, 0), Cp))           # thin rod: no inertia about its own axis
rod.potential_energy = mp * g * (L / 2) * sp.cos(al)
Lag = arm.kinetic_energy(N) + rod.kinetic_energy(N) - rod.potential_energy
check('(2)-(3) Lagrangian by sympy.physics.mechanics equals T - V of route 1', sp.expand(sp.trigsimp(Lag - (T_claim - G * sp.cos(al)))))

# ---------- (4) the DC motor, route 1: Kirchhoff's voltage law and the Lorentz torque ----------
# voltage source V across R, Lambda and the back-emf k*phid:  V = R I + Lambda dI/dt + k phid ; torque on the rotor k I
# route 2: electromechanical Lagrangian, q_e the charge through the winding, Rayleigh function for R and the bearings
qe = dynamicsymbols('q_e'); qed = sp.diff(qe, t)
Lem = T_claim - G * sp.cos(al) + sp.Rational(1, 2) * Lam * qed**2 + k * phi * qed
D = sp.Rational(1, 2) * R * qed**2 + sp.Rational(1, 2) * br * phid**2 + sp.Rational(1, 2) * bp * ald**2
def EL(q, Q=0):
    qd = sp.diff(q, t)
    return sp.diff(sp.diff(Lem, qd), t) - sp.diff(Lem, q) + sp.diff(D, qd) - Q
e_q = EL(qe, V)            # generalised force on q_e is the source voltage
check('(4) electrical equation from the Lagrangian = Kirchhoff  V = R I + Lambda I\' + k phi\'',
      e_q - (Lam * sp.diff(qed, t) + k * phid + R * qed - V))
e_phi = EL(phi)            # torque k*qed appears from d/dt(dL/dphid) - dL/dphi with dL/dphi = k qed
e_al = EL(al)

# ---------- (5) equations of motion in matrix form ----------
phidd, aldd = sp.diff(phi, t, 2), sp.diff(al, t, 2)
tau = sp.symbols('tau')
M = sp.Matrix([[J0 + Jp * sp.sin(al)**2, h * sp.cos(al)], [h * sp.cos(al), Jp]])
Cvec = sp.Matrix([2 * Jp * sp.sin(al) * sp.cos(al) * phid * ald - h * sp.sin(al) * ald**2,
                  -Jp * sp.sin(al) * sp.cos(al) * phid**2])
grav = sp.Matrix([0, -G * sp.sin(al)])
fric = sp.Matrix([br * phid, bp * ald])
lhs = M * sp.Matrix([phidd, aldd]) + Cvec + grav + fric
check('(5) arm equation: Lagrangian with motor = M qdd + C + dV + friction - (k I, 0)', sp.expand(e_phi - (lhs[0] - k * qed)))
check('(5) pendulum equation', sp.expand(e_al - lhs[1]))
# route 2 for (5): LagrangesMethod on the mechanical Lagrangian with generalised forces
LM = LagrangesMethod(Lag, [phi, al], forcelist=[(A, (tau - br * phid) * N.z), (B, -(-bp * ald) * A.x)], frame=N)
LM.form_lagranges_equations()
MM = LM.mass_matrix; FF = LM.forcing
check('(5) mass matrix by LagrangesMethod', sp.simplify(MM - M))
check('(5) forcing by LagrangesMethod', sp.simplify(FF - (sp.Matrix([tau, 0]) - Cvec - grav - fric)))

# inductance dropped: electrical time Lambda/R; with Lambda -> 0, I = (V - k phid)/R, tau = k (V - k phid)/R
tau_motor = k * (V - k * phid) / R

# ---------- (6) upright and hanging rests; (7) linearisation ----------
x = sp.symbols('x1:5')     # (phi, alpha, phid, alphad)
def f(alpha0):
    sub = {phi: x[0], al: alpha0 + x[1], phid: x[2], ald: x[3]}
    Ms = M.subs(sub); rhs = (sp.Matrix([tau_motor, 0]) - Cvec - grav - fric).subs(sub)
    acc = Ms.LUsolve(rhs)
    return sp.Matrix([x[2], x[3], acc[0], acc[1]])
def lin(alpha0):
    F = f(alpha0); z = {xi: 0 for xi in x}; z.update({V: 0})
    A_ = F.jacobian(x).subs(z).applyfunc(sp.simplify); B_ = F.diff(V).subs(z).applyfunc(sp.simplify)
    return A_, B_
Au, Bu = lin(0)
Delta = J0 * Jp - h**2
Au_claim = sp.Matrix([[0, 0, 1, 0], [0, 0, 0, 1],
                      [0, -h * G / Delta, -Jp * (br + k**2 / R) / Delta, h * bp / Delta],
                      [0, J0 * G / Delta, h * (br + k**2 / R) / Delta, -J0 * bp / Delta]])
Bu_claim = sp.Matrix([0, 0, Jp * k / (R * Delta), -h * k / (R * Delta)])
check('(7) A at the upright rest', Au - Au_claim)
check('(7) B at the upright rest', Bu - Bu_claim)
# controllability (8): det of [B, AB, A^2 B, A^3 B]
Af, Bf = Au_claim.subs({br: 0, bp: 0}), Bu_claim
Cm = sp.Matrix.hstack(Bf, Af * Bf, Af**2 * Bf, Af**3 * Bf)
detC0 = sp.factor(Cm.det(method='berkowitz'))
check('(8) without friction det C = -k^4 G^2 h^2 / (R^4 Delta^4)  (zero only when h = 0, i.e. r = 0)', detC0 - (-k**4 * G**2 * h**2 / (R**4 * Delta**4)))
# frictionless free swing: the pendulum's growth rate at the top and its frequency at the bottom
lam = sp.symbols('lambda')
Au0 = Au_claim.subs({br: 0, bp: 0, k: 0})
cp = sp.factor((lam * sp.eye(4) - Au0).det())
check('(9) open loop at the top: eigenvalues 0, 0, +-sqrt(J0 G/Delta)', sp.expand(cp - lam**2 * (lam**2 - J0 * G / Delta)))
Ad, Bd = lin(sp.pi)
Ad0 = Ad.subs({br: 0, bp: 0, k: 0})
cpd = sp.factor((lam * sp.eye(4) - Ad0).det())
check('(9) at the bottom: eigenvalues 0, 0, +-i sqrt(J0 G/Delta)', sp.expand(cpd - lam**2 * (lam**2 + J0 * G / Delta)))

# ---------- (10) energy of the pendulum alone and its rate: the swing-up law ----------
Ep = sp.Rational(1, 2) * Jp * ald**2 + G * sp.cos(al)          # pendulum energy, zero speed at the top gives E* = G
# from the pendulum row of (5): Jp aldd = -h cos(al) phidd + Jp sin cos phid^2 + G sin(al) - bp ald
aldd_sol = (-h * sp.cos(al) * phidd + Jp * sp.sin(al) * sp.cos(al) * phid**2 + G * sp.sin(al) - bp * ald) / Jp
dEp = sp.diff(Ep, t).subs(sp.diff(al, t, 2), aldd_sol)
check('(10) dEp/dt = -h cos(al) ald phidd + Jp sin cos phid^2 ald - bp ald^2',
      sp.expand(dEp - (-h * sp.cos(al) * ald * phidd + Jp * sp.sin(al) * sp.cos(al) * phid**2 * ald - bp * ald**2)))
# with phidd = u and u = kE (Ep - G) ald cos(al): dEp/dt = -h kE (Ep - G) (ald cos al)^2 + (centrifugal, friction)
kE = sp.symbols('k_E', positive=True)
u = kE * (Ep - G) * ald * sp.cos(al)
Vly = sp.Rational(1, 2) * (Ep - G)**2
dV = sp.expand(((Ep - G) * (-h * sp.cos(al) * ald * u)))
check('(11) Lyapunov function (Ep-G)^2/2 falls: d/dt = -h kE (Ep-G)^2 (ald cos al)^2 (driving part)',
      dV + h * kE * (Ep - G)**2 * (ald * sp.cos(al))**2)

# ---------- (12) collocated partial feedback linearisation: the torque that gives the arm acceleration u ----------
uu = sp.symbols('u')
aldd_u = aldd_sol.subs(phidd, uu)
tau_pfl = sp.expand(((J0 + Jp * sp.sin(al)**2) * uu + h * sp.cos(al) * aldd_u + Cvec[0] + br * phid))
check('(12) with tau_pfl the arm row of (5) gives phidd = u exactly',
      sp.simplify((M * sp.Matrix([uu, aldd_u]) + Cvec + grav + fric)[0] - tau_pfl))
Mbar = sp.simplify(J0 + Jp * sp.sin(al)**2 - h**2 * sp.cos(al)**2 / Jp)
check('(12) effective inertia of the arm with the pendulum riding along: J0 + Jp sin^2 - h^2 cos^2 / Jp',
      sp.simplify(sp.diff(tau_pfl, uu) - Mbar))

# ---------- (13) energy book: d/dt (T + V) = tau phid - br phid^2 - bp ald^2 ; electrical: V I = R I^2 + k I phid ----------
E = T_claim + G * sp.cos(al)
sol = sp.Matrix([phidd, aldd]).subs({})  # placeholder to keep names
accs = M.LUsolve(sp.Matrix([tau, 0]) - Cvec - grav - fric)
dE = sp.diff(E, t).subs({phidd: accs[0], aldd: accs[1]})
check('(13) dE/dt = tau phid - br phid^2 - bp ald^2', sp.simplify(dE - (tau * phid - br * phid**2 - bp * ald**2)))
Ielec = (V - k * phid) / R
check('(13) electrical power V I = R I^2 + k I phid  (Joule heat + mechanical work)', sp.simplify(V * Ielec - (R * Ielec**2 + k * Ielec * phid)))

print('ALL PASS' if ok else 'SOME FAILED')
sys.exit(0 if ok else 1)
