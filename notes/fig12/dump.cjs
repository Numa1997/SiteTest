// Dump every scalar of the Fig. 12 store at the page's defaults (and for a few variants) as JSON: the numbers the note quotes.
// Usage: node notes/fig12/dump.cjs > notes/fig12/numbers.json
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public');
const server = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': p.endsWith('.html') ? 'text/html' : p.endsWith('.js') ? 'text/javascript' : 'application/octet-stream' }); r.end(b); }); }).listen(0);
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1400, height: 900 } });
  await pg.goto(`http://localhost:${server.address().port}/simulations/furuta-pendulum.html`);
  await pg.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds.get('basin_n') > 0, null, { timeout: 30000 });
  const snap = () => pg.evaluate(() => { const d = Sim.data.ds, o = {}; Object.keys(d.vars).forEach(k => { const v = d.get(k); if (typeof v !== 'object' || v === null) o[k] = v; else if (v.length <= 16) o[k] = Array.from(v); }); return o; });
  const out = { defaults: await snap() };
  const set = (id, v) => pg.evaluate(([id, v]) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('input')); e.dispatchEvent(new Event('change')); }, [id, v]);
  const press = (sel) => pg.evaluate(s => document.querySelector(s).click(), sel);
  await press('[data-preset="catch"]'); await pg.evaluate(() => document.getElementById('solve').click()); out.catchFromHanging = await snap();
  await press('[data-preset="off"]'); await pg.evaluate(() => document.getElementById('solve').click()); out.off = await snap();
  await press('[data-preset="swing"]'); await set('rho', 1); await pg.evaluate(() => document.getElementById('solve').click()); out.rho10 = await snap();
  await set('rho', 0); await set('ra', 0.02); await pg.evaluate(() => document.getElementById('solve').click()); out.r002 = await snap();
  await set('ra', 0.16); await set('vmax', 6); await pg.evaluate(() => document.getElementById('solve').click()); out.v6 = await snap();
  await set('vmax', 12); await set('kE', 0); await pg.evaluate(() => document.getElementById('solve').click()); out.kE0 = await snap();
  console.log(JSON.stringify(out, null, 1)); await b.close(); server.close();
})();
