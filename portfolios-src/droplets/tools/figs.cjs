// The lecture notes' figures, drawn at build time from the model (physics.cjs) and the stored runs (data/*.json).
// Prints a JSON object {name: svg}; build.py replaces {{FIG:name}} in the text with the SVG.
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs'), C = require('../chart.cjs');
const D = n => JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', n + '.json')));
const A = P.air(283.15, 85000), A20 = P.air(293.15, 101325);
const figs = {};
const range = (a, b, n, log) => Array.from({ length: n }, (_, i) => log ? a * Math.pow(b / a, i / (n - 1)) : a + (b - a) * i / (n - 1));

// 1. fall speed against diameter, 20 C and 1013 hPa, with Gunn and Kinzer's measurements
const GK = [[0.1, 27], [0.2, 72], [0.3, 117], [0.4, 162], [0.5, 206], [0.6, 247], [0.7, 287], [0.8, 327], [0.9, 367], [1.0, 403], [1.2, 464], [1.4, 517], [1.6, 565], [1.8, 609], [2.0, 649], [2.4, 727], [2.8, 782], [3.2, 826], [3.6, 860], [4.0, 883], [4.6, 903], [5.2, 912], [5.8, 917]];
const dd = range(0.01, 6, 160, true);
figs.fallspeed = C.line({ id: 'f1', w: 600, h: 330, xlog: true, ylog: true, xmin: 0.01, xmax: 6, ymin: 0.003, ymax: 20, xlabel: 'drop diameter d (mm)', ylabel: 'terminal speed (m/s)', series: [
  { x: dd, y: dd.map(d => P.vStokes(d / 2e3, A20)), label: 'Stokes (L0)', color: '#6f665e', dash: '5 4' },
  { x: dd, y: dd.map(d => P.vBeard(d / 2e3, A20)), label: 'drag balance, Beard (L1)', color: '#7d1d2f' },
  { x: GK.map(q => q[0]), y: GK.map(q => q[1] / 100), label: 'measured, Gunn and Kinzer 1949', color: '#33627f', dots: true }] });

// 2. one collector in an open cloud: radius against time
function grow(vlaw, W, tEnd) {
  const r = 8e-6, xs = [0], ys = [40]; let R = 40e-6, t = 0, dt = 0.5;
  while (t < tEnd && R < 200e-6) {
    const f = RR => W * Math.pow(RR + r, 2) * (vlaw(RR) - vlaw(r)) / (4 * 1000 * RR * RR);
    const k1 = f(R), k2 = f(R + dt / 2 * k1), k3 = f(R + dt / 2 * k2), k4 = f(R + dt * k3);
    R += dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += dt;
    if (Math.round(t / dt) % 20 === 0) { xs.push(t / 60); ys.push(R * 1e6); }
  }
  return { x: xs, y: ys };
}
const W = 300e6 * P.massOf(8e-6);
const gS = grow(a => P.vStokes(a, A), W, 1500), gB = grow(a => P.vBeard(a, A), W, 1500);
const tb = range(0, 21, 200);
figs.growth = C.line({ id: 'f2', w: 600, h: 320, xmin: 0, xmax: 20, ymin: 40, ymax: 200, xlabel: 'time (min)', ylabel: 'collector radius R (µm)', series: [
  { x: tb, y: tb.map(t => P.L0radius(t * 60, 40e-6, W, A) * 1e6), label: 'Stokes, r ≪ R (blows up at 21.1 min)', color: '#6f665e', dash: '5 4' },
  { x: gS.x, y: gS.y, label: 'Stokes, droplet radius 8 µm', color: '#c9783f' },
  { x: gB.x, y: gB.y, label: 'drag balance (L1), 8 µm', color: '#7d1d2f' }], hlines: [{ y: 100, label: '100 µm' }] });

