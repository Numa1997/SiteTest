#!/usr/bin/env node
// Validation of the physics block of rotor_sim.html against the Python engine of the derivations.
//  1. Sol's 18 mountings, single and double, at Sol's brake constants (data/L1_mountings.json, from engine.py): the mean power
//     must agree within 0.1 %; prints every pair and the largest relative difference; exit 1 if any differs by more.
//  2. If notes/rotor-pendula/derive/L4_check_2000.json exists: the geared generator at its settings (ratio, efficiency, c_e),
//     with the smoothing band of that check (1e-3 of the swing it found, at least 0.01 rad); prints the differences in the load
//     power and in the power the rotor pays. Informative only (no pass/fail).
// Usage: node tools/check_sim.js [--no-geared]
const fs = require('fs');
const path = require('path');
const { loadPhysics } = require('./physics_block');
const { simulate, DEFAULTS } = loadPhysics();

const ROOT = path.join(__dirname, '..');
const L1 = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'L1_mountings.json'), 'utf8'));
const LIMIT = 1e-3;
let worst = 0, worstAt = '';
const pct = x => (x * 100).toExponential(2) + ' %';
console.log(`Ideal brake: ${DEFAULTS.steps} steps per turn, ${DEFAULTS.settle} turns to settle, ${DEFAULTS.measure} to measure, from rest.`);
console.log('rpm  pivot  pendulum   c (N m s)    page (mW)    engine.py (mW)   rel. diff');
const t0 = Date.now();
for (const r of L1) {
  for (const pend of ['single', 'double']) {
    const c = r['c_' + pend], ref = r['P_' + pend];
    const out = simulate({ rpm: r.rpm, frac: r.pct / 100, pend, c });
    const rel = Math.abs(out.P_mean / ref - 1);
    if (rel > worst) { worst = rel; worstAt = `${r.rpm} rpm ${r.pct} % ${pend}`; }
    console.log(`${String(r.rpm).padStart(3)}  ${String(r.pct).padStart(3)} %  ${pend.padEnd(8)} ${c.toFixed(6).padStart(10)}  ${(out.P_mean * 1e3).toFixed(6).padStart(11)}  ${(ref * 1e3).toFixed(6).padStart(14)}   ${pct(rel)}`);
  }
}
console.log(`Largest relative difference: ${pct(worst)} (${worstAt}); limit ${pct(LIMIT)}. ${((Date.now() - t0) / 1000).toFixed(1)} s for 36 runs.`);
const pass = worst <= LIMIT;
console.log(pass ? 'PASS' : 'FAIL');
const SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
const sci = (x, d = 1) => { const [m, e] = x.toExponential(d).split('e'); return `${m}·10${String(+e).split('').map(c => SUP[c]).join('')}`; };


let wl = null, wp = null;
const L4 = path.join(ROOT, '..', '..', 'notes', 'rotor-pendula', 'derive', 'L4_check_2000.json');
if (!process.argv.includes('--no-geared') && fs.existsSync(L4)) {
  const rows = JSON.parse(fs.readFileSync(L4, 'utf8'));
  if (!rows.length || rows[0].c_e == null || rows[0].P_load == null) {
    console.log(`\n${path.relative(process.cwd(), L4)} has no c_e / P_load fields (an older version); geared comparison skipped.`);
  } else {
    console.log(`\nGeared generator against L4_check_2000.json (Python, 2000 steps per turn, 100 + 20 turns), page at ${DEFAULTS.stepsGeared} steps per turn, ${DEFAULTS.settleGeared} + ${DEFAULTS.measureGeared} turns:`);
    console.log('rpm  pivot   N   R_L (ohm)   load page / L4 (mW)        diff     paid page / L4 (mW)       diff    swing page / L4');
    wl = 0; wp = 0;
    for (const r of rows) {
      const bandScale = r.Theta != null ? Math.max(r.Theta, 1e-2) : null;
      const out = simulate({ rpm: r.rpm, frac: r.frac, pend: 'single', gen: 'geared', N: r.N, ce: r.c_e, bandScale });
      const dl = out.P_load / r.P_load - 1, dp = out.P_paid / r.P_paid - 1;
      wl = Math.max(wl, Math.abs(dl)); wp = Math.max(wp, Math.abs(dp));
      console.log(`${String(r.rpm).padStart(3)}  ${String(Math.round(r.frac * 100)).padStart(3)} %  ${String(r.N).padStart(3)}  ${(r.R_load != null ? r.R_load : out.model.RL).toFixed(3).padStart(9)}  ` +
        `${(out.P_load * 1e3).toFixed(4).padStart(9)} / ${(r.P_load * 1e3).toFixed(4).padStart(9)}  ${(dl * 100).toFixed(3).padStart(8)} %  ` +
        `${(out.P_paid * 1e3).toFixed(4).padStart(9)} / ${(r.P_paid * 1e3).toFixed(4).padStart(9)}  ${(dp * 100).toFixed(3).padStart(8)} %  ` +
        `${out.thetaAbsMax.toFixed(4)} / ${r.Theta != null ? r.Theta.toFixed(4) : '–'}`);
    }
    console.log(`Largest relative difference: load ${pct(wl)}, paid ${pct(wp)}.`);
  }
}
// the result, for the page's physics section (tools/build_sim.py reads it)
const summary = { chk_worst: sci(worst), chk_at: worstAt, chk_steps: String(DEFAULTS.steps), chk_settle: String(DEFAULTS.settle),
  chk_measure: String(DEFAULTS.measure), chk_runs: String(2 * L1.length), chk_geared_steps: String(DEFAULTS.stepsGeared),
  chk_geared_sentence: wl == null ? '.'
    : `. For the geared generator it runs the settings of the Python check L4_check_2000.json (2000 steps per turn): the load power differs by at most ${sci(wl * 100)} % and the power the rotor pays by at most ${sci(wp * 100)} %.` };
fs.writeFileSync(path.join(ROOT, 'data', 'sim_check.json'), JSON.stringify({ n: summary, worst, pass, geared: wl == null ? null : { load: wl, paid: wp } }, null, 1));
process.exit(pass ? 0 : 1);
