"""Flat wall of Fig. 14: a slab V = V0 for |x| < a/2 (all y, z), or a hard wall (psi = 0 there), met by the same 3D Gaussian
packet as the sphere (sigma0 = 3, x0 = -14, k0 = sqrt(2E), hbar = m = 1).

Why 1D is exact: V depends on x only, so H = H_x + H_y + H_z and the packet, a product of three Gaussians, stays a product:
psi(x, y, z, t) = chi(x, t) g(y, t) g(z, t). g is a free 1D Gaussian; chi solves the 1D equation with the barrier.

chi: Crank-Nicolson on a uniform grid with the fourth-order Laplacian (-1, 16, -30, 16, -1) / (12 dx^2); unitary to rounding,
second order in dt, fourth order in dx. A hard wall removes the points |x| <= a/2 (psi = 0 there) and closes the stencil next
to each face with the odd mirror image (the ghost value beyond the face is -psi at the mirror point), so psi = 0 on the face.
g: the exact free solution, g(y, t) = (2 pi s0^2)^(-1/4) (1 + i t / (2 s0^2))^(-1/2) exp(-y^2 / (4 s0^2 (1 + i t / (2 s0^2)))).
"""
import numpy as np, time
from scipy.linalg import solve_banded

HARD = 1e6     # V0 at or above this means a hard wall

def gfree(y, t, s0):
    c = 1 + 1j * t / (2 * s0**2)
    return (2 * np.pi * s0**2) ** -0.25 * c ** -0.5 * np.exp(-y**2 / (4 * s0**2 * c))

def T_plane(E, V0, a):
    """Transmission probability of a plane wave of energy E through the slab (Griffiths 2.4; checked in check_flat.py)."""
    E = np.asarray(E, float); T = np.zeros_like(E)
    if V0 >= HARD: return T
    if V0 == 0: return np.ones_like(E)
    lo = E < V0; hi = E > V0; eq = np.isclose(E, V0)
    q = np.sqrt(2 * (V0 - E[lo])); T[lo] = 1 / (1 + V0**2 * np.sinh(q * a)**2 / (4 * E[lo] * (V0 - E[lo])))
    kp = np.sqrt(2 * (E[hi] - V0)); T[hi] = 1 / (1 + V0**2 * np.sin(kp * a)**2 / (4 * E[hi] * (E[hi] - V0)))
    T[eq] = 1 / (1 + E[eq] * a**2 / 2)
    return T

def T_packet(E, V0, a, s0=3.0):
    """Average of T over the packet's momenta along x: |phi(k)|^2 is a Gaussian about k0 with standard deviation 1/(2 s0)."""
    k0 = np.sqrt(2 * E); sk = 1 / (2 * s0)
    k = np.linspace(max(1e-6, k0 - 8 * sk), k0 + 8 * sk, 4001)
    w = np.exp(-(k - k0)**2 / (2 * sk**2)); w /= np.trapezoid(w, k)
    return float(np.trapezoid(w * T_plane(k**2 / 2, V0, a), k))

def run(E, V0, a, s0=3.0, x0=-14.0, travel=30.0, dt=0.01, dx=0.05, X=200.0, nframes=48, view=(-32.0, 0.5, 128, 64)):
    hard = V0 >= HARD
    n = int(round(2 * X / dx)); x = -X + dx * np.arange(n + 1)
    k0 = np.sqrt(2 * E)
    chi = (2 * np.pi * s0**2) ** -0.25 * np.exp(-(x - x0)**2 / (4 * s0**2) + 1j * k0 * x)
    inside = np.abs(x) < a / 2 - 1e-9; face = np.isclose(np.abs(x), a / 2)
    V = np.zeros_like(x)
    if not hard: V[inside] = V0; V[face] = V0 / 2          # the face point carries half: the slab is a wide
    wall = (inside | face) if hard else np.zeros_like(inside)
    chi[wall] = 0
    # H = -(1/2) D2 + V, D2 fourth order; banded form for solve_banded with (2, 2) bands
    c = np.array([-1, 16, -30, 16, -1]) / (12 * dx**2)
    H = np.zeros((5, n + 1), complex)        # ab[2 + i - j, j] = H[i, j]
    for off, cf in zip((-2, -1, 0, 1, 2), c):
        H[2 - off, max(0, off):n + 1 + min(0, off)] = -0.5 * cf
    H[2] += V
    # ends of the box: psi = 0 beyond (the packet never comes near: X = 200)
    if hard:
        idx = np.where(wall)[0]; L0, R0 = idx[0], idx[-1]       # first and last wall point (both faces are grid points)
        for j in idx:                                            # wall rows: identity, no coupling
            H[:, j] = 0
            for off in (-2, -1, 1, 2):
                i = j - off
                if 0 <= i <= n: H[2 + i - j, j] = 0              # column j: nothing couples into the wall
            H[2, j] = 0
        for i in idx:
            for off in (-2, -1, 1, 2):
                j = i + off
                if 0 <= j <= n: H[2 + i - j, j] = 0              # row i: the wall couples to nothing
        # odd ghosts: the point next to a face sees psi(face + dx) = -psi(face - dx)
        H[2, L0 - 1] += 0.5 * c[4]       # row L0-1: term c[4] psi[L0+1] = c[4] (-psi[L0-1]); H = -c/2 * D2
        H[2, R0 + 1] += 0.5 * c[0]
    A = H * (0.5j * dt); A[2] += 1                               # (1 + i H dt/2) chi_new = (1 - i H dt/2) chi
    B = -H * (0.5j * dt); B[2] += 1
    if hard:
        A[2, wall] = 1; B[2, wall] = 0
    def apply(Bm, v):
        out = Bm[2] * v
        for off in (-2, -1, 1, 2):
            if off > 0: out[:-off] += Bm[2 - off, off:] * v[off:]
            else: out[-off:] += Bm[2 - off, :off] * v[:off]
        return out
    steps = int(round(travel / k0 / dt)); per = max(1, steps // (nframes - 1))
    x0v, st, nx, nr = view
    xi = np.round((x0v + st * np.arange(nx) + X) / dx).astype(int)       # the view's x points on the fine grid
    rho = st * np.arange(nr)
    out = []; curves = []; t0 = time.time()
    for f in range(nframes):
        if f:
            for _ in range(per): chi = solve_banded((2, 2), A, apply(B, chi))
        t = f * per * dt
        p = np.abs(chi)**2
        norm = p.sum() * dx; behind = p[x < -a / 2].sum() * dx; ahead = p[x > a / 2].sum() * dx
        gr = gfree(rho, t, s0) * gfree(0.0, t, s0)                    # g(y) g(z) = g(0) g(rho) for a Gaussian: y^2 + z^2 = rho^2
        out.append(chi[xi][:, None] * gr[None, :])
        sy = s0 * np.sqrt(1 + (t / (2 * s0**2))**2)
        curves.append((t, float(norm), float(behind), float(ahead), float(sy)))
    return dict(E=E, V0=V0, a=a, hard=hard, steps=per * (nframes - 1), dt=dt, dx=dx, X=X, plane=np.array(out), curves=np.array(curves),
                chi_end=chi, x=x, wall=time.time() - t0)
