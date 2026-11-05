// The page's own braking after a rolling catch (headless Chromium, frame-by-frame driver as t9.cjs): random falls, then
// how long the cart takes to come to rest, how far it rolls, the largest lean, force and W / c* while braking.
'use strict';
const { chromium } = require('playwright'); const path = require('path');
const ROOT = process.env.ROOT || path.resolve(__dirname, '../../..'), N = +(process.env.N || 12);
(async () => { const b = await chromium.launch(), pg = await b.newPage({ viewport: { width: 1280, height: 900 } }); const errs = []; pg.on('pageerror', (e) => errs.push(e.message));
  await pg.goto('file://' + ROOT + '/public/simulations/double-inverted-pendulum.html'); await pg.waitForTimeout(1500);
  await pg.evaluate(() => { const bt = document.getElementById('play'); if (bt.getAttribute('aria-pressed') === 'false') bt.click(); });
  const set = (o) => pg.evaluate((o) => { for (const k in o) { const el = document.getElementById(k); el.value = o[k]; el.dispatchEvent(new Event('input', { bubbles: true })); } }, o);
  let seed = 99; const rnd = () => { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; };
  for (const Ts of (process.env.TS || '10,40').split(',').map(Number)) { await set({ Ts }); const c = await pg.evaluate(() => DIPC.finishCatch()); let ok = 0; const rows = [];
    for (let i = 0; i < N; i++) { const s0 = [(rnd() - .5), (rnd() * 2 - 1) * Math.PI, (rnd() * 2 - 1) * Math.PI, (rnd() - .5), (rnd() - .5) * 6, (rnd() - .5) * 6];
      const r = await pg.evaluate((s0) => { DIPC.finishCatch(); document.getElementById('reset').click(); DIPC.rolling = true; DIPC.s = s0;
        let tCaught = null, vCaught = 0, xCaught = 0, tStop = null, lean = 0, umax = 0, wmax = 0;
        for (let f = 0; f < 60 * 60; f++) { DIPC.step(1 / 60); DIPC.think(8);
          const st = DIPC.s, ref = DIPC.ref;
          if (tCaught === null && ref.brake) { tCaught = DIPC.t; vCaught = ref.v; xCaught = st[0]; }
          if (tCaught !== null && tStop === null) { const w = (a) => Math.abs(a - 2 * Math.PI * Math.round(a / (2 * Math.PI))); lean = Math.max(lean, w(st[1]), w(st[2])); umax = Math.max(umax, Math.abs(DIPC.u)); wmax = Math.max(wmax, DIPC.W() / DIPC.cLevel);
            if (ref.kind === 'fixed') tStop = DIPC.t; } }
        const st = DIPC.s, w = (a) => Math.abs(a - 2 * Math.PI * Math.round(a / (2 * Math.PI)));
        return { mode: DIPC.mode, end: [w(st[1]), w(st[2]), st[3]].map((v) => +v.toFixed(4)), tCaught, vCaught, tStop, roll: tStop !== null ? st[0] - xCaught : null, lean: lean * 180 / Math.PI, umax, wmax }; }, s0);
      const good = r.mode === 'balance' && r.end[0] < 0.05 && r.end[1] < 0.05 && Math.abs(r.end[2]) < 0.01; if (good) ok++;
      rows.push(`  ${i} ${good ? 'ok ' : 'NOT'} caught at ${r.tCaught === null ? '–' : r.tCaught.toFixed(1)} s moving ${r.vCaught.toFixed(2)} m/s; at rest after ${r.tStop === null ? 'never' : (r.tStop - r.tCaught).toFixed(2) + ' s'}, rolled ${r.roll === null ? '–' : r.roll.toFixed(2)} m; while braking lean ≤ ${r.lean.toFixed(2)}°, |u| ≤ ${r.umax.toFixed(1)} N, W ≤ ${r.wmax.toFixed(2)} c*; end speed ${r.end[2]} m/s`); }
    console.log(`Ts ${Ts} ms, c* = ${c.toFixed(1)}: ${ok}/${N} balanced and at rest after 60 s`); rows.forEach((l) => console.log(l)); }
  console.log('page errors:', errs.join(' | ') || 'none'); await b.close(); })();
