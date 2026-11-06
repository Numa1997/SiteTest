// Gate of the one-wheel cart's controller: dumps the page's LQR gains (strut and drive motor) and the road runs (passive, skyhook, LQR
// over the bump, the kerb and the cobbles; 6 s, 1 ms steps, the page's own step()) to JSON, for tools/fig12/gate_ctl3.py to compare
// with the offline design and simulation.
// node notes/fig12/gate-ctl3.cjs out.json
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch();
  const pg = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8765/simulations/beer-slosh.html', { waitUntil: 'networkidle' }); await pg.waitForTimeout(1500);
  const r = await pg.evaluate(() => {
    const S = window.SLOSH, ds = S.ds; document.getElementById('play').click();
    const res = { V: ds.get('V_mL'), se: S.P.se, sw: S.P.sw, sv: S.P.sv, su: S.P.su, sm: S.P.sm, Ts: S.P.Ts, Imax: S.P.Imax, Bl: S.P.Bl, v: S.P.v, csky: S.P.csky, n: S.Ct.n, K: [S.Ct.K[0].slice(), S.Ct.K[1].slice()], tau: ds.get('tau_cl'), iters: S.Ct.iters, runs: {} };
    for (const [road, hr] of [['bump', 0.03], ['kerb', 0.02], ['cobbles', 0.006]]) for (const law of ['passive', 'skyhook', 'lqr']) {
      document.querySelector(`#law button[data-v="${law}"]`).click(); document.querySelector(`#road button[data-v="${road}"]`).click();
      const hs = document.getElementById('hr'); hs.value = hr * 1000; hs.dispatchEvent(new Event('input')); S.buildRoad(); S.restart();
      let peak = 0, maxUs = 0, maxUm = 0, maxKick = 0, Nmin = 1e9; const eta = [];
      for (let i = 0; i < 6000; i++) { S.step(); if (i % 10 === 0) { let best = -1e9; for (let q = 0; q < 72; q++) best = Math.max(best, S.etaWall(2 * Math.PI * q / 72)); peak = Math.max(peak, Math.abs(best)); maxUs = Math.max(maxUs, Math.abs(S.Ct.us)); maxUm = Math.max(maxUm, Math.abs(S.Ct.um)); maxKick = Math.max(maxKick, Math.abs(S.road.kick)); Nmin = Math.min(Nmin, S.road.N); eta.push(+best.toFixed(7)); } }
      res.runs[road + ':' + law] = { peak, maxUs, maxUm, maxKick, Nmin, eta };
    }
    return res;
  });
  require('fs').writeFileSync(out, JSON.stringify(r)); console.log('wrote', out, 'errors', errs.length, errs.join(' | '));
  await b.close();
})();
