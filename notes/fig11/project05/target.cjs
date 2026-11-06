const { chromium } = require('playwright');
const cases = (process.env.CASES || 'vacuum:still,air:still,water:still,glycerol:still,honey:still,water:river').split(',');
(async () => {
  const b = await chromium.launch();
  for (const c of cases) {
    const [med, flow, cpl] = c.split(':');
    const pg = await b.newPage({ viewport: { width: 1100, height: 900 } });
    await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' });
    await pg.waitForTimeout(1500);
    await pg.evaluate(([m, f, k]) => { const e = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('change', { bubbles: true })); };
      e('med', m); if (m !== 'vacuum') { e('flow', f); if (k) e('cpl', k); } }, [med, flow, cpl]);
    await pg.waitForTimeout(3000);
    await pg.click('button[data-go="1"]');
    const g = n => pg.evaluate(n => DIPC.ds.get(n), n); const rows = [];
    for (let i = 0; i < 12; i++) { await pg.waitForTimeout(2000); rows.push([+(await g('t')).toFixed(1), +(await g('x')).toFixed(3), await g('mode'), +(await g('u')).toFixed(2), +(await g('x_target'))]); }
    console.log(c, JSON.stringify(rows.filter((r, i) => i % 2 === 1)));
    await pg.close();
  }
  await b.close();
})();
