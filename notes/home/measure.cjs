// Home page proportions, measured: index panel size and type, content column width, characters per line of the prose,
// and whether anything scrolls sideways. node notes/home/measure.cjs [tag] [en|de|ar]   (serves dist/ on :8766, or BASE=...)
const { chromium } = require('playwright');
const tag = process.argv[2] || 'now', lang = process.argv[3] || 'en';
const URL = `${process.env.BASE || 'http://localhost:8766/'}${lang === 'en' ? '' : lang + '/'}index.html`;
(async () => {
  const b = await chromium.launch();
  for (const [w, h] of [[1920, 1080], [1440, 900], [1280, 800], [1024, 768], [390, 844]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } }), errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.goto(URL, { waitUntil: 'networkidle' }); await p.waitForTimeout(600);
    await p.evaluate(() => document.getElementById('positions') && document.getElementById('positions').scrollIntoView()); await p.waitForTimeout(700);
    const r = await p.evaluate(() => {
      const ix = document.querySelector('.index'), a = ix && ix.querySelector('a'), cs = a && getComputedStyle(a), main = document.querySelector('.content') || document.querySelector('main');
      const ir = ix.getBoundingClientRect(), mr = main.getBoundingClientRect();
      // characters per line of the prose paragraphs: text length / number of line boxes
      const cpl = [];
      for (const el of main.querySelectorAll('p, dd, li')) {
        const t = el.textContent.trim(); if (t.length < 120 || !el.offsetParent) continue;
        const lh = parseFloat(getComputedStyle(el).lineHeight) || 1, lines = Math.round(el.getBoundingClientRect().height / lh);
        if (lines >= 2) cpl.push(t.length / lines);
      }
      cpl.sort((x, y) => x - y);
      return { index: Math.round(ir.width) + '×' + Math.round(ir.height), indexFont: cs ? cs.fontSize + ' ' + cs.fontFamily.split(',')[0] + ' ' + cs.textTransform : '-',
        content: Math.round(mr.left) + '…' + Math.round(mr.right), body: getComputedStyle(document.body).fontSize,
        cpl: cpl.length ? Math.round(cpl[Math.floor(cpl.length / 2)]) + ' median, ' + Math.round(cpl[cpl.length - 1]) + ' max' : '-',
        sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth };
    });
    await p.screenshot({ path: `notes/home/${tag}-${lang}-${w}.png` });
    console.log(`${tag} ${lang} ${w}: errors ${errs.length} · index ${r.index} px, links ${r.indexFont} · content x ${r.content} · body ${r.body} · prose ${r.cpl} characters per line · sideways ${r.sideways} px`);
    await p.close();
  }
  await b.close();
})();
