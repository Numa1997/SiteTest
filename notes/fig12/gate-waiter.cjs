// The page's waiter against the offline design: its gains, and a 20 cm carry on its own integrator. node notes/fig12/gate-waiter.cjs <out.json>
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/beer-slosh.html'); await pg.waitForTimeout(1500);
  const r = await pg.evaluate(() => { const S = window.SLOSH, ds = S.ds; document.getElementById('play').click();
    S.aO.fill(0); S.vO.fill(0); document.querySelector('#ctl button[data-v="waiter"]').click();
    const K = Array.from(ds.get('K')), t0 = S.t; S.Tg.x = 0.2; let peak = 0, settle = null, Fmax = 0; const xs = [];
    for (let i = 0; i < 4000; i++) { S.step(); const e = Math.abs(S.etaWall(0)); peak = Math.max(peak, e); xs.push(S.G.x - 0.2); }
    for (let i = 0; i < xs.length; i++) { if (xs.slice(i).every(v => Math.abs(v) < 0.002)) { settle = (i + 1) * 1e-3; break; } }
    return { K, peak, settle, tau: ds.get('tau_cl'), Me: ds.get('M_e'), M: ds.get('M_tot') }; });
  fs.writeFileSync(process.argv[2], JSON.stringify(r)); console.log(JSON.stringify(r)); await b.close(); })();
