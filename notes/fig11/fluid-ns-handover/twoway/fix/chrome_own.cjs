// Your own field: choose it, type formulas, check the arrows, the divergence verdict, an error, and screenshots.
const { chromium } = require('playwright'); const path = require('path'); const OUT = process.env.OUT;
(async () => {
  const br = await chromium.launch(); const lang = process.env.LANG2 || '', W = +(process.env.W || 1100);
  const pg = await br.newPage({ viewport: { width: W, height: 900 }, deviceScaleFactor: 1 }); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('file://' + path.resolve(__dirname, '../../../../../public/' + lang + 'simulations/double-inverted-pendulum.html')); await pg.waitForTimeout(2000);
  const pick = (m, f) => pg.evaluate((a) => { const M = document.getElementById('med'); M.value = a.m; M.dispatchEvent(new Event('change')); const F = document.getElementById('flow'); F.value = a.f; F.dispatchEvent(new Event('change')); }, { m, f });
  const type = (id, v) => pg.fill('#' + id, v);
  const state = () => pg.evaluate(() => ({ shown: !document.getElementById('own').hidden, msg: document.getElementById('own-msg').textContent, bad: document.getElementById('own-msg').className, div: DIPC.ds.get('own_div'), grad: DIPC.ds.get('own_grad'), u: DIPC.ds.get('own_u'), fg: Array.from(DIPC.ds.get('fg_u')).slice(200, 203).map(v => +v.toFixed(4)), x: DIPC.s[0], th1: DIPC.s[1] }));
  await pick('water', 'own'); await pg.waitForTimeout(1500); console.log('default swirl', JSON.stringify(await state()));
  if (OUT) { await pg.evaluate(() => window.scrollTo(0, 0)); await pg.waitForTimeout(300); await pg.screenshot({ path: `${OUT}/own_${lang.replace('/', '') || 'en'}_${W}.png` }); await pg.evaluate(() => document.getElementById('own').scrollIntoView({ block: 'center' })); await pg.waitForTimeout(300); await pg.screenshot({ path: `${OUT}/ownbox_${lang.replace('/', '') || 'en'}_${W}.png` }); }
  await type('own-u', 'U*x'); await type('own-v', 'U*y'); await pg.waitForTimeout(1200); console.log('source (div 2U)', JSON.stringify(await state()));
  await type('own-u', 'U*sin(x'); await pg.waitForTimeout(400); console.log('typo', JSON.stringify(await state()));
  await type('own-u', 'U*(1 + 0.5*sin(2*pi*t/3))'); await type('own-v', '0'); await pg.waitForTimeout(1200); console.log('gust', JSON.stringify(await state()));
  await pick('water', 'breeze'); await pg.waitForTimeout(500); console.log('breeze', JSON.stringify(await state()));
  if (OUT) { await pick('water', 'eddy'); await pg.waitForTimeout(3000); await pg.evaluate(() => window.scrollTo(0, 0)); await pg.waitForTimeout(300); await pg.screenshot({ path: `${OUT}/eddy_${lang.replace('/', '') || 'en'}_${W}.png` }); }
  console.log('page errors', errs.length, errs.slice(0, 3)); await br.close(); })();
