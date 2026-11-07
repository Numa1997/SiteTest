// An independent reference for the project 05 page (Balancing Two Rods on a Cart), written from the lecture note,
// not copied from the page's code: rows (8a), (8), (8b) of the equations of motion, solved by Cramer's rule;
// RK4 as in (18); the reference equilibria (25)-(26); the three laws of the supervisor (16), (21), (24).
// Everything takes the machine as d = (d1..d6) and f = (f1, f2) of (6)-(7), read from the page's store.
'use strict';
const TAU = 2 * Math.PI;

// section 13: the flows (13.3) and the fluid's generalised forces (35) with f of (33)-(34), written again from the note.
// Gauss-Legendre with 8 points from the published table (Abramowitz & Stegun, 25.4.30), not from the page's Newton iteration.
const GZ = [0.1834346424956498, 0.5255324099163290, 0.7966664774136267, 0.9602898564975363], GW = [0.3626837833783620, 0.3137066458778873, 0.2223810344533745, 0.1012285362903763];
const NODES = []; for (let k = 0; k < 4; k++) { NODES.push([(1 - GZ[k]) / 2, GW[k] / 2]); NODES.push([(1 + GZ[k]) / 2, GW[k] / 2]); }
const RODN = []; for (let p = 0; p < 3; p++) for (const [x, w] of NODES) RODN.push([(p + x) / 3, w / 3]);   // along a rod: 3 panels of 8 points
const YF = -3.3, YS = 3.4, CH = 0.12, RR = 0.01;   // CH: project 05's cart height; a page with another cart passes fl.CH
// stream functions of the deep and slow flows (13.3), written from the formulas of the note, not from the page's velocities
const PSI = {
  internal: (X, Y, t, U) => { const k = 2 * Math.PI / 12, m = 2 * Math.PI / 4, w = 2 * Math.PI / 45; return U / m * Math.cos(k * X - w * t) * Math.sin(m * Y); },
  gyre: (X, Y, t, U) => { const ep = 0.25 * Math.sin(2 * Math.PI * t / 15), xp = (X + 3) / 3, yp = (Y + 1.5) / 3; return 3 * U / Math.PI * Math.sin(Math.PI * (ep * xp * xp + (1 - 2 * ep) * xp)) * Math.sin(Math.PI * yp); },
  deepsea: (X, Y, t, U) => [[8, 10, 23, 0.3], [5, 75, 31, 2.1], [3.5, 140, 41, 4.0], [6, 200, 53, 1.2], [2.5, 260, 67, 5.3], [4, 320, 89, 3.7]].reduce((s, [l, d, T, ph]) => { const k = 2 * Math.PI / l, a = d * Math.PI / 180; return s + U / Math.sqrt(6) / k * Math.sin(k * Math.cos(a) * X + k * Math.sin(a) * Y - 2 * Math.PI / T * t + ph); }, 0),
  tides: (X, Y, t, U) => { const k = 2 * Math.PI / 30; return U / 2 * Y * (Math.cos(k * X - 2 * Math.PI / 20 * t) + Math.cos(k * X - 2 * Math.PI / 22 * t + 1)); },
};
function flow(k, X, Y, t, U, nu) {
  const T = 2 * Math.PI;
  if (PSI[k]) { const e = 1e-5, p = PSI[k]; return [(p(X, Y + e, t, U) - p(X, Y - e, t, U)) / (2 * e), -(p(X + e, Y, t, U) - p(X - e, Y, t, U)) / (2 * e)]; }   // the deep and slow flows: u = ∂ψ/∂y, v = −∂ψ/∂x of their stream functions, numerically
  if (k === 'breeze') return [U, 0];
  if (k === 'gusts') return [U * (1 + 0.5 * Math.sin(T * 0.13 * t) + 0.3 * Math.sin(T * 0.37 * t + 1) + 0.2 * Math.sin(T * 0.71 * t + 2)), 0];
  if (k === 'ground') { const z = Y - YF; return [z > 0.03 ? U * Math.log(z / 0.03) / Math.log(3.3 / 0.03) : 0, 0]; }
  if (k === 'lorry') { const tau = t - 12 * Math.floor(t / 12); return [U * (Math.exp(-(((tau - 2) / 0.45) ** 2)) - 0.35 * Math.exp(-(((tau - 3.1) / 0.6) ** 2))), 0]; }
  if (k === 'fan') { const al = 6 ** (2 / 3) / 0.35, xp = Math.max(0.5, X + 6), nj = U * 6 ** (1 / 3) / (6 * al * al), e = al * (Y - 0.6) / xp ** (2 / 3), sh = 1 / Math.cosh(e) ** 2;   // Bickley: psi = 6 nu a x^(1/3) tanh(a y / x^(2/3))
    return [6 * nj * al * al * xp ** (-1 / 3) * sh, 2 * nj * al * xp ** (-2 / 3) * (2 * e * sh - Math.tanh(e))]; }
  if (k === 'eddy') { const c = 0.4 * U, tb = t - 20 * Math.floor(t / 20), xc = -6 + c * tb, rc2 = 0.45 * 0.45 + 4 * nu * tb, dx = X - xc, dy = Y - 0.6, r2 = dx * dx + dy * dy, G2pi = 0.45 * U / 0.6381726863389515;
    const g = r2 > 1e-12 ? G2pi * (1 - Math.exp(-r2 / rc2)) / r2 : G2pi / rc2; return [c - g * dy, g * dx]; }
  if (k === 'river') { const z = Y - YF; return [z > 0 ? U * (z / (YS - YF)) ** (1 / 7) : 0, 0]; }
  if (k === 'waves') { const h = YS - YF, kw = T / 20, om = Math.sqrt(9.81 * kw * Math.tanh(kw * h)), a = U * Math.tanh(kw * h) / om, z = Y - YF, ph = kw * X - om * t;   // Airy, bed at the floor
    return [a * om * Math.cosh(kw * z) / Math.sinh(kw * h) * Math.cos(ph), a * om * Math.sinh(kw * z) / Math.sinh(kw * h) * Math.sin(ph)]; }
  if (k === 'shear') return [U * Y, 0];
  if (k === 'jets') return [U * X, -U * Y];
  if (k === 'cells') { const A = U * Math.exp(-2 * nu * Math.PI * Math.PI * t); return [A * Math.sin(Math.PI * X) * Math.cos(Math.PI * Y), -A * Math.cos(Math.PI * X) * Math.sin(Math.PI * Y)]; }
  if (k === 'street') { const l = 1.6, h = 0.281 * l, G = 0.4 * U * l / Math.tanh(Math.PI * h / l), x0 = 0.8 * U * t;
    const vrow = (xr, yr, Gm) => { const e = T * (Y - yr) / l, z = T * (X - xr) / l, D = Math.cosh(e) - Math.cos(z) + 0.35 * 0.35; return [-Gm * Math.sinh(e) / (2 * l * D), Gm * Math.sin(z) / (2 * l * D)]; };
    const a = vrow(x0 + l / 2, 0.6 + h / 2, -G), b = vrow(x0, 0.6 - h / 2, G); return [U + a[0] + b[0], a[1] + b[1]]; }
  return [0, 0];
}
// (39): the flow's acceleration Dv/Dt = dv/dt + (v.grad)v, by central differences of step 1e-4 (written apart from the page's accelF)
function flowAcc(fl, X, Y, t) { const h = 1e-4, f = (dx, dy, dt) => flow(fl.flow, X + dx, Y + dy, t + dt, fl.U, fl.nu), v = f(0, 0, 0);
  const dT = [0, 1].map((k) => (f(0, 0, h)[k] - f(0, 0, -h)[k]) / (2 * h)), dX = [0, 1].map((k) => (f(h, 0, 0)[k] - f(-h, 0, 0)[k]) / (2 * h)), dY = [0, 1].map((k) => (f(0, h, 0)[k] - f(0, -h, 0)[k]) / (2 * h));
  return [0, 1].map((k) => dT[k] + v[0] * dX[k] + v[1] * dY[k]); }
