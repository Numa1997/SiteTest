"""SymPy checks of the steps added to the lecture notes in the revision of 30 October 2026 (notes/rotor-pendula/revision.md).

Each block checks one display or one sentence of algebra that the revision writes out; the section is named in its line.
Prints PASS/FAIL per check, exits 1 on any failure.  Run: python3 -I R_revision.py
"""
import sys
import sympy as sp

fails = 0
def check(name, expr_zero):
    global fails
    ok = sp.simplify(expr_zero) == 0
    print(('PASS ' if ok else 'FAIL ') + name)
    fails += 0 if ok else 1

t = sp.symbols('t', real=True)
m, l, rp, g, c, J1, M1d1, Om, s = sp.symbols('m l r_p g c J_1 M1d1 Omega s', positive=True)
I = m*l**2/3
ph, th = sp.Function('varphi')(t), sp.Function('theta')(t)
tau = sp.Symbol('tau')

# 1.3: the energy function and (1.7).  E = sum qdot dL/dqdot - L = T + V, and dE/dt = sum qdot (d/dt dL/dqdot - dL/dq).
T = (J1*ph.diff(t)**2/2 + I*(ph.diff(t) + th.diff(t))**2/2 + m*rp**2*ph.diff(t)**2/2
     + m*l/2*rp*ph.diff(t)*(ph.diff(t) + th.diff(t))*sp.cos(th))
V = M1d1*g*sp.sin(ph) + m*g*(rp*sp.sin(ph) + l/2*sp.sin(ph + th))
L = T - V
qs = [ph, th]
E = sum(q.diff(t)*L.diff(q.diff(t)) for q in qs) - L
check('1.3  energy function equals T + V', E - (T + V))
EL = {q: L.diff(q.diff(t)).diff(t) - L.diff(q) for q in qs}
check('1.3  dE/dt = sum qdot * (Lagrange expression)', E.diff(t) - sum(q.diff(t)*EL[q] for q in qs))
# with the Lagrange equations EL[phi] = tau, EL[theta] = -c thetadot, dE/dt = tau phidot - c thetadot^2 (substitution is linear)

# 2.2: rotating-frame torques about the hinge, gravity included, give (1.6).
e = sp.Matrix([1, 0, 0]); en = sp.Matrix([0, 1, 0]); z = sp.Matrix([0, 0, 1])
th_, ph_, phdd = sp.symbols('theta varphi varphi_dd', real=True)
et = sp.Matrix([sp.cos(th_), sp.sin(th_), 0])
rprime = rp*e + s*et
cross = lambda a, b: a.cross(b)
tq = lambda F: z.dot(cross(s*et, F))
cf = sp.integrate(m/l*tq(Om**2*rprime), (s, 0, l))
eu = sp.integrate(m/l*tq(-phdd*cross(z, rprime)), (s, 0, l))
gvec = g*(-sp.sin(ph_)*e - sp.cos(ph_)*en)               # gravity in the turning frame: phi from the horizontal
gr = sp.integrate(m/l*tq(gvec), (s, 0, l))
check('2.2  centrifugal torque', cf + m*l/2*Om**2*rp*sp.sin(th_))
check('2.2  Euler torque', eu + (I + m*l/2*rp*sp.cos(th_))*phdd)
check('2.2  gravity torque = -(ml/2) g cos(phi+theta)', gr + m*l/2*g*sp.cos(ph_ + th_))
check('2.2  zhat x (zhat x r) = -r in the plane', (cross(z, cross(z, rprime)) + rprime).norm())
# the acceleration in the turning frame: r = Rot(phi) r'(t); second derivative
phf = sp.Function('phi')(t); x1, y1 = sp.Function('x1')(t), sp.Function('y1')(t)
Rm = sp.Matrix([[sp.cos(phf), -sp.sin(phf), 0], [sp.sin(phf), sp.cos(phf), 0], [0, 0, 1]])
r1 = sp.Matrix([x1, y1, 0])
acc_ground_in_rot = Rm.T*(Rm*r1).diff(t, 2)
w = phf.diff(t)*z
rhs = r1.diff(t, 2) + 2*cross(w, r1.diff(t)) + cross(w, cross(w, r1)) + cross(w.diff(t), r1)
check('2.2  rotating-frame acceleration (two differentiations)', (acc_ground_in_rot - rhs).applyfunc(sp.simplify).norm())

