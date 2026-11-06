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
    // the review's checks (round 3)
    // 1. the 3D body pitches the right way: with the pitch +0.1 rad (front down) the glass foot must sit at x_O = d_g + h_g ψ, z_O = h_g − d_g ψ (+ the body's height), read back from the glass group's world matrix
    document.querySelector('#law button[data-v="passive"]').click(); document.querySelector('#road button[data-v="smooth"]').click(); S.restart();
    S.q[S.IP] = 0.1; window.SLOSH3D.render(); const T = window.SLOSH3D; const wp = new (T.scene.position.constructor)(); T.glassG.getWorldPosition(wp); const bp = T.cart.position;
    res.pitch3d = { x: wp.x, y: wp.y - bp.y, x_phys: S.P.dg * Math.cos(0.1) + S.P.hg * Math.sin(0.1), z_phys: S.P.hg * Math.cos(0.1) - S.P.dg * Math.sin(0.1) }; S.q[S.IP] = 0; S.restart();
    // 2. restart after a kerb under the LQR: the first controller sample must be quiet (the road under the wheels is reset)
    document.querySelector('#law button[data-v="lqr"]').click(); document.querySelector('#road button[data-v="kerb"]').click(); S.restart(); for (let i = 0; i < 2500; i++) S.step();
    S.restart(); S.step(); res.restartU = Math.max(Math.abs(ds.get('u_f')), Math.abs(ds.get('u_r')));
    // 3. the rough road: its highest point in the first 3 m is the slider's height, and it starts without a step
    document.querySelector('#road button[data-v="rough"]').click(); S.restart(); let pk = 0; for (let x = 1; x <= 4; x += 0.001) pk = Math.max(pk, Math.abs(S.zRoad(x))); res.rough = { peak_mm: pk * 1e3, h_mm: S.P.hr * 1e3, z_start_mm: Math.abs(S.zRoad(1.0005)) * 1e3 };
    // 4. the design is deferred: a slider's input marks it dirty; the next control sample under the LQR runs it
    const before = S.Ct.iters; document.getElementById('se').dispatchEvent(new Event('input', { bubbles: true })); res.designDirty = S.Ct.dirty === true; S.step(); res.designRan = S.Ct.dirty === false && S.Ct.ok === true;
    // 5. a second pointer ends a push (synthetic pointer events on the canvas)
    const cv = window.SLOSH3D.canvas, rb = cv.getBoundingClientRect(), pe = (type, id, x, y) => cv.dispatchEvent(new PointerEvent(type, { pointerId: id, pointerType: 'touch', clientX: x, clientY: y, bubbles: true, isPrimary: id === 1 }));
    document.querySelector('#road button[data-v="smooth"]').click(); S.restart();
    S.setPush(30); pe('pointerdown', 1, rb.left + rb.width / 2, rb.top + rb.height / 2); pe('pointerdown', 2, rb.left + rb.width / 2 + 80, rb.top + rb.height / 2); res.pinchEndsPush = S.push.F; pe('pointerup', 1, 0, 0); pe('pointerup', 2, 0, 0); S.setPush(0);
    // 6. a plain wheel over the view does not zoom; Shift + wheel does
    const d0 = T.view.dist; cv.dispatchEvent(new WheelEvent('wheel', { deltaY: 300, bubbles: true, cancelable: true })); const d1 = T.view.dist; cv.dispatchEvent(new WheelEvent('wheel', { deltaY: 300, shiftKey: true, bubbles: true, cancelable: true })); const d2 = T.view.dist; T.view.dist = d0; T.placeCam();
    res.wheel = { plain: d1 === d0, shift: d2 !== d0 };
    // 7. the interpolated shapes keep their size between two data fills (the sign rule): max|ψ(rim)| = 1 for every mode at 490 mL
    Sim.setSlider ? 0 : 0; const sl = document.getElementById('V'); sl.value = 490; sl.dispatchEvent(new Event('input', { bubbles: true })); res.rim490 = { min: Math.min(...ds.get('rim_max')), max: Math.max(...ds.get('rim_max')), Qx11: ds.get('Qx')[0] }; sl.value = 500; sl.dispatchEvent(new Event('input', { bubbles: true }));
    document.querySelector('#law button[data-v="passive"]').click(); S.restart();
    return res;
  });
  const bad = r.checks.filter(c => c[3] === 'DIFFER');
  const order = r.bump.passive > r.bump.skyhook && r.bump.skyhook > r.bump.lqr;
  console.log(`${process.argv[4] || 'en/'} width ${W}: errors ${errs.length}, katex errors ${r.katex}, overflow ${r.over}px, walkthrough ${r.walk}`);
  console.log(`checks: ${r.checks.length - bad.length}/${r.checks.length} agree` + (bad.length ? ' DIFFER: ' + JSON.stringify(bad) : ''));
  console.log('drawn:', JSON.stringify(r.drawn));
  console.log(`push: force while held ${Fheld.toFixed(1)} N, after release ${Fafter} N; cart moved ${(r.xc * 1000).toFixed(1)} mm, speed ${(r.vx * 1000).toFixed(0)} mm/s`);
  console.log(`bump peaks (mm): passive ${r.bump.passive}, skyhook ${r.bump.skyhook}, lqr ${r.bump.lqr}; ordered ${order}`);
  const p3 = Math.abs(r.pitch3d.x - r.pitch3d.x_phys) < 1e-6 && Math.abs(r.pitch3d.y - r.pitch3d.z_phys) < 1e-6;
  const roughOk = Math.abs(r.rough.peak_mm - r.rough.h_mm) < 0.05 && r.rough.z_start_mm < 0.01, rimOk = r.rim490.min > 0.999 && r.rim490.max < 1.001 && Math.abs(r.rim490.Qx11) > 0.03;
  console.log(`3D pitch read-back: glass foot x ${r.pitch3d.x.toFixed(5)} (physics ${r.pitch3d.x_phys.toFixed(5)}), z ${r.pitch3d.y.toFixed(5)} (physics ${r.pitch3d.z_phys.toFixed(5)}): ${p3 ? 'identical' : 'DIFFER'}`);
  console.log(`restart after kerb: first LQR sample ${r.restartU.toExponential(1)} N; rough road peak ${r.rough.peak_mm.toFixed(2)} mm for slider ${r.rough.h_mm} mm, start ${r.rough.z_start_mm.toExponential(1)} mm; design deferred ${r.designDirty} then run ${r.designRan}; pinch ends push ${r.pinchEndsPush === 0}; wheel plain/shift ${r.wheel.plain}/${r.wheel.shift}; rim max at 490 mL ${r.rim490.min.toFixed(5)}..${r.rim490.max.toFixed(5)}, Q11 ${(r.rim490.Qx11 * 1e3).toFixed(2)} mm`);
  const extraOk = p3 && r.restartU < 1e-2 && roughOk && r.designDirty && r.designRan && r.pinchEndsPush === 0 && r.wheel.plain && r.wheel.shift && rimOk;
  if (errs.length) console.log(errs.slice(0, 6).join('\n'));
  await pg.screenshot({ path: `${out}/test-${W}.png`, fullPage: false });
  await b.close();
  const okDrawn = Object.values(r.drawn).every(d => d.ok !== false);
  process.exit(errs.length || bad.length || r.katex || r.over > 0 || !order || Fheld <= 0 || Fafter !== 0 || !okDrawn || !extraOk ? 1 : 0);
})();
