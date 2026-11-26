// Film the home page scenes: frames of the top of the page over 60 s, the margins after scrolling 900 px, and counts read from
// the scenes themselves (trees standing, trees grown, cloud droplets). node notes/home/scenes/film.cjs <tag>   (serves dist/ on :8766)
// Writes notes/home/scenes/<tag>/<width>-t<s>.png, <width>-scroll-<k>.png and <tag>/counts.json.
const { chromium } = require('playwright'), fs = require('fs');
const tag = process.argv[2] || 'now', URL = (process.env.BASE || 'http://localhost:8766/') + 'index.html', DIR = `notes/home/scenes/${tag}`;
const TIMES = (process.env.TIMES || '2,10,20,30,40,50,60').split(',').map(Number), WIDTHS = (process.env.WIDTHS || '1920,1600,1100').split(',').map(Number);
fs.mkdirSync(DIR, { recursive: true });
(async () => {
  const b = await chromium.launch(), out = {};
  for (const w of WIDTHS) {
    const h = 1080, p = await b.newPage({ viewport: { width: w, height: h } }), errs = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto(URL, { waitUntil: 'networkidle' }); if (process.env.YEAR) await p.evaluate(y => { const s = document.querySelector('[data-bg=forest]').__bgScene; s.YEAR = +y; }, process.env.YEAR);   // YEAR=40 films a year in 40 s (to see every season's sky)
    const t0 = Date.now(); const rows = [];
    for (const t of TIMES) {
      await p.waitForTimeout(Math.max(0, t * 1000 - (Date.now() - t0)));
      const c = await p.evaluate(() => { const f = document.querySelector('[data-bg=forest]'), s = f && f.__bgScene; if (!s || !s.A) return null;
        return { trees: s.A.length, grown: s.A.filter(q => q.mat).length, year: +(s.Y / s.YEAR).toFixed(2), vapour: s.V.length, clouds: (s.Cs || []).length, water: +(s.Cs || []).reduce((a, c) => a + c.m, 0).toFixed(1), sky: Object.keys(s.am || {}).filter(k => s.am[k] > .3).join(' '), cb: !!s.cb }; });
      rows.push(Object.assign({ t }, c)); await p.screenshot({ path: `${DIR}/${w}-t${t}.png` });
    }
    await p.evaluate(() => scrollTo(0, 900)); await p.waitForTimeout(2500);
    for (let k = 0; k < 6; k++) { await p.screenshot({ path: `${DIR}/${w}-scroll-${k}.png` }); await p.waitForTimeout(500); }
    const side = await p.evaluate(() => { const r = document.querySelector('[data-bg=rails]'), s = r && r.__bgScene; return s ? { ok: s.ok, bars: (s.Bs || []).length, err: s.err || null, data: !!s.D } : null; });
    out[w] = { forest: rows, rails: side, errors: errs, sideways: await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth) };
    console.log(w, JSON.stringify(out[w]));
    await p.close();
  }
  fs.writeFileSync(`${DIR}/counts.json`, JSON.stringify(out, null, 1)); await b.close();
})();
