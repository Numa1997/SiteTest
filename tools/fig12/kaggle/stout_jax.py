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
BODY_TOP = -0.014              # m, the top of the cart's body below the glass's inner floor (the glass's foot is 14 mm thick)
BODY_HALF = (0.11, 0.06)       # m, half the body's length and width (as drawn: 220 mm by 120 mm)
OMEGA = 2 * math.pi * 3.42     # rad/s, the first sloshing mode: sets the Stokes layer, sqrt(2 nu / omega) = 0.44 mm
MODELS = {
    # no friction and no head: what the numerical method alone loses (used to measure numerical damping)
    "inviscid": dict(nu=0.0, wall=False, skin=False, head=False),
    # the stout's viscosity and the glass's boundary layer, clean surface, no head
    "wall": dict(nu=NU_STOUT, wall=True, skin=False, head=False),
    # the whole model (notes/fig12/research/verification.md): viscosity, the glass's boundary layer, the surface that cannot stretch
    # (protein skin, or the head as a lid), and the head of foam: its weight on the stout, its friction on the glass, its spilling
    "full": dict(nu=NU_STOUT, wall=True, skin=True, head=True),
    # the head as a heavy lid only (weight and mass, no shear resistance, no friction on the glass): the check of its inertia
    "lid": dict(nu=NU_STOUT, wall=True, skin=False, head=True, sheet=False),
}
# The head of foam: every number from notes/fig12/research/data-for-solver.md (13 Nov 2026).
HEAD0 = 0.019        # m, the head as served: 18-20 mm specification; 17.5-22.2 mm measured two minutes after pouring (KegWorks 2019)
GAMMA = 0.0442       # N/m, surface tension of degassed Guinness, 20 C, pendant drop (Voelp & Willenbacher 2021, Table 2)
# the air in a pub (continuous model's drag, Stout.air_drag): 20 C, 101.3 kPa, dry; density and viscosity from the standard tables
# (CRC Handbook: rho = p M / (R T) = 1.204 kg/m^3, mu = 1.81e-5 Pa s)
RHO_AIR = 1.204
MU_AIR = 1.81e-5
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


def foam_flow_stress(Ca):
    """Viscous stress (Pa) of the wet foam flowing at capillary number Ca = mu gamma_dot R32 / gamma: Tcholakova et al., PRE 78,
    011405 (2008), films and menisci, in units of gamma/R32 (notes/fig12/research handover, part B2):
        tau / (gamma/R) = 0.7 Ca^0.47 Phi^(5/6) / (1 - Phi)^0.5 + 8 Ca^0.7 Phi^(5/6) / (1 - Phi)^0.15.
    At 10 1/s (Ca = 1.58e-5) the two terms are 7.5 and 4.2 Pa; their sum, 11.8 Pa, is the research file's value (wolfram/05)."""
    return GAMMA / RBUB * GAS ** (5.0 / 6.0) * (0.7 * Ca ** 0.47 / PHI_F ** 0.5 + 8.0 * Ca ** 0.7 / PHI_F ** 0.15)


def head_wall_stress(v):
    """Stress (Pa) of the head's edge sliding on the glass at speed |v| (m/s): the smaller of the sliding law (Cantat 2013) and
    what the foam itself can carry, its yield stress plus its viscous stress (Tcholakova et al., PRE 78, 011405 (2008), eq. 48b)
    in a layer one bubble diameter thick."""
    v = jnp.abs(v); Ca = MU_STOUT * v / GAMMA
    slide = Z_WALL * GAMMA / RBUB * (6.82 * Ca ** (2.0 / 3.0) + 0.94 * LR_WALL * Ca ** (1.0 / 3.0))
    Cas = MU_STOUT * v / (2.0 * GAMMA)
    carry = TAU_Y + foam_flow_stress(Cas)
    return jnp.minimum(slide, carry)


# ====================================================================== the head as an elasto-viscoplastic foam (Step 4, 21 Nov 2026)
# notes/spill/STATE-projection-fix.md, instruction section 6 (B.1). The head is a jammed wet foam (gas fraction GAS = 0.73 > PHI_C):
# below the yield stress TAU_Y an elastic solid of shear modulus G_HEAD, above it a plastic flow whose excess stress is Tcholakova's
# viscous stress. Per particle the isochoric elastic left Cauchy-Green tensor be (det = 1, packed xx yy zz xy xz yz), Kirchhoff stress
# tau = G dev(be), von Mises invariant s = sqrt(tau:tau / 2) (= |tau_xz| in simple shear). Return map, backward Euler, engineering
# plastic shear rate gp = sqrt(2 Dp:Dp): trial b = f be f^T, f = I + dt C (C the APIC velocity gradient), normalised to det 1;
# s_tr > TAU_Y: solve s_tr - G dt gp = TAU_Y + tau_v(gp), scale dev(b) by s_new / s_tr, restore det 1 with b = D + c I.
def tch_coeffs(gamma=GAMMA, R32=RBUB, gas=GAS, mu=MU_STOUT):
    """tau_v(gdot) = A1 gdot^0.47 + A2 gdot^0.70 (Pa), foam_flow_stress written in gdot: the same law (Tcholakova et al. 2008)."""
    base = gamma / R32 * gas ** (5.0 / 6.0); k = mu * R32 / gamma
    return base * 0.7 * k ** 0.47 / (1.0 - gas) ** 0.5, base * 8.0 * k ** 0.70 / (1.0 - gas) ** 0.15


EVP_A1, EVP_A2 = tch_coeffs()
RHO_HEAD = PHI_F * 1007.0            # kg/m^3, 271.89: the head's density, liquid fraction times the stout's (gas mass neglected)


def sym_unpack(b6):
    xx, yy, zz, xy, xz, yz = [b6[..., i] for i in range(6)]
    return jnp.stack([jnp.stack([xx, xy, xz], -1), jnp.stack([xy, yy, yz], -1), jnp.stack([xz, yz, zz], -1)], -2)


def sym_pack(B):
    return jnp.stack([B[..., 0, 0], B[..., 1, 1], B[..., 2, 2], B[..., 0, 1], B[..., 0, 2], B[..., 1, 2]], -1)


def det3(B):
    return (B[..., 0, 0] * (B[..., 1, 1] * B[..., 2, 2] - B[..., 1, 2] * B[..., 2, 1]) - B[..., 0, 1] * (B[..., 1, 0] * B[..., 2, 2] - B[..., 1, 2] * B[..., 2, 0])
            + B[..., 0, 2] * (B[..., 1, 0] * B[..., 2, 1] - B[..., 1, 1] * B[..., 2, 0]))


def evp_tau(be6, G=G_HEAD):
    """Kirchhoff stress G dev(be), packed (N, 6)."""
    tr = (be6[..., 0] + be6[..., 1] + be6[..., 2]) / 3.0
    return G * (be6 - jnp.stack([tr, tr, tr, 0.0 * tr, 0.0 * tr, 0.0 * tr], -1))


def evp_return_map(be6, C, dt, G=G_HEAD, tau_y=TAU_Y, A1=EVP_A1, A2=EVP_A2, n_gp=6, n_c=5, hw=False):
    """One backward-Euler step of the elasto-viscoplastic head, per particle. be6 (N, 6) float32, C (N, 3, 3) the velocity gradient
    (C[i, a] = d u_i / d x_a). Returns be6_new, yielded (bool), gp (1/s), s_new (Pa), det(be_new), the relative residual of the
    gp equation after n_gp Newton steps. Newton in u = gp^0.47 on h(u) = G dt u^(1/0.47) + A2 u^(0.70/0.47) + A1 u - (s_tr - tau_y),
    from u0 = min((s_tr - tau_y)/A1, ((s_tr - tau_y)/(G dt))^0.47), an upper bound of the root (h is convex and increasing), so the
    iterates fall monotonically onto it. det(D + c I) = 1 by Newton on c^3 - I2 c + I3 - 1 = 0 from c0 = 1 + sqrt(4 I2 / 3) (above
    the largest root, the cubic convex beyond it: monotone)."""
    if hw:   # 25 Nov 2026 (flag evp_hw): Hughes-Winget increment f = (I - dt C / 2)^-1 (I + dt C / 2); for a pure rotation C = W it is
        # exactly orthogonal, so be = I stays I and spin makes no stress (f = I + dt C grows s by G (W dt)^2 / sqrt 3 per step)
        I3h = jnp.eye(3, dtype=F32)[None]
        f = jnp.linalg.solve(I3h - 0.5 * dt * C, I3h + 0.5 * dt * C)
    else:
        f = jnp.eye(3, dtype=F32)[None] + dt * C
    B = sym_unpack(be6); Bt = f @ B @ jnp.swapaxes(f, -1, -2)
    Bt = Bt / jnp.cbrt(jnp.maximum(det3(Bt), 1e-30))[..., None, None]
    tr = jnp.trace(Bt, axis1=-2, axis2=-1) / 3.0; I3m = jnp.eye(3, dtype=F32)[None]
    D = Bt - tr[..., None, None] * I3m
    s_tr = G * jnp.sqrt(0.5 * jnp.sum(D * D, (-2, -1)))
    y = s_tr > tau_y
    rhs = jnp.maximum(s_tr - tau_y, 0.0)
    e1 = 1.0 / 0.47; e2 = 0.70 / 0.47
    u = jnp.minimum(rhs / A1, (rhs / (G * dt)) ** 0.47)
    for _ in range(n_gp):
        h = G * dt * u ** e1 + A2 * u ** e2 + A1 * u - rhs
        dh = G * dt * e1 * u ** (e1 - 1.0) + A2 * e2 * u ** (e2 - 1.0) + A1
        u = jnp.maximum(u - h / dh, 0.0)
    gp = jnp.where(y, u ** e1, 0.0)
    res = jnp.where(y, jnp.abs(G * dt * gp + A2 * u ** e2 + A1 * u - rhs) / jnp.maximum(rhs, 1e-30), 0.0)
    s_new = jnp.where(y, tau_y + A1 * gp ** 0.47 + A2 * gp ** 0.70, s_tr)
    Db = jnp.where(y[..., None, None], (s_new / jnp.maximum(s_tr, 1e-30))[..., None, None] * D, D)
    I2 = 0.5 * jnp.sum(Db * Db, (-2, -1)); I3 = det3(Db)
    c = 1.0 + jnp.sqrt(4.0 * I2 / 3.0)
    for _ in range(n_c):
        c = c - (c ** 3 - I2 * c + I3 - 1.0) / (3.0 * c * c - I2)
    Bn = jnp.where(y[..., None, None], Db + c[..., None, None] * I3m, Bt)
    return sym_pack(Bn).astype(F32), y, gp.astype(F32), s_new.astype(F32), det3(Bn), res


def evp_trial_trace(be6, C, dt):
    """Audit only (instruction 0004, 23 Nov 2026; nothing in the default path calls it): tr of the elastic trial state of
    evp_return_map, the same first lines: f = I + dt C, Bt = f B f^T / det(f B f^T)^(1/3). Used for E_drop = V (G/2) (tr Bt - tr B_new)."""
    f = jnp.eye(3, dtype=F32)[None] + dt * C
    B = sym_unpack(be6); Bt = f @ B @ jnp.swapaxes(f, -1, -2)
    Bt = Bt / jnp.cbrt(jnp.maximum(det3(Bt), 1e-30))[..., None, None]
    return jnp.trace(Bt, axis1=-2, axis2=-1)


