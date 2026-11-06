// Fig. 12, part 1: the 3D stout set swinging in open loop by the 25 mm bump at 1 m/s, then the slosh feedback (probes, Kalman filter, LQR)
// switched on at 1.0 s simulated; screenshots before the switch and 1.5 s after, at 1280 and 390 px (deviceScaleFactor 2), and
// the lean the probes read. node notes/fig12/calm-shots.cjs <out-dir> [base-url] (serve.cjs for threads); QUERY='' for the live model.
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || 'notes/fig12/shots', base = process.argv[3] || 'http://localhost:8790', q = process.env.QUERY != null ? process.env.QUERY : '?grid=4';
  require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(), errs = [];
  for (const [name, vp] of [['1280', { width: 1280, height: 900 }], ['390', { width: 390, height: 844 }]]) {
    const p = await b.newPage({ viewport: vp, deviceScaleFactor: 2 });
    p.on('pageerror', (e) => errs.push(e.message)); p.on('console', (m) => { if (m.type() === 'error' && !/cloudflareinsights/.test(m.text())) errs.push(m.text()); });
    await p.goto(base + '/simulations/beer-slosh.html' + q); await p.waitForTimeout(500);
    await p.evaluate(() => { const s = document.getElementById('bumpH'); s.value = 25; s.dispatchEvent(new Event('input')); document.getElementById('ctrl-off').click(); document.getElementById('reset').click(); });
    await p.waitForFunction(() => Fig12.world.t > 1.0, null, { timeout: 120000, polling: 'raf' });
    await p.locator('.stage').screenshot({ path: `${out}/calm-${name}-before.png` });
    const before = await p.evaluate(() => ({ t: Fig12.world.t, lean: 2000 * Fig12.world.cart.probe.y }));
    await p.click('#ctrl-slosh'); await p.evaluate(() => { window.__max = 0; window.__t0 = Fig12.world.t; });
    await p.waitForFunction(() => { const w = Fig12.world; if (w.t > window.__t0 + 1) window.__max = Math.max(window.__max, Math.abs(2000 * w.cart.probe.y)); return w.t > window.__t0 + 1.5; }, null, { timeout: 180000, polling: 'raf' });
    await p.locator('.stage').screenshot({ path: `${out}/calm-${name}-after.png` });
    const r = await p.evaluate(() => ({ t: Fig12.world.t, lean: 2000 * Fig12.world.cart.probe.y, maxLate: window.__max, rate: document.getElementById('cap-rate').textContent, sx: document.documentElement.scrollWidth > innerWidth }));
    console.log(`${name} px: lean ${before.lean.toFixed(1)} mm at ${before.t.toFixed(2)} s (open loop); slosh feedback on; ${r.lean.toFixed(1)} mm at ${r.t.toFixed(2)} s, largest |lean| in its last 0.5 s ${r.maxLate.toFixed(1)} mm; caption "${r.rate}"; sideways scroll ${r.sx}`);
    await p.close();
  }
  console.log('errors: ' + (errs.length ? errs.join(' | ') : 'none'));
  await b.close();
})();
