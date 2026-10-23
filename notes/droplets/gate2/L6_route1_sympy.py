"""Gate 2, level L6 (chapter 7), route 1: SymPy. No numbered equation. Checks: Kolmogorov time, Stokes numbers, the epsilon -> 0 limit of the Ayala-Rosa-Wang
weak-inertia formula as printed in the paper (eq. 81 with the corrigendum's form of the mean |w_r|), and the units of every term.
The formula is transcribed from the paper (Ayala, Rosa and Wang 2008, New J. Phys. 10, 075016, eq. 81, eq. 26, Table 2 and the corrigendum
10 (2008) 099802), NOT from physics.cjs."""
import sympy as sp
import dims as dm
from dims import ONE, same, length, time, speed, accel
nu_, eps_, tK = sp.symbols('nu epsilon tau_K', positive=True)
a_, b_ = sp.symbols('a b')
print('== Kolmogorov time by dimensional analysis: nu^a eps^b with the dimension of a time')
# nu: L^2 T^-1 ; eps: L^2 T^-3 ; require L^0 T^1
sol = sp.solve([2 * a_ + 2 * b_, -a_ - 3 * b_ - 1], [a_, b_], dict=True)[0]
print('   exponents:', sol, ' -> tau_K = (nu/eps)^(1/2)  ; printed sqrt(nu/eps):', sp.simplify(nu_**sol[a_] * eps_**sol[b_] - sp.sqrt(nu_ / eps_)) == 0)
same('tau_K = sqrt(nu/eps)', (dm.nu / dm.eps) ** sp.Rational(1, 2), time)
same('v_K = (nu eps)^(1/4)', (dm.nu * dm.eps) ** sp.Rational(1, 4), speed)
print('   smallest eddies: v_K eta/nu with eta = (nu^3/eps)^(1/4) =', sp.simplify(((nu_ * eps_)**sp.Rational(1, 4) * (nu_**3 / eps_)**sp.Rational(1, 4)) / nu_), '(Reynolds number 1 at the Kolmogorov scale)')
print('   units of the energy dissipation rate per unit mass eps: m^2 s^-3 =', dm.eps, '(J/kg/s)')

print('\n== the turbulent relative velocity in the weak-inertia limit (paper eq. 81 + eq. 26 + corrigendum eq. 4)')
R, nu, eps, g, d, a0, vk, tk, A, B, Rl = sp.symbols('R nu epsilon g d a0 v_k tau_k A B R_lambda', positive=True)
# d = tau_p1 - tau_p2 ; A = v_p1 tau_p1 - v_p2 tau_p2 ; vk, tk Kolmogorov scales
sigma2 = R**2 * eps / (15 * nu) + d**2 * a0 * (vk / tk)**2 + A**2 * 2 * eps / (15 * nu)
wr = sp.sqrt(2 / sp.pi) * sp.sqrt(sigma2 + sp.pi / 8 * d**2 * g**2)
wg = d * g / 2
ratio = wr / wg
print('   ratio <|w_r|> / (gravitational |v1 - v2|/2) with |v1 - v2| = d g :', sp.simplify(ratio))
subsK = {vk: (nu * eps)**sp.Rational(1, 4), tk: sp.sqrt(nu / eps)}
r_eps = sp.simplify(ratio.subs(subsK))
print('   with v_k, tau_k substituted: ratio =', r_eps)
print('   limit eps -> 0 :', sp.limit(r_eps, eps, 0, '+'), '  (gravity alone)')
ser = sp.series(r_eps, eps, 0, sp.Rational(3, 2)).removeO()
print('   expansion in eps (leading terms):', sp.simplify(ser))
lin = sp.simplify(sp.diff(r_eps, eps).subs(eps, 0)) if False else None
c1 = sp.simplify(sp.limit((r_eps - 1) / eps, eps, 0, '+'))
print('   (ratio - 1)/eps as eps -> 0 =', c1, ' = 4/(pi d^2 g^2) [R^2/(15 nu) + 2 A^2/(15 nu)]  :', sp.simplify(c1 - 4 / (sp.pi * d**2 * g**2) * (R**2 / (15 * nu) + 2 * A**2 / (15 * nu))) == 0, '(the acceleration term enters at eps^(3/2))')
print('   limit d -> 0 (equal drops): ratio -> oo, i.e. the gravitational reference vanishes; the formula is for size ratios where gravity dominates (text: ratio below 0.6)')
print('   sigma = 0 : <|w_r|> =', sp.simplify(wr.subs(sigma2, 0)) if False else sp.simplify(sp.sqrt(2 / sp.pi) * sp.sqrt(sp.pi / 8 * d**2 * g**2)), ' = d g/2 : gravity only')
print('   units of each term of sigma^2 [m^2/s^2]:')
same('R^2 eps/(15 nu)', length**2 * dm.eps / dm.nu, speed**2)
same('d^2 a0 (v_k/tau_k)^2   (d = tau difference [s])', time**2 * (speed / time)**2, speed**2)
same('A^2 2 eps/(15 nu)  (A = v tau [m])', length**2 * dm.eps / dm.nu, speed**2)
same('(pi/8) d^2 g^2', time**2 * accel**2, speed**2)
print('   a0 = (11 + 7 R_lambda)/(205 + R_lambda) at R_lambda = 2e4:', sp.N(sp.Rational(11 + 7 * 20000, 205 + 20000), 8), '(-> 7 as R_lambda -> oo; Table 2 of the paper)')

print('\n== Stokes numbers quoted in the text')
tau_p40, tau_p8, tauK = sp.symbols('tau_p40 tau_p8 tauK')
print('   tau_p = v/g (the drag-corrected response time of chapter 3 and Table 2 of the paper: v_p = tau_p |g|); with v_Beard(40 um) = 0.17709 m/s: tau_p = %.2f ms ; v_Beard(8 um) = 0.007963: %.3f ms' % (0.17709 / 9.81 * 1e3, 0.007963 / 9.81 * 1e3))
print('   tau_K = sqrt(nu/eps) with nu = 1.6935e-5 m^2/s (10 C, 850 hPa), eps = 1e-2 m^2/s^3: %.2f ms ; St(40 um) = %.3f ; St(8 um) = %.4f' % (1e3 * (1.6935e-5 / 1e-2)**0.5, 0.17709 / 9.81 / (1.6935e-5 / 1e-2)**0.5, 0.007963 / 9.81 / (1.6935e-5 / 1e-2)**0.5))
