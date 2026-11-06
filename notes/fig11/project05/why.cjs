const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const med of (process.env.MEDS || 'water,honey').split(',')) {
    const pg = await b.newPage(); await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1200);
    await pg.evaluate((m) => { const s = document.getElementById('med'); s.value = m; s.dispatchEvent(new Event('change', { bubbles: true })); window.__tm = DIPC.ds.get('t'); }, med);
    const tr = [];
    for (let i = 0; i < 12; i++) { await pg.waitForTimeout(250); tr.push(await pg.evaluate(() => [DIPC.ds.get('t').toFixed(2), DIPC.ds.get('x').toFixed(3), (DIPC.ds.get('th1w') * 57.3).toFixed(2), (DIPC.ds.get('th2w') * 57.3).toFixed(2), DIPC.mode, +DIPC.W().toFixed(4), +(DIPC.cLevel || 0).toFixed(4)].join(' '))); }
    console.log(med, 'medium set at t', await pg.evaluate(() => window.__tm), '\n ' + tr.join('\n '), '\n log', JSON.stringify(await pg.evaluate(() => DIPC.log.slice(0, 3))));
    await pg.close(); }
  await b.close();
})();
