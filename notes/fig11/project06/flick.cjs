// Project 06: which flick does the balancer catch? For each medium and each J (N·s): Reset, settle 2 s, flick the top to the right, watch 5 s.
// "caught" = no rescue in the supervisor's log and both rods within 2° of their rest state at the end.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/' + (process.env.PAGE || 'rods-in-liquid.html'), { waitUntil: 'load' }); await pg.waitForTimeout(1500);
  for (const med of (process.env.MEDS || 'water,glycerol,honey').split(',')) {
    const out = [];
    for (const J of (process.env.JS || '0.5,1,1.5,2,2.5,3,3.5,4').split(',').map(Number)) {
      await pg.evaluate(([m, J]) => { const set = (id, v, ev) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event(ev, { bubbles: true })); }; set('med', m, 'change'); set('J', J, 'input'); document.getElementById('reset').click(); }, [med, J]);
      await pg.waitForTimeout(2000); const n0 = await pg.evaluate(() => DIPC.log.length);
      await pg.click('#flickR'); await pg.waitForTimeout(5000);
      const r = await pg.evaluate((n0) => ({ ev: DIPC.log.slice(n0).map(l => l.ev), a1: Math.abs(DIPC.ds.get('th1w') - DIPC.EQ.th1) * 57.3, a2: Math.abs(DIPC.ds.get('th2w') - DIPC.EQ.th2) * 57.3, x: DIPC.s[0] }), n0);
      out.push(`J ${J}: ${r.ev.includes('rescue') ? 'fell (' + r.ev.join(',') + ')' : r.a1 < 2 && r.a2 < 2 ? 'caught' : 'not settled'} x ${r.x.toFixed(2)}`);
    }
    console.log(med + '\n  ' + out.join('\n  '));
  }
  await b.close();
})();
