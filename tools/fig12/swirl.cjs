// Does the nonlinear live model swirl? The glass shaken along the road, a_x = A sin(2 pi f t), for T seconds, from rest
// (with the 0.4 um seed of the side mode r1). Printed every second: the swing along the road and across it at the wall
// (largest |q1| and |s1| in that second, mm). Planar waves keep s1 at the seed; a swirl grows s1 to the size of q1.
//   node tools/fig12/swirl.cjs [A m/s^2] [f/f11 ...] [T s]
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { NMFluid } = load('stout-cart.js'), G = load('guinness-glass.js'), NM = load('stout-nm.js');
const A = +(process.argv[2] || 0.5), ratios = (process.argv[3] || '0.95,1.0,1.03,1.06').split(',').map(Number), T = +(process.argv[4] || 20);
for (const rf of ratios) {
  const f = new NMFluid({ dx: 0.004, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03, nmCoeffs: NM });
  const f11 = f.w[0] / 2 / Math.PI, fr = rf * f11, dt = 1 / 200, row = [];
  let mq = 0, ms = 0;
  for (let n = 0; n * dt < T; n++) {
    f.step(dt, A * Math.sin(2 * Math.PI * fr * n * dt), 0);
    mq = Math.max(mq, Math.abs(f.q[0])); ms = Math.max(ms, Math.abs(f.s1));
    if ((n + 1) % 200 === 0) { row.push(`${(mq * 1000).toFixed(1)}/${(ms * 1000).toFixed(1)}`); mq = 0; ms = 0; }
  }
  console.log(`A ${A} m/s^2, f/f11 ${rf} (${fr.toFixed(3)} Hz): per second, largest |q1| / |s1| in mm: ${row.join(' ')}; spilled ${(f.spillV * 1e6).toFixed(1)} ml`);
}
