# Fig. 15, 3D: a Gaussian electron wave packet meets TWO barriers, solved in three dimensions on Kaggle's GPUs.
# Scheme as Fig. 14 (tools/kaggle/schrodinger-shapes/solver3d.py): Strang split-step Fourier, hbar = m = 1, grid spacing 0.5 a,
# dt = 0.01, a smooth absorbing border sin^(1/8) in the outer tenth of each axis, complex64 on the GPU.
# Box: Nx x N x N points (default 192 x 128 x 128: 96 a along the flight, 64 a across), so a sigma0 = 3 packet starts at
# x0 = -20 a, 14 a clear of every barrier and 22 a clear of the border.
#
# Shapes (barrier height V0, thickness D = 1 a, centre spacing S = 2.5 a; every face of the planar shapes lies on a cell
# boundary of the 0.5 a grid, odd multiples of 0.25 a, so the grid holds exactly the intended barrier; see notes/fig15/grid_test2.py):
#   dflat   two infinite walls |x -/+ S/2| < D/2                      (separable: x-marginal = the 1D problem exactly)
#   dcoin   two discs of radius size, same x profile, axis along the flight
#   dshell  two concentric spherical shells |r - Rc| < D/2, Rc = size and size + S, about the origin
#   sflat, scoin, sshell   the single barriers (one wall / disc at x = 0, one shell at r = size): the limit and check of each stack
# Stored per run (on the host, every frame): the half y >= 0 of the plane z = 0 over x in [-32, 32), |psi| and arg psi as 8-bit
# levels of each frame's own peak (peaks in the header); the probability profile along x (integral over y, z), float32;
# region probabilities from the whole psi.
import numpy as np, jax, jax.numpy as jnp, time

V0_DEF, D, S, X0, SIG0 = 2.0, 1.0, 2.5, -20.0, 3.0
SHAPES = ("dflat", "dcoin", "dshell", "sflat", "scoin", "sshell")