// 3. droplet paths around a 40 um collector (creeping flow), drawn like the simulation panel
(function () {
  const R = 40e-6, r = 8e-6, U = P.vBeard(R, A), vr = P.vBeard(r, A), gs = P.G0 * (1 - A.rho / 1000), St = vr / gs * U / R, S = vr / U, p = r / R;
  const Wd = 520, H = 400, sc = 68, cx = Wd / 2, cz = H * 0.42, parts = [`<svg class="chart" viewBox="0 0 ${Wd} ${H + 64}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="droplet paths around a 40 micrometre collector"><rect width="${Wd}" height="${H + 64}" fill="#fff"/><defs><clipPath id="f3clip"><rect width="${Wd}" height="${H}"/></clipPath></defs><g transform="translate(0 38)"><rect width="${Wd}" height="${H}" fill="#fff" stroke="#ece3d2"/><g clip-path="url(#f3clip)">`];
  [0.15, 0.35, 0.55, 0.75, 0.95, 1.15, 1.35, 1.55].map(f => f * (1 + p)).forEach(b => {
    const q = P.trajPath('stokes', St, S, p, b, 6, 3.2), col = q.hit ? '#7d1d2f' : '#33627f';
    for (const sg of [1, -1]) parts.push(`<polyline fill="none" stroke="${col}" stroke-width="1.6" points="${q.x.map((x, i) => (cx + sg * x * sc).toFixed(1) + ',' + (cz - q.z[i] * sc).toFixed(1)).join(' ')}"/>`);
  });
  parts.push(`<circle cx="${cx}" cy="${cz}" r="${sc}" fill="#e1ebf0" stroke="#23160f" stroke-width="1.5"/><circle cx="${cx}" cy="${cz}" r="${sc * (1 + p)}" fill="none" stroke="#6f665e" stroke-dasharray="3 3"/>`);
  parts.push(`</g></g><text x="12" y="15" class="tick">collector R = 40 µm, droplet r = 8 µm, St = ${St.toFixed(2)}</text><text x="12" y="31" class="tick">air rises past the collector; droplets come from below</text><text x="12" y="${H + 56}" class="tick">wine: touches · blue: carried round · dashed: contact at R + r</text></svg>`);
  figs.paths = parts.join('');
})();

// 4. collision efficiency against size ratio, this study against Hall (1980)
const tab = D('etab_warm'), hall = D('hall1980'), ps = range(0.02, 0.6, 60);
const effSeries = [];
[[30, '#c9783f'], [40, '#7d1d2f'], [60, '#33627f'], [100, '#3c6a46']].forEach(([Rum, col]) => {
  effSeries.push({ x: ps, y: ps.map(p => P.tableE(tab, Rum * 1e-6, p)), label: `R = ${Rum} µm, this study`, color: col });
  const row = hall.E[hall.R.indexOf(Rum)];
  effSeries.push({ x: hall.p.slice(0, 12), y: row.slice(0, 12), color: col, dots: true, r: 2.5 });
});
figs.efficiency = C.line({ id: 'f4', w: 600, h: 330, xmin: 0, xmax: 0.6, ymin: 0, ymax: 1.02, xlabel: 'size ratio p = r/R', ylabel: 'collision efficiency E', series: effSeries, legendAt: 'bottomright' });

// 5. the warm cloud: F40 against time, two kernels, two bookkeepings, and Hall's efficiencies
const w = D('warm'), m = t => t.map(s => s / 60);
figs.warm = C.line({ id: 'f5', w: 600, h: 330, xmin: 0, xmax: 30, ymin: 0, ymax: 1, xlabel: 'time (min)', ylabel: 'water in drops r ≥ 40 µm, F₄₀', series: [
  { x: m(w.thesis.t), y: w.thesis.F40, label: 'thesis kernel, SCE', color: '#6f665e' },
  { x: m(w.thesis.gce.t), y: w.thesis.gce.F40, label: 'thesis kernel, GCE', color: '#6f665e', dash: '5 4' },
  { x: m(w.extended.t), y: w.extended.F40, label: 'extended kernel, SCE', color: '#7d1d2f' },
  { x: m(w.extended.gce.t), y: w.extended.gce.F40, label: 'extended kernel, GCE', color: '#7d1d2f', dash: '5 4' },
  { x: m(w.extHall.t), y: w.extHall.F40, label: 'extended, Hall’s efficiencies', color: '#33627f', dash: '2 3' }],
  hlines: [{ y: 0.5 }, { y: 0.9 }] });

