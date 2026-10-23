"""L8 (Gate 1 and Gate 2 algebra): surface energy as a Lyapunov function of collection, the energy-only Monte Carlo, maximum entropy.
   python3 derive/L8_sympy.py
"""
import sympy as sp

m, mp, rho, sig, x, p, r, R = sp.symbols('m m_p rho sigma x p r R', positive=True)

# (a) surface of a sphere as a function of its mass: 4 pi r^2 = (36 pi)^(1/3) rho^(-2/3) m^(2/3)
rad = (3 * m / (4 * sp.pi * rho)) ** sp.Rational(1, 3)
c = sp.simplify(4 * sp.pi * rad ** 2 / m ** sp.Rational(2, 3))
print('(a) 4 pi r^2 / m^(2/3) =', c, '; equals (36 pi)^(1/3) rho^(-2/3):', sp.simplify(c - (36 * sp.pi) ** sp.Rational(1, 3) * rho ** sp.Rational(-2, 3)) == 0)

# (b) a merger changes sum m^(2/3) by (m+m')^(2/3) - m^(2/3) - m'^(2/3) = (m+m')^(2/3) [1 - x^(2/3) - (1-x)^(2/3)], x = m/(m+m')
g = 1 - x ** sp.Rational(2, 3) - (1 - x) ** sp.Rational(2, 3)
print('(b) bracket/(m+m\')^(2/3) =', g)
print('    x^(2/3) > x on (0,1), so x^(2/3) + (1-x)^(2/3) > x + (1-x) = 1 and the bracket is negative: every merger lowers the surface')
xs = sp.solve(sp.diff(g, x), x)
print('    stationary point', xs, '; bracket there', sp.nsimplify(g.subs(x, xs[0])), '=', sp.N(g.subs(x, xs[0]), 6))
frac = 1 - 1 / (x ** sp.Rational(2, 3) + (1 - x) ** sp.Rational(2, 3))
print('    share of the two surfaces destroyed, largest at x = 1/2:', sp.nsimplify(frac.subs(x, sp.Rational(1, 2))), '=', sp.N(frac.subs(x, sp.Rational(1, 2)), 6))
print('    check: d^2/dx^2 of the bracket at 1/2 =', sp.N(sp.diff(g, x, 2).subs(x, sp.Rational(1, 2)), 6), '(> 0: a minimum of the bracket, the deepest drop)')

# (c) released area of a large drop R eating a small one r = pR, over the small drop's surface: 1 - (2/3) p + p^4/9 + ...
rel = (R ** 2 + (p * R) ** 2 - (R ** 3 + (p * R) ** 3) ** sp.Rational(2, 3)) / (p * R) ** 2
print('(c) released / small surface =', sp.series(sp.simplify(rel), p, 0, 6))
print('    at p = 0.2 (40 on 8 um):', sp.N(rel.subs(p, sp.Rational(1, 5)), 6))

# (d) the two-bin deposit (5.3) lowers sum m^(2/3) at least as much as the exact product: Jensen for the concave m^(2/3)
xk, f = sp.symbols('x_k f', positive=True)
q = sp.symbols('q', positive=True)      # x_{k+1} = q x_k, q = 2^(1/s)
xstar = (1 - f) * xk + f * q * xk         # the lever rule keeps the mass: (1-f) x_k + f x_{k+1} = x*
gap = (1 - f) * xk ** sp.Rational(2, 3) + f * (q * xk) ** sp.Rational(2, 3) - xstar ** sp.Rational(2, 3)
gap_s = sp.simplify(gap / xk ** sp.Rational(2, 3))
print('(d) deposit surface minus product surface, over x_k^(2/3):', gap_s)
num = [sp.N(gap_s.subs({q: 2 ** sp.Rational(1, 8), f: fv}), 4) for fv in (sp.Rational(1, 10), sp.Rational(1, 2), sp.Rational(9, 10))]
print('    at s = 8 (q = 2^(1/8)), f = 0.1, 0.5, 0.9:', num, '(all <= 0: Jensen)')
ser = sp.series(gap_s.subs(q, 1 + sp.Symbol('d')), sp.Symbol('d'), 0, 3).removeO()
print('    small bin width d = q - 1:', sp.factor(sp.simplify(ser)), '(second order in the bin width)')

# (e) constant kernel K: n = (N^2/M) exp(-N m/M) with N(t) = N0/(1 + K N0 t/2) solves (5.1) exactly
t, K, N0, M = sp.symbols('t K N_0 M', positive=True)
N = N0 / (1 + K * N0 * t / 2)
n = lambda mm: N ** 2 / M * sp.exp(-N * mm / M)
gain = K / 2 * sp.integrate(n(mp) * n(m - mp), (mp, 0, m))
loss = K * n(m) * sp.integrate(n(mp), (mp, 0, sp.oo))
print('(e) constant kernel: d n/dt - gain + loss =', sp.simplify(sp.diff(n(m), t) - gain + loss))
print('    number', sp.simplify(sp.integrate(n(m), (m, 0, sp.oo)) - N), ', water', sp.simplify(sp.integrate(m * n(m), (m, 0, sp.oo)) - M), '(zero: N(t) and M exact)')

# (f) maximum entropy: maximise H = -int n ln(n/w) dm at fixed N and M (w the prior): n = w exp(-1 - a - b m)
a, b = sp.symbols('alpha beta', positive=True)
nn = sp.Function('n')(m)
w = sp.symbols('w', positive=True)
Lag = -nn * sp.log(nn / w) - a * nn - b * m * nn
sol = sp.solve(sp.diff(Lag, nn), nn)
print('(f) stationary n(m) =', sol, '-> with uniform prior in mass, fixing N and M:')
nme = N0 ** 2 / M * sp.exp(-N0 * m / M)
print('    n = (N^2/M) exp(-N m/M): number', sp.simplify(sp.integrate(nme, (m, 0, sp.oo))), ', water', sp.simplify(sp.integrate(m * nme, (m, 0, sp.oo))))
print('    second variation -1/n < 0: a maximum. The same function as (e): the constant kernel drives the cloud to the maximum-entropy shape.')
# uniform prior in radius instead: n(r) dr = C exp(-b m(r)) dr  ->  n(m) = C exp(-b m) dr/dm, a gamma of shape 1/3 in mass
drdm = sp.diff(rad, m)
print('    prior uniform in radius instead: n(m) proportional to exp(-b m) *', sp.simplify(drdm), ' i.e. m^(-2/3) exp(-b m): another shape')
# gamma family from a third constraint on <ln m>: n = C m^(nu-1) exp(-lam m); nu from psi(nu) - ln(nu) = <ln m> - ln(M/N)
nu, lam = sp.symbols('nu lambda', positive=True)
gam = m ** (nu - 1) * sp.exp(-lam * m)
Z = sp.integrate(gam, (m, 0, sp.oo), conds='none')
mean = sp.simplify(sp.integrate(m * gam, (m, 0, sp.oo), conds='none') / Z)
print('    gamma n ~ m^(nu-1) exp(-lam m): mean mass', mean, '; <ln m> = digamma(nu) - ln(lam)')

# (g) the energy-only Monte Carlo: Metropolis with uniform pair proposals; every merger has dE < 0 (b), so it is always accepted,
#     every split has dE/kT ~ +1e10 (derive/L8_energy.cjs), so never: each step merges a uniformly chosen pair, which is the jump
#     chain of the coalescence process with a constant kernel; its large-volume limit is (e) in the step clock N(steps)/N0.
print('(g) Metropolis, uniform pairs: accept min(1, exp(-dE/kT)) = 1 for every merger -> constant-kernel coalescence (clock = steps)')
