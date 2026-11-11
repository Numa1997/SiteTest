// The figures and numbers of the Fig. 12 lecture note's sections on the real glass (Part D, 11 November 2026), in the house
// chart style (white plate, Plex Mono ticks): node tools/fig12/figures-d.cjs [out dir]
// Reads only the page's data and engine: public/data/fig12/modes.json and nm.json (tools/fig12/modes_fem.py, nm_tulip.py) and
// public/scripts/stout-modal.js. Writes three SVGs into [out dir] (default: the system's temporary folder, fig12-figures-d/) for
// pasting into the note, and prints every number the note quotes from them:
//   fig-d-freq.svg   f11 of the tulip against the fill height (finite elements), a straight cylinder of the same surface radius
//                    and depth beside it (exact), and the wall's slope at the surface
//   fig-d-damp.svg   the damping ratio of the first mode from the wall layer, the surface skin and the bulk, against the fill
//                    (the stout's viscosity, as the page)
//   fig-d-decay.svg  a free swing released at 5 mm wall height, the page's model (TulipNM as the page builds it) with heads of
//                    0, 5 and 15 mm, and with friction off; Viola et al.'s arrest time t* (their eq. 7.6) marked for each head
const fs = require('fs'), path = require('path'), os = require('os');
const root = path.join(__dirname, '../..');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(root, 'public/scripts', f), 'utf8'))(m); return m.exports; };
const G = load('guinness-glass.js'), { TulipNM } = load('stout-modal.js');
const rd = (f) => JSON.parse(fs.readFileSync(path.join(root, 'public/data/fig12', f), 'utf8'));
const data = rd('modes.json'), nmData = rd('nm.json');
const out = process.argv[2] || path.join(os.tmpdir(), 'fig12-figures-d'); fs.mkdirSync(out, { recursive: true });
const f1 = (v) => v.toFixed(1);
const INK = '#1c1518', MUTED = '#8b8079', GRID = '#eee6d9', WINE = '#7a1f2b', DARK = '#4a413d';
const g = data.g, XI = 1.8411837813, NU = 2.05e-6;
const Rz = (z) => { const P = G.R, f = z / G.dz, i = Math.min(P.length - 2, Math.floor(f)); return P[i] + (f - i) * (P[i + 1] - P[i]); };
const hs = data.h, L = data.levels;
const row = (h) => hs.indexOf(h);

