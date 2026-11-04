const { chromium } = require('playwright'); const path = require('path');
const url = 'file://' + path.resolve('/home/user/SiteTest/public/simulations/double-inverted-pendulum.html');
const scen = process.argv[2] || 'random';
(async () => { const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1280, height: 900 } });
 const errs = []; pg.on('pageerror', e => errs.push(e.message));
 await pg.goto(url); await pg.waitForTimeout(1500);
 await pg.evaluate(() => { const b = document.getElementById('play'); if (b.textContent.trim() === 'Pause') b.click(); });
 const runFor = (sec) => pg.evaluate((sec) => { const n = Math.round(sec * 60); let um = 0, xm = 0, tc = null; const L0 = DIPC.log.length;
   for (let i = 0; i < n; i++) { DIPC.step(1 / 60); DIPC.think(8); um = Math.max(um, Math.abs(DIPC.u)); xm = Math.max(xm, Math.abs(DIPC.s[0])); }
   const s = DIPC.s, lg = DIPC.log.slice(L0), c = lg.filter(e => e.ev === 'caught').pop();
   return { mode: DIPC.mode, th: [s[1], s[2]].map(a => +(a - 2 * Math.PI * Math.round(a / (2 * Math.PI))).toFixed(3)), umax: +um.toFixed(0), xmax: +xm.toFixed(2), tcaught: c ? +c.t.toFixed(1) : null, ms: lg.filter(e => e.ms).map(e => e.ms), evs: lg.map(e => e.ev).join(',') }; }, sec);
 const set = (o) => pg.evaluate((o) => { for (const k in o) { const el = document.getElementById(k); el.value = o[k]; el.dispatchEvent(new Event('input', { bubbles: true })); } }, o);
 let seed = 99; const rnd = () => { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; };
 const configs = { cont40: [{ Ts: 40 }], random: [{}], machines: [{ Ts: 40 }, { Ts: 60 }, { m0: 3 }, { m1: 1, m2: 1.5 }, { L1: 1, L2: 1.2 }, { L1: 0.3, L2: 0.4 }, { Fmax: 30 }, { Fmax: 120 }], ts40: [{ Ts: 40 }] }[scen];
 for (const cfg of configs) { await set({ m0: 1.5, m1: 0.5, m2: 0.75, L1: 0.5, L2: 0.75, Fmax: 60, Ts: 10, rho: 0 }); await set(cfg); if (scen === 'cont40') await pg.evaluate(() => { DIPC.gmode = 'cont'; });
  const cl = await pg.evaluate(() => DIPC.finishCatch()); const N = scen === 'random' ? 40 : 6; if (process.env.STOP) await pg.evaluate(() => { DIPC.rolling = false; }); let ok = 0; const tcs = [], mss = [];
  for (let i = 0; i < N; i++) { const s0 = [(rnd() - .5), (rnd() * 2 - 1) * Math.PI, (rnd() * 2 - 1) * Math.PI, (rnd() - .5), (rnd() - .5) * 6, (rnd() - .5) * 6];
   await pg.evaluate((s0) => { DIPC.finishCatch(); document.getElementById('reset').click(); DIPC.s = s0; }, s0);
   const r = await runFor(60); const good = r.mode === 'balance' && Math.abs(r.th[0]) < 0.05 && Math.abs(r.th[1]) < 0.05; if (good) { ok++; tcs.push(r.tcaught || 0); } mss.push(...r.ms);
   if (!good || scen !== 'random') console.log(' ', i, good ? 'ok' : 'NOT', JSON.stringify({ s0: s0.map(v => +v.toFixed(2)), ...r })); }
  tcs.sort((a, b) => a - b); mss.sort((a, b) => a - b);
  console.log(JSON.stringify(cfg), `c=${cl.toFixed(0)}: ${ok}/${N} balanced; time to catch median ${tcs[tcs.length >> 1]} s, max ${tcs[tcs.length - 1]} s; successful plans took ${mss[0]}–${mss[mss.length - 1]} ms (median ${mss[mss.length >> 1]})`); }
 console.log('errors:', errs.join(' | ') || 'none'); await b.close(); })();
