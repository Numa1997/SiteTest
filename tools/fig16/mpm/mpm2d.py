"""Fig. 16 one-model spill, version A: a 2-D planar MLS-MPM solver for the pint of stout with its head (JAX, float32, explicit).

Written 20 Nov 2026 on branch claude/guinness-one-model; plan and parameters in notes/spill/STATE-one-model.md.
Runs on Kaggle only. Nothing here is run in the editing container.

The slice is the vertical plane through the glass's axis (x across, z up, depth 1 m per unit; masses are per metre of depth).
One material law for every particle, set by its gas fraction phi (fixed during the ride):
    rest density        rho0 = (1 - phi) rho_l
    pressure            p = K (J^-7 - 1),  K = rho0 c^2 / 7,  cut at p >= 0 (no surface tension in version 1: the liquid cannot pull)
    shear stress        tau = 2 eta(gdot) dev(D),  D = sym(C),  dev taken in 3-D (plane strain: D_yy = 0)
    eta                 phi < PHI_JAM: Newtonian, eta = rho0 nu
                        phi >= PHI_JAM (the head): Herschel-Bulkley, Papanastasiou-regularised,
                        eta = K_hb gdot^(n_hb - 1) + sigma_y (1 - exp(-m_pap gdot)) / gdot,  capped at eta_cap (explicit step limit)
Transfers: MLS-MPM with APIC (Hu et al. 2018, "A moving least squares material point method"), quadratic B-splines.
Thin wall: compatible PIC (CPIC, Hu et al. 2018, "A moving least squares ..." sec. 5) by two velocity slots per grid node, one for each
side of the glass wall. Below the rim a particle writes to and reads from the slot of its own side only, so particles on opposite
sides of the 2.5 mm wall never share a grid velocity; above the rim (z >= zrim) both slots are merged into one velocity.
Each slot sees its own solid: slot 0 (inside) sees everything outside the glass's cavity below the rim as solid; slot 1 (outside)
sees the glass and its cavity as solid. The deck is solid for both.
Wall condition on the grid (each slot): separating (liquid may leave a wall, never enter it): v.n < 0 is removed where phi_s < 0;
Navier slip by the implicit wall friction  v_t <- v_t / (1 + dt eta A / (m (l_s + d)))  at nodes within half a cell of a wall
(A = dx per metre of depth, d = max(phi_s, 0)); l_s = 0 is no-slip, l_s = inf is free slip.
Frame: the glass is fixed in this frame; the frame's acceleration enters as a body force b(t) (gravity included).
"""
import json, math, time
import numpy as np
import jax, jax.numpy as jnp
from jax import lax

F32 = jnp.float32
PHI_JAM = 0.64          # gas fraction at which the liquid is treated as a jammed foam (owner's rule: Newtonian for phi < 0.64)


# ====================================================================== parameters (every one named; values and sources in the state file)
def default_params():
    return dict(
        rho_l=1007.0,            # kg/m^3, the liquid (tools/fig16/kaggle/run16.py:22)
        phi_body=0.03,           # gas fraction of the stout's body (owner, assumed)
        phi_head=0.73,           # gas fraction of the head (stout_jax.py: PHI_F = 0.27)
        nu=2.06e-3 / 1007.0,     # m^2/s, the stout (Benilov, Cummins & Lee, arXiv 1205.5233; stout_jax.py:33)
        sigma_y=10.0,            # Pa, the head's yield stress (owner's start; sweep 0-50)
        K_hb=5.0,                # Pa s^n, Herschel-Bulkley consistency: Yue et al. 2015 Table I "pie" (assumed, see state file)
        n_hb=0.27,               # Herschel-Bulkley index, same source (assumed)
        m_pap=0.2,               # s, Papanastasiou regularisation time (assumed)
        c=50.0,                  # m/s, sound speed of the stiff equation of state (owner's start)
        ls_stout=0.0,            # m, Navier slip length of the stout (no-slip)
        ls_head=math.inf,        # m, Navier slip length of the head (free slip)
        gamma=0.0,               # N/m, surface tension: not in version 1 (stage E)
        air_drag=False,          # switch, off (not in version 1)
        dx=0.0015,               # m, grid spacing
        ppc=2,                   # particles per cell along each axis
        dt=1.0e-3 / 84,          # s, 1.19e-5 s: c dt / dx = 0.40, and 84 steps make 1 ms
        cfl_visc=0.5,            # eta_cap = cfl_visc rho0 dx^2 / (4 dt)
        g=9.81,                  # m/s^2
        stout_top=0.125,         # m, the stout's level above the cavity floor (run16.py:22)
        head_h=0.019,            # m, the head as served (stout_jax.py:50)
        deck_z=-0.030,           # m, the deck's top face below the cavity floor (owner's brief)
        deck_half=0.155,         # m, half the deck's length along the ride (310 mm)
        deck_thick=0.012,        # m, the deck slab (assumed; only its top face matters)
        wall=0.0025,             # m, glass wall (stout_jax.py:100)
        x_half=0.185, z_lo=-0.080, z_hi=0.170,   # m, the grid's extent
        cpic=True,               # side-tagged transfers on (False: one slot, the negative control)
    )