// ------------------------------------------------------------------ numbers
const fT = L.map((l) => l.m1.f[0]);
const fC = hs.map((h, i) => { const R = data.R_surface[i], H = h / 1000; return Math.sqrt(g * XI / R * Math.tanh(XI * H / R)) / (2 * Math.PI); });
const slope = hs.map((h) => (Rz(h / 1000 + 2e-4) - Rz(h / 1000 - 2e-4)) / 4e-4);
let imin = 0; fT.forEach((v, i) => { if (v < fT[imin]) imin = i; });
console.log('f11 of the tulip (finite elements) against the fill: h mm, R(h) mm, wall slope dR/dz, f11 Hz, cylinder of the same R(h) and depth Hz, difference %');
for (const h of [30, 40, 50, 60, 70, 77.5, 80, 90, 92.5, 100, 110, 115, 120, 125, 130, 140, 145]) {
  const i = row(h); console.log(`  ${h}  ${(data.R_surface[i] * 1000).toFixed(2)}  ${slope[i].toFixed(3)}  ${fT[i].toFixed(4)}  ${fC[i].toFixed(4)}  ${((fT[i] / fC[i] - 1) * 100).toFixed(2)}`);
}
console.log(`  lowest f11 ${fT[imin].toFixed(4)} Hz at ${hs[imin]} mm; largest shortfall against the cylinder ${Math.min(...fT.map((v, i) => (v / fC[i] - 1) * 100)).toFixed(2)} %`);
{
  const i = row(125), m1 = L[i].m1, R = data.R_surface[i], k = m1.kappa;
  const M = 1000 * m1.Ix[0] / (k[0] * m1.c[0]);
  console.log(`125 mm: R(h) ${(R * 1000).toFixed(2)} mm; m = 1: f ${m1.f.slice(0, 3).map((v) => v.toFixed(4)).join(', ')} Hz; kappa ${k.slice(0, 3).join(', ')} 1/m; kappa R ${(k[0] * R).toFixed(4)}`);
  console.log(`  push coefficients c_n ${m1.c.slice(0, 4).map((v) => (v * 1000).toFixed(3)).join(', ')} mm; c_1/R ${(m1.c[0] / R).toFixed(4)} (cylinder 2/(xi^2-1) = ${(2 / (XI * XI - 1)).toFixed(4)}); sum over 40 modes ${m1.c_sum_40_over_R} R`);
  let s4 = 0; for (let n = 0; n < 4; n++) s4 += m1.c[n] * m1.e[n][m1.e[n].length - 1];
  console.log(`  steady wall rise per m/s^2: mode 1 ${(-m1.c[0] / g * 1000).toFixed(3)} mm, 4 modes ${(-s4 / g * 1000).toFixed(3)} mm, the plane -R/g ${(-R / g * 1000).toFixed(3)} mm`);
  console.log(`  Ix_1 ${m1.Ix[0].toExponential(4)} m^3 (cylinder pi R^3/xi^2 = ${(Math.PI * R ** 3 / XI ** 2).toExponential(4)}); modal mass rho Ix/(kappa c) ${(M * 1000).toFixed(2)} g; rho Ix/c ${(1000 * m1.Ix[0] / m1.c[0]).toFixed(3)} kg/m (not a mass)`);
  console.log(`  momentum per unit wall speed rho Ix ${(1000 * m1.Ix[0] * 1000).toFixed(2)} g = (kg m/s)/(m/s)`);
  const w = 2 * Math.PI * m1.f[0], sq = 0.5 * Math.sqrt(NU / (2 * w));
  const zw = sq * m1.Lam[0], zs = sq * m1.LamS[0], zb = NU * m1.Bk[0] / w;
  console.log(`  friction, nu ${NU}: Lambda ${m1.Lam[0]} 1/m (Lambda R ${(m1.Lam[0] * R).toFixed(4)}), LamS ${m1.LamS[0]} (LamS R ${(m1.LamS[0] * R).toFixed(4)}), Bk ${m1.Bk[0]} (Bk R^2 ${(m1.Bk[0] * R * R).toFixed(3)}; deep water 2 xi^2 = ${(2 * XI * XI).toFixed(3)})`);
  console.log(`  zeta wall ${zw.toFixed(5)}, skin ${zs.toFixed(5)}, bulk ${zb.toFixed(5)}, sum ${(zw + zs + zb).toFixed(5)}; Stokes layer delta = sqrt(2 nu/w) ${(Math.sqrt(2 * NU / w) * 1000).toFixed(3)} mm; e-folding time of the amplitude 1/(zeta w) ${(1 / ((zw + zs + zb) * w)).toFixed(2)} s`);
  console.log(`  with water's nu 1e-6: wall ${(0.5 * Math.sqrt(1e-6 / (2 * w)) * m1.Lam[0]).toFixed(5)}`);
  console.log(`  deep cylinder: K = (pi/sqrt2)(xi^2+1)/(xi^2-1) xi^(-1/4) = ${(Math.PI / Math.SQRT2 * (XI * XI + 1) / (XI * XI - 1) * Math.pow(XI, -0.25)).toFixed(4)}; Lambda R = ${((XI * XI + 1) / (XI * XI - 1)).toFixed(4)}`);
  const e1 = m1.e[0]; console.log(`  mode-1 shape e(r) at r/R = 0, 0.25, 0.5, 0.75, 1: ${[0, 8, 16, 24, 32].map((j) => e1[j].toFixed(4)).join(', ')}`);
}
// the large-swing coefficients against the fill
console.log('large swings (nm.json): h mm, d1, d2, sigma1^2 (= kappa R)');
for (const h of [50, 75, 100, 125, 140]) { const N = nmData.levels[nmData.h.indexOf(h)]; console.log(`  ${h}  ${N.d.d1.toFixed(4)}  ${N.d.d2.toFixed(4)}  ${N.sigma2.p1.toFixed(4)}`); }
{ const N = nmData.levels[nmData.h.indexOf(125)], M1 = 1000 * N.Rs ** 3 * N.mu.p1 / N.Rw[1] ** 2; console.log(`  modal mass from nm.json rho R^3 mu_1 / Rw1^2 = ${(M1 * 1000).toFixed(2)} g`); }

