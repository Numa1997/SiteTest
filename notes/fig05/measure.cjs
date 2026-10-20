// Fig. 5 note: measure the page's numbers in headless Chromium, and check the page after editing.
// Usage: node notes/fig05/measure.cjs  (serves /tmp/fig05-dist on port 8705)
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const ROOT = '/tmp/fig05-dist', PORT = 8705;
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json', '.png': 'image/png' };
const srv = http.createServer((q, r) => {
  let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  const f = path.join(ROOT, p);
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); });
});
const shot = process.argv[2] || '';
(async () => {
  await new Promise(res => srv.listen(PORT, res));
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = {};
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    const errs = [];
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('pageerror', e => errs.push(String(e)));
    await page.goto(`http://localhost:${PORT}/simulations/water-wave.html`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    const r = await page.evaluate(async () => {
      const ds = Sim.data.ds, g = n => ds.get(n);
      const res = {};
      res.defaults = { f: g('f'), k_m: g('k_m'), c: g('c'), T: g('T'), omega: g('omega'), cg: g('cg'), a: g('a'), ak: g('ak'), stokes: g('stokes'), deep: g('deep'), r_z: Array.from(g('r_z')), N: g('N'), layers: g('layers'), parcels: g('N') * g('layers'), world_w: g('world_w'), box_w: g('box_w'), box_h: g('box_h'), follow: g('follow'), X0_follow: g('X0')[g('follow')], layers_drawn: g('layers_drawn'), aomega_mps: g('a') * g('omega') / 100 };
      // surface points per frame: the loop for (X = -60; X <= WORLD_W + 60; X += 3) in draw(), counted for this field width
      let n = 0; for (let X = -60; X <= g('world_w') + 60; X += 3) n++; res.defaults.surface_points = n;
      res.readouts = { c: document.getElementById('r-c').textContent, T: document.getElementById('r-t').textContent, ak: document.getElementById('r-ak').textContent, deep: document.getElementById('r-deep').textContent };
      // set a slider and fire its input event, then read back
      const set = (id, v) => { const el = document.getElementById(id); el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); };
      const rd = () => ({ c: document.getElementById('r-c').textContent, T: document.getElementById('r-t').textContent, ak: document.getElementById('r-ak').textContent, deep: document.getElementById('r-deep').textContent, f: document.getElementById('freq').value });
      set('lambda', 120); res.lam120 = rd(); set('lambda', 400); res.lam400 = rd(); set('lambda', 260);
      set('amp', 50); res.amp50 = Object.assign(rd(), { a: g('a'), ak: g('ak') }); set('amp', 24);
      const disp = document.getElementById('disp'); disp.checked = false; disp.dispatchEvent(new Event('change')); set('freq', 0.5); res.dispOff = Object.assign(rd(), { cg_stored: g('cg'), c_deep: g('c_deep') });
      disp.checked = true; disp.dispatchEvent(new Event('change')); res.dispOn = rd();
      return res;
    });
    // after-edit checks: all folds open, katex errors, sideways scroll, refs
    const chk = await page.evaluate(async () => {
      const btn = t => [...document.querySelectorAll('button')].find(b => new RegExp(t, 'i').test(b.textContent));
      const wait = ms => new Promise(r => setTimeout(r, ms));
      btn('collapse all').click(); await wait(300);
      // open every fold of the note and the walkthrough by its own toggle, outermost first, and check it reports open
      const toggles = [...document.querySelectorAll('#paper .fs-toggle, #walk .fs-toggle')];
      let opened = 0, failed = [];
      for (const t of toggles) { if (t.getAttribute('aria-expanded') !== 'true') t.click(); await wait(450);
        const node = t.closest('[data-collapsed]'); if (t.getAttribute('aria-expanded') === 'true' && node && node.getAttribute('data-collapsed') === '0') opened++; else failed.push(t.getAttribute('data-label')); }
      btn('expand all').click(); await wait(300);
      const secs = [...document.querySelectorAll('#paper .psec')];
      const closed = { toggles: toggles.length, opened, failed, stillClosed: document.querySelectorAll('#paper [data-open="0"], #walk [data-open="0"]').length };
      return { katexErrors: document.querySelectorAll('#paper .katex-error').length, katex: document.querySelectorAll('#paper .katex').length,
        sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth, sections: secs.length, foldsShort: closed,
        refs: [...document.querySelectorAll('#paper .prefs li')].map(li => ({ text: li.textContent.slice(0, 60), links: [...li.querySelectorAll('a')].map(a => a.href) })),
        eqTags: [...document.querySelectorAll('#paper .katex-display .tag')].map(t => t.textContent.trim()) };
    });
    if (shot) {
      for (const id of shot.split(',')) {
        const el = await page.$('#' + id); if (el) { await el.scrollIntoViewIfNeeded(); await page.waitForTimeout(300); await el.screenshot({ path: `/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/fig05-${id}-${w}.png` }); }
      }
    }
    out[`${w}x${h}`] = { errors: errs, measure: r, check: chk };
    await page.close();
  }
  await browser.close(); srv.close();
  console.log(JSON.stringify(out, null, 1));
})();
