// The double pendulum of Fig. 13, computed live in the browser (no recorded motion): the films reem.html, construction.html and
// catch.html use it. Same physics and the same controller as tools/fig13/hunt.py and tools/fig13/butterfly_control.py.
//
// Two equal uniform rods, m = 1 kg, l = 1 m, g = 9.8 m/s^2; angles th1, th2 from straight down; conjugate momenta p1, p2.
// H = (B p1^2 - 2 C cos(th1 - th2) p1 p2 + A p2^2) / (2 (A B - C^2 cos^2)) - U1 cos th1 - U2 cos th2,
// A = m a^2 + I + m l^2, B = m a^2 + I, C = m l a, U1 = g (m a + m l), U2 = g m a, with a = l/2, I = m l^2 / 12 (chaos_map.coefficients).
// A motor at the top pin adds a torque tau to dp1/dt (generalised force on th1).
// The butterfly: both rods hanging still, struck with (P1, P2); it closes after T with 24 turns of the lower rod (butterfly.py, Newton).
(function (root) {
    'use strict';
    const m = 1, l = 1, g = 9.8, a = l / 2, I = m * l * l / 12;
    const A = m * a * a + I + m * l * l, B = m * a * a + I, C = m * l * a, U1 = g * (m * a + m * l), U2 = g * m * a;
    const P1 = 3.557312977100609, P2 = 12.211005483946245, T = 2.659405430607505, NTURN = 24;

    function deriv(q1, q2, p1, p2, tau, o) {
        const d = q1 - q2, cs = Math.cos(d), sn = Math.sin(d), det = A * B - C * C * cs * cs;
        const w1 = (B * p1 - C * cs * p2) / det, w2 = (A * p2 - C * cs * p1) / det, e = C * w1 * w2 * sn;
        o[0] = w1; o[1] = w2; o[2] = -e - U1 * Math.sin(q1) + tau; o[3] = e - U2 * Math.sin(q2);
    }
    const k1 = [0, 0, 0, 0], k2 = [0, 0, 0, 0], k3 = [0, 0, 0, 0], k4 = [0, 0, 0, 0];
    function rk4(s, h, tau) {     // one classical Runge-Kutta step, in place; tau held over the step
        deriv(s[0], s[1], s[2], s[3], tau, k1);
        deriv(s[0] + .5 * h * k1[0], s[1] + .5 * h * k1[1], s[2] + .5 * h * k1[2], s[3] + .5 * h * k1[3], tau, k2);
        deriv(s[0] + .5 * h * k2[0], s[1] + .5 * h * k2[1], s[2] + .5 * h * k2[2], s[3] + .5 * h * k2[3], tau, k3);
        deriv(s[0] + h * k3[0], s[1] + h * k3[1], s[2] + h * k3[2], s[3] + h * k3[3], tau, k4);
        for (let i = 0; i < 4; i++) s[i] += h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);
    }
    function energy(s) {
        const c = Math.cos(s[0] - s[1]), det = A * B - C * C * c * c;
        return 0.5 * (B * s[2] * s[2] - 2 * C * c * s[2] * s[3] + A * s[3] * s[3]) / det - U1 * Math.cos(s[0]) - U2 * Math.cos(s[1]);
    }
    function omega1(s) { const c = Math.cos(s[0] - s[1]); return (B * s[2] - C * c * s[3]) / (A * B - C * C * c * c); }

    // The butterfly as n samples over one lap (th1, th2), integrated live from its strike; sub-steps keep the step below 0.2 ms.
    function butterfly(n) {
        const dt = T / (n - 1), sub = Math.max(1, Math.ceil(dt / 2e-4)), h = dt / sub, s = [0, 0, P1, P2];
        const th1 = new Float64Array(n), th2 = new Float64Array(n);
        for (let i = 0; i < n; i++) { th1[i] = s[0]; th2[i] = s[1]; if (i < n - 1) for (let j = 0; j < sub; j++) rk4(s, h, 0); }
        return { T, th1, th2, p1: P1, p2: P2, closure: [s[0], s[1] - 2 * Math.PI * NTURN, s[2] - P1, s[3] - P2] };
    }

    // ---------------------------------------------------------------- the motor's controller (butterfly_control.py, sections 1-4)
    const M = 2400, H = T / M, SUB = 4, Qd = [1, 1, 0.05, 0.05], R = 1e-3, TAU_MAX = 60, KT = 2.5;
    // kE, kA, kI, wait_max, steer_max, window, e_tol, a_tol, catch_at (SETTINGS in butterfly_control.py)
    // catchAt 0.6, eTol 5 J, aTol 3: measured 9 Nov 2026 on 100 random starts (pendulum.js in Node): all caught and held, median 16 s after the
// motor switches on (catchAt 0.2, eTol 1, aTol 1: 29 of 40 within 400 s). The catch's basin: from 0.3 away 16 of 16, from 0.6 12 of 16.
const SET = { kE: 0.01, kA: 0.05, kI: 0.005, waitMax: 12, steerMax: 12, win: 3, eTol: 5, aTol: 3, catchAt: 0.6, eLow: 60, releaseAt: 0.005 };
    function step(s, tau) { for (let j = 0; j < SUB; j++) rk4(s, H / SUB, tau); }     // one control step of H, four sub-steps

    function design() {
        // the orbit at M + 1 points, then the linear step maps Phi_k, B_k by central differences, then the periodic Riccati equation
        const S = [], s = [0, 0, P1, P2];
        for (let k = 0; k <= M; k++) { S.push(s.slice()); if (k < M) step(s, 0); }
        const PHI = [], BB = [], eps = 1e-6;
        for (let k = 0; k < M; k++) {
            const Ph = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
            for (let j = 0; j < 4; j++) {
                const sp = S[k].slice(), sm = S[k].slice(); sp[j] += eps; sm[j] -= eps; step(sp, 0); step(sm, 0);
                for (let i = 0; i < 4; i++) Ph[i][j] = (sp[i] - sm[i]) / (2 * eps);
            }
            const sp = S[k].slice(), sm = S[k].slice(); step(sp, 1e-3); step(sm, -1e-3);
            PHI.push(Ph); BB.push([0, 1, 2, 3].map(i => (sp[i] - sm[i]) / 2e-3));
        }
        let P = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
        const K = new Array(M);
        for (let lap = 0; lap < 60; lap++) {
            const P0 = P.map(r => r.slice());
            for (let k = M - 1; k >= 0; k--) {
                const Ak = PHI[k], b = BB[k];
                const Pb = [0, 1, 2, 3].map(i => P[i][0] * b[0] + P[i][1] * b[1] + P[i][2] * b[2] + P[i][3] * b[3]);    // P b
                const Sg = R + b[0] * Pb[0] + b[1] * Pb[1] + b[2] * Pb[2] + b[3] * Pb[3];
                const bPA = [0, 1, 2, 3].map(j => Pb[0] * Ak[0][j] + Pb[1] * Ak[1][j] + Pb[2] * Ak[2][j] + Pb[3] * Ak[3][j]);   // b^T P A
                K[k] = bPA.map(v => v / Sg);
                const PA = [0, 1, 2, 3].map(i => [0, 1, 2, 3].map(j => P[i][0] * Ak[0][j] + P[i][1] * Ak[1][j] + P[i][2] * Ak[2][j] + P[i][3] * Ak[3][j]));
                const Pn = [0, 1, 2, 3].map(i => [0, 1, 2, 3].map(j => (i === j ? Qd[i] * H : 0)
                    + Ak[0][i] * PA[0][j] + Ak[1][i] * PA[1][j] + Ak[2][i] * PA[2][j] + Ak[3][i] * PA[3][j] - bPA[i] * bPA[j] / Sg));
                for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) P[i][j] = 0.5 * (Pn[i][j] + Pn[j][i]);
            }
            let dmax = 0, pmax = 0; for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { dmax = Math.max(dmax, Math.abs(P[i][j] - P0[i][j])); pmax = Math.max(pmax, Math.abs(P[i][j])); }
            if (lap && dmax < 1e-9 * pmax) break;
        }
        const Pmax = S.reduce((v, x) => Math.max(v, Math.abs(x[2] + x[3])), 0);
        return { S, K, Pmax, Estar: energy([0, 0, P1, P2]) };
    }

    function nearest(D, s, kg, win, sg) {
        let best = 1e18, kb = kg;
        for (let j = -win; j <= win; j++) {
            const k = ((kg + j) % M + M) % M, Sk = D.S[k];
            let v = 0;
            for (let i = 0; i < 4; i++) { let d = s[i] - sg * Sk[i]; if (i < 2) d -= 2 * Math.PI * Math.round(d / (2 * Math.PI)); v += Qd[i] * d * d; }
            if (v < best) { best = v; kb = k; }
        }
        return [kb, Math.sqrt(best)];
    }
    function nearest2(D, s, kg, win, sg) {
        if (win < M / 2) { const [k, d] = nearest(D, s, kg, win, sg); return [k, d, sg]; }
        const [k1, d1] = nearest(D, s, kg, win, 1), [k2, d2] = nearest(D, s, kg, win, -1);
        return d1 <= d2 ? [k1, d1, 1] : [k2, d2, -1];
    }

    // The run: from the state s0 = [th1, th2, p1, p2] (or a strike p = [p1, p2] from hanging still), free for tFree seconds,
    // then the controller; held holdLaps laps after the catch, then let go.
    // modes: -1 free, 0 pump and steer (or drain after a miss), 1 wait, 2 catch and hold, 3 let go.
    function Run(D, p, tFree, holdLaps) {
        this.D = D; this.s0 = p.length === 2 ? [0, 0, p[0], p[1]] : p.slice(); this.tFree = tFree; this.holdLaps = holdLaps; this.reset();
    }
    Run.prototype.reset = function () {
        this.s = this.s0.slice(); this.i = 0; this.t = 0;
        this.mode = -1; this.k = 0; this.dist = 9; this.sg = 1; this.zA = 0; this.zE = 0;
        const nb = Math.round(SET.win / H); this.hist = new Float64Array(nb).fill(Math.abs(this.s0[2] + this.s0[3])); this.hi = 0; this.reach = 0;
        this.hops = 0; this.tHop = -1; this.tSteer = 0; this.drain = false; this.tWait = 0;
        this.ev = { on: this.tFree, wait: null, catch: null, release: null };
        this.log = { t: [], th1: [], th2: [], tau: [], E: [], dist: [], mode: [] };
        this.tau = 0; this.record();
    };
    Run.prototype.record = function () {
        const L = this.log, s = this.s;
        L.t.push(this.t); L.th1.push(s[0]); L.th2.push(s[1]); L.tau.push(this.tau); L.E.push(energy(s)); L.dist.push(this.dist); L.mode.push(this.mode);
    };
    Run.prototype.ctrl = function () {     // the torque for the next step: butterfly_control.catch_anywhere
        const D = this.D, s = this.s, t = this.t, E = energy(s), w1 = omega1(s), P = s[2] + s[3];
        if (this.mode === -1) { if (t >= this.tFree - 1e-9) { this.mode = 0; this.tSteer = t; } else return 0; }
        if (this.mode === 3) return 0;
        this.hist[this.hi] = Math.abs(P); this.hi = (this.hi + 1) % this.hist.length;
        if (this.i % 50 === 0) { let mx = 0; for (const v of this.hist) mx = Math.max(mx, v); this.reach = mx; }
        let tau = 0;
        if (this.mode === 0 && t - this.tSteer > SET.steerMax) { this.hops++; this.tHop = t; this.tSteer = t; this.zA = 0; this.zE = 0; this.drain = true; }
        if (this.mode === 0 && this.drain) {
            tau = SET.kE * (SET.eLow - E) * w1;
            if (E < SET.eLow + 5 || t - this.tHop > 6) { this.drain = false; this.tSteer = t; }
        } else if (this.mode === 0) {
            if (t - this.tFree > SET.win) { this.zA += H * (D.Pmax - this.reach); this.zE += H * (D.Estar - E); }
            tau = (SET.kE * (D.Estar - E) + SET.kI * 0.05 * this.zE) * w1 + (SET.kA * (D.Pmax - this.reach) + SET.kI * this.zA) * P;
            if (t - this.tFree > SET.win && t - this.tSteer > SET.win && Math.abs(E - D.Estar) < SET.eTol && Math.abs(this.reach - D.Pmax) < SET.aTol) {
                this.mode = 1; this.tWait = t; [this.k, this.dist, this.sg] = nearest2(D, s, 0, M / 2, this.sg); if (this.ev.wait === null) this.ev.wait = t;
            }
        } else if (this.mode === 1) {
            if (this.i % 4 === 0) {
                [this.k, this.dist, this.sg] = nearest2(D, s, (this.k + 4) % M, 40, this.sg);
                if (this.i % 400 === 0) [this.k, this.dist, this.sg] = nearest2(D, s, this.k, M / 2, this.sg);
            }
            if (this.dist < SET.catchAt) { this.mode = 2; this.ev.catch = t; }
            else if (t - this.tWait > SET.waitMax) { this.mode = 0; this.hops++; this.tHop = t; this.tSteer = t; this.zA = 0; this.zE = 0; this.drain = true; }
        }
        if (this.mode === 2) {
            [this.k, this.dist, this.sg] = nearest2(D, s, (this.k + 1) % M, 30, this.sg);
            const Sk = D.S[this.k], Kk = D.K[this.k];
            tau = 0;
            for (let j = 0; j < 4; j++) { let d = s[j] - this.sg * Sk[j]; if (j < 2) d -= 2 * Math.PI * Math.round(d / (2 * Math.PI)); tau -= Kk[j] * d; }
            if (this.dist > 1) { this.mode = 0; this.hops++; this.tHop = t; this.tSteer = t; this.zA = 0; this.zE = 0; this.drain = true; tau = 0; this.ev.catch = null; }
            else if (t - this.ev.catch >= this.holdLaps * T && this.dist < SET.releaseAt) { this.mode = 3; this.ev.release = t; tau = 0; }   // let go only once settled
        }
        return Math.max(-TAU_MAX, Math.min(TAU_MAX, tau));
    };
    Run.prototype.advance = function (tTarget, logEvery) {   // integrate up to tTarget, recording every logEvery steps
        while (this.t + 0.5 * H <= tTarget) {
            this.tau = this.ctrl();
            step(this.s, this.tau); this.i++; this.t = this.i * H;
            if (this.mode === 3 && this.i % 400 === 0) { const r = nearest2(this.D, this.s, this.k, M / 2, 1); this.dist = r[1]; }
            if (this.i % logEvery === 0) this.record();
        }
    };

    const api = { deriv, rk4, energy, omega1, butterfly, design, Run, nearest2, consts: { m, l, g, A, B, C, U1, U2, P1, P2, T, NTURN, M, H, TAU_MAX, KT, Qd, R, SET } };
    if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.PEND = api;
})(this);