// 6. mass spectra of the extended run
const g = P.makeGrid(8, 4e-3), ru = g.r.map(r => r * 1e6), spec = N => N.map((n, k) => n * g.x[k] / g.dlnr * 1e3);
figs.spectra = C.line({ id: 'f6', w: 600, h: 300, xlog: true, xmin: 2, xmax: 4000, ymin: 0, xlabel: 'radius r (µm)', ylabel: 'g = dM/d ln r (g/m³)',
  series: [[0, '#6f665e', 'start'], [600, '#c9783f', '10 min'], [1200, '#7d1d2f', '20 min'], [1800, '#33627f', '30 min']].map(([t, c, l]) => ({ x: ru, y: spec(w.extended.snaps[t]), label: l, color: c })) });

// 7. Golovin test: numerical against exact at 60 min, 2 and 8 bins per doubling
(function () {
  const b = 1.5, mbar = P.massOf(10e-6), L = 1e-3, N0 = L / mbar, s8 = [];
  [[2, '#c9783f'], [8, '#7d1d2f']].forEach(([s, col]) => {
    const gr = P.makeGrid(s, 4e-3), n = gr.n, wb = Math.LN2 / s, K = new Float64Array(n * n);
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) K[i * n + j] = b * (gr.x[i] + gr.x[j]);
    const Nb = Float64Array.from(gr.x.map(x => N0 / mbar * Math.exp(-x / mbar) * x * wb));
    const res = P.sceRun(gr, null, null, null, { K, N0: Nb, dt: 1, tEnd: 3600, recordEvery: 3600, snapAt: [3600] });
    s8.push({ x: gr.r.map(r => r * 1e6), y: res.snaps[3600].map((N, k) => N * gr.x[k] / (gr.dlnr) * 1e3), label: `${s} bins per doubling`, color: col });
  });
  const rr = range(5, 3000, 300, true);
  s8.push({ x: rr, y: rr.map(r => { const x = P.massOf(r * 1e-6); return P.golovinDensity(x, 3600, b, N0, mbar) * x * x * 3 * 1e3; }), label: 'exact (Golovin)', color: '#23160f', dash: '5 4' });
  figs.golovin = C.line({ id: 'f7', w: 600, h: 300, xlog: true, xmin: 5, xmax: 3000, ymin: 0, xlabel: 'radius r (µm)', ylabel: 'g = dM/d ln r (g/m³)', series: s8 });
})();

// 8. ensemble-mean F40 against the volume, and the SCE (truncated modes)
const st = D('stochastic'), br = D('bridge').s16;
const sF = [];
[['1', '#c9783f'], ['10', '#3c6a46'], ['100', '#33627f'], ['1000', '#7d1d2f']].forEach(([V, c]) => {
  const runs = st.V[V], n = runs.length;
  sF.push({ x: runs[0].F40.map((_, i) => i), y: runs[0].F40.map((_, i) => runs.reduce((a, r) => a + r.F40[i], 0) / n), label: `${V} cm³ (${n} runs)`, color: c });
});
sF.push({ x: m(br.t), y: br.F40, label: 'SCE (mean field)', color: '#23160f', dash: '5 4' });
figs.luckF40 = C.line({ id: 'f8', w: 600, h: 310, xmin: 0, xmax: 25, ymin: 0, ymax: 1, xlabel: 'time (min)', ylabel: 'mean water in drops r ≥ 40 µm', series: sF });

