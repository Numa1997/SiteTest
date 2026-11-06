require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const a = +process.argv[2], b = +process.argv[3];
const w = new T.World({ dx: 0.025, U: 0.3, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, s: [0, 0.08, 0.05, 0, 0, 0], nsub: 20 }); w.P.nPre = a; w.P.nPost = b;
for (let k = 0; k < 20; k++) w.step(() => 0); const t0 = Date.now(); let its = 0; for (let k = 0; k < 60; k++) { w.step(() => 0); its += w.its0 + w.itsx; }
console.log('smooth', a, b, 'ms/step', ((Date.now() - t0) / 60).toFixed(1), 'main its/step', (its / 60).toFixed(2), 'state', w.s.slice(0, 3).map(v => v.toFixed(6)).join(' '));
