# Guinness on a one-wheel cart, computed in JAX on Kaggle's GPU (13 Nov 2026). Everything that moves is computed on the GPU:
# the stout (incompressible Navier-Stokes with a free surface), the drops that leave over the rim, and the cart.
#
# The stout. APIC particles (Jiang et al. 2015) on a staggered grid; the curved glass enters through the open fraction of
# every cell face (Batty, Bertails & Bridson 2007); pressure by preconditioned conjugate gradients so that the velocity is
# divergence-free; the free surface is a level set built from the particles (Zhu & Bridson 2005, kernel 2 dx, radius
# 0.9 dx, with mirror images in the glass wall) and carries p = 0 exactly on the surface by the ghost-fluid rule (Enright,
# Nguyen, Gibou & Fedkiw 2003). Faces closed by the glass take the liquid's velocity by extrapolation (free slip on the grid);
# the thin boundary layer on the glass (0.4 mm, below the grid) brakes the liquid next to the wall at the Stokes-layer
# rate sqrt(nu omega / 2) per unit wall area; viscosity nu on the grid, explicit. Computed in the glass's frame: every
# particle feels gravity minus the glass's acceleration. This is the algorithm of tools/fig12/kaggle/solver.py (v2, Taichi),
# written again in JAX line by line (the function names say which Taichi kernel each one replaces).
#
# Over the rim. A particle that crosses the rim outside the glass's radius leaves the stout: from then on it is a drop in
# free flight (gravity minus the glass's acceleration, in the glass's frame) until it falls 0.25 m below the glass's
# floor; its mass leaves the cart (ml) at that instant.
#
# The cart. A port of Cart in public/scripts/stout-cart.js (and of the Python port in solver.py), in float64 on the GPU,
# sub-stepped at 0.1 ms inside each fluid step; the stout pushes back on it with F = -dP/dt (P the stout's momentum
# relative to the glass), so cart and stout are one coupled solution.
#
# Precision: the fluid in float32 (the T4 does float64 at 1/32 speed), sums of the conjugate gradient and of the books in
# float64, the cart in float64.
import math
import numpy as np
import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp
from jax import lax

F32, F64, I32 = jnp.float32, jnp.float64, jnp.int32

NU_STOUT = 2.06e-3 / 1007.0   # m^2/s: Guinness at 6 C, mu = 2.06e-3 Pa s, rho = 1007 kg/m^3 (Benilov, Cummins & Lee, arXiv 1205.5233, sec. II)
MU_STOUT = 2.06e-3
OMEGA = 2 * math.pi * 3.42     # rad/s, the first sloshing mode: sets the Stokes layer, sqrt(2 nu / omega) = 0.44 mm
MODELS = {
    # no friction and no head: what the numerical method alone loses (used to measure numerical damping)
    "inviscid": dict(nu=0.0, wall=False, skin=False, head=False),
    # the stout's viscosity and the glass's boundary layer, clean surface, no head
    "wall": dict(nu=NU_STOUT, wall=True, skin=False, head=False),
    # the whole model (notes/fig12/research/verification.md): viscosity, the glass's boundary layer, the surface that cannot stretch
    # (protein skin, or the head as a lid), and the head of foam: its weight on the stout, its friction on the glass, its spilling
    "full": dict(nu=NU_STOUT, wall=True, skin=True, head=True),
}
# The head of foam: every number from notes/fig12/research/data-for-solver.md (13 Nov 2026).
HEAD0 = 0.019        # m, the head as served: 18-20 mm specification; 17.5-22.2 mm measured two minutes after pouring (KegWorks 2019)
GAMMA = 0.0442       # N/m, surface tension of degassed Guinness, 20 C, pendant drop (Voelp & Willenbacher 2021, Table 2)
E_INF = 0.0187       # N/m, its surface dilatational elasticity (same table)
RBUB = 34e-6         # m, Sauter radius of the head's bubbles: the stout's own (mean diameter 61 um, log-normal sigma 0.24; Watamura 2019)
PHI_F = 0.27         # liquid fraction of the head: 0.24-0.36 from the column equilibrium and its slow drainage (data-for-solver.md)
GAS = 1.0 - PHI_F
PHI_C = 0.635        # gas fraction at jamming (Voelp & Willenbacher 2021)
P_GEN = (GAMMA + 2.0 * E_INF) / RBUB                     # Pa, the generalized Laplace pressure, 2400 Pa
G_HEAD = 1.0 * P_GEN * GAS * (GAS - PHI_C)                # Pa, shear modulus, 166 Pa (a_d = 1)
TAU_Y = 0.25 * P_GEN * (GAS - PHI_C) ** 2                 # Pa, yield stress, 5.4 Pa (k_d = 0.25)
# Wall friction of the head (Cantat, Phys. Fluids 25, 031303 (2013), eq. 18-49; stiff protein surfaces, the sliding branch), with
# her fitted prefactor Z and meniscus ratio l/r_m against liquid fraction (her Fig. 14, data of Marze et al.; held at the 0.25
# values beyond 0.25). Checked: the same law predicts Viola et al. 2016's measured foam damping within 4-11 %.
_PHI_TAB = np.array([0.10, 0.15, 0.20, 0.25]); _Z_TAB = np.array([0.6, 0.44, 0.32, 0.18]); _LR_TAB = np.array([0.5, 0.25, 0.09, 0.004])
Z_WALL = float(np.interp(PHI_F, _PHI_TAB, _Z_TAB)); LR_WALL = float(np.interp(PHI_F, _PHI_TAB, _LR_TAB))


def head_wall_stress(v):
    """Stress (Pa) of the head's edge sliding on the glass at speed |v| (m/s): the smaller of the sliding law (Cantat 2013) and
    what the foam itself can carry, its yield stress plus its viscous stress (Tcholakova et al., PRE 78, 011405 (2008), eq. 48b)
    in a layer one bubble diameter thick."""
    v = jnp.abs(v); Ca = MU_STOUT * v / GAMMA
    slide = Z_WALL * GAMMA / RBUB * (6.82 * Ca ** (2.0 / 3.0) + 0.94 * LR_WALL * Ca ** (1.0 / 3.0))
    Cas = MU_STOUT * v / (2.0 * GAMMA)
    carry = TAU_Y + GAMMA / RBUB * 0.7 * Cas ** 0.47 * GAS ** (5.0 / 6.0) / PHI_F ** 0.5   # films term, eq. 54 (as data-for-solver.md)
    return jnp.minimum(slide, carry)


