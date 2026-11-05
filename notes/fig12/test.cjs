// Fig. 12 browser test: errors, KaTeX, overflow, data-panel checks and read-backs, walkthrough, scripted drag. node notes/fig12/test.cjs <outdir> [width]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2], W = +(process.argv[3] || 1440);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: W, height: W < 600 ? 844 : 900 } })).newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await pg.goto('http://localhost:8765/' + (process.argv[4] || '') + 'simulations/beer-slosh.html', { waitUntil: 'networkidle' });
  await pg.waitForTimeout(1500);
  // scripted drag of the glass: pointer down on the glass, move 60 px right, release
  const box = await (await pg.$('#stage3d canvas')).boundingBox();
  await pg.evaluate(() => document.getElementById('stage3d').scrollIntoView());
  const b2 = await (await pg.$('#stage3d canvas')).boundingBox();
  const cx = b2.x + b2.width / 2, cy = b2.y + b2.height * 0.45;
  await pg.mouse.move(cx, cy); await pg.mouse.down(); for (let i = 1; i <= 10; i++) { await pg.mouse.move(cx + 8 * i, cy); await pg.waitForTimeout(20); } await pg.mouse.up();
  await pg.waitForTimeout(2500);
  const r = await pg.evaluate(() => {
    const S = window.SLOSH, ds = S.ds, D = Sim.data, res = { checks: [], drawn: {} };
    for (const [name, fn] of Object.entries(D.check)) {
      const v = ds.get(name); const isArr = v && v.length !== undefined && typeof v !== 'string';
      const idxs = isArr ? [0, 2, v.length - 1] : [null];
      for (const k of idxs) { const c = fn(k), sv = isArr ? v[k] : v, rel = Math.abs(c.value - sv) / Math.max(1e-30, Math.abs(sv)); res.checks.push([name + (isArr ? '[' + k + ']' : ''), sv, c.value, rel < 1e-9 || Math.abs(c.value - sv) < 1e-15 ? 'identical' : rel < 1e-6 ? 'agree' : 'DIFFER']); }
    }
    for (const [name, fn] of Object.entries(D.drawn)) res.drawn[name] = fn();
    res.glass = { x: ds.get('xg'), Tx: S.Tg.x }; res.eta = ds.get('eta_w'); res.walk = !!document.querySelector('#walk .walk__card, #walk table, #walk [class*=walk]');
    res.katex = document.querySelectorAll('.katex-error').length; res.over = document.documentElement.scrollWidth - document.documentElement.clientWidth;
    res.ungrouped = Object.keys(ds.vars ? ds.vars : {}).length; return res;
  });
  const bad = r.checks.filter(c => c[3] === 'DIFFER');
  console.log(`${process.argv[4] || 'en/'} width ${W}: errors ${errs.length}, katex errors ${r.katex}, overflow ${r.over}px, walkthrough ${r.walk}`);
  console.log(`checks: ${r.checks.length - bad.length}/${r.checks.length} agree` + (bad.length ? ' DIFFER: ' + JSON.stringify(bad) : ''));
  console.log('drawn:', JSON.stringify(r.drawn));
  console.log(`drag: glass target x = ${(r.glass.Tx * 1000).toFixed(1)} mm, glass at ${(r.glass.x * 1000).toFixed(1)} mm; wave at wall after release ${(r.eta * 1000).toFixed(2)} mm`);
  if (errs.length) console.log(errs.slice(0, 6).join('\n'));
  await pg.screenshot({ path: `${out}/test-${W}.png`, fullPage: false });
  await b.close(); process.exit(errs.length || bad.length || r.katex || r.over > 0 ? 1 : 0);
})();
