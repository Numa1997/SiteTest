// Gate 2, L1: single-collector time 40 -> 100 um with Stokes and with the drag balance, weights and bounds (text, chapter 2)
const P = require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs');
const A = P.air(283.15, 85000), r = 8e-6, W = 300e6 * P.massOf(8e-6);
function integrate(f, a, b, n) { let s = 0, h = (b - a) / n; for (let i = 0; i < n; i++) { const x = a + (i + 0.5) * h; s += f(x) * h; } return s; }
const w = R => 4 * 1000 * R * R / ((R + r) * (R + r) * W);
const dvS = R => P.vStokes(R, A) - P.vStokes(r, A), dvB = R => P.vBeard(R, A) - P.vBeard(r, A);
const tS = integrate(R => w(R) / dvS(R), 40e-6, 100e-6, 20000) / 60, tB = integrate(R => w(R) / dvB(R), 40e-6, 100e-6, 20000) / 60;
let lo = 1e9, hi = 0; for (let R = 40e-6; R <= 100e-6; R += 1e-7) { const q = dvS(R) / dvB(R); lo = Math.min(lo, q); hi = Math.max(hi, q); }
console.log('t_Stokes = %s min (text 9.96), t_drag = %s min (text 13.02), ratio %s (text 1.31), bounds %s %s (text 1.12, 1.70)', tS.toFixed(3), tB.toFixed(3), (tB / tS).toFixed(3), lo.toFixed(3), hi.toFixed(3));
