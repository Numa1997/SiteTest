"""Gate 2, level L4 (chapter 5), route 2 (numerical, SciPy): (a) Golovin's solution substituted into the SCE (5.1) by quadrature, (b) (5.2) vs (5.1) for a
non-polynomial kernel by nested quadrature, (c) lever rule as a numerical statement on random bins, (d) first moments of the printed Golovin density.
The density used in (a) is coded here with scipy.special.ive; the model's golovinDensity (physics.cjs) is compared against it."""
import json, numpy as np
from scipy.integrate import quad, dblquad
from scipy.special import ive
rng = np.random.default_rng(11)
D = json.load(open('L4_golovin_dump.json'))

def n_gol(u, T):    # units: mbar = N0 = b = 1 ; z = 1 - exp(-T)
    z = 1 - np.exp(-T)
    if z < 1e-14: return np.exp(-u)
    a = 2 * u * np.sqrt(z)
    return (1 - z) / (u * np.sqrt(z)) * ive(1, a) * np.exp(a - (1 + z) * u)
print('== model golovinDensity against scipy.special.ive implementation (units mbar = N0 = b = 1)')
rel = [abs(r['n'] / n_gol(r['u'], r['T']) - 1) for r in D['unit']]
print('   28 points: max relative difference %.2e (A&S 9.8.3/9.8.4 polynomial for I1 is good to about 1e-7)' % max(rel))
relb = [abs(r['v'] / ive(1, r['x']) - 1) for r in D['besselI1e']]
print('   besselI1e at 10 arguments: max relative difference %.2e' % max(relb))

print('== (a) Golovin density substituted into (5.1): dn/dt by central difference in t vs gain - loss by quadrature (K = m + m\', b = 1)')
def qinf(f, T, lo=0.0):
    z = 1 - np.exp(-T); umax = 60.0 / max((1 - np.sqrt(z))**2, 1e-12) if z > 0 else 60.0
    edges = [lo] + [e for e in np.geomspace(1e-2, umax, 40) if e > lo]
    return sum(quad(f, a, b, epsabs=0, epsrel=1e-11, limit=400)[0] for a, b in zip(edges[:-1], edges[1:]))
def rhs51(u, T):
    gain = 0.5 * quad(lambda x: (x + (u - x)) * n_gol(x, T) * n_gol(u - x, T), 0, u, epsabs=0, epsrel=1e-11, limit=400)[0]
    loss = n_gol(u, T) * qinf(lambda x: (u + x) * n_gol(x, T), T)
    return gain - loss
worst = 0
for T in [0.3, 1.0, 2.0, 5.4]:
    for u in [0.2, 1.0, 3.0, 8.0]:
        h = 1e-4 * T
        lhs = (n_gol(u, T + h) - n_gol(u, T - h)) / (2 * h)
        r_ = rhs51(u, T)
        rel_ = abs(lhs - r_) / max(abs(lhs), abs(r_), 1e-300)
        worst = max(worst, rel_ if max(abs(lhs), abs(r_)) > 1e-12 else 0)
        print('   T = %.1f u = %4.1f : dn/dT = % .8e ; gain - loss = % .8e ; rel diff %.1e' % (T, u, lhs, r_, rel_))
print('   worst relative residual: %.1e (finite-difference limited, h = 1e-4 T)' % worst)
print('   initial condition n(u,0) = exp(-u):', max(abs(n_gol(u, 0.0) - np.exp(-u)) for u in [0.1, 1, 5]))
print('   moments of the printed density: number/exp(-T) = %s ; mass = %s (should be 1)' % ([float('%.9f' % (qinf(lambda x: n_gol(x, T), T) / np.exp(-T))) for T in (0.3, 2.0, 5.4)], [float('%.9f' % qinf(lambda x: x * n_gol(x, T), T)) for T in (0.3, 2.0, 5.4)]))
print('   SI parameters of the text (b = 1.5, mean radius 10 um, 1 g/m3): model density at 3 times vs the unit-scaled formula n = (N0/mbar) n_gol(u, bLt):')
L = D['N0'] * D['mbar']; b = 1.5
for r in D['si']:
    u = (4 / 3 * np.pi * 1000 * (r['rum'] * 1e-6)**3) / D['mbar']; T = b * L * r['t']
    mine = D['N0'] / D['mbar'] * n_gol(u, T)
    print('      t = %4d s r = %3d um : model %.6e ; own %.6e ; rel diff %.1e' % (r['t'], r['rum'], r['n'], mine, abs(r['n'] / mine - 1) if mine > 0 else 0)) if r['rum'] in (10, 40) else None

print('== (b) (5.2) against (5.1) for a physical-shaped kernel K = (m^(1/3)+m\'^(1/3))^2 |m^(2/3)-m\'^(2/3)| and n = exp(-m), phi = m, 1, m^2, sin(m)')
Kf = lambda x, y: (x**(1 / 3) + y**(1 / 3))**2 * abs(x**(2 / 3) - y**(2 / 3))
nn = lambda x: np.exp(-x)
def dndt(x):
    gain = 0.5 * quad(lambda y: Kf(y, x - y) * nn(y) * nn(x - y), 0, x, epsabs=1e-14, epsrel=1e-12, limit=400, points=[x / 2])[0]
    loss = nn(x) * quad(lambda y: Kf(x, y) * nn(y), 0, 90, epsabs=1e-14, epsrel=1e-12, limit=400, points=[x])[0]
    return gain - loss
for name, ph in [('m', lambda x: x), ('1', lambda x: 1.0), ('m^2', lambda x: x * x), ('sin m', np.sin)]:
    left = quad(lambda x: ph(x) * dndt(x), 0, 60, epsabs=1e-13, epsrel=1e-10, limit=400)[0]
    right = 0.5 * dblquad(lambda y, x: Kf(x, y) * nn(x) * nn(y) * (ph(x + y) - ph(x) - ph(y)), 0, 60, 0, 60, epsabs=1e-12, epsrel=1e-9)[0]
    print('   phi = %-6s  int phi dn/dt dm = % .10e ; (5.2) right side = % .10e ; diff % .1e' % (name, left, right, left - right))

print('== (c) lever rule (5.3): random bins and random product masses, number and mass of the deposit')
bad = 0
for _ in range(100000):
    xk = rng.uniform(0.1, 10); xk1 = xk * 2**(1 / 8); xs = rng.uniform(xk, xk1); C = rng.uniform(0.1, 7)
    f = (xs - xk) / (xk1 - xk); nu1 = f * C; nu0 = (1 - f) * C
    bad = max(bad, abs(nu0 + nu1 - C) / C, abs(xk * nu0 + xk1 * nu1 - xs * C) / (xs * C), 0 if (nu0 >= 0 and nu1 >= 0) else 1)
print('   max violation over 1e5 random cases (number, mass, non-negativity): %.1e' % bad)
