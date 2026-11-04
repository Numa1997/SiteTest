const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const out = [];
 for (const lang of ['', 'de/', 'ar/']) for (const w of [1280, 390]) { const pg = await b.newPage({ viewport: { width: w, height: 900 } }); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('file://' + path.resolve('/home/claude/SiteTest/public/' + lang + 'simulations/double-inverted-pendulum.html')); await pg.waitForTimeout(2500);
  await pg.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true)); await pg.waitForTimeout(500);
  const r = await pg.evaluate(() => ({ kerr: document.querySelectorAll('.katex-error').length, pend: document.querySelectorAll('.i18n-pending').length, sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, rc: document.getElementById('r-c').textContent, walk: document.querySelectorAll('#walk [class*=step]').length, swing: document.getElementById('swing').textContent }));
  // swing-up in this language, 10 s real time
  await pg.evaluate(() => { document.getElementById('stage').scrollIntoView(); document.getElementById('swing').click(); }); await pg.waitForTimeout(9000);
  r.after = await pg.evaluate(() => ({ mode: DIPC.mode, t: +DIPC.t.toFixed(1), state: document.getElementById('state').textContent.slice(0, 60) }));
  if (w === 390) await pg.screenshot({ path: `l-${lang.replace('/', '') || 'en'}-390.png` });
  const sec = await pg.$('#p-calm'); if (sec && w === 1280) { await sec.scrollIntoViewIfNeeded(); await sec.screenshot({ path: `l-${lang.replace('/', '') || 'en'}-calm.png` }); }
  out.push((lang || 'en/') + w + ' ' + JSON.stringify(r) + ' errors:' + (errs.join('|') || 'none')); await pg.close(); }
 console.log(out.join('\n')); await b.close(); })();
