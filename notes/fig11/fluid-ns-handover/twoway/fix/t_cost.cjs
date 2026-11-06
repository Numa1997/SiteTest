require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const w0 = 0; const w = new T.World({ dx: 0.025, U: +(process.env.U||0.3), machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: process.env.MED||'glycerol' }, s: [0, 0.08, 0.05, 0, 0, 0], nsub: 20 });
for (const k of (process.env.OPT || "").split(",").filter(Boolean)) w[k] = true; for (let k = 0; k < 20; k++) w.step(() => 0); w.prof = null; const t0 = Date.now(); for (let k = 0; k < 50; k++) w.step(() => 0);
console.log('ms/step', (Date.now() - t0) / 50, '[measure, sample+spread, advect, diffuse, pressure, machine+project]', w.prof.map(v => (v / 50).toFixed(2)).join(' '), 'its', w.its0, w.itsx, 'grid', w.nx, w.ny);
