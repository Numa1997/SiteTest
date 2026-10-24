// L10: a cloud with a shape. Super-droplets move with the fall speed, a mean overturning motion held inside the outline and a stochastic
// element, collide in their cells, evaporate (with ventilation) in clear air, and rain out through the ground.
//   node tools/run_cloud.cjs CASE [CASE ...]    runs the named cases, each into data/cloud/<case>.json
//   node tools/run_cloud.cjs --merge            joins data/cloud/*.json into data/cloud.json
// Cases: tests (box convergence and well-mixed), the ladder (column, evap, cell, reference), the sensitivities (Le50, Le200, peaked,
// peakedAyala, noVent), the named shapes (box, disc, tower) and the random outlines (rough0, rough3, rough6). About 1.5 h on 4 cores.
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const A = P.air(283.15, 85000);
const tab = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'etab_warm.json')));
const ext = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const DIR = path.join(__dirname, '..', 'data', 'cloud'), tEnd = 2700, per = [96, 32];
const r4 = v => +v.toPrecision(4);
if (process.argv.includes('--merge')) {
  const out = { tEnd, per, cases: {} };
  for (const f of fs.readdirSync(DIR).sort()) { const d = JSON.parse(fs.readFileSync(path.join(DIR, f))); if (f === 'tests.json') Object.assign(out, d); else out.cases[f.replace('.json', '')] = d; }
  fs.writeFileSync(path.join(__dirname, '..', 'data', 'cloud.json'), JSON.stringify(out));
  console.log('merged', Object.keys(out.cases).join(', '));
  process.exit(0);
}
fs.mkdirSync(DIR, { recursive: true });
const g8 = P.makeGrid(8, 4e-3);

function tests() {
  // super-droplet convergence: one cell, no motion, against the collection equation with the same cut modes (s = 16)
  const sce = P.sceRun(P.makeGrid(16, 4e-3), A, ext, [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }], { dt: 0.5, tEnd: 1200, recordEvery: 1, trunc: 3 });
  const tq = (t, F, q) => { for (let i = 1; i < F.length; i++) if (F[i] >= q) return t[i - 1] + (q - F[i - 1]) / (F[i] - F[i - 1]) * (t[i] - t[i - 1]); return null; };
  const ref = [tq(sce.t, sce.F40, 0.5) / 60, tq(sce.t, sce.F40, 0.9) / 60], conv = [];
  for (const [nd, nc, seeds] of [[24, 8, 32], [96, 32, 32], [384, 128, 32], [1536, 512, 12]]) {
    const res = []; let ge = 0, gm = 0;
    for (let s = 1; s <= seeds; s++) {
      const c = P.makeCloud(A, ext, { seed: 5000 + s, Lx: 50, Lz: 50, h: 50, box: true, inside: () => true, perCell: [nd, nc], S: 0 });
      const T = [0], F = [c.census().M40 / c.M0];
      for (let k = 1; k <= 1500 && F[F.length - 1] < 0.9; k++) { c.step(1); T.push(k); F.push(c.census().M40 / c.M0); }
      res.push([tq(T, F, 0.5) / 60, tq(T, F, 0.9) / 60]); ge += c.gamEvents; gm += c.gamMany;
    }
    const m = i => res.reduce((a, r) => a + r[i], 0) / res.length, se = i => Math.sqrt(res.reduce((a, r) => a + (r[i] - m(i)) ** 2, 0) / (res.length - 1) / res.length);
    conv.push({ per: nd + nc, seeds, t50: [m(0), se(0)], t90: [m(1), se(1)], bias50: m(0) / ref[0] - 1, bias90: m(1) / ref[1] - 1, se90: se(1) / ref[1], gamMany: gm / ge });
    console.log(`box, ${nd + nc} per cell, ${seeds} seeds: t50 ${m(0).toFixed(3)} ± ${se(0).toFixed(3)}, t90 ${m(1).toFixed(3)} ± ${se(1).toFixed(3)} min (equation ${ref.map(v => v.toFixed(3)).join('/')}); t90 bias ${(100 * (m(1) / ref[1] - 1)).toFixed(1)} ± ${(100 * se(1) / ref[1]).toFixed(1)} %; collisions with gamma > 1: ${(100 * gm / ge).toFixed(1)} %`);
  }
  // well-mixed test: tiny drops (no fall) spread evenly over the whole slice, eps peaked in the core, the mean cell on; 4 seeds,
  // the variance of counts per 200 m x 100 m region over its Poisson value, at 30 and 120 min, with the full drift and with no drift
  const mix = {};
  for (const drift of ['full', 'none']) {
    const rows = [];
    for (let s = 1; s <= 4; s++) {
      const c = P.makeCloud(A, ext, { seed: 77 + s, shape: 'cumulus', inside2: null, perCell: [6, 0], modes: [{ N: 1, rg: 1e-9, sg: 1.0001 }, { N: 0, rg: 1e-9, sg: 1.0001 }], S: 0, peaked: true, eps: 4e-2, epsOut: 1e-3,
        noDrift: drift === 'none', uniformStart: true });
      const chi = () => { const H = new Float64Array(150); c.sd.forEach(q => { H[Math.min(14, Math.floor(q.z / 100)) * 10 + Math.min(9, Math.floor(q.x / 200))]++; }); const n = H.reduce((a, v) => a + v, 0), e = n / 150; return H.reduce((a, v) => a + (v - e) ** 2 / e, 0) / 149; };
      const row = []; for (let k = 1; k <= 7200; k++) { c.step(1); if (k === 1800 || k === 7200) row.push(chi()); } rows.push(row);
    }
    mix[drift] = { chi30: rows.map(r => r[0]), chi120: rows.map(r => r[1]) };
    console.log(`well-mixed, drift ${drift}: chi^2 per region at 30 min ${mix[drift].chi30.map(v => v.toFixed(2)).join(', ')}; at 120 min ${mix[drift].chi120.map(v => v.toFixed(2)).join(', ')} (Poisson 1 ± 0.12)`);
  }
  return { box: { ref, conv }, mix };
}

