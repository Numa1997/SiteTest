"""Fig. 15 correction, discs and shells: the exact reduction to two dimensions (x, rho), and a reference solver for it.

The packet starts on the x axis and flies along it; discs are centred on that axis and shells on the origin, which lies on it.
So psi does not depend on the angle about the axis (m = 0), and with hbar = m = 1
    i d psi/dt = -1/2 (d^2/dx^2 + d^2/drho^2 + (1/rho) d/drho) psi + V(x, rho) psi.
This is the 3D problem, exactly, on a 2D grid.

Scheme: Strang split-step. The kinetic factor exp(-i (kx^2 + krho^2) dt / 2) is applied exactly: FFT along x, and along rho the
quasi-discrete Hankel transform of order 0 (Guizar-Sicairos and Gutierrez-Vega, J. Opt. Soc. Am. A 21, 53 (2004)): with j_n the
zeros of J0, S = j_{N+1}, nodes rho_n = j_n Rmax / S, wave numbers k_n = j_n / Rmax, and the symmetric matrix
    T_mn = 2 J0(j_m j_n / S) / (S |J1(j_m)| |J1(j_n)|),
the scaled field u_n = psi(rho_n) / |J1(j_n)| transforms as u -> T u. T is made exactly orthogonal (T (T^2)^(-1/2)), so the free
step M = T diag(exp(-i k^2 dt/2)) T is unitary. Norm: Int |psi|^2 2 pi rho drho dx = (4 pi Rmax^2 / S^2) sum |u|^2 hx.
V is held as cell averages ('cell': each x cell of width hx and each rho cell between midpoints of nodes, the share of the cell
inside a barrier), or by rt3d2's drawing rules ('rt3d2': V0 on x points strictly inside a barrier; across, the azimuthal average of
the 0.5 a Cartesian staircase disc, which is what the m = 0 wave sees of it).
Absorbing borders: sin^(1/8) on the outer tenth of the x box (as rt3d2) and on the outer Wrho of the rho range. What they absorb is
counted by where it was taken: x < xl (reflected), x > xr (transmitted), between (undecided).
T_ref = P(x > xr) + absorbed(x > xr) + (P(between) + absorbed(between)) / 2 at the end; the undecided half is the uncertainty.
complex128 throughout.
"""
import numpy as np
from scipy.special import jn_zeros, j0, j1

POW = 0.125


def qdht(N, Rmax):
    j = jn_zeros(0, N + 1); S = j[-1]; jn = j[:-1]
    T = 2 * j0(np.outer(jn, jn) / S) / (S * np.outer(np.abs(j1(jn)), np.abs(j1(jn))))
    w, U = np.linalg.eigh(T @ T); T = T @ (U * w ** -0.5) @ U.T       # exactly orthogonal, symmetric
    T = 0.5 * (T + T.T)
    rho = jn * Rmax / S; k = jn / Rmax; J1 = np.abs(j1(jn))
    wq = 4 * np.pi * Rmax**2 / S**2      # sum |u|^2 * wq * hx = Int |psi|^2 dV
    # rho cell edges (midpoints between nodes, 0 at the axis, Rmax at the end), for cell averages
    e = np.r_[0.0, 0.5 * (rho[1:] + rho[:-1]), Rmax]
    return dict(T=T, rho=rho, k=k, J1=J1, wq=wq, edges=e, S=S, Rmax=Rmax)


def border(n, W):
    m = np.ones(n); e = np.arange(W); m[:W] = np.sin(0.5 * np.pi * e / W) ** POW; m[-W:] = m[:W][::-1]; return m


def centres(sp):
    N, P, D = sp["N"], sp["P"], sp["D"]
    for c in (0.0, 0.25):
        cs = [c + (k - (N - 1) / 2) * P for k in range(N)]
        faces = [f for ck in cs for f in (ck - D / 2, ck + D / 2)]
        if all(abs((f - 0.25) / 0.5 - round((f - 0.25) / 0.5)) < 1e-9 for f in faces): return cs
    raise ValueError


def extent(sp):
    if sp["shape"] == "shell":
        Ro = sp["R"] + (sp["N"] - 1) * sp["P"] + sp["D"] / 2; return -Ro, Ro
    cs = centres(sp); return cs[0] - sp["D"] / 2, cs[-1] + sp["D"] / 2


