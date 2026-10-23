/* Numa Koudsie · data panel
   A variable explorer in the manner of Spyder's, fed by one store: the page's dataset (scripts/dataset.js).
   The simulation writes every number into that dataset at the moment it computes it; this panel only reads.
   Nothing is recorded unless the reader asks: the panel catches one instant when it opens, records one
   round on request, and repaints every frame only while Live is switched on. When nobody is looking, this
   file does no work at all.

   A page opts in by defining Sim.data next to its own state and loading this file after its own script,
   with styles/data.css in its head.

   Sim.data = {
     ds:         the dataset,
     kicker:     optional heading text; defaults to the dataset title
     rowLabel:   { dimension: function (row) → text }             optional array row headings
     colLabel:   { variable: function (column) → html }            optional 2-D array column headings
     at:         { variable: function (row, column?) → html }     optional array-cell explanation
     playing:    function () → bool;  play: function ()           the page's clock
     groups:     [{ title, note, vars: ['lambda', 'k', ...] }]    names of dataset variables, in display order
     colour:     { psi: function (value, j, i) → [r, g, b] | null } shading for array cells (presentation only)
     probe:      function (xCss, yCss) → ref | null               what lies at a point of the figure (Read values pins it)
     inspect:    function (ref) → { title, at: {x, y}, rows: [[symbol, value, units, varName, index]] }
     locate:     function (varName, index) → {x, y} | null        where an array element is drawn, css px
     check:      { name: function (index) → { formula, inputs: [[symbol, value, units, digits]], value } }
     drawn:      { name: function (index) → { what, drawn, expected, ok, note } }   read-back from the picture
     round:      { label: fn → text, time: varName, length: fn → span of the time variable,
                   columns: [scalar names], point: fn → probe ref, mode: 'change' (optional),
                   blocked: fn → reason | null (optional) }       what one recorded round is
     about:      html                                             what still differs between data and picture
     file:       'fig1-wave-interference'                         base name of the saved archive
   }

   Record      one round of the running simulation, every frame of it caught (at most 600 samples), then
               shown as charts and a table, and saved on request.
   Variables   name, type, shape and value of every dataset variable at one caught instant; Live repaints
               them every frame.
   Read values a switch under the figure: a click or tap pins a point, a drag moves the pin, the marker follows the object,
               and its values sit in a strip under the figure. Off, the figure behaves as if this file were absent.
   Check       for any value: stored value, the formula recomputed from the stored inputs, and the read-back
               from the picture, with the agreement stated.
   Save        a zip of NumPy .npy files, dataset.json, the recorded rounds as CSV and a README. */
