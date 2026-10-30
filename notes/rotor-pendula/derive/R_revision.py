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

# 1.5: the action of a swing of amplitude a in u = -A cos(theta - theta_b): J = (8 sqrt A/pi)[E(k) - (1-k^2) K(k)], k = sin(a/2),
#      checked against (1/2pi) * closed integral of theta' d theta at three amplitudes, and its two limits.
Aa = sp.Integer(90)
for amp in (sp.Rational(1, 2), 2, sp.Rational(29, 10)):
    k2 = sp.sin(amp/2)**2
    Jf = 8*sp.sqrt(Aa)/sp.pi*(sp.elliptic_e(k2) - (1 - k2)*sp.elliptic_k(k2))       # sympy's elliptic_k(m), m = k^2
    u_ = sp.symbols('u_')
    Jn = 2/(2*sp.pi)*sp.Integral(sp.sqrt(2*Aa*(sp.cos(u_) - sp.cos(amp))), (u_, -amp, amp))
    check(f'1.5  elliptic action at a = {amp}', sp.N(Jf - Jn, 12) if abs(sp.N(Jf - Jn, 12)) > 1e-9 else 0)
kk = sp.symbols('k', positive=True)
Jk = 8/sp.pi*(sp.elliptic_e(kk**2) - (1 - kk**2)*sp.elliptic_k(kk**2))
check('1.5  small swing: J -> 2 k^2 ~ a^2/2 (per sqrt A)', sp.limit(Jk/kk**2, kk, 0) - 2)
check('1.5  a -> pi: J -> J_s = 8/pi (per sqrt A), numerically at k = 1 - 1e-14', 0 if abs(sp.N(Jk.subs(kk, 1 - sp.Rational(1, 10**14)) - 8/sp.pi, 20)) < 1e-10 else 1)
# 1.5: near the top x'' = A x, x = x_min cosh(sqrt A (phi - phi0)) solves it with x' = 0 at phi0.
xm, ph0 = sp.symbols('x_min varphi_0', positive=True)
xs_ = xm*sp.cosh(sp.sqrt(Aa)*(phv - ph0))
check('1.5  cosh solves x\'\' = A x', sp.simplify(xs_.diff(phv, 2) - Aa*xs_))
check('1.5  arccosh(1/x) ~ ln(2/x) as x -> 0', sp.limit(sp.acosh(1/xm) - sp.log(2/xm), xm, 0))

# 6.4: Kolmogorov's exponents from dimensions: E(k) [m^3 s^-2] = eps^a [m^2 s^-3]^a k^b [m^-b].
aK, bK = sp.symbols('a_K b_K')
solK = sp.solve([sp.Eq(2*aK - bK, 3), sp.Eq(-3*aK, -2)], [aK, bK])
check('6.4  Kolmogorov: a = 2/3, b = -5/3', abs(solK[aK] - sp.Rational(2, 3)) + abs(solK[bK] + sp.Rational(5, 3)))

# 1.5: the adiabatic step for the harmonic case H = p^2/2 + w(lam)^2 q^2/2: dH/dlam / dH/dp = -dp/dlam on the orbit,
#      and the action (1/2pi) closed integral p dq = E/w.
qq, pp, EE, lm = sp.symbols('q p E lambda', positive=True)
wf = sp.Function('w')(lm)
Hh = pp**2/2 + wf**2*qq**2/2
porb = sp.sqrt(2*EE - wf**2*qq**2)
check('1.5  on the orbit dH/dlam + dH/dp * dp/dlam = 0', sp.simplify((Hh.diff(lm) + Hh.diff(pp)*porb.diff(lm)).subs(pp, porb)))
amp = sp.sqrt(2*EE)/wf
Jh = 2*sp.integrate(sp.sqrt(2*EE - sp.Symbol('W', positive=True)**2*qq**2), (qq, -sp.sqrt(2*EE)/sp.Symbol('W', positive=True), sp.sqrt(2*EE)/sp.Symbol('W', positive=True)))/(2*sp.pi)
check('1.5  harmonic action = E/w', sp.simplify(Jh - EE/sp.Symbol('W', positive=True)))

# 8.2: the linear equations of the blade's edgewise mode x and the second blade's absolute angle chi (L3_shake2.py's Lagrangian,
#      one rod, mode slope at the tip Phi = 1): the forms written in the notes, and no Coriolis (first-derivative) terms.
Pp_, me_, ke_ = sp.symbols('Phi_p m_e k_e', positive=True)
xx_, ch_ = sp.Function('x')(t), sp.Function('chi')(t)
phw = Om*t
er_ = sp.Matrix([sp.cos(phw), sp.sin(phw)]); et_ = sp.Matrix([-sp.sin(phw), sp.cos(phw)])
pos_ = rp*er_ + Pp_*xx_*et_ + s*sp.Matrix([sp.cos(phw + ch_), sp.sin(phw + ch_)])
v_ = pos_.diff(t)
Lx = me_/2*xx_.diff(t)**2 + sp.integrate(m/l*v_.dot(v_)/2, (s, 0, l)) - ke_/2*xx_**2
ep = sp.symbols('ep')
def lin(gq):
    E_ = sp.diff(Lx.diff(gq.diff(t)), t) - Lx.diff(gq)
    return sp.expand(sp.trigsimp(sp.series(E_.subs({xx_: ep*xx_, ch_: ep*ch_}).doit(), ep, 0, 2).removeO().subs(ep, 1)))
