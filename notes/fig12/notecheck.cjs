// Fig. 12 note check: display equations wider than their box, KaTeX errors, numbered equations, sideways scroll; screenshots of the note.
// Usage: node notes/fig12/notecheck.cjs [lang]
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); r.end(b); }); }).listen(0);
(async () => {
  const lang = process.argv[2] && process.argv[2] !== 'en' ? process.argv[2] : '';
  const b = await chromium.launch(); let bad = 0;
  for (const W of [1400, 390]) {
    const pg = await b.newPage({ viewport: { width: W, height: 900 } }); const errs = [];
    pg.on('pageerror', e => errs.push(String(e)));
    await pg.goto(`http://localhost:${server.address().port}/${lang ? lang + '/' : ''}simulations/furuta-pendulum.html`);
    await pg.waitForFunction(() => document.querySelector('.paper.is-typeset'), null, { timeout: 20000 });
    await pg.evaluate(() => { const x = [...document.querySelectorAll('.fold-tool')].find(e => /expand/i.test(e.textContent) || e.dataset.fold === 'expand'); if (x) x.click(); });
    await pg.waitForTimeout(800);
    const r = await pg.evaluate(() => { const p = document.querySelector('#paper');
      return { katexErr: document.querySelectorAll('.katex-error').length, tags: [...p.querySelectorAll('.katex-display .tag')].length,
        wide: [...p.querySelectorAll('.katex-display')].filter(d => d.scrollWidth > d.clientWidth + 1).map(d => (d.querySelector('.tag') || { textContent: '?' }).textContent.trim() + ' ' + d.scrollWidth + '/' + d.clientWidth),
        sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth }; });
    console.log(W, lang || 'en', JSON.stringify(r), errs);
    if (r.katexErr || r.sideways > 0 || errs.length || (W > 900 && r.wide.length)) bad++;
    await (await pg.$('#paper')).screenshot({ path: path.join(__dirname, `shots/paper-${W}${lang ? '-' + lang : ''}.png`) });
    await pg.close();
  }
  await b.close(); server.close(); process.exit(bad ? 1 : 0);
})();
