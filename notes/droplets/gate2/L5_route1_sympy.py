"""Gate 2, level L5 (chapter 6), route 1: SymPy. Equation (6.1), the Poisson argument, Gillespie's waiting time and the thinning statement (6.2)."""
import sympy as sp
from dims import *
k, N, mu, V, n, t, lam, p_, s = sp.symbols('k N mu V n t lambda p s', positive=True)
kk = sp.symbols('kk', integer=True, nonnegative=True)

print('== (6.1)  P(no drop of 100 um in V by t) = exp(-V n100), median V n100 = ln 2')
print('  rare, independent drops: N candidates in the volume, each above 100 um with probability mu/N (mu = V n100 = expected number)')
pbin = sp.binomial(N, kk) * (mu / N)**kk * (1 - mu / N)**(N - kk)
for kv in range(4):
    lim = sp.limit(pbin.subs(kk, kv), N, sp.oo)
    print('   k = %d : limit N->oo of binomial pmf = %s ; Poisson pmf exp(-mu) mu^k/k! = %s ; difference %s' % (kv, sp.simplify(lim), sp.exp(-mu) * mu**kv / sp.factorial(kv), sp.simplify(lim - sp.exp(-mu) * mu**kv / sp.factorial(kv))))
P0 = sp.exp(-mu)
print('  P(no drop) = exp(-mu); mean = var = mu:', sp.simplify(sum(kv * sp.exp(-mu) * mu**kv / sp.factorial(kv) for kv in range(0, 60)).subs(mu, 3).evalf(12)), '(mu = 3 test of the mean)')
print('  median: exp(-mu) = 1/2 ->', sp.solve(sp.Eq(sp.exp(-mu), sp.Rational(1, 2)), mu), '= ln 2 =', sp.N(sp.log(2), 8))
print('  limits: V -> 0 or n100 -> 0: P -> 1 ; V n100 -> oo: P -> 0 ; for V n100 << 1, 1 - P = V n100 (first-order expansion):', sp.series(1 - P0, mu, 0, 3))
same('V n100', length**3 * (ONE / length**3), ONE)
print('  statement used: n100 in the mean field is the Poisson mean at time t. ln 2 = 0.693: volume 100 cm3 = 1e-4 m3 needs n100 = ln2/V =', sp.N(sp.log(2) / sp.Rational(1, 10000), 5), 'm^-3 ; 1000 cm3:', sp.N(sp.log(2) / sp.Rational(1, 1000), 5), 'm^-3 ; 1 m3:', sp.N(sp.log(2), 5), 'm^-3')

print('\n== Gillespie waiting time tau = -ln(u1)/a0')
a0, u1, tau = sp.symbols('a0 u1 tau', positive=True)
# survival P(waiting time > tau) = exp(-a0 tau) (rate a0, memoryless); inverse transform: u = exp(-a0 tau)
print('  solve u = exp(-a0 tau) for tau:', sp.solve(sp.Eq(u1, sp.exp(-a0 * tau)), tau), '; u1 uniform on (0,1] so 1-u1 is too: -ln(u1)/a0 has survival', sp.simplify(sp.exp(-a0 * tau)))
print('  mean waiting time = int_0^oo tau a0 exp(-a0 tau) dtau =', sp.integrate(tau * a0 * sp.exp(-a0 * tau), (tau, 0, sp.oo)), ' (= 1/a0)')
same('tau = ln(u)/a0 with a0 in 1/s', ONE / (ONE / time), time)

print('\n== thinning (6.2): a Poisson stream of rate lam*, each point kept with probability q = K/K*, is Poisson with rate lam* q')
lam_s, q_, tt, z_ = sp.symbols('lam_star q t z', positive=True)
M = lam_s * tt
# generating function of kept count: sum_n Poisson(n; M) (1 - q + q z)^n
pgf = sp.simplify(sp.summation(sp.exp(-M) * M**kk / sp.factorial(kk) * (1 - q_ + q_ * z_)**kk, (kk, 0, sp.oo)))
print('  PGF of kept count =', pgf, '; PGF of Poisson(q lam* t) =', sp.exp(M * q_ * (z_ - 1)), '; difference:', sp.simplify(pgf - sp.exp(M * q_ * (z_ - 1))))
print('  counts in disjoint intervals stay independent (independent marks): the thinned process is Poisson with rate lam* q = lam* K/K*')
print('\n  per-pair rate bookkeeping of the class scheme (V = volume):')
Ks, Kij, Va, na, nb = sp.symbols('Kstar K_ij V n_a n_b', positive=True)
# different classes a != b: proposals at K* n_a n_b / V ; pair chosen uniformly among n_a n_b ; accepted with K_ij/K*
print('   a != b : K* n_a n_b/V * 1/(n_a n_b) * K_ij/K* =', sp.simplify(Ks * na * nb / Va / (na * nb) * Kij / Ks), ' (= K_ij/V)')
# same class: proposals at K* n_a^2/(2V); an ordered pair (i, j) uniform among n_a^2; i = j rejected; unordered pair {i,j} has probability 2/n_a^2
print('   a = b  : K* n_a^2/(2V) * 2/n_a^2 * K_ij/K* =', sp.simplify(Ks * na**2 / (2 * Va) * 2 / na**2 * Kij / Ks), ' ; total accepted-eligible proposals rate K* n_a^2/(2V) * (n_a-1)/n_a =', sp.simplify(Ks * na**2 / (2 * Va) * (na - 1) / na), '= K* n_a (n_a-1)/(2V) = (K*/V) x number of pairs')
print('  Gillespie method: the process is a continuous-time Markov chain with total rate a0 = sum over pairs K_ij/V; the next event is after Exp(a0) and is pair (i,j) with probability (K_ij/V)/a0 (competing exponential clocks): choosing a class pair with probability K* n_a n_b/(V A*) and a member pair uniformly then accepting with K/K* gives exactly (K_ij/V)/a0 among accepted proposals')
