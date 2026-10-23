// L5 ensembles: exact stochastic runs of the thesis cloud (extended kernel, modes truncated at 3 sigma_g unless --full) in
// V = 1, 10, 100, 1000 cm^3. Writes data/stochastic.json with --json.
'use strict';
const P = require('../physics.cjs'), fs = require('fs'), path = require('path');
const A = P.air(283.15, 85000), tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const ko = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const trunc = process.argv.includes('--full') ? 0 : 3;
const plan = [[1, 200], [10, 100], [100, 100], [1000, 30]];
const out = { trunc, plan, V: {} };
for (const [V, n] of plan) {
  const t0 = Date.now(), runs = [];
  for (let k = 1; k <= n; k++) {
    const seed = 1000 * V + k, u = P.rng(seed), radii = P.drawModes(modes, V, u, trunc);
    const r = P.gillespieRun(V, radii, A, ko, { u, seed, tEnd: 3600, recordEvery: 60, firstR: [100e-6, 1e-3] });
    runs.push({ seed, F40: r.F40.map(x => +x.toFixed(5)), rmax: r.rmax.map(x => +(x * 1e6).toFixed(2)), t100: r.firsts[100e-6] ?? null,
      big100: r['bigMerges' + 100e-6] ?? null, t1mm: r.firsts[1e-3] ?? null, events: r.events, proposals: r.proposals, violations: r.violations });
  }
  out.V[V] = runs;
  const F = i => runs.reduce((a, q) => a + q.F40[i], 0) / n, Fse = i => Math.sqrt(runs.reduce((a, q) => a + (q.F40[i] - F(i)) ** 2, 0) / (n - 1) / n);
  const t100 = runs.map(q => q.t100).filter(x => x !== null).sort((a, b) => a - b);
  const viaBig = runs.filter(q => q.t100 !== null && q.big100 >= 1).length;
  console.log(`V=${V} cm^3, ${n} runs: F40 at 5/10/15 min = ${[5, 10, 15].map(i => F(i).toFixed(3) + '±' + Fse(i).toFixed(3)).join(', ')}; ` +
    `100 um drop in ${t100.length}/${n} runs, median ${t100.length ? t100[Math.floor(t100.length / 2)].toFixed(0) : '-'} s, via a merger with a partner >= 30 um in ${viaBig}/${t100.length}; ` +
    `violations ${runs.reduce((a, q) => a + q.violations, 0)}, acceptance ${(runs[0].events / runs[0].proposals).toFixed(2)} [${((Date.now() - t0) / 1000).toFixed(0)} s]`);
}
if (process.argv.includes('--json')) fs.writeFileSync(path.join(__dirname, '..', 'data', trunc ? 'stochastic.json' : 'stochastic_full.json'), JSON.stringify(out));
