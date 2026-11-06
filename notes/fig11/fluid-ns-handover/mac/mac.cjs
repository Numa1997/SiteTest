// 2D incompressible Navier–Stokes on a staggered (MAC) grid, two-way coupled to the cart and two rods of project 05.
// Pressure coupling after Batty, Bertails & Bridson 2007 (ACM TOG 26(3) 100): fluid-fraction face weights w (eq. 4, 7),
// solid enters the divergence with (1 - w) v_body, force on the solid = -sum vol (grad p) (eq. 10), solved together.
// Articulated bodies: generalized coordinates q = (x, th1, th2). The divergence is linear in qdot, so p = p0 + sum_i qdot_i p_i,
// the generalized fluid force is Q(qdot) = Q[p0] + K qdot, and the machine is advanced implicitly: (D - dt K) qdot' = D qdot + dt (H u - C - G + Q[p0]).
// Units SI; 2D fields are per metre of depth, each body's force is multiplied by its own depth b_k.
'use strict';

function fracInside(a, b) {   // fraction of the segment between level-set values a, b that is inside (phi < 0)
  if (a < 0 && b < 0) return 1; if (a >= 0 && b >= 0) return 0;
  return a < 0 ? a / (a - b) : b / (b - a);
}

// ---------- multigrid-preconditioned CG for  sum_f w_f (p_c - p_nb) / h^2 = r  on cell centres ----------
class Poisson {
  constructor(nx, ny, h, levels) {
    this.L = []; let n = nx, m = ny, hh = h;
    for (let l = 0; l < levels; l++) {
      this.L.push({ nx: n, ny: m, h: hh, wx: new Float64Array((n + 1) * m), wy: new Float64Array(n * (m + 1)), d: new Float64Array(n * m),
        x: new Float64Array(n * m), b: new Float64Array(n * m), r: new Float64Array(n * m) });
      if (n % 2 || m % 2 || n <= 8 || m <= 8) break; n /= 2; m /= 2; hh *= 2;
    }
    const N = nx * ny; this.rr = new Float64Array(N); this.z = new Float64Array(N); this.pp = new Float64Array(N); this.Ap = new Float64Array(N);
  }
  setWeights(wx, wy) {   // finest weights given; coarser by averaging the two fine faces under each coarse face
    const L0 = this.L[0]; L0.wx.set(wx); L0.wy.set(wy);
    for (let l = 1; l < this.L.length; l++) { const F = this.L[l - 1], C = this.L[l];
      for (let J = 0; J < C.ny; J++) for (let I = 0; I <= C.nx; I++) C.wx[J * (C.nx + 1) + I] = 0.5 * (F.wx[(2 * J) * (F.nx + 1) + 2 * I] + F.wx[(2 * J + 1) * (F.nx + 1) + 2 * I]);
      for (let J = 0; J <= C.ny; J++) for (let I = 0; I < C.nx; I++) C.wy[J * C.nx + I] = 0.5 * (F.wy[(2 * J) * F.nx + 2 * I] + F.wy[(2 * J) * F.nx + 2 * I + 1]);
    }
    for (const Lv of this.L) { const { nx, ny, wx, wy, d } = Lv, ih = 1 / (Lv.h * Lv.h), N = nx * ny;
      if (!Lv.cw) { Lv.cw = new Float64Array(N); Lv.ce = new Float64Array(N); Lv.cs = new Float64Array(N); Lv.cn = new Float64Array(N); Lv.id = new Float64Array(N); }
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const c = j * nx + i;
        d[c] = (wx[j * (nx + 1) + i] + wx[j * (nx + 1) + i + 1] + wy[j * nx + i] + wy[(j + 1) * nx + i]) * ih;
        Lv.cw[c] = i > 0 ? wx[j * (nx + 1) + i] * ih : 0; Lv.ce[c] = i < nx - 1 ? wx[j * (nx + 1) + i + 1] * ih : 0;
        Lv.cs[c] = j > 0 ? wy[j * nx + i] * ih : 0; Lv.cn[c] = j < ny - 1 ? wy[(j + 1) * nx + i] * ih : 0; Lv.id[c] = d[c] > 0 ? 1 / d[c] : 0; } }
  }
  apply(Lv, x, out) {   // padded access avoided by zero coefficients on the edges (x[c±1] read only where the coefficient is non-zero)
    const { nx, ny, d, cw, ce, cs, cn } = Lv, N = nx * ny;
    for (let c = 0; c < N; c++) { let s = d[c] * x[c];
      if (cw[c]) s -= cw[c] * x[c - 1]; if (ce[c]) s -= ce[c] * x[c + 1]; if (cs[c]) s -= cs[c] * x[c - nx]; if (cn[c]) s -= cn[c] * x[c + nx];
      out[c] = s; }
  }
  smooth(Lv, x, b, sweeps, order) {   // red-black Gauss–Seidel; order 0: red then black, 1: black then red (symmetric V-cycle)
    const { nx, ny, cw, ce, cs, cn, id } = Lv;
    for (let s = 0; s < sweeps; s++) for (let pass = 0; pass < 2; pass++) { const col = (pass + order) & 1;
      for (let j = 0; j < ny; j++) { const row = j * nx; for (let i = (j + col) & 1; i < nx; i += 2) { const c = row + i;
        if (!id[c]) { x[c] = 0; continue; }
        let s2 = b[c]; if (cw[c]) s2 += cw[c] * x[c - 1]; if (ce[c]) s2 += ce[c] * x[c + 1]; if (cs[c]) s2 += cs[c] * x[c - nx]; if (cn[c]) s2 += cn[c] * x[c + nx];
        x[c] = s2 * id[c]; } } }
  }
  vcycle(l) {
    const Lv = this.L[l];
    if (l === this.L.length - 1) { Lv.x.fill(0); this.smooth(Lv, Lv.x, Lv.b, 40, 0); this.smooth(Lv, Lv.x, Lv.b, 40, 1); return; }
    Lv.x.fill(0); this.smooth(Lv, Lv.x, Lv.b, 2, 0);
    this.apply(Lv, Lv.x, Lv.r); for (let c = 0; c < Lv.r.length; c++) Lv.r[c] = Lv.b[c] - Lv.r[c];
    const C = this.L[l + 1];
    for (let J = 0; J < C.ny; J++) for (let I = 0; I < C.nx; I++) { const f = 2 * J * Lv.nx + 2 * I;
      C.b[J * C.nx + I] = 0.25 * (Lv.r[f] + Lv.r[f + 1] + Lv.r[f + Lv.nx] + Lv.r[f + Lv.nx + 1]); }
    this.vcycle(l + 1);
    for (let J = 0; J < C.ny; J++) for (let I = 0; I < C.nx; I++) { const f = 2 * J * Lv.nx + 2 * I, e = C.x[J * C.nx + I];
      Lv.x[f] += e; Lv.x[f + 1] += e; Lv.x[f + Lv.nx] += e; Lv.x[f + Lv.nx + 1] += e; }
    this.smooth(Lv, Lv.x, Lv.b, 2, 1);
  }
  precond(r, z) { const L0 = this.L[0]; L0.b.set(r); this.vcycle(0); z.set(L0.x); }
  solve(b, x, tol = this.tol || 1e-6, maxit = 100) {   // x holds the warm start; returns iterations
    const L0 = this.L[0], N = b.length, { rr, z, pp, Ap } = this;
    this.apply(L0, x, Ap); let bn = 0; for (let c = 0; c < N; c++) { rr[c] = L0.d[c] ? b[c] - Ap[c] : 0; bn += b[c] * b[c]; }
    bn = Math.sqrt(bn) || 1; this.precond(rr, z); pp.set(z); let rz = 0; for (let c = 0; c < N; c++) rz += rr[c] * z[c];
    for (let it = 0; it < maxit; it++) {
      let rn = 0; for (let c = 0; c < N; c++) rn += rr[c] * rr[c]; if (Math.sqrt(rn) < tol * bn) return it;
      this.apply(L0, pp, Ap); let pAp = 0; for (let c = 0; c < N; c++) pAp += pp[c] * Ap[c]; const a = rz / pAp;
      for (let c = 0; c < N; c++) { x[c] += a * pp[c]; rr[c] -= a * Ap[c]; }
      this.precond(rr, z); let rz2 = 0; for (let c = 0; c < N; c++) rz2 += rr[c] * z[c]; const bb = rz2 / rz; rz = rz2;
      for (let c = 0; c < N; c++) pp[c] = z[c] + bb * pp[c];
    }
    return maxit;
  }
}

