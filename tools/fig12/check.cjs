// Offline checks of the stout solver: node tools/fig12/check.cjs <test> [dx] [steps per second]
//   rest      the tulip at rest for 1 s: fastest particle, surface height
//   tilt      a steady push a = 2 m/s^2 along x: the surface must tilt to slope -a/g (any glass shape)
//   cylfreq   a straight cylinder R = 4 cm, h = 10 cm, after a short push: frequency against linear theory 3.382 Hz
//   freq      the tulip after a short push: frequency and damping (no closed form; compare two grids)
//   spill     the tulip given a hard push: particles over the rim leave; mass and momentum book-keeping
// Every number printed is measured.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Fluid } = load('stout-cart.js'), G = load('guinness-glass.js');
const EXTRA = process.env.FOPT ? JSON.parse(process.env.FOPT) : {};
const test = process.argv[2] || 'rest', dx = +(process.argv[3] || 0.004), dt = 1 / +(process.argv[4] || 200);
const tulip = () => new Fluid(Object.assign({ dx, profile: G, h0: 0.125, H: G.R.length * G.dz + 0.03 }, EXTRA));
const centre = (f) => { f.columnHeights(); return f.columnHeightAt(0, 0); };
const wallDiff = (f, r) => { f.columnHeights(); return f.columnHeightAt(r, 0) - f.columnHeightAt(-r, 0); };
function freq(f, r) {
  for (let n = 0; n < Math.round(0.3 / dt); n++) f.step(dt, 0, 0);
  const T = [], P = [];
  for (let n = 0; n < Math.round(1.6 / dt); n++) { const t = n * dt; f.step(dt, t < 0.05 ? 1.5 : 0, 0); let m = 0; for (let p = 0; p < f.np; p++) m += f.pu[p]; T.push(t); P.push(m); }
  const z = []; for (let i = 1; i < P.length; i++) if (T[i] > 0.1 && P[i - 1] < 0 && P[i] >= 0) z.push(T[i - 1] + (T[i] - T[i - 1]) * (-P[i - 1]) / (P[i] - P[i - 1]));
  const pk = []; for (let i = 1; i < P.length - 1; i++) if (T[i] > 0.1 && Math.abs(P[i]) > Math.abs(P[i - 1]) && Math.abs(P[i]) >= Math.abs(P[i + 1])) pk.push(Math.abs(P[i]));
  const per = (z[z.length - 1] - z[0]) / (z.length - 1), dec = Math.log(pk[0] / pk[2]);
  return { f: 1 / per, zeta: dec / Math.sqrt(4 * Math.PI * Math.PI + dec * dec) };
}
const t0 = Date.now();
if (test === 'rest') {
  const f = tulip(); f.levelSet(); const h0 = centre(f);
  for (let n = 0; n < Math.round(1 / dt); n++) f.step(dt, 0, 0);
  console.log(`rest (tulip, dx ${dx * 1000} mm, dt 1/${1 / dt} s): ${f.np} particles, ${(f.mLiquid * 1000).toFixed(1)} g; centre ${(h0 * 1000).toFixed(2)} -> ${(centre(f) * 1000).toFixed(2)} mm; fastest particle ${(f.maxSpeed() * 1000).toFixed(1)} mm/s; spilled ${f.spilled}`);
} else if (test === 'tilt' || test === 'cyltilt') {
  // quasi-static: the push rises as 1 - cos over 2 s (much longer than a swing, 0.3 s), then the centre of mass of the
  // liquid is averaged over 2.5-5.5 s (ten swings). To first order in the slope, a plane surface tilted by -a/g puts the
  // centre of mass at x = -(a/g) I / V with I = pi R(h)^4 / 4 the second moment of the surface's circle: any glass.
  const cyl = test === 'cyltilt', vc = process.argv[5] != null ? +process.argv[5] : undefined;
  const f = cyl ? new Fluid(Object.assign({ dx, profile: { dz: 0.0005, R: new Array(296).fill(0.04) }, h0: 0.10, H: 0.18, volumeCorrection: vc }, EXTRA)) : new Fluid(Object.assign({ dx, profile: G, h0: 0.125, H: G.R.length * G.dz + 0.03, volumeCorrection: vc }, EXTRA));
  const A = 2.0; let xs = 0, ns = 0;
  for (let n = 0; n < Math.round(5.5 / dt); n++) {
    const t = n * dt; f.step(dt, t < 2 ? A * 0.5 * (1 - Math.cos(Math.PI * t / 2)) : A, 0);
    if (t > 2.5) { let xb = 0; for (let p = 0; p < f.np; p++) xb += f.px[p]; xs += xb / f.np; ns++; }
  }
  const Rh = f.Rz(f.h0), V = f.volumeTo(f.h0), exact = -(A / 9.81) * Math.PI * Math.pow(Rh, 4) / 4 / V;
  console.log(`${cyl ? 'cylinder' : 'tulip'} under a steady push a = ${A} m/s^2 (dx ${dx * 1000} mm, volume correction ${f.volumeCorrection}): time-mean centre of mass ${(xs / ns * 1000).toFixed(3)} mm; exact (first order) ${(exact * 1000).toFixed(3)} mm; difference ${(100 * (xs / ns / exact - 1)).toFixed(1)} %`);
} else if (test === 'cylfreq') {
  const f = new Fluid(Object.assign({ dx, profile: { dz: 0.0005, R: new Array(296).fill(0.04) }, h0: 0.10, H: 0.18, volumeCorrection: process.argv[5] != null ? +process.argv[5] : undefined }, EXTRA));
  const r = freq(f), xi = 1.8412, th = Math.sqrt(9.81 * xi / 0.04 * Math.tanh(xi * 0.10 / 0.04)) / (2 * Math.PI);
  console.log(`cylinder R 40 mm, h 100 mm, dx ${dx * 1000} mm, dt 1/${1 / dt}: f = ${r.f.toFixed(3)} Hz (linear theory ${th.toFixed(3)} Hz, ${(100 * (r.f / th - 1)).toFixed(1)} %); damping ratio ${r.zeta.toFixed(4)}`);
} else if (test === 'freq') {
  const r = freq(tulip());
  console.log(`tulip, h 125 mm, dx ${dx * 1000} mm, dt 1/${1 / dt}: f = ${r.f.toFixed(3)} Hz; damping ratio ${r.zeta.toFixed(4)}`);
} else if (test === 'spill') {
  const f = tulip(), n0 = f.np, m0 = f.liquidMass(); let Pout = 0;
  for (let n = 0; n < Math.round(1.5 / dt); n++) { const t = n * dt; f.step(dt, t < 0.12 ? 25 : 0, 0); Pout += f.spillPx; }
  console.log(`spill (tulip, 25 m/s^2 for 0.12 s): ${f.spilled} particles left the glass (${n0} -> ${f.np}); liquid ${(m0 * 1000).toFixed(1)} -> ${(f.liquidMass() * 1000).toFixed(1)} g, spilled ${((m0 - f.liquidMass()) * 1000).toFixed(1)} g = ${(f.spilled * 2 * f.mp * 1000).toFixed(1)} g counted; momentum carried out ${Pout.toFixed(4)} kg m/s`);
}
console.log(`(${((Date.now() - t0) / 1000).toFixed(0)} s)`);
