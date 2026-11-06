// Held rods, self field on: is the velocity the rods use (u_read − u_self) equal to U?  And how does the force compare with the law at that velocity?
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const med = process.env.MED || 'glycerol', dx = +(process.env.DX || 0.025), U = +(process.env.U || 0.5), ang = +(process.env.ANG || 0) * Math.PI / 180;
const w = new T.World({ dx, U, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, ang, ang, 0, 0, 0], nsub: 10 });
w.frozen = true; w.cartGone = true; w.selfField = true; for (const k of (process.env.OPT || '').split(',').filter(Boolean)) w[k] = true;
const TEND = +(process.env.TEND || 4); while (w.t < TEND - 1e-9) w.step(null);
const NP = T.NP; let ue = 0, ur = 0, umin = 1e9, umax = -1e9;
for (let o = 0; o < 4 * NP; o += 2) { const e = w.uS[o] - w.uSelf[o]; ue += e; ur += w.uS[o]; umin = Math.min(umin, e); umax = Math.max(umax, e); }
ue /= 2 * NP; ur /= 2 * NP;
let F = 0; for (let o = 0; o < 4 * NP; o += 2) F += w.impNew[o]; F /= (w.h * w.nsub);
const p = w.mp, law = (xi, V) => xi * V + p.cq * V * V, F0 = law(p.xi[0], U) * p.L1 + law(p.xi[1], U) * p.L2;
console.log(med, 'U', U, 'dx', dx, 'ang', process.env.ANG || 0, '| u_read/U', (ur / U).toFixed(4), 'u_eff/U', (ue / U).toFixed(4), 'min', (umin / U).toFixed(4), 'max', (umax / U).toFixed(4), '| drag/law(U)', (F / F0).toFixed(4));
if (process.env.DBG) { const dtf = w.h * w.nsub; for (let k = 0; k < 2; k++) for (const i of [0, 6, 12, 23]) { const o = 2 * (k * NP + i), K = T.pointKin(p, w.s, k, i, {});
  console.log(k, i, 'Y', w.pos[o + 1].toFixed(3), 'uE', (w.uE[o] / U).toFixed(4), 'aS', w.aS[o].toExponential(2), 'f/law', (w.impNew[o] / dtf / K.wq / law(p.xi[k], U)).toFixed(4)); } }
if (process.env.DBG) { const o = 2 * (0 * NP + 12), K = T.pointKin(p, w.s, 0, 12, {}), f = {}; w.rodForce(0, K, w.uE[o], w.uE[o + 1], w.aS[o], w.aS[o + 1], f);
  console.log('direct rodForce/law', (f.fx / law(p.xi[0], U)).toFixed(5), 'uE', w.uE[o], 'uS', w.uS[o], 'uSelf', w.uSelf[o], 'vx', K.vx, 'xi', p.xi[0], 'cq', p.cq, 'kr', p.kr); }