// ---------- the coupled world ----------
class World {
  constructor(o) {
    Object.assign(this, { nx: 256, ny: 160, dx: 0.0125, x0: -1.6, y0: -0.75, rho: 1261, nu: 1.412 / 1261, U: 0, levels: 6 }, o);
    const { nx, ny } = this;
    this.u = new Float64Array((nx + 1) * ny); this.v = new Float64Array(nx * (ny + 1));
    this.wu = new Float64Array((nx + 1) * ny); this.wv = new Float64Array(nx * (ny + 1));   // fluid fraction of each face's staggered cell
    this.bu = new Int8Array((nx + 1) * ny); this.bv = new Int8Array(nx * (ny + 1));          // owner body of each face (-1 none)
    this.phi = new Float64Array(nx * ny); this.own = new Int8Array(nx * ny);
    this.Ju = new Float64Array((nx + 1) * ny * 3); this.Jv = new Float64Array(nx * (ny + 1) * 3);   // d(face velocity component)/d(qdot_i) of the owner body
    this.P = new Poisson(nx, ny, this.dx, this.levels);
    this.p = [0, 1, 2, 3].map(() => new Float64Array(nx * ny));   // p0, p1, p2, p3 (warm starts kept)
    this.rhs = new Float64Array(nx * ny); this.t = 0; this.its = [0, 0, 0, 0];
    this.u.fill(this.U);
  }
  xu(i) { return this.x0 + i * this.dx; } yu(j) { return this.y0 + (j + 0.5) * this.dx; }
  xv(i) { return this.x0 + (i + 0.5) * this.dx; } yv(j) { return this.y0 + j * this.dx; }
  xc(i) { return this.x0 + (i + 0.5) * this.dx; } yc(j) { return this.y0 + (j + 0.5) * this.dx; }
  // geometry: the machine provides sdf(k, x, y) and jac(k, x, y) -> [[dux/dq0, duy/dq0], [.. q1], [.. q2]]
  measure(mach) {
    const { nx, ny } = this, K = mach.nb;
    const pad = 3 * this.dx, bb = [];
    for (let k = 0; k < K; k++) bb.push(mach.bbox ? mach.bbox(k) : [-1e9, 1e9, -1e9, 1e9]);
    const near = (x, y) => { for (let k = 0; k < K; k++) { const B = bb[k]; if (x > B[0] - pad && x < B[1] + pad && y > B[2] - pad && y < B[3] + pad) return true; } return false; };
    this._near = near;
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const x = this.xc(i), y = this.yc(j); let best = 1e9, bk = -1;
      if (near(x, y)) for (let k = 0; k < K; k++) { const d = mach.sdf(k, x, y); if (d < best) { best = d; bk = k; } }
      this.phi[j * nx + i] = best; this.own[j * nx + i] = bk; }
    const face = (x, y, comp, wSeg, Wout, Bout, Jout, idx) => {
      Wout[idx] = 1 - wSeg; let best = 1e9, bk = -1;
      if (!near(x, y)) { Bout[idx] = -1; Jout[idx * 3] = Jout[idx * 3 + 1] = Jout[idx * 3 + 2] = 0; return; }
      for (let k = 0; k < K; k++) { const d = mach.sdf(k, x, y); if (d < best) { best = d; bk = k; } }
      if (wSeg > 0 || best < 2 * this.dx) { Bout[idx] = bk; const J = mach.jac(bk, x, y); for (let q = 0; q < 3; q++) Jout[idx * 3 + q] = J[q][comp]; }
      else { Bout[idx] = -1; Jout[idx * 3] = Jout[idx * 3 + 1] = Jout[idx * 3 + 2] = 0; }
    };
    for (let j = 0; j < ny; j++) for (let i = 0; i <= nx; i++) { const idx = j * (nx + 1) + i;
      const a = i > 0 ? this.phi[j * nx + i - 1] : this.phi[j * nx + i], b = i < nx ? this.phi[j * nx + i] : this.phi[j * nx + i - 1];
      face(this.xu(i), this.yu(j), 0, fracInside(a, b), this.wu, this.bu, this.Ju, idx); }
    for (let j = 0; j <= ny; j++) for (let i = 0; i < nx; i++) { const idx = j * nx + i;
      const a = j > 0 ? this.phi[(j - 1) * nx + i] : this.phi[j * nx + i], b = j < ny ? this.phi[j * nx + i] : this.phi[(j - 1) * nx + i];
      face(this.xv(i), this.yv(j), 1, fracInside(a, b), this.wv, this.bv, this.Jv, idx); }
    // domain edges: left inflow and top/bottom walls are Neumann (weight 0 in the Poisson matrix); right edge outflow, Dirichlet p = 0
    const wx = new Float64Array(this.wu), wy = new Float64Array(this.wv);
    for (let j = 0; j < ny; j++) { wx[j * (nx + 1)] = 0; }
    for (let i = 0; i < nx; i++) { wy[i] = 0; wy[ny * nx + i] = 0; }
    this.wx = wx; this.wy = wy; this.P.setWeights(wx, wy);
  }
  bodyVel(qd) {   // face velocity of the owner body, for faces near or inside bodies
    const { nx, ny } = this;
    const fu = (idx) => this.Ju[idx * 3] * qd[0] + this.Ju[idx * 3 + 1] * qd[1] + this.Ju[idx * 3 + 2] * qd[2];
    const fv = (idx) => this.Jv[idx * 3] * qd[0] + this.Jv[idx * 3 + 1] * qd[1] + this.Jv[idx * 3 + 2] * qd[2];
    return { fu, fv };
  }
  sampleU(x, y) { const { nx, ny, dx } = this; let fx = (x - this.x0) / dx, fy = (y - this.y0) / dx - 0.5;
    fx = Math.min(Math.max(fx, 0), nx - 1e-9); fy = Math.min(Math.max(fy, 0), ny - 1 - 1e-9); const i = fx | 0, j = fy | 0, a = fx - i, b = fy - j, u = this.u, W = nx + 1;
    return (1 - a) * (1 - b) * u[j * W + i] + a * (1 - b) * u[j * W + i + 1] + (1 - a) * b * u[(j + 1) * W + i] + a * b * u[(j + 1) * W + i + 1]; }
  sampleV(x, y) { const { nx, ny, dx } = this; let fx = (x - this.x0) / dx - 0.5, fy = (y - this.y0) / dx;
    fx = Math.min(Math.max(fx, 0), nx - 1 - 1e-9); fy = Math.min(Math.max(fy, 0), ny - 1e-9); const i = fx | 0, j = fy | 0, a = fx - i, b = fy - j, v = this.v, W = nx;
    return (1 - a) * (1 - b) * v[j * W + i] + a * (1 - b) * v[j * W + i + 1] + (1 - a) * b * v[(j + 1) * W + i] + a * b * v[(j + 1) * W + i + 1]; }
  advect(dt) {   // MacCormack: forward semi-Lagrangian, backward check, half the error added back, clamped to the local extrema
    const { nx, ny, dx, x0, y0 } = this, Wu = nx + 1, u0 = this._u0 || (this._u0 = new Float64Array(this.u.length)), v0 = this._v0 || (this._v0 = new Float64Array(this.v.length));
    u0.set(this.u); v0.set(this.v);
    const uF = this._uF || (this._uF = new Float64Array(this.u.length)), vF = this._vF || (this._vF = new Float64Array(this.v.length));
    const ix = 1 / dx;
    // bilinear samplers on the staggered arrays, in grid units
    const sU = (A, gx, gy) => { if (gx < 0) gx = 0; else if (gx > nx - 1e-9) gx = nx - 1e-9; if (gy < 0) gy = 0; else if (gy > ny - 1 - 1e-9) gy = ny - 1 - 1e-9;
      const i = gx | 0, j = gy | 0, a = gx - i, b = gy - j, c = j * Wu + i; return (1 - b) * ((1 - a) * A[c] + a * A[c + 1]) + b * ((1 - a) * A[c + Wu] + a * A[c + Wu + 1]); };
    const sV = (A, gx, gy) => { if (gx < 0) gx = 0; else if (gx > nx - 1 - 1e-9) gx = nx - 1 - 1e-9; if (gy < 0) gy = 0; else if (gy > ny - 1e-9) gy = ny - 1e-9;
      const i = gx | 0, j = gy | 0, a = gx - i, b = gy - j, c = j * nx + i; return (1 - b) * ((1 - a) * A[c] + a * A[c + 1]) + b * ((1 - a) * A[c + nx] + a * A[c + nx + 1]); };
    // velocity at a point given in grid units of the cell-corner frame (x = x0 + X dx): u-grid (X, Y-0.5), v-grid (X-0.5, Y)
    let PX = 0, PY = 0;
    const trace = (X, Y, h) => {   // midpoint rule with the frozen field (u0, v0); h = dt / dx, signed
      const ux = sU(u0, X, Y - 0.5), uy = sV(v0, X - 0.5, Y), Xm = X - 0.5 * h * ux, Ym = Y - 0.5 * h * uy;
      PX = X - h * sU(u0, Xm, Ym - 0.5); PY = Y - h * sV(v0, Xm - 0.5, Ym); };
    const h = dt * ix;
    for (let j = 0; j < ny; j++) for (let i = 1; i < nx; i++) { trace(i, j + 0.5, h); uF[j * Wu + i] = sU(u0, PX, PY - 0.5); }
    for (let j = 1; j < ny; j++) for (let i = 0; i < nx; i++) { trace(i + 0.5, j, h); vF[j * nx + i] = sV(v0, PX - 0.5, PY); }
    for (let j = 0; j < ny; j++) for (let i = 1; i < nx; i++) { const c = j * Wu + i;
      trace(i, j + 0.5, -h); const back = sU(uF, PX, PY - 0.5); let val = uF[c] + 0.5 * (u0[c] - back);
      trace(i, j + 0.5, h); let gx = PX, gy = PY - 0.5; if (gx < 0) gx = 0; else if (gx > nx - 1e-9) gx = nx - 1e-9; if (gy < 0) gy = 0; else if (gy > ny - 1 - 1e-9) gy = ny - 1 - 1e-9;
      const ii = gx | 0, jj = gy | 0, k = jj * Wu + ii, A = u0[k], B = u0[k + 1], C = u0[k + Wu], D = u0[k + Wu + 1];
      const lo = Math.min(A, B, C, D), hi = Math.max(A, B, C, D); this.u[c] = (val < lo || val > hi) ? uF[c] : val; }
    for (let j = 1; j < ny; j++) for (let i = 0; i < nx; i++) { const c = j * nx + i;
      trace(i + 0.5, j, -h); const back = sV(vF, PX - 0.5, PY); let val = vF[c] + 0.5 * (v0[c] - back);
      trace(i + 0.5, j, h); let gx = PX - 0.5, gy = PY; if (gx < 0) gx = 0; else if (gx > nx - 1 - 1e-9) gx = nx - 1 - 1e-9; if (gy < 0) gy = 0; else if (gy > ny - 1e-9) gy = ny - 1e-9;
      const ii = gx | 0, jj = gy | 0, k = jj * nx + ii, A = v0[k], B = v0[k + 1], C = v0[k + nx], D = v0[k + nx + 1];
      const lo = Math.min(A, B, C, D), hi = Math.max(A, B, C, D); this.v[c] = (val < lo || val > hi) ? vF[c] : val; }
    for (let j = 0; j < ny; j++) { this.u[j * Wu] = this.U; this.u[j * Wu + nx] = this.u[j * Wu + nx - 1]; }   // inflow U, outflow copied
    for (let i = 0; i < nx; i++) { this.v[i] = 0; this.v[ny * nx + i] = 0; }
  }
  imposeBody(qd) {   // faces whose staggered cell is mostly solid carry the body's velocity (no-slip for the viscous step, and the advection's interior)
    const { nx, ny } = this, { fu, fv } = this.bodyVel(qd);
    for (let c = 0; c < this.u.length; c++) if (this.bu[c] >= 0 && this.wu[c] <= 0) this.u[c] = fu(c);
    for (let c = 0; c < this.v.length; c++) if (this.bv[c] >= 0 && this.wv[c] <= 0) this.v[c] = fv(c);
  }
  diffuse(dt, qd) {   // explicit viscosity, substepped for stability, body faces held at the body velocity
    const { nx, ny, dx, nu } = this; if (!nu) return;
    const n = Math.max(1, Math.ceil(nu * dt / (0.2 * dx * dx))), h = dt / n, a = nu * h / (dx * dx);
    for (let s = 0; s < n; s++) {
      const u0 = Float64Array.from(this.u), v0 = Float64Array.from(this.v), W = nx + 1;
      for (let j = 0; j < ny; j++) for (let i = 1; i < nx; i++) { const c = j * W + i; if (this.bu[c] >= 0 && this.wu[c] <= 0) continue;
        const up = j < ny - 1 ? u0[c + W] : u0[c], dn = j > 0 ? u0[c - W] : u0[c]; this.u[c] = u0[c] + a * (u0[c - 1] + u0[c + 1] + up + dn - 4 * u0[c]); }
      for (let j = 1; j < ny; j++) for (let i = 0; i < nx; i++) { const c = j * nx + i; if (this.bv[c] >= 0 && this.wv[c] <= 0) continue;
        const lf = i > 0 ? v0[c - 1] : v0[c], rt = i < nx - 1 ? v0[c + 1] : v0[c]; this.v[c] = v0[c] + a * (lf + rt + v0[c + nx] + v0[c - nx] - 4 * v0[c]); }
      this.imposeBody(qd);
    }
  }
  // divergence of (w u + (1 - w) v_body) split into the fluid part and the three unit-velocity parts
  rhsFluid(out) { const { nx, ny, dx } = this, W = nx + 1;
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const c = j * nx + i;
      out[c] = -((this.wu[j * W + i + 1] * this.u[j * W + i + 1] - this.wu[j * W + i] * this.u[j * W + i]) + (this.wv[(j + 1) * nx + i] * this.v[(j + 1) * nx + i] - this.wv[j * nx + i] * this.v[j * nx + i])) / dx; } }
  rhsBody(q, out) { const { nx, ny, dx } = this, W = nx + 1;
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const c = j * nx + i;
      const ue = (1 - this.wu[j * W + i + 1]) * this.Ju[(j * W + i + 1) * 3 + q], uw = (1 - this.wu[j * W + i]) * this.Ju[(j * W + i) * 3 + q];
      const vn = (1 - this.wv[(j + 1) * nx + i]) * this.Jv[((j + 1) * nx + i) * 3 + q], vs = (1 - this.wv[j * nx + i]) * this.Jv[(j * nx + i) * 3 + q];
      out[c] = -((ue - uw) + (vn - vs)) / dx; } }
  // generalized force of a pressure field on the machine: Q_q = -sum_faces b_owner * vol * (dp/dn) * J_q, vol = (1 - w) dx^2 per metre of depth
  genForce(p, depth) { const { nx, ny, dx } = this, W = nx + 1, Q = [0, 0, 0], per = [[0, 0], [0, 0], [0, 0]];
    for (let j = 0; j < ny; j++) for (let i = 1; i < nx; i++) { const f = j * W + i, k = this.bu[f]; if (k < 0) continue; const s = 1 - this.wu[f]; if (s <= 0) continue;
      const g = (p[j * nx + i] - p[j * nx + i - 1]) / dx, fx = -depth[k] * s * dx * dx * g;
      for (let q = 0; q < 3; q++) Q[q] += fx * this.Ju[f * 3 + q]; per[k][0] += fx; }
    for (let j = 1; j < ny; j++) for (let i = 0; i < nx; i++) { const f = j * nx + i, k = this.bv[f]; if (k < 0) continue; const s = 1 - this.wv[f]; if (s <= 0) continue;
      const g = (p[j * nx + i] - p[(j - 1) * nx + i]) / dx, fy = -depth[k] * s * dx * dx * g;
      for (let q = 0; q < 3; q++) Q[q] += fy * this.Jv[f * 3 + q]; per[k][1] += fy; }
    return { Q, per };
  }
  project(p, dt) { const { nx, ny, dx, rho } = this, W = nx + 1, s = dt / (rho * dx);
    for (let j = 0; j < ny; j++) for (let i = 1; i <= nx; i++) { const c = j * W + i; if (this.wx[c] <= 0) continue; const pr = i < nx ? p[j * nx + i] : 0; this.u[c] -= s * (pr - p[j * nx + i - 1]); }
    for (let j = 1; j < ny; j++) for (let i = 0; i < nx; i++) { const c = j * nx + i; if (this.wy[c] <= 0) continue; this.v[c] -= s * (p[j * nx + i] - p[(j - 1) * nx + i]); } }
  // one coupled step: machine m provides state, mass matrix, forces; returns diagnostics
  step(m, dt, uMotor) {
    const sc = this.rho * this.dx * this.dx / dt;   // Poisson solved with weights / dx^2; scale rhs to pressure units: A p = rho/dt * rhs_div
    m.pose(); this.measure(m);
    this.imposeBody(m.qd);
    this.advect(dt);
    this.imposeBody(m.qd);
    this.diffuse(dt, m.qd);
    // pressure: p = p0 + sum qdot'_i p_i
    const f = this.rho / dt;
    this.rhsFluid(this.rhs); for (let c = 0; c < this.rhs.length; c++) this.rhs[c] *= f; this.its[0] = this.P.solve(this.rhs, this.p[0]);
    for (let q = 0; q < 3; q++) { this.rhsBody(q, this.rhs); for (let c = 0; c < this.rhs.length; c++) this.rhs[c] *= f; this.its[q + 1] = this.P.solve(this.rhs, this.p[q + 1]); }
    const F0 = this.genForce(this.p[0], m.depth), Kc = [0, 1, 2].map(q => this.genForce(this.p[q + 1], m.depth));
    const K = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]; for (let a = 0; a < 3; a++) for (let b = 0; b < 3; b++) K[a][b] = Kc[b].Q[a];
    const qdNew = m.implicitStep(dt, uMotor, F0.Q, K);
    // fluid velocity with the final pressure, body faces with the new body velocity
    const p = new Float64Array(this.p[0]); for (let q = 0; q < 3; q++) for (let c = 0; c < p.length; c++) p[c] += qdNew[q] * this.p[q + 1][c];
    this.project(p, dt);
    this.pFinal = p;
    { const { nx, ny, dx } = this, Wd = nx + 1, { fu, fv } = this.bodyVel(qdNew); let mx = 0;
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const c = j * nx + i; if (this.P.L[0].d[c] === 0) continue;
        const fl = (k, w, uu) => w * uu, e = j * Wd + i + 1, ww = j * Wd + i, n2 = (j + 1) * nx + i, s2 = j * nx + i;
        const d = ((this.wu[e] * this.u[e] + (1 - this.wu[e]) * fu(e)) - (this.wu[ww] * this.u[ww] + (1 - this.wu[ww]) * fu(ww))
                 + (this.wv[n2] * this.v[n2] + (1 - this.wv[n2]) * fv(n2)) - (this.wv[s2] * this.v[s2] + (1 - this.wv[s2]) * fv(s2))) / dx;
        if (Math.abs(d) > mx) mx = Math.abs(d); }
      this.divAfter = mx; }
    const Qf = [0, 1, 2].map(a => F0.Q[a] + K[a][0] * qdNew[0] + K[a][1] * qdNew[1] + K[a][2] * qdNew[2]);
    const per = F0.per.map((v, k) => [v[0] + Kc[0].per[k][0] * qdNew[0] + Kc[1].per[k][0] * qdNew[1] + Kc[2].per[k][0] * qdNew[2], v[1] + Kc[0].per[k][1] * qdNew[0] + Kc[1].per[k][1] * qdNew[1] + Kc[2].per[k][1] * qdNew[2]]);
    m.advance(dt, qdNew);
    this.imposeBody(m.qd);
    this.t += dt;
    return { Q: Qf, K, per, its: this.its.slice(), div: this.divAfter };
  }
  maxDiv() { const { nx, ny, dx } = this, W = nx + 1; let mx = 0; const qd = this._qd || [0, 0, 0];
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const c = j * nx + i; if (this.P.L[0].d[c] === 0) continue;
      const d = ((this.wu[j * W + i + 1] * this.u[j * W + i + 1] - this.wu[j * W + i] * this.u[j * W + i]) + (this.wv[(j + 1) * nx + i] * this.v[(j + 1) * nx + i] - this.wv[j * nx + i] * this.v[j * nx + i])) / dx;
      mx = Math.max(mx, Math.abs(d)); } return mx; }
}

