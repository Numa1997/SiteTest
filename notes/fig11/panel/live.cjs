// The live page on phyeinusul.com in English, German and Arabic at 1280 and 390 px: no page errors, the data panel opens,
// Record catches one round, the page is exactly as wide as the window.
'use strict';
const { chromium } = require('playwright');
const BASE = process.env.SITE || 'https://phyeinusul.com';
(async () => { const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined; const b = await chromium.launch(proxy ? { proxy } : {});
  for (const lang of ['', 'de/', 'ar/']) for (const w of [1280, 390]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 }, ignoreHTTPSErrors: !!proxy }), pg = await ctx.newPage(), errs = []; pg.on('pageerror', (e) => errs.push(e.message));
    await pg.goto(BASE + '/' + lang + 'simulations/double-inverted-pendulum.html?live=' + Date.now(), { waitUntil: 'load' }); await pg.waitForTimeout(2500);
    const r = await pg.evaluate(() => ({ tab: !!document.querySelector('.dp-tab'), lang: document.documentElement.lang, dir: document.getElementById('data-panel') && document.getElementById('data-panel').getAttribute('dir') }));
    await pg.evaluate(() => { if (!document.body.classList.contains('dp-open')) document.querySelector('.dp-tab').click(); }); await pg.waitForTimeout(800);
    r.open = await pg.evaluate(() => document.body.classList.contains('dp-open'));
    r.ledgerRows = await pg.evaluate(() => document.querySelectorAll('#data-panel tbody tr').length);
    await pg.evaluate(() => document.querySelector('#data-panel [data-rec]').click());
    r.recording = await pg.evaluate(() => window.__dataPanel.recording());
    r.rounds = await pg.evaluate(() => new Promise((res) => { const t0 = performance.now(); const f = () => { if (window.__dataPanel.rounds().length || performance.now() - t0 > 20000) res(window.__dataPanel.rounds().length); else setTimeout(f, 250); }; f(); }));
    r.sw = await pg.evaluate(() => document.documentElement.scrollWidth); r.cw = await pg.evaluate(() => document.documentElement.clientWidth);
    console.log(`${(lang || 'en/') + w}: ${JSON.stringify(r)} width ${r.sw === r.cw ? 'equal' : 'DIFFERENT'} errors: ${errs.join(' | ') || 'none'}`); await ctx.close(); }
  await b.close(); })();
