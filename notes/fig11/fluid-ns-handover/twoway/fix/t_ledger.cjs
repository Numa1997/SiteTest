// The energy book of the coupled run, every scheme loss named and measured, and the residual (should be round-off if nothing is missing).
// Wm = ΔE_machine + ΔK_fluid + D_rod + D_visc + L_adv + L_proj + L_imp + L_lag + L_transit − E_geom + E_out + residual
require('../../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay, P = require('../../waterlily/pageparams.json');
const med = process.env.MED || 'glycerol', dx = +(process.env.DX || 0.025), nsub = +(process.env.NSUB || 20), dur = +(process.env.DUR || 3);
const Kg = P[med].K, w = new T.World({ dx, U: +(process.env.U || 0), x0: -1.6, y0: -0.6, nx: Math.round(3.2 / dx), ny: Math.round(2.0 / dx), machine: { m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: med }, s: [0, 0.08, -0.05, 0, 0, 0], nsub });
for (const k of (process.env.OPT || '').split(',').filter(Boolean)) w[k] = true;
let uh = 0, tN = 0; const ctrl = (s, t) => { if (t >= tN - 1e-9) { uh = 0; for (let i = 0; i < 6; i++) uh -= Kg[i] * s[i]; uh = Math.max(-60, Math.min(60, uh)); tN += 0.01; } return uh; };
let Wcart = 0, Wrodsum = 0; const p = w.mp, E0 = T.energy(p, w.s), K0 = w.KE();
while (w.t < dur - 1e-9) { const fl0 = w.book.Wfl || 0; w.step(ctrl); }
const B = w.book, dEm = T.energy(p, w.s) - E0, dK = w.KE() - K0, Wc = B.WcNP + B.WcP, Wrods = B.Wfl - Wc;
const Dvisc = B.Wshear - (B.Ediff - B.EimpD), Ladv = -(B.Eadv - B.EimpA), Lproj = B.Lproj, Limp = B.Wimp - B.Eimp;
const Lt = -Wrods - B.Drod - B.Erod;   // the rods' energy that left the machine, less the heat below the grid and what the spreading gave the water
const Llag = -Wc - (B.Wshear + B.Wimp - B.WcPend);   // the cart's energy that left the machine, less what arrived through shear, overrides and pressure at the end velocity
const Eout = B.Ebnd || 0, other = dK - (B.Erod + B.Eadv + B.Ediff + B.Eproj + B.Egeom);
const Rold = B.Wm - dEm - dK - B.Drod - (B.Wshear - B.Ediff);
const resid = B.Wm - dEm - dK - B.Drod - Dvisc - Ladv - Lproj - Limp - Llag - Lt + B.Egeom + Eout;
const r = (v) => +v.toFixed(5);
console.log(JSON.stringify({ med, nsub, U: w.U, W_motor: r(B.Wm), machine_check: r(dEm - B.Wm - B.Wfl), dE_machine: r(dEm), dK: r(dK), D_rod: r(B.Drod), D_visc: r(Dvisc), L_adv: r(Ladv), L_proj: r(Lproj), L_imp: r(Limp), L_lag: r(Llag), L_transit: r(Lt), E_geom: r(B.Egeom), E_in_ends: r(Eout), K_unbucketed: r(other), R_old: r(Rold), R_old_pct: +(100 * Rold / B.Wm).toFixed(2), residual: r(resid), residual_pct: +(100 * resid / B.Wm).toFixed(3) }));
