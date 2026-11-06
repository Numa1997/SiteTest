/* Two-way coupled fluid for project 05 (double inverted pendulum on a cart), CPU only, browser and Node.
 *
 * The world: the machine stands in a tank of depth b (into the screen) equal to the cart's depth, 0.2 m; the fluid moves in the
 * plane of the screen, the same in every slice of the depth (a 2D velocity field, per metre of depth times b).
 * - The cart (0.36 x 0.12 m, filling the depth) is a resolved body on the grid. Pressure coupling after Batty, Bertails & Bridson
 *   2007 (ACM TOG 26(3) 100): fluid fraction of every face, the cart's velocity enters the divergence where the face is solid,
 *   the pressure force on the cart is -sum vol grad p; the pressure is linear in the cart's velocity (p = p0 + xdot' p_x), so the
 *   cart's added mass is implicit (stable for a cart lighter than the fluid it displaces). Viscous shear on its faces is booked.
 * - Each rod (2 cm thick, 1/10 of the depth) is an actuator line: Gauss points along it read the grid velocity there (Peskin's
 *   4-point kernel), the force per metre of rod follows from the page's law (33)-(34) (resistive-force theory + pressure drag) plus
 *   Morison's inertia term (39) with the fluid's acceleration from the grid, and the opposite impulse is spread back into the grid
 *   with the same kernel. Interpolation and spreading are adjoint, so the power the fluid gives the rod and the power the rod gives
 *   the fluid differ by exactly f.w (the drag's dissipation below the grid).
 * - The machine is integrated with the page's RK4 at h (1 ms) inside each fluid step; the rods' impulses are summed with RK4's
 *   weights, so the momentum the rods lose is the momentum the fluid gains, to round-off. That impulse is spread into the fluid at
 *   the start of the next fluid step (one step in transit, booked).
 * Units SI. Fields per metre of depth; forces on the fluid divided by b.
 */
