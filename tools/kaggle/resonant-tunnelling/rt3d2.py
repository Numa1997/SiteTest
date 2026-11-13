# Fig. 15, 3D, generation 2: the whole parameter space. The scheme of rt3d.py (generation 1), generalised:
#   Strang split-step Fourier, hbar = m = 1, grid 0.5 a, dt = 0.01, absorbing border sin^(1/8) in the outer tenth of each axis,
#   complex64 on the GPU.
# A run is a spec (a dict):
#   shape   'flat' (walls: all y, z) | 'coin' (discs of radius R on the flight axis) | 'shell' (concentric spherical shells)
#   N       number of barriers (1, 2, 3, 5, 10; shells 1 or 2)
#   V0, D   barrier height and thickness;  P  centre-to-centre spacing (period);  R  disc radius, or the inner shell's radius
#   bias    a voltage across the structure: V(x) falls linearly by `bias` from the left face of the first barrier to the right face
#           of the last (the contacts), flat on either side: 0 on the left, -bias on the right (the tilted potential of iv.py)
#   E       mean kinetic energy of the packet;  sx, sp  packet widths along and across the flight;  Nx  grid points along x
# Walls and discs: the barrier centres are c_k = c + (k - (N-1)/2) P, with c = 0 or 0.25 chosen so that every face c_k +- D/2 lies
# on a cell boundary of the 0.5 a grid (an odd multiple of 0.25 a): the grid then holds each barrier at its intended thickness.
# The packet starts 4 sx clear of the first face (at least 14 a), wholly outside every barrier (its share inside is stored).
# Stored per run, as in generation 1: the plane z = 0, half y >= 0, over the interior of the box, |psi| and arg psi as 8-bit levels
# of each frame's own peak (peaks in the header); the probability along x (integral over y, z), float32; region probabilities.
import numpy as np, jax, jax.numpy as jnp, time


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
    return dict(Nx=Nx, N=N, dx=dx, x=x, y=y, K2=K2, mask=mask, mx=mx, kx=kx, inner=(Nx // 2 - max(4, Nx // 10)) * dx)


def centres(sp):
    """Barrier centres along x (walls, discs): faces on odd multiples of 0.25."""
    N, P, D = sp["N"], sp["P"], sp["D"]
    for c in (0.0, 0.25):
        cs = [c + (k - (N - 1) / 2) * P for k in range(N)]
        faces = [f for ck in cs for f in (ck - D / 2, ck + D / 2)]
        if all(abs((f - 0.25) / 0.5 - round((f - 0.25) / 0.5)) < 1e-9 for f in faces): return cs
    raise ValueError(f"no grid-aligned placement for N={N}, P={P}, D={D}")


def extent(sp):
    """(first face, last face) along x of the structure."""
    if sp["shape"] == "shell":
        Rout = sp["R"] + (sp["N"] - 1) * sp["P"] + sp["D"] / 2
        return -Rout, Rout
    cs = centres(sp); return cs[0] - sp["D"] / 2, cs[-1] + sp["D"] / 2


def x0_of(sp):
    return extent(sp)[0] - max(14.0, 4 * sp["sx"])


def segs_1d(sp):
    """The structure along x as flat barriers (for tm.py): exact for walls without bias."""
    return [(c - sp["D"] / 2, c + sp["D"] / 2, sp["V0"]) for c in centres(sp)]


def vbias(sp, x):
    xl, xr = extent(sp)
    if not sp.get("bias"): return np.zeros_like(x)
    return -sp["bias"] * np.clip((x - xl) / (xr - xl), 0.0, 1.0)


def geometry(sp, X, Y, Z):
    """inside: where the barrier potential V0 acts; regions: name -> mask, for the probability curves."""
    rho2 = Y**2 + Z**2; D = sp["D"]
    if sp["shape"] in ("flat", "coin"):
        lat = np.ones_like(X, bool) if sp["shape"] == "flat" else rho2 < sp["R"]**2
        cs = centres(sp); slab = np.zeros_like(X, bool)
        for c in cs: slab |= np.abs(X - c) < D / 2
        xl, xr = cs[0] - D / 2, cs[-1] + D / 2
        regions = dict(left=X < xl, right=X > xr)
        if len(cs) > 1: regions["well"] = (X > cs[0] + D / 2) & (X < cs[-1] - D / 2) & ~slab & lat
        return slab & lat, regions
    r = np.sqrt(X**2 + rho2); Rs = [sp["R"] + k * sp["P"] for k in range(sp["N"])]
    inside = np.zeros_like(X, bool)
    for Rc in Rs: inside |= np.abs(r - Rc) < D / 2
    regions = dict(core=r < Rs[0] - D / 2, out=r > Rs[-1] + D / 2)
    if len(Rs) > 1: regions["gap"] = (r > Rs[0] + D / 2) & (r < Rs[-1] - D / 2) & ~inside
    return inside, regions


def tau_est(sp, tm):
    """The longest lifetime 1/Gamma of the 1D resonances within the packet's energy window (walls, no bias), capped; it sets the
    run length (3 tau after the flight), so that the trapped wave has decayed when the run stops."""
    if sp["shape"] == "shell": return 30.0
    k0 = np.sqrt(2 * sp["E"]); dE = k0 / (2 * sp["sx"])
    Es = np.linspace(max(0.02, sp["E"] - 4 * dE - 0.3), sp["E"] + 4 * dE + 0.3, 2400)   # wide enough that no peak in the window is cut
    lo, hi = sp["E"] - 4 * dE, sp["E"] + 4 * dE
    segs = segs_1d(sp); T = np.array([abs(tm.solve(e, segs)[0])**2 for e in Es]); tau = 5.0
    for i in range(1, len(T) - 1):
        if T[i] > 0.5 and T[i] >= T[i - 1] and T[i] >= T[i + 1]:
            h = T[i] / 2; l = i; r = i
            while l > 0 and T[l] > h: l -= 1
            while r < len(T) - 1 and T[r] > h: r += 1
            if T[l] <= h and T[r] <= h and r > l and lo <= Es[i] <= hi: tau = max(tau, 1 / (Es[r] - Es[l]))
    return float(min(tau, 60.0 if sp["sx"] <= 4 else 150.0))


def t_end_of(sp, tm):
    """The flight of the packet's trailing edge (2 sx behind its centre) from the start to 20 a past the last face, plus three
    lifetimes of the longest-lived resonance the packet holds."""
    xl, xr = extent(sp); v = np.sqrt(2 * sp["E"])
    return float((xr + 20 - x0_of(sp) + 2 * sp["sx"]) / v + 3 * tau_est(sp, tm))


def run(g, sp, t_end, dt=0.01, nframes=200):
    N, dx, x, y = g["N"], g["dx"], g["x"], g["y"]
    X, Y, Z = np.meshgrid(x, y, y, indexing="ij")
    k0 = np.sqrt(2 * sp["E"]); x0 = x0_of(sp)
    psi = np.exp(-(X - x0)**2 / (4 * sp["sx"]**2) - (Y**2 + Z**2) / (4 * sp["sp"]**2) + 1j * k0 * X)
    psi = psi / np.sqrt((np.abs(psi)**2).sum() * dx**3)
    inside, regions = geometry(sp, X, Y, Z)
    start_in_barrier = float((np.abs(psi[inside])**2).sum() * dx**3)
    start_in_border = float((np.abs(psi)**2 * (1 - g["mask"])).sum() * dx**3)
    V = np.where(inside, sp["V0"], 0.0) + vbias(sp, X)
    del X, Y, Z
    steps = int(round(t_end / dt)); per = max(1, steps // (nframes - 1))
    halfV = jnp.asarray(np.exp(-0.5j * V * dt), jnp.complex64); del V
    kin = jnp.asarray(np.exp(-0.5j * g["K2"] * dt), jnp.complex64)
    mask = jnp.asarray(g["mask"], jnp.float32)
    R = {k: jnp.asarray(v, jnp.float32) for k, v in regions.items()}
    i0 = int(np.searchsorted(x, -g["inner"])); i1 = int(np.searchsorted(x, g["inner"]))
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
        prof = rho.sum(axis=(1, 2)) / dx
        reg = {k: (rho * m).sum() for k, m in R.items()}
        pz = p[i0:i1, N // 2:, N // 2]
        return rho.sum(), prof, reg, jnp.abs(pz), jnp.angle(pz)

    A, Pp, peaks, prof, curves = [], [], [], [], []
    t0 = time.time()
    for f in range(nframes):
        if f: p = chunk(p)
        n, pr, reg, sl, ph = jax.device_get(measure(p))
        sl = np.nan_to_num(sl); pk = float(sl.max()) or 1.0
        qa = np.clip(np.round(255 * sl / pk), 0, 255).astype(np.uint8)
        qp = (np.round((np.nan_to_num(ph) + np.pi) / (2 * np.pi) * 255) % 256).astype(np.uint8); qp[qa < 3] = 0
        A.append(qa); Pp.append(qp); peaks.append(pk); prof.append(np.asarray(pr, np.float32))
        curves.append([f * per * dt, float(n)] + [float(reg[k]) for k in sorted(regions)])
    jax.block_until_ready(p)
    return dict(steps=per * (nframes - 1), frame_dt=per * dt, nframes=nframes, x0=x0,
                amp=np.array(A), phase=np.array(Pp), peaks=peaks, prof=np.array(prof), curves=np.array(curves),
                curve_names=["t", "norm"] + sorted(regions), start_in_barrier=start_in_barrier, start_in_border=start_in_border,
                x_first=float(x[i0]), nxs=i1 - i0, wall=time.time() - t0)


def run1d(g, sp, t_end, dt=0.01, nframes=200):
    """The walls' exact 1D twin (any N, any bias) on the same x axis, mask and step: psi_3D = chi(x) g(y) g(z) whenever V depends
    on x alone. Returns the profile |chi|^2 every frame and the share transmitted and reflected, counting what the border absorbed."""
    x, dx = g["x"], g["dx"]; n = x.size; k = g["kx"]; m = g["mx"]
    V = vbias(sp, x)
    for c in centres(sp): V = V + np.where(np.abs(x - c) < sp["D"] / 2, sp["V0"], 0.0)
    k0 = np.sqrt(2 * sp["E"]); x0 = x0_of(sp)
    chi = np.exp(-(x - x0)**2 / (4 * sp["sx"]**2) + 1j * k0 * x).astype(np.complex128); chi /= np.sqrt((abs(chi)**2).sum() * dx)
    hv = np.exp(-0.5j * V * dt); kin = np.exp(-0.5j * k**2 * dt)
    steps = int(round(t_end / dt)); per = max(1, steps // (nframes - 1))
    lost_l = lost_r = 0.0; prof = []
    xl, xr = extent(sp)
    for f in range(nframes):
        for _ in range(per if f else 0):
            chi = hv * chi; chi = np.fft.ifft(kin * np.fft.fft(chi)); chi = hv * chi
            before = abs(chi)**2; chi = chi * m; d = (before - abs(chi)**2) * dx
            lost_l += d[x < 0].sum(); lost_r += d[x > 0].sum()
        prof.append((abs(chi)**2).astype(np.float32))
    return dict(prof=np.array(prof), transmitted=float((abs(chi[x > xr])**2).sum() * dx + lost_r),
                reflected=float((abs(chi[x < xl])**2).sum() * dx + lost_l), norm_end=float((abs(chi)**2).sum() * dx))
