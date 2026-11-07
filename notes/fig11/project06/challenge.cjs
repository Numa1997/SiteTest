// "Challenge, not eliminate" (Numa, 6 Nov 2026), measured with the page itself: for each deep and slow flow and each liquid, the largest U
// (0.1 m/s steps) at which the running page, supervisor included, keeps the rods up for T s after the flow is chosen while they balance:
// no rescue, the cart within 1.5 m of the rail's middle. The flow comes up over 8 s (13.8). The page's own step() and think() at 60 frames
// per second of simulated time; the reader sees the same run. Prints U* per case and the uStart table for the page's settings.
const { chromium } = require('playwright');
const T = +(process.env.T || 120);
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage(); const res = {};
  await pg.goto('http://localhost:8765/simulations/' + (process.env.PAGE || 'rods-in-liquid.html'), { waitUntil: 'load' }); await pg.waitForTimeout(1500);
  for (const med of (process.env.MEDS || 'water,glycerol,honey').split(',')) for (const fl of (process.env.FLOWS || 'internal,gyre,deepsea,tides').split(',')) {
    const run = (U) => pg.evaluate(([m, f, U, T]) => {
      const ch = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('change', { bubbles: true })); };
      const inp = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('input', { bubbles: true })); };
      ch('flow', 'still'); ch('med', m); document.getElementById('reset').click(); DIPC.finishCatch();
      for (let i = 0; i < 120; i++) { DIPC.step(1 / 60); DIPC.think(8); }
      const n0 = DIPC.log.length; ch('flow', f); inp('Uf', U); DIPC.finishCatch(); let xm = 0, a = 0;
      for (let i = 0; i < T * 60; i++) { DIPC.step(1 / 60); DIPC.think(8); xm = Math.max(xm, Math.abs(DIPC.s[0])); const ev = DIPC.log.slice(n0).map(l => l.ev); if (ev.includes('rescue') || xm > 1.5) return { ok: false, t: i / 60, xm, ev: ev.join(',') }; }
      return { ok: true, xm }; }, [med, fl, U, T]);
    const D = +(process.env.STEP || 0.1), top = +(process.env.TOP || 4);   // the grid of U (m/s) and the largest U tried
    let lo = 0, hi = Math.round(top / D) + 1, best = null;
    while (hi - lo > 1) { const mid = (lo + hi) >> 1, q = await run(+(mid * D).toFixed(2)); if (q.ok) { lo = mid; best = q; } else hi = mid; }
    (res[med] = res[med] || {})[fl] = +(lo * D).toFixed(2);
    console.log(med.padEnd(9), fl.padEnd(9), 'U*', +(lo * D).toFixed(2), 'm/s', best ? `| cart within ${best.xm.toFixed(2)} m` : '| even 0.1 m/s is too strong');
  }
  console.log('uStart', JSON.stringify(res)); await b.close();
})();