# ====================================================================== geometry (built once, before the run)
class Geometry:
    """The glass on the grid: open fractions of every face, wall area per cell, masks. Cell (i, j, k) has its centre at
    (x0 + (i + 1/2) dx, x0 + (j + 1/2) dx, z0 + (k + 1/2) dx); z0 = -2 dx (two cells of glass below the floor)."""

    def __init__(self, R, dzp, fill, dx):
        R = np.asarray(R, float); self.R = R; self.dzp = dzp; self.fill = fill; self.dx = dx; self.nR = len(R)
        self.zrim = (len(R) - 1) * dzp; Rmax = R.max()
        self.n = n = int(math.ceil(2 * (Rmax + 2 * dx) / dx)); self.nz = nz = int(math.ceil((self.zrim + 0.02) / dx)) + 2
        self.x0 = -n * dx / 2; self.z0 = -2 * dx
        s = (np.arange(4) + 0.5) / 4
        xs4 = self.x0 + dx * (np.arange(n)[:, None] + s[None, :]).ravel()      # 4 samples across each cell
        zs4 = self.z0 + dx * (np.arange(nz)[:, None] + s[None, :]).ravel()
        xf = self.x0 + dx * np.arange(n + 1); zf = self.z0 + dx * np.arange(nz + 1)
        ins = self.inside
        thu = ins(xf[:, None, None], xs4[None, :, None], zs4[None, None, :]).reshape(n + 1, n, 4, nz, 4).mean((2, 4))
        thv = ins(xs4[:, None, None], xf[None, :, None], zs4[None, None, :]).reshape(n, 4, n + 1, nz, 4).mean((1, 4))
        thw = ins(xs4[:, None, None], xs4[None, :, None], zf[None, None, :]).reshape(n, 4, n, 4, nz + 1).mean((1, 3))
        thu[0] = thu[-1] = 0; thv[:, 0] = thv[:, -1] = 0; thw[:, :, 0] = 0      # the box is closed except its top
        self.thu, self.thv, self.thw = thu, thv, thw
        c = self.x0 + (np.arange(n) + 0.5) * dx; zc = self.z0 + (np.arange(nz) + 0.5) * dx
        X, Y, Z = np.meshgrid(c, c, zc, indexing="ij"); r2 = X * X + Y * Y
        self.xc, self.zc = c, zc
        Rcav = self.Rz(np.minimum(Z, self.zrim - 1e-6))
        self.cav_inner = (Z > 0) & (r2 < (Rcav - 0.5 * dx) ** 2)                       # well inside the cavity
        self.wallcut = (Z > 0) & (Z < self.zrim) & (r2 >= (self.Rz(Z) - 0.5 * dx) ** 2)   # cut by the glass
        self.cavc = ins(X, Y, Z)                                                       # centre inside the cavity
        self._wall_area()
        self.Rfill = float(self.Rz(fill))

    def Rz(self, z):
        f = np.clip(np.asarray(z) / self.dzp, 0.0, self.nR - 1.001)
        return np.interp(f, np.arange(self.nR), self.R)

    def inside(self, x, y, z):
        z = np.asarray(z, float)
        return ((z > 0) & ((z >= self.zrim) | (x * x + y * y < self.Rz(z) ** 2))).astype(float)

    def _wall_area(self):
        """Area of glass inside each cell, per cell volume (as solver.py): the side wall of each layer, 2 pi R ds, shared by
        the layer's cells cut by it; the floor gives the cells above it dx^2 times their bottom's part inside the glass."""
        n, nz, dx, R, dzp = self.n, self.nz, self.dx, self.R, self.dzp
        s = (np.arange(4) + 0.5) / 4
        xc = self.x0 + dx * (np.arange(n)[:, None] + s[None, :])
        r2 = xc[:, None, :, None] ** 2 + xc[None, :, None, :] ** 2
        zp = np.arange(len(R)) * dzp; ds = np.sqrt(dzp ** 2 + np.diff(R) ** 2)
        A = np.zeros((n, n, nz))
        for k in range(nz):
            za, zb = self.z0 + k * dx, self.z0 + (k + 1) * dx
            inside = np.zeros((n, n)); tot = 0
            for c in s:
                z = za + c * dx
                if z <= 0: continue
                Rz = float(self.Rz(min(z, self.zrim)))
                inside += (r2 < Rz * Rz).reshape(n, n, 16).sum(2); tot += 16
            if tot == 0: continue
            frac = inside / (4 * 16); cut = (frac > 0) & (frac < 1)
            a, b = max(za, 0.0), min(zb, self.zrim)
            if b > a and cut.any():
                m = (zp[:-1] + 0.5 * dzp > a) & (zp[:-1] + 0.5 * dzp <= b)
                side = float((2 * np.pi * 0.5 * (R[:-1] + R[1:]) * ds)[m].sum())
                A[:, :, k] += np.where(cut, side / cut.sum(), 0.0)
            if k == 2:
                A[:, :, k] += (r2 < R[0] ** 2).reshape(n, n, 16).mean(2) * dx * dx
        a = A / dx ** 3
        pad = lambda arr, ax: np.concatenate([np.take(arr, [0], ax) * 0, arr, np.take(arr, [0], ax) * 0], ax)
        self.ac = a
        self.au = np.where(self.thu > 0, 0.5 * (pad(a, 0)[:-1] + pad(a, 0)[1:]), 0)
        self.av = np.where(self.thv > 0, 0.5 * (pad(a, 1)[:, :-1] + pad(a, 1)[:, 1:]), 0)
        self.aw = np.where(self.thw > 0, 0.5 * (pad(a, 2)[:, :, :-1] + pad(a, 2)[:, :, 1:]), 0)
        self.area_cells = float(A.sum())
        self.area_profile = float((2 * np.pi * 0.5 * (R[:-1] + R[1:]) * ds).sum() + np.pi * R[0] ** 2)


def glass_volume(R, dzp, fill, n=20000):
    z = np.linspace(0, fill, n + 1); r = np.interp(z / dzp, np.arange(len(R)), R)
    return float(np.trapezoid(np.pi * r * r, z) if hasattr(np, "trapezoid") else np.trapz(np.pi * r * r, z))


def seed_particles(G, ppc=2, seed=1):
    """ppc^3 particles per cell inside the glass below the fill, jittered (as solver.py)."""
    rng = np.random.default_rng(seed); h = G.dx / ppc; pts = []
    xs = G.x0 + h * (np.arange(int(G.n * ppc)) + 0.5); zs = np.arange(h / 2, G.fill, h)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    for z in zs:
        Rz = float(G.Rz(z)); m = X * X + Y * Y < (Rz - 0.25 * h) ** 2
        pts.append(np.stack([X[m], Y[m], np.full(m.sum(), z)], 1))
    P = np.concatenate(pts); P = P + rng.uniform(-0.3 * h, 0.3 * h, P.shape)
    P[:, 2] = np.clip(P[:, 2], 0.2 * h, G.fill - 0.2 * h)
    return P


# ====================================================================== shifted arrays
def sh(a, d, ax, fill=0):
    """out[..., i, ...] = a[..., i + d, ...] along axis ax; `fill` where i + d falls outside."""
    L = a.shape[ax]; pw = [(0, 0)] * a.ndim
    if d > 0:
        pw[ax] = (0, d); return lax.slice_in_dim(jnp.pad(a, pw, constant_values=fill), d, d + L, axis=ax)
    pw[ax] = (-d, 0); return lax.slice_in_dim(jnp.pad(a, pw, constant_values=fill), 0, L, axis=ax)


def lo(a, ax, fill):   # face-shaped array of the cell on the low side of each face (index i -> cell i - 1)
    pw = [(0, 0)] * a.ndim; pw[ax] = (1, 0); return jnp.pad(a, pw, constant_values=fill)


def hi(a, ax, fill):   # face-shaped array of the cell on the high side of each face (index i -> cell i)
    pw = [(0, 0)] * a.ndim; pw[ax] = (0, 1); return jnp.pad(a, pw, constant_values=fill)


def cut_hi(f, ax):     # the face above each cell (index i + 1), cell-shaped
    return lax.slice_in_dim(f, 1, f.shape[ax], axis=ax)


def cut_lo(f, ax):     # the face below each cell (index i), cell-shaped
    return lax.slice_in_dim(f, 0, f.shape[ax] - 1, axis=ax)


