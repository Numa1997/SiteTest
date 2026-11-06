// Identify the 3D solver's first sloshing mode as the controller's plant: node tools/fig12/ident.cjs [runs/linearity-3d-*.json ...]
// The runs of linearity.cjs push the glass from rest with a_x(t) = A sin(pi t / Tp), t < Tp, and record the lean
// (front − back wall height at r = R(h)) after every 5 ms step. The plant the observer and the LQR use is one oscillator,
//     q'' + 2 zeta w q' + w^2 q = −beta a_x(t),     the probes reading y = lean / 2 = q + c   (c: the reading's offset at rest),
// integrated here exactly as ModalFluid.step integrates it (symplectic Euler in 0.5 ms substeps, a_x held over each 5 ms step).
// For each (w, zeta) on a grid, beta and c enter linearly and are solved by least squares; the pair with the smallest misfit wins
// (then refined on a finer grid). Printed per amplitude: f = w / 2 pi, zeta, beta, c, the rms misfit, and beta / w^2 (the static
// lean per unit acceleration, s^2). Defaults: the A = 0.5, 1 and 2 m/s^2 runs (below breaking, notes/fig12/phase1.md §3).
const path = require('path');
const files = process.argv.slice(2).length ? process.argv.slice(2) : ['a', 'b'].map((s) => path.join(__dirname, '../../notes/fig12/runs/linearity-3d-' + s + '.json'));
function simulate(w, z, A, Tp, n, dt) {   // unit beta: the response to -a_x
  const out = new Float64Array(n), sub = Math.max(1, Math.ceil(dt / 0.0005)), hs = dt / sub;
  let q = 0, qd = 0;
  for (let k = 0; k < n; k++) {
    const t = k * dt, ax = t < Tp ? A * Math.sin(Math.PI * t / Tp) : 0;
    for (let s = 0; s < sub; s++) { qd += hs * (-w * w * q - 2 * z * w * qd - ax); q += hs * qd; }
    out[k] = q;
  }
  return out;
}
function fit(y, A, Tp, dt, wr, zr) {
  let best = null;
  for (const w of wr) for (const z of zr) {
    const u = simulate(w, z, A, Tp, y.length, dt);
    // least squares for y = beta u + c
    let su = 0, suu = 0, sy = 0, suy = 0; const n = y.length;
    for (let k = 0; k < n; k++) { su += u[k]; suu += u[k] * u[k]; sy += y[k]; suy += u[k] * y[k]; }
    const det = n * suu - su * su, beta = (n * suy - su * sy) / det, c = (sy - beta * su) / n;
    let e = 0; for (let k = 0; k < n; k++) { const r = y[k] - beta * u[k] - c; e += r * r; }
    e = Math.sqrt(e / n);
    if (!best || e < best.e) best = { w, z, beta, c, e };
  }
  return best;
}
const range = (a, b, n) => Array.from({ length: n }, (_, k) => a + (b - a) * k / (n - 1));
for (const file of files) {
  const d = require(path.resolve(file));
  for (const o of d.out) {
    if (o.A > 2.01) continue;                                  // above breaking the plant is not linear (phase1.md §3)
    const dt = o.series[1][0] - o.series[0][0], y = Float64Array.from(o.series, (r) => r[1] / 2000);
    let b = fit(y, o.A, d.Tp, dt, range(2 * Math.PI * 2.9, 2 * Math.PI * 3.6, 71), range(0, 0.06, 61));
    b = fit(y, o.A, d.Tp, dt, range(b.w - 0.05, b.w + 0.05, 41), range(Math.max(0, b.z - 0.002), b.z + 0.002, 41));
    console.log(`A ${o.A} m/s^2: f ${(b.w / 2 / Math.PI).toFixed(3)} Hz, zeta ${b.z.toFixed(4)}, beta ${b.beta.toFixed(3)}, offset ${(b.c * 1000).toFixed(2)} mm, rms misfit ${(b.e * 1000).toFixed(2)} mm, beta/w^2 ${(b.beta / b.w / b.w * 1000).toFixed(2)} mm per m/s^2`);
  }
}