# 2.2: the largest tilt of the apparent gravity.
Gam = sp.symbols('Gamma', positive=True)
f = -sp.cos(ph_)/(Gam - sp.sin(ph_))
check('2.2  d tan(theta_b)/d phi', f.diff(ph_) - (Gam*sp.sin(ph_) - 1)/(Gam - sp.sin(ph_))**2)
fx = f.subs(sp.cos(ph_), sp.sqrt(1 - 1/Gam**2)).subs(sp.sin(ph_), 1/Gam)
check('2.2  at sin phi = 1/Gamma, tan theta_b = -1/sqrt(Gamma^2-1)', sp.simplify(fx + 1/sp.sqrt(Gam**2 - 1)))

# 2.3: energy books in the turning frame, rotor steady (phi = Omega t): d/dt[I thdot^2/2 - (ml/2) rp Om^2 cos th] =
#      -(ml/2) g cos(phi+th) thdot - c thdot^2, using (1.6) with phi'' = 0.
thdd = (-(m*l/2)*Om**2*rp*sp.sin(th) - (m*l/2)*g*sp.cos(Om*t + th) - c*th.diff(t))/I
Erel = I*th.diff(t)**2/2 - m*l/2*rp*Om**2*sp.cos(th)
dE = Erel.diff(t).subs(th.diff(t, 2), thdd)
check('2.3  turning-frame energy balance', dE - (-(m*l/2)*g*sp.cos(Om*t + th)*th.diff(t) - c*th.diff(t)**2))

# 3.1: theta sin(phi) for a once-per-turn swing is a constant plus a twice-per-turn part.
Th, de = sp.symbols('Theta delta', real=True)
prod = -Th*sp.cos(ph_ - de)*sp.sin(ph_)
check('3.1  -Theta cos(phi-delta) sin(phi) = -Theta/2 [sin delta + sin(2 phi - delta)]',
      sp.expand_trig(prod + Th/2*(sp.sin(de) + sp.sin(2*ph_ - de))))

# 4.1: Radau IIA (3 stages): nodes, order 5, stability function R(z) -> 0 at infinity (L-stable).
s6 = sp.sqrt(6)
C = sp.Matrix([(4 - s6)/10, (4 + s6)/10, 1])
A = sp.Matrix([[(88 - 7*s6)/360, (296 - 169*s6)/1800, (-2 + 3*s6)/225],
               [(296 + 169*s6)/1800, (88 + 7*s6)/360, (-2 - 3*s6)/225],
               [(16 - s6)/36, (16 + s6)/36, sp.Rational(1, 9)]])
b = A.row(2)
check('4.1  Radau IIA row sums = nodes', (A*sp.ones(3, 1) - C).applyfunc(sp.simplify).norm())
for k in range(1, 6):
    check(f'4.1  Radau IIA quadrature exact for t^{k-1}', sp.simplify(sum(b[i]*C[i]**(k - 1) for i in range(3)) - sp.Rational(1, k)))
zz = sp.symbols('z')
Rz = sp.simplify(1 + zz*(b*(sp.eye(3) - zz*A).inv()*sp.ones(3, 1))[0])
check('4.1  Radau IIA stability function = (1 + 2z/5 + z^2/20)/(1 - 3z/5 + 3z^2/20 - z^3/60)',
      sp.simplify(Rz - (1 + 2*zz/5 + zz**2/20)/(1 - 3*zz/5 + 3*zz**2/20 - zz**3/60)))
check('4.1  R(z) -> 0 as z -> -infinity', sp.limit(Rz, zz, -sp.oo))
check('4.1  R(z) agrees with exp(z) to z^5', sp.series(Rz - sp.exp(zz), zz, 0, 6).removeO())

# 4.2: the hinge force m Om^2 r_cm acting at the hinge has the torque m Om^2 rp (l/2) sin(theta) about the hub.
rcm = rp*e + l/2*et
check('4.2  torque of the hinge pull about the hub', z.dot(cross(rp*e, m*Om**2*rcm)) - m*Om**2*rp*l/2*sp.sin(th_))

# 6.2: Bernoulli in front and behind gives the thrust; with momentum it fixes the speed at the disc.
rho, Ar, v, vd, vw = sp.symbols('rho A v v_d v_w', positive=True)
dp = sp.Rational(1, 2)*rho*(v**2 - vw**2)                      # (p+ - p-) from two Bernoulli lines, p_inf cancels
sol = sp.solve(sp.Eq(Ar*dp, rho*Ar*vd*(v - vw)), vd)
check('6.2  Bernoulli + momentum: v_disc = (v + v_w)/2', sol[0] - (v + vw)/2)
a_ = sp.symbols('a', positive=True)
P = rho*Ar*v*(1 - a_)*(v - v*(1 - 2*a_))*v*(1 - a_)
check('6.2  P = (1/2) rho A v^3 4a(1-a)^2', P - rho*Ar*v**3/2*4*a_*(1 - a_)**2)
check('6.2  dCp/da = 4(1-a)(1-3a)', (4*a_*(1 - a_)**2).diff(a_) - 4*(1 - a_)*(1 - 3*a_))

