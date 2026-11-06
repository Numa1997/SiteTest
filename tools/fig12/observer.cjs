// The numbers of the note's §8.5 (the probes and the Kalman filter), from the page's own code:
//   node tools/fig12/observer.cjs [3d|modal] [dx]
// Prints the plant (w, zeta, beta), the LQR gains and the closed loop's poles for that plant, A_d, B_d, Q_d, the Kalman gain
// at the sample with a probe reading once the filter's covariance has settled into its 5-sample cycle, the estimate's standard
// deviations there, and (3d) the probes' reading noise at rest: the rms of y_q over 2 s of the stout standing still.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { World } = load('stout-cart.js'), G = load('guinness-glass.js');
const model = process.argv[2] || '3d', dx = +(process.argv[3] || 0.004);
const w = new World({ fluid: { dx, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03, modal: model === 'modal' }, road: { bumps: [{ x: 50, h: 0, L: 0.25 }], Rw: 0.04 }, cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: 1, ctrl: 'slosh' }, dtMax: 1 / 200 });
const c = w.cart, o = c.obs, m = c.sloshMode, K = c.lqrGains(), f4 = (a) => a.map((v) => v.toPrecision(4)).join(', ');
console.log(`${model} ${dx * 1000} mm: plant f ${(m.w / 2 / Math.PI).toFixed(3)} Hz, zeta ${m.zeta}, beta ${m.beta.toFixed(4)}; M_x ${c.massX().toFixed(4)} kg, b ${c.bForce()} N/A`);
console.log(`LQR K = (${f4(K)})`);
// closed-loop poles of A - B K (4 x 4) by the QR-free route: characteristic polynomial by Faddeev–LeVerrier, roots by Durand–Kerner
const Mx = c.massX(), b = c.bForce(), cx = c.cx, W = m.w, z = m.zeta, be = m.beta;
const A = [[-cx / Mx, 0, 0, 0], [0, 0, 1, 0], [be * cx / Mx, -W * W, -2 * z * W, 0], [-1, 0, 0, 0]], B = [b / Mx, 0, -be * b / Mx, 0];
const Acl = A.map((r, i) => r.map((v, j) => v - B[i] * K[j]));
const mul = (X, Y) => X.map((r) => Y[0].map((_, j) => r.reduce((s, v, k) => s + v * Y[k][j], 0)));
let Mk = Acl.map((r) => r.slice()), coef = [1];
for (let k = 1; k <= 4; k++) { if (k > 1) { const Mp = Mk.map((r, i) => r.map((v, j) => v + (i === j ? coef[k - 1] : 0))); Mk = mul(Acl, Mp); } const tr = Mk.reduce((s, r, i) => s + r[i], 0); coef.push(-tr / k); }
let roots = [0, 1, 2, 3].map((k) => ({ re: 0.4 * Math.cos(2.4 * k) * 10, im: 0.9 * Math.sin(2.4 * k) * 10 }));
const cm = (a, b2) => ({ re: a.re * b2.re - a.im * b2.im, im: a.re * b2.im + a.im * b2.re }), cd = (a, b2) => { const d = b2.re * b2.re + b2.im * b2.im; return { re: (a.re * b2.re + a.im * b2.im) / d, im: (a.im * b2.re - a.re * b2.im) / d }; };
for (let it = 0; it < 2000; it++) roots = roots.map((r, i) => { let p = { re: 1, im: 0 }; for (let k = 1; k <= 4; k++) p = { re: cm(p, r).re + coef[k], im: cm(p, r).im }; let q = { re: 1, im: 0 }; roots.forEach((s, j) => { if (j !== i) q = cm(q, { re: r.re - s.re, im: r.im - s.im }); }); const d = cd(p, q); return { re: r.re - d.re, im: r.im - d.im }; });
console.log('closed-loop poles (1/s): ' + roots.sort((a, b2) => a.re - b2.re).map((r) => r.re.toFixed(2) + (Math.abs(r.im) > 1e-6 ? (r.im > 0 ? ' + ' : ' − ') + Math.abs(r.im).toFixed(2) + 'j' : '')).join(', '));
const sw = roots.filter((r) => Math.abs(r.im) > 1e-6)[0]; if (sw) console.log(`swing pair damping ratio ${(-sw.re / Math.hypot(sw.re, sw.im)).toFixed(3)}`);
console.log(`A_d = [${o.Ad.map(f4).join('; ')}]\nB_d = (${f4(o.Bd)})\nQ_d diag = (${f4(o.Qd.map((r, i) => r[i]))})`);
console.log(`filter: sigma_q ${o.sigQ} m, sigma_v ${o.sigV} m/s, W_F ${o.WF} N^2 s, W_a ${o.Wa} m^2/s^3`);
// settle the covariance: a probe reading every 5th sample (5 ms fluid step, 1 ms sampling)
for (let k = 0; k < 20000; k++) o.update(0, o.x[0], k % 5 === 4 ? 0 : null);
o.update(0, o.x[0], null); o.update(0, o.x[0], null); o.update(0, o.x[0], null); o.update(0, o.x[0], null); o.update(0, o.x[0], 0);
console.log(`Kalman gain at a probe sample, rows v, q, q'; columns speed, swing: [${o.L.map(f4).join('; ')}]`);
console.log(`estimate sd after it: v ${Math.sqrt(o.P[0][0]).toExponential(3)} m/s, q ${(Math.sqrt(o.P[1][1]) * 1000).toFixed(3)} mm, q' ${(Math.sqrt(o.P[2][2]) * 1000).toFixed(2)} mm/s`);
if (model === '3d') {
  const ys = []; const w2 = new World({ fluid: { dx, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03 }, road: { bumps: [{ x: 50, h: 0, L: 0.25 }], Rw: 0.04 }, cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: 0, ctrl: 'off' }, dtMax: 1 / 200 });
  while (w2.t < 2 - 1e-9) { w2.advance(1 / 200); ys.push(w2.cart.probe.y); }
  const mean = ys.reduce((s, v) => s + v, 0) / ys.length, sd = Math.sqrt(ys.reduce((s, v) => s + (v - mean) ** 2, 0) / ys.length);
  console.log(`probes at rest (cart standing, 2 s, ${ys.length} readings): y_q mean ${(mean * 1000).toFixed(3)} mm, sd ${(sd * 1000).toFixed(3)} mm, range ${(Math.min(...ys) * 1000).toFixed(2)} to ${(Math.max(...ys) * 1000).toFixed(2)} mm`);
}
