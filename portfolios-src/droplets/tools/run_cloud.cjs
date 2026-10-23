// L10: a cloud with a shape. Super-droplets move with the fall speed, a steady overturning cell and a stochastic element (the
// unresolved eddies), collide in their cells, evaporate in clear air, and rain out through the base.
//   node tools/run_cloud.cjs [--json]   (about 20 min; SEEDS=n, ONLY=name,name)
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000);
const tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const ext = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const seeds = +(process.env.SEEDS || 3), tEnd = 2700, per = [96, 32];
const out = { tEnd, per, cases: {} };
const r4 = v => +v.toPrecision(4);

// 0. checks: the box against the collection equation; well-mixedness of the stochastic element
function boxTest() {
  const res = [];
  for (let s = 1; s <= 4; s++) {
    const c = P.makeCloud(A, ext, { seed: 900 + s, Lx: 50, Lz: 50, h: 50, box: true, inside: () => true, perCell: [8192, 2048], S: 0 });
    let prev = c.census(), t50 = null, t90 = null;
    for (let k = 1; k <= 1500 && t90 === null; k++) {
      c.step(1); const z = c.census(), f = z.M40 / c.M0, fp = prev.M40 / c.M0;
      if (t50 === null && f >= 0.5) t50 = k - 1 + (0.5 - fp) / (f - fp);
      if (t90 === null && f >= 0.9) t90 = k - 1 + (0.9 - fp) / (f - fp);
      prev = z;
    }
    res.push([t50 / 60, t90 / 60]);
  }
  const m = i => res.reduce((a, r) => a + r[i], 0) / res.length, se = i => Math.sqrt(res.reduce((a, r) => a + (r[i] - m(i)) ** 2, 0) / (res.length - 1) / res.length);
  const g = P.makeGrid(16, 4e-3), modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
  const sce = P.sceRun(g, A, ext, modes, { dt: 0.5, tEnd: 1200, recordEvery: 1, trunc: 3 });
  const tq = q => { for (let i = 1; i < sce.F40.length; i++) if (sce.F40[i] >= q) return (sce.t[i - 1] + (q - sce.F40[i - 1]) / (sce.F40[i] - sce.F40[i - 1]) * (sce.t[i] - sce.t[i - 1])) / 60; };
  return { sdm: [m(0), se(0), m(1), se(1)], sce: [tq(0.5), tq(0.9)] };
}
function mixTest() {   // tiny drops (no fall), uniform start over the whole domain, peaked eps, mean flow: they must stay uniform
  const c = P.makeCloud(A, ext, { seed: 77, inside: () => true, perCell: [6, 0], modes: [{ N: 1, rg: 1e-9, sg: 1.0001 }, { N: 0, rg: 1e-9, sg: 1.0001 }], S: 0, peaked: true, eps: 4e-2, epsOut: 1e-3 });
  const cnt = () => { const H = new Float64Array(15 * 10); c.sd.forEach(q => { H[Math.min(14, Math.floor(q.z / 100)) * 10 + Math.min(9, Math.floor(q.x / 200))]++; }); return H; };
  const chi = H => { const n = H.reduce((a, v) => a + v, 0), e = n / H.length; return H.reduce((a, v) => a + (v - e) ** 2 / e, 0) / (H.length - 1); };
  const c0 = chi(cnt());
  for (let k = 0; k < 1800; k++) c.step(1);
  const H = cnt(), n = H.reduce((a, v) => a + v, 0), e = n / H.length;
  return { n, chi0: c0, chi: chi(H), maxDev: Math.max(...H.map(v => Math.abs(v / e - 1))), core: H[7 * 10 + 4] / e, corner: H[0] / e };
}
let t0 = Date.now();
if (!process.env.ONLY) {
  out.box = boxTest();
  console.log(`box (10 240 super-droplets, 4 seeds): t50 ${out.box.sdm[0].toFixed(3)} ± ${out.box.sdm[1].toFixed(3)}, t90 ${out.box.sdm[2].toFixed(3)} ± ${out.box.sdm[3].toFixed(3)} min; collection equation, same modes cut at 3 sigma_g, s = 16: ${out.box.sce.map(v => v.toFixed(3)).join(' / ')} [${((Date.now() - t0) / 1000).toFixed(0)} s]`);
  t0 = Date.now(); out.mix = mixTest();
  console.log(`well-mixed test (${out.mix.n} air parcels, 30 min, eps from 4e-2 in the core to 1e-3): chi^2 per cell ${out.mix.chi0.toFixed(2)} at the start, ${out.mix.chi.toFixed(2)} after; largest cell deviation ${(100 * out.mix.maxDev).toFixed(1)} %; core cell ${out.mix.core.toFixed(3)}, corner ${out.mix.corner.toFixed(3)} of the mean [${((Date.now() - t0) / 1000).toFixed(0)} s]`);
}

