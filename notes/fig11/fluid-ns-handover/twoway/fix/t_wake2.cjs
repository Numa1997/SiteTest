// How big is the wake-return part? Rods carried back and forth through still water; per-rod self field with memory τ = ∞, 1 s, 0.2 s,
// and the truth runs (rod k not pushing). rms force differences relative to the truth's rms, over t > 1 s.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const med = process.env.MED || 'glycerol', A = +(process.env.A || 0.15), om = +(process.env.OM || 4), TEND = +(process.env.TEND || 6), NP = T.NP;
function run(o) { const w = new T.World({ dx: 0.025, U: 0, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, 0, 0, A * om, 0, 0], nsub: 10, selfField: !!o.self });
  w.cartGone = true; w.kinematic = (t) => [A * Math.sin(om * t), 0, 0, A * om * Math.cos(om * t), 0, 0]; if (o.noPushRod !== undefined) w.noPushRod = o.noPushRod; if (o.self) { w.selfPerRod = true; if (process.env.ONEV) w.selfOneV = true; if (o.tau) w.selfTau = o.tau; }
  const F = [[], []]; while (w.t < TEND - 1e-9) { w.step(null); for (let k = 0; k < 2; k++) { let f = 0; for (let i = 0; i < NP; i++) f += w.impNew[2 * (k * NP + i)]; F[k].push(f / (w.h * w.nsub)); } } return F; }
const R = { base: run({}), inf: run({ self: true }), t1: run({ self: true, tau: 1 }), t02: run({ self: true, tau: 0.2 }) }, tr = [run({ noPushRod: 0 }), run({ noPushRod: 1 })];
const n0 = 100, rms = (a) => Math.sqrt(a.slice(n0).reduce((s, v) => s + v * v, 0) / (a.length - n0)), rd = (a, b) => Math.sqrt(a.slice(n0).reduce((s, v, i) => s + (v - b[i + n0]) ** 2, 0) / (a.length - n0));
const out = { med, A, om, period_s: +(2 * Math.PI / om).toFixed(2) };
for (let k = 0; k < 2; k++) { const T0 = rms(tr[k][k]), o = {}; for (const key in R) o[key + '_vs_truth'] = +(rd(R[key][k], tr[k][k]) / T0).toFixed(4); o.inf_vs_t02 = +(rd(R.inf[k], R.t02[k]) / T0).toFixed(4); out['rod' + k] = o; }
console.log(JSON.stringify(out));
