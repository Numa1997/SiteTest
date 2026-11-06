// The cart's energy book over a bump: node tools/fig12/energy.cjs [bump mm]
// With every damper and the drag set (almost) to zero and no motor current, the cart of stout-cart.js must keep
//   E = ½ M_x ẋ² + ½ M_s ż_b² + ½ m_w ż_w² + ½ k (z_b − z_w − L_s)² + ½ k_t max(0, z_a(x) − z_w)² + M_s g z_b + m_w g z_w
// constant while the tyre touches the road: the road's push −N z_a′ and the tyre's lift N are the two derivatives of one
// potential, ½ k_t max(0, z_a(x) − z_w)² (zero when the wheel is off the road). With the page's dampers on, dE/dt must equal the power they take out.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { Cart, Road } = load('stout-cart.js');
const hb = +(process.argv[2] || 10) / 1000;
for (const lossless of [true, false]) {
  const road = new Road({ bumps: [{ x: 1, h: hb, L: 0.25 }], Rw: 0.04, xmin: -1, xmax: 4 });
  const e = 1e-12, o = { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: 1, ml: 0.4266, road, ctrl: 'off' };
  if (lossless) Object.assign(o, { c: e, ct: e, cx: e });
  const c = new Cart(o), g = c.g, Ms = c.Mb + c.ml, Mx = c.massX();
  const E = () => 0.5 * Mx * c.vx ** 2 + 0.5 * Ms * c.vzb ** 2 + 0.5 * c.mw * c.vzw ** 2 + 0.5 * c.k * (c.zb - c.zw - c.Ls) ** 2
    + 0.5 * c.kt * Math.max(0, c.road.axle(c.x)[0] - c.zw) ** 2 + Ms * g * c.zb + c.mw * g * c.zw;
  const h = 1e-4, E0 = E(); let dmax = 0, W = 0, Nmin = 1e9;
  for (let n = 0; n < 15000; n++) {
    // power the dampers, the drag and the motor put in over the step (forces at the start of the step, as the integrator uses them)
    const vza = c.dza * c.vx, P = -c.c * (c.vzb - c.vzw) ** 2 - c.ct * (vza - c.vzw) * (vza - c.vzw) * (c.N > 0 ? 1 : 0) - c.cx * c.vx ** 2 + c.Fdrive * c.vx;
    c.step(h, 0, 0); W += P * h; Nmin = Math.min(Nmin, c.N);
    dmax = Math.max(dmax, Math.abs(E() - E0 - W));
  }
  console.log(`${lossless ? 'lossless' : 'page dampers, open loop'}, bump ${hb * 1000} mm, 1.5 s: E0 ${E0.toFixed(5)} J; largest |E - E0 - work of dampers, drag and motor| ${dmax.toExponential(2)} J; smallest tyre load ${Nmin.toFixed(2)} N; speed after ${c.vx.toFixed(4)} m/s`);
}
