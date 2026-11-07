// Project 06: choose a deep and slow flow while the rods balance (the reader's way of meeting it), per liquid. The flow comes up over
// 8 s (13.8); every second for T s: t, mode, x, θ1, θ2 (deg), u, the ramp factor, and whether the supervisor had to rescue.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const out = [];
  for (const med of (process.env.MEDS || 'water,glycerol,honey').split(',')) for (const fl of (process.env.FLOWS || 'internal,gyre,deepsea,tides').split(',')) {
    const pg = await b.newPage(); await pg.goto('http://localhost:8765/simulations/' + (process.env.PAGE || 'rods-in-liquid.html'), { waitUntil: 'load' }); await pg.waitForTimeout(1500);
    const r = await pg.evaluate(([m, f, T]) => { const set = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('change', { bubbles: true })); };
      set('med', m); DIPC.finishCatch(); for (let i = 0; i < 120; i++) { DIPC.step(1 / 60); DIPC.think(8); }
      const n0 = DIPC.log.length, U = (() => { set('flow', f); return +document.getElementById('Uf').value; })(); let a1 = 0, a2 = 0, xm = 0;
      for (let i = 0; i < T * 60; i++) { DIPC.step(1 / 60); DIPC.think(8); const w = v => Math.abs(Math.atan2(Math.sin(v), Math.cos(v))); a1 = Math.max(a1, w(DIPC.s[1] - DIPC.EQ.th1)); a2 = Math.max(a2, w(DIPC.s[2] - DIPC.EQ.th2)); xm = Math.max(xm, Math.abs(DIPC.s[0])); }
      return { U, ev: DIPC.log.slice(n0).map(l => l.ev), a1: a1 * 57.3, a2: a2 * 57.3, xm, mode: DIPC.mode, th1: DIPC.EQ.th1 * 57.3, th2: DIPC.EQ.th2 * 57.3 }; }, [med, fl, +(process.env.T || 60)]);
    out.push(`${med.padEnd(9)} ${fl.padEnd(9)} U ${r.U} m/s: ${r.ev.includes('rescue') ? 'KNOCKED DOWN (' + r.ev.join(',') + ')' : 'held'}; largest gap to the rest state ${r.a1.toFixed(1)}°, ${r.a2.toFixed(1)}°; cart within ${r.xm.toFixed(2)} m; at the end ${r.mode}, rest state ${r.th1.toFixed(1)}°, ${r.th2.toFixed(1)}°`);
    console.log(out[out.length - 1]); await pg.close(); }
  await b.close();
})();
