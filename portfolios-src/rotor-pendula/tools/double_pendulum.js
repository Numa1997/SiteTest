#!/usr/bin/env node
// The double pendulum, free and with its first arm driven round at a steady rate (chapter 1 of the notes).
//  - Free: the site's own engine, deriv() and rk4() copied at run time out of public/simulations/Double Pendulum.html
//    (Fig. 2: point masses m1 = m2 = 1 kg on l1 = l2 = 1 m, g = 9.81, RK4 at h = 1/600 s), started from the page's
//    default 120 deg, 150 deg. Its largest Lyapunov exponent, from the tangent of two copies 1e-9 apart renormalised
//    every 0.05 s, and the separation of an unrenormalised twin.
//  - Driven: the same Lagrangian with theta1 = Omega t prescribed. The first arm's equation drops out and the second arm obeys,
//    counted in turns (phi = Omega t measured from the horizontal), theta'' + kappa theta' + R sin(theta) + G cos(phi + theta) = 0,
//    with R = l1/l2, G = g/(l2 Omega^2) for a point bob (R = 3 r_p/(2l), G = 3g/(2l Omega^2) for the rod of the notes).
//    Largest Lyapunov exponent per turn from the tangent equation, over a range of Gamma = R/G, from 9 starts each.
//  - Check of the reduction: along a driven run, the first arm's Lagrange equation gives the torque that keeps it turning;
//    its work equals the change of the pair's energy (eq. 1.8 of the notes with no brake).
// Writes data/L0_double.json. Usage: node tools/double_pendulum.js   (about a minute)
const fs = require('fs');
const path = require('path');

const PAGE = path.join(__dirname, '..', '..', '..', 'public', 'simulations', 'Double Pendulum.html');
const src = fs.readFileSync(PAGE, 'utf8');
const a = src.indexOf('function deriv(s)'), b = src.indexOf('function energy(s)');
if (a < 0 || b < a) throw new Error('deriv/rk4 not found in the Double Pendulum page');
const engineText = src.slice(a, b);
const g = 9.81, m1 = 1, l1 = 1, m2 = 1, l2 = 1, H = 1 / 600;
const engine = new Function('g', 'm1', 'l1', 'm2', 'l2', engineText + '\nreturn { deriv: deriv, rk4: rk4 };')(g, m1, l1, m2, l2);
const energy = s => 0.5 * (m1 + m2) * l1 * l1 * s[2] * s[2] + 0.5 * m2 * l2 * l2 * s[3] * s[3]
  + m2 * l1 * l2 * s[2] * s[3] * Math.cos(s[0] - s[1]) - (m1 + m2) * g * l1 * Math.cos(s[0]) - m2 * g * l2 * Math.cos(s[1]);
const D2R = Math.PI / 180;
const out = { page: 'public/simulations/Double Pendulum.html', m1, l1, m2, l2, g, h: H };

// ---- free: Lyapunov exponent and twin separation, from the page's 120, 150 degrees ------------------------------------------
{
  const s0 = [120 * D2R, 150 * D2R, 0, 0], E0 = energy(s0), eps = 1e-9, T = 200, every = 30;   // renormalise every 30 steps = 0.05 s
  let s = s0.slice(), t2 = s0.slice(); t2[0] += eps;
  let sum = 0, n = Math.round(T / H), Emax = 0;
  for (let k = 1; k <= n; k++) {
    s = engine.rk4(s, H); t2 = engine.rk4(t2, H);
    if (k % every === 0) {
      const d = Math.hypot(...t2.map((v, i) => v - s[i]));
      sum += Math.log(d / eps);
      t2 = s.map((v, i) => v + (t2[i] - v) * eps / d);
    }
    Emax = Math.max(Emax, Math.abs(energy(s) - E0));
  }
  out.free = { lyap_per_s: sum / T, T, energy_drift_J: Emax, E0 };
  // twin 1e-3 rad away in theta1 (the page's chaos twin) and 1e-9 away, unrenormalised: the lower bob's separation (m) every 0.1 s
  const twin = d0 => {
    let p = s0.slice(), q = s0.slice(); q[0] += d0;
    const ts = [], sep = [];
    for (let k = 0; k <= Math.round(30 / H); k++) {
      if (k % 60 === 0) {
        const xa = l1 * Math.sin(p[0]) + l2 * Math.sin(p[1]), ya = -l1 * Math.cos(p[0]) - l2 * Math.cos(p[1]);
        const xb = l1 * Math.sin(q[0]) + l2 * Math.sin(q[1]), yb = -l1 * Math.cos(q[0]) - l2 * Math.cos(q[1]);
        ts.push(+(k * H).toFixed(3)); sep.push(Math.hypot(xa - xb, ya - yb));
      }
      p = engine.rk4(p, H); q = engine.rk4(q, H);
    }
    return { t: ts, sep };
  };
  out.free.twin_1e3 = twin(1e-3); out.free.twin_1e9 = twin(1e-9);
}

