// The windowed measure() against a full pass, after the cart has moved: the same weights to the last bit, the same sign of the distance everywhere, the same distance near the cart.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const mk = () => new T.World({ dx: 0.025, machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' } });
const a = mk(), b = mk(); b.fullMeasure = true; let bad = 0, near = 0, ok = true;
for (const x of [0, 0.013, 0.05, 0.3, -0.4, -0.41, 0.9]) { a.s[0] = b.s[0] = x; a.measure(); b.measure();
  for (const k of ['wu', 'wv', 'su', 'sv', 'wx', 'wy']) if (!a[k].every((v, i) => v === b[k][i])) { ok = false; console.log('differs', k, x); }
  for (const k of ['phU', 'phV']) a[k].forEach((v, i) => { const r = b[k][i]; if ((v < 0) !== (r < 0)) bad++; if (Math.abs(r) < 0.06 && v !== r) near++; }); }
const tm = (w, n = 200) => { const t = process.hrtime.bigint(); for (let i = 0; i < n; i++) { w.s[0] += 1e-4; w.measure(); } return (Number(process.hrtime.bigint() - t) / 1e6 / n).toFixed(3); };
console.log('weights identical', ok, '| sign differences', bad, '| distance differences within 6 cm of the cart', near, '| ms windowed', tm(a), 'full', tm(b));
