// Test 1: Taylor-Green vortex, exact decay exp(-2 nu k^2 t); and the speed of one step at several grid sizes.
const { Solver } = require('./ns.cjs');
const L = 2 * Math.PI, U = 1, k = 1, nu = 0.01;
for (const N of [64, 128, 256, 512, 1024]) {
  const s = new Solver({ N, M: N, Lx: L, Ly: L, nu, eta: 1e9, cfl: 0.2 });
  s.setOmega((x, y) => 2 * U * k * Math.sin(k * x) * Math.sin(k * y));
  const T = 1, dt = 0.01; let t0 = Date.now(), n = 0;
  const nmax = N >= 1024 ? 10 : Math.round(T / dt);
  for (; n < nmax; n++) s.step(dt);
  const ms = (Date.now() - t0) / n;
  s.velocity(); const t = s.t, f = Math.exp(-2 * nu * k * k * t);
  let e = 0, m = 0;
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) { const p = j * N + i, x = (i + 0.5) * s.dx, y = (j + 0.5) * s.dy;
    const ue = U * Math.sin(k * x) * Math.cos(k * y) * f; e = Math.max(e, Math.abs(s.u[p] - ue)); m = Math.max(m, Math.abs(ue)); }
  console.log(`N=${N}  t=${t.toFixed(2)}  max|u-u_exact|/max|u| = ${(e / m).toExponential(2)}  ${ms.toFixed(1)} ms/step`);
}
