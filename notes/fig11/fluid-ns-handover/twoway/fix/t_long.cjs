// Stability of the solved fluid over a long run: the page's LQR balancing for 60 s, a flick (both rods kicked) every 15 s.
// Prints per 10 s: max |θ1|, |θ2|, |x|, the scheme's loss R so far (% of motor work), the lag gain so far, the fluid's KE; NaN check.
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay, P = require('../../waterlily/pageparams.json');
const med = process.env.MED || 'glycerol', DUR = +(process.env.DUR || 60), KICK = +(process.env.KICK || 1.5), Kg = P[med].K;
const w = new T.World({ dx: 0.025, U: +(process.env.U || 0), machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, 0.04, -0.02, 0, 0, 0], nsub: 20 });
let uh = 0, tN = 0; const ctrl = (s, t) => { if (t >= tN - 1e-9) { uh = 0; for (let i = 0; i < 6; i++) uh -= Kg[i] * s[i]; uh = Math.max(-60, Math.min(60, uh)); tN += 0.01; } return uh; };
const p = w.mp, E0 = T.energy(p, w.s), K0 = w.KE(); let mx = [0, 0, 0], nextKick = 5, nextOut = 10, bad = false;
while (w.t < DUR - 1e-9) { if (w.t >= nextKick - 1e-9) { w.s[4] += KICK; w.s[5] -= KICK; nextKick += 15; }
  w.step(ctrl); mx = [Math.max(mx[0], Math.abs(w.s[1])), Math.max(mx[1], Math.abs(w.s[2])), Math.max(mx[2], Math.abs(w.s[0]))]; if (!w.s.every(isFinite)) { bad = true; break; }
  if (w.t >= nextOut - 1e-9) { const B = w.book, dEm = T.energy(p, w.s) - E0, dK = w.KE() - K0, Dv = B.Wshear - (B.Ediff - B.EimpD), R = B.Wm - dEm - dK - B.Drod - Dv;
    console.log(JSON.stringify({ med, t: +w.t.toFixed(1), max_th1: +mx[0].toFixed(3), max_th2: +mx[1].toFixed(3), max_x: +mx[2].toFixed(3), W_motor: +B.Wm.toFixed(3), R_pct: +(100 * R / B.Wm).toFixed(1), L_lag: +(-(B.WcNP + B.WcP) - (B.Wshear + B.Wimp - B.WcPend)).toFixed(3), KE_fluid: +w.KE().toFixed(4) })); mx = [0, 0, 0]; nextOut += 10; } }
console.log(bad ? 'NaN: UNSTABLE' : 'finite to the end');
