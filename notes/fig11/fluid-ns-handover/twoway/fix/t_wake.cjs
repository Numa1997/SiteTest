// The mother session's test of the self field: rods carried back and forth through still water (no cart), x = A sin(ωt), rods upright.
// Runs: base (rods read u), self (rods read u − δu), and for each rod k a truth run where rod k does not push (rod k reads u: the other rod's
// wake and its own nothing). Reported per rod: rms force, and the rms difference of the force from the truth run (rod-rod part), over t > 1 s.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const med = process.env.MED || 'glycerol', A = +(process.env.A || 0.15), om = +(process.env.OM || 4), TEND = +(process.env.TEND || 4), NP = T.NP;
const ang = +(process.env.ANG || 0) * Math.PI / 180;
function run(o) { const w = new T.World({ dx: 0.025, U: 0, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, ang, ang, A * om, 0, 0], nsub: 10, selfField: !!o.self });
  w.cartGone = true; w.kinematic = (t) => [A * Math.sin(om * t), ang, ang, A * om * Math.cos(om * t), 0, 0]; if (o.noPushRod !== undefined) w.noPushRod = o.noPushRod; if (o.self) { if (process.env.PERROD) w.selfPerRod = true; if (process.env.TAU) w.selfTau = +process.env.TAU; }
  const F = [[], []]; while (w.t < TEND - 1e-9) { w.step(null); for (let k = 0; k < 2; k++) { let f = 0; for (let i = 0; i < NP; i++) f += w.impNew[2 * (k * NP + i)]; F[k].push(f / (w.h * w.nsub)); } } return F; }
const base = run({}), self = run({ self: true }), tr = [run({ noPushRod: 0 }), run({ noPushRod: 1 })];
const n0 = Math.round(1 / 0.01), rms = (a) => Math.sqrt(a.slice(n0).reduce((s, v) => s + v * v, 0) / (a.length - n0)), rd = (a, b) => Math.sqrt(a.slice(n0).reduce((s, v, i) => s + (v - b[i + n0]) ** 2, 0) / (a.length - n0));
const out = { med, A, om, KC_kernel: +(2 * Math.PI * A / 0.1).toFixed(2) };
for (let k = 0; k < 2; k++) out['rod' + k] = { rms_base: +rms(base[k]).toFixed(4), rms_self: +rms(self[k]).toFixed(4), rms_truth: +rms(tr[k][k]).toFixed(4),
  base_vs_truth: +(rd(base[k], tr[k][k]) / rms(tr[k][k])).toFixed(4), self_vs_truth: +(rd(self[k], tr[k][k]) / rms(tr[k][k])).toFixed(4) };
console.log(JSON.stringify(out));
