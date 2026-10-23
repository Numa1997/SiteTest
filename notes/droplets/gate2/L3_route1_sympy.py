"""Gate 2, level L3 (chapter 4), route 1: SymPy. Equations (4.1)-(4.2)."""
import sympy as sp
from dims import *
m1, m2 = sp.symbols('m1 m2', positive=True)
v1 = sp.Matrix(sp.symbols('v1x v1y v1z', real=True)); v2 = sp.Matrix(sp.symbols('v2x v2y v2z', real=True))
Msum = m1 + m2
print('== (4.1)  kinetic energy = centre-of-mass part + relative part')
V = (m1 * v1 + m2 * v2) / Msum            # centre-of-mass velocity: the point where total momentum is M V
dv = v1 - v2
print('  v1 = V + m2/M dv :', sp.simplify(v1 - (V + m2 / Msum * dv)).T, ' ; v2 = V - m1/M dv :', sp.simplify(v2 - (V - m1 / Msum * dv)).T, ' (both 0: the two decompositions printed in the text are exactly the centre-of-mass split)')
KE = sp.Rational(1, 2) * m1 * v1.dot(v1) + sp.Rational(1, 2) * m2 * v2.dot(v2)
mured = m1 * m2 / Msum
rhs = sp.Rational(1, 2) * Msum * V.dot(V) + sp.Rational(1, 2) * mured * dv.dot(dv)
print('  KE - [M V^2/2 + mu_red dv^2/2] =', sp.simplify(sp.expand(KE - rhs)))
# the cross term explicitly: m1 (m2/M) V.dv - m2 (m1/M) V.dv
cross = sp.simplify(m1 * V.dot(m2 / Msum * dv) - m2 * V.dot(m1 / Msum * dv))
print('  cross terms m1 V.(m2/M dv) + m2 V.(-m1/M dv) =', cross)
print('  momentum conservation: total momentum m1 v1 + m2 v2 = M V, so V is constant in any collision (internal forces); a perfect merger ends with all mass at V:')
KE_after_merge = sp.Rational(1, 2) * Msum * V.dot(V)
print('  KE before - KE after merger (energy available to deform / dissipate) =', sp.simplify(sp.expand(KE - KE_after_merge - sp.Rational(1, 2) * mured * dv.dot(dv))), '(0 means it equals mu_red dv^2/2 = CKE)')
same('CKE = mu_red dv^2/2', kg * speed**2, energy)
print('  limits: m2 -> oo (wall): mu_red ->', sp.limit(mured, m2, sp.oo), '(=m1, CKE = m1 dv^2/2) ; equal masses mu_red =', sp.simplify(mured.subs(m2, m1)), ' (= m/2) ; dv = 0 -> CKE = 0 ; CKE >= 0 always (mu_red > 0)')
print('  mu_red <= min(m1, m2):', sp.simplify(sp.Min(m1, m2) - mured).subs({m1: 2, m2: 3}), '(spot value 2 - 6/5 = 4/5 > 0)')

print('\n== (4.2)  We = CKE/(pi sigma d_c^2) , E_coal = exp(-1.15 We)')
d1, d2, sigma_, rho, dc = sp.symbols('d1 d2 sigma rho d_c', positive=True)
# volume conservation: (pi/6) d_c^3 = (pi/6)(d1^3 + d2^3)
dc_expr = sp.solve(sp.Eq(sp.pi / 6 * dc**3, sp.pi / 6 * (d1**3 + d2**3)), dc)
print('  merged diameter from volume conservation (equal densities):', dc_expr, ' ; printed (d1^3+d2^3)^(1/3)')
print('  surface energy of the merged drop sigma * pi d_c^2 =', sp.simplify(sigma_ * sp.pi * dc**2), ' (area of a sphere = pi d^2)')
same('We = CKE/(pi sigma d_c^2)', energy / (sigma * length**2), ONE)
same('sigma = N/m', sigma, energy / length**2)
We = sp.symbols('We', positive=True)
Ecoal = sp.exp(-sp.Rational(115, 100) * We)
print('  E_coal(0) =', Ecoal.subs(We, 0), ', limit We->oo =', sp.limit(Ecoal, We, sp.oo), ', derivative sign:', sp.simplify(sp.diff(Ecoal, We)), '(< 0: more energy, less coalescence)')
print('  E_coal = 1/2 at We =', sp.N(sp.log(2) / sp.Rational(115, 100), 6), '; E_coal = 0.55 -> We =', sp.N(-sp.log(sp.Rational(55, 100)) / sp.Rational(115, 100), 4), '(text: We = 0.52 -> E = 0.55): exp(-1.15*0.52) =', sp.N(sp.exp(-sp.Rational(115, 100) * sp.Rational(52, 100)), 4))
print('  text: We = 61 -> exp(-1.15*61) =', sp.N(sp.exp(-sp.Rational(115, 100) * 61), 3), '(switched off, as stated)')
print('  text: We = 2.0e-5 -> E_coal =', sp.N(sp.exp(-sp.Rational(115, 100) * sp.Rational(2, 100000)), 7), ' (text 0.99998) ; 1/We =', 1 / 2.0e-5, '(text: surface 50 000 times stiffer)')
print('  NOTE: the numerical factor 1.15 and the exponential form are a fit (Straub et al. 2010 form; the thesis law); no derivation exists. Only structure, units, limits are checked here.')
