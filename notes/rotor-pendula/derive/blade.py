"""The second blade, derived twice: Lagrange from the positions, and Newton in the turning frame.

The machine: the mother blade turns at a constant Omega; at its tip, radius r_p, a second blade (a thin uniform rod of mass m and
length l) is hinged on an axis parallel to the shaft and turns in the rotor plane by theta (0 = straight out). A brake at the hinge
puts the torque -c theta' on the second blade and +c theta' on the mother blade. Rotor angle phi = Omega t from the horizontal,
y up. A point at distance s along the second blade is at  r_p e(phi) + s e(phi + theta),  e(a) = (cos a, sin a).

Run: python3 -I blade.py   (prints PASS or FAIL per check; exit status 1 on any FAIL)
"""
import sympy as sp

t, s = sp.symbols('t s', real=True)
m, l, rp, g, Om, c = sp.symbols('m l r_p g Omega c', positive=True)
q, w, a, ph = sp.symbols('theta thetadot thetaddot phi', real=True)      # theta, theta', theta'' (time) and phi as plain symbols
I, Ic, mlc = m*l**2/3, m*l**2/12, m*l/2                                    # about the hinge, about the centre of mass, first moment
fails = []


def check(name, expr_zero):
    ok = sp.simplify(expr_zero) == 0
    print(('PASS ' if ok else 'FAIL ') + name)
    if not ok:
        fails.append(name)


e = lambda ang: sp.Matrix([sp.cos(ang), sp.sin(ang)])
cross = lambda u, v: u[0]*v[1] - u[1]*v[0]                                # z-component of a planar cross product

# ---------------------------------------------------------------------------------------------------------------- 1. Lagrange
PH, TH = sp.Function('phi')(t), sp.Function('theta')(t)
pos = rp*e(PH) + s*e(PH + TH)
vel = pos.diff(t)
T_L = sp.integrate((m/l)*vel.dot(vel)/2, (s, 0, l))                         # kinetic energy, ground frame
V_L = sp.integrate((m/l)*g*pos[1], (s, 0, l))                               # potential energy
Lag = T_L - V_L
on = {PH.diff(t, 2): 0, PH.diff(t): Om}                                     # the rotor turns uniformly
plain = lambda x: x.subs(on).subs({TH.diff(t, 2): a, TH.diff(t): w}).subs({TH: q, PH: ph})
eom_L = plain(sp.diff(Lag.diff(TH.diff(t)), t) - Lag.diff(TH)) + c*w        # = 0
tau_L = plain(sp.diff(Lag.diff(PH.diff(t)), t) - Lag.diff(PH))              # torque on phi the rotor must supply (brake internal)
T_L, V_L = plain(T_L), plain(V_L)

# the forms used on the page
eom_page = I*a + mlc*(Om**2*rp*sp.sin(q) + g*sp.cos(ph + q)) + c*w
T_page = I*(Om + w)**2/2 + m*rp**2*Om**2/2 + mlc*rp*Om*(Om + w)*sp.cos(q)
V_page = m*g*(rp*sp.sin(ph) + (l/2)*sp.sin(ph + q))
tau_page = mlc*rp*(a*sp.cos(q) - (Om + w)**2*sp.sin(q)) + m*g*rp*sp.cos(ph) - c*w
a_shell = sp.solve(eom_page, a)[0]                                          # theta'' from the equation of motion

check('Lagrange: equation of motion = I q\'\' + (ml/2)[Om^2 r_p sin q + g cos(phi+q)] + c q\'', eom_L - eom_page)
check('Lagrange: kinetic energy = page (rotor_sim.html, bladeEnergy)', T_L - T_page)
check('Lagrange: potential energy = page', V_L - V_page)
check('Lagrange: rotor torque, on shell = page\'s (ml/2) r_p [q\'\' cos q - (Om+q\')^2 sin q] + m g r_p cos phi - c q\'',
      (tau_L - tau_page).subs(a, a_shell))

