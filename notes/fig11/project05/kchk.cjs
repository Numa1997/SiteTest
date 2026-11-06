const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const L of ['', 'de/', 'ar/']) for (const W of [1100, 390]) {
    const pg = await b.newPage({ viewport: { width: W, height: 900 } }); const errs = [];
    pg.on('pageerror', e => errs.push(e.message));
    await pg.goto(`http://localhost:8765/${L}simulations/double-inverted-pendulum.html`, { waitUntil: 'load' });
    await pg.waitForTimeout(2500);
    const r = await pg.evaluate(() => { document.querySelectorAll('details').forEach(d => d.open = true);
      return { kerr: document.querySelectorAll('.katex-error').length, pend: document.querySelectorAll('.i18n-pending').length,
        over: document.documentElement.scrollWidth > document.documentElement.clientWidth,
        row: [...document.querySelectorAll('td,th')].filter(c => /own field|eigenes Feld|حقلك/.test(c.textContent)).length,
        opt: !!document.querySelector('option[value=own]') }; });
    console.log((L || 'en/') + W, JSON.stringify(r), 'errors', errs.length, errs[0] || '');
    await pg.close();
  }
  await b.close();
})();
