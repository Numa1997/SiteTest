/* Live preview for Fig. 14 (A Wave Packet Meets a Sphere): the same equation and the same method as the Kaggle runs
   (tools/kaggle/schrodinger-sphere/solver.py), on a coarser grid, in a Web Worker so the page keeps drawing.
   i dpsi/dt = -(1/2) lap psi + V psi (hbar = m = 1), Strang split step: half a potential step, a full kinetic step in
   Fourier space, half a potential step, then the absorbing mask. N^3 = 64^3 points on a box of side L = 64 a (as on Kaggle) for slow packets, so the grid step is 1 a (Kaggle: 0.5 a);
   a faster packet needs a finer step, so the box shrinks to keep the step below pi / (k0 + 0.67): its fastest Fourier
   components (k0 plus four momentum widths 1/(2 sigma0)) must stay below the grid's highest wave number pi / dx.
   Message in:  { id, E, V0, R, N (default 64), L (default 64, smaller for fast packets, see above), dt (default 0.04, rounded so frames fall on the Kaggle frame times), nframes (48), sigma0 (3), x0 (-14), travel (30) }
   Messages out: { id, type: 'frame', f, n, out, L, amp (Uint8Array out*out), ph (Uint8Array), vol (Uint8Array N^3, |psi| at each point in
                 levels of the first frame's peak point, index (x*N + y)*N + z), curve: [t, norm, behind, ahead, sigma_y] }
                 { id, type: 'done', ms, steps } ; { id, type: 'error', message }
   The levels are coded exactly as the Kaggle runs: |psi| in 256 levels of the first frame's peak in the plane z = 0,
   arg psi in 256 levels (0 where the amplitude is below 3 levels). */