# ------------------------------------------------------------------------------------------------- 2. Newton, turning frame
# In the frame turning with the mother blade the hinge is fixed at (r_p, 0). On the element dm = (m/l) ds at x = r_p x^ + s e(q):
# centrifugal dm Om^2 x, Coriolis -2 dm Om z^ x v (v = s q' e_perp, so the force lies along the rod: no torque about the hinge),
# no Euler force (Om constant), gravity dm g (cos, sin)(-pi/2 - phi) (lab "down" seen from a frame turned by phi).
x_el = sp.Matrix([rp, 0]) + s*e(q)
r_hinge = s*e(q)
F_cf = (m/l)*Om**2*x_el
v_el = s*w*sp.Matrix([-sp.sin(q), sp.cos(q)])
F_cor = -2*(m/l)*Om*sp.Matrix([-v_el[1], v_el[0]])                          # -2 Om z^ x v
F_g = (m/l)*g*e(-sp.pi/2 - ph)
torque = sp.integrate(cross(r_hinge, F_cf) + cross(r_hinge, F_cor) + cross(r_hinge, F_g), (s, 0, l)) - c*w
check('Newton (turning frame): Coriolis gives no torque about the hinge', sp.integrate(cross(r_hinge, F_cor), (s, 0, l)))
check('Newton (turning frame): I q\'\' = centrifugal + gravity + brake torques, same equation', (I*a - torque) - eom_page)

# Newton in the ground frame for the rotor's torque: the second blade's angular momentum about the hub changes by the torque of
# gravity plus the torque the mother blade exerts on it (hinge force and brake couple). The rotor must supply that torque.
Lz = sp.integrate((m/l)*cross(pos, vel), (s, 0, l))
dLz = plain(Lz.diff(t))
grav_hub = plain(sp.integrate((m/l)*cross(pos, sp.Matrix([0, -g])), (s, 0, l)))
tau_newton = dLz - grav_hub                                                 # = (r_p x F_p)_z + brake couple on the second blade
check('Newton (ground frame): rotor torque = dL_z/dt - gravity torque = Lagrange\'s', (tau_newton - tau_L))

# Koenig: T = 1/2 m v_cm^2 + 1/2 I_c (Om + q')^2
r_cm = rp*e(PH) + (l/2)*e(PH + TH)
T_K = plain(m*r_cm.diff(t).dot(r_cm.diff(t))/2) + Ic*(Om + w)**2/2
check('Koenig: 1/2 m v_cm^2 + 1/2 (m l^2/12)(Om+q\')^2 = page\'s kinetic energy', T_K - T_page)
check('Potential: m g y_cm = page', m*g*plain(r_cm[1]) - V_page)

# energy book: d(T+V)/dt = Om tau_rot - c q'^2 on shell
dTV = (sp.diff(T_page, q)*w + sp.diff(T_page, w)*a + sp.diff(V_page, q)*w + sp.diff(V_page, ph)*Om)
check('Energy book: d(T+V)/dt = Om tau_rot - c q\'^2', (dTV - (Om*tau_page - c*w**2)).subs(a, a_shell))

# ------------------------------------------------------------------------------------------ 3. dimensionless form and P*
R = sp.simplify(mlc*rp/I); G = sp.simplify(mlc*g/(I*Om**2)); kap = sp.Symbol('kappa', positive=True)
check('R = (ml/2) r_p / I = 3 r_p/(2 l)', R - 3*rp/(2*l))
check('G = (ml/2) g/(I Om^2) = 3 g/(2 l Om^2)', G - 3*g/(2*l*Om**2))
check('Divided by I Om^2 (q\'\' = Om^2 q\'\'_phi, q\' = Om q\'_phi, c = kappa I Om): the page\'s blade-angle form',
      (eom_page/(I*Om**2)).subs({a: Om**2*sp.Symbol('A'), w: Om*sp.Symbol('W'), c: kap*I*Om})
      - (sp.Symbol('A') + kap*sp.Symbol('W') + R*sp.sin(q) + G*sp.cos(ph + q)))
# small swings, theta = Re[Th e^{i phi}]: (R - 1 + i kappa) Th = -G (the parametric term G theta sin phi dropped)
Th = -G/(R - 1 + sp.I*kap)
Pbar = kap*I*Om**3*G**2/(2*((R - 1)**2 + kap**2))                          # mean c q'^2 with q' = Om theta', c = kappa I Om
check('Small swings: mean power c Om^2 |Th|^2/2 = I Om^3 kappa G^2 / (2[(R-1)^2 + kappa^2]) (the page\'s linearPower)',
      sp.simplify(kap*I*Om*Om**2*Th*sp.conjugate(Th)/2 - Pbar))
