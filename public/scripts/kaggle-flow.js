/* Kaggle flow: the page side of the pipeline that brings precomputed data from Kaggle to a simulation page.
   A page that plays stored runs uses four pieces from here (docs/kaggle-pipeline.md):
   - KaggleFlow.slider: a parameter control over a list of stops that shows which stops are computed and stored
     (filled dots, a solid band) and which are not (hollow dots, a hatched band). Near the edge of the stored band it
     grows heavier: the thumb follows the hand less and less (a soft zone over the last part of the stored range), so a
     visitor slides into the uncomputed region slowly, never with a jump.
   - KaggleFlow.governor: a first-order lag for the playback speed, so speed changes are eased, never stepped.
   - KaggleFlow.popup: the loading notice, faded in only when there is nothing left to show; it draws the pipeline
     (this page, kaggle-bridge, Kaggle GPU, stored, back here) with the real stage lit and a dot travelling along it.
   - KaggleFlow.bridge: the client of the Worker kaggle-bridge. With no address it answers "not connected" at once,
     so a page behaves the same, honestly, before the bridge exists.
   No physics here: a page supplies its own data, its own live solver and its own drawing. */
(function () {
    'use strict';
    var KF = window.KaggleFlow = {};
    function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
    function smooth(x) { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); }
    KF.smooth = smooth;

    /* ---------------- the slider ----------------
       opt.host      element to build into
       opt.stops     the values a visitor can pick, in order (computed or not)
       opt.index     the starting stop
       opt.stored    function (i) -> true when stop i is computed and stored for the current other parameters
       opt.soft      fraction of the stored band, at each end, over which the control grows heavy (default 0.28)
       opt.minGain   the thumb's speed relative to the hand deep in the soft zone and beyond (default 0.22)
       opt.format    function (value) -> text for the output
       opt.label     the control's name (HTML), opt.onChange(i, value) when the picked stop changes */
    KF.slider = function (opt) {
        var stops = opt.stops, n = stops.length, soft = opt.soft == null ? 0.28 : opt.soft, minGain = opt.minGain == null ? 0.22 : opt.minGain;
        var fmt = opt.format || function (v) { return String(v); };
        var u = opt.index, target = u, idx = opt.index, dragging = false, lastX = 0, raf = 0, band = [0, n - 1];
        var root = document.createElement('div'); root.className = 'kf-slider ctl';
        root.innerHTML = '<span class="ctl__row"><span>' + opt.label + '</span><output></output></span>' +
            '<div class="kf-track" role="slider" tabindex="0" aria-label="' + (opt.aria || '') + '" aria-valuemin="0" aria-valuemax="' + (n - 1) + '">' +
            '<span class="kf-hatch"></span><span class="kf-band"></span><span class="kf-soft kf-soft--lo"></span><span class="kf-soft kf-soft--hi"></span>' +
            '<span class="kf-dots"></span><span class="kf-thumb"></span></div>' +
            '<span class="kf-note"></span>';
        opt.host.appendChild(root);
        var out = root.querySelector('output'), track = root.querySelector('.kf-track'), thumb = root.querySelector('.kf-thumb'),
            bandEl = root.querySelector('.kf-band'), softLo = root.querySelector('.kf-soft--lo'), softHi = root.querySelector('.kf-soft--hi'),
            dots = root.querySelector('.kf-dots'), note = root.querySelector('.kf-note');
        for (var i = 0; i < n; i++) { var d = document.createElement('i'); d.style.left = pct(i); dots.appendChild(d); }
        function pct(x) { return (n > 1 ? 100 * x / (n - 1) : 50) + '%'; }
        function width() { return Math.max(1, track.clientWidth); }
        /* the stored band: the longest run of stored stops that contains the current stop, or the nearest one */
        function findBand() {
            var c = clamp(Math.round(u), 0, n - 1), lo = -1, hi = -1;
            if (opt.stored(c)) { lo = hi = c; } else {
                for (var r = 1; r < n && lo < 0; r++) { if (c - r >= 0 && opt.stored(c - r)) lo = hi = c - r; else if (c + r < n && opt.stored(c + r)) lo = hi = c + r; }
            }
            if (lo < 0) return null;
            while (lo > 0 && opt.stored(lo - 1)) lo--;
            while (hi < n - 1 && opt.stored(hi + 1)) hi++;
            return [lo, hi];
        }
        /* 0 well inside the stored band, rising smoothly to 1 at its edge, 1 beyond it */
        function closeness(x) {
            if (!band) return 1;
            var w = Math.max(1, soft * (band[1] - band[0]));
            if (x > band[1] || x < band[0]) return 1;
            return Math.max(band[1] < n - 1 ? smooth((x - (band[1] - w)) / w) : 0, band[0] > 0 ? smooth(((band[0] + w) - x) / w) : 0);
        }
        function gain(x) { return 1 - (1 - minGain) * closeness(x); }
        function paintBand() {
            band = findBand();
            for (var i = 0; i < n; i++) dots.children[i].className = opt.stored(i) ? '' : 'no';
            if (!band) { bandEl.style.display = softLo.style.display = softHi.style.display = 'none'; return; }
            var w = Math.max(1, soft * (band[1] - band[0]));
            bandEl.style.display = ''; bandEl.style.left = pct(band[0]); bandEl.style.right = (100 - parseFloat(pct(band[1]))) + '%';
            softHi.style.display = band[1] < n - 1 ? '' : 'none'; softHi.style.left = pct(band[1] - w); softHi.style.right = (100 - parseFloat(pct(band[1]))) + '%';
            softLo.style.display = band[0] > 0 ? '' : 'none'; softLo.style.left = pct(band[0]); softLo.style.right = (100 - parseFloat(pct(band[0] + w))) + '%';
        }
        function paint() {
            thumb.style.left = pct(u);
            var c = closeness(u);
            root.style.setProperty('--heavy', c.toFixed(3));
            root.classList.toggle('is-heavy', c > 0.02);
            var s = opt.stored(idx);
            root.classList.toggle('is-out', !s);
            out.textContent = fmt(stops[idx]);
            note.textContent = !s ? 'not computed yet' : c > 0.02 ? 'near the edge of the computed range' : '';
            track.setAttribute('aria-valuenow', idx); track.setAttribute('aria-valuetext', fmt(stops[idx]) + (s ? '' : ', not computed yet'));
        }
        function settle() {
            var j = clamp(Math.round(u), 0, n - 1);
            if (j !== idx) { idx = j; paint(); if (opt.onChange) opt.onChange(idx, stops[idx]); } else paint();
        }
        function animate() {
            cancelAnimationFrame(raf);
            var last = 0;
            (function step(ts) {
                var dt = last ? Math.min((ts - last) / 1000, 0.05) : 0.016; last = ts;
                u += (target - u) * (1 - Math.exp(-dt / 0.12));
                if (Math.abs(target - u) < 0.002) u = target;
                settle();
                if (u !== target && !dragging) raf = requestAnimationFrame(step);
            })(performance.now());
        }
        track.addEventListener('pointerdown', function (e) {
            dragging = true; lastX = e.clientX; track.setPointerCapture(e.pointerId); root.classList.add('is-drag');
            var r = track.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * (n - 1);
            if (Math.abs(x - u) > 0.6) { target = clamp(Math.round(x), 0, n - 1); dragging = false; animate(); dragging = true; }
            e.preventDefault();
        });
        track.addEventListener('pointermove', function (e) {
            if (!dragging) return;
            var dx = e.clientX - lastX; lastX = e.clientX;
            u = clamp(u + dx / width() * (n - 1) * gain(u), 0, n - 1); target = u; settle();
        });
        function end() { if (!dragging) return; dragging = false; root.classList.remove('is-drag'); target = clamp(Math.round(u), 0, n - 1); animate(); }
        track.addEventListener('pointerup', end); track.addEventListener('pointercancel', end);
        track.addEventListener('keydown', function (e) {
            var k = e.key, d = k === 'ArrowRight' || k === 'ArrowUp' ? 1 : k === 'ArrowLeft' || k === 'ArrowDown' ? -1 : 0;
            if (k === 'Home') { target = 0; animate(); e.preventDefault(); } else if (k === 'End') { target = n - 1; animate(); e.preventDefault(); }
            if (!d) return; target = clamp(Math.round(target) + d, 0, n - 1); animate(); e.preventDefault();
        });
        paintBand(); paint();
        if (window.ResizeObserver) new ResizeObserver(paint).observe(track);
        return {
            el: root,
            get index() { return idx; }, get value() { return stops[idx]; }, get position() { return u; },
            closeness: function () { return closeness(u); },
            stored: function () { return opt.stored(idx); },
            /* which way the visitor is heading out of the band: +1, -1, or 0 inside */
            heading: function () { return !band ? 0 : u > band[1] - Math.max(1, soft * (band[1] - band[0])) && band[1] < n - 1 ? 1 : u < band[0] + Math.max(1, soft * (band[1] - band[0])) && band[0] > 0 ? -1 : 0; },
            band: function () { return band ? band.slice() : null; },
            refresh: function () { paintBand(); paint(); },
            set: function (i, now) { target = clamp(i, 0, n - 1); if (now) { u = target; settle(); } else animate(); }
        };
    };

    /* ---------------- eased speed ---------------- */
    KF.governor = function (tau, start) {
        var s = start == null ? 1 : start;
        return { step: function (goal, dt) { s += (goal - s) * (1 - Math.exp(-dt / tau)); if (Math.abs(goal - s) < 1e-4) s = goal; return s; }, get value() { return s; }, set: function (v) { s = v; } };
    };

    /* ---------------- the loading notice with the pipeline ---------------- */
    var STAGES = ['This page', 'kaggle-bridge', 'Kaggle GPU', 'Stored', 'Back here'];
    KF.popup = function (host) {
        var el = document.createElement('div'); el.className = 'kf-pop'; el.setAttribute('role', 'status'); el.setAttribute('aria-live', 'polite');
        var W = 520, H = 92, xs = STAGES.map(function (_, i) { return 46 + i * (W - 92) / (STAGES.length - 1); });
        var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="kf-pipe" aria-hidden="true">';
        for (var i = 0; i < STAGES.length - 1; i++) svg += '<line class="kf-edge" data-e="' + i + '" x1="' + (xs[i] + 14) + '" y1="34" x2="' + (xs[i + 1] - 14) + '" y2="34"/>';
        STAGES.forEach(function (s, i) { svg += '<g class="kf-node" data-n="' + i + '"><circle cx="' + xs[i] + '" cy="34" r="11"/><text x="' + xs[i] + '" y="70">' + s + '</text></g>'; });
        svg += '<circle class="kf-packet" r="4.5" cx="' + xs[0] + '" cy="34"/></svg>';
        el.innerHTML = '<p class="kf-pop__kicker">Computing the next part</p><p class="kf-pop__title"></p>' + svg +
            '<div class="kf-pop__bar"><span></span></div><p class="kf-pop__text"></p>';
        host.appendChild(el);
        var title = el.querySelector('.kf-pop__title'), text = el.querySelector('.kf-pop__text'), bar = el.querySelector('.kf-pop__bar span'),
            packet = el.querySelector('.kf-packet'), stage = 0, raf = 0, shown = false, broken = -1;
        function run(ts) {
            if (!shown) return;
            var a = stage, b = Math.min(stage + 1, STAGES.length - 1), f = (ts / 1400) % 1;
            if (broken === stage) f = 0.5 + 0.08 * Math.sin(ts / 200);
            packet.setAttribute('cx', (xs[a] + (xs[b] - xs[a]) * f).toFixed(1));
            raf = requestAnimationFrame(run);
        }
        return {
            show: function () { if (shown) return; shown = true; el.classList.add('is-on'); raf = requestAnimationFrame(run); },
            hide: function () { shown = false; el.classList.remove('is-on'); cancelAnimationFrame(raf); },
            get shown() { return shown; },
            /* s.stage: 0..4 the step now working; s.broken: index of a step that is not available (drawn dashed); s.title, s.text, s.progress 0..1 */
            set: function (s) {
                stage = s.stage; broken = s.broken == null ? -1 : s.broken;
                el.querySelectorAll('.kf-node').forEach(function (g, i) { g.classList.toggle('is-done', i < stage); g.classList.toggle('is-now', i === stage); g.classList.toggle('is-off', i === broken); });
                el.querySelectorAll('.kf-edge').forEach(function (l, i) { l.classList.toggle('is-done', i < stage); l.classList.toggle('is-off', i === broken || i + 1 === broken); });
                if (s.title != null) title.textContent = s.title;
                if (s.text != null) text.innerHTML = s.text;
                bar.style.width = (100 * clamp(s.progress || 0, 0, 1)).toFixed(1) + '%';
            }
        };
    };

    /* ---------------- the client of the Worker kaggle-bridge ----------------
       opt.url: the bridge's address, or null while it is not connected; opt.project: this page's project name.
       request(params) resolves to { state: 'stored', url } | { state: 'queued' | 'running', job, progress, stage } | { state: 'offline', reason } */
    KF.bridge = function (opt) {
        var url = opt.url || null;
        function offline() { return Promise.resolve({ state: 'offline', reason: 'The link from this page to Kaggle (the Worker kaggle-bridge) is not switched on yet, so new regions cannot be computed on Kaggle from here.' }); }
        return {
            get connected() { return !!url; },
            request: function (params) {
                if (!url) return offline();
                return fetch(url + '/v1/' + encodeURIComponent(opt.project) + '/block', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(params) })
                    .then(function (r) { return r.json(); }).catch(function (e) { return { state: 'offline', reason: 'kaggle-bridge did not answer: ' + e.message }; });
            },
            status: function (job) {
                if (!url) return offline();
                return fetch(url + '/v1/job/' + encodeURIComponent(job)).then(function (r) { return r.json(); }).catch(function (e) { return { state: 'offline', reason: e.message }; });
            }
        };
    };
})();
