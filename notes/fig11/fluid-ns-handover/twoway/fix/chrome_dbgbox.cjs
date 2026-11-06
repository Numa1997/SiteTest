const { chromium } = require('playwright'); const path = require('path');
(async () => { const br = await chromium.launch(); const pg = await br.newPage({ viewport: { width: 1100, height: 900 } });
  await pg.goto('file://' + path.resolve(__dirname, '../../../../../public/simulations/double-inverted-pendulum.html')); await pg.waitForTimeout(1500);
  await pg.evaluate(() => { const M = document.getElementById('med'); M.value = 'water'; M.dispatchEvent(new Event('change')); const F = document.getElementById('flow'); F.value = 'own'; F.dispatchEvent(new Event('change')); });
  await pg.waitForTimeout(500);
  console.log(await pg.evaluate(() => ['flow-note', 'own'].map(id => { const e = document.getElementById(id), cs = getComputedStyle(e), r = e.getBoundingClientRect(); let p = e.parentElement, chain = []; while (p && chain.length < 4) { const c = getComputedStyle(p); chain.push(p.className + ':' + c.display + '/' + c.overflow + '/h' + Math.round(p.getBoundingClientRect().height)); p = p.parentElement; } return id + ' disp=' + cs.display + ' vis=' + cs.visibility + ' rect=' + [r.x, r.y, r.width, r.height].map(Math.round) + ' text=' + e.textContent.slice(0, 60) + ' || ' + chain.join(' < '); }).join('\n')));
  await br.close(); })();
