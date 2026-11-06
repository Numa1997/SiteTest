// Where does the fluid's energy go, operator by operator? Machine side: ΔE_m = W_motor + W_fl. Fluid side: ΔKE = E_rod + E_adv + E_diff + E_proj + E_geom.
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay, P = require('../waterlily/pageparams.json');
const med = process.env.MED || 'glycerol', dx = +(process.env.DX || 0.025), nsub = +(process.env.NSUB || 20), dur = 3;
const Kg = P[med].K, w = new T.World({ dx, x0: -1.6, y0: -0.6, nx: Math.round(3.2 / dx), ny: Math.round(2.0 / dx), machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, 0.08, -0.05, 0, 0, 0], nsub });
let uh = 0, tN = 0; const ctrl = (s, t) => { if (t >= tN - 1e-9) { uh = 0; for (let i = 0; i < 6; i++) uh -= Kg[i] * s[i]; uh = Math.max(-60, Math.min(60, uh)); tN += 0.01; } return uh; };
let Wrod = 0, Wcart = 0; w.onSub = null;
const p = w.mp, E0 = T.energy(p, w.s), K0 = w.KE();
while (w.t < dur - 1e-9) { const x0 = w.s[0]; w.step(ctrl); Wcart += w.Fc * (w.s[0] - x0); }
const B = w.book, dEm = T.energy(p, w.s) - E0, dK = w.KE() - K0, Wrods = B.Wfl - Wcart;
const r = (v) => +v.toFixed(4);
console.log(JSON.stringify({ med, dx, nsub, machine_check: r(dEm - B.Wm - B.Wfl), W_motor: r(B.Wm), W_fl_on_machine: r(B.Wfl), of_which_cart: r(Wcart), of_which_rods: r(Wrods),
  dKE: r(dK), E_rod: r(B.Erod), expected_E_rod: r(-Wrods - B.Drod), E_adv: r(B.Eadv), E_diff: r(B.Ediff), W_shear: r(B.Wshear), E_proj: r(B.Eproj), E_geom: r(dK - B.Erod - B.Eadv - B.Ediff - B.Eproj),
  cart_work_on_fluid: r(-Wcart), proj_plus_shear_minus_cartwork: r(B.Eproj + B.Wshear + Wcart) }));
