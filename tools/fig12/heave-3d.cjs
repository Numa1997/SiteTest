// Vertical jolts on a swinging stout: the 3D solver against the live model's law w^2 -> w^2 (1 + a_z/g) (layer 4).
// node tools/fig12/heave-3d.cjs [model 3d|modes] [Az m/s^2] [t_jolt s ...]
// The stout is set swinging by a_x = 2 sin(pi t/0.3) m/s^2 for t < 0.3 s, then gets a vertical half-sine a_z = s Az sin(pi (t - t_j)/0.1)
// for 0.1 s, s = +1 and -1, and a run without it. Linear theory: on a still surface a_z does nothing; on a swinging one it
// changes the phase and, depending on the moment, the amplitude. The odd part (R(+Az) - R(-Az))/2 is the jolt's linear
// effect; it is printed against the live model run with the 3D grid's own frequency and damping (3.19 Hz, zeta 0.001).
// OUT=file.json saves every series (lean every 5 ms).
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Fluid } = load('stout-cart.js'), { TulipModes } = load('stout-modal.js'), G = load('guinness-glass.js');
const data = JSON.parse(fs.readFileSync(path.join(__dirname, '../../public/data/fig12/modes.json'), 'utf8'));
const model = process.argv[2] || '3d', Az = +(process.argv[3] || 5), tjs = (process.argv.slice(4).length ? process.argv.slice(4) : ['1.0', '1.08']).map(Number);
const dt = 1 / 200, T = 2.5;
function run(kind, sgn, tj) {
  let f;
  if (kind === '3d') f = new Fluid({ dx: 0.004, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03 });
  else { f = new TulipModes({ data, profile: G, h0: 0.125, nModes: 4 }); const s = 3.19 / (f.w[0] / 2 / Math.PI); f.w = f.w.map((w) => w * s); f.beta = f.w.map((w, n) => w * w / f.g * f.c[n]); f.zeta = f.zeta.map(() => 0.001); }
  const Rs = f.Rz(Math.min(f.h0, f.zRim)), out = [];
  for (let n = 0; n * dt < T - 1e-9; n++) {
    const t = n * dt, ax = t < 0.3 ? 2 * Math.sin(Math.PI * t / 0.3) : 0, az = sgn && t >= tj && t < tj + 0.1 ? sgn * Az * Math.sin(Math.PI * (t - tj) / 0.1) : 0;
    f.step(dt, ax, az);
    if (f.columnHeights) f.columnHeights();
    out.push(+((f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0)) * 1000).toFixed(3));
  }
  return out;
}
const res = { model, Az, runs: {} };
const base = run(model, 0, 0); res.runs.none = base;
for (const tj of tjs) {
  const p = run(model, 1, tj), m = run(model, -1, tj); res.runs['+' + tj] = p; res.runs['-' + tj] = m;
  const i0 = Math.round((tj + 0.15) / dt), odd = p.map((v, k) => (v - m[k]) / 2);
  const amp = (a) => { let s = 0; for (let k = i0; k < a.length; k++) s = Math.max(s, Math.abs(a[k])); return s; };
  console.log(`${model} jolt +-${Az} m/s^2 at ${tj} s: largest lean after it, none ${amp(base).toFixed(1)}, + ${amp(p).toFixed(1)}, - ${amp(m).toFixed(1)} mm; odd part (the jolt's linear effect) up to ${amp(odd).toFixed(1)} mm`);
}
if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify(res));
