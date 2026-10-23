// L8 (Gate 1 numbers): scales of drops in a turbulent cloud, and the kernels the L8 model must reproduce or predict.
//   node derive/L8_scales.cjs
'use strict';
const P = require('../physics.cjs');
const A = P.air(283.15, 85000), g = P.G0, nu = A.nu;
const v = a => P.vBeard(a, A), tau = a => v(a) / (g * (1 - A.rho / 1000));
for (const eps of [1e-3, 1e-2, 4e-2]) {
  const eta = Math.pow(nu ** 3 / eps, 0.25), tK = Math.sqrt(nu / eps), uK = Math.pow(nu * eps, 0.25);
  console.log(`eps = ${eps} m^2/s^3: Kolmogorov length ${(eta * 1e3).toFixed(2)} mm, time ${(tK * 1e3).toFixed(1)} ms, speed ${(uK * 1e3).toFixed(1)} mm/s`);
  for (const [R, r] of [[40, 8], [60, 50], [20, 18]]) {
    const Ru = R * 1e-6, ru = r * 1e-6, a = Ru + ru, dvg = Math.abs(v(Ru) - v(ru));
    const Kg = Math.PI * a * a * dvg;                                  // geometric gravitational kernel
    const Kst = Math.sqrt(8 * Math.PI / 15) * a ** 3 / tK;            // Saffman-Turner shear kernel (zero inertia)
    console.log(`   ${R}/${r} um: separation at contact ${(a * 1e6).toFixed(0)} um = ${(a / eta).toFixed(3)} eta; gravity dv ${(dvg * 1e3).toFixed(2)} mm/s, ` +
      `shear dv ~ a/tK ${(a / tK * 1e3).toFixed(2)} mm/s; St ${(tau(Ru) / tK).toFixed(3)}/${(tau(ru) / tK).toFixed(3)}; Saffman-Turner/gravity ${(Kst / Kg).toFixed(4)}; ` +
      `Ayala factor ${(P.ayalaFactor(Ru, ru, A, eps)).toFixed(3)}`);
  }
}
