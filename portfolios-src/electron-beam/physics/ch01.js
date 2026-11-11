/* The Electron Beam, from Tip to Measurement · physics/ch01.js
   Chapter 1, a free electron in fields: Thomson's cathode-ray tube, reduced to its physics. One electron (charge -e, mass m) enters
   uniform fields at the origin with speed v_0 at the angle theta_0 to B, in the x-z plane; E points along +y, B along +z (contract.json).
   It is followed for the time t_run with the relativistic equation of motion (text, chapter 1, section 4)

       d(gamma m v)/dt = q (E + v x B),   q = -e,   gamma = (1 - v^2/c^2)^(-1/2),

   written for u = gamma v:   dr/dt = u/gamma,   du/dt = (q/m)(E + (u/gamma) x B),   gamma = sqrt(1 + u^2/c^2).
   Two integrators, chosen by `integrator`:
     'boris'  the Boris pusher (J. P. Boris, Proc. 4th Conf. Numerical Simulation of Plasmas, 1970): half electric kick, rotation by
              u' = u + u x t, u+ = u + u' x s with t = (q h/2m) B/gamma, s = 2t/(1 + t^2), half electric kick; u at half steps, r at whole steps;
     'rk4'    the classical fourth-order Runge-Kutta step (text, section 8).
   Outputs: the gyroradius and cyclotron frequency of the motion about B, the relative change of the kinetic energy over the run,
   the stored path (x, y, z interleaved, at most 301 points), the end position and the direction of the velocity at the end.
   energy_drift = (K_end - K_start)/K_start with K = (gamma - 1) m c^2. For E = 0 it is the integrator's error alone; with E != 0 it also holds
   the work the field does. Mirrored line by line by ref/ch01.py (checks/check_parity.py). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./core.js'));
  else { root.EB = root.EB || {}; root.EB.ch01 = factory(root.EB.core); }
})(typeof self !== 'undefined' ? self : this, function (core) {
  'use strict';
  const { C } = core;
  const q = -C.e;
  const MAX_STEPS = 400000, MAX_POINTS = 300;

  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
  const scale = (a, s) => [a[0] * s, a[1] * s, a[2] * s];
  const gammaOf = u => Math.sqrt(1 + dot(u, u) / (C.c * C.c));
  // gamma - 1 without the cancellation of gamma - 1: u^2/(c^2 (1 + gamma)); the energy change of a run is a ratio of two of these
  const gammaM1 = u => dot(u, u) / (C.c * C.c * (1 + gammaOf(u)));

  // Boris: advance u by h in fields E, B held at the particle's position
  function borisKick(u, E, B, h) {
    const a = q * h / (2 * C.m_e);
    const um = add(u, scale(E, a));                       // half electric kick
    const t = scale(B, a / gammaOf(um));                  // tan(phi/2) along B
    const s = scale(t, 2 / (1 + dot(t, t)));
    const up = add(um, cross(um, t));
    const uplus = add(um, cross(up, s));                  // a turn of u by the angle phi = 2 atan|t|: its length is unchanged
    return add(uplus, scale(E, a));                       // second half electric kick
  }
  function rhs(u, E, B) {
    const g = gammaOf(u), v = scale(u, 1 / g);
    return [v, scale(add(E, cross(v, B)), q / C.m_e)];
  }
  function rk4Step(r, u, h, E, B) {
    const k1 = rhs(u, E, B);
    const k2 = rhs(add(u, scale(k1[1], h / 2)), E, B);
    const k3 = rhs(add(u, scale(k2[1], h / 2)), E, B);
    const k4 = rhs(add(u, scale(k3[1], h)), E, B);
    const w = (a, b, c, d) => add(add(a, scale(add(b, c), 2)), d);
    return [add(r, scale(w(k1[0], k2[0], k3[0], k4[0]), h / 6)), add(u, scale(w(k1[1], k2[1], k3[1], k4[1]), h / 6))];
  }

  function compute(p) {
    const E = [0, p.E_field, 0], B = [0, 0, p.B_field];
    const g0 = 1 / Math.sqrt(1 - (p.v_0 / C.c) * (p.v_0 / C.c));
    let u = [g0 * p.v_0 * Math.sin(p.theta_0), 0, g0 * p.v_0 * Math.cos(p.theta_0)];
    const u0 = u.slice();
    const n = Math.min(MAX_STEPS, Math.max(1, Math.ceil(p.t_run / p.dt)));
    const h = p.t_run / n;
    const stride = Math.max(1, Math.ceil(n / MAX_POINTS));
    let r = [0, 0, 0];
    const path = [0, 0, 0];
    let uh = null;
    if (p.integrator === 'boris') uh = borisKick(u, E, B, -h / 2);
    for (let i = 1; i <= n; i++) {
      if (p.integrator === 'boris') {
        uh = borisKick(uh, E, B, h);
        r = add(r, scale(uh, h / gammaOf(uh)));
      } else {
        [r, u] = rk4Step(r, u, h, E, B);
      }
      if (i % stride === 0 || i === n) path.push(r[0], r[1], r[2]);
    }
    if (p.integrator === 'boris') u = borisKick(uh, E, B, h / 2);   // velocity at the end time, from the half-step value
    const g1 = gammaOf(u);
    const v = scale(u, 1 / g1);
    return {
      r_g: p.B_field > 0 ? g0 * C.m_e * p.v_0 * Math.sin(p.theta_0) / (C.e * p.B_field) : 0,
      omega_c: C.e * p.B_field / (g0 * C.m_e),
      energy_drift: gammaM1(u) / gammaM1(u0) - 1,
      trajectory: path,
      x_end: r[0], y_end: r[1], z_end: r[2],
      theta_end: Math.atan2(v[1], v[0]),
    };
  }

  // the canvas: the path seen from two sides, one common scale, start and end marked. A view's title stands above its frame and
  // breaks after the colon when it is wider than the view; the key below breaks into two lines when it is wider than the canvas.
  function draw(ctx, w, h, p, out) {
    const tr = out.trajectory, np = tr.length / 3;
    ctx.clearRect(0, 0, w, h);
    ctx.font = "11px 'IBM Plex Mono', monospace";
    const views = [['x', 'y', 'top (x, y): E up, B out'], ['x', 'z', 'side (x, z): B up']];
    const idx = { x: 0, y: 1, z: 2 };
    const pad = 12, gap = 14, vw = (w - 2 * pad - gap) / 2, lh = 14;
    const titles = views.map(v => ctx.measureText(v[2]).width <= vw ? [v[2]] : [v[2].slice(0, v[2].indexOf(':') + 1), v[2].slice(v[2].indexOf(':') + 2)]);
    const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
    for (let i = 0; i < np; i++) for (let k = 0; k < 3; k++) { lo[k] = Math.min(lo[k], tr[3 * i + k]); hi[k] = Math.max(hi[k], tr[3 * i + k]); }
    const span = Math.max(hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2], 1e-9);
    const key = ['black: start   green: end', 'field of view ' + core.fmt(span / 0.86 * 1e3, 2) + ' mm'];
    const keyLines = ctx.measureText(key.join('   ')).width <= w - 2 * pad ? [key.join('   ')] : key;
    const top = 8 + lh * Math.max(...titles.map(t => t.length)), bottom = 8 + lh * keyLines.length, vh = h - top - bottom;
    const sc = Math.min(vw, vh) * 0.86 / span;
    views.forEach((vd, j) => {
      const x0 = pad + j * (vw + gap), a = idx[vd[0]], b = idx[vd[1]];
      ctx.fillStyle = '#fff'; ctx.strokeStyle = '#cdc1ae'; ctx.lineWidth = 1;
      ctx.__nocollide = true;                                   // the frame and the axes are ground (checks/check_figures.cjs)
      ctx.fillRect(x0, top, vw, vh); ctx.strokeRect(x0 + 0.5, top + 0.5, vw - 1, vh - 1);
      const cx = x0 + vw / 2 - sc * (lo[a] + hi[a]) / 2, cy = top + vh / 2 + sc * (lo[b] + hi[b]) / 2;
      const X = t => cx + sc * t, Y = t => cy - sc * t;
      ctx.strokeStyle = '#e6dfd2';
      ctx.beginPath(); ctx.moveTo(x0, Y(0)); ctx.lineTo(x0 + vw, Y(0)); ctx.moveTo(X(0), top); ctx.lineTo(X(0), top + vh); ctx.stroke();
      ctx.__nocollide = false;
      ctx.fillStyle = '#6f655f'; ctx.textAlign = 'left';
      titles[j].forEach((t, i) => ctx.fillText(t, x0, top - 6 - lh * (titles[j].length - 1 - i)));
      ctx.strokeStyle = '#7a1f2b'; ctx.lineWidth = 2; ctx.beginPath();
      for (let i = 0; i < np; i++) { const px = X(tr[3 * i + a]), py = Y(tr[3 * i + b]); if (i) ctx.lineTo(px, py); else ctx.moveTo(px, py); }
      ctx.stroke();
      ctx.fillStyle = '#1c1518'; ctx.beginPath(); ctx.arc(X(0), Y(0), 3.5, 0, 2 * Math.PI); ctx.fill();
      ctx.fillStyle = '#3a8a5a'; ctx.beginPath(); ctx.arc(X(tr[3 * (np - 1) + a]), Y(tr[3 * (np - 1) + b]), 3.5, 0, 2 * Math.PI); ctx.fill();
    });
    ctx.fillStyle = '#6f655f'; ctx.textAlign = 'right';
    keyLines.forEach((t, i) => ctx.fillText(t, w - pad, h - 5 - lh * (keyLines.length - 1 - i)));
  }

  return {
    id: 'ch01',
    inputs: ['E_field', 'B_field', 'v_0', 'theta_0', 'dt', 'integrator', 't_run'],
    outputs: ['r_g', 'omega_c', 'energy_drift', 'trajectory', 'x_end', 'y_end', 'z_end', 'theta_end'],
    // both sides are float64 with the same algorithm (see the note)
    tolerance: { rel: 1e-12, abs: 1e-12, note: 'energy_drift is a difference of two nearly equal numbers: rounding accumulated over some 4000 steps differs by up to 1e-13 between the two orderings of the same arithmetic, so the absolute floor is 1e-12; every other output agrees to 1e-15 relative' },
    cases: [
      {},
      { integrator: 'rk4' },
      { E_field: 0, B_field: 0.01, v_0: 2.6446533679e7, theta_0: 1.2, dt: 2.2e-11, t_run: 7.17e-8 },
      { E_field: 0, B_field: 0.01, v_0: 2.6446533679e7, theta_0: 1.2, dt: 2.2e-11, t_run: 7.17e-8, integrator: 'rk4' },
      { E_field: 6666.666666666667, B_field: 0, v_0: 2.6446533679e7, theta_0: 1.5707963267948966, dt: 2e-12, t_run: 1.89e-9 },
      { E_field: 6666.666666666667, B_field: 2.5208e-4, v_0: 2.6446533679e7, theta_0: 1.5707963267948966, dt: 2e-12, t_run: 1.89e-9, integrator: 'rk4' },
      { E_field: 0, B_field: 0.004, v_0: 2.6446533679e7, theta_0: 0.06, dt: 4e-12, t_run: 2.4e-8 },
      { E_field: 5e5, B_field: 0.05, v_0: 2.0e8, theta_0: 0.7, dt: 1e-12, t_run: 4e-9 },
    ],
    ui: {
      controls: ['E_field', 'B_field', 'v_0', 'theta_0', 't_run', 'dt', 'integrator'],
      readouts: ['r_g', 'omega_c', 'energy_drift', 'x_end', 'y_end', 'z_end', 'theta_end'],
      aspect: '16 / 7', aspectPhone: '4 / 3',
      title: 'An electron in uniform E and B',
      caption: 'One electron in a uniform electric field (along y) and a uniform magnetic field (along z), followed by the integrator chosen below. B only, at a right angle to the velocity: a circle. E only: a parabola. E = vB at a right angle: a straight line, Thomson’s balance. B at a small angle to the velocity: a helix. The energy error is the change of the kinetic energy over the run; for E = 0 it is the integrator’s error.',
    },
    compute,
    draw,
  };
});
