/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.bench = {
    intro: 'Eight steps from one sine to the sum, the plots and the spectrum. The live column reads Wave 1 and the sum at the centre of the view, X = 400 px; load a preset and watch it change.',
    steps: [
        {
            title: 'One component, and what its sliders mean',
            where: 'y(w, X)',
            math: '⟦y1|y<sub>i</sub>⟧ = ⟦A|A<sub>i</sub>⟧ sin(2π ⟦f|f<sub>i</sub>⟧ (X/200 − ⟦s|s<sub>i</sub>⟧ t) + ⟦phi|φ<sub>i</sub>⟧)<br>⟦k|k<sub>i</sub>⟧ = 2π f<sub>i</sub>/200, &nbsp; ⟦w|ω<sub>i</sub>⟧ = 2π f<sub>i</sub> s<sub>i</sub>, &nbsp; ⟦lam|λ<sub>i</sub>⟧ = 200/f<sub>i</sub>, &nbsp; ⟦v|v<sub>i</sub>⟧ = 200 s<sub>i</sub>',
            note: 'Expanding the argument gives k<sub>i</sub>X − ω<sub>i</sub>t + φ<sub>i</sub>. The Frequency slider counts cycles per 200 px; it equals the temporal frequency in Hz only at Speed 1×. The phase speed ω/k = 200 s<sub>i</sub> px/s depends on the Speed slider alone.',
            code: `function ⟦y1|y(w, X)⟧ { return ⟦A|w.A⟧ * Math.sin(2 * Math.PI * ⟦f|w.f⟧ * (X / 200 - ⟦s|w.s⟧ * simT) + ⟦phi|w.phi⟧); }`,
            syms: [
                ['A', 'A<sub>1</sub>', 'waves[0].A', 'amplitude, px'],
                ['f', 'f<sub>1</sub>', 'waves[0].f', 'cycles per 200 px'],
                ['s', 's<sub>1</sub>', 'waves[0].s', 'speed factor'],
                ['phi', 'φ<sub>1</sub>', 'waves[0].phi', 'phase'],
                ['k', 'k<sub>1</sub>', '2π f / 200', 'rad/px'],
                ['w', 'ω<sub>1</sub>', '2π f s', 'rad/s'],
                ['lam', 'λ<sub>1</sub>', '200 / f', 'px'],
                ['v', 'v<sub>1</sub>', '200 s', 'px/s'],
                ['y1', 'y<sub>1</sub>', 'y(waves[0], 400)', 'Wave 1 at the centre, px']
            ]
        },
        {
            title: 'Sampling the view',
            where: 'draw() — samples and X',
            math: '⟦X|X<sub>j</sub>⟧ = (j / M) · 800 px, &nbsp; j = 0, 1, …, ⟦M|M⟧, &nbsp; M = plot width in screen px',
            note: 'The view always spans 800 world pixels, so a wave with f = 1 shows four wavelengths on a phone and on a monitor. One sample per screen pixel is dense enough: the shortest wave, f = 3, has λ = 67 px of world, still many samples per wavelength on any screen wider than about 200 px.',
            code: `var ⟦M|samples = Math.max(2, Math.round(right - left))⟧;
...
var ⟦X|X = i / samples * WORLD_W⟧, py = mid2 - y(wv, X) / compRange * hComp / 2;`,
            syms: [
                ['M', 'M', 'samples', 'samples across the plot'],
                ['dX', 'ΔX', '800 / samples', 'world px between samples']
            ]
        },
        {
            title: 'Superposition is a plain sum',
            where: 'draw() — the sum loop',
            math: '⟦sum|y(X, t)⟧ = Σ<sub>i</sub> y<sub>i</sub>(X, t), &nbsp; ⟦pk|peak⟧ = max<sub>j</sub> |y(X<sub>j</sub>, t)|',
            note: 'With equal speeds every component solves the same linear wave equation, so the sum is again a solution (see the derivation above). With unequal speeds the sum is still exact arithmetic, but it describes one real medium only if the speeds follow a consistent dispersion relation ω(k). The peak is taken over the sampled points of the current frame, so it can sit a hair below the true maximum between samples.',
            code: `var X = i / samples * WORLD_W, v = 0;
for (var j = 0; j < waves.length; j++) ⟦sum|v += y(waves[j], X)⟧;
⟦pk|pk = Math.max(pk, Math.abs(v))⟧;`,
            syms: [
                ['N', 'N', 'waves.length', 'components'],
                ['sum', 'y(400, t)', 'v at X = 400', 'sum at the centre, px'],
                ['pk', 'peak', 'peak', 'largest |y| this frame, px']
            ]
        },
        {
            title: 'Fitting the curves into their panels',
            where: 'nice() and draw()',
            math: '⟦R|R<sub>sum</sub>⟧ = nice(Σ A<sub>i</sub>), &nbsp; R<sub>comp</sub> = nice(max A<sub>i</sub>)<br>nice(v) = max(20, 10⌈v/10⌉), &nbsp; p<sub>y</sub> = mid − (y / R) · h/2',
            note: 'The upper axis runs from −R to +R with R the sum of amplitudes rounded up to 10 px, which by step 08 is a guaranteed bound, so the sum can never leave its panel. Screen y points down, hence the minus sign.',
            code: `function nice(v) { return Math.max(20, Math.ceil(v / 10) * 10); }
var ⟦R|sumRange = nice(waves.reduce(function (a, v) { return a + v.A; }, 0))⟧;
var compRange = nice(waves.reduce(function (a, v) { return Math.max(a, v.A); }, 0));
...
pts.push(mid1 - v / sumRange * hSum / 2);`,
            syms: [
                ['R', 'R<sub>sum</sub>', 'sumRange', 'upper axis limit, px'],
                ['Rc', 'R<sub>comp</sub>', 'compRange', 'lower axis limit, px']
            ]
        },
        {
            title: 'Beats preset',
            where: 'the Beats button',
            math: 'A sin a + A sin b = 2A cos((a − b)/2) sin((a + b)/2)<br>⟦bl|beat length⟧ = 2π/Δk = 200/|f<sub>1</sub> − f<sub>2</sub>|',
            note: 'With f = 1.00 and 1.25 the envelope repeats every 200/0.25 = 800 px: exactly one beat across the view. With equal speeds the envelope and the carrier both move at 200 px/s; give one wave another speed and the envelope moves at 200(f₁s₁ − f₂s₂)/(f₁ − f₂).',
            code: `document.getElementById('p-beats').addEventListener('click', function () {
    preset([{ A: 18, f: 1 }, { A: 18, f: 1.25 }]);
});`,
            syms: [
                ['bl', 'beat length', '200 / |f₁ − f₂|', 'for Waves 1 and 2, px'],
                ['venv', 'v<sub>env</sub>', '200 (f₁s₁ − f₂s₂)/(f₁ − f₂)', 'envelope speed, px/s']
            ]
        },
        {
            title: 'Square-wave preset',
            where: 'the Square wave button',
            math: 'sq(x) = (4/π) Σ<sub>n odd</sub> sin(nx)/n<br>⟦An|A<sub>n</sub>⟧ = 30/n, &nbsp; f<sub>n</sub> = 0.4 n, &nbsp; n = 1, 3, 5, 7 &nbsp;⇒&nbsp; height ≈ (π/4) · 30 ≈ 23.6 px',
            note: 'Only odd harmonics, with amplitudes falling as 1/n. Rounding 30/n to 0.1 px (30/7 = 4.2857 → 4.3) changes the shape by less than a pixel. Four terms already show the flat tops and the Gibbs overshoot near the jumps.',
            code: `preset([1, 3, 5, 7].map(function (n) {
    return { ⟦An|A: Math.round(30 / n * 10) / 10⟧, f: 0.4 * n };
}));`,
            syms: [
                ['An', 'A<sub>n</sub>', 'waves[i].A', 'amplitudes now loaded'],
                ['fn', 'f<sub>n</sub>', 'waves[i].f', 'frequencies now loaded']
            ]
        },
        {
            title: 'The spectrum',
            where: 'lines() and drawSpectrum()',
            math: '⟦hl|ν<sub>i</sub>⟧ = f<sub>i</sub> s<sub>i</sub>, &nbsp; C = Σ<sub>same ν</sub> A<sub>i</sub> e<sup>iφ<sub>i</sub></sup>, &nbsp; stem height ∝ |C|<br>x<sub>line</sub> = left + (ν / 6 Hz) · (right − left)',
            note: 'At a fixed point x = 0 each component oscillates as A sin(φ − 2πνt), so the frequency you would hear is ν = f·s, not f alone. Components with the same ν add as phasors: in phase they give 2A, in antiphase nothing, and the stem shows exactly that.',
            code: `var ⟦hl|nu = Math.round(wv.f * wv.s * 1e6) / 1e6⟧, g = groups[nu];
g.re += wv.A * Math.cos(wv.phi);
g.im += wv.A * Math.sin(wv.phi);
...
return { nu: g.nu, A: g.nu === 0 ? Math.abs(g.im) : Math.hypot(g.re, g.im), ... };
...
var X = function (nu) { return left + nu / NUMAX * (right - left); };`,
            syms: [
                ['hl', 'ν<sub>1</sub>', 'wv.f * wv.s', 'Wave 1 temporal frequency'],
                ['fmax', 'ν<sub>max</sub>', 'NUMAX', 'right edge of the axis']
            ]
        },
        {
            title: 'A bound that always holds',
            where: 'the readouts',
            math: '|Σ y<sub>i</sub>| ≤ Σ |y<sub>i</sub>| ≤ ⟦sA|Σ A<sub>i</sub>⟧',
            note: 'The triangle inequality: the peak can reach the sum of amplitudes only where every component is at a crest at once. Compare the two readouts under the plot: the sampled peak is always the smaller one.',
            code: `document.getElementById('r-sum').textContent = ⟦sA|waves.reduce(function (a, v) { return a + v.A; }, 0)⟧.toFixed(1) + ' px';
document.getElementById('r-peak').textContent = ⟦pk|peak⟧.toFixed(1) + ' px';`,
            syms: [
                ['sA', 'Σ A<sub>i</sub>', 'sum of amplitudes', 'px'],
                ['pk', 'peak', 'peak', 'px'],
                ['ratio', 'peak / Σ A', '', '≤ 1 always']
            ]
        }
    ]
};
