// 2D incompressible Navier-Stokes, vorticity form, Fourier pseudo-spectral, Brinkman volume penalization
// (Kolomenskiy & Schneider 2009, eq. 8; Engels et al. 2013, eq. 5), velocity sponge, exact viscous factor, AB2.
// State: omega-hat on an N x M periodic grid of size Lx x Ly. Velocity u = curl(psi) + Uinf, omega = -lap(psi).
'use strict';

function makeFFT(n) {            // iterative radix-2 complex FFT, in place on (re, im) with stride
  const lg = Math.log2(n); if (lg % 1) throw new Error('n must be a power of 2');
  const rev = new Uint32Array(n); for (let i = 0; i < n; i++) { let r = 0, x = i; for (let b = 0; b < lg; b++) { r = (r << 1) | (x & 1); x >>= 1; } rev[i] = r; }
  const cs = new Float64Array(n / 2), sn = new Float64Array(n / 2);
  for (let i = 0; i < n / 2; i++) { cs[i] = Math.cos(2 * Math.PI * i / n); sn[i] = Math.sin(2 * Math.PI * i / n); }
  const tr = new Float64Array(n), ti = new Float64Array(n);
  return function (re, im, off, stride, inv) {
    for (let i = 0; i < n; i++) { const j = off + rev[i] * stride; tr[i] = re[j]; ti[i] = im[j]; }
    const sg = inv ? 1 : -1;
    for (let size = 2; size <= n; size <<= 1) {
      const half = size >> 1, step = n / size;
      for (let s = 0; s < n; s += size) for (let k = 0; k < half; k++) {
        const wr = cs[k * step], wi = sg * sn[k * step], a = s + k, b = a + half;
        const xr = tr[b] * wr - ti[b] * wi, xi = tr[b] * wi + ti[b] * wr;
        tr[b] = tr[a] - xr; ti[b] = ti[a] - xi; tr[a] += xr; ti[a] += xi;
      }
    }
    const sc = inv ? 1 / n : 1;
    for (let i = 0; i < n; i++) { const j = off + i * stride; re[j] = tr[i] * sc; im[j] = ti[i] * sc; }
  };
}