# ====================================================================== geometry (built once, before the run)
class Geometry:
    """The glass on the grid: open fractions of every face, wall area per cell, masks. Cell (i, j, k) has its centre at
    (x0 + (i + 1/2) dx, x0 + (j + 1/2) dx, z0 + (k + 1/2) dx); z0 = -2 dx (two cells of glass below the floor).
    body = None: the grid is the glass's cavity and 20 mm above the rim (Fig. 12 and Fig. 16 up to 18 Nov 2026).
    body = (hx, hy, z_top), the continuous model (18 Nov 2026, notes/spill/STATE.md): the grid covers the cart's body top
    (|x| < hx, |y| < hy, at z_top below the glass's inner floor) and 30 mm above the rim; the glass is a SOLID inside the grid (its
    wall from R(z) to R(max(z, 8 mm)) + 2.5 mm, its foot down to z_top) and so is the body below z_top. Liquid anywhere on the grid
    obeys the same equations; the grid is open at its sides, top and bottom beyond the body."""

    WALL = 0.0025

    def __init__(self, R, dzp, fill, dx, body=None, top=0.03, lip=0.0):
        R = np.asarray(R, float); self.R = R; self.dzp = dzp; self.fill = fill; self.dx = dx; self.nR = len(R)
        self.zrim = (len(R) - 1) * dzp; Rmax = R.max(); self.body = body
        # Step 3 (20 Nov 2026): top = the grid's height above the rim (continuous model; 0.03 m = unchanged); lip = radius of the
        # rounded rim (0 = the square top of the wall, unchanged). With lip > 0 the wall above zc = rim - lip is the disc of radius lip
        # about (R_m, zc), R_m = R(zc) + WALL/2: a half-round lip of the wall's own half-thickness, the rim's height unchanged.
        self.lip = float(lip); self.zlip = self.zrim - self.lip; self.Rm = float(self.Rz(self.zlip - 1e-9) + 0.5 * self.WALL) if lip > 0 else None
        if body is None:
            self.n = n = int(math.ceil(2 * (Rmax + 2 * dx) / dx)); self.nz = nz = int(math.ceil((self.zrim + 0.02) / dx)) + 2
            self.x0 = -n * dx / 2; self.z0 = -2 * dx
            nx = ny = n; self.y0 = self.x0
        else:
            hx, hy, zt = body
            # z0 = -k dx puts the cavity's floor (z = 0) on a face, as the old grid does (the floor mid-cell left stout below it)
            # a grid as long and as wide as the body (19 Nov 2026: the Fig. 16 deck is 310 x 124 mm; a square grid on the longer side
            # spent 60 % of its cells on the air beside the deck): nx cells along x, ny across, both even about the glass's axis
            nx = int(math.ceil(2 * (hx + 2 * dx) / dx)); ny = int(math.ceil(2 * (hy + 2 * dx) / dx)); self.n = n = nx
            self.z0 = -(int(math.ceil(-zt / dx)) + 4) * dx
            self.nz = nz = int(math.ceil((self.zrim + top - self.z0) / dx)); self.x0 = -nx * dx / 2; self.y0 = -ny * dx / 2
        self.nx, self.ny = nx, ny
        s = (np.arange(4) + 0.5) / 4
        xs4 = self.x0 + dx * (np.arange(nx)[:, None] + s[None, :]).ravel()      # 4 samples across each cell
        ys4 = self.y0 + dx * (np.arange(ny)[:, None] + s[None, :]).ravel()
        zs4 = self.z0 + dx * (np.arange(nz)[:, None] + s[None, :]).ravel()
        xf = self.x0 + dx * np.arange(nx + 1); yf = self.y0 + dx * np.arange(ny + 1); zf = self.z0 + dx * np.arange(nz + 1)
        ins = self.inside if body is None else self.open
        thu = ins(xf[:, None, None], ys4[None, :, None], zs4[None, None, :]).reshape(nx + 1, ny, 4, nz, 4).mean((2, 4))
        thv = ins(xs4[:, None, None], yf[None, :, None], zs4[None, None, :]).reshape(nx, 4, ny + 1, nz, 4).mean((1, 4))
        thw = ins(xs4[:, None, None], ys4[None, :, None], zf[None, None, :]).reshape(nx, 4, ny, 4, nz + 1).mean((1, 3))
        if body is None: thu[0] = thu[-1] = 0; thv[:, 0] = thv[:, -1] = 0; thw[:, :, 0] = 0      # the box is closed except its top
        c = self.x0 + (np.arange(nx) + 0.5) * dx; cy = self.y0 + (np.arange(ny) + 0.5) * dx; zc = self.z0 + (np.arange(nz) + 0.5) * dx
        if body is not None:
            # a face is closed when the segment between the two cell centres it joins crosses a solid anywhere (9 points): the glass's
            # wall is thinner than two cells, and a face cut by it would otherwise couple the stout inside to the air outside through
            # the pressure (smoke test 1, 18 Nov 2026: the pint at rest leaked; review by the open-problems session)
            # (only when both cell centres are open: a cell whose centre lies in the wall is a cut cell and keeps its face fractions,
            # as in the old model; closing those too lost the liquid in the sliver beside the wall, smoke test 3-4: wall columns 1.4 mm low)
            # 19 Nov 2026 (GPU rest checks 2-4: the pint at rest sank 13-15 mm in 0.3 s on every body; the old model held): one pressure per
            # cell, so a cell must not join the stout in the glass to the air outside it. The glass wall (2.5 mm) is thinner than two cells,
            # and a cell can hold an open sliver on each side of it; cc51c2c left such cells open both ways, and the stout lost its
            # hydrostatic support through them. Rule: below the rim every cell belongs to one side, the cavity or the outside, the side that
            # holds more of its open volume (2 x 2 x 2 samples); a face between cells of different sides is closed. Above the rim nothing is
            # closed (the stout flows over the rim there).
            q4 = np.array([-0.25, 0.25]) * dx
            nin = np.zeros((nx, ny, nz)); nout = np.zeros((nx, ny, nz))
            for ox in q4:
                for oy in q4:
                    for oz in q4:
                        Xs, Ys, Zs = np.meshgrid(c + ox, cy + oy, zc + oz, indexing="ij")
                        op = ~self.solid(Xs, Ys, Zs); cv_ = self.cavity(Xs, Ys, Zs)
                        nin += op & cv_; nout += op & ~cv_
            side = nin > nout                                           # True: the cavity's side
            low = (zc < self.zrim)[None, None, :]
            du = np.zeros_like(thu, bool); du[1:-1] = (side[1:] != side[:-1]) & low & True
            dv = np.zeros_like(thv, bool); dv[:, 1:-1] = (side[:, 1:] != side[:, :-1]) & low
            zcf = self.z0 + dx * np.arange(nz + 1)
            dw = np.zeros_like(thw, bool); dw[:, :, 1:-1] = (side[:, :, 1:] != side[:, :, :-1]) & (zcf[1:-1] < self.zrim)[None, None, :]
            thu = np.where(du, 0.0, thu); thv = np.where(dv, 0.0, thv); thw = np.where(dw, 0.0, thw)
            self.side = side
        self.thu, self.thv, self.thw = thu, thv, thw
        X, Y, Z = np.meshgrid(c, cy, zc, indexing="ij"); r2 = X * X + Y * Y
        self.xc, self.yc, self.zc = c, cy, zc
        Rcav = self.Rz(np.minimum(Z, self.zrim - 1e-6))
        self.cav_inner = (Z > 0) & (r2 < (Rcav - 0.5 * dx) ** 2)                       # well inside the cavity
        self.wallcut = (Z > 0) & (Z < self.zrim) & (r2 >= (self.Rz(Z) - 0.5 * dx) ** 2) & (r2 < (self.Rz(Z) + 0.5 * dx) ** 2 if body else True)   # cut by the glass's inner wall
        self.cavc = self.inside(X, Y, Z) if body is None else self.cavity(X, Y, Z)    # centre inside the cavity (or above it)
        # where the level set is built from the particles: the cavity's interior (old model), or every open cell (continuous model)
        # (continuous model: open cells at least half a cell from any solid, as cav_inner keeps half a cell from the inner wall: an
        # empty cell against a wall, where the particles stand thinner, must not read as air; smoke test 3 read the wall columns 1.4 mm low)
        if body is None: self.lsdom = self.cav_inner
        else:
            # half a cell from the cavity's inner wall (the old rule, cav_inner) inside the cavity; every open cell elsewhere, so a film
            # down the outside of the glass or a puddle on the body keeps its own free surface (review, 18 Nov 2026)
            self.lsdom = np.where(self.cavity(X, Y, Z), self.cav_inner, ~self.solid(X, Y, Z))
        if body is None: self._wall_area()
        else: self._wall_area_solid(xs4, ys4, zs4)
        self.Rfill = float(self.Rz(fill))

    def Rz(self, z):
        f = np.clip(np.asarray(z) / self.dzp, 0.0, self.nR - 1.001)
        return np.interp(f, np.arange(self.nR), self.R)

    def inside(self, x, y, z):
        z = np.asarray(z, float)
        return ((z > 0) & ((z >= self.zrim) | (x * x + y * y < self.Rz(z) ** 2))).astype(float)

    def cavity(self, x, y, z):
        """The glass's cavity and the cylinder of the rim's radius above it (the stout 'in the glass', for the books)."""
        z = np.asarray(z, float); r2 = x * x + y * y
        return (z > 0) & (r2 < self.Rz(np.minimum(z, self.zrim - 1e-6)) ** 2)

    def solid(self, x, y, z):
        """The continuous model's solids: the glass (wall shell and foot) and the cart's body below its top."""
        hx, hy, zt = self.body; z = np.asarray(z, float)
        deck = (z <= zt) & (np.abs(x) < hx) & (np.abs(y) < hy)
        return self.glass(x, y, z) | deck

    def glass(self, x, y, z):
        """The glass alone (wall shell, rounded lip if lip > 0, foot), continuous model."""
        hx, hy, zt = self.body; z = np.asarray(z, float); r2 = x * x + y * y
        Rin = self.Rz(np.clip(z, 0.0, self.zrim - 1e-6)); Rout = self.Rz(np.clip(z, 0.008, self.zrim - 1e-6)) + self.WALL
        wall = (z > 0) & (z < self.zlip) & (r2 >= Rin ** 2) & (r2 < Rout ** 2)
        if self.lip > 0: wall = wall | ((z >= self.zlip) & ((np.sqrt(r2) - self.Rm) ** 2 + (z - self.zlip) ** 2 < self.lip ** 2))
        foot = (z <= 0) & (z > zt) & (r2 < Rout ** 2)
        return wall | foot

    def section_lines(self, narc=24):
        """The glass's (r, z) section as two polylines: the cavity's surface (floor, inner wall, inner half of the lip up to its
        top) and the outside's surface (deck top beside the foot, foot side, outer wall, outer half of the lip up to its top)."""
        hx, hy, zt = self.body; zrim = self.zrim
        zp = np.arange(self.nR) * self.dzp; zp = zp[zp < self.zlip]; zp = np.append(zp, self.zlip)
        ri = self.Rz(zp); ro = self.Rz(np.maximum(zp, 0.008)) + self.WALL; rf = float(self.Rz(0.008) + self.WALL)
        cav = [(0.0, 0.0)] + list(zip(ri, zp)); ext = [(rf + 1.0, zt), (rf, zt)] + list(zip(ro, zp))
        if self.lip > 0:
            a = np.linspace(0.0, 0.5 * np.pi, narc)
            cav += list(zip(self.Rm - self.lip * np.cos(a), self.zlip + self.lip * np.sin(a)))
            ext += list(zip(self.Rm + self.lip * np.cos(a), self.zlip + self.lip * np.sin(a)))
        return np.array(cav), np.array(ext)
        return wall | foot | deck

    def open(self, x, y, z):
        return (~self.solid(x, y, z)).astype(float)

    def side_of(self, x, y, z, chunk=4096):
        """Step 2 (20 Nov 2026, notes/spill/STATE-projection-fix.md): which side of the glass a point belongs to, True = the cavity's.
        An open point is on the side whose region holds it (the cavity below the rim: z > 0, r < R(z)); every other open point,
        above the rim included, is False (above the rim the sides are not used). A point in the glass (wall shell or foot) is on the
        side of the nearer of the two open surfaces in the (r, z) section: the cavity's (floor and inner wall) or the outside's
        (outer wall, the foot's side and the deck's top beside it). Above the floor of the bowl this is the wall's mid-surface
        r = R_mid(z) = (R_in + R_out)/2 wherever the wall is cut radially; it also splits the foot and the thick base of the bowl,
        where the radial mid-line would not follow the wall. The deck is False."""
        x, y, z = np.broadcast_arrays(np.asarray(x, float), np.asarray(y, float), np.asarray(z, float))
        shp = x.shape; x = x.ravel(); y = y.ravel(); z = z.ravel(); r = np.hypot(x, y)
        hx, hy, zt = self.body; zrim = self.zrim
        out = self.cavity(x, y, z) & (z < zrim)
        gl = self.glass(x, y, z)
        if gl.any():
            cav, ext = self.section_lines()
            def dmin(P, poly):
                a = poly[:-1]; b = poly[1:]; ab = b - a; L2 = np.maximum((ab ** 2).sum(1), 1e-30); d = np.empty(len(P))
                for i in range(0, len(P), chunk):
                    p = P[i:i + chunk, None, :]
                    t = np.clip(((p - a[None]) * ab[None]).sum(2) / L2[None], 0, 1)
                    d[i:i + chunk] = np.sqrt(((p - (a[None] + t[..., None] * ab[None])) ** 2).sum(2)).min(1)
                return d
            P = np.stack([r[gl], z[gl]], 1)
            out[gl] = dmin(P, cav) < dmin(P, ext)
        return out.reshape(shp)

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

    def _wall_area_solid(self, xs4, ys4, zs4):
        """Area of solid surface in each cell, per cell volume, for the continuous model: on 4 x 4 x 4 samples per cell, the
        crossings between solid and open samples along each axis give the surface's projections (A_x, A_y, A_z), each crossing
        (dx/4)^2; for a surface that is flat across the cell its area is |(A_x, A_y, A_z)|."""
        nx, ny, nz, dx = self.nx, self.ny, self.nz, self.dx; h2 = (dx / 4) ** 2; A = np.zeros((nx, ny, nz))
        X, Y = np.meshgrid(xs4, ys4, indexing="ij")
        for k in range(nz):
            S = np.stack([self.solid(X, Y, np.full_like(X, z)) for z in zs4[4 * k:4 * k + 4]], -1)   # (4n, 4n, 4)
            S = S.reshape(nx, 4, ny, 4, 4).transpose(0, 2, 1, 3, 4)                                  # (nx, ny, 4, 4, 4)
            ax_ = np.abs(np.diff(S.astype(int), axis=2)).sum((2, 3, 4)); ay = np.abs(np.diff(S.astype(int), axis=3)).sum((2, 3, 4))
            az = np.abs(np.diff(S.astype(int), axis=4)).sum((2, 3, 4))
            A[:, :, k] = np.sqrt(ax_ ** 2 + ay ** 2 + az ** 2) * h2 * 4.0 / 3.0   # 3 of the 4 sample intervals per cell lie inside it
        a = A / dx ** 3
        pad = lambda arr, ax: np.concatenate([np.take(arr, [0], ax) * 0, arr, np.take(arr, [0], ax) * 0], ax)
        self.ac = a
        self.au = np.where(self.thu > 0, 0.5 * (pad(a, 0)[:-1] + pad(a, 0)[1:]), 0)
        self.av = np.where(self.thv > 0, 0.5 * (pad(a, 1)[:, :-1] + pad(a, 1)[:, 1:]), 0)
        self.aw = np.where(self.thw > 0, 0.5 * (pad(a, 2)[:, :, :-1] + pad(a, 2)[:, :, 1:]), 0)
        self.area_cells = float(A.sum()); self.area_profile = float("nan")


def glass_volume(R, dzp, fill, n=20000):
    z = np.linspace(0, fill, n + 1); r = np.interp(z / dzp, np.arange(len(R)), R)
    return float(np.trapezoid(np.pi * r * r, z) if hasattr(np, "trapezoid") else np.trapz(np.pi * r * r, z))


def seed_lattice(G, ppc=2):
    """The lattice the stout is seeded on: ppc points per cell across (spacing h = dx/ppc), and layers every hz up the glass,
    hz = fill / round(fill / h), so that a whole number of layers ends exactly at the fill (13 Nov 2026: with hz = h the
    seeded stout stopped at 124 mm on a 4 mm grid). A point belongs to the glass where its centre is 0.25 h inside the wall.
    Returns the points' x (= y) coordinates, hz, the number of layers up to the rim, and mask(z) for one layer."""
    h = G.dx / ppc; hz = G.fill / max(1, round(G.fill / h))
    xs = G.x0 + h * (np.arange(int(G.n * ppc)) + 0.5); X, Y = np.meshgrid(xs, xs, indexing="ij"); r2 = X * X + Y * Y
    mask = lambda z: r2 < (float(G.Rz(z)) - 0.25 * h) ** 2
    return xs, hz, int(math.ceil(G.zrim / hz)), mask, h


def seed_particles(G, ppc=2, seed=1):
    """ppc^2 points per cell across, layers every hz from the floor to the fill, inside the glass, jittered sideways by at most
    0.3 h (so no point leaves its column) and in height by at most 0.3 hz."""
    rng = np.random.default_rng(seed); xs, hz, _, mask, h = seed_lattice(G, ppc); pts = []
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    for z in hz * (np.arange(int(round(G.fill / hz))) + 0.5):
        m = mask(z); pts.append(np.stack([X[m], Y[m], np.full(m.sum(), z)], 1))
    P = np.concatenate(pts)
    P[:, :2] += rng.uniform(-0.3 * h, 0.3 * h, (len(P), 2)); P[:, 2] += rng.uniform(-0.3 * hz, 0.3 * hz, len(P))
    return P


