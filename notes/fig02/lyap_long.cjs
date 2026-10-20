// Fig. 2: largest Lyapunov exponent of the default start (120°, 150°, at rest, equal masses and lengths), Benettin's method:
// a perturbation of size 1e-8 in the full state (θ1, θ2, ω1, ω2), rescaled every 0.1 s, the logarithms of its growth averaged.
// Physics lines copied from the page (deriv, rk4). Run: node notes/fig02/lyap_long.cjs
'use strict';
const g = 9.81, m1 = 1, l1 = 1, m2 = 1, l2 = 1, H = 1 / 600;
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
function dist(a, b) { return Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3]); }
const rad = Math.PI / 180, def = [120 * rad, 150 * rad, 0, 0];
function lyap(T, h, dir) {
    let a = def.slice(), b = def.map((v, i) => v + 1e-8 * dir[i]), sum = 0, out = [];
    const N = Math.round(T / h), every = Math.round(0.1 / h), blk = Math.round(2000 / h);
    for (let k = 1; k <= N; k++) {
        a = rk4(a, h); b = rk4(b, h);
        if (k % every === 0) { const dd = dist(a, b); sum += Math.log(dd / 1e-8); b = a.map((v, i) => v + (b[i] - v) * 1e-8 / dd); }
        if (k % blk === 0) out.push((sum / (k * h)).toFixed(4));
    }
    return out;
}
console.log('h, dir θ1, running mean every 2000 s:', lyap(20000, H, [1, 0, 0, 0]).join(' '));
console.log('h, dir ω2, running mean every 2000 s:', lyap(20000, H, [0, 0, 0, 1]).join(' '));
console.log('h/2, dir θ1, running mean every 2000 s:', lyap(10000, H / 2, [1, 0, 0, 0]).join(' '));
