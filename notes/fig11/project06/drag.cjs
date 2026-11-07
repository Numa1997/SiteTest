// Project 06: drag the cart with the mouse and let go, in a flow. Per case med:flow:U the page settles for 6 s, reads the flow's rest state
// (θ1*, θ2*, u*), then the mouse grabs the cart, drags it DX m in about 1 s, holds HOLD s and lets go; every second for T s it reports
// t, mode, x, θ1, θ2 (deg) and u, and finally how far the rods are from the rest state. SHOT=<prefix> saves screenshots while held and at the end.
const { chromium } = require('playwright');
const PAGE = process.env.PAGE || 'rods-in-liquid.html';
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const c of (process.env.CASES || 'water:river:0.5').split(',')) {
    const [med, fl, U] = c.split(':'); const pg = await b.newPage({ viewport: { width: +(process.env.W || 1100), height: 900 } }); pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('http://localhost:8765/simulations/' + PAGE, { waitUntil: 'load' }); await pg.waitForTimeout(1200);
    await pg.evaluate(([m, f, U]) => { const set = (id, v, ev) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event(ev, { bubbles: true })); }; set('med', m, 'change'); set('flow', f, 'change'); if (U === U) set('Uf', U, 'input'); }, [med, fl, +U]);
    await pg.waitForTimeout(6000);
    const eq = await pg.evaluate(() => ({ on: DIPC.EQ.on, th1: DIPC.EQ.th1 * 57.296, th2: DIPC.EQ.th2 * 57.296, u: DIPC.EQ.u, U: +document.getElementById('Uf').value }));
    const box = await pg.$eval('#cv', e => { const r = e.getBoundingClientRect(); return { x: r.left, y: r.top }; });
    const at = await pg.evaluate(() => ({ x: DIPC.ds.get('cart_px'), y: DIPC.ds.get('cart_py'), h: DIPC.ds.get('cart_h'), sc: DIPC.ds.get('sc') }));
    const DX = +(process.env.DX || 0.3), x0 = box.x + at.x + at.h, y0 = box.y + at.y + at.h / 2;   // a point on the hull beside the slot
    await pg.mouse.move(x0, y0); await pg.mouse.down();
    for (let k = 1; k <= 20; k++) { await pg.mouse.move(x0 + DX * at.sc * k / 20, y0); await pg.waitForTimeout(50); }
    const held = await pg.evaluate(() => DIPC.ds.get('held'));
    await pg.waitForTimeout(1000 * +(process.env.HOLD || 1));
    if (process.env.SHOT) await pg.screenshot({ path: `${process.env.SHOT}-${med}-${fl}-held.png` });
    const xr = await pg.evaluate(() => DIPC.s[0]), trel = await pg.evaluate(() => DIPC.t); await pg.mouse.up(); console.log(`  released at page time ${trel.toFixed(2)} s`);
    const rows = []; for (let i = 0; i < +(process.env.T || 15); i++) { await pg.waitForTimeout(1000); rows.push(await pg.evaluate(() => [DIPC.t.toFixed(0), DIPC.mode, DIPC.s[0].toFixed(2), (DIPC.ds.get('th1w') * 57.3).toFixed(1), (DIPC.ds.get('th2w') * 57.3).toFixed(1), DIPC.u.toFixed(0)].join(' '))); }
    const end = await pg.evaluate((tr) => { const c = DIPC.log.filter(l => l.ev === 'caught').pop(); return { th1: DIPC.ds.get('th1w') * 57.296, th2: DIPC.ds.get('th2w') * 57.296, e1: DIPC.EQ.th1 * 57.296, e2: DIPC.EQ.th2 * 57.296, x: DIPC.s[0], t: DIPC.t, tc: c ? c.t : NaN, tr }; }, xr);
    if (process.env.SHOT) await pg.screenshot({ path: `${process.env.SHOT}-${med}-${fl}-end.png` });
    console.log(c, `U ${eq.U} m/s, rest state θ1* ${eq.th1.toFixed(1)}°, θ2* ${eq.th2.toFixed(1)}°, u* ${eq.u.toFixed(1)} N (told: ${eq.on}); grabbed: held=${held}, let go at x = ${xr.toFixed(2)} m`);
    console.log('  ' + rows.filter((r, i) => i % 3 === 2).join('\n  '));
    console.log(`  end, page time ${end.t.toFixed(1)} s, ${(end.t - end.tc).toFixed(1)} s after the catch: θ1 − θ1* = ${(end.th1 - end.e1).toFixed(2)}°, θ2 − θ2* = ${(end.th2 - end.e2).toFixed(2)}°, x = ${end.x.toFixed(2)} m; log ${JSON.stringify(await pg.evaluate(() => DIPC.log.map(l => l.ev + '@' + l.t.toFixed(1))))}`);
    await pg.close(); }
  console.log('page errors:', errs.length ? errs : 'none'); await b.close();
})();
