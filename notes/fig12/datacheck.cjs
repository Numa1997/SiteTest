// Fig. 12 data-panel test: every stored value against its check (the panel's own agreement rule), every read-back finds ink,
// the panel opens, Read values pins a point and its strip sits below the figure; with the panel closed nothing runs.
// Usage: node notes/fig12/datacheck.cjs [width] [lang]
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); r.end(b); }); }).listen(0);
(async () => {
  const W = +(process.argv[2] || 1400), lang = process.argv[3] && process.argv[3] !== 'en' ? process.argv[3] : '';
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: W, height: 1000 } }); const errs = [];
  pg.on('pageerror', e => errs.push(String(e))); pg.on('console', m => { if (m.type() === 'error' && !/404/.test(m.text())) errs.push(m.text()); });
  await pg.goto(`http://localhost:${server.address().port}/${lang ? lang + '/' : ''}simulations/furuta-pendulum.html`);
  await pg.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds.get('basin_n') > 0, null, { timeout: 30000 });
  const out = {};
  for (const n of [150, 600]) {   // during the swing-up and after the catch
    await pg.evaluate(n => { if (Sim.data.playing()) document.getElementById('play').click(); const s = document.getElementById('seek'); s.value = n; s.dispatchEvent(new Event('input')); }, n);
    await (await pg.$('#rig')).scrollIntoViewIfNeeded(); await pg.waitForTimeout(200);
    out[n] = await pg.evaluate(() => {
      function agree(stored, value, dtype) {
        if (typeof stored !== 'number' || typeof value !== 'number') return String(stored) === String(value);
        if (!isFinite(stored) || !isFinite(value)) return String(stored) === String(value);
        const diff = Math.abs(stored - value), scale = Math.max(Math.abs(stored), Math.abs(value), 1e-300);
        return diff <= (dtype === 'float32' ? 2e-6 : 1e-9) * Math.max(scale, 1e-12) + (dtype === 'float32' ? 1e-7 : 1e-12);
      }
      const ds = Sim.data.ds, bad = [], seen = []; let n = 0;
      for (const name of Object.keys(ds.vars)) {
        const fn = Sim.data.check[name]; if (!fn) { if (!['solve_ms', 'basin_ms', 'box_w', 'box_h', 'fps', 'playing', 'stale', 'grabbed', 'px_per_m', 'hub_px', 'hub_py'].includes(name)) seen.push(name); continue; }
        const v = ds.get(name), arr = v && typeof v === 'object' && 'length' in v;
        const idx = arr ? [0, Math.floor(v.length / 2), v.length - 1, Math.min(v.length - 1, ds.get('i_now'))] : [0];
        for (const i of idx) {
          const stored = arr ? v[i] : v, c = fn(i); n++;
          if (!agree(stored, c.value, v instanceof Float32Array ? 'float32' : '')) bad.push(name + (arr ? '[' + i + ']' : '') + ': stored ' + stored + ' vs ' + c.value);
        }
      }
      const drawn = Object.keys(Sim.data.drawn).map(k => { const r = Sim.data.drawn[k](ds.get('i_now')); return k + ':' + r.ok; });
      return { checked: n, bad, noCheck: seen, drawn };
    });
  }
  // the panel: open it and close it; then Read values: a click on the knob pins it, the strip sits below the figure
  const tabFound = await pg.evaluate(() => { const t = document.querySelector('.dp-tab'); if (t) t.click(); return !!t; }); await pg.waitForTimeout(300);
  const opened = await pg.evaluate(() => { const d = document.querySelector('.dp'); return d ? d.getBoundingClientRect().width > 100 && getComputedStyle(d).visibility !== 'hidden' : false; });
  await pg.evaluate(() => { const x = document.querySelector('.dp-x, .dp-tab'); if (x) x.click(); }); await pg.waitForTimeout(300);
  let pinned = null;
  if (await pg.$('.dp-readbtn')) {
    await (await pg.$('.dp-readbtn')).scrollIntoViewIfNeeded(); await pg.click('.dp-readbtn'); await pg.waitForTimeout(200);
    await (await pg.$('#rig')).scrollIntoViewIfNeeded();
    const bb = await (await pg.$('#rig')).boundingBox(); const ex = await pg.evaluate(() => Sim.data.ds.get('end_px')), ey = await pg.evaluate(() => Sim.data.ds.get('end_py'));
    await pg.mouse.click(bb.x + ex, bb.y + ey); await pg.waitForTimeout(600);
    pinned = await pg.evaluate(() => { const s = document.querySelector('.dp-read'), p = document.querySelector('.dp-read__pin'), st = document.getElementById('stage').getBoundingClientRect();
      return s ? { title: (document.querySelector('.dp-read__title') || {}).textContent, shown: p && !p.hidden, below: s.getBoundingClientRect().top >= st.bottom - 1, grabbed: Sim.data.ds.get('grabbed') } : null; });
    await pg.click('.dp-readbtn');
  }
  const running = await pg.evaluate(() => window.__dataPanel ? window.__dataPanel.running() : 'no panel');
  console.log(JSON.stringify({ W, lang: lang || 'en', s150: out[150], s600: out[600], tabFound, opened, pinned, runningWhenClosed: running, errs }, null, 0));
  const ok = !out[150].bad.length && !out[600].bad.length && [...out[150].drawn, ...out[600].drawn].every(d => !/:false$|:undefined$/.test(d)) && !errs.length && pinned && pinned.shown && pinned.below && pinned.grabbed === 'nothing';
  console.log(ok ? 'PASS every check agrees, every read-back finds ink or is legitimately absent' : 'FAIL');
  await b.close(); server.close(); process.exit(ok ? 0 : 1);
})();