(function (root, factory) { if (typeof module === 'object' && module.exports) module.exports = factory(); else root.TwoWay = factory(); })(typeof globalThis !== "undefined" ? globalThis : this, function () {
'use strict';

function fracInside(a, b) { if (a < 0 && b < 0) return 1; if (a >= 0 && b >= 0) return 0; return a < 0 ? a / (a - b) : b / (b - a); }
function phi4(r) { r = Math.abs(r); if (r < 1) return (3 - 2 * r + Math.sqrt(1 + 4 * r - 4 * r * r)) / 8; if (r < 2) return (5 - 2 * r - Math.sqrt(-7 + 12 * r - 4 * r * r)) / 8; return 0; }   // Peskin 2002, Acta Numerica 11, eq. (6.27)

/* ---------- multigrid-preconditioned CG for sum_f w_f (p_c - p_nb)/h^2 = r (from mac/mac.cjs, tested there) ---------- */
function Poisson(nx, ny, h) {
  this.L = []; var n = nx, m = ny, hh = h;
  for (;;) { this.L.push({ nx: n, ny: m, h: hh, wx: new Float64Array((n + 1) * m), wy: new Float64Array(n * (m + 1)), d: new Float64Array(n * m), x: new Float64Array(n * m), b: new Float64Array(n * m), r: new Float64Array(n * m),
      cw: new Float64Array(n * m), ce: new Float64Array(n * m), cs: new Float64Array(n * m), cn: new Float64Array(n * m), id: new Float64Array(n * m) });
    if (n % 2 || m % 2 || n <= 8 || m <= 8) break; n /= 2; m /= 2; hh *= 2; }
  var N = nx * ny; this.rr = new Float64Array(N); this.z = new Float64Array(N); this.pp = new Float64Array(N); this.Ap = new Float64Array(N); this.tol = 1e-4;
}
Poisson.prototype.setWeights = function (wx, wy) {
  var L0 = this.L[0], l, I, J; L0.wx.set(wx); L0.wy.set(wy);
  for (l = 1; l < this.L.length; l++) { var F = this.L[l - 1], C = this.L[l];
    for (J = 0; J < C.ny; J++) for (I = 0; I <= C.nx; I++) C.wx[J * (C.nx + 1) + I] = 0.5 * (F.wx[(2 * J) * (F.nx + 1) + 2 * I] + F.wx[(2 * J + 1) * (F.nx + 1) + 2 * I]);
    for (J = 0; J <= C.ny; J++) for (I = 0; I < C.nx; I++) C.wy[J * C.nx + I] = 0.5 * (F.wy[(2 * J) * F.nx + 2 * I] + F.wy[(2 * J) * F.nx + 2 * I + 1]); }
  for (l = 0; l < this.L.length; l++) { var Lv = this.L[l], nx = Lv.nx, ny = Lv.ny, ih = 1 / (Lv.h * Lv.h), i, j;
    for (j = 0; j < ny; j++) for (i = 0; i < nx; i++) { var c = j * nx + i;
      Lv.d[c] = (Lv.wx[j * (nx + 1) + i] + Lv.wx[j * (nx + 1) + i + 1] + Lv.wy[j * nx + i] + Lv.wy[(j + 1) * nx + i]) * ih;
      Lv.cw[c] = i > 0 ? Lv.wx[j * (nx + 1) + i] * ih : 0; Lv.ce[c] = i < nx - 1 ? Lv.wx[j * (nx + 1) + i + 1] * ih : 0;
      Lv.cs[c] = j > 0 ? Lv.wy[j * nx + i] * ih : 0; Lv.cn[c] = j < ny - 1 ? Lv.wy[(j + 1) * nx + i] * ih : 0; Lv.id[c] = Lv.d[c] > 0 ? 1 / Lv.d[c] : 0; } }
};
Poisson.prototype.apply = function (Lv, x, out) { var nx = Lv.nx, ny = Lv.ny, d = Lv.d, cw = Lv.cw, ce = Lv.ce, cs = Lv.cs, cn = Lv.cn, i, j, c, s;
  for (j = 0; j < ny; j++) for (i = 0; i < nx; i++) { c = j * nx + i;
    if (j === 0 || j === ny - 1 || i === 0 || i === nx - 1) { s = d[c] * x[c]; if (cw[c]) s -= cw[c] * x[c - 1]; if (ce[c]) s -= ce[c] * x[c + 1]; if (cs[c]) s -= cs[c] * x[c - nx]; if (cn[c]) s -= cn[c] * x[c + nx]; out[c] = s; }
    else out[c] = d[c] * x[c] - cw[c] * x[c - 1] - ce[c] * x[c + 1] - cs[c] * x[c - nx] - cn[c] * x[c + nx]; } };
Poisson.prototype.smooth = function (Lv, x, b, sweeps, order) {   // red-black Gauss–Seidel; the interior without branches, the edge cells with them
  var nx = Lv.nx, ny = Lv.ny, cw = Lv.cw, ce = Lv.ce, cs = Lv.cs, cn = Lv.cn, id = Lv.id, i, j, c, s2;
  for (var s = 0; s < sweeps; s++) for (var pass = 0; pass < 2; pass++) { var col = (pass + order) & 1;
    for (j = 0; j < ny; j++) { var row = j * nx, edgeRow = j === 0 || j === ny - 1;
      for (i = (j + col) & 1; i < nx; i += 2) { c = row + i;
        if (edgeRow || i === 0 || i === nx - 1) { if (!id[c]) { x[c] = 0; continue; } s2 = b[c]; if (cw[c]) s2 += cw[c] * x[c - 1]; if (ce[c]) s2 += ce[c] * x[c + 1]; if (cs[c]) s2 += cs[c] * x[c - nx]; if (cn[c]) s2 += cn[c] * x[c + nx]; x[c] = s2 * id[c]; }
        else x[c] = (b[c] + cw[c] * x[c - 1] + ce[c] * x[c + 1] + cs[c] * x[c - nx] + cn[c] * x[c + nx]) * id[c]; } } } };
Poisson.prototype.vcycle = function (l) { var Lv = this.L[l], c;
  if (l === this.L.length - 1) { Lv.x.fill(0); this.smooth(Lv, Lv.x, Lv.b, 40, 0); this.smooth(Lv, Lv.x, Lv.b, 40, 1); return; }
  Lv.x.fill(0); this.smooth(Lv, Lv.x, Lv.b, 2, 0); this.apply(Lv, Lv.x, Lv.r); for (c = 0; c < Lv.r.length; c++) Lv.r[c] = Lv.b[c] - Lv.r[c];
  var C = this.L[l + 1], I, J;
  for (J = 0; J < C.ny; J++) for (I = 0; I < C.nx; I++) { var f = 2 * J * Lv.nx + 2 * I; C.b[J * C.nx + I] = 0.25 * (Lv.r[f] + Lv.r[f + 1] + Lv.r[f + Lv.nx] + Lv.r[f + Lv.nx + 1]); }
  this.vcycle(l + 1);
  for (J = 0; J < C.ny; J++) for (I = 0; I < C.nx; I++) { var f2 = 2 * J * Lv.nx + 2 * I, e = C.x[J * C.nx + I]; Lv.x[f2] += e; Lv.x[f2 + 1] += e; Lv.x[f2 + Lv.nx] += e; Lv.x[f2 + Lv.nx + 1] += e; }
  this.smooth(Lv, Lv.x, Lv.b, 2, 1); };
Poisson.prototype.solve = function (b, x, maxit) {   // x: warm start; returns iterations; relative residual this.tol
  maxit = maxit || 200; var L0 = this.L[0], N = b.length, rr = this.rr, z = this.z, pp = this.pp, Ap = this.Ap, c;
  this.apply(L0, x, Ap); var bn = 0; for (c = 0; c < N; c++) { rr[c] = L0.d[c] ? b[c] - Ap[c] : 0; bn += b[c] * b[c]; }
  bn = Math.sqrt(bn); if (!bn) { x.fill(0); return 0; }
  L0.b.set(rr); this.vcycle(0); z.set(L0.x); pp.set(z); var rz = 0; for (c = 0; c < N; c++) rz += rr[c] * z[c];
  for (var it = 0; it < maxit; it++) {
    var rn = 0; for (c = 0; c < N; c++) rn += rr[c] * rr[c]; if (Math.sqrt(rn) < this.tol * bn) return it;
    this.apply(L0, pp, Ap); var pAp = 0; for (c = 0; c < N; c++) pAp += pp[c] * Ap[c]; var a = rz / pAp;
    for (c = 0; c < N; c++) { x[c] += a * pp[c]; rr[c] -= a * Ap[c]; }
    L0.b.set(rr); this.vcycle(0); z.set(L0.x); var rz2 = 0; for (c = 0; c < N; c++) rz2 += rr[c] * z[c]; var bb = rz2 / rz; rz = rz2;
    for (c = 0; c < N; c++) pp[c] = z[c] + bb * pp[c]; }
  return maxit; };

/* ---------- the machine: the page's model (5)-(9), with the medium's buoyancy (37) and the rods' added mass (38), (40) ---------- */
var MEDIA = { air: { rho: 1.184, mu: 1.85e-5 }, water: { rho: 998.2, mu: 1.0016e-3 }, glycerol: { rho: 1261, mu: 1.412 }, honey: { rho: 1420, mu: 7 } };   // the page's table 13.1
var ROD_R = 0.01, CD_ROD = 1.2, CA_ROD = 1, G = 9.81, CART_W = 0.36, CART_H = 0.12, CART_B = 0.2;
var GLN = (function (n) { var x = [], w = [], i, j, it; for (i = 1; i <= n; i++) { var z = Math.cos(Math.PI * (i - 0.25) / (n + 0.5)), pp = 1;
    for (it = 0; it < 100; it++) { var p1 = 1, p2 = 0; for (j = 1; j <= n; j++) { var p3 = p2; p2 = p1; p1 = ((2 * j - 1) * z * p2 - (j - 1) * p3) / j; } pp = n * (z * p1 - p2) / (z * z - 1); var z1 = z; z = z1 - p1 / pp; if (Math.abs(z - z1) < 1e-16) break; }
    x.push((1 - z) / 2); w.push(1 / ((1 - z * z) * pp * pp)); } return { x: x, w: w }; })(8);
var GLR = { x: [], w: [] }; for (var gp = 0; gp < 3; gp++) for (var gi = 0; gi < 8; gi++) { GLR.x.push((gp + GLN.x[gi]) / 3); GLR.w.push(GLN.w[gi] / 3); }   // the page's 3 panels of 8 Gauss points

function machinePar(o) {   // o: m0, m1, m2, L1, L2, medium
  var m0 = o.m0, m1 = o.m1, m2 = o.m2, L1 = o.L1, L2 = o.L2, md = MEDIA[o.medium], rho = md ? md.rho : 0, mu = md ? md.mu : 0, bA = rho * Math.PI * ROD_R * ROD_R * G;
  return { m0: m0, m1: m1, m2: m2, L1: L1, L2: L2, rho: rho, mu: mu,
    d: [m0 + m1 + m2, (m1 / 2 + m2) * L1, m2 * L2 / 2, (m1 / 3 + m2) * L1 * L1, m2 * L1 * L2 / 2, m2 * L2 * L2 / 3],
    f: [(m1 / 2 + m2) * L1 * G - bA * (L1 * L1 / 2 + L1 * L2), m2 * L2 * G / 2 - bA * L2 * L2 / 2],
    mua: CA_ROD * rho * Math.PI * ROD_R * ROD_R,   // added mass per metre of rod, across it (38)
    xi: [L1, L2].map(function (L) { return 4 * Math.PI * mu / Math.log(L / ROD_R); }), cq: 0.5 * rho * CD_ROD * 2 * ROD_R, kr: (1 + CA_ROD) * rho * Math.PI * ROD_R * ROD_R };
}
function Dmat(p, a, b) { var d = p.d, c1 = Math.cos(a), c2 = Math.cos(b), c12 = Math.cos(a - b), m = p.mua, L1 = p.L1, L2 = p.L2;
  var M = [[d[0], d[1] * c1, d[2] * c2], [d[1] * c1, d[3], d[4] * c12], [d[2] * c2, d[4] * c12, d[5]]];
  if (m) { M[0][0] += m * (L1 * c1 * c1 + L2 * c2 * c2); M[0][1] += m * L1 * (L1 * c1 / 2 + L2 * c2 * c12); M[0][2] += m * L2 * L2 * c2 / 2;
    M[1][1] += m * L1 * L1 * (L1 / 3 + L2 * c12 * c12); M[1][2] += m * L1 * L2 * L2 * c12 / 2; M[2][2] += m * L2 * L2 * L2 / 3; M[1][0] = M[0][1]; M[2][0] = M[0][2]; M[2][1] = M[1][2]; }
  return M; }
function Cvec(p, s) { var d = p.d, a = s[1], b = s[2], xd = s[3], ad = s[4], bd = s[5], sab = Math.sin(a - b), m = p.mua, L1 = p.L1, L2 = p.L2;
  var C = [-d[1] * Math.sin(a) * ad * ad - d[2] * Math.sin(b) * bd * bd, d[4] * sab * bd * bd, -d[4] * sab * ad * ad];
  if (m) { C[0] += (-ad * ad * L1 * (L1 + L2) * m * Math.sin(a) - 2 * ad * L1 * m * xd * Math.sin(2 * a) - L2 * m * (ad * (ad - 2 * bd) * L1 * Math.sin(a - 2 * b) + bd * (bd * L2 + 4 * xd * Math.cos(b)) * Math.sin(b))) / 2;
    C[1] += L1 * m * (xd * xd * Math.sin(2 * a) + L2 * (2 * bd * xd * Math.sin(a - 2 * b) + (bd * bd * L2 - 2 * ad * (ad - 2 * bd) * L1 * Math.cos(a - b)) * Math.sin(a - b))) / 2;
    C[2] += -L2 * m * (2 * ad * L1 * xd * Math.sin(a - 2 * b) + ad * ad * L1 * L2 * Math.sin(a - b) + ad * ad * L1 * L1 * Math.sin(2 * (a - b)) - xd * xd * Math.sin(2 * b)) / 2; }
  return C; }
function energy(p, s) { var M = Dmat(p, s[1], s[2]), v = [s[3], s[4], s[5]], T = 0; for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) T += 0.5 * v[i] * M[i][j] * v[j]; return T + p.f[0] * Math.cos(s[1]) + p.f[1] * Math.cos(s[2]); }
function momX(p, s) { var M = Dmat(p, s[1], s[2]); return M[0][0] * s[3] + M[0][1] * s[4] + M[0][2] * s[5]; }   // ∂T/∂ẋ: the x-momentum of cart, rods and the water the rods carry
function solve3(M, r) { var A = M.map(function (row, i) { return row.concat([r[i]]); }), i, j, k;
  for (i = 0; i < 3; i++) { var piv = i; for (j = i + 1; j < 3; j++) if (Math.abs(A[j][i]) > Math.abs(A[piv][i])) piv = j; var t = A[i]; A[i] = A[piv]; A[piv] = t;
    for (j = i + 1; j < 3; j++) { var f = A[j][i] / A[i][i]; for (k = i; k < 4; k++) A[j][k] -= f * A[i][k]; } }
  var x = [0, 0, 0]; for (i = 2; i >= 0; i--) { var s = A[i][3]; for (j = i + 1; j < 3; j++) s -= A[i][j] * x[j]; x[i] = s / A[i][i]; } return x; }

/* rod points: k = 0 lower rod, 1 upper rod; GLR.x.length points each. Position, velocity, and Jacobian columns d r/d q_i */
var NP = GLR.x.length;
function pointKin(p, s, k, i, out) { var L = k ? p.L2 : p.L1, sg = GLR.x[i] * L, s1 = Math.sin(s[1]), c1 = Math.cos(s[1]), s2 = Math.sin(s[2]), c2 = Math.cos(s[2]), sn = k ? s2 : s1, cs = k ? c2 : c1;
  out.X = s[0] + (k ? p.L1 * s1 : 0) + sg * sn; out.Y = (k ? p.L1 * c1 : 0) + sg * cs;
  out.vx = s[3] + (k ? p.L1 * c1 * s[4] : 0) + sg * cs * (k ? s[5] : s[4]); out.vy = -(k ? p.L1 * s1 * s[4] : 0) - sg * sn * (k ? s[5] : s[4]);
  out.sn = sn; out.cs = cs; out.sg = sg; out.wq = GLR.w[i] * L; out.c1 = c1; out.s1 = s1; return out; }

/* ---------- the world ---------- */
function World(o) {
  var self = this; o = o || {};
  this.dx = o.dx || 0.025; this.x0 = o.x0 !== undefined ? o.x0 : -2; this.y0 = o.y0 !== undefined ? o.y0 : -0.8;
  this.nx = o.nx || Math.round(4 / this.dx); this.ny = o.ny || Math.round(2.4 / this.dx);
  this.b = CART_B; this.U = o.U || 0; this.h = o.h || 0.001; this.nsub = o.nsub || 5;
  this.mp = machinePar(o.machine); this.rho = o.rho || this.mp.rho; this.nu = (o.mu || this.mp.mu) / Math.max(this.rho, 1e-30);
  var nx = this.nx, ny = this.ny, NU = (nx + 1) * ny, NV = nx * (ny + 1), N = nx * ny;
  this.u = new Float64Array(NU); this.v = new Float64Array(NV); this.u.fill(this.U);
  this.wu = new Float64Array(NU); this.wv = new Float64Array(NV); this.su = new Uint8Array(NU); this.sv = new Uint8Array(NV);   // fluid fraction; 1 where the face is inside the cart
  this.nearU = new Uint8Array(NU);   // faces next to the cart whose staggered cell is partly or wholly solid: they carry the cart's velocity in the divergence
  this.phi = new Float64Array(N); this.phU = new Float64Array(NU); this.phV = new Float64Array(NV); /* signed distance to the body at every face centre, negative inside */ this.P = new Poisson(nx, ny, this.dx); this.p0 = new Float64Array(N); this.px = new Float64Array(N); this.rhs = new Float64Array(N); this.pF = new Float64Array(N);
  this.s = (o.s || [0, 0, 0, 0, 0, 0]).slice(); this.t = 0; this.u_m = 0;
  this.uS = new Float64Array(2 * NP * 2); this.uS1 = new Float64Array(2 * NP * 2); this.aS = new Float64Array(2 * NP * 2); this.pos = new Float64Array(2 * NP * 2);   // sampled velocity now and a step ago, fluid acceleration, where each point stood
  this.imp = new Float64Array(2 * NP * 2); this.impPos = new Float64Array(2 * NP * 2); this.haveImp = false; this.first = true;   // the impulse in transit and where it is delivered
  this.book = { Wm: 0, Drod: 0, Wvisc: 0, Eadv: 0, Ediff: 0, Eproj: 0, Erod: 0, Ecart: 0, Pwall: 0, Pmotor: 0, Ptransit: 0 };
  this.tmpU = new Float64Array(NU); this.tmpV = new Float64Array(NV); this.u0 = new Float64Array(NU); this.v0 = new Float64Array(NV); this.uF = new Float64Array(NU); this.vF = new Float64Array(NV);
  this.kin = {}; this.measure();
}
var W = World.prototype;
W.xu = function (i) { return this.x0 + i * this.dx; }; W.yu = function (j) { return this.y0 + (j + 0.5) * this.dx; };
W.xv = function (i) { return this.x0 + (i + 0.5) * this.dx; }; W.yv = function (j) { return this.y0 + j * this.dx; };
W.cartSdf = function (X, Y) { if (this.cartGone) return 1; var qx = Math.abs(X - this.s[0]) - CART_W / 2, qy = Math.abs(Y + CART_H / 2) - CART_H / 2; return Math.hypot(Math.max(qx, 0), Math.max(qy, 0)) + Math.min(Math.max(qx, qy), 0); };
W.measureCircle = function (xc, yc, r) {   // tests only: a fixed circle, fractions by 8 × 8 supersampling of each control volume
  var nx = this.nx, ny = this.ny, dx = this.dx, i, j, c, a, b, n = 8;
  function frac(X, Y) { if (Math.hypot(X - xc, Y - yc) > r + dx) return 0; if (Math.hypot(X - xc, Y - yc) < r - dx) return 1; var k = 0; for (a = 0; a < n; a++) for (b = 0; b < n; b++) if (Math.hypot(X + (a + 0.5) / n * dx - dx / 2 - xc, Y + (b + 0.5) / n * dx - dx / 2 - yc) < r) k++; return k / (n * n); }
  for (j = 0; j < ny; j++) for (i = 0; i <= nx; i++) this.phU[j * (nx + 1) + i] = Math.hypot(this.xu(i) - xc, this.yu(j) - yc) - r;
  for (j = 0; j <= ny; j++) for (i = 0; i < nx; i++) this.phV[j * nx + i] = Math.hypot(this.xv(i) - xc, this.yv(j) - yc) - r;
  for (j = 0; j < ny; j++) for (i = 0; i <= nx; i++) { c = j * (nx + 1) + i; var f = frac(this.xu(i), this.yu(j)); this.wu[c] = 1 - f; this.su[c] = f > 0 ? 1 : 0; }
  for (j = 0; j <= ny; j++) for (i = 0; i < nx; i++) { c = j * nx + i; var f2 = frac(this.xv(i), this.yv(j)); this.wv[c] = 1 - f2; this.sv[c] = f2 > 0 ? 1 : 0; }
  this.finishWeights(); };
W.measure = function () {   // fluid fraction of the control volume (dx × dx) around every face: Batty's kinetic-energy weights; exact for the cart, an axis-aligned rectangle
  var nx = this.nx, ny = this.ny, dx = this.dx, i, j, c, x0 = this.x0, y0 = this.y0, xa = this.s[0] - CART_W / 2, xb = this.s[0] + CART_W / 2, ya = -CART_H, yb = 0, gone = this.cartGone, h = dx / 2, ia = 1 / (dx * dx);
  function ov(a, b, lo, hi) { var l = Math.min(b, hi) - Math.max(a, lo); return l > 0 ? l : 0; }
  for (j = 0; j < ny; j++) { var yc = y0 + (j + 0.5) * dx, oyu = gone ? 0 : ov(yc - h, yc + h, ya, yb);
    for (i = 0; i <= nx; i++) { c = j * (nx + 1) + i; var xf = x0 + i * dx, fs = oyu ? ov(xf - h, xf + h, xa, xb) * oyu * ia : 0; if (fs > 1 - 1e-12) fs = 1; this.wu[c] = 1 - fs; this.su[c] = fs > 0 ? 1 : 0; } }
  for (j = 0; j <= ny; j++) { var yf = y0 + j * dx, oyv = gone ? 0 : ov(yf - h, yf + h, ya, yb);
    for (i = 0; i < nx; i++) { c = j * nx + i; var xc = x0 + (i + 0.5) * dx, fs2 = oyv ? ov(xc - h, xc + h, xa, xb) * oyv * ia : 0; if (fs2 > 1 - 1e-12) fs2 = 1; this.wv[c] = 1 - fs2; this.sv[c] = fs2 > 0 ? 1 : 0; } }
  for (j = 0; j < ny; j++) for (i = 0; i <= nx; i++) this.phU[j * (nx + 1) + i] = this.cartSdf(x0 + i * dx, y0 + (j + 0.5) * dx);
  for (j = 0; j <= ny; j++) for (i = 0; i < nx; i++) this.phV[j * nx + i] = this.cartSdf(x0 + (i + 0.5) * dx, y0 + j * dx);
  this.finishWeights(); };
W.finishWeights = function () { var nx = this.nx, ny = this.ny, i, j;
  var wx = this.tmpU, wy = this.tmpV; wx.set(this.wu); wy.set(this.wv);
  for (j = 0; j < ny; j++) wx[j * (nx + 1)] = 0;   // left edge: given inflow (Neumann for p); right edge: open, p = 0 (Dirichlet, through the diagonal)
  for (i = 0; i < nx; i++) { wy[i] = 0; wy[ny * nx + i] = 0; }   // floor and lid: walls without friction
  this.wx = Float64Array.from(wx); this.wy = Float64Array.from(wy); this.P.setWeights(this.wx, this.wy);
};
W.impose = function (xd, strict) { var c, dP = 0; for (c = 0; c < this.u.length; c++) if (this.phU[c] < 0 && (!strict || this.wx[c] <= 0)) { dP += this.wu[c] * (xd - this.u[c]); this.u[c] = xd; } for (c = 0; c < this.v.length; c++) if (this.phV[c] < 0 && (!strict || this.wy[c] <= 0)) this.v[c] = 0;   // faces whose centre lies inside the body move with it
  this.impX = (this.impX || 0) + this.rho * this.b * this.dx * this.dx * dP; };   // the x-momentum the body gives the partly fluid faces it overrides (N s), credited to the body
W.boundary = function () { var nx = this.nx, ny = this.ny, Wu = nx + 1, j, i;
  for (j = 0; j < ny; j++) { this.u[j * Wu] = this.inflow ? this.inflow(this.yu(j)) : this.U; this.u[j * Wu + nx] = this.u[j * Wu + nx - 1]; }
  for (i = 0; i < nx; i++) { this.v[i] = 0; this.v[ny * nx + i] = 0; } };
W.KE = function () {   // ½ ρ b Σ w u² dx² over the faces: the fluid's kinetic energy (J)
  var s = 0, c; for (c = 0; c < this.u.length; c++) s += this.wu[c] * this.u[c] * this.u[c]; for (c = 0; c < this.v.length; c++) s += this.wv[c] * this.v[c] * this.v[c];
  return 0.5 * this.rho * this.b * this.dx * this.dx * s; };
W.momX = function () { var s = 0, c; for (c = 0; c < this.u.length; c++) s += this.wu[c] * this.u[c]; return this.rho * this.b * this.dx * this.dx * s; };

/* bilinear samplers on the staggered arrays, grid units */
W.sU = function (A, gx, gy) { var nx = this.nx, ny = this.ny, Wu = nx + 1; if (gx < 0) gx = 0; else if (gx > nx - 1e-9) gx = nx - 1e-9; if (gy < 0) gy = 0; else if (gy > ny - 1 - 1e-9) gy = ny - 1 - 1e-9;
  var i = gx | 0, j = gy | 0, a = gx - i, b = gy - j, c = j * Wu + i; return (1 - b) * ((1 - a) * A[c] + a * A[c + 1]) + b * ((1 - a) * A[c + Wu] + a * A[c + Wu + 1]); };
W.sV = function (A, gx, gy) { var nx = this.nx, ny = this.ny; if (gx < 0) gx = 0; else if (gx > nx - 1 - 1e-9) gx = nx - 1 - 1e-9; if (gy < 0) gy = 0; else if (gy > ny - 1e-9) gy = ny - 1e-9;
  var i = gx | 0, j = gy | 0, a = gx - i, b = gy - j, c = j * nx + i; return (1 - b) * ((1 - a) * A[c] + a * A[c + 1]) + b * ((1 - a) * A[c + nx] + a * A[c + nx + 1]); };
W.velAt = function (X, Y) { var gx = (X - this.x0) / this.dx, gy = (Y - this.y0) / this.dx; return [this.sU(this.u, gx, gy - 0.5), this.sV(this.v, gx - 0.5, gy)]; };

W.extrapolate = function (sweeps) {   // fill the faces inside the body with the mean of their outside neighbours (sweeps layers deep), so advection reads fluid, not the body
  var nx = this.nx, ny = this.ny, Wu = nx + 1, pu = this.phU, pv = this.phV, u = this.u, v = this.v, mu = this._mu || (this._mu = new Uint8Array(u.length)), mv = this._mv || (this._mv = new Uint8Array(v.length)), i, j, c, k;
  for (c = 0; c < u.length; c++) mu[c] = pu[c] < 0 ? 0 : 1; for (c = 0; c < v.length; c++) mv[c] = pv[c] < 0 ? 0 : 1;
  for (k = 0; k < sweeps; k++) { var tu = [], tv = [];
    for (j = 0; j < ny; j++) for (i = 0; i <= nx; i++) { c = j * Wu + i; if (mu[c]) continue; var s = 0, n = 0;
      if (i > 0 && mu[c - 1] === 1) { s += u[c - 1]; n++; } if (i < nx && mu[c + 1] === 1) { s += u[c + 1]; n++; } if (j > 0 && mu[c - Wu] === 1) { s += u[c - Wu]; n++; } if (j < ny - 1 && mu[c + Wu] === 1) { s += u[c + Wu]; n++; }
      if (n) tu.push(c, s / n); }
    for (j = 0; j <= ny; j++) for (i = 0; i < nx; i++) { c = j * nx + i; if (mv[c]) continue; var s2 = 0, n2 = 0;
      if (i > 0 && mv[c - 1] === 1) { s2 += v[c - 1]; n2++; } if (i < nx - 1 && mv[c + 1] === 1) { s2 += v[c + 1]; n2++; } if (j > 0 && mv[c - nx] === 1) { s2 += v[c - nx]; n2++; } if (j < ny && mv[c + nx] === 1) { s2 += v[c + nx]; n2++; }
      if (n2) tv.push(c, s2 / n2); }
    for (c = 0; c < tu.length; c += 2) { this.impX = (this.impX || 0) + this.rho * this.b * this.dx * this.dx * this.wu[tu[c]] * (tu[c + 1] - u[tu[c]]); u[tu[c]] = tu[c + 1]; mu[tu[c]] = 1; } for (c = 0; c < tv.length; c += 2) { v[tv[c]] = tv[c + 1]; mv[tv[c]] = 1; } } };
W.advect = function (dt) {   // MacCormack with semi-Lagrangian steps, midpoint backtrace, clamped to the local extrema of the departure cell (Selle et al. 2008, J. Sci. Comput. 35, 350)
  var nx = this.nx, ny = this.ny, Wu = nx + 1, self = this, u0 = this.u0, v0 = this.v0, uF = this.uF, vF = this.vF, i, j, c; u0.set(this.u); v0.set(this.v);
  var h = dt / this.dx, dXu = this._dXu || (this._dXu = new Float64Array(u0.length)), dYu = this._dYu || (this._dYu = new Float64Array(u0.length)), dXv = this._dXv || (this._dXv = new Float64Array(v0.length)), dYv = this._dYv || (this._dYv = new Float64Array(v0.length));
  var sU = function (A, gx, gy) { if (gx < 0) gx = 0; else if (gx > nx - 1e-9) gx = nx - 1e-9; if (gy < 0) gy = 0; else if (gy > ny - 1 - 1e-9) gy = ny - 1 - 1e-9;
    var i = gx | 0, j = gy | 0, a = gx - i, b = gy - j, c = j * Wu + i; return (1 - b) * ((1 - a) * A[c] + a * A[c + 1]) + b * ((1 - a) * A[c + Wu] + a * A[c + Wu + 1]); };
  var sV = function (A, gx, gy) { if (gx < 0) gx = 0; else if (gx > nx - 1 - 1e-9) gx = nx - 1 - 1e-9; if (gy < 0) gy = 0; else if (gy > ny - 1e-9) gy = ny - 1e-9;
    var i = gx | 0, j = gy | 0, a = gx - i, b = gy - j, c = j * nx + i; return (1 - b) * ((1 - a) * A[c] + a * A[c + 1]) + b * ((1 - a) * A[c + nx] + a * A[c + nx + 1]); };
  var PX = 0, PY = 0;
  function trace(X, Y, hh) { var ux = sU(u0, X, Y - 0.5), uy = sV(v0, X - 0.5, Y), Xm = X - 0.5 * hh * ux, Ym = Y - 0.5 * hh * uy; PX = X - hh * sU(u0, Xm, Ym - 0.5); PY = Y - hh * sV(v0, Xm - 0.5, Ym); }
  for (j = 0; j < ny; j++) for (i = 1; i < nx; i++) { c = j * Wu + i; trace(i, j + 0.5, h); dXu[c] = PX; dYu[c] = PY; uF[c] = sU(u0, PX, PY - 0.5); }
  for (j = 1; j < ny; j++) for (i = 0; i < nx; i++) { c = j * nx + i; trace(i + 0.5, j, h); dXv[c] = PX; dYv[c] = PY; vF[c] = sV(v0, PX - 0.5, PY); }
  for (j = 0; j < ny; j++) for (i = 1; i < nx; i++) { c = j * Wu + i; trace(i, j + 0.5, -h); var val = uF[c] + 0.5 * (u0[c] - sU(uF, PX, PY - 0.5));
    var gx = Math.min(Math.max(dXu[c], 0), nx - 1e-9), gy = Math.min(Math.max(dYu[c] - 0.5, 0), ny - 1 - 1e-9), k = (gy | 0) * Wu + (gx | 0);
    var a1 = u0[k], a2 = u0[k + 1], a3 = u0[k + Wu], a4 = u0[k + Wu + 1], lo = Math.min(a1, a2, a3, a4), hi = Math.max(a1, a2, a3, a4); this.u[c] = (val < lo || val > hi) ? uF[c] : val; }
  for (j = 1; j < ny; j++) for (i = 0; i < nx; i++) { c = j * nx + i; trace(i + 0.5, j, -h); var val2 = vF[c] + 0.5 * (v0[c] - sV(vF, PX - 0.5, PY));
    var gx2 = Math.min(Math.max(dXv[c] - 0.5, 0), nx - 1 - 1e-9), gy2 = Math.min(Math.max(dYv[c], 0), ny - 1e-9), k2 = (gy2 | 0) * nx + (gx2 | 0);
    var b1 = v0[k2], b2 = v0[k2 + 1], b3 = v0[k2 + nx], b4 = v0[k2 + nx + 1], lo2 = Math.min(b1, b2, b3, b4), hi2 = Math.max(b1, b2, b3, b4); this.v[c] = (val2 < lo2 || val2 > hi2) ? vF[c] : val2; }
  this.boundary(); };
W.diffuse = function (dt, xd) {   // explicit viscosity, substepped; no-slip on the body at its true surface by a ghost value (linear through the wall, distance θ dx),
  // the wall link taken implicitly so that small θ stays stable (Gibou et al. 2002, J. Comput. Phys. 176, 205). Returns the x-momentum the body's surface gave the fluid (N s).
  var nx = this.nx, ny = this.ny, dx = this.dx, nu = this.nu, Wu = nx + 1, i, j, c, k; if (!nu || !this.rho) return 0;
  var n = Math.max(1, Math.ceil(nu * dt / (0.2 * dx * dx))), a = nu * (dt / n) / (dx * dx), u0 = this.u0, v0 = this.v0, shear = 0, pu = this.phU, pv = this.phV, ns = this.noslip;
  for (var s = 0; s < n; s++) { u0.set(this.u); v0.set(this.v);
    for (j = 0; j < ny; j++) for (i = 1; i < nx; i++) { c = j * Wu + i; if (pu[c] < 0) continue;
      var nb = [c - 1, c + 1, j < ny - 1 ? c + Wu : -1, j > 0 ? c - Wu : -1], sum = 0, imp = 0, impb = 0;
      for (k = 0; k < 4; k++) { var q = nb[k];
        if (q < 0) { sum += ns ? -2 * u0[c] : 0; continue; }   // lid and floor: mirror (no friction) or no-slip
        if (pu[q] < 0) { var th = Math.max(pu[c] / (pu[c] - pu[q]), 0.05); imp += 1 / th; impb += xd / th; }   // a link through the body's surface
        else sum += u0[q] - u0[c]; }
      var un = (u0[c] + a * sum + a * impb) / (1 + a * imp); this.u[c] = un; if (imp) shear += this.wu[c] * a * (impb - imp * un); }
    for (j = 1; j < ny; j++) for (i = 0; i < nx; i++) { c = j * nx + i; if (pv[c] < 0) continue;
      var nb2 = [i > 0 ? c - 1 : -1, i < nx - 1 ? c + 1 : -1, c + nx, c - nx], sum2 = 0, imp2 = 0;
      for (k = 0; k < 4; k++) { var q2 = nb2[k]; if (q2 < 0) continue;
        if (pv[q2] < 0) { var th2 = Math.max(pv[c] / (pv[c] - pv[q2]), 0.05); imp2 += 1 / th2; } else sum2 += v0[q2] - v0[c]; }
      this.v[c] = (v0[c] + a * sum2) / (1 + a * imp2); }
    this.impose(xd); this.boundary(); }
  return this.rho * this.b * dx * dx * shear; };
/* the actuator lines: sample, and spread */
W.sampleAll = function () {   // the grid velocity at every rod point, with Peskin's kernel (the adjoint of spread)
  var p = this.mp, s = this.s, k, i, K = this.kin;
  for (k = 0; k < 2; k++) for (i = 0; i < NP; i++) { pointKin(p, s, k, i, K); var o = 2 * (k * NP + i); this.pos[o] = K.X; this.pos[o + 1] = K.Y; var uv = this.interp(K.X, K.Y); this.uS[o] = uv[0]; this.uS[o + 1] = uv[1]; } };
W.interp = function (X, Y) { var nx = this.nx, ny = this.ny, Wu = nx + 1, dx = this.dx, gx = (X - this.x0) / dx, gy = (Y - this.y0) / dx - 0.5, i0 = Math.floor(gx), j0 = Math.floor(gy), su = 0, sv = 0, i, j;
  for (j = j0 - 1; j <= j0 + 2; j++) { if (j < 0 || j >= ny) continue; var wy = phi4(j - gy); for (i = i0 - 1; i <= i0 + 2; i++) { if (i < 0 || i > nx) continue; su += wy * phi4(i - gx) * this.u[j * Wu + i]; } }
  gx -= 0.5; gy += 0.5; i0 = Math.floor(gx); j0 = Math.floor(gy);
  for (j = j0 - 1; j <= j0 + 2; j++) { if (j < 0 || j > ny) continue; var wy2 = phi4(j - gy); for (i = i0 - 1; i <= i0 + 2; i++) { if (i < 0 || i >= nx) continue; sv += wy2 * phi4(i - gx) * this.v[j * nx + i]; } }
  return [su, sv]; };
W.spread = function (X, Y, Ix, Iy) {   // an impulse (N s) on the fluid at (X, Y): Δu = I δ_h / (ρ b); what lands on faces inside the cart is the cart's. Returns [Ix to cart, Ix spread]
  var nx = this.nx, ny = this.ny, Wu = nx + 1, dx = this.dx, f = 1 / (this.rho * this.b * dx * dx), gx = (X - this.x0) / dx, gy = (Y - this.y0) / dx - 0.5, i0 = Math.floor(gx), j0 = Math.floor(gy), toCart = 0, i, j, c, w;
  for (j = j0 - 1; j <= j0 + 2; j++) { var wy = phi4(j - gy); for (i = i0 - 1; i <= i0 + 2; i++) { w = wy * phi4(i - gx); if (!w) continue; c = Math.min(Math.max(j, 0), ny - 1) * Wu + Math.min(Math.max(i, 0), nx);
    if (this.wu[c] < 0.5) toCart += w * Ix; else this.u[c] += w * Ix * f / this.wu[c]; } }   // momentum of a face is ρ b dx² w u
  gx -= 0.5; gy += 0.5; i0 = Math.floor(gx); j0 = Math.floor(gy);
  for (j = j0 - 1; j <= j0 + 2; j++) { var wy2 = phi4(j - gy); for (i = i0 - 1; i <= i0 + 2; i++) { w = wy2 * phi4(i - gx); if (!w) continue; c = Math.min(Math.max(j, 0), ny) * nx + Math.min(Math.max(i, 0), nx - 1);
    if (this.wv[c] < 0.5) continue; this.v[c] += w * Iy * f / this.wv[c]; } }   // what lands inside the cart vertically goes into the rail
  return toCart; };

/* the force per metre of rod at one point, from the relative velocity w = v_point - u_fluid and the fluid's acceleration (33), (34), (39) */
W.rodForce = function (k, K, ux, uy, ax, ay, out) { var p = this.mp, xi = p.xi[k], wx = K.vx - ux, wy = K.vy - uy, wt = wx * K.sn + wy * K.cs, wn = wx * K.cs - wy * K.sn;
  var fn = -xi * wn - p.cq * Math.abs(wn) * wn + p.kr * (ax * K.cs - ay * K.sn), ft = -xi / 2 * wt;
  out.fx = ft * K.sn + fn * K.cs; out.fy = ft * K.cs - fn * K.sn; out.diss = -(ft * wt + (-xi * wn - p.cq * Math.abs(wn) * wn) * wn); return out; };   // diss ≥ 0: the drag's power lost below the grid, per metre

/* the machine's right-hand side with the cart's fluid force Fc held and the fluid frozen at the sampled velocities */
W.mrhs = function (s, u, Fc, acc, ma) { var p = this.mp, k, i, K = this.kin, Q = [Fc + u, 0, 0], f = this._f || (this._f = {}), P = 0, Dd = 0;
  if (this.rho && !this.noRods) for (k = 0; k < 2; k++) for (i = 0; i < NP; i++) { pointKin(p, s, k, i, K); var o = 2 * (k * NP + i);
    this.rodForce(k, K, this.uS[o], this.uS[o + 1], this.aS[o], this.aS[o + 1], f);
    Q[0] += K.wq * f.fx; if (k) { Q[1] += K.wq * p.L1 * (f.fx * K.c1 - f.fy * K.s1); Q[2] += K.wq * K.sg * (f.fx * K.cs - f.fy * K.sn); } else Q[1] += K.wq * K.sg * (f.fx * K.cs - f.fy * K.sn);
    if (acc) { acc[o] = K.wq * f.fx; acc[o + 1] = K.wq * f.fy; } Dd += K.wq * f.diss; P += K.wq * (f.fx * K.vx + f.fy * K.vy); }
  var C = Cvec(p, s), Gv = [0, -p.f[0] * Math.sin(s[1]), -p.f[1] * Math.sin(s[2])], Dm = Dmat(p, s[1], s[2]); if (ma) Dm[0][0] += ma;   // the water the cart must push aside, from the coupled pressure
  var q = solve3(Dm, [Q[0] - C[0] - Gv[0], Q[1] - C[1] - Gv[1], Q[2] - C[2] - Gv[2]]);
  var r = [s[3], s[4], s[5], q[0], q[1], q[2]]; r.D = Dd; r.P = P; r.Q = [Q[0] - Fc - u, Q[1], Q[2]]; return r; };   // r.Q: the rods' generalised force alone
W.runMachine = function (s0, ctrl, t0, G, ma, n, h, record) {   // n RK4 steps of h. The cart feels G - m_a ẍ from the fluid: m_a = -K_x dt rides on the cart's mass, G = Q0 + K_x ẋ0 is held;
  // over the step its impulse is dt (Q0 + K_x ẋ'), exactly the coupled pressure's (Batty). The motor force u = ctrl(s, t) at the start of each substep (the controller holds it between its samples).
  // With record: the rods' impulses summed with RK4's weights into this.impNew, the books, and onSub(s_before, s_after, t, u, W_fluid) for every substep.
  var s = s0.slice(), a1 = this._a1 || (this._a1 = new Float64Array(4 * NP)), a2 = this._a2 || (this._a2 = new Float64Array(4 * NP)), a3 = this._a3 || (this._a3 = new Float64Array(4 * NP)), a4 = this._a4 || (this._a4 = new Float64Array(4 * NP)), Dr = 0, Wm = 0, Wfl = 0, Qr = [0, 0, 0], j, m, t = t0;
  for (m = 0; m < n; m++) { var u = ctrl ? ctrl(s, t) : 0;
    var k1 = this.mrhs(s, u, G, record && a1, ma), s2 = s.map(function (v, i) { return v + h / 2 * k1[i]; });
    var k2 = this.mrhs(s2, u, G, record && a2, ma), s3 = s.map(function (v, i) { return v + h / 2 * k2[i]; });
    var k3 = this.mrhs(s3, u, G, record && a3, ma), s4 = s.map(function (v, i) { return v + h * k3[i]; });
    var k4 = this.mrhs(s4, u, G, record && a4, ma);
    var sn = this.frozen ? s : s.map(function (v, i) { return v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]); });
    if (record) { for (j = 0; j < 4 * NP; j++) this.impNew[j] += h / 6 * (a1[j] + 2 * a2[j] + 2 * a3[j] + a4[j]);
      var dD = h / 6 * (k1.D + 2 * k2.D + 2 * k3.D + k4.D), dW = h / 6 * (k1.P + 2 * k2.P + 2 * k3.P + k4.P) + G * (sn[0] - s[0]) - ma * (sn[3] * sn[3] - s[3] * s[3]) / 2;   // the fluid's work on the machine: rods + cart (G Δx − m_a Δ(ẋ²)/2)
      for (j = 0; j < 3; j++) Qr[j] += (k1.Q[j] + 2 * k2.Q[j] + 2 * k3.Q[j] + k4.Q[j]) / (6 * n);
      Dr += dD; Wm += u * (sn[0] - s[0]); Wfl += dW; this.u_m = u; if (this.onSub) this.onSub(s, sn, t, u, dW); }
    s = sn; t += h; }
  if (record) { this._Dr = Dr; this._Wm = Wm; this._Wfl = Wfl; this.Qrod = Qr; } return s; };
