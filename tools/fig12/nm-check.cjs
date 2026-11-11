// Checks of the page's large-swing model (TulipNM in public/scripts/stout-modal.js). node tools/fig12/nm-check.cjs; exit 1 on failure.
//  1 small swings: TulipNM and the linear TulipModes give the same lean over a 10 mm bump at 1 m/s (open loop, World)
//  2 planar softening, 125 mm fill, released at a 15 and a 32 mm lean: against the 3D solver's free swing from 14.7 to 32.7 mm
//    (3.194 -> 3.109 Hz, -2.66 %, notes/fig12/runs/linearity-3d-*.json, tools/fig12/linfit.cjs)
//  3 friction off: no drift of the swing's amplitude over 20 s
//  4 shaken sideways at a_x = 0.3 sin(2 pi f t) m/s^2 for 20 s: at f = 0.97 f11 the swing turns into a swirl, at 1.06 f11 it stays
//    planar (FLT 2016's regime boundaries for the page's cylinder coefficients: 0.925, 0.985, 1.035 f11; notes/fig12/check-11-9.md)
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { World } = load('stout-cart.js'), { TulipModes, TulipNM } = load('stout-modal.js'), G = load('guinness-glass.js');
const rd = (f) => JSON.parse(fs.readFileSync(path.join(__dirname, '../../public/data/fig12', f), 'utf8'));
const data = rd('modes.json'), nmData = rd('nm.json');
const fails = []; const ok = (c, msg) => { console.log((c ? 'ok   ' : 'FAIL ') + msg); if (!c) fails.push(msg); };
const mkNM = (o) => new TulipNM(Object.assign({ data, nmData, profile: G, h0: 0.125 }, o || {}));
const bumps = []; for (let n = 0; n < 60; n++) bumps.push({ x: 1.0 + 2 * n, h: 0.010, L: 0.25 });
const world = (fluid) => new World({ fluidInstance: fluid, road: { bumps, Rw: 0.04, xmin: -1, xmax: 125 }, cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: 1, ctrl: 'off', susp: false }, dtMax: 0.001 });
{ // 1
  const lean = (f) => { const w = world(f); let m = 0; while (w.t < 2.3 - 1e-9) { w.advance(0.001); m = Math.max(m, Math.abs(f.wallAt ? f.wallAt(0) - f.wallAt(Math.PI) : 2 * f.wallLift())); } return m * 1000; };
  const a = lean(new TulipModes({ data, profile: G, h0: 0.125 })), b = lean(mkNM());
  ok(Math.abs(a - b) < 0.6, `10 mm bump, open loop: lean ${b.toFixed(2)} mm (large-swing model), ${a.toFixed(2)} mm (linear model)`);
}
// a free swing of lean L (mm) from rest-released p1, friction off: its frequency by zero crossings of the wall height
function freeSwing(L, T, opt) {
  const f = mkNM(Object.assign({ friction: false }, opt || {})); f.b[1] = L / 2 / 1000 / (f.Rs * f.Rw[1]); f.b[2] = 1e-9;
  const ys = [], dt = 0.0005; let amp0 = 0, amp1 = 0;
  for (let k = 0; k * dt < T; k++) { f.step(dt, 0, 0); ys.push(f.wallAt(0) - f.wallAt(Math.PI)); }
  const c = []; for (let k = 1; k < ys.length; k++) if (Math.sign(ys[k]) !== Math.sign(ys[k - 1])) c.push((k - ys[k] / (ys[k] - ys[k - 1])) * dt);
  const n1 = Math.round(1 / dt); for (let k = 0; k < n1; k++) amp0 = Math.max(amp0, Math.abs(ys[k])); for (let k = ys.length - n1; k < ys.length; k++) amp1 = Math.max(amp1, Math.abs(ys[k]));
  return { f: (c.length - 1) / (2 * (c[c.length - 1] - c[0])), amp0: amp0 * 1000, amp1: amp1 * 1000 };
}
{ // 2
  const a = freeSwing(15, 12), b = freeSwing(32, 12), sh = (b.f / a.f - 1) * 100;
  ok(Math.abs(sh - (-2.66)) < 0.3, `planar softening at 125 mm: ${a.f.toFixed(4)} Hz (lean ${a.amp0.toFixed(1)} mm) -> ${b.f.toFixed(4)} Hz (${b.amp0.toFixed(1)} mm): ${sh.toFixed(2)} % (3D solver -2.66 %)`);
}
{ // 3
  const a = freeSwing(20, 20);
  ok(Math.abs(a.amp1 / a.amp0 - 1) < 0.01, `friction off, 20 s: lean amplitude ${a.amp0.toFixed(2)} mm in the first second, ${a.amp1.toFixed(2)} mm in the last`);
}
{ // 4
  const run = (ratio) => {
    const f = mkNM({ skin: 1 }), f11 = f.w[0] / (2 * Math.PI) * ratio, dt = 0.001; let sw = 0, pl = 0;
    for (let k = 0; k * dt < 20; k++) { const t = k * dt; f.step(dt, 0.3 * Math.sin(2 * Math.PI * f11 * t), 0); if (t > 15) { sw = Math.max(sw, Math.abs(f.s1)); pl = Math.max(pl, Math.abs(f.q[0])); } }
    return { sw: sw * 1000, pl: pl * 1000, breaks: f.breaks };
  };
  const a = run(0.97), b = run(1.06);
  ok(a.sw > 0.3 * a.pl, `shaken at 0.97 f11: sideways swing ${a.sw.toFixed(1)} mm against ${a.pl.toFixed(1)} mm along the road (a swirl)`);
  ok(b.sw < 0.05 * b.pl, `shaken at 1.06 f11: sideways swing ${b.sw.toFixed(3)} mm against ${b.pl.toFixed(1)} mm along the road (planar)`);
}
console.log(fails.length ? `FAILED ${fails.length}` : 'ALL PASSED');
process.exit(fails.length ? 1 : 0);
