// L8 (Gate 1 numbers): the energy and entropy scales of merging, and the channel rates at the start of the warm cloud.
//   node derive/L8_energy.cjs
// Surface energy of a drop 4 pi r^2 sigma = sigma (36 pi)^(1/3) rho_w^(-2/3) m^(2/3); a merger of r1, r2 releases
// sigma 4 pi (r1^2 + r2^2 - R^2), R^3 = r1^3 + r2^3, which viscosity turns into heat; entropy produced Delta E / T.
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000), T = A.T, sig = P.sigmaWater(T), kB = P.K_B;
const tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const ext = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const CW = 4192;          // J/(kg K), specific heat of liquid water at 10 C (IAPWS-95, rounded)
const NUW = 1.307e-6;     // m^2/s, kinematic viscosity of water at 10 C
const f = (x, d = 3) => x.toPrecision(d);
const area = r => 4 * Math.PI * r * r;
function release(r1, r2) { const R = Math.cbrt(r1 ** 3 + r2 ** 3); return sig * (area(r1) + area(r2) - area(R)); }
console.log(`air: T = ${T} K, rho_a = ${A.rho.toFixed(4)} kg/m3, nu = ${A.nu.toExponential(3)} m2/s; sigma(10 C) = ${sig.toFixed(5)} N/m; kT = ${f(kB * T)} J`);
console.log('\npair (um)    released (J)   / small drop surface   heat dT (K)   entropy (k_B)   collision KE (J)   released/KE   We');
for (const [R, r] of [[40, 8], [8, 8], [10, 8], [40, 40], [60, 50], [20, 18], [100, 8], [100, 40], [1000, 100]]) {
  const a = R * 1e-6, b = r * 1e-6, dE = release(a, b), m = P.massOf(a) + P.massOf(b);
  const va = P.vBeard(a, A), vb = P.vBeard(b, A), mu = P.massOf(a) * P.massOf(b) / m, KE = 0.5 * mu * (va - vb) ** 2;
  const We = P.weber(a, b, Math.abs(va - vb), sig);
  console.log(`${String(R).padStart(5)}/${String(r).padEnd(5)}  ${f(dE).padStart(10)}     ${f(dE / (sig * area(b))).padStart(8)}             ${f(dE / (m * CW)).padStart(9)}     ${f(dE / T / kB).padStart(9)}       ${KE > 0 ? f(KE).padStart(9) : '        0'}        ${KE > 0 ? f(dE / KE).padStart(7) : '    inf'}    ${We > 0 ? We.toExponential(2) : 0}`);
}
const x = 0.5; console.log(`\nlargest share of the surface destroyed by one merger (equal drops): 1 - 2^(-1/3) = ${f(1 - Math.pow(2, -1 / 3), 4)}`);
console.log(`viscous damping time of the merged drop's wobble (Lamb, l = 2: r^2/(5 nu_w)): 40 um ${f(1e3 * (40e-6) ** 2 / (5 * NUW))} ms, 100 um ${f(1e3 * (100e-6) ** 2 / (5 * NUW))} ms`);
// the warm cloud at the start, on the grid of chapter 5 (s = 8)
const grid = P.makeGrid(8, 4e-3), n = grid.n;
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const Nd = P.lognormalBins(grid, [modes[0]]), Nc = P.lognormalBins(grid, [modes[1]]);
let Ed = 0, Ec = 0, Pg = 0, M = 0;
const gs = r => P.G0 * (1 - A.rho / P.RHO_W);
for (let k = 0; k < n; k++) {
  Ed += sig * Nd[k] * area(grid.r[k]); Ec += sig * Nc[k] * area(grid.r[k]);
  Pg += (Nd[k] + Nc[k]) * grid.x[k] * gs() * P.vBeard(grid.r[k], A); M += (Nd[k] + Nc[k]) * grid.x[k];
}
console.log(`\nwarm cloud at t = 0: water ${f(M * 1e3, 4)} g/m3; surface energy ${f(Ed + Ec, 4)} J/m3 (droplets ${f(Ed / (Ed + Ec) * 100, 3)} %, collectors ${f(Ec / (Ed + Ec) * 100, 3)} %)`);
console.log(`gravity's work dissipated by drag, g* sum N m v: ${f(Pg)} W/m3; turbulence rho_a eps: ${f(A.rho * 1e-3)} / ${f(A.rho * 1e-2)} / ${f(A.rho * 1e-1)} W/m3 at eps = 1e-3 / 1e-2 / 1e-1 m2/s3`);
// channel rates at t = 0: pairs (droplet, droplet), (collector, droplet), (collector, collector); number of mergers and energy released
const K = P.kernelMatrix(grid, A, ext);
const ch = { dd: [0, 0, 0], cd: [0, 0, 0], cc: [0, 0, 0] };
for (let i = 0; i < n; i++) for (let j = i; j < n; j++) {
  const w = i === j ? 0.5 : 1, kij = K[i * n + j];
  const dE = sig * (area(grid.r[i]) + area(grid.r[j]) - area(P.radiusOf(grid.x[i] + grid.x[j])));
  const add = (key, rate) => { ch[key][0] += rate; ch[key][1] += rate * dE; ch[key][2] += rate * grid.x[i]; };
  // number of i-j pairs per m^3 split by mode of each partner
  add('dd', w * kij * Nd[i] * Nd[j]);
  add('cd', (i === j ? 1 : 1) * kij * (Nd[i] * Nc[j] + (i === j ? 0 : Nc[i] * Nd[j])));
  add('cc', w * kij * Nc[i] * Nc[j]);
}
const tot = ch.dd[0] + ch.cd[0] + ch.cc[0], totE = ch.dd[1] + ch.cd[1] + ch.cc[1];
console.log('\nextended kernel at t = 0       mergers (cm^-3 s^-1)   share    energy released (W/m3)   share');
for (const k of ['dd', 'cd', 'cc']) console.log(`  ${({ dd: 'droplet-droplet  ', cd: 'collector-droplet', cc: 'collector-collector' })[k].padEnd(20)}          ${f(ch[k][0] * 1e-6).padStart(9)}        ${f(100 * ch[k][0] / tot).padStart(6)} %      ${f(ch[k][1]).padStart(9)}             ${f(100 * ch[k][1] / totE).padStart(6)} %`);
console.log(`  surface-energy release / gravity's dissipation = ${f(totE / Pg)}`);
const Ntot = 301e6, pd = 300 / 301, pc = 1 / 301;
console.log(`\nenergy-only Monte Carlo (every pair equally likely): droplet-droplet ${f(100 * pd * pd)} %, collector-droplet ${f(100 * 2 * pd * pc)} %, collector-collector ${f(100 * pc * pc)} % of the first mergers`);
console.log(`Metropolis acceptance of the gentlest merger listed (largest radius 1000 um aside): exp(-dE/kT) with dE/kT = -${f(release(8e-6, 8e-6) / (kB * T))}: accepted; of its reverse: exp(-${f(release(8e-6, 8e-6) / (kB * T))}) = 0`);
