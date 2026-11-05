// How hard may the balancer's reference speed be changed before the rods are lost?  Measured on the true loop:
// the nonlinear equations (8a), (8), (8b) (notes/fig11/panel/ref.cjs, independent of the page), RK4 at 1 ms, the balancer
// u = sat(-K (s - s_r)) looked at every T_s and held, u_max = 60 N, default machine. Gains K and P from Wolfram (Ts 10 and 40 ms).
// 1. one jump of the reference speed from a balanced cruise: largest jump caught (bisection), against the certified sqrt(0.9 c*/P44)
// 2. a steady deceleration of the reference from 3 m/s, place kept (A) or put at the cart at every look (B): largest caught
// 3. the reference governor of the note: at every look, the reference placed at the cart and its speed moved toward zero by the
//    largest step with W(s - s_r) <= gamma c*; time to stop from 1, 2, 4 m/s, largest lean, largest force, largest W / c*
'use strict';
const R = require('../panel/ref.cjs');
const d = [2.75, 0.5, 0.28125, 0.5 / 3 * 0.25 + 0.75 * 0.25, 0.75 * 0.5 * 0.75 / 2, 0.75 * 0.75 * 0.75 / 3], f = [(0.25 + 0.75) * 0.5 * 9.81, 0.75 * 0.75 * 9.81 / 2], H = 0.001, F = 60;
const G = {
  10: { K: [5.321928301601418, -408.0090336913436, 493.66332331431414, 11.555723079636834, -13.1468125487928, 76.27720437920465], P4: [107.32566475168753, -289.5460505235076, 1377.3396713290297, 172.46250025181004, 105.10587140264147, 239.70984030424538], c: 37.3 },
  40: { K: [2.5283373680916092, -251.3931673751606, 278.99987475813543, 5.540129872466662, -10.589707418704878, 41.286000390868416], P4: [107.85099270513788, -319.2159929626897, 1417.9541136891835, 173.59541550159554, 104.62529668732905, 246.31169488204702], c: 116 } };
