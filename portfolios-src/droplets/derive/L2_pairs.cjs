'use strict';
const { efficiency } = require('./L2_traj.cjs');
const B = require('./beard.cjs');
function pair(R, r, A, Z) {
  const U = B.vt(R, A), vr = B.vt(r, A), gs = B.g * (1 - A.rho / 1000);
  const tau = vr / gs, St = tau * U / R, S = vr / U, p = r / R, Re = 2 * R * A.rho * U / A.mu;
  const es = efficiency('stokes', St, S, p, Z || 200), ep = efficiency('potential', St, S, p, 30);
  const E = (es.E + ep.E * Re / 60) / (1 + Re / 60);
  return { R, r, St, S, Re, ES: es.E, EP: ep.E, E };
}
const A = B.air(283.15, 85000);
console.log(' R(um) r(um)   St     S     Re_c   E_Stokes E_pot   E_blend');
for (const [R, r] of [[20, 8], [30, 8], [40, 8], [40, 10], [50, 8], [60, 8], [100, 8], [100, 10], [200, 8], [50, 45], [60, 50], [60, 55]]) {
  const t0 = Date.now(); const q = pair(R * 1e-6, r * 1e-6, A);
  console.log(`${String(R).padStart(5)} ${String(r).padStart(5)}  ${q.St.toFixed(3).padStart(6)} ${q.S.toFixed(3)} ${q.Re.toFixed(2).padStart(6)}  ${q.ES.toFixed(4)}  ${q.EP.toFixed(4)}  ${q.E.toFixed(4)}   (${Date.now() - t0} ms)`);
}
// convergence in the start distance for the Stokes field
for (const Z of [50, 100, 200, 400]) { const q = pair(40e-6, 8e-6, A, Z); console.log(`Z=${Z}: E_Stokes(40,8)=${q.ES.toFixed(5)}`); }
// Langmuir's air (785 mb, +2 C) for comparison with his Table 4 (40 um collector, 8 um droplet: 0.394)
const L = B.air(275.15, 78500); const q = pair(40e-6, 8e-6, L); console.log(`Langmuir air: E_blend(40,8)=${q.E.toFixed(3)} (his Table 4: 0.394); E_Stokes ${q.ES.toFixed(3)}, E_pot ${q.EP.toFixed(3)}`);
