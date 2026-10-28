// Home page: which prose elements run longest (characters per line), with their classes and computed max-width.
// node notes/home/longlines.cjs [width]
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(), w = +(process.argv[2] || 1440), p = await b.newPage({ viewport: { width: w, height: 900 } });
  await p.goto(`${process.env.BASE || 'http://localhost:8766/'}index.html`, { waitUntil: 'networkidle' });
  const r = await p.evaluate(() => [...document.querySelector('.content').querySelectorAll('p, dd, li, span, div')].filter(el => {
    const t = el.textContent.trim(); return t.length > 120 && el.offsetParent && el.children.length < 4;
  }).map(el => { const cs = getComputedStyle(el), lh = parseFloat(cs.lineHeight) || 1, lines = Math.max(1, Math.round(el.getBoundingClientRect().height / lh));
    return [Math.round(el.textContent.trim().length / lines), el.tagName.toLowerCase() + '.' + el.className, cs.maxWidth, Math.round(el.getBoundingClientRect().width), el.textContent.trim().slice(0, 50)]; })
    .sort((a, b) => b[0] - a[0]).slice(0, 8));
  r.forEach(x => console.log(x.join(' | ')));
  await b.close();
})();
