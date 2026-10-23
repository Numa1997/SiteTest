'use strict';
// Point droplet (p -> 0), no settling (S = 0): compare with Langmuir (1948) Table 1, K = St (radius-based)
const { efficiency } = require('./L2_traj.cjs');
const tab = { 0.2: [0.081, 0], 0.4: [0.199, 0], 1: [0.445, 0], 1.5: [0.563, 0.066], 2: [0.640, 0.186], 3: [0.738, 0.326], 5: [0.826, 0.472], 10: [0.907, 0.634], 20: [0.952, 0.760], 50: [0.980, 0.872], 100: [0.990, 0.924] };
console.log('  K    E_A here  Langmuir   E_V here  Langmuir   E_A=K^2/(K+1/2)^2  E_V=[1+.75ln2K/(K-1.214)]^-2');
for (const K of Object.keys(tab).map(Number)) {
  const p = 1e-4;
  const ea = efficiency('potential', K, 0, p, 30).E, ev = efficiency('stokes', K, 0, p, 400).E;
  const fa = K * K / Math.pow(K + 0.5, 2), fv = K > 1.214 ? Math.pow(1 + 0.75 * Math.log(2 * K) / (K - 1.214), -2) : 0;
  console.log(`${String(K).padStart(5)}   ${ea.toFixed(3)}    ${tab[K][0].toFixed(3)}      ${ev.toFixed(3)}    ${tab[K][1].toFixed(3)}      ${fa.toFixed(3)}              ${fv.toFixed(3)}`);
}