// run the loop; refFn(k, s, ref) may change the reference at look k; returns the worst lean and whether the rods came home
function run(Ts, s0, ref0, refFn, Tend) {
  const g = G[Ts], n = Math.round(Ts / H / 1); let s = s0.slice(), ref = Object.assign({}, ref0), u = 0, worst = 0, umax = 0, k = 0, tStop = null;
  for (let i = 0, t = 0; t < Tend; i++) {
    if (i % Ts === 0) { if (refFn) refFn(k++, s, ref, t); const xr = ref.x + ref.v * (t - ref.t0); u = R.lawBalance(g.K, s, xr, ref.v, F); umax = Math.max(umax, Math.abs(u)); if (tStop === null && ref.v === 0 && ref.done) tStop = t; }
    s = R.rk4(d, f, s, u, H); t += H; worst = Math.max(worst, Math.abs(R.wrap(s[1])), Math.abs(R.wrap(s[2])));
    if (worst > 1.4) return { ok: false, worst, umax, tStop };
  }
  return { ok: Math.abs(R.wrap(s[1])) < 0.01 && Math.abs(R.wrap(s[2])) < 0.01 && Math.abs(s[3] - ref.v) < 0.02, worst, umax, tStop, vEnd: s[3] };
}
const W_P = {"10":[[1.0831706840799916e2,-1.0478289684695284e2,6.937814234149572e2,1.0732566475167984e2,6.258033222771424e1,1.2559075742997778e2],[-1.0478289684603095e2,1.2346933918079445e4,-1.5583833530148093e4,-2.89546050521543e2,-2.4127015904966413e2,-2.4360129194695905e3],[6.937814234141078e2,-1.5583833530163098e4,2.784065474742094e4,1.3773396713269753e3,9.84726792090896e2,4.461687410535799e3],[1.0732566475168753e2,-2.895460505235076e2,1.3773396713290297e3,1.7246250025181004e2,1.0510587140264147e2,2.3970984030424538e2],[6.2580332227719566e1,-2.4127015905094464e2,9.847267920922258e2,1.0510587140263974e2,8.621236005564604e1,1.775178824946157e2],[1.2559075742986558e2,-2.43601291947227e3,4.4616874105365105e3,2.397098403039704e2,1.775178824944388e2,7.699285601095363e2]],"40":[[1.0856073232917825e2,-1.185327516920861e2,7.12604423831394e2,1.0785099270514146e2,6.235772640447943e1,1.2865083217318173e2],[-1.1853275169207305e2,1.3136691061614934e4,-1.666058089480186e4,-3.1921599296267186e2,-2.2801631168194464e2,-2.6106569257016677e3],[7.126044238313259e2,-1.666058089480152e4,2.9310198353725966e4,1.4179541136891075e3,9.668178246536739e2,4.7001685077965785e3],[1.0785099270513788e2,-3.192159929626897e2,1.4179541136891835e3,1.7359541550159554e2,1.0462529668732905e2,2.4631169488204702e2],[6.235772640447724e1,-2.2801631168196252e2,9.668178246537323e2,1.0462529668732945e2,8.645254607670066e1,1.7462574139115208e2],[1.286508321731706e2,-2.6106569257015803e3,4.700168507796538e3,2.463116948820349e2,1.7462574139114253e2,8.086432365854125e2]]};   // P from Wolfram's DiscreteRiccatiSolve with the exact period cost
const bisect = (ok, lo, hi) => { for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; if (ok(m)) lo = m; else hi = m; } return lo; };
const deg = (r) => (r * 180 / Math.PI).toFixed(2) + '°';
for (const Ts of [10, 40]) {
  const g = G[Ts], cert = Math.sqrt(0.9 * g.c / g.P4[3]);
  // 1. a jump of the reference speed by D from a balanced cruise at 2 m/s
  const jump = (D) => run(Ts, [0, 0, 0, 2, 0, 0], { x: 0, v: 2 - D, t0: 0 }, null, 30).ok;
  const scan = []; for (let D = 0.1; D <= 12.001; D += 0.1) scan.push(jump(D) ? '+' : '.');
  console.log(`Ts ${Ts} ms: jumps of 0.1 to 12 m/s in steps of 0.1 (+ caught, . lost): ${scan.join('')}`);
  const Dmax = bisect(jump, 0, 20), at = run(Ts, [0, 0, 0, 2, 0, 0], { x: 0, v: 2 - 0.999 * Dmax, t0: 0 }, null, 30);
  console.log(`Ts ${Ts} ms: one speed jump: certified ${cert.toFixed(3)} m/s (sqrt(0.9 c*/P44), c* = ${g.c}); largest caught ${Dmax.toFixed(3)} m/s (${(Dmax / cert).toFixed(1)} times), worst lean there ${deg(at.worst)}, force ${at.umax.toFixed(1)} N`);
  // 2. a steady deceleration from 40 m/s to rest (long enough to be steady)
  for (const mode of ['A', 'B']) {
    const ramp = (a) => run(Ts, [0, 0, 0, 40, 0, 0], { x: 0, v: 40, t0: 0 }, (k, s, ref, t) => { if (ref.v === 0) return; const v = Math.max(0, ref.v - a * Ts / 1000);
      const xr = mode === 'B' ? s[0] : ref.x + ref.v * (t - ref.t0); ref.x = xr; ref.v = v; ref.t0 = t; ref.done = v === 0; }, 60).ok;
    const amax = bisect(ramp, 0, 30); const at2 = run(Ts, [0, 0, 0, 40, 0, 0], { x: 0, v: 40, t0: 0 }, (k, s, ref, t) => { if (ref.v === 0) return; const v = Math.max(0, ref.v - 0.999 * amax * Ts / 1000); const xr = mode === 'B' ? s[0] : ref.x + ref.v * (t - ref.t0); ref.x = xr; ref.v = v; ref.t0 = t; ref.done = v === 0; }, 60);
    console.log(`  steady deceleration from 40 m/s, place ${mode === 'A' ? 'kept (A)' : 'at the cart (B)'}: largest caught ${amax.toFixed(2)} m/s², worst lean there ${deg(at2.worst)} (arctan(a/g) = ${deg(Math.atan(amax / 9.81))}), force ${at2.umax.toFixed(1)} N`);
  }
  // 3. the governor
  for (const gam of [0.9, 0.5, 0.25]) for (const v0 of [1, 2, 4]) {
    let wmax = 0, nsteps = 0;
    const r = run(Ts, [0, 0, 0, v0, 0, 0], { x: 0, v: v0, t0: 0 }, (k, s, ref, t) => {
      const e = [0, R.wrap(s[1]), R.wrap(s[2]), s[3] - ref.v, s[4], s[5]];   // place at the cart: x error zero
      const Pe4 = e.reduce((a, v, i) => a + g.P4[i] * v, 0), Pfull = null;
      const W = Wof(Ts, e); wmax = Math.max(wmax, W / g.c);
      if (ref.v === 0) { ref.done = true; return; }
      const disc = Pe4 * Pe4 - g.P4[3] * (W - gam * g.c); if (disc < 0) { ref.x = s[0]; ref.t0 = t; return; }
      const sgn = Math.sign(ref.v), Dm = (-sgn * Pe4 + Math.sqrt(disc)) / g.P4[3];   // largest change of v_r toward zero: W(e + D sgn e4) <= gam c*
      const D = Math.max(0, Math.min(Math.abs(ref.v), Dm)); ref.x = s[0]; ref.v = ref.v - sgn * D; ref.t0 = t; nsteps++; }, 40);
    console.log(`  governor gamma ${gam}, from ${v0} m/s: stopped after ${r.tStop === null ? 'NOT' : r.tStop.toFixed(2) + ' s'}, caught ${r.ok}, worst lean ${deg(r.worst)}, force at most ${r.umax.toFixed(2)} N, W at a look at most ${wmax.toFixed(2)} c*`);
  }
}
function Wof(Ts, e) { return W_P[Ts] ? quad(W_P[Ts], e) : NaN; }
function quad(P, e) { let t = 0; for (let i = 0; i < 6; i++) for (let j = 0; j < 6; j++) t += e[i] * P[i][j] * e[j]; return t; }