# 6.5: aerodynamic torque; at fixed tip-speed ratio it is k Omega^2 with k = (1/2) rho pi r^5 Cp/lambda^3.
r, lam, Cp = sp.symbols('r lambda C_p', positive=True)
vv = Om*r/lam
Q = sp.Rational(1, 2)*rho*sp.pi*r**2*vv**3*Cp/Om
check('6.5  Q_aero = (1/2) rho pi r^5 Cp/lambda^3 Omega^2', Q - sp.Rational(1, 2)*rho*sp.pi*r**5*Cp/lam**3*Om**2)

# 7.2: the spring about a lean theta_s held by a steady air force: R/cos(theta_s).
Ft, ths = sp.symbols('F_t theta_s', real=True)
torque = -(m*l/2)*Om**2*rp*sp.sin(th_) + Ft*l/2*sp.cos(th_)
stiff = -torque.diff(th_).subs(th_, ths).subs(Ft, m*Om**2*rp*sp.tan(ths))
check('7.2  stiffness about the lean = (ml/2) rp Om^2 / cos(theta_s)', stiff - (m*l/2)*rp*Om**2/sp.cos(ths))
# 7.2: two pushes a quarter turn apart: the mean power at a fixed brake goes as cc^2 + ss^2.
cc, ss, kap, Rr = sp.symbols('c_c c_s kappa R', positive=True)
Aamp = (cc - sp.I*ss)/((Rr - 1) + sp.I*kap)                   # push Re[(cc - i ss) e^{i phi}] = cc cos + ss sin
Pm = kap*sp.Abs(Aamp)**2/2
check('7.2  power with pushes in cos and sin goes as cc^2 + ss^2', sp.simplify(Pm - kap*(cc**2 + ss**2)/(2*((Rr - 1)**2 + kap**2))))

# 8.1: a stator tilted by beta = beta0 cos(phi): with psi = theta + beta the absolute angle,
#      psi'' + kappa theta' + R psi = push  =>  theta'' + kappa theta' + R theta = push - (R - 1) beta.
b0 = sp.symbols('beta0', real=True)
phv = sp.symbols('varphi', real=True)
thf = sp.Function('th')(phv)
beta = b0*sp.cos(phv)
lhs_psi = (thf + beta).diff(phv, 2) + kap*thf.diff(phv) + Rr*(thf + beta)
check('8.1  tilt gives the push -(R-1) beta', sp.simplify(lhs_psi - (thf.diff(phv, 2) + kap*thf.diff(phv) + Rr*thf) - (Rr - 1)*beta))

# 8.3: max over qdot of (b.qdot)^2/(qdot^T M qdot) = b^T M^-1 b (2 x 2, symbolic), attained at qdot = M^-1 b.
m11, m12, m22, b1, b2, x1s, x2s = sp.symbols('m11 m12 m22 b1 b2 x1 x2', real=True)
Mm = sp.Matrix([[m11, m12], [m12, m22]]); bb = sp.Matrix([b1, b2]); xx = sp.Matrix([x1s, x2s])
ratio = (bb.dot(xx))**2/(xx.T*Mm*xx)[0]
xs = Mm.inv()*bb
check('8.3  ratio at qdot = M^-1 b equals b^T M^-1 b', sp.simplify(ratio.subs({x1s: xs[0], x2s: xs[1]}) - (bb.T*Mm.inv()*bb)[0]))
grad = [sp.simplify(ratio.diff(q).subs({x1s: xs[0], x2s: xs[1]})) for q in (x1s, x2s)]
check('8.3  qdot = M^-1 b is a stationary point of the ratio', sum(abs(gq) for gq in grad))
check('8.3  rod on a hinge: (ml/2)^2/(ml^2/3) = 3m/4', (m*l/2)**2/I - sp.Rational(3, 4)*m)

# 9.1: P*/(ceiling at that swing) = pi/(4 sqrt 2).
check('9.1  ceiling fraction', (sp.Rational(1, 2)/sp.sqrt(2))/(2/sp.pi) - sp.pi/(4*sp.sqrt(2)))

print('ALL PASS' if fails == 0 else f'{fails} FAIL')
sys.exit(1 if fails else 0)
