// Fig. 1: after the edit, check the page at 1440x900 and 390x844 — console errors, KaTeX errors, sideways scroll, every fold opens —
// and screenshot the three edited places. Run: node notes/fig01/render-check.cjs (serve.cjs on port 8701)
const { execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
const URL = 'http://localhost:8701/simulations/' + encodeURIComponent('Circular Wave Interference Visualization.html');
const exe = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const OUT = process.argv[2] || '/tmp/fig01-shots';
const sleep = ms => new Promise(r => setTimeout(r, ms));
require('fs').mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await chromium.launch({ executablePath: exe });
  const report = [];
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h } });
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push('pageerror: ' + e));
    page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
    page.on('requestfailed', r => errors.push('requestfailed: ' + r.url()));
    await page.goto(URL); await sleep(2500);
    // open every fold, one by one through its own toggle
    const folds = await page.evaluate(() => document.querySelectorAll('[data-fold-level]').length);
    let opened = 0; const stuck = [];
    for (let q = 0; q < folds; q++) {
      const state = await page.evaluate(q => { const n = document.querySelectorAll('[data-fold-level]')[q]; return { collapsed: n.getAttribute('data-collapsed'), id: n.id || n.querySelector('h3,h4,h2') && n.querySelector('h3,h4,h2').textContent.trim().slice(0, 40) }; }, q);
      if (state.collapsed === '1') {
        const btn = (await page.$$('[data-fold-level]'))[q];
        const t = await btn.$(':scope > .fs-head .fs-toggle');
        await t.scrollIntoViewIfNeeded(); await t.click(); await sleep(450);
      }
      const ok = await page.evaluate(q => { const n = document.querySelectorAll('[data-fold-level]')[q]; const f = n.querySelector(':scope > .fold'); return n.getAttribute('data-collapsed') === '0' && f && f.getBoundingClientRect().height > 20 && !f.hasAttribute('inert'); }, q);
      if (ok) opened++; else stuck.push(state.id);
    }
    await sleep(600);
    const res = await page.evaluate(() => ({
      katexErrors: document.querySelectorAll('.katex-error').length,
      katexCount: document.querySelectorAll('#paper .katex').length,
      rawDelims: (document.getElementById('paper').innerText.match(/\\\(|\\\[/g) || []).length,
      scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth,
      prefsLinks: Array.from(document.querySelectorAll('.prefs a')).map(a => a.href),
      prefsItems: document.querySelectorAll('.prefs li').length,
      lines: document.documentElement.outerHTML.length
    }));
    report.push({ viewport: w + 'x' + h, folds, opened, stuck, errors, ...res, sideways: res.scrollW > res.clientW });
    // screenshots of the edited paragraphs
    const shots = [
      ['p4', () => Array.from(document.querySelectorAll('#p-add p')).find(p => p.textContent.includes('scissors'))],
      ['p6', () => Array.from(document.querySelectorAll('#p-row p')).find(p => p.textContent.includes('Set the damping aside'))],
      ['refs', () => document.querySelector('.prefs')]
    ];
    for (const [name] of shots) {
      const handle = await page.evaluateHandle(name => {
        if (name === 'p4') return Array.from(document.querySelectorAll('#p-add p')).find(p => p.textContent.includes('scissors'));
        if (name === 'p6') return Array.from(document.querySelectorAll('#p-row p')).find(p => p.textContent.includes('Set the damping aside'));
        return document.querySelector('.prefs');
      }, name);
      const el = handle.asElement();
      if (el) { await el.scrollIntoViewIfNeeded(); await sleep(300); await el.screenshot({ path: `${OUT}/${name}-${w}.png` }); }
    }
    await ctx.close();
  }
  console.log(JSON.stringify(report, null, 1));
  await browser.close();
})();
