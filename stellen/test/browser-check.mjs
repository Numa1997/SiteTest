// Clicks through the page in headless Chromium against the local server
// (npm run dev, with the invented records of test/seed.sql). Not part of
// `npm test`, because it needs a browser:
//
//   PLAYWRIGHT=/path/to/node_modules/playwright/index.js node test/browser-check.mjs [base-url] [screenshot-dir]
//   (PLAYWRIGHT may be left out when playwright is installed beside this folder)
//
// Checks, in German (default) and English, at 1440 × 900 and 390 × 844:
// no script error and no refused request (security policy); German first;
// the switch changes every visible word; a card can be marked Applied and
// put back; a hand-added posting appears and can be deleted; the record and
// e-mail log show; nothing scrolls sideways on a phone.
const pw = await import(process.env.PLAYWRIGHT ?? 'playwright');
const chromium = pw.chromium ?? pw.default.chromium;

const BASE = process.argv[2] ?? 'http://127.0.0.1:8787';
const SHOTS = process.argv[3] ?? null;
const results = [];
const check = (name, ok, detail = '') => { results.push({ name, ok, detail }); console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? '  · ' + detail : '')); };

const browser = await chromium.launch();
for (const [vw, vh, tag] of [[1440, 900, 'desktop'], [390, 844, 'phone']]) {
  const ctx = await browser.newContext({ viewport: { width: vw, height: vh }, locale: 'de-DE' });
  const page = await ctx.newPage();
  const problems = [];
  page.on('pageerror', e => problems.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') problems.push('console: ' + m.text()); });
  page.on('requestfailed', r => problems.push('failed: ' + r.url()));

  await page.goto(BASE + '/', { waitUntil: 'networkidle' });
  await page.waitForSelector('.board');
  check(`${tag}: html lang is de by default`, await page.getAttribute('html', 'lang') === 'de');
  check(`${tag}: German heading`, (await page.textContent('h1')) === 'Offene Stellen', await page.textContent('h1'));
  check(`${tag}: tab title`, (await page.title()) === 'Stellenrecherche · Numa Koudsie', await page.title());
  const tally = await page.$$eval('.tally .t b', bs => bs.map(b => b.textContent));
  // seed: 5 listed (n6 removed), j5 applied, +1 hand-added; Germany board = n1,n2,n3,(n5 applied),added → 4 open; Europe n4
  check(`${tag}: tally Open/Applied/Not relevant = 4/1/0`, tally.join('/') === '4/1/0', tally.join('/'));
  check(`${tag}: removed card is absent`, !(await page.content()).includes('Removed test card'));

  // open the computational category, see the card with its German title first
  await page.click('#cat-computational .sec-head');
  await page.click('#area-computational-berlin .area-head');
  await page.waitForTimeout(400);
  const h4 = await page.textContent('[data-card="j1"] h4');
  check(`${tag}: German page shows the employer's own title`, h4.includes('Simulationsingenieur Wärmeübertragung'), h4);
  const note = await page.textContent('[data-card="j1"] .note');
  check(`${tag}: German note when one exists`, note.startsWith('Erfundene Testkarte'), note.slice(0, 40));
  if (SHOTS) await page.screenshot({ path: `${SHOTS}/${tag}-de.png`, fullPage: false });

  // Applied, then Undo from the record
  await page.click('[data-card="j1"] .remove');
  await page.click('[data-card="j1"] .choose .applied');
  await page.waitForTimeout(500);
  const tally2 = await page.$$eval('.tally .t b', bs => bs.map(b => b.textContent));
  check(`${tag}: Beworben moves the card to the record`, tally2.join('/') === '3/2/0', tally2.join('/'));
  await page.click('#record .sec-head');
  await page.waitForTimeout(400);
  const recText = await page.textContent('#record');
  check(`${tag}: record lists it with the German title`, recText.includes('Simulationsingenieur Wärmeübertragung'));
  check(`${tag}: e-mail stage shown in German`, recText.includes('Eingangsbestätigung erhalten'));
  if (SHOTS) await page.screenshot({ path: `${SHOTS}/${tag}-de-record.png`, fullPage: false });
  await page.click('#record li:has-text("Simulationsingenieur") .undo');
  await page.waitForTimeout(500);
  const tally3 = await page.$$eval('.tally .t b', bs => bs.map(b => b.textContent));
  check(`${tag}: Rückgängig puts it back`, tally3.join('/') === '4/1/0', tally3.join('/'));

  // add a posting by hand, then delete it
  await page.click('#cat-energy .sec-head');
  await page.click('#cat-energy .add');
  await page.fill('[data-addform] input[name=url]', 'kein link');
  await page.click('[data-addform] .save');
  const err = await page.textContent('.form-error');
  check(`${tag}: form refuses a bad link in German`, err.startsWith('Bitte den vollständigen Link'), err);
  await page.fill('[data-addform] input[name=url]', 'https://example.com/test-' + tag);
  await page.fill('[data-addform] input[name=title]', 'Testingenieur Energie');
  await page.fill('[data-addform] input[name=city]', 'Leipzig');
  await page.check('[data-addform] input[value=leipzig]');
  await page.click('[data-addform] .save');
  await page.waitForTimeout(600);
  await page.click('#area-energy-leipzig .area-head').catch(() => {});
  await page.waitForTimeout(400);
  const mine = page.locator('.card.mine:has-text("Testingenieur Energie")');
  check(`${tag}: added card appears, marked "selbst hinzugefügt"`, (await mine.count()) === 1 && (await mine.textContent()).includes('selbst hinzugefügt'));
  page.once('dialog', d => d.accept());
  await mine.locator('.remove').click();
  await mine.locator('.mistake').click();
  await page.waitForTimeout(600);
  check(`${tag}: added card deleted without counting`, (await page.locator('.card.mine:has-text("Testingenieur Energie")').count()) === 0);

  // switch to English: every word changes, the choice survives a reload
  await page.click('.ubtn.lang');
  await page.waitForTimeout(200);
  check(`${tag}: English heading after the switch`, (await page.textContent('h1')) === 'Open postings');
  check(`${tag}: html lang en`, await page.getAttribute('html', 'lang') === 'en');
  const body = await page.textContent('.board');
  const leftovers = ['Offene Stellen', 'Bewerbungsnachweis', 'Alle öffnen', 'Abmelden', 'Stelle hinzufügen', 'Raum Leipzig'].filter(w => body.includes(w));
  check(`${tag}: no German interface words left on the English page`, leftovers.length === 0, leftovers.join(', '));
  await page.reload({ waitUntil: 'networkidle' });
  await page.waitForSelector('.board');
  check(`${tag}: English kept after reload`, (await page.textContent('h1')) === 'Open postings');
  await page.click('#cat-computational .sec-head').catch(() => {});
  await page.waitForTimeout(400);
  if (SHOTS) await page.screenshot({ path: `${SHOTS}/${tag}-en.png`, fullPage: false });
  // Europe board
  await page.click('.boardrow .segbtn:nth-child(2)');
  await page.waitForTimeout(200);
  check(`${tag}: Europe board heading`, (await page.textContent('h1')) === 'Open in Europe');
  await page.click('.ubtn.lang');
  await page.waitForTimeout(200);
  check(`${tag}: Europe board heading in German`, (await page.textContent('h1')) === 'Offen in Europa');
  await page.click('.boardrow .segbtn:nth-child(1)');

  const sideways = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  check(`${tag}: no sideways scroll`, sideways <= 0, sideways + ' px');
  const fonts = await page.evaluate(async () => { await document.fonts.ready; return [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, '')); });
  check(`${tag}: house fonts load from the site itself`, ['Instrument Serif', 'IBM Plex Sans', 'IBM Plex Mono'].every(f => fonts.includes(f)), [...new Set(fonts)].join(', '));
  check(`${tag}: no script error, no refused request`, problems.length === 0, problems.join(' | '));
  await ctx.close();
}
await browser.close();
const failed = results.filter(r => !r.ok).length;
console.log(`\n${results.length - failed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
