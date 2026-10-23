// Does the SCE's far tail converge with grid resolution? Time at which V N(r >= 100 um) = ln 2 (the median first-drop time of a
// Poisson count), for V = 1 m^3, 1 L, 100 cm^3, truncated modes (3 sigma), extended kernel, s = 8, 16, 32.
'use strict';
const P = require('../physics.cjs'), fs = require('fs'), path = require('path');
const A = P.air(283.15, 85000), tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const ko = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
for (const s of (process.argv[2] || '8,16,32').split(',').map(Number)) {
  const t0 = Date.now(), g = P.makeGrid(s, 4e-3);
  const r = P.sceRun(g, A, ko, modes, { dt: s >= 32 ? 0.5 : 1, tEnd: 900, recordEvery: 5, trunc: 3 });
  const at = v => { for (let i = 0; i < r.N100.length; i++) if (r.N100[i] >= v) return r.t[i]; return null; };
  console.log(`s=${s}: first-drop median for 1 m^3 at ${at(Math.LN2)} s, 1 L at ${at(Math.LN2 * 1e3)} s, 100 cm^3 at ${at(Math.LN2 * 1e4)} s; N100 at 60/120/300 s = ${[12, 24, 60].map(i => r.N100[i].toExponential(2)).join(', ')} m^-3  [${((Date.now() - t0) / 1000).toFixed(0)} s]`);
}
