// The double pendulum of Fig. 13, computed live in the browser (no recorded motion): the films reem.html, construction.html and
// catch.html use it. Same physics and the same controller as tools/fig13/hunt.py and tools/fig13/butterfly_control.py.
//
// Two equal uniform rods, m = 1 kg, l = 1 m, g = 9.8 m/s^2; angles th1, th2 from straight down; conjugate momenta p1, p2.
// H = (B p1^2 - 2 C cos(th1 - th2) p1 p2 + A p2^2) / (2 (A B - C^2 cos^2)) - U1 cos th1 - U2 cos th2,
// A = m a^2 + I + m l^2, B = m a^2 + I, C = m l a, U1 = g (m a + m l), U2 = g m a, with a = l/2, I = m l^2 / 12 (chaos_map.coefficients).
// A motor at the top pin adds a torque tau to dp1/dt (generalised force on th1).
// The butterfly: both rods hanging still, struck with (P1, P2); it closes after T with 24 turns of the lower rod (butterfly.py, Newton).
// The motor can be asked for any closed orbit of TARGETS (ten flowers, four butterflies). Butterflies: pump and steer, wait, catch with
// periodic gains (as in butterfly_control.py). Flowers: energy, angular momentum and turn (whirlTau; in this file only, measured in
// docs/simulations/fig13-momentum-spirographs.md).
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

    // The closed drawings of the flower hunt (public/scripts/fig13-hunt-data.js, from tools/fig13/hunt.py and butterfly.py): each is the
    // pendulum hanging still, struck with (p1, p2); its state returns after T. The motor can be asked for any of them.
    const TARGETS = [
        { kind: 'flower', k: 3, name: 'flower, 3 petals', p1: 24.419586238808712, p2: -0.0004607745336384989, T: 0.4465718978201654, stability: 'stable' },
        { kind: 'flower', k: 4, name: 'flower, 4 petals', p1: -17.426342306916315, p2: 5.755006385053785, T: 0.3495292453352251, stability: 'neutral' },
        { kind: 'flower', k: 5, name: 'flower, 5 petals', p1: -17.74793623783917, p2: 0.2477671480785474, T: 0.9508984745254958, stability: 'stable' },
        { kind: 'flower', k: 5, name: 'flower, 5 petals', p1: -16.412625902102565, p2: 7.991411096162447, T: 0.3799963324636021, stability: 'neutral' },
        { kind: 'flower', k: 5, name: 'flower, 5 petals', p1: 7.671772722010223, p2: 16.82458162193583, T: 0.5034102393217916, stability: 'neutral' },
        { kind: 'flower', k: 7, name: 'flower, 7 petals', p1: -30.04130416905347, p2: 2.518723444743994, T: 0.5714901911342563, stability: 'neutral' },
        { kind: 'flower', k: 7, name: 'flower, 7 petals', p1: -28.03235376302406, p2: 0.47553121378988383, T: 0.7940805909588777, stability: 'neutral' },
        { kind: 'flower', k: 7, name: 'flower, 7 petals', p1: -24.12612037391662, p2: 0.4251953641427306, T: 0.9265459006964112, stability: 'neutral' },
        { kind: 'flower', k: 7, name: 'flower, 7 petals', p1: 7.513697070897135, p2: 12.342943405762057, T: 1.3281056695459412, stability: 'unstable' },
        { kind: 'flower', k: 8, name: 'flower, 8 petals', p1: 9.282445657594842, p2: 15.47837590601134, T: 1.1233131243070957, stability: 'stable' },
        { kind: 'butterfly', k: 12, name: 'butterfly, 12 turns', p1: 3.4376141146207613, p2: 7.845559204869023, T: 2.3176915902889834, stability: 'unstable' },
        { kind: 'butterfly', k: 18, name: 'butterfly, 18 turns', p1: 3.5587349114936213, p2: 10.212011840611115, T: 2.477276212981421, stability: 'neutral' },
        { kind: 'butterfly', k: 24, name: 'butterfly, 24 turns', p1: 3.557312977100609, p2: 12.211005483946245, T: 2.659405430607505, stability: 'neutral' },
        { kind: 'butterfly', k: 32, name: 'butterfly, 32 turns', p1: 3.5542239000745335, p2: 14.097850207770898, T: 2.999701066775611, stability: 'neutral' }
    ];
    // n samples of (th1, th2) over one lap of a target, for drawing it
    function orbit(tg, n) {
        const dt = tg.T / (n - 1), sub = Math.max(1, Math.ceil(dt / 2e-4)), h = dt / sub, s = [0, 0, tg.p1, tg.p2];
        const th1 = new Float64Array(n), th2 = new Float64Array(n);
        for (let i = 0; i < n; i++) { th1[i] = s[0]; th2[i] = s[1]; if (i < n - 1) for (let j = 0; j < sub; j++) rk4(s, h, 0); }
        return { th1, th2 };
    }

    // ---------------------------------------------------------------- the motor's controller (butterfly_control.py, sections 1-4)
    const M = 2400, H = T / M, SUB = 4, Qd = [1, 1, 0.05, 0.05], R = 1e-3, TAU_MAX = 60, KT = 2.5;
    // kE, kA, kI, wait_max, steer_max, window, e_tol, a_tol, catch_at (SETTINGS in butterfly_control.py)
    // catchAt 0.6, eTol 5 J, aTol 3: measured 11 Nov 2026 with tools/fig13/catch_stats.cjs on three sets of 100 random starts (seeds 1, 2, 2026):
    // all caught and held, median 17.5 to 18.9 s after the motor switches on, slowest 229 s; the same count at 8 and 16 sub-steps.
    // (catchAt 0.2, eTol 1, aTol 1: 29 of 40 within 400 s.) The catch's basin, 200 random states per distance: 0.3: 140, 0.6: 62 held.