// 9. first 100 um drop: share of volumes that have one, exact runs against the SCE's Poisson bridge
// (6.1) with the largest n100 reached so far: later the large drops merge with each other and their number falls, but a volume
// that once held one has had its first drop
const nmax = []; br.N100.reduce((mx, N, i) => (nmax[i] = Math.max(mx, N)), 0);
const sC = [];
[['10', '#3c6a46'], ['100', '#33627f'], ['1000', '#7d1d2f']].forEach(([V, c]) => {
  const t = st.V[V].map(r => r.t100).filter(x => x !== null).sort((a, b) => a - b), n = st.V[V].length;
  sC.push({ x: [0].concat(t.map(x => x / 60)), y: [0].concat(t.map((_, i) => (i + 1) / n)), label: `${V} cm³, exact (${n} runs)`, color: c });
  sC.push({ x: m(br.t), y: nmax.map(N => 1 - Math.exp(-(+V) * 1e-6 * N)), color: c, dash: '4 3', width: 1.5 });
});
sC.push({ x: m(br.t), y: nmax.map(N => 1 - Math.exp(-N)), label: '1 m³, Poisson (6.1)', color: '#23160f', dash: '4 3', width: 1.5 });
figs.first = C.line({ id: 'f9', w: 600, h: 310, xmin: 0, xmax: 20, ymin: 0, ymax: 1, xlabel: 'time (min)', ylabel: 'share of volumes with a drop r ≥ 100 µm', series: sC, legendAt: 'bottomright' });

// 10. coalescence efficiency (4.2) for a collector R meeting a drop R/2, with drag-balance and with Stokes speeds
(function () {
  const Rs = range(20e-6, 2e-3, 120, true), sig = P.sigmaWater(A.T);
  const E = v => Rs.map(R => P.eCoal(R, R / 2, Math.abs(v(R) - v(R / 2)), sig));
  figs.coal = C.line({ id: 'f10', w: 600, h: 300, xlog: true, xmin: 0.02, xmax: 2, ymin: 0, ymax: 1.02, xlabel: 'collector radius R (mm), partner R/2', ylabel: 'coalescence efficiency', series: [
    { x: Rs.map(R => R * 1e3), y: E(a => P.vBeard(a, A)), label: 'drag-balance speeds (chapter 2)', color: '#7d1d2f' },
    { x: Rs.map(R => R * 1e3), y: E(a => P.vStokes(a, A)), label: "Stokes speeds (the thesis kernel)", color: '#6f665e', dash: '5 4' }] });
})();
// 11. turbulent gain of the 40/8 um kernel (Ayala et al. 2008, inside its range) against the dissipation rate
(function () {
  const es = range(1.5e-4, 5e-2, 80, true);
  figs.turb = C.line({ id: 'f11', w: 600, h: 300, xlog: true, xmin: 1.5e-4, xmax: 5e-2, ymin: 0, ymax: 35, xlabel: 'dissipation rate ε (m²/s³)', ylabel: 'kernel raised by (%)', series: [
    { x: es, y: es.map(e => (P.ayalaFactor(40e-6, 8e-6, A, e) - 1) * 100), label: '40 µm collector, 8 µm droplet', color: '#33627f' }] });
})();

