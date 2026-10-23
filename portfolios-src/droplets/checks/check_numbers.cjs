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
console.log(`\n${pass} of ${pass + fail} numbers found in the text`);
console.log(fail ? 'NUMBER CHECK FAIL' : 'NUMBER CHECK PASS');
process.exit(fail ? 1 : 0);
