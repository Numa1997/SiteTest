/* Fig. 12 computed on Kaggle: the live preview, computed in the visitor's browser where Kaggle has not computed yet.
 * Runs the site's own coarse solver (stout-cart.js: APIC on a 4 mm grid, half the glass mirrored, the same one-wheel cart
 * with the motor holding the set speed) over the same road as the stored rides, and sends one frame per 1/30 s of ride in
 * the stored rides' format: the surface on StoutView's polar grid (17 rings x 64 angles, uint8 in steps of q about the
 * fill), the cart's position, speed, body and axle heights, the lean (front wall minus back wall, before rounding) and the
 * spilled mass. The page draws these frames with the same code as Kaggle's and labels them as a preview.
 * Known to differ from Kaggle (docs/simulations/fig12-beer-slosh.md): 4 mm grid instead of 1.5 mm, 25,666 particles
 * instead of 1,002,808, half glass mirrored; its free swing is 3.21 Hz (6 % slow against 3.42 Hz, check.cjs freq).
 * Measured speed: 0.23 x real time on one thread (Node 22, 12 November 2026); slower on phones. */
importScripts('guinness-glass.js', 'stout-cart.js', 'stout-view.js');

onmessage = function (e) {
  const o = e.data, G = self.GUINNESS_GLASS, NR = o.nr, NTH = o.nth, M = NTH * (NR + 1);
  const t0 = performance.now();
  const w = new StoutCart.World({
    fluid: { dx: 0.004, profile: G, h0: o.fill, H: (G.R.length - 1) * G.dz + 0.03 },
    road: { bumps: o.bumps, Rw: 0.04, xmin: -1, xmax: 0.5 + o.v0 * o.n / o.fps * 1.2 + 2 },
    cart: { x0: 0.5, Rw: 0.04, Ls: 0.135, v0: o.v0, ctrl: 'speed', susp: false },
    dtMax: 1 / 200
  });
  // the drawing code's own reading of the surface (StoutView.surface: column heights, bicubic, wall extension)
  const v = Object.create(self.StoutView.prototype); v.world = w; v.nr = NR; v.nth = NTH;
  const m0 = w.fluid.liquidMass();
  let k = 0;
  function frame() {
    const H = v.surface(), bytes = new Uint8Array(M);
    for (let ir = 0; ir <= NR; ir++) for (let j = 0; j < NTH; j++) bytes[ir * NTH + j] = Math.max(0, Math.min(255, Math.round((H[ir][j] - o.fill) / o.q) + 128));
    const c = w.cart;
    postMessage({ k: k, bytes: bytes, x: c.x, v: c.vx, zb: c.zb, zw: c.zw, lean: (H[NR][0] - H[NR][NTH / 2]) * 1000,
      spill: Math.max(0, (m0 - w.fluid.liquidMass()) * 1000), wall: (performance.now() - t0) / 1000, t: w.t, np: w.fluid.np }, [bytes.buffer]);
    k++;
    if (k < o.n) { w.advance(1 / o.fps); setTimeout(frame, 0); }   // a turn of the message loop between frames
    else postMessage({ done: true, wall: (performance.now() - t0) / 1000 });
  }
  frame();
};
