// Honey: the balancer alone (rescue off), rods start upright at the page's initial tilt: does it hold, and how fast does W fall?
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1200);
  const med = process.env.MED || 'honey';
  await pg.evaluate((m) => { DIPC.superOn = false; const s = document.getElementById('med'); s.value = m; s.dispatchEvent(new Event('change', { bubbles: true })); }, med);
  for (let i = 0; i < 16; i++) { await pg.waitForTimeout(1000); console.log(await pg.evaluate(() => [DIPC.ds.get('t').toFixed(1), DIPC.ds.get('x').toFixed(3), (DIPC.ds.get('th1w') * 57.3).toFixed(2), (DIPC.ds.get('th2w') * 57.3).toFixed(2), DIPC.mode, DIPC.W().toFixed(3), (DIPC.cLevel || 0).toFixed(3), DIPC.u.toFixed(1)].join(' '))); }
  await b.close();
})();
