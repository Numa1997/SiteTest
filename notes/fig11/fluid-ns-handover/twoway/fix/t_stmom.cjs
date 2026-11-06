// Error 3, discriminating test on Schäfer–Turek 2D-1 at steady state: the force on the cylinder three ways.
// (a) read on the body (Q0: pressure, shear, overrides), (b) control volume round it (as t_st2), (c) the whole channel's balance:
// momentum in at the inlet minus out at the outlet, plus the inlet pressure force, plus the channel walls' shear (counted in diffuse), per second.
// Also the momentum each operator changes, over the last second, with the operators' own credits.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const ny = +(process.env.NY || 40), dx = 0.41 / ny, nx = Math.ceil(2.2 / dx / 8) * 8, H = +(process.env.H || 0.002), NS = 5;
const w = new T.World({ dx, nx, ny, x0: 0, y0: 0, rho: 1, mu: 1e-3, machine: { m0: 1, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, h: H, nsub: NS, selfField: false });
w.U = 0; w.inflow = (y) => 4 * 0.3 * y * (0.41 - y) / (0.41 * 0.41); w.noslip = true; w.frozen = true; w.noRods = true; w.b = 1;
for (const k of (process.env.OPT || '').split(',').filter(Boolean)) w[k] = true;
w.geom = process.env.NOCYL ? function () { this.cartGone = true; this.measure(); } : function () { this.measureCircle(0.2, 0.2, 0.05); }; for (let c = 0; c < w.u.length; c++) w.u[c] = 0;
const TEND = +(process.env.TEND || 12); while (w.t < TEND - 1 - 1e-9) w.step(null);
const snap = () => JSON.parse(JSON.stringify(w.book)); const B0 = snap(), P0 = w.momX(); let Q = 0, ends = 0, endsF = 0, endsP = 0, n = 0; const Wu = nx + 1, dt = H * NS;
while (w.t < TEND - 1e-9) { w.step(null); Q += w.Q0; n++;
  let f = 0, fF = 0, fP = 0; for (let j = 0; j < ny; j++) { const ui = w.u[j * Wu], uo = w.u[j * Wu + nx]; fF += (ui * ui - uo * uo) * dx; fP += w.pF[j * nx] * dx / w.rho; } f = fF + fP; ends += w.rho * w.b * f; endsF += w.rho * w.b * fF; endsP += w.rho * w.b * fP; }
const B1 = snap(), d = (k) => ((B1[k] || 0) - (B0[k] || 0)) / (n * dt), cD = (F) => +(2 * F / (0.2 * 0.2 * 0.1)).toFixed(4);
const Fbody = Q / n, Fglob = ends / n + d('Pwall'), dPdt = (w.momX() - P0) / (n * dt);
const Fp = Fbody + d('Pshear') + d('Pimp'); console.log(JSON.stringify({ left_adv: +(d('Padv') - endsF / n - d('PimpA')).toExponential(2), left_proj: +(d('Pproj') - endsP / n + Fp - d('PimpP')).toExponential(2), left_diff: +(d('Pdiff') - d('Pwall') - d('Pshear') - d('PimpD')).toExponential(2), left_geom: +(d('PgeomEtc') - (d('Pimp') - d('PimpA') - d('PimpD') - d('PimpP'))).toExponential(2), cells_per_D: +(0.1 / dx).toFixed(1), dt, cD_body: cD(Fbody), cD_global: cD(Fglob - dPdt), dP_fluid_per_s: +dPdt.toExponential(2),
  per_s: { P_adv: +d('Padv').toFixed(6), P_diff: +d('Pdiff').toFixed(6), P_proj: +d('Pproj').toFixed(6), P_geom: +d('PgeomEtc').toFixed(6), shear_body: +d('Pshear').toFixed(6), wall: +d('Pwall').toFixed(6), ends: +(ends / n).toFixed(6), body: +Fbody.toFixed(6), imp_adv: +d('PimpA').toFixed(6), imp_diff: +d('PimpD').toFixed(6), imp_proj: +d('PimpP').toFixed(6), imp_all: +d('Pimp').toFixed(6), toCart: +d('toCartP').toFixed(6) } }));