def x0_of(sp):
    return extent(sp)[0] - max(14.0, 4 * sp["sx"])


def overlap(a, b, lo, hi):
    """length of [a, b] inside [lo, hi], elementwise over arrays a, b"""
    return np.clip(np.minimum(b, hi) - np.maximum(a, lo), 0, None)


def staircase_disc_profile(rho, R, h=0.5, nth=720):
    """Azimuthal average of rt3d2's Cartesian disc (cells of the 0.5 grid whose centre lies strictly inside R)."""
    th = (np.arange(nth) + 0.5) * np.pi / 2 / nth
    y = rho[:, None] * np.cos(th)[None]; z = rho[:, None] * np.sin(th)[None]
    yc = np.round(y / h) * h; zc = np.round(z / h) * h
    return ((yc**2 + zc**2) < R**2).mean(1)


def potential(sp, x, hx, Q, rule="cell", sub=8):
    """V(x, rho) on the grid (Nx, Nrho) and the region masks."""
    rho, e = Q["rho"], Q["edges"]; D, V0 = sp["D"], sp["V0"]; xl, xr = extent(sp)
    if sp["shape"] in ("flat", "coin"):
        cs = centres(sp)
        if rule == "rt3d2":
            fx = np.zeros_like(x)
            for c in cs: fx += (np.abs(x - c) < D / 2)
        else:
            fx = sum(overlap(x - hx / 2, x + hx / 2, c - D / 2, c + D / 2) for c in cs) / hx
        if sp["shape"] == "flat": fr = np.ones_like(rho)
        elif rule == "rt3d2": fr = staircase_disc_profile(rho, sp["R"])
        else: fr = np.clip((np.minimum(e[1:], sp["R"])**2 - e[:-1]**2) / (e[1:]**2 - e[:-1]**2), 0, 1)
        V = V0 * fx[:, None] * fr[None, :]
    else:
        Rs = [sp["R"] + k * sp["P"] for k in range(sp["N"])]
        if rule == "rt3d2":
            # the Cartesian staircase: r of the nearest 0.5 grid point; azimuthal average over the cross-section
            th = (np.arange(180) + 0.5) * np.pi / 2 / 180
            yc = np.round(rho[:, None] * np.cos(th) / 0.5) * 0.5; zc = np.round(rho[:, None] * np.sin(th) / 0.5) * 0.5
            r2c = yc**2 + zc**2; xc = np.round((x - 0.0) / 0.5) * 0.5
            rr = np.sqrt(xc[:, None, None]**2 + r2c[None])
            ins = np.zeros(rr.shape, bool)
            for Rc in Rs: ins |= np.abs(rr - Rc) < D / 2
            V = V0 * ins.mean(2)
        else:
            # cell averages by sub x sub sampling, area-weighted in rho
            u = (np.arange(sub) + 0.5) / sub
            xs = (x[:, None] - hx / 2 + hx * u[None])                       # (Nx, sub)
            rs = e[:-1, None] + (e[1:] - e[:-1])[:, None] * u[None]         # (Nr, sub)
            wr = rs / rs.sum(1, keepdims=True)
            r = np.sqrt(xs[:, :, None, None]**2 + rs[None, None]**2)        # (Nx, sub, Nr, sub)
            ins = np.zeros(r.shape, bool)
            for Rc in Rs: ins |= np.abs(r - Rc) < D / 2
            V = V0 * (ins * wr[None, None]).sum(3).mean(1)
    if sp.get("bias"):
        V = V - sp["bias"] * np.clip((x - xl) / (xr - xl), 0, 1)[:, None]
    X = x[:, None]; Rh = rho[None, :]
    if sp["shape"] in ("flat", "coin"):
        cs = centres(sp); slab = np.zeros_like(x, bool)
        for c in cs: slab |= np.abs(x - c) < D / 2
        lat = np.ones_like(rho, bool) if sp["shape"] == "flat" else rho < sp["R"]
        reg = dict(left=np.broadcast_to(X < xl, V.shape), right=np.broadcast_to(X > xr, V.shape))
        if len(cs) > 1:
            reg["well"] = ((x > cs[0] + D / 2) & (x < cs[-1] - D / 2) & ~slab)[:, None] & lat[None, :]
    else:
        Rs = [sp["R"] + k * sp["P"] for k in range(sp["N"])]; r = np.sqrt(X**2 + Rh**2)
        ins = np.zeros(r.shape, bool)
        for Rc in Rs: ins |= np.abs(r - Rc) < D / 2
        reg = dict(core=r < Rs[0] - D / 2, out=r > Rs[-1] + D / 2)
        if len(Rs) > 1: reg["gap"] = (r > Rs[0] + D / 2) & (r < Rs[-1] - D / 2) & ~ins
    side = dict(L=np.broadcast_to(X < xl, V.shape), R=np.broadcast_to(X > xr, V.shape))
    side["M"] = ~(side["L"] | side["R"])
    return V, reg, side


