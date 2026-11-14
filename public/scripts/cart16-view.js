/* Fig. 16 (prototype): the new cart drawn with Fig. 12's own engine. Cart16View extends StoutView2 (scripts/stout-view2.js,
 * not edited): the camera, the projection and, above all, drawGlass are Fig. 12's, so the glass is the same Guinness tulip with
 * its lettering and the stout and head are drawn from the same stored fields. Only the machine under the glass is new: a deck
 * on four wheels, each wheel on a swing arm hinged under the deck, a coil spring over a damper from the arm to a tower on the
 * deck with a voice-coil actuator and a load cell at its top, hub motors in the rear wheels, an IMU beside the glass's seat,
 * the controller, the battery and a road scanner on a boom. The glass is clamped to the deck and moves and tilts with it.
 * Computes nothing physical. The pose (each axle's height, the deck's height and pitch) is handed in by the page. */
(function (root) {
  'use strict';
  const SV2 = root.StoutView2;
  const INK = '#1c1518', MUTED = '#6b6166', WINE = '#7a1f2b', GOLD = '#c9a86a';
  const G = { wb: 0.22, yw: 0.088, Rw: 0.045, hw: 0.012, deckL: 0.31, deckW: 0.124, deckT: 0.012, armL: 0.078, yArm: 0.066, pivDrop: 0.022, towerH: 0.050 };

  function View(canvas, world, o) { SV2.call(this, canvas, world, o); this.roadW = 0.30; this.names = true; this.pose = { zwF: G.Rw, zwR: G.Rw, zc: 0.150, pitch: 0, wheelAng: 0, us: [0, 0, 0, 0] }; this.G = G; }
  View.prototype = Object.create(SV2.prototype);
  View.G = G;

  View.prototype.draw = function () {
    const ctx = this.ctx, W = this.cv.width, Hc = this.cv.height, c = this.world.cart, po = this.pose;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    const dpr = W / (this.cssW || W);
    if (this.viewHeight) this.scale = Hc / this.viewHeight;
    const cam = this.cam = this.camera(W, Hc), base = SV2.prototype.project.bind(this);
    const P = (p) => base(cam, p[0], p[1], p[2]);
    const zr = (x) => c.road.zr(x + c.x);
    // the deck's frame: a point (x, y, z) fixed to the deck, z measured up from the deck's underside at its middle
    const cp = Math.cos(po.pitch), sp = Math.sin(po.pitch);
    const T = (p) => [p[0] * cp - p[2] * sp, p[1], po.zc + p[0] * sp + p[2] * cp];
    const near = cam.Cp[1] < 0 ? -1 : 1;                       // the side of the cart toward the camera (sign of y)
    const depth = (p) => { const v = [p[0] - cam.Cp[0], p[1] - cam.Cp[1], p[2] - cam.Cp[2]]; return v[0] * cam.d[0] + v[1] * cam.d[1] + v[2] * cam.d[2]; };
    const path = (pts, close) => { ctx.beginPath(); pts.forEach((p, k) => { const q = P(p); k ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); }); if (close) ctx.closePath(); };
    const poly = (pts, fill, stroke, lw) => { path(pts, true); if (fill) { ctx.fillStyle = fill; ctx.fill(); } if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = (lw || 1.5) * dpr; ctx.lineJoin = 'round'; ctx.stroke(); } };
    const line = (pts, stroke, lw) => { path(pts, false); ctx.strokeStyle = stroke; ctx.lineWidth = lw * dpr; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.stroke(); };
    // a round bar from a to b of diameter d (m): an ink outline with the fill laid over it
    const tube = (a, b, d, fill, cap) => { const A = P(a), B = P(b), w = Math.max(1.5 * dpr, cam.f * d / (0.5 * (A[2] + B[2])));
      for (const [col, ww] of [[INK, w + 2.4 * dpr], [fill, w]]) { ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]); ctx.strokeStyle = col; ctx.lineWidth = ww; ctx.lineCap = cap || 'butt'; ctx.stroke(); } };
    // a box given by its eight corners (already in the world), faces toward the camera only
    const box = (c0, c1, fills, X) => {
      const v = []; for (const z of [c0[2], c1[2]]) for (const y of [c0[1], c1[1]]) for (const x of [c0[0], c1[0]]) v.push((X || ((q) => q))([x, y, z]));
      const F = [[0, 1, 3, 2, 'bottom'], [4, 6, 7, 5, 'top'], [0, 4, 5, 1, 'y0'], [2, 3, 7, 6, 'y1'], [0, 2, 6, 4, 'x0'], [1, 5, 7, 3, 'x1']];
      for (const f of F) {
        const a = v[f[0]], b = v[f[1]], d = v[f[2]], n = [(b[1] - a[1]) * (d[2] - a[2]) - (b[2] - a[2]) * (d[1] - a[1]), (b[2] - a[2]) * (d[0] - a[0]) - (b[0] - a[0]) * (d[2] - a[2]), (b[0] - a[0]) * (d[1] - a[1]) - (b[1] - a[1]) * (d[0] - a[0])];
        const cc = [0, 1, 2].map((i) => (v[f[0]][i] + v[f[2]][i]) / 2), out = [0, 1, 2].map((i) => cc[i] - (c0[i] + c1[i]) / 2), To = X ? X([(c0[0] + c1[0]) / 2, (c0[1] + c1[1]) / 2, (c0[2] + c1[2]) / 2]) : [(c0[0] + c1[0]) / 2, (c0[1] + c1[1]) / 2, (c0[2] + c1[2]) / 2];
        const o2 = [cc[0] - To[0], cc[1] - To[1], cc[2] - To[2]], s = n[0] * o2[0] + n[1] * o2[1] + n[2] * o2[2] < 0 ? -1 : 1;
        const view = [cc[0] - cam.Cp[0], cc[1] - cam.Cp[1], cc[2] - cam.Cp[2]];
        if (s * (n[0] * view[0] + n[1] * view[1] + n[2] * view[2]) < 0) poly([v[f[0]], v[f[1]], v[f[2]], v[f[3]]], fills[f[4]] || fills.side || fills.top, INK, 1.5);
      }
    };

    ctx.fillStyle = '#f5f1ea'; ctx.fillRect(0, 0, W, Hc);
    // ---- the road, as Fig. 12 draws it: a ribbon following z_r(x), the near ground down to the frame, a tick every 10 cm
    const span = 0.5 * W / this.scale * 1.7 + 0.3, yN = near * this.roadW / 2, yF = -yN, step = 0.01;
    const edge = (y, from, to) => { for (let x = from; from < to ? x <= to : x >= to; x += from < to ? step : -step) { const p = P([x, y, zr(x)]); ctx.lineTo(p[0], p[1]); } };
    ctx.beginPath(); { const p = P([-span, yN, zr(-span)]); ctx.moveTo(p[0], p[1]); } edge(yN, -span, span); ctx.lineTo(W + 10, Hc + 10); ctx.lineTo(-10, Hc + 10); ctx.closePath(); ctx.fillStyle = '#ded6c8'; ctx.fill();
    ctx.beginPath(); { const p = P([-span, yF, zr(-span)]); ctx.moveTo(p[0], p[1]); } edge(yF, -span, span); edge(yN, span, -span); ctx.closePath(); ctx.fillStyle = '#e9e2d6'; ctx.fill();
    ctx.beginPath(); { const p = P([-span, yF, zr(-span)]); ctx.moveTo(p[0], p[1]); } edge(yF, -span, span); ctx.strokeStyle = 'rgba(28,21,24,0.35)'; ctx.lineWidth = 1 * dpr; ctx.stroke();
    ctx.beginPath(); { const p = P([-span, yN, zr(-span)]); ctx.moveTo(p[0], p[1]); } edge(yN, -span, span); ctx.strokeStyle = INK; ctx.lineWidth = 2 * dpr; ctx.stroke();
    for (const yt of [-G.yw, G.yw]) { ctx.beginPath(); { const p = P([-span, yt, zr(-span)]); ctx.moveTo(p[0], p[1]); } edge(yt, -span, span); ctx.strokeStyle = 'rgba(28,21,24,0.18)'; ctx.lineWidth = 1 * dpr; ctx.stroke(); }
    ctx.fillStyle = MUTED; ctx.font = `${11 * dpr}px "IBM Plex Mono", monospace`; ctx.textAlign = 'center';
    for (let m = Math.ceil((c.x - span) * 10); m <= (c.x + span) * 10; m++) {
      const xr = m / 10 - c.x, p = P([xr, yN, zr(xr)]), q = P([xr, yN + near * (m % 10 === 0 ? 0.02 : 0.01), zr(xr)]);
      if (p[0] < -20 || p[0] > W + 20) continue;
      ctx.strokeStyle = MUTED; ctx.lineWidth = 1 * dpr; ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.stroke();
      if (m % 5 === 0) ctx.fillText(`${(m / 10).toFixed(1)} m`, q[0], q[1] + 14 * dpr);
    }

    // ---- the parts, each a small drawing routine with a depth, painted from far to near
    const items = [], put = (at, fn) => items.push({ d: depth(at), fn: fn });
    const wheel = (xa, side, zw, motor) => {
      const y0 = side * G.yw, yn = y0 + near * G.hw, yf = y0 - near * G.hw, R = G.Rw, ang = po.wheelAng;
      const circ = (y, rad) => { ctx.beginPath(); for (let k = 0; k <= 48; k++) { const t = k / 48 * 2 * Math.PI, p = P([xa + rad * Math.cos(t), y, zw + rad * Math.sin(t)]); k ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); } ctx.closePath(); };
      circ(yf, R); ctx.fillStyle = '#1f1a1c'; ctx.fill();
      ctx.fillStyle = '#231d20';
      for (let k = 0; k < 48; k++) { const t0 = k / 48 * 2 * Math.PI, t1 = (k + 1) / 48 * 2 * Math.PI; path([[t0, yf], [t1, yf], [t1, yn], [t0, yn]].map(([t, y]) => [xa + R * Math.cos(t), y, zw + R * Math.sin(t)]), true); ctx.fill(); }
      circ(yn, R); ctx.fillStyle = '#2a2326'; ctx.fill(); ctx.strokeStyle = INK; ctx.lineWidth = 1.5 * dpr; ctx.stroke();
      circ(yn, R * 0.72); ctx.fillStyle = '#d9d2c7'; ctx.fill(); ctx.stroke();
      ctx.strokeStyle = INK; ctx.lineWidth = 2 * dpr;
      for (let k = 0; k < 5; k++) { const a = ang + k * 2 * Math.PI / 5; line([[xa, yn, zw], [xa + 0.72 * R * Math.cos(a), yn, zw + 0.72 * R * Math.sin(a)]], INK, 2); }
      circ(yn, R * (motor ? 0.40 : 0.16)); ctx.fillStyle = motor ? WINE : INK; ctx.fill(); ctx.strokeStyle = INK; ctx.lineWidth = 1.5 * dpr; ctx.stroke();
      if (motor) { circ(yn, R * 0.10); ctx.fillStyle = GOLD; ctx.fill(); }
    };
    const corner = (sx, side, k) => {
      const xa = sx * G.wb / 2, zw = sx > 0 ? po.zwF : po.zwR, ya = side * G.yArm;
      const piv = T([xa + G.armL, ya, -G.pivDrop]), ax = [xa, ya, zw];
      const lo = [xa + 0.014 + (piv[0] - xa) * 0.12, ya, zw + 0.012 + (piv[2] - zw) * 0.12], hi = T([xa + 0.030, ya, G.deckT + G.towerH - 0.006]);
      const L = (t) => [lo[0] + (hi[0] - lo[0]) * t, lo[1] + (hi[1] - lo[1]) * t, lo[2] + (hi[2] - lo[2]) * t];
      // hanger under the deck with the hinge, the tower on the deck
      put(piv, () => { box([xa + G.armL - 0.012, ya - 0.007, -G.pivDrop - 0.008], [xa + G.armL + 0.012, ya + 0.007, 0], { side: '#cfc7ba', top: '#ddd5c8' }, T); const q = P(piv); ctx.beginPath(); ctx.arc(q[0], q[1], 3.2 * dpr, 0, 2 * Math.PI); ctx.fillStyle = GOLD; ctx.fill(); ctx.strokeStyle = INK; ctx.lineWidth = 1.2 * dpr; ctx.stroke(); });
      const yt = ya - side * 0.019;                              // the tower stands inboard of the strut; a pin joins them at the top
      put(T([xa + 0.030, yt - side * 0.01, G.deckT + G.towerH / 2]), () => { box([xa + 0.018, yt - 0.006, G.deckT], [xa + 0.042, yt + 0.006, G.deckT + G.towerH], { side: '#cfc7ba', top: '#e6dfd3', y0: '#d6cec1', y1: '#d6cec1' }, T); tube(T([xa + 0.030, yt, G.deckT + G.towerH - 0.006]), hi, 0.006, GOLD); });
      put([(piv[0] + ax[0]) / 2, ya, (piv[2] + ax[2]) / 2], () => { tube(piv, ax, 0.011, '#5a5054', 'round'); tube([xa, ya, zw], [xa, side * (G.yw - G.hw), zw], 0.008, '#8a8286'); });
      put([L(0.5)[0], ya + side * 0.02, L(0.5)[2]], () => {
        tube(L(0.0), L(0.46), 0.015, '#3a3236');                                             // the damper's body
        tube(L(0.46), L(0.74), 0.005, '#b9b2a8');                                            // its rod
        const u = [hi[0] - lo[0], hi[2] - lo[2]], n = Math.hypot(u[0], u[1]), ex = [u[1] / n, -u[0] / n], turns = 7, rs = 0.012, pts = [];   // the coil: a helix about the strut
        for (let q = 0; q <= turns * 24; q++) { const t = q / (turns * 24), a = 2 * Math.PI * turns * t, cpt = L(0.06 + 0.64 * t); pts.push([cpt[0] + rs * Math.cos(a) * ex[0], cpt[1] + rs * Math.sin(a), cpt[2] + rs * Math.cos(a) * ex[1]]); }
        line(pts, INK, 3.4); line(pts, '#9a9390', 1.2);
        tube(L(0.72), L(0.90), 0.026, WINE);                                                 // the voice-coil actuator
        tube(L(0.90), L(0.97), 0.018, GOLD);                                                 // the load cell
        const u_s = po.us[k] || 0;
        if (Math.abs(u_s) > 0.2) { const a0 = L(0.81), a1 = [a0[0], a0[1] + near * 0.03, a0[2]], a2 = [a1[0], a1[1], a1[2] + u_s / 4 * 0.01]; line([a1, a2], WINE, 2.5); const e = P(a2); ctx.fillStyle = WINE; ctx.font = `${10 * dpr}px "IBM Plex Mono", monospace`; ctx.textAlign = 'left'; ctx.fillText(u_s.toFixed(1) + ' N', e[0] + 5 * dpr, e[1] + 3 * dpr); }
      });
      put([xa, side * G.yw + near * 0.02, zw], () => wheel(xa, side, zw, sx < 0));
    };
    let k = 0; for (const sx of [1, -1]) for (const side of [1, -1]) corner(sx, side, k++);
    // the battery under the deck, the deck, the controller, the scanner on its boom
    put(T([0, 0, -0.03]), () => box([-0.07, -0.038, -0.034], [0.07, 0.038, -0.002], { side: '#4b4246', top: '#5a5054', y0: '#5a5054', y1: '#5a5054' }, T));
    put(T([0, 0, 0.004]), () => {
      box([-G.deckL / 2, -G.deckW / 2, 0], [G.deckL / 2, G.deckW / 2, G.deckT], { top: '#f3eee5', side: '#ddd5c8', y0: '#efe9df', y1: '#efe9df' }, T);
      ctx.fillStyle = MUTED; ctx.font = `${10 * dpr}px "IBM Plex Mono", monospace`; ctx.textAlign = 'center'; const q = P(T([-0.07, near * G.deckW / 2, G.deckT / 2])); ctx.fillText('DECK', q[0], q[1] + 3.5 * dpr);
    });
    put(T([-0.112, 0, 0.03]), () => {
      box([-0.146, -0.040, G.deckT], [-0.078, 0.040, G.deckT + 0.022], { top: '#4b4246', side: '#3a3236', y0: '#443b3f', y1: '#443b3f' }, T);
      for (let f = 0; f < 6; f++) box([-0.142, -0.034 + f * 0.0125, G.deckT + 0.022], [-0.082, -0.030 + f * 0.0125, G.deckT + 0.030], { top: '#cfc7ba', side: '#b9b2a8', y0: '#c4bcb0', y1: '#c4bcb0' }, T);
    });
    put(T([0.24, 0, 0.04]), () => {
      tube(T([G.deckL / 2 - 0.004, 0, G.deckT + 0.004]), T([0.235, 0, G.deckT + 0.030]), 0.007, '#8a8286');
      const h0 = T([0.245, 0, G.deckT + 0.022]), g0 = [h0[0] + 0.055, -0.07, zr(h0[0] + 0.055)], g1 = [h0[0] + 0.055, 0.07, zr(h0[0] + 0.055)];
      path([h0, g0, g1], true); ctx.fillStyle = 'rgba(122,31,43,0.10)'; ctx.fill(); line([g0, g1], WINE, 1.4);
      box([0.232, -0.022, G.deckT + 0.020], [0.262, 0.022, G.deckT + 0.042], { top: '#4b4246', side: '#3a3236', y0: '#443b3f', y1: '#443b3f' }, T);
    });
    // the seat plate with its clamp ring, the IMU beside it; then Fig. 12's glass itself, standing on the seat and tilting with the deck
    const zSeat = G.deckT + 0.004;
    put(T([0, 0, 0.09]), () => {
      const ring = (z, rad, fill, lw) => { ctx.beginPath(); for (let q = 0; q <= 64; q++) { const t = q / 64 * 2 * Math.PI, p = P(T([rad * Math.cos(t), rad * Math.sin(t), z])); q ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); } ctx.closePath(); if (fill) { ctx.fillStyle = fill; ctx.fill(); } ctx.strokeStyle = INK; ctx.lineWidth = lw * dpr; ctx.stroke(); };
      ring(G.deckT, 0.050, '#b9b2a8', 1.5); ring(zSeat, 0.050, '#cfc7ba', 1.5);
      box([0.054, near * 0.030 - 0.008, G.deckT], [0.070, near * 0.030 + 0.008, G.deckT + 0.005], { top: WINE, side: '#5c1620', y0: '#5c1620', y1: '#5c1620' }, T);     // the IMU
      const keep = this.project;
      this.project = (cm, x, y, z) => { const p = T([x, y, z]); return base(cm, p[0], p[1], p[2]); };   // Fig. 12's glass, in the deck's frame
      this.drawGlass(cam, zSeat);
      this.project = keep;
      // the clamp ring over the glass's foot, with three bolts
      for (let q = 0; q < 3; q++) { const a = q * 2.094 + 0.6; tube(T([0.043 * Math.cos(a), 0.043 * Math.sin(a), zSeat]), T([0.043 * Math.cos(a), 0.043 * Math.sin(a), zSeat + 0.014]), 0.006, GOLD); }
      ctx.beginPath(); for (let q = 0; q <= 40; q++) { const t = (near < 0 ? Math.PI : 0) + q / 40 * Math.PI, p = P(T([0.039 * Math.cos(t), 0.039 * Math.sin(t), zSeat + 0.011])); q ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); }
      ctx.strokeStyle = INK; ctx.lineWidth = 6.4 * dpr; ctx.lineCap = 'round'; ctx.stroke(); ctx.strokeStyle = WINE; ctx.lineWidth = 4 * dpr; ctx.stroke();
    });
    items.sort((a, b) => b.d - a.d).forEach((it) => it.fn());

    // where the names point (css px), for the page's labels
    const A = (p) => { const q = P(p); return [q[0] / dpr, q[1] / dpr]; };
    const fr = (side) => ({ xa: G.wb / 2, ya: side * G.yArm });
    const nf = fr(near), zF = po.zwF;
    const pivF = T([nf.xa + G.armL, nf.ya, -G.pivDrop]), loF = [nf.xa + 0.014 + (pivF[0] - nf.xa) * 0.12, nf.ya, zF + 0.012 + (pivF[2] - zF) * 0.12], hiF = T([nf.xa + 0.030, nf.ya, G.deckT + G.towerH - 0.006]);
    const LF = (t) => [loF[0] + (hiF[0] - loF[0]) * t, nf.ya, loF[2] + (hiF[2] - loF[2]) * t];
    this.anchors = {
      glass: A(T([-0.036, near * 0.01, zSeat + 0.014 + 0.085])), clamp: A(T([-0.039, near * 0.02, zSeat + 0.011])), imu: A(T([0.062, near * 0.030, G.deckT + 0.005])),
      ctl: A(T([-0.112, near * 0.02, G.deckT + 0.03])), battery: A(T([-0.04, near * 0.038, -0.02])), motor: A([-G.wb / 2, near * (G.yw + G.hw), po.zwR]),
      arm: A([(pivF[0] + nf.xa) / 2, nf.ya, (pivF[2] + zF) / 2]), hinge: A(pivF), spring: A(LF(0.35)), coil: A(LF(0.81)), cell: A(LF(0.94)),
      encoder: A([G.wb / 2, near * (G.yw + G.hw), zF]), scanner: A(T([0.247, near * 0.022, G.deckT + 0.031])), road: A([0.30, near * 0.07, zr(0.30)]),
    };
  };
  root.Cart16View = View;
})(typeof self !== 'undefined' ? self : this);
