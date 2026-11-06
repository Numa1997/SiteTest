const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1500);
  for (const med of (process.env.MEDS || 'vacuum,water,glycerol,honey').split(',')) for (const drag of [false, true]) {
    if (med === 'vacuum' && drag) continue;
    const r = await pg.evaluate(([m, drag, Ts, E0, XL, UL]) => { var process = { env: { XL: XL, UL: UL } }; { const e = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('change', { bubbles: true })); }; e('med', m);
      DIPC.planDrag = drag; const out = [];
      for (const T of Ts) { const s0 = [0, Math.PI - E0, Math.PI - E0 * 0.5, 0, 0, 0]; const t0 = performance.now(); const j = new DIPC.PlanJob(DIPC.p, s0, T, { x: +(process.env.XL||1.5), u: +(process.env.UL||0) || DIPC.sF.value, vw: 0.3 });
        while (!j.done && performance.now() - t0 < 60000) j.work(50);
        out.push(`T${T}: ${j.ok ? 'OK' : 'fail'} it ${j.it} ${(performance.now() - t0) / 1000 | 0}s d ${j.res.dmax.toExponential(1)} term ${j.res.term.toFixed(3)} umax ${j.res.umax.toFixed(0)} xmax ${j.res.xmax.toFixed(2)}`); }
      return out; } }, [med, drag, (process.env.TS || '4,6,8,10').split(',').map(Number), +(process.env.E0 || 0), process.env.XL, process.env.UL]);
    console.log(med, drag ? 'drag' : 'nodrag', r.join(' | '));
  }
  await b.close();
})();
