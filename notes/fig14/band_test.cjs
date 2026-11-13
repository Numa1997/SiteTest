const fs = require('fs'); const s = fs.readFileSync(__dirname + '/../../public/scripts/fig14-sheet-worker.js', 'utf8');
const i = s.indexOf('function bandMatrix('), j = s.indexOf('var PKM = null;');
eval(s.slice(i, j) + '; globalThis.bandMatrix = bandMatrix;');
// a wave that fits the 64 a box: k = 2 pi n / 64; the largest stored energy E = 4.5 has k0 = 3 -> n = 30.6; test n = 31 and a packet
const N = 128, d = 0.5, xs = new Float64Array(289); for (let a = 0; a < 289; a++) xs[a] = -24 + a / 6 + 32;
const M = bandMatrix(N, d, xs);
let worst = 0;
for (const n of [5, 17, 31, 45, 60]) { const k = 2 * Math.PI * n / 64; let e = 0; for (let a = 0; a < 289; a++) { let v = 0; for (let q = 0; q < N; q++) v += M[a * N + q] * Math.cos(k * (q * d) + 0.3); e = Math.max(e, Math.abs(v - Math.cos(k * xs[a] + 0.3))); } console.log('plane wave n =', n, 'lambda =', (64 / n).toFixed(2), 'a: largest error', e.toExponential(1)); worst = Math.max(worst, e); }
// a Gaussian packet exp(-(x-x0)^2/4s^2) cos(k0 x), E = 4.5, k0 = 3 (not on the box's wave numbers)
{ const f = (x) => Math.exp(-((x - 30) ** 2) / 36) * Math.cos(3 * x); let e = 0; for (let a = 0; a < 289; a++) { let v = 0; for (let q = 0; q < N; q++) v += M[a * N + q] * f(q * d); e = Math.max(e, Math.abs(v - f(xs[a]))); } console.log('Gaussian packet, k0 = 3, sigma0 = 3: largest error', e.toExponential(1)); }
// stored points returned exactly
{ let e = 0; for (let a = 0; a < 289; a += 3) { const q0 = Math.round(xs[a] / d); for (let q = 0; q < N; q++) e = Math.max(e, Math.abs(M[a * N + q] - (q === q0 ? 1 : 0))); } console.log('at stored points: largest departure of the weights from (1, 0, 0, ...)', e.toExponential(1)); }