# ====================================================================== the glass and the deck
class Glass2D:
    """The glass's section in the plane of its axis, from tools/fig12/glass_profile.json (the Irish Imperial pint, inner radius R(z))."""

    def __init__(self, profile_path, P):
        d = json.load(open(profile_path))
        self.R = np.asarray(d["R"], float); self.dz = float(d["dz"]); self.zrim = (len(self.R) - 1) * self.dz
        self.zp = np.arange(len(self.R)) * self.dz; self.P = P

    def Rin(self, z):        # inner radius at height z (clamped to the glass)
        return np.interp(np.clip(z, 0.0, self.zrim), self.zp, self.R)

    def Rout(self, z):       # outer radius: the wall is 2.5 mm thick, and below 8 mm the base keeps the 8 mm radius (stout_jax.py:174)
        return np.interp(np.clip(np.maximum(z, 0.008), 0.0, self.zrim), self.zp, self.R) + self.P["wall"]

    def Rmid(self, z):
        return 0.5 * (self.Rin(z) + self.Rout(z))

    def polygons(self):
        """Closed polygons (counter-clockwise lists of (x, z)) of: the glass solid, the inner-slot solid, the outer-slot solid."""
        P = self.P; zs = self.zp; zt = P["deck_z"]
        ro = self.Rout(zs); ri = self.Rin(zs); rf = float(self.Rout(0.0))
        # the glass: foot from the deck up to z = 0, wall from 0 to the rim; the cavity is a notch from the top
        right_out = [(r, z) for r, z in zip(ro, zs)]
        right_in = [(r, z) for r, z in zip(ri[::-1], zs[::-1])]
        glass = [(-rf, zt), (rf, zt), (rf, 0.0)] + right_out + right_in + [(-r, z) for r, z in zip(ri, zs)] + \
                [(-r, z) for r, z in zip(ro[::-1], zs[::-1])] + [(-rf, 0.0)]
        X = P["x_half"] + 0.01; Zb = P["z_lo"] - 0.01
        # inner slot: below the rim, everything outside the cavity is solid
        inner = [(-X, Zb), (X, Zb), (X, self.zrim), (ri[-1], self.zrim)] + right_in[1:] + [(-r, z) for r, z in zip(ri, zs)][:-1] + \
                [(-ri[-1], self.zrim), (-X, self.zrim)]
        # outer slot: the glass and its cavity are solid (the glass's outline closed across the rim)
        outer = [(-rf, zt), (rf, zt), (rf, 0.0)] + right_out + [(-r, z) for r, z in zip(ro[::-1], zs[::-1])] + [(-rf, 0.0)]
        return [np.asarray(p) for p in (glass, inner, outer)]


