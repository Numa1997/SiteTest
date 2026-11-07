// Fig. 12 with the GPU solver, in headless Chromium with WebGPU (SwiftShader here): the page starts on the graphics chip, runs,
// shows no errors, and draws the stout. node notes/fig12/gpu-page-test.cjs [out dir] [seconds of simulated time]
// Screenshots at 1280 and 390 px, deviceScaleFactor 2. Prints the model, the rate, the readouts, errors.
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/fig12-gpu'; fs.mkdirSync(out, { recursive: true });
  const T = +(process.argv[3] || 0.3);
  const srv = spawn('node', [path.join(__dirname, 'serve.cjs'), '8795'], { stdio: 'ignore' }); await new Promise((r) => setTimeout(r, 700));
  const b = await chromium.launch({ args: ['--enable-unsafe-webgpu', '--enable-features=Vulkan', '--use-vulkan=swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const errs = [];
  for (const W of [1280, 390]) {
    const p = await b.newPage({ viewport: { width: W, height: W > 600 ? 900 : 844 }, deviceScaleFactor: 2 });
    p.on('pageerror', (e) => errs.push(W + ': ' + e.message)); p.on('console', (m) => { if (m.type() === 'error') errs.push(W + ': ' + m.text().slice(0, 300)); });
    await p.goto('http://localhost:8795/simulations/beer-slosh.html' + (process.env.QUERY || ''));
    await p.waitForFunction(() => window.Fig12 && window.Fig12.world && Fig12.world.t > 0, null, { timeout: 120000, polling: 200 });
    await p.waitForFunction((T) => Fig12.world.t >= T, T, { timeout: 600000, polling: 500 });
    await p.click('#play'); await p.waitForFunction(() => !Fig12.busy(), null, { timeout: 60000, polling: 100 });
    const r = await p.evaluate(() => ({ gpu: Fig12.gpu, t: Fig12.world.t, x: Fig12.world.cart.x, np: Fig12.world.fluid.np, cap: document.getElementById('cap-model').textContent, rate: document.getElementById('cap-rate').textContent, solver: document.getElementById('r-solver').textContent, lean: document.getElementById('r-dw').textContent, sideways: document.documentElement.scrollWidth > innerWidth, errors: Fig12.world.fluid.errors || [] }));
    console.log(W + 'px', JSON.stringify(r));
    await p.locator('#stage').screenshot({ path: path.join(out, 'gpu-' + W + '.png') });
    await p.close();
  }
  console.log('errors:', errs.length ? errs : 'none');
  await b.close(); srv.kill();
})();
