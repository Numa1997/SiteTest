// Browser check of the built page, at 360, 390, 1024 and 1440 px, in Chromium (the preinstalled Playwright).
//   node portfolios-src/electron-beam/checks/check_page.cjs                       serves public/ and opens /portfolios/electron-beam/index.html
//   node ... --file PATH_TO_BUILT_HTML [--shots DIR]                              any built page; its ../../ links are served from public/ too
// Fails on: a KaTeX error, a page error or console error, sideways scroll, a request to anywhere but the page's own origin
// (data: and blob: aside), a response with status 400 or more, a title not in Instrument Serif at weight 400, a simulation canvas
// with nothing drawn (alpha read before colour), a simulation whose readouts do not change when its first slider moves.
// Screenshots (device scale 2) go to notes/electron-beam/shots/ unless --shots says otherwise (that folder is git-ignored).
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..', '..', '..');
const arg = n => (process.argv.includes(n) ? process.argv[process.argv.indexOf(n) + 1] : null);
const shots = path.resolve(arg('--shots') || path.join(ROOT, 'notes', 'electron-beam', 'shots'));
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.json': 'application/json', '.png': 'image/png', '.webp': 'image/webp' };

function serve(extraFile) {
  const pub = path.join(ROOT, 'public');
  return new Promise(res => {
    const s = http.createServer((q, r) => {
      let u = decodeURIComponent(q.url.split('?')[0]);
      let f = u === '/__page__.html' && extraFile ? extraFile : path.join(pub, u);
      if (!f.startsWith(pub) && f !== extraFile) { r.writeHead(403); return r.end(); }
      if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
      if (!fs.existsSync(f)) { r.writeHead(404); return r.end('not found'); }
      r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' });
      fs.createReadStream(f).pipe(r);
    }).listen(0, '127.0.0.1', () => res(s));
  });
}

(async () => {
  const file = arg('--file') ? path.resolve(arg('--file')) : null;
  const srv = await serve(file);
  const origin = 'http://127.0.0.1:' + srv.address().port;
  // a stand-alone build (out/index.html) links ../../../public/..; served at /__page__.html those links would leave the root, so rewrite them
  let url = origin + (arg('--path') || '/portfolios/electron-beam/index.html');
  if (file) url = origin + '/__page__.html';
  fs.mkdirSync(shots, { recursive: true });
  const browser = await chromium.launch();
  let ok = true;
  for (const w of [360, 390, 1024, 1440]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 2 });
    const pg = await ctx.newPage();
    const errs = [], outside = [], bad = [];
    pg.on('pageerror', e => errs.push('pageerror: ' + e.message));
    pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    pg.on('request', r => { const u = r.url(); if (!u.startsWith(origin) && !u.startsWith('data:') && !u.startsWith('blob:')) outside.push(u); });
    pg.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });
    await pg.goto(url, { waitUntil: 'networkidle' });
    await pg.evaluate(() => document.fonts.ready);
    const res = { w };
    res.katex_errors = await pg.locator('.katex-error').count();
    res.katex_ok = await pg.locator('.katex').count();
    res.overflow = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    res.wide_elements = await pg.evaluate(() => { const W = document.documentElement.clientWidth; return Array.from(document.querySelectorAll('main *')).filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > W + 1 && !e.closest('.katex-display') && !e.closest('svg') && !e.closest('.ptab') && !e.closest('.pfig__plate'); }).slice(0, 3).map(e => e.tagName + '.' + e.className); });
    res.h1_font = await pg.evaluate(() => { const c = getComputedStyle(document.querySelector('h1')); return c.fontFamily.split(',')[0].replace(/["']/g, '') + ' ' + c.fontWeight; });
    res.fonts = await pg.evaluate(() => ['Instrument Serif', 'IBM Plex Sans', 'IBM Plex Mono', 'Latin Modern Roman'].filter(f => document.fonts.check('16px "' + f + '"')));
    res.chapters = await pg.locator('.chapter').count();
    res.todo = await pg.locator('.chapter--todo').count();
    res.back_link = await pg.locator('a.back').getAttribute('href');
    // each running simulation: something drawn (alpha first), and the readouts move with the first slider
    const sims = await pg.locator('.eb-sim[data-module]').count();
    res.sims = [];
    for (let i = 0; i < sims; i++) {
      const el = pg.locator('.eb-sim[data-module]').nth(i);
      await el.scrollIntoViewIfNeeded();
      await pg.waitForTimeout(150);
      const drawn = await el.locator('canvas').evaluate(c => { const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0; for (let k = 3; k < d.length; k += 4) if (d[k] > 0) n++; return n; });
      const before = await el.locator('[data-out]').allInnerTexts();
      const slider = el.locator('input[type=range][data-symbol]').first();
      let moved = null;
      if (await slider.count()) {
        const v = await slider.inputValue();
        await slider.evaluate((s, nv) => { s.value = nv; s.dispatchEvent(new Event('input', { bubbles: true })); }, String(v < 500 ? 900 : 100));
        await pg.waitForTimeout(150);
        moved = JSON.stringify(before) !== JSON.stringify(await el.locator('[data-out]').allInnerTexts());
      }
      const err = await el.locator('.eb-sim__err').isVisible();
      res.sims.push({ module: await el.getAttribute('data-module'), drawn_pixels: drawn, readouts_move: moved, error_shown: err });
    }
    res.errors = errs; res.outside = outside; res.bad_responses = bad;
    await pg.evaluate(() => window.scrollTo(0, 0));
    await pg.screenshot({ path: path.join(shots, `top-${w}.png`) });
    await pg.screenshot({ path: path.join(shots, `page-${w}.png`), fullPage: true });
    const fail = res.katex_errors || errs.length || outside.length || bad.length || res.overflow > 0 || res.wide_elements.length ||
      !/^Instrument Serif 400$/.test(res.h1_font) || res.fonts.length < 4 ||
      res.sims.some(s => s.drawn_pixels === 0 || s.readouts_move === false || s.error_shown);
    ok = ok && !fail;
    console.log((fail ? 'FAIL ' : 'PASS ') + JSON.stringify(res));
    await ctx.close();
  }
  await browser.close(); srv.close();
  console.log('PAGE CHECK ' + (ok ? 'PASS' : 'FAIL') + '  screenshots in ' + path.relative(ROOT, shots));
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
