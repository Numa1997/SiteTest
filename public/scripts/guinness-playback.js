/* Fig. 12, computed on Kaggle: plays stored rides of the pint on the one-wheel cart (public/data/fig12/<date>/rides.json).
 * Computes nothing physical. Each stored frame holds the cart's position, speed, body and axle heights, the lean, the
 * spilled mass and the stout's surface on the polar grid of StoutView (17 rings x 64 angles, uint8 in 0.2 mm steps about
 * the fill, zlib-packed). The frame is handed to the website's own drawing code (stout-view.js) as a "fluid" whose
 * heightAt() reads the stored grid. Near the end of the computed time the playback slows smoothly to zero speed; only
 * there the pop-up about the pipeline fades in. Changing the ride cross-fades.
 *
 * The store (scripts/dataset.js): every number the page shows is written into one dataset where it is set. The file's
 * arrays go in when a ride is chosen (pick), the playback numbers every frame (tick), and StoutView writes what it draws
 * (camera, drawn points, the surface as drawn) through view.ds. The data panel (scripts/datalog.js, loaded once the
 * store is declared) only reads it, and proves each value three ways: stored, recomputed from stored inputs, read back
 * from the picture. */
(function () {
  'use strict';
  const DIR = '../data/fig12/2026-11-12/';
  const DATA_URL = DIR + 'rides.json', INDEX_URL = DIR + 'index.json';
  const F11 = 3.421;         // Hz, first sloshing mode of a deep cylinder of radius R(h) = 39.1 mm (note, eq. 16)
  const SLOW = 3.0;          // s of ride before the computed end over which the playback slows to zero
  const ROUND = 4.0;         // s of ride in one recorded round of the data panel
  const GROUND_Y = 0.95, GLASS_BASE = 0.014, BODY_H = 0.03, GLASS_FLOOR = 0.012;   // drawing constants handed to StoutView
  const $ = (id) => document.getElementById(id);
  const cv = $('cv'), pop = $('pop'), play = $('play'), tbar = $('tbar'), vbar = $('vbar');

  Promise.all([fetch(DATA_URL).then((r) => r.arrayBuffer()), fetch(INDEX_URL).then((r) => r.json())])
    .then(([buf, idx]) => start(buf, idx))
    .catch((e) => { $('cap-t').textContent = 'data not loaded: ' + e.message; });

  async function unpack(r) {
    if (r.bytes) return;
    const s = atob(r.frames), a = new Uint8Array(s.length);
    for (let i = 0; i < s.length; i++) a[i] = s.charCodeAt(i);
    const st = new Blob([a]).stream().pipeThrough(new DecompressionStream('deflate'));
    r.bytes = new Uint8Array(await new Response(st).arrayBuffer());
    // the file's lists as typed arrays, once per ride (the store holds these very arrays)
    for (const k of ['x', 'v', 'zb', 'zw', 'lean', 'spill', 'road_zr']) r['_' + k] = Float64Array.from(r[k]);
  }
  async function sha256(buf) {
    if (!(window.crypto && crypto.subtle)) return 'not available (needs https)';
    const h = new Uint8Array(await crypto.subtle.digest('SHA-256', buf));
    return Array.from(h, (b) => b.toString(16).padStart(2, '0')).join('');
  }

  async function start(buf, IDX) {
    const D = JSON.parse(new TextDecoder().decode(buf));
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
    const cart = { x: 0, vx: 0, zw: 0, zb: 0, Rw: 0.04, Mb: 1.5, ml: D.ml, Ls: 0.135, g: 9.81, k: 600, us: 0, glassFloor: GLASS_FLOOR, ride: null,
      road: { zr: (x) => { const r = cart.ride, f = (x - r.road_x0) / r.road_dx, i = Math.floor(f); if (i < 0 || i > r.road_zr.length - 2) return 0; return r.road_zr[i] + (f - i) * (r.road_zr[i + 1] - r.road_zr[i]); } } };
    const view = new window.StoutView(cv, { fluid: fluid, cart: cart, drops: [] }, { viewHeight: 0.40, groundY: GROUND_Y, elevDeg: 16, azimDeg: -24 });
    view.glassWall = 0.0032; view.glassBase = GLASS_BASE;
    glassLook(view);

    const rides = D.rides.slice().sort((a, b) => a.v0 - b.v0);
    const nMax = Math.max.apply(null, rides.map((r) => r.n));

    /* ---------- the store ---------- */
    const Sim = window.Sim;
    const ds = Sim.dataset({ title: 'Fig. 12 computed on Kaggle', attrs: { figure: 12, page: 'guinness-kaggle.html', data: DATA_URL,
      generated: IDX.generated, kaggle_notebook: IDX.kaggle.url, kaggle_version: IDX.kaggle.version } });
    const S = (n, t, a) => ds.var(n, [], t, a);
    // what the reader chooses
    S('ride_i', 'int', { symbol: 'i<sub>ride</sub>', long_name: 'the ride chosen: position of the speed control', computed_in: 'Set speed control (pick)', digits: 0 });
    S('v0', 'float', { symbol: 'v<sub>0</sub>', units: 'm/s', long_name: 'set speed of the chosen ride, as computed on Kaggle', computed_in: 'pick(), from the file', digits: 2 });
    S('road', 'str', { symbol: 'road', long_name: 'the road of the chosen ride', computed_in: 'pick(), from the file' });
    S('n_rides', 'int', { symbol: 'N<sub>rides</sub>', long_name: 'rides stored in the file', computed_in: 'start(), from the file', digits: 0 });
    // the file and what was stored with it
    S('generated', 'str', { symbol: 'date', long_name: 'date the data was generated on Kaggle', computed_in: 'index.json', source: IDX.kaggle.url });
    S('nb_version', 'int', { symbol: 'version', long_name: 'version of the Kaggle notebook that computed the data', computed_in: 'index.json', digits: 0 });
    S('file_bytes', 'int', { symbol: 'bytes', units: 'B', long_name: 'size of rides.json as fetched', computed_in: 'start(): length of the fetched file', digits: 0 });
    S('sha_file', 'str', { symbol: 'SHA-256', long_name: 'fingerprint of rides.json as fetched, computed in this browser', computed_in: 'start(): crypto.subtle.digest' });
    S('fill', 'float', { symbol: 'h<sub>0</sub>', units: 'm', long_name: 'fill height of the stout at rest', computed_in: 'rides.json (FILL in the notebook)', digits: 4 });
    S('q', 'float', { symbol: 'δ', units: 'm', long_name: 'height step of the stored surface (one uint8 step)', computed_in: 'rides.json', digits: 4 });
    S('fps', 'float', { symbol: 'f<sub>s</sub>', units: '1/s', long_name: 'stored frames per second of ride', computed_in: 'rides.json (FPS in the notebook)', digits: 0 });
    S('nr', 'int', { symbol: 'N<sub>r</sub>', long_name: 'rings of the surface grid (ring 0 is the axis)', computed_in: 'rides.json', digits: 0 });
    S('nth', 'int', { symbol: 'N<sub>θ</sub>', long_name: 'angles of the surface grid', computed_in: 'rides.json', digits: 0 });
    S('ml', 'float', { symbol: 'm<sub>ℓ</sub>', units: 'kg', long_name: 'mass of stout in the glass at the start', computed_in: 'rides.json (ρ V in the notebook)', digits: 4 });
    S('R_fill', 'float', { symbol: 'R(h<sub>0</sub>)', units: 'm', long_name: 'inner radius of the glass at the fill height: radius of the outer ring', computed_in: 'start(), from the glass table', formula: 'linear interpolation of the measured glass profile at h<sub>0</sub>', digits: 5 });
    S('z_rim', 'float', { symbol: 'z<sub>rim</sub>', units: 'm', long_name: 'height of the rim above the inner floor', computed_in: 'start(), from the glass table', digits: 4 });
    // the stored ride
    ds.dim('n', nMax); ds.dim('ir', NR + 1); ds.dim('ith', NTH); ds.dim('m', 2);
    ds.coord('t_n', 'n', Float64Array, { symbol: 't<sub>n</sub>', units: 's', long_name: 'ride time of stored frame n', computed_in: 'pick()', formula: 'n / f<sub>s</sub>', digits: 3 });
    const A = (n, a) => ds.var(n, ['n'], Float64Array, a);
    A('x', { symbol: 'x<sub>n</sub>', units: 'm', long_name: 'cart position along the road', computed_in: 'Kaggle (Cart.step), stored in rides.json', digits: 4 });
    A('v', { symbol: 'v<sub>n</sub>', units: 'm/s', long_name: 'cart speed', computed_in: 'Kaggle (Cart.step), stored in rides.json', digits: 4 });
    A('zb', { symbol: 'z<sub>b,n</sub>', units: 'm', long_name: 'height of the body’s underside above the road level', computed_in: 'Kaggle (Cart.step), stored in rides.json', digits: 6 });
    A('zw', { symbol: 'z<sub>w,n</sub>', units: 'm', long_name: 'height of the axle above the road level', computed_in: 'Kaggle (Cart.step), stored in rides.json', digits: 6 });
    A('lean', { symbol: 'Δη<sub>n</sub>', units: 'mm', long_name: 'lean: surface at the front wall minus the back wall, before rounding', computed_in: 'Kaggle (record: polar_surface), stored in rides.json', digits: 2 });
    A('spill', { symbol: 'm<sub>s,n</sub>', units: 'g', long_name: 'stout spilled over the rim so far', computed_in: 'Kaggle (record: spilled particles × particle mass)', digits: 2 });
    ds.var('eta_q', ['n', 'ir', 'ith'], Uint8Array, { symbol: 'b<sub>n,i,j</sub>', long_name: 'stored surface: height in steps of δ about the fill, ring i, angle j', computed_in: 'Kaggle (polar_surface, rounded to δ), unpacked in pick()', formula: 'η = h<sub>0</sub> + (b − 128) δ', digits: 0 });
    ds.coord('road_x', 'm', Float64Array, { symbol: 'x<sub>m</sub>', units: 'm', long_name: 'road position of stored road sample m', computed_in: 'pick()', formula: 'x<sub>0</sub> + m Δx<sub>road</sub>', digits: 3 });
    ds.var('road_zr', ['m'], Float64Array, { symbol: 'z<sub>r,m</sub>', units: 'm', long_name: 'road height', computed_in: 'Kaggle (road_table), stored in rides.json every 5 mm', digits: 5 });
    S('dur', 'float', { symbol: 'T<sub>ride</sub>', units: 's', long_name: 'computed length of the chosen ride', computed_in: 'pick()', formula: '(N − 1) / f<sub>s</sub>', digits: 2 });
    S('n_frames', 'int', { symbol: 'N', long_name: 'stored frames of the chosen ride', computed_in: 'pick(), from the file', digits: 0 });
    S('lean_max', 'float', { symbol: 'max |Δη|', units: 'mm', long_name: 'largest lean over the ride', computed_in: 'pick()', formula: 'max over n of |Δη<sub>n</sub>|', digits: 2 });
    S('v_min', 'float', { symbol: 'min v', units: 'm/s', long_name: 'lowest cart speed over the ride', computed_in: 'pick()', formula: 'min over n of v<sub>n</sub>', digits: 4 });
    S('v_max', 'float', { symbol: 'max v', units: 'm/s', long_name: 'highest cart speed over the ride', computed_in: 'pick()', formula: 'max over n of v<sub>n</sub>', digits: 4 });
    S('spill_end', 'float', { symbol: 'm<sub>s,N−1</sub>', units: 'g', long_name: 'stout spilled by the end of the ride', computed_in: 'pick()', formula: 'm<sub>s</sub> at the last frame', digits: 2 });
    // playback now
    S('playing', 'bool', { symbol: 'playing', long_name: 'the playback is running', computed_in: 'Play / Pause button' });
    S('t_play', 'float', { symbol: 't', units: 's', long_name: 'ride time being shown', computed_in: 'tick()', formula: 't += r Δt<sub>wall</sub>', digits: 3, updates: 'every frame' });
    S('rate', 'float', { symbol: 'r', long_name: 'playback rate: 1 is real time; it eases to 0 over the last 3 s of computed data', computed_in: 'tick()', formula: 'r = min(1, √((T<sub>ride</sub> − t) / 3 s))', digits: 4, updates: 'every frame' });
    S('i_now', 'int', { symbol: 'n', long_name: 'stored frame on screen (no interpolation between frames)', computed_in: 'tick()', formula: 'n = round(t f<sub>s</sub>)', digits: 0, updates: 'every frame' });
    S('x_now', 'float', { symbol: 'x', units: 'm', long_name: 'cart position now', computed_in: 'tick()', formula: 'x<sub>n</sub>', digits: 4, updates: 'every frame' });
    S('v_now', 'float', { symbol: 'v', units: 'm/s', long_name: 'cart speed now', computed_in: 'tick()', formula: 'v<sub>n</sub>', digits: 4, updates: 'every frame' });
    S('zb_now', 'float', { symbol: 'z<sub>b</sub>', units: 'm', long_name: 'body height now', computed_in: 'tick()', formula: 'z<sub>b,n</sub>', digits: 6, updates: 'every frame' });
    S('zw_now', 'float', { symbol: 'z<sub>w</sub>', units: 'm', long_name: 'axle height now', computed_in: 'tick()', formula: 'z<sub>w,n</sub>', digits: 6, updates: 'every frame' });
    S('lean_now', 'float', { symbol: 'Δη', units: 'mm', long_name: 'lean now, as Kaggle recorded it', computed_in: 'tick()', formula: 'Δη<sub>n</sub>', digits: 2, updates: 'every frame' });
    S('spill_now', 'float', { symbol: 'm<sub>s</sub>', units: 'g', long_name: 'stout spilled so far', computed_in: 'tick()', formula: 'm<sub>s,n</sub>', digits: 2, updates: 'every frame' });
    S('i_text', 'int', { symbol: 'n<sub>text</sub>', long_name: 'frame whose numbers the Readings show (rewritten 4 times a second)', computed_in: 'tick()', digits: 0 });
    ds.var('eta_draw', ['ir', 'ith'], Float64Array, { symbol: 'η<sub>i,j</sub>', units: 'm', long_name: 'surface height as drawn, ring i, angle j, above the glass’s inner floor', computed_in: 'StoutView.surface() via fluid.heightAt', formula: 'h<sub>0</sub> + (b<sub>n,i,j</sub> − 128) δ', digits: 5 });
    S('eta_front', 'float', { symbol: 'η<sub>front</sub>', units: 'm', long_name: 'surface as drawn at the front wall', computed_in: 'StoutView.surface()', digits: 5 });
    S('eta_back', 'float', { symbol: 'η<sub>back</sub>', units: 'm', long_name: 'surface as drawn at the back wall', computed_in: 'StoutView.surface()', digits: 5 });
    S('dw', 'float', { symbol: 'Δη<sub>grid</sub>', units: 'm', long_name: 'lean read from the stored, rounded grid', computed_in: 'StoutView.surface()', formula: 'η<sub>front</sub> − η<sub>back</sub>', digits: 5 });
    S('eta_mid', 'float', { symbol: 'η<sub>mid</sub>', units: 'm', long_name: 'surface as drawn on the glass’s axis', computed_in: 'StoutView.afterGlass()', digits: 5 });
    S('lean_gap', 'float', { symbol: 'Δη − Δη<sub>grid</sub>', units: 'mm', long_name: 'Kaggle’s lean minus the lean of the rounded grid: the rounding, at most one step δ', computed_in: 'tick()', formula: 'Δη − 1000 Δη<sub>grid</sub>', digits: 3 });
    // phase space of the first sloshing mode, from the stored surface (worked out when a ride is chosen)
    S('f11', 'float', { symbol: 'f<sub>11</sub>', units: 'Hz', long_name: 'first sloshing mode of a deep cylinder of the surface radius R(h<sub>0</sub>) = 39.1 mm', computed_in: 'constant of this page', source: 'Fig. 12 lecture note, eq. (16); docs/simulations/fig12-beer-slosh.md', digits: 3 });
    S('w11', 'float', { symbol: 'ω<sub>11</sub>', units: 'rad/s', long_name: 'its angular frequency', computed_in: 'start()', formula: '2π f<sub>11</sub>', digits: 3 });
    ds.var('q1', ['n'], Float64Array, { symbol: 'q<sub>n</sub>', units: 'mm', long_name: 'first sloshing mode: its height at the wall (the cos θ part of the outer ring)', computed_in: 'pick() → store()', formula: 'q = (2/N<sub>θ</sub>) Σ<sub>j</sub> η<sub>N<sub>r</sub>,j</sub> cos θ<sub>j</sub>', digits: 3 });
    ds.var('p1', ['n'], Float64Array, { symbol: 'p<sub>n</sub>', units: 'mm', long_name: 'its rate divided by ω<sub>11</sub>, from the frames on either side', computed_in: 'pick() → store()', formula: 'p = (q<sub>n+1</sub> − q<sub>n−1</sub>) / (2 sin ω<sub>11</sub>h), h = 1/f<sub>s</sub>', digits: 3 });
    S('ph_range', 'float', { symbol: 'q<sub>max</sub>', units: 'mm', long_name: 'half-width of the phase plot: largest |q| or |p| of the ride, plus 10 %', computed_in: 'pick() → store()', formula: '1.1 max over n of max(|q<sub>n</sub>|, |p<sub>n</sub>|)', digits: 3 });
    S('q_now', 'float', { symbol: 'q', units: 'mm', long_name: 'first mode now', computed_in: 'tick()', formula: 'q<sub>n</sub>', digits: 3, updates: 'every frame' });
    S('p_now', 'float', { symbol: 'q̇/ω<sub>11</sub>', units: 'mm', long_name: 'its scaled rate now', computed_in: 'tick()', formula: 'p<sub>n</sub>', digits: 3, updates: 'every frame' });
    S('amp_now', 'float', { symbol: 'A', units: 'mm', long_name: 'amplitude of the swing now: distance of the state from the centre', computed_in: 'tick()', formula: '√(q² + p²)', digits: 3, updates: 'every frame' });
    S('ph_cx', 'float', { symbol: 'X<sub>ph</sub>', units: 'px', long_name: 'screen x of the phase plot’s centre', computed_in: 'drawPhase()', digits: 2 });
    S('ph_cy', 'float', { symbol: 'Y<sub>ph</sub>', units: 'px', long_name: 'screen y of the phase plot’s centre', computed_in: 'drawPhase()', digits: 2 });
    S('ph_s', 'float', { symbol: 's<sub>ph</sub>', units: 'px/mm', long_name: 'scale of the phase plot, the same on both axes', computed_in: 'drawPhase()', digits: 3 });
    S('ph_x_px', 'float', { symbol: 'X<sub>state</sub>', units: 'px', long_name: 'screen x of the state dot', computed_in: 'drawPhase()', formula: 'X<sub>ph</sub> + s<sub>ph</sub> q', digits: 2 });
    S('ph_y_px', 'float', { symbol: 'Y<sub>state</sub>', units: 'px', long_name: 'screen y of the state dot', computed_in: 'drawPhase()', formula: 'Y<sub>ph</sub> − s<sub>ph</sub> p', digits: 2 });
    // the drawing
    const Dr = (n, sym, u, ln, d, f) => S(n, 'float', { symbol: sym, units: u, long_name: ln, computed_in: 'StoutView.draw()', formula: f, digits: d });
    Dr('scale', 's', 'px/m', 'px per metre at the camera’s target', 2, 'canvas height / 0.40 m');
    Dr('cam_x', 'x<sub>cam</sub>', 'm', 'the camera rides with the cart: its x', 4);
    Dr('elev', 'ε', 'rad', 'camera looks down by', 4); Dr('azim', 'α', 'rad', 'camera turned toward the front by', 4);
    Dr('cam_dist', 'd', 'm', 'camera distance from its target', 3); Dr('cam_zt', 'z<sub>T</sub>', 'm', 'height of the camera’s target', 3);
    Dr('focal', 'F', 'px', 'focal length', 2, 's d'); Dr('cam_cx', 'X<sub>0</sub>', 'px', 'screen x of the axis of view', 2, 'W / 2');
    Dr('cam_cy', 'Y<sub>0</sub>', 'px', 'screen y of the axis of view', 2, 'set so the road under the axle sits at 0.95 of the height');
    Dr('ground_px', 'y<sub>road</sub>', 'px', 'screen y of the road under the axle', 2);
    Dr('axle_px_x', 'X<sub>axle</sub>', 'px', 'screen x of the axle', 2); Dr('axle_px_y', 'Y<sub>axle</sub>', 'px', 'screen y of the axle', 2);
    Dr('body_px_x', 'X<sub>body</sub>', 'px', 'screen x of the body’s near bottom edge', 2); Dr('body_px_y', 'Y<sub>body</sub>', 'px', 'screen y of the body’s near bottom edge', 2);
    Dr('glass_px_x', 'X<sub>glass</sub>', 'px', 'screen x of a reference point on the glass axis at z<sub>b</sub> + 12 mm + h<sub>0</sub>', 2);
    Dr('glass_px_y', 'Y<sub>glass</sub>', 'px', 'screen y of that reference point', 2);
    Dr('canvas_w', 'W', 'px', 'figure width', 1); Dr('canvas_h', 'H', 'px', 'figure height', 1);
    Dr('front_px_x', 'X<sub>front</sub>', 'px', 'screen x of the head’s band at the front wall', 2); Dr('front_px_y', 'Y<sub>front</sub>', 'px', 'screen y of the head’s band at the front wall', 2);
    Dr('back_px_x', 'X<sub>top</sub>', 'px', 'screen x of the head’s top on the axis', 2); Dr('back_px_y', 'Y<sub>top</sub>', 'px', 'screen y of the head’s top on the axis', 2);
    Dr('head_h', 'h<sub>head</sub>', 'm', 'thickness of the drawn head (drawn, not computed)', 3);
    Dr('r_s', 'r<sub>s</sub>', 'm', 'radius of the drawn surface’s outer ring', 5);
    S('glass_base', 'float', { symbol: 'b<sub>glass</sub>', units: 'm', long_name: 'thickness of the drawn glass foot', computed_in: 'this page (view.glassBase)', digits: 3 });
    S('body_h', 'float', { symbol: 'h<sub>body</sub>', units: 'm', long_name: 'height of the drawn body', computed_in: 'stout-view.js (bodyH)', digits: 3 });
    view.ds = ds;                                // StoutView writes its camera and the points it draws into the store

    const sha = await sha256(buf);
    ds.set('n_rides', rides.length); ds.set('generated', IDX.generated); ds.set('nb_version', IDX.kaggle.version);
    ds.set('file_bytes', buf.byteLength); ds.set('sha_file', sha);
    ds.set('fill', D.fill); ds.set('q', D.q); ds.set('fps', D.fps); ds.set('nr', NR); ds.set('nth', NTH); ds.set('ml', D.ml);
    ds.set('R_fill', Rh); ds.set('z_rim', zRim); ds.set('f11', F11); ds.set('w11', 2 * Math.PI * F11); ds.set('glass_base', view.glassBase); ds.set('body_h', view.bodyH);
    const fileIdx = (IDX.files || []).find((f) => f.path === 'rides.json') || {};

    vbar.max = rides.length - 1; vbar.value = Math.floor((rides.length - 1) / 2);
    $('road-name').textContent = 'Road: ' + rides[0].road + ' (the same road at every speed).';
    let ride = null, T = 0, rate = 1, playing = true, last = null, lastTxt = 0, ended = false;
    const dur = () => (ride.n - 1) / D.fps;

    function store(r, i) {                        // the chosen ride into the store: the very arrays the playback reads
      ds.dim('n', r.n); ds.dim('m', r._road_zr.length);
      ds.set('ride_i', i); ds.set('v0', r.v0); ds.set('road', r.road); ds.set('n_frames', r.n); ds.set('dur', (r.n - 1) / D.fps);
      ds.set('x', r._x); ds.set('v', r._v); ds.set('zb', r._zb); ds.set('zw', r._zw); ds.set('lean', r._lean); ds.set('spill', r._spill);
      ds.set('eta_q', r.bytes); ds.set('road_zr', r._road_zr);
      const tn = ds.alloc('t_n'); for (let k = 0; k < r.n; k++) tn[k] = k / D.fps;
      const rx = ds.alloc('road_x'); for (let k = 0; k < rx.length; k++) rx[k] = r.road_x0 + k * r.road_dx;
      let lm = 0, vmn = Infinity, vmx = -Infinity; for (let k = 0; k < r.n; k++) { lm = Math.max(lm, Math.abs(r._lean[k])); vmn = Math.min(vmn, r._v[k]); vmx = Math.max(vmx, r._v[k]); }
      // the first sloshing mode from the stored surface: the cos θ part of the outer ring (at the wall η = q cos θ), and
      // its rate over ω11 from the frames on either side, divided by 2 sin(ω11 h) so that a pure swing at f11 is a circle
      const q = ds.alloc('q1'), pr = ds.alloc('p1'), ring = NR * NTH, w = 2 * Math.PI * F11, h = 1 / D.fps;
      for (let k = 0; k < r.n; k++) { let a = 0; for (let j = 0; j < NTH; j++) a += (D.fill + (r.bytes[k * M + ring + j] - 128) * D.q) * Math.cos(2 * Math.PI * j / NTH); q[k] = 2 / NTH * a * 1000; }
      let pm = 0;
      for (let k = 0; k < r.n; k++) { const k0 = Math.max(0, k - 1), k1 = Math.min(r.n - 1, k + 1); pr[k] = (q[k1] - q[k0]) / ((k1 - k0) * Math.sin(w * h)); pm = Math.max(pm, Math.abs(q[k]), Math.abs(pr[k])); }
      ds.touch('q1'); ds.touch('p1'); ds.set('ph_range', 1.1 * pm);
      ds.set('lean_max', lm); ds.set('v_min', vmn); ds.set('v_max', vmx); ds.set('spill_end', r._spill[r.n - 1]);
    }
    async function pick(fade) {
      const i = +vbar.value, r = rides[i]; await unpack(r);
      const swap = () => { ride = r; cart.ride = r; T = 0; ended = false; hidePop(); store(r, i); $('v-out').textContent = r.v0.toFixed(2) + ' m/s (computed)'; };
      if (fade && ride) { cv.style.opacity = '0'; setTimeout(() => { swap(); cv.style.opacity = '1'; }, 350); } else swap();
    }
    function showPop() { pop.hidden = false; requestAnimationFrame(() => pop.classList.add('is-on')); }
    function hidePop() { pop.classList.remove('is-on'); setTimeout(() => { if (!pop.classList.contains('is-on')) pop.hidden = true; }, 600); }
    function setPlaying(p) { playing = p; play.textContent = playing ? 'Pause' : 'Play'; ds.set('playing', playing); }

    vbar.addEventListener('input', () => pick(true));
    tbar.addEventListener('input', () => { if (ride) { T = tbar.value / 1000 * dur(); ended = false; hidePop(); } });
    play.addEventListener('click', () => setPlaying(!playing));
    $('again').addEventListener('click', () => { cv.style.opacity = '0'; setTimeout(() => { T = 0; ended = false; hidePop(); cv.style.opacity = '1'; }, 350); });
    await pick(false); setPlaying(true);

    function tick(now) {
      requestAnimationFrame(tick);                // first, so the data panel's frame reads a frame this page has written
      if (!(ride && ride.bytes)) return;
      if (last != null && playing && !ended) {
        // the playback rate eases to zero over the last SLOW seconds: rate = sqrt(left / SLOW), which reaches the end
        const left = dur() - T;
        rate = left >= SLOW ? 1 : Math.sqrt(Math.max(0, left) / SLOW);
        T = Math.min(dur(), T + rate * (now - last) / 1000);
        if (dur() - T < 0.01) { T = dur(); ended = true; showPop(); }
      }
      last = now;
      const k = Math.min(ride.n - 1, Math.max(0, Math.round(T * D.fps)));
      ds.set('t_play', T); ds.set('rate', rate); ds.set('i_now', k);
      fluid.frame = ride.bytes.subarray(k * M, (k + 1) * M);
      cart.x = ride._x[k]; cart.vx = ride._v[k]; cart.zw = ride._zw[k]; cart.zb = ride._zb[k];
      ds.set('x_now', cart.x); ds.set('v_now', cart.vx); ds.set('zb_now', cart.zb); ds.set('zw_now', cart.zw);
      ds.set('lean_now', ride._lean[k]); ds.set('spill_now', ride._spill[k]);
      const rc = cv.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
      const W = Math.round(rc.width * dpr), H = Math.round(rc.height * dpr);
      if (W > 0 && (cv.width !== W || cv.height !== H)) { cv.width = W; cv.height = H; }
      view.cssW = rc.width || cv.width; view.draw();
      ds.set('lean_gap', ride._lean[k] - 1000 * ds.get('dw'));
      { const qn = ds.get('q1')[k], pn = ds.get('p1')[k]; ds.set('q_now', qn); ds.set('p_now', pn); ds.set('amp_now', Math.hypot(qn, pn)); }
      drawPhase(k);
      if (playing) tbar.value = Math.round(T / dur() * 1000);
      if (now - lastTxt > 250) {        // the words change four times a second
        lastTxt = now;
        $('t-out').textContent = (k / D.fps).toFixed(1) + ' of ' + dur().toFixed(0) + ' s';
        $('cap-t').textContent = rate < 0.999 && !ended ? 'slowing: computed data ends at ' + dur().toFixed(0) + ' s' : (ended ? 'end of computed data' : 'stored ride, real time');
        $('r-v').textContent = ride._v[k].toFixed(3) + ' m/s'; $('r-l').textContent = ride._lean[k].toFixed(1) + ' mm'; $('r-s').textContent = ride._spill[k].toFixed(1) + ' g';
        ds.set('i_text', k);
        $('cap-ph').textContent = 'amplitude now ' + ds.get('amp_now').toFixed(2) + ' mm';
      }
    }
    requestAnimationFrame(tick);

    // the phase space of the first mode: q across, p = q̇/ω11 up, the same scale on both axes so a free swing is a circle
    const phc = $('ph'), pbox = Sim.canvas2d(phc), TH = Sim.theme;
    function drawPhase(k) {
      const rc = phc.getBoundingClientRect();
      if (Math.round(rc.width) !== pbox.w || Math.round(rc.height) !== pbox.h) pbox.fit();
      const c = pbox.ctx, W = pbox.w, H = pbox.h, q = ds.get('q1'), p = ds.get('p1'), R = ds.get('ph_range') || 1, n = ride.n;
      const side = Math.min(W - 70, H - 56), cx = Math.round(W / 2 + 10), cy = Math.round(24 + side / 2), sc = side / (2 * R);
      ds.set('ph_cx', cx); ds.set('ph_cy', cy); ds.set('ph_s', sc);
      const X = (v) => cx + sc * v, Y = (v) => cy - sc * v, L = cx - side / 2, Rr = cx + side / 2, T0 = cy - side / 2, B = cy + side / 2;
      c.clearRect(0, 0, W, H); c.fillStyle = '#ffffff'; c.fillRect(L, T0, side, side);
      c.font = TH.mono; c.lineWidth = 1;
      const tk = Sim.ticks(-R, R, W < 500 ? 4 : 6);
      tk.values.forEach((v) => {
        c.strokeStyle = v === 0 ? TH.rule : TH.ruleSoft;
        c.beginPath(); c.moveTo(X(v), T0); c.lineTo(X(v), B); c.stroke(); c.beginPath(); c.moveTo(L, Y(v)); c.lineTo(Rr, Y(v)); c.stroke();
        const lab = v === 0 ? '0' : Sim.fmt(v, tk.digits).replace('-', '−');
        c.fillStyle = TH.muted; c.textAlign = 'center'; c.textBaseline = 'alphabetic'; c.fillText(lab, X(v), B + 15);
        c.textAlign = 'right'; c.textBaseline = 'middle'; c.fillText(lab, L - 6, Y(v));
      });
      c.strokeStyle = TH.rule; c.strokeRect(L, T0, side, side);
      c.fillStyle = TH.muted; c.textAlign = 'right'; c.textBaseline = 'alphabetic'; c.fillText('q (mm)', Rr, B + 30);
      c.textAlign = 'left'; c.fillText('q̇/ω₁₁ (mm)', L, T0 - 8);
      c.save(); c.beginPath(); c.rect(L, T0, side, side); c.clip();
      c.lineJoin = 'round';
      c.strokeStyle = 'rgba(28,21,24,0.13)'; c.lineWidth = 1; c.beginPath();
      for (let m = 0; m < n; m++) { if (m) c.lineTo(X(q[m]), Y(p[m])); else c.moveTo(X(q[m]), Y(p[m])); } c.stroke();
      const a = Math.hypot(q[k], p[k]);                                         // what an undamped swing of this amplitude would trace
      c.setLineDash([5, 4]); c.strokeStyle = TH.rose; c.lineWidth = 1.4; c.beginPath(); c.arc(cx, cy, sc * a, 0, 2 * Math.PI); c.stroke(); c.setLineDash([]);
      c.strokeStyle = TH.ink; c.lineWidth = 1.6; c.beginPath();
      for (let m = Math.max(0, k - D.fps); m <= k; m++) { if (m > k - D.fps && m > 0) c.lineTo(X(q[m]), Y(p[m])); else c.moveTo(X(q[m]), Y(p[m])); } c.stroke();
      c.restore();
      const sx = X(q[k]), sy = Y(p[k]);
      c.fillStyle = TH.accent; c.strokeStyle = TH.card; c.lineWidth = 1.5; c.beginPath(); c.arc(sx, sy, 5, 0, 2 * Math.PI); c.fill(); c.stroke();
      ds.set('ph_x_px', sx); ds.set('ph_y_px', sy);
    }

    defineData();
    const dl = document.createElement('script'); dl.src = '../scripts/datalog.js'; document.body.appendChild(dl);   // the data panel, once the store is declared

    /* ---------- the data panel's hooks: three proofs per value ---------- */
    function defineData() {
      const g = (n) => ds.get(n), inp = (n, sym, u, d) => [sym, g(n), u, d];
      // the pinhole camera written out again from its stored constants (StoutView.camera and .project), css px;
      // points relative to the cart: x from the axle, y across (+ away from the viewer), z up from the road level
      function proj(x, y, z) {
        const e = g('elev'), a = g('azim'), Dd = g('cam_dist'), zT = g('cam_zt'), F = g('focal');
        const d = [Math.sin(a) * Math.cos(e), Math.cos(a) * Math.cos(e), -Math.sin(e)], r = [Math.cos(a), -Math.sin(a), 0], u = [Math.sin(a) * Math.sin(e), Math.cos(a) * Math.sin(e), Math.cos(e)];
        const v = [x + Dd * d[0], y + Dd * d[1], z - zT + Dd * d[2]], dep = v[0] * d[0] + v[1] * d[1] + v[2] * d[2];
        return [g('cam_cx') + F * (v[0] * r[0] + v[1] * r[1]) / dep, g('cam_cy') - F * (v[0] * u[0] + v[1] * u[1] + v[2] * u[2]) / dep];
      }
      const CAMIN = () => [inp('elev', 'ε', 'rad', 4), inp('azim', 'α', 'rad', 4), inp('cam_dist', 'd', 'm', 3), inp('cam_zt', 'z<sub>T</sub>', 'm', 3), inp('focal', 'F', 'px', 2), inp('cam_cx', 'X<sub>0</sub>', 'px', 2), inp('cam_cy', 'Y<sub>0</sub>', 'px', 2)];
      const projCheck = (lab, pt, k, extra) => ({ formula: 'the camera’s projection of ' + lab + ' (pinhole: turn by α and ε, divide by depth, times F)', inputs: CAMIN().concat(extra || []), value: proj(pt[0], pt[1], pt[2])[k] });
      const zG = () => g('zb_now') + g('body_h') + g('glass_base');      // the glass's inner floor, above the road level
      const node = (i) => { const ir = Math.floor(i / NTH), it = i % NTH, r = g('r_s') * ir / NR, th = 2 * Math.PI * it / NTH; return { ir, it, r, th, x: r * Math.cos(th), y: r * Math.sin(th) }; };
      const nodeAt = (i) => { const q = node(i), p = proj(q.x, q.y, zG() + g('eta_draw')[i] + g('head_h')); return { x: p[0], y: p[1] }; };
      const etaFromBytes = (i) => g('fill') + (g('eta_q')[g('i_now') * M + i] - 128) * g('q');
      const BYTE = (i) => [['b<sub>n,i,j</sub>', g('eta_q')[g('i_now') * M + i], '', 0], inp('fill', 'h<sub>0</sub>', 'm', 4), inp('q', 'δ', 'm', 4), inp('i_now', 'n', '', 0)];
      const atNow = (arr, sym, u, d) => () => ({ formula: sym + ' read from the stored ride at the frame on screen, n = ' + g('i_now'), inputs: [inp('i_now', 'n', '', 0)], value: g(arr)[g('i_now')] });
      function pix(xc, yc, test, what, expected, note, rv) {
        const dpr = cv.width / cv.getBoundingClientRect().width, at = (x, y) => view.ctx.getImageData(Math.floor(x * dpr), Math.floor(y * dpr), 1, 1).data;
        let d = at(xc, yc);
        for (let k = 1; rv && k <= rv && !(d[3] > 0 && test(d)); k++) { const up = at(xc, yc - k), dn = at(xc, yc + k); if (up[3] > 0 && test(up)) d = up; else if (dn[3] > 0 && test(dn)) d = dn; }
        return { what: what + ', (' + Sim.fmt(xc, 1) + ', ' + Sim.fmt(yc, 1) + ') css px', drawn: d[3] === 0 ? 'nothing (transparent)' : 'rgb(' + d[0] + ', ' + d[1] + ', ' + d[2] + ')', expected: expected, ok: d[3] > 0 && test(d), note: note };
      }
      const isHead = (d) => d[0] > 170 && d[1] > 150 && d[2] > 110 && d[0] - d[2] < 90;
      const isInk = (d) => d[0] < 90 && d[1] < 90 && d[2] < 90;
      const headDrawn = (side) => side === 'front'
        ? pix(g('front_px_x'), g('front_px_y'), isHead, 'three quarters up the head’s band at the front wall', 'the cream of the head, about rgb(220, 205, 175)', 'The head is drawn as a 12 mm band laid on the stored surface; a point three quarters up it at the front wall is cream only if the surface was drawn at the stored height there. That point lies only about 2 mm under the rim, and the rim’s dark line, about 1.6 px wide, can pass over it, so the search goes up to 3 px up and down to the cream beside the line.', 3)
        : pix(g('back_px_x'), g('back_px_y'), isHead, 'the top of the head on the glass’s axis', 'the cream of the head, about rgb(236, 225, 201)', 'The top of the head on the axis: the pixel is cream only if the head’s sheet was drawn at the stored height there. From this camera the glass’s near rim and its white highlight, two lines about 1 px wide, pass over this very point, so the search goes up to 3 px up and down to the cream beside them (measured at 390 and 1440 px wide: cream from 2 px off the point).', 3);
      const axleDrawn = () => pix(g('axle_px_x'), g('axle_px_y'), isInk, 'the axle', 'the dark hub dot, rgb(28, 21, 24)', 'The hub is a 4 px dot at the axle, drawn over the spokes, at the stored axle height.');
      const bodyDrawn = () => pix(g('body_px_x'), g('body_px_y') - 0.5, isInk, 'bottom edge of the body', 'the 2 px ink outline of the body', 'The body is a box from z<sub>b</sub> to z<sub>b</sub> + 3 cm with a 2 px outline; its near bottom edge, seen through the camera, is at the stored height (searched 2 px up and down, the outline is anti-aliased).', 2);
      const nodeDrawn = (i) => { const q = node(i), p = nodeAt(i); return pix(p.x, p.y, isHead, 'the head’s top above ring ' + q.ir + ', angle ' + Sim.fmt(q.th * 180 / Math.PI, 1) + '°', 'the cream of the head', 'Each node of the stored grid is a corner of the head’s lit sheet, drawn 12 mm above the stored height. A node on the far rim can sit under the glass’s rim line, and then the pixel there is the line’s grey, not cream.', 2); };
      const textDrawn = (id, arr, dig, unit, lab) => () => {
        const el = $(id), k = g('i_text'), want = g(arr)[k].toFixed(dig) + ' ' + unit, got = el.textContent;
        return { what: 'the Readings box, “' + lab + '”', drawn: '“' + got + '”', expected: '“' + want + '”, the stored value at frame ' + k, ok: got === want, note: 'The words are rewritten 4 times a second, so they show frame n<sub>text</sub> = ' + k + ', which can trail the frame on screen (n = ' + g('i_now') + ') by up to a quarter second of ride.' };
      };
      const isWineDot = (d) => d[0] > 90 && d[0] < 170 && d[1] < 70 && d[2] < 80;
      function phDrawn() {
        const dpr = phc.width / phc.getBoundingClientRect().width, x = g('ph_x_px'), y = g('ph_y_px'), d = pbox.ctx.getImageData(Math.floor(x * dpr), Math.floor(y * dpr), 1, 1).data;
        return { what: 'the state dot on the phase plot, (' + Sim.fmt(x, 1) + ', ' + Sim.fmt(y, 1) + ') css px', drawn: d[3] === 0 ? 'nothing (transparent)' : 'rgb(' + d[0] + ', ' + d[1] + ', ' + d[2] + ')', expected: 'wine, rgb(122, 31, 43)', ok: d[3] > 0 && isWineDot(d), note: 'The state is a wine dot of 5 px radius at (q, p) through the plot’s centre and scale; the pixel at the stored point is wine only if the dot was drawn there.' };
      }
      const RING = 12;
      function probe(x, y) {
        if (!g('canvas_w')) return null;
        let best = null, bd = RING;
        for (let i = 0; i < M; i++) { const p = nodeAt(i), dd = Math.hypot(p.x - x, p.y - y); if (dd < bd) { bd = dd; best = i; } }
        if (best != null) return { what: 'node', i: best };
        const ax = g('axle_px_x'), ay = g('axle_px_y'), rW = Math.abs(proj(0.04, -0.01, g('zw_now'))[0] - ax);
        if (Math.hypot(x - ax, y - ay) < rW) return { what: 'wheel' };
        const by = g('body_px_y'), top = proj(0, -0.06, g('zb_now') + g('body_h'))[1];
        if (y <= by + 4 && y >= top - 4 && Math.abs(x - ax) < 0.12 * g('scale')) return { what: 'body' };
        return null;
      }
      Sim.data = {
        ds: ds, kicker: 'Fig. 12 on Kaggle · data', file: 'fig12-guinness-kaggle',
        playing: () => playing, play: () => setPlaying(true),
        groups: [
          { title: 'What you chose', note: 'the ride, by the position of the speed control', vars: ['ride_i', 'v0', 'road', 'n_rides'] },
          { title: 'The file', note: 'where the numbers come from, and its fingerprint', vars: ['generated', 'nb_version', 'file_bytes', 'sha_file', 'fill', 'q', 'fps', 'nr', 'nth', 'ml', 'R_fill', 'z_rim'] },
          { title: 'The stored ride', note: 'computed on Kaggle, as stored; this page computes none of it', vars: ['t_n', 'x', 'v', 'zb', 'zw', 'lean', 'spill', 'eta_q', 'road_x', 'road_zr', 'n_frames', 'dur', 'lean_max', 'v_min', 'v_max', 'spill_end'] },
          { title: 'Playback now', note: 'which stored frame is on screen, and its numbers', vars: ['playing', 't_play', 'rate', 'i_now', 'x_now', 'v_now', 'zb_now', 'zw_now', 'lean_now', 'spill_now', 'i_text', 'eta_draw', 'eta_front', 'eta_back', 'dw', 'eta_mid', 'lean_gap'] },
          { title: 'Phase space', note: 'the first sloshing mode and its rate, from the stored surface', vars: ['f11', 'w11', 'q1', 'p1', 'ph_range', 'q_now', 'p_now', 'amp_now', 'ph_cx', 'ph_cy', 'ph_s', 'ph_x_px', 'ph_y_px'] },
          { title: 'Drawing', note: 'how stored numbers become pixels: the camera and the points it places', vars: ['scale', 'cam_x', 'elev', 'azim', 'cam_dist', 'cam_zt', 'focal', 'cam_cx', 'cam_cy', 'ground_px', 'axle_px_x', 'axle_px_y', 'body_px_x', 'body_px_y', 'glass_px_x', 'glass_px_y', 'front_px_x', 'front_px_y', 'back_px_x', 'back_px_y', 'canvas_w', 'canvas_h', 'head_h', 'r_s', 'glass_base', 'body_h'] },
        ],
        ledger: {
          headline: [{ v: 'lean_now', title: 'surface lean' }, { v: 'v_now', title: 'cart speed' }, { v: 'x_now', title: 'along the road' }, { v: 'spill_now', title: 'stout spilled' }, { v: 'amp_now', title: 'first-mode swing' }, { v: 'rate', title: 'playback rate' }],
          sections: [
            { title: 'What you chose', note: 'the ride, by the position of the speed control', vars: ['ride_i', 'v0', 'road', 'n_rides'], how: 'set' },
            { title: 'The file', note: 'where the numbers come from, and its fingerprint', vars: ['generated', 'nb_version', 'file_bytes', 'sha_file', 'fill', 'q', 'fps', 'nr', 'nth', 'ml', 'R_fill', 'z_rim'], how: 'constant' },
            { title: 'Playback now', note: 'which stored frame is on screen, and its numbers', vars: ['playing', 't_play', 'rate', 'i_now', 'x_now', 'v_now', 'zb_now', 'zw_now', 'lean_now', 'spill_now', 'i_text', 'eta_front', 'eta_back', 'dw', 'eta_mid', 'lean_gap', 'eta_draw'], how: 'formula' },
            { title: 'The stored ride', note: 'computed on Kaggle, as stored; this page computes none of it', vars: ['t_n', 'x', 'v', 'zb', 'zw', 'lean', 'spill', 'eta_q', 'road_x', 'road_zr', 'n_frames', 'dur', 'lean_max', 'v_min', 'v_max', 'spill_end'], how: 'run' },
            { title: 'Phase space', note: 'the first sloshing mode and its rate, from the stored surface', vars: ['f11', 'w11', 'q1', 'p1', 'ph_range', 'q_now', 'p_now', 'amp_now', 'ph_cx', 'ph_cy', 'ph_s', 'ph_x_px', 'ph_y_px'], how: 'formula' },
            { title: 'Drawing', note: 'how stored numbers become pixels', vars: ['scale', 'cam_x', 'elev', 'azim', 'cam_dist', 'cam_zt', 'focal', 'cam_cx', 'cam_cy', 'ground_px', 'axle_px_x', 'axle_px_y', 'body_px_x', 'body_px_y', 'glass_px_x', 'glass_px_y', 'front_px_x', 'front_px_y', 'back_px_x', 'back_px_y', 'canvas_w', 'canvas_h', 'head_h', 'r_s', 'glass_base', 'body_h'], how: 'drawing', folded: true },
          ],
          controls: { vbar: 'ride_i', play: 'playing', tbar: 't_play' },
          current: { n: 'i_now' },
        },
        probe: probe,
        inspect: (ref) => {
          if (ref.what === 'node') {
            const q = node(ref.i), k = g('i_now');
            return { title: 'the stout, ring ' + q.ir + ' of ' + NR + ' (r = ' + Sim.fmt(q.r * 1000, 1) + ' mm), angle ' + Sim.fmt(q.th * 180 / Math.PI, 1) + '°', at: nodeAt(ref.i),
              rows: [['η<sub>i,j</sub>', g('eta_draw')[ref.i], 'm', 'eta_draw', ref.i], ['b<sub>n,i,j</sub>', g('eta_q')[k * M + ref.i], '', 'eta_q', k * M + ref.i], ['Δη', g('lean_now'), 'mm', 'lean_now'], ['t', g('t_play'), 's', 't_play'], ['n', k, '', 'i_now']] };
          }
          if (ref.what === 'wheel') return { title: 'the wheel', at: { x: g('axle_px_x'), y: g('axle_px_y') }, rows: [['z<sub>w</sub>', g('zw_now'), 'm', 'zw_now'], ['x', g('x_now'), 'm', 'x_now'], ['v', g('v_now'), 'm/s', 'v_now'], ['n', g('i_now'), '', 'i_now']] };
          return { title: 'the body', at: { x: g('body_px_x'), y: g('body_px_y') }, rows: [['z<sub>b</sub>', g('zb_now'), 'm', 'zb_now'], ['v', g('v_now'), 'm/s', 'v_now'], ['n', g('i_now'), '', 'i_now']] };
        },
        locate: (name, idx) => {
          if (name === 'eta_draw') return nodeAt(idx);
          if (name === 'eta_q') { const i = idx % M; return Math.floor(idx / M) === g('i_now') ? nodeAt(i) : null; }
          return null;
        },
        check: {
          ride_i: () => ({ formula: 'read from the Set speed control now', inputs: [['control', vbar.value, '', 0]], value: +vbar.value }),
          v0: () => ({ formula: 'v<sub>0</sub> of ride i<sub>ride</sub> in the file (rides sorted by speed)', inputs: [inp('ride_i', 'i<sub>ride</sub>', '', 0)], value: rides[g('ride_i')].v0 }),
          road: () => ({ formula: 'road of ride i<sub>ride</sub> in the file', inputs: [inp('ride_i', 'i<sub>ride</sub>', '', 0)], value: rides[g('ride_i')].road }),
          n_rides: () => ({ formula: 'rides listed in index.json', inputs: [], value: IDX.rides.length }),
          file_bytes: () => ({ formula: 'size written in index.json when the data was committed', inputs: [], value: fileIdx.bytes }),
          sha_file: () => ({ formula: 'SHA-256 written in index.json when the data was committed; equal only if not one byte changed on the way', inputs: [], value: fileIdx.sha256 }),
          generated: () => ({ formula: 'date in index.json', inputs: [], value: IDX.generated }),
          nb_version: () => ({ formula: 'Kaggle notebook version in index.json', inputs: [], value: IDX.kaggle.version }),
          R_fill: () => { const f = g('fill') / G.dz, i = Math.min(Math.floor(f), G.R.length - 2); return { formula: 'R<sub>i</sub> + (h<sub>0</sub>/Δz − i)(R<sub>i+1</sub> − R<sub>i</sub>), i = ⌊h<sub>0</sub>/Δz⌋, from the measured glass table (guinness-glass.js)', inputs: [inp('fill', 'h<sub>0</sub>', 'm', 4), ['Δz', G.dz, 'm', 4], ['R<sub>i</sub>', G.R[i], 'm', 5], ['R<sub>i+1</sub>', G.R[i + 1], 'm', 5]], value: G.R[i] + (f - i) * (G.R[i + 1] - G.R[i]) }; },
          r_s: () => ({ formula: 'R(h<sub>0</sub>): the drawing’s outer ring is the glass’s radius at the fill', inputs: [inp('R_fill', 'R(h<sub>0</sub>)', 'm', 5)], value: g('R_fill') }),
          z_rim: () => ({ formula: '(number of table rows − 1) Δz', inputs: [['rows', G.R.length, '', 0], ['Δz', G.dz, 'm', 4]], value: (G.R.length - 1) * G.dz }),
          t_n: (n) => ({ formula: 'n / f<sub>s</sub>, n = ' + n, inputs: [inp('fps', 'f<sub>s</sub>', '1/s', 0)], value: n / g('fps') }),
          road_x: (m) => ({ formula: 'x<sub>0</sub> + m Δx<sub>road</sub>, m = ' + m, inputs: [['x<sub>0</sub>', rides[g('ride_i')].road_x0, 'm', 3], ['Δx<sub>road</sub>', rides[g('ride_i')].road_dx, 'm', 4]], value: rides[g('ride_i')].road_x0 + m * rides[g('ride_i')].road_dx }),
          n_frames: () => ({ formula: 'frames listed for this ride in index.json', inputs: [inp('ride_i', 'i<sub>ride</sub>', '', 0)], value: (IDX.rides.slice().sort((a, b) => a.v0 - b.v0)[g('ride_i')] || {}).frames }),
          dur: () => ({ formula: '(N − 1) / f<sub>s</sub>', inputs: [inp('n_frames', 'N', '', 0), inp('fps', 'f<sub>s</sub>', '1/s', 0)], value: (g('n_frames') - 1) / g('fps') }),
          lean_max: () => { const a = g('lean'); let m = 0; for (let k = 0; k < g('n_frames'); k++) m = Math.max(m, Math.abs(a[k])); return { formula: 'max over all N stored frames of |Δη<sub>n</sub>|', inputs: [inp('n_frames', 'N', '', 0)], value: m }; },
          v_min: () => { const a = g('v'); let m = Infinity; for (let k = 0; k < g('n_frames'); k++) m = Math.min(m, a[k]); return { formula: 'min over all N stored frames of v<sub>n</sub>', inputs: [inp('n_frames', 'N', '', 0)], value: m }; },
          v_max: () => { const a = g('v'); let m = -Infinity; for (let k = 0; k < g('n_frames'); k++) m = Math.max(m, a[k]); return { formula: 'max over all N stored frames of v<sub>n</sub>', inputs: [inp('n_frames', 'N', '', 0)], value: m }; },
          spill_end: () => ({ formula: 'm<sub>s</sub> at the last frame, n = N − 1', inputs: [inp('n_frames', 'N', '', 0)], value: g('spill')[g('n_frames') - 1] }),
          playing: () => ({ formula: 'the Play / Pause button now says', inputs: [['button', play.textContent, '']], value: play.textContent === 'Pause' }),
          rate: () => { const left = g('dur') - g('t_play'); return { formula: 'r = 1 while T<sub>ride</sub> − t ≥ 3 s, else √((T<sub>ride</sub> − t) / 3 s)' + (playing ? '' : ' (paused: the last rate is kept)'), inputs: [inp('dur', 'T<sub>ride</sub>', 's', 2), inp('t_play', 't', 's', 3)], value: playing && !ended ? (left >= SLOW ? 1 : Math.sqrt(Math.max(0, left) / SLOW)) : g('rate') }; },
          i_now: () => ({ formula: 'round(t f<sub>s</sub>), kept within 0 … N − 1', inputs: [inp('t_play', 't', 's', 3), inp('fps', 'f<sub>s</sub>', '1/s', 0), inp('n_frames', 'N', '', 0)], value: Math.min(g('n_frames') - 1, Math.max(0, Math.round(g('t_play') * g('fps')))) }),
          x_now: atNow('x', 'x<sub>n</sub>'), v_now: atNow('v', 'v<sub>n</sub>'), zb_now: atNow('zb', 'z<sub>b,n</sub>'), zw_now: atNow('zw', 'z<sub>w,n</sub>'),
          lean_now: atNow('lean', 'Δη<sub>n</sub>'), spill_now: atNow('spill', 'm<sub>s,n</sub>'),
          eta_draw: (i) => ({ formula: 'h<sub>0</sub> + (b − 128) δ at ring ' + Math.floor(i / NTH) + ', angle ' + (i % NTH) + ' of frame n', inputs: BYTE(i), value: etaFromBytes(i) }),
          eta_front: () => ({ formula: 'h<sub>0</sub> + (b − 128) δ at the outer ring, angle 0 (the front wall)', inputs: BYTE(NR * NTH), value: etaFromBytes(NR * NTH) }),
          eta_back: () => ({ formula: 'h<sub>0</sub> + (b − 128) δ at the outer ring, angle 180° (the back wall)', inputs: BYTE(NR * NTH + NTH / 2), value: etaFromBytes(NR * NTH + NTH / 2) }),
          eta_mid: () => ({ formula: 'h<sub>0</sub> + (b − 128) δ on the axis (ring 0)', inputs: BYTE(0), value: etaFromBytes(0) }),
          dw: () => ({ formula: 'η<sub>front</sub> − η<sub>back</sub>', inputs: [inp('eta_front', 'η<sub>front</sub>', 'm', 5), inp('eta_back', 'η<sub>back</sub>', 'm', 5)], value: g('eta_front') - g('eta_back') }),
          lean_gap: () => ({ formula: 'Δη − 1000 Δη<sub>grid</sub>; |gap| ≤ 1000 δ = 0.2 mm, because the file stores the surface rounded to q and Kaggle took Δη before rounding', inputs: [inp('lean_now', 'Δη', 'mm', 2), inp('dw', 'Δη<sub>grid</sub>', 'm', 5)], value: g('lean_now') - 1000 * g('dw') }),
          scale: () => ({ formula: 'H / 0.40 m: 40 cm of scene from top to bottom at the target', inputs: [inp('canvas_h', 'H', 'px', 1)], value: g('canvas_h') / 0.40 }),
          cam_x: () => ({ formula: 'the camera rides with the cart: x', inputs: [inp('x_now', 'x', 'm', 4)], value: g('x_now') }),
          elev: () => ({ formula: '16° in radians (this page’s camera)', inputs: [], value: 16 * Math.PI / 180 }),
          azim: () => ({ formula: '−24° in radians (this page’s camera)', inputs: [], value: -24 * Math.PI / 180 }),
          focal: () => ({ formula: 'F = s d', inputs: [inp('scale', 's', 'px/m', 2), inp('cam_dist', 'd', 'm', 3)], value: g('scale') * g('cam_dist') }),
          cam_cx: () => ({ formula: 'W / 2', inputs: [inp('canvas_w', 'W', 'px', 1)], value: g('canvas_w') / 2 }),
          cam_cy: () => { const e = g('elev'), a = g('azim'), Dd = g('cam_dist'), zT = g('cam_zt'), d = [Math.sin(a) * Math.cos(e), Math.cos(a) * Math.cos(e), -Math.sin(e)], u = [Math.sin(a) * Math.sin(e), Math.cos(a) * Math.sin(e), Math.cos(e)], v0 = [Dd * d[0], Dd * d[1], -(zT - Dd * d[2])], du = (p, q) => p[0] * q[0] + p[1] * q[1] + p[2] * q[2];
            return { formula: '0.95 H + F (v·u)/(v·d), v from the camera to the road under the axle', inputs: [inp('canvas_h', 'H', 'px', 1)].concat(CAMIN().slice(0, 5)), value: GROUND_Y * g('canvas_h') + g('focal') * du(v0, u) / du(v0, d) }; },
          ground_px: () => projCheck('the road under the axle', [0, 0, 0], 1),
          axle_px_x: () => projCheck('the axle', [0, -0.01, g('zw_now')], 0, [inp('zw_now', 'z<sub>w</sub>', 'm', 6)]),
          axle_px_y: () => projCheck('the axle', [0, -0.01, g('zw_now')], 1, [inp('zw_now', 'z<sub>w</sub>', 'm', 6)]),
          body_px_x: () => projCheck('the body’s near bottom edge', [-0.08, -0.06, g('zb_now')], 0, [inp('zb_now', 'z<sub>b</sub>', 'm', 6)]),
          body_px_y: () => projCheck('the body’s near bottom edge', [-0.08, -0.06, g('zb_now')], 1, [inp('zb_now', 'z<sub>b</sub>', 'm', 6)]),
          glass_px_x: () => projCheck('the reference point on the glass axis', [0, 0, g('zb_now') + GLASS_FLOOR + g('fill')], 0, [inp('zb_now', 'z<sub>b</sub>', 'm', 6), inp('fill', 'h<sub>0</sub>', 'm', 4)]),
          glass_px_y: () => projCheck('the reference point on the glass axis', [0, 0, g('zb_now') + GLASS_FLOOR + g('fill')], 1, [inp('zb_now', 'z<sub>b</sub>', 'm', 6), inp('fill', 'h<sub>0</sub>', 'm', 4)]),
          front_px_x: () => projCheck('the head’s band at the front wall (0.98 r<sub>s</sub>, 0, z<sub>G</sub> + η<sub>front</sub> + ¾ h<sub>head</sub>)', [0.98 * g('r_s'), 0, zG() + g('eta_front') + 0.75 * g('head_h')], 0, [inp('zb_now', 'z<sub>b</sub>', 'm', 6), inp('eta_front', 'η<sub>front</sub>', 'm', 5), inp('head_h', 'h<sub>head</sub>', 'm', 3)]),
          front_px_y: () => projCheck('the head’s band at the front wall (0.98 r<sub>s</sub>, 0, z<sub>G</sub> + η<sub>front</sub> + ¾ h<sub>head</sub>)', [0.98 * g('r_s'), 0, zG() + g('eta_front') + 0.75 * g('head_h')], 1, [inp('zb_now', 'z<sub>b</sub>', 'm', 6), inp('eta_front', 'η<sub>front</sub>', 'm', 5), inp('head_h', 'h<sub>head</sub>', 'm', 3)]),
          back_px_x: () => projCheck('the head’s top on the axis (0, 0, z<sub>G</sub> + η<sub>mid</sub> + h<sub>head</sub>)', [0, 0, zG() + g('eta_mid') + g('head_h')], 0, [inp('zb_now', 'z<sub>b</sub>', 'm', 6), inp('eta_mid', 'η<sub>mid</sub>', 'm', 5), inp('head_h', 'h<sub>head</sub>', 'm', 3)]),
          back_px_y: () => projCheck('the head’s top on the axis (0, 0, z<sub>G</sub> + η<sub>mid</sub> + h<sub>head</sub>)', [0, 0, zG() + g('eta_mid') + g('head_h')], 1, [inp('zb_now', 'z<sub>b</sub>', 'm', 6), inp('eta_mid', 'η<sub>mid</sub>', 'm', 5), inp('head_h', 'h<sub>head</sub>', 'm', 3)]),
          w11: () => ({ formula: '2π f<sub>11</sub>', inputs: [inp('f11', 'f<sub>11</sub>', 'Hz', 3)], value: 2 * Math.PI * g('f11') }),
          q1: (n) => { const b = g('eta_q'); let a = 0; for (let j = 0; j < NTH; j++) a += (g('fill') + (b[n * M + NR * NTH + j] - 128) * g('q')) * Math.cos(2 * Math.PI * j / NTH);
            return { formula: '1000 (2/N<sub>θ</sub>) Σ<sub>j</sub> [h<sub>0</sub> + (b<sub>n,N<sub>r</sub>,j</sub> − 128) δ] cos(2π j/N<sub>θ</sub>), the 64 stored bytes of the outer ring at frame n = ' + n, inputs: [inp('fill', 'h<sub>0</sub>', 'm', 4), inp('q', 'δ', 'm', 4), inp('nth', 'N<sub>θ</sub>', '', 0)], value: 2 / NTH * a * 1000 }; },
          p1: (n) => { const q = g('q1'), N = g('n_frames'), k0 = Math.max(0, n - 1), k1 = Math.min(N - 1, n + 1);
            return { formula: '(q<sub>' + k1 + '</sub> − q<sub>' + k0 + '</sub>) / (' + (k1 - k0) + ' sin ω<sub>11</sub>h)' + (k1 - k0 === 1 ? ', one-sided at the end of the ride' : ''), inputs: [['q<sub>' + k1 + '</sub>', q[k1], 'mm', 3], ['q<sub>' + k0 + '</sub>', q[k0], 'mm', 3], inp('w11', 'ω<sub>11</sub>', 'rad/s', 3), inp('fps', 'f<sub>s</sub>', '1/s', 0)], value: (q[k1] - q[k0]) / ((k1 - k0) * Math.sin(g('w11') / g('fps'))) }; },
          ph_range: () => { const q = g('q1'), p = g('p1'); let m = 0; for (let k = 0; k < g('n_frames'); k++) m = Math.max(m, Math.abs(q[k]), Math.abs(p[k])); return { formula: '1.1 max over all N frames of max(|q<sub>n</sub>|, |p<sub>n</sub>|)', inputs: [inp('n_frames', 'N', '', 0)], value: 1.1 * m }; },
          q_now: atNow('q1', 'q<sub>n</sub>'), p_now: atNow('p1', 'p<sub>n</sub>'),
          amp_now: () => ({ formula: '√(q² + p²)', inputs: [inp('q_now', 'q', 'mm', 3), inp('p_now', 'p', 'mm', 3)], value: Math.hypot(g('q_now'), g('p_now')) }),
          ph_x_px: () => ({ formula: 'X<sub>ph</sub> + s<sub>ph</sub> q', inputs: [inp('ph_cx', 'X<sub>ph</sub>', 'px', 2), inp('ph_s', 's<sub>ph</sub>', 'px/mm', 3), inp('q_now', 'q', 'mm', 3)], value: g('ph_cx') + g('ph_s') * g('q_now') }),
          ph_y_px: () => ({ formula: 'Y<sub>ph</sub> − s<sub>ph</sub> p', inputs: [inp('ph_cy', 'Y<sub>ph</sub>', 'px', 2), inp('ph_s', 's<sub>ph</sub>', 'px/mm', 3), inp('p_now', 'p', 'mm', 3)], value: g('ph_cy') - g('ph_s') * g('p_now') }),
          ph_s: () => { const r = phc.getBoundingClientRect(), side = Math.min(Math.round(r.width) - 70, Math.round(r.height) - 56); return { formula: 'side / (2 q<sub>max</sub>), side = min(W − 70, H − 56) of the phase canvas', inputs: [['W', Math.round(r.width), 'px', 0], ['H', Math.round(r.height), 'px', 0], inp('ph_range', 'q<sub>max</sub>', 'mm', 3)], value: side / (2 * g('ph_range')) }; },
          canvas_w: () => ({ formula: 'width of the figure on the page, css px', inputs: [], value: cv.getBoundingClientRect().width }),
          canvas_h: () => ({ formula: 'canvas height in device px / device pixel ratio', inputs: [['height', cv.height, 'px', 0]], value: cv.height / (cv.width / cv.getBoundingClientRect().width) }),
        },
        drawn: {
          eta_front: () => headDrawn('front'), front_px_y: () => headDrawn('front'), dw: () => headDrawn('front'),
          eta_mid: () => headDrawn('back'), back_px_y: () => headDrawn('back'),
          axle_px_x: axleDrawn, axle_px_y: axleDrawn, zw_now: axleDrawn,
          body_px_y: bodyDrawn, zb_now: bodyDrawn,
          eta_draw: nodeDrawn,
          v_now: textDrawn('r-v', 'v', 3, 'm/s', 'cart speed'),
          lean_now: textDrawn('r-l', 'lean', 1, 'mm', 'surface lean'),
          spill_now: textDrawn('r-s', 'spill', 1, 'g', 'stout spilled'),
          ph_x_px: phDrawn, ph_y_px: phDrawn, q_now: phDrawn, p_now: phDrawn,
          x_now: () => ({ what: 'the cart’s position', drawn: 'not one point: the camera rides with the cart, so x shows as the road’s 10 cm ticks sliding under the wheel', expected: '', ok: null, note: 'Not read back as a pixel.' }),
        },
        round: { time: 't_play', label: () => ROUND + ' s of the stored ride, as it plays', length: () => ROUND,
          columns: ['x_now', 'v_now', 'lean_now', 'dw', 'zb_now', 'zw_now', 'spill_now', 'i_now'],
          point: () => ({ what: 'node', i: NR * NTH }),
          blocked: () => (g('dur') - g('t_play') < ROUND + SLOW ? 'Less than ' + (ROUND + SLOW) + ' s of computed data is left, and the playback slows down over the last ' + SLOW + ' s. Move the time back or ride again.' : null) },
        about: 'This page computes no physics: every number of the ride was computed on Kaggle and is read from the file, whose SHA-256 fingerprint is checked against index.json. The picture is the website’s own drawing code (stout-view.js) through a pinhole camera (looking down at 16°, turned 24° toward the front) that rides with the cart; every point the panel checks is recomputed from the camera’s stored constants. Four things differ between the data and the picture. (1) The surface is stored rounded to 0.2 mm steps; Kaggle’s lean Δη was taken before rounding, so it can differ from the lean of the stored grid by up to 0.2 mm (lean_gap; measured over all 1,803 stored frames: at most 0.19 mm). (2) Between the 17 × 64 grid nodes the surface is drawn by straight-line (bilinear) interpolation; the nodes themselves are drawn exactly. (3) The head is drawn, not computed: a 12 mm cream band laid on the stored surface; the glass’s highlights and tint are drawing only. (4) Only stored frames are shown, 30 per second of ride, never a blend of two; near the end of the data the playback slows down, so one stored frame can stay on screen longer. (5) The phase space is worked out here from the stored surface, not computed on Kaggle: q is the cos θ part of the outer ring, and its rate comes from the frames on either side, 1/30 s apart, divided by 2 sin(ω<sub>11</sub>h) instead of 2ω<sub>11</sub>h, so that a pure swing at f<sub>11</sub> = 3.421 Hz traces an exact circle (the plain central difference would read it 8 % low).',
      };
    }
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