// 1. the cases
const cases = {
  reference: { shape: 'cumulus' },
  noStochastic: { shape: 'cumulus', stochastic: false },
  stillAir: { shape: 'cumulus', W0: 0 },
  box: { shape: 'box' },
  disc: { shape: 'disc' },
  tower: { shape: 'tower' },
  peakedEps: { shape: 'cumulus', peaked: true, eps: 4e-2, epsOut: 1e-3, kernelEps: true },
};
const only = process.env.ONLY ? process.env.ONLY.split(',') : Object.keys(cases);
for (const name of only) {
  const cfg = cases[name], runs = [];
  t0 = Date.now();
  for (let s = 1; s <= seeds; s++) {
    const ko = cfg.kernelEps ? Object.assign({}, ext, { eps: 'local' }) : ext;
    const c = P.makeCloud(A, ko, Object.assign({ seed: 1000 + s, perCell: per }, cfg));
    const rec = { t: [], M: [], M40: [], M100: [], rain: [], evap: [] }, snaps = {};
    const census = () => { const z = c.census(); rec.t.push(z.t); rec.M.push(z.M / c.M0); rec.M40.push(z.M40 / c.M0); rec.M100.push(z.M100 / c.M0); rec.rain.push(z.rain / c.M0); rec.evap.push(z.evap / c.M0); };
    census();
    const snap = () => { const q = c.sd.filter((_, i) => i % 6 === 0); snaps[c.t] = q.map(d => [Math.round(d.x), Math.round(d.z), +(d.r * 1e6).toFixed(1)]); };
    if (s === 1) snap();
    for (let k = 1; k <= tEnd; k++) { c.step(1); if (k % 30 === 0) census(); if (s === 1 && [600, 1200, 1800, 2700].includes(k)) snap(); }
    const born = c.bornLog;     // every super-droplet's first passage of 100 um, logged when it happens
    const rainBig = c.rainLog.filter(q => q[2] >= 100e-6);
    const tRain = f => { for (let i = 0; i < rec.rain.length; i++) if (rec.rain[i] >= f) return rec.t[i]; return null; };
    runs.push({ seed: 1000 + s, n0: rec.M.length && c.sd.length, M0: c.M0, first100: c.first100, rec, born, snaps: s === 1 ? snaps : undefined,
      firstRain: rainBig.length ? rainBig[0][0] : null, t1: tRain(0.01), t10: tRain(0.1), collisions: c.collisions,
      rainX: rainBig.map(q => [Math.round(q[1]), q[0], +(q[2] * 1e6).toFixed(0), r4(q[3] * P.massOf(q[2]) / c.M0)]) });
  }
  const mean = a => a.filter(v => v !== null).reduce((x, y) => x + y, 0) / a.filter(v => v !== null).length;
  const last = q => q.rec;
  const L = runs.map(last), iEnd = L[0].t.length - 1;
  console.log(`${name.padEnd(13)} [${((Date.now() - t0) / 1000).toFixed(0)} s, ${seeds} seeds]: first 100 um drop at ${runs.map(q => q.first100 ? (q.first100.t / 60).toFixed(1) + ' min (' + q.first100.x.toFixed(0) + ', ' + q.first100.z.toFixed(0) + ' m)' : '-').join('; ')}`);
  console.log(`${''.padEnd(13)} first drizzle at the ground ${runs.map(q => q.firstRain === null ? '-' : (q.firstRain / 60).toFixed(1)).join(' / ')} min; 1 % / 10 % of the water rained by ${(mean(runs.map(q => q.t1)) / 60).toFixed(1)} / ${(mean(runs.map(q => q.t10)) / 60).toFixed(1)} min; ` +
    `at 45 min: in the air ${(100 * mean(L.map(r => r.M[iEnd]))).toFixed(1)} %, rained ${(100 * mean(L.map(r => r.rain[iEnd]))).toFixed(1)} %, evaporated ${(100 * mean(L.map(r => r.evap[iEnd]))).toFixed(1)} %`);
  out.cases[name] = { cfg: Object.assign({}, cfg), runs };
}
if (process.argv.includes('--json')) {
  const prev = (() => { try { return JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'cloud.json'))); } catch (e) { return {}; } })();
  if (process.env.ONLY) { prev.cases = Object.assign(prev.cases || {}, out.cases); fs.writeFileSync(path.join(__dirname, '..', 'data', 'cloud.json'), JSON.stringify(prev)); }
  else fs.writeFileSync(path.join(__dirname, '..', 'data', 'cloud.json'), JSON.stringify(out));
}
