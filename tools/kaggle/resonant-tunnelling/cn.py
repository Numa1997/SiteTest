"""Fig. 15, Step B4: an independent time-dependent solve of the double barrier, to check recon.py frame by frame.

Crank-Nicolson in time with the fourth-order Laplacian (-1, 16, -30, 16, -1) / (12 dx^2), the scheme of Fig. 14's
tools/kaggle/schrodinger-shapes/flat.py. The barrier faces of Fig. 15 do not fall on grid points, so each grid point carries the
potential averaged over its own cell [x - dx/2, x + dx/2] (second-order in the face position). Box [-X, X] with psi = 0 beyond,
far larger than any distance the packet travels. hbar = m = 1.
"""
import numpy as np, time
from scipy.linalg import solve_banded


def cell_potential(x, dx, segs):
    V = np.zeros_like(x)
    for (l, r, V0) in segs:
        lo = np.maximum(x - dx / 2, l); hi = np.minimum(x + dx / 2, r)
        V += V0 * np.clip(hi - lo, 0, None) / dx
    return V


def run(E, segs, s0, x0, times, dx=0.025, dt=0.005, X=None, xv=None):
    k0 = np.sqrt(2 * E)
    if X is None:
        X = abs(x0) + (k0 + 10 / (2 * s0)) * times[-1] + 10 * s0 + 50
    X = np.ceil(X)                     # a whole number, so the stored points (multiples of 0.25) are grid points
    n = int(round(2 * X / dx)); x = -X + dx * np.arange(n + 1)
    psi = (2 * np.pi * s0**2) ** -0.25 * np.exp(-(x - x0)**2 / (4 * s0**2) + 1j * k0 * x)
    V = cell_potential(x, dx, segs)
    c = np.array([-1, 16, -30, 16, -1]) / (12 * dx**2)
    H = np.zeros((5, n + 1), complex)
    for off, cf in zip((-2, -1, 0, 1, 2), c):
        H[2 - off, max(0, off):n + 1 + min(0, off)] = -0.5 * cf
    H[2] += V
    A = H * (0.5j * dt); A[2] += 1
    B = -H * (0.5j * dt); B[2] += 1

    def apply(Bm, v):
        out = Bm[2] * v
        for off in (-2, -1, 1, 2):
            if off > 0: out[:-off] += Bm[2 - off, off:] * v[off:]
            else: out[-off:] += Bm[2 - off, :off] * v[:off]
        return out
    steps = np.rint(np.asarray(times) / dt).astype(int)
    assert np.allclose(steps * dt, times, atol=1e-9), "frame times must be whole numbers of steps"
    xi = np.rint((xv + X) / dx).astype(int); assert np.allclose(x[xi], xv)
    out = []; done = 0; t0 = time.time(); norms = []
    for st in steps:
        while done < st:
            psi = solve_banded((2, 2), A, apply(B, psi)); done += 1
        out.append(psi[xi].copy()); norms.append(float(np.sum(np.abs(psi)**2) * dx))
    return dict(frames=np.array(out), norm=np.array(norms), x=x, V=V, seconds=time.time() - t0, X=X, dx=dx, dt=dt)
