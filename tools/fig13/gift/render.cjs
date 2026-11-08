// Render the butterfly film frame by frame with the preinstalled headless Chromium.
//   node tools/fig13/gift/render.cjs THEME OUTDIR DSF [frame,frame,... | all] [PAGE] [SCENE]
//   PAGE: butterfly3d (default) or morph; SCENE (morph only): wheel or butterfly
// Serves nothing itself: start `python3 -m http.server 8766` in the repository root first.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [theme, outdir, dsf, which, page, scene] = [process.argv[2], process.argv[3], Number(process.argv[4] || 1), process.argv[5] || 'all', process.argv[6] || 'butterfly3d', process.argv[7] || 'butterfly'];
  fs.mkdirSync(outdir, { recursive: true });
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: dsf });
  const p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto(`http://localhost:8766/tools/fig13/gift/${page}.html?theme=${theme}&scene=${scene}&film=1`, { waitUntil: 'load' });
  await p.waitForFunction(() => window.__ready === true, null, { timeout: 60000 });
  const total = await p.evaluate(() => window.FILM.frames());
  const list = which === 'all' ? Array.from({ length: total }, (_, i) => i) : which.split(',').map(Number);
  const t0 = Date.now(); const png = dsf >= 2 || which !== 'all';
  for (const f of list) {
    await p.evaluate(f => window.renderFrame(f), f);
    const name = `${outdir}/f${String(f).padStart(4, '0')}.${png ? 'png' : 'jpg'}`;
    await p.screenshot(png ? { path: name } : { path: name, type: 'jpeg', quality: 93 });
    if (list.length > 20 && f % 60 === 0) console.log(theme, 'frame', f, 'of', total, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  console.log(theme, 'done', list.length, 'frames in', ((Date.now() - t0) / 1000).toFixed(0), 's; total frames in film:', total, '; errors:', errs.length ? errs : 'none');
  await b.close();
})();
