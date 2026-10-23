"""Gate 2, level L2 (chapter 3), route 1: SymPy. Equations (3.1)-(3.5)."""
import sympy as sp
from dims import *
t, s_ = sp.symbols('t s', positive=True)
r, R, U, mu, rhow, rhoa, g, m_ = sp.symbols('r R U mu rho_w rho_a g m', positive=True)
St, S, p, eta, kappa = sp.symbols('St S p eta kappa', positive=True)

print('== (3.1)  partner in the collector frame (frame moves at constant velocity: inertial, no extra force)')
# m dv/dt = 6 pi mu r (u - v) - (m - m_displaced) g e_z ;  divide by 6 pi mu r
mp = sp.Rational(4, 3) * sp.pi * r**3 * rhow
tau0 = sp.simplify(mp / (6 * sp.pi * mu * r))
print('  m/(6 pi mu r) =', tau0, ' ; printed Stokes tau = 2 rho_w r^2/(9 mu): difference', sp.simplify(tau0 - 2 * rhow * r**2 / (9 * mu)))
gs = g * (1 - rhoa / rhow)
wt = sp.simplify(mp * (1 - rhoa / rhow) * g / (6 * sp.pi * mu * r))
print('  (weight - buoyancy)/(6 pi mu r) =', wt, ' = tau0 g* :', sp.simplify(wt - tau0 * gs) == 0, '  and tau0 g* = v_Stokes(r):', sp.simplify(tau0 * gs - 2 * (rhow - rhoa) * g * r**2 / (9 * mu)) == 0)
print('  so tau dv/dt = u - v - tau g* e_z with tau = v(r)/g* is (3.1); in still air v -> -tau g* e_z = -v(r) e_z: partner falls at v(r)')
same('tau = 2 rho_w r^2/(9 mu)', dens * m**2 / visc, time)
same('tau g*', time * accel, speed)

print('\n== (3.2)  scaling: x = R y, v = U w, u = U a, t = (R/U) s')
y1, w1, a1, Rr, Uu, tau, gstar = sp.symbols('y w a R U tau gstar', positive=True)
Sf = sp.Function('w')(s_)
# tau dv/dt = u - v - tau g* e_z with v = U w(s), t = R s/U  =>  tau U (U/R) dw/ds = U a - U w - tau g*
lhs = tau * Uu * (Uu / Rr) * sp.Symbol('dw')
rhs = Uu * a1 - Uu * w1 - tau * gstar
eqn = sp.expand((lhs - rhs) / Uu)           # divide by U
St_ = tau * Uu / Rr; S_ = tau * gstar / Uu
print('  divided by U:', sp.collect(eqn, sp.Symbol('dw')))
print('  coefficient of dw/ds = tau U/R = St ;  settling term tau g*/U = S :', sp.simplify(eqn.coeff(sp.Symbol('dw')) - St_) == 0, ', and with tau = v(r)/g*, S = v(r)/U :', sp.simplify(S_.subs(tau, sp.Symbol('vr') / gstar) - sp.Symbol('vr') / Uu) == 0)
same('St = tau U / R', time * speed / length, ONE)
same('S = v(r)/U', speed / speed, ONE)
print('  contact when |x| = R + r  <=>  |y| = 1 + r/R = 1 + p')

print('\n== two model flows (used in 3.3 and the small-collector paragraph)')
rr_, th = sp.symbols('r_ theta', positive=True)
Apot = 1
psi_pot = sp.Rational(1, 2) * U * sp.sin(th)**2 * (rr_**2 - Apot / rr_)
E2 = lambda ps: sp.diff(ps, rr_, 2) + sp.sin(th) / rr_**2 * sp.diff(sp.diff(ps, th) / sp.sin(th), th)
print('  potential: E2 psi =', sp.simplify(E2(psi_pot)), '(0: the stream function of an irrotational flow) ; u_r(r=1) =', sp.simplify((sp.diff(psi_pot, th) / (rr_**2 * sp.sin(th))).subs(rr_, 1)), '(no penetration) ; u_th(r=1) =', sp.simplify((-sp.diff(psi_pot, rr_) / (rr_ * sp.sin(th))).subs(rr_, 1)), '(slips)')
ur_pot = sp.diff(psi_pot, th) / (rr_**2 * sp.sin(th)); ur_cr = sp.diff(sp.sin(th)**2 / 2 * U * (rr_**2 - sp.Rational(3, 2) * rr_ + 1 / (2 * rr_)), th) / (rr_**2 * sp.sin(th))
ax_pot = sp.simplify(ur_pot.subs(th, sp.pi)); ax_cr = sp.simplify(ur_cr.subs(th, sp.pi))
print('  axis below the sphere (th = pi): u_r potential =', ax_pot, ' ; creeping =', ax_cr, ' (negative = toward the sphere)')
inward_pot = sp.simplify(-ax_pot.subs(rr_, 1 + eta) / U); inward_cr = sp.simplify(-ax_cr.subs(rr_, 1 + eta) / U)
print('  approach speed toward the surface / U: potential', inward_pot, '-> series', sp.series(inward_pot, eta, 0, 3).removeO(), ' (text 1-(1+eta)^-3 ~ 3 eta)')
print('                                          creeping ', inward_cr, '-> series', sp.series(inward_cr, eta, 0, 4).removeO(), ' (text: vanishes as 3/2 eta^2)')
print('  small-collector paragraph: creeping approach at eta = p = 0.2 :', sp.N(inward_cr.subs(eta, sp.Rational(1, 5)), 5), ' (text 0.039) against S = 0.045')

