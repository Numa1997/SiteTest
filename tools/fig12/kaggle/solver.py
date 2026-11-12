# Guinness on a one-wheel cart: the stout computed on the GPU (Taichi), coupled both ways to the cart. Solver v2 (13 Nov 2026).
# Fluid: incompressible Navier-Stokes equations with a free surface, APIC particles on a staggered grid, pressure by
# conjugate gradients with cut-cell face fractions for the curved glass (Batty, Bertails & Bridson 2007). Computed in the
# glass's frame: every particle feels gravity minus the glass's acceleration.
# v2 against v1 (the rides of 12 Nov 2026):
#  - free surface: a level set from the particles (Zhu & Bridson 2005, kernel 2 dx, radius 0.9 dx), carried into the cells
#    cut by the glass from their neighbours, and ghost-fluid pressure p = 0 on the surface itself (Enright, Nguyen, Gibou &
#    Fedkiw 2003), as the website's solver stout-cart.js does; v1 put p = 0 at the centre of the first air cell and filled
#    wall cells by a rule;
#  - the glass: faces closed by the glass are extrapolated from the liquid (free slip on the grid); v1 held them at zero,
#    which brakes the particles along the wall like a no-slip wall one cell thick;
#  - viscosity nu = 1.0e-6 m^2/s on the grid, explicit (the Fig. 12 note's value);
#  - the wall's boundary layer, 0.4 mm thick, far below the grid: the Stokes-layer stress tau = rho sqrt(nu omega / 2) u_slip
#    on the liquid next to the glass (the oscillating Stokes layer at the swing's frequency, omega = 2 pi 3.42 Hz);
#  - the head of foam: the Plateau borders of the bubbles rub on the glass (Sauret, Boulogne, Cappello, Dressaire & Stone,
#    Phys. Fluids 27, 022103, 2015): a force per length of contact line F = Lambda(v) v, Lambda = Lambda0 (|v| / 0.1 m/s)^(-1/3),
#    Lambda0 = C rho / (2 k_S) from their measured damping of a confined foam (w / tau = C = 1.6-3.1 cm/s, k_S = 45.5 /m),
#    on the liquid within 2 dx of the surface next to the glass. The cart: a line-by-line port of Cart in
# public/scripts/stout-cart.js (via tools/fig12/of/cart/cart.H); the stout pushes back on it with F = -dP/dt.
import math, time, json
import numpy as np
import taichi as ti

# ------------------------------------------------------------------ the cart (CPU, double precision)
CART_COMMON = dict(Mb=1.5, mw=0.3, Rw=0.04, Iw=0.00024, k=600.0, c=8.0, kt=20000.0, ct=5.0, cx=2.0, Crr=0.0, Tf=0.0,
                   bf=0.0, CdA=0.0, rhoAir=1.2, vSmooth=0.001, Ls=0.135, g=9.81, Ngear=10.0, Km=0.02, Ra=2.0, Jm=2e-6,
                   Vmax=12.0, Imax=3.0, tauI=0.002, Ts=0.001, Kp=25.178818315223719, Ki=316.40636258071589,
                   csky=47.636016270456992, Umax=40.0, tauU=0.005, mu=0.8)   # write_cart.cjs output for fill 125 mm, rho 1007


def road_table(road, Rw=0.04, xmin=-1.0, xmax=14.0, h=0.0005):
    """Road.build of stout-cart.js: the axle height z_a(x) of a rigid wheel rolling over the profile, every h."""
    n = int(round((xmax - xmin) / h)) + 1
    x = xmin + h * np.arange(n)
    kind = road.get("kind", "bumps")
    if kind == "bumps":
        zr = np.zeros(n)
        for b in road["bumps"]:
            s = (x - b["x"]) / b["L"]
            m = (s > -0.5) & (s < 0.5)
            zr[m] += 0.5 * b["h"] * (1 + np.cos(2 * np.pi * s[m]))
    elif kind == "drawn":   # straight segments between points (kerb), level beyond the ends
        P = np.array(road["points"], float)
        zr = np.interp(x, P[:, 0], P[:, 1])
    elif kind == "washboard":
        lam, H = 0.30, 0.020
        zr = 0.5 * H * (1 - np.cos(2 * np.pi * x / lam))
        zr = (zr - np.interp(1.0, x, zr)) * np.clip(np.where(x <= 0.5, 0, np.where(x >= 1, 1, 0.5 * (1 - np.cos(np.pi * (x - 0.5) / 0.5)))), 0, 1)
    else:
        raise ValueError(kind)
    m = int(math.ceil(Rw / h))
    za = np.full(n, -1e9)
    for d in range(-m, m + 1):
        s = d * h
        if abs(s) > Rw: continue
        sh = np.full(n, -1e9)
        if d >= 0: sh[:n - d] = zr[d:]
        else: sh[-d:] = zr[:n + d]
        za = np.maximum(za, sh + math.sqrt(Rw * Rw - s * s))
    return xmin, h, za, zr


class Cart:
    def __init__(self, params, road, x0=0.5):
        for k, v in params.items(): setattr(self, k, float(v))
        self.ctrl = int(params.get("ctrl", 1)); self.susp = int(params.get("susp", 0))
        self.xmin, self.h, self.za = road[:3]
        self.reset(x0)

    def axle(self, x):
        f = (x - self.xmin) / self.h; j = int(math.floor(f)); j = min(max(j, 0), len(self.za) - 2)
        t = f - j; A, B = self.za[j], self.za[j + 1]
        return A + t * (B - A), (B - A) / self.h

    def bForce(self): return self.Ngear * self.Km / self.Rw

    def resist(self, v, N):
        sg = v / math.sqrt(v * v + self.vSmooth ** 2)
        return self.cx * v + self.Crr * N * sg + self.Tf / self.Rw * sg + self.bf * v / self.Rw ** 2 + 0.5 * self.rhoAir * self.CdA * v * abs(v)

    def resistAtSetSpeed(self): return self.resist(self.v0, (self.Mb + self.ml + self.mw) * self.g)
    def massX(self): return self.Mb + self.ml + self.mw + (self.Iw + self.Ngear ** 2 * self.Jm) / self.Rw ** 2

    def reset(self, x0):
        Ms = self.Mb + self.ml; a, d = self.axle(x0)
        self.x = x0; self.vx = self.v0
        self.zw = a - (Ms + self.mw) * self.g / self.kt
        self.zb = self.zw + self.Ls - Ms * self.g / self.k
        self.vzb = self.vzw = self.t = 0.0
        self.i = self.resistAtSetSpeed() / self.bForce(); self.icmd = self.i; self.xi = 0.0; self.us = self.uscmd = 0.0; self.tSample = 0.0
        self.forces(0.0, 0.0)

    def sample(self):
        i0 = self.resistAtSetSpeed() / self.bForce(); e = self.v0 - self.vx
        if self.ctrl in (1, 2):
            ic = i0 + self.Kp * e + self.Ki * self.xi
            if self.ctrl == 2:
                a, d = self.axle(self.x + self.vx * self.tauI); ic += (self.Mb + self.ml + self.mw) * self.g * d / self.bForce()
            if abs(ic) < self.Imax: self.xi += e * self.Ts
            self.icmd = ic
        else:
            self.icmd = i0
        u = -self.csky * self.vzb if self.susp else 0.0
        self.uscmd = min(max(u, -self.Umax), self.Umax)

    def forces(self, Fx, Fz):
        Ms = self.Mb + self.ml; a, d = self.axle(self.x)
        N = self.kt * (a - self.zw) + self.ct * (d * self.vx - self.vzw); N = max(N, 0.0)
        FS = -self.k * (self.zb - self.zw - self.Ls) - self.c * (self.vzb - self.vzw) + self.us
        Fm0 = self.bForce() * self.i; Fg = self.mu * N; Fm = min(max(Fm0, -Fg), Fg); Fr = -N * d
        FR = self.resist(self.vx, N)
        self.ax = (Fr + Fm - FR + Fx) / self.massX()
        self.azb = (FS - Ms * self.g + Fz) / Ms
        self.azw = (-FS - self.mw * self.g + N) / self.mw
        E = self.Km * self.Ngear * self.vx / self.Rw
        il = min(max(self.icmd, -self.Imax), self.Imax)
        il = min(max(il, (-self.Vmax - E) / self.Ra), (self.Vmax - E) / self.Ra)
        self.ireach = il; self.N = N

    def step(self, hh, Fx, Fz):
        self.tSample += hh
        if self.tSample >= self.Ts - 1e-12:
            self.tSample -= self.Ts; self.sample(); self.forces(Fx, Fz)
        self.vx += hh * self.ax; self.vzb += hh * self.azb; self.vzw += hh * self.azw
        self.x += hh * self.vx; self.zb += hh * self.vzb; self.zw += hh * self.vzw
        self.i = self.ireach + (self.i - self.ireach) * math.exp(-hh / self.tauI)
        self.us = self.uscmd + (self.us - self.uscmd) * math.exp(-hh / self.tauU)
        self.t += hh
        self.forces(Fx, Fz)


