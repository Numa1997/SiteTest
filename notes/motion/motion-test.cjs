// Motion test: every fold, menu and tab on each page type, at four widths, en/de/ar. Usage: node motion-test.cjs <base> <outdir>
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = process.argv[2] || 'http://localhost:8765/';
const OUT = process.argv[3] || '.';
const WIDTHS = [[390, 844], [844, 390], [1100, 800], [1440, 900]];
const PAGES = [
  ['home', 'index.html'], ['sims', 'simulations.html'], ['projects', 'portfolios.html'],
  ['sim', 'simulations/pendulum-control.html'], ['lucretius', 'lucretius.html'],
];
const LANGS = ['', 'de/', 'ar/'];
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function testPage(browser, lang, key, path, w, h, shots) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(BASE + lang + path, { waitUntil: 'load' });
  await sleep(1500);
  const r = { page: lang + path, w, h, errors, folds: 0, opened: 0, closed: 0, issues: [] };
  const overflow = async (when) => {
    const o = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    if (o > 1) r.issues.push(`horizontal overflow ${o}px ${when}`);
  };
  await overflow('at load');
  const n = await page.evaluate(() => document.querySelectorAll('[data-fold-level="1"]').length);
  r.folds = n;
  for (let i = 0; i < n; i++) {
    // open: sample height and first item opacity every frame for 1.1 s
    const s = await page.evaluate(async (i) => {
      const node = document.querySelectorAll('[data-fold-level="1"]')[i];
      node.scrollIntoView({ block: 'start', behavior: 'instant' });
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      const fold = node.querySelector(':scope > .fold'), body = fold.querySelector('.fs-body');
      const first = body.firstElementChild;
      const btn = node.querySelector(':scope > .fs-head .fs-toggle');
      const t0 = performance.now(), hs = [], ops = [], tops = [];
      const head = node.querySelector(':scope > .fs-head');
      btn.click();
      const risingAt0 = fold.classList.contains('is-rising');
      while (performance.now() - t0 < 1100) {
        await new Promise(r => requestAnimationFrame(r));
        hs.push(fold.getBoundingClientRect().height);
        ops.push(first ? +getComputedStyle(first).opacity : 1);
        tops.push(head.getBoundingClientRect().top + window.scrollY);
      }
      return { open: node.getAttribute('data-collapsed') === '0', hs, ops, risingAt0, label: (head.textContent || '').trim().slice(0, 40) };
    }, i);
    if (s.open) r.opened++;
    else r.issues.push(`fold ${i} did not open`);
    // no jump: height never drops while opening, and no single frame takes more than 45 % of the full height when it is tall
    const full = Math.max(...s.hs);
    for (let k = 1; k < s.hs.length; k++) {
      if (s.hs[k] < s.hs[k - 1] - 1) { r.issues.push(`fold ${i} height fell while opening`); break; }
    }
    const steps = s.hs.slice(1).map((v, k) => v - s.hs[k]);
    if (full > 200 && Math.max(...steps) > 0.45 * full) r.issues.push(`fold ${i} (${s.label}) opened in a jump: ${Math.max(...steps).toFixed(0)} of ${full.toFixed(0)} px in one frame`);
    for (let k = 1; k < s.ops.length; k++) if (s.ops[k] < s.ops[k - 1] - 0.02) { r.issues.push(`fold ${i} first item flashed (opacity fell)`); break; }
    if (!s.risingAt0) r.issues.push(`fold ${i}: items did not rise`);
    r.frames = (r.frames || 0) + s.hs.length;
    await overflow(`with fold ${i} open`);
    // close
    const c = await page.evaluate(async (i) => {
      const node = document.querySelectorAll('[data-fold-level="1"]')[i];
      const fold = node.querySelector(':scope > .fold');
      node.querySelector(':scope > .fs-head .fs-toggle').click();
      const t0 = performance.now(), hs = [];
      while (performance.now() - t0 < 950) { await new Promise(r => requestAnimationFrame(r)); hs.push(fold.getBoundingClientRect().height); }
      return { closed: node.getAttribute('data-collapsed') === '1', hs, rising: fold.classList.contains('is-rising') };
    }, i);
    if (c.closed && c.hs[c.hs.length - 1] < 1) r.closed++;
    else r.issues.push(`fold ${i} did not close fully (${c.hs[c.hs.length - 1]})`);
    for (let k = 1; k < c.hs.length; k++) if (c.hs[k] > c.hs[k - 1] + 1) { r.issues.push(`fold ${i} height rose while closing`); break; }
  }
  // halfway screenshot of one opening (first page language, one fold)
  if (shots && n) {
    await page.evaluate(() => { const node = document.querySelectorAll('[data-fold-level="1"]')[0]; node.scrollIntoView({ block: 'start', behavior: 'instant' }); window.scrollBy(0, -20); });
    await sleep(200);
    await page.evaluate(() => document.querySelectorAll('[data-fold-level="1"]')[0].querySelector('.fs-toggle').click());
    await sleep(375);
    await page.screenshot({ path: `${OUT}/half-${(lang || 'en/').replace('/', '')}-${key}-${w}.png` });
    await sleep(1000);
    await page.screenshot({ path: `${OUT}/open-${(lang || 'en/').replace('/', '')}-${key}-${w}.png` });
    await page.evaluate(() => document.querySelectorAll('[data-fold-level="1"]')[0].querySelector('.fs-toggle').click());
    await sleep(900);
  }
  // Expand all / Collapse all
  const all = await page.evaluate(async () => {
    const b = document.querySelectorAll('.fold-tool'); if (b.length < 2) return null;
    b[0].click(); await new Promise(r => setTimeout(r, 1400));
    const opened = [...document.querySelectorAll('[data-fold-level]')].every(n => n.getAttribute('data-collapsed') === '0');
    b[1].click(); await new Promise(r => setTimeout(r, 1400));
    const closed = [...document.querySelectorAll('[data-fold-level]')].every(n => n.getAttribute('data-collapsed') === '1');
    return { opened, closed };
  });
  if (all) { if (!all.opened || !all.closed) r.issues.push(`expand/collapse all: ${JSON.stringify(all)}`); r.all = all; }
  // simulations list: More / Less on a card
  const card = await page.evaluate(async () => {
    const m = document.querySelector('[data-card] .fs-more'); if (!m) return null;
    const node = m.closest('[data-fold-level]'); if (node && node.getAttribute('data-collapsed') !== '0') node.querySelector('.fs-toggle').click();
    await new Promise(r => setTimeout(r, 900));
    const c = m.closest('[data-card]'); m.click(); const rising = c.querySelector('.fold').classList.contains('is-rising');
    await new Promise(r => setTimeout(r, 1200)); const open = c.getAttribute('data-collapsed') === '0';
    m.click(); await new Promise(r => setTimeout(r, 900)); return { rising, open, closed: c.getAttribute('data-collapsed') === '1' };
  });
  if (card) { r.card = card; if (!card.open || !card.closed) r.issues.push('card More/Less ' + JSON.stringify(card)); }
  // simulation page: walkthrough tabs, data panel and its table sections
  if (key === 'sim') {
    const sim = await page.evaluate(async () => {
      const out = {};
      const steps = document.querySelectorAll('.walk__steps button');
      if (steps.length > 1) {
        const w = document.querySelector('.walk'); if (w && w.getAttribute('data-collapsed') !== '0') w.querySelector('.fs-toggle').click();
        await new Promise(r => setTimeout(r, 900));
        steps[1].click(); await new Promise(r => setTimeout(r, 60));
        const c = document.querySelector('.walk__card'); out.walkAnim = c ? getComputedStyle(c).animationName + ' ' + getComputedStyle(c).animationDuration : 'none';
        await new Promise(r => setTimeout(r, 900));
        out.walkSelected = steps[1].getAttribute('aria-selected');
      }
      const tab = document.querySelector('.dp-tab');
      if (tab) {
        tab.click(); await new Promise(r => setTimeout(r, 300));
        const dp = document.querySelector('.dp'); out.panelHalf = getComputedStyle(dp).transform;
        await new Promise(r => setTimeout(r, 700)); out.panelOpen = getComputedStyle(dp).transform;
        const f = document.querySelector('[data-fold]');
        if (f) {
          const sec = f.closest('.dp-sec'); const wasFolded = sec.classList.contains('is-folded');
          f.click(); await new Promise(r => setTimeout(r, 100)); out.secMid = sec.className;
          await new Promise(r => setTimeout(r, 1500)); out.secAfter1 = sec.className;
          f.click(); await new Promise(r => setTimeout(r, 100)); out.secMid2 = sec.className;
          await new Promise(r => setTimeout(r, 1500)); out.secAfter2 = sec.className; out.wasFolded = wasFolded;
        }
        const close = document.querySelector('.dp [data-close], .dp__close, .dp button[aria-label*="lose"]');
        out.closeBtn = !!close;
      }
      return out;
    });
    r.sim = sim;
  }
  // an in-page jump glides (not instant)
  const jump = await page.evaluate(async () => {
    const as = [...document.querySelectorAll('a[href^="#"]')].filter(a => { const t = a.getAttribute('href').slice(1); const el = t && document.getElementById(decodeURIComponent(t)); return el && a.offsetParent && Math.abs(el.getBoundingClientRect().top) > 600; });
    if (!as.length) return null;
    window.scrollTo({ top: 0, behavior: 'instant' }); await new Promise(r => setTimeout(r, 100));
    const a = as[0]; const y0 = window.scrollY; a.click();
    const ys = []; const t0 = performance.now();
    while (performance.now() - t0 < 1000) { await new Promise(r => requestAnimationFrame(r)); ys.push(window.scrollY); }
    return { href: a.getAttribute('href'), y0, first: ys[0], mid: ys[Math.floor(ys.length / 4)], end: ys[ys.length - 1], frames: ys.length };
  });
  if (jump) { r.jump = jump; if (jump.end === jump.y0) r.issues.push('jump did not move'); else if (jump.first === jump.end) r.issues.push('jump was instant'); }
  await overflow('at end');
  await ctx.close();
  return r;
}

