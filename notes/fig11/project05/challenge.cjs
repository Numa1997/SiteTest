// "Challenge, not eliminate" (Numa, 6 Nov 2026): for each deep and slow flow and each medium, the largest U (slider grid, 0.1 m/s steps)
// at which the balancer alone, default machine, 60 N, T_s = 10 ms, starting upright at x = 0 with target 0, holds the rods for T seconds
// with its force never above FRAC of the limit. Integrated with the page's own rk4 (full fluid force (35)), the page's K, u = sat(−K s) held over T_s.
// Reports at that U: the largest tilt of each rod, the farthest the cart is pushed, and the motor's peak share.
const { chromium } = require('playwright');
const TEND = +(process.env.T || 120), FRAC = +(process.env.FRAC || 0.75);
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1200);
  for (const med of (process.env.MEDS || 'air,water,glycerol,honey').split(',')) for (const fl of (process.env.FLOWS || 'internal,gyre,deepsea,tides').split(',')) {
    const r = await pg.evaluate(([m, fl, TEND, FRAC]) => {
      const set = (id, v, ev) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event(ev, { bubbles: true })); };
      set('med', m, 'change'); set('flow', fl, 'change');
      const run = (U) => { set('Uf', U, 'input'); const p = DIPC.p, K = DIPC.K, F = 60, wrap = a => Math.atan2(Math.sin(a), Math.cos(a));
        let s = [0, 0, 0, 0, 0, 0], t = 0, u = 0, a1 = 0, a2 = 0, xm = 0, um = 0;
        for (let n = 0; n < TEND * 1000; n++) { if (n % 10 === 0) { const e = [s[0], wrap(s[1]), wrap(s[2]), s[3], s[4], s[5]]; u = 0; for (let i = 0; i < 6; i++) u -= K[i] * e[i]; u = Math.max(-F, Math.min(F, u)); um = Math.max(um, Math.abs(u)); }
          s = DIPC.rk4(p, s, u, 0.001, t); t += 0.001; a1 = Math.max(a1, Math.abs(wrap(s[1]))); a2 = Math.max(a2, Math.abs(wrap(s[2]))); xm = Math.max(xm, Math.abs(s[0]));
          if (a1 > 0.5 || a2 > 0.5 || xm > 3) return { ok: false, a1, a2, xm, um }; }
        return { ok: um <= FRAC * F, a1, a2, xm, um }; };
      let lo = 0, hi = 81, best = null;   // in tenths of m/s
      const r8 = run(8); if (r8.ok) return { U: 8, ...r8, capped: true };
      while (hi - lo > 1) { const mid = (lo + hi) >> 1, q = run(mid / 10); if (q.ok) { lo = mid; best = q; } else hi = mid; }
      return best ? { U: lo / 10, ...best } : { U: 0, note: 'even 0.1 m/s is too strong', ...run(0.1) }; }, [med, fl, TEND, FRAC]);
    const d = v => (v * 180 / Math.PI).toFixed(1);
    console.log(med.padEnd(9), fl.padEnd(9), 'U*', r.U, 'm/s', r.capped ? '(slider top)' : '', r.note || '', '| tilt', d(r.a1), d(r.a2), 'deg | cart', r.xm.toFixed(2), 'm | motor peak', (r.um / 60 * 100).toFixed(0), '%'); }
  await b.close();
})();
