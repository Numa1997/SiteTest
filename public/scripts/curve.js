/* Numa Koudsie · parameter curves
   A knob that turns by itself. The reader picks a curve p(t) and one of the page's sliders; while the simulation plays,
   the slider follows the curve exactly as if a hand moved it: the page hears an ordinary 'input' event and answers as it
   always does. The curve's time runs on the page's own clock, so it pauses when the page pauses. A hand on the slider
   stops the curve at once.

   Every number of the curve is written into the page's store (scripts/dataset.js) where it is computed: the time of the
   run, the value p(t), the value the slider took (a slider moves in steps), the curve sampled for its chart, the reader's
   own points and the slopes between them. The chart and the data panel only read the store.

   var curve = Sim.curve({
       ds: ds,                                     the page's dataset
       after: element,                             the panel group the curve's group is placed after
       knobs: [{ id: 'lambda', slider: lambda, name, symbol: 'λ', units: 'px', digits: 1 }],   name: the slider's label, translated
       examples: [{ knob: 'lambda', shape: 'inv', from: 64, to: 16, T: 30, loop: false, name, why }],   name, why: translated words
       play: function () { clk.set(true); },      starts the page's clock
       playing: function () { return clk.playing; },
       extra: function () { return text; }        optional: one more fact for the status line while a curve runs
   });
   curve.step(dt)              in the page's clock callback, before the page reads its sliders
   curve.extend(Sim.data)      adds the curve's group, checks and read-backs to the data panel
   curve.round(spec)           a page's round, which becomes the rest of the curve run while a curve plays
   curve.running()             true while a curve moves a knob

   Shapes, with u = t / T the fraction of the run done, a the value at the start and b at the end:
     line   p = a + (b − a) u                                  a straight ramp
     jerk   p = a + (b − a)(10u³ − 15u⁴ + 6u⁵)                 minimum jerk (Flash & Hogan 1985): starts and stops at rest
     exp    p = a (b/a)^u                                      exponential sweep: equal time per doubling (Farina)
     inv    p = 1 / (1/a + (1/b − 1/a) u)                      1/p changes at a steady rate
     tri    p = a + (b − a)(1 − |2u − 1|)                      there and back at a steady rate
     swell  p = a + (b − a)(1 − cos 2πu) / 2                   a smooth swell to b and back
     own    monotone cubic through the reader's points (Fritsch & Carlson 1980): never overshoots them */
