// The cart on rough roads (part 3): node tools/fig12/roads.cjs <nm|modal|3d> <road,...> <ctrl,...> [v0 m/s] [seconds] [dx]
// road: isoA isoB isoC isoD washboard setts. The cart starts at x = 0.5 m on the set speed; the roughness ramps in over
// 0.5–1 m. Printed per run: the road's rms height, the glass's vertical acceleration (rms over the run after 1.5 s, and the rms
// in the band 6.5–7.2 Hz around twice the swing frequency, f = 2 f11 = 6.84 Hz, by a discrete Fourier sum), the largest
// lean, the stout spilled, the share of 1 ms samples with the tyre off the road (N = 0) and with the drive at its grip
// limit mu N, and the smallest tyre load. The parametric (Faraday) threshold for the first mode is a vertical acceleration of
// amplitude 4 zeta g = 0.21 m/s^2 at 6.84 Hz (note §6.6); a band rms r stands for an amplitude of about r sqrt 2.
const fs = require('fs'), path = require('path');
const load = (f) => { const m = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/scripts', f), 'utf8'))(m); return m.exports; };
const { World } = load('stout-cart.js'), G = load('guinness-glass.js'), NM = load('stout-nm.js');
const model = process.argv[2] || 'nm', roads = (process.argv[3] || 'isoA,isoB,isoC,isoD,washboard,setts').split(','), ctrls = (process.argv[4] || 'off,speed,slosh').split(',');
const v0 = +(process.argv[5] || 1), T = +(process.argv[6] || 6), dx = +(process.argv[7] || 0.004);
for (const rd of roads) for (const ctrl of ctrls) {
  const road = rd.startsWith('iso') ? { kind: 'iso', cls: rd.slice(3) } : { kind: rd };
  const w = new World({ fluid: { dx, profile: G, h0: 0.125, H: (G.R.length - 1) * G.dz + 0.03, modal: model !== '3d', nm: model === 'nm', nmCoeffs: NM },
    road: Object.assign({ Rw: 0.04, xmin: -1, xmax: 125 }, road), cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0, ctrl }, dtMax: 1 / 200 });
  const c = w.cart, f = w.fluid, t0 = Date.now(), az = [];
  let lean = 0, air = 0, grip = 0, ns = 0, Nmin = 1e9, swirl = 0;
  while (w.t < T - 1e-9) {
    w.advance(1 / 200);
    if (w.t > 1.5) az.push(w.lastAz);
    lean = Math.max(lean, Math.abs(c.probe.ef - c.probe.eb)); if (f.s1 != null) swirl = Math.max(swirl, Math.abs(f.s1));
    ns++; if (c.N <= 0) air++; if (c.slip) grip++; Nmin = Math.min(Nmin, c.N);
  }
  const rms = Math.sqrt(az.reduce((a, v) => a + v * v, 0) / az.length), dt = 1 / 200, Tn = az.length * dt;
  let band = 0; for (let fr = 6.5; fr <= 7.2001; fr += 1 / Tn) { let re = 0, im = 0; az.forEach((v, k) => { re += v * Math.cos(2 * Math.PI * fr * k * dt); im += v * Math.sin(2 * Math.PI * fr * k * dt); }); band += 2 * (re * re + im * im) / (az.length * az.length); }
  console.log(`${model} ${rd} (rms ${(c.road.rms * 1000).toFixed(1)} mm), ${ctrl}, ${v0} m/s: glass a_z rms ${rms.toFixed(2)} m/s^2, in 6.5–7.2 Hz ${Math.sqrt(band).toFixed(3)} m/s^2; lean max ${(lean * 1000).toFixed(1)} mm${f.s1 != null ? ', swirl max ' + (swirl * 1000).toFixed(1) + ' mm' : ''}; spilled ${((w.spilledMass || 0) * 1000).toFixed(1)} g; tyre off the road ${(100 * air / ns).toFixed(1)} % of steps, drive at grip limit ${(100 * grip / ns).toFixed(1)} %, smallest tyre load ${Nmin.toFixed(2)} N (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
}
