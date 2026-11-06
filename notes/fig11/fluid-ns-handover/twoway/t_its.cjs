require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay, P = require('../waterlily/pageparams.json'); const Kg = P.glycerol.K, dx = 0.025;
const w = new T.World({ dx, x0: -1.6, y0: -0.6, nx: 128, ny: 80, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, s: [0, 0.08, -0.05, 0, 0, 0], nsub: 10 });
let uh = 0, tN = 0; const ctrl = (s, t) => { if (t >= tN - 1e-9) { uh = 0; for (let i = 0; i < 6; i++) uh -= Kg[i] * s[i]; uh = Math.max(-60, Math.min(60, uh)); tN += 0.01; } return uh; };
const its = []; for (let n = 0; n < 200; n++) { w.step(ctrl); its.push([w.its0, w.itsx]); }
console.log(JSON.stringify(its.slice(-10)), 'levels', w.P.L.map(l => l.nx + 'x' + l.ny).join(' '));
let t = process.hrtime.bigint(); for (let k = 0; k < 20; k++) { w.P.L[0].b.set(w.rhs); w.P.vcycle(0); } console.log('vcycle ms', Number(process.hrtime.bigint() - t) / 20e6);
