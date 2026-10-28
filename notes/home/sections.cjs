// Home page: one screenshot per section (hero, simulations, skills, footer) at a given width, to look at proportions.
// node notes/home/sections.cjs [tag] [width] [en|de|ar]
const { chromium } = require('playwright');
const tag = process.argv[2] || 'now', w = +(process.argv[3] || 1440), lang = process.argv[4] || 'en';
(async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: w, height: 900 } });
  await p.goto(`${process.env.BASE || 'http://localhost:8766/'}${lang === 'en' ? '' : lang + '/'}index.html`, { waitUntil: 'networkidle' });
  for (const id of ['top', 'simulations', 'skills']) {
    await p.evaluate(i => { const e = document.getElementById(i); if (e) e.scrollIntoView(); else scrollTo(0, 0); }, id); await p.waitForTimeout(1400);
    await p.screenshot({ path: `notes/home/${tag}-${id}-${lang}-${w}.png` });
  }
  await b.close();
})();
