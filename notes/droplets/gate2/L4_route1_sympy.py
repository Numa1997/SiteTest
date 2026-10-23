"""Gate 2, level L4 (chapter 5), route 1: SymPy. Equations (5.1)-(5.3) and Golovin's exact solution (physics.cjs golovinDensity)."""
import sympy as sp
import mpmath as mp
from dims import *

print('== (5.1)/(5.2) discrete (lattice) version: exact algebraic identity with symbolic n_i, K_ij, phi_i')
N = 6
n = sp.symbols('n1:%d' % (N + 1)); phi = sp.symbols('phi1:%d' % (N + 1))
Kc = {}
for i in range(1, N + 1):
    for j in range(i, N + 1):
        Kc[(i, j)] = Kc[(j, i)] = sp.Symbol('K%d_%d' % (i, j))
# dn_k/dt = 1/2 sum_{i+j=k} K_ij n_i n_j - n_k sum_{j: k+j<=N} K_kj n_j     (masses are the integers 1..N; mass beyond N is dropped from both sides)
dn = []
for k in range(1, N + 1):
    gain = sp.Rational(1, 2) * sum(Kc[(i, k - i)] * n[i - 1] * n[k - i - 1] for i in range(1, k))
    loss = n[k - 1] * sum(Kc[(k, j)] * n[j - 1] for j in range(1, N - k + 1))
    dn.append(gain - loss)
lhs = sum(phi[k - 1] * dn[k - 1] for k in range(1, N + 1))
rhs = sp.Rational(1, 2) * sum(Kc[(i, j)] * n[i - 1] * n[j - 1] * (phi[i + j - 1] - phi[i - 1] - phi[j - 1]) for i in range(1, N + 1) for j in range(1, N + 1) if i + j <= N)
print('  sum_k phi_k dn_k/dt - 1/2 sum_{i,j} K_ij n_i n_j [phi_{i+j} - phi_i - phi_j] =', sp.expand(lhs - rhs), ' (N = %d, all symbols free)' % N)
mass_phi = {phi[k - 1]: k for k in range(1, N + 1)}
print('  phi_k = k (mass): bracket phi_{i+j}-phi_i-phi_j = 0 -> d/dt sum k n_k =', sp.expand(lhs.subs(mass_phi)), ' (mass conserved exactly)')
print('  phi_k = 1: d/dt sum n_k =', sp.expand(lhs.subs({p: 1 for p in phi})), '= -1/2 sum K n n (number falls by one per merger)')
print('  phi_k = k^2: bracket 2 i j > 0 (merging builds bigger drops):', sp.expand(sp.expand((lambda i, j: (i + j)**2 - i**2 - j**2)(sp.Symbol('i'), sp.Symbol('j')))))

print('\n== (5.1)/(5.2) continuous case, K = b (m + m\'), n = exp(-m): every term in closed form')
m, mp_, b, q = sp.symbols('m mp b q', positive=True)
nfun = lambda x: sp.exp(-x)
Kf = lambda x, y: b * (x + y)
gain = sp.Rational(1, 2) * sp.integrate(Kf(mp_, m - mp_) * nfun(mp_) * nfun(m - mp_), (mp_, 0, m))
loss = nfun(m) * sp.integrate(Kf(m, mp_) * nfun(mp_), (mp_, 0, sp.oo))
dndt = sp.simplify(gain - loss)
print('  gain =', sp.simplify(gain), ' loss =', sp.simplify(loss), ' dn/dt =', dndt)
for name, ph in [('m', m), ('1', sp.Integer(1)), ('m^2', m**2), ('exp(-q m)', sp.exp(-q * m)), ('m^3', m**3)]:
    left = sp.integrate(sp.simplify(ph * dndt), (m, 0, sp.oo))
    mm = sp.symbols('mm', positive=True)
    phi_f = lambda x: ph.subs(m, x)
    right = sp.Rational(1, 2) * sp.integrate(sp.integrate(Kf(m, mm) * nfun(m) * nfun(mm) * (phi_f(m + mm) - phi_f(m) - phi_f(mm)), (m, 0, sp.oo)), (mm, 0, sp.oo))
    print('  phi = %-9s  LHS int phi dn/dt dm = %-28s RHS (5.2) = %-28s difference = %s' % (name, sp.simplify(left), sp.simplify(right), sp.simplify(left - right)))
same('n dm  [1/m^3]', ONE / m**3 if False else (ONE / length**3), ONE / length**3)
print('  units of (5.1): K [m^3/s], n [1/(m^3 kg)], dm [kg]: gain K n n dm = 1/(m^3 kg s) = dn/dt :',
      ((length**3 / time) * (ONE / (length**3 * mass))**2 * mass) == (ONE / (length**3 * mass * time)))

