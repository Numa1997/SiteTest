const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1500);
  for (const med of ['air', 'water', 'glycerol', 'honey']) for (const fl of ['still', 'own']) {
    const r = await pg.evaluate(([med, fl]) => {
      const md = document.querySelector('option[value=vacuum]').closest('select'); md.value = med; md.dispatchEvent(new Event('change', { bubbles: true }));
      const m = document.querySelector('option[value=own]').closest('select'); m.value = fl; m.dispatchEvent(new Event('change', { bubbles: true }));
      if (fl === 'own') { for (const [id, v] of [['own-u', '0.5'], ['own-v', '0']]) { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); } }
      const D = window.DIPC, p = D.p, st = [0, 0.05, 0.05, 0, 0, 0];
      const Q = D.fluidQ(p, st, 0);
      return { med, fl, field: p.fl && p.fl.field, rho: p.fl.rho, mu: p.fl.mu, xi1: p.fl.xi[0], cq: p.fl.cq, cl: p.fl.cl, cc: p.fl.cc, Qx: Q[0], Qt1: Q[1], Qt2: Q[2] };
    }, [med, fl]);
    console.log(JSON.stringify(r, (k, v) => typeof v === 'number' ? +v.toPrecision(4) : v));
  }
  console.log('errors', errs.length, errs.slice(0, 2)); await b.close();
})();
