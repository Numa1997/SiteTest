// g. Cost: frame time with the data panel closed, before (main) and after (this branch); when the panel's loop runs.
'use strict';
const { chromium } = require('playwright'); const path = require('path');
const BASE = process.env.BASE, NEW = process.env.ROOT || require('path').resolve(__dirname, '../../..');
const q = (a, p) => { const b = a.slice().sort((x, y) => x - y); return b[Math.min(b.length - 1, Math.floor(p * b.length))]; };
async function measure(b, root, label) {
  const pg = await b.newPage({ viewport: { width: 1280, height: 900 } }); const errs = []; pg.on('pageerror', (e) => errs.push(e.message));
  // every animation-frame callback timed; one frame's cost is the sum of the callbacks that ran in it
  await pg.addInitScript(() => { window.__ft = []; const raf = window.requestAnimationFrame.bind(window); let cur = null, curT = -1;
    window.requestAnimationFrame = (cb) => raf((ts) => { const t0 = performance.now(); cb(ts); const d = performance.now() - t0; if (ts !== curT) { if (cur !== null) window.__ft.push(cur); cur = 0; curT = ts; } cur += d; }); });
  await pg.goto('file://' + path.resolve(root + '/public/simulations/double-inverted-pendulum.html'));
  await pg.evaluate(() => { try { localStorage.setItem('datapanel.open', '0'); } catch (e) {} });
  await pg.waitForTimeout(4000); await pg.evaluate(() => { window.__ft = []; }); await pg.waitForTimeout(15000);
  const ft = await pg.evaluate(() => window.__ft), info = await pg.evaluate(() => ({ panel: !!window.__dataPanel, running: window.__dataPanel ? window.__dataPanel.running() : null, open: document.body.classList.contains('dp-open'), mode: DIPC.mode }));
  // the physics alone: 60 simulated seconds driven frame by frame, as t9.cjs does (step + think), at rest
  const drive = await pg.evaluate(() => { const t0 = performance.now(); for (let i = 0; i < 3600; i++) { DIPC.step(1 / 60); DIPC.think(8); } return (performance.now() - t0) / 3600; });
  const mean = ft.reduce((a, v) => a + v, 0) / ft.length;
  console.log(`${label}: ${ft.length} frames in 15 s, script time per frame mean ${mean.toFixed(3)} ms, median ${q(ft, 0.5).toFixed(3)}, p95 ${q(ft, 0.95).toFixed(3)}, max ${Math.max(...ft).toFixed(3)} ms; ` +
    `step+think per frame (driven) ${drive.toFixed(3)} ms; panel ${info.panel ? 'present' : 'absent'}, open ${info.open}, loop running ${info.running}; errors ${errs.join(' | ') || 'none'}`);
  return pg;
}
(async () => { const b = await chromium.launch();
  if (!process.env.SKIP) for (let rep = 0; rep < 2; rep++) { if (BASE) await (await measure(b, BASE, `before (main), run ${rep + 1}`)).close(); await (await measure(b, NEW, `after (branch), run ${rep + 1}`)).close(); }
  // when does the panel's loop run? (buttons pressed by script: below about 1500 px the open panel lies over the page, as on every figure)
  const pg = await b.newPage({ viewport: { width: 1280, height: 900 } }); await pg.goto('file://' + path.resolve(NEW + '/public/simulations/double-inverted-pendulum.html')); await pg.waitForTimeout(2500);
  const press = (sel) => pg.evaluate((s) => document.querySelector(s).click(), sel);
  const st = async (what) => { await pg.waitForTimeout(400); const r = await pg.evaluate(() => ({ run: window.__dataPanel.running(), open: document.body.classList.contains('dp-open'), playing: DIPC.ds.get('playing') })); console.log(`  panel loop running ${String(r.run).padEnd(5)} · ${what} (panel ${r.open ? 'open' : 'closed'}, clock ${r.playing ? 'playing' : 'paused'})`); };
  await pg.evaluate(() => { if (document.body.classList.contains('dp-open')) document.querySelector('.dp__close').click(); }); await pg.waitForTimeout(2000); await st('closed');
  await press('.dp-tab'); await st('open, Live on, playing');
  await press('#play'); await pg.waitForTimeout(1800); await st('open, Live on, paused, 1.8 s after the last action');
  await press('#play'); await press('.dp__close'); await pg.waitForTimeout(1800); await st('closed again, playing');
  await press('.dp-tab'); const recSel = await pg.evaluate(() => { const bt = [...document.querySelectorAll('#data-panel button')].find((x) => /Record/.test(x.textContent)); if (bt) { bt.setAttribute('data-t', 'rec'); return '[data-t=rec]'; } return null; });
  await press(recSel); await press('.dp__close'); await st('panel closed while a round records');
  const done = await pg.evaluate(() => new Promise((res) => { const t0 = performance.now(); const w = () => { if (!window.__dataPanel.recording() || performance.now() - t0 > 15000) res(window.__dataPanel.rounds().length); else setTimeout(w, 200); }; w(); }));
  console.log(`  rounds recorded: ${done}`); await pg.waitForTimeout(1800); await st('after the round (the finished round opens the panel to show its charts)');
  // pointer rules: a sweep across the running figure changes nothing, with Read values off and on; a click with Read on pins and does not grab a rod
  const box = await (await pg.$('#cv')).boundingBox();
  const sweep = async (label) => { let maxOverlay = 0, held = 0; for (let k = 0; k <= 40; k++) { await pg.mouse.move(box.x + box.width * k / 40, box.y + box.height * (0.2 + 0.6 * k / 40)); await pg.waitForTimeout(20);
      const r = await pg.evaluate(() => { const o = document.querySelector('.dp-overlay'); let n = 0; if (o && o.width) { const d = o.getContext('2d').getImageData(0, 0, o.width, o.height).data; for (let i = 3; i < d.length; i += 4) if (d[i]) n++; } return { n, held: DIPC.held, strip: (document.querySelector('.dp-read') || {}).textContent || '' }; });
      maxOverlay = Math.max(maxOverlay, r.n); held = Math.max(held, r.held); }
    console.log(`  sweep across the running figure, ${label}: overlay pixels painted at most ${maxOverlay}, rod grabbed ${held ? 'YES' : 'no'}`); };
  await sweep('Read values off');
  await press('.dp-readbtn'); await st('Read values on, nothing pinned'); await sweep('Read values on, nothing pinned');
  const tip = await pg.evaluate(() => ({ x: DIPC.ds.get('tip_px'), y: DIPC.ds.get('tip_py') })); await pg.mouse.move(box.x + tip.x, box.y + tip.y); await pg.mouse.down(); await pg.waitForTimeout(150);
  const heldOnPin = await pg.evaluate(() => DIPC.held); await pg.mouse.up(); await st('Read values on, the top of the upper rod pinned');
  const rate = await pg.evaluate(() => new Promise((res) => { const el = document.querySelector('.dp-read'); let last = el.textContent, n = 0, frames = 0; const t0 = performance.now();
    const f = () => { frames++; if (el.textContent !== last) { n++; last = el.textContent; } if (performance.now() - t0 < 3000) requestAnimationFrame(f); else res({ n, frames, text: last.slice(0, 120) }); }; requestAnimationFrame(f); }));
  console.log(`  pin: a press on the upper rod with Read values on grabbed ${heldOnPin ? 'the rod (WRONG)' : 'nothing'}; the strip under the figure changed ${rate.n} times in 3 s over ${rate.frames} frames: “${rate.text}”`);
  const marker = await pg.evaluate(() => { const o = document.querySelector('.dp-overlay'); const d = o.getContext('2d').getImageData(0, 0, o.width, o.height).data; let n = 0; for (let i = 3; i < d.length; i += 4) if (d[i]) n++; return n; });
  console.log(`  the pin's marker: ${marker} overlay pixels painted (drawn every frame on the overlay, not on the figure)`);
  await press('.dp-readbtn'); await pg.waitForTimeout(1800); await st('Read values off again');
  await press('.dp__close'); await pg.waitForTimeout(1800); await st('panel closed at the end');
  await b.close(); })();
