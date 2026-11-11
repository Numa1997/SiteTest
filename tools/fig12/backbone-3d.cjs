// The 3D solver's free swing at any fill height: how its frequency falls as the swing grows (the backbone curve).
// node tools/fig12/backbone-3d.cjs <fill mm> <A m/s^2> [T s] [dx m]      OUT=file.json saves the lean every 5 ms
// The glass at rest gets a_x = A sin(pi t/0.3) for t < 0.3 s, then swings freely. MODE=tilt instead ramps a_x up to A over
// 0.6 s (half cosine), holds it to t = 1 s and drops it: the surface, tilted by A, then swings freely about level with a lean
// set by A (about 2 R(h) A/g), and the fit runs over 1.2 <= t <= 2.7 s. Printed: the free swing's lean amplitude and
// frequency from a least-squares fit of a damped cosine over the first 1.5 s after t = 0.5 s (later the half glass's slow beat
// sets in, see note §12), and the spill. Lean = front minus back wall height at r = R(h), as the page reads it.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Fluid } = load('stout-cart.js'), G = load('guinness-glass.js');
const TILT = process.env.MODE === 'tilt';
const h0 = +(process.argv[2] || 125) / 1000, A = +(process.argv[3] || 2), T = +(process.argv[4] || (TILT ? 2.7 : 2.2)), dx = +(process.argv[5] || 0.004), dt = 1 / 200;
const force = (t) => TILT ? (t < 0.6 ? A * 0.5 * (1 - Math.cos(Math.PI * t / 0.6)) : t < 1.0 ? A : 0) : (t < 0.3 ? A * Math.sin(Math.PI * t / 0.3) : 0);
const T0 = TILT ? 1.2 : 0.5, T1 = TILT ? 2.7 : 2.0;
const f = new Fluid({ dx, profile: G, h0, H: (G.R.length - 1) * G.dz + 0.03 }), Rs = f.Rz(Math.min(h0, f.zRim)), ys = [];
for (let n = 0; n * dt < T - 1e-9; n++) {
  const t = n * dt; f.step(dt, force(t + 0.5 * dt), 0); f.columnHeights();
  ys.push([+(t + dt).toFixed(3), (f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0)) * 1000]);
}
// fit y = a cos(w t) + b sin(w t) + c over 0.5 <= t <= 2.0: scan w, linear least squares for (a, b, c) at each
const sel = ys.filter(([t]) => t >= T0 && t <= T1);
let best = null;
for (let fr = 2.5; fr <= 4.5; fr += 0.0005) {
  const w = 2 * Math.PI * fr; let S = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], r = [0, 0, 0];
  for (const [t, y] of sel) { const v = [Math.cos(w * t), Math.sin(w * t), 1]; for (let i = 0; i < 3; i++) { r[i] += v[i] * y; for (let j = 0; j < 3; j++) S[i][j] += v[i] * v[j]; } }
  const det = (M) => M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0]) + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]);
  const D = det(S), sol = [0, 1, 2].map((k) => det(S.map((row, i) => row.map((v, j) => (j === k ? r[i] : v)))) / D);
  let e = 0; for (const [t, y] of sel) { const w_ = w * t; const d = sol[0] * Math.cos(w_) + sol[1] * Math.sin(w_) + sol[2] - y; e += d * d; }
  if (!best || e < best.e) best = { e, fr, amp: Math.hypot(sol[0], sol[1]) };
}
console.log(`${TILT ? 'tilt-release ' : ''}3D fill ${h0 * 1000} mm (R ${(Rs * 1000).toFixed(2)} mm), A ${A} m/s^2, dx ${dx * 1000} mm: free swing lean ${best.amp.toFixed(1)} mm at ${best.fr.toFixed(4)} Hz (rms misfit ${Math.sqrt(best.e / sel.length).toFixed(2)} mm); spill ${((f.spilled || 0) * 2 * f.mp * 1000).toFixed(1)} g`);
if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify({ h0, A, dx, mode: TILT ? 'tilt' : 'pulse', fit: best, series: ys }));
