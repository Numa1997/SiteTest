// Home page, section "How this site is made" (#made): is it drawn, is every list filled from scripts/site-tools.js,
// and does it fit? node notes/home/made.cjs [en|de|ar]   (BASE=https://phyeinusul.com/ for the live site)
const { chromium } = require('playwright');
const lang = process.argv[2] || 'en', pre = lang === 'en' ? '' : lang + '/';
const URL = `${process.env.BASE || 'http://localhost:8765/'}${pre}index.html`;
(async () => {
  const b = await chromium.launch();
  for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } }), errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.goto(URL, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.getElementById('made').scrollIntoView()); await p.waitForTimeout(1200);
    const r = await p.evaluate(() => {
      const box = document.getElementById('made'), rows = [...box.querySelectorAll('[data-tools]')].filter(e => e.tagName === 'DD');
      const filled = rows.filter(d => d.textContent.trim()).length, hidden = rows.filter(d => d.parentNode.style.display === 'none').length;
      const rb = box.getBoundingClientRect();
      return { title: box.querySelector('h2').textContent, filled, hidden, rows: rows.length,
        date: box.querySelector('[data-tools="date"]').textContent, files: box.querySelector('[data-tools="files"]').textContent,
        engine: box.querySelector('[data-tools="engine"]').textContent, y: rb.top + scrollY, h: rb.height,
        pending: box.querySelectorAll('.i18n-pending').length, sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth };
    });
    await p.screenshot({ path: `notes/home/made-${lang}-${w}.png`, clip: { x: 0, y: r.y - 20, width: w, height: r.h + 40 }, fullPage: true });
    console.log(`${lang} ${w}: errors ${errs.length} · "${r.title}" · lists filled ${r.filled}/${r.rows - r.hidden} (${r.hidden} empty, hidden) · engine "${r.engine}" · read ${r.date}, ${r.files} files · pending ${r.pending} · sideways ${r.sideways} px`);
    await p.close();
  }
  await b.close();
})();
