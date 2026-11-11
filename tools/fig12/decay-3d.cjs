// The 3D solver's free swing dying out: how much friction the stout feels.
// node tools/fig12/decay-3d.cjs <fill mm> <friction on|off> [T s] [dx m]      OUT=file.json saves the lean every 5 ms
// The glass is tilted as in backbone-3d.cjs MODE=tilt (a_x ramped to A = 1.5 m/s^2 over 0.6 s, held to 1 s, dropped), then
// swings freely. Stout viscosity nu = 2.05e-6 m^2/s (Benilov 2013) in both runs; "on" adds the wall's Stokes-layer stress
// (public/data/fig12/wall-kernel.json). Printed: the decay rate from a least-squares fit of
//   lean = e^{-s t} (a cos w t + b sin w t) + c   over 1.2 s <= t <= T
// (s and w scanned, a, b, c linear), its damping ratio zeta = s / sqrt(s^2 + w^2), and the wall power's mean.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Fluid } = load('stout-cart.js'), G = load('guinness-glass.js');
const K = JSON.parse(fs.readFileSync(path.join(__dirname, '../../public/data/fig12/wall-kernel.json'), 'utf8'));
const h0 = +process.argv[2] / 1000, on = process.argv[3] === 'on', T = +(process.argv[4] || 8), dx = +(process.argv[5] || 0.003), dt = +(process.env.DT || 0.005), A = 1.5;
if (!(h0 > 0) || !['on', 'off'].includes(process.argv[3])) throw new Error('usage: decay-3d.cjs <fill mm> <on|off> [T] [dx]');
const force = (t) => (t < 0.6 ? A * 0.5 * (1 - Math.cos(Math.PI * t / 0.6)) : t < 1.0 ? A : 0);
const f = new Fluid({ dx, profile: G, h0, H: (G.R.length - 1) * G.dz + 0.03, nu: 2.05e-6, wallFriction: on ? K : null, flip: +(process.env.FLIP || 0), densityProjection: +(process.env.DP || 0), quadratic: process.env.Q === '1', thetaMin: +(process.env.TMIN || 0.05), whole: process.env.WHOLE === '1' });   // FLIP: FLIP share; WHOLE=1: whole glass
const Rs = f.Rz(Math.min(h0, f.zRim)), ys = [], t0 = Date.now();
// the stout's energy relative to rest, whole glass (2 x the half glass): kinetic sum m v^2/2 + potential sum m g z, from the particles
// kinetic from the particles; potential of the swing from the surface: rho g (eta - mean)^2 / 2 over the columns whose centre
// lies inside 0.95 R(h) (the particles' own heights drift as they settle, by far more than the swing's energy: measured)
const energy = () => {
  let k = 0; for (let q = 0; q < f.np; q++) k += f.pu[q] ** 2 + f.pv[q] ** 2 + f.pw[q] ** 2;
  const H = f.colH, cells = []; let m = 0;
  for (let j = 0; j < f.ny; j++) for (let i = 0; i < f.nx; i++) { const x = f.x0 + (i + 0.5) * dx, y = (j + 0.5) * dx; if (x * x + y * y < (0.95 * Rs) ** 2) { cells.push(H[i + f.nx * j]); m += H[i + f.nx * j]; } }
  m /= cells.length; let p = 0; for (const h of cells) p += (h - m) ** 2;
  return [2 * f.mp * 0.5 * k, 2 * 0.5 * f.rho * f.g * p * dx * dx];
};
const P0 = 0, Es = [];
let pw = 0, npw = 0;
for (let n = 0; n * dt < T - 1e-9; n++) {
  const t = n * dt; f.step(dt, force(t + 0.5 * dt), 0); f.columnHeights();
  ys.push([+(t + dt).toFixed(3), (f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0)) * 1000]);
  const [ke, pe] = energy(); Es.push([+(t + dt).toFixed(3), ke, pe - P0, on ? f.wallPower : 0]);
  if (on && t > 1.2) { pw += f.wallPower; npw++; }
}
// energy budget after release: mean energy, its trend (least-squares slope), mean wall power, and zeta's from each
{
  const S = Es.filter(([t]) => t >= 1.2), n = S.length, E = S.map(([, k, p]) => k + p), tt = S.map(([t]) => t);
  const mt = tt.reduce((a, b) => a + b) / n, mE = E.reduce((a, b) => a + b) / n;
  let sxy = 0, sxx = 0; for (let i = 0; i < n; i++) { sxy += (tt[i] - mt) * (E[i] - mE); sxx += (tt[i] - mt) ** 2; }
  const slope = sxy / sxx, mP = S.reduce((a, s) => a + s[3], 0) / n, w = 2 * Math.PI * 3.41;
  console.log(`energy after release: mean ${(1e6 * mE).toFixed(2)} uJ, trend ${(1e6 * slope).toFixed(3)} uW (zeta of the trend ${(-slope / (2 * w * mE)).toFixed(5)}), wall power ${(1e6 * mP).toFixed(3)} uW (zeta of the wall ${(mP / (2 * w * mE)).toFixed(5)}, at omega = 2 pi 3.41 Hz)`);
}
const sel = ys.filter(([t]) => t >= 1.2);
function lsq(s, w) {
  let S = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], r = [0, 0, 0];
  for (const [t, y] of sel) { const e = Math.exp(-s * (t - 1.2)), v = [e * Math.cos(w * t), e * Math.sin(w * t), 1]; for (let i = 0; i < 3; i++) { r[i] += v[i] * y; for (let j = 0; j < 3; j++) S[i][j] += v[i] * v[j]; } }
  const det = (M) => M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0]) + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]);
  const D = det(S), x = [0, 1, 2].map((k) => det(S.map((row, i) => row.map((v, j) => (j === k ? r[i] : v)))) / D);
  let e = 0; for (const [t, y] of sel) { const g = Math.exp(-s * (t - 1.2)); const d = g * (x[0] * Math.cos(w * t) + x[1] * Math.sin(w * t)) + x[2] - y; e += d * d; }
  return { e, amp: Math.hypot(x[0], x[1]) };
}
let best = null;
for (let fr = 3.0; fr <= 3.8; fr += 0.002) for (let s = 0; s <= 0.6; s += 0.004) { const r = lsq(s, 2 * Math.PI * fr); if (!best || r.e < best.e) best = { ...r, fr, s }; }
// refine around the best
const b0 = best;
for (let fr = b0.fr - 0.002; fr <= b0.fr + 0.002; fr += 0.0001) for (let s = Math.max(0, b0.s - 0.004); s <= b0.s + 0.004; s += 0.0002) { const r = lsq(s, 2 * Math.PI * fr); if (r.e < best.e) best = { ...r, fr, s }; }
const w = 2 * Math.PI * best.fr, zeta = best.s / Math.hypot(best.s, w);
console.log(`decay fill ${h0 * 1000} mm, dx ${dx * 1000} mm, friction ${on ? 'on' : 'off'}: ${best.fr.toFixed(4)} Hz, lean ${best.amp.toFixed(2)} mm at t = 1.2 s, decay rate ${best.s.toFixed(4)} 1/s, zeta ${zeta.toFixed(5)}, rms misfit ${Math.sqrt(best.e / sel.length).toFixed(3)} mm${on ? `, mean wall power ${(1e6 * pw / npw).toFixed(3)} uW` : ''} (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify({ h0, dx, on, fit: { f: best.fr, s: best.s, zeta, amp: best.amp }, series: ys, energy: Es }));
