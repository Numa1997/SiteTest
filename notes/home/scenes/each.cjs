// Screenshot every scene of scenes.html after it has run for T s in view. node notes/home/scenes/each.cjs [width]
const { chromium } = require('playwright'); const w = +(process.argv[2] || 1600), T = +(process.env.T || 6);
(async () => { const b = await chromium.launch(), p = await b.newPage({ viewport: { width: w, height: 1000 } }), errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8766/scenes.html', { waitUntil: 'networkidle' });
  for (const id of await p.$$eval('.scn', a => a.map(e => e.id))) { const el = await p.$('#' + id + ' .scn__stage'); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(T * 1000);
    await el.screenshot({ path: `notes/home/scenes/after/scene-${id}-${w}.png` }); }
  console.log('errors', errs.length, await p.$eval('[data-stored=coupled]', e => e.textContent)); await b.close(); })();