# ------------------------------------------------------------------ the stout (GPU)
def glass_volume(R, dzp, fill, n=20000):
    z = np.linspace(0, fill, n + 1); r = np.interp(z / dzp, np.arange(len(R)), R)
    return np.trapezoid(np.pi * r * r, z) if hasattr(np, "trapezoid") else np.trapz(np.pi * r * r, z)


MODELS = {
    # v1: the solver of the rides of 12 Nov 2026 (for comparison only)
    "v1": dict(ghost=False, fill=True, closed="zero", nu=0.0, wall=False, foam=False, omega=2 * math.pi * 3.42, foamC=0.0235),
    # v2 without any friction: what the numbers alone lose
    "inviscid": dict(ghost=True, fill=False, closed="extrap", nu=0.0, wall=False, foam=False, omega=2 * math.pi * 3.42, foamC=0.0235),
    # v2 with the stout's viscosity and the glass's boundary layer
    "wall": dict(ghost=True, fill=False, closed="extrap", nu=1.0e-6, wall=True, foam=False, omega=2 * math.pi * 3.42, foamC=0.0235),
    # v2 with the head of foam too (the rides)
    "full": dict(ghost=True, fill=False, closed="extrap", nu=1.0e-6, wall=True, foam=True, omega=2 * math.pi * 3.42, foamC=0.0235),
}


