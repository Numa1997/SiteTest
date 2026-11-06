// Fig. 12 data panel, part 2: checks on a bump, Read values, a recorded round, Save, idle (node notes/fig12/panel-test2.cjs <out>)
const { chromium } = require('playwright'); const { spawn, execFileSync } = require('child_process'); const path = require('path'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/fig12-panel2'; fs.mkdirSync(out, { recursive: true });
  const srv = spawn('python3', ['-m', 'http.server', '8776', '--directory', path.join(__dirname, '../../public')], { stdio: 'ignore' }); await new Promise(r => setTimeout(r, 800));
  const b = await chromium.launch(); const errs = [];
  for (const W of [1600, 1100, 390]) {
    const p = await b.newPage({ viewport: { width: W, height: 1000 }, deviceScaleFactor: 1, acceptDownloads: true });
    p.on('pageerror', e => errs.push(W + ': ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(W + ': ' + m.text()); });
    await p.goto('http://localhost:8776/simulations/beer-slosh.html');
    // wait until the wheel is on the first bump (x between 0.92 and 1.08 m), then pause
    await p.waitForFunction(() => Fig12.world.cart.x > 0.92, null, { timeout: 60000, polling: 50 });
    await p.click('#play'); await p.waitForTimeout(300);
    const r = await p.evaluate(() => {
      const D = Sim.data, ds = D.ds, bad = []; let n = 0;
      const agree = (a, b) => typeof a !== 'number' ? String(a) === String(b) : Math.abs(a - b) <= 1e-9 * Math.max(Math.abs(a), Math.abs(b)) + 1e-12;
      for (const name in D.check) { const v = ds.vars[name]; if (!v) continue;
        if (v.dims.length) { const a = ds.get(name); for (const i of [0, Math.floor(a.length / 2), a.length - 1]) { n++; if (!agree(a[i], D.check[name](i).value)) bad.push(name + '[' + i + ']'); } }
        else { n++; if (!agree(ds.get(name), D.check[name]().value)) bad.push(name + ' ' + ds.get(name) + ' vs ' + D.check[name]().value); } }
      const dr = Object.keys(D.drawn).map(k => k + ':' + D.drawn[k]().ok);
      return { x: Fig12.world.cart.x, dza: ds.get('dz_a'), N: ds.get('N'), n, bad, dr: dr.filter(s => !/true$/.test(s)) };
    });
    console.log(W + 'px on the bump: x = ' + r.x.toFixed(3) + ' m, z_a′ = ' + r.dza.toFixed(4) + ', N = ' + r.N.toFixed(2) + ' N; checks ' + r.n + ', DIFFER ' + (r.bad.length ? JSON.stringify(r.bad) : 'none') + '; read-backs failing: ' + (r.dr.length ? r.dr : 'none'));
    if (W !== 1600) { await p.close(); continue; }
    // close the panel, Live off: no work
    await p.evaluate(() => document.querySelector('.dp__close').click());
    await p.waitForTimeout(1500);
    console.log('panel closed, paused: running =', await p.evaluate(() => window.__dataPanel.running()));
    // pointer sweep with Read values off: the figure must not change
    const box = await p.locator('#cv').boundingBox();
    const before = await p.locator('#cv').screenshot();
    for (let k = 0; k <= 40; k++) await p.mouse.move(box.x + box.width * k / 40, box.y + box.height * 0.45);
    await p.waitForTimeout(300);
    const after = await p.locator('#cv').screenshot();
    console.log('sweep with Read values off: figure unchanged =', Buffer.compare(before, after) === 0);
    // Read values on, pin the stout
    const rv = p.locator('button:has-text("Read values")').first(); await rv.click(); await p.waitForTimeout(300);
    const at = await p.evaluate(() => ({ x: Sim.data.ds.get('axle_px_x'), y: Sim.data.ds.get('front_px_y') + 15 }));
    await p.mouse.click(box.x + at.x, box.y + at.y); await p.waitForTimeout(600);
    const strip = await p.evaluate(() => { const s = document.querySelector('.dp-strip, .dp-read, [class*="strip"]'); if (!s) return null; const r = s.getBoundingClientRect(), f = document.getElementById('stage').getBoundingClientRect(); return { text: s.textContent.slice(0, 120), top: r.top, figBottom: f.bottom }; });
    console.log('pinned strip:', JSON.stringify(strip));
    await p.screenshot({ path: path.join(out, 'pinned.png') });
    // play, record one round
    await p.evaluate(() => { const t = document.querySelector('.dp-tab'); if (t.getAttribute('aria-expanded') !== 'true') t.click(); });
    await p.click('#play');
    await p.locator('button:has-text("Record")').first().click();
    await p.waitForFunction(() => window.__dataPanel.rounds().length > 0, null, { timeout: 120000, polling: 500 });
    console.log('rounds recorded:', await p.evaluate(() => window.__dataPanel.rounds().length));
    await p.waitForTimeout(800); await p.screenshot({ path: path.join(out, 'round.png') });
    // save
    const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 30000 }), p.locator('button:has-text("Save")').first().click()]);
    const file = path.join(out, 'fig12.npz'); await dl.saveAs(file); console.log('saved', file, fs.statSync(file).size, 'bytes');
    await p.close();
  }
  console.log('errors:', errs.length ? errs : 'none');
  await b.close(); srv.kill();
})();
