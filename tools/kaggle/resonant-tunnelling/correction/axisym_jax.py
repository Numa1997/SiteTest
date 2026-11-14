"""Fig. 15 correction, discs and shells: the axisymmetric (x, rho) solver of axisym.py in JAX, for the GPU (and CPU checks).

Same scheme and setup as axisym.run (read its docstring): Strang split-step, FFT along x, the orthogonal QDHT step M along rho,
cell-averaged V, sin^(1/8) borders; what the borders absorb is counted by side (x < xl, x > xr, between). Additions:
  - frames: the half-plane rho >= 0 at the stored frame times, |psi| and arg psi on the page's output points (x on the stored 0.5 a
    grid, rho = 0, 0.5, ..., 31.5), interpolated from the solver grid in rho by the exact Bessel series of the QDHT (band-limited),
    and taken from the fine x grid at the coinciding points;
  - the x-profile p(x, t) = Int |psi|^2 2 pi rho drho on the stored 0.5 a points (fine-grid cell sums);
  - the norm drift, measured: sum |u|^2 + absorbed, which must stay 1.
dtype: complex128 (x64) or complex64.
"""
import time
import numpy as np
import jax, jax.numpy as jnp
from scipy.special import j0
import axisym as ax


def bessel_rows(Q, rho_out):
    """Matrix B (len(rho_out) x Nr) with psi(rho_out) = B @ psi_nodes for a field band-limited to the QDHT's wave numbers:
    psi(rho) = sum_m Psi_m J0(k_m rho), Psi = T-transform of the scaled nodes."""
    # scaled nodes u_n = psi_n / J1_n ; spectrum (scaled) U = T u ; psi(rho) = sum_m c_m U_m J0(k_m rho), with c_m chosen so
    # that psi(rho_n) = psi_n reproduces: c_m = 2 / (Rmax^2 ... ) -> build by solving on the nodes instead (exact interpolation)
    Jn = j0(np.outer(Q["rho"], Q["k"]))               # (Nr, Nr): psi_nodes = Jn @ a
    Jo = j0(np.outer(rho_out, Q["k"]))
    return Jo @ np.linalg.solve(Jn, np.eye(len(Q["rho"])))


def run(sp, t_end, hx=0.0625, Lx=None, Nr=160, Rmax=40.0, Wr=8.0, dt=0.01, nframes=200, rule="cell", dtype="c128",
        out_x=None, out_rho=None, frame_dt=None):
    if dtype == "c128": jax.config.update("jax_enable_x64", True)
    cdt = jnp.complex128 if dtype == "c128" else jnp.complex64; rdt = jnp.float64 if dtype == "c128" else jnp.float32
    Lx = Lx or sp["Nx"] * 0.5
    Nx = int(round(Lx / hx)); x = (np.arange(Nx) - Nx // 2) * hx; kx = 2 * np.pi * np.fft.fftfreq(Nx, hx)
    Q = ax.qdht(Nr, Rmax); rho = Q["rho"]
    mx = ax.border(Nx, max(4, Nx // 10)); mr = np.ones(Nr); W = rho > Rmax - Wr
    nW = int(W.sum()); e = np.arange(nW)[::-1]; mr[W] = np.sin(0.5 * np.pi * e / nW) ** ax.POW
    mask = mx[:, None] * mr[None, :]
    V, reg, side = ax.potential(sp, x, hx, Q, rule)
    k0 = np.sqrt(2 * sp["E"]); x0 = ax.x0_of(sp)
    psi = np.exp(-(x[:, None] - x0)**2 / (4 * sp["sx"]**2) - rho[None, :]**2 / (4 * sp["sp"]**2) + 1j * k0 * x[:, None])
    u = psi / Q["J1"][None, :]; wq = Q["wq"] * hx; u /= np.sqrt((np.abs(u)**2).sum() * wq)
    if frame_dt is None:
        steps = int(round(t_end / dt)); per = max(1, steps // (nframes - 1))
    else:
        per = int(round(frame_dt / dt))
    hv = jnp.asarray(np.exp(-0.5j * V * dt), cdt)
    Mr = jnp.asarray(Q["T"] @ (np.exp(-0.5j * Q["k"]**2 * dt)[:, None] * Q["T"]), cdt)
    Dx = jnp.asarray(np.exp(-0.5j * kx**2 * dt)[:, None], cdt)
    M = jnp.asarray(mask, rdt)
    S = {k: jnp.asarray(v, rdt) for k, v in side.items()}; Rg = {k: jnp.asarray(v, rdt) for k, v in reg.items()}

    @jax.jit
    def chunk(u):
        def body(i, c):
            u, aL, aR, aM = c
            u = hv * u; u = jnp.fft.ifft(Dx * jnp.fft.fft(u, axis=0), axis=0) @ Mr; u = hv * u
            b = jnp.abs(u)**2; u = u * M; lost = (b - jnp.abs(u)**2) * wq
            return u, aL + (lost * S["L"]).sum(), aR + (lost * S["R"]).sum(), aM + (lost * S["M"]).sum()
        z = jnp.zeros((), rdt)
        return jax.lax.fori_loop(0, per, body, (u, z, z, z))

    @jax.jit
    def measure(u):
        d = jnp.abs(u)**2 * wq
        return d.sum(), {k: (d * m).sum() for k, m in Rg.items()}, {k: (d * m).sum() for k, m in S.items()}

    # output points
    if out_x is not None:
        ix = np.rint((np.asarray(out_x) - x[0]) / hx).astype(int); assert np.allclose(x[ix], out_x)
        B = jnp.asarray(bessel_rows(Q, np.asarray(out_rho)) * Q["J1"][None, :], cdt)       # acts on scaled u
        IX = jnp.asarray(ix)
    p = jnp.asarray(u, cdt); A = dict(L=0.0, R=0.0, M=0.0)
    curves, frames, profs = [], [], []
    t0 = time.time()
    for f in range(nframes):
        if f:
            p, aL, aR, aM = chunk(p); A["L"] += float(aL); A["R"] += float(aR); A["M"] += float(aM)
        n, rg, sd = jax.device_get(measure(p))
        curves.append([f * per * dt, float(n)] + [float(rg[k]) for k in sorted(reg)] + [A["L"], A["R"], A["M"]])
        if out_x is not None:
            half = (p[IX] @ B.T)                          # (len(out_x), len(out_rho)) complex psi
            frames.append(np.asarray(half))
            line = np.asarray((jnp.abs(p)**2).sum(1)) * wq / hx       # Int |psi|^2 2 pi rho drho at each fine x
            prof = line[ix]
            profs.append(prof)
    wall = time.time() - t0
    C = np.array(curves); names = ["t", "norm"] + sorted(reg) + ["absL", "absR", "absM"]
    last = C[-1]; cn = dict(zip(names, last))
    _, _, sd = jax.device_get(measure(p))
    T = float(sd["R"]) + A["R"] + 0.5 * (float(sd["M"]) + A["M"])
    drift = float(np.max(np.abs(C[:, 1] + C[:, -3] + C[:, -2] + C[:, -1] - 1)))
    return dict(T=T, T_unc=0.5 * (float(sd["M"]) + A["M"]), curves=C, names=names, steps=per * (nframes - 1), frame_dt=per * dt,
                wall=wall, s_per_step=wall / max(1, per * (nframes - 1)), drift=drift, cells=Nx * Nr,
                frames=np.array(frames) if frames else None, profs=np.array(profs) if profs else None)
