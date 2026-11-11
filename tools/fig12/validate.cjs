// Stage E of the pipeline: the page's model against the full 3D solver on random roads, regime by regime.
// node tools/fig12/validate.cjs <regime> <first seed> <count> [out.json]
//   regimes: gentle (bumps 2-8 mm), violent (bumps 15-25 mm, open loop), vertical (ripples under the wheel), spilling (fill
//   135-140 mm, bumps 15-25 mm, open loop), fills (fill 80-140 mm, bumps 5-15 mm)
// Each case: a seeded random road (Road kind 'drawn'), set speed 0.8-1.2 m/s, the cart from x = 0.5 m, 3 s. The 3D solver (half
// glass, 3 mm grid by default, DX=0.004 for 4 mm; World.advance at 5 ms) against the page's model (TulipNM) as the 3D solver's twin:
// natural frequencies times the grid's measured ratio to the finite elements (3 mm 0.958: 0.957-0.961 at 75-140 mm; 4 mm 0.943:
// 0.940-0.947; notes/fig12/runs/3d/backbone-*), friction off and the grid's own damping ratio (3 mm 0.002, 4 mm 0.004) instead (the
// 3D solver has no wall layer, skin or foam). The 3 mm grid because the 4 mm grid fails the exact steady tilt by up to 46 % on the
// flared wall (tools/fig12/tilt-exact.cjs; 3 mm within 5-6 % at 75-125 mm, 13-23 % at 140 mm): this tests the
// model's form (modes, nonlinearity, heave, coupling, pour), not its physical frequency and friction, which are tested against
// the finite elements and the literature (modal-check.cjs, modes_fem.py check).
// Per case: the lean (front minus back wall height at r = R(h)) every 5 ms from both, its rms difference over the rms of the 3D
// lean (e_lean), the largest lean of each, the cart's speed (rms difference, mm/s), the spilled mass of each.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { World, Rng } = load('stout-cart.js'), { TulipNM } = load('stout-modal.js'), G = load('guinness-glass.js');
const rd = (f) => JSON.parse(fs.readFileSync(path.join(__dirname, '../../public/data/fig12', f), 'utf8'));
const data = rd('modes.json'), nmData = rd('nm.json');
const [regime, s0, cnt, outFile] = [process.argv[2] || 'gentle', +(process.argv[3] || 1), +(process.argv[4] || 1), process.argv[5]];
//   e_env: the envelope's rms difference over the 3D envelope's rms (see below); peak_ratio: model's largest lean over the 3D's
const T = 3.0, H = (G.R.length - 1) * G.dz + 0.03, DX = +(process.env.DX || 0.003), FS = DX <= 0.0031 ? 0.958 : 0.943, ZG = DX <= 0.0031 ? 0.002 : 0.004;
function makeCase(seed) {
  const r = new Rng(1000 * seed + { gentle: 1, violent: 2, vertical: 3, spilling: 4, fills: 5 }[regime]), u = () => r.u(), P = [[0, 0]];
  let fill = 0.125, ctrl = u() < 0.5 ? 'off' : 'speed', v0 = 0.8 + 0.4 * u();
  const bump = (x, h, L) => { for (let k = 0; k <= 8; k++) P.push([x + L * k / 8, h * 0.5 * (1 - Math.cos(2 * Math.PI * k / 8))]); };
  if (regime === 'vertical') { const lam = 0.2 + 0.2 * u(), hh = 0.005 + 0.01 * u(); for (let x = 1; x < 3; x += lam / 8) P.push([x, hh * 0.5 * (1 - Math.cos(2 * Math.PI * (x - 1) / lam))]); P.push([3.2, 0]); }
  else {
    const [hl, hhh] = { gentle: [0.002, 0.008], violent: [0.015, 0.025], spilling: [0.015, 0.025], fills: [0.005, 0.015] }[regime];
    if (regime === 'violent' || regime === 'spilling') ctrl = 'off';
    if (regime === 'spilling') fill = 0.135 + 0.005 * u();
    if (regime === 'fills') fill = 0.080 + 0.060 * u();
    let x = 0.8 + 0.3 * u(); for (let k = 0; k < 3; k++) { const L = 0.2 + 0.3 * u(); bump(x, hl + (hhh - hl) * u(), L); x += L + 0.3 + 0.6 * u(); }
  }
  P.push([20, 0]); P.sort((a, b) => a[0] - b[0]);
  const pts = P.filter((p, i) => i === 0 || p[0] > P[i - 1][0] + 1e-6);
  return { seed, regime, fill: +fill.toFixed(4), ctrl, v0: +v0.toFixed(3), points: pts };
}
function run(c, twin) {
  const road = { kind: 'drawn', points: c.points, Rw: 0.04, xmin: -1, xmax: 14 }, cart = { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: c.v0, ctrl: c.ctrl, susp: false };
  const w = twin ? new World({ fluidInstance: new TulipNM({ data, nmData, profile: G, h0: c.fill, nModes: 3, friction: false, zetaExtra: ZG, freqScale: FS }), road, cart, dtMax: 0.001 })
    : new World({ fluid: { dx: DX, profile: G, h0: c.fill, H }, road, cart, dtMax: 1 / 200 });
  const f = w.fluid, Rs = f.Rz(Math.min(c.fill, f.zRim)), lean = [], vx = [];
  while (w.t < T - 1e-9) {
    w.advance(0.005); if (f.columnHeights && !twin) f.columnHeights();
    lean.push((f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0)) * 1000); vx.push(w.cart.vx);
  }
  return { lean, vx, spill: (w.spilledMass || 0) * 1000 };
}
const out = [];
for (let s = s0; s < s0 + cnt; s++) {
  const c = makeCase(s), t0 = Date.now(), a = run(c, false), b = run(c, true), n = Math.min(a.lean.length, b.lean.length);
  let d2 = 0, a2 = 0, v2 = 0, la = 0, lb = 0;
  for (let k = 0; k < n; k++) { d2 += (b.lean[k] - a.lean[k]) ** 2; a2 += a.lean[k] ** 2; v2 += (b.vx[k] - a.vx[k]) ** 2; la = Math.max(la, Math.abs(a.lean[k])); lb = Math.max(lb, Math.abs(b.lean[k])); }
  // the swing's envelope: the largest |lean| in each 0.3 s window (a swing of 3.2 Hz has one crest per window), compared window by
  // window (insensitive to a phase that drifts as a small frequency difference accumulates)
  const env = (L) => { const o = []; for (let k = 0; k + 60 <= n; k += 60) { let m = 0; for (let j = k; j < k + 60; j++) m = Math.max(m, Math.abs(L[j])); o.push(m); } return o; };
  const ea = env(a.lean), eb = env(b.lean); let de = 0, ae = 0; for (let k = 0; k < ea.length; k++) { de += (eb[k] - ea[k]) ** 2; ae += ea[k] ** 2; }
  const r = { ...c, points: undefined, dx: DX, e_env: +Math.sqrt(de / Math.max(ae, 1e-12)).toFixed(3), peak_ratio: +(lb / Math.max(la, 1e-9)).toFixed(3), e_lean: +(Math.sqrt(d2 / Math.max(a2, 1e-12))).toFixed(3), rms_lean_3d: +Math.sqrt(a2 / n).toFixed(2), lean_3d: +la.toFixed(1), lean_model: +lb.toFixed(1),
    dv_rms_mm_s: +(1000 * Math.sqrt(v2 / n)).toFixed(2), spill_3d: +a.spill.toFixed(1), spill_model: +b.spill.toFixed(1), seconds: (Date.now() - t0) / 1000, series: { lean_3d: a.lean.map((v) => +v.toFixed(2)), lean_model: b.lean.map((v) => +v.toFixed(2)) } };
  out.push(r);
  console.log(`${regime} #${s}: fill ${(c.fill * 1000).toFixed(1)} mm, ${c.ctrl}, ${c.v0} m/s: lean 3D ${r.lean_3d} / model ${r.lean_model} mm, envelope ${(r.e_env * 100).toFixed(0)} % apart, point by point ${(r.e_lean * 100).toFixed(0)} % of the 3D's rms ${r.rms_lean_3d} mm; speed ${r.dv_rms_mm_s} mm/s rms apart; spilled ${r.spill_3d} / ${r.spill_model} g (${r.seconds.toFixed(0)} s)`);
}
if (outFile) fs.writeFileSync(outFile, JSON.stringify(out));
