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
      $('bx-f40').innerHTML = CHART.line({ w: 620, h: 300, series: s, xmin: 0, xmax: 30, ymin: 0, ymax: 1, xlabel: 'time (min)', ylabel: 'water in drops r ≥ 40 µm', legendAt: 'bottom', id: 'bxf' });
    }
    function drawSpec(grid, N, t) {
      var x = grid.r.map(function (r) { return r * 1e6; });
      var g0 = PHYS.lognormalBins(grid, MODES).map(function (n, k) { return n * grid.x[k] / grid.dlnr * 1e3; });
      var g = N.map(function (n, k) { return n * grid.x[k] / grid.dlnr * 1e3; });
      $('bx-spec').innerHTML = CHART.line({ w: 620, h: 280, xlog: true, xmin: 2, xmax: 4000, ymin: 0, series: [
        { x: x, y: g0, label: 'start', color: '#6f665e', dash: '4 3' }, { x: x, y: g, label: 'after ' + Math.round(t / 60) + ' min', color: '#7d1d2f' }],
        xlabel: 'radius r (µm)', ylabel: 'g = dM/d ln r (g/m³)', legendAt: 'right', id: 'bxs' });
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
      var W = 520, H = 420, sc = 70, cx = W / 2, cz = H * 0.42, parts = ['<svg viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="droplet paths around a collector">',
        '<rect width="' + W + '" height="' + H + '" fill="#fff"/>'];
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
      parts.push('<text x="12" y="20" class="tick">air rises past the collector (its frame); droplets enter from below</text>');
      parts.push('<text x="12" y="' + (H - 12) + '" class="tick">wine: touches · blue: carried round · dashed: contact at R + r</text></svg>');
      $('tj-svg').innerHTML = parts.join('');
      $('tj-out').innerHTML = 'Stokes number St = τU/R = <b>' + St.toFixed(2) + '</b> · settling ratio S = <b>' + S.toFixed(3) + '</b> · collector Re = <b>' + Re.toFixed(2) +
        '</b><br>E (creeping flow) = <b>' + e.ES.toFixed(3) + '</b> · E (potential flow) = <b>' + e.EP.toFixed(3) + '</b> · E (Langmuir’s blend) = <b>' + e.E.toFixed(3) + '</b>';
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
        s.push({ x: minutes(br.t), y: br.N100.map(function (n100) { return 1 - Math.exp(-Vm * n100); }), color: cols[V], dash: '4 3', width: 1.5 });
      });
      $('lk-cdf').innerHTML = CHART.line({ w: 620, h: 300, xmin: 0, xmax: 20, ymin: 0, ymax: 1, series: s.concat(extra || []), xlabel: 'time (min)',
        ylabel: 'share of volumes with a 100 µm drop', legendAt: 'right', id: 'lkc' });
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
        $('lk-out').innerHTML = V + ' cm³ (' + radii.length + ' drops, seed ' + seed + '): ' + r.events + ' mergers in 30 min; first drop of 100 µm at <b>' +
          (t100 !== undefined ? (t100 / 60).toFixed(1) + ' min</b>, grown through ' + nb + ' merger(s) with drops of 30 µm or more' : 'none within 30 min</b>');
        $('lk-rmax').innerHTML = CHART.line({ w: 620, h: 260, xmin: 0, xmax: 30, ymin: 30, ymax: 160, series: [
          { x: minutes(r.t), y: r.rmax.map(function (x) { return x * 1e6; }), label: 'largest drop in your volume', color: '#7d1d2f', width: 2.5 }],
          hlines: [{ y: 100, label: '100 µm' }], xlabel: 'time (min)', ylabel: 'radius (µm)', legendAt: 'bottom', id: 'lkr' });
      }, 20);
    });
  }

  route();
})();
