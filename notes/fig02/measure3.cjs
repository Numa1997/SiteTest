// Fig. 2 measurements, part 3: where RK4 at h = 1/600 s fails. Physics lines copied from the page, as in measure.cjs.
// Run: node notes/fig02/measure3.cjs
'use strict';
const g = 9.81, m1 = 1, l1 = 1, H = 1 / 600;
let m2 = 1, l2 = 1;
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
function energy(s) {
    var kin = 0.5 * (m1 + m2) * l1 * l1 * s[2] * s[2] + 0.5 * m2 * l2 * l2 * s[3] * s[3]
        + m2 * l1 * l2 * s[2] * s[3] * Math.cos(s[0] - s[1]);
    var pot = -(m1 + m2) * g * l1 * Math.cos(s[0]) - m2 * g * l2 * Math.cos(s[1]);
    return kin + pot;
}
const rad = Math.PI / 180;
function run(ms, ls, s0deg, h, T) {
    m2 = m1 * Math.exp(ms); l2 = l1 * Math.exp(ls);
    let s = [s0deg[0] * rad, s0deg[1] * rad, s0deg[2], s0deg[3]];
    const E0 = energy(s), Es = (m1 + m2) * g * l1 + m2 * g * l2;
    let mx = 0, w1max = 0, w2max = 0, a1max = 0;
    const N = Math.round(T / h), per = Math.round((1 / 60) / h);
    for (let k = 1; k <= N; k++) {
        s = rk4(s, h);
        w1max = Math.max(w1max, Math.abs(s[2])); w2max = Math.max(w2max, Math.abs(s[3]));
        if (k % per === 0) mx = Math.max(mx, Math.abs((energy(s) - E0) / Es));
    }
    return { m2: +m2.toFixed(3), l2: +l2.toFixed(3), E0: +E0.toFixed(2), Es: +Es.toFixed(2), maxAbsEps: mx, w1max: +w1max.toFixed(1), w2max: +w2max.toFixed(1), stepsPerRadOfFastestTurn: +(1 / (Math.max(w1max, w2max) * h)).toFixed(1) };
}
const cases = [
    ['default', 0, 0, [120, 150, 0, 0]],
    ['m2/m1 = 10', 2.3, 0, [120, 150, 0, 0]],
    ['m2/m1 = 10, l2/l1 = 5', 2.3, 1.6, [120, 150, 0, 0]],
    ['m2/m1 = 10, l2/l1 = 0.2', 2.3, -1.6, [120, 150, 0, 0]],
    ['m2/m1 = 0.1', -2.3, 0, [120, 150, 0, 0]],
    ['m2/m1 = 0.1, l2/l1 = 0.2', -2.3, -1.6, [120, 150, 0, 0]],
    ['l2/l1 = 0.2', 0, -1.6, [120, 150, 0, 0]],
    ['l2/l1 = 5', 0, 1.6, [120, 150, 0, 0]],
    ['default angles, w = +-5', 0, 0, [120, 150, 5, -5]],
    ['m2/m1 = 10, w = 5, -5', 2.3, 0, [120, 150, 5, -5]],
    ['worst grid corner', 2.3, 1.6, [90, -90, 5, -5]],
    ['m2/m1 = 10, 180, 180', 2.3, 0, [180, 180, 0, 0]],
    ['m2/m1 = 10, 90, -90', 2.3, 0, [90, -90, 0, 0]]
];
for (const c of cases) {
    const r1 = run(c[1], c[2], c[3], H, 20), r2 = run(c[1], c[2], c[3], H / 2, 20), r4 = run(c[1], c[2], c[3], H / 4, 20);
    console.log(c[0].padEnd(28), JSON.stringify(r1), ' | h/2:', r2.maxAbsEps.toExponential(2), ' h/4:', r4.maxAbsEps.toExponential(2));
}
// sweep the mass ratio at the default angles: worst |eps| in 20 s
console.log('mass-ratio sweep, default angles, l2 = l1, 20 s:');
for (const ms of [0, 0.5, 1, 1.5, 1.8, 2.0, 2.1, 2.2, 2.3]) { const r = run(ms, 0, [120, 150, 0, 0], H, 20); console.log('  m2/m1 =', Math.exp(ms).toFixed(2), 'max|eps| =', r.maxAbsEps.toExponential(2), 'max|w1| =', r.w1max); }
