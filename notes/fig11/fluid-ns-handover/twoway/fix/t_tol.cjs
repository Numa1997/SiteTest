// Main pressure tolerance 1e-4 against 1e-3 on the page's tank: the cart's added mass m_a, its fluid force F_c and the state, step by step over a balancing run.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay, P = require('../../waterlily/pageparams.json');
const med = process.env.MED || 'glycerol', Kg = P[med].K;
function run(tol) { const w = new T.World({ dx: 0.025, U: +(process.env.U || 0), machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, 0.08, 0.05, 0, 0, 0], nsub: 20 }); w.P.tol = tol;
  let uh = 0, tN = 0; const ctrl = (s, t) => { if (t >= tN - 1e-9) { uh = 0; for (let i = 0; i < 6; i++) uh -= Kg[i] * s[i]; uh = Math.max(-60, Math.min(60, uh)); tN += 0.01; } return uh; };
  const out = [], t0 = Date.now(); let its = 0, n = 0; while (w.t < 3 - 1e-9) { w.step(ctrl); out.push([w.ma, w.Fc, w.s[0], w.s[1], w.maxDiv()]); its += w.its0 + w.itsx; n++; } return { out, ms: (Date.now() - t0) / n, its: its / n }; }
const A = run(1e-4), B = run(1e-3); let dma = 0, dF = 0, dx = 0, dth = 0, Fm = 0, divA = 0, divB = 0;
for (let i = 0; i < A.out.length; i++) { const a = A.out[i], b = B.out[i]; dma = Math.max(dma, Math.abs(a[0] - b[0]) / a[0]); dF = Math.max(dF, Math.abs(a[1] - b[1])); Fm = Math.max(Fm, Math.abs(a[1])); dx = Math.max(dx, Math.abs(a[2] - b[2])); dth = Math.max(dth, Math.abs(a[3] - b[3])); divA = Math.max(divA, a[4]); divB = Math.max(divB, b[4]); }
console.log(med, 'max |Δm_a|/m_a', dma.toExponential(2), 'max |ΔF_c| N', dF.toExponential(2), 'of max |F_c|', Fm.toFixed(3), 'max |Δx| m', dx.toExponential(2), 'max |Δθ1| rad', dth.toExponential(2), 'max div 1e-4/1e-3', divA.toExponential(2), divB.toExponential(2), 'ms', A.ms.toFixed(1), B.ms.toFixed(1), 'its', A.its.toFixed(2), B.its.toFixed(2));
