// A fixed cylinder (radius a) in a uniform stream oscillating as U(t) = U0 sin ωt, Re and KC small (advection negligible).
// Exact (unsteady Stokes, Wolfram-checked form for the moving cylinder + Froude–Krylov): F = ρπa² [2 + 4 K1(ka)/(ka K0(ka))] dU/dt in complex amplitudes, k = √(−iω/ν).
// Prints the in-phase (∝ dU/dt) and quadrature (∝ U) parts of the measured force against the exact ones.
require('../../../../public/scripts/twoway.js'); const T = globalThis.TwoWay;
const a = 0.05, L = 2.0, ny = +(process.env.NY || 160), dx = L / ny, U0 = 0.01, Tp = 2, om = 2 * Math.PI / Tp, nu = 1e-3;
const w = new T.World({ dx, nx: ny, ny, x0: -L / 2, y0: -L / 2, rho: 1, mu: nu, machine: { m0: 1, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, medium: 'glycerol' }, h: +(process.env.H || 0.001), nsub: 5 });
w.frozen = true; w.noRods = true; w.b = 1; for (const k of (process.env.OPT || '').split(',').filter(Boolean)) w[k] = true;
w.inflow = () => U0 * Math.sin(om * w.t); w.u.fill(0);
w.geom = function () { this.measureCircle(0, 0, a); };
const rec = []; while (w.t < 4 * Tp - 1e-9) { const t0 = w.t; w.step(null); rec.push([t0 + 0.5 * w.h * w.nsub, w.Q0]); }
// least squares over the last period: F ≈ A cos ωt + B sin ωt ; dU/dt = U0 ω cos ωt, U = U0 sin ωt
let c = 0, s = 0, n = 0; for (const [t, F] of rec) if (t > 3 * Tp) { c += F * Math.cos(om * t); s += F * Math.sin(om * t); n++; }
const A = 2 * c / n, B = 2 * s / n;
console.log(JSON.stringify({ cells_per_radius: +(a / dx).toFixed(1), dt: w.h * w.nsub, A_inphase_over_rhoPiA2_U0_om: +(A / (Math.PI * a * a * U0 * om)).toFixed(4), B_quadrature_over_rhoPiA2_U0_om: +(B / (Math.PI * a * a * U0 * om)).toFixed(4) }));
