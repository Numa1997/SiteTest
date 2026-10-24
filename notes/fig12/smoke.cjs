// Fig. 12 smoke test: load the page from public/, report errors, key stored numbers, a screenshot.
// Usage: node notes/fig12/smoke.cjs [width] [lang]
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); r.end(b); }); }).listen(0);
(async () => {
  const W = +(process.argv[2] || 1400), lang = process.argv[3] || '', port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: 1000 } });
  const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  page.on('pageerror', e => errs.push(String(e)));
  await page.goto(`http://localhost:${port}/${lang ? lang + '/' : ''}simulations/furuta-pendulum.html`, { waitUntil: 'load' });
  await page.waitForTimeout(4000);
  const r = await page.evaluate(() => { const d = Sim.data.ds, g = k => d.get(k); return {
    solve_ms: g('solve_ms'), basin_ms: g('basin_ms'), c: g('c_meas'), t_catch: g('t_catch'), t_settle: g('t_settle'), swings: g('n_swings'), err: g('err_half'), err_t: g('err_end'), bal: g('balance'), tsat: g('t_sat'), basin_n: g('basin_n'), cin: g('c_in'),
    K: Array.from(g('Kg')), P: Array.from(g('Pm')), grow: g('grow'), slow: g('slow'), rank: g('rank'), wbot: g('w_bot'), status: document.getElementById('status').textContent,
    katexErr: document.querySelectorAll('.katex-error').length, sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth }; });
  console.log(JSON.stringify(r, null, 1)); console.log('errors:', errs);
  await page.evaluate(() => { document.getElementById('seek').value = 600; document.getElementById('seek').dispatchEvent(new Event('input')); });
  await page.waitForTimeout(300);
  const el = await page.$('.sim__grid'); await el.screenshot({ path: path.join(__dirname, `shots/smoke-${W}${lang ? '-' + lang : ''}.png`) });
  await browser.close(); server.close();
})();