// ---- driven: theta'' + kappa theta' + R sin(theta) + G cos(phi + theta) = 0, phi in radians of rotor turning -----------------
function drivenLyap(R, G, kappa, th0, w0, turns, perTurn) {
  const h = 2 * Math.PI / perTurn;
  const f = (ph, y) => {           // y = [theta, theta', dtheta, dtheta']
    const c = Math.cos(ph + y[0]), sn = Math.sin(ph + y[0]);
    return [y[1], -kappa * y[1] - R * Math.sin(y[0]) - G * c, y[3], -kappa * y[3] - (R * Math.cos(y[0]) - G * sn) * y[2]];
  };
  let y = [th0, w0, 1, 0], ph = 0, sum = 0, nTr = 50 * perTurn;   // let 50 turns pass, then measure
  const n = (turns + 50) * perTurn;
  for (let k = 0; k < n; k++) {
    const k1 = f(ph, y), k2 = f(ph + h / 2, y.map((v, i) => v + h / 2 * k1[i])), k3 = f(ph + h / 2, y.map((v, i) => v + h / 2 * k2[i])),
      k4 = f(ph + h, y.map((v, i) => v + h * k3[i]));
    y = y.map((v, i) => v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])); ph += h;
    if ((k + 1) % (perTurn / 4) === 0) {
      const d = Math.hypot(y[2], y[3]);
      if (k + 1 > nTr) sum += Math.log(d);
      y[2] /= d; y[3] /= d;
    }
  }
  return sum / turns;
}
// a small fixed set of starts: on the line at rest, and eight others spread over angle and rate (some tumbling over)
const STARTS = [[0, 0], [0.5, 0], [-1, 1], [2, 0], [3, -2], [-2.5, 3], [1.5, -4], [-0.5, 6], [Math.PI - 0.1, 0]];
function sweep(R, kappa, gammas, turns, perTurn) {
  return gammas.map(Gam => {
    const G = R / Gam, ex = STARTS.map(([t, w]) => drivenLyap(R, G, kappa, t, w, turns, perTurn));
    return { Gamma: Gam, G, max: Math.max(...ex), n_chaotic: ex.filter(e => e > 0.02).length, lyap: ex };
  });
}
const T0 = Date.now();
const gam = [];
for (let i = 0; i <= 24; i++) gam.push(+Math.pow(10, -1 + 2.5 * i / 24).toPrecision(4));   // Gamma from 0.1 to 31.6
out.driven = {
  starts: STARTS, threshold: 0.02,
  equal_arms: { R: l1 / l2, kappa: 0, sweep: sweep(l1 / l2, 0, gam, 400, 800) },
  rod_63m: { R: 94.5, kappa: 0, sweep: sweep(94.5, 0, gam.filter(x => x >= 1), 400, 800) },
};
console.log(`driven sweeps in ${((Date.now() - T0) / 1000).toFixed(1)} s`);
// the turbine's numbers (rod, 1 kg on 1 m at 63 m): no brake, and the best brake kappa* = R - 1
const SETUP = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'setup.json'), 'utf8'));
out.turbine = [6, 8, 10].map(v => {
  const Om = SETUP.LAM_STAR * v / SETUP.R_ROT, R = 1.5 * SETUP.R_ROT / SETUP.L_B, G = 1.5 * SETUP.G0 / (SETUP.L_B * Om * Om);
  const free = STARTS.map(([t, w]) => drivenLyap(R, G, 0, t, w, 400, 800));
  const braked = STARTS.map(([t, w]) => drivenLyap(R, G, R - 1, t, w, 200, 1600));
  return { wind: v, R, G, Gamma: R / G, unbraked_max: Math.max(...free), unbraked: free, braked_max: Math.max(...braked) };
});
// a check of the step: the equal-arm sweep at Gamma = 1 with twice as many steps per turn
out.driven.step_check = { Gamma: 1, per800: sweep(1, 0, [1], 400, 800)[0].max, per1600: sweep(1, 0, [1], 400, 1600)[0].max };

