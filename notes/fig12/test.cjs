// Browser test of Fig. 12: node notes/fig12/test.cjs <out-dir> [base-url]
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/fig12-test'; fs.mkdirSync(out, { recursive: true });
  let srv = null, base = process.argv[3];
  if (!base) { srv = spawn('python3', ['-m', 'http.server', '8772', '--directory', path.join(__dirname, '../../public')], { stdio: 'ignore' }); await new Promise(r => setTimeout(r, 800)); base = 'http://localhost:8772'; }
  const b = await chromium.launch(); const errs = [];
  for (const [name, vp] of [['desktop', { width: 1440, height: 1000 }], ['phone', { width: 390, height: 844 }]]) {
    const p = await b.newPage({ viewport: vp, deviceScaleFactor: 1 });
    p.on('pageerror', e => errs.push(name + ': ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(name + ' console: ' + m.text()); });
    await p.goto(base + '/simulations/beer-slosh.html'); await p.waitForTimeout(1500);
    const s0 = await p.evaluate(() => ({ t: Fig12.world.t, x: Fig12.world.cart.x }));
    await p.waitForTimeout(6000);
    const s1 = await p.evaluate(() => ({ t: Fig12.world.t, x: Fig12.world.cart.x, rate: document.getElementById('cap-rate').textContent, dw: document.getElementById('r-dw').textContent, solver: document.getElementById('r-solver').textContent }));
    console.log(name, JSON.stringify(s0), '→', JSON.stringify(s1));
    await p.screenshot({ path: path.join(out, name + '.png') });
    if (name === 'desktop') {
      // speed control on: a push is answered by the motor (the current drops); open loop: the push speeds the cart up
      const i0 = await p.evaluate(() => Fig12.world.cart.i); await p.keyboard.down('ArrowRight'); await p.waitForTimeout(2500);
      const i1 = await p.evaluate(() => Fig12.world.cart.i); await p.keyboard.up('ArrowRight');
      console.log('push with speed control: motor current', i0.toFixed(2), '→', i1.toFixed(2), 'A');
      await p.click('#ctrl-off'); await p.waitForTimeout(300);
      const v0 = await p.evaluate(() => Fig12.world.cart.vx); await p.keyboard.down('ArrowRight'); await p.waitForTimeout(2500); const v1 = await p.evaluate(() => Fig12.world.cart.vx); await p.keyboard.up('ArrowRight');
      console.log('push in open loop: speed', v0.toFixed(3), '→', v1.toFixed(3));
      // drag: press on the cart and pull 10 cm back; the hand force appears and the cart is held back
      const bb = await p.locator('#cv').boundingBox();
      await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height * 0.7); await p.mouse.down(); await p.mouse.move(bb.x + bb.width / 2 - 120, bb.y + bb.height * 0.7, { steps: 5 });
      await p.waitForTimeout(1500); const dr = await p.evaluate(() => ({ hand: Fig12.world.cart.hand, F: Fig12.world.cart.Fhand, v: Fig12.world.cart.vx })); await p.mouse.up();
      console.log('drag: hand at', dr.hand && dr.hand.toFixed(3), 'm, hand force', dr.F.toFixed(2), 'N, speed', dr.v.toFixed(3), 'm/s');
      await p.locator('#stage').screenshot({ path: path.join(out, 'stage.png') });
      const ovf = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth); console.log('horizontal overflow px', ovf);
    } else {
      const ovf = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth); console.log('phone horizontal overflow px', ovf);
    }
    await p.close();
  }
  console.log('errors:', errs.length ? errs : 'none');
  await b.close(); if (srv) srv.kill();
})();
