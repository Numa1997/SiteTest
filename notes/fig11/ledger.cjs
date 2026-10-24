// Gates of the bookkeeper (skill phyein-usul-bookkeeper, section 6) for the double pendulum under control, one language, 1440, 1100 and 390 px:
// console errors, the ledger is a <table> with header cells, 3–7 headline numbers, text rewritten at most ~4 times a second while playing and a
// headline number changing, the energy book's residual shown and inside its tolerance, the panel idle when closed, no sideways scroll, and at
// 1440 px a recorded round and a Save whose archive numpy reads. Screenshots of the open panel in notes/fig11/shots/.
// Usage: node notes/fig11/ledger.cjs en|de|ar
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const root = path.join(__dirname, '../../public');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); r.end(b); }); }).listen(0);
(async () => {
  const lang = process.argv[2] || 'en', L = lang === 'en' ? '' : lang + '/'; let fail = 0;
  const b = await chromium.launch();
  for (const W of [1440, 1100, 390]) {
    const pg = await b.newPage({ viewport: { width: W, height: 1000 }, acceptDownloads: true }); const errs = [];
    pg.on('pageerror', e => errs.push(String(e))); pg.on('console', m => { if (m.type() === 'error' && !/404/.test(m.text())) errs.push(m.text()); });
    await pg.goto(`http://localhost:${server.address().port}/${L}simulations/pendulum-control.html`);
    await pg.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds.get('solve_ms') > 0 && Sim.data.ledger, null, { timeout: 30000 });
    // drag ball 2 so the run has motion, then open the panel while it plays
    const rig = await pg.$('#rig'); await rig.scrollIntoViewIfNeeded(); const bb = await rig.boundingBox();
    const bx = await pg.evaluate(() => Sim.data.ds.get('b2_px')), by = await pg.evaluate(() => Sim.data.ds.get('b2_py'));
    await pg.mouse.move(bb.x + bx, bb.y + by); await pg.mouse.down(); for (let k = 1; k <= 10; k++) { await pg.mouse.move(bb.x + bx - 7 * k, bb.y + by - 2 * k); await pg.waitForTimeout(30); } await pg.mouse.up();
    await pg.waitForTimeout(300);
    await pg.evaluate(() => document.querySelector('.dp-tab').click()); await pg.waitForTimeout(600);
    const s = await pg.evaluate(async () => {
      const tbl = document.querySelector('.dp-ledger table.dp-tbl'), th = tbl ? tbl.querySelectorAll('thead th').length : 0, heads = document.querySelectorAll('.dp-hl__i').length;
      const body = document.querySelector('.dp-ledger'); let rewrites = 0; const mo = new MutationObserver(() => { rewrites++; }); mo.observe(body, { childList: true, characterData: true, subtree: true });
      const h0 = [...document.querySelectorAll('.dp-hl__v b')].map(e => e.textContent); let ticks = 0, last = body.innerText;
      const t0 = performance.now(); while (performance.now() - t0 < 3000) { await new Promise(r => setTimeout(r, 50)); const now = body.innerText; if (now !== last) { ticks++; last = now; } }
      mo.disconnect(); const h1 = [...document.querySelectorAll('.dp-hl__v b')].map(e => e.textContent);
      const book = document.querySelector('.dp-book'), pageRes = book && book.querySelector('[data-r="page"]').textContent, panelRes = book && book.querySelector('[data-r="panel"]').textContent;
      const d = Sim.data.ds, res = d.get('bal_now'), scale = Math.abs(d.get('E0')) + Math.abs(d.get('Wc_now')) + Math.abs(d.get('Qs_now')) + Math.abs(d.get('E_now'));
      return { table: !!tbl, th, heads, textChangesIn3s: ticks, headlineChanged: h0.join('|') !== h1.join('|'), playing: Sim.data.playing(), pageRes, panelRes, rel: Math.abs(res) / scale,
        sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth };
    });
    await pg.screenshot({ path: path.join(__dirname, `shots/ledger-${lang}-${W}.png`) });
    let saved = null;
    if (W === 1440) {
      const dl = pg.waitForEvent('download', { timeout: 20000 }).catch(() => null);
      await pg.evaluate(() => document.querySelector('.dp [data-save]').click()); const d = await dl;
      if (d) { const f = path.join(__dirname, `shots/save-${lang}.zip`); await d.saveAs(f);
        try { saved = execSync(`python3 -c "import zipfile,io,numpy as np,sys; z=zipfile.ZipFile(sys.argv[1]); assert z.testzip() is None; n=[x for x in z.namelist() if x.endswith('.npz')]; a=np.load(io.BytesIO(z.read(n[0]))) if n else None; print(len(z.namelist()),'files;', ('th1 %s, Kg %s, bal_now %s' % (a['th1'].shape, a['Kg'].shape, a['bal_now'].shape)) if a is not None else z.namelist()[:6])" ${f}`).toString().trim(); } catch (e) { saved = 'numpy failed: ' + String(e).slice(0, 120); } }
      else saved = 'no download';
    }
    await pg.evaluate(() => { const c = document.querySelector('.dp__close'); if (c) c.click(); }); await pg.waitForTimeout(400);
    const idle = await pg.evaluate(() => window.__dataPanel.running());
    const ok = !errs.length && s.table && s.th >= 4 && s.heads >= 3 && s.heads <= 7 && s.textChangesIn3s <= 14 && s.headlineChanged && s.rel <= 1e-8 && /e|0/.test(s.pageRes || '') && !idle && s.sideways <= 0 && (W !== 1440 || /files/.test(saved || ''));
    if (!ok) fail++;
    console.log(`${lang} ${W}: ${ok ? 'PASS' : 'FAIL'} · errors ${errs.length} · table ${s.table} with ${s.th} header cells · headline ${s.heads} · text rewrites in 3 s ${s.textChangesIn3s} · headline changed ${s.headlineChanged} · book residual: page ${s.pageRes}, panel ${s.panelRes}, relative ${s.rel.toExponential(1)} (tol 1e-8) · idle when closed ${!idle} · sideways ${s.sideways} px${saved ? ' · save: ' + saved : ''}${errs.length ? ' · ' + errs[0] : ''}`);
    await pg.close();
  }
  await b.close(); server.close(); process.exit(fail ? 1 : 0);
})();
