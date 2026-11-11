// The cart over one bump with the GPU solver (World.advanceGpu), in headless Chromium: the GPU counterpart of study.cjs and
// control.cjs.  node tools/fig12/gpu-study.cjs <bump mm> <off|speed|slosh> [batch n] [seconds] [ON s]
// The cart starts at x = 0.5 m at 1 m/s and crosses one cosine bump (centre 1 m, 25 cm long); batches of n fluid steps of 5 ms
// (n = 1: World.advance's coupling exactly; n = 4: what a 50 Hz frame needs). ON=t starts in open loop and switches the
// controller on at t. ROAD=washboard|isoC|... replaces the bumps (then <bump mm> is ignored), V0= sets the speed.
// Printed as study.cjs: the largest |front − back wall| (the lean), |a_x|, |a_z|, spilled mass, |A(3.200 Hz)| of a_x, the
// smallest tyre load; and the rms lean in the last second, the largest motor current. SERIES=file.json saves t, a_x, a_z,
// lean, probes' reading, estimate, current every batch. In this container the GPU is SwiftShader (CPU emulation).
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const fs = require('fs'), path = require('path');
const bump = +(process.argv[2] || 25) / 1000, ctrl = process.argv[3] || 'off', nB = +(process.argv[4] || 1), T = +(process.argv[5] || 2.3);
const ON = process.env.ON ? +process.env.ON : null, ROAD = process.env.ROAD || null, V0 = +(process.env.V0 || 1);
(async () => {
  const port = 8793, srv = spawn('node', [path.join(__dirname, '../../notes/fig12/serve.cjs'), String(port)], { stdio: 'ignore' });
  await new Promise((r) => setTimeout(r, 700));
  const b = await chromium.launch({ args: ['--enable-unsafe-webgpu', '--enable-features=Vulkan', '--use-vulkan=swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const page = await b.newPage(); const cons = [];
  page.on('pageerror', (e) => cons.push('page error: ' + e.message)); page.on('console', (m) => { if (m.type() === 'error') cons.push(m.text().slice(0, 300)); });
  await page.goto(`http://localhost:${port}/none`);
  for (const s of ['guinness-glass.js', 'stout-cart.js', 'stout-gpu.js']) await page.addScriptTag({ url: '/scripts/' + s });
  const r = await page.evaluate(async ({ bump, ctrl, nB, T, ON, ROAD, V0 }) => {
    const dev = await StoutGpu.GpuFluid.device(); if (!dev) return { error: 'no WebGPU device' };
    const G = GUINNESS_GLASS, f = new StoutGpu.GpuFluid({ dx: 0.004, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03 });
    await f.init(dev);
    const bumps = []; for (let n = 0; n < 60; n++) bumps.push({ x: 1.0 + 2 * n, h: bump, L: 0.25 });
    const road = { bumps, Rw: 0.04, xmin: -1, xmax: 125 };
    if (ROAD) { if (ROAD.indexOf('iso') === 0) { road.kind = 'iso'; road.cls = ROAD.slice(3); } else road.kind = ROAD; }
    const w = new StoutCart.World({ fluidInstance: f, road, cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: V0, ctrl: ON !== null ? 'off' : ctrl, susp: false }, dtMax: 1 / 200 });
    const Rs = f.Rz(Math.min(f.h0, f.zRim)), fS = 3.200, series = [];
    let dw = 0, tdw = 0, ax = 0, az = 0, re = 0, im = 0, Nmin = 1e9, imax = 0;
    const t0 = performance.now();
    while (w.t < T - 1e-9) {
      if (ON !== null && w.t >= ON - 1e-9 && w.cart.ctrl !== ctrl) w.cart.ctrl = ctrl;
      const per = await w.advanceGpu(nB / 200);
      const d = f.columnHeightAt(Rs, 0) - f.columnHeightAt(-Rs, 0);
      if (Math.abs(d) > Math.abs(dw)) { dw = d; tdw = w.t; }
      ax = Math.max(ax, Math.abs(w.lastAx)); az = Math.max(az, Math.abs(w.lastAz)); Nmin = Math.min(Nmin, w.cart.N); imax = Math.max(imax, Math.abs(w.cart.i));
      const ph = 2 * Math.PI * fS * w.t, hb = per.length / 200; re += w.lastAx * Math.cos(ph) * hb; im -= w.lastAx * Math.sin(ph) * hb;
      series.push([+w.t.toFixed(4), +w.lastAx.toFixed(4), +w.lastAz.toFixed(4), +(d * 1000).toFixed(3), +(2 * w.cart.probe.y * 1000).toFixed(3), +(2 * w.cart.obs.x[1] * 1000).toFixed(3), +w.cart.i.toFixed(4), +w.cart.x.toFixed(4)]);
    }
    const last = series.filter((s) => s[0] > T - 1), rms = Math.sqrt(last.reduce((a, s) => a + s[3] * s[3], 0) / Math.max(1, last.length));
    return { dw: Math.abs(dw) * 1000, tdw, ax, az, spill: (w.spilledMass || 0) * 1000, A: Math.hypot(re, im), Nmin, rms, imax, ms: (performance.now() - t0) / w.steps, steps: w.steps, errors: f.errors.slice(0, 3), series };
  }, { bump, ctrl, nB, T, ON, ROAD, V0 });
  if (r.error) console.log(r.error);
  else {
    const tag = `GPU ${ROAD ? 'road ' + ROAD : 'bump ' + (bump * 1000).toFixed(0) + ' mm'} at ${V0} m/s, ${ctrl}${ON !== null ? ' from ' + ON + ' s' : ''}, batch ${nB}`;
    console.log(`${tag}: dw ${r.dw.toFixed(1)} mm (t ${r.tdw.toFixed(2)} s); a_x ${r.ax.toFixed(2)} m/s^2; a_z ${r.az.toFixed(2)} m/s^2; spill ${r.spill.toFixed(1)} g; |A(3.200 Hz)| ${r.A.toFixed(4)} m/s; smallest tyre load ${r.Nmin.toFixed(2)} N; rms lean last second ${r.rms.toFixed(1)} mm; largest current ${r.imax.toFixed(2)} A; ${r.ms.toFixed(0)} ms a step; errors ${r.errors.length ? r.errors : 'none'}`);
    if (process.env.SERIES) fs.writeFileSync(process.env.SERIES, JSON.stringify({ tag, cols: ['t s', 'a_x m/s^2', 'a_z m/s^2', 'lean mm', 'probes mm', 'estimate mm', 'i A', 'x m'], rows: r.series }));
  }
  if (cons.length) console.log(cons.slice(0, 5));
  await b.close(); srv.kill();
})();
