/* Fig. 12: a pint of Guinness on a one-wheel cart.
 *
 * Fluid: the incompressible Navier–Stokes equations for the stout, solved in the glass's frame by APIC
 * (particles carry the velocity and its local gradient, a staggered MAC grid enforces div u = 0):
 *     Du/Dt = -grad(p)/rho + nu lap(u) + g - a_glass(t),   div u = 0,   p = 0 on the free surface.
 * The glass translates with the cart body and never rotates, so its frame is non-inertial only through
 * the uniform fictitious force -a_glass. The glass is an upright circular cylinder (radius R); its wall is
 * cut through the Cartesian cells with fractional face areas (Batty, Bertails & Bridson 2007), and the
 * free surface uses ghost-fluid pressure (Enright et al. 2003). The forcing lies in the x-z plane and the
 * glass is mirror-symmetric about y = 0, so the flow is too: only y >= 0 is solved, with v = 0 on y = 0.
 *
 * Cart: one wheel with a radial tyre on a road z_r(x), a body guided vertically on the axle, a spring
 * and a damper between them, the cart free to roll in x. The tyre force acts along the contact normal,
 * so on a slope it has a horizontal part -N z_a'(x): that is what pushes the glass forward and back.
 * The liquid acts back on the cart through the rate of change of its momentum.
 *
 * SI units throughout. Runs in the browser (window.StoutCart) and in Node (require).
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.StoutCart = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ------------------------------------------------------------------ fluid */
  function Fluid(o) {
    o = o || {};
    this.R = o.R || 0.04;           // inner radius of the glass, m
    this.h0 = o.h0 || 0.06;         // depth of stout at rest, m
    this.dx = o.dx || 0.004;        // grid cell, m
    this.rho = o.rho || 1000;       // density, kg/m^3
    this.nu = o.nu != null ? o.nu : 1.0e-6;   // kinematic viscosity, m^2/s (taken as water)
    this.g = o.g || 9.81;
    const R = this.R, dx = this.dx;
    this.nx = Math.round(2 * R / dx);
    this.ny = Math.round(R / dx);
    this.nz = Math.ceil((o.H || 0.092) / dx);
    this.H = this.nz * dx;          // the box top (the rim, closed by a lid the liquid must not reach)
    this.x0 = -R;
    const nx = this.nx, ny = this.ny, nz = this.nz;
    this.nc = nx * ny * nz;
    this.nu_ = (nx + 1) * ny * nz; this.nv_ = nx * (ny + 1) * nz; this.nw_ = nx * ny * (nz + 1);
    const F = Float64Array;
    this.u = new F(this.nu_); this.v = new F(this.nv_); this.w = new F(this.nw_);
    this.uo = new F(this.nu_); this.vo = new F(this.nv_); this.wo = new F(this.nw_);
    this.mu = new F(this.nu_); this.mv = new F(this.nv_); this.mw = new F(this.nw_);   // P2G weights
    this.au = new F(this.nu_); this.av = new F(this.nv_); this.aw = new F(this.nw_);   // open face fractions
    this.ku = new Uint8Array(this.nu_); this.kv = new Uint8Array(this.nv_); this.kw = new Uint8Array(this.nw_); // valid
    this.tmpU = new F(this.nu_); this.tmpV = new F(this.nv_); this.tmpW = new F(this.nw_);
    this.cnt = new Int32Array(this.nc);       // particles per cell
    this.fluid = new Uint8Array(this.nc);
    this.phi = new F(this.nc);
    this.q = new F(this.nc); this.rhs = new F(this.nc);
    this.Ad = new F(this.nc); this.Ax = new F(this.nc); this.Ay = new F(this.nc); this.Az = new F(this.nc);
    this.mic = new F(this.nc); this.r_ = new F(this.nc); this.z_ = new F(this.nc); this.s_ = new F(this.nc);
    this.faceFractions();
    this.ppcSide = o.ppcSide || 2;
    this.wallImages = o.wallImages != null ? o.wallImages : true;
    this.rpFactor = o.rpFactor || 1.0;
    this.forcedPhi = o.forcedPhi != null ? o.forcedPhi : 0.05;
    this.thetaMin = o.thetaMin || 0.05;
    this.relaxStrength = o.relax != null ? o.relax : 0;   // off: not needed at dt = 1/400 s (measured)
    this.seed(this.ppcSide, o.seed || 12345);
    this.t = 0;
    this.cgIters = 0;
  }

  Fluid.prototype.faceFractions = function () {
    const R = this.R, dx = this.dx, nx = this.nx, ny = this.ny, nz = this.nz, x0 = this.x0;
    // open fraction of each face; slivers under 10 % are closed (moves the wall by < 0.1 dx, keeps the solve well posed)
    const clamp = (a) => { a = Math.max(0, Math.min(1, a)); return a < 0.1 ? 0 : a; };
    for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i <= nx; i++) {
      const xf = x0 + i * dx, Y = R * R - xf * xf > 0 ? Math.sqrt(R * R - xf * xf) : 0;
      this.au[i + (nx + 1) * (j + ny * k)] = clamp((Y - j * dx) / dx);
    }
    for (let k = 0; k < nz; k++) for (let j = 0; j <= ny; j++) for (let i = 0; i < nx; i++) {
      const yf = j * dx, X = R * R - yf * yf > 0 ? Math.sqrt(R * R - yf * yf) : 0;
      const a = x0 + i * dx, b = a + dx;
      const len = Math.max(0, Math.min(b, X) - Math.max(a, -X));
      this.av[i + nx * (j + (ny + 1) * k)] = j === 0 ? 0 : clamp(len / dx);   // y = 0 is the mirror plane: v = 0
    }
    const S = 10;
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      let inside = 0;
      for (let a = 0; a < S; a++) for (let b = 0; b < S; b++) {
        const x = x0 + (i + (a + 0.5) / S) * dx, y = (j + (b + 0.5) / S) * dx;
        if (x * x + y * y < R * R) inside++;
      }
      let f = inside / (S * S); if (f < 0.1) f = 0;
      for (let k = 0; k <= nz; k++) this.aw[i + nx * (j + ny * k)] = (k === 0 || k === nz) ? 0 : f;
    }
  };

  Fluid.prototype.seed = function (s, seed) {
    let st = seed >>> 0;
    const rnd = () => { st = (st * 1664525 + 1013904223) >>> 0; return st / 4294967296; };
    const R = this.R, dx = this.dx, xs = [], ys = [], zs = [];
    for (let k = 0; k < this.nz; k++) for (let j = 0; j < this.ny; j++) for (let i = 0; i < this.nx; i++)
      for (let a = 0; a < s; a++) for (let b = 0; b < s; b++) for (let c = 0; c < s; c++) {
        const x = this.x0 + (i + (a + 0.5 + 0.6 * (rnd() - 0.5)) / s) * dx;
        const y = (j + (b + 0.5 + 0.6 * (rnd() - 0.5)) / s) * dx;
        const z = (k + (c + 0.5 + 0.6 * (rnd() - 0.5)) / s) * dx;
        if (x * x + y * y < (R - 0.15 * dx) ** 2 && z < this.h0 && y > 0) { xs.push(x); ys.push(y); zs.push(z); }
      }
    const n = this.np = xs.length;
    this.px = Float64Array.from(xs); this.py = Float64Array.from(ys); this.pz = Float64Array.from(zs);
    this.pu = new Float64Array(n); this.pv = new Float64Array(n); this.pw = new Float64Array(n);
    // APIC: each particle also carries the local velocity gradient, one row per component (Jiang et al. 2015)
    this.pc = [0, 1, 2].map(() => [new Float64Array(n), new Float64Array(n), new Float64Array(n)]);
    // the half glass holds half the liquid: m_l/2 = rho * pi R^2 h0 / 2, shared equally by the particles
    this.mLiquid = this.rho * Math.PI * R * R * this.h0;
    this.mp = 0.5 * this.mLiquid / n;
    // radius of the particles for the surface reconstruction: one particle spacing, so that the liquid at rest
    // reads its true depth h0 (measured: 60.0 +- 0.3 mm on 3 and 4 mm grids, tools/fig12/check.cjs rest)
    this.rp = dx / s * this.rpFactor;
    this.Vseed = (dx / s) ** 3;
  };

  // trilinear stencil on a staggered component with dims (sx,sy,sz) and offsets (ox,oy,oz) in cells:
  // the 8 node indices (clamped: a node beyond y = 0 is its own mirror image), weights, weight gradients
  // with respect to the particle position, and the node-minus-particle offsets (unclamped, geometric)
  function stencil(f, x, y, z, sx, sy, sz, ox, oy, oz) {
    const dx = f.dx, fx = (x - f.x0) / dx - ox, fy = y / dx - oy, fz = z / dx - oz;
    const i = Math.floor(fx), j = Math.floor(fy), k = Math.floor(fz);
    const tx = fx - i, ty = fy - j, tz = fz - k;
    const S = stencil.out;
    const I = S.I, J = S.J, K = S.K, wx = S.wx, wy = S.wy, wz = S.wz, gx = S.g;
    I[0] = i < 0 ? 0 : i >= sx ? sx - 1 : i; I[1] = i + 1 < 0 ? 0 : i + 1 >= sx ? sx - 1 : i + 1;
    J[0] = j < 0 ? 0 : j >= sy ? sy - 1 : j; J[1] = j + 1 < 0 ? 0 : j + 1 >= sy ? sy - 1 : j + 1;
    K[0] = k < 0 ? 0 : k >= sz ? sz - 1 : k; K[1] = k + 1 < 0 ? 0 : k + 1 >= sz ? sz - 1 : k + 1;
    wx[0] = 1 - tx; wx[1] = tx; wy[0] = 1 - ty; wy[1] = ty; wz[0] = 1 - tz; wz[1] = tz; gx[0] = -1 / dx; gx[1] = 1 / dx;
    let n = 0;
    for (let c = 0; c < 2; c++) for (let b = 0; b < 2; b++) for (let a = 0; a < 2; a++) {
      S.idx[n] = I[a] + sx * (J[b] + sy * K[c]);
      S.wt[n] = wx[a] * wy[b] * wz[c];
      S.gx[n] = gx[a] * wy[b] * wz[c]; S.gy[n] = wx[a] * gx[b] * wz[c]; S.gz[n] = wx[a] * wy[b] * gx[c];
      S.dx[n] = (a - tx) * dx; S.dy[n] = (b - ty) * dx; S.dz[n] = (c - tz) * dx;
      n++;
    }
    return S;
  }
  stencil.out = { idx: new Int32Array(8), wt: new Float64Array(8), gx: new Float64Array(8), gy: new Float64Array(8),
    gz: new Float64Array(8), dx: new Float64Array(8), dy: new Float64Array(8), dz: new Float64Array(8),
    I: new Int32Array(2), J: new Int32Array(2), K: new Int32Array(2), wx: new Float64Array(2), wy: new Float64Array(2),
    wz: new Float64Array(2), g: new Float64Array(2) };

  Fluid.prototype.comp = function (c) {
    const nx = this.nx, ny = this.ny, nz = this.nz;
    if (c === 0) return [this.u, nx + 1, ny, nz, 0, 0.5, 0.5];
    if (c === 1) return [this.v, nx, ny + 1, nz, 0.5, 0, 0.5];
    return [this.w, nx, ny, nz + 1, 0.5, 0.5, 0];
  };

  Fluid.prototype.sample = function (c, x, y, z) {
    const [a, sx, sy, sz, ox, oy, oz] = this.comp(c);
    const S = stencil(this, x, y, z, sx, sy, sz, ox, oy, oz);
    let s = 0;
    for (let m = 0; m < 8; m++) s += a[S.idx[m]] * S.wt[m];
    return s;
  };

  Fluid.prototype.p2g = function () {
    const comps = [[this.u, this.mu, this.pu], [this.v, this.mv, this.pv], [this.w, this.mw, this.pw]];
    for (let c = 0; c < 3; c++) {
      const [a, m, pvel] = comps[c], [cx, cy, cz] = this.pc[c];
      a.fill(0); m.fill(0);
      const [, sx, sy, sz, ox, oy, oz] = this.comp(c);
      for (let p = 0; p < this.np; p++) {
        const S = stencil(this, this.px[p], this.py[p], this.pz[p], sx, sy, sz, ox, oy, oz);
        const u0 = pvel[p], gx = cx[p], gy = cy[p], gz = cz[p];
        for (let n = 0; n < 8; n++) {
          const wt = S.wt[n];
          a[S.idx[n]] += wt * (u0 + gx * S.dx[n] + gy * S.dy[n] + gz * S.dz[n]); m[S.idx[n]] += wt;
        }
      }
      for (let n = 0; n < a.length; n++) a[n] = m[n] > 1e-9 ? a[n] / m[n] : 0;
    }
  };

  // particles sorted by cell (cellStart, sorted) and counted per cell (cnt)
  Fluid.prototype.levelSetBins = function () {
    const nx = this.nx, ny = this.ny, nz = this.nz, dx = this.dx, nc = this.nc;
    const cnt = this.cnt; cnt.fill(0);
    if (!this.cellStart || this.cellStart.length !== nc + 1) { this.cellStart = new Int32Array(nc + 1); }
    if (!this.sorted || this.sorted.length !== this.np) this.sorted = new Int32Array(this.np);
    const cellOf = (p) => {
      let i = Math.floor((this.px[p] - this.x0) / dx), j = Math.floor(this.py[p] / dx), k = Math.floor(this.pz[p] / dx);
      i = i < 0 ? 0 : i >= nx ? nx - 1 : i; j = j < 0 ? 0 : j >= ny ? ny - 1 : j; k = k < 0 ? 0 : k >= nz ? nz - 1 : k;
      return i + nx * (j + ny * k);
    };
    const pc = this.pcell || (this.pcell = new Int32Array(this.np));
    for (let p = 0; p < this.np; p++) { pc[p] = cellOf(p); cnt[pc[p]]++; }
    const cs = this.cellStart; cs[0] = 0;
    for (let c = 0; c < nc; c++) cs[c + 1] = cs[c] + cnt[c];
    const fillp = this.fillp || (this.fillp = new Int32Array(nc));
    fillp.set(cs.subarray(0, nc));
    for (let p = 0; p < this.np; p++) this.sorted[fillp[pc[p]]++] = p;
  };

  // Level set of the liquid from the particles (Zhu & Bridson 2005), and the fluid cells (phi < 0)
  Fluid.prototype.levelSet = function () {
    const nx = this.nx, ny = this.ny, nz = this.nz, dx = this.dx, nc = this.nc;
    this.levelSetBins(); const cnt = this.cnt;
    const Rk = 2 * dx, R2 = Rk * Rk, r = this.rp, Rc = this.R - 0.5 * dx;
    // the level set is measured only within two cells of an empty cell inside the glass; deeper cells are liquid
    const empty = this.emptyMask || (this.emptyMask = new Uint8Array(nc));
    for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const c = i + nx * (j + ny * k), xc = this.x0 + (i + 0.5) * dx, yc = (j + 0.5) * dx;
      empty[c] = cnt[c] === 0 && xc * xc + yc * yc < Rc * Rc ? 1 : 0;
    }
    for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const c = i + nx * (j + ny * k);
      let near = false;
      for (let kk = Math.max(0, k - 2); kk <= Math.min(nz - 1, k + 2) && !near; kk++)
        for (let jj = Math.max(0, j - 2); jj <= Math.min(ny - 1, j + 2) && !near; jj++)
          for (let ii = Math.max(0, i - 2); ii <= Math.min(nx - 1, i + 2); ii++) if (empty[ii + nx * (jj + ny * kk)]) { near = true; break; }
      if (!near) { this.phi[c] = cnt[c] > 0 ? -2 * dx : 2 * dx; continue; }
      const xc = this.x0 + (i + 0.5) * dx, yc = (j + 0.5) * dx, zc = (k + 0.5) * dx;
      const ph = this.phiAt(xc, yc, zc, Rk, R2, r);
      this.phi[c] = ph;
    }
    // Liquid cells: inside the level set, or holding particles (so that no particle is left without pressure). A cell
    // that holds particles but reads phi >= 0 gets phi = -0.05 dx. Measured: -0.5 dx here broke the slosh (4.3 Hz
    // instead of 3.5 Hz on the 4 mm grid); the spurious flow at rest that first suggested it came from the time
    // step (clean at dt = 1/400 s), not from this.
    for (let c = 0; c < nc; c++) {
      this.fluid[c] = this.phi[c] < 0 || cnt[c] > 0 ? 1 : 0;
      if (cnt[c] > 0 && this.phi[c] >= 0) this.phi[c] = -this.forcedPhi * dx;
    }
    // Cells cut by the glass wall hold few or no particles, and the particle level set reads them as air. A wall
    // cell that shares an open side face with liquid at the same height is liquid: otherwise it would be a
    // pocket of zero pressure below the surface and the stout would drain into it.
    const R = this.R, ph = this.phi, fl = this.fluid;
    const U = (i, j, k) => i + (nx + 1) * (j + ny * k), V = (i, j, k) => i + nx * (j + (ny + 1) * k);
    for (let sweep = 0; sweep < 2; sweep++) for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const c = i + nx * (j + ny * k);
      if (fl[c]) continue;
      const x = this.x0 + (i + 0.5) * dx, y = (j + 0.5) * dx;
      if (x * x + y * y < (R - 0.5 * dx) ** 2) continue;            // only cells cut by the wall
      let best = 1;
      if (i > 0 && this.au[U(i, j, k)] > 0 && fl[c - 1]) best = Math.min(best, ph[c - 1]);
      if (i < nx - 1 && this.au[U(i + 1, j, k)] > 0 && fl[c + 1]) best = Math.min(best, ph[c + 1]);
      if (j > 0 && this.av[V(i, j, k)] > 0 && fl[c - nx]) best = Math.min(best, ph[c - nx]);
      if (j < ny - 1 && this.av[V(i, j + 1, k)] > 0 && fl[c + nx]) best = Math.min(best, ph[c + nx]);
      if (best < 1) { fl[c] = 1; ph[c] = Math.min(best, -0.05 * dx); }
    }
  };

  // phi(x) = |x - xbar| - r, xbar the kernel-weighted mean of nearby particles (mirror images included)
  Fluid.prototype.phiAt = function (x, y, z, Rk, R2, r) {
    const nx = this.nx, ny = this.ny, nz = this.nz, dx = this.dx;
    const span = Math.ceil(Rk / dx);
    const ic = Math.floor((x - this.x0) / dx), jc = Math.floor(y / dx), kc = Math.floor(z / dx);
    let W = 0, sx = 0, sy = 0, sz = 0;
    for (let k = Math.max(0, kc - span); k <= Math.min(nz - 1, kc + span); k++)
      for (let j = Math.max(0, jc - span); j <= Math.min(ny - 1, Math.abs(jc) + span); j++)
        for (let i = Math.max(0, ic - span); i <= Math.min(nx - 1, ic + span); i++) {
          const c = i + nx * (j + ny * k);
          for (let s = this.cellStart[c]; s < this.cellStart[c + 1]; s++) {
            const p = this.sorted[s], ppx = this.px[p], ppy = this.py[p], ppz = this.pz[p];
            const ddz = ppz - z, rr = Math.sqrt(ppx * ppx + ppy * ppy);
            // the particle, its image in the mirror plane y = 0, and, near the wall, its images in the wall
            // (r -> 2R - r): the liquid meets the wall at a right angle and the wall cells read as liquid
            const nImg = this.wallImages && rr > this.R - Rk ? 4 : 2, fw = rr > 1e-9 ? (2 * this.R - rr) / rr : 0;
            for (let m = 0; m < nImg; m++) {
              const qx = m < 2 ? ppx : ppx * fw, qy0 = m < 2 ? ppy : ppy * fw, qy = (m & 1) ? -qy0 : qy0;
              const ddx = qx - x, ddy = qy - y, d2 = ddx * ddx + ddy * ddy + ddz * ddz;
              if (d2 < R2) {
                const q = 1 - d2 / R2, wt = q * q * q;
                W += wt; sx += wt * qx; sy += wt * qy; sz += wt * ppz;
              }
            }
          }
        }
    if (W < 1e-12) return 3 * dx;
    const mx = sx / W - x, my = sy / W - y, mz = sz / W - z;
    return Math.sqrt(mx * mx + my * my + mz * mz) - r;
  };

  Fluid.prototype.forces = function (dt, ax, az) {
    const gz = -this.g - az, gx = -ax;
    for (let n = 0; n < this.nu_; n++) if (this.au[n] > 0) this.u[n] += dt * gx;
    for (let n = 0; n < this.nw_; n++) if (this.aw[n] > 0) this.w[n] += dt * gz;
    if (this.nu > 0) this.viscosity(dt);
  };

  // explicit nu * lap(u) on each component (stable: nu dt / dx^2 ~ 1e-4)
  Fluid.prototype.viscosity = function (dt) {
    const c = this.nu * dt / (this.dx * this.dx);
    const arr = [[this.u, this.tmpU, this.au], [this.v, this.tmpV, this.av], [this.w, this.tmpW, this.aw]];
    for (let comp = 0; comp < 3; comp++) {
      const [a, t, open] = arr[comp];
      const [, sx, sy, sz] = this.comp(comp);
      t.set(a);
      for (let k = 1; k < sz - 1; k++) for (let j = 1; j < sy - 1; j++) for (let i = 1; i < sx - 1; i++) {
        const n = i + sx * (j + sy * k);
        if (open[n] <= 0) continue;
        const lap = t[n - 1] + t[n + 1] + t[n - sx] + t[n + sx] + t[n - sx * sy] + t[n + sx * sy] - 6 * t[n];
        a[n] += c * lap;
      }
    }
  };

  // pressure projection: solve A q = b for q = p dt / rho with face weights and ghost-fluid surface
  Fluid.prototype.project = function (dt) {
    const nx = this.nx, ny = this.ny, nz = this.nz, dx = this.dx;
    const fl = this.fluid, phi = this.phi;
    const Ad = this.Ad, Ax = this.Ax, Ay = this.Ay, Az = this.Az, b = this.rhs;
    Ad.fill(0); Ax.fill(0); Ay.fill(0); Az.fill(0); b.fill(0);
    const tmin = this.thetaMin;
    const th = (c, n) => { let t = phi[c] / (phi[c] - phi[n]); return t < tmin ? tmin : t > 1 ? 1 : t; };
    const U = (i, j, k) => i + (nx + 1) * (j + ny * k), V = (i, j, k) => i + nx * (j + (ny + 1) * k), Wd = (i, j, k) => i + nx * (j + ny * k);
    for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const c = i + nx * (j + ny * k);
      if (!fl[c]) continue;
      // the six faces: [weight, velocity, sign, neighbour cell or -1]
      const faces = [
        [this.au[U(i + 1, j, k)], this.u[U(i + 1, j, k)], 1, i + 1 < nx ? c + 1 : -1, 0],
        [this.au[U(i, j, k)], this.u[U(i, j, k)], -1, i > 0 ? c - 1 : -1, 0],
        [this.av[V(i, j + 1, k)], this.v[V(i, j + 1, k)], 1, j + 1 < ny ? c + nx : -1, 1],
        [this.av[V(i, j, k)], this.v[V(i, j, k)], -1, j > 0 ? c - nx : -1, 1],
        [this.aw[Wd(i, j, k + 1)], this.w[Wd(i, j, k + 1)], 1, k + 1 < nz ? c + nx * ny : -1, 2],
        [this.aw[Wd(i, j, k)], this.w[Wd(i, j, k)], -1, k > 0 ? c - nx * ny : -1, 2],
      ];
      let div = 0;
      for (let f = 0; f < 6; f++) {
        const [wt, vel, s, nb, axis] = faces[f];
        if (wt <= 0) continue;
        div += s * wt * vel;
        if (nb < 0) continue;
        if (fl[nb]) {
          Ad[c] += wt;
          if (s > 0) { if (axis === 0) Ax[c] = -wt; else if (axis === 1) Ay[c] = -wt; else Az[c] = -wt; }
        } else {
          Ad[c] += wt / th(c, nb);
        }
      }
      b[c] = -dx * div;
    }
    this.pcg();
    // velocity update on faces with at least one liquid side
    const q = this.q;
    this.ku.fill(0); this.kv.fill(0); this.kw.fill(0);
    const ghost = (c, n) => q[c] * (1 - 1 / th(c, n));
    for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 1; i < nx; i++) {
      const f = U(i, j, k); if (this.au[f] <= 0) continue;
      const cl = (i - 1) + nx * (j + ny * k), cr = cl + 1;
      if (!fl[cl] && !fl[cr]) continue;
      const ql = fl[cl] ? q[cl] : ghost(cr, cl), qr = fl[cr] ? q[cr] : ghost(cl, cr);
      this.u[f] -= (qr - ql) / dx; this.ku[f] = 1;
    }
    for (let k = 0; k < nz; k++) for (let j = 1; j < ny; j++) for (let i = 0; i < nx; i++) {
      const f = V(i, j, k); if (this.av[f] <= 0) continue;
      const cl = i + nx * ((j - 1) + ny * k), cr = cl + nx;
      if (!fl[cl] && !fl[cr]) continue;
      const ql = fl[cl] ? q[cl] : ghost(cr, cl), qr = fl[cr] ? q[cr] : ghost(cl, cr);
      this.v[f] -= (qr - ql) / dx; this.kv[f] = 1;
    }
    for (let k = 1; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const f = Wd(i, j, k); if (this.aw[f] <= 0) continue;
      const cl = i + nx * (j + ny * (k - 1)), cr = cl + nx * ny;
      if (!fl[cl] && !fl[cr]) continue;
      const ql = fl[cl] ? q[cl] : ghost(cr, cl), qr = fl[cr] ? q[cr] : ghost(cl, cr);
      this.w[f] -= (qr - ql) / dx; this.kw[f] = 1;
    }
    // Faces closed by the glass wall carry no flux, but they must not hold a zero velocity: particles sliding
    // along the wall would read it and be braked as by a no-slip wall one cell thick. They are filled by
    // extrapolation from the liquid (free slip); the particle collision removes the normal part. Two planes
    // are exact: v = 0 on the mirror plane y = 0 (odd in y), w = 0 on the flat bottom and the lid.
    for (let k = 0; k < nz; k++) for (let i = 0; i < nx; i++) { const f = V(i, 0, k); this.v[f] = 0; this.kv[f] = 1; }
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const f0 = Wd(i, j, 0), f1 = Wd(i, j, nz); this.w[f0] = 0; this.kw[f0] = 1; this.w[f1] = 0; this.kw[f1] = 1;
    }
  };

  // preconditioned conjugate gradient with MIC(0) (Bridson, Fluid Simulation for Computer Graphics, 2015)
  Fluid.prototype.pcg = function () {
    const nx = this.nx, ny = this.ny, nz = this.nz, nxy = nx * ny, nc = this.nc;
    const Ad = this.Ad, Ax = this.Ax, Ay = this.Ay, Az = this.Az, fl = this.fluid;
    const pc = this.mic, q = this.q, r = this.r_, z = this.z_, s = this.s_, b = this.rhs;
    const tau = 0.97, sigma = 0.25;
    pc.fill(0);
    for (let c = 0; c < nc; c++) {
      if (!fl[c]) continue;
      let e = Ad[c];
      const cx = c - 1, cy = c - nx, cz = c - nxy;
      const i = c % nx, j = Math.floor(c / nx) % ny, k = Math.floor(c / nxy);
      if (i > 0 && fl[cx]) e -= (Ax[cx] * pc[cx]) ** 2 + tau * Ax[cx] * (Ay[cx] + Az[cx]) * pc[cx] * pc[cx];
      if (j > 0 && fl[cy]) e -= (Ay[cy] * pc[cy]) ** 2 + tau * Ay[cy] * (Ax[cy] + Az[cy]) * pc[cy] * pc[cy];
      if (k > 0 && fl[cz]) e -= (Az[cz] * pc[cz]) ** 2 + tau * Az[cz] * (Ax[cz] + Ay[cz]) * pc[cz] * pc[cz];
      if (e < sigma * Ad[c]) e = Ad[c];
      pc[c] = e > 1e-30 ? 1 / Math.sqrt(e) : 0;
    }
    const applyA = (x, out) => {
      for (let c = 0; c < nc; c++) {
        if (!fl[c]) { out[c] = 0; continue; }
        let v = Ad[c] * x[c];
        const i = c % nx, j = Math.floor(c / nx) % ny, k = Math.floor(c / nxy);
        if (i + 1 < nx) v += Ax[c] * x[c + 1];
        if (i > 0) v += Ax[c - 1] * x[c - 1];
        if (j + 1 < ny) v += Ay[c] * x[c + nx];
        if (j > 0) v += Ay[c - nx] * x[c - nx];
        if (k + 1 < nz) v += Az[c] * x[c + nxy];
        if (k > 0) v += Az[c - nxy] * x[c - nxy];
        out[c] = v;
      }
    };
    const precond = (rr, out) => {
      const t = this.tmpPre || (this.tmpPre = new Float64Array(nc));
      for (let c = 0; c < nc; c++) {
        if (!fl[c]) { t[c] = 0; continue; }
        let v = rr[c];
        const i = c % nx, j = Math.floor(c / nx) % ny, k = Math.floor(c / nxy);
        if (i > 0) v -= Ax[c - 1] * pc[c - 1] * t[c - 1];
        if (j > 0) v -= Ay[c - nx] * pc[c - nx] * t[c - nx];
        if (k > 0) v -= Az[c - nxy] * pc[c - nxy] * t[c - nxy];
        t[c] = v * pc[c];
      }
      for (let c = nc - 1; c >= 0; c--) {
        if (!fl[c]) { out[c] = 0; continue; }
        let v = t[c];
        const i = c % nx, j = Math.floor(c / nx) % ny, k = Math.floor(c / nxy);
        if (i + 1 < nx) v -= Ax[c] * pc[c] * out[c + 1];
        if (j + 1 < ny) v -= Ay[c] * pc[c] * out[c + nx];
        if (k + 1 < nz) v -= Az[c] * pc[c] * out[c + nxy];
        out[c] = v * pc[c];
      }
    };
    q.fill(0); r.set(b);
    let rmax = 0; for (let c = 0; c < nc; c++) rmax = Math.max(rmax, Math.abs(r[c]));
    if (rmax < 1e-14) { this.cgIters = 0; return; }
    const tol = 1e-7 * rmax;
    precond(r, z); s.set(z);
    let sigmaR = 0; for (let c = 0; c < nc; c++) sigmaR += z[c] * r[c];
    let it = 0;
    for (; it < 300; it++) {
      applyA(s, z);
      let sz = 0; for (let c = 0; c < nc; c++) sz += s[c] * z[c];
      const alpha = sigmaR / sz;
      rmax = 0;
      for (let c = 0; c < nc; c++) { q[c] += alpha * s[c]; r[c] -= alpha * z[c]; if (Math.abs(r[c]) > rmax) rmax = Math.abs(r[c]); }
      if (rmax < tol) break;
      precond(r, z);
      let sn = 0; for (let c = 0; c < nc; c++) sn += z[c] * r[c];
      const beta = sn / sigmaR; sigmaR = sn;
      for (let c = 0; c < nc; c++) s[c] = z[c] + beta * s[c];
    }
    this.cgIters = it + 1; this.cgResidual = rmax;
  };

  // extend the liquid velocity into the air a few cells, so that surface particles find a velocity
  Fluid.prototype.extrapolate = function (layers) {
    const arr = [[this.u, this.ku, this.tmpU], [this.v, this.kv, this.tmpV], [this.w, this.kw, this.tmpW]];
    for (let comp = 0; comp < 3; comp++) {
      const [a, valid, t] = arr[comp];
      const [, sx, sy, sz] = this.comp(comp);
      const nv = new Uint8Array(valid.length);
      for (let L = 0; L < layers; L++) {
        nv.set(valid); t.set(a);
        for (let k = 0; k < sz; k++) for (let j = 0; j < sy; j++) for (let i = 0; i < sx; i++) {
          const n = i + sx * (j + sy * k);
          if (valid[n]) continue;
          let s = 0, m = 0;
          if (i > 0 && valid[n - 1]) { s += t[n - 1]; m++; }
          if (i < sx - 1 && valid[n + 1]) { s += t[n + 1]; m++; }
          if (j > 0 && valid[n - sx]) { s += t[n - sx]; m++; }
          if (j < sy - 1 && valid[n + sx]) { s += t[n + sx]; m++; }
          if (k > 0 && valid[n - sx * sy]) { s += t[n - sx * sy]; m++; }
          if (k < sz - 1 && valid[n + sx * sy]) { s += t[n + sx * sy]; m++; }
          if (m) { a[n] = s / m; nv[n] = 1; }
        }
        valid.set(nv);
      }
      for (let n = 0; n < a.length; n++) if (!valid[n]) a[n] = 0;
    }
  };

  Fluid.prototype.g2p = function () {
    const comps = [[this.u, this.pu], [this.v, this.pv], [this.w, this.pw]];
    for (let c = 0; c < 3; c++) {
      const [a, pvel] = comps[c], [cx, cy, cz] = this.pc[c];
      const [, sx, sy, sz, ox, oy, oz] = this.comp(c);
      for (let p = 0; p < this.np; p++) {
        const S = stencil(this, this.px[p], this.py[p], this.pz[p], sx, sy, sz, ox, oy, oz);
        let vn = 0, gx = 0, gy = 0, gz = 0;
        for (let n = 0; n < 8; n++) { const q = a[S.idx[n]]; vn += q * S.wt[n]; gx += q * S.gx[n]; gy += q * S.gy[n]; gz += q * S.gz[n]; }
        pvel[p] = vn; cx[p] = gx; cy[p] = gy; cz[p] = gz;
      }
    }
  };

  Fluid.prototype.advect = function (dt) {
    const R = this.R, e = 0.02 * this.dx, Rin = R - e;
    for (let p = 0; p < this.np; p++) {
      let x = this.px[p], y = this.py[p], z = this.pz[p];
      const u1 = this.sample(0, x, y, z), v1 = this.sample(1, x, y, z), w1 = this.sample(2, x, y, z);
      const xm = x + 0.5 * dt * u1, ym = Math.abs(y + 0.5 * dt * v1), zm = z + 0.5 * dt * w1;
      x += dt * this.sample(0, xm, ym, zm); y += dt * this.sample(1, xm, ym, zm); z += dt * this.sample(2, xm, ym, zm);
      if (y < 0) { y = -y; this.pv[p] = -this.pv[p]; }           // mirror plane
      this.px[p] = x; this.py[p] = y; this.pz[p] = z;
    }
    this.collide();
  };

  // the glass wall: a particle outside the wall is put back inside and loses its outward speed; likewise bottom and lid
  Fluid.prototype.collide = function () {
    const R = this.R, e = 0.02 * this.dx, Rin = R - e;
    for (let p = 0; p < this.np; p++) {
      let x = this.px[p], y = this.py[p], z = this.pz[p];
      const r2 = x * x + y * y;
      if (r2 > Rin * Rin) {
        const r = Math.sqrt(r2), nxr = x / r, nyr = y / r;
        x = nxr * Rin; y = nyr * Rin;
        const un = this.pu[p] * nxr + this.pv[p] * nyr;
        if (un > 0) { this.pu[p] -= un * nxr; this.pv[p] -= un * nyr; }
      }
      if (z < e) { z = e; if (this.pw[p] < 0) this.pw[p] = 0; }
      if (z > this.H - e) { z = this.H - e; if (this.pw[p] > 0) this.pw[p] = 0; }
      this.px[p] = x; this.py[p] = y; this.pz[p] = z;
    }
  };

  // Keep the particles evenly spaced: pairs closer than the seeding spacing d0 are pushed apart, each by a fraction
  // of the overlap, along the line between them. This moves no mass and adds no momentum (equal and opposite shifts);
  // without it APIC particles cluster and leave voids that the pressure solve reads as air below the surface.
  Fluid.prototype.relax = function (strength) {
    const dx = this.dx, nx = this.nx, ny = this.ny, nz = this.nz, d0 = this.dx / this.ppcSide, d02 = d0 * d0;
    const n = this.np, sx = this.relX || (this.relX = new Float64Array(n)), sy = this.relY || (this.relY = new Float64Array(n)), sz = this.relZ || (this.relZ = new Float64Array(n));
    sx.fill(0); sy.fill(0); sz.fill(0);
    this.levelSetBins();
    for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const c = i + nx * (j + ny * k);
      for (let a = this.cellStart[c]; a < this.cellStart[c + 1]; a++) {
        const p = this.sorted[a];
        for (let kk = k; kk <= Math.min(nz - 1, k + 1); kk++) for (let jj = Math.max(0, j - 1); jj <= Math.min(ny - 1, j + 1); jj++)
          for (let ii = Math.max(0, i - 1); ii <= Math.min(nx - 1, i + 1); ii++) {
            const c2 = ii + nx * (jj + ny * kk);
            if (c2 < c) continue;                       // each pair once
            for (let b = this.cellStart[c2]; b < this.cellStart[c2 + 1]; b++) {
              const q = this.sorted[b];
              if (c2 === c && q <= p) continue;
              const ex = this.px[q] - this.px[p], ey = this.py[q] - this.py[p], ez = this.pz[q] - this.pz[p];
              const d2 = ex * ex + ey * ey + ez * ez;
              if (d2 >= d02 || d2 < 1e-18) continue;
              const d = Math.sqrt(d2), m = 0.5 * strength * (d0 - d) / d;
              sx[p] -= m * ex; sy[p] -= m * ey; sz[p] -= m * ez; sx[q] += m * ex; sy[q] += m * ey; sz[q] += m * ez;
            }
          }
      }
    }
    for (let p = 0; p < n; p++) { this.px[p] += sx[p]; this.py[p] = Math.abs(this.py[p] + sy[p]); this.pz[p] += sz[p]; }
    this.collide();
  };

  // momentum of the whole liquid relative to the glass (both halves): x and z components, kg m/s
  Fluid.prototype.momentum = function () {
    let mx = 0, mz = 0;
    for (let p = 0; p < this.np; p++) { mx += this.pu[p]; mz += this.pw[p]; }
    return [2 * this.mp * mx, 2 * this.mp * mz];
  };

  Fluid.prototype.maxSpeed = function () {
    let m = 0;
    for (let p = 0; p < this.np; p++) { const s = this.pu[p] ** 2 + this.pv[p] ** 2 + this.pw[p] ** 2; if (s > m) m = s; }
    return Math.sqrt(m);
  };

  // one time step dt (s) with the glass's acceleration (ax, az) in m/s^2 held over the step
  Fluid.prototype.step = function (dt, ax, az) {
    this.levelSet();
    this.p2g();
    this.forces(dt, ax, az);
    this.project(dt);
    this.extrapolate(3);
    this.g2p();
    this.advect(dt);
    if (this.relaxStrength > 0) this.relax(this.relaxStrength);
    this.t += dt;
  };

  // height of the free surface above the glass bottom at (x, y), found along the vertical from phi
  Fluid.prototype.surfaceHeight = function (x, y) {
    y = Math.abs(y);
    const dx = this.dx, Rk = 2 * dx, R2 = Rk * Rk, r = this.rp;
    let zHi = this.H - 0.5 * dx, zLo = 0.5 * dx;
    let pHi = this.phiAt(x, y, zHi, Rk, R2, r);
    if (pHi < 0) return zHi;
    // march down in half cells to find the first sign change, then bisect
    let z = zHi, pz = pHi;
    for (; z > zLo; z -= 0.5 * dx) {
      const p = this.phiAt(x, y, z - 0.5 * dx, Rk, R2, r);
      if (p < 0) { zLo = z - 0.5 * dx; zHi = z; break; }
      pz = p;
    }
    if (z <= 0.5 * dx) return 0;
    for (let n = 0; n < 6; n++) {
      const zm = 0.5 * (zLo + zHi), p = this.phiAt(x, y, zm, Rk, R2, r);
      if (p < 0) zLo = zm; else zHi = zm;
    }
    return 0.5 * (zLo + zHi);
  };

  // Height of the liquid column over each grid column: the particles' volume standing on the column divided by
  // the column's open area (the wall cuts the edge columns). This is the depth-averaged free surface: it holds
  // the liquid's volume exactly and ignores drops thrown above the surface; it cannot show a breaking wave.
  // A 3 x 3 area-weighted average smooths it over about one cell. Returns a Float64Array nx * ny, metres.
  Fluid.prototype.columnHeights = function () {
    const nx = this.nx, ny = this.ny, dx = this.dx;
    const vol = this.colVol || (this.colVol = new Float64Array(nx * ny));
    const out = this.colH || (this.colH = new Float64Array(nx * ny));
    vol.fill(0);
    const Vp = this.Vseed;              // the volume each particle fills at its seeding spacing, (dx/s)^3
    const fold = (j) => (j < 0 ? -j - 1 : j >= ny ? ny - 1 : j);
    for (let p = 0; p < this.np; p++) {
      let i = Math.floor((this.px[p] - this.x0) / dx), j = Math.floor(this.py[p] / dx);
      i = i < 0 ? 0 : i >= nx ? nx - 1 : i; j = j < 0 ? 0 : j >= ny ? ny - 1 : j;
      vol[i + nx * j] += Vp;
    }
    const area = (i, j) => this.colArea[i + nx * j];
    if (!this.colArea) {
      this.colArea = new Float64Array(nx * ny);
      const S = 16;
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        let n = 0;
        for (let a = 0; a < S; a++) for (let b = 0; b < S; b++) {
          const x = this.x0 + (i + (a + 0.5) / S) * dx, y = (j + (b + 0.5) / S) * dx;
          if (x * x + y * y < this.R * this.R) n++;
        }
        this.colArea[i + nx * j] = n / (S * S) * dx * dx;
      }
    }
    // volume and open area are smoothed by the same 3 x 3 binomial filter (exact for a flat surface); the mirror
    // plane folds y < 0 back onto y > 0
    const blur = (src, dst) => {
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        let a = 0;
        for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) {
          const ii = i + di; if (ii < 0 || ii >= nx) continue;
          a += (di ? 0.25 : 0.5) * (dj ? 0.25 : 0.5) * src[ii + nx * fold(j + dj)];
        }
        dst[i + nx * j] = a;
      }
    };
    const t1 = this.colT1 || (this.colT1 = new Float64Array(nx * ny));
    const A1 = this.colA1 || (this.colA1 = (() => { const q = new Float64Array(nx * ny); blur(this.colArea, q); return q; })());
    blur(vol, t1);
    for (let n = 0; n < nx * ny; n++) out[n] = A1[n] > 0.02 * dx * dx ? t1[n] / A1[n] : 0;
    void area;
    return out;
  };

  // the column height at (x, y), bilinear between column centres (y folded by the mirror plane)
  Fluid.prototype.columnHeightAt = function (x, y) {
    const nx = this.nx, ny = this.ny, dx = this.dx, H = this.colH;
    y = Math.abs(y);
    // columns near the wall are cut by it and hold too few particles to count: beyond r1 = R - 2.5 dx the height
    // is extended linearly along the radius from the values at r1 and r1 - 1.5 dx
    const r = Math.hypot(x, y), r1 = this.R - 2.5 * dx, r2 = r1 - 1.5 * dx;
    if (r > r1) {
      const cx = x / r, cy = y / r, h1 = this.colBilinear(cx * r1, cy * r1), h2 = this.colBilinear(cx * r2, cy * r2);
      return h1 + (r - r1) * (h1 - h2) / (r1 - r2);
    }
    return this.colBilinear(x, y);
  };
  Fluid.prototype.colBilinear = function (x, y) {
    const nx = this.nx, ny = this.ny, dx = this.dx, H = this.colH;
    const fx = (x - this.x0) / dx - 0.5, fy = y / dx - 0.5;
    let i = Math.floor(fx), j = Math.floor(fy); const tx = fx - i, ty = fy - j;
    const at = (a, b) => {
      a = a < 0 ? 0 : a >= nx ? nx - 1 : a; b = b < 0 ? -b - 1 : b; b = b >= ny ? ny - 1 : b;
      return H[a + nx * b];
    };
    return (1 - tx) * (1 - ty) * at(i, j) + tx * (1 - ty) * at(i + 1, j) + (1 - tx) * ty * at(i, j + 1) + tx * ty * at(i + 1, j + 1);
  };

  /* ------------------------------------------------------------------- road */
  function Road(o) {
    o = o || {};
    this.bumps = o.bumps || [{ x: 1.0, h: 0.02, L: 0.25 }];   // cosine bumps: centre, height, length (m)
    this.Rw = o.Rw || 0.05;
    this.xmin = o.xmin != null ? o.xmin : -1; this.xmax = o.xmax != null ? o.xmax : 8; this.h = 0.0005;
    this.build();
  }
  Road.prototype.zr = function (x) {
    let z = 0;
    for (const b of this.bumps) {
      const s = (x - b.x) / b.L;
      if (s > -0.5 && s < 0.5) z += 0.5 * b.h * (1 + Math.cos(2 * Math.PI * s));
    }
    return z;
  };
  // the axle path of a rigid wheel of radius Rw rolling over z_r: z_a(x) = max_s [z_r(s) + sqrt(Rw^2 - (s-x)^2)]
  Road.prototype.build = function () {   // z_a is the axle height of an undeformed wheel
    const n = Math.round((this.xmax - this.xmin) / this.h) + 1, Rw = this.Rw, h = this.h;
    const zr = new Float64Array(n);
    for (let i = 0; i < n; i++) zr[i] = this.zr(this.xmin + i * h);
    const za = new Float64Array(n), m = Math.ceil(Rw / h);
    for (let i = 0; i < n; i++) {
      let best = -1e9;
      for (let d = -m; d <= m; d++) {
        const j = i + d; if (j < 0 || j >= n) continue;
        const s = d * h; if (Math.abs(s) > Rw) continue;
        const v = zr[j] + Math.sqrt(Rw * Rw - s * s);
        if (v > best) best = v;
      }
      za[i] = best;
    }
    this.za = za; this.n = n;
  };
  Road.prototype.axle = function (x) {               // [z_a, dz_a/dx]
    const f = (x - this.xmin) / this.h;
    let i = Math.floor(f); if (i < 0) i = 0; if (i > this.n - 2) i = this.n - 2;
    const t = f - i, a = this.za[i], b = this.za[i + 1];
    return [a + t * (b - a), (b - a) / this.h];
  };

  /* ------------------------------------------------------------------- cart */
  function Cart(o) {
    o = o || {};
    this.Mb = o.Mb || 1.5;       // body and glass, without the stout, kg
    this.mw = o.mw || 0.3;       // wheel, kg
    this.Rw = o.Rw || 0.05;      // wheel radius, m
    this.Iw = o.Iw || 0.5 * this.mw * this.Rw * this.Rw;   // wheel moment of inertia (a disc), kg m^2
    this.k = o.k || 600;         // suspension spring, N/m
    this.c = o.c || 8;           // suspension damper, N s/m
    this.kt = o.kt || 2.0e4;     // radial tyre stiffness, N/m
    this.ct = o.ct || 5;         // tyre damping, N s/m
    this.cx = o.cx || 2;         // rolling and air drag, N s/m
    this.v0 = o.v0 != null ? o.v0 : 1.0;  // cruising speed the drive force is set for, m/s
    this.ml = o.ml || 0;         // liquid mass, kg (set by the coupling)
    this.Ls = o.Ls || 0.08;      // unloaded spring length (body above axle), m
    this.g = 9.81;
    this.road = o.road || new Road({ Rw: this.Rw });
    this.pushF = 0;              // the reader's push, N (horizontal)
    this.reset(o.x0 != null ? o.x0 : 0);
  }
  Cart.prototype.reset = function (x) {
    const g = this.g, Ms = this.Mb + this.ml, za = this.road.axle(x)[0];
    this.x = x; this.vx = this.v0;
    this.zw = za - (Ms + this.mw) * g / this.kt;                 // static tyre deflection
    this.zb = this.zw + this.Ls - Ms * g / this.k;               // static spring deflection
    this.vzb = 0; this.vzw = 0;
    this.N = (Ms + this.mw) * g; this.ax = 0; this.azb = 0; this.t = 0;
  };
  // one step h with the liquid's reaction (Fx, Fz) on the glass (the part beyond rigid co-motion)
  Cart.prototype.step = function (h, Fx, Fz) {
    const g = this.g, Ms = this.Mb + this.ml;
    const [za, dza] = this.road.axle(this.x);
    const vza = dza * this.vx;
    let N = this.kt * (za - this.zw) + this.ct * (vza - this.vzw);
    if (N < 0) N = 0;                                            // the tyre cannot pull on the road
    const Fs = -this.k * (this.zb - this.zw - this.Ls) - this.c * (this.vzb - this.vzw);  // on the body
    const Mx = Ms + this.mw + this.Iw / (this.Rw * this.Rw);
    const Fdrive = this.cx * this.v0;
    const ax = (-N * dza + Fdrive - this.cx * this.vx + this.pushF + Fx) / Mx;
    const azb = (Fs - Ms * g + Fz) / Ms;
    const azw = (-Fs - this.mw * g + N) / this.mw;
    this.vx += h * ax; this.vzb += h * azb; this.vzw += h * azw;      // symplectic Euler
    this.x += h * this.vx; this.zb += h * this.vzb; this.zw += h * this.vzw;
    this.N = N; this.ax = ax; this.azb = azb; this.t += h;
  };

  /* --------------------------------------------------------------- coupling */
  function World(o) {
    o = o || {};
    this.fluid = new Fluid(o.fluid);
    const co = Object.assign({}, o.cart || {});
    co.ml = this.fluid.mLiquid;
    if (o.road) co.road = new Road(o.road);
    this.cart = new Cart(co);
    this.dtMax = o.dtMax || 1 / 400;
    this.hCart = o.hCart || 1e-4;
    this.Fx = 0; this.Fz = 0;
    this.P = this.fluid.momentum();
    this.t = 0; this.lastAx = 0; this.lastAz = 0;
    this.fluid.levelSet();          // so that the surface can be read before the first step
  }
  // advance by dt (s), in fluid steps no longer than dtMax and a CFL limit of one cell
  World.prototype.advance = function (dt) {
    let left = dt;
    while (left > 1e-12) {
      const umax = this.fluid.maxSpeed();
      let h = Math.min(this.dtMax, left, umax > 0 ? 0.8 * this.fluid.dx / umax : this.dtMax);
      const c = this.cart, vx0 = c.vx, vz0 = c.vzb;
      const n = Math.max(1, Math.round(h / this.hCart)), hc = h / n;
      for (let i = 0; i < n; i++) c.step(hc, this.Fx, this.Fz);
      const ax = (c.vx - vx0) / h, az = (c.vzb - vz0) / h;     // the glass's mean acceleration over the step
      this.fluid.step(h, ax, az);
      const P = this.fluid.momentum();
      // reaction of the liquid on the glass beyond rigid co-motion: -dP_rel/dt
      this.Fx = -(P[0] - this.P[0]) / h; this.Fz = -(P[1] - this.P[1]) / h;
      this.P = P; this.lastAx = ax; this.lastAz = az;
      left -= h; this.t += h;
    }
  };

  return { Fluid, Road, Cart, World };
});
