// Fig. 12 on a phone-sized window, CPU slowed 4x: frames per second, how fast simulated time runs, and where the time goes.
// node notes/fig12/perf.cjs [slowdown]
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const pg = await ctx.newPage(); const cdp = await ctx.newCDPSession(pg); await cdp.send('Emulation.setCPUThrottlingRate', { rate: +(process.argv[2] || 4) });
  await pg.goto('http://localhost:8765/simulations/beer-slosh.html'); await pg.waitForTimeout(2000);
  await pg.evaluate(() => { document.getElementById('stage-cart').scrollIntoView(); document.querySelector('#road button[data-v="rough"]').click(); });
  const r = await pg.evaluate(() => new Promise(res => { const S = window.SLOSH; let frames = 0; const t0 = performance.now(), tsim0 = S.t;
    function f() { frames++; if (performance.now() - t0 < 5000) requestAnimationFrame(f); else res({ fps: frames / 5, sim_speed: (S.t - tsim0) / 5 }); } requestAnimationFrame(f); }));
  console.log(JSON.stringify(r)); await b.close(); })();