@ti.data_oriented
class Stout:
    def __init__(self, R, dzp, fill, rho, dx, ppc=2, arch=None, seed=1, model=None):
        R = np.asarray(R, float); self.R = R; self.ppc = ppc; self.dzp = dzp; self.fill = fill; self.rho = rho; self.dx = dx
        M = dict(MODELS["full"]); M.update(model or {}); self.model = M
        self.ghost = 1 if M["ghost"] else 0; self.fillrule = 1 if M["fill"] else 0; self.closed_zero = 1 if M["closed"] == "zero" else 0
        self.nu = float(M["nu"]); self.gs = float(math.sqrt(M["nu"] * M["omega"] / 2)) if M["wall"] else 0.0   # m/s
        self.lam0 = float(M["foamC"] * rho / (2 * 45.5)) if M["foam"] else 0.0                                 # kg/(m s)
        self.Hb = 2.0 * dx; self.rls = 0.9 * dx
        self.zrim = (len(R) - 1) * dzp; Rmax = R.max()
        self.n = int(math.ceil(2 * (Rmax + 2 * dx) / dx)); self.nz = int(math.ceil((self.zrim + 0.02) / dx)) + 2
        self.x0 = -self.n * dx / 2; self.z0 = -2 * dx          # grid origin: two cells of glass below the floor
        nx, ny, nz = self.n, self.n, self.nz
        # glass profile on the device
        self.Rf = ti.field(ti.f32, len(R)); self.Rf.from_numpy(R.astype(np.float32))
        self.nR = len(R)
        # staggered grid: u on x-faces, v on y-faces, w on z-faces; open fractions th*; weights m*
        self.u = ti.field(ti.f32, (nx + 1, ny, nz)); self.v = ti.field(ti.f32, (nx, ny + 1, nz)); self.w = ti.field(ti.f32, (nx, ny, nz + 1))
        self.mu_ = ti.field(ti.f32, (nx + 1, ny, nz)); self.mv = ti.field(ti.f32, (nx, ny + 1, nz)); self.mw = ti.field(ti.f32, (nx, ny, nz + 1))
        self.thu = ti.field(ti.f32, (nx + 1, ny, nz)); self.thv = ti.field(ti.f32, (nx, ny + 1, nz)); self.thw = ti.field(ti.f32, (nx, ny, nz + 1))
        self.cnt = ti.field(ti.i32, (nx, ny, nz)); self.liq = ti.field(ti.i32, (nx, ny, nz))
        self.p = ti.field(ti.f32, (nx, ny, nz)); self.b = ti.field(ti.f32, (nx, ny, nz)); self.r = ti.field(ti.f32, (nx, ny, nz))
        self.d = ti.field(ti.f32, (nx, ny, nz)); self.q = ti.field(ti.f32, (nx, ny, nz)); self.zv = ti.field(ti.f32, (nx, ny, nz))
        self.diag = ti.field(ti.f32, (nx, ny, nz))
        self.ku = ti.field(ti.i32, (nx + 1, ny, nz)); self.kv = ti.field(ti.i32, (nx, ny + 1, nz)); self.kw = ti.field(ti.i32, (nx, ny, nz + 1))
        self.ku2 = ti.field(ti.i32, (nx + 1, ny, nz)); self.kv2 = ti.field(ti.i32, (nx, ny + 1, nz)); self.kw2 = ti.field(ti.i32, (nx, ny, nz + 1))
        self.tu = ti.field(ti.f32, (nx + 1, ny, nz)); self.tv = ti.field(ti.f32, (nx, ny + 1, nz)); self.tw = ti.field(ti.f32, (nx, ny, nz + 1))
        self.s1 = ti.field(ti.f32, ()); self.s2 = ti.field(ti.f32, ())
        # level set and its helpers (v2)
        self.phi = ti.field(ti.f32, (nx, ny, nz)); self.phi2 = ti.field(ti.f32, (nx, ny, nz)); self.liq2 = ti.field(ti.i32, (nx, ny, nz))
        self.mA = ti.field(ti.i32, (nx, ny, nz)); self.mB = ti.field(ti.i32, (nx, ny, nz)); self.near = ti.field(ti.i32, (nx, ny, nz))
        self.nearP = ti.field(ti.i32, (nx, ny, nz))
        self.Wk = ti.field(ti.f32, (nx, ny, nz)); self.Sk = ti.Vector.field(3, ti.f32, (nx, ny, nz))
        # wall area per cell volume (1/m) of the cells cut by the glass, and its mean on each face (v2 wall and foam friction)
        self.ac = ti.field(ti.f32, (nx, ny, nz))
        self.au = ti.field(ti.f32, (nx + 1, ny, nz)); self.av = ti.field(ti.f32, (nx, ny + 1, nz)); self.aw = ti.field(ti.f32, (nx, ny, nz + 1))
        self.ewall = ti.field(ti.f64, ()); self.efoam = ti.field(ti.f64, ()); self.evisc = ti.field(ti.f64, ())
        self.mom = ti.Vector.field(3, ti.f32, ()); self.nact = ti.field(ti.i32, ()); self.spilled = ti.field(ti.i32, ())
        # particles: seed ppc^3 per cell inside the glass below the fill
        rng = np.random.default_rng(seed); pts = []
        h = dx / ppc
        xs = self.x0 + h * (np.arange(int(nx * ppc)) + 0.5); zs = np.arange(h / 2, fill, h)
        X, Y = np.meshgrid(xs, xs, indexing="ij")
        for z in zs:
            Rz = np.interp(z / dzp, np.arange(len(R)), R)
            m = X * X + Y * Y < (Rz - 0.25 * h) ** 2
            P = np.stack([X[m], Y[m], np.full(m.sum(), z)], 1)
            pts.append(P)
        P = np.concatenate(pts) + rng.uniform(-0.3 * h, 0.3 * h, (sum(len(p) for p in pts), 3))
        P[:, 2] = np.clip(P[:, 2], 0.2 * h, fill - 0.2 * h)
        self.N = len(P); self.V = glass_volume(R, dzp, fill); self.mp = rho * self.V / self.N
        self.xp = ti.Vector.field(3, ti.f32, self.N); self.vp = ti.Vector.field(3, ti.f32, self.N)
        self.cpx = ti.Vector.field(3, ti.f32, self.N); self.cpy = ti.Vector.field(3, ti.f32, self.N); self.cpz = ti.Vector.field(3, ti.f32, self.N)
        self.act = ti.field(ti.i32, self.N)
        self.xp.from_numpy(P.astype(np.float32)); self.act.fill(1)
        self.ncells = nx * ny * nz
        self._fractions()
        self._wall_area()

    # ---- geometry
    @ti.func
    def Rz(self, z):
        f = ti.min(ti.max(z / self.dzp, 0.0), self.nR - 1.001)
        i = ti.cast(ti.floor(f), ti.i32)
        return self.Rf[i] + (f - i) * (self.Rf[i + 1] - self.Rf[i])

    @ti.func
    def inside(self, p):   # inside the glass's cavity (the open top above the rim counts as inside: the air above)
        r2 = p[0] * p[0] + p[1] * p[1]
        ok = 0
        if p[2] > 0.0:
            if p[2] >= self.zrim: ok = 1
            else:
                R = self.Rz(p[2]); ok = 1 if r2 < R * R else 0
        return ok

    @ti.kernel
    def _fractions_k(self):
        dx = self.dx
        for i, j, k in self.thu:   # x-face at x0 + i dx, centre (j+.5, k+.5)
            c = 0
            for a, b in ti.static(ti.ndrange(4, 4)):
                c += self.inside(ti.Vector([self.x0 + i * dx, self.x0 + (j + (a + 0.5) / 4) * dx, self.z0 + (k + (b + 0.5) / 4) * dx]))
            self.thu[i, j, k] = c / 16.0
        for i, j, k in self.thv:
            c = 0
            for a, b in ti.static(ti.ndrange(4, 4)):
                c += self.inside(ti.Vector([self.x0 + (i + (a + 0.5) / 4) * dx, self.x0 + j * dx, self.z0 + (k + (b + 0.5) / 4) * dx]))
            self.thv[i, j, k] = c / 16.0
        for i, j, k in self.thw:
            c = 0
            for a, b in ti.static(ti.ndrange(4, 4)):
                c += self.inside(ti.Vector([self.x0 + (i + (a + 0.5) / 4) * dx, self.x0 + (j + (b + 0.5) / 4) * dx, self.z0 + k * dx]))
            self.thw[i, j, k] = c / 16.0

    def _fractions(self):
        self._fractions_k()
        # the outer boundary of the box is closed except the top
        thu = self.thu.to_numpy(); thu[0] = thu[-1] = 0; self.thu.from_numpy(thu)
        thv = self.thv.to_numpy(); thv[:, 0] = thv[:, -1] = 0; self.thv.from_numpy(thv)
        thw = self.thw.to_numpy(); thw[:, :, 0] = 0; self.thw.from_numpy(thw)

    def _wall_area(self):
        """Area of glass inside each cell, per cell volume. The side wall of each layer of cells, 2 pi R ds over the layer's
        height (ds along the profile), is shared equally by the layer's cells cut by it (4 x 4 x 4 points inside and outside);
        the floor gives each cell above it dx^2 times the part of its bottom inside the glass."""
        n, nz, dx, R, dzp = self.n, self.nz, self.dx, self.R, self.dzp
        s = (np.arange(4) + 0.5) / 4
        xc = self.x0 + dx * (np.arange(n)[:, None] + s[None, :])          # (n, 4)
        r2 = xc[:, None, :, None] ** 2 + xc[None, :, None, :] ** 2         # (n, n, 4, 4)
        zp = np.arange(len(R)) * dzp; ds = np.sqrt(dzp ** 2 + np.diff(R) ** 2)
        A = np.zeros((n, n, nz))
        for k in range(nz):
            za, zb = self.z0 + k * dx, self.z0 + (k + 1) * dx
            inside = np.zeros((n, n)); tot = 0
            for c in s:
                z = za + c * dx
                if z <= 0: continue
                Rz = np.interp(min(z, self.zrim) / dzp, np.arange(len(R)), R)
                inside += (r2 < Rz * Rz).reshape(n, n, 16).sum(2); tot += 16
            if tot == 0: continue
            frac = inside / (4 * 16)
            cut = (frac > 0) & (frac < 1)
            a, b = max(za, 0.0), min(zb, self.zrim)
            if b > a and cut.any():
                m = (zp[:-1] + 0.5 * dzp > a) & (zp[:-1] + 0.5 * dzp <= b)
                side = float((2 * np.pi * 0.5 * (R[:-1] + R[1:]) * ds)[m].sum())
                A[:, :, k] += np.where(cut, side / cut.sum(), 0.0)
            if k == 2:                     # the layer standing on the floor (z0 = -2 dx)
                bot = (r2 < R[0] ** 2).reshape(n, n, 16).mean(2)
                A[:, :, k] += bot * dx * dx
        self.Awall = A
        a = (A / dx ** 3).astype(np.float32); self.ac.from_numpy(a)
        thu, thv, thw = self.thu.to_numpy(), self.thv.to_numpy(), self.thw.to_numpy()
        pad = lambda arr, ax: np.concatenate([np.take(arr, [0], ax) * 0, arr, np.take(arr, [0], ax) * 0], ax)
        au = 0.5 * (pad(a, 0)[:-1] + pad(a, 0)[1:]); av = 0.5 * (pad(a, 1)[:, :-1] + pad(a, 1)[:, 1:]); aw = 0.5 * (pad(a, 2)[:, :, :-1] + pad(a, 2)[:, :, 1:])
        self.au.from_numpy(np.where(thu > 0, au, 0).astype(np.float32)); self.av.from_numpy(np.where(thv > 0, av, 0).astype(np.float32))
        self.aw.from_numpy(np.where(thw > 0, aw, 0).astype(np.float32))
        Rf = float(np.interp(self.fill / dzp, np.arange(len(R)), R))
        self.wall_check = dict(area_cells=float(A.sum()), area_profile_below_rim=float((2 * np.pi * 0.5 * (R[:-1] + R[1:]) * ds).sum() + np.pi * R[0] ** 2),
                               R_fill=Rf)

    # ---- particles to grid (APIC, trilinear)
    @ti.kernel
    def p2g(self):
        dx = self.dx; inv = 1.0 / dx
        for I in ti.grouped(self.u): self.u[I] = 0.0; self.mu_[I] = 0.0
        for I in ti.grouped(self.v): self.v[I] = 0.0; self.mv[I] = 0.0
        for I in ti.grouped(self.w): self.w[I] = 0.0; self.mw[I] = 0.0
        for I in ti.grouped(self.cnt): self.cnt[I] = 0
        for p in self.xp:
            if self.act[p] == 1:
                X = self.xp[p]; V = self.vp[p]
                g = ti.Vector([(X[0] - self.x0) * inv, (X[1] - self.x0) * inv, (X[2] - self.z0) * inv])
                ci = ti.cast(ti.floor(g), ti.i32)
                if 0 <= ci[0] < self.n and 0 <= ci[1] < self.n and 0 <= ci[2] < self.nz:
                    self.cnt[ci] += 1
                for comp in ti.static(range(3)):
                    off = ti.Vector([0.5, 0.5, 0.5]); off[comp] = 0.0
                    gg = g - off; base = ti.cast(ti.floor(gg), ti.i32); fr = gg - base
                    C = self.cpx[p] if comp == 0 else (self.cpy[p] if comp == 1 else self.cpz[p])
                    for a, b, c in ti.static(ti.ndrange(2, 2, 2)):
                        wgt = (fr[0] if a else 1 - fr[0]) * (fr[1] if b else 1 - fr[1]) * (fr[2] if c else 1 - fr[2])
                        node = base + ti.Vector([a, b, c])
                        dpos = (ti.Vector([a, b, c]) - fr) * dx
                        val = wgt * (V[comp] + C.dot(dpos))
                        if ti.static(comp == 0):
                            if 0 <= node[0] <= self.n and 0 <= node[1] < self.n and 0 <= node[2] < self.nz:
                                self.u[node] += val; self.mu_[node] += wgt
                        elif ti.static(comp == 1):
                            if 0 <= node[0] < self.n and 0 <= node[1] <= self.n and 0 <= node[2] < self.nz:
                                self.v[node] += val; self.mv[node] += wgt
                        else:
                            if 0 <= node[0] < self.n and 0 <= node[1] < self.n and 0 <= node[2] <= self.nz:
                                self.w[node] += val; self.mw[node] += wgt

    @ti.kernel
    def normalize_force(self, dt: ti.f32, gx: ti.f32, gz: ti.f32):
        for I in ti.grouped(self.u):
            self.u[I] = (self.u[I] / self.mu_[I] + dt * gx) if self.mu_[I] > 1e-6 else 0.0
            if self.thu[I] == 0: self.u[I] = 0.0
        for I in ti.grouped(self.v):
            self.v[I] = self.v[I] / self.mv[I] if self.mv[I] > 1e-6 else 0.0
            if self.thv[I] == 0: self.v[I] = 0.0
        for I in ti.grouped(self.w):
            self.w[I] = (self.w[I] / self.mw[I] + dt * gz) if self.mw[I] > 1e-6 else 0.0
            if self.thw[I] == 0: self.w[I] = 0.0
        for I in ti.grouped(self.cnt):
            self.liq[I] = 1 if self.cnt[I] > 0 else 0

    # ---- level set of the liquid (v2)
    @ti.func
    def Rcav(self, z):        # radius of the cavity at height z (above the rim: the rim's radius)
        return self.Rz(ti.min(z, self.zrim - 1e-6))

    @ti.kernel
    def ls_empty(self):
        dx = self.dx
        for i, j, k in self.cnt:
            xc = self.x0 + (i + 0.5) * dx; yc = self.x0 + (j + 0.5) * dx; zc = self.z0 + (k + 0.5) * dx
            e = 0
            if self.cnt[i, j, k] == 0 and zc > 0:
                Rc = self.Rcav(zc) - 0.5 * dx
                if xc * xc + yc * yc < Rc * Rc: e = 1
            self.mA[i, j, k] = e
            self.Wk[i, j, k] = 0.0; self.Sk[i, j, k] = ti.Vector([0.0, 0.0, 0.0])

    @ti.kernel
    def dilate(self, src: ti.template(), dst: ti.template(), axis: ti.i32):
        for I in ti.grouped(src):
            v = 0
            for d in range(-2, 3):
                J = I; J[axis] += d
                if 0 <= J[0] < self.n and 0 <= J[1] < self.n and 0 <= J[2] < self.nz:
                    if src[J] == 1: v = 1
            dst[I] = v

    @ti.kernel
    def ls_scatter(self):
        dx = self.dx; inv = 1.0 / dx; R2 = 4.0 * dx * dx
        for p in self.xp:
            if self.act[p] == 1:
                X = self.xp[p]
                ci = ti.cast(ti.floor(ti.Vector([(X[0] - self.x0) * inv, (X[1] - self.x0) * inv, (X[2] - self.z0) * inv])), ti.i32)
                ok = 0
                if 0 <= ci[0] < self.n and 0 <= ci[1] < self.n and 0 <= ci[2] < self.nz: ok = self.nearP[ci]
                if ok == 1:
                    rr = ti.sqrt(X[0] * X[0] + X[1] * X[1]); Rw = self.Rz(X[2])
                    nim = 2 if (X[2] < self.zrim and rr > Rw - 2.0 * dx and rr > 1e-9) else 1
                    fw = (2.0 * Rw - rr) / rr if rr > 1e-9 else 0.0
                    for m in range(nim):
                        Q = X
                        if m == 1: Q = ti.Vector([X[0] * fw, X[1] * fw, X[2]])   # its image in the wall (r -> 2R - r)
                        qi = ti.cast(ti.floor(ti.Vector([(Q[0] - self.x0) * inv - 0.5, (Q[1] - self.x0) * inv - 0.5, (Q[2] - self.z0) * inv - 0.5])), ti.i32)
                        for a, b, c in ti.ndrange((-1, 3), (-1, 3), (-1, 3)):
                            J = qi + ti.Vector([a, b, c])
                            if 0 <= J[0] < self.n and 0 <= J[1] < self.n and 0 <= J[2] < self.nz:
                                if self.near[J] == 1:
                                    xc = ti.Vector([self.x0 + (J[0] + 0.5) * dx, self.x0 + (J[1] + 0.5) * dx, self.z0 + (J[2] + 0.5) * dx])
                                    dd = Q - xc; d2 = dd.dot(dd)
                                    if d2 < R2:
                                        q = 1.0 - d2 / R2; wt = q * q * q
                                        self.Wk[J] += wt; self.Sk[J] += wt * dd

    @ti.kernel
    def ls_phi(self):
        dx = self.dx
        for I in ti.grouped(self.phi):
            ph = 0.0
            if self.near[I] == 1:
                ph = (self.Sk[I] / self.Wk[I]).norm() - self.rls if self.Wk[I] > 1e-12 else 3.0 * dx
            else:
                ph = -2.0 * dx if self.cnt[I] > 0 else 2.0 * dx
            l = 1 if (ph < 0 or self.cnt[I] > 0) else 0
            if self.cnt[I] > 0 and ph >= 0: ph = -0.05 * dx
            self.phi[I] = ph; self.liq[I] = l

    @ti.kernel
    def ls_inherit(self):
        # a cell cut by the glass that reads as air takes the lowest phi of the liquid cells beside it through open faces,
        # or of the liquid cell above it if that lies well below the surface (stout-cart.js, inheritWallPhi)
        dx = self.dx
        for i, j, k in self.phi:
            self.phi2[i, j, k] = self.phi[i, j, k]; self.liq2[i, j, k] = self.liq[i, j, k]
            if self.liq[i, j, k] == 0:
                xc = self.x0 + (i + 0.5) * dx; yc = self.x0 + (j + 0.5) * dx; zc = self.z0 + (k + 0.5) * dx
                Rc = self.Rz(zc)
                if zc > 0 and zc < self.zrim and xc * xc + yc * yc >= (Rc - 0.5 * dx) ** 2:
                    best = 1.0
                    if self.thu[i, j, k] > 0 and self.isliq(i - 1, j, k): best = ti.min(best, self.phi[i - 1, j, k])
                    if self.thu[i + 1, j, k] > 0 and self.isliq(i + 1, j, k): best = ti.min(best, self.phi[i + 1, j, k])
                    if self.thv[i, j, k] > 0 and self.isliq(i, j - 1, k): best = ti.min(best, self.phi[i, j - 1, k])
                    if self.thv[i, j + 1, k] > 0 and self.isliq(i, j + 1, k): best = ti.min(best, self.phi[i, j + 1, k])
                    if k < self.nz - 1:
                        if self.thw[i, j, k + 1] > 0 and self.liq[i, j, k + 1] == 1 and self.phi[i, j, k + 1] < -0.5 * dx:
                            best = ti.min(best, self.phi[i, j, k + 1])
                    if best < 1.0:
                        self.liq2[i, j, k] = 1; self.phi2[i, j, k] = ti.min(best, -0.05 * dx)

    @ti.kernel
    def ls_commit(self):
        for I in ti.grouped(self.phi): self.phi[I] = self.phi2[I]; self.liq[I] = self.liq2[I]

    def level_set(self):
        self.ls_empty()
        self.dilate(self.mA, self.mB, 0); self.dilate(self.mB, self.mA, 1); self.dilate(self.mA, self.near, 2)
        self.dilate(self.near, self.mA, 0); self.dilate(self.mA, self.mB, 1); self.dilate(self.mB, self.nearP, 2)
        self.ls_scatter(); self.ls_phi()
        for _ in range(3): self.ls_inherit(); self.ls_commit()

    def classify(self):
        if self.fillrule: self.fill_wall_cells()     # v1 (liq from the counts, set in normalize_force)
        else: self.level_set()

    # ---- viscosity and friction on the grid, before the pressure (v2)
    @ti.func
    def _visc(self, f: ti.template(), m: ti.template(), th: ti.template(), t: ti.template(), c: ti.f32):
        for I in ti.grouped(f): t[I] = f[I]
        for I in ti.grouped(f):
            if th[I] > 0 and m[I] > 1e-6:
                lap = 0.0
                for d in ti.static(range(3)):
                    for sg in ti.static((-1, 1)):
                        J = I; J[d] += sg
                        if 0 <= J[0] < f.shape[0] and 0 <= J[1] < f.shape[1] and 0 <= J[2] < f.shape[2]:
                            if th[J] > 0 and m[J] > 1e-6: lap += t[J] - t[I]   # no flux into the glass or the air (no stress)
                f[I] = t[I] + c * lap

    @ti.kernel
    def viscosity(self, dt: ti.f32):
        c = self.nu * dt / (self.dx * self.dx)
        self._visc(self.u, self.mu_, self.thu, self.tu, c)
        self._visc(self.v, self.mv, self.thv, self.tv, c)
        self._visc(self.w, self.mw, self.thw, self.tw, c)

    @ti.func
    def band(self, i, j, k):   # a liquid cell cut by the glass within Hb of the surface: where the foam rubs the glass
        r = 0
        if 0 <= i < self.n and 0 <= j < self.n and 0 <= k < self.nz:
            if self.liq[i, j, k] == 1 and self.ac[i, j, k] > 0 and self.phi[i, j, k] >= -self.Hb: r = 1
        return r

    @ti.func
    def _fric(self, f: ti.template(), m: ti.template(), a: ti.template(), comp: ti.template(), dt: ti.f32):
        dV = self.rho * self.dx ** 3
        for I in ti.grouped(f):
            if a[I] > 0 and m[I] > 1e-6:
                u0 = f[I]
                gw = self.gs * a[I]
                gf = 0.0
                if ti.static(self.lam0 > 0):
                    L = I; L[comp] -= 1
                    if self.band(I[0], I[1], I[2]) or self.band(L[0], L[1], L[2]):
                        sp = ti.max(ti.abs(u0), 0.005)
                        gf = self.lam0 * ti.pow(sp / 0.1, -1.0 / 3.0) * a[I] / (self.rho * self.Hb)
                g = gw + gf
                if g > 0:
                    u1 = u0 * ti.exp(-g * dt); f[I] = u1
                    dE = 0.5 * dV * (u0 * u0 - u1 * u1)
                    self.ewall[None] += ti.cast(dE * gw / g, ti.f64); self.efoam[None] += ti.cast(dE * gf / g, ti.f64)

    @ti.kernel
    def friction(self, dt: ti.f32):
        self._fric(self.u, self.mu_, self.au, 0, dt)
        self._fric(self.v, self.mv, self.av, 1, dt)
        self._fric(self.w, self.mw, self.aw, 2, dt)

    @ti.kernel
    def fill_wall_pass(self):
        # a cell cut by the glass may hold no particle although liquid surrounds it (the particles stay a little off the
        # wall); left empty it would act as a pocket of air at zero pressure and drain the stout. Such a cell counts as
        # liquid when the cell above it is liquid, or when a liquid neighbour beside it has liquid above it (so the cell
        # lies below the surface). Repeated a few times.
        for i, j, k in self.liq:
            if self.liq[i, j, k] == 0 and k < self.nz - 1:
                o0 = self.thu[i, j, k]; o1 = self.thu[i + 1, j, k]; o2 = self.thv[i, j, k]; o3 = self.thv[i, j + 1, k]
                o4 = self.thw[i, j, k]; o5 = self.thw[i, j, k + 1]
                cut = o0 < 1 or o1 < 1 or o2 < 1 or o3 < 1 or o4 < 1 or o5 < 1
                if cut and o0 + o1 + o2 + o3 + o4 + o5 > 0:
                    f = 0
                    if o5 > 0 and self.liq[i, j, k + 1] == 1: f = 1
                    if o0 > 0 and self.isliq(i - 1, j, k) and self.isliq(i - 1, j, k + 1): f = 1
                    if o1 > 0 and self.isliq(i + 1, j, k) and self.isliq(i + 1, j, k + 1): f = 1
                    if o2 > 0 and self.isliq(i, j - 1, k) and self.isliq(i, j - 1, k + 1): f = 1
                    if o3 > 0 and self.isliq(i, j + 1, k) and self.isliq(i, j + 1, k + 1): f = 1
                    if f == 1: self.liq[i, j, k] = 2

    @ti.kernel
    def fill_wall_commit(self):
        for I in ti.grouped(self.liq):
            if self.liq[I] == 2: self.liq[I] = 1

    def fill_wall_cells(self, passes=4):
        for _ in range(passes): self.fill_wall_pass(); self.fill_wall_commit()

    # ---- pressure: A p = b over liquid cells, p = 0 in air, no flux through the glass (face fractions)
    @ti.func
    def isliq(self, i, j, k):
        r = 0
        if 0 <= i < self.n and 0 <= j < self.n and 0 <= k < self.nz: r = self.liq[i, j, k]
        return r

    @ti.func
    def theta(self, i, j, k, a, b, c):
        # the fraction of the way from the liquid cell (i, j, k) to the air cell (a, b, c) at which the surface lies
        # (ghost fluid); 1 for v1 and outside the box (p = 0 at the air cell's centre)
        t = 1.0
        if ti.static(self.ghost == 1):
            if 0 <= a < self.n and 0 <= b < self.n and 0 <= c < self.nz:
                pc = self.phi[i, j, k]; pn = self.phi[a, b, c]
                if pc - pn < -1e-12: t = ti.min(ti.max(pc / (pc - pn), 0.05), 1.0)
        return t

    @ti.func
    def dterm(self, th, i, j, k, a, b, c):
        r = 0.0
        if th > 0:
            r = th if self.isliq(a, b, c) else th / self.theta(i, j, k, a, b, c)
        return r

    @ti.kernel
    def build(self):
        dx = self.dx
        for i, j, k in self.liq:
            self.b[i, j, k] = 0.0; self.diag[i, j, k] = 0.0
            if self.liq[i, j, k] == 1:
                div = self.thu[i + 1, j, k] * self.u[i + 1, j, k] - self.thu[i, j, k] * self.u[i, j, k] \
                    + self.thv[i, j + 1, k] * self.v[i, j + 1, k] - self.thv[i, j, k] * self.v[i, j, k] \
                    + self.thw[i, j, k + 1] * self.w[i, j, k + 1] - self.thw[i, j, k] * self.w[i, j, k]
                self.b[i, j, k] = -div * dx
                self.diag[i, j, k] = self.dterm(self.thu[i + 1, j, k], i, j, k, i + 1, j, k) + self.dterm(self.thu[i, j, k], i, j, k, i - 1, j, k) \
                    + self.dterm(self.thv[i, j + 1, k], i, j, k, i, j + 1, k) + self.dterm(self.thv[i, j, k], i, j, k, i, j - 1, k) \
                    + self.dterm(self.thw[i, j, k + 1], i, j, k, i, j, k + 1) + self.dterm(self.thw[i, j, k], i, j, k, i, j, k - 1)

    @ti.kernel
    def matvec(self, x: ti.template(), y: ti.template()):
        for i, j, k in self.liq:
            y[i, j, k] = 0.0
            if self.liq[i, j, k] == 1 and self.diag[i, j, k] > 0:
                s = self.diag[i, j, k] * x[i, j, k]
                if self.isliq(i + 1, j, k): s -= self.thu[i + 1, j, k] * x[i + 1, j, k]
                if self.isliq(i - 1, j, k): s -= self.thu[i, j, k] * x[i - 1, j, k]
                if self.isliq(i, j + 1, k): s -= self.thv[i, j + 1, k] * x[i, j + 1, k]
                if self.isliq(i, j - 1, k): s -= self.thv[i, j, k] * x[i, j - 1, k]
                if self.isliq(i, j, k + 1): s -= self.thw[i, j, k + 1] * x[i, j, k + 1]
                if self.isliq(i, j, k - 1): s -= self.thw[i, j, k] * x[i, j, k - 1]
                y[i, j, k] = s

    @ti.kernel
    def cg_init(self):   # r = b - A p (p warm-started), z = M^-1 r, d = z
        self.s1[None] = 0.0
        for I in ti.grouped(self.r):
            rr = 0.0
            if self.liq[I] == 1 and self.diag[I] > 0: rr = self.b[I] - self.q[I]
            else: self.p[I] = 0.0
            self.r[I] = rr
            zz = rr / self.diag[I] if self.diag[I] > 0 else 0.0
            self.zv[I] = zz; self.d[I] = zz
            self.s1[None] += rr * zz

    @ti.kernel
    def dot_dq(self) -> ti.f32:
        s = 0.0
        for I in ti.grouped(self.d): s += self.d[I] * self.q[I]
        return s

    @ti.kernel
    def cg_update(self, alpha: ti.f32) -> ti.f32:
        s = 0.0
        for I in ti.grouped(self.p):
            self.p[I] += alpha * self.d[I]; self.r[I] -= alpha * self.q[I]
            zz = self.r[I] / self.diag[I] if self.diag[I] > 0 else 0.0
            self.zv[I] = zz
            s += self.r[I] * zz
        return s

    @ti.kernel
    def cg_dir(self, beta: ti.f32):
        for I in ti.grouped(self.d): self.d[I] = self.zv[I] + beta * self.d[I]

    @ti.kernel
    def rnorm(self) -> ti.f32:
        s = 0.0
        for I in ti.grouped(self.r): ti.atomic_max(s, ti.abs(self.r[I]))   # a reduction (s = max(s, ...) races on the GPU)
        return s

    @ti.kernel
    def bnorm(self) -> ti.f32:
        s = 0.0
        for I in ti.grouped(self.b): ti.atomic_max(s, ti.abs(self.b[I]))
        return s

    def solve(self, tol=1e-5, maxit=600):
        self.build()
        bn = self.bnorm()
        if bn == 0: return 0
        self.matvec(self.p, self.q); self.cg_init()
        rz = self.s1[None]; it = 0
        while it < maxit:
            self.matvec(self.d, self.q)
            dq = self.dot_dq()
            if dq <= 0: break
            alpha = rz / dq
            rz2 = self.cg_update(alpha)
            it += 1
            if it % 8 == 0 and self.rnorm() < tol * bn: break
            self.cg_dir(rz2 / rz); rz = rz2
        return it

    @ti.func
    def pside(self, i, j, k, a, b, c):
        # pressure at cell (i, j, k) seen from its neighbour (a, b, c): its own if liquid, else the ghost value that puts
        # p = 0 on the surface between them (0 at the cell's centre for v1)
        r = 0.0
        if self.isliq(i, j, k): r = self.p[i, j, k]
        elif self.isliq(a, b, c): r = self.p[a, b, c] * (1.0 - 1.0 / self.theta(a, b, c, i, j, k))
        return r

    @ti.kernel
    def project(self):
        dx = self.dx
        for i, j, k in self.u:
            self.ku[i, j, k] = 0
            if self.thu[i, j, k] > 0:
                if self.isliq(i, j, k) or self.isliq(i - 1, j, k):
                    self.u[i, j, k] -= (self.pside(i, j, k, i - 1, j, k) - self.pside(i - 1, j, k, i, j, k)) / dx; self.ku[i, j, k] = 1
            elif self.closed_zero == 1: self.ku[i, j, k] = 1; self.u[i, j, k] = 0.0      # v1: the glass zero, and known
        for i, j, k in self.v:
            self.kv[i, j, k] = 0
            if self.thv[i, j, k] > 0:
                if self.isliq(i, j, k) or self.isliq(i, j - 1, k):
                    self.v[i, j, k] -= (self.pside(i, j, k, i, j - 1, k) - self.pside(i, j - 1, k, i, j, k)) / dx; self.kv[i, j, k] = 1
            elif self.closed_zero == 1: self.kv[i, j, k] = 1; self.v[i, j, k] = 0.0
        for i, j, k in self.w:
            self.kw[i, j, k] = 0
            if self.thw[i, j, k] > 0:
                if self.isliq(i, j, k) or self.isliq(i, j, k - 1):
                    self.w[i, j, k] -= (self.pside(i, j, k, i, j, k - 1) - self.pside(i, j, k - 1, i, j, k)) / dx; self.kw[i, j, k] = 1
            elif k <= 2 or self.closed_zero == 1: self.kw[i, j, k] = 1; self.w[i, j, k] = 0.0   # v2: only the flat floor (w = 0 exactly)

    @ti.func
    def _ext(self, f: ti.template(), kf: ti.template(), tf: ti.template(), kf2: ti.template()):
        for I in ti.grouped(f):
            tf[I] = f[I]; kf2[I] = kf[I]
            if kf[I] == 0:
                s = 0.0; c = 0
                for d in ti.static(range(3)):
                    for sg in ti.static((-1, 1)):
                        J = I; J[d] += sg
                        if 0 <= J[0] < f.shape[0] and 0 <= J[1] < f.shape[1] and 0 <= J[2] < f.shape[2]:
                            if kf[J] == 1:
                                s += f[J]; c += 1
                if c > 0: tf[I] = s / c; kf2[I] = 1
                else: tf[I] = 0.0

    @ti.kernel
    def extrap_k(self):
        self._ext(self.u, self.ku, self.tu, self.ku2)
        self._ext(self.v, self.kv, self.tv, self.kv2)
        self._ext(self.w, self.kw, self.tw, self.kw2)

    @ti.kernel
    def extrap_copy(self):
        for I in ti.grouped(self.u):
            if self.thu[I] > 0 or self.closed_zero == 0: self.u[I] = self.tu[I]
            self.ku[I] = self.ku2[I]
        for I in ti.grouped(self.v):
            if self.thv[I] > 0 or self.closed_zero == 0: self.v[I] = self.tv[I]
            self.kv[I] = self.kv2[I]
        for I in ti.grouped(self.w):
            if self.thw[I] > 0 or self.closed_zero == 0: self.w[I] = self.tw[I]
            self.kw[I] = self.kw2[I]

    def extrapolate(self, layers=3):
        for _ in range(layers): self.extrap_k(); self.extrap_copy()

    # ---- grid to particles (APIC), move, keep inside the glass, count what leaves over the rim
    @ti.kernel
    def g2p(self, dt: ti.f32):
        dx = self.dx; inv = 1.0 / dx
        self.mom[None] = ti.Vector([0.0, 0.0, 0.0]); self.nact[None] = 0
        for p in self.xp:
            if self.act[p] == 1:
                X = self.xp[p]
                g = ti.Vector([(X[0] - self.x0) * inv, (X[1] - self.x0) * inv, (X[2] - self.z0) * inv])
                newv = ti.Vector([0.0, 0.0, 0.0])
                for comp in ti.static(range(3)):
                    off = ti.Vector([0.5, 0.5, 0.5]); off[comp] = 0.0
                    gg = g - off; base = ti.cast(ti.floor(gg), ti.i32); fr = gg - base
                    vel = 0.0; C = ti.Vector([0.0, 0.0, 0.0])
                    for a, b, c in ti.static(ti.ndrange(2, 2, 2)):
                        node = base + ti.Vector([a, b, c])
                        val = 0.0
                        if ti.static(comp == 0):
                            if 0 <= node[0] <= self.n and 0 <= node[1] < self.n and 0 <= node[2] < self.nz: val = self.u[node]
                        elif ti.static(comp == 1):
                            if 0 <= node[0] < self.n and 0 <= node[1] <= self.n and 0 <= node[2] < self.nz: val = self.v[node]
                        else:
                            if 0 <= node[0] < self.n and 0 <= node[1] < self.n and 0 <= node[2] <= self.nz: val = self.w[node]
                        wa = fr[0] if a else 1 - fr[0]; wb = fr[1] if b else 1 - fr[1]; wc = fr[2] if c else 1 - fr[2]
                        vel += wa * wb * wc * val
                        # gradient of the trilinear weight
                        C += val * ti.Vector([(1 if a else -1) * wb * wc, wa * (1 if b else -1) * wc, wa * wb * (1 if c else -1)]) * inv
                    newv[comp] = vel
                    if ti.static(comp == 0): self.cpx[p] = C
                    elif ti.static(comp == 1): self.cpy[p] = C
                    else: self.cpz[p] = C
                Xn = X + dt * newv
                # the glass: push a particle that crossed the wall back inside and drop its velocity into the wall
                r = ti.sqrt(Xn[0] * Xn[0] + Xn[1] * Xn[1])
                if Xn[2] < 0.1 * dx:
                    Xn[2] = 0.1 * dx
                    if newv[2] < 0: newv[2] = 0.0
                if Xn[2] < self.zrim:
                    R = self.Rz(Xn[2]) - 0.1 * dx
                    if r > R and r > 0:
                        nr = ti.Vector([Xn[0] / r, Xn[1] / r, 0.0])
                        Xn[0] *= R / r; Xn[1] *= R / r
                        vn = newv.dot(nr)
                        if vn > 0: newv -= vn * nr
                else:
                    if r > self.Rz(self.zrim - 1e-6):   # over the rim and outside it: spilled
                        self.act[p] = 0; self.spilled[None] += 1
                if Xn[2] > self.z0 + (self.nz - 1) * dx: self.act[p] = 0; self.spilled[None] += 1
                self.xp[p] = Xn; self.vp[p] = newv
                if self.act[p] == 1:
                    self.mom[None] += newv; self.nact[None] += 1

    @ti.kernel
    def col_counts(self, out: ti.types.ndarray()):
        for i, j in ti.ndrange(self.n, self.n): out[i, j] = 0
        for p in self.xp:
            if self.act[p] == 1:
                X = self.xp[p]
                i = ti.cast(ti.floor((X[0] - self.x0) / self.dx), ti.i32); j = ti.cast(ti.floor((X[1] - self.x0) / self.dx), ti.i32)
                if 0 <= i < self.n and 0 <= j < self.n: out[i, j] += 1

    def step(self, dt, gx, gz):
        self.p2g(); self.normalize_force(dt, gx, gz); self.classify()
        if self.nu > 0: self.viscosity(dt)
        if self.gs > 0 or self.lam0 > 0: self.friction(dt)
        it = self.solve(); self.project(); self.extrapolate(); self.g2p(dt)
        return it

    def max_speed(self):
        return float(np.abs(self.vp.to_numpy()[self.act.to_numpy() == 1]).max())


