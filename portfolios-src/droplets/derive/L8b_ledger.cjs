// L8b: the numbers of section 10.4 (ripening as a gradient descent), from physics.cjs and data/ripening.json.
//   node derive/L8b_ledger.cjs
'use strict';
const P = require('../physics.cjs'), R = require('../data/ripening.json'), EN = require('../data/energy.json');
const A = P.air(283.15, 85000), sig = P.sigmaWater(A.T), Rv = 461.5, T = A.T, a = P.kelvinA(A), G = P.growthG(A), C = R.classes;
const at = t => C.rec.find(q => q.t === t), q0 = at(0);
console.log(`a = ${(a * 1e9).toFixed(3)} nm, G = ${G.toExponential(3)} m^2/s, sigma = ${sig.toFixed(5)}`);
// G's two resistances (Rogers and Yau 7.17, 7.18), as in growthG
{ const L = 2.477e6, Kt = 2.48e-2, es = 611.2 * Math.exp(17.67 * (T - 273.15) / (T - 29.65)), Dv = 2.11e-5 * Math.pow(T / 273.15, 1.94) * (101325 / A.p);
  const Fk = (L / (Rv * T) - 1) * L * 1000 / (Kt * T), Fd = 1000 * Rv * T / (Dv * es);
  console.log(`F_k = ${Fk.toExponential(3)}, F_d = ${Fd.toExponential(3)} s/m^2; heat share ${(100 * Fk / (Fk + Fd)).toFixed(0)} %; D_v = ${Dv.toExponential(3)}, e_s = ${es.toFixed(0)} Pa; diffusion alone G_d = ${(1 / Fd).toExponential(3)}`); }
for (const r of [8e-6, 40e-6]) console.log(`mu(${r * 1e6} um) = ${(2 * sig / (1000 * r)).toFixed(2)} J/kg = lifting by ${(2 * sig / (1000 * r) / 9.81).toFixed(2)} m; a/r = ${(a / r).toExponential(3)}`);
console.log(`start: s = ${q0.s.toExponential(3)} (${(100 * q0.s).toFixed(4)} %), r_c = ${(q0.rc * 1e6).toFixed(2)} um, growing ${(100 * q0.nUp / (q0.nUp + q0.nDown)).toFixed(1)} %`);
// one step, drop by drop
const rate = (r, s) => 4 * Math.PI * 1000 * r * G * P.ventilation(r, A) * (s - a / r);
for (const r of [5e-6, 8e-6, 12e-6, 40e-6]) { const md = rate(r, q0.s); console.log(`  r = ${r * 1e6} um: f_v ${P.ventilation(r, A).toFixed(3)}, dm/dt = ${md.toExponential(3)} kg/s = ${(100 * md * 3600 / P.massOf(r)).toFixed(2)} % of its mass per hour, dr/dt = ${(md / (4 * Math.PI * 1000 * r * r) * 3.6e9).toFixed(3)} um/h`); }
console.log(`  a 40 um collector gains ${(rate(40e-6, q0.s) / rate(12e-6, q0.s)).toFixed(1)} times what a 12 um droplet gains`);
// who receives the flux at the start: the classes of the two modes (rebuilt as in run_ripening.cjs)
{ const nz = 60001, zs = Float64Array.from({ length: nz }, (_, i) => -3 + 6 * i / (nz - 1)), cdf = new Float64Array(nz);
  for (let i = 1; i < nz; i++) cdf[i] = cdf[i - 1] + 0.5 * (Math.exp(-zs[i] * zs[i] / 2) + Math.exp(-zs[i - 1] * zs[i - 1] / 2));
  const zOf = q => { const c = q * cdf[nz - 1]; let lo = 0, hi = nz - 1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (cdf[m] <= c) lo = m; else hi = m; } return zs[lo] + (zs[hi] - zs[lo]) * (c - cdf[lo]) / (cdf[hi] - cdf[lo]); };
  let upD = 0, upC = 0, nUpD = 0, mean = 0, nAll = 0, sf = 0, srf = 0;
  for (const [md, nC] of [[{ N: 300e6, rg: 8e-6, sg: 1.25 }, 800], [{ N: 1e6, rg: 40e-6, sg: 1.2 }, 300]]) for (let k = 0; k < nC; k++) {
    const r = md.rg * Math.exp(Math.log(md.sg) * zOf((k + 0.5) / nC)), w = md.N / nC, m = rate(r, q0.s);
    mean += w * r; nAll += w; sf += w * P.ventilation(r, A); srf += w * r * P.ventilation(r, A);
    if (m > 0) { if (r < 20e-6) { upD += w * m; nUpD += w; } else upC += w * m; }
  }
  console.log(`  number-mean radius ${(mean / nAll * 1e6).toFixed(3)} um; sum r f/sum f = ${(srf / sf * 1e6).toFixed(3)} um; flux ${(upD + upC).toExponential(3)} kg/s/m^3 (stored ${q0.flux.toExponential(3)}): ${(100 * upD / (upD + upC)).toFixed(1)} % to droplets above r_c (${(nUpD / 1e6).toFixed(0)} per cm^3), ${(100 * upC / (upD + upC)).toFixed(1)} % to collectors`); }
