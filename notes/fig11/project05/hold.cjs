const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const med of (process.env.MEDS || 'vacuum,air,water,glycerol,honey').split(',')) for (const lq of [false, true]) {
    const pg = await b.newPage(); await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1200);
    await pg.evaluate(([m, lq]) => { DIPC.lqDrag = lq; DIPC.superOn = false; const s = document.getElementById('med'); s.value = m; s.dispatchEvent(new Event('change', { bubbles: true })); }, [med, lq]);
    await pg.waitForTimeout(2500); const t0 = await pg.evaluate(() => DIPC.ds.get('t'));
    await pg.click('button[data-go="1"]'); const rows = [];
    let reach = null, mx = 0;
    for (let i = 0; i < 60; i++) { await pg.waitForTimeout(500); const r = await pg.evaluate(() => [DIPC.ds.get('t'), DIPC.ds.get('x'), DIPC.mode, DIPC.log.filter(e => e.ev === 'rescue').length, DIPC.lost, Math.max(Math.abs(DIPC.ds.get('th1w')), Math.abs(DIPC.ds.get('th2w'))) * 57.3]); mx = Math.max(mx || 0, r[5]); if (reach === null && Math.abs(r[1] - 1) < 0.02 && r[2] === 'balance') reach = (r[0] - t0).toFixed(1); rows.push(r); }
    const last = rows[rows.length - 1];
    console.log(med.padEnd(9), lq ? 'drag-aware' : 'old       ', 'x after 30 s', last[1].toFixed(3), 'mode', last[2], 'rescues', last[3], 'lost', last[4], 'max lean', (mx||0).toFixed(1), 'deg', 'within 2 cm at', reach, 's');
    await pg.close(); }
  await b.close();
})();
