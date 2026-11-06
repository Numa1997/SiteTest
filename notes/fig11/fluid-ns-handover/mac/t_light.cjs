// T1: a light cylinder (mass 0.1 of the displaced fluid) pushed by a constant force in fluid at rest.
// Potential flow at early times: acceleration = F / (m + rho pi a^2) exactly (added mass of a circle = displaced mass).
// Tests the implicit coupling (light body) and the variational pressure's added mass at modest resolution.
const { World } = require('./mac.cjs');
const a = +(process.env.A || 0.08), dx = +(process.env.DX || 0.01), ratio = +(process.env.RATIO || 0.1), rho = 1000;
const L = 2.56, n = Math.round(L / dx / 16) * 16;
const W = new World({ nx: n, ny: n, dx: L / n, x0: -L / 2, y0: -L / 2, rho, nu: 0, U: 0, levels: 7 });
const mDisp = rho * Math.PI * a * a, m = ratio * mDisp, Fpush = 1.0;   // per metre of depth
const circ = {
  nb: 1, q: [0, 0, 0], qd: [0, 0, 0], depth: [1],
  pose() {}, bbox() { return [this.q[0] - a, this.q[0] + a, -a, a]; }, sdf(k, X, Y) { return Math.hypot(X - this.q[0], Y) - a; }, jac() { return [[1, 0], [0, 0], [0, 0]]; },
  implicitStep(dt, u, Q0, K) {   // m (qd' - qd)/dt = F + Q0 + K qd'   (x only; th1, th2 pinned)
    const qd = (m * this.qd[0] + dt * (Fpush + Q0[0])) / (m - dt * K[0][0]); return [qd, 0, 0]; },
  advance(dt, qdNew) { this.qd = qdNew; this.q[0] += dt * qdNew[0]; },
};
const dt = 2e-3, exact = Fpush / (m + mDisp); let t0 = Date.now(), out = [];
for (let k = 1; k <= 25; k++) { const r = W.step(circ, dt, 0); if (k % 5 === 0) out.push({ t: +(k * dt).toFixed(3), v: +circ.qd[0].toFixed(5), v_exact: +(exact * k * dt).toFixed(5), its: r.its, K00: +r.K[0][0].toFixed(2) }); }
const ms = (Date.now() - t0) / 25;
console.log(JSON.stringify({ a_over_dx: a / (L / n), grid: [n, n], ratio, accel: circ.qd[0] / W.t, exact, err_pct: +(100 * (circ.qd[0] / W.t / exact - 1)).toFixed(2), added_mass_measured_over_rhoPiA2: +((Fpush / (circ.qd[0] / W.t) - m) / mDisp).toFixed(4), ms_per_step: ms }));
console.log(JSON.stringify(out));
