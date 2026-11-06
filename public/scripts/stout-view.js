/* Fig. 12: drawing the cart and the pint of stout (canvas 2D). Reads the state of a StoutCart.World; computes nothing
 * physical. The surface of the stout is the liquid column height computed by the solver (Fluid.columnHeights), read
 * on a polar grid over the whole glass (the half that is not solved is its mirror image), seen from slightly above.
 * The creamy head is DRAWN, not simulated: a layer of constant thickness headH laid on the simulated surface. */
(function (root) {
  'use strict';
  const C = {
    paper: '#f5f1ea', ink: '#1c1518', muted: '#6b6166', accent: '#7a1f2b', line: 'rgba(28,21,24,0.85)',
    stoutDark: [14, 8, 7], stoutRuby: [62, 18, 14], head: [236, 225, 201], headShade: [196, 178, 146], glass: 'rgba(120,140,150,0.10)',
  };
  const lerp = (a, b, t) => a + (b - a) * t;
  const rgb = (c, a) => a == null ? `rgb(${c[0] | 0},${c[1] | 0},${c[2] | 0})` : `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a})`;
  const mix = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];

  function View(canvas, world, o) {
    o = o || {};
    this.cv = canvas; this.ctx = canvas.getContext('2d'); this.world = world;
    this.scale = o.scale || 2600;        // px per metre
    this.elev = (o.elevDeg != null ? o.elevDeg : 14) * Math.PI / 180;
    this.nr = o.nr || 9; this.nth = o.nth || 48;
    this.bodyW = 0.22; this.bodyH = 0.03; this.headH = o.headH != null ? o.headH : 0.012; this.carrierGap = 0.006; this.glassWall = 0.004; this.glassBase = 0.006;
    this.groundY = o.groundY || 0.80;   // fraction of canvas height where z = 0 sits
    this.camX = null;
  }

  // free-surface heights on the polar grid: h[ir][ith], ir = 0..nr (r = R ir / nr), ith over the full circle
  View.prototype.surface = function () {
    const f = this.world.fluid, R = f.R, nr = this.nr, nth = this.nth, H = [];
    f.columnHeights();
    for (let ir = 0; ir <= nr; ir++) {
      const row = [], r = R * ir / nr;
      for (let it = 0; it < nth; it++) {
        const th = 2 * Math.PI * it / nth;
        row.push(f.columnHeightAt(r * Math.cos(th), r * Math.sin(th)));
      }
      H.push(row);
    }
    return H;
  };

  View.prototype.draw = function (extra) {
    const ctx = this.ctx, W = this.cv.width, Hc = this.cv.height, s = this.scale, w = this.world, c = w.cart, f = w.fluid;
    const dpr = W / (this.cssW || W);
    if (this.camX == null) this.camX = c.x;
    this.camX = c.x;                                           // the camera rides with the cart
    const X = (x) => W / 2 + (x - this.camX) * s, Z = (z) => Hc * this.groundY - z * s;
    ctx.fillStyle = C.paper; ctx.fillRect(0, 0, W, Hc);

    // road and ground
    const road = c.road;
    ctx.beginPath();
    const x0 = this.camX - W / 2 / s, x1 = this.camX + W / 2 / s;
    for (let px = 0; px <= W; px += 2) { const x = x0 + px / s; const y = Z(road.zr(x)); px === 0 ? ctx.moveTo(px, y) : ctx.lineTo(px, y); }
    ctx.lineTo(W, Hc); ctx.lineTo(0, Hc); ctx.closePath();
    ctx.fillStyle = '#e9e2d6'; ctx.fill();
    ctx.beginPath();
    for (let px = 0; px <= W; px += 2) { const x = x0 + px / s; const y = Z(road.zr(x)); px === 0 ? ctx.moveTo(px, y) : ctx.lineTo(px, y); }
    ctx.strokeStyle = C.ink; ctx.lineWidth = 2 * dpr; ctx.stroke();
    // distance ticks every 10 cm so the travel reads
    ctx.fillStyle = C.muted; ctx.font = `${11 * dpr}px "IBM Plex Mono", monospace`; ctx.textAlign = 'center';
    for (let m = Math.ceil(x0 * 10); m <= x1 * 10; m++) {
      const x = m / 10, y = Z(road.zr(x));
      ctx.fillRect(X(x) - 0.5 * dpr, y + 4 * dpr, 1 * dpr, (m % 10 === 0 ? 10 : 5) * dpr);
      if (m % 5 === 0) ctx.fillText(`${(m / 10).toFixed(1)} m`, X(x), y + 26 * dpr);
    }

    // wheel
    const Rw = c.Rw, ax = X(c.x), ay = Z(c.zw);
    ctx.beginPath(); ctx.arc(ax, ay, Rw * s, 0, 2 * Math.PI); ctx.fillStyle = '#2a2326'; ctx.fill();
    ctx.beginPath(); ctx.arc(ax, ay, Rw * s * 0.72, 0, 2 * Math.PI); ctx.fillStyle = '#d9d2c7'; ctx.fill();
    const ang = -c.x / Rw;
    ctx.strokeStyle = C.ink; ctx.lineWidth = 2 * dpr;
    for (let k = 0; k < 5; k++) {
      const a = ang + k * 2 * Math.PI / 5;
      ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(ax + Math.cos(a) * Rw * s * 0.72, ay + Math.sin(a) * Rw * s * 0.72); ctx.stroke();
    }
    ctx.beginPath(); ctx.arc(ax, ay, 4 * dpr, 0, 2 * Math.PI); ctx.fillStyle = C.ink; ctx.fill();

    // axle carrier (a fork over the wheel) and the body
    const carrierZ = c.zw + Rw + this.carrierGap, bodyZ = c.zb;
    const cw = 0.11;
    ctx.fillStyle = '#4b4246';
    ctx.fillRect(X(c.x - cw / 2), Z(carrierZ + 0.006), cw * s, 0.006 * s);
    ctx.fillRect(X(c.x - 0.004), Z(carrierZ), 0.008 * s, (carrierZ - c.zw) * s);
    // spring (left) and damper (right) between carrier and body
    const zA = carrierZ + 0.006, zB = bodyZ, sx = c.x - 0.035, dxp = c.x + 0.035;
    ctx.strokeStyle = C.ink; ctx.lineWidth = 2 * dpr; ctx.beginPath();
    const coils = 7, amp = 0.012;
    ctx.moveTo(X(sx), Z(zA)); ctx.lineTo(X(sx), Z(zA + 0.006));
    for (let k = 1; k < 2 * coils; k++) {
      const zz = zA + 0.006 + (zB - zA - 0.012) * k / (2 * coils);
      ctx.lineTo(X(sx + (k % 2 ? amp : -amp)), Z(zz));
    }
    ctx.lineTo(X(sx), Z(zB - 0.006)); ctx.lineTo(X(sx), Z(zB)); ctx.stroke();
    const mid = 0.5 * (zA + zB);
    ctx.beginPath(); ctx.moveTo(X(dxp), Z(zA)); ctx.lineTo(X(dxp), Z(mid - 0.004)); ctx.stroke();
    ctx.strokeRect(X(dxp - 0.011), Z(mid + 0.012), 0.022 * s, (mid + 0.012 - (zA + 0.004)) * s);
    ctx.beginPath(); ctx.moveTo(X(dxp), Z(zB)); ctx.lineTo(X(dxp), Z(mid + 0.004));
    ctx.moveTo(X(dxp - 0.008), Z(mid + 0.004)); ctx.lineTo(X(dxp + 0.008), Z(mid + 0.004)); ctx.stroke();
    // body block
    ctx.fillStyle = '#efe9df'; ctx.strokeStyle = C.ink; ctx.lineWidth = 2 * dpr;
    ctx.fillRect(X(c.x - this.bodyW / 2), Z(bodyZ + this.bodyH), this.bodyW * s, this.bodyH * s);
    ctx.strokeRect(X(c.x - this.bodyW / 2), Z(bodyZ + this.bodyH), this.bodyW * s, this.bodyH * s);
    ctx.fillStyle = C.muted; ctx.font = `${12 * dpr}px "IBM Plex Mono", monospace`; ctx.textAlign = 'center';
    ctx.fillText('BODY', X(c.x), Z(bodyZ + this.bodyH / 2) + 4 * dpr);

    // the glass and the stout, seen from slightly above
    this.drawGlass(X(c.x), Z(bodyZ + this.bodyH), extra);
  };

  View.prototype.drawGlass = function (cx, cy, extra) {
    const ctx = this.ctx, s = this.scale, f = this.world.fluid, R = f.R, e = this.elev, se = Math.sin(e), ce = Math.cos(e);
    const dpr = this.cv.width / (this.cssW || this.cv.width);
    const base = this.glassBase, Hglass = f.H, Ro = R + this.glassWall;
    // projection: x right, y away from the viewer, z up (glass frame, z = 0 at the inner bottom)
    const P = (x, y, z) => [cx + x * s, cy - (base + z) * ce * s - y * se * s];
    const ell = (z, r, from, to, ccw) => { const [px, py] = P(0, 0, z); ctx.ellipse(px, py, r * s, r * se * s, 0, from, to, ccw); };

    // back half of the glass: inside wall
    ctx.beginPath(); ell(Hglass, Ro, Math.PI, 2 * Math.PI); ell(-base, Ro, 2 * Math.PI, Math.PI, true); ctx.closePath();
    ctx.fillStyle = 'rgba(205,214,218,0.55)'; ctx.fill();

    const Hs = this.surface(), nr = this.nr, nth = this.nth, hh = this.headH;
    const pt = (ir, it) => {
      const r = R * ir / nr, th = 2 * Math.PI * it / nth;
      return [r * Math.cos(th), r * Math.sin(th), Hs[ir][((it % nth) + nth) % nth] + hh];
    };
    // the drink's body: the front half of the wall from the bottom to the surface
    ctx.beginPath();
    for (let it = nth / 2; it <= nth; it++) { const [x, y, z] = pt(nr, it); const [px, py] = P(x, y, z); it === nth / 2 ? ctx.moveTo(px, py) : ctx.lineTo(px, py); }
    for (let it = nth; it >= nth / 2; it--) { const [x, y] = pt(nr, it); const [px, py] = P(x, y, 0); ctx.lineTo(px, py); }
    ctx.closePath();
    // the back half of the liquid's outline too, so the surface quads have liquid beneath
    const g = ctx.createLinearGradient(0, P(0, 0, f.h0)[1], 0, P(0, 0, 0)[1]);
    g.addColorStop(0, rgb(C.stoutDark)); g.addColorStop(0.85, rgb(C.stoutDark)); g.addColorStop(1, rgb(C.stoutRuby));
    // surface: quads drawn from the back (large y) to the front, shaded by their normal
    const quads = [];
    for (let ir = 0; ir < nr; ir++) for (let it = 0; it < nth; it++) {
      const a = pt(ir, it), b = pt(ir + 1, it), c2 = pt(ir + 1, it + 1), d = pt(ir, it + 1);
      const ux = c2[0] - a[0], uy = c2[1] - a[1], uz = c2[2] - a[2], vx = d[0] - b[0], vy = d[1] - b[1], vz = d[2] - b[2];
      let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
      if (nz < 0) { nx = -nx; ny = -ny; nz = -nz; }
      const nl = Math.hypot(nx, ny, nz) || 1;
      const depth = (a[1] + b[1] + c2[1] + d[1]) / 4;
      quads.push([depth, [a, b, c2, d], nx / nl, ny / nl, nz / nl]);
    }
    quads.sort((p, q) => q[0] - p[0]);
    const L = [-0.45, 0.35, 0.82], Ll = Math.hypot(...L), view = [0, -se, ce];
    for (const [, vs, nx, ny, nz] of quads) {
      const lam = Math.max(0, (nx * L[0] + ny * L[1] + nz * L[2]) / Ll);
      const hx = L[0] / Ll + view[0], hy = L[1] / Ll + view[1], hz = L[2] / Ll + view[2], hl = Math.hypot(hx, hy, hz);
      const spec = Math.pow(Math.max(0, (nx * hx + ny * hy + nz * hz) / hl), 60);
      let col = mix(C.headShade, C.head, Math.min(1, 0.35 + 0.75 * lam));
      col = mix(col, [252, 248, 238], 0.5 * spec);
      ctx.beginPath();
      vs.forEach(([x, y, z], k) => { const [px, py] = P(x, y, z); k ? ctx.lineTo(px, py) : ctx.moveTo(px, py); });
      ctx.closePath(); ctx.fillStyle = rgb(col); ctx.fill(); ctx.strokeStyle = rgb(col); ctx.lineWidth = 0.6 * dpr; ctx.stroke();
    }
    // front of the drink over the near part of the surface: the head band first
    ctx.beginPath();
    for (let it = nth / 2; it <= nth; it++) { const [x, y, z] = pt(nr, it); const [px, py] = P(x, y, z); it === nth / 2 ? ctx.moveTo(px, py) : ctx.lineTo(px, py); }
    for (let it = nth; it >= nth / 2; it--) { const [x, y] = pt(nr, it); const [px, py] = P(x, y, 0); ctx.lineTo(px, py); }
    ctx.closePath(); ctx.fillStyle = rgb(C.head); ctx.fill();
    // the stout below the head: the same front wall, up to the simulated surface
    ctx.beginPath();
    for (let it = nth / 2; it <= nth; it++) { const [x, y, z] = pt(nr, it); const [px, py] = P(x, y, z - hh); it === nth / 2 ? ctx.moveTo(px, py) : ctx.lineTo(px, py); }
    for (let it = nth; it >= nth / 2; it--) { const [x, y] = pt(nr, it); const [px, py] = P(x, y, 0); ctx.lineTo(px, py); }
    ctx.closePath(); ctx.fillStyle = g; ctx.fill();
    // the line where stout meets head along the front wall
    ctx.beginPath();
    for (let it = nth / 2; it <= nth; it++) { const [x, y, z] = pt(nr, it); const [px, py] = P(x, y, z - hh); it === nth / 2 ? ctx.moveTo(px, py) : ctx.lineTo(px, py); }
    ctx.strokeStyle = 'rgba(150,120,90,0.8)'; ctx.lineWidth = 1 * dpr; ctx.stroke();

    // glass: front wall tint, outlines, rim, base
    ctx.beginPath(); ell(Hglass, Ro, 0, Math.PI); ell(-base, Ro, Math.PI, 0, true); ctx.closePath();
    ctx.fillStyle = C.glass; ctx.fill();
    ctx.strokeStyle = C.line; ctx.lineWidth = 1.6 * dpr;
    ctx.beginPath(); ell(Hglass, Ro, 0, 2 * Math.PI); ctx.stroke();
    ctx.beginPath(); ell(Hglass, R, 0, 2 * Math.PI); ctx.strokeStyle = 'rgba(28,21,24,0.35)'; ctx.stroke();
    ctx.strokeStyle = C.line;
    ctx.beginPath(); const [lx0, ly0] = P(-Ro, 0, Hglass), [lx1, ly1] = P(-Ro, 0, -base); ctx.moveTo(lx0, ly0); ctx.lineTo(lx1, ly1); ctx.stroke();
    ctx.beginPath(); const [rx0, ry0] = P(Ro, 0, Hglass), [rx1, ry1] = P(Ro, 0, -base); ctx.moveTo(rx0, ry0); ctx.lineTo(rx1, ry1); ctx.stroke();
    ctx.beginPath(); ell(-base, Ro, 0, Math.PI); ctx.stroke();
    this.lastSurface = Hs;
  };

  root.StoutView = View;
})(typeof self !== 'undefined' ? self : this);
