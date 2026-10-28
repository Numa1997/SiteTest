// Fig. 11: screenshot of §1.1 "How the cart brings the chain home" and its Figure 2, with KaTeX and page-error counts.
// node notes/fig11/note-shot.cjs [en|de|ar] [width]
const { chromium } = require('playwright');
const lang = process.argv[2] || 'en', w = +(process.argv[3] || 1400), pre = lang === 'en' ? '' : lang + '/';
(async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: w, height: 1000 } }), errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto(`${process.env.BASE || 'http://localhost:8765/'}${pre}simulations/pendulum-control.html`, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  const r = await p.evaluate(() => {
    const h = document.getElementById('p-home'), flow = document.querySelector('.eflow'), fig = flow.closest('.pfig'), sec = document.getElementById('p-leash');
    const hid = !h.offsetParent || !fig.offsetParent, top = h.getBoundingClientRect().top + scrollY - 12, end = fig.getBoundingClientRect().bottom + scrollY + 260;
    const fr = flow.getBoundingClientRect(), over = [], ts = [...flow.children].map(c => c.getBoundingClientRect());
    ts.forEach((a, i) => ts.slice(i + 1).forEach(c => { if (a.left < c.right - 0.5 && c.left < a.right - 0.5 && a.top < c.bottom - 0.5 && c.top < a.bottom - 0.5) over.push(i); }));
    const outside = ts.filter(t => t.left < fr.left - 1 || t.right > fr.right + 1).length + (flow.scrollWidth > flow.clientWidth + 1 ? 1 : 0);
    const words = [...flow.querySelectorAll('.eflow__box b')].map(b => b.textContent).join(' / ');
    return { hid, top, h: end - top, katex: sec.querySelectorAll('.katex-error').length, pending: sec.querySelectorAll('.i18n-pending').length, texts: ts.length, words, overlaps: over.length, outside, sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth };
  });
  await p.screenshot({ path: `notes/fig11/shots/note11-${lang}-${w}.png`, clip: { x: 0, y: r.top, width: w, height: Math.min(r.h, 4000) }, fullPage: true });
  const f1 = await p.evaluate(() => {
    const pl = document.querySelector('.fig1-lbl').closest('.pfig__plate'), pr = pl.getBoundingClientRect();
    const ls = [...pl.querySelectorAll('.fig1-lbl')].map(e => e.getBoundingClientRect());
    return { y: pr.top + scrollY, h: pr.height, n: ls.length, words: [...pl.querySelectorAll('.fig1-lbl')].map(e => e.textContent).join(' / '), out: ls.filter(r => r.left < pr.left - 1 || r.right > pr.right + 1 || r.bottom > pr.bottom + 1).length, px: Math.round(parseFloat(getComputedStyle(pl.querySelector('.fig1-lbl')).fontSize)) };
  });
  await p.screenshot({ path: `notes/fig11/shots/fig1-${lang}-${w}.png`, clip: { x: 0, y: f1.y, width: w, height: f1.h }, fullPage: true });
  const pt = await p.evaluate(() => { const h = document.querySelector('#p-parts'), card = h.closest('[data-card]') || h; const r = card.getBoundingClientRect(); return { y: r.top + scrollY, h: r.height }; });
  await p.screenshot({ path: `notes/fig11/shots/parts-${lang}-${w}.png`, clip: { x: 0, y: pt.y, width: w, height: Math.min(pt.h, 9000) }, fullPage: true });
  const tour = await p.evaluate(() => { const h = document.getElementById('p-parts'); return { shown: !!h.offsetParent, n: h.textContent.slice(0, 26) }; });
  console.log(`${lang} ${w}: Figure 1 labels ${f1.n} (${f1.words}) at ${f1.px} px, outside the drawing ${f1.out} · §1.1 heading shown ${tour.shown}: "${tour.n}"`);
  console.log(`${lang} ${w}: hidden by a fold ${r.hid} · errors ${errs.length} · KaTeX ${r.katex} · pending ${r.pending} · Figure 2: ${r.texts} parts (${r.words}), overlapping ${r.overlaps}, outside the plate ${r.outside} · sideways ${r.sideways} px`);
  await b.close();
})();