# ====================================================================== the solver
class Stout:
    def __init__(self, G, model="full", ppc=2, seed=1, rho=1007.0, K_frac=0.35, M_drops=4096, tol=1e-5, maxit=600):
        self.G = G; self.rho = rho; self.ppc = ppc
        M = MODELS[model]; self.model = model
        self.nu = M["nu"]; self.gs = math.sqrt(M["nu"] * OMEGA / 2) if M["wall"] else 0.0
        self.skin = M["skin"]
        dx = G.dx; self.dx = dx; self.Hb = 2.0 * dx; self.rls = 0.9 * dx; self.tol = tol; self.maxit = maxit
        n, nz = G.n, G.nz; self.n, self.nz = n, nz
        self.dims = (n, n, nz)
        self.fshape = [(n + 1, n, nz), (n, n + 1, nz), (n, n, nz + 1)]
        P = seed_particles(G, ppc, seed)
        self.N = len(P); self.V = glass_volume(G.R, G.dzp, G.fill); self.mp = rho * self.V / self.N
        self.K = int(K_frac * self.N); self.M = M_drops
        self.P0 = P.astype(np.float32)
        f = lambda a: jnp.asarray(a, F32)
        self.th = [f(G.thu), f(G.thv), f(G.thw)]; self.af = [f(G.au), f(G.av), f(G.aw)]; self.ac = f(G.ac)
        self.cav_inner = jnp.asarray(G.cav_inner); self.wallcut = jnp.asarray(G.wallcut); self.cavc = jnp.asarray(G.cavc > 0)
        self.Rd = jnp.asarray(G.R, F32)
        self.origin = jnp.asarray([G.x0, G.x0, G.z0], F32)
        k = np.arange(nz + 1)[None, None, :]
        self.floor_w = jnp.asarray((G.thw == 0) & (k <= 2))       # closed floor faces: w = 0 exactly
        c = jnp.asarray(G.xc, F32); zc = jnp.asarray(G.zc, F32)
        self.cc = (c, c, zc)
        o = np.array([(a, b, c) for a in range(-1, 3) for b in range(-1, 3) for c in range(-1, 3)], np.int32)
        self.off64 = jnp.asarray(o)
        self.corners = jnp.asarray(np.array([(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)], np.int32))
        # the head of foam lives on the columns of the grid (n x n), as a thickness h_f on top of the stout's surface
        self.head = M["head"]; self.rho_f = PHI_F * rho
        X, Y = np.meshgrid(G.xc, G.xc, indexing="ij")
        self.rc = jnp.asarray(np.hypot(X, Y), F32); self.colx = jnp.asarray(X, F32); self.coly = jnp.asarray(Y, F32)
        self.ell = G.Rfill / 1.84118         # m, the depth over which the foam's sliding speed dies away upward, 1/k (Sauret 2015)
        self.Rrim = float(G.Rz(G.zrim - 1e-6))
        self.MF = 4096                       # lumps of head in flight, at most

    # ---------------------------------------------------------------- state
    def init_state(self):
        N = self.N; G = self.G
        hf0 = jnp.where(self.rc < G.Rfill, HEAD0 if self.head else 0.0, 0.0).astype(F32)
        z64 = jnp.zeros((), F64)
        return dict(xp=jnp.asarray(self.P0), vp=jnp.zeros((N, 3), F32), C=jnp.zeros((N, 3, 3), F32),
                    act=jnp.ones(N, bool), fly=jnp.zeros(N, bool), landed=jnp.zeros(N, bool),
                    p=jnp.zeros(self.dims, F32), ewall=z64, efoam=z64, eskin=z64,
                    hf=hf0, foam_spill=z64, foam0=jnp.sum(hf0.astype(F64)) * self.dx ** 2,
                    bx=jnp.full((self.MF, 3), jnp.nan, F32), bv=jnp.zeros((self.MF, 3), F32), bvol=jnp.zeros(self.MF, F32),
                    bptr=jnp.zeros((), I32))

    def heff(self, hf):
        """Height of glass over which a head of thickness hf slides, weighted by its sliding speed to the power 5/3."""
        return 0.6 * self.ell * (1.0 - jnp.exp(-5.0 * hf / (3.0 * self.ell)))

    # ---------------------------------------------------------------- helpers
    def Rz(self, z):
        f = jnp.clip(z / self.G.dzp, 0.0, self.G.nR - 1.001); i = jnp.floor(f).astype(I32)
        return self.Rd[i] + (f - i) * (self.Rd[i + 1] - self.Rd[i])

    def flat(self, idx, shape):   # (..., 3) int -> flat index, and whether it lies inside `shape`
        ok = (idx[..., 0] >= 0) & (idx[..., 0] < shape[0]) & (idx[..., 1] >= 0) & (idx[..., 1] < shape[1]) & (idx[..., 2] >= 0) & (idx[..., 2] < shape[2])
        fl = (idx[..., 0] * shape[1] + idx[..., 1]) * shape[2] + idx[..., 2]
        return jnp.where(ok, fl, 0), ok

    def _corners(self, g, comp, shape):
        off = jnp.full(3, 0.5, F32).at[comp].set(0.0)
        gg = g - off; base = jnp.floor(gg).astype(I32); fr = gg - base
        node = base[None, :, :] + self.corners[:, None, :]                      # (8, N, 3)
        cf = self.corners.astype(F32)[:, None, :]
        wv = jnp.where(cf > 0, fr[None], 1 - fr[None])                          # (8, N, 3)
        w = wv[..., 0] * wv[..., 1] * wv[..., 2]
        fl, ok = self.flat(node, shape)
        return fl, ok, w, wv, cf, fr

    # ---------------------------------------------------------------- particles to grid (Taichi p2g)
    def p2g(self, s):
        dx = self.dx; X, V, C, act = s["xp"], s["vp"], s["C"], s["act"]
        g = (X - self.origin) / dx
        ci = jnp.floor(g).astype(I32); cfl, cok = self.flat(ci, self.dims)
        cnt = jnp.zeros(math.prod(self.dims), I32).at[cfl].add((cok & act).astype(I32)).reshape(self.dims)
        vel, mass = [], []
        for comp in range(3):
            shape = self.fshape[comp]
            fl, ok, w, wv, cf, fr = self._corners(g, comp, shape)
            dpos = (cf - fr[None]) * dx                                         # (8, N, 3)
            val = w * (V[None, :, comp] + jnp.sum(C[None, :, comp, :] * dpos, -1))
            m = ok & act[None]
            upd = jnp.stack([jnp.where(m, val, 0.0), jnp.where(m, w, 0.0)], -1).reshape(-1, 2)
            acc = jnp.zeros((math.prod(shape), 2), F32).at[fl.reshape(-1)].add(upd)
            vel.append(acc[:, 0].reshape(shape)); mass.append(acc[:, 1].reshape(shape))
        return vel, mass, cnt

    def normalize_force(self, vel, mass, dt, gx, gz):
        out = []
        for comp in range(3):
            f = vel[comp] / jnp.maximum(mass[comp], 1e-30)
            f = f + dt * (gx if comp == 0 else (gz if comp == 2 else 0.0))
            out.append(jnp.where((mass[comp] > 1e-6) & (self.th[comp] > 0), f, 0.0).astype(F32))
        return out

    # ---------------------------------------------------------------- level set of the liquid (Taichi level_set)
    def dilate(self, m):
        for ax in range(3):
            m = m | sh(m, 1, ax, False) | sh(m, 2, ax, False) | sh(m, -1, ax, False) | sh(m, -2, ax, False)
        return m

    def level_set(self, s, cnt):
        dx = self.dx; G = self.G
        mA = (cnt == 0) & self.cav_inner
        near = self.dilate(mA); nearP = self.dilate(near)
        X, act = s["xp"], s["act"]
        ci = jnp.floor((X - self.origin) / dx).astype(I32); cfl, cok = self.flat(ci, self.dims)
        sel_mask = act & cok & nearP.reshape(-1)[cfl]
        nsel = jnp.sum(sel_mask, dtype=I32)
        sel = jnp.nonzero(sel_mask, size=self.K, fill_value=0)[0]
        valid = jnp.arange(self.K) < nsel
        Q = X[sel]
        rr = jnp.sqrt(Q[:, 0] ** 2 + Q[:, 1] ** 2); Rw = self.Rz(Q[:, 2])
        img = (Q[:, 2] < G.zrim) & (rr > Rw - 2.0 * dx) & (rr > 1e-9)
        fw = jnp.where(rr > 1e-9, (2.0 * Rw - rr) / jnp.maximum(rr, 1e-9), 0.0)
        Q2 = jnp.stack([Q[:, 0] * fw, Q[:, 1] * fw, Q[:, 2]], -1)
        R2 = 4.0 * dx * dx; size = math.prod(self.dims)
        W = jnp.zeros(size, F32); S = jnp.zeros((size, 3), F32)
        nearf = near.reshape(-1)
        for q, ok_q in ((Q, valid), (Q2, valid & img)):
            qi = jnp.floor((q - self.origin) / dx - 0.5).astype(I32)
            J = qi[:, None, :] + self.off64[None]                                  # (K, 64, 3)
            fl, ok = self.flat(J, self.dims)
            xcJ = self.origin + (J.astype(F32) + 0.5) * dx
            dd = q[:, None, :] - xcJ; d2 = jnp.sum(dd * dd, -1)
            use = ok & ok_q[:, None] & nearf[fl] & (d2 < R2)
            qq = 1.0 - d2 / R2; wt = jnp.where(use, qq * qq * qq, 0.0)
            W = W.at[fl.reshape(-1)].add(wt.reshape(-1))
            S = S.at[fl.reshape(-1)].add((wt[..., None] * dd).reshape(-1, 3))
        W = W.reshape(self.dims); S = S.reshape(self.dims + (3,))
        has = W > 1e-12
        ph_near = jnp.where(has, jnp.sqrt(jnp.sum((S / jnp.where(has, W, 1.0)[..., None]) ** 2, -1)) - self.rls, 3.0 * dx)
        ph = jnp.where(near, ph_near, jnp.where(cnt > 0, -2.0 * dx, 2.0 * dx))
        liq = (ph < 0) | (cnt > 0)
        ph = jnp.where((cnt > 0) & (ph >= 0), -0.05 * dx, ph).astype(F32)
        thu, thv, thw = self.th
        for _ in range(3):   # Taichi ls_inherit: cells cut by the glass that read as air take the liquid's phi beside them
            best = jnp.ones(self.dims, F32)
            for ax, th in ((0, thu), (1, thv)):
                best = jnp.minimum(best, jnp.where((cut_lo(th, ax) > 0) & sh(liq, -1, ax, False), sh(ph, -1, ax, 1.0), 1.0))
                best = jnp.minimum(best, jnp.where((cut_hi(th, ax) > 0) & sh(liq, 1, ax, False), sh(ph, 1, ax, 1.0), 1.0))
            above = sh(ph, 1, 2, 1.0)
            best = jnp.minimum(best, jnp.where((cut_hi(thw, 2) > 0) & sh(liq, 1, 2, False) & (above < -0.5 * dx), above, 1.0))
            take = (~liq) & self.wallcut & (best < 1.0)
            liq = liq | take; ph = jnp.where(take, jnp.minimum(best, -0.05 * dx), ph)
        return ph, liq, nsel

    # ---------------------------------------------------------------- viscosity and friction (Taichi viscosity, friction)
    def viscosity(self, vel, mass, dt):
        c = self.nu * dt / self.dx ** 2; out = []
        for comp in range(3):
            f = vel[comp]; ok = (self.th[comp] > 0) & (mass[comp] > 1e-6); lap = jnp.zeros_like(f)
            for ax in range(3):
                for d in (-1, 1):
                    lap = lap + jnp.where(sh(ok, d, ax, False), sh(f, d, ax, 0.0) - f, 0.0)
            out.append(jnp.where(ok, f + c * lap, f))
        return out

    def friction(self, vel, mass, ph, liq, dt, hf):
        """The three thin layers the 1.5 mm grid cannot resolve, as stresses on the faces next to them (verification.md, items 2, 3, 5):
        - the glass: the Stokes-layer stress rho sqrt(nu omega/2) u on the glass's area in each cut cell;
        - the surface that cannot stretch (protein skin, or the head held still by the glass): the same stress on the horizontal
          velocity of the faces of the top liquid cells, over one cell's area per cell;
        - the head's edge sliding up and down the glass: the head's wall stress (head_wall_stress) on the vertical velocity of the
          liquid in the top two cells next to the glass, over the head's effective height, clamped so that it can stop the motion
          but never reverse it.
        Returns the velocities and the energy each one took (J)."""
        dx = self.dx; dV = self.rho * dx ** 3; z = jnp.zeros((), F64); ew, es, ef = z, z, z; out = []
        top = liq & ~sh(liq, 1, 2, False)                                    # liquid cells with air above
        band = liq & (self.ac > 0) & (ph >= -self.Hb) & (hf[:, :, None] > 0)  # where the head's edge meets the glass
        aeff = (self.heff(hf) / self.Hb)[:, :, None]                         # the head's sliding height packed into the band
        for comp in range(3):
            u0 = vel[comp]; ok = (self.th[comp] > 0) & (mass[comp] > 1e-6); u = u0
            if self.gs > 0:                                                   # glass
                g = self.gs * self.af[comp]; u = jnp.where(ok & (g > 0), u * jnp.exp(-g * dt), u)
                ew = ew + 0.5 * dV * jnp.sum(jnp.where(ok, u0 * u0 - u * u, 0.0).astype(F64))
            if self.skin and comp < 2:                                        # surface that cannot stretch
                u1 = u; tf = lo(top, comp, False) | hi(top, comp, False)
                u = jnp.where(ok & tf, u * jnp.exp(-self.gs / dx * dt), u)
                es = es + 0.5 * dV * jnp.sum(jnp.where(ok, u1 * u1 - u * u, 0.0).astype(F64))
            if self.head and comp == 2:                                       # the head's edge on the glass
                u1 = u; bf = lo(band, 2, False) | hi(band, 2, False)
                a3 = 0.5 * (lo(aeff * jnp.ones(self.dims, F32), 2, 0.0) + hi(aeff * jnp.ones(self.dims, F32), 2, 0.0))
                dv = dt * head_wall_stress(u) * self.af[2] * a3 / self.rho
                u = jnp.where(ok & bf, jnp.sign(u) * jnp.maximum(jnp.abs(u) - dv, 0.0), u)
                ef = ef + 0.5 * dV * jnp.sum(jnp.where(ok, u1 * u1 - u * u, 0.0).astype(F64))
            out.append(u.astype(F32))
        return out, ew, es, ef

    def surface(self, ph, liq):
        """The free surface of the main body of stout, as a height on the grid's columns: in each column, the first air cell
        above liquid that rests on the bottom, and the zero of the level set between it and the liquid cell below it."""
        dx = self.dx
        air = self.cavc & ~liq
        seen = lax.cummax(liq.astype(I32), axis=2) > 0
        cand = air & sh(seen, -1, 2, False)
        has = jnp.any(cand, 2); k = jnp.argmax(cand, 2); kb = jnp.maximum(k - 1, 0)
        pa = jnp.take_along_axis(ph, k[..., None], 2)[..., 0]; pb = jnp.take_along_axis(ph, kb[..., None], 2)[..., 0]
        frac = jnp.clip(pb / jnp.where(pa - pb > 1e-12, pa - pb, 1.0), 0.0, 1.0)
        frac = jnp.where((pa - pb > 1e-12) & (pb < 0), frac, 0.5)
        H = jnp.where(has, self.cc[2][kb] + frac * dx, jnp.nan)
        return jnp.where(jnp.any(liq & self.cavc, 2), H, jnp.nan).astype(F32)

    def head_spill(self, s, H, dt, gx, gz):
        """The head above the rim (verification.md, item 6): where the head's top stands e above the rim, at the glass, the part
        above the rim breaks away once its weight and outward push beat its strength, rho_f (|g_eff| e/2 + a_out e) >= tau_y.
        It leaves as a lump in free flight. Lumps already flying move under gravity minus the glass's acceleration."""
        G = self.G; dx = self.dx; hf = s["hf"]
        ok = jnp.isfinite(H)
        Hs = jnp.where(ok, H, 0.0)
        atwall = ok & (self.rc >= self.Rz(Hs) - 1.5 * dx)
        e = jnp.where(atwall, Hs + hf - G.zrim, 0.0)
        aout = gx * self.colx / jnp.maximum(self.rc, 1e-9)                   # outward push per unit mass in the glass's frame
        fail = (e > 0) & (hf > 0) & (self.rho_f * (jnp.abs(gz) * 0.5 + jnp.maximum(aout, 0.0)) * e >= TAU_Y)
        cut = jnp.where(fail, jnp.minimum(e, hf), 0.0)
        # lumps: one per breaking column, at the rim, starting at rest relative to the glass
        m = cut.reshape(-1) > 0; nnew = jnp.sum(m, dtype=I32)
        rank = jnp.cumsum(m.astype(I32)) - 1
        slot = jnp.where(m, (s["bptr"] + rank) % self.MF, self.MF)            # MF = out of range: dropped by mode="drop"
        sc = self.Rrim / jnp.maximum(self.rc.reshape(-1), 1e-9)
        pos = jnp.stack([self.colx.reshape(-1) * sc, self.coly.reshape(-1) * sc, G.zrim + 0.5 * cut.reshape(-1)], -1)
        bx = s["bx"].at[slot].set(pos.astype(F32), mode="drop"); bv = s["bv"].at[slot].set(0.0, mode="drop")
        bvol = s["bvol"].at[slot].set((cut.reshape(-1) * dx * dx).astype(F32), mode="drop")
        flying = jnp.isfinite(bx[:, 2]) & (bx[:, 2] > -0.25)
        bv = jnp.where(flying[:, None], bv + dt * jnp.array([gx, 0.0, gz], F32), bv)
        bx = jnp.where(flying[:, None], bx + dt * bv, bx)
        return dict(s, hf=(hf - cut).astype(F32), bx=bx, bv=bv, bvol=bvol, bptr=(s["bptr"] + nnew) % self.MF,
                    foam_spill=s["foam_spill"] + jnp.sum(cut.astype(F64)) * dx * dx)

    # ---------------------------------------------------------------- pressure (Taichi build, matvec, solve, project)
    def _faces(self, ph, liq, ax):
        liqL, liqR = lo(liq, ax, False), hi(liq, ax, False)
        inL, inR = lo(jnp.ones(self.dims, bool), ax, False), hi(jnp.ones(self.dims, bool), ax, False)
        phL, phR = lo(ph, ax, 0.0), hi(ph, ax, 0.0)
        cLR = inR & (phL - phR < -1e-12); cRL = inL & (phR - phL < -1e-12)
        tLR = jnp.where(cLR, jnp.clip(phL / jnp.where(cLR, phL - phR, -1.0), 0.05, 1.0), 1.0)   # surface's place, L liquid
        tRL = jnp.where(cRL, jnp.clip(phR / jnp.where(cRL, phR - phL, -1.0), 0.05, 1.0), 1.0)   # surface's place, R liquid
        return liqL, liqR, tLR, tRL

    def pressure(self, vel, ph, liq, p_prev, ps):
        """ps: the pressure on the free surface (the weight of the head), in the solver's units (Pa x dt / rho), one value per
        column, set on the air side of the surface. Ghost fluid: p = ps at the surface, so the air neighbour of a liquid cell
        reads p_ghost = p_liq (1 - 1/theta) + ps / theta: the diagonal gets th / theta and the right side th ps / theta."""
        dx = self.dx; diag = jnp.zeros(self.dims, F32); div = jnp.zeros(self.dims, F32); rhs = jnp.zeros(self.dims, F32)
        cp, cm, faces = [], [], []
        ps3 = jnp.broadcast_to(ps[:, :, None], self.dims).astype(F32)
        for ax in range(3):
            th = self.th[ax]; liqL, liqR, tLR, tRL = self._faces(ph, liq, ax); faces.append((liqL, liqR, tLR, tRL))
            open_ = th > 0
            dL = jnp.where(open_, jnp.where(liqR, th, th / tLR), 0.0)
            dR = jnp.where(open_, jnp.where(liqL, th, th / tRL), 0.0)
            diag = diag + cut_hi(dL, ax) + cut_lo(dR, ax)
            psL, psR = lo(ps3, ax, 0.0), hi(ps3, ax, 0.0)
            sL = jnp.where(open_ & liqL & ~liqR, th * psR / tLR, 0.0)      # liquid L, air R: the surface load seen by L
            sR = jnp.where(open_ & liqR & ~liqL, th * psL / tRL, 0.0)
            rhs = rhs + cut_hi(sL, ax) + cut_lo(sR, ax)
            cp.append(cut_hi(th * liqR, ax)); cm.append(cut_lo(th * liqL, ax))
            flux = th * vel[ax]; div = div + cut_hi(flux, ax) - cut_lo(flux, ax)
        A = liq & (diag > 0)
        diag = jnp.where(A, diag, 0.0); cp = [jnp.where(A, c, 0.0) for c in cp]; cm = [jnp.where(A, c, 0.0) for c in cm]
        b = jnp.where(A, -div * dx + rhs, 0.0)
        inv = jnp.where(A, 1.0 / jnp.where(A, diag, 1.0), 0.0)

        def mv(x):
            y = diag * x
            for ax in range(3): y = y - cp[ax] * sh(x, 1, ax, 0.0) - cm[ax] * sh(x, -1, ax, 0.0)
            return y

        dot = lambda a, c: jnp.sum((a * c).astype(F64))
        bn = jnp.max(jnp.abs(b))
        p = jnp.where(A, p_prev, 0.0)
        r = b - mv(p); z = r * inv; d = z; rz = dot(r, z)

        def cond(c):
            p, r, d, rz, it, rn, ok = c
            return (it < self.maxit) & (rn >= self.tol * bn) & ok & (bn > 0)

        def body(c):
            p, r, d, rz, it, rn, ok = c
            q = mv(d); dq = dot(d, q); good = dq > 0
            alpha = jnp.where(good, rz / jnp.where(good, dq, 1.0), 0.0).astype(F32)
            p = p + alpha * d; r = r - alpha * q; z = r * inv; rz2 = dot(r, z)
            d = z + (rz2 / jnp.where(rz != 0, rz, 1.0)).astype(F32) * d
            return p, r, d, rz2, it + 1, jnp.max(jnp.abs(r)), good

        p, r, d, rz, it, rn, ok = lax.while_loop(cond, body, (p, r, d, rz, jnp.zeros((), I32), jnp.max(jnp.abs(r)), jnp.ones((), bool)))
        # projection with p = 0 on the surface (ghost fluid), and the faces known afterwards
        out, known = [], []
        for ax in range(3):
            liqL, liqR, tLR, tRL = faces[ax]
            pL, pR = lo(p, ax, 0.0), hi(p, ax, 0.0)
            psR = jnp.where(liqR, pR, jnp.where(liqL, pL * (1.0 - 1.0 / tLR), 0.0))
            psL = jnp.where(liqL, pL, jnp.where(liqR, pR * (1.0 - 1.0 / tRL), 0.0))
            upd = (self.th[ax] > 0) & (liqL | liqR)
            f = jnp.where(upd, vel[ax] - (psR - psL) / dx, vel[ax]); k = upd
            if ax == 2:
                f = jnp.where(self.floor_w, 0.0, f); k = k | self.floor_w
            out.append(f.astype(F32)); known.append(k)
        return out, known, p, it, rn / jnp.maximum(bn, 1e-30)

    def extrapolate(self, vel, known, layers=3):
        out = []
        for f, k in zip(vel, known):
            for _ in range(layers):
                s = jnp.zeros_like(f); c = jnp.zeros(f.shape, F32)
                for ax in range(3):
                    for d in (-1, 1):
                        kk = sh(k, d, ax, False); s = s + jnp.where(kk, sh(f, d, ax, 0.0), 0.0); c = c + kk
                f = jnp.where(k, f, jnp.where(c > 0, s / jnp.maximum(c, 1.0), 0.0)); k = k | (c > 0)
            out.append(f)
        return out

    # ---------------------------------------------------------------- grid to particles, move, glass, rim (Taichi g2p)
    def g2p(self, s, vel, dt, gx, gz):
        dx = self.dx; G = self.G; X, act = s["xp"], s["act"]
        g = (X - self.origin) / dx; vs, Cs = [], []
        for comp in range(3):
            fl, ok, w, wv, cf, fr = self._corners(g, comp, self.fshape[comp])
            val = jnp.where(ok, vel[comp].reshape(-1)[fl], 0.0)                    # (8, N)
            vs.append(jnp.sum(w * val, 0))
            sg = 2.0 * cf - 1.0                                                     # d(weight)/d(fraction) signs
            gw = jnp.stack([sg[..., 0] * wv[..., 1] * wv[..., 2], wv[..., 0] * sg[..., 1] * wv[..., 2], wv[..., 0] * wv[..., 1] * sg[..., 2]], -1)
            Cs.append(jnp.sum(val[..., None] * gw, 0) / dx)
        newv = jnp.stack(vs, -1); C = jnp.stack(Cs, 1)
        Xn = X + dt * newv
        below = Xn[:, 2] < 0.1 * dx
        Xn = Xn.at[:, 2].set(jnp.where(below, 0.1 * dx, Xn[:, 2]))
        newv = newv.at[:, 2].set(jnp.where(below & (newv[:, 2] < 0), 0.0, newv[:, 2]))
        r = jnp.sqrt(Xn[:, 0] ** 2 + Xn[:, 1] ** 2); Rw = self.Rz(Xn[:, 2]) - 0.1 * dx
        inglass = Xn[:, 2] < G.zrim
        out = inglass & (r > Rw) & (r > 0)
        scale = jnp.where(out, Rw / jnp.maximum(r, 1e-12), 1.0)
        Xn = Xn.at[:, 0].multiply(scale).at[:, 1].multiply(scale)
        nr = jnp.stack([Xn[:, 0], Xn[:, 1], jnp.zeros_like(r)], -1) / jnp.maximum(r, 1e-12)[:, None]
        vn = jnp.sum(newv * nr, -1)
        newv = jnp.where((out & (vn > 0))[:, None], newv - vn[:, None] * nr, newv)
        over = (~inglass) & (r > float(G.Rz(G.zrim - 1e-6)))
        top = Xn[:, 2] > G.z0 + (self.nz - 1) * dx
        leave = act & (over | top)
        act2 = act & ~leave
        # drops in free flight (gravity minus the glass's acceleration), until 0.25 m below the floor
        fly = s["fly"]; vf = s["vp"] + dt * jnp.array([gx, 0.0, gz], F32); xf = s["xp"] + dt * vf
        land = fly & (xf[:, 2] < -0.25)
        xp = jnp.where(act[:, None], Xn, jnp.where(fly[:, None], xf, s["xp"]))
        vp = jnp.where(act[:, None], newv, jnp.where(fly[:, None], vf, s["vp"]))
        fly2 = (fly & ~land) | leave
        s = dict(s, xp=xp.astype(F32), vp=vp.astype(F32), C=jnp.where(act[:, None, None], C, 0.0).astype(F32),
                 act=act2, fly=fly2, landed=s["landed"] | land)
        mom = jnp.sum(jnp.where(act2[:, None], newv, 0.0).astype(F64), 0)
        return s, mom

    # ---------------------------------------------------------------- one fluid step (Taichi Stout.step)
    def step(self, s, dt, gx, gz):
        dt = jnp.asarray(dt, F32); gx = jnp.asarray(gx, F32); gz = jnp.asarray(gz, F32)
        vel, mass, cnt = self.p2g(s)
        vel = self.normalize_force(vel, mass, dt, gx, gz)
        ph, liq, nsel = self.level_set(s, cnt)
        H = self.surface(ph, liq)
        if self.nu > 0: vel = self.viscosity(vel, mass, dt)
        z = jnp.zeros((), F64); ew = es = ef = z
        if self.gs > 0 or self.skin or self.head: vel, ew, es, ef = self.friction(vel, mass, ph, liq, dt, s["hf"])
        # the head's weight on the surface (verification.md item 4), in the solver's pressure units (Pa x dt / rho)
        ps = (self.rho_f * s["hf"] * jnp.maximum(-gz, 0.0) * dt / self.rho).astype(F32) if self.head else jnp.zeros((self.n, self.n), F32)
        vel, known, p, it, res = self.pressure(vel, ph, liq, s["p"], ps)
        vel = self.extrapolate(vel, known)
        s, mom = self.g2p(s, vel, dt, gx, gz)
        if self.head: s = self.head_spill(s, H, dt, gx, gz)
        s = dict(s, p=p, ewall=s["ewall"] + ew, eskin=s["eskin"] + es, efoam=s["efoam"] + ef)
        vmax = jnp.max(jnp.where(s["act"][:, None], jnp.abs(s["vp"]), 0.0))
        mhead = self.rho_f * jnp.sum(s["hf"].astype(F64)) * self.dx ** 2
        diag = dict(it=it, res=res, mom=mom, nact=jnp.sum(s["act"], dtype=I32), nsel=nsel, vmax=vmax, mhead=mhead)
        return s, diag

    def resort(self, s):
        """Sort the particles by cell (only the order in memory changes), so that neighbours on the grid are neighbours in
        memory: the scatters and gathers then touch the memory in order."""
        ci = jnp.floor((s["xp"] - self.origin) / self.dx).astype(I32); fl, ok = self.flat(ci, self.dims)
        key = jnp.where(s["act"] & ok, fl, math.prod(self.dims))
        o = jnp.argsort(key)
        return {k: (v[o] if (hasattr(v, "shape") and v.ndim >= 1 and v.shape[0] == self.N) else v) for k, v in s.items()}

    # ---------------------------------------------------------------- what is stored each frame (on the GPU)
    def observe(self, s):
        """The free surface of the main body of stout, as a height on the grid's columns: in each column, the first air cell
        above liquid that rests on the bottom, and the zero of the level set between it and the liquid cell below it.
        Drops: the particles more than 1.5 dx above their column's surface, and those in free flight outside the glass."""
        dx = self.dx; G = self.G
        vel, mass, cnt = self.p2g(s)
        ph, liq, nsel = self.level_set(s, cnt)
        H = self.surface(ph, liq)
        # drops
        X, act, fly = s["xp"], s["act"], s["fly"]
        i = jnp.clip(jnp.floor((X[:, 0] - G.x0) / dx).astype(I32), 0, self.n - 1)
        j = jnp.clip(jnp.floor((X[:, 1] - G.x0) / dx).astype(I32), 0, self.n - 1)
        Hp = H[i, j]
        loose = act & jnp.isfinite(Hp) & (X[:, 2] > Hp + 1.5 * dx)
        dmask = loose | fly
        nd = jnp.sum(dmask, dtype=I32)
        di = jnp.nonzero(dmask, size=self.M, fill_value=0)[0]
        drops = jnp.where((jnp.arange(self.M) < nd)[:, None], X[di], jnp.nan)
        # books
        v = s["vp"].astype(F64); z = X[:, 2].astype(F64)
        KE = 0.5 * self.mp * jnp.sum(jnp.where(act[:, None], v * v, 0.0))
        PE = self.mp * 9.81 * jnp.sum(jnp.where(act, z, 0.0))
        Px = self.mp * jnp.sum(jnp.where(act, v[:, 0], 0.0))
        return dict(H=H, drops=drops.astype(F32), ndrops=nd, nloose=jnp.sum(loose, dtype=I32), nfly=jnp.sum(fly, dtype=I32),
                    nlanded=jnp.sum(s["landed"], dtype=I32), nact=jnp.sum(act, dtype=I32), KE=KE, PE=PE, Px=Px,
                    ewall=s["ewall"], efoam=s["efoam"], eskin=s["eskin"], nliq=jnp.sum(liq, dtype=I32), nsel=nsel,
                    hf=s["hf"], lumps=s["bx"], lumpvol=s["bvol"], foam_spill=s["foam_spill"], foam0=s["foam0"])

    def polar(self, H, nr=16, nth=64, Rmax=None):
        """The stored surface H sampled (bilinear, on the GPU) on rings r = Rmax ir / nr, theta = 2 pi ith / nth;
        Rmax defaults to the glass's radius at the fill less half a cell (the last columns whose centres are in the glass)."""
        G = self.G; dx = self.dx; Rmax = (G.Rfill - 0.5 * dx) if Rmax is None else Rmax
        r = Rmax * jnp.arange(nr + 1) / nr; th = 2 * jnp.pi * jnp.arange(nth) / nth
        x = r[:, None] * jnp.cos(th)[None]; y = r[:, None] * jnp.sin(th)[None]
        fx = (x - G.x0) / dx - 0.5; fy = (y - G.x0) / dx - 0.5
        i = jnp.clip(jnp.floor(fx).astype(I32), 0, self.n - 2); j = jnp.clip(jnp.floor(fy).astype(I32), 0, self.n - 2)
        tx = fx - i; ty = fy - j
        Hf = jnp.where(jnp.isfinite(H), H, jnp.nanmean(H))
        return ((1 - tx) * (1 - ty) * Hf[i, j] + tx * (1 - ty) * Hf[i + 1, j] + (1 - tx) * ty * Hf[i, j + 1] + tx * ty * Hf[i + 1, j + 1]).astype(F32)


