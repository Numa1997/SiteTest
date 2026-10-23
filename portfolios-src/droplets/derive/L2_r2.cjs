// L2, round 2 of Gate 1: numbers that answer skeptic-G1-L2-r1 (objections 2, 6, 7, 13; prediction 3).
//   node derive/L2_r2.cjs
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000);
const tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const hall = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'hall1980.json')));

// objection 2: sensitivity of E(40, 8) to Langmuir's crossover Reynolds number (60 in his eq. 23)
const pe = P.pairEfficiency(40e-6, 8e-6, A);
for (const Rc of [60, 20, 6, 2]) console.log(`crossover ${String(Rc).padStart(2)}: E(40, 8) = ${((pe.ES + pe.EP * pe.Re / Rc) / (1 + pe.Re / Rc)).toFixed(3)}`);
// along the growth path r = 8 um: ours against Hall
for (const R of [40, 50, 60, 80, 100, 150, 200, 300]) {
  const e = P.pairEfficiency(R * 1e-6, 8e-6, A).E, h = P.hallE(hall, R * 1e-6, 8 / R);
  console.log(`R = ${R} um, r = 8 um: ours ${e.toFixed(3)}, Hall ${h.toFixed(3)}, ratio ${(h / e).toFixed(2)}`);
}
// objection 7: hovering criterion. Inertialess partner on the axis reaches the surface only if its settling S is below the
// air's approach speed at contact, I(p) = 1 - 3/(2(1+p)) + 1/(2(1+p)^3) in creeping flow.
for (const R of [20, 30, 40]) for (const r of [6, 8, 10, 12]) {
  const p = r / R, I = 1 - 1.5 / (1 + p) + 0.5 / (1 + p) ** 3, S = P.vBeard(r * 1e-6, A) / P.vBeard(R * 1e-6, A);
  console.log(`R = ${R}, r = ${r}: p = ${p.toFixed(2)}, S = ${S.toFixed(3)}, I(p) = ${I.toFixed(3)} -> ${S > I ? 'hovers (inertialess limit)' : 'can reach'}`);
}
// objection 6: the share of the kernel carried by near-equal pairs (p > 0.9) at t = 0 and after 10 min (extended SCE)
const grid = P.makeGrid(8, 4e-3), modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const ko = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const run = P.sceRun(grid, A, ko, modes, { dt: 1, tEnd: 600, recordEvery: 600, snapAt: [0, 600] });
for (const t of [0, 600]) {
  const N = run.snaps[t]; let all = 0, near = 0;
  for (let i = 0; i < grid.n; i++) for (let j = i + 1; j < grid.n; j++) {
    const m = P.kernel(grid.r[i], grid.r[j], A, ko) * N[i] * N[j] * grid.x[i];   // mass moved upward per second by pair (i, j)
    all += m; if (grid.r[i] / grid.r[j] > 0.9) near += m;
  }
  console.log(`t = ${t} s: share of the mass transfer rate in pairs with r/R > 0.9: ${(near / all * 100).toFixed(2)} %`);
}
// prediction 3: Hall's values for collectors below 30 um
const interp = (r, q) => { for (let i = 1; i < r.F40.length; i++) if (r.F40[i] >= q) return (r.t[i - 1] + (r.t[i] - r.t[i - 1]) * (q - r.F40[i - 1]) / (r.F40[i] - r.F40[i - 1])) / 60; };
for (const [name, k] of [['own table', ko], ['own table, Hall below 30 um', Object.assign({}, ko, { hall, hallBelow: 30e-6 })]]) {
  const r = P.sceRun(grid, A, k, modes, { dt: 1, tEnd: 1500, recordEvery: 5, snapAt: [] });
  console.log(`${name}: t50/t90 = ${interp(r, 0.5).toFixed(3)}/${interp(r, 0.9).toFixed(3)} min`);
}
