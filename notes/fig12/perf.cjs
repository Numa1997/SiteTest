// Fig. 12 on a phone-sized window, CPU slowed 4x: frames per second, and where the time goes (physics+2D vs 3D render).
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const pg = await ctx.newPage(); const cdp = await ctx.newCDPSession(pg); await cdp.send('Emulation.setCPUThrottlingRate', { rate: +(process.argv[2] || 4) });
  await pg.goto('http://localhost:8765/simulations/beer-slosh.html'); await pg.waitForTimeout(2000);
  await pg.evaluate(() => document.getElementById('stage3d').scrollIntoView());
  const r = await pg.evaluate(() => new Promise(res => { const S = window.SLOSH, R = window.SLOSH3D; let t3 = 0, n3 = 0, ts = 0, ns = 0;
    const r0 = R.render; R.render = function () { const a = performance.now(); r0(); t3 += performance.now() - a; n3++; };
    const s0 = S.step; let frames = 0; const t0 = performance.now(), tsim0 = S.t;
    function f() { frames++; if (performance.now() - t0 < 5000) requestAnimationFrame(f); else res({ fps: frames / 5, render_ms: t3 / Math.max(1, n3), sim_speed: (S.t - tsim0) / 5 }); } requestAnimationFrame(f); }));
  console.log(JSON.stringify(r)); await b.close(); })();
