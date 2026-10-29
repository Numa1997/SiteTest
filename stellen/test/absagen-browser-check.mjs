// /absagen in headless Chromium against the local server (npm run dev, with mails sent to /api/ingest first):
// no script errors or blocked resources, no sideways scroll, fonts loaded, the print button, and a printed PDF.
// Usage: node test/absagen-browser-check.mjs [base-url] [folder-for-screenshots-and-pdf]
const pw = await import(process.env.PLAYWRIGHT ?? 'playwright');
const chromium = pw.chromium ?? pw.default.chromium;
const BASE = process.argv[2] ?? 'http://127.0.0.1:8787';
const OUT = process.argv[3] ?? null;
let fails = 0;
const check = (name, ok, detail = '') => { if (!ok) fails++; console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? '  · ' + detail : '')); };

const browser = await chromium.launch();
for (const [vw, vh, tag] of [[1440, 900, 'desktop'], [390, 844, 'phone']]) {
  const ctx = await browser.newContext({ viewport: { width: vw, height: vh }, locale: 'de-DE' });
  const page = await ctx.newPage();
  const problems = [];
  page.on('console', m => { if (m.type() === 'error') problems.push(m.text()); });
  page.on('pageerror', e => problems.push(String(e)));
  page.on('requestfailed', r => problems.push('failed ' + r.url()));
  await page.goto(BASE + '/absagen', { waitUntil: 'networkidle' });
  check(`${tag}: no script error, no blocked resource`, problems.length === 0, problems.join(' | ').slice(0, 300));
  const sw = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  check(`${tag}: no sideways scroll`, sw <= 1, 'overflow ' + sw + ' px');
  const fonts = await page.evaluate(async () => { await document.fonts.ready; return ['Instrument Serif', 'IBM Plex Sans'].map(f => document.fonts.check('16px "' + f + '"')); });
  check(`${tag}: Instrument Serif and IBM Plex Sans loaded`, fonts.every(Boolean), JSON.stringify(fonts));
  const n = await page.locator('article.mail').count();
  check(`${tag}: mails shown as boxes`, n > 0, n + ' boxes');
  const border = await page.locator('article.mail').first().evaluate(e => getComputedStyle(e).borderTopWidth + ' ' + getComputedStyle(e).borderLeftWidth);
  check(`${tag}: boxes clearly bordered`, /^1px 4px$/.test(border), border);
  check(`${tag}: print button present`, await page.locator('#print').isVisible());
  if (OUT) await page.screenshot({ path: `${OUT}/absagen-${tag}.png`, fullPage: true });
  if (tag === 'desktop' && OUT) {
    await page.emulateMedia({ media: 'print' });
    check('print: utility bar hidden', !(await page.locator('.utility').isVisible()));
    check('print: cover shown', await page.locator('.cover').isVisible());
    await page.pdf({ path: `${OUT}/absagen-print.pdf`, format: 'A4', preferCSSPageSize: true, printBackground: true });
    check('print: PDF written', true, `${OUT}/absagen-print.pdf`);
  }
  await ctx.close();
}
await browser.close();
console.log(fails ? `\n${fails} FAILED` : '\nALL PASS');
process.exit(fails ? 1 : 0);
