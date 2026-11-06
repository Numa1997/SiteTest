// Fig. 12 screenshots for review (deviceScaleFactor 2): at rest, swinging after a push in open loop, spilling over a 25 mm
// bump, at 1280 px and 390 px; and the lecture note opened, checked for KaTeX errors and sideways scroll.
// node notes/fig12/shots.cjs <out-dir> <base-url>   (serve with: node notes/fig12/serve.cjs 8790)
const { chromium } = require('playwright'), fs = require('fs');
(async () => {
  const out = process.argv[2] || 'notes/fig12', base = process.argv[3] || 'http://localhost:8790'; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(), errs = [];
  const ignore = (t) => /cloudflareinsights/.test(t);   // Cloudflare's analytics, injected site-wide on the live site, blocked by the CSP
  for (const [name, vp] of [['desktop', { width: 1280, height: 900 }], ['phone', { width: 390, height: 844 }]]) {
    const p = await b.newPage({ viewport: vp, deviceScaleFactor: 2 });
    p.on('pageerror', e => errs.push(name + ': ' + e.message)); p.on('console', m => { if (m.type() === 'error' && !ignore(m.text())) errs.push(name + ' console: ' + m.text()); });
    await p.goto(base + '/simulations/beer-slosh.html'); await p.waitForTimeout(1200);
    const fig = await p.$('figure.stage');
    // at rest: road flat, cart standing
    await p.evaluate(() => { document.getElementById('play').click(); });
    await p.evaluate(() => { const s = document.getElementById('bumpH'); s.value = 0; s.dispatchEvent(new Event('input')); document.getElementById('reset').click(); });
    await p.waitForTimeout(1500); await fig.screenshot({ path: `${out}/shot-${name}-rest.png` });
    // a push in open loop: hold the push button for 0.6 s of simulated time, then let it swing
    await p.evaluate(() => { document.getElementById('ctrl-off').click(); });
    if ((await p.textContent('#play')) !== 'Pause') await p.click('#play');
    const btn = await p.$('#push-fwd'), bb = await btn.boundingBox();
    await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2); await p.mouse.down();
    await p.waitForFunction(() => Fig12.world.t > 1.2, null, { timeout: 60000 }); await p.mouse.up();
    await p.waitForFunction(() => Fig12.world.t > 1.6, null, { timeout: 60000 });
    const swing = await p.evaluate(() => ({ t: Fig12.world.t, dw: document.getElementById('r-dw').textContent }));
    await fig.screenshot({ path: `${out}/shot-${name}-push.png` });
    // spilling: 25 mm bumps, open loop, from the start
    await p.evaluate(() => { const s = document.getElementById('bumpH'); s.value = 25; s.dispatchEvent(new Event('input')); document.getElementById('reset').click(); document.getElementById('ctrl-off').click(); });
    await p.waitForFunction(() => (Fig12.world.spilledMass || 0) > 0.004, null, { timeout: 120000 });
    await p.waitForTimeout(400);
    const spill = await p.evaluate(() => ({ t: Fig12.world.t, sp: document.getElementById('r-sp').textContent, drops: (Fig12.world.drops || []).length, ds: Sim.data.ds.get('spilled_g') }));
    await fig.screenshot({ path: `${out}/shot-${name}-spill.png` });
    // the note: open every section, count KaTeX errors and formulas, measure sideways overflow
    await p.evaluate(() => { const x = [...document.querySelectorAll('button.fold-tool')].find(e => /Expand all/.test(e.textContent)); if (x) x.click(); });
    await p.waitForTimeout(800);
    const note = await p.evaluate(() => ({ katex: document.querySelectorAll('#paper .katex').length, errors: document.querySelectorAll('#paper .katex-error').length,
      errText: [...document.querySelectorAll('#paper .katex-error')].slice(0, 3).map(e => e.textContent.slice(0, 80)),
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth, svgs: document.querySelectorAll('#paper .pfig svg').length }));
    console.log(name, 'swing', JSON.stringify(swing), 'spill', JSON.stringify(spill), 'note', JSON.stringify(note));
    for (const id of ['p-slosh', 'p-speed', 'p-checks']) { const el = await p.$('#' + id); await el.screenshot({ path: `${out}/note-${name}-${id}.png` }); }
    await p.close();
  }
  console.log('errors:', errs.length ? errs.join('\n') : 'none'); await b.close();
})();
