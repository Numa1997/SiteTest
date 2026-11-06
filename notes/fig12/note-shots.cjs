// Fig. 12: opens the lecture note at 1280 and 390 px, counts KaTeX errors, checks for sideways scroll on the page and wide
// display equations, and screenshots §8.5. node notes/fig12/note-shots.cjs <out-dir> [base-url]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || 'notes/fig12/shots', base = process.argv[3] || 'http://localhost:8790';
  const b = await chromium.launch();
  for (const W of [1280, 390]) {
    const p = await b.newPage({ viewport: { width: W, height: 900 }, deviceScaleFactor: W === 390 ? 2 : 1 });
    await p.goto(base + '/simulations/beer-slosh.html'); await p.waitForTimeout(1500);
    await p.evaluate(() => document.querySelectorAll('details, .fold').forEach((d) => { if (d.tagName === 'DETAILS') d.open = true; }));
    await p.evaluate(() => { const b2 = document.querySelector('#paper button, .paper__toggle, [data-fold]'); if (b2) b2.click(); });
    await p.waitForTimeout(1500);
    const r = await p.evaluate(() => {
      const h = [...document.querySelectorAll('h4')].find((e) => /8\.5/.test(e.textContent));
      const sec = h ? h.closest('section') : null;
      const wide = [...document.querySelectorAll('.katex-display')].filter((e) => e.scrollWidth > e.clientWidth + 1 && sec && sec.contains(e)).length;
      if (h) h.scrollIntoView();
      return { err: document.querySelectorAll('.katex-error').length, sx: document.documentElement.scrollWidth > innerWidth, found: !!h, visible: h ? h.getBoundingClientRect().height > 0 : false, wide };
    });
    console.log(`${W} px: KaTeX errors ${r.err}, sideways scroll ${r.sx}, §8.5 found ${r.found} visible ${r.visible}, display equations in §8 wider than their box ${r.wide}`);
    for (let k = 0; k < (W === 390 ? 6 : 3); k++) { await p.screenshot({ path: `${out}/note85-${W}-${k}.png` }); await p.mouse.wheel(0, 850); await p.waitForTimeout(300); }
    await p.close();
  }
  await b.close();
})();