def poly_sdf(poly, X, Z, chunk=4096):
    """Signed distance from points (X, Z) to a closed polygon: negative inside. Exact (point-to-segment, even-odd inside test)."""
    a = poly; b = np.roll(poly, -1, axis=0); ab = b - a; L2 = np.maximum((ab ** 2).sum(1), 1e-30)
    pts = np.stack([X.ravel(), Z.ravel()], 1); out = np.empty(len(pts))
    for s in range(0, len(pts), chunk):
        p = pts[s:s + chunk, None, :]
        t = np.clip(((p - a[None]) * ab[None]).sum(2) / L2[None], 0.0, 1.0)
        q = a[None] + t[..., None] * ab[None]; dist = np.sqrt(((p - q) ** 2).sum(2)).min(1)
        py = p[:, 0, 1][:, None]; px = p[:, 0, 0][:, None]
        cond = (a[None, :, 1] > py) != (b[None, :, 1] > py)
        xint = a[None, :, 0] + (py - a[None, :, 1]) * ab[None, :, 0] / np.where(ab[None, :, 1] == 0, 1e-30, ab[None, :, 1])
        inside = (np.sum(cond & (px < xint), 1) % 2) == 1
        out[s:s + chunk] = np.where(inside, -dist, dist)
    return out.reshape(X.shape)


def box_sdf(X, Z, xh, z0, z1):
    """Signed distance to the box |x| < xh, z0 < z < z1."""
    qx = np.abs(X) - xh; qz = np.maximum(z0 - Z, Z - z1)
    o = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qz, 0) ** 2); i = np.minimum(np.maximum(qx, qz), 0.0)
    return o + i


class Grid2D:
    """Node fields built once: the signed distance and unit normal of each slot's solid, the true solid, the node's side, masks."""

    def __init__(self, G, P):
        dx = P["dx"]; self.dx = dx
        self.x0 = -P["x_half"]; self.z0 = P["z_lo"]
        self.nx = int(math.ceil(2 * P["x_half"] / dx)) + 1; self.nz = int(math.ceil((P["z_hi"] - P["z_lo"]) / dx)) + 1
        xn = self.x0 + dx * np.arange(self.nx); zn = self.z0 + dx * np.arange(self.nz)
        X, Z = np.meshgrid(xn, zn, indexing="ij"); self.X, self.Z = X, Z
        glass, inner, outer = G.polygons()
        deck = box_sdf(X, Z, P["deck_half"], P["deck_z"] - P["deck_thick"], P["deck_z"])
        true = np.minimum(poly_sdf(glass, X, Z), deck)
        s_in = np.minimum(poly_sdf(inner, X, Z), deck); s_out = np.minimum(poly_sdf(outer, X, Z), deck)
        if P["cpic"]:
            sd = np.stack([s_in, s_out])
        else:
            sd = np.stack([true, true])
        nrm = np.zeros(sd.shape + (2,))
        for s in range(2):
            gx, gz = np.gradient(sd[s], dx, dx); gn = np.sqrt(gx ** 2 + gz ** 2) + 1e-12
            nrm[s, ..., 0] = gx / gn; nrm[s, ..., 1] = gz / gn
        side = np.where(np.abs(X) < G.Rmid(Z), 0, 1).astype(np.int32)       # which side of the wall's mid-surface a node lies on
        above = (Z >= G.zrim)                                                  # nodes above the rim: one merged velocity
        edge = np.zeros_like(X, bool); edge[:2] = edge[-2:] = True; edge[:, :2] = edge[:, -2:] = True
        self.np_true = true
        self.sdf = jnp.asarray(sd, F32); self.nrm = jnp.asarray(nrm, F32); self.true = jnp.asarray(true, F32)
        self.side = jnp.asarray(side); self.above = jnp.asarray(above); self.edge = jnp.asarray(edge)


# ====================================================================== particles
def tag_of(G, x, z):
    """A particle's side by its position: 0 inside the cavity's column, 1 outside it, 2 at or above the rim (free)."""
    zc = jnp.clip(z, 0.0, G.zrim)
    rin = jnp.interp(zc, jnp.asarray(G.zp, F32), jnp.asarray(G.R, F32))
    rout = jnp.interp(jnp.clip(jnp.maximum(z, 0.008), 0.0, G.zrim), jnp.asarray(G.zp, F32), jnp.asarray(G.R, F32)) + G.P["wall"]
    rmid = 0.5 * (rin + rout)
    return jnp.where(z >= G.zrim, 2, jnp.where(jnp.abs(x) < rmid, 0, 1)).astype(jnp.int32), rout


