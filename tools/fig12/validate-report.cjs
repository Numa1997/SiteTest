// Stage E report: gathers tools/fig12/validate.cjs results (notes/fig12/runs/validate/*.json), writes notes/fig12/validation.md
// and notes/fig12/runs/validation-summary.json, and exits 1 if a stated tolerance is exceeded.
// Tolerances, set from the 3D solver's own uncertainty (reading noise about 1 mm on a lean of 4-30 mm; grid spread of the softening
// as large as its size; notes/fig12/runs/3d/), on two measures that a drifting phase does not spoil:
//   the swing's envelope (largest |lean| per 0.3 s window): median difference at most 30 %, worst case at most 80 %
//   the largest lean of the run: median |model/3D - 1| at most 25 %, worst at most 60 % (violent and spilling: at most 40 % and 70 %,
//   the five-mode theory's known shortfall on the tallest crests, notes/fig12/runs/spill-fit.json)
// The 3D solver's resolution (decided with the site's owner on 11 November 2026, after the first run failed in three regimes, nearly all
// on small swings): only what the 3D solver resolves is judged: envelope windows where its swing exceeds FLOOR_WIN = 3 mm, and the largest
// lean of cases where its largest lean exceeds FLOOR_CASE = 5 mm. At rest its lean reading has 1 mm of noise in 0.29 mm steps, and on the
// sloped wall it under-responds to small swings (a 1.0 mm swing where 6.3 mm was expected: notes/fig12/runs/3d/backbone-tilt-75-*).
// What is excluded is counted and reported.
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '../../notes/fig12/runs/validate'), all = [];
for (const f of fs.readdirSync(dir).filter((f) => f.endsWith('.json'))) all.push(...JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')));
const FLOOR_WIN = 3, FLOOR_CASE = 5;
// the envelope from the stored series: largest |lean| per 0.3 s window (60 samples of 5 ms), windows where the 3D's exceeds FLOOR_WIN
function envErr(r) {
  const a = r.series.lean_3d, b = r.series.lean_model, n = Math.min(a.length, b.length); let d = 0, s = 0, used = 0, all = 0;
  for (let k = 0; k + 60 <= n; k += 60) { let ma = 0, mb = 0; for (let j = k; j < k + 60; j++) { ma = Math.max(ma, Math.abs(a[j])); mb = Math.max(mb, Math.abs(b[j])); } all++; if (ma <= FLOOR_WIN) continue; used++; d += (mb - ma) ** 2; s += ma * ma; }
  return used ? { e: Math.sqrt(d / s), used, all } : null;
}
const tol = { env: [0.30, 0.80], peak: { default: [0.25, 0.60], violent: [0.40, 0.70], spilling: [0.40, 0.70] } };
const med = (a) => { const s = [...a].sort((x, y) => x - y); return s.length ? (s.length % 2 ? s[s.length >> 1] : 0.5 * (s[s.length / 2 - 1] + s[s.length / 2])) : NaN; };
const pc = (x) => (100 * x).toFixed(0) + ' %';
let fail = [], md = ['# Fig. 12 validation: the page\'s model against the full 3D solver', '',
  'Written by `tools/fig12/validate-report.cjs` from `notes/fig12/runs/validate/` (runs of `tools/fig12/validate.cjs` on GitHub\'s runners,',
  '`.github/workflows/fig12-validate.yml`). Each case is a random road of its regime, 3 s, the cart from 0.5 m at 0.8-1.2 m/s. The 3D solver',
  '(half glass, 3 mm grid) against the page\'s model run as the 3D solver\'s twin (its frequencies times 0.958, the grid\'s; friction off,',
  'the grid\'s damping 0.002): this tests the model\'s form; its physical frequencies and friction are tested elsewhere.', '',
  'In plain words, per regime: how far the size of the swing over time (its envelope) differs, how far the largest lean differs, how far',
  'the cart\'s speed differs, and the spilled stout.', ''];
const regimes = [...new Set(all.map((r) => r.regime))];
const summary = {};
for (const g of regimes) {
  const R0 = all.filter((r) => r.regime === g), R = R0.filter((r) => r.lean_3d > FLOOR_CASE), Rs = R0.filter((r) => r.lean_3d <= FLOOR_CASE);
  R.forEach((r) => { const q = envErr(r); r.e_env_floor = q ? q.e : null; r.win_used = q ? q.used : 0; });
  const RE = R.filter((r) => r.e_env_floor != null), env = RE.map((r) => r.e_env_floor), pk = R.map((r) => Math.abs(r.peak_ratio - 1)), dv = R0.map((r) => r.dv_rms_mm_s);
  if (!R.length) { md.push(`## ${g} (${R0.length} roads)`, '', `- Every road's swing stays under ${FLOOR_CASE} mm in the 3D solver: nothing it can resolve to judge.`, ''); continue; }
  const worstEnv = RE.reduce((a, r) => (r.e_env_floor > a.e_env_floor ? r : a)), worstPk = R.reduce((a, r) => (Math.abs(r.peak_ratio - 1) > Math.abs(a.peak_ratio - 1) ? r : a));
  const smallNote = Rs.length ? `${Rs.length} of ${R0.length} roads keep the 3D swing under ${FLOOR_CASE} mm and are not judged; on them the largest leans are ${med(Rs.map((r) => r.lean_3d)).toFixed(1)} mm (3D) and ${med(Rs.map((r) => r.lean_model)).toFixed(1)} mm (model) typically.` : 'Every road is judged.';
  const pt = tol.peak[g] || tol.peak.default, low = R.filter((r) => r.peak_ratio < 1).length;
  const sp3 = R0.reduce((a, r) => a + r.spill_3d, 0), spm = R0.reduce((a, r) => a + r.spill_model, 0);
  summary[g] = { cases: R0.length, judged: R.length, env_median: med(env), env_worst: worstEnv.e_env_floor, peak_median: med(pk), peak_worst: Math.abs(worstPk.peak_ratio - 1), model_lower: low, dv_median_mm_s: med(dv), spill_3d_g: sp3, spill_model_g: spm };
  md.push(`## ${g} (${R0.length} roads)`, '', `- ${smallNote}`,
    `- The swing's size over time differs by ${pc(med(env))} typically and by ${pc(worstEnv.e_env_floor)} at worst (road ${worstEnv.seed}), over the windows where the 3D swing exceeds ${FLOOR_WIN} mm. Tolerance: ${pc(tol.env[0])} typical, ${pc(tol.env[1])} worst.`,
    `- The largest lean differs by ${pc(med(pk))} typically and by ${pc(Math.abs(worstPk.peak_ratio - 1))} at worst (road ${worstPk.seed}: 3D ${worstPk.lean_3d} mm, model ${worstPk.lean_model} mm); the model's is the lower in ${low} of ${R.length}. Tolerance: ${pc(pt[0])} typical, ${pc(pt[1])} worst.`,
    `- The cart's speed differs by ${med(dv).toFixed(2)} mm/s rms typically: the stout's push on the cart is the same in both.`,
    `- Spilled: ${sp3.toFixed(0)} g in the 3D runs, ${spm.toFixed(0)} g in the model's, over all ${R0.length} roads (reported, not judged: see below).`, '');
  if (med(env) > tol.env[0]) fail.push(`${g}: envelope median ${pc(med(env))}`);
  if (worstEnv.e_env_floor > tol.env[1]) fail.push(`${g}: envelope worst ${pc(worstEnv.e_env_floor)}`);
  if (med(pk) > pt[0]) fail.push(`${g}: peak median ${pc(med(pk))}`);
  if (Math.abs(worstPk.peak_ratio - 1) > pt[1]) fail.push(`${g}: peak worst ${pc(Math.abs(worstPk.peak_ratio - 1))}`);
}
md.push('## Spilled stout', '', 'The pour is reported, not judged. On single hard pushes, where the 3 and 4 mm grids agree within 5 %, the model spills 5-23 % less than the 3D solver (tools/fig12/spill-fit.cjs). On roads that only just lift the crest over the rim the model pours more than the 3D solver, up to about twice at 125 mm fill: an overflow thinner than one cell (3-4 mm) can hardly leave the 3D grid, so which is nearer a real glass there is not settled by these runs.', '',
  '## History', '', 'The first runs used the 4 mm grid. It fails the exact steady tilt (a held push tilts the surface into the plane 2 R(h) a/g in any glass) by up to 46 % on the flared wall, the 3 mm grid by 5-6 % at 75-125 mm and 13-23 % at 140 mm (tools/fig12/tilt-exact.cjs); since then the reference is the 3 mm grid.', '', 'First run (workflow run 43052998146, 11 November 2026, 4 mm grid), every case judged: FAILED in fills (envelope median 33 %, worst 212 %; largest lean worst 137 %, a 4.3 mm swing), gentle (envelope median 51 %, worst 81 %) and vertical (envelope worst 130 %, largest lean worst 66 %). The resolution floor above was then added, with the site owner\u2019s agreement.', '',
  fail.length ? '**Result: FAILED** — ' + fail.join('; ') : '**Result: every regime within its stated tolerance.**', '');
fs.writeFileSync(path.join(__dirname, '../../notes/fig12/validation.md'), md.join('\n'));
fs.writeFileSync(path.join(__dirname, '../../notes/fig12/runs/validation-summary.json'), JSON.stringify({ tol, summary, fail }, null, 1));
console.log(md.join('\n'));
process.exit(fail.length ? 1 : 0);
