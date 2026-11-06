require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay, P = require('../../waterlily/pageparams.json');
const Kg = P.glycerol.K;
function run(ex) { const w = new T.World({ dx: 0.025, U: +(process.env.U || 0), machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, s: [0, 0.08, 0.05, 0, 0, 0], nsub: 20 }); w.P.extrap = ex;
  let uh = 0, tN = 0; const ctrl = (s, t) => { if (t >= tN - 1e-9) { uh = 0; for (let i = 0; i < 6; i++) uh -= Kg[i] * s[i]; uh = Math.max(-60, Math.min(60, uh)); tN += 0.01; } return uh; };
  for (let k = 0; k < 20; k++) w.step(ctrl); const t0 = Date.now(); let its = [0, 0, 0], n = 0, div = 0; while (w.t < 3 - 1e-9) { w.step(ctrl); its[0] += w.its0; its[1] += w.itsx; its[2] += w.itsS; n++; div = Math.max(div, w.maxDiv()); }
  return { ms: ((Date.now() - t0) / n).toFixed(1), its: its.map(v => (v / n).toFixed(2)).join('/'), maxdiv: div.toExponential(2), s: w.s.slice(0, 3).map(v => v.toFixed(5)).join(' '), ma: w.ma.toFixed(4) }; }
for (const e of [true, false, true, false]) console.log(e ? 'extrap' : 'plain ', JSON.stringify(run(e)));
