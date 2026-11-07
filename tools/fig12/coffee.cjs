// Part C: a mug of coffee beside the pint of stout (note section 14). Prints
//   1. for each vessel: the first sloshing frequency f11 (eq. 16, with and without surface tension), the wall's damping ratio
//      (Abramson's eq., as the live models use it), the steady push that tilts the surface up to the rim, the foam's extra
//      damping (Sauret et al. 2015, scaled from their cell's wall gap w to the glass's radius R), and the walking steps' ratio
//      to f11;
//   2. both vessels carried by a walker: the glass's forward acceleration a_x = A w^2 [sin(w t) + e2 4 sin(2 w t)], w = 2 pi f_step,
//      A = 10 mm by default (Mayer & Krechetnikov: forward oscillations "on the order of 1 cm"), e2 the second harmonic's share of the
//      displacement (Han 2016 saw the harmonic; its size is our assumption: 0.3, Mayer & Krechetnikov's middle noise level),
//      from rest, through the nonlinear live model (stout-cart.js NMFluid, the same code as the page's). Printed: the steps
//      walked before the first drop leaves (f_step times the time), or "none" in T seconds, and the largest wall rise.
//   node tools/fig12/coffee.cjs [T s] [A mm]
// The mug: an upright cylinder, R = 35 mm, coffee 100 mm deep (Mayer & Krechetnikov's "typical common size"), filled so that
// a push of g tan(12.1 deg) tilts it to the rim (their middle fill level, alpha = 12.1 deg): the rim 7.5 mm above the coffee.
// The NM coefficients are those of h/R = 3.197 (the pint); the mug's 2.86 changes tanh(xi11 h/R) by 4e-5.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { NMFluid } = load('stout-cart.js'), G = load('guinness-glass.js'), NM = load('stout-nm.js');
const T = +(process.argv[2] || 20), Amm = +(process.argv[3] || 10), g = 9.81, rho = 1000, XI = 1.841184;
const tanA = Math.tan(12.1 * Math.PI / 180), Rm = 0.035, hm = 0.100, gapM = Rm * tanA;
const mug = (zs) => new NMFluid({ R: Rm, h0: hm, zRim: hm + gapM, nmCoeffs: NM, zetaScale: zs });
const pint = (zs) => new NMFluid({ dx: 0.004, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03, nmCoeffs: NM, zetaScale: zs });
const fOf = (R, h, sigma) => { const k = XI / R; return Math.sqrt(g * k * Math.tanh(k * h) * (1 + sigma * k * k / (rho * g))) / (2 * Math.PI); };
const wF = [1.6, 3.1];   // Sauret et al.: w / tau_f at the plateau, cm/s (exponential fit 1.6 +- 0.3; their eq. 14 fit 3.1)
console.log('1. The two vessels');
const zsFoam = {};
for (const [name, mk, sig] of [['mug of coffee', mug, 0.072], ['pint of stout', pint, 0.072]]) {
  const f = mk(1), R = f.Rs, f11 = f.w[0] / 2 / Math.PI, gap = f.zRim - f.h;
  const z = f.zeta[0], foam = wF.map((c) => (c / 100 / R) / f.w[0]);
  zsFoam[name] = foam.map((zf) => (z + zf) / z);
  console.log(`  ${name}: R(h) ${(R * 1000).toFixed(1)} mm, depth ${(f.h * 1000).toFixed(1)} mm, rim ${(gap * 1000).toFixed(1)} mm above;` +
    ` f11 ${f11.toFixed(3)} Hz (deep cylinder of R(h), eq. 16: ${fOf(R, f.h, 0).toFixed(3)} Hz, with surface tension ${sig} N/m ${fOf(R, f.h, sig).toFixed(3)} Hz);` +
    ` wall damping zeta ${z.toFixed(4)} (decay time ${(1 / (z * f.w[0])).toFixed(1)} s); push to the rim g gap/R ${(g * gap / R).toFixed(2)} m/s^2;` +
    ` foam would add zeta ${foam.map((v) => v.toFixed(3)).join(' to ')}; walking 1-2.5 Hz is ${(1 / f11).toFixed(2)}-${(2.5 / f11).toFixed(2)} f11, its 2nd harmonic ${(2 / f11).toFixed(2)}-${(5 / f11).toFixed(2)} f11`);
}
console.log(`  Mayer & Krechetnikov's fill levels alpha 8.1-16.5 deg tilt to the rim at g tan(alpha) = ${(g * Math.tan(8.1 * Math.PI / 180)).toFixed(2)}-${(g * Math.tan(16.5 * Math.PI / 180)).toFixed(2)} m/s^2`);
console.log(`2. Carried by a walker, A = ${Amm} mm, ${T} s from rest: steps before the first drop (largest wall rise, mm; spilled, ml)`);
const steps = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5];
const cases = [['mug of coffee', mug, 1, 'mug'], ['pint of stout', pint, 1, 'pint, no head'],
  ['pint of stout', pint, zsFoam['pint of stout'][0], 'pint, head (zeta x ' + zsFoam['pint of stout'][0].toFixed(1) + ')']];
for (const e2 of [0, 0.3]) for (const [, mk, zs, label] of cases) {
  const row = [];
  for (const fs_ of steps) {
    const f = mk(zs), w = 2 * Math.PI * fs_, dt = 1 / 400, A = Amm / 1000;
    let tSpill = null, lift = 0;
    for (let n = 0; n * dt < T; n++) {
      const t = n * dt, ax = A * w * w * (Math.sin(w * t) + e2 * 4 * Math.sin(2 * w * t));
      f.step(dt, ax, 0);
      lift = Math.max(lift, f.wallLift());
      if (tSpill === null && f.spillV > 1e-9) tSpill = t;
    }
    row.push(`${fs_} Hz: ${tSpill === null ? 'none' : (tSpill * fs_).toFixed(1)} (${(lift * 1000).toFixed(1)}${f.spillV > 0 ? '; ' + (f.spillV * 1e6).toFixed(0) : ''})`);
  }
  console.log(`  e2 ${e2}, ${label.padEnd(26)} ${row.join('; ')}`);
}
