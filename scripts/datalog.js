/* Numa Koudsie · data panel
   A live variable explorer in the manner of Spyder's, fed by one store: the page's dataset (scripts/dataset.js).
   The simulation writes every number into that dataset at the moment it computes it; this panel only reads.
   A page opts in by defining Sim.data next to its own state and loading this file after its own script, with
   styles/data.css in its head.

   Sim.data = {
     ds:       the dataset,
     playing:  function () → bool,
     groups:   [{ title, note, vars: ['lambda', 'k', ...] }]        names of dataset variables, in display order
     colour:   { psi: function (value, j, i) → [r, g, b] | null }  shading for array cells (presentation only)
     probe:    function (xCss, yCss) → ref | null                   what lies under the pointer on the figure
     inspect:  function (ref) → { title, at: {x, y}, rows: [[symbol, value, units, varName, index]] }
     locate:   function (varName, index) → {x, y} | null            where an array element is drawn, css px
     check:    { name: function (index) → { formula, inputs: [[symbol, value, units]], value } }
                                                                    an independent recomputation, the self-test
     drawn:    { name: function (index) → { what, drawn, expected, ok, note } }   read-back from the picture
     log:      { every, max, label, time: varName, columns: [varName, ...] }
     about:    html                                                  what still differs between data and picture
     file:     'fig1-wave-interference'                              base name of the saved archive
   }

   Variables   name, type, shape and value of every dataset variable, repainted every frame while open.
   Tables      any array opens as a table; only the cells in view are drawn.
   Probe       the pointer over the figure reads the values there; a marker shows the point; the last point
               is held in the panel so its values can be checked.
   Check       for any value: stored value, the formula recomputed from the stored inputs, and the read-back
               from the picture, with the agreement stated.
   Log         one row per step of time (or per change), newest at the bottom, bounded.
   Save        a zip of NumPy .npy files, dataset.json, log.csv and a README with the Python lines to open it. */
