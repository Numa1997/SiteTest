/* Project 07 · chapter 2 · the source on screen.  Browser only: reads EB_CH02 (physics/ch02.js), draws four canvases.
   Pipeline (CLAUDE.md, "A data table is a pipeline"): compute() runs the model when a control changes and writes every number into
   STORE at the line that computes it; the frame loop and the readouts only read STORE (and mix the clean and covered parts with the
   coverage theta(t); nothing is recomputed for display). Nothing reacts to the pointer merely crossing a figure. */
(function () {
  'use strict';
  const E = window.EB_CH02, eV = E.K.e;
  const root = document.getElementById('ebsim');
  if (!root || !E) return;
  const $ = id => document.getElementById(id);
  const STORE = window.EB_CH02_STORE = { inputs: {}, apex: {}, handover: {}, timeline: {}, notes: 'every value written where it is computed; see compute()' };
  const put = (grp, name, value, unit, how) => { (STORE[grp] = STORE[grp] || {})[name] = { value, unit, how }; return value; };

  /* ------------------------------------------------------------------ controls */
  const log = (lo, hi) => ({ to: x => Math.exp(Math.log(lo) + (Math.log(hi) - Math.log(lo)) * x), from: v => (Math.log(v) - Math.log(lo)) / (Math.log(hi) - Math.log(lo)) });
  const lin = (lo, hi) => ({ to: x => lo + (hi - lo) * x, from: v => (v - lo) / (hi - lo) });
  const CTL = {
    r:    { map: log(10, 600),     fmt: v => v.toFixed(0) + ' nm',        step: 0.002 },
    V:    { map: log(100, 8000),   fmt: v => v.toFixed(0) + ' V',         step: 0.002 },
    k:    { map: lin(1, 12),       fmt: v => v.toFixed(1),                step: 0.005 },
    phi:  { map: lin(2, 6),        fmt: v => v.toFixed(2) + ' eV',        step: 0.0025 },
    T:    { map: lin(250, 2400),   fmt: v => v.toFixed(0) + ' K',         step: 0.002 },
    p:    { map: log(1e-11, 1e-6), fmt: v => v.toExponential(1).replace('e-', '×10⁻').replace('e+', '×10') + ' Pa', step: 0.002 },
    sk:   { map: lin(0.05, 1),     fmt: v => v.toFixed(2),                step: 0.01 },
    Ed:   { map: lin(0.8, 3.5),    fmt: v => v.toFixed(2) + ' eV',        step: 0.005 },
    dads: { map: lin(0, 2),        fmt: v => v.toFixed(2) + ' eV',        step: 0.005 },
    Tfl:  { map: lin(500, 2200),   fmt: v => v.toFixed(0) + ' K',         step: 0.005 },
    tfl:  { map: lin(1, 30),       fmt: v => v.toFixed(0) + ' s',         step: 0.01 },
    thr:  { map: lin(0.3, 0.95),   fmt: v => v.toFixed(2),                step: 0.005 },
  };
  const PRESETS = {
    cold:     { r: 50, V: 1000, k: 5, phi: 4.5, T: 300, p: 1e-8, sk: 0.535, Ed: 1.9, dads: 1.0, Tfl: 1000, tfl: 5, thr: 0.7 },
    schottky: { r: 500, V: 2000, k: 8, phi: 2.9, T: 1800, p: 1e-8, sk: 0.535, Ed: 1.9, dads: 1.0, Tfl: 1000, tfl: 5, thr: 0.7 },
  };
  // the exact value of each control lives in VAL; the slider position is only a way to change it (a slider has a finite step,
  // and the current depends on the voltage as F^17: 0.4 % of V would be 7 % of the current)
  const VAL = {};
  function setCtl(id, v) { VAL[id] = v; $('eb-' + id).value = CTL[id].map.from(v); show(id); }
  function getCtl(id) { return VAL[id]; }
  function show(id) {
    const el = $('eb-' + id), x = parseFloat(el.value);
    el.style.setProperty('--p', (CTL[id].map.from(VAL[id]) * 100).toFixed(1) + '%');
    $('eb-' + id + '-out').textContent = CTL[id].fmt(VAL[id]);
  }
  function fromSlider(id) { VAL[id] = CTL[id].map.to(parseFloat($('eb-' + id).value)); show(id); }
  Object.keys(CTL).forEach(id => { const el = $('eb-' + id); el.min = 0; el.max = 1; el.step = CTL[id].step / 4; });
  const MASS = { H2: 2.016, N2: 28.0134, CO: 28.0101 };

  /* ------------------------------------------------------------------ model: runs when a control changes */
  let M = null;           // the computed state, see compute()
  let busy = false, dirty = true, tCursor = 0, playing = true, lastTs = 0;

  function readInputs() {
    const I = {};
    Object.keys(CTL).forEach(id => { I[id] = getCtl(id); });
    I.gas = $('eb-gas').value; I.auto = $('eb-auto').checked;
    return I;
  }

  function compute() {
    const I = readInputs(), nm = 1e-9;
    ['r', 'V', 'k', 'phi', 'T', 'p'].forEach(n => put('inputs', n, I[n], { r: 'nm', V: 'V', k: '1', phi: 'eV', T: 'K', p: 'Pa' }[n], 'control'));
    const r = I.r * nm, V = I.V, k = I.k, phi = I.phi * eV, T = I.T, phiV = (I.phi + I.dads) * eV;
    const F0 = put('apex', 'F', E.tipField(V, r, k), 'V/m', 'F = V/(k r), @eq:apexfield@');
    const mC = E.emissionModel(F0, phi, T), mV = E.emissionModel(F0, phiV, T);
    put('apex', 'f', mC.f, '1', 'scaled field, @eq:roots@'); put('apex', 'J_clean', mC.J, 'A/m²', 'master formula @eq:Jint@');
    put('apex', 'J_covered', mV.J, 'A/m²', 'same, work function raised by the assumed Δφ_ads');
    const cap = { r, k, T, nodes: 16 };
    const IC = put('apex', 'I_clean', E.tipCurrent(V, { ...cap, phi }), 'A', 'cap integral of J, F = F0 cos θ');
    const IV = put('apex', 'I_covered', E.tipCurrent(V, { ...cap, phi: phiV }), 'A', 'cap integral, covered work function');
    // sweep for the Fowler-Nordheim plot: 13 voltages from 0.7 V to 1.15 V
    const sweep = [];
    for (let i = 0; i < 13; i++) {
      const v = V * (0.7 + 0.45 * i / 12);
      sweep.push({ V: v, Ic: E.tipCurrent(v, { ...cap, phi }), Iv: E.tipCurrent(v, { ...cap, phi: phiV }) });
    }
    // energy distribution on a common grid (relative to the Fermi level), clean and covered
    const e0 = mC.peak - 1.6 * eV, e1 = mC.peak + 1.1 * eV, n = 400, grid = [], Pc = [], Pv = [];
    const interp = (m, x) => { const w = m.w, dw = w[1] - w[0], t = (x - w[0]) / dw, i = Math.floor(t); if (i < 0 || i >= w.length - 1) return 0; const u = t - i; return m.P[i] * (1 - u) + m.P[i + 1] * u; };
    for (let i = 0; i < n; i++) { const x = e0 + (e1 - e0) * i / (n - 1); grid.push(x); Pc.push(interp(mC, x)); Pv.push(interp(mV, x)); }
    // contamination timeline: the whole run at once (exact solution of the rate equation), played back afterwards
    const mg = MASS[I.gas], Ns = 1e19;
    const rho = IC > 0 ? IV / IC : 1;
    const a = I.sk * E.hkFlux(I.p, 300, mg) / Ns, kd = E.kDes(I.Ed, T);
    put('timeline', 'flux', E.hkFlux(I.p, 300, mg), 'm⁻² s⁻¹', 'Hertz–Knudsen, @eq:HK@');
    put('timeline', 'a', a, 's⁻¹', 'κ s Φ / N_s, @eq:rate@'); put('timeline', 'k_d', kd, 's⁻¹', 'ν0 exp(−E_d/kT)');
    const thStar = rho < 1 ? (1 - I.thr) / (1 - rho) : Infinity;
    const tStar = isFinite(thStar) ? E.timeToCoverage(thStar, a, kd) : Infinity;
    const tmax = Math.min(4e7, Math.max(900, isFinite(tStar) ? 3.4 * tStar : 6 * 3600));
    const cyc = E.cycle({ pPa: I.p, Tg: 300, mu: mg, Ns, s: I.sk, kappa: 1, Ed: I.Ed, T, Tflash: I.Tfl, tflash: I.tfl, thr: I.auto ? I.thr : 0, theta0: 0, rho, tmax, dt: tmax / 4000 });
    put('timeline', 'tmax', tmax, 's', 'run length: 3.4 intervals between flashes'); put('timeline', 'rho', rho, '1', 'I_covered / I_clean');
    M = { I, F0, mC, mV, IC, IV, sweep, grid, Pc, Pv, cyc, rho, tmax, a, kd, tStar, V, r };
    tCursor = Math.min(tCursor, tmax); dirty = false;
    $('eb-scrub').max = tmax; $('eb-scrub').step = tmax / 2000;
    state(); drawStatic(); frame(0);
  }

  /* ------------------------------------------------------------------ state at the playback cursor (mixes clean and covered parts) */
  function stateAt(t) {
    const c = M.cyc, ts = c.t; let lo = 0, hi = ts.length - 1;
    while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (ts[mid] <= t) lo = mid; else hi = mid; }
    const th = c.theta[lo], rat = c.ratio[lo];
    let since = t, lastFlash = null; for (const f of c.flashes) if (f <= t) lastFlash = f;
    if (lastFlash !== null) since = t - lastFlash;
    const flashing = lastFlash !== null && t - lastFlash < M.I.tfl && Number.isNaN(c.ratio[lo]);
    return { th: Math.min(1, Math.max(0, th)), ratio: rat, since, flashing, nflash: c.flashes.filter(f => f <= t).length };
  }
  function mixture(th) {
    const m = M, J = (1 - th) * m.mC.J + th * m.mV.J;
    const Ie = (1 - th) * m.IC + th * m.IV;
    const Br = (1 - th) * m.mC.B_r + th * m.mV.B_r;
    const met = J > 0 ? ((1 - th) * m.mC.J * m.mC.meanEt + th * m.mV.J * m.mV.meanEt) / J : 0;
    const P = m.Pc.map((x, i) => (1 - th) * x + th * m.Pv[i]);
    let ip = 0; for (let i = 1; i < P.length; i++) if (P[i] > P[ip]) ip = i;
    const dw = m.grid[1] - m.grid[0], hmax = P[ip] / 2; let l = ip, r = ip;
    while (l > 0 && P[l] > hmax) l--; while (r < P.length - 1 && P[r] > hmax) r++;
    // crossings between grid points by linear interpolation (the display grid has 400 points)
    const xl = l < ip ? l + (hmax - P[l]) / (P[l + 1] - P[l]) : l, xr = r > ip ? r - 1 + (P[r - 1] - hmax) / (P[r - 1] - P[r]) : r;
    const fwhm = P[ip] > 0 ? (xr - xl) * dw : 0;
    return { J, Ie, Br, met, P, fwhm, dE: fwhm, dv: 2 * m.r * Math.sqrt(met / (E.K.e * m.V)) };
  }

  /* ------------------------------------------------------------------ drawing */
  const C = { ink: '#1c1518', ink2: '#3a322e', wine: '#7a1f2b', rose: '#e2a2aa', tan: '#7a4b12', muted: '#8b8079', rule: '#d9d0c2', card: '#fffaf3', soft: '#ece5d8' };
  function ctxOf(id) {
    const cv = $(id), box = cv.parentElement, dpr = Math.min(2, window.devicePixelRatio || 1);
    const w = box.clientWidth, h = box.clientHeight;
    if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
    const g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
    return { g, w, h };
  }
  function axes(g, w, h, m, xlab, ylab, xt, yt) {
    g.save(); g.font = "10.5px 'IBM Plex Mono', monospace"; g.fillStyle = C.muted; g.strokeStyle = C.soft; g.lineWidth = 1;
    xt.forEach(([x, s]) => { g.beginPath(); g.moveTo(x, m.t); g.lineTo(x, h - m.b); g.stroke(); g.textAlign = 'center'; g.fillText(s, x, h - m.b + 14); });
    yt.forEach(([y, s]) => { g.beginPath(); g.moveTo(m.l, y); g.lineTo(w - m.r, y); g.stroke(); g.textAlign = 'right'; g.fillText(s, m.l - 5, y + 3); });
    g.strokeStyle = '#cdc1ae'; g.strokeRect(m.l, m.t, w - m.l - m.r, h - m.t - m.b);
    g.fillStyle = C.ink2; g.font = "11px 'IBM Plex Sans', sans-serif"; g.textAlign = 'center'; g.fillText(xlab, (m.l + w - m.r) / 2, h - 4);
    g.save(); g.translate(11, (m.t + h - m.b) / 2); g.rotate(-Math.PI / 2); g.fillText(ylab, 0, 0); g.restore(); g.restore();
  }
  const nice = (lo, hi, n) => { const span = hi - lo, raw = span / n, mag = Math.pow(10, Math.floor(Math.log10(raw))); let st = mag; for (const q of [1, 2, 2.5, 5, 10]) { if (raw <= q * mag) { st = q * mag; break; } } const o = []; for (let t = Math.ceil(lo / st - 1e-9) * st; t <= hi + 1e-9 * span; t += st) o.push(t); return o; };

  // ---- Fowler–Nordheim plot ---------------------------------------------------------------------------------
  function drawFN(th) {
    const { g, w, h } = ctxOf('eb-fn'), m = { l: 58, r: 12, t: 10, b: 36 };
    const pts = M.sweep.map(s => ({ x: 1000 / s.V, c: Math.log(s.Ic / (s.V * s.V)), v: Math.log(s.Iv / (s.V * s.V)), y: Math.log(((1 - th) * s.Ic + th * s.Iv) / (s.V * s.V)) }));
    const ys = pts.flatMap(p => [p.c, isFinite(p.v) ? p.v : p.c, isFinite(p.y) ? p.y : p.c]).filter(isFinite);
    let y0 = Math.min(...ys), y1 = Math.max(...ys); const pad = (y1 - y0) * 0.08 + 0.2; y0 -= pad; y1 += pad;
    const x0 = Math.min(...pts.map(p => p.x)), x1 = Math.max(...pts.map(p => p.x)), dx = (x1 - x0) * 0.06;
    const X = x => m.l + (x - (x0 - dx)) / ((x1 + dx) - (x0 - dx)) * (w - m.l - m.r), Y = y => h - m.b - (y - y0) / (y1 - y0) * (h - m.t - m.b);
    axes(g, w, h, m, '1000 / V  (1/kV)', 'ln( I / V² )', nice(x0 - dx, x1 + dx, 4).map(x => [X(x), x.toFixed(2)]), nice(y0, y1, 4).map(y => [Y(y), y.toFixed(0)]));
    // clean-tip line through the sweep (least squares) and its slope
    const n = pts.length, sx = pts.reduce((a, p) => a + p.x, 0), sy = pts.reduce((a, p) => a + p.c, 0), sxx = pts.reduce((a, p) => a + p.x * p.x, 0), sxy = pts.reduce((a, p) => a + p.x * p.c, 0);
    const slope = (n * sxy - sx * sy) / (n * sxx - sx * sx), icpt = (sy - slope * sx) / n;
    g.strokeStyle = C.muted; g.setLineDash([5, 4]); g.lineWidth = 1.4; g.beginPath(); g.moveTo(X(x0 - dx), Y(icpt + slope * (x0 - dx))); g.lineTo(X(x1 + dx), Y(icpt + slope * (x1 + dx))); g.stroke(); g.setLineDash([]);
    if (th > 0.002) { g.strokeStyle = C.rose; g.lineWidth = 1.6; g.beginPath(); pts.forEach((p, i) => { const px = X(p.x), py = Y(isFinite(p.v) ? p.v : y0); i ? g.lineTo(px, py) : g.moveTo(px, py); }); g.stroke(); }
    g.strokeStyle = C.wine; g.lineWidth = 2.2; g.beginPath(); pts.forEach((p, i) => { const px = X(p.x), py = Y(isFinite(p.y) ? p.y : y0); i ? g.lineTo(px, py) : g.moveTo(px, py); }); g.stroke();
    const op = pts.reduce((a, p) => Math.abs(p.x - 1000 / M.V) < Math.abs(a.x - 1000 / M.V) ? p : a, pts[0]);
    g.fillStyle = C.wine; g.beginPath(); g.arc(X(op.x), Y(isFinite(op.y) ? op.y : y0), 4.6, 0, 7); g.fill();
    const bphi = 6.83089 * Math.pow(M.I.phi, 1.5);        // b φ^{3/2}, V/nm
    put('apex', 'FN_slope', slope * 1000, 'V', 'least-squares slope of ln(I/V²) against 1/V, clean tip');
    put('apex', 'zeta_from_slope', Math.abs(slope * 1000) / (bphi * (1 - M.mC.f / 6)), 'nm', 'ζ = |S| / (b φ^{3/2} (1 − f/6)), @eq:FNslope@');
  }

  // ---- energy distribution ----------------------------------------------------------------------------------
  function drawEnergy(mx) {
    const { g, w, h } = ctxOf('eb-en'), m = { l: 50, r: 12, t: 10, b: 36 }, gr = M.grid, e0 = gr[0] / eV, e1 = gr[gr.length - 1] / eV;
    const pmax = Math.max(...M.Pc) || 1;
    const X = x => m.l + (x - e0) / (e1 - e0) * (w - m.l - m.r), Y = y => h - m.b - y / (pmax * 1.08) * (h - m.t - m.b);
    axes(g, w, h, m, 'energy relative to the Fermi level  ε  (eV)', 'P(ε) / peak (clean)', nice(e0, e1, 5).map(x => [X(x), x.toFixed(1)]), [0, 0.5, 1].map(y => [Y(y * pmax), y.toFixed(1)]));
    const draw = (P, col, lw, fill) => { g.beginPath(); P.forEach((v, i) => { const px = X(gr[i] / eV), py = Y(v); i ? g.lineTo(px, py) : g.moveTo(px, py); }); if (fill) { g.lineTo(X(e1), Y(0)); g.lineTo(X(e0), Y(0)); g.closePath(); g.fillStyle = fill; g.fill(); } g.strokeStyle = col; g.lineWidth = lw; g.stroke(); };
    draw(M.Pc, C.muted, 1.3);
    draw(mx.P, C.wine, 2.2, 'rgba(122,31,43,.14)');
    g.strokeStyle = C.ink; g.setLineDash([5, 4]); g.lineWidth = 1.2; g.beginPath(); g.moveTo(X(0), m.t); g.lineTo(X(0), h - m.b); g.stroke(); g.setLineDash([]);
    g.fillStyle = C.ink2; g.font = "10.5px 'IBM Plex Mono', monospace"; g.textAlign = 'left'; g.fillText('Fermi level', X(0) + 4, m.t + 11);
    const top = M.mC.top / eV; if (top > e0 && top < e1) { g.strokeStyle = C.tan; g.beginPath(); g.moveTo(X(top), m.t); g.lineTo(X(top), h - m.b); g.stroke(); g.fillStyle = C.tan; g.fillText('barrier top', X(top) + 4, m.t + 24); }
    // FWHM bar of the mixture
    const P = mx.P; let ip = 0; for (let i = 1; i < P.length; i++) if (P[i] > P[ip]) ip = i;
    if (P[ip] > 0) { const hm = P[ip] / 2; let l = ip, r = ip; while (l > 0 && P[l] > hm) l--; while (r < P.length - 1 && P[r] > hm) r++; const dwv = gr[1] - gr[0], xl = gr[0] + (l < ip ? l + (hm - P[l]) / (P[l + 1] - P[l]) : l) * dwv, xr = gr[0] + (r > ip ? r - 1 + (P[r - 1] - hm) / (P[r - 1] - P[r]) : r) * dwv; g.strokeStyle = C.ink; g.lineWidth = 1.6; g.beginPath(); g.moveTo(X(xl / eV), Y(hm)); g.lineTo(X(xr / eV), Y(hm)); g.stroke(); g.fillStyle = C.ink; g.textAlign = 'left'; g.fillText('ΔE = ' + (mx.fwhm / eV).toFixed(3) + ' eV', Math.min(X(xr / eV) + 6, w - 105), Y(hm) - 6); }
  }

  // ---- coverage and current against time ---------------------------------------------------------------------
  function timeUnit(tmax) { return tmax < 7200 ? [1 / 60, 'min'] : tmax < 3 * 86400 ? [1 / 3600, 'h'] : [1 / 86400, 'days']; }
  function drawTime(t) {
    const { g, w, h } = ctxOf('eb-tm'), m = { l: 50, r: 12, t: 10, b: 36 }, [u, un] = timeUnit(M.tmax), c = M.cyc;
    const X = x => m.l + x / M.tmax * (w - m.l - m.r), Y = y => h - m.b - y / 1.2 * (h - m.t - m.b);
    axes(g, w, h, m, 'time (' + un + ')', 'θ, I / I₀', nice(0, M.tmax * u, 5).map(x => [X(x / u), String(+x.toFixed(2))]), [0, 0.25, 0.5, 0.75, 1].map(y => [Y(y), String(y)]));
    if (M.I.auto) { g.strokeStyle = C.muted; g.setLineDash([3, 4]); g.beginPath(); g.moveTo(m.l, Y(M.I.thr)); g.lineTo(w - m.r, Y(M.I.thr)); g.stroke(); g.setLineDash([]); }
    c.flashes.forEach(f => { g.strokeStyle = C.rose; g.lineWidth = 1; g.beginPath(); g.moveTo(X(f), m.t); g.lineTo(X(f), h - m.b); g.stroke(); });
    const line = (arr, col, lw) => { g.strokeStyle = col; g.lineWidth = lw; g.beginPath(); let pen = false; c.t.forEach((tt, i) => { const v = arr[i]; if (!Number.isFinite(v)) { pen = false; return; } const px = X(tt), py = Y(v); pen ? g.lineTo(px, py) : g.moveTo(px, py); pen = true; }); g.stroke(); };
    line(c.theta, C.ink2, 1.8); line(c.ratio, C.wine, 2.4);
    g.strokeStyle = C.ink; g.lineWidth = 1.2; g.beginPath(); g.moveTo(X(t), m.t); g.lineTo(X(t), h - m.b); g.stroke();
    g.font = "10.5px 'IBM Plex Mono', monospace"; g.textAlign = 'left'; g.fillStyle = C.ink2; g.fillText('θ coverage', m.l + 8, m.t + 12); g.fillStyle = C.wine; g.fillText('I / I₀', m.l + 90, m.t + 12);
  }

  // ---- the tip --------------------------------------------------------------------------------------------------
  const dots = []; for (let i = 0; i < 60; i++) dots.push({ s: (i * 0.6180339887) % 1, a: ((i * 0.7548776662) % 1) });
  function drawTip(st, mx, ts) {
    const { g, w, h } = ctxOf('eb-tip');
    const apexX = w * 0.60, apexY = h * 0.5, rpx = 12 + 44 * (Math.log(M.I.r / 10) / Math.log(60));        // drawn radius: 12 to 56 px for 10 to 600 nm
    const anodeX = w * 0.90, ang = 0.16;
    // anode with hole
    g.fillStyle = '#d9d0c2'; g.strokeStyle = C.ink; g.lineWidth = 1.2; g.fillRect(anodeX, 0, 10, h * 0.40); g.strokeRect(anodeX, 0, 10, h * 0.40); g.fillRect(anodeX, h * 0.60, 10, h * 0.40); g.strokeRect(anodeX, h * 0.60, 10, h * 0.40);
    g.fillStyle = C.ink2; g.font = "10.5px 'IBM Plex Mono', monospace"; g.textAlign = 'center'; g.fillText('anode 0 V', anodeX + 5, 14);
    // shank: cone with half angle ang ending in a sphere of radius rpx
    const cx = apexX - rpx, tx = cx - rpx * Math.sin(ang), ty = rpx * Math.cos(ang), L = apexX;
    const glow = st.flashing;
    g.fillStyle = glow ? '#f2b8bf' : '#efe4c8'; g.strokeStyle = glow ? C.wine : C.ink; g.lineWidth = 1.6;
    g.beginPath(); g.moveTo(10, apexY - ty - (tx - 10) * Math.tan(ang)); g.lineTo(tx, apexY - ty); g.arc(cx, apexY, rpx, -(Math.PI / 2 - ang), Math.PI / 2 - ang); g.lineTo(10, apexY + ty + (tx - 10) * Math.tan(ang)); g.closePath(); g.fill(); g.stroke();
    // field lines: more of them for a higher field
    const nl = Math.max(3, Math.min(13, Math.round(2 + 1.6 * M.F0 * 1e-9))), lines = [];
    for (let i = 0; i < nl; i++) {
      const a = (i / (nl - 1) - 0.5) * 1.7, x0 = cx + rpx * Math.cos(a), y0 = apexY + rpx * Math.sin(a), x1 = anodeX, y1 = apexY + a * h * 0.34;
      lines.push([x0, y0, x0 + 60 * Math.cos(a) + 30, y0 + 60 * Math.sin(a), x1 - 70, y1, x1, y1]);
      g.strokeStyle = 'rgba(122,31,43,.30)'; g.setLineDash([5, 4]); g.lineWidth = 1; g.beginPath(); g.moveTo(x0, y0); g.bezierCurveTo(lines[i][2], lines[i][3], lines[i][4], lines[i][5], x1, y1); g.stroke(); g.setLineDash([]);
    }
    // adsorbed atoms on the cap
    const na = Math.round(st.th * 40);
    g.fillStyle = C.ink;
    for (let i = 0; i < na; i++) { const a = (dots[i].a - 0.5) * 2.4, px = cx + (rpx + 3) * Math.cos(a), py = apexY + (rpx + 3) * Math.sin(a); g.beginPath(); g.arc(px, py, 2.4, 0, 7); g.fill(); }
    // electrons moving along the lines: how many follows the logarithm of the current
    const level = st.flashing ? 0 : Math.max(0, Math.min(1, (Math.log10(Math.max(mx.Ie, 1e-15)) + 12) / 9));
    const ne = Math.round(level * 34), bez = (p, s) => { const u = 1 - s; return [u * u * u * p[0] + 3 * u * u * s * p[2] + 3 * u * s * s * p[4] + s * s * s * p[6], u * u * u * p[1] + 3 * u * u * s * p[3] + 3 * u * s * s * p[5] + s * s * s * p[7]]; };
    g.fillStyle = C.wine;
    for (let i = 0; i < ne; i++) { const L_ = lines[i % nl], s = (dots[i].s + ts * 0.00045 * (0.7 + dots[i].a)) % 1, [px, py] = bez(L_, s); g.beginPath(); g.arc(px, py, 2.3, 0, 7); g.fill(); }
    g.fillStyle = C.ink2; g.textAlign = 'left'; g.fillText('r = ' + M.I.r.toFixed(0) + ' nm (apex on a logarithmic scale; shank and gap not to scale)', 10, h - 8);
    if (glow) { g.fillStyle = C.wine; g.font = "600 12px 'IBM Plex Mono', monospace"; g.fillText('FLASH: tip heated to ' + M.I.Tfl.toFixed(0) + ' K', 10, 18); }
  }

  /* ------------------------------------------------------------------ frame loop and readouts */
  let st = null, mx = null;
  function state() { st = stateAt(tCursor); mx = mixture(st.th); store(); }
  function store() {
    put('handover', 'I_e', mx.Ie, 'A', '(1−θ) I_clean + θ I_covered'); put('handover', 'B_r', mx.Br, 'A m⁻² sr⁻¹ V⁻¹', 'e j(ε_t=0)/π, mixed with θ');
    put('handover', 'dE', mx.fwhm / eV, 'eV', 'FWHM of the mixed distribution'); put('handover', 'd_v', mx.dv * 1e9, 'nm', '2 r sqrt(<ε_t>/(eV)), @eq:bimp@');
    put('timeline', 'theta', st.th, '1', 'rate equation, exact'); put('timeline', 'I_over_I0', Number.isFinite(st.ratio) ? st.ratio : null, '1', '(1−θ)+θρ');
    put('timeline', 't', tCursor, 's', 'playback cursor'); put('timeline', 'since_flash', st.since, 's', 'time since the last flash'); put('timeline', 'flashes', st.nflash, '1', 'flashes so far');
  }
  function drawStatic() { /* nothing is static: all canvases redraw each frame; kept for clarity */ }
  function frame(ts) {
    if (!M) return;
    if (playing && lastTs) { const speed = parseFloat($('eb-speed').value); tCursor += (ts - lastTs) / 1000 * speed; if (tCursor > M.tmax) tCursor = 0; }
    lastTs = ts; $('eb-scrub').value = tCursor;
    state(); drawTip(st, mx, ts); drawFN(st.th); drawEnergy(mx); drawTime(tCursor);
  }
  function loop(ts) { try { if (dirty && !busy) { busy = true; setTimeout(() => { $('eb-status').textContent = 'computing…'; setTimeout(() => { compute(); $('eb-status').textContent = ''; busy = false; }, 10); }, 0); } else frame(ts); } catch (e) { $('eb-status').textContent = 'error: ' + e.message; console.error(e); return; } requestAnimationFrame(loop); }

  const fmtS = s => s < 120 ? s.toFixed(0) + ' s' : s < 7200 ? (s / 60).toFixed(0) + ' min' : s < 172800 ? (s / 3600).toFixed(1) + ' h' : (s / 86400).toFixed(1) + ' days';
  const sci = (v, d) => { if (!isFinite(v) || v === 0) return '0'; const e = Math.floor(Math.log10(Math.abs(v))); return (v / Math.pow(10, e)).toFixed(d) + '×10' + String(e).replace('-', '⁻').replace(/\d/g, c => '⁰¹²³⁴⁵⁶⁷⁸⁹'[c]); };
  function readouts() {                                  // text rewritten 4 times a second at most
    if (!M || !st) return;
    const R = {
      'eb-o-F': (M.F0 * 1e-9).toFixed(2) + ' V/nm (f = ' + M.mC.f.toFixed(3) + ')', 'eb-o-reg': M.mC.regime.replace('emission', ''),
      'eb-o-I': sci(mx.Ie, 2) + ' A', 'eb-o-B': sci(mx.Br, 2) + ' A m⁻² sr⁻¹ V⁻¹', 'eb-o-dE': (mx.fwhm / eV).toFixed(3) + ' eV', 'eb-o-dv': (mx.dv * 1e9).toFixed(2) + ' nm',
      'eb-o-th': (st.th * 100).toFixed(2) + ' %', 'eb-o-r': Number.isFinite(st.ratio) ? st.ratio.toFixed(3) : 'flashing', 'eb-o-t': fmtS(st.since), 'eb-o-n': String(st.nflash),
      'eb-o-fl': sci(E.hkFlux(M.I.p, 300, MASS[M.I.gas]), 2) + ' m⁻² s⁻¹', 'eb-o-ml': fmtS(1e19 / E.hkFlux(M.I.p, 300, MASS[M.I.gas])),
    };
    Object.keys(R).forEach(id => { const el = $(id); if (el && el.textContent !== R[id]) el.textContent = R[id]; });
  }
  setInterval(readouts, 250);

  /* ------------------------------------------------------------------ wiring */
  let deb = 0; const touch = () => { clearTimeout(deb); deb = setTimeout(() => { dirty = true; }, 120); };
  Object.keys(CTL).forEach(id => $('eb-' + id).addEventListener('input', () => { fromSlider(id); touch(); }));
  ['eb-gas', 'eb-auto'].forEach(id => $(id).addEventListener('change', touch));
  $('eb-play').addEventListener('click', () => { playing = !playing; $('eb-play').textContent = playing ? 'Pause' : 'Play'; });
  $('eb-scrub').addEventListener('input', () => { tCursor = parseFloat($('eb-scrub').value); if (playing) { playing = false; $('eb-play').textContent = 'Play'; } });
  $('eb-flash').addEventListener('click', () => {            // restart the run from a clean tip
    tCursor = 0; lastTs = 0;
  });
  document.querySelectorAll('[data-eb-preset]').forEach(b => b.addEventListener('click', () => { const P = PRESETS[b.dataset.ebPreset]; Object.keys(P).forEach(k => setCtl(k, P[k])); tCursor = 0; touch(); }));
  Object.keys(PRESETS.cold).forEach(k => setCtl(k, PRESETS.cold[k]));
  window.addEventListener('resize', () => { if (M) frame(lastTs); });
  requestAnimationFrame(loop);
})();
