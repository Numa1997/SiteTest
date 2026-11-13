/* fig14-sheet-worker.js: the meshed sheet of Fig. 14, computed off the page's main thread so that the animation never waits.
   The page sends one stored run (the 8-bit levels of |psi| and arg psi exactly as Kaggle's file holds them) and asks for
   frames; for each frame this worker returns psi (real and imaginary part) on the sheet's fine grid, 1/6 a apart, and four
   numbers the page scales the height with. Nothing is computed that the run did not hold: the fine grid is the band-limited
   (Fourier) interpolation of the stored points, the unique sum of the plane waves that fit the stored box which passes through
   every stored value. Packets: the stored cut psi(x, |y|) of the plane z = 0, 128 x 128 points 0.5 a apart, onto
   -24 <= x, y <= 24 (289 x 289 points). Spherical waves: u = r psi of the stored profile along r (u odd in r), then psi = u / r
   at every point of -32 <= x, y <= 32 (385 x 385 points); two sources: the sum of two such waves about (+s/2, 0) and (-s/2, 0).
   Messages in: { type: 'run', id, kind: 'packet' | 'radial', n, A, P, ... } and { type: 'want', id, frames: [f, ...] }.
   Message out: { id, f, n, x0, RE, IM, mre, gre, mab, gab } (largest |Re psi| and its steepest slope; the same for |psi|^2).
   Docs: docs/simulations/fig14-schrodinger-sphere.md. */
