/* Fig. 12, computed on Kaggle: plays stored rides of the pint on the one-wheel cart (public/data/fig12/<date>/rides.json).
 * Computes nothing physical. Each stored frame holds the cart's position, speed, body and axle heights, the lean, the
 * spilled mass and the stout's surface on the polar grid of StoutView (17 rings x 64 angles, uint8 in 0.2 mm steps about
 * the fill, zlib-packed). The frame is handed to the website's own drawing code (stout-view.js) as a "fluid" whose
 * heightAt() reads the stored grid. Near the end of the computed time the playback slows smoothly to zero speed; only
 * there the pop-up about the pipeline fades in. Changing the ride cross-fades. */
(function () {
  'use strict';
  const DATA_URL = '../data/fig12/2026-11-12/rides.json';
  const SLOW = 3.0;          // s of ride before the computed end over which the playback slows to zero
  const $ = (id) => document.getElementById(id);
  const cv = $('cv'), pop = $('pop'), play = $('play'), tbar = $('tbar'), vbar = $('vbar');

  fetch(DATA_URL).then((r) => r.json()).then(start).catch((e) => { $('cap-t').textContent = 'data not loaded: ' + e.message; });

  async function unpack(r) {
    if (r.bytes) return;
    const s = atob(r.frames), a = new Uint8Array(s.length);
    for (let i = 0; i < s.length; i++) a[i] = s.charCodeAt(i);
    const st = new Blob([a]).stream().pipeThrough(new DecompressionStream('deflate'));
    r.bytes = new Uint8Array(await new Response(st).arrayBuffer());
  }

  async function start(D) {
    const G = window.GUINNESS_GLASS;
    const Rz = (z) => { const f = Math.max(0, z) / G.dz, i = Math.min(Math.floor(f), G.R.length - 2); return G.R[i] + (f - i) * (G.R[i + 1] - G.R[i]); };
    const zRim = (G.R.length - 1) * G.dz, Rh = Rz(D.fill), NR = D.nr, NTH = D.nth, M = NTH * (NR + 1);
    const fluid = {
      modal: true, h0: D.fill, zRim: zRim, H: zRim, Rbox: Infinity, dx: 0.0015, Rz: Rz, frame: null,
      columnHeights() {},
      heightAt(x, y) {          // bilinear on the stored polar grid
        const P = this.frame, r = Math.min(Math.hypot(x, y), Rh), th = Math.atan2(y, x);
        const fr = r / Rh * NR, ir = Math.min(Math.floor(fr), NR - 1), tr = fr - ir;
        const ft = ((th / (2 * Math.PI) * NTH) % NTH + NTH) % NTH, it = Math.floor(ft) % NTH, tt = ft - Math.floor(ft), it2 = (it + 1) % NTH;
        const v = (a, b) => D.fill + (P[a * NTH + b] - 128) * D.q;
        return (1 - tr) * ((1 - tt) * v(ir, it) + tt * v(ir, it2)) + tr * ((1 - tt) * v(ir + 1, it) + tt * v(ir + 1, it2));
      },
      columnHeightAt(x, y) { return this.heightAt(x, y); },
    };
    const cart = { x: 0, vx: 0, zw: 0, zb: 0, Rw: 0.04, Mb: 1.5, ml: D.ml, Ls: 0.135, g: 9.81, k: 600, us: 0, glassFloor: 0.012, ride: null,
      road: { zr: (x) => { const r = cart.ride, f = (x - r.road_x0) / r.road_dx, i = Math.floor(f); if (i < 0 || i > r.road_zr.length - 2) return 0; return r.road_zr[i] + (f - i) * (r.road_zr[i + 1] - r.road_zr[i]); } } };
    const view = new window.StoutView(cv, { fluid: fluid, cart: cart, drops: [] }, { viewHeight: 0.40, groundY: 0.95, elevDeg: 16, azimDeg: -24 });
    view.glassWall = 0.0032; view.glassBase = 0.014;
    glassLook(view);

    const rides = D.rides.slice().sort((a, b) => a.v0 - b.v0);
    vbar.max = rides.length - 1; vbar.value = Math.floor((rides.length - 1) / 2);
    $('road-name').textContent = 'Road: ' + rides[0].road + ' (the same road at every speed).';
    let ride = null, T = 0, rate = 1, playing = true, last = null, lastTxt = 0, ended = false;
    const dur = () => (ride.n - 1) / D.fps;

    async function pick(fade) {
      const r = rides[+vbar.value]; await unpack(r);
      const swap = () => { ride = r; cart.ride = r; T = 0; ended = false; hidePop(); $('v-out').textContent = r.v0.toFixed(2) + ' m/s (computed)'; };
      if (fade && ride) { cv.style.opacity = '0'; setTimeout(() => { swap(); cv.style.opacity = '1'; }, 350); } else swap();
    }
    function showPop() { pop.hidden = false; requestAnimationFrame(() => pop.classList.add('is-on')); }
    function hidePop() { pop.classList.remove('is-on'); setTimeout(() => { if (!pop.classList.contains('is-on')) pop.hidden = true; }, 600); }

    vbar.addEventListener('input', () => pick(true));
    tbar.addEventListener('input', () => { if (ride) { T = tbar.value / 1000 * dur(); ended = false; hidePop(); } });
    play.addEventListener('click', () => { playing = !playing; play.textContent = playing ? 'Pause' : 'Play'; });
    $('again').addEventListener('click', () => { cv.style.opacity = '0'; setTimeout(() => { T = 0; ended = false; hidePop(); cv.style.opacity = '1'; }, 350); });
    await pick(false);

    function tick(now) {
      if (ride && ride.bytes) {
        if (last != null && playing && !ended) {
          // the playback rate eases to zero over the last SLOW seconds: rate = sqrt(left / SLOW), which reaches the end
          const left = dur() - T;
          rate = left >= SLOW ? 1 : Math.sqrt(Math.max(0, left) / SLOW);
          T = Math.min(dur(), T + rate * (now - last) / 1000);
          if (dur() - T < 0.01) { T = dur(); ended = true; showPop(); }
        }
        last = now;
        const k = Math.min(ride.n - 1, Math.max(0, Math.round(T * D.fps)));
        fluid.frame = ride.bytes.subarray(k * M, (k + 1) * M);
        cart.x = ride.x[k]; cart.vx = ride.v[k]; cart.zw = ride.zw[k]; cart.zb = ride.zb[k];
        const rc = cv.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
        const W = Math.round(rc.width * dpr), H = Math.round(rc.height * dpr);
        if (W > 0 && (cv.width !== W || cv.height !== H)) { cv.width = W; cv.height = H; }
        view.cssW = rc.width || cv.width; view.draw();
        if (playing) tbar.value = Math.round(T / dur() * 1000);
        if (now - lastTxt > 250) {        // the words change four times a second
          lastTxt = now;
          $('t-out').textContent = (k / D.fps).toFixed(1) + ' of ' + dur().toFixed(0) + ' s';
          $('cap-t').textContent = rate < 0.999 && !ended ? 'slowing: computed data ends at ' + dur().toFixed(0) + ' s' : (ended ? 'end of computed data' : 'stored ride, real time');
          $('r-v').textContent = ride.v[k].toFixed(3) + ' m/s'; $('r-l').textContent = ride.lean[k].toFixed(1) + ' mm'; $('r-s').textContent = ride.spill[k].toFixed(1) + ' g';
        }
      }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  // the glass drawn as glass: denser toward the silhouette, long highlights, a bright rim, a heavy base (drawing only)
  function glassLook(view) {
    const baseFront = view.drawGlassFront.bind(view);
    view.drawGlassFront = function (cam, P, zRim, Rin, Rout, thL, thR, gen, arc, base, f, dpr) {
      const ctx = this.ctx, pl = P(Rout(f.h0) * Math.cos(thL), Rout(f.h0) * Math.sin(thL), f.h0), pr = P(Rout(f.h0) * Math.cos(thR), Rout(f.h0) * Math.sin(thR), f.h0);
      const outline = () => { ctx.beginPath(); { const p = P(Rout(0) * Math.cos(thL), Rout(0) * Math.sin(thL), -base); ctx.moveTo(p[0], p[1]); }
        gen(thL, 0, zRim, Rout, true); arc(zRim, Rout(zRim), thL, thR); gen(thR, 0, zRim, Rout, false); arc(-base, Rout(0), thR, thL); ctx.closePath(); };
      const gEdge = ctx.createLinearGradient(pl[0], 0, pr[0], 0);
      [[0, .42], [.05, .2], [.16, .05], [.5, .02], [.84, .05], [.95, .22], [1, .45]].forEach(([s, a]) => gEdge.addColorStop(s, `rgba(150,170,178,${a})`));
      outline(); ctx.fillStyle = gEdge; ctx.fill();
      ctx.save(); outline(); ctx.clip();
      for (const [off, w, a] of [[-0.62, 0.07, 0.55], [-0.40, 0.025, 0.35], [0.55, 0.04, 0.28]]) {
        const xa = pl[0] + (pr[0] - pl[0]) * (0.5 + off / 2), wpx = (pr[0] - pl[0]) * w, g = ctx.createLinearGradient(xa - wpx, 0, xa + wpx, 0);
        g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(0.5, `rgba(255,255,255,${a})`); g.addColorStop(1, 'rgba(255,255,255,0)');
        const top = P(0, 0, zRim * 0.97), bot = P(0, 0, 0.012); ctx.fillStyle = g; ctx.fillRect(xa - wpx, top[1], 2 * wpx, bot[1] - top[1]);
      }
      ctx.restore();
      ctx.beginPath(); { const p = P(Rout(0) * Math.cos(thL), Rout(0) * Math.sin(thL), -base); ctx.moveTo(p[0], p[1]); }
      arc(-base, Rout(0), thL, thR - 2 * Math.PI); { const p = P(Rin(0) * Math.cos(thR), Rin(0) * Math.sin(thR), 0); ctx.lineTo(p[0], p[1]); } arc(0, Rin(0), thR - 2 * Math.PI, thL); ctx.closePath();
      const pb = P(0, 0, -base), pt = P(0, 0, 0), gb = ctx.createLinearGradient(0, pb[1], 0, pt[1]);
      gb.addColorStop(0, 'rgba(120,140,148,0.55)'); gb.addColorStop(1, 'rgba(220,232,236,0.35)'); ctx.fillStyle = gb; ctx.fill();
      baseFront(cam, P, zRim, Rin, Rout, thL, thR, gen, arc, base, f, dpr);
      ctx.strokeStyle = 'rgba(255,255,255,0.85)'; ctx.lineWidth = 1.4 * dpr;
      ctx.beginPath(); { const p = P(Rout(zRim) * Math.cos(thR + 0.15), Rout(zRim) * Math.sin(thR + 0.15), zRim); ctx.moveTo(p[0], p[1]); } arc(zRim, Rout(zRim) - 0.0008, thR + 0.15, thR + 2.2); ctx.stroke();
    };
  }
})();
