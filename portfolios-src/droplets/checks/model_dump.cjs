// Prints, as JSON, the numbers that checks/check_physics.py compares with its own independent Python versions.
// Everything here comes from the model itself (physics.cjs); nothing is recomputed in this file.
//   node checks/model_dump.cjs > dump.json
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000);
const tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const ko = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const out = { air: A };

// fall speeds
out.radii = [5e-6, 8e-6, 20e-6, 40e-6, 60e-6, 100e-6, 300e-6, 600e-6, 1e-3, 2e-3];
out.vBeard = out.radii.map(r => P.vBeard(r, A));
out.vStokes = out.radii.map(r => P.vStokes(r, A));

// collision efficiency of 40 um on 8 um, and the critical Stokes numbers
out.pair = P.pairEfficiency(40e-6, 8e-6, A);
out.stc = { potential: P.criticalStokes('potential', 100), stokes: P.criticalStokes('stokes', 100) };

// Golovin's exact solution at a few masses
const b = 1.5, L = 1e-3, mbar = P.massOf(10e-6), N0 = L / mbar;
out.golovin = { b, L, mbar, N0, t: 3600, m: [0.1, 1, 10, 100, 1000, 1e4].map(u => u * mbar) };
out.golovin.n = out.golovin.m.map(m => P.golovinDensity(m, 3600, b, N0, mbar));

// the extended kernel on the s = 8 grid, the initial spectrum, and the model's own SCE result
const grid = P.makeGrid(8, 4e-3);
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
out.grid = { s: 8, x: grid.x, r: grid.r };
out.K = Array.from(P.kernelMatrix(grid, A, ko));
out.N0 = Array.from(P.lognormalBins(grid, modes));
const sce = P.sceRun(grid, A, ko, modes, { dt: 1, tEnd: 1200, recordEvery: 5, K: Float64Array.from(out.K) });
out.sce = { t: sce.t, F40: sce.F40 };

// the stochastic engine on a problem with an exact answer: one 40 um collector and n identical 8 um droplets. Identical
// droplets fall at the same speed and never meet, so the only events are captures, a pure death chain.
const n = 20, V = 0.05, T = 60, runs = +(process.env.RUNS || 4000);
const chain = { n, V, T, R0: 40e-6, r: 8e-6, runs, rates: [], k: [] };
for (let k = 0; k < n; k++) {
  const Rk = Math.cbrt(40e-6 ** 3 + k * 8e-6 ** 3);
  chain.rates.push((n - k) * P.kernel(Rk, 8e-6, A, ko) / (V * 1e-6));
}
for (let s = 1; s <= runs; s++) {
  const radii = [40e-6].concat(Array(n).fill(8e-6));
  const res = P.gillespieRun(V, radii, A, ko, { seed: s, tEnd: T, recordEvery: T, firstR: [] });
  const rmax = res.rmax[res.rmax.length - 1];
  chain.k.push(Math.round((rmax ** 3 - 40e-6 ** 3) / 8e-6 ** 3));
  if (res.violations) chain.violations = (chain.violations || 0) + res.violations;
}
out.chain = chain;
process.stdout.write(JSON.stringify(out));
