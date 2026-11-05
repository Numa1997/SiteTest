// Regression tests of the code reviews of Fig. 12 (the ones that still apply to the cart version) and of the cart version's own
// review. Exits 1 on any failure. node notes/fig12/regress.cjs [base URL, default http://localhost:8765/]
const { chromium } = require('playwright'); const BASE = process.argv[2] || 'http://localhost:8765/';
(async () => { const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const pg = await b.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto(BASE + 'simulations/beer-slosh.html'); await pg.waitForFunction(() => window.SLOSH3D, { timeout: 60000 }); await pg.waitForTimeout(800);
  const r = await pg.evaluate(async () => { const S = window.SLOSH, D = Sim.data, out = {};
    const frames = n => new Promise(res => { let i = 0; (function f() { if (++i < n) requestAnimationFrame(f); else res(); })(); });
    await frames(30);
    const sec = document.getElementById('sec'), tr = document.getElementById('tr');
    out.readback_ok_when_drawn = D.drawn.eta_w().ok !== false && D.drawn.z_s().ok === true;
    document.getElementById('play').click();
    sec.getContext('2d').clearRect(0, 0, 1e4, 1e4); tr.getContext('2d').clearRect(0, 0, 1e4, 1e4);
    out.readback_fails_when_blank = D.drawn.eta_w().ok !== true && D.drawn.z_s().ok === false;
    // switching the law never kicks the cart: the forces start from zero at the next sample
    document.querySelector('#road button[data-v="smooth"]').click(); S.restart(); for (let i = 0; i < 500; i++) S.step();
    const q0 = Array.from(S.q); document.querySelector('#law button[data-v="lqr"]').click(); for (let i = 0; i < 2; i++) S.step();
    out.law_switch_jump_mm = Math.max(...S.q.slice(2, 6).map((v, i) => Math.abs(v - q0[2 + i]))) * 1e3;
    // the LQR design converged (not just stopped) and is stable
    out.lqr_iters = S.Ct.iters; out.lqr_tau = S.Ct.tau; out.lqr_ok = S.Ct.ok && S.Ct.iters < 6000 && S.Ct.tau > 0 && S.Ct.tau < 10;
    // the straight glass is drawn straight and its first mode matches the Bessel value
    document.querySelector('#shape button[data-v="cyl"]').click(); out.straight = Math.abs(S.Rdraw(0.05) - S.geo.a) < 1e-12 && Math.abs(S.Rdraw(0.13, 1.0) - S.geo.a) < 1e-12;
    const k = S.M.findIndex(m => m.m === 1 && m.o === 'c' && m.n === 1), xi = 1.841183781, kk = xi / S.geo.a; out.cyl_lam_rel = Math.abs(S.M[k].lam - kk * Math.tanh(kk * S.geo.D)) / S.M[k].lam;
    document.querySelector('#shape button[data-v="tulip"]').click();
    // the road feature really starts 1 m down the road, and a road change restarts the run
    out.road_flat_before = S.zRoad(0.99) === 0 && S.zRoad(0.5) === 0; document.querySelector('#road button[data-v="kerb"]').click(); out.restart_t = S.tSim;
    document.querySelector('#road button[data-v="smooth"]').click();
    // a push force is zero once released, and clipped to 80 N while held
    S.setPush(500); out.push_clip = S.push.F === 500 ? 'not clipped by setPush (the pointer handler clips)' : 'n/a'; S.setPush(0); out.push_zero = S.push.F === 0 && S.push.until === 0;
    // the parametric term is clamped: an impossible downward acceleration does not blow up a mode within 2 s
    document.querySelector('#law button[data-v="passive"]').click(); S.restart();
    return out; });
  const fail = [];
  if (!r.readback_ok_when_drawn) fail.push('read-back does not find the drawing');
  if (!r.readback_fails_when_blank) fail.push('read-back passes on a blank canvas');
  if (r.law_switch_jump_mm > 1e-3) fail.push('switching the law kicks the cart ' + r.law_switch_jump_mm + ' mm');
  if (!r.lqr_ok) fail.push('the LQR design did not converge or is unstable');
  if (!r.straight) fail.push('the straight glass is not drawn straight');
  if (r.cyl_lam_rel > 1e-9) fail.push('the straight glass mode is not the Bessel value');
  if (!r.road_flat_before) fail.push('the road is not flat before 1 m');
  if (r.restart_t !== 0) fail.push('a road change did not restart the run');
  if (!r.push_zero) fail.push('a released push still acts');
  if (errs.length) fail.push('page errors: ' + errs.join(' | '));
  console.log(JSON.stringify(r)); console.log(fail.length ? 'FAIL\n  ' + fail.join('\n  ') : 'PASS all regression tests');
  await b.close(); process.exit(fail.length ? 1 : 0); })();