def seed_head(G, ppc=2, seed=2, h=None, jitter_z=0.0):
    """Step 4: the head's particles on the pint's lattice above the fill, FILL <= z < FILL + h (h = HEAD0, kept at every grid). Layers at
    exactly the lattice spacing hl = dx / ppc: n_full = floor(h / hl) full layers from the fill up, plus one top layer of thickness
    h - n_full hl if that is > 0 (0.25 mm at dx 1.5 mm). Each particle carries the volume of the region nearest to it: hl^2 times its
    layer's thickness inside the head, so every interior cell holds exactly one cell volume (v1 spaced 25 layers at 0.760 mm: 1.0133,
    the slab test's -9.4 %); and the particles of the ring next to the wall (lattice points with a neighbour outside the glass) also
    carry the strip between them and the wall (the lattice keeps points 0.25 hl inside it): in each layer, the glass's volume of that
    layer (integral of pi R(z)^2 over its thickness) minus the layer's particles at hl^2 t, shared equally by the ring (21 Nov,
    instruction option 2). The total then equals the glass's volume by construction. No vertical jitter by default (jitter_z = 0;
    a vertical jitter moves particles across cell faces); sideways jitter 0.3 hl as seed_particles (it never leaves the cell).
    Returns the points, the glass's volume between FILL and FILL + h, each particle's volume (m^3), and per layer
    (z, thickness, particles, ring particles, ring volume factor)."""
    h = HEAD0 if h is None else h
    rng = np.random.default_rng(seed); xs, _, _, mask, hl = seed_lattice(G, ppc)
    n_full = int(math.floor(h / hl + 1e-9)); t_top = h - n_full * hl
    edges = [(G.fill + k * hl, G.fill + (k + 1) * hl) for k in range(n_full)] + ([(G.fill + n_full * hl, G.fill + h)] if t_top > 1e-12 else [])
    X, Y = np.meshgrid(xs, xs, indexing="ij"); pts = []; vols = []; info = []
    for zl, zh in edges:
        z = 0.5 * (zl + zh); t = zh - zl; m = mask(z)
        nb = np.ones_like(m)
        for ax in (0, 1):
            for d in (-1, 1): nb &= np.roll(m, d, ax)
        ring = m & ~nb
        zz = np.linspace(zl, zh, 401); Vlay = float(np.trapezoid(np.pi * G.Rz(zz) ** 2, zz)) if hasattr(np, "trapezoid") else float(np.trapz(np.pi * G.Rz(zz) ** 2, zz))
        base = hl * hl * t; n = int(m.sum()); nr = int(ring.sum())
        fac = 1.0 + (Vlay - n * base) / max(nr * base, 1e-300)
        v = np.where(ring, fac * base, base)[m]
        pts.append(np.stack([X[m], Y[m], np.full(n, z)], 1)); vols.append(v)
        info.append(dict(z=z, t=t, n=n, n_ring=nr, ring_factor=float(fac), V_layer_glass=Vlay, V_layer_particles=float(v.sum())))
    P = np.concatenate(pts); vol = np.concatenate(vols)
    th = np.concatenate([np.full(i["n"], i["t"]) for i in info])
    P[:, :2] += rng.uniform(-0.3 * hl, 0.3 * hl, (len(P), 2)); P[:, 2] += rng.uniform(-jitter_z, jitter_z, len(P)) * th
    V = float(sum(i["V_layer_glass"] for i in info))
    return P, V, vol, info


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
    def __init__(self, G, model="full", ppc=2, seed=1, rho=1007.0, K_frac=0.62, M_drops=16384, tol=1e-5, maxit=600, head_mass=True, vol_corr=0.0,
                 extra=None, head_mode="sheet"):
        self.G = G; self.rho = rho; self.ppc = ppc
        # the volume correction (Fig. 16 run 4, 15 Nov 2026): 0 = off, Fig. 12's runs unchanged. After violent stirring the particle cloud
        # stayed spread out (the stored surface of the uncontrolled kerb stood 24 mm above the height its remaining stout fills at rest):
        # the projection makes the grid velocity divergence-free, but nothing returns drifted particles to their resting spacing. With
        # vol_corr = kappa > 0 each interior cell is given the net outflow kappa (n/n0 - 1) dx / dt, n the particles in its 5 x 5 x 5 block,
        # n0 = 125 ppc^3 at rest (only swelling beyond 5 %, see volume_source); a sparse block draws stout in, a crowded one pushes it out (Kugelstadt et al. 2019). The drift that does
        # this comes from a second projection (of a zero velocity field with that target) and moves the particles' positions only; put into
        # the velocity it overshot (a 6 mm test stretched by 20 % fell to 0.85 of the rest volume). A dead band of 3 % keeps the pint at
        # rest exactly as before.
        self.vol_corr = float(vol_corr)
        M = MODELS[model]; self.model = model
        self.nu = M["nu"]; self.gs = math.sqrt(M["nu"] * OMEGA / 2) if M["wall"] else 0.0
        self.skin = M["skin"]
        dx = G.dx; self.dx = dx; self.Hb = 2.0 * dx; self.rls = 0.9 * dx      # the pressure step's level set: closes the gaps between the sparse particles at the glass
        self.rread = 0.505 * dx  # the read-out's: derived 13 Nov 2026, reads a flat seeded layer to -0.09..+0.02 cell (0.9 dx reads 0.5-1.0 cell high)
        self.tol = tol; self.maxit = maxit
        # absolute floor of the pressure residual (owner, 22 Nov 2026): the conjugate gradient also stops when max |r| < atol, so a
        # near-empty right-hand side counts as converged. Units: the solver's pressure p dt / rho, residual in m^2/s (b = -div dx).
        # A residual r leaves a cell's net outflow wrong by r / dx (m/s), its volume by r dt / dx^2 per step: with r = 1e-10 m^2/s,
        # dx 1.5 mm, dt 7.67e-4 s and 1 300 steps a second, even if every cell erred the same way the pint's height would move 5.5 um in a
        # second, ten times below Step 4.4's 50 um mark. Typical steps stop on the relative test (1e-5 of max |b|) long before it.
        self.atol = 1e-10
        n, nz = G.n, G.nz; self.n, self.nz = n, nz
        nx, ny = G.nx, G.ny; self.nx, self.ny = nx, ny          # nx = ny = n on the old square grid (bit for bit as before)
        self.dims = (nx, ny, nz)
        self.fshape = [(nx + 1, ny, nz), (nx, ny + 1, nz), (nx, ny, nz + 1)]
        P = seed_particles(G, ppc, seed)
        self.N = len(P); self.V = glass_volume(G.R, G.dzp, G.fill); self.mp = rho * self.V / self.N
        # Step 2 (20 Nov 2026): extra particles (positions, m) after the pint's, each of the pint's particle mass; None: unchanged
        self.N_pint = self.N
        if extra is not None: P = np.concatenate([P, np.asarray(extra, float)]); self.N = len(P)
        if head_mode == "evp":   # Step 4: the head's particles after the stout's (and any extra): FILL <= z < FILL + HEAD0
            Ph, self.V_head_glass, vol_h, self.head_layers = seed_head(G, ppc, seed + 1); self.N_head = len(Ph); self.N_stout = self.N
            self.Vp_stout = self.V / self.N_pint; self.V_head = float(vol_h.sum())       # the head's particles' volume (m^3)
            self.Vp_head = self.V_head / self.N_head; self.mp_head = RHO_HEAD * self.Vp_head   # means, for the logs only
            # per-particle volume and mass, carried in the state (resort keeps them with their particles); stout as before
            self.pvol0 = np.concatenate([np.full(self.N_stout, self.Vp_stout), vol_h]).astype(np.float32)
            self.pmass0 = np.concatenate([np.full(self.N_stout, self.mp), RHO_HEAD * vol_h]).astype(np.float32)
            self.m_stout0 = float(np.sum(self.pmass0[:self.N_stout].astype(np.float64))); self.m_head0 = float(np.sum(RHO_HEAD * vol_h))
            P = np.concatenate([P, Ph]); self.N = len(P)
        self.K = int(K_frac * self.N); self.M = M_drops
        self.P0 = P.astype(np.float32)
        f = lambda a: jnp.asarray(a, F32)
        self.th = [f(G.thu), f(G.thv), f(G.thw)]; self.af = [f(G.au), f(G.av), f(G.aw)]; self.ac = f(G.ac)
        self.cav_inner = jnp.asarray(G.cav_inner); self.wallcut = jnp.asarray(G.wallcut); self.cavc = jnp.asarray(G.cavc > 0)
        self.lsdom = jnp.asarray(G.lsdom)
        self.Rd = jnp.asarray(G.R, F32)
        self.origin = jnp.asarray([G.x0, G.y0, G.z0], F32)
        k = np.arange(nz + 1)[None, None, :]
        self.floor_w = jnp.asarray((G.thw == 0) & (k <= 2))       # closed floor faces: w = 0 exactly
        # the continuous model (G.body set, 18 Nov 2026): every closed face of the glass and of the cart's body holds w = 0, and the
        # stout's free surface carries the surface tension GAMMA wherever no head lies on it
        self.cont = G.body is not None
        self.ls_extend = False   # test switch (20 Nov 2026, notes/spill/STATE-projection-fix.md): see enable_ls_extend; off = the v8 code unchanged
        self.side_vis = False    # Step 2 switch (20 Nov 2026): see enable_side_vis; off = unchanged
        self.wall_guard = False  # Step 3 switch (20 Nov 2026): _g2p_cont keeps cavity particles 1e-5 m inside the inner wall; off = unchanged
        # Step 4 (21 Nov 2026): head_mode "sheet" = the head as before (bit for bit); "evp" = the head as elasto-viscoplastic foam
        # particles (see _init_evp); then the 2-D head (head_sheet, head_spill, its weight and Robin load) and the skin are off
        self.evp = head_mode == "evp"
        self.diag_g2p = False    # Step 3 verify (diagnostic only): the state also carries each particle's position before _g2p_cont's
                                 # collisions (xprop) and whether it touched the glass (g2p_glass); the motion is unchanged
        self.audit = False       # instruction 0004 (23 Nov 2026), diagnostic only: with head_mode "evp", step() also returns the energy
                                 # ledger of its sub-steps, U_el, E_drop, the E_plastic split and the shadow cell-strain E_plastic (needs
                                 # diag_g2p = True and the state key "be_cell"); False (default) = the code path unchanged
        if self.cont: self.floor_w = jnp.asarray(G.thw == 0)
        self.gamma = GAMMA if self.cont else 0.0
        c = jnp.asarray(G.xc, F32); cy = jnp.asarray(G.yc, F32); zc = jnp.asarray(G.zc, F32)
        self.cc = (c, cy, zc)
        o = np.array([(a, b, c) for a in range(-1, 3) for b in range(-1, 3) for c in range(-1, 3)], np.int32)
        self.off64 = jnp.asarray(o)
        self.corners = jnp.asarray(np.array([(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)], np.int32))
        # the head of foam lives on the columns of the grid (n x n), as a thickness h_f on top of the stout's surface
        self.head = M["head"]; self.rho_f = PHI_F * rho; self.sheet = M.get("sheet", True)
        if self.evp: self.head = False; self.sheet = False; self.skin = False; self.m_floor = 0.05 * RHO_HEAD * dx ** 3
        # the head's mass (13 Nov 2026, run 8): the head moves up and down with the stout's surface, so the stout must accelerate
        # it; set False to recover runs 6 and 7 (weight only)
        self.head_mass = head_mass
        X, Y = np.meshgrid(G.xc, G.yc, indexing="ij")
        self.rc = jnp.asarray(np.hypot(X, Y), F32); self.colx = jnp.asarray(X, F32); self.coly = jnp.asarray(Y, F32)
        # the open part of each column at the fill (the horizontal face nearest the fill height): the head lies on every column
        # that holds stout there, out to the glass, and a column's head counts hf x this area (13 Nov 2026, run 3: the head lay
        # only on columns whose centre is inside the glass; its weight, 51 Pa, then squeezed the stout up into the bare columns
        # at the glass at 11 mm/s in one step from rest, and the pint at rest stirred itself)
        self.afill = jnp.asarray(G.thw[:, :, int(round((G.fill - G.z0) / dx))], F32)
        if G.body is not None:
            # the continuous model's grid also covers the air around the glass, open at the fill height too: the head lies only on the
            # glass's own columns, those whose centre is within the glass's radius at the fill plus one cell (19 Nov 2026: GPU check 2
            # laid it on every column over the deck, and the pint at rest sank 9.6 mm in 0.3 s)
            self.afill = jnp.where(jnp.asarray(np.hypot(*np.meshgrid(G.xc, G.yc, indexing="ij")) < G.Rfill + dx), self.afill, 0.0).astype(F32)
        self.ell = G.Rfill / 1.84118         # m, the depth over which the foam's sliding speed dies away upward, 1/k (Sauret 2015)
        self.Rrim = float(G.Rz(G.zrim - 1e-6))
        self.MF = 4096                       # lumps of head in flight, at most
        # face centres (x, z) of the u and w faces, for the rotating frame's forces (Fig. 16; unused when rot is None)
        xf = G.x0 + dx * np.arange(n + 1); zf = G.z0 + dx * np.arange(nz + 1)
        self.fu_x = jnp.asarray(xf[:, None, None], F32); self.fu_z = jnp.asarray(G.zc[None, None, :], F32)
        self.fw_x = jnp.asarray(G.xc[:, None, None], F32); self.fw_z = jnp.asarray(zf[None, None, :], F32)

    # ---------------------------------------------------------------- the glass's frame when the glass also turns (Fig. 16)
    @staticmethod
    def frame_accel(x, z, vx, vz, gx, gz, rot):
        """Acceleration felt in the glass's frame at (x, z) by matter moving at (vx, vz) relative to the glass, when the glass turns
        about the y axis at rate om (rad/s, positive from e_x towards e_z, i.e. the deck's nose-up pitch rate) with angular
        acceleration al, and its point S = (0, 0, zS) accelerates so that the uniform part there is (gx, gz):
            a = g_eff(S) - al x (r - S) - om x (om x (r - S)) - 2 om x v
              = (gx + al Z + om^2 X + 2 om vz,   gz - al X + om^2 Z - 2 om vx),   X = x, Z = z - zS.
        Euler (al), centrifugal (om^2) and Coriolis (2 om v) terms; rot = (om, al, zS). With rot None: (gx, gz)."""
        if rot is None: return gx, gz
        om, al, zS = rot; Z = z - zS
        return gx + al * Z + om * om * x + 2.0 * om * vz, gz - al * x + om * om * Z - 2.0 * om * vx

    def body_force(self, vel, mass, dt, gx, gz, rot):
        """dt times the body force on every open face with stout. rot None: the uniform effective gravity (Fig. 12, unchanged).
        rot = (om, al, zS): plus the Euler and centrifugal forces at each face's centre, and the Coriolis force as an exact rotation
        of each cell's velocity by -2 om dt (it does no work), handed to the faces as the mean of the two cells' changes."""
        if rot is None:
            return [jnp.where((mass[c] > 1e-6) & (self.th[c] > 0), vel[c] + dt * (gx if c == 0 else (gz if c == 2 else 0.0)), vel[c]).astype(F32) for c in range(3)]
        om, al, zS = rot
        ax_u, _ = self.frame_accel(self.fu_x, self.fu_z, 0.0, 0.0, gx, gz, rot)
        _, az_w = self.frame_accel(self.fw_x, self.fw_z, 0.0, 0.0, gx, gz, rot)
        uc = 0.5 * (cut_lo(vel[0], 0) + cut_hi(vel[0], 0)); wc = 0.5 * (cut_lo(vel[2], 2) + cut_hi(vel[2], 2))
        ph = 2.0 * om * dt; cph, sph = jnp.cos(ph) - 1.0, jnp.sin(ph)
        du = cph * uc + sph * wc; dw = -sph * uc + cph * wc                   # (u, w) -> R(-2 om dt) (u, w), minus (u, w)
        du_f = 0.5 * (lo(du, 0, 0.0) + hi(du, 0, 0.0)); dw_f = 0.5 * (lo(dw, 2, 0.0) + hi(dw, 2, 0.0))
        inc = [dt * ax_u + du_f, None, dt * az_w + dw_f]
        return [jnp.where((mass[c] > 1e-6) & (self.th[c] > 0), vel[c] + inc[c], vel[c]).astype(F32) if c != 1 else vel[1] for c in range(3)]

    def swelling(self, liq, act):
        """The pint's swelling: volume of the cells the level set calls liquid (open part of each, inside the cavity) over the true
        volume of the stout still in the glass, minus 1. At rest about +0.5 % (the half-filled surface layer); after the uncontrolled
        rides of run 3, +18 to +48 %."""
        vliq = jnp.sum(jnp.where(liq & self.cavc, 1.0, 0.0).astype(F64)) * self.dx ** 3
        return vliq / jnp.maximum(jnp.sum(act, dtype=F64) * self.mp / self.rho, 1e-12) - 1.0

    def volume_source(self, cnt, liq, dt, gate=1.0):
        """The volume correction's target net outflow of each interior cell (m/s): kappa (n/n0 - 1 + d) dx/dt where the 5 x 5 x 5 block about
        the cell holds n < (1 - d) n0 particles (n0 = 125 ppc^3, d = 0.05); zero elsewhere. Every cell of the block must be liquid and well
        inside the cavity. Only swelling is corrected, the fault measured (Fig. 16 run 3: +18 to +48 % after the uncontrolled rides): a
        3 x 3 x 3 block (216 particles) counts with about 7 % noise, and correcting both ways inside a 3 % band stirred a pint at rest
        until its read surface fell 29 mm in 0.8 s (6 mm test, 15 Nov 2026); 125 cells hold about 1,000 particles, about 3 % noise."""
        inner = liq & self.cav_inner; c = cnt.astype(F32); ok = inner
        for ax in range(3):
            c = c + sh(c, 1, ax, 0.0) + sh(c, -1, ax, 0.0) + sh(c, 2, ax, 0.0) + sh(c, -2, ax, 0.0)
            ok = ok & sh(ok, 1, ax, False) & sh(ok, -1, ax, False) & sh(ok, 2, ax, False) & sh(ok, -2, ax, False)
        dev = jnp.clip(c / (125.0 * self.ppc ** 3) - 1.0, -0.5, 0.0)
        dev = jnp.where(dev < -0.05, dev + 0.05, 0.0)
        return jnp.where(ok, gate * self.vol_corr * dev * self.dx / dt, 0.0).astype(F32)

    # ---------------------------------------------------------------- state
    def init_state(self):
        N = self.N
        hf0 = jnp.where(self.afill > 0, HEAD0 if self.head else 0.0, 0.0).astype(F32)
        z64 = jnp.zeros((), F64)
        return dict(xp=jnp.asarray(self.P0), vp=jnp.zeros((N, 3), F32), C=jnp.zeros((N, 3, 3), F32),
                    act=jnp.ones(N, bool), fly=jnp.zeros(N, bool), landed=jnp.zeros(N, bool), stuck=jnp.zeros(N, bool),
                    p=jnp.zeros(self.dims, F32), ewall=z64, efoam=z64, eskin=z64,
                    hf=hf0, wh=jnp.zeros((self.nx, self.ny), F32), foam_spill=z64, foam0=jnp.sum((hf0 * self.afill).astype(F64)) * self.dx ** 2,
                    bx=jnp.full((self.MF, 3), jnp.nan, F32), bv=jnp.zeros((self.MF, 3), F32), bvol=jnp.zeros(self.MF, F32),
                    bptr=jnp.zeros((), I32),
                    **(dict(xprop=jnp.asarray(self.P0), g2p_glass=jnp.zeros(N, bool)) if self.diag_g2p else {}),
                    **(dict(is_head=jnp.arange(N) >= self.N_stout, be=jnp.tile(jnp.asarray([1, 1, 1, 0, 0, 0], F32), (N, 1)),
                           pvol=jnp.asarray(self.pvol0), pmass=jnp.asarray(self.pmass0)) if self.evp else {}))

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

    def p2g_evp(self, s):
        """Step 4, head_mode "evp": p2g with two materials. Per face: momentum, mass M (kg), the sum of weights (occupancy, returned as
        `mass` so every occupancy test stays a weight test), volume V_f and the head's volume V_hf (m^3), and the explicit deviatoric
        force F_dev = -sum over head particles of V_p tau_p . grad w (N). `vel` is returned as (momentum / M) x (sum of weights), so that
        normalize_force (vel / sum of weights) gives the mass-weighted velocity."""
        dx = self.dx; X, V, C, act, ish = s["xp"], s["vp"], s["C"], s["act"], s["is_head"]
        g = (X - self.origin) / dx
        ci = jnp.floor(g).astype(I32); cfl, cok = self.flat(ci, self.dims)
        cnt = jnp.zeros(math.prod(self.dims), I32).at[cfl].add((cok & act).astype(I32)).reshape(self.dims)
        mpart = s["pmass"]; vpart = s["pvol"]                                  # per particle (state), so resort keeps them
        tau = sym_unpack(jnp.where(ish[:, None], evp_tau(s["be"]), 0.0))
        vel, mass, ex = [], [], dict(M=[], Vf=[], Vh=[], Fdev=[])
        for comp in range(3):
            shape = self.fshape[comp]
            fl, ok, w, wv, cf, fr = self._corners(g, comp, shape)
            dpos = (cf - fr[None]) * dx
            val = w * (V[None, :, comp] + jnp.sum(C[None, :, comp, :] * dpos, -1))
            sg = 2.0 * cf - 1.0
            gw = jnp.stack([sg[..., 0] * wv[..., 1] * wv[..., 2], wv[..., 0] * sg[..., 1] * wv[..., 2], wv[..., 0] * wv[..., 1] * sg[..., 2]], -1) / dx
            fdev = -vpart[None] * jnp.sum(tau[None, :, comp, :] * gw, -1)
            m = ok & act[None]
            cols = [val * mpart[None], w * mpart[None], w, w * vpart[None], w * jnp.where(ish, vpart, 0.0)[None], fdev]
            upd = jnp.stack([jnp.where(m, c_, 0.0) for c_ in cols], -1).reshape(-1, 6)
            acc = jnp.zeros((math.prod(shape), 6), F32).at[fl.reshape(-1)].add(upd)
            M_ = acc[:, 1].reshape(shape); ws = acc[:, 2].reshape(shape)
            vel.append(jnp.where(M_ > 0, acc[:, 0].reshape(shape) / jnp.where(M_ > 0, M_, 1.0), 0.0) * ws); mass.append(ws)
            ex["M"].append(M_); ex["Vf"].append(acc[:, 3].reshape(shape)); ex["Vh"].append(acc[:, 4].reshape(shape)); ex["Fdev"].append(acc[:, 5].reshape(shape))
        # face density rho_f = clip(M / V_f, rho_h, rho); faces with no volume take the stout's; beta = rho / rho_f; head fraction f_h
        ex["rho_f"] = [jnp.where(vf > 0, jnp.clip(M_ / jnp.where(vf > 0, vf, 1.0), RHO_HEAD, self.rho), self.rho).astype(F32) for M_, vf in zip(ex["M"], ex["Vf"])]
        ex["beta"] = [(self.rho / r).astype(F32) for r in ex["rho_f"]]
        ex["fh"] = [jnp.where(vf > 0, jnp.clip(vh / jnp.where(vf > 0, vf, 1.0), 0.0, 1.0), 0.0).astype(F32) for vh, vf in zip(ex["Vh"], ex["Vf"])]
        return vel, mass, cnt, ex

    def friction_evp(self, vel, mass, dt, ex):
        """Step 4, head_mode "evp": the glass's stress on the faces beside it, implicit, u <- u / (1 + dt lambda), with
        lambda = A_f / max(M_f, m_floor) [(1 - f_h) rho g_s + f_h tau_w(|u|) / max(|u|, 1e-4 m/s)], A_f = af dx^3 the wall area at the face:
        the stout's Stokes layer (g_s = sqrt(nu omega / 2)) and the head's Cantat wall stress (head_wall_stress), each on its share f_h.
        The force on the face is the wall area times the wall stress whatever the face's open fraction (23 Nov, instruction "step4-close":
        v1 divided by rho_f dx^3, a full cell's mass, so a cut face, which holds M_f = alpha_open rho_f dx^3, got only alpha_open of the
        force). Returns the velocities and the energy taken (J), 0.5 M_f (u0^2 - u^2), split between the stout's layer and the head's
        stress in proportion to their parts of lambda."""
        dV = self.dx ** 3; es = jnp.zeros((), F64); ef = jnp.zeros((), F64); out = []
        for comp in range(3):
            u0 = vel[comp]; ok = (self.th[comp] > 0) & (mass[comp] > 1e-6); fh = ex["fh"][comp]; M = ex["M"][comp]
            au = jnp.abs(u0); k = self.af[comp] * dV / jnp.maximum(M, self.m_floor)
            ls = k * (1.0 - fh) * self.rho * self.gs; lf = k * fh * head_wall_stress(au) / jnp.maximum(au, 1e-4); lam = ls + lf
            wall = ok & (self.af[comp] > 0)
            u = jnp.where(wall, u0 / (1.0 + dt * lam), u0)
            dE = jnp.where(wall, 0.5 * M * (u0 * u0 - u * u), 0.0); fr = ls / jnp.maximum(lam, 1e-30)
            es = es + jnp.sum((dE * fr).astype(F64)); ef = ef + jnp.sum((dE * (1.0 - fr)).astype(F64))
            out.append(u.astype(F32))
        return out, es, ef

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

    def build_sides(self):
        """Step 2 masks (logging, and the switch below): cell_side (True: the cavity's side, Geometry.side_of at the cell centre),
        below_rim (centre below the rim), solidc (centre in a solid), and for each face component its side and whether its centre
        is below the rim. Built once, on the CPU."""
        if hasattr(self, "cell_side"): return
        G = self.G; dx = self.dx
        X, Y, Z = np.meshgrid(G.xc, G.yc, G.zc, indexing="ij")
        self.cell_side_np = G.side_of(X, Y, Z); self.below_rim_np = Z < G.zrim; self.solidc_np = G.solid(X, Y, Z)
        self.cell_side = jnp.asarray(self.cell_side_np); self.below_rim = jnp.asarray(self.below_rim_np); self.solidc = jnp.asarray(self.solidc_np)
        xf = G.x0 + dx * np.arange(self.nx + 1); yf = G.y0 + dx * np.arange(self.ny + 1); zf = G.z0 + dx * np.arange(self.nz + 1)
        pts = [(xf, G.yc, G.zc), (G.xc, yf, G.zc), (G.xc, G.yc, zf)]
        self.fside, self.fbelow = [], []
        for a, b, c in pts:
            Xf, Yf, Zf = np.meshgrid(a, b, c, indexing="ij")
            self.fside.append(jnp.asarray(G.side_of(Xf, Yf, Zf))); self.fbelow.append(jnp.asarray(Zf < G.zrim))

    def enable_side_vis(self):
        """Step 2 switch (20 Nov 2026, notes/spill/STATE-projection-fix.md): below the rim, information does not cross the glass wall.
        (1) A particle's kernel in the level set writes only into cells on its own side (side of a particle: r < R_mid(min(z, rim)),
        R_mid = (R_in + R_out)/2); its mirror image across the inner wall writes only into open cavity cells below the rim.
        (2) The solid extension (enable_ls_extend, call it after this) reads only open cells on the solid cell's own side.
        (3) The velocity is extrapolated into unknown faces twice, once from the known faces on the cavity's side (and above the
        rim), once from those on the outside (and above the rim); each particle reads the copy of its own side.
        The 2.5 mm wall is thinner than the kernel (2 dx = 3 mm): without this, liquid on one side wets cells on the other."""
        self.build_sides(); self.side_vis = True

    def p_side(self, X):
        """Side of each particle, True = the cavity's: r < R_mid(min(z, rim)), as Geometry.side_of on the open regions."""
        G = self.G; zr_ = G.zrim; rr = jnp.sqrt(X[:, 0] ** 2 + X[:, 1] ** 2)
        Rin = self.Rz(jnp.clip(X[:, 2], 0.0, zr_ - 1e-6)); Rout = self.Rz(jnp.clip(X[:, 2], 0.008, zr_ - 1e-6)) + G.WALL
        return rr < 0.5 * (Rin + Rout)

    def enable_ls_extend(self):
        """Test switch, sub-run 2 of the bowl-base drain test (20 Nov 2026). On every cell whose centre lies in the glass (wall or
        foot) and which has an open face, the liquid level set is extended from the nearest open point along the glass's normal,
        phi_liq(x) = phi_liq(x - phi_glass(x) n_s(x)) (solid extrapolation as Ando et al.), and these cells no longer use wallcut /
        ls_inherit. phi_glass is the exact signed distance to the glass's (r, z) section (negative inside), n_s its gradient; the
        value at the surface point is read trilinearly from the cell centres that are not in the glass (weights renormalised)."""
        G = self.G; dx = self.dx; nx, ny, nz = self.dims
        X, Y, Z = np.meshgrid(G.xc, G.yc, G.zc, indexing="ij")
        hx, hy, zt = G.body; zrim = G.zrim
        in_glass = G.glass   # Step 3: the glass with its lip (lip = 0: as before)
        thu, thv, thw = G.thu, G.thv, G.thw
        openf = (thu[1:] > 0) | (thu[:-1] > 0) | (thv[:, 1:] > 0) | (thv[:, :-1] > 0) | (thw[:, :, 1:] > 0) | (thw[:, :, :-1] > 0)
        gl = in_glass(X, Y, Z); E = gl & openf
        # the glass's section in (r, z): the polygon without its edge on the axis
        cavl, extl = G.section_lines(); rf = float(G.Rz(0.008) + G.WALL)
        pts = [(0.0, zt)] + [tuple(p) for p in extl[1:]] + [tuple(p) for p in cavl[::-1]]
        a = np.array(pts[:-1]); b = np.array(pts[1:]); ab = b - a; L2 = np.maximum((ab ** 2).sum(1), 1e-30)
        def dist(r, z):
            p = np.stack([r, z], -1)[:, None, :]
            t = np.clip(((p - a[None]) * ab[None]).sum(2) / L2[None], 0, 1)
            return np.sqrt(((p - (a[None] + t[..., None] * ab[None])) ** 2).sum(2)).min(1)
        def sdf(r, z):
            return np.where(in_glass(r, np.zeros_like(r), z), -1.0, 1.0) * dist(r, z)
        ii = np.argwhere(E); x = X[E]; y = Y[E]; z = Z[E]; r = np.hypot(x, y)
        sv = self.side_vis
        if sv: side = self.cell_side_np; side_e = side[E]   # Step 2: read only open cells on the solid cell's own side
        phi = sdf(r, z); h = 1e-4
        gr = (sdf(r + h, z) - sdf(r - h, z)) / (2 * h); gz = (sdf(r, z + h) - sdf(r, z - h)) / (2 * h)
        gn = np.maximum(np.hypot(gr, gz), 1e-12); gr /= gn; gz /= gn
        cx = np.where(r > 1e-9, x / np.maximum(r, 1e-9), 1.0); cy = np.where(r > 1e-9, y / np.maximum(r, 1e-9), 0.0)
        n3 = np.stack([gr * cx, gr * cy, gz], 1)
        org = np.array([G.x0, G.y0, G.z0])
        idx = np.zeros((len(ii), 8), np.int64); wts = np.zeros((len(ii), 8), np.float32); found = np.zeros(len(ii), bool)
        for push in (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0):   # the surface point; pushed further into the open only if no open centre is around it
            q = np.stack([x, y, z], 1) + (-phi + push * dx)[:, None] * n3
            g = (q - org) / dx - 0.5; i0 = np.floor(g).astype(np.int64); f = g - i0
            k = 0
            for ox in (0, 1):
                for oy in (0, 1):
                    for oz in (0, 1):
                        I = np.clip(i0 + np.array([ox, oy, oz]), 0, np.array([nx - 1, ny - 1, nz - 1]))
                        w = (f[:, 0] if ox else 1 - f[:, 0]) * (f[:, 1] if oy else 1 - f[:, 1]) * (f[:, 2] if oz else 1 - f[:, 2])
                        ok = ~gl[I[:, 0], I[:, 1], I[:, 2]] & ~self._solid_np(G, I)
                        if sv: ok = ok & (side[I[:, 0], I[:, 1], I[:, 2]] == side_e)
                        new = ~found
                        idx[new, k] = ((I[:, 0] * ny + I[:, 1]) * nz + I[:, 2])[new]
                        wts[new, k] = np.where(ok, w, 0.0)[new]
                        k += 1
            s_ = wts.sum(1); found = found | (s_ > 1e-6)
            if found.all(): break
        wts = wts / np.maximum(wts.sum(1, keepdims=True), 1e-12)
        self.ext_cells = jnp.asarray((ii[:, 0] * ny + ii[:, 1]) * nz + ii[:, 2], I32)
        self.ext_idx = jnp.asarray(idx, I32); self.ext_w = jnp.asarray(wts, F32)
        self.ext_mask = jnp.asarray(E); self.ls_extend = True
        self.ext_info = dict(cells=int(E.sum()), unresolved=int((~found).sum()), phi_mm=[float(phi.min() * 1e3), float(phi.max() * 1e3)],
                             side_vis=bool(sv), cavity_side_cells=int(side_e.sum()) if sv else None)
        return self.ext_info

    @staticmethod
    def _solid_np(G, I):
        xc = G.x0 + (I[:, 0] + 0.5) * G.dx; yc = G.y0 + (I[:, 1] + 0.5) * G.dx; zc = G.z0 + (I[:, 2] + 0.5) * G.dx
        return G.solid(xc, yc, zc)

    def level_set(self, s, cnt):
        dx = self.dx; G = self.G
        mA = (cnt == 0) & self.lsdom   # continuous model: everywhere, so liquid outside the glass has its own free surface too
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
        if self.cont: img = img & (rr < Rw) & (Q[:, 2] > 0)   # mirror only stout inside the cavity across the inner wall (not stout down the outside)
        fw = jnp.where(rr > 1e-9, (2.0 * Rw - rr) / jnp.maximum(rr, 1e-9), 0.0)
        Q2 = jnp.stack([Q[:, 0] * fw, Q[:, 1] * fw, Q[:, 2]], -1)
        R2 = 4.0 * dx * dx; size = math.prod(self.dims)
        W = jnp.zeros(size, F32); S = jnp.zeros((size, 3), F32)
        nearf = near.reshape(-1)
        if self.side_vis:   # Step 2: each kernel writes only on its own side of the glass below the rim (see enable_side_vis)
            pin = self.p_side(Q); csf = self.cell_side.reshape(-1); brf = self.below_rim.reshape(-1); slf = self.solidc.reshape(-1)
        for mirror, (q, ok_q) in enumerate(((Q, valid), (Q2, valid & img))):
            qi = jnp.floor((q - self.origin) / dx - 0.5).astype(I32)
            J = qi[:, None, :] + self.off64[None]                                  # (K, 64, 3)
            fl, ok = self.flat(J, self.dims)
            xcJ = self.origin + (J.astype(F32) + 0.5) * dx
            dd = q[:, None, :] - xcJ; d2 = jnp.sum(dd * dd, -1)
            use = ok & ok_q[:, None] & nearf[fl] & (d2 < R2)
            if self.side_vis:
                if mirror: use = use & csf[fl] & ~slf[fl] & brf[fl]
                else: use = use & (~brf[fl] | (csf[fl] == pin[:, None]))
            qq = 1.0 - d2 / R2; wt = jnp.where(use, qq * qq * qq, 0.0)
            W = W.at[fl.reshape(-1)].add(wt.reshape(-1))
            S = S.at[fl.reshape(-1)].add((wt[..., None] * dd).reshape(-1, 3))
        W = W.reshape(self.dims); S = S.reshape(self.dims + (3,))
        has = W > 1e-12
        ph_near = jnp.where(has, jnp.sqrt(jnp.sum((S / jnp.where(has, W, 1.0)[..., None]) ** 2, -1)) - self.rls, 3.0 * dx)
        ph = jnp.where(near, ph_near, jnp.where(cnt > 0, -2.0 * dx, 2.0 * dx))
        phr = ph.astype(F32)            # the level set as the particles give it, before the pressure step's adjustments: read-outs use this
        liq = (ph < 0) | (cnt > 0)
        ph = jnp.where((cnt > 0) & (ph >= 0), -0.05 * dx, ph).astype(F32)
        thu, thv, thw = self.th
        if self.ls_extend:   # test switch: solid cells take the level set of the nearest open point along the glass's normal
            phs = jnp.sum(self.ext_w * ph.reshape(-1)[self.ext_idx], 1)
            ph = ph.reshape(-1).at[self.ext_cells].set(phs).reshape(self.dims)
            liq = liq.reshape(-1).at[self.ext_cells].set(phs < 0).reshape(self.dims)
        for _ in range(3):   # Taichi ls_inherit: cells cut by the glass that read as air take the liquid's phi beside them
            best = jnp.ones(self.dims, F32)
            for ax, th in ((0, thu), (1, thv)):
                best = jnp.minimum(best, jnp.where((cut_lo(th, ax) > 0) & sh(liq, -1, ax, False), sh(ph, -1, ax, 1.0), 1.0))
                best = jnp.minimum(best, jnp.where((cut_hi(th, ax) > 0) & sh(liq, 1, ax, False), sh(ph, 1, ax, 1.0), 1.0))
            above = sh(ph, 1, 2, 1.0)
            best = jnp.minimum(best, jnp.where((cut_hi(thw, 2) > 0) & sh(liq, 1, 2, False) & (above < -0.5 * dx), above, 1.0))
            take = (~liq) & self.wallcut & (best < 1.0)
            if self.ls_extend: take = take & ~self.ext_mask
            liq = liq | take; ph = jnp.where(take, jnp.minimum(best, -0.05 * dx), ph)
        return ph, liq, nsel, phr

    # ---------------------------------------------------------------- viscosity and friction (Taichi viscosity, friction)
    def viscosity(self, vel, mass, dt, fh=None):
        c = self.nu * dt / self.dx ** 2; out = []
        for comp in range(3):
            f = vel[comp]; ok = (self.th[comp] > 0) & (mass[comp] > 1e-6); lap = jnp.zeros_like(f)
            for ax in range(3):
                for d in (-1, 1):
                    lap = lap + jnp.where(sh(ok, d, ax, False), sh(f, d, ax, 0.0) - f, 0.0)
            cc = c if fh is None else c * (1.0 - fh[comp])     # Step 4: the stout's viscosity on its share of the face only
            out.append(jnp.where(ok, f + cc * lap, f))
        return out

    def friction(self, vel, mass, ph, liq, dt, hf):
        """The three thin layers the 1.5 mm grid cannot resolve, as stresses on the faces next to them (verification.md, items 2, 3, 5):
        - the glass: the Stokes-layer stress rho sqrt(nu omega/2) u on the glass's area in each cut cell;
        - the surface that cannot stretch (protein skin, or the head held still by the glass): the same stress on the horizontal
          velocity of the faces of the top liquid cells, over one cell's area per cell;
        - the head of foam (head_sheet): a sheet lying on the stout that resists being sheared and rubs on the glass.
        Returns the velocities and the energy each one took (J)."""
        dx = self.dx; dV = self.rho * dx ** 3; z = jnp.zeros((), F64); ew, es, ef = z, z, z; out = []
        top = liq & ~sh(liq, 1, 2, False)                                    # liquid cells with air above
        for comp in range(3):
            u0 = vel[comp]; ok = (self.th[comp] > 0) & (mass[comp] > 1e-6); u = u0
            if self.gs > 0:                                                   # glass
                g = self.gs * self.af[comp]; u = jnp.where(ok & (g > 0), u * jnp.exp(-g * dt), u)
                ew = ew + 0.5 * dV * jnp.sum(jnp.where(ok, u0 * u0 - u * u, 0.0).astype(F64))
            if self.skin and comp < 2:                                        # surface that cannot stretch
                u1 = u; tf = lo(top, comp, False) | hi(top, comp, False)
                u = jnp.where(ok & tf, u * jnp.exp(-self.gs / dx * dt), u)
                es = es + 0.5 * dV * jnp.sum(jnp.where(ok, u1 * u1 - u * u, 0.0).astype(F64))
            if self.head and self.sheet and comp == 2:                        # the head: a sheet that resists shear
                u1 = u; u = self.head_sheet(u, ok, top, hf, dt)
                ef = ef + 0.5 * dV * jnp.sum(jnp.where(ok, u1 * u1 - u * u, 0.0).astype(F64))
            out.append(u.astype(F32))
        return out, ew, es, ef

    def head_sheet(self, w, ok, top, hf, dt):
        """The head as a sheet in vertical shear. The head rides on the stout, so its vertical velocity in each column is the
        stout's there, w_s(x, y). Where neighbouring columns move at different speeds the head between them is sheared, and it
        resists with the stress of a wet foam: its yield stress plus its viscous stress (Herschel-Bulkley; Tcholakova et al. 2008,
        eq. 54, films term), tau = (tau_y + tau_v(g)) with g = |grad w_s| the shear rate. Over the head's thickness h_f that is a
        force per unit area of surface f = div(h_f tau grad w_s / g); at the glass the head's edge rubs with head_wall_stress
        over the height heff. The force acts on the top layer of the stout (two cells, mass rho 2 dx per area), implicitly:
            rho 2dx (w' - w)/dt = div(h_f eta grad w') - kappa w',  eta = tau/g (g no smaller than 0.05 1/s: below it the head
        is locked), kappa = wall stress / |w| x wall area per column area. Solved by conjugate gradients on the columns; the
        change w' - w goes onto the vertical faces of the top cells; the pressure projection then passes it to the stout below."""
        dx = self.dx
        wc = 0.5 * (cut_lo(w, 2) + cut_hi(w, 2)); okc = cut_lo(ok, 2) | cut_hi(ok, 2)
        t = top & self.cavc & okc
        cntc = jnp.sum(t, 2); has = (cntc > 0) & (hf > 0)
        ws = jnp.where(has, jnp.sum(jnp.where(t, wc, 0.0), 2) / jnp.maximum(cntc, 1), 0.0)
        acs = jnp.sum(jnp.where(t, self.ac, 0.0), 2) / jnp.maximum(cntc, 1)                 # wall area per volume at the surface cell, 1/m
        m = self.rho * self.Hb
        # shear rate on the faces between columns, from the velocity now
        def face(a, ax): return 0.5 * (a + sh(a, 1, ax, 0.0))
        gx_ = (sh(ws, 1, 0, 0.0) - ws) / dx; gy_ = (sh(ws, 1, 1, 0.0) - ws) / dx
        gyx = face(0.5 * (sh(ws, 1, 1, 0.0) - sh(ws, -1, 1, 0.0)) / dx, 0); gxy = face(0.5 * (sh(ws, 1, 0, 0.0) - sh(ws, -1, 0, 0.0)) / dx, 1)
        def eta(g):
            g = jnp.maximum(g, 0.05); Ca = MU_STOUT * g * RBUB / GAMMA
            return (TAU_Y + foam_flow_stress(Ca)) / g
        both = lambda ax: has & sh(has, 1, ax, False)
        cx = jnp.where(both(0), face(hf, 0) * eta(jnp.sqrt(gx_ ** 2 + gyx ** 2)), 0.0) / dx ** 2     # coupling to the column at i + 1
        cy = jnp.where(both(1), face(hf, 1) * eta(jnp.sqrt(gy_ ** 2 + gxy ** 2)), 0.0) / dx ** 2
        kap = jnp.where(has, acs * self.heff(hf) * head_wall_stress(ws) / jnp.maximum(jnp.abs(ws), 1e-3), 0.0)
        diag = m + dt * (cx + sh(cx, -1, 0, 0.0) + cy + sh(cy, -1, 1, 0.0) + kap)
        def A(x):
            return diag * x - dt * (cx * sh(x, 1, 0, 0.0) + sh(cx * x, -1, 0, 0.0) + cy * sh(x, 1, 1, 0.0) + sh(cy * x, -1, 1, 0.0))
        b = m * ws; x = ws; r = b - A(x); z = r / diag; d = z; rz = jnp.sum(r * z)
        def it(_, c):
            x, r, d, rz = c
            q = A(d); al = rz / jnp.maximum(jnp.sum(d * q), 1e-30)
            x = x + al * d; r = r - al * q; z = r / diag; rz2 = jnp.sum(r * z)
            return x, r, z + rz2 / jnp.maximum(rz, 1e-30) * d, rz2
        x, r, d, rz = lax.fori_loop(0, 60, it, (x, r, d, rz))
        dw = jnp.where(has, x - ws, 0.0).astype(F32)
        fmask = lo(t, 2, False) | hi(t, 2, False)                                           # the vertical faces of the top cells
        return jnp.where(fmask & ok, w + dw[:, :, None], w)

    def surface(self, phr):
        """The free surface of the main body of stout, as a height on the grid's columns. Two fields from the same particles:
        phr, built with radius 0.9 dx, closes the small gaps that open between particles; q = phr + 0.395 dx, the same field with
        the read-out radius 0.505 dx, puts its zero on the stout's true top (a flat seeded layer reads -0.09..+0.02 cell).
        1. The body: the highest cell of the column where phr marks stout in it and in the two cells below (so a drop in the air,
           one or two cells across, is not taken for the stout).
        2. The surface: the highest zero of q in the top three cells of that body, between two cell centres.
        If q marks no stout in those three cells, the body's top less the mean offset of the 0.9 dx field (0.68 cell) is used,
        and the column is counted (the second value returned; stored per frame as `nfallback`).
        13 Nov 2026, run 3: reading the top of a three-cell run of q alone fell into gaps 1-2 cells below the surface, 3-4.6 mm,
        in single columns at r = 29-31 mm after 1.8 s at rest; the guard stopped the run."""
        dx = self.dx; q = phr + (self.rls - self.rread); nz = phr.shape[2]
        wet = self.cavc & (phr < 0)
        run = wet & sh(wet, -1, 2, False) & sh(wet, -2, 2, False)
        kt = nz - 1 - jnp.argmax(run[:, :, ::-1], 2)                     # top cell of the body (phr)
        # a column whose body ends because the glass ends there (the cell above has its centre outside the glass), not because
        # air begins, has no surface of its own: at the glass the tulip is widest at z = 116 mm (39.3 mm), so columns whose centre
        # is outside at the fill but inside lower down read 120 mm, and their stout above as 84 drops at rest (run 4, 13 Nov 2026)
        capped = ~jnp.take_along_axis(self.cavc, jnp.minimum(kt + 1, nz - 1)[..., None], 2)[..., 0]
        has = jnp.any(run, 2) & ~capped
        qa = lambda k: jnp.take_along_axis(q, jnp.clip(k, 0, nz - 1)[..., None], 2)[..., 0]
        Hs, found = jnp.zeros(kt.shape, F32), jnp.zeros(kt.shape, bool)
        for j in (2, 1, 0):                                                # lowest first; a higher crossing overwrites it
            k = kt - j; pb, pa = qa(k), qa(k + 1)
            cross = (pb < 0) & ((pa >= 0) | (j == 0))
            frac = jnp.where(pa > pb, jnp.clip(-pb / jnp.maximum(pa - pb, 1e-12), 0.0, 1.0), 0.5)
            Hk = self.cc[2][jnp.clip(k, 0, nz - 1)] + frac * dx
            Hs = jnp.where(cross, Hk, Hs); found = found | cross
        pt, pu = jnp.take_along_axis(phr, kt[..., None], 2)[..., 0], qa(kt + 1) - (self.rls - self.rread)
        f9 = jnp.where(pu > pt, jnp.clip(-pt / jnp.maximum(pu - pt, 1e-12), 0.0, 1.0), 0.5)
        Hf = self.cc[2][kt] + f9 * dx - 0.68 * dx
        return jnp.where(has, jnp.where(found, Hs, Hf), jnp.nan).astype(F32), jnp.sum(has & ~found, dtype=I32)

    def head_spill(self, s, H, dt, gx, gz, rot=None):
        """The head above the rim (verification.md, item 6): where the head's top stands e above the rim, at the glass, the part
        above the rim breaks away once its weight and outward push beat its strength, rho_f (|g_eff| e/2 + a_out e) >= tau_y.
        It leaves as a lump in free flight. Lumps already flying move under gravity minus the glass's acceleration."""
        G = self.G; dx = self.dx; hf = s["hf"]
        ok = jnp.isfinite(H)
        Hs = jnp.where(ok, H, 0.0)
        atwall = ok & (self.rc >= self.Rz(Hs) - 1.5 * dx)
        e = jnp.where(atwall, Hs + hf - G.zrim, 0.0)
        gxr, gzr = self.frame_accel(self.colx, G.zrim, 0.0, 0.0, gx, gz, rot)   # the field at the rim (uniform when rot is None)
        aout = gxr * self.colx / jnp.maximum(self.rc, 1e-9)                  # outward push per unit mass in the glass's frame
        fail = (e > 0) & (hf > 0) & (self.rho_f * (jnp.abs(gzr) * 0.5 + jnp.maximum(aout, 0.0)) * e >= TAU_Y)
        cut = jnp.where(fail, jnp.minimum(e, hf), 0.0)
        # lumps: one per breaking column, at the rim, starting at rest relative to the glass
        m = cut.reshape(-1) > 0; nnew = jnp.sum(m, dtype=I32)
        rank = jnp.cumsum(m.astype(I32)) - 1
        slot = jnp.where(m, (s["bptr"] + rank) % self.MF, self.MF)            # MF = out of range: dropped by mode="drop"
        sc = self.Rrim / jnp.maximum(self.rc.reshape(-1), 1e-9)
        pos = jnp.stack([self.colx.reshape(-1) * sc, self.coly.reshape(-1) * sc, G.zrim + 0.5 * cut.reshape(-1)], -1)
        bx = s["bx"].at[slot].set(pos.astype(F32), mode="drop"); bv = s["bv"].at[slot].set(0.0, mode="drop")
        bvol = s["bvol"].at[slot].set(((cut * self.afill).reshape(-1) * dx * dx).astype(F32), mode="drop")
        onbody = (jnp.abs(bx[:, 0]) < BODY_HALF[0]) & (jnp.abs(bx[:, 1]) < BODY_HALF[1])
        flying = jnp.isfinite(bx[:, 2]) & (bx[:, 2] > -0.25) & ~((bx[:, 2] <= BODY_TOP) & onbody & (bv[:, 2] == 0))
        if rot is None: acc = jnp.array([gx, 0.0, gz], F32)
        else:
            a_x, a_z = self.frame_accel(bx[:, 0], bx[:, 2], bv[:, 0], bv[:, 2], gx, gz, rot); acc = jnp.stack([a_x, jnp.zeros_like(a_x), a_z], -1)
        bv = jnp.where(flying[:, None], bv + dt * acc, bv)
        bn = bx + dt * bv; hitb = flying & (bn[:, 2] < BODY_TOP) & (bx[:, 2] >= BODY_TOP) & onbody
        bn = jnp.where(hitb[:, None], bn.at[:, 2].set(BODY_TOP), bn); bv = jnp.where(hitb[:, None], 0.0, bv)
        bx = jnp.where(flying[:, None], bn, bx)
        return dict(s, hf=(hf - cut).astype(F32), bx=bx, bv=bv, bvol=bvol, bptr=(s["bptr"] + nnew) % self.MF,
                    foam_spill=s["foam_spill"] + jnp.sum((cut * self.afill).astype(F64)) * dx * dx)

    # ---------------------------------------------------------------- pressure (Taichi build, matvec, solve, project)
    def _faces(self, ph, liq, ax):
        liqL, liqR = lo(liq, ax, False), hi(liq, ax, False)
        inL, inR = lo(jnp.ones(self.dims, bool), ax, False), hi(jnp.ones(self.dims, bool), ax, False)
        phL, phR = lo(ph, ax, 0.0), hi(ph, ax, 0.0)
        cLR = inR & (phL - phR < -1e-12); cRL = inL & (phR - phL < -1e-12)
        tLR = jnp.where(cLR, jnp.clip(phL / jnp.where(cLR, phL - phR, -1.0), 0.05, 1.0), 1.0)   # surface's place, L liquid
        tRL = jnp.where(cRL, jnp.clip(phR / jnp.where(cRL, phR - phL, -1.0), 0.05, 1.0), 1.0)   # surface's place, R liquid
        return liqL, liqR, tLR, tRL

    def tension(self, ph, hf, dt):
        """Surface tension on the stout's free surface (continuous model): the pressure just inside the surface exceeds the air's by
        gamma kappa (Young-Laplace), kappa = div(grad phi / |grad phi|) of the level set (phi < 0 in the liquid, so a drop has kappa =
        2/r > 0), by central differences. It enters the ghost-fluid rule as the surface's pressure, in the solver's units p dt / rho.
        |kappa| is held below 2/dx (a drop one cell across): the grid resolves nothing smaller. Not where the head lies on the stout
        (its own sheet carries the surface there). Explicit capillary waves need dt < sqrt(rho dx^3 / (2 pi gamma)) = 3.5 ms at 1.5 mm."""
        dx = self.dx; g = []
        for ax in range(3): g.append((sh(ph, 1, ax, 0.0) - sh(ph, -1, ax, 0.0)) / (2 * dx))
        nn = jnp.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2) + 1e-6
        kap = sum((sh(g[ax] / nn, 1, ax, 0.0) - sh(g[ax] / nn, -1, ax, 0.0)) / (2 * dx) for ax in range(3))
        kap = jnp.clip(kap, -2.0 / dx, 2.0 / dx)
        bare = jnp.broadcast_to((hf <= 0)[:, :, None], self.dims) | ~self.cavc
        return jnp.where(bare & (jnp.abs(ph) < 2.0 * dx), self.gamma * kap * dt / self.rho, 0.0).astype(F32)

    def air_drag(self, vel, mass, ph, liq, dt, wind, beta=None):
        """The air's drag on stout outside the glass (continuous model, 18 Nov 2026; notes/spill/STATE.md, 'Air'). The air is at rest on
        the ground, so in the glass's frame it blows at wind = (-v_x, -v_z) of the glass. On each surface cell of liquid outside the
        cavity the wind presses on the frontal area dx^2 max(0, -n . U_hat) (n the liquid's outward normal), with the sphere's drag
        coefficient C_D(Re) of Schiller & Naumann, C_D = 24/Re (1 + 0.15 Re^0.687), Re = rho_a |U| d / mu_a < 1000, d the local size
        4/|kappa| (a sphere of diameter d has kappa = 4/d), held between dx and 10 mm. The force is shared by the cell's liquid,
        rho dx^3: for a drop resolved by several cells the frontal areas add to pi d^2/4 and the masses to pi d^3 rho/6, so the
        acceleration is (3/4) C_D rho_a U^2 / (rho d), the textbook law. Inside the glass the air is sheltered (its effect on the
        pint's surface was estimated at 0.1 mm of stout and is left out)."""
        dx = self.dx; ux, uz = wind
        g = [(sh(ph, 1, ax, 0.0) - sh(ph, -1, ax, 0.0)) / (2 * dx) for ax in range(3)]
        nn = jnp.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2) + 1e-6; n = [gi / nn for gi in g]
        kap = sum((sh(n[ax], 1, ax, 0.0) - sh(n[ax], -1, ax, 0.0)) / (2 * dx) for ax in range(3))
        d = jnp.clip(4.0 / jnp.maximum(jnp.abs(kap), 1e-6), dx, 0.01)
        uc = [0.5 * (cut_lo(vel[ax], ax) + cut_hi(vel[ax], ax)) for ax in range(3)]   # the liquid's velocity at cell centres
        U = [ux - uc[0], -uc[1], uz - uc[2]]; Um = jnp.sqrt(U[0] ** 2 + U[1] ** 2 + U[2] ** 2) + 1e-9
        front = jnp.maximum(0.0, -(n[0] * U[0] + n[1] * U[1] + n[2] * U[2]) / Um)
        # the surface as a one-sided smoothed delta on the liquid side, (1 + cos(pi phi/e))/e for -e < phi < 0, e = 1.5 dx: its volume
        # integral is the surface's area, so the summed force is exactly the frontal area times the pressure (drag check 1, 036b81d:
        # the surface cells alone gave 67 % of the law for an 8 mm drop)
        e = 1.5 * dx; band = liq & (ph < 0) & (ph > -e) & ~self.cavc
        delta = jnp.where(band, (1.0 + jnp.cos(jnp.pi * ph / e)) / e, 0.0)
        Re = jnp.clip(RHO_AIR * Um * d / MU_AIR, 0.1, 1000.0); CD = 24.0 / Re * (1.0 + 0.15 * Re ** 0.687)
        a = 0.5 * RHO_AIR * CD * Um * front * delta / self.rho                      # times U_vec: acceleration
        out = []
        for ax in range(3):
            ac = a * U[ax]; aL, aR = lo(ac, ax, 0.0), hi(ac, ax, 0.0)
            af = (aL + aR) / jnp.maximum(1.0, (aL != 0).astype(F32) + (aR != 0).astype(F32))   # a face beside air takes its liquid cell's whole value
            if beta is not None: af = af * beta[ax]                                   # Step 4: the drag over the face's own density
            out.append(jnp.where((mass[ax] > 1e-6) & (self.th[ax] > 0), vel[ax] + dt * af, vel[ax]).astype(F32))
        return out

    def _surf_faces(self, ph, liq):
        liqL, liqR, tLR, tRL = self._faces(ph, liq, 2)
        return liqL & ~liqR & (self.th[2] > 0)

    def pressure(self, vel, ph, liq, p_prev, ps, mu=None, w_old=None, geff_dt=0.0, src=None, pst=None, beta=None):
        """ps: the pressure on the free surface (the weight of the head), in the solver's units (Pa x dt / rho), one value per
        column, set on the air side of the surface. Ghost fluid: p = ps at the surface, so the air neighbour of a liquid cell
        reads p_ghost = p_liq (1 - 1/theta) + ps / theta: the diagonal gets th / theta and the right side th ps / theta.
        mu (run 8): the head's mass per area over rho, m_s/rho = rho_f h_f/rho (m), one value per column. The head moves up and
        down with the surface, so under it p_s = m_s (g_eff + dw/dt): in the solver's units P_s = mu (g_eff dt + w' - w_old),
        with w' the new vertical velocity of the face the surface crosses (liquid below, air above). Put into the ghost-fluid
        rule this is a Robin condition: the face takes theta + mu/dx in place of theta, and the load mu (g_eff dt + w* - w_old),
        w* the face's velocity before the pressure step. At rest it gives the hydrostatic pressure with the head's weight; in
        motion the stout carries the head's inertia, implicitly (an explicit, lagged load would be unstable for short waves:
        mu k = 5.1 mm x 2094 1/m = 10.7 at the grid's shortest wave)."""
        dx = self.dx; diag = jnp.zeros(self.dims, F32); div = jnp.zeros(self.dims, F32); rhs = jnp.zeros(self.dims, F32)
        cp, cm, faces, loads = [], [], [], []
        ps3 = jnp.broadcast_to(ps[:, :, None], self.dims).astype(F32)
        if pst is not None: ps3 = (ps3 + pst).astype(F32)               # surface tension (continuous model): gamma kappa, solver units
        for ax in range(3):
            thv = self.th[ax]; liqL, liqR, tLR, tRL = self._faces(ph, liq, ax)
            th = thv if beta is None else thv * beta[ax]   # Step 4: variable density in the coefficients only (rho / rho_f); the divergence stays volume-based
            surf = None
            if ax == 2 and mu is not None:                                   # the head's mass on the faces the surface crosses
                surf = liqL & ~liqR & (th > 0); muF = jnp.broadcast_to(mu[:, :, None], tLR.shape)
                tLR = jnp.where(surf, tLR + muF / dx, tLR)
            faces.append((liqL, liqR, tLR, tRL))
            open_ = th > 0
            dL = jnp.where(open_, jnp.where(liqR, th, th / tLR), 0.0)
            dR = jnp.where(open_, jnp.where(liqL, th, th / tRL), 0.0)
            diag = diag + cut_hi(dL, ax) + cut_lo(dR, ax)
            psL, psR = lo(ps3, ax, 0.0), hi(ps3, ax, 0.0)
            if surf is not None:
                psR = jnp.where(surf, muF * (geff_dt + vel[2] - w_old), psR).astype(F32)
            loads.append((psL, psR))
            sL = jnp.where(open_ & liqL & ~liqR, th * psR / tLR, 0.0)      # liquid L, air R: the surface load seen by L
            sR = jnp.where(open_ & liqR & ~liqL, th * psL / tRL, 0.0)
            rhs = rhs + cut_hi(sL, ax) + cut_lo(sR, ax)
            cp.append(cut_hi(th * liqR, ax)); cm.append(cut_lo(th * liqL, ax))
            flux = thv * vel[ax]; div = div + cut_hi(flux, ax) - cut_lo(flux, ax)
        if src is not None: div = div - src                              # the volume correction's target outflow (m/s), see __init__
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
            return (it < self.maxit) & (rn >= self.tol * bn) & (rn >= self.atol) & ok & (bn > 0)

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
            qL, qR = loads[ax]                                         # the head's load on the surface, as in the matrix
            psR = jnp.where(liqR, pR, jnp.where(liqL, pL * (1.0 - 1.0 / tLR) + qR / tLR, 0.0))
            psL = jnp.where(liqL, pL, jnp.where(liqR, pR * (1.0 - 1.0 / tRL) + qL / tRL, 0.0))
            upd = (self.th[ax] > 0) & (liqL | liqR)
            bta = 1.0 if beta is None else beta[ax]
            f = jnp.where(upd, vel[ax] - bta * (psR - psL) / dx, vel[ax]); k = upd
            if ax == 2:
                f = jnp.where(self.floor_w, 0.0, f); k = k | self.floor_w
            out.append(f.astype(F32)); known.append(k)
        return out, known, p, it, rn / jnp.maximum(bn, 1e-30), rn, bn

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
    def g2p(self, s, vel, dt, gx, gz, rot=None, uc=None, vel_out=None):
        dx = self.dx; G = self.G; X, act = s["xp"], s["act"]
        g = (X - self.origin) / dx; vs, Cs, us = [], [], []
        if vel_out is not None: pin = self.p_side(X)   # Step 2: vel is the cavity side's copy, vel_out the outside's
        for comp in range(3):
            fl, ok, w, wv, cf, fr = self._corners(g, comp, self.fshape[comp])
            val = jnp.where(ok, vel[comp].reshape(-1)[fl], 0.0)                    # (8, N)
            if vel_out is not None:
                val = jnp.where(pin[None, :], val, jnp.where(ok, vel_out[comp].reshape(-1)[fl], 0.0))
            vs.append(jnp.sum(w * val, 0))
            if uc is not None: us.append(jnp.sum(w * jnp.where(ok, uc[comp].reshape(-1)[fl], 0.0), 0))
            sg = 2.0 * cf - 1.0                                                     # d(weight)/d(fraction) signs
            gw = jnp.stack([sg[..., 0] * wv[..., 1] * wv[..., 2], wv[..., 0] * sg[..., 1] * wv[..., 2], wv[..., 0] * wv[..., 1] * sg[..., 2]], -1)
            Cs.append(jnp.sum(val[..., None] * gw, 0) / dx)
        newv = jnp.stack(vs, -1); C = jnp.stack(Cs, 1)
        Xn = X + dt * (newv if uc is None else newv + jnp.stack(us, -1))     # the volume correction's drift moves the particle, not its velocity
        if self.cont: return self._g2p_cont(s, X, Xn, newv, C, act, dt, gx, gz, rot)
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
        # a drop that comes down on the cart's body (its top is BODY_TOP below the glass's inner floor) stays where it lands
        if rot is None: acc = jnp.array([gx, 0.0, gz], F32)
        else:
            a_x, a_z = self.frame_accel(s["xp"][:, 0], s["xp"][:, 2], s["vp"][:, 0], s["vp"][:, 2], gx, gz, rot)
            acc = jnp.stack([a_x, jnp.zeros_like(a_x), a_z], -1)
        fly = s["fly"]; vf = s["vp"] + dt * acc; xf = s["xp"] + dt * vf
        hit = fly & (xf[:, 2] < BODY_TOP) & (s["xp"][:, 2] >= BODY_TOP) & (jnp.abs(xf[:, 0]) < BODY_HALF[0]) & (jnp.abs(xf[:, 1]) < BODY_HALF[1])
        xf = jnp.where(hit[:, None], xf.at[:, 2].set(BODY_TOP), xf); vf = jnp.where(hit[:, None], 0.0, vf)
        land = fly & ~hit & (xf[:, 2] < -0.25)
        xp = jnp.where(act[:, None], Xn, jnp.where(fly[:, None], xf, s["xp"]))
        vp = jnp.where(act[:, None], newv, jnp.where(fly[:, None], vf, s["vp"]))
        fly2 = (fly & ~land & ~hit) | leave
        s = dict(s, xp=xp.astype(F32), vp=vp.astype(F32), C=jnp.where(act[:, None, None], C, 0.0).astype(F32),
                 act=act2, fly=fly2, landed=s["landed"] | land, stuck=s["stuck"] | hit)
        mom = jnp.sum(jnp.where(act2[:, None], newv, 0.0).astype(F64), 0)
        return s, mom

    def _g2p_cont(self, s, X, Xn, newv, C, act, dt, gx, gz, rot):
        """The continuous model's particle update (18 Nov 2026). Every particle stays a particle of the same liquid wherever it is:
        no free flight, no change of equations at the rim. The glass (wall shell, foot) and the cart's body are solids: a particle
        that a step carries into one is put back on the side it came from, a tenth of a cell off the surface, and loses its velocity
        into the surface (no penetration; sliding is left to the liquid's viscosity and the wall layer). A particle above the grid's
        top feels the same body force with no pressure (the air's p = 0), as a drop in the air does on the grid. A particle that
        leaves the grid sideways or below it has fallen off the cart: it leaves the computation and its mass the cart (landed)."""
        G = self.G; dx = self.dx; hx, hy, zt = G.body; W = G.WALL; eps = 0.1 * dx; zr_ = G.zrim
        # above the grid: the body force alone (no grid values there)
        if rot is None: acc = jnp.broadcast_to(jnp.array([gx, 0.0, gz], F32), X.shape)
        else:
            a_x, a_z = self.frame_accel(X[:, 0], X[:, 2], s["vp"][:, 0], s["vp"][:, 2], gx, gz, rot)
            acc = jnp.stack([a_x, jnp.zeros_like(a_x), a_z], -1)
        topz = G.z0 + self.nz * dx
        high = X[:, 2] >= topz - 0.5 * dx
        vb = s["vp"] + dt * acc
        newv = jnp.where(high[:, None], vb, newv); Xn = jnp.where(high[:, None], X + dt * vb, Xn)
        C = jnp.where(high[:, None, None], 0.0, C)
        Xprop = Xn                                                             # diagnostic only (diag_g2p)
        # the glass: the wall shell between R(z) and R(max(z, 8 mm)) + W for 0 < z < rim, the foot below the floor
        def radii(z):
            Rin = self.Rz(jnp.clip(z, 0.0, zr_ - 1e-6)); Rout = self.Rz(jnp.clip(z, 0.008, zr_ - 1e-6)) + W
            return Rin, Rout
        ro = jnp.sqrt(X[:, 0] ** 2 + X[:, 1] ** 2); Rin_o, Rout_o = radii(X[:, 2])
        r = jnp.sqrt(Xn[:, 0] ** 2 + Xn[:, 1] ** 2); z = Xn[:, 2]; Rin, Rout = radii(z)
        er = jnp.stack([Xn[:, 0], Xn[:, 1], jnp.zeros_like(r)], -1) / jnp.maximum(r, 1e-12)[:, None]
        lip = G.lip; zcl = G.zlip                                                  # Step 3: rounded lip (lip = 0: zcl = rim, as before)
        in_wall = (z > 0) & (z < zcl) & (r >= Rin) & (r < Rout)
        in_foot = (z <= 0) & (z > zt) & (r < Rout)
        if lip > 0:   # the lip: the disc of radius lip about (R_m, zc); a particle in it goes out along the disc's radius
            dr_c = r - G.Rm; dz_c = z - zcl; dc = jnp.sqrt(dr_c ** 2 + dz_c ** 2)
            in_cap = (z >= zcl) & (dc < lip)
        else: in_cap = jnp.zeros_like(in_wall)
        hit = in_wall | in_foot
        from_top = hit & (X[:, 2] >= zr_) if lip == 0 else jnp.zeros_like(hit)   # came down onto the rim's square top
        # from inside the cavity: the old position inside it, or (if a step left it in the wall) nearer the inner face than the outer
        from_in = hit & ~from_top & (X[:, 2] > 0) & ((ro < Rin_o) | (ro - Rin_o < Rout_o - ro))
        from_out = hit & ~from_top & ~from_in                                 # from outside the glass
        # inside: back to the inner wall (or up to the cavity's floor if it came through the floor)
        floor_in = from_in & in_foot
        # back into the cavity: first up to the floor if it went through it, then in to the inner wall at that height (the floor's
        # corner is steep, R grows 2 mm per 0.5 mm: a particle lifted to the floor can still stand in the wall; smoke test 2 found 48
        # particles pushed out that way onto the body)
        zin = jnp.where(floor_in, eps, Xn[:, 2]); Rin_b = self.Rz(jnp.clip(zin, 0.0, zr_ - 1e-6))
        rin_t = jnp.where(from_in, jnp.minimum(1.0, (Rin_b - eps) / jnp.maximum(r, 1e-12)), 1.0)
        rout_t = jnp.where(from_out, (Rout + eps) / jnp.maximum(r, 1e-12), 1.0)
        sc = rin_t * rout_t
        Xn = Xn.at[:, 0].multiply(sc).at[:, 1].multiply(sc)
        Xn = Xn.at[:, 2].set(jnp.where(from_top, zr_ + eps, jnp.where(floor_in, eps, Xn[:, 2])))
        vn = jnp.sum(newv * er, -1)
        newv = jnp.where((from_in & (rin_t < 1.0) & (vn > 0))[:, None], newv - vn[:, None] * er, newv)
        newv = jnp.where((from_out & (vn < 0))[:, None], newv - vn[:, None] * er, newv)
        newv = newv.at[:, 2].set(jnp.where((from_top | floor_in) & (newv[:, 2] < 0), 0.0, newv[:, 2]))
        if lip > 0:
            ok_ = dc > 1e-9; nr_ = jnp.where(ok_, dr_c / jnp.maximum(dc, 1e-9), 0.0); nz_ = jnp.where(ok_, dz_c / jnp.maximum(dc, 1e-9), 1.0)
            rc_new = G.Rm + (lip + eps) * nr_; zc_new = zcl + (lip + eps) * nz_
            scc = jnp.where(in_cap, rc_new / jnp.maximum(r, 1e-12), 1.0)
            Xn = Xn.at[:, 0].multiply(scc).at[:, 1].multiply(scc)
            Xn = Xn.at[:, 2].set(jnp.where(in_cap, zc_new, Xn[:, 2]))
            n3 = nr_[:, None] * er + nz_[:, None] * jnp.array([0.0, 0.0, 1.0], F32)[None, :]
            vnc = jnp.sum(newv * n3, -1)
            newv = jnp.where((in_cap & (vnc < 0))[:, None], newv - vnc[:, None] * n3, newv)
        if self.wall_guard:   # Step 3 (plan 2.4): a particle in the cavity stays at least 1e-5 m inside the inner wall (float32 grazing)
            rg = jnp.sqrt(Xn[:, 0] ** 2 + Xn[:, 1] ** 2); Rg = self.Rz(jnp.clip(Xn[:, 2], 0.0, zr_ - 1e-6))
            gd = (Xn[:, 2] > 0) & (Xn[:, 2] < zcl) & (rg < Rg) & (rg > Rg - 1e-5)
            sg_ = jnp.where(gd, (Rg - 1e-5) / jnp.maximum(rg, 1e-12), 1.0)
            Xn = Xn.at[:, 0].multiply(sg_).at[:, 1].multiply(sg_)
        # the cart's body top
        deck = (Xn[:, 2] < zt + eps) & (jnp.abs(Xn[:, 0]) < hx) & (jnp.abs(Xn[:, 1]) < hy) & (X[:, 2] >= zt)
        Xn = Xn.at[:, 2].set(jnp.where(deck, zt + eps, Xn[:, 2]))
        newv = newv.at[:, 2].set(jnp.where(deck & (newv[:, 2] < 0), 0.0, newv[:, 2]))
        # off the cart: outside the grid sideways or below it
        hxg, hyg = -G.x0, -G.y0
        gone = act & ((jnp.abs(Xn[:, 0]) > hxg - 0.5 * dx) | (jnp.abs(Xn[:, 1]) > hyg - 0.5 * dx) | (Xn[:, 2] < G.z0 + 0.5 * dx))
        act2 = act & ~gone
        xp = jnp.where(act[:, None], Xn, s["xp"]); vp = jnp.where(act[:, None], newv, s["vp"])
        s = dict(s, xp=xp.astype(F32), vp=vp.astype(F32), C=jnp.where(act2[:, None, None], C, 0.0).astype(F32),
                 act=act2, landed=s["landed"] | gone)
        if self.diag_g2p: s = dict(s, xprop=Xprop.astype(F32), g2p_glass=hit | in_cap)
        mom = jnp.sum(jnp.where(act2[:, None], newv, 0.0).astype(F64), 0)
        return s, mom

    # ---------------------------------------------------------------- one fluid step (Taichi Stout.step)
    def prepare(self, s):
        """The part of a step that depends only on the particles: their velocities on the grid, the level set, the surface. The
        ride computes it before the cart's sub-steps, so the wall probes read the surface the last fluid step left (as
        World.readProbes in stout-cart.js), and the step then reuses it."""
        if self.evp: vel, mass, cnt, ex = self.p2g_evp(s)
        else: vel, mass, cnt = self.p2g(s); ex = None
        ph, liq, nsel, phr = self.level_set(s, cnt)
        H, _ = self.surface(phr)
        return dict(vel=vel, mass=mass, cnt=cnt, ph=ph, liq=liq, nsel=nsel, phr=phr, H=H, **({"ex": ex} if self.evp else {}))

    def probes(self, H):
        """The two level probes on the glass's wall at r = R(fill), theta = 0 (front) and pi (back), read as
        Fluid.columnHeightAt of stout-cart.js reads them: beyond r1 = R - 2.5 dx the height is extended straight along the
        radius from r1 and r1 - 1.5 dx, each read bilinearly from the columns (columns without a surface left out).
        Returns y_q = (eta_front - eta_back)/2."""
        G = self.G; dx = self.dx; r = G.Rfill; r1 = r - 2.5 * dx; r2 = r1 - 1.5 * dx
        Hf = jnp.where(jnp.isfinite(H), H, 0.0); w0 = jnp.isfinite(H).astype(F32)
        def bil(x, y):
            fx = (x - G.x0) / dx - 0.5; fy = (y - G.y0) / dx - 0.5
            i = jnp.clip(jnp.floor(fx).astype(I32), 0, self.nx - 2); j = jnp.clip(jnp.floor(fy).astype(I32), 0, self.ny - 2)
            tx = fx - i; ty = fy - j
            ws = [((1 - tx) * (1 - ty), i, j), (tx * (1 - ty), i + 1, j), ((1 - tx) * ty, i, j + 1), (tx * ty, i + 1, j + 1)]
            num = sum(w * w0[a, b] * Hf[a, b] for w, a, b in ws); den = sum(w * w0[a, b] for w, a, b in ws)
            return num / jnp.maximum(den, 1e-9)
        def at(sgn):
            h1, h2 = bil(sgn * r1, 0.0), bil(sgn * r2, 0.0)
            return h1 + (r - r1) * (h1 - h2) / (r1 - r2)
        return (0.5 * (at(1.0) - at(-1.0))).astype(F64)

    def probes_patch(self, H):
        """Fig. 16's level probes as an area sensor (15 Nov 2026): each probe reads the median height of the columns whose centres lie
        within a patch on the glass's axis of travel, r1 - 2.4 dx <= |x| <= r1 + 0.7 dx and |y| <= 1.5 dx (3 x 3 columns at dx = 1.5 mm, centres 33.0, 34.5, 36.0 mm) (r1 = R - 2.5 dx), so one
        column that spikes for one picture (a drop landing at the wall, or the surface finder's fallback; audit M3: 5 mm in one
        column for 1/60 s) cannot move it; y_q = (median_front - median_back)/2 divided by the first mode's shape at the patch's mean
        radius, J1(xi r_p / R) / J1(xi), so that y_q reads the swing's height at the wall, as probes() does. Fig. 12 never calls it."""
        if not hasattr(self, "_patch"):
            G = self.G; dx = self.dx; c = G.x0 + (np.arange(self.nx) + 0.5) * dx; cy = G.y0 + (np.arange(self.ny) + 0.5) * dx; r1 = G.Rfill - 2.5 * dx
            X, Y = np.meshgrid(c, cy, indexing="ij"); idx = {}
            for s in (1, -1):
                m = (s * X >= r1 - 2.4 * dx) & (s * X <= r1 + 0.7 * dx) & (np.abs(Y) <= 1.5 * dx)   # 3 x 3 columns at dx 1.5 mm
                idx[s] = (jnp.asarray(np.nonzero(m)[0]), jnp.asarray(np.nonzero(m)[1]), float(np.mean(np.abs(X[m]))))
            from scipy.special import j1
            rp = 0.5 * (idx[1][2] + idx[-1][2]); xi = 1.8411837813406593
            self._patch = (idx, float(j1(xi * rp / G.Rfill) / j1(xi)))
        idx, shape = self._patch
        med = lambda s: jnp.nanmedian(H[idx[s][0], idx[s][1]])
        return jnp.nan_to_num(0.5 * (med(1) - med(-1)) / shape).astype(F64)

    def evp_grad(self, X, vel):
        """25 Nov 2026 (flag evp_consistent): the velocity gradient C[i, a] = sum over the 8 MAC corners of u_i grad_a w, at positions X,
        with exactly the weights and weight gradients P2G uses for F_dev. With vel = the kick's velocity (see step), sum_p V_p tau_p : C_p
        equals the kinetic energy the F_dev kick takes from the grid divided by dt: the return map then works on the deformation the
        stress force acted on (the discrete adjoint), so the foam cannot dissipate energy the flow never gave it."""
        dx = self.dx; g = (X - self.origin) / dx; Cs = []
        for comp in range(3):
            fl, ok, w, wv, cf, fr = self._corners(g, comp, self.fshape[comp])
            val = jnp.where(ok, vel[comp].reshape(-1)[fl], 0.0)
            sg = 2.0 * cf - 1.0
            gw = jnp.stack([sg[..., 0] * wv[..., 1] * wv[..., 2], wv[..., 0] * sg[..., 1] * wv[..., 2], wv[..., 0] * wv[..., 1] * sg[..., 2]], -1)
            Cs.append(jnp.sum(val[..., None] * gw, 0) / dx)
        return jnp.stack(Cs, 1)

    def step(self, s, dt, gx, gz, prep=None, rot=None, wind=None):
        """rot = (om, al, zS): the glass also turns (Fig. 16); None: the glass only translates (Fig. 12, unchanged)."""
        dt = jnp.asarray(dt, F32); gx = jnp.asarray(gx, F32); gz = jnp.asarray(gz, F32)
        if rot is not None: rot = tuple(jnp.asarray(r, F32) for r in rot)
        pr = self.prepare(s) if prep is None else prep
        aud = self.evp and self.audit; s0 = s
        vel, mass = pr["vel"], pr["mass"]
        # 13 Nov 2026, run 3: gravity's kick of this step (dt g) was added before the viscous and thin-layer stresses, so the glass's
        # Stokes layer and the head braked gravity itself: a pint at rest lost 0.63 mJ of potential energy in 2 s, the books
        # counted 0.77 mJ "dissipated", and the stout stirred (up to 3.7 mm/s). The stresses now act on the velocity the stout
        # has (the last step's, free of divergence); the body force is added after them, just before the pressure step.
        vel = self.normalize_force(vel, mass, dt, 0.0, 0.0)
        # the head's vertical velocity as the step starts: its own, kept from the last step (the particles' hand-over smooths
        # the stout's velocity at the surface, and the head's momentum equation must close step by step)
        w_old = jnp.broadcast_to(s["wh"][:, :, None], vel[2].shape)
        ph, liq, nsel, H = pr["ph"], pr["liq"], pr["nsel"], pr["H"]
        ex = pr.get("ex") if self.evp else None
        if aud: au = [vel]
        if self.nu > 0: vel = self.viscosity(vel, mass, dt, fh=None if ex is None else ex["fh"])
        if aud: au.append(vel)
        z = jnp.zeros((), F64); ew = es = ef = z
        if self.evp:   # Step 4: the glass's stress (stout and head), then the head's deviatoric force u += dt F_dev / max(M_f, m_floor)
            vel, ew_s, ew_f = self.friction_evp(vel, mass, dt, ex); ew = ew_s + ew_f
            if aud: au.append(vel)
            v_bk = vel
            vel = [jnp.where((self.th[c] > 0) & (mass[c] > 1e-6), vel[c] + dt * ex["Fdev"][c] / jnp.maximum(ex["M"][c], self.m_floor), vel[c]).astype(F32)
                   for c in range(3)]
            if aud: au.append(vel)
            if getattr(self, "evp_consistent", False):   # the kick's work-conjugate velocity: (M / max(M, m_floor)) x the kick's midpoint
                # velocity on the kicked faces, 0 elsewhere; then sum_f u_k . F_dev dt is exactly the kick's kinetic-energy change
                uk = [jnp.where((self.th[c] > 0) & (mass[c] > 1e-6), ex["M"][c] / jnp.maximum(ex["M"][c], self.m_floor) * 0.5 * (v_bk[c] + vel[c]), 0.0).astype(F32)
                      for c in range(3)]
        elif self.gs > 0 or self.skin or self.head: vel, ew, es, ef = self.friction(vel, mass, ph, liq, dt, s["hf"])
        vel = self.body_force(vel, mass, dt, gx, gz, rot)
        if self.cont and wind is not None: vel = self.air_drag(vel, mass, pr["ph"], pr["liq"], dt, wind, beta=None if ex is None else ex["beta"])
        # the head's weight on the surface (verification.md item 4), in the solver's pressure units (Pa x dt / rho); with rot, the
        # vertical field of each column at the fill height
        gzh = gz if rot is None else self.frame_accel(self.colx, self.G.fill, 0.0, 0.0, gx, gz, rot)[1]
        ps = (self.rho_f * s["hf"] * jnp.maximum(-gzh, 0.0) * dt / self.rho).astype(F32) if self.head else jnp.zeros((self.nx, self.ny), F32)
        mu = (self.rho_f * s["hf"] / self.rho).astype(F32) if (self.head and self.head_mass) else None
        gdt = jnp.maximum(-gzh, 0.0) * dt
        if rot is not None: gdt = gdt[:, :, None]
        uc = None
        if self.vol_corr > 0:   # the volume correction moves positions only (Kugelstadt et al. 2019): its own projection of a zero velocity field
            # the gate (run 4b): the correction acts only while the whole pint has swollen by more than 4 % (fully from 8 %); run 4 without
            # it stirred the pint at rest at 1.5 mm (rest guard: 1.54 mm, limit 0.75 mm)
            gate = jnp.clip((self.swelling(liq, s["act"]) - 0.04) / 0.04, 0.0, 1.0).astype(F32)
            src = self.volume_source(pr["cnt"], liq, dt, gate); zf = [jnp.zeros_like(v) for v in vel]
            uc, kc, _, _, _, _, _ = self.pressure(zf, ph, liq, jnp.zeros_like(s["p"]), jnp.zeros((self.nx, self.ny), F32), src=src)
            uc = self.extrapolate(uc, kc)
        pst = self.tension(ph, s["hf"], dt) if self.cont else None
        vel, known, p, it, res, res_abs, bnorm = self.pressure(vel, ph, liq, s["p"], ps, mu=mu, w_old=w_old, geff_dt=gdt, pst=pst,
                                               beta=None if ex is None else ex["beta"])
        if aud: au.append(vel)
        if mu is not None:   # the head's new vertical velocity: that of the face its surface crosses (liquid below, air above)
            sf = self._surf_faces(ph, liq); nsf = jnp.sum(sf, 2)
            wh = jnp.where(nsf > 0, jnp.sum(jnp.where(sf, vel[2], 0.0), 2) / jnp.maximum(nsf, 1), s["wh"]).astype(F32)
            s = dict(s, wh=wh)
        if self.side_vis:   # Step 2: one extrapolated copy per side of the glass below the rim (see enable_side_vis)
            vel_out = self.extrapolate(vel, [k & (~fs | ~fb) for k, fs, fb in zip(known, self.fside, self.fbelow)])
            vel = self.extrapolate(vel, [k & (fs | ~fb) for k, fs, fb in zip(known, self.fside, self.fbelow)])
        else:
            vel = self.extrapolate(vel, known); vel_out = None
        s, mom = self.g2p(s, vel, dt, gx, gz, rot, uc=uc, vel_out=vel_out)
        evd = {}
        if self.evp:   # Step 4: the head's return map, after G2P, with the APIC velocity gradient C of the new step
            if getattr(self, "evp_consistent", False):   # the gradient of the kick's velocity at the P2G positions (step start)
                ben, yl, gp, s_new, det, rres = evp_return_map(s["be"], self.evp_grad(s0["xp"], uk), dt, hw=getattr(self, "evp_hw", False))
            else:
                ben, yl, gp, s_new, det, rres = evp_return_map(s["be"], s["C"], dt, hw=getattr(self, "evp_hw", False))
            hd = s["is_head"] & s["act"]
            if aud: s, adiag = self._audit_evp(s0, s, au, vel, mass, ex, dt, gz, ben, yl, gp, s_new, hd)
            s = dict(s, be=jnp.where(hd[:, None], ben, s["be"]))
            mpart = s["pmass"].astype(F64)
            okf = [(self.th[c] > 0) & (mass[c] > 1e-6) for c in range(3)]
            n_floor = sum(jnp.sum(okf[c] & (ex["M"][c] < self.m_floor), dtype=I32) for c in range(3))           # diagnostic: faces where
            n_floor_head = sum(jnp.sum(okf[c] & (ex["M"][c] < self.m_floor) & (ex["fh"][c] > 0.5), dtype=I32) for c in range(3))  # m_floor acts
            e_plastic = jnp.sum(jnp.where(hd & yl, s["pvol"].astype(F64) * s_new.astype(F64) * gp.astype(F64), 0.0)) * dt   # sum V_p s gp dt (J)
            evd = dict(e_wall_stout=ew_s, e_wall_foam=ew_f, e_plastic=e_plastic, n_yielded=jnp.sum(hd & yl, dtype=I32), gp_max=jnp.max(jnp.where(hd, gp, 0.0)), s_max=jnp.max(jnp.where(hd, s_new, 0.0)),
                       det_min=jnp.min(jnp.where(hd, det, 1.0)), det_max=jnp.max(jnp.where(hd, det, 1.0)), rm_res=jnp.max(jnp.where(hd, rres, 0.0)),
                       mom_phys=jnp.sum(jnp.where(s["act"][:, None], mpart[:, None] * s["vp"].astype(F64), 0.0), 0), n_floor=n_floor, n_floor_head=n_floor_head)
            if aud: evd.update(adiag)
        if self.head: s = self.head_spill(s, H, dt, gx, gz, rot)
        s = dict(s, p=p, ewall=s["ewall"] + ew, eskin=s["eskin"] + es, efoam=s["efoam"] + ef)
        vmax = jnp.max(jnp.where(s["act"][:, None], jnp.abs(s["vp"]), 0.0))
        mhead = self.rho_f * jnp.sum((s["hf"] * self.afill).astype(F64)) * self.dx ** 2
        diag = dict(it=it, res=res, res_abs=res_abs, bnorm=bnorm, conv=(res < self.tol) | (res_abs < self.atol), mom=mom, nact=jnp.sum(s["act"], dtype=I32),
                    nsel=nsel, vmax=vmax, mhead=mhead, **evd)
        return s, diag

    def _audit_evp(self, s0, s, au, velx, mass, ex, dt, gz, ben, yl, gp, s_new, hd):
        """Instruction 0004 (23 Nov 2026), diagnostic only (self.audit): reads the step, changes no motion. s0 the state at the step's
        start, s after G2P (be not yet updated), au = the grid velocities after P2G, viscosity, friction_evp, F_dev and the pressure step,
        velx the extrapolated (cavity-side) field G2P read. Returns s with the shadow be_cell updated, and the diagnostics (J, float64):
        KE_g = sum over occupied open faces 0.5 M_f u^2; the ledger dE_P2G, dE_visc, dE_wall, dE_dev, dE_grav_proj (with PE of the
        positions before collisions, xprop), dE_G2P_coll, and dE_mech; U_el = sum_head V (G/2)(tr be - 3) after the return map; E_drop =
        sum_yielded V (G/2)(tr be_trial - tr be_new); W_trial = sum_head V (G/2)(tr be_trial - tr be_old); E_plastic split: particles
        whose P2G corners touch an occupied face with M_f < m_floor / else within 1.5 dx of the inner wall / else interior; the shadow
        be_cell driven by f = I + dt D_cell (D_cell the symmetric cell-centred strain rate of velx, the particle's cell) and its
        E_plastic_cellD."""
        F6 = F64; dx = self.dx; gg = -gz.astype(F6)
        okf = [(self.th[c] > 0) & (mass[c] > 1e-6) for c in range(3)]; M6 = [ex["M"][c].astype(F6) for c in range(3)]
        KEg = lambda v: sum(jnp.sum(jnp.where(okf[c], 0.5 * M6[c] * v[c].astype(F6) ** 2, 0.0)) for c in range(3))
        k0, k1, k2, k3, k5 = [KEg(v) for v in au]
        pm = s0["pmass"].astype(F6); a0 = s0["act"]; a1 = s["act"]
        KEb = 0.5 * jnp.sum(jnp.where(a0, pm * jnp.sum(s0["vp"].astype(F6) ** 2, 1), 0.0)); PEb = gg * jnp.sum(jnp.where(a0, pm * s0["xp"][:, 2].astype(F6), 0.0))
        PEp = gg * jnp.sum(jnp.where(a0, pm * s["xprop"][:, 2].astype(F6), 0.0))
        KEa = 0.5 * jnp.sum(jnp.where(a1, pm * jnp.sum(s["vp"].astype(F6) ** 2, 1), 0.0)); PEa = gg * jnp.sum(jnp.where(a1, pm * s["xp"][:, 2].astype(F6), 0.0))
        dW = [jnp.where(okf[c], 0.5 * M6[c] * (au[2][c].astype(F6) ** 2 - au[3][c].astype(F6) ** 2), 0.0) for c in range(3)]
        d = dict(aud_KE_p=KEa, aud_PE=PEa, aud_dE_P2G=k0 - KEb, aud_dE_visc=k1 - k0, aud_dE_wall=k2 - k1, aud_dE_dev=k3 - k2,
                 aud_dE_grav_proj=k5 - k3 + PEp - PEb, aud_dE_G2P_coll=KEa - k5 + PEa - PEp, aud_dE_mech=KEa + PEa - KEb - PEb,
                 aud_W_sg_mfloor=sum(jnp.sum(jnp.where(ex["M"][c] < self.m_floor, dW[c], 0.0)) for c in range(3)),
                 aud_n_gone=jnp.sum(a0 & ~a1, dtype=I32))
        V = s["pvol"].astype(F6); trf = lambda b: (b[:, 0] + b[:, 1] + b[:, 2]).astype(F6)
        trn = trf(ben); tro = trf(s["be"]); trt = evp_trial_trace(s["be"], s["C"], dt).astype(F6); Gh = 0.5 * G_HEAD
        epl = jnp.where(hd & yl, V * s_new.astype(F6) * gp.astype(F6), 0.0) * dt.astype(F6)
        X0 = s0["xp"]; g = (X0 - self.origin) / dx; mfl = jnp.zeros(self.N, bool)
        for c in range(3):
            fl, ok, w, wv, cf, fr = self._corners(g, c, self.fshape[c])
            flag = (okf[c] & (ex["M"][c] < self.m_floor)).reshape(-1)[fl] & ok
            mfl = mfl | jnp.any(flag, 0)
        r0 = jnp.hypot(X0[:, 0], X0[:, 1]); z0 = X0[:, 2]; G = self.G
        nearw = (z0 < G.zrim) & (self.Rz(jnp.clip(z0, 0.0, G.zrim - 1e-6)) - r0 < 1.5 * dx) & ~mfl
        inter = ~mfl & ~nearw
        d.update(aud_U_el=jnp.sum(jnp.where(hd, V * Gh * (trn - 3.0), 0.0)), aud_E_drop=jnp.sum(jnp.where(hd & yl, V * Gh * (trt - trn), 0.0)),
                 aud_W_trial=jnp.sum(jnp.where(hd, V * Gh * (trt - tro), 0.0)), aud_E_pl_mfloor=jnp.sum(jnp.where(mfl, epl, 0.0)),
                 aud_E_pl_wall=jnp.sum(jnp.where(nearw, epl, 0.0)), aud_E_pl_interior=jnp.sum(jnp.where(inter, epl, 0.0)),
                 aud_ny_mfloor=jnp.sum(hd & yl & mfl, dtype=I32), aud_ny_wall=jnp.sum(hd & yl & nearw, dtype=I32), aud_ny_interior=jnp.sum(hd & yl & inter, dtype=I32),
                 aud_n_head_mfloor=jnp.sum(hd & mfl, dtype=I32), aud_n_head_wall=jnp.sum(hd & nearw, dtype=I32))
        # the shadow: cell-centred L = grad u of the field G2P read, D = sym(L), the particle's cell at its P2G position
        Uc = [0.5 * (cut_lo(velx[a], a) + cut_hi(velx[a], a)) for a in range(3)]
        L = [[(cut_hi(velx[a], a) - cut_lo(velx[a], a)) / dx if a == b else (sh(Uc[a], 1, b, 0.0) - sh(Uc[a], -1, b, 0.0)) / (2.0 * dx)
              for b in range(3)] for a in range(3)]
        Dc = jnp.stack([jnp.stack([0.5 * (L[a][b] + L[b][a]) for b in range(3)], -1) for a in range(3)], -2).reshape(-1, 3, 3)
        flc, okc = self.flat(jnp.floor(g).astype(I32), self.dims)
        Dp = jnp.where(okc[:, None, None], Dc[flc], 0.0).astype(F32)
        bc, yc, gpc, sc, _, _ = evp_return_map(s0["be_cell"], Dp, dt)
        d.update(aud_E_pl_cellD=jnp.sum(jnp.where(hd & yc, V * sc.astype(F6) * gpc.astype(F6), 0.0)) * dt.astype(F6),
                 aud_ny_cellD=jnp.sum(hd & yc, dtype=I32), aud_s_max_cellD=jnp.max(jnp.where(hd, sc, 0.0)))
        return dict(s, be_cell=jnp.where(hd[:, None], bc, s0["be_cell"])), d

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
        ph, liq, nsel, phr = self.level_set(s, cnt)
        H, nfb = self.surface(phr)
        # drops
        X, act, fly = s["xp"], s["act"], s["fly"]
        i = jnp.clip(jnp.floor((X[:, 0] - G.x0) / dx).astype(I32), 0, self.nx - 1)
        j = jnp.clip(jnp.floor((X[:, 1] - G.y0) / dx).astype(I32), 0, self.ny - 1)
        # a drop stands more than 1.5 dx above the surface of its column and of the eight around it (stout climbing the glass in a
        # cut column is not a drop)
        Hm = jnp.where(jnp.isfinite(H), H, -jnp.inf); Hm = jnp.maximum(Hm, jnp.maximum(sh(Hm, 1, 0, -jnp.inf), sh(Hm, -1, 0, -jnp.inf)))
        Hm = jnp.maximum(Hm, jnp.maximum(sh(Hm, 1, 1, -jnp.inf), sh(Hm, -1, 1, -jnp.inf)))
        Hp = Hm[i, j]
        loose = act & jnp.isfinite(Hp) & (X[:, 2] > Hp + 1.5 * dx)
        dmask = loose | fly | s["stuck"]
        if self.cont:   # the continuous model: also every particle outside the glass's cavity (down the glass, on the cart, in the air)
            rX = jnp.sqrt(X[:, 0] ** 2 + X[:, 1] ** 2)
            incav = (X[:, 2] > 0) & (rX < self.Rz(jnp.clip(X[:, 2], 0.0, G.zrim - 1e-6)))
            fly = act & ~incav; dmask = loose | fly
        nd = jnp.sum(dmask, dtype=I32)
        di = jnp.nonzero(dmask, size=self.M, fill_value=0)[0]
        drops = jnp.where((jnp.arange(self.M) < nd)[:, None], X[di], jnp.nan)
        # books
        v = s["vp"].astype(F64); z = X[:, 2].astype(F64)
        KE = 0.5 * self.mp * jnp.sum(jnp.where(act[:, None], v * v, 0.0))
        PE = self.mp * 9.81 * jnp.sum(jnp.where(act, z, 0.0))
        Px = self.mp * jnp.sum(jnp.where(act, v[:, 0], 0.0))
        return dict(H=H, nfallback=nfb, drops=drops.astype(F32), ndrops=nd, nloose=jnp.sum(loose, dtype=I32), nfly=jnp.sum(fly, dtype=I32),
                    nlanded=jnp.sum(s["landed"], dtype=I32), nstuck=jnp.sum(s["stuck"], dtype=I32), nact=jnp.sum(act, dtype=I32), KE=KE, PE=PE, Px=Px,
                    ewall=s["ewall"], efoam=s["efoam"], eskin=s["eskin"], nliq=jnp.sum(liq, dtype=I32), nsel=nsel,
                    hf=s["hf"], lumps=s["bx"], lumpvol=s["bvol"], foam_spill=s["foam_spill"], foam0=s["foam0"],
                    vhead=jnp.sum((s["hf"] * self.afill).astype(F64)) * dx * dx)   # the head still in the glass (m^3), for the books

    def polar(self, H, nr=16, nth=64, Rmax=None):
        """The stored surface H sampled (bilinear, on the GPU) on rings r = Rmax ir / nr, theta = 2 pi ith / nth;
        Rmax defaults to the glass's radius at the fill less half a cell (the last columns whose centres are in the glass)."""
        G = self.G; dx = self.dx; Rmax = (G.Rfill - 0.5 * dx) if Rmax is None else Rmax
        r = Rmax * jnp.arange(nr + 1) / nr; th = 2 * jnp.pi * jnp.arange(nth) / nth
        x = r[:, None] * jnp.cos(th)[None]; y = r[:, None] * jnp.sin(th)[None]
        fx = (x - G.x0) / dx - 0.5; fy = (y - G.y0) / dx - 0.5
        i = jnp.clip(jnp.floor(fx).astype(I32), 0, self.nx - 2); j = jnp.clip(jnp.floor(fy).astype(I32), 0, self.ny - 2)
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


