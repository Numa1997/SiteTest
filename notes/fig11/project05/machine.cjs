// Is there a machine (masses, lengths, motor limit) that the planner CAN swing up in a liquid? Sets the sliders, then runs PlanJob with drag in its model.
// env: MEDS, MACH as "m0/m1/m2/L1/L2/F;..." , TS (horizons, s)
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1500);
  for (const mach of (process.env.MACH || '1.5/0.5/0.75/0.5/0.75/60').split(';')) for (const med of (process.env.MEDS || 'water').split(',')) {
    const r = await pg.evaluate(([mach, m, Ts]) => {
      const [m0, m1, m2, L1, L2, F] = mach.split('/').map(Number), set = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('input', { bubbles: true })); };
      set('m0', m0); set('m1', m1); set('m2', m2); set('L1', L1); set('L2', L2); set('Fmax', F);
      const e = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('change', { bubbles: true })); }; e('med', m); if (m !== 'vacuum') e('flow', 'still');
      DIPC.planDrag = true; const out = [];
      for (const T of Ts) { const s0 = [0, Math.PI, Math.PI, 0, 0, 0], t0 = performance.now(), j = new DIPC.PlanJob(DIPC.p, s0, T, { x: 1.5, u: F, vw: 0.3 });
        while (!j.done && performance.now() - t0 < 60000) j.work(50);
        out.push(`T${T}: ${j.ok ? 'OK' : 'fail'} d ${j.res.dmax.toExponential(1)} umax ${j.res.umax.toFixed(0)} xmax ${j.res.xmax.toFixed(2)}`); }
      return out.join(' | '); }, [mach, med, (process.env.TS || '4,6').split(',').map(Number)]);
    console.log(mach, med, r); }
  await b.close();
})();
