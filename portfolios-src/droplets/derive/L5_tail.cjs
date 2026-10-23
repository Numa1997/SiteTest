// L5, round 2: is the collection equation's tail converged for the Poisson bridge? Medians of the first 100 um drop
// from (6.1) at s = 8, 16, 32 bins per doubling (truncated modes, extended kernel, dt = 1 s).   node derive/L5_tail.cjs
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000), tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const ko = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
for (const s of [8, 16, 32]) {
  const t0 = Date.now();
  const r = P.sceRun(P.makeGrid(s, 4e-3), A, ko, modes, { dt: 1, tEnd: 420, recordEvery: 1, trunc: 3, snapAt: [] });
  const nmax = []; r.N100.reduce((m, N, i) => (nmax[i] = Math.max(m, N)), 0);
  const at = V => { for (let i = 0; i < nmax.length; i++) if (V * nmax[i] >= Math.LN2) return r.t[i]; return null; };
  console.log(`s = ${s}: median first 100 um drop from (6.1): 1 m^3 ${at(1)} s, 1000 cm^3 ${at(1e-3)} s, 100 cm^3 ${at(1e-4)} s  [${((Date.now() - t0) / 1000).toFixed(0)} s]`);
}
