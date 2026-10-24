// Fig. 12 translation check in one language at 1400 and 390 px: pending pieces, page errors, KaTeX errors, sideways scroll,
// English left in visible text, and the data panel present. Usage: node notes/fig12/i18ncheck.cjs de|ar|en
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); r.end(b); }); }).listen(0);
(async () => {
  const lang = process.argv[2]; const L = lang === 'en' ? '' : lang + '/'; let bad = 0;
  const b = await chromium.launch();
  for (const W of [1400, 390]) {
    const pg = await b.newPage({ viewport: { width: W, height: 900 } }); const errs = [];
    pg.on('pageerror', e => errs.push(String(e))); pg.on('console', m => { if (m.type() === 'error' && !/404/.test(m.text())) errs.push(m.text()); });
    await pg.goto(`http://localhost:${server.address().port}/${L}simulations/furuta-pendulum.html`);
    await pg.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds.get('basin_n') > 0 && document.querySelector('.paper.is-typeset'), null, { timeout: 30000 });
    const r = await pg.evaluate(() => {
      const visible = document.body.innerText;
      const en = (visible.match(/\b(the|and|which|with|of)\b/g) || []).length;
      return { lang: document.documentElement.lang, dir: document.documentElement.dir, pending: document.querySelectorAll('.i18n-pending').length,
        katexErr: document.querySelectorAll('.katex-error').length, sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        panel: !!document.querySelector('.dp-tab'), englishWords: en, status: document.getElementById('status').textContent.slice(0, 70) };
    });
    const ok = !errs.length && !r.pending && !r.katexErr && r.sideways <= 0 && r.panel;
    if (!ok) bad++;
    console.log(`i18n  ${lang} ${W}: ${ok ? 'PASS' : 'FAIL'} ${JSON.stringify(r)} ${errs.slice(0, 2).join(' | ')}`);
    await pg.screenshot({ path: path.join(__dirname, `shots/i18n-${lang}-${W}.png`) });
    await pg.close();
  }
  await b.close(); server.close(); process.exit(bad ? 1 : 0);
})();
