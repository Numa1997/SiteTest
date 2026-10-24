/* Droplet Collection: the data panel's hooks, inlined by tools/build.py after app.js. The panel (scripts/datalog.js) only reads the
   store that app.js writes (Sim.cloudStore). These hooks read only stored variables: they say what lies at a point of the cloud
   picture, recompute values from stored inputs, and read values back from the picture. Every word they write goes through T(). */
(function () {
  'use strict';
  if (!window.Sim || !Sim.dataset || !Sim.cloudStore) return;
  var T = window.T || function (s) { return s; }, ds = Sim.cloudStore, G = function (k) { return ds.get(k); };
  var cv = document.getElementById('sh-cv'), box = { canvas: cv, ctx: cv.getContext('2d'), get dpr() { return G('dpr'); } };
  var RHO = PHYS.RHO_W, CLS = [T('droplet'), T('collector'), T('drizzle drop')], REG = [T('updraft core'), T('flank'), T('edge band'), T('clear air'), T('below the base')];
  var VOLS = Object.keys(DATA.stoch.n);

  // ---- where stored things are drawn: x across, z up, the picture W × H css px for Lx × Lz metres
  function kx() { return G('W_px') / G('Lx'); }
  function kz() { return G('H_px') / G('Lz'); }
  function at(x, z) { return { x: x * kx(), y: G('H_px') - z * kz() }; }
  function cellOf(c) { return { i: c % 40, j: Math.floor(c / 40) }; }
  function cellAt(c) { var q = cellOf(c), h = G('h'); return at((q.i + 0.5) * h, (q.j + 0.5) * h); }
  function cellIndex(x, z) { var h = G('h'); return Math.min(29, Math.max(0, Math.floor(z / h))) * 40 + Math.min(39, Math.max(0, Math.floor(x / h))); }
  var last = 0;
  function indexOf(id) {        // the store's row of a super-droplet; rows shift as drops rain out, so look it up by its number
    var ID = G('sd_id');
    if (ID[last] === id) return last;
    for (var i = 0; i < ID.length; i++) if (ID[i] === id) return (last = i);
    return -1;
  }
  function mass(rum) { var r = rum * 1e-6; return 4 / 3 * Math.PI * RHO * r * r * r; }
  function air() { return PHYS.air(G('T_air'), G('p_air')); }
  function table() { return { lnR: G('etab_lnR'), lnp: G('etab_lnp'), E: G('etab') }; }

  // ---- Read values: the drop under the pointer (the largest class within 6 px wins, then the nearest), else the 50 m cell
  function probe(x, y) {
    var W = G('W_px'), H = G('H_px');
    if (!(x >= 0 && y >= 0 && x <= W && y <= H)) return null;
    var X = G('sd_x'), Z = G('sd_z'), CL = G('sd_cls'), ID = G('sd_id'), a = kx(), b = kz(), best = -1, bc = -1, bd = 37;
    for (var i = 0; i < X.length; i++) {
      var dx = X[i] * a - x, dy = H - Z[i] * b - y, d = dx * dx + dy * dy;
      if (d < 37 && (CL[i] > bc || CL[i] === bc && d < bd)) { best = i; bc = CL[i]; bd = d; }
    }
    if (best >= 0) return { sd: ID[best], cell: cellIndex(X[best], Z[best]) };
    return { cell: cellIndex(x / a, (H - y) / b) };
  }
  function cellRows(c) {
    return [[T('LWC (cell)'), G('cell_lwc')[c], 'g/m³', 'cell_lwc', c], [T('n (cell)'), G('cell_n')[c], '', 'cell_n', c], [T('r<sub>max</sub> (cell)'), G('cell_rmax')[c], 'µm', 'cell_rmax', c]];
  }
  function dropRows(i) {      // the same rows whether the drop is still there or not (i = −1: empty), so a recorded round keeps its columns
    var v = function (k) { return i < 0 ? NaN : G(k)[i]; }, j = i < 0 ? null : i;
    return [['x', v('sd_x'), 'm', 'sd_x', j], ['z', v('sd_z'), 'm', 'sd_z', j], ['r', v('sd_r'), 'µm', 'sd_r', j], ['ξ', v('sd_xi'), '', 'sd_xi', j], [T('class'), v('sd_cls'), '', 'sd_cls', j]];
  }
  function cellTitle(c) { var q = cellOf(c), h = G('h'); return T('cell at x = ') + (q.i + 0.5) * h + T(' m, z = ') + (q.j + 0.5) * h + T(' m'); }
  function inspect(ref) {
    var rows = [['t', G('t'), 's', 't', null]];
    if (ref.sd !== undefined) {
      var i = indexOf(ref.sd);
      if (i < 0) return { title: T('super-droplet ') + ref.sd + T(' is gone (rained out, evaporated, or its drops merged away); showing the ') + cellTitle(ref.cell) + T(' where it was pinned'), at: cellAt(ref.cell), rows: rows.concat(dropRows(-1), cellRows(ref.cell)) };
      var X = G('sd_x'), Z = G('sd_z'), c = cellIndex(X[i], Z[i]);
      return { title: T('super-droplet ') + ref.sd + ' · ' + CLS[G('sd_cls')[i]] + T(', ') + cellTitle(c), at: at(X[i], Z[i]), rows: rows.concat(dropRows(i), cellRows(c)) };
    }
    return { title: cellTitle(ref.cell), at: cellAt(ref.cell), rows: rows.concat(cellRows(ref.cell)) };
  }
  function locate(name, idx) {
    if (/^sd_/.test(name)) { var X = G('sd_x'), Z = G('sd_z'); return idx < X.length ? at(X[idx], Z[idx]) : null; }
    if (/^cell_/.test(name)) return cellAt(idx);
    if (name === 'reg') { var nz = ds.dims.rz; return at((Math.floor(idx / nz) + 0.5) * 25, (idx % nz + 0.5) * 25); }
    return null;
  }

  // ---- Check, second answer: recomputed from stored inputs only
  function inp(sym, name, units, digits) { return [sym, G(name), units, digits === undefined ? 4 : digits]; }
  function sum(f) { var s = 0, n = G('sd_x').length; for (var i = 0; i < n; i++) s += f(i); return s; }
  var check = {
    rho_air: function () { return { formula: 'ρ<sub>a</sub> = p / (R<sub>d</sub> T)', inputs: [inp('p', 'p_air', 'Pa', 0), inp('T', 'T_air', 'K', 2), ['R<sub>d</sub>', PHYS.R_D, 'J/(kg K)', 2]], value: air().rho }; },
    mu_air: function () { return { formula: T('Sutherland’s law, PHYS.air(T, p), in µPa·s'), inputs: [inp('T', 'T_air', 'K', 2)], value: air().mu * 1e6 }; },
    dV: function () { return { formula: 'ΔV = h³', inputs: [inp('h', 'h', 'm', 0)], value: Math.pow(G('h'), 3) }; },
    xi1: function () { return { formula: 'ξ<sub>1</sub> = N<sub>1</sub> ΔV / n<sub>1</sub>', inputs: [inp('N<sub>1</sub>', 'N1', 'm⁻³', 0), inp('ΔV', 'dV', 'm³', 0), inp('n<sub>1</sub>', 'per1', '', 0)], value: G('N1') * G('dV') / G('per1') }; },
    xi2: function () { return { formula: 'ξ<sub>2</sub> = N<sub>2</sub> ΔV / n<sub>2</sub>', inputs: [inp('N<sub>2</sub>', 'N2', 'm⁻³', 0), inp('ΔV', 'dV', 'm³', 0), inp('n<sub>2</sub>', 'per2', '', 0)], value: G('N2') * G('dV') / G('per2') }; },
    sigma_u: function () { return { formula: 'σ<sub>u</sub> = (ε L<sub>e</sub>)<sup>1/3</sup>', inputs: [inp('ε', 'eps', 'm²/s³'), inp('L<sub>e</sub>', 'Le', 'm', 0)], value: Math.cbrt(G('eps') * G('Le')) }; },
    T_L: function () { return { formula: 'T<sub>L</sub> = 2σ<sub>u</sub>² / (C<sub>0</sub> ε)', inputs: [inp('σ<sub>u</sub>', 'sigma_u', 'm/s'), inp('C<sub>0</sub>', 'C0', '', 0), inp('ε', 'eps', 'm²/s³')], value: 2 * G('sigma_u') * G('sigma_u') / (G('C0') * G('eps')) }; },
    G_grow: function () { return { formula: T('G = 1 / (F<sub>k</sub> + F<sub>d</sub>), PHYS.growthG(T, p), in µm²/s'), inputs: [inp('T', 'T_air', 'K', 2), inp('p', 'p_air', 'Pa', 0)], value: PHYS.growthG({ T: G('T_air'), p: G('p_air') }) * 1e12 }; },
    E_40_10: function () { return { formula: T('E(R = 40 µm, p = 0.25), bilinear in the stored table E over ln R and ln p'), inputs: [['R', 40, 'µm', 0], ['p', 0.25, '', 2]], value: PHYS.tableE(table(), 40e-6, 0.25, 'clamp') }; },
    E_100_20: function () { return { formula: T('E(R = 100 µm, p = 0.2), bilinear in the stored table E over ln R and ln p'), inputs: [['R', 100, 'µm', 0], ['p', 0.2, '', 2]], value: PHYS.tableE(table(), 100e-6, 0.2, 'clamp') }; },
    K_40_10: function () {
      var A = air(), v1 = PHYS.vBeard(40e-6, A), v2 = PHYS.vBeard(10e-6, A);
      return { formula: T('K = π (R + r)² |v<sub>R</sub> − v<sub>r</sub>| E E<sub>c</sub>, with E from the stored table, in cm³/s'), inputs: [['R', 40, 'µm', 0], ['r', 10, 'µm', 0], ['v<sub>R</sub>', v1 * 100, 'cm/s', 3], ['v<sub>r</sub>', v2 * 100, 'cm/s', 3], inp('E(40, 10)', 'E_40_10', '')],
        value: PHYS.kernel(40e-6, 10e-6, A, { speed: 'beard', eff: 'table', coal: 'law', near: 'clamp', tab: table() }) * 1e6 };
    },
    t_min: function () { return { formula: 't / 60', inputs: [inp('t', 't', 's', 0)], value: G('t') / 60 }; },
    n_sd: function () { return { formula: T('the number of rows of the stored super-droplets'), inputs: [], value: G('sd_x').length }; },
    N_air: function () { return { formula: 'N = Σ ξ<sub>i</sub>', inputs: [[T('rows'), G('sd_xi').length, '', 0]], value: sum(function (i) { return G('sd_xi')[i]; }) }; },
    M_air: function () { var R = G('sd_r'), XI = G('sd_xi'); return { formula: 'M = Σ ξ<sub>i</sub> (4/3) π ρ<sub>w</sub> r<sub>i</sub>³', inputs: [['ρ<sub>w</sub>', RHO, 'kg/m³', 0], [T('rows'), R.length, '', 0]], value: sum(function (i) { return XI[i] * mass(R[i]); }) }; },
    M40: function () { var R = G('sd_r'), XI = G('sd_xi'); return { formula: 'M<sub>40</sub> = Σ<sub>r ≥ 40 µm</sub> ξ<sub>i</sub> (4/3) π ρ<sub>w</sub> r<sub>i</sub>³', inputs: [['ρ<sub>w</sub>', RHO, 'kg/m³', 0]], value: sum(function (i) { return R[i] >= 40 ? XI[i] * mass(R[i]) : 0; }) }; },
    M100: function () { var R = G('sd_r'), XI = G('sd_xi'); return { formula: 'M<sub>100</sub> = Σ<sub>r ≥ 100 µm</sub> ξ<sub>i</sub> (4/3) π ρ<sub>w</sub> r<sub>i</sub>³', inputs: [['ρ<sub>w</sub>', RHO, 'kg/m³', 0]], value: sum(function (i) { return R[i] >= 100 ? XI[i] * mass(R[i]) : 0; }) }; },
    N_share: function () { return { formula: '100 N / N<sub>0</sub>', inputs: [inp('N', 'N_air', '', 0), inp('N<sub>0</sub>', 'N0', '', 0)], value: 100 * G('N_air') / G('N0') }; },
    F_air: function () { return { formula: '100 M / M<sub>0</sub>', inputs: [inp('M', 'M_air', 'kg', 3), inp('M<sub>0</sub>', 'M0', 'kg', 3)], value: 100 * G('M_air') / G('M0') }; },
    F100: function () { return { formula: '100 M<sub>100</sub> / M<sub>0</sub>', inputs: [inp('M<sub>100</sub>', 'M100', 'kg', 3), inp('M<sub>0</sub>', 'M0', 'kg', 3)], value: 100 * G('M100') / G('M0') }; },
    F_rain: function () { return { formula: '100 M<sub>rain</sub> / M<sub>0</sub>', inputs: [inp('M<sub>rain</sub>', 'rain', 'kg', 3), inp('M<sub>0</sub>', 'M0', 'kg', 3)], value: 100 * G('rain') / G('M0') }; },
    F_evap: function () { return { formula: '100 M<sub>evap</sub> / M<sub>0</sub>', inputs: [inp('M<sub>evap</sub>', 'evap', 'kg', 3), inp('M<sub>0</sub>', 'M0', 'kg', 3)], value: 100 * G('evap') / G('M0') }; },
    F_evap_below: function () { return { formula: '100 M<sub>evap, base</sub> / M<sub>0</sub>', inputs: [inp('M<sub>evap, base</sub>', 'evap_below', 'kg', 3), inp('M<sub>0</sub>', 'M0', 'kg', 3)], value: 100 * G('evap_below') / G('M0') }; },
    r_max: function () { var R = G('sd_r'), m = 0; for (var i = 0; i < R.length; i++) m = Math.max(m, R[i]); return { formula: 'max r<sub>i</sub>', inputs: [[T('rows'), R.length, '', 0]], value: m }; },
    M0: function () { return { formula: T('the water book read the other way: M<sub>0</sub> = M + M<sub>rain</sub> + M<sub>evap</sub>'), inputs: [inp('M', 'M_air', 'kg', 3), inp('M<sub>rain</sub>', 'rain', 'kg', 3), inp('M<sub>evap</sub>', 'evap', 'kg', 3)], value: G('M_air') + G('rain') + G('evap') }; },
    N0: function () { return { formula: T('the number book read the other way: N<sub>0</sub> = N + N<sub>rain</sub> + N<sub>evap</sub> + N<sub>merge</sub>'), inputs: [inp('N', 'N_air', '', 0), inp('N<sub>rain</sub>', 'N_rain', '', 0), inp('N<sub>evap</sub>', 'N_evap', '', 0), inp('N<sub>merge</sub>', 'mergers', '', 0)], value: G('N_air') + G('N_rain') + G('N_evap') + G('mergers') }; },
    book_M_res: function () { return { formula: 'δM = M<sub>0</sub> − M − M<sub>rain</sub> − M<sub>evap</sub>', inputs: [inp('M<sub>0</sub>', 'M0', 'kg', 3), inp('M', 'M_air', 'kg', 3), inp('M<sub>rain</sub>', 'rain', 'kg', 3), inp('M<sub>evap</sub>', 'evap', 'kg', 3)], value: G('M0') - G('M_air') - G('rain') - G('evap') }; },
    book_M_rel: function () { return { formula: 'δM / M<sub>0</sub>', inputs: [inp('δM', 'book_M_res', 'kg', 9), inp('M<sub>0</sub>', 'M0', 'kg', 3)], value: G('book_M_res') / G('M0') }; },
    book_N_res: function () { return { formula: 'δN = N<sub>0</sub> − N − N<sub>rain</sub> − N<sub>evap</sub> − N<sub>merge</sub>', inputs: [inp('N<sub>0</sub>', 'N0', '', 0), inp('N', 'N_air', '', 0), inp('N<sub>rain</sub>', 'N_rain', '', 0), inp('N<sub>evap</sub>', 'N_evap', '', 0), inp('N<sub>merge</sub>', 'mergers', '', 0)], value: G('N0') - G('N_air') - G('N_rain') - G('N_evap') - G('mergers') }; },
    book_N_rel: function () { return { formula: 'δN / N<sub>0</sub>', inputs: [inp('δN', 'book_N_res', '', 0), inp('N<sub>0</sub>', 'N0', '', 0)], value: G('book_N_res') / G('N0') }; },
    px_per_m: function () { return { formula: 's = W / L<sub>x</sub>', inputs: [inp('W', 'W_px', 'px', 0), inp('L<sub>x</sub>', 'Lx', 'm', 0)], value: G('W_px') / G('Lx') }; },
    sd_cls: function (i) { var r = G('sd_r')[i]; return { formula: T('0 if r &lt; 20 µm, 1 if r &lt; 100 µm, else 2'), inputs: [['r', r, 'µm', 2]], value: r >= 100 ? 2 : r >= 20 ? 1 : 0 }; },
    cell_lwc: function (c) {
      var X = G('sd_x'), Z = G('sd_z'), R = G('sd_r'), XI = G('sd_xi'), dV = G('dV'), n = 0, s = sum(function (i) { if (cellIndex(X[i], Z[i]) !== c) return 0; n++; return XI[i] * mass(R[i]); });
      return { formula: T('LWC = Σ<sub>cell</sub> ξ<sub>i</sub> (4/3) π ρ<sub>w</sub> r<sub>i</sub>³ / ΔV, in g/m³'), inputs: [inp('ΔV', 'dV', 'm³', 0), [T('super-droplets in the cell'), n, '', 0]], value: s / dV * 1e3 };
    },
    cell_n: function (c) { var X = G('sd_x'), Z = G('sd_z'); return { formula: T('count of stored super-droplets whose (x, z) falls in the cell'), inputs: [], value: sum(function (i) { return cellIndex(X[i], Z[i]) === c ? 1 : 0; }) }; },
    cell_rmax: function (c) { var X = G('sd_x'), Z = G('sd_z'), R = G('sd_r'), m = 0; for (var i = 0; i < X.length; i++) if (cellIndex(X[i], Z[i]) === c) m = Math.max(m, R[i]); return { formula: T('max r<sub>i</sub> over the cell'), inputs: [], value: m }; },
    lk_rank: function () {
      var V = G('lk_V'), t = G('lk_t100'), runs = G('t100_' + V) || [], k = 0;
      for (var i = 0; i < runs.length; i++) if (runs[i] < (t === t ? t : 30)) k++;   // runs in minutes; your run lasts 30 min
      return { formula: T('100 · (stored runs with an earlier first 100 µm drop) / n<sub>runs</sub>'), inputs: [inp('t<sub>100</sub>', 'lk_t100', 'min', 2), inp('n<sub>runs</sub>', 'ens_n_' + V, '', 0)], value: 100 * k / G('ens_n_' + V) };
    }
  };
  ['v10', 'v20', 'v40', 'v100'].forEach(function (n) {
    var r = +n.slice(1);
    check[n] = function () { return { formula: T('Beard (1976), PHYS.vBeard(r, air(T, p)), in cm/s'), inputs: [['r', r, 'µm', 0], inp('T', 'T_air', 'K', 2), inp('p', 'p_air', 'Pa', 0)], value: PHYS.vBeard(r * 1e-6, air()) * 100 }; };
  });
  VOLS.forEach(function (V) {     // the ensemble's spread, from the stored sorted times
    var arr = function () { return G('t100_' + V); };
    function q(p) { var t = arr(); if (!t.length) return NaN; var x = p * (t.length - 1), i = Math.floor(x), f = x - i; return i + 1 < t.length ? t[i] + f * (t[i + 1] - t[i]) : t[i]; }
    check['ens_hit_' + V] = function () { return { formula: 'P<sub>60</sub> = 100 · n / n<sub>runs</sub>', inputs: [[T('runs with t<sub>100</sub>'), arr().length, '', 0], inp('n<sub>runs</sub>', 'ens_n_' + V, '', 0)], value: 100 * arr().length / G('ens_n_' + V) }; };
    check['ens_mean_' + V] = function () { var t = arr(), s = 0; for (var i = 0; i < t.length; i++) s += t[i]; return { formula: '⟨t<sub>100</sub>⟩ = Σ t<sub>100</sub> / n', inputs: [['n', t.length, '', 0]], value: t.length ? s / t.length : NaN }; };
    check['ens_sd_' + V] = function () { var t = arr(), m = G('ens_mean_' + V), s = 0; for (var i = 0; i < t.length; i++) s += (t[i] - m) * (t[i] - m); return { formula: 's<sub>t</sub> = √(Σ (t<sub>100</sub> − ⟨t<sub>100</sub>⟩)² / (n − 1))', inputs: [['n', t.length, '', 0], inp('⟨t<sub>100</sub>⟩', 'ens_mean_' + V, 'min', 2)], value: t.length > 1 ? Math.sqrt(s / (t.length - 1)) : NaN }; };
    [10, 50, 90].forEach(function (p) {
      check['ens_p' + p + '_' + V] = function () { return { formula: T('linear interpolation in the stored sorted t<sub>100</sub> at (n − 1) · ') + p / 100, inputs: [['n', arr().length, '', 0]], value: q(p / 100) }; };
    });
  });

  // ---- Check, third answer: read back from the picture. A transparent pixel never passes (alpha first, then colour).
  var IS = [function (c) { return c[3] > 200 && c[2] > c[0] + 25 && c[2] < 215; },                                   // droplet: blue at 55 % over the sky
    function (c) { return c[3] > 200 && c[0] > 170 && c[0] - c[2] > 90 && c[1] > 90 && c[1] < 150; },                     // collector: ochre #c9783f
    function (c) { return c[3] > 200 && c[0] > c[1] + 50 && c[0] > c[2] + 40 && c[0] < 170; }];                           // drizzle: wine #7d1d2f
  var COL = [T('blue'), T('ochre'), T('wine')];
  function dot(i) {
    var X = G('sd_x'), Z = G('sd_z'), cl = G('sd_cls')[i], p = at(X[i], Z[i]), q = Sim.readPixel(box, p.x, p.y, 1, IS[cl]);
    var what = T('the dot of super-droplet ') + G('sd_id')[i] + ', (' + Sim.fmt(p.x, 1) + ', ' + Sim.fmt(p.y, 1) + T(') css px');
    if (q.found) return { what: what, drawn: q.text, expected: COL[cl] + T(', class ') + cl + ' (' + CLS[cl] + ')', ok: true, note: T('Drawn at x·s, H − z·s with s = W / L<sub>x</sub>; the colour shows the class, not the radius.') };
    var other = -1; for (var k = 0; k < 3; k++) if (k !== cl && Sim.readPixel(box, p.x, p.y, 0, IS[k]).found) other = k;
    var c = Sim.readPixel(box, p.x, p.y, 0).rgba;
    if (other >= 0 || c[3] > 200 && c[0] < 60 && c[1] < 40) return { what: what, drawn: q.text, expected: COL[cl], ok: null, note: other >= 0 ? T('A ') + CLS[other] + T(' drawn later covers this dot: the dots overlap and the last one drawn shows.') : T('The followed drop’s trail or the probe’s frame covers this dot.') };
    return { what: what, drawn: q.text, expected: COL[cl] + T(', class ') + cl, ok: false, note: T('Nothing of the expected colour within 1 px of where the store puts this drop.') };
  }
  var BG = [function (c) { return c[3] > 250 && Math.abs(c[0] - 214) < 8 && Math.abs(c[1] - 228) < 8 && Math.abs(c[2] - 235) < 8; },
    function (c) { return c[3] > 250 && Math.abs(c[0] - 244) < 6 && Math.abs(c[1] - 248) < 6 && Math.abs(c[2] - 250) < 6; }];
  function readText(id, re) { var el = document.getElementById(id), m = el && re.exec(el.textContent); return m ? parseFloat(m[1]) : NaN; }
  function words(id, re, name, digits, label) {
    return function () {
      var shown = readText(id, re), want = G(name), ok = Math.abs(shown - want) <= 0.5 * Math.pow(10, -digits) + 1e-12;
      return { what: T('the readout ') + label, drawn: isFinite(shown) ? Sim.fmt(shown, digits) : T('not shown'), expected: isFinite(want) ? Sim.fmt(want, digits) : T('not yet'), ok: !isFinite(want) && !isFinite(shown) ? true : ok ? true : G('running') ? null : false,
        note: T('The words are rewritten from the store about four times a second, so while the cloud runs they can be up to 250 ms behind.') };
    };
  }
  var drawn = {
    sd_x: dot, sd_z: dot, sd_r: dot, sd_xi: dot, sd_cls: dot, sd_id: dot,
    reg: function (idx) {
      var nz = ds.dims.rz, p = at((Math.floor(idx / nz) + 0.5) * 25, (idx % nz + 0.5) * 25), rg = G('reg')[idx], inside = rg <= 2, q = Sim.readPixel(box, p.x, p.y, 6, BG[inside ? 0 : 1]);
      return { what: T('the background near the middle of this 25 m square, within 6 px'), drawn: q.text, expected: inside ? T('pale blue: saturated cloud') : T('near white: clear air'), ok: q.found ? true : null,
        note: T('The pale cloud is drawn on 20 m squares tested against the outline; the regions are kept on 25 m squares, so near the outline the two can differ by a square.') };
    },
    t_min: words('sh-time', /t = ([\d.]+) min/, 't_min', 1, T('t = … min above the picture')),
    F_air: words('sh-out', /still in the air ([\d.]+) %/, 'F_air', 1, T('“water still in the air”')),
    F100: words('sh-out', /≥ 100 µm ([\d.]+) %/, 'F100', 1, T('“in drops ≥ 100 µm”')),
    F_rain: words('sh-out', /rained out ([\d.]+) %/, 'F_rain', 1, T('“rained out”')),
    F_evap: words('sh-out', /evaporated ([\d.]+) %/, 'F_evap', 1, T('“evaporated”')),
    t100_first: words('sh-out', /100 µm: ([\d.]+) min/, 't100_first', 1, T('“first drop of 100 µm”')),
    W_px: function () { return { what: T('the picture’s width on the page'), drawn: Sim.fmt(cv.getBoundingClientRect().width, 1) + ' px', expected: Sim.fmt(G('W_px'), 1) + ' px', ok: Math.abs(cv.getBoundingClientRect().width - G('W_px')) < 0.6, note: T('The canvas holds W · dpr device pixels and is shown W css pixels wide.') }; },
    H_px: function () { return { what: T('the picture’s height on the page'), drawn: Sim.fmt(cv.getBoundingClientRect().height, 1) + ' px', expected: Sim.fmt(G('H_px'), 1) + ' px', ok: Math.abs(cv.getBoundingClientRect().height - G('H_px')) < 0.6, note: T('H = 0.75 W, the slice’s 1.5 km by 2 km.') }; }
  };

  // ---- the panel's contract (scripts/datalog.js)
  var ens = [];
  VOLS.forEach(function (V) { ens.push('ens_n_' + V, 'ens_hit_' + V, 'ens_mean_' + V, 'ens_sd_' + V, 'ens_p10_' + V, 'ens_p50_' + V, 'ens_p90_' + V, 't100_' + V); });
  function biggest() { var R = G('sd_r'), ID = G('sd_id'), b = -1, m = -1; for (var i = 0; i < R.length; i++) if (R[i] > m) { m = R[i]; b = i; } return b >= 0 ? { sd: ID[b], cell: cellIndex(G('sd_x')[b], G('sd_z')[b]) } : null; }
  Sim.data = {
    ds: ds, kicker: T('Droplet Collection · data'), file: 'droplet-collection-cloud',
    playing: function () { return !!G('running'); },
    play: function () { if (!G('running')) document.getElementById('sh-go').click(); },
    groups: [
      { title: T('Cloud set-up'), note: T('what you choose in panel 4, and what the page fixes: the air, the two drop modes, the slice and its cells'),
        vars: ['shape', 'W0', 'stochastic', 'Le', 'per_frame', 'seed', 'kernel', 'T_air', 'p_air', 'N1', 'rg1', 'sg1', 'N2', 'rg2', 'sg2', 'Lx', 'Lz', 'h', 'per1', 'per2', 'S_out', 'eps', 'C0', 'dt'] },
      { title: T('Derived constants'), note: T('worked out once from the set-up: the air, fall speeds, collision efficiencies, the kernel, the eddies, the starting cloud'),
        vars: ['rho_air', 'mu_air', 'dV', 'xi1', 'xi2', 'v10', 'v20', 'v40', 'v100', 'E_40_10', 'E_100_20', 'K_40_10', 'etab_lnR', 'etab_lnp', 'etab', 'sigma_u', 'T_L', 'G_grow', 'zbase', 'reg', 'n_sd0', 'M0', 'N0'] },
      { title: T('The state now'), note: T('the cloud at this frame: where its water is, its largest drop, the first drizzle drop'),
        vars: ['t', 't_min', 'F100', 'F_air', 'F_rain', 'F_evap', 'F_evap_below', 'M_air', 'M40', 'M100', 'M_in', 'N_air', 'N_share', 'n_sd', 'r_max', 't100_first', 'x100', 'z100', 'follow_id', 'follow_r', 'follow_z', 'probe_i', 'probe_j', 'probe_u', 'probe_w', 'probe_reg'] },
      { title: T('The books'), note: T('water: M<sub>0</sub> = M + M<sub>rain</sub> + M<sub>evap</sub> + δM; drops: N<sub>0</sub> = N + N<sub>rain</sub> + N<sub>evap</sub> + N<sub>merge</sub> + δN. The residuals δ should be rounding only.'),
        vars: ['rain', 'evap', 'evap_below', 'book_M_res', 'book_M_rel', 'N_rain', 'N_evap', 'mergers', 'book_N_res', 'book_N_rel'] },
      { title: T('Super-droplets and cells now'), note: T('one row per super-droplet still in the air, and the 40 × 30 collision cells of 50 m'),
        vars: ['sd_id', 'sd_x', 'sd_z', 'sd_r', 'sd_xi', 'sd_cls', 'cell_lwc', 'cell_n', 'cell_rmax'] },
      { title: T('Lucky drops: the exact runs as an ensemble'), note: T('panel 3: the stored exact runs of each volume, their spread, and your own run against them'),
        vars: ens.concat(['lk_V', 'lk_seed', 'lk_drops', 'lk_events', 'lk_t100', 'lk_big', 'lk_rank', 'lk_t', 'lk_rmax']) },
      { title: T('Solver'), note: T('how the cloud is stepped: 1 s steps, super-droplet pairs drawn in each cell'), vars: ['steps', 'step_ms', 'gam_events', 'gam_many', 'running'] },
      { title: T('Drawing'), note: T('how stored metres become pixels'), vars: ['W_px', 'H_px', 'dpr', 'px_per_m'] }
    ],
    rowLabel: { sd: function (i) { return 'id ' + G('sd_id')[i]; }, cz: function (j) { return 'z ' + j * 50 + '–' + (j + 1) * 50 + ' m'; } },
    colLabel: { cell_lwc: function (i) { return 'x ' + i * 50; }, cell_n: function (i) { return 'x ' + i * 50; }, cell_rmax: function (i) { return 'x ' + i * 50; } },
    probe: probe, inspect: inspect, locate: locate, check: check, drawn: drawn,
    round: { time: 't', label: function () { return T('five cloud-minutes of panel 4'); }, length: function () { return 300; },
      columns: ['F100', 'F_air', 'F_rain', 'F_evap', 'N_air', 'n_sd', 'r_max', 'book_M_rel', 'book_N_rel'], point: biggest,
      blocked: function () { return G('t') > 2400 ? T('fewer than five cloud-minutes are left before the cloud stops at 45 min; press New cloud') : null; } },
    about: T('The picture is drawn from the model’s super-droplets in the same frame in which the store copies them, so positions agree exactly; ' +
      'a drop’s radius is drawn only as one of three dot sizes and colours (its class: droplet below 20 µm, collector, drizzle from 100 µm), not to scale, and dots overlap, so a later dot covers an earlier one. ' +
      'The store keeps radii in µm, speeds in cm/s, viscosity in µPa·s and the growth constant in µm²/s; the model works in SI units. ' +
      'The pale cloud is drawn on 20 m squares tested against the outline, the regions are kept on 25 m squares and the cells of the store are the model’s 50 m collision cells. ' +
      'The arrows of the mean motion are drawn once per cloud, every 100 m. The followed drop’s trail keeps its last 900 positions and is not stored. ' +
      'Rain, evaporation and mergers are running totals the model adds up step by step; the two books check them against the drops still in the air. ' +
      'The words beside the picture are rewritten from the store about four times a second; the dots every frame. ' +
      'The ensemble of panel 3 is read from the stored exact runs (data/stochastic.json), not rerun here; your own run is a new random history each time.')
  };

  // ---- the ledger (scripts/datalog.js, Sim.data.ledger): what the panel shows first, the rest in causal order, and the two books.
  // It only names stored variables; the residuals are stored by app.js at the line that computes them.
  var ensVars = [], ensRuns = [];
  VOLS.forEach(function (V) { ensVars.push('ens_n_' + V, 'ens_hit_' + V, 'ens_mean_' + V, 'ens_sd_' + V, 'ens_p10_' + V, 'ens_p50_' + V, 'ens_p90_' + V); ensRuns.push('t100_' + V); });
  var how = { per_frame: 'set', seed: 'set', kernel: 'constant', etab: 'run', etab_lnR: 'run', etab_lnp: 'run', reg: 'solver', n_sd0: 'solver', M0: 'solver', N0: 'solver', zbase: 'solver',
    t: 'solver', M_air: 'solver', M40: 'solver', M100: 'solver', M_in: 'solver', t100_first: 'solver', x100: 'solver', z100: 'solver', follow_id: 'set', probe_i: 'set', probe_j: 'set',
    rain: 'solver', evap: 'solver', evap_below: 'solver', N_rain: 'solver', N_evap: 'solver', mergers: 'solver', lk_V: 'set', lk_seed: 'solver', lk_drops: 'solver', lk_events: 'solver',
    lk_t100: 'solver', lk_big: 'solver', lk_t: 'solver', lk_rmax: 'solver', lk_rank: 'formula', running: 'set' };
  ['shape', 'W0', 'stochastic', 'Le'].forEach(function (n) { how[n] = 'set'; });
  ['sd_id', 'sd_x', 'sd_z', 'sd_r', 'sd_xi'].forEach(function (n) { how[n] = 'solver'; });
  ensRuns.forEach(function (n) { how[n] = 'run'; }); VOLS.forEach(function (V) { how['ens_n_' + V] = 'run'; });
  var AIR = ['T_air', 'p_air'];
  Sim.data.ledger = {
    headline: [{ v: 'F100', title: T('water in drizzle') }, { v: 'N_share', title: T('drops left') }, { v: 't_min', title: T('cloud time') },
      { v: 't100_first', title: T('first drizzle drop') }, { v: 'F_rain', title: T('rained out') }, { v: 'r_max', title: T('largest drop') }],
    sections: [
      { title: T('Cloud set-up'), note: T('what you choose in panel 4, and what the page fixes: the air, the two drop modes, the slice and its cells'), how: 'constant',
        vars: ['shape', 'W0', 'stochastic', 'Le', 'per_frame', 'seed', 'kernel', 'T_air', 'p_air', 'N1', 'rg1', 'sg1', 'N2', 'rg2', 'sg2', 'Lx', 'Lz', 'h', 'per1', 'per2', 'S_out', 'eps', 'C0', 'dt'] },
      { title: T('What follows from it'), note: T('worked out from the set-up before anything moves: the air, fall speeds, collision efficiencies, the kernel, the eddies, the starting cloud'), how: 'formula',
        vars: ['rho_air', 'mu_air', 'dV', 'xi1', 'xi2', 'v10', 'v20', 'v40', 'v100', 'E_40_10', 'E_100_20', 'K_40_10', 'etab', 'etab_lnR', 'etab_lnp', 'sigma_u', 'T_L', 'G_grow', 'zbase', 'reg', 'n_sd0', 'M0', 'N0'] },
      { title: T('The state now'), note: T('the cloud at this frame: where its water is, its largest drop, the first drizzle drop, the drop you follow and the probe you pinned'), how: 'formula',
        vars: ['t', 't_min', 'F100', 'F_air', 'F_rain', 'F_evap', 'F_evap_below', 'M_air', 'M40', 'M100', 'M_in', 'N_air', 'N_share', 'n_sd', 'r_max', 't100_first', 'x100', 'z100', 'follow_id', 'follow_r', 'follow_z', 'probe_i', 'probe_j', 'probe_u', 'probe_w', 'probe_reg'] },
      { title: T('Super-droplets and cells now'), note: T('one row per super-droplet still in the air (each stands for ξ real drops), and the 40 × 30 collision cells of 50 m'), how: 'formula',
        vars: ['sd_id', 'sd_x', 'sd_z', 'sd_r', 'sd_xi', 'sd_cls', 'cell_lwc', 'cell_n', 'cell_rmax'] },
      { title: T('Lucky drops: the exact runs as an ensemble'), note: T('panel 3: the stored exact runs of each volume, their spread, and your own run against them'), how: 'formula',
        vars: ensVars.concat(ensRuns, ['lk_V', 'lk_seed', 'lk_drops', 'lk_events', 'lk_t100', 'lk_big', 'lk_rank', 'lk_t', 'lk_rmax']) },
      { title: T('Solver'), note: T('how the cloud is stepped: 1 s steps, super-droplet pairs drawn in each cell'), how: 'solver', folded: true, vars: ['steps', 'step_ms', 'gam_events', 'gam_many', 'running'] },
      { title: T('Drawing'), note: T('how stored metres become pixels'), how: 'drawing', folded: true, vars: ['W_px', 'H_px', 'dpr', 'px_per_m'] }
    ],
    how: how,
    books: [
      { title: T('Water'), short: T('water'), note: T('Every gram of water at the start is still in the air, has reached the ground, or has evaporated outside the cloud; merging moves water between drops but never makes or destroys it.'),
        rows: [[1, 'M0'], [-1, 'rain'], [-1, 'evap']], total: 'M_air', residual: 'book_M_res', tol: 1e-9, paused: function () { return null; } },
      { title: T('Drops'), short: T('drops'), note: T('Every drop at the start is still in the air, has rained out, has evaporated completely, or was swallowed in a merger: two drops become one, so each merger removes one drop.'),
        rows: [[1, 'N0'], [-1, 'N_rain'], [-1, 'N_evap'], [-1, 'mergers']], total: 'N_air', residual: 'book_N_res', tol: 1e-12, paused: function () { return null; } }
    ],
    deps: { rho_air: AIR, mu_air: AIR, G_grow: AIR, v10: AIR, v20: AIR, v40: AIR, v100: AIR, E_40_10: ['etab'], E_100_20: ['etab'], K_40_10: AIR.concat(['etab']),
      dV: ['h'], xi1: ['N1', 'h', 'per1'], xi2: ['N2', 'h', 'per2'], sigma_u: ['eps', 'Le'], T_L: ['eps', 'Le', 'C0'], px_per_m: ['W_px'], lk_rank: ['lk_V', 'lk_t100'] },
    controls: { 'sh-shape': 'shape', 'sh-wind': 'W0', 'sh-stoch': 'stochastic', 'sh-le': 'Le', 'sh-speed': 'per_frame', 'lk-V': 'lk_V' }
  };
})();