ex, ec = lin(xx_), lin(ch_)
want_x = (me_ + m)*xx_.diff(t, 2) + (ke_ - m*Om**2)*xx_ + m*l/2*(ch_.diff(t, 2) - Om**2*ch_)
want_c = I*ch_.diff(t, 2) + m*l/2*Om**2*rp*ch_ + m*l/2*(xx_.diff(t, 2) - Om**2*xx_)
check('8.2  mode equation as written (Phi = 1)', sp.simplify(ex.subs(Pp_, 1) - want_x))
check('8.2  second blade equation as written (Phi = 1)', sp.simplify(ec.subs(Pp_, 1) - want_c))
check('8.2  no first-derivative (Coriolis) terms', sum(abs(e_.coeff(g_.diff(t))) for e_ in (ex, ec) for g_ in (xx_, ch_) if e_.coeff(g_.diff(t)) != 0) if any(e_.coeff(g_.diff(t)) != 0 for e_ in (ex, ec) for g_ in (xx_, ch_)) else 0)

# 6.3: the wake's swirl as a share of the power, C_p/(4(1-a) lambda^2) = 2/(9 lambda^2) at the Betz point; the best ratio of
#      alpha/lambda^2 + beta eps lambda is (2 alpha/(beta eps))^(1/3).
Qs, md_, r_, v0, lm_, al_, be_, ep_ = sp.symbols('Q mdot r v lambda alpha beta epsilon', positive=True)
a3, Cp3 = sp.symbols('a C_p', positive=True)
frac_ = (md_*(Qs/(md_*r_))**2/2)/(Qs*Om)
frac_ = sp.simplify(frac_.subs(Qs, Cp3*v0**2/(2*(1 - a3))*md_/Om).subs(Om, lm_*v0/r_))
check('6.3  swirl share = C_p/(4(1-a) lambda^2)', sp.simplify(frac_ - Cp3/(4*(1 - a3)*lm_**2)))
check('6.3  = 2/(9 lambda^2) at a = 1/3, C_p = 16/27', sp.simplify(frac_.subs({a3: sp.Rational(1, 3), Cp3: sp.Rational(16, 27)}) - sp.Rational(2, 9)/lm_**2))
lopt = sp.solve(sp.diff(al_/lm_**2 + be_*ep_*lm_, lm_), lm_)[0]
check('6.3  best ratio (2 alpha/(beta eps))^(1/3)', sp.simplify(lopt - (2*al_/(be_*ep_))**sp.Rational(1, 3)))

# 6.3: the drag share averaged over the disc, weighted by r dr: (2/3) lambda C_D/C_L; and the best ratio (2/3 C_L/C_D)^(1/3).
rr_, R0_ = sp.symbols('r R_0', positive=True)
check('6.3  disc average of r/R weighted by r dr = 2/3', sp.integrate(rr_/R0_*rr_, (rr_, 0, R0_))/sp.integrate(rr_, (rr_, 0, R0_)) - sp.Rational(2, 3))
check('6.3  2 c_s/c_d = 2/3', 2*sp.Rational(2, 9)/sp.Rational(2, 3) - sp.Rational(2, 3))

# 8.2: the frequency-domain system. With y, chi ~ e^{i w t}, the two equations of 8.2 (generator torque -c(chidot - Phi' ydot) on
#      the blade, +Phi' c(...) on the mode) become a symmetric 2x2 system; check it against the time-domain equations.
w_, Ph_, c_, cb_, mb2, kb2, F_ = sp.symbols('omega Phi_d c c_b m_b k_b F', real=True)
yh, chh = sp.symbols('yhat chihat')
iw = sp.I*w_
eq_y = (mb2 + m)*(iw**2*yh) + cb_*iw*yh + (kb2 - m*Om**2)*yh + m*l/2*(iw**2*chh - Om**2*chh) - Ph_*c_*(iw*chh - Ph_*iw*yh) - F_
eq_c = I*iw**2*chh + m*l/2*Om**2*rp*chh + m*l/2*(iw**2*yh - Om**2*yh) + c_*(iw*chh - Ph_*iw*yh)
Mw = sp.Matrix([[kb2 - m*Om**2 - (mb2 + m)*w_**2 + iw*(cb_ + Ph_**2*c_), -m*l/2*(w_**2 + Om**2) - iw*Ph_*c_],
                [-m*l/2*(w_**2 + Om**2) - iw*Ph_*c_, m*l/2*Om**2*rp - I*w_**2 + iw*c_]])
lhs_ = Mw*sp.Matrix([yh, chh]) - sp.Matrix([F_, 0])
check('8.2  frequency system, mode row', sp.expand(lhs_[0] - eq_y))
check('8.2  frequency system, second-blade row', sp.expand(lhs_[1] - eq_c))
check('8.2  the matrix is symmetric', sp.expand(Mw[0, 1] - Mw[1, 0]))

# 9.1: P*/(ceiling at that swing) = pi/(4 sqrt 2).
check('9.1  ceiling fraction', (sp.Rational(1, 2)/sp.sqrt(2))/(2/sp.pi) - sp.pi/(4*sp.sqrt(2)))

print('ALL PASS' if fails == 0 else f'{fails} FAIL')
sys.exit(1 if fails else 0)
