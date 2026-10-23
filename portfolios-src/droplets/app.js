/* Droplet Collection: the page's script. Uses PHYS (the model), CHART (SVG charts) and DATA (stored runs and tables).
   Nothing reacts to the pointer merely crossing a figure: every action starts from a button, a select or a slider. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ------------------------------------------------------------ tabs, with #sim / #book / #problems / #checks deep links
  var TABS = ['sim', 'book', 'problems', 'checks'];
  function show(tab, frag) {
    TABS.forEach(function (t) {
      $(t).hidden = t !== tab;
      $('t-' + t).setAttribute('aria-selected', t === tab ? 'true' : 'false');
    });
    if (frag) { var el = document.getElementById(frag); if (el) el.scrollIntoView({ block: 'start' }); }
    else window.scrollTo(0, 0);
  }
  function route() {
    var h = decodeURIComponent((location.hash || '').slice(1));
    if (!h) { show('sim'); return; }
    if (TABS.indexOf(h) >= 0) { show(h); return; }
    var el = document.getElementById(h);
    if (el) { var host = el.closest('.tab'); if (host) show(host.id, h); }
  }
  TABS.forEach(function (t) { $('t-' + t).addEventListener('click', function () { history.replaceState(null, '', '#' + t); show(t); }); });
  window.addEventListener('hashchange', route);
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = decodeURIComponent(a.getAttribute('href').slice(1)), el = document.getElementById(id);
    if (!el) return;
    var host = el.closest('.tab');
    if (host && host.hidden) { e.preventDefault(); history.replaceState(null, '', '#' + id); show(host.id, id); }
  });
  var bar = document.querySelector('.progress span');
  window.addEventListener('scroll', function () {
    var h = document.documentElement, p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
    bar.style.width = (100 * p).toFixed(1) + '%';
  }, { passive: true });

  var A = PHYS.air(283.15, 85000);
  var MODES = [{ N: 300e6, rg: 8e-6, sg: 1.25 }, { N: 1e6, rg: 40e-6, sg: 1.2 }];
  function minutes(t) { return t.map(function (s) { return s / 60; }); }
  function tCross(t, F, q) {
    for (var i = 1; i < F.length; i++) if (F[i] >= q) return t[i - 1] + (q - F[i - 1]) / (F[i] - F[i - 1]) * (t[i] - t[i - 1]);
    return null;
  }

  // ------------------------------------------------------------ panel 1: the cloud in a box (SCE or GCE, choose the ingredients)
  var box = $('box');
  if (box) {
    var ref = DATA.warm, running = false;
    function kopt() {
      var o = { speed: $('bx-speed').value, eff: $('bx-eff').value, coal: $('bx-coal').value, near: 'clamp', tab: DATA.etab_warm, hall: DATA.hall1980 };
      return o;
    }
    function drawF40(series) {
      var s = [
        { x: minutes(ref.thesis.t), y: ref.thesis.F40, label: 'thesis kernel, SCE (stored)', color: '#6f665e', dash: '5 4', width: 1.5 },
        { x: minutes(ref.extended.t), y: ref.extended.F40, label: 'extended kernel, SCE (stored)', color: '#33627f', dash: '5 4', width: 1.5 }
      ].concat(series || []);
      $('bx-f40').innerHTML = CHART.line({ w: 620, h: 300, series: s, xmin: 0, xmax: 30, ymin: 0, ymax: 1, xlabel: 'time (min)', ylabel: 'water in drops r ≥ 40 µm', id: 'bxf' });
    }
    function drawSpec(grid, N, t) {
      var x = grid.r.map(function (r) { return r * 1e6; });
      var g0 = PHYS.lognormalBins(grid, MODES).map(function (n, k) { return n * grid.x[k] / grid.dlnr * 1e3; });
      var g = N.map(function (n, k) { return n * grid.x[k] / grid.dlnr * 1e3; });
      $('bx-spec').innerHTML = CHART.line({ w: 620, h: 280, xlog: true, xmin: 2, xmax: 4000, ymin: 0, series: [
        { x: x, y: g0, label: 'start', color: '#6f665e', dash: '4 3' }, { x: x, y: g, label: 'after ' + Math.round(t / 60) + ' min', color: '#7d1d2f' }],
        xlabel: 'radius r (µm)', ylabel: 'g = dM/d ln r (g/m³)', id: 'bxs' });
    }
    drawF40();
    $('bx-run').addEventListener('click', function () {
      if (running) return; running = true;
      var o = kopt(), book = $('bx-book').value, grid = PHYS.makeGrid(4, 4e-3), tEnd = 30 * 60;
      $('bx-status').textContent = 'building the kernel…';
      setTimeout(function () {
        if (book === 'gce') {
          var g = PHYS.gceRun(grid, A, o, MODES, { dt: 1, tEnd: tEnd, recordEvery: 10 });
          drawF40([{ x: minutes(g.t), y: g.F40, label: 'your run (GCE)', color: '#7d1d2f', width: 2.5 }]);
          report(g.t, g.F40, 'GCE'); running = false; return;
        }
        var K = PHYS.kernelMatrix(grid, A, o), N = PHYS.lognormalBins(grid, MODES), over = { N: 0, M: 0 };
        var M0 = PHYS.moments(grid, N, over).M, k40 = grid.r.findIndex(function (r) { return r >= 40e-6; });
        var t = 0, tt = [0], FF = [], snaps = {};
        function F40() { var m = 0; for (var k = k40; k < grid.n; k++) m += N[k] * grid.x[k]; return m / M0; }
        FF.push(F40());
        (function chunk() {
          var stop = Math.min(tEnd, t + 120);
          while (t < stop) { PHYS.sceStep(grid, K, N, over, 1); t += 1; if (t % 10 === 0) { tt.push(t); FF.push(F40()); } if (t % 60 === 0) snaps[t] = Float64Array.from(N); }
          drawF40([{ x: minutes(tt), y: FF, label: 'your run (SCE)', color: '#7d1d2f', width: 2.5 }]);
          $('bx-status').textContent = 'solving… ' + Math.round(t / 60) + ' of 30 min';
          if (t < tEnd) setTimeout(chunk, 0);
          else {
            report(tt, FF, 'SCE'); running = false;
            var sl = $('bx-time'); sl.disabled = false;
            var upd = function () { var m = +sl.value; $('bx-tlab').textContent = m + ' min'; drawSpec(grid, m === 0 ? PHYS.lognormalBins(grid, MODES) : snaps[m * 60], m * 60); };
            sl.oninput = upd; upd();
          }
        })();
      }, 20);
    });
    function report(t, F, how) {
      var a = tCross(t, F, 0.5), b = tCross(t, F, 0.9);
      $('bx-status').textContent = 'done';
      $('bx-out').innerHTML = how + ' at 4 bins per doubling: half the water above 40 µm at <b>' + (a ? (a / 60).toFixed(1) + ' min' : 'not within 30 min') +
        '</b>, 90 % at <b>' + (b ? (b / 60).toFixed(1) + ' min' : 'not within 30 min') + '</b>. (The stored curves use 8 bins per doubling.)';
    }
  }

  // ------------------------------------------------------------ panel 2: a droplet meets a collector
  var tj = $('traj');
  if (tj) {
    function drawTraj() {
      var R = +$('tj-R').value * 1e-6, r = +$('tj-r').value * 1e-6, flow = $('tj-flow').value;
      $('tj-Rl').textContent = (R * 1e6).toFixed(0) + ' µm'; $('tj-rl').textContent = (r * 1e6).toFixed(0) + ' µm';
      if (r >= R) { $('tj-out').textContent = 'Choose a droplet smaller than the collector.'; $('tj-svg').innerHTML = ''; return; }
      var U = PHYS.vBeard(R, A), vr = PHYS.vBeard(r, A), gs = PHYS.G0 * (1 - A.rho / 1000), St = vr / gs * U / R, S = vr / U, p = r / R;
      var Re = 2 * R * A.rho * U / A.mu;
      var e = PHYS.pairEfficiency(R, r, A), fl = flow === 'blend' ? 'stokes' : flow;
      var bc = Math.sqrt(Math.max(0, (flow === 'potential' ? e.EP : e.ES))) * (1 + p);
      var W = 520, H = 420, sc = 70, cx = W / 2, cz = H * 0.42, parts = ['<svg viewBox="0 0 ' + W + ' ' + (H + 60) + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="droplet paths around a collector">',
        '<rect width="' + W + '" height="' + (H + 60) + '" fill="#fff"/><defs><clipPath id="tjclip"><rect width="' + W + '" height="' + H + '"/></clipPath></defs><g transform="translate(0 30)"><rect width="' + W + '" height="' + H + '" fill="#fff" stroke="#ece3d2"/><g clip-path="url(#tjclip)">'];
      var offs = [0.15, 0.35, 0.55, 0.75, 0.95, 1.15, 1.35, 1.55, 1.75].map(function (f) { return f * (1 + p); });
      offs.forEach(function (b) {
        var q = PHYS.trajPath(fl, St, S, p, b, 6, 3.2), pts = [];
        for (var i = 0; i < q.x.length; i++) { pts.push((cx + q.x[i] * sc).toFixed(1) + ',' + (cz - q.z[i] * sc).toFixed(1)); pts.push((cx - q.x[i] * sc).toFixed(1) + ',' + (cz - q.z[i] * sc).toFixed(1)); }
        var L = [], Rr = [];
        for (var j = 0; j < q.x.length; j++) { L.push((cx + q.x[j] * sc).toFixed(1) + ',' + (cz - q.z[j] * sc).toFixed(1)); Rr.push((cx - q.x[j] * sc).toFixed(1) + ',' + (cz - q.z[j] * sc).toFixed(1)); }
        var col = q.hit ? '#7d1d2f' : '#33627f';
        parts.push('<polyline fill="none" stroke="' + col + '" stroke-width="1.6" points="' + L.join(' ') + '"/><polyline fill="none" stroke="' + col + '" stroke-width="1.6" points="' + Rr.join(' ') + '"/>');
      });
      parts.push('<circle cx="' + cx + '" cy="' + cz + '" r="' + sc + '" fill="#e1ebf0" stroke="#23160f" stroke-width="1.5"/>');
      parts.push('<circle cx="' + cx + '" cy="' + cz + '" r="' + (sc * (1 + p)) + '" fill="none" stroke="#6f665e" stroke-dasharray="3 3"/>');
      parts.push('</g></g><text x="12" y="19" class="tick">air rises past the collector (its frame); droplets enter from below</text>');
      parts.push('<text x="12" y="' + (H + 52) + '" class="tick">wine: touches · blue: carried round · dashed: contact at R + r</text></svg>');
      $('tj-svg').innerHTML = parts.join('');
      $('tj-out').innerHTML = 'Stokes number St = τU/R = <b>' + St.toFixed(2) + '</b> · settling ratio S = <b>' + S.toFixed(3) + '</b> · collector Re = <b>' + Re.toFixed(2) +
        '</b><br>E (creeping flow) = <b>' + e.ES.toFixed(3) + '</b> · E (potential flow) = <b>' + e.EP.toFixed(3) + '</b> · E (Langmuir’s blend) = <b>' + e.E.toFixed(3) + '</b>' +
        (p > 0.6 ? '<br>Size ratio p = ' + p.toFixed(2) + ' is above 0.6, where the one-sided flow fails: the collection equation uses E at p = 0.6 instead (chapter 3).' : '');
    }
    ['tj-R', 'tj-r', 'tj-flow'].forEach(function (id) { $(id).addEventListener('change', drawTraj); });
    ['tj-R', 'tj-r'].forEach(function (id) { $(id).addEventListener('input', function () { $(id + 'l').textContent = $(id).value + ' µm'; }); });
    drawTraj();
  }

  // ------------------------------------------------------------ panel 3: lucky drops (exact stochastic runs)
  var lk = $('luck');
  if (lk) {
    var ST = DATA.stoch;
    function drawCDF(extra) {
      var cols = { 10: '#3c6a46', 100: '#33627f', 1000: '#7d1d2f' }, s = [];
      [10, 100, 1000].forEach(function (V) {
        var t = ST.t100[V].slice().sort(function (a, b) { return a - b; }), n = ST.n[V];
        s.push({ x: [0].concat(t.map(function (x) { return x / 60; })), y: [0].concat(t.map(function (x, i) { return (i + 1) / n; })), label: V + ' cm³: ' + n + ' exact runs', color: cols[V], width: 2 });
        var br = DATA.bridge, Vm = V * 1e-6;
        var mx = 0;   // (6.1) with the largest n100 so far: a volume that once held a 100 um drop has had its first drop (figure 6.1)
        s.push({ x: minutes(br.t), y: br.N100.map(function (n100) { mx = Math.max(mx, n100); return 1 - Math.exp(-Vm * mx); }), color: cols[V], dash: '4 3', width: 1.5 });
      });
      $('lk-cdf').innerHTML = CHART.line({ w: 620, h: 300, xmin: 0, xmax: 20, ymin: 0, ymax: 1, series: s.concat(extra || []), xlabel: 'time (min)',
        ylabel: 'share of volumes with a 100 µm drop', id: 'lkc' });
    }
    drawCDF();
    $('lk-run').addEventListener('click', function () {
      var V = +$('lk-V').value, seed = 1 + Math.floor(Math.random() * 1e9), u = PHYS.rng(seed);
      var radii = PHYS.drawModes(MODES, V, u, 3);
      $('lk-status').textContent = 'running ' + radii.length + ' drops…';
      setTimeout(function () {
        var r = PHYS.gillespieRun(V, radii, A, { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab: DATA.etab_warm }, { u: u, seed: seed, tEnd: 1800, recordEvery: 10 });
        var t100 = r.firsts[100e-6];
        $('lk-status').textContent = 'done';
        var nb = r['bigMerges' + 100e-6];
        $('lk-out').innerHTML = V + ' cm³ (' + radii.length + ' drops, seed ' + seed + '): ' + r.events + ' mergers in 30 min; ' +
          (t100 !== undefined ? 'the first 100 µm drop appeared at <b>' + (t100 / 60).toFixed(1) + ' min</b>, after ' + nb + (nb === 1 ? ' merger' : ' mergers') + ' with drops of 30 µm or more'
            : '<b>no drop reached 100 µm</b> within 30 min');
        $('lk-rmax').innerHTML = CHART.line({ w: 620, h: 260, xmin: 0, xmax: 30, ymin: 30, ymax: 160, series: [
          { x: minutes(r.t), y: r.rmax.map(function (x) { return x * 1e6; }), label: 'largest drop in your volume', color: '#7d1d2f', width: 2.5 }],
          hlines: [{ y: 100, label: '100 µm' }], xlabel: 'time (min)', ylabel: 'radius (µm)', id: 'lkr' });
      }, 20);
    });
  }

  // ------------------------------------------------------------ panel 4: a cloud with a shape (fall + mean motion + stochastic element)
  var sh = $('shape');
  if (sh) {
    var cv = $('sh-cv'), ctx = cv.getContext('2d'), CW = cv.width, CH = cv.height, PADB = 20, cloud = null, timer = null, probe = null, lastText = 0;
    var KO = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab: DATA.etab_warm };
    var sx = function (x) { return x / 2000 * CW; }, sz = function (z) { return (CH - PADB) - z / 1500 * (CH - PADB); };
    function newCloud() {
      cloud = PHYS.makeCloud(A, KO, { shape: $('sh-shape').value, W0: +$('sh-wind').value, stochastic: $('sh-stoch').value === 'on', eps: +$('sh-eps').value,
        perCell: [24, 8], seed: 1 + Math.floor(Math.random() * 1e9) });
      bg = null; draw(); text(true);
    }
    var bg = null;
    function background() {     // the shape, the ground and the mean motion's arrows, drawn once per cloud
      var c = document.createElement('canvas'); c.width = CW; c.height = CH; var g = c.getContext('2d'), i, j, v = [0, 0];
      g.fillStyle = '#f4f8fa'; g.fillRect(0, 0, CW, CH);
      g.fillStyle = '#e1ebf0';
      for (i = 0; i < 80; i++) for (j = 0; j < 60; j++) { var x = (i + 0.5) * 25, z = (j + 0.5) * 25; if (cloud.inside(x, z)) g.fillRect(sx(i * 25), sz((j + 1) * 25), sx(25) + 0.6, sz(0) - sz(25) + 0.6); }
      g.strokeStyle = 'rgba(51,98,127,0.35)'; g.lineWidth = 1;
      if (cloud.W0 > 0) for (i = 1; i < 10; i++) for (j = 1; j < 8; j++) {
        var X = i * 200, Z = j * 190; cloud.flow(X, Z, v); var L = 26 / Math.max(1e-9, cloud.W0), ex = sx(X) + v[0] * L, ez = sz(Z) - v[1] * L;
        g.beginPath(); g.moveTo(sx(X), sz(Z)); g.lineTo(ex, ez); g.stroke();
        var a = Math.atan2(ez - sz(Z), ex - sx(X)); g.beginPath(); g.moveTo(ex, ez); g.lineTo(ex - 5 * Math.cos(a - 0.4), ez - 5 * Math.sin(a - 0.4)); g.moveTo(ex, ez); g.lineTo(ex - 5 * Math.cos(a + 0.4), ez - 5 * Math.sin(a + 0.4)); g.stroke();
      }
      g.fillStyle = '#6f665e'; g.fillRect(0, CH - PADB, CW, 2);
      g.font = '11px "IBM Plex Mono", monospace'; g.fillText('ground: rain is counted here', 8, CH - 5);
      return c;
    }
    function draw() {
      if (!bg) bg = background();
      ctx.drawImage(bg, 0, 0);
      var s = cloud.sd, i;
      for (i = 0; i < s.length; i++) {
        var q = s[i], r = q.r;
        ctx.fillStyle = r >= 100e-6 ? '#7d1d2f' : r >= 20e-6 ? '#c9783f' : 'rgba(51,98,127,0.45)';
        var d = r >= 100e-6 ? 3.2 : r >= 20e-6 ? 2 : 1.2;
        ctx.fillRect(sx(q.x) - d / 2, sz(q.z) - d / 2, d, d);
      }
      if (probe) { ctx.strokeStyle = '#23160f'; ctx.lineWidth = 1.5; ctx.strokeRect(sx(probe.i * 50), sz((probe.j + 1) * 50), sx(50), sz(0) - sz(50)); }
      ctx.fillStyle = '#23160f'; ctx.font = '12px "IBM Plex Mono", monospace'; ctx.fillText('t = ' + (cloud.t / 60).toFixed(1) + ' min', 8, 16);
    }
    function text(force) {
      var now = performance.now(); if (!force && now - lastText < 250) return; lastText = now;   // words change about four times a second
      var z = cloud.census(), f = function (v) { return (100 * v / cloud.M0).toFixed(1) + ' %'; };
      $('sh-out').innerHTML = 'time <b>' + (cloud.t / 60).toFixed(1) + ' min</b><br>water still in the air ' + f(z.M) + ' (in drops ≥ 100 µm ' + f(z.M100) + ')<br>rained out ' + f(z.rain) +
        ' · evaporated in clear air ' + f(z.evap) + '<br>first drop of 100 µm: ' + (cloud.first100 ? (cloud.first100.t / 60).toFixed(1) + ' min at x = ' + cloud.first100.x.toFixed(0) + ' m, z = ' + cloud.first100.z.toFixed(0) + ' m' : 'not yet');
      if (probe) {
        var x = (probe.i + 0.5) * 50, zz = (probe.j + 0.5) * 50, v = [0, 0], e = cloud.epsAt(x, zz), s2 = cloud.sig2At(x, zz), n = 0, w = 0, rmax = 0;
        cloud.flow(x, zz, v);
        cloud.sd.forEach(function (q) { if (Math.floor(q.x / 50) === probe.i && Math.floor(q.z / 50) === probe.j) { n++; w += q.xi * PHYS.massOf(q.r); rmax = Math.max(rmax, q.r); } });
        $('sh-probe').innerHTML = 'probe at x = ' + x + ' m, z = ' + zz + ' m (' + (cloud.inside(x, zz) ? 'inside the cloud' : 'clear air') + ')<br>mean wind ' + v[0].toFixed(2) + ' / ' + v[1].toFixed(2) +
          ' m/s (across / up) · stochastic element σ = ' + (cloud.stochastic ? Math.sqrt(s2).toFixed(2) + ' m/s, memory T_L = ' + (2 * s2 / (6 * e)).toFixed(0) + ' s' : 'off') +
          '<br>super-droplets here ' + n + ' · water ' + (w / 125000 * 1e3).toFixed(3) + ' g/m³ · largest drop ' + (rmax * 1e6).toFixed(0) + ' µm';
      }
    }
    function loop() {
      cloud.step(1); cloud.step(1);
      draw(); text(false);
      if (cloud.t < 2700 && cloud.sd.length) timer = requestAnimationFrame(loop); else { timer = null; $('sh-go').textContent = 'Start'; $('sh-status').textContent = 'stopped at 45 min'; text(true); }
    }
    $('sh-go').addEventListener('click', function () {
      if (timer) { cancelAnimationFrame(timer); timer = null; $('sh-go').textContent = 'Start'; $('sh-status').textContent = 'paused'; text(true); return; }
      if (reduceMotion) { for (var k = 0; k < 60; k++) cloud.step(1); draw(); text(true); $('sh-status').textContent = 'advanced one minute (reduced motion)'; return; }
      $('sh-go').textContent = 'Pause'; $('sh-status').textContent = 'running'; timer = requestAnimationFrame(loop);
    });
    $('sh-reset').addEventListener('click', function () { if (timer) { cancelAnimationFrame(timer); timer = null; $('sh-go').textContent = 'Start'; } $('sh-status').textContent = ''; newCloud(); });
    ['sh-shape', 'sh-wind', 'sh-stoch', 'sh-eps'].forEach(function (id) { $(id).addEventListener('change', function () { $('sh-reset').click(); }); });
    cv.addEventListener('click', function (e) {
      var b = cv.getBoundingClientRect(), x = (e.clientX - b.left) / b.width * CW, y = (e.clientY - b.top) / b.height * CH;
      if (y > CH - PADB) return;
      probe = { i: Math.min(39, Math.floor(x / CW * 40)), j: Math.min(29, Math.floor((CH - PADB - y) / (CH - PADB) * 30)) };
      draw(); text(true);
    });
    $('sh-clear').addEventListener('click', function () { probe = null; $('sh-probe').textContent = 'No probe pinned.'; draw(); });
    newCloud();
  }

  // ------------------------------------------------------------ panel 5: one landscape, three rules
  var ru = $('rules');
  if (ru) {
    var marks = [1, 0.95, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01];
    function curve(radii, kind) {
      var a23 = function (r) { return Math.pow(PHYS.massOf(r), 2 / 3); }, S0 = 0, S, N0 = radii.length, xs = [0], ys = [1], mi = 1, dd = 0, cd = 0, n = 0, first = null;
      radii.forEach(function (r) { S0 += a23(r); }); S = S0;
      function ev(a, b, alive) {
        var R = Math.cbrt(a * a * a + b * b * b); S -= a23(a) + a23(b) - a23(R); n++;
        var big = Math.max(a, b), sm = Math.min(a, b); if (big < 20e-6) dd++; else if (sm < 20e-6) cd++;
        if (first === null && R >= 100e-6) first = n;
        while (mi < marks.length && (alive - 1) / N0 <= marks[mi]) { xs.push(1 - marks[mi]); ys.push(S / S0); mi++; }
      }
      if (kind === 'steepest') {
        var s = radii.slice().sort(function (p, q) { return q - p; }), bigR = s[0];
        for (var k = 1; k < s.length; k++) { ev(bigR, s[k], N0 - k + 1); bigR = Math.cbrt(bigR * bigR * bigR + s[k] * s[k] * s[k]); }
      } else {
        var u = PHYS.rng(1 + Math.floor(Math.random() * 1e9));
        PHYS.gillespieRun(10, radii, A, kind === 'constant' ? { constant: 1e-10 } : KO2, { u: u, tEnd: kind === 'constant' ? 1e12 : 3600, recordEvery: kind === 'constant' ? 1e12 : 3600, onEvent: function (a, b, t, alive) { ev(a, b, alive); } });
      }
      return { xs: xs, ys: ys, dd: dd, cd: cd, n: n, first: first, S: S / S0 };
    }
    var KO2 = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab: DATA.etab_warm };
    $('ru-run').addEventListener('click', function () {
      $('ru-status').textContent = 'merging…';
      setTimeout(function () {
        var u = PHYS.rng(1 + Math.floor(Math.random() * 1e9)), radii = PHYS.drawModes(MODES, 10, u, 3);
        var P1 = curve(radii, 'physical'), P2 = curve(radii, 'constant'), P3 = curve(radii, 'steepest');
        $('ru-plot').innerHTML = CHART.line({ w: 620, h: 310, xmin: 0, xmax: 1, ymin: 0, ymax: 1, xlabel: 'share of the drops merged away, 1 − N/N₀', ylabel: 'surface energy left / at start', id: 'rup', series: [
          { x: P1.xs, y: P1.ys, label: 'kernel of chapters 1–4 (one hour)', color: '#7d1d2f' }, { x: P2.xs, y: P2.ys, label: 'every pair alike (Metropolis)', color: '#33627f' },
          { x: P3.xs, y: P3.ys, label: 'largest pair first', color: '#3c6a46', dash: '5 4' }] });
        var pc = function (a, b) { return (100 * a / Math.max(1, b)).toFixed(2) + ' %'; };
        $('ru-out').innerHTML = radii.length + ' drops.<br>Kernel: ' + P1.n + ' mergers in an hour, droplet–droplet ' + pc(P1.dd, P1.n) + ', collector–droplet ' + pc(P1.cd, P1.n) + '; first 100 µm drop after ' + (P1.first || '–') + ' mergers.' +
          '<br>Every pair alike: droplet–droplet ' + pc(P2.dd, P2.n) + '; first 100 µm drop after ' + P2.first + ' mergers.<br>Largest pair first: first 100 µm drop after ' + P3.first + ' mergers.';
        $('ru-status').textContent = 'done';
      }, 20);
    });
  }

  route();
})();
