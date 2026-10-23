// L8: energy, entropy and who eats whom. Diagnostics on the collection equation (L4) and the exact Monte Carlo (L5), and the two
// models that make "minimise energy" a rule of motion (every pair equally likely; the largest pair first).
//   node tools/run_energy.cjs [--json]      writes data/energy.json with --json
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000), T = A.T, sig = P.sigmaWater(T), kB = P.K_B, gs = P.G0 * (1 - A.rho / P.RHO_W);
const tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const ext = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const CUTS = [20e-6, 100e-6], NAMES = ['droplets', 'collectors', 'drizzle'];
const ES = sig * P.SURF;                     // J per kg^(2/3): surface energy of a drop is ES m^(2/3)
const s = 8, grid = P.makeGrid(s, 4e-3), n = grid.n, w = Math.LN2 / s;
const vk = grid.r.map(r => P.vBeard(r, A));
const out = { s, cuts: CUTS, names: NAMES, sigma: sig, T, r: grid.r };
const t0all = Date.now();
const r6 = v => +v.toPrecision(6);

// ---------------------------------------------------------------- A. the warm cloud with the ledger (extended kernel)
const Nstart = P.lognormalBins(grid, modes), Nd = P.lognormalBins(grid, [modes[0]]);
const led = P.makeLedger(grid, CUTS, Nd.map((v, k) => v * grid.x[k]));
const recs = [];
let t0 = Date.now();
const K = P.kernelMatrix(grid, A, ext);
function classState(N, over) {
  const num = [0, 0, 0], wat = [0, 0, 0], tag = [0, 0, 0];
  for (let k = 0; k < n; k++) { const c = led.cls[k]; num[c] += N[k]; wat[c] += N[k] * grid.x[k]; tag[c] += led.tag[k]; }
  num[2] += over.N; wat[2] += over.M; tag[2] += led.overTag;
  return { num, wat, tag };
}
const sce = P.sceRun(grid, A, ext, modes, { K, dt: 1, tEnd: 3600, recordEvery: 10, snapAt: [], ledger: led,
  onRecord: (t, N, over, L) => {
    let Pg = 0; for (let k = 0; k < n; k++) Pg += N[k] * grid.x[k] * gs * vk[k];
    if (over.N > 0) Pg += over.M * gs * P.vBeard(P.radiusOf(over.M / over.N), A);
    const me = P.maxentCompare(grid, N, over), cs = classState(N, over);
    recs.push({ t, Es: ES * P.surfaceSum(L, N), Pg, num: cs.num, wat: cs.wat, tag: cs.tag, mergers: Array.from(L.mergers), eaten: Array.from(L.eaten),
      released: Array.from(L.released, v => v * ES), gate: Array.from(L.gate), gateBin: Array.from(L.gateBin), Ntot: me.N, epsExp: me.epsExp, epsGamma: me.epsGamma, nu: me.nu,
      spec: (t % 60 === 0) ? { N: Array.from(N), over: { N: over.N, M: over.M }, Mexp: Array.from(me.Mexp), Mgamma: Array.from(me.Mgamma) } : null });
  } });
