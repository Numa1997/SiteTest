/* The Electron Beam, from Tip to Measurement · physics/ch04.js
   Chapter 4, the lens: a round magnetic lens with Glaser's bell-shaped field, focused on the wafer. Pure module (physics/core.js
   pattern); mirrored line by line by ref/ch04.py.

     B(z) = B0 / (1 + (z/a)^2),  B0 = mu0 NI / (pi a)              Ampere: the integral of B along the axis is mu0 NI
     paraxial ray in the rotating frame:  r'' = -eta B^2 r,  eta = e / (8 m V*)
     field off the axis (div B = 0, curl B = 0):  B_z = B - r^2 B''/4,  B_r = -r B'/2 + r^3 B'''/16
     exact ray in a static magnetic field with z as the variable (the speed is constant):
       x'' = (q/p) s [x'y' B_x - (1 + x'^2) B_y + y' B_z],  y'' = (q/p) s [(1 + y'^2) B_x - x'y' B_y - x' B_z],  s = sqrt(1 + x'^2 + y'^2)
   All integrals are RK4 in t with z = a tan t (NSTEP steps), so the steps crowd into the lens.
   The lens centre is at z = 0, the object (the crossover or source image the lens demagnifies) at z = -u_obj, the wafer at z = +WD.
   NI is the excitation that brings the axial ray back to the axis at the wafer (bisection). C_s comes from rays traced at two image angles
   (2 and 4 mrad) with the linear (defocus) part removed by a ray of tiny angle; C_c from the paraxial ray at V*(1 +- 1e-4). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./core.js'));
  else { root.EB = root.EB || {}; root.EB.ch04 = factory(root.EB.core); }
})(typeof self !== 'undefined' ? self : this, function (core) {
  'use strict';
  const { C } = core;
  const E = C.e, ME = C.m_e, MU0 = C.mu0;
  let NSTEP = 6000;
  const vstar = V => V * (1 + E * V / (2 * ME * C.c * C.c));

  function glaser(z, B0, a) {
    const u = z / a, q = 1 + u * u;
    return [B0 / q, -2 * B0 * u / (a * q * q), B0 * (6 * u * u - 2) / (a * a * q * q * q), 24 * B0 * u * (1 - u * u) / (a * a * a * q * q * q * q)];
  }
  function grid(a, z0, z1) { const t0 = Math.atan(z0 / a), t1 = Math.atan(z1 / a); return [t0, (t1 - t0) / NSTEP]; }

  function paraxial(B0, a, eta, z0, z1, r0, rp0, record) {
    const [t0, h] = grid(a, z0, z1);
    const f = (t, y) => { const z = a * Math.tan(t), dz = a / (Math.cos(t) * Math.cos(t)), B = B0 / (1 + (z / a) * (z / a)); return [y[1] * dz, -eta * B * B * y[0] * dz]; };
    let y = [r0, rp0], t = t0;
    for (let i = 0; i < NSTEP; i++) {
      if (record && i % 20 === 0) record.push(a * Math.tan(t), y[0]);
      const k1 = f(t, y);
      const k2 = f(t + h / 2, [y[0] + h / 2 * k1[0], y[1] + h / 2 * k1[1]]);
      const k3 = f(t + h / 2, [y[0] + h / 2 * k2[0], y[1] + h / 2 * k2[1]]);
      const k4 = f(t + h, [y[0] + h * k3[0], y[1] + h * k3[1]]);
      y = [y[0] + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]), y[1] + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])];
      t += h;
    }
    if (record) record.push(a * Math.tan(t), y[0]);
    return y;
  }

  function ray3d(B0, a, qp, z0, z1, xp0) {
    const [t0, h] = grid(a, z0, z1);
    const f = (t, s) => {
      const [x, y, xp, yp] = s, z = a * Math.tan(t), dz = a / (Math.cos(t) * Math.cos(t));
      const [B, B1, B2, B3] = glaser(z, B0, a), r2 = x * x + y * y;
      const Bz = B - r2 * B2 / 4, Brr = -B1 / 2 + r2 * B3 / 16, Bx = Brr * x, By = Brr * y;
      const w = Math.sqrt(1 + xp * xp + yp * yp);
      const xpp = qp * w * (xp * yp * Bx - (1 + xp * xp) * By + yp * Bz);
      const ypp = qp * w * ((1 + yp * yp) * Bx - xp * yp * By - xp * Bz);
      return [xp * dz, yp * dz, xpp * dz, ypp * dz];
    };
    let s = [0, 0, xp0, 0], t = t0;
    const add = (u, k, c) => [u[0] + c * k[0], u[1] + c * k[1], u[2] + c * k[2], u[3] + c * k[3]];
    for (let i = 0; i < NSTEP; i++) {
      const k1 = f(t, s), k2 = f(t + h / 2, add(s, k1, h / 2)), k3 = f(t + h / 2, add(s, k2, h / 2)), k4 = f(t + h, add(s, k3, h));
      s = [0, 1, 2, 3].map(i => s[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]));
      t += h;
    }
    return [s[0], s[1]];
  }

  function focusB0(a, eta, u, wd) {
    let lo = 0, hi = Math.sqrt(3 / eta) / a;
    for (let i = 0; i < 60; i++) {
      const mid = (lo + hi) / 2, r = paraxial(mid, a, eta, -u, wd, 0, 1)[0];
      if (r > 0) lo = mid; else hi = mid;
    }
    return (lo + hi) / 2;
  }

  function solve(p, record) {
    const a = p.a_lens, u = p.u_obj, wd = p.WD, Vs = vstar(p.V_land);
    const eta = E / (8 * ME * Vs), pmom = Math.sqrt(2 * ME * E * Vs);
    const B0 = focusB0(a, eta, u, wd), NI = B0 * Math.PI * a / MU0;
    const rpi = paraxial(B0, a, eta, -u, wd, 0, 1, record)[1], M = 1 / Math.abs(rpi);
    const zfar = 2000 * a, f = -1 / paraxial(B0, a, eta, -zfar, zfar, 1, 0)[1];
    const omega = Math.sqrt(1 + eta * B0 * B0 * a * a);
    const theta = Math.sqrt(E / (8 * ME * Vs)) * B0 * a * (Math.atan(wd / a) + Math.atan(u / a));
    const qp = -E / pmom, eps = 1e-9, [xe, ye] = ray3d(B0, a, qp, -u, wd, eps);
    const miss = [2e-3, 4e-3].map(ai => { const ao = ai * M, [x, y] = ray3d(B0, a, qp, -u, wd, ao), k = ao / eps; return Math.hypot(x - k * xe, y - k * ye); });
    const a1 = 2e-3, a2 = 4e-3;
    const Cs = (miss[0] * Math.pow(a2, 5) - miss[1] * Math.pow(a1, 5)) / (Math.pow(a1, 3) * Math.pow(a2, 5) - Math.pow(a2, 3) * Math.pow(a1, 5));
    const d = 1e-4, rpl = paraxial(B0, a, eta / (1 + d), -u, wd, 0, 1)[0], rmi = paraxial(B0, a, eta / (1 - d), -u, wd, 0, 1)[0];
    const Cc = Math.abs((rpl - rmi) / (2 * d)) * M;
    return { NI, B_0: B0, M, f, C_s: Cs, C_c: Cc, theta_rot: theta, omega_G: omega, lens_ray: record };
  }
  const compute = p => solve(p, []);

  // the drawing: the lens (coil and pole pieces) in section, the field B(z) on a strip, and the axial ray from the object to the wafer
  function draw(ctx, w, h, p, out) {
    ctx.clearRect(0, 0, w, h);
    const rec = out.lens_ray, a = p.a_lens;
    // horizontal axis: z from -6a to WD + a on a linear scale (the object is far to the left; its ray enters from the edge)
    const zl = -Math.max(6 * a, 1.2 * p.WD), zr = p.WD * 1.15 + a, L = 30, R = w - 20;
    const X = z => L + (z - zl) / (zr - zl) * (R - L);
    const yAx = h * 0.58, sc = (h * 0.30);
    let rmax = 0; for (let i = 0; i < rec.length; i += 2) if (rec[i] >= zl) rmax = Math.max(rmax, Math.abs(rec[i + 1]));
    ctx.font = "11px 'IBM Plex Mono', monospace";
    // coil and pole pieces (drawn, not to scale)
    ctx.fillStyle = '#efe4c8'; ctx.strokeStyle = '#3a322e'; ctx.lineWidth = 1;
    const cw = Math.max(16, X(1.6 * a) - X(-1.6 * a));
    ctx.fillRect(X(0) - cw / 2, 8, cw, h * 0.16); ctx.strokeRect(X(0) - cw / 2, 8, cw, h * 0.16);
    ctx.fillRect(X(0) - cw / 2, h - 8 - h * 0.16, cw, h * 0.16); ctx.strokeRect(X(0) - cw / 2, h - 8 - h * 0.16, cw, h * 0.16);
    ctx.fillStyle = '#5a504b'; ctx.textAlign = 'center'; ctx.fillText('coil, NI = ' + core.fmt(out.NI, 3) + ' A', X(0), 8 + h * 0.16 + 13);
    // field strip
    ctx.strokeStyle = '#8b8079'; ctx.setLineDash([4, 3]); ctx.beginPath();
    for (let i = 0; i <= 200; i++) { const z = zl + (zr - zl) * i / 200, y = yAx - sc * 0.9 * glaser(z, 1, a)[0]; i ? ctx.lineTo(X(z), y) : ctx.moveTo(X(z), y); }
    ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = '#8b8079'; ctx.textAlign = 'left'; ctx.fillText('B(z), dashed', X(a) + 6, yAx - sc * 0.9);
    // axis and wafer
    ctx.strokeStyle = '#d9d0c2'; ctx.beginPath(); ctx.moveTo(L, yAx); ctx.lineTo(R, yAx); ctx.stroke();
    ctx.fillStyle = '#3a322e'; ctx.fillRect(X(p.WD) - 2, yAx - sc * 0.6, 4, sc * 1.2);
    ctx.fillStyle = '#5a504b'; ctx.textAlign = 'left'; ctx.fillText('wafer', X(p.WD) + 6, yAx + 4);
    // the ray (and its mirror image), scaled to the largest excursion in view
    ctx.strokeStyle = '#7a1f2b'; ctx.lineWidth = 1.8;
    for (const sgn of [1, -1]) {
      ctx.beginPath(); let first = true;
      for (let i = 0; i < rec.length; i += 2) { if (rec[i] < zl) continue; const xx = X(rec[i]), yy = yAx - sgn * sc * rec[i + 1] / rmax; first ? ctx.moveTo(xx, yy) : ctx.lineTo(xx, yy); first = false; }
      ctx.stroke();
    }
    ctx.fillStyle = '#5a504b'; ctx.textAlign = 'left'; ctx.fillText('← from the object, ' + core.fmt(p.u_obj * 1e3, 3) + ' mm', L, yAx - sc * 0.55);
  }

  return {
    id: 'ch04',
    inputs: ['a_lens', 'u_obj', 'WD', 'V_land'],
    outputs: ['NI', 'B_0', 'M', 'f', 'C_s', 'C_c', 'theta_rot', 'omega_G', 'lens_ray'],
    tolerance: { rel: 1e-9, abs: 1e-14, note: 'the same RK4 on the same grid in float64; C_s is a small difference of traced positions (agrees to about 1e-10); the ray passes through zero at the wafer, where only an absolute floor of 1e-14 m is meaningful' },
    cases: [{}, { WD: 5e-3 }, { a_lens: 1e-3, WD: 2e-3, V_land: 3000 }, { V_land: 30000 }],
    ui: {
      controls: ['V_land', 'a_lens', 'WD', 'u_obj'],
      readouts: ['NI', 'f', 'C_s', 'C_c', 'M', 'theta_rot'],
      aspect: '4 / 3', aspectPhone: '4 / 3',
      caption: 'The objective lens in section: coil (drawn, not to scale), the bell-shaped field on the axis (dashed) and the axial ray from the object to the wafer. The excitation NI is solved so that the ray meets the axis at the wafer.',
    },
    compute, draw, paraxial, ray3d, glaser, focusB0,
    setSteps: n => { NSTEP = n; },
  };
});
