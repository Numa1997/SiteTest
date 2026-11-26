/* Fig. 2b, the flip-time film of the double pendulum (docs/simulations/fig02-double-pendulum.md, "The flip-time film").
   The film and its maps were computed once on Kaggle (tools/sims/dp_film.py) and are read from Cloudflare R2 through
   scripts/simdata.js. This file computes no physics of its own: it plays the film, reads stored values, and asks the page's own
   live integrator (window.__dpLive, set by the page script) to run a picked start again as the check.
   Pointer rule: nothing reacts to the pointer crossing the film; "Read a start" is a switch, a click pins. */
(function () {
    'use strict';
    var T = window._t || function (s) { return s; };
    var box = document.getElementById('film-box'), video = document.getElementById('film-v'), mark = document.getElementById('film-mark');
    var slider = document.getElementById('film-f'), fOut = document.getElementById('film-f-out'), playBtn = document.getElementById('film-play');
    var readBox = document.getElementById('film-read'), swingBtn = document.getElementById('film-swing'), strip = document.getElementById('film-pin');
    var cap = document.getElementById('film-cap'), rM = document.getElementById('film-r-m'), rK = document.getElementById('film-r-k'), rL = document.getElementById('film-r-live');
    var bar = document.getElementById('film-bar');
    if (!box || !video) return;
    var ds = Sim.data && Sim.data.ds;
    var S = window.__dpFilm = { hdr: null, gen: null, f: 0, pin: null, err: null, words: 0 };
    var hdr, g, n, fps, frames, lastWords = 0, pal = null, grab = document.createElement('canvas'), gctx = null;

    function declare() {
        if (!ds) return;
        ds.var('film_f', [], 'int', { symbol: 'f', long_name: 'film frame shown', computed_in: 'dp-film.js', formula: 'floor(t_video × fps)', digits: 0, source: 'Read from the video clock.' });
        ds.var('film_m2', [], 'float', { symbol: 'm₂ (film)', units: 'kg', long_name: 'lower mass of the film frame shown', computed_in: 'tools/sims/dp_film.py on Kaggle', formula: 'm₁ e^(ln m₀ + f Δ)', digits: 4, source: 'Stored in film.json, frames[f].m2.' });
        ds.var('pin_th1', [], 'float', { symbol: 'θ₁ (pin)', units: '°', long_name: 'start angle of the pinned pixel', computed_in: 'dp-film.js', formula: '−180 + 360 b / n', digits: 1 });
        ds.var('pin_th2', [], 'float', { symbol: 'θ₂ (pin)', units: '°', long_name: 'start angle of the pinned pixel', computed_in: 'dp-film.js', formula: '−180 + 360 a / n', digits: 1 });
        ds.var('pin_k', [], 'int', { symbol: 'k', long_name: 'stored step of the first flip (65535: none within 10 s)', computed_in: 'tools/sims/dp_film.py on Kaggle', formula: 'first step with |θ₁| > π or |θ₂| > π', digits: 0, source: 'Read from map_<f>.bin, checked by SHA-256.' });
        ds.var('pin_t', [], 'float', { symbol: 't_flip', units: 's', long_name: 'stored time of the first flip', computed_in: 'dp-film.js', formula: 'k h', digits: 4 });
        ds.var('pin_k_live', [], 'int', { symbol: 'k (live)', long_name: 'the same start run again now by the page’s own RK4', computed_in: 'the page script, flipStep()', formula: 'first step with |θ₁| > π or |θ₂| > π', digits: 0 });
        Sim.data.groups.push({ title: T('Flip-time film (computed on Kaggle)'), note: T('the film frame shown and the pinned start'), vars: ['film_f', 'film_m2', 'pin_th1', 'pin_th2', 'pin_k', 'pin_t', 'pin_k_live'] });
        Sim.data.check.pin_t = function () { return S.pin ? { formula: 't = k h', inputs: [['k', S.pin.k, '', 0], ['h', hdr.params.h, 's', 6]], value: S.pin.k < hdr.params.failed ? S.pin.k * hdr.params.h : undefined } : { formula: T('no start pinned'), inputs: [], value: undefined }; };
        Sim.data.check.pin_k = function () { return S.pin ? { formula: T('the page’s RK4 (h = 1/600 s) from θ₁, θ₂ and m₂ read from the store, ω = 0'), inputs: [['θ₁', S.pin.d1, '°', 1], ['θ₂', S.pin.d2, '°', 1], ['m₂', S.pin.m2, 'kg', 6]], value: S.pin.live } : { formula: T('no start pinned'), inputs: [], value: undefined }; };
        Sim.data.drawn = Sim.data.drawn || {};
        Sim.data.drawn.pin_k = function () { return S.pin ? S.pin.px : { what: T('no start pinned'), drawn: '', expected: '', ok: true }; };
    }

    function colourOf(k) {
        var c = hdr.colour, p = hdr.params;
        if (k === p.never) return c.never;
        if (k === p.failed) return c.failed;
        var t = Math.max(k, 1) * p.h, u = Math.log(t / c.t_lo) / Math.log(p.T_max / c.t_lo);
        return c.lut[Math.round(255 * Math.min(1, Math.max(0, u)))];
    }
    function frameOf(t) { return Math.max(0, Math.min(frames - 1, Math.floor(t * fps))); }
    function ratio(m) { return m < 1 ? '1/' + (1 / m).toFixed(2) : m.toFixed(2); }

    function words(force) {                         // text rewritten at most 4 times a second while the film plays
        var now = performance.now();
        if (!force && now - lastWords < 250) return;
        lastWords = now; S.words++;
        var fr = hdr.frames[S.f];
        cap.textContent = 'm₂/m₁ = ' + ratio(fr.m2 / hdr.params.m1);
        fOut.textContent = (S.f + 1) + ' / ' + frames;
        rM.textContent = ratio(fr.m2 / hdr.params.m1) + (S.f % 4 === 0 ? T(' (a slider step)') : '');
        slider.value = S.f; Sim.slider && slider.style.setProperty('--p', (S.f / (frames - 1)) * 100 + '%');
        if (ds) { ds.set('film_f', S.f); ds.set('film_m2', fr.m2); }
    }

    function drawMark() {                           // the pin's ring, every frame
        var r = box.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
        if (mark.width !== Math.round(r.width * dpr)) { mark.width = Math.round(r.width * dpr); mark.height = Math.round(r.height * dpr); }
        var c = mark.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, r.width, r.height);
        if (!S.pin) return;
        var x = (S.pin.b + 0.5) / n * r.width, y = (n - S.pin.a - 0.5) / n * r.height;
        c.lineWidth = 2; c.strokeStyle = '#fff'; c.beginPath(); c.arc(x, y, 9, 0, 2 * Math.PI); c.stroke();
        c.lineWidth = 1.2; c.strokeStyle = '#7a1f2b'; c.beginPath(); c.arc(x, y, 9, 0, 2 * Math.PI); c.stroke();
    }

    function tick() {
        if (hdr) {
            var f = frameOf(video.currentTime);
            if (f !== S.f) { S.f = f; words(false); }
            drawMark();
        }
        requestAnimationFrame(tick);
    }

    function seek(f) {
        S.f = f; video.currentTime = (f + 0.5) / fps; words(true);
        return new Promise(function (res) { var done = function () { video.removeEventListener('seeked', done); res(); }; video.addEventListener('seeked', done); });
    }

    function readPixel(a, b) {                      // the film's own pixel, at the video's native size, after the seek
        if (!gctx) { grab.width = n; grab.height = n; gctx = grab.getContext('2d', { willReadFrequently: true }); }
        gctx.clearRect(0, 0, n, n); gctx.drawImage(video, 0, 0, n, n);
        return gctx.getImageData(b, n - 1 - a, 1, 1).data;
    }

    function pinAt(a, b) {
        var f = S.f, fr = hdr.frames[f], name = fr.file;
        strip.hidden = false; strip.textContent = T('Reading the stored map of this frame …');
        return g.file(name).then(function (buf) {
            var k = new DataView(buf).getUint16(2 * (a * n + b), true);
            var d1 = -180 + 360 * b / n, d2 = -180 + 360 * a / n, lnm = fr.ln_m;
            var live = window.__dpLive ? window.__dpLive.flipStep(d1 * Math.PI / 180, d2 * Math.PI / 180, lnm, hdr.params.k_max) : undefined;
            var px = readPixel(a, b), want = colourOf(k), gap = Math.max(Math.abs(px[0] - want[0]), Math.abs(px[1] - want[1]), Math.abs(px[2] - want[2]));
            var drawn = px[3] === 0 ? T('nothing (transparent)') : 'rgb(' + px[0] + ', ' + px[1] + ', ' + px[2] + ')';
            S.pin = { f: f, a: a, b: b, d1: d1, d2: d2, lnm: lnm, m2: fr.m2, k: k, live: live, gap: gap,
                px: { what: T('film pixel, column ') + b + T(', row ') + (n - 1 - a), drawn: drawn, expected: 'rgb(' + want.join(', ') + ')' + T(', the colour of the stored value'),
                      ok: px[3] === 255 && gap <= 24, note: T('The film is H.264, a lossy code: the model measured its gap against the stored colours (film.json, checks.film_vs_map).') } };
            var tk = k === hdr.params.never ? T('no flip within 10 s') : k === hdr.params.failed ? T('the method failed') : T('first flip at step ') + k + ' (t = ' + (k * hdr.params.h).toFixed(3) + ' s)';
            rK.textContent = k === hdr.params.never ? T('none in 10 s') : (k * hdr.params.h).toFixed(3) + ' s';
            rL.textContent = live === k ? T('identical') : (live === hdr.params.never ? T('none in 10 s') : (live * hdr.params.h).toFixed(3) + ' s');
            strip.textContent = 'θ₁ = ' + d1.toFixed(1) + '°, θ₂ = ' + d2.toFixed(1) + '°, m₂/m₁ = ' + ratio(fr.m2 / hdr.params.m1) + ' · ' + T('stored: ') + tk +
                ' · ' + T('the page’s RK4 now: ') + (live === k ? T('the same step') : T('step ') + live) + ' · ' + T('pixel ') + drawn + T(' against ') + 'rgb(' + want.join(', ') + ')' + T(', gap ') + gap;
            swingBtn.disabled = !(S.f % 4 === 0 && b % 2 === 0 && a % 2 === 0);
            if (ds) { ds.set('pin_th1', d1); ds.set('pin_th2', d2); ds.set('pin_k', k); ds.set('pin_t', k < hdr.params.failed ? k * hdr.params.h : NaN); ds.set('pin_k_live', live); }
        }).catch(function (e) { strip.textContent = String(e && e.message || e); });
    }

    function onClick(ev) {
        if (!readBox.checked || !hdr) return;
        var r = box.getBoundingClientRect();
        var b = Math.floor((ev.clientX - r.left) / r.width * n), row = Math.floor((ev.clientY - r.top) / r.height * n);
        var a = n - 1 - row;
        b = Math.max(0, Math.min(n - 2, b - (b % 2))); a = Math.max(0, Math.min(n - 2, a - (a % 2)));   // a start the sliders reach: whole degrees
        pinAt(a, b);
    }

    function setPlaying(on) {
        if (on) { video.play().catch(function () {}); playBtn.textContent = T('Pause'); }
        else { video.pause(); playBtn.textContent = T('Play'); }
    }

    function legend() {
        var c = bar.getContext('2d'), w = bar.width = 240, h = bar.height = 12;
        for (var i = 0; i < w; i++) { var q = hdr.colour.lut[Math.round(255 * i / (w - 1))]; c.fillStyle = 'rgb(' + q.join(',') + ')'; c.fillRect(i, 0, 1, h); }
    }

    function boot() {
        declare();
        SimData.open('double_pendulum_film', { format: 1, base: '../', host: box }).then(function (gen) {
            g = gen; S.gen = { date: gen.date, version: gen.version, commit: gen.commit, run: gen.entry && gen.entry.run };
            return g.file('film.json');
        }).then(function (buf) {
            hdr = S.hdr = JSON.parse(new TextDecoder().decode(buf));
            n = hdr.params.n; fps = hdr.params.fps; frames = hdr.params.frames;
            slider.max = frames - 1; legend();
            video.src = g.url('film.mp4'); video.poster = g.url('poster.png');
            video.addEventListener('loadeddata', function () { words(true); }, { once: true });
            setPlaying(!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches));
            requestAnimationFrame(tick);
        }).catch(function (e) { S.err = String(e && e.message || e); });
        playBtn.addEventListener('click', function () { if (readBox.checked) return; setPlaying(video.paused); });
        slider.addEventListener('input', function () {
            if (!hdr) return;
            setPlaying(false);
            var f = parseInt(slider.value, 10); if (readBox.checked) f -= f % 4;
            seek(f).then(function () { if (S.pin) pinAt(S.pin.a, S.pin.b); });
        });
        readBox.addEventListener('change', function () {
            if (!hdr) return;
            if (readBox.checked) { setPlaying(false); slider.step = 4; seek(S.f - (S.f % 4)); strip.hidden = false; strip.textContent = T('Click a point of the film to pin its start.'); box.style.cursor = 'crosshair'; }
            else { slider.step = 1; S.pin = null; strip.hidden = true; swingBtn.disabled = true; box.style.cursor = ''; rK.textContent = rL.textContent = '—'; }
        });
        box.addEventListener('click', onClick);
        swingBtn.addEventListener('click', function () {
            if (!S.pin || !window.__dpLive) return;
            window.__dpLive.swing(S.pin.d1, S.pin.d2, S.pin.lnm);
            var st = document.getElementById('stage'); if (st) st.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }
    boot();
})();
