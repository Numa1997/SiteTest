// How well does the 3D solver hold a steady tilt? A push a held constant tilts the surface into the plane eta = h - (a/g) x in any
// glass (exact, linear theory), so the lean at the wall is 2 R(h) a/g. node tools/fig12/tilt-exact.cjs
// Reads the tilt-release runs (notes/fig12/runs/3d/backbone-tilt-*.json: a ramped up to A over 0.6 s, held to 1.0 s) and compares the
// mean lean over 0.65-1.0 s with 2 R(h) A/g. The ramp leaves a residual swing of a few per cent about the tilt.
const fs = require('fs'), path = require('path'), dir = path.join(__dirname, '../../notes/fig12/runs/3d');
const G = (() => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts/guinness-glass.js'), 'utf8'))(m); return m.exports; })();
const Rz = (z) => { const f = z / G.dz, i = Math.floor(f); return G.R[i] + (f - i) * (G.R[i + 1] - G.R[i]); };
for (const h of [75, 100, 125, 140]) for (const g of ['4mm', '3mm']) {
  const out = [];
  for (const A of [2.5, 5]) {
    const f = path.join(dir, `backbone-tilt-${h}-${A}-${g}.json`); if (!fs.existsSync(f)) continue;
    const s = JSON.parse(fs.readFileSync(f, 'utf8')).series.filter((r) => r[0] > 0.65 && r[0] <= 1.0), m = s.reduce((a, r) => a + r[1], 0) / s.length, ex = -2 * Rz(h / 1000) * A / 9.81 * 1000;
    out.push(`A ${A}: ${m.toFixed(1)} vs exact ${ex.toFixed(1)} mm (${((m / ex - 1) * 100).toFixed(0)} %)`);
  }
  console.log(`${h} mm, ${g}: ${out.join(';  ')}`);
}