# ====================================================================== the cart (float64, on the GPU)
CART_COMMON = dict(Mb=1.5, mw=0.3, Rw=0.04, Iw=0.00024, k=600.0, c=8.0, kt=20000.0, ct=5.0, cx=2.0, Crr=0.0, Tf=0.0,
                   bf=0.0, CdA=0.0, rhoAir=1.2, vSmooth=0.001, Ls=0.135, g=9.81, Ngear=10.0, Km=0.02, Ra=2.0, Jm=2e-6,
                   Vmax=12.0, Imax=3.0, tauI=0.002, Ts=0.001, Kp=25.178818315223719, Ki=316.40636258071589,
                   csky=47.636016270456992, Umax=40.0, tauU=0.005, mu=0.8)   # solver.py (write_cart.cjs, fill 125 mm, rho 1007)


def road_table(road, Rw=0.04, xmin=-1.0, xmax=14.0, h=0.0005):
    """Road.build of stout-cart.js: the axle height of a rigid wheel rolling over the profile, every h (as solver.py)."""
    n = int(round((xmax - xmin) / h)) + 1; x = xmin + h * np.arange(n); kind = road.get("kind", "bumps")
    if kind == "bumps":
        zr = np.zeros(n)
        for b in road["bumps"]:
            s = (x - b["x"]) / b["L"]; m = (s > -0.5) & (s < 0.5); zr[m] += 0.5 * b["h"] * (1 + np.cos(2 * np.pi * s[m]))
    elif kind == "drawn":
        P = np.array(road["points"], float); zr = np.interp(x, P[:, 0], P[:, 1])
    else:
        raise ValueError(kind)
    m = int(math.ceil(Rw / h)); za = np.full(n, -1e9)
    for d in range(-m, m + 1):
        s = d * h
        if abs(s) > Rw: continue
        sh_ = np.full(n, -1e9)
        if d >= 0: sh_[:n - d] = zr[d:]
        else: sh_[-d:] = zr[:n + d]
        za = np.maximum(za, sh_ + math.sqrt(Rw * Rw - s * s))
    return xmin, h, za, zr


