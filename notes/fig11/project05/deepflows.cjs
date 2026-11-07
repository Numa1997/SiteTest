// The deep and slow flows (13.3): page velocities against the stream functions of ref.cjs (numerical derivatives), and their divergence, on a grid over the rig and 300 s.
const { chromium } = require('playwright'); const R = require('../panel/ref.cjs');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1200);
  for (const k of ['internal', 'gyre', 'deepsea', 'tides']) {
    const pts = []; for (let X = -3; X <= 3; X += 0.5) for (let Y = -1.5; Y <= 1.5; Y += 0.5) for (const t of [0, 7.3, 61, 299]) pts.push([X, Y, t]);
    const pv = await pg.evaluate(([k, pts]) => pts.map(([X, Y, t]) => { const v = DIPC.fieldV(k, X, Y, t, 1, 1e-6), h = 1e-4, a = DIPC.fieldV(k, X + h, Y, t, 1, 1e-6), c = DIPC.fieldV(k, X - h, Y, t, 1, 1e-6), d = DIPC.fieldV(k, X, Y + h, t, 1, 1e-6), e = DIPC.fieldV(k, X, Y - h, t, 1, 1e-6); return [v[0], v[1], (a[0] - c[0] + d[1] - e[1]) / (2 * h)]; }), [k, pts]);
    let dmax = 0, div = 0, vmax = 0; pts.forEach(([X, Y, t], i) => { const r = R.flow(k, X, Y, t, 1, 1e-6); dmax = Math.max(dmax, Math.hypot(r[0] - pv[i][0], r[1] - pv[i][1])); div = Math.max(div, Math.abs(pv[i][2])); vmax = Math.max(vmax, Math.hypot(pv[i][0], pv[i][1])); });
    console.log(k.padEnd(9), 'points', pts.length, 'max |page − ref| (U = 1 m/s)', dmax.toExponential(1), 'm/s; max |div v|', div.toExponential(1), '1/s; max speed', vmax.toFixed(2), 'm/s'); }
  await b.close();
})();
