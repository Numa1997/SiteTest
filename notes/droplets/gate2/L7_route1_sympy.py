"""Gate 2, level L7 (chapter 8), route 1: SymPy. Equations (8.1) and (8.2); the soft-hit limit of (8.2).
(8.2) is compared with Sotiropoulou et al. (2021, ACP 21, 9741, Appendix B, eqs. B5 and B8, read in this run), the source that prints Phillips et al.'s (2017) law."""
import sympy as sp
import dims as dm
from dims import ONE, same, length, time, energy

print('== (8.1)  dN_new/dt = sum_pairs K n1 n2 F')
K, n1, n2, F = sp.symbols('K n1 n2 F', positive=True)
same('K n1 n2  [events per m3 per s]', (length**3 / time) * (ONE / length**3)**2, ONE / (length**3 * time))
same('K n1 n2 F  [new particles per m3 per s]', (length**3 / time) * (ONE / length**3)**2, ONE / (length**3 * time))
print('  pair counting: N1 drops of kind 1 and N2 of kind 2 in a volume V: N1 N2 pairs, each meeting at rate K/V -> events per volume = K N1 N2/V^2 = K n1 n2.')
N = sp.symbols('N', positive=True)
print('  same kind: N(N-1)/2 pairs -> events per volume = K N(N-1)/(2 V^2) -> (1/2) K n^2 for large N:', sp.simplify(sp.limit((K * N * (N - 1) / 2 / N**2), N, sp.oo)), '= K/2 (times n^2)')
print('  so a sum over all pairs of bins (i <= j) needs the factor 1/2 for i = j: the script tools/run_cold.cjs uses rate = K n_p n_q (1/2 if i == j), as required.')
print('  limits: F = 0 (rime splintering at -10 C) -> 0 ; F constant -> N_new = F x event rate.')

print('\n== (8.2)  F = alpha A [1 - exp(-(C K0/(alpha A))^gamma)], gamma = 0.3')
al, A_, C, K0, gam, x = sp.symbols('alpha A C K_0 gamma x', positive=True)
Fexpr = al * A_ * (1 - sp.exp(-(C * K0 / (al * A_))**gam))
# units: alpha [m^2] A [m^-2] C [J^-1] K0 [J]
same('alpha A  (surface x bumps per area)', length**2 * (ONE / length**2), ONE)
same('C K0/(alpha A)', (ONE / energy) * energy / (length**2 / length**2), ONE)
y = sp.symbols('y', positive=True)       # y = x^gamma, x = C K0/(alpha A)
print('  with y = (C K0/(alpha A))^gamma:  F = alpha A (1 - exp(-y))')
print('  hard hit  C K0 -> oo (y -> oo): F/(alpha A) ->', sp.limit(1 - sp.exp(-y), y, sp.oo), ' = every bump breaks, F -> alpha A')
print('  no energy K0 -> 0 (y -> 0): F/(alpha A) ->', sp.limit(1 - sp.exp(-y), y, 0, '+'), '(no energy, no fragments)')
dF = sp.simplify(sp.diff(Fexpr, K0))
print('  dF/dK0 =', dF, '; minus alpha A e^-y gamma y/K0 :', sp.simplify(dF - al * A_ * sp.exp(-(C * K0 / (al * A_))**gam) * gam * (C * K0 / (al * A_))**gam / K0), ' (positive: F rises monotonically with the energy)')
dlog = sp.simplify(sp.diff(sp.log(Fexpr), K0) * K0)
print('  local exponent d ln F/d ln K0 =', dlog, ' -> gamma * y e^-y/(1 - e^-y); limit y -> 0:', sp.limit(y * sp.exp(-y) / (1 - sp.exp(-y)), y, 0, '+'), ' so F ~ K0^gamma')
print('  soft hit: 1 - exp(-y) =', sp.series(1 - sp.exp(-y), y, 0, 4), '-> F = alpha A [x^0.3 - x^0.6/2 + x^0.9/6 - ...] = alpha^0.7 A^0.7 (C K0)^0.3 (1 - x^0.3/2 + ...) ; relative correction x^0.3/2 at x = 1.74e-5 :', sp.N(sp.Float('1.74e-5')**sp.Rational(3, 10) / 2, 4))
print('  scaling: K0 x 10 -> F x 10^0.3 =', sp.N(10**sp.Rational(3, 10), 5), ' ; K0 x 1e-8 -> F x', sp.N(sp.Float(1e-8)**sp.Rational(3, 10), 3), ' (the weak power: eight orders of energy lower give only 2.4 orders fewer fragments)')

