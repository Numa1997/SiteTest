// The GPU solver (public/scripts/stout-gpu.js) from rest, in headless Chromium, the same experiment as linearity.cjs:
//   node tools/fig12/gpu-linearity.cjs A1,A2,... [Tp s] [T s]          OUT=file.json saves the lean every step (linfit.cjs reads it)
//   REST=1 node tools/fig12/gpu-linearity.cjs 0 1 1                      the stout left alone: fastest particle, drift of the surface
//   TILT=2 node tools/fig12/gpu-linearity.cjs 0 0 5.5                    a steady push of 2 m/s^2, ramped in over 2 s as (1 - cos)/2: the static tilt
// The glass is at rest at t = 0 and gets a_x(t) = A sin(pi t / Tp) for t < Tp, nothing after (no cart). Printed: the largest lean
// (front − back wall height at r = R(h), as linearity.cjs), the free swing's frequency from zero crossings, the spill, the
// pressure solve's iterations, the fastest particle, the time per step, and the device. With TILT the centre of mass of the
// liquid along x averaged over 2.5–5.5 s, every other step (from the particle positions read back; check.cjs's protocol for the
// processor, note section 12), against the exact −0.877 mm of note §3.5.
// In this container Chromium has WebGPU only on SwiftShader (a CPU emulation of a GPU): the numbers are the solver's, the
// time per step says nothing about a real graphics chip.
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const fs = require('fs'), path = require('path');
const amps = (process.argv[2] || '1').split(',').map(Number), Tp = +(process.argv[3] || 0.3), T = +(process.argv[4] || 2.0);
const TILT = process.env.TILT ? +process.env.TILT : null;
(async () => {
  const port = 8792, srv = spawn('node', [path.join(__dirname, '../../notes/fig12/serve.cjs'), String(port)], { stdio: 'ignore' });
  await new Promise((r) => setTimeout(r, 700));
  const b = await chromium.launch({ args: ['--enable-unsafe-webgpu', '--enable-features=Vulkan', '--use-vulkan=swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const page = await b.newPage(); const cons = [];
  page.on('pageerror', (e) => cons.push('page error: ' + e.message));
  await page.goto(`http://localhost:${port}/none`);           // any page of the site's origin (a secure context)
  for (const s of ['guinness-glass.js', 'stout-gpu.js']) await page.addScriptTag({ url: '/scripts/' + s });
  const out = [];
  for (const A of amps) {
    const r = await page.evaluate(async ({ A, Tp, T, TILT }) => {
      const dev = await StoutGpu.GpuFluid.device(); if (!dev) return { error: 'no WebGPU device' };
      const G = GUINNESS_GLASS, f = new StoutGpu.GpuFluid({ dx: 0.004, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03 });
      await f.init(dev);
      const Rs = f.Rz(Math.min(f.h0, f.zRim)), dt = 1 / 200, series = [], cross = [], com = [];
      let lean = 0, tl = 0, prev = null, itSum = 0, vmax = 0;
      const t0 = performance.now();
      for (let n = 0; n * dt < T - 1e-9; n++) {
        const t = n * dt, ax = TILT !== null ? (t < 2 ? TILT * 0.5 * (1 - Math.cos(Math.PI * t / 2)) : TILT) : t < Tp ? A * Math.sin(Math.PI * t / Tp) : 0;
        await f.steps([{ dt, ax, az: 0 }]);
        itSum += f.cgIters; vmax = Math.max(vmax, f.vmax);
        const d = f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0), tt = t + dt;
        series.push([+tt.toFixed(3), +(d * 1000).toFixed(2), +(f.vmax * 1000).toFixed(2)]);
        if (Math.abs(d) > Math.abs(lean)) { lean = d; tl = tt; }
        if (tt > Tp + 0.1 && prev !== null && Math.sign(d) !== Math.sign(prev) && prev !== 0) cross.push(tt - dt * d / (d - prev));
        prev = d;
        if (TILT !== null && tt > 2.5 - 1e-9 && n % 2 === 0) { await f.readPositions(); let s = 0; for (let p = 0; p < f.nRead; p++) s += f.px[p]; com.push(s / f.nRead); }
      }
      const ms = (performance.now() - t0) / series.length;
      const fr = cross.length > 2 ? (cross.length - 1) / (2 * (cross[cross.length - 1] - cross[0])) : NaN;
      return { A, lean_mm: +(lean * 1000).toFixed(1), t_s: +tl.toFixed(3), f_Hz: +fr.toFixed(3), spill_g: +(f.spilled * f.mp * 1000).toFixed(1), np0: f.npStart, np: f.np,
        cg_mean: +(itSum / series.length).toFixed(1), vmax_mm_s: +(vmax * 1000).toFixed(1), ms_per_step: +ms.toFixed(0), com_mm: com.length ? +(1000 * com.reduce((a, c) => a + c, 0) / com.length).toFixed(3) : null,
        device: dev.gpuInfo, errors: f.errors.slice(0, 3), series };
    }, { A, Tp, T, TILT });
    if (r.error) { console.log(r.error); break; }
    out.push(r);
    console.log(`gpu A ${A} m/s^2${TILT !== null ? ` (steady ${TILT} m/s^2)` : ''}: lean ${r.lean_mm} mm at ${r.t_s} s; free swing ${r.f_Hz} Hz; spill ${r.spill_g} g; particles ${r.np0} -> ${r.np}; CG ${r.cg_mean} it.; fastest particle ${r.vmax_mm_s} mm/s` +
      (r.com_mm !== null ? `; centre of mass x over 2.5–5.5 s ${r.com_mm} mm` : '') + `; ${r.ms_per_step} ms a step on ${r.device.vendor}/${r.device.architecture}; errors ${r.errors.length ? r.errors : 'none'}`);
  }
  if (cons.length) console.log(cons.slice(0, 5));
  if (process.env.OUT) fs.writeFileSync(process.env.OUT, JSON.stringify({ model: 'gpu', Tp, T, out }));
  await b.close(); srv.kill();
})();
