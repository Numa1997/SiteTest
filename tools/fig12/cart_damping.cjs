/* Fig. 12 computed on Kaggle: how much the cart alone damps the stout's swing.
 * Runs the site's reduced model (stout-cart.js ModalFluid, three sloshing modes) on the same one-wheel cart, road and
 * speed loop as the Kaggle rides, once with the stout's own damping switched off (zetaScale 0) and once with the wall's
 * (zetaScale 1, zeta_1 = 0.0053), and writes the first mode's wall height q every 1/30 s to cart_damping.json beside this
 * file. tools/fig12/kaggle_decay.py --modal fits the free decay after the last bump.
 * Run: node tools/fig12/cart_damping.cjs */
const fs = require('fs'), os = require('os'), path = require('path'), P = path.join(__dirname, '../../public/scripts/');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(P + f, 'utf8'))(m); return m.exports; };
const G = load('guinness-glass.js'), SC = load('stout-cart.js');
// the road of the stored rides (the notebook's ROADS, version 3)
const bumps = [{ x: 1.5, h: 0.01, L: 0.6 }, { x: 3.5, h: -0.008, L: 0.6 }, { x: 5.75, h: 0.005, L: 0.5 }, { x: 6.25, h: 0.005, L: 0.5 },
  { x: 6.75, h: 0.005, L: 0.5 }, { x: 7.25, h: 0.005, L: 0.5 }, { x: 9.0, h: 0.01, L: 0.25 }];
const out = {};
for (const v0 of [0.5, 1.0, 1.5]) for (const zs of [0, 1]) {
  const w = new SC.World({ fluid: { modal: true, zetaScale: zs, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03, nModes: 3 },
    road: { bumps, Rw: 0.04, xmin: -1, xmax: 60 }, cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0, ctrl: 'speed', susp: false }, dtMax: 1 / 400 });
  const t = [], q = [], x = [];
  while (w.t < 20 - 1e-9) { w.advance(1 / 30); t.push(w.t); q.push(w.fluid.q[0] * 1000); x.push(w.cart.x); }
  out[v0.toFixed(1) + (zs ? ' wall' : ' no wall')] = { v0, zeta_fluid: w.fluid.zeta[0], t, q, x };
}
const file = path.join(os.tmpdir(), 'fig12_cart_damping.json'); fs.writeFileSync(file, JSON.stringify(out));
console.log('wrote', file, Object.keys(out).join(', '));