// the page's model as the page builds it
const page = (o) => new TulipNM(Object.assign({ data, nmData, profile: G, h0: 0.125, nModes: 3, skin: 1, foam: { h: 0.015 }, friction: true, dx: 0.004 }, o || {}));
console.log('the foam (the page model at 125 mm): head mm, h_eff mm, alpha, Viola arrest time t* from 5 mm s, model: time to 1/e of 5 mm s, to 1 % s');
const X0 = 0.005, c = 0.5356;
function release(o, T) {
  const f = page(o); f.b[1] = X0 / (f.Rs * f.Rw[1]); f.b[2] = 0; f.syncQ();
  const dt = 0.001, ys = []; let te = null, t1 = null, last = 0;
  for (let k = 0; k * dt < T - 1e-9; k++) {
    f.step(dt, 0, 0); const y = f.wallAt(0) - f.h; ys.push([+(k * dt + dt).toFixed(3), y]);
    if (Math.abs(y) > 1e-6 * X0) last = k * dt + dt;
  }
  // envelope: largest |y| from each time on (the amplitude still to come)
  const env = new Array(ys.length); let m = 0; for (let k = ys.length - 1; k >= 0; k--) { m = Math.max(m, Math.abs(ys[k][1])); env[k] = m; }
  for (let k = 0; k < ys.length; k++) { if (te === null && env[k] < X0 / Math.E) te = ys[k][0]; if (t1 === null && env[k] < 0.01 * X0) t1 = ys[k][0]; }
  return { f, ys, te, t1, last };
}
const runs = {};
for (const hh of [0, 5, 10, 15, 20]) {
  const r = release({ foam: { h: hh / 1000 } }, 8); runs[hh] = r; const f = r.f;
  const n = 2 / 3, l = f.Rs / XI, heff = l / (n + 1) * (1 - Math.exp(-(n + 1) * hh / 1000 / l));
  const s0 = f.zeta[0], w = f.w[0], u0 = Math.cbrt(X0 / f.Rs);
  const tStar = f.alpha > 0 ? 3 / (s0 * w) * Math.log(1 + s0 * u0 / (c * f.alpha)) : Infinity;
  r.tStar = tStar;
  console.log(`  ${hh}  ${(heff * 1000).toFixed(2)}  ${f.alpha.toFixed(4)}  ${tStar.toFixed(2)}  ${r.te}  ${r.t1}   (zeta of the linear terms ${s0.toFixed(5)}; effective zeta from the foam at 5 / 1 mm: ${(c * f.alpha * Math.pow(X0 / f.Rs, -1 / 3)).toFixed(3)} / ${(c * f.alpha * Math.pow(0.001 / f.Rs, -1 / 3)).toFixed(3)})`);
}
{ const r = release({ friction: false }, 8); runs.off = r; console.log(`  friction off: amplitude after 8 s ${(Math.max(...r.ys.slice(-400).map((p) => Math.abs(p[1]))) * 1000).toFixed(3)} mm`); }
{ const r = release({ foam: { h: 0 } }, 30); console.log(`  no head: 1/e after ${r.te} s, 1 % after ${r.t1} s`); }
{ const f = page({ foam: { h: 0.015 } }); console.log(`  the plant the controller is given at 125 mm (no foam: it is not linear): f ${(f.w[0] / 2 / Math.PI).toFixed(4)} Hz, zeta ${f.zeta[0].toFixed(5)}, beta ${f.beta[0].toFixed(4)}`); }