// ---------------------------------------------------------------- L8: energy, entropy and who eats whom (data/energy.json)
(function () {
  const E = D('energy'), wr = E.warm.recs, tm = wr.map(q => q.t / 60);
  // 12. energy flows: surface energy released by merging, and gravity's work dissipated by drag, per m^3 of air
  const rel = wr.map((q, i) => i === 0 ? null : (wr[i - 1].Es - q.Es) / (q.t - wr[i - 1].t));
  figs.energyflow = C.line({ id: 'f12', w: 600, h: 320, ylog: true, xmin: 0, xmax: 30, ymin: 1e-8, ymax: 0.1, xlabel: 'time (min)', ylabel: 'power per m³ of cloud (W/m³)', series: [
    { x: tm.slice(1), y: rel.slice(1), label: 'surface energy released by merging', color: '#7d1d2f' },
    { x: tm, y: wr.map(q => q.Pg), label: 'gravity’s work turned to heat by drag', color: '#33627f' },
    { x: [0, 30], y: [E.warm.rhoEps || 1.0458e-2, E.warm.rhoEps || 1.0458e-2], label: 'turbulence, ρₐε at ε = 10⁻² m²/s³', color: '#6f665e', dash: '5 4' }] });
  // 13. the three populations: share of the water in droplets, collectors and drizzle
  const W0 = E.warm.W0, cols = ['#33627f', '#c9783f', '#7d1d2f'];
  figs.populations = C.line({ id: 'f13', w: 600, h: 300, xmin: 0, xmax: 30, ymin: 0, ymax: 1, xlabel: 'time (min)', ylabel: 'share of the water', series:
    [0, 1, 2].map(c => ({ x: tm, y: wr.map(q => q.wat[c] / W0), label: ['droplets (r < 20 µm)', 'collectors (20–100 µm)', 'drizzle (r ≥ 100 µm)'][c], color: cols[c] })) });
  // 14. the diet: water eaten in each channel since the start, as a share of all the water
  const ch = [[1, 0, 'collectors ate droplets', '#c9783f', null], [2, 0, 'drizzle ate droplets', '#7d1d2f', null], [1, 1, 'collectors ate collectors', '#c9783f', '5 4'],
    [2, 1, 'drizzle ate collectors', '#7d1d2f', '5 4'], [2, 2, 'drizzle ate drizzle', '#7d1d2f', '2 3'], [0, 0, 'droplets ate droplets', '#33627f', null]];
  figs.diet = C.line({ id: 'f14', w: 600, h: 320, ylog: true, xmin: 0, xmax: 30, ymin: 1e-6, ymax: 2, xlabel: 'time (min)', ylabel: 'water eaten so far / all water', series:
    ch.map(([a, b, l, c, d]) => ({ x: tm, y: wr.map(q => q.eaten[a * 3 + b] / W0), label: l, color: c, dash: d })) });
  // 15. the spectrum at 6 min (half the water above 40 um) against the two maximum-entropy shapes with its number and water
  const g = P.makeGrid(E.s, 4e-3), ru = g.r.map(r => r * 1e6), q6 = wr.find(q => q.t === 360), toG = Mk => Mk.map(v => v / g.dlnr * 1e3);
  figs.maxent = C.line({ id: 'f15', w: 600, h: 300, xlog: true, xmin: 2, xmax: 1000, ymin: 0, xlabel: 'radius r (µm)', ylabel: 'g = dM/d ln r (g/m³)', series: [
    { x: ru, y: toG(q6.spec.N.map((n, k) => n * g.x[k])), label: 'the cloud at 6 min (chapter 5)', color: '#7d1d2f' },
    { x: ru, y: toG(q6.spec.Mexp), label: 'maximum entropy, same N and M', color: '#33627f', dash: '5 4' },
    { x: ru, y: toG(q6.spec.Mgamma), label: 'maximum entropy, also ⟨ln m⟩ (gamma)', color: '#3c6a46', dash: '2 3' }] });
  // 16. distance from the maximum-entropy shape as the number of drops falls: gravity's kernel against the constant kernel
  const byN = E.warm.epsByN.filter(r => r[0] > 0 && r[0] <= 1), cr = E.constant.rows;
  figs.maxentdist = C.line({ id: 'f16', w: 600, h: 310, xlog: true, xmin: 1e-4, xmax: 1, ymin: 0, ymax: 2, xlabel: 'drops left, N/N₀', ylabel: 'spectrum error ε (0 = same shape)', series: [
    { x: byN.map(r => r[0]), y: byN.map(r => r[1]), label: 'gravity, against the exponential', color: '#7d1d2f' },
    { x: byN.map(r => r[0]), y: byN.map(r => r[2]), label: 'gravity, against the gamma', color: '#7d1d2f', dash: '2 3' },
    { x: cr.map(r => r.f), y: cr.map(r => r.epsExp), label: 'every pair alike, exponential', color: '#33627f' },
    { x: cr.map(r => r.f), y: cr.map(r => r.epsGamma), label: 'every pair alike, gamma', color: '#33627f', dash: '2 3' }] });
  // 17. surface energy left against the share of drops merged, under three rules (100 cm^3, Monte Carlo means; steepest: one run)
  const mc = E.mc, xf = a => a.map(q => 1 - q.f);
  figs.rules = C.line({ id: 'f17', w: 600, h: 310, xmin: 0, xmax: 1, ymin: 0, ymax: 1, xlabel: 'share of the drops merged away, 1 − N/N₀', ylabel: 'surface energy left / at start', series: [
    { x: [0].concat(xf(mc.physical.agg)), y: [1].concat(mc.physical.agg.map(q => q.S)), label: 'gravity’s kernel (the cloud)', color: '#7d1d2f' },
    { x: [0].concat(xf(mc.constant.agg)), y: [1].concat(mc.constant.agg.map(q => q.S)), label: 'every pair alike (energy only)', color: '#33627f' },
    { x: [0].concat(mc.steepest.rows.map(q => 1 - q.f)), y: [1].concat(mc.steepest.rows.map(q => q.S)), label: 'largest pair first (steepest descent)', color: '#3c6a46', dash: '5 4' }] });
})();