NR, NTH = 16, 64   # the website's drawing grid (StoutView): r = R(h) ir / 16, theta = 2 pi ith / 64


def polar_surface(S, fill):
    """The surface on the website's polar grid. Each column of the grid (dx by dx, vertical) holds count x V_p of stout,
    so its surface is at z_in + count V_p / dx^2, z_in the height where the glass has widened past the column's centre
    (volume-exact for the columns clear of the wall). Near the wall (beyond r1 = R(h) - 3.5 dx) the columns are cut by
    the glass, so the height there is extended linearly along the radius from r1 and r1 - 3.5 dx (as the website does)."""
    n, dx = S.n, S.dx
    cnt = np.zeros((n, n), np.int32); S.col_counts(cnt)
    c = S.x0 + (np.arange(n) + 0.5) * dx
    X, Y = np.meshgrid(c, c, indexing="ij"); rc = np.hypot(X, Y)
    zz = np.arange(len(S.R)) * S.dzp
    zin = np.interp(rc, np.maximum.accumulate(S.R), zz, right=np.nan)
    Vp = S.V / S.N
    Hc = zin + cnt * Vp / dx ** 2
    # a light 3 x 3 average over the columns clear of the wall (one particle more or less in a column is 0.2 mm at 1.5 mm)
    ok = np.isfinite(Hc) & (rc < float(np.interp(fill / S.dzp, np.arange(len(S.R)), S.R)) - 1.5 * dx)
    Hz = np.where(ok, Hc, 0.0); W = ok.astype(float)
    Hs = sum(np.roll(np.roll(Hz, a, 0), b, 1) for a in (-1, 0, 1) for b in (-1, 0, 1))
    Ws = sum(np.roll(np.roll(W, a, 0), b, 1) for a in (-1, 0, 1) for b in (-1, 0, 1))
    Hc = np.where(ok, Hs / np.maximum(Ws, 1), Hc)
    Rh = float(np.interp(fill / S.dzp, np.arange(len(S.R)), S.R)); r1 = Rh - 3.5 * dx; r2 = r1 - 3.5 * dx

    def bil(x, y):
        fx = (x - S.x0) / dx - 0.5; fy = (y - S.x0) / dx - 0.5
        i = np.clip(np.floor(fx).astype(int), 0, n - 2); j = np.clip(np.floor(fy).astype(int), 0, n - 2); tx = fx - i; ty = fy - j
        return (1 - tx) * (1 - ty) * Hc[i, j] + tx * (1 - ty) * Hc[i + 1, j] + (1 - tx) * ty * Hc[i, j + 1] + tx * ty * Hc[i + 1, j + 1]
    th = 2 * np.pi * np.arange(NTH) / NTH; out = np.zeros((NR + 1, NTH))
    for ir in range(NR + 1):
        r = Rh * ir / NR
        if r <= r1: out[ir] = bil(r * np.cos(th), r * np.sin(th))
        else:
            h1 = bil(r1 * np.cos(th), r1 * np.sin(th)); h2 = bil(r2 * np.cos(th), r2 * np.sin(th))
            out[ir] = h1 + (r - r1) * (h1 - h2) / (r1 - r2)
    # around each ring, a short circular average (weights 1 2 3 2 1 over 5 points 28 degrees wide): it keeps the swing's
    # shape and removes the column-by-column flicker of the particle counts
    w = np.array([1, 2, 3, 2, 1], float) / 9
    out = sum(w[k] * np.roll(out, k - 2, axis=1) for k in range(5))
    return out