/* generalized x-force of a pressure field on the cart: -Σ b (1 - w) dx² ∂p/∂x over the cart's u-faces */
W.cartForce = function (p) { var nx = this.nx, ny = this.ny, dx = this.dx, Wu = nx + 1, F = 0, i, j;
  for (j = 0; j < ny; j++) for (i = 1; i < nx; i++) { var c = j * Wu + i, sol = 1 - this.wu[c]; if (sol <= 0) continue; F -= this.b * sol * dx * dx * (p[j * nx + i] - p[j * nx + i - 1]) / dx; }
  return F; };
W.divFluid = function (out) { var nx = this.nx, ny = this.ny, dx = this.dx, Wu = nx + 1, i, j;
  for (j = 0; j < ny; j++) for (i = 0; i < nx; i++) { var c = j * nx + i; out[c] = -((this.wu[j * Wu + i + 1] * this.u[j * Wu + i + 1] - this.wu[j * Wu + i] * this.u[j * Wu + i]) + (this.wv[(j + 1) * nx + i] * this.v[(j + 1) * nx + i] - this.wv[j * nx + i] * this.v[j * nx + i])) / dx; } };
W.divCart = function (out) {   // divergence of (1 - w) · 1 on the u-faces: the cart moving at 1 m/s
  var nx = this.nx, ny = this.ny, dx = this.dx, Wu = nx + 1, i, j;
  for (j = 0; j < ny; j++) for (i = 0; i < nx; i++) out[j * nx + i] = -((1 - this.wu[j * Wu + i + 1]) - (1 - this.wu[j * Wu + i])) / dx; };
