// 13.8: the controller is told the flow. Drag-and-release test in the running page: wait, read the flow's rest state, knock the machine
// (cart moved DX m and given speed V, rods tilted by D1, D2 degrees from the rest state), then watch T s. CASES med:flow:U, env DX V D1 D2 T GO (target x).
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const c of (process.env.CASES || 'water:breeze:0.3,glycerol:breeze:0.3,honey:breeze:0.15').split(',')) {
    const [med, fl, U] = c.split(':'); const pg = await b.newPage(); pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1200);
    await pg.evaluate(([m, f, U]) => { const set = (id, v, ev) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event(ev, { bubbles: true })); }; set('med', m, 'change'); set('flow', f, 'change'); set('Uf', U, 'input'); }, [med, fl, +U]);
    await pg.waitForTimeout(6000);
    const eq = await pg.evaluate(() => ({ on: DIPC.EQ.on, th1: DIPC.EQ.th1 * 57.296, th2: DIPC.EQ.th2 * 57.296, u: DIPC.EQ.u, s: DIPC.s.map(v => +v.toFixed(3)), c: DIPC.cLevel }));
    const D = (k, d) => +(process.env[k] || d);
    await pg.evaluate(([dx, v, d1, d2, go]) => { const s = DIPC.s.slice(); s[0] += dx; s[3] = v; s[1] += d1 * Math.PI / 180; s[2] += d2 * Math.PI / 180; DIPC.s = s; if (go !== null) document.querySelector('button[data-go="' + go + '"]').click(); }, [D('DX', 0.3), D('V', 1), D('D1', 15), D('D2', -10), process.env.GO || null]);
    const rows = []; for (let i = 0; i < D('T', 20); i++) { await pg.waitForTimeout(1000); rows.push(await pg.evaluate(() => [DIPC.t.toFixed(0), DIPC.mode, DIPC.s[0].toFixed(2), (DIPC.ds.get('th1w') * 57.3).toFixed(1), (DIPC.ds.get('th2w') * 57.3).toFixed(1), DIPC.u.toFixed(1)].join(' '))); }
    console.log(c, 'rest state', JSON.stringify({ on: eq.on, th1: +eq.th1.toFixed(2), th2: +eq.th2.toFixed(2), u: +eq.u.toFixed(2), c: eq.c && +eq.c.toFixed(3), before_knock: eq.s }));
    console.log('  ' + rows.filter((r, i) => i % 4 === 3).join('\n  '), '\n  log', JSON.stringify(await pg.evaluate(() => DIPC.log.map(l => l.ev + '@' + l.t.toFixed(1)))));
    await pg.close(); }
  console.log('page errors:', errs.length ? errs : 'none'); await b.close();
})();
