// Gate of the suspension controller: dumps the page's LQR gains and the bump runs (passive, skyhook, LQR; 6 s, 1 ms steps, the
// page's own step()) to JSON, for tools/fig12/gate_ctl3.py to compare with the offline design and simulation.
// node notes/fig12/gate-ctl3.cjs out.json
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8765/simulations/beer-slosh.html', { waitUntil: 'networkidle' }); await pg.waitForTimeout(1500);
  const r = await pg.evaluate(() => {
    const S = window.SLOSH, ds = S.ds; document.getElementById('play').click();
    const res = { V: ds.get('V_mL'), se: S.P.se, sp: S.P.sp, sv: S.P.sv, su: S.P.su, Ts: S.P.Ts, Imax: S.P.Imax, Bl: S.P.Bl, hr: S.P.hr, v: S.P.v, n: S.Ct.n, K: [S.Ct.K[0].slice(), S.Ct.K[1].slice()], tau: ds.get('tau_cl'), iters: S.Ct.iters, runs: {} };
    for (const law of ['passive', 'skyhook', 'lqr']) {
      document.querySelector(`#law button[data-v="${law}"]`).click(); document.querySelector('#road button[data-v="bump"]').click(); S.restart();
      let peak = 0, maxU = 0, maxPsi = 0; const eta = [];
      for (let i = 0; i < 6000; i++) { S.step(); if (i % 10 === 0) { let best = -1e9; for (let q = 0; q < 72; q++) best = Math.max(best, S.etaWall(2 * Math.PI * q / 72)); peak = Math.max(peak, Math.abs(best)); maxU = Math.max(maxU, Math.abs(S.Ct.uf), Math.abs(S.Ct.ur)); maxPsi = Math.max(maxPsi, Math.abs(S.q[S.IP])); eta.push(+best.toFixed(7)); } }
      res.runs[law] = { peak, maxU, maxPsi, eta };
    }
    return res;
  });
  require('fs').writeFileSync(out, JSON.stringify(r)); console.log('wrote', out, 'errors', errs.length, errs.join(' | '));
  await b.close();
})();
