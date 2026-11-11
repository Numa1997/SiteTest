// Fig. 13, the catch: the statistics quoted in the catch lecture note, from the browser's own code (gift/pendulum.js) run in Node.
//   node tools/fig13/catch_stats.cjs starts SEED [N=100] [SUB=4] [MAXT=900] [OUT.json]   random starts: caught? when? how near after release?
//   node tools/fig13/catch_stats.cjs basin  SEED [N=200] [SUB=4]                          the catch's basin: LQR switched on at a given distance
//   node tools/fig13/catch_stats.cjs strike P1 P2 [SUB=4]                                 one strike from hanging still, free for 8 s (the film's run)
// SUB is the number of RK4 sub-steps per control step (the page uses 4); a result that changes with SUB is an integration artefact.
// Random numbers: mulberry32(SEED). Starts: even n struck from rest with |p_i| <= 12, odd n random angles with |p_i| <= 6 kg m^2/s.
// A chaotic run depends on the last digit of the arithmetic: Node, Chromium and Python agree on the statistics, not on single runs.
'use strict';
const fs = require('fs'), path = require('path');
function load(sub) {
    const src = fs.readFileSync(path.join(__dirname, 'gift', 'pendulum.js'), 'utf8').replace('SUB = 4,', 'SUB = ' + sub + ',');
    const m = { exports: {} }; new Function('module', src).call({}, m); return m.exports;
}
function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const [mode, a1, a2, a3, a4, a5] = process.argv.slice(2);
if (mode === 'starts') {
    const SEED = +a1, N = +(a2 || 100), P = load(+(a3 || 4)), MAXT = +(a4 || 900), rnd = mulberry32(SEED), u = a => (2 * rnd() - 1) * a;
    const D = P.design(), T = P.consts.T, out = [];
    for (let n = 0; n < N; n++) {
        const s0 = n % 2 === 0 ? [0, 0, u(12), u(12)] : [u(Math.PI), u(Math.PI), u(6), u(6)];
        const r = new P.Run(D, s0, 0, 4); let t = 0;
        while (t < MAXT) { t += 1; r.advance(t, 1e9); if (r.mode === 3) break; }
        const sRel = r.s.slice(); let after4 = null;
        if (r.mode === 3) { r.advance(r.ev.release + 4 * T, 1e9); after4 = Math.min(P.nearest2(D, r.s, r.k, P.consts.M / 2, 1)[1], P.nearest2(D, r.s, r.k, P.consts.M / 2, -1)[1]); }
        out.push({ n, s0, caught: r.mode === 3, tCatch: r.ev.catch, tRelease: r.ev.release, misses: r.hops, mirror: r.sg < 0, after4, sRel });
    }
    const ok = out.filter(o => o.caught), tc = ok.map(o => o.tCatch).sort((a, b) => a - b), a4s = ok.map(o => o.after4).sort((a, b) => a - b), q = (v, p) => v[Math.min(v.length - 1, Math.floor(p * v.length))];
    console.log(`seed ${SEED}, ${a3 || 4} sub-steps: ${ok.length} of ${N} caught and released within ${MAXT} s; catch time after the motor switches on: median ${q(tc, .5).toFixed(1)} s, ` +
        `${tc.filter(x => x <= 60).length} within 60 s, 90 % within ${q(tc, .9).toFixed(0)} s, slowest ${tc[tc.length - 1].toFixed(0)} s; mirror butterfly ${ok.filter(o => o.mirror).length}; ` +
        `distance four free laps after release: median ${q(a4s, .5).toFixed(4)}, 90 % below ${q(a4s, .9).toFixed(4)}, worst ${a4s[a4s.length - 1].toFixed(4)}`);
    if (a5) fs.writeFileSync(a5, JSON.stringify(out));
} else if (mode === 'basin') {
    const P = load(+(a3 || 4)), D = P.design(), Qd = P.consts.Qd, M = P.consts.M, rnd = mulberry32(+a1), N = +(a2 || 200);
    const gauss = () => Math.sqrt(-2 * Math.log(rnd() + 1e-300)) * Math.cos(2 * Math.PI * rnd()), line = [];
    for (const d of [0.1, 0.2, 0.3, 0.4, 0.6, 0.8]) {      // a random point of the lap, a random direction of weighted length d, the LQR on from the start
        let ok = 0;
        for (let n = 0; n < N; n++) {
            const k = Math.floor(rnd() * M), w = [0, 1, 2, 3].map(i => gauss() / Math.sqrt(Qd[i])), nrm = Math.sqrt(w.reduce((s, v, i) => s + Qd[i] * v * v, 0));
            const r = new P.Run(D, D.S[k].map((v, i) => v + d * w[i] / nrm), 0, 4); r.mode = 2; r.k = k; r.ev.catch = 0; r.dist = d;
            for (let t = 1; t <= 60; t++) { r.advance(t, 1e9); if (r.mode === 0 || r.mode === 1) break; if (r.mode === 3 || (r.dist < 0.005 && t > 8)) { ok++; break; } }
        }
        line.push(`${d}: ${ok}/${N}`);
    }
    console.log(`basin, seed ${a1}: held (within 0.005, never past 1) from distance ` + line.join(', '));
} else if (mode === 'strike') {
    const P = load(+(a3 || 4)), D = P.design(), r = new P.Run(D, [+a1, +a2], 8, 4); r.advance(600, 1e9);
    console.log(`strike (${a1}, ${a2}), free 8 s: steering settled ${r.ev.wait}, caught ${r.ev.catch}, let go ${r.ev.release} s; misses ${r.hops}`);
} else console.log('see the head of this file');
