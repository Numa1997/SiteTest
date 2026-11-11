// The page's pour model against the 3D solver's spill runs (notes/fig12/runs/3d/spill-*.json, from .github/workflows/fig12-3d.yml):
// the same push a_x = A sin(pi t/Tp), t < Tp, at the same fill, friction off (the 3D solver has almost none over 1.5 s).
// node tools/fig12/spill-fit.cjs [Cd]      prints, per case, the spilled grams and the largest lean of both, and the totals
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { TulipNM } = load('stout-modal.js'), G = load('guinness-glass.js');
const rd = (f) => JSON.parse(fs.readFileSync(path.join(__dirname, '../../public/data/fig12', f), 'utf8'));
const data = rd('modes.json'), nmData = rd('nm.json'), dir = path.join(__dirname, '../../notes/fig12/runs/3d');
const Cd = process.argv[2] != null ? +process.argv[2] : undefined, cap = process.env.CAP ? +process.env.CAP : null;   // default: the engine's own (C_d 1.0, cap 2.0)
const files = fs.readdirSync(dir).filter((f) => /^spill-.*\.json$/.test(f)).sort();
const out = [];
for (const f of files) {
  const d = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
  const m = new TulipNM(Object.assign({ data, nmData, profile: G, h0: d.h0, nModes: 3, friction: false }, Cd != null ? { Cd } : {}));
  if (cap != null) m.capFactor = cap;
  const dt = 0.001; let lean = 0;
  for (let k = 0; k * dt < d.T - 1e-9; k++) { const t = k * dt; m.step(dt, t < d.Tp ? d.A * Math.sin(Math.PI * (t + 0.5 * dt) / d.Tp) : 0, 0); lean = Math.max(lean, Math.abs(m.wallAt(0) - m.wallAt(Math.PI))); }
  const g3 = d.rows[d.rows.length - 1][3], l3 = Math.max(...d.rows.map((r) => Math.abs(r[1]))), gm = m.spillV * m.rho * 1000;
  out.push({ f, h: d.h0 * 1000, A: d.A, dx: d.dx * 1000, g3, gm, l3, lm: lean * 1000, breaks: m.breaks });
}
for (const o of out) console.log(`${o.h} mm A ${String(o.A).padStart(2)} dx ${o.dx}: spilled 3D ${o.g3.toFixed(1).padStart(6)} g, model ${o.gm.toFixed(1).padStart(6)} g; largest lean 3D ${o.l3.toFixed(1)} mm, model ${o.lm.toFixed(1)} mm${o.breaks ? ' (capped ' + o.breaks + ' substeps)' : ''}`);
for (const dx of [4, 3]) { const s = out.filter((o) => o.dx === dx); console.log(`dx ${dx} mm totals: 3D ${s.reduce((a, o) => a + o.g3, 0).toFixed(0)} g, model ${s.reduce((a, o) => a + o.gm, 0).toFixed(0)} g`); }
if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify({ Cd: out.length ? undefined : null, engineDefaults: true, out }, null, 1));