CTRL = {"off": 0, "speed": 1, "preview": 2, "slosh": 3, "joint": 4}


def slosh_lqr(Mx, b, cx, w, z, be, Imax, lim=None):
    """Cart.lqrGains of stout-cart.js: LQR on x = (dv, q, q', xi), u = di, for M_x dv' = b di - c_x dv,
    q'' = -w^2 q - 2 zeta w q' - beta dv', xi' = -dv; Bryson weights 1/(0.05 m/s)^2, 1/(2 mm)^2, 1/(2 mm w)^2, 1/(0.02 m)^2,
    r = 1/I_max^2. The JS integrates the Riccati flow to its steady state; here the same equation is solved directly."""
    import scipy.linalg as sl
    lim = lim or [0.05, 0.002, 0.002 * w, 0.02]
    A = np.array([[-cx / Mx, 0, 0, 0], [0, 0, 1, 0], [be * cx / Mx, -w * w, -2 * z * w, 0], [-1, 0, 0, 0]])
    B = np.array([[b / Mx], [0.0], [-be * b / Mx], [0.0]]); Q = np.diag([1.0 / v ** 2 for v in lim]); r = 1.0 / Imax ** 2
    P = sl.solve_continuous_are(A, B, Q, np.array([[r]]))
    return (B.T @ P / r).ravel()


