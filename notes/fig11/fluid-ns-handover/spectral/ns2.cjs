// 2D incompressible Navier-Stokes on a periodic box, vorticity state, Fourier pseudo-spectral (2/3 dealiasing).
// One step:  (1) SSP-RK3 with exact viscous integrating factor for  d(omega)/dt = curl(u x omega)  (bodies absent);
//            (2) implicit Brinkman penalization and velocity sponge, pointwise in velocity (backward Euler):
//                u_pen = (u + lam*sum_j chi_j u_sj + lsp*sp*u_target) / (1 + lam*sum_j chi_j + lsp*sp),  lam = dt/eta;
//                the change u_pen - u is returned to omega through its curl, i.e. projected (pressure enforces div u = 0).
// Force of the fluid on body j, per unit depth and unit density (Engels et al. 2013, eq. 4):
//                F_j = int chi_j/eta (u_pen - u_sj) dA + d/dt int_{body} u_sj dA.
'use strict';
const { makeFFT } = require('./ns.cjs');

class NS {
  constructor(o) {
    Object.assign(this, { N: 256, M: 256, Lx: 1, Ly: 1, nu: 1e-3, eta: 1e-4, etaSp: 1e-3, cfl: 0.8, dtMax: 1e-2, mix: false }, o);
    const N = this.N, M = this.M, NM = N * M;
    this.dx = this.Lx / N; this.dy = this.Ly / M; this.dA = this.dx * this.dy;
    this.fx = makeFFT(N); this.fy = M === N ? this.fx : makeFFT(M);
    this.kx = new Float64Array(N); this.ky = new Float64Array(M);
    for (let i = 0; i < N; i++) this.kx[i] = 2 * Math.PI / this.Lx * (i <= N / 2 ? i : i - N);
    for (let j = 0; j < M; j++) this.ky[j] = 2 * Math.PI / this.Ly * (j <= M / 2 ? j : j - M);
    this.k2 = new Float64Array(NM); this.deal = new Float64Array(NM);
    for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) {
      const p = j * N + i; this.k2[p] = this.kx[i] ** 2 + this.ky[j] ** 2;
      this.deal[p] = (Math.min(i, N - i) < N / 3 && Math.min(j, M - j) < M / 3) ? 1 : 0;
    }
    const A = () => new Float64Array(NM);
    Object.assign(this, { wr: A(), wi: A(), r0: A(), i0: A(), r1: A(), i1: A(), nr: A(), ni: A(), ar: A(), ai: A(), br: A(), bi: A(),
      u: A(), v: A(), w: A(), sp: A(), tx: A(), ty: A() });
    this.Ux = 0; this.Uy = 0; this.t = 0; this.bodies = [];
  }
  fft2(re, im, inv) { const N = this.N, M = this.M; for (let j = 0; j < M; j++) this.fx(re, im, j * N, 1, inv); for (let i = 0; i < N; i++) this.fy(re, im, i, N, inv); }
  setOmega(f) {
    const N = this.N, M = this.M;
    for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) { const p = j * N + i; this.wr[p] = f(this.X(i), this.Y(j)); this.wi[p] = 0; }
    this.fft2(this.wr, this.wi, false); for (let p = 0; p < N * M; p++) { this.wr[p] *= this.deal[p]; this.wi[p] *= this.deal[p]; } this.wr[0] = this.wi[0] = 0;
  }
  X(i) { return (i + 0.5) * this.dx; } Y(j) { return (j + 0.5) * this.dy; }
  velocity(wr, wi) {   // omega-hat -> physical u, v (with the mean) and omega
    const N = this.N, M = this.M, ar = this.ar, ai = this.ai, br = this.br, bi = this.bi;
    for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) {
      const p = j * N + i, k2 = this.k2[p]; if (k2 === 0) { ar[p] = ai[p] = br[p] = bi[p] = 0; continue; }
      const pr = wr[p] / k2, pi = wi[p] / k2, kx = this.kx[i], ky = this.ky[j];
      const uR = -ky * pi, uI = ky * pr, vR = kx * pi, vI = -kx * pr;
      ar[p] = uR - vI; ai[p] = uI + vR; br[p] = wr[p]; bi[p] = wi[p];
    }
    this.fft2(ar, ai, true); this.fft2(br, bi, true);
    for (let p = 0; p < N * M; p++) { this.u[p] = ar[p] + this.Ux; this.v[p] = ai[p] + this.Uy; this.w[p] = br[p]; }
  }
  curlOf(fx, fy, outR, outI, add, nodeal) {   // out (+)= dealiased hat of curl(f) = i kx fy - i ky fx
    const N = this.N, M = this.M, ar = this.ar, ai = this.ai;
    for (let p = 0; p < N * M; p++) { ar[p] = fx[p]; ai[p] = fy[p]; }
    this.fft2(ar, ai, false);
    for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) {
      const p = j * N + i, q = ((M - j) % M) * N + ((N - i) % N);
      const FxR = 0.5 * (ar[p] + ar[q]), FxI = 0.5 * (ai[p] - ai[q]), FyR = 0.5 * (ai[p] + ai[q]), FyI = -0.5 * (ar[p] - ar[q]);
      const kx = this.kx[i], ky = this.ky[j], d = nodeal ? 1 : this.deal[p], cr = d * (-kx * FyI + ky * FxI), ci = d * (kx * FyR - ky * FxR);
      if (add) { outR[p] += cr; outI[p] += ci; } else { outR[p] = cr; outI[p] = ci; }
    }
  }
  adv(wr, wi, outR, outI, book) {   // N-hat = curl(u x omega) = curl(v w, -u w); with inRhs also minus the penalization and sponge forces (K&S 2009, eq. 8)
    this.velocity(wr, wi); const NM = this.N * this.M;
    if (!this.inRhs) { for (let p = 0; p < NM; p++) { this.tx[p] = this.v[p] * this.w[p]; this.ty[p] = -this.u[p] * this.w[p]; } }
    else {
      const ie = 1 / this.eta, isp = 1 / this.etaSp, N = this.N, M = this.M;
      if (book) for (const b of this.bodies) { b._Fx = 0; b._Fy = 0; b._Mz = 0; }
      for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) { const p = j * N + i, u = this.u[p], v = this.v[p], w = this.w[p]; let px = 0, py = 0;
        for (const b of this.bodies) { const ch = b.chi[p]; if (ch > 0) { const fx = ch * ie * (u - b.usx[p]), fy = ch * ie * (v - b.usy[p]); px += fx; py += fy;
          if (book) { b._Fx += fx; b._Fy += fy; b._Mz += (this.X(i) - b.xc) * fy - (this.Y(j) - b.yc) * fx; } } }
        const sp = this.sp[p]; let sx = 0, sy = 0; if (sp) { sx = sp * isp * (u - this.Ux - this.tgx[p]); sy = sp * isp * (v - this.Uy - this.tgy[p]); }
        this.tx[p] = v * w - px - sx; this.ty[p] = -u * w - py - sy; }
      if (book) for (const b of this.bodies) b.Fpen = [b._Fx * this.dA, b._Fy * this.dA, b._Mz * this.dA];   // force of the fluid on the body, per unit density and depth (K&S eq. 6, first term)
    }
    this.curlOf(this.tx, this.ty, outR, outI, false);
  }
  maxSpeed() { let m = 1e-12; for (let p = 0; p < this.N * this.M; p++) { const s = Math.abs(this.u[p]) / this.dx + Math.abs(this.v[p]) / this.dy; if (s > m) m = s; } return m; }
  step(dt) {
    const NM = this.N * this.M, nu = this.nu, k2 = this.k2;
    const E = (tau, p) => Math.exp(-nu * k2[p] * tau);
    // SSP-RK3 in the integrating-factor variable
    if (this.inRhs) for (const b of this.bodies) b.update(this.t, this);   // masks and body velocities at the start of the step
    this.adv(this.wr, this.wi, this.nr, this.ni, true);
    if (dt === undefined) dt = Math.min(this.dtMax, this.cfl / this.maxSpeed());
    if (this.inRhs) dt = Math.min(dt, 2 * this.eta);   // explicit penalization: RK3 stable for dt/eta < 2.51
    for (let p = 0; p < NM; p++) { const e = E(dt, p); this.r0[p] = e * (this.wr[p] + dt * this.nr[p]); this.i0[p] = e * (this.wi[p] + dt * this.ni[p]); }
    this.adv(this.r0, this.i0, this.nr, this.ni);
    for (let p = 0; p < NM; p++) { const a = E(dt / 2, p), b = E(-dt / 2, p);
      this.r1[p] = 0.75 * a * this.wr[p] + 0.25 * b * (this.r0[p] + dt * this.nr[p]); this.i1[p] = 0.75 * a * this.wi[p] + 0.25 * b * (this.i0[p] + dt * this.ni[p]); }
    this.adv(this.r1, this.i1, this.nr, this.ni);
    for (let p = 0; p < NM; p++) { const a = E(dt, p), b = E(dt / 2, p);
      this.wr[p] = (a * this.wr[p] + 2 * b * (this.r1[p] + dt * this.nr[p])) / 3; this.wi[p] = (a * this.wi[p] + 2 * b * (this.i1[p] + dt * this.ni[p])) / 3; }
    this.t += dt;
    if (!this.inRhs) this.penalize(dt);
    else for (const b of this.bodies) {   // the inertia of the fluid the body holds, d/dt of int chi u_s dA (K&S eq. 6, second term)
      let Px = 0, Py = 0; for (let p = 0; p < NM; p++) { const ch = b.chi[p]; if (ch > 0) { Px += ch * b.usx[p]; Py += ch * b.usy[p]; } }
      const P = [Px * this.dA, Py * this.dA]; b.Fin = b.Pprev ? [(P[0] - b.Pprev[0]) / dt, (P[1] - b.Pprev[1]) / dt] : [0, 0]; b.Pprev = P;
      b.F = [b.Fpen[0] + b.Fin[0], b.Fpen[1] + b.Fin[1]]; }
    return dt;
  }
  penalize(dt) {   // backward-Euler penalization of every body and the sponge at the new time; books the forces
    const NM = this.N * this.M, lam = dt / this.eta, lsp = dt / this.etaSp;
    this.velocity(this.wr, this.wi);
    for (const b of this.bodies) b.update(this.t, this);         // body fills b.chi, b.usx, b.usy at time t
    const du = this.tx, dv = this.ty;
    let num, den;
    for (let p = 0; p < NM; p++) {
      let cx = 0, cy = 0, c = 0;
      for (const b of this.bodies) { const ch = b.chi[p]; if (ch > 0) { c += ch; cx += ch * b.usx[p]; cy += ch * b.usy[p]; } }
      const s = this.sp[p], sx = s ? s * (this.Ux + this.tgx[p]) : 0, sy = s ? s * (this.Uy + this.tgy[p]) : 0;
      let up, vp;
      if (this.mix) {   // volume-fraction mixing (BDIM, zeroth order): u <- (1 - chi) u + sum chi_j u_sj, then the sponge
        const cc = Math.min(1, c), sc = c > 1 ? 1 / c : 1, u1 = (1 - cc) * this.u[p] + sc * cx, v1 = (1 - cc) * this.v[p] + sc * cy;
        for (const b of this.bodies) { const ch = b.chi[p] * sc; if (ch > 0) { b.fx[p] = ch * (this.u[p] - b.usx[p]) / dt; b.fy[p] = ch * (this.v[p] - b.usy[p]) / dt; } }
        const d2 = 1 + lsp * s; up = (u1 + lsp * sx) / d2; vp = (v1 + lsp * sy) / d2;
      } else if (this.expPen) {   // exact integration of du/dt = -sum chi_j/eta (u - u_sj) - sp/etaSp (u - u_t) over the step
        const K = lam * c + lsp * s;
        if (K > 0) { const tx = (lam * cx + lsp * sx) / K, ty = (lam * cy + lsp * sy) / K, e = Math.exp(-K), g = (1 - e) / K;
          up = tx + (this.u[p] - tx) * e; vp = ty + (this.v[p] - ty) * e;
          for (const b of this.bodies) { const ch = b.chi[p]; if (ch > 0) { b.fx[p] = lam * ch * g * (this.u[p] - b.usx[p]) / dt; b.fy[p] = lam * ch * g * (this.v[p] - b.usy[p]) / dt; } }
        } else { up = this.u[p]; vp = this.v[p]; }
      } else {
        den = 1 + lam * c + lsp * s;
        up = (this.u[p] + lam * cx + lsp * sx) / den; vp = (this.v[p] + lam * cy + lsp * sy) / den;
        for (const b of this.bodies) { const ch = b.chi[p]; if (ch > 0) { b.fx[p] = ch / this.eta * (up - b.usx[p]); b.fy[p] = ch / this.eta * (vp - b.usy[p]); } }
      }
      du[p] = up - this.u[p]; dv[p] = vp - this.v[p];
    }
    for (const b of this.bodies) {   // integrate the force density and its moment, and the momentum of the fluid the body holds
      let Fx = 0, Fy = 0, Mz = 0, Px = 0, Py = 0;
      for (let j = 0; j < this.M; j++) for (let i = 0; i < this.N; i++) { const p = j * this.N + i, ch = b.chi[p]; if (ch > 0) {
        Fx += b.fx[p]; Fy += b.fy[p]; Mz += (this.X(i) - b.xc) * b.fy[p] - (this.Y(j) - b.yc) * b.fx[p]; Px += ch * b.usx[p]; Py += ch * b.usy[p]; } }
      const dA = this.dA; b.Fpen = [Fx * dA, Fy * dA, Mz * dA];
      const P = [Px * dA, Py * dA];
      b.Fin = b.Pprev ? [(P[0] - b.Pprev[0]) / dt, (P[1] - b.Pprev[1]) / dt] : [0, 0]; b.Pprev = P;
      b.F = [b.Fpen[0] + b.Fin[0], b.Fpen[1] + b.Fin[1]];
    }
    this.curlOf(du, dv, this.wr, this.wi, true, this.penNoDeal);
  }
  setSponge(f) { const N = this.N, M = this.M; this.tgx = new Float64Array(N * M); this.tgy = new Float64Array(N * M);
    for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) { const p = j * N + i, r = f(this.X(i), this.Y(j)); this.sp[p] = r[0]; this.tgx[p] = r[1]; this.tgy[p] = r[2]; } }
}

