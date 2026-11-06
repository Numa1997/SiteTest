// The inline SVG figures of the Fig. 12 lecture note, in the house chart style (white plate, Plex Mono ticks, Latin Modern
// symbols): node tools/fig12/figures.cjs  ->  notes/fig12/fig-glass.svg, notes/fig12/fig-bump.svg
// fig-glass: the glass's inner radius R(z) from scripts/guinness-glass.js, both halves, with the fill height and the rim.
// fig-bump:  the glass's horizontal acceleration and the stout's front − back lean over a 10 mm bump, open loop against speed
//            control, from the series that tools/fig12/study.cjs writes (SERIES=…json); run those first:
//   SERIES=notes/fig12/runs/series_10_off_0_0.004.json   node tools/fig12/study.cjs 10 off 0 0.004
//   SERIES=notes/fig12/runs/series_10_speed_0_0.004.json node tools/fig12/study.cjs 10 speed 0 0.004
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../..');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(root, 'public/scripts', f), 'utf8'))(m); return m.exports; };
const G = load('guinness-glass.js');
const f1 = (v) => v.toFixed(1);
const INK = '#1c1518', MUTED = '#8b8079', GRID = '#eee6d9', WINE = '#7a1f2b', DARK = '#4a413d';

// ---------------------------------------------------------------- the glass
{
  const W = 720, H = 380, s = 2000;                 // px per metre: 160 mm -> 320 px
  const cx = 250, z0 = 340;                         // axis and the cavity floor on the plate
  const X = (r) => cx + r * s, Z = (z) => z0 - z * s;
  const P = G.R, dz = G.dz, n = P.length, zr = (n - 1) * dz, h0 = 0.125;
  const Rz = (z) => { const f = z / dz, i = Math.min(n - 2, Math.floor(f)); return P[i] + (f - i) * (P[i + 1] - P[i]); };
  let right = '', left = '', fill = '';
  for (let i = 0; i < n; i++) { const z = i * dz; right += `${i ? 'L' : 'M'}${f1(X(P[i]))} ${f1(Z(z))} `; left += `${i ? 'L' : 'M'}${f1(X(-P[i]))} ${f1(Z(z))} `; }
  fill = `M${f1(X(-P[0]))} ${f1(Z(0))} `;
  for (let i = 0; i * dz <= h0 + 1e-9; i++) fill += `L${f1(X(-P[i]))} ${f1(Z(i * dz))} `;
  for (let i = Math.round(h0 / dz); i >= 0; i--) fill += `L${f1(X(P[i]))} ${f1(Z(i * dz))} `;
  fill += 'Z';
  const Rh = Rz(h0), Rmax = Math.max(...P), zmax = P.indexOf(Rmax) * dz;
  const tick = (z, lab) => `<line x1="${f1(X(-0.052))}" x2="${f1(X(-0.048))}" y1="${f1(Z(z))}" y2="${f1(Z(z))}" stroke="${MUTED}"/><text class="tick" x="${f1(X(-0.054))}" y="${f1(Z(z) + 4)}" text-anchor="end">${lab}</text>`;
  let ticks = ''; for (let z = 0; z <= 0.15 + 1e-9; z += 0.025) ticks += tick(z, (z * 1000).toFixed(0));
  const svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Section of the Guinness tulip glass used by the page: the inner radius R(z) on both sides of the axis, from the floor of the cavity to the rim at 147.5 mm; the stout filled to 125 mm; the widest point 39.3 mm at 113 mm; the coordinates x along the road and z up.">
<rect x="0" y="0" width="${W}" height="${H}" fill="#fff"/>
<line x1="${f1(X(-0.05))}" x2="${f1(X(-0.05))}" y1="${f1(Z(0))}" y2="${f1(Z(0.15))}" stroke="${MUTED}"/>
${ticks}
<text class="tick" x="${f1(X(-0.05))}" y="${f1(Z(0.155) - 4)}" text-anchor="middle">z (mm)</text>
<path d="${fill}" fill="#3e1712" fill-opacity="0.85"/>
<path d="${right}" fill="none" stroke="${INK}" stroke-width="2"/>
<path d="${left}" fill="none" stroke="${INK}" stroke-width="2"/>
<line x1="${f1(X(-P[0]))}" x2="${f1(X(P[0]))}" y1="${f1(Z(0))}" y2="${f1(Z(0))}" stroke="${INK}" stroke-width="2"/>
<line x1="${cx}" x2="${cx}" y1="${f1(Z(0) + 8)}" y2="${f1(Z(zr) - 14)}" stroke="${MUTED}" stroke-dasharray="4 4"/>
<line x1="${f1(X(-Rh) - 6)}" x2="${f1(X(Rh) + 70)}" y1="${f1(Z(h0))}" y2="${f1(Z(h0))}" stroke="${WINE}" stroke-width="1.4" stroke-dasharray="5 3"/>
<text class="tick" x="${f1(X(Rh) + 74)}" y="${f1(Z(h0) + 4)}">fill h = 125 mm, R(h) = ${(Rh * 1000).toFixed(1)} mm</text>
<line x1="${f1(X(P[n - 1]))}" x2="${f1(X(P[n - 1]) + 70)}" y1="${f1(Z(zr))}" y2="${f1(Z(zr))}" stroke="${MUTED}" stroke-width="1"/>
<text class="tick" x="${f1(X(P[n - 1]) + 74)}" y="${f1(Z(zr) + 4)}">rim z = ${(zr * 1000).toFixed(1)} mm, R = ${(P[n - 1] * 1000).toFixed(1)} mm</text>
<line x1="${f1(X(Rmax))}" x2="${f1(X(Rmax) + 70)}" y1="${f1(Z(zmax))}" y2="${f1(Z(zmax))}" stroke="${MUTED}" stroke-width="1"/>
<text class="tick" x="${f1(X(Rmax) + 74)}" y="${f1(Z(zmax) + 4)}">widest R = ${(Rmax * 1000).toFixed(1)} mm at z = ${(zmax * 1000).toFixed(0)} mm</text>
<line x1="${f1(X(P[40]))}" x2="${f1(X(P[40]) + 70)}" y1="${f1(Z(40 * dz))}" y2="${f1(Z(40 * dz))}" stroke="${MUTED}" stroke-width="1"/>
<text class="tick" x="${f1(X(P[40]) + 74)}" y="${f1(Z(40 * dz) + 4)}">R = ${(P[40] * 1000).toFixed(1)} mm at z = 20 mm</text>
<line x1="${cx}" x2="${f1(X(0.032))}" y1="${f1(Z(0.06))}" y2="${f1(Z(0.06))}" stroke="#f5f1ea" stroke-width="1.2"/>
<path d="M${f1(X(0.032) - 7)} ${f1(Z(0.06) - 4)} L${f1(X(0.032))} ${f1(Z(0.06))} L${f1(X(0.032) - 7)} ${f1(Z(0.06) + 4)}" fill="none" stroke="#f5f1ea" stroke-width="1.2"/>
<text class="m" x="${f1(X(0.012))}" y="${f1(Z(0.06) - 8)}" fill="#f5f1ea" style="fill:#f5f1ea">R(z)</text>
<line x1="70" x2="130" y1="350" y2="350" stroke="${MUTED}" stroke-width="1.4"/><path d="M126 346 L134 350 L126 354 Z" fill="${MUTED}"/>
<line x1="70" x2="70" y1="350" y2="290" stroke="${MUTED}" stroke-width="1.4"/><path d="M66 294 L70 286 L74 294 Z" fill="${MUTED}"/>
<text class="m" x="138" y="356">x</text><text class="m" x="64" y="280">z</text>
<text class="tick" x="80" y="372">x along the road, travel →</text>
</svg>`;
  fs.writeFileSync(path.join(root, 'notes/fig12/fig-glass.svg'), svg);
}

// ---------------------------------------------------------------- the bump
{
  const rd = (n) => JSON.parse(fs.readFileSync(path.join(root, 'notes/fig12/runs', n), 'utf8')).rows;
  const off = rd('series_10_off_0_0.004.json'), on = rd('series_10_speed_0_0.004.json');
  const W = 720, H = 470, L = 64, R = 698, T1 = 18, B1 = 188, T2 = 236, B2 = 406, t0 = 0, t1 = 2.3;
  const X = (t) => L + (t - t0) / (t1 - t0) * (R - L);
  const panel = (T, B, lo, hi, step, col, lab, unit) => {
    const Y = (v) => B - (v - lo) / (hi - lo) * (B - T);
    let g = '';
    for (let v = lo; v <= hi + 1e-9; v += step) g += `<line x1="${L}" x2="${R}" y1="${f1(Y(v))}" y2="${f1(Y(v))}" stroke="${GRID}"/><text class="tick" x="${L - 8}" y="${f1(Y(v) + 4)}" text-anchor="end">${+v.toFixed(2)}</text>`;
    g += `<line x1="${L}" x2="${L}" y1="${T}" y2="${B}" stroke="${MUTED}"/><line x1="${L}" x2="${R}" y1="${B}" y2="${B}" stroke="${MUTED}"/>`;
    for (let t = 0; t <= t1 + 1e-9; t += 0.5) g += `<line x1="${f1(X(t))}" x2="${f1(X(t))}" y1="${B}" y2="${B + 5}" stroke="${MUTED}"/><text class="tick" x="${f1(X(t))}" y="${B + 19}" text-anchor="middle">${t.toFixed(1)}</text>`;
    g += `<text class="lbl" x="${L + 6}" y="${T + 13}">${lab} (${unit})</text>`;
    const line = (rows, c, w) => { let d = ''; rows.forEach((r, i) => { d += `${i ? 'L' : 'M'}${f1(X(r[0]))} ${f1(Y(r[col]))} `; }); return `<path d="${d}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linejoin="round"/>`; };
    const id = 'c' + T;
    return g + `<defs><clipPath id="${id}"><rect x="${L}" y="${T}" width="${R - L}" height="${B - T}"/></clipPath></defs><g clip-path="url(#${id})">` + line(off, DARK, 1.6) + line(on, WINE, 2.0) + '</g>';
  };
  // the time the wheel is on the bump: the axle path rises above its level between these times (open loop; speed control is within 0.01 s)
  const svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Two panels against time over 2.3 s. Top: the glass's horizontal acceleration, a single sine-like cycle of about plus and minus 1.2 m/s² in open loop as the wheel crosses the bump between 0.375 and 0.625 s, and a smaller cycle of about 0.5 m/s² with speed control. Bottom: the stout's lean, front minus back wall: in open loop it swings up to 25 mm and keeps swinging at about 3.2 Hz; with speed control it stays within about 4 mm.">
