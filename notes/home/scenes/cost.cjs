// Cost of drawing one frame of a scene: mean and worst milliseconds inside its draw() over N seconds. node notes/home/scenes/cost.cjs [base url] [scene] [width]
const { chromium } = require('playwright');
(async () => { const base = process.argv[2] || 'http://localhost:8766/', scene = process.argv[3] || 'forest', w = +(process.argv[4] || 1920), b = await chromium.launch(), p = await b.newPage({ viewport: { width: w, height: 1080 } });
  await p.goto(base + 'index.html', { waitUntil: 'networkidle' });
  if (process.env.YEAR) await p.evaluate(y => { document.querySelector('[data-bg=forest]').__bgScene.YEAR = +y; }, process.env.YEAR);
  if (scene === 'rails') { await p.evaluate(() => scrollTo(0, 900)); await p.waitForTimeout(2500); }
  await p.evaluate(sc => { const s = document.querySelector('[data-bg=' + sc + ']').__bgScene, d = s.draw; window.__c = { n: 0, t: 0, mx: 0 }; s.draw = function (dt) { const a = performance.now(); d.call(s, dt); const e = performance.now() - a; __c.n++; __c.t += e; if (e > __c.mx) __c.mx = e; }; }, scene);
  for (let k = 0; k < +(process.env.ROUNDS || 3); k++) { await p.waitForTimeout(8000); console.log(scene, w, JSON.stringify(await p.evaluate(() => { const r = { frames: __c.n, mean_ms: +(__c.t / __c.n).toFixed(2), worst_ms: +__c.mx.toFixed(1) }; __c.n = 0; __c.t = 0; __c.mx = 0; return r; }))); }
  await b.close(); })();