(function () {
    'use strict';
    var Sim = window.Sim || (window.Sim = {});
    var NQ = 201;

    var SHAPES = {
        line:  { name: _t('Straight ramp'), formula: 'p = a + (b − a) u',
                 why: _t('The knob moves at a constant rate from a to b. The plainest sweep; its rate jumps from zero at the start and back to zero at the end.'),
                 f: function (u, a, b) { return a + (b - a) * u; } },
        jerk:  { name: _t('Smooth S-curve (minimum jerk)'), formula: 'p = a + (b − a)(10u³ − 15u⁴ + 6u⁵)',
                 why: _t('Starts and ends at rest, with no jump in the rate or in its rate of change: of all paths from a to b in the time T, it is the one whose rate changes most gently (least jerk, the third derivative). Flash and Hogan found that the human hand moves this way between two targets (J. Neurosci. 5, 1688–1703, 1985). Its fastest moment is halfway, at 15/8 of the average rate.'),
                 f: function (u, a, b) { return a + (b - a) * u * u * u * (10 - 15 * u + 6 * u * u); } },
        exp:   { name: _t('Exponential sweep'), formula: 'p = a (b/a)<sup>u</sup>', positive: true,
                 why: _t('Equal time for every doubling or halving: the swept sine acousticians use to measure rooms and loudspeakers (A. Farina, exponential sine sweep; equation 18 of his notes for the 23rd Nordic Sound Symposium, 2007). Needs a and b of the same sign.'),
                 f: function (u, a, b) { return a * Math.pow(b / a, u); } },
        inv:   { name: _t('Steady in 1/p'), formula: 'p = 1 / (1/a + (1/b − 1/a) u)', positive: true,
                 why: _t('The reciprocal 1/p changes at a steady rate. Use it for a quantity whose effect goes as one over the knob. Needs a and b of the same sign.'),
                 f: function (u, a, b) { return 1 / (1 / a + (1 / b - 1 / a) * u); } },
        tri:   { name: _t('There and back'), formula: 'p = a + (b − a)(1 − |2u − 1|)',
                 why: _t('From a to b in half the time, then back to a at the same steady rate. With Repeat on, the knob sweeps to and fro.'),
                 f: function (u, a, b) { return a + (b - a) * (1 - Math.abs(2 * u - 1)); } },
        swell: { name: _t('Swell and return'), formula: 'p = a + (b − a)(1 − cos 2πu) / 2',
                 why: _t('A smooth swell from a to b and back, at rest at both ends of the run and at the top: like breathing. With Repeat on it never jolts.'),
                 f: function (u, a, b) { return a + (b - a) * (1 - Math.cos(2 * Math.PI * u)) / 2; } },
        own:   { name: _t('Your own curve'), formula: _t('monotone cubic through your points'),
                 why: _t('Click the chart to add a point, drag a point to move it, double-click a point to remove it; the first and last points move only up and down. Between your points the curve is a monotone cubic (Fritsch and Carlson, SIAM J. Numer. Anal. 17, 238–246, 1980): it never overshoots them, so the knob stays between the values you set. Keys: ← → choose a point, ↑ ↓ move it, Delete removes it.') }
    };
    var GENERIC = ['line', 'jerk', 'exp', 'tri', 'swell'];

    /* Fritsch–Carlson slopes for a monotone cubic Hermite curve through (xs, ys): secants, averaged slopes, zero at a turn,
       and each pair (α, β) = (m_k, m_k+1)/δ_k pulled back inside the circle of radius 3, which keeps every piece monotone */
    function slopes(xs, ys) {
        var n = xs.length, d = [], m = [], k;
        if (n < 2) return [0];
        for (k = 0; k < n - 1; k++) d[k] = (ys[k + 1] - ys[k]) / (xs[k + 1] - xs[k]);
        m[0] = d[0]; m[n - 1] = d[n - 2];
        for (k = 1; k < n - 1; k++) m[k] = d[k - 1] * d[k] <= 0 ? 0 : (d[k - 1] + d[k]) / 2;
        for (k = 0; k < n - 1; k++) {
            if (d[k] === 0) { m[k] = 0; m[k + 1] = 0; continue; }
            var al = m[k] / d[k], be = m[k + 1] / d[k];
            if (al < 0) { m[k] = 0; al = 0; }
            if (be < 0) { m[k + 1] = 0; be = 0; }
            var s = al * al + be * be;
            if (s > 9) { var tau = 3 / Math.sqrt(s); m[k] = tau * al * d[k]; m[k + 1] = tau * be * d[k]; }
        }
        return m;
    }
    /* the cubic Hermite piece between two points: h00 = 2s³ − 3s² + 1, h10 = s³ − 2s² + s, h01 = −2s³ + 3s², h11 = s³ − s² */
    function hermite(xs, ys, ms, x) {
        var n = xs.length, k = 0;
        if (n === 1 || x <= xs[0]) return ys[0];
        if (x >= xs[n - 1]) return ys[n - 1];
        while (k < n - 2 && x > xs[k + 1]) k++;
        var h = xs[k + 1] - xs[k], s = (x - xs[k]) / h, s2 = s * s, s3 = s2 * s;
        return ys[k] * (2 * s3 - 3 * s2 + 1) + h * ms[k] * (s3 - 2 * s2 + s) + ys[k + 1] * (3 * s2 - 2 * s3) + h * ms[k + 1] * (s3 - s2);
    }
    /* the value v put on a range slider's steps, counted from its minimum, inside its range, and written with as many decimals
       as the step has (0.1 → one), so that 16 + 397 · 0.1 is stored as 55.7 and not 55.70000000000001 */
    function snap(el, v) {
        var lo = parseFloat(el.min), hi = parseFloat(el.max), st = parseFloat(el.step) || 1;
        var dec = (String(el.step || '1').split('.')[1] || '').length;
        var q = Math.min(hi, Math.max(lo, lo + Math.round((v - lo) / st) * st));
        return +q.toFixed(dec);
    }

    Sim.curve = function (opts) {
        var ds = opts.ds, knobs = opts.knobs, examples = opts.examples || [];
        var st = { on: false, k: 0, shape: 'line', ex: -1, a: 0, b: 1, T: 10, loop: false, t: 0, runs: 0, pts: null, sel: -1, msg: '', shownAt: 0 };
        var C = Sim.theme;
        function knob() { return knobs[st.k]; }
        function lo() { return parseFloat(knob().slider.el.min); }
        function hi() { return parseFloat(knob().slider.el.max); }
        function fmtv(v) { return Sim.fmt(v, knob().digits); }

        /* ---------- the store ---------- */
        function declare() {
            var kb = knob(), un = kb.units || '', dg = kb.digits;
            ds.var('cv_on', [], 'bool', { symbol: _t('curve on'), long_name: 'a curve is moving a knob now', computed_in: 'curve: Play curve, Stop, the end of a run, a hand on the knob' });
            ds.var('cv_knob', [], 'str', { symbol: _t('knob'), long_name: 'the slider the curve moves', computed_in: 'curve: Knob' });
            ds.var('cv_name', [], 'str', { symbol: _t('curve'), long_name: 'the curve chosen', computed_in: 'curve: Curve' });
            ds.var('cv_formula', [], 'str', { symbol: 'p(u)', long_name: 'the formula of the curve, with u = t_c / T_c', computed_in: 'curve: Curve' });
            ds.var('cv_a', [], 'float', { symbol: 'a', units: un, long_name: 'value of the curve at the start of a run, u = 0', computed_in: 'curve: From', digits: dg + 2 });
            ds.var('cv_b', [], 'float', { symbol: 'b', units: un, long_name: 'value of the curve at the end of a run, u = 1 (for There and back and Swell: at the turn)', computed_in: 'curve: To', digits: dg + 2 });
            ds.var('cv_T', [], 'float', { symbol: 'T<sub>c</sub>', units: 's', long_name: 'duration of one run of the curve', computed_in: 'curve: Time', digits: 1 });
            ds.var('cv_loop', [], 'bool', { symbol: _t('repeat'), long_name: 'the curve starts again at the end of a run', computed_in: 'curve: Repeat' });
            ds.var('cv_t', [], 'float', { symbol: 't<sub>c</sub>', units: 's', long_name: 'time since the run began, on the page clock', computed_in: 'curve.step()', formula: 't<sub>c</sub> ← t<sub>c</sub> + Δt, back by T<sub>c</sub> when a repeated run ends', digits: 3, source: 'Accumulated frame by frame from the page clock.' });
            ds.var('cv_u', [], 'float', { symbol: 'u', long_name: 'fraction of the run done', computed_in: 'curve.step()', formula: 'u = t<sub>c</sub> / T<sub>c</sub>', digits: 4 });
            ds.var('cv_p', [], 'float', { symbol: 'p(u)', units: un, long_name: 'the value of the curve now', computed_in: 'curve.step()', formula: 'the formula p(u) above', digits: dg + 3 });
            ds.var('cv_set', [], 'float', { symbol: 'p<sub>set</sub>', units: un, long_name: 'the value the slider took: p(u) on the slider’s steps; this is what the simulation uses', computed_in: 'curve.step()', formula: 'min + round((p − min) / step) · step, kept inside the range', digits: dg + 2 });
            ds.var('cv_runs', [], 'int', { symbol: _t('runs'), long_name: 'runs of the curve finished since Play curve', computed_in: 'curve.step()', digits: 0, source: 'Counted at the end of each run.' });
            ds.var('cv_tq', ['cq'], Float64Array, { symbol: 't<sub>q</sub>', units: 's', long_name: 'times at which the curve is sampled for its chart', computed_in: 'curve: resample()', formula: 't<sub>q</sub> = q T<sub>c</sub> / 200', digits: 3, coordinate: true });
            ds.var('cv_pq', ['cq'], Float64Array, { symbol: 'p<sub>q</sub>', units: un, long_name: 'the curve at those times, as its chart draws it', computed_in: 'curve: resample()', formula: 'p(q / 200)', digits: dg + 3 });
            ds.var('cv_ku', ['ck'], Float64Array, { symbol: 'u<sub>k</sub>', long_name: 'your points: fraction of the run', computed_in: 'curve: your points', digits: 4, coordinate: true });
            ds.var('cv_kp', ['ck'], Float64Array, { symbol: 'p<sub>k</sub>', units: un, long_name: 'your points: value of the knob', computed_in: 'curve: your points', digits: dg + 2 });
            ds.var('cv_km', ['ck'], Float64Array, { symbol: 'm<sub>k</sub>', units: un ? un + _t(' per run') : _t('per run'), long_name: 'slope of the curve at each of your points (Fritsch–Carlson)', computed_in: 'curve: slopes()', formula: 'average of the neighbouring secants; 0 at a turn; (α, β) kept inside the circle of radius 3', digits: dg + 3 });
        }
        ds.dim('cq', NQ);
        ds.dim('ck', 0);

        function value(u) {
            u = Math.max(0, Math.min(1, u));
            if (st.shape === 'own') return hermite(ds.get('cv_ku'), ds.get('cv_kp'), ds.get('cv_km'), u);
            return SHAPES[st.shape].f(u, st.a, st.b);
        }
        function storePoints() {
            ds.dim('ck', st.pts.length);
            var ku = ds.alloc('cv_ku'), kp = ds.alloc('cv_kp'), km = ds.alloc('cv_km');
            st.pts.forEach(function (q, i) { ku[i] = q.u; kp[i] = q.p; });
            var m = slopes(Array.prototype.slice.call(ku), Array.prototype.slice.call(kp));
            for (var i = 0; i < m.length; i++) km[i] = m[i];
            ds.touch('cv_ku'); ds.touch('cv_kp'); ds.touch('cv_km');
            st.a = st.pts[0].p; st.b = st.pts[st.pts.length - 1].p;
        }
        function resample() {
            if (st.shape === 'own') storePoints();
            var tq = ds.alloc('cv_tq'), pq = ds.alloc('cv_pq');
            for (var q = 0; q < NQ; q++) { tq[q] = q * st.T / (NQ - 1); pq[q] = value(q / (NQ - 1)); }
            ds.touch('cv_tq'); ds.touch('cv_pq');
            ds.set('cv_a', st.a); ds.set('cv_b', st.b); ds.set('cv_T', st.T); ds.set('cv_loop', st.loop);
            ds.set('cv_knob', knob().id); ds.set('cv_name', currentName());
            ds.set('cv_formula', SHAPES[st.shape].formula.replace(/<\/?sup>/g, ''));
            ds.set('cv_u', st.T > 0 ? Math.min(1, st.t / st.T) : 0);
            ds.set('cv_p', value(ds.get('cv_u')));
        }
        function currentName() { return st.ex >= 0 ? examples[st.ex].name : SHAPES[st.shape].name; }

        /* ---------- moving the knob ---------- */
        var own = false;   /* true while this file moves the slider, so the page's 'input' handler is not taken for a hand */
        function apply(p) {
            if (!isFinite(p)) return;
            var el = knob().slider.el, before = el.value;
            el.value = String(snap(el, p));
            ds.set('cv_set', parseFloat(el.value));
            if (el.value !== before) { own = true; el.dispatchEvent(new Event('input', { bubbles: true })); own = false; }
        }
        function begin() {
            if (SHAPES[st.shape].positive && !(st.a * st.b > 0)) { st.msg = _t('This curve needs From and To of the same sign, neither zero.'); show(true); return; }
            st.t = 0; st.runs = 0; st.on = true; st.msg = '';
            ds.set('cv_on', true); ds.set('cv_t', 0); ds.set('cv_runs', 0);
            resample();
            apply(ds.get('cv_p'));
            if (opts.play && opts.playing && !opts.playing()) opts.play();
            paintButtons(); draw(); show(true);
        }
        function end(msg) {
            if (!st.on && !msg) return;
            st.on = false; st.msg = msg || '';
            ds.set('cv_on', false);
            paintButtons(); draw(); show(true);
        }
        function step(dt) {
            if (!st.on) return;
            if (dt > 0) {
                st.t += dt;
                if (st.t >= st.T) {
                    if (st.loop) { st.runs += Math.floor(st.t / st.T); st.t -= Math.floor(st.t / st.T) * st.T; }
                    else { st.t = st.T; st.runs += 1; }
                }
                ds.set('cv_t', st.t); ds.set('cv_runs', st.runs);
                var u = st.T > 0 ? st.t / st.T : 1;
                ds.set('cv_u', u);
                ds.set('cv_p', value(u));
                apply(ds.get('cv_p'));
                if (!st.loop && st.t >= st.T) { end(_t('Done: {sym} reached {v} {units}. Play again, change the curve, or pick another.', { sym: knob().symbol, v: fmtv(ds.get('cv_set')), units: knob().units || '' })); return; }
            }
            draw();
            show(false);
        }

        /* ---------- the panel group ---------- */
        var g = document.createElement('div');
        g.className = 'panel__group curve';
        g.setAttribute('role', 'group');
        g.setAttribute('aria-label', _t('Curve: a knob that moves by itself'));
        g.innerHTML =
            '<p class="panel__label">' + _t('Curve · a knob that moves by itself') + '</p>' +
            '<label class="ctl"><span class="ctl__row"><span>' + _t('Curve') + '</span></span><select class="sel" data-cv="shape"></select></label>' +
            '<label class="ctl"><span class="ctl__row"><span>' + _t('Knob it moves') + '</span></span><select class="sel" data-cv="knob"></select></label>' +
            '<p class="curve__why" data-cv="why"></p>' +
            '<div class="curve__plot"><canvas data-cv="plot" tabindex="0"></canvas></div>' +
            '<p class="curve__hint" data-cv="hint">' + _t('Click or drag on the chart to make this curve your own.') + '</p>' +
            '<div class="curve__nums">' +
                '<label><span>' + _t('From a') + '</span><input type="number" class="sel" data-cv="a"></label>' +
                '<label><span>' + _t('To b') + '</span><input type="number" class="sel" data-cv="b"></label>' +
                '<label><span>' + _t('Time T, s') + '</span><input type="number" class="sel" data-cv="T" min="1" max="600" step="1"></label>' +
            '</div>' +
            '<label class="curve__loop"><input type="checkbox" data-cv="loop"> ' + _t('Repeat') + '</label>' +
            '<div class="actions"><button type="button" class="btn" data-cv="go">' + _t('Play curve') + '</button>' +
            '<button type="button" class="btn btn--ghost" data-cv="stop">' + _t('Stop') + '</button></div>' +
            '<p class="curve__st" data-cv="st"></p>';
        opts.after.insertAdjacentElement('afterend', g);
        function $(k) { return g.querySelector('[data-cv="' + k + '"]'); }
        var selShape = $('shape'), selKnob = $('knob'), why = $('why'), hint = $('hint'), plot = $('plot'), inA = $('a'), inB = $('b'), inT = $('T'), inLoop = $('loop'), btnGo = $('go'), btnStop = $('stop'), stEl = $('st');
        plot.setAttribute('aria-label', _t('Chart of the curve: time across, the knob’s value up; a dot marks the value now.'));

        function fillShapes() {
            var h = '';
            if (examples.length) {
                h += '<optgroup label="' + _t('Examples for this simulation') + '">';
                examples.forEach(function (ex, i) {
                    var kb = knobs.filter(function (q) { return q.id === ex.knob; })[0];
                    h += '<option value="ex:' + i + '">' + kb.symbol + ' · ' + ex.name + '</option>';
                });
                h += '</optgroup>';
            }
            h += '<optgroup label="' + _t('Shapes for any knob') + '">';
            GENERIC.forEach(function (s) { h += '<option value="sh:' + s + '">' + SHAPES[s].name + '</option>'; });
            h += '</optgroup><option value="sh:own">' + SHAPES.own.name + '</option>';
            selShape.innerHTML = h;
            selKnob.innerHTML = knobs.map(function (kb, i) { return '<option value="' + i + '">' + kb.name + '</option>'; }).join('');
        }
        function setInputs() {
            var el = knob().slider.el;
            [inA, inB].forEach(function (inp) { inp.min = el.min; inp.max = el.max; inp.step = el.step || 'any'; });
            inA.value = +st.a.toFixed(6); inB.value = +st.b.toFixed(6); inT.value = st.T; inLoop.checked = st.loop;
            inA.disabled = inB.disabled = false;
            selShape.value = st.ex >= 0 ? 'ex:' + st.ex : 'sh:' + st.shape;
            selKnob.value = String(st.k);
            hint.hidden = st.shape === 'own';
            var ex = st.ex >= 0 ? examples[st.ex] : null;
            why.innerHTML = (ex ? ex.why + ' ' : '') + '<span class="curve__f">' + SHAPES[st.shape].formula + (st.shape === 'own' ? '' : ', u = t / T') + '</span>' + (ex ? '' : ' ' + SHAPES[st.shape].why);
        }
        function ownFrom(shape) {
            /* your own curve starts as the shape on screen, read at five points */
            st.pts = [0, 0.25, 0.5, 0.75, 1].map(function (u) { return { u: u, p: Math.min(hi(), Math.max(lo(), SHAPES[shape].f(u, st.a, st.b))) }; });
            st.sel = -1;
        }
        function choose(v) {
            if (st.on) end(_t('Stopped: you changed the curve.'));
            if (v.slice(0, 3) === 'ex:') {
                var ex = examples[+v.slice(3)];
                st.ex = +v.slice(3);
                st.k = knobs.map(function (q) { return q.id; }).indexOf(ex.knob);
                st.shape = ex.shape; st.a = ex.from; st.b = ex.to; st.T = ex.T; st.loop = !!ex.loop;
            } else {
                var s = v.slice(3), from = st.shape;
                st.ex = -1;
                if (s === 'own') { if (from !== 'own') ownFrom(from); }
                else if (SHAPES[s].positive && !(st.a * st.b > 0)) { st.a = Math.max(lo(), parseFloat(knob().slider.el.step) || 1); st.b = hi(); }
                st.shape = s;
            }
            declare(); resample(); setInputs(); draw(); show(true);
        }
        selShape.addEventListener('change', function () { choose(selShape.value); });
        selKnob.addEventListener('change', function () {
            if (st.on) end(_t('Stopped: you changed the curve.'));
            st.k = +selKnob.value; st.ex = -1;
            st.a = lo(); st.b = hi();
            if (SHAPES[st.shape].positive && !(st.a * st.b > 0)) st.a = Math.max(lo(), parseFloat(knob().slider.el.step) || 1);
            if (st.shape === 'own') ownFrom('line');
            declare(); resample(); setInputs(); draw(); show(true);
        });
        function readNums() {
            var a = parseFloat(inA.value), b = parseFloat(inB.value), T = parseFloat(inT.value);
            if (isFinite(a)) st.a = Math.min(hi(), Math.max(lo(), a));
            if (isFinite(b)) st.b = Math.min(hi(), Math.max(lo(), b));
            if (isFinite(T)) st.T = Math.min(600, Math.max(1, T));
            if (st.shape === 'own') { st.pts[0].p = st.a; st.pts[st.pts.length - 1].p = st.b; }
            st.loop = inLoop.checked;
            if (st.t > st.T) st.t = st.T;
            resample(); draw(); show(true);
        }
        [inA, inB, inT].forEach(function (inp) { inp.addEventListener('change', function () { readNums(); setInputs(); }); });
        inLoop.addEventListener('change', readNums);
        btnGo.addEventListener('click', begin);
        btnStop.addEventListener('click', function () { end(_t('Stopped. The knob stays where the curve left it.')); });
        function paintButtons() { btnStop.disabled = !st.on; btnGo.textContent = st.on ? _t('Play again') : _t('Play curve'); }

        /* a hand on the knob wins: the curve stops */
        knobs.forEach(function (kb, i) {
            kb.slider.el.addEventListener('input', function () { if (!own && st.on && st.k === i) end(_t('You took the knob, so the curve stopped.')); });
        });

        /* the status line: words rewritten at most four times a second, like the data panel's */
        function show(now) {
            var ms = performance.now();
            if (!now && ms - st.shownAt < 250) return;
            st.shownAt = ms;
            var kb = knob(), txt;
            if (st.on) {
                txt = _t('{sym} = {v} {units} · {t} s of {T} s', { sym: kb.symbol, v: fmtv(ds.get('cv_set')), units: kb.units || '', t: Sim.fmt(st.t, 1), T: Sim.fmt(st.T, 0) });
                if (st.loop) txt += ' · ' + _t('run {n}', { n: st.runs + 1 });
                if (opts.playing && !opts.playing()) txt += ' · ' + _t('paused: the curve goes on when the simulation plays');
            } else txt = st.msg || _t('Press Play curve: the knob follows the curve while you watch the figure.');
            var ex = st.on && opts.extra ? opts.extra() : '';
            if (ex) txt += ' · ' + ex;
            if (txt !== stEl.textContent) stEl.textContent = txt;
        }

        /* ---------- the chart: drawn from the stored samples, the marker every frame ---------- */
        var box = Sim.canvas2d(plot), R = { x0: 0, x1: 1, y0: 1, y1: 0 }, drawnAt = null;
        function px(u) { return R.x0 + (R.x1 - R.x0) * u; }
        function py(p) { return R.y0 + (R.y1 - R.y0) * (p - lo()) / (hi() - lo()); }
        function draw() {
            var c = box.ctx, W = box.w, H = box.h, tq = ds.get('cv_tq'), pq = ds.get('cv_pq'), kb = knob();
            c.clearRect(0, 0, W, H);
            c.fillStyle = '#fff'; c.fillRect(0, 0, W, H);
            c.font = C.mono; c.textBaseline = 'middle';
            var labLo = fmtv(lo()), labHi = fmtv(hi());
            R.x0 = 10 + Math.max(c.measureText(labLo).width, c.measureText(labHi).width); R.x1 = W - 10; R.y0 = H - 22; R.y1 = 10;
            c.strokeStyle = C.ruleSoft; c.lineWidth = 1;
            c.beginPath(); c.moveTo(R.x0, Math.round(R.y1) + 0.5); c.lineTo(R.x1, Math.round(R.y1) + 0.5); c.moveTo(R.x0, Math.round(R.y0) + 0.5); c.lineTo(R.x1, Math.round(R.y0) + 0.5); c.stroke();
            c.fillStyle = C.muted; c.textAlign = 'right';
            c.fillText(labHi, R.x0 - 5, R.y1); c.fillText(labLo, R.x0 - 5, R.y0);
            c.textAlign = 'left'; c.textBaseline = 'alphabetic';
            c.fillText('0', R.x0, H - 6);
            c.textAlign = 'right'; c.fillText(Sim.fmt(st.T, 0) + ' s', R.x1, H - 6);
            c.textAlign = 'center'; c.fillText(kb.symbol + (kb.units ? ', ' + kb.units : ''), (R.x0 + R.x1) / 2, H - 6);
            c.save(); c.beginPath(); c.rect(R.x0 - 1, R.y1 - 6, R.x1 - R.x0 + 2, R.y0 - R.y1 + 12); c.clip();
            c.strokeStyle = C.accent; c.lineWidth = 2; c.lineJoin = 'round'; c.beginPath();
            for (var q = 0; q < NQ; q++) { var x = px(tq[q] / st.T), y = py(pq[q]); if (q) c.lineTo(x, y); else c.moveTo(x, y); }
            c.stroke();
            c.restore();
            if (st.shape === 'own') {
                st.pts.forEach(function (pt, i) {
                    c.beginPath(); c.arc(px(pt.u), py(pt.p), i === st.sel ? 5.5 : 4.5, 0, 2 * Math.PI);
                    c.fillStyle = i === st.sel ? C.accent : C.card; c.fill(); c.lineWidth = 1.5; c.strokeStyle = C.ink; c.stroke();
                });
            }
            drawnAt = null;
            if (st.on || st.t > 0) {
                var u = ds.get('cv_u'), xn = px(u), yn = py(ds.get('cv_p'));
                c.strokeStyle = C.rule; c.lineWidth = 1; c.beginPath(); c.moveTo(Math.round(xn) + 0.5, R.y1); c.lineTo(Math.round(xn) + 0.5, R.y0); c.stroke();
                c.beginPath(); c.arc(xn, yn, 5, 0, 2 * Math.PI); c.fillStyle = C.accent; c.fill(); c.lineWidth = 2; c.strokeStyle = C.card; c.stroke();
                c.beginPath(); c.arc(xn, yn, 2.5, 0, 2 * Math.PI); c.fillStyle = C.accent; c.fill();
                drawnAt = { x: xn, y: yn };
            }
        }
        Sim.onResize(plot, function () { box.fit(); draw(); });

        /* your own curve: click to add, drag to move, double-click to remove; a preset dragged becomes your own */
        var drag = -1;
        function at(e) { var r = plot.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
        function toU(x) { return Math.max(0, Math.min(1, (x - R.x0) / (R.x1 - R.x0))); }
        function toP(y) { return Math.max(lo(), Math.min(hi(), lo() + (y - R.y0) / (R.y1 - R.y0) * (hi() - lo()))); }
        function hit(m) {
            var best = -1, bd = 12;
            (st.pts || []).forEach(function (pt, i) { var d = Math.hypot(px(pt.u) - m.x, py(pt.p) - m.y); if (d < bd) { bd = d; best = i; } });
            return best;
        }
        function movePoint(i, u, p) {
            var n = st.pts.length;
            if (i === 0) u = 0; else if (i === n - 1) u = 1;
            else u = Math.max(st.pts[i - 1].u + 0.01, Math.min(st.pts[i + 1].u - 0.01, u));
            st.pts[i].u = u; st.pts[i].p = p;
        }
        function becomeOwn() {
            if (st.shape === 'own') return;
            ownFrom(st.shape); st.shape = 'own'; st.ex = -1;
            declare(); setInputs();
        }
        plot.addEventListener('pointerdown', function (e) {
            if (e.button !== 0) return;
            var m = at(e);
            becomeOwn();
            var i = hit(m);
            if (i < 0) {
                var u = toU(m.x), k = 0;
                while (k < st.pts.length && st.pts[k].u < u) k++;
                if (k === 0 || k === st.pts.length || st.pts[k].u - u < 0.01 || u - st.pts[k - 1].u < 0.01) { resample(); draw(); return; }
                st.pts.splice(k, 0, { u: u, p: toP(m.y) });
                i = k;
            }
            st.sel = drag = i;
            plot.setPointerCapture(e.pointerId);
            resample(); setInputs(); draw(); show(true);
            e.preventDefault();
        });
        plot.addEventListener('pointermove', function (e) {
            if (drag < 0) return;
            var m = at(e);
            movePoint(drag, toU(m.x), toP(m.y));
            resample(); draw(); show(false);
        });
        function release() { if (drag >= 0) { drag = -1; setInputs(); show(true); } }
        plot.addEventListener('pointerup', release);
        plot.addEventListener('pointercancel', release);
        plot.addEventListener('dblclick', function (e) {
            if (st.shape !== 'own') return;
            var i = hit(at(e));
            if (i > 0 && i < st.pts.length - 1) { st.pts.splice(i, 1); st.sel = -1; resample(); setInputs(); draw(); show(true); }
        });
        plot.addEventListener('keydown', function (e) {
            if (st.shape !== 'own' && /^Arrow/.test(e.key)) becomeOwn();
            if (st.shape !== 'own') return;
            var n = st.pts.length, d = (hi() - lo()) / (e.shiftKey ? 10 : 100);
            if (e.key === 'ArrowRight') st.sel = Math.min(n - 1, st.sel + 1);
            else if (e.key === 'ArrowLeft') st.sel = Math.max(0, st.sel < 0 ? 0 : st.sel - 1);
            else if ((e.key === 'ArrowUp' || e.key === 'ArrowDown') && st.sel >= 0) movePoint(st.sel, st.pts[st.sel].u, Math.max(lo(), Math.min(hi(), st.pts[st.sel].p + (e.key === 'ArrowUp' ? d : -d))));
            else if ((e.key === 'Delete' || e.key === 'Backspace') && st.sel > 0 && st.sel < n - 1) { st.pts.splice(st.sel, 1); st.sel = -1; }
            else return;
            e.preventDefault();
            resample(); setInputs(); draw(); show(true);
        });

        /* first state: the page's first example, or a straight ramp over the first knob's range */
        fillShapes();
        if (examples.length) choose('ex:0');
        else { st.a = lo(); st.b = hi(); choose('sh:line'); }
        ds.set('cv_on', false); ds.set('cv_t', 0); ds.set('cv_runs', 0); ds.set('cv_set', knob().slider.value);
        paintButtons();

        /* ---------- the data panel: a group, checks from the stored inputs, read-backs from the chart and the slider ---------- */
        var VARS = ['cv_on', 'cv_knob', 'cv_name', 'cv_formula', 'cv_a', 'cv_b', 'cv_T', 'cv_loop', 'cv_t', 'cv_u', 'cv_p', 'cv_set', 'cv_runs', 'cv_tq', 'cv_pq', 'cv_ku', 'cv_kp', 'cv_km'];
        function storedValue(u) {
            /* the curve worked out again from the store alone: the shape's formula with the stored a, b, or your stored points */
            if (st.shape === 'own') {
                var xs = Array.prototype.slice.call(ds.get('cv_ku')), ys = Array.prototype.slice.call(ds.get('cv_kp'));
                return hermite(xs, ys, slopes(xs, ys), u);
            }
            return SHAPES[st.shape].f(Math.max(0, Math.min(1, u)), ds.get('cv_a'), ds.get('cv_b'));
        }
        function inputsAB() {
            var un = knob().units || '', dg = knob().digits + 2;
            if (st.shape === 'own') return [['u<sub>k</sub>, p<sub>k</sub>', ds.get('cv_ku').length + _t(' points'), '', 0]];
            return [['a', ds.get('cv_a'), un, dg], ['b', ds.get('cv_b'), un, dg]];
        }
        function extend(spec) {
            spec.groups = spec.groups || [];
            spec.groups.push({ title: _t('Parameter curve'), note: _t('a knob that moves by itself: the curve you chose, and where its run is'), vars: VARS });
            if (spec.ledger && spec.ledger.sections) spec.ledger.sections.push({ title: _t('Parameter curve'), note: _t('a knob that moves by itself: the curve you chose, and where its run is'), vars: VARS, how: 'set' });
            spec.check = spec.check || {};
            spec.drawn = spec.drawn || {};
            spec.check.cv_u = function () { return { formula: 'u = t<sub>c</sub> / T<sub>c</sub>', inputs: [['t<sub>c</sub>', ds.get('cv_t'), 's', 3], ['T<sub>c</sub>', ds.get('cv_T'), 's', 1]], value: ds.get('cv_t') / ds.get('cv_T') }; };
            spec.check.cv_p = function () { return { formula: ds.get('cv_formula') + ', u = ' + Sim.fmt(ds.get('cv_u'), 4), inputs: [['u', ds.get('cv_u'), '', 4]].concat(inputsAB()), value: storedValue(ds.get('cv_u')) }; };
            spec.check.cv_set = function () {
                var el = knob().slider.el;
                return { formula: 'min + round((p − min) / step) · step', inputs: [['p', ds.get('cv_p'), knob().units || '', knob().digits + 3], ['min', parseFloat(el.min), '', 3], ['step', parseFloat(el.step) || 1, '', 3]], value: snap(el, ds.get('cv_p')) };
            };
            spec.check.cv_tq = function (q) { return { formula: 'q T<sub>c</sub> / 200', inputs: [['q', q, '', 0], ['T<sub>c</sub>', ds.get('cv_T'), 's', 1]], value: q * ds.get('cv_T') / (NQ - 1) }; };
            spec.check.cv_pq = function (q) { return { formula: ds.get('cv_formula') + ', u = q / 200', inputs: [['q', q, '', 0]].concat(inputsAB()), value: storedValue(q / (NQ - 1)) }; };
            spec.check.cv_km = function (k) {
                var xs = Array.prototype.slice.call(ds.get('cv_ku')), ys = Array.prototype.slice.call(ds.get('cv_kp'));
                return { formula: _t('Fritsch–Carlson slopes from your stored points'), inputs: [[_t('points'), xs.length, '', 0]], value: slopes(xs, ys)[k] };
            };
            spec.drawn.cv_p = function () {
                if (!drawnAt) return { what: _t('the dot on the curve chart'), drawn: _t('no dot: no run yet'), expected: '—', ok: null, note: _t('The dot appears once a curve has been played.') };
                var r = Sim.readPixel(box, drawnAt.x, drawnAt.y, 1, Sim.isBurgundy);
                return { what: _t('the dot on the curve chart at ({x}, {y}) css px', { x: Math.round(drawnAt.x), y: Math.round(drawnAt.y) }), drawn: r.text, expected: _t('burgundy'), ok: r.found };
            };
            spec.drawn.cv_set = function () {
                var el = knob().slider.el, v = parseFloat(el.value);
                return { what: _t('the position of the {name} slider', { name: knob().name }), drawn: fmtv(v) + ' ' + (knob().units || ''), expected: fmtv(ds.get('cv_set')) + ' ' + (knob().units || ''), ok: v === ds.get('cv_set') };
            };
            return spec;
        }
        function round(base) {
            var cols = (base.columns || []).concat(['cv_p', 'cv_set'].filter(function (n) { return (base.columns || []).indexOf(n) < 0; }));
            return {
                time: base.time, mode: base.mode, point: base.point, blocked: base.blocked, columns: cols,
                label: function () {
                    return st.on ? _t('the rest of the curve run: {name}, {sym} from {a} to {b} {units} in {T} s', { name: currentName(), sym: knob().symbol, a: fmtv(st.a), b: fmtv(st.b), units: knob().units || '', T: Sim.fmt(st.T, 0) }) : base.label();
                },
                length: function () { return st.on ? Math.max(0.1, st.T - st.t) : base.length(); }
            };
        }
        return { step: step, extend: extend, round: round, running: function () { return st.on; } };
    };
})();
