// "Challenge, not eliminate" (Numa, 6 Nov 2026), for project 06's machine: for each deep and slow flow and each liquid, the largest U
// (0.1 m/s steps) at which the page's balancer, told the flow (13.8), holds the rods for T s starting at the flow's rest state at x = 0, with
// its force never above FRAC of the motor's limit. The law is the page's: every T_s the rest state (θ1*, θ2*, u*) is re-solved where the
// reference is (flowEq, warm-started), u = sat(u* − K (s − s*)) held over T_s; the machine is the page's rk4 with the full fluid force (35).
const { chromium } = require('playwright');
const TEND = +(process.env.T || 120), FRAC = +(process.env.FRAC || 0.75);
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/' + (process.env.PAGE || 'rods-in-liquid.html'), { waitUntil: 'load' }); await pg.waitForTimeout(1500);
  const res = {};
  for (const med of (process.env.MEDS || 'water,glycerol,honey').split(',')) for (const fl of (process.env.FLOWS || 'internal,gyre,deepsea,tides').split(',')) {
    const r = await pg.evaluate(([m, fl, TEND, FRAC]) => {
      const set = (id, v, ev) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event(ev, { bubbles: true })); };
      set('med', m, 'change'); set('flow', fl, 'change');
      const run = (U) => { set('Uf', U, 'input'); const p = DIPC.p, K = DIPC.K, F = +document.getElementById('Fmax').value, Ts = +document.getElementById('Ts').value / 1000, nT = Math.round(Ts / 0.001), wrap = a => Math.atan2(Math.sin(a), Math.cos(a));
        let e = DIPC.flowEq(0, 0, [0, 0, 0]); if (!e.ok) return { ok: false, why: 'no rest state at t = 0' };
        let s = [0, e.th1, e.th2, 0, 0, 0], t = 0, u = 0, a1 = 0, a2 = 0, xm = 0, um = 0;
        for (let n = 0; n < TEND * 1000; n++) {
          if (n % nT === 0) { const e2 = DIPC.flowEq(0, t, [e.th1, e.th2, e.u]); if (!e2.ok) return { ok: false, why: 'rest state lost at t = ' + t.toFixed(1), a1, a2, xm, um }; e = e2;
            const d = [s[0], wrap(s[1] - e.th1), wrap(s[2] - e.th2), s[3], s[4], s[5]]; u = e.u; for (let i = 0; i < 6; i++) u -= K[i] * d[i]; u = Math.max(-F, Math.min(F, u)); um = Math.max(um, Math.abs(u)); }
          s = DIPC.rk4(p, s, u, 0.001, t); t += 0.001; a1 = Math.max(a1, Math.abs(wrap(s[1]))); a2 = Math.max(a2, Math.abs(wrap(s[2]))); xm = Math.max(xm, Math.abs(s[0]));
          if (Math.abs(wrap(s[1] - e.th1)) > 0.5 || Math.abs(wrap(s[2] - e.th2)) > 0.5 || xm > 1.5) return { ok: false, why: 'fell at t = ' + t.toFixed(1), a1, a2, xm, um }; }
        return { ok: um <= FRAC * F, a1, a2, xm, um, F }; };
      let lo = 0, hi = 81, best = null;
      const r8 = run(8); if (r8.ok) return { U: 8, ...r8, capped: true };
      while (hi - lo > 1) { const mid = (lo + hi) >> 1, q = run(mid / 10); if (q.ok) { lo = mid; best = q; } else hi = mid; }
      return best ? { U: lo / 10, ...best } : { U: 0, note: 'even 0.1 m/s is too strong', ...run(0.1) }; }, [med, fl, TEND, FRAC]);
    const d = v => (v * 180 / Math.PI).toFixed(1);
    (res[med] = res[med] || {})[fl] = r.U;
    console.log(med.padEnd(9), fl.padEnd(9), 'U*', r.U, 'm/s', r.capped ? '(slider top)' : '', r.note || '', '| largest lean', d(r.a1 || 0), d(r.a2 || 0), 'deg | cart', (r.xm || 0).toFixed(2), 'm | motor peak', ((r.um || 0) / (r.F || 400) * 100).toFixed(0), '%');
  }
  console.log('uStart', JSON.stringify(res)); await b.close();
})();