def run(sp, t_end, hx=0.125, Lx=None, Nr=160, Rmax=40.0, Wr=8.0, dt=0.01, nframes=200, rule="cell", keep_frames=False):
    Lx = Lx or sp["Nx"] * 0.5
    Nx = int(round(Lx / hx)); x = (np.arange(Nx) - Nx // 2) * hx
    kx = 2 * np.pi * np.fft.fftfreq(Nx, hx)
    Q = qdht(Nr, Rmax); rho = Q["rho"]
    mx = border(Nx, max(4, Nx // 10)); mr = np.ones(Nr); W = rho > Rmax - Wr
    nW = int(W.sum()); e = np.arange(nW)[::-1]; mr[W] = np.sin(0.5 * np.pi * e / nW) ** POW
    mask = mx[:, None] * mr[None, :]
    V, reg, side = potential(sp, x, hx, Q, rule)
    k0 = np.sqrt(2 * sp["E"]); x0 = x0_of(sp)
    psi = np.exp(-(x[:, None] - x0)**2 / (4 * sp["sx"]**2) - rho[None, :]**2 / (4 * sp["sp"]**2) + 1j * k0 * x[:, None])
    u = psi / Q["J1"][None, :]
    wq = Q["wq"] * hx
    u /= np.sqrt((np.abs(u)**2).sum() * wq)
    inside = V > 0.5 * sp["V0"] if sp["V0"] > 0 else np.zeros_like(V, bool)
    start_in_barrier = float((np.abs(u)**2 * (V != 0) * (np.abs(V) > 0)).sum() * wq) if not sp.get("bias") else None
    hv = np.exp(-0.5j * V * dt)
    Mr = Q["T"] @ (np.exp(-0.5j * Q["k"]**2 * dt)[:, None] * Q["T"])
    Dx = np.exp(-0.5j * kx**2 * dt)[:, None]
    steps = int(round(t_end / dt)); per = max(1, steps // (nframes - 1))
    absorbed = dict(L=0.0, R=0.0, M=0.0); absorbed_r = dict(L=0.0, R=0.0, M=0.0)
    curves = []; frames = []
    names = ["t", "norm"] + sorted(reg) + ["absL", "absR", "absM"]
    rho2 = lambda a: np.abs(a)**2 * wq
    for f in range(nframes):
        for _ in range(per if f else 0):
            u = hv * u
            u = np.fft.ifft(Dx * np.fft.fft(u, axis=0), axis=0) @ Mr
            u = hv * u
            before = np.abs(u)**2
            u = u * mask
            lost = (before - np.abs(u)**2) * wq
            for s_, m in side.items(): absorbed[s_] += float(lost[m].sum())
        d = rho2(u)
        curves.append([f * per * dt, float(d.sum())] + [float(d[m].sum()) for _, m in sorted(reg.items())] +
                      [absorbed["L"], absorbed["R"], absorbed["M"]])
        if keep_frames: frames.append((u * Q["J1"][None, :]).copy())
    C = np.array(curves)
    cn = {n: C[:, i] for i, n in enumerate(names)}
    d = rho2(u); P_R = float(d[side["R"]].sum()); P_M = float(d[side["M"]].sum())
    T = P_R + absorbed["R"] + 0.5 * (P_M + absorbed["M"])
    out = dict(T=T, T_unc=0.5 * (P_M + absorbed["M"]), curves=C, names=names, x=x, rho=rho, steps=per * (nframes - 1),
               frame_dt=per * dt, wq=wq, V=V, start_in_barrier=start_in_barrier)
    if keep_frames: out["frames"] = frames
    return out
