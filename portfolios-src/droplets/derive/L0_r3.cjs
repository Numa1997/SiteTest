// L0, round 3 of Gate 1: the numbers that answer skeptic-G1-L0-r2 (N1, N5, N10, N11).
//   node derive/L0_r3.cjs
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000), RW = 1000;
const tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const hall = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'hall1980.json')));
const r = 8e-6, R0 = 40e-6, Nc0 = 1e6, Wd = 300e6 * P.massOf(r);   // droplet water, kg/m^3

// one collector: dR/dt = E pi (R + r)^2 [v(R) - v(r)] W / (4 pi R^2 rho_w), W fixed (open) or W(R) (closed box, N_c collectors)
function grow(law, eff, W0, Nc, Rstop, tMax) {
  const v = a => law === 'stokes' ? P.vStokes(a, A) : P.vBeard(a, A);
  const E = R => eff === 'one' ? 1 : eff === 'hall' ? P.hallE(hall, R, r / R) : P.tableE(tab, R, r / R, 'clamp');
  const M0 = P.massOf(R0);
  const W = R => Nc ? W0 - Nc * (P.massOf(R) - M0) : W0;
  const f = R => Math.max(0, E(R) * Math.PI * (R + r) ** 2 * (v(R) - v(r)) * W(R) / (4 * Math.PI * R * R * RW));
  let R = R0, t = 0, dist = 0, sweep = 0; const h = 0.05, out = { hit: {} };
  while (t < tMax) {
    const k1 = f(R), k2 = f(R + h / 2 * k1), k3 = f(R + h / 2 * k2), k4 = f(R + h * k3);
    const Rn = R + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4);
    dist += h * v(R + 0.5 * (Rn - R));
    sweep += h * (Nc || 0) * E(R) * Math.PI * (R + r) ** 2 * (v(R) - v(r));
    for (const q of Rstop) if (out.hit[q] === undefined && Rn >= q) out.hit[q] = t + h * (q - R) / (Rn - R);
    const Fc = Nc ? Nc * P.massOf(Rn) / (Nc * M0 + W0) : 0;
    if (Nc && out.t50 === undefined && Fc >= 0.5) out.t50 = t + h;
    if (Nc && out.t90 === undefined && Fc >= 0.9) { out.t90 = t + h; out.dist90 = dist; out.sweep90 = sweep; }
    R = Rn; t += h;
    if (!Nc && R >= Rstop[Rstop.length - 1]) break;
  }
  out.R = R; return out;
}
const mn = s => s === undefined ? '  -  ' : (s / 60).toFixed(2);

console.log('N5. L0 observables with each correction (min): open 40->60, open 40->100 | closed box t50, t90');
for (const [law, eff, name] of [['stokes', 'one', 'L0 (Stokes, E = 1)'], ['beard', 'one', 'Beard, E = 1'], ['stokes', 'table', 'Stokes, own E table'],
  ['beard', 'table', 'Beard and own E table'], ['beard', 'hall', 'Beard and Hall (1980) E']]) {
  const o = grow(law, eff, Wd, 0, [60e-6, 100e-6], 7200);
  const c = grow(law, eff, Wd, Nc0, [], 7200);
  console.log(`  ${name.padEnd(24)} ${mn(o.hit[60e-6])}  ${mn(o.hit[100e-6])}  |  ${mn(c.t50)}  ${mn(c.t90)}`);
}

console.log('N10. closed box (Stokes, E = 1): fall distance by t90 and the number of times the air is swept');
const c0 = grow('stokes', 'one', Wd, Nc0, [], 3600);
console.log(`  t90 = ${mn(c0.t90)} min, distance ${c0.dist90.toFixed(1)} m, sweeps ${c0.sweep90.toFixed(2)}`);

console.log('N11. closed box against the open cloud (Stokes, E = 1, finite r), time 40 -> 100 um, same droplet water');
const open = grow('stokes', 'one', Wd, 0, [100e-6], 7200).hit[100e-6];
for (const Nc of [0.15e6, 0.05e6, 0.015e6, 0.005e6]) {
  const c = grow('stokes', 'one', Wd, Nc, [100e-6], 20000).hit[100e-6];
  console.log(`  N_c = ${(Nc / 1e6).toFixed(3)} cm^-3: ${mn(c)} min against ${mn(open)} min, ${c ? '+' + ((c / open - 1) * 100).toFixed(1) + ' %' : 'never'}`);
}

console.log('N1. the full SCE with the L0 kernel on every pair (s = 8, dt = 1 s, grid to 4 mm, lognormal modes)');
const grid = P.makeGrid(8, 4e-3), modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
for (const [name, ko] of [['Stokes, E = 1, coalescence 1', { speed: 'stokes', eff: 'one', coal: 'one' }],
  ['Stokes, E = 1, coalescence law (the thesis kernel)', { speed: 'stokes', eff: 'one', coal: 'law' }]]) {
  const s = P.sceRun(grid, A, ko, modes, { dt: 1, tEnd: 600, recordEvery: 5 });
  const at = q => { for (let i = 0; i < s.F40.length; i++) if (s.F40[i] + s.over[i] >= q) { const j = i - 1; return s.t[j] + 5 * (q - s.F40[j] - s.over[j]) / (s.F40[i] + s.over[i] - s.F40[j] - s.over[j]); } return null; };
  const i5 = s.t.indexOf(300), i10 = s.t.indexOf(600);
  const k1mm = grid.r.findIndex(x => x >= 1e-3);
  let m1 = 0; for (let k = k1mm; k < grid.n; k++) m1 += s.N[k] * grid.x[k];
  console.log(`  ${name}: t50/t90 = ${(at(0.5) / 60).toFixed(2)}/${(at(0.9) / 60).toFixed(2)} min (counting mass that left the grid); ` +
    `left the 4 mm grid by 5 min ${(s.over[i5] * 100).toFixed(1)} %, by 10 min ${(s.over[i10] * 100).toFixed(1)} %; ` +
    `in drops >= 1 mm or off the grid at 10 min ${((m1 / s.M0 + s.over[i10]) * 100).toFixed(1)} %; mass drift ${Math.max(...s.drift.map(Math.abs)).toExponential(1)}`);
}