(function () {
    'use strict'; var T = window.T || function (s) { return s; };   /* the panel's words on a translated page (sim.js) */
    var Sim = window.Sim, spec = Sim && Sim.data, ds = spec && spec.ds;
    if (!spec || !ds) return;

    /* ---------- helpers ---------- */
    var KEY = 'datapanel.';
    function load(k) { try { return localStorage.getItem(KEY + k); } catch (e) { return null; } }
    function store(k, v) { try { localStorage.setItem(KEY + k, v); } catch (e) { /* storage blocked: the choice lasts for this page */ } }
    function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
    function plain(html) { return String(html).replace(/<sub>(.*?)<\/sub>/g, '_$1').replace(/<sup>(.*?)<\/sup>/g, '^$1').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>'); }
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
    function clock() { var d = new Date(); return [d.getHours(), d.getMinutes(), d.getSeconds()].map(function (x) { return (x < 10 ? '0' : '') + x; }).join(':'); }

    var NEG = [58, 50, 46], MID = [255, 250, 243], POS = [122, 31, 43];
    Sim.colourMap = function (v, lim) {
        var a = lim > 0 ? v / lim : 0;
        if (!(a === a)) a = 0;
        a = a > 1 ? 1 : a < -1 ? -1 : a;
        var s = Math.pow(Math.abs(a), 0.8), end = a < 0 ? NEG : POS;
        return [0, 1, 2].map(function (c) { return Math.round(MID[c] + (end[c] - MID[c]) * s); });
    };
    var TOUCH = !!(window.matchMedia && window.matchMedia('(hover: none)').matches);

    /* ---------- reading the dataset ---------- */
    function V(n) { return ds.vars[n]; }
    function A(n) { return V(n).attrs; }
    function sym(n) { return A(n).symbol || n; }
    function digitsOf(n) { var d = A(n).digits; return d === undefined ? 4 : d; }
    function unitOf(n) { return A(n).units || ''; }
    function kindOf(n) { var k = V(n).dims.length; return k === 0 ? 'scalar' : k === 1 ? 'vector' : 'matrix'; }
    function typeLabel(n) { return V(n).dims.length ? T('array of ') + ds.dtype(n) : V(n).type; }
    function shapeLabel(n) {
        var v = V(n);
        if (!v.dims.length) return 'scalar';
        return v.dims.map(function (d) { return d + ' ' + (ds.dims[d] || 0); }).join(' × ');
    }
    function rows2(n) { return ds.dims[V(n).dims[0]] || 0; }
    function cols2(n) { return ds.dims[V(n).dims[1]] || 0; }
    function colourFn(n) { return spec.colour && spec.colour[n]; }
    function isNumScalar(n) { var v = V(n); return !!v && !v.dims.length && (v.type === 'float' || v.type === 'int' || v.type === 'bool'); }
    var vars = [];
    spec.groups.forEach(function (g) { g.vars.forEach(function (n) { if (V(n)) vars.push(n); }); });

    /* ---------- what one round is: every simulation supplies its round specification ---------- */
    var R = spec.round;
    var TV = R.time && V(R.time) ? R.time : null;
    function timeNow() { var t = TV ? ds.get(TV) : NaN; return typeof t === 'number' && isFinite(t) ? t : performance.now() / 1000; }
    function timeSym() { return TV ? sym(TV) : 't'; }
    function timeUnit() { return TV ? unitOf(TV) : 's'; }
    function timeText(t) { return timeSym() + ' = ' + num(t, 2) + (timeUnit() ? ' ' + timeUnit() : ''); }
    /* the same as HTML: the symbol is already HTML (t<sub>play</sub>), the number and unit are text */
    function timeHTML(t) { return timeSym() + ' = ' + esc(num(t, 2)) + (timeUnit() ? ' ' + esc(timeUnit()) : ''); }
    var roundCols = (R.columns || []).filter(function (n) { return n !== TV && isNumScalar(n); });

    /* ---------- the panel ---------- */
    var ICON = '<svg width="16" height="16" viewBox="0 0 14 14" aria-hidden="true"><rect x="1" y="1.5" width="12" height="11" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>' +
        '<path d="M1 5.2h12M1 8.8h12M5.2 1.5v11" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>';
    var CHK = '<svg width="13" height="13" viewBox="0 0 12 12" aria-hidden="true"><path d="M1.5 6.5l3 3 6-7" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    var SAVE = '<svg width="16" height="16" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1.5v8M3.8 6.3L7 9.5l3.2-3.2M2 12.5h10" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    var REDO = '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M11.5 4.5A5 5 0 1 0 12 8.2" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M12 1.8v3.2H8.8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

    var tab = document.createElement('button');
    tab.type = 'button';
    tab.className = 'dp-tab'; tab.lang = 'en'; tab.dir = 'ltr';   /* the panel's words are English, also on a page in another language */
    tab.setAttribute('aria-controls', 'data-panel');
    tab.innerHTML = ICON + T('<span>Data</span>');
    /* on a phone the pill floats over the page: it steps aside while the reader scrolls down, and comes back on any scroll up */
    var lastY = window.scrollY;
    window.addEventListener('scroll', function () {
        var y = window.scrollY;
        if (Math.abs(y - lastY) < 6) return;
        tab.classList.toggle('dp-tab--away', y > lastY && y > 80);
        lastY = y;
    }, { passive: true });

    var panel = document.createElement('aside');
    panel.className = 'dp';
    panel.id = 'data-panel'; panel.lang = 'en'; panel.dir = 'ltr';
    panel.setAttribute('aria-label', T('Simulation data'));
    panel.innerHTML =
        '<header class="dp__head"><div class="dp__bar"><p class="dp__kicker">' + esc(T(spec.kicker || ds.title)) + '</p>' +
        '<div class="dp__tools"><span class="dp__state" data-state></span>' +
        '<button type="button" class="dp__icon" data-save title="Save the data: NumPy .npy files in a zip" aria-label="Save the data">' + SAVE + '</button>' +
        '<button type="button" class="dp__icon dp__close" aria-label="Close the data panel">' +
        '<svg width="13" height="13" viewBox="0 0 12 12" aria-hidden="true"><path d="M1.5 1.5l9 9M10.5 1.5l-9 9" stroke="currentColor" stroke-width="1.5"/></svg></button></div></div>' +
        '<h2 class="dp__title">' + esc(T(ds.title)) + '<span class="dp__dot">.</span></h2>' +
        T('<p class="dp__sub">Every number the simulation computes lands in one store. Nothing is recorded until you ask.</p></header>') +
        T('<section class="dp-rec" aria-live="polite"><div class="dp-rec__txt"><p class="dp-rec__k">Record one round</p><p class="dp-rec__what"></p>') +
        '<div class="dp-rec__prog" hidden><div class="dp-rec__bar"><i></i></div><p class="dp-rec__st"></p></div></div>' +
        T('<button type="button" class="dp-rec__go" data-rec><span class="dp-rec__dot" aria-hidden="true"></span><span data-rec-label>Record</span></button></section>') +
        '<div class="dp__tabs" role="tablist" aria-label="Data views">' +
        T('<button type="button" role="tab" data-tab="vars">Variables <span class="dp__count">') + vars.length + '</span></button>' +
        T('<button type="button" role="tab" data-tab="rounds">Rounds <span class="dp__count" data-round-count>0</span></button></div>') +
        '<div class="dp__body">' +
        '<section class="dp__pane" data-pane="vars">' +
        '<div class="dp-instant"><p class="dp-instant__t"></p><div class="dp-instant__tools">' +
        '<button type="button" class="dp-btn" data-catch>' + REDO + T(' Catch now</button>') +
        T('<label class="dp-live"><input type="checkbox" data-live><span>Live</span></label></div></div>') +
        T('<div class="dp-probe"><p class="dp-probe__label">Pinned point</p>') +
        T('<p class="dp-probe__hint">Switch on <b>Read values</b> under the figure, then ') + (TOUCH ? 'tap' : 'click') + T(' a point to pin it. Its values appear here and under the figure.</p>') +
        '<div class="dp-probe__body" hidden><p class="dp-probe__title"></p><table class="dp-probe__table"><tbody></tbody></table></div></div>' +
        '<div class="dp-vars"></div></section>' +
        '<section class="dp__pane dp-arr" data-pane="array" hidden></section>' +
        '<section class="dp__pane dp-check" data-pane="check" hidden></section>' +
        '<section class="dp__pane dp-rounds" data-pane="rounds" hidden></section></div>' +
        T('<details class="dp-about"><summary>How the numbers and the picture are tied</summary><div class="dp-about__body">') +
        T('<p>The simulation keeps its numbers in one named store, a dataset with dimensions, coordinates, variables and units, the same shape of record as a NetCDF or HDF5 file. It writes a value into the store at the moment it computes it, every frame, overwriting the previous frame: the store holds one instant, so it never grows. The picture is drawn from the same numbers.</p>') +
        T('<p>This panel reads the store only when you ask. Opening it catches one instant; Catch now catches another; Live repaints every frame, which costs the most. Read values pins one point of the figure and shows its values in a strip under the figure, four times a second. Recording a round copies the scalars and the pinned point at every frame of that round, at most 600 samples, then stops.</p>') +
        T('<p>What can still differ, and why: the table rounds to a few decimals, the store keeps the full number. ') + T(spec.about || '') + T(' Press the check mark beside any value to see the stored number, the formula recomputed from the stored inputs, and the read-back from the picture.</p>') +
        '</div></details>';

    document.body.appendChild(tab);
    document.body.appendChild(panel);

    var stateEl = panel.querySelector('[data-state]');
    var panes = {};
    Array.prototype.forEach.call(panel.querySelectorAll('[data-pane]'), function (p) { panes[p.getAttribute('data-pane')] = p; });
    var tabs = panel.querySelectorAll('[data-tab]');
    var varsHost = panes.vars.querySelector('.dp-vars');
    var instantEl = panes.vars.querySelector('.dp-instant__t');
    var liveBox = panes.vars.querySelector('[data-live]');
    var PAL = null;
    function palette() {
        if (PAL) return PAL;
        var cs = getComputedStyle(panel);
        function tok(n, f) { var v = cs.getPropertyValue(n).trim(); return v || f; }
        PAL = { accent: tok('--accent', '#7a1f2b'), ink: tok('--ink', '#1c1518'), ink3: tok('--ink-3', '#5a504b'), rule: tok('--rule', '#d9d0c2'), muted: tok('--muted', '#8b8079'), soft: tok('--card-soft', '#f7f1e8') };
        return PAL;
    }

    /* ---------- Variables: one caught instant, or live ---------- */
    var html = '';
    spec.groups.forEach(function (g, gi) {
        var items = g.vars.filter(function (n) { return V(n); });
        if (!items.length) return;
        html += '<section class="dp-sec"><header class="dp-sec__hd"><span class="dp-sec__n">' + (gi + 1 < 10 ? '0' : '') + (gi + 1) + '</span><div><h3>' + esc(T(g.title)) + '</h3>' + (g.note ? '<p>' + T(g.note) + '</p>' : '') + '</div></header>';
        items.forEach(function (n) {
            var opens = kindOf(n) !== 'scalar', a = A(n), t = opens ? 'array' : (V(n).type || 'float').replace(/[^a-z]/gi, '');
            html += '<div class="dp-item' + (opens ? T(' dp-item--arr') : '') + '" data-v="' + esc(n) + '"' + (opens ? T(' tabindex="0" role="button" aria-label="Open ') + esc(plain(sym(n))) + T(' as a table"') : '') + '>' +
                '<div class="dp-item__id"><span class="dp-sym">' + sym(n) + '</span>' + (a.long_name ? '<span class="dp-item__name">' + T(a.long_name) + '</span>' : '') + '</div>' +
                '<div class="dp-item__val">' + (opens ? '<canvas class="dp-thumb" aria-hidden="true"></canvas>' : '') + '<span class="dp-item__v"></span></div>' +
                '<div class="dp-item__act">' + (opens ? '<span class="dp-more" aria-hidden="true">›</span>' : '<button type="button" class="dp-chk" data-check="' + esc(n) + T('" aria-label="Check ') + esc(plain(sym(n))) + '" title="Check this value">' + CHK + '</button>') + '</div>' +
                '<div class="dp-item__meta"><span class="dp-type dp-type--' + t + '">' + esc(typeLabel(n)) + '</span><span class="dp-item__shape"></span>' +
                '<code>' + esc(n) + (a.computed_in ? ' · ' + esc(a.computed_in) : '') + '</code></div></div>';
        });
        html += '</section>';
    });
    varsHost.innerHTML = html;

    var cells = {};
    vars.forEach(function (n) {
        var el = varsHost.querySelector('.dp-item[data-v="' + n + '"]');
        cells[n] = { v: el.querySelector('.dp-item__v'), shape: el.querySelector('.dp-item__shape'), thumb: el.querySelector('.dp-thumb'), h: null, s: null, tver: -1, tAt: 0 };
    });

    var statCache = {};
    function stats(n) {
        var v = V(n), c = statCache[n];
        if (c && c.ver === v.version && c.len === (v.data ? v.data.length : 0)) return c;
        var d = v.data || [], lo = Infinity, hi = -Infinity, sum = 0, m = d.length, k = 0;
        for (var p = 0; p < m; p++) { var x = d[p]; if (x === x && isFinite(x)) { if (x < lo) lo = x; if (x > hi) hi = x; sum += x; k++; } }
        c = statCache[n] = { ver: v.version, len: m, min: k ? lo : NaN, max: k ? hi : NaN, mean: k ? sum / k : NaN };
        return c;
    }
    function describe(n) {
        var k = kindOf(n), d = digitsOf(n), x;
        if (k !== 'scalar') {
            var st = stats(n);
            return { shape: shapeLabel(n), html: st.min === st.min ? num(st.min, Math.min(d, 3)) + ' … ' + num(st.max, Math.min(d, 3)) + (unitOf(n) ? ' <span class="dp-u">' + unitOf(n) + '</span>' : '') : 'empty' };
        }
        if (A(n).colour === true) {
            x = ds.get(n);
            return { shape: 'scalar', html: x ? '<i class="dp-sw" style="background:rgb(' + x.join(',') + ')"></i>' + x.join(', ') : '—' };
        }
        x = ds.get(n);
        return { shape: 'scalar', html: esc(num(x, d)) + (unitOf(n) && x !== undefined && x !== null && typeof x !== 'boolean' ? ' <span class="dp-u">' + unitOf(n) + '</span>' : '') };
    }
    /* a small picture of an array: a line for one dimension, a heat map for two; drawn from the same instant as the numbers */
    function drawThumb(n, cv) {
        var v = V(n), d = v.data, dpr = Math.min(window.devicePixelRatio || 1, 2), W = 128, H = 34, P = palette();
        if (cv.width !== W * dpr) { cv.width = W * dpr; cv.height = H * dpr; }
        var c = cv.getContext('2d');
        c.setTransform(dpr, 0, 0, dpr, 0, 0);
        c.clearRect(0, 0, W, H);
        if (!d || !d.length) return;
        var st = stats(n);
        if (v.dims.length === 2) {
            var R2 = rows2(n), C2 = cols2(n);
            if (!R2 || !C2) return;
            var w = Math.min(C2, W * dpr), h = Math.min(R2, H * dpr), img = c.createImageData(w, h), f = colourFn(n), lim = Math.max(Math.abs(st.min), Math.abs(st.max)) || 1;
            for (var y = 0; y < h; y++) {
                var j = Math.min(R2 - 1, Math.floor(y * R2 / h));
                for (var x = 0; x < w; x++) {
                    var i = Math.min(C2 - 1, Math.floor(x * C2 / w)), val = d[j * C2 + i], rgb = (f && safe(function () { return f(val, j, i); }, null)) || Sim.colourMap(val, lim), q = (y * w + x) * 4;
                    img.data[q] = rgb[0]; img.data[q + 1] = rgb[1]; img.data[q + 2] = rgb[2]; img.data[q + 3] = 255;
                }
            }
            var off = document.createElement('canvas');
            off.width = w; off.height = h;
            off.getContext('2d').putImageData(img, 0, 0);
            c.imageSmoothingEnabled = w < W;
            c.drawImage(off, 0, 0, W, H);
            c.strokeStyle = P.rule; c.lineWidth = 1; c.strokeRect(0.5, 0.5, W - 1, H - 1);
            return;
        }
        var lo = st.min, hi = st.max, m = d.length;
        if (!(lo === lo)) return;
        if (hi - lo < 1e-12) { lo -= 1; hi += 1; }
        var pad = 3, sy = function (val) { return H - pad - (val - lo) / (hi - lo) * (H - 2 * pad); };
        if (lo < 0 && hi > 0) { c.strokeStyle = P.rule; c.lineWidth = 1; c.beginPath(); c.moveTo(0, Math.round(sy(0)) + 0.5); c.lineTo(W, Math.round(sy(0)) + 0.5); c.stroke(); }
        c.strokeStyle = P.accent; c.fillStyle = P.accent; c.lineWidth = 1.5; c.lineJoin = 'round';
        if (m === 1) { c.beginPath(); c.arc(W / 2, sy(d[0]), 2.5, 0, Math.PI * 2); c.fill(); return; }
        c.beginPath();
        var started = false;
        for (var p = 0; p < m; p++) {
            var xv = d[p];
            if (!(xv === xv) || !isFinite(xv)) { started = false; continue; }
            var px = p / (m - 1) * (W - 2) + 1, py = sy(xv);
            if (started) c.lineTo(px, py); else { c.moveTo(px, py); started = true; }
        }
        c.stroke();
        if (m <= 24) for (p = 0; p < m; p++) { if (d[p] === d[p]) { c.beginPath(); c.arc(p / (m - 1) * (W - 2) + 1, sy(d[p]), 1.8, 0, Math.PI * 2); c.fill(); } }
    }
    function paintVars(throttle) {
        var now = performance.now();
        vars.forEach(function (n) {
            var d = safe(function () { return describe(n); }, { shape: '—', html: '—' }), c = cells[n];
            if (d.shape !== c.s) { c.shape.textContent = d.shape; c.s = d.shape; }
            if (d.html !== c.h) { c.v.innerHTML = d.html; c.h = d.html; }
            if (c.thumb && V(n).version !== c.tver && (!throttle || now - c.tAt > 250)) {
                safe(function () { drawThumb(n, c.thumb); });
                c.tver = V(n).version;
                c.tAt = now;
            }
        });
    }
    var caught = { t: NaN, why: '' };
    function paintInstant() {
        var t = liveOn ? timeNow() : caught.t, txt;
        if (liveOn) txt = T('<b>Live</b> · ') + timeHTML(t) + T(' · repainted every frame');
        else txt = T('<b>Values at ') + timeHTML(t) + T('</b> · caught ') + esc(caught.why);
        if (txt !== instantEl._h) { instantEl.innerHTML = txt; instantEl._h = txt; }
    }
    function catchNow(why) {
        caught = { t: timeNow(), why: why || T('now, ') + clock() };
        if (view === 'array' && current) { snap = takeSnap(current); paintArray(); }
        if (view === 'check' && checking) runCheck();
        paint(true);
    }

    /* ---------- an array as a table: drawn from a copy taken at one instant, so every cell shows the same frame ---------- */
    function makeGrid(host, src, probeEl, onHot) {
        var CW = src.cw || 74, CH = 28, RH = src.rh || 56, HH = 32;
        host.innerHTML = '<div class="dg__top" style="height:' + HH + 'px"><div class="dg__corner" style="flex-basis:' + RH + 'px">' + esc(src.corner) + '</div><div class="dg__cols"></div></div>' +
            '<div class="dg__main"><div class="dg__rows" style="flex-basis:' + RH + 'px"></div><div class="dg__cells"></div></div>';
        var colsEl = host.querySelector('.dg__cols'), rowsEl = host.querySelector('.dg__rows'), cellsEl = host.querySelector('.dg__cells');
        var Rn = -1, Cn = -1, win = '', items = [], hot = null;
        function sizeTo(r, c) {
            Rn = r; Cn = c;
            colsEl.style.width = cellsEl.style.width = Cn * CW + 'px';
            rowsEl.style.height = cellsEl.style.height = Rn * CH + 'px';
        }
        function layout() {
            var sl = host.scrollLeft, st = host.scrollTop;
            var i0 = Math.max(0, Math.floor(sl / CW)), i1 = Math.min(Cn, Math.ceil((sl + host.clientWidth - RH) / CW) + 1);
            var j0 = Math.max(0, Math.floor(st / CH)), j1 = Math.min(Rn, Math.ceil((st + host.clientHeight - HH) / CH) + 1);
            var key = [i0, i1, j0, j1, Rn, Cn].join();
            if (key === win) return;
            win = key;
            var h = '', i, j;
            for (i = i0; i < i1; i++) h += '<div class="dg__h" style="left:' + i * CW + 'px;width:' + CW + 'px">' + src.colLabel(i) + '</div>';
            colsEl.innerHTML = h;
            h = '';
            for (j = j0; j < j1; j++) h += '<div class="dg__h dg__h--row" style="top:' + j * CH + 'px;height:' + CH + 'px">' + esc(src.rowLabel(j)) + '</div>';
            rowsEl.innerHTML = h;
            h = '';
            for (j = j0; j < j1; j++) for (i = i0; i < i1; i++) h += '<div class="dg__c" data-j="' + j + '" data-i="' + i + '" style="left:' + i * CW + 'px;top:' + j * CH + 'px;width:' + CW + 'px;height:' + CH + 'px"></div>';
            cellsEl.innerHTML = h;
            items = Array.prototype.map.call(cellsEl.children, function (el) { return { el: el, j: +el.getAttribute('data-j'), i: +el.getAttribute('data-i'), t: null, bg: null }; });
            fill();
            if (hot) mark(hot.j, hot.i);
        }
        function fill() {
            items.forEach(function (it) {
                var v = src.get(it.j, it.i), t = num(v, src.digits(it.i));
                if (t !== it.t) { it.el.textContent = t; it.t = t; }
                var rgb = src.colour ? src.colour(v, it.j, it.i) : null, bg = rgb ? 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')' : '';
                if (bg !== it.bg) { it.el.style.background = bg; it.el.style.color = rgb ? textOn(rgb) : ''; it.bg = bg; }
            });
        }
        function paintGrid() {
            var r = src.rows(), c = src.cols();
            if (r !== Rn || c !== Cn) { sizeTo(r, c); win = ''; if (hot && (hot.j >= Rn || hot.i >= Cn)) hot = null; }
            var before = win;
            layout();
            if (win === before) fill();
            if (hot) probeEl.innerHTML = src.probe(hot.j, hot.i, src.get(hot.j, hot.i));
        }
        function mark(j, i) { items.forEach(function (it) { it.el.classList.toggle('is-hot', it.j === j && it.i === i); }); }
        function onPoint(e) {
            var c = e.target.closest && e.target.closest('.dg__c');
            if (!c) return;
            hot = { j: +c.getAttribute('data-j'), i: +c.getAttribute('data-i') };
            mark(hot.j, hot.i);
            probeEl.innerHTML = src.probe(hot.j, hot.i, src.get(hot.j, hot.i));
            if (onHot) onHot(hot.j, hot.i, e.type === 'click');
        }
        cellsEl.addEventListener('mouseover', onPoint);
        cellsEl.addEventListener('click', onPoint);
        cellsEl.addEventListener('mouseleave', function () { if (onHot) onHot(null); });
        host.addEventListener('scroll', layout, { passive: true });
        var ro = 'ResizeObserver' in window ? new ResizeObserver(function () { win = ''; layout(); }) : null;
        if (ro) ro.observe(host);
        paintGrid();
        return { paint: paintGrid, destroy: function () { if (ro) ro.disconnect(); } };
    }

    var grid = null, current = null, statsEl = null, snap = null, snapEl = null;
    function takeSnap(n) {
        var names = kindOf(n) === 'matrix' ? [n] : ds.along(V(n).dims[0]), s = { data: {}, t: timeNow(), R: 0, C: 0 };
        names.forEach(function (m) { var d = V(m).data; s.data[m] = d && d.slice ? d.slice() : d; });
        if (kindOf(n) === 'matrix') { s.R = rows2(n); s.C = cols2(n); } else { s.R = ds.dims[V(n).dims[0]] || 0; s.names = names; }
        return s;
    }
    function snapStats(n) {
        var d = snap.data[n] || [], lo = Infinity, hi = -Infinity, sum = 0, k = 0;
        for (var p = 0; p < d.length; p++) { var x = d[p]; if (x === x && isFinite(x)) { if (x < lo) lo = x; if (x > hi) hi = x; sum += x; k++; } }
        return { min: k ? lo : NaN, max: k ? hi : NaN, mean: k ? sum / k : NaN };
    }
    function checkButton(n, idx) {
        return '<button type="button" class="dp-chk dp-chk--text" data-check="' + esc(n) + '" data-idx="' + idx + '">' + CHK + T(' Check</button>');
    }
    function gridSource(n) {
        var v = V(n), d = digitsOf(n);
        if (v.dims.length === 1) {
            var dim = v.dims[0];
            return {
                cw: 108, corner: dim, rh: 64,
                rows: function () { return snap.R; }, cols: function () { return snap.names.length; },
                get: function (j, i) { var c = snap.data[snap.names[i]]; return c ? c[j] : undefined; },
                digits: function (i) { return digitsOf(snap.names[i]); },
                colour: function (x, j, i) { var f = colourFn(snap.names[i]); return f && typeof x === 'number' ? f(x, j, 0) : null; },
                colLabel: function (i) { var c = snap.names[i]; return sym(c) + (unitOf(c) ? ' · ' + unitOf(c) : ''); },
                rowLabel: function (j) { var lab = spec.rowLabel && spec.rowLabel[dim]; return lab ? lab(j) : String(j); },
                varAt: function (i) { return snap.names[i]; },
                probe: function (j, i, x) {
                    var c = snap.names[i], at = spec.at && spec.at[c];
                    return '<b>' + sym(c) + '[' + j + ']</b> = ' + esc(num(x, digitsOf(c))) + (unitOf(c) ? ' ' + unitOf(c) : '') + checkButton(c, j) + (at ? '<span>' + at(j) + '</span>' : '');
                }
            };
        }
        return {
            cw: A(n).cw ? Math.round(A(n).cw * 1.12) : 74, corner: v.dims[0] + ' \\ ' + v.dims[1],
            rows: function () { return snap.R; }, cols: function () { return snap.C; },
            get: function (j, i) { return snap.data[n][j * snap.C + i]; },
            digits: function () { return d; }, colour: colourFn(n),
            colLabel: function (i) { var lab = spec.colLabel && spec.colLabel[n]; return lab ? lab(i) : String(i); },
            rowLabel: function (j) { var lab = spec.rowLabel && spec.rowLabel[v.dims[0]]; return lab ? lab(j) : String(j); },
            varAt: function () { return n; },
            probe: function (j, i, x) {
                var at = spec.at && spec.at[n];
                return '<b>' + sym(n) + '[' + j + ', ' + i + ']</b> = ' + esc(num(x, d)) + (unitOf(n) ? ' ' + unitOf(n) : '') + checkButton(n, j * snap.C + i) + (at ? '<span>' + at(j, i) + '</span>' : '');
            }
        };
    }
    function paintArray() {
        if (!current || !snap) return;
        var n = current, h, d = digitsOf(n);
        if (kindOf(n) === 'matrix') {
            var st = snapStats(n);
            h = T('<div><dt>shape</dt><dd>') + snap.R + ' × ' + snap.C + T('</dd></div><div><dt>min</dt><dd>') + num(st.min, d) + '</dd></div>' +
                T('<div><dt>max</dt><dd>') + num(st.max, d) + T('</dd></div><div><dt>mean</dt><dd>') + num(st.mean, d) + '</dd></div>';
        } else {
            h = T('<div><dt>length</dt><dd>') + snap.R + T('</dd></div><div class="wide"><dt>variables along ') + esc(V(n).dims[0]) + '</dt><dd>' + snap.names.map(sym).join(', ') + '</dd></div>';
        }
        if (h !== statsEl._h) { statsEl.innerHTML = h; statsEl._h = h; }
        var st2 = liveOn ? T('<b>Live</b> · ') + timeHTML(snap.t) : T('<b>Copied at ') + timeHTML(snap.t) + T('</b> · every cell shows this one frame');
        if (st2 !== snapEl._h) { snapEl.innerHTML = st2; snapEl._h = st2; }
        if (grid) safe(grid.paint);
    }
    function openArray(n) {
        if (grid) grid.destroy();
        current = n;
        snap = takeSnap(n);
        var a = A(n);
        panes.array.innerHTML =
            T('<div class="dp-arr__top"><button type="button" class="dp-back">← All variables</button>') +
            '<div class="dp-arr__title"><span class="dp-sym">' + sym(n) + '</span><span class="dp-type dp-type--array">' + esc(typeLabel(n)) + '</span></div>' +
            (a.long_name ? '<p class="dp-arr__mean">' + T(a.long_name) + (a.formula ? ' · <em>' + a.formula + '</em>' : '') + '</p>' : '') +
            '<dl class="dp-arr__stats"></dl><div class="dp-arr__snap"><p class="dp-arr__when"></p><button type="button" class="dp-btn" data-catch>' + REDO + T(' Copy again</button></div></div>') +
            '<div class="dg" tabindex="0" aria-label="' + esc(n) + ' as a table"></div>' +
            '<p class="dp-arr__probe">' + (TOUCH ? T('Tap a cell to read its index and value, and to find it in the figure.') : T('Point at a cell to read its index and value, and to find it in the figure.')) + '</p>';
        statsEl = panes.array.querySelector('.dp-arr__stats');
        snapEl = panes.array.querySelector('.dp-arr__when');
        panes.array.querySelector('.dp-back').addEventListener('click', function () { show('vars'); });
        show('array');
        var src = gridSource(n);
        grid = makeGrid(panes.array.querySelector('.dg'), src, panes.array.querySelector('.dp-arr__probe'), function (j, i, tapped) {
            if (j === null) { held.cell = null; probe.cellUntil = 0; return; }
            held.cell = { name: src.varAt(i), idx: kindOf(n) === 'matrix' ? j * snap.C + i : j };
            probe.cellUntil = performance.now() + (tapped ? 3000 : 600);
            kick();
        });
        paintArray();
    }
    varsHost.addEventListener('click', function (e) {
        var b = e.target.closest('[data-check]');
        if (b) { openCheck(b.getAttribute('data-check'), 0); return; }
        var it = e.target.closest('.dp-item--arr');
        if (it) openArray(it.getAttribute('data-v'));
    });
    varsHost.addEventListener('keydown', function (e) {
        var it = e.target.closest && e.target.closest('.dp-item--arr');
        if (it && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); openArray(it.getAttribute('data-v')); }
    });
    panes.array.addEventListener('click', function (e) {
        var b = e.target.closest('[data-check]');
        if (b) { openCheck(b.getAttribute('data-check'), +b.getAttribute('data-idx')); return; }
        if (e.target.closest('[data-catch]')) { snap = takeSnap(current); paintArray(); }
    });

    /* ---------- Check: stored value, recomputed value, read-back from the picture, all at one instant ---------- */
    var checking = null;
    function openCheck(n, idx) {
        checking = { name: n, idx: idx || 0 };
        panes.check.innerHTML = T('<div class="dp-arr__top dp-check__top"><button type="button" class="dp-back">← Back</button>') +
            '<button type="button" class="dp-btn" data-recheck>' + REDO + T(' Check again</button></div><div class="dp-check__body"></div>');
        panes.check.querySelector('.dp-back').addEventListener('click', function () { show(kindOf(n) === 'scalar' ? 'vars' : (current ? 'array' : 'vars')); });
        panes.check.querySelector('[data-recheck]').addEventListener('click', runCheck);
        show('check');
        runCheck();
    }
    function agreement(stored, value, dtype) {
        if (typeof stored !== 'number' || typeof value !== 'number') return { ok: String(stored) === String(value), text: String(stored) === String(value) ? 'identical' : 'differ' };
        if (!isFinite(stored) || !isFinite(value)) return { ok: String(stored) === String(value), diff: 0, text: String(stored) === String(value) ? T('both undefined now (not applicable)') : T('DIFFER: one is undefined') };
        var diff = Math.abs(stored - value), scale = Math.max(Math.abs(stored), Math.abs(value), 1e-300);
        var tol = (dtype === 'float32' ? 2e-6 : 1e-9) * Math.max(scale, 1e-12) + (dtype === 'float32' ? 1e-7 : 1e-12);
        var ok = diff <= tol, figs = diff === 0 ? '∞' : String(Math.max(0, Math.floor(-Math.log10(diff / scale))));
        return { ok: ok, diff: diff, text: ok ? (diff === 0 ? 'identical' : T('agree to ') + figs + T(' significant figures; the rest is ') + (dtype === 'float32' ? 'float32 storage' : 'rounding') + T(', difference ') + sci(diff)) : T('DIFFER by ') + sci(diff) };
    }
    function runCheck() {
        if (!checking) return;
        var n = checking.name, idx = checking.idx, v = V(n), a = A(n), d = digitsOf(n), body = panes.check.querySelector('.dp-check__body');
        var stored = v.dims.length ? v.data[idx] : v.data, where = '', t = timeNow();
        if (v.dims.length === 2) { var c = cols2(n); where = '[' + Math.floor(idx / c) + ', ' + (idx % c) + ']'; }
        else if (v.dims.length === 1) where = '[' + idx + ']';
        var h = '<div class="dp-check__hd"><span class="dp-sym">' + sym(n) + esc(where) + '</span>' + (a.long_name ? '<p>' + T(a.long_name) + '</p>' : '') +
            T('<p class="dp-check__when">Checked at ') + timeHTML(t) + ', ' + clock() + T('. All three answers below come from this one frame.</p></div>');
        h += T('<section class="dp-check__sec"><h4><span>1</span>Stored in the dataset</h4><p class="dp-check__big">') + esc(num(stored, d)) + (unitOf(n) ? ' <span class="dp-u">' + unitOf(n) + '</span>' : '') + '</p>' +
            T('<dl class="dp-check__meta"><div><dt>variable</dt><dd>') + esc(n) + ' ' + esc(where) + T('</dd></div><div><dt>type</dt><dd>') + esc(typeLabel(n)) + '</dd></div>' +
            (a.computed_in ? T('<div><dt>computed in</dt><dd>') + esc(a.computed_in) + '</dd></div>' : '') +
            (a.updates ? T('<div><dt>updates</dt><dd>') + esc(a.updates) + '</dd></div>' : '') +
            (a.formula ? T('<div class="wide"><dt>formula</dt><dd>') + a.formula + '</dd></div>' : '') + '</dl></section>';
        var chk = spec.check && spec.check[n], r = chk ? safe(function () { return chk(idx); }, null) : null;
        h += T('<section class="dp-check__sec"><h4><span>2</span>Recomputed now, from the stored inputs</h4>');
        if (r) {
            var ag = agreement(stored, r.value, ds.dtype(n));
            h += (r.formula ? '<p class="dp-check__formula">' + r.formula + '</p>' : '') +
                '<table class="dp-check__in"><tbody>' + (r.inputs || []).map(function (row) {
                    return '<tr><th>' + row[0] + '</th><td>' + esc(typeof row[1] === 'number' ? num(row[1], row[3] === undefined ? 4 : row[3]) : String(row[1])) + '</td><td>' + (row[2] || '') + '</td></tr>';
                }).join('') + '</tbody></table>' +
                '<p class="dp-check__big">' + esc(num(r.value, Math.max(d, 6))) + '</p>' +
                '<p class="dp-check__verdict ' + (ag.ok ? 'is-ok' : 'is-bad') + '">' + (ag.ok ? CHK + T(' Stored and recomputed ') : T('✕ Stored and recomputed ')) + esc(ag.text) + '</p>';
        } else {
            h += '<p class="dp-check__note">' + (a.source ? esc(a.source) : T('No independent formula for this value: it is an input, read from the control.')) + '</p>';
        }
        h += '</section>';
        var dr = spec.drawn && spec.drawn[n], rd = dr ? safe(function () { return dr(idx); }, null) : null;
        h += T('<section class="dp-check__sec"><h4><span>3</span>Read back from the picture</h4>');
        if (rd) {
            h += '<dl class="dp-check__meta"><div class="wide"><dt>' + esc(rd.what) + '</dt><dd>' + esc(rd.drawn) + '</dd></div>' +
                T('<div class="wide"><dt>expected from the store</dt><dd>') + esc(rd.expected) + '</dd></div></dl>' +
                '<p class="dp-check__verdict ' + (rd.ok === null ? 'is-na' : rd.ok ? 'is-ok' : 'is-bad') + '">' + (rd.ok === null ? '' : rd.ok ? CHK + ' ' : '✕ ') + esc(rd.ok === null ? T('Not in the picture at the moment, so there is nothing to read back.') : rd.ok ? T('The picture shows this value.') : T('The picture does not match.')) + '</p>' +
                (rd.note ? '<p class="dp-check__note">' + rd.note + '</p>' : '');
        } else {
            h += '<p class="dp-check__note">' + (a.drawn_note ? a.drawn_note : T('This value is not drawn directly; it enters the picture through the arrays computed from it.')) + '</p>';
        }
        h += '</section>';
        body.innerHTML = h;
    }

    /* ---------- Read values: a tool the reader switches on, as in MATLAB's data cursor and PhET's probes.
       Off, the figure behaves exactly as without this file. On, a click or tap pins the object under it, a drag moves the pin,
       the marker follows the object every frame, and its values sit in a strip under the figure, rewritten four times a second.
       Crossing the figure with the pointer shows nothing; a pause of 0.3 s while Read is on outlines what a click would pin. ---------- */
    var stage = document.getElementById('stage'), held = { ref: null, cell: null }, overlay = null, octx = null, strip = null, readBtn = null;
    var probe = { on: false, pinned: false, dragging: false, hover: null, preview: null, dwell: 0, cellUntil: 0, marked: false, shownAt: 0, lastEnd: 0, empty: false };
    var probeBody = panes.vars.querySelector('.dp-probe__body'), probeHint = panes.vars.querySelector('.dp-probe__hint');
    var probeTitle = panes.vars.querySelector('.dp-probe__title'), probeRows = panes.vars.querySelector('.dp-probe__table tbody');
    var stripHint = null, stripPin = null, stripTitle = null, stripVals = null;
    var CROSS = '<svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="4.2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 0.8v3.2M8 12v3.2M0.8 8h3.2M12 8h3.2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
    function stageXY(e) { var r = stage.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
    /* a finger is wide and many objects move: when nothing lies exactly at the point, look on two rings around it, 12 and 22 px out */
    function refAt(at, finger) {
        var ref = safe(function () { return spec.probe(at.x, at.y); }, null);
        for (var r = 12; !ref && finger && r <= 22; r += 10) {
            for (var k = 0; k < 8 && !ref; k++) { var a = k * Math.PI / 4; ref = safe(function () { return spec.probe(at.x + r * Math.cos(a), at.y + r * Math.sin(a)); }, null); }
        }
        return ref;
    }
    function setRead(on) {
        probe.on = on;
        probe.pinned = false; probe.dragging = false; probe.preview = null; probe.empty = false;
        clearTimeout(probe.dwell);
        if (readBtn) { readBtn.setAttribute('aria-pressed', on ? 'true' : 'false'); readBtn.lastChild.textContent = on ? T(' Reading · stop') : T(' Read values'); }
        if (stage) stage.classList.toggle('dp-reading', on);
        if (strip) strip.hidden = !on;
        paintStrip();
        kick();
    }
    if (stage && spec.probe && spec.inspect) {
        overlay = document.createElement('canvas');
        overlay.className = 'dp-overlay';
        overlay.setAttribute('aria-hidden', 'true');
        stage.appendChild(overlay);
        octx = overlay.getContext('2d');
        /* the strip lives under the figure, between it and its caption, so it never covers what it describes */
        strip = document.createElement('div');
        strip.className = 'dp-read'; strip.lang = 'en'; strip.dir = 'ltr';
        strip.hidden = true;
        strip.setAttribute('aria-live', 'polite');
        strip.innerHTML = '<p class="dp-read__hint">' + (TOUCH ? T('Tap a point in the figure to pin it; drag to move the pin.') : T('Click a point in the figure to pin it; drag to move the pin. Esc stops reading.')) + '</p>' +
            '<div class="dp-read__pin" hidden><p class="dp-read__title"></p><div class="dp-read__vals"></div></div>';
        stage.insertAdjacentElement('afterend', strip);
        stripHint = strip.querySelector('.dp-read__hint'); stripPin = strip.querySelector('.dp-read__pin');
        stripTitle = strip.querySelector('.dp-read__title'); stripVals = strip.querySelector('.dp-read__vals');
        readBtn = document.createElement('button');
        readBtn.type = 'button';
        readBtn.className = 'dp-readbtn'; readBtn.lang = 'en';
        readBtn.setAttribute('aria-pressed', 'false');
        readBtn.title = T('Pin a point of the figure and read its values');
        readBtn.innerHTML = CROSS + T('<span> Read values</span>');
        var cap = stage.parentNode && stage.parentNode.querySelector('.stage__cap');
        if (cap) cap.appendChild(readBtn); else strip.insertAdjacentElement('beforebegin', readBtn);
        readBtn.addEventListener('click', function () { setRead(!probe.on); });
        strip.addEventListener('click', function (e) {
            var b = e.target.closest('[data-check]');
            if (b) { if (!isOpen) setOpen(true, true); openCheck(b.getAttribute('data-check'), +b.getAttribute('data-idx')); }
        });
        var fitOverlay = function () {
            var r = stage.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
            overlay.width = Math.max(1, Math.round(r.width * dpr));
            overlay.height = Math.max(1, Math.round(r.height * dpr));
            octx.setTransform(dpr, 0, 0, dpr, 0, 0);
            dirty = [];
            if (probe.marked || probe.pinned) kick();
        };
        fitOverlay();
        if ('ResizeObserver' in window) new ResizeObserver(fitOverlay).observe(stage);
        var pinAt = function (at, finger) {
            var ref = refAt(at, finger);
            probe.empty = !ref;
            if (ref) { held.ref = ref; probe.pinned = true; }
            else if (!probe.dragging || !probe.pinned) probe.pinned = false;
            probe.preview = null;
            paintStrip();
            kick();
        };
        /* capture phase: while Read is on, the gesture belongs to the reading, and the page's own click, draw or pan does not run */
        var own = function (e) { if (probe.on) { e.stopPropagation(); return true; } return false; };
        stage.addEventListener('pointerdown', function (e) {
            if (!own(e)) return;
            if (e.button > 0) return;
            probe.dragging = true;
            if (stage.setPointerCapture) safe(function () { stage.setPointerCapture(e.pointerId); });
            pinAt(stageXY(e), true);
        }, true);
        stage.addEventListener('pointermove', function (e) {
            if (!own(e)) return;
            if (probe.dragging) { pinAt(stageXY(e), true); return; }
            if (e.pointerType !== 'mouse') return;
            /* moving: no outline; resting 0.3 s: outline what a click would pin */
            probe.hover = stageXY(e);
            if (probe.preview) { probe.preview = null; kick(); }
            clearTimeout(probe.dwell);
            probe.dwell = setTimeout(function () { if (probe.on && probe.hover) { probe.preview = refAt(probe.hover, true); kick(); } }, 300);
        }, true);
        var up = function (e) { if (!own(e)) return; probe.dragging = false; probe.lastEnd = performance.now(); };
        stage.addEventListener('pointerup', up, true);
        stage.addEventListener('pointercancel', up, true);
        stage.addEventListener('pointerleave', function () { probe.hover = null; clearTimeout(probe.dwell); if (probe.preview) { probe.preview = null; kick(); } });
        ['click', 'mousedown', 'mouseup', 'dblclick', 'contextmenu'].forEach(function (t) { stage.addEventListener(t, function (e) { if (probe.on) { e.stopPropagation(); if (t !== 'mousedown') e.preventDefault(); } }, true); });
        document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && probe.on) setRead(false); });
    }
    var dirty = [];
    function touched(x, y, r) { dirty.push([x - r - 3, y - r - 3, 2 * r + 6]); }
    function wipe() {
        if (dirty.length > 6) { var dpr = Math.min(window.devicePixelRatio || 1, 2); octx.clearRect(0, 0, overlay.width / dpr, overlay.height / dpr); }
        else dirty.forEach(function (d) { octx.clearRect(d[0], d[1], d[2], d[2]); });
        dirty = [];
    }
    function drawRing(x, y, r, colour, width) { octx.beginPath(); octx.arc(x, y, r, 0, Math.PI * 2); octx.strokeStyle = colour; octx.lineWidth = width; octx.stroke(); touched(x, y, r + width); }
    function drawPin(x, y) {
        drawRing(x, y, 11, 'rgba(255, 250, 243, 0.9)', 4);
        drawRing(x, y, 11, '#7a1f2b', 2);
        octx.beginPath();
        octx.moveTo(x - 18, y); octx.lineTo(x - 13, y); octx.moveTo(x + 13, y); octx.lineTo(x + 18, y);
        octx.moveTo(x, y - 18); octx.lineTo(x, y - 13); octx.moveTo(x, y + 13); octx.lineTo(x, y + 18);
        octx.strokeStyle = '#7a1f2b'; octx.lineWidth = 2; octx.stroke();
        touched(x, y, 19);
    }
    function clearOverlay() {
        if (!overlay || !probe.marked) return;
        wipe();
        probe.marked = false;
    }
    /* the marker is drawn every frame so it stays on the moving object; the words are rewritten at most four times a second */
    function paintProbe() {
        if (!overlay) return;
        wipe();
        probe.marked = false;
        if (probe.on && probe.preview) {
            var pv = safe(function () { return spec.inspect(probe.preview); }, null);
            if (pv && pv.at) { drawRing(pv.at.x, pv.at.y, 9, 'rgba(28, 21, 24, 0.55)', 1.4); probe.marked = true; }
        }
        if (probe.on && probe.pinned && held.ref) {
            var info = safe(function () { return spec.inspect(held.ref); }, null);
            if (info && info.at) { drawPin(info.at.x, info.at.y); probe.marked = true; }
        }
        if (held.cell && spec.locate && performance.now() < probe.cellUntil) {
            var at = safe(function () { return spec.locate(held.cell.name, held.cell.idx); }, null);
            if (at) {
                octx.beginPath();
                octx.arc(at.x, at.y, 7, 0, Math.PI * 2);
                octx.fillStyle = 'rgba(122, 31, 43, 0.25)';
                octx.fill();
                drawRing(at.x, at.y, 7, '#7a1f2b', 1.8);
                probe.marked = true;
            }
        }
        if (performance.now() - probe.shownAt > 250) paintStrip();
    }
    function rowsKey(rows) { return rows.map(function (row) { return row[0] + '|' + row[3] + '|' + row[4] + '|' + (row[2] || ''); }).join(';'); }
    function paintStrip() {
        probe.shownAt = performance.now();
        var info = held.ref ? safe(function () { return spec.inspect(held.ref); }, null) : null, t = timeHTML(timeNow());
        if (strip && probe.on) {
            var showPin = probe.pinned && info;
            stripPin.hidden = !showPin;
            stripHint.hidden = !!showPin;
            if (!showPin && probe.empty) stripHint.textContent = T('Nothing to pin there. ') + (TOUCH ? T('Tap') : T('Click')) + T(' on something drawn in the figure.');
            else if (!showPin) stripHint.textContent = TOUCH ? T('Tap a point in the figure to pin it; drag to move the pin.') : T('Click a point in the figure to pin it; drag to move the pin. Esc stops reading.');
            if (showPin) {
                var th = T(info.title) + ' <span>· ' + t + '</span>';
                if (th !== stripTitle._h) { stripTitle.innerHTML = th; stripTitle._h = th; }
                var key = rowsKey(info.rows);
                if (key !== stripVals._k) {
                    stripVals.innerHTML = info.rows.map(function (row) {
                        var n = row[3], ok = n && V(n);
                        return '<' + (ok ? T('button type="button" data-check="') + esc(n) + '" data-idx="' + (row[4] || 0) + T('" title="Check this value"') : 'span') + ' class="dp-read__v"><i>' + row[0] + '</i><b></b>' + (row[2] ? '<u>' + row[2] + '</u>' : '') + '</' + (ok ? 'button' : 'span') + '>';
                    }).join('');
                    stripVals._k = key;
                    stripVals._v = Array.prototype.slice.call(stripVals.querySelectorAll('b'));
                }
                info.rows.forEach(function (row, q) {
                    var n = row[3], txt = num(row[1], n && V(n) ? digitsOf(n) : 4), el = stripVals._v[q];
                    if (el && el.textContent !== txt) el.textContent = txt;
                });
            }
        }
        if (info && isOpen) {
            probeHint.hidden = true;
            probeBody.hidden = false;
            var ph = T(info.title) + ' <span>· ' + t + (probe.on && probe.pinned ? '' : T(' · last pinned')) + '</span>';
            if (ph !== probeTitle._h) { probeTitle.innerHTML = ph; probeTitle._h = ph; }
            var k2 = rowsKey(info.rows);
            if (k2 !== probeRows._k) {
                probeRows.innerHTML = info.rows.map(function (row) {
                    var n = row[3], idx = row[4];
                    return '<tr><th>' + row[0] + '</th><td><span class="dp-probe__v"></span>' + (row[2] ? ' <span class="dp-u">' + row[2] + '</span>' : '') + '</td><td>' +
                        (n && V(n) ? '<button type="button" class="dp-chk" data-check="' + esc(n) + '" data-idx="' + (idx || 0) + '" aria-label="Check" title="Check this value">' + CHK + '</button>' : '') + '</td></tr>';
                }).join('');
                probeRows._k = k2;
                probeRows._v = Array.prototype.slice.call(probeRows.querySelectorAll('.dp-probe__v'));
            }
            info.rows.forEach(function (row, q) {
                var n = row[3], txt = num(row[1], n && V(n) ? digitsOf(n) : 4), el = probeRows._v[q];
                if (el && el.textContent !== txt) el.textContent = txt;
            });
        }
    }
    panes.vars.querySelector('.dp-probe').addEventListener('click', function (e) {
        var b = e.target.closest('[data-check]');
        if (b) openCheck(b.getAttribute('data-check'), +b.getAttribute('data-idx'));
    });

    /* ---------- Rounds: record one round of the running simulation, every frame, then stop ---------- */
    var MAXS = 600, rounds = [], roundNo = 0, rec = null, sel = -1;
    var recBox = panel.querySelector('.dp-rec'), recWhat = recBox.querySelector('.dp-rec__what'), recProg = recBox.querySelector('.dp-rec__prog');
    var recBar = recBox.querySelector('.dp-rec__bar i'), recSt = recBox.querySelector('.dp-rec__st'), recBtn = recBox.querySelector('[data-rec]'), recLab = recBox.querySelector('[data-rec-label]');
    var roundCount = panel.querySelector('[data-round-count]');
    function roundLength() { var len = +safe(R.length, 10); return len > 0 && isFinite(len) ? len : 10; }
    function describeRound() {
        if (rec) return;
        var lab = safe(R.label, '') || 'ten seconds of play';
        var txt = T('One round = <b>') + lab + T('</b>.<span class="dp-more-txt"> Every frame of it is caught') + (spec.inspect ? T(', with ') + (held.ref ? 'the point you pinned' : T('a point the page chooses; pin another with Read values')) : '') + T('; then the recording stops by itself.</span>');
        var why = R.blocked ? safe(R.blocked, null) : null;
        if (why) txt += T(' <span class="dp-rec__why"><b>Not now.</b> ') + esc(why) + '</span>';
        if (txt !== recWhat._h) { recWhat.innerHTML = txt; recWhat._h = txt; }
    }
    function scalarNames() { return ds.order.filter(isNumScalar); }
    function startRound() {
        if (rec) { finishRound('stopped early'); return; }
        var why = R.blocked ? safe(R.blocked, null) : null;
        if (why) { recWhat.innerHTML = T('<b>Not now.</b> ') + esc(why); recWhat._h = null; return; }
        if (spec.play && spec.playing && !safe(spec.playing, true)) safe(spec.play);
        var ref = held.ref || (R.point ? safe(R.point, null) : null), info = ref ? safe(function () { return spec.inspect(ref); }, null) : null;
        var names = scalarNames();
        rec = {
            no: roundNo + 1, len: roundLength(), label: safe(R.label, '') || 'ten seconds of play', mode: R.mode, ref: info ? ref : null,
            pointTitle: info ? info.title : '', pointRows: info ? info.rows.map(function (row) { return { label: row[0], units: row[2] || '', name: row[3], idx: row[4], key: row[0] + '|' + row[3] }; }) : [],   /* the key leaves out the index: a followed point moves through a stored run */
            names: names, t0: null, lastEl: -Infinity, key: null, n: 0, frames: 0, wall0: performance.now(),
            buf: { __t: [], __el: [] }, params: (spec.groups[0] ? spec.groups[0].vars : []).filter(isNumScalar).map(function (n) { return [n, ds.get(n)]; })
        };
        names.forEach(function (n) { rec.buf[n] = []; });
        rec.pointRows.forEach(function (pr, k) { rec.buf['__p' + k] = []; });
        rec.interval = rec.mode === 'change' ? 0 : rec.len / MAXS;
        recBox.classList.add('is-rec');
        recLab.textContent = T('Stop');
        recProg.hidden = false;
        recWhat.innerHTML = T('Recording <b>round ') + rec.no + '</b>: ' + esc(rec.label) + (rec.pointTitle ? T('<span class="dp-more-txt">, following ') + rec.pointTitle + '</span>' : '') + '.';
        recWhat._h = null;
        progress(0, 0);
        kick();
    }
    function progress(frac, el) {
        recBar.style.width = (100 * Math.max(0, Math.min(1, frac))) + '%';
        var paused = spec.playing && !safe(spec.playing, true) && rec && rec.mode !== 'change';
        var blocked = rec && R.blocked ? safe(R.blocked, null) : null;
        recSt.innerHTML = blocked ? T('<b>Waiting.</b> ') + esc(blocked) : paused ? T('<b>Paused.</b> Press Play: the round goes on when the simulation does.') :
            rec.mode === 'change' ? num(el, 1) + T(' of ') + num(rec.len, 0) + ' s · ' + rec.n + T(' changes caught · move a slider') :
            num(el, 2) + T(' of ') + num(rec.len, 2) + (timeUnit() ? ' ' + timeUnit() : '') + ' · ' + rec.n + T(' samples');
    }
    function recordFrame() {
        if (!rec) return;
        var t = timeNow();
        if (rec.t0 === null) rec.t0 = t;
        var el = t - rec.t0, take;
        if (el < -1e-9) { finishRound('the clock was reset'); return; }
        rec.frames++;
        if (rec.mode === 'change') {
            var key = roundCols.map(function (n) { return String(ds.get(n)); }).join('|');
            take = key !== rec.key;
            rec.key = key;
        } else take = rec.n === 0 || el - rec.lastEl >= rec.interval * 0.999 || el >= rec.len - 1e-9;
        /* Reserve the last sample for the frame that ends a sampled round. */
        if (take && rec.n < MAXS && (rec.mode === 'change' || rec.n < MAXS - 1 || el >= rec.len - 1e-9)) {
            rec.buf.__t.push(t); rec.buf.__el.push(el);
            rec.names.forEach(function (n) { var x = ds.get(n); rec.buf[n].push(typeof x === 'boolean' ? (x ? 1 : 0) : typeof x === 'number' ? x : NaN); });
            if (rec.pointRows.length) {
                var info = safe(function () { return spec.inspect(rec.ref); }, null), rows = info ? info.rows : [];
                rec.pointRows.forEach(function (pr, k) {
                    var row = rows[k], ok = row && (row[0] + '|' + row[3]) === pr.key;
                    rec.buf['__p' + k].push(ok && typeof row[1] === 'number' ? row[1] : NaN);
                });
            }
            rec.lastEl = el;
            rec.n++;
        }
        /* the progress bar is repainted eight times a second, not every frame: the samples are what matter */
        var nowMs = performance.now();
        if (!rec.shownAt || nowMs - rec.shownAt > 125) { progress(el / rec.len, el); rec.shownAt = nowMs; }
        if (el >= rec.len - 1e-9 || rec.n >= MAXS && rec.mode === 'change') finishRound(null);
    }
    function finishRound(why) {
        var r = rec;
        rec = null;
        recBox.classList.remove('is-rec');
        recLab.textContent = T('Record');
        recProg.hidden = true;
        recWhat._h = null;
        if (!r || r.n < 2) { describeRound(); if (r) recWhat.innerHTML += T(' <b>The last round caught fewer than two samples') + (why ? ' (' + esc(why) + ')' : '') + '.</b>'; return; }
        roundNo = r.no;
        var F = function (a) { return Float64Array.from(a); };
        var series = [{ key: TV || 't', label: timeSym(), units: timeUnit(), digits: TV ? Math.max(2, digitsOf(TV)) : 3, data: F(r.buf.__t), time: true }];
        roundCols.forEach(function (n) { series.push({ key: n, label: sym(n), units: unitOf(n), digits: digitsOf(n), data: F(r.buf[n]) }); });
        r.pointRows.forEach(function (pr, k) {
            series.push({ key: (pr.name || 'point_' + k) + (pr.idx !== undefined ? '_' + pr.idx : '') + T('_at_point'), label: pr.label, units: pr.units, digits: pr.name && V(pr.name) ? digitsOf(pr.name) : 4, data: F(r.buf['__p' + k]), point: true });
        });
        var all = {};
        r.names.forEach(function (n) { all[n] = F(r.buf[n]); });
        rounds.push({ no: r.no, label: r.label, len: r.len, n: r.n, frames: r.frames, el: r.buf.__el[r.buf.__el.length - 1], why: why, at: clock(), pointTitle: r.pointTitle, params: r.params, series: series, all: all, elapsed: F(r.buf.__el) });
        if (rounds.length > 5) rounds.shift();
        sel = rounds.length - 1;
        roundCount.textContent = rounds.length;
        describeRound();
        catchNow(T('at the end of round ') + r.no);
        if (!isOpen) setOpen(true, false);
        show('rounds');
        panes.rounds.scrollTop = 0;
    }
    recBtn.addEventListener('click', startRound);

    function seriesRange(s) {
        var lo = Infinity, hi = -Infinity;
        for (var i = 0; i < s.data.length; i++) { var x = s.data[i]; if (x === x && isFinite(x)) { if (x < lo) lo = x; if (x > hi) hi = x; } }
        return lo <= hi ? [lo, hi] : [NaN, NaN];
    }
    function drawChart(cv, s, x, cursor) {
        var P = palette(), dpr = Math.min(window.devicePixelRatio || 1, 2), W = cv.clientWidth || 300, H = cv.clientHeight || 64;
        if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)) { cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
        var c = cv.getContext('2d');
        c.setTransform(dpr, 0, 0, dpr, 0, 0);
        c.clearRect(0, 0, W, H);
        var rg = seriesRange(s), lo = rg[0], hi = rg[1], n = s.data.length;
        if (!(lo === lo)) { c.fillStyle = P.muted; c.font = T('12px ') + getComputedStyle(cv).fontFamily; c.fillText('not defined during this round', 8, H / 2 + 4); return; }
        var span = Math.max(hi - lo, 0.02 * Math.max(Math.abs(hi), Math.abs(lo)), 1e-12), mid = (hi + lo) / 2;
        lo = mid - span / 2; hi = mid + span / 2;
        var x0 = x[0], x1 = x[n - 1] > x0 ? x[n - 1] : x0 + 1, pad = 6;
        var sx = function (v) { return 1 + (v - x0) / (x1 - x0) * (W - 2); }, sy = function (v) { return H - pad - (v - lo) / (hi - lo) * (H - 2 * pad); };
        c.strokeStyle = P.rule; c.lineWidth = 1;
        c.beginPath(); c.moveTo(0, H - 0.5); c.lineTo(W, H - 0.5); c.stroke();
        if (lo < 0 && hi > 0) { c.setLineDash([3, 4]); c.beginPath(); c.moveTo(0, Math.round(sy(0)) + 0.5); c.lineTo(W, Math.round(sy(0)) + 0.5); c.stroke(); c.setLineDash([]); }
        c.strokeStyle = s.point ? P.ink : P.accent; c.lineWidth = 1.7; c.lineJoin = 'round';
        c.beginPath();
        var on = false;
        for (var i = 0; i < n; i++) {
            var v = s.data[i];
            if (!(v === v) || !isFinite(v)) { on = false; continue; }
            if (on) c.lineTo(sx(x[i]), sy(v)); else { c.moveTo(sx(x[i]), sy(v)); on = true; }
        }
        c.stroke();
        if (cursor !== null && cursor >= 0 && cursor < n) {
            var cx = Math.round(sx(x[cursor])) + 0.5;
            c.strokeStyle = P.ink3; c.lineWidth = 1; c.beginPath(); c.moveTo(cx, 0); c.lineTo(cx, H); c.stroke();
            var cv2 = s.data[cursor];
            if (cv2 === cv2 && isFinite(cv2)) { c.fillStyle = s.point ? P.ink : P.accent; c.beginPath(); c.arc(cx, sy(cv2), 3.5, 0, Math.PI * 2); c.fill(); }
        }
    }
    function renderRounds() {
        var host = panes.rounds;
        if (!rounds.length) {
            host.innerHTML = T('<div class="dp-empty"><p class="dp-empty__k">No round yet</p><h3>Record one round of the simulation.</h3>') +
                T('<p>Press <b>Record</b> above. The simulation keeps running exactly as before; for one round (') + esc(safe(R.label, '') || 'ten seconds') + T(') every frame’s numbers are copied here, then the recording stops by itself.</p>') +
                T('<p>You get one chart per quantity, a table of every sample, and a file you can open in Python. ') + T('Pin a point with <b>Read values</b> under the figure first, and its values are recorded too.</p></div>');
            return;
        }
        var r = rounds[sel], x = r.elapsed;
        var chips = rounds.map(function (q, k) { return '<button type="button" class="dp-chip' + (k === sel ? T(' is-on') : '') + '" data-round="' + k + T('">Round ') + q.no + '</button>'; }).join('');
        var params = r.params.map(function (p) { return '<span><i>' + sym(p[0]) + '</i> ' + esc(num(p[1], digitsOf(p[0]))) + (unitOf(p[0]) ? ' ' + unitOf(p[0]) : '') + '</span>'; }).join('');
        var h = '<div class="dp-rd">' + (rounds.length > 1 ? '<div class="dp-rd__chips">' + chips + '</div>' : '') +
            T('<header class="dp-rd__hd"><div class="dp-rd__top"><h3>Round ') + r.no + '<span class="dp__dot">.</span></h3>' +
            '<div class="dp-rd__tools"><button type="button" class="dp-btn dp-btn--solid" data-round-save>' + SAVE + T(' Save<span class="dp-more-txt"> this round</span></button>') +
            T('<button type="button" class="dp-btn" data-round-csv>CSV</button></div></div>') +
            '<p class="dp-rd__sum">' + esc(r.label) + ' · ' + r.n + T(' samples from ') + r.frames + T(' frames · caught at ') + esc(r.at) + (r.why ? ' · ' + esc(r.why) : '') + '</p>' +
            (params ? '<p class="dp-rd__par">' + params + '</p>' : '') + '</header>' +
            '<p class="dp-rd__read" aria-live="polite"></p><div class="dp-rd__charts">';
        /* a quantity that does not change during the round, or is not defined in it, gets one line, not a flat chart */
        var still = [], undef = [];
        r.series.forEach(function (s, k) {
            if (s.time) return;
            var rg = seriesRange(s);
            if (!(rg[0] === rg[0])) { undef.push(s); return; }
            if (rg[1] - rg[0] <= 1e-12 * Math.max(1, Math.abs(rg[1]))) { still.push([s, rg[0]]); return; }
            h += '<figure class="dp-ch' + (s.point ? T(' dp-ch--pt') : '') + '"><figcaption><span class="dp-sym">' + s.label + '</span>' + (s.units ? '<span class="dp-u">' + s.units + '</span>' : '') +
                (s.point ? T('<em>at the point</em>') : '') + '<b>' + esc(num(rg[0], s.digits)) + ' … ' + esc(num(rg[1], s.digits)) + '</b></figcaption><canvas data-series="' + k + '"></canvas></figure>';
        });
        h += '</div>' + (still.length ? T('<p class="dp-rd__still"><b>Constant during the round</b>') + still.map(function (q) { return '<span><i>' + q[0].label + '</i> ' + esc(num(q[1], q[0].digits)) + (q[0].units ? ' ' + q[0].units : '') + (q[0].point ? T(' <em>at the point</em>') : '') + '</span>'; }).join('') + '</p>' : '') +
            (undef.length ? T('<p class="dp-rd__still"><b>Not defined during the round</b>') + undef.map(function (q) { return '<span><i>' + q.label + '</i></span>'; }).join('') + '</p>' : '') +
            (r.pointTitle ? T('<p class="dp-rd__note">Black lines follow ') + r.pointTitle + T(', the point followed when the round began.</p>') : '') +
            T('<details class="dp-rd__tbl"><summary>Every sample · ') + r.n + T(' rows × ') + r.series.length + T(' columns</summary><div class="dp-rd__wrap"><table><thead><tr><th>#</th>') +
            r.series.map(function (s) { return '<th><span class="dp-sym">' + s.label + '</span>' + (s.units ? '<small>' + s.units + '</small>' : '') + '</th>'; }).join('') + '</tr></thead><tbody>';
        for (var i = 0; i < r.n; i++) h += '<tr><th>' + (i + 1) + '</th>' + r.series.map(function (s) { return '<td>' + esc(num(s.data[i], s.digits)) + '</td>'; }).join('') + '</tr>';
        h += '</tbody></table></div></details></div>';
        host.innerHTML = h;
        var canv = Array.prototype.slice.call(host.querySelectorAll(T('canvas[data-series]')));
        var readEl = host.querySelector('.dp-rd__read');
        function readout(i) {
            var head = i === null ? (TOUCH ? T('Touch a chart to read one sample.') : T('Point at a chart to read every quantity at one sample.')) : T('<b>Sample ') + (i + 1) + T(' of ') + r.n + '</b> · ' + timeSym() + ' = ' + esc(num(r.series[0].data[i], r.series[0].digits)) + (timeUnit() ? ' ' + timeUnit() : '') + ' · ' + esc(num(x[i], 3)) + (timeUnit() ? ' ' + esc(timeUnit()) : '') + T(' into the round');
            readEl.innerHTML = head;
        }
        function drawAll(cur) { canv.forEach(function (cv) { drawChart(cv, r.series[+cv.getAttribute('data-series')], x, cur); }); }
        drawAll(null);
        readout(null);
        var chartsEl = host.querySelector('.dp-rd__charts');
        function pick(e) {
            var cv = e.target.closest && e.target.closest(T('canvas[data-series]'));
            if (!cv) return;
            var rc = cv.getBoundingClientRect(), f = Math.max(0, Math.min(1, (e.clientX - rc.left) / rc.width)), target = x[0] + f * (x[r.n - 1] - x[0]), best = 0;
            for (var i = 1; i < r.n; i++) if (Math.abs(x[i] - target) < Math.abs(x[best] - target)) best = i;
            drawAll(best);
            readout(best);
            var vals = r.series.slice(1).map(function (s) { return '<span><i>' + s.label + '</i> ' + esc(num(s.data[best], s.digits)) + (s.units ? ' ' + s.units : '') + '</span>'; }).join('');
            readEl.innerHTML += '<span class="dp-rd__vals">' + vals + '</span>';
        }
        chartsEl.addEventListener('pointermove', pick);
        chartsEl.addEventListener('pointerdown', pick);
        chartsEl.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') { drawAll(null); readout(null); } });
    }
    function roundCsv(r) {
        var cols = r.series.map(function (s) { return s.key; }), extra = Object.keys(r.all).filter(function (n) { return cols.indexOf(n) < 0; });
        var head = ['sample', 'time_into_round'].concat(cols, extra).join(',');
        var lines = [head];
        for (var i = 0; i < r.n; i++) lines.push([i + 1, r.elapsed[i]].concat(r.series.map(function (s) { return s.data[i]; }), extra.map(function (n) { return r.all[n][i]; })).map(function (v) { return v === v ? String(v) : ''; }).join(','));
        return lines.join('\n') + '\n';
    }
    function download(blob, name) {
        var a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = name;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
    }
    function stamp() { return new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19); }
    panes.rounds.addEventListener('click', function (e) {
        var b = e.target.closest('[data-round]');
        if (b) { sel = +b.getAttribute('data-round'); renderRounds(); return; }
        var r = rounds[sel];
        if (!r) return;
        if (e.target.closest('[data-round-csv]')) { download(new Blob([roundCsv(r)], { type: T('text/csv') }), (spec.file || 'dataset') + T('-round-') + r.no + '-' + stamp() + '.csv'); return; }
        if (e.target.closest('[data-round-save]')) {
            var rd = Sim.dataset({ title: ds.title + T(' · round ') + r.no, attrs: { page: location.pathname.split('/').pop(), round: r.label, samples: r.n, frames: r.frames, caught_at: r.at, time_variable: TV || 'wall clock', point: plain(r.pointTitle || '') } });
            r.params.forEach(function (p) { rd.attrs['start_' + p[0]] = p[1]; });
            rd.dim('sample', r.n);
            rd.coord('time_into_round', 'sample', Float64Array, { units: timeUnit(), long_name: 'time since the round began' });
            rd.set('time_into_round', r.elapsed);
            r.series.forEach(function (s) { if (!rd.has(s.key)) { rd.var(s.key, ['sample'], Float64Array, { symbol: plain(s.label), units: s.units, long_name: s.point ? plain(s.label) + T(' at ') + plain(r.pointTitle) : (V(s.key) ? plain(A(s.key).long_name || '') : '') }); rd.set(s.key, s.data); } });
            Object.keys(r.all).forEach(function (n) { if (!rd.has(n)) { rd.var(n, ['sample'], Float64Array, { symbol: plain(sym(n)), units: unitOf(n), long_name: plain(A(n).long_name || '') }); rd.set(n, r.all[n]); } });
            var filename = (spec.file || 'dataset') + T('-round-') + r.no + '-' + stamp() + '.zip';
            download(rd.npz([{ name: T('round.csv'), bytes: roundCsv(r) }, { name: T('README.txt'), bytes: readme(T('round ') + r.no, filename) }]), filename);
        }
    });

    /* ---------- Save ---------- */
    function readme(what, filename) {
        return [
            ds.title + ' · ' + what + T(' saved from ') + location.href.replace(/[#?].*$/, ''),
            T('Saved ') + new Date().toISOString(),
            '',
            'Each array variable is a NumPy .npy file; dataset.json lists every variable with its dimensions, dtype,',
            'units and attributes, and holds the scalars. Recorded rounds, if any, are CSV files with one row per sample.',
            '',
            T('Python:'),
            '    import json, zipfile, numpy as np',
            '    z = zipfile.ZipFile(' + JSON.stringify(filename) + ')',
            "    meta = json.load(z.open(T('dataset.json')))",
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
        var filename = (spec.file || 'dataset') + '-' + stamp() + '.zip';
        var extra = rounds.map(function (r) { return { name: 'round-' + r.no + '.csv', bytes: roundCsv(r) }; });
        extra.push({ name: T('README.txt'), bytes: readme(T('the store at ') + timeText(timeNow()).replace(/<[^>]+>/g, ''), filename) });
        download(ds.npz(extra), filename);
    });

    /* ---------- open, close, tabs ---------- */
    var isOpen = false, view = 'vars', liveOn = false;
    function show(name) {
        view = name;
        Object.keys(panes).forEach(function (k) { panes[k].hidden = k !== name; });
        Array.prototype.forEach.call(tabs, function (b) {
            var on = b.getAttribute('data-tab') === (name === 'rounds' ? 'rounds' : 'vars');
            b.setAttribute('aria-selected', on ? 'true' : 'false');
        });
        if (name === 'vars' || name === 'rounds') store('tab', name);
        if (name === 'rounds') renderRounds();
        paint(true);
    }
    function setOpen(open, save) {
        isOpen = open;
        document.body.classList.toggle('dp-open', open);
        tab.setAttribute('aria-expanded', open ? 'true' : 'false');
        panel.setAttribute('aria-hidden', open ? 'false' : 'true');
        if (open) panel.removeAttribute('inert'); else panel.setAttribute('inert', '');
        if (save) store('open', open ? '1' : '0');
        if (open) { describeRound(); catchNow('when the panel opened'); }
        kick();
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
    panes.vars.querySelector('[data-catch]').addEventListener('click', function () { catchNow(); });
    liveBox.addEventListener('change', function () {
        liveOn = liveBox.checked;
        store('live', liveOn ? '1' : '0');
        if (!liveOn) catchNow(T('when Live was switched off'));
        paint(true);
        kick();
    });

    function paintState() {
        var st = rec ? 'recording' : liveOn && isOpen ? 'live' : 'still', txt = rec ? 'recording' : st === 'live' ? 'live' : 'one instant';
        if (stateEl._s !== st) { stateEl.className = 'dp__state is-' + st; stateEl.textContent = txt; stateEl._s = st; }
    }
    function paint(force) {
        paintState();
        if (!isOpen) return;
        if (view === 'vars') { if (force || liveOn) { paintVars(liveOn && !force); paintInstant(); } }
        else if (view === 'array') { if (liveOn) snap = takeSnap(current); if (force || liveOn) paintArray(); }
    }

    /* ---------- the loop: it runs only while something needs it, and after the simulation's own frame ---------- */
    var running = false;
    function wanted() { return !!rec || (probe.on && (probe.pinned || !!probe.preview)) || performance.now() < probe.cellUntil || (isOpen && liveOn) || probe.marked; }
    function kick() { if (!running && wanted()) { running = true; requestAnimationFrame(frame); } }
    function frame() {
        if (rec) safe(recordFrame);
        if (overlay && (probe.on || probe.marked || performance.now() < probe.cellUntil)) safe(paintProbe);
        if (isOpen && liveOn) paint(false); else paintState();
        if (wanted()) requestAnimationFrame(frame);
        else { running = false; safe(clearOverlay); }
    }
    document.addEventListener('visibilitychange', function () { if (!document.hidden) kick(); });

    var saved = load('open');
    liveOn = load('live') === '1';
    liveBox.checked = liveOn;
    setOpen(saved === null ? window.innerWidth >= 1500 : saved === '1', false);
    show(load('tab') === 'rounds' ? 'rounds' : 'vars');
    describeRound();
    /* the first instant is caught after the simulation has drawn twice, so it is a real frame, not the empty start */
    requestAnimationFrame(function () { requestAnimationFrame(function () { if (isOpen && !liveOn) catchNow('when the page opened'); }); });
    /* the length of a round can depend on any control: refresh its description after any input, never on a timer */
    var pend = false;
    function soon() { if (pend) return; pend = true; requestAnimationFrame(function () { pend = false; describeRound(); }); }
    document.addEventListener('input', soon, true);
    document.addEventListener('click', soon, true);
    window.__dataPanel = { running: function () { return running; }, rounds: function () { return rounds; }, recording: function () { return !!rec; } };
})();
