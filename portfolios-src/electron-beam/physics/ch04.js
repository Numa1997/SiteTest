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

  const NOFOCUS = 'no focus on the wafer. Even the strongest excitation of a lens with one crossing (ω = 2) does not bring the ray back to the axis this close to the lens centre. Move the wafer further from the centre or the object further away.';
  function focusB0(a, eta, u, wd) {
    let lo = 0, hi = Math.sqrt(3 / eta) / a;
    if (paraxial(hi, a, eta, -u, wd, 0, 1)[0] > 0) throw new Error(NOFOCUS);
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

  // Labels that keep clear of the drawing: every line a label must not touch is registered as points (CSS px), every placed label and
  // every solid part as a box; a label goes to the first of its candidate places ([x, y, align, ...]) whose box, grown by a margin,
  // holds no point, meets no box and stays inside the bounds (the canvas unless given). put returns the box and the place used.
  function labels(ctx, w, h) {
    const P = [], Bx = [];
    const seg = (x0, y0, x1, y1) => { const n = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0) / 2)); for (let i = 0; i <= n; i++) P.push(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); };
    const box = (t, c) => { ctx.textAlign = c[2] || 'left'; const m = ctx.measureText(t); return [c[0] - m.actualBoundingBoxLeft, c[1] - m.actualBoundingBoxAscent, c[0] + m.actualBoundingBoxRight, c[1] + m.actualBoundingBoxDescent]; };
    const free = (b, m, r) => {
      if (b[0] < r[0] + 1 || b[1] < r[1] + 1 || b[2] > r[2] - 1 || b[3] > r[3] - 1) return false;
      for (let i = 0; i < P.length; i += 2) if (P[i] > b[0] - m && P[i] < b[2] + m && P[i + 1] > b[1] - m && P[i + 1] < b[3] + m) return false;
      return Bx.every(c => b[2] + m <= c[0] || c[2] + m <= b[0] || b[3] + m <= c[1] || c[3] + m <= b[1]);
    };
    return {
      line(xy) { for (let i = 2; i < xy.length; i += 2) seg(xy[i - 2], xy[i - 1], xy[i], xy[i + 1]); if (xy.length === 2) P.push(xy[0], xy[1]); },
      block(b) { Bx.push(b); },
      free: (b, m = 3, r = [0, 0, w, h]) => free(b, m, r),
      put(t, cands, m = 3, r = [0, 0, w, h]) {
        const c = cands.find(c => free(box(t, c), m, r)) || cands[0], b = box(t, c);
        ctx.fillText(t, c[0], c[1]); Bx.push(b); return [b, c];
      },
    };
  }

  // the drawing: the lens (coil and pole pieces) in section, the field B(z) on the axis, and the axial ray from the object to the wafer;
  // a key along the bottom edge names the ray and the field, so that no label sits on a line
  function draw(ctx, w, h, p, out) {
    ctx.clearRect(0, 0, w, h);
    const rec = out.lens_ray, a = p.a_lens, lab = labels(ctx, w, h);
    ctx.font = "11px 'IBM Plex Mono', monospace";
    const H = h - 40;                                                    // the drawing above, the key in the last 40 px
    // horizontal axis: z from -6a to WD + a on a linear scale (the object is far to the left; its ray enters from the edge)
    const zl = -Math.max(6 * a, 1.2 * p.WD), zr = p.WD * 1.15 + a, L = 16, R = w - 16;
    const X = z => L + (z - zl) / (zr - zl) * (R - L);
    // coil and pole pieces (drawn, not to scale) at the top and the bottom; the ray's height A keeps it clear of the coil's label
    const ch = Math.max(14, H * 0.13), cw = Math.max(16, X(1.6 * a) - X(-1.6 * a)), yAx = H / 2, A = yAx - (8 + ch + 24);
    ctx.fillStyle = '#efe4c8'; ctx.strokeStyle = '#3a322e'; ctx.lineWidth = 1;
    for (const y of [8, H - 8 - ch]) { ctx.fillRect(X(0) - cw / 2, y, cw, ch); ctx.strokeRect(X(0) - cw / 2, y, cw, ch); lab.block([X(0) - cw / 2, y, X(0) + cw / 2, y + ch]); }
    // the field on the axis, dashed, its peak at 0.9 of the ray's height
    const fz = []; for (let i = 0; i <= 200; i++) { const z = zl + (zr - zl) * i / 200; fz.push(X(z), yAx - 0.9 * A * glaser(z, 1, a)[0]); }
    ctx.strokeStyle = '#8b8079'; ctx.setLineDash([4, 3]); ctx.beginPath(); for (let i = 0; i < fz.length; i += 2) i ? ctx.lineTo(fz[i], fz[i + 1]) : ctx.moveTo(fz[i], fz[i + 1]); ctx.stroke(); ctx.setLineDash([]);
    lab.line(fz);
    // axis and wafer
    ctx.strokeStyle = '#d9d0c2'; ctx.beginPath(); ctx.moveTo(L, yAx); ctx.lineTo(R, yAx); ctx.stroke(); lab.line([L, yAx, R, yAx]);
    const xw = X(p.WD), hw = 0.6 * A;
    ctx.fillStyle = '#3a322e'; ctx.fillRect(xw - 2, yAx - hw, 4, 2 * hw); lab.block([xw - 2, yAx - hw, xw + 2, yAx + hw]);
    // the ray (and its mirror image), scaled to the largest excursion in view
    let rmax = 0; for (let i = 0; i < rec.length; i += 2) if (rec[i] >= zl) rmax = Math.max(rmax, Math.abs(rec[i + 1]));
    ctx.strokeStyle = '#7a1f2b'; ctx.lineWidth = 1.8;
    for (const sgn of [1, -1]) {
      const xy = []; for (let i = 0; i < rec.length; i += 2) if (rec[i] >= zl) xy.push(X(rec[i]), yAx - sgn * A * rec[i + 1] / rmax);
      ctx.beginPath(); for (let i = 0; i < xy.length; i += 2) i ? ctx.lineTo(xy[i], xy[i + 1]) : ctx.moveTo(xy[i], xy[i + 1]); ctx.stroke();
      lab.line(xy);
    }
    ctx.lineWidth = 1;
    // the two labels in the drawing, each at the first free place of a few
    ctx.fillStyle = '#5a504b';
    lab.put('coil, NI = ' + core.fmt(out.NI, 3) + ' A', [[X(0), 8 + ch + 14, 'center'], [X(0), H - 8 - ch - 6, 'center'], [X(0) + cw / 2 + 6, 8 + ch - 2, 'left'], [X(0) - cw / 2 - 6, 8 + ch - 2, 'right']]);
    lab.put('wafer', [[xw, yAx - hw - 6, 'center'], [xw + 2, yAx - hw - 6, 'right'], [xw, yAx + hw + 14, 'center'], [xw + 2, yAx + hw + 14, 'right'], [xw - 6, yAx - hw + 8, 'right'], [xw - 6, yAx + hw - 2, 'right']]);
    // the key: what the wine line and the dashed line are
    const k1 = H + 16, k2 = H + 32;
    ctx.strokeStyle = '#7a1f2b'; ctx.lineWidth = 1.8; ctx.beginPath(); ctx.moveTo(L, k1 - 4); ctx.lineTo(L + 22, k1 - 4); ctx.stroke();
    ctx.strokeStyle = '#8b8079'; ctx.lineWidth = 1; ctx.setLineDash([4, 3]); ctx.beginPath(); ctx.moveTo(L, k2 - 4); ctx.lineTo(L + 22, k2 - 4); ctx.stroke(); ctx.setLineDash([]);
    ctx.textAlign = 'left'; ctx.fillStyle = '#5a504b'; ctx.fillText('ray ← from the object, ' + core.fmt(p.u_obj * 1e3, 3) + ' mm', L + 30, k1);
    ctx.fillStyle = '#8b8079'; ctx.fillText('B(z) on the axis', L + 30, k2);
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
      aspect: '4 / 3', aspectPhone: '1 / 1',
      caption: 'The objective lens in section: coil (drawn, not to scale), the bell-shaped field on the axis (dashed) and the axial ray from the object to the wafer. The excitation NI is solved so that the ray meets the axis at the wafer; where no excitation with a single crossing can do that, the simulation says so instead of drawing. The lens is computed at the landing voltage: this lens model has no retarding field.',
    },
    compute, draw, paraxial, ray3d, glaser, focusB0,
    setSteps: n => { NSTEP = n; },
  };
});
