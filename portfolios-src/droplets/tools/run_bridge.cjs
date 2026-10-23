// The SCE's tail for the Poisson bridge of L5: truncated modes (3 sigma_g), extended kernel, s = 16, records every 5 s for 20 min.
'use strict';
const P = require('../physics.cjs'), fs = require('fs'), path = require('path');
const A = P.air(283.15, 85000), tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const ko = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const out = {};
for (const s of [8, 16]) {
  const r = P.sceRun(P.makeGrid(s, 4e-3), A, ko, modes, { dt: 1, tEnd: 3600, recordEvery: 5, trunc: 3, snapAt: [] });
  out['s' + s] = { t: r.t, N100: r.N100.map(x => +x.toPrecision(6)), N1mm: r.N1mm.map(x => +x.toPrecision(6)), F40: r.F40.map(x => +x.toPrecision(6)), F100: r.F100.map(x => +x.toPrecision(6)) };
  const at = (a, v) => { for (let i = 0; i < a.length; i++) if (a[i] >= v) return r.t[i]; return null; };
  console.log(`s=${s}: median first 100 um drop: 1 m^3 ${at(r.N100, Math.LN2)} s, 1000 cm^3 ${at(r.N100, Math.LN2 * 1e3)} s, 100 cm^3 ${at(r.N100, Math.LN2 * 1e4)} s; first 1 mm drop in 1 m^3 ${at(r.N1mm, Math.LN2)} s; half the water >= 100 um at ${at(r.F100, 0.5)} s`);
}
fs.writeFileSync(path.join(__dirname, '..', 'data', 'bridge.json'), JSON.stringify(out));
