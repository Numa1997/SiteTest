// what the pointer looks like over each part of the figure, the hand mark while dragging, and the layout at common screens
const { chromium } = require('playwright'); const path = require('path');
const ROOT = process.env.ROOT || '/home/user/SiteTest';
(async () => { const b = await chromium.launch();
  for (const [w, h] of [[1366, 768], [1440, 900], [1920, 1080], [390, 844]]) {
    const pg = await b.newPage({ viewport: { width: w, height: h } }), errs = []; pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('file://' + ROOT + '/public/simulations/double-inverted-pendulum.html'); await pg.waitForTimeout(2500);
    await pg.evaluate(() => document.getElementById('stage').scrollIntoView({ block: 'start' })); await pg.waitForTimeout(500);
    const box = await (await pg.$('#cv')).boundingBox(), trb = await (await pg.$('#tr')).boundingBox(), g = await pg.evaluate(() => DIPC.geo);
    const cur = async (x, y) => { await pg.mouse.move(box.x + x, box.y + y); await pg.waitForTimeout(60); return pg.evaluate(() => getComputedStyle(document.getElementById('cv')).cursor); };
    const c = { empty: await cur(30, 60), cart: await cur(g.hx, g.hy + 12), rod: await cur((g.ex + g.tx) / 2, (g.ey + g.ty) / 2) };
    await pg.mouse.move(box.x + g.hx, box.y + g.hy + 12); await pg.mouse.down(); c.held = await pg.evaluate(() => getComputedStyle(document.getElementById('cv')).cursor);
    for (let i = 1; i <= 12; i++) { await pg.mouse.move(box.x + g.hx + 10 * i, box.y + g.hy + 12); await pg.waitForTimeout(25); }
    await pg.waitForTimeout(250); const hp = await pg.evaluate(() => ({ hand_px: DIPC.ds.get('hand_px'), check: Sim.data.check.hand_px().value }));
    await pg.screenshot({ path: path.join(__dirname, `cur-${w}x${h}.png`) });
    await pg.mouse.up(); await pg.waitForTimeout(100); c.after = await pg.evaluate(() => getComputedStyle(document.getElementById('cv')).cursor);
    const fit = { figure: [Math.round(box.width), Math.round(box.height)], trace: Math.round(trb.height), bothOnScreen: trb.y + trb.height <= h, sc: +(await pg.evaluate(() => DIPC.ds.get('sc'))).toFixed(0), railVisible_m: +(box.width / await pg.evaluate(() => DIPC.ds.get('sc'))).toFixed(1) };
    console.log(w + 'x' + h, JSON.stringify({ cursor: c, hand: hp, fit, pointerAtPx: +(box.x + g.hx + 120 - box.x).toFixed(0) }), 'errors', errs.join('|') || 'none'); await pg.close(); }
  await b.close(); })();
