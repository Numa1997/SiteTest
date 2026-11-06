// Still cart alone in a breeze, solved NS (inRhs scheme). Records the force every 0.02 s, averages the last 2 s,
// screenshots at 1..4 s, and dumps the final vorticity and velocity (every cell) for the page overlay.
const { chromium } = require('playwright'), fs = require('fs'), path = require('path');
const MED = { glycerol: { rho: 1261, mu: 1.412 }, honey: { rho: 1420, mu: 7 } };
(async () => {
  const med = process.env.MED, U = +process.env.U, N = +(process.env.N || 256), T = +(process.env.T || 4), m = MED[med], nu = m.mu / m.rho;
  const out = `cf2_${med}_${U}`; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 900, height: 520 }, deviceScaleFactor: 2 }); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('file://' + path.resolve(__dirname, 'play_bundle.html') + `?N=${N}&U=${U}&nu=${nu}&rho=${m.rho}&inrhs=1&eta=2e-4&bodies=cart&still=1&yc=0.8&kick=0.5&wmax=${Math.max(20, 40 * U)}`); await pg.waitForTimeout(300);
  const hist = [];
  for (let t = 0.02; t <= T + 1e-9; t += 0.02) { const r = await pg.evaluate((t) => { stepTo(t); return [ns.t, ns.bodies[0].F[0], ns.bodies[0].F[1]]; }, t); hist.push(r);
    if (Math.abs(t - Math.round(t)) < 1e-6) await pg.screenshot({ path: `${out}/t${Math.round(t)}.png` }); }
  const field = await pg.evaluate(() => { ns.velocity(ns.wr, ns.wi); return { N: ns.N, M: ns.M, Lx: ns.Lx, Ly: ns.Ly, X0: 1.1, YC: 0.8, CH: 0.12, u: Array.from(ns.u, v => +v.toFixed(4)), v: Array.from(ns.v, v => +v.toFixed(4)), w: Array.from(ns.w, v => +v.toFixed(3)), chi: Array.from(ns.bodies[0].chi, v => +v.toFixed(3)) }; });
  fs.writeFileSync(`${out}/field.json`, JSON.stringify(field)); fs.writeFileSync(`${out}/hist.json`, JSON.stringify(hist));
  const last = hist.filter(h => h[0] > T - 2), mean = (k) => last.reduce((s, h) => s + h[k], 0) / last.length, sd = (k) => Math.sqrt(last.reduce((s, h) => s + (h[k] - mean(k)) ** 2, 0) / last.length);
  const k = m.rho * 0.2;   // per unit density and depth -> N for the 0.2 m deep cart
  console.log(JSON.stringify({ med, U, nu, Re_h: U * 0.12 / nu, drag_N: +(mean(1) * k).toFixed(2), drag_sd_N: +(sd(1) * k).toFixed(2), lift_N: +(mean(2) * k).toFixed(2), lift_sd_N: +(sd(2) * k).toFixed(2), CD_2D: +(mean(1) * 2 / (U * U * 0.12)).toFixed(3), errors: errs.join('|') || 'none' }));
  await b.close();
})();
