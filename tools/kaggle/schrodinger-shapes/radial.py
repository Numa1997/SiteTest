"""Spherical waves of Fig. 14: a shell-shaped wave whose crests are spheres about the origin, meeting a barrier centred there.

Why 1D is exact: with V = V(r) and a wave the same in every direction (angular momentum l = 0), u = r psi obeys
    i du/dt = -(1/2) d2u/dr2 + V(r) u,   u(0, t) = 0,
the 1D equation on the half-line (Griffiths, Introduction to Quantum Mechanics, section 4.1). The half-line with u(0) = 0 is
solved on the whole line with u odd and V even: an odd start stays odd, so u(0) = 0 at every time without a boundary condition.
Normalisation: integral_0^inf |u|^2 dr = 1, so psi = u / (sqrt(4 pi) r) has integral |psi|^2 d^3r = 1.

Two cases (hbar = m = 1, k = sqrt(2E), shell width sigma0 = 2, so that the starting shell does not yet reach the wall):
  'out': u(r, 0) ~ f(r) - f(-r), f(r) = exp(-(r - r0)^2 / (4 sigma0^2) + i k r), r0 = 6: a shell leaving the centre, meeting a
         spherical shell wall V = V0 for |r - Rw| < d/2 at Rw = 16 (d = 0.5 ... 3), or a hard wall (u = 0 there), or a well.
         The radial problem is then exactly the flat wall of flat.py, so T_packet of flat.py is the reference.
  'in':  the same with k -> -k and r0 = 28: a shell closing in on a ball V = V0 for r < R at the centre (R = 2 ... 6), hard or a well.
Crank-Nicolson, fourth-order Laplacian, as flat.py; a hard wall removes its points and closes the stencil with the odd mirror.
"""
import numpy as np, time
from scipy.linalg import solve_banded
HARD = 1e6

def run(E, V0, size, kind, s0=2.0, dt=0.01, dx=0.05, X=200.0, nframes=48, nr=97, rstep=0.5):
    hard = V0 >= HARD
    n = int(round(2 * X / dx)); x = -X + dx * np.arange(n + 1); r = np.abs(x)
    k = np.sqrt(2 * E) * (1 if kind == 'out' else -1)
    r0 = 6.0 if kind == "out" else 28.0
    f = lambda y: np.exp(-(y - r0)**2 / (4 * s0**2) + 1j * k * y)
    u = f(x) - f(-x)                                                    # odd: u(0) = 0
    if kind == 'out':
        Rw = 16.0; inside = np.abs(r - Rw) < size / 2 - 1e-9; face = np.isclose(np.abs(r - Rw), size / 2)
    else:
        inside = r < size - 1e-9; face = np.isclose(r, size)
    V = np.zeros_like(x)
    if not hard: V[inside] = V0; V[face] = V0 / 2
    wall = (inside | face) if hard else np.zeros_like(inside)
    u[wall] = 0
    u /= np.sqrt(np.sum(np.abs(u[x > 0])**2) * dx)                       # integral over r > 0 of |u|^2 = 1
    c = np.array([-1, 16, -30, 16, -1]) / (12 * dx**2)
    H = np.zeros((5, n + 1), complex)
    for off, cf in zip((-2, -1, 0, 1, 2), c):
        H[2 - off, max(0, off):n + 1 + min(0, off)] = -0.5 * cf
    H[2] += V
    if hard:
        idx = np.where(wall)[0]
        for j in idx:
            H[:, j] = 0
            for off in (-2, -1, 1, 2):
                i = j + off
                if 0 <= i <= n: H[2 + j - i, i] = 0
        # odd ghosts at each face of each wall interval: the point next to a face sees -psi at its mirror
        edges = [j for j in idx if (j - 1) not in set(idx)] ; ends = [j for j in idx if (j + 1) not in set(idx)]
        for L0 in edges: H[2, L0 - 1] += 0.5 * c[4]
        for R0 in ends: H[2, R0 + 1] += 0.5 * c[0]
    A = H * (0.5j * dt); A[2] += 1
    B = -H * (0.5j * dt); B[2] += 1
    if hard: A[2, wall] = 1; B[2, wall] = 0
    def apply(Bm, v):
        out = Bm[2] * v
        for off in (-2, -1, 1, 2):
            if off > 0: out[:-off] += Bm[2 - off, off:] * v[off:]
            else: out[-off:] += Bm[2 - off, :off] * v[:off]
        return out
    travel = 24.0 if kind == 'out' else 40.0
    steps = int(round(travel / abs(k) / dt)); per = max(1, steps // (nframes - 1))
    rr = rstep * np.arange(nr); ri = np.round((rr + X) / dx).astype(int)
    edge_lo = (16.0 - size / 2) if kind == 'out' else size
    edge_hi = (16.0 + size / 2) if kind == 'out' else size
    prof = []; curves = []; t0 = time.time()
    for fr in range(nframes):
        if fr:
            for _ in range(per): u = solve_banded((2, 2), A, apply(B, u))
        t = fr * per * dt
        pos = x > 0; p = np.abs(u[pos])**2 * dx; rp = x[pos]
        norm = p.sum(); low = p[rp < edge_lo].sum(); high = p[rp > edge_hi].sum(); rmean = (p * rp).sum() / max(norm, 1e-30)
        ur = u[ri]; psi = np.empty(nr, complex)
        psi[1:] = ur[1:] / (np.sqrt(4 * np.pi) * rr[1:])
        psi[0] = (u[ri[0] + 1] / dx) / np.sqrt(4 * np.pi)                 # psi(0) = u'(0) / sqrt(4 pi)
        prof.append(psi); curves.append((t, float(norm), float(low), float(high), float(rmean)))
    return dict(E=E, V0=V0, size=size, kind=kind, hard=hard, steps=per * (nframes - 1), dt=dt, dx=dx, profile=np.array(prof), curves=np.array(curves), wall=time.time() - t0)