const tA = (Date.now() - t0) / 1000;
// the same run without the ledger: the water must evolve bit for bit as before
t0 = Date.now();
const plain = P.sceRun(grid, A, ext, modes, { K, dt: 1, tEnd: 3600, recordEvery: 10 });
let identical = true; for (let k = 0; k < n; k++) if (plain.N[k] !== sce.N[k]) identical = false;
const tq = (q, F, t) => { for (let i = 1; i < F.length; i++) if (F[i] >= q) return t[i - 1] + (q - F[i - 1]) / (F[i] - F[i - 1]) * (t[i] - t[i - 1]); return null; };
const t50 = tq(0.5, sce.F40, sce.t), t90 = tq(0.9, sce.F40, sce.t);
const W0 = sce.M0, tagErr = (() => { const last = recs[recs.length - 1]; const tagSum = last.tag.reduce((a, v) => a + v, 0); const d0 = Nd.reduce((a, v, k) => a + v * grid.x[k], 0); return tagSum / d0 - 1; })();
// drizzle water budget: its change equals the binned gateway plus the water drizzle drops ate from smaller classes
const last = recs[recs.length - 1], first = recs[0];
const dW2 = last.wat[2] - first.wat[2], inflow = last.gateBin[0] + last.gateBin[1] + last.eaten[2 * 3 + 0] + last.eaten[2 * 3 + 1];
console.log(`A. warm cloud, extended kernel, s = 8, dt = 1 s, with the ledger [${tA.toFixed(1)} s; without ${((Date.now() - t0) / 1000).toFixed(1)} s]`);
console.log(`   water evolves bit for bit as without the ledger: ${identical}; t50/t90 = ${(t50 / 60).toFixed(3)}/${(t90 / 60).toFixed(3)} min (interpolated, records every 10 s)`);
console.log(`   Lyapunov check: steps where the surface rose ${led.rises || 0} (largest relative rise ${(led.maxRise || 0).toExponential(1)}); droplet-mode tag conserved to ${tagErr.toExponential(1)}; drizzle budget closes to ${((dW2 - inflow) / W0).toExponential(1)} of the water`);
const at = tt => recs.reduce((b, q) => Math.abs(q.t - tt) < Math.abs(b.t - tt) ? q : b, recs[0]);
for (const [lab, tt] of [['t = 0', 0], ['t50', t50], ['t90', t90], ['20 min', 1200], ['60 min', 3600]]) {
  const q = at(tt), tot = q.mergers.reduce((a, v) => a + v, 0);
  const ch = (a, b) => q.mergers[a * 3 + b], chE = (a, b) => q.eaten[a * 3 + b];
  const dd = ch(0, 0), cd = ch(1, 0), cc = ch(1, 1), Dd = ch(2, 0), Dc = ch(2, 1), DD = ch(2, 2);
  const share = v => tot > 0 ? (100 * v / tot).toFixed(3) : '-';
  const Wd = q.wat[2] > 0 ? q.tag[2] / q.wat[2] : 0, gb = q.gateBin[0] + q.gateBin[1], g = q.gate[0] + q.gate[1];
  console.log(`   ${lab.padEnd(6)} (${(q.t / 60).toFixed(2)} min): E_s = ${q.Es.toExponential(4)} J/m3 (${(100 * q.Es / first.Es).toFixed(2)} % of start); gravity ${q.Pg.toExponential(3)} W/m3; N = ${(q.Ntot * 1e-6).toFixed(2)} cm^-3`);
  console.log(`          mergers by channel (% of ${(tot * 1e-6).toFixed(3)} cm^-3): d-d ${share(dd)}, c-d ${share(cd)}, c-c ${share(cc)}, D-d ${share(Dd)}, D-c ${share(Dc)}, D-D ${share(DD)}`);
  console.log(`          water in classes (% of all): ${q.wat.map(v => (100 * v / W0).toFixed(2)).join(' / ')}; numbers ${q.num.map(v => (v * 1e-6).toExponential(3)).join(' / ')} cm^-3`);
  console.log(`          drizzle water from the droplet mode ${(100 * Wd).toFixed(2)} %; gateway into drizzle via a collector partner: binned ${gb > 0 ? (100 * q.gateBin[1] / gb).toFixed(2) : '-'} %, exact product ${g > 0 ? (100 * q.gate[1] / g).toFixed(2) : '-'} %`);
  console.log(`          max-entropy spectrum error: exponential ${q.epsExp.toFixed(3)}, gamma ${q.epsGamma.toFixed(3)} (nu = ${q.nu.toFixed(3)})`);
}
// release rate against gravity over the run
let maxRatio = 0, tMax = 0;
for (let i = 1; i < recs.length; i++) { const rel = (recs[i - 1].Es - recs[i].Es) / (recs[i].t - recs[i - 1].t), ratio = rel / (0.5 * (recs[i].Pg + recs[i - 1].Pg)); if (ratio > maxRatio) { maxRatio = ratio; tMax = recs[i].t; } }
const totRel = first.Es - last.Es, totMerg = last.mergers.reduce((a, v) => a + v, 0);
let gravWork = 0; for (let i = 1; i < recs.length; i++) gravWork += 0.5 * (recs[i].Pg + recs[i - 1].Pg) * (recs[i].t - recs[i - 1].t);
console.log(`   surface-energy release / gravity's drag dissipation: largest ${maxRatio.toFixed(4)} (at ${tMax} s); over the hour ${totRel.toExponential(3)} J/m3 released against ${gravWork.toExponential(3)} J/m3 of gravity's work (${(totRel / gravWork * 100).toFixed(2)} %)`);
console.log(`   entropy produced by merging in the hour ${(totRel / T).toExponential(3)} J/(K m3); per merger on average ${(totRel / totMerg / (kB * T)).toExponential(2)} k_B; time for gravity to dissipate the start's surface energy ${(first.Es / first.Pg).toFixed(1)} s`);
out.warm = { t50, t90, identical, rises: led.rises || 0, maxRise: led.maxRise || 0, tagErr, budget: (dW2 - inflow) / W0, W0, Es0: first.Es, Pg0: first.Pg, maxRatio, tMax, totRel, gravWork, totMerg,
  recs: recs.map(q => ({ t: q.t, Es: r6(q.Es), Pg: r6(q.Pg), num: q.num.map(r6), wat: q.wat.map(r6), tag: q.tag.map(r6), mergers: q.mergers.map(r6), eaten: q.eaten.map(r6), released: q.released.map(r6),
    gate: q.gate.map(r6), gateBin: q.gateBin.map(r6), N: r6(q.Ntot), epsExp: r6(q.epsExp), epsGamma: r6(q.epsGamma), nu: r6(q.nu),
    spec: q.spec ? { N: q.spec.N.map(r6), over: q.spec.over, Mexp: q.spec.Mexp.map(r6), Mgamma: q.spec.Mgamma.map(r6) } : undefined })) };