// ---- the reduction checked: the first arm's equation becomes the torque that drives it --------------------------------------
// Equal arms, theta1 = Omega t from 120 deg, theta2 from 150 deg, at rest relative to the arm, Gamma = Omega^2 l1/g = 4.
{
  const Om = Math.sqrt(4 * g / l1), h = 2 * Math.PI / Om / 4000;
  // second arm with the first prescribed (point bob, angles from the downward vertical as on the page):
  // l2 th2'' = l1 Om^2 sin(th1 - th2) - g sin(th2)
  const acc2 = (t1, t2) => (l1 * Om * Om * Math.sin(t1 - t2) - g * Math.sin(t2)) / l2;
  // the first arm's Lagrange equation, read as the torque tau the drive must supply:
  // (m1+m2) l1^2 th1'' + m2 l1 l2 [th2'' cos(d) + w2^2 sin(d)] + (m1+m2) g l1 sin(th1) = tau,  d = th1 - th2, th1'' = 0
  const tau = (t1, t2, w2, a2) => m2 * l1 * l2 * (a2 * Math.cos(t1 - t2) + w2 * w2 * Math.sin(t1 - t2)) + (m1 + m2) * g * l1 * Math.sin(t1);
  let t = 0, y = [150 * D2R, Om, 0];            // theta2, omega2, and the drive's work, integrated together by RK4
  const th1 = tt => 120 * D2R + Om * tt;
  const E = (tt, a, w) => energy([th1(tt), a, Om, w]);
  const E0 = E(0, y[0], y[1]);
  const f = (tt, z) => { const a2 = acc2(th1(tt), z[0]); return [z[1], a2, Om * tau(th1(tt), z[0], z[1], a2)]; };
  let worst = 0;
  for (let k = 0; k < 4000 * 20; k++) {           // 20 turns
    const k1 = f(t, y), k2 = f(t + h / 2, y.map((v, i) => v + h / 2 * k1[i])), k3 = f(t + h / 2, y.map((v, i) => v + h / 2 * k2[i])),
      k4 = f(t + h, y.map((v, i) => v + h * k3[i]));
    y = y.map((v, i) => v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])); t += h;
    worst = Math.max(worst, Math.abs(y[2] - (E(t, y[0], y[1]) - E0)));
  }
  out.reduction = { Gamma: 4, turns: 20, worst_energy_gap_J: worst, energy_scale_J: (m1 + m2) * g * l1 };
}
fs.writeFileSync(path.join(__dirname, '..', 'data', 'L0_double.json'), JSON.stringify(out));
console.log('free: Lyapunov', out.free.lyap_per_s.toFixed(3), '/s, energy drift', out.free.energy_drift_J.toExponential(2), 'J');
for (const k of ['equal_arms', 'rod_63m']) console.log(k, out.driven[k].sweep.map(r => `${r.Gamma}:${r.max.toFixed(3)}(${r.n_chaotic})`).join(' '));
for (const r of out.turbine) console.log(`${r.wind} m/s Gamma ${r.Gamma.toFixed(2)}: unbraked max ${r.unbraked_max.toFixed(4)}, braked max ${r.braked_max.toFixed(3)} per turn`);
console.log('step check', out.driven.step_check, 'reduction', out.reduction);
console.log(`data/L0_double.json in ${((Date.now() - T0) / 1000).toFixed(1)} s`);
