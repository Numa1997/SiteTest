// The whole glass (the GPU solver, public/scripts/stout-gpu.js, in headless Chromium) shaken sideways: does the swing turn into a
// swirl? node tools/fig12/gpu-shake.cjs <A m/s^2> <f / f11> <T s> [fill mm]      OUT=file.json saves every step's swings
// a_x = A sin(2 pi f t), f = ratio x the grid's own f11 (3.200 Hz at 4 mm and 125 mm fill, tools/fig12/gpu-linearity.cjs; other
// fills: F11=<Hz>). Recorded every 5 ms step: the swing along the road, front minus back wall height at r = R(h) (theta = 0, pi), and
// across it (theta = pi/2, 3 pi/2): a swirl is a cross swing of the same order. Steps go in batches of up to 16 per submission.
// A real glass is never perfectly round, and the solver seeds both halves as mirror images: the run is given a seed, a sideways
// a_y = SEED sin(pi t/0.1) for t < 0.1 s (SEED = 0.02 m/s^2 by default: a cross swing of about 0.02 mm).
// In GitHub's runners and in this container Chromium has WebGPU only on SwiftShader (a CPU stand-in): slow but the same numbers.
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const fs = require('fs'), path = require('path');
const A = +(process.argv[2] || 0.3), ratio = +(process.argv[3] || 1), T = +(process.argv[4] || 1), h0 = +(process.argv[5] || 125) / 1000;
const F11 = +(process.env.F11 || 3.200), port = +(process.env.PORT || 8793), B = 16, SEED = process.env.SEED != null ? +process.env.SEED : 0.02;
(async () => {
  const srv = spawn('node', [path.join(__dirname, '../../notes/fig12/serve.cjs'), String(port)], { stdio: 'ignore' });
  await new Promise((r) => setTimeout(r, 700));
  const b = await chromium.launch({ args: ['--enable-unsafe-webgpu', '--enable-features=Vulkan', '--use-vulkan=swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const page = await b.newPage(); const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  await page.goto(`http://localhost:${port}/none`);
  for (const s of ['guinness-glass.js', 'stout-gpu.js']) await page.addScriptTag({ url: '/scripts/' + s });
  const r = await page.evaluate(async ({ A, ratio, T, h0, F11, B, SEED }) => {
    const dev = await StoutGpu.GpuFluid.device(); if (!dev) return { error: 'no WebGPU device' };
    const G = GUINNESS_GLASS, f = new StoutGpu.GpuFluid({ dx: 0.004, profile: G, h0, H: (G.R.length - 1) * G.dz + 0.03 });
    await f.init(dev);
    const Rs = f.Rz(Math.min(h0, f.zRim)), dt = 1 / 200, w = 2 * Math.PI * ratio * F11, rows = [], t0 = performance.now();
    let n = 0;
    while (n * dt < T - 1e-9) {
      const list = []; for (let k = 0; k < B && (n + k) * dt < T - 1e-9; k++) { const t = (n + k + 0.5) * dt; list.push({ dt, ax: A * Math.sin(w * t), az: 0, ay: t < 0.1 ? SEED * Math.sin(Math.PI * t / 0.1) : 0 }); }
      await f.steps(list); n += list.length;     // column counts are read back for the batch's last step
      rows.push([+(n * dt).toFixed(3), +((f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0)) * 1000).toFixed(3), +((f.columnHeightAt(0, Rs) - f.columnHeightAt(0, -Rs)) * 1000).toFixed(3), +(f.spilled * f.mp * 1000).toFixed(2)]);
    }
    return { rows, ms: (performance.now() - t0) / n, np: f.np, device: dev.gpuInfo, errors: f.errors.slice(0, 3) };
  }, { A, ratio, T, h0, F11, B, SEED });
  if (r.error) { console.log(r.error); process.exitCode = 1; }
  else {
    const tail = r.rows.filter((x) => x[0] > T * 0.75), mx = (k) => Math.max(...tail.map((x) => Math.abs(x[k])));
    console.log(`gpu shake A ${A} m/s^2 at ${ratio} f11 (${(ratio * F11).toFixed(3)} Hz), fill ${h0 * 1000} mm, ${T} s: last quarter, along ${mx(1).toFixed(1)} mm, across ${mx(2).toFixed(1)} mm (lean); spilled ${r.rows[r.rows.length - 1][3]} g; ${r.ms.toFixed(0)} ms a step on ${r.device.vendor}/${r.device.architecture}; errors ${r.errors.length ? r.errors : 'none'}${errs.length ? '; page ' + errs.slice(0, 2) : ''}`);
    if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify({ A, ratio, T, h0, F11, cols: ['t s', 'along mm', 'across mm', 'spilled g'], rows: r.rows, ms: r.ms }));
  }
  await b.close(); srv.kill();
})();
