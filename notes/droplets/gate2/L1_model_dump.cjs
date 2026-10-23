// Gate 2, L1: dump the model's fall speeds (read only) for the python cross-check.
const P = require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs');
const out = {};
for (const [name, T, p] of [['cloud', 283.15, 85000], ['std20', 293.15, 101325]]) {
  const A = P.air(T, p); out[name] = { air: A, k: P.stokesK(A), rows: [] };
  for (const a_um of [8, 20, 30, 40, 41, 50, 60, 80, 100, 150, 200, 300, 500, 1000]) {
    const a = a_um * 1e-6; out[name].rows.push({ a_um, vS: P.vStokes(a, A), vB: P.vBeard(a, A) });
  }
}
console.log(JSON.stringify(out));
