// The controllers against the stout, through the probes and the Kalman filter, in Node:
//   node tools/fig12/control.cjs <3d|modal|nm> <bump mm | push N> <off,speed,slosh,...> [dx] [seconds]
// Scenario "25" (a number): one cosine bump of that height at the set speed 1 m/s, the cart starting at x = 0.5 m (the bump is
// at 1 m: the disturbance is over by t = 0.65 s). Scenario "push10" (push and a force in N): a flat road, and the reader's push
// F(t) = F0 sin(pi t / 0.3 s) for t < 0.3 s on the cart at 1 m/s, a hard forward start of the same shape as linearity.cjs.
// SENSE=0.001 adds that much noise (m, standard deviation) to each probe reading, and a fifth of it in m/s to the speed.
// The lean is the probes' reading, front − back wall (2 y_q without the added noise): what the page shows as the lean.
// Printed per controller: the largest lean during and after the disturbance, the fitted free decay after it, the time until
// the lean stays within 3 mm, the rms lean in the last second (the residual), the rms and largest motor current, the rms of
// the estimate's error against the probes' lean (2 q_hat − lean) and, for the live model, against the true mode 2 q_1.
// The decay fit, on [t_end + 0.05 s, t_end + 1.5 s]: lean = e^{−sigma t} (a cos w_d t + b sin w_d t) + c, w_d and sigma
// scanned, a, b, c by least squares; zeta = sigma / sqrt(sigma^2 + w_d^2). OUT=file.json saves the series.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { World } = load('stout-cart.js'), G = load('guinness-glass.js'), NM = load('stout-nm.js');
const model = process.argv[2] || 'modal', scen = process.argv[3] || '25', ctrls = (process.argv[4] || 'off,speed,slosh').split(',');
const dx = +(process.argv[5] || 0.004), T = +(process.argv[6] || 3.0), sense = +(process.env.SENSE || 0);
const isPush = /^push/.test(scen), F0 = isPush ? +scen.slice(4) : 0, bumpH = isPush ? 0 : +scen / 1000, Tp = 0.3;
// ON=1.0: every run starts in open loop and the controller named is switched on at that time (s), the stout already swinging:
// then the decay is fitted from the switch on. This is the page's experiment: turn the controller on and watch the stout calm.
const ON = process.env.ON ? +process.env.ON : null;
const tEnd = ON !== null ? ON : isPush ? Tp : 0.65;
function decayFit(ts, ys) {
  const rng = (a, b, n) => Array.from({ length: n }, (_, k) => a + (b - a) * k / (n - 1));
  let best = null;
  const tryAll = (ws, ss) => {
    for (const w of ws) for (const s of ss) {
      // least squares y = a e cos + b e sin + c
      const X = ts.map((t) => { const e = Math.exp(-s * (t - ts[0])); return [e * Math.cos(w * t), e * Math.sin(w * t), 1]; });
      const N = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], r = [0, 0, 0];
      X.forEach((x, k) => { for (let i = 0; i < 3; i++) { r[i] += x[i] * ys[k]; for (let j = 0; j < 3; j++) N[i][j] += x[i] * x[j]; } });
      const sol = solve3(N, r); if (!sol) continue;
      let e = 0; X.forEach((x, k) => { const d = ys[k] - (sol[0] * x[0] + sol[1] * x[1] + sol[2] * x[2]); e += d * d; });
      e = Math.sqrt(e / ys.length);
      if (!best || e < best.e) best = { w, s, e, a: Math.hypot(sol[0], sol[1]), c: sol[2] };
    }
  };
  tryAll(rng(2 * Math.PI * 1.0, 2 * Math.PI * 4.5, 71), rng(0, 25, 101));
  tryAll(rng(best.w - 0.3, best.w + 0.3, 31), rng(Math.max(0, best.s - 0.3), best.s + 0.3, 31));
  return { f: best.w / 2 / Math.PI, sigma: best.s, zeta: best.s / Math.hypot(best.s, best.w), amp: best.a, rms: best.e, c: best.c };
}
function solve3(A, b) {
  const M = A.map((r, i) => r.concat([b[i]]));
  for (let c = 0; c < 3; c++) {
    let p = c; for (let r = c + 1; r < 3; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    if (Math.abs(M[p][c]) < 1e-300) return null; [M[c], M[p]] = [M[p], M[c]];
    for (let r = 0; r < 3; r++) if (r !== c) { const f = M[r][c] / M[c][c]; for (let k = c; k < 4; k++) M[r][k] -= f * M[c][k]; }
  }
  return [0, 1, 2].map((i) => M[i][3] / M[i][i]);
}
const results = [];
for (const ctrl of ctrls) {
  const bumps = []; for (let n = 0; n < 60; n++) bumps.push({ x: 1.0 + 2 * n, h: bumpH, L: 0.25 });
  const w = new World({
    fluid: { dx, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03, modal: model === 'modal' || model === 'nm', nm: model === 'nm', nmCoeffs: NM },
    road: { bumps, Rw: 0.04, xmin: -1, xmax: 125 },
    cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: 1, ctrl: ON !== null ? 'off' : ctrl },
    sensors: { noiseQ: sense, noiseV: sense / 5 },
    dtMax: 1 / 200
  });
  const f = w.fluid, c = w.cart, t0 = Date.now(), rows = [];
  while (w.t < T - 1e-9) {
    if (ON !== null && c.ctrl !== ctrl && w.t >= ON - 1e-9) { c.ctrl = ctrl; c.xi = 0; }   // as the page's buttons do
    c.pushF = isPush && w.t < Tp ? F0 * Math.sin(Math.PI * (w.t + 0.0025) / Tp) : 0;   // held over the 5 ms step, sampled at its middle
    w.advance(1 / 200);
    const pr = c.probe, lean = pr.ef - pr.eb, est = 2 * c.obs.x[1], truth = f.modal ? 2 * f.q[0] : NaN;
    rows.push([w.t, lean, est, truth, c.i, c.vx, 2 * pr.y]);
  }
  const during = rows.filter((r) => r[0] <= tEnd + 0.05), after = rows.filter((r) => r[0] > tEnd + 0.05);
  const peak = (a) => a.reduce((m, r) => Math.max(m, Math.abs(r[1])), 0);
  const win = after.filter((r) => r[0] <= tEnd + 1.5), fit = decayFit(win.map((r) => r[0]), win.map((r) => r[1]));
  let tIn = tEnd; for (const r of rows) if (r[0] > tEnd && Math.abs(r[1]) > 0.003) tIn = r[0];
  if (tIn > T - 0.1) tIn = Infinity;                           // still above 3 mm at the end of the run
  const last = rows.filter((r) => r[0] > T - 1), rms = (a, k) => Math.sqrt(a.reduce((s, r) => s + r[k] * r[k], 0) / a.length);
  const estErr = Math.sqrt(rows.reduce((s, r) => s + (r[2] - r[1]) ** 2, 0) / rows.length);
  const truthErr = f.modal ? Math.sqrt(rows.reduce((s, r) => s + (r[2] - r[3]) ** 2, 0) / rows.length) : NaN;
  const iMax = rows.reduce((m, r) => Math.max(m, Math.abs(r[4])), 0), iRms = rms(rows, 4);
  const spill = (w.spilledMass || 0) * 1000;
  const res = { ctrl, peakDuring: peak(during) * 1000, peakAfter: peak(after) * 1000, fit, tWithin3mm: tIn - tEnd, residualRms: rms(last, 1) * 1000, iRms, iMax, estErr: estErr * 1000, truthErr: truthErr * 1000, spill, secs: (Date.now() - t0) / 1000 };
  results.push(Object.assign({ series: rows.map((r) => r.map((v) => +(+v).toPrecision(6))) }, res));
  console.log(`${model} ${dx * 1000} mm, ${isPush ? 'push ' + F0 + ' N' : 'bump ' + scen + ' mm'}${sense ? ', added noise ' + sense * 1000 + ' mm' : ''}, ${ON !== null ? 'open loop, then ' + ctrl + ' from ' + ON + ' s' : ctrl}: lean peak ${res.peakDuring.toFixed(1)} mm during, ${res.peakAfter.toFixed(1)} mm after; free decay ${fit.f.toFixed(2)} Hz, zeta ${fit.zeta.toFixed(3)} (sigma ${fit.sigma.toFixed(2)} 1/s, fit rms ${(fit.rms * 1000).toFixed(2)} mm, offset ${(fit.c * 1000).toFixed(2)} mm); within 3 mm ${isFinite(res.tWithin3mm) ? 'after ' + res.tWithin3mm.toFixed(2) + ' s' : 'never in the run'}; residual rms ${res.residualRms.toFixed(2)} mm; current rms ${iRms.toFixed(2)} A, max ${iMax.toFixed(2)} A; estimate error rms ${res.estErr.toFixed(2)} mm vs probes${f.modal ? ', ' + res.truthErr.toFixed(2) + ' mm vs mode 1' : ''}; spilled ${spill.toFixed(1)} g (${res.secs.toFixed(0)} s)`);
}
if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify({ model, scen, dx, T, sense, cols: ['t s', 'lean m', '2 q_hat m', '2 q1 m', 'i A', 'v m/s', 'probe reading 2 y_q m'], results }));
