// Fig. 2: at mass ratio 10 (default angles), where in the motion does RK4 lose its energy? Largest per-step energy jumps
// against the angle between the rods. Physics copied from the page. Run: node notes/fig02/where.cjs
'use strict';
const g = 9.81, m1 = 1, l1 = 1, H = 1 / 600; let m2 = Math.exp(2.3), l2 = 1;
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
    var kin = 0.5 * (m1 + m2) * l1 * l1 * s[2] * s[2] + 0.5 * m2 * l2 * l2 * s[3] * s[3] + m2 * l1 * l2 * s[2] * s[3] * Math.cos(s[0] - s[1]);
    return kin - (m1 + m2) * g * l1 * Math.cos(s[0]) - m2 * g * l2 * Math.cos(s[1]);
}
const rad = Math.PI / 180, Es = (m1 + m2) * g * l1 + m2 * g * l2;
let s = [120 * rad, 150 * rad, 0, 0], E = energy(s); const jumps = [];
for (let k = 1; k <= 20 * 600; k++) {
    const n = rk4(s, H), En = energy(n);
    let d = (s[0] - s[1]) % (2 * Math.PI); if (d > Math.PI) d -= 2 * Math.PI; if (d < -Math.PI) d += 2 * Math.PI;
    jumps.push([Math.abs(En - E) / Es, d, Math.abs(s[2]), Math.abs(deriv(s)[2]), k * H]); s = n; E = En;
}
jumps.sort((a, b) => b[0] - a[0]);
const tot = jumps.reduce((a, j) => a + j[0], 0), top = jumps.slice(0, 120), topSum = top.reduce((a, j) => a + j[0], 0);
console.log('sum of |dE| per step / Es over 20 s:', tot.toExponential(2), '; the largest 120 steps (1 %) carry', (100 * topSum / tot).toFixed(0), '%');
console.log('|delta| (deg) at the 12 largest jumps:', top.slice(0, 12).map(j => (Math.abs(j[1]) / rad).toFixed(0)).join(' '));
console.log('|alpha1| at those steps (rad/s^2):', top.slice(0, 12).map(j => j[3].toFixed(0)).join(' '), '; times:', top.slice(0, 12).map(j => j[4].toFixed(2)).join(' '));
const near = top.filter(j => Math.abs(Math.sin(j[1])) < 0.5).length; console.log('of the top 120, with |sin delta| < 0.5 (rods within 30 deg of in line or folded):', near);
let a1max = 0; for (const j of jumps) a1max = Math.max(a1max, j[3]); console.log('max |alpha1| over 20 s:', a1max.toFixed(0));
m2 = 1; let s1 = [120 * rad, 150 * rad, 0, 0], a1d = 0; for (let k = 1; k <= 12000; k++) { a1d = Math.max(a1d, Math.abs(deriv(s1)[2])); s1 = rk4(s1, H); } console.log('equal masses: max |alpha1| over 20 s:', a1d.toFixed(0));