<rect x="0" y="0" width="${W}" height="${H}" fill="#fff"/>
<rect x="${f1(X(0.375))}" y="${T1}" width="${f1(X(0.625) - X(0.375))}" height="${B1 - T1}" fill="#f5f1ea"/>
<rect x="${f1(X(0.375))}" y="${T2}" width="${f1(X(0.625) - X(0.375))}" height="${B2 - T2}" fill="#f5f1ea"/>
${panel(T1, B1, -1.5, 1.5, 0.5, 1, 'glass acceleration along the road, a_gx', 'm/s²')}
${panel(T2, B2, -30, 30, 10, 3, 'lean of the stout, front − back wall, Δη', 'mm')}
<text class="lbl" x="${R}" y="${B2 + 36}" text-anchor="end">time t (s)</text>
<line x1="${L}" x2="${L + 22}" y1="${H - 14}" y2="${H - 14}" stroke="${DARK}" stroke-width="2.2" stroke-linecap="round"/><text class="lbl" x="${L + 30}" y="${H - 10}">open loop (fixed motor current)</text>
<line x1="${L + 300}" x2="${L + 322}" y1="${H - 14}" y2="${H - 14}" stroke="${WINE}" stroke-width="2.2" stroke-linecap="round"/><text class="lbl" x="${L + 330}" y="${H - 10}">PI speed control</text>
</svg>`;
  fs.writeFileSync(path.join(root, 'notes/fig12/fig-bump.svg'), svg);
}
console.log('wrote notes/fig12/fig-glass.svg, notes/fig12/fig-bump.svg');
