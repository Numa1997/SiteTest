// The catalog thumbnail of Fig. 12: the rig canvas at one moment of the swing-up, cropped to 800 × 500 px (images/sims/furuta-pendulum.webp).
// Usage: node notes/fig12/thumb.cjs [sample]   then the WebP is written by the Python line at the end of this script's output
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2' };
const server = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); r.end(b); }); }).listen(0);
(async () => {
  const n = +(process.argv[2] || 230);
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2 });
  await pg.goto(`http://localhost:${server.address().port}/simulations/furuta-pendulum.html`);
  await pg.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds.get('basin_n') > 0, null, { timeout: 30000 });
  await pg.evaluate(n => { document.getElementById('play').click(); const s = document.getElementById('seek'); s.value = n; s.dispatchEvent(new Event('input')); }, n);
  await pg.waitForTimeout(300);
  const c = await pg.$('#rig'); await c.scrollIntoViewIfNeeded(); const bb = await c.boundingBox();
  const hub = await pg.evaluate(() => ({ x: Sim.data.ds.get('hub_px'), y: Sim.data.ds.get('hub_py'), s: Sim.data.ds.get('px_per_m') }));
  const w = 1.0 * hub.s, h = w * 5 / 8;   // 1.0 m wide in the rig's scale, 16 : 10, below the energy bars
  await pg.screenshot({ path: path.join(__dirname, 'shots/thumb.png'), clip: { x: bb.x + hub.x - 0.46 * w, y: bb.y + hub.y - 0.28 * hub.s, width: w, height: h } });
  await b.close(); server.close();
})();
