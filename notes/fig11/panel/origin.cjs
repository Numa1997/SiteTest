// a. Origin: where every stored number is written, and proof that the drawing, Sim.live and the panel only read.
'use strict';
const fs = require('fs'), path = require('path'); const { chromium } = require('playwright');
const ROOT = process.env.ROOT || require('path').resolve(__dirname, '../../..'), FILE = ROOT + '/public/simulations/double-inverted-pendulum.html';
const src = fs.readFileSync(FILE, 'utf8').split('\n');
const s0 = src.findIndex((l) => l.trim() === '<script>' ), body = src.slice(s0);
// every write into the store and the function that holds it: a scan of the script that counts braces outside strings and comments
const W = {}; (() => { const st = []; let depth = 0, pend = null;
  const WR = /^(?:ds\.set\('(\w+)'|ds\.get\('(\w+)'\)\.set\(|ds\.touch\('(\w+)'\)|LG\.(\w+)\[[^\]]+\] = )/;
  body.forEach((l) => { let i = 0;
    while (i < l.length) { const rest = l.slice(i), m = rest.match(/^(?:function\*?\s+(\w+)\s*\(|(Sim\.\w+|window\.\w+|\w+)\s*=\s*function\s*\(|Sim\.(clock)\(function)/);
      if (m) { pend = m[1] || m[2] || m[3]; i += m[0].length; continue; }
      const w = rest.match(WR); if (w) { const v = w[1] || w[2] || w[3] || w[4], f = st.length ? st[st.length - 1].name : '(top level)'; (W[f] = W[f] || new Set()).add(v); i += w[0].length; continue; }
      const c = l[i]; if (c === '/' && l[i + 1] === '/') break;
      if (c === "'" || c === '"' || c === '`') { i++; while (i < l.length && l[i] !== c) { if (l[i] === '\\') i++; i++; } i++; continue; }
      if (c === '{') { depth++; if (pend) { st.push({ name: pend, depth }); pend = null; } } else if (c === '}') { if (st.length && st[st.length - 1].depth === depth) st.pop(); depth--; }
      i++; } }); })();
console.log('a1 writes into the store, by the function that holds the line (static, from the page source):');
for (const f of Object.keys(W)) console.log(`   ${f.padEnd(12)} ${[...W[f]].join(', ')}`);
// 2. the display code: what it may not do
function bodyOf(startRe) { const i = body.findIndex((l) => startRe.test(l)); let depth = 0, out = []; for (let k = i; k < body.length; k++) { out.push(body[k]); for (const ch of body[k]) { if (ch === '{') depth++; if (ch === '}') depth--; } if (depth <= 0 && k > i) break; } return { at: i + s0 + 1, text: out.join('\n') }; }
const BAD = [/\brhs\(/, /\brk4\(/, /\benergy\(/, /\bWof\(/, /\bWred\(/, /\brefXV\(/, /\bfallRates\(/, /\bspecRad\(/, /\bdlqr\(/, /\blqr\(/, /\bEp\(/, /\bs\[/, /\btSim\b/, /\bp\.(L1|L2|m1|m2|d|f)\b/, /\bref\.\w/, /\bxref\b/, /\bsF\.value/, /\bcLevel\b/, /\bK\[/, /\bPm\b/, /\bSmod\b/];
const parts = [['draw()', /^\s{8}function draw\(\)/], ['drawTrace()', /^\s{8}function drawTrace\(\)/], ['Sim.live', /^\s{8}Sim\.live = function/], ['clock: words', /^\s{8}var clk = Sim\.clock/]];
let clean = true; console.log('a2 the display code reads only the store (no physics call, no read of the page’s own state):');
for (const [name, re] of parts) { const b = bodyOf(re), hits = []; BAD.forEach((r) => { const m = b.text.match(r); if (m) hits.push(m[0]); });
  let txt = b.text; if (name === 'clock: words') txt = txt.replace(/step\(dt\); think\(8\); diagnostics\(dt\); draw\(\);/, '');   // the clock first runs the simulation, then the display
  const hits2 = []; BAD.forEach((r) => { const m = txt.match(r); if (m) hits2.push(m[0]); });
  console.log(`   ${name.padEnd(13)} line ${b.at}: ${hits2.length ? 'READS PAGE STATE: ' + hits2.join(' ') : 'store only'}`); if (hits2.length) clean = false; }
const writesInDisplay = (W['drawTrace'] ? [...W['drawTrace']] : []).concat(W['live'] ? [...W['live']] : []);
console.log(`   draw() writes only the drawing section: ${[...(W['draw'] || [])].join(', ')}; drawTrace and Sim.live write ${writesInDisplay.length ? writesInDisplay.join(', ') : 'nothing'}`);
const dl = fs.readFileSync(ROOT + '/public/scripts/datalog.js', 'utf8'), dlw = (dl.match(/ds\.(set|touch|alloc|var|dim|coord)\(/g) || []);
console.log(`   datalog.js calls on the store that write: ${dlw.length ? dlw.join(' ') : 'none'} (it reads with ds.get, ds.vars, ds.along, ds.npz)`);
(async () => { const b = await chromium.launch(), pg = await b.newPage({ viewport: { width: 1600, height: 900 } }); const errs = []; pg.on('pageerror', (e) => errs.push(e.message));
  // 3. at run time: every ds.set and ds.touch, with the function that called it, while the panel is open and live
  await pg.addInitScript(() => { window.__writers = {}; let S0;   // trap the moment dataset.js defines Sim.dataset, and wrap the store it makes
    Object.defineProperty(window, 'Sim', { configurable: true, get() { return S0; }, set(v) { S0 = v; let D0; Object.defineProperty(v, 'dataset', { configurable: true, get() { return D0; }, set(f) { D0 = wrap(f); } }); } });
    function wrap(D) { return function (m) { const ds = D(m), set = ds.set.bind(ds), touch = ds.touch.bind(ds);
      const who = () => { const fr = new Error().stack.split('\n').slice(3); for (const l of fr) { const m = l.match(/at ([\w.$]+) \(/); if (m && !/^Array\./.test(m[1])) return m[1] + (l.includes('datalog.js') ? ' [datalog.js]' : ''); } return '(page script, top level)'; };
      ds.set = function (n, v) { const w = who(); (window.__writers[n] = window.__writers[n] || {})[w] = 1; return set(n, v); };
      ds.touch = function (n) { const w = who(); (window.__writers[n] = window.__writers[n] || {})[w] = 1; return touch(n); }; return ds; }; } });
  await pg.goto('file://' + FILE); await pg.waitForTimeout(2000);
  await pg.evaluate(() => { if (!document.body.classList.contains('dp-open')) document.querySelector('.dp-tab').click(); }); await pg.waitForTimeout(1500);
  await pg.click('#flickR'); await pg.waitForTimeout(1500); await pg.evaluate(() => DIPC.swingUp()); await pg.waitForTimeout(3000);
  const w = await pg.evaluate(() => window.__writers), byF = {};
  for (const n in w) for (const f in w[n]) (byF[f] = byF[f] || []).push(n);
  console.log('a3 writers seen at run time (panel open and live, a flick, the start of a swing-up), function → variables:');
  for (const f in byF) console.log(`   ${f.padEnd(28)} ${byF[f].length} variables: ${byF[f].slice(0, 14).join(', ')}${byF[f].length > 14 ? ', …' : ''}`);
  const bad = Object.keys(byF).filter((f) => /datalog|live|inspect|probe|check|drawn/.test(f));
  console.log(`   writes from the panel, Sim.live or the panel hooks: ${bad.length ? bad.join(', ') : 'none'}`);
  // 4. edit the store, redraw: the picture follows the store, not the page's state; Sim.live too
  await pg.evaluate(() => { document.getElementById('play').click(); }); await pg.waitForTimeout(300);
  await pg.evaluate(() => { document.querySelector('.dp__close').click(); }); await pg.waitForTimeout(200);
  const r = await pg.evaluate(() => { const ds = DIPC.ds, S = ds.get('s_now'), cv = document.getElementById('cv'), c = cv.getContext('2d'), dpr = cv.width / cv.getBoundingClientRect().width;
    const white = (x, y) => { let sx = 0, sy = 0, n = 0; for (let j = Math.round((y - 7) * dpr); j <= Math.round((y + 7) * dpr); j++) for (let i = Math.round((x - 7) * dpr); i <= Math.round((x + 7) * dpr); i++) { const p = c.getImageData(i, j, 1, 1).data; if (p[3] === 255 && p[0] === 255 && p[1] === 255 && p[2] === 255) { sx += i + .5; sy += j + .5; n++; } } return n ? [sx / n / dpr, sy / n / dpr, n] : null; };
    const pageS = DIPC.s.slice(), before = [ds.get('mid_px'), ds.get('mid_py')], liveBefore = Sim.live().t1;
    S[1] += 0.3; DIPC.draw(); const after = [ds.get('mid_px'), ds.get('mid_py')], seenAfter = white(after[0], after[1]), seenBefore = white(before[0], before[1]), liveAfter = Sim.live().t1;
    S[1] -= 0.3; DIPC.draw();
    return { pageTh1: pageS[1], storeTh1: S[1], before, after, seenAfter, seenBefore, liveBefore, liveAfter, pageUnchanged: DIPC.s[1] === pageS[1] }; });
  console.log(`a4 store edit: θ₁ in the store raised by 0.3 rad (the page’s own state left at ${r.pageTh1.toFixed(4)} rad), then draw():`);
  console.log(`   hinge between the rods stored at (${r.before.map((v) => v.toFixed(2))}) → (${r.after.map((v) => v.toFixed(2))}); white disc found at the new place: ${r.seenAfter ? '(' + r.seenAfter.slice(0, 2).map((v) => v.toFixed(2)) + '), ' + r.seenAfter[2] + ' px' : 'no'}; at the old place: ${r.seenBefore ? 'yes' : 'no'}`);
  console.log(`   Sim.live().t1 ${r.liveBefore} → ${r.liveAfter}; the page’s state unchanged: ${r.pageUnchanged}`);
  console.log(`a: ${clean && !Object.keys(byF).some((f) => /datalog/.test(f)) && r.seenAfter && !r.seenBefore && r.liveBefore !== r.liveAfter ? 'PASS' : 'FAIL'}; page errors: ${errs.join(' | ') || 'none'}`);
  await b.close(); })();