// ---------------------------------------------------------------- B. the constant kernel: every pair equally likely
const DTF = +(process.env.DTF || 0.02);   // step: K0 N dt = DTF
const K0 = 1e-10;                                 // m^3/s; sets only the clock
const Kc = new Float64Array(n * n).fill(K0);
function runConstant(Nfirst, stops) {             // adaptive step dt = 0.02/(K0 N); records at the requested N/N0
  const N = Float64Array.from(Nfirst), over = { N: 0, M: 0 }, L = P.makeLedger(grid, CUTS, null);
  let Ntot = N.reduce((a, v) => a + v, 0); const Nini = Ntot, rows = []; let t = 0, si = 0, rises = 0, steps = 0;
  while (si < stops.length) {
    const dt = DTF / (K0 * Ntot), S0 = P.surfaceSum(L, N);
    P.sceStep(grid, Kc, N, over, dt, null, L); t += dt; steps++;
    if (P.surfaceSum(L, N) > S0) rises++;
    Ntot = over.N; for (let k = 0; k < n; k++) Ntot += N[k];
    while (si < stops.length && Ntot / Nini <= stops[si]) { const me = P.maxentCompare(grid, N, over); rows.push({ f: stops[si], t, Nf: Ntot / Nini, epsExp: me.epsExp, epsGamma: me.epsGamma, nu: me.nu, N: Array.from(N), over: { ...over }, Mexp: Array.from(me.Mexp), mergers: Array.from(L.mergers) }); si++; }
  }
  return { rows, rises, steps, Nini };
}
t0 = Date.now();
// B1. exact test: exponential start with the warm cloud's number and water
const M0w = W0, N0w = Nstart.reduce((a, v) => a + v, 0), mb = M0w / N0w;
const Nexp = Float64Array.from(grid.x.map(x => N0w / mb * Math.exp(-x / mb) * x * w));
const ex = runConstant(Nexp, [0.1, 0.01]);
const Nb0 = Nexp.reduce((a, v) => a + v, 0);     // the binned start (the grid begins at 1 um: the exponential's drops below it are not on it)
console.log(`B1. binned start holds ${(Nb0 / N0w).toFixed(5)} of the exponential's drops and ${(Nexp.reduce((a, v, k) => a + v * grid.x[k], 0) / M0w).toFixed(6)} of its water`);
for (const q of ex.rows) {
  const Nexact = Nb0 / (1 + K0 * Nb0 * q.t / 2);
  let eps = 0, Mt = q.over.M; for (let k = 0; k < n; k++) Mt += q.N[k] * grid.x[k];
  const Nn = Nexact, Mm = Mt;           // exact shape (N^2/M) exp(-N m/M) with the exact N(t) and the water
  for (let k = 0; k < n; k++) eps += Math.abs(q.N[k] * grid.x[k] - Nn * Nn / Mm * Math.exp(-Nn * grid.x[k] / Mm) * grid.x[k] * grid.x[k] * w);
  console.log(`B1. constant kernel, exponential start: N/N0 = ${q.Nf.toFixed(4)} at K0 N0 t/2 = ${(K0 * Nb0 * q.t / 2).toFixed(3)}; N against exact ${(q.Nf * Nb0 / Nexact - 1).toExponential(2)}; spectrum error against the exact exponential ${(eps / Mt).toFixed(4)}`);
  q.epsExact = eps / Mt; q.Nerr = q.Nf * Nb0 / Nexact - 1;
}
// B2. the thesis start
const stops = [0.9, 0.7, 0.5, 0.3, 0.2, 0.1, 0.05, 0.03, 0.02, 0.01, 0.005, 0.003, 0.002, 0.001, 5e-4, 2e-4, 1e-4];
const cs = runConstant(Nstart, stops);
console.log(`B2. constant kernel from the warm cloud's start (${cs.steps} steps, surface rose in ${cs.rises}) [${((Date.now() - t0) / 1000).toFixed(1)} s]`);
for (const q of cs.rows) {
  const tot = q.mergers.reduce((a, v) => a + v, 0), dd = q.mergers[0], cd = q.mergers[3], cc = q.mergers[4];
  console.log(`   N/N0 = ${q.f}: spectrum error exponential ${q.epsExp.toFixed(3)}, gamma ${q.epsGamma.toFixed(3)} (nu ${q.nu.toFixed(3)}); mergers d-d ${(100 * dd / tot).toFixed(2)} %, c-d ${(100 * cd / tot).toFixed(2)} %, c-c ${(100 * cc / tot).toFixed(3)} %`);
}
out.constant = { K0, exact: ex.rows.map(q => ({ f: q.f, Nf: q.Nf, epsExact: q.epsExact, Nerr: q.Nerr })), rises: cs.rises,
  rows: cs.rows.map(q => ({ f: q.f, t: q.t, epsExp: r6(q.epsExp), epsGamma: r6(q.epsGamma), nu: r6(q.nu), mergers: q.mergers.map(r6), N: q.N.map(r6), over: q.over, Mexp: q.Mexp.map(r6) })) };
