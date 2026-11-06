// Discriminating test of the self field in a non-uniform flow: the cart swings (prescribed), the rods stand on it in the cart's wake.
// A: rods push the water, self field on: the rods use u − δu.  B: the same, but the rods do not push the water (noPush): the true undisturbed water.
// Compare u − δu (A) with u (B) at the rod points, every fluid step, and the forces from them.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const med = process.env.MED || 'glycerol', A0 = +(process.env.A || 0.3), om = +(process.env.OM || 3), TEND = +(process.env.TEND || 3), ang = +(process.env.ANG || 0) * Math.PI / 180;
function mk(push, self) { const w = new T.World({ dx: 0.025, U: +(process.env.U || 0), machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, ang, ang, A0 * om, 0, 0], nsub: 10 });
  w.kinematic = (t) => [A0 * Math.sin(om * t), ang, ang, A0 * om * Math.cos(om * t), 0, 0]; w.selfField = false; if (!push) w.noPush = true; else if (self) { w.selfField = true; if (process.env.STOL) w.selfTol = +process.env.STOL; } return w; }
const a = mk(true, true), b = mk(false), c = mk(true, false), NP = T.NP; let s2 = 0, sd2 = 0, ss2 = 0, n = 0, fA = 0, fB = 0, fdiff2 = 0;
let fC = 0; while (a.t < TEND - 1e-9) { a.step(null); b.step(null); c.step(null); if (a.t < 0.5) continue;
  for (let o = 0; o < 4 * NP; o++) { const d = a.uE[o] - b.uE[o]; sd2 += d * d; s2 += b.uE[o] * b.uE[o]; ss2 += (a.uS[o] - b.uE[o]) ** 2; n++; }
  let FA = 0, FB = 0; for (let o = 0; o < 4 * NP; o += 2) { FA += a.impNew[o]; FB += b.impNew[o]; } fdiff2 += (FA - FB) ** 2; fB += FB * FB; let FC = 0; for (let o = 0; o < 4 * NP; o += 2) FC += c.impNew[o]; fC += (FC - FB) ** 2; }
console.log(JSON.stringify({ med, A: A0, om, U: +(process.env.U || 0), rms_u_undisturbed: +Math.sqrt(s2 / n).toFixed(4), rms_err_corrected: +Math.sqrt(sd2 / n).toFixed(5), rms_err_uncorrected: +Math.sqrt(ss2 / n).toFixed(5), rel_force_err: +Math.sqrt(fdiff2 / fB).toFixed(4), rel_force_err_uncorrected: +Math.sqrt(fC / fB).toFixed(4) }));
