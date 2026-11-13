# 3D time-dependent Schrödinger equation, split-step Fourier (Strang), units hbar = m = 1: the remaining cases of Fig. 14.
# Same grid, border and step as tools/kaggle/schrodinger-sphere/solver.py (128^3 points, L = 64 a, periodic, absorbing border).
#   shape 'sphere' : ball of radius size at the origin (wells and the hard ball; the finite heights were computed on 2026-11-12)
#   shape 'coin'   : disc of radius size and thickness COIN_A, its axis along the flight: |x| < COIN_A / 2, rho < size
#   shape 'tube'   : endless tube along the flight, radius size, wall TUBE_W thick: |rho - size| < TUBE_W / 2
#   shape 'soff'   : spherical wave from the side onto a ball of radius size at the origin
#   shape 'sslab'  : spherical wave onto a flat wall |x| < size / 2
#   shape 'spil'   : spherical wave onto a pillar of radius size along z (rho_z = sqrt(x^2 + y^2) < size)
# Waves: a Gaussian packet from x0 = -14 a along +x (sphere, coin, tube), or a spherical shell (l = 0 about its own centre
# at (SRC_X, 0, 0) = (-17, 0, 0), u = r psi as in radial.py, r0 = 5 a, sigma0 = 2 a, outgoing: at the start its amplitude at the
# nearest point of a barrier of radius 4 is exp(-(13 - 5)^2 / 16) = 0.018 of its peak, so the wave starts outside the barrier).
# Version 2 (13 November 2026, 02:40 UTC): version 1 put the source at -12 with r0 = 6, so the shell began inside the barrier;
# and it left the start wave's tail inside hard walls, where it stayed. Now the start wave is set to zero inside a hard wall
# and normalised again (a hard wall means psi = 0 inside).
# Hard wall: the height HARD_V = 200 (the wave reaches 1 / sqrt(2 * 200) = 0.05 a into it, a tenth of the grid spacing; every
# energy of the grid is below 2.3 % of it) with a step four times shorter. Pure phase factors: no probability is removed.
# Stored per run: the half y >= 0 of the plane z = 0, |psi| and arg psi as 8-bit levels of EACH frame's peak |psi| in the plane
# (the list of peaks is in the header), and the probability curves from the whole psi.
import numpy as np, jax, jax.numpy as jnp, time
HARD_V, HARD_SUB, COIN_A, TUBE_W, SRC_X, SH_R0, SH_S0, SH_TRAVEL = 200.0, 4, 1.0, 1.0, -17.0, 5.0, 2.0, 24.0
SHELLS = ("soff", "sslab", "spil")