W.project = function (p, dt) { var nx = this.nx, ny = this.ny, dx = this.dx, Wu = nx + 1, s = dt / (this.rho * dx), i, j, c;
  for (j = 0; j < ny; j++) for (i = 1; i <= nx; i++) { c = j * Wu + i; if (this.wx[c] <= 0) continue; this.u[c] -= s * ((i < nx ? p[j * nx + i] : 0) - p[j * nx + i - 1]); }
  for (j = 1; j < ny; j++) for (i = 0; i < nx; i++) { c = j * nx + i; if (this.wy[c] <= 0) continue; this.v[c] -= s * (p[j * nx + i] - p[(j - 1) * nx + i]); } };
W.maxDiv = function () { var nx = this.nx, ny = this.ny, dx = this.dx, Wu = nx + 1, xd = this.s[3], mx = 0, i, j;
  for (j = 0; j < ny; j++) for (i = 0; i < nx; i++) { if (!this.P.L[0].d[j * nx + i]) continue;
    var e = j * Wu + i + 1, w = j * Wu + i, n = (j + 1) * nx + i, s = j * nx + i;
    var d = ((this.wu[e] * this.u[e] + (1 - this.wu[e]) * xd) - (this.wu[w] * this.u[w] + (1 - this.wu[w]) * xd) + this.wv[n] * this.v[n] - this.wv[s] * this.v[s]) / dx;
    if (Math.abs(d) > mx) mx = Math.abs(d); } return mx; };

