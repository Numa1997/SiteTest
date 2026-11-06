require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const w = new T.World({ dx: 0.025, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' } });
const tm = (f, n = 200) => { const t = process.hrtime.bigint(); for (let i = 0; i < n; i++) f(); return (Number(process.hrtime.bigint() - t) / 1e6 / n).toFixed(3); };
for (let r = 0; r < 2; r++) console.log('measure', tm(() => { w.s[0] += 1e-4; w.measure(); }), 'finishWeights', tm(() => w.finishWeights()), 'setWeights', tm(() => w.P.setWeights(w.wx, w.wy)));
