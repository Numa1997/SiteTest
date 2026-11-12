"""Fig. 14: SymPy and NumPy checks of every formula in the note."""
import sympy as sp, numpy as np, scipy.linalg as sl
x, t, k0, s = sp.symbols('x t k_0 sigma', positive=True)
# 1. the free Gaussian packet in 1D (hbar = m = 1): the closed form solves i psi_t = -psi_xx/2, and its width
tau = t / (2 * s**2)
psi = (2 * sp.pi * s**2) ** sp.Rational(-1, 4) * (1 + sp.I * tau) ** sp.Rational(-1, 2) * sp.exp(-(x - k0 * t)**2 / (4 * s**2 * (1 + sp.I * tau)) + sp.I * k0 * x - sp.I * k0**2 * t / 2)
res = sp.simplify(sp.I * sp.diff(psi, t) + sp.diff(psi, x, 2) / 2)
print('1. free packet solves the equation:', sp.simplify(res / psi) == 0)
rho = sp.simplify(psi * sp.conjugate(psi))
var = sp.simplify(sp.integrate((x - k0 * t)**2 * rho, (x, -sp.oo, sp.oo)) / sp.integrate(rho, (x, -sp.oo, sp.oo)))
print('   variance:', sp.factor(var), ' = sigma^2 (1 + tau^2)?', sp.simplify(var - s**2 * (1 + tau**2)) == 0)
q, al, be = sp.symbols('q alpha beta')
alpha = s**2 * (1 + sp.I * tau)
print('   Re(1/alpha) =', sp.simplify(sp.re(sp.expand_complex(1 / alpha))), ' vs 1/(sigma^2 (1+tau^2)):', sp.simplify(sp.re(sp.expand_complex(1 / alpha)) - 1 / (s**2 * (1 + tau**2))) == 0)
# 2. momentum width and mean energy
k = sp.symbols('k', real=True)
phi2 = sp.exp(-2 * s**2 * (k - k0)**2)
mk2 = sp.simplify(sp.integrate(k**2 * phi2, (k, -sp.oo, sp.oo)) / sp.integrate(phi2, (k, -sp.oo, sp.oo)))
print('2. <k^2> along x =', sp.expand(mk2), '; across: 1/(4 sigma^2) each; <E> = k0^2/2 + 3/(8 sigma^2) =', 2.5 + 3 / 72)
# 3. the rectangular barrier of thickness a: match at x = 0 and x = a
E, V0, a = sp.symbols('E V_0 a', positive=True)
kk, ka = sp.sqrt(2 * E), sp.sqrt(2 * (V0 - E))
r, C, D, tt = sp.symbols('r C D t')
eqs = [sp.Eq(1 + r, C + D), sp.Eq(sp.I * kk * (1 - r), ka * (C - D)),
       sp.Eq(C * sp.exp(ka * a) + D * sp.exp(-ka * a), tt * sp.exp(sp.I * kk * a)),
       sp.Eq(ka * (C * sp.exp(ka * a) - D * sp.exp(-ka * a)), sp.I * kk * tt * sp.exp(sp.I * kk * a))]
sol = sp.solve(eqs, [r, C, D, tt], dict=True)[0]
T = sp.simplify(sp.Abs(sol[tt])**2)
Tf = 1 / (1 + V0**2 * sp.sinh(ka * a)**2 / (4 * E * (V0 - E)))
for (e, v, aa) in [(2.5, 3, 8), (2.5, 3, 4), (1.0, 3.0, 2.0), (2.0, 3.0, 8.0)]:
    num = complex(sol[tt].subs({E: e, V0: v, a: aa}).evalf()); print('3. E=%g V0=%g a=%g |t|^2 = %.6e  formula %.6e' % (e, v, aa, abs(num)**2, float(Tf.subs({E: e, V0: v, a: aa}))))
# over the barrier: the sin^2 branch, checked by a direct linear solve with a real wave number inside
def Tnum(e, v, aa):
    k1 = np.sqrt(2 * e); q = np.sqrt(complex(2 * (e - v)))   # inside: exp(+-i q x)
    M = np.array([[1, -1, -1, 0], [-1j * k1, -1j * q, 1j * q, 0], [0, np.exp(1j * q * aa), np.exp(-1j * q * aa), -np.exp(1j * k1 * aa)],
                  [0, 1j * q * np.exp(1j * q * aa), -1j * q * np.exp(-1j * q * aa), -1j * k1 * np.exp(1j * k1 * aa)]], complex)
    rhs = np.array([-1, -1j * k1, 0, 0], complex); return abs(np.linalg.solve(M, rhs)[3])**2
