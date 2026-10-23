'use strict';
const T = require('./L2_traj.cjs');
const B = require('./beard.cjs');
const A = B.air(283.15, 85000);
const R = 20e-6, U = B.vt(R, A), gs = B.g * (1 - A.rho / 1000);
for (const p of [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]) {
  const r = p * R, vr = B.vt(r, A), St = vr / gs * U / R, S = vr / U;
  const F = T.flowField('stokes');
  // scan b in [0, 0.3] for hits
  const hitsAt = [];
  for (let i = 0; i <= 60; i++) { const b = i * 0.3 / 60; hitsAt.push(T.hits(F, St, S, p, b + 1e-9, 200) ? 1 : 0); }
  const e = T.efficiency('stokes', St, S, p, 200);
  console.log(`p=${p} St=${St.toFixed(3)} S=${S.toFixed(3)} E=${e.E.toExponential(3)} bc=${e.bc.toFixed(5)} hits(b=0..0.3): ${hitsAt.join('')}`);
}
