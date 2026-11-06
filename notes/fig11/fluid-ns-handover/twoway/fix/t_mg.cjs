// The pressure solver alone, on the page's tank with the cart in it: iterations and time to tol for different smoothing counts, from a cold and a warm start.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const w = new T.World({ dx: 0.025, U: 0.3, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, s: [0, 0.08, 0.05, 0, 0, 0], nsub: 20, selfField: false });
for (let k = 0; k < 30; k++) w.step(() => 0);
const P = w.P, N = w.nx * w.ny, b = new Float64Array(N); w.divFluid(b); for (let i = 0; i < N; i++) b[i] *= w.rho / 0.02; const pc = Float64Array.from(w.p0);
for (const [a, c] of [[2, 2], [1, 1], [1, 2], [3, 3]]) { P.nPre = a; P.nPost = c;
  let t = process.hrtime.bigint(), x = new Float64Array(N), it = P.solve(b, x); const tc = Number(process.hrtime.bigint() - t) / 1e6;
  let tw = 0, itw = 0; for (let r = 0; r < 20; r++) { const y = Float64Array.from(pc); for (let i = 0; i < N; i++) y[i] *= 1 + 0.01 * Math.sin(i); t = process.hrtime.bigint(); itw += P.solve(b, y); tw += Number(process.hrtime.bigint() - t) / 1e6; }
  console.log('pre/post', a, c, 'cold its', it, tc.toFixed(2), 'ms | warm its', (itw / 20).toFixed(2), (tw / 20).toFixed(2), 'ms'); }