def setup(Nx=192, N=128, dx=0.5):
    def axis(n):
        x = (np.arange(n) - n // 2) * dx
        k = 2 * np.pi * np.fft.fftfreq(n, dx)
        W = max(4, n // 10); m = np.ones(n); e = np.arange(W)
        m[:W] = np.sin(0.5 * np.pi * e / W) ** 0.125; m[-W:] = m[:W][::-1]
        return x, k, m
    x, kx, mx = axis(Nx); y, ky, my = axis(N)
    K2 = kx[:, None, None]**2 + ky[None, :, None]**2 + ky[None, None, :]**2
    mask = mx[:, None, None] * my[None, :, None] * my[None, None, :]
    return dict(Nx=Nx, N=N, dx=dx, x=x, y=y, K2=K2, mask=mask)


def geometry(shape, size, X, Y, Z):
    """inside: where V = V0. regions: name -> boolean mask, for the probability curves."""
    rho2 = Y**2 + Z**2
    if shape in ("dflat", "dcoin", "sflat", "scoin"):
        lat = np.ones_like(X, bool) if shape.endswith("flat") else rho2 < size**2
        if shape[0] == "d":
            slab = (np.abs(X - S / 2) < D / 2) | (np.abs(X + S / 2) < D / 2)
            outer = S / 2 + D / 2; inner = S / 2 - D / 2
            regions = dict(left=X < -outer, right=X > outer, well=(np.abs(X) < inner) & lat)
        else:
            slab = np.abs(X) < D / 2
            regions = dict(left=X < -D / 2, right=X > D / 2)
        return slab & lat, regions
    if shape in ("dshell", "sshell"):
        r = np.sqrt(X**2 + rho2)
        if shape == "dshell":
            r1, r2 = size, size + S
            inside = (np.abs(r - r1) < D / 2) | (np.abs(r - r2) < D / 2)
            regions = dict(core=r < r1 - D / 2, gap=(r > r1 + D / 2) & (r < r2 - D / 2), out=r > r2 + D / 2)
        else:
            inside = np.abs(r - size) < D / 2
            regions = dict(core=r < size - D / 2, out=r > size + D / 2)
        return inside, regions
    raise ValueError(shape)


def t_end_of(E, tau=14.2):
    """Flight from x0 = -20 to +20 at the mean speed, plus three lifetimes of the trapped state (tau of the 1D resonance)."""
    return 40.0 / np.sqrt(2 * E) + 3 * tau


def run(g, shape, E, size=0.0, V0=V0_DEF, dt=0.01, nframes=200, t_end=None, xcrop=(-32.0, 32.0)):
    N, dx, x, y = g["N"], g["dx"], g["x"], g["y"]
    X, Y, Z = np.meshgrid(x, y, y, indexing="ij")
    k0 = np.sqrt(2 * E)
    psi = np.exp(-((X - X0)**2 + Y**2 + Z**2) / (4 * SIG0**2) + 1j * k0 * X)
    psi = psi / np.sqrt((np.abs(psi)**2).sum() * dx**3)
    inside, regions = geometry(shape, size, X, Y, Z)
    start_in_barrier = float((np.abs(psi[inside])**2).sum() * dx**3)       # the start wave's share inside a barrier (must be ~0)
    start_in_border = float((np.abs(psi)**2 * (1 - g["mask"])).sum() * dx**3)
    V = np.where(inside, V0, 0.0)
    del X, Y, Z
    if t_end is None: t_end = t_end_of(E)
    steps = int(round(t_end / dt)); per = max(1, steps // (nframes - 1))
    halfV = jnp.asarray(np.exp(-0.5j * V * dt), jnp.complex64)
    kin = jnp.asarray(np.exp(-0.5j * g["K2"] * dt), jnp.complex64)
    mask = jnp.asarray(g["mask"], jnp.float32)
    R = {k: jnp.asarray(v, jnp.float32) for k, v in regions.items()}
    i0 = int(np.searchsorted(x, xcrop[0])); i1 = int(np.searchsorted(x, xcrop[1]))
    p = jnp.asarray(psi, jnp.complex64); del psi

    @jax.jit
    def chunk(p):
        def body(i, p):
            p = halfV * p; p = jnp.fft.ifftn(kin * jnp.fft.fftn(p)); p = halfV * p
            return p * mask
        return jax.lax.fori_loop(0, per, body, p)

    @jax.jit
    def measure(p):
        rho = (jnp.abs(p)**2) * dx**3
        prof = rho.sum(axis=(1, 2)) / dx                                  # probability per unit length along x
        reg = {k: (rho * m).sum() for k, m in R.items()}
        pz = p[i0:i1, N // 2:, N // 2]
        return rho.sum(), prof, reg, jnp.abs(pz), jnp.angle(pz)

    A, P, peaks, prof, curves = [], [], [], [], []
    t0 = time.time()
    for f in range(nframes):
        if f: p = chunk(p)
        n, pr, reg, sl, ph = jax.device_get(measure(p))
        sl = np.nan_to_num(sl); pk = float(sl.max()) or 1.0
        qa = np.clip(np.round(255 * sl / pk), 0, 255).astype(np.uint8)
        qp = (np.round((np.nan_to_num(ph) + np.pi) / (2 * np.pi) * 255) % 256).astype(np.uint8); qp[qa < 3] = 0
        A.append(qa); P.append(qp); peaks.append(pk); prof.append(np.asarray(pr, np.float32))
        curves.append([f * per * dt, float(n)] + [float(reg[k]) for k in sorted(regions)])
    jax.block_until_ready(p)
    return dict(shape=shape, E=E, V0=V0, size=size, steps=per * (nframes - 1), dt=dt, frame_dt=per * dt, nframes=nframes,
                amp=np.array(A), phase=np.array(P), peaks=peaks, prof=np.array(prof), curves=np.array(curves),
                curve_names=["t", "norm"] + sorted(regions), start_in_barrier=start_in_barrier, start_in_border=start_in_border,
                x_first=float(x[i0]), nxs=i1 - i0, wall=time.time() - t0)


def run1d(g, E, V0=V0_DEF, single=False, dt=0.01, nframes=200, t_end=None):
    """The flat walls' exact 1D twin on the same x-axis, mask and step (numpy, host): psi_3D = chi(x) g(y) g(z) for dflat/sflat,
    so the 3D run's x-profile divided by its norm must equal this run's |chi|^2 divided by its norm. Also returns the probability
    the border absorbed on the left and on the right (reflected and transmitted waves that left the box)."""
    x, dx = g["x"], g["dx"]; n = x.size
    k = 2 * np.pi * np.fft.fftfreq(n, dx)
    W = max(4, n // 10); m = np.ones(n); e = np.arange(W); m[:W] = np.sin(0.5 * np.pi * e / W) ** 0.125; m[-W:] = m[:W][::-1]
    slab = (np.abs(x) < D / 2) if single else ((np.abs(x - S / 2) < D / 2) | (np.abs(x + S / 2) < D / 2))
    V = np.where(slab, V0, 0.0); k0 = np.sqrt(2 * E)
    chi = np.exp(-(x - X0)**2 / (4 * SIG0**2) + 1j * k0 * x).astype(np.complex128); chi /= np.sqrt((abs(chi)**2).sum() * dx)
    hv = np.exp(-0.5j * V * dt); kin = np.exp(-0.5j * k**2 * dt)
    if t_end is None: t_end = t_end_of(E)
    steps = int(round(t_end / dt)); per = max(1, steps // (nframes - 1))
    lost_l = lost_r = 0.0; prof = []
    for f in range(nframes):
        for _ in range(per if f else 0):
            chi = hv * chi; chi = np.fft.ifft(kin * np.fft.fft(chi)); chi = hv * chi
            before = abs(chi)**2; chi = chi * m; d = (before - abs(chi)**2) * dx
            lost_l += d[x < 0].sum(); lost_r += d[x > 0].sum()
        prof.append((abs(chi)**2).astype(np.float32))
    edge = D / 2 if single else S / 2 + D / 2
    return dict(prof=np.array(prof), transmitted=float((abs(chi[x > edge])**2).sum() * dx + lost_r),
                reflected=float((abs(chi[x < -edge])**2).sum() * dx + lost_l), norm_end=float((abs(chi)**2).sum() * dx))
