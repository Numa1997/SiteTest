/* The Electron Beam, from Tip to Measurement · physics/ch03.js
   Chapter 3, acceleration: what a voltage does to an electron's energy, momentum and wavelength, exactly (relativistically), and what
   deceleration to a lower landing voltage does to the beam angle. Pure module (physics/core.js pattern); mirrored by ref/ch03.py.

     E_0 = e V                         kinetic energy after a potential step V (energy conservation, chapter 1)
     gamma = 1 + e V / (m c^2)
     p^2 = 2 m e V (1 + e V / (2 m c^2)) = 2 m e V*      from (E_0 + m c^2)^2 = (p c)^2 + (m c^2)^2
     lambda = h / p                    de Broglie
     ang_mag = p_acc / p_land = sqrt(V*_acc / V*_land)    transverse momentum conserved in an axial field: tan(alpha) = p_perp / p_z */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./core.js'));
  else { root.EB = root.EB || {}; root.EB.ch03 = factory(root.EB.core); }
})(typeof self !== 'undefined' ? self : this, function (core) {
  'use strict';
  const { C } = core;
  const mc2 = C.m_e * C.c * C.c;
  const vstar = V => V * (1 + C.e * V / (2 * mc2));
  const lam = V => C.h / Math.sqrt(2 * C.m_e * C.e * vstar(V));
  const lamNR = V => C.h / Math.sqrt(2 * C.m_e * C.e * V);

  function compute(p) {
    const V = p.V_acc, Vl = p.V_land;
    const curve = [];
    for (let i = 0; i <= 60; i++) { const v = Math.pow(10, 1 + 5 * i / 60); curve.push(v, lam(v), lamNR(v)); }
    return {
      E_0: C.e * V, gamma: 1 + C.e * V / mc2, V_star: vstar(V), lambda_e: lam(V),
      V_star_land: vstar(Vl), lambda_land: lam(Vl), ang_mag: Math.sqrt(vstar(V) / vstar(Vl)), lambda_curve: curve,
    };
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

  // left (or above): the gun drawn (tip, extractor, anode at V_acc, retarding plate at the wafer); right (or below): lambda(V) on log axes.
  // Every word sits where nothing is drawn: the plate labels at the first free place beside the beam, the wafer's below its plate, the key
  // of the plot below its axis, and the two marks' words at the first free place of a few around their dots.
  function draw(ctx, w, h, p, out) {
    ctx.clearRect(0, 0, w, h);
    const narrow = w < 560 || h > w, gw = narrow ? w : w * 0.42, gh = narrow ? h * 0.52 : h, lab = labels(ctx, w, h);
    ctx.font = "11px 'IBM Plex Mono', monospace"; ctx.textAlign = 'left';
    // gun: vertical column, electrons go down
    const cx = gw / 2, y0 = 18, y1 = gh - 24, hw = gw * 0.38;
    ctx.fillStyle = '#efe4c8'; ctx.strokeStyle = '#3a322e'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(cx - 9, y0); ctx.lineTo(cx + 9, y0); ctx.lineTo(cx + 2, y0 + 36); ctx.arc(cx, y0 + 36, 2, 0, Math.PI); ctx.closePath(); ctx.fill(); ctx.stroke();
    lab.block([cx - 9, y0, cx + 9, y0 + 38]);
    const yE = y0 + 0.24 * (y1 - y0), yA = y0 + 0.46 * (y1 - y0), yW = y1 - 8;
    const plate = y => { ctx.fillStyle = '#d9d0c2'; ctx.fillRect(cx - hw, y, hw - 7, 6); ctx.fillRect(cx + 7, y, hw - 7, 6); ctx.strokeRect(cx - hw, y, hw - 7, 6); ctx.strokeRect(cx + 7, y, hw - 7, 6); lab.block([cx - hw, y, cx - 7, y + 6]); lab.block([cx + 7, y, cx + hw, y + 6]); };
    plate(yE); plate(yA);
    ctx.fillStyle = '#d9d0c2'; ctx.fillRect(cx - hw, yW, 2 * hw, 8); ctx.strokeRect(cx - hw, yW, 2 * hw, 8); lab.block([cx - hw, yW, cx + hw, yW + 8]);
    // the beam: a cone that narrows to the anode, then opens by ang_mag on the way down if decelerated
    ctx.strokeStyle = '#7a1f2b'; ctx.lineWidth = 1.5;
    // the beam spreads from the tip at a half-angle that stays the same down the column (slope s1 per pixel); in the last stretch, the
    // retarding field near the wafer, the half-angle is multiplied by ang_mag (chapter 3, the angle factor). Drawn with an exaggerated angle.
    const yR = yW - 0.16 * (y1 - y0), s1 = 0.10, s2 = Math.min(1.2, s1 * out.ang_mag);
    const wR = s1 * (yR - (y0 + 38)), wW = wR + s2 * (yW - yR);
    ctx.beginPath(); ctx.moveTo(cx, y0 + 38); ctx.lineTo(cx - wR, yR); ctx.lineTo(cx - wW, yW); ctx.moveTo(cx, y0 + 38); ctx.lineTo(cx + wR, yR); ctx.lineTo(cx + wW, yW); ctx.stroke();
    lab.line([cx, y0 + 38, cx - wR, yR, cx - wW, yW]); lab.line([cx, y0 + 38, cx + wR, yR, cx + wW, yW]);
    ctx.strokeStyle = '#8b8079'; ctx.lineWidth = 1; ctx.setLineDash([3, 3]); ctx.beginPath(); ctx.moveTo(cx - hw, yR); ctx.lineTo(cx + hw, yR); ctx.stroke(); ctx.setLineDash([]);
    lab.line([cx - hw, yR, cx + hw, yR]);
    ctx.fillStyle = '#5a504b';
    for (const [y, t] of [[yE, 'extractor'], [yA, 'anode: +' + core.fmt(p.V_acc, 3) + ' V']]) { const xb = cx + Math.max(12, 10 + s1 * (y + 18 - y0 - 38)); lab.put(t, [[xb, y + 18], [xb + 10, y + 18], [xb, y - 6], [cx - xb + cx, y + 18, 'right']]); }
    lab.put('wafer: lands at ' + core.fmt(p.V_land, 3) + ' V', [[cx - hw, yW + 21], [cx, yW + 21, 'center']]);
    // plot, with its key of two line samples below the voltage axis
    const px = narrow ? 52 : gw + 56, pw = (narrow ? w : w - gw) - (narrow ? 52 : 56) - 22;
    const rowKey = pw >= 250, keyH = rowKey ? 18 : 34;
    const py = narrow ? gh + 10 : 14, ph = h - py - 40 - (rowKey ? 0 : 16);
    const lx = v => px + (Math.log10(v) - 1) / 5 * pw, ly = l => py + (Math.log10(l) - Math.log10(4e-10)) / (Math.log10(8e-13) - Math.log10(4e-10)) * ph;
    ctx.strokeStyle = '#d9d0c2'; ctx.lineWidth = 1; ctx.__nocollide = true; ctx.strokeRect(px, py, pw, ph); ctx.__nocollide = false;   // the frame
    ctx.fillStyle = '#6f655f'; ctx.textAlign = 'center';
    for (let k = 1; k <= 6; k++) { const x = lx(Math.pow(10, k)); ctx.beginPath(); ctx.moveTo(x, py + ph); ctx.lineTo(x, py + ph + 4); ctx.stroke(); lab.line([x, py + ph, x, py + ph + 4]); ctx.fillText(['10 V', '100 V', '1 kV', '10 kV', '100 kV', '1 MV'][k - 1], x, py + ph + 15); }
    ctx.textAlign = 'right';
    for (const [l, t] of [[1e-10, '100 pm'], [1e-11, '10 pm'], [1e-12, '1 pm']]) { const y = ly(l); ctx.beginPath(); ctx.moveTo(px - 4, y); ctx.lineTo(px, y); ctx.stroke(); lab.line([px - 4, y, px, y]); ctx.fillText(t, px - 6, y + 4); }
    const cv = out.lambda_curve, n = cv.length / 3;
    const line = (k, col, dash) => {
      ctx.strokeStyle = col; ctx.setLineDash(dash); ctx.lineWidth = 2; ctx.beginPath();
      const xy = []; for (let i = 0; i < n; i++) { const X = lx(cv[3 * i]), Y = ly(cv[3 * i + k]); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); xy.push(X, Y); }
      ctx.stroke(); ctx.setLineDash([]); lab.line(xy);
    };
    line(2, '#8b8079', [5, 4]); line(1, '#7a1f2b', []);
    // the two marks: the dots first, then the words; the curve falls to the right, so above-right and below-left of a dot are free
    const dots = [[p.V_acc, out.lambda_e, 'column'], [p.V_land, out.lambda_land, 'landing']];
    ctx.fillStyle = '#1c1518';
    for (const [V, l] of dots) { ctx.beginPath(); ctx.arc(lx(V), ly(l), 4, 0, 2 * Math.PI); ctx.fill(); lab.block([lx(V) - 4, ly(l) - 4, lx(V) + 4, ly(l) + 4]); }
    const plotBox = [px, py, px + pw, py + ph];
    for (const [V, l, t] of dots) {
      const x = lx(V), y = ly(l), up = [[x + 7, y - 8], [x + 2, y - 10], [x + 14, y - 14]], dn = [[x - 7, y + 14, 'right'], [x - 2, y + 18, 'right'], [x - 14, y + 22, 'right']];
      lab.put(t, t === 'column' ? up.concat(dn) : dn.concat(up), 3, plotBox);
    }
    // the key
    const ky = py + ph + 34, items = [['λ exact', '#7a1f2b', []], ['λ without relativity (dashed)', '#8b8079', [5, 4]]];
    let kx = px - 40;
    items.forEach(([t, col, dash], i) => {
      const yk = rowKey ? ky : ky + 16 * i, xk = rowKey ? kx : px - 40;
      ctx.strokeStyle = col; ctx.setLineDash(dash); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(xk, yk - 4); ctx.lineTo(xk + 22, yk - 4); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = col; ctx.textAlign = 'left'; ctx.fillText(t, xk + 28, yk);
      kx += 28 + ctx.measureText(t).width + 18;
    });
  }

  return {
    id: 'ch03',
    inputs: ['V_acc', 'V_land'],
    outputs: ['E_0', 'lambda_e', 'gamma', 'V_star', 'V_star_land', 'lambda_land', 'ang_mag', 'lambda_curve'],
    tolerance: { rel: 1e-14, abs: 0, note: 'closed formulas in float64 on both sides' },
    cases: [{}, { V_acc: 100, V_land: 100 }, { V_acc: 3e4, V_land: 500 }, { V_acc: 3e5, V_land: 3e4 }],
    ui: {
      controls: ['V_acc', 'V_land'],
      readouts: ['V_star', 'lambda_e', 'lambda_land', 'ang_mag'],
      aspect: '1 / 1', aspectPhone: '3 / 4',
      caption: 'First panel: the gun drawn (not to scale), the beam spreading from the tip at one angle down the column and, below the dashed line where the retarding field acts, at an angle larger by the factor of (3.4) when it is slowed. Second panel: the electron wavelength against voltage, exact (wine) and without relativity (grey, dashed), with the column and landing values marked. A landing voltage above the column voltage means the beam is accelerated again before the wafer.',
    },
    compute, draw,
  };
});
