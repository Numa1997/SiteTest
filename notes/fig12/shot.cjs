// render the catalog thumbnail of Fig. 12: the side view as the passive cart's head runs over the rim after the bump, 800 x 500
// node notes/fig12/shot.cjs out.png
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch();
  const pg = await (await b.newContext({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1 })).newPage();
  await pg.goto('http://localhost:8765/simulations/beer-slosh.html', { waitUntil: 'networkidle' }); await pg.waitForFunction(() => window.SLOSH && window.SLOSH.cartMap); await pg.waitForTimeout(400);
  await pg.evaluate(() => { const S = window.SLOSH; document.getElementById('play').click(); document.querySelector('#law button[data-v="passive"]').click(); document.querySelector('#road button[data-v="bump"]').click(); S.restart(); for (let i = 0; i < 1150; i++) S.step(); document.getElementById('stage-cart').scrollIntoView(); });
  await pg.waitForTimeout(300);
  const c = await pg.$('#cart'); const box = await c.boundingBox();
  const w = box.width, h = Math.min(box.height, w * 500 / 800), y0 = box.y + (box.height - h) / 2;
  await pg.screenshot({ path: out, clip: { x: box.x, y: y0, width: w, height: h } });
  console.log('thumb', w, h); await b.close();
})();
