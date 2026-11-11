// Gate 1.3a: the whole glass reproduces the half glass under a push along the road.
// node tools/fig12/whole-check.cjs [dx m] [dt s] [T s]      exit 1 on failure
// Both glasses: tulip at 125 mm, stout viscosity, wall friction, a_x ramped to 1.5 m/s^2 over 0.6 s, held to 1 s, dropped.
// Limits fixed before the run: the leans (front minus back wall height) differ by at most 10 % of the half glass's rms lean
// (rms over the run); the whole glass's sideways lean (left minus right) stays under 10 % of its lean along the road; the
// liquid's sideways momentum under 1 % of its momentum along the road (rms).
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Fluid } = load('stout-cart.js'), G = load('guinness-glass.js');
const K = JSON.parse(fs.readFileSync(path.join(__dirname, '../../public/data/fig12/wall-kernel.json'), 'utf8'));
const dx = +(process.argv[2] || 0.004), dt = +(process.argv[3] || 0.00125), T = +(process.argv[4] || 3), A = 1.5;
const force = (t) => (t < 0.6 ? A * 0.5 * (1 - Math.cos(Math.PI * t / 0.6)) : t < 1.0 ? A : 0);
function run(whole) {
  const f = new Fluid({ dx, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03, nu: 2.05e-6, wallFriction: K, whole });
  const Rs = f.Rz(0.125), out = [], t0 = Date.now(); let n = 0;
  for (let k = 0; k * dt < T - 1e-9; k++) {
    f.step(dt, force((k + 0.5) * dt), 0);
    if ((k + 1) % Math.round(0.005 / dt) === 0) {
      f.columnHeights();
      let py = 0, px = 0; for (let p = 0; p < f.np; p++) { px += f.pu[p]; py += f.pv[p]; }
      out.push([(f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0)) * 1000, whole ? (f.columnHeightAt(0, Rs) - f.columnHeightAt(0, -Rs)) * 1000 : 0, px, py]);
    }
  }
  console.log(`${whole ? 'whole' : 'half '} glass: ${f.nx}x${f.ny}x${f.nz} cells, ${f.np} particles, mass ${(1000 * f.liquidMass()).toFixed(2)} g, ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  return out;
}
const h = run(false), w = run(true);
if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify({ dx, dt, half: h, whole: w }));
const n = Math.min(h.length, w.length), rms = (a) => Math.sqrt(a.reduce((s, v) => s + v * v, 0) / a.length);
const d = rms(h.slice(0, n).map((v, i) => w[i][0] - v[0])), L = rms(h.slice(0, n).map((v) => v[0])), Ly = rms(w.map((v) => v[1])), Lw = rms(w.map((v) => v[0]));
const Py = rms(w.map((v) => v[3])), Px = rms(w.map((v) => v[2]));
const checks = [[d < 0.1 * L, `lean along the road: whole minus half ${d.toFixed(2)} mm rms against ${L.toFixed(2)} mm rms (limit 10 %: ${(100 * d / L).toFixed(1)} %)`],
  [Ly < 0.1 * Lw, `whole glass, sideways lean ${Ly.toFixed(2)} mm rms against ${Lw.toFixed(2)} mm along the road (limit 10 %)`],
  [Py < 0.01 * Px, `whole glass, sideways momentum ${(100 * Py / Px).toFixed(3)} % of that along the road (limit 1 %)`]];
console.log(`whole-glass check, dx ${dx * 1000} mm, dt ${dt * 1000} ms, ${T} s:`);
for (const [ok, msg] of checks) console.log((ok ? '  pass ' : '  FAIL ') + msg);
process.exit(checks.every((c) => c[0]) ? 0 : 1);
