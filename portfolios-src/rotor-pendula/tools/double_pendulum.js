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
// ---- once-per-turn snapshots (Poincaré sections) and the edge of chaos (section 1.5 of the notes) ---------------------------
// The held pendulum, no brake, sampled each time the first arm passes the horizontal rising (phi = 0 mod 2 pi).
// Each orbit also carries its largest Lyapunov exponent per turn (tangent equation, renormalised every quarter turn).
function section(R, G, th0, w0, turns, perTurn) {
  const h = 2 * Math.PI / perTurn;
  const f = (ph, y) => {
    const c = Math.cos(ph + y[0]), sn = Math.sin(ph + y[0]);
    return [y[1], -R * Math.sin(y[0]) - G * c, y[3], -(R * Math.cos(y[0]) - G * sn) * y[2]];
  };
  let y = [th0, w0, 1, 0], ph = 0, sum = 0;
  const pts = [];
  for (let n = 0; n < turns; n++) {
    for (let k = 0; k < perTurn; k++) {
      const k1 = f(ph, y), k2 = f(ph + h / 2, y.map((v, i) => v + h / 2 * k1[i])), k3 = f(ph + h / 2, y.map((v, i) => v + h / 2 * k2[i])),
        k4 = f(ph + h, y.map((v, i) => v + h * k3[i]));
      y = y.map((v, i) => v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])); ph += h;
      if ((k + 1) % (perTurn / 4) === 0) { const d = Math.hypot(y[2], y[3]); sum += Math.log(d); y[2] /= d; y[3] /= d; }
    }
    ph = 0;                                                       // phi is periodic: restart the clock each turn, exactly
    const th = Math.atan2(Math.sin(y[0]), Math.cos(y[0]));
    pts.push([+th.toFixed(4), +y[1].toFixed(4)]);
  }
  return { th0, w0, lyap: sum / turns, pts };
}
// complete elliptic integrals K(m), E(m), parameter m = k^2, by the arithmetic-geometric mean
function KE(m) {
  let a = 1, b = Math.sqrt(1 - m), c = Math.sqrt(m), s = 0.5 * c * c, p = 0.5;
  while (Math.abs(c) > 1e-15) { const an = (a + b) / 2; c = (a - b) / 2; b = Math.sqrt(a * b); a = an; p *= 2; s += p * c * c; }
  const K = Math.PI / (2 * a);
  return [K, K * (1 - s)];
}
// the action (1/2 pi) times the area of a swing in the frozen landscape u = -A cos(theta - theta_b): libration of amplitude a,
// J = (8 sqrt(A)/pi)[E(k) - (1 - k^2) K(k)], k = sin(a/2); rotation of energy E > A, J = (1/2 pi) int sqrt(2(E + A cos x)) dx
const Jlib = (A, a) => { const k2 = Math.sin(a / 2) ** 2, [K, E] = KE(k2); return 8 * Math.sqrt(A) / Math.PI * (E - (1 - k2) * K); };
const Jrot = (A, E) => { let s = 0; const n = 4000; for (let i = 0; i <= n; i++) { const x = -Math.PI + 2 * Math.PI * i / n; s += (i % n === 0 ? 1 : i % 2 ? 4 : 2) * Math.sqrt(2 * (E + A * Math.cos(x))); } return s * (2 * Math.PI / n) / 3 / (2 * Math.PI); };
const bisect = (fn, lo, hi) => { for (let i = 0; i < 200; i++) { const mid = (lo + hi) / 2; if ((fn(lo) < 0) === (fn(mid) < 0)) lo = mid; else hi = mid; } return (lo + hi) / 2; };
{
  const T1 = Date.now(), PT = 800;
  // equal arms (point bob, R = l1/l2 = 1) held at Gamma = 4: G = R/Gamma
  const eq = { R: 1, G: 0.25, Gamma: 4, orbits: [] };
  eq.orbits.push(section(1, 0.25, 0, 0, 2500, PT));                                         // the chaotic sea, one orbit
  for (const t of [0.85, 0.95, 1.05, 1.15, 1.25, 1.35, 1.55]) eq.orbits.push(section(1, 0.25, t, 0, 300, PT));   // the island and a satellite
  for (const w of [2.2, 2.6, 3.0, -2.6, -3.0, -3.4]) eq.orbits.push(section(1, 0.25, 0, w, 300, PT));         // tumbling right over
  // the rod of the notes at 6 m/s, the largest push
  const v6 = 6, Om6 = SETUP.LAM_STAR * v6 / SETUP.R_ROT;
  const R = 1.5 * SETUP.R_ROT / SETUP.L_B, G = 1.5 * SETUP.G0 / (SETUP.L_B * Om6 * Om6), thb = Math.atan2(-G, R), A0 = Math.hypot(R, G);
  const rod = { wind: v6, R, G, Gamma: R / G, theta_b: thb, A0, orbits: [] };
  for (let i = 0; i < 12; i++) rod.orbits.push(section(R, G, thb + 0.05 + i * (1.95 - thb - 0.05) / 11, 0, 200, PT));   // rings in the bowl
  rod.orbits.push(section(R, G, 2.3, 0, 1500, PT)); rod.orbits.push(section(R, G, thb, 19.5, 1500, PT));            // the chaotic layer
  for (const w of [21.5, 24.5, 28, -21.5, -24.5, -28]) rod.orbits.push(section(R, G, thb, w, 200, PT));             // tumbling right over
  // the edge of chaos predicted: the hilltop's height A = sqrt(R^2 - 2RG sin(phi) + G^2) runs from R - G to R + G once per turn;
  // a swing whose action stays below the lowest hilltop's separatrix action 8 sqrt(R - G)/pi never reaches the top, one above the
  // highest one's (4 sqrt(R + G)/pi for a rotation) always clears it. Drawn in the frozen landscape at phi = 0, where A = A0.
  const Jin = 8 * Math.sqrt(R - G) / Math.PI, Jout = 4 * Math.sqrt(R + G) / Math.PI;
  const aIn = bisect(a => Jlib(A0, a) - Jin, 1e-6, Math.PI - 1e-6);
  const Eout = bisect(E => Jrot(A0, E) - Jout, A0 * (1 + 1e-12), 20 * A0);
  rod.pred = { J_in: Jin, J_out: Jout, amp_in: aIn, w_in: 2 * Math.sqrt(A0) * Math.sin(aIn / 2), E_out: Eout, w_out: Math.sqrt(2 * (Eout + A0)),
    right: thb + aIn, left: thb - aIn };
  // the edge of chaos measured: largest exponent per turn (50 turns let pass, 400 measured) along two lines through the bowl's bottom
  const THR = 0.2, scan = (pairs) => pairs.map(([t, w]) => [t, w, drivenLyap(R, G, 0, t, w, 400, PT)]);
  const lin = (a, b, n) => Array.from({ length: n }, (_, i) => a + (b - a) * i / (n - 1));
  const right = scan(lin(1.7, 2.4, 36).map(t => [t, 0])), left = scan(lin(-2.2, -2.9, 36).map(t => [t, 0]));
  const up = scan(lin(14, 22, 33).map(w => [thb, w])), down = scan(lin(-14, -22, 33).map(w => [thb, w]));
  const firstChaos = arr => arr.findIndex(r => r[2] > THR);
  const edge = (arr, j) => { const i = firstChaos(arr); return [arr[i - 1][j], arr[i][j]]; };              // last regular, first chaotic
  const lastChaos = arr => { let i = arr.length - 1; while (arr[i][2] <= THR) i--; return [arr[i][1], arr[i + 1][1]]; }; // last chaotic, first regular beyond
  rod.meas = { threshold: THR, right: edge(right, 0), left: edge(left, 0), w_in_up: edge(up, 1), w_in_down: edge(down, 1),
    w_out_up: lastChaos(up), w_out_down: lastChaos(down), scans: { right, left, up, down } };
  // the period of a free swing of amplitude a in the bowl A, in turns: T = 4 K(sin^2(a/2))/sqrt(A) / (2 pi)
  rod.period_turns = [0.5, 1, 2, 2.5, 3, 3.1].map(a => [a, 4 * KE(Math.sin(a / 2) ** 2)[0] / Math.sqrt(A0) / (2 * Math.PI)]);
  out.poincare = { phase: 'phi = 0: the first arm horizontal, rising', perTurn: PT, equal: eq, rod };
  console.log(`sections in ${((Date.now() - T1) / 1000).toFixed(1)} s; predicted`, rod.pred, 'measured', { ...rod.meas, scans: undefined });
}
fs.writeFileSync(path.join(__dirname, '..', 'data', 'L0_double.json'), JSON.stringify(out));
console.log('free: Lyapunov', out.free.lyap_per_s.toFixed(3), '/s, energy drift', out.free.energy_drift_J.toExponential(2), 'J');
for (const k of ['equal_arms', 'rod_63m']) console.log(k, out.driven[k].sweep.map(r => `${r.Gamma}:${r.max.toFixed(3)}(${r.n_chaotic})`).join(' '));
for (const r of out.turbine) console.log(`${r.wind} m/s Gamma ${r.Gamma.toFixed(2)}: unbraked max ${r.unbraked_max.toFixed(4)}, braked max ${r.braked_max.toFixed(3)} per turn`);
console.log('step check', out.driven.step_check, 'reduction', out.reduction);
console.log(`data/L0_double.json in ${((Date.now() - T0) / 1000).toFixed(1)} s`);