// (38): the added mass of the rods and the cart, M_a(a, b), and its derivatives along a and b; the velocity terms by Christoffel symbols
function addedM(ma, L1, L2, a, b) { const m = ma.mu, c1 = Math.cos(a), c2 = Math.cos(b), s1 = Math.sin(a), s2 = Math.sin(b), c12 = Math.cos(a - b), s12 = Math.sin(a - b);
  const M = [[m * (L1 * c1 * c1 + L2 * c2 * c2) + ma.mc, m * L1 * (L1 * c1 / 2 + L2 * c2 * c12), m * L2 * L2 * c2 / 2], [0, m * L1 * L1 * (L1 / 3 + L2 * c12 * c12), m * L1 * L2 * L2 * c12 / 2], [0, 0, m * L2 * L2 * L2 / 3]];
  const Ma = [[-2 * m * L1 * c1 * s1, m * L1 * (-L1 * s1 / 2 - L2 * c2 * s12), 0], [0, -2 * m * L1 * L1 * L2 * c12 * s12, -m * L1 * L2 * L2 * s12 / 2], [0, 0, 0]];   // d/da
  const Mb = [[-2 * m * L2 * c2 * s2, m * L1 * L2 * (-s2 * c12 + c2 * s12), -m * L2 * L2 * s2 / 2], [0, 2 * m * L1 * L1 * L2 * c12 * s12, m * L1 * L2 * L2 * s12 / 2], [0, 0, 0]];  // d/db
  for (const X of [M, Ma, Mb]) { X[1][0] = X[0][1]; X[2][0] = X[0][2]; X[2][1] = X[1][2]; } return { M, dM: [null, Ma, Mb] }; }