def setup(N, L, dtype=jnp.complex64):
    dx = L / N
    x = (np.arange(N) - N // 2) * dx
    k = 2 * np.pi * np.fft.fftfreq(N, dx)
    K2 = k[:, None, None]**2 + k[None, :, None]**2 + k[None, None, :]**2
    W = max(4, N // 10); m1 = np.ones(N)                       # absorbing layer: smooth mask in the outer W cells of each face
    edge = np.arange(W); m1[:W] = np.sin(0.5 * np.pi * edge / W)**0.125; m1[-W:] = m1[:W][::-1]
    mask = m1[:, None, None] * m1[None, :, None] * m1[None, None, :]
    return dict(N=N, L=L, dx=dx, x=x, K2=K2, mask=mask, dtype=dtype)

def barrier(shape, size, X, Y, Z):
    """inside: where V = V0; (mb, ma): the two regions whose probability the curves count ('behind' and 'ahead')."""
    rho2 = Y**2 + Z**2
    if shape in ("sphere", "soff"):
        return X**2 + rho2 < size**2, X < -size, X > size
    if shape == "coin":
        return (np.abs(X) < COIN_A / 2) & (rho2 < size**2), X < -COIN_A / 2, X > COIN_A / 2
    if shape == "tube":                                         # counted: inside the tube, and outside it
        rho = np.sqrt(rho2); return np.abs(rho - size) < TUBE_W / 2, rho <= size - TUBE_W / 2, rho >= size + TUBE_W / 2
    if shape == "sslab":
        return np.abs(X) < size / 2, X < -size / 2, X > size / 2
    if shape == "spil":
        return X**2 + Y**2 < size**2, X < -size, X > size
    raise ValueError(shape)

def start(shape, E, X, Y, Z, dx):
    k0 = np.sqrt(2 * E)
    if shape in SHELLS:                                         # psi = u(r) / r about (SRC_X, 0, 0); u odd in r, so psi is smooth at r = 0
        r = np.maximum(np.sqrt((X - SRC_X)**2 + Y**2 + Z**2), 1e-6)
        u = np.exp(-(r - SH_R0)**2 / (4 * SH_S0**2) + 1j * k0 * r) - np.exp(-(r + SH_R0)**2 / (4 * SH_S0**2) - 1j * k0 * r)
        psi = u / r
    else:
        psi = np.exp(-((X + 14.0)**2 + Y**2 + Z**2) / (4 * 3.0**2) + 1j * k0 * X)
    return psi / np.sqrt((np.abs(psi)**2).sum() * dx**3), k0

def run3(g, shape, E, V0, size, hard=False, travel=None, dt=0.01, nframes=48, wave=None, wave_every=2):
    """wave = (slice x, slice y, slice z): also stores Re psi on those points, every wave_every-th frame, as int8 levels of that
    frame's peak |Re psi| there (the peaks are returned)."""
    N, dx, x, dtype = g["N"], g["dx"], g["x"], g["dtype"]
    rdt = jnp.float32 if dtype == jnp.complex64 else jnp.float64
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    psi, k0 = start(shape, E, X, Y, Z, dx)
    inside, mb, ma = barrier(shape, size, X, Y, Z)
    del X, Y, Z
    if travel is None: travel = SH_TRAVEL if shape in SHELLS else 30.0
    if hard:                                                    # psi = 0 inside a hard wall from the start
        psi = np.where(inside, 0.0, psi); psi = psi / np.sqrt((np.abs(psi)**2).sum() * dx**3)
    sub = HARD_SUB if hard else 1; h = dt / sub
    V = np.where(inside, HARD_V if hard else V0, 0.0)
    steps = int(round(travel / k0 / dt)); per = max(1, steps // (nframes - 1))   # per: frame interval in steps of dt
    halfV = jnp.asarray(np.exp(-0.5j * V * h), dtype); kin = jnp.asarray(np.exp(-0.5j * g["K2"] * h), dtype)
    mask = jnp.asarray(g["mask"] ** (1.0 / sub), rdt); psi = jnp.asarray(psi, dtype)   # the border takes the same share per unit time
    MB = jnp.asarray(mb, rdt); MA = jnp.asarray(ma, rdt); xs = jnp.asarray(x, rdt)
    @jax.jit
    def chunk(p):
        def body(i, p):
            p = halfV * p; p = jnp.fft.ifftn(kin * jnp.fft.fftn(p)); p = halfV * p
            return p * mask
        return jax.lax.fori_loop(0, per * sub, body, p)
    @jax.jit
    def measure(p):
        rho = (jnp.abs(p)**2).astype(rdt) * dx**3
        ry = rho.sum(axis=(0, 2)); norm = ry.sum()
        behind = (rho * MB).sum(); ahead = (rho * MA).sum()
        my = (ry * xs).sum() / norm; sy = jnp.sqrt((ry * (xs - my)**2).sum() / norm)
        pz = p[:, N // 2:, N // 2]           # the plane z = 0, its half y >= 0
        wv = p[wave].real.astype(rdt) if wave is not None else jnp.zeros((1, 1, 1), rdt)
        return norm, behind, ahead, sy, jnp.abs(pz), jnp.angle(pz), wv
    A, P, peaks, WF, wpeaks, wframes, curves = [], [], [], [], [], [], []
    t0 = time.time()
    for f in range(nframes):
        if f: psi = chunk(psi)
        n, b, a, sy, sl, ph, wv = jax.device_get(measure(psi))
        sl = np.nan_to_num(sl); pk = float(sl.max()) or 1.0
        qa = np.clip(np.round(255 * sl / pk), 0, 255).astype(np.uint8)
        qp = (np.round((np.nan_to_num(ph) + np.pi) / (2 * np.pi) * 255) % 256).astype(np.uint8)
        qp[qa < 3] = 0                       # no phase where there is (almost) no wave: compresses well
        A.append(qa); P.append(qp); peaks.append(pk)
        if wave is not None and f % wave_every == 0:
            wv = np.nan_to_num(wv); wp = float(np.abs(wv).max()) or 1.0
            WF.append(np.clip(np.round(127 * wv / wp), -127, 127).astype(np.int8)); wpeaks.append(wp); wframes.append(f)
        curves.append((f * per * dt, float(n), float(b), float(a), float(sy)))
    jax.block_until_ready(psi)
    return dict(shape=shape, E=E, V0=V0, size=size, hard=bool(hard), steps=per * sub * (nframes - 1), dt=h, frame_dt=per * dt,
                amp=np.array(A), phase=np.array(P), peaks=peaks, curves=np.array(curves),
                wave=np.array(WF) if wave is not None else None, wpeaks=wpeaks, wframes=wframes, wall=time.time() - t0)