print('\n== worked example of the text (collision of a 40 um and an 8 um ice sphere at -10 C, 600 hPa)')
rho_i = 900.0
m40 = sp.Rational(4, 3) * sp.pi * (sp.Float('40e-6'))**3 * rho_i; m8 = sp.Rational(4, 3) * sp.pi * (sp.Float('8e-6'))**3 * rho_i
v40, v8 = sp.Float('0.1726'), sp.Float('0.0076')
mu_red = m40 * m8 / (m40 + m8); K0v = mu_red * (v40 - v8)**2 / 2
print('  masses %.4e %.4e kg ; mu_red %.4e kg ; K0 = %.3e J (text 2.6e-14)' % (m40, m8, mu_red, K0v))
T = sp.Float('263.15'); fT = sp.Rational(1, 3) + max(sp.Rational(2, 3) - abs(T - 258) / 9, 0)
D_clamp = sp.Float('5e-4'); a0 = sp.Float('3.78e4') * (1 + sp.Float('0.0079') / D_clamp**sp.Rational(3, 2))
Aval = a0 * fT
alpha = sp.pi * (2 * sp.Float('8e-6'))**2          # surface of the smaller sphere, D = 16 um
aA = alpha * Aval
Cv = sp.Float('6.3e6')
xv = Cv * K0v / aA
Fv = aA * (1 - sp.exp(-xv**sp.Rational(3, 10)))
print('  T = 263.15 K: temperature factor %.4f ; a0(D = 0.5 mm) = %.4e ; A = %.4e m^-2 (B8: A = a0/3 + max(2 a0/3 - a0 |T-258|/9, 0))' % (fT, a0, Aval))
print('  alpha = pi D^2 = %.4e m^2 ; alpha A = %.3e (text 9.2e-3) ; C K0 = %.3e (text 1.6e-7) ; x = %.3e ; F = %.3e (text 3.4e-4) ; 1/F = %.0f collisions per fragment (text "one per three thousand")' % (alpha, aA, Cv * K0v, xv, Fv, 1 / Fv))
print('  soft-hit approximation alpha A x^0.3 = %.3e ; ratio exact/approx = %.4f' % (aA * xv**sp.Rational(3, 10), Fv / (aA * xv**sp.Rational(3, 10))))
print('  with C = 2.2e4 (psi = 3.5e-3): F = %.3e ; ratio of the two C values = %.1f ; (6.3e6/2.2e4)^0.3 = %.2f' % (aA * (1 - sp.exp(-(sp.Float('2.205e4') * K0v / aA)**sp.Rational(3, 10))), 6.3e6 / 2.205e4, (6.3e6 / 2.205e4) ** 0.3))
print('  old rule: 0.001 x m_larger / m_fragment(5 um radius, 900 kg/m3) = %.3f fragments (text 0.51)' % (0.001 * m40 / (sp.Rational(4, 3) * sp.pi * sp.Float('5e-6')**3 * rho_i)))
print('  F_liq(-10 C) from the thesis polynomial: %.2f %% (text 44.55) ; 301 x that = %.1f liquid, %.1f ice per cm3 (text 134.1, 166.9)' % (sum(c * (-10.0)**j for j, c in enumerate([98.9, 4.291, -0.318, -0.02623, -6.398e-4, -5.279e-6])), 301 * 0.4455, 301 * (1 - 0.4455)))
print('  table: 2.80 freezing drops x 1.7 = %.2f ; 0.14 x 12 = %.2f ; ratio old rule 2.6 / 1.6e-3 = %.0f, 2.6 / 0.050 = %.0f' % (2.80 * 1.7, 0.14 * 12, 2.6 / 1.6e-3, 2.6 / 0.050))
