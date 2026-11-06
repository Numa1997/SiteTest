const { World } = require('./mac.cjs');
const L = 2.56, n = 256, a = 0.08, rho = 1000;
const W = new World({ nx: n, ny: n, dx: L / n, x0: -L / 2, y0: -L / 2, rho, nu: 1e-3, U: 0.5, levels: 7 });
const circ = { nb: 1, q: [0, 0, 0], qd: [0, 0, 0], depth: [1], pose() {}, bbox() { return [this.q[0] - a, this.q[0] + a, -a, a]; }, sdf(k, X, Y) { return Math.hypot(X - this.q[0], Y) - a; }, jac() { return [[1, 0], [0, 0], [0, 0]]; },
  implicitStep(dt, u, Q0, K) { return [0, 0, 0]; }, advance() {} };
const T = {}; const tic = (k, f) => { const t = process.hrtime.bigint(); const r = f(); T[k] = (T[k] || 0) + Number(process.hrtime.bigint() - t) / 1e6; return r; };
const dt = 2e-3;
for (let s = 0; s < 10; s++) {
  tic('measure', () => W.measure(circ)); tic('impose', () => W.imposeBody(circ.qd)); tic('advect', () => W.advect(dt)); tic('diffuse', () => W.diffuse(dt, circ.qd));
  tic('rhs+solve p0', () => { W.rhsFluid(W.rhs); for (let c = 0; c < W.rhs.length; c++) W.rhs[c] *= rho / dt; return W.P.solve(W.rhs, W.p[0]); });
  tic('rhs+solve p1', () => { W.rhsBody(0, W.rhs); for (let c = 0; c < W.rhs.length; c++) W.rhs[c] *= rho / dt; return W.P.solve(W.rhs, W.p[1]); });
  tic('genForce', () => W.genForce(W.p[0], [1]));
  tic('project', () => W.project(W.p[0], dt));
}
for (const k in T) console.log(k.padEnd(14), (T[k] / 10).toFixed(1), 'ms');