def susp_lqr(Ms, mw, k, c, kt, ct, a=0.5, sm=0.010, d=0.0002, u=40.0):
    """Cart.suspGains of stout-cart.js: the quarter car's LQR on y = (stroke, v_b, v_w, tyre compression), cost on the body's
    acceleration a (cross term), the stroke, the tyre's compression and the force (Bryson: 0.5 m/s^2, 10 mm, 0.2 mm, 40 N)."""
    import scipy.linalg as sl
    A = np.array([[0, 1, -1, 0], [-k / Ms, -c / Ms, c / Ms, 0], [k / mw, c / mw, -(c + ct) / mw, kt / mw], [0, 0, -1, 0]])
    B = np.array([[0.0], [1 / Ms], [-1 / mw], [0.0]])
    Ca = np.array([-k / Ms, -c / Ms, c / Ms, 0]); Da = 1 / Ms; wa = 1 / a ** 2
    Q = wa * np.outer(Ca, Ca) + np.diag([1 / sm ** 2, 0, 0, 1 / d ** 2]); N = (wa * Ca * Da)[:, None]; R = wa * Da * Da + 1 / u ** 2
    P = sl.solve_continuous_are(A, B, Q, np.array([[R]]), s=N)
    return ((B.T @ P + N.T) / R).ravel()


