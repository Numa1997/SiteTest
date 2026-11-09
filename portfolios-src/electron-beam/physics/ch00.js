/* The Electron Beam, from Tip to Measurement · physics/ch00.js
   Chapter 0, the goal: why a beam of electrons and not light. Worked example of the module pattern (physics/core.js).

   Model. Light of wavelength lambda_opt through an objective of numerical aperture NA resolves at best a period (pitch)
     d_opt = lambda_opt / (2 NA)                                  (Abbe; Born & Wolf, Principles of Optics, 7th ed., section 8.6)
   An electron accelerated from rest through a voltage V has kinetic energy eV, Lorentz factor gamma = 1 + eV/(m c^2) and
   momentum p = sqrt(2 m e V (1 + eV/(2 m c^2))) (from E^2 = (pc)^2 + (mc^2)^2 with E = mc^2 + eV), so its de Broglie wavelength is
     lambda_e = h / sqrt(2 m e V (1 + eV/(2 m c^2)))
   Chapter 3 derives the second formula in full; here it only sets the scale. The ratios to the feature width w say which probe can
   resolve the feature at all (a ratio above 1 cannot). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./core.js'));
  else { root.EB = root.EB || {}; root.EB.ch00 = factory(root.EB.core); }
})(typeof self !== 'undefined' ? self : this, function (core) {
  'use strict';
  const { C } = core;

  function compute(p) {
    const V = p.V_acc;
    const eV = C.e * V;                                    // J, kinetic energy
    const mc2 = C.m_e * C.c * C.c;                         // J, rest energy
    const gamma = 1 + eV / mc2;
    const pmom = Math.sqrt(2 * C.m_e * eV * (1 + eV / (2 * mc2)));   // kg m/s
    const lambda_e = C.h / pmom;                           // m
    const d_opt = p.lambda_opt / (2 * p.NA);               // m
    return { lambda_e, gamma, d_opt, ratio_opt: d_opt / p.w_feat, ratio_e: lambda_e / p.w_feat };
  }

  // the canvas: four lengths on one logarithmic ruler from 1 pm to 1 µm
  function draw(ctx, w, h, p, out) {
    const lo = -12, hi = -6, padL = 18, padR = 18;
    const X = x => padL + (Math.log10(x) - lo) / (hi - lo) * (w - padL - padR);
    const y0 = Math.round(h * 0.62);
    ctx.clearRect(0, 0, w, h);
    ctx.strokeStyle = '#3a322e'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(padL, y0); ctx.lineTo(w - padR, y0); ctx.stroke();
    ctx.font = "11px 'IBM Plex Mono', monospace"; ctx.fillStyle = '#6f655f'; ctx.textAlign = 'center';
    const names = { '-12': '1 pm', '-11': '10 pm', '-10': '100 pm', '-9': '1 nm', '-8': '10 nm', '-7': '100 nm', '-6': '1 µm' };
    for (let k = lo; k <= hi; k++) {
      const x = X(Math.pow(10, k));
      ctx.beginPath(); ctx.moveTo(x, y0 - 4); ctx.lineTo(x, y0 + 4); ctx.stroke();
      if (w > 420 || k % 2 === 0) ctx.fillText(names[String(k)], x, y0 + 18);
    }
    const marks = [
      { v: out.lambda_e, t: 'electron λ', c: '#7a1f2b', up: 1 },
      { v: p.w_feat, t: 'feature w', c: '#1c1518', up: 2 },
      { v: out.d_opt, t: 'light: λ/2NA', c: '#7a4b12', up: 3 },
      { v: p.lambda_opt, t: 'light λ', c: '#8b8079', up: 1 },
    ];
    ctx.font = "12.5px 'IBM Plex Sans', sans-serif";
    for (const m of marks) {
      const x = core.clamp(X(m.v), padL, w - padR), y = y0 - 14 - 22 * m.up;
      ctx.strokeStyle = m.c; ctx.fillStyle = m.c; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(x, y0); ctx.lineTo(x, y + 4); ctx.stroke();
      ctx.beginPath(); ctx.arc(x, y0, 3.5, 0, 2 * Math.PI); ctx.fill();
      ctx.textAlign = x < w / 2 ? 'left' : 'right';
      ctx.fillText(m.t, x + (x < w / 2 ? 5 : -5), y);
    }
  }

  return {
    id: 'ch00',
    inputs: ['V_acc', 'lambda_opt', 'NA', 'w_feat'],
    outputs: ['lambda_e', 'gamma', 'd_opt', 'ratio_opt', 'ratio_e'],
    // parity with ref/ch00.py: the same formula in float64 on both sides, so agreement to a few ulp is expected
    tolerance: { rel: 1e-13, abs: 0 },
    // the inputs check_parity.py runs on both sides (missing keys take the contract's defaults)
    cases: [{}, { V_acc: 100 }, { V_acc: 3e4 }, { V_acc: 3e5, lambda_opt: 1.93e-7, NA: 1.35 }, { lambda_opt: 1.35e-8, NA: 0.33, w_feat: 3e-9 }],
    ui: {
      controls: ['V_acc', 'lambda_opt', 'NA', 'w_feat'],
      readouts: ['lambda_e', 'd_opt', 'ratio_opt', 'ratio_e'],
      aspect: '16 / 6', aspectPhone: '4 / 3',
      caption: 'Four lengths on one logarithmic ruler: the electron wavelength, the feature, the smallest period (pitch) light can resolve, λ/2NA, and the light’s wavelength. The default NA of 0.95 is a dry objective; chapter 0’s ArF example uses the immersion value 1.35.',
    },
    compute,
    draw,
  };
});
