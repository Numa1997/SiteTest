// A small parameter study of Fig. 12, run in Node through World.advance with the page's own options (beer-slosh.html, build()):
//   node tools/fig12/study.cjs <bump mm> <speed|off> <susp 0|1> [dx] [seconds]
// The cart starts at x = 0.5 m at the set speed 1 m/s, crosses one cosine bump (centre x = 1 m, 25 cm long) and runs on; the
// next bump (x = 3 m) is not reached in the default 2.3 s. Printed, all measured over the run:
//   dw     the largest |front − back wall| height of the stout, as the page reads it (column heights at r = R(h), θ = 0 and π)
//   a_x    the largest |horizontal acceleration of the glass| (mean over each fluid step, World.lastAx)
//   a_z    the largest |vertical acceleration of the glass|, gravity excluded (World.lastAz): the heave
//   spill  the stout that left over the rim, g
//   N      the smallest tyre load at the end of a fluid step (0: the wheel was off the road)
//   |A(f)| the Fourier amplitude |∫ a_x(t) e^{−2πift} dt| of the glass's horizontal acceleration at the stout's swing frequency
//          f = 3.214 Hz (the tulip's free swing on the 4 mm grid; 3.263 Hz on 3 mm): what drives the swing (see the note, §3)
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { World } = load('stout-cart.js'), G = load('guinness-glass.js');
const bump = +(process.argv[2] || 10) / 1000, ctrl = process.argv[3] || 'speed', susp = process.argv[4] === '1';
const dx = +(process.argv[5] || 0.004), T = +(process.argv[6] || 2.3), fS = dx <= 0.0031 ? 3.263 : 3.214;
const bumps = []; for (let n = 0; n < 60; n++) bumps.push({ x: 1.0 + 2 * n, h: bump, L: 0.25 });
const w = new World({
  fluid: { dx, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03 },
  road: { bumps, Rw: 0.04, xmin: -1, xmax: 125 },
  cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: 1, ctrl, susp },
  dtMax: 1 / 200
});
const f = w.fluid, Rs = f.Rz(Math.min(f.h0, f.zRim));
let dw = 0, tdw = 0, ax = 0, az = 0, re = 0, im = 0, vmin = 9, vmax = 0, Nmin = 1e9;
const t0 = Date.now(), series = [];
while (w.t < T - 1e-9) {
  w.advance(1 / 200);
  f.columnHeights();
  const d = f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0);
  if (Math.abs(d) > Math.abs(dw)) { dw = d; tdw = w.t; }
  ax = Math.max(ax, Math.abs(w.lastAx)); az = Math.max(az, Math.abs(w.lastAz));
  vmin = Math.min(vmin, w.cart.vx); Nmin = Math.min(Nmin, w.cart.N); vmax = Math.max(vmax, w.cart.vx);
  const ph = 2 * Math.PI * fS * w.t; re += w.lastAx * Math.cos(ph) / 200; im -= w.lastAx * Math.sin(ph) / 200;
  series.push([+w.t.toFixed(4), +w.lastAx.toFixed(4), +w.lastAz.toFixed(4), +(d * 1000).toFixed(3)]);
}
const tag = `bump ${(bump * 1000).toFixed(0)} mm, ${ctrl === 'speed' ? 'speed control' : 'open loop'}, suspension ${susp ? 'skyhook' : 'passive'}, dx ${dx * 1000} mm`;
console.log(`${tag}: dw ${(Math.abs(dw) * 1000).toFixed(1)} mm (t ${tdw.toFixed(2)} s); a_x ${ax.toFixed(2)} m/s^2; a_z ${az.toFixed(2)} m/s^2; spill ${((w.spilledMass || 0) * 1000).toFixed(1)} g; |A(${fS} Hz)| ${Math.hypot(re, im).toFixed(4)} m/s; speed ${vmin.toFixed(3)}-${vmax.toFixed(3)} m/s; smallest tyre load ${Nmin.toFixed(2)} N (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
if (process.env.SERIES) fs.writeFileSync(process.env.SERIES, JSON.stringify({ tag, cols: ['t s', 'a_x m/s^2', 'a_z m/s^2', 'dw mm'], rows: series }));
