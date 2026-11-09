// Projects page in en/de/ar at 390 and 1100 px: page errors, KaTeX errors, pending translations, sideways scroll, the #electron-beam entry and
// its four plates loaded; screenshots of the entry. node notes/electron-beam/tools/check_projects.cjs OUTDIR
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..', '..', '..'), pub = path.join(ROOT, 'public'), out = process.argv[2];
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp' };
const srv = http.createServer((q, r) => { let f = path.join(pub, decodeURIComponent(q.url.split('?')[0])); if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html'); if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0, '127.0.0.1', async () => {
  const b = await chromium.launch(); let ok = true; fs.mkdirSync(out, { recursive: true });
  for (const lang of ['', 'de/', 'ar/']) for (const w of [390, 1100]) {
    const pg = await b.newPage({ viewport: { width: w, height: 900 } }); const errs = [], bad = [];
    pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); pg.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });
    await pg.goto('http://127.0.0.1:' + srv.address().port + '/' + lang + 'portfolios.html#electron-beam', { waitUntil: 'networkidle' });
    await pg.evaluate(() => { document.querySelectorAll('#electron-beam [aria-expanded="false"], #electron-beam .fold__toggle').forEach(x => x.click && x.click()); });
    await pg.waitForTimeout(800);
    const r = await pg.evaluate(() => ({ katex: document.querySelectorAll('.katex-error').length, pending: document.querySelectorAll('#electron-beam .i18n-pending').length,
      over: document.documentElement.scrollWidth - document.documentElement.clientWidth, entry: !!document.getElementById('electron-beam'),
      plates: Array.from(document.querySelectorAll('#electron-beam img')).map(i => i.complete && i.naturalWidth > 0), title: (document.querySelector('#eb-title') || {}).textContent }));
    const fail = errs.length || bad.length || r.katex || r.pending || r.over > 0 || !r.entry || r.plates.length !== 4 || r.plates.some(x => !x);
    ok = ok && !fail; console.log((fail ? 'FAIL ' : 'PASS ') + (lang || 'en/') + ' ' + w + ' ' + JSON.stringify(r) + (errs.length ? ' errors ' + errs.join('|') : '') + (bad.length ? ' bad ' + bad.join('|') : ''));
    await pg.locator('#electron-beam').screenshot({ path: path.join(out, 'projects-' + (lang.replace('/', '') || 'en') + '-' + w + '.png') });
    await pg.close();
  }
  await b.close(); srv.close(); console.log('PROJECTS CHECK ' + (ok ? 'PASS' : 'FAIL')); process.exit(ok ? 0 : 1);
});
