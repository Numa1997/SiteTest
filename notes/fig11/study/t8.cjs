const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1280, height: 900 } }); const errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
 await pg.goto('file://' + path.resolve('/home/claude/SiteTest/public/simulations/double-inverted-pendulum.html')); await pg.waitForTimeout(1500);
 await pg.evaluate(() => { const b = document.getElementById('play'); if (b.textContent.trim() === 'Pause') b.click(); });
 const set = (o) => pg.evaluate((o) => { for (const k in o) { const el = document.getElementById(k); el.value = o[k]; el.dispatchEvent(new Event('input', { bubbles: true })); } }, o);
 for (const Ts of [10, 40]) { await set({ Ts }); const r = await pg.evaluate(() => { const t0 = performance.now(); const c = DIPC.finishCatch(); return { K: DIPC.K.map(v => +v.toFixed(3)), c: +c.toFixed(2), ms: Math.round(performance.now() - t0), lam: document.getElementById('r-lam').textContent, set: document.getElementById('r-set').textContent }; }); console.log('Ts', Ts, JSON.stringify(r)); }
 await pg.evaluate(() => { DIPC.gmode = 'cont'; }); await set({ Ts: 40 }); console.log('continuous gains at 40 ms:', JSON.stringify(await pg.evaluate(() => ({ c: DIPC.finishCatch(), lam: document.getElementById('r-lam').textContent, set: document.getElementById('r-set').textContent }))));
 await pg.evaluate(() => { DIPC.gmode = 'sampled'; }); await set({ Ts: 10 }); await pg.evaluate(() => DIPC.finishCatch());
 console.log('errors:', errs.join(' | ') || 'none'); await b.close(); })();
