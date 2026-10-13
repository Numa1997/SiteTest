/* Numa Koudsie · data panel
   A live variable explorer in the manner of Spyder's: every number a simulation computes, in a side panel.
   A page opts in by defining Sim.data next to its own state (see the Fig. 1 page) and loading this file after
   its own script, with styles/data.css in its head.

   Variables tab  name, type, size and value of every quantity, repainted every frame while the panel is open.
   Array view     any vector or matrix opens as a table; only the cells in view are drawn, so a
                  360 × 360 field costs no more than a 10 × 20 one.
   Log tab        one row per fixed step of time (or one row per change, for pages without a clock), the newest
                  at the bottom; the oldest rows drop off after spec.log.max, so memory stays bounded.

   Shared helpers for page specs:
   Sim.frameStats { dt, fps, frames, play, wall }  measured by this panel: last frame interval, smoothed frame rate,
                  frames seen, play time (advances only while spec.playing() is true) and seconds since load.
   Sim.colourMap(v, lim)  the site's ink → cream → burgundy map for a signed value, as [r, g, b]. */
(function () {
    'use strict';
    var Sim = window.Sim, spec = Sim && Sim.data;
    if (!spec) return;

    /* ---------- small helpers ---------- */
    var KEY = 'datapanel.';
    function load(k) { try { return localStorage.getItem(KEY + k); } catch (e) { return null; } }
    function store(k, v) { try { localStorage.setItem(KEY + k, v); } catch (e) { /* storage blocked: the choice lasts for this page */ } }
    function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
    /* integers from 10 000 up get a thin space every three digits, SI style */
    function grouped(n) {
        var s = String(Math.round(Math.abs(n)));
        if (s.length > 4) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
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
    /* readable text on a coloured cell */
    function textOn(rgb) { return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2] > 150 ? '#1c1518' : '#fffaf3'; }
    function kindOf(v) { return v.kind || 'scalar'; }
    function columnsOf(v) { return typeof v.columns === 'function' ? v.columns() : v.columns; }

    /* trough (ink) → rest (cream) → crest (burgundy), the colour table of Fig. 1 */
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
    function safe(fn, fallback) { try { return fn(); } catch (e) { return fallback; } }

    var vars = [];
    spec.groups.forEach(function (g) { g.vars.forEach(function (v) { vars.push(v); }); });

    /* ---------- the panel ---------- */
    var ICON = '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><rect x="1" y="1.5" width="12" height="11" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/>' +
        '<path d="M1 5.2h12M1 8.8h12M5.2 1.5v11" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>';

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
        '<header class="dp__head"><div class="dp__intro"><p class="dp__kicker">' + esc(spec.kicker) + '</p>' +
        '<h2 class="dp__title">' + esc(spec.title) + '</h2><p class="dp__sub">' + spec.subtitle + '</p></div>' +
        '<span class="dp__live">live</span>' +
        '<button type="button" class="dp__close" aria-label="Close the data panel">' +
        '<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M1.5 1.5l9 9M10.5 1.5l-9 9" stroke="currentColor" stroke-width="1.5"/></svg></button></header>' +
        '<div class="dp__tabs" role="tablist" aria-label="Data views">' +
        '<button type="button" role="tab" data-tab="vars">Variables <span class="dp__count">' + vars.length + '</span></button>' +
        '<button type="button" role="tab" data-tab="log">Log <span class="dp__count" data-log-count>0</span></button></div>' +
        '<div class="dp__body">' +
        '<section class="dp__pane" data-pane="vars"></section>' +
        '<section class="dp__pane dp-arr" data-pane="array" hidden></section>' +
        '<section class="dp__pane dp-log" data-pane="log" hidden></section></div>' +
        '<p class="dp__foot">' + spec.foot + '</p>';

    document.body.appendChild(tab);
    document.body.appendChild(panel);

    var live = panel.querySelector('.dp__live');
    var panes = {};
    Array.prototype.forEach.call(panel.querySelectorAll('[data-pane]'), function (p) { panes[p.getAttribute('data-pane')] = p; });
    var tabs = panel.querySelectorAll('[data-tab]');

    /* ---------- Variables: Spyder's four columns ---------- */
    var rowsHtml = '<table class="dp-table"><thead><tr><th scope="col">Name</th><th scope="col">Type</th><th scope="col">Size</th><th scope="col">Value</th></tr></thead><tbody>';
    spec.groups.forEach(function (g) {
        rowsHtml += '<tr class="dp-group"><th colspan="4" scope="rowgroup">' + esc(g.title) + (g.note ? '<span>' + g.note + '</span>' : '') + '</th></tr>';
        g.vars.forEach(function (v) {
            var k = kindOf(v), opens = k === 'vector' || k === 'matrix';
            rowsHtml += '<tr class="dp-row' + (opens ? ' dp-row--open' : '') + '" data-v="' + vars.indexOf(v) + '"' +
                (opens ? ' tabindex="0" title="Open as a table"' : '') + '>' +
                '<td class="dp-name"><span class="dp-sym">' + v.name + '</span>' + (v.code ? '<code>' + esc(v.code) + '</code>' : '') +
                (v.meaning ? '<small>' + v.meaning + '</small>' : '') + '</td>' +
                '<td><span class="dp-type dp-type--' + (opens ? 'array' : (v.type || 'float').split(' ')[0].replace(/[^a-z]/gi, '')) + '">' + esc(v.type || 'float') + '</span></td>' +
                '<td class="dp-size"></td><td class="dp-val"></td></tr>';
        });
    });
    panes.vars.innerHTML = rowsHtml + '</tbody></table>';

    var cells = vars.map(function (v, n) {
        var tr = panes.vars.querySelector('tr[data-v="' + n + '"]');
        return { size: tr.querySelector('.dp-size'), val: tr.querySelector('.dp-val'), s: null, h: null };
    });

    /* min, max and mean of a matrix, recomputed only when its version changes */
    function stats(v) {
        var ver = v.version ? v.version() : NaN;
        if (v._st && ver === v._ver) return v._st;
        if (v.prepare) v.prepare();
        var R = v.rows(), C = v.cols(), lo = Infinity, hi = -Infinity, sum = 0;
        for (var j = 0; j < R; j++) {
            for (var i = 0; i < C; i++) {
                var x = v.get(j, i);
                if (x < lo) lo = x;
                if (x > hi) hi = x;
                sum += x;
            }
        }
        v._ver = ver;
        v._st = R * C ? { min: lo, max: hi, mean: sum / (R * C) } : { min: NaN, max: NaN, mean: NaN };
        return v._st;
    }

    function describe(v) {
        var k = kindOf(v), size, html;
        if (k === 'matrix') {
            var st = stats(v), d = v.digits === undefined ? 4 : v.digits;
            size = v.rows() + ' × ' + v.cols();
            html = '<span class="dp-range">' + num(st.min, Math.min(d, 3)) + ' … ' + num(st.max, Math.min(d, 3)) + '</span>' +
                '<small>mean ' + num(st.mean, d) + '</small><span class="dp-more" aria-hidden="true">›</span>';
        } else if (k === 'vector') {
            var n = v.length(), col = columnsOf(v)[0], parts = [];
            for (var i = 0; i < Math.min(n, 3); i++) parts.push(num(col.get(i), col.digits));
            size = String(n);
            html = '<span class="dp-range">[' + parts.join(', ') + (n > 3 ? ', …' : '') + ']</span><span class="dp-more" aria-hidden="true">›</span>';
        } else if (k === 'colour') {
            var c = v.get();
            size = '3';
            html = c ? '<i class="dp-sw" style="background:rgb(' + c.join(',') + ')"></i>' + c.join(', ') : '—';
        } else {
            var x = v.get();
            size = v.size || '1';
            html = esc(num(x, v.digits)) + (v.unit && x !== undefined && x !== null ? ' <span class="dp-u">' + v.unit + '</span>' : '');
        }
        return { size: size, html: html };
    }

    function paintVars() {
        vars.forEach(function (v, n) {
            var d = safe(function () { return describe(v); }, { size: '—', html: '—' }), c = cells[n];
            if (d.size !== c.s) { c.size.textContent = d.size; c.s = d.size; }
            if (d.html !== c.h) { c.val.innerHTML = d.html; c.h = d.html; }
        });
    }

    /* ---------- Array view: a table that draws only the cells in view ---------- */
    function makeGrid(host, src, probeEl) {
        var CW = src.cw || 66, CH = 22, RH = 48, HH = 26;
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
            for (i = i0; i < i1; i++) h += '<div class="dg__h" style="left:' + i * CW + 'px;width:' + CW + 'px">' + esc(src.colLabel(i)) + '</div>';
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
            if (src.prepare) src.prepare();
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
                if (src.colour) {
                    var rgb = src.colour(v, it.j, it.i), bg = rgb ? 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')' : '';
                    if (bg !== it.bg) { it.el.style.background = bg; it.el.style.color = rgb ? textOn(rgb) : ''; it.bg = bg; }
                }
            });
            if (hot) probeEl.innerHTML = src.probe(hot.j, hot.i, src.get(hot.j, hot.i));
        }
        function mark(j, i) {
            items.forEach(function (it) { it.el.classList.toggle('is-hot', it.j === j && it.i === i); });
        }
        function onPoint(e) {
            var c = e.target.closest && e.target.closest('.dg__c');
            if (!c) return;
            hot = { j: +c.getAttribute('data-j'), i: +c.getAttribute('data-i') };
            mark(hot.j, hot.i);
            probeEl.innerHTML = src.probe(hot.j, hot.i, src.get(hot.j, hot.i));
        }
        cellsEl.addEventListener('mouseover', onPoint);
        cellsEl.addEventListener('click', onPoint);
        host.addEventListener('scroll', layout, { passive: true });
        var ro = 'ResizeObserver' in window ? new ResizeObserver(function () { win = ''; layout(); }) : null;
        if (ro) ro.observe(host);
        paint();
        return { paint: paint, destroy: function () { if (ro) ro.disconnect(); } };
    }

    var grid = null, current = null, statsEl = null;

    function gridSource(v) {
        if (kindOf(v) === 'vector') {
            return {
                cw: v.cw || 104, corner: v.corner || 'index',
                rows: v.length, cols: function () { return columnsOf(v).length; },
                get: function (j, i) { var c = columnsOf(v)[i]; return c ? c.get(j) : undefined; },
                digits: function (i) { var c = columnsOf(v)[i]; return c ? c.digits : 4; },
                colour: function (x, j, i) { var c = columnsOf(v)[i]; return c && c.colour && typeof x === 'number' ? c.colour(x, j) : null; },
                colLabel: function (i) { var c = columnsOf(v)[i]; return c ? c.name + (c.unit ? ' · ' + c.unit : '') : ''; },
                rowLabel: v.rowLabel || String,
                probe: function (j, i, x) {
                    var c = columnsOf(v)[i] || {}, row = v.rowLabel ? v.rowLabel(j) : j;
                    return '<b>' + esc(c.name) + '[' + esc(row) + ']</b> = ' + esc(num(x, c.digits)) + (c.unit ? ' ' + c.unit : '') +
                        (v.at ? '<span>' + v.at(j) + '</span>' : '');
                }
            };
        }
        return {
            cw: v.cw, corner: 'j \\ i', prepare: v.prepare,
            rows: v.rows, cols: v.cols, get: v.get, colour: v.colour,
            digits: function () { return v.digits === undefined ? 4 : v.digits; },
            colLabel: v.colLabel || String, rowLabel: v.rowLabel || String,
            probe: function (j, i, x) {
                return '<b>' + v.name + '[' + j + ', ' + i + ']</b> = ' + esc(num(x, v.digits === undefined ? 4 : v.digits)) +
                    (v.at ? '<span>' + v.at(j, i) + '</span>' : '');
            }
        };
    }

    function paintArrStats() {
        if (!current || !statsEl) return;
        var v = current, h;
        if (kindOf(v) === 'matrix') {
            var st = stats(v), d = v.digits === undefined ? 4 : v.digits;
            h = '<div><dt>shape</dt><dd>' + v.rows() + ' × ' + v.cols() + '</dd></div><div><dt>min</dt><dd>' + num(st.min, d) + '</dd></div>' +
                '<div><dt>max</dt><dd>' + num(st.max, d) + '</dd></div><div><dt>mean</dt><dd>' + num(st.mean, d) + '</dd></div>';
        } else {
            h = '<div><dt>length</dt><dd>' + v.length() + '</dd></div><div class="wide"><dt>columns</dt><dd>' +
                esc(columnsOf(v).map(function (c) { return c.name; }).join(', ')) + '</dd></div>';
        }
        if (h !== statsEl._h) { statsEl.innerHTML = h; statsEl._h = h; }
    }

    function openArray(v) {
        if (grid) grid.destroy();
        current = v;
        panes.array.innerHTML =
            '<div class="dp-arr__top"><button type="button" class="dp-back">← All variables</button>' +
            '<div class="dp-arr__title"><span class="dp-sym">' + v.name + '</span>' + (v.code ? '<code>' + esc(v.code) + '</code>' : '') +
            '<span class="dp-type dp-type--array">' + esc(v.type) + '</span></div>' +
            (v.meaning ? '<p class="dp-arr__mean">' + v.meaning + (v.updates ? ' · <em>updates ' + v.updates + '</em>' : '') + '</p>' : '') +
            '<dl class="dp-arr__stats"></dl></div>' +
            '<div class="dg" tabindex="0" aria-label="' + esc(v.code || 'array') + ' as a table"></div>' +
            '<p class="dp-arr__probe">Point at a cell to read its index and value.</p>';
        statsEl = panes.array.querySelector('.dp-arr__stats');
        panes.array.querySelector('.dp-back').addEventListener('click', function () { show('vars'); });
        show('array');
        grid = makeGrid(panes.array.querySelector('.dg'), gridSource(v), panes.array.querySelector('.dp-arr__probe'));
        paintArrStats();
    }

    panes.vars.addEventListener('click', function (e) {
        var tr = e.target.closest('.dp-row--open');
        if (tr) openArray(vars[+tr.getAttribute('data-v')]);
    });
    panes.vars.addEventListener('keydown', function (e) {
        var tr = e.target.closest && e.target.closest('.dp-row--open');
        if (tr && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); openArray(vars[+tr.getAttribute('data-v')]); }
    });

    /* ---------- Log: one row per step of play time ---------- */
    var L = spec.log, logBody = null, logWrap = null, logInfo = null, logCount = panel.querySelector('[data-log-count]');
    var total = 0, nextT = 0, lastKey = null;
    if (L) {
        panes.log.innerHTML =
            '<div class="dp-log__bar"><span class="dp-log__info"></span><button type="button" class="dp-btn" data-log-clear>Clear</button></div>' +
            '<div class="dp-log__wrap" tabindex="0" aria-label="Log table"><table class="dp-log__table"><thead><tr><th scope="col">#</th>' +
            L.columns.map(function (c) { return '<th scope="col">' + c.name + (c.unit ? '<small>' + c.unit + '</small>' : '') + '</th>'; }).join('') +
            '</tr></thead><tbody></tbody></table></div>';
        logBody = panes.log.querySelector('tbody');
        logWrap = panes.log.querySelector('.dp-log__wrap');
        logInfo = panes.log.querySelector('.dp-log__info');
        panes.log.querySelector('[data-log-clear]').addEventListener('click', function () {
            logBody.innerHTML = '';
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
        var cellsText = null;
        if (L.mode === 'change') {
            /* a new row only when a non-stamp column changed */
            cellsText = L.columns.map(function (c) { return num(safe(c.get), c.digits); });
            var key = cellsText.filter(function (x, i) { return !L.columns[i].stamp; }).join('|');
            if (key === lastKey) return;
            lastKey = key;
        } else {
            var every = L.every || 0.1, t = L.time ? L.time() : stats0.play;
            if (t < nextT - every) nextT = t;
            if (t < nextT) return;
            nextT = (Math.floor(t / every + 1e-9) + 1) * every;
            cellsText = L.columns.map(function (c) { return num(safe(c.get), c.digits); });
        }
        total++;
        var stick = logWrap.scrollTop + logWrap.clientHeight >= logWrap.scrollHeight - 24;
        var tr = document.createElement('tr');
        tr.innerHTML = '<th scope="row">' + total + '</th>' + cellsText.map(function (x) { return '<td>' + esc(x) + '</td>'; }).join('');
        logBody.appendChild(tr);
        while (logBody.rows.length > L.max) logBody.removeChild(logBody.firstChild);
        if (stick) logWrap.scrollTop = logWrap.scrollHeight;
        infoLog();
    }

    /* ---------- open, close, tabs ---------- */
    var isOpen = false, view = 'vars';
    function show(name) {
        view = name;
        Object.keys(panes).forEach(function (k) { panes[k].hidden = k !== name; });
        Array.prototype.forEach.call(tabs, function (b) {
            var on = b.getAttribute('data-tab') === (name === 'array' ? 'vars' : name);
            b.setAttribute('aria-selected', on ? 'true' : 'false');
        });
        if (name !== 'array') store('tab', name);
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
            show(t === 'vars' && view === 'array' ? 'array' : t);
        });
    });

    function paint() {
        if (!isOpen) return;
        var playing = spec.playing ? safe(spec.playing, false) : true;
        live.classList.toggle('is-live', playing);
        live.textContent = playing ? 'live' : 'paused';
        if (view === 'vars') paintVars();
        else if (view === 'array' && grid) { safe(grid.paint); paintArrStats(); }
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
        paint();
        requestAnimationFrame(frame);
    }

    var saved = load('open');
    setOpen(saved === null ? window.innerWidth >= 1500 : saved === '1', false);
    show(load('tab') === 'log' && L ? 'log' : 'vars');
    requestAnimationFrame(frame);
})();
