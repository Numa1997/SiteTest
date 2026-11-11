// Stage E report: gathers tools/fig12/validate.cjs results (notes/fig12/runs/validate/*.json), writes notes/fig12/validation.md
// and notes/fig12/runs/validation-summary.json, and exits 1 if a stated tolerance is exceeded.
// Tolerances, set from the 3D solver's own uncertainty (reading noise about 1 mm on a lean of 4-30 mm; grid spread of the softening
// as large as its size; notes/fig12/runs/3d/), on two measures that a drifting phase does not spoil:
//   the swing's envelope (largest |lean| per 0.3 s window): median difference at most 30 %, worst case at most 80 %
//   the largest lean of the run: median |model/3D - 1| at most 25 %, worst at most 60 % (violent and spilling: at most 40 % and 70 %,
//   the five-mode theory's known shortfall on the tallest crests, notes/fig12/runs/spill-fit.json)
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '../../notes/fig12/runs/validate'), all = [];
for (const f of fs.readdirSync(dir).filter((f) => f.endsWith('.json'))) all.push(...JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')));
const tol = { env: [0.30, 0.80], peak: { default: [0.25, 0.60], violent: [0.40, 0.70], spilling: [0.40, 0.70] } };
const med = (a) => { const s = [...a].sort((x, y) => x - y); return s.length ? (s.length % 2 ? s[s.length >> 1] : 0.5 * (s[s.length / 2 - 1] + s[s.length / 2])) : NaN; };
const pc = (x) => (100 * x).toFixed(0) + ' %';
let fail = [], md = ['# Fig. 12 validation: the page\'s model against the full 3D solver', '',
  'Written by `tools/fig12/validate-report.cjs` from `notes/fig12/runs/validate/` (runs of `tools/fig12/validate.cjs` on GitHub\'s runners,',
  '`.github/workflows/fig12-validate.yml`). Each case is a random road of its regime, 3 s, the cart from 0.5 m at 0.8-1.2 m/s. The 3D solver',
  '(half glass, 4 mm grid) against the page\'s model run as the 3D solver\'s twin (its frequencies times 0.943, the grid\'s; friction off,',
  'the grid\'s damping 0.004): this tests the model\'s form; its physical frequencies and friction are tested elsewhere.', '',
  'In plain words, per regime: how far the size of the swing over time (its envelope) differs, how far the largest lean differs, how far',
  'the cart\'s speed differs, and the spilled stout.', ''];
const regimes = [...new Set(all.map((r) => r.regime))];
const summary = {};
for (const g of regimes) {
  const R = all.filter((r) => r.regime === g), env = R.map((r) => r.e_env), pk = R.map((r) => Math.abs(r.peak_ratio - 1)), dv = R.map((r) => r.dv_rms_mm_s);
  const worstEnv = R.reduce((a, r) => (r.e_env > a.e_env ? r : a)), worstPk = R.reduce((a, r) => (Math.abs(r.peak_ratio - 1) > Math.abs(a.peak_ratio - 1) ? r : a));
  const pt = tol.peak[g] || tol.peak.default, low = R.filter((r) => r.peak_ratio < 1).length;
  const sp3 = R.reduce((a, r) => a + r.spill_3d, 0), spm = R.reduce((a, r) => a + r.spill_model, 0);
  summary[g] = { cases: R.length, env_median: med(env), env_worst: worstEnv.e_env, peak_median: med(pk), peak_worst: Math.abs(worstPk.peak_ratio - 1), model_lower: low, dv_median_mm_s: med(dv), spill_3d_g: sp3, spill_model_g: spm };
  md.push(`## ${g} (${R.length} roads)`, '',
    `- The swing's size over time differs by ${pc(med(env))} typically and by ${pc(worstEnv.e_env)} at worst (road ${worstEnv.seed}). Tolerance: ${pc(tol.env[0])} typical, ${pc(tol.env[1])} worst.`,
    `- The largest lean differs by ${pc(med(pk))} typically and by ${pc(Math.abs(worstPk.peak_ratio - 1))} at worst (road ${worstPk.seed}: 3D ${worstPk.lean_3d} mm, model ${worstPk.lean_model} mm); the model's is the lower in ${low} of ${R.length}. Tolerance: ${pc(pt[0])} typical, ${pc(pt[1])} worst.`,
    `- The cart's speed differs by ${med(dv).toFixed(2)} mm/s rms typically: the stout's push on the cart is the same in both.`,
    `- Spilled: ${sp3.toFixed(0)} g in the 3D runs, ${spm.toFixed(0)} g in the model's, over all ${R.length} roads.`, '');
  if (med(env) > tol.env[0]) fail.push(`${g}: envelope median ${pc(med(env))}`);
  if (worstEnv.e_env > tol.env[1]) fail.push(`${g}: envelope worst ${pc(worstEnv.e_env)}`);
  if (med(pk) > pt[0]) fail.push(`${g}: peak median ${pc(med(pk))}`);
  if (Math.abs(worstPk.peak_ratio - 1) > pt[1]) fail.push(`${g}: peak worst ${pc(Math.abs(worstPk.peak_ratio - 1))}`);
}
md.push(fail.length ? '**Result: FAILED** — ' + fail.join('; ') : '**Result: every regime within its stated tolerance.**', '');
fs.writeFileSync(path.join(__dirname, '../../notes/fig12/validation.md'), md.join('\n'));
fs.writeFileSync(path.join(__dirname, '../../notes/fig12/runs/validation-summary.json'), JSON.stringify({ tol, summary, fail }, null, 1));
console.log(md.join('\n'));
process.exit(fail.length ? 1 : 0);
