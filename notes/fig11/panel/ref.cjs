// An independent reference for the project 05 page (Balancing Two Rods on a Cart), written from the lecture note,
// not copied from the page's code: rows (8a), (8), (8b) of the equations of motion, solved by Cramer's rule;
// RK4 as in (18); the reference equilibria (25)-(26); the three laws of the supervisor (16), (21), (24).
// Everything takes the machine as d = (d1..d6) and f = (f1, f2) of (6)-(7), read from the page's store.
'use strict';
const TAU = 2 * Math.PI;

// (8a), (8), (8b):  M q'' = r, with q = (x, th1, th2)
function accel(d, f, s, u) {
  const [x, a, b, xd, ad, bd] = s, c1 = Math.cos(a), c2 = Math.cos(b), s1 = Math.sin(a), s2 = Math.sin(b), c12 = Math.cos(a - b), s12 = Math.sin(a - b);
  const M = [[d[0], d[1] * c1, d[2] * c2], [d[1] * c1, d[3], d[4] * c12], [d[2] * c2, d[4] * c12, d[5]]];
  const r = [u + d[1] * s1 * ad * ad + d[2] * s2 * bd * bd,      // (8a): d1 x'' + d2 c1 th1'' + d3 c2 th2'' - d2 s1 th1'^2 - d3 s2 th2'^2 = u
             f[0] * s1 - d[4] * s12 * bd * bd,                    // (8):  d2 c1 x'' + d4 th1'' + d5 c12 th2'' + d5 s12 th2'^2 - f1 s1 = 0
             f[1] * s2 + d[4] * s12 * ad * ad];                   // (8b): d3 c2 x'' + d5 c12 th1'' + d6 th2'' - d5 s12 th1'^2 - f2 s2 = 0
  const det3 = (A) => A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]);
  const D = det3(M), col = (k) => M.map((row, i) => row.map((v, j) => (j === k ? r[i] : v)));
  return [det3(col(0)) / D, det3(col(1)) / D, det3(col(2)) / D];
}
function rhs(d, f, s, u) { const q = accel(d, f, s, u); return [s[3], s[4], s[5], q[0], q[1], q[2]]; }
function rk4(d, f, s, u, h) {   // (18)
  const k1 = rhs(d, f, s, u), k2 = rhs(d, f, s.map((v, i) => v + h / 2 * k1[i]), u), k3 = rhs(d, f, s.map((v, i) => v + h / 2 * k2[i]), u), k4 = rhs(d, f, s.map((v, i) => v + h * k3[i]), u);
  return s.map((v, i) => v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]));
}
function wrap(a) { return a - TAU * Math.round(a / TAU); }
// (25) fixed and cruise, (26) the glide: e(tau) = (e0 + (v + w e0) tau) e^{-w tau}
function refAt(kind, x0, v0, t0, e0, t, w) {
  if (kind === 0) return [x0, 0];
  const tau = t - t0; if (kind === 1) return [x0 + v0 * tau, v0];
  const B = v0 + w * e0, ex = Math.exp(-w * tau); return [x0 + (e0 + B * tau) * ex, (B - w * (e0 + B * tau)) * ex];
}
const sat = (v, F) => Math.max(-F, Math.min(F, v));
// (16): u = sat(-K (s - s_r)), s_r = (x_r, 0, 0, v_r, 0, 0), angles measured after wrapping
function lawBalance(K, s, xr, vr, F) { const e = [s[0] - xr, wrap(s[1]), wrap(s[2]), s[3] - vr, s[4], s[5]]; let v = 0; for (let i = 0; i < 6; i++) v -= K[i] * e[i]; return sat(v, F); }
// (21): a = clip(k P - 4 (x - xc) - 4 x', +-8), P = d2 c1 th1' + d3 c2 th2'; the force that gives the cart this acceleration, from rows (8), (8b) then (8a)
function forceFor(d, f, s, a) {
  const [x, t1, t2, xd, w1, w2] = s, c1 = Math.cos(t1), c2 = Math.cos(t2), s1 = Math.sin(t1), s2 = Math.sin(t2), c12 = Math.cos(t1 - t2), s12 = Math.sin(t1 - t2);
  const b1 = f[0] * s1 - d[4] * s12 * w2 * w2 - d[1] * c1 * a, b2 = f[1] * s2 + d[4] * s12 * w1 * w1 - d[2] * c2 * a;
  const A = d[3], B = d[4] * c12, C = d[5], det = A * C - B * B, q1 = (b1 * C - B * b2) / det, q2 = (A * b2 - B * b1) / det;
  return d[0] * a + d[1] * c1 * q1 + d[2] * c2 * q2 - d[1] * s1 * w1 * w1 - d[2] * s2 * w2 * w2;
}
function lawCalm(d, f, s, xc, kc, F) { const P = d[1] * Math.cos(s[1]) * s[4] + d[2] * Math.cos(s[2]) * s[5], a = Math.max(-8, Math.min(8, kc * P - 4 * (s[0] - xc) - 4 * s[3])); return sat(forceFor(d, f, s, a), F); }
// (24): u = sat(u_plan[k] - K_k (s - x_c e1 - s_plan[k])), k = round((t - t_plan) / 10 ms)
function lawTrack(plan, s, t, tp, xc, F) {
  const k = Math.round((t - tp) / 0.01); let v = plan.u[k];
  for (let i = 0; i < 6; i++) v -= plan.K[6 * k + i] * (s[i] - (i === 0 ? xc : 0) - plan.nom[6 * k + i]);
  return sat(v, F);
}
// the energy of cart and rods, (5) and (7)
function energy(d, f, s) { const [x, a, b, v, p, q] = s; return 0.5 * (d[0] * v * v + d[3] * p * p + d[5] * q * q) + d[1] * Math.cos(a) * v * p + d[2] * Math.cos(b) * v * q + d[4] * Math.cos(a - b) * p * q + f[0] * Math.cos(a) + f[1] * Math.cos(b); }
module.exports = { accel, rhs, rk4, wrap, refAt, sat, lawBalance, lawCalm, lawTrack, forceFor, energy };
