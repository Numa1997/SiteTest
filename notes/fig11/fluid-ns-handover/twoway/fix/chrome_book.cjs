// The English page in Chromium: KaTeX errors, page errors, and the solved fluid's water book while it runs (glycerol, still, then a flick).
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const br = await chromium.launch(); const pg = await br.newPage({ viewport: { width: 1100, height: 900 } }); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  const lang = process.env.LANG2 || ''; await pg.goto('file://' + path.resolve(__dirname, '../../../../../public/' + lang + 'simulations/double-inverted-pendulum.html')); await pg.waitForTimeout(2500);
  await pg.evaluate(() => { const M = document.getElementById('med'); M.value = 'glycerol'; M.dispatchEvent(new Event('change')); const C = document.getElementById('cpl'); C.disabled = false; C.value = 'solved'; C.dispatchEvent(new Event('change')); });
  await pg.waitForTimeout(4000); await pg.evaluate(() => DIPC.flick && DIPC.flick(1)); await pg.waitForTimeout(3000);
  const r = await pg.evaluate(() => { const g = (n) => DIPC.ds.get(n); const rows = ['tw_Wm', 'tw_Eb', 'tw_Drod', 'tw_Dvis', 'tw_Lp', 'tw_La', 'tw_Li', 'tw_Ll', 'tw_Lt', 'tw_Eg', 'tw_dEK', 'tw_rr', 'tw_res', 'tw_div', 'tw_ms', 'tw_slow']; const o = {}; rows.forEach(n => o[n] = +(+g(n)).toPrecision(4)); const h = Sim.data.check.tw_res(); o.hook_res = +h.value.toPrecision(6); o.stored_res = +(+g('tw_res')).toPrecision(6); o.katexErr = document.querySelectorAll('.katex-error').length; o.pending = document.querySelectorAll('.i18n-pending').length; o.overflow = document.documentElement.scrollWidth > document.documentElement.clientWidth; o.t = DIPC.t; return o; });
  console.log(JSON.stringify(r)); console.log('page errors', errs.length, errs.slice(0, 3)); await br.close(); })();
