/* Fig. 12: drawing the cart and the pint of stout (canvas 2D) through a perspective camera. Reads the state of a
 * StoutCart.World; computes nothing physical. The surface of the stout is the liquid column height computed by the
 * solver (Fluid.columnHeights), interpolated smoothly (bicubic Catmull–Rom) for the picture, read on a polar grid over
 * the whole glass (the half that is not solved is its mirror image), lit by one light, and seen by a pinhole camera
 * above and to the side that rides with the cart. The dark body of the drink takes its colour from the path length of
 * the view ray through it (Beer–Lambert). The creamy head is DRAWN, not simulated: a layer of constant thickness headH
 * laid on the simulated surface. Everything the picture places is written into the store (css px) with the camera's
 * constants, so the data panel can recompute each point from the projection. */
(function (root) {
  'use strict';
  const C = {
    paper: '#f5f1ea', ink: '#1c1518', muted: '#6b6166', accent: '#7a1f2b', line: 'rgba(28,21,24,0.85)',
    stoutDark: [14, 8, 7], stoutRuby: [96, 22, 16], head: [236, 225, 201], headShade: [196, 178, 146], glass: 'rgba(120,140,150,0.10)',
  };
  const lerp = (a, b, t) => a + (b - a) * t;
  const rgb = (c, a) => a == null ? `rgb(${c[0] | 0},${c[1] | 0},${c[2] | 0})` : `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a})`;
  const mix = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];

  function View(canvas, world, o) {
    o = o || {};
    this.cv = canvas; this.ctx = canvas.getContext('2d'); this.world = world;
    this.scale = o.scale || 2600;        // px per metre at the camera's target depth
    // the camera: looks down at elev, from the side at azim (negative: from the direction of travel, so the front wall is
    // near), from a distance dist, at the point (0, 0, targetZ) above the axle
    this.elev = (o.elevDeg != null ? o.elevDeg : 22) * Math.PI / 180;
    this.azim = (o.azimDeg != null ? o.azimDeg : -18) * Math.PI / 180;
    this.dist = o.dist || 2.2; this.targetZ = o.targetZ != null ? o.targetZ : 0.24;
    this.nr = o.nr || 16; this.nth = o.nth || 64;
    this.bodyW = 0.22; this.bodyD = 0.12; this.bodyH = 0.03; this.headH = o.headH != null ? o.headH : 0.012; this.carrierGap = 0.006; this.glassWall = 0.0025; this.glassBase = 0.006;
    this.roadW = 0.14;                   // the road ribbon, m across
    this.kappa = Math.log(2) / 0.006;    // Beer–Lambert: half the light left after 6 mm of stout (a drawing constant)
    this.light = (() => { const L = [-0.35, -0.55, 0.76], n = Math.hypot(...L); return L.map((v) => v / n); })();
    this.groundY = o.groundY || 0.80;    // fraction of canvas height where the road under the axle sits
    this.viewHeight = o.viewHeight || 0; // metres of scene shown top to bottom at the target depth (0: use scale)
    this.camX = null;
  }

  // The pinhole camera, as pure arithmetic from its constants (the page's checks repeat it). Points are given relative
  // to the cart: x along the road from the axle, y across (positive away from the viewer), z up from the road level.
  View.prototype.camera = function (W, Hc) {
    const s = this.scale, e = this.elev, a = this.azim, D = this.dist, zT = this.targetZ;
    const d = [Math.sin(a) * Math.cos(e), Math.cos(a) * Math.cos(e), -Math.sin(e)];   // from the camera to the target
    const r = [Math.cos(a), -Math.sin(a), 0];                                          // screen right
    const u = [Math.sin(a) * Math.sin(e), Math.cos(a) * Math.sin(e), Math.cos(e)];     // screen up (r × d)
    const Cp = [-D * d[0], -D * d[1], zT - D * d[2]];                                   // the camera's position
    const f = s * D, cx = W / 2;
    const v0 = [-Cp[0], -Cp[1], -Cp[2]];                                               // to the road point under the axle
    const cy = this.groundY * Hc + f * dot(v0, u) / dot(v0, d);                        // so that that point sits at groundY
    return { d, r, u, Cp, f, cx, cy };
  };
  View.prototype.project = function (cam, x, y, z) {
    const v = [x - cam.Cp[0], y - cam.Cp[1], z - cam.Cp[2]], dep = dot(v, cam.d);
    return [cam.cx + cam.f * dot(v, cam.r) / dep, cam.cy - cam.f * dot(v, cam.u) / dep, dep];
  };

  // The surface for the picture: the column heights h_ji (volume-exact per column) interpolated by a bicubic
  // Catmull–Rom spline, so that the sheet bends instead of stepping; it passes through every column value. y is folded
  // by the mirror plane. Beyond r1 = R(h) − 3.5 Δx the columns are cut by the wall and hold too few particles, so the
  // height is extended linearly along the radius from r1 and r1 − 3.5 Δx. (Measured at rest after 0.5 s, 4 mm: the ring at
  // the wall varies by 2.1 mm with this baseline, by 5.3 mm with Fluid.columnHeightAt's 2.5 and 1.5 Δx.)
  View.prototype.heightAt = function (x, y) {
    const f = this.world.fluid, dx = f.dx;
    if (f.modal) return f.heightAt(x, y);                        // the modal model's surface is already smooth: drawn exactly
    if (f.gpu) return f.columnHeightAt(x, y);                    // the GPU solver: the whole glass's column heights, as the probes read them
    y = Math.abs(y);
    const r = Math.hypot(x, y), r1 = f.Rz(Math.min(f.h0, f.zRim)) - 3.5 * dx, r2 = r1 - 3.5 * dx;
    if (r > r1) {
      const cx = x / r, cy = y / r, h1 = this.bicubic(cx * r1, cy * r1), h2 = this.bicubic(cx * r2, cy * r2);
      return h1 + (r - r1) * (h1 - h2) / (r1 - r2);
    }
    return this.bicubic(x, y);
  };
  View.prototype.bicubic = function (x, y) {
    const f = this.world.fluid, nx = f.nx, ny = f.ny, dx = f.dx, H = f.colH;
    const fx = (x - f.x0) / dx - 0.5, fy = y / dx - 0.5;
    const i = Math.floor(fx), j = Math.floor(fy), tx = fx - i, ty = fy - j;
    const at = (a, b) => { a = a < 0 ? 0 : a >= nx ? nx - 1 : a; b = b < 0 ? -b - 1 : b; b = b >= ny ? ny - 1 : b; return H[a + nx * b]; };
    const cr = (p0, p1, p2, p3, t) => 0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (3 * p1 - p0 - 3 * p2 + p3) * t * t * t);
    const rows = [];
    for (let b = -1; b <= 2; b++) rows.push(cr(at(i - 1, j + b), at(i, j + b), at(i + 1, j + b), at(i + 2, j + b), tx));
    return cr(rows[0], rows[1], rows[2], rows[3], ty);
  };

  // free-surface heights on the polar grid: h[ir][ith], ir = 0..nr (r = R ir / nr), ith over the full circle
  View.prototype.surface = function () {
    const f = this.world.fluid, R = f.Rz(Math.min(f.h0, f.zRim)), nr = this.nr, nth = this.nth, H = [];
    f.columnHeights();
    for (let ir = 0; ir <= nr; ir++) {
      const row = [], r = R * ir / nr;
      for (let it = 0; it < nth; it++) { const th = 2 * Math.PI * it / nth; row.push(this.heightAt(r * Math.cos(th), r * Math.sin(th))); }
      H.push(row);
    }
    const D = this.ds;
    if (D) {                                                     // what is drawn, as drawn: heights on the polar grid
      const e = D.get('eta_draw');
      for (let ir = 0; ir <= nr; ir++) for (let it = 0; it < nth; it++) e[ir * nth + it] = H[ir][it];
      D.touch('eta_draw');
      // the lean the readout shows is the solver's own reading at the wall (Fluid.columnHeightAt), as in the note's study
      const ef = f.columnHeightAt(R, 0), eb = f.columnHeightAt(-R, 0);
      D.set('eta_front', ef); D.set('eta_back', eb); D.set('dw', ef - eb);
    }
    return H;
  };

  View.prototype.draw = function () {
    const ctx = this.ctx, W = this.cv.width, Hc = this.cv.height, w = this.world, c = w.cart, f = w.fluid;
    ctx.setTransform(1, 0, 0, 1, 0, 0);                       // device pixels throughout
    const dpr = W / (this.cssW || W);
    if (this.viewHeight) this.scale = Hc / this.viewHeight;
    this.camX = c.x;                                           // the camera rides with the cart
    const cam = this.cam = this.camera(W, Hc), P = (x, y, z) => this.project(cam, x, y, z);
    const road = c.road, zr = (x) => road.zr(x + c.x);         // the road under the cart, x relative to the axle
    const D = this.ds;
    if (D) {
      D.set('scale', this.scale / dpr); D.set('cam_x', this.camX); D.set('elev', this.elev); D.set('azim', this.azim); D.set('cam_dist', this.dist); D.set('cam_zt', this.targetZ);
      D.set('focal', cam.f / dpr); D.set('cam_cx', cam.cx / dpr); D.set('cam_cy', cam.cy / dpr);
      const g0 = P(0, 0, 0), ax = P(0, -0.01, c.zw), bd = P(-0.08, -this.bodyD / 2, c.zb), gl = P(0, 0, c.zb + c.glassFloor + f.h0);
      D.set('ground_px', g0[1] / dpr); D.set('axle_px_x', ax[0] / dpr); D.set('axle_px_y', ax[1] / dpr);
      D.set('body_px_x', bd[0] / dpr); D.set('body_px_y', bd[1] / dpr); D.set('glass_px_x', gl[0] / dpr); D.set('glass_px_y', gl[1] / dpr);
      D.set('canvas_w', W / dpr); D.set('canvas_h', Hc / dpr);
    }
    ctx.fillStyle = C.paper; ctx.fillRect(0, 0, W, Hc);

    // the road: a ribbon roadW across following z_r(x), the wheel's track down its middle, ticks every 10 cm on the near edge
    const span = 0.5 * W / this.scale * 1.6 + 0.3, yN = -this.roadW / 2, yF = this.roadW / 2, step = 0.01;
    const edge = (y, from, to) => { for (let x = from; from < to ? x <= to : x >= to; x += from < to ? step : -step) { const p = P(x, y, zr(x)); ctx.lineTo(p[0], p[1]); } };
    ctx.beginPath(); { const p = P(-span, yN, zr(-span)); ctx.moveTo(p[0], p[1]); } edge(yN, -span, span); ctx.lineTo(W + 10, Hc + 10); ctx.lineTo(-10, Hc + 10); ctx.closePath();
    ctx.fillStyle = '#ded6c8'; ctx.fill();                   // the ground on the near side, down to the frame
    ctx.beginPath(); { const p = P(-span, yF, zr(-span)); ctx.moveTo(p[0], p[1]); } edge(yF, -span, span); edge(yN, span, -span); ctx.closePath();
    ctx.fillStyle = '#e9e2d6'; ctx.fill();
    ctx.beginPath(); { const p = P(-span, yF, zr(-span)); ctx.moveTo(p[0], p[1]); } edge(yF, -span, span); ctx.strokeStyle = 'rgba(28,21,24,0.35)'; ctx.lineWidth = 1 * dpr; ctx.stroke();
    ctx.beginPath(); { const p = P(-span, yN, zr(-span)); ctx.moveTo(p[0], p[1]); } edge(yN, -span, span); ctx.strokeStyle = C.ink; ctx.lineWidth = 2 * dpr; ctx.stroke();
    ctx.beginPath(); { const p = P(-span, 0, zr(-span)); ctx.moveTo(p[0], p[1]); } edge(0, -span, span); ctx.strokeStyle = 'rgba(28,21,24,0.25)'; ctx.lineWidth = 1 * dpr; ctx.stroke();
    ctx.fillStyle = C.muted; ctx.font = `${11 * dpr}px "IBM Plex Mono", monospace`; ctx.textAlign = 'center';
    for (let m = Math.ceil((c.x - span) * 10); m <= (c.x + span) * 10; m++) {
      const xr = m / 10 - c.x, p = P(xr, yN, zr(xr)), q = P(xr, yN - (m % 10 === 0 ? 0.02 : 0.01), zr(xr));
      if (p[0] < -20 || p[0] > W + 20) continue;
      ctx.strokeStyle = C.muted; ctx.lineWidth = 1 * dpr; ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.stroke();
      if (m % 5 === 0) ctx.fillText(`${(m / 10).toFixed(1)} m`, q[0], q[1] + 14 * dpr);
    }

    // the wheel: a disc of radius Rw in the plane y = 0, 2 cm thick; far face, tread, near face, spokes, hub
    const Rw = c.Rw, ang = -c.x / Rw, circle = (y, rad, zc) => { ctx.beginPath(); for (let k = 0; k <= 48; k++) { const t = k / 48 * 2 * Math.PI, p = P(rad * Math.cos(t), y, zc + rad * Math.sin(t)); k ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); } ctx.closePath(); };
    circle(0.01, Rw, c.zw); ctx.fillStyle = '#1f1a1c'; ctx.fill();
    ctx.fillStyle = '#231d20';                                  // the tread: a band of quads between the two faces
    for (let k = 0; k < 48; k++) {
      const t0 = k / 48 * 2 * Math.PI, t1 = (k + 1) / 48 * 2 * Math.PI;
      const q = [[t0, -0.01], [t1, -0.01], [t1, 0.01], [t0, 0.01]].map(([t, y]) => P(Rw * Math.cos(t), y, c.zw + Rw * Math.sin(t)));
      ctx.beginPath(); q.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath(); ctx.fill();
    }
    circle(-0.01, Rw, c.zw); ctx.fillStyle = '#2a2326'; ctx.fill();
    circle(-0.01, Rw * 0.72, c.zw); ctx.fillStyle = '#d9d2c7'; ctx.fill();
    ctx.strokeStyle = C.ink; ctx.lineWidth = 2 * dpr;
    for (let k = 0; k < 5; k++) {
      const a = ang + k * 2 * Math.PI / 5, p0 = P(0, -0.01, c.zw), p1 = P(0.72 * Rw * Math.cos(a), -0.01, c.zw + 0.72 * Rw * Math.sin(a));
      ctx.beginPath(); ctx.moveTo(p0[0], p0[1]); ctx.lineTo(p1[0], p1[1]); ctx.stroke();
    }
    { const h = P(0, -0.01, c.zw); ctx.beginPath(); ctx.arc(h[0], h[1], 4 * dpr, 0, 2 * Math.PI); ctx.fillStyle = C.ink; ctx.fill(); }

    // axle carrier (a fork over the wheel), spring and damper in the near plane, the body as a box
    const carrierZ = c.zw + Rw + this.carrierGap, bodyZ = c.zb, yS = -0.045;
    const poly = (pts, fill, stroke, lw) => { ctx.beginPath(); pts.forEach((p, k) => { const q = P(p[0], p[1], p[2]); k ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); }); ctx.closePath(); if (fill) { ctx.fillStyle = fill; ctx.fill(); } if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = (lw || 1) * dpr; ctx.stroke(); } };
    const line = (pts, stroke, lw) => { ctx.beginPath(); pts.forEach((p, k) => { const q = P(p[0], p[1], p[2]); k ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); }); ctx.strokeStyle = stroke; ctx.lineWidth = lw * dpr; ctx.stroke(); };
    poly([[-0.004, -0.02, c.zw], [0.004, -0.02, c.zw], [0.004, -0.02, carrierZ], [-0.004, -0.02, carrierZ]], '#4b4246');
    poly([[-0.055, -0.03, carrierZ], [0.055, -0.03, carrierZ], [0.055, 0.03, carrierZ], [-0.055, 0.03, carrierZ]], '#5a5054');
    poly([[-0.055, -0.03, carrierZ], [0.055, -0.03, carrierZ], [0.055, -0.03, carrierZ + 0.006], [-0.055, -0.03, carrierZ + 0.006]], '#4b4246');
    const zA = carrierZ + 0.006, zB = bodyZ, sx = -0.035, dxp = 0.035, coils = 7, amp = 0.012, spring = [[sx, yS, zA], [sx, yS, zA + 0.006]];
    for (let k = 1; k < 2 * coils; k++) spring.push([sx + (k % 2 ? amp : -amp), yS, zA + 0.006 + (zB - zA - 0.012) * k / (2 * coils)]);
    spring.push([sx, yS, zB - 0.006], [sx, yS, zB]); line(spring, C.ink, 2);
    const mid = 0.5 * (zA + zB);
    line([[dxp, yS, zA], [dxp, yS, mid - 0.004]], C.ink, 2);
    poly([[dxp - 0.011, yS, zA + 0.004], [dxp + 0.011, yS, zA + 0.004], [dxp + 0.011, yS, mid + 0.012], [dxp - 0.011, yS, mid + 0.012]], null, C.ink, 2);
    line([[dxp, yS, zB], [dxp, yS, mid + 0.004]], C.ink, 2); line([[dxp - 0.008, yS, mid + 0.004], [dxp + 0.008, yS, mid + 0.004]], C.ink, 2);
    // the spring's compression made readable: a gauge beside it, from 20 mm compressed (bottom) to 20 mm extended (top), the
    // static compression at the middle, the present stroke as a wine bar from it; and the active force as an arrow on the body
    { const Ms = c.Mb + c.ml, s0 = c.Ls - Ms * c.g / c.k, st = c.zb - c.zw - s0, gx = sx - 0.03, gz = 0.5 * (zA + zB), sc = 1;
      const top = P(gx, yS, gz + 0.020 * sc), bot = P(gx, yS, gz - 0.020 * sc), mid = P(gx, yS, gz), cur = P(gx, yS, gz + Math.max(-0.02, Math.min(0.02, st)) * sc);
      ctx.strokeStyle = 'rgba(28,21,24,0.5)'; ctx.lineWidth = 1 * dpr; ctx.beginPath(); ctx.moveTo(top[0], top[1]); ctx.lineTo(bot[0], bot[1]); ctx.stroke();
      for (const p of [top, mid, bot]) { ctx.beginPath(); ctx.moveTo(p[0] - 4 * dpr, p[1]); ctx.lineTo(p[0] + 4 * dpr, p[1]); ctx.stroke(); }
      ctx.strokeStyle = C.accent; ctx.lineWidth = 4 * dpr; ctx.lineCap = 'butt'; ctx.beginPath(); ctx.moveTo(mid[0], mid[1]); ctx.lineTo(cur[0], cur[1]); ctx.stroke();
      ctx.fillStyle = C.muted; ctx.font = `${10 * dpr}px "IBM Plex Mono", monospace`; ctx.textAlign = 'right';
      ctx.fillText((st >= 0 ? '+' : '') + (st * 1000).toFixed(1) + ' mm', mid[0] - 7 * dpr, mid[1] + 3 * dpr);
      if (this.ds && this.ds.has('gauge_px_y')) { this.ds.set('gauge_px_x', cur[0] / dpr); this.ds.set('gauge_px_y', 0.5 * (mid[1] + cur[1]) / dpr); this.ds.set('gauge_mid_y', mid[1] / dpr); }
      if (Math.abs(c.us) > 0.2) {                               // the active force on the body, 1 cm per 4 N
        const a0 = P(dxp + 0.03, yS, zB), a1 = P(dxp + 0.03, yS, zB + c.us / 4 * 0.01), dir = Math.sign(a1[1] - a0[1]) || 1;
        ctx.strokeStyle = C.accent; ctx.lineWidth = 2.5 * dpr; ctx.beginPath(); ctx.moveTo(a0[0], a0[1]); ctx.lineTo(a1[0], a1[1]); ctx.stroke();
        ctx.fillStyle = C.accent; ctx.beginPath(); ctx.moveTo(a1[0], a1[1]); ctx.lineTo(a1[0] - 4 * dpr, a1[1] - 6 * dpr * dir); ctx.lineTo(a1[0] + 4 * dpr, a1[1] - 6 * dpr * dir); ctx.closePath(); ctx.fill();
        ctx.textAlign = 'left'; ctx.fillText(c.us.toFixed(1) + ' N', a1[0] + 5 * dpr, a1[1] + 3 * dpr);
      }
    }
    const bw = this.bodyW / 2, bdp = this.bodyD / 2, bt = bodyZ + this.bodyH;
    poly([[-bw, -bdp, bt], [bw, -bdp, bt], [bw, bdp, bt], [-bw, bdp, bt]], '#f3eee5', C.ink, 2);              // top face
    poly([[bw, -bdp, bodyZ], [bw, bdp, bodyZ], [bw, bdp, bt], [bw, -bdp, bt]], '#ddd5c8', C.ink, 2);          // the end face toward the camera
    poly([[-bw, -bdp, bodyZ], [bw, -bdp, bodyZ], [bw, -bdp, bt], [-bw, -bdp, bt]], '#efe9df', C.ink, 2);      // near face
    ctx.fillStyle = C.muted; ctx.font = `${12 * dpr}px "IBM Plex Mono", monospace`; ctx.textAlign = 'center';
    { const p = P(0, -bdp, bodyZ + this.bodyH / 2); ctx.fillText('BODY', p[0], p[1] + 4 * dpr); }

    // the glass and the stout
    this.drawGlass(cam, bodyZ + this.bodyH);
    // spilled stout: drops in the air drawn as streaks along their velocity (the solver moves them, World.moveDrops),
    // splashes where they landed
    const drops = w.drops;
    if (drops && drops.length) {   // the 3D solvers' spilled particles, or the drops a mode model emits where it pours
      for (const d of drops) {
        const p = P(d.x - c.x, d.y, d.z);
        if (p[0] < -5 || p[0] > W + 5 || p[2] <= 0.05) continue;
        if (d.landed) { ctx.fillStyle = rgb(C.stoutDark, 0.9); ctx.beginPath(); ctx.ellipse(p[0], p[1], 2.2 * dpr, 0.9 * dpr, 0, 0, 2 * Math.PI); ctx.fill(); continue; }
        const dt = 0.008, q = P(d.x - c.x - (d.vx - c.vx) * dt, d.y - d.vy * dt, d.z - d.vz * dt);
        ctx.strokeStyle = rgb(C.stoutDark, 0.55); ctx.lineWidth = 3 * dpr; ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(q[0], q[1]); ctx.lineTo(p[0], p[1]); ctx.stroke();
      }
    }
    if (this.charts) this.drawCharts(W, Hc, dpr);
    if (this.slowText) {                                        // the 3D solver runs slower than real time: say so in the figure
      const narrow = W / dpr < 600; ctx.font = `600 ${(narrow ? 10 : 12) * dpr}px "IBM Plex Mono", monospace`; ctx.textAlign = 'center'; ctx.fillStyle = C.accent;
      const parts = narrow ? this.slowText.split(' ×') : [this.slowText];
      parts.forEach((t, k) => ctx.fillText(k ? '×' + t : t, W / 2, (narrow ? 14 : 20) * dpr + k * 13 * dpr));
    }
  };

  // Live charts in the empty sky of the figure, from the store's numbers as they were written (drawing only):
  // left, the last 4 s of the stout's lean (front − back wall) and the motor current; right, the first mode's phase
  // portrait (q1, q1'/w1) with the rim as its boundary, |q| = z_rim − h: a path that crosses it spills.
  View.prototype.record = function (t, lean, cur, q, qd, w, free, est, stroke, us) {
    const H = this.hist || (this.hist = []);
    if (H.length && t < H[H.length - 1][0]) H.length = 0;      // a restart
    H.push([t, lean, cur, q, qd, w, free, est, stroke || 0, us || 0]);
    while (H.length && H[0][0] < t - 4) H.shift();
  };
  View.prototype.drawCharts = function (W, Hc, dpr) {
    const H = this.hist; if (!H || H.length < 2) return;
    const ctx = this.ctx, mono = (px) => `${px * dpr}px "IBM Plex Mono", monospace`;
    const narrow = W / dpr < 600, pad = (narrow ? 6 : 10) * dpr, cw = Math.min((narrow ? 0.34 : 0.36) * W, 330 * dpr), ch = Math.min((narrow ? 0.17 : 0.22) * Hc, 120 * dpr);
    const box = (x, y, w, h) => { ctx.fillStyle = 'rgba(255,255,255,0.82)'; ctx.fillRect(x, y, w, h); ctx.strokeStyle = 'rgba(28,21,24,0.25)'; ctx.lineWidth = 1 * dpr; ctx.strokeRect(x, y, w, h); };
    // the strip chart
    const x0 = pad, y0 = pad, t1 = H[H.length - 1][0], t0 = t1 - 4, free = H[H.length - 1][6];
    box(x0, y0, cw, ch);
    const lim = Math.max(10, 2 * free * 1000 * 1.1), X = (t) => x0 + (t - t0) / 4 * cw, Yl = (v) => y0 + ch / 2 - v / lim * (ch / 2 - 6 * dpr), Yi = (v) => y0 + ch / 2 - v / 3 * (ch / 2 - 6 * dpr);
    ctx.strokeStyle = 'rgba(122,31,43,0.35)'; ctx.setLineDash([4 * dpr, 3 * dpr]);
    for (const sg of [1, -1]) { ctx.beginPath(); ctx.moveTo(x0, Yl(sg * 2 * free * 1000)); ctx.lineTo(x0 + cw, Yl(sg * 2 * free * 1000)); ctx.stroke(); }
    ctx.setLineDash([]); ctx.strokeStyle = 'rgba(28,21,24,0.15)'; ctx.beginPath(); ctx.moveTo(x0, y0 + ch / 2); ctx.lineTo(x0 + cw, y0 + ch / 2); ctx.stroke();
    const line = (k, Y, col, lw) => { ctx.beginPath(); H.forEach((r, i) => { const px = X(r[0]), py = Math.max(y0, Math.min(y0 + ch, Y(r[k]))); i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); }); ctx.strokeStyle = col; ctx.lineWidth = lw * dpr; ctx.stroke(); };
    line(2, Yi, '#8b8079', 1.2); line(1, (v) => Yl(v * 1000), C.accent, 2);
    if (H[H.length - 1][7] != null) line(7, (v) => Yl(v * 1000), C.ink, 1.2);
    ctx.font = mono(narrow ? 9 : 10); ctx.textAlign = 'left'; ctx.fillStyle = C.accent; ctx.fillText((narrow ? 'lean ±' : 'lean: probes (±') + Math.round(lim) + (narrow ? ' mm' : ' mm)'), x0 + 5 * dpr, y0 + 11 * dpr);
    { const wd = ctx.measureText((narrow ? 'lean ±' : 'lean: probes (±') + Math.round(lim) + (narrow ? ' mm' : ' mm)')).width; ctx.fillStyle = C.ink; ctx.fillText(narrow ? ' · est.' : ' · estimate', x0 + 5 * dpr + wd, y0 + 11 * dpr); }
    ctx.fillStyle = '#6b6166'; ctx.fillText(narrow ? 'current ±3 A' : 'motor current (±3 A)', x0 + 5 * dpr, y0 + ch - 5 * dpr);
    if (!narrow) { ctx.textAlign = 'right'; ctx.fillStyle = 'rgba(122,31,43,0.7)'; ctx.fillText('rim', x0 + cw - 4 * dpr, Yl(2 * free * 1000) - 3 * dpr); ctx.fillStyle = '#6b6166'; ctx.fillText('last 4 s', x0 + cw - 4 * dpr, y0 + ch - 6 * dpr); }
    // the spring: its stroke about the static compression (± 20 mm) and the active force (± 40 N), under the lean chart
    { const y1 = y0 + ch + (narrow ? 4 : 6) * dpr, ch2 = Math.round(ch * 0.8);
      box(x0, y1, cw, ch2);
      const Ys = (v) => y1 + ch2 / 2 - v / 0.02 * (ch2 / 2 - 5 * dpr), Yu = (v) => y1 + ch2 / 2 - v / 40 * (ch2 / 2 - 5 * dpr);
      ctx.strokeStyle = 'rgba(28,21,24,0.15)'; ctx.beginPath(); ctx.moveTo(x0, y1 + ch2 / 2); ctx.lineTo(x0 + cw, y1 + ch2 / 2); ctx.stroke();
      const ln = (k, Y, col, lw) => { ctx.beginPath(); H.forEach((r, i) => { const px = X(r[0]), py = Math.max(y1, Math.min(y1 + ch2, Y(r[k]))); i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); }); ctx.strokeStyle = col; ctx.lineWidth = lw * dpr; ctx.stroke(); };
      ln(9, Yu, '#8b8079', 1.2); ln(8, Ys, C.ink, 1.8);
      ctx.font = mono(narrow ? 9 : 10); ctx.textAlign = 'left'; ctx.fillStyle = C.ink; ctx.fillText(narrow ? 'spring ±20 mm' : 'spring stroke (±20 mm)', x0 + 5 * dpr, y1 + 11 * dpr);
      ctx.fillStyle = '#6b6166'; ctx.fillText(narrow ? 'active ±40 N' : 'active force (±40 N)', x0 + 5 * dpr, y1 + ch2 - 5 * dpr);
      this.chartSpringBox = [x0 / dpr, y1 / dpr, cw / dpr, ch2 / dpr]; }
    // the phase portrait
    const s0 = Math.min(ch, 120 * dpr), px0 = W - pad - s0, py0 = pad, R = free * 1.15, Pm = (q) => px0 + s0 / 2 + q / R * (s0 / 2 - 6 * dpr), Pv = (v) => py0 + s0 / 2 - v / R * (s0 / 2 - 6 * dpr);
    box(px0, py0, s0, s0);
    ctx.strokeStyle = 'rgba(122,31,43,0.35)'; ctx.setLineDash([4 * dpr, 3 * dpr]);
    for (const sg of [1, -1]) { ctx.beginPath(); ctx.moveTo(Pm(sg * free), py0); ctx.lineTo(Pm(sg * free), py0 + s0); ctx.stroke(); }
    ctx.setLineDash([]); ctx.beginPath();
    H.forEach((r, i) => { const a = Math.max(px0, Math.min(px0 + s0, Pm(r[3]))), b = Math.max(py0, Math.min(py0 + s0, Pv(r[4] / r[5]))); i ? ctx.lineTo(a, b) : ctx.moveTo(a, b); });
    ctx.strokeStyle = C.accent; ctx.lineWidth = 1.5 * dpr; ctx.stroke();
    const L = H[H.length - 1]; ctx.beginPath(); ctx.arc(Math.max(px0, Math.min(px0 + s0, Pm(L[3]))), Math.max(py0, Math.min(py0 + s0, Pv(L[4] / L[5]))), 3 * dpr, 0, 2 * Math.PI); ctx.fillStyle = C.accent; ctx.fill();
    ctx.font = mono(narrow ? 9 : 10); ctx.textAlign = 'left'; ctx.fillStyle = '#6b6166'; ctx.fillText(narrow ? 'swing, est.' : 'estimate q̂, q̂̇/ω', px0 + 5 * dpr, py0 + 11 * dpr);
    ctx.textAlign = 'right'; ctx.fillStyle = 'rgba(122,31,43,0.7)'; ctx.fillText('rim', px0 + s0 - 4 * dpr, py0 + s0 - 5 * dpr);
  };

  // The glass and the stout. The glass is a body of revolution with inner radius R(z) (the solver's wall) and a wall
  // 2.5 mm thick, its floor zG above the road; the stout fills it to the computed surface; the head is a layer on it.
  View.prototype.drawGlass = function (cam, zTopOfBody) {
    const ctx = this.ctx, f = this.world.fluid, dpr = this.cv.width / (this.cssW || this.cv.width);
    const base = this.glassBase, wall = this.glassWall, zRim = isFinite(f.zRim) ? f.zRim : f.H, zG = zTopOfBody + base;
    const Rin = (z) => Math.min(f.Rz(Math.min(z, zRim - 1e-6)), f.Rbox), Rout = (z) => Rin(Math.max(0.008, z)) + wall;   // the foot is solid glass: straight below 8 mm
    const P = (x, y, z) => this.project(cam, x, y, zG + z);                    // glass coordinates: z = 0 at the inner floor
    const thC = Math.atan2(cam.Cp[1], cam.Cp[0]);                              // the camera's direction from the axis
    const thL = thC + Math.PI / 2, thR = thC - Math.PI / 2;                    // the silhouette generatrices (left and right on screen)
    const Z = []; for (let z = 0; z <= zRim + 1e-9; z += 0.002) Z.push(z); if (Z[Z.length - 1] < zRim) Z.push(zRim);
    const gen = (th, z0, z1, rf, up) => { const zs = Z.filter((z) => z >= z0 - 1e-9 && z <= z1 + 1e-9); if (!up) zs.reverse(); zs.forEach((z) => { const p = P(rf(z) * Math.cos(th), rf(z) * Math.sin(th), z); ctx.lineTo(p[0], p[1]); }); };
    const arc = (z, rad, from, to) => { const n = 40; for (let k = 0; k <= n; k++) { const t = from + (to - from) * k / n, p = P(rad * Math.cos(t), rad * Math.sin(t), z); ctx.lineTo(p[0], p[1]); } };
    // the whole glass seen through, tinted: left generatrix up, far rim, right generatrix down, near foot
    ctx.beginPath(); { const p = P(Rout(0) * Math.cos(thL), Rout(0) * Math.sin(thL), -base); ctx.moveTo(p[0], p[1]); }
    gen(thL, 0, zRim, Rout, true); arc(zRim, Rout(zRim), thL, thR + 2 * Math.PI); gen(thR, 0, zRim, Rout, false); arc(-base, Rout(0), thR, thL); ctx.closePath();
    ctx.fillStyle = 'rgba(205,214,218,0.45)'; ctx.fill();

    const Hs = this.surface(), nr = this.nr, nth = this.nth, hh = this.headH, rS = f.Rz(Math.min(f.h0, f.zRim));
    if (f.gpu && this.gpuView) {
      // the GPU solver's stout, drawn on the graphics chip from its particles (scripts/stout-gpu-view.js), laid in the glass;
      // the head there is the top headH of the stout, painted from the surface map hs (the column heights, as the probes read them)
      const N = this.gpuView.hsN, R0 = rS + 2 * f.dx, hs = this.hsMap || (this.hsMap = new Float32Array(N * N));
      for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) hs[i + N * j] = f.columnHeightAt(-R0 + 2 * R0 * i / (N - 1), -R0 + 2 * R0 * j / (N - 1));
      this.gpuView.headH = hh;
      const img = this.gpuView.render(cam, this.cv.width, this.cv.height, zG, hs, R0, this.light);
      ctx.drawImage(img, 0, 0);
      this.drawGlassFront(cam, P, zRim, Rin, Rout, thL, thR, gen, arc, base, f, dpr);
      return this.afterGlass(P, f, rS, hh, dpr, Hs);
    }
    const etaAt = (th) => { const it = ((th / (2 * Math.PI) * nth) % nth + nth) % nth, i0 = Math.floor(it), t = it - i0; return Hs[nr][i0] + t * (Hs[nr][(i0 + 1) % nth] - Hs[nr][i0]); };
    const rB = rS - 0.0005;
    // the body of the drink: its near face, from the surface at the near arc down the generatrices to the floor
    const nearArc = (zOff, dir) => { const n = 48; for (let k = 0; k <= n; k++) { const t = dir > 0 ? thR + Math.PI * k / n : thL - Math.PI * k / n, p = P(rB * Math.cos(t), rB * Math.sin(t), etaAt(t) + zOff); ctx.lineTo(p[0], p[1]); } };
    ctx.beginPath(); { const p = P(rB * Math.cos(thR), rB * Math.sin(thR), etaAt(thR)); ctx.moveTo(p[0], p[1]); }
    nearArc(0, 1); gen(thL, 0, etaAt(thL), Rin, false); arc(0, Rin(0), thL, thR); ctx.closePath();
    // Beer–Lambert across the glass: light through a path 2 sqrt(R² − x²) long, ruby where thin, black where long
    const pL = P(-rS * Math.cos(thC + Math.PI / 2) * 0 + rS * Math.cos(thL), rS * Math.sin(thL), f.h0 / 2), pR = P(rS * Math.cos(thR), rS * Math.sin(thR), f.h0 / 2);
    const g = ctx.createLinearGradient(pL[0], 0, pR[0], 0);
    for (let k = 0; k <= 16; k++) { const xr = -1 + 2 * k / 16, ell = 2 * rS * Math.sqrt(Math.max(0, 1 - xr * xr)), T = Math.exp(-this.kappa * ell); g.addColorStop(k / 16, rgb(mix(C.stoutDark, C.stoutRuby, T))); }
    ctx.fillStyle = g; ctx.fill();
    // the head's side, a band from the surface up by headH along the near arc
    ctx.beginPath(); { const p = P(rB * Math.cos(thR), rB * Math.sin(thR), etaAt(thR)); ctx.moveTo(p[0], p[1]); }
    nearArc(0, 1); nearArc(hh, -1); ctx.closePath(); ctx.fillStyle = rgb(mix(C.headShade, C.head, 0.55)); ctx.fill();
    // the head's top: the sheet, quads from far to near, lit by one light (Phong)
    const pt = (ir, it) => { const r = rS * ir / nr, th = 2 * Math.PI * it / nth; return [r * Math.cos(th), r * Math.sin(th), Hs[ir][((it % nth) + nth) % nth] + hh]; };
    const quads = [], L = this.light, E = [-cam.d[0], -cam.d[1], -cam.d[2]], Hv = [L[0] + E[0], L[1] + E[1], L[2] + E[2]], Hl = Math.hypot(...Hv);
    // on a narrow figure (a phone: the glass is about 70 px wide) the sheet is drawn over every other angle of the same stored
    // surface: half the quads, the stored and checked points unchanged
    const stp = this.cssW && this.cssW < 600 ? 2 : 1;
    for (let ir = 0; ir < nr; ir++) for (let it = 0; it < nth; it += stp) {
      const a = pt(ir, it), b = pt(ir + 1, it), c2 = pt(ir + 1, it + stp), d = pt(ir, it + stp);
      const ux = c2[0] - a[0], uy = c2[1] - a[1], uz = c2[2] - a[2], vx = d[0] - b[0], vy = d[1] - b[1], vz = d[2] - b[2];
      let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
      if (nz < 0) { nx = -nx; ny = -ny; nz = -nz; }
      const nl = Math.hypot(nx, ny, nz) || 1, mx = (a[0] + c2[0]) / 2, my = (a[1] + c2[1]) / 2, mz = (a[2] + c2[2]) / 2;
      const dep = dot([mx - cam.Cp[0], my - cam.Cp[1], zG + mz - cam.Cp[2]], cam.d);
      quads.push([dep, [a, b, c2, d], nx / nl, ny / nl, nz / nl]);
    }
    quads.sort((p, q) => q[0] - p[0]);
    for (const [, vs, nx, ny, nz] of quads) {
      const lam = Math.max(0, nx * L[0] + ny * L[1] + nz * L[2]);
      const spec = Math.pow(Math.max(0, (nx * Hv[0] + ny * Hv[1] + nz * Hv[2]) / Hl), 48);
      let col = mix(C.headShade, C.head, Math.min(1, 0.3 + 0.8 * lam));
      col = mix(col, [253, 250, 242], 0.45 * spec);
      ctx.beginPath();
      vs.forEach(([x, y, z], k) => { const p = P(x, y, z); k ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); });
      ctx.closePath(); ctx.fillStyle = rgb(col); ctx.fill(); ctx.strokeStyle = rgb(col); ctx.lineWidth = 0.7 * dpr; ctx.stroke();
    }
    // the edge of the head along the near wall
    ctx.beginPath(); { const p = P(rB * Math.cos(thR), rB * Math.sin(thR), etaAt(thR)); ctx.moveTo(p[0], p[1]); } nearArc(0, 1);
    ctx.strokeStyle = 'rgba(150,120,90,0.8)'; ctx.lineWidth = 1 * dpr; ctx.stroke();

    this.drawGlassFront(cam, P, zRim, Rin, Rout, thL, thR, gen, arc, base, f, dpr);
    return this.afterGlass(P, f, rS, hh, dpr, Hs);
  };
  // the glass in front of the stout: tint, outlines, rim, foot, and the two probes on the wall
  View.prototype.drawGlassFront = function (cam, P, zRim, Rin, Rout, thL, thR, gen, arc, base, f, dpr) {
    const ctx = this.ctx;
    // glass: front tint, outer and inner outlines, rim, foot
    ctx.beginPath(); { const p = P(Rout(0) * Math.cos(thL), Rout(0) * Math.sin(thL), -base); ctx.moveTo(p[0], p[1]); }
    gen(thL, 0, zRim, Rout, true); arc(zRim, Rout(zRim), thL, thR); gen(thR, 0, zRim, Rout, false); arc(-base, Rout(0), thR, thL);
    ctx.closePath(); ctx.fillStyle = C.glass; ctx.fill();
    ctx.lineWidth = 1.6 * dpr; ctx.strokeStyle = C.line;
    for (const th of [thL, thR]) { ctx.beginPath(); { const p = P(Rout(0) * Math.cos(th), Rout(0) * Math.sin(th), -base); ctx.moveTo(p[0], p[1]); } gen(th, 0, zRim, Rout, true); ctx.stroke(); }
    ctx.strokeStyle = 'rgba(28,21,24,0.30)'; ctx.lineWidth = 1 * dpr;
    for (const th of [thL, thR]) { ctx.beginPath(); { const p = P(Rin(0) * Math.cos(th), Rin(0) * Math.sin(th), 0); ctx.moveTo(p[0], p[1]); } gen(th, 0, zRim, Rin, true); ctx.stroke(); }
    ctx.lineWidth = 1.6 * dpr; ctx.strokeStyle = C.line;
    ctx.beginPath(); { const p = P(Rout(zRim), 0, zRim); ctx.moveTo(p[0], p[1]); } arc(zRim, Rout(zRim), 0, 2 * Math.PI); ctx.stroke();
    ctx.strokeStyle = 'rgba(28,21,24,0.35)'; ctx.lineWidth = 1 * dpr;
    ctx.beginPath(); { const p = P(Rin(zRim), 0, zRim); ctx.moveTo(p[0], p[1]); } arc(zRim, Rin(zRim), 0, 2 * Math.PI); ctx.stroke();
    ctx.strokeStyle = C.line; ctx.lineWidth = 1.6 * dpr; ctx.beginPath(); { const p = P(Rout(0) * Math.cos(thR), Rout(0) * Math.sin(thR), -base); ctx.moveTo(p[0], p[1]); } arc(-base, Rout(0), thR, thL); ctx.stroke();
    // the two level probes: thin strips on the inner wall at theta = 0 (front) and pi (back), 60 mm long about the fill
    // height, each with a white dot (3 px) where it reads the surface now (World.readProbes; the dot is the reading, not a drawing)
    const pr = this.world.cart.probe;
    if (pr && pr.r) {
      for (const [sg, eta] of [[1, pr.ef], [-1, pr.eb]]) {
        // the strip is left open where the head's band lies on the surface, so the head stays visible at the wall
        const rr = pr.r - 0.0006, top = Math.min(zRim, f.h0 + 0.03), bot = f.h0 - 0.03;
        ctx.strokeStyle = 'rgba(28,21,24,0.75)'; ctx.lineWidth = 2.5 * dpr; ctx.lineCap = 'butt';
        const g0 = f.gpu ? eta - this.headH : eta, g1 = f.gpu ? eta : eta + this.headH;   // the head: on the surface (CPU drawing) or its top band (GPU drawing)
        for (const [z0, z1] of [[bot, Math.min(g0, top)], [Math.max(bot, g1), top]]) {
          if (z1 <= z0) continue;
          const a = P(sg * rr, 0, z0), b = P(sg * rr, 0, z1); ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
        }
        const m = P(sg * rr, 0, eta);
        ctx.beginPath(); ctx.arc(m[0], m[1], 3 * dpr, 0, 2 * Math.PI); ctx.fillStyle = '#ffffff'; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 1.2 * dpr; ctx.stroke();
        if (this.ds && this.ds.has('probe_px_x') && sg > 0) { this.ds.set('probe_px_x', m[0] / dpr); this.ds.set('probe_px_y', m[1] / dpr); }
      }
    }
  };
  // what the store keeps of the drawn glass: the read-back points of the head
  View.prototype.afterGlass = function (P, f, rS, hh, dpr, Hs) {
    this.lastSurface = Hs;
    if (this.ds) {                                               // the head's middle at the front wall (near band) and its top on the axis
      // the head's band at the front wall and its top on the axis (CPU drawing: a band laid on the surface; GPU drawing: the top
      // headH of the stout, so the points sit half a band below the surface and just under it)
      const D = this.ds, em = f.columnHeightAt(0, 0), fr = P(0.98 * rS, 0, f.columnHeightAt(rS, 0) + (f.gpu ? -0.5 : 0.75) * hh), bk = P(0, 0, em + (f.gpu ? -0.002 : hh));   // the head's band at the front wall; its top on the axis
      D.set('eta_mid', em);
      D.set('front_px_x', fr[0] / dpr); D.set('front_px_y', fr[1] / dpr); D.set('back_px_x', bk[0] / dpr); D.set('back_px_y', bk[1] / dpr);
      D.set('head_h', hh); D.set('r_s', rS);
    }
  };

  root.StoutView = View;
})(typeof self !== 'undefined' ? self : this);
