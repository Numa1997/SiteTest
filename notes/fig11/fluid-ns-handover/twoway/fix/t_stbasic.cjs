// Schäfer–Turek 2D-1 set-up, sanity: mass flux through several sections, the profile 0.1 m downstream of the inlet against the parabola,
// and dp/dx far downstream against Poiseuille -8 mu U_max / H^2 (=-0.05712 Pa/m for U_max 0.3, H 0.41, mu 1e-3).
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const ny = +(process.env.NY || 40), dx = 0.41 / ny, nx = Math.ceil(2.2 / dx / 8) * 8;
const w = new T.World({ dx, nx, ny, x0: 0, y0: 0, rho: 1, mu: 1e-3, machine: { m0: 1, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, h: 0.002, nsub: 5, selfField: false });
w.U = 0; w.inflow = (y) => 4 * 0.3 * y * (0.41 - y) / (0.41 * 0.41); w.noslip = true; w.frozen = true; w.noRods = true; w.b = 1;
const CYL = process.env.NOCYL ? null : 1; w.geom = function () { if (CYL) this.measureCircle(0.2, 0.2, 0.05); else { this.cartGone = true; this.measure(); } };
for (let c = 0; c < w.u.length; c++) w.u[c] = 0; while (w.t < 12 - 1e-9) w.step(null);
const Wu = nx + 1, flux = (i) => { let s = 0; for (let j = 0; j < ny; j++) s += w.wu[j * Wu + i] * w.u[j * Wu + i] * dx; return s; };
const exactQ = 2 / 3 * 0.3 * 0.41; const out = { cells_per_D: +(0.1 / dx).toFixed(1), Q_exact: +exactQ.toFixed(6) };
for (const x of [0, 0.1, 0.2, 0.5, 1.0, 2.0]) out['Q@' + x] = +(flux(Math.round(x / dx)) / exactQ).toFixed(5);
let e = 0; const i1 = Math.round(0.1 / dx); for (let j = 0; j < ny; j++) e = Math.max(e, Math.abs(w.u[j * Wu + i1] - w.inflow((j + 0.5) * dx))); out.profile_err_at_0p1 = +(e / 0.3).toFixed(5);
const jc = Math.floor(ny / 2), pa = w.pF[jc * nx + Math.round(1.2 / dx)], pb = w.pF[jc * nx + Math.round(1.8 / dx)]; out.dpdx_far_over_poiseuille = +(((pb - pa) / ((Math.round(1.8 / dx) - Math.round(1.2 / dx)) * dx)) / (-8e-3 * 0.3 / (0.41 * 0.41))).toFixed(4);
out.umax_outlet = +Math.max(...Array.from({ length: ny }, (_, j) => w.u[j * Wu + nx - 1])).toFixed(5);
console.log(JSON.stringify(out));
