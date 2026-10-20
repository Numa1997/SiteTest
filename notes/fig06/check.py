# Fig. 6 note: checks of the numbers in the note, with the page's own formulas and preset values.
# Run: python3 notes/fig06/check.py
import numpy as np, sympy as sp

out = {}
# --- Section 3: the two-wave derivative step and the cancelling headphone ---
X, t, A, k, w, phi = sp.symbols('X t A k omega phi', real=True)
y = A*sp.sin(k*X - w*t + phi)
out['d2y/dt2 / y'] = sp.simplify(sp.diff(y, t, 2)/y)          # -> -omega**2
out['d2y/dX2 / y'] = sp.simplify(sp.diff(y, X, 2)/y)          # -> -k**2
out['d/dt y'] = sp.diff(y, t)                                  # -> -A omega cos(...)
C = 20*np.sqrt(2*(1+np.cos(3.15)))
out['phase 3.15 rad: miss'] = 3.15 - np.pi
out['phase 3.15 rad: C (px)'] = C

# --- Section 4.1: envelope and carrier speeds, Exercise 4.1 ---
def venv(f1, s1, f2, s2): return 200*(f1*s1 - f2*s2)/(f1 - f2)
def vcar(f1, s1, f2, s2): return 200*(f1*s1 + f2*s2)/(f1 + f2)
out['Ex4.1 v_env (px/s)'] = venv(1, 1, 1.25, 0.5)
out['Ex4.1 v_carrier (px/s)'] = vcar(1, 1, 1.25, 0.5)
# deep water: v_g / v_p
g_, kk = sp.symbols('g k', positive=True)
om = sp.sqrt(g_*kk)
out['deep water v_g/v_p'] = sp.simplify(sp.diff(om, kk)/(om/kk))

# --- Section 5: Gibbs table, partial sums of (11) on a 0.01 px grid over one wavelength ---
Xg = np.arange(0, 500 + 1e-9, 0.01)
x = 2*np.pi*0.4*Xg/200
H = np.pi/4*30
def peak(amps, ns):
    S = np.zeros_like(x)
    for a, n in zip(amps, ns): S += a*np.sin(n*x)
    return S.max()
rows = []
for N, label in [(1, '1'), (3, '3 (no Wave 4)'), (4, '4 (preset)'), (10, '10'), (100, '100')]:
    ns = list(range(1, 2*N, 2))
    amps = [round(30/n*10)/10 for n in ns] if N in (3, 4) else [30/n for n in ns]
    p = peak(amps, ns)
    rows.append((label, ns[-1], round(p, 2), round(100*(p - H)/(2*H), 2)))
Si = sp.Si(sp.pi).evalf(10)
lim = 2/sp.pi*Si
rows.append(('limit (16)', '-', round(float(lim*H), 2), round(float(100*(lim - 1)/2), 2)))
out['Gibbs table'] = rows
out['(16) limit'] = float(lim)
out['overshoot px above plateau'] = float((lim - 1)*H)
out['one term above plateau (%)'] = 100*(30/H - 1)

# --- Section 6: Parseval and Exercise 6.1 ---
A4 = [30, 10, 6, 4.3]
out['Parseval (px^2)'] = 0.5*sum(a*a for a in A4)
out['H^2 (px^2)'] = H*H
out['ratio'] = 0.5*sum(a*a for a in A4)/H**2
xx = np.linspace(0, 2*np.pi, 2_000_001)
S4 = sum(a*np.sin(n*xx) for a, n in zip(A4, [1, 3, 5, 7]))
S4p = 30*np.sin(xx) + 10*np.sin(3*xx + 3.15) + 6*np.sin(5*xx) + 4.3*np.sin(7*xx)
out['Ex6.1 peak preset'] = S4.max()
out['Ex6.1 peak, Wave 2 phase 3.15'] = np.abs(S4p).max()
out['sum of amplitudes'] = sum(A4)

# --- Section 6: the string-energy step (the edit) ---
mu, T, v = sp.symbols('mu T v', positive=True)
yy = A*sp.sin(k*X - w*t)
e = sp.Rational(1, 2)*mu*sp.diff(yy, t)**2 + sp.Rational(1, 2)*T*sp.diff(yy, X)**2
# average over one period in t at fixed X (the same as over one wavelength), with T = mu v^2 and v = w/k
eavg = sp.integrate(e.subs(T, mu*(w/k)**2), (t, 0, 2*sp.pi/w))*w/(2*sp.pi)
out['mean energy per length, one component'] = sp.simplify(eavg)   # -> A^2 mu omega^2 / 2
kin = sp.integrate((sp.Rational(1, 2)*mu*sp.diff(yy, t)**2), (t, 0, 2*sp.pi/w))*w/(2*sp.pi)
pot = sp.integrate((sp.Rational(1, 2)*mu*(w/k)**2*sp.diff(yy, X)**2), (t, 0, 2*sp.pi/w))*w/(2*sp.pi)
out['kinetic = stretching on average'] = sp.simplify(kin - pot) == 0
# the square preset on such a string: share of energy in each harmonic, with omega_n proportional to n
En = [a*a*n*n for a, n in zip(A4, [1, 3, 5, 7])]
out['energy shares n=1,3,5,7 (relative to n=1)'] = [round(x_/En[0], 3) for x_ in En]

# --- Section 7: chord error A k^2 dX^2 / 8, shortest wave f = 3, A = 40 ---
kk3 = 2*np.pi*3/200
for M in (712, 298):
    dX = 800/M
    out[f'chord gap M={M} (px)'] = 40*kk3**2*dX**2/8
    out[f'samples per shortest wavelength M={M}'] = (200/3)/dX
out['sine calls, square preset, M=712'] = 3*4*713

for kk_, vv in out.items(): print(f'{kk_}: {vv}')
