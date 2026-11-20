// Fig. 13, the sheet's worker (20 November 2026): integrates the grid of pendulums on a second thread, so that the page's own thread
// only paints and answers the reader. The page sends the model and the strikes ('build') and then asks for n steps at a time ('run');
// the worker answers with the tip positions recorded every REC steps and the states. rk4n and tip are the page's own functions, copied
// letter for letter (tools/fig13/sheet_worker_check.cjs fails if they differ), so a cell's pendulum here and the pinned copy on the page
// follow the same states bit for bit.
'use strict';
const REC = 5;
let par = null, S = null, M = 0, steps = 0, gen = 0;
function rk4n(s, h, n) {
    const { A, B, C, U1, U2 } = par, AB = A * B, CC = C * C, hh = 0.5 * h, h6 = h / 6, sin = Math.sin, cos = Math.cos;
    let a = s[0], b = s[1], p = s[2], q = s[3];
    for (let k = 0; k < n; k++) {
        let d = a - b, c = cos(d), sn = sin(d), det = AB - CC * c * c;
        const a1 = (B * p - C * c * q) / det, b1 = (A * q - C * c * p) / det; let e = C * a1 * b1 * sn;
        const p1 = -e - U1 * sin(a), q1 = e - U2 * sin(b);
        let ta = a + hh * a1, tb = b + hh * b1, tp = p + hh * p1, tq = q + hh * q1;
        d = ta - tb; c = cos(d); sn = sin(d); det = AB - CC * c * c;
        const a2 = (B * tp - C * c * tq) / det, b2 = (A * tq - C * c * tp) / det; e = C * a2 * b2 * sn;
        const p2 = -e - U1 * sin(ta), q2 = e - U2 * sin(tb);
        ta = a + hh * a2; tb = b + hh * b2; tp = p + hh * p2; tq = q + hh * q2;
        d = ta - tb; c = cos(d); sn = sin(d); det = AB - CC * c * c;
        const a3 = (B * tp - C * c * tq) / det, b3 = (A * tq - C * c * tp) / det; e = C * a3 * b3 * sn;
        const p3 = -e - U1 * sin(ta), q3 = e - U2 * sin(tb);
        ta = a + h * a3; tb = b + h * b3; tp = p + h * p3; tq = q + h * q3;
        d = ta - tb; c = cos(d); sn = sin(d); det = AB - CC * c * c;
        const a4 = (B * tp - C * c * tq) / det, b4 = (A * tq - C * c * tp) / det; e = C * a4 * b4 * sn;
        const p4 = -e - U1 * sin(ta), q4 = e - U2 * sin(tb);
        a += h6 * (a1 + 2 * a2 + 2 * a3 + a4); b += h6 * (b1 + 2 * b2 + 2 * b3 + b4); p += h6 * (p1 + 2 * p2 + 2 * p3 + p4); q += h6 * (q1 + 2 * q2 + 2 * q3 + q4);
    }
    s[0] = a; s[1] = b; s[2] = p; s[3] = q;
}
function tip(s) { return [par.l1 * Math.sin(s[0]) + par.l2 * Math.sin(s[1]), par.l1 * Math.cos(s[0]) + par.l2 * Math.cos(s[1])]; }
onmessage = e => {
    const m = e.data;
    if (m.type === 'build') { par = m.par; M = m.strikes.length / 2; S = new Float64Array(4 * M); steps = 0; gen = m.gen;
        for (let q = 0; q < M; q++) { S[4 * q + 2] = m.strikes[2 * q]; S[4 * q + 3] = m.strikes[2 * q + 1]; } return; }
    if (m.type !== 'run' || m.gen !== gen) return;
    const n = m.n, H = m.h, r = Math.floor((steps + n) / REC) - Math.floor(steps / REC), pts = new Float32Array(2 * M * r), s = new Float64Array(4);
    for (let q = 0; q < M; q++) {
        s[0] = S[4 * q]; s[1] = S[4 * q + 1]; s[2] = S[4 * q + 2]; s[3] = S[4 * q + 3];
        let o = 2 * q * r;
        for (let k = 0; k < n;) {
            const j = Math.min(REC - (steps + k) % REC, n - k);
            rk4n(s, H, j); k += j;
            if ((steps + k) % REC === 0) { const [x, y] = tip(s); pts[o++] = x; pts[o++] = y; }
        }
        S[4 * q] = s[0]; S[4 * q + 1] = s[1]; S[4 * q + 2] = s[2]; S[4 * q + 3] = s[3];
    }
    steps += n;
    const st = S.slice();
    postMessage({ gen, n, r, pts, st }, [pts.buffer, st.buffer]);
};
