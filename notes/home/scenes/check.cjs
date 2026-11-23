// Step 5 check: page errors, sideways scroll, mounted scenes, reduced motion, at 1920/1600/1100/390 px. node notes/home/scenes/check.cjs
const { chromium } = require('playwright');
const PAGES = ['index.html', 'de/index.html', 'ar/index.html', 'scenes.html', 'simulations.html', 'portfolios.html', 'lucretius.html'];
(async () => { const b = await chromium.launch(); let bad = 0;
  for (const rm of [false, true]) for (const w of rm ? [1600] : [1920, 1600, 1100, 390]) for (const pg of PAGES) {
    const c = await b.newContext({ viewport: { width: w, height: 1000 }, reducedMotion: rm ? 'reduce' : 'no-preference' }), p = await c.newPage(), errs = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto('http://localhost:8766/' + pg, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
    const r = await p.evaluate(() => ({ side: document.documentElement.scrollWidth - document.documentElement.clientWidth, scenes: (window.__bgScenes || {}).count || 0, canv: document.querySelectorAll('canvas.bgs').length, knobs: document.querySelectorAll('.scn__k').length }));
    const ok = !errs.length && r.side <= 0 && (rm ? r.canv === 0 : true); if (!ok) bad++;
    console.log((ok ? 'ok ' : 'BAD') + ` ${rm ? 'reduced' : 'motion '} ${w} ${pg}: errors ${errs.length} sideways ${r.side} scenes ${r.scenes} canvases ${r.canv} knobs ${r.knobs}` + (errs.length ? ' ' + errs.slice(0, 2).join(' | ') : ''));
    if (pg === 'scenes.html' && !rm && (w === 1600 || w === 390)) await p.screenshot({ path: `notes/home/scenes/after/scenes-${w}.png`, fullPage: true });
    await c.close(); }
  console.log(bad ? bad + ' problems' : 'all clean'); await b.close(); })();
