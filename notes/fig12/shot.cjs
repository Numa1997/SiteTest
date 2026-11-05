// render the catalog thumbnail of Fig. 12: the cart mid-bump under the LQR, 800 x 500
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1 })).newPage();
  await pg.goto('http://localhost:8765/simulations/beer-slosh.html', { waitUntil: 'networkidle' }); await pg.waitForFunction(() => window.SLOSH3D, { timeout: 60000 }); await pg.waitForTimeout(600);
  await pg.evaluate(() => { const S = window.SLOSH; document.getElementById('play').click(); document.querySelector('#law button[data-v="passive"]').click(); document.querySelector('#road button[data-v="bump"]').click(); S.restart(); for (let i = 0; i < 1150; i++) S.step(); const V = window.SLOSH3D.view; V.az = -0.95; V.el = 0.3; V.dist = 1.8; window.SLOSH3D.placeCam(); window.SLOSH3D.render(); });
  await pg.waitForTimeout(300); await pg.evaluate(() => window.SLOSH3D.render());
  const c = await pg.$('#stage3d canvas'); await c.scrollIntoViewIfNeeded(); await pg.waitForTimeout(300); await pg.evaluate(() => window.SLOSH3D.render()); const box = await c.boundingBox();
  const w = box.width, h = w * 500 / 800, y0 = box.y + (box.height - h) / 2;
  await pg.screenshot({ path: out, clip: { x: box.x, y: y0, width: w, height: h } });
  console.log('thumb', w, h); await b.close();
})();