const SET = { kE: 0.01, kA: 0.05, kI: 0.005, waitMax: 12, steerMax: 12, win: 3, eTol: 5, aTol: 3, catchAt: 0.6, eLow: 60, releaseAt: 0.005 };
    // whirling orbits: rates of the energy and angular-momentum loops (1/s), averaging time (s), energy window in which a catch may start (J),
    // fraction of E* up to which the motor simply pumps, time allowed before starting over (s); for steadily whirling orbits: rate of the
    // turn loop (1/s), largest detuning of the angular momentum (fraction of Pbar), distance at which it counts as caught, as lost, and at
    // which the film lets go
    const WH = { cE: 2, cL: 1.5, tm: 0.2, eCatch: 15, pumpTo: 0.6, steerMax: 25, kpsi: 0.8, detune: 0.12, lockAt: 0.2, lockOut: 0.7, releaseAt: 0.05 };
    function step(s, tau, h) { for (let j = 0; j < SUB; j++) rk4(s, h / SUB, tau); }     // one control step of h, four sub-steps

    // design(): the butterfly of the films (2400 steps a lap). design(tg): any closed orbit tg = { p1, p2, T }; its lap is cut into
    // Mt = round(T / H) control steps of Ht = T / Mt, so the step stays within 0.2 % of the butterfly's 1.108 ms and tiles the lap exactly.
    function design(tg) {
        // the orbit at M + 1 points, then the linear step maps Phi_k, B_k by central differences, then the periodic Riccati equation
        const p1 = tg ? tg.p1 : P1, p2 = tg ? tg.p2 : P2, Tt = tg ? tg.T : T, Mt = tg ? Math.round(Tt / H) : M, Ht = Tt / Mt;
        const S = [], s = [0, 0, p1, p2];
        for (let k = 0; k <= Mt; k++) { S.push(s.slice()); if (k < Mt) step(s, 0, Ht); }
        const PHI = [], BB = [], eps = 1e-6;
        for (let k = 0; k < Mt; k++) {
            const Ph = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
            for (let j = 0; j < 4; j++) {
                const sp = S[k].slice(), sm = S[k].slice(); sp[j] += eps; sm[j] -= eps; step(sp, 0, Ht); step(sm, 0, Ht);
                for (let i = 0; i < 4; i++) Ph[i][j] = (sp[i] - sm[i]) / (2 * eps);
            }
            const sp = S[k].slice(), sm = S[k].slice(); step(sp, 1e-3, Ht); step(sm, -1e-3, Ht);
            PHI.push(Ph); BB.push([0, 1, 2, 3].map(i => (sp[i] - sm[i]) / 2e-3));
        }
        let P = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
        const K = new Array(Mt); let converged = false;
        for (let lap = 0; lap < 400; lap++) {
            const P0 = P.map(r => r.slice());
            for (let k = Mt - 1; k >= 0; k--) {
                const Ak = PHI[k], b = BB[k];
                const Pb = [0, 1, 2, 3].map(i => P[i][0] * b[0] + P[i][1] * b[1] + P[i][2] * b[2] + P[i][3] * b[3]);    // P b
                const Sg = R + b[0] * Pb[0] + b[1] * Pb[1] + b[2] * Pb[2] + b[3] * Pb[3];
                const bPA = [0, 1, 2, 3].map(j => Pb[0] * Ak[0][j] + Pb[1] * Ak[1][j] + Pb[2] * Ak[2][j] + Pb[3] * Ak[3][j]);   // b^T P A
                K[k] = bPA.map(v => v / Sg);
                const PA = [0, 1, 2, 3].map(i => [0, 1, 2, 3].map(j => P[i][0] * Ak[0][j] + P[i][1] * Ak[1][j] + P[i][2] * Ak[2][j] + P[i][3] * Ak[3][j]));
                const Pn = [0, 1, 2, 3].map(i => [0, 1, 2, 3].map(j => (i === j ? Qd[i] * Ht : 0)
                    + Ak[0][i] * PA[0][j] + Ak[1][i] * PA[1][j] + Ak[2][i] * PA[2][j] + Ak[3][i] * PA[3][j] - bPA[i] * bPA[j] / Sg));
                for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) P[i][j] = 0.5 * (Pn[i][j] + Pn[j][i]);
            }
            let dmax = 0, pmax = 0; for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { dmax = Math.max(dmax, Math.abs(P[i][j] - P0[i][j])); pmax = Math.max(pmax, Math.abs(P[i][j])); }
            if (lap && dmax < 1e-9 * pmax) { converged = true; break; }
        }
        const Pmax = S.reduce((v, x) => Math.max(v, Math.abs(x[2] + x[3])), 0);
        const dth = k => { const d = S[Mt][k] - S[0][k]; return d - 2 * Math.PI * Math.round(d / (2 * Math.PI)); };
        const closure = Math.max(Math.abs(dth(0)), Math.abs(dth(1)), Math.abs(S[Mt][2] - S[0][2]), Math.abs(S[Mt][3] - S[0][3]));   // how well the lap closes, in this arithmetic
        // Two kinds of closed orbit. Swinging (the butterflies): the upper rod swings to and fro, p1 + p2 rises and falls by half its size.
        // Whirling (the flowers): both rods go round, and p1 + p2, the angular momentum about the pin, stays within a few per cent of
        // its mean: with gravity off it would be exactly constant. A whirling orbit is named by its energy, that mean (Pbar), and whether
        // the lower rod turns faster or slower than the upper one (sense = sign of mean(w2 - w1) * Pbar).
        let Pbar = 0, Psq = 0, rel = 0; const o = [0, 0, 0, 0];
        for (let k = 0; k < Mt; k++) { const x = S[k], q = x[2] + x[3]; Pbar += q / Mt; Psq += q * q / Mt; deriv(x[0], x[1], x[2], x[3], 0, o); rel += (o[1] - o[0]) / Mt; }
        const whirl = Math.sqrt(Math.max(0, Psq - Pbar * Pbar)) < 0.1 * Math.abs(Pbar);
        // steady: the upper rod never stops or turns back on the lap (it whirls steadily). For these the motor does not use the gains K:
        // it locks the energy, the angular momentum and the turn of the whole picture (see Run.whirlTau).
        let wmin = 1e9, wmax = -1e9; for (let k = 0; k < Mt; k++) { const w = omega1(S[k]); wmin = Math.min(wmin, w); wmax = Math.max(wmax, w); }
        const Dn = { S, K, Pmax, Estar: energy([0, 0, p1, p2]), M: Mt, H: Ht, T: Tt, p1, p2, closure, converged, whirl, steady: whirl && wmin * wmax > 0,
                     Pbar: Math.abs(Pbar), Lsign: Math.sign(Pbar), sense: Math.sign(rel * Pbar), cpsi: 0 };
        if (Dn.steady) {
            // How fast does the whole picture turn when the angular momentum is a little off, at the same energy? Strike a little differently
            // along the direction in (p1, p2) that leaves the energy alone, (-w2, w1), run one lap, and read the turn psi of the picture.
            deriv(0, 0, p1, p2, 0, o); const nn = Math.hypot(o[0], o[1]); let c = 0;
            for (const e of [0.05, -0.05]) {
                const x = [0, 0, p1 - e * o[1] / nn, p2 + e * o[0] / nn]; let Lm = 0;
                for (let k = 0; k < Mt; k++) { Lm += (x[2] + x[3]) / Mt; step(x, 0, Ht); }
                c += 0.5 * phase(Dn, x, 1)[1] / (Tt * (Lm - Pbar));
            }
            Dn.cpsi = c;      // rad/s of turning per kg m^2/s of excess angular momentum
        }
        return Dn;
    }

    function nearest(D, s, kg, win, sg) {
        let best = 1e18, kb = kg;
        for (let j = -win; j <= win; j++) {
            const M = D.M, k = ((kg + j) % M + M) % M, Sk = D.S[k];
            let v = 0;
            for (let i = 0; i < 4; i++) { let d = s[i] - sg * Sk[i]; if (i < 2) d -= 2 * Math.PI * Math.round(d / (2 * Math.PI)); v += Qd[i] * d * d; }
            if (v < best) { best = v; kb = k; }
        }
        return [kb, Math.sqrt(best)];
    }
    // Where on the lap is the state, and by how much is the whole picture turned about the pin? The angle between the rods and the two
    // momenta do not change when the pendulum is turned as a whole (exactly so without gravity); they give the place k on the lap. The
    // turn psi is then the upper rod's angle minus the orbit's at k. (A flower of n petals has n such places; the small weight on psi
    // picks the one that needs the least turning.)
    function phase(D, s, sg) {
        const M = D.M, dl = s[0] - s[1], TP = 2 * Math.PI; let best = 1e18, kb = 0, pb = 0;
        for (let k = 0; k < M; k++) {
            const x = D.S[k]; let a = dl - sg * (x[0] - x[1]); a -= TP * Math.round(a / TP);
            const b = s[2] - sg * x[2], c = s[3] - sg * x[3]; let ps = s[0] - sg * x[0]; ps -= TP * Math.round(ps / TP);
            const v = a * a + 0.05 * (b * b + c * c) + 0.02 * ps * ps;
            if (v < best) { best = v; kb = k; pb = ps; }
        }
        return [kb, pb];
    }
    function nearest2(D, s, kg, win, sg) {
        if (win < Math.floor(D.M / 2)) { const [k, d] = nearest(D, s, kg, win, sg); return [k, d, sg]; }
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
        this.t0 = 0; this.i0 = 0;                       // the clock: t = t0 + (i - i0) H of the present target
        const nb = Math.round(SET.win / this.D.H); this.hist = new Float64Array(nb).fill(Math.abs(this.s0[2] + this.s0[3])); this.hi = 0; this.reach = 0;
        this.hops = 0; this.tHop = -1; this.tSteer = 0; this.drain = false; this.tWait = 0;
        this.Pm = this.s0[2] + this.s0[3]; this.wm = 0; this.w2m = 0; this.rm = 0; this.slips = 0; this.psi = 0;    // running means for the whirling orbits
        this.ev = { on: this.tFree, wait: null, catch: null, release: null };
        this.log = { t: [], th1: [], th2: [], tau: [], E: [], dist: [], mode: [] };
        this.tau = 0; this.record();
    };
    // The motor waits for a request: with tFree = Infinity the pendulum stays free until engage() is called. letGo() frees it again.
    Run.prototype.engage = function () {
        if (this.mode === 3) { this.mode = -1; this.ev.catch = null; this.ev.release = null; this.ev.wait = null; this.zA = 0; this.zE = 0; this.drain = false; this.hops = 0; this.dist = 9; }
        if (this.mode === -1) { this.tFree = this.t; this.ev.on = this.t; }
    };
    // Ask for another closed orbit, at any moment. A free pendulum stays free; a motor at work leaves what it was doing and starts
    // again for the new target (pump and steer to its energy and swing, wait, catch).
    Run.prototype.setTarget = function (D2) {
        if (D2 === this.D) return;
        this.t0 = this.t; this.i0 = this.i; this.D = D2;
        const nb = Math.round(SET.win / D2.H); this.hist = new Float64Array(nb).fill(this.reach || Math.abs(this.s[2] + this.s[3])); this.hi = 0;
        this.k = 0; this.dist = 9; this.sg = 1; this.zA = 0; this.zE = 0; this.drain = false; this.hops = 0; this.slips = 0; this.psi = 0;
        this.ev.wait = null; this.ev.catch = null; this.ev.release = null;
        if (this.mode === 3) this.mode = -1;
        else if (this.mode >= 0) { this.mode = 0; this.tFree = this.t; this.tSteer = this.t; this.ev.on = this.t; }
    };
    Run.prototype.letGo = function () { if (this.mode >= 0 && this.mode !== 3) { this.mode = 3; this.ev.release = this.t; } };
    Run.prototype.record = function () {
        const L = this.log, s = this.s;
        L.t.push(this.t); L.th1.push(s[0]); L.th2.push(s[1]); L.tau.push(this.tau); L.E.push(energy(s)); L.dist.push(this.dist); L.mode.push(this.mode);
    };
    Run.prototype.ctrl = function () {     // the torque for the next step: butterfly_control.catch_anywhere
        const D = this.D, M = D.M, HALF = Math.floor(M / 2), H = D.H, s = this.s, t = this.t, E = energy(s), w1 = omega1(s), P = s[2] + s[3];
        if (this.mode === -1) { if (t >= this.tFree - 1e-9) { this.mode = 0; this.tSteer = t; } else return 0; }
        if (this.mode === 3) return 0;
        this.hist[this.hi] = Math.abs(P); this.hi = (this.hi + 1) % this.hist.length;
        if (D.whirl) { deriv(s[0], s[1], s[2], s[3], 0, k1); const al = H / WH.tm; this.Pm += al * (P - this.Pm); this.wm += al * (w1 - this.wm); this.w2m += al * (w1 * w1 - this.w2m); this.rm += al * (k1[1] - k1[0] - this.rm); }
        if (this.i % 50 === 0) { let mx = 0; for (const v of this.hist) mx = Math.max(mx, v); this.reach = mx; }
        let tau = 0;
        if (this.mode === 0 && t - this.tSteer > (D.whirl ? WH.steerMax : SET.steerMax)) { this.hops++; this.tHop = t; this.tSteer = t; this.zA = 0; this.zE = 0; this.drain = true; }
        if (this.mode === 0 && this.drain) {
            tau = SET.kE * (SET.eLow - E) * w1;
            if (E < SET.eLow + 5 || t - this.tHop > 6) { this.drain = false; this.tSteer = t; }
        } else if (this.mode === 0 && D.whirl) {
            tau = this.whirlTau(E, w1);
            // with the energy and the momentum right the tip already draws the flower, turned by some angle; a steadily whirling flower is
            // turned into place by the same law (whirlTau), the others are handed to the catch when close enough
            if (this.i % 16 === 0 && Math.abs(D.Estar - E) < WH.eCatch) {
                [this.k, this.dist, this.sg] = nearest2(D, s, 0, HALF, this.sg);
                if (this.dist < (D.steady ? WH.lockAt : SET.catchAt)) { this.mode = 2; this.ev.catch = t; if (this.ev.wait === null) this.ev.wait = t; }
            }
        } else if (this.mode === 0) {
            if (t - this.tFree > SET.win) { this.zA += H * (D.Pmax - this.reach); this.zE += H * (D.Estar - E); }
            tau = (SET.kE * (D.Estar - E) + SET.kI * 0.05 * this.zE) * w1 + (SET.kA * (D.Pmax - this.reach) + SET.kI * this.zA) * P;
            if (t - this.tFree > SET.win && t - this.tSteer > SET.win && Math.abs(E - D.Estar) < SET.eTol && Math.abs(this.reach - D.Pmax) < SET.aTol) {
                this.mode = 1; this.tWait = t; [this.k, this.dist, this.sg] = nearest2(D, s, 0, HALF, this.sg); if (this.ev.wait === null) this.ev.wait = t;
            }
        } else if (this.mode === 1) {
            if (this.i % 4 === 0) {
                [this.k, this.dist, this.sg] = nearest2(D, s, (this.k + 4) % M, 40, this.sg);
                if (this.i % 400 === 0) [this.k, this.dist, this.sg] = nearest2(D, s, this.k, HALF, this.sg);
            }
            if (this.dist < SET.catchAt) { this.mode = 2; this.ev.catch = t; }
            else if (t - this.tWait > SET.waitMax) { this.mode = 0; this.hops++; this.tHop = t; this.tSteer = t; this.zA = 0; this.zE = 0; this.drain = true; }
        }
        if (this.mode === 2 && D.steady) {
            tau = this.whirlTau(E, w1);
            if (this.i % 16 === 0) [this.k, this.dist, this.sg] = nearest2(D, s, 0, HALF, this.sg);
            if (this.dist > WH.lockOut) { this.mode = 0; this.slips++; this.tSteer = t; this.ev.catch = null; }
            else if (t - this.ev.catch >= this.holdLaps * D.T && this.dist < WH.releaseAt) { this.mode = 3; this.ev.release = t; tau = 0; }
        } else if (this.mode === 2) {
            [this.k, this.dist, this.sg] = nearest2(D, s, (this.k + 1) % M, 30, this.sg);
            const Sk = D.S[this.k], Kk = D.K[this.k];
            tau = 0;
            for (let j = 0; j < 4; j++) { let d = s[j] - this.sg * Sk[j]; if (j < 2) d -= 2 * Math.PI * Math.round(d / (2 * Math.PI)); tau -= Kk[j] * d; }
            if (this.dist > 1 && D.whirl) { this.mode = 0; this.slips++; this.tSteer = t; tau = 0; this.ev.catch = null; }      // a whirling orbit: energy and momentum are still right, steer on and try again
            else if (this.dist > 1) { this.mode = 0; this.hops++; this.tHop = t; this.tSteer = t; this.zA = 0; this.zE = 0; this.drain = true; tau = 0; this.ev.catch = null; }
            else if (t - this.ev.catch >= this.holdLaps * D.T && this.dist < SET.releaseAt) { this.mode = 3; this.ev.release = t; tau = 0; }   // let go only once settled
        }
        return Math.max(-TAU_MAX, Math.min(TAU_MAX, tau));
    };
    // The torque for a whirling orbit. One torque moves the energy and the angular momentum together: dE/dt = tau w1, dP/dt = tau
    // (+ gravity, which averages out). With tau = a w1 + b and the rod's turning uneven: dE/dt = a <w1^2> + b <w1>, dP/dt = a <w1> + b;
    // ask for dE/dt = cE (E* - E) and dP/dt = cL (Lref - P) and solve for a and b. Which mirror image: the one whose lower rod already
    // turns the way this one does (the motor holds the upper rod; it cannot quickly reverse the lower one). For a steadily whirling
    // orbit Lref is detuned a little from the orbit's own value while the picture is turned by psi: a little more angular momentum
    // turns the whole flower forward at cpsi rad/s per unit, so Lref = Pbar - (kpsi / cpsi) psi brings psi to zero at the rate kpsi.
    Run.prototype.whirlTau = function (E, w1) {
        const D = this.D, sgn = D.sense * (this.rm >= 0 ? 1 : -1), dE = D.Estar - E;
        if (E < WH.pumpTo * D.Estar) { this.psi = 0; return SET.kE * dE * w1; }
        let Lref = sgn * D.Pbar;
        if (D.steady && Math.abs(dE) < WH.eCatch) {
            if (this.i % 8 === 0) this.psi = phase(D, this.s, sgn * D.Lsign)[1];
            Lref += Math.max(-WH.detune * D.Pbar, Math.min(WH.detune * D.Pbar, -(WH.kpsi / D.cpsi) * this.psi));
        }
        const v = Math.max(this.w2m - this.wm * this.wm, 4), Ed = WH.cE * dE, Ld = WH.cL * (Lref - this.Pm), a = (Ed - this.wm * Ld) / v;
        return a * w1 + Ld - a * this.wm;
    };
    Run.prototype.advance = function (tTarget, logEvery) {   // integrate up to tTarget, recording every logEvery steps
        while (this.t + 0.5 * this.D.H <= tTarget) {
            this.tau = this.ctrl();
            const H = this.D.H; step(this.s, this.tau, H); this.i++; this.t = this.t0 + (this.i - this.i0) * H;
            if (this.mode === 3 && this.i % 400 === 0) { const r = nearest2(this.D, this.s, this.k, Math.floor(this.D.M / 2), 1); this.dist = r[1]; }
            if (this.i % logEvery === 0) this.record();
        }
    };

    const api = { deriv, rk4, energy, omega1, butterfly, orbit, TARGETS, design, Run, nearest2, phase, consts: { m, l, g, A, B, C, U1, U2, P1, P2, T, NTURN, M, H, TAU_MAX, KT, Qd, R, SET } };
    if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.PEND = api;
})(this);
