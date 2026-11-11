/* The Electron Beam, from Tip to Measurement · physics/ch05.js
   Chapter 5, the spot: how large the probe is for a given current and beam angle, and which angle makes it smallest.
   Pure module (physics/core.js pattern); mirrored by ref/ch05.py.

   Probe current and source image (Bronsgeest et al. 2008, Eq. 6, with the practical brightness B_pr = B_r / ln 2 of chapter 3):
       I_p = B_pr V* (pi d_I^2 / 4)(pi alpha^2)   =>   d_I = sqrt(4 I_p / (pi^2 B_pr V* alpha^2))
   'fw50' (diameter holding half the current; Barth & Kruit 1996 root-power sum, coefficients of Bronsgeest et al. 2008, Eqs. 18-21):
       d_A = 0.54 lambda / alpha (their Eq. 19 prints 0.66e-9 / (alpha sqrt(V)) in m and V; with lambda = 1.226 nm / sqrt(V) that is 0.54 lambda / alpha;
       the half-current diameter of the Airy disc is 0.535 lambda / alpha),  d_S = 0.18 C_s alpha^3,  d_C = 0.6 C_c (dE50 / eV*) alpha with dE50 the FW50
       of the energy distribution (chapter 2)
       d_p = sqrt( ((d_A^4 + d_S^4)^(1.3/4) + d_I^1.3)^(2/1.3) + d_C^2 )
   'rss' (classic quadrature sum):  d_A = 1.22 lambda / alpha (Airy disc to the first zero), d_S = 0.5 C_s alpha^3 (disc of least confusion),
       d_C = C_c (dE / eV*) alpha,  d_p = sqrt(d_A^2 + d_S^2 + d_C^2 + d_I^2)
   'rss' uses dE, the FWHM of chapter 2. alpha_opt: golden-section search on ln alpha over [0.1, 100] mrad, 80 steps; the curve spans the same range. */
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
      dA = 0.54 * lam / alpha; dS = 0.18 * p.C_s * Math.pow(alpha, 3); dC = 0.6 * p.C_c * (p.dE50 / (C.e * Vs)) * alpha;
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
    for (let i = 0; i <= 60; i++) { const a = 1e-4 * Math.pow(1000, i / 60), q = terms(p, a); curve.push(a, q.dA, q.dS, q.dC, q.dI, q.dp); }
    return { d_p: t.dp, d_I: t.dI, d_A: t.dA, d_S: t.dS, d_C: t.dC, alpha_opt: aopt, d_p_opt: terms(p, aopt).dp, spot_curve: curve };
  }

  // Labels that keep clear of the drawing: every line a label must not touch is registered as points (CSS px), every placed label and
  // every solid part as a box; a label goes to the first of its candidate places ([x, y, align, ...]) whose box, grown by a margin,
  // holds no point, meets no box and stays inside the bounds (the canvas unless given). put returns the box and the place used.
  function labels(ctx, w, h) {
    const P = [], Bx = [];
    const seg = (x0, y0, x1, y1) => { const n = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0) / 2)); for (let i = 0; i <= n; i++) P.push(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); };
    const box = (t, c) => { ctx.textAlign = c[2] || 'left'; const m = ctx.measureText(t); return [c[0] - m.actualBoundingBoxLeft, c[1] - m.actualBoundingBoxAscent, c[0] + m.actualBoundingBoxRight, c[1] + m.actualBoundingBoxDescent]; };
    const free = (b, m, r) => {
      if (b[0] < r[0] + 1 || b[1] < r[1] + 1 || b[2] > r[2] - 1 || b[3] > r[3] - 1) return false;
      for (let i = 0; i < P.length; i += 2) if (P[i] > b[0] - m && P[i] < b[2] + m && P[i + 1] > b[1] - m && P[i + 1] < b[3] + m) return false;
      return Bx.every(c => b[2] + m <= c[0] || c[2] + m <= b[0] || b[3] + m <= c[1] || c[3] + m <= b[1]);
    };
    return {
      line(xy) { for (let i = 2; i < xy.length; i += 2) seg(xy[i - 2], xy[i - 1], xy[i], xy[i + 1]); if (xy.length === 2) P.push(xy[0], xy[1]); },
      block(b) { Bx.push(b); },
      free: (b, m = 3, r = [0, 0, w, h]) => free(b, m, r),
      put(t, cands, m = 3, r = [0, 0, w, h]) {
        const c = cands.find(c => free(box(t, c), m, r)) || cands[0], b = box(t, c);
        ctx.fillText(t, c[0], c[1]); Bx.push(b); return [b, c];
      },
    };
  }

  // d_p and its four parts against alpha on log-log axes; the present alpha and alpha_opt marked
  function draw(ctx, w, h, p, out) {
    ctx.clearRect(0, 0, w, h);
    const L = 64, R = w - 12, T = 14, B = h - (w < 460 ? 94 : 78);
    const cv = out.spot_curve, n = cv.length / 6;
    let ymin = Infinity, ymax = 0;
    for (let i = 0; i < n; i++) { ymax = Math.max(ymax, cv[6 * i + 5]); ymin = Math.min(ymin, cv[6 * i + 5]); }
    const y0 = Math.log10(ymin) - 1.2, y1 = Math.log10(ymax) + 0.1;
    const X = a => L + (Math.log10(a) + 4) / 3 * (R - L), Y = d => B - (Math.log10(Math.max(d, 1e-14)) - y0) / (y1 - y0) * (B - T);
    ctx.strokeStyle = '#d9d0c2'; ctx.lineWidth = 1; ctx.__nocollide = true; ctx.strokeRect(L, T, R - L, B - T); ctx.__nocollide = false;   // the frame
    ctx.font = "11px 'IBM Plex Mono', monospace"; ctx.fillStyle = '#6f655f'; ctx.textAlign = 'center';
    for (const a of [1e-4, 1e-3, 1e-2, 1e-1]) { ctx.beginPath(); ctx.moveTo(X(a), B); ctx.lineTo(X(a), B + 4); ctx.stroke(); ctx.textAlign = a > 0.05 ? 'right' : (a < 2e-4 ? 'left' : 'center'); ctx.fillText(String(+(a * 1e3).toPrecision(2)), a > 0.05 ? X(a) + 2 : X(a), B + 16); }
    ctx.textAlign = 'center';
    ctx.fillText('beam half-angle α (mrad)', (L + R) / 2, B + 32);
    ctx.textAlign = 'right';
    for (let k = Math.ceil(y0); k <= Math.floor(y1); k++) { const y = Y(Math.pow(10, k)); ctx.beginPath(); ctx.moveTo(L - 4, y); ctx.lineTo(L, y); ctx.stroke(); ctx.fillText(core.fmt(Math.pow(10, k + 9), 1) + ' nm', L - 6, y + 4); }
    const ser = [[1, '#8b8079', [5, 3], 'diffraction'], [2, '#7a4b12', [2, 3], 'spherical'], [3, '#e2a2aa', [], 'chromatic'], [4, '#3a322e', [6, 2, 2, 2], 'source image'], [5, '#7a1f2b', [], 'probe']];
    ctx.save(); ctx.beginPath(); ctx.rect(L, T, R - L, B - T); ctx.clip();
    for (const [k, col, dash] of ser) { ctx.strokeStyle = col; ctx.setLineDash(dash); ctx.lineWidth = k === 5 ? 2.4 : 1.4; ctx.beginPath(); for (let i = 0; i < n; i++) { const xx = X(cv[6 * i]), yy = Y(cv[6 * i + k]); i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); }
    ctx.restore(); ctx.setLineDash([]);
    // the two marks: the dots first, then each word at the first free place of a few, above the probe curve where it can (the probe is
    // the upper envelope of its parts, so above it nothing is drawn); a word lifted beyond its first row hangs from a short leader
    const lab = labels(ctx, w, h);
    for (const a of [1e-4, 1e-3, 1e-2, 1e-1]) lab.line([X(a), B, X(a), B + 4]);
    for (let k = Math.ceil(y0); k <= Math.floor(y1); k++) lab.line([L - 4, Y(Math.pow(10, k)), L, Y(Math.pow(10, k))]);
    for (const [k] of ser) { const xy = []; for (let i = 0; i < n; i++) { const xx = X(cv[6 * i]), yy = Y(cv[6 * i + k]); if (yy >= T && yy <= B) xy.push(xx, yy); else if (xy.length) { lab.line(xy); xy.length = 0; } } lab.line(xy); }
    const marks = [[out.alpha_opt, out.d_p_opt, '#1c1518', 'optimum'], [p.alpha, out.d_p, '#7a1f2b', 'now']];
    for (const [a, d, col] of marks) { const x = X(a), y = Y(d); ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, 4, 0, 2 * Math.PI); ctx.fill(); lab.block([x - 4, y - 4, x + 4, y + 4]); }
    for (const [a, d, col, t] of marks) {
      const x = X(a), y = Y(d), c = [];
      for (const dy of [-9, -25, -41, -57]) c.push([x, y + dy, 'center', dy], [x - 3, y + dy, 'right', dy], [x + 3, y + dy, 'left', dy], [x - 16, y + dy, 'right', dy], [x + 16, y + dy, 'left', dy]);
      c.push([x + 8, y + 4, 'left', 0], [x - 8, y + 4, 'right', 0], [x, y + 18, 'center', 0], [x + 8, y + 18, 'left', 0], [x - 8, y + 18, 'right', 0]);
      ctx.fillStyle = col;
      const [b, cc] = lab.put(t, c, 3, [L, T, R, B]);
      const qx = Math.max(b[0], Math.min(b[2], x)), qy = Math.max(b[1], Math.min(b[3], y)), dist = Math.hypot(qx - x, qy - y);
      if (dist > 10) {                                                  // the leader, from the dot's rim to 2 px short of the word
        const ux = (qx - x) / dist, uy = (qy - y) / dist;
        ctx.__nocollide = true; ctx.strokeStyle = col; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x + 5 * ux, y + 5 * uy); ctx.lineTo(qx - 2 * ux, qy - 2 * uy); ctx.stroke(); ctx.__nocollide = false;
        lab.line([x + 5 * ux, y + 5 * uy, qx - 2 * ux, qy - 2 * uy]);
      }
    }
    ctx.textAlign = 'left';
    // legend below the plot, three items in the first row and two in the second, so it never covers a curve
    const nc = w < 460 ? 2 : 3, colW = (R - L + 40) / nc;
    ser.forEach(([k, col, dash, t], i) => { const x0 = L - 40 + colW * (i % nc), y0 = B + 50 + 16 * Math.floor(i / nc); ctx.strokeStyle = col; ctx.setLineDash(dash); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x0, y0 - 4); ctx.lineTo(x0 + 20, y0 - 4); ctx.stroke(); ctx.setLineDash([]); ctx.fillStyle = '#5a504b'; ctx.fillText(t, x0 + 27, y0); });
  }

  return {
    id: 'ch05',
    inputs: ['C_s', 'C_c', 'B_r', 'dE', 'dE50', 'V_land', 'alpha', 'I_p', 'probe_convention'],
    outputs: ['d_p', 'd_I', 'd_A', 'd_S', 'd_C', 'alpha_opt', 'd_p_opt', 'spot_curve'],
    tolerance: { rel: 1e-8, abs: 0, note: 'closed formulas agree to 1e-15; alpha_opt sits on a flat minimum, where a rounding tie can send the golden-section search down a neighbouring path: about 1e-12 at the test cases, 2e-9 at 100 V' },
    cases: [{}, { probe_convention: 'rss' }, { V_land: 30000, I_p: 1e-9 }, { C_s: 2e-4, C_c: 2e-4, I_p: 1e-12 }, { V_land: 100 }],
    ui: {
      controls: ['probe_convention', 'alpha', 'I_p', 'V_land', 'C_s', 'C_c', 'dE50', 'dE', 'B_r'],
      readouts: ['d_p', 'd_A', 'd_S', 'd_C', 'd_I', 'alpha_opt', 'd_p_opt'],
      aspect: '4 / 3', aspectPhone: '1 / 1',
      caption: 'The probe diameter (wine) and its four parts against the beam half-angle, on logarithmic axes, for the asked probe current. Diffraction falls with the angle, the aberrations rise with it, and the source image shrinks as the angle opens because the same current then needs less area. The dot marked optimum is the smallest probe. The FW50 sum uses the FW50 energy width ΔE₅₀, the classic sum the FWHM ΔE. Above about a nanoampere at 800 V the Coulomb repulsion between the electrons in the beam, which this model leaves out, starts to blur the probe as well.',
    },
    compute, draw, terms,
  };
});
