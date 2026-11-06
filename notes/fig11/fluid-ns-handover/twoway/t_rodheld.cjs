// T3: both rods held upright in a uniform stream U. The page's law gives f = ξU + c_q U² per metre (across the rod). How much of it does the
// actuator line keep once its own wake has formed? The rod reads the grid velocity at its points, which its own force has slowed down.
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const med = process.env.MED || 'glycerol', dx = +(process.env.DX || 0.025), U = +(process.env.U || 0.5), dur = +(process.env.DUR || 4);
const w = new T.World({ dx, U, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, 0, 0, 0, 0, 0], nsub: 10 });
w.frozen = true; w.cartGone = !!process.env.NOCART;
const p = w.mp, law = (xi) => xi * U + p.cq * U * U;   // per metre, rod at rest, flow U across it
const F0 = law(p.xi[0]) * p.L1 + law(p.xi[1]) * p.L2;
for (let n = 1; w.t < dur - 1e-9; n++) { w.step(null);
  if (n % 50 === 0) { let Fx = 0; for (let o = 0; o < 4 * T.NP; o += 2) Fx += w.impNew[o]; Fx /= 0.01; let us = 0, uu = 0; for (let o = 0; o < 4 * T.NP; o += 2) { us += w.uS[o]; } us /= 2 * T.NP;
    console.log(JSON.stringify({ t: +w.t.toFixed(2), F_rods: +Fx.toFixed(3), F_law_undisturbed: +F0.toFixed(3), ratio: +(Fx / F0).toFixed(3), mean_u_at_rods: +us.toFixed(4), U })); } }
