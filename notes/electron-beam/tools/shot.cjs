// Screenshot one element of the built project-07 page (for the finisher's own look; scale 1).
//   node notes/electron-beam/tools/shot.cjs SELECTOR WIDTH OUT.png [maxHeight]
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..', '..', '..'), pub = path.join(ROOT, 'public');
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.png': 'image/png', '.webp': 'image/webp' };
const [sel, W, out, maxH] = process.argv.slice(2);
const srv = http.createServer((q, r) => { let f = path.join(pub, decodeURIComponent(q.url.split('?')[0])); if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html'); if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0, '127.0.0.1', async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: +W, height: 1000 } });
  const errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://127.0.0.1:' + srv.address().port + '/portfolios/electron-beam/index.html', { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(600);
  const el = pg.locator(sel).first(); await el.scrollIntoViewIfNeeded(); await pg.waitForTimeout(400);
  const bb = await el.boundingBox();
  await pg.screenshot({ path: out, fullPage: true, clip: { x: bb.x, y: bb.y + await pg.evaluate(() => scrollY), width: bb.width, height: Math.min(bb.height, +(maxH || 2400)) } });
  console.log('shot', out, Math.round(bb.width), Math.round(bb.height), errs.length ? 'ERRORS ' + errs.join(' | ') : 'no errors');
  await b.close(); srv.close();
});
