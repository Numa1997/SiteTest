// Checks of the page's live model, the tulip's computed modes (public/scripts/stout-modal.js), each against an independent
// number. node tools/fig12/modal-check.cjs        exit 1 if any check fails.
//  1 steady push: a_x held, swing damped out; the wall height must be -(a_x/g) sum_n c_n e_n(R) (the finite elements' tilt)
//  2 free swing after a pulse: frequency (Fourier peak) = the data's f11; energy decay rate = 2 zeta11 w11
//  3 heave on a still surface does nothing (linear theory: a_z only scales the stiffness)
//  4 heave pumps a swinging surface at twice its frequency (Mathieu): growth rate = (eps/4) w for a_z = eps g cos(2 w t), zeta = 0
//  5 the same road cut into frames of different lengths gives bit-identical histories (FixedStepper)
//  6 the cart over a 10 mm bump at 1 m/s, open loop, through World: lean against the old cylinder modes and the 3D solver
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { World } = load('stout-cart.js'), { TulipModes, FixedStepper } = load('stout-modal.js'), G = load('guinness-glass.js');
const data = JSON.parse(fs.readFileSync(path.join(__dirname, '../../public/data/fig12/modes.json'), 'utf8'));
const fails = []; const ok = (c, msg) => { console.log((c ? 'ok   ' : 'FAIL ') + msg); if (!c) fails.push(msg); };
const mk = (o) => new TulipModes(Object.assign({ data, profile: G, h0: 0.125 }, o || {}));

