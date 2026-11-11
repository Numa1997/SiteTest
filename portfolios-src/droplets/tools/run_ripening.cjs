// L8b: vapour ripening of the warm cloud in a closed saturated volume, the gradient descent of surface free energy.
// Pure water, and drops each holding the salt of a dry ammonium sulfate particle. 10 cm^3 (3010 drops), modes cut at 3 sigma_g.
//   node tools/run_ripening.cjs [--json]      writes data/ripening.json
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000), modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const EN = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'energy.json')));
const t50 = EN.warm.t50, t90 = EN.warm.t90;
// Record times: the nine of the first version (the numbers quoted in chapter 10 are read at these), and 73 more spaced evenly in ln t
// from 1 min to 1 day, so that figure 10.2 is a curve and the ledger of section 10.4 can be followed step by step.
const keyAt = [0, Math.round(t50), Math.round(t90), 1800, 3600, 3 * 3600, 6 * 3600, 12 * 3600, 86400];
const recAt = Array.from(new Set(keyAt.concat(Array.from({ length: 73 }, (_, k) => Math.round(60 * Math.pow(1440, k / 72)))))).sort((p, q) => p - q);
const LED = ['s', 'rc', 'nUp', 'nDown', 'flux', 'P', 'moved', 'diss', 'Wd', 'Wc', 'nd', 'nc'], sig6 = v => +v.toPrecision(6);
// salt: van 't Hoff factor i = 3, M_s = 0.13214 kg/mol, rho_s = 1770 kg/m^3; b = 3 i M_w m_s / (4 pi rho_w M_s)
const bSalt = rd => 3 * 3 * 0.018015 * (4 / 3 * Math.PI * rd ** 3 * 1770) / (4 * Math.PI * 1000 * 0.13214);
const out = { recAt, keyAt, t50, t90, a: P.kelvinA(A), G: P.growthG(A), bSalt: bSalt(0.05e-6), cases: {} };
for (const [name, bfun] of [['pure', null], ['salt', () => bSalt(0.05e-6)]]) {
  const runs = [];
  for (let s = 1; s <= 3; s++) {
    const u = P.rng(700 + s), radii = P.drawModes(modes, 10, u, 3), t0 = Date.now();
    const R = P.ripen(radii, A, { tEnd: 86400, recAt, b: bfun || undefined, ledger: !bfun });
    runs.push(R.rec.map(q => { const o = { t: q.t, alive: q.alive, F: q.F / R.rec[0].F, F0: q.t === 0 ? q.F : undefined, M: q.M, rmean3: q.rmean3,
      r: s === 1 && keyAt.includes(q.t) ? q.r.map(v => +(v * 1e6).toFixed(3)) : undefined };
      if (!bfun) LED.forEach(k => { o[k] = sig6(q[k]); }); return o; }));
    console.log(`${name} seed ${700 + s}: ${R.steps} steps [${((Date.now() - t0) / 1000).toFixed(1)} s]: ` + R.rec.filter(q => keyAt.includes(q.t)).map(q => `${(q.t / 60).toFixed(1)} min F ${(q.F / R.rec[0].F).toFixed(3)} n ${q.alive}`).join('; '));
  }
  out.cases[name] = runs;
}
// ---------------------------------------------------------------- the same cloud as classes of identical drops (per m^3 of air)
// Drops of one size ripen identically, so the distribution can be followed exactly as classes: each mode cut at 3 sigma_g and divided
// into classes of equal number, a class standing at the middle of its share. The class edges ride along as tracers of weight 0;
// ripening keeps the order of sizes, so the water of a class stays between its two edges and its density per unit ln r is its water
// over the distance of the edges. This gives the spectrum as a smooth curve, where a histogram of 3010 drawn drops (ten of them
// collectors) cannot.
{
  // quantiles of the standard normal cut at +-3: tabulate the cumulative share on a fine grid and invert by interpolation
  const nz = 60001, zs = Float64Array.from({ length: nz }, (_, i) => -3 + 6 * i / (nz - 1)), cdf = new Float64Array(nz);
  for (let i = 1; i < nz; i++) cdf[i] = cdf[i - 1] + 0.5 * (Math.exp(-zs[i] * zs[i] / 2) + Math.exp(-zs[i - 1] * zs[i - 1] / 2));
  const zOf = q => { const c = q * cdf[nz - 1]; let lo = 0, hi = nz - 1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (cdf[m] <= c) lo = m; else hi = m; } return zs[lo] + (zs[hi] - zs[lo]) * (c - cdf[lo]) / (cdf[hi] - cdf[lo]); };
  const radii = [], w = [], layout = [];
  for (const [md, nC] of [[modes[0], 800], [modes[1], 300]]) {
    const first = radii.length, ls = Math.log(md.sg);
    for (let k = 0; k <= nC; k++) { radii.push(md.rg * Math.exp(ls * zOf(k / nC))); w.push(0); }                   // edges, tracers
    for (let k = 0; k < nC; k++) { radii.push(md.rg * Math.exp(ls * zOf((k + 0.5) / nC))); w.push(md.N / nC); }   // classes
    layout.push({ edge0: first, c0: first + nC + 1, nC });
  }
  const specAt = [0, 3600, 6 * 3600, 86400], t0 = Date.now();
  const R = P.ripen(radii, A, { tEnd: 86400, recAt, w, ledger: true });
  const M0 = w.reduce((a, wk, k) => a + wk * P.massOf(radii[k]), 0);
  const spectrum = q => {   // points (r in um, share of the water per unit ln r), each hump closed with zeros at its outer edges
    const x = [], y = [];
    for (const L of layout) {
      const px = [], py = [];
      for (let k = 0; k < L.nC; k++) {
        const rc = q.r[L.c0 + k], e1 = q.r[L.edge0 + k], e2 = q.r[L.edge0 + k + 1];
        if (!(rc > 0 && e1 > 0 && e2 > e1)) continue;
        if (!px.length) { px.push(e1 * 1e6); py.push(0); }
        px.push(rc * 1e6); py.push(w[L.c0 + k] * P.massOf(rc) / M0 / Math.log(e2 / e1));
      }
      if (px.length) { px.push(q.r[L.edge0 + L.nC] * 1e6); py.push(0); }
      px.forEach((v, i) => { x.push(+v.toFixed(4)); y.push(+py[i].toFixed(5)); });
    }
    return { x, y };
  };
  out.classes = { nDroplet: 800, nCollector: 300, F0: R.rec[0].F, M0,
    rec: R.rec.map(q => { const o = { t: q.t, alive: q.alive, F: q.F / R.rec[0].F, M: q.M }; LED.forEach(k => { o[k] = sig6(q[k]); }); return o; }),
    spec: specAt.map(t => Object.assign({ t }, spectrum(R.rec.find(q => q.t === t)))) };
  // the rate of change of the radius against the radius, at the start and after one hour: dr/dt = G f_v (s - a/r)/r
  out.classes.rate = [0, 3600].map(t => { const q = R.rec.find(v => v.t === t), x = [], y = [];
    for (let k = 0; k <= 400; k++) { const r = 2e-6 * Math.pow(50, k / 400); x.push(+(r * 1e6).toFixed(4)); y.push(+(out.G * P.ventilation(r, A) * (q.s - out.a / r) / r * 3.6e9).toFixed(6)); }
    return { t, rc: q.rc, x, y }; });
  const at = t => R.rec.find(q => q.t === t), mp = name => out.cases.pure.reduce((a, r) => a + r.find(q => q.t === 3600)[name], 0) / 3;
  console.log(`classes (1100, per m^3): ${R.steps} steps [${((Date.now() - t0) / 1000).toFixed(1)} s]; F left after 1 h ${(at(3600).F / R.rec[0].F).toFixed(4)} (three draws: ${mp('F').toFixed(4)}), after 1 day ${(at(86400).F / R.rec[0].F).toFixed(4)}; water kept to ${(at(86400).M - 1).toExponential(1)}`);
  for (const t of [0, 60, 3600, 6 * 3600, 86400]) { const q = at(t); console.log(`   t = ${t} s: r_c ${(q.rc * 1e6).toFixed(2)} um, s ${(q.s).toExponential(3)}, growing ${(100 * q.nUp / (q.nUp + q.nDown)).toFixed(1)} % of ${q.alive.toExponential(3)} drops/m^3, flux ${q.flux.toExponential(3)} kg/s/m^3, moved ${(100 * q.moved / M0).toFixed(2)} % of the water, droplet mode holds ${(100 * q.Wd / M0).toFixed(2)} %, -dF/dt ${q.P.toExponential(3)} W/m^3, (F0 - F)/integral of P = ${t ? ((R.rec[0].F - q.F) / q.diss).toFixed(4) : '-'}`); }
}
// late-time growth of the cube of the mean radius against Lifshitz-Slyozov-Wagner's (4/9) G a (pure water)
const pr = out.cases.pure[0], i12 = pr.findIndex(q => q.t === 12 * 3600), i24 = pr.findIndex(q => q.t === 86400);
out.lsw = { measured: (pr[i24].rmean3 ** 3 - pr[i12].rmean3 ** 3) / (12 * 3600), theory: 4 / 9 * out.G * out.a };
console.log(`r^3 growth 12-24 h: ${out.lsw.measured.toExponential(3)} m^3/s against LSW (4/9) G a = ${out.lsw.theory.toExponential(3)} (ratio ${(out.lsw.measured / out.lsw.theory).toFixed(2)}); collection lowers F to ${(EN.warm.recs.find(q => Math.abs(q.t - 810) < 6).Es / EN.warm.Es0).toFixed(3)} by t90`);
if (process.argv.includes('--json')) fs.writeFileSync(path.join(__dirname, '..', 'data', 'ripening.json'), JSON.stringify(out));
