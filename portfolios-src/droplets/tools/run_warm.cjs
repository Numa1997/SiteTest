// The warm reference cloud (L4): SCE and GCE with the thesis kernel and the extended kernel.
//   node tools/run_warm.cjs [--json]   -> prints t50/t90 (first recorded minute) and writes data/warm.json with --json
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000);
let tab = null; try { tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json'))); } catch (e) { /* table not generated yet */ }
const hall = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'hall1980.json')));
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const kernels = {
  thesis: { speed: 'stokes', eff: 'one', coal: 'law' },
  thesisBeard: { speed: 'beard', eff: 'one', coal: 'law' },
  extended: { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab },
  extHall: { speed: 'beard', eff: 'hall', coal: 'law', hall },
  extHallSmall: { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab, hall, hallBelow: 30e-6 },
  extNearOne: { speed: 'beard', eff: 'table', coal: 'law', near: 'one', tab },
  extCoalOne: { speed: 'beard', eff: 'table', coal: 'one', near: 'clamp', tab },
  extTurb: { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab, eps: 1e-2 },
  extTurb400: { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab, eps: 4e-2 },
};
const s = +(process.env.BINS || 8), dt = +(process.env.DT || 1);
const grid = P.makeGrid(s, 4e-3);
const out = {};
const which = (process.env.ONLY || 'thesis,extended').split(',');
for (const name of which) {
  const ko = kernels[name], t0 = Date.now();
  const sce = P.sceRun(grid, A, ko, modes, { dt, tEnd: 3600, recordEvery: +(process.env.RECORD || 60) });
  const r5 = a => a.map(x => +x.toPrecision(6));
  const line = { t: sce.t, F40: r5(sce.F40), F100: r5(sce.F100), N100: r5(sce.N100), N1mm: r5(sce.N1mm), over: r5(sce.over), drift: sce.drift.map(x => +x.toExponential(2)) };
  const t50 = sce.tq(0.5), t90 = sce.tq(0.9), mi = Math.round(60 / +(process.env.RECORD || 60));
  let msg = `${name.padEnd(11)} SCE: t50/t90 = ${t50 / 60}/${t90 / 60} min, F40(0) = ${sce.F40[0].toFixed(4)}, F40(60) = ${sce.F40[60 * mi].toFixed(4)}, overflow(60) = ${sce.over[60 * mi].toExponential(2)}, max |mass drift| = ${Math.max(...sce.drift.map(Math.abs)).toExponential(1)}, fixes ${sce.fixes}, N(>=100um) at 10/20/30 min = ${[10, 20, 30].map(m => (sce.N100[m * mi]).toExponential(2)).join(', ')} m^-3`;
  if (name === 'thesis' || name === 'extended') {
    const gce = P.gceRun(grid, A, ko, modes, { dt, tEnd: 3600, recordEvery: +(process.env.RECORD || 60) });
    msg += `\n${''.padEnd(11)} GCE: t50/t90 = ${gce.tq(0.5) / 60}/${gce.tq(0.9) / 60} min`;
    line.gce = { t: gce.t, F40: r5(gce.F40) };
  }
  console.log(msg + `  [${((Date.now() - t0) / 1000).toFixed(1)} s]`);
  out[name] = line;
  out[name].snaps = {}; for (const k in sce.snaps) out[name].snaps[k] = sce.snaps[k].map(x => +x.toPrecision(5));
}
out.grid = { s, r: grid.r, x: grid.x };
if (process.argv.includes('--json')) fs.writeFileSync(path.join(__dirname, '..', 'data', 'warm.json'), JSON.stringify(out));