def Tpage(E_, V, a_):   # the page's T1D, copied
    if V == 0: return 1
    if abs(E_ - V) < 1e-9: return 1 / (1 + a_ * a_ * V / 2)
    if E_ < V: k_ = np.sqrt(2 * (V - E_)); s_ = np.sinh(k_ * a_); return 1 / (1 + V * V * s_ * s_ / (4 * E_ * (V - E_)))
    k2 = np.sqrt(2 * (E_ - V)); s2 = np.sin(k2 * a_); return 1 / (1 + V * V * s2 * s2 / (4 * E_ * (E_ - V)))
for (e, v, aa) in [(2.5, 3, 8), (4.5, 4, 4), (4.0, 3.0, 8.0), (2.5, 0.5, 8), (1.0, 1.0, 8.0)]:
    print('   direct solve E=%g V0=%g a=%g: %.6e   page T1D %.6e' % (e, v, aa, Tnum(e if e != v else e + 1e-9, v, aa), Tpage(e, v, aa)))
Es = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]; Vs = [0, 0.5, 1, 1.5, 2, 3, 4, 6, 8]; Rs = [2, 3, 4, 5, 6]
best = max(((Tpage(e, v, 2 * R), e, v, R) for e in Es for v in Vs for R in Rs if e < v))
print('   largest T1D with E < V0 on the grid: %.3e at E=%g V0=%g R=%g' % best)
# 4. Strang splitting: log(e^{A/2} e^B e^{A/2}) = A + B - [A,[A,B]]/24 - [B,[A,B]]/12 + O(5), checked with matrices
rng = np.random.default_rng(1)
def herm(n): m = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); return (m + m.conj().T) / 2
Vm, Tm = np.diag(rng.normal(size=6)), herm(6)
cm = lambda X, Y: X @ Y - Y @ X
print('4. Strang: dt, ||S - exp(-iH dt)||, ratio to the BCH prediction, ||log S - (-iH dt)|| / dt^3')
for dt in [0.2, 0.1, 0.05, 0.025]:
    A, B = -1j * Vm * dt, -1j * Tm * dt
    S = sl.expm(A / 2) @ sl.expm(B) @ sl.expm(A / 2); ex = sl.expm(A + B)
    pred = -cm(A, cm(A, B)) / 24 - cm(B, cm(A, B)) / 12
    Lg = sl.logm(S); err = np.linalg.norm(Lg - (A + B) - pred) / np.linalg.norm(pred)
    Heff_extra = (dt**2 / 24) * (cm(Vm, cm(Vm, Tm)) + 2 * cm(Tm, cm(Vm, Tm)))
    print('   %.3f  %.3e  rel. rest after BCH %.2e  Heff check %.2e  hermitian %s' % (dt, np.linalg.norm(S - ex), err,
          np.linalg.norm((1j / dt) * Lg - (Vm + Tm + Heff_extra)) / np.linalg.norm(Heff_extra), np.allclose(S.conj().T @ S, np.eye(6))))
# 5. [V,[V,T]] = -|grad V|^2 for T = -lap/2 (1D symbolic)
f = sp.Function('f'); Vx = sp.Function('V')
Top = lambda g: -sp.diff(g, x, 2) / 2
c1 = lambda g: Vx(x) * Top(g) - Top(Vx(x) * g)
c2 = sp.simplify(Vx(x) * c1(f(x)) - c1(Vx(x) * f(x)))
print('5. [V,[V,T]] f =', c2)
# 6. numbers
for e in [0.5, 2.0, 2.5, 4.5]:
    k = np.sqrt(2 * e); print('6. E=%g k0=%.4f lambda=%.4f a, v=%.4f, t_end(30 a)=%.2f, k0*sigma0=%.2f, k0 R(4)=%.2f' % (e, k, 2 * np.pi / k, k, 30 / k, 3 * k, 4 * k))
for (e, v) in [(2.5, 3), (2, 3), (0.5, 8), (4.5, 6)]:
    print('   E=%g V0=%g kappa=%.4f, 1/kappa=%.4f a, e^{-2 kappa 8}=%.2e' % (e, v, np.sqrt(2 * (v - e)), 1 / np.sqrt(2 * (v - e)), np.exp(-2 * np.sqrt(2 * (v - e)) * 8)))
print('   transverse fraction aimed at a disc of radius R: 1 - exp(-R^2/(2 sigma0^2)):', {R: round(1 - np.exp(-R**2 / 18), 4) for R in Rs})
# electron units for a = 0.1 nm
hbar, me, eV = 1.054571817e-34, 9.1093837015e-31, 1.602176634e-19
aa = 1e-10; Eu = hbar**2 / (me * aa**2); tu = me * aa**2 / hbar
print('7. electron, a = 0.1 nm: energy unit %.4f eV, time unit %.4e s, speed unit %.4e m/s' % (Eu / eV, tu, aa / tu))
print('   free spreading time 2 sigma0^2 = 18 time units = %.3e s' % (18 * tu))