const base = { shape: 'cumulus', W0: 1, Le: 100, eps: 1e-2 };
const CASES = {
  column: { cfg: { shape: 'cumulus', W0: 0, stochastic: false, S: 0 }, seeds: 4 },
  evap: { cfg: { shape: 'cumulus', W0: 0, stochastic: false }, seeds: 4 },
  cell: { cfg: { shape: 'cumulus', W0: 1, stochastic: false }, seeds: 4 },
  reference: { cfg: base, seeds: 4, detail: true },
  Le50: { cfg: Object.assign({}, base, { Le: 50 }), seeds: 4 },
  Le200: { cfg: Object.assign({}, base, { Le: 200 }), seeds: 4 },
  peaked: { cfg: Object.assign({}, base, { peaked: true, eps: 4e-2, epsOut: 1e-3 }), seeds: 4 },
  peakedAyala: { cfg: Object.assign({}, base, { peaked: true, eps: 4e-2, epsOut: 1e-3, kernelEps: true }), seeds: 4 },
  noVent: { cfg: Object.assign({}, base, { vent: false }), seeds: 4 },
  box: { cfg: Object.assign({}, base, { shape: 'box' }), seeds: 2 },
  disc: { cfg: Object.assign({}, base, { shape: 'disc' }), seeds: 2 },
  tower: { cfg: Object.assign({}, base, { shape: 'tower' }), seeds: 2 },
  rough0: { cfg: Object.assign({}, base, { shape: 'random', outline: { rough: 0 } }), outlines: [1, 2, 3], seeds: 2 },
  rough3: { cfg: Object.assign({}, base, { shape: 'random', outline: { rough: 0.3 } }), outlines: [1, 2, 3], seeds: 2 },
  rough6: { cfg: Object.assign({}, base, { shape: 'random', outline: { rough: 0.6 } }), outlines: [1, 2, 3], seeds: 2 },
};

