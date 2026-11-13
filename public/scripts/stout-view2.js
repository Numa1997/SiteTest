/* Fig. 12, computed in JAX on Kaggle: the stored ride (public/data/fig12/<date>/<ride>.json) and its drawing. Computes nothing
 * physical. StoutRide unpacks the file: per frame, the stout's surface on the solver's own columns (n x n, steps of qH), the
 * thickness of the head of foam on each column (steps of qhf), the drops of stout in the air and the lumps of head in the air.
 * StoutView2 is StoutView (the cart, the road, the camera) with the glass drawn from those stored fields: the stout's body, the
 * head as a layer of the stored thickness on the stored surface, drops and lumps where they were stored, and the lettering on
 * the glass. Where a column has no stored value (cut by the glass) the nearest stored columns are used; nothing is extended. */
(function (root) {
  'use strict';
  const SV = root.StoutView;
  const lerp = (a, b, t) => a + (b - a) * t;
  const mix = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
  const rgb = (c, a) => a == null ? `rgb(${c[0] | 0},${c[1] | 0},${c[2] | 0})` : `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a})`;
  const C = { stoutDark: [16, 9, 8], stoutRuby: [104, 24, 16], stoutTop: [34, 20, 16], cream: [240, 229, 204], creamLit: [250, 243, 226],
    creamShade: [203, 184, 150], gold: [201, 168, 106], ink: '#1c1518' };

  async function inflate(b64, Type) {
    const s = atob(b64), a = new Uint8Array(s.length);
    for (let i = 0; i < s.length; i++) a[i] = s.charCodeAt(i);
    const st = new Blob([a]).stream().pipeThrough(new DecompressionStream('deflate'));
    return new Type(await new Response(st).arrayBuffer());
  }

  function StoutRide(D) { this.D = D; this.n = D.n; this.frames = D.frames; this.dx = D.dx; this.x0 = D.x0; this.fill = D.fill; this.fps = D.fps; }
  StoutRide.prototype.unpack = async function () {
    const D = this.D, n2 = this.n * this.n;
    const H = await inflate(D.H, Int16Array);                    // differences from the frame before: a running sum restores them
    for (let k = 1; k < this.frames; k++) { const a = k * n2, b = a - n2; for (let i = 0; i < n2; i++) H[a + i] = (H[a + i] + H[b + i]) << 16 >> 16; }
    this.H = H; this.hf = await inflate(D.hf, Uint8Array);
    this.drops = await inflate(D.drops, Int16Array); this.lumps = await inflate(D.lumps, Int16Array);
    const off = (c) => { const o = new Int32Array(c.length + 1); for (let k = 0; k < c.length; k++) o[k + 1] = o[k] + c[k]; return o; };
    this.dOff = off(D.nd); this.lOff = off(D.nl);
    return this;
  };
  // stored surface (m above the glass's inner floor) and head thickness (m) at (x, y) of frame k: bilinear over the stored
  // columns around the point, leaving out those with no stout; NaN if none of the four holds a value
  StoutRide.prototype.at = function (k, x, y) {
    const n = this.n, fx = (x - this.x0) / this.dx - 0.5, fy = (y - this.x0) / this.dx - 0.5;
    const i = Math.floor(fx), j = Math.floor(fy), tx = fx - i, ty = fy - j, base = k * n * n;
    let w = 0, h = 0, f = 0;
    for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++) {
      const ii = i + a, jj = j + b; if (ii < 0 || jj < 0 || ii >= n || jj >= n) continue;
      const v = this.H[base + ii * n + jj]; if (v === -32768) continue;
      const ww = (a ? tx : 1 - tx) * (b ? ty : 1 - ty); w += ww; h += ww * v; f += ww * this.hf[base + ii * n + jj];
    }
    return w > 1e-6 ? [h / w * this.D.qH, f / w * this.D.qhf] : null;
  };
  // the same along a ray from the axis: the outermost stored value at or inside radius r in direction th
  StoutRide.prototype.atInward = function (k, r, th) {
    const c = Math.cos(th), s = Math.sin(th);
    for (let q = r; q > 0; q -= 0.5 * this.dx) { const v = this.at(k, q * c, q * s); if (v) return v; }
    return this.at(k, 0, 0) || [this.fill, 0];
  };

  function View2(canvas, world, o) { SV.call(this, canvas, world, o); this.nr = 14; this.nth = 96; this.ride = null; this.k = 0; this.letter = true; }
  View2.prototype = Object.create(SV.prototype);
  View2.prototype.setFrame = function (ride, k) { this.ride = ride; this.k = Math.max(0, Math.min(ride.frames - 1, k)); };

  View2.prototype.drawGlass = function (cam, zTopOfBody) {
    const ctx = this.ctx, f = this.world.fluid, ride = this.ride, k = this.k, dpr = this.cv.width / (this.cssW || this.cv.width);
    const base = this.glassBase, wall = this.glassWall, zRim = f.zRim, zG = zTopOfBody + base;
    const Rin = (z) => f.Rz(Math.max(0, Math.min(z, zRim - 1e-6))), Rout = (z) => Rin(Math.max(0.008, z)) + wall;
    const P = (x, y, z) => this.project(cam, x, y, zG + z);
    const thC = Math.atan2(cam.Cp[1], cam.Cp[0]), thL = thC + Math.PI / 2, thR = thC - Math.PI / 2;
    const Z = []; for (let z = 0; z <= zRim + 1e-9; z += 0.002) Z.push(z); if (Z[Z.length - 1] < zRim) Z.push(zRim);
    const gen = (th, z0, z1, rf, up) => { const zs = Z.filter((z) => z >= z0 - 1e-9 && z <= z1 + 1e-9); if (!up) zs.reverse(); zs.forEach((z) => { const p = P(rf(z) * Math.cos(th), rf(z) * Math.sin(th), z); ctx.lineTo(p[0], p[1]); }); };
    const arc = (z, rad, from, to) => { const n = 40; for (let q = 0; q <= n; q++) { const t = from + (to - from) * q / n, p = P(rad * Math.cos(t), rad * Math.sin(t), z); ctx.lineTo(p[0], p[1]); } };
    // the whole glass seen through, tinted
    ctx.beginPath(); { const p = P(Rout(0) * Math.cos(thL), Rout(0) * Math.sin(thL), -base); ctx.moveTo(p[0], p[1]); }
    gen(thL, 0, zRim, Rout, true); arc(zRim, Rout(zRim), thL, thR + 2 * Math.PI); gen(thR, 0, zRim, Rout, false); arc(-base, Rout(0), thR, thL); ctx.closePath();
    ctx.fillStyle = 'rgba(205,214,218,0.45)'; ctx.fill();
    if (!ride) return;

    // the stored surface and head on rings and angles: the outer ring is the wall at the surface's own height there
    const nr = this.nr, nth = this.nth, edge = [], S = [];
    for (let it = 0; it < nth; it++) {
      const th = 2 * Math.PI * it / nth;
      let v = ride.atInward(k, Rin(ride.fill), th); const r = Rin(Math.min(v[0], zRim)) - 0.0004; v = ride.atInward(k, r, th);
      edge.push([r, v[0], v[1]]);
    }
    for (let ir = 0; ir <= nr; ir++) {
      const row = [];
      for (let it = 0; it < nth; it++) {
        const th = 2 * Math.PI * it / nth, e = edge[it], r = e[0] * ir / nr, v = ir === nr ? [e[1], e[2]] : (ride.at(k, r * Math.cos(th), r * Math.sin(th)) || ride.atInward(k, r, th));
        row.push([r * Math.cos(th), r * Math.sin(th), v[0], v[1]]);
      }
      S.push(row);
    }
    const eAt = (th) => { const q = ((th / (2 * Math.PI) * nth) % nth + nth) % nth, i0 = Math.floor(q), t = q - i0, a = edge[i0], b = edge[(i0 + 1) % nth]; return [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)]; };
    const nearArc = (hOff, dir) => { const n = 64; for (let q = 0; q <= n; q++) { const t = dir > 0 ? thR + Math.PI * q / n : thL - Math.PI * q / n, e = eAt(t), p = P(e[0] * Math.cos(t), e[0] * Math.sin(t), e[1] + hOff * e[2]); ctx.lineTo(p[0], p[1]); } };

    // the body of the stout: its near face, from the surface along the near arc, down the glass to the floor and up again
    const eL = eAt(thL), eR = eAt(thR);
    ctx.beginPath(); { const p = P(eR[0] * Math.cos(thR), eR[0] * Math.sin(thR), eR[1]); ctx.moveTo(p[0], p[1]); }
    nearArc(0, 1); gen(thL, 0, eL[1], Rin, false); arc(0, Rin(0), thL, thR); gen(thR, 0, eR[1], Rin, true); ctx.closePath();
    const rS = Rin(ride.fill), pL = P(rS * Math.cos(thL), rS * Math.sin(thL), ride.fill / 2), pR = P(rS * Math.cos(thR), rS * Math.sin(thR), ride.fill / 2);
    const g = ctx.createLinearGradient(pL[0], 0, pR[0], 0);       // Beer–Lambert across the glass: ruby where the path is short
    for (let q = 0; q <= 16; q++) { const xr = -1 + 2 * q / 16, ell = 2 * rS * Math.sqrt(Math.max(0, 1 - xr * xr)), T = Math.exp(-this.kappa * ell); g.addColorStop(q / 16, rgb(mix(C.stoutDark, C.stoutRuby, T))); }
    ctx.fillStyle = g; ctx.fill();
    // a soft light down the body, as on a round glass
    { const gl = ctx.createLinearGradient(pL[0], 0, pR[0], 0); gl.addColorStop(0, 'rgba(255,255,255,0)'); gl.addColorStop(0.22, 'rgba(255,255,255,0.10)'); gl.addColorStop(0.3, 'rgba(255,255,255,0)'); gl.addColorStop(0.8, 'rgba(255,255,255,0)'); gl.addColorStop(0.88, 'rgba(255,255,255,0.06)'); gl.addColorStop(1, 'rgba(255,255,255,0)'); ctx.fillStyle = gl; ctx.fill(); }

    // the head seen through the glass: the band between the stout's surface and the head's top along the near arc
    ctx.beginPath(); { const p = P(eR[0] * Math.cos(thR), eR[0] * Math.sin(thR), eR[1]); ctx.moveTo(p[0], p[1]); }
    nearArc(0, 1); nearArc(1, -1); ctx.closePath();
    { const top = P(0, 0, ride.fill + 0.019), bot = P(0, 0, ride.fill), gh = ctx.createLinearGradient(0, top[1], 0, bot[1]);
      gh.addColorStop(0, rgb(C.cream)); gh.addColorStop(0.75, rgb(mix(C.cream, C.creamShade, 0.35))); gh.addColorStop(1, rgb(mix(C.cream, C.creamShade, 0.8))); ctx.fillStyle = gh; ctx.fill(); }

    // the top: the head's surface (or the bare stout where the head has gone), quads from far to near, lit softly
    const L = this.light, quads = [];
    const top = (ir, it) => { const s = S[ir][((it % nth) + nth) % nth]; return [s[0], s[1], s[2] + s[3], s[3]]; };
    for (let ir = 0; ir < nr; ir++) for (let it = 0; it < nth; it++) {
      const a = top(ir, it), b = top(ir + 1, it), c2 = top(ir + 1, it + 1), d = top(ir, it + 1);
      const ux = c2[0] - a[0], uy = c2[1] - a[1], uz = c2[2] - a[2], vx = d[0] - b[0], vy = d[1] - b[1], vz = d[2] - b[2];
      let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx; if (nz < 0) { nx = -nx; ny = -ny; nz = -nz; }
      const nl = Math.hypot(nx, ny, nz) || 1, mx = (a[0] + c2[0]) / 2, my = (a[1] + c2[1]) / 2, mz = (a[2] + c2[2]) / 2;
      const dep = (mx - cam.Cp[0]) * cam.d[0] + (my - cam.Cp[1]) * cam.d[1] + (zG + mz - cam.Cp[2]) * cam.d[2];
      quads.push([dep, [a, b, c2, d], (nx * L[0] + ny * L[1] + nz * L[2]) / nl, (a[3] + b[3] + c2[3] + d[3]) / 4, Math.hypot(mx, my) / rS]);
    }
    quads.sort((p, q) => q[0] - p[0]);
    for (const [, vs, lam, hfm, rr] of quads) {
      const foam = Math.min(1, hfm / 0.0015), l = Math.max(0, lam);
      let col = mix(mix(C.creamShade, C.creamLit, Math.min(1, 0.35 + 0.75 * l)), C.cream, 0.25 + 0.2 * rr);   // matt cream, a little deeper at the glass
      col = mix(mix(C.stoutDark, C.stoutTop, 0.4 + 0.6 * l), col, foam);
      ctx.beginPath(); vs.forEach((v, q) => { const p = P(v[0], v[1], v[2]); q ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); });
      ctx.closePath(); ctx.fillStyle = rgb(col); ctx.fill(); ctx.strokeStyle = rgb(col); ctx.lineWidth = 0.8 * dpr; ctx.stroke();
    }
    // the line where the stout meets the head, seen through the glass
    ctx.beginPath(); { const p = P(eR[0] * Math.cos(thR), eR[0] * Math.sin(thR), eR[1]); ctx.moveTo(p[0], p[1]); } nearArc(0, 1);
    ctx.strokeStyle = 'rgba(96,64,40,0.55)'; ctx.lineWidth = 1 * dpr; ctx.stroke();

    this.drawGlassFront(cam, P, zRim, Rin, Rout, thL, thR, gen, arc, base, f, dpr);
    if (this.letter) this.drawLettering(cam, P, Rout, thC, dpr);

    // what left the glass, where it was stored: drops of stout (dark) and lumps of head (cream), nearest last
    const pts = [], D = ride.D;
    for (let q = ride.dOff[k]; q < ride.dOff[k + 1]; q++) pts.push([ride.drops[3 * q] * D.qd, ride.drops[3 * q + 1] * D.qd, ride.drops[3 * q + 2] * D.qd, 0.0011, 0]);
    for (let q = ride.lOff[k]; q < ride.lOff[k + 1]; q++) pts.push([ride.lumps[4 * q] * D.qd, ride.lumps[4 * q + 1] * D.qd, ride.lumps[4 * q + 2] * D.qd, Math.cbrt(0.75 * ride.lumps[4 * q + 3] * D.qv / Math.PI), 1]);
    const scr = pts.map((d) => { const p = P(d[0], d[1], d[2]); return [p[2], p[0], p[1], Math.max(1.1 * dpr, cam.f * d[3] / p[2]), d[4]]; }).filter((p) => p[0] > 0.05);
    scr.sort((a, b) => b[0] - a[0]);
    for (const [, x, y, r, kind] of scr) {
      ctx.beginPath(); ctx.arc(x, y, r, 0, 2 * Math.PI);
      if (kind) { ctx.fillStyle = rgb(C.cream); ctx.fill(); ctx.strokeStyle = rgb(C.creamShade, 0.9); ctx.lineWidth = 0.6 * dpr; ctx.stroke(); }
      else { ctx.fillStyle = rgb(C.stoutDark, 0.92); ctx.fill(); }
    }
    this.lastEdge = edge;
  };

  // The lettering on the glass: the word GUINNESS in the house's title face and a small harp drawn here from strokes (an
  // original drawing, not the brewery's emblem), laid on the outside of the glass facing the camera and bent with it.
  View2.prototype.drawLettering = function (cam, P, Rout, thC, dpr) {
    const ctx = this.ctx, word = 'GUINNESS', zBase = 0.058, capH = 0.0085, font = '400 100px "Instrument Serif", serif', cap = 68;   // cap height of the face at 100 px
    const m = capH / cap; ctx.save(); ctx.font = font; ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
    const widths = [...word].map((c) => ctx.measureText(c).width + 9), total = widths.reduce((a, b) => a + b, 0) * m;
    const sgn = (() => { const a = P(Rout(zBase) * Math.cos(thC + 0.1), Rout(zBase) * Math.sin(thC + 0.1), zBase), b = P(Rout(zBase) * Math.cos(thC - 0.1), Rout(zBase) * Math.sin(thC - 0.1), zBase); return a[0] < b[0] ? -1 : 1; })();
    const on = (s, z) => { const R = Rout(z), th = thC + sgn * s / R; return P(R * Math.cos(th), R * Math.sin(th), z); };    // s: metres to the right along the glass
    let s = -total / 2;
    ctx.fillStyle = rgb(C.gold);
    [...word].forEach((c, i) => {
      const w = widths[i] * m, p0 = on(s, zBase), pR = on(s + w, zBase), pU = on(s, zBase + capH);
      ctx.setTransform((pR[0] - p0[0]) / widths[i], (pR[1] - p0[1]) / widths[i], (p0[0] - pU[0]) / cap, (p0[1] - pU[1]) / cap, p0[0], p0[1]);
      ctx.fillText(c, 0, 0); s += w;
    });
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    // the harp: neck, pillar, soundboard and strings, in millimetres on the glass (u to the right, w up from its foot)
    const z0 = zBase + capH + 0.006, sc = 0.001, U = (u, w) => on(u * sc, z0 + w * sc);
    const path = (pts, lw) => { ctx.beginPath(); pts.forEach((q, i) => { const p = U(q[0], q[1]); i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); }); ctx.strokeStyle = rgb(C.gold); ctx.lineWidth = lw * dpr; ctx.lineJoin = 'round'; ctx.lineCap = 'round'; ctx.stroke(); };
    const neck = [], pillar = [];
    for (let q = 0; q <= 12; q++) { const t = q / 12; neck.push([-5 + 10.5 * t, 17 + 2.2 * Math.sin(Math.PI * t) - 3.5 * t * t]); }
    for (let q = 0; q <= 12; q++) { const t = q / 12; pillar.push([5.5 + 1.6 * Math.sin(Math.PI * t), 15.7 - 15.7 * t]); }
    path(neck, 2.2); path(pillar, 2.2); path([[-5, 17], [-4.2, 9], [5.5, 0]], 2.6);
    for (let q = 0; q < 6; q++) { const u = -3 + 1.45 * q, t = (u + 5) / 10.5, wTop = 17 + 2.2 * Math.sin(Math.PI * t) - 3.5 * t * t, wBot = u < -4.2 ? 9 : 9 - 9 * (u + 4.2) / 9.7; path([[u, wTop - 0.4], [u, wBot + 0.4]], 0.9); }
    ctx.restore();
  };

  root.StoutRide = StoutRide; root.StoutView2 = View2;
})(typeof self !== 'undefined' ? self : this);
