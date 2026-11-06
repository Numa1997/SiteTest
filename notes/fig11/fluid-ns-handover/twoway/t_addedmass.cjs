// T1: the cart's added mass from the coupled pressure, m_a = -K_x dt, against the panel method's 0.020539 ρ b (unbounded potential flow).
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const exact = 0.020539 * 1261 * 0.2;
for (const dx of [0.025, 0.0125, 0.00625]) {
  const L = 6.4, n = Math.round(L / dx);
  const w = new T.World({ dx, nx: n, ny: n, x0: -L / 2, y0: -L / 2 + 0.06, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, nsub: 10 });
  w.measure(); w.P.tol = 1e-6; w.divCart(w.rhs); const f = w.rho / 0.01; for (let i = 0; i < w.rhs.length; i++) w.rhs[i] *= f; const its = w.P.solve(w.rhs, w.px, 400);
  const Kx = w.cartForce(w.px), ma = -Kx * 0.01;
  // the right edge is open (p = 0) and the left a wall: check the box effect by flipping which side the cart is near? It stands in the middle, 3.2 m from each.
  console.log(JSON.stringify({ dx, cells_per_height: +(0.12 / dx).toFixed(1), its, m_a: +ma.toFixed(4), exact: +exact.toFixed(4), err_pct: +(100 * (ma / exact - 1)).toFixed(2) }));
}
