// Drag the cart with a real mouse in headless Chromium: the motor lets go, the rods fall under the cart's motion alone,
// every hand step is recomputed from the store (force from (29)+(30), RK4 replay), the energy book balances, and after
// the release the controller takes over. ROOT selects the checkout; LANG '' | 'de/' | 'ar/'.
'use strict';
const { chromium } = require('playwright'); const path = require('path');
const ROOT = process.env.ROOT, LANG = process.env.LANG2 || '';
(async () => {
  const b = await chromium.launch(), pg = await b.newPage({ viewport: { width: 1280, height: 900 } }), errs = []; pg.on('pageerror', (e) => errs.push(e.message));
  await pg.goto('file://' + path.join(ROOT, 'public', LANG, 'simulations/double-inverted-pendulum.html')); await pg.waitForTimeout(2500);
  await pg.evaluate(() => DIPC.finishCatch());
  const cv = await pg.$('#cv'); await cv.scrollIntoViewIfNeeded(); await pg.waitForTimeout(800);
  const box = await cv.boundingBox(), geo = await pg.evaluate(() => DIPC.geo);
  const x0 = box.x + geo.hx, y0 = box.y + geo.hy + 12;
  const log = [];
  const snap = async (tag) => log.push(Object.assign({ tag }, await pg.evaluate(() => { const g = (n) => DIPC.ds.get(n); return { t: +g('t').toFixed(3), held: g('held'), mode: g('mode'), x: +g('x').toFixed(3), th1: +(g('th1w') * 180 / Math.PI).toFixed(2), th2: +(g('th2w') * 180 / Math.PI).toFixed(2), u: +g('u').toFixed(2), uh: +(g('hand_u') || 0).toFixed(2), xh: +(g('hand_x') || 0).toFixed(3), bal: g('bal'), status: document.getElementById('state').textContent }; })));
  await snap('before');
  await pg.mouse.move(x0, y0); await pg.mouse.down(); await pg.waitForTimeout(200); await snap('grabbed');
  for (let i = 1; i <= 20; i++) { await pg.mouse.move(x0 + 8 * i, y0); await pg.waitForTimeout(15); }
  await snap('dragged 160 px'); await pg.waitForTimeout(400); await snap('held still 0.4 s');
  await pg.screenshot({ path: path.join(__dirname, 'drag-held.png'), clip: { x: box.x, y: box.y, width: box.width, height: box.height } });
  // the store's own checks of every hand step: force from (29)+(30), and the RK4 replay
  const chk = await pg.evaluate(() => { const ds = DIPC.ds, n = ds.get('st_n'), k = ds.get('st_kind'), ch = Sim.data.check; let nh = 0, du = 0, ds1 = 0;
    for (let r = 0; r < n; r++) if (k[r] === 2) { nh++; const a = ch.st_u(r); du = Math.max(du, Math.abs(a.value - ds.get('st_u')[r]));
      for (let i = 0; i < 6; i++) { const c = ch.st_s1(6 * r + i); ds1 = Math.max(ds1, Math.abs(c.value - ds.get('st_s1')[6 * r + i])); } }
    const hu = ch.hand_u(), ha = ch.hand_a(); return { handSteps: nh, maxForceDiff: du, maxReplayDiff: ds1, hand_u: [hu.value, ds.get('hand_u')], hand_a: [ha.value, ds.get('hand_a')], bal: ds.get('bal'), Eext: ds.get('E_ext') }; });
  await pg.mouse.up(); await pg.waitForTimeout(100); await snap('released');
  for (const w of [1500, 4000, 10000]) { await pg.waitForTimeout(w); await snap('after +' + w + ' ms'); }
  console.log(JSON.stringify(chk)); log.forEach((l) => console.log(JSON.stringify(l)));
  console.log('page errors:', errs.join(' | ') || 'none'); await b.close(); })();
