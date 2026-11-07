// Project 06: grab the cart in still water, drag it 0.3 m in 1 s, hold 1 s, let go; every 0.2 s: t, held, mode, x, θ1, θ2 (deg, not wrapped: whole turns show), and the supervisor log.
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1100, height: 900 } });
  await pg.goto('http://localhost:8765/simulations/rods-in-liquid.html', { waitUntil: 'load' }); await pg.waitForTimeout(4000);
  const box = await pg.$eval('#cv', e => { const r = e.getBoundingClientRect(); return { x: r.left, y: r.top }; });
  const at = await pg.evaluate(() => ({ x: DIPC.ds.get('cart_px'), y: DIPC.ds.get('cart_py'), h: DIPC.ds.get('cart_h'), sc: DIPC.ds.get('sc') }));
  const x0 = box.x + at.x + at.h, y0 = box.y + at.y + at.h / 2; await pg.mouse.move(x0, y0); await pg.mouse.down();
  const rec = async (tag) => console.log(tag, await pg.evaluate(() => [DIPC.t.toFixed(2), DIPC.held, DIPC.mode, DIPC.s[0].toFixed(2), (DIPC.s[1] * 57.3).toFixed(1), (DIPC.s[2] * 57.3).toFixed(1), DIPC.log.length].join(' ')));
  for (let k = 1; k <= 20; k++) { await pg.mouse.move(x0 + 0.3 * at.sc * k / 20, y0); await pg.waitForTimeout(50); if (k % 5 === 0) await rec('drag'); }
  for (let k = 0; k < 5; k++) { await pg.waitForTimeout(200); await rec('hold'); }
  await pg.mouse.up(); for (let k = 0; k < 15; k++) { await pg.waitForTimeout(200); await rec('rel'); }
  console.log(JSON.stringify(await pg.evaluate(() => DIPC.log))); await b.close(); })();