def seed(G, P, outer_band=None):
    """Particles ppc x ppc per cell. Inside the cavity: stout to stout_top, head above it to stout_top + head_h.
    outer_band = (width, top): also stout outside the wall, from the outer wall out to width, from the deck up to top (the control).
    Each particle starts at the hydrostatic pressure of its depth, so the column starts in balance: J0 = (1 + p_h / K)^(-1/7)."""
    dx = P["dx"]; h = dx / P["ppc"]
    xs = np.arange(-P["x_half"] + h / 2, P["x_half"], h); zs = np.arange(P["deck_z"] + h / 2, P["stout_top"] + P["head_h"], h)
    X, Z = np.meshgrid(xs, zs, indexing="ij"); X = X.ravel(); Z = Z.ravel()
    top = P["stout_top"] + P["head_h"]
    cav = (Z > 0) & (Z < top) & (np.abs(X) < G.Rin(Z))
    phi = np.where(Z < P["stout_top"], P["phi_body"], P["phi_head"])
    keep = cav.copy()
    if outer_band is not None:
        w, zt_ = outer_band
        band = (Z > P["deck_z"]) & (Z < zt_) & (np.abs(X) > G.Rout(Z)) & (np.abs(X) < G.Rout(Z) + w) & (Z < G.zrim)
        band &= ~((Z <= 0) & (np.abs(X) < float(G.Rout(0.0))))
        keep |= band; phi = np.where(band, P["phi_body"], phi)
    X, Z, phi = X[keep], Z[keep], phi[keep]
    rho0 = (1 - phi) * P["rho_l"]; K = rho0 * P["c"] ** 2 / 7.0
    # hydrostatic pressure: inside, the head over the stout; outside, the stout band's own column
    rho_h = (1 - P["phi_head"]) * P["rho_l"]; rho_s = (1 - P["phi_body"]) * P["rho_l"]
    inside = np.abs(X) < G.Rin(np.clip(Z, 0, G.zrim))
    p_in = np.where(Z >= P["stout_top"], rho_h * P["g"] * (top - Z), rho_h * P["g"] * P["head_h"] + rho_s * P["g"] * (P["stout_top"] - Z))
    p_out = rho_s * P["g"] * ((outer_band[1] if outer_band else 0.0) - Z)
    ph = np.maximum(np.where(inside, p_in, p_out), 0.0)
    J0 = (1.0 + ph / K) ** (-1.0 / 7.0)
    V0 = h * h / J0                      # reference volume (J = 1): the particle fills h^2 at its compressed start
    m = rho0 * V0
    return dict(x=np.stack([X, Z], 1), v=np.zeros((len(X), 2)), C=np.zeros((len(X), 2, 2)), J=J0, m=m, V0=V0, phi=phi, rho0=rho0)


