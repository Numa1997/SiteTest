// Offline checks of the stout solver (node tools/fig12/check.cjs). Every number printed is measured.
const fs = require('fs'), path = require('path'); const mod = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts/stout-cart.js'), 'utf8'))(mod); const { Fluid } = mod.exports;
const which = process.argv[2] || 'all';
const dt = 1 / 400;
function wallDiff(f) { const xr = 0.8 * f.R; return f.surfaceHeight(xr, 0) - f.surfaceHeight(-xr, 0); }

if (which === 'all' || which === 'rest') {
  const f = new Fluid(); const t0 = Date.now();
  for (let n = 0; n < 400; n++) f.step(dt, 0, 0);
  const ms = (Date.now() - t0) / 400;
  console.log(`rest: particles ${f.np}, grid ${f.nx}x${f.ny}x${f.nz}, ${ms.toFixed(1)} ms/step, max speed after 1 s ${(f.maxSpeed()*1000).toFixed(2)} mm/s, ` +
    `centre height ${(f.surfaceHeight(0,0)*1000).toFixed(2)} mm (h0 = 60 mm), CG iters ${f.cgIters}`);
}
if (which === 'all' || which === 'freq') {
  const f = new Fluid();
  for (let n = 0; n < 120; n++) f.step(dt, 0, 0);         // settle 0.3 s
  const ts = [], ds = [];
  for (let n = 0; n < 1400; n++) {
    const t = n * dt, ax = t < 0.05 ? 1.5 : 0;            // a short push, then free sloshing
    f.step(dt, ax, 0);
    if (n % 2 === 0) { ts.push(t); ds.push(wallDiff(f)); }
  }
  const cross = [];
  for (let i = 1; i < ds.length; i++) if (t0ok(ts[i]) && ds[i - 1] < 0 && ds[i] >= 0) cross.push(ts[i - 1] + (ts[i] - ts[i - 1]) * (-ds[i - 1]) / (ds[i] - ds[i - 1]));
  function t0ok(t) { return t > 0.15; }
  const T = (cross[cross.length - 1] - cross[0]) / (cross.length - 1);
  const xi = 1.8412, R = f.R, h = f.h0, fLin = Math.sqrt(9.81 * xi / R * Math.tanh(xi * h / R)) / (2 * Math.PI);
  let peaks = []; for (let i = 1; i < ds.length - 1; i++) if (ds[i] > ds[i-1] && ds[i] >= ds[i+1] && ts[i] > 0.15) peaks.push(ds[i]);
  console.log(`free slosh: ${cross.length} up-crossings, measured f = ${(1/T).toFixed(3)} Hz; linear potential theory f11 = ${fLin.toFixed(3)} Hz; ` +
    `wall-to-wall difference peaks (mm): ${peaks.slice(0,8).map(p => (p*1000).toFixed(2)).join(' ')}`);
}
if (which === 'all' || which === 'tilt') {
  const f = new Fluid(); const A = 2.0;
  const sl = [];
  for (let n = 0; n < 1200; n++) {
    const t = n * dt, ax = A * Math.min(1, t / 0.4);
    f.step(dt, ax, 0);
    if (t > 1.5 && n % 4 === 0) { const xr = 0.6 * f.R; sl.push((f.surfaceHeight(xr, 0) - f.surfaceHeight(-xr, 0)) / (2 * xr)); }
  }
  const m = sl.reduce((a, b) => a + b, 0) / sl.length;
  console.log(`steady push a = ${A} m/s^2: mean surface slope ${m.toFixed(4)} (exact for a fluid at rest in the glass: -a/g = ${(-A/9.81).toFixed(4)})`);
}
