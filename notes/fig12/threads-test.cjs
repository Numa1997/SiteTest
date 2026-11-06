// Fig. 12 with worker threads, in Chromium: the threaded solver must give the same numbers as the single-thread one, to the
// last digit, and the page must say how many threads it uses. node notes/fig12/threads-test.cjs [base URL] [dx]
// Without a base URL it serves public/ itself with the isolation headers (notes/fig12/serve.cjs).
const { chromium } = require('playwright'), { spawn, execFileSync } = require('child_process'), path = require('path');
(async () => {
  let base = process.argv[2], srv = null; const dx = +(process.argv[3] || 0.004);
  if (!base) { srv = spawn('node', [path.join(__dirname, 'serve.cjs'), '8791'], { stdio: 'ignore' }); await new Promise(r => setTimeout(r, 800)); base = 'http://localhost:8791'; }
  const node = execFileSync('node', [path.join(__dirname, '../../tools/fig12/same.cjs'), String(dx)]).toString().trim();
  const b = await chromium.launch(); const pg = await b.newPage(); const errors = [];
  pg.on('pageerror', e => errors.push(String(e))); pg.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await pg.goto(base + '/simulations/beer-slosh.html'); await pg.waitForTimeout(1500);
  const info = await pg.evaluate(() => ({ isolated: window.crossOriginIsolated, cpus: navigator.hardwareConcurrency, threads: window.Fig12.pool ? window.Fig12.pool.P : 1, attached: !!window.Fig12.world.fluid.pool, readout: document.getElementById('r-solver').textContent }));
  console.log('page:', JSON.stringify(info));
  const run = (threaded) => pg.evaluate(async ([dx, threaded]) => {
    const G = GUINNESS_GLASS, pool = window.Fig12.pool;
    const f = new StoutCart.Fluid({ dx, profile: G, h0: 0.125, H: G.R.length * G.dz + 0.03, shared: threaded });
    if (threaded) { pool.attach(f); for (let i = 0; i < 100 && !f.pool; i++) await new Promise(r => setTimeout(r, 20)); if (!f.pool) return 'pool did not attach'; }
    let it = 0; const t0 = performance.now();
    for (let n = 0; n < 200; n++) { f.step(1 / 200, n < 24 ? 25 * Math.sin(Math.PI * n / 24) : 0, n < 24 ? 3 : 0); it += f.cgIters; }
    const ms = (performance.now() - t0) / 200;
    const parts = [f.px, f.py, f.pz, f.pu, f.pv, f.pw].map(a => a.slice(0, f.np)).concat([f.phi.slice(), f.q.slice()]);
    const bytes = new Uint8Array(parts.reduce((s, a) => s + a.byteLength, 0)); let o = 0;
    for (const a of parts) { bytes.set(new Uint8Array(a.buffer), o); o += a.byteLength; }
    const h = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))).map(x => x.toString(16).padStart(2, '0')).join('').slice(0, 16);
    if (threaded) pool.attach(window.Fig12.world.fluid);
    return { line: `np ${f.np}, spilled ${f.spilled}, CG iterations ${it}, x[0] ${f.px[0]}, u[0] ${f.pu[0]}, sha256 ${h}`, ms };
  }, [dx, threaded]);
  const one = await run(false), many = await run(true);
  console.log('node      ', node);
  console.log('1 thread  ', one.line, `(${one.ms.toFixed(2)} ms per step)`);
  console.log(info.threads + ' threads ', many.line, `(${many.ms.toFixed(2)} ms per step)`);
  console.log('identical:', one.line === node && many.line === node);
  await pg.waitForTimeout(500);
  console.log('page after:', await pg.evaluate(() => ({ attached: !!window.Fig12.world.fluid.pool, readout: document.getElementById('r-solver').textContent })));
  console.log('errors:', errors.length ? errors : 'none');
  await b.close(); if (srv) srv.kill();
})();
