// the page's Q (35) at one fixed test state, for the Wolfram gate
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('file:///home/user/SiteTest/public/simulations/double-inverted-pendulum.html'); await pg.waitForTimeout(1500);
  const r = await pg.evaluate(() => { const s = [0.3, 0.4, -0.3, 0.5, 1.2, -0.8], t = 1.7, out = {};
    for (const [med, flow] of [['air', 'fan'], ['air', 'street'], ['air', 'eddy'], ['water', 'waves'], ['glycerol', 'cells'], ['air', 'ground']]) {
      const M = document.getElementById('med'), F = document.getElementById('flow'); M.value = med; M.dispatchEvent(new Event('change')); F.value = flow; F.dispatchEvent(new Event('change'));
      const p = { L1: 0.5, L2: 0.75, fl: DIPC.fluidPar(0.5, 0.75) }; p.fl.U = 2; out[med + '/' + flow] = { Q: DIPC.fluidQ(p, s, t), fl: p.fl }; }
    return out; });
  for (const k in r) console.log(k.padEnd(16), r[k].Q.map(v => v.toPrecision(15)).join('  '), '| xi', r[k].fl.xi.map(v => v.toPrecision(12)).join(' '), 'cq', r[k].fl.cq.toPrecision(12), 'cl', r[k].fl.cl.toPrecision(12), 'cc', r[k].fl.cc.toPrecision(12), 'nu', r[k].fl.nu.toPrecision(12));
  await b.close(); })();
