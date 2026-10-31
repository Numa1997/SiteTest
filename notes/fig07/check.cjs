// Fig. 7 page check in headless Chromium: console errors, KaTeX errors, sideways scroll, folds, store values.
// Run (with notes/fig07/serve.cjs serving /tmp/fig07-dist on 8707): node notes/fig07/check.cjs [tag]
'use strict';
const { execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
const fs = require('fs');
const URL = 'http://localhost:8707/simulations/phasor-sums.html';
const tag = process.argv[2] || 'run';
(async () => {
  const browser = await chromium.launch();
  const out = {};
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(URL, { waitUntil: 'load' });
    await page.waitForFunction(() => document.querySelectorAll('#paper .katex').length > 50, null, { timeout: 15000 });
    await page.waitForTimeout(1200);
    const r = await page.evaluate(() => {
      const ds = Sim.data.ds, el = document.scrollingElement;
      const fig = document.getElementById('stage').getBoundingClientRect();
      const ro = document.getElementById('r-energy').getBoundingClientRect();
      return {
        katexErrors: document.querySelectorAll('.katex-error').length,
        katexInPaper: document.querySelectorAll('#paper .katex').length,
        tags: Array.from(document.querySelectorAll('#paper .tag')).map(t => t.textContent.trim()),
        sideways: el.scrollWidth - el.clientWidth,
        box: [ds.get('box_w'), ds.get('box_h')], scale: ds.get('scale'), fitR: ds.get('fitR'), n_path: ds.get('n_path'),
        period: ds.get('period'), q: ds.get('q'),
        figure: { left: fig.left, right: fig.right, top: fig.top, bottom: fig.bottom },
        readoutE: { left: ro.left, right: ro.right, top: ro.top, bottom: ro.bottom },
        refs: Array.from(document.querySelectorAll('#paper .prefs li')).map(li => ({ text: li.textContent.slice(0, 60), links: Array.from(li.querySelectorAll('a')).map(a => a.href) }))
      };
    });
    // folds: close then open each one; count those that end open
    const folds = await page.evaluate(async () => {
      const nodes = Array.from(document.querySelectorAll('#paper [data-fold-level]'));
      let ok = 0, bad = [];
      for (const n of nodes) {
        const b = n.querySelector(':scope > .fs-head .fs-toggle');
        if (!b) { bad.push(n.id || n.textContent.slice(0, 30)); continue; }
        b.click(); await new Promise(r => setTimeout(r, 400));
        const closed = n.getAttribute('data-collapsed') === '1';
        b.click(); await new Promise(r => setTimeout(r, 400));
        const open = n.getAttribute('data-collapsed') === '0';
        if (closed && open) ok++; else bad.push(n.id || n.textContent.slice(0, 30));
      }
      return { total: nodes.length, ok, bad };
    });
    r.folds = folds;
    r.sidewaysAfterFolds = await page.evaluate(() => document.scrollingElement.scrollWidth - document.scrollingElement.clientWidth);
    r.katexErrorsAfter = await page.evaluate(() => document.querySelectorAll('.katex-error').length);
    r.consoleErrors = errors;
    await page.screenshot({ path: __dirname + `/shot-${tag}-${w}.png`, fullPage: false });
    const paper = await page.$('#paper');
    await paper.screenshot({ path: require('os').tmpdir() + `/fig07-paper-${tag}-${w}.png` });
    out[w] = r;
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(__dirname + `/check-${tag}.json`, JSON.stringify(out, null, 1));
  console.log(JSON.stringify(out, null, 1));
})();
