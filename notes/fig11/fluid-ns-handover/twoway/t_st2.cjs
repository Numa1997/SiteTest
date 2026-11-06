// Root-cause diagnostics on Schäfer–Turek 2D-1 (Re 20). Reference (table 3): c_D 5.57–5.59, c_L 0.0104–0.0110, La 0.0842–0.0852, Δp 0.1172–0.1176.
// Prints: c_D read on the body (and its pressure part), c_D from a control volume, the recirculation length La on y = 0.2, and Δp by extrapolation from fluid cells.
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const ny = +(process.env.NY || 40), dx = 0.41 / ny, nx = Math.ceil(2.2 / dx / 8) * 8, H = +(process.env.H || 0.002), NS = +(process.env.NS || 5), TEND = +(process.env.TEND || 12);
const w = new T.World({ dx, nx, ny, x0: 0, y0: 0, rho: 1, mu: 1e-3, machine: { m0: 1, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, h: H, nsub: NS });
w.U = 0; w.inflow = (y) => 4 * 0.3 * y * (0.41 - y) / (0.41 * 0.41); w.noslip = true; w.frozen = true; w.noRods = true; w.b = 1;
for (const k of (process.env.OPT || '').split(',').filter(Boolean)) w[k] = true;
w.geom = function () { this.measureCircle(0.2, 0.2, 0.05); };
for (let c = 0; c < w.u.length; c++) w.u[c] = 0;
const F = []; while (w.t < TEND - 1e-9) { w.step(null); F.push(w.Q0); }
const Fx = F.slice(-50).reduce((a, b) => a + b, 0) / 50;
const Wu = nx + 1, U = (i, j) => w.u[j * Wu + i], V = (i, j) => w.v[j * nx + i], P = (i, j) => w.pF[j * nx + i], mu = 1e-3, d = dx;
// control volume [0.1, 0.3] × [0.1, 0.3]
const iL = Math.round(0.1 / d), iR = Math.round(0.3 / d), jB = Math.round(0.1 / d), jT = Math.round(0.3 / d); let Fcv = 0;
for (let j = jB; j < jT; j++) for (const [i, sg] of [[iL, -1], [iR, 1]]) { const u = U(i, j), p = 0.5 * (P(i - 1, j) + P(i, j)), dudx = (U(i + 1, j) - U(i - 1, j)) / (2 * d); Fcv -= sg * (u * u + p - 2 * mu * dudx) * d; }
for (let i = iL; i < iR; i++) for (const [j, sg] of [[jB, -1], [jT, 1]]) { const uc = 0.5 * (U(i, j) + U(i + 1, j)), um = 0.5 * (U(i, j - 1) + U(i + 1, j - 1)); Fcv -= sg * (0.5 * (uc + um) * V(i, j) - mu * ((uc - um) / d + (V(i + 1, j) - V(i - 1, j)) / (2 * d))) * d; }
// La: on y = 0.2, behind x = 0.25, where the u on the centre line turns positive
let La = NaN, prev = null; for (let X = 0.25 + 1e-4; X < 0.6; X += dx / 20) { const u = w.velAt(X, 0.2)[0]; if (prev !== null && prev < 0 && u >= 0) { La = X - 0.25; break; } prev = u; }
// Δp: pressure at the cell centres on the row through y = 0.2, outside the body, extrapolated linearly to x = 0.15 and 0.25
const jr = Math.floor(0.2 / d - 0.5), fy = 0.2 / d - 0.5 - jr, pRow = (i) => (1 - fy) * P(i, jr) + fy * P(i, jr + 1), xc = (i) => (i + 0.5) * d;
let iF = Math.floor(0.15 / d - 0.5); while (xc(iF) > 0.15) iF--; const pf = pRow(iF) + (pRow(iF) - pRow(iF - 1)) * (0.15 - xc(iF)) / d;
let iB = Math.ceil(0.25 / d - 0.5); while (xc(iB) < 0.25) iB++; const pb = pRow(iB) + (pRow(iB) - pRow(iB + 1)) * (xc(iB) - 0.25) / d;
console.log(JSON.stringify({ opt: process.env.OPT || 'base', cells_per_D: +(0.1 / dx).toFixed(1), dt: H * NS, cD_body: +(2 * Fx / 0.004).toFixed(3), cD_pressure: +(2 * w.cartForce(w.pF) / 0.004).toFixed(3), cD_cv: +(2 * Fcv / 0.004).toFixed(3), La: +La.toFixed(4), dp: +(pf - pb).toFixed(4), ref: 'cD 5.57-5.59, La 0.0842-0.0852, dp 0.1172-0.1176' }));
