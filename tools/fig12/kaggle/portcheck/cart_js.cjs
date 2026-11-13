// The site's Cart (public/scripts/stout-cart.js) on one road with a rigid load and a prescribed probe signal: the reference
// for the JAX port (stout_jax.Cart). node cart_js.cjs <ctrl> <susp 0|1> <out.json>; reads case.json beside it.
const path = require('path'), fs = require('fs');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../../../public/scripts', f), 'utf8'))(m); return m.exports; };
const SC = load('stout-cart.js');
const C = JSON.parse(fs.readFileSync(path.join(__dirname, 'case.json'), 'utf8'));
const [ctrl, susp, out] = [process.argv[2], +process.argv[3], process.argv[4]];
const road = new SC.Road({ kind: 'bumps', bumps: C.bumps, Rw: C.cart.Rw, xmin: -1, xmax: C.xmax });
const cart = new SC.Cart(Object.assign({}, C.cart, { v0: C.v0, ml: C.ml, ctrl, susp: !!susp, road, x0: C.x0 }));
cart.sloshMode = C.plant;
const so = { sigQ: 0.0008, sigV: 0.002, WF: 0.5, Wa: 0.002 };
cart.probe = { y: 0, fresh: false }; cart.noiseQ = 0; cart.noiseV = 0;
cart.obs = new SC.Observer({ w: C.plant.w, zeta: C.plant.zeta, beta: C.plant.beta, Mx: cart.massX(), b: cart.bForce(), cx: cart.cx, Ts: cart.Ts, sigQ: so.sigQ, sigV: so.sigV, WF: so.WF, Wa: so.Wa, v: cart.vx });
cart.uPrev = cart.i;
const rec = { t: [], x: [], vx: [], zb: [], zw: [], i: [], icmd: [], us: [], xi: [], q: [], K: cart.lqrGains(), Ks: cart.suspGains() };
const yq = (t) => C.probe.A * Math.sin(C.probe.w * t) * Math.exp(-C.probe.d * t);
let t = 0;
for (let n = 0; n < C.nsteps; n++) {
  if (n > 0) { cart.probe.y = yq(t); cart.probe.fresh = true; }
  for (let k = 0; k < C.nsub; k++) cart.step(C.h / C.nsub, 0, 0);
  t += C.h;
  rec.t.push(t); rec.x.push(cart.x); rec.vx.push(cart.vx); rec.zb.push(cart.zb); rec.zw.push(cart.zw); rec.i.push(cart.i); rec.icmd.push(cart.icmd);
  rec.us.push(cart.us); rec.xi.push(cart.xi); rec.q.push(cart.obs.x[1]);
}
fs.writeFileSync(out, JSON.stringify(rec));
