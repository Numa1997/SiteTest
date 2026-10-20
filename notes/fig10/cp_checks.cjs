// Fig. 10, scratch checks of the power-coefficient fit and the controller numbers.
// cp() and tauAero() are copied verbatim from public/simulations/wind-turbine.html (L643-L652), constants from L554-L556.
// Run: node notes/fig10/cp_checks.cjs
'use strict';
var RHO = 1.225, R = 40, J = 4.0e6, AREA = Math.PI * R * R, TMAX = 1.2e6, WN = 0.6, ZC = 0.8;
var C1 = 0.5176, C2 = 116, C4 = 5, C5 = 21, C6 = 0.0068;
function cp(lam) {
    if (lam <= 0.05) return 0;
    var inv = 1 / lam - 0.035;
    if (inv <= 0) return 0;
    var li = 1 / inv;
    return Math.max(0, C1 * (C2 / li - C4) * Math.exp(-C5 / li) + C6 * lam);
}
function cpVariant(lam) { // the reproduction with c6 * lambda_i as the last term
    var inv = 1 / lam - 0.035; if (inv <= 0) return 0; var li = 1 / inv;
    return Math.max(0, C1 * (C2 / li - C4) * Math.exp(-C5 / li) + C6 * li);
}
function tauAero(w, v) {
    return w > 1e-6 ? 0.5 * RHO * AREA * v * v * v * cp(w * R / v) / w : 0;
}
var out = {};
// 1. the page's own scan (optimum(), L655)
var best = 0, lbest = 0;
for (var l = 0.5; l <= 14; l += 0.001) { var c = cp(l); if (c > best) { best = c; lbest = l; } }
out.lam_opt = lbest; out.cp_max = best;
out.K_opt = 0.5 * RHO * Math.PI * Math.pow(R, 5) * best / Math.pow(lbest, 3);
// 2. the variant
var bv = 0, lv = 0;
for (l = 0.5; l <= 14; l += 0.001) { c = cpVariant(l); if (c > bv) { bv = c; lv = l; } }
out.variant = { cp_max: bv, lam_opt: lv };
// 3. where the unclipped fit crosses zero
function raw(lam) { var li = 1 / (1 / lam - 0.035); return C1 * (C2 / li - C4) * Math.exp(-C5 / li) + C6 * lam; }
var a = 12, b = 14; for (var k = 0; k < 60; k++) { var m = (a + b) / 2; if (raw(m) > 0) a = m; else b = m; }
out.cp_zero = a;
// 4. c_p / lambda^3: where it rises, and its sign against the value at the optimum, grid 1e-4 from 0.0501
var g0 = best / Math.pow(lbest, 3), rises = [], prev = null, bad = [];
for (var i = 501; i <= 140000; i++) {
    var x = i * 1e-4, f = cp(x) / (x * x * x);
    if (prev !== null && f > prev) rises.push(x);
    prev = f;
    if (x < lbest - 1e-3 && !(f > g0)) bad.push(['below', x]);
    if (x > lbest + 1e-3 && !(f < g0)) bad.push(['above', x]);
}
out.cp_over_lam3_rises = rises.length ? [rises[0], rises[rises.length - 1]] : null;
out.sign_violations = bad.slice(0, 5); out.sign_violation_count = bad.length;
// 5. powers and speeds of sections 1, 2, 4
out.area = AREA;
out.P_wind_8 = 0.5 * RHO * AREA * 512; out.P_wind_11 = 0.5 * RHO * AREA * 1331;
out.omega_15rpm = 15 * 2 * Math.PI / 60; out.tip_15rpm = out.omega_15rpm * R; out.tip_kmh = out.tip_15rpm * 3.6;
out.best_8 = best * out.P_wind_8; out.rpm_best_8 = lbest * 8 / R * 60 / (2 * Math.PI);
out.omega_star_8 = lbest * 8 / R;
out.relax_8 = J / (3 * out.K_opt * out.omega_star_8);
// slope of tau_aero at the optimum, numerically, against -K_opt * omega_*
var ws = out.omega_star_8;
out.slope_at_opt_numeric = (tauAero(ws + 1e-4, 8) - tauAero(ws - 1e-4, 8)) / 2e-4;
out.slope_at_opt_formula = -out.K_opt * ws;
// 6. PI gains at 15 rpm, 8 m/s (solve(), L698-L699)
var wref = 15 * 2 * Math.PI / 60;
var dtd = (tauAero(wref + 1e-4, 8) - tauAero(wref - 1e-4, 8)) / 2e-4;
out.dtau_dw = dtd; out.Kp = 2 * ZC * WN * J + dtd; out.Ki = J * WN * WN;
out.decay_rate = ZC * WN; out.omega_d = WN * Math.sqrt(1 - ZC * ZC);
out.swing_ratio = Math.exp(-Math.PI * ZC / Math.sqrt(1 - ZC * ZC));
// 7. the step: lambda at 9.5 m/s and 15 rpm, c_p there
out.lam_step = wref * R / 9.5; out.cp_step = cp(out.lam_step);
// 8. the relative-wind angle at the tip and at mid-blade at lambda_opt
out.tip_angle_deg = Math.atan(1 / lbest) * 180 / Math.PI;
out.mid_angle_deg = Math.atan(2 / lbest) * 180 / Math.PI;
console.log(JSON.stringify(out, null, 1));
