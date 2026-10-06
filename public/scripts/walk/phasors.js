/* From symbols to code — Fig. 7, phasor sums.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live() in phasor-sums.html. Values for "arm 1" refer to the first circle card. */
window.WALK = window.WALK || {};

window.WALK.phasors = {
    intro: 'Eight steps from “an arm turning at a steady rate” to the curve on the screen and the song that shakes it. Every value in the table is read live from the arrays the figure is drawn from.',
    steps: [
        {
            title: 'One arm: a phasor',
            where: 'sumAt() — inside the loop over arms',
            math: 'z<sub>1</sub>(t) = ⟦A|A⟧ e<sup>i ⟦ang|(ωt + φ)⟧</sup> = ⟦x1|A cos(ωt + φ)⟧ + i ⟦y1|A sin(ωt + φ)⟧',
            note: 'Euler’s formula e<sup>iθ</sup> = cos θ + i sin θ turns one complex number into two real ones: the x and y of the arm’s tip relative to its pivot. The angle grows linearly in time; that is all “uniform circular motion” means.',
            code: `var ⟦ang|ang = p.freq * time + p.phase⟧;
var ⟦x1|vx = p.amp * Math.cos(ang)⟧, ⟦y1|vy = p.amp * Math.sin(ang)⟧;`,
            syms: [
                ['A', 'A', 'p.amp', 'radius of arm 1'],
                ['w', 'ω', 'p.freq', 'angular frequency of arm 1'],
                ['ph', 'φ', 'p.phase', 'starting angle of arm 1'],
                ['t', 't', 't', 'time'],
                ['ang', 'ωt + φ', 'ang', 'current angle of arm 1'],
                ['x1', 'Re z₁', 'vx', 'x of arm 1'],
                ['y1', 'Im z₁', 'vy', 'y of arm 1']
            ]
        },
        {
            title: 'Tip to tail: the sum',
            where: 'sumAt() — the accumulation',
            math: '⟦x|x⟧ + i⟦y|y⟧ = z(t) = Σ<sub>k=1</sub><sup>⟦N|N⟧</sup> A<sub>k</sub> e<sup>i(ω<sub>k</sub>t + φ<sub>k</sub>)</sup>, &nbsp; ⟦absz||z|⟧',
            note: 'Mounting an arm on the previous tip is vector addition, so the pen position is the running sum. The partial sums are the joints of the chain you see; only the last one draws.',
            code: `x += vx;
y += vy;
parts.push({ vx: vx, vy: vy, amp: p.amp, color: p.color });`,
            syms: [
                ['N', 'N', 'list.length', 'number of arms'],
                ['x', 'Re z', 'x', 'pen x'],
                ['y', 'Im z', 'y', 'pen y'],
                ['absz', '|z|', 'Math.hypot(x, y)', 'distance of the pen from the centre']
            ]
        },
        {
            title: 'The clock',
            where: 'Sim.clock callback',
            math: '⟦t|t⟧ ← t + ⟦dt|Δt⟧ · ⟦sf|s⟧, &nbsp; s = ⟦spd|speed⟧ · (1 + mid · drive)',
            note: 'Δt is the real time since the last frame, capped at 50 ms so a background tab does not jump. Because z(t) is evaluated in closed form, there is no integration error however large t becomes.',
            code: `⟦sf|lastSpeed = speed.value * speedFactor()⟧;
if (mode === 'live' && dt > 0) {
    ⟦t|t += dt * lastSpeed⟧;`,
            syms: [
                ['dt', 'Δt', 'dt', 'time since the last frame'],
                ['spd', 'speed', 'speed.value', 'slider'],
                ['sf', 's', 'lastSpeed', 'effective speed including Auto Dance'],
                ['t', 't', 't', 'time']
            ]
        },
        {
            title: 'When the curve closes',
            where: 'structure()',
            math: '⟦G|G⟧ = gcd(100ω<sub>1</sub>, …, 100ω<sub>N</sub>), &nbsp; ⟦g|g⟧ = G/100, &nbsp; ⟦Tc|T⟧ = 2π / g',
            note: 'z(t + T) = z(t) needs every ω<sub>k</sub>T to be a multiple of 2π. Sliders move in steps of 0.01 rad/s, so 100ω is an integer and Euclid’s algorithm finds the largest common frequency g exactly.',
            code: `list.forEach(function (p) { if (p.amp > 0) w.push(Math.round(p.freq * 100)); });
var G = 0, M = 0;
w.forEach(function (x) { ⟦G|G = gcd(G, x)⟧; });
...
return { n: w.length, G: G, ⟦g|g: G / 100⟧, M: M, q: q };`,
            syms: [
                ['G', 'G', 'G', 'gcd of 100ω, integer'],
                ['g', 'g', 'G / 100', 'common frequency'],
                ['Tc', 'T', 'TAU / g', 'period of the closed curve']
            ]
        },
        {
            title: 'Rotational symmetry',
            where: 'structure()',
            math: '⟦M|M⟧ = gcd(ω<sub>j</sub> − ω<sub>1</sub>), &nbsp; ω<sub>1</sub>/M = p/q &nbsp;⇒&nbsp; ⟦q|q⟧-fold symmetry',
            note: 'Waiting τ = 2π/M multiplies every term by e<sup>iω<sub>k</sub>τ</sup>; these factors are all equal, so the whole curve turns rigidly by 2π ω<sub>1</sub>/M. Reducing that fraction to p/q gives the order of the rotation group.',
            code: `for (var i = 1; i < w.length; i++) ⟦M|M = gcd(M, w[i] - w[0])⟧;
var ⟦q|q = M ? M / gcd(w[0], M) : 0⟧;`,
            syms: [
                ['M', 'M', 'M', 'gcd of frequency differences, ×100'],
                ['q', 'q', 'q', 'order of the symmetry']
            ]
        },
        {
            title: 'Average size: Parseval',
            where: 'readouts()',
            math: '⟨|z|²⟩<sub>t</sub> = ⟦E|Σ A<sub>k</sub>²⟧, &nbsp; while at this instant ⟦absz2||z(t)|²⟧',
            note: 'Cross terms A<sub>j</sub>A<sub>k</sub> cos((ω<sub>j</sub> − ω<sub>k</sub>)t + …) average to zero over a long time when the frequencies differ, so only the squares survive. The instantaneous |z|² swings around this mean.',
            code: `var e = 0;
phasors.forEach(function (p) { ⟦E|e += p.amp * p.amp⟧; });`,
            syms: [
                ['E', 'Σ A²', 'e', 'time-averaged |z|²'],
                ['absz2', '|z|²', 'x*x + y*y', 'squared distance now']
            ]
        },
        {
            title: 'Final shape and morphing',
            where: 'refinal() and morphStep()',
            math: '⟦n|n⟧ samples over ⟦span|one period⟧; &nbsp; p ← p + ⟦alpha|α⟧ (q − p)',
            note: 'The whole closed curve is sampled at once. When a slider moves, each sample relaxes toward its new target like a first-order low-pass filter: the gap shrinks by (1 − α) every frame. The last row is the largest gap still left.',
            code: `var ⟦n|n = Math.max(1500, Math.min(12000, Math.round(sp / TAU * 700)))⟧;
...
morphPath[i].x += (finalPath[i].x - morphPath[i].x) * ⟦alpha|a⟧;
morphPath[i].y += (finalPath[i].y - morphPath[i].y) * a;`,
            syms: [
                ['n', 'n', 'finalN', 'samples on the final curve'],
                ['span', 'span', 'finalSpan', 'time span drawn'],
                ['alpha', 'α', 'morph.value', 'morph rate per frame'],
                ['dev', 'max |p − q|', '—', 'remaining morph gap (every 7th sample)']
            ]
        },
        {
            title: 'Auto Dance: sound into radii',
            where: 'buildLive()',
            math: '⟦Ar|A′⟧ = ⟦A|A⟧ · ⟦mul|m⟧, &nbsp; m = [1 + ease(⟦bass|bass⟧) · drive · (1 − 0.7|ω|/|ω|<sub>max</sub>)] · ⟦burst|burst⟧',
            note: 'For arms at or below the median |ω|. Faster arms use 1 + high · drive instead. The copy A′ is what gets drawn; the stored A is never changed, so switching Auto Dance off returns the exact original curve.',
            code: `if (danceOn) {
    if (absF[i] <= med) mul = 1 + EASE[p.curve](clamp01(⟦bass|energy.bass⟧)) * dBass.value * (1 - 0.7 * absF[i] / maxAbs);
    else mul = 1 + clamp01(energy.high) * dHigh.value;
    ⟦mul|mul *= burst⟧;
}
return { ⟦Ar|amp: p.amp * mul⟧, freq: p.freq, phase: p.phase, color: p.color, mul: mul };`,
            syms: [
                ['dance', 'on/off', 'danceOn', 'Auto Dance switch'],
                ['bass', 'bass', 'energy.bass', 'smoothed bass level, 0–1'],
                ['burst', 'burst', 'burst', 'beat multiplier, decays to 1'],
                ['mul', 'm', 'l.mul', 'multiplier of arm 1'],
                ['A', 'A', 'p.amp', 'stored radius of arm 1'],
                ['Ar', 'A′', 'live[0].amp', 'drawn radius of arm 1']
            ]
        }
    ]
};
