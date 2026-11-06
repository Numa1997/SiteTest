// Acceptance test of the rods' self field: force on the rods over the law at the undisturbed relative velocity, as vectors.
// MODE=held: rods held at angle ANG (deg from upright) in a stream U.  MODE=moving: no stream; the rods (no cart) carried at speed V through still water.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const med = process.env.MED || 'glycerol', dx = +(process.env.DX || 0.025), U = +(process.env.U || 0.5), ang = +(process.env.ANG || 0) * Math.PI / 180, mode = process.env.MODE || 'held';
const V = +(process.env.V || 0.3), TEND = +(process.env.TEND || (mode === 'moving' ? 3 : 4)), x0 = mode === 'moving' ? -1.2 : 0;
const w = new T.World({ dx, U: mode === 'moving' ? 0 : U, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [x0, ang, ang, mode === 'moving' ? V : 0, 0, 0], nsub: 10 });
w.cartGone = true; if (process.env.ONEV) w.selfOneV = true; if (process.env.TAU) w.selfTau = +process.env.TAU; if (process.env.STOL) w.selfTol = +process.env.STOL; if (mode === 'moving') w.kinematic = (t) => [x0 + V * t, ang, ang, V, 0, 0]; else w.frozen = true;
w.selfField = false; for (const k of (process.env.OPT || '').split(',').filter(Boolean)) w[k] = true;
while (w.t < TEND - 1e-9) w.step(null);
const p = w.mp, NP = T.NP, dtf = w.h * w.nsub, Uw = mode === 'moving' ? 0 : U; let Fx = 0, Fy = 0, Rx = 0, Ry = 0; const f = {};
for (let k = 0; k < 2; k++) for (let i = 0; i < NP; i++) { const o = 2 * (k * NP + i), K = T.pointKin(p, w.s, k, i, {});
  Fx += w.impNew[o] / dtf; Fy += w.impNew[o + 1] / dtf; w.rodForce(k, K, Uw, 0, 0, 0, f); Rx += K.wq * f.fx; Ry += K.wq * f.fy; }
const R2 = Rx * Rx + Ry * Ry, along = (Fx * Rx + Fy * Ry) / R2, perp = (Fy * Rx - Fx * Ry) / R2;
console.log(JSON.stringify({ tau: process.env.TAU || 'inf', perrod: !!process.env.PERROD, med, mode, U: mode === 'moving' ? V : U, dx, ang: +(ang * 180 / Math.PI).toFixed(0), opt: process.env.OPT || 'base', law_N: +Math.sqrt(R2).toFixed(4), F_over_law: +along.toFixed(4), sideways: +perp.toFixed(4) }));
