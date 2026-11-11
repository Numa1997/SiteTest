// Gate 1.1: still stout stays still. node tools/fig12/rest-gate.cjs <dx m> [T s] [dt s]      exit 1 on failure
// The tulip filled to 125 mm, no forcing, stout viscosity, wall friction on, T seconds (30 by default) at dt (5 ms).
// Limits, fixed before the first run (11 November 2026): the centre of mass moves less than 20 um; the kinetic energy
// (whole glass, particles with their affine part) averaged over the last 10 s stays under 0.1 uJ; no particle faster
// than 5 mm/s after the first second; the kinetic energy of the last 10 s at most twice that of 5-15 s (nothing grows).
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Fluid } = load('stout-cart.js'), G = load('guinness-glass.js');
const K = JSON.parse(fs.readFileSync(path.join(__dirname, '../../public/data/fig12/wall-kernel.json'), 'utf8'));
const dx = +process.argv[2], T = +(process.argv[3] || 30), dt = +(process.argv[4] || 0.005);
if (!(dx > 0)) throw new Error('usage: rest-gate.cjs <dx> [T] [dt]');
const f = new Fluid({ dx, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03, nu: 2.05e-6, wallFriction: process.env.FRICTION === '0' ? null : K, volumeCorrection: +(process.env.VC || 0), relax: +(process.env.RELAX || 0), flip: +(process.env.FLIP || 0), densityProjection: +(process.env.DP || 0), quadratic: process.env.Q === '1', whole: process.env.WHOLE === '1' });   // FRICTION=0: off; VC: volume correction (diagnosis)
const W = 2 * f.mp, I = dx * dx / 4, zc = () => { let s = 0; for (let p = 0; p < f.np; p++) s += f.pz[p]; return s / f.np; };
const ke = () => { let k = 0; for (let p = 0; p < f.np; p++) { let a = 0; for (let c = 0; c < 3; c++) a += f.pc[c][0][p] ** 2 + f.pc[c][1][p] ** 2 + f.pc[c][2][p] ** 2; k += f.pu[p] ** 2 + f.pv[p] ** 2 + f.pw[p] ** 2 + I * a; } return 0.5 * W * k; };
const z0 = zc(), t0 = Date.now(); let vmax = 0, zmax = 0; const K1 = [], K2 = [];
for (let n = 1; n * dt <= T + 1e-9; n++) {
  f.step(dt, 0, 0); const t = n * dt;
  if (t > 1) for (let p = 0; p < f.np; p++) { const v = f.pu[p] ** 2 + f.pv[p] ** 2 + f.pw[p] ** 2; if (v > vmax) vmax = v; }
  zmax = Math.max(zmax, Math.abs(zc() - z0));
  if (n % 20 === 0) { const k = ke(); if (t > 5 && t <= 15) K1.push(k); if (t > T - 10) K2.push(k); }
  if (n % 1000 === 0) { let b = -1, bv = 0; for (let p = 0; p < f.np; p++) { const v = f.pu[p] ** 2 + f.pv[p] ** 2 + f.pw[p] ** 2; if (v > bv) { bv = v; b = p; } }
    console.log(`  t ${t.toFixed(0)} s: centre of mass moved ${(1e6 * (zc() - z0)).toFixed(1)} um, kinetic ${(1e6 * ke()).toFixed(4)} uJ, fastest ${(1000 * Math.sqrt(bv)).toFixed(1)} mm/s at z ${(1000 * f.pz[b]).toFixed(1)} mm, r/R ${(Math.hypot(f.px[b], f.py[b]) / f.Rz(f.pz[b])).toFixed(2)}, particles ${f.np}`); }
}
const m = (a) => a.reduce((s, v) => s + v, 0) / a.length, k1 = m(K1), k2 = m(K2);
const checks = [[zmax < 20e-6, `centre of mass moved at most ${(1e6 * zmax).toFixed(1)} um (limit 20)`], [k2 < 0.1e-6, `kinetic energy, last 10 s: ${(1e6 * k2).toFixed(4)} uJ (limit 0.1)`],
  [Math.sqrt(vmax) < 0.005, `fastest particle after 1 s: ${(1000 * Math.sqrt(vmax)).toFixed(2)} mm/s (limit 5)`], [k2 <= 2 * k1, `kinetic energy, last 10 s / 5-15 s: ${(k2 / k1).toFixed(2)} (limit 2)`]];
console.log(`rest gate, tulip 125 mm, dx ${dx * 1000} mm, dt ${dt * 1000} ms, ${T} s (${((Date.now() - t0) / 1000).toFixed(0)} s to compute):`);
for (const [ok, msg] of checks) console.log((ok ? '  pass ' : '  FAIL ') + msg);
process.exit(checks.every((c) => c[0]) ? 0 : 1);
