// Fig. 12, part 3: the live model on a rough road with each controller; screenshots after a set simulated time and what spilled.
// node notes/fig12/road-shots.cjs <out-dir> [base-url] [road=washboard] [seconds=5]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || 'notes/fig12/shots', base = process.argv[3] || 'http://localhost:8790', road = process.argv[4] || 'washboard', T = +(process.argv[5] || 5);
  require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch(), errs = [];
  for (const [name, vp] of [['1280', { width: 1280, height: 900 }], ['390', { width: 390, height: 844 }]]) {
    const p = await b.newPage({ viewport: vp, deviceScaleFactor: 2 });
    p.on('pageerror', (e) => errs.push(e.message)); p.on('console', (m) => { if (m.type() === 'error' && !/cloudflareinsights/.test(m.text())) errs.push(m.text()); });
    await p.goto(base + '/simulations/beer-slosh.html'); await p.waitForTimeout(500);
    for (const c of ['off', 'slosh']) {
      await p.selectOption('#roadKind', road);
      await p.evaluate((c) => { document.getElementById('ctrl-' + c).click(); document.getElementById('reset').click(); }, c);
      await p.waitForFunction((T) => Fig12.world.t > T, T, { timeout: 120000, polling: 'raf' });
      await p.locator('.stage').screenshot({ path: `${out}/road-${road}-${c}-${name}.png` });
      const r = await p.evaluate(() => ({ t: Fig12.world.t, sp: (Fig12.world.spilledMass || 0) * 1000, lean: 2000 * Fig12.world.cart.probe.y, sx: document.documentElement.scrollWidth > innerWidth }));
      console.log(`${name} px, ${road}, ${c}: at ${r.t.toFixed(1)} s spilled ${r.sp.toFixed(1)} g, lean now ${r.lean.toFixed(1)} mm; sideways scroll ${r.sx}`);
    }
    await p.close();
  }
  console.log('errors: ' + (errs.length ? errs.join(' | ') : 'none'));
  await b.close();
})();
