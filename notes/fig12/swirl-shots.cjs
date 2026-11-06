// Fig. 12, part 2: the nonlinear live model shaken along the road at its own frequency (the cart held on a flat road, the
// glass's acceleration a_x = 0.6 sin(2 pi f11 t) applied by a hand-free push of M_x a_x), until it swirls; screenshots at
// 1280 and 390 px when the sideways swing s1 has grown. node notes/fig12/swirl-shots.cjs <out-dir> [base-url]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || 'notes/fig12/shots', base = process.argv[3] || 'http://localhost:8790';
  require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(), errs = [];
  for (const [name, vp] of [['1280', { width: 1280, height: 900 }], ['390', { width: 390, height: 844 }]]) {
    const p = await b.newPage({ viewport: vp, deviceScaleFactor: 2 });
    p.on('pageerror', (e) => errs.push(e.message)); p.on('console', (m) => { if (m.type() === 'error' && !/cloudflareinsights/.test(m.text())) errs.push(m.text()); });
    await p.goto(base + '/simulations/beer-slosh.html'); await p.waitForTimeout(500);
    await p.evaluate(() => { const s = document.getElementById('bumpH'); s.value = 0; s.dispatchEvent(new Event('input')); document.getElementById('ctrl-off').click(); document.getElementById('reset').click(); });
    // shake: the page's clock calls world.advance; wrap it so each fluid step sees a sinusoidal push on the cart
    await p.evaluate(() => { const w = Fig12.world, f = w.fluid, f11 = f.w[0] / 2 / Math.PI, adv = w.advance.bind(w);
      w.advance = (dt) => { const n = Math.max(1, Math.ceil(dt / 0.005)); for (let k = 0; k < n; k++) { w.cart.pushF = w.cart.massX() * 0.6 * Math.sin(2 * Math.PI * 0.99 * f11 * w.t); adv(dt / n); } }; });
    await p.waitForFunction(() => Math.abs(Fig12.world.fluid.s1) > 0.012 && Math.abs(Fig12.world.fluid.s1) > 0.6 * Math.abs(Fig12.world.fluid.q[0]), null, { timeout: 120000, polling: 'raf' });
    await p.waitForTimeout(200);
    await p.locator('.stage').screenshot({ path: `${out}/swirl-${name}.png` });
    const r = await p.evaluate(() => ({ t: Fig12.world.t, q1: Fig12.world.fluid.q[0] * 1000, s1: Fig12.world.fluid.s1 * 1000, rate: document.getElementById('cap-rate').textContent }));
    console.log(`${name} px: swirl at ${r.t.toFixed(1)} s: q1 ${r.q1.toFixed(1)} mm, s1 ${r.s1.toFixed(1)} mm; caption "${r.rate}"`);
    await p.close();
  }
  console.log('errors: ' + (errs.length ? errs.join(' | ') : 'none'));
  await b.close();
})();
