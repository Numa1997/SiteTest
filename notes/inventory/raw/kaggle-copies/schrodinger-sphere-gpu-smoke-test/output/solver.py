# 3D time-dependent Schrödinger equation, split-step Fourier (Strang), units hbar = m = 1.
import numpy as np, jax, jax.numpy as jnp, time, zlib
def setup(N, L, dtype=jnp.complex64):
    dx = L / N
    x = (np.arange(N) - N // 2) * dx
    k = 2 * np.pi * np.fft.fftfreq(N, dx)
    K2 = k[:, None, None]**2 + k[None, :, None]**2 + k[None, None, :]**2
    # absorbing layer: smooth mask in the outer W cells of each face
    W = max(4, N // 10); m1 = np.ones(N)
    edge = np.arange(W); m1[:W] = np.sin(0.5 * np.pi * edge / W)**0.125 ; m1[-W:] = m1[:W][::-1]
    mask = m1[:, None, None] * m1[None, :, None] * m1[None, None, :]
    return dict(N=N, L=L, dx=dx, x=x, K2=K2, mask=mask, dtype=dtype)

def run(g, E, V0, R, sigma0=3.0, x0=-14.0, travel=30.0, dt=0.01, nframes=48, out=128):
    N, dx, x, dtype = g["N"], g["dx"], g["x"], g["dtype"]
    rdt = jnp.float32 if dtype == jnp.complex64 else jnp.float64
    k0 = np.sqrt(2 * E)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    psi = (2 * np.pi * sigma0**2) ** -0.75 * np.exp(-((X - x0)**2 + Y**2 + Z**2) / (4 * sigma0**2) + 1j * k0 * X)
    V = np.where(X**2 + Y**2 + Z**2 < R**2, V0, 0.0)
    del X, Y, Z
    steps = int(round(travel / k0 / dt)); per = max(1, steps // (nframes - 1))
    halfV = jnp.asarray(np.exp(-0.5j * V * dt), dtype); kin = jnp.asarray(np.exp(-0.5j * g["K2"] * dt), dtype)
    mask = jnp.asarray(g["mask"], rdt); psi = jnp.asarray(psi, dtype)
    @jax.jit
    def chunk(p):
        def body(i, p):
            p = halfV * p; p = jnp.fft.ifftn(kin * jnp.fft.fftn(p)); p = halfV * p
            return p * mask
        return jax.lax.fori_loop(0, per, body, p)
    xs = jnp.asarray(x, rdt)
    @jax.jit
    def measure(p):
        rho = (jnp.abs(p)**2).astype(rdt) * dx**3
        rx = rho.sum(axis=(1, 2)); ry = rho.sum(axis=(0, 2))
        norm = rx.sum()
        behind = jnp.where(xs < -R, rx, 0).sum(); ahead = jnp.where(xs > R, rx, 0).sum()
        my = (ry * xs).sum() / norm; sy = jnp.sqrt((ry * (xs - my)**2).sum() / norm)
        pz = p[:, :, N // 2]                # the plane z = 0, through the sphere's centre
        sl = jnp.abs(pz); ph = jnp.angle(pz)
        return norm, behind, ahead, sy, sl, ph
    st = max(1, N // out); amp0 = None; F = []; P = []; curves = []
    t0 = time.time()
    for f in range(nframes):
        if f: psi = chunk(psi)
        n, b, a, sy, sl, ph = jax.device_get(measure(psi))
        if amp0 is None: amp0 = sl.max()
        qa = np.clip(np.round(255 * np.nan_to_num(sl[::st, ::st]) / amp0), 0, 255).astype(np.uint8)
        qp = (np.round((np.nan_to_num(ph[::st, ::st]) + np.pi) / (2 * np.pi) * 255) % 256).astype(np.uint8)
        qp[qa < 3] = 0                      # no phase where there is (almost) no wave: compresses well
        F.append(qa); P.append(qp)
        curves.append((f * per * dt, float(n), float(b), float(a), float(sy)))
    jax.block_until_ready(psi)
    return dict(E=E, V0=V0, R=R, steps=per * (nframes - 1), dt=dt, amp=np.array(F), phase=np.array(P),
                curves=np.array(curves), wall=time.time() - t0)
