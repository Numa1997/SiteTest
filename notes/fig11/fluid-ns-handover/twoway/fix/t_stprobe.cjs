// Schäfer–Turek 2D-1 on the MAC solver: the probes of the Wolfram FEM reference (fix/STATUS.md), to find where the flow departs.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const ny = +(process.env.NY || 40), dx = 0.41 / ny, nx = Math.ceil(2.2 / dx / 8) * 8, NS = +(process.env.NS || 5);
const w = new T.World({ dx, nx, ny, x0: 0, y0: 0, rho: 1, mu: 1e-3, machine: { m0: 1, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, h: 0.002, nsub: NS, selfField: false });
w.U = 0; w.inflow = (y) => 4 * 0.3 * y * (0.41 - y) / (0.41 * 0.41); w.noslip = true; w.frozen = true; w.noRods = true; w.b = 1;
for (const k of (process.env.OPT || '').split(',').filter(Boolean)) w[k] = true;
w.geom = function () { this.measureCircle(0.2, 0.2, 0.05); }; for (let c = 0; c < w.u.length; c++) w.u[c] = 0; while (w.t < +(process.env.TEND || 12) - 1e-9) w.step(null);
const pAt = (X, Y) => { const gx = X / dx - 0.5, gy = Y / dx - 0.5, i = Math.floor(gx), j = Math.floor(gy), a = gx - i, b = gy - j, P = (ii, jj) => w.pF[jj * nx + ii]; return (1 - b) * ((1 - a) * P(i, j) + a * P(i + 1, j)) + b * ((1 - a) * P(i, j + 1) + a * P(i + 1, j + 1)); };
const R = +(process.env.R || 0.0501), r5 = (v) => +v.toFixed(5);
const out = { cells_per_D: +(0.1 / dx).toFixed(1), opt: process.env.OPT || 'base' };
out.surfp = [0, 1, 2, 3, 4, 5, 6, 7].map(k => r5(pAt(0.2 + R * Math.cos(k * Math.PI / 4), 0.2 + R * Math.sin(k * Math.PI / 4))));
out.paxis = [0, 0.05, 0.1, 0.14, 0.15, 0.25, 0.26, 0.3, 0.5, 1.0, 1.5].map(x => r5(pAt(Math.max(x, dx / 2), 0.2)));
out.ugap = [0.252, 0.26, 0.28, 0.30, 0.33, 0.36, 0.40].map(y => r5(w.velAt(0.2, y)[0]));
out.uwake = [0.27, 0.30, 0.33, 0.36, 0.4, 0.5, 0.7, 1.0].map(x => r5(w.velAt(x, 0.2)[0]));
out.uup = [0.05, 0.1, 0.13, 0.145].map(x => r5(w.velAt(x, 0.2)[0]));
console.log(JSON.stringify(out));
