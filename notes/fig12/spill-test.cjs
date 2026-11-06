// Fig. 12: drive a hard bump in open loop until the stout spills, then run every data-panel check (node notes/fig12/spill-test.cjs <out> [base])
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path'), fs = require('fs');
(async () => {
  const out = process.argv[2] || '/tmp/fig12-spill'; fs.mkdirSync(out, { recursive: true });
  const base = process.argv[3] || 'http://localhost:8779'; const srv = process.argv[3] ? null : spawn('python3', ['-m', 'http.server', '8779', '--directory', path.join(__dirname, '../../public')], { stdio: 'ignore' }); await new Promise(r => setTimeout(r, 800));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 }); const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto(base + '/simulations/beer-slosh.html'); await p.waitForTimeout(800);
  await p.evaluate(() => { const set = (id, v) => { const el = document.getElementById(id); el.value = v; el.dispatchEvent(new Event('input')); }; set('bumpH', 25); set('v0', 1.0); });
  await p.click('#ctrl-off'); await p.click('#reset'); await p.waitForTimeout(300);
  await p.click('#ctrl-off');
  const t0 = Date.now();
  await p.waitForFunction(() => Fig12.world.fluid.spilled > 0 && Fig12.world.drops && Fig12.world.drops.some(d => !d.landed), null, { timeout: 240000, polling: 200 });
  await p.waitForTimeout(1200); await p.click('#play'); await p.waitForTimeout(300);
  const r = await p.evaluate(() => {
    const D = Sim.data, ds = D.ds, bad = []; let n = 0;
    const agree = (a, b) => typeof a !== 'number' ? String(a) === String(b) : (Number.isNaN(a) && Number.isNaN(b)) || Math.abs(a - b) <= 1e-9 * Math.max(Math.abs(a), Math.abs(b)) + 1e-12;
    for (const name in D.check) { const v = ds.vars[name]; if (!v) continue;
      if (v.dims.length) { const a = ds.get(name), np = ds.get('np'); for (const i of [0, Math.floor((name[0] === 'p' ? np : a.length) / 2), (name[0] === 'p' ? np : a.length) - 1]) { n++; if (!agree(a[i], D.check[name](i).value)) bad.push(name + '[' + i + ']'); } }
      else { n++; if (!agree(ds.get(name), D.check[name]().value)) bad.push(name + ' ' + ds.get(name) + ' vs ' + D.check[name]().value); } }
    const w = Fig12.world; return { t: w.t, spilled_g: ds.get('spilled_g'), ml: ds.get('ml'), drops: w.drops.length, airborne: w.drops.filter(d => !d.landed).length, n, bad };
  });
  console.log(`spilled after ${((Date.now() - t0) / 1000).toFixed(0)} s real, t = ${r.t.toFixed(2)} s simulated: ${r.spilled_g.toFixed(1)} g over the rim, ${r.ml.toFixed(4)} kg left, ${r.drops} drops (${r.airborne} in the air); checks ${r.n}, DIFFER ${r.bad.length ? JSON.stringify(r.bad) : 'none'}`);
  await p.locator('#stage').screenshot({ path: path.join(out, 'spill.png') });
  console.log('errors:', errs.length ? errs : 'none'); await b.close(); if (srv) srv.kill();
})();
