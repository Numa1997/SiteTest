// Loads the page's own pipeline functions (resamp, dft, chainAt, param, poly, SHAPES) from the page source,
// verbatim, so the Node checks run the page's code and not a re-typed copy.
// Usage: const P = require('./pagecode.cjs'); P.decompose(P.SHAPES.heart()) -> { samples, coefs, meanZ2, arcLen }
'use strict';
const fs = require('fs');
const path = require('path');
const src = fs.readFileSync(path.join(__dirname, '../../public/simulations/draw-decompose.html'), 'utf8');
function grab(startMarker, endMarker) {
    const a = src.indexOf(startMarker);
    const b = src.indexOf(endMarker, a);
    if (a < 0 || b < 0) throw new Error('marker not found: ' + startMarker);
    return src.slice(a, b);
}
const code = [
    grab('function resamp(pts, N) {', '/* c_k = (1/N)'),
    grab('function dft(z) {', 'function chainAt(time, n) {'),
    grab('function chainAt(time, n) {', 'function decompose(pts, name) {'),
    grab('function param(fx, fy, closed) {', 'var NAMES =')
].join('\n');
const factory = new Function('TAU', 'KMAXin', `
    var KMAX = KMAXin, arcLen = 0, coefs = [];
    ${code}
    return {
        resamp: function (p, N) { return resamp(p, N); },
        dft: function (z) { return dft(z); },
        chainAt: function (t, n, c) { coefs = c; return chainAt(t, n); },
        SHAPES: SHAPES, arcLen: function () { return arcLen; }
    };`);
function make(KMAX) { return factory(2 * Math.PI, KMAX); }
const P60 = make(60);
// the page's decompose(), lines for centring and meanZ2 transcribed (they sit inside decompose with ds taps)
function centre(r) {
    let mx = 0, my = 0;
    r.forEach(p => { mx += p.x; my += p.y; });
    mx /= r.length; my /= r.length;
    const s = r.map(p => ({ x: p.x - mx, y: p.y - my }));
    let E = 0; s.forEach(p => { E += p.x * p.x + p.y * p.y; }); E /= r.length;
    return { samples: s, meanZ2: E, mx, my };
}
function decompose(pts, N, P) {
    P = P || P60; N = N || 256;
    const r = P.resamp(pts, N);
    const L = P.arcLen();
    const c = centre(r);
    return Object.assign(c, { coefs: P.dft(c.samples), L, step: L / (N - 1) });
}
// resampling at spacing L/N without repeating the start point (the variant the note mentions in 7.1)
function resampPeriodic(pts, N) {
    // linear interpolation along the polyline at s = n L / N, as resamp() does but without the sample at s = L
    const acc = [0];
    for (let i = 1; i < pts.length; i++) acc.push(acc[i - 1] + Math.hypot(pts[i].x - pts[i - 1].x, pts[i].y - pts[i - 1].y));
    const L = acc[acc.length - 1];
    const out = []; let j = 0;
    for (let n = 0; n < N; n++) {
        const tgt = n * L / N;
        while (j < acc.length - 2 && acc[j + 1] < tgt) j++;
        const f = acc[j + 1] > acc[j] ? Math.min(1, (tgt - acc[j]) / (acc[j + 1] - acc[j])) : 0;
        out.push({ x: pts[j].x + f * (pts[j + 1].x - pts[j].x), y: pts[j].y + f * (pts[j + 1].y - pts[j].y) });
    }
    return { r: out, L };
}
module.exports = { make, P60, SHAPES: P60.SHAPES, decompose, centre, resampPeriodic, src };
