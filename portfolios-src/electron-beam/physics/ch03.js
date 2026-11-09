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

  // left: the gun drawn (tip, extractor, anode at V_acc, retarding plate at the wafer); right: lambda(V) on log axes
  function draw(ctx, w, h, p, out) {
    ctx.clearRect(0, 0, w, h);
    const narrow = w < 560, gw = narrow ? w : w * 0.42, gh = narrow ? h * 0.42 : h;
    ctx.font = "11px 'IBM Plex Mono', monospace"; ctx.textAlign = 'left';
    // gun: vertical column, electrons go down
    const cx = gw / 2, y0 = 18, y1 = gh - 16;
    ctx.fillStyle = '#efe4c8'; ctx.strokeStyle = '#3a322e'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(cx - 9, y0); ctx.lineTo(cx + 9, y0); ctx.lineTo(cx + 2, y0 + 36); ctx.arc(cx, y0 + 36, 2, 0, Math.PI); ctx.closePath(); ctx.fill(); ctx.stroke();
    const plate = (y, label) => { ctx.fillStyle = '#d9d0c2'; ctx.fillRect(cx - gw * 0.38, y, gw * 0.38 - 7, 6); ctx.fillRect(cx + 7, y, gw * 0.38 - 7, 6); ctx.strokeRect(cx - gw * 0.38, y, gw * 0.38 - 7, 6); ctx.strokeRect(cx + 7, y, gw * 0.38 - 7, 6); ctx.fillStyle = '#5a504b'; ctx.fillText(label, cx + gw * 0.38 - 2 > gw - 4 ? 4 : cx + 10, y - 4); };
    const yE = y0 + 0.24 * (y1 - y0), yA = y0 + 0.46 * (y1 - y0), yW = y1 - 8;
    plate(yE, 'extractor'); plate(yA, 'anode: +' + core.fmt(p.V_acc, 3) + ' V');
    ctx.fillStyle = '#d9d0c2'; ctx.fillRect(cx - gw * 0.38, yW, gw * 0.76, 8); ctx.strokeRect(cx - gw * 0.38, yW, gw * 0.76, 8);
    ctx.fillStyle = '#5a504b'; ctx.fillText('wafer: lands at ' + core.fmt(p.V_land, 3) + ' V', cx - gw * 0.38, yW - 5);
    // the beam: a cone that narrows to the anode, then opens by ang_mag on the way down if decelerated
    ctx.strokeStyle = '#7a1f2b'; ctx.lineWidth = 1.5;
    const a1 = 0.06 * gw, a2 = Math.min(gw * 0.36, a1 * out.ang_mag);
    ctx.beginPath(); ctx.moveTo(cx, y0 + 38); ctx.lineTo(cx - a1 * 0.6, yA); ctx.lineTo(cx - a2 * 0.6, yW); ctx.moveTo(cx, y0 + 38); ctx.lineTo(cx + a1 * 0.6, yA); ctx.lineTo(cx + a2 * 0.6, yW); ctx.stroke();
    // plot
    const px = narrow ? 44 : gw + 52, py = narrow ? gh + 10 : 14, pw = (narrow ? w : w - gw) - 66, ph = (narrow ? h - gh : h) - 44;
    const lx = v => px + (Math.log10(v) - 1) / 5 * pw, ly = l => py + (Math.log10(l) - Math.log10(4e-10)) / (Math.log10(8e-13) - Math.log10(4e-10)) * ph;
    ctx.strokeStyle = '#d9d0c2'; ctx.lineWidth = 1; ctx.strokeRect(px, py, pw, ph);
    ctx.fillStyle = '#6f655f'; ctx.textAlign = 'center';
    for (let k = 1; k <= 6; k++) { const x = lx(Math.pow(10, k)); ctx.beginPath(); ctx.moveTo(x, py + ph); ctx.lineTo(x, py + ph + 4); ctx.stroke(); ctx.fillText(['10 V', '100 V', '1 kV', '10 kV', '100 kV', '1 MV'][k - 1], x, py + ph + 15); }
    ctx.textAlign = 'right';
    for (const [l, t] of [[1e-10, '100 pm'], [1e-11, '10 pm'], [1e-12, '1 pm']]) { const y = ly(l); ctx.beginPath(); ctx.moveTo(px - 4, y); ctx.lineTo(px, y); ctx.stroke(); ctx.fillText(t, px - 6, y + 4); }
    const cv = out.lambda_curve, n = cv.length / 3;
    const line = (k, col, dash) => { ctx.strokeStyle = col; ctx.setLineDash(dash); ctx.lineWidth = 2; ctx.beginPath(); for (let i = 0; i < n; i++) { const X = lx(cv[3 * i]), Y = ly(cv[3 * i + k]); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); } ctx.stroke(); ctx.setLineDash([]); };
    line(2, '#8b8079', [5, 4]); line(1, '#7a1f2b', []);
    const dot = (V, l, t) => { ctx.fillStyle = '#1c1518'; ctx.beginPath(); ctx.arc(lx(V), ly(l), 4, 0, 2 * Math.PI); ctx.fill(); ctx.textAlign = 'left'; ctx.fillText(t, lx(V) + 7, ly(l) - 6); };
    dot(p.V_acc, out.lambda_e, 'column'); dot(p.V_land, out.lambda_land, 'landing');
    ctx.textAlign = 'left'; ctx.fillStyle = '#7a1f2b'; ctx.fillText('λ exact', px + 8, py + 14); ctx.fillStyle = '#8b8079'; ctx.fillText('λ without relativity (dashed)', px + 8, py + 28);
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
      aspect: '16 / 7', aspectPhone: '3 / 4',
      caption: 'Left: the gun drawn, the beam narrowing to the anode and opening again if it is slowed before the wafer. Right: the electron wavelength against voltage, exact (wine) and without relativity (grey, dashed), with the column and landing values marked.',
    },
    compute, draw,
  };
});
