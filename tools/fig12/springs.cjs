// Part B: what the controllers do to the suspension spring, and whether the joint design (motor + active suspension) holds the
// stout where the motor alone fails. node tools/fig12/springs.cjs <nm|3d> <road,...> <ctrl,...> [v0,...] [seconds]
// road: bumps10 bumps25 (one cosine bump of that height in mm), isoA..isoD, washboard, setts. ctrl: off, speed, slosh,
// slosh+sky (slosh feedback with the skyhook suspension), joint (one LQR for the motor and the suspension, the heave in its
// model: Cart.sample 'joint'). Several speeds run each case at each. The cart starts at x = 0.5 m.
// Printed per run, over the run after 1.5 s (bumps: over the whole run):
//   stroke     rms and largest |z_b - z_w - s_0|, the spring's compression about its static value (mm): what the spring does
//   u_s        rms and largest active force (N)
//   heave      rms of the glass's vertical acceleration a_z (m/s^2), and its rms in 6.5–7.2 Hz (the Faraday band)
//   lean       largest |front - back| at the probes (mm); spilled (g); largest motor current (A); tyre off the road (% of steps)
// Measured once, before Part B (scratch script of 6 November 2026, now this tool): on bumps the slosh feedback left the stroke
// unchanged; on the washboard at 0.85 m/s it doubled it.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { World } = load('stout-cart.js'), G = load('guinness-glass.js'), NM = load('stout-nm.js');
const model = process.argv[2] || 'nm', roads = (process.argv[3] || 'bumps25,washboard').split(','), ctrls = (process.argv[4] || 'off,slosh,slosh+sky,joint').split(',');
const speeds = (process.argv[5] || '1').split(',').map(Number), T = +(process.argv[6] || 6);
const out = [];
for (const rd of roads) for (const v0 of speeds) for (const cs of ctrls) {
  const ctrl = cs.split('+')[0], sky = /\+sky/.test(cs);
  let road;
  if (rd.startsWith('bumps')) { const h = +rd.slice(5) / 1000, b = []; for (let n = 0; n < 60; n++) b.push({ x: 1 + 2 * n, h, L: 0.25 }); road = { bumps: b }; }
  else road = rd.startsWith('iso') ? { kind: 'iso', cls: rd.slice(3) } : { kind: rd };
  const w = new World({ fluid: { dx: 0.004, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03, modal: model !== '3d', nm: model === 'nm', nmCoeffs: NM },
    road: Object.assign({ Rw: 0.04, xmin: -1, xmax: 125 }, road), cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0, ctrl, susp: sky }, dtMax: 1 / 200 });
  const c = w.cart, f = w.fluid, t0 = Date.now(), s0 = c.Ls - (c.Mb + c.ml) * c.g / c.k, az = [], st = [], us = [];
  const tFrom = rd.startsWith('bumps') ? 0 : 1.5;
  let lean = 0, imax = 0, air = 0, ns = 0, smax = 0, umax = 0;
  while (w.t < T - 1e-9) {
    w.advance(1 / 200);
    lean = Math.max(lean, Math.abs(c.probe.ef - c.probe.eb)); imax = Math.max(imax, Math.abs(c.i));
    ns++; if (c.N <= 0) air++;
    if (w.t > tFrom) { const s = c.zb - c.zw - s0; az.push(w.lastAz); st.push(s); us.push(c.us); smax = Math.max(smax, Math.abs(s)); umax = Math.max(umax, Math.abs(c.us)); }
  }
  const rms = (a) => Math.sqrt(a.reduce((x, v) => x + v * v, 0) / Math.max(1, a.length)), dt = 1 / 200, Tn = az.length * dt;
  let band = 0; for (let fr = 6.5; fr <= 7.2001; fr += 1 / Tn) { let re = 0, im = 0; az.forEach((v, k) => { re += v * Math.cos(2 * Math.PI * fr * k * dt); im += v * Math.sin(2 * Math.PI * fr * k * dt); }); band += 2 * (re * re + im * im) / (az.length * az.length); }
  const r = { model, road: rd, v0, ctrl: cs, stroke_rms_mm: rms(st) * 1000, stroke_max_mm: smax * 1000, us_rms: rms(us), us_max: umax, heave_rms: rms(az), heave_band: Math.sqrt(band), lean_mm: lean * 1000, spilled_g: (w.spilledMass || 0) * 1000, i_max: imax, air_pct: 100 * air / ns };
  out.push(r);
  console.log(`${model} ${rd} ${v0} m/s ${cs.padEnd(9)}: stroke rms ${r.stroke_rms_mm.toFixed(2)} max ${r.stroke_max_mm.toFixed(1)} mm; u_s rms ${r.us_rms.toFixed(1)} max ${r.us_max.toFixed(1)} N; heave rms ${r.heave_rms.toFixed(2)} m/s^2, band ${r.heave_band.toFixed(3)}; lean ${r.lean_mm.toFixed(1)} mm; spilled ${r.spilled_g.toFixed(1)} g; current max ${r.i_max.toFixed(2)} A; tyre off ${r.air_pct.toFixed(1)} % (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
}
if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify(out, null, 1));