# ====================================================================== one step
def make_step(G, Gr, P):
    dx = P["dx"]; inv_dx = 1.0 / dx; dt = P["dt"]; nx, nz = Gr.nx, Gr.nz
    c2 = P["c"] ** 2; cpic = P["cpic"]
    x0 = jnp.array([Gr.x0, Gr.z0], F32)
    if P["gamma"] != 0.0 or P["air_drag"]:
        raise NotImplementedError("surface tension and air drag are stage E / a later switch; version 1 runs with both off")

    def eta_of(Cm, rho0, head):
        D = 0.5 * (Cm + jnp.swapaxes(Cm, 1, 2))
        tr = D[:, 0, 0] + D[:, 1, 1]
        dev = D - (tr / 3.0)[:, None, None] * jnp.eye(2, dtype=F32)
        dyy = -tr / 3.0                                                     # the out-of-plane deviatoric component (plane strain)
        gd = jnp.sqrt(2.0 * (jnp.sum(dev * dev, (1, 2)) + dyy * dyy))
        gds = jnp.maximum(gd, 1e-8)
        eta_n = rho0 * P["nu"]
        eta_h = P["K_hb"] * gds ** (P["n_hb"] - 1.0) + P["sigma_y"] * (1.0 - jnp.exp(-P["m_pap"] * gds)) / gds
        cap = P["cfl_visc"] * rho0 * dx * dx / (4.0 * dt)
        eta = jnp.where(head, jnp.minimum(eta_h, cap), eta_n)
        capped = head & (eta_h > cap)
        return eta, dev, capped

    def step(state, body):
        x, v, C, J = state["x"], state["v"], state["C"], state["J"]
        m, V0, rho0, phi = state["m"], state["V0"], state["rho0"], state["phi"]
        head = phi >= PHI_JAM
        tag, _ = tag_of(G, x[:, 0], x[:, 1])
        # stress (Cauchy) times current volume, folded into the APIC affine matrix
        K = rho0 * c2 / 7.0
        p = jnp.maximum(K * (J ** -7.0 - 1.0), 0.0)
        eta, dev, capped = eta_of(C, rho0, head)
        sig = -p[:, None, None] * jnp.eye(2, dtype=F32) + 2.0 * eta[:, None, None] * dev
        Vp = V0 * J
        affine = -dt * 4.0 * inv_dx * inv_dx * Vp[:, None, None] * sig + m[:, None, None] * C
        # quadratic B-spline weights
        xg = (x - x0) * inv_dx
        base = jnp.floor(xg - 0.5).astype(jnp.int32)
        base = jnp.clip(base, 0, jnp.array([nx - 3, nz - 3]))
        fx = xg - base
        w = jnp.stack([0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2], 1)   # (N, 3, 2)
        offs = jnp.array([(i, j) for i in range(3) for j in range(3)], jnp.int32)                   # (9, 2)
        idx = base[:, None, :] + offs[None]                                                          # (N, 9, 2)
        wij = w[:, offs[:, 0], 0] * w[:, offs[:, 1], 1]                                              # (N, 9)
        dpos = (offs[None].astype(F32) - fx[:, None, :]) * dx                                        # (N, 9, 2)
        nside = Gr.side[idx[..., 0], idx[..., 1]]
        if cpic:
            slot = jnp.where(tag[:, None] == 2, nside, tag[:, None])
        else:
            slot = jnp.zeros_like(nside)
        mom = wij[..., None] * (m[:, None, None] * v[:, None, :] + jnp.einsum("nab,nkb->nka", affine, dpos))
        ms = wij * m[:, None]
        ehead = jnp.where(head, eta, 0.0); estout = jnp.where(head, 0.0, eta)
        chans = jnp.concatenate([ms[..., None], mom, (ms * estout[:, None])[..., None], (ms * ehead[:, None])[..., None]], -1)  # (N,9,5)
        grid = jnp.zeros((2, nx, nz, 5), F32).at[slot, idx[..., 0], idx[..., 1]].add(chans)
        # above the rim the two slots are one velocity
        merged = grid[0] + grid[1]
        grid = jnp.where(Gr.above[None, ..., None], merged[None], grid)
        gm = grid[..., 0]; has = gm > 0
        gv = jnp.where(has[..., None], grid[..., 1:3] / jnp.where(has, gm, 1.0)[..., None], 0.0) + dt * body[None, None, None, :]
        # walls: separating condition, then implicit Navier-slip friction
        sd = Gr.sdf; n = Gr.nrm
        vn = jnp.sum(gv * n, -1)
        gv = jnp.where(((sd < 0) & (vn < 0))[..., None], gv - vn[..., None] * n, gv)
        vn = jnp.sum(gv * n, -1); vt = gv - vn[..., None] * n
        d = jnp.maximum(sd, 0.0)
        mm = jnp.where(has, gm, 1.0)
        # (a phase absent from a node adds nothing, also where l_s + d = 0: no 0/0)
        fs = jnp.where(grid[..., 3] > 0, grid[..., 3] / (P["ls_stout"] + d), 0.0)
        fh = jnp.where(grid[..., 4] > 0, grid[..., 4] / (P["ls_head"] + d), 0.0)
        coef = dt * dx * (fs + fh) / (mm * mm)
        near = (sd < 0.5 * dx) & has
        vt = jnp.where(near[..., None], vt / (1.0 + coef)[..., None], vt)
        gv = vn[..., None] * n + vt
        # the grid's own edge: nothing leaves the box
        gv = jnp.where(Gr.edge[None, ..., None], 0.0, gv)
        # grid to particles
        gvp = gv[slot, idx[..., 0], idx[..., 1]]                                                     # (N, 9, 2)
        v_new = jnp.sum(wij[..., None] * gvp, 1)
        C_new = 4.0 * inv_dx * inv_dx * jnp.einsum("nk,nka,nkb->nab", wij, gvp, dpos)
        J_new = J * (1.0 + dt * (C_new[:, 0, 0] + C_new[:, 1, 1]))
        x_new = x + dt * v_new
        tag_new, _ = tag_of(G, x_new[:, 0], x_new[:, 1])
        crossed = (tag < 2) & (tag_new < 2) & (tag != tag_new)
        out = dict(state, x=x_new, v=v_new, C=C_new, J=J_new)
        return out, crossed, capped

    return step