def observer_design(w, z, be, Mx, b, cx, Ts, WF=0.5, Wa=0.002):
    """Observer.design of stout-cart.js: the Kalman filter's model on z = (v, q, q') discretised exactly for a current held
    over the sample (A_d, B_d from one exponential of [[A, B], [0, 0]] T_s), and the noise's covariance by Van Loan's method."""
    import scipy.linalg as sl
    A = np.array([[-cx / Mx, 0, 0], [0, 0, 1], [be * cx / Mx, -w * w, -2 * z * w]]); B = np.array([b / Mx, 0, -be * b / Mx])
    G = np.array([[1 / Mx, 0], [0, 0], [-be / Mx, 1]]); W = np.diag([WF, Wa])
    M4 = np.zeros((4, 4)); M4[:3, :3] = A * Ts; M4[:3, 3] = B * Ts; E4 = sl.expm(M4)
    Ad, Bd = E4[:3, :3], E4[:3, 3]
    GWG = G @ W @ G.T; M6 = np.zeros((6, 6)); M6[:3, :3] = -A; M6[:3, 3:] = GWG; M6[3:, 3:] = A.T
    E6 = sl.expm(M6 * Ts); Qd = Ad @ E6[:3, 3:]
    return Ad, Bd, 0.5 * (Qd + Qd.T)