kstar = [k for k in sp.solve(sp.diff(Pbar, kap), kap) if k.is_positive is not False]
print('     best brake(s) from dP/dkappa = 0:', kstar)
check('Best brake kappa* = R - 1 (R > 1 for any second blade shorter than 1.5 r_p)', kstar[0] - (R - 1))
Pst = sp.simplify(Pbar.subs(kap, R - 1))
check('P* = I Om^3 G^2/(4 (R-1)) = (ml/2)^2 g^2/[4 Om ((ml/2) r_p - I)]', Pst - mlc**2*g**2/(4*Om*(mlc*rp - I)))
check('P* = m g^2 l/[8 Om (r_p - 2l/3)]', Pst - m*g**2*l/(8*Om*(rp - 2*l/3)))
tau_peak = sp.simplify(((R - 1)*I*Om)*Om*G/(sp.sqrt(2)*(R - 1)))           # c Om |Th| at kappa*: |Th| = G/(sqrt2 (R-1))
check('Peak brake torque at kappa*: c Om |Th| = (ml/2) g/sqrt2', tau_peak - mlc*g/sp.sqrt(2))
check('Resonance R = 1 needs l = 3 r_p/2', sp.solve(R - 1, l)[0] - 3*rp/2)

# ------------------------------------------------------------------------------------------------- 4. the rotor's bill
# over a steady periodic state the means of total derivatives vanish: (ml/2) r_p (q'' cos q - q'^2 sin q) = (ml/2) r_p d/dt(q' cos q),
# -2 Om q' sin q = 2 Om d/dt(cos q), m g r_p cos phi averages to 0 over whole turns, c q' = d/dt(c q).
total_derivs = mlc*rp*sp.diff(w*sp.cos(q), q)*w + mlc*rp*sp.cos(q)*a + mlc*rp*2*Om*sp.diff(sp.cos(q), q)*w - c*w
check('Bill: tau_rot = -(ml/2) r_p Om^2 sin q + m g r_p cos phi + total derivatives (so P_mean = -(ml/2) r_p Om^3 <sin q>)',
      tau_page - (-mlc*rp*Om**2*sp.sin(q) + m*g*rp*sp.cos(ph) + total_derivs))

# ------------------------------------------------------------------------------------------------------ 5. the generator
# Motor angle N theta: its spin energy 1/2 J N^2 q'^2 adds J N^2 to I; in the unit I Om^2 that is j = J N^2 / I. The rotor's
# work rate with the generator, in the unit I Om^3 per unit rotor angle: tau_rot/(I Om^2) with the device torque -k x.
A_, W_, x_ = sp.symbols('A W x')
tau_g = (mlc*rp*(Om**2*A_*sp.cos(q) - Om**2*(1 + W_)**2*sp.sin(q)) + m*g*rp*sp.cos(ph))/(I*Om**2) - x_
Gp = m*g*rp/(I*Om**2)
check('Generator: rotor work rate = R (q\'\' cos q - (1+q\')^2 sin q) + G_p cos phi - k x, with G_p = m g r_p/(I Om^2)',
      tau_g - (R*(A_*sp.cos(q) - (1 + W_)**2*sp.sin(q)) + Gp*sp.cos(ph) - x_))
check('Generator: G_p = (4/3) G R for the rod (= G R only for a point mass)', Gp - sp.Rational(4, 3)*G*R)

# ------------------------------------------------------------------------------------------------------------- 6. limits
# a general rigid body: inertia I_p about the hinge, first moment M l_c. Its equation is I_p q'' + M l_c [...] + c q' = 0; the point
# pendulum is I_p = M L^2, M l_c = M L, and the rod I_p = m l^2/3, M l_c = m l/2.
Ip, Mlc, M, L = sp.symbols('I_p Ml_c M L', positive=True)
eom_body = Ip*a + Mlc*(Om**2*rp*sp.sin(q) + g*sp.cos(ph + q)) + c*w
check('Limit: the rigid-body equation with I_p = M L^2, M l_c = M L is the point pendulum (1.3)',
      eom_body.subs({Ip: M*L**2, Mlc: M*L}) - (M*L**2*a + M*L*(Om**2*rp*sp.sin(q) + g*sp.cos(ph + q)) + c*w))
