require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const w = new T.World({ dx: 0.025, U: 0.3, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: process.env.MED || 'glycerol' }, s: [0, 0.08, 0.05, 0, 0, 0], nsub: 20 });
w.selfField = true; if (process.env.STOL) w.selfTol = +process.env.STOL; for (let k = 0; k < 20; k++) w.step(() => 0);
const tm = {}; for (const f of ['shadowAdvectStored', 'shadowDiffuse', 'shadowProject', 'shadowSpread', 'shadowRead']) { const g = w[f].bind(w); tm[f] = 0; w[f] = function (a) { const t = process.hrtime.bigint(); g(a); tm[f] += Number(process.hrtime.bigint() - t) / 1e6; }; }
let its = 0; for (let k = 0; k < 50; k++) { w.step(() => 0); its += w.itsS; }
for (const f in tm) tm[f] = +(tm[f] / 50).toFixed(2); console.log(tm, 'itsS mean', its / 50);
