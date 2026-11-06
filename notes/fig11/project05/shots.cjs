// Screenshots for the report: the strong short machine swung up in water and carried to +1 m (1100 and 390 px), the default machine
// pumping in water, and the en/de/ar pages rendering section 13.7 without sideways scroll or KaTeX errors. OUT=<dir>
const { chromium } = require('playwright'); const OUT = process.env.OUT || '.';
const setup = async (pg, mach, med) => pg.evaluate(([mach, m]) => { const [m0, m1, m2, L1, L2, F] = mach.split('/').map(Number), set = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('input', { bubbles: true })); };
  set('m0', m0); set('m1', m1); set('m2', m2); set('L1', L1); set('L2', L2); set('Fmax', F); const e = document.getElementById('med'); e.value = m; e.dispatchEvent(new Event('change', { bubbles: true })); }, [mach, med]);
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const W of [1100, 390]) {
    const pg = await b.newPage({ viewport: { width: W, height: W > 500 ? 900 : 844 }, deviceScaleFactor: 2 }); pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1200);
    await setup(pg, '1.5/2/2/0.2/0.25/200', 'water'); await pg.waitForTimeout(2500); await pg.click('#swing');
    for (let i = 0; i < 40; i++) { await pg.waitForTimeout(1000); if (i === 22) await pg.click('button[data-go="1"]'); }
    const st = await pg.evaluate(() => ({ t: DIPC.t, x: DIPC.s[0], th1: DIPC.ds.get('th1w') * 57.3, th2: DIPC.ds.get('th2w') * 57.3, mode: DIPC.mode, log: DIPC.log.map(l => l.ev + '@' + l.t.toFixed(1)).join(' '), sw: document.documentElement.scrollWidth }));
    console.log(W, JSON.stringify(st));
    await pg.evaluate(() => document.querySelector('canvas').scrollIntoView({ block: 'center' }));
    await pg.screenshot({ path: OUT + '/water-strong-' + W + '.png' }); await pg.close(); }
  { const pg = await b.newPage({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 2 }); pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1200);
    await setup(pg, '1.5/0.5/0.75/0.5/0.75/60', 'water'); await pg.waitForTimeout(1500); await pg.click('#swing'); await pg.waitForTimeout(16000);
    console.log('default pump', JSON.stringify(await pg.evaluate(() => ({ mode: DIPC.mode, th1: DIPC.ds.get('th1w') * 57.3, th2: DIPC.ds.get('th2w') * 57.3, log: DIPC.log.map(l => l.ev).join(' ') }))));
    await pg.evaluate(() => document.querySelector('canvas').scrollIntoView({ block: 'center' }));
    await pg.screenshot({ path: OUT + '/water-default-pump-1100.png' }); await pg.close(); }
  for (const L of ['en', 'de', 'ar']) for (const W of [1100, 390]) {
    const pg = await b.newPage({ viewport: { width: W, height: 900 } }); pg.on('pageerror', e => errs.push(L + ': ' + e.message));
    await pg.goto('http://localhost:8765/' + (L === 'en' ? '' : L + '/') + 'simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(2000);
    const info = await pg.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, h: [...document.querySelectorAll('h4')].filter(h => h.textContent.includes('13.7')).map(h => h.textContent.trim()).join('|'), katexErr: document.querySelectorAll('.katex-error').length, tags: (document.body.innerHTML.match(/\(4[78]\)/g) || []).length }));
    console.log(L, W, JSON.stringify(info)); await pg.close(); }
  console.log('page errors:', errs.length ? errs : 'none'); await b.close();
})();
