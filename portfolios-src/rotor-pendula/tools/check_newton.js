#!/usr/bin/env node
// Does the Newton cap of the Radau IIA engine change the geared generator's results, and are they converged in the step?
// Runs the simulation page's own physics block (tools/physics_block.js) in Node at the 16 settings of data/L4_check_2000.json
// (three winds x three brakes at the ratio 492, and every other catalogue ratio at 8 m/s), three ways:
//   A. 2000 steps per turn, smoothing band 1e-3, Newton cap 12   (the Python check L4_check.py, for comparison)
//   B. the same with the cap raised to 40                         (does the cap matter?)
//   C. 4000 steps per turn, band 3e-4, cap 40                     (convergence in the step and the band)
// For each it counts the steps where Newton stopped at the cap without reaching 1e-12, in the settle and the measured turns,
// and the largest last correction there. The test text is patched in memory only; rotor_sim.html is not changed.
// Usage: node tools/check_newton.js     (writes data/newton_check.json)
const fs = require('fs');
const path = require('path');
const { physicsText } = require('./physics_block');

const BLOCK = physicsText();
function load(cap) {
  const t = BLOCK
    .replace('const tol = 1e-12, maxit = 12, eps = 1e-7;', `const tol = 1e-12, maxit = ${cap}, eps = 1e-7;`)
    .replace('if (err < tol) break;', '__S.last = err; if (err < tol) break;')
    .replace('return Math.min(it, maxit);', 'if (it > maxit) { if (t < __S.tSettle) __S.capSettle++; else { __S.capMeas++; __S.worst = Math.max(__S.worst, __S.last); } } __S.steps++; return Math.min(it, maxit);');
  if (t === BLOCK || !t.includes(`maxit = ${cap}`) || !t.includes('__S.capMeas++')) throw new Error('the physics block changed: patch points not found');
  return new Function('__S', t + '\nreturn { CONST, DEFAULTS, makeModel, simulate };');
}
const ref = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'L4_check_2000.json')));
const RUNS = [['A', 2000, 1e-3, 12], ['B', 2000, 1e-3, 40], ['C', 4000, 3e-4, 40]];
const out = [];
const T0 = Date.now();
for (const r of ref) {
  const row = { wind: r.wind, N: r.N, mult: r.mult, kind: r.kind, py: { load: r.P_load, paid: r.P_paid } };
  for (const [key, steps, band, cap] of RUNS) {
    const S = { tSettle: 0, capSettle: 0, capMeas: 0, worst: 0, last: 0, steps: 0 };
    const { simulate, DEFAULTS } = load(cap)(S);
    S.tSettle = 2 * Math.PI * DEFAULTS.settleGeared;           // the geared equation runs in the rotor angle
    const t1 = Date.now();
    const o = simulate({ wind: r.wind, gen: 'geared', N: r.N, ce: r.c_e, stepsGeared: steps, band, framesPerTurn: steps / 10 });   // frames only feed the playback record
    row[key] = { load: o.P_load, paid: o.P_paid, fric: o.P_fric, Theta: o.thetaAbsMax, capSettle: S.capSettle, capMeas: S.capMeas,
      steps: S.steps, worst: S.worst, s: (Date.now() - t1) / 1000 };
  }
  const rel = (a, b) => a / b - 1;
  row.A_vs_py = Math.max(Math.abs(rel(row.A.load, r.P_load)), Math.abs(rel(row.A.paid, r.P_paid)));
  row.B_vs_A = Math.max(Math.abs(rel(row.B.load, row.A.load)), Math.abs(rel(row.B.paid, row.A.paid)));
  row.C_vs_B = Math.max(Math.abs(rel(row.C.load, row.B.load)), Math.abs(rel(row.C.paid, row.B.paid)));
  out.push(row);
  const c = k => `${row[k].capSettle}+${row[k].capMeas}`;
  console.log(`${r.wind} m/s N ${String(r.N).padStart(4)} x${r.mult} ${r.kind.padEnd(5)}: load ${(row.B.load * 1e3).toFixed(4)} mW; ` +
    `capped settle+measured A ${c('A')}, B ${c('B')}, C ${c('C')}; A vs Python ${row.A_vs_py.toExponential(1)}, ` +
    `cap 40 vs 12 ${row.B_vs_A.toExponential(1)}, 4000 vs 2000 ${row.C_vs_B.toExponential(1)}  (${(row.A.s + row.B.s + row.C.s).toFixed(0)} s)`);
}
const mx = k => Math.max(...out.map(r => r[k]));
const sum = (k, f) => out.reduce((s, r) => s + r[k][f], 0);
let fails = 0;
const check = (ok, what) => { console.log((ok ? 'PASS ' : 'FAIL ') + what); if (!ok) fails++; };
check(mx('A_vs_py') < 1e-3, `run A reproduces the Python L4_check_2000.json (largest difference ${mx('A_vs_py').toExponential(1)})`);
check(sum('B', 'capMeas') === 0, `with a cap of 40 no step of the measured turns stops unconverged (${sum('B', 'capMeas')} do; ${sum('B', 'capSettle')} in the settle turns)`);
check(mx('B_vs_A') < 1e-3, `the cap of 12 changes the load and paid powers by less than 0.1 % (largest ${mx('B_vs_A').toExponential(1)})`);
check(mx('C_vs_B') < 1e-2, `4000 steps and a band of 3e-4 change them by less than 1 % (largest ${mx('C_vs_B').toExponential(1)})`);
fs.writeFileSync(path.join(__dirname, '..', 'data', 'newton_check.json'), JSON.stringify(out, null, 1));
console.log(`${fails ? fails + ' FAIL' : 'ALL PASS'}; ${((Date.now() - T0) / 1000).toFixed(0)} s`);
process.exit(fails ? 1 : 0);
