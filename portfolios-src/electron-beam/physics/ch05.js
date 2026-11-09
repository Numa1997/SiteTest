/* The Electron Beam, from Tip to Measurement · physics/ch05.js
   Chapter 5, the spot: how large the probe is for a given current and beam angle, and which angle makes it smallest.
   Pure module (physics/core.js pattern); mirrored by ref/ch05.py.

   Probe current and source image (Bronsgeest et al. 2008, Eq. 6, with the practical brightness B_pr = B_r / ln 2 of chapter 3):
       I_p = B_pr V* (pi d_I^2 / 4)(pi alpha^2)   =>   d_I = sqrt(4 I_p / (pi^2 B_pr V* alpha^2))
   'fw50' (diameter holding half the current; Barth & Kruit 1996 root-power sum, coefficients of Bronsgeest et al. 2008, Eqs. 18-21):
       d_A = 0.66 lambda / alpha,  d_S = 0.18 C_s alpha^3,  d_C = 0.6 C_c (dE / eV*) alpha
       d_p = sqrt( ((d_A^4 + d_S^4)^(1.3/4) + d_I^1.3)^(2/1.3) + d_C^2 )
   'rss' (classic quadrature sum):  d_A = 1.22 lambda / alpha (Airy disc to the first zero), d_S = 0.5 C_s alpha^3 (disc of least confusion),
       d_C = C_c (dE / eV*) alpha,  d_p = sqrt(d_A^2 + d_S^2 + d_C^2 + d_I^2)
   dE is the FWHM of chapter 2, used for dE_FW50 in 'fw50' (chapter 5 states the difference). alpha_opt: golden-section search on ln alpha
   over [0.1, 100] mrad, 80 steps. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./core.js'));
  else { root.EB = root.EB || {}; root.EB.ch05 = factory(root.EB.core); }
})(typeof self !== 'undefined' ? self : this, function (core) {
  'use strict';
  const { C } = core;
  const vstar = V => V * (1 + C.e * V / (2 * C.m_e * C.c * C.c));

  function terms(p, alpha) {
    const Vs = vstar(p.V_land), lam = C.h / Math.sqrt(2 * C.m_e * C.e * Vs), rel = p.dE / (C.e * Vs);
    const Bpr = p.B_r / Math.LN2;
    const dI = Math.sqrt(4 * p.I_p / (Math.PI * Math.PI * Bpr * Vs * alpha * alpha));
    let dA, dS, dC, dp;
    if (p.probe_convention === 'rss') {
      dA = 1.22 * lam / alpha; dS = 0.5 * p.C_s * Math.pow(alpha, 3); dC = p.C_c * rel * alpha;
      dp = Math.sqrt(dA * dA + dS * dS + dC * dC + dI * dI);
    } else {
      dA = 0.66 * lam / alpha; dS = 0.18 * p.C_s * Math.pow(alpha, 3); dC = 0.6 * p.C_c * rel * alpha;
      const inner = Math.pow(Math.pow(dA, 4) + Math.pow(dS, 4), 1.3 / 4) + Math.pow(dI, 1.3);
      dp = Math.sqrt(Math.pow(inner, 2 / 1.3) + dC * dC);
    }
    return { dA, dS, dC, dI, dp };
  }

  function compute(p) {
    const t = terms(p, p.alpha);
    // golden-section search for the smallest d_p over ln(alpha)
    let lo = Math.log(1e-4), hi = Math.log(1e-1);
    const g = (Math.sqrt(5) - 1) / 2;
    let x1 = hi - g * (hi - lo), x2 = lo + g * (hi - lo), f1 = terms(p, Math.exp(x1)).dp, f2 = terms(p, Math.exp(x2)).dp;
    for (let i = 0; i < 80; i++) {
      if (f1 < f2) { hi = x2; x2 = x1; f2 = f1; x1 = hi - g * (hi - lo); f1 = terms(p, Math.exp(x1)).dp; }
      else { lo = x1; x1 = x2; f1 = f2; x2 = lo + g * (hi - lo); f2 = terms(p, Math.exp(x2)).dp; }
    }
    const aopt = Math.exp((lo + hi) / 2);
    const curve = [];
    for (let i = 0; i <= 60; i++) { const a = 5e-4 * Math.pow(100, i / 60), q = terms(p, a); curve.push(a, q.dA, q.dS, q.dC, q.dI, q.dp); }
    return { d_p: t.dp, d_I: t.dI, d_A: t.dA, d_S: t.dS, d_C: t.dC, alpha_opt: aopt, d_p_opt: terms(p, aopt).dp, spot_curve: curve };
  }

  // d_p and its four parts against alpha on log-log axes; the present alpha and alpha_opt marked
  function draw(ctx, w, h, p, out) {
    ctx.clearRect(0, 0, w, h);
    const L = 52, R = w - 12, T = 14, B = h - 34;
    const cv = out.spot_curve, n = cv.length / 6;
    let ymin = Infinity, ymax = 0;
    for (let i = 0; i < n; i++) { ymax = Math.max(ymax, cv[6 * i + 5]); ymin = Math.min(ymin, cv[6 * i + 5]); }
    const y0 = Math.log10(ymin) - 1.2, y1 = Math.log10(ymax) + 0.1;
    const X = a => L + (Math.log10(a) - Math.log10(5e-4)) / 2 * (R - L), Y = d => B - (Math.log10(Math.max(d, 1e-14)) - y0) / (y1 - y0) * (B - T);
    ctx.strokeStyle = '#d9d0c2'; ctx.lineWidth = 1; ctx.strokeRect(L, T, R - L, B - T);
    ctx.font = "11px 'IBM Plex Mono', monospace"; ctx.fillStyle = '#6f655f'; ctx.textAlign = 'center';
    for (const a of [1e-3, 1e-2]) { ctx.beginPath(); ctx.moveTo(X(a), B); ctx.lineTo(X(a), B + 4); ctx.stroke(); ctx.fillText(core.fmt(a * 1e3, 2) + ' mrad', X(a), B + 16); }
    ctx.fillText('beam half-angle α', (L + R) / 2, h - 4);
    ctx.textAlign = 'right';
    for (let k = Math.ceil(y0); k <= Math.floor(y1); k++) { const y = Y(Math.pow(10, k)); ctx.beginPath(); ctx.moveTo(L - 4, y); ctx.lineTo(L, y); ctx.stroke(); ctx.fillText(core.fmt(Math.pow(10, k + 9), 1) + ' nm', L - 6, y + 4); }
    const ser = [[1, '#8b8079', [5, 3], 'diffraction'], [2, '#7a4b12', [2, 3], 'spherical'], [3, '#e2a2aa', [], 'chromatic'], [4, '#3a322e', [6, 2, 2, 2], 'source image'], [5, '#7a1f2b', [], 'probe']];
    ctx.save(); ctx.beginPath(); ctx.rect(L, T, R - L, B - T); ctx.clip();
    for (const [k, col, dash] of ser) { ctx.strokeStyle = col; ctx.setLineDash(dash); ctx.lineWidth = k === 5 ? 2.4 : 1.4; ctx.beginPath(); for (let i = 0; i < n; i++) { const xx = X(cv[6 * i]), yy = Y(cv[6 * i + k]); i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); }
    ctx.restore(); ctx.setLineDash([]);
    const mark = (a, d, col, t, dy) => { ctx.fillStyle = col; ctx.beginPath(); ctx.arc(X(a), Y(d), 4, 0, 2 * Math.PI); ctx.fill(); ctx.textAlign = 'left'; ctx.fillText(t, X(a) + 6, Y(d) + dy); };
    mark(out.alpha_opt, out.d_p_opt, '#1c1518', 'optimum', 16); mark(p.alpha, out.d_p, '#7a1f2b', 'now', -8);
    ctx.textAlign = 'left';
    ser.forEach(([k, col, dash, t], i) => { ctx.strokeStyle = col; ctx.setLineDash(dash); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(L + 8, T + 12 + 13 * i); ctx.lineTo(L + 28, T + 12 + 13 * i); ctx.stroke(); ctx.setLineDash([]); ctx.fillStyle = '#5a504b'; ctx.fillText(t, L + 32, T + 16 + 13 * i); });
  }

  return {
    id: 'ch05',
    inputs: ['C_s', 'C_c', 'B_r', 'dE', 'V_land', 'alpha', 'I_p', 'probe_convention'],
    outputs: ['d_p', 'd_I', 'd_A', 'd_S', 'd_C', 'alpha_opt', 'd_p_opt', 'spot_curve'],
    tolerance: { rel: 1e-9, abs: 0, note: 'closed formulas agree to 1e-15; alpha_opt sits on a flat minimum, where a rounding tie can send the golden-section search down a neighbouring path, so it agrees to about 1e-12' },
    cases: [{}, { probe_convention: 'rss' }, { V_land: 30000, I_p: 1e-9 }, { C_s: 2e-4, C_c: 2e-4, I_p: 1e-12 }],
    ui: {
      controls: ['probe_convention', 'alpha', 'I_p', 'V_land', 'C_s', 'C_c', 'dE', 'B_r'],
      readouts: ['d_p', 'd_I', 'alpha_opt', 'd_p_opt'],
      aspect: '4 / 3', aspectPhone: '4 / 3',
      caption: 'The probe diameter (wine) and its four parts against the beam half-angle, on logarithmic axes, for the asked probe current. Diffraction falls with the angle, the aberrations rise with it, and the source image shrinks as the angle opens because the same current then needs less area. The dot marked optimum is the smallest probe.',
    },
    compute, draw, terms,
  };
});
