// Catch statistics for every pattern of PEND.TARGETS: node tools/fig13/catch_targets.cjs [starts=20] [seconds allowed=150]
// Each start: the page's own start or a dragged pose at rest; Catch it pressed after 4 s; held = still caught 6 s (or 6 laps) later.
const fs = require('fs'), os = require('os'), path = require('path'); const tmp = path.join(os.tmpdir(), 'pend_' + process.pid + '.cjs'); fs.copyFileSync(path.join(__dirname, 'gift/pendulum.js'), tmp);
const P = require(tmp); const NS = +process.argv[2] || 20, CAP = +process.argv[3] || 150;
let seed = 2026; const rnd = () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296;
const starts = [[2.85, 3.0, 0, 0]]; while (starts.length < NS) { const r0 = 0.3 + 1.69 * rnd(), phi = 2 * Math.PI * rnd(), be = Math.acos(r0 / 2); starts.push([phi + be, phi - be, 0, 0]); }
const med = a => a.length ? a.slice().sort((x, y) => x - y)[Math.floor(a.length / 2)] : NaN;
for (const tg of P.TARGETS) {
  const t0 = Date.now(), D = P.design(tg), tD = Date.now() - t0;
  const w = []; let first = 0, heldOK = 0, tauHold = 0;
  for (const s0 of starts) { const R = new P.Run(D, s0, Infinity, Infinity); R.ev.on = Infinity; R.advance(4, 4); R.engage(); let t = 4; const need = Math.max(6, 6 * D.T);
    while (t < 4 + CAP && !(R.mode === 2 && R.ev.catch !== null && R.t - R.ev.catch > need)) { t += 0.5; R.advance(t, 4); }
    if (R.mode === 2 && R.ev.catch !== null && R.t - R.ev.catch > need) { w.push(R.ev.catch - 4); if (!R.hops) first++; if (R.dist < 0.1) heldOK++; const L = R.log.tau; let mx = 0; for (let i = L.length - 200; i < L.length; i++) mx = Math.max(mx, Math.abs(L[i])); tauHold = Math.max(tauHold, mx); } }
  console.log(`${tg.name.padEnd(20)} ${tg.stability.padEnd(8)} E*=${D.Estar.toFixed(0).padStart(4)} J T=${tg.T.toFixed(2)} M=${String(D.M).padStart(4)} close=${D.closure.toExponential(1)} conv=${D.converged ? 'y' : 'N'} design ${tD} ms | caught+held ${w.length}/${NS}, first try ${first}, d<0.1: ${heldOK}, wait median ${med(w).toFixed(1)} s max ${(w.length ? Math.max(...w) : NaN).toFixed(0)} s, hold torque <= ${tauHold.toFixed(2)} N m`);
}
