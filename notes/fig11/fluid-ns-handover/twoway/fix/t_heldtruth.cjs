// Per-rod self field, rods held in a stream U: each rod's force against its truth run (that rod not pushing, the other pushing), and the
// isolated law. ANG: 0 across, 90 along, 45.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay, NP = T.NP;
const med = process.env.MED || 'glycerol', U = +(process.env.U || 0.5), ang = +(process.env.ANG || 0) * Math.PI / 180, dx = +(process.env.DX || 0.025);
function run(o) { const w = new T.World({ dx, U, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, ang, ang, 0, 0, 0], nsub: 10, selfField: !!o.self });
  w.cartGone = true; w.frozen = true; if (o.np !== undefined) w.noPushRod = o.np; while (w.t < 4 - 1e-9) w.step(null);
  const F = [[0, 0], [0, 0]]; for (let k = 0; k < 2; k++) for (let i = 0; i < NP; i++) { const q = 2 * (k * NP + i); F[k][0] += w.impNew[q] / (w.h * w.nsub); F[k][1] += w.impNew[q + 1] / (w.h * w.nsub); } return F; }
const S = run({ self: true }), B = run({}), T0 = run({ np: 0 }), T1 = run({ np: 1 }), tr = [T0[0], T1[1]];
const mag = (v) => Math.hypot(v[0], v[1]), dev = (a, b) => mag([a[0] - b[0], a[1] - b[1]]) / mag(b);
console.log(JSON.stringify({ med, U, ang: process.env.ANG || 0, dx, rod0: { self_vs_truth: +dev(S[0], tr[0]).toFixed(4), base_vs_truth: +dev(B[0], tr[0]).toFixed(4) }, rod1: { self_vs_truth: +dev(S[1], tr[1]).toFixed(4), base_vs_truth: +dev(B[1], tr[1]).toFixed(4) } }));