class Cart:
    """Cart of stout-cart.js in JAX (float64), with its controllers, sampled every T_s = 1 ms (Cart.sample):
    ctrl "off" (i = c_x v0 / b), "speed" (PI with anti-windup), "preview" (PI + the road ahead one current lag early),
    "slosh" (LQR on the Kalman estimate of (v, q, q') and the integral), "joint" (the slosh LQR + the current that cancels the
    heave's parametric term + the active suspension's own LQR); susp = 1 adds the skyhook (not with "joint", which has its LQR).
    The observer (Observer of stout-cart.js) is fed by the encoder's speed every sample, the measured current held over the
    sample, and the two wall probes' half difference once per fluid step; "joint" puts the body accelerometer's a_z into its
    model. Sensor noise: none (the site's default). plant = (w, zeta, beta): the first mode as the solver has it."""

    def __init__(self, params, road):
        self.p = {k: float(v) for k, v in params.items() if k not in ("ctrl", "susp", "plant", "sensors")}
        c = params.get("ctrl", 1); self.ctrl = CTRL[c] if isinstance(c, str) else int(c); self.susp = int(params.get("susp", 0))
        self.plant = dict(params.get("plant") or dict(w=2 * math.pi * 3.42, zeta=0.005, beta=1.54))
        self.sensors = dict(dict(sigQ=0.0008, sigV=0.002, WF=0.5, Wa=0.002), **(params.get("sensors") or {}))
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

    def design(self, ml):
        """The gains and the filter, once, for the full glass (lqrGains and suspGains cache theirs on first use)."""
        P = self.p; m = self.plant; Mx = float(self.massX(ml)); b = self.bForce(); so = self.sensors
        self.K = jnp.asarray(slosh_lqr(Mx, b, P["cx"], m["w"], m["zeta"], m["beta"], P["Imax"]), F64)
        self.Ks = jnp.asarray(susp_lqr(P["Mb"] + ml, P["mw"], P["k"], P["c"], P["kt"], P["ct"]), F64)
        Ad, Bd, Qd = observer_design(m["w"], m["zeta"], m["beta"], Mx, b, P["cx"], P["Ts"], so["WF"], so["Wa"])
        self.Ad0, self.Bd0, self.Qd = jnp.asarray(Ad, F64), jnp.asarray(Bd, F64), jnp.asarray(Qd, F64)
        self.Mx0 = Mx

    def init(self, x0, ml):
        P = self.p; Ms = P["Mb"] + ml; a, d = self.axle(jnp.asarray(x0, F64))
        self.design(float(ml))
        zw = a - (Ms + P["mw"]) * P["g"] / P["kt"]; zb = zw + P["Ls"] - Ms * P["g"] / P["k"]
        z = jnp.zeros((), F64); so = self.sensors; w = self.plant["w"]
        c = dict(x=jnp.asarray(x0, F64), vx=jnp.asarray(P["v0"], F64), zb=zb, vzb=z, zw=zw, vzw=z, t=z, ml=jnp.asarray(ml, F64),
                 xi=z, us=z, uscmd=z, tS=z, ax=z, azb=z, azw=z, ireach=z, N=z,
                 # the observer (Observer.reset: at rest on the set speed, the stout still, known to the sensors' accuracy)
                 oxh=jnp.asarray([P["v0"], 0.0, 0.0], F64), oP=jnp.diag(jnp.asarray([so["sigV"] ** 2, so["sigQ"] ** 2, (so["sigQ"] * w) ** 2], F64)),
                 uPrev=z, azMeas=z, py=z, pfresh=z, ipar=z)
        i0 = self.resist(c["vx"], (P["Mb"] + ml + P["mw"]) * P["g"]) / self.bForce()
        c.update(i=i0, icmd=i0, uPrev=i0)
        return self.forces(c, 0.0, 0.0)

    def disc(self, az):
        """Observer.discretise: the swing's stiffness w^2 (1 + a_z/g) for this sample, A_d and B_d again (exact hold)."""
        P = self.p; m = self.plant; Mx = self.Mx0; b = self.bForce(); cx = P["cx"]; Ts = P["Ts"]
        w2 = m["w"] ** 2 * (1 + az / 9.81); z, be, w = m["zeta"], m["beta"], m["w"]
        M4 = jnp.zeros((4, 4), F64)
        M4 = M4.at[0, 0].set(-cx / Mx * Ts).at[1, 2].set(Ts).at[2, 0].set(be * cx / Mx * Ts).at[2, 1].set(-w2 * Ts).at[2, 2].set(-2 * z * w * Ts)
        M4 = M4.at[0, 3].set(b / Mx * Ts).at[2, 3].set(-be * b / Mx * Ts)
        E4 = jax.scipy.linalg.expm(M4)
        return E4[:3, :3], E4[:3, 3]

    def observe(self, c, u, yv, yq, fresh, az):
        """Observer.update: predict with u held since the last sample, then correct with y_v and, when the probes are fresh,
        y_q; Joseph's form."""
        so = self.sensors
        Ad, Bd = self.disc(az) if self.ctrl == 4 else (self.Ad0, self.Bd0)
        xp = Ad @ c["oxh"] + Bd * u; Pp = Ad @ c["oP"] @ Ad.T + self.Qd
        Rv, Rq = so["sigV"] ** 2, so["sigQ"] ** 2; I3 = jnp.eye(3, dtype=F64)
        # one measurement (the speed)
        S1 = Pp[0, 0] + Rv; L1 = Pp[:, 0] / S1; x1 = xp + L1 * (yv - xp[0])
        IKH1 = I3 - jnp.outer(L1, jnp.asarray([1.0, 0.0, 0.0], F64)); P1 = IKH1 @ Pp @ IKH1.T + Rv * jnp.outer(L1, L1)
        # two (speed and the probes)
        S2 = Pp[:2, :2] + jnp.diag(jnp.asarray([Rv, Rq], F64)); det = S2[0, 0] * S2[1, 1] - S2[0, 1] * S2[1, 0]
        Si = jnp.asarray([[S2[1, 1], -S2[0, 1]], [-S2[1, 0], S2[0, 0]]], F64) / det
        L2 = Pp[:, :2] @ Si; nu2 = jnp.asarray([yv, yq], F64) - xp[:2]; x2 = xp + L2 @ nu2
        H2 = jnp.asarray([[1.0, 0, 0], [0, 1.0, 0]], F64); IKH2 = I3 - L2 @ H2
        P2 = IKH2 @ Pp @ IKH2.T + L2 @ jnp.diag(jnp.asarray([Rv, Rq], F64)) @ L2.T
        x = jnp.where(fresh > 0, x2, x1); Pn = jnp.where(fresh > 0, P2, P1)
        return x, 0.5 * (Pn + Pn.T)

    def sample(self, c):
        P = self.p
        i0 = self.resist(jnp.asarray(P["v0"], F64), (P["Mb"] + c["ml"] + P["mw"]) * P["g"]) / self.bForce()
        e = P["v0"] - c["vx"]; b = self.bForce()
        if self.ctrl in (3, 4):
            # the sensors and the observer: the encoder's speed, the probes' newest reading if the fluid has stepped since the
            # last sample, the current held over the last sample; joint: the body accelerometer's a_z into the model
            az = c["azb"]
            xh, Ph = self.observe(c, c["uPrev"], c["vx"], c["py"], c["pfresh"], az)
            c = dict(c, oxh=xh, oP=Ph, uPrev=c["i"], azMeas=az, pfresh=jnp.zeros((), F64))
            K = self.K
            ic = i0 - (K[0] * (xh[0] - P["v0"]) + K[1] * xh[1] + K[2] * xh[2] + K[3] * c["xi"])
            if self.ctrl == 4:
                m = self.plant
                ipar = -self.massX(c["ml"]) * m["w"] ** 2 * (az / P["g"]) * xh[1] / (m["beta"] * b)
                ic = ic + ipar
                Ms = P["Mb"] + c["ml"]; s0 = P["Ls"] - Ms * P["g"] / P["k"]; N0 = (Ms + P["mw"]) * P["g"]
                y = jnp.stack([c["zb"] - c["zw"] - s0, c["vzb"], c["vzw"], (c["N"] - N0) / P["kt"]])
                u = jnp.clip(-jnp.dot(self.Ks, y), -P["Umax"], P["Umax"])
                xi = jnp.where(jnp.abs(ic) < P["Imax"], c["xi"] + e * P["Ts"], c["xi"])
                return dict(c, icmd=ic, xi=xi, uscmd=u, ipar=ipar)
            xi = jnp.where(jnp.abs(ic) < P["Imax"], c["xi"] + e * P["Ts"], c["xi"])
        elif self.ctrl in (1, 2):
            ic = i0 + P["Kp"] * e + P["Ki"] * c["xi"]
            if self.ctrl == 2:
                a, d = self.axle(c["x"] + c["vx"] * P["tauI"]); ic = ic + (P["Mb"] + c["ml"] + P["mw"]) * P["g"] * d / b
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
        # the controller only when a sample is due (lax.cond: the filter's matrix exponential is not computed in between)
        c = lax.cond(due, lambda cc: self.forces(self.sample(dict(cc, tS=tS - P["Ts"])), Fx, Fz), lambda cc: dict(cc, tS=tS), c)
        vx = c["vx"] + hh * c["ax"]; vzb = c["vzb"] + hh * c["azb"]; vzw = c["vzw"] + hh * c["azw"]
        c = dict(c, vx=vx, vzb=vzb, vzw=vzw, x=c["x"] + hh * vx, zb=c["zb"] + hh * vzb, zw=c["zw"] + hh * vzw,
                 i=c["ireach"] + (c["i"] - c["ireach"]) * jnp.exp(-hh / P["tauI"]),
                 us=c["uscmd"] + (c["us"] - c["uscmd"]) * jnp.exp(-hh / P["tauU"]), t=c["t"] + hh)
        return self.forces(c, Fx, Fz)


