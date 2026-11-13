// Fig. 12 in JAX: the built Kaggle page in headless Chromium at four widths, with the stored rides of public/data/fig12/2026-11-13/.
// For each width: errors, sideways scroll, the ride list, the frame rule (frame drawn = round(30 T)), and screenshots of the stage
// (and of the kerb ride at the head's spill). node notes/fig12/jax/page-test.cjs <out dir>
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/fig12-jax-page'; fs.mkdirSync(out, { recursive: true });
  const srv = spawn('node', [path.join(__dirname, '..', 'serve.cjs'), '8796'], { stdio: 'ignore' }); await new Promise((r) => setTimeout(r, 700));
  const b = await chromium.launch(); const errs = [];
  for (const W of [360, 390, 1024, 1440]) {
    const p = await b.newPage({ viewport: { width: W, height: W > 600 ? 900 : 800 }, deviceScaleFactor: 1 });
    p.on('pageerror', (e) => errs.push(W + ': ' + e.message)); p.on('console', (m) => { if (m.type() === 'error') errs.push(W + ': ' + m.text().slice(0, 200)); });
    await p.goto('http://localhost:8796/simulations/guinness-kaggle.html');
    await p.waitForFunction(() => window.GuinnessJax && document.getElementById('cap-t').textContent.startsWith('stored picture'), null, { timeout: 60000 });
    await p.waitForTimeout(2000);
    const s = await p.evaluate(() => ({ rides: GuinnessJax.files.map((f) => f.label), st: GuinnessJax.state(), cap: document.getElementById('cap-t').textContent,
      v: document.getElementById('r-v').textContent, sideways: document.documentElement.scrollWidth > innerWidth }));
    console.log(W + 'px', JSON.stringify(s));
    await p.locator('#stage').screenshot({ path: path.join(out, `resonant-${W}.png`) });
    if (W === 390 || W === 1440) {
      const i = await p.evaluate(() => GuinnessJax.files.findIndex((f) => f.path === 'ride_sharp30.json'));
      await p.evaluate((i) => GuinnessJax.choose(i), i);
      await p.waitForFunction(() => document.getElementById('cap-t').textContent.includes('ride_sharp30'), null, { timeout: 60000 });
      await p.evaluate(() => GuinnessJax.seek(26 / 30)); await p.waitForTimeout(400);
      const r = await p.evaluate(() => ({ st: GuinnessJax.state(), cap: document.getElementById('cap-t').textContent, s: document.getElementById('r-s').textContent, h: document.getElementById('r-h').textContent, d: document.getElementById('r-d').textContent }));
      console.log(W + 'px kerb', JSON.stringify(r));
      await p.locator('#stage').screenshot({ path: path.join(out, `kerb-${W}.png`) });
      await p.screenshot({ path: path.join(out, `page-${W}.png`), fullPage: false });
    }
    await p.close();
  }
  console.log('errors:', errs.length ? errs : 'none');
  await b.close(); srv.kill();
})();