class Cart:
    """Cart of stout-cart.js in JAX. State: a dict of float64 scalars. ctrl: 0 off, 1 speed PI, 2 speed PI + road preview."""

    def __init__(self, params, road):
        self.p = {k: float(v) for k, v in params.items() if k not in ("ctrl", "susp")}
        self.ctrl = int(params.get("ctrl", 1)); self.susp = int(params.get("susp", 0))
        self.xmin, self.h, za, self.zr = road; self.za = jnp.asarray(za, F64); self.nza = len(za)

    def axle(self, x):
        f = (x - self.xmin) / self.h; j = jnp.clip(jnp.floor(f).astype(I32), 0, self.nza - 2); t = f - j
        A, B = self.za[j], self.za[j + 1]
        return A + t * (B - A), (B - A) / self.h

    def bForce(self): return self.p["Ngear"] * self.p["Km"] / self.p["Rw"]

    def resist(self, v, N):
        P = self.p; sg = v / jnp.sqrt(v * v + P["vSmooth"] ** 2)
        return P["cx"] * v + P["Crr"] * N * sg + P["Tf"] / P["Rw"] * sg + P["bf"] * v / P["Rw"] ** 2 + 0.5 * P["rhoAir"] * P["CdA"] * v * jnp.abs(v)

    def massX(self, ml):
        P = self.p; return P["Mb"] + ml + P["mw"] + (P["Iw"] + P["Ngear"] ** 2 * P["Jm"]) / P["Rw"] ** 2

    def init(self, x0, ml):
        P = self.p; Ms = P["Mb"] + ml; a, d = self.axle(jnp.asarray(x0, F64))
        zw = a - (Ms + P["mw"]) * P["g"] / P["kt"]; zb = zw + P["Ls"] - Ms * P["g"] / P["k"]
        z = jnp.zeros((), F64)
        c = dict(x=jnp.asarray(x0, F64), vx=jnp.asarray(P["v0"], F64), zb=zb, vzb=z, zw=zw, vzw=z, t=z, ml=jnp.asarray(ml, F64),
                 xi=z, us=z, uscmd=z, tS=z, ax=z, azb=z, azw=z, ireach=z, N=z)
        i0 = self.resist(c["vx"], (P["Mb"] + ml + P["mw"]) * P["g"]) / self.bForce()
        c.update(i=i0, icmd=i0)
        return self.forces(c, 0.0, 0.0)

    def sample(self, c):
        P = self.p
        i0 = self.resist(jnp.asarray(P["v0"], F64), (P["Mb"] + c["ml"] + P["mw"]) * P["g"]) / self.bForce()
        e = P["v0"] - c["vx"]
        if self.ctrl in (1, 2):
            ic = i0 + P["Kp"] * e + P["Ki"] * c["xi"]
            if self.ctrl == 2:
                a, d = self.axle(c["x"] + c["vx"] * P["tauI"]); ic = ic + (P["Mb"] + c["ml"] + P["mw"]) * P["g"] * d / self.bForce()
            xi = jnp.where(jnp.abs(ic) < P["Imax"], c["xi"] + e * P["Ts"], c["xi"])
        else:
            ic = i0; xi = c["xi"]
        u = -P["csky"] * c["vzb"] if self.susp else jnp.zeros((), F64)
        return dict(c, icmd=ic, xi=xi, uscmd=jnp.clip(u, -P["Umax"], P["Umax"]))

    def forces(self, c, Fx, Fz):
        P = self.p; Ms = P["Mb"] + c["ml"]; a, d = self.axle(c["x"])
        N = jnp.maximum(P["kt"] * (a - c["zw"]) + P["ct"] * (d * c["vx"] - c["vzw"]), 0.0)
        FS = -P["k"] * (c["zb"] - c["zw"] - P["Ls"]) - P["c"] * (c["vzb"] - c["vzw"]) + c["us"]
        Fm0 = self.bForce() * c["i"]; Fg = P["mu"] * N; Fm = jnp.clip(Fm0, -Fg, Fg); Fr = -N * d
        FR = self.resist(c["vx"], N)
        ax = (Fr + Fm - FR + Fx) / self.massX(c["ml"])
        azb = (FS - Ms * P["g"] + Fz) / Ms; azw = (-FS - P["mw"] * P["g"] + N) / P["mw"]
        E = P["Km"] * P["Ngear"] * c["vx"] / P["Rw"]
        il = jnp.clip(c["icmd"], -P["Imax"], P["Imax"]); il = jnp.clip(il, (-P["Vmax"] - E) / P["Ra"], (P["Vmax"] - E) / P["Ra"])
        return dict(c, ax=ax, azb=azb, azw=azw, ireach=il, N=N)

    def step(self, c, hh, Fx, Fz):
        P = self.p; tS = c["tS"] + hh; due = tS >= P["Ts"] - 1e-12
        cs = self.forces(self.sample(dict(c, tS=tS - P["Ts"])), Fx, Fz)
        c = jax.tree_util.tree_map(lambda a, b: jnp.where(due, a, b), cs, dict(c, tS=tS))
        vx = c["vx"] + hh * c["ax"]; vzb = c["vzb"] + hh * c["azb"]; vzw = c["vzw"] + hh * c["azw"]
        c = dict(c, vx=vx, vzb=vzb, vzw=vzw, x=c["x"] + hh * vx, zb=c["zb"] + hh * vzb, zw=c["zw"] + hh * vzw,
                 i=c["ireach"] + (c["i"] - c["ireach"]) * jnp.exp(-hh / P["tauI"]),
                 us=c["uscmd"] + (c["us"] - c["uscmd"]) * jnp.exp(-hh / P["tauU"]), t=c["t"] + hh)
        return self.forces(c, Fx, Fz)