# ====================================================================== advancing to the next frame (one compiled loop)
def make_advance(S, mode, cart=None, cfl=0.8, dtmax=0.002, push=None, cut_to_frame=False):
    """Returns advance(state, t, t_end, extra) -> (state, t, extra, stats), compiled once. mode "free": glass held still,
    pushed along x by a(t) = push_a sin(pi (t - t0) / push_T) for t0 <= t < t0 + push_T (push = (t0, push_a, push_T)).
    mode "ride": the cart drives the glass; extra carries the cart's state, the stout's last momentum and its push.
    cut_to_frame (owner, 22 Nov 2026): False = dt is never shortened to land on t_end; the frame is the first step that reaches it, and
    advance returns that step's true time t >= t_end (record it). True = the old rule (last step cut to t_end), kept only to rerun old
    figures bit for bit."""
    dx = S.dx

    def body(c):
        s, t, ex, st = c
        dt = jnp.minimum(dtmax, cfl * dx / jnp.maximum(ex["vmax"], 1e-6))
        if cut_to_frame: dt = jnp.minimum(dt, ex["t_end"] - t)
        if mode == "free":
            t0, pa, pT = push; tm = t + 0.5 * dt
            ax = jnp.where((tm >= t0) & (tm < t0 + pT), pa * jnp.sin(jnp.pi * (tm - t0) / pT), 0.0)
            s, d = S.step(s, dt, -ax, -9.81)
            ex = dict(ex, vmax=d["vmax"].astype(F64))
        else:
            # World.advance of stout-cart.js: the probes read the surface the last fluid step left (fresh for the cart's
            # first sample after it; the reading at rest before the first step is the filter's start, not a measurement)
            prep = S.prepare(s)
            cs = dict(ex["cart"], py=S.probes(prep["H"]), pfresh=jnp.where(ex["probeOk"], 1.0, ex["cart"]["pfresh"]))
            vx0, vz0 = cs["vx"], cs["vzb"]
            nsub = jnp.maximum(1, jnp.round(dt / 1e-4).astype(I32)); hc = dt / nsub
            cs = lax.fori_loop(0, nsub, lambda _, cc: cart.step(cc, hc, ex["F"][0], ex["F"][1]), cs)
            ax, az = (cs["vx"] - vx0) / dt, (cs["vzb"] - vz0) / dt
            s, d = S.step(s, dt, -ax, -9.81 - az, prep=prep, wind=(-cs["vx"], -cs["vzb"]) if S.cont else None)
            P = d["mom"] * S.mp
            F = jnp.where(ex["haveP"], -(P - ex["P"]) / dt, 0.0)
            cs = dict(cs, ml=S.rho * S.V * d["nact"].astype(F64) / S.N + d["mhead"])
            ex = dict(ex, cart=cs, P=P, F=jnp.stack([F[0], F[2]]), haveP=jnp.ones((), bool), vmax=d["vmax"].astype(F64),
                      imp=ex["imp"] + jnp.stack([F[0], F[2]]) * dt, probeOk=jnp.ones((), bool))
        st = dict(steps=st["steps"] + 1, its=st["its"] + d["it"], itmax=jnp.maximum(st["itmax"], d["it"]),
                  resmax=jnp.maximum(st["resmax"], d["res"].astype(F64)), nselmax=jnp.maximum(st["nselmax"], d["nsel"]))
        return s, t + dt, ex, st

    def advance(s, t, ex):
        st = dict(steps=jnp.zeros((), I32), its=jnp.zeros((), I32), itmax=jnp.zeros((), I32), resmax=jnp.zeros((), F64), nselmax=jnp.zeros((), I32))
        s, t, ex, st = lax.while_loop(lambda c: c[1] < c[2]["t_end"] - 1e-9, body, (s, t, ex, st))
        return S.resort(s), t, ex, st

    return jax.jit(advance)


def ride_extra(S, cart_obj, x0=0.5):
    ml = S.rho * S.V + (S.rho_f * HEAD0 * float(np.sum(np.asarray(S.afill))) * S.dx ** 2 if S.head else 0.0)
    # the stout starts at rest in the glass, so its momentum relative to the glass is exactly zero: the push of the very first
    # step counts too (13 Nov 2026; before, the first step's push was skipped, 4 % of the impulse in a two-frame check)
    return dict(cart=cart_obj.init(x0, ml), P=jnp.zeros(3, F64), F=jnp.zeros(2, F64), haveP=jnp.ones((), bool),
                vmax=jnp.zeros((), F64), imp=jnp.zeros(2, F64), t_end=jnp.zeros((), F64), probeOk=jnp.zeros((), bool))