class Solver {
  constructor(o) {
    Object.assign(this, { N: 256, M: 256, Lx: 1, Ly: 1, nu: 1e-3, eta: 1e-3, etaSp: 1e-2, cfl: 0.2, dtMax: 1e-2 }, o);
    const N = this.N, M = this.M, NM = N * M;
    this.dx = this.Lx / N; this.dy = this.Ly / M;
    this.fx = makeFFT(N); this.fy = M === N ? this.fx : makeFFT(M);
    this.kx = new Float64Array(N); this.ky = new Float64Array(M);
    for (let i = 0; i < N; i++) this.kx[i] = 2 * Math.PI / this.Lx * (i <= N / 2 ? i : i - N);
    for (let j = 0; j < M; j++) this.ky[j] = 2 * Math.PI / this.Ly * (j <= M / 2 ? j : j - M);
    this.k2 = new Float64Array(NM); this.deal = new Float64Array(NM);
    for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) {
      const p = j * N + i; this.k2[p] = this.kx[i] ** 2 + this.ky[j] ** 2;
      this.deal[p] = (Math.abs(i <= N / 2 ? i : N - i) < N / 3 && Math.abs(j <= M / 2 ? j : M - j) < M / 3) ? 1 : 0;   // 2/3 rule
    }
    const A = () => new Float64Array(NM);
    this.wr = A(); this.wi = A();          // omega-hat
    this.nr = A(); this.ni = A();          // N-hat at the previous step (AB2)
    this.ar = A(); this.ai = A(); this.br = A(); this.bi = A();   // work
    this.u = A(); this.v = A(); this.w = A();                      // physical u, v, omega
    this.chi = A(); this.usx = A(); this.usy = A();                // total body mask and chi*u_s
    this.sp = A(); this.u0x = A(); this.u0y = A();                 // sponge mask, target perturbation velocity
    this.Px = A(); this.Py = A();                                  // penalization force density chi/eta (u - u_s), per unit density
    this.Ux = 0; this.Uy = 0;                                      // mean (irrotational) velocity Uinf(t)
    this.t = 0; this.dtPrev = 0; this.started = false; this.steps = 0;
  }
  fft2(re, im, inv) { const N = this.N, M = this.M; for (let j = 0; j < M; j++) this.fx(re, im, j * N, 1, inv); for (let i = 0; i < N; i++) this.fy(re, im, i, N, inv); }
  setOmega(f) {   // physical omega(x, y) -> omega-hat, dealiased, mean removed
    const N = this.N, M = this.M;
    for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) { const p = j * N + i; this.wr[p] = f((i + 0.5) * this.dx, (j + 0.5) * this.dy); this.wi[p] = 0; }
    this.fft2(this.wr, this.wi, false); for (let p = 0; p < N * M; p++) { this.wr[p] *= this.deal[p]; this.wi[p] *= this.deal[p]; } this.wr[0] = 0; this.wi[0] = 0;
    this.started = false;
  }
  velocity() {    // omega-hat -> physical u, v, omega (2 complex FFTs: u + i v packed, omega alone)
    const N = this.N, M = this.M, ar = this.ar, ai = this.ai, br = this.br, bi = this.bi;
    for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) {
      const p = j * N + i, k2 = this.k2[p]; if (k2 === 0) { ar[p] = ai[p] = 0; br[p] = bi[p] = 0; continue; }
      const pr = this.wr[p] / k2, pi = this.wi[p] / k2, kx = this.kx[i], ky = this.ky[j];   // psi-hat = omega-hat/k^2
      // u-hat = i ky psi, v-hat = -i kx psi;  pack z = u + i v  ->  z-hat = u-hat + i v-hat
      const uR = -ky * pi, uI = ky * pr, vR = kx * pi, vI = -kx * pr;
      ar[p] = uR - vI; ai[p] = uI + vR;
      br[p] = this.wr[p]; bi[p] = this.wi[p];
    }
    this.fft2(ar, ai, true); this.fft2(br, bi, true);
    for (let p = 0; p < N * M; p++) { this.u[p] = ar[p] + this.Ux; this.v[p] = ai[p] + this.Uy; this.w[p] = br[p]; }
  }
  rhs(outR, outI) {   // N-hat = curl( u x omega - chi/eta (u - u_s) - sp/etaSp (u - Uinf - u0) ), dealiased
    const N = this.N, M = this.M, ar = this.ar, ai = this.ai, ie = 1 / this.eta, isp = 1 / this.etaSp;
    this.velocity();
    for (let p = 0; p < N * M; p++) {
      const u = this.u[p], v = this.v[p], w = this.w[p];
      const px = (this.chi[p] * u - this.usx[p]) * ie, py = (this.chi[p] * v - this.usy[p]) * ie;   // usx holds chi*u_s
      this.Px[p] = px; this.Py[p] = py;
      const sx = this.sp[p] * (u - this.Ux - this.u0x[p]) * isp, sy = this.sp[p] * (v - this.Uy - this.u0y[p]) * isp;
      ar[p] = v * w - px - sx; ai[p] = -u * w - py - sy;
    }
    this.fft2(ar, ai, false);
    for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) {
      const p = j * N + i, q = ((M - j) % M) * N + ((N - i) % N);
      const FxR = 0.5 * (ar[p] + ar[q]), FxI = 0.5 * (ai[p] - ai[q]), FyR = 0.5 * (ai[p] + ai[q]), FyI = -0.5 * (ar[p] - ar[q]);   // unpack two real FFTs
      const kx = this.kx[i], ky = this.ky[j], d = this.deal[p];
      outR[p] = d * (-kx * FyI + ky * FxI); outI[p] = d * (kx * FyR - ky * FxR);   // i kx Fy - i ky Fx
    }
  }
  dtCFL() { let m = 1e-12; for (let p = 0; p < this.N * this.M; p++) { const s = Math.abs(this.u[p]) + Math.abs(this.v[p]); if (s > m) m = s; } return Math.min(this.dtMax, this.cfl * Math.min(this.dx, this.dy) / m, 0.9 * this.eta); }
  step(dt) {   // adaptive AB2 with exact integration of the viscous term (K&S 2009, eqs. 15-17)
    const NM = this.N * this.M, cr = this.ar === this.br ? null : new Float64Array(0);
    if (!this._Nr) { this._Nr = new Float64Array(NM); this._Ni = new Float64Array(NM); }
    const Nr = this._Nr, Ni = this._Ni; this.rhs(Nr, Ni);
    if (dt === undefined) dt = this.dtCFL();
    const nu = this.nu;
    if (!this.started) {   // first-order start: exponential Euler
      for (let p = 0; p < NM; p++) { const e = Math.exp(-nu * this.k2[p] * dt); this.wr[p] = e * (this.wr[p] + dt * Nr[p]); this.wi[p] = e * (this.wi[p] + dt * Ni[p]); }
      this.started = true;
    } else {
      const dn = this.dtPrev, b10 = 0.5 * dt / dn * (dt + 2 * dn), b11 = -0.5 * dt * dt / dn;
      for (let p = 0; p < NM; p++) {
        const e1 = Math.exp(-nu * this.k2[p] * dt), e0 = Math.exp(-nu * this.k2[p] * dn);
        this.wr[p] = e1 * (this.wr[p] + b10 * Nr[p] + b11 * e0 * this.nr[p]);
        this.wi[p] = e1 * (this.wi[p] + b10 * Ni[p] + b11 * e0 * this.ni[p]);
      }
    }
    this.nr.set(Nr); this.ni.set(Ni); this.dtPrev = dt; this.t += dt; this.steps++;
    this.wr[0] = 0; this.wi[0] = 0;
    return dt;
  }
}
module.exports = { Solver, makeFFT };
