// Golovin test of the SCE scheme (L4): sum kernel K = b (m + m'), exponential start, against the exact solution.
// b = 1.5 m^3 kg^-1 s^-1, mean radius 10 um, L = 1 g/m^3, 60 min (the parameters of the baseline's test, after Bott 1998).
'use strict';
const P = require('../physics.cjs');
function run(s, dt) {
  const grid = P.makeGrid(s, 4e-3), n = grid.n, b = 1.5, mbar = P.massOf(10e-6), L = 1e-3, N0 = L / mbar, w = Math.LN2 / s;
  const K = new Float64Array(n * n);
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) K[i * n + j] = b * (grid.x[i] + grid.x[j]);
  const Nb = Float64Array.from(grid.x.map(x => N0 / mbar * Math.exp(-x / mbar) * x * w));
  const res = P.sceRun(grid, null, null, null, { K, N0: Nb, dt, tEnd: 3600, recordEvery: 3600, snapAt: [3600] });
  const t = 3600, Nend = res.snaps[3600];
  let eps = 0, Nnum = 0, Mnum = 0, kmax = 0, kmaxE = 0, gmax = 0, gmaxE = 0;
  for (let k = 0; k < n; k++) {
    const Mk = Nend[k] * grid.x[k], Me = P.golovinDensity(grid.x[k], t, b, N0, mbar) * grid.x[k] * grid.x[k] * w;
    eps += Math.abs(Mk - Me); Nnum += Nend[k]; Mnum += Mk;
    if (Mk > gmax) { gmax = Mk; kmax = k; } if (Me > gmaxE) { gmaxE = Me; kmaxE = k; }
  }
  eps /= L;
  const Mstart = Nb.reduce((a, v, k) => a + v * grid.x[k], 0);
  const Nexact = N0 * Math.exp(-b * L * t);
  return { s, dt, bins: n, eps, massErr: (Mnum + res.overflow.M) / L - 1, massStart: Mstart / L - 1, schemeDrift: (Mnum + res.overflow.M) / Mstart - 1,
    numErr: (Nnum + res.overflow.N) / Nexact - 1, peak: grid.r[kmax] * 1e6, peakExact: grid.r[kmaxE] * 1e6, fixes: res.fixes, over: res.overflow.M / L };
}
const rows = [];
for (const [s, dt] of [[2, 1], [4, 1], [8, 1], [8, 0.5], [16, 1]]) {
  const t0 = Date.now(), r = run(s, dt); rows.push(r);
  console.log(`s=${String(s).padStart(2)} dt=${dt}: bins ${r.bins}, eps ${r.eps.toFixed(4)}, mass error ${r.massErr.toExponential(2)} (initial truncation ${r.massStart.toExponential(2)}, scheme drift ${r.schemeDrift.toExponential(1)}), number error ${r.numErr.toFixed(4)}, peak ${r.peak.toFixed(0)} um (exact ${r.peakExact.toFixed(0)}), overflow ${r.over.toExponential(1)}, fixes ${r.fixes}  [${((Date.now() - t0) / 1000).toFixed(1)} s]`);
}
const e = s => rows.find(r => r.s === s && r.dt === 1).eps;
console.log(`observed order log2(eps_s/eps_2s): 2->4 ${Math.log2(e(2) / e(4)).toFixed(2)}, 4->8 ${Math.log2(e(4) / e(8)).toFixed(2)}, 8->16 ${Math.log2(e(8) / e(16)).toFixed(2)}`);
if (process.argv[2] === '--json') require('fs').writeFileSync(require('path').join(__dirname, '..', 'data', 'golovin.json'), JSON.stringify(rows));
