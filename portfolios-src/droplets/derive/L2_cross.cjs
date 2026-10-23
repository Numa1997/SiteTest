// L2, round 3: how far observable 1 moves with Langmuir's crossover Reynolds number (60 in his eq. 23), and with E = 1 for small
// collectors (a check of what droplet-droplet pairs carry).  node derive/L2_cross.cjs   (about 3 minutes; table cached in data/)
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000);
const f = path.join(__dirname, '..', 'data', 'etab_split.json');
let sp;
if (fs.existsSync(f)) sp = JSON.parse(fs.readFileSync(f));
else { sp = P.makeTable(A, { split: true }); fs.writeFileSync(f, JSON.stringify(sp)); }
const grid = P.makeGrid(8, 4e-3), modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const interp = (r, q) => { for (let i = 1; i < r.F40.length; i++) if (r.F40[i] >= q) return (r.t[i - 1] + (r.t[i] - r.t[i - 1]) * (q - r.F40[i - 1]) / (r.F40[i] - r.F40[i - 1])) / 60; };
const run = ko => P.sceRun(grid, A, ko, modes, { dt: 1, tEnd: 1800, recordEvery: 5, snapAt: [] });
for (const c of [60, 20, 6, 2]) {
  const tab = Object.assign({}, sp, { E: sp.ES.map((es, i) => (es + sp.EP[i] * sp.Re[i] / c) / (1 + sp.Re[i] / c)) });
  const r = run({ speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab });
  console.log(`crossover ${String(c).padStart(2)}: E(40, 8) = ${P.tableE(tab, 40e-6, 0.2, 'clamp').toFixed(3)}, SCE t50/t90 = ${interp(r, 0.5).toFixed(2)}/${interp(r, 0.9).toFixed(2)} min`);
}
// E = 1 for collectors below 30 um (all their partners), the rest from the table at crossover 60
const tab60 = Object.assign({}, sp, { E: sp.ES.map((es, i) => (es + sp.EP[i] * sp.Re[i] / 60) / (1 + sp.Re[i] / 60)) });
const lnR30 = Math.log(30e-6);
const tabOne = Object.assign({}, tab60, { E: tab60.E.map((e, i) => sp.lnR[Math.floor(i / sp.lnp.length)] < lnR30 ? 1 : e) });
const r1 = run({ speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab: tabOne });
console.log(`E = 1 for collectors below 30 um: SCE t50/t90 = ${interp(r1, 0.5).toFixed(2)}/${interp(r1, 0.9).toFixed(2)} min`);
