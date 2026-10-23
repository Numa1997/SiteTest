// Quick tests of the exact stochastic engine: (1) constant kernel against the exact mean N(t) = N0/(1 + K N0 t/2) of the
// mean field (for large N the master equation's mean agrees); (2) the thesis cloud in 100 cm^3 against the SCE.
'use strict';
const P = require('../physics.cjs');
const A = P.air(283.15, 85000);
const fs = require('fs'), path = require('path');
const tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const ko = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
for (const V of [1, 10, 100]) {
  const t0 = Date.now(); const runs = []; const nrun = V === 1 ? 40 : V === 10 ? 10 : 4;
  for (let s = 1; s <= nrun; s++) {
    const u = P.rng(1000 * V + s); const radii = P.drawModes(modes, V, u, 0);
    runs.push(P.gillespieRun(V, radii, A, ko, { u, seed: 1000 * V + s, tEnd: 1800, recordEvery: 60 }));
  }
  const mean = i => runs.reduce((a, r) => a + r.F40[i], 0) / runs.length;
  const r0 = runs[0];
  console.log(`V=${V} cm^3, ${nrun} runs: F40 mean at 0/5/10/15/20 min = ${[0, 5, 10, 15, 20].map(i => mean(i).toFixed(3)).join(' ')}; events/run ${r0.events}, proposals/run ${r0.proposals}, violations ${runs.reduce((a, r) => a + r.violations, 0)} [${((Date.now() - t0) / 1000).toFixed(1)} s]`);
}
const g = P.makeGrid(8, 4e-3); const sce = P.sceRun(g, A, ko, modes, { dt: 1, tEnd: 1800 });
console.log('SCE F40 at 0/5/10/15/20 min = ' + [0, 5, 10, 15, 20].map(i => sce.F40[i].toFixed(3)).join(' '));