function christoffel(dM, qd) { const C = [0, 0, 0];   // C_i = sum_jk (d_k M_ij - 1/2 d_i M_jk) qd_j qd_k, with d_x M = 0
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) for (let k = 0; k < 3; k++) C[i] += ((dM[k] ? dM[k][i][j] : 0) - 0.5 * (dM[i] ? dM[i][j][k] : 0)) * qd[j] * qd[k]; return C; }
function fluidQ(fl, s, t) {   // rods as lines from the hinge; f = -xi_perp w_n n - (xi_perp/2) w_t t - c_q |w_n| w_n n; the cart: -c_lin w - c_quad |w| w on its face
  const [x, a, b, xd, ad, bd] = s, Q = [0, 0, 0];
  for (let k = 0; k < 2; k++) { const L = k ? fl.L2 : fl.L1, th = k ? b : a, om = k ? bd : ad, t1 = [Math.sin(th), Math.cos(th)], n1 = [Math.cos(th), -Math.sin(th)];
    const bx = k ? x + fl.L1 * Math.sin(a) : x, by = k ? fl.L1 * Math.cos(a) : 0, bvx = k ? xd + fl.L1 * Math.cos(a) * ad : xd, bvy = k ? -fl.L1 * Math.sin(a) * ad : 0;
    for (const [xn, wn] of RODN) { const sg = xn * L, P = [bx + sg * t1[0], by + sg * t1[1]], V = [bvx + sg * om * n1[0], bvy + sg * om * n1[1]], F = flow(fl.flow, P[0], P[1], t, fl.U, fl.nu);
      const w = [V[0] - F[0], V[1] - F[1]], wt = w[0] * t1[0] + w[1] * t1[1], wnn = w[0] * n1[0] + w[1] * n1[1];
      let fn = -fl.xi[k] * wnn - fl.cq * Math.abs(wnn) * wnn; if (fl.acc) { const A = flowAcc(fl, P[0], P[1], t); fn += fl.kr * (A[0] * n1[0] + A[1] * n1[1]); }
      const ft = -0.5 * fl.xi[k] * wt, fv = [ft * t1[0] + fn * n1[0], ft * t1[1] + fn * n1[1]], q = wn * L;
      Q[0] += q * fv[0]; if (k === 0) Q[1] += q * sg * fn; else { Q[1] += q * fl.L1 * (fv[0] * Math.cos(a) - fv[1] * Math.sin(a)); Q[2] += q * sg * fn; } } }
  let um = 0; for (const [xn, wn] of NODES) um += wn * flow(fl.flow, x, -(fl.CH || CH) * xn, t, fl.U, fl.nu)[0];
  const wc = xd - um; Q[0] += -fl.cl * wc - fl.cc * Math.abs(wc) * wc + (fl.acc ? fl.kc * flowAcc(fl, x, -(fl.CH || CH) / 2, t)[0] : 0); return Q;
}
// (8a), (8), (8b):  M q'' = r, with q = (x, th1, th2); with a medium, Q of (35) on the right
function accel(d, f, s, u, t, fl) {
  const [x, a, b, xd, ad, bd] = s, c1 = Math.cos(a), c2 = Math.cos(b), s1 = Math.sin(a), s2 = Math.sin(b), c12 = Math.cos(a - b), s12 = Math.sin(a - b);
  const M = [[d[0], d[1] * c1, d[2] * c2], [d[1] * c1, d[3], d[4] * c12], [d[2] * c2, d[4] * c12, d[5]]];
  const r = [u + d[1] * s1 * ad * ad + d[2] * s2 * bd * bd,      // (8a): d1 x'' + d2 c1 th1'' + d3 c2 th2'' - d2 s1 th1'^2 - d3 s2 th2'^2 = u
             f[0] * s1 - d[4] * s12 * bd * bd,                    // (8):  d2 c1 x'' + d4 th1'' + d5 c12 th2'' + d5 s12 th2'^2 - f1 s1 = 0
             f[1] * s2 + d[4] * s12 * ad * ad];                   // (8b): d3 c2 x'' + d5 c12 th1'' + d6 th2'' - d5 s12 th1'^2 - f2 s2 = 0
  if (fl) { const Q = fluidQ(fl, s, t); r[0] += Q[0]; r[1] += Q[1]; r[2] += Q[2];
    if (fl.ma) { const A = addedM(fl.ma, fl.L1, fl.L2, a, b), C = christoffel(A.dM, [xd, ad, bd]); for (let i = 0; i < 3; i++) { r[i] -= C[i]; for (let j = 0; j < 3; j++) M[i][j] += A.M[i][j]; } } }
  const det3 = (A) => A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]);
  const D = det3(M), col = (k) => M.map((row, i) => row.map((v, j) => (j === k ? r[i] : v)));
  return [det3(col(0)) / D, det3(col(1)) / D, det3(col(2)) / D];
}
function rhs(d, f, s, u, t, fl) { const q = accel(d, f, s, u, t, fl); return [s[3], s[4], s[5], q[0], q[1], q[2]]; }
function rk4(d, f, s, u, h, t, fl) {   // (18), the flow taken at t, t + h/2, t + h/2, t + h
  const k1 = rhs(d, f, s, u, t, fl), k2 = rhs(d, f, s.map((v, i) => v + h / 2 * k1[i]), u, t + h / 2, fl), k3 = rhs(d, f, s.map((v, i) => v + h / 2 * k2[i]), u, t + h / 2, fl), k4 = rhs(d, f, s.map((v, i) => v + h * k3[i]), u, t + h, fl);
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
function forceFor(d, f, s, a, t, fl) {   // with a medium, its added mass (38)-(40) and, when a flow is given, Q of (35) join rows (8), (8b) and (8a)
  const [x, t1, t2, xd, w1, w2] = s, c1 = Math.cos(t1), c2 = Math.cos(t2), s1 = Math.sin(t1), s2 = Math.sin(t2), c12 = Math.cos(t1 - t2), s12 = Math.sin(t1 - t2);
  const M = [[d[0], d[1] * c1, d[2] * c2], [d[1] * c1, d[3], d[4] * c12], [d[2] * c2, d[4] * c12, d[5]]], Q = fl && fl.flow ? fluidQ(fl, s, t) : [0, 0, 0];
  let C = [0, 0, 0]; if (fl && fl.ma) { const A = addedM(fl.ma, fl.L1, fl.L2, t1, t2); C = christoffel(A.dM, [xd, w1, w2]); for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) M[i][j] += A.M[i][j]; }
  const b1 = f[0] * s1 - d[4] * s12 * w2 * w2 - M[1][0] * a + Q[1] - C[1], b2 = f[1] * s2 + d[4] * s12 * w1 * w1 - M[2][0] * a + Q[2] - C[2];
  const det = M[1][1] * M[2][2] - M[1][2] * M[2][1], q1 = (b1 * M[2][2] - M[1][2] * b2) / det, q2 = (M[1][1] * b2 - M[2][1] * b1) / det;
  return M[0][0] * a + M[0][1] * q1 + M[0][2] * q2 - d[1] * s1 * w1 * w1 - d[2] * s2 * w2 * w2 + C[0] - Q[0];
}
function lawCalm(d, f, s, xc, kc, F, ma) { const P = d[1] * Math.cos(s[1]) * s[4] + d[2] * Math.cos(s[2]) * s[5], a = Math.max(-8, Math.min(8, kc * P - 4 * (s[0] - xc) - 4 * s[3])); return sat(forceFor(d, f, s, a, 0, ma), F); }   // ma: the medium's added mass, known to the controller (not the flow)
// (24): u = sat(u_plan[k] - K_k (s - x_c e1 - s_plan[k])), k = round((t - t_plan) / 10 ms)
function lawTrack(plan, s, t, tp, xc, F) {
  const k = Math.round((t - tp) / 0.01); let v = plan.u[k];
  for (let i = 0; i < 6; i++) v -= plan.K[6 * k + i] * (s[i] - (i === 0 ? xc : 0) - plan.nom[6 * k + i]);
  return sat(v, F);
}
// the energy of cart and rods, (5) and (7)
function energy(d, f, s) { const [x, a, b, v, p, q] = s; return 0.5 * (d[0] * v * v + d[3] * p * p + d[5] * q * q) + d[1] * Math.cos(a) * v * p + d[2] * Math.cos(b) * v * q + d[4] * Math.cos(a - b) * p * q + f[0] * Math.cos(a) + f[1] * Math.cos(b); }
module.exports = { flow, fluidQ, accel, rhs, rk4, wrap, refAt, sat, lawBalance, lawCalm, lawTrack, forceFor, energy };