/* one fluid step of dt = nsub · h; ctrl(s, t) gives the motor force, called once at the start (sampled, held) */
W.step = function (ctrl) {
  var h = this.h, n = this.nsub, dt = h * n, B = this.book, k, i, o, xd0 = this.s[3];
  if (!this.rho) { this.impNew = new Float64Array(4 * NP); var sV = this.runMachine(this.s, ctrl, this.t, 0, 0, n, h, true); B.Wm += this._Wm; this.s = sV; this.t += dt; return; }
  var T0 = Date.now(); if (this.geom) this.geom(); else this.measure(); var impPrev = this.impX || 0; this.impX = 0; this.impose(xd0); this.boundary(); var T1 = Date.now();
  // 1. sample the fluid at the rod points (divergence-free field at the start of the step) and its acceleration there
  this.uS1.set(this.uS); this.sampleAll();
  if (this.first) { this.aS.fill(0); this.first = false; } else for (o = 0; o < 4 * NP; o++) this.aS[o] = (this.uS[o] - this.uS1[o]) / dt;   // ∂u/∂t at the point
  for (o = 0; o < 4 * NP; o += 2) { var X = this.pos[o], Y = this.pos[o + 1], e = 0.5 * this.dx, gxp = this.interp(X + e, Y), gxm = this.interp(X - e, Y), gyp = this.interp(X, Y + e), gym = this.interp(X, Y - e), ux = this.uS[o], uy = this.uS[o + 1];
    this.aS[o] += (ux * (gxp[0] - gxm[0]) + uy * (gyp[0] - gym[0])) / (2 * e); this.aS[o + 1] += (ux * (gxp[1] - gxm[1]) + uy * (gyp[1] - gym[1])) / (2 * e); }   // + (u·∇)u: the acceleration of the fluid's particles (39)
  var E = this.KE(), Pf = this.momX();
  // 2. deliver last step's impulse of the rods to the fluid (Newton's third law: minus what the rods received)
  var toCart = 0; if (this.haveImp) for (o = 0; o < 4 * NP; o += 2) toCart += this.spread(this.impPos[o], this.impPos[o + 1], -this.imp[o], -this.imp[o + 1]);
  var E1 = this.KE(); B.Erod += E1 - E; B.Ptransit = 0;
  // 3. advect and diffuse
  var T2 = Date.now(); if (!this.noExtrap) this.extrapolate(3); this.advect(dt); this.impose(xd0); var T3 = Date.now(); var E2 = this.KE(); B.Eadv += E2 - E1;
  var shear = this.diffuse(dt, xd0); var E3 = this.KE(); B.Ediff += E3 - E2; B.Wshear = (B.Wshear || 0) + shear * xd0;   // the cart's shear does work shear·ẋ on the fluid; the rest of Ediff is viscous dissipation
  // 4. pressure: p = p0 + ẋ' p_x
  var T4 = Date.now(); this.divFluid(this.rhs); var f = this.rho / dt; for (i = 0; i < this.rhs.length; i++) this.rhs[i] *= f; this.its0 = this.P.solve(this.rhs, this.p0);
  this.divCart(this.rhs); for (i = 0; i < this.rhs.length; i++) this.rhs[i] *= f; this.itsx = this.P.solve(this.rhs, this.px);
  var Q0 = this.cartForce(this.p0) - shear / dt + toCart / dt - (this.impX + impPrev) / dt, Kx = this.cartForce(this.px);   // the fluid's force on the cart is Q0 + Kx ẋ' (Kx < 0: the water the cart must push aside)
  // 5. the machine over the step, with the cart force consistent with its velocity at the end of the step (two RK4 runs give the slope; a third checks)
  var T5 = Date.now(), s0 = this.s, ma = -Kx * dt, G = Q0 + Kx * xd0;
  this.impNew = new Float64Array(4 * NP); var sN = this.runMachine(s0, ctrl, this.t, G, ma, n, h, true); var Fc = Q0 + Kx * sN[3];   // the cart's mean fluid force over the step
  // 6. project with the cart's new velocity
  for (i = 0; i < this.pF.length; i++) this.pF[i] = this.p0[i] + sN[3] * this.px[i];
  this.project(this.pF, dt); B.Ebnd = (B.Ebnd || 0) + this.boundaryPower() * dt; this.impX = 0; this.impose(sN[3], true);   // after the pressure step only the wholly solid faces are overridden, so the field stays divergence-free
  this.boundary(); var E4 = this.KE(); B.Eproj += E4 - E3;
  // books: motor work u Δx, the cart's work by the fluid, the rods' dissipation below the grid, impulse in transit
  B.Wm += this._Wm; B.Ecart += Fc * (sN[0] - s0[0]); B.Drod += this._Dr; B.Wfl = (B.Wfl || 0) + this._Wfl;
  this.imp.set(this.impNew); for (o = 0; o < 4 * NP; o += 2) { this.impPos[o] = this.pos[o]; this.impPos[o + 1] = this.pos[o + 1]; } this.haveImp = true;
  var T6 = Date.now(); this.prof = this.prof || [0, 0, 0, 0, 0, 0]; [T1 - T0, T2 - T1, T3 - T2, T4 - T3, T5 - T4, T6 - T5].forEach(function (v, i) { this.prof[i] += v; }, this);
  this.Fc = Fc; this.Q0 = Q0; this.Kx = Kx; this.ma = ma; this.s = sN; this.t += dt;
};
W.vorticity = function (out) {   // ω = ∂v/∂x − ∂u/∂y at the cell corners ((nx+1) × (ny+1), zero on the edges and inside the cart), 1/s
  var nx = this.nx, ny = this.ny, Wu = nx + 1, dx = this.dx, i, j; out.fill(0);
  for (j = 1; j < ny; j++) for (i = 1; i < nx; i++) { if (this.phU[j * Wu + i] < 0 && this.phU[(j - 1) * Wu + i] < 0) continue; out[j * Wu + i] = ((this.v[j * nx + i] - this.v[j * nx + i - 1]) - (this.u[j * Wu + i] - this.u[(j - 1) * Wu + i])) / dx; }
  return out; };
W.boundaryPower = function () {   // power carried into the tank through its ends: ρ b Δ Σ u (½u² + p/ρ) at the inlet, minus the same at the open end (p = 0 there), W
  var nx = this.nx, ny = this.ny, Wu = nx + 1, j, P = 0, r = this.rho;
  for (j = 0; j < ny; j++) { var ui = this.u[j * Wu], uo = this.u[j * Wu + nx]; P += ui * (0.5 * r * ui * ui + this.pF[j * nx]) - uo * (0.5 * r * uo * uo); }
  return P * this.b * this.dx; };
W.transitX = function () { var s = 0; for (var o = 0; o < 4 * NP; o += 2) s -= this.imp[o]; return this.haveImp ? s : 0; };   // the x-impulse the rods have taken and the fluid has not yet received (N s)

return { World: World, machinePar: machinePar, Dmat: Dmat, energy: energy, momX: momX, MEDIA: MEDIA, GLR: GLR, NP: NP, phi4: phi4, pointKin: pointKin, CART_W: CART_W, CART_H: CART_H, CART_B: CART_B, ROD_R: ROD_R };
});