'use strict';
var job = 0;
function fftPlan(N) {
    var bits = Math.round(Math.log2(N)), rev = new Uint32Array(N), cs = new Float64Array(N / 2), sn = new Float64Array(N / 2);
    for (var i = 0; i < N; i++) { var r = 0; for (var b = 0; b < bits; b++) r |= ((i >> b) & 1) << (bits - 1 - b); rev[i] = r; }
    for (var k = 0; k < N / 2; k++) { cs[k] = Math.cos(-2 * Math.PI * k / N); sn[k] = Math.sin(-2 * Math.PI * k / N); }
    return { N: N, rev: rev, cs: cs, sn: sn };
}
/* in place on re[0..N), im[0..N); sign -1 forward, +1 inverse (unscaled) */
function fft1(p, re, im, sign) {
    var N = p.N, rev = p.rev, i, j, t;
    for (i = 0; i < N; i++) { j = rev[i]; if (j > i) { t = re[i]; re[i] = re[j]; re[j] = t; t = im[i]; im[i] = im[j]; im[j] = t; } }
    for (var size = 2; size <= N; size <<= 1) {
        var half = size >> 1, step = N / size;
        for (var s = 0; s < N; s += size) {
            for (var k = 0; k < half; k++) {
                var c = p.cs[k * step], w = sign < 0 ? p.sn[k * step] : -p.sn[k * step];
                var a = s + k, b = a + half, xr = re[b] * c - im[b] * w, xi = re[b] * w + im[b] * c;
                re[b] = re[a] - xr; im[b] = im[a] - xi; re[a] += xr; im[a] += xi;
            }
        }
    }
}
function fft3(p, re, im, sign, tr, ti) {
    var N = p.N, N2 = N * N, a, b, c, o;
    for (a = 0; a < N; a++) for (b = 0; b < N; b++) {          /* along z: contiguous */
        o = a * N2 + b * N;
        for (c = 0; c < N; c++) { tr[c] = re[o + c]; ti[c] = im[o + c]; }
        fft1(p, tr, ti, sign);
        for (c = 0; c < N; c++) { re[o + c] = tr[c]; im[o + c] = ti[c]; }
    }
    for (a = 0; a < N; a++) for (c = 0; c < N; c++) {          /* along y: stride N */
        o = a * N2 + c;
        for (b = 0; b < N; b++) { tr[b] = re[o + b * N]; ti[b] = im[o + b * N]; }
        fft1(p, tr, ti, sign);
        for (b = 0; b < N; b++) { re[o + b * N] = tr[b]; im[o + b * N] = ti[b]; }
    }
    for (b = 0; b < N; b++) for (c = 0; c < N; c++) {          /* along x: stride N^2 */
        o = b * N + c;
        for (a = 0; a < N; a++) { tr[a] = re[o + a * N2]; ti[a] = im[o + a * N2]; }
        fft1(p, tr, ti, sign);
        for (a = 0; a < N; a++) { re[o + a * N2] = tr[a]; im[o + a * N2] = ti[a]; }
    }
}
function run(m) {
    var id = m.id, N = m.N || 64, L = m.L || 64 * Math.min(1, Math.PI / (Math.sqrt(2 * m.E) + 0.67)), dx = L / N, dt0 = m.dt || 0.04, nf = m.nframes || 48, s0 = m.sigma0 || 3, x0 = m.x0 == null ? -14 : m.x0, travel = m.travel || 30;
    var E = m.E, V0 = m.V0, R = m.R, k0 = Math.sqrt(2 * E), N3 = N * N * N, N2 = N * N, t0 = Date.now();
    var re = new Float32Array(N3), im = new Float32Array(N3), hvr = new Float32Array(N3), hvi = new Float32Array(N3), kr = new Float32Array(N3), ki = new Float32Array(N3), mask = new Float32Array(N3);
    var x = new Float64Array(N), kk = new Float64Array(N), m1 = new Float64Array(N), W = Math.max(4, Math.floor(N / 10)), a, b, c, q;
    for (a = 0; a < N; a++) { x[a] = (a - N / 2) * dx; kk[a] = 2 * Math.PI * (a < N / 2 ? a : a - N) / (N * dx); m1[a] = 1; }
    for (a = 0; a < W; a++) { m1[a] = Math.pow(Math.sin(0.5 * Math.PI * a / W), 0.125); m1[N - 1 - a] = m1[a]; }
    /* frames at the same times as the Kaggle runs: Kaggle takes round(travel / k0 / 0.01) steps of 0.01 and stores every
       floor(steps / (nf - 1))-th state; here each frame interval is cut into sub steps of about dt0 */
    var kSteps = Math.round(travel / k0 / 0.01), kPer = Math.max(1, Math.floor(kSteps / (nf - 1))), frameDt = kPer * 0.01;
    var per = Math.max(1, Math.round(frameDt / dt0)), dt = frameDt / per;
    var norm0 = Math.pow(2 * Math.PI * s0 * s0, -0.75);
    for (a = 0; a < N; a++) for (b = 0; b < N; b++) for (c = 0; c < N; c++) {
        q = a * N2 + b * N + c;
        var X = x[a], Y = x[b], Z = x[c], g = norm0 * Math.exp(-((X - x0) * (X - x0) + Y * Y + Z * Z) / (4 * s0 * s0));
        re[q] = g * Math.cos(k0 * X); im[q] = g * Math.sin(k0 * X);
        var V = X * X + Y * Y + Z * Z < R * R ? V0 : 0, ph = -0.5 * V * dt;
        hvr[q] = Math.cos(ph); hvi[q] = Math.sin(ph);
        var K2 = kk[a] * kk[a] + kk[b] * kk[b] + kk[c] * kk[c], pk = -0.5 * K2 * dt;
        kr[q] = Math.cos(pk) / N3; ki[q] = Math.sin(pk) / N3;     /* the 1/N^3 of the inverse transform folded in */
        mask[q] = m1[a] * m1[b] * m1[c];
    }
    var plan = fftPlan(N), tr = new Float64Array(N), ti = new Float64Array(N), amp0 = 0, vol0 = 1, dV = dx * dx * dx;
    function mul(ar, ai) { for (var i = 0; i < N3; i++) { var r0 = re[i], i0 = im[i]; re[i] = r0 * ar[i] - i0 * ai[i]; im[i] = r0 * ai[i] + i0 * ar[i]; } }
    function measure(f) {
        var rx = new Float64Array(N), ry = new Float64Array(N), A = new Float32Array(N2), P = new Float32Array(N2), zc = N / 2;
        for (a = 0; a < N; a++) for (b = 0; b < N; b++) {
            var o = a * N2 + b * N;
            for (c = 0; c < N; c++) { var r2 = re[o + c] * re[o + c] + im[o + c] * im[o + c]; rx[a] += r2; ry[b] += r2; }
            A[a * N + b] = Math.hypot(re[o + zc], im[o + zc]); P[a * N + b] = Math.atan2(im[o + zc], re[o + zc]);
        }
        var nrm = 0, beh = 0, ah = 0, my = 0, sy = 0;
        for (a = 0; a < N; a++) { rx[a] *= dV; ry[a] *= dV; nrm += rx[a]; if (x[a] < -R) beh += rx[a]; if (x[a] > R) ah += rx[a]; my += ry[a] * x[a]; }
        my /= nrm; for (a = 0; a < N; a++) sy += ry[a] * (x[a] - my) * (x[a] - my); sy = Math.sqrt(sy / nrm);
        if (f === 0) { amp0 = 0; for (q = 0; q < N2; q++) if (A[q] > amp0) amp0 = A[q]; }
        var qa = new Uint8Array(N2), qp = new Uint8Array(N2), qv = new Uint8Array(N3);
        if (f === 0) { vol0 = 0; for (q = 0; q < N3; q++) { var m0 = re[q] * re[q] + im[q] * im[q]; if (m0 > vol0) vol0 = m0; } vol0 = Math.sqrt(vol0); }
        for (q = 0; q < N3; q++) qv[q] = Math.min(255, Math.round(255 * Math.sqrt(re[q] * re[q] + im[q] * im[q]) / vol0));
        for (q = 0; q < N2; q++) {
            var lv = Math.min(255, Math.max(0, Math.round(255 * A[q] / amp0))); qa[q] = lv;
            qp[q] = lv < 3 ? 0 : (Math.round((P[q] + Math.PI) / (2 * Math.PI) * 255) % 256);
        }
        postMessage({ id: id, type: 'frame', f: f, n: nf, out: N, L: L, amp: qa, ph: qp, vol: qv, curve: [f * per * dt, nrm, beh, ah, sy] }, [qa.buffer, qp.buffer, qv.buffer]);
    }
    measure(0);
    for (var f = 1; f < nf; f++) {
        for (var s = 0; s < per; s++) {
            if (job !== id) return;
            mul(hvr, hvi); fft3(plan, re, im, -1, tr, ti); mul(kr, ki); fft3(plan, re, im, 1, tr, ti); mul(hvr, hvi);
            for (q = 0; q < N3; q++) { re[q] *= mask[q]; im[q] *= mask[q]; }
        }
        measure(f);
    }
    postMessage({ id: id, type: 'done', ms: Date.now() - t0, steps: per * (nf - 1) });
}
var queue = null;
onmessage = function (e) { job = e.data.id; queue = e.data; setTimeout(function () { if (queue && queue.id === job) { var m = queue; queue = null; try { run(m); } catch (err) { postMessage({ id: m.id, type: 'error', message: String(err && err.message || err) }); } } }, 0); };
