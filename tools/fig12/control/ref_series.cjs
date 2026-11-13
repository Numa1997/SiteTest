// Reference rides of the site's own reduced model (stout-cart.js, World with the linear live model ModalFluid), for Gate B1:
// the JAX port (tools/fig12/control/plant_jax.py) must reproduce these states step by step.
//   node tools/fig12/control/ref_series.cjs [bump mm] [T s] > tools/fig12/control/ref_series.json
// Setup = tools/fig12/study.cjs with MODAL=1: one cosine bump every 2 m from x = 1 m, 25 cm long, the cart from x = 0.5 m at
// 1 m/s, fluid steps of 5 ms, cart steps of 0.1 ms, controller every 1 ms. One row per fluid step: t, x, vx, zb, vzb, zw,
// vzw, i, icmd, us, q1..q3, qd1..qd3, the filter's estimate (v, q, q'), the probes' y_q, a_x, a_z, lean (front - back, m).
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { World } = load('stout-cart.js'), G = load('guinness-glass.js');
const bump = +(process.argv[2] || 10) / 1000, T = +(process.argv[3] || 2.3);
const bumps = []; for (let n = 0; n < 60; n++) bumps.push({ x: 1.0 + 2 * n, h: bump, L: 0.25 });
const out = { bump, T, dtFluid: 0.005, hCart: 1e-4, Ts: 0.001, cols: ['t', 'x', 'vx', 'zb', 'vzb', 'zw', 'vzw', 'i', 'icmd', 'us', 'q1', 'q2', 'q3', 'qd1', 'qd2', 'qd3', 'zh_v', 'zh_q', 'zh_qd', 'y_q', 'a_x', 'a_z', 'lean'], runs: {} };
for (const [ctrl, susp] of [['off', false], ['speed', false], ['preview', false], ['slosh', false], ['joint', false], ['preview', true]]) {
  const w = new World({
    fluid: { profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03, modal: true },
    road: { bumps, Rw: 0.04, xmin: -1, xmax: 125 },
    cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: 1, ctrl, susp },
    dtMax: 1 / 200
  });
  const f = w.fluid, c = w.cart, rows = [];
  let lmax = 0;
  const row = () => { const l = f.heightAt(f.Rs, 0) - f.heightAt(-f.Rs, 0); lmax = Math.max(lmax, Math.abs(l)); const o = c.obs.x;
    rows.push([w.t, c.x, c.vx, c.zb, c.vzb, c.zw, c.vzw, c.i, c.icmd, c.us, f.q[0], f.q[1], f.q[2], f.qd[0], f.qd[1], f.qd[2], o[0], o[1], o[2], c.probe.y, w.lastAx, w.lastAz, l]); };
  row();
  while (w.t < T - 1e-9) { w.advance(1 / 200); row(); }
  const key = ctrl + (susp ? '+skyhook' : '');
  out.runs[key] = { lean_max_mm: +(lmax * 1000).toFixed(3), plant: c.sloshMode, K: c.lqrGains(), Ks: c.suspGains(), Mx: c.massX(), ml: c.ml, rows: rows.map((r) => r.map((v) => +v.toPrecision(12))) };
  process.stderr.write(`${key}: largest lean ${(lmax * 1000).toFixed(2)} mm\n`);
}
process.stdout.write(JSON.stringify(out));
