// Added mass of a 2D blade (the rod of project 05 seen in a 2D world): chord c = 0.5 m, thickness 0.02 m, oscillating across itself.
// Nearly inviscid (nu = 1e-5), small amplitude. Inertial force amplitude / (w^2 X) = m_a + interior mass; compare with rho pi (c/2)^2.
const { NS, Body } = require('./ns2.cjs');
const N = +(process.env.N || 256), L = 2.56, nu = 1e-5, c = 0.5, h = 0.02, f = 2, w = 2 * Math.PI * f, X = 0.004;
const ns = new NS({ N, M: N, Lx: L, Ly: L, nu, eta: 1e-4, cfl: 0.5, dtMax: 1 / (f * 200) }); ns.setSponge(() => [0, 0, 0]);
const sdfBox = (x, y) => { const qx = Math.abs(x) - c / 2 + h / 2, qy = Math.abs(y); return Math.hypot(Math.max(qx, 0), 0) > 0 ? Math.hypot(Math.max(qx, 0), Math.max(qy, 0)) - h / 2 : qy - h / 2; };  // stadium: segment with radius h/2
const bl = new Body(ns, { ramp: true, sdf: (x, y) => { const qx = Math.max(Math.abs(x) - (c / 2 - h / 2), 0); return Math.hypot(qx, y) - h / 2; }, xc: L / 2, yc: L / 2,
  motion: (t, b) => { b.yc = L / 2 + X * Math.sin(w * t); b.vy = X * w * Math.cos(w * t); } });
ns.bodies = [bl]; ns.setOmega(() => 0);
const P = 4, hist = []; while (ns.t < P / f - 1e-12) { ns.step(Math.min(1 / (f * 200), P / f - ns.t)); hist.push([ns.t, bl.F[1]]); }
let cc = 0, ss = 0, cs = 0, yc = 0, ys = 0; for (const q of hist) if (q[0] > (P - 2) / f) { const C = Math.cos(w * q[0]), S = Math.sin(w * q[0]); cc += C * C; ss += S * S; cs += C * S; yc += q[1] * C; ys += q[1] * S; }
const det = cc * ss - cs * cs, A = (yc * ss - ys * cs) / det, B = (ys * cc - yc * cs) / det;
let area = 0; for (let p = 0; p < N * N; p++) area += bl.chi[p]; area *= ns.dA;
// F = (m_a + m_in) * w^2 X sin(wt) for a pure inertial force (density 1); m_in is the fluid inside, 'area'
console.log(JSON.stringify({ N, dx: L / N, cos: A, sin: B, mTotal: B / (w * w * X), interior: area, addedMass: B / (w * w * X) - area, potentialPlate: Math.PI * (c / 2) ** 2, ratio: (B / (w * w * X) - area) / (Math.PI * (c / 2) ** 2) }));
