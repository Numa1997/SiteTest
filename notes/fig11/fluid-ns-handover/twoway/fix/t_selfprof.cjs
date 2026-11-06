// Rods held upright across a uniform stream U, no cart: dump, per rod point, the position, the velocity read and the force per metre.
// Used to test whether a linear 2D Oseen self-influence predicts the slowing the solver measures, point by point.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const med = process.env.MED || 'glycerol', dx = +(process.env.DX || 0.025), U = +(process.env.U || 0.5), TEND = +(process.env.TEND || 4);
const ang = +(process.env.ANG || 0) * Math.PI / 180;   // both rods tilted by ang (0 = upright, across the stream)
const w = new T.World({ dx, U, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, ang, ang, 0, 0, 0], nsub: 10 });
w.frozen = true; w.cartGone = true; w.selfField = false; for (const k of (process.env.OPT || '').split(',').filter(Boolean)) w[k] = true;
while (w.t < TEND - 1e-9) w.step(null);
const p = w.mp, NP = T.NP, dtf = w.h * w.nsub, pts = [];
for (let k = 0; k < 2; k++) for (let i = 0; i < NP; i++) { const o = 2 * (k * NP + i), K = T.pointKin(p, w.s, k, i, {});
  pts.push({ k, X: w.pos[o], Y: w.pos[o + 1], ux: w.uS[o], uy: w.uS[o + 1], wq: K.wq, fx: w.impNew[o] / dtf / K.wq, fy: w.impNew[o + 1] / dtf / K.wq }); }
const out = { med, dx, U, ang: ang * 180 / Math.PI, rho: w.rho, nu: w.nu, b: w.b, xi: p.xi, cq: p.cq, pts };
require('fs').writeFileSync(process.env.OUT || `fix/prof_${med}_${U}_${dx}_${(ang*180/Math.PI)|0}.json`, JSON.stringify(out));
let F = 0, us = 0; for (const q of pts) { F += q.fx * q.wq; us += q.ux; } us /= pts.length;
console.log(med, U, dx, 'meanSlow/U', ((U - us) / U).toFixed(4), 'F', F.toFixed(4));