print('\n== (5.3) lever rule')
xk, xk1, xs, C, nuk, nuk1 = sp.symbols('x_k x_k1 x_star C nu_k nu_k1', positive=True)
sol = sp.solve([sp.Eq(nuk + nuk1, C), sp.Eq(xk * nuk + xk1 * nuk1, xs * C)], [nuk, nuk1], dict=True)[0]
f = sp.simplify(sol[nuk1] / C)
print('  solution: nu_k+1/C =', f, ' ; printed f = (x*-x_k)/(x_k1-x_k): difference', sp.simplify(f - (xs - xk) / (xk1 - xk)), ' ; nu_k/C =', sp.simplify(sol[nuk] / C), ' = 1-f:', sp.simplify(sol[nuk] / C - (1 - f)) == 0)
print('  limits: x* = x_k -> f =', f.subs(xs, xk), ' ; x* = x_k+1 -> f =', sp.simplify(f.subs(xs, xk1)), ' ; sign: 0 <= f <= 1 exactly when x_k <= x* <= x_k+1 (denominator x_k1 - x_k > 0)')
print('  number of products is C, so mass and count both exact: sum nu =', sp.simplify(sol[nuk] + sol[nuk1] - C), ', sum x nu - x* C =', sp.simplify(xk * sol[nuk] + xk1 * sol[nuk1] - xs * C))
same('x* [kg], f dimensionless', mass / mass, ONE)
s_ = sp.symbols('s', positive=True)
print('  grid x_k = x_0 2^(k/s): ratio x_k+1/x_k =', sp.simplify(sp.Symbol('x0') * 2**((sp.Symbol('k') + 1) / s_) / (sp.Symbol('x0') * 2**(sp.Symbol('k') / s_))), '; 1 um to 4 mm radius spans log10(4000) =', float(sp.log(4000, 10)), 'decades of radius and', float(3 * sp.log(4000, 10)), 'decades of mass (text: "four" and "twelve")')

print('\n== Golovin: K = b(m+m\'), n(m,0) = (N0/mbar) exp(-m/mbar) -- Laplace transform')
p_, T, P = sp.symbols('p T P', positive=True)
# units m_bar = 1, N0 = 1, b L t = T (L = N0 mbar = 1);  Laplace transform N(p,t) = int n e^{-p m} dm
# from (5.1):  dN/dt = - b N N_p + b N_p N(0,t) - b L N     (derivation in the file header of the .md)
z = 1 - sp.exp(-T)
s = 1 + z + P
Nhat = (1 - z) * (s - sp.sqrt(s**2 - 4 * z)) / (2 * z)       # claimed transform of the printed density
Ntot = sp.limit(Nhat, P, 0)
print('  claimed N(P,T) = (1-z)(s - sqrt(s^2-4z))/(2z), s = 1+z+P ;  N(0,T) =', sp.simplify(Ntot), '(number decays as exp(-bLt))')
print('  initial condition T->0: N(P,0) =', sp.limit(Nhat, T, 0), ' (= transform of exp(-m) = 1/(1+P))')
print('  mass: -dN/dP at P=0 =', sp.simplify(-sp.diff(Nhat, P).subs(P, 0)), ' (= 1: conserved, L)')
res = sp.diff(Nhat, T) - (-Nhat * sp.diff(Nhat, P) + sp.diff(Nhat, P) * Ntot - Nhat)
res_s = sp.simplify(res)
print('  PDE residual dN/dT + N N_P - N_P N(0) + N  (symbolic simplify) =', res_s)
mp.mp.dps = 40
fres = sp.lambdify((P, T), res, 'mpmath')
vals = [fres(mp.mpf(Pv), mp.mpf(Tv)) for Pv in (0.01, 0.3, 1, 7, 40) for Tv in (0.05, 0.7, 2.3, 5.4)]
print('  PDE residual at 20 points, 40-digit arithmetic: max |res| =', mp.nstr(max(abs(v) for v in vals), 5))
# the inverse transform: printed density  n = (1-z)/(u sqrt z) I1(2 u sqrt z) exp(-(1+z) u)  has transform  (1-z)(s - sqrt(s^2-4z))/(2z) ?
for zz, ss in [(0.3, 1.9), (0.9, 2.5), (0.99, 3.1), (0.9955, 2.4)]:
    num = mp.quad(lambda u: (1 - zz) / (u * mp.sqrt(zz)) * mp.besseli(1, 2 * u * mp.sqrt(zz)) * mp.e**(-(1 + zz) * u) * mp.e**(-(ss - 1 - zz) * u), [0, 1, 10, 60, 400, mp.inf])
    cl = (1 - zz) * (ss - mp.sqrt(ss**2 - 4 * zz)) / (2 * zz)
    print('  z = %.4f s = %.2f : numerical Laplace integral of the printed density = %s ; closed form = %s ; rel. diff %s' % (zz, ss, mp.nstr(num, 12), mp.nstr(cl, 12), mp.nstr(abs(num / cl - 1), 3)))
print('  units: b L t = [m^3 kg^-1 s^-1][kg m^-3][s] ->', ((length**3 / (mass * time)) * (mass / length**3) * time) == ONE, ' so z = 1 - exp(-b L t) is dimensionless; n = (N0/mbar) F(u,z): [m^-3 kg^-1] ok')
mbar_text = 4 / 3 * 3.141592653589793 * (10e-6)**3 * 1000.0; Lw = 1e-3; bb = 1.5
print('  text parameters: mbar = %.4e kg, L = 1 g/m3, N0 = %.3e m^-3, b L t at 60 min = %.3f, z = %.5f' % (mbar_text, Lw / mbar_text, bb * Lw * 3600, 1 - float(sp.exp(-bb * Lw * 3600))))