// the physical kernel's error against N/N0 (from A), for the same plot
out.warm.epsByN = recs.map(q => [r6(q.Ntot / N0w), r6(q.epsExp), r6(q.epsGamma)]);

// ---------------------------------------------------------------- C. the exact Monte Carlo under three rules, 100 cm^3
const V = 100, trunc = 3, nSeeds = +(process.env.SEEDS || 20);
const clsOf = r => r < CUTS[0] ? 0 : r < CUTS[1] ? 1 : 2;
const area23 = r => Math.pow(P.massOf(r), 2 / 3);
const marks = [0.99, 0.95, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01];
function mcRun(kind, seed) {
  const u = P.rng(seed), radii = P.drawModes(modes, V, u, trunc), Nini = radii.length;
  let S = radii.reduce((a, r) => a + area23(r), 0); const S0 = S;
  const ch = new Float64Array(9), rows = []; let mi = 0, bad = 0, first100 = null;
  const note = (alive) => { while (mi < marks.length && (alive - 1) / Nini <= marks[mi]) { rows.push({ f: marks[mi], merged: Nini - alive + 1, S: S / S0, ch: Array.from(ch) }); mi++; } };
  const onEvent = (r1, r2, t, alive) => {
    const a = Math.max(r1, r2), b = Math.min(r1, r2), R = Math.cbrt(a * a * a + b * b * b), d = area23(a) + area23(b) - area23(R);
    if (!(d > 0)) bad++;
    S -= d; ch[clsOf(a) * 3 + clsOf(b)]++;
    if (first100 === null && R >= 100e-6) first100 = { merged: Nini - alive + 1, t, partner: b };
    note(alive);
  };
  const kopt = kind === 'constant' ? { constant: 1e-10 } : ext;
  const res = P.gillespieRun(V, radii, A, kopt, { u, seed, tEnd: kind === 'constant' ? 1e12 : 3600, recordEvery: kind === 'constant' ? 1e12 : 3600, onEvent, firstR: [100e-6] });
  return { seed, Nini, rows, bad, events: res.events, first100, S: S / S0 };
}
function steepest(seed) {      // the largest drop eats the next largest, until one drop is left; the ledger at the same marks
  const u = P.rng(seed), radii = P.drawModes(modes, V, u, trunc).sort((p, q) => q - p), Nini = radii.length;
  let S = radii.reduce((a, r) => a + area23(r), 0); const S0 = S, ch = new Float64Array(9), rows = []; let mi = 0, big = radii[0], first100 = null;
  for (let k = 1; k < Nini; k++) {
    const b = radii[k], R = Math.cbrt(big ** 3 + b ** 3), d = area23(big) + area23(b) - area23(R);
    S -= d; ch[clsOf(big) * 3 + clsOf(b)]++; big = R;
    if (first100 === null && R >= 100e-6) first100 = { merged: k, partner: b };
    const alive = Nini - k;
    while (mi < marks.length && alive / Nini <= marks[mi]) { rows.push({ f: marks[mi], merged: k, S: S / S0, ch: Array.from(ch) }); mi++; }
  }
  return { seed, Nini, rows, first100, S: S / S0, rFinal: big };
}
out.mc = { V, trunc, marks, seeds: nSeeds };
for (const kind of ['physical', 'constant']) {
  t0 = Date.now();
  const runs = []; for (let k = 1; k <= nSeeds; k++) runs.push(mcRun(kind, (kind === 'physical' ? 800000 : 810000) + k));
  const agg = marks.map(f => {
    const have = runs.map(q => q.rows.find(r => r.f === f)).filter(Boolean);
    if (!have.length) return null;
    const mean = a => a.reduce((x, y) => x + y, 0) / a.length, se = a => a.length > 1 ? Math.sqrt(a.reduce((x, y) => x + (y - mean(a)) ** 2, 0) / (a.length - 1) / a.length) : 0;
    const shares = [0, 1, 2, 3, 4, 5, 6, 7, 8].map(c => have.map(r => r.ch[c] / r.merged));
    return { f, runs: have.length, S: mean(have.map(r => r.S)), Sse: se(have.map(r => r.S)), share: shares.map(mean), shareSe: shares.map(se) };
  }).filter(Boolean);
  out.mc[kind] = { agg, bad: runs.reduce((a, q) => a + q.bad, 0), first100: runs.map(q => q.first100), events: runs.map(q => q.events) };
  console.log(`C. Monte Carlo, ${kind} rule, ${V} cm^3, ${nSeeds} seeds: energy-raising mergers ${out.mc[kind].bad} [${((Date.now() - t0) / 1000).toFixed(0)} s]`);
  for (const q of agg) console.log(`   N/N0 = ${q.f} (${q.runs} runs): surface ${(100 * q.S).toFixed(2)} ± ${(100 * q.Sse).toFixed(2)} % of start; mergers d-d ${(100 * q.share[0]).toFixed(2)} %, c-d ${(100 * q.share[3]).toFixed(2)} %, c-c ${(100 * q.share[4]).toFixed(2)} %, D-d ${(100 * q.share[6]).toFixed(2)} %, D-c ${(100 * q.share[7]).toFixed(2)} %, D-D ${(100 * q.share[8]).toFixed(2)} %`);
  const f1 = runs.map(q => q.first100).filter(Boolean);
  if (f1.length) console.log(`   first drop of 100 um: in ${f1.length}/${nSeeds} runs, after ${(f1.map(q => q.merged).sort((a, b) => a - b)[Math.floor(f1.length / 2)])} mergers (median), partner >= 20 um in ${f1.filter(q => q.partner >= 20e-6).length}`);
}
{
  const st = []; for (let k = 1; k <= nSeeds; k++) st.push(steepest(800000 + k));
  const q0 = st[0];
  console.log(`C. steepest descent, ${V} cm^3 (seed 800001): first 100 um drop after ${q0.first100.merged} mergers (partner ${(q0.first100.partner * 1e6).toFixed(1)} um); final drop ${(q0.rFinal * 1e3).toFixed(3)} mm`);
  for (const q of q0.rows) { const tot = q.merged; console.log(`   N/N0 = ${q.f}: surface ${(100 * q.S).toFixed(2)} % of start; mergers c-c ${(100 * q.ch[4] / tot).toFixed(2)} %, D-c ${(100 * q.ch[7] / tot).toFixed(2)} %, D-d ${(100 * q.ch[6] / tot).toFixed(2)} %`); }
  out.mc.steepest = { rows: q0.rows, first100: q0.first100, rFinal: q0.rFinal, Nini: q0.Nini };
}
console.log(`[all ${((Date.now() - t0all) / 1000).toFixed(0)} s]`);
if (process.argv.includes('--json')) fs.writeFileSync(path.join(__dirname, '..', 'data', 'energy.json'), JSON.stringify(out));
