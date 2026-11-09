/* Project 07 · The Electron Beam · chapter 2, the source.
   Pure module: runs in the page and in Node (CommonJS module.exports, or globalThis.EB_CH02 after `await import()` because the repository is type:module). SI units everywhere unless a name says eV.
   Mirror of ref/ch02.py (NumPy). Constants are CODATA 2018 exact values; until the scaffold's physics/core.js lands they are
   repeated here (request in notes/electron-beam/requests.md).

   Model (every line is derived on the page, section numbers in the comments refer to text/ch02.py):
     free-electron metal, Fermi level mu = 0, work function phi, planar Schottky-Nordheim (SN) barrier
         U(x) = phi - eps - e F x - e^2 / (16 pi eps0 x)            (eps = energy relative to mu)           [2.2]
     WKB transmission of normal energy w:   D(w) = 1 / (1 + exp G(w)),  G = (2/hbar) Int sqrt(2 m U) dx      [2.3]
     supply function:  N(w) = (4 pi m kT / h^3) ln(1 + exp(-w/kT))                                             [2.4]
     current density:  J = e Int N(w) D(w) dw                                                                [2.5]
     total-energy distribution: P(eps) = f(eps) Int_{-inf}^{eps} D(w) dw                                      [2.8]
   The analytic Fowler-Nordheim form (Forbes' v(f), t(f)) is the T -> 0 limit of the same integrals.          [2.6]  */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();   // CommonJS
  else root.EB_CH02 = factory();                                                   // page, or Node ESM (import, then globalThis.EB_CH02)
})(typeof globalThis !== 'undefined' ? globalThis : self, function () {
  'use strict';

  /* ---------------------------------------------------------------- constants (CODATA 2018) */
  const K = { e: 1.602176634e-19, h: 6.62607015e-34, me: 9.1093837015e-31, eps0: 8.8541878128e-12,
              kB: 1.380649e-23, u: 1.66053906660e-27, c: 299792458 };
  K.hbar = K.h / (2 * Math.PI);
  K.Q0 = K.e * K.e / (16 * Math.PI * K.eps0);                 // image-charge constant, J m
  K.bFN = 4 * Math.sqrt(2 * K.me) / (3 * K.hbar * K.e);       // J^-3/2 V/m: G_triangular = bFN phi^{3/2} / F
  K.RD = 4 * Math.PI * K.me * K.e * K.kB * K.kB / (K.h * K.h * K.h);  // Richardson constant, A m^-2 K^-2
  const eV = K.e;

  /* ---------------------------------------------------------------- Gauss-Legendre nodes */
  const GL = {};
  function gauleg(n) {
    if (GL[n]) return GL[n];
    const x = new Float64Array(n), w = new Float64Array(n);
    for (let i = 0; i < n; i++) {
      let z = Math.cos(Math.PI * (i + 0.75) / (n + 0.5)), pp = 1;
      for (let it = 0; it < 100; it++) {
        let p1 = 1, p2 = 0;
        for (let j = 0; j < n; j++) { const p3 = p2; p2 = p1; p1 = ((2 * j + 1) * z * p2 - j * p3) / (j + 1); }
        pp = n * (z * p1 - p2) / (z * z - 1);
        const dz = p1 / pp; z -= dz; if (Math.abs(dz) < 1e-15) break;
      }
      x[i] = z; w[i] = 2 / ((1 - z * z) * pp * pp);
    }
    return (GL[n] = { x, w });
  }

  /* ---------------------------------------------------------------- the barrier */
  const schottkyLowering = F => Math.sqrt(K.e * K.e * K.e * F / (4 * Math.PI * K.eps0));    // J  [2.2]
  const scaledField = (F, phi) => K.e * K.e * K.e * F / (4 * Math.PI * K.eps0 * phi * phi);  // f = (dphi/phi)^2
  const referenceField = phi => 4 * Math.PI * K.eps0 * phi * phi / (K.e * K.e * K.e);         // F_R, V/m

  // WKB exponent G for barrier height phi (J, from the energy of the electron) in field F (V/m): exact roots, 48-point Gauss-Legendre
  function barrierG(F, phi, n) {
    if (phi <= 0) return 0;
    const f = scaledField(F, phi);
    if (f >= 1) return 0;
    const s = Math.sqrt(1 - f), x1 = phi * (1 - s) / (2 * K.e * F), x2 = phi * (1 + s) / (2 * K.e * F), D = x2 - x1;
    const g = gauleg(n || 48);
    let S = 0;
    for (let i = 0; i < g.x.length; i++) {
      const th = Math.PI / 4 * (g.x[i] + 1), sn = Math.sin(th), cs = Math.cos(th);
      S += g.w[i] * 2 * D * D * sn * sn * cs * cs / Math.sqrt(x1 + D * sn * sn);
    }
    S *= Math.PI / 4;
    return 2 * Math.sqrt(2 * K.me) / K.hbar * Math.sqrt(K.e * F) * S;
  }

  // v(f): exact, from the integral (any phi gives the same v), and Forbes' simple good approximation
  function vExact(f) {
    if (f <= 0) return 1; if (f >= 1) return 0;
    const phi = 4.5 * eV, F = f * referenceField(phi);
    return barrierG(F, phi, 64) * F / (K.bFN * Math.pow(phi, 1.5));
  }
  const vForbes = f => f <= 0 ? 1 : 1 - f + f * Math.log(f) / 6;
  const tForbes = f => f <= 0 ? 1 : 1 + f / 9 - f * Math.log(f) / 18;

  /* ---------------------------------------------------------------- analytic Fowler-Nordheim current density [2.6] */
  const dTunnel = (F, phi) => K.hbar * K.e * F / (2 * Math.sqrt(2 * K.me * phi) * tForbes(Math.min(scaledField(F, phi), 1)));  // J
  function jFN(F, phi, T) {
    const f = scaledField(F, phi);
    if (f >= 1) return NaN;
    const t = tForbes(f), v = vForbes(f);
    let J = K.e * K.e * K.e * F * F / (8 * Math.PI * K.h * phi * t * t) * Math.exp(-v * K.bFN * Math.pow(phi, 1.5) / F);
    if (T > 0) { const x = Math.PI * K.kB * T / dTunnel(F, phi); J *= x < 1.5 ? x / Math.sin(x) : NaN; }
    return J;
  }
  const jRichardson = (T, phi) => K.RD * T * T * Math.exp(-phi / (K.kB * T));
  const jSchottky = (F, T, phi) => K.RD * T * T * Math.exp(-(phi - schottkyLowering(F)) / (K.kB * T));

  /* ---------------------------------------------------------------- dilogarithm helper: L(z) = -Li2(-z), z > 0 */
  function negLi2(z) {
    const li2 = y => { let s = 0, p = 1; for (let k = 1; k < 60; k++) { p *= y; s += p / (k * k); } return s; };
    const small = zz => { const y = zz / (1 + zz), l = Math.log(1 + zz); return li2(y) + 0.5 * l * l; };   // Landen
    if (z <= 1) return small(z);
    const l = Math.log(z); return Math.PI * Math.PI / 6 + 0.5 * l * l - small(1 / z);
  }

  /* ---------------------------------------------------------------- the full model at one point of the surface [2.5, 2.8] */
  // F V/m, phi J, T K  ->  current density J, energy distribution P(eps), FWHM, brightness ingredients
  function emissionModel(F, phi, T, opt) {
    opt = opt || {};
    T = Math.max(T, 1);
    const kT = K.kB * T, dphi = schottkyLowering(F), top = phi - dphi;          // barrier top, J, above the Fermi level
    const f0 = scaledField(F, phi);
    const d = f0 < 1 ? dTunnel(F, phi) : 0.1 * eV;
    const lo = -Math.max(25 * d, 12 * kT), hi = Math.max(14 * kT, top + 14 * kT);
    const step = Math.min(d, kT) / 14;
    const n = Math.max(400, Math.min(opt.maxPoints || 2400, Math.ceil((hi - lo) / step)));
    const w = new Float64Array(n), D = new Float64Array(n), dw = (hi - lo) / (n - 1);
    // slope of G at the barrier top, for the parabolic-top (Kemble) continuation above it
    let sTop = 0;
    if (top > 0) { const dl = Math.min(0.02 * eV, 0.2 * top); sTop = barrierG(F, phi - (top - dl), 24) / dl; }
    for (let i = 0; i < n; i++) {
      const wi = lo + i * dw; w[i] = wi;
      let G;
      if (wi <= top) G = barrierG(F, phi - wi, 24); else G = -(wi - top) * sTop;
      D[i] = G > 700 ? 0 : 1 / (1 + Math.exp(G));
    }
    const ferm = x => x > 700 ? 0 : 1 / (1 + Math.exp(x / kT));
    const pref = 4 * Math.PI * K.me / (K.h * K.h * K.h);                           // 4 pi m / h^3
    let sJ = 0, sj0 = 0, g0 = 0, g1 = 0;
    const C = new Float64Array(n), P = new Float64Array(n);
    for (let i = 0; i < n; i++) {
      const wi = w[i], z = Math.exp(-wi / kT), lw = wi / kT > 40 ? z : Math.log(1 + z);   // ln(1+e^{-w/kT})
      const wt = (i === 0 || i === n - 1) ? 0.5 : 1;
      sJ += wt * lw * D[i]; sj0 += wt * ferm(wi) * D[i];
      g0 += wt * lw * D[i]; g1 += wt * negLi2(Math.min(z, 1e300)) * D[i];
      if (i > 0) C[i] = C[i - 1] + 0.5 * (D[i] + D[i - 1]) * dw;
      P[i] = ferm(wi) * C[i];
    }
    const J = K.e * pref * kT * sJ * dw;                                           // [2.5]
    const jt0 = K.e * pref * sj0 * dw;                                             // A m^-2 J^-1 at zero transverse energy
    const meanEt = g0 > 0 ? kT * g1 / g0 : 0;                                      // mean transverse energy, J: (kT)^2 Int L D / (kT Int ln D)
    let ip = 0; for (let i = 1; i < n; i++) if (P[i] > P[ip]) ip = i;
    const half = P[ip] / 2; let l = ip, r = ip;
    while (l > 0 && P[l] > half) l--; while (r < n - 1 && P[r] > half) r++;
    const xl = l < ip ? w[l] + (half - P[l]) / (P[l + 1] - P[l]) * dw : w[l];
    const xr = r > ip ? w[r - 1] + (P[r - 1] - half) / (P[r - 1] - P[r]) * dw : w[r];
    let sP = 0; for (let i = 0; i < n; i++) sP += ((i === 0 || i === n - 1) ? 0.5 : 1) * P[i];
    const Jcheck = K.e * pref * sP * dw;                                           // must equal J (integration by parts)
    return { J, Jcheck, jt0, B_r: eV * jt0 / Math.PI, meanEt, fwhm: xr - xl, peak: w[ip], top, d, f: f0, kT, dphi,
             w, D, P, Ppeak: P[ip], regime: regimeOf(f0, kT, w[ip], top) };
  }
  // Gomer's three regimes by where the emitted-energy peak sits: below the Fermi level, between it and the barrier top, at the top
  function regimeOf(f, kT, peak, top) {
    if (f >= 1) return 'field above the barrier: no tunnelling barrier left';
    if (peak < 0) return 'cold field emission';
    if (top > 0 && peak < top - 3 * kT) return 'thermal-field emission';
    return 'thermionic (Schottky) emission';
  }

  /* ---------------------------------------------------------------- the tip: sphere in a field [2.1] */
  const tipField = (V, r, k) => V / (k * r);                                       // F = V / (k r)
  function tipCurrent(V, p) {
    // p: {r, k, phi (J), T}. Cap of a sphere, F(theta) = F0 cos(theta); I = 2 pi r^2 Int_0^1 J(F0 u) du
    const F0 = tipField(V, p.r, p.k), g = gauleg(p.nodes || 24);
    const u0 = p.u0 === undefined ? 0 : p.u0, a = (1 - u0) / 2, b = (1 + u0) / 2;
    let s = 0;
    for (let i = 0; i < g.x.length; i++) {
      const u = a * g.x[i] + b, Fu = F0 * u;
      const J = p.fast ? jFN(Fu, p.phi, p.T) : emissionModel(Fu, p.phi, p.T, { maxPoints: 500 }).J;
      s += g.w[i] * (isFinite(J) ? J : 0);
    }
    return 2 * Math.PI * p.r * p.r * a * s;
  }

  // the four numbers handed to chapter 3 (contract section 6 of PLAN.md)
  function handover(p) {
    const F0 = tipField(p.V, p.r, p.k), m = emissionModel(F0, p.phi, p.T);
    const I_e = tipCurrent(p.V, p);
    const dE = m.fwhm, d_v = 2 * p.r * Math.sqrt(m.meanEt / (K.e * p.V));
    return { I_e, B_r: m.B_r, dE, dE_eV: dE / eV, d_v, F0, f: m.f, J0: m.J, meanEt_eV: m.meanEt / eV, regime: m.regime };
  }

  /* ---------------------------------------------------------------- vacuum and contamination [2.9-2.12] */
  const hkFlux = (pPa, Tg, mu) => pPa / Math.sqrt(2 * Math.PI * mu * K.u * K.kB * Tg);          // molecules m^-2 s^-1
  const kDes = (Ed, T, nu0) => (nu0 || 1e13) * Math.exp(-Ed * eV / (K.kB * T));                  // s^-1
  function coverageStep(theta0, dt, a, kd) {                                                    // exact solution of dtheta/dt = a(1-theta) - kd theta
    const lam = a + kd, thInf = lam > 0 ? a / lam : 0;
    return thInf + (theta0 - thInf) * Math.exp(-lam * dt);
  }
  const timeToCoverage = (th, a, kd) => { const lam = a + kd, inf = a / lam; return th < inf ? -Math.log(1 - th / inf) / lam : Infinity; };
  const currentRatio = (theta, rho) => (1 - theta) + theta * rho;                               // patch model, model assumption
  function coveredRatio(F, phi, dphiAds) { return jFN(F, phi + dphiAds * eV, 0) / jFN(F, phi, 0); }

  // run the cycle: p {pPa, Tg, mu, Ns, s, kappa, Ed, T (tip, K), Tflash, tflash, thr (trigger I/I0, 0 = never), theta0, rho, tmax, dt}
  function cycle(p) {
    const phiFlux = hkFlux(p.pPa, p.Tg, p.mu), a = p.kappa * p.s * phiFlux / p.Ns;
    const kRT = kDes(p.Ed, p.T), kFl = kDes(p.Ed, p.Tflash);
    const out = { t: [], theta: [], ratio: [], flashes: [], a, kRT, kFl, flux: phiFlux };
    let t = 0, th = p.theta0 || 0, tf = -1;
    const every = Math.max(1, Math.round(p.tmax / p.dt / 1200));
    for (let i = 0; t <= p.tmax; i++) {
      if (i % every === 0) { out.t.push(t); out.theta.push(th); out.ratio.push(currentRatio(th, p.rho)); }
      if (p.thr > 0 && currentRatio(th, p.rho) < p.thr) {
        out.flashes.push(t);
        th = coverageStep(th, p.tflash, a, kFl); t += p.tflash;      // tip hot: desorption fast, no emission measured
        out.t.push(t); out.theta.push(th); out.ratio.push(NaN);
        continue;
      }
      th = coverageStep(th, p.dt, a, kRT); t += p.dt;
    }
    return out;
  }

  /* ---------------------------------------------------------------- Fowler-Nordheim plot of the tip */
  function fnPlot(p, V1, V2, n) {
    const pts = [];
    for (let i = 0; i < n; i++) {
      const V = V1 + (V2 - V1) * i / (n - 1), I = tipCurrent(V, p);
      pts.push({ V, I, x: 1 / V, y: Math.log(I / (V * V)) });
    }
    return pts;
  }

  return { K, gauleg, schottkyLowering, scaledField, referenceField, barrierG, vExact, vForbes, tForbes, dTunnel, jFN, jRichardson, jSchottky,
           negLi2, emissionModel, tipField, tipCurrent, handover, hkFlux, kDes, coverageStep, timeToCoverage, currentRatio, coveredRatio,
           cycle, fnPlot };
});
