// Fig. 13: "How the eye is built", on momentum-spirographs.html.
// An animation in five steps and a graph, both read from the same chaos map as the sheet (images/fig13/chaos-map-rods-P20.png,
// written by tools/fig13/chaos_map.py and map_png.py): v = (alpha / 255)^(1 / 0.8). Nothing on the map is recomputed here.
// Step 1 integrates two strikes and their twins live (the same equations, step and measure as chaos_map.py) and shows the value it
// gets next to the value the map holds for that strike: the map is that measurement made for every pixel.
(function () {
    'use strict';
    const $ = id => document.getElementById(id);
    const cv = $('eye-cv'), gv = $('eye-graph');
    if (!cv || !gv) return;
    const cx = cv.getContext('2d'), gx = gv.getContext('2d');

    // ---------------------------------------------------------------- the pendulum: two equal uniform rods, m = 1 kg, l = 1 m, g = 9.8
    const A = 4 / 3, B = 1 / 3, C = 1 / 2, U1 = 14.7, U2 = 4.9;
    const K = (p1, p2) => (B * p1 * p1 - 2 * C * p1 * p2 + A * p2 * p2) / (2 * (A * B - C * C));   // energy of a strike from hanging still, J
    const LIM = [2 * U2, 2 * U1, 2 * (U1 + U2)];                                                // 9.8, 29.4, 39.2 J
    const FOLD = [19 - 4 * Math.sqrt(21), 19 + 4 * Math.sqrt(21)];                              // fold lines p1 = k p2: 0.6697, 37.33
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
    // chaos_map.py: twin with theta1 + 1e-4 rad, 16000 RK4 steps of 0.05/120 s (6.67 s); distance in (th1, th2, p1, p2), capped at 1,
    // averaged over the steps; v = log(1000 d) / log(1000) clipped to [0, 1] (map_png.py)
    const STEPS = 16000, H = 0.05 / 30 / 4, KEEP = 40;
    function twins(p1, p2) {
        const a = [0, 0, p1, p2], b = [1e-4, 0, p1, p2], fr = []; let sum = 0;
        for (let k = 1; k <= STEPS; k++) {
            rk4(a, H); rk4(b, H);
            const dd = Math.min(1, Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3])); sum += dd;
            if (k % KEEP === 0) fr.push([a[0], a[1], b[0], b[1], dd]);
        }
        const d = sum / STEPS; return { p1, p2, fr, d, v: Math.min(1, Math.max(0, Math.log(1000 * Math.max(d, 1e-12)) / Math.log(1000))) };
    }
    // one strike in the pupil (6.2 J) and one in the iris (32.3 J), each at the centre of a map pixel, so that the live value and the
    // pixel's value are the same measurement (they differ by the 8-bit rounding of the image, at most 0.0023 near these strikes)
    const PIXC = (x, y) => [((x + .5) / 1280 - .5) * 2 * 20 * 16 / 9, (.5 - (y + .5) / 720) * 40];
    const DEMO = [[703, 324], [694, 287]].map(([x, y]) => Object.assign(twins(...PIXC(x, y)), { px: x, py: y }));

    // ---------------------------------------------------------------- the map
    const MW = 1280, MH = 720, PW = 20 * 16 / 9, PH = 20;      // p1 in [-35.56, 35.56], p2 in [-20, 20], kg m^2/s
    let map = null, px = null;
    function mapV(p1, p2) {           // bilinear between pixel centres, as the sheet's mapValue
        if (!px) return null;
        const fx = (p1 / (2 * PW) + .5) * MW - .5, fy = (.5 - p2 / (2 * PH)) * MH - .5;
        const x0 = Math.max(0, Math.min(MW - 2, Math.floor(fx))), y0 = Math.max(0, Math.min(MH - 2, Math.floor(fy))), tx = fx - x0, ty = fy - y0;
        const v = (x, y) => Math.pow(px[(y * MW + x) * 4 + 3] / 255, 1 / 0.8);
        return (v(x0, y0) * (1 - tx) + v(x0 + 1, y0) * tx) * (1 - ty) + (v(x0, y0 + 1) * (1 - tx) + v(x0 + 1, y0 + 1) * tx) * ty;
    }
    // the graph's data: share of strikes with v > 0.5, in 48 bins of energy spaced evenly in log K from 0.5 to 5000 J
    const KLO = 0.5, KHI = 5000, NB = 48, bins = [];
    function makeBins() {
        const n = new Float64Array(NB), c = new Float64Array(NB), lo = Math.log(KLO), w = (Math.log(KHI) - lo) / NB;
        for (let y = 0; y < MH; y++) for (let x = 0; x < MW; x++) {
            const p1 = ((x + .5) / MW - .5) * 2 * PW, p2 = (.5 - (y + .5) / MH) * 2 * PH, k = Math.floor((Math.log(Math.max(K(p1, p2), KLO)) - lo) / w);
            if (k < 0 || k >= NB) continue;
            n[k]++; if (px[(y * MW + x) * 4 + 3] / 255 > Math.pow(0.5, 0.8)) c[k]++;
        }
        for (let k = 0; k < NB; k++) bins.push({ k0: Math.exp(lo + k * w), k1: Math.exp(lo + (k + 1) * w), n: n[k], share: n[k] ? c[k] / n[k] : null });
        let tot = 0, ch = 0; const band = (a, b) => { let nn = 0, cc = 0; for (let y = 0; y < MH; y++) for (let x = 0; x < MW; x++) { const kk = K(((x + .5) / MW - .5) * 2 * PW, (.5 - (y + .5) / MH) * 2 * PH); if (kk >= a && kk < b) { nn++; if (px[(y * MW + x) * 4 + 3] / 255 > Math.pow(0.5, 0.8)) cc++; } } return [nn / (MW * MH), nn ? cc / nn : 0]; };
        STATS.pupil = band(0, LIM[0]); STATS.iris = band(LIM[1], LIM[2]); STATS.low = band(LIM[0], LIM[1]); STATS.far = band(196, 1e9);
        for (let i = 3; i < px.length; i += 4) { tot++; if (px[i] / 255 > Math.pow(0.5, 0.8)) ch++; } STATS.all = ch / tot;
    }
    const STATS = {};

    // ---------------------------------------------------------------- the timeline: five steps, 30 s
    const STEP = [[0, 9, 'One strike, two twins'], [9, 15, 'Every strike'], [15, 21, 'Energy draws ellipses'], [21, 25, 'The iris'], [25, 31, 'The lashes']];
    const TEND = 31;
    let t = 0, playing = false, last = null, night = true, pinK = null, asp = 16 / 9;
    const ease = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u), seg = (a, b) => ease((t - a) / (b - a));
    function fullPH() { return Math.max(PH, PW / asp); }
    function view() {        // half-height of the view in p2 (kg m^2/s), centred on the hanging pendulum's zero strike
        const z1 = 6.5, z3 = 9.5, F = fullPH();
        if (t < 9) return z1;
        if (t < 15) return z1 + (F - z1) * seg(9, 11.5);
        if (t < 25) return F + (z3 - F) * seg(15, 16.5);
        return z3 + (F - z3) * seg(25, 27);
    }
    let W = 0, Hh = 0, dpr = 1, S = 1;
    const X = p1 => W / 2 + p1 * S, Y = p2 => Hh / 2 - p2 * S;
    function fit() {
        const r = cv.parentElement.getBoundingClientRect(); dpr = Math.min(window.devicePixelRatio || 1, 2);
        asp = r.width < 560 ? 4 / 3 : 16 / 9;
        const w = Math.round(r.width), h = Math.round(w / asp);
        cv.style.height = h + 'px'; cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); W = cv.width; Hh = cv.height;
        const gw = Math.round(gv.parentElement.getBoundingClientRect().width), gh = Math.round(Math.max(200, Math.min(300, gw * 0.36)));
        gv.style.height = gh + 'px'; gv.width = Math.round(gw * dpr); gv.height = Math.round(gh * dpr);
        draw();
    }
    const col = () => night ? { bg: '#140d10', ink: '#fff6ea', soft: 'rgba(245,241,234,.62)', rule: 'rgba(245,241,234,.16)', rose: [226, 162, 170], box: 'rgba(20,13,16,.86)', pupil: '#8fe3d0', iris: '#ffd27a', lash: '#fff6ea' }
        : { bg: '#fffaf3', ink: '#1c1518', soft: 'rgba(28,21,24,.62)', rule: 'rgba(28,21,24,.14)', rose: [122, 31, 43], box: 'rgba(255,250,243,.9)', pupil: '#1d7f6e', iris: '#a8670a', lash: '#1c1518' };
    const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
    function label(c, txt, x, y, color, align) {
        const f = Math.round(13 * dpr); c.font = `${f}px "IBM Plex Mono", monospace`; c.textBaseline = 'middle';
        const w = c.measureText(txt).width + 10 * dpr; let x0 = align === 'right' ? x - w : x; x0 = Math.max(4 * dpr, Math.min(W - w - 4 * dpr, x0));
        const y0 = Math.max(f, Math.min(Hh - f, y));
        c.fillStyle = col().box; c.fillRect(x0, y0 - f * .85, w, f * 1.7); c.fillStyle = color; c.textAlign = 'left'; c.fillText(txt, x0 + 5 * dpr, y0);
    }
    function ellipse(c, ke, frac) {      // the strikes of energy ke; frac < 1 draws part of it, from the p1 axis round
        c.beginPath(); const n = 160, m = Math.max(1, Math.round(n * (frac === undefined ? 1 : frac)));
        for (let k = 0; k <= m; k++) { const a = k / n * 2 * Math.PI, r = Math.sqrt(ke / K(Math.cos(a), Math.sin(a))); k ? c.lineTo(X(r * Math.cos(a)), Y(r * Math.sin(a))) : c.moveTo(X(r * Math.cos(a)), Y(r * Math.sin(a))); }
        if (m === n) c.closePath();
    }
    function ring2(c, ke) { for (let k = 0; k <= 160; k++) { const a = k / 160 * 2 * Math.PI, r = Math.sqrt(ke / K(Math.cos(a), Math.sin(a))); k ? c.lineTo(X(r * Math.cos(a)), Y(r * Math.sin(a))) : c.moveTo(X(r * Math.cos(a)), Y(r * Math.sin(a))); } c.closePath(); }
    const small = () => W / dpr < 560;

    function draw() {
        if (!W) return;
        const c = cx, K_ = col(); S = (Hh / 2) / view();
        c.setTransform(1, 0, 0, 1, 0, 0); c.fillStyle = K_.bg; c.fillRect(0, 0, W, Hh);
        // axes
        c.strokeStyle = K_.rule; c.lineWidth = dpr; c.beginPath(); c.moveTo(0, Y(0)); c.lineTo(W, Y(0)); c.moveTo(X(0), 0); c.lineTo(X(0), Hh); c.stroke();
        c.fillStyle = K_.soft; c.font = `${Math.round(12 * dpr)}px "IBM Plex Mono", monospace`; c.textBaseline = 'alphabetic';
        c.textAlign = 'right'; c.fillText('p₁ (upper rod) →', W - 6 * dpr, Y(0) - 6 * dpr); c.textAlign = 'left'; c.fillText('↑ p₂ (lower rod)', X(0) + 6 * dpr, 16 * dpr);
        // the map: before step 2 only the demo pixels; during step 2 it fills from the top; afterwards whole
        if (map) {
            const reveal = t < 9 ? 0 : t < 15 ? seg(9.4, 14.4) : 1;
            if (reveal > 0) {
                const rows = Math.round(MH * reveal);
                c.save(); c.globalAlpha = .95; c.imageSmoothingEnabled = S * 2 * PW / MW < 2 * dpr;
                c.drawImage(map, 0, 0, MW, rows, X(-PW), Y(PH), 2 * PW * S, 2 * PH * S * rows / MH); c.restore();
                if (reveal < 1) { const yl = Y(PH) + 2 * PH * S * rows / MH; c.strokeStyle = rgba(K_.rose, .9); c.lineWidth = 2 * dpr; c.beginPath(); c.moveTo(Math.max(0, X(-PW)), yl); c.lineTo(Math.min(W, X(PW)), yl); c.stroke();
                    label(c, small() ? `${Math.round(reveal * MW * MH).toLocaleString('en')} strikes` : `${Math.round(reveal * MW * MH).toLocaleString('en')} of 921,600 strikes, each with its twin`, 8 * dpr, yl + 16 * dpr, K_.ink); }
            }
        }
        // step 1: two strikes and their twins
        if (t < 15) for (let i = 0; i < 2; i++) {
            const D = DEMO[i], t0 = i * 4.5, u = (t - t0 - .6) / 3.4;            // 3.4 s of screen for 6.67 s of motion
            if (t < t0) continue;
            const x = X(D.p1), y = Y(D.p2), done = u >= 1 || t >= 9, sz = Math.max(5 * dpr, 2 * PW / MW * S);
            if (done) { c.fillStyle = D.v > 0.02 ? rgba([122 + 104 * D.v, 31 + 131 * D.v, 43 + 127 * D.v], Math.pow(D.v, .8) || .0) : 'rgba(0,0,0,0)'; c.fillRect(x - sz, y - sz, 2 * sz, 2 * sz); }
            c.strokeStyle = i ? K_.iris : K_.pupil; c.lineWidth = 2 * dpr; c.strokeRect(x - sz - 3 * dpr, y - sz - 3 * dpr, 2 * sz + 6 * dpr, 2 * sz + 6 * dpr);
            if (t < 9 && t < t0 + 4.5) drawTwins(c, D, Math.max(0, Math.min(1, u)), i);
            if (t < 9) label(c, small() ? `${K(D.p1, D.p2).toFixed(1)} J` : `strike (${D.p1.toFixed(2)}, ${D.p2.toFixed(2)}): ${K(D.p1, D.p2).toFixed(1)} J`, x + sz + 8 * dpr, y - sz - 12 * dpr, i ? K_.iris : K_.pupil);
        }
        // steps 3 to 5: the energy ellipses, the pupil, the iris, the lashes
        if (t >= 15) {
            const kc = curK();
            // the iris band, 9.8 to 196 J, shaded faintly
            if (t >= 21) { const a = seg(21, 22.5); c.fillStyle = rgba(K_.rose, .10 * a); c.beginPath(); ring2(c, 196); ring2(c, LIM[0]); c.fill('evenodd'); }
            const ring = (ke, color, dash, a0) => { if (kc < ke * .999 && t < 25) { if (kc > 0) { c.strokeStyle = color; c.lineWidth = 2 * dpr; c.setLineDash(dash); ellipse(c, kc); c.stroke(); c.setLineDash([]); } return false; }
                c.strokeStyle = color; c.lineWidth = 2 * dpr; c.setLineDash(dash); ellipse(c, ke); c.stroke(); c.setLineDash([]); return true; };
            if (ring(LIM[0], K_.pupil, [])) { c.fillStyle = night ? 'rgba(143,227,208,.16)' : 'rgba(29,127,110,.12)'; ellipse(c, LIM[0]); c.fill(); }
            ring(LIM[1], K_.iris, [5 * dpr, 4 * dpr]); ring(LIM[2], K_.iris, []);
            if (t >= 22.5) { c.strokeStyle = rgba(K_.rose, .8); c.lineWidth = 1.5 * dpr; c.setLineDash([2 * dpr, 5 * dpr]); ellipse(c, 196, Math.min(1, (t - 22.5) / 1.5)); c.stroke(); c.setLineDash([]); }
            if (kc > 0 && kc < 196 && t < 25) label(c, `${kc.toFixed(1)} J`, X(Math.sqrt(kc / K(1, 0))) + 6 * dpr, Y(0) + 14 * dpr, K_.ink);
            // labels
            const pa = seg(16.8, 17.6), ia = seg(19.6, 20.4);
            if (pa > 0) { c.globalAlpha = pa; label(c, small() ? 'pupil · < 9.8 J · 0 % chaotic' : `pupil: below 9.8 J no rod can go over the top · ${pct(STATS.pupil, 1)} chaotic`, X(0) + 10 * dpr, Y(0) + 34 * dpr, K_.pupil); c.globalAlpha = 1; }
            if (ia > 0) { c.globalAlpha = ia; const r = Math.sqrt(LIM[2] / K(Math.cos(.39), Math.sin(.39))); label(c, small() ? `iris · 29–39 J · ${pct(STATS.iris, 1)}` : `iris: 29.4 to 39.2 J, a rod just goes over · ${pct(STATS.iris, 1)} chaotic`, X(r * Math.cos(.39)) + 8 * dpr, Y(r * Math.sin(.39)) - 18 * dpr, K_.iris); c.globalAlpha = 1; }
            if (t >= 23.6) { c.globalAlpha = seg(23.6, 24.4); const r = Math.sqrt(196 / K(-.2, 1)); label(c, small() ? '196 J · chaos fades' : '196 J: gravity is now small, chaos fades out', X(-.2 * r) - 8 * dpr, Y(r) - 14 * dpr, K_.soft, 'right'); c.globalAlpha = 1; }
            // the lashes
            if (t >= 25.8) {
                const u = seg(25.8, 28.4), big = 3 * Math.max(PW, PH);
                c.strokeStyle = K_.lash; c.lineWidth = 1.6 * dpr; c.setLineDash([6 * dpr, 5 * dpr]);
                for (const k of FOLD) { const n = Math.hypot(k, 1), L = big * u; c.beginPath(); c.moveTo(X(-L * k / n), Y(-L / n)); c.lineTo(X(L * k / n), Y(L / n)); c.stroke(); }
                c.setLineDash([]);
                if (t >= 28.4) { c.globalAlpha = seg(28.4, 29.2); const n = Math.hypot(FOLD[0], 1), r = view() * .62;
                    label(c, small() ? 'lashes: fold lines' : 'lashes: the fold lines · within 1.1° of them 65.9 % chaotic, beyond 5.7° none', X(-r * FOLD[0] / n) + 10 * dpr, Y(-r / n), K_.lash); c.globalAlpha = 1; }
            }
        }
        // the reader's pinned energy (tap the graph)
        if (pinK !== null) { c.strokeStyle = K_.ink; c.lineWidth = 2.4 * dpr; c.setLineDash([1.5 * dpr, 4 * dpr]); ellipse(c, pinK); c.stroke(); c.setLineDash([]);
            const r = Math.sqrt(pinK / K(-1, -.15)); label(c, `${fmtK(pinK)} J`, X(-r) - 6 * dpr, Y(-.15 * r), K_.ink, 'right'); }
        drawGraph();
        syncUI();
    }
    const pct = (s, d) => s ? (100 * s[1]).toFixed(d) + ' %' : '…';
    const fmtK = k => k < 10 ? k.toFixed(1) : k < 1000 ? k.toFixed(0) : k.toFixed(0);
    function curK() {        // the energy the drawing has reached: grows in step 3 (0 to 39.2 J) and step 4 (39.2 to 196 J)
        if (t < 15.3) return 0;
        if (t < 20) return LIM[2] * Math.pow(seg(15.3, 19.6), 1.6);
        if (t < 21) return LIM[2];
        if (t < 24) return LIM[2] * Math.pow(196 / LIM[2], seg(21.2, 23.6));
        return 196;
    }
    function drawTwins(c, D, u, i) {      // the pendulum and its twin, in a panel in a corner, with their distance against time
        const K_ = col(), pw = Math.min(W * (small() ? .44 : .3), Hh * .62), ph = pw * 1.25, x0 = 10 * dpr, y0 = 10 * dpr;
        c.fillStyle = K_.box; c.strokeStyle = K_.rule; c.lineWidth = dpr; c.beginPath(); c.roundRect(x0, y0, pw, ph, 8 * dpr); c.fill(); c.stroke();
        const n = D.fr.length, j = Math.min(n - 1, Math.floor(u * (n - 1))), f = D.fr[j], L = pw * .2, ox = x0 + pw / 2, oy = y0 + pw * .5;
        const one = (a, b, colr, w) => { const x1 = ox + L * Math.sin(a), y1 = oy + L * Math.cos(a), x2 = x1 + L * Math.sin(b), y2 = y1 + L * Math.cos(b);
            c.strokeStyle = colr; c.lineWidth = w; c.lineCap = 'round'; c.beginPath(); c.moveTo(ox, oy); c.lineTo(x1, y1); c.lineTo(x2, y2); c.stroke(); return [x2, y2]; };
        // the tip's path, last 0.5 s
        for (const [ia, ib, colr] of [[0, 1, rgba(K_.rose, .55)], [2, 3, i ? 'rgba(255,210,122,.55)' : 'rgba(143,227,208,.55)']]) {
            c.strokeStyle = colr; c.lineWidth = 1.2 * dpr; c.beginPath();
            for (let k = Math.max(0, j - 75); k <= j; k++) { const g = D.fr[k], x = ox + L * (Math.sin(g[ia]) + Math.sin(g[ib])), y = oy + L * (Math.cos(g[ia]) + Math.cos(g[ib])); k > Math.max(0, j - 75) ? c.lineTo(x, y) : c.moveTo(x, y); }
            c.stroke();
        }
        one(f[2], f[3], i ? K_.iris : K_.pupil, 3 * dpr); one(f[0], f[1], K_.ink, 3 * dpr);
        c.fillStyle = K_.ink; c.beginPath(); c.arc(ox, oy, 3 * dpr, 0, 7); c.fill();
        // distance against time, log scale 1e-5 .. 1
        const gx0 = x0 + 10 * dpr, gw = pw - 20 * dpr, gy0 = y0 + pw * 1.0, gh = ph - pw * 1.0 - 26 * dpr, yy = d => gy0 + gh * (1 - (Math.log10(Math.max(d, 1e-5)) + 5) / 5);
        c.strokeStyle = K_.rule; c.strokeRect(gx0, gy0, gw, gh);
        c.strokeStyle = i ? K_.iris : K_.pupil; c.lineWidth = 1.5 * dpr; c.beginPath();
        for (let k = 0; k <= j; k++) { const x = gx0 + gw * k / (n - 1), y = yy(D.fr[k][4]); k ? c.lineTo(x, y) : c.moveTo(x, y); } c.stroke();
        c.fillStyle = K_.soft; c.font = `${Math.round(11 * dpr)}px "IBM Plex Mono", monospace`; c.textAlign = 'left'; c.textBaseline = 'top';
        c.fillText('twins apart (log)', gx0 + 3 * dpr, gy0 + 2 * dpr);
        c.textBaseline = 'alphabetic'; c.fillStyle = K_.ink; c.font = `${Math.round(12 * dpr)}px "IBM Plex Mono", monospace`;
        c.fillText(`t = ${(u * STEPS * H).toFixed(1)} s`, x0 + 10 * dpr, y0 + ph - 9 * dpr);
    }

    // ---------------------------------------------------------------- the graph
    let GX = null;
    function drawGraph() {
        const c = gx, K_ = col(), w = gv.width, h = gv.height; if (!w) return;
        c.setTransform(1, 0, 0, 1, 0, 0); c.fillStyle = K_.bg; c.fillRect(0, 0, w, h);
        const l = 44 * dpr, r = 12 * dpr, tp = 16 * dpr, bt = 34 * dpr, pw = w - l - r, ph = h - tp - bt;
        const xk = k => l + pw * (Math.log(k) - Math.log(KLO)) / (Math.log(KHI) - Math.log(KLO)), yv = s => tp + ph * (1 - s);
        GX = { l, pw, xk };
        c.font = `${Math.round(11.5 * dpr)}px "IBM Plex Mono", monospace`; c.fillStyle = K_.soft; c.strokeStyle = K_.rule; c.lineWidth = dpr;
        c.textAlign = 'right'; c.textBaseline = 'middle';
        for (const s of [0, .25, .5, .75, 1]) { c.beginPath(); c.moveTo(l, yv(s)); c.lineTo(l + pw, yv(s)); c.stroke(); c.fillText(`${s * 100}%`, l - 5 * dpr, yv(s)); }
        c.textAlign = 'center'; c.textBaseline = 'top';
        for (const k of [1, 10, 100, 1000]) c.fillText(`${k} J`, xk(k), tp + ph + 6 * dpr);
        c.fillText(small() ? 'energy of the strike →' : 'energy of the strike, K (log scale) →', l + pw * .5, tp + ph + 19 * dpr);
        // the zones
        const zone = (a, b, colr, txt) => { c.fillStyle = colr; c.fillRect(xk(a), tp, xk(b) - xk(a), ph); };
        zone(KLO, LIM[0], night ? 'rgba(143,227,208,.08)' : 'rgba(29,127,110,.07)'); zone(LIM[1], LIM[2], night ? 'rgba(255,210,122,.10)' : 'rgba(168,103,10,.08)');
        c.setLineDash([4 * dpr, 4 * dpr]);
        for (const [k, colr] of [[LIM[0], K_.pupil], [LIM[1], K_.iris], [LIM[2], K_.iris], [196, K_.soft]]) { c.strokeStyle = colr; c.beginPath(); c.moveTo(xk(k), tp); c.lineTo(xk(k), tp + ph); c.stroke(); }
        c.setLineDash([]);
        c.textBaseline = 'top'; c.textAlign = 'left'; c.fillStyle = K_.pupil; c.fillText('pupil', xk(1.2), tp + 4 * dpr);
        c.fillStyle = K_.iris; c.fillText('iris', xk(LIM[1]) + 3 * dpr, tp + 4 * dpr);
        c.fillStyle = K_.soft; if (!small()) c.fillText('lashes only', xk(260), tp + 4 * dpr);
        // the curve
        if (bins.length) {
            c.beginPath(); let first = true;
            for (const b of bins) { if (b.share === null || b.n < 40) continue; const x = xk(Math.sqrt(b.k0 * b.k1)), y = yv(b.share); first ? c.moveTo(x, y) : c.lineTo(x, y); first = false; }
            c.strokeStyle = rgba(K_.rose, 1); c.lineWidth = 2.4 * dpr; c.stroke();
            for (const b of bins) { if (b.share === null || b.n < 40) continue; c.fillStyle = rgba(K_.rose, 1); c.beginPath(); c.arc(xk(Math.sqrt(b.k0 * b.k1)), yv(b.share), 2.4 * dpr, 0, 7); c.fill(); }
        } else { c.fillStyle = K_.soft; c.textAlign = 'center'; c.fillText('reading the map…', l + pw / 2, tp + ph / 2); }
        // the animation's energy, and the reader's pin
        const kc = t >= 15 && t < 25 ? curK() : 0;
        if (kc > KLO) { c.strokeStyle = K_.ink; c.lineWidth = 2 * dpr; c.beginPath(); c.moveTo(xk(kc), tp); c.lineTo(xk(kc), tp + ph); c.stroke(); }
        if (pinK !== null) { const b = binOf(pinK); c.strokeStyle = K_.ink; c.lineWidth = 2 * dpr; c.setLineDash([1.5 * dpr, 3.5 * dpr]); c.beginPath(); c.moveTo(xk(pinK), tp); c.lineTo(xk(pinK), tp + ph); c.stroke(); c.setLineDash([]);
            if (b && b.share !== null) { c.fillStyle = K_.ink; c.beginPath(); c.arc(xk(pinK), yv(b.share), 5 * dpr, 0, 7); c.fill(); } }
    }
    const binOf = k => bins.find(b => k >= b.k0 && k < b.k1) || null;
    function pinAt(k) {
        pinK = Math.min(KHI * .99, Math.max(KLO * 1.01, k)); const b = binOf(pinK);
        $('eye-read').textContent = b && b.share !== null
            ? `K = ${fmtK(pinK)} J: of the strikes with ${fmtK(b.k0)} to ${fmtK(b.k1)} J, ${(100 * b.share).toFixed(1)} % are chaotic (${b.n.toLocaleString('en')} pixels of the map). Its ellipse is drawn on the eye.`
            : `K = ${fmtK(pinK)} J`;
        $('eye-unpin').hidden = false; draw();
    }
    gv.addEventListener('pointerdown', e => { if (!GX) return; const r = gv.getBoundingClientRect(), x = (e.clientX - r.left) * dpr; const u = (x - GX.l) / GX.pw; if (u < 0 || u > 1) return;
        pinAt(Math.exp(Math.log(KLO) + u * (Math.log(KHI) - Math.log(KLO)))); });
    gv.addEventListener('keydown', e => { if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return; e.preventDefault(); pinAt((pinK || LIM[2]) * (e.key === 'ArrowRight' ? 1.1 : 1 / 1.1)); });
    $('eye-unpin').onclick = () => { pinK = null; $('eye-unpin').hidden = true; $('eye-read').textContent = 'Tap the graph to pin an energy: its share is read here and its ellipse is drawn on the eye.'; draw(); };

    // ---------------------------------------------------------------- words, buttons, clock
    const SAY = [
        () => `Every point of the sheet is one experiment: the pendulum hangs still and is struck with the momenta (p₁, p₂). A twin is struck the same way, its upper rod turned by 0.0001 rad. For 6.67 s the page measures how far apart the two get. ${DEMO[0].v < .05 ? 'In the pupil (green) they stay together: v = ' + DEMO[0].v.toFixed(2) + '.' : ''} In the iris (yellow) they part: v = ${DEMO[1].v.toFixed(3)} computed now in your browser, ${mv(1)} read from the map.`,
        () => 'The same measurement for 921,600 strikes, one per pixel, gives the map behind Fig. 13: bright where twins part (chaos), dark where they stay together.',
        () => 'Strikes that give the pendulum the same energy lie on an ellipse. Below 9.8 J the lower rod cannot be lifted over the top: that ellipse is the pupil, and nothing inside it is chaotic.',
        () => `Around it, from 9.8 J, a rod can go over the top, and gravity decides at each near-miss whether it does. That ring is the iris: between 29.4 and 39.2 J ${pct(STATS.iris, 1)} of strikes are chaotic. By 196 J chaos has nearly gone.`,
        () => 'Far out the strike is much stronger than gravity, and only two straight lines stay chaotic: the strikes that send the elbow exactly to the fold, where it hesitates. These are the lashes. That is the whole eye: a pupil, an iris and two lashes, all drawn by energy.',
    ];
    const mv = i => px ? Math.pow(px[(DEMO[i].py * MW + DEMO[i].px) * 4 + 3] / 255, 1 / 0.8).toFixed(3) : '…';   // that pixel of the map
    const stepOf = () => { let k = 0; while (k + 1 < STEP.length && t >= STEP[k + 1][0]) k++; return k; };
    let lastStep = -1, lastSayAt = 0;
    function syncUI() {
        const k = stepOf();
        document.querySelectorAll('#eye-steps button').forEach((b, i) => b.setAttribute('aria-pressed', i === k ? 'true' : 'false'));
        const now = performance.now();
        if (k !== lastStep || now - lastSayAt > 1000) { $('eye-say').textContent = `${k + 1} · ${STEP[k][2]}. ${SAY[k]()}`; lastStep = k; lastSayAt = now; }
        $('eye-scrub').value = String(Math.round(t * 10));
        $('eye-play').textContent = playing ? 'Pause' : t >= TEND - .01 ? 'Again' : 'Play';
    }
    $('eye-play').onclick = () => { if (t >= TEND - .01) t = 0; playing = !playing; last = null; if (playing) requestAnimationFrame(tick); draw(); };
    $('eye-scrub').max = String(TEND * 10);
    $('eye-scrub').addEventListener('input', e => { t = +e.target.value / 10; draw(); });
    document.querySelectorAll('#eye-steps button').forEach((b, i) => b.onclick = () => { t = STEP[i][0] + (i === 0 ? 0 : .01); if (!playing) { playing = true; last = null; requestAnimationFrame(tick); } draw(); });
    function tick(ts) {
        if (!playing) return;
        if (last !== null) t = Math.min(TEND, t + Math.min(.1, (ts - last) / 1000));
        last = ts; draw();
        if (t >= TEND) { playing = false; draw(); return; }
        requestAnimationFrame(tick);
    }
    // start when the figure comes into view (once); stop while it is off screen
    let seen = false;
    if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(e => {
        if (e.isIntersecting && !seen) { seen = true; if (!matchMedia('(prefers-reduced-motion: reduce)').matches) { playing = true; last = null; requestAnimationFrame(tick); } else { t = TEND; draw(); } }
        else if (!e.isIntersecting && playing) { playing = false; draw(); }
    }), { threshold: .35 }).observe(cv);
    // follow the page's Night / Paper choice
    const stage = $('stage'); if (stage) { const sync = () => { night = stage.classList.contains('is-night'); draw(); }; new MutationObserver(sync).observe(stage, { attributes: true, attributeFilter: ['class'] }); night = stage.classList.contains('is-night'); }
    if ('ResizeObserver' in window) new ResizeObserver(fit).observe(cv.parentElement); else addEventListener('resize', fit);
    const im = new Image(); im.onload = () => { map = im; const o = document.createElement('canvas'); o.width = MW; o.height = MH; const oc = o.getContext('2d'); oc.drawImage(im, 0, 0); px = oc.getImageData(0, 0, MW, MH).data; makeBins(); lastStep = -1; draw(); };
    im.src = '../images/fig13/chaos-map-rods-P20.png';
    fit();
    window.__fig13eye = { demo: DEMO, stats: STATS, bins, mapV, setT: x => { t = x; playing = false; draw(); }, get t() { return t; }, pinAt };
})();
