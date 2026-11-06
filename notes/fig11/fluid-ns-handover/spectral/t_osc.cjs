// A cylinder (a = 0.05 m) oscillating x = X sin(w t) in fluid at rest, periodic box, density 1.
// Exact unsteady-Stokes force (derived in Wolfram): F = -rho pi a^2 [1 + 4 K1(ka)/(ka K0(ka))] dU/dt, k = sqrt(-i w/nu).
// Fit F(t) = c cos(wt) + s sin(wt) over the last two periods; print c, s for comparison with the exact complex amplitude.
const { NS, Body } = require('./ns2.cjs');
const N = +(process.env.N || 512), L = 1.28, nu = +(process.env.NU || 1e-3), a = 0.05, f = 1, w = 2 * Math.PI * f, X = +(process.env.X || 0.002);
const ns = new NS({ N, M: N, Lx: L, Ly: L, nu, eta: +(process.env.ETA || 2e-5), cfl: 0.5, dtMax: 1 / (f * 400), mix: !!process.env.MIX });
ns.setSponge(() => [0, 0, 0]);
const cyl = new Body(ns, { sdf: (x, y) => Math.hypot(x, y) - a, xc: L / 2, yc: L / 2,
  motion: (t, b) => { b.xc = L / 2 + X * Math.sin(w * t); b.vx = X * w * Math.cos(w * t); } });
ns.bodies = [cyl]; ns.setOmega(() => 0);
const P = +(process.env.P || 5), hist = [], t0 = Date.now();
while (ns.t < P / f - 1e-12) { ns.step(Math.min(1 / (f * 400), P / f - ns.t)); hist.push([ns.t, cyl.F[0], cyl.Fpen[0], cyl.Fin[0]]); }
const fit = (col) => { let cc = 0, ss = 0, cs = 0, yc = 0, ys = 0; for (const h of hist) if (h[0] > (P - 2) / f) {
  const c = Math.cos(w * h[0]), s = Math.sin(w * h[0]); cc += c * c; ss += s * s; cs += c * s; yc += h[col] * c; ys += h[col] * s; }
  const det = cc * ss - cs * cs; return [(yc * ss - ys * cs) / det, (ys * cc - yc * cs) / det]; };
let mass = 0; for (let p = 0; p < N * N; p++) mass += cyl.chi[p]; mass *= ns.dA;
console.log(JSON.stringify({ N, nu, X, KC: 2 * Math.PI * X / (2 * a), eta: ns.eta, steps: hist.length, total: fit(1), pen: fit(2), interior: fit(3), maskArea: mass, piA2: Math.PI * a * a, sec: (Date.now() - t0) / 1000 }));
