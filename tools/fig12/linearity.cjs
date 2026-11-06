// Where the linear modes fail, measured from rest: node tools/fig12/linearity.cjs [model 3d|modal] [A1,A2,...] [Tp s] [T s]
// The glass is at rest at t = 0; it is given one half-sine acceleration pulse a_x(t) = A sin(pi t / Tp) for t < Tp (a hard
// forward start: speed gain 2 A Tp / pi), and nothing after. Both models get exactly this a_x(t) (no cart, no coupling).
// Printed per amplitude: the largest lean (front − back wall height at r = R(h)), lean / A (constant if the response is
// linear), the free swing's frequency after the pulse (from zero crossings of the lean, t > Tp + 0.1 s), and the spill.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Fluid, ModalFluid } = load('stout-cart.js'), G = load('guinness-glass.js');
const model = process.argv[2] || 'modal', amps = (process.argv[3] || '0.5,1,2,4,6').split(',').map(Number);
const Tp = +(process.argv[4] || 0.3), T = +(process.argv[5] || 2.0), dt = 1 / 200;
const out = [];
for (const A of amps) {
  const o = { dx: 0.004, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03 };
  const f = model === '3d' ? new Fluid(o) : new ModalFluid(o);
  const Rs = f.Rz(Math.min(f.h0, f.zRim)), t0 = Date.now();
  let lean = 0, tl = 0, prev = null, cross = [];
  const series = [];
  for (let n = 0; n * dt < T - 1e-9; n++) {
    const t = n * dt, ax = t < Tp ? A * Math.sin(Math.PI * t / Tp) : 0;
    f.step(dt, ax, 0);
    if (f.columnHeights) f.columnHeights();
    const d = f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0), tt = t + dt;
    series.push([+tt.toFixed(3), +(d * 1000).toFixed(2)]);
    if (Math.abs(d) > Math.abs(lean)) { lean = d; tl = tt; }
    if (tt > Tp + 0.1 && prev !== null && Math.sign(d) !== Math.sign(prev) && prev !== 0) cross.push(tt - dt * d / (d - prev));
    prev = d;
  }
  const fr = cross.length > 2 ? (cross.length - 1) / (2 * (cross[cross.length - 1] - cross[0])) : NaN;
  const spill = model === '3d' ? (f.spilled || 0) * 2 * f.mp * 1000 : f.spillV * 1000 * 1000;
  out.push({ A, lean_mm: +(lean * 1000).toFixed(1), t_s: +tl.toFixed(3), lean_per_A: +(Math.abs(lean) * 1000 / A).toFixed(2), f_Hz: +fr.toFixed(3), spill_g: +spill.toFixed(1), series });
  console.log(`${model} A ${A} m/s^2 (dv ${(2 * A * Tp / Math.PI).toFixed(2)} m/s): lean ${(lean * 1000).toFixed(1)} mm at ${tl.toFixed(2)} s; lean/A ${(Math.abs(lean) * 1000 / A).toFixed(2)} mm per m/s^2; free swing ${fr.toFixed(3)} Hz; spill ${spill.toFixed(1)} g (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
}
if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify({ model, Tp, T, out }));