// A rigid body from a signed distance d(x, y) (negative inside), with a smooth mask chi = erfc(d/delta)/2 (Engels et al. 2013, sec. 3.1.4).
function erfc(x) { const z = Math.abs(x), t = 1 / (1 + 0.5 * z), r = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277))))))))); return x >= 0 ? r : 2 - r; }
class Body {
  constructor(ns, o) { const NM = ns.N * ns.M; Object.assign(this, { xc: 0, yc: 0, th: 0, vx: 0, vy: 0, om: 0, delta: 1.0 * ns.dx, motion: null }, o);
    this.chi = new Float64Array(NM); this.usx = new Float64Array(NM); this.usy = new Float64Array(NM); this.fx = new Float64Array(NM); this.fy = new Float64Array(NM); }
  update(t, ns) {
    if (this.motion) this.motion(t, this);
    const N = ns.N, M = ns.M, c = Math.cos(this.th), s = Math.sin(this.th), cut = 4 * this.delta;
    for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) {
      const p = j * N + i; let X = ns.X(i) - this.xc, Y = ns.Y(j) - this.yc;
      if (this.periodic) { X -= ns.Lx * Math.round(X / ns.Lx); Y -= ns.Ly * Math.round(Y / ns.Ly); }
      const xl = c * X + s * Y, yl = -s * X + c * Y, d = this.sdf(xl, yl);
      if (d > cut) { this.chi[p] = 0; this.fx[p] = this.fy[p] = 0; continue; }
      this.chi[p] = this.ramp ? Math.min(1, Math.max(0, 0.5 - d / this.delta)) : 0.5 * erfc(d / this.delta);   // ramp: volume fraction of a cell cut by a straight wall
      this.usx[p] = this.vx - this.om * Y; this.usy[p] = this.vy + this.om * X;
    }
  }
}
module.exports = { NS, Body, erfc };
