// Is one multigrid V-cycle, as a stationary iteration x += ω V(b − A x), convergent for the tank's pressure? Convergence factor per cycle for several ω.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const w = new T.World({ dx: 0.025, U: 0.3, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, s: [0, 0.08, 0.05, 0, 0, 0], nsub: 20 });
for (let k = 0; k < 10; k++) w.step(() => 0);
const P = w.P, L0 = P.L[0], N = w.nx * w.ny, b = new Float64Array(N); w.withShadow(function () { this.divFluid(b); }, 0); for (let i = 0; i < N; i++) b[i] *= w.rho / 0.02;
const res = (x) => { P.apply(L0, x, P.Ap); let s = 0; for (let c = 0; c < N; c++) { const r = L0.d[c] ? b[c] - P.Ap[c] : 0; s += r * r; } return Math.sqrt(s); };
for (const om of [1, 0.8, 0.6, 0.5, 0.4]) { const x = new Float64Array(N); const r0 = res(x); const rs = [];
  for (let it = 0; it < 6; it++) { P.apply(L0, x, P.Ap); for (let c = 0; c < N; c++) P.rr[c] = L0.d[c] ? b[c] - P.Ap[c] : 0; L0.b.set(P.rr); P.vcycle(0); for (let c = 0; c < N; c++) x[c] += om * L0.x[c]; rs.push(res(x) / r0); }
  console.log('ω', om, rs.map(v => v.toExponential(1)).join(' ')); }
