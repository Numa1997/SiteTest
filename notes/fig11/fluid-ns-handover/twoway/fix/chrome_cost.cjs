// The solved fluid's cost per 20 ms fluid step in headless Chromium (the store's tw_ms), glycerol and water, still water then a breeze.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const br = await chromium.launch(); const pg = await br.newPage({ viewport: { width: 1100, height: 900 } }); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('file://' + path.resolve(__dirname, '../../../../../public/simulations/double-inverted-pendulum.html')); await pg.waitForTimeout(1500);
  for (const [m, f, U] of [['glycerol', 'still', 0], ['water', 'breeze', 0.3]]) {
    await pg.evaluate((a) => { const S = document.getElementById('Uf'); S.value = a.U; S.dispatchEvent(new Event('input', { bubbles: true }));
      const M = document.getElementById('med'); M.value = a.m; M.dispatchEvent(new Event('change')); const F = document.getElementById('flow'); F.value = a.f; F.dispatchEvent(new Event('change'));
      const C = document.getElementById('cpl'); C.disabled = false; C.value = 'solved'; C.dispatchEvent(new Event('change')); }, { m, f, U });
    await pg.waitForTimeout(2000); const xs = [];
    for (let k = 0; k < 40; k++) { await pg.waitForTimeout(100); xs.push(await pg.evaluate(() => [DIPC.ds.get('tw_ms'), DIPC.ds.get('tw_slow'), DIPC.ds.get('tw_on')])); }
    const ms = xs.map(x => x[0]).sort((a, b) => a - b); console.log(m, f, 'on', xs[0][2], 'tw_ms median', ms[20].toFixed(1), 'p90', ms[36].toFixed(1), 'speed', xs[xs.length - 1][1]);
  }
  console.log('page errors', errs.length, errs.slice(0, 3)); await br.close(); })();