def make_chunk(step, nsteps, body_fn):
    """nsteps steps in one compiled loop; returns the state, the crossings in the chunk (per particle, OR), and the capped count."""
    def chunk(state, t0):
        def body(k, carry):
            st, cr, cp = carry
            t = t0 + k * st["dt"]
            st2, crossed, capped = step(st, body_fn(t))
            return st2, cr | crossed, jnp.maximum(cp, jnp.sum(capped))
        N = state["x"].shape[0]
        return lax.fori_loop(0, nsteps, body, (state, jnp.zeros(N, bool), jnp.int32(0)))
    return jax.jit(chunk)


def to_state(p, P):
    s = {k: jnp.asarray(v, F32) for k, v in p.items()}
    s["dt"] = jnp.asarray(P["dt"], F32)
    return s


def diagnostics(G, Gr, P, st, tag0):
    """Read-only numbers of one instant (no effect on the run)."""
    x = st["x"]; J = st["J"]; head = st["phi"] >= PHI_JAM
    tag, rout = tag_of(G, x[:, 0], x[:, 1])
    below = (x[:, 1] < G.zrim) & (x[:, 1] > 0)
    outside_from_in = jnp.sum((tag0 == 0) & below & (jnp.abs(x[:, 0]) > rout))
    inside_from_out = jnp.sum((tag0 == 1) & below & (jnp.abs(x[:, 0]) < jnp.interp(x[:, 1], jnp.asarray(G.zp, F32), jnp.asarray(G.R, F32))))
    # depth into the true solid, by bilinear interpolation of the node field
    xg = (x - jnp.array([Gr.x0, Gr.z0], F32)) / Gr.dx
    i = jnp.clip(jnp.floor(xg).astype(jnp.int32), 0, jnp.array([Gr.nx - 2, Gr.nz - 2])); f = xg - i
    T = Gr.true
    phi_p = (T[i[:, 0], i[:, 1]] * (1 - f[:, 0]) * (1 - f[:, 1]) + T[i[:, 0] + 1, i[:, 1]] * f[:, 0] * (1 - f[:, 1]) +
             T[i[:, 0], i[:, 1] + 1] * (1 - f[:, 0]) * f[:, 1] + T[i[:, 0] + 1, i[:, 1] + 1] * f[:, 0] * f[:, 1])
    # isolated particles: no other particle in its cell or the 8 around it
    ci = jnp.clip(jnp.floor(xg).astype(jnp.int32), 1, jnp.array([Gr.nx - 2, Gr.nz - 2]))
    cnt = jnp.zeros((Gr.nx, Gr.nz), jnp.int32).at[ci[:, 0], ci[:, 1]].add(1)
    nb = sum(cnt[ci[:, 0] + a, ci[:, 1] + b] for a in (-1, 0, 1) for b in (-1, 0, 1))
    vmax = jnp.max(jnp.sqrt(jnp.sum(st["v"] ** 2, 1)))
    centre = jnp.abs(x[:, 0]) < 0.010
    return dict(outside_from_inside=int(outside_from_in), inside_from_outside=int(inside_from_out),
                min_sdf_mm=float(jnp.min(phi_p)) * 1e3, n_in_solid=int(jnp.sum(phi_p < 0)),
                J_err_stout=float(jnp.max(jnp.where(head, 0.0, jnp.abs(J - 1)))), J_err_head=float(jnp.max(jnp.where(head, jnp.abs(J - 1), 0.0))),
                J_mean_stout=float(jnp.sum(jnp.where(head, 0, J)) / jnp.maximum(jnp.sum(~head), 1)),
                isolated=int(jnp.sum(nb == 1)), vmax=float(vmax),
                z_top_centre_mm=float(jnp.max(jnp.where(centre, x[:, 1], -1.0))) * 1e3,
                N=int(x.shape[0]), mass=float(jnp.sum(st["m"])))