function regionMaxent(spec) {   // a region's spectrum (number per bin of the s = 8 grid) against its best gamma
  const N = new Float64Array(g8.n); for (const b in spec) { const k = +b; if (k >= 0 && k < g8.n) N[k] += spec[b]; }
  const tot = N.reduce((a, v) => a + v, 0); if (tot <= 0) return null;
  const me = P.maxentCompare(g8, N, { N: 0, M: 0 }); return [r4(me.epsExp), r4(me.epsGamma)];
}
function runCase(name) {
  const C = CASES[name], runs = [];
  const outlines = C.outlines || [null];
  for (const ol of outlines) for (let s = 1; s <= C.seeds; s++) {
    const cfg = Object.assign({}, C.cfg); if (ol !== null) cfg.outline = Object.assign({}, cfg.outline, { seed: ol });
    const ko = cfg.kernelEps ? Object.assign({}, ext, { eps: 'local' }) : ext, t0 = Date.now();
    const c = P.makeCloud(A, ko, Object.assign({ seed: 1000 + s, perCell: per }, cfg));
    let area = 0; for (let x = 2.5; x < 2000; x += 5) for (let z = 2.5; z < 1500; z += 5) if (c.inside(x, z)) area += 25;
    const perim = P.perimeter(c.inside, 2000, 1500);
    const rec = { t: [], M: [], M100: [], rain: [], evap: [], evapBelow: [] }, regs = [];
    const census = () => { const z = c.census(); rec.t.push(z.t); rec.M.push(r4(z.M / c.M0)); rec.M100.push(r4(z.M100 / c.M0)); rec.rain.push(r4(z.rain / c.M0)); rec.evap.push(r4(z.evap / c.M0)); rec.evapBelow.push(r4(z.evapBelow / c.M0)); };
    const snaps = {}, detail = C.detail && s === 1;
    const regRec = () => { const rc = c.regionCensus(); regs.push({ t: c.t, W: Array.from(rc.W, v => r4(v / c.M0)), maxent: rc.spec.map(regionMaxent),
      mergers: Array.from(c.led.mergers, r4), eaten: Array.from(c.led.eaten, v => r4(v / c.M0)), released: Array.from(c.led.released, r4) }); };
    census(); if (detail) { regRec(); snaps[0] = c.sd.filter((_, i) => i % 6 === 0).map(d => [Math.round(d.x), Math.round(d.z), +(d.r * 1e6).toFixed(1)]); }
    for (let k = 1; k <= tEnd; k++) {
      c.step(1);
      if (k % 30 === 0) census();
      if (detail && k % 300 === 0) regRec();
      if (detail && [600, 1200, 1800, 2700].includes(k)) snaps[k] = c.sd.filter((_, i) => i % 6 === 0).map(d => [Math.round(d.x), Math.round(d.z), +(d.r * 1e6).toFixed(1)]);
    }
    const i = rec.t.length - 1, rainBig = c.rainLog.filter(q => q[2] >= 100e-6);
    const fateC = {}; if (detail) for (const key in c.fate.initC) fateC[key] = [r4(c.fate.initC[key] / c.M0), r4((c.fate.rainC[key] || 0) / c.fate.initC[key]), r4((c.fate.evapC[key] || 0) / c.fate.initC[key])];
    const bornW = c.bornLog.reduce((a, b) => a + b[3], 0), bornCore = c.bornLog.filter(b => c.regionAt(b[0], b[1]) === 0).reduce((a, b) => a + b[3], 0);
    let coreArea = 0, inArea = 0; for (let q = 0; q < c.reg.length; q++) { if (c.reg[q] <= 2) inArea++; if (c.reg[q] === 0) coreArea++; }
    runs.push({ seed: 1000 + s, outline: ol, area, perim, M0: c.M0, rec, first100: c.first100, firstRain: rainBig.length ? rainBig[0][0] : null,
      rain: rec.rain[i], evap: rec.evap[i], evapBelow: rec.evapBelow[i], aloft: rec.M[i], gamMany: c.gamMany / Math.max(1, c.gamEvents),
      bornCoreShare: bornW > 0 ? bornCore / bornW : null, coreAreaShare: coreArea / inArea, nBorn: c.bornLog.length,
      initR: Array.from(c.initR, v => r4(v / c.M0)), rainR: Array.from(c.fate.rainR, v => r4(v / c.M0)), evapR: Array.from(c.fate.evapR, v => r4(v / c.M0)),
      regs: detail ? regs : undefined, fateC: detail ? fateC : undefined, snaps: detail ? snaps : undefined,
      born: detail ? c.bornLog.map(b => [b[0], b[1], b[2]]) : undefined });
    console.log(`${name} outline ${ol} seed ${1000 + s} [${((Date.now() - t0) / 1000).toFixed(0)} s]: area ${(area / 1e6).toFixed(3)} km2, edge/area ${(perim / area * 1000).toFixed(2)}/km; rain ${(100 * rec.rain[i]).toFixed(1)} %, evaporated ${(100 * rec.evap[i]).toFixed(1)} % (below base ${(100 * rec.evapBelow[i]).toFixed(1)}), aloft ${(100 * rec.M[i]).toFixed(1)} %; first drizzle at the ground ${rainBig.length ? (rainBig[0][0] / 60).toFixed(1) : '-'} min; drizzle born in the core ${bornW ? (100 * bornCore / bornW).toFixed(1) : '-'} % (water-weighted), core area ${(100 * coreArea / inArea).toFixed(1)} %`);
  }
  return { cfg: C.cfg, runs };
}
for (const name of process.argv.slice(2)) {
  const out = name === 'tests' ? tests() : runCase(name);
  fs.writeFileSync(path.join(DIR, name + '.json'), JSON.stringify(out));
}