# l -> 0 at fixed m is a singular limit: I ~ l^2 while the first moment ~ l, so theta'' ~ 1/l and the blade relaxes to its
# quasi-static angle (torque bracket Om^2 r_p sin q + g cos(phi+q) = 0) in a time ~ sqrt(l). Taken at a fixed c and an arbitrary
# angle the hinge force stays finite, (3/4) m r_p (bracket) cos q, which is that fast relaxation, not a point mass. On the
# quasi-static angle, with the brake in its own unit (c = kappa I Om), the limit is the point mass m at r_p:
tau_qs = tau_page.subs(a, a_shell).subs(c, kap*I*Om).subs(g*sp.cos(ph + q), -Om**2*rp*sp.sin(q))
tau_qs = tau_qs.subs(sp.cos(ph), sp.Symbol('cphi'))                         # keep m g r_p cos(phi) apart from the substitution above
check('Limit l -> 0 (quasi-static angle, c = kappa I Om): the rotor torque becomes that of a point mass m at r_p, m g r_p cos phi',
      sp.limit(tau_qs, l, 0) - m*g*rp*sp.Symbol('cphi'))
check('Limit l -> 0 at fixed c and any angle: the hinge force stays finite, -(3/4) m r_p cos q (Om^2 r_p sin q + g cos(phi+q))',
      sp.limit(tau_page.subs(a, a_shell).subs(c, kap*I*Om), l, 0) - (m*g*rp*sp.cos(ph) - sp.Rational(3, 4)*m*rp*sp.cos(q)*(Om**2*rp*sp.sin(q) + g*sp.cos(ph + q))))
check('Limit l -> 0: the kinetic energy becomes 1/2 m r_p^2 Om^2', sp.limit(T_page, l, 0) - m*rp**2*Om**2/2)
check('Limit l -> 0: P* -> 0 (no lever for gravity)', sp.limit(Pst, l, 0))
# Omega -> 0 with phi fixed at phi0: a hanging physical pendulum. Hanging rest at phi0 + q = -pi/2; small swings about it.
phi0, u = sp.symbols('phi0 u', real=True)
eom0 = eom_page.subs(Om, 0).subs(c, 0).subs({ph: phi0, q: -sp.pi/2 - phi0 + u})
lin = sp.series(eom0, u, 0, 2).removeO()
omega2 = sp.simplify(lin.coeff(u)/I)
check('Limit Om -> 0: hanging physical pendulum, omega^2 = 3 g/(2 l)', omega2 - 3*g/(2*l))

# ------------------------------------------------------------------------------------------------------------- 7. units
from sympy.physics.units import kilogram, meter, second, newton, watt, joule
import sympy.physics.units.util
from sympy.physics.units import Quantity
U = {m: kilogram, l: meter, rp: meter, g: meter/second**2, Om: 1/second, c: newton*meter*second, w: 1/second, a: 1/second**2}
def same_units(name, terms, unit):
    want = sp.physics.units.util.convert_to(unit, [kilogram, meter, second])
    ok = True
    for term in terms:
        got = sp.physics.units.util.convert_to(term.subs(U).subs({q: 0, ph: 0}) if term.has(q, ph) else term.subs(U), [kilogram, meter, second])
        ratio = sp.simplify(got/want)
        if ratio.free_symbols or ratio.atoms(Quantity):
            ok = False
            print('     units differ:', term, '->', got)
    print(('PASS ' if ok else 'FAIL ') + name)
    if not ok:
        fails.append(name)
same_units('Units: every term of the equation of motion is a torque (N m)',
           [I*a, mlc*Om**2*rp, mlc*g, c*w], newton*meter)
same_units('Units: the energies are joules', [I*Om**2, m*rp**2*Om**2, mlc*rp*Om**2, m*g*rp, m*g*l], joule)
same_units('Units: P* and the rotor power are watts', [m*g**2*l/(Om*rp), mlc*rp*Om**3], watt)
same_units('Units: tau* is a torque', [mlc*g], newton*meter)
same_units('Units: kappa = c/(I Om), R, G are pure numbers', [c/(I*Om), mlc*rp/I, mlc*g/(I*Om**2)], 1)

print(('FAIL: ' + '; '.join(fails)) if fails else 'ALL PASS')
raise SystemExit(1 if fails else 0)
