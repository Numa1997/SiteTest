// Energy book of the coupled run: W_motor = ΔE_machine + ΔKE_fluid + D_rod (below the grid) + D_visc (resolved) + R (the scheme's loss)
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay, P = require('../waterlily/pageparams.json');
const med = process.env.MED || 'glycerol', dx = +(process.env.DX || 0.025), dur = +(process.env.DUR || 3), nsub = +(process.env.NSUB || 5);
const Kg = P[med].K, w = new T.World({ dx, U: +(process.env.U || 0), x0: -1.6, y0: -0.6, nx: Math.round(3.2 / dx), ny: Math.round(2.0 / dx), machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, 0.08, -0.05, 0, 0, 0], nsub });
let uh = 0, tNext = 0; const ctrl = (s, t) => { if (t >= tNext - 1e-9) { uh = 0; for (let i = 0; i < 6; i++) uh -= Kg[i] * s[i]; uh = Math.max(-60, Math.min(60, uh)); tNext += 0.01; } return uh; };
if (process.env.TOL) w.P.tol = +process.env.TOL; for (const k of (process.env.OPT || '').split(',').filter(Boolean)) w[k] = true; const p = w.mp, E0 = T.energy(p, w.s), K0 = w.KE(), t0 = Date.now(); let n = 0;
while (w.t < dur - 1e-9) { w.step(ctrl); n++; }
const B = w.book, dEm = T.energy(p, w.s) - E0, dK = w.KE() - K0, Dv = B.Wshear - B.Ediff, R = B.Wm - dEm - dK - B.Drod - Dv;
console.log(JSON.stringify({ med, dx, nsub, t: +w.t.toFixed(3), x: +w.s[0].toFixed(4), th1: +w.s[1].toFixed(5), th2: +w.s[2].toFixed(5),
  W_motor: +B.Wm.toFixed(5), dE_machine: +dEm.toFixed(5), dKE_fluid: +dK.toFixed(5), D_rod_subgrid: +B.Drod.toFixed(5), D_visc_resolved: +Dv.toFixed(5), R_scheme: +R.toFixed(5), R_pct_of_motor: +(100 * R / B.Wm).toFixed(1),
  E_advect: +B.Eadv.toFixed(5), ms_per_step: +((Date.now() - t0) / n).toFixed(1), prof_ms: w.prof.map(v => +(v / n).toFixed(2)), realtime_factor: +((Date.now() - t0) / 1000 / w.t).toFixed(2) }));
