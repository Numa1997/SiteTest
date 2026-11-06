// A channel whose walls are BODIES that cut through the cells (not grid-aligned): plane Poiseuille between y = ya and y = ya + Hc.
// Exact: u = 4 U_max s (Hc − s)/Hc², dp/dx = −8 μ U_max / Hc². Tests the cut-cell no-slip and pressure for flow ALONG a wall.
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const off = +(process.env.OFF || 0.37), ny = +(process.env.NY || 48), dx = 0.5 / ny, nx = Math.ceil(1.2 / dx / 8) * 8, Hc = 0.41, ya = 0.04 + off * dx, Um = 0.3;
const w = new T.World({ dx, nx, ny, x0: 0, y0: 0, rho: 1, mu: 1e-3, machine: { m0: 1, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, h: 0.002, nsub: 5 });
w.frozen = true; w.noRods = true; w.b = 1; w.noslip = true; for (const k of (process.env.OPT || '').split(',').filter(Boolean)) w[k] = true;
const prof = (y) => { const s = y - ya; return s > 0 && s < Hc ? 4 * Um * s * (Hc - s) / (Hc * Hc) : 0; };
w.inflow = prof; const sdf = (X, Y) => Math.min(Y - ya, ya + Hc - Y) * -1 < 0 ? -Math.min(Y - ya, ya + Hc - Y) * -1 * -1 : 0;
w.geom = function () { this.measureSdf((X, Y) => Math.min(Y - ya, ya + Hc - Y)); };   // positive in the channel, negative in the walls (the body)
for (let j = 0; j < ny; j++) for (let i = 0; i <= nx; i++) w.u[j * (nx + 1) + i] = prof(w.yu(j));
while (w.t < +(process.env.TEND || 6) - 1e-9) w.step(null);
const P = (i, j) => w.pF[j * nx + i], jm = Math.round((ya + Hc / 2) / dx - 0.5), i1 = Math.round(0.3 / dx), i2 = Math.round(0.9 / dx);
const g = (P(i2, jm) - P(i1, jm)) / ((i2 - i1) * dx), ex = -8e-3 * Um / (Hc * Hc);
let err = 0, umax = 0; const ic = Math.round(0.6 / dx); for (let j = 0; j < ny; j++) { const y = w.yu(j); if (y - ya > 0 && ya + Hc - y > 0) { err = Math.max(err, Math.abs(w.u[j * (nx + 1) + ic] - prof(y))); umax = Math.max(umax, w.u[j * (nx + 1) + ic]); } }
console.log(JSON.stringify({ opt: process.env.OPT || 'base', off, ny, dpdx: +g.toFixed(6), exact: +ex.toFixed(6), err_pct: +(100 * (g / ex - 1)).toFixed(2), max_u_err_over_Um: +(err / Um).toFixed(4), umax: +umax.toFixed(4) }));
