// Regression tests for the round-1 code review of Fig. 12. node notes/fig12/regress.cjs
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const pg = await b.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8765/simulations/beer-slosh.html'); await pg.waitForTimeout(1500);
  const r = await pg.evaluate(async () => { const S = window.SLOSH, D = Sim.data, out = {};
    document.getElementById('play').click();                                   // pause: we drive the clock by hand
    // 1 read-backs fail on a cleared canvas
    const sec = document.getElementById('sec'), tr = document.getElementById('tr');
    sec.getContext('2d').clearRect(0, 0, 1e4, 1e4); tr.getContext('2d').clearRect(0, 0, 1e4, 1e4);
    out.readback_fails_when_blank = D.drawn.eta_w().ok === false && D.drawn.z_s().ok === false;
    // 2 stopping the shaker: no jump in the glass's position
    document.getElementById('shF1').click(); for (let i = 0; i < 777; i++) S.step();
    const before = S.ds.get('xg'); const off = S.shakerOffset().x + S.G.x;
    document.getElementById('shOff').click(); const after = S.shakerOffset().x + S.G.x;
    out.shaker_stop_jump_mm = Math.abs(after - off) * 1000;
    // 3 the cut turns the short way: rocking along 88° then 92°
    const k = S.M.findIndex(m => m.m === 1 && m.n === 1), NK = S.M.length, set = deg => { const a = deg * Math.PI / 180; S.aO.fill(0); S.vO.fill(0); S.aO[k] = 0.003 * Math.cos(a); S.aO[NK + k] = 0.003 * Math.sin(a); };
    document.querySelector('#plane button[data-v="follow"]').click();
    set(88); for (let i = 0; i < 200; i++) window.dispatchEvent(new Event('noop')); 
    return out; });
  // drive frames for the cut test through real animation frames
  await pg.evaluate(() => document.getElementById('play').click()); await pg.waitForTimeout(100);
  const turn = await pg.evaluate(async () => { const S = window.SLOSH, k = S.M.findIndex(m => m.m === 1 && m.n === 1), NK = S.M.length;
    const hold = deg => { const a = deg * Math.PI / 180; S.aO.fill(0); S.vO.fill(0); S.aO[k] = 0.003 * Math.cos(a); S.aO[NK + k] = 0.003 * Math.sin(a); };
    const frames = (n, deg) => new Promise(res => { let i = 0; (function f() { hold(deg); if (++i < n) requestAnimationFrame(f); else res(); })(); });
    await frames(120, 88); const a1 = S.thP * 180 / Math.PI; const seen = [];
    await new Promise(res => { let i = 0; (function f() { hold(92); seen.push(S.thP * 180 / Math.PI); if (++i < 120) requestAnimationFrame(f); else res(); })(); });
    return { start: a1, min_seen: Math.min(...seen.map(x => ((x % 180) + 180) % 180)), end: seen[seen.length - 1] }; });
  // 4 straight glass: the cut's wall is vertical
  const straight = await pg.evaluate(async () => { document.querySelector('#shape button[data-v="cyl"]').click(); await new Promise(r => setTimeout(r, 300));
    const S = window.SLOSH; return Math.abs(S.Rdraw(0.05) - S.Rdraw(0.13)) < 1e-12 && Math.abs(S.Rdraw(0.05) - S.geo.a) < 1e-12; });
  console.log(JSON.stringify(Object.assign(r, { cut_turn: turn, straight_draws_cylinder: straight, errors: errs.length })));
  await b.close(); })();
