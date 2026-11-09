/* The Electron Beam, from Tip to Measurement · physics/ch07.js
   Chapter 7, detect and measure: the secondary-electron line profile of a line-and-space pattern, its shot noise, the width an edge
   algorithm reads from it, how precise that width is, and how many such measurements fit in an hour. Pure module; mirrored by ref/ch07.py.

   Geometry: one period of width `pitch`, a line of width `cd` at half height, height h, sidewalls tilted by beta from the vertical, so each
   sidewall projects onto the width w = h tan(beta) and the top is cd - w wide.
   Yield (secant law of the escape depth): on a surface tilted by theta the SE yield is delta / cos(theta); the sidewall (theta = 90 deg - beta)
   gives delta / sin(beta) over its projected width w. The excess over the flat value, delta (1/sin(beta) - 1) w = delta h (1/cos(beta) - tan(beta)),
   stays finite as beta -> 0 (then delta h).  Backscattered electrons add a flat eta_BSE (no topographic contrast assumed for them).
   Blur: Gaussian, sigma_b^2 = sigma_p^2 + sigma_sig^2, sigma_p = d_p / (2 sqrt(2 ln 2)) (a Gaussian probe of FW50 d_p), sigma_sig from chapter 6.
   Counts: nbar = I_p t_d / e beam electrons per pixel; each collected with the yield Y(x) and the collection fraction eta_c. Taking the beam
   electrons and the secondaries each Poisson, the counts per pixel of one line have mean nbar m and variance nbar (m + m^2), m = eta_c Y(x).
   N_px lines along the feature are averaged into one profile, so its variance is that over N_px.
   Edge algorithm (threshold on the outer flank of each edge peak): baseline b = mean of the pixels in the middle half of the space; peak level
   = mean of the three pixels around the maximum of each half; threshold T = (b + peak) / 2; the edge is where the profile, walked outwards
   from the peak, first falls below T (linear interpolation between pixels). CD_meas = x_R - x_L.
   sigma_CD: first-order error propagation, sigma^2 = sum_i (dCD/dS_i)^2 var_i, with dCD/dS_i by finite differences of the algorithm itself;
   sigma_CD_mc: the same algorithm on 1000 noisy averaged profiles (Gaussian noise of the stated variance, Box-Muller from core.rng, seed fixed).
   SNR: (peak - baseline) / sqrt(variance at the baseline) for one line, the contrast an operator sees in the raw image.
   Time per site: N_px^2 t_d (one square image) + t_ov.  erf: Abramowitz and Stegun 7.1.26 (|error| < 1.5e-7). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./core.js'));
  else { root.EB = root.EB || {}; root.EB.ch07 = factory(root.EB.core); }
})(typeof self !== 'undefined' ? self : this, function (core) {
  'use strict';
  const { C } = core;
  const SEED = 7072026, NMC = 1000;
  function erf(x) {
    const s = x < 0 ? -1 : 1, a = Math.abs(x), t = 1 / (1 + 0.3275911 * a);
    const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-a * a);
    return s * y;
  }
  const Phi = u => 0.5 * (1 + erf(u / Math.SQRT2));
  // blurred yield at x: flat delta + eta, plus the two sidewall excesses spread over their projected widths and blurred by sigma_b;
  // the pattern is periodic, so the neighbouring periods' edges are added too
  function yieldAt(x, p, sb) {
    const w = p.height * Math.tan(p.sidewall), dens = p.delta_SE * p.height * (1 / Math.cos(p.sidewall) - Math.tan(p.sidewall));
    let Y = p.delta_SE + p.eta_BSE;
    for (let k = -2; k <= 2; k++) {
      const c = k * p.pitch;
      for (const [a, b] of [[c - (p.cd + w) / 2, c - (p.cd - w) / 2], [c + (p.cd - w) / 2, c + (p.cd + w) / 2]]) {
        if (b - a < 1e-6 * sb) Y += dens * Math.exp(-0.5 * ((x - 0.5 * (a + b)) / sb) ** 2) / (sb * Math.sqrt(2 * Math.PI));
        else Y += dens / (b - a) * (Phi((x - a) / sb) - Phi((x - b) / sb));
      }
    }
    return Y;
  }
  function setup(p) {
    const n = Math.max(8, Math.round(p.pitch / p.px)), dx = p.pitch / n;
    const sp = p.d_p / (2 * Math.sqrt(2 * Math.LN2)), sb = Math.sqrt(sp * sp + p.sigma_sig * p.sigma_sig);
    const nbar = p.I_p * p.t_d / C.e;
    const x = [], mean = [], varLine = [];
    for (let i = 0; i < n; i++) {
      const xi = -p.pitch / 2 + (i + 0.5) * dx, m = p.eta_c * yieldAt(xi, p, sb);
      x.push(xi); mean.push(nbar * m); varLine.push(nbar * (m + m * m));
    }
    return { n, dx, sb, nbar, x, mean, varLine };
  }
  // the edge algorithm on a profile S sampled at x (one period centred on the line); returns [xL, xR] or null
  function edges(S, x, p) {
    const n = S.length, q = (p.pitch - p.cd) / 4;
    let bs = 0, nb = 0;
    for (let i = 0; i < n; i++) if (Math.abs(x[i]) >= p.pitch / 2 - q) { bs += S[i]; nb++; }
    if (!nb) return null;
    const b = bs / nb, half = Math.floor(n / 2);
    const side = (lo, hi, dir) => {
      let im = lo; for (let i = lo; i < hi; i++) if (S[i] > S[im]) im = i;
      const pk = (S[Math.max(im - 1, 0)] + S[im] + S[Math.min(im + 1, n - 1)]) / 3, T = 0.5 * (b + pk);
      for (let i = im; i + dir >= 0 && i + dir < n; i += dir) {
        const j = i + dir;
        if (S[j] < T) { const f = (S[i] - T) / (S[i] - S[j]); return x[i] + f * (x[j] - x[i]); }
      }
      return null;
    };
    const xL = side(0, half, -1), xR = side(half, n, 1);
    return xL === null || xR === null ? null : [xL, xR];
  }
  function compute(p) {
    const st = setup(p), N = p.N_px;
    const e0 = edges(st.mean, st.x, p);
    if (!e0) throw new Error('the edge algorithm finds no edges: the space is narrower than a few pixels or the edges are blurred into each other');
    let mx = -Infinity, mn = Infinity; for (const v of st.mean) { mx = Math.max(mx, v); mn = Math.min(mn, v); }
    if (mx - mn < 1e-3 * mn) throw new Error('the edges are blurred away: the profile varies by less than 0.1 % across the period, so there is nothing to measure (the blur of the signal is much wider than the pitch)');
    const cd0 = e0[1] - e0[0];
    // error propagation: dCD/dS_i by finite differences of the algorithm
    let v = 0;
    const S = st.mean.slice();
    for (let i = 0; i < st.n; i++) {
      const h = 1e-6 * Math.max(1e-30, Math.abs(S[i])) + 1e-12;
      S[i] += h; const e1 = edges(S, st.x, p); S[i] -= h;
      const g = e1 ? ((e1[1] - e1[0]) - cd0) / h : 0;
      v += g * g * st.varLine[i] / N;
    }
    // Monte Carlo: the same algorithm on NMC noisy averaged profiles
    const rnd = core.rng(SEED), sd = st.varLine.map(z => Math.sqrt(z / N));
    let s1 = 0, s2 = 0, ok = 0;
    const noisy = new Array(st.n), avgShown = [], lineShown = [];
    for (let r = 0; r < NMC; r++) {
      for (let i = 0; i < st.n; i++) {
        const u1 = 1 - rnd(), u2 = rnd();
        noisy[i] = st.mean[i] + sd[i] * Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
      }
      if (r === 0) for (let i = 0; i < st.n; i++) avgShown.push(noisy[i]);
      const e = edges(noisy, st.x, p);
      if (e) { const c = e[1] - e[0]; s1 += c; s2 += c * c; ok++; }
    }
    const mc = ok > 1 ? Math.sqrt(Math.max(0, (s2 - s1 * s1 / ok) / (ok - 1))) : NaN;
    // one raw line, for the figure (Gaussian noise of one line's variance)
    for (let i = 0; i < st.n; i++) { const u1 = 1 - rnd(), u2 = rnd(); lineShown.push(st.mean[i] + Math.sqrt(st.varLine[i]) * Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2)); }
    // SNR of one line
    let ib = 0; for (let i = 0; i < st.n; i++) if (Math.abs(st.x[i]) > Math.abs(st.x[ib])) ib = i;
    let ip = 0; for (let i = 0; i < st.n; i++) if (st.mean[i] > st.mean[ip]) ip = i;
    const snr = (st.mean[ip] - st.mean[ib]) / Math.sqrt(st.varLine[ib]);
    const curve = [];
    for (let i = 0; i < st.n; i++) curve.push(st.x[i], st.mean[i], lineShown[i], avgShown[i]);
    const tSite = N * N * p.t_d + p.t_ov;
    return { SNR: snr, sigma_CD: Math.sqrt(v), MPH: 1 / tSite, CD_meas: cd0, sigma_CD_mc: mc, dose: p.I_p * p.t_d / (p.px * p.px), n_pe: st.nbar, prof_curve: curve };
  }

  // one period: the line in section below, the counts of one noisy line (dots), the mean of N_px lines (dark), the expectation (wine), the edges
  function draw(ctx, w, h, p, out) {
    ctx.clearRect(0, 0, w, h);
    const cv = out.prof_curve, n = cv.length / 4, L = 46, R = w - 10, T = 12, B = h - 92;
    let ymax = 0; for (let i = 0; i < n; i++) ymax = Math.max(ymax, cv[4 * i + 1], cv[4 * i + 3]);
    ymax *= 1.15;
    const X = x => L + (x / p.pitch + 0.5) * (R - L), Y = v => B - Math.max(0, Math.min(1.3, v / ymax)) * (B - T);
    ctx.strokeStyle = '#d9d0c2'; ctx.lineWidth = 1; ctx.strokeRect(L, T, R - L, B - T);
    ctx.font = "11px 'IBM Plex Mono', monospace"; ctx.fillStyle = '#6f655f'; ctx.textAlign = 'right';
    for (const f of [0, 0.5, 1]) { const v = f * ymax / 1.15; ctx.fillText(core.fmt(v, 2), L - 4, Y(v) + 4); }
    ctx.save(); ctx.translate(12, (T + B) / 2); ctx.rotate(-Math.PI / 2); ctx.textAlign = 'center'; ctx.fillText('counts per pixel', 0, 0); ctx.restore();
    ctx.fillStyle = 'rgba(58,50,46,0.45)';
    for (let i = 0; i < n; i++) { ctx.beginPath(); ctx.arc(X(cv[4 * i]), Y(cv[4 * i + 2]), 1.8, 0, 2 * Math.PI); ctx.fill(); }
    const line = (k, col, lw) => { ctx.strokeStyle = col; ctx.lineWidth = lw; ctx.beginPath(); for (let i = 0; i < n; i++) { const xx = X(cv[4 * i]), yy = Y(cv[4 * i + k]); i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); };
    line(3, '#3a322e', 1.4); line(1, '#7a1f2b', 2.2);
    // the line in section, to scale in x
    const gy = h - 30, sc = Math.min(40 / Math.max(p.height, 1e-12), 1e12), hh = Math.min(44, p.height * sc), ww = p.height * Math.tan(p.sidewall) * (R - L) / p.pitch;
    ctx.fillStyle = '#efe4c8'; ctx.strokeStyle = '#3a322e'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(L, gy); ctx.lineTo(X(-p.cd / 2) - ww / 2, gy); ctx.lineTo(X(-p.cd / 2) + ww / 2, gy - hh); ctx.lineTo(X(p.cd / 2) - ww / 2, gy - hh); ctx.lineTo(X(p.cd / 2) + ww / 2, gy); ctx.lineTo(R, gy); ctx.lineTo(R, gy + 8); ctx.lineTo(L, gy + 8); ctx.closePath(); ctx.fill(); ctx.stroke();
    // measured edges (noise-free algorithm), dashed through both panels
    const xc = out.CD_meas / 2;
    ctx.strokeStyle = '#1c1518'; ctx.setLineDash([4, 3]);
    for (const xe of [-xc, xc]) { ctx.beginPath(); ctx.moveTo(X(xe), T); ctx.lineTo(X(xe), gy + 8); ctx.stroke(); }
    ctx.setLineDash([]);
    ctx.fillStyle = '#3a322e'; ctx.textAlign = 'left';
    ctx.fillText(w < 460 ? 'wine expected · dark mean · dots one line' : 'wine: expected · dark: mean of ' + p.N_px + ' lines · dots: one line', w < 460 ? 6 : L, h - 8);
  }

  return {
    id: 'ch07',
    inputs: ['d_p', 'I_p', 't_d', 'N_px', 'eta_c', 'cd', 'pitch', 'height', 'sidewall', 'px', 't_ov', 'delta_SE', 'eta_BSE', 'sigma_sig'],
    outputs: ['SNR', 'sigma_CD', 'MPH', 'CD_meas', 'sigma_CD_mc', 'dose', 'n_pe', 'prof_curve'],
    tolerance: { rel: 1e-9, abs: 1e-15, note: 'closed formulas and the same algorithm on both sides; the Monte Carlo uses the same random numbers, and log and cos may differ in the last bit' },
    cases: [{}, { t_d: 1e-6 }, { N_px: 64, I_p: 1e-12 }, { sidewall: 0, height: 5e-8, cd: 1.5e-8 }, { d_p: 2e-8, sigma_sig: 1e-8, pitch: 1e-7 }],
    ui: {
      controls: ['t_d', 'N_px', 'I_p', 'd_p', 'eta_c', 'cd', 'pitch', 'height', 'sidewall', 'px'],
      readouts: ['n_pe', 'SNR', 'CD_meas', 'sigma_CD', 'sigma_CD_mc', 'dose', 'MPH'],
      aspect: '16 / 10', aspectPhone: '4 / 5',
      caption: 'One period of a line-and-space pattern, seen by the secondary-electron detector: the line in section below, the expected counts above (wine), one noisy scan line (dots) and the mean of all scan lines (dark). The dashed lines are the edges the threshold algorithm finds. The two edges are bright because a beam on a steep sidewall frees more secondaries near a surface. The yields and the blur of the signal are chapter 6’s silicon at 800 V and can be changed in chapter 8.',
    },
    compute, draw, edges, setup, yieldAt, erf,
  };
});
