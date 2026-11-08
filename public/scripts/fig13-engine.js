/* Fig. 13 engine: the general double pendulum and the long-exposure plate. Used by simulations/flower-hunt.html.
 *
 * Physics. Link i has mass m_i, length l_i, centre of mass a_i below its upper joint, moment of inertia I_i about it.
 *   A = m1 a1^2 + I1 + m2 l1^2,  B = m2 a2^2 + I2,  C = m2 l1 a2,  U1 = g (m1 a1 + m2 l1),  U2 = g m2 a2
 *   H = (B p1^2 - 2 C cos(D) p1 p2 + A p2^2) / (2 det) - U1 cos th1 - U2 cos th2,   det = A B - C^2 cos^2(D),  D = th1 - th2
 *   th1' = (B p1 - C cos(D) p2) / det,  th2' = (A p2 - C cos(D) p1) / det
 *   p1'  = -C th1' th2' sin(D) - U1 sin th1,   p2' = +C th1' th2' sin(D) - U2 sin th2
 * Uniform rods: a = l/2, I = m l^2/12 (2swap's video). Point masses: a = l, I = 0 (Fig. 2). Checked against tools/fig13/hunt.py.
 *
 * Plate. Light is laid down along the tip's path, the same amount per unit length (so the brightness counts passes, not
 * speed), into a float buffer that fades by exp(-dt / tau). A logarithmic tone curve maps it to the house colours.
 */