// ---------- project 05's machine in the 2D world ----------
class Machine {
  constructor(o) {
    Object.assign(this, { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, w: 0.02, cw: 0.36, ch: 0.12, depth: [0.2, 0.02, 0.02], rho: 1261, g: 9.81,
      K: [5.885587698152317, -297.35065624888904, 376.94950633324845, 16.857296568025124, -11.85241735175428, 89.41084011288147], umax: 60, Ts: 0.01 }, o);
    this.q = [0, 0, 0]; this.qd = [0, 0, 0]; this.nb = 3;
  }
  d() { const { m0, m1, m2, L1, L2 } = this; return [m0 + m1 + m2, (m1 / 2 + m2) * L1, m2 * L2 / 2, (m1 / 3 + m2) * L1 * L1, m2 * L1 * L2 / 2, m2 * L2 * L2 / 3]; }
  f() { const { m1, m2, L1, L2, g, rho, w, depth } = this, bA1 = rho * w * depth[1] * g, bA2 = rho * w * depth[2] * g;   // weight minus buoyancy of the 2D rods
    return [(m1 / 2 + m2) * L1 * g - bA1 * L1 * L1 / 2 - bA2 * L1 * L2, m2 * L2 * g / 2 - bA2 * L2 * L2 / 2]; }
  pose() { const [x, a, b] = this.q; this.hinge = [x, 0]; this.elbow = [x + this.L1 * Math.sin(a), this.L1 * Math.cos(a)]; this.ca = Math.cos(a); this.sa = Math.sin(a); this.cb = Math.cos(b); this.sb = Math.sin(b); }
  sdf(k, X, Y) {
    if (k === 0) { const qx = Math.abs(X - this.q[0]) - this.cw / 2, qy = Math.abs(Y + this.ch / 2) - this.ch / 2; return Math.hypot(Math.max(qx, 0), Math.max(qy, 0)) + Math.min(Math.max(qx, qy), 0); }
    const [hx, hy] = k === 1 ? this.hinge : this.elbow, L = k === 1 ? this.L1 : this.L2, s = k === 1 ? this.sa : this.sb, c = k === 1 ? this.ca : this.cb;
    const dx = X - hx, dy = Y - hy, t = Math.min(Math.max(dx * s + dy * c, 0), L); return Math.hypot(dx - t * s, dy - t * c) - this.w / 2;
  }
  bbox(k) { if (k === 0) return [this.q[0] - this.cw / 2, this.q[0] + this.cw / 2, -this.ch, 0];
    const [hx, hy] = k === 1 ? this.hinge : this.elbow, L = k === 1 ? this.L1 : this.L2, s = k === 1 ? this.sa : this.sb, c = k === 1 ? this.ca : this.cb, r = this.w / 2;
    return [Math.min(hx, hx + L * s) - r, Math.max(hx, hx + L * s) + r, Math.min(hy, hy + L * c) - r, Math.max(hy, hy + L * c) + r]; }
  jac(k, X, Y) {   // rows: d(point velocity)/d(xdot), d/d(th1dot), d/d(th2dot)
    if (k === 0) return [[1, 0], [0, 0], [0, 0]];
    if (k === 1) { const [hx, hy] = this.hinge; return [[1, 0], [Y - hy, -(X - hx)], [0, 0]]; }
    const [ex, ey] = this.elbow; return [[1, 0], [this.L1 * this.ca, -this.L1 * this.sa], [Y - ey, -(X - ex)]];
  }
  implicitStep(dt, u, Q0, K) {   // (D - dt K) qd' = D qd + dt (H u - C qd^2 - G + Q0)
    const [x, a, b] = this.q, [xd, ad, bd] = this.qd, d = this.d(), f = this.f(), sab = Math.sin(a - b);
    const D = [[d[0], d[1] * Math.cos(a), d[2] * Math.cos(b)], [d[1] * Math.cos(a), d[3], d[4] * Math.cos(a - b)], [d[2] * Math.cos(b), d[4] * Math.cos(a - b), d[5]]];
    const Cq = [-d[1] * Math.sin(a) * ad * ad - d[2] * Math.sin(b) * bd * bd, d[4] * sab * bd * bd, -d[4] * sab * ad * ad], G = [0, -f[0] * Math.sin(a), -f[1] * Math.sin(b)];
    const A = D.map((r, i) => r.map((v, j) => v - dt * K[i][j])), rhs = [0, 1, 2].map(i => D[i][0] * xd + D[i][1] * ad + D[i][2] * bd + dt * ((i === 0 ? u : 0) - Cq[i] - G[i] + Q0[i]));
    return solve3(A, rhs);
  }
  advance(dt, qdNew) { this.qd = qdNew; for (let i = 0; i < 3; i++) this.q[i] += dt * qdNew[i]; }
  control(sref) { const s = [...this.q, ...this.qd]; let u = 0; for (let i = 0; i < 6; i++) u -= this.K[i] * (s[i] - sref[i]); return Math.max(-this.umax, Math.min(this.umax, u)); }
}
function solve3(A, b) { const M = A.map((r, i) => [...r, b[i]]);
  for (let c = 0; c < 3; c++) { let p = c; for (let r = c + 1; r < 3; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r; [M[c], M[p]] = [M[p], M[c]];
    for (let r = 0; r < 3; r++) if (r !== c) { const f = M[r][c] / M[c][c]; for (let k = c; k < 4; k++) M[r][k] -= f * M[c][k]; } }
  return [M[0][3] / M[0][0], M[1][3] / M[1][1], M[2][3] / M[2][2]]; }

module.exports = { World, Machine, Poisson, fracInside, solve3 };
