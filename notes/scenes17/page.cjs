// Fig. 17 page check: errors, sideways scroll, every scene drawn (alpha before colour), readouts, at 1600 and 390 px; reduced motion.
// node notes/scenes17/page.cjs   (serve dist/ on port 8766 first)
const { chromium } = require('playwright');
const SC = ['spin', 'wind', 'forest', 'roots', 'powder', 'harp', 'mix', 'motes', 'swerve', 'shores', 'seeds', 'chip', 'atlas'];
(async () => { const b = await chromium.launch(); let bad = 0;
  for (const [w, rm] of [[1600, false], [390, false], [1600, true]]) {
    const c = await b.newContext({ viewport: { width: w, height: 1000 }, reducedMotion: rm ? 'reduce' : 'no-preference' }), p = await c.newPage(), errs = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto('http://localhost:8766/simulations/living-scenes.html', { waitUntil: 'networkidle' });
    for (const s of SC) {
      await p.click(`#scene-chips button[data-s="${s}"]`); await p.waitForTimeout(s === 'spin' ? 3500 : 2500);
      const r = await p.evaluate(n => { const h = document.querySelector(`[data-bg="${n}"]`), cv = h && h.querySelector('canvas'); if (!cv || !cv.width) return { drawn: 0, w: 0 };
        const d = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data; let k = 0; for (let i = 3; i < d.length; i += 4) if (d[i] > 20) k++;
        return { drawn: k / (cv.width * cv.height), w: cv.width, h: cv.height, ro: document.getElementById('readouts').innerText.replace(/\n/g, ' '), src: document.getElementById('src-t').textContent.slice(0, 140),
          side: document.documentElement.scrollWidth - document.documentElement.clientWidth }; }, s);
      const ok = r.drawn > 0.002 && r.side <= 0; if (!ok) bad++;
      console.log((ok ? 'ok ' : 'BAD') + ` ${w}${rm ? ' reduced' : ''} ${s}: canvas ${r.w}x${r.h} drawn ${(100 * r.drawn).toFixed(1)}% | ${r.ro || ''} | ${r.src}`);
      if (w === 1600 && !rm && ['spin', 'wind', 'forest', 'atlas'].includes(s)) await p.locator('.sim__grid').screenshot({ path: `notes/scenes17/shots/${s}-1600.png` });
      if (w === 390 && s === 'spin') await p.screenshot({ path: 'notes/scenes17/shots/spin-390.png', fullPage: false });
    }
    if (w === 1600 && !rm) { await p.click('#scene-chips button[data-s="spin"]'); await p.click('button[data-v="20"]'); await p.waitForTimeout(3000);
      console.log('K0=20:', await p.evaluate(() => document.getElementById('readouts').innerText.replace(/\n/g, ' '))); await p.evaluate(() => document.getElementById('paper').scrollIntoView()); await p.waitForTimeout(2500);
      await p.screenshot({ path: 'notes/scenes17/shots/note-1600.png' }); await p.locator('#p-spin figure').nth(1).screenshot({ path: 'notes/scenes17/shots/fig2.png' }); }
    console.log(`${w}${rm ? ' reduced' : ''}: errors ${errs.length} ${errs.slice(0, 3).join(' | ')}`); if (errs.length) bad++;
    await c.close(); }
  console.log(bad ? bad + ' problems' : 'all clean'); await b.close(); })();