// ---------------------------------------------------------------- L10: a cloud with a shape (data/cloud.json, tools/run_cloud.cjs)
(function () {
  let CL; try { CL = D('cloud'); } catch (e) { return; }
  if (!CL.cases || !CL.cases.reference) return;
  const Lx = 2000, Lz = 1500, W = 560, H = 420, H0 = 420, sx = x => 40 + x / Lx * W, sz = z => 14 + (1 - z / Lz) * H;
  function slice(id, inside, dots, note, extra) {
    const p = [`<svg class="chart" viewBox="0 0 ${W + 60} ${H + 70}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${note}"><rect width="${W + 60}" height="${H + 70}" fill="#fff"/>`];
    p.push(`<rect x="40" y="14" width="${W}" height="${H}" fill="#f4f8fa" stroke="#3f2c23"/>`);
    for (let i = 0; i < 80; i++) for (let j = 0; j < 60; j++) { const x = (i + 0.5) * 25, z = (j + 0.5) * 25; if (inside(x, z)) p.push(`<rect x="${sx(i * 25).toFixed(1)}" y="${sz((j + 1) * 25).toFixed(1)}" width="${(W / 80 + 0.4).toFixed(2)}" height="${(H / 60 + 0.4).toFixed(2)}" fill="#e1ebf0"/>`); }
    dots.forEach(d => p.push(`<circle cx="${sx(d[0]).toFixed(1)}" cy="${sz(d[1]).toFixed(1)}" r="${d[2]}" fill="${d[3]}"/>`));
    if (extra) p.push(extra);
    [0, 500, 1000, 1500, 2000].forEach(x => p.push(`<text x="${sx(x)}" y="${H + 30}" text-anchor="middle" class="tick">${x}</text>`));
    [0, 500, 1000, 1500].forEach(z => p.push(`<text x="34" y="${sz(z) + 4}" text-anchor="end" class="tick">${z}</text>`));
    p.push(`<text x="${40 + W / 2}" y="${H + 48}" text-anchor="middle" class="axl">x (m)</text><text transform="translate(12 ${14 + H / 2}) rotate(-90)" text-anchor="middle" class="axl">height z (m)</text>`);
    p.push(`<text x="40" y="${H + 64}" class="tick">${note}</text></svg>`);
    return p.join('');
  }
  const inside = P.shapeFn('cumulus', Lx, Lz), ref = CL.cases.reference.runs[0];
  // 18. the reference cloud at 20 min
  const sn = ref.snaps[1200], col = r => r >= 100 ? '#7d1d2f' : r >= 20 ? '#c9783f' : 'rgba(51,98,127,0.5)';
  figs.cloudsnap = slice('f18', inside, sn.map(d => [d[0], d[1], d[2] >= 100 ? 2.2 : d[2] >= 20 ? 1.5 : 0.9, col(d[2])]), 'blue: droplets · ochre: collectors · wine: drizzle ≥ 100 µm (one dot in six)');
  // 19. where drizzle is born: the place each super-droplet first reached 100 um, coloured by the time
  const born = CL.cases.reference.runs.flatMap(q => q.born), HB = {}, h = 50;
  born.forEach(b => { const k = Math.floor(b[0] / h) + ',' + Math.floor(b[1] / h); HB[k] = (HB[k] || 0) + 1; });
  const hmax = Math.max(...Object.values(HB)), cells = Object.keys(HB).map(k => { const [i, j] = k.split(',').map(Number); return [i, j, HB[k] / hmax]; });
  const shade = cells.map(([i, j, v]) => `<rect x="${sx(i * h).toFixed(1)}" y="${sz((j + 1) * h).toFixed(1)}" width="${(W * h / Lx).toFixed(2)}" height="${(H0 * h / Lz).toFixed(2)}" fill="#7d1d2f" fill-opacity="${(0.08 + 0.92 * v).toFixed(2)}"/>`).join('');
  const core = `<line x1="${sx(720)}" x2="${sx(720)}" y1="${sz(1350)}" y2="${sz(300)}" stroke="#23160f" stroke-dasharray="4 3"/><line x1="${sx(1280)}" x2="${sx(1280)}" y1="${sz(1350)}" y2="${sz(300)}" stroke="#23160f" stroke-dasharray="4 3"/>`;
  figs.cloudwhere = slice('f19', inside, [], 'where drops first reach 100 µm (3 runs, darker = more); dashed: the updraft core', '<g>' + shade + core + '</g>');
  // 20. rain at the ground: share of the water rained out, for each case (mean of the runs)
  const cases = [['reference', 'cumulus, wind and eddies', '#7d1d2f', null], ['noStochastic', 'no stochastic element', '#7d1d2f', '5 4'], ['stillAir', 'still air, eddies only', '#6f665e', null],
    ['peakedEps', 'eddies strongest in the core', '#9a5b8f', '2 3'], ['box', 'box', '#33627f', null], ['disc', 'disc', '#3c6a46', null], ['tower', 'tall tower', '#c9783f', null]];
  const ser = [];
  cases.forEach(([k, l, c, d]) => { const R = CL.cases[k]; if (!R) return; const runs = R.runs, t = runs[0].rec.t.map(v => v / 60);
    ser.push({ x: t, y: t.map((_, i) => runs.reduce((a, q) => a + q.rec.rain[i], 0) / runs.length), label: l, color: c, dash: d }); });
  figs.cloudrain = C.line({ id: 'f20', w: 600, h: 320, xmin: 0, xmax: 45, ymin: 0, xlabel: 'time (min)', ylabel: 'share of the water rained out', series: ser });
  const ev = [];
  cases.forEach(([k, l, c, d]) => { const R = CL.cases[k]; if (!R) return; const runs = R.runs, t = runs[0].rec.t.map(v => v / 60);
    ev.push({ x: t, y: t.map((_, i) => runs.reduce((a, q) => a + q.rec.evap[i], 0) / runs.length), label: l, color: c, dash: d }); });
  figs.cloudevap = C.line({ id: 'f21', w: 600, h: 320, xmin: 0, xmax: 45, ymin: 0, xlabel: 'time (min)', ylabel: 'share of the water evaporated in clear air', series: ev });
})();
process.stdout.write(JSON.stringify(figs));