(function () {
    'use strict';
    var Sim = window.Sim, spec = Sim && Sim.data, ds = spec && spec.ds;
    if (!spec || !ds) return;

    /* ---------- helpers ---------- */
    var KEY = 'datapanel.';
    function load(k) { try { return localStorage.getItem(KEY + k); } catch (e) { return null; } }
    function store(k, v) { try { localStorage.setItem(KEY + k, v); } catch (e) { /* storage blocked: the choice lasts for this page */ } }
    function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
    function grouped(n) {
        var s = String(Math.round(Math.abs(n)));
        if (s.length > 4) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
        return (n < 0 ? '−' : '') + s;
    }
    function num(v, d) {
        if (v === undefined || v === null) return '—';
        if (typeof v === 'string') return v;
        if (typeof v === 'boolean') return v ? 'True' : 'False';
        if (!isFinite(v)) return '—';
        if (d === 0 && Math.abs(v) >= 10000) return grouped(v);
        return Sim.fmt(v, d === undefined ? 4 : d);
    }
    function sci(v) { return v === 0 ? '0' : v.toExponential(2).replace(/-/g, '−'); }
    function textOn(rgb) { return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2] > 150 ? '#1c1518' : '#fffaf3'; }
    function safe(fn, fallback) { try { return fn(); } catch (e) { return fallback; } }

    var NEG = [58, 50, 46], MID = [255, 250, 243], POS = [122, 31, 43];
    Sim.colourMap = function (v, lim) {
        var a = lim > 0 ? v / lim : 0;
        if (!(a === a)) a = 0;
        a = a > 1 ? 1 : a < -1 ? -1 : a;
        var s = Math.pow(Math.abs(a), 0.8), end = a < 0 ? NEG : POS;
        return [0, 1, 2].map(function (c) { return Math.round(MID[c] + (end[c] - MID[c]) * s); });
    };
    var stats0 = { dt: 0, fps: 0, frames: 0, play: 0, wall: 0 };
    Sim.frameStats = stats0;

    /* ---------- reading the dataset ---------- */
    function V(n) { return ds.vars[n]; }
    function A(n) { return V(n).attrs; }
    function sym(n) { return A(n).symbol || n; }
    function digitsOf(n) { var d = A(n).digits; return d === undefined ? 4 : d; }
    function unitOf(n) { return A(n).units || ''; }
    function kindOf(n) { var k = V(n).dims.length; return k === 0 ? 'scalar' : k === 1 ? 'vector' : 'matrix'; }
    function typeLabel(n) { return V(n).dims.length ? 'Array of ' + ds.dtype(n) : V(n).type; }
    function shapeLabel(n) {
        var v = V(n);
        if (!v.dims.length) return A(n).size || '1';
        return '(' + v.dims.map(function (d) { return d + ': ' + (ds.dims[d] || 0); }).join(', ') + ')';
    }
    function rows2(n) { return ds.dims[V(n).dims[0]] || 0; }
    function cols2(n) { return ds.dims[V(n).dims[1]] || 0; }
    function colourFn(n) { return spec.colour && spec.colour[n]; }
    var vars = [];
    spec.groups.forEach(function (g) { g.vars.forEach(function (n) { if (V(n)) vars.push(n); }); });

    /* ---------- the panel ---------- */
    var ICON = '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><rect x="1" y="1.5" width="12" height="11" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>' +
        '<path d="M1 5.2h12M1 8.8h12M5.2 1.5v11" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>';
    var CHK = '<svg width="11" height="11" viewBox="0 0 12 12" aria-hidden="true"><path d="M1.5 6.5l3 3 6-7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';

    var tab = document.createElement('button');
    tab.type = 'button';
    tab.className = 'dp-tab';
    tab.setAttribute('aria-controls', 'data-panel');
    tab.innerHTML = ICON + '<span>Data</span>';

    var panel = document.createElement('aside');
    panel.className = 'dp';
    panel.id = 'data-panel';
    panel.setAttribute('aria-label', 'Simulation data');
    panel.innerHTML =
        '<header class="dp__head"><div class="dp__intro"><p class="dp__kicker">' + esc(spec.kicker || ds.title) + '</p>' +
        '<h2 class="dp__title">' + esc(ds.title) + '</h2><p class="dp__sub">One store. The simulation writes every number here as it computes it; the picture and this table read the same store.</p></div>' +
        '<span class="dp__live">live</span>' +
        '<div class="dp__tools"><button type="button" class="dp__icon" data-save title="Save the data: NumPy .npy files in a zip" aria-label="Save the data">' +
        '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1.5v8M3.8 6.3L7 9.5l3.2-3.2M2 12.5h10" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>' +
        '<button type="button" class="dp__icon dp__close" aria-label="Close the data panel">' +
        '<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M1.5 1.5l9 9M10.5 1.5l-9 9" stroke="currentColor" stroke-width="1.5"/></svg></button></div></header>' +
        '<div class="dp__tabs" role="tablist" aria-label="Data views">' +
        '<button type="button" role="tab" data-tab="vars">Variables <span class="dp__count">' + vars.length + '</span></button>' +
        '<button type="button" role="tab" data-tab="log">Log <span class="dp__count" data-log-count>0</span></button></div>' +
        '<div class="dp__body">' +
        '<section class="dp__pane" data-pane="vars"><div class="dp-probe"><p class="dp-probe__label">Under the pointer</p>' +
        '<p class="dp-probe__hint">Move the pointer over the figure to read the values at that point. The last point stays here.</p>' +
        '<div class="dp-probe__body" hidden><p class="dp-probe__title"></p><table class="dp-probe__table"><tbody></tbody></table></div></div>' +
        '<div class="dp-vars"></div></section>' +
        '<section class="dp__pane dp-arr" data-pane="array" hidden></section>' +
        '<section class="dp__pane dp-check" data-pane="check" hidden></section>' +
        '<section class="dp__pane dp-log" data-pane="log" hidden></section></div>' +
        '<details class="dp-about"><summary>How the numbers and the picture are tied</summary><div class="dp-about__body">' +
        '<p>The simulation keeps its numbers in one named store, a dataset with dimensions, coordinates, variables and units, the same shape of record as a NetCDF or HDF5 file. It writes a value into the store at the moment it computes it. The picture is drawn from the arrays in the store, and this table is repainted from the store after every frame, so both show the same instant.</p>' +
        '<p>What can still differ, and why: the table rounds to a few decimals, the store keeps the full number. ' + (spec.about || '') + ' Press the check mark beside any value to see the stored number, the formula recomputed from the stored inputs, and the read-back from the picture.</p>' +
        '</div></details>';

    document.body.appendChild(tab);
    document.body.appendChild(panel);

    var live = panel.querySelector('.dp__live');
    var panes = {};
    Array.prototype.forEach.call(panel.querySelectorAll('[data-pane]'), function (p) { panes[p.getAttribute('data-pane')] = p; });
    var tabs = panel.querySelectorAll('[data-tab]');
    var varsHost = panes.vars.querySelector('.dp-vars');

    /* ---------- Variables ---------- */
    var rowsHtml = '<table class="dp-table"><thead><tr><th scope="col">Name</th><th scope="col">Type</th><th scope="col">Shape</th><th scope="col">Value</th></tr></thead><tbody>';
    spec.groups.forEach(function (g) {
        rowsHtml += '<tr class="dp-group"><th colspan="4" scope="rowgroup">' + esc(g.title) + (g.note ? '<span>' + g.note + '</span>' : '') + '</th></tr>';
        g.vars.forEach(function (n) {
            if (!V(n)) return;
            var k = kindOf(n), opens = k !== 'scalar', a = A(n);
            rowsHtml += '<tr class="dp-row' + (opens ? ' dp-row--open' : '') + '" data-v="' + esc(n) + '"' + (opens ? ' tabindex="0" title="Open as a table"' : '') + '>' +
                '<td class="dp-name"><span class="dp-sym">' + sym(n) + '</span>' + (a.computed_in ? '<code>' + esc(a.computed_in) + '</code>' : '') +
                (a.long_name ? '<small>' + a.long_name + '</small>' : '') + '</td>' +
                '<td><span class="dp-type dp-type--' + (opens ? 'array' : (V(n).type || 'float').replace(/[^a-z]/gi, '')) + '">' + esc(typeLabel(n)) + '</span></td>' +
                '<td class="dp-size"></td><td class="dp-val"><span class="dp-val__t"></span>' +
                (opens ? '<span class="dp-more" aria-hidden="true">›</span>' : '<button type="button" class="dp-chk" data-check="' + esc(n) + '" title="Check this value">' + CHK + '</button>') + '</td></tr>';
        });
    });
    varsHost.innerHTML = rowsHtml + '</tbody></table>';

    var cells = {};
    vars.forEach(function (n) {
        var tr = varsHost.querySelector('tr[data-v="' + n + '"]');
        cells[n] = { size: tr.querySelector('.dp-size'), val: tr.querySelector('.dp-val__t'), s: null, h: null };
    });

    var statCache = {};
    function stats(n) {
        var v = V(n), c = statCache[n];
        if (c && c.ver === v.version) return c;
        var d = v.data, lo = Infinity, hi = -Infinity, sum = 0, m = d.length;
        for (var p = 0; p < m; p++) { var x = d[p]; if (x < lo) lo = x; if (x > hi) hi = x; sum += x; }
        c = statCache[n] = { ver: v.version, min: m ? lo : NaN, max: m ? hi : NaN, mean: m ? sum / m : NaN };
        return c;
    }
    function describe(n) {
        var k = kindOf(n), d = digitsOf(n), html, x;
        if (k === 'matrix') {
            var st = stats(n);
            html = '<span class="dp-range">' + num(st.min, Math.min(d, 3)) + ' … ' + num(st.max, Math.min(d, 3)) + '</span><small>mean ' + num(st.mean, d) + '</small>';
        } else if (k === 'vector') {
            var arr = V(n).data, parts = [];
            for (var i = 0; i < Math.min(arr.length, 3); i++) parts.push(num(arr[i], d));
            html = '<span class="dp-range">[' + parts.join(', ') + (arr.length > 3 ? ', …' : '') + ']</span>';
        } else if (A(n).colour === true) {
            x = ds.get(n);
            html = x ? '<i class="dp-sw" style="background:rgb(' + x.join(',') + ')"></i>' + x.join(', ') : '—';
        } else {
            x = ds.get(n);
            html = esc(num(x, d)) + (unitOf(n) && x !== undefined && x !== null ? ' <span class="dp-u">' + unitOf(n) + '</span>' : '');
        }
        return { size: shapeLabel(n), html: html };
    }
    function paintVars() {
        vars.forEach(function (n) {
            var d = safe(function () { return describe(n); }, { size: '—', html: '—' }), c = cells[n];
            if (d.size !== c.s) { c.size.textContent = d.size; c.s = d.size; }
            if (d.html !== c.h) { c.val.innerHTML = d.html; c.h = d.html; }
        });
    }

    /* ---------- grid: a table that draws only the cells in view ---------- */
    function makeGrid(host, src, probeEl, onHot) {
        var CW = src.cw || 66, CH = 22, RH = src.rh || 48, HH = 26;
        host.innerHTML = '<div class="dg__top" style="height:' + HH + 'px"><div class="dg__corner" style="flex-basis:' + RH + 'px">' + esc(src.corner) + '</div><div class="dg__cols"></div></div>' +
            '<div class="dg__main"><div class="dg__rows" style="flex-basis:' + RH + 'px"></div><div class="dg__cells"></div></div>';
        var colsEl = host.querySelector('.dg__cols'), rowsEl = host.querySelector('.dg__rows'), cellsEl = host.querySelector('.dg__cells');
        var R = -1, C = -1, win = '', items = [], hot = null;
        function sizeTo(r, c) {
            R = r; C = c;
            colsEl.style.width = cellsEl.style.width = C * CW + 'px';
            rowsEl.style.height = cellsEl.style.height = R * CH + 'px';
        }
        function layout() {
            var sl = host.scrollLeft, st = host.scrollTop;
            var i0 = Math.max(0, Math.floor(sl / CW)), i1 = Math.min(C, Math.ceil((sl + host.clientWidth - RH) / CW) + 1);
            var j0 = Math.max(0, Math.floor(st / CH)), j1 = Math.min(R, Math.ceil((st + host.clientHeight - HH) / CH) + 1);
            var key = [i0, i1, j0, j1, R, C].join();
            if (key === win) return;
            win = key;
            var h = '', i, j;
            for (i = i0; i < i1; i++) h += '<div class="dg__h" style="left:' + i * CW + 'px;width:' + CW + 'px">' + src.colLabel(i) + '</div>';
            colsEl.innerHTML = h;
            h = '';
            for (j = j0; j < j1; j++) h += '<div class="dg__h dg__h--row" style="top:' + j * CH + 'px;height:' + CH + 'px">' + esc(src.rowLabel(j)) + '</div>';
            rowsEl.innerHTML = h;
            h = '';
            for (j = j0; j < j1; j++) {
                for (i = i0; i < i1; i++) {
                    h += '<div class="dg__c" data-j="' + j + '" data-i="' + i + '" style="left:' + i * CW + 'px;top:' + j * CH + 'px;width:' + CW + 'px;height:' + CH + 'px"></div>';
                }
            }
            cellsEl.innerHTML = h;
            items = Array.prototype.map.call(cellsEl.children, function (el) {
                return { el: el, j: +el.getAttribute('data-j'), i: +el.getAttribute('data-i'), t: null, bg: null };
            });
            if (hot) mark(hot.j, hot.i);
        }
        function paint() {
            var r = src.rows(), c = src.cols();
            if (r !== R || c !== C) {
                sizeTo(r, c);
                win = '';
                if (hot && (hot.j >= R || hot.i >= C)) hot = null;
            }
            layout();
            items.forEach(function (it) {
                var v = src.get(it.j, it.i), t = num(v, src.digits(it.i));
                if (t !== it.t) { it.el.textContent = t; it.t = t; }
                var rgb = src.colour ? src.colour(v, it.j, it.i) : null, bg = rgb ? 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')' : '';
                if (bg !== it.bg) { it.el.style.background = bg; it.el.style.color = rgb ? textOn(rgb) : ''; it.bg = bg; }
            });
            if (hot) probeEl.innerHTML = src.probe(hot.j, hot.i, src.get(hot.j, hot.i));
        }
        function mark(j, i) { items.forEach(function (it) { it.el.classList.toggle('is-hot', it.j === j && it.i === i); }); }
        function onPoint(e) {
            var c = e.target.closest && e.target.closest('.dg__c');
            if (!c) return;
            hot = { j: +c.getAttribute('data-j'), i: +c.getAttribute('data-i') };
            mark(hot.j, hot.i);
            probeEl.innerHTML = src.probe(hot.j, hot.i, src.get(hot.j, hot.i));
            if (onHot) onHot(hot.j, hot.i);
        }
        cellsEl.addEventListener('mouseover', onPoint);
        cellsEl.addEventListener('click', onPoint);
        cellsEl.addEventListener('mouseleave', function () { if (onHot) onHot(null); });
        host.addEventListener('scroll', layout, { passive: true });
        var ro = 'ResizeObserver' in window ? new ResizeObserver(function () { win = ''; layout(); }) : null;
        if (ro) ro.observe(host);
        paint();
        return { paint: paint, destroy: function () { if (ro) ro.disconnect(); } };
    }

    var grid = null, current = null, statsEl = null;
    function checkButton(n, idx) {
        return '<button type="button" class="dp-chk dp-chk--text" data-check="' + esc(n) + '" data-idx="' + idx + '">' + CHK + ' Check</button>';
    }
    function gridSource(n) {
        var v = V(n), d = digitsOf(n);
        if (v.dims.length === 1) {
            var dim = v.dims[0], cols = ds.along(dim);
            return {
                cw: 100, corner: dim, rh: 56,
                rows: function () { return ds.dims[dim] || 0; }, cols: function () { return cols.length; },
                get: function (j, i) { var c = V(cols[i]); return c.data ? c.data[j] : undefined; },
                digits: function (i) { return digitsOf(cols[i]); },
                colour: function (x, j, i) { var f = colourFn(cols[i]); return f && typeof x === 'number' ? f(x, j, 0) : null; },
                colLabel: function (i) { return sym(cols[i]) + (unitOf(cols[i]) ? ' · ' + unitOf(cols[i]) : ''); },
                rowLabel: function (j) { var lab = spec.rowLabel && spec.rowLabel[dim]; return lab ? lab(j) : String(j); },
                varAt: function (i) { return cols[i]; },
                probe: function (j, i, x) {
                    var c = cols[i], at = spec.at && spec.at[c];
                    return '<b>' + sym(c) + '[' + j + ']</b> = ' + esc(num(x, digitsOf(c))) + (unitOf(c) ? ' ' + unitOf(c) : '') +
                        checkButton(c, j) + (at ? '<span>' + at(j) + '</span>' : '');
                }
            };
        }
        return {
            cw: A(n).cw, corner: v.dims[0] + ' \\ ' + v.dims[1],
            rows: function () { return rows2(n); }, cols: function () { return cols2(n); },
            get: function (j, i) { return v.data[j * cols2(n) + i]; },
            digits: function () { return d; }, colour: colourFn(n),
            colLabel: function (i) { var lab = spec.colLabel && spec.colLabel[n]; return lab ? lab(i) : String(i); },
            rowLabel: function (j) { var lab = spec.rowLabel && spec.rowLabel[v.dims[0]]; return lab ? lab(j) : String(j); },
            varAt: function () { return n; },
            probe: function (j, i, x) {
                var at = spec.at && spec.at[n];
                return '<b>' + sym(n) + '[' + j + ', ' + i + ']</b> = ' + esc(num(x, d)) + (unitOf(n) ? ' ' + unitOf(n) : '') +
                    checkButton(n, j * cols2(n) + i) + (at ? '<span>' + at(j, i) + '</span>' : '');
            }
        };
    }
    function paintArrStats() {
        if (!current || !statsEl) return;
        var n = current, h, d = digitsOf(n);
        if (kindOf(n) === 'matrix') {
            var st = stats(n);
            h = '<div><dt>shape</dt><dd>' + esc(shapeLabel(n)) + '</dd></div><div><dt>min</dt><dd>' + num(st.min, d) + '</dd></div>' +
                '<div><dt>max</dt><dd>' + num(st.max, d) + '</dd></div><div><dt>mean</dt><dd>' + num(st.mean, d) + '</dd></div>';
        } else {
            var dim = V(n).dims[0];
            h = '<div><dt>length</dt><dd>' + (ds.dims[dim] || 0) + '</dd></div><div class="wide"><dt>variables along ' + esc(dim) + '</dt><dd>' +
                ds.along(dim).map(sym).join(', ') + '</dd></div>';
        }
        if (h !== statsEl._h) { statsEl.innerHTML = h; statsEl._h = h; }
    }
    function openArray(n) {
        if (grid) grid.destroy();
        current = n;
        var a = A(n);
        panes.array.innerHTML =
            '<div class="dp-arr__top"><button type="button" class="dp-back">← All variables</button>' +
            '<div class="dp-arr__title"><span class="dp-sym">' + sym(n) + '</span>' + (a.computed_in ? '<code>' + esc(a.computed_in) + '</code>' : '') +
            '<span class="dp-type dp-type--array">' + esc(typeLabel(n)) + '</span></div>' +
            (a.long_name ? '<p class="dp-arr__mean">' + a.long_name + (a.formula ? ' · <em>' + a.formula + '</em>' : '') + (a.updates ? ' · <em>updates ' + a.updates + '</em>' : '') + '</p>' : '') +
            '<dl class="dp-arr__stats"></dl></div>' +
            '<div class="dg" tabindex="0" aria-label="' + esc(n) + ' as a table"></div>' +
            '<p class="dp-arr__probe">Point at a cell to read its index and value, and to find it in the figure.</p>';
        statsEl = panes.array.querySelector('.dp-arr__stats');
        panes.array.querySelector('.dp-back').addEventListener('click', function () { show('vars'); });
        show('array');
        var src = gridSource(n);
        grid = makeGrid(panes.array.querySelector('.dg'), src, panes.array.querySelector('.dp-arr__probe'), function (j, i) {
            if (j === null) { held.cell = null; return; }
            var name = src.varAt(i), idx = kindOf(n) === 'matrix' ? j * cols2(n) + i : j;
            held.cell = { name: name, idx: idx };
        });
        paintArrStats();
    }
    varsHost.addEventListener('click', function (e) {
        var b = e.target.closest('[data-check]');
        if (b) { openCheck(b.getAttribute('data-check'), 0); return; }
        var tr = e.target.closest('.dp-row--open');
        if (tr) openArray(tr.getAttribute('data-v'));
    });
    varsHost.addEventListener('keydown', function (e) {
        var tr = e.target.closest && e.target.closest('.dp-row--open');
        if (tr && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); openArray(tr.getAttribute('data-v')); }
    });
    panes.array.addEventListener('click', function (e) {
        var b = e.target.closest('[data-check]');
        if (b) openCheck(b.getAttribute('data-check'), +b.getAttribute('data-idx'));
    });

    /* ---------- Check: stored value, recomputed value, read-back from the picture ---------- */
    var checking = null;
    function openCheck(n, idx) {
        checking = { name: n, idx: idx || 0 };
        panes.check.innerHTML = '<div class="dp-arr__top"><button type="button" class="dp-back">← Back</button></div><div class="dp-check__body"></div>';
        panes.check.querySelector('.dp-back').addEventListener('click', function () { show(kindOf(n) === 'scalar' ? 'vars' : (current ? 'array' : 'vars')); });
        show('check');
        paintCheck(true);
    }
    function agreement(stored, value, dtype) {
        if (typeof stored !== 'number' || typeof value !== 'number') return { ok: String(stored) === String(value), text: String(stored) === String(value) ? 'identical' : 'differ' };
        if (!isFinite(stored) || !isFinite(value)) return { ok: String(stored) === String(value), diff: 0, text: String(stored) === String(value) ? 'both undefined now (not applicable)' : 'DIFFER: one is undefined' };
        var diff = Math.abs(stored - value), scale = Math.max(Math.abs(stored), Math.abs(value), 1e-300);
        var tol = (dtype === 'float32' ? 2e-6 : 1e-9) * Math.max(scale, 1e-12) + (dtype === 'float32' ? 1e-7 : 1e-12);
        var ok = diff <= tol, figs = diff === 0 ? '∞' : String(Math.max(0, Math.floor(-Math.log10(diff / scale))));
        return { ok: ok, diff: diff, text: ok ? (diff === 0 ? 'identical' : 'agree to ' + figs + ' significant figures; the rest is ' + (dtype === 'float32' ? 'float32 storage' : 'rounding') + ', difference ' + sci(diff)) : 'DIFFER by ' + sci(diff) };
    }
    function paintCheck(force) {
        if (!checking) return;
        var n = checking.name, idx = checking.idx, v = V(n), a = A(n), d = digitsOf(n), body = panes.check.querySelector('.dp-check__body');
        var stored = v.dims.length ? v.data[idx] : v.data, where = '';
        if (v.dims.length === 2) { var c = cols2(n); where = '[' + Math.floor(idx / c) + ', ' + (idx % c) + ']'; }
        else if (v.dims.length === 1) where = '[' + idx + ']';
        var h = '<div class="dp-check__hd"><span class="dp-sym">' + sym(n) + esc(where) + '</span>' +
            (a.long_name ? '<p>' + a.long_name + '</p>' : '') + '</div>';
        h += '<section class="dp-check__sec"><h4>1 · Stored in the dataset</h4><p class="dp-check__big">' + esc(num(stored, d)) + (unitOf(n) ? ' <span class="dp-u">' + unitOf(n) + '</span>' : '') + '</p>' +
            '<dl class="dp-check__meta"><div><dt>variable</dt><dd>' + esc(n) + ' ' + esc(where) + '</dd></div><div><dt>type</dt><dd>' + esc(typeLabel(n)) + '</dd></div>' +
            (a.computed_in ? '<div><dt>computed in</dt><dd>' + esc(a.computed_in) + '</dd></div>' : '') +
            (a.formula ? '<div class="wide"><dt>formula</dt><dd>' + a.formula + '</dd></div>' : '') +
            (a.updates ? '<div class="wide"><dt>updates</dt><dd>' + esc(a.updates) + '</dd></div>' : '') + '</dl></section>';
        var chk = spec.check && spec.check[n], r = chk ? safe(function () { return chk(idx); }, null) : null;
        h += '<section class="dp-check__sec"><h4>2 · Recomputed now, from the stored inputs</h4>';
        if (r) {
            var ag = agreement(stored, r.value, ds.dtype(n));
            h += (r.formula ? '<p class="dp-check__formula">' + r.formula + '</p>' : '') +
                '<table class="dp-check__in"><tbody>' + (r.inputs || []).map(function (row) {
                    return '<tr><th>' + row[0] + '</th><td>' + esc(typeof row[1] === 'number' ? num(row[1], row[3] === undefined ? 4 : row[3]) : String(row[1])) + '</td><td>' + (row[2] || '') + '</td></tr>';
                }).join('') + '</tbody></table>' +
                '<p class="dp-check__big">' + esc(num(r.value, Math.max(d, 6))) + '</p>' +
                '<p class="dp-check__verdict ' + (ag.ok ? 'is-ok' : 'is-bad') + '">' + (ag.ok ? CHK + ' Stored and recomputed ' : '✕ Stored and recomputed ') + esc(ag.text) + '</p>';
        } else {
            h += '<p class="dp-check__note">' + (a.source ? esc(a.source) : 'No independent formula for this value: it is an input, read from the control.') + '</p>';
        }
        h += '</section>';
        var dr = spec.drawn && spec.drawn[n], rd = dr ? safe(function () { return dr(idx); }, null) : null;
        h += '<section class="dp-check__sec"><h4>3 · Read back from the picture</h4>';
        if (rd) {
            h += '<dl class="dp-check__meta"><div class="wide"><dt>' + esc(rd.what) + '</dt><dd>' + esc(rd.drawn) + '</dd></div>' +
                '<div class="wide"><dt>expected from the store</dt><dd>' + esc(rd.expected) + '</dd></div></dl>' +
                '<p class="dp-check__verdict ' + (rd.ok ? 'is-ok' : 'is-bad') + '">' + (rd.ok ? CHK + ' ' : '✕ ') + esc(rd.ok ? 'The picture shows this value.' : 'The picture does not match.') + '</p>' +
                (rd.note ? '<p class="dp-check__note">' + rd.note + '</p>' : '');
        } else {
            h += '<p class="dp-check__note">' + (a.drawn_note ? a.drawn_note : 'This value is not drawn directly; it enters the picture through the arrays computed from it.') + '</p>';
        }
        h += '</section>';
        if (h !== body._h || force) { body.innerHTML = h; body._h = h; }
    }

    /* ---------- the probe on the figure ---------- */
    var stage = document.getElementById('stage'), held = { ref: null, cell: null }, overlay = null, octx = null, tip = null, pointerIn = false, pointerAt = null;
    var probeBody = panes.vars.querySelector('.dp-probe__body'), probeHint = panes.vars.querySelector('.dp-probe__hint');
    var probeTitle = panes.vars.querySelector('.dp-probe__title'), probeRows = panes.vars.querySelector('.dp-probe__table tbody');
    if (stage && spec.probe && spec.inspect) {
        overlay = document.createElement('canvas');
        overlay.className = 'dp-overlay';
        overlay.setAttribute('aria-hidden', 'true');
        stage.appendChild(overlay);
        octx = overlay.getContext('2d');
        tip = document.createElement('div');
        tip.className = 'dp-tip';
        tip.hidden = true;
        stage.appendChild(tip);
        function fitOverlay() {
            var r = stage.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
            overlay.width = Math.max(1, Math.round(r.width * dpr));
            overlay.height = Math.max(1, Math.round(r.height * dpr));
            octx.setTransform(dpr, 0, 0, dpr, 0, 0);
        }
        fitOverlay();
        if ('ResizeObserver' in window) new ResizeObserver(fitOverlay).observe(stage);
        stage.addEventListener('pointermove', function (e) {
            var r = stage.getBoundingClientRect();
            pointerAt = { x: e.clientX - r.left, y: e.clientY - r.top };
            pointerIn = true;
            var ref = safe(function () { return spec.probe(pointerAt.x, pointerAt.y); }, null);
            if (ref) held.ref = ref;
        });
        stage.addEventListener('pointerleave', function () { pointerIn = false; tip.hidden = true; });
    }
    function drawMark(x, y, strong) {
        octx.beginPath();
        octx.arc(x, y, strong ? 9 : 7, 0, Math.PI * 2);
        octx.strokeStyle = strong ? '#1c1518' : 'rgba(28, 21, 24, 0.55)';
        octx.lineWidth = strong ? 1.8 : 1.2;
        octx.stroke();
        octx.beginPath();
        octx.moveTo(x - 14, y); octx.lineTo(x - 11, y); octx.moveTo(x + 11, y); octx.lineTo(x + 14, y);
        octx.moveTo(x, y - 14); octx.lineTo(x, y - 11); octx.moveTo(x, y + 11); octx.lineTo(x, y + 14);
        octx.stroke();
    }
    function paintProbe() {
        if (!overlay) return;
        var w = overlay.width / Math.min(window.devicePixelRatio || 1, 2), hgt = overlay.height / Math.min(window.devicePixelRatio || 1, 2);
        octx.clearRect(0, 0, w, hgt);
        var info = held.ref ? safe(function () { return spec.inspect(held.ref); }, null) : null;
        if (info && info.at) drawMark(info.at.x, info.at.y, pointerIn);
        if (held.cell && spec.locate) {
            var at = safe(function () { return spec.locate(held.cell.name, held.cell.idx); }, null);
            if (at) {
                octx.beginPath();
                octx.arc(at.x, at.y, 6, 0, Math.PI * 2);
                octx.fillStyle = 'rgba(122, 31, 43, 0.25)';
                octx.fill();
                octx.strokeStyle = '#7a1f2b';
                octx.lineWidth = 1.6;
                octx.stroke();
            }
        }
        if (info && pointerIn && pointerAt) {
            var h = '<b>' + info.title + '</b>' + info.rows.slice(0, 8).map(function (row) {
                return '<span><i>' + row[0] + '</i>' + esc(num(row[1], row[4] !== undefined && V(row[3]) ? digitsOf(row[3]) : 4)) + (row[2] ? ' <u>' + row[2] + '</u>' : '') + '</span>';
            }).join('');
            if (h !== tip._h) { tip.innerHTML = h; tip._h = h; }
            tip.hidden = false;
            var tw = tip.offsetWidth, th = tip.offsetHeight, x = pointerAt.x + 16, y = pointerAt.y + 16;
            if (x + tw > w - 6) x = pointerAt.x - tw - 12;
            if (y + th > hgt - 6) y = pointerAt.y - th - 12;
            tip.style.left = Math.max(4, x) + 'px';
            tip.style.top = Math.max(4, y) + 'px';
        }
        if (info) {
            probeHint.hidden = true;
            probeBody.hidden = false;
            var ph = esc(info.title);
            if (ph !== probeTitle._h) { probeTitle.innerHTML = ph; probeTitle._h = ph; }
            /* the rows are rebuilt only when the set of quantities changes; values are updated in place, so the Check buttons stay clickable */
            var key = info.rows.map(function (row) { return row[0] + '|' + row[3] + '|' + row[4] + '|' + (row[2] || ''); }).join(';');
            if (key !== probeRows._k) {
                probeRows.innerHTML = info.rows.map(function (row) {
                    var n = row[3], idx = row[4];
                    return '<tr><th>' + row[0] + '</th><td><span class="dp-probe__v"></span>' + (row[2] ? ' <span class="dp-u">' + row[2] + '</span>' : '') + '</td><td>' +
                        (n && V(n) ? '<button type="button" class="dp-chk" data-check="' + esc(n) + '" data-idx="' + (idx || 0) + '" title="Check this value">' + CHK + '</button>' : '') + '</td></tr>';
                }).join('');
                probeRows._k = key;
                probeRows._v = Array.prototype.slice.call(probeRows.querySelectorAll('.dp-probe__v'));
            }
            info.rows.forEach(function (row, q) {
                var n = row[3], t = num(row[1], n && V(n) ? digitsOf(n) : 4), el = probeRows._v[q];
                if (el && el.textContent !== t) el.textContent = t;
            });
        }
    }
    panes.vars.querySelector('.dp-probe').addEventListener('click', function (e) {
        var b = e.target.closest('[data-check]');
        if (b) openCheck(b.getAttribute('data-check'), +b.getAttribute('data-idx'));
    });

    /* ---------- Log ---------- */
    var L = spec.log, logBody = null, logWrap = null, logInfo = null, logCount = panel.querySelector('[data-log-count]');
    var total = 0, nextT = 0, lastKey = null, logRows = [];
    if (L) {
        panes.log.innerHTML =
            '<div class="dp-log__bar"><span class="dp-log__info"></span><button type="button" class="dp-btn" data-log-clear>Clear</button></div>' +
            '<div class="dp-log__wrap" tabindex="0" aria-label="Log table"><table class="dp-log__table"><thead><tr><th scope="col">#</th>' +
            L.columns.map(function (n) { return '<th scope="col">' + sym(n) + (unitOf(n) ? '<small>' + unitOf(n) + '</small>' : '') + '</th>'; }).join('') +
            '</tr></thead><tbody></tbody></table></div>';
        logBody = panes.log.querySelector('tbody');
        logWrap = panes.log.querySelector('.dp-log__wrap');
        logInfo = panes.log.querySelector('.dp-log__info');
        panes.log.querySelector('[data-log-clear]').addEventListener('click', function () {
            logBody.innerHTML = '';
            logRows = [];
            total = 0;
            lastKey = null;
            infoLog();
        });
        infoLog();
    }
    function infoLog() {
        var n = logBody ? logBody.rows.length : 0;
        logCount.textContent = n;
        logInfo.textContent = (L.mode === 'change' ? 'one row each time a value changes' : 'one row every ' + L.every + ' s of ' + (L.label || 'play time')) +
            ' · ' + n + ' of ' + grouped(L.max) + ' rows kept';
    }
    function sample() {
        if (!L) return;
        var values = L.columns.map(function (n) { return ds.get(n); });
        var texts = values.map(function (x, i) { return num(x, digitsOf(L.columns[i])); });
        if (L.mode === 'change') {
            var key = texts.filter(function (x, i) { return L.columns[i] !== L.time; }).join('|');
            if (key === lastKey) return;
            lastKey = key;
        } else {
            var every = L.every || 0.1, t = L.time ? ds.get(L.time) : stats0.play;
            if (t < nextT - every) nextT = t;
            if (t < nextT) return;
            nextT = (Math.floor(t / every + 1e-9) + 1) * every;
        }
        total++;
        var stick = logWrap.scrollTop + logWrap.clientHeight >= logWrap.scrollHeight - 24;
        var tr = document.createElement('tr');
        tr.innerHTML = '<th scope="row">' + total + '</th>' + texts.map(function (x) { return '<td>' + esc(x) + '</td>'; }).join('');
        logBody.appendChild(tr);
        logRows.push([total].concat(values.map(function (x) { return typeof x === 'number' ? x : (x === true ? 1 : x === false ? 0 : x); })));
        while (logBody.rows.length > L.max) { logBody.removeChild(logBody.firstChild); logRows.shift(); }
        if (stick) logWrap.scrollTop = logWrap.scrollHeight;
        infoLog();
    }

    /* ---------- Save ---------- */
    function csv() {
        if (!L) return '';
        var head = ['row'].concat(L.columns).join(',');
        return head + '\n' + logRows.map(function (r) { return r.map(function (x) { return typeof x === 'number' ? String(x) : JSON.stringify(x); }).join(','); }).join('\n') + '\n';
    }
    function readme() {
        var base = (spec.file || 'dataset');
        return [
            ds.title + ' · data saved from ' + location.href.replace(/[#?].*$/, ''),
            'Saved ' + new Date().toISOString(),
            '',
            'Each array variable is a NumPy .npy file; dataset.json lists every variable with its dimensions, dtype,',
            'units and attributes, and holds the scalars. log.csv is the Log tab at the time of saving.',
            '',
            'Python:',
            '    import json, zipfile, numpy as np',
            "    z = zipfile.ZipFile('" + base + ".zip')",
            "    meta = json.load(z.open('dataset.json'))",
            "    arrays = {k: np.load(z.open(v['file'])) for k, v in meta['data_vars'].items() if 'file' in v}",
            "    scalars = {k: v['value'] for k, v in meta['data_vars'].items() if 'value' in v}",
            '',
            'With xarray:',
            '    import xarray as xr',
            "    ds = xr.Dataset({k: (meta['data_vars'][k]['dims'], a, meta['data_vars'][k]['attrs']) for k, a in arrays.items()}, attrs=meta['attrs'])",
            ''
        ].join('\n');
    }
    panel.querySelector('[data-save]').addEventListener('click', function () {
        var base = spec.file || 'dataset', stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        var blob = ds.npz([{ name: 'log.csv', bytes: csv() }, { name: 'README.txt', bytes: readme() }]);
        var a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = base + '-' + stamp + '.zip';
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
    });

    /* ---------- open, close, tabs ---------- */
    var isOpen = false, view = 'vars';
    function show(name) {
        view = name;
        Object.keys(panes).forEach(function (k) { panes[k].hidden = k !== name; });
        Array.prototype.forEach.call(tabs, function (b) {
            var on = b.getAttribute('data-tab') === (name === 'log' ? 'log' : 'vars');
            b.setAttribute('aria-selected', on ? 'true' : 'false');
        });
        if (name === 'vars' || name === 'log') store('tab', name);
        if (name === 'log' && logWrap) logWrap.scrollTop = logWrap.scrollHeight;
        paint();
    }
    function setOpen(open, save) {
        isOpen = open;
        document.body.classList.toggle('dp-open', open);
        tab.setAttribute('aria-expanded', open ? 'true' : 'false');
        panel.setAttribute('aria-hidden', open ? 'false' : 'true');
        if (open) panel.removeAttribute('inert'); else panel.setAttribute('inert', '');
        if (save) store('open', open ? '1' : '0');
        if (open) paint();
    }
    tab.addEventListener('click', function () { setOpen(true, true); panel.querySelector('.dp__close').focus(); });
    panel.querySelector('.dp__close').addEventListener('click', function () { setOpen(false, true); tab.focus(); });
    panel.addEventListener('keydown', function (e) { if (e.key === 'Escape') { setOpen(false, true); tab.focus(); } });
    Array.prototype.forEach.call(tabs, function (b) {
        b.addEventListener('click', function () {
            var t = b.getAttribute('data-tab');
            show(t === 'vars' && (view === 'array' || view === 'check') ? view : t);
        });
    });

    function paint() {
        if (!isOpen) return;
        var playing = spec.playing ? safe(spec.playing, false) : true;
        live.classList.toggle('is-live', playing);
        live.textContent = playing ? 'live' : 'paused';
        if (view === 'vars') { paintVars(); }
        else if (view === 'array' && grid) { safe(grid.paint); paintArrStats(); }
        else if (view === 'check') paintCheck(false);
    }

    /* runs after the simulation's own frame callback, so every number is read from the same instant */
    var lastTs = 0, born = 0;
    function frame(ts) {
        var dt = lastTs ? (ts - lastTs) / 1000 : 0;
        if (!born) born = ts;
        lastTs = ts;
        stats0.wall = (ts - born) / 1000;
        if (dt > 0) {
            stats0.frames++;
            stats0.dt = dt;
            stats0.fps = stats0.fps ? stats0.fps + (1 / dt - stats0.fps) * 0.1 : 1 / dt;
            if (safe(spec.playing, true)) stats0.play += Math.min(dt, 0.05);
        }
        safe(sample);
        safe(paintProbe);
        paint();
        requestAnimationFrame(frame);
    }

    var saved = load('open');
    setOpen(saved === null ? window.innerWidth >= 1500 : saved === '1', false);
    show(load('tab') === 'log' && L ? 'log' : 'vars');
    requestAnimationFrame(frame);
})();