{ // 1
  const f = mk({ zetaExtra: 0.3 }), ax = 1.0;
  for (let k = 0; k < 20000; k++) f.step(0.001, ax, 0);
  let want = 0; for (let n = 0; n < f.N; n++) want += -ax / f.g * f.c[n] * f.shapeAt(n, f.Rs);
  ok(Math.abs(f.wallLift() / want - 1) < 1e-6, `steady push 1 m/s^2: wall ${(f.wallLift() * 1000).toFixed(4)} mm, finite elements ${(want * 1000).toFixed(4)} mm (${f.N} modes)`);
}
{ // 2
  const f = mk({ nModes: 1 }), dt = 0.001, T = 20, ys = [], Es = [];
  for (let k = 0; k * dt < T; k++) { const t = k * dt; f.step(dt, t < 0.05 ? 2 * Math.sin(Math.PI * t / 0.05) : 0, 0); ys.push(f.wallLift()); Es.push(f.energy()); }
  let best = 0, fb = 0;
  for (let fr = 3.0; fr < 3.8; fr += 0.0002) { let re = 0, im = 0; for (let k = 100; k < ys.length; k++) { re += ys[k] * Math.cos(2 * Math.PI * fr * k * dt); im += ys[k] * Math.sin(2 * Math.PI * fr * k * dt); } const a = re * re + im * im; if (a > best) { best = a; fb = fr; } }
  const fw = f.w[0] / (2 * Math.PI) * Math.sqrt(1 - f.zeta[0] ** 2);
  ok(Math.abs(fb - fw) < 0.002, `free swing ${fb.toFixed(4)} Hz, data (damped) ${fw.toFixed(4)} Hz`);
  const i1 = 1000, i2 = ys.length - 1, rate = Math.log(Es[i1] / Es[i2]) / ((i2 - i1) * dt);
  ok(Math.abs(rate / (2 * f.zeta[0] * f.w[0]) - 1) < 0.01, `energy decay ${rate.toFixed(5)} 1/s, 2 zeta w ${(2 * f.zeta[0] * f.w[0]).toFixed(5)} 1/s (zeta ${f.zeta[0].toFixed(5)}: wall and bulk, stout nu 2.05e-6)`);
}
{ // 3
  const f = mk(); for (let k = 0; k < 5000; k++) f.step(0.001, 0, 5 * Math.sin(2 * Math.PI * 7 * k * 0.001));
  ok(f.wallLift() === 0, `heave alone on a still surface: wall ${f.wallLift()} m`);
}
{ // 4
  const f = mk({ nModes: 1, nu: 0 }), w = f.w[0], eps = 0.02, dt = 0.0005; f.q[0] = 1e-4;
  const A = []; for (let k = 0; k * dt < 30; k++) { f.step(dt, 0, eps * f.g * Math.cos(2 * w * k * dt)); A.push(Math.hypot(f.q[0], f.qd[0] / w)); }
  const rate = Math.log(A[A.length - 1] / A[Math.round(5 / dt)]) / (A.length * dt - 5);
  ok(Math.abs(rate / (eps * w / 4) - 1) < 0.03, `Mathieu pumping: growth ${rate.toFixed(4)} 1/s, theory eps w/4 = ${(eps * w / 4).toFixed(4)} 1/s`);
}
{ // 7 friction off: the swing keeps its energy. Symplectic Euler keeps a modified energy exactly, so the plain energy wobbles
  //   within each swing by about w h (0.5 %) but must not drift: its mean over the first and the last second must agree
  const f = mk({ friction: false }); f.q[0] = 0.005; let a = 0, b = 0;
  for (let k = 0; k < 20000; k++) { f.step(0.001, 0, 0); if (k < 1000) a += f.energy(); if (k >= 19000) b += f.energy(); }
  ok(Math.abs(b / a - 1) < 1e-4, `friction off, 20 s free swing: mean energy of the last second / first second = ${(b / a).toFixed(7)}`);
}
{ // 8 the books: energy lost = the friction power integrated (stout's skin and a 5 mm head)
  const f = mk({ skin: 1, foam: { h: 0.005 } }); f.q[0] = 0.01; const E0 = f.energy(); let W = 0;
  for (let k = 0; k < 5000; k++) { f.step(0.001, 0, 0); W += (f.Pvisc + f.Pfoam) * 0.001; }
  const lost = E0 - f.energy();
  ok(Math.abs(W / lost - 1) < 0.01, `energy lost in 5 s ${(lost * 1e3).toFixed(4)} mJ, friction work ${(W * 1e3).toFixed(4)} mJ`);
}
{ // 9 foam alone on one mode: the swing stops in finite time, Viola et al. eq. 7.6: t* = 3/(s w) ln[1 + s/(c alpha) (X0/R)^(1/3)],
  //   c = 2 Gamma(1/3) / (5 Gamma(5/6) sqrt(pi)) = 0.5356, s the linear damping ratio (multiple scales, small s and alpha)
  const al = 0.02, f = mk({ nModes: 1, foam: { alpha: al } }), X0 = 0.005; f.q[0] = X0;
  // their envelope dA/dt~ = -s A - c alpha A^(2/3) with u = A^(1/3): u = (u0 + c alpha/s) e^(-s t~/3) - c alpha/s, so A falls to
  // 1e-3 A0 (u to 0.1 u0) at t1 = 3/(s w) ln[(u0 + c alpha/s)/(0.1 u0 + c alpha/s)] and to 0 at t*
  const s0 = f.zeta[0], w = f.w[0], c = 0.5356, u0 = Math.cbrt(X0 / f.Rs), r = c * al / s0;
  const tStar = 3 / (s0 * w) * Math.log(1 + u0 / r), t1 = 3 / (s0 * w) * Math.log((u0 + r) / (0.1 * u0 + r));
  let t = 0; const A = () => Math.hypot(f.q[0], f.qd[0] / w);
  while (A() > 1e-3 * X0 && t < 60) { f.step(0.0005, 0, 0); t += 0.0005; }
  ok(Math.abs(t / t1 - 1) < 0.02, `foam alpha ${al}: swing of ${X0 * 1000} mm falls to 0.1 % after ${t.toFixed(2)} s, Viola et al.'s envelope ${t1.toFixed(2)} s (and stops at ${tStar.toFixed(2)} s)`);
}
{ // 10 the modal mass from the linear data equals the nonlinear data's rho R^3 mu / Rw1^2 (two independent routes)
  const N = JSON.parse(fs.readFileSync(path.join(__dirname, '../../public/data/fig12/nm.json'), 'utf8')), j = N.h.indexOf(125), L = N.levels[j];
  const f = mk(), Mn = 1000 * L.Rs ** 3 * L.mu.p1 / L.Rw[1] ** 2;
  ok(Math.abs(f.M[0] / Mn - 1) < 1e-3, `modal mass of mode 1 at 125 mm: ${f.M[0].toFixed(5)} kg (linear data), ${Mn.toFixed(5)} kg (nonlinear data)`);
}
const bumps = []; for (let n = 0; n < 60; n++) bumps.push({ x: 1.0 + 2 * n, h: 0.010, L: 0.25 });
const mkWorld = (fluid, ctrl) => new World({ fluidInstance: fluid, road: { bumps, Rw: 0.04, xmin: -1, xmax: 125 }, cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: 1, ctrl: ctrl || 'off', susp: false }, dtMax: 0.001 });
{ // 5
  // every step's state recorded; the first 2000 steps compared value by value
  const run = (frames) => {
    const w = mkWorld(mk()), st = new FixedStepper(w), hist = [], adv = w.advance.bind(w);
    w.advance = (h) => { adv(h); hist.push(w.t, w.cart.x, w.cart.vx, w.cart.zb, w.fluid.q[0], w.fluid.qd[0]); };
    let i = 0; while (st.steps < 2000) st.advance(frames[i++ % frames.length]);
    return hist.slice(0, 6 * 2000);
  };
  const a = run([1 / 60]), b = run([0.0313, 0.0041, 0.017, 0.0229]);
  ok(a.length === b.length && a.every((v, k) => v === b[k]), `frames of 16.7 ms vs mixed 4-31 ms: 2000 steps bit-identical (step 2000: x ${a[a.length - 5]}, q1 ${a[a.length - 2]})`);
}
{ // 6
  const w = mkWorld(mk()); let dw = 0;
  while (w.t < 2.3 - 1e-9) { w.advance(0.001); const d = 2 * w.fluid.wallLift(); if (Math.abs(d) > Math.abs(dw)) dw = d; }
  console.log(`info 10 mm bump, open loop: lean ${(Math.abs(dw) * 1000).toFixed(1)} mm (old cylinder modes 24.7 mm, 3D solver 4 mm grid 25.0 mm, note §13)`);
  ok(Math.abs(Math.abs(dw) * 1000 - 25) < 3, 'within 3 mm of the 3D solver');
}
console.log(fails.length ? `FAILED ${fails.length}` : 'ALL PASSED');
process.exit(fails.length ? 1 : 0);
