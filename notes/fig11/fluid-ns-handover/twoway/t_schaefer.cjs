// Benchmark: Schäfer & Turek 1996, 2D-1 (Re 20): channel 2.2 × 0.41 m, no-slip walls, parabolic inflow U_max 0.3 m/s, cylinder D 0.1 at (0.2, 0.2),
// ν = 1e-3, ρ = 1. Reference band c_D 5.57–5.59, c_L 0.0104–0.0110 (dfg_benchmark_results). c_D = 2 F_x / (ρ Ū² D), Ū = 0.2.
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const ny = +(process.env.NY || 40), dx = 0.41 / ny, nx = Math.ceil(2.2 / dx / 8) * 8;
const w = new T.World({ dx, nx, ny, x0: 0, y0: 0, rho: 1, mu: 1e-3, machine: { m0: 1, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, h: +(process.env.H || 0.002), nsub: 5 });
w.U = 0; w.inflow = (y) => 4 * 0.3 * y * (0.41 - y) / (0.41 * 0.41); w.noslip = true; w.frozen = true; w.noRods = true; w.b = 1;
w.geom = function () { this.measureCircle(0.2, 0.2, 0.05); };
for (let c = 0; c < w.u.length; c++) w.u[c] = 0;
let F = []; while (w.t < 12 - 1e-9) { w.step(null); F.push(w.Q0); }
const Fx = F.slice(-100).reduce((a, b) => a + b, 0) / 100;
console.log(JSON.stringify({ cells_per_D: +(0.1 / dx).toFixed(1), grid: [nx, ny], cD: +(2 * Fx / (0.04 * 0.1)).toFixed(3), band: '5.57-5.59', err_pct_vs_5_58: +(100 * (2 * Fx / 0.004 / 5.58 - 1)).toFixed(1) }));
{ const pAt = (X, Y) => { const i = Math.floor((X - w.x0) / w.dx - 0.5), j = Math.floor((Y - w.y0) / w.dx - 0.5), a = (X - w.x0) / w.dx - 0.5 - i, b = (Y - w.y0) / w.dx - 0.5 - j, P = w.pF, n = w.nx;
    return (1 - a) * (1 - b) * P[j * n + i] + a * (1 - b) * P[j * n + i + 1] + (1 - a) * b * P[(j + 1) * n + i] + a * b * P[(j + 1) * n + i + 1]; };
  const dp = pAt(0.15, 0.2) - pAt(0.25, 0.2); const pr = w.cartForce(w.pF); 
  console.log(JSON.stringify({ dp: +dp.toFixed(4), dp_ref: '0.1172-0.1176', cD_pressure_part: +(2 * pr / 0.004).toFixed(3), cD_rest: +(2 * (Fx - pr) / 0.004).toFixed(3) })); }
{ // control-volume drag: F_x = -∮ (ρ u u·n + p n_x - τ_xj n_j) dS over the box [0.1, 0.3] × [0.1, 0.3] (steady flow)
  const nx = w.nx, Wu = nx + 1, d = w.dx, mu = 1e-3, U = (i, j) => w.u[j * Wu + i], V = (i, j) => w.v[j * nx + i], Pc = (i, j) => w.pF[j * nx + i];
  const iL = Math.round(0.1 / d), iR = Math.round(0.3 / d), jB = Math.round(0.1 / d), jT = Math.round(0.3 / d); let F = 0;
  for (let j = jB; j < jT; j++) { for (const [i, sg] of [[iL, -1], [iR, 1]]) { const u = U(i, j), p = 0.5 * (Pc(i - 1, j) + Pc(i, j)), dudx = (U(i + 1, j) - U(i - 1, j)) / (2 * d);
      F -= sg * (u * u + p - 2 * mu * dudx) * d; } }
  for (let i = iL; i < iR; i++) { for (const [j, sg] of [[jB, -1], [jT, 1]]) { const uc = 0.5 * (U(i, j) + U(i + 1, j)), um = 0.5 * (U(i, j - 1) + U(i + 1, j - 1)), vc = 0.5 * (V(i, j)), uu = 0.5 * (uc + um);
      const dudy = (uc - um) / d, dvdx = (V(i + 1, j) - V(i - 1, j)) / (2 * d); F -= sg * (uu * V(i, j) - mu * (dudy + dvdx)) * d; } }
  console.log(JSON.stringify({ cD_controlvolume: +(2 * F / 0.004).toFixed(3) })); }
