// L7: ice-production rates at t = 0 in the thesis's cold cloud (-10 C, 600 hPa): the same two lognormal modes, split bin by bin
// into liquid and ice spheres with the thesis's supercooled liquid fraction F(T). Collision rates from the extended kernel
// (Beard speeds with each phase's density, trajectory efficiencies computed for each pair, E_coal = 1 for pairs with ice).
'use strict';
const P = require('../physics.cjs'), fs = require('fs'), path = require('path');
const T = 263.15, Tc = T - 273.15, A = P.air(T, 60000);
const a = [98.9, 4.291, -0.318, -0.02623, -6.398e-4, -5.279e-6];
const Fliq = Math.min(1, Math.max(0, a.reduce((s, c, j) => s + c * Math.pow(Tc, j), 0) / 100));
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const g = P.makeGrid(4, 4e-3);
const Nw = P.lognormalBins(g, modes, 1000), Ni = P.lognormalBins(g, modes, 900);
const parts = [];
for (let k = 0; k < g.n; k++) {
  if (Nw[k] * Fliq > 1e-6 * 300e6 * 1e-6 || Nw[k] > 1) parts.push({ ph: 'w', r: P.radiusOf(g.x[k], 1000), m: g.x[k], n: Nw[k] * Fliq, rho: 1000 });
  if (Ni[k] * (1 - Fliq) > 1) parts.push({ ph: 'i', r: P.radiusOf(g.x[k], 900), m: g.x[k], n: Ni[k] * (1 - Fliq), rho: 900 });
}
const use = parts.filter(q => q.n > 1);           // at least 1 per m^3
for (const q of use) q.v = P.vBeard(q.r, A, q.rho);
const ntot = ph => use.filter(q => q.ph === ph).reduce((s, q) => s + q.n, 0);
console.log(`F_liq(${Tc} C) = ${(Fliq * 100).toFixed(2)} %; liquid ${(ntot('w') / 1e6).toFixed(1)} cm^-3, ice ${(ntot('i') / 1e6).toFixed(1)} cm^-3`);
const mf = P.massOf(5e-6, 900);
// Phillips et al. (2017) breakup law, graupel-graupel coefficients (the nearest category to dense ice spheres), as printed in
// Sotiropoulou et al. (2021, Appendix B, read): a0 = 3.78e4 (1 + 0.0079 / D^1.5), D (m) the diameter of the smaller particle, fitted for
// 0.5 mm < D < 5 mm and to be clamped to that range outside it; A = a0 [1/3 + max(2/3 - |T - 258|/9, 0)]; gamma = 0.3;
// C = 6.3e6 psi with psi = 3.5e-3 (sublimation correction after Vardiman 1978) or 1; at most 100 fragments per collision.
const fT = 1 / 3 + Math.max(2 / 3 - Math.abs(T - 258) / 9, 0);
const PH = { A: D => 3.78e4 * (1 + 0.0079 / Math.pow(D, 1.5)) * fT, g: 0.3, Dclamp: D => Math.min(5e-3, Math.max(5e-4, D)) };
let rime = 0, rime25 = 0, rime25big = 0, ii = 0, fragHi = 0, fragLo = 0, fragTrueD = 0, oldRule = 0; const kev = [];
for (let i = 0; i < use.length; i++) for (let j = i; j < use.length; j++) {
  const p = use[i], q = use[j];
  if (p.ph === 'w' && q.ph === 'w') continue;
  const dv = Math.abs(p.v - q.v); if (dv === 0) continue;
  const big = p.v >= q.v ? p : q, sm = big === p ? q : p;
  const E = P.pairEfficiency(big.r, sm.r, A, big.rho, sm.rho).E;
  const K = Math.PI * Math.pow(p.r + q.r, 2) * dv * E;
  const rate = K * p.n * q.n * (i === j ? 0.5 : 1);           // events per m^3 per s
  if (p.ph === 'i' && q.ph === 'i') {
    ii += rate;
    const K0 = 0.5 * p.m * q.m / (p.m + q.m) * dv * dv, D = 2 * Math.min(p.r, q.r), alpha = Math.PI * D * D;
    const N = (C, Dl) => Math.min(100, alpha * PH.A(Dl) * (1 - Math.exp(-Math.pow(C * K0 / (alpha * PH.A(Dl)), PH.g))));
    fragHi += rate * N(6.3e6, PH.Dclamp(D)); fragLo += rate * N(6.3e6 * 3.5e-3, PH.Dclamp(D)); fragTrueD += rate * N(6.3e6, D);
    kev.push([K0, rate]);
    oldRule += rate * 0.001 * Math.max(p.m, q.m) / mf;
  } else {
    rime += rate; const liq = p.ph === 'w' ? p : q, ice = liq === p ? q : p; if (liq.r >= 25e-6) { rime25 += rate; if (liq.r > ice.r) rime25big += rate; }
  }
}
const perMin = x => (x * 60 / 1e6);                          // per cm^3 per minute
kev.sort((x, y) => x[0] - y[0]); const tot = kev.reduce((a, e) => a + e[1], 0);
const kq = q => { let c = 0; for (const e of kev) { c += e[1]; if (c >= q * tot) return e[0]; } return kev[kev.length - 1][0]; };
console.log(`F_liq = ${(Fliq * 100).toFixed(2)} %, temperature factor of A ${fT.toFixed(4)}, A at D = 0.5 mm ${PH.A(5e-4).toExponential(3)} m^-2`);
console.log(`riming events ${perMin(rime).toFixed(3)} cm^-3 min^-1; with liquid drop >= 25 um radius ${perMin(rime25).toFixed(4)}, of which the drop is the larger partner ${perMin(rime25big).toFixed(4)}`);
console.log(`ice-ice collisions ${perMin(ii).toFixed(3)} cm^-3 min^-1; collision energy (event-weighted) 5/50/95 % = ${kq(0.05).toExponential(1)} / ${kq(0.5).toExponential(1)} / ${kq(0.95).toExponential(1)} J, largest ${kev[kev.length - 1][0].toExponential(1)} J`);
console.log(`new ice per cm^3 per minute: Hallett-Mossop 0 (stops below about -8 C); drop shattering 0 to ${perMin(rime25 * 1.7).toExponential(2)} (0 to 0.14 x 12 = 1.7 fragments per freezing drop); ` +
  `ice-ice breakup (Phillips, D clamped to 0.5 mm) ${perMin(fragLo).toExponential(2)} (psi = 3.5e-3) to ${perMin(fragHi).toExponential(2)} (psi = 1), with the true D ${perMin(fragTrueD).toExponential(2)}; ` +
  `the old rule (lambda = 0.001 per event, 5 um radius fragments) ${perMin(oldRule).toExponential(2)}; old rule / breakup ${(oldRule / fragHi).toExponential(2)} (clamped), ${(oldRule / fragTrueD).toFixed(0)} (true D)`);
const out = { T, p: 60000, Fliq, liquid: ntot('w'), ice: ntot('i'), rime, rime25, rime25big, ii, fragLo, fragHi, fragTrueD, oldRule, hm: 0, shatter: [0, rime25 * 1.7],
  K0q: [kq(0.05), kq(0.5), kq(0.95), kev[kev.length - 1][0]], A05: PH.A(5e-4) };
if (process.argv.includes('--json')) fs.writeFileSync(path.join(__dirname, '..', 'data', 'cold.json'), JSON.stringify(out));
