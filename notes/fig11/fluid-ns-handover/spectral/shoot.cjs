// Run play.html headless, step to the requested times, screenshot each. Usage: N=256 TIMES=0.5,1,1.5 OUT=frames node shoot.cjs
const { chromium } = require('playwright'), fs = require('fs'), path = require('path');
(async () => {
  const N = process.env.N || '256', out = process.env.OUT || 'frames_' + N, times = (process.env.TIMES || '0.5,1,1.5,2,2.5,3').split(',').map(Number);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 900, height: 520 }, deviceScaleFactor: 2 }); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('file://' + path.resolve(__dirname, 'play_bundle.html') + '?N=' + N + '&U=' + (process.env.U || 1.5) + '&nu=' + (process.env.NU || 1.5e-5) + '&rho=' + (process.env.RHO || 1.18) + '&eta=' + (process.env.ETA || 1e-6) + '&cfl=' + (process.env.CFL || 0.6) + (process.env.INRHS ? '&inrhs=1' : '') + '&' + (process.env.QX || '')); await pg.waitForTimeout(500);
  const t0 = Date.now(), log = [];
  for (const T of times) { const r = await pg.evaluate((T) => stepTo(T), T); await pg.screenshot({ path: `${out}/t${T.toFixed(2)}.png` });
    log.push(r); console.log(`t=${T} F(cart,rod1,rod2 per unit rho,depth)=${JSON.stringify(r.F.map(f => f.map(v => +v.toFixed(4))))} ${((Date.now() - t0) / 1000).toFixed(0)} s`); }
  fs.writeFileSync(`${out}/forces.json`, JSON.stringify(log)); console.log('errors:', errs.join('|') || 'none'); await b.close();
})();
