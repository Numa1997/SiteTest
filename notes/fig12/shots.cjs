// Element screenshots of the three canvases of Fig. 12 at one width and language, at a chosen playback sample.
// Usage: node notes/fig12/shots.cjs width [lang] [sample]
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); r.end(b); }); }).listen(0);
(async () => {
  const W = +process.argv[2], lang = process.argv[3] && process.argv[3] !== 'en' ? process.argv[3] : '', n = +(process.argv[4] || 150);
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: W, height: 900 }, deviceScaleFactor: 2 });
  await pg.goto(`http://localhost:${server.address().port}/${lang ? lang + '/' : ''}simulations/furuta-pendulum.html`);
  await pg.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds.get('basin_n') > 0, null, { timeout: 30000 });
  await pg.evaluate(n => { document.getElementById('play').click(); const s = document.getElementById('seek'); s.value = n; s.dispatchEvent(new Event('input')); }, n);
  await pg.waitForTimeout(300);
  for (const id of ['stage', 'stage-force', 'stage-phase']) await (await pg.$('#' + id)).screenshot({ path: path.join(__dirname, `shots/${id}-${W}${lang ? '-' + lang : ''}.png`) });
  await b.close(); server.close();
})();