'use strict';
var MS = 1 / 6;
function bandMatrix(N, d, xs) {        /* N samples spaced d apart, periodic with period N d (N even); row a: weights at offset xs[a] from sample 0 */
    var M = new Float64Array(xs.length * N), P = N * d;
    for (var a = 0; a < xs.length; a++) for (var j = 0; j < N; j++) {
        var s = xs[a] - j * d; s -= P * Math.round(s / P); var t = 2 * Math.PI * s / P;
        M[a * N + j] = Math.abs(s) < 1e-9 ? 1 : Math.sin(N * t / 2) / (N * Math.tan(t / 2));   /* the periodic sinc of an even N */
    }
    return M;
}
var PKM = null;
function packetMats() {
    if (PKM) return PKM;
    var n = 289, xs = new Float64Array(n); for (var a = 0; a < n; a++) xs[a] = (-24 + a * MS) + 32;   /* offset from the first stored point, x = -32 */
    PKM = { n: n, x0: -24, M: bandMatrix(128, 0.5, xs), S: new Float64Array(2 * 128 * 128), T: new Float64Array(2 * n * 128) };
    return PKM;
}
function packetSheet(R, f) {   /* psi(x, y, 0): the stored cut at rho = |y|; scaled by the frame's peak (R.pk) and, for the pillar, times g(0, t) (R.g) */
    var K = packetMats(), n = K.n, S = K.S, T = K.T, M = K.M, base = f * R.nx * R.nr, pk = R.pk ? R.pk[f] : 1, gr = pk, gi = 0;
    if (R.g) { gr = R.g[2 * f] * pk; gi = R.g[2 * f + 1] * pk; }
    var RE = new Float32Array(n * n), IM = new Float32Array(n * n);
    for (var i = 0; i < 128; i++) for (var jy = 0; jy < 128; jy++) {
        var rr = Math.abs(jy - 64), q = 2 * (i * 128 + jy), re = 0, im = 0;
        if (rr < R.nr) { var a2 = R.A[base + i * R.nr + rr]; if (a2 >= 3) { var ph = R.P[base + i * R.nr + rr] / 255 * 2 * Math.PI - Math.PI; re = a2 / 255 * Math.cos(ph); im = a2 / 255 * Math.sin(ph); } }
        S[q] = re * gr - im * gi; S[q + 1] = re * gi + im * gr;
    }
    for (var a = 0; a < n; a++) {   /* along x */
        var ta = 2 * a * 128; for (var z = 0; z < 256; z++) T[ta + z] = 0;
        for (var i2 = 0; i2 < 128; i2++) { var w = M[a * 128 + i2]; if (w === 0) continue; var si = 2 * i2 * 128; for (var jy2 = 0; jy2 < 256; jy2++) T[ta + jy2] += w * S[si + jy2]; }
    }
    var half = (n - 1) / 2;   /* along y, for y >= 0; the cut is even in y, so the half y < 0 is its mirror */
    for (var b = half; b < n; b++) for (var a3 = 0; a3 < n; a3++) {
        var sr = 0, sim = 0, tb = 2 * a3 * 128, mb = b * 128;
        for (var jy3 = 0; jy3 < 128; jy3++) { var w2 = M[mb + jy3]; sr += w2 * T[tb + 2 * jy3]; sim += w2 * T[tb + 2 * jy3 + 1]; }
        RE[a3 * n + b] = RE[a3 * n + (n - 1 - b)] = sr; IM[a3 * n + b] = IM[a3 * n + (n - 1 - b)] = sim;
    }
    return { n: n, x0: K.x0, RE: RE, IM: IM };
}
var RDM = null, RDR = 0.01, RDN = 5601;   /* spherical waves: psi(r) tabulated every 0.01 a out to 56 a, from the 97 stored radii */
function radialTable(R, f) {
    if (!RDM) { var xs = new Float64Array(RDN); for (var t = 0; t < RDN; t++) xs[t] = t * RDR + 48; RDM = { M: bandMatrix(192, 0.5, xs), re: new Float64Array(RDN), im: new Float64Array(RDN), ur: new Float64Array(192), ui: new Float64Array(192) }; }
    var nr = R.nr, rs = R.rstep, sc = R.sc[f], ob = f * nr, ur = RDM.ur, ui = RDM.ui, M = RDM.M;
    for (var k = 0; k < 192; k++) {   /* u = r psi on the whole line, odd in r: samples at r = -48 + 0.5 k */
        var r = -48 + k * rs, j = Math.round(Math.abs(r) / rs), sg = r < 0 ? -1 : 1, a = j < nr ? R.A[ob + j] : 0, re = 0, im = 0;
        if (a >= 3) { var ph = R.P[ob + j] / 255 * 2 * Math.PI - Math.PI; re = a * sc * Math.cos(ph); im = a * sc * Math.sin(ph); }
        ur[k] = sg * Math.abs(r) * re; ui[k] = sg * Math.abs(r) * im;
    }
    for (var t2 = 0; t2 < RDN; t2++) {
        var r2 = t2 * RDR, sr = 0, si = 0, mo = t2 * 192;
        if (r2 > 48) { RDM.re[t2] = 0; RDM.im[t2] = 0; continue; }
        for (var k2 = 0; k2 < 192; k2++) { var w = M[mo + k2]; sr += w * ur[k2]; si += w * ui[k2]; }
        RDM.re[t2] = sr; RDM.im[t2] = si;   /* u(r) for now */
    }
    var u1r = RDM.re[1], u1i = RDM.im[1];
    for (var t3 = 1; t3 < RDN; t3++) { RDM.re[t3] /= t3 * RDR; RDM.im[t3] /= t3 * RDR; }   /* psi = u / r */
    RDM.re[0] = u1r / RDR; RDM.im[0] = u1i / RDR;                                            /* at r = 0: u(0.01) / 0.01 */
    return RDM;
}
function radialSheet(R, f) {
    var D = radialTable(R, f), n = 385, x0 = -32, s2 = R.two / 2, RE = new Float32Array(n * n), IM = new Float32Array(n * n), dre = D.re, dim = D.im;
    function add(q, r) { var u = r / RDR, i = Math.floor(u), w = u - i; if (i >= RDN - 1) return; RE[q] += dre[i] * (1 - w) + dre[i + 1] * w; IM[q] += dim[i] * (1 - w) + dim[i + 1] * w; }
    for (var i = 0; i < n; i++) { var x = x0 + i * MS; for (var j = 0; j < n; j++) { var y = x0 + j * MS, q = i * n + j;
        if (R.two) { add(q, Math.sqrt((x - s2) * (x - s2) + y * y)); add(q, Math.sqrt((x + s2) * (x + s2) + y * y)); }   /* psi = psi_1 + psi_2 */
        else add(q, Math.sqrt(x * x + y * y)); } }
    return { n: n, x0: x0, RE: RE, IM: IM };
}
function stats(sh) {   /* the largest |Re psi| and |psi|^2 on the sheet and their steepest slopes (central differences, 1/6 a) */
    var n = sh.n, RE = sh.RE, IM = sh.IM, N = n * n, AB = new Float32Array(N), mre = 0, mab = 0, gre = 0, gab = 0, q, v;
    for (q = 0; q < N; q++) { v = Math.abs(RE[q]); if (v > mre) mre = v; v = RE[q] * RE[q] + IM[q] * IM[q]; AB[q] = v; if (v > mab) mab = v; }
    for (var i = 1; i < n - 1; i++) for (var j = 1; j < n - 1; j++) {
        q = i * n + j; var gx = RE[q + n] - RE[q - n], gy = RE[q + 1] - RE[q - 1], g2 = gx * gx + gy * gy; if (g2 > gre) gre = g2;
        gx = AB[q + n] - AB[q - n]; gy = AB[q + 1] - AB[q - 1]; g2 = gx * gx + gy * gy; if (g2 > gab) gab = g2;
    }
    return { mre: mre, mab: mab, gre: Math.sqrt(gre) / (2 * MS), gab: Math.sqrt(gab) / (2 * MS) };
}
var RUN = null, QUEUE = [], busy = false;
function pump() {
    if (busy || !QUEUE.length || !RUN) return;
    busy = true;
    var f = QUEUE.shift(), id = RUN.id;
    var sh = RUN.kind === 'radial' ? radialSheet(RUN, f) : packetSheet(RUN, f), st = stats(sh);
    self.postMessage({ id: id, f: f, n: sh.n, x0: sh.x0, RE: sh.RE, IM: sh.IM, mre: st.mre, gre: st.gre, mab: st.mab, gab: st.gab }, [sh.RE.buffer, sh.IM.buffer]);
    busy = false;
    if (QUEUE.length) setTimeout(pump, 0);   /* one frame per turn, so a newer request can replace the queue in between */
}
self.onmessage = function (e) {
    var m = e.data;
    if (m.type === 'run') { RUN = m; QUEUE = []; }
    else if (m.type === 'want' && RUN && m.id === RUN.id) { QUEUE = m.frames.slice(); setTimeout(pump, 0); }
};
