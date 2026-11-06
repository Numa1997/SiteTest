// Fig. 12, the live model: the same 25 mm bump at 1 m/s with each controller, screenshot after 2.6 s (deviceScaleFactor 2),
// and the largest lean the page read. node notes/fig12/ctrl-shots.cjs <out-dir> <base-url>
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || 'notes/fig12', base = process.argv[3] || 'http://localhost:8790';
  const b = await chromium.launch(), errs = [];
  for (const [name, vp] of [['desktop', { width: 1280, height: 900 }], ['phone', { width: 390, height: 844 }]]) {
    const p = await b.newPage({ viewport: vp, deviceScaleFactor: 2 });
    p.on('pageerror', (e) => errs.push(e.message)); p.on('console', (m) => { if (m.type() === 'error' && !/cloudflareinsights/.test(m.text())) errs.push(m.text()); });
    await p.goto(base + '/simulations/beer-slosh.html'); await p.waitForTimeout(800);
    for (const c of ['off', 'speed', 'preview', 'slosh']) {
      if (name === 'phone' && c !== 'slosh' && c !== 'off') continue;
      await p.evaluate((c) => { const s = document.getElementById('bumpH'); s.value = 25; s.dispatchEvent(new Event('input')); document.getElementById('ctrl-' + c).click(); document.getElementById('reset').click(); window.__lean = 0; }, c);
      await p.waitForFunction(() => { const f = Fig12.world.fluid, l = Math.abs(f.columnHeightAt(f.Rz(f.h0), 0) - f.columnHeightAt(-f.Rz(f.h0), 0)); window.__lean = Math.max(window.__lean, l); return Fig12.world.t > 2.6; }, null, { timeout: 60000, polling: 'raf' });
      const r = await p.evaluate(() => ({ t: Fig12.world.t.toFixed(2), lean: (window.__lean * 1000).toFixed(1), spilled: ((Fig12.world.spilledMass || 0) * 1000).toFixed(1), rate: document.getElementById('cap-rate').textContent }));
      console.log(name, c, JSON.stringify(r));
      await (await p.$('figure.stage')).screenshot({ path: `${out}/live-${name}-${c}.png` });
    }
    await p.close();
  }
  console.log('errors:', errs.length ? errs.join('\n') : 'none'); await b.close();
})();
