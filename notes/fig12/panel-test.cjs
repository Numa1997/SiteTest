// Fig. 12 data panel: every check and every read-back, run in Chromium (node notes/fig12/panel-test.cjs <out-dir> [base-url])
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/fig12-panel'; fs.mkdirSync(out, { recursive: true });
  let srv = null, base = process.argv[3];
  if (!base) { srv = spawn('python3', ['-m', 'http.server', '8775', '--directory', path.join(__dirname, '../../public')], { stdio: 'ignore' }); await new Promise(r => setTimeout(r, 800)); base = 'http://localhost:8775'; }
  const b = await chromium.launch(); const errs = [];
  const p = await b.newPage({ viewport: { width: 1600, height: 1100 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto(base + '/simulations/beer-slosh.html'); await p.waitForTimeout(5000);
  await p.click('#play'); await p.waitForTimeout(400);           // pause: store and picture hold still
  const res = await p.evaluate(() => {
    const D = Sim.data, ds = D.ds, out = { checks: [], drawn: [], missing: [] };
    // the panel's own agreement rule (datalog.js agreement): relative 1e-9 for float64
    const agree = (a, b) => { if (typeof a !== 'number' || typeof b !== 'number') return String(a) === String(b); const d = Math.abs(a - b), s = Math.max(Math.abs(a), Math.abs(b)); return d <= 1e-9 * s + 1e-12; };
    for (const g of D.groups) for (const name of g.vars) {
      const v = ds.vars[name]; if (!v) { out.missing.push(name); continue; }
      const fn = D.check[name];
      if (!fn) { out.checks.push([name, 'no check (a set value, constant or measurement)']); continue; }
      if (v.dims.length) {
        const arr = ds.get(name), idx = [0, Math.floor(arr.length / 3), Math.floor(arr.length / 2), arr.length - 1];
        for (const i of idx) { const c = fn(i); out.checks.push([name + '[' + i + ']', agree(arr[i], c.value) ? 'identical/agree' : 'DIFFER ' + arr[i] + ' vs ' + c.value]); }
      } else { const c = fn(); out.checks.push([name, agree(ds.get(name), c.value) ? 'identical/agree' : 'DIFFER ' + ds.get(name) + ' vs ' + c.value]); }
    }
    for (const name in D.drawn) { const r = D.drawn[name](); out.drawn.push([name, r.ok, r.drawn]); }
    return out;
  });
  const bad = res.checks.filter(c => /DIFFER/.test(c[1])), nochk = res.checks.filter(c => /^no check/.test(c[1])).map(c => c[0]);
  console.log('checks run:', res.checks.length - nochk.length, ' DIFFER:', bad.length ? bad : 'none');
  console.log('without a check:', nochk.join(' '));
  console.log('read-backs:', res.drawn.map(d => d[0] + '=' + d[1] + ' ' + d[2]).join(' | '));
  console.log('missing vars:', res.missing.length ? res.missing : 'none');
  // open the panel and take a picture
  const tab = p.locator('.dp-tab').first();
  if (await tab.count()) { await p.evaluate(() => document.querySelector('.dp-tab').scrollIntoView()); await p.evaluate(() => { const t = document.querySelector('.dp-tab'); if (t.getAttribute('aria-expanded') !== 'true') t.click(); }); await p.waitForTimeout(800); await p.screenshot({ path: path.join(out, 'panel.png'), fullPage: false }); }
  console.log('panel running while paused and closed:', await p.evaluate(() => window.__dataPanel && window.__dataPanel.running()));
  console.log('errors:', errs.length ? errs : 'none');
  await b.close(); if (srv) srv.kill();
})();
