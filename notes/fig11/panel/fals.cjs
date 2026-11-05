// f. Falsification: corrupt one thing, show that the tests of hon.cjs fail, revert, show that they pass again.
'use strict';
const fs = require('fs'), path = require('path'); const { chromium } = require('playwright');
const { EXTRACT, PICTURE, checkLogs, checkPicture } = require('./hon.cjs');
const ROOT = process.env.ROOT || require('path').resolve(__dirname, '../../..'), SIM = ROOT + '/public/simulations/';
async function grab(pg) { const r = await pg.evaluate(EXTRACT, { lastI: -1, lastJ: -1, plSerial: 0 }); const acc = { st: r.st, cs: r.cs, ctx: { [r.ctx.ver]: r.ctx }, plans: {}, b1: r.b1, sig: r.sig }; if (r.plan) acc.plans[r.plan.serial] = r.plan; return acc; }
const show = (tag, c) => { console.log(`${tag}: ${c.ok ? 'ALL PASS' : 'FAILS'}`); c.lines.filter((l) => /PASS|FAIL/.test(l)).forEach((l) => console.log('  ' + l.trim())); };
(async () => { const b = await chromium.launch(); let pg = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await pg.goto('file://' + SIM + 'double-inverted-pendulum.html'); await pg.waitForTimeout(1200); await pg.evaluate(() => DIPC.finishCatch());
  await pg.click('#reset'); await pg.waitForTimeout(3500); await pg.click('#play'); await pg.waitForTimeout(300);   // 3.5 s of balancing, then paused
  show('f0 clean store', checkLogs(await grab(pg)));
  // f1: one stored force 1e-9 N off
  const f1 = await pg.evaluate(() => { const a = DIPC.ds.get('cs_u'), r = Math.floor(DIPC.ds.get('cs_n') / 2), old = a[r]; a[r] = old + 1e-9; return { r, old, j: DIPC.ds.get('cs_i')[r] }; });
  console.log(`f1 corrupt: sample j = ${f1.j}, stored force ${f1.old} N raised by 1e-9 N`); show('f1 corrupted', checkLogs(await grab(pg)));
  await pg.evaluate((f) => { DIPC.ds.get('cs_u')[f.r] = f.old; }, f1); show('f1 reverted', checkLogs(await grab(pg)));
  // f2: one stored state 1e-12 rad off
  const f2 = await pg.evaluate(() => { const a = DIPC.ds.get('st_s1'), r = Math.floor(DIPC.ds.get('st_n') / 2), old = a[6 * r + 1]; a[6 * r + 1] = old + 1e-12; return { r, old, k: DIPC.ds.get('st_i')[r] }; });
  console.log(`f2 corrupt: step k = ${f2.k}, stored θ₁ after the step ${f2.old} rad raised by 1e-12 rad`); show('f2 corrupted', checkLogs(await grab(pg)));
  await pg.evaluate((f) => { DIPC.ds.get('st_s1')[6 * f.r + 1] = f.old; }, f2); show('f2 reverted', checkLogs(await grab(pg)));
  // f3: a display that computes its own state instead of reading the store: a copy of the page whose draw() takes the page's s with x 1 cm off
  const src = fs.readFileSync(SIM + 'double-inverted-pendulum.html', 'utf8'), A = "S = g2('s_now'),", B = "S = s.map(function (v, i) { return i === 0 ? v + 0.01 : v; }),";
  if (src.split(A).length !== 2) throw new Error('draw() line not found'); const tmp = SIM + '_falsify-f3.html'; fs.writeFileSync(tmp, src.replace(A, B));
  for (const [tag, file] of [['f3 display recomputes (x + 1 cm)', '_falsify-f3.html'], ['f3 reverted (the real page)', 'double-inverted-pendulum.html']]) {
    await pg.close(); pg = await b.newPage({ viewport: { width: 1280, height: 900 } }); await pg.goto('file://' + SIM + file); await pg.waitForTimeout(1200); await pg.evaluate(() => DIPC.finishCatch());
    await pg.click('#reset'); await pg.waitForTimeout(2500); await pg.click('#play'); await pg.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
    const c = checkPicture(await pg.evaluate(PICTURE), tag); console.log(`${tag}: ${c.ok ? 'ALL PASS' : 'FAILS'}`); c.lines.forEach((l) => console.log('  ' + l.trim())); }
  fs.unlinkSync(tmp); console.log(`removed ${path.basename(tmp)}: ${!fs.existsSync(tmp)}`); await b.close(); })();
