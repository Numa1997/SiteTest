"""Pillar of Fig. 14: a round column V = V0 for x^2 + y^2 < R^2, unbounded along z, or a hard column (psi = 0 inside), met by
the same 3D Gaussian packet as the sphere (sigma0 = 3, x0 = -14, k0 = sqrt(2E), hbar = m = 1), flying along x.

Why 2D is exact: V does not depend on z, so H = H_xy + H_z and psi(x, y, z, t) = phi(x, y, t) g(z, t): phi solves the 2D
equation with the disc, g is the free Gaussian (flat.gfree). The 3D picture is phi drawn at every z, weighted by g(z).

phi: Strang split-step Fourier on the same grid as the sphere (128 x 128 points, 0.5 a apart, box 64 a, the same absorbing
border in the outer tenth, made mirror-symmetric and the same per unit time for every dt). Hard column: after every step psi is set to 0 at the grid points inside the disc (projection). That
removes the small part the free step pushes into the column, so the norm falls by O(dt) per reflection: the stored norm curve
measures this error, and the convergence check in check_pillar.py halves dt to show it.
"""
import numpy as np, time
HARD = 1e6

def run(E, V0, R, s0=3.0, x0=-14.0, travel=30.0, dt=0.0025, N=128, L=64.0, nframes=48, hard_dt=0.0005):
    hard = V0 >= HARD
    if hard and hard_dt: dt = hard_dt
    dx = L / N; x = (np.arange(N) - N // 2) * dx
    X, Y = np.meshgrid(x, x, indexing="ij")
    k = 2 * np.pi * np.fft.fftfreq(N, dx); K2 = k[:, None]**2 + k[None, :]**2
    W = max(4, N // 10); d = np.minimum(np.arange(N), N - np.arange(N))        # cells to the periodic seam at x = +-L/2: mirror-symmetric
    m1 = np.sin(0.5 * np.pi * (np.minimum(d, W) + 1) / (W + 1)) ** (0.125 * dt / 0.01)   # never exactly 0: a finite absorber  # the sphere's border, per unit time (not per step)
    mask = m1[:, None] * m1[None, :]
    k0 = np.sqrt(2 * E)
    phi = (2 * np.pi * s0**2) ** -0.5 * np.exp(-((X - x0)**2 + Y**2) / (4 * s0**2) + 1j * k0 * X)
    disc = X**2 + Y**2 < R**2
    halfV = np.exp(-0.5j * np.where(disc, 0.0 if hard else V0, 0.0) * dt)
    kin = np.exp(-0.5j * K2 * dt)
    keep = (~disc).astype(float) if hard else np.ones_like(X)
    half = halfV * np.sqrt(mask)        # the border as half a step on each side, like V: keeps Strang's symmetry
    phi = phi * keep
    base = 0.0025; fdt = max(1, int(round(travel / k0 / base)) // (nframes - 1)) * base   # frame interval: the same for every dt
    per = int(round(fdt / dt))
    frames = []; curves = []; t0 = time.time()
    for f in range(nframes):
        if f:
            for _ in range(per):
                phi = half * phi; phi = np.fft.ifft2(kin * np.fft.fft2(phi)); phi = half * phi * keep
        t = f * per * dt
        p = np.abs(phi)**2 * dx**2
        rx = p.sum(axis=1); norm = rx.sum()
        behind = rx[x < -R].sum(); ahead = rx[x > R].sum()
        my = (p.sum(axis=0) * x).sum() / norm; sy = np.sqrt((p.sum(axis=0) * (x - my)**2).sum() / norm)
        frames.append(phi[:, N // 2:].copy())       # y >= 0; the half y < 0 is its mirror image
        curves.append((t, float(norm), float(behind), float(ahead), float(sy)))
    return dict(E=E, V0=V0, R=R, hard=hard, steps=per * (nframes - 1), dt=dt, plane=np.array(frames), curves=np.array(curves), wall=time.time() - t0, full_end=phi)
