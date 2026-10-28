// Fig. 11: screenshot of §1.1 "How the cart brings the chain home" and its Figure 2, with KaTeX and page-error counts.
// node notes/fig11/note-shot.cjs [en|de|ar] [width]
const { chromium } = require('playwright');
const lang = process.argv[2] || 'en', w = +(process.argv[3] || 1400), pre = lang === 'en' ? '' : lang + '/';
(async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: w, height: 1000 } }), errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto(`http://localhost:8765/${pre}simulations/pendulum-control.html`, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  const r = await p.evaluate(() => {
    const h = document.getElementById('p-home'), fig = document.getElementById('ah-home').closest('.pfig'), sec = document.getElementById('p-leash');
    const hid = !h.offsetParent || !fig.offsetParent, top = h.getBoundingClientRect().top + scrollY - 12, end = fig.getBoundingClientRect().bottom + scrollY + 260;
    const svg = [...fig.querySelectorAll('svg')].find(v => v.getBoundingClientRect().width > 0), sr = svg.getBoundingClientRect(), over = [];
    const ts = [...svg.querySelectorAll('text')].map(t => t.getBoundingClientRect());
    ts.forEach((a, i) => ts.slice(i + 1).forEach(c => { if (a.left < c.right && c.left < a.right && a.top < c.bottom && c.top < a.bottom) over.push(i); }));
    const outside = ts.filter(t => t.left < sr.left - 1 || t.right > sr.right + 1).length;
    return { hid, top, h: end - top, katex: sec.querySelectorAll('.katex-error').length, pending: sec.querySelectorAll('.i18n-pending').length, texts: ts.length, overlaps: over.length, outside, sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth };
  });
  await p.screenshot({ path: `notes/fig11/shots/note11-${lang}-${w}.png`, clip: { x: 0, y: r.top, width: w, height: Math.min(r.h, 4000) }, fullPage: true });
  console.log(`${lang} ${w}: hidden by a fold ${r.hid} · errors ${errs.length} · KaTeX ${r.katex} · pending ${r.pending} · Figure 2 texts ${r.texts}, overlapping ${r.overlaps}, outside the plate ${r.outside} · sideways ${r.sideways} px`);
  await b.close();
})();
