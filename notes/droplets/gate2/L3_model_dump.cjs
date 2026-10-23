// Gate 2, L3: fall speeds (inputs, read only from the model) for the chapter-4 example numbers
const P = require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs');
const out = {};
for (const [name, T, p] of [['cloud', 283.15, 85000], ['std20', 293.15, 101325]]) {
  const A = P.air(T, p); out[name] = { T, air: A, sigma_model: P.sigmaWater(T), k: P.stokesK(A), v: {} };
  for (const a of [8, 40, 50, 60, 250, 500]) out[name].v[a] = { B: P.vBeard(a * 1e-6, A), S: P.vStokes(a * 1e-6, A) };
}
console.log(JSON.stringify(out));