// ------------------------------------------------------------------ figure: frequency against fill
{
  const W = 720, H = 470, Lx = 64, Rx = 698, T1 = 18, B1 = 268, T2 = 316, B2 = 406, h0 = 30, h1 = 145;
  const X = (h) => Lx + (h - h0) / (h1 - h0) * (Rx - Lx);
  const Y1 = (f) => B1 - (f - 3.2) / (4.2 - 3.2) * (B1 - T1), Y2 = (s) => B2 - (s + 0.1) / (0.4 + 0.1) * (B2 - T2);
  let s = `<rect x="0" y="0" width="${W}" height="${H}" fill="#fff"/>`;
  for (let f = 3.2; f <= 4.2 + 1e-9; f += 0.1) s += `<line x1="${Lx}" x2="${Rx}" y1="${f1(Y1(f))}" y2="${f1(Y1(f))}" stroke="${GRID}"/><text class="tick" x="${Lx - 8}" y="${f1(Y1(f) + 4)}" text-anchor="end">${f.toFixed(1)}</text>`;
  for (let v = -0.1; v <= 0.4 + 1e-9; v += 0.1) s += `<line x1="${Lx}" x2="${Rx}" y1="${f1(Y2(v))}" y2="${f1(Y2(v))}" stroke="${GRID}"/><text class="tick" x="${Lx - 8}" y="${f1(Y2(v) + 4)}" text-anchor="end">${(+v.toFixed(1)).toString().replace('-', '−')}</text>`;
  s += `<line x1="${Lx}" x2="${Rx}" y1="${f1(Y2(0))}" y2="${f1(Y2(0))}" stroke="${MUTED}" stroke-dasharray="3 3"/>`;
  for (const [T, B] of [[T1, B1], [T2, B2]]) {
    s += `<line x1="${Lx}" x2="${Lx}" y1="${T}" y2="${B}" stroke="${MUTED}"/><line x1="${Lx}" x2="${Rx}" y1="${B}" y2="${B}" stroke="${MUTED}"/>`;
    for (let h = 30; h <= 145 + 1e-9; h += 10) s += `<line x1="${f1(X(h))}" x2="${f1(X(h))}" y1="${B}" y2="${B + 5}" stroke="${MUTED}"/>` + (`<text class="tick" x="${f1(X(h))}" y="${B + 19}" text-anchor="middle">${h}</text>`);
  }
  const pth = (xs, ys, Y) => xs.map((h, i) => `${i ? 'L' : 'M'}${f1(X(h))} ${f1(Y(ys[i]))}`).join(' ');
  s += `<path d="${pth(hs, fC, Y1)}" fill="none" stroke="${DARK}" stroke-width="1.6" stroke-dasharray="6 4"/>`;
  s += `<path d="${pth(hs, fT, Y1)}" fill="none" stroke="${WINE}" stroke-width="2.2"/>`;
  hs.forEach((h, i) => { s += `<circle cx="${f1(X(h))}" cy="${f1(Y1(fT[i]))}" r="2" fill="${WINE}"/>`; });
  const i125 = row(125);
  s += `<line x1="${f1(X(125))}" x2="${f1(X(125))}" y1="${T1}" y2="${B2}" stroke="${MUTED}" stroke-dasharray="2 3"/><text class="tick" x="${f1(X(125) + 4)}" y="${f1(Y1(fT[i125]) + 22)}">125 mm: ${fT[i125].toFixed(3)} Hz</text>`;
  s += `<circle cx="${f1(X(hs[imin]))}" cy="${f1(Y1(fT[imin]))}" r="4" fill="none" stroke="${WINE}" stroke-width="1.4"/><text class="tick" x="${f1(X(hs[imin]))}" y="${f1(Y1(fT[imin]) + 22)}" text-anchor="middle">lowest ${fT[imin].toFixed(3)} Hz at ${hs[imin]} mm</text>`;
  s += `<path d="${pth(hs, slope, Y2)}" fill="none" stroke="${INK}" stroke-width="1.8"/>`;
  s += `<text class="lbl" x="${Lx + 6}" y="${T1 + 13}">first sloshing frequency f₁₁ (Hz)</text>`;
  s += `<text class="lbl" x="${Rx - 6}" y="${T2 + 13}" text-anchor="end">slope of the wall at the surface, dR/dz</text>`;
  s += `<text class="lbl" x="${Rx}" y="${B2 + 36}" text-anchor="end">fill height h (mm)</text>`;
  s += `<line x1="${Lx}" x2="${Lx + 22}" y1="${H - 14}" y2="${H - 14}" stroke="${WINE}" stroke-width="2.2" stroke-linecap="round"/><text class="lbl" x="${Lx + 30}" y="${H - 10}">the tulip, finite elements</text>`;
  s += `<line x1="${Lx + 260}" x2="${Lx + 282}" y1="${H - 14}" y2="${H - 14}" stroke="${DARK}" stroke-width="1.6" stroke-dasharray="6 4"/><text class="lbl" x="${Lx + 290}" y="${H - 10}">straight glass of the same R(h) and depth, eq. (16)</text>`;
  const svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Two panels against the fill height from 30 to 145 mm. Top: the tulip's first sloshing frequency, about 4.0 Hz at 30 to 40 mm, falling to its lowest, ${fT[imin].toFixed(2)} Hz, at ${hs[imin]} mm, and rising to ${fT[fT.length - 1].toFixed(2)} Hz at 145 mm; a dashed line for a straight glass of the same surface radius lies above the tulip's up to about 127 mm and below it beyond. Bottom: the slope of the wall at the surface, up to +0.26 near 70 mm and negative above 116 mm.">\n${s}\n</svg>`;
  fs.writeFileSync(path.join(out, 'fig-d-freq.svg'), svg);
}
// ------------------------------------------------------------------ figure: damping against fill
{
  const W = 720, H = 360, Lx = 64, Rx = 698, T = 18, B = 290, h0 = 30, h1 = 145, zmax = 0.018;
  const X = (h) => Lx + (h - h0) / (h1 - h0) * (Rx - Lx), Y = (z) => B - z / zmax * (B - T);
  const zs = { wall: [], skin: [], bulk: [], sum: [] };
  L.forEach((l) => { const m1 = l.m1, w = 2 * Math.PI * m1.f[0], sq = 0.5 * Math.sqrt(NU / (2 * w)); const a = sq * m1.Lam[0], b = sq * m1.LamS[0], c2 = NU * m1.Bk[0] / w; zs.wall.push(a); zs.skin.push(b); zs.bulk.push(c2); zs.sum.push(a + b + c2); });
  let s = `<rect x="0" y="0" width="${W}" height="${H}" fill="#fff"/>`;
  for (let z = 0; z <= zmax + 1e-9; z += 0.002) s += `<line x1="${Lx}" x2="${Rx}" y1="${f1(Y(z))}" y2="${f1(Y(z))}" stroke="${GRID}"/><text class="tick" x="${Lx - 8}" y="${f1(Y(z) + 4)}" text-anchor="end">${z.toFixed(3)}</text>`;
  s += `<line x1="${Lx}" x2="${Lx}" y1="${T}" y2="${B}" stroke="${MUTED}"/><line x1="${Lx}" x2="${Rx}" y1="${B}" y2="${B}" stroke="${MUTED}"/>`;
  for (let h = 30; h <= 145 + 1e-9; h += 10) s += `<line x1="${f1(X(h))}" x2="${f1(X(h))}" y1="${B}" y2="${B + 5}" stroke="${MUTED}"/><text class="tick" x="${f1(X(h))}" y="${B + 19}" text-anchor="middle">${h}</text>`;
  const pth = (ys) => hs.map((h, i) => `${i ? 'L' : 'M'}${f1(X(h))} ${f1(Y(ys[i]))}`).join(' ');
  s += `<path d="${pth(zs.sum)}" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
  s += `<path d="${pth(zs.wall)}" fill="none" stroke="${WINE}" stroke-width="1.8"/>`;
  s += `<path d="${pth(zs.skin)}" fill="none" stroke="${DARK}" stroke-width="1.6" stroke-dasharray="6 4"/>`;
  s += `<path d="${pth(zs.bulk)}" fill="none" stroke="${MUTED}" stroke-width="1.6"/>`;
  const i = row(125);
  s += `<line x1="${f1(X(125))}" x2="${f1(X(125))}" y1="${T}" y2="${B}" stroke="${MUTED}" stroke-dasharray="2 3"/>`;
  s += `<text class="tick" x="${f1(X(125) - 4)}" y="${f1(Y(zs.sum[i]) - 8)}" text-anchor="end">sum ${zs.sum[i].toFixed(4)}</text>`;
  s += `<text class="lbl" x="${Lx + 6}" y="${T + 13}">damping ratio of the first swing, ζ (stout, ν = 2.05 mm²/s)</text>`;
  s += `<text class="lbl" x="${Rx}" y="${B + 36}" text-anchor="end">fill height h (mm)</text>`;
  const lg = [[WINE, '', 'wall layer'], [DARK, '6 4', 'surface skin'], [MUTED, '', 'bulk'], [INK, '', 'sum']];
  lg.forEach(([col, da, lab], k) => { const x = Lx + k * 150; s += `<line x1="${x}" x2="${x + 22}" y1="${H - 14}" y2="${H - 14}" stroke="${col}" stroke-width="2" ${da ? `stroke-dasharray="${da}"` : ''}/><text class="lbl" x="${x + 30}" y="${H - 10}">${lab}</text>`; });
  const svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="The damping ratio of the first sloshing mode against the fill height: the wall layer and the surface skin each give about 0.005, the bulk about 0.0004; their sum is ${zs.sum[i].toFixed(4)} at 125 mm and changes little with the fill.">\n${s}\n</svg>`;
  fs.writeFileSync(path.join(out, 'fig-d-damp.svg'), svg);
  console.log(`damping figure: sum ranges ${Math.min(...zs.sum).toFixed(4)}-${Math.max(...zs.sum).toFixed(4)}; wall ${Math.min(...zs.wall).toFixed(4)}-${Math.max(...zs.wall).toFixed(4)}; skin ${Math.min(...zs.skin).toFixed(4)}-${Math.max(...zs.skin).toFixed(4)}; bulk ${Math.min(...zs.bulk).toFixed(5)}-${Math.max(...zs.bulk).toFixed(5)}`);
}
// ------------------------------------------------------------------ figure: a free swing and the head
{
  const W = 720, H = 400, Lx = 64, Rx = 698, T = 18, B = 318, t0 = 0, t1 = 6, ymax = 7;
  const X = (t) => Lx + (t - t0) / (t1 - t0) * (Rx - Lx), Y = (y) => (T + B) / 2 - y / ymax * (B - T) / 2;
  let s = `<rect x="0" y="0" width="${W}" height="${H}" fill="#fff"/>`;
  for (let y = -5; y <= 5 + 1e-9; y += 2.5) s += `<line x1="${Lx}" x2="${Rx}" y1="${f1(Y(y))}" y2="${f1(Y(y))}" stroke="${GRID}"/><text class="tick" x="${Lx - 8}" y="${f1(Y(y) + 4)}" text-anchor="end">${(+y.toFixed(1)).toString().replace('-', '−')}</text>`;
  s += `<line x1="${Lx}" x2="${Lx}" y1="${T}" y2="${B}" stroke="${MUTED}"/><line x1="${Lx}" x2="${Rx}" y1="${B}" y2="${B}" stroke="${MUTED}"/>`;
  for (let t = 0; t <= t1 + 1e-9; t += 1) s += `<line x1="${f1(X(t))}" x2="${f1(X(t))}" y1="${B}" y2="${B + 5}" stroke="${MUTED}"/><text class="tick" x="${f1(X(t))}" y="${B + 19}" text-anchor="middle">${t}</text>`;
  const trace = (r, col, w, op) => { let d = ''; r.ys.forEach(([t, y], k) => { if (t <= t1 && k % 8 === 0) d += `${d ? 'L' : 'M'}${f1(X(t))} ${f1(Y(y * 1000))} `; }); return `<path d="${d}" fill="none" stroke="${col}" stroke-width="${w}" stroke-opacity="${op}" stroke-linejoin="round"/>`; };
  s += `<defs><clipPath id="cd"><rect x="${Lx}" y="${T}" width="${Rx - Lx}" height="${B - T}"/></clipPath></defs><g clip-path="url(#cd)">`;
  s += trace(runs.off, MUTED, 0.8, 0.45) + trace(runs[0], DARK, 1.3, 1) + trace(runs[5], '#b0707a', 1.5, 1) + trace(runs[15], WINE, 2, 1) + '</g>';
  for (const [hh, col] of [[5, '#b0707a'], [15, WINE]]) { const ts = runs[hh].tStar; if (ts < t1) s += `<line x1="${f1(X(ts))}" x2="${f1(X(ts))}" y1="${f1(Y(-5.6))}" y2="${f1(Y(-6.4))}" stroke="${col}" stroke-width="2"/><text class="tick" x="${f1(X(ts) + 4)}" y="${f1(Y(-6.4) + 2)}">t* ${ts.toFixed(2)} s</text>`; }
  s += `<text class="lbl" x="${Lx + 6}" y="${T + 13}">height of the stout at the front wall above rest (mm)</text>`;
  s += `<text class="lbl" x="${Rx}" y="${B + 36}" text-anchor="end">time after release t (s)</text>`;
  const lg = [[MUTED, 'friction off'], [DARK, 'no head'], ['#b0707a', 'head 5 mm'], [WINE, 'head 15 mm (the page)']];
  lg.forEach(([col, lab], k) => { const x = Lx + k * 150; s += `<line x1="${x}" x2="${x + 22}" y1="${H - 14}" y2="${H - 14}" stroke="${col}" stroke-width="2.2" stroke-linecap="round"/><text class="lbl" x="${x + 30}" y="${H - 10}">${lab}</text>`; });
  const svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="The stout's height at the front wall after release from 5 mm, over 6 s, in the page's model: with friction off the swing keeps its size; with no head it shrinks slowly; with a 5 mm head it stops after about ${runs[5].t1.toFixed(1)} s; with the page's 15 mm head after about ${runs[15].t1.toFixed(1)} s; the arrest times of Viola et al.'s formula are marked.">\n${s}\n</svg>`;
  fs.writeFileSync(path.join(out, 'fig-d-decay.svg'), svg);
}
console.log(`wrote fig-d-freq.svg, fig-d-damp.svg, fig-d-decay.svg into ${out}`);
