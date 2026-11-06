// Fig. 12 browser test: errors, KaTeX, overflow, data-panel checks and read-backs, walkthrough, a scripted drag on the side view,
// the bump under each control law, and the checks the reviews asked for. node notes/fig12/test.cjs <outdir> [width] [de/|ar/]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2], W = +(process.argv[3] || 1440);
  const b = await chromium.launch();
  const pg = await (await b.newContext({ viewport: { width: W, height: W < 600 ? 844 : 900 } })).newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await pg.goto('http://localhost:8765/' + (process.argv[4] || '') + 'simulations/beer-slosh.html', { waitUntil: 'networkidle' });
  await pg.waitForFunction(() => window.SLOSH && window.SLOSH.cartMap, { timeout: 30000 }); await pg.waitForTimeout(500);
  // scripted push: pointer down on the side view, drag 60 px along the road, hold, release
  await pg.evaluate(() => document.getElementById('stage-cart').scrollIntoView());
  const bx = await (await pg.$('#cart')).boundingBox();
  const cx = bx.x + bx.width / 2, cy = bx.y + bx.height * 0.4;
  await pg.mouse.move(cx, cy); await pg.mouse.down(); for (let i = 1; i <= 10; i++) { await pg.mouse.move(cx + 6 * i, cy); await pg.waitForTimeout(20); }
  const Fheld = await pg.evaluate(() => window.SLOSH.push.Fx); await pg.waitForTimeout(400); await pg.mouse.up();
  const Fafter = await pg.evaluate(() => window.SLOSH.push.Fx + window.SLOSH.push.Fz);
  await pg.waitForTimeout(800);
  const r = await pg.evaluate(() => {
    const S = window.SLOSH, ds = S.ds, D = Sim.data, res = { checks: [], drawn: {} };
    for (const [name, fn] of Object.entries(D.check)) {
      const v = ds.get(name); const isArr = v && v.length !== undefined && typeof v !== 'string';
      const idxs = isArr ? [0, 2, v.length - 1] : [null];
      for (const k of idxs) { const c = fn(k), sv = isArr ? v[k] : v, rel = Math.abs(c.value - sv) / Math.max(1e-30, Math.abs(sv)); res.checks.push([name + (isArr ? '[' + k + ']' : ''), sv, c.value, rel < 1e-9 || Math.abs(c.value - sv) < 1e-15 ? 'identical' : rel < 1e-6 ? 'agree' : 'DIFFER']); }
    }
    for (const [name, fn] of Object.entries(D.drawn)) res.drawn[name] = fn();
    res.xc = S.q[S.IX]; res.vx = S.qd[S.IX]; res.walk = !!document.querySelector('#walk .walk__card, #walk table, #walk [class*=walk]');
    res.katex = document.querySelectorAll('.katex-error').length; res.over = document.documentElement.scrollWidth - document.documentElement.clientWidth;
    res.pending = document.querySelectorAll('.i18n-pending').length;
    // the bump under each law, stepped directly: the three peaks must be ordered passive > skyhook > lqr, and the head must stay in under the LQR
    res.bump = {};
    for (const law of ['passive', 'skyhook', 'lqr']) {
      document.querySelector(`#law button[data-v="${law}"]`).click(); document.querySelector('#road button[data-v="bump"]').click(); S.restart();
      let peak = 0, spills = 0; for (let i = 0; i < 3000; i++) { S.step(); if (i % 10 === 0) { let best = -1e9; for (let q = 0; q < 72; q++) best = Math.max(best, S.etaWall(2 * Math.PI * q / 72)); peak = Math.max(peak, Math.abs(best)); } }
      res.bump[law] = +(peak * 1e3).toFixed(2);
    }
    // the kick: on the up-slope of the bump the road pushes back (negative), on the down-slope forward; on a smooth road nothing
    document.querySelector('#law button[data-v="passive"]').click(); document.querySelector('#road button[data-v="bump"]').click(); S.restart();
    let kmin = 0, kmax = 0; for (let i = 0; i < 1500; i++) { S.step(); kmin = Math.min(kmin, S.road.kick); kmax = Math.max(kmax, S.road.kick); }
    document.querySelector('#road button[data-v="smooth"]').click(); S.restart(); let ksm = 0; for (let i = 0; i < 1500; i++) { S.step(); ksm = Math.max(ksm, Math.abs(S.road.kick)); }
    res.kick = { back: kmin, forward: kmax, smooth: ksm };
    // the axle's path is the envelope: at a kerb the rim meets the edge before the axle is over it
    document.querySelector('#road button[data-v="kerb"]').click(); S.buildRoad(); res.kerb = { za_before: S.zAxle(0.97), zr_before: S.zRoad(0.97), za_on: S.zAxle(1.1), zr_on: S.zRoad(1.1) };
    // restart after a kerb under the LQR: the first controller sample is quiet
    document.querySelector('#law button[data-v="lqr"]').click(); S.restart(); for (let i = 0; i < 2500; i++) S.step();
    S.restart(); S.step(); res.restartU = Math.max(Math.abs(ds.get('u_s')), Math.abs(ds.get('u_m')));
    // the rough road: its highest point in the first 3 m is the slider's height, and it starts without a step
    document.querySelector('#road button[data-v="rough"]').click(); S.buildRoad(); S.restart(); let pk = 0; for (let x = 1; x <= 4; x += 0.001) pk = Math.max(pk, Math.abs(S.zRoad(x)));
    res.rough = { peak_mm: pk * 1e3, h_mm: S.P.hr * 1e3, z_start_mm: Math.abs(S.zRoad(1.002)) * 1e3 };
    // the design is deferred: a slider's input marks it dirty; the next control sample under the LQR runs it
    document.getElementById('se').dispatchEvent(new Event('input', { bubbles: true })); res.designDirty = S.Ct.dirty === true; S.step(); res.designRan = S.Ct.dirty === false && S.Ct.ok === true;
    // the interpolated shapes keep their size between two data fills: max|ψ(rim)| = 1 for every mode at 490 mL
    const sl = document.getElementById('V'); sl.value = 490; sl.dispatchEvent(new Event('input', { bubbles: true })); res.rim490 = { min: Math.min(...ds.get('rim_max')), max: Math.max(...ds.get('rim_max')), Qx11: ds.get('Qx')[0] }; sl.value = 500; sl.dispatchEvent(new Event('input', { bubbles: true }));
    document.querySelector('#law button[data-v="passive"]').click(); document.querySelector('#road button[data-v="smooth"]').click(); S.restart();
    return res;
  });
  const bad = r.checks.filter(c => c[3] === 'DIFFER');
  const order = r.bump.passive > r.bump.skyhook && r.bump.skyhook > r.bump.lqr;
  console.log(`${process.argv[4] || 'en/'} width ${W}: errors ${errs.length}, katex errors ${r.katex}, overflow ${r.over}px, pending ${r.pending}, walkthrough ${r.walk}`);
  console.log(`checks: ${r.checks.length - bad.length}/${r.checks.length} agree` + (bad.length ? ' DIFFER: ' + JSON.stringify(bad) : ''));
  console.log('drawn:', JSON.stringify(r.drawn));
  console.log(`push: force while held ${Fheld.toFixed(1)} N, after release ${Fafter} N; cart ahead ${(r.xc * 1000).toFixed(1)} mm, speed ${(r.vx * 1000).toFixed(0)} mm/s`);
  console.log(`bump peaks (mm): passive ${r.bump.passive}, skyhook ${r.bump.skyhook}, lqr ${r.bump.lqr}; ordered ${order}`);
  const kickOk = r.kick.back < -10 && r.kick.forward > 5 && r.kick.smooth < 1e-9, kerbOk = r.kerb.za_before > r.kerb.zr_before + 1e-3 && Math.abs(r.kerb.za_on - r.kerb.zr_on) < 1e-6;
  const roughOk = Math.abs(r.rough.peak_mm - r.rough.h_mm) < 0.05 && r.rough.z_start_mm < 0.01, rimOk = r.rim490.min > 0.999 && r.rim490.max < 1.001 && Math.abs(r.rim490.Qx11) > 0.03;
  console.log(`kick: back ${r.kick.back.toFixed(1)} N, forward ${r.kick.forward.toFixed(1)} N, smooth road ${r.kick.smooth}; kerb envelope: axle ${(r.kerb.za_before * 1000).toFixed(1)} mm while the road is ${(r.kerb.zr_before * 1000).toFixed(1)} mm (3 cm before the edge); ${kickOk && kerbOk ? 'ok' : 'WRONG'}`);
  console.log(`restart after kerb: first LQR sample ${r.restartU.toExponential(1)} N; rough road peak ${r.rough.peak_mm.toFixed(2)} mm for slider ${r.rough.h_mm} mm, start ${r.rough.z_start_mm.toExponential(1)} mm; design deferred ${r.designDirty} then run ${r.designRan}; rim max at 490 mL ${r.rim490.min.toFixed(5)}..${r.rim490.max.toFixed(5)}, Q11 ${(r.rim490.Qx11 * 1e3).toFixed(2)} mm`);
  const extraOk = kickOk && kerbOk && r.restartU < 1e-2 && roughOk && r.designDirty && r.designRan && rimOk && r.bump.lqr < 2;
  if (errs.length) console.log(errs.slice(0, 6).join('\n'));
  await pg.screenshot({ path: `${out}/test-${W}.png`, fullPage: false });
  await b.close();
  const okDrawn = Object.values(r.drawn).every(d => d.ok !== false);
  process.exit(errs.length || bad.length || r.katex || r.over > 0 || r.pending || !order || Fheld <= 0 || Fafter !== 0 || !okDrawn || !extraOk ? 1 : 0);
})();