async function reduced(browser) {
  const ctx = await browser.newContext({ viewport: { width: 1100, height: 800 }, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto(BASE + 'simulations.html'); await sleep(1200);
  const r = await page.evaluate(async () => {
    const node = document.querySelector('[data-fold-level="1"]'), fold = node.querySelector('.fold');
    node.querySelector('.fs-toggle').click();
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    const hFrame2 = fold.getBoundingClientRect().height, full = fold.firstElementChild.scrollHeight;
    const btn = document.querySelector('.fold-tool');
    return { td: getComputedStyle(fold).transitionDuration, hFrame2, full, hover: getComputedStyle(btn).transitionDuration, rising: fold.classList.contains('is-rising') };
  });
  await ctx.close();
  return r;
}

(async () => {
  const browser = await chromium.launch();
  const results = [];
  const jobs = [];
  for (const lang of LANGS) for (const [key, path] of PAGES) for (const [w, h] of WIDTHS) jobs.push([lang, key, path, w, h]);
  const shotKeys = new Set();
  let idx = 0;
  async function worker() {
    while (idx < jobs.length) {
      const [lang, key, path, w, h] = jobs[idx++];
      const shots = lang === '' || (w === 390 && key === 'sims');
      try { results.push(await testPage(browser, lang, key, path, w, h, shots)); }
      catch (e) { results.push({ page: lang + path, w, h, issues: ['TEST FAILED ' + e.message.split('\n')[0]] }); }
      process.stdout.write('.');
    }
  }
  await Promise.all([worker(), worker(), worker(), worker()]);
  const red = await reduced(browser);
  await browser.close();
  fs.writeFileSync(`${OUT}/results.json`, JSON.stringify({ results, reduced: red }, null, 1));
  console.log('\nreduced motion:', JSON.stringify(red));
  for (const r of results.sort((a, b) => (a.page + a.w).localeCompare(b.page + b.w))) {
    console.log(`${r.page} ${r.w}x${r.h}: folds ${r.folds} opened ${r.opened} closed ${r.closed} errors ${r.errors ? r.errors.length : '?'} issues ${r.issues.length}${r.issues.length ? ' :: ' + r.issues.slice(0, 4).join(' | ') : ''}`);
    if (r.errors && r.errors.length) console.log('   errors:', r.errors.slice(0, 3).join(' || ').slice(0, 300));
  }
})();
