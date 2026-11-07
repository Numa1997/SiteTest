// Project 06, note 13.7: the swing-up planner of section 11 (drag in its model), from hanging at rest, for given machines and media.
// MACH "m0/m1/m2/L1/L2/F;..." (default this page's), MEDS, TS (horizons, s), PAGE. Reports success, steps, the largest gap, end error,
// the largest force and cart excursion, and the computing time in Chromium.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/' + (process.env.PAGE || 'rods-in-liquid.html'), { waitUntil: 'load' }); await pg.waitForTimeout(1500);
  for (const mach of (process.env.MACH || '1.5/3/3/0.2/0.25/400').split(';')) for (const med of (process.env.MEDS || 'water,glycerol,honey').split(',')) {
    const r = await pg.evaluate(([mach, m, Ts]) => {
      const [m0, m1, m2, L1, L2, F] = mach.split('/').map(Number), set = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('input', { bubbles: true })); };
      set('m0', m0); set('m1', m1); set('m2', m2); set('L1', L1); set('L2', L2); set('Fmax', F);
      const e = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('change', { bubbles: true })); }; e('med', m); if (m !== 'vacuum') e('flow', 'still');
      const out = [];
      for (const T of Ts) { const s0 = [0, Math.PI, Math.PI, 0, 0, 0], t0 = performance.now(), j = new DIPC.PlanJob(DIPC.p, s0, T, { x: 1.5, u: F, vw: 0.3 });
        while (!j.done && performance.now() - t0 < 120000) j.work(50);
        out.push(`T ${T} s: ${j.ok ? 'found' : 'none'}, ${j.it} steps, gap ${j.res.dmax.toExponential(1)}, end ${j.res.term.toFixed(3)}, |u| ≤ ${j.res.umax.toFixed(0)} N, |x| ≤ ${j.res.xmax.toFixed(2)} m, ${((performance.now() - t0) / 1000).toFixed(1)} s`); }
      return out.join(' | '); }, [mach, med, (process.env.TS || '3,4').split(',').map(Number)]);
    console.log(mach, med, '|', r); }
  await b.close();
})();
