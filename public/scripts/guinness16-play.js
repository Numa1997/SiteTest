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
    // (the store is handed to the drawing as deckStore, not ds: with ds, Fig. 12's inherited drawing would write its own names)
    if (document.fonts && document.fonts.load) { try { await document.fonts.load('400 100px "Instrument Serif"'); } catch (e) { /* the lettering falls back to a serif */ } }
    // run 3 (15 November 2026: the turning deck's forces in the fluid, 60 pictures a second, control off on every road) where it was
    // computed, run 2 (14 November) otherwise; seed 1 of each
    const D16B = '../data/fig16/2026-11-15/'; let I16B = null;
    try { const rb = await fetch(D16B + 'index-16.json'); if (rb.ok) I16B = await rb.json(); } catch (e) { /* run 2 alone */ }
    const all = I16.files.map((f) => Object.assign({ dir: D16 }, f)).concat(I16B ? I16B.files.map((f) => Object.assign({ dir: D16B }, f)) : []).filter((f) => f.kind === 'ride' && !/seed2/.test(f.path));
    const pick = (road, ctrl) => { const c = all.filter((f) => f.road === road && f.ctrl === ctrl); return c.find((f) => f.dir === D16B) || c[0]; };
    const rides = []; Object.keys(BEST12).forEach((road) => ['full', 'off'].forEach((ctrl) => { const f = pick(road, ctrl); if (f) rides.push(f); }));
    const cache = new Map();

    /* ---------- the store (scripts/dataset.js): every number the page shows, written where it is set; the data panel
       (scripts/datalog.js, appended once the store is declared) only reads it. Nothing physical is computed here: the rides'
       arrays are copied as stored, the values "now" are the stored values at the picture on screen. ---------- */
    const Sim = window.Sim, ds = Sim && Sim.dataset ? Sim.dataset({ title: 'Fig. 16 computed on Kaggle', attrs: { figure: 16, page: 'guinness-cart-control.html',
      kaggle_notebook: I16B ? I16B.kaggle && I16B.kaggle.url : I16.kaggle && I16.kaggle.url } }) : null;
    const SV = (n, t, a) => ds.var(n, [], t, a), AV = (n, dim, a) => ds.var(n, [dim], Float64Array, a);
    const RUN = 'Kaggle (run16.py), stored in the ride file', RIDE = 'choose(), copied from the ride file';
    if (ds) {
      // what the reader chose, and the files
      SV('road', 'str', { symbol: 'road', long_name: 'the road of the chosen ride', computed_in: 'Road buttons' });
      SV('ctrl_on', 'bool', { symbol: 'control', long_name: 'the new cart’s control system is on in the ride on the right', computed_in: 'Control system switch' });
      SV('v0', 'float', { symbol: 'v<sub>0</sub>', units: 'm/s', long_name: 'set speed of the chosen ride', computed_in: 'index-16.json', digits: 2 });
      SV('ride16', 'str', { symbol: 'file<sub>16</sub>', long_name: 'the stored ride on the right (Fig. 16)', computed_in: 'choose()' });
      SV('ride12', 'str', { symbol: 'file<sub>12</sub>', long_name: 'Fig. 12’s best stored ride on the same road, on the left', computed_in: 'choose()' });
      SV('sha16', 'str', { symbol: 'SHA-256<sub>16</sub>', long_name: 'fingerprint of the right ride file as fetched, computed in this browser', computed_in: 'load(): crypto.subtle.digest' });
      SV('sha12', 'str', { symbol: 'SHA-256<sub>12</sub>', long_name: 'fingerprint of the left ride file as fetched, computed in this browser', computed_in: 'load(): crypto.subtle.digest' });
      SV('nb_version', 'int', { symbol: 'version', long_name: 'version of the Kaggle GPU notebook that computed the right ride', computed_in: 'index-16.json', digits: 0 });
      SV('fps16', 'float', { symbol: 'f<sub>16</sub>', units: '1/s', long_name: 'stored pictures a second of the right ride', computed_in: 'the ride file', digits: 0 });
      SV('fps12', 'float', { symbol: 'f<sub>12</sub>', units: '1/s', long_name: 'stored pictures a second of the left ride', computed_in: 'the ride file', digits: 0 });
      SV('frames16', 'int', { symbol: 'N<sub>16</sub>', long_name: 'stored pictures of the right ride', computed_in: 'the ride file', digits: 0 });
      SV('frames12', 'int', { symbol: 'N<sub>12</sub>', long_name: 'stored pictures of the left ride', computed_in: 'the ride file', digits: 0 });
      SV('dur', 'float', { symbol: 'T<sub>ride</sub>', units: 's', long_name: 'length of the playback: the longer of the two stored rides', computed_in: 'dur()', formula: 'max((N<sub>12</sub> − 1)/f<sub>12</sub>, (N<sub>16</sub> − 1)/f<sub>16</sub>)', digits: 3 });
      SV('head_ml0', 'float', { symbol: 'V<sub>head,0</sub>', units: 'mL', long_name: 'volume of the head of foam at the start of the right ride', computed_in: RUN + ' (books.head_ml0)', digits: 4 });
      // the stored rides, as stored
      ds.dim('k', 1); ds.dim('k12', 1);
      ds.coord('t16', 'k', Float64Array, { symbol: 't<sub>k</sub>', units: 's', long_name: 'ride time of stored picture k (right)', computed_in: RIDE, formula: 'k / f<sub>16</sub>', digits: 4 });
      AV('tilt16', 'k', { symbol: 'τ<sub>k</sub>', units: 'mm', long_name: 'tilt of the stout: twice the cos θ part of the surface on the outer ring', computed_in: RUN, digits: 3 });
      AV('th16', 'k', { symbol: 'θ<sub>k</sub>', units: 'rad', long_name: 'pitch angle of the deck, as stored (its first value is the cart at rest)', computed_in: RUN, digits: 6 });
      AV('cur16', 'k', { symbol: 'i<sub>k</sub>', units: 'A', long_name: 'hub-motor current', computed_in: RUN, digits: 3 });
      AV('uf16', 'k', { symbol: 'u<sub>f,k</sub>', units: 'N', long_name: 'actuator force of the front axle (its two struts together)', computed_in: RUN, digits: 2 });
      AV('ur16', 'k', { symbol: 'u<sub>r,k</sub>', units: 'N', long_name: 'actuator force of the rear axle (its two struts together)', computed_in: RUN, digits: 2 });
      AV('v16', 'k', { symbol: 'v<sub>k</sub>', units: 'm/s', long_name: 'cart speed', computed_in: RUN, digits: 4 });
      AV('hglass16', 'k', { symbol: 'V<sub>glass,k</sub>', units: 'mL', long_name: 'head of foam still in the glass', computed_in: RUN, digits: 4 });
      AV('hspill16', 'k', { symbol: 'V<sub>spill,k</sub>', units: 'mL', long_name: 'head of foam spilled over the rim so far', computed_in: RUN, digits: 4 });
      AV('sspill16', 'k', { symbol: 'm<sub>s,k</sub>', units: 'g', long_name: 'stout spilled over the rim so far', computed_in: RUN, digits: 3 });
      AV('hspill12', 'k12', { symbol: 'V<sub>spill,12</sub>', units: 'mL', long_name: 'Fig. 12: head of foam spilled so far', computed_in: 'Kaggle (Fig. 12 run 10), stored in the ride file', digits: 4 });
      AV('sspill12', 'k12', { symbol: 'm<sub>s,12</sub>', units: 'g', long_name: 'Fig. 12: stout spilled so far', computed_in: 'Kaggle (Fig. 12 run 10), stored in the ride file', digits: 3 });
      // playback now
      SV('playing', 'bool', { symbol: 'playing', long_name: 'the playback is running', computed_in: 'Play / Pause button' });
      SV('t_play', 'float', { symbol: 't', units: 's', long_name: 'ride time on screen, one clock for both rides', computed_in: 'tick()', formula: 't += Δt<sub>wall</sub> (at most 0.1 s a frame)', digits: 3, updates: 'every frame' });
      SV('k16', 'int', { symbol: 'k', long_name: 'stored picture on the right (no picture is interpolated)', computed_in: 'tick()', formula: 'min(N<sub>16</sub> − 1, round(t f<sub>16</sub>))', digits: 0, updates: 'every frame' });
      SV('k12', 'int', { symbol: 'k<sub>12</sub>', long_name: 'stored picture on the left', computed_in: 'tick()', formula: 'min(N<sub>12</sub> − 1, round(t f<sub>12</sub>))', digits: 0, updates: 'every frame' });
      SV('tilt_now', 'float', { symbol: 'τ', units: 'mm', long_name: 'tilt of the stout on the right now', computed_in: 'tick()', formula: 'τ<sub>k</sub>', digits: 3, updates: 'every frame' });
      SV('pitch_now', 'float', { symbol: 'Δθ', units: '°', long_name: 'deck pitch now, from its value at rest', computed_in: 'tick()', formula: '(θ<sub>k</sub> − θ<sub>0</sub>) 180/π', digits: 3, updates: 'every frame' });
      SV('cur_now', 'float', { symbol: 'i', units: 'A', long_name: 'hub-motor current now', computed_in: 'tick()', formula: 'i<sub>k</sub>', digits: 3, updates: 'every frame' });
      SV('uf_now', 'float', { symbol: 'u<sub>f</sub>', units: 'N', long_name: 'front actuators now', computed_in: 'tick()', formula: 'u<sub>f,k</sub>', digits: 2, updates: 'every frame' });
      SV('ur_now', 'float', { symbol: 'u<sub>r</sub>', units: 'N', long_name: 'rear actuators now', computed_in: 'tick()', formula: 'u<sub>r,k</sub>', digits: 2, updates: 'every frame' });
      SV('v_now', 'float', { symbol: 'v', units: 'm/s', long_name: 'cart speed now', computed_in: 'tick()', formula: 'v<sub>k</sub>', digits: 4, updates: 'every frame' });
      SV('hglass_now', 'float', { symbol: 'V<sub>glass</sub>', units: 'mL', long_name: 'head in the glass now', computed_in: 'tick()', formula: 'V<sub>glass,k</sub>', digits: 4, updates: 'every frame' });
      SV('hspill_now', 'float', { symbol: 'V<sub>spill</sub>', units: 'mL', long_name: 'head spilled so far, now', computed_in: 'tick()', formula: 'V<sub>spill,k</sub>', digits: 4, updates: 'every frame' });
      SV('sspill_now', 'float', { symbol: 'm<sub>s</sub>', units: 'g', long_name: 'stout spilled so far, now', computed_in: 'tick()', formula: 'm<sub>s,k</sub>', digits: 3, updates: 'every frame' });
      SV('head_res', 'float', { symbol: 'r<sub>head</sub>', units: 'mL', long_name: 'the head’s books: in the glass + spilled − at the start (zero if no foam is lost or made)', computed_in: 'tick()', formula: 'V<sub>glass</sub> + V<sub>spill</sub> − V<sub>head,0</sub>', digits: 6, updates: 'every frame' });
      SV('tilt12_now', 'float', { symbol: 'τ<sub>12</sub>', units: 'mm', long_name: 'Fig. 12: tilt now, read on this page from the stored surface (Fig. 12’s files store only the largest)', computed_in: 'tilt12(): as pack_ride.py reads it', formula: '2 (2/64) Σ<sub>j</sub> h(R − Δx/2, θ<sub>j</sub>) cos θ<sub>j</sub>', digits: 3, updates: 'every frame' });
      SV('hspill12_now', 'float', { symbol: 'V<sub>spill,12</sub>', units: 'mL', long_name: 'Fig. 12: head spilled so far, now', computed_in: 'tick()', digits: 4, updates: 'every frame' });
      SV('sspill12_now', 'float', { symbol: 'm<sub>s,12</sub>', units: 'g', long_name: 'Fig. 12: stout spilled so far, now', computed_in: 'tick()', digits: 3, updates: 'every frame' });
      SV('k_text16', 'int', { symbol: 'k<sub>text</sub>', long_name: 'the right picture whose numbers the readings show (rewritten 4 times a second)', computed_in: 'tick()', digits: 0 });
      SV('k_text12', 'int', { symbol: 'k<sub>12,text</sub>', long_name: 'the left picture whose numbers the readings show', computed_in: 'tick()', digits: 0 });
      // the drawing: where the deck was drawn (written by cart16-view.js once it records it; NaN until then)
      for (const [n, l] of [['deck_px_fx', 'screen x of the deck top’s front edge'], ['deck_px_fy', 'screen y of the deck top’s front edge'], ['deck_px_rx', 'screen x of the deck top’s rear edge'], ['deck_px_ry', 'screen y of the deck top’s rear edge']]) {
        SV(n, 'float', { symbol: n.replace('deck_px_', 'P<sub>') + '</sub>', units: 'px', long_name: l + ', as drawn (css px)', computed_in: 'Cart16View.draw()', digits: 2 }); ds.set(n, NaN);
      }
      B.v.deckStore = ds;
    }
    // the chosen ride into the store, as stored
    function fillRide(f) {
      if (!ds) return;
      const D2 = r16.D, D1 = r12.D, N = r16.frames, N1 = r12.frames;
      ds.dim('k', N); ds.dim('k12', N1);
      ['t16', 'tilt16', 'th16', 'cur16', 'uf16', 'ur16', 'v16', 'hglass16', 'hspill16', 'sspill16'].forEach((n) => ds.alloc(n)); ds.alloc('hspill12'); ds.alloc('sspill12');
      const cp = (n, a) => { const o = ds.get(n); for (let k = 0; k < o.length; k++) o[k] = a ? a[k] : NaN; ds.touch(n); };
      const t = ds.get('t16'); for (let k = 0; k < N; k++) t[k] = k / fps(r16); ds.touch('t16');
      cp('tilt16', D2.tilt_mm); cp('th16', D2.th); cp('cur16', D2.i); cp('uf16', D2.uf); cp('ur16', D2.ur); cp('v16', D2.v);
      cp('hglass16', D2.head_glass_ml); cp('hspill16', D2.head_spill_ml); cp('sspill16', D2.spill_g); cp('hspill12', D1.head_spill_ml); cp('sspill12', D1.spill_g);
      ds.set('road', f.road); ds.set('ctrl_on', f.ctrl === 'full'); ds.set('v0', f.v0); ds.set('ride16', f.dir.split('/').slice(-2, -1)[0] + '/' + f.path); ds.set('ride12', BEST12[f.road]);
      ds.set('sha16', r16.sha || '—'); ds.set('sha12', r12.sha || '—'); ds.set('nb_version', f.dir === D16B && I16B ? I16B.kaggle.version : I16.kaggle.version);
      ds.set('fps16', fps(r16)); ds.set('fps12', fps(r12)); ds.set('frames16', N); ds.set('frames12', N1); ds.set('dur', dur());
      ds.set('head_ml0', D2.books ? D2.books.head_ml0 : NaN);
    }
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
        r16 = n16; r12 = n12; cur = i; if (r16.D.cart) window.Cart16View.fromCart(r16.D.cart);
        if (keep) T = Math.min(T, dur()); else { T = 0; playing = true; $('play').textContent = 'Pause'; }
        fillRide(f);
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
    // ?no3d=1 leaves the 3D close-ups out (the data panel does not use them; panel16_check.py loads the page this way, because software
    // WebGL on a test machine can take many seconds a picture and blocks the page)
    const NO3D = new URLSearchParams(location.search).get('no3d') === '1';
    const mk3d = () => { if (NO3D || close.a || !window.Pint3D || !$('p12')) return; close.a = new window.Pint3D($('p12'), GP); close.b = new window.Pint3D($('p16'), GP); close.a.size(); close.b.size(); };
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
      // the stored pose, as stored: the axles' heights and the deck's centre of mass above the road, and the deck's pitch (one geometry:
      // the drawn cart takes its wheelbase, wheel radius and hinge depth from the ride's stored cart, Cart16View.fromCart)
      B.v.pose = { zwF: D2.zf[k2], zwR: D2.zr[k2], zc: D2.zc[k2], pitch: D2.th[k2],
                   wheelAng: -lerpAt(D2.x, T * fps(r16)) / G16.Rw, wheelRate: D2.v[k2] / G16.Rw, us: [D2.uf[k2] / 2, D2.uf[k2] / 2, D2.ur[k2] / 2, D2.ur[k2] / 2] };
      B.v.setFrame(r16, k2); B.v.draw();
      if (ds) {                                                   // the store, at the picture on screen
        ds.set('playing', playing); ds.set('t_play', T); ds.set('k16', k2); ds.set('k12', k1);
        ds.set('tilt_now', D2.tilt_mm[k2]); ds.set('pitch_now', (D2.th[k2] - D2.th[0]) * 180 / Math.PI); ds.set('cur_now', D2.i[k2]);
        ds.set('uf_now', D2.uf[k2]); ds.set('ur_now', D2.ur[k2]); ds.set('v_now', D2.v[k2]);
        const hg = D2.head_glass_ml ? D2.head_glass_ml[k2] : NaN, hs = D2.head_spill_ml[k2];
        ds.set('hglass_now', hg); ds.set('hspill_now', hs); ds.set('sspill_now', D2.spill_g[k2]); ds.set('head_res', hg + hs - ds.get('head_ml0'));
        ds.set('tilt12_now', tilt12(r12, k1)); ds.set('hspill12_now', D1.head_spill_ml[k1]); ds.set('sspill12_now', D1.spill_g[k1]);
      }
      if (close.a) {
        close.a.setFrame(r12, k1); close.a.render();
        // the realistic 3D view of Fig. 16 carries the pint on the 3D cart over the road (cart3d.js), moved by the same stored pose
        if (close.b.setCart && !close.b.cart) close.b.setCart(G16);
        if (close.b.setPose) close.b.setPose(B.v.pose, (x) => B.cart.road.zr(x + B.cart.x), B.cart.x);
        close.b.setFrame(r16, k2); close.b.render();
      }
      if (fade) {                                                 // the switch: the last picture of the other ride fades out over 0.45 s
        const u = (now - fade.t0) / 450, g = B.v.cv.getContext('2d');
        if (u >= 1) fade = null; else { g.save(); g.globalAlpha = 1 - u; g.drawImage(fade.img, 0, 0); g.restore(); }
      }
      if (document.activeElement !== $('tbar')) $('tbar').value = Math.round(T / dur() * 1000);
      if (now - lastTxt > 250) {                                  // words rewritten four times a second
        lastTxt = now; if (ds) { ds.set('k_text16', k2); ds.set('k_text12', k1); }
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
    if (ds) { defineData(); const dl = document.createElement('script'); dl.src = '../scripts/datalog.js'; document.body.appendChild(dl); }   // the data panel, once the store holds a ride

    /* ---------- the data panel's hooks: per value, the stored number, the formula recomputed from stored inputs, and the
       picture read back (the words of the readings, or a pixel where the drawing records where it drew) ---------- */
    function defineData() {
      const g = (n) => ds.get(n), inp = (n, s, u, d) => [s, g(n), u, d], K = () => g('k16'), Kt = () => g('k_text16'), Kt12 = () => g('k_text12');
      const atNow = (arr, s) => () => ({ formula: s + ' of the stored ride at the picture on screen, k = ' + K(), inputs: [inp('k16', 'k', '', 0)], value: g(arr)[K()] });
      // the readings box read back: its words must be the stored value at the picture they were written for, formatted as the page formats it
      const text = (id, want, lab, k) => () => {
        const got = $(id).textContent;
        return { what: 'the readings, “' + lab + '”', drawn: '“' + got + '”', expected: '“' + want() + '”, the stored value at picture ' + k(), ok: got === want(),
          note: 'The words are rewritten 4 times a second, so they show picture k<sub>text</sub>, which may trail the picture on screen by up to a quarter second while it plays.' };
      };
      const at16 = (a) => r16.D[a][Kt()], at12 = (a) => r12.D[a][Kt12()];
      // a pixel of the right figure where the drawing says it drew the deck: it must be drawn (alpha first), and not the paper
      function deckPixel(xn, yn, what) {
        const x = g(xn), y = g(yn);
        if (!isFinite(x) || !isFinite(y)) return { what: what, drawn: 'not recorded', expected: 'the deck’s top edge', ok: false, note: 'Cart16View.draw() does not yet record where it draws the deck (deckStore); until it does, only the readings are read back.' };
        const c = B.v.cv, dpr = c.width / c.getBoundingClientRect().width, d = B.v.ctx.getImageData(Math.floor(x * dpr), Math.floor(y * dpr), 1, 1).data;
        return { what: what + ', (' + fmt(x, 1) + ', ' + fmt(y, 1) + ') css px', drawn: d[3] === 0 ? 'nothing (transparent)' : 'rgb(' + d[0] + ', ' + d[1] + ', ' + d[2] + ')',
          expected: 'an opaque pixel of the deck', ok: d[3] > 0, note: 'Alpha is tested first: a transparent pixel would pass any colour test.' };
      }
      // the panes of the figure, in css px relative to the stage
      const stage = $('stage'), rel = (el) => { const a = stage.getBoundingClientRect(), b = el.getBoundingClientRect(); return { x: b.left - a.left, y: b.top - a.top, w: b.width, h: b.height }; };
      const PANES = { cart16: 'c16', pint16: 'p16', cart12: 'c12', pint12: 'p12' };
      function centre(what) {
        const r = rel($(PANES[what]));
        if (what === 'cart16' && isFinite(g('deck_px_fx'))) return { x: r.x + 0.5 * (g('deck_px_fx') + g('deck_px_rx')), y: r.y + 0.5 * (g('deck_px_fy') + g('deck_px_ry')) };
        return { x: r.x + r.w / 2, y: r.y + r.h / 2 };
      }
      function probe(x, y) {
        for (const what of Object.keys(PANES)) { const r = rel($(PANES[what])); if (x >= r.x && x <= r.x + r.w && y >= r.y && y <= r.y + r.h) return { what: what }; }
        return null;
      }
      const ROWS = {
        cart16: ['the new cart (Fig. 16)', [['Δθ', 'pitch_now', '°'], ['i', 'cur_now', 'A'], ['u<sub>f</sub>', 'uf_now', 'N'], ['u<sub>r</sub>', 'ur_now', 'N'], ['v', 'v_now', 'm/s'], ['k', 'k16', '']]],
        pint16: ['the pint on the new cart (Fig. 16)', [['τ', 'tilt_now', 'mm'], ['V<sub>spill</sub>', 'hspill_now', 'mL'], ['V<sub>glass</sub>', 'hglass_now', 'mL'], ['m<sub>s</sub>', 'sspill_now', 'g'], ['k', 'k16', '']]],
        cart12: ['Fig. 12’s cart and pint', [['τ<sub>12</sub>', 'tilt12_now', 'mm'], ['V<sub>spill,12</sub>', 'hspill12_now', 'mL'], ['m<sub>s,12</sub>', 'sspill12_now', 'g'], ['k<sub>12</sub>', 'k12', '']]],
      };
      ROWS.pint12 = ['Fig. 12’s pint, close up', ROWS.cart12[1]];
      const NOW16 = ['t_play', 'k16', 'tilt_now', 'pitch_now', 'cur_now', 'uf_now', 'ur_now', 'v_now', 'hglass_now', 'hspill_now', 'sspill_now', 'head_res'];
      Sim.data = {
        ds: ds, kicker: 'Fig. 16 on Kaggle · data', file: 'fig16-guinness-cart-control',
        playing: () => playing, play: () => { playing = true; $('play').textContent = 'Pause'; },
        groups: [],
        ledger: {
          headline: [{ v: 'tilt_now', title: 'tilt of the stout' }, { v: 'hspill_now', title: 'head spilled' }, { v: 'pitch_now', title: 'deck pitch' },
                     { v: 'cur_now', title: 'hub motors' }, { v: 'uf_now', title: 'front actuators' }, { v: 'tilt12_now', title: 'Fig. 12: tilt' }],
          sections: [
            { title: 'What you chose', note: 'the road and the control switch; they pick two stored files', vars: ['road', 'ctrl_on', 'v0', 'ride16', 'ride12'], how: 'set' },
            { title: 'The files', note: 'where the numbers come from, and their fingerprints', vars: ['nb_version', 'sha16', 'sha12', 'fps16', 'fps12', 'frames16', 'frames12', 'dur', 'head_ml0'], how: 'constant' },
            { title: 'Playback now', note: 'the stored values at the picture on screen', vars: ['playing'].concat(NOW16), how: 'formula' },
            { title: 'Fig. 12 now', note: 'the left ride at the same ride time', vars: ['k12', 'tilt12_now', 'hspill12_now', 'sspill12_now'], how: 'formula' },
            { title: 'The stored rides', note: 'computed on Kaggle, as stored; this page computes none of it', vars: ['t16', 'tilt16', 'th16', 'cur16', 'uf16', 'ur16', 'v16', 'hglass16', 'hspill16', 'sspill16', 'hspill12', 'sspill12'], how: 'run' },
            { title: 'Drawing', note: 'where the picture was drawn, and which picture the readings show', vars: ['k_text16', 'k_text12', 'deck_px_fx', 'deck_px_fy', 'deck_px_rx', 'deck_px_ry'], how: 'drawing', folded: true },
          ],
          books: [{ title: 'The head of foam', note: 'foam is neither made nor lost: what is in the glass and what has spilled add up to what was there at the start',
            rows: [[+1, 'hglass_now'], [+1, 'hspill_now']], total: 'head_ml0', residual: 'head_res', tol: 1e-6 }],
          controls: { play: 'playing', tbar: 't_play', 'ctl-sw': 'ctrl_on' },
          current: { k: 'k16', k12: 'k12' },
        },
        probe: probe,
        inspect: (ref) => ({ title: ROWS[ref.what][0], at: centre(ref.what), rows: ROWS[ref.what][1].map((r) => [r[0], g(r[1]), r[2], r[1]]) }),
        locate: (name, idx) => (/16$/.test(name) && idx === K()) ? centre(name === 'th16' || name === 'cur16' || /^u[fr]16/.test(name) || name === 'v16' ? 'cart16' : 'pint16') : null,
        check: {
          k16: () => ({ formula: 'min(N<sub>16</sub> − 1, round(t f<sub>16</sub>))', inputs: [inp('t_play', 't', 's', 3), inp('fps16', 'f<sub>16</sub>', '1/s', 0), inp('frames16', 'N<sub>16</sub>', '', 0)], value: Math.min(g('frames16') - 1, Math.round(g('t_play') * g('fps16'))) }),
          k12: () => ({ formula: 'min(N<sub>12</sub> − 1, round(t f<sub>12</sub>))', inputs: [inp('t_play', 't', 's', 3), inp('fps12', 'f<sub>12</sub>', '1/s', 0), inp('frames12', 'N<sub>12</sub>', '', 0)], value: Math.min(g('frames12') - 1, Math.round(g('t_play') * g('fps12'))) }),
          dur: () => ({ formula: 'max((N<sub>12</sub> − 1)/f<sub>12</sub>, (N<sub>16</sub> − 1)/f<sub>16</sub>)', inputs: [inp('frames12', 'N<sub>12</sub>', '', 0), inp('fps12', 'f<sub>12</sub>', '1/s', 0), inp('frames16', 'N<sub>16</sub>', '', 0), inp('fps16', 'f<sub>16</sub>', '1/s', 0)], value: Math.max((g('frames12') - 1) / g('fps12'), (g('frames16') - 1) / g('fps16')) }),
          t16: (k) => ({ formula: 'k / f<sub>16</sub>, k = ' + k, inputs: [inp('fps16', 'f<sub>16</sub>', '1/s', 0)], value: k / g('fps16') }),
          tilt_now: atNow('tilt16', 'τ<sub>k</sub>'), cur_now: atNow('cur16', 'i<sub>k</sub>'), uf_now: atNow('uf16', 'u<sub>f,k</sub>'), ur_now: atNow('ur16', 'u<sub>r,k</sub>'),
          v_now: atNow('v16', 'v<sub>k</sub>'), hglass_now: atNow('hglass16', 'V<sub>glass,k</sub>'), hspill_now: atNow('hspill16', 'V<sub>spill,k</sub>'), sspill_now: atNow('sspill16', 'm<sub>s,k</sub>'),
          pitch_now: () => ({ formula: '(θ<sub>k</sub> − θ<sub>0</sub>) 180/π', inputs: [['θ<sub>k</sub>', g('th16')[K()], 'rad', 6], ['θ<sub>0</sub>', g('th16')[0], 'rad', 6]], value: (g('th16')[K()] - g('th16')[0]) * 180 / Math.PI }),
          head_res: () => ({ formula: 'V<sub>glass</sub> + V<sub>spill</sub> − V<sub>head,0</sub>', inputs: [inp('hglass_now', 'V<sub>glass</sub>', 'mL', 4), inp('hspill_now', 'V<sub>spill</sub>', 'mL', 4), inp('head_ml0', 'V<sub>head,0</sub>', 'mL', 4)], value: g('hglass_now') + g('hspill_now') - g('head_ml0') }),
          hspill12_now: () => ({ formula: 'Fig. 12’s stored head spilled at k<sub>12</sub>', inputs: [inp('k12', 'k<sub>12</sub>', '', 0)], value: g('hspill12')[g('k12')] }),
          sspill12_now: () => ({ formula: 'Fig. 12’s stored stout spilled at k<sub>12</sub>', inputs: [inp('k12', 'k<sub>12</sub>', '', 0)], value: g('sspill12')[g('k12')] }),
          tilt12_now: () => { const R = Rz(r12.fill) - 0.5 * r12.dx; let s = 0; for (let j = 0; j < 64; j++) { const th = 2 * Math.PI * j / 64; s += r12.atInward(g('k12'), R, th)[0] * Math.cos(th); }
            return { formula: '2 (2/64) Σ<sub>j</sub> h(R − Δx/2, θ<sub>j</sub>) cos θ<sub>j</sub>, written out again from the stored surface of picture k<sub>12</sub>', inputs: [inp('k12', 'k<sub>12</sub>', '', 0), ['R', R, 'm', 5]], value: 2 * (2 / 64) * s * 1000 }; },
          sha16: () => ({ formula: 'SHA-256 written in index-16.json when the data was committed; equal only if not one byte changed on the way', inputs: [], value: rides[cur].sha256 }),
          nb_version: () => ({ formula: 'Kaggle notebook version in the ride’s index-16.json', inputs: [], value: rides[cur].dir === D16B && I16B ? I16B.kaggle.version : I16.kaggle.version }),
        },
        drawn: {
          tilt_now: text('b-tilt', () => fmt(Math.abs(at16('tilt_mm')), 1) + ' mm', 'tilt of the stout', Kt),
          hspill_now: text('b-head', () => fmt(at16('head_spill_ml'), 2) + ' mL', 'head spilled', Kt),
          sspill_now: text('b-stout', () => fmt(at16('spill_g'), 2) + ' g', 'stout spilled', Kt),
          pitch_now: text('b-pitch', () => fmt((at16('th') - r16.D.th[0]) * 180 / Math.PI, 1) + '°', 'deck pitch', Kt),
          cur_now: text('b-i', () => fmt(at16('i'), 1) + ' A', 'hub motors', Kt),
          uf_now: text('b-u', () => fmt(at16('uf'), 0) + ' / ' + fmt(at16('ur'), 0) + ' N', 'actuators front / rear', Kt),
          ur_now: text('b-u', () => fmt(at16('uf'), 0) + ' / ' + fmt(at16('ur'), 0) + ' N', 'actuators front / rear', Kt),
          v_now: text('b-v', () => fmt(at16('v'), 2) + ' m/s', 'speed', Kt),
          tilt12_now: text('a-tilt', () => fmt(Math.abs(tilt12(r12, Kt12())), 1) + ' mm', 'Fig. 12: tilt of the stout', Kt12),
          hspill12_now: text('a-head', () => fmt(at12('head_spill_ml'), 2) + ' mL', 'Fig. 12: head spilled', Kt12),
          sspill12_now: text('a-stout', () => fmt(at12('spill_g'), 2) + ' g', 'Fig. 12: stout spilled', Kt12),
          deck_px_fx: () => deckPixel('deck_px_fx', 'deck_px_fy', 'the deck top’s front edge'), deck_px_fy: () => deckPixel('deck_px_fx', 'deck_px_fy', 'the deck top’s front edge'),
          deck_px_rx: () => deckPixel('deck_px_rx', 'deck_px_ry', 'the deck top’s rear edge'), deck_px_ry: () => deckPixel('deck_px_rx', 'deck_px_ry', 'the deck top’s rear edge'),
        },
        round: { time: 't_play', label: () => 'the whole ride, ' + fmt(g('dur'), 1) + ' s', length: () => g('dur'),
          columns: ['tilt_now', 'pitch_now', 'cur_now', 'uf_now', 'ur_now', 'v_now', 'hspill_now', 'sspill_now', 'tilt12_now'] },
        about: 'This page computes no physics: every number of both rides was computed on Kaggle and is read from the ride files, whose SHA-256 fingerprints are checked against their index. Where the picture and the store differ: (1) the readings are rewritten 4 times a second, so their words trail the picture by up to a quarter second; (2) the wheels turn by the cart’s position interpolated between stored pictures, which is kinematics only, while every physical quantity is shown at the nearest stored picture; (3) when the control switch is pressed, the old picture fades out over 0.45 s; (4) Fig. 12’s tilt per picture is read on this page from Fig. 12’s stored surface, because its files store only the largest; (5) the 3D close-ups draw the same stored picture and record no points of their own, so they are read through the store, not pixel by pixel.',
      };
    }
    window.Guinness16 = { state: () => ({ T: T, cur: cur, playing: playing }), choose: choose, seek: (t) => { T = t; playing = false; $('play').textContent = 'Play'; } };
  }).catch((e) => { $('cap-t').textContent = 'data not loaded: ' + e.message; });
})();
