'use strict';
// Trace one trajectory and report where it touches (polar angle from the upstream axis) or how close it passes.
const T = require('./L2_traj.cjs');
const B = require('./beard.cjs');
const A = B.air(283.15, 85000);
function trace(R, p, b, flow) {
  const U = B.vt(R, A), gs = B.g * (1 - A.rho / 1000), r = p * R, vr = B.vt(r, A), St = vr / gs * U / R, S = vr / U;
  const F = T.flowField(flow); let x = b, z = -200; const a0 = F.a(x, z); let y = [x, z, a0[0], a0[1] - S];
  const rc = 1 + p; let h = 1e-3, minGap = 1e9, zmin = 0, s = 0;
  for (let n = 0; n < 4e6; n++) {
    const f = (y) => { const a = F.a(y[0], y[1]); return [y[2], y[3], (a[0] - y[2]) / St, (a[1] - y[3] - S) / St]; };
    // RK4 fixed small step near the collector, larger far away
    const q = Math.hypot(y[0], y[1]); h = Math.min(0.02 * St, 0.002 * Math.max(q - rc, 0.01) + 1e-4);
    const k1 = f(y), k2 = f(y.map((v, i) => v + h / 2 * k1[i])), k3 = f(y.map((v, i) => v + h / 2 * k2[i])), k4 = f(y.map((v, i) => v + h * k3[i]));
    y = y.map((v, i) => v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])); s += h;
    const gap = Math.hypot(y[0], y[1]) - rc;
    if (gap < minGap) { minGap = gap; zmin = y[1]; }
    if (gap <= 0) return `touches at polar angle ${(Math.acos(-y[1] / Math.hypot(y[0], y[1])) * 180 / Math.PI).toFixed(1)} deg from the upstream axis (z=${y[1].toFixed(3)})`;
    if (y[1] > 4) return `misses; closest gap ${minGap.toExponential(2)} at z=${zmin.toFixed(3)}`;
  }
  return 'unfinished';
}
for (const p of [0.4, 0.45, 0.5]) for (const b of [0.0, 0.05, 0.12]) console.log(`R=20um p=${p} b=${b}: ${trace(20e-6, p, b, 'stokes')}`);
console.log(`R=40um p=0.2 b=0.3: ${trace(40e-6, 0.2, 0.3, 'stokes')}`);
console.log(`R=40um p=0.2 b=0.6: ${trace(40e-6, 0.2, 0.6, 'stokes')}`);
