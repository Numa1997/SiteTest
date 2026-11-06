const { chromium } = require('playwright');
const cases = (process.env.CASES || 'water:own,honey:still,glycerol:still').split(',');
(async () => {
  const b = await chromium.launch();
  for (const c of cases) {
    const [med, flow] = c.split(':');
    const pg = await b.newPage({ viewport: { width: 1100, height: 900 } });
    await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' });
    await pg.waitForTimeout(1500);
    await pg.evaluate(([m, f]) => { const e = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('change', { bubbles: true })); }; e('med', m); e('flow', f); }, [med, flow]);
    if (med !== 'water') { await pg.waitForTimeout(2000); await pg.click('button[data-go="1"]'); }
    await pg.waitForTimeout(+(process.env.SECS || 30) * 1000);
    const r = await pg.evaluate(() => { const L = DIPC.log, cnt = {}; L.forEach(e => cnt[e.ev] = (cnt[e.ev] || 0) + 1);
      return { t: DIPC.ds.get('t').toFixed(1), x: DIPC.ds.get('x').toFixed(2), mode: DIPC.mode, cnt, last: L.slice(-6) }; });
    console.log(c, JSON.stringify(r));
    await pg.close();
  }
  await b.close();
})();
