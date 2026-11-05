// node notes/fig12/shot.cjs <outdir> [width] [actions]: open Fig. 12, run, screenshot; print errors and store numbers
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2], W = +(process.argv[3] || 1440), act = process.argv[4] || '';
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const ctx = await b.newContext({ viewport: { width: W, height: W < 600 ? 844 : 900 }, deviceScaleFactor: 1 });
  const pg = await ctx.newPage(); const errs = [];
  pg.on('pageerror', e => errs.push('pageerror: ' + e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await pg.goto('http://localhost:8765/simulations/beer-slosh.html', { waitUntil: 'networkidle' });
  await pg.waitForTimeout(800);
  if (act.includes('f1')) await pg.click('#shF1');
  if (act.includes('f2')) await pg.click('#shF2');
  await pg.waitForTimeout(+(process.env.WAIT || 4000));
  const info = await pg.evaluate(() => { const d = window.SLOSH && window.SLOSH.ds; if (!d) return 'no SLOSH'; const g = n => d.get(n);
    return { t: g('t'), f11: document.getElementById('r-f1').textContent, z1: document.getElementById('r-z1').textContent, tau: document.getElementById('r-tau').textContent, eta_mm: g('eta_w') * 1000, umax: g('u_max'), state: document.getElementById('state').textContent, webgl: !!window.SLOSH3D, katexErr: document.querySelectorAll('.katex-error').length, sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }; });
  console.log(JSON.stringify(info)); console.log(errs.slice(0, 8).join('\n') || 'no errors');
  await pg.screenshot({ path: `${out}/slosh-${W}${act ? '-' + act : ''}.png` });
  for (const id of ['stage3d', 'stage', 'stage-tr']) { const e = await pg.$('#' + id); await e.scrollIntoViewIfNeeded(); await e.screenshot({ path: `${out}/el-${id}-${W}.png` }); }
  await b.close();
})();