def run(R, dzp, fill, rho, ride, end, fps=30, dx=0.0015, ppc=2, log=print, cfl=0.8, dtmax=0.002, progress_s=60, model="full"):
    road = road_table(ride["road"], xmax=max(14.0, 0.5 + ride["v0"] * end * 1.2 + 2))
    S = Stout(R, dzp, fill, rho, dx, ppc, model=MODELS[model])
    params = dict(CART_COMMON, v0=ride["v0"], ml=S.rho * S.V, ctrl={"off": 0, "speed": 1, "preview": 2}[ride["ctrl"]],
                  susp=1 if ride["susp"] else 0)
    cart = Cart(params, road)
    log(f"glass grid {S.n} x {S.n} x {S.nz} = {S.ncells:,} cells of {dx * 1e3:.1f} mm; {S.N:,} particles; stout {S.rho * S.V * 1e3:.1f} g")
    rec = dict(t=[], x=[], v=[], zb=[], zw=[], lean_mm=[], spill_g=[], P=[])

    def record(t):
        P = polar_surface(S, fill)
        rec["t"].append(round(t, 4)); rec["x"].append(cart.x); rec["v"].append(cart.vx); rec["zb"].append(cart.zb); rec["zw"].append(cart.zw)
        rec["lean_mm"].append(float((P[NR, 0] - P[NR, NTH // 2]) * 1e3)); rec["spill_g"].append(float(S.spilled[None] * S.mp * 1e3))
        rec["P"].append(P)

    t = 0.0; nsteps = 0; its = 0; Pprev = None; dtprev = None; F = (0.0, 0.0); spill_prev = 0
    next_frame = 0.0; T0 = time.time(); tlast = T0
    S.vp.fill(0); S.cpx.fill(0); S.cpy.fill(0); S.cpz.fill(0)
    while t < end - 1e-9:
        if t >= next_frame - 1e-9: record(next_frame); next_frame += 1.0 / fps
        vmax = S.max_speed() if nsteps % 10 == 0 else vmax
        dt = min(dtmax, cfl * dx / max(vmax, 1e-6), end - t)
        # cart over this step, with the stout's push from the last step; the glass's acceleration over the step
        vx0, vz0 = cart.vx, cart.vzb
        nsub = max(1, int(round(dt / 1e-4))); hc = dt / nsub
        for _ in range(nsub): cart.step(hc, F[0], F[1])
        ax, az = (cart.vx - vx0) / dt, (cart.vzb - vz0) / dt
        its += S.step(dt, -ax, -9.81 - az)
        # the stout's push on the glass: minus the change of its momentum in the glass's frame (plus what spilled)
        P = np.array(S.mom[None].to_numpy(), float) * S.mp
        sp = S.spilled[None]
        if Pprev is not None:
            F = (-(P[0] - Pprev[0]) / dtprev, -(P[2] - Pprev[2]) / dtprev)
        cart.ml = S.rho * S.V * S.nact[None] / S.N
        Pprev, dtprev = P, dt
        t += dt; nsteps += 1
        if time.time() - tlast > progress_s:
            tlast = time.time(); el = tlast - T0
            log(f"{t:.2f} of {end} s of stout done; {nsteps:,} steps, {its / nsteps:.0f} pressure iterations a step; about {el / t * (end - t) / 60:.1f} min left")
    if t >= next_frame - 1e-9: record(next_frame)
    wall = time.time() - T0
    return rec, dict(steps=nsteps, cg_iterations=its, wall_s=wall, cells=S.ncells, particles=S.N, dx=dx), road