print('\n== (3.3)  St eta\'\' + eta\' + 3 eta = 0')
# axis, p=0, S=0: eta = distance from surface; the partner moves toward the surface (d eta/ds = w) driven by air speed -3 eta
etaf = sp.Function('eta')
ode = sp.Eq(St * etaf(s_).diff(s_, 2) + etaf(s_).diff(s_) + 3 * etaf(s_), 0)
cs = sp.solve(St * kappa**2 + kappa + 3, kappa)
print('  characteristic roots of St k^2 + k + 3 = 0 :', cs, ' ; printed (-1 +- sqrt(1-12 St))/(2 St): ', [sp.simplify(c_ - (-1 + sg * sp.sqrt(1 - 12 * St)) / (2 * St)) for c_, sg in zip(cs, (-1, 1))] if sp.simplify(cs[0] - (-1 - sp.sqrt(1 - 12 * St)) / (2 * St)) == 0 else 'order swapped')
print('  discriminant 1 - 12 St = 0 at St =', sp.solve(1 - 12 * St, St))
print('  (3.4) St_c = 1/12 ; at St_c the double root is kappa =', sp.simplify(cs[0].subs(St, sp.Rational(1, 12))), '= -1/(2 St_c) = -6')
# the physical start: partner slaved to the air, w0 = -3 eta0.  Crossing of zero?
e0, c1, c2 = sp.symbols('eta0 c1 c2')
k1, k2 = sp.symbols('k1 k2')
sol = sp.solve([c1 + c2 - e0, c1 * k1 + c2 * k2 - (-3 * e0)], [c1, c2])
print('  overdamped, slaved start eta\'(0) = -3 eta0 : c1 =', sp.simplify(sol[c1]), ', c2 =', sp.simplify(sol[c2]))
print('  general start eta\'(0)=v0: c_slow >= 0 <=> v0 >= k_fast*eta0 ; the physical slaved start has v0 = -3 eta0 >= k_fast eta0 whenever |k_fast| >= 3:')
for Stv in [sp.Rational(1, 100), sp.Rational(1, 24), sp.Rational(1, 13), sp.Rational(1, 12)]:
    kf = sp.N((-1 - sp.sqrt(1 - 12 * Stv)) / (2 * Stv)); print('    St = %s : k_fast = %.4f (>= 3 in magnitude: %s)' % (Stv, kf, abs(kf) >= 3))
omega = sp.sqrt(12 * St - 1) / (2 * St)
print('  underdamped (12 St > 1): eta = exp(-s/(2 St)) (A cos(w s) + B sin(w s)), w =', omega, ' -> zero crossing at s = pi/w - phase (every period): partner reaches the surface')
print('  units: St eta\'\' : St dimensionless, eta in R, s in R/U -> all three terms in R (consistent). Limit St -> 0: eta\' = -3 eta, eta = eta0 exp(-3 s): approaches but never reaches (inertialess partner)')

print('\n== (3.5)  E = b_c^2/(1+p)^2')
b, bc, n_, rc, Sset, Z = sp.symbols('b b_c n r_c S Z', positive=True)
rc_ = 1 + p
# hit rate = n * (flux per area = (1-S)U) * pi bc^2 ; geometric = n (1-S) U pi (1+p)^2 R^2 ; ratio:
Eexp = (n_ * (1 - Sset) * sp.pi * bc**2) / (n_ * (1 - Sset) * sp.pi * rc_**2)
print('  hit rate / geometric rate =', sp.simplify(Eexp), ' (the factor n (1-S) U cancels, S enters only through U_rel)')
x_, q_ = sp.symbols('x q', positive=True)
for name, gfun in [('creeping', lambda q: 1 - sp.Rational(3, 2) / q + 1 / (2 * q**3)), ('potential', lambda q: 1 - 1 / q**3)]:
    psi_f = lambda x, q: sp.Rational(1, 2) * x**2 * gfun(q)   # psi/(U R^2) in terms of x = sin(th) q,  q = |y|  : psi = 1/2 q^2 sin^2 g(q) = 1/2 x^2 g(q)
    # far start: q -> oo , g -> 1 : psi -> 1/2 b^2.  Finite start at distance Z on the axis: x = b, q ~ sqrt(b^2+Z^2)
    flux = 2 * (psi_f(b, sp.sqrt(b**2 + Z**2)) - sp.Rational(1, 2) * Sset * b**2) / ((1 - Sset) * rc_**2)
    print('  %-9s finite start: E = 2 (psi(b) - S b^2/2)/((1-S)(1+p)^2) ; lim Z->oo ->' % name, sp.simplify(sp.limit(flux, Z, sp.oo)), ' (= b^2/(1+p)^2)')
    # inertialess, S=0: the grazing streamline touches q=1+p at theta=pi/2
    Eint = sp.simplify(gfun(1 + p))
    print('  %-9s zero inertia, S=0: b_c^2 = 2 psi(1+p, th=pi/2) -> E_int = %s ; p=0: %s ; p=0.2: %s ; p=1: %s' % (name, Eint, sp.simplify(Eint.subs(p, 0)), sp.N(Eint.subs(p, sp.Rational(1, 5)), 6), sp.N(Eint.subs(p, 1), 6)))
print('  limit St -> oo (straight paths): b_c = 1+p, E = 1. Limit p -> 0, St < St_c: E = 0 (no hit). Range 0 <= E <= 1 for the capture area against the geometric area; E can exceed 1 only when the capture area exceeds pi(R+r)^2 (does not happen for one-sided flow)')
same('E = b_c^2/(1+p)^2', length**2 / length**2, ONE)
