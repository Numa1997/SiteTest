/* Fig. 12, computed in JAX on Kaggle: plays the stored rides (public/data/fig12/<date>/, listed in index-jax.json) in real
 * time. Computes nothing physical: each stored frame (30 a second) holds the cart, the stout's surface on the solver's
 * columns, the head's thickness, the drops and the lumps of head; StoutView2 draws exactly those. No frame is interpolated
 * and the ride never slows: at the end of the stored time it stops. Every file is checked against the SHA-256 in the index. */
(function () {
  'use strict';
  const DIR = '../data/fig12/2026-11-13-run8/', INDEX_URL = DIR + 'index-jax.json';
  const GROUND_Y = 0.95, GLASS_BASE = 0.014, GLASS_FLOOR = 0.012;       // drawing constants handed to the view
  const REST = { zw: 0.04 - 0.0011, zb: 0.04 - 0.0011 + 0.135 - 0.0320 };  // the cart standing still (free-swing tests): drawn, not computed
  const $ = (id) => document.getElementById(id);
  const cv = $('cv'), play = $('play'), tbar = $('tbar'), host = $('ride-host'), roadCv = $('road');
  const fmt = (v, d) => (v == null || !isFinite(v)) ? '—' : v.toFixed(d);

  async function sha256(buf) {
    if (!(window.crypto && crypto.subtle)) return null;
    const h = new Uint8Array(await crypto.subtle.digest('SHA-256', buf));
    return Array.from(h, (b) => b.toString(16).padStart(2, '0')).join('');
  }

  fetch(INDEX_URL).then((r) => r.json()).then(start).catch((e) => { $('cap-t').textContent = 'data not loaded: ' + e.message; });

  async function start(IDX) {
    const G = window.GUINNESS_GLASS;
    const Rz = (z) => { const f = Math.max(0, z) / G.dz, i = Math.min(Math.floor(f), G.R.length - 2); return G.R[i] + (f - i) * (G.R[i + 1] - G.R[i]); };
    const zRim = (G.R.length - 1) * G.dz;
    const fluid = { modal: true, h0: 0.125, zRim: zRim, H: zRim, Rbox: Infinity, dx: 0.0015, Rz: Rz };
    let ride = null, bumps = [];
    const zr = (x) => { let s = 0; for (const b of bumps) { const u = (x - b.x) / b.L; if (Math.abs(u) < 0.5) s += 0.5 * b.h * (1 + Math.cos(2 * Math.PI * u)); } return s; };
    const cart = { x: 0.5, vx: 0, zw: REST.zw, zb: REST.zb, Rw: 0.04, Mb: 1.5, ml: 0.43, Ls: 0.135, g: 9.81, k: 600, us: 0, glassFloor: GLASS_FLOOR, road: { zr: zr } };
    const view = new window.StoutView2(cv, { fluid: fluid, cart: cart, drops: [] }, { viewHeight: 0.40, groundY: GROUND_Y, elevDeg: 16, azimDeg: -24 });
    view.glassWall = 0.0032; view.glassBase = GLASS_BASE;
    if (document.fonts && document.fonts.load) { try { await document.fonts.load('400 100px "Instrument Serif"'); } catch (e) { /* the lettering falls back to a serif */ } }

    const files = IDX.files.slice(), cache = new Map();
    let cur = -1, T = 0, playing = true, last = null, lastTxt = 0, loading = false;
    const dur = () => (ride.frames - 1) / ride.fps;

    async function load(i) {
      if (cache.has(i)) return cache.get(i);
      const f = files[i], buf = await (await fetch(DIR + f.path)).arrayBuffer(), sha = await sha256(buf);
      if (sha && f.sha256 && sha !== f.sha256) throw new Error(f.path + ': the file does not match the fingerprint stored with it');
      const D = JSON.parse(new TextDecoder().decode(buf)), r = await new window.StoutRide(D).unpack();
      r.sha = sha; r.bytes = buf.byteLength; cache.set(i, r); return r;
    }
    async function choose(i) {
      if (loading || i === cur) return;
      loading = true; cv.classList.add('is-held'); $('cap-t').textContent = 'loading ' + files[i].path + ' …';
      try {
        const r = await load(i); ride = r; cur = i; bumps = r.D.bumps || []; fluid.h0 = r.fill; fluid.dx = r.dx; T = 0; playing = true; play.textContent = 'Pause';
        [...host.children].forEach((b, j) => b.setAttribute('aria-pressed', j === i ? 'true' : 'false'));
        if (cmpRows) cmpRows.forEach((tr, j) => tr.classList.toggle('is-on', j === i));
        $('ride-note').textContent = describe(r.D); drawRoad();
      } catch (e) { $('cap-t').textContent = e.message; }
      loading = false; cv.classList.remove('is-held');
    }
    function describe(D) {
      const h = D.head ? ` Head of foam: ${(D.head_ml || 0).toFixed(0)} mL at the start, bubbles of ${(D.head.R32 * 1e6).toFixed(0)} µm (Sauter radius), ${Math.round(D.head.phi_l * 100)} % liquid.` : '';
      if (D.x) return `The cart drives at ${D.v0.toFixed(1)} m/s over: ${D.road}. ${D.frames} stored pictures, ${((D.frames - 1) / D.fps).toFixed(1)} s.` + h;
      return `The cart stands still. ${D.task && D.task.end ? 'The glass is given one short push along the road after 0.3 s, then left alone.' : ''} ${D.frames} stored pictures, ${((D.frames - 1) / D.fps).toFixed(1)} s.` + h;
    }
    // the comparison: every stored ride with the numbers Kaggle stored for it (largest lean, head and stout spilled, the
    // largest motor current among the stored pictures); a row chooses its ride. Nothing here is computed but the layout.
    let cmpRows = null;
    const cmp = $('cmp');
    if (cmp) {
      const CT = { speed: 'speed held only', preview: 'road preview', slosh: 'slosh LQR', joint: 'joint control' };
      const order = files.map((f, i) => i).filter((i) => files[i].kind === 'ride')
        .sort((a, b) => (files[a].road || '').localeCompare(files[b].road || '') || ['speed', 'preview', 'slosh', 'joint'].indexOf(files[a].ctrl) - ['speed', 'preview', 'slosh', 'joint'].indexOf(files[b].ctrl));
      const tb = document.createElement('tbody'); cmpRows = files.map(() => document.createElement('tr'));
      let road = null;
      for (const i of order) {
        const f = files[i], m = f.measured || {};
        if (f.road !== road) { road = f.road; const th = document.createElement('tr'); th.className = 'cmp-road'; th.innerHTML = `<th colspan="6">${road}, ${(f.v0 || 0).toFixed(1)} m/s</th>`; tb.appendChild(th); }
        const tr = cmpRows[i]; tr.tabIndex = 0;
        tr.innerHTML = `<td>${CT[f.ctrl] || f.ctrl}</td><td>${fmt(m.tilt_max_mm, 1)}</td><td>${fmt(m.lean_max_mm, 1)}</td><td>${fmt(m.head_spilled_ml, 2)}</td><td>${fmt(m.spilled_g, 2)}</td><td>${fmt(m.i_max_stored_A, 2)}</td>`;
        tr.addEventListener('click', () => choose(i)); tr.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(i); } });
        tb.appendChild(tr);
      }
      cmp.appendChild(tb);
    }
    files.forEach((f, i) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'btn btn--ghost g-ride'; b.textContent = f.label || f.path; b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', () => choose(i)); host.appendChild(b);
    });

    // the road of the chosen ride, drawn from its stored bumps, with the cart's stored position
    function drawRoad() {
      if (!roadCv || !ride) return;
      const dpr = Math.min(2, window.devicePixelRatio || 1), W = roadCv.clientWidth, H = roadCv.clientHeight; roadCv.width = W * dpr; roadCv.height = H * dpr;
      const c = roadCv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
      const D = ride.D, x0 = 0, x1 = D.x ? Math.max(4, D.x[D.x.length - 1] + 0.5) : 4, zmax = 0.03, X = (x) => 8 + (x - x0) / (x1 - x0) * (W - 16), Y = (z) => H - 16 - z / zmax * (H - 30);
      c.strokeStyle = 'rgba(28,21,24,0.25)'; c.lineWidth = 1; c.beginPath(); c.moveTo(X(x0), Y(0)); c.lineTo(X(x1), Y(0)); c.stroke();
      c.beginPath(); for (let q = 0; q <= 400; q++) { const x = x0 + (x1 - x0) * q / 400; q ? c.lineTo(X(x), Y(zr(x))) : c.moveTo(X(x), Y(zr(x))); }
      c.strokeStyle = '#1c1518'; c.lineWidth = 1.6; c.stroke();
      c.font = '10px "IBM Plex Mono", monospace'; c.fillStyle = '#6b6166'; c.textAlign = 'left'; c.fillText('road height, up to 30 mm', 8, 11); c.textAlign = 'right'; c.fillText(x1.toFixed(1) + ' m', W - 8, H - 3); c.textAlign = 'left'; c.fillText('0 m', 8, H - 3);
      const k = Math.round(T * ride.fps), xc = D.x ? D.x[Math.min(k, D.frames - 1)] : 0.5;
      c.fillStyle = '#7a1f2b'; c.beginPath(); c.arc(X(xc), Y(zr(xc)) - 5, 4, 0, 2 * Math.PI); c.fill();
    }

    function resize() {
      const box = cv.parentElement.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
      cv.width = Math.max(2, Math.round(box.width * dpr)); cv.height = Math.max(2, Math.round(box.height * dpr)); view.cssW = box.width;
      drawRoad();
    }
    window.addEventListener('resize', resize); resize();

    play.addEventListener('click', () => {
      if (!ride) return;
      if (T >= dur() - 1e-9) { T = 0; playing = true; } else playing = !playing;
      play.textContent = playing ? 'Pause' : 'Play';
    });
    $('again').addEventListener('click', () => { T = 0; playing = true; play.textContent = 'Pause'; });
    tbar.addEventListener('input', () => { if (ride) { T = tbar.value / 1000 * dur(); } });

    function tick(now) {
      requestAnimationFrame(tick);
      if (!ride) return;
      const dt = last == null ? 0 : Math.min(0.1, (now - last) / 1000); last = now;
      if (playing) { T += dt; if (T >= dur()) { T = dur(); playing = false; play.textContent = 'Ride again'; } }
      const D = ride.D, k = Math.min(D.frames - 1, Math.round(T * ride.fps));
      if (D.x) { cart.x = D.x[k]; cart.vx = D.v[k]; cart.zb = D.zb[k]; cart.zw = D.zw[k]; cart.us = D.us ? D.us[k] : 0; } else { cart.x = 0.5; cart.vx = 0; cart.zb = REST.zb; cart.zw = REST.zw; cart.us = 0; }
      view.setFrame(ride, k); view.draw();
      if (document.activeElement !== tbar) tbar.value = Math.round(T / dur() * 1000);
      if (now - lastTxt > 250) {                                  // words rewritten four times a second
        lastTxt = now;
        $('t-out').textContent = `${fmt(D.t[k], 2)} of ${fmt(dur(), 1)} s`;
        $('r-v').textContent = D.v ? fmt(D.v[k], 2) + ' m/s' : 'at rest';
        // the books as the run counted them (stored to 1 mg, 2.3 particles of 0.429 mg, and to 0.001 mL); older files hold no head volume
        if ($('r-sg')) $('r-sg').textContent = D.stout_g ? fmt(D.stout_g[k], 3) + ' g' : '—';
        $('r-s').textContent = fmt(D.spill_g[k], 3) + ' g';
        if ($('r-hg')) $('r-hg').textContent = D.head_glass_ml ? fmt(D.head_glass_ml[k], 2) + ' mL' : (D.head ? '—' : 'no head');
        $('r-h').textContent = fmt(D.head_spill_ml[k], 2) + ' mL';
        $('r-d').textContent = String(D.nd[k] + D.nl[k]);
        if ($('r-i')) $('r-i').textContent = D.i ? fmt(D.i[k], 2) + ' A' : '—';
        if ($('r-u')) $('r-u').textContent = D.us ? fmt(D.us[k], 1) + ' N' : (D.i ? '0 N' : '—');
        $('cap-t').textContent = `stored picture ${k + 1} of ${D.frames} · ${files[cur].path}`;
        drawRoad();
      }
    }
    await choose(Math.max(0, files.findIndex((f) => f.default)));
    requestAnimationFrame(tick);
    window.GuinnessJax = { view: view, files: files, state: () => ({ T: T, k: Math.round(T * ride.fps), playing: playing, cur: cur }), choose: choose, seek: (t) => { T = t; playing = false; } };
  }
})();
