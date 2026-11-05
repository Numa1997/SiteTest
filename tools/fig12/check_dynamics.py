"""Gate: the page's RK4 (h = 1 ms) against SciPy DOP853 (rtol 1e-11) on the same modal equations (12), for a scripted shake.
Usage: python3 tools/fig12/check_dynamics.py <dump.json from notes/fig12/gate.cjs> ; prints PASS/FAIL with the largest difference."""
import json, sys, math, numpy as np
from scipy.integrate import solve_ivp
d = json.load(open(sys.argv[1])); g = 9.81; NK = d['NK']; lam, Q, gam, muf, m = map(np.array, (d['lam'], d['Q'], d['gam'], d['muf'], d['m']))
A, f, sig, rho = d['A'], d['f'], d['sig'], d['rho']; W = 2 * math.pi * f; tau = 0.3
def sacc(t):   # same eased-in shaker as the page, re-typed from the note, not read from the page's code
    e = math.exp(-t / tau); w = 1 - e; wd = e / tau; wdd = -e / tau ** 2
    return A * (wdd * math.sin(W * t) + 2 * wd * W * math.cos(W * t) - w * W * W * math.sin(W * t))
def rhs(t, y):
    a = y[:2 * NK]; v = y[2 * NK:]; s = sacc(t); AX = s if d['shake'] == 'x' else 0.0; AZ = s if d['shake'] == 'z' else 0.0
    O2 = (lam * (g + AZ) + sig * lam ** 3 / rho) / (1 + muf); F = np.where(m == 1, -lam * Q * AX / (1 + muf), 0.0)
    dv = np.empty(2 * NK); dv[:NK] = -2 * gam * v[:NK] - O2 * a[:NK] + F
    dv[NK:] = np.where(m == 0, 0.0, -2 * gam * v[NK:] - O2 * a[NK:])
    da = v.copy(); da[NK:][m == 0] = 0.0
    return np.r_[da, dv]
y0 = np.r_[d['a0'], np.zeros(2 * NK)]
ts = np.array([s[0] for s in d['samples']]); Yp = np.array([s[1] for s in d['samples']])
sol = solve_ivp(rhs, (0, ts[-1]), y0, method='DOP853', rtol=1e-11, atol=1e-15, t_eval=ts)
Ys = sol.y[:2 * NK].T
err = np.abs(Yp - Ys).max(); scale = np.abs(Ys).max(); k = d['k11']
print(f"shake {d['shake']}, A = {A*1e3:.2f} mm, f = {f:.4f} Hz, {ts[-1]:.1f} s: largest |a_page - a_scipy| = {err:.3e} m, largest |a| = {scale:.3e} m, ratio {err/scale:.2e}")
print(f"  mode (1,1) cos at the end: page {Yp[-1, k]*1e3:.6f} mm, SciPy {Ys[-1, k]*1e3:.6f} mm")
ok = err / scale < 1e-6; print('PASS' if ok else 'FAIL', 'page RK4 agrees with DOP853 to 1e-6 of the largest amplitude'); sys.exit(0 if ok else 1)
