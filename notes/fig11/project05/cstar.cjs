const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage(); await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1500);
  for (const med of ['vacuum', 'air', 'water', 'glycerol', 'honey']) for (const [pd, lq] of [[true, true]]) {
    const r = await pg.evaluate(async ([m, pd, lq]) => { DIPC.planDrag = pd; DIPC.lqDrag = lq; const s = document.getElementById('med'); s.value = m; s.dispatchEvent(new Event('change', { bubbles: true }));
      for (let i = 0; i < 100 && DIPC.ds.get('c_busy'); i++) await new Promise(r => setTimeout(r, 100)); return [DIPC.ds.get('c_star'), DIPC.ds.get('c_busy')]; }, [med, pd, lq]);
    console.log(med.padEnd(9), 'planner drag', pd ? 'yes' : 'no ', 'balancer drag', lq ? 'yes' : 'no ', 'c* =', r[0], r[1] ? '(busy)' : '');
  }
  await b.close();
})();
