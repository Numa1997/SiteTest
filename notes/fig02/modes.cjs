// Fig. 2, Exercise 5.1: periods from the page's own integrator, equal masses and lengths, starts (5°, 7°) and (5°, −7°).
// Physics lines copied from the page. Run: node notes/fig02/modes.cjs
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
const rad = Math.PI / 180;
for (const t2 of [7, -7]) {
    let s = [5 * rad, t2 * rad, 0, 0], prev = s[0], cross = [];
    for (let k = 1; k <= 60 * 600; k++) { s = rk4(s, H); if (prev > 0 && s[0] <= 0) cross.push(k * H - H * s[0] / (s[0] - prev)); prev = s[0]; }
    const T10 = cross[10] - cross[0];
    console.log('start 5°,', t2 + '°: ten periods', T10.toFixed(3), 's, one period', (T10 / 10).toFixed(4), 's');
}
