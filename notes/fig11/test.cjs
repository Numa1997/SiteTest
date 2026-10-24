// Fig. 11 test, one language at 1400 and 390 px: page and KaTeX errors, sideways scroll, untranslated pieces, every data-panel
// check against the stored value (the panel's own rule), every read-back, a scripted drag of ball 2 that must settle at the
// rest y*(0.3 m), and the Read values rule (a pointer sweep with Read values off changes no pixel). Screenshots in notes/fig11/shots/.
// Usage: node notes/fig11/test.cjs en|de|ar
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '../../public');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); r.end(b); }); }).listen(0);
fs.mkdirSync(path.join(__dirname, 'shots'), { recursive: true });
(async () => {
  const lang = process.argv[2] || 'en', L = lang === 'en' ? '' : lang + '/'; let fail = 0;
  const b = await chromium.launch();
  for (const W of [1400, 390]) {
    const pg = await b.newPage({ viewport: { width: W, height: 1000 } }); const errs = [];
    pg.on('pageerror', e => errs.push(String(e))); pg.on('console', m => { if (m.type() === 'error' && !/404/.test(m.text())) errs.push(m.text()); });
    await pg.goto(`http://localhost:${server.address().port}/${L}simulations/pendulum-control.html`);
    await pg.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds.get('solve_ms') > 0 && document.querySelector('.paper.is-typeset'), null, { timeout: 30000 });
    await pg.waitForTimeout(500);
    const page = await pg.evaluate(() => ({ katexErr: document.querySelectorAll('.katex-error').length, pending: document.querySelectorAll('.i18n-pending').length,
      sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      coil: [...document.querySelectorAll('.panel__label')].map(e => e.innerText).find(t => /κ|K\s*=\s*10/.test(t)) || '', rk4: (document.getElementById('r-err').previousElementSibling || {}).innerText }));
    // data checks at a paused frame
    await pg.evaluate(() => { if (Sim.data.playing()) document.getElementById('play').click(); const s = document.getElementById('seek'); s.value = 400; s.dispatchEvent(new Event('input')); });
    await (await pg.$('#rig')).scrollIntoViewIfNeeded(); await pg.waitForTimeout(200);
    const data = await pg.evaluate(() => {
      function agree(a, v, f32) { if (typeof a !== 'number' || typeof v !== 'number') return String(a) === String(v); if (!isFinite(a) || !isFinite(v)) return String(a) === String(v);
        const d = Math.abs(a - v), s = Math.max(Math.abs(a), Math.abs(v), 1e-300); return d <= (f32 ? 2e-6 : 1e-9) * Math.max(s, 1e-12) + (f32 ? 1e-7 : 1e-12); }
      const ds = Sim.data.ds, bad = []; let n = 0;
      for (const name of Object.keys(ds.vars)) { const fn = Sim.data.check[name]; if (!fn) continue; const v = ds.get(name), arr = v && typeof v === 'object' && 'length' in v;
        for (const i of (arr ? [0, Math.floor(v.length / 2), v.length - 1, Math.min(v.length - 1, ds.get('i_now'))] : [0])) { n++; const c = fn(i); if (!agree(arr ? v[i] : v, c.value, v instanceof Float32Array)) bad.push(name + (arr ? '[' + i + ']' : '')); } }
      const drawn = Object.keys(Sim.data.drawn).map(k => k + ':' + Sim.data.drawn[k](ds.get('i_now')).ok);
      return { checks: n, bad, drawn };
    });
    // hover with Read values off: no pixel changes
    const rig = await pg.$('#rig'); let bb = await rig.boundingBox(); const s0 = await rig.screenshot();
    for (let k = 0; k <= 30; k++) await pg.mouse.move(bb.x + bb.width * k / 30, bb.y + bb.height * 0.35 + 25 * Math.sin(k));
    const hoverSame = Buffer.compare(s0, await rig.screenshot()) === 0; bb = await rig.boundingBox();
    // drag ball 2 sideways and up, hold, let go
    const g = k => pg.evaluate(k => Sim.data.ds.get(k), k);
    const bx = await g('b2_px'), by = await g('b2_py');
    await pg.mouse.move(bb.x + bx, bb.y + by); await pg.mouse.down();
    for (let k = 1; k <= 12; k++) { await pg.mouse.move(bb.x + bx - k * 6, bb.y + by - k * 2); await pg.waitForTimeout(30); }
    await pg.waitForTimeout(300); const held = await g('grabbed'); await pg.mouse.up(); await pg.waitForTimeout(500);
    const end = await pg.evaluate(() => { const d = Sim.data.ds, N = d.get('th1').length - 1, deg = 180 / Math.PI;
      return { released: d.get('released'), y0: Array.from(d.get('y0s')).map(v => +v.toFixed(4)), settle: d.get('t_settle'), th1: d.get('th1')[N] * deg, th2: d.get('th2')[N] * deg, X: d.get('Xs')[N], th1eq: d.get('th1_eq') * deg, th2eq: d.get('th2_eq') * deg, r: d.get('r') }; });
    const settled = end.released && isFinite(end.settle) && Math.abs(end.th1 - 5.78) < 0.01 && Math.abs(end.th2 - 8.36) < 0.01 && Math.abs(end.X - 0.30) < 0.001;
    const okDrawn = data.drawn.every(d => !/:false$|:undefined$/.test(d));
    const ok = !errs.length && !page.katexErr && !page.pending && page.sideways <= 0 && !data.bad.length && data.checks >= 152 && okDrawn && hoverSame && /ball 2/.test(held) && settled;
    if (!ok) fail++;
    console.log(`${lang} ${W}: ${ok ? 'PASS' : 'FAIL'} · errors ${errs.length} · KaTeX ${page.katexErr} · pending ${page.pending} · sideways ${page.sideways} px · checks ${data.checks - data.bad.length}/${data.checks} agree · read-backs ${data.drawn.join(' ')} · hover changes nothing: ${hoverSame} · held "${held}" · settled at t = ${end.settle} s, end θ1 = ${end.th1.toFixed(3)}°, θ2 = ${end.th2.toFixed(3)}°, X = ${end.X.toFixed(4)} m (rest ${end.th1eq.toFixed(2)}°, ${end.th2eq.toFixed(2)}°, r = ${end.r}) · coil heading "${page.coil}" · readout "${page.rk4}"${data.bad.length ? ' · DIFFER: ' + data.bad.join(', ') : ''}${errs.length ? ' · ' + errs[0] : ''}`);
    await pg.evaluate(() => window.scrollTo(0, 0)); await pg.waitForTimeout(200);
    await pg.screenshot({ path: path.join(__dirname, `shots/fig11-${lang}-${W}.png`) });
    await (await pg.$('.panel')).screenshot({ path: path.join(__dirname, `shots/fig11-panel-${lang}-${W}.png`) });
    await pg.close();
  }
  await b.close(); server.close(); process.exit(fail ? 1 : 0);
})();
