/* Numa Koudsie · simulations
   Shared helpers: the site palette, crisp high-DPI canvases, styled sliders and a pausable clock. */
(function () {
    'use strict';

    var theme = {
        paper: '#f5f1ea',
        card: '#fffaf3',
        cardSoft: '#fbf6ee',
        ink: '#1c1518',
        ink2: '#3a322e',
        ink3: '#5a504b',
        muted: '#8b8079',
        rule: '#d9d0c2',
        ruleSoft: '#e6dfd2',
        accent: '#7a1f2b',
        accentDark: '#4d0f18',
        rose: '#e2a2aa',
        tan: '#efe4c8',
        tanInk: '#7a4b12',
        mono: "500 11px 'IBM Plex Mono', ui-monospace, Menlo, monospace",
        serif: "italic 17px 'IBM Plex Serif', Georgia, serif"
    };

    /* canvas sized to its CSS box, drawn in CSS pixels */
    function canvas2d(canvas) {
        var ctx = canvas.getContext('2d');
        var box = { canvas: canvas, ctx: ctx, w: 1, h: 1, dpr: 1 };
        box.fit = function () {
            var r = canvas.getBoundingClientRect();
            box.dpr = Math.min(window.devicePixelRatio || 1, 2);
            box.w = Math.max(1, Math.round(r.width));
            box.h = Math.max(1, Math.round(r.height));
            canvas.width = Math.round(box.w * box.dpr);
            canvas.height = Math.round(box.h * box.dpr);
            ctx.setTransform(box.dpr, 0, 0, box.dpr, 0, 0);
            return box;
        };
        return box.fit();
    }

    function onResize(el, fn) {
        var t = null;
        var run = function () {
            clearTimeout(t);
            t = setTimeout(fn, 80);
        };
        if ('ResizeObserver' in window) new ResizeObserver(run).observe(el);
        else window.addEventListener('resize', run);
    }

    /* <input type="range" id="x"> with an optional <output id="x-out"> */
    function slider(id, opts) {
        opts = opts || {};
        var input = document.getElementById(id);
        var out = document.getElementById(id + '-out');
        var format = opts.format || function (v) { return String(v); };
        function paint() {
            var min = parseFloat(input.min), max = parseFloat(input.max), v = parseFloat(input.value);
            input.style.setProperty('--p', ((v - min) / (max - min)) * 100 + '%');
            if (out) out.textContent = format(v);
        }
        input.addEventListener('input', function () {
            paint();
            if (opts.onInput) opts.onInput(parseFloat(input.value));
        });
        paint();
        return {
            el: input,
            get value() { return parseFloat(input.value); },
            set: function (v) { input.value = v; paint(); },
            paint: paint
        };
    }

    /* requestAnimationFrame clock; tick(dt, t) gets dt = 0 while paused */
    function clock(tick) {
        var playing = !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches), last = 0, t = 0, listeners = [];
        function frame(ts) {
            var dt = last ? Math.min((ts - last) / 1000, 0.05) : 0;
            last = ts;
            if (!playing) dt = 0;
            t += dt;
            tick(dt, t);
            requestAnimationFrame(frame);
        }
        requestAnimationFrame(frame);
        var api = {
            get playing() { return playing; },
            set: function (p) {
                playing = !!p;
                listeners.forEach(function (fn) { fn(playing); });
            },
            toggle: function () { api.set(!playing); },
            onChange: function (fn) { listeners.push(fn); }
        };
        return api;
    }

    function playButton(button, clk) {
        function paint(p) {
            button.textContent = p ? 'Pause' : 'Play';
            button.setAttribute('aria-pressed', p ? 'false' : 'true');
        }
        button.addEventListener('click', clk.toggle);
        clk.onChange(paint);
        paint(clk.playing);
    }

    /* fixed decimals, typographic minus, never "-0.00" */
    function fmt(v, digits) {
        var s = Number(v).toFixed(digits);
        if (/^-0(\.0*)?$/.test(s)) s = s.slice(1);
        return s.replace('-', '−');
    }

    /* visible error banner instead of a silently frozen canvas */
    function showError(message) {
        if (document.getElementById('sim-error')) return;
        var host = document.querySelector('main') || document.body;
        var el = document.createElement('div');
        el.id = 'sim-error';
        el.className = 'sim-error';
        el.setAttribute('role', 'alert');
        var b = document.createElement('b');
        b.textContent = 'This simulation stopped. ';
        el.appendChild(b);
        el.appendChild(document.createTextNode(String(message || 'Unknown error.') + ' Reload the page to try again.'));
        host.insertBefore(el, host.firstChild);
    }
    window.addEventListener('error', function (e) { showError(e.message); });

    /* ---------- derivation cards: every step and sub-step opens and closes ---------- */
    function cards() {
        var deriv = document.querySelector('.deriv');
        if (!deriv) return;
        var skip = document.createElement('a');
        skip.className = 'skip-link';
        skip.href = '#deriv-title';
        skip.textContent = 'Skip to the physics and code';
        document.body.insertBefore(skip, document.body.firstChild);
        window.addEventListener('beforeprint', function () {
            Array.prototype.forEach.call(deriv.querySelectorAll('details'), function (d) { d.open = true; });
        });
        Array.prototype.forEach.call(deriv.querySelectorAll('article.step'), function (step, i) {
            var card = document.createElement('details');
            card.className = 'card step';
            card.id = step.id;
            if (i === 0) card.open = true;
            var sum = document.createElement('summary');
            sum.className = 'card__sum';
            var num = step.querySelector('.step__num'), h3 = step.querySelector('h3');
            if (num) sum.appendChild(num);
            if (h3) sum.appendChild(h3);
            var body = document.createElement('div');
            body.className = 'card__body';
            var subBody = null, subs = 0;
            while (step.firstChild) {
                var node = step.firstChild;
                if (node.nodeType === 1 && node.tagName === 'H4') {
                    var sub = document.createElement('details');
                    sub.className = 'sub';
                    if (subs++ === 0) sub.open = true;
                    var ss = document.createElement('summary');
                    ss.className = 'sub__sum';
                    ss.appendChild(node);
                    subBody = document.createElement('div');
                    subBody.className = 'sub__body';
                    sub.appendChild(ss);
                    sub.appendChild(subBody);
                    body.appendChild(sub);
                    continue;
                }
                (subBody || body).appendChild(node);
            }
            card.appendChild(sum);
            card.appendChild(body);
            step.parentNode.replaceChild(card, step);
        });
        var head = deriv.querySelector('.deriv__head');
        if (head) {
            var tools = document.createElement('div');
            tools.className = 'deriv__tools';
            tools.innerHTML = '<button type="button" class="btn btn--ghost" data-all="1">Expand all</button>' +
                '<button type="button" class="btn btn--ghost" data-all="0">Collapse all</button>';
            tools.addEventListener('click', function (e) {
                var b = e.target.closest('[data-all]');
                if (!b) return;
                var open = b.getAttribute('data-all') === '1';
                Array.prototype.forEach.call(deriv.querySelectorAll('details'), function (d) { d.open = open; });
            });
            head.appendChild(tools);
        }
        /* the step index opens the card it points to */
        function openTarget(hash) {
            var t = hash && document.getElementById(hash.slice(1));
            if (t && t.tagName === 'DETAILS') t.open = true;
        }
        deriv.addEventListener('click', function (e) {
            var a = e.target.closest('a[href^="#"]');
            if (a) openTarget(a.getAttribute('href'));
        });
        openTarget(location.hash);
    }

    /* ---------- walkthrough: algebra, code and live numbers side by side ---------- */
    function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
    var MARK = /⟦([A-Za-z0-9_]+)\|([^⟧]*)⟧/g;
    /* text with ⟦key|shown text⟧ marks; each mark becomes a span tied to one quantity */
    function markup(text, escapeText) {
        var out = '', last = 0, m, f = escapeText ? esc : function (x) { return x; };
        MARK.lastIndex = 0;
        while ((m = MARK.exec(text))) {
            out += f(text.slice(last, m.index)) + '<span class="k" data-k="' + m[1] + '" tabindex="0">' + f(m[2]) + '</span>';
            last = MARK.lastIndex;
        }
        return out + f(text.slice(last));
    }

    function walkthrough(data) {
        var host = document.getElementById('walk');
        if (!host || !data) return;
        var cur = 0, held = false;
        host.innerHTML =
            '<div class="walk__head"><h2>From symbols to code</h2><p>' + data.intro + '</p>' +
            '<label class="switch walk__hold"><span>Hold the numbers</span><input type="checkbox"></label></div>' +
            '<div class="walk__frame"><ol class="walk__steps" role="tablist" aria-label="Steps"></ol>' +
            '<div class="walk__card" role="tabpanel"></div></div>';
        var list = host.querySelector('.walk__steps'), card = host.querySelector('.walk__card');
        var snap = null;
        host.querySelector('.walk__hold input').addEventListener('change', function (e) {
            held = e.target.checked;
            snap = held ? read() : null;
            host.classList.toggle('is-held', held);
        });
        data.steps.forEach(function (st, i) {
            var li = document.createElement('li');
            li.innerHTML = '<button type="button" role="tab"><span>' + (i < 9 ? '0' : '') + (i + 1) + '</span>' + st.title + '</button>';
            li.firstChild.addEventListener('click', function () { show(i); });
            li.firstChild.addEventListener('keydown', function (e) {
                var last = data.steps.length - 1;
                var to = { ArrowDown: cur + 1, ArrowRight: cur + 1, ArrowUp: cur - 1, ArrowLeft: cur - 1, Home: 0, End: last }[e.key];
                if (to === undefined) return;
                e.preventDefault();
                to = Math.max(0, Math.min(last, to));
                show(to);
                list.children[to].firstChild.focus();
            });
            list.appendChild(li);
        });

        function light(key, on) {
            Array.prototype.forEach.call(card.querySelectorAll('[data-k="' + key + '"]'), function (el) {
                el.classList.toggle('is-lit', on);
            });
        }
        function show(i) {
            cur = i;
            var st = data.steps[i];
            Array.prototype.forEach.call(list.children, function (li, j) {
                li.firstChild.setAttribute('aria-selected', j === i ? 'true' : 'false');
            });
            var rows = st.syms.map(function (r) {
                return '<tr data-k="' + r[0] + '"><td class="walk__sym">' + r[1] + '</td><td><code>' + esc(r[2]) +
                    '</code></td><td class="walk__val" data-v="' + r[0] + '">—</td><td>' + r[3] + '</td></tr>';
            }).join('');
            card.innerHTML =
                '<div class="walk__top"><p class="walk__num">Step ' + (i + 1) + ' of ' + data.steps.length + '</p>' +
                '<h3>' + st.title + '</h3><p class="walk__where">' + esc(st.where) + '</p></div>' +
                '<div class="walk__cols"><div class="walk__math"><p class="walk__label">Algebra</p>' +
                '<div class="eq walk__eq">' + markup(st.math, false) + '</div><p class="walk__note">' + st.note + '</p></div>' +
                '<div class="walk__code"><p class="walk__label">Code · as written in this page</p><pre><code>' + markup(st.code, true) + '</code></pre></div></div>' +
                '<div class="walk__tablewrap"><table class="walk__table"><thead><tr><th>Symbol</th><th>In code</th><th class="now">Now</th><th>Meaning</th></tr></thead>' +
                '<tbody>' + rows + '</tbody></table></div>' +
                '<div class="walk__nav"><button type="button" class="btn btn--ghost" data-go="-1"' + (i === 0 ? ' disabled' : '') + '>← Previous</button>' +
                '<button type="button" class="btn" data-go="1"' + (i === data.steps.length - 1 ? ' disabled' : '') + '>Next →</button></div>';
            Array.prototype.forEach.call(card.querySelectorAll('[data-go]'), function (b) {
                b.addEventListener('click', function () { show(cur + parseInt(b.getAttribute('data-go'), 10)); });
            });
            update(true);
        }
        ['mouseover', 'focusin'].forEach(function (ev) {
            card.addEventListener(ev, function (e) { var t = e.target.closest('[data-k]'); if (t) light(t.getAttribute('data-k'), true); });
        });
        ['mouseout', 'focusout'].forEach(function (ev) {
            card.addEventListener(ev, function (e) { var t = e.target.closest('[data-k]'); if (t) light(t.getAttribute('data-k'), false); });
        });
        function read() {
            try { return window.Sim.live ? window.Sim.live() : {}; } catch (err) { return {}; }
        }
        /* while held, every step shows the same frozen instant */
        function update(force) {
            if (held && !force) return;
            var vals = held && snap ? snap : read();
            Array.prototype.forEach.call(card.querySelectorAll('[data-v]'), function (td) {
                var v = vals[td.getAttribute('data-v')];
                td.textContent = v === undefined ? '—' : v;
            });
        }
        setInterval(update, 200);
        show(0);
    }

    function boot() {
        cards();
        var host = document.getElementById('walk');
        if (!host) return;
        var s = document.createElement('script');
        s.charset = 'utf-8';
        s.src = '../scripts/walk/' + host.getAttribute('data-walk') + '.js';
        s.onload = function () { walkthrough((window.WALK || {})[host.getAttribute('data-walk')]); };
        document.body.appendChild(s);
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
    else boot();

    window.Sim = {
        theme: theme,
        canvas2d: canvas2d,
        onResize: onResize,
        slider: slider,
        clock: clock,
        playButton: playButton,
        fmt: fmt,
        showError: showError
    };
})();
