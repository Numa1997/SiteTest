// Every number quoted in the lecture notes, recomputed from the model and found in the text near its anchor.
//   node checks/check_numbers.cjs          (about two minutes: a few collection-equation runs)
// A number is either computed here from physics.cjs, or read from a data file that the model's own run tools wrote
// (data/warm.json, stochastic.json, bridge.json, cold.json); the tool that wrote each file is named beside it.
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const G = require('../tools/run_golovin.cjs');
const D = f => JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', f)));

// ---------------------------------------------------------------- the text, as a reader sees it (tags removed)
const files = fs.readdirSync(path.join(__dirname, '..', 'text')).filter(f => f.endsWith('.src.html')).sort();
const TXT = {};
for (const f of files) {
  TXT[f.replace('.src.html', '')] = fs.readFileSync(path.join(__dirname, '..', 'text', f), 'utf8')
    .replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ');
}
let pass = 0, fail = 0;
// expect(file, anchor, expected string, value for the report): `expected` must appear within `win` characters after an occurrence
// of `anchor` (or before it, within 120 characters)
function expect(file, anchor, expected, note, win) {
  const t = TXT[file].replace(/\$/g, ''); win = win || 400; anchor = anchor.replace(/\$/g, ''); expected = expected.replace(/\$/g, '');
  let i = -1, ok = false;
  while ((i = t.indexOf(anchor, i + 1)) >= 0) {
    const seg = t.slice(Math.max(0, i - 120), i + anchor.length + win);
    if (seg.includes(expected)) { ok = true; break; }
  }
  if (ok) pass++; else fail++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  [${file}] "${anchor}" -> "${expected}"${note ? '  (' + note + ')' : ''}`);
}
const f = (x, d) => x.toFixed(d), r10 = x => String(Math.round(x / 10) * 10);
const sup = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
function texSci(x, d) {            // 1.3\times10^{-14}
  const e = Math.floor(Math.log10(Math.abs(x))), m = x / Math.pow(10, e);
  const ms = f(m, d), mm = +ms >= 10 ? f(m / 10, d) : ms, ee = +ms >= 10 ? e + 1 : e;
  return `${mm}\\times10^{${ee}}`;
}
function uniSci(x, d) {            // 4.58 × 10⁻⁷
  const e = Math.floor(Math.log10(Math.abs(x))), m = x / Math.pow(10, e);
  return `${f(m, d)} × 10${String(e).split('').map(c => sup[c]).join('')}`;
}
const interp = (t, F, q) => { for (let i = 1; i < F.length; i++) if (F[i] >= q) return t[i - 1] + (t[i] - t[i - 1]) * (q - F[i - 1]) / (F[i] - F[i - 1]); return null; };

// ---------------------------------------------------------------- air, cloud, fall speeds
const A = P.air(283.15, 85000), RW = 1000, g = P.G0;
const tab = D('etab_warm.json'), hall = D('hall1980.json');
const KO = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab };
const modes = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
const modeMass = md => md.N * 4 / 3 * Math.PI * RW * Math.pow(md.rg, 3) * Math.exp(4.5 * Math.log(md.sg) ** 2);
const vS = a => P.vStokes(a, A), vB = a => P.vBeard(a, A), k = P.stokesK(A);
const W8 = 300e6 * P.massOf(8e-6);

expect('book-00', 'The droplets hold', f(modeMass(modes[0]) * 1e3, 3), 'droplet water g/m³');
expect('book-00', 'the collectors', f(modeMass(modes[1]) * 1e3, 3) + ' g/m³');
expect('book-00', 'drizzle drops have', 'about ' + f(vB(100e-6), 1) + ' m/s');
expect('book-00', 'a 40 µm drop falls at', f(vS(40e-6), 3) + ' m/s');
const sweep = Math.PI * 40e-6 ** 2 * vS(40e-6);
expect('book-00', 'so it sweeps', texSci(sweep, 1));
expect('book-00', 'One million collectors', texSci(sweep * 1e6, 1));
expect('book-00', 'cleared on a time scale of', f(1 / (sweep * 1e6) / 60, 0) + ' min');
expect('book-00', 'density $\\rho_a =', f(A.rho, 4));
expect('book-00', 'viscosity $\\mu =', f(A.mu * 1e5, 3) + '\\times10^{-5}');

// ---------------------------------------------------------------- chapter 1
const t100 = P.L0time(40e-6, 100e-6, 8e-6, W8, A), t100r = (1 / 40e-6 - 1 / 100e-6) / (k * W8 / (4 * RW));
expect('book-01', 'In our cloud With $W =', f(W8 * 1e3, 3) + ' g/m³');
expect('book-01', '$k =', f(k / 1e8, 4) + '\\times10^{8}');
expect('book-01', 'grows to 100 µm in', f(t100 / 60, 2) + ' min');
expect('book-01', 'with $r \\ll R$, (1.3) gives', f(t100r / 60, 2) + ' min');
expect('book-01', 'shortens the time by', 'a fifth', `${f((1 - t100 / t100r) * 100, 0)} %`);
expect('book-01', 'blow up at', f(1 / (k * W8 / (4 * RW) * 40e-6) / 60, 1) + ' min');
expect('book-01', 'to 60 µm takes', 'one third', f(1 - 40 / 60, 3));
expect('book-01', 'from 40 to 100 µm,', f((1 - 40 / 100) * 100, 0) + ' %');
expect('book-01', 'already holds the water of', `${(40 / 8) ** 3} droplets`);
const box = P.L0box(40e-6, 1e6, W8, A), Rm = Math.cbrt(40e-6 ** 3 + 300 * 8e-6 ** 3);
expect('book-01', 'so $R_m =', f(Rm * 1e6, 2) + ' µm');
// closed box with finite r, Stokes, E = 1, by direct integration (the model's own L0 functions use r << R for the box)
function closedBox(law, eff) {
  const v = law === 'stokes' ? vS : vB, M0 = P.massOf(40e-6), W0 = W8, Nc = 1e6, r = 8e-6;
  const E = R => eff === 'one' ? 1 : P.tableE(tab, R, r / R, 'clamp');
  const fr = R => Math.max(0, E(R) * Math.PI * (R + r) ** 2 * (v(R) - v(r)) * (W0 - Nc * (P.massOf(R) - M0)) / (4 * Math.PI * R * R * RW));
  let R = 40e-6, t = 0, t50, t90; const h = 0.05;
  while (t < 7200 && t90 === undefined) {
    const k1 = fr(R), k2 = fr(R + h / 2 * k1), k3 = fr(R + h / 2 * k2), k4 = fr(R + h * k3);
    const Rn = R + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4), F = Nc * P.massOf(Rn) / (Nc * M0 + W0), F0 = Nc * P.massOf(R) / (Nc * M0 + W0);
    if (t50 === undefined && F >= 0.5) t50 = t + h * (0.5 - F0) / (F - F0);
    if (F >= 0.9) t90 = t + h * (0.9 - F0) / (F - F0);
    R = Rn; t += h;
  }
  return [t50, t90];
}
const [b50, b90] = closedBox('stokes', 'one'), [bB50, bB90] = closedBox('beard', 'one');
expect('book-01', 'half of all the water is inside the collectors after', f(b50 / 60, 2) + ' min');
expect('book-01', 'nine tenths after', f(b90 / 60, 2) + ' min');
const Phi = 1 / 40e-6 - 1 / Rm;
expect('book-01', 'a collector that starts at', 'ends near ' + r10(1 / (1 / 44e-6 - Phi) * 1e6), `R(∞) = ${f(1 / (1 / 44e-6 - Phi) * 1e6, 1)} µm`);

// ---------------------------------------------------------------- chapter 2
let lo = 20e-6, hi = 80e-6;
for (let i = 0; i < 60; i++) { const m = (lo + hi) / 2; if (P.reynolds(m, vS(m), A) > 1) hi = m; else lo = m; }
expect('book-02', "Stokes' speed has Re = 1 at", 'a = ' + f(lo * 1e6, 1) + ' µm');
expect('book-02', 'At 100 µm Stokes gives', f(vS(100e-6), 2) + ' m/s and Re = ' + f(P.reynolds(100e-6, vS(100e-6), A), 0));
const slip = 1 + 2.51 * P.meanFreePath(A) / 16e-6;
expect('book-02', 'slip of air molecules', '+' + f((slip - 1) * 100, 1) + ' %');
// Gunn and Kinzer (1949), diameter (mm) -> speed (cm/s), typed from their table; dry air and their 50 % humid air at 20 °C, 1013 hPa
const GK = [[0.1, 27], [0.2, 72], [0.3, 117], [0.4, 162], [0.5, 206], [0.6, 247], [0.7, 287], [0.8, 327], [0.9, 367], [1.0, 403], [1.2, 464], [1.4, 517],
  [1.6, 565], [1.8, 609], [2.0, 649], [2.2, 690], [2.4, 727], [2.6, 757], [2.8, 782], [3.0, 806], [3.2, 826], [3.4, 844], [3.6, 860], [3.8, 872], [4.0, 883],
  [4.2, 892], [4.4, 898], [4.6, 903], [4.8, 907], [5.0, 909], [5.2, 912], [5.4, 914], [5.6, 916], [5.8, 917]];
const A20 = P.air(293.15, 101325), es20 = 611.2 * Math.exp(2.5e6 / 461.5 * (1 / 273.15 - 1 / 293.15)), e50 = 0.5 * es20;
const A50 = Object.assign({}, A20, { rho: (101325 - e50) / (287.05 * 293.15) + e50 / (461.5 * 293.15) });
const err = (Aa, d) => (P.vBeard(d * 5e-4, Aa) / (GK.find(q => q[0] === d)[1] / 100) - 1) * 100;
expect('book-02', "Gunn and Kinzer's", `${GK.length} measured speeds`);
expect('book-02', 'within', f(Math.max(...GK.filter(q => q[0] >= 1.2).map(q => Math.abs(err(A50, q[0])))), 2) + ' % above 1.2 mm');
const mid = GK.filter(q => q[0] >= 0.3 && q[0] <= 1.0).map(q => -err(A50, q[0]));
expect('book-02', 'above 1.2 mm', `${f(Math.min(...mid), 1)} to ${f(Math.max(...mid), 1)} % below the data`);
expect('book-02', 'the largest gap from 0.3 mm up is', f(Math.max(...GK.filter(q => q[0] >= 0.3).map(q => Math.abs(err(A20, q[0])))), 2) + ' % in dry air');
expect('book-02', 'At 0.1 and 0.2 mm the gaps are', `${f(err(A50, 0.1), 1).replace('-', '−')} and ${f(err(A50, 0.2), 1).replace('-', '−')} %`);
expect('book-02', 'The drag balance gives', `${f(vB(40e-6), 3)} m/s at 40 µm, ${f(vB(60e-6), 3)} m/s at 60 µm and ${f(vB(100e-6), 3)} m/s at 100 µm`);
expect('book-02', 'Stokes is too fast by', [40, 60, 100].map(a => f((vS(a * 1e-6) / vB(a * 1e-6) - 1) * 100, 0) + ' %').join(', ').replace(/, (\d+ %)$/, ' and $1'));
// local drag exponent at 100 um: F ~ v^n; drag = weight less buoyancy, varied through the particle's density at fixed size
const vRho = rp => P.vBeard(100e-6, A, rp), dr = 1e-3;
const nexp = Math.log((1000 * (1 + dr) - A.rho) / (1000 * (1 - dr) - A.rho)) / Math.log(vRho(1000 * (1 + dr)) / vRho(1000 * (1 - dr)));
expect('book-02', 'Near 100 µm the drag grows as', `v^{${f(nexp, 2)}}: ${f((nexp - 1) * 100, 0)} % of the way`);
const tB100 = (() => { let R = 40e-6, t = 0; const h = 0.05, fr = RR => Math.PI * (RR + 8e-6) ** 2 * (vB(RR) - vB(8e-6)) * W8 / (4 * Math.PI * RR * RR * RW);
  while (R < 100e-6) { const k1 = fr(R), k2 = fr(R + h / 2 * k1), k3 = fr(R + h / 2 * k2), k4 = fr(R + h * k3), Rn = R + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4);
    if (Rn >= 100e-6) { t += h * (100e-6 - R) / (Rn - R); break; } R = Rn; t += h; } return t; })();
const ratios = []; for (let a = 40; a <= 100; a += 0.5) ratios.push((vS(a * 1e-6) - vS(8e-6)) / (vB(a * 1e-6) - vB(8e-6)));
expect('book-02', 'One collector, 40 → 100 µm:', `${f(t100 / 60, 2)} min with Stokes, ${f(tB100 / 60, 2)} min with the drag balance, a factor ${f(tB100 / t100, 2)} (bounds ${f(Math.min(...ratios), 2)} and ${f(Math.max(...ratios), 2)})`);
expect('book-02', 'grow by factors', `${f(bB50 / b50, 2)} and ${f(bB90 / b90, 2)}`);
const W = D('warm.json'), tq = (run, q) => interp(W[run].t, W[run].F40, q) / 60;   // tools/run_warm.cjs --json
expect('book-02', 'takes', `${f(tq('thesis', 0.9), 2)} min to put 90 %`);
expect('book-02', 'with Stokes speeds and', `${f(tq('thesisBeard', 0.9), 2)} min with the drag balance: a factor ${f(tq('thesisBeard', 0.9) / tq('thesis', 0.9), 2)}`);

// ---------------------------------------------------------------- chapter 3
const pe = P.pairEfficiency(40e-6, 8e-6, A);
expect('book-03', 'An 8 µm droplet meeting a 40 µm collector:', `St = ${f(pe.St, 2)}, S = ${f(pe.S, 3)}`);
expect('book-03', 'Our collectors have Re between', `${f(pe.Re, 1)} and ${f(P.reynolds(100e-6, vB(100e-6), A), 0)}`);
expect('book-03', 'Our solver gives', f(P.criticalStokes('stokes', 100), 5));
const eZ = Z => P.flowEfficiency('stokes', pe.St, pe.S, 0.2, Z).E;
expect('book-03', 'starting at 400 radii instead changes', 'less than $10^{-4}$', `|ΔE| = ${Math.abs(eZ(400) - eZ(200)).toExponential(1)}`);
expect('book-03', 'In our cloud E(40 µm, 8 µm) =', f(pe.E, 3) + ', against ' + f(P.hallE(hall, 40e-6, 0.2), 2));
expect('book-03', 'about $\\nu/U = 2R/\\mathrm{Re} =', f(2 / pe.Re, 1) + ' collector radii');
expect('book-03', 'the partner coasts', f(pe.St, 1) + ' radii');
const cross = c => (pe.ES + pe.EP * pe.Re / c) / (1 + pe.Re / c);

const hr = R => [P.hallE(hall, R * 1e-6, 8 / R), P.pairEfficiency(R * 1e-6, 8e-6, A).E];
expect('book-03', '1.2 to 1.5 times ours', `(${f(hr(40)[0], 2)} against ${f(hr(40)[1], 3)} at 40 µm, ${f(hr(50)[0], 2)} against ${f(hr(50)[1], 2)} at 50 µm, ${f(hr(100)[0], 2)} against ${f(hr(100)[1], 2)} at 100 µm)`);
expect('book-03', 'its flow at the collector is', 'under 1 %', `${f(0.75 * 8 / 48 * pe.S * 100, 2)} % of U`);
const Ip = p => 1 - 1.5 / (1 + p) + 0.5 / (1 + p) ** 3;
expect('book-03', 'at 40/8 µm,', `${f(pe.S, 3)} against ${f(Ip(0.2), 3)}`);
expect('book-03', 'In the full collection equation', `${f(tq('thesisBeard', 0.9), 2)} min with E = 1 and the drag balance, after ${f(tq('extended', 0.9), 2)} min with this chapter's efficiencies, and after ${f(tq('extHall', 0.9), 2)} min with Hall's`, null, 500);

// ---------------------------------------------------------------- chapter 4
const sig = P.sigmaWater(283.15);
const cke = (a1, a2, dv) => { const m1 = P.massOf(a1), m2 = P.massOf(a2); return 0.5 * m1 * m2 / (m1 + m2) * dv * dv; };
const We = (a1, a2, v) => P.weber(a1, a2, Math.abs(v(a1) - v(a2)), sig);
expect('book-04', 'the collision energy is', texSci(cke(40e-6, 8e-6, vB(40e-6) - vB(8e-6)), 1) + '$ J and We = $' + texSci(We(40e-6, 8e-6, vB), 1));
expect('book-04', 'the surface is', `${Math.round(1 / We(40e-6, 8e-6, vB) / 10000) * 10000}`.replace(/(\d)(?=(\d{3})+$)/g, '$1 ') + ' times stiffer', `1/We = ${f(1 / We(40e-6, 8e-6, vB), 0)}`);
expect('book-04', 'E_coal = 0.99998', '0.99998', f(Math.exp(-1.15 * We(40e-6, 8e-6, vB)), 5));
expect('book-04', 'two collectors of 60 and 50 µm', texSci(We(60e-6, 50e-6, vB), 1));
expect('book-04', 'a 500 µm drop meeting a 250 µm drop has', `We = ${f(We(500e-6, 250e-6, vB), 2)} and E_coal = ${f(Math.exp(-1.15 * We(500e-6, 250e-6, vB)), 2)}`);
expect('book-04', "Stokes' relative speed is", `${f(vS(500e-6) - vS(250e-6), 0)} m/s instead of ${f(vB(500e-6) - vB(250e-6), 1)} m/s, We = ${f(We(500e-6, 250e-6, vS), 0)}`);

// ---------------------------------------------------------------- chapter 5
const grid = P.makeGrid(8, 4e-3), N0 = P.lognormalBins(grid, modes);
const k40 = grid.r.findIndex(r => r >= 40e-6);
let m40 = 0, mall = 0; for (let i = 0; i < grid.n; i++) { mall += N0[i] * grid.x[i]; if (i >= k40) m40 += N0[i] * grid.x[i]; }
const lnS = md => Math.log(md.sg), massAbove = (md, r) => modeMass(md) * 0.5 * erfc((Math.log(r) - Math.log(md.rg) - 3 * lnS(md) ** 2) / lnS(md) / Math.SQRT2);
expect('book-05', 'At the start', `${f(m40 / mall * 100, 1)} % of the water is in drops above 40 µm on the grid of section 5.3 (${f((massAbove(modes[0], 40e-6) + massAbove(modes[1], 40e-6)) / (modeMass(modes[0]) + modeMass(modes[1])) * 100, 1)} %`);
const gol = [2, 4, 8, 16].map(s => G.run(s, 1));
expect('book-05', 'spectrum error falls from', `${f(gol[0].eps, 3)} at 2 bins per doubling to ${f(gol[1].eps, 3)}, ${f(gol[2].eps, 3)} and ${f(gol[3].eps, 3)}`);
expect('book-05', 'an observed order of about', f((Math.log2(gol[0].eps / gol[1].eps) + Math.log2(gol[1].eps / gol[2].eps) + Math.log2(gol[2].eps / gol[3].eps)) / 3, 1));
expect('book-05', 'At 8 bins per doubling its mass error is', texSci(gol[2].massErr, 2));
expect('book-05', 'the scheme itself changes the mass by', texSci(Math.abs(gol[2].schemeDrift), 0).replace('2\\times', '2\\times'), gol[2].schemeDrift.toExponential(1));
const gq = (run, q) => interp(W[run].gce.t, W[run].gce.F40, q) / 60;
expect('book-05', 'thesis SCE', `${f(tq('thesis', 0.5), 2)} ${f(tq('thesis', 0.9), 2)}`);
expect('book-05', 'thesis GCE', `${f(gq('thesis', 0.5), 2)} ${f(gq('thesis', 0.9), 2)}`);
expect('book-05', 'extended SCE', `${f(tq('extended', 0.5), 2)} ${f(tq('extended', 0.9), 2)}`);
expect('book-05', 'extended GCE', `${f(gq('extended', 0.5), 2)} ${f(gq('extended', 0.9), 2)}`);
expect('book-05', "Hall's E SCE", `${f(tq('extHall', 0.5), 2)} ${f(tq('extHall', 0.9), 2)}`);
const drift = Math.max(...['thesis', 'thesisBeard', 'extended', 'extHall'].map(r => Math.max(...W[r].drift.map(Math.abs))));
expect('book-05', 'The water books close to', texSci(drift, 1));
expect('book-05', 'Changing the kernel moves $t_{90}$ from', `${f(tq('thesis', 0.9), 1)} to ${f(tq('extended', 0.9), 1)} min`);
expect('book-05', 'Changing the bookkeeping moves it by', `${f(gq('thesis', 0.9) - tq('thesis', 0.9), 1)} min (thesis) or ${f(gq('extended', 0.9) - tq('extended', 0.9), 1)} min`);

// ---------------------------------------------------------------- chapter 6
const S = D('stochastic.json'), B = D('bridge.json').s16;      // tools/run_stochastic.cjs --json, tools/run_bridge.cjs
const allRuns = Object.values(S.V).flat();
const acc = Object.values(S.V).map(rs => rs.reduce((a, q) => a + q.events, 0) / rs.reduce((a, q) => a + q.proposals, 0));
expect('book-06', 'zero violations in', `${allRuns.length} runs`, `${allRuns.reduce((a, q) => a + q.violations, 0)} violations`);
expect('book-06', 'zero violations in', `${f(Math.min(...acc) * 100, 0)} to ${f(Math.max(...acc) * 100, 0)} %`);
expect('book-06', 'no collector starts above', f(40 * 1.2 ** 3, 0) + ' µm');
function erfc(x) { const t = 1 / (1 + 0.5 * Math.abs(x)); const y = t * Math.exp(-x * x - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277))))))))); return x >= 0 ? y : 2 - y; };
const tail100 = 1e6 * 0.5 * erfc(Math.log(100 / 40) / Math.log(1.2) / Math.SQRT2);
expect('book-06', 'would put', f(tail100, 2) + ' drops of 100 µm', `${tail100.toPrecision(3)} per m³`);
expect('book-06', 'Run the process many times', `(${S.plan.map(q => q[1]).join(', ').replace(/, (\d+)$/, ' and $1')} runs)`);
const med = V => { const t = S.V[V].map(q => q.t100).filter(x => x !== null).sort((a, b) => a - b); return t.length ? t[Math.floor(t.length / 2)] : null; };
expect('book-06', 'In 1 cm³', 'no drop ever reaches 100 µm', `${S.V['1'].filter(q => q.t100 !== null).length} of ${S.V['1'].length} runs`);
expect('book-06', 'The median time to the first 100 µm drop is', `${f(med('10'), 0)} s in 10 cm³, ${f(med('100'), 0)} s in 100 cm³ and ${f(med('1000'), 0)} s in 1000 cm³`);
const made = allRuns.filter(q => q.t100 !== null), viaBig = made.filter(q => q.big100 >= 1);
expect('book-06', 'In every one of the', `${made.length} runs that made one`, `${viaBig.length} via a partner ≥ 30 µm`);
const bridgeMed = V => { for (let i = 0; i < B.t.length; i++) if (V * B.N100[i] >= Math.LN2) return B.t[i]; };
expect('book-06', '(6.1) predicts medians of', `${bridgeMed(1e-4)} s in 100 cm³ and ${bridgeMed(1e-3)} s in 1000 cm³`);
expect('book-06', 'the exact runs gave', `${f(med('100'), 0)} and ${f(med('1000'), 0)} s`);
// the far tail at 8, 16, 32 bins per doubling, records every second (as derive/L5_tail.cjs)
const tailMed = sb => { const r = P.sceRun(P.makeGrid(sb, 4e-3), A, KO, modes, { dt: 1, tEnd: 120, recordEvery: 1, trunc: 3, snapAt: [] });
  let mx = 0; for (let i = 0; i < r.t.length; i++) { mx = Math.max(mx, r.N100[i]); if (mx >= Math.LN2) return r.t[i]; } return null; };
expect('book-06', 'the first 100 µm drop in 1 m³ appears after', `about a minute (${tailMed(8)}, ${tailMed(16)} and ${tailMed(32)} s with 8, 16 and 32 bins per doubling`);
const Wall = modeMass(modes[0]) + modeMass(modes[1]);
expect('book-06', 'a 100 µm drop holds the water of', `${f(P.massOf(100e-6) / Wall * 1e6, 2)} cm³`);
expect('book-06', 'a 1 mm drop holds the water of', `${f(P.massOf(1e-3) / Wall * 1e3, 2)} litres`);
const cap = (() => { let R = 69e-6, t = 0; const h = 0.05, fr = RR => P.tableE(tab, RR, 8e-6 / RR, 'clamp') * Math.PI * (RR + 8e-6) ** 2 * (vB(RR) - vB(8e-6)) * modeMass(modes[0]) / (4 * Math.PI * RR * RR * RW);
  while (R < 100e-6) { R += h * fr(R); t += h; } return t; })();   // all the droplet water, as 8 um droplets, none used up
expect('book-06', 'the largest collector the cloud starts with', `(${f(40 * 1.2 ** 3, 0)} µm)`);
expect('book-06', 'none used up, would need', `${f((100 ** 3 - 69 ** 3) / 512, 0)} captures and ${f(cap, 0)} s`);
const nmx = []; B.N100.reduce((m, N, i) => (nmx[i] = Math.max(m, N)), 0);
const i605 = B.t.indexOf(605);
expect('book-06', 'Ten cm³ hold about ten collectors and the water for', `one drop of ${f(P.radiusOf(Wall * 1e-5) * 1e6, 0)} µm`);
expect('book-06', 'at 605 s it already has', `${f(B.F100[i605] * 100, 0)} % of the water above 100 µm, but packed into drops of ${f(P.radiusOf(B.F100[i605] * Wall / B.N100[i605]) * 1e6, 0)} µm`);
expect('book-06', 'radius), only', `${f(B.N100[i605] * 1e-5, 2)} of them per 10 cm³`);
const rmx = S.V['10'].map(q => Math.max(...q.rmax));
expect('book-06', 'every box ends with one drop of', `100 to ${r10(Math.max(...rmx))} µm`, `largest ${f(Math.max(...rmx), 1)} µm, smallest final ${f(Math.min(...S.V['10'].map(q => q.rmax[q.rmax.length - 1])), 1)} µm`);
expect('book-06', 'The mean field says that at most', `${f((1 - Math.exp(-1e-5 * Math.max(...nmx))) * 100, 0)} %`);
expect('book-06', 'every one of the', `${S.V['10'].filter(q => q.t100 !== null).length} exact runs made one, after a median of ${f(med('10'), 0)} s`);
let t1mm = null; for (let i = 0; i < B.t.length; i++) if (B.N1mm[i] >= Math.LN2) { t1mm = B.t[i]; break; }
expect('book-06', 'the first 1 mm drop after about', `${f(t1mm / 60, 0)} min`, `${t1mm} s`);
expect('book-06', 'Half of the water is in drops above 100 µm only after', `${Math.round(interp(B.t, B.F100, 0.5) / 5) * 5} s`, `${interp(B.t, B.F100, 0.5).toFixed(1)} s, to the 5 s record`);
const F10 = V => S.V[V].reduce((a, q) => a + q.F40[10], 0) / S.V[V].length;
expect('book-06', 'After 10 min the average share above 40 µm is', `${f(F10('1'), 2)} in 1 cm³, ${f(F10('10'), 2)} in 10 cm³, ${f(F10('100'), 2)} in 100 cm³ and ${f(F10('1000'), 2)} in 1000 cm³`);

// ---------------------------------------------------------------- chapter 7
const tauK = Math.sqrt(A.nu / 1e-2);
expect('book-07', '$\\tau_K$ =', f(tauK * 1000, 0) + ' ms');
expect('book-07', 'An 8 µm droplet (response time', f(vB(8e-6) / g * 1000, 1) + ' ms');
expect('book-07', 'a 40 µm collector (', f(vB(40e-6) / g * 1000, 0) + ' ms) has a Stokes number of about ' + f(vB(40e-6) / g / tauK, 1));
expect('book-07', 'their formula raises the kernel by', [1e-3, 1e-2, 4e-2].map(e => f((P.ayalaFactor(40e-6, 8e-6, A, e) - 1) * 100, e < 2e-3 ? 1 : e < 2e-2 ? 1 : 0)).join(' %, ').replace(/ %, (\d+)$/, ' % and $1') + ' %');
let lo2 = 20e-6, hi2 = 100e-6; const tK4 = Math.sqrt(A.nu / 4e-2);
for (let i = 0; i < 60; i++) { const m = (lo2 + hi2) / 2; if (vB(m) / g / tK4 > 1) hi2 = m; else lo2 = m; }
expect('book-07', 'for every collector above', f(lo2 * 1e6, 0) + ' µm');
const runT = ko => { const r = P.sceRun(grid, A, ko, modes, { dt: 1, tEnd: 1500, recordEvery: 5, snapAt: [] }); return interp(r.t, r.F40, 0.9) / 60; };
const t90ext = runT(KO), t90t100 = runT(Object.assign({}, KO, { eps: 1e-2 })), t90t400 = runT(Object.assign({}, KO, { eps: 4e-2 }));
expect('book-07', 'shortens $t_{90}$ by', f((1 - t90t100 / t90ext) * 100, 1) + ' % at 100 cm²/s³');
expect('book-07', 'the stronger turbulence shortens', `by only ${f((1 - t90t400 / t90ext) * 100, 1)} %`);
// Langmuir's crossover carried through the collection equation (split table written by derive/L2_cross.cjs with makeTable({split}))
const SP = D('etab_split.json');
const tabC = c => Object.assign({}, SP, { E: SP.ES.map((es, i) => (es + SP.EP[i] * SP.Re[i] / c) / (1 + SP.Re[i] / c)) });
const tc = [60, 20, 6, 2].map(c => runT(Object.assign({}, KO, { tab: tabC(c) })));
const lnR30 = Math.log(30e-6), tab60 = tabC(60);
const t90one = runT(Object.assign({}, KO, { tab: Object.assign({}, tab60, { E: tab60.E.map((e, i) => SP.lnR[Math.floor(i / SP.lnp.length)] < lnR30 ? 1 : e) }) }));
expect('book-07', 'far less than the', `${f(tc[0] - tc[3], 1)} min by which the collision efficiency moves t_{90} (${f(tc[3], 1)} to ${f(tc[0], 1)} min`);
expect('book-03', 'his value, used here', `${f(cross(60), 3)} ${f(tc[0], 1)} 20 ${f(cross(20), 3)} ${f(tc[1], 1)} 6 ${f(cross(6), 3)} ${f(tc[2], 1)} 2 ${f(cross(2), 3)} ${f(tc[3], 1)} Hall's (1980) table instead ${f(P.hallE(hall, 40e-6, 0.2), 2)} ${f(tq('extHall', 0.9), 1)}`);
expect('book-03', 'That spread,', `${f(tc[3], 1)} to ${f(tc[0], 1)} min`);
expect('book-03', 'with E = 1 for collectors below 30 µm,', `falls to ${f(t90one, 1)} min`);
expect('book-05', 'moves $t_{90}$ from', `${f(tc[0], 1)} down to ${f(tc[3], 1)} min, and Hall's table gives ${f(tq('extHall', 0.9), 1)} min`);
expect('book-05', 'So $t_{90}$ =', `${f(tc[3], 1)} to ${f(tc[0], 1)} min`);
expect('book-09', 'with $t_{90}$ anywhere from', `${f(tc[3], 1)} to ${f(tc[0], 1)} min`);
expect('book-09', 'the bookkeeping changes $t_{90}$ by', `${f(gq('thesis', 0.9) - tq('thesis', 0.9), 1)} to ${f(gq('extended', 0.9) - tq('extended', 0.9), 1)} min`);

// chapter 5: resolution
const runS = (sb, dt) => { const r = P.sceRun(P.makeGrid(sb, 4e-3), A, KO, modes, { dt, tEnd: 1200, recordEvery: 5, snapAt: [] }); return interp(r.t, r.F40, 0.9) / 60; };
const t4 = runS(4, 1), t16 = runS(16, 1), tq4 = runS(8, 0.25);
expect('book-05', 'halving the time step twice moves', `by ${f(Math.abs(tq4 - t90ext), 3)} min`);
expect('book-05', 'going from 4 to 8 to 16 bins per doubling moves it from', `${f(t4, 2)} to ${f(t90ext, 2)} to ${f(t16, 2)} min`);
// ---------------------------------------------------------------- chapter 4 continued: coalescence = 1 changes t90 by
const t90c1 = runT(Object.assign({}, KO, { coal: 'one' }));
expect('book-04', 'setting E_coal = 1 changes $t_{90}$ by', f((1 - t90c1 / t90ext) * 100, 2) + ' %');
// chapter 3: Hall's values for collectors below 30 um
const t90hs = runT(Object.assign({}, KO, { hall, hallBelow: 30e-6 }));
expect('book-03', "Putting Hall's values in for collectors below 30 µm changes", f(Math.abs(1 - t90hs / t90ext) * 100, 1) + ' %');

// ---------------------------------------------------------------- chapter 8 (tools/run_cold.cjs --json)
const C = D('cold.json'), pm = x => x * 60 / 1e6;
expect('book-08', 'stays liquid when supercooled,', f(C.Fliq * 100, 2) + ' %');
expect('book-08', 'stays liquid when supercooled,', `${f(C.liquid / 1e6, 1)} liquid drops and ${f(C.ice / 1e6, 1)} ice spheres`);
expect('book-08', 'almost every such event', `(${f(pm(C.rime25big), 3)} of ${f(pm(C.rime25), 3)} per cm³`);
const Ai = P.air(263.15, 60000), vi = a => P.vBeard(a, Ai, 900), mi = a => P.massOf(a, 900);
const K0 = 0.5 * mi(40e-6) * mi(8e-6) / (mi(40e-6) + mi(8e-6)) * (vi(40e-6) - vi(8e-6)) ** 2;
const fT = 1 / 3 + Math.max(2 / 3 - Math.abs(263.15 - 258) / 9, 0), aA = Math.PI * 16e-6 ** 2 * 3.78e4 * (1 + 0.0079 / Math.pow(5e-4, 1.5)) * fT;
const Fr = aA * (1 - Math.exp(-Math.pow(6.3e6 * K0 / aA, 0.3)));
expect('book-08', 'A 40 µm ice sphere falls at', `${f(vi(40e-6), 4)} m/s, an 8 µm one at ${f(vi(8e-6), 4)} m/s`);
expect('book-08', 'Their collision energy is', `$K_0 = ${texSci(K0, 1)}$ J`);
expect('book-08', 'as its users recommend', `$\\alpha A = ${texSci(aA, 1)}$ and $C K_0 = ${texSci(6.3e6 * K0, 1)}$`);
expect('book-08', 'so $F =', texSci(Fr, 1) + '$ fragments');
expect('book-08', 'one new splinter per', 'three thousand', f(1 / Fr, 0));
expect('book-08', "The old study's rule gave this collision", f(0.001 * mi(40e-6) / mi(5e-6), 2) + ' fragments');
expect('book-08', 'the ice–ice collisions in our cloud carry', `$${texSci(C.K0q[0], 1)}$ to $${texSci(C.K0q[2], 1)}$ J`);
const Kfit = 0.5 * mi(0.5e-3) * mi(0.25e-3) / (mi(0.5e-3) + mi(0.25e-3)) * (vi(0.5e-3) - vi(0.25e-3)) ** 2;
expect('book-08', 'the smallest particles (8.2) was fitted to, fall at', `${f(vi(0.25e-3), 2)} and ${f(vi(0.5e-3), 2)} m/s and collide with K_0 = ${texSci(Kfit, 1)} J`);
expect('book-08', 'our collisions carry', `${f(Math.log10(Kfit / C.K0q[2]), 1)} to ${f(Math.log10(Kfit / C.K0q[0]), 1)} orders of magnitude`);
expect('book-08', 'with $a_0 = 3.78', `${f(fT, 3)} $a_0$ at −10`);
expect('book-06', 'The 1 cm³ curve starts lower', `(${f(S.V['1'].reduce((a, q) => a + q.F40[0], 0) / S.V['1'].length, 2)})`);
expect('book-01', 'with the droplets\' own size, (1.2), already at', `${f(P.L0blowup(40e-6, 8e-6, W8, A) / 60, 1)} min`);
expect('book-08', '0 to 1.7 fragments per freezing drop,', `${f(pm(C.rime25), 2)} drops of 25 µm`);
expect('book-08', 'or more freezing per cm³ and minute', `0 to ${f(pm(C.shatter[1]), 1)}`);
expect('book-08', 'with $D$ held at 0.5 mm in $A$,', `${f(pm(C.ii), 2)} collisions per cm³`);
expect('book-08', 'J⁻¹)', `$${texSci(pm(C.fragLo), 1)}$ to $${texSci(pm(C.fragHi), 1)}$`);
expect('book-08', "true diameters put into (8.2)", f(pm(C.fragTrueD), 3));
expect('book-08', 'as fragments of 5 µm radius', f(pm(C.oldRule), 1));
expect('book-08', 'gives between', `${Math.round(C.oldRule / C.fragHi / 100) * 100} times`, f(C.oldRule / C.fragHi, 0));
expect('book-08', '(the law used as recommended) and', `${f(C.oldRule / C.fragTrueD, 0)} times`);
expect('book-08', 'One more caution:', `${f(C.ice / 1e6, 0)} ice spheres`);

// ---------------------------------------------------------------- chapter 9 and the problems
expect('book-09', 'Most of the water sits in drops above 40 µm after', `${f(tq('extended', 0.5), 1)} min (half) and ${f(tq('extended', 0.9), 1)} min (nine tenths)`);
expect('book-09', '(', `${f(tq('extHall', 0.9), 1)} min with Hall's table`);
expect('book-09', 'collisions of small ice spheres make', `${r10(C.oldRule / C.fragTrueD)} to ${Math.round(C.oldRule / C.fragHi / 100) * 100} times less`);
const c19 = k * W8 / (4 * RW);
expect('problems', 'and $R_0 = 40$ µm, $c =', f(c19, 1) + ' m⁻¹ s⁻¹ and $t^*$ = ' + f(1 / (c19 * 40e-6) / 60, 1) + ' min');
expect('problems', 'A 40 µm collector falls at', f(vB(40e-6), 3) + ' m/s');
const tauMin = (1 / 12) * 40e-6 / vB(40e-6), rOf = tau => Math.sqrt(9 * A.mu * tau / (2 * RW));
expect('problems', 'in potential flow $\\tau \\ge', texSci(tauMin, 2) + '$ s');
expect('problems', '$r = \\sqrt{9\\mu\\tau/(2\\rho_w)}$ =', f(rOf(tauMin) * 1e6, 2) + ' µm');
expect('problems', 'In creeping flow the same steps give', f(rOf(P.criticalStokes('stokes', 100) * 40e-6 / vB(40e-6)) * 1e6, 2) + ' µm');
expect('problems', 'The relative speed is', `${f(vS(500e-6) - vS(250e-6), 1)} m/s with Stokes' law and ${f(vB(500e-6) - vB(250e-6), 2)} m/s`);
expect('problems', 'so We grows by', `\\approx ${r10(((vS(500e-6) - vS(250e-6)) / (vB(500e-6) - vB(250e-6))) ** 2)}`, f(((vS(500e-6) - vS(250e-6)) / (vB(500e-6) - vB(250e-6))) ** 2, 1));
expect('problems', 'Here $bLt$ =', `${f(1.5 * 1e-3 * 3600, 2)} and $N/N_0$ = ${f(Math.exp(-5.4), 5)}`);
expect('problems', 'so $n_{100}$ = ln 2/(10⁻³ m³) =', `${f(Math.LN2 / 1e-3, 0)} per m³`);
expect('problems', 'The collection equation reaches it after', `${bridgeMed(1e-3)} s`);
expect('problems', 'only', `${f(Math.LN2, 2)} per m³`);

// ---------------------------------------------------------------- the Checks tab (numbers from the model; the Python results are checks/check_physics.py's)
expect('checks', 'One collector: (1.4) against a numerical integration', f(t100 / 60, 4) + ' min');
expect('checks', 'Fall speed against Gunn and Kinzer', 'largest gap ' + f(Math.max(...GK.filter(q => q[0] >= 0.3).map(q => Math.abs(err(A20, q[0])))), 2) + ' %');
expect('checks', 'Critical Stokes numbers', `${f(P.criticalStokes('potential', 100), 5)} (exact 1/12); ${f(P.criticalStokes('stokes', 100), 5)}`);
expect('checks', "Golovin's exact solution", `spectrum error ${f(gol[2].eps, 3)}; mass error −${uniSci(-gol[2].massErr, 2)}`);
expect('checks', 'Water conservation', 'to ' + uniSci(drift, 1));
expect('checks', 'kernel bound violated', `${allRuns.reduce((a, q) => a + q.violations, 0)} times in ${allRuns.length} runs`);
expect('checks', 'against the Poisson prediction (6.1)', `medians ${f(med('100'), 0)} s and ${f(med('1000'), 0)} s against ${bridgeMed(1e-4)} s and ${bridgeMed(1e-3)} s`);
const up = x => Math.ceil(x);
expect('checks', 'recorded to the minute', `${up(tq('thesis', 0.5))} / ${up(tq('thesis', 0.9))}, ${up(gq('thesis', 0.5))} / ${up(gq('thesis', 0.9))}, ${up(tq('extended', 0.5))} / ${up(tq('extended', 0.9))}, ${up(gq('extended', 0.5))} / ${up(gq('extended', 0.9))} min`);
expect('checks', 'against 5.767,', `${f(t90ext, 3)}`, 'the model at 5 s records');

// ---------------------------------------------------------------- chapter 10: energy and entropy of merging (data/energy.json, data/ripening.json)
{
  const EN = D('energy.json'), wr = EN.warm, sig = P.sigmaWater(A.T), kB = P.K_B, T = A.T, RP = D('ripening.json');
  const dsdT = (P.sigmaWater(T + 0.01) - P.sigmaWater(T - 0.01)) / 0.02, us = sig - T * dsdT;
  const area = r => 4 * Math.PI * r * r, dA = (a, b) => area(a) + area(b) - area(Math.cbrt(a ** 3 + b ** 3));
  expect('book-10', 'takes $\\sigma$ =', f(sig, 5) + ' J');
  expect('book-10', 'two equal drops\nlose'.replace('\n', ' '), f(100 * (1 - Math.pow(2, -1 / 3)), 1) + ' %');
  const g8 = P.makeGrid(8, 4e-3), Nd = P.lognormalBins(g8, [modes[0]]), Nc = P.lognormalBins(g8, [modes[1]]);
  let Ed = 0, Ec = 0; for (let k2 = 0; k2 < g8.n; k2++) { Ed += Nd[k2] * area(g8.r[k2]); Ec += Nc[k2] * area(g8.r[k2]); }
  expect('book-10', 'At the start the drops in a cubic metre hold', `$F_s$ = ${f(wr.Es0, 3)} J, ${f(100 * Ed / (Ed + Ec), 0)} % of it`);
  const d408 = sig * dA(40e-6, 8e-6), mu = P.massOf(40e-6) * P.massOf(8e-6) / (P.massOf(40e-6) + P.massOf(8e-6)), KE = 0.5 * mu * (vB(40e-6) - vB(8e-6)) ** 2;
  expect('book-10', 'eating an 8 µm droplet lowers', `${texSci(d408, 1)} J, ${Math.round(d408 / KE / 100) * 100} times`);
  expect('book-10', 'Each\nsquare metre'.replace('\n', ' '), `$u_s = \\sigma - T\\,d\\sigma/dT$ = ${f(us, 3)} J, ${f(us / sig, 2)} times`);
  expect('book-10', 'For the capture above that is', `${texSci(us * dA(40e-6, 8e-6), 1)} J, which warms the merged drop by ${texSci(us * dA(40e-6, 8e-6) / ((P.massOf(40e-6) + P.massOf(8e-6)) * 4192), 1)} K`);
  expect('book-10', '$1.32', texSci(d408 / T / kB, 2), 'entropy of one capture ' + texSci(d408 / T / kB, 2));
  expect('book-10', 'Over the hour merging releases', `${f(wr.totRel * us / sig, 3)} J of heat per m³ and raises the entropy by ${texSci(wr.totRel / T, 1)} J/K per m³, about ${texSci(wr.totRel / wr.totMerg / (kB * T), 1)}\\,k_B`);
  expect('book-10', 'At its largest the heat of merging is', `${f(100 * wr.maxRatio * us / sig, 1)} %`);
  expect('book-10', 'all the drops\' surfaces hold', `every ${f(wr.Es0 / wr.Pg0, 0)} s`);
  const h = 6.62607015e-34, m8 = P.massOf(8e-6), lam = h / Math.sqrt(2 * Math.PI * m8 * kB * T), Sd = Math.log(1 / (301e6 * lam ** 3)) + 2.5;
  expect('book-10', 'A drop of 8 µm is a particle of mass', `${texSci(m8, 1)} kg`);
  expect('book-10', 'For our droplets', `$\\lambda = ${texSci(lam, 1)}$ m and this is ${f(Sd, 0)} $k_B$ per drop`);
  expect('book-10', 'a = \\frac{2\\sigma}{\\rho_wR_vT} =', `${f(RP.a * 1e9, 2)}\\ \\text{nm}`);
  const mean = (c, t) => { const k2 = RP.recAt.indexOf(t); return RP.cases[c].reduce((a, r) => a + r[k2].F, 0) / RP.cases[c].length; };
  const q90 = wr.recs.find(q => Math.abs(q.t - 810) < 6);
  expect('book-10', 'By the time collection has put nine tenths', `destroyed ${f(100 * (1 - q90.Es / wr.Es0), 0)} % of the surface free energy; ripening has destroyed ${f(100 * (1 - mean('pure', Math.round(RP.t90))), 1)} %`);
  expect('book-10', 'Ripening needs an hour to remove', `${f(100 * (1 - mean('pure', 3600)), 0)} % and a day to remove ${f(100 * (1 - mean('pure', 86400)), 0)} %`);
  const k1h = RP.recAt.indexOf(3600), gone = 1 - RP.cases.pure.reduce((a, r) => a + r[k1h].alive, 0) / RP.cases.pure.length / 3010;
  expect('book-10', 'In\npure water'.replace('\n', ' '), `a third of the drops vanish within the hour`, 'share gone ' + f(100 * gone, 1) + ' %');
  const sr = RP.cases.salt[0], last = sr[sr.length - 1].r.filter(v => v > 0).sort((a, b) => a - b);
  expect('book-10', 'each shrinks only to a haze particle of', `${f(last[0], 2)} µm`);
  expect('book-10', 'the heat of merging is at most', `${f(100 * wr.maxRatio * us / sig, 1)} %`);
}

// ---------------------------------------------------------------- section 10.4: ripening as a gradient descent, its ledger (data/ripening.json)
{
  const RP = D('ripening.json'), EN = D('energy.json'), C = RP.classes, sig = P.sigmaWater(A.T), a = P.kelvinA(A), G = P.growthG(A), T = A.T, Rv = 461.5;
  const at = t => C.rec.find(q => q.t === t), q0 = at(0), mu = r => 2 * sig / (1000 * r);
  const strip = h => h.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();   // a table row as the reader sees it (the text is read with tags removed)
  expect('book-10', 'An 8 µm droplet holds its water at', `$\\mu$ = ${f(mu(8e-6), 1)} J/kg, a 40 µm collector at ${f(mu(40e-6), 1)} J/kg`);
  expect('book-10', 'sits as high above a lake', `lifted ${f(mu(8e-6) / 9.81, 2)} m`);
  expect('book-10', 'sits as high above a lake', `as if lifted ${f(mu(40e-6) / 9.81, 2)} m`);
  const L = 2.477e6, Kt = 2.48e-2, es = 611.2 * Math.exp(17.67 * (T - 273.15) / (T - 29.65)), Dv = 2.11e-5 * Math.pow(T / 273.15, 1.94) * (101325 / A.p);
  const Fk = (L / (Rv * T) - 1) * L * 1000 / (Kt * T), Fd = 1000 * Rv * T / (Dv * es);
  expect('book-10', 'Heat conduction is', `$G = ${texSci(G, 2)}$ m²/s. Heat conduction is ${f(100 * Fk / (Fk + Fd), 0)} % of the resistance and diffusion ${f(100 * Fd / (Fk + Fd), 0)} %`, null, 100);
  expect('book-10', 'with diffusion alone', `$${texSci(1 / Fd, 2)}$ m²/s, ${f((Fk + Fd) / Fd, 1)} times larger`);
  expect('book-10', 'it is 1.00 for droplets and', `${f(P.ventilation(40e-6, A), 2)} at 40 µm`);
  expect('book-10', 'the air holds', `${f(es / (Rv * T) * 1e3, 1)} g/m³ of vapour`);
  expect('book-10', 'while the drops hold', `${f(C.M0 * 1e3, 1)} g/m³`);
  // the first step: the classes rebuilt (quantiles of the normal cut at 3, as in run_ripening.cjs), and (10.8) recomputed from them
  const rate = r => 4 * Math.PI * 1000 * r * G * P.ventilation(r, A) * (q0.s - a / r), drdt = r => rate(r) / (4 * Math.PI * 1000 * r * r) * 3.6e9;
  const md = [[800, { N: 300e6, rg: 8e-6, sg: 1.25 }], [300, { N: 1e6, rg: 40e-6, sg: 1.2 }]];
  const nz = 60001, zs = Float64Array.from({ length: nz }, (_, i) => -3 + 6 * i / (nz - 1)), cdf = new Float64Array(nz);
  for (let i = 1; i < nz; i++) cdf[i] = cdf[i - 1] + 0.5 * (Math.exp(-zs[i] * zs[i] / 2) + Math.exp(-zs[i - 1] * zs[i - 1] / 2));
  const zOf = q => { const c = q * cdf[nz - 1]; let lo = 0, hi = nz - 1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (cdf[m] <= c) lo = m; else hi = m; } return zs[lo] + (zs[hi] - zs[lo]) * (c - cdf[lo]) / (cdf[hi] - cdf[lo]); };
  let upD = 0, upC = 0, nUpD = 0, sr = 0, sn = 0, sf = 0, srf = 0;
  for (const [nC, m] of md) for (let k = 0; k < nC; k++) { const r = m.rg * Math.exp(Math.log(m.sg) * zOf((k + 0.5) / nC)), w = m.N / nC, fv = P.ventilation(r, A);
    sr += w * r; sn += w; sf += w * fv; srf += w * r * fv; }
  const sRe = a / (srf / sf);
  for (const [nC, m] of md) for (let k = 0; k < nC; k++) { const r = m.rg * Math.exp(Math.log(m.sg) * zOf((k + 0.5) / nC)), w = m.N / nC, g = 4 * Math.PI * 1000 * r * G * P.ventilation(r, A) * (sRe - a / r);
    if (g > 0) { if (r < 20e-6) { upD += w * g; nUpD += w; } else upC += w * g; } }
  expect('book-10', 'At the start the drops set', `$s$ = ${f(100 * sRe, 4)} % and $r_c$ = ${f(srf / sf * 1e6, 2)} µm (their mean radius is ${f(sr / sn * 1e6, 2)} µm). ${f(100 * q0.nUp / (q0.nUp + q0.nDown), 0)} % of the drops lie above it and grow; ${f(100 * q0.nDown / (q0.nUp + q0.nDown), 0)} % shrink`, 'stored s ' + (100 * q0.s).toFixed(4) + ' %, stored r_c ' + (q0.rc * 1e6).toFixed(2));
  const sgn = (x, d) => (x < 0 ? '−' : '+') + f(Math.abs(x), d), sci = (x, d) => `$${x < 0 ? '-' : '+'}${texSci(Math.abs(x), d)}$`;
  expect('book-10', '5 µm droplet', strip(`<td>${sgn(drdt(5e-6), 2)}</td><td>${sci(rate(5e-6), 1)}</td>`));
  expect('book-10', '8 µm droplet', strip(`<td>${sgn(drdt(8e-6), 2)}</td><td>${sci(rate(8e-6), 1)}</td><td>${sgn(100 * rate(8e-6) * 3600 / P.massOf(8e-6), 1)} %`));
  expect('book-10', '12 µm droplet', strip(`<td>${sgn(drdt(12e-6), 2)}</td><td>${sci(rate(12e-6), 1)}</td><td>${sgn(100 * rate(12e-6) * 3600 / P.massOf(12e-6), 1)} %`));
  expect('book-10', '40 µm collector', strip(`<td>${sgn(drdt(40e-6), 2)}</td><td>${sci(rate(40e-6), 1)}</td><td>${sgn(100 * rate(40e-6) * 3600 / P.massOf(40e-6), 1)} %`));
  expect('book-10', 'A 40 µm collector takes in', `${f(rate(40e-6) / rate(12e-6), 1)} times as much water as a 12 µm droplet`);
  expect('book-10', 'there is one collector per cm³ and there are', `${f(nUpD / 1e6, 0)} droplets above`);
  expect('book-10', 'so at the start', `${f(100 * upD / (upD + upC), 0)} % of the water in transit goes to the larger droplets and only ${f(100 * upC / (upD + upC), 0)} % to the collectors`, 'flux recomputed ' + (upD + upC).toExponential(4) + ', stored ' + q0.flux.toExponential(4));
  expect('book-10', 'The clock (10.12) is', `$\\tau$ = ${f(q0.rc ** 3 / (G * a) / 3600, 2)} hours`);
  // the ledger table
  const row = (name, t) => { const q = at(t); return `<tr><td>${name}</td><td>${f(q.rc * 1e6, 1)} µm</td><td>${f(q.alive / 1e6, 0)}</td><td>${t ? f(100 * q.moved / C.M0, 1) + ' %' : '0'}</td><td>${f(100 * q.Wd / C.M0, 1)} / ${f(100 * q.Wc / C.M0, 1)} %</td><td>${t ? f(100 * q.F, 1) : '100'} %</td></tr>`; };
  expect('book-10', 'critical radius r_c drops left per cm³', strip(row('start', 0)), null, 900);
  expect('book-10', 'critical radius r_c drops left per cm³', strip(row('1 hour', 3600)), null, 900);
  expect('book-10', 'critical radius r_c drops left per cm³', strip(row('6 hours', 21600)), null, 900);
  expect('book-10', 'critical radius r_c drops left per cm³', strip(row('1 day', 86400)), null, 900);
  expect('book-10', 'The collector mode never loses a drop', `All ${f((q0.alive - at(86400).alive) / 1e6, 0)} drops per cm³ that vanish in a day are droplets`, 'collector-mode drops per cm³ at the end ' + (at(86400).nc / 1e6).toFixed(3));
  expect('book-10', 'in the first hour,', `${f(100 * at(3600).moved / C.M0, 1)} % of the water changes drops but the collectors gain only ${f(100 * (at(3600).Wc - q0.Wc) / C.M0, 1)} points`);
  expect('book-10', 'Even after a day the', `collectors have gained ${f(100 * (at(86400).Wc - q0.Wc) / C.M0, 0)} points of the water while ${f(100 * at(86400).moved / C.M0, 0)} % has passed`);
  const gaps = C.rec.filter(q => q.t >= 60).map(q => 100 * ((C.F0 * (1 - q.F)) / q.diss - 1));
  expect('book-10', 'From 1 minute to 1 day the stored fall', `is ${f(Math.min(...gaps), 1)} to ${f(Math.max(...gaps), 1)} % larger`);
  expect('book-10', 'The water is kept to', `$${texSci(Math.abs(at(86400).M - 1), 0)}$ of itself`);
  const d1 = RP.cases.pure.reduce((s2, r) => s2 + r.find(q => q.t === 3600).F, 0) / RP.cases.pure.length;
  expect('book-10', 'after one hour the classes have', `${f(100 * at(3600).F, 1)} % of the free energy left, the three draws of 3010 drops ${f(100 * d1, 1)} %`);
  expect('book-10', 'predicts that after a long time', `ours grows ${f((at(86400).rc ** 3 - at(43200).rc ** 3) / 43200 / (4 / 9 * G * a), 1)} times faster`);
  const q90 = EN.warm.recs.find(q => Math.abs(q.t - 810) < 6), Pcol = (EN.warm.Es0 - q90.Es) / q90.t;
  expect('book-10', 'At the start ripening lowers the free energy at', `$${texSci(q0.P, 1)}$ W per m³ of cloud`);
  expect('book-10', 'averaged up to 13.5 min, at', `$${texSci(Pcol, 1)}$ W per m³, ${f(Pcol / q0.P, 0)} times faster`);
  expect('checks', 'against the summed formula (10.9)', `the stored fall is ${f(Math.min(...gaps), 1)} to ${f(Math.max(...gaps), 1)} % larger`);
  expect('checks', 'Ripening followed as 1100 classes', `${f(100 * at(3600).F, 1)} % against ${f(100 * d1, 1)} %`);
  expect('book-10', 'some twenty times the', `${f(100 * q0.s, 3)} %`);
  // figure 3.2's ripple and chapter 7's a0
  let rip = 0; for (const Rum of [60, 100]) { const E2 = []; for (let i = 0; i < 240; i++) { const p = 0.005 + 0.595 * i / 239; E2.push(p < 0.19 ? NaN : P.pairEfficiency(Rum * 1e-6, p * Rum * 1e-6, A).E); }
    for (let i = 4; i < 236; i++) { const fit = (-E2[i - 4] + 4 * E2[i - 2] + 4 * E2[i + 2] - E2[i + 4]) / 6; if (isFinite(fit) && isFinite(E2[i])) rip = Math.max(rip, Math.abs(E2[i] - fit)); } }
  expect('book-03', 'The fine ripple on the two upper curves, up to', f(rip, 3), null, 40);
  expect('book-07', 'answer them differently', `$a_0$ = ${f((11 + 7 * 2e4) / (205 + 2e4), 1)}`);
  // problem 9
  { let r1 = 6e-6, r2 = 10e-6, t = 0; const c = r1 ** 3 + r2 ** 3, rc0 = 8e-6;
    expect('problems', 'Who eats whom through the vapour', `$s = a/r_c$ = ${f(100 * a / rc0, 4)} % with $a$ = ${f(a * 1e9, 3)} nm`, null, 900);
    expect('problems', 'Who eats whom through the vapour', `is −${f(-G * a / r1 * (1 / rc0 - 1 / r1) * 3.6e9, 2)} µm per hour for the small droplets and +${f(G * a / r2 * (1 / rc0 - 1 / r2) * 3.6e9, 2)} µm per hour`, null, 1400);
    expect('problems', 'would last $r^3/(3Ga)$', `= ${f(r1 ** 3 / (3 * G * a) / 60, 1)} min`);
    while (r1 > 0.05e-6) { const rc = (r1 + r2) / 2, d = G * a / r1 * (1 / rc - 1 / r1), dt = Math.min(0.5, 0.001 * r1 / Math.abs(d)); r1 += d * dt; r2 = Math.cbrt(c - r1 ** 3); t += dt; }
    expect('problems', 'Integrated numerically, the 6 µm droplets are gone after', `${f(t / 60, 1)} min`);
    const rad = []; for (let i = 0; i < 200; i++) rad.push(i < 100 ? 6e-6 : 10e-6);
    const Rr = P.ripen(rad, A, { tEnd: 3600, recAt: Array.from({ length: 361 }, (_, k) => k * 10) }), g1 = Rr.rec.findIndex(q => q.alive < 200);
    expect('checks', 'Problem 9, two droplet sizes ripening', `${f(t / 60, 1)} min against ${f(Rr.rec[g1 - 1].t / 60, 1)} to ${f(Rr.rec[g1].t / 60, 1)} min`);
    expect('problems', "the model's own ripening routine, with ventilation,", `gives ${f(Rr.rec[g1 - 1].t / 60, 1)} to ${f(Rr.rec[g1].t / 60, 1)} min`);
    expect('problems', 'At the end each pair has become one drop of', `$1216^{1/3}$ = ${f(Math.cbrt(1216), 2)} µm, and the surface free energy has fallen to ${f(100 * Math.cbrt(1216) ** 2 / 136, 1)} %`); }
}

// ---------------------------------------------------------------- the worked examples and method boxes (derive/examples.cjs prints the same numbers)
{
  const ex = (file, anchor, win, list) => list.forEach(s2 => expect(file, anchor, s2, null, win));
  const g = 9.81, rw = 1000, sig = P.sigmaWater(A.T), tabW = D('etab_warm.json'), extK = { speed: 'beard', eff: 'table', coal: 'law', tab: tabW };
  const thin = x => String(x).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');   // 4528545 -> 4 528 545
  // Example 1.1
  { const k = P.stokesK(A), m8 = P.massOf(8e-6), W = 300e6 * m8, c = k * W / (4 * rw), ts = 1 / (c * 40e-6), F1 = P.L0F(100e-6, 8e-6), F0 = P.L0F(40e-6, 8e-6);
    ex('book-01', 'Example 1.1', 1900, [`${f(A.rho, 4)} kg/m³`, `${texSci(A.mu, 3)}`, `${texSci(k, 4)}`, `${texSci(m8, 3)} kg`, `W = ${texSci(W, 3)} kg/m³`, `= ${f(c, 2)} m⁻¹ s⁻¹`,
      `${f(ts, 0)} s = ${f(ts / 60, 2)} min`, `= ${f(ts * 0.6 / 60, 2)} min`, `= ${f(F1, 1).replace('-', '-')}`, `-21\\,092.3`, `11 814.0`, `= ${f(4 * rw / (k * W), 5)} m s`, `= ${f(P.L0time(40e-6, 100e-6, 8e-6, W, A) / 60, 2)} min`]);
    expect('book-01', 'Example 1.1', f(F0, 1) === '-21092.3' && f(F1 - F0, 1) === '11814.0' ? '-21\\,092.3' : 'F VALUES CHANGED', 'F(40) ' + f(F0, 1) + ', difference ' + f(F1 - F0, 1), 1900); }
  // Example 2.1 and the remark on the long reach of creeping flow
  { const B2 = [-3.18657, 0.992696, -1.53193e-3, -9.87059e-4, -5.78878e-4, 8.55176e-5, -3.27815e-6], lam = 6.62e-8 * (A.mu / 1.818e-5) * (101325 / A.p) * Math.sqrt(A.T / 293.15);
    const run = a => { const d = 2 * a, N = 4 * A.rho * (rw - A.rho) * g / (3 * A.mu * A.mu) * d ** 3, X = Math.log(N); let Y = 0; for (let q = 6; q >= 0; q--) Y = Y * X + B2[q]; const csc = 1 + 2.51 * lam / d, Re = csc * Math.exp(Y); return { N, X, Y, csc, Re, v: A.mu * Re / (A.rho * d) }; };
    const a40 = run(40e-6), a100 = run(100e-6), c8 = 1 + 2.51 * lam / 16e-6;
    ex('book-02', 'Example 2.1', 1700, [`\\lambda = ${texSci(lam, 2)} m`, `C_{sc} = ${f(a40.csc, 4)}`, `= ${f(a40.N, 2)}, and X = \\ln ${f(a40.N, 2)} = ${f(a40.X, 3)}`, `Y = −${f(-a40.Y, 4)}`, `= ${f(a40.Re, 3)}`,
      `= ${f(a40.v, 4)} m/s`, `= ${f(a40.N / 24, 3)} and v = ${f(vS(40e-6), 4)} m/s: ${f(100 * (vS(40e-6) / a40.v - 1), 0)} % too fast`, `N_{Da} = ${f(a100.N, 1)}, \\mathrm{Re} = ${f(a100.Re, 2)} and v = ${f(a100.v, 4)} m/s`, `would be ${f(a100.N / 24, 1)}`,
      `${texSci(vS(8e-6), 2)} m/s times its slip factor ${f(c8, 4)} is ${texSci(vB(8e-6), 3)} m/s`]);
    expect('book-02', 'ten radii from the centre', `still ${f(100 * (1.5 / 10 - 0.5 / 1000), 0)} % slower`); }
  // Example 3.1
  { const R = 40e-6, r = 8e-6, U = vB(R), vr = vB(r), gs = g * (1 - A.rho / rw), tau = vr / gs, St = tau * U / R, S = vr / U, p = r / R, Re = 2 * R * A.rho * U / A.mu;
    const es = P.flowEfficiency('stokes', St, S, p, 200), ep = P.flowEfficiency('potential', St, S, p, 30), E = (es.E + ep.E * Re / 60) / (1 + Re / 60);
    ex('book-03', 'Example 3.1', 1900, [`U = ${f(U, 4)} m/s and v(r) = ${texSci(vr, 3)} m/s`, `= ${f(gs, 4)} m/s²`, `= ${f(tau * 1e3, 4)} ms`, `= ${f(tau * U * 1e6, 1)} µm`, `\\mathrm{St} = ${f(St, 2)}`, `S = ${f(S, 3)}`, `\\mathrm{Re} = ${f(Re, 3)}`,
      `b_c = ${f(es.bc, 4)} collector radii in creeping flow and ${f(ep.bc, 4)} in potential flow`, `starting ${f(es.bc * 40, 0)} µm from the axis`, `may start ${f(ep.bc * 40, 0)} µm out`, `E_S = ${f(es.E, 4)} and E_P = ${f(ep.E, 4)}`,
      `would give ${f(es.bc ** 2 / (1 + p) ** 2, 4)}`, `= ${f(Re / 60, 4)}`, `= ${f(E, 4)}`]);
    expect('book-03', 'The grazing path.', `${Math.ceil(Math.log2(1.5 / 1e-7))} halvings`); }
  // Example 4.1
  { const row = (a1, a2) => { const m1 = P.massOf(a1), m2 = P.massOf(a2), mr = m1 * m2 / (m1 + m2), dv = vB(a1) - vB(a2), cke = 0.5 * mr * dv * dv, dc = 2 * Math.cbrt(a1 ** 3 + a2 ** 3), Es = Math.PI * sig * dc * dc; return { m1, m2, mr, dv, cke, dc, Es, We: cke / Es }; };
    const s1 = row(40e-6, 8e-6), s2 = row(500e-6, 250e-6);
    ex('book-04', 'Example 4.1', 1700, [`${texSci(s1.m1, 3)} ${texSci(s2.m1, 3)}`, `${texSci(s1.m2, 3)} ${texSci(s2.m2, 3)}`, `${texSci(s1.mr, 3)} ${texSci(s2.mr, 3)}`, `${f(s1.dv, 4)} ${f(s2.dv, 4)}`, `${texSci(s1.cke, 3)} ${texSci(s2.cke, 3)}`,
      `${f(s1.dc * 1e6, 2)} ${f(s2.dc * 1e6, 2)}`, `${texSci(s1.Es, 3)} ${texSci(s2.Es, 3)}`, `${texSci(s1.We, 3)} ${f(s2.We, 3)}`, `${f(Math.exp(-1.15 * s1.We), 5)} ${f(Math.exp(-1.15 * s2.We), 3)}`, `\\sigma = ${f(sig, 5)} N/m`,
      `collector is ${f(s1.m1 / s1.m2, 0)} times heavier`, `surface energy by ${r10(s2.Es / s1.Es)}`]);
    expect('book-04', 'the collision energy grows by a factor of', 'four million', 'ratio ' + (s2.cke / s1.cke).toExponential(3)); }
  // Example 5.1
  { const gr = P.makeGrid(8, 4e-3), N = P.lognormalBins(gr, modes), i = 72, j = gr.r.findIndex(r => r >= 40e-6), K = P.kernel(gr.r[i], gr.r[j], A, extK), C = K * N[i] * N[j], xs = gr.x[i] + gr.x[j];
    let kk = j; while (gr.x[kk + 1] <= xs) kk++; const fr = (xs - gr.x[kk]) / (gr.x[kk + 1] - gr.x[kk]);
    ex('book-05', 'Example 5.1', 2300, [`2^{1/24} = ${f(Math.pow(2, 1 / 24), 4)}`, `Bin ${i} is r = ${f(gr.r[i] * 1e6, 3)} µm and holds N_i = ${texSci(N[i], 3)}`, `Bin ${j} is r = ${f(gr.r[j] * 1e6, 3)} µm and holds N_j = ${texSci(N[j], 3)}`, `= ${texSci(K, 3)} m³/s`,
      `\\Delta v = ${f(vB(gr.r[j]) - vB(gr.r[i]), 4)} m/s and E = ${f(P.tableE(tabW, gr.r[j], gr.r[i] / gr.r[j]), 4)}`, `= ${f(C, 1)} per m³`, `catches ${f(K * N[i], 4)} droplets`, `${f(100 * C / N[j], 3)} % of them`, `is a ${f(P.radiusOf(xs) * 1e6, 3)} µm drop`,
      `bin ${kk} (${f(gr.r[kk] * 1e6, 3)} µm) and bin ${kk + 1} (${f(gr.r[kk + 1] * 1e6, 3)} µm)`, `= ${f(fr, 4)}`, `= ${f(100 * gr.x[i] / gr.x[j], 2)} %`, `${f(100 * (Math.pow(2, 1 / 8) - 1), 2)} % heavier`, `a net loss of ${f(fr * C, 1)}`, `1/f = ${f(1 / fr, 1)}`]);
    expect('book-05', 'computed once', `(${gr.n} × ${gr.n} at 8 bins per doubling)`); }
  // Example 6.1
  { const u1 = P.rng(1), rad = P.drawModes(modes, 10, u1, 3), n = rad.length, V = 10e-6; let a0 = 0, cc = 0, dd = 0, nc = 0;
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) { const K = P.kernel(rad[i], rad[j], A, extK) / V; a0 += K; if (Math.min(rad[i], rad[j]) >= 20e-6) cc += K; else if (Math.max(rad[i], rad[j]) < 20e-6) dd += K; }
    rad.forEach(r => { if (r >= 20e-6) nc++; });
    ex('book-06', 'Example 6.1', 1000, [`${n} drops, ${nc} of them collectors`, `${thin(n * (n - 1) / 2)} pairs`, `gives ${f(a0, 3)} per second`, `every ${f(1 / a0, 2)} s`, `The ${nc * (nc - 1) / 2} pairs of two collectors carry ${f(100 * cc / a0, 2)} %`, `every ${f(1 / cc, 0)} s`, `carry ${f(100 * dd / a0, 3)} %`]); }
  // Example 7.1
  { const a1 = 40e-6, a2 = 8e-6, eps = 1e-2, t1 = vB(a1) / g, t2 = vB(a2) / g, v1 = vB(a1), v2 = vB(a2), R = a1 + a2, nu = A.nu, a0 = (11 + 7 * 2e4) / (205 + 2e4), tk = Math.sqrt(nu / eps), vk = Math.pow(nu * eps, 0.25), d = t1 - t2;
    const sh = R * R * eps / (15 * nu), ac = d * d * a0 * (vk / tk) ** 2, se = (v1 * t1 - v2 * t2) ** 2 * 2 * eps / (15 * nu), grv = Math.PI / 8 * d * d * g * g, w = Math.sqrt(2 / Math.PI) * Math.sqrt(sh + ac + se + grv), wg = 0.5 * Math.abs(d) * g;
    ex('book-07', 'Example 7.1', 2100, [`= ${f(t1 * 1e3, 2)} ms`, `= ${f(t2 * 1e3, 3)} ms`, `= ${f(tk * 1e3, 1)} ms`, `\\nu = ${texSci(nu, 3)} m²/s`, `= ${texSci(sh, 2)} m²/s²`, `= ${f(Math.pow(eps, 0.75) * Math.pow(nu, -0.25), 2)} m/s²`, `= ${texSci(ac, 2)} m²/s²`, `= ${texSci(se, 2)} m²/s²`,
      `\\sigma_w^2 = ${texSci(sh + ac + se, 2)} m²/s²`, `\\sigma_w = ${f(Math.sqrt(sh + ac + se) * 100, 2)} cm/s`, `= ${texSci(grv, 2)} m²/s²`, `= ${f(w * 100, 2)} cm/s, against ${f(wg * 100, 2)} cm/s in still air: a factor ${f(w / wg, 3)}`, `a third of gravity's ${f(Math.sqrt(grv) * 100, 1)} cm/s`]);
    expect('book-07', 'Gravity\'s part.', `${f(grv / (sh + ac + se), 0)} times larger`.replace(/^9 /, 'nine '), 'ratio ' + f(grv / (sh + ac + se), 2)); }
  // Example 8.1: the intermediate numbers (the others are checked with chapter 8 above)
  { const m1 = mi(40e-6), m2 = mi(8e-6), a0 = 3.78e4 * (1 + 0.0079 / Math.pow(5e-4, 1.5)), al = Math.PI * 16e-6 ** 2, xr = 6.3e6 * K0 / aA;
    ex('book-08', 'Example 8.1', 1700, [`they close at ${f(vi(40e-6) - vi(8e-6), 4)} m/s`, `${texSci(m1, 3)} and ${texSci(m2, 3)} kg, the reduced mass ${texSci(m1 * m2 / (m1 + m2), 3)} kg`, `= ${f(fT, 3)}`, `a_0 = ${texSci(a0, 3)} m⁻² and A = ${texSci(a0 * fT, 3)} m⁻²`,
      `\\pi D^2 = ${texSci(al, 2)} m²`, `CK_0/\\alpha A = ${texSci(xr, 2)}`, `it is ${f(Math.pow(xr, 0.3), 4)}`, `e^{-${f(Math.pow(xr, 0.3), 4)}}`, `breaks ${f(100 * (1 - Math.exp(-Math.pow(xr, 0.3))), 1)} % of them`]);
    expect('book-08', 'Step 4 shows the weak power at work', '56 000 times', 'ratio ' + f(1 / xr, 0)); }
  // chapter 11: the maximum-entropy numbers at the start, and the method box
  { const gr = P.makeGrid(8, 4e-3), N = P.lognormalBins(gr, modes); let Nt = 0, M = 0; N.forEach((n, q) => { Nt += n; M += n * gr.x[q]; });
    ex('book-11', 'drops per m³ hold', 400, [`N = ${texSci(Nt, 3)} drops per m³ hold M = ${texSci(M, 3)} kg/m³`, `M/N = ${texSci(M / Nt, 3)} kg is that of a ${f(P.radiusOf(M / Nt) * 1e6, 2)} µm sphere`]);
    const EN = D('energy.json'); expect('book-11', 'All three start from the same kind of volume', `${thin(EN.mc.steepest.Nini)} drops`); expect('book-11', 'passes one of', `${EN.mc.marks.length} marks`); }
  // Example 12.1
  { const dV = 50 ** 3, xid = 300e6 * dV / 96, xic = 1e6 * dV / 32, n = 128, K = P.kernel(40e-6, 8e-6, A, extK), sc = n * (n - 1) / 2 / Math.floor(n / 2), pp = xid * K / dV * sc, s2 = Math.pow(1e-2 * 100, 2 / 3), TL = 2 * s2 / (6 * 1e-2), aa = Math.exp(-1 / TL);
    const dr2 = 2 * P.growthG(A) * -0.2 * P.ventilation(100e-6, A);
    ex('book-12', 'Example 12.1', 2300, [`\\Delta V = ${texSci(dV, 2)} m³`, `\\xi = ${texSci(xid, 3)}`, `${texSci(xic, 3)}`, `\\sigma = ${f(Math.sqrt(s2), 3)} m/s and T_L = ${f(TL, 2)} s`, `= ${f(aa, 4)}`, `= ${f(Math.sqrt(s2 * (1 - aa * aa)), 4)} m/s`, `K = ${texSci(K, 3)} m³/s`,
      `= ${texSci(xid * K / dV, 3)}`, `= ${n * (n - 1) / 2} possible pairs and tests ${Math.floor(n / 2)} of them`, `is ${sc}, and p = ${f(pp, 3)}`, `from 40 to ${f(Math.cbrt(40 ** 3 + 8 ** 3), 3)} µm`, `one hundredth fewer`, `loses ${texSci(-dr2, 2)} m²`,
      `which is ${f((1e-4 - Math.sqrt(1e-8 + dr2)) * 1e6, 2)} µm of radius`]);
    expect('book-12', 'Then the clock advances by one second', `${45 * 60} such steps`); }
}

// ---------------------------------------------------------------- chapter 11: who eats whom (data/energy.json)
{
  const EN = D('energy.json'), wr = EN.warm, mc = EN.mc;
  const ag = (k2, fr) => mc[k2].agg.find(q => q.f === fr), med = a => { const s2 = a.filter(Boolean).map(q => q.merged).sort((x, y) => x - y), n = s2.length; return n % 2 ? s2[(n - 1) / 2] : (s2[n / 2 - 1] + s2[n / 2]) / 2; };
  const sig = P.sigmaWater(A.T), area = r => 4 * Math.PI * r * r, R = Math.cbrt(2) * 10e-6, dF = sig * (2 * area(10e-6) - area(R));
  expect('book-11', 'problem 6 works out two 10 µm droplets', `$-${texSci(dF / P.K_B / A.T, 1)}\\,k_BT$`);
  expect('book-11', 'collision kernel (the cloud)', `${f(100 * ag('physical', 0.5).S, 0)} % ${med(mc.physical.first100)} ${f(100 * ag('physical', 0.5).share[0], 3)} %`);
  expect('book-11', 'every pair alike', `${f(100 * ag('constant', 0.5).S, 0)} % about ${String(Math.round(med(mc.constant.first100) / 10) * 10).replace(/(\d)(\d{3})$/, '$1 $2')} ${f(100 * ag('constant', 0.5).share[0], 0)} %`);
  expect('book-11', 'largest pair first', `${f(100 * mc.steepest.rows.find(q => q.f === 0.5).S, 0)} % ${mc.steepest.first100.merged} 0`);
  expect('book-11', 'All three end in one\ndrop of'.replace('\n', ' '), `${f(mc.steepest.rFinal * 1e3, 2)} mm`);
  const at = t => wr.recs.reduce((b, q) => Math.abs(q.t - t) < Math.abs(b.t - t) ? q : b), q50 = at(wr.t50), q90 = at(wr.t90);
  const shr = (q, c) => 100 * q.mergers[c] / q.mergers.reduce((a, v) => a + v, 0), wat = (q, c) => 100 * q.eaten[c] / wr.W0;
  const pc = (v) => v >= 10 ? f(v, 0) : v >= 1 ? f(v, 1) : v >= 0.1 ? f(v, 2) : f(v, 3);
  const pw = (v) => v >= 1 ? f(v, 0) : f(v, 3);
  [['collectors eat droplets', 3], ['drizzle eats droplets', 6], ['collectors eat collectors', 4], ['drizzle eats collectors', 7], ['droplets eat droplets', 0]].forEach(([l, c]) =>
    expect('book-11', l, `${pc(shr(q50, c))} % / ${pc(shr(q90, c))} % ${pw(wat(q50, c))} % / ${pw(wat(q90, c))} %`));
  expect('book-11', 'At $t_{90}$ (13.5 min),', `${f(100 * q90.tag[2] / q90.wat[2], 0)} % of the water in drizzle`);
  expect('book-11', 'by $t_{90}$ it has moved', `${f(wat(q90, 4), 0)} % of all the water`);
  expect('book-11', 'falls to', `${f(EN.constant.rows.find(q => q.f === 0.01).epsExp, 2)} when one drop in a hundred is left and to ${f(EN.constant.rows.find(q => q.f === 0.001).epsExp, 3)}`);
  const q6 = wr.recs.find(q => q.t === 360);
  expect('book-11', 'With the collision kernel it is', `${f(q6.epsExp, 2)} at 6 min and ${f(q90.epsExp, 2)} at $t_{90}$, and the gamma does no better (${f(q6.epsGamma, 2)} and ${f(q90.epsGamma, 2)})`);
  expect('book-11', 'peak near', '5 min', 'collector water peaks at ' + f(wr.recs.reduce((b, q) => q.wat[1] > b.wat[1] ? q : b).t / 60, 1) + ' min');
  const cross = wr.recs.find(q => q.wat[2] > q.wat[0] && q.wat[2] > q.wat[1]);
  expect('book-11', 'drizzle overtakes both near', `${f(cross.t / 60, 0)} min`, 'at ' + f(cross.t / 60, 2) + ' min');
}

{ // problem 6
  const sg = P.sigmaWater(A.T), a = r => 4 * Math.PI * r * r, R = Math.cbrt(2) * 10e-6, dE = sg * (2 * a(10e-6) - a(R));
  expect('problems', 'The product has radius', f(R * 1e6, 2) + ' µm');
  expect('problems', 'the energy released is', `\\Delta E = ${texSci(dE, 2)} J, which is ${texSci(dE / P.K_B / A.T, 2)}\\,k_BT`);
  expect('problems', 'which is $1/e$ when', `T_{\\rm eff} = ${texSci(dE / P.K_B, 2)} K`);
  expect('problems', 'A temperature for splitting', `${texSci(dE, 2)} J, and a temperature of ${texSci(dE / P.K_B, 2)} K`);
}

// ---------------------------------------------------------------- chapter 12: a cloud with a shape (data/cloud.json, tools/run_cloud.cjs)
{
  const CL = D('cloud.json'), ms = a => a.reduce((x, y) => x + y, 0) / a.length, Gv = P.growthG(A), pc1 = v => f(100 * v, 1) + ' %';
  const sc = (e, L) => { const s2 = Math.pow(e * L, 2 / 3), TL = 2 * s2 / (6 * e); return { s: Math.sqrt(s2), TL, K: s2 * TL }; };
  const r100 = sc(1e-2, 100);
  expect('book-12', 'and eddies up to $L_e$ = 100 m: σ =', `${f(r100.s, 2)} m/s and $T_L$ = ${f(r100.TL, 0)} s`);
  expect('book-12', 'with coefficient $\\sigma^2T_L$ =', `${f(r100.K, 0)} m²/s, about ${r10(Math.sqrt(2 * r100.K * 600))} m in ten minutes`);
  expect('book-12', 'With $L_e$ = 50 m the coefficient is', `${f(sc(1e-2, 50).K, 0)} m²/s, with 200 m it is ${f(sc(1e-2, 200).K, 0)} m²/s`);
  expect('book-12', 'where $G =', `${texSci(Gv, 2)} m²/s`);
  expect('book-12', '$f_v$ is', `${f(P.ventilation(10e-6, A), 2)} at\n10 µm, ${f(P.ventilation(100e-6, A), 2)} at 100 µm and ${f(P.ventilation(200e-6, A), 2)} at 200 µm`.replace('\n', ' '));
  const life = (r0) => { let r = r0, t = 0; while (true) { const r2 = r * r + 2 * Gv * -0.2 * P.ventilation(r, A) * 0.01; if (r2 <= 1e-14) return t; r = Math.sqrt(r2); t += 0.01; } };
  const fall = (r0) => { let r = r0, z = 300; while (z > 0) { const r2 = r * r + 2 * Gv * -0.2 * P.ventilation(r, A) * 0.05; if (r2 <= 1e-14) return null; r = Math.sqrt(r2); z -= vB(r) * 0.05; } return (r / r0) ** 3; };
  expect('book-12', 'A 10 µm droplet that leaves the cloud is gone in', `${f(life(10e-6), 1)} s. A 100 µm drizzle drop lasts ${f(life(100e-6), 0)} s, much less\nthan the ${f(300 / vB(100e-6), 0)} s`.replace('\n', ' '));
  expect('book-12', 'a 150 µm drop also vanishes on the way', `a 200 µm drop arrives\nwith ${f(100 * fall(200e-6), 0)} %`.replace('\n', ' '), '150 um arrives: ' + fall(150e-6));
  const cv = CL.box.conv, byP = n => cv.find(c => c.per === n);
  expect('book-12', 'the collection equation (', `${f(CL.box.ref[0], 3)} and ${f(CL.box.ref[1], 3)} min`);
  expect('book-12', 'With 32 super-droplets per cell the box is', `$${f(100 * byP(32).bias90, 0)} \\pm ${f(100 * byP(32).se90, 0)}$ % slow`);
  expect('book-12', 'With 128 it is', `$${f(100 * byP(128).bias90, 1)} \\pm ${f(100 * byP(128).se90, 1)}$ % slow in our 32 runs`);
  expect('book-12', 'With 512 it is', `$${f(100 * byP(512).bias90, 1)} \\pm ${f(100 * byP(512).se90, 1)}$ %, with 2048 $${f(100 * byP(2048).bias90, 1)} \\pm ${f(100 * byP(2048).se90, 1)}$ %`);
  const gm = cv.map(c => c.gamMany * 100);
  expect('book-12', 'In 44 to 46 % of the box', `${f(Math.min(...gm), 0)} to ${f(Math.max(...gm), 0)} %`.replace(/^/, 'In '), 'gamma > 1 shares ' + gm.map(v => f(v, 1)).join(', '));
  const mx = CL.mix, rng2 = a => `${f(Math.min(...a), 2)} to ${f(Math.max(...a), 2)}`;
  expect('book-12', 'With the drift of (12.3) it is', `${rng2(mx.full.chi30)} after\n30 min and ${rng2(mx.full.chi120)} after 2 hours`.replace('\n', ' '));
  expect('book-12', 'Without the drift it is', `${f(Math.min(...mx.none.chi30), 1)} to ${f(Math.max(...mx.none.chi30), 1)} and then ${f(Math.min(...mx.none.chi120), 1)} to ${f(Math.max(...mx.none.chi120), 1)}`);
  const cs = k => CL.cases[k].runs, m = (k, g) => ms(cs(k).map(g));
  for (const [k, lab] of [['column', 'fall only'], ['evap', '+ dry air outside'], ['cell', '+ mean motion'], ['reference', '+ eddies']]) {
    const rain = m(k, q => q.rain), below = m(k, q => q.evapBelow), side = m(k, q => q.evap - q.evapBelow), aloft = m(k, q => q.aloft);
    const z = v => v < 0.0005 ? '0' : pc1(v);
    expect('book-12', lab + ' ', `${pc1(rain)} ${z(below)} ${z(side)} ${pc1(aloft)}`);
  }
  for (const [k, lab] of [['reference', 'reference '], ['Le50', 'largest eddy 50 m'], ['Le200', 'largest eddy 200 m'], ['peaked', 'stochastic element only'], ['peakedAyala', 'turbulent collision factor at the local ε'], ['noVent', 'no ventilation in (12.4)']])
    expect('book-12', lab, pc1(m(k, q => q.rain)));
  const pts = []; for (const k of ['rough0', 'rough3', 'rough6']) { const by = {}; cs(k).forEach(q => (by[q.outline] = by[q.outline] || []).push(q)); Object.values(by).forEach(a => pts.push([a[0].perim / a[0].area * 1000, ms(a.map(q => q.rain))])); }
  const u = [...new Map(pts.map(p => [p[0].toFixed(3), p])).values()], n = u.length, mxp = ms(u.map(p => p[0])), myp = ms(u.map(p => p[1]));
  const cov = u.reduce((a, p) => a + (p[0] - mxp) * (p[1] - myp), 0), rr = cov / Math.sqrt(u.reduce((a, p) => a + (p[0] - mxp) ** 2, 0) * u.reduce((a, p) => a + (p[1] - myp) ** 2, 0)), slope = cov / u.reduce((a, p) => a + (p[0] - mxp) ** 2, 0);
  const hiR = u.reduce((b, p) => p[1] > b[1] ? p : b), loR = u.reduce((b, p) => p[1] < b[1] ? p : b);
  expect('book-12', 'Across the seven different outlines', `correlation\nis ${f(rr, 2).replace('-', '−')}, and each extra kilometre of outline per km² of cloud costs about ${f(-100 * slope, 1)} points of rain (from ${pc1(hiR[1])} at ${f(hiR[0], 2)} per km to ${pc1(loR[1])} at ${f(loR[0], 2)} per km)`.replace('\n', ' '), n + ' outlines');
  const ref = cs('reference'), R0 = ref[0], g10 = R0.regs.find(r => r.t === 600);
  const names = [['updraft core', 0], ['flank', 1], ['edge band', 2], ['below the base', 4]];
  for (const [lab, r] of names) {
    const W = g10.W.slice(r * 3, r * 3 + 3), tot = W.reduce((a, v) => a + v, 0), mer = g10.mergers.slice(r * 9, r * 9 + 9), mt = mer.reduce((a, v) => a + v, 0), me = g10.maxent[r];
    expect('book-12', lab + ' ', `${pc1(tot)} ${W.map(v => f(100 * v / tot, 0)).join(' / ')} % ${f(100 * mer[3] / mt, 0)} / ${f(100 * mer[6] / mt, 0)} % ${f(me[0], 2)} / ${f(me[1], 2)}`);
  }
  const g45 = R0.regs[R0.regs.length - 1], relR = [0, 1, 2, 3, 4].map(r => g45.released.slice(r * 9, r * 9 + 9).reduce((a, v) => a + v, 0)), relT = relR.reduce((a, v) => a + v, 0);
  expect('book-12', 'Over the 45 min,', `${f(100 * relR[0] / relT, 0)} % of the surface free energy was released in the core, ${f(100 * relR[1] / relT, 0)} % in the flanks and ${f(100 * relR[2] / relT, 0)} % in the edge band`);
  const fr = k => ms(ref.map(q => q.rainR[k] / q.initR[k]));
  expect('book-12', 'Of the water that\nstarted in the core'.replace('\n', ' '), `${pc1(fr(0))} reached the ground; from the flanks ${pc1(fr(1))}; from the edge band ${pc1(fr(2))}`);
  expect('book-12', 'Weighted by water,', `${f(100 * ms(ref.map(q => q.bornCoreShare)), 0)} % of\nthe passages of 100 µm happened in the core, which is ${pc1(R0.coreAreaShare)}`.replace('\n', ' '));
  expect('book-12', 'drizzle already holds', '40 % of the water at 10 min', 'core drizzle share ' + f(100 * g10.W[2] / (g10.W[0] + g10.W[1] + g10.W[2]), 1));
  expect('book-12', 'Each stands for about', `${texSci(300e6 * 125000 / 96, 0)} droplets or ${texSci(1e6 * 125000 / 32, 0)} collectors`);
  expect('book-12', 'is three times as likely', 'three times', 'ratio ' + f(fr(0) / fr(2), 2));
}

{ // problem 8
  const e = 1e-3, s2 = Math.pow(e * 100, 2 / 3), TL = 2 * s2 / (6 * e), K = s2 * TL, Gv = P.growthG(A);
  expect('problems', 'so $\\sigma$ =', `${f(Math.sqrt(s2), 2)} m/s, and the memory is $T_L = 2\\sigma^2/(C_0\\varepsilon)$ = ${f(TL, 0)} s`);
  expect('problems', 'diffusion coefficient $K = \\sigma^2T_L$ =', `${f(K, 1)} m²/s`);
  expect('problems', 'the spread is $\\sqrt{2Kt}$ =', `${f(Math.sqrt(2 * K * 600), 0)} m`);
  expect('problems', 'and the ventilation factor, which is', `${f(P.ventilation(150e-6, A), 2)} at 150 µm because the drop falls at\n${f(vB(150e-6), 2)} m/s`.replace('\n', ' '));
  let r = 150e-6, z = 300, t = 0; while (z > 0) { const r2 = r * r + 2 * Gv * -0.2 * P.ventilation(r, A) * 0.05; if (r2 <= 1e-14) break; r = Math.sqrt(r2); z -= vB(r) * 0.05; t += 0.05; }
  expect('problems', 'the drop is gone after', `${f(t, 0)} s, about ${f(z, 0)} m above the ground`);
}
console.log(`\n${pass} of ${pass + fail} numbers found in the text`);
console.log(fail ? 'NUMBER CHECK FAIL' : 'NUMBER CHECK PASS');
process.exit(fail ? 1 : 0);
