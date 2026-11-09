// Makes the plates of project 07's entry on the Projects page from the built page's own figures (scale 2, white plate), as PNG
// in the scratch folder given; tools/plates.py-style conversion to WebP follows with Pillow.
//   node notes/electron-beam/tools/plates.cjs OUTDIR '#fig-a' name-a '#fig-b' name-b ...
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..', '..', '..'), pub = path.join(ROOT, 'public');
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.woff2': 'font/woff2' };
const [out, ...pairs] = process.argv.slice(2);
const srv = http.createServer((q, r) => { let f = path.join(pub, decodeURIComponent(q.url.split('?')[0])); if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html'); if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0, '127.0.0.1', async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 2 });
  await pg.goto('http://127.0.0.1:' + srv.address().port + '/portfolios/electron-beam/index.html', { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  fs.mkdirSync(out, { recursive: true });
  for (let i = 0; i < pairs.length; i += 2) {
    const el = pg.locator(pairs[i]).first(); await el.scrollIntoViewIfNeeded(); await pg.waitForTimeout(700);
    await el.screenshot({ path: path.join(out, pairs[i + 1] + '.png') }); console.log('plate', pairs[i + 1]);
  }
  await b.close(); srv.close();
});
