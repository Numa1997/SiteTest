const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const out = [];
  for (const q of ['', '?gen=2026-11-14']) {
    const p = await b.newPage({ viewport: { width: 1440, height: 1000 } }); const errs = [], bad = [];
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text().slice(0, 200)); });
    p.on('pageerror', e => errs.push('PAGEERROR ' + String(e).slice(0, 300)));
    p.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url().slice(-90)); });
    await p.goto('https://phyeinusul.com/simulations/resonant-tunnelling.html' + q, { waitUntil: 'load', timeout: 90000 });
    const snap = async (tag) => {
      await p.waitForTimeout(3500);
      const o = await p.evaluate(() => ({
        t: document.getElementById('r-t').textContent,
        src: document.getElementById('src-t').textContent.replace(/\s+/g, ' ').slice(0, 520),
        cpx: document.getElementById('cap-px').textContent,
        civ: document.getElementById('cap-iv').textContent.slice(0, 120),
        cte: document.getElementById('cap-te').textContent }));
      out.push(Object.assign({ q, tag }, o));
    };
    await snap('default run');
    const shapes = await p.$$('.chips[data-key="shape"] button');
    for (let i = 0; i < shapes.length; i++) {
      await shapes[i].click(); await snap('shape ' + (await shapes[i].textContent()).trim());
      const n = await p.$eval('#energy', e => +e.max);
      for (const k of [Math.floor(n / 2), n]) {
        await p.$eval('#energy', (e, k) => { e.value = k; e.dispatchEvent(new Event('input', { bubbles: true })); }, k);
        await snap('  energy index ' + k);
      }
    }
    if (q) await p.screenshot({ path: process.argv[2], fullPage: false });
    out.push({ q, errors: errs, bad });
    await p.close();
  }
  console.log(JSON.stringify(out, null, 1)); await b.close();
})();
