// Empty channel 2.2 × 0.41 m, parabolic inflow U_max 0.3, no-slip walls, ν 1e-3: exact Poiseuille, dp/dx = -8 μ U_max / H² = -0.014277 Pa/m.
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const ny = +(process.env.NY || 40), dx = 0.41 / ny, nx = Math.ceil(2.2 / dx / 8) * 8;
const w = new T.World({ dx, nx, ny, x0: 0, y0: 0, rho: 1, mu: 1e-3, machine: { m0: 1, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, h: 0.002, nsub: 5 });
w.inflow = (y) => 4 * 0.3 * y * (0.41 - y) / (0.41 * 0.41); w.noslip = true; w.frozen = true; w.noRods = true; w.b = 1; w.cartGone = true;
for (let j = 0; j < ny; j++) for (let i = 0; i <= nx; i++) w.u[j * (nx + 1) + i] = w.inflow(w.yu(j));
while (w.t < 6 - 1e-9) w.step(null);
const pc = (X) => { const i = Math.round((X - w.x0) / dx - 0.5), j = ny / 2; return 0.5 * (w.pF[j * nx + i] + w.pF[(j - 1) * nx + i]); };
const g = (pc(1.5) - pc(0.5)) / 1.0;
let err = 0; const i = Math.round(1.1 / dx); for (let j = 0; j < ny; j++) err = Math.max(err, Math.abs(w.u[j * (nx + 1) + i] - w.inflow(w.yu(j))));
console.log(JSON.stringify({ ny, dpdx: +g.toFixed(6), exact: -0.014277, err_pct: +(100 * (g / -0.014277 - 1)).toFixed(2), max_u_err_mid: +err.toExponential(2) }));
