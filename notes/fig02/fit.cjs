// Fig. 2, Figure 3's high-energy curve: the first time d >= 0.1 m, and a least-squares line through ln d up to then,
// sampled at every RK4 step and at every 30th step (the figure's 0.05 s). Physics copied from the page. Run: node notes/fig02/fit.cjs
'use strict';
const g = 9.81, m1 = 1, l1 = 1, m2 = 1, l2 = 1, H = 1 / 600, EPS = 0.001;
function deriv(s) {
    var t1 = s[0], t2 = s[1], o1 = s[2], o2 = s[3], d = t1 - t2;
    var den = 2 * m1 + m2 - m2 * Math.cos(2 * d);
    var a1 = (-g * (2 * m1 + m2) * Math.sin(t1) - m2 * g * Math.sin(t1 - 2 * t2)
        - 2 * Math.sin(d) * m2 * (o2 * o2 * l2 + o1 * o1 * l1 * Math.cos(d))) / (l1 * den);
    var a2 = (2 * Math.sin(d) * (o1 * o1 * l1 * (m1 + m2) + g * (m1 + m2) * Math.cos(t1)
        + o2 * o2 * l2 * m2 * Math.cos(d))) / (l2 * den);
    return [o1, o2, a1, a2];
}
function rk4(s, h) {
    var k1 = deriv(s), i, s2 = [], s3 = [], s4 = [], out = [];
    for (i = 0; i < 4; i++) s2[i] = s[i] + h / 2 * k1[i];
    var k2 = deriv(s2);
    for (i = 0; i < 4; i++) s3[i] = s[i] + h / 2 * k2[i];
    var k3 = deriv(s3);
    for (i = 0; i < 4; i++) s4[i] = s[i] + h * k3[i];
    var k4 = deriv(s4);
    for (i = 0; i < 4; i++) out[i] = s[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);
    return out;
}
const rad = Math.PI / 180;
function bob2(s) { return [l1 * Math.sin(s[0]) + l2 * Math.sin(s[1]), -l1 * Math.cos(s[0]) - l2 * Math.cos(s[1])]; }
let a = [120 * rad, 150 * rad, 0, 0], b = [a[0] + EPS, a[1], 0, 0];
const T = [0], D = [EPS];
let first = null;
for (let k = 1; k <= 20 * 600; k++) {
    a = rk4(a, H); b = rk4(b, H);
    const p = bob2(a), q = bob2(b), d = Math.hypot(p[0] - q[0], p[1] - q[1]);
    T.push(k * H); D.push(d);
    if (first === null && d >= 0.1) first = k * H;
}
function fit(every, t1) {
    let n = 0, sx = 0, sy = 0, sxx = 0, sxy = 0;
    for (let i = 0; i < T.length; i += every) if (T[i] <= t1 + 1e-12) { const x = T[i], y = Math.log(D[i]); n++; sx += x; sy += y; sxx += x * x; sxy += x * y; }
    return (n * sxy - sx * sy) / (n * sxx - sx * sx);
}
console.log('first step with d >= 0.1 m at t =', first.toFixed(4), 's');
console.log('slope of ln d, every step, 0 to that time:', fit(1, first).toFixed(3), '1/s; every 0.05 s:', fit(30, first).toFixed(3), '1/s');
console.log('doubling time ln2/slope:', (Math.log(2) / fit(1, first)).toFixed(3), 's');
console.log('d at t = 5 s:', D[3000].toFixed(3), 'm; at 4 s:', D[2400].toFixed(4), 'm');
