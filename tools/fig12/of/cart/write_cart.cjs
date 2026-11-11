// Fig. 12: write the cart's parameters and road table for the C++ cart (cart.H) from the JavaScript Cart and Road
// (public/scripts/stout-cart.js), so both are defined in one place.
// node tools/fig12/of/cart/write_cart.cjs '<json ride>' <out dir>
// ride: {"road": {...Road options...}, "v0": 1, "ctrl": "off|speed|preview", "susp": false, "fill": 0.125, "rho": 1000}
// The cart's own options are the page's: x0 0.5 m, wheel radius 0.04 m, spring length 0.135 m.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../../../public/scripts', f), 'utf8'))(m); return m.exports; };
const S = load('stout-cart.js'), G = load('guinness-glass.js');
const ride = JSON.parse(process.argv[2]), out = process.argv[3];
for (const k of ['road', 'v0', 'ctrl', 'susp', 'fill', 'rho']) if (!(k in ride)) throw new Error('ride: missing ' + k);
// the stout's mass: rho times the glass's volume up to the fill (the same integral as Fluid.volumeTo)
const Rz = (z) => { const f = Math.max(0, z) / G.dz, i = Math.floor(f); if (i >= G.R.length - 1) return G.R[G.R.length - 1]; return G.R[i] + (f - i) * (G.R[i + 1] - G.R[i]); };
const nV = Math.max(1, Math.round(ride.fill / 5e-5)), dV = ride.fill / nV; let V = 0;
for (let k = 0; k <= nV; k++) { const r = Rz(k * dV); V += (k === 0 || k === nV ? 0.5 : 1) * Math.PI * r * r * dV; }
const road = new S.Road(Object.assign({ Rw: 0.04, xmin: -1, xmax: 14 }, ride.road));
const c = new S.Cart({ x0: 0.5, Rw: 0.04, Ls: 0.135, v0: ride.v0, ctrl: ride.ctrl, susp: ride.susp, road, ml: ride.rho * V });
const keys = ['Mb', 'mw', 'Rw', 'Iw', 'k', 'c', 'kt', 'ct', 'cx', 'Crr', 'Tf', 'bf', 'CdA', 'rhoAir', 'vSmooth', 'v0', 'ml', 'Ls', 'g', 'Ngear', 'Km', 'Ra', 'Jm', 'Vmax', 'Imax', 'tauI', 'Ts', 'Kp', 'Ki', 'csky', 'Umax', 'tauU', 'mu'];
const lines = keys.map((k) => { if (typeof c[k] !== 'number' || !isFinite(c[k])) throw new Error('cart: ' + k + ' not a number'); return k + ' ' + c[k].toPrecision(17); });
lines.push('ctrl ' + { off: 0, speed: 1, preview: 2 }[ride.ctrl], 'susp ' + (ride.susp ? 1 : 0), 'x0 0.5');
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, 'cart.params'), lines.join('\n') + '\n');
fs.writeFileSync(path.join(out, 'road.table'), road.xmin.toPrecision(17) + ' ' + road.h.toPrecision(17) + ' ' + road.za.length + '\n' + Array.from(road.za, (v) => v.toPrecision(17)).join('\n') + '\n');
console.log(`cart for ${JSON.stringify(ride.road)} at ${ride.v0} m/s, ${ride.ctrl}${ride.susp ? ' + suspension' : ''}: stout ${(1000 * ride.rho * V).toFixed(1)} g; road table ${road.za.length} points`);
if (process.env.TRACE) {   // the JavaScript cart's own ride with the stout rigid, for test_cart
  const T = +process.env.TRACE, rows = [];
  for (let n = 1; n * 1e-4 <= T + 1e-12; n++) { c.step(1e-4, 0, 0); if (n % 100 === 0) rows.push([c.t, c.x, c.vx, c.zb, c.zw, c.i, c.xi].map((v) => v.toPrecision(17)).join(' ')); }
  fs.writeFileSync(path.join(out, 'trace.js.txt'), rows.join('\n') + '\n');
}
