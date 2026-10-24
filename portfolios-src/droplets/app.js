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

  // ------------------------------------------------------------ the store
  // Panels 3 and 4 write every number they compute into one named store (the site's scripts/dataset.js), at the line that computes
  // it; the readouts on this page and the data panel (datahooks.js with scripts/datalog.js) only read it. The standalone build has
  // no site scripts: there a bare stand-in with the same calls keeps the readouts working.
  var ds = window.Sim && Sim.dataset ? Sim.dataset({ title: 'A cloud with a shape', attrs: { study: 'Droplet Collection', panels: 'panel 4, a cloud with a shape; panel 3, lucky drops' } }) : (function () {
    var v = {}, dims = {};
    return { dims: dims, vars: v, dim: function (n, z) { dims[n] = z; return z; }, var: function (n, d, ty, at) {
        var x = v[n] = v[n] || { dims: d, type: ty, attrs: at || {} }, z = 1; d.forEach(function (k) { z *= dims[k] || 0; }); if (d.length && (!x.data || x.data.length !== z)) x.data = new ty(z); return x; },
      set: function (n, x) { v[n].data = x; return x; }, get: function (n) { return v[n] && v[n].data; }, touch: function () {}, has: function (n) { return !!v[n]; } };
  })();
  if (window.Sim) Sim.cloudStore = ds;
  function S(name, value) { return ds.set(name, value); }
  function def(list) { list.forEach(function (d) { ds.var(d[0], d[1], d[2], d[3]); }); }
  function sc(sym, name, units, digits, how, more) { var a = { symbol: sym, long_name: name, units: units, digits: digits, computed_in: how }; for (var k in more || {}) a[k] = more[k]; return a; }
  def([
    ['T_air', [], 'float', sc('T', 'air temperature', 'K', 2, 'set by the page', { source: 'PHYS.air(283.15, 85000) at the top of app.js' })],
    ['p_air', [], 'float', sc('p', 'air pressure', 'Pa', 0, 'set by the page', { source: 'PHYS.air(283.15, 85000)' })],
    ['rho_air', [], 'float', sc('ρ<sub>a</sub>', 'density of the air', 'kg/m³', 4, 'PHYS.air', { formula: 'ρ<sub>a</sub> = p / (R<sub>d</sub> T)' })],
    ['mu_air', [], 'float', sc('μ', 'viscosity of the air', 'µPa·s', 4, 'PHYS.air', { formula: 'Sutherland: μ = 17.2 µPa·s (T/273)<sup>3/2</sup> (393 K)/(T + 120 K)' })],
    ['N1', [], 'float', sc('N<sub>1</sub>', 'droplet mode: number per cubic metre', 'm⁻³', 0, 'MODES, set by the page')],
    ['rg1', [], 'float', sc('r<sub>g1</sub>', 'droplet mode: median radius', 'µm', 1, 'MODES')],
    ['sg1', [], 'float', sc('σ<sub>g1</sub>', 'droplet mode: geometric spread', '', 2, 'MODES')],
    ['N2', [], 'float', sc('N<sub>2</sub>', 'collector mode: number per cubic metre', 'm⁻³', 0, 'MODES')],
    ['rg2', [], 'float', sc('r<sub>g2</sub>', 'collector mode: median radius', 'µm', 1, 'MODES')],
    ['sg2', [], 'float', sc('σ<sub>g2</sub>', 'collector mode: geometric spread', '', 2, 'MODES')]
  ]);
  S('T_air', A.T); S('p_air', A.p); S('rho_air', A.rho); S('mu_air', A.mu * 1e6);
  S('N1', MODES[0].N); S('rg1', MODES[0].rg * 1e6); S('sg1', MODES[0].sg); S('N2', MODES[1].N); S('rg2', MODES[1].rg * 1e6); S('sg2', MODES[1].sg);
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
    // the stored exact runs as an ensemble: for each volume the times of the first 100 µm drop, and their spread, written once here
    function quant(sorted, q) { if (!sorted.length) return NaN; var x = q * (sorted.length - 1), i = Math.floor(x), f = x - i; return i + 1 < sorted.length ? sorted[i] + f * (sorted[i + 1] - sorted[i]) : sorted[i]; }
    Object.keys(ST.n).forEach(function (V) {
      var t = ST.t100[V].slice().sort(function (a, b) { return a - b; }), n = ST.n[V], k = t.length, mean = 0, sd = 0;
      ds.dim('run_' + V, k);
      ds.var('t100_' + V, ['run_' + V], Float64Array, sc('t<sub>100</sub>', 'first 100 µm drop in each stored run of ' + V + ' cm³ that had one, sorted', 'min', 2, 'data/stochastic.json', { source: 'read from the stored exact runs (tools/run_stochastic.cjs)' })).data.set(t.map(function (x) { return x / 60; }));
      t.forEach(function (x) { mean += x / 60 / k; }); t.forEach(function (x) { sd += Math.pow(x / 60 - mean, 2) / Math.max(1, k - 1); }); sd = Math.sqrt(sd);
      def([
        ['ens_n_' + V, [], 'int', sc('n<sub>runs</sub>', 'stored exact runs of ' + V + ' cm³', '', 0, 'data/stochastic.json')],
        ['ens_hit_' + V, [], 'float', sc('P<sub>60</sub>', 'share of those runs with a 100 µm drop within their 60 min', '%', 1, 'app.js, ensemble', { formula: 'P<sub>60</sub> = 100 · (runs with t<sub>100</sub>) / n<sub>runs</sub>' })],
        ['ens_mean_' + V, [], 'float', sc('⟨t<sub>100</sub>⟩', 'mean time of the first 100 µm drop, over the runs that had one', 'min', 2, 'app.js, ensemble', { formula: '⟨t<sub>100</sub>⟩ = Σ t<sub>100</sub> / n' })],
        ['ens_sd_' + V, [], 'float', sc('s<sub>t</sub>', 'spread: standard deviation of t<sub>100</sub> between runs', 'min', 2, 'app.js, ensemble', { formula: 's<sub>t</sub> = √(Σ (t<sub>100</sub> − ⟨t<sub>100</sub>⟩)² / (n − 1))' })],
        ['ens_p10_' + V, [], 'float', sc('t<sub>100</sub><sup>10 %</sup>', 'the luckiest tenth of the runs had its first 100 µm drop by', 'min', 2, 'app.js, ensemble', { formula: 'linear interpolation in the sorted t<sub>100</sub> at (n − 1)·0.1' })],
        ['ens_p50_' + V, [], 'float', sc('t<sub>100</sub><sup>50 %</sup>', 'median time of the first 100 µm drop', 'min', 2, 'app.js, ensemble', { formula: 'linear interpolation in the sorted t<sub>100</sub> at (n − 1)·0.5' })],
        ['ens_p90_' + V, [], 'float', sc('t<sub>100</sub><sup>90 %</sup>', 'nine tenths of the runs with a drizzle drop had it by', 'min', 2, 'app.js, ensemble', { formula: 'linear interpolation in the sorted t<sub>100</sub> at (n − 1)·0.9' })]
      ]);
      S('ens_n_' + V, n); S('ens_hit_' + V, 100 * k / n); S('ens_mean_' + V, k ? mean : NaN); S('ens_sd_' + V, k > 1 ? sd : NaN);
      S('ens_p10_' + V, quant(t, 0.1) / 60); S('ens_p50_' + V, quant(t, 0.5) / 60); S('ens_p90_' + V, quant(t, 0.9) / 60);
    });
    def([
      ['lk_V', [], 'int', sc('V', 'volume of your exact run', 'cm³', 0, 'the Volume menu of panel 3')],
      ['lk_seed', [], 'int', sc('seed', 'seed of your run’s random numbers', '', 0, 'drawn when you pressed Run')],
      ['lk_drops', [], 'int', sc('N<sub>0</sub>', 'drops drawn into your volume', '', 0, 'PHYS.drawModes')],
      ['lk_events', [], 'int', sc('n<sub>merge</sub>', 'mergers in your 30 minutes', '', 0, 'PHYS.gillespieRun')],
      ['lk_t100', [], 'float', sc('t<sub>100</sub>', 'your first 100 µm drop (empty: none in 30 min)', 'min', 2, 'PHYS.gillespieRun')],
      ['lk_big', [], 'int', sc('n<sub>big</sub>', 'mergers with drops of 30 µm or more before it', '', 0, 'PHYS.gillespieRun')],
      ['lk_rank', [], 'float', sc('rank', 'share of the stored runs of this volume that were luckier (an earlier first drizzle drop)', '%', 1, 'app.js, after your run', { formula: '100 · (stored runs with t<sub>100</sub> &lt; yours) / n<sub>runs</sub>; without a drop of yours in 30 min, the runs that had one by 30 min' })]
    ]);
    ['lk_V', 'lk_seed', 'lk_drops', 'lk_events', 'lk_t100', 'lk_big', 'lk_rank'].forEach(function (k) { S(k, NaN); });   // empty until you run a volume
    ds.dim('lk_n', 0);
    ds.var('lk_t', ['lk_n'], Float64Array, sc('t', 'time of each sample of your run', 'min', 2, 'PHYS.gillespieRun, every 10 s'));
    ds.var('lk_rmax', ['lk_n'], Float64Array, sc('r<sub>max</sub>', 'largest drop in your volume', 'µm', 1, 'PHYS.gillespieRun, every 10 s'));
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
        S('lk_V', V); S('lk_seed', seed); S('lk_drops', radii.length); S('lk_events', r.events); S('lk_t100', t100 !== undefined ? t100 / 60 : NaN); S('lk_big', t100 !== undefined ? nb : NaN);
        var stored = ST.t100[V] || [], earlier = stored.filter(function (x) { return x < (t100 === undefined ? 1800 : t100); }).length;   // your run lasts 30 min, the stored ones 60
        S('lk_rank', ST.n[V] ? 100 * earlier / ST.n[V] : NaN);
        ds.dim('lk_n', r.t.length); ds.var('lk_t', ['lk_n'], Float64Array).data.set(minutes(r.t)); ds.var('lk_rmax', ['lk_n'], Float64Array).data.set(r.rmax.map(function (x) { return x * 1e6; }));
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
    var cv = $('sh-cv'), ctx = cv.getContext('2d'), cloud = null, timer = null, probe = null, lastText = 0, bg = null, follow = null, trail = [];
    var CW = 600, CH = 450, dpr = 1;
    var KO = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab: DATA.etab_warm };
    var sx = function (x) { return x / 2000 * CW; }, sz = function (z) { return CH - z / 1500 * CH; };
    var steps = 0, KOtext = 'Beard fall speed, efficiency table, coalescence law, nearly equal pairs clamped at r/R = 0.6';
    // the store's variables for this panel, declared once; their values are written where they are computed, below
    var ET = DATA.etab_warm;
    ds.dim('eR', ET.lnR.length); ds.dim('ep', ET.lnp.length);
    ds.var('etab_lnR', ['eR'], Float64Array, sc('ln R', 'collector radius of each table row, as ln(R / 1 m)', '', 4, 'data/etab_warm.json', { coordinate: true, source: 'read from the stored efficiency table (tools/gen_tables.cjs)' })).data.set(ET.lnR);
    ds.var('etab_lnp', ['ep'], Float64Array, sc('ln p', 'size ratio p = r/R of each table column, as ln p', '', 4, 'data/etab_warm.json', { coordinate: true })).data.set(ET.lnp);
    ds.var('etab', ['eR', 'ep'], Float64Array, sc('E', 'collision efficiency E(R, p) from the droplet trajectories, the table the kernel reads', '', 4, 'data/etab_warm.json', { source: 'read from the stored efficiency table (tools/gen_tables.cjs)' })).data.set(ET.E);
    def([
      ['shape', [], 'str', sc('outline', 'cloud outline', '', 0, 'the Cloud outline menu')],
      ['W0', [], 'float', sc('W<sub>0</sub>', 'peak updraft of the mean motion', 'm/s', 2, 'the Mean motion menu')],
      ['stochastic', [], 'bool', sc('eddies', 'stochastic element (eddies) on', '', 0, 'the Stochastic element menu')],
      ['Le', [], 'float', sc('L<sub>e</sub>', 'size of the largest eddy', 'm', 0, 'the Largest eddy menu')],
      ['per_frame', [], 'int', sc('n<sub>f</sub>', 'model steps of 1 s drawn per frame', '', 0, 'the Speed menu')],
      ['seed', [], 'int', sc('seed', 'seed of the cloud’s random numbers (outline, drops, eddies, mergers)', '', 0, 'drawn when the cloud is made')],
      ['kernel', [], 'str', sc('K', 'how the collision kernel is built', '', 0, 'set by the page (KO)')],
      ['Lx', [], 'float', sc('L<sub>x</sub>', 'width of the slice', 'm', 0, 'PHYS.makeCloud')],
      ['Lz', [], 'float', sc('L<sub>z</sub>', 'height of the slice', 'm', 0, 'PHYS.makeCloud')],
      ['h', [], 'float', sc('h', 'side of a collision cell', 'm', 0, 'PHYS.makeCloud')],
      ['per1', [], 'int', sc('n<sub>1</sub>', 'super-droplets per cell for the droplet mode', '', 0, 'set by the page (perCell)')],
      ['per2', [], 'int', sc('n<sub>2</sub>', 'super-droplets per cell for the collector mode', '', 0, 'set by the page (perCell)')],
      ['S_out', [], 'float', sc('S', 'supersaturation of the clear air outside the outline (negative: drops evaporate)', '', 2, 'PHYS.makeCloud')],
      ['eps', [], 'float', sc('ε', 'dissipation rate of the eddies', 'm²/s³', 4, 'PHYS.makeCloud')],
      ['C0', [], 'float', sc('C<sub>0</sub>', 'Lagrangian structure-function constant', '', 0, 'PHYS.makeCloud (fixed at 6)')],
      ['dt', [], 'float', sc('Δt', 'model time step', 's', 0, 'cloud.step(1)')],
      ['dV', [], 'float', sc('ΔV', 'volume of one collision cell, h³', 'm³', 0, 'PHYS.makeCloud', { formula: 'ΔV = h³' })],
      ['xi1', [], 'float', sc('ξ<sub>1</sub>', 'real drops one droplet super-droplet stands for', '', 0, 'PHYS.makeCloud', { formula: 'ξ<sub>1</sub> = N<sub>1</sub> ΔV / n<sub>1</sub>' })],
      ['xi2', [], 'float', sc('ξ<sub>2</sub>', 'real drops one collector super-droplet stands for', '', 0, 'PHYS.makeCloud', { formula: 'ξ<sub>2</sub> = N<sub>2</sub> ΔV / n<sub>2</sub>' })],
      ['sigma_u', [], 'float', sc('σ<sub>u</sub>', 'eddy speed, one component', 'm/s', 3, 'cloud.sig2At', { formula: 'σ<sub>u</sub> = (ε L<sub>e</sub>)<sup>1/3</sup>' })],
      ['T_L', [], 'float', sc('T<sub>L</sub>', 'memory of the eddies (Lagrangian time)', 's', 1, 'cloud.move', { formula: 'T<sub>L</sub> = 2σ<sub>u</sub>² / (C<sub>0</sub> ε)' })],
      ['G_grow', [], 'float', sc('G', 'growth constant of dr²/dt = 2 G S (heat and vapour diffusion)', 'µm²/s', 2, 'PHYS.growthG', { formula: 'G = 1 / (F<sub>k</sub> + F<sub>d</sub>), Rogers and Yau 7.17' })],
      ['v10', [], 'float', sc('v(10 µm)', 'fall speed of a 10 µm droplet', 'cm/s', 3, 'PHYS.vBeard', { formula: 'Beard (1976), Stokes regime with slip' })],
      ['v20', [], 'float', sc('v(20 µm)', 'fall speed of a 20 µm drop', 'cm/s', 3, 'PHYS.vBeard')],
      ['v40', [], 'float', sc('v(40 µm)', 'fall speed of a 40 µm collector', 'cm/s', 3, 'PHYS.vBeard')],
      ['v100', [], 'float', sc('v(100 µm)', 'fall speed of a 100 µm drizzle drop', 'cm/s', 3, 'PHYS.vBeard', { formula: 'Beard (1976), second regime' })],
      ['E_40_10', [], 'float', sc('E(40, 10)', 'collision efficiency, 40 µm collector and 10 µm droplet', '', 4, 'PHYS.tableE', { formula: 'bilinear in ln R and ln p in the table E' })],
      ['E_100_20', [], 'float', sc('E(100, 20)', 'collision efficiency, 100 µm collector and 20 µm drop', '', 4, 'PHYS.tableE')],
      ['K_40_10', [], 'float', sc('K(40, 10)', 'collision kernel for that pair: volume swept per second', 'cm³/s', 6, 'PHYS.kernel', { formula: 'K = π (R + r)² |v<sub>R</sub> − v<sub>r</sub>| E E<sub>c</sub>' })],
      ['zbase', [], 'float', sc('z<sub>base</sub>', 'height of the cloud base', 'm', 0, 'PHYS.makeCloud')],
      ['n_sd0', [], 'int', sc('n<sub>sd,0</sub>', 'super-droplets at the start', '', 0, 'PHYS.makeCloud')],
      ['M0', [], 'float', sc('M<sub>0</sub>', 'water in the slice at the start', 'kg', 3, 'PHYS.makeCloud', { formula: 'M<sub>0</sub> = Σ ξ<sub>i</sub> (4/3) π ρ<sub>w</sub> r<sub>i</sub>³ at t = 0' })],
      ['N0', [], 'float', sc('N<sub>0</sub>', 'real drops in the slice at the start', '', 0, 'PHYS.makeCloud', { formula: 'N<sub>0</sub> = Σ ξ<sub>i</sub> at t = 0' })],
      ['t', [], 'float', sc('t', 'cloud time', 's', 0, 'cloud.step')],
      ['t_min', [], 'float', sc('t', 'cloud time in minutes', 'min', 2, 'record()', { formula: 't / 60' })],
      ['n_sd', [], 'int', sc('n<sub>sd</sub>', 'super-droplets still in the air', '', 0, 'record()')],
      ['N_air', [], 'float', sc('N', 'real drops still in the air', '', 0, 'record()', { formula: 'N = Σ ξ<sub>i</sub>' })],
      ['M_air', [], 'float', sc('M', 'water still in the air', 'kg', 3, 'cloud.census', { formula: 'M = Σ ξ<sub>i</sub> (4/3) π ρ<sub>w</sub> r<sub>i</sub>³' })],
      ['M40', [], 'float', sc('M<sub>40</sub>', 'water in drops of 40 µm or more', 'kg', 3, 'cloud.census')],
      ['M100', [], 'float', sc('M<sub>100</sub>', 'water in drizzle drops, 100 µm or more', 'kg', 3, 'cloud.census')],
      ['M_in', [], 'float', sc('M<sub>in</sub>', 'water inside the outline', 'kg', 3, 'cloud.census')],
      ['F_air', [], 'float', sc('f<sub>air</sub>', 'share of the water still in the air', '%', 2, 'record()', { formula: '100 M / M<sub>0</sub>' })],
      ['F100', [], 'float', sc('f<sub>100</sub>', 'share of the water in drizzle drops (100 µm or more)', '%', 2, 'record()', { formula: '100 M<sub>100</sub> / M<sub>0</sub>' })],
      ['F_rain', [], 'float', sc('f<sub>rain</sub>', 'share of the water rained out', '%', 2, 'record()', { formula: '100 M<sub>rain</sub> / M<sub>0</sub>' })],
      ['F_evap', [], 'float', sc('f<sub>evap</sub>', 'share of the water evaporated', '%', 2, 'record()', { formula: '100 M<sub>evap</sub> / M<sub>0</sub>' })],
      ['F_evap_below', [], 'float', sc('f<sub>evap, base</sub>', 'share evaporated below the cloud base', '%', 2, 'record()', { formula: '100 M<sub>evap, base</sub> / M<sub>0</sub>' })],
      ['rain', [], 'float', sc('M<sub>rain</sub>', 'water that reached the ground', 'kg', 3, 'cloud.step', { source: 'added up step by step as drops cross z = 0; the water book checks it' })],
      ['evap', [], 'float', sc('M<sub>evap</sub>', 'water evaporated outside the outline', 'kg', 3, 'cloud.step', { source: 'added up step by step from dr²/dt = 2 G S f<sub>v</sub>; the water book checks it' })],
      ['evap_below', [], 'float', sc('M<sub>evap, base</sub>', 'of it, below the cloud base', 'kg', 3, 'cloud.step')],
      ['N_rain', [], 'float', sc('N<sub>rain</sub>', 'drops that reached the ground', '', 0, 'cloud.step', { source: 'added up step by step; the number book checks it' })],
      ['N_evap', [], 'float', sc('N<sub>evap</sub>', 'drops that evaporated completely', '', 0, 'cloud.step', { source: 'added up step by step; the number book checks it' })],
      ['mergers', [], 'float', sc('N<sub>merge</sub>', 'drops lost to mergers (two become one)', '', 0, 'cloud.step', { source: 'added up step by step: each merger event removes ξ drops; the number book checks it' })],
      ['r_max', [], 'float', sc('r<sub>max</sub>', 'largest drop in the air', 'µm', 1, 'record()', { formula: 'max r<sub>i</sub>' })],
      ['t100_first', [], 'float', sc('t<sub>100</sub>', 'first drizzle drop (100 µm) in the slice (empty: not yet)', 'min', 2, 'cloud.step')],
      ['x100', [], 'float', sc('x<sub>100</sub>', 'where it formed, across', 'm', 0, 'cloud.step')],
      ['z100', [], 'float', sc('z<sub>100</sub>', 'where it formed, height', 'm', 0, 'cloud.step')],
      ['follow_id', [], 'int', sc('id<sub>f</sub>', 'super-droplet followed (−1: none)', '', 0, 'Follow one drop')],
      ['follow_r', [], 'float', sc('r<sub>f</sub>', 'radius of the followed drop', 'µm', 1, 'record()')],
      ['follow_z', [], 'float', sc('z<sub>f</sub>', 'height of the followed drop', 'm', 0, 'record()')],
      ['book_M_res', [], 'float', sc('δM', 'water book: M<sub>0</sub> − M − M<sub>rain</sub> − M<sub>evap</sub>', 'kg', 9, 'record()', { formula: 'δM = M<sub>0</sub> − M − M<sub>rain</sub> − M<sub>evap</sub>' })],
      ['book_M_rel', [], 'float', sc('δM/M<sub>0</sub>', 'water book, relative residual (tolerance 10⁻⁹)', '', 15, 'record()')],
      ['book_N_res', [], 'float', sc('δN', 'number book: N<sub>0</sub> − N − N<sub>rain</sub> − N<sub>evap</sub> − N<sub>merge</sub>', '', 0, 'record()', { formula: 'δN = N<sub>0</sub> − N − N<sub>rain</sub> − N<sub>evap</sub> − N<sub>merge</sub>' })],
      ['book_N_rel', [], 'float', sc('δN/N<sub>0</sub>', 'number book, relative residual (tolerance 10⁻¹²)', '', 15, 'record()')],
      ['steps', [], 'int', sc('n<sub>step</sub>', 'model steps done for this cloud', '', 0, 'advance()')],
      ['step_ms', [], 'float', sc('τ<sub>step</sub>', 'wall time of the last frame’s steps', 'ms', 1, 'advance()')],
      ['gam_events', [], 'int', sc('n<sub>γ</sub>', 'merger events between super-droplet pairs', '', 0, 'cloud.step')],
      ['gam_many', [], 'int', sc('n<sub>γ&gt;1</sub>', 'events in which one drop swallowed several (γ &gt; 1)', '', 0, 'cloud.step')],
      ['running', [], 'bool', sc('running', 'the cloud is advancing', '', 0, 'Start / Pause')],
      ['W_px', [], 'float', sc('W', 'width of the picture', 'px', 0, 'size()')],
      ['H_px', [], 'float', sc('H', 'height of the picture', 'px', 0, 'size()')],
      ['dpr', [], 'float', sc('dpr', 'device pixels per css pixel', '', 2, 'size()')],
      ['px_per_m', [], 'float', sc('s', 'scale: css pixels per metre', 'px/m', 4, 'size()', { formula: 's = W / L<sub>x</sub>' })],
      ['probe_i', [], 'int', sc('i<sub>p</sub>', 'column of the probe pinned by a click (−1: none)', '', 0, 'click on the picture')],
      ['probe_j', [], 'int', sc('j<sub>p</sub>', 'row of the probe pinned by a click (−1: none)', '', 0, 'click on the picture')],
      ['probe_u', [], 'float', sc('u<sub>p</sub>', 'mean wind across at the probe', 'm/s', 2, 'cloud.flow')],
      ['probe_w', [], 'float', sc('w<sub>p</sub>', 'mean wind up at the probe', 'm/s', 2, 'cloud.flow')],
      ['probe_reg', [], 'int', sc('region', 'region at the probe: 0 core, 1 flank, 2 edge band, 3 clear air, 4 below the base', '', 0, 'cloud.regionAt')]
    ]);
    ds.dim('sd', 0);
    [['sd_x', Float64Array, sc('x', 'position across', 'm', 1, 'cloud.step')], ['sd_z', Float64Array, sc('z', 'height', 'm', 1, 'cloud.step')],
      ['sd_r', Float64Array, sc('r', 'radius', 'µm', 2, 'cloud.step')], ['sd_xi', Float64Array, sc('ξ', 'real drops the super-droplet stands for (its multiplicity)', '', 0, 'cloud.step')],
      ['sd_id', Int32Array, sc('id', 'the super-droplet’s number, fixed for its life', '', 0, 'PHYS.makeCloud')],
      ['sd_cls', Uint8Array, sc('class', '0 droplet (below 20 µm), 1 collector, 2 drizzle (100 µm or more)', '', 0, 'record()', { formula: '0 if r &lt; 20 µm, 1 if r &lt; 100 µm, else 2' })]
    ].forEach(function (d) { ds.var(d[0], ['sd'], d[1], d[2]); });
    ds.dim('cz', 30); ds.dim('cx', 40);
    ds.var('cell_lwc', ['cz', 'cx'], Float64Array, sc('LWC', 'water per cubic metre in each 50 m cell (row 0 at the ground)', 'g/m³', 3, 'record()', { formula: 'Σ<sub>cell</sub> ξ<sub>i</sub> (4/3) π ρ<sub>w</sub> r<sub>i</sub>³ / ΔV' }));
    ds.var('cell_n', ['cz', 'cx'], Int32Array, sc('n<sub>cell</sub>', 'super-droplets in each cell', '', 0, 'record()'));
    ds.var('cell_rmax', ['cz', 'cx'], Float64Array, sc('r<sub>max</sub>', 'largest drop in each cell', 'µm', 1, 'record()'));
    var CAP = 0, buf = {};
    // every frame (and when a cloud is made): the state copied out of the model's super-droplets, the census and the two books
    function record() {
      var s = cloud.sd, n = s.length, i, q, Nair = 0, rmax = 0, nx = cloud.nx, nz = cloud.nz, h = cloud.h, dV = h * h * h;
      if (n > CAP) { CAP = Math.max(n, 2 * CAP); ['sd_x', 'sd_z', 'sd_r', 'sd_xi'].forEach(function (k) { buf[k] = new Float64Array(CAP); }); buf.sd_id = new Int32Array(CAP); buf.sd_cls = new Uint8Array(CAP); }
      var X = buf.sd_x, Z = buf.sd_z, R = buf.sd_r, XI = buf.sd_xi, ID = buf.sd_id, CL = buf.sd_cls, lwc = ds.get('cell_lwc'), cn = ds.get('cell_n'), crm = ds.get('cell_rmax');
      lwc.fill(0); cn.fill(0); crm.fill(0);
      for (i = 0; i < n; i++) {
        q = s[i]; X[i] = q.x; Z[i] = q.z; R[i] = q.r * 1e6; XI[i] = q.xi; ID[i] = q.id; CL[i] = q.r >= 100e-6 ? 2 : q.r >= 20e-6 ? 1 : 0;
        Nair += q.xi; if (q.r > rmax) rmax = q.r;
        var c = Math.min(nz - 1, Math.max(0, Math.floor(q.z / h))) * nx + Math.min(nx - 1, Math.max(0, Math.floor(q.x / h)));
        cn[c]++; lwc[c] += q.xi * PHYS.massOf(q.r) / dV * 1e3; if (R[i] > crm[c]) crm[c] = R[i];
      }
      ds.dim('sd', n);
      ['sd_x', 'sd_z', 'sd_r', 'sd_xi', 'sd_id', 'sd_cls'].forEach(function (k) { S(k, buf[k].subarray(0, n)); });
      ds.touch('cell_lwc'); ds.touch('cell_n'); ds.touch('cell_rmax');
      var z = cloud.census(), M0 = cloud.M0, f = cloud.first100;
      S('t', cloud.t); S('t_min', cloud.t / 60); S('n_sd', n); S('N_air', Nair); S('M_air', z.M); S('M40', z.M40); S('M100', z.M100); S('M_in', z.Min);
      S('rain', z.rain); S('evap', z.evap); S('evap_below', z.evapBelow); S('N_rain', cloud.rainN); S('N_evap', cloud.evapN); S('mergers', cloud.mergers);
      S('F_air', 100 * z.M / M0); S('F100', 100 * z.M100 / M0); S('F_rain', 100 * z.rain / M0); S('F_evap', 100 * z.evap / M0); S('F_evap_below', 100 * z.evapBelow / M0);
      S('r_max', rmax * 1e6); S('t100_first', f ? f.t / 60 : NaN); S('x100', f ? f.x : NaN); S('z100', f ? f.z : NaN);
      S('follow_id', follow ? follow.q.id : -1); S('follow_r', follow && follow.alive ? follow.q.r * 1e6 : NaN); S('follow_z', follow && follow.alive ? follow.q.z : NaN);
      var dM = M0 - z.M - z.rain - z.evap, dN = cloud.N0 - Nair - cloud.rainN - cloud.evapN - cloud.mergers;
      S('book_M_res', dM); S('book_M_rel', dM / M0); S('book_N_res', dN); S('book_N_rel', dN / cloud.N0);
      S('steps', steps); S('gam_events', cloud.gamEvents); S('gam_many', cloud.gamMany);
    }
    function size() {    // draw at the displayed size times the device pixel ratio, so lines and dots stay sharp on a phone
      var w = Math.max(280, cv.closest('.plot').clientWidth - 12); dpr = window.devicePixelRatio || 1;
      CW = w; CH = Math.round(w * 0.75); cv.width = Math.round(CW * dpr); cv.height = Math.round(CH * dpr); cv.style.height = CH + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); bg = null;
      S('W_px', CW); S('H_px', CH); S('dpr', dpr); S('px_per_m', CW / 2000);
    }
    function newCloud() {
      var shape = $('sh-shape').value, seed = 1 + Math.floor(Math.random() * 1e9);
      cloud = PHYS.makeCloud(A, KO, { shape: shape, outline: { seed: seed, rough: 0.5 }, W0: +$('sh-wind').value, stochastic: $('sh-stoch').value === 'on', Le: +$('sh-le').value,
        perCell: [24, 8], seed: seed });
      bg = null; follow = null; trail = []; steps = 0;
      var e = cloud.epsAt(1000, 750), s2 = cloud.sig2At(1000, 750), dV = cloud.h * cloud.h * cloud.h;
      S('shape', shape); S('W0', cloud.W0); S('stochastic', cloud.stochastic); S('Le', cloud.Le); S('per_frame', +$('sh-speed').value); S('seed', seed); S('kernel', KOtext);
      S('Lx', cloud.Lx); S('Lz', cloud.Lz); S('h', cloud.h); S('per1', 24); S('per2', 8); S('S_out', cloud.S); S('eps', e); S('C0', 6); S('dt', 1);
      S('dV', dV); S('xi1', MODES[0].N * dV / 24); S('xi2', MODES[1].N * dV / 8); S('sigma_u', Math.sqrt(s2)); S('T_L', 2 * s2 / (6 * e)); S('G_grow', cloud.G * 1e12);
      S('v10', PHYS.vBeard(10e-6, A) * 100); S('v20', PHYS.vBeard(20e-6, A) * 100); S('v40', PHYS.vBeard(40e-6, A) * 100); S('v100', PHYS.vBeard(100e-6, A) * 100);
      S('E_40_10', PHYS.tableE(KO.tab, 40e-6, 0.25, KO.near)); S('E_100_20', PHYS.tableE(KO.tab, 100e-6, 0.2, KO.near)); S('K_40_10', PHYS.kernel(40e-6, 10e-6, A, KO) * 1e6);
      S('zbase', cloud.zbase); S('n_sd0', cloud.sd.length); S('M0', cloud.M0); S('N0', cloud.N0); S('running', !!timer); S('step_ms', NaN);
      pinProbe();
      if (ds.vars.reg) ds.set('reg', cloud.reg); else { ds.dim('rx', cloud.nxR); ds.dim('rz', cloud.nzR); ds.var('reg', ['rx', 'rz'], Int8Array, sc('region', 'region of each 25 m square: 0 updraft core, 1 flank, 2 edge band, 3 clear air, 4 below the base', '', 0, 'PHYS.makeCloud')); ds.set('reg', cloud.reg); }
      record(); draw(); text(true);
    }
    function background() {     // the outline, the ground and the mean motion's arrows (only where it blows), drawn once per cloud
      var c = document.createElement('canvas'); c.width = cv.width; c.height = cv.height; var g = c.getContext('2d'), i, j, v = [0, 0];
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.fillStyle = '#f4f8fa'; g.fillRect(0, 0, CW, CH);
      g.fillStyle = '#d6e4eb';
      for (i = 0; i < 100; i++) for (j = 0; j < 75; j++) { var x = (i + 0.5) * 20, z = (j + 0.5) * 20; if (cloud.inside(x, z)) g.fillRect(sx(i * 20), sz((j + 1) * 20), sx(20) + 0.6, sz(0) - sz(20) + 0.6); }
      g.strokeStyle = 'rgba(35,22,15,0.55)'; g.lineWidth = 1;
      if (cloud.W0 > 0) for (i = 1; i < 20; i++) for (j = 1; j < 15; j++) {
        var X = i * 100, Z = j * 100; cloud.flow(X, Z, v); var sp = Math.hypot(v[0], v[1]); if (sp < 0.05) continue;
        var L = 22 * sp / cloud.W0 * CW / 600, ex = sx(X) + v[0] / sp * L, ez = sz(Z) - v[1] / sp * L, a = Math.atan2(ez - sz(Z), ex - sx(X));
        g.beginPath(); g.moveTo(sx(X), sz(Z)); g.lineTo(ex, ez); g.lineTo(ex - 4 * Math.cos(a - 0.45), ez - 4 * Math.sin(a - 0.45)); g.moveTo(ex, ez); g.lineTo(ex - 4 * Math.cos(a + 0.45), ez - 4 * Math.sin(a + 0.45)); g.stroke();
      }
      g.fillStyle = '#6f665e'; g.fillRect(0, CH - 2, CW, 2);
      return c;
    }
    function draw() {
      if (!bg) bg = background();
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(bg, 0, 0); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var s = cloud.sd, i, k = CW / 600;
      for (i = 0; i < s.length; i++) {
        var q = s[i], r = q.r;
        ctx.fillStyle = r >= 100e-6 ? '#7d1d2f' : r >= 20e-6 ? '#c9783f' : 'rgba(51,98,127,0.55)';
        var d = Math.max(r >= 100e-6 ? 3.2 : r >= 20e-6 ? 2.2 : 2, (r >= 100e-6 ? 3.2 : r >= 20e-6 ? 2 : 1.4) * k);
        ctx.fillRect(sx(q.x) - d / 2, sz(q.z) - d / 2, d, d);
      }
      if (trail.length > 1) { ctx.strokeStyle = '#23160f'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(sx(trail[0][0]), sz(trail[0][1])); for (i = 1; i < trail.length; i++) ctx.lineTo(sx(trail[i][0]), sz(trail[i][1])); ctx.stroke();
        var e = trail[trail.length - 1]; ctx.beginPath(); ctx.arc(sx(e[0]), sz(e[1]), 4, 0, 2 * Math.PI); ctx.stroke(); }
      if (probe) { ctx.strokeStyle = '#23160f'; ctx.lineWidth = 1.5; ctx.strokeRect(sx(probe.i * 50), sz((probe.j + 1) * 50), sx(50), sz(0) - sz(50)); }
    }
    var REG = ['updraft core', 'flank', 'edge band (within 100 m of the outline)', 'clear air', 'below the base'];
    function pinProbe() {      // the probe's place and the mean motion there, written when it is pinned (and for each new cloud)
      var v = [NaN, NaN], x, zz;
      if (probe) { x = (probe.i + 0.5) * 50; zz = (probe.j + 0.5) * 50; cloud.flow(x, zz, v); }
      S('probe_i', probe ? probe.i : -1); S('probe_j', probe ? probe.j : -1); S('probe_u', v[0]); S('probe_w', v[1]); S('probe_reg', probe ? cloud.regionAt(x, zz) : -1);
    }
    function text(force) {      // the readouts only read the store
      var now = performance.now(); if (!force && now - lastText < 250) return; lastText = now;   // words change about four times a second
      var g = function (k) { return ds.get(k); }, f = function (v) { return v.toFixed(1) + ' %'; }, t1 = g('t100_first');
      $('sh-time').textContent = 't = ' + g('t_min').toFixed(1) + ' min';
      $('sh-out').innerHTML = 'water still in the air ' + f(g('F_air')) + ' (in drops ≥ 100 µm ' + f(g('F100')) + ')<br>rained out ' + f(g('F_rain')) +
        ' · evaporated ' + f(g('F_evap')) + ' (of which below the base ' + f(g('F_evap_below')) + ')<br>first drop of 100 µm: ' + (t1 === t1 ? t1.toFixed(1) + ' min at x = ' + g('x100').toFixed(0) + ' m, z = ' + g('z100').toFixed(0) + ' m' : 'not yet') +
        (follow ? '<br>followed drop: ' + (follow.alive ? g('follow_r').toFixed(1) + ' µm at z = ' + g('follow_z').toFixed(0) + ' m' : follow.end) : '');
      if (probe) {
        var c = probe.j * 40 + probe.i;
        $('sh-probe').innerHTML = 'probe at x = ' + (probe.i + 0.5) * 50 + ' m, z = ' + (probe.j + 0.5) * 50 + ' m: ' + REG[g('probe_reg')] + '<br>mean wind ' + g('probe_u').toFixed(2) + ' / ' + g('probe_w').toFixed(2) +
          ' m/s (across / up) · eddies σ = ' + (g('stochastic') ? g('sigma_u').toFixed(2) + ' m/s, memory T_L = ' + g('T_L').toFixed(0) + ' s' : 'off') +
          '<br>super-droplets here ' + g('cell_n')[c] + ' · water ' + g('cell_lwc')[c].toFixed(3) + ' g/m³ · largest drop ' + g('cell_rmax')[c].toFixed(0) + ' µm';
      }
    }
    function advance() {
      var per = +$('sh-speed').value, t0 = performance.now();
      for (var k = 0; k < per; k++) {
        cloud.step(1); steps++;
        if (follow && follow.alive) { if (cloud.sd.indexOf(follow.q) < 0) { follow.alive = false; follow.end = follow.q.z < 0.5 ? 'reached the ground as rain' : 'gone (evaporated or merged away)'; } else { trail.push([follow.q.x, follow.q.z]); if (trail.length > 900) trail.shift(); } }
      }
      S('per_frame', per); S('step_ms', performance.now() - t0); record();
    }
    function loop() {
      advance(); draw(); text(false);
      if (cloud.t < 2700 && cloud.sd.length) timer = requestAnimationFrame(loop); else { timer = null; S('running', false); $('sh-go').textContent = 'Start'; $('sh-status').textContent = 'stopped at 45 min'; text(true); }
    }
    $('sh-go').addEventListener('click', function () {
      if (timer) { cancelAnimationFrame(timer); timer = null; S('running', false); $('sh-go').textContent = 'Start'; $('sh-status').textContent = 'paused'; text(true); return; }
      if (reduceMotion) { for (var k = 0; k < 60; k++) { cloud.step(1); steps++; } record(); draw(); text(true); $('sh-status').textContent = 'advanced one minute (reduced motion)'; return; }
      $('sh-go').textContent = 'Pause'; $('sh-status').textContent = 'running'; timer = requestAnimationFrame(loop); S('running', true);
    });
    $('sh-follow').addEventListener('click', function () {     // follow a droplet that starts low in the updraft core
      var best = null, bd = 1e9;
      cloud.sd.forEach(function (q) { if (q.r < 20e-6 && cloud.regionAt(q.x, q.z) === 0) { var d = Math.abs(q.x - 1000) + Math.abs(q.z - 450); if (d < bd) { bd = d; best = q; } } });
      if (!best) best = cloud.sd[Math.floor(cloud.sd.length / 2)];
      follow = { q: best, alive: true }; trail = [[best.x, best.z]]; record(); draw(); text(true);
    });
    $('sh-reset').addEventListener('click', function () { if (timer) { cancelAnimationFrame(timer); timer = null; $('sh-go').textContent = 'Start'; } $('sh-status').textContent = ''; newCloud(); S('running', false); });
    ['sh-shape', 'sh-wind', 'sh-stoch', 'sh-le'].forEach(function (id) { $(id).addEventListener('change', function () { $('sh-reset').click(); }); });
    $('sh-speed').addEventListener('change', function () { S('per_frame', +$('sh-speed').value); });
    cv.addEventListener('click', function (e) {
      var b = cv.getBoundingClientRect(), x = (e.clientX - b.left) / b.width * 2000, z = (1 - (e.clientY - b.top) / b.height) * 1500;
      probe = { i: Math.min(39, Math.max(0, Math.floor(x / 50))), j: Math.min(29, Math.max(0, Math.floor(z / 50))) };
      pinProbe(); draw(); text(true);
    });
    $('sh-clear').addEventListener('click', function () { probe = null; pinProbe(); $('sh-probe').textContent = 'No probe pinned.'; draw(); });
    window.addEventListener('resize', function () { if (!cloud) return; size(); draw(); });
    // the page can reflow without a window resize (the data panel, when open, narrows the page): redraw when the plot's width changes
    if (window.ResizeObserver) new ResizeObserver(function () { if (cloud && Math.abs(cv.closest('.plot').clientWidth - 12 - CW) > 0.5) { size(); draw(); } }).observe(cv.closest('.plot'));
    size(); newCloud();
  }

  // ------------------------------------------------------------ panel 5: one landscape, three rules
  var ru = $('rules');
  if (ru) {
    var marks = [1, 0.95, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01];
    var KO2 = { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab: DATA.etab_warm };
    function curve(radii, kind, V) {
      var a23 = function (r) { return Math.pow(PHYS.massOf(r), 2 / 3); }, S0 = 0, S, N0 = radii.length, xs = [0], ys = [1], mi = 1, dd = 0, n = 0, first = null, half = null;
      var live = radii.slice();   // radii now, kept only to draw the spectrum when half the drops have merged
      radii.forEach(function (r) { S0 += a23(r); }); S = S0;
      function ev(a, b, alive) {
        var R = Math.cbrt(a * a * a + b * b * b); S -= a23(a) + a23(b) - a23(R); n++;
        if (Math.max(a, b) < 20e-6) dd++;
        if (first === null && R >= 100e-6) first = n;
        while (mi < marks.length && (alive - 1) / N0 <= marks[mi]) { xs.push(1 - marks[mi]); ys.push(S / S0); mi++; }
      }
      if (kind === 'steepest') {
        var s = radii.slice().sort(function (p, q) { return q - p; }), bigR = s[0];
        for (var k = 1; k < s.length; k++) { ev(bigR, s[k], N0 - k + 1); bigR = Math.cbrt(bigR * bigR * bigR + s[k] * s[k] * s[k]); if (half === null && k >= N0 / 2) half = [bigR].concat(s.slice(k + 1)); }
      } else {
        var u = PHYS.rng(1 + Math.floor(Math.random() * 1e9)), pool = {};
        PHYS.gillespieRun(V, radii, A, kind === 'constant' ? { constant: 1e-10 } : KO2, { u: u, tEnd: kind === 'constant' ? 1e12 : 3600, recordEvery: kind === 'constant' ? 1e12 : 3600,
          onEvent: function (a, b, t, alive) {
            if (half === null) { var ka = a.toPrecision(15), kb = b.toPrecision(15); pool[ka] = (pool[ka] || 0) + 1; pool[kb] = (pool[kb] || 0) + 1; var R = Math.cbrt(a * a * a + b * b * b), kr = R.toPrecision(15); pool[kr] = (pool[kr] || 0) - 1;
              if (alive - 1 <= N0 / 2) { half = []; var gone = pool; live.forEach(function (r) { var kk = r.toPrecision(15); if (gone[kk] > 0) gone[kk]--; else half.push(r); }); for (var key in gone) if (gone[key] < 0) for (var g = 0; g < -gone[key]; g++) half.push(+key); } }
            ev(a, b, alive);
          } });
      }
      return { xs: xs, ys: ys, dd: dd, n: n, first: first, half: half };
    }
    function spectrum(rr) {
      var bins = 40, lo = Math.log(2), hi = Math.log(400), dl = (hi - lo) / bins, h = new Array(bins).fill(0), tot = 0, xs = [];
      for (var i = 0; i < bins; i++) xs.push(Math.exp(lo + (i + 0.5) * dl));
      (rr || []).forEach(function (r) { var um = r * 1e6, b = Math.floor((Math.log(um) - lo) / dl); if (b >= 0 && b < bins) { h[b] += um * um * um; } tot += um * um * um; });
      return { x: xs, y: h.map(function (v) { return v / Math.max(tot, 1e-30) / dl; }) };
    }
    $('ru-run').addEventListener('click', function () {
      $('ru-status').textContent = 'merging…';
      setTimeout(function () {
        var V = +$('ru-V').value, u = PHYS.rng(1 + Math.floor(Math.random() * 1e9)), radii = PHYS.drawModes(MODES, V, u, 3);
        var P1 = curve(radii, 'physical', V), P2 = curve(radii, 'constant', V), P3 = curve(radii, 'steepest', V);
        $('ru-plot').innerHTML = CHART.line({ w: 620, h: 300, xmin: 0, xmax: 1, ymin: 0, ymax: 1, xlabel: 'share of the drops merged away, 1 − N/N₀', ylabel: 'surface free energy left / at start', id: 'rup', series: [
          { x: P1.xs, y: P1.ys, label: 'collision kernel (one hour)', color: '#7d1d2f' }, { x: P2.xs, y: P2.ys, label: 'every pair alike', color: '#33627f' },
          { x: P3.xs, y: P3.ys, label: 'largest pair first', color: '#3c6a46', dash: '5 4' }] });
        var s1 = spectrum(P1.half), s2 = spectrum(P2.half), s3 = spectrum(P3.half);
        $('ru-spec').innerHTML = CHART.line({ w: 620, h: 280, xlog: true, xmin: 2, xmax: 400, ymin: 0, xlabel: 'radius r (µm)', ylabel: 'share of the water per unit ln r', id: 'rus', series: [
          { x: s1.x, y: s1.y, label: 'collision kernel, half merged', color: '#7d1d2f' }, { x: s2.x, y: s2.y, label: 'every pair alike, half merged', color: '#33627f' },
          { x: s3.x, y: s3.y, label: 'largest pair first, half merged', color: '#3c6a46', dash: '5 4' }] });
        var pc = function (a, b) { return (100 * a / Math.max(1, b)).toFixed(2) + ' %'; };
        $('ru-out').innerHTML = radii.length + ' drops.<br>Collision kernel: ' + P1.n + ' mergers in an hour, droplet–droplet ' + pc(P1.dd, P1.n) + '; first 100 µm drop after ' + (P1.first || '–') + ' mergers.' +
          '<br>Every pair alike: droplet–droplet ' + pc(P2.dd, P2.n) + '; first 100 µm drop after ' + P2.first + ' mergers.<br>Largest pair first: first 100 µm drop after ' + P3.first + ' mergers.';
        $('ru-status').textContent = 'done';
      }, 20);
    });
  }

  route();
})();
