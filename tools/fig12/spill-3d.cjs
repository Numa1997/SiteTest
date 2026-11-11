// The 3D solver (half glass, public/scripts/stout-cart.js) pushed hard enough to spill or to break: the reference for the page's
// pour model and breaking limit. node tools/fig12/spill-3d.cjs <fill mm> <A m/s^2> [Tp s] [T s] [dx m]   OUT=file.json saves the series
// a_x = A sin(pi t/Tp) for t < Tp, nothing after. Recorded every 5 ms: the lean (front minus back wall height at r = R(h)), the
// highest wall point over 36 angles of the half glass (mirrored), and the stout spilled so far (g, both halves).
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Fluid } = load('stout-cart.js'), G = load('guinness-glass.js');
const h0 = +(process.argv[2] || 125) / 1000, A = +(process.argv[3] || 6), Tp = +(process.argv[4] || 0.3), T = +(process.argv[5] || 1.5), dx = +(process.argv[6] || 0.004), dt = 1 / 200;
const f = new Fluid({ dx, profile: G, h0, H: (G.R.length - 1) * G.dz + 0.03 }), Rs = f.Rz(Math.min(h0, f.zRim)), rows = [], t0 = Date.now();
for (let n = 0; n * dt < T - 1e-9; n++) {
  const t = n * dt; f.step(dt, t < Tp ? A * Math.sin(Math.PI * (t + 0.5 * dt) / Tp) : 0, 0); f.columnHeights();
  let top = -1; for (let k = 0; k <= 18; k++) { const th = Math.PI * k / 18; top = Math.max(top, f.columnHeightAt(Rs * Math.cos(th), Rs * Math.sin(th))); }
  rows.push([+(t + dt).toFixed(3), +((f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0)) * 1000).toFixed(2), +((top - h0) * 1000).toFixed(2), +((f.spilled || 0) * 2 * f.mp * 1000).toFixed(2)]);
}
const mx = Math.max(...rows.map((r) => Math.abs(r[1])));
console.log(`3D fill ${h0 * 1000} mm, A ${A} m/s^2, Tp ${Tp} s, dx ${dx * 1000} mm: largest lean ${mx.toFixed(1)} mm, spilled ${rows[rows.length - 1][3]} g (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify({ h0, A, Tp, T, dx, cols: ['t s', 'lean mm', 'highest wall above rest mm', 'spilled g'], rows }));
