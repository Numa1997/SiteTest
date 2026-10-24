"""Region of attraction of the LQR catch, measured: a vectorised RK4 over many starts at once.
Run: python3 notes/fig12/roa.py"""
import sys; sys.path.insert(0, 'notes/fig12')
import numpy as np, physics as P

def batch(Y, K, T=4.0, h=1e-3):
    Y = Y.copy()
    def f(Y):
        ph, al, w, v = Y.T
        e = np.stack([P.wrap(ph), P.wrap(al), w, v], 1)
        V = np.clip(-(e @ K), -P.VMAX, P.VMAX)
        tau = P.KM * (V - P.KM * w) / P.RM
        s, c = np.sin(al), np.cos(al)
        a11 = P.J0 + P.JP * s * s; a12 = P.HH * c; a22 = P.JP
        r1 = tau - P.BR * w - 2 * P.JP * s * c * w * v + P.HH * s * v * v
        r2 = P.JP * s * c * w * w + P.GG * s - P.BP * v
        det = a11 * a22 - a12 * a12
        return np.stack([w, v, (a22 * r1 - a12 * r2) / det, (a11 * r2 - a12 * r1) / det], 1)
    for i in range(int(round(T / h))):
        k1 = f(Y); k2 = f(Y + h / 2 * k1); k3 = f(Y + h / 2 * k2); k4 = f(Y + h * k3)
        Y = Y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        Y[np.abs(Y[:, 2]) > 500] = np.nan
    e = np.stack([P.wrap(Y[:, 0]), P.wrap(Y[:, 1]), Y[:, 2], Y[:, 3]], 1)
    return np.nanmax(np.abs(e), 1) < 0.01

if __name__ == '__main__':
    A, B = P.linear(); K, Pm = P.lqr(A, B, (2, 40, 0.5, 2), 1.0)
    na, nv = 61, 61
    al = np.radians(np.linspace(-60, 60, na)); vv = np.linspace(-12, 12, nv)
    AA, VV = np.meshgrid(al, vv, indexing='ij')
    Y = np.stack([np.zeros(AA.size), AA.ravel(), np.zeros(AA.size), VV.ravel()], 1)
    okm = batch(Y, K).reshape(na, nv)
    print('slice phi = phi*, phid = 0: caught', okm.sum(), 'of', okm.size)
    for j in [0, nv // 4, nv // 2, 3 * nv // 4, nv - 1]:
        row = okm[:, j]; a_ok = np.degrees(al[row]); print(f'  alpha_dot = {vv[j]:6.1f} rad/s: alpha from {a_ok.min() if row.any() else np.nan:6.1f} to {a_ok.max() if row.any() else np.nan:6.1f} deg')
    # the largest Lyapunov level c whose whole surface (sampled in 4D) is caught
    rng = np.random.default_rng(1)
    Lc = np.linalg.cholesky(np.linalg.inv(Pm))
    def surface(c, n=2000):
        z = rng.standard_normal((n, 4)); z /= np.linalg.norm(z, axis=1)[:, None]
        return (np.sqrt(c) * (Lc @ z.T)).T
    lo, hi = 0.0, 50.0
    for it in range(14):
        c = 0.5 * (lo + hi); frac = batch(surface(c), K).mean()
        if frac == 1.0: lo = c
        else: hi = c
        print(f'  c = {c:8.4f}: caught {frac*100:6.2f} % of 2000 starts on the surface')
    print('largest level with every sampled start caught: c =', lo)
    np.savez('notes/fig12/roa.npz', al=al, vv=vv, ok=okm, c=lo, P=Pm, K=K)
