// Screenshot chosen sections of the Fig. 12 note. Usage: node notes/fig12/secshot.cjs width lang id [id …]
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); r.end(b); }); }).listen(0);
(async () => {
  const [W, lang, ...ids] = process.argv.slice(2); const L = lang && lang !== 'en' ? lang + '/' : '';
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: +W, height: 900 }, deviceScaleFactor: 1.5 });
  await pg.goto(`http://localhost:${server.address().port}/${L}simulations/furuta-pendulum.html`);
  await pg.waitForFunction(() => document.querySelector('.paper.is-typeset'), null, { timeout: 20000 }); await pg.waitForTimeout(800);
  await pg.addStyleTag({ content: '.fsec__band, .fold-bar, [class*="fsec__hd"] { position: static !important; }' });
  for (const id of ids) { const el = await pg.$('#' + id); await el.screenshot({ path: path.join(__dirname, `shots/sec-${id}-${W}${L ? '-' + lang : ''}.png`) }); }
  await b.close(); server.close();
})();
