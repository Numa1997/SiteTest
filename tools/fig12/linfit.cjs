// Fit the free swing after the pulse in the series written by linearity.cjs: node tools/fig12/linfit.cjs runs/*.json
// For t in [Tp + 0.1 s, T]: least squares of lean(t) = a cos(2 pi f t) + b sin(2 pi f t) + c + d t over f on a 0.5 mHz grid
// in 2.5–4.5 Hz; the f with the smallest residual is the swing frequency, sqrt(a^2 + b^2) its amplitude, rms the misfit.
const fs = require('fs');
function solve(M, v) { const n = v.length; for (let i = 0; i < n; i++) { let p = i; for (let r = i + 1; r < n; r++) if (Math.abs(M[r][i]) > Math.abs(M[p][i])) p = r; [M[i], M[p]] = [M[p], M[i]]; [v[i], v[p]] = [v[p], v[i]]; for (let r = i + 1; r < n; r++) { const k = M[r][i] / M[i][i]; for (let c = i; c < n; c++) M[r][c] -= k * M[i][c]; v[r] -= k * v[i]; } } const x = new Array(n); for (let i = n - 1; i >= 0; i--) { let s = v[i]; for (let c = i + 1; c < n; c++) s -= M[i][c] * x[c]; x[i] = s / M[i][i]; } return x; }
for (const file of process.argv.slice(2)) {
  const J = JSON.parse(fs.readFileSync(file, 'utf8'));
  for (const r of J.out) {
    const pts = r.series.filter(([t]) => t > J.Tp + 0.1);
    let best = null;
    for (let f = 2.5; f <= 4.5; f += 0.0005) {
      const w = 2 * Math.PI * f, M = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], v = [0,0,0,0];
      for (const [t, y] of pts) { const b = [Math.cos(w * t), Math.sin(w * t), 1, t]; for (let i = 0; i < 4; i++) { v[i] += b[i] * y; for (let j = 0; j < 4; j++) M[i][j] += b[i] * b[j]; } }
      const x = solve(M, v); let e = 0; for (const [t, y] of pts) { const m = x[0] * Math.cos(w * t) + x[1] * Math.sin(w * t) + x[2] + x[3] * t; e += (y - m) ** 2; }
      if (!best || e < best.e) best = { f, amp: Math.hypot(x[0], x[1]), e };
    }
    console.log(`${J.model.padEnd(5)} A ${String(r.A).padStart(3)} m/s^2: peak lean ${String(Math.abs(r.lean_mm)).padStart(5)} mm, free swing ${best.amp.toFixed(1).padStart(5)} mm at ${best.f.toFixed(3)} Hz, misfit rms ${Math.sqrt(best.e / pts.length).toFixed(2)} mm, spill ${r.spill_g} g`);
  }
}
