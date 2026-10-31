/* Numa Koudsie · simulations
   Shared helpers: the site palette, crisp high-DPI canvases, styled sliders and a pausable clock. */
(function () {
    'use strict'; window._t = window.T = window.T || function (s, v) { var d = window.I18N, r = d && d[s]; if (r && typeof r === 'object' && v && 'n' in v) r = r[new Intl.PluralRules(document.documentElement.lang).select(v.n)] || r.other; if (typeof r !== 'string') r = s; return v ? r.replace(/\{(\w+)\}/g, function (m, k) { return k in v ? v[k] : m; }) : r; };   /* a page's words: scripts/i18n/strings-<lang>.js on a translated page */

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
        serif: "italic 17px 'Latin Modern Roman', KaTeX_Math, 'Times New Roman', serif"
    };

    /* the site root, from this script's own address (scripts/sim.js) */
    var ROOT = (function () {
        var s = document.currentScript && document.currentScript.src;
        return s ? s.replace(/scripts\/sim\.js(\?.*)?$/, '') : '../';
    })();

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

    /* a canvas label set like the lecture notes: 'c_{p}', 'τ_{aero}', 'F_{0}/k', 'x^{2}'.
       Symbols in Latin Modern italic; a subscript of more than one letter is a word, so it stands upright.
       Returns the width drawn, in css px. */
    var TEX_FAMILY = "'Latin Modern Roman', KaTeX_Math, 'Times New Roman', serif";
    var TEX_UPRIGHT = "'Latin Modern Roman', KaTeX_Main, 'Times New Roman', serif";
    function texRuns(s) {
        var out = [], buf = '', i = 0;
        while (i < s.length) {
            var ch = s.charAt(i);
            if (s.substr(i, 8) === '\\mathrm{') {
                // \mathrm{…}: words and units, set upright as in TeX
                if (buf) { out.push({ t: buf, lv: 0 }); buf = ''; }
                var e = s.indexOf('}', i + 8);
                if (e < 0) e = s.length;
                out.push({ t: s.slice(i + 8, e), lv: 0, rm: true });
                i = e + 1;
                continue;
            }
            if ((ch === '_' || ch === '^') && s.charAt(i + 1) === '{') {
                if (buf) { out.push({ t: buf, lv: 0 }); buf = ''; }
                var j = s.indexOf('}', i + 2);
                if (j < 0) j = s.length;
                out.push({ t: s.slice(i + 2, j), lv: ch === '_' ? -1 : 1 });
                i = j + 1;
                continue;
            }
            buf += ch;
            i++;
        }
        if (buf) out.push({ t: buf, lv: 0 });
        // letters are italic, everything else upright, as in typeset mathematics; a subscript word stays upright
        var split = [];
        out.forEach(function (r) {
            if (r.rm || (r.lv !== 0 && /^[A-Za-z]{2,}$/.test(r.t))) { split.push({ t: r.t, lv: r.lv, up: true }); return; }
            // Latin and lower-case Greek letters are italic; capital Greek (Σ, Δ, Ω) stays upright, as TeX and KaTeX set it
            (r.t.match(/[A-Za-zα-ωϐ-ϵ]+|[^A-Za-zα-ωϐ-ϵ]+/g) || []).forEach(function (piece) {
                split.push({ t: piece, lv: r.lv, up: !/[A-Za-zα-ωϐ-ϵ]/.test(piece) });
            });
        });
        return split;
    }
    function tex(ctx, s, x, y, o) {
        o = o || {};
        var size = o.size || 15, runs = texRuns(String(s)), widths = [], total = 0;
        function font(r) {
            // upright runs fall back to KaTeX_Main, whose Greek is upright; KaTeX_Math has italic glyphs only
            return (o.upright || r.up ? '' : 'italic ') + (r.lv ? Math.round(size * 0.7) : size) + 'px ' + (o.upright || r.up ? TEX_UPRIGHT : TEX_FAMILY);
        }
        ctx.save();   // the caller's font, alignment and colour come back unchanged
        runs.forEach(function (r) { ctx.font = font(r); var wd = ctx.measureText(r.t).width; widths.push(wd); total += wd; });
        if (o.measure) { ctx.restore(); return total; }
        var x0 = o.align === 'right' ? x - total : o.align === 'center' ? x - total / 2 : x;
        ctx.textAlign = 'left';
        ctx.textBaseline = o.baseline || 'alphabetic';
        if (o.color) ctx.fillStyle = o.color;
        runs.forEach(function (r, k) {
            ctx.font = font(r);
            ctx.fillText(r.t, x0, y + (r.lv < 0 ? size * 0.28 : r.lv > 0 ? -size * 0.4 : 0));
            x0 += widths[k];
        });
        ctx.restore();
        return total;
    }

    /* tick values for an axis: about n steps of 1, 2 or 5 × 10^k */
    function ticks(lo, hi, n) {
        var raw = (hi - lo) / Math.max(1, n || 4), p = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), f = raw / p;
        var step = (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * p, out = [];
        for (var v = Math.ceil(lo / step - 1e-9) * step; v <= hi + step * 1e-9; v += step) out.push(Math.abs(v) < step * 1e-9 ? 0 : v);
        return { step: step, values: out, digits: Math.max(0, -Math.floor(Math.log(step) / Math.LN10 + 1e-9)) };
    }

    /* the colour of the canvas at (x, y) css px, searched within r px for a pixel that passes test(rgba).
       A transparent pixel never passes: the read-back first asks whether anything was drawn there at all. */
    function readPixel(box, x, y, r, test) {
        var d = Math.max(0, Math.round((r || 0) * box.dpr)), cx = Math.round(x * box.dpr), cy = Math.round(y * box.dpr), best = null;
        var x0 = Math.max(0, cx - d), y0 = Math.max(0, cy - d), wd = Math.min(box.canvas.width - x0, 2 * d + 1), ht = Math.min(box.canvas.height - y0, 2 * d + 1);
        if (wd <= 0 || ht <= 0) return { found: false, rgba: [0, 0, 0, 0], text: 'outside the canvas' };
        var px = box.ctx.getImageData(x0, y0, wd, ht).data, centre = null;
        for (var j = 0; j < ht; j++) for (var i = 0; i < wd; i++) {
            var k = 4 * (j * wd + i), c = [px[k], px[k + 1], px[k + 2], px[k + 3]];
            if (x0 + i === cx && y0 + j === cy) centre = c;
            if (c[3] > 0 && (!test || test(c))) {
                var dist = Math.hypot(x0 + i - cx, y0 + j - cy);
                if (!best || dist < best.dist) best = { c: c, dist: dist };
            }
        }
        var c = best ? best.c : (centre || [0, 0, 0, 0]);
        return { found: !!best, rgba: c, dist: best ? best.dist / box.dpr : null,
            text: c[3] === 0 ? 'nothing (transparent)' : 'rgb(' + c[0] + ', ' + c[1] + ', ' + c[2] + ')' + (best && best.dist > 0 ? ', ' + (best.dist / box.dpr).toFixed(1) + ' px away' : '') };
    }
    function isBurgundy(c) { return c[3] > 0 && c[0] > c[1] + 40 && c[0] > c[2] + 30 && c[0] < 215; }

    function onResize(el, fn) {
        var t = null;
        var run = function () {
            clearTimeout(t);
            t = setTimeout(function () { fn(); wakeClock(); }, 80);   /* a refit clears the canvas: let a held clock draw it again */
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

    /* requestAnimationFrame clock; tick(dt, t) gets dt = 0 while paused; while nothing shows the run it holds (showing(), at the end) */
    function clock(tick) {
        var playing = !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches), last = 0, t = 0, listeners = [];
        function frame(ts) { if (!showing()) { last = 0; return holdUntilShown(frame); }
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
            button.textContent = p ? T('Pause') : T('Play');
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
        b.textContent = T('This simulation stopped. ');
        el.appendChild(b);
        el.appendChild(document.createTextNode(String(message || T('Unknown error.')) + T(' Reload the page to try again.')));
        host.insertBefore(el, host.firstChild);
    }
    window.addEventListener('error', function (e) { showError(e.message); });

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

    /* The Algebra column is written as light HTML (<sub>, <sup>, Unicode symbols) with ⟦key|…⟧ marks.
       Once KaTeX has loaded, each line is translated to TeX and typeset like the lecture note; a mark becomes
       \htmlClass{k}{\htmlData{k=key}{…}}, so the hover link to the code and the table keeps working.
       A line KaTeX cannot read stays as the HTML it was written in. */
    var TEX_CHARS = {
        '−': '-', '·': '\\cdot ', '×': '\\times ', '½': '\\tfrac{1}{2}', '⅓': '\\tfrac{1}{3}', '⅔': '\\tfrac{2}{3}', '¼': '\\tfrac{1}{4}',
        '²': '^{2}', '³': '^{3}', '⁴': '^{4}', '⁻': '^{-}', '₀': '_{0}', '₁': '_{1}', '₂': '_{2}', '₃': '_{3}', '₄': '_{4}', '₅': '_{5}', '₆': '_{6}',
        '…': '\\ldots ', '⇒': '\\;\\Rightarrow\\; ', '⟺': '\\;\\Longleftrightarrow\\; ', '→': '\\to ', '←': '\\leftarrow ', '≈': '\\approx ', '≤': '\\le ',
        '≥': '\\ge ', '≠': '\\ne ', '±': '\\pm ', '∓': '\\mp ', '⌊': '\\lfloor ', '⌋': '\\rfloor ', '∫': '\\int ', '∂': '\\partial ', '∑': '\\sum ',
        '∞': '\\infty ', '°': '^{\\circ}', '√': '\\surd ', '∝': '\\propto ', '∈': '\\in ', '⟨': '\\langle ', '⟩': '\\rangle ', '|': '\\vert ',
        '%': '\\%', '#': '\\#', '&': '\\&', '_': '\\_', '{': '\\{', '}': '\\}', '\\': '\\backslash ', '$': '\\$', '~': '\\sim ', '^': '\\hat{}', ' ': '\\;'
    };
    var TEX_FUNCS = { sin: 1, cos: 1, tan: 1, exp: 1, ln: 1, log: 1, max: 1, min: 1, arg: 1, det: 1, sinh: 1, cosh: 1, tanh: 1, lim: 1 };
    function texText(s) {
        // phrases of words (three or more lower-case letters, or a function name) become \text{…} or \sin; the rest maps character by character
        var SUP = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-', '⁺': '+' };
        var SUB = { '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9' };
        s = s.replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+/g, function (r) { return '\u0003' + r.split('').map(function (c) { return SUP[c]; }).join('') + '\u0004'; })
             .replace(/[₀₁₂₃₄₅₆₇₈₉]+/g, function (r) { return '\u0005' + r.split('').map(function (c) { return SUB[c]; }).join('') + '\u0004'; })
             .replace(/ẍ/g, '\u0006').replace(/ẋ/g, '\u0007');
        return s.replace(/√\(([^()]*)\)/g, '\u0001$1\u0002').split(/([A-Za-z]{2,}(?:[  ]+[a-z]{2,})*)/).map(function (part, i, all) {
            if (i % 2) {
                if (TEX_FUNCS[part]) return '\\' + part + ' ';
                if (/^[a-z]{3,}/.test(part) || /\s/.test(part) || /^(kg|px|Hz|rad|kN|MN|ms|km|mm|cm|nm|kW|MW|GW|rpm|Pa)$/.test(part)) {
                    return (/\s$/.test(all[i - 1] || '') ? '\\ ' : '') + '\\text{' + part.replace(/ /g, ' ') + '}';
                }
                return part;
            }
            return part.split('').map(function (ch) {
                if (ch === '\u0001') return '\\sqrt{';
                if (ch === '\u0002') return '}';
                if (ch === '\u0003') return '^{';
                if (ch === '\u0005') return '_{';
                if (ch === '\u0004') return '}';
                if (ch === '\u0006') return '\\ddot{x}';
                if (ch === '\u0007') return '\\dot{x}';
                return Object.prototype.hasOwnProperty.call(TEX_CHARS, ch) ? TEX_CHARS[ch] : ch;
            }).join('');
        }).join('');
    }
    function htmlToTex(html) {
        var out = '', re = /<(\/?)(sub|sup|span|i|b|em|strong|br)\b([^>]*)>|⟦([A-Za-z0-9_]+)\||⟧|&(nbsp|emsp|ensp|thinsp|lt|gt|amp|minus|middot);/g, last = 0, m, stack = [];
        var ENT = { nbsp: ' ', emsp: '\\quad ', ensp: '\\;', thinsp: '\\,', lt: '<', gt: '>', amp: '\\&', minus: '-', middot: '\\cdot ' };
        while ((m = re.exec(html))) {
            out += texText(html.slice(last, m.index));
            last = re.lastIndex;
            if (m[4]) { out += '\\htmlClass{k}{\\htmlData{k=' + m[4] + '}{'; stack.push('}}'); continue; }
            if (m[0] === '⟧') { out += stack.pop() || ''; continue; }
            if (m[5]) { out += ENT[m[5]] === ' ' ? '\\;' : ENT[m[5]]; continue; }
            var tag = m[2], close = m[1] === '/';
            if (tag === 'sub' || tag === 'sup') { out += close ? '}' : (tag === 'sub' ? '_{' : '^{'); continue; }
            if (tag === 'span') {
                if (close) { out += stack.pop() || ''; continue; }
                if (/font-style:\s*normal/.test(m[3])) { out += (/\s$/.test(out) ? '\\ ' : '') + '\\textrm{'; stack.push('}'); } else stack.push('');
                continue;
            }
        }
        out += texText(html.slice(last));
        // an equation number set apart at the end of a line keeps its upright parentheses
        out = out.replace(/\\textrm\{\s*\\(sin|cos|tan|exp|ln|log|max|min|arg|det|sinh|cosh|tanh|lim)\s*\}/g, '\\$1 ')
                 .replace(/\\textrm\{\\text\{([^{}]*)\}\}/g, '\\textrm{$1}');
        return out.replace(/\\textrm\{\s*\((\d+[a-z]?)\)\s*\}/g, '\\qquad\\textrm{($1)}').replace(/(\\quad|\\;)\s*\((\d+[a-z]?)\)\s*$/, '\\qquad\\textrm{($2)}');
    }
    function algebra(math) {
        return String(math).split(/<br\s*\/?>/i).map(function (line) {
            if (window.katex) {
                try {
                    return '<div class="walk__line">' + window.katex.renderToString(htmlToTex(line), {
                        throwOnError: true, strict: 'ignore',
                        trust: function (c) { return c.command === '\\htmlClass' || c.command === '\\htmlData'; }
                    }) + '</div>';
                } catch (err) { /* keep the line as written */ }
            }
            return '<div class="walk__line">' + markup(line, false) + '</div>';
        }).join('');
    }

    function walkthrough(data) {
        var host = document.getElementById('walk');
        if (!host || !data) return;
        var cur = 0, held = false;
        host.innerHTML =
            T('<div class="walk__head"><h2>From symbols to code</h2><p>') + data.intro + '</p>' +
            T('<label class="switch walk__hold"><span>Hold the numbers</span><input type="checkbox"></label></div>') +
            T('<div class="walk__frame"><ol class="walk__steps" role="tablist" aria-label="Steps"></ol>') +
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
                '<div class="walk__top"><p class="walk__num">' + T('Step {i} of {n}', { i: i + 1, n: data.steps.length }) + '</p>' +
                '<h3>' + st.title + '</h3><p class="walk__where">' + esc(st.where) + '</p></div>' +
                T('<div class="walk__cols"><div class="walk__math"><p class="walk__label">Algebra</p>') +
                '<div class="eq walk__eq">' + algebra(st.math) + '</div><p class="walk__note">' + st.note + '</p></div>' +
                T('<div class="walk__code"><p class="walk__label">Code · as written in this page</p><pre><code>') + markup(st.code, true) + '</code></pre></div></div>' +
                '<div class="walk__tablewrap"><table class="walk__table"><thead><tr>' + T('<th>Symbol</th><th>In code</th><th class="now">Now</th><th>Meaning</th>') + '</tr></thead>' +
                '<tbody>' + rows + '</tbody></table></div>' +
                '<div class="walk__nav"><button type="button" class="btn btn--ghost" data-go="-1"' + (i === 0 ? ' disabled' : '') + '>' + T('← Previous') + '</button>' +
                '<button type="button" class="btn" data-go="1"' + (i === data.steps.length - 1 ? ' disabled' : '') + '>' + T('Next →') + '</button></div>';
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
        /* while held, every step shows the same frozen instant; a cell is written only when its text changes, and not while out of view */
        function update(force) {
            if ((held || !walkInView) && !force) return;
            var vals = held && snap ? snap : read();
            Array.prototype.forEach.call(card.querySelectorAll('[data-v]'), function (td) {
                var v = vals[td.getAttribute('data-v')], txt = v === undefined ? '—' : String(v);
                if (td.textContent !== txt) td.textContent = txt;
            });
        }
        var walkInView = true; if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { walkInView = es[es.length - 1].isIntersecting; }, { rootMargin: '200px 0px' }).observe(host); setInterval(update, 200);
        show(0);
        /* KaTeX may arrive after the first step was drawn: draw the step again, typeset */
        document.addEventListener('typeset', function () { show(cur); });
        if (window.Fold) window.Fold.walk(host);
    }

    /* ---------- lecture notes: KaTeX typesets \( … \) and \[ … \] in every .paper ---------- */
    function load(src, done) {
        var s = document.createElement('script');
        s.src = src;
        s.onload = done;
        s.onerror = done;
        document.head.appendChild(s);
    }
    function typeset() {
        var papers = document.querySelectorAll('.paper'), caps = document.querySelectorAll('.stage__cap, .formula');
        if (!papers.length && !caps.length) return;
        if (!papers.length) { if (Array.prototype.some.call(caps, function (c) { return c.textContent.indexOf('\\(') >= 0; })) mathIn(caps); return; }   /* KaTeX only if a caption holds maths */
        var skip = document.createElement('a');
        skip.className = 'skip-link';
        skip.href = '#' + (papers[0].id || 'paper');
        skip.textContent = T('Skip to the lecture note');
        document.body.insertBefore(skip, document.body.firstChild);
        function show() {
            Array.prototype.forEach.call(papers, function (p) { p.classList.add('is-typeset'); });
        }
        var fallback = setTimeout(show, 4000);
        load(ROOT + 'vendor/katex/katex.min.js', function () {
            load(ROOT + 'vendor/katex/contrib/auto-render.min.js', function () {
                clearTimeout(fallback);
                if (window.renderMathInElement) {
                    Array.prototype.forEach.call(papers, function (p) {
                        window.renderMathInElement(p, {
                            delimiters: [{ left: '\\[', right: '\\]', display: true }, { left: '\\(', right: '\\)', display: false }],
                            ignoredClasses: ['notex'],
                            throwOnError: false
                        });
                    });
                    renderCaps(caps);
                }
                show();
                document.dispatchEvent(new CustomEvent('typeset'));
            });
        });
        /* the contents list marks the section being read */
        var links = document.querySelectorAll('.paper__toc a[href^="#"]');
        if (!links.length || !('IntersectionObserver' in window)) return;
        var byId = {};
        Array.prototype.forEach.call(links, function (a) { byId[a.getAttribute('href').slice(1)] = a; });
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (en) {
                if (!en.isIntersecting || !byId[en.target.id]) return;
                Array.prototype.forEach.call(links, function (a) { a.classList.remove('is-here'); });
                byId[en.target.id].classList.add('is-here');
            });
        }, { rootMargin: '-20% 0px -70% 0px' });
        Object.keys(byId).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
    }

    /* the figure captions carry their equations in \\( … \\) too, set in the same mathematics as the lecture note */
    function renderCaps(caps) {
        Array.prototype.forEach.call(caps, function (c) {
            window.renderMathInElement(c, { delimiters: [{ left: '\\(', right: '\\)', display: false }], throwOnError: false });
        });
        document.documentElement.classList.add('tex-ready');
    }
    function mathIn(caps) {
        var fallback = setTimeout(function () { document.documentElement.classList.add('tex-ready'); }, 4000);
        load(ROOT + 'vendor/katex/katex.min.js', function () {
            load(ROOT + 'vendor/katex/contrib/auto-render.min.js', function () {
                clearTimeout(fallback);
                if (window.renderMathInElement) renderCaps(caps);
                document.dispatchEvent(new CustomEvent('typeset'));
            });
        });
    }

    function boot() {
        typeset();
        var host = document.getElementById('walk');
        if (!host || !host.getAttribute('data-walk')) return;   /* only an element that names its walkthrough */
        var s = document.createElement('script');
        s.charset = 'utf-8';
        s.src = (window.I18N_WALK ? ROOT + 'scripts/walk/' + document.documentElement.lang + '/' : '../scripts/walk/') + host.getAttribute('data-walk') + '.js';
        s.onload = function () { walkthrough((window.WALK || {})[host.getAttribute('data-walk')]); };
        document.body.appendChild(s);
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
    else boot();

    window.Sim = {
        theme: theme,
        canvas2d: canvas2d,
        tex: tex,
        ticks: ticks,
        readPixel: readPixel,
        isBurgundy: isBurgundy,
        onResize: onResize,
        slider: slider,
        clock: clock,
        playButton: playButton,
        fmt: fmt,
        showError: showError
    };
    /* Is anything that shows the run on screen? The figure (.sim__head, .sim__grid) or the walkthrough's live values (#walk), seen
       by an IntersectionObserver (it asks for no layout); or the data panel, open or recording. While none is, the clock holds:
       the simulation's time stands still, as in a hidden tab, and goes on from the same instant when the reader scrolls back.
       Without those elements or IntersectionObserver the clock always runs. See docs/performance.md, change 3. */
    var shown = null, wakeUntil = 0;
    function showing() {
        if (shown === null) {
            shown = { n: 1 };   /* until the observer first reports, count the run as seen */
            /* before printing too, the held figure is drawn again (see wakeClock) */
            window.addEventListener('beforeprint', wakeClock);
            var els = [].slice.call(document.querySelectorAll('.sim__head, .sim__grid, #walk'));
            if (!els.length || !('IntersectionObserver' in window)) shown.always = true;
            else {
                var vis = [];
                var io = new IntersectionObserver(function (es) {
                    es.forEach(function (e) { vis[els.indexOf(e.target)] = e.isIntersecting; });
                    shown.n = vis.filter(Boolean).length;
                }, { rootMargin: '200px 0px' });   /* wakes a little before the figure enters */
                els.forEach(function (el) { io.observe(el); });
            }
        }
        if (shown.always || shown.n > 0 || performance.now() < wakeUntil) return true;
        var dp = window.__dataPanel, tab = document.querySelector('.dp-tab');
        return !!(dp && dp.recording && dp.recording()) || !!(tab && tab.getAttribute('aria-expanded') === 'true');
    }
    /* Sim.onResize refits (and so clears) a canvas, and several pages draw it again only on their next tick: after a refit the clock
       runs for a second even when nothing shows the run, so a held figure is never left blank (a page opened deep in the note,
       a resize, a print) */
    var heldClocks = [];
    function wakeClock() {
        wakeUntil = performance.now() + 1000;
        var h = heldClocks; heldClocks = [];
        h.forEach(function (frame) { requestAnimationFrame(frame); });   /* at once, not at the next look of the timer */
    }
    /* while held: no frame is asked for; a timer looks again every 200 ms, and the first frame after it starts with dt = 0, so the run
       goes on from the same instant */
    function holdUntilShown(frame) {
        heldClocks.push(frame);
        setTimeout(function wait() {
            var i = heldClocks.indexOf(frame);
            if (i < 0) return;   /* woken already */
            if (showing()) { heldClocks.splice(i, 1); requestAnimationFrame(frame); } else setTimeout(wait, 200);
        }, 200);
    }
})();
