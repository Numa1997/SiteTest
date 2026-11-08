const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8813/simulations/momentum-spirographs.html');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const T = +process.argv[2] || 6;
  const res = await p.evaluate((T) => { const f = window.__fig13; f.pause(); const t0 = performance.now(); f.advance(T - f.t()); return { t: f.t(), ms: performance.now() - t0,
     tips: f.pend().map(q => [q.xs[q.xs.length - 1], q.ys[q.ys.length - 1]]) }; }, T);
  await p.waitForTimeout(400);
  await p.screenshot({ path: process.argv[3] + '/fig13-page.png', clip: { x: 0, y: 0, width: 1440, height: 1000 } });
  const st = await p.$('.stage'); await st.screenshot({ path: process.argv[3] + '/fig13-stage.png' });
  const pf = await p.$('.pfig'); await pf.screenshot({ path: process.argv[3] + '/fig13-schematic.png' });
  // alpha-first readback: is anything drawn on the curve canvas?
  const ink = await p.evaluate(() => { const c = document.getElementById('cv'); const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < d.length; i += 4) if (d[i] > 0) n++; return n / (d.length / 4); });
  require('fs').writeFileSync(process.argv[3] + '/js_tips.json', JSON.stringify(res));
  console.log(JSON.stringify({ t: res.t, ms: Math.round(res.ms), inked_fraction: ink.toFixed(4), errors: errs }));
  await b.close();
})();
