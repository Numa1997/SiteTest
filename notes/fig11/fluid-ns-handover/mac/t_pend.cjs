// T2: project 05's machine in the 2D two-way coupled fluid. Glycerol, breeze U, the page's controller (glycerol gains), 10 ms zero-order hold.
const { World, Machine } = require('./mac.cjs');
const fs = require('fs');
const U = +(process.env.U || 0.5), dx = +(process.env.DX || 0.0125), T = +(process.env.T || 4), HOLD = +(process.env.HOLD || 0.5), dt = +(process.env.DT || 0.005);
const rho = +(process.env.RHO || 1261), mu = +(process.env.MU || 1.412);
const nx = Math.round(3.2 / dx / 32) * 32, ny = Math.round(2.4 / dx / 32) * 32;
const W = new World({ nx, ny, dx, x0: -1.6, y0: -0.8, rho, nu: mu / rho, U, levels: 7 }); W.P.tol = 1e-5;
const M = new Machine({ rho }); M.q = [0, +(process.env.TH1 || 0.05), +(process.env.TH2 || -0.03)];
const held = { get nb() { return M.nb; }, get depth() { return M.depth; }, get q() { return M.q; }, get qd() { return M.qd; }, pose: () => M.pose(), sdf: (k, x, y) => M.sdf(k, x, y), bbox: (k) => M.bbox(k), jac: (k, x, y) => M.jac(k, x, y),
  implicitStep: () => [0, 0, 0], advance: () => {} };
const log = []; let u = 0, tNextU = 0, t = -HOLD; const t0 = Date.now();
while (t < T - 1e-9) {
  const holding = t < 0;
  if (!holding && t >= tNextU - 1e-9) { u = M.control([0, 0, 0, 0, 0, 0]); tNextU += M.Ts; }
  const r = W.step(holding ? held : M, dt, holding ? 0 : u); t += dt;
  if (Math.round(t / dt) % 10 === 0) { const row = { t: +t.toFixed(3), x: +M.q[0].toFixed(4), th1: +M.q[1].toFixed(4), th2: +M.q[2].toFixed(4), u: +u.toFixed(2), Qx: +r.Q[0].toFixed(3), Q1: +r.Q[1].toFixed(4), Q2: +r.Q[2].toFixed(4),
    cartFx: +r.per[0][0].toFixed(3), rod1Fx: +r.per[1][0].toFixed(3), rod2Fx: +r.per[2][0].toFixed(3), its: r.its.join('/'), div: +(r.div || 0).toExponential(1), wall: ((Date.now() - t0) / 1000).toFixed(0) };
    log.push(row); if (Math.round(t / dt) % (+(process.env.EVERY || 40)) === 0) console.log(JSON.stringify(row)); }
  if (Math.abs(M.q[1]) > 1.2 || Math.abs(M.q[2]) > 1.2 || M.q.some(isNaN)) { console.log('stopped: rods fell or NaN at t =', t.toFixed(3)); break; }
}
console.log(JSON.stringify({ grid: [nx, ny], dx, U, rho, mu, ms_per_step: (Date.now() - t0) / Math.round((t + HOLD) / dt), final: M.q.map(v => +v.toFixed(4)) }));
fs.writeFileSync(`pend_U${U}_dx${dx}.json`, JSON.stringify(log));
