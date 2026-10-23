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
  const Wd = 520, H = 400, sc = 68, cx = Wd / 2, cz = H * 0.42, parts = [`<svg class="chart" viewBox="0 0 ${Wd} ${H + 64}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="droplet paths around a 40 micrometre collector"><rect width="${Wd}" height="${H + 64}" fill="#fff"/><g transform="translate(0 38)"><rect width="${Wd}" height="${H}" fill="#fff" stroke="#ece3d2"/>`];
  [0.15, 0.35, 0.55, 0.75, 0.95, 1.15, 1.35, 1.55].map(f => f * (1 + p)).forEach(b => {
    const q = P.trajPath('stokes', St, S, p, b, 6, 3.2), col = q.hit ? '#7d1d2f' : '#33627f';
    for (const sg of [1, -1]) parts.push(`<polyline fill="none" stroke="${col}" stroke-width="1.6" points="${q.x.map((x, i) => (cx + sg * x * sc).toFixed(1) + ',' + (cz - q.z[i] * sc).toFixed(1)).join(' ')}"/>`);
  });
  parts.push(`<circle cx="${cx}" cy="${cz}" r="${sc}" fill="#e1ebf0" stroke="#23160f" stroke-width="1.5"/><circle cx="${cx}" cy="${cz}" r="${sc * (1 + p)}" fill="none" stroke="#6f665e" stroke-dasharray="3 3"/>`);
  parts.push(`</g><text x="12" y="15" class="tick">collector R = 40 µm, droplet r = 8 µm, St = ${St.toFixed(2)}</text><text x="12" y="31" class="tick">air rises past the collector; droplets come from below</text><text x="12" y="${H + 56}" class="tick">wine: touches · blue: carried round · dashed: contact at R + r</text></svg>`);
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

process.stdout.write(JSON.stringify(figs));
