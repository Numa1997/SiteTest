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
    // The glass: an inner radius R(z) above the cavity floor. With o.profile ({dz, R: [...]}, metres) it is the measured
    // tulip (scripts/guinness-glass.js), open above its rim z_rim; without, a straight cylinder of radius o.R closed by a lid
    // at the box top (the checks against the cylinder's exact sloshing frequency use that).
    this.profile = o.profile || null;
    if (this.profile) {
      const P = this.profile.R;
      this.zRim = (P.length - 1) * this.profile.dz;
      this.R = Math.max.apply(null, P);
      this.Rrim = P[P.length - 1];
    } else { this.R = o.R || 0.04; this.zRim = Infinity; this.Rrim = this.R; }
    this.h0 = o.h0 || 0.06;         // depth of stout at rest, m
    this.dx = o.dx || 0.004;        // grid cell, m
    this.rho = o.rho || 1000;       // density, kg/m^3
    this.nu = o.nu != null ? o.nu : 1.0e-6;   // kinematic viscosity, m^2/s (taken as water)
    this.g = o.g || 9.81;
    const dx = this.dx;
    this.nx = 2 * Math.ceil(this.R / dx);
    this.ny = Math.ceil(this.R / dx);
    this.nz = Math.ceil((o.H || 0.092) / dx);
    this.H = this.nz * dx;          // the box top: for the tulip 3 cm or so above the rim, for the cylinder a lid
    this.x0 = -(this.nx / 2) * dx;
    this.Rbox = (this.nx / 2) * dx;
    const nx = this.nx, ny = this.ny, nz = this.nz;
    this.nc = nx * ny * nz;
    this.nu_ = (nx + 1) * ny * nz; this.nv_ = nx * (ny + 1) * nz; this.nw_ = nx * ny * (nz + 1);
    const F = Float64Array;
    // o.shared: the arrays the worker threads read or write live in shared memory (scripts/stout-pool.js); same numbers
    this.shared = !!o.shared;
    this.u = this.mk(F, this.nu_); this.v = this.mk(F, this.nv_); this.w = this.mk(F, this.nw_);
    this.uo = new F(this.nu_); this.vo = new F(this.nv_); this.wo = new F(this.nw_);
    this.mu = this.mk(F, this.nu_); this.mv = this.mk(F, this.nv_); this.mw = this.mk(F, this.nw_);   // P2G weights
    this.au = new F(this.nu_); this.av = new F(this.nv_); this.aw = new F(this.nw_);   // open face fractions
    this.ku = new Uint8Array(this.nu_); this.kv = new Uint8Array(this.nv_); this.kw = new Uint8Array(this.nw_); // valid
    this.tmpU = new F(this.nu_); this.tmpV = new F(this.nv_); this.tmpW = new F(this.nw_);
    this.cnt = new Int32Array(this.nc);       // particles per cell
    this.fluid = new Uint8Array(this.nc);
    this.phi = this.mk(F, this.nc);
    this.q = new F(this.nc); this.rhs = new F(this.nc);
    this.Ad = new F(this.nc); this.Ax = new F(this.nc); this.Ay = new F(this.nc); this.Az = new F(this.nc);
    this.mic = new F(this.nc); this.r_ = new F(this.nc); this.z_ = new F(this.nc); this.s_ = new F(this.nc);
    this.sliver = o.sliver != null ? o.sliver : 0.1;
    this.faceFractions();
    this.ppcSide = o.ppcSide || 2;
    this.wallImages = o.wallImages != null ? o.wallImages : true;
    this.rpFactor = o.rpFactor || 1.8;     // particle radius of the level set, in particle spacings (see Fluid.seed)
    this.forcedPhi = o.forcedPhi != null ? o.forcedPhi : 0.05;
    this.thetaMin = o.thetaMin || 0.05;
    this.wallPhi = o.wallPhi || 'inherit';
    this.forceCells = o.forceCells != null ? o.forceCells : true;
    this.kernel = o.kernel || 2;          // radius of the particle kernel of the level set, in cells
    this.relaxStrength = o.relax != null ? o.relax : 0;   // off: not needed at dt = 1/400 s (measured)
    this.volumeCorrection = o.volumeCorrection != null ? o.volumeCorrection : 0;   // gamma, a fraction of the excess per step (off: not needed with rp = 1.8 spacings, measured)
    this.n0 = this.ppcSide * this.ppcSide * this.ppcSide;
    this.seed(this.ppcSide, o.seed || 12345);
    this.t = 0;
    this.cgIters = 0;
  }

  // inner radius of the glass at height z (m); above the rim there is no wall (the box edge stands in, unused)
  Fluid.prototype.Rz = function (z) {
    if (!this.profile) return this.R;
    if (z > this.zRim) return 10;
    const P = this.profile.R, f = (z < 0 ? 0 : z) / this.profile.dz, i = Math.floor(f);
    if (i >= P.length - 1) return P[P.length - 1];
    return P[i] + (f - i) * (P[i + 1] - P[i]);
  };
  // slope dR/dz of the wall
  Fluid.prototype.dRz = function (z) {
    if (!this.profile || z >= this.zRim) return 0;
    const P = this.profile.R, f = (z < 0 ? 0 : z) / this.profile.dz, i = Math.min(P.length - 2, Math.floor(f));
    return (P[i + 1] - P[i]) / this.profile.dz;
  };
  // volume of liquid that fills the glass to height h: integral of pi R(z)^2 dz (trapezoid on 0.05 mm)
  Fluid.prototype.volumeTo = function (h) {
    const n = Math.max(1, Math.round(h / 5e-5)), d = h / n; let v = 0;
    for (let k = 0; k <= n; k++) { const r = this.Rz(k * d); v += (k === 0 || k === n ? 0.5 : 1) * Math.PI * r * r * d; }
    return v;
  };

  Fluid.prototype.faceFractions = function () {
    const dx = this.dx, nx = this.nx, ny = this.ny, nz = this.nz, x0 = this.x0;
    // open fraction of each face, with the wall radius at the face's height; slivers under 10 % are closed (moves the
    // wall by < 0.1 dx, keeps the solve well posed)
    const sl = this.sliver, clamp = (a) => { a = Math.max(0, Math.min(1, a)); return a < sl ? 0 : a; };
    for (let k = 0; k < nz; k++) {
      const R = Math.min(this.Rz((k + 0.5) * dx), this.Rbox * 2);
      for (let j = 0; j < ny; j++) for (let i = 0; i <= nx; i++) {
        const xf = x0 + i * dx, Y = R * R - xf * xf > 0 ? Math.sqrt(R * R - xf * xf) : 0;
        this.au[i + (nx + 1) * (j + ny * k)] = (i === 0 || i === nx) ? 0 : clamp((Y - j * dx) / dx);
      }
      for (let j = 0; j <= ny; j++) for (let i = 0; i < nx; i++) {
        const yf = j * dx, X = R * R - yf * yf > 0 ? Math.sqrt(R * R - yf * yf) : 0;
        const a = x0 + i * dx, b = a + dx;
        const len = Math.max(0, Math.min(b, X) - Math.max(a, -X));
        this.av[i + nx * (j + (ny + 1) * k)] = (j === 0 || j === ny) ? 0 : clamp(len / dx);   // y = 0 is the mirror plane: v = 0
      }
    }
    const S = 10;
    for (let k = 0; k <= nz; k++) {
      const R = Math.min(this.Rz(k * dx), this.Rbox * 2);
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        let inside = 0;
        for (let a = 0; a < S; a++) for (let b = 0; b < S; b++) {
          const x = x0 + (i + (a + 0.5) / S) * dx, y = (j + (b + 0.5) / S) * dx;
          if (x * x + y * y < R * R) inside++;
        }
        let f = inside / (S * S); if (f < this.sliver) f = 0;
        this.aw[i + nx * (j + ny * k)] = (k === 0 || k === nz) ? 0 : f;
      }
    }
  };

  // a typed array, in shared memory when the fluid is shared with worker threads
  Fluid.prototype.mk = function (T, n) {
    return this.shared ? new T(new SharedArrayBuffer(Math.max(1, n) * T.BYTES_PER_ELEMENT)) : new T(n);
  };
  Fluid.prototype.seed = function (s, seed) {
    let st = seed >>> 0;
    const rnd = () => { st = (st * 1664525 + 1013904223) >>> 0; return st / 4294967296; };
    const dx = this.dx, xs = [], ys = [], zs = [];
    for (let k = 0; k < this.nz; k++) for (let j = 0; j < this.ny; j++) for (let i = 0; i < this.nx; i++)
      for (let a = 0; a < s; a++) for (let b = 0; b < s; b++) for (let c = 0; c < s; c++) {
        const x = this.x0 + (i + (a + 0.5 + 0.6 * (rnd() - 0.5)) / s) * dx;
        const y = (j + (b + 0.5 + 0.6 * (rnd() - 0.5)) / s) * dx;
        const z = (k + (c + 0.5 + 0.6 * (rnd() - 0.5)) / s) * dx;
        if (x * x + y * y < (this.Rz(z) - 0.15 * dx) ** 2 && z < this.h0 && y > 0) { xs.push(x); ys.push(y); zs.push(z); }
      }
    const n = this.np = xs.length;
    const F = Float64Array;
    this.px = this.mk(F, n); this.py = this.mk(F, n); this.pz = this.mk(F, n); this.px.set(xs); this.py.set(ys); this.pz.set(zs);
    this.pu = this.mk(F, n); this.pv = this.mk(F, n); this.pw = this.mk(F, n);
    // APIC: each particle also carries the local velocity gradient, one row per component (Jiang et al. 2015)
    this.pc = [0, 1, 2].map(() => [this.mk(F, n), this.mk(F, n), this.mk(F, n)]);
    // the half glass holds half the liquid: m_l/2 = rho V(h0) / 2, V(h) the integral of pi R(z)^2, shared equally by the
    // particles; a spilled particle takes its m_p with it
    this.mLiquid = this.rho * this.volumeTo(this.h0);
    this.npStart = n; this.spilled = 0;
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

  // trilinear value of component c at (x, y, z); flat code, no allocation (the hot path of advection)
  Fluid.prototype.sample = function (c, x, y, z) {
    const dx = this.dx, nx = this.nx, ny = this.ny, nz = this.nz;
    let a, sx, sy, sz, fx = (x - this.x0) / dx, fy = y / dx, fz = z / dx;
    if (c === 0) { a = this.u; sx = nx + 1; sy = ny; sz = nz; fy -= 0.5; fz -= 0.5; }
    else if (c === 1) { a = this.v; sx = nx; sy = ny + 1; sz = nz; fx -= 0.5; fz -= 0.5; }
    else { a = this.w; sx = nx; sy = ny; sz = nz + 1; fx -= 0.5; fy -= 0.5; }
    const i = Math.floor(fx), j = Math.floor(fy), k = Math.floor(fz), tx = fx - i, ty = fy - j, tz = fz - k;
    const i0 = i < 0 ? 0 : i >= sx ? sx - 1 : i, i1 = i + 1 < 0 ? 0 : i + 1 >= sx ? sx - 1 : i + 1;
    const j0 = j < 0 ? 0 : j >= sy ? sy - 1 : j, j1 = j + 1 < 0 ? 0 : j + 1 >= sy ? sy - 1 : j + 1;
    const k0 = k < 0 ? 0 : k >= sz ? sz - 1 : k, k1 = k + 1 < 0 ? 0 : k + 1 >= sz ? sz - 1 : k + 1;
    const sxy = sx * sy, b00 = j0 * sx + k0 * sxy, b10 = j1 * sx + k0 * sxy, b01 = j0 * sx + k1 * sxy, b11 = j1 * sx + k1 * sxy;
    const c00 = a[i0 + b00] + tx * (a[i1 + b00] - a[i0 + b00]), c10 = a[i0 + b10] + tx * (a[i1 + b10] - a[i0 + b10]);
    const c01 = a[i0 + b01] + tx * (a[i1 + b01] - a[i0 + b01]), c11 = a[i0 + b11] + tx * (a[i1 + b11] - a[i0 + b11]);
    const d0 = c00 + ty * (c10 - c00), d1 = c01 + ty * (c11 - c01);
    return d0 + tz * (d1 - d0);
  };

  // APIC transfer kernels for one staggered component, flat code. For each particle: base node (i, j, k), fractions
  // (tx, ty, tz); node offsets from the particle are ((a - tx) dx, (b - ty) dx, (c - tz) dx), a, b, c in {0, 1}.
  Fluid.prototype.transfer = function (comp, toGrid, p0, p1) {
    const dx = this.dx, nx = this.nx, ny = this.ny, nz = this.nz, inv = 1 / dx, pa = p0 || 0, np = p1 != null ? p1 : this.np;
    let a, m, pvel, sx, sy, sz, ox = 0, oy = 0, oz = 0;
    if (comp === 0) { a = this.u; m = this.mu; pvel = this.pu; sx = nx + 1; sy = ny; sz = nz; oy = 0.5; oz = 0.5; }
    else if (comp === 1) { a = this.v; m = this.mv; pvel = this.pv; sx = nx; sy = ny + 1; sz = nz; ox = 0.5; oz = 0.5; }
    else { a = this.w; m = this.mw; pvel = this.pw; sx = nx; sy = ny; sz = nz + 1; ox = 0.5; oy = 0.5; }
    const [cx, cy, cz] = this.pc[comp], sxy = sx * sy, px = this.px, py = this.py, pz = this.pz, x0 = this.x0;
    if (toGrid) { a.fill(0); m.fill(0); }
    for (let p = pa; p < np; p++) {
      const fx = (px[p] - x0) * inv - ox, fy = py[p] * inv - oy, fz = pz[p] * inv - oz;
      const i = Math.floor(fx), j = Math.floor(fy), k = Math.floor(fz), tx = fx - i, ty = fy - j, tz = fz - k;
      const I0 = i < 0 ? 0 : i >= sx ? sx - 1 : i, I1 = i + 1 < 0 ? 0 : i + 1 >= sx ? sx - 1 : i + 1;
      const J0 = j < 0 ? 0 : j >= sy ? sy - 1 : j, J1 = j + 1 < 0 ? 0 : j + 1 >= sy ? sy - 1 : j + 1;
      const K0 = k < 0 ? 0 : k >= sz ? sz - 1 : k, K1 = k + 1 < 0 ? 0 : k + 1 >= sz ? sz - 1 : k + 1;
      const n000 = I0 + J0 * sx + K0 * sxy, n100 = I1 + J0 * sx + K0 * sxy, n010 = I0 + J1 * sx + K0 * sxy, n110 = I1 + J1 * sx + K0 * sxy;
      const n001 = I0 + J0 * sx + K1 * sxy, n101 = I1 + J0 * sx + K1 * sxy, n011 = I0 + J1 * sx + K1 * sxy, n111 = I1 + J1 * sx + K1 * sxy;
      const ux = 1 - tx, uy = 1 - ty, uz = 1 - tz;
      const w000 = ux * uy * uz, w100 = tx * uy * uz, w010 = ux * ty * uz, w110 = tx * ty * uz;
      const w001 = ux * uy * tz, w101 = tx * uy * tz, w011 = ux * ty * tz, w111 = tx * ty * tz;
      if (toGrid) {
        const u0 = pvel[p], gx = cx[p] * dx, gy = cy[p] * dx, gz = cz[p] * dx;
        const ax0 = -tx * gx, ax1 = (1 - tx) * gx, ay0 = -ty * gy, ay1 = (1 - ty) * gy, az0 = -tz * gz, az1 = (1 - tz) * gz;
        a[n000] += w000 * (u0 + ax0 + ay0 + az0); m[n000] += w000;
        a[n100] += w100 * (u0 + ax1 + ay0 + az0); m[n100] += w100;
        a[n010] += w010 * (u0 + ax0 + ay1 + az0); m[n010] += w010;
        a[n110] += w110 * (u0 + ax1 + ay1 + az0); m[n110] += w110;
        a[n001] += w001 * (u0 + ax0 + ay0 + az1); m[n001] += w001;
        a[n101] += w101 * (u0 + ax1 + ay0 + az1); m[n101] += w101;
        a[n011] += w011 * (u0 + ax0 + ay1 + az1); m[n011] += w011;
        a[n111] += w111 * (u0 + ax1 + ay1 + az1); m[n111] += w111;
      } else {
        const q000 = a[n000], q100 = a[n100], q010 = a[n010], q110 = a[n110], q001 = a[n001], q101 = a[n101], q011 = a[n011], q111 = a[n111];
        pvel[p] = w000 * q000 + w100 * q100 + w010 * q010 + w110 * q110 + w001 * q001 + w101 * q101 + w011 * q011 + w111 * q111;
        // the velocity gradient at the particle: derivatives of the trilinear weights
        cx[p] = inv * (uy * uz * (q100 - q000) + ty * uz * (q110 - q010) + uy * tz * (q101 - q001) + ty * tz * (q111 - q011));
        cy[p] = inv * (ux * uz * (q010 - q000) + tx * uz * (q110 - q100) + ux * tz * (q011 - q001) + tx * tz * (q111 - q101));
        cz[p] = inv * (ux * uy * (q001 - q000) + tx * uy * (q101 - q100) + ux * ty * (q011 - q010) + tx * ty * (q111 - q110));
      }
    }
    if (toGrid) for (let n = 0; n < a.length; n++) a[n] = m[n] > 1e-9 ? a[n] / m[n] : 0;
  };
  Fluid.prototype.p2g = function () {
    if (!this.pool) { for (let c = 0; c < 3; c++) this.transfer(c, true); return; }
    // threads: each owns a slab of grid layers and adds into it every particle that reaches it, in particle order, so
    // that every grid value receives the same terms in the same order as above
    this.u.fill(0); this.mu.fill(0); this.v.fill(0); this.mv.fill(0); this.w.fill(0); this.mw.fill(0);
    this.pool.slabs(this);
    this.pool.run(3, this.np, 0, 0);
    for (const [a, m] of [[this.u, this.mu], [this.v, this.mv], [this.w, this.mw]]) for (let n = 0; n < a.length; n++) a[n] = m[n] > 1e-9 ? a[n] / m[n] : 0;
  };
  Fluid.prototype.g2p = function () {
    if (this.pool) { this.pool.run(2, this.np, 0, 0); return; }
    for (let c = 0; c < 3; c++) this.transfer(c, false);
  };
  // particle-to-grid for the grid layers k0 <= k < k1 of all three components (one thread's slab): Fluid.transfer's terms,
  // in its order, for the nodes in the slab only
  Fluid.prototype.p2gSlab = function (k0, k1) {
    const dx = this.dx, nx = this.nx, ny = this.ny, nz = this.nz, np = this.np, inv = 1 / dx;
    const px = this.px, py = this.py, pz = this.pz, x0 = this.x0;
    for (let comp = 0; comp < 3; comp++) {
      let a, m, pvel, sx, sy, sz, ox = 0, oy = 0, oz = 0;
      if (comp === 0) { a = this.u; m = this.mu; pvel = this.pu; sx = nx + 1; sy = ny; sz = nz; oy = 0.5; oz = 0.5; }
      else if (comp === 1) { a = this.v; m = this.mv; pvel = this.pv; sx = nx; sy = ny + 1; sz = nz; ox = 0.5; oz = 0.5; }
      else { a = this.w; m = this.mw; pvel = this.pw; sx = nx; sy = ny; sz = nz + 1; ox = 0.5; oy = 0.5; }
      const [cx, cy, cz] = this.pc[comp], sxy = sx * sy;
      for (let p = 0; p < np; p++) {
        const fz = pz[p] * inv - oz, k = Math.floor(fz);
        const K0 = k < 0 ? 0 : k >= sz ? sz - 1 : k, K1 = k + 1 < 0 ? 0 : k + 1 >= sz ? sz - 1 : k + 1;
        const in0 = K0 >= k0 && K0 < k1, in1 = K1 >= k0 && K1 < k1;
        if (!in0 && !in1) continue;
        const fx = (px[p] - x0) * inv - ox, fy = py[p] * inv - oy;
        const i = Math.floor(fx), j = Math.floor(fy), tx = fx - i, ty = fy - j, tz = fz - k;
        const I0 = i < 0 ? 0 : i >= sx ? sx - 1 : i, I1 = i + 1 < 0 ? 0 : i + 1 >= sx ? sx - 1 : i + 1;
        const J0 = j < 0 ? 0 : j >= sy ? sy - 1 : j, J1 = j + 1 < 0 ? 0 : j + 1 >= sy ? sy - 1 : j + 1;
        const ux = 1 - tx, uy = 1 - ty, uz = 1 - tz;
        const u0 = pvel[p], gx = cx[p] * dx, gy = cy[p] * dx, gz = cz[p] * dx;
        const ax0 = -tx * gx, ax1 = (1 - tx) * gx, ay0 = -ty * gy, ay1 = (1 - ty) * gy, az0 = -tz * gz, az1 = (1 - tz) * gz;
        if (in0) {
          const n000 = I0 + J0 * sx + K0 * sxy, n100 = I1 + J0 * sx + K0 * sxy, n010 = I0 + J1 * sx + K0 * sxy, n110 = I1 + J1 * sx + K0 * sxy;
          const w000 = ux * uy * uz, w100 = tx * uy * uz, w010 = ux * ty * uz, w110 = tx * ty * uz;
          a[n000] += w000 * (u0 + ax0 + ay0 + az0); m[n000] += w000;
          a[n100] += w100 * (u0 + ax1 + ay0 + az0); m[n100] += w100;
          a[n010] += w010 * (u0 + ax0 + ay1 + az0); m[n010] += w010;
          a[n110] += w110 * (u0 + ax1 + ay1 + az0); m[n110] += w110;
        }
        if (in1) {
          const n001 = I0 + J0 * sx + K1 * sxy, n101 = I1 + J0 * sx + K1 * sxy, n011 = I0 + J1 * sx + K1 * sxy, n111 = I1 + J1 * sx + K1 * sxy;
          const w001 = ux * uy * tz, w101 = tx * uy * tz, w011 = ux * ty * tz, w111 = tx * ty * tz;
          a[n001] += w001 * (u0 + ax0 + ay0 + az1); m[n001] += w001;
          a[n101] += w101 * (u0 + ax1 + ay0 + az1); m[n101] += w101;
          a[n011] += w011 * (u0 + ax0 + ay1 + az1); m[n011] += w011;
          a[n111] += w111 * (u0 + ax1 + ay1 + az1); m[n111] += w111;
        }
      }
    }
  };

  // particles sorted by cell (cellStart, sorted) and counted per cell (cnt)
  Fluid.prototype.levelSetBins = function () {
    const nx = this.nx, ny = this.ny, nz = this.nz, dx = this.dx, nc = this.nc;
    const cnt = this.cnt; cnt.fill(0);
    if (!this.cellStart || this.cellStart.length !== nc + 1) { this.cellStart = this.mk(Int32Array, nc + 1); }
    if (!this.sorted || this.sorted.length < this.np) this.sorted = this.mk(Int32Array, this.np);
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
    const Rk = this.kernel * dx, R2 = Rk * Rk, r = this.rp;
    // the level set is measured only within two cells of an empty cell inside the glass; deeper cells are liquid
    const empty = this.emptyMask || (this.emptyMask = new Uint8Array(nc));
    for (let k = 0; k < nz; k++) {
      const Rc = Math.min(this.Rz((k + 0.5) * dx), this.Rbox) - 0.5 * dx;
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        const c = i + nx * (j + ny * k), xc = this.x0 + (i + 0.5) * dx, yc = (j + 0.5) * dx;
        empty[c] = cnt[c] === 0 && xc * xc + yc * yc < Rc * Rc ? 1 : 0;
      }
    }
    // "near": within two cells (in each index) of an empty cell, found by dilating the empty mask by 2 along x, then y,
    // then z (the same set as testing the 5 x 5 x 5 block around each cell, at 15 reads per cell instead of 125)
    const nearA = this.nearA || (this.nearA = new Uint8Array(nc)), nearB = this.nearB || (this.nearB = new Uint8Array(nc));
    const dilate = (src, dst, axis) => {
      const st = axis === 0 ? 1 : axis === 1 ? nx : nx * ny, n = axis === 0 ? nx : axis === 1 ? ny : nz;
      for (let k = 0, c = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++, c++) {
        const a = axis === 0 ? i : axis === 1 ? j : k, lo = a < 2 ? -a : -2, hi = a + 2 >= n ? n - 1 - a : 2;
        let v = 0;
        for (let d = lo; d <= hi; d++) if (src[c + d * st]) { v = 1; break; }
        dst[c] = v;
      }
    };
    dilate(empty, nearA, 0); dilate(nearA, nearB, 1); dilate(nearB, nearA, 2);
    // a cell with no particle anywhere in its 5 x 5 x 5 block reads phi = 3 dx without a search (no particle, no image
    // in reach): the air above the liquid, most of the near cells
    const occ = this.occA || (this.occA = new Uint8Array(nc)), occB = this.occB || (this.occB = new Uint8Array(nc));
    for (let c = 0; c < nc; c++) occ[c] = cnt[c] > 0 ? 1 : 0;
    dilate(occ, occB, 0); dilate(occB, occ, 1); dilate(occ, occB, 2);
    const fast = this.kernel === 2, pool = fast && this.pool;
    if (fast) this.levelSetParticles(Rk);
    const list = pool ? pool.cells : null; let nl = 0;
    for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const c = i + nx * (j + ny * k);
      if (!nearA[c]) { this.phi[c] = cnt[c] > 0 ? -2 * dx : 2 * dx; continue; }
      if (!fast) { this.phi[c] = this.phiAt(this.x0 + (i + 0.5) * dx, (j + 0.5) * dx, (k + 0.5) * dx, Rk, R2, r); continue; }
      if (!occB[c]) this.phi[c] = 3 * dx;
      else if (pool) list[nl++] = c;               // searched below, by the threads
      else this.phi[c] = this.phiCell(i, j, k, R2, r);
    }
    if (pool) pool.run(1, nl, R2, r);
    // Liquid cells: inside the level set, or holding particles (so that no particle is left without pressure). A cell
    // that holds particles but reads phi >= 0 gets phi = -0.05 dx. Measured: -0.5 dx here broke the slosh (4.3 Hz
    // instead of 3.5 Hz on the 4 mm grid); the spurious flow at rest that first suggested it came from the time
    // step (clean at dt = 1/400 s), not from this.
    for (let c = 0; c < nc; c++) {
      if (this.forceCells) {
        this.fluid[c] = this.phi[c] < 0 || cnt[c] > 0 ? 1 : 0;
        if (cnt[c] > 0 && this.phi[c] >= 0) this.phi[c] = -this.forcedPhi * dx;
      } else this.fluid[c] = this.phi[c] < 0 ? 1 : 0;
    }
    // Cells cut by the glass wall hold few particles (part of them lies in the wall), so the particle level set misreads
    // them; a column of such cells along the wall, joined to the liquid mostly through its top and bottom faces, whose
    // top read below the true surface, had too low a pressure and drained: measured, a steady circulation down the high
    // wall at 20-30 mm/s that ate a steady tilt (centre of mass 15 % of the exact value). So the level set is carried
    // from inside the glass into the wall cells (as liquid level sets are extended into solids): a cut cell takes the
    // mean phi of its neighbours at the same height whose centres are inside, and is liquid where that is negative.
    if (this.wallPhi === 'linear') this.linearWallPhi(); else if (this.wallPhi === 'extend') this.extendWallPhi(); else this.inheritWallPhi();
  };
  // Near the wall the particle kernel sees particles on one side only (or, with mirror images, a surface forced flat at
  // the wall), so the level set there is biased. A free surface is locally a plane, and the level set of a plane is
  // linear in space; so in the band within 2 cells of the wall phi is extrapolated linearly along the radius from two
  // points 2.5 and 3.5 cells in from the wall, where the kernel sees particles all round.
  Fluid.prototype.linearWallPhi = function () {
    const nx = this.nx, ny = this.ny, nz = this.nz, dx = this.dx, nc = this.nc, ph = this.phi, fl = this.fluid;
    const src = this.phiSrc || (this.phiSrc = new Float64Array(nc)); src.set(ph);
    const at = (x, y, z) => {                                 // trilinear phi at a point, from the unmodified field
      const fx = (x - this.x0) / dx - 0.5, fy = Math.abs(y) / dx - 0.5, fz = z / dx - 0.5;
      const i = Math.floor(fx), j = Math.floor(fy), k = Math.floor(fz), tx = fx - i, ty = fy - j, tz = fz - k;
      let v = 0;
      for (let c = 0; c < 2; c++) for (let b = 0; b < 2; b++) for (let a = 0; a < 2; a++) {
        let ii = i + a, jj = j + b, kk = k + c;
        ii = ii < 0 ? 0 : ii >= nx ? nx - 1 : ii; jj = jj < 0 ? -jj - 1 : jj >= ny ? ny - 1 : jj; kk = kk < 0 ? 0 : kk >= nz ? nz - 1 : kk;
        v += (a ? tx : 1 - tx) * (b ? ty : 1 - ty) * (c ? tz : 1 - tz) * src[ii + nx * (jj + ny * kk)];
      }
      return v;
    };
    for (let k = 0; k < nz; k++) {
      const zc = (k + 0.5) * dx, R = this.Rz(zc);
      if (R > this.Rbox) continue;                           // above the rim: no wall
      const r1 = R - 2.5 * dx, r2 = R - 3.5 * dx;
      if (r2 <= 0) continue;
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        const x = this.x0 + (i + 0.5) * dx, y = (j + 0.5) * dx, r = Math.hypot(x, y);
        if (r < R - 2 * dx) continue;
        const cx = x / r, cy = y / r, p1 = at(cx * r1, cy * r1, zc), p2 = at(cx * r2, cy * r2, zc);
        const c = i + nx * (j + ny * k);
        ph[c] = p1 + (r - r1) * (p1 - p2) / (r1 - r2);
        fl[c] = ph[c] < 0 ? 1 : 0;
      }
    }
  };
  // wall cells: carry the level set from inside the glass into the cut cells
  Fluid.prototype.extendWallPhi = function () {
    const nx = this.nx, ny = this.ny, nz = this.nz, dx = this.dx, nc = this.nc;
    const ph = this.phi, fl = this.fluid;
    const inside = this.cellInside || (this.cellInside = (() => {
      const m = new Uint8Array(nc);
      for (let k = 0; k < nz; k++) { const R = this.Rz((k + 0.5) * dx);
        for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const x = this.x0 + (i + 0.5) * dx, y = (j + 0.5) * dx;
          m[i + nx * (j + ny * k)] = (R > this.Rbox || x * x + y * y < (R - 0.5 * dx) * (R - 0.5 * dx)) ? 1 : 0; } }
      return m; })());
    const done = this.cellDone || (this.cellDone = new Uint8Array(nc)); done.set(inside);
    for (let sweep = 0; sweep < 3; sweep++) {
      for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        const c = i + nx * (j + ny * k);
        if (done[c]) continue;
        let s = 0, m = 0;
        if (i > 0 && done[c - 1] === 1) { s += ph[c - 1]; m++; }
        if (i < nx - 1 && done[c + 1] === 1) { s += ph[c + 1]; m++; }
        if (j > 0 && done[c - nx] === 1) { s += ph[c - nx]; m++; }
        if (j < ny - 1 && done[c + nx] === 1) { s += ph[c + nx]; m++; }
        if (m) { ph[c] = s / m; fl[c] = ph[c] < 0 ? 1 : 0; done[c] = 2; }
      }
      for (let c = 0; c < nc; c++) if (done[c] === 2) done[c] = 1;
    }
  };
  // wall cells: a cut cell is liquid when it shares an open face with liquid beside it, or above it well below the surface
  Fluid.prototype.inheritWallPhi = function () {
    const nx = this.nx, ny = this.ny, nz = this.nz, dx = this.dx, ph = this.phi, fl = this.fluid;
    const U = (i, j, k) => i + (nx + 1) * (j + ny * k), V = (i, j, k) => i + nx * (j + (ny + 1) * k), Wf = (i, j, k) => i + nx * (j + ny * k);
    for (let sweep = 0; sweep < 2; sweep++) for (let k = nz - 1; k >= 0; k--) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const c = i + nx * (j + ny * k);
      if (fl[c]) continue;
      const x = this.x0 + (i + 0.5) * dx, y = (j + 0.5) * dx, R = this.Rz((k + 0.5) * dx);
      if (R > this.Rbox || x * x + y * y < (R - 0.5 * dx) ** 2) continue;   // only cells cut by the wall
      let best = 1;
      if (i > 0 && this.au[U(i, j, k)] > 0 && fl[c - 1]) best = Math.min(best, ph[c - 1]);
      if (i < nx - 1 && this.au[U(i + 1, j, k)] > 0 && fl[c + 1]) best = Math.min(best, ph[c + 1]);
      if (j > 0 && this.av[V(i, j, k)] > 0 && fl[c - nx]) best = Math.min(best, ph[c - nx]);
      if (j < ny - 1 && this.av[V(i, j + 1, k)] > 0 && fl[c + nx]) best = Math.min(best, ph[c + nx]);
      if (k < nz - 1 && this.aw[Wf(i, j, k + 1)] > 0 && fl[c + nx * ny] && ph[c + nx * ny] < -0.5 * dx) best = Math.min(best, ph[c + nx * ny]);
      if (best < 1) { fl[c] = 1; ph[c] = Math.min(best, -0.05 * dx); }
    }
  };

  // Per particle, once per step: its image in the wall (x, y scaled by fw = (2R - r)/r) and whether it has one (within the
  // kernel radius of the wall, below the rim); per cell, whether any of its particles has a wall image. The same numbers
  // phiAt computes for every pair, computed once.
  Fluid.prototype.levelSetParticles = function (Rk) {
    const np = this.np, nc = this.nc, px = this.px, py = this.py, pz = this.pz;
    if (!this.imgF || this.imgF.length < np) { this.imgF = new Float64Array(this.px.length); this.imgN = new Uint8Array(this.px.length); }
    const cellImg = this.cellImg || (this.cellImg = this.mk(Uint8Array, nc)); cellImg.fill(0);
    const fwA = this.imgF, nA = this.imgN, pcell = this.pcell;
    for (let p = 0; p < np; p++) {
      const ppx = px[p], ppy = py[p], ppz = pz[p], rr = Math.sqrt(ppx * ppx + ppy * ppy);
      const Rw = this.Rz(ppz), nImg = this.wallImages && ppz < this.zRim && rr > Rw - Rk ? 4 : 2;
      fwA[p] = rr > 1e-9 ? (2 * Rw - rr) / rr : 0; nA[p] = nImg;
      if (nImg === 4) cellImg[pcell[p]] = 1;
    }
    // the same numbers in cell order (sorted), so that the search below reads memory in sequence
    const L = this.px.length;
    if (!this.sX || this.sX.length < L) { const F = Float64Array; this.sX = this.mk(F, L); this.sY = this.mk(F, L); this.sZ = this.mk(F, L); this.sF = this.mk(F, L); this.sN = this.mk(Uint8Array, L); }
    const sorted = this.sorted, sX = this.sX, sY = this.sY, sZ = this.sZ, sF = this.sF, sN = this.sN;
    for (let s = 0; s < np; s++) { const p = sorted[s]; sX[s] = px[p]; sY[s] = py[p]; sZ[s] = pz[p]; sF[s] = fwA[p]; sN[s] = nA[p]; }
    // the cells of the 5 x 5 x 5 block around a cell centre that the kernel sphere (radius 2 dx) can reach: a cell is
    // skipped when its nearest point is at least 2 dx away and none of its particles has a wall image (those can land
    // anywhere near the wall). Same order as the full block, so the sums are added in the same order.
    if (!this.blockOff) {
      const off = [];
      for (let dk = -2; dk <= 2; dk++) for (let dj = -2; dj <= 2; dj++) for (let di = -2; di <= 2; di++) {
        const g = (d) => { const a = Math.abs(d); return a < 1 ? 0 : (a - 0.5) * (a - 0.5); };
        off.push(di, dj, dk, g(di) + g(dj) + g(dk) < 4 ? 1 : 0);   // in units of dx^2; R_k^2 = 4 dx^2
      }
      this.blockOff = Int32Array.from(off);
    }
  };
  // phi for the cells list[a], list[a + step], ... below list[b] (one thread's share of the search)
  Fluid.prototype.phiCells = function (list, a, b, R2, r, step) {
    const nx = this.nx, nxy = this.nx * this.ny;
    for (let n = a; n < b; n += step || 1) { const c = list[n]; this.phi[c] = this.phiCell(c % nx, Math.floor(c / nx) % this.ny, Math.floor(c / nxy), R2, r); }
  };
  // phi at the centre of cell (i, j, k): phiAt with the per-particle numbers of levelSetParticles (kernel radius 2 cells)
  Fluid.prototype.phiCell = function (ic, jc, kc, R2, r) {
    const nx = this.nx, ny = this.ny, nz = this.nz, dx = this.dx;
    const x = this.x0 + (ic + 0.5) * dx, y = (jc + 0.5) * dx, z = (kc + 0.5) * dx;
    const off = this.blockOff, cs = this.cellStart, sX = this.sX, sY = this.sY, sZ = this.sZ, sF = this.sF, sN = this.sN;
    const cellImg = this.cellImg;
    // mirror images lie at y <= 0, at least y = (j + 1/2) dx from this centre: out of reach (2 dx) from the third row on
    const mirror = jc < 2;
    let W = 0, sx = 0, sy = 0, sz = 0;
    for (let o = 0; o < off.length; o += 4) {
      const i = ic + off[o], j = jc + off[o + 1], k = kc + off[o + 2];
      if (i < 0 || i >= nx || j < 0 || j >= ny || k < 0 || k >= nz) continue;
      const c = i + nx * (j + ny * k), reach = off[o + 3];
      if (!reach && !cellImg[c]) continue;
      for (let s = cs[c], e = cs[c + 1]; s < e; s++) {
        // the particle, its mirror image in y = 0, and, near the wall, its image in the wall and that image's mirror
        // image, in that order (the order of the sums is the order of phiAt's)
        const ppx = sX[s], ppy = sY[s], ppz = sZ[s], ddz = ppz - z, dz2 = ddz * ddz;
        let ddx = ppx - x, ddy, d2;
        if (reach) {
          ddy = ppy - y; d2 = ddx * ddx + ddy * ddy + dz2;
          if (d2 < R2) { const q = 1 - d2 / R2, wt = q * q * q; W += wt; sx += wt * ppx; sy += wt * ppy; sz += wt * ppz; }
          if (mirror) {
            ddy = -ppy - y; d2 = ddx * ddx + ddy * ddy + dz2;
            if (d2 < R2) { const q = 1 - d2 / R2, wt = q * q * q; W += wt; sx += wt * ppx; sy += wt * -ppy; sz += wt * ppz; }
          }
        }
        if (sN[s] === 4) {
          const fw = sF[s], qx = ppx * fw, qy = ppy * fw;
          ddx = qx - x; ddy = qy - y; d2 = ddx * ddx + ddy * ddy + dz2;
          if (d2 < R2) { const q = 1 - d2 / R2, wt = q * q * q; W += wt; sx += wt * qx; sy += wt * qy; sz += wt * ppz; }
          if (mirror) {
            ddy = -qy - y; d2 = ddx * ddx + ddy * ddy + dz2;
            if (d2 < R2) { const q = 1 - d2 / R2, wt = q * q * q; W += wt; sx += wt * qx; sy += wt * -qy; sz += wt * ppz; }
          }
        }
      }
    }
    if (W < 1e-12) return 3 * dx;
    const mx = sx / W - x, my = sy / W - y, mz = sz / W - z;
    return Math.sqrt(mx * mx + my * my + mz * mz) - r;
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
            const Rw = this.Rz(ppz), nImg = this.wallImages && ppz < this.zRim && rr > Rw - Rk ? 4 : 2, fw = rr > 1e-9 ? (2 * Rw - rr) / rr : 0;
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
      // the six faces, written out: open fraction, velocity, side (+1 high, -1 low), neighbour cell or -1
      let div = 0;
      const fu1 = U(i + 1, j, k), fu0 = U(i, j, k), fv1 = V(i, j + 1, k), fv0 = V(i, j, k), fw1 = Wd(i, j, k + 1), fw0 = Wd(i, j, k);
      let wt;
      wt = this.au[fu1]; if (wt > 0) { div += wt * this.u[fu1]; if (i + 1 < nx) { if (fl[c + 1]) { Ad[c] += wt; Ax[c] = -wt; } else Ad[c] += wt / th(c, c + 1); } }
      wt = this.au[fu0]; if (wt > 0) { div -= wt * this.u[fu0]; if (i > 0) { if (fl[c - 1]) Ad[c] += wt; else Ad[c] += wt / th(c, c - 1); } }
      wt = this.av[fv1]; if (wt > 0) { div += wt * this.v[fv1]; if (j + 1 < ny) { if (fl[c + nx]) { Ad[c] += wt; Ay[c] = -wt; } else Ad[c] += wt / th(c, c + nx); } }
      wt = this.av[fv0]; if (wt > 0) { div -= wt * this.v[fv0]; if (j > 0) { if (fl[c - nx]) Ad[c] += wt; else Ad[c] += wt / th(c, c - nx); } }
      const nxy = nx * ny;
      wt = this.aw[fw1]; if (wt > 0) { div += wt * this.w[fw1]; if (k + 1 < nz) { if (fl[c + nxy]) { Ad[c] += wt; Az[c] = -wt; } else Ad[c] += wt / th(c, c + nxy); } }
      wt = this.aw[fw0]; if (wt > 0) { div -= wt * this.w[fw0]; if (k > 0) { if (fl[c - nxy]) Ad[c] += wt; else Ad[c] += wt / th(c, c - nxy); } }
      // volume correction: in a cell deep in the liquid, ask for the divergence (n_c/n0 - 1) * gamma / dt (n_c the particles
      // splatted to the cell centre with trilinear weights, a smooth count), so that an
      // overfull cell (particles crowded) expands and an underfull one contracts. Without it the particles drift apart
      // under a steady load (measured: +2.7 % volume in 4 s under a = 2 m/s^2) and the surface creeps up.
      let target = 0;
      if (this.volumeCorrection > 0 && phi[c] < -dx && this.Ad[c] >= 5.999) target = this.volumeCorrection * (this.dens[c] / this.n0 - 1) / dt;
      b[c] = -dx * (div - target * dx);
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
    // The liquid cells in index order, each with its six "has a neighbour on this side" bits; every loop below runs over
    // this list only (about 4 000 of the 9 000 cells at 4 mm). The arithmetic and its order are those of a loop over all
    // cells that skips the air: the air entries of r, z, s and the work vector are zero and stay zero.
    const L = this.cgList || (this.cgList = new Int32Array(nc)), B = this.cgBits || (this.cgBits = new Uint8Array(nc));
    let nf = 0;
    for (let k = 0, c = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++, c++) {
      if (!fl[c]) continue;
      L[nf] = c; B[nf] = (i > 0 ? 1 : 0) | (i + 1 < nx ? 2 : 0) | (j > 0 ? 4 : 0) | (j + 1 < ny ? 8 : 0) | (k > 0 ? 16 : 0) | (k + 1 < nz ? 32 : 0);
      nf++;
    }
    const t = this.tmpPre || (this.tmpPre = new Float64Array(nc));
    r.fill(0); z.fill(0); s.fill(0); t.fill(0);
    // the products A_off * pc the triangular sweeps use, once per solve instead of once per sweep ((A pc) t is how the
    // sweeps multiplied anyway, left to right)
    const Px = this.cgPx || (this.cgPx = new Float64Array(nc)), Py = this.cgPy || (this.cgPy = new Float64Array(nc)), Pz = this.cgPz || (this.cgPz = new Float64Array(nc));
    for (let c = 0; c < nc; c++) { Px[c] = Ax[c] * pc[c]; Py[c] = Ay[c] * pc[c]; Pz[c] = Az[c] * pc[c]; }
    const applyA = (x, out) => {
      for (let n = 0; n < nf; n++) {
        const c = L[n], bb = B[n];
        let v = Ad[c] * x[c];
        if (bb & 2) v += Ax[c] * x[c + 1];
        if (bb & 1) v += Ax[c - 1] * x[c - 1];
        if (bb & 8) v += Ay[c] * x[c + nx];
        if (bb & 4) v += Ay[c - nx] * x[c - nx];
        if (bb & 32) v += Az[c] * x[c + nxy];
        if (bb & 16) v += Az[c - nxy] * x[c - nxy];
        out[c] = v;
      }
    };
    const precond = (rr, out) => {
      for (let n = 0; n < nf; n++) {
        const c = L[n], bb = B[n];
        let v = rr[c];
        if (bb & 1) v -= Px[c - 1] * t[c - 1];
        if (bb & 4) v -= Py[c - nx] * t[c - nx];
        if (bb & 16) v -= Pz[c - nxy] * t[c - nxy];
        t[c] = v * pc[c];
      }
      for (let n = nf - 1; n >= 0; n--) {
        const c = L[n], bb = B[n];
        let v = t[c];
        if (bb & 2) v -= Px[c] * out[c + 1];
        if (bb & 8) v -= Py[c] * out[c + nx];
        if (bb & 32) v -= Pz[c] * out[c + nxy];
        out[c] = v * pc[c];
      }
    };
    // warm start from the previous step's pressure (it changes little between steps); tolerance relative to |b|
    let bmax = 0; for (let c = 0; c < nc; c++) { if (!fl[c]) q[c] = 0; if (Math.abs(b[c]) > bmax) bmax = Math.abs(b[c]); }
    if (bmax < 1e-14) { q.fill(0); this.cgIters = 0; return; }
    applyA(q, r);
    let rmax = 0; for (let n = 0; n < nf; n++) { const c = L[n]; r[c] = b[c] - r[c]; if (Math.abs(r[c]) > rmax) rmax = Math.abs(r[c]); }
    const tol = 1e-7 * bmax;
    if (rmax < tol) { this.cgIters = 0; return; }
    precond(r, z); s.set(z);
    let sigmaR = 0; for (let n = 0; n < nf; n++) { const c = L[n]; sigmaR += z[c] * r[c]; }
    let it = 0;
    for (; it < 300; it++) {
      applyA(s, z);
      let sz = 0; for (let n = 0; n < nf; n++) { const c = L[n]; sz += s[c] * z[c]; }
      const alpha = sigmaR / sz;
      rmax = 0;
      for (let n = 0; n < nf; n++) { const c = L[n]; q[c] += alpha * s[c]; r[c] -= alpha * z[c]; if (Math.abs(r[c]) > rmax) rmax = Math.abs(r[c]); }
      if (rmax < tol) break;
      precond(r, z);
      let sn = 0; for (let n = 0; n < nf; n++) { const c = L[n]; sn += z[c] * r[c]; }
      const beta = sn / sigmaR; sigmaR = sn;
      for (let n = 0; n < nf; n++) { const c = L[n]; s[c] = z[c] + beta * s[c]; }
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

  // Second-order Runge–Kutta (midpoint) through the grid velocity. The three components are sampled by one closure each,
  // made once per step with the grid's numbers bound (the same arithmetic as Fluid.sample, without its dispatch).
  function sampler(a, sx, sy, sz, ox, oy, oz, x0, dx) {
    const sxy = sx * sy, inv = 1 / dx;
    return function (x, y, z) {
      const fx = (x - x0) / dx - ox, fy = y / dx - oy, fz = z / dx - oz;
      const i = Math.floor(fx), j = Math.floor(fy), k = Math.floor(fz), tx = fx - i, ty = fy - j, tz = fz - k;
      const i0 = i < 0 ? 0 : i >= sx ? sx - 1 : i, i1 = i + 1 < 0 ? 0 : i + 1 >= sx ? sx - 1 : i + 1;
      const j0 = j < 0 ? 0 : j >= sy ? sy - 1 : j, j1 = j + 1 < 0 ? 0 : j + 1 >= sy ? sy - 1 : j + 1;
      const k0 = k < 0 ? 0 : k >= sz ? sz - 1 : k, k1 = k + 1 < 0 ? 0 : k + 1 >= sz ? sz - 1 : k + 1;
      const b00 = j0 * sx + k0 * sxy, b10 = j1 * sx + k0 * sxy, b01 = j0 * sx + k1 * sxy, b11 = j1 * sx + k1 * sxy;
      const c00 = a[i0 + b00] + tx * (a[i1 + b00] - a[i0 + b00]), c10 = a[i0 + b10] + tx * (a[i1 + b10] - a[i0 + b10]);
      const c01 = a[i0 + b01] + tx * (a[i1 + b01] - a[i0 + b01]), c11 = a[i0 + b11] + tx * (a[i1 + b11] - a[i0 + b11]);
      const d0 = c00 + ty * (c10 - c00), d1 = c01 + ty * (c11 - c01);
      return d0 + tz * (d1 - d0);
    };
  }
  Fluid.prototype.advect = function (dt) {
    if (this.pool) this.pool.run(4, this.np, dt, 0); else this.advectRange(dt, 0, this.np);
    this.collide();
  };
  Fluid.prototype.advectRange = function (dt, p0, p1) {
    const nx = this.nx, ny = this.ny, nz = this.nz, x0 = this.x0, dx = this.dx;
    if (!this.sU) {
      this.sU = sampler(this.u, nx + 1, ny, nz, 0, 0.5, 0.5, x0, dx);
      this.sV = sampler(this.v, nx, ny + 1, nz, 0.5, 0, 0.5, x0, dx);
      this.sW = sampler(this.w, nx, ny, nz + 1, 0.5, 0.5, 0, x0, dx);
    }
    const sU = this.sU, sV = this.sV, sW = this.sW, px = this.px, py = this.py, pz = this.pz, pv = this.pv, h = 0.5 * dt;
    for (let p = p0; p < p1; p++) {
      let x = px[p], y = py[p], z = pz[p];
      const u1 = sU(x, y, z), v1 = sV(x, y, z), w1 = sW(x, y, z);
      const xm = x + h * u1, ym = Math.abs(y + h * v1), zm = z + h * w1;
      x += dt * sU(xm, ym, zm); y += dt * sV(xm, ym, zm); z += dt * sW(xm, ym, zm);
      if (y < 0) { y = -y; pv[p] = -pv[p]; }           // mirror plane
      px[p] = x; py[p] = y; pz[p] = z;
    }
  };

  // The glass wall R(z): a particle outside it is put back onto the wall along the wall's normal and loses its speed along the
  // wall's outward normal n = (cos t, sin t, -R'(z)) / sqrt(1 + R'^2) (free slip); likewise the floor and the box top.
  // Above the rim there is no wall: a particle that is above the rim and outside the rim's radius has left the glass
  // (spilled). It is removed, and its mass and its momentum relative to the glass are recorded for the coupling.
  Fluid.prototype.collide = function () {
    const e = 0.02 * this.dx, spill = isFinite(this.zRim);
    this.spillNow = 0; this.spillPx = 0; this.spillPz = 0;
    if (!this.spillList) this.spillList = [];
    for (let p = 0; p < this.np; p++) {
      let x = this.px[p], y = this.py[p], z = this.pz[p];
      const r2 = x * x + y * y;
      if (spill && z > this.zRim && r2 > this.Rrim * this.Rrim) {
        this.spillList.push([x, y, z, this.pu[p], this.pv[p], this.pw[p]]);
        this.spillNow++; this.spillPx += this.pu[p]; this.spillPz += this.pw[p];
        this.removeParticle(p); p--; continue;
      }
      const Rin = Math.min(this.Rz(z), this.Rbox) - e;
      if (r2 > Rin * Rin) {
        // back to the wall along its normal: the distance to the wall line r = R(z) is (r - R) / l, so the particle
        // moves by that much along -n (radially in by (r - R)/l^2, and up by s (r - R)/l^2 where the wall leans out)
        const r = Math.sqrt(r2), cx = x / r, cy = y / r, s = this.dRz(z), l2 = 1 + s * s, l = Math.sqrt(l2);
        const nx = cx / l, ny = cy / l, nz = -s / l, pen = r - Rin;
        const rn = r - pen / l2; z += s * pen / l2;
        x = cx * rn; y = cy * rn;
        const un = this.pu[p] * nx + this.pv[p] * ny + this.pw[p] * nz;
        if (un > 0) { this.pu[p] -= un * nx; this.pv[p] -= un * ny; this.pw[p] -= un * nz; }
      }
      if (z < e) { z = e; if (this.pw[p] < 0) this.pw[p] = 0; }
      if (z > this.H - e) { z = this.H - e; if (this.pw[p] > 0) this.pw[p] = 0; }
      this.px[p] = x; this.py[p] = y; this.pz[p] = z;
    }
    this.spilled += this.spillNow;
    // both halves: the momentum (relative to the glass) carried out this step, kg m/s
    this.spillPx *= 2 * this.mp; this.spillPz *= 2 * this.mp;
  };
  // remove particle p by moving the last particle into its place
  Fluid.prototype.removeParticle = function (p) {
    const q = this.np - 1;
    if (p !== q) {
      this.px[p] = this.px[q]; this.py[p] = this.py[q]; this.pz[p] = this.pz[q];
      this.pu[p] = this.pu[q]; this.pv[p] = this.pv[q]; this.pw[p] = this.pw[q];
      for (let c = 0; c < 3; c++) for (let d = 0; d < 3; d++) this.pc[c][d][p] = this.pc[c][d][q];
    }
    this.px[q] = NaN; this.py[q] = NaN; this.pz[q] = NaN;
    this.np = q;
  };
  // mass of the stout still in the glass (both halves)
  Fluid.prototype.liquidMass = function () { return 2 * this.mp * this.np; };

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

  // particles per cell, counted smoothly: each particle shares itself among the 8 nearest cell centres (trilinear)
  Fluid.prototype.density = function () {
    const nx = this.nx, ny = this.ny, nz = this.nz, dx = this.dx, inv = 1 / dx;
    const d = this.dens || (this.dens = new Float64Array(this.nc)); d.fill(0);
    for (let p = 0; p < this.np; p++) {
      const fx = (this.px[p] - this.x0) * inv - 0.5, fy = this.py[p] * inv - 0.5, fz = this.pz[p] * inv - 0.5;
      const i = Math.floor(fx), j = Math.floor(fy), k = Math.floor(fz), tx = fx - i, ty = fy - j, tz = fz - k;
      for (let c = 0; c < 2; c++) { let kk = k + c; if (kk < 0 || kk >= nz) continue; const wz = c ? tz : 1 - tz;
        for (let b = 0; b < 2; b++) { let jj = j + b; jj = jj < 0 ? -jj - 1 : jj; if (jj >= ny) continue; const wy = b ? ty : 1 - ty;   // y < 0: the mirror cell
          for (let a = 0; a < 2; a++) { const ii = i + a; if (ii < 0 || ii >= nx) continue; d[ii + nx * (jj + ny * kk)] += (a ? tx : 1 - tx) * wy * wz; } } }
    }
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
    if (this.volumeCorrection > 0) this.density();
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

  // Height of the liquid column over each grid column. The particles' volume standing on the column, smoothed with a
  // 3 x 3 binomial filter, is matched to the column's open volume up to height h, smoothed the same way: h solves
  // B(V_col) = B(integral from 0 to h of a_col(z) dz), a_col(z) the part of the column's square inside the wall R(z).
  // For a flat surface the two sides agree exactly. This is the depth-averaged free surface: it holds the liquid's
  // volume and ignores drops thrown above the surface; it cannot show a breaking wave. Float64Array nx * ny, metres.
  Fluid.prototype.columnHeights = function () {
    const nx = this.nx, ny = this.ny, dx = this.dx, ncol = nx * ny;
    const vol = this.colVol || (this.colVol = new Float64Array(ncol));
    const out = this.colH || (this.colH = new Float64Array(ncol));
    vol.fill(0);
    const Vp = this.Vseed;              // the volume each particle fills at its seeding spacing, (dx/s)^3
    const fold = (j) => (j < 0 ? -j - 1 : j >= ny ? ny - 1 : j);
    for (let p = 0; p < this.np; p++) {
      let i = Math.floor((this.px[p] - this.x0) / dx), j = Math.floor(this.py[p] / dx);
      i = i < 0 ? 0 : i >= nx ? nx - 1 : i; j = j < 0 ? 0 : j >= ny ? ny - 1 : j;
      vol[i + nx * j] += Vp;
    }
    const blur = (src, dst, off, stride) => {   // 3 x 3 binomial on one level of a column table
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        let a = 0;
        for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) {
          const ii = i + di; if (ii < 0 || ii >= nx) continue;
          a += (di ? 0.25 : 0.5) * (dj ? 0.25 : 0.5) * src[(ii + nx * fold(j + dj)) * stride + off];
        }
        dst[(i + nx * j) * stride + off] = a;
      }
    };
    if (!this.colVb) this.buildColumnTables(blur);
    const t1 = this.colT1 || (this.colT1 = new Float64Array(ncol));
    blur(vol, t1, 0, 1);
    const M = this.colM, Vb = this.colVb, dz = this.colDz;
    for (let n = 0; n < ncol; n++) {
      const v = t1[n], base = n * (M + 1);
      if (Vb[base + M] <= 0) { out[n] = 0; continue; }
      if (v >= Vb[base + M]) { out[n] = M * dz; continue; }
      let lo = 0, hi = M;                                    // Vb increases with height: bisect
      while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (Vb[base + mid] <= v) lo = mid; else hi = mid; }
      const a = Vb[base + lo], b = Vb[base + hi];
      out[n] = (lo + (b > a ? (v - a) / (b - a) : 0)) * dz;
    }
    return out;
  };
  // the open volume of every column up to each height (every 0.5 mm), and the same smoothed by the column filter
  Fluid.prototype.buildColumnTables = function (blur) {
    const nx = this.nx, ny = this.ny, dx = this.dx, ncol = nx * ny, dz = 0.0005, M = Math.round(this.H / dz), S = 12;
    const Vc = new Float64Array(ncol * (M + 1)), Vb = new Float64Array(ncol * (M + 1));
    for (let m = 1; m <= M; m++) {
      const R = Math.min(this.Rz((m - 0.5) * dz), 2 * this.Rbox), R2 = R * R;
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        let n = 0;
        for (let a = 0; a < S; a++) for (let b = 0; b < S; b++) {
          const x = this.x0 + (i + (a + 0.5) / S) * dx, y = (j + (b + 0.5) / S) * dx;
          if (x * x + y * y < R2) n++;
        }
        const c = i + nx * j;
        Vc[c * (M + 1) + m] = Vc[c * (M + 1) + m - 1] + n / (S * S) * dx * dx * dz;
      }
    }
    for (let m = 0; m <= M; m++) blur(Vc, Vb, m, M + 1);
    this.colVc = Vc; this.colVb = Vb; this.colM = M; this.colDz = dz;
    // the open area of each column at the bottom, kept for the checks
    this.colArea = new Float64Array(ncol);
    for (let c = 0; c < ncol; c++) this.colArea[c] = Vc[c * (M + 1) + 1] / dz;
  };

  // the column height at (x, y), bilinear between column centres (y folded by the mirror plane)
  Fluid.prototype.columnHeightAt = function (x, y) {
    const nx = this.nx, ny = this.ny, dx = this.dx, H = this.colH;
    y = Math.abs(y);
    // columns near the wall are cut by it and hold too few particles to count: beyond r1 = R(h0) - 2.5 dx the height
    // is extended linearly along the radius from the values at r1 and r1 - 1.5 dx
    const r = Math.hypot(x, y), r1 = this.Rz(Math.min(this.h0, this.zRim)) - 2.5 * dx, r2 = r1 - 1.5 * dx;
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
  // The cart: x along the road, z_b the body (bottom), z_w the axle. The wheel rolls without slipping, driven through a
  // gearbox by a DC motor whose current is set by a current loop (a torque drive). A sampled controller sets the current:
  // 'off' holds the current that balances the drag at the set speed (open loop), 'speed' adds a PI loop on the speed.
  // An active suspension can add a force between body and axle (skyhook on the body's vertical speed). The reader can
  // push with buttons or drag the cart with a hand modelled as a spring and damper with a force limit.
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
    this.v0 = o.v0 != null ? o.v0 : 1.0;  // set speed, m/s
    this.ml = o.ml || 0;         // stout in the glass, kg (set by the coupling; falls as it spills)
    this.Ls = o.Ls || 0.08;      // unloaded spring length (body above axle), m
    this.bodyW = o.bodyW || 0.22; this.bodyH = o.bodyH || 0.03;   // the body block, m (it catches spilled drops)
    this.glassFloor = o.glassFloor || 0.036;   // the glass's inner floor above the body's bottom: body 30 mm + glass base 6 mm
    this.g = 9.81;
    // drive: DC gear motor (a small 12 V motor; the numbers are a modelling choice, stated in the note)
    this.Ngear = o.Ngear || 10;  // gear ratio, motor turns per wheel turn
    this.Km = o.Km || 0.02;      // torque constant = back-EMF constant, N m/A = V s/rad
    this.Ra = o.Ra || 2.0;       // armature resistance, ohm
    this.Jm = o.Jm || 2e-6;      // rotor inertia, kg m^2
    this.Vmax = o.Vmax || 12;    // supply voltage, V
    this.Imax = o.Imax || 3;     // current limit of the drive, A
    this.tauI = o.tauI || 0.002; // time constant of the current loop, s
    this.ctrl = o.ctrl || 'speed';
    this.Ts = o.Ts || 0.001;     // controller sampling period, s
    const b = this.Ngear * this.Km / this.Rw;                 // force at the road per amp, N/A
    const M = this.Mb + this.ml + this.mw + this.Iw / (this.Rw * this.Rw) + this.Ngear * this.Ngear * this.Jm / (this.Rw * this.Rw);
    this.wc = o.wc || 2 * Math.PI * 8;                         // speed-loop crossover, rad/s
    this.Kp = o.Kp || M * this.wc / b;                         // A per m/s
    this.Ki = o.Ki || this.Kp * this.wc / 4;                   // A per m
    // active suspension: skyhook on the body's vertical speed, a force actuator with a lag and a limit
    this.susp = o.susp || false;
    this.csky = o.csky || 2 * 0.7 * Math.sqrt(this.k * (this.Mb + this.ml));   // N s/m
    this.Umax = o.Umax || 40;    // N
    this.tauU = o.tauU || 0.005; // s
    // the reader's hand
    this.kh = o.kh || 300; this.ch = o.ch || 30; this.Fhmax = o.Fhmax || 25;   // N/m, N s/m, N
    this.hand = null;            // x the hand pulls towards, or null
    this.road = o.road || new Road({ Rw: this.Rw });
    this.pushF = 0;              // the reader's push, N (horizontal)
    this.reset(o.x0 != null ? o.x0 : 0);
  }
  Cart.prototype.bForce = function () { return this.Ngear * this.Km / this.Rw; };
  Cart.prototype.massX = function () { return this.Mb + this.ml + this.mw + (this.Iw + this.Ngear * this.Ngear * this.Jm) / (this.Rw * this.Rw); };
  Cart.prototype.reset = function (x) {
    const g = this.g, Ms = this.Mb + this.ml, za = this.road.axle(x)[0];
    this.x = x; this.vx = this.v0;
    this.zw = za - (Ms + this.mw) * g / this.kt;                 // static tyre deflection
    this.zb = this.zw + this.Ls - Ms * g / this.k;               // static spring deflection
    this.vzb = 0; this.vzw = 0; this.t = 0; this.Flx = 0; this.Flz = 0;
    this.i = this.cx * this.v0 / this.bForce();                  // the current that holds the set speed against the drag
    this.icmd = this.i; this.xi = 0; this.us = 0; this.uscmd = 0; this.tSample = 0;
    this.forces(0, 0);
  };
  // the controller, run every Ts: the motor current command, and the suspension force command
  Cart.prototype.sample = function () {
    const i0 = this.cx * this.v0 / this.bForce(), e = this.v0 - this.vx;
    if (this.ds) { this.ds.set('v_s', this.vx); this.ds.set('xi_s', this.xi); this.ds.set('vzb_s', this.vzb); }
    if (this.ctrl === 'speed') {
      let ic = i0 + this.Kp * e + this.Ki * this.xi;
      if (Math.abs(ic) < this.Imax) this.xi += e * this.Ts;     // anti-windup: integrate only when not saturated
      this.icmd = ic;
    } else this.icmd = i0;
    this.uscmd = this.susp ? -this.csky * this.vzb : 0;
    if (this.uscmd > this.Umax) this.uscmd = this.Umax; else if (this.uscmd < -this.Umax) this.uscmd = -this.Umax;
  };
  // the forces at the present state, with the liquid's reaction (Fx, Fz) beyond rigid co-motion: kept on the cart
  // (and in the store, when the page gave one) so that every stored force belongs to the stored state
  Cart.prototype.forces = function (Fx, Fz) {
    const g = this.g, Ms = this.Mb + this.ml, D = this.ds;
    const ad = this.road.axle(this.x), za = ad[0], dza = ad[1];
    const vza = dza * this.vx;
    let N = this.kt * (za - this.zw) + this.ct * (vza - this.vzw);
    if (N < 0) N = 0;                                            // the tyre cannot pull on the road
    const Fs = -this.k * (this.zb - this.zw - this.Ls) - this.c * (this.vzb - this.vzw) + this.us;  // on the body
    const Mx = this.massX();
    const Fmotor = this.bForce() * this.i, Froad = -N * dza;
    let Fhand = 0;
    if (this.hand != null) { Fhand = this.kh * (this.hand - this.x) - this.ch * this.vx; if (Fhand > this.Fhmax) Fhand = this.Fhmax; else if (Fhand < -this.Fhmax) Fhand = -this.Fhmax; }
    const ax = (Froad + Fmotor - this.cx * this.vx + this.pushF + Fhand + Fx) / Mx;
    const azb = (Fs - Ms * g + Fz) / Ms;
    const azw = (-Fs - this.mw * g + N) / this.mw;
    // the current the drive can reach: limited by the drive and by the voltage left over the back-EMF
    const emf = this.Km * this.Ngear * this.vx / this.Rw;
    let ilim = this.icmd; if (ilim > this.Imax) ilim = this.Imax; else if (ilim < -this.Imax) ilim = -this.Imax;
    const iHi = (this.Vmax - emf) / this.Ra, iLo = (-this.Vmax - emf) / this.Ra;
    if (ilim > iHi) ilim = iHi; else if (ilim < iLo) ilim = iLo;
    this.za = za; this.dza = dza; this.N = N; this.Fs = Fs; this.Froad = Froad; this.Fdrive = Fmotor; this.Fhand = Fhand;
    this.ax = ax; this.azb = azb; this.azw = azw; this.Flx = Fx; this.Flz = Fz; this.ireach = ilim; this.emf = emf;
    this.Vm = this.Ra * this.i + emf;                             // motor voltage
    if (D) {
      D.set('x', this.x); D.set('vx', this.vx); D.set('zb', this.zb); D.set('vzb', this.vzb); D.set('zw', this.zw); D.set('vzw', this.vzw);
      D.set('z_a', za); D.set('dz_a', dza); D.set('N', N); D.set('F_s', Fs); D.set('F_road', Froad); D.set('F_drive', Fmotor);
      D.set('F_push', this.pushF); D.set('F_hand', Fhand); D.set('F_lx', Fx); D.set('F_lz', Fz); D.set('a_x', ax); D.set('a_zb', azb); D.set('a_zw', azw);
      D.set('i_m', this.i); D.set('i_cmd', this.icmd); D.set('i_reach', ilim); D.set('V_m', this.Vm); D.set('emf', emf); D.set('u_s', this.us); D.set('u_s_cmd', this.uscmd);
      D.set('Mx', Mx); D.set('Ms', Ms); D.set('ml', this.ml);
    }
  };
  // one step h: the controller when a sample is due; then symplectic Euler for the mechanics (velocities from the forces
  // at the present state, positions from the new velocities); the current and the suspension force follow their
  // first-order lags exactly over h; then the forces at the new state, for the next step
  Cart.prototype.step = function (h, Fx, Fz) {
    this.tSample += h;
    if (this.tSample >= this.Ts - 1e-12) { this.tSample -= this.Ts; this.sample(); this.forces(Fx, Fz); }
    this.vx += h * this.ax; this.vzb += h * this.azb; this.vzw += h * this.azw;
    this.x += h * this.vx; this.zb += h * this.vzb; this.zw += h * this.vzw;
    const ei = Math.exp(-h / this.tauI), eu = Math.exp(-h / this.tauU);
    this.i = this.ireach + (this.i - this.ireach) * ei;
    this.us = this.uscmd + (this.us - this.uscmd) * eu;
    this.t += h;
    this.forces(Fx, Fz);
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
  // advance by dt (s), in equal fluid steps no longer than dtMax and the CFL limit (0.8 cell per step)
  World.prototype.advance = function (dt) {
    let left = dt;
    while (left > 1e-12) {
      const umax = this.fluid.maxSpeed();
      // the longest step allowed (dtMax, and a particle crosses at most 0.8 cell); when it is shorter than what is left, the
      // rest is cut into equal steps, not into full steps and a sliver (a 0.02 ms remainder step was measured)
      const hmax = Math.min(this.dtMax, umax > 0 ? 0.8 * this.fluid.dx / umax : this.dtMax);
      const h = left <= hmax ? left : left / Math.ceil(left / hmax);
      const c = this.cart, vx0 = c.vx, vz0 = c.vzb;
      // The stout's push is handed over as an impulse: the momentum -(dP + P_spill) it gave up in the last fluid step is
      // spread over this step, whatever its length. (Handing over the force -(dP + P_spill)/h_last instead multiplied the
      // impulse by h/h_last: after a step cut short by the CFL limit, e.g. a 0.02 ms remainder before a 5 ms step, the cart
      // got a kick hundreds of times too large; found 6 November 2026, tools/fig12/study.cjs 25 off.) Equal steps: unchanged.
      if (this.J && h !== this.hLast) { this.Fx = this.J[0] / h; this.Fz = this.J[1] / h; c.forces(this.Fx, this.Fz); }
      const n = Math.max(1, Math.round(h / this.hCart)), hc = h / n;
      for (let i = 0; i < n; i++) c.step(hc, this.Fx, this.Fz);
      const ax = (c.vx - vx0) / h, az = (c.vzb - vz0) / h;     // the glass's mean acceleration over the step
      this.fluid.step(h, ax, az);
      const P = this.fluid.momentum();
      // reaction of the liquid on the glass beyond rigid co-motion: -dP_rel/dt, counting the momentum that left over
      // the rim with the spilled stout (it was not pushed by the glass at the moment it left)
      const P0 = this.P, f = this.fluid;
      this.J = [-(P[0] + f.spillPx - P0[0]), -(P[1] + f.spillPz - P0[1])]; this.hLast = h;
      this.Fx = this.J[0] / h; this.Fz = this.J[1] / h;
      if (f.spillNow) { c.ml = f.liquidMass(); this.dropsFrom(f.spillList); }
      f.spillList.length = 0;
      this.moveDrops(h);
      this.P = P; this.lastAx = ax; this.lastAz = az;
      c.forces(this.Fx, this.Fz);                               // the stout's new reaction acts from now
      left -= h; this.t += h; this.steps = (this.steps || 0) + 1;
      const D = this.ds;
      if (D) {
        D.set('t', this.t); D.set('h_f', h); D.set('n_cart', n); D.set('vx_0', vx0); D.set('vzb_0', vz0); D.set('vx_1', c.vx); D.set('vzb_1', c.vzb);
        D.set('a_gx', ax); D.set('a_gz', az); D.set('P0_x', P0[0]); D.set('P0_z', P0[1]); D.set('P_x', P[0]); D.set('P_z', P[1]);
        D.set('F_lx_next', this.Fx); D.set('F_lz_next', this.Fz); D.set('steps', this.steps); D.set('P_spill_x', f.spillPx); D.set('P_spill_z', f.spillPz);
        D.set('cg_iters', this.fluid.cgIters); D.set('cg_res', this.fluid.cgResidual || 0);
      }
    }
  };

  // Spilled stout in the room: each particle that left over the rim becomes a drop (with its mirror image, the other
  // half of the glass) at the glass's position plus its own, with the glass's velocity plus its own, falling freely
  // (no air drag) until it meets the body's top or the road, where it stays as a splash. At most 6000 drops are kept.
  World.prototype.dropsFrom = function (list) {
    const c = this.cart, D = this.drops || (this.drops = []);
    for (const q of list) for (const m of [1, -1]) {
      if (D.length >= 6000) D.shift();
      D.push({ x: c.x + q[0], y: m * q[1], z: c.zb + c.glassFloor + q[2], vx: c.vx + q[3], vy: m * q[4], vz: c.vzb + q[5], landed: false });
    }
    this.spilledMass = (this.spilledMass || 0) + list.length * 2 * this.fluid.mp;
  };
  World.prototype.moveDrops = function (h) {
    const D = this.drops; if (!D) return;
    const g = this.cart.g, road = this.cart.road;
    const c = this.cart, top = c.zb + c.bodyH;
    for (const d of D) {
      if (d.onBody) { d.x = c.x + d.rel; d.z = c.zb + c.bodyH; continue; }   // a splash on the body rides with it
      if (d.landed) continue;
      const zPrev = d.z;
      d.vz -= g * h; d.x += d.vx * h; d.y += d.vy * h; d.z += d.vz * h;
      // the body's top face catches a drop that crosses it inside the body's footprint
      if (zPrev >= top && d.z <= top && Math.abs(d.x - c.x) <= c.bodyW / 2) { d.z = top; d.landed = true; d.onBody = true; d.rel = d.x - c.x; continue; }
      const zr = road.zr(d.x);
      if (d.z <= zr) { d.z = zr; d.landed = true; }
    }
  };

  // give the world a store (scripts/dataset.js): the particles' positions and the column heights then live in the
  // store's arrays, and the scalars above are written into it where they are computed
  World.prototype.attach = function (ds) {
    const f = this.fluid;
    // the store holds the solver's particle arrays (with threads, the shared ones; otherwise the store's own, filled)
    ['px', 'py', 'pz'].forEach((k) => { if (f.shared) ds.set(k, f[k]); else { const a = ds.get(k); a.set(f[k]); f[k] = a; } });
    f.colH = ds.get('h_col');
    this.ds = ds; this.cart.ds = ds;
    this.cart.forces(this.Fx, this.Fz);
    f.columnHeights(); ds.touch('h_col');
  };

  return { Fluid, Road, Cart, World };
});
