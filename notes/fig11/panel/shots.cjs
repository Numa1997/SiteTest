// screenshots of the page with the data panel open, and the layout facts: page width, panel box, what the panel covers
const { chromium } = require('playwright'); const path = require('path');
const ROOT = process.env.ROOT || require('path').resolve(__dirname, '../../..'), OUT = process.env.OUT || '.', PAGE = process.env.PAGE || 'simulations/double-inverted-pendulum.html';
(async () => { const b = await chromium.launch();
  for (const w of (process.env.W || '1600,1280,390').split(',').map(Number)) { const pg = await b.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: +(process.env.DPR || 1) }); const errs = []; pg.on('pageerror', (e) => errs.push(e.message));
    await pg.goto('file://' + path.resolve(ROOT + '/public/' + PAGE)); await pg.waitForTimeout(2500);
    await pg.evaluate(() => { if (!document.body.classList.contains('dp-open')) document.querySelector('.dp-tab').click(); }); await pg.waitForTimeout(1500);
    const r = await pg.evaluate(() => { const p = document.getElementById('data-panel').getBoundingClientRect(), play = document.getElementById('play').getBoundingClientRect(), st = document.getElementById('stage').getBoundingClientRect();
      const at = document.elementFromPoint(play.x + play.width / 2, play.y + play.height / 2);
      return { sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, panel: [Math.round(p.x), Math.round(p.width)], stage: [Math.round(st.x), Math.round(st.width)], playCovered: !at || !at.closest('#play'), bodyPad: getComputedStyle(document.body).paddingRight || getComputedStyle(document.body).marginRight }; });
    await pg.screenshot({ path: `${OUT}/panel-${w}.png` }); console.log(w, JSON.stringify(r), 'errors:', errs.join(' | ') || 'none'); await pg.close(); }
  await b.close(); })();
