/* Fig. 16, computed on Kaggle: plays the stored rides of the four-wheel cart (public/data/fig16/<date>/, listed in index-16.json) beside
 * Fig. 12's best stored ride on the same road (public/data/fig12/2026-11-14-run10/), on one clock. Computes nothing physical: each
 * stored frame (30 or 60 a second, the ride's own fps) holds the stout's surface, the head, drops and lumps (drawn by Fig. 12's StoutView2 and, on the right,
 * by Cart16View on top of it), the cart's pose and its control signals. No frame is interpolated; every file is checked against the
 * SHA-256 in its index. The one value read on the page from stored data is Fig. 12's tilt per frame (its files store only the largest),
 * read from Fig. 12's stored surface exactly as tools/fig12/kaggle/pack_ride.py reads it. */
(function () {
  'use strict';
  const D16 = '../data/fig16/2026-11-14/', D12 = '../data/fig12/2026-11-14-run10/';
  // Fig. 12's best stored ride on each road (index-jax.json: least head spilled, then least tilt): the kerb with the slosh LQR, the
  // gentle roads with joint control
  const BEST12 = { 'one sharp 30 mm bump': 'ride_sharp30_slosh.json', 'five 20 mm bumps in step with the swing': 'ride_resonant_joint.json', 'one 25 mm bump': 'ride_bump25_joint.json' };
  const $ = (id) => document.getElementById(id), fmt = (v, d) => (v == null || !isFinite(v)) ? '—' : v.toFixed(d);
  const GP = window.GUINNESS_GLASS, G16 = window.Cart16View.G;
  const Rz = (z) => { const f = Math.max(0, z) / GP.dz, i = Math.min(Math.floor(f), GP.R.length - 2); return GP.R[i] + (f - i) * (GP.R[i + 1] - GP.R[i]); };
  const zRim = (GP.R.length - 1) * GP.dz;

  async function sha256(buf) {
    if (!(window.crypto && crypto.subtle)) return null;
    return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', buf)), (b) => b.toString(16).padStart(2, '0')).join('');
  }
  async function load(url, want) {
    const buf = await (await fetch(url)).arrayBuffer(), sha = await sha256(buf);
    if (sha && want && sha !== want) throw new Error(url.split('/').pop() + ': the file does not match the fingerprint stored with it');
    const r = await new window.StoutRide(JSON.parse(new TextDecoder().decode(buf))).unpack(); r.sha = sha; r.checked = !!(sha && want); return r;
  }
  function pane(canvas, View, o) {
    const fluid = { modal: true, h0: 0.125, zRim: zRim, H: zRim, Rbox: Infinity, dx: 0.0015, Rz: Rz }, bumps = [];
    const zr = (x) => { let s = 0; for (const b of bumps) { const u = (x - b.x) / b.L; if (Math.abs(u) < 0.5) s += 0.5 * b.h * (1 + Math.cos(2 * Math.PI * u)); } return s; };
    const cart = { x: 0.5, vx: 0, zw: 0.04, zb: 0.14, Rw: 0.04, Mb: 1.5, ml: 0.43, Ls: 0.135, g: 9.81, k: 600, us: 0, glassFloor: 0.012, road: { zr: zr } };
    const v = new View(canvas, { fluid: fluid, cart: cart, drops: [] }, o); v.glassWall = 0.0032; v.glassBase = 0.014;
    return { v, cart, fluid, bumps };
  }
  // the tilt of a Fig. 12 frame: twice the cos(theta) part of the stored surface on the outer ring, as pack_ride.py reads it
  function tilt12(r, k) {
    const R = Rz(r.fill) - 0.5 * r.dx, n = 64; let s = 0;
    for (let j = 0; j < n; j++) { const th = 2 * Math.PI * j / n, h = r.atInward(k, R, th); s += h[0] * Math.cos(th); }
    return 2 * (2 / n) * s * 1000;
  }

  fetch(D16 + 'index-16.json').then((r) => r.json()).then(async (I16) => {
    const I12 = await (await fetch(D12 + 'index-jax.json')).json();
    const sha12 = {}; I12.files.forEach((f) => { sha12[f.path] = f.sha256; });
    const A = pane($('c12'), window.StoutView2, { viewHeight: 0.46, groundY: 0.86, elevDeg: 16, azimDeg: -24 });
    const B = pane($('c16'), window.Cart16View, { viewHeight: 0.56, groundY: 0.84, elevDeg: 16, azimDeg: -24 }); B.v.targetZ = 0.20;
    if (document.fonts && document.fonts.load) { try { await document.fonts.load('400 100px "Instrument Serif"'); } catch (e) { /* the lettering falls back to a serif */ } }
    // run 3 (15 November 2026: the turning deck's forces in the fluid, 60 pictures a second, control off on every road) where it was
    // computed, run 2 (14 November) otherwise; seed 1 of each
    const D16B = '../data/fig16/2026-11-15/'; let I16B = null;
    try { const rb = await fetch(D16B + 'index-16.json'); if (rb.ok) I16B = await rb.json(); } catch (e) { /* run 2 alone */ }
    const all = I16.files.map((f) => Object.assign({ dir: D16 }, f)).concat(I16B ? I16B.files.map((f) => Object.assign({ dir: D16B }, f)) : []).filter((f) => f.kind === 'ride' && !/seed2/.test(f.path));
    const pick = (road, ctrl) => { const c = all.filter((f) => f.road === road && f.ctrl === ctrl); return c.find((f) => f.dir === D16B) || c[0]; };
    const rides = []; Object.keys(BEST12).forEach((road) => ['full', 'off'].forEach((ctrl) => { const f = pick(road, ctrl); if (f) rides.push(f); }));
    const cache = new Map();
    let r12 = null, r16 = null, cur = -1, T = 0, playing = true, last = null, lastTxt = 0, busy = false, fade = null;
    const fps = (r) => r.fps || 30;   // stored pictures a second: 30 in Fig. 12 and Fig. 16's run 2, 60 from run 3
    const dur = () => Math.max((r12.frames - 1) / fps(r12), (r16.frames - 1) / fps(r16));
    const get = async (url, want) => { if (!cache.has(url)) cache.set(url, await load(url, want)); return cache.get(url); };

    // keep: the switch of the control system: the same road at the same ride time, the old picture cross-faded out over 0.45 s
    async function choose(i, keep) {
      if (busy || i === cur || i < 0) return; busy = true;
      const f = rides[i]; $('cap-t').textContent = 'loading ' + f.path + ' …';
      try {
        const [n16, n12] = await Promise.all([get(f.dir + f.path, f.sha256), get(D12 + BEST12[f.road], sha12[BEST12[f.road]])]);
        if (keep && r16) { const c = B.v.cv, o = document.createElement('canvas'); o.width = c.width; o.height = c.height; o.getContext('2d').drawImage(c, 0, 0); fade = { img: o, t0: performance.now() }; }
        r16 = n16; r12 = n12; cur = i;
        if (keep) T = Math.min(T, dur()); else { T = 0; playing = true; $('play').textContent = 'Pause'; }
        for (const [P, r] of [[A, r12], [B, r16]]) { P.bumps.length = 0; (r.D.bumps || []).forEach((b) => P.bumps.push(b)); P.fluid.h0 = r.fill; P.fluid.dx = r.dx; }
        [...$('ride-host').children].forEach((b) => b.setAttribute('aria-pressed', b.dataset.road === f.road ? 'true' : 'false'));
        $('ctl-sw').setAttribute('aria-pressed', f.ctrl === 'full' ? 'true' : 'false'); $('ctl-sw-v').textContent = f.ctrl === 'full' ? 'on' : 'off';
        $('h12').textContent = 'Fig. 12 · one wheel · ' + ({ slosh: 'slosh LQR', joint: 'joint control' })[r12.D.ctrl];
        $('h16').textContent = 'Fig. 16 · four wheels · control system ' + (f.ctrl === 'full' ? 'on' : 'off');
        $('ride-note').textContent = `${f.road[0].toUpperCase()}${f.road.slice(1)} at ${fmt(f.v0, 1)} m/s. Left: Fig. 12's best stored ride on this road, ${r12.D.name}. ` +
          `Right: ${f.path} (${f.dir.split('/').slice(-2, -1)[0]}), ${f.frames} stored pictures, ${fps(r16)} a second${f.seconds < f.task_end - 0.02 ? ', the run stopped early on Kaggle at ' + fmt(r16.D.t[r16.frames - 1], 2) + ' s' : ''}. ` +
          `Fingerprints ${r12.checked && r16.checked ? 'checked: both files match their index' : 'not checked (this browser cannot compute SHA-256)'}.`;
      } catch (e) { $('cap-t').textContent = e.message; }
      busy = false;
    }
    rides.forEach((f) => { f.task_end = f.road === 'one sharp 30 mm bump' ? 4 : 8; });
    const idx = (road, ctrl) => rides.findIndex((f) => f.road === road && f.ctrl === ctrl);
    Object.keys(BEST12).forEach((road) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'btn btn--ghost g-ride'; b.dataset.road = road;
      b.textContent = `${road[0].toUpperCase()}${road.slice(1)}, ${road === 'one sharp 30 mm bump' ? '1.5' : '1.0'} m/s`; b.setAttribute('aria-pressed', 'false');
      b.onclick = () => choose(idx(road, cur >= 0 ? rides[cur].ctrl : 'full')); $('ride-host').appendChild(b); });
    $('ctl-sw').onclick = () => { if (cur < 0) return; const f = rides[cur]; choose(idx(f.road, f.ctrl === 'full' ? 'off' : 'full'), true); };
    // the comparison, from the two indexes (stored numbers only)
    const tb = $('cmp').appendChild(document.createElement('tbody'));
    for (const road of Object.keys(BEST12)) {
      const f12 = I12.files.find((f) => f.path === BEST12[road]), m12 = f12.measured;
      const th = document.createElement('tr'); th.className = 'cmp-road'; th.innerHTML = `<th colspan="5">${road}, ${fmt(f12.v0, 1)} m/s</th>`; tb.appendChild(th);
      const row = (name, m) => { const tr = document.createElement('tr'); tr.innerHTML = `<td>${name}</td><td>${fmt(m.tilt_max_mm, 2)}</td><td>${fmt(m.head_spilled_ml, 3)}</td><td>${fmt(m.spilled_g, 2)}</td><td>${fmt(m.i_max_A != null ? m.i_max_A : m.i_max_stored_A, 2)}</td>`; tb.appendChild(tr); };
      row('Fig. 12, ' + ({ slosh: 'slosh LQR', joint: 'joint' })[f12.ctrl], m12);
      rides.filter((f) => f.road === road).forEach((f) => row('Fig. 16, control ' + (f.ctrl === 'full' ? 'on' : 'off') + (f.seconds < f.task_end - 0.02 ? ' *' : ''), f.measured));
    }
    $('play').onclick = () => { if (T >= dur() - 1e-9) T = 0; playing = !playing || T === 0; $('play').textContent = playing ? 'Pause' : 'Play'; };
    $('again').onclick = () => { T = 0; playing = true; $('play').textContent = 'Pause'; };
    $('tbar').addEventListener('input', () => { if (r12) T = $('tbar').value / 1000 * dur(); });
    function size() { for (const P of [A, B]) { const c = P.v.cv, r = c.parentElement.getBoundingClientRect(), d = Math.min(2, devicePixelRatio || 1); c.width = Math.max(2, Math.round(r.width * d)); c.height = Math.max(2, Math.round(r.height * d)); P.v.cssW = r.width; } }
    addEventListener('resize', size); size();

    // the 3D close-ups of the two pints (pint3d-view.js, an ES module that may load after this script)
    const close = { a: null, b: null };
    const mk3d = () => { if (close.a || !window.Pint3D || !$('p12')) return; close.a = new window.Pint3D($('p12'), GP); close.b = new window.Pint3D($('p16'), GP); close.a.size(); close.b.size(); };
    mk3d(); addEventListener('pint3d-ready', mk3d); addEventListener('resize', () => { if (close.a) { close.a.size(); close.b.size(); } });
    const lerpAt = (a, f) => { const i = Math.max(0, Math.min(a.length - 2, Math.floor(f))), t = Math.max(0, Math.min(1, f - i)); return a[i] + t * (a[i + 1] - a[i]); };   // the wheel's position between stored pictures (kinematics only)
    function tick(now) {
      requestAnimationFrame(tick);
      if (!r12 || !r16) return;
      const dt = last == null ? 0 : Math.min(0.1, (now - last) / 1000); last = now;
      if (playing) { T += dt; if (T >= dur()) { T = dur(); playing = false; $('play').textContent = 'Play'; } }
      const k1 = Math.min(r12.frames - 1, Math.round(T * fps(r12))), D1 = r12.D;
      Object.assign(A.cart, { x: D1.x[k1], xw: lerpAt(D1.x, T * fps(r12)), vx: D1.v[k1], zb: D1.zb[k1], zw: D1.zw[k1], us: D1.us ? D1.us[k1] : 0 });
      A.v.setFrame(r12, k1); A.v.draw();
      const k2 = Math.min(r16.frames - 1, Math.round(T * fps(r16))), D2 = r16.D;
      // the stored pose: axle heights, the deck's centre and pitch, each measured from its first stored value (the cart at rest on
      // the flat road); the actuators' stored force per axle, shared by its two struts
      B.cart.x = D2.x[k2]; B.cart.vx = D2.v[k2];
      B.v.pose = { zwF: D2.zf[k2] - D2.zf[0] + G16.Rw, zwR: D2.zr[k2] - D2.zr[0] + G16.Rw, zc: D2.zc[k2] - D2.zc[0] + G16.Rw + 0.098, pitch: D2.th[k2] - D2.th[0],
                   wheelAng: -lerpAt(D2.x, T * fps(r16)) / G16.Rw, wheelRate: D2.v[k2] / G16.Rw, us: [D2.uf[k2] / 2, D2.uf[k2] / 2, D2.ur[k2] / 2, D2.ur[k2] / 2] };
      B.v.setFrame(r16, k2); B.v.draw();
      if (close.a) { close.a.setFrame(r12, k1); close.a.render(); close.b.setFrame(r16, k2); close.b.render(); }
      if (fade) {                                                 // the switch: the last picture of the other ride fades out over 0.45 s
        const u = (now - fade.t0) / 450, g = B.v.cv.getContext('2d');
        if (u >= 1) fade = null; else { g.save(); g.globalAlpha = 1 - u; g.drawImage(fade.img, 0, 0); g.restore(); }
      }
      if (document.activeElement !== $('tbar')) $('tbar').value = Math.round(T / dur() * 1000);
      if (now - lastTxt > 250) {                                  // words rewritten four times a second
        lastTxt = now;
        $('t-out').textContent = `${fmt(T, 2)} of ${fmt(dur(), 1)} s`;
        $('a-tilt').textContent = fmt(Math.abs(tilt12(r12, k1)), 1) + ' mm'; $('a-head').textContent = fmt(D1.head_spill_ml[k1], 2) + ' mL'; $('a-stout').textContent = fmt(D1.spill_g[k1], 2) + ' g';
        $('b-tilt').textContent = fmt(Math.abs(D2.tilt_mm[k2]), 1) + ' mm'; $('b-head').textContent = fmt(D2.head_spill_ml[k2], 2) + ' mL'; $('b-stout').textContent = fmt(D2.spill_g[k2], 2) + ' g';
        $('b-pitch').textContent = fmt((D2.th[k2] - D2.th[0]) * 180 / Math.PI, 1) + '°'; $('b-i').textContent = fmt(D2.i[k2], 1) + ' A';
        $('b-u').textContent = fmt(D2.uf[k2], 0) + ' / ' + fmt(D2.ur[k2], 0) + ' N'; $('b-v').textContent = fmt(D2.v[k2], 2) + ' m/s';
        $('cap-t').textContent = `stored pictures ${k1 + 1} and ${k2 + 1}` + (k2 < Math.round(T * fps(r16)) ? ' (the right ride ended here)' : '');
      }
    }
    const q = new URLSearchParams(location.search);
    await choose(Math.max(0, rides.findIndex((f) => f.path === (q.get('ride') || 'kerb_full.json'))));
    if (q.get('t')) { T = +q.get('t'); playing = false; $('play').textContent = 'Play'; }
    requestAnimationFrame(tick);
    window.Guinness16 = { state: () => ({ T: T, cur: cur, playing: playing }), choose: choose, seek: (t) => { T = t; playing = false; $('play').textContent = 'Play'; } };
  }).catch((e) => { $('cap-t').textContent = 'data not loaded: ' + e.message; });
})();