(function () {
    'use strict';
    function Model(par) {
        var m = { par: {}, A: 0, B: 0, C: 0, U1: 0, U2: 0 };
        m.set = function (p) {
            for (var k in p) m.par[k] = p[k];
            var q = m.par, rods = q.model === 'rods';
            var a1 = rods ? q.l1 / 2 : q.l1, a2 = rods ? q.l2 / 2 : q.l2;
            var I1 = rods ? q.m1 * q.l1 * q.l1 / 12 : 0, I2 = rods ? q.m2 * q.l2 * q.l2 / 12 : 0;
            m.A = q.m1 * a1 * a1 + I1 + q.m2 * q.l1 * q.l1; m.B = q.m2 * a2 * a2 + I2; m.C = q.m2 * q.l1 * a2;
            m.U1 = q.g * (q.m1 * a1 + q.m2 * q.l1); m.U2 = q.g * q.m2 * a2;
        };
        m.deriv = function (s, o) {
            var d = s[0] - s[1], c = Math.cos(d), sn = Math.sin(d), det = m.A * m.B - m.C * m.C * c * c;
            var w1 = (m.B * s[2] - m.C * c * s[3]) / det, w2 = (m.A * s[3] - m.C * c * s[2]) / det, e = m.C * w1 * w2 * sn;
            o[0] = w1; o[1] = w2; o[2] = -e - m.U1 * Math.sin(s[0]); o[3] = e - m.U2 * Math.sin(s[1]);
        };
        var k1 = new Float64Array(4), k2 = new Float64Array(4), k3 = new Float64Array(4), k4 = new Float64Array(4), t = new Float64Array(4);
        m.rk4 = function (s, h) {
            var i;
            m.deriv(s, k1); for (i = 0; i < 4; i++) t[i] = s[i] + 0.5 * h * k1[i];
            m.deriv(t, k2); for (i = 0; i < 4; i++) t[i] = s[i] + 0.5 * h * k2[i];
            m.deriv(t, k3); for (i = 0; i < 4; i++) t[i] = s[i] + h * k3[i];
            m.deriv(t, k4); for (i = 0; i < 4; i++) s[i] += h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);
        };
        m.energy = function (s) {
            var c = Math.cos(s[0] - s[1]), det = m.A * m.B - m.C * m.C * c * c;
            return (m.B * s[2] * s[2] - 2 * m.C * c * s[2] * s[3] + m.A * s[3] * s[3]) / (2 * det) - m.U1 * Math.cos(s[0]) - m.U2 * Math.cos(s[1]);
        };
        m.tip = function (s) {   /* metres, y pointing down */
            return [m.par.l1 * Math.sin(s[0]) + m.par.l2 * Math.sin(s[1]), m.par.l1 * Math.cos(s[0]) + m.par.l2 * Math.cos(s[1])];
        };
        m.set(par);
        return m;
    }

    var NIGHT = [[0, [122, 31, 43]], [0.6, [226, 162, 170]], [1, [255, 246, 234]]];
    var PAPER = [[0, [226, 162, 170]], [0.55, [122, 31, 43]], [1, [28, 21, 24]]];
    function ramp(st, f) {
        for (var i = 1; i < st.length; i++) if (f <= st[i][0]) {
            var u = (f - st[i - 1][0]) / (st[i][0] - st[i - 1][0]), a = st[i - 1][1], b = st[i][1];
            return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u];
        }
        return st[st.length - 1][1];
    }
    function Plate(canvas, night, maxDpr) {
        var LUTN = 4096, DMAX = 9, D0 = 0.22;
        var p = { canvas: canvas, ctx: canvas.getContext('2d'), night: night, W: 2, H: 2 };
        var D = new Float32Array(4), img = null, px = null, pal = new Uint32Array(LUTN);
        p.palette = function () {
            var st = p.night ? NIGHT : PAPER, norm = Math.log(1 + DMAX / D0);
            for (var i = 0; i < LUTN; i++) {
                var d = i / (LUTN - 1) * DMAX, f = Math.min(1, Math.log(1 + d / D0) / norm), c = ramp(st, f);
                var a = Math.round(255 * Math.pow(Math.min(1, f * (p.night ? 1.7 : 1.5)), 0.8));
                pal[i] = (a << 24) | (Math.round(c[2]) << 16) | (Math.round(c[1]) << 8) | Math.round(c[0]);
            }
        };
        p.resize = function () {
            var r = canvas.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, maxDpr || 2);
            p.W = Math.max(2, Math.round(r.width * dpr)); p.H = Math.max(2, Math.round(r.height * dpr));
            canvas.width = p.W; canvas.height = p.H;
            D = new Float32Array(p.W * p.H); img = p.ctx.createImageData(p.W, p.H); px = new Uint32Array(img.data.buffer);
        };
        p.clear = function () { D.fill(0); };
        p.splat = function (x0, y0, x1, y1) {
            var len = Math.hypot(x1 - x0, y1 - y0), m = Math.max(1, Math.ceil(len / 0.4)), w = len / m, W = p.W, H = p.H;
            for (var k = 0; k < m; k++) {
                var f = (k + .5) / m, x = x0 + (x1 - x0) * f, y = y0 + (y1 - y0) * f, ix = Math.floor(x), iy = Math.floor(y);
                if (ix < 0 || iy < 0 || ix >= W - 1 || iy >= H - 1) continue;
                var fx = x - ix, fy = y - iy, o = iy * W + ix;
                D[o] += w * (1 - fx) * (1 - fy); D[o + 1] += w * fx * (1 - fy); D[o + W] += w * (1 - fx) * fy; D[o + W + 1] += w * fx * fy;
            }
        };
        p.fade = function (factor) { for (var i = 0; i < D.length; i++) D[i] *= factor; };
        p.paint = function () {
            var sc = (LUTN - 1) / DMAX, last = LUTN - 1, n = D.length;
            for (var i = 0; i < n; i++) { var d = D[i]; px[i] = d < 0.004 ? 0 : pal[Math.min(last, (d * sc) | 0)]; }
            p.ctx.putImageData(img, 0, 0);
        };
        p.setNight = function (b) { p.night = b; p.palette(); };
        p.palette(); p.resize();
        return p;
    }
    window.Fig13 = { Model: Model, Plate: Plate };
})();
