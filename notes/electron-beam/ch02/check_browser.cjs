// Browser check of the chapter-2 preview: node notes/electron-beam/ch02/check_browser.cjs [port]
// 4 widths (360, 390, 1024, 1440 px): console and page errors, KaTeX errors, sideways scroll, requests outside the site,
// canvases drawn (alpha before colour), the simulation's stored numbers against the NumPy reference, and screenshots.
const { chromium } = require('playwright'), path = require('path'), fs = require('fs'), { spawn, execFileSync } = require('child_process');
const HERE = __dirname, ROOT = path.join(HERE, '..', '..', '..'), PORT = process.argv[2] || '8765';
const SHOTS = path.join(HERE, '..', 'shots'); fs.mkdirSync(SHOTS, { recursive: true });
(async () => {
  const srv = spawn('python3', [path.join(HERE, 'serve.py'), PORT], { stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 800));
  const browser = await chromium.launch(); let bad = 0; const fail = m => { bad++; console.log('FAIL ' + m); };
  for (const w of [360, 390, 1024, 1440]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 }), page = await ctx.newPage();
    const errs = [], reqs = [], logs = [];
    page.on('pageerror', e => errs.push('pageerror: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    page.on('request', r => { const u = new URL(r.url()); if (u.origin !== 'http://127.0.0.1:' + PORT && !r.url().startsWith('data:')) reqs.push(r.url()); });
    page.on('requestfailed', r => errs.push('requestfailed: ' + r.url()));
    await page.goto(`http://127.0.0.1:${PORT}/__preview/index.html`, { waitUntil: 'load' });
    await page.waitForFunction(() => window.EB_CH02_STORE && window.EB_CH02_STORE.handover && window.EB_CH02_STORE.handover.I_e, null, { timeout: 30000 });
    await page.waitForTimeout(1500);
    const r = await page.evaluate(() => {
      const sw = document.documentElement.scrollWidth, iw = window.innerWidth;
      const katexErr = document.querySelectorAll('.katex-error').length, katexN = document.querySelectorAll('.katex').length;
      const wide = [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); return b.right > iw + 1 && !e.closest('.katex-display') && !e.closest('.ptab-wrap') && getComputedStyle(e).position !== 'fixed'; }).slice(0, 5).map(e => e.tagName + '.' + e.className + ' ' + Math.round(e.getBoundingClientRect().right));
      const canv = ['eb-tip', 'eb-fn', 'eb-en', 'eb-tm'].map(id => { const c = document.getElementById(id), g = c.getContext('2d'), d = g.getImageData(0, 0, c.width, c.height).data; let a = 0, wine = 0; for (let i = 0; i < d.length; i += 4) { if (d[i + 3] > 0) { a++; if (d[i] > 100 && d[i] < 140 && d[i + 1] < 60 && d[i + 2] < 70) wine++; } } return { id, w: c.width, h: c.height, drawn: a, wine }; });
      const S = window.EB_CH02_STORE;
      return { sw, iw, katexErr, katexN, wide, canv, I_e: S.handover.I_e.value, B_r: S.handover.B_r.value, dE: S.handover.dE.value, d_v: S.handover.d_v.value, theta: S.timeline.theta.value, t: S.timeline.t.value,
               readI: document.getElementById('eb-o-I').textContent, readdE: document.getElementById('eb-o-dE').textContent, title: document.title,
               overflowX: [...document.querySelectorAll('.pfig svg, .ebsim canvas')].filter(e => e.getBoundingClientRect().right > iw + 1).length };
    });
    if (errs.length) fail(`${w}px page/console errors: ` + errs.slice(0, 4).join(' | '));
    if (reqs.length) fail(`${w}px requests outside the site: ` + reqs.slice(0, 3).join(' '));
    if (r.katexErr) fail(`${w}px KaTeX errors: ${r.katexErr}`);
    if (r.sw > r.iw + 1) fail(`${w}px sideways scroll: scrollWidth ${r.sw} > ${r.iw}; wide: ${r.wide.join('; ')}`);
    r.canv.forEach(c => { if (c.drawn < 500) fail(`${w}px canvas ${c.id} looks blank (${c.drawn} non-transparent pixels)`); if (c.wine < 20 && c.id !== 'eb-tip') fail(`${w}px canvas ${c.id} has no wine curve (${c.wine})`); });
    console.log(`${w}px: katex ${r.katexN} formulas, errors ${r.katexErr}, scroll ${r.sw}/${r.iw}, canvases drawn ${r.canv.map(c => c.id + ':' + c.drawn).join(' ')}, theta ${r.theta.toFixed(4)} at t=${r.t.toFixed(1)} s, I_e ${r.I_e.toExponential(4)} A (readout "${r.readI}"), B_r ${r.B_r.toExponential(3)}, dE ${r.dE.toFixed(4)} eV, d_v ${r.d_v.toFixed(3)} nm`);
    if (w === 1440 || w === 360) {
      await page.screenshot({ path: path.join(SHOTS, `ch02-top-${w}.png`) });
      const sim = await page.$('#ebsim'); await sim.scrollIntoViewIfNeeded(); await page.waitForTimeout(600); await sim.screenshot({ path: path.join(SHOTS, `ch02-sim-${w}.png`) });
    }
    if (w === 1440) {                      // numbers: page store at theta ~ 0 against the NumPy reference
      await page.evaluate(() => { document.getElementById('eb-scrub').value = 0; document.getElementById('eb-scrub').dispatchEvent(new Event('input')); });
      await page.waitForTimeout(700);
      const S = await page.evaluate(() => { const s = window.EB_CH02_STORE; return { th: s.timeline.theta.value, I: s.handover.I_e.value, B: s.handover.B_r.value, dE: s.handover.dE.value, dv: s.handover.d_v.value }; });
      const py = JSON.parse(execFileSync('python3', ['-c', `
import importlib.util, json, math
sp = importlib.util.spec_from_file_location('r', '${path.join(ROOT, 'portfolios-src', 'electron-beam', 'ref', 'ch02.py').replace(/\\/g, '/')}'); R = importlib.util.module_from_spec(sp); sp.loader.exec_module(R)
h = R.handover(1000.0, 50e-9, 5.0, 4.5 * R.eV, 300.0)
print(json.dumps({'I': R.tip_current(1000.0, 50e-9, 5.0, 4.5 * R.eV, 300.0, nodes=16), 'B': h['B_r'], 'dE': h['dE_eV'], 'dv': h['d_v'] * 1e9}))`]).toString());
      const rel = (a, b) => Math.abs(a - b) / Math.abs(b);
      console.log(`  store at theta=${S.th.toExponential(2)} vs NumPy reference: I_e ${rel(S.I, py.I).toExponential(1)}, B_r ${rel(S.B, py.B).toExponential(1)}, dE ${rel(S.dE, py.dE).toExponential(1)}, d_v ${rel(S.dv, py.dv).toExponential(1)}`);
      if (S.th > 1e-3) console.log('  (cursor not at 0: theta > 1e-3, comparison is for the mixed state)');
      else if (rel(S.I, py.I) > 2e-3 || rel(S.B, py.B) > 2e-3 || rel(S.dE, py.dE) > 0.03 || rel(S.dv, py.dv) > 0.02) fail('store differs from the reference');
    }
    await ctx.close();
  }
  await browser.close(); srv.kill();
  console.log(bad ? `${bad} FAILURES` : 'ALL BROWSER CHECKS PASS'); process.exit(bad ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
