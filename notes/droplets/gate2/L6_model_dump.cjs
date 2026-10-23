// Gate 2, L6: model values (read only) for the python cross-check: ayalaFactor, fall speeds, air
const P = require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs');
const A = P.air(283.15, 85000), out = { nu: A.nu, rho: A.rho, mu: A.mu, factor: [], v: {}, cut: {} };
for (const eps of [1e-12, 1e-10, 1e-8, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 4e-2, 0.1]) out.factor.push({ eps, f: P.ayalaFactor(40e-6, 8e-6, A, eps) });
for (const a of [8, 20, 30, 40, 43, 50, 60]) out.v[a] = P.vBeard(a * 1e-6, A);
// size at which the Stokes number tau_p/tau_K passes 1 for eps = 0.04 (the text: 43 um): scan
for (let a = 30; a <= 60; a += 0.05) { const tp = P.vBeard(a * 1e-6, A) / 9.81, tk = Math.sqrt(A.nu / 0.04); if (tp / tk > 1) { out.cut.a1 = a; break; } }
// pairs used for the factor with different partner sizes
out.pairs = [];
for (const [a1, a2] of [[40, 8], [30, 10], [20, 10], [50, 10]]) for (const eps of [1e-3, 1e-2, 4e-2]) out.pairs.push({ a1, a2, eps, f: P.ayalaFactor(a1 * 1e-6, a2 * 1e-6, A, eps) });
console.log(JSON.stringify(out));
