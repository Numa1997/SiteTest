// Fig. 13: the catalogue of closed drawings, on momentum-spirographs.html (#catalogue).
// Data: scripts/fig13-catalogue-data.js (strike, period, turns, energy, stability index of 228 closed orbits, found on the family map and
// pinned by bisection; tools/fig13/catalogue_build.py). Every picture here is integrated in the browser from the strike alone
// (two equal uniform rods, m = 1 kg, l = 1 m, g = 9.8; classical Runge-Kutta, steps of at most 0.2 ms): nothing is stored but the strike.
(function () {
    'use strict';
    const $ = id => document.getElementById(id), grid = $('cat-grid'), DATA = window.FIG13_CATALOGUE;
    if (!grid || !DATA) return;
    const A = 4 / 3, B = 1 / 3, C = 1 / 2, U1 = 14.7, U2 = 4.9;
    function deriv(s, o) {
        const d = s[0] - s[1], cs = Math.cos(d), sn = Math.sin(d), det = A * B - C * C * cs * cs;
        const w1 = (B * s[2] - C * cs * s[3]) / det, w2 = (A * s[3] - C * cs * s[2]) / det, e = C * w1 * w2 * sn;
        o[0] = w1; o[1] = w2; o[2] = -e - U1 * Math.sin(s[0]); o[3] = e - U2 * Math.sin(s[1]);
    }
    const k1 = [0, 0, 0, 0], k2 = [0, 0, 0, 0], k3 = [0, 0, 0, 0], k4 = [0, 0, 0, 0], tmp = [0, 0, 0, 0];
    function rk4(s, h) {
        deriv(s, k1); for (let i = 0; i < 4; i++) tmp[i] = s[i] + .5 * h * k1[i];
        deriv(tmp, k2); for (let i = 0; i < 4; i++) tmp[i] = s[i] + .5 * h * k2[i];
        deriv(tmp, k3); for (let i = 0; i < 4; i++) tmp[i] = s[i] + h * k3[i];
        deriv(tmp, k4); for (let i = 0; i < 4; i++) s[i] += h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);
    }
    const O = DATA.map((r, i) => ({ i, p1: r[0], p2: r[1], T: r[2], n1: r[3], n2: r[4], E: r[5], s: r[6], hunt: !!r[7], k: Math.abs(r[3] - r[4]) }));
    const kind = o => Math.abs(o.s) < 1.99 ? 'stable' : Math.abs(Math.abs(o.s) - 2) <= 0.01 ? 'neutral' : 'unstable';
    const COL = { stable: '#8fe3d0', neutral: '#ffd27a', unstable: '#ff8c8c' };
    function lap(o, n) {          // the tip over one lap: n points of (x, height)
        const sub = Math.max(1, Math.ceil(o.T / n / 2e-4)), h = o.T / n / sub, s = [0, 0, o.p1, o.p2], pts = new Float32Array(2 * (n + 1));
        for (let i = 0; i <= n; i++) { pts[2 * i] = Math.sin(s[0]) + Math.sin(s[1]); pts[2 * i + 1] = -(Math.cos(s[0]) + Math.cos(s[1])); if (i < n) for (let j = 0; j < sub; j++) rk4(s, h); }
        return pts;
    }
    function drawLap(c, pts, w, color, lw) {
        c.strokeStyle = color; c.lineWidth = lw; c.lineJoin = 'round'; c.beginPath();
        for (let i = 0; i < pts.length; i += 2) { const x = w / 2 + pts[i] * w * .22, y = w / 2 - pts[i + 1] * w * .22; i ? c.lineTo(x, y) : c.moveTo(x, y); }
        c.stroke();
    }
    // ---------------------------------------------------------------- the grid
    let order = 'E', filter = 'all', sel = null;
    const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { paint(e.target); io.unobserve(e.target); } }), { rootMargin: '300px' }) : null;
    function paint(btn) {
        const o = O[+btn.dataset.i], cv = btn.querySelector('canvas'), dpr = Math.min(window.devicePixelRatio || 1, 2), w = Math.round(cv.clientWidth * dpr) || 240;
        cv.width = w; cv.height = w; const c = cv.getContext('2d');
        drawLap(c, lap(o, 700), w, 'rgba(226,162,170,.95)', Math.max(1, dpr * .9));
    }
    function build() {
        const list = O.filter(o => filter === 'all' || (filter === 'butterfly' ? o.n1 === 0 : filter === 'flower' ? o.n1 !== 0 : filter === 'hunt' ? o.hunt : kind(o) === filter));
        const key = { E: o => o.E, T: o => o.T, k: o => o.k * 1e4 + o.E, s: o => Math.abs(o.s) }[order];
        list.sort((a, b) => key(a) - key(b));
        grid.textContent = '';
        for (const o of list) {
            const b = document.createElement('button'); b.type = 'button'; b.className = 'cat__tile'; b.dataset.i = o.i; b.style.setProperty('--k', COL[kind(o)]);
            b.setAttribute('aria-label', `Closed drawing: upper rod ${o.n1} turns, lower rod ${o.n2} turns per lap, ${o.E.toFixed(0)} joules, period ${o.T.toFixed(2)} seconds, ${kind(o)}`);
            b.innerHTML = `<canvas></canvas><span>(${o.n1}, ${o.n2})</span><small>${o.E.toFixed(0)} J · ${o.T.toFixed(2)} s</small>`;
            b.onclick = () => choose(o, true); grid.append(b); if (io) io.observe(b); else paint(b);
        }
        $('cat-count').textContent = `${list.length} of ${O.length} closed drawings`;
        mark();
    }
    function mark() { grid.querySelectorAll('.cat__tile').forEach(b => b.classList.toggle('is-on', sel && +b.dataset.i === sel.i)); }
    document.querySelectorAll('#cat-filter button').forEach(b => b.onclick = () => { filter = b.dataset.f; document.querySelectorAll('#cat-filter button').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false')); build(); });
    $('cat-sort').onchange = e => { order = e.target.value; build(); };
    // ---------------------------------------------------------------- the viewer: the chosen pendulum, running
    const vc = $('cat-view'), vx = vc.getContext('2d');
    let st = null, ideal = null, trail = [], playing = false, last = null, tSim = 0, speed = .5, pushed = false, seen = false;
    function choose(o, scroll) {
        sel = o; st = [0, 0, o.p1, o.p2]; ideal = lap(o, 1400); trail = []; tSim = 0; pushed = false; mark();
        const kd = kind(o), lam = Math.abs(o.s) > 2 ? Math.log((Math.abs(o.s) + Math.sqrt(o.s * o.s - 4)) / 2) : 0;
        $('cat-name').textContent = o.n1 === 0 ? `Butterfly: the lower rod turns ${Math.abs(o.n2)} times per lap, the upper rod only swings` : `Flower of ${o.k} petals: upper rod ${o.n1} turn${Math.abs(o.n1) === 1 ? '' : 's'}, lower rod ${o.n2} per lap`;
        $('cat-facts').innerHTML = `<dt>strike p₁, p₂</dt><dd>${o.p1.toFixed(4)}, ${o.p2.toFixed(4)} kg·m²/s</dd><dt>energy</dt><dd>${o.E.toFixed(1)} J (hanging still: −19.6 J)</dd><dt>period</dt><dd>${o.T.toFixed(4)} s</dd><dt>stability index</dt><dd>${o.s.toFixed(3)} · ${kd}</dd>`;
        $('cat-say').textContent = kd === 'stable' ? 'Stable: a small push only makes the drawing wobble around itself. Press Push and watch it stay.'
            : kd === 'neutral' ? 'Neutral: a small push makes the drawing drift slowly; it neither snaps back nor runs away.'
            : `Unstable: a small push grows about ${Math.exp(lam).toFixed(1)} times every lap${o.s < -2 ? ', flipping sides each lap' : ''}. Press Push and watch it come apart.`;
        speed = o.T < 1.2 ? .25 : .5; $('cat-speed').value = String(speed);
        if (!playing) { playing = true; last = null; requestAnimationFrame(tick); }
        $('cat-play').textContent = 'Pause'; drawView();
        if (scroll) $('cat-viewer').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    function sizeView() { const dpr = Math.min(window.devicePixelRatio || 1, 2), w = Math.round(vc.clientWidth * dpr); if (w && vc.width !== w) { vc.width = w; vc.height = w; } }
    function drawView() {
        sizeView(); const w = vc.width, c = vx, dpr = w / vc.clientWidth; if (!w || !st) return;
        c.fillStyle = '#140d10'; c.fillRect(0, 0, w, w);
        c.strokeStyle = 'rgba(245,241,234,.12)'; c.lineWidth = dpr; c.setLineDash([3 * dpr, 6 * dpr]); for (const r of [1, 2]) { c.beginPath(); c.arc(w / 2, w / 2, r * w * .22, 0, 7); c.stroke(); } c.setLineDash([]);
        drawLap(c, ideal, w, 'rgba(226,162,170,.30)', 1.2 * dpr);
        if (trail.length > 2) { c.strokeStyle = COL[kind(sel)]; c.lineWidth = 1.8 * dpr; c.beginPath(); for (let i = 0; i < trail.length; i += 2) { const x = w / 2 + trail[i] * w * .22, y = w / 2 - trail[i + 1] * w * .22; i ? c.lineTo(x, y) : c.moveTo(x, y); } c.stroke(); }
        const L = w * .22, x1 = w / 2 + L * Math.sin(st[0]), y1 = w / 2 + L * Math.cos(st[0]), x2 = x1 + L * Math.sin(st[1]), y2 = y1 + L * Math.cos(st[1]);
        c.strokeStyle = '#fff6ea'; c.lineWidth = 4 * dpr; c.lineCap = 'round'; c.beginPath(); c.moveTo(w / 2, w / 2); c.lineTo(x1, y1); c.lineTo(x2, y2); c.stroke();
        c.fillStyle = '#7a1f2b'; c.strokeStyle = '#fff6ea'; c.lineWidth = 1.5 * dpr; for (const [x, y] of [[w / 2, w / 2], [x1, y1]]) { c.beginPath(); c.arc(x, y, 5 * dpr, 0, 7); c.fill(); c.stroke(); }
        c.fillStyle = 'rgba(245,241,234,.7)'; c.font = `${Math.round(12 * dpr)}px "IBM Plex Mono", monospace`; c.textAlign = 'left'; c.textBaseline = 'top';
        c.fillText(`t = ${tSim.toFixed(2)} s · lap ${(tSim / sel.T).toFixed(1)}${pushed ? ' · pushed' : ''}`, 8 * dpr, 8 * dpr);
    }
    function tick(ts) {
        if (!playing || !sel) return;
        if (last !== null) {
            const dt = Math.min(.05, (ts - last) / 1000) * speed, n = Math.max(1, Math.ceil(dt / 2e-4)), h = dt / n, every = Math.max(1, Math.round(.002 / h));
            for (let i = 0; i < n; i++) { rk4(st, h); if (i % every === 0) trail.push(Math.sin(st[0]) + Math.sin(st[1]), -(Math.cos(st[0]) + Math.cos(st[1]))); }
            tSim += dt; const keep = 2 * Math.round(Math.min(3 * sel.T, 6) / (every * h)); if (trail.length > keep) trail.splice(0, trail.length - keep);
        }
        last = ts; drawView(); requestAnimationFrame(tick);
    }
    $('cat-play').onclick = () => { playing = !playing; last = null; $('cat-play').textContent = playing ? 'Pause' : 'Play'; if (playing) requestAnimationFrame(tick); };
    $('cat-push').onclick = () => { if (!st) return; st[0] += 0.02; pushed = true; drawView(); };       // a push: the upper rod turned by 0.02 rad (1.1 degrees)
    $('cat-again').onclick = () => { if (sel) choose(sel, false); };
    $('cat-speed').onchange = e => { speed = +e.target.value; };
    $('cat-sheet').onclick = () => { const F = window.__fig13; if (!sel || !F || !F.strikeAt) return; F.strikeAt(sel.p1, sel.p2); const s = $('sheet'); if (s) s.scrollIntoView({ behavior: 'smooth', block: 'start' }); };
    if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(e => {
        if (e.isIntersecting && !seen) { seen = true; playing = true; last = null; $('cat-play').textContent = 'Pause'; requestAnimationFrame(tick); }
        else if (!e.isIntersecting && playing) { playing = false; $('cat-play').textContent = 'Play'; }
    }), { threshold: .05 }).observe($('cat-viewer'));
    if ('ResizeObserver' in window) new ResizeObserver(() => drawView()).observe(vc);
    build();
    choose(O.find(o => o.hunt && o.n1 === 0 && o.n2 === 24) || O[0], false); playing = false; $('cat-play').textContent = 'Play';   // the butterfly waits, drawn, until the viewer is on screen
    window.__fig13cat = { orbits: O, kind, choose, state: () => ({ sel: sel && sel.i, t: tSim, st: st && st.slice(), playing, pushed }), lap };
})();
