// L4, round 2: grid and time-step convergence of observable 1 (extended kernel), and the constant-kernel identity.
//   node derive/L4_conv.cjs
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000), tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const ko = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const interp = (r, q) => { for (let i = 1; i < r.F40.length; i++) if (r.F40[i] >= q) return (r.t[i - 1] + (r.t[i] - r.t[i - 1]) * (q - r.F40[i - 1]) / (r.F40[i] - r.F40[i - 1])) / 60; };
for (const [s, dt] of [[4, 1], [8, 1], [16, 1], [8, 0.5], [8, 0.25]]) {
  const r = P.sceRun(P.makeGrid(s, 4e-3), A, ko, modes, { dt, tEnd: 1200, recordEvery: 5, snapAt: [] });
  console.log(`s = ${String(s).padStart(2)}, dt = ${dt} s: t50/t90 = ${interp(r, 0.5).toFixed(3)}/${interp(r, 0.9).toFixed(3)} min, limiter fixes ${r.fixes}`);
}
// constant kernel K0, monodisperse start: N(t) = N0 / (1 + K0 N0 t / 2)
const g = P.makeGrid(8, 4e-3), n = g.n, K0 = 1e-12, N0 = 1e9, K = new Float64Array(n * n).fill(K0);
const Nb = new Float64Array(n); Nb[P.makeGrid(8, 4e-3).r.findIndex(r => r >= 10e-6)] = N0;
const t = 2 / (K0 * N0) * 3;      // N/N0 = 1/4
const r = P.sceRun(g, null, null, null, { K, N0: Nb, dt: 1, tEnd: t, recordEvery: t, snapAt: [] });
const Nend = r.N.reduce((a, v) => a + v, 0) + r.overflow.N;
console.log(`constant kernel: N/N0 = ${(Nend / N0).toFixed(5)} against exact ${(1 / (1 + K0 * N0 * t / 2)).toFixed(5)} after ${t} s`);