# ====================================================================== advancing to the next frame (one compiled loop)
def make_advance(S, mode, cart=None, cfl=0.8, dtmax=0.002, push=None):
    """Returns advance(state, t, t_end, extra) -> (state, t, extra, stats), compiled once. mode "free": glass held still,
    pushed along x by a(t) = push_a sin(pi (t - t0) / push_T) for t0 <= t < t0 + push_T (push = (t0, push_a, push_T)).
    mode "ride": the cart drives the glass; extra carries the cart's state, the stout's last momentum and its push."""
    dx = S.dx

    def body(c):
        s, t, ex, st = c
        dt = jnp.minimum(jnp.minimum(dtmax, cfl * dx / jnp.maximum(ex["vmax"], 1e-6)), ex["t_end"] - t)
        if mode == "free":
            t0, pa, pT = push; tm = t + 0.5 * dt
            ax = jnp.where((tm >= t0) & (tm < t0 + pT), pa * jnp.sin(jnp.pi * (tm - t0) / pT), 0.0)
            s, d = S.step(s, dt, -ax, -9.81)
            ex = dict(ex, vmax=d["vmax"].astype(F64))
        else:
            cs = ex["cart"]; vx0, vz0 = cs["vx"], cs["vzb"]
            nsub = jnp.maximum(1, jnp.round(dt / 1e-4).astype(I32)); hc = dt / nsub
            cs = lax.fori_loop(0, nsub, lambda _, cc: cart.step(cc, hc, ex["F"][0], ex["F"][1]), cs)
            ax, az = (cs["vx"] - vx0) / dt, (cs["vzb"] - vz0) / dt
            s, d = S.step(s, dt, -ax, -9.81 - az)
            P = d["mom"] * S.mp
            F = jnp.where(ex["haveP"], -(P - ex["P"]) / dt, 0.0)
            cs = dict(cs, ml=S.rho * S.V * d["nact"].astype(F64) / S.N + d["mhead"])
            ex = dict(ex, cart=cs, P=P, F=jnp.stack([F[0], F[2]]), haveP=jnp.ones((), bool), vmax=d["vmax"].astype(F64),
                      imp=ex["imp"] + jnp.stack([F[0], F[2]]) * dt)
        st = dict(steps=st["steps"] + 1, its=st["its"] + d["it"], itmax=jnp.maximum(st["itmax"], d["it"]),
                  resmax=jnp.maximum(st["resmax"], d["res"].astype(F64)), nselmax=jnp.maximum(st["nselmax"], d["nsel"]))
        return s, t + dt, ex, st

    def advance(s, t, ex):
        st = dict(steps=jnp.zeros((), I32), its=jnp.zeros((), I32), itmax=jnp.zeros((), I32), resmax=jnp.zeros((), F64), nselmax=jnp.zeros((), I32))
        s, t, ex, st = lax.while_loop(lambda c: c[1] < c[2]["t_end"] - 1e-9, body, (s, t, ex, st))
        return S.resort(s), t, ex, st

    return jax.jit(advance)


def ride_extra(S, cart_obj, x0=0.5):
    ml = S.rho * S.V + (S.rho_f * HEAD0 * float(np.sum(np.asarray(S.rc) < S.G.Rfill)) * S.dx ** 2 if S.head else 0.0)
    return dict(cart=cart_obj.init(x0, ml), P=jnp.zeros(3, F64), F=jnp.zeros(2, F64), haveP=jnp.zeros((), bool),
                vmax=jnp.zeros((), F64), imp=jnp.zeros(2, F64), t_end=jnp.zeros((), F64))
