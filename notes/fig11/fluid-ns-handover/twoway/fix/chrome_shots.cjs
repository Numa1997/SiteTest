// en/de/ar at 1100 and 390 px, water solved: errors, KaTeX errors, pending, overflow; screenshots of section 13.6's changed part.
const { chromium } = require('playwright'); const path = require('path'); const OUT = process.env.OUT;
(async () => {
  const br = await chromium.launch();
  for (const lang of ['', 'de/', 'ar/']) for (const W of [1100, 390]) {
    const pg = await br.newPage({ viewport: { width: W, height: 900 }, deviceScaleFactor: 1 }); const errs = []; pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('file://' + path.resolve(__dirname, '../../../../../public/' + lang + 'simulations/double-inverted-pendulum.html')); await pg.waitForTimeout(2000);
    await pg.evaluate(() => { const M = document.getElementById('med'); M.value = 'water'; M.dispatchEvent(new Event('change')); const C = document.getElementById('cpl'); C.disabled = false; C.value = 'solved'; C.dispatchEvent(new Event('change')); });
    await pg.waitForTimeout(2500);
    // open every fold so the note is laid out, then measure
    await pg.evaluate(() => { document.querySelectorAll('details').forEach(d => d.open = true); document.querySelectorAll('[aria-expanded="false"]').forEach(b => { try { b.click(); } catch (e) {} }); });
    await pg.waitForTimeout(1500);
    const r = await pg.evaluate(() => ({ katex: document.querySelectorAll('.katex-error').length, pending: document.querySelectorAll('.i18n-pending').length, overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth }));
    const h = await pg.evaluateHandle(() => [...document.querySelectorAll('h4')].find(e => /13\.6/.test(e.textContent)));
    let shot = 'none'; try { const t = await pg.evaluateHandle(() => { return [...document.querySelectorAll('table')].find(t => /2D-1|شيفر/.test(t.textContent) && t.closest('article')) || null; });
      await pg.evaluate(() => { document.querySelectorAll('aside, [class*="dp-panel"], [class*="datapanel"], [id^="dp"]').forEach(e => { if (!e.closest('article')) e.style.display = 'none'; }); }); const tab = t.asElement(); if (tab) { await tab.scrollIntoViewIfNeeded(); await pg.waitForTimeout(300); shot = `${OUT}/s136_${lang.replace('/', '') || 'en'}_${W}.png`; await tab.screenshot({ path: shot }); } } catch (e) { shot = 'fail ' + e.message.slice(0, 60); }
    console.log(lang || 'en/', W, JSON.stringify(r), 'errors', errs.length, errs.slice(0, 2), shot); await pg.close(); }
  await br.close(); })();
