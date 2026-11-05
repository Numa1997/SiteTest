// Fig. 12 browser test: errors, KaTeX, overflow, data-panel checks and read-backs, walkthrough, a scripted push of the cart, a bump
// under each control law. node notes/fig12/test.cjs <outdir> [width] [de/|ar/]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2], W = +(process.argv[3] || 1440);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: W, height: W < 600 ? 844 : 900 } })).newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await pg.goto('http://localhost:8765/' + (process.argv[4] || '') + 'simulations/beer-slosh.html', { waitUntil: 'networkidle' });
  await pg.waitForFunction(() => window.SLOSH3D, { timeout: 60000 }); await pg.waitForTimeout(800);
  // scripted push: pointer down on the cart's body, drag 60 px along the screen projection of x, hold, release
  await pg.evaluate(() => document.getElementById('stage3d').scrollIntoView());
  const b2 = await (await pg.$('#stage3d canvas')).boundingBox();
  const cx = b2.x + b2.width / 2, cy = b2.y + b2.height * 0.62;
  await pg.mouse.move(cx, cy); await pg.mouse.down(); for (let i = 1; i <= 10; i++) { await pg.mouse.move(cx + 6 * i, cy); await pg.waitForTimeout(20); }
  const Fheld = await pg.evaluate(() => window.SLOSH.push.F); await pg.waitForTimeout(400); await pg.mouse.up();
  const Fafter = await pg.evaluate(() => window.SLOSH.push.F);
  await pg.waitForTimeout(800);
  const r = await pg.evaluate(() => {
    const S = window.SLOSH, ds = S.ds, D = Sim.data, res = { checks: [], drawn: {} };
    for (const [name, fn] of Object.entries(D.check)) {
      const v = ds.get(name); const isArr = v && v.length !== undefined && typeof v !== 'string';
      const idxs = isArr ? [0, 2, v.length - 1] : [null];
      for (const k of idxs) { const c = fn(k), sv = isArr ? v[k] : v, rel = Math.abs(c.value - sv) / Math.max(1e-30, Math.abs(sv)); res.checks.push([name + (isArr ? '[' + k + ']' : ''), sv, c.value, rel < 1e-9 || Math.abs(c.value - sv) < 1e-15 ? 'identical' : rel < 1e-6 ? 'agree' : 'DIFFER']); }
    }
    for (const [name, fn] of Object.entries(D.drawn)) res.drawn[name] = fn();
    res.xc = S.q[S.IX]; res.vx = S.qd[S.IX]; res.eta = ds.get('eta_w'); res.walk = !!document.querySelector('#walk .walk__card, #walk table, #walk [class*=walk]');
    res.katex = document.querySelectorAll('.katex-error').length; res.over = document.documentElement.scrollWidth - document.documentElement.clientWidth;
    // the bump under each law, stepped directly: the three peaks must be ordered passive > skyhook > lqr
    res.bump = {};
    for (const law of ['passive', 'skyhook', 'lqr']) {
      document.querySelector(`#law button[data-v="${law}"]`).click(); document.querySelector('#road button[data-v="bump"]').click(); S.restart();
      let peak = 0; for (let i = 0; i < 3000; i++) { S.step(); if (i % 10 === 0) { let best = -1e9; for (let q = 0; q < 72; q++) best = Math.max(best, S.etaWall(2 * Math.PI * q / 72)); peak = Math.max(peak, Math.abs(best)); } }
      res.bump[law] = +(peak * 1e3).toFixed(2);
    }
    document.querySelector('#law button[data-v="passive"]').click(); document.querySelector('#road button[data-v="smooth"]').click(); S.restart();
    return res;
  });
  const bad = r.checks.filter(c => c[3] === 'DIFFER');
  const order = r.bump.passive > r.bump.skyhook && r.bump.skyhook > r.bump.lqr;
  console.log(`${process.argv[4] || 'en/'} width ${W}: errors ${errs.length}, katex errors ${r.katex}, overflow ${r.over}px, walkthrough ${r.walk}`);
  console.log(`checks: ${r.checks.length - bad.length}/${r.checks.length} agree` + (bad.length ? ' DIFFER: ' + JSON.stringify(bad) : ''));
  console.log('drawn:', JSON.stringify(r.drawn));
  console.log(`push: force while held ${Fheld.toFixed(1)} N, after release ${Fafter} N; cart moved ${(r.xc * 1000).toFixed(1)} mm, speed ${(r.vx * 1000).toFixed(0)} mm/s`);
  console.log(`bump peaks (mm): passive ${r.bump.passive}, skyhook ${r.bump.skyhook}, lqr ${r.bump.lqr}; ordered ${order}`);
  if (errs.length) console.log(errs.slice(0, 6).join('\n'));
  await pg.screenshot({ path: `${out}/test-${W}.png`, fullPage: false });
  await b.close();
  const okDrawn = Object.values(r.drawn).every(d => d.ok !== false);
  process.exit(errs.length || bad.length || r.katex || r.over > 0 || !order || Fheld <= 0 || Fafter !== 0 || !okDrawn ? 1 : 0);
})();