// time scales
console.log(`r_c^3/(G a) = ${(q0.rc ** 3 / (G * a)).toFixed(0)} s = ${(q0.rc ** 3 / (G * a) / 3600).toFixed(2)} h; smallest drop ${(8 * Math.pow(1.25, -3)).toFixed(2)} um: r^3/(3 G a) = ${((8e-6 * Math.pow(1.25, -3)) ** 3 / (3 * G * a)).toFixed(0)} s; largest droplet ${(8 * 1.25 ** 3).toFixed(1)} um, collectors ${(40 / 1.2 ** 3).toFixed(1)} to ${(40 * 1.2 ** 3).toFixed(1)} um`);
const firstGone = C.rec.find(q => q.alive < q0.alive * (1 - 1e-9)), lastFull = C.rec[C.rec.indexOf(firstGone) - 1];
console.log(`first class gone between ${lastFull.t} and ${firstGone.t} s`);
// the table
for (const t of [60, 3600, 21600, 86400]) { const q = at(t); console.log(`t = ${t}: r_c ${(q.rc * 1e6).toFixed(1)} um; drops ${(q.alive / 1e6).toFixed(0)} per cm^3; growing ${(100 * q.nUp / (q.nUp + q.nDown)).toFixed(0)} %; passed ${(100 * q.moved / C.M0).toFixed(1)} %; droplet mode ${(100 * q.Wd / C.M0).toFixed(1)} %, collector mode ${(100 * q.Wc / C.M0).toFixed(1)} %; droplet-mode drops ${(q.nd / 1e6).toFixed(0)}, collector-mode ${(q.nc / 1e6).toFixed(2)} per cm^3; F left ${(100 * q.F).toFixed(1)} %; s ${(100 * q.s).toFixed(4)} %`); }
console.log(`start shares: droplet mode ${(100 * q0.Wd / C.M0).toFixed(1)} %, collectors ${(100 * q0.Wc / C.M0).toFixed(1)} %; water ${(C.M0 * 1e3).toFixed(3)} g/m^3; F0 ${C.F0.toFixed(4)} J/m^3`);
const gaps = C.rec.filter(q => q.t >= 60).map(q => (C.F0 * (1 - q.F)) / q.diss - 1);
console.log(`(F0 - F)/integral of P - 1: ${(100 * Math.min(...gaps)).toFixed(2)} to ${(100 * Math.max(...gaps)).toFixed(2)} %`);
const q90 = EN.warm.recs.find(q => Math.abs(q.t - 810) < 6), Pcol = (EN.warm.Es0 - q90.Es) / q90.t;
console.log(`-dF/dt: ripening at start ${q0.P.toExponential(2)} W/m^3, largest ${Math.max(...C.rec.map(q => q.P)).toExponential(2)} at ${C.rec.reduce((b, q) => q.P > b.P ? q : b).t} s; entropy production at start ${(q0.P / T).toExponential(2)} W/K/m^3; collection mean to t90 ${Pcol.toExponential(2)} W/m^3, ratio ${(Pcol / q0.P).toFixed(0)}`);
console.log(`r_c^3 growth 12-24 h over (4/9) G a: ${((at(86400).rc ** 3 - at(43200).rc ** 3) / 43200 / (4 / 9 * G * a)).toFixed(2)}; vanished drops by 1 h: ${(100 * (1 - at(3600).alive / q0.alive)).toFixed(1)} %, by 1 day ${(100 * (1 - at(86400).alive / q0.alive)).toFixed(1)} %`);
