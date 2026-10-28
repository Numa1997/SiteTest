#!/usr/bin/env node
// The Wind tab's physics block (rotor_wind.html, between /*WIND-BEGIN*/ and /*WIND-END*/) against its Python reference,
// notes/rotor-pendula/derive/L6_wind.py (data/L6_wind_ref.json): the same field from the same random numbers, the
// rotor-effective wind, the steady rotor speed and brake, and a 60 s run of the machine with the wing-shaped second blade
// (every term in use). Then the energy book over a full field period at 8 m/s. Writes data/wind_check.json.
// Usage: node tools/check_wind.js [page]   (about 20 s)
const fs = require('fs');
const path = require('path');
const PAGE = process.argv[2] || path.join(__dirname, '..', 'rotor_wind.html');
const src = fs.readFileSync(PAGE, 'utf8');
const a = src.indexOf('/*WIND-BEGIN*/'), b = src.indexOf('/*WIND-END*/');
if (a < 0 || b < a) throw new Error('no wind block in ' + PAGE);
const W = new Function(src.slice(a, b) + '\nreturn { WCONST, synthField, makeMachine, wStep, wEnergy, veffAt, wStart };')();
const ref = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'L6_wind_ref.json'), 'utf8'));
let fails = 0;
const check = (name, ok, detail) => { if (!ok) fails++; console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? '  (' + detail + ')' : '')); };
const T0 = Date.now();
const F = W.synthField(ref.U, ref.cls, ref.seed);
const synthMs = Date.now() - T0;
let worstF = 0;
for (const s of ref.field_samples) worstF = Math.max(worstF, Math.abs(F.f[s.comp][s.k * F.P + s.p] - s.value));
check('field samples equal the reference', worstF < 1e-9, 'worst ' + worstF.toExponential(2) + ' m/s');
let worstV = 0;
ref.veff.forEach((v, k) => { worstV = Math.max(worstV, Math.abs(F.veff[k] - v)); });
check('rotor-effective wind equals the reference', worstV < 1e-9, 'worst ' + worstV.toExponential(2) + ' m/s');
const md = W.makeMachine(F, ref.shape);
check('steady rotor speed and brake equal the reference', Math.abs(md.Om0 - ref.Om0) < 1e-9 && Math.abs(md.c - ref.c) < 1e-8,
  `Omega0 ${md.Om0} vs ${ref.Om0}`);
let y = W.wStart(F, md), t = 0, worstR = 0, worstTh = 0;
const h = W.WCONST.h, every = 200;
for (let k = 0, j = 0; j < ref.run.length; k++) {
  if (k % every === 0) {
    const r = ref.run[j++];
    for (let i = 0; i < 7; i++) worstR = Math.max(worstR, Math.abs(y[i] - r[1 + i]) / Math.max(1, Math.abs(r[1 + i])));
    worstTh = Math.max(worstTh, Math.abs(y[2] - r[3]));
  }
  y = W.wStep(t, y, h, F, md); t += h;
}
check('60 s run, wing: state equals the reference', worstR < 1e-7, 'worst relative ' + worstR.toExponential(2) + ', theta ' + worstTh.toExponential(2) + ' rad');
// energy book over one field period at 8 m/s, class A, record 1, wing
y = W.wStart(F, md); t = 0;
const E0 = W.wEnergy(y); let worstB = 0;
const n = Math.round(W.WCONST.Trec / h);
for (let k = 0; k < n; k++) {
  y = W.wStep(t, y, h, F, md); t += h;
  if (k % 20 === 0) {
    const res = y[4] + y[5] - y[6] - (W.wEnergy(y) - E0);
    worstB = Math.max(worstB, Math.abs(res) / (Math.abs(y[4]) + Math.abs(y[5]) + y[6] + Math.abs(W.wEnergy(y) - E0)));
  }
}
check('energy book over 256 s closes', worstB < 1e-6, 'worst relative residual ' + worstB.toExponential(2));
const out = { synth_ms: synthMs, field_worst: worstF, veff_worst: worstV, run_worst_rel: worstR, book_worst_rel: worstB, P_mean_256: y[6] / t };
fs.writeFileSync(path.join(__dirname, '..', 'data', 'wind_check.json'), JSON.stringify(out, null, 1));
console.log(`synthesis ${synthMs} ms; mean power over 256 s ${(y[6] / t * 1e3).toFixed(1)} mW`);
process.exit(fails ? 1 : 0);
