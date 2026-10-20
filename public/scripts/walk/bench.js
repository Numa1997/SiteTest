/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.bench = {
    intro: 'Thirteen steps through the lecture note above, in its order: the state of the bench, the equations (1) to (11), (17) and (19) beside the lines that evaluate them, and then how the page computes and draws (Sections 7 and 8). Equations (12) to (16) and (18) are proofs about the sum; no line of code evaluates them. The Now column reads the store: Wave 1 and the sum at the centre of the view, X = 400 px. Load a preset and watch it change.',
    steps: [
        {
            title: 'The state: four numbers per wave',
            where: 'add(p) and render() — the wave list, its defaults and its sliders; the last lines of the script — the start',
            math: 'wave i = 1, …, ⟦N|N⟧, &nbsp; N ≤ 6: &nbsp; (⟦A|A<sub>i</sub>⟧, ⟦f|f<sub>i</sub>⟧, ⟦phi|φ<sub>i</sub>⟧, ⟦s|s<sub>i</sub>⟧)<br>at the start: N = 1, &nbsp; A<sub>1</sub> = 20 px, &nbsp; f<sub>1</sub> = 1, &nbsp; φ<sub>1</sub> = 0, &nbsp; s<sub>1</sub> = 1 &nbsp; (Section 2)',
            note: 'A wave on the bench is nothing but four numbers, and the list <code>waves</code> holds one object per wave card. The first line refuses a seventh wave (<code>MAX_WAVES</code> is 6). <code>waves.push</code> adds a new wave, and the four lines inside give each slider its default: <code>A</code> is the Amplitude A<sub>i</sub> = 20 px, <code>f</code> the Frequency f<sub>i</sub> = 1, <code>phi</code> the Phase φ<sub>i</sub> = 0 rad and <code>s</code> the Speed factor s<sub>i</sub> = 1, the last two plain numbers. The four <code>field</code> lines build the sliders on the card and fix their ranges: A<sub>i</sub> from 0 to 40 px in whole pixels, f<sub>i</sub> from 0.1 to 3 (<code>FMAX</code>) in steps of 0.05, φ<sub>i</sub> from 0 to 6.28 rad in steps of 0.05 rad, s<sub>i</sub> from 0 to 2 in steps of 0.05. The <code>Sim.slider</code> line writes the slider’s number into <code>w.A</code> each time you drag it; the three lines after it do the same for <code>w.f</code>, <code>w.phi</code> and <code>w.s</code>, and the Phase card shows φ<sub>i</sub>/π. Apart from the clock time t (step 10) nothing else is state: no velocities, no history, nothing to integrate. The last line puts one wave on the bench when the page opens; the presets of steps 6 and 7 replace the whole list.',
            code: `if (waves.length >= MAX_WAVES) return;
...
waves.push({
...
⟦A|A: p.A !== undefined ? p.A : 20⟧,
⟦f|f: p.f !== undefined ? p.f : 1⟧,
⟦phi|phi: p.phi !== undefined ? p.phi : 0⟧,
⟦s|s: p.s !== undefined ? p.s : 1⟧
});
...
field({ id: key + 'A', name: 'Amplitude', min: 0, max: 40, step: 1, value: w.A }) +
field({ id: key + 'f', name: 'Frequency', min: 0.1, max: FMAX, step: 0.05, value: w.f }) +
field({ id: key + 'p', name: 'Phase', min: 0, max: 6.28, step: 0.05, value: w.phi }) +
field({ id: key + 's', name: 'Speed', min: 0, max: 2, step: 0.05, value: w.s }) +
...
Sim.slider(key + 'A', { format: function (v) { return v + ' px'; }, onInput: function (v) { ⟦A|w.A = v⟧; } });
...
add({ A: 20, f: 1 });`,
            syms: [
                ['N', 'N', 'waves.length', 'waves on the bench, at most 6'],
                ['A', 'A<sub>1</sub>', 'waves[0].A', 'amplitude of Wave 1, px'],
                ['f', 'f<sub>1</sub>', 'waves[0].f', 'Frequency slider of Wave 1: wavelengths per 200 px'],
                ['phi', 'φ<sub>1</sub>', 'waves[0].phi', 'phase of Wave 1, shown in units of π rad'],
                ['s', 's<sub>1</sub>', 'waves[0].s', 'Speed factor of Wave 1, a plain number']
            ]
        },
        {
            title: 'One wave: equation (1)',
            where: 'y(w, X); draw() — each wave at the centre of the view',
            math: '⟦y1|y<sub>i</sub>(X, t)⟧ = ⟦A|A<sub>i</sub>⟧ sin(2π ⟦f|f<sub>i</sub>⟧ (X/200 − ⟦s|s<sub>i</sub>⟧ ⟦t|t⟧) + ⟦phi|φ<sub>i</sub>⟧) &nbsp; (1)',
            note: 'The function <code>y</code> is equation (1) letter for letter. Its argument <code>w</code> is one wave object of step 1, so <code>w.A</code> is A<sub>i</sub> in px, <code>w.f</code> is f<sub>i</sub>, <code>w.s</code> is s<sub>i</sub> and <code>w.phi</code> is φ<sub>i</sub> in rad. <code>X</code> is the position in px from the left edge of the 800 px view, and <code>simT</code> is the time t in s, advanced by the clock (step 10). Dividing X by 200 measures the position in the units in which f<sub>i</sub> counts wavelengths, one unit being 200 px. The page calls this one function for every point of every curve, so each curve you see is (1) evaluated, not an approximation of it. The second line, in <code>draw()</code>, evaluates it once per wave at the centre of the view, X = 400 px, and stores the result in <code>y4</code>; the Now column shows the entry of Wave 1.',
            code: `function ⟦y1|y(w, X)⟧ { return ⟦A|w.A⟧ * Math.sin(2 * Math.PI * ⟦f|w.f⟧ * (X / 200 - ⟦s|w.s⟧ * ⟦t|simT⟧) + ⟦phi|w.phi⟧); }
...
⟦y1|y4[wi] = y(wv0, 400)⟧; s400 += y4[wi];`,
            syms: [
                ['A', 'A<sub>1</sub>', 'waves[0].A', 'amplitude, px'],
                ['f', 'f<sub>1</sub>', 'waves[0].f', 'wavelengths per 200 px'],
                ['s', 's<sub>1</sub>', 'waves[0].s', 'speed factor'],
                ['phi', 'φ<sub>1</sub>', 'waves[0].phi', 'phase, in units of π rad'],
                ['y1', 'y<sub>1</sub>(400, t)', 'y4[0]', 'Wave 1 at X = 400 px now, px']
            ]
        },
        {
            title: 'Wavenumber, frequency and speed: equation (2)',
            where: 'draw() — the loop over the waves',
            math: '⟦k|k<sub>i</sub>⟧ = 2π f<sub>i</sub>/200 rad/px, &nbsp; ⟦lam|λ<sub>i</sub>⟧ = 2π/k<sub>i</sub> = 200/f<sub>i</sub> px<br>⟦w|ω<sub>i</sub>⟧ = 2π f<sub>i</sub> s<sub>i</sub> rad/s, &nbsp; ⟦hl|ν<sub>i</sub>⟧ = ω<sub>i</sub>/2π = f<sub>i</sub> s<sub>i</sub> Hz<br>⟦v|v<sub>i</sub>⟧ = ω<sub>i</sub>/k<sub>i</sub> = 200 s<sub>i</sub> px/s &nbsp; (2)',
            note: 'The loop runs once per wave in every frame. <code>wv0</code> is wave i of step 1 and <code>wi</code> its index counted from 0, so Wave 1 is <code>wi = 0</code>. Each assignment on the last line is one entry of (2), written into the store where it is computed: <code>kw</code> is the wavenumber k<sub>i</sub> in rad per px of the medium, <code>omw</code> the angular frequency ω<sub>i</sub> in rad/s, <code>lamw</code> the wavelength λ<sub>i</sub> in px, <code>vw</code> the phase speed v<sub>i</sub> in px/s, and <code>nuw</code> the frequency ν<sub>i</sub> in Hz, the number of crests passing a fixed point each second. Only ν<sub>i</sub> is rounded, to 10<sup>−6</sup> Hz, so that two waves meant to share a frequency compare as exactly equal when the spectrum groups them (step 8). Three facts of the note can be read off this line: λ<sub>i</sub> uses f alone, so the 800 px view holds 4f<sub>i</sub> wavelengths; v<sub>i</sub> uses s alone, so the Frequency slider never changes the speed; and ν<sub>i</sub> equals the Frequency slider’s number only at Speed 1. None of these values feeds the curves, since <code>y</code> of step 2 works from f and s directly; they are kept for the Data panel and the Now column.',
            code: `for (wi = 0; wi < NW; wi++) {
wv0 = waves[wi];
...
⟦k|kw[wi] = 2 * Math.PI * wv0.f / 200⟧; ⟦w|omw[wi] = 2 * Math.PI * wv0.f * wv0.s⟧; ⟦lam|lamw[wi] = 200 / wv0.f⟧; ⟦v|vw[wi] = 200 * wv0.s⟧; ⟦hl|nuw[wi] = Math.round(wv0.f * wv0.s * 1e6) / 1e6⟧;`,
            syms: [
                ['k', 'k<sub>1</sub>', 'kw[0]', 'wavenumber of Wave 1, rad/px'],
                ['lam', 'λ<sub>1</sub>', 'lamw[0]', 'wavelength, px'],
                ['w', 'ω<sub>1</sub>', 'omw[0]', 'angular frequency, rad/s'],
                ['hl', 'ν<sub>1</sub>', 'nuw[0]', 'frequency at a fixed point, Hz'],
                ['v', 'v<sub>1</sub>', 'vw[0]', 'phase speed, px/s']
            ]
        },
        {
            title: 'Waves simply add: equations (3) and (4)',
            where: 'draw() — the value at the centre and the sum loop',
            math: '∂<sup>2</sup>y<sub>i</sub>/∂t<sup>2</sup> = v<sub>i</sub><sup>2</sup> ∂<sup>2</sup>y<sub>i</sub>/∂X<sup>2</sup> &nbsp; (3)<br>ℒ(a y<sub>1</sub> + b y<sub>2</sub>) = a ℒy<sub>1</sub> + b ℒy<sub>2</sub> = 0, &nbsp; ℒ = ∂<sub>t</sub><sup>2</sup> − v<sup>2</sup> ∂<sub>X</sub><sup>2</sup> &nbsp; (4)<br>⟦sum|y(X, t)⟧ = Σ<sub>i</sub> y<sub>i</sub>(X, t)',
            note: 'The page never solves (3); it is the reason the page may add. Each wave of (1) satisfies its own wave equation (3) with v<sub>i</sub> = 200 s<sub>i</sub> px/s, and when all Speeds are equal the operator ℒ is the same for every wave, so by (4) any sum of solutions is again a solution. The code does exactly that sum. In the first line, <code>s400</code> collects every wave’s value at the centre of the view, X = 400 px, and becomes the Now value of y(400, t). In the sum loop, the counter <code>i</code> runs over the samples, the note’s j (step 11), and <code>X</code> is the sample’s position in px. The inner counter <code>j</code> runs over the waves, the note’s i: <code>v</code> starts at 0 and collects <code>y(waves[j], X)</code> from every wave, so after the inner loop <code>v</code> is y(X, t) in px at that sample, and <code>Ys[i]</code> stores it. Mind the swapped letters: in the code i counts samples and j waves, in the note the other way round. With unequal Speeds nothing in the code changes; the sum is still exact arithmetic, but it then imitates a dispersive medium, in which each wave obeys its own (3).',
            code: `y4[wi] = y(wv0, 400); ⟦sum|s400 += y4[wi]⟧;
...
var pts = [], pk = 0;
for (var i = 0; i <= samples; i++) {
var X = i / samples * WORLD_W, v = 0;
for (var j = 0; j < ⟦N|waves.length⟧; j++) ⟦sum|v += y(waves[j], X)⟧;
...
Xs[i] = X; Ys[i] = v; PYs[i] = pts[i];`,
            syms: [
                ['N', 'N', 'waves.length', 'waves added at every sample'],
                ['y1', 'y<sub>1</sub>(400, t)', 'y4[0]', 'Wave 1 at the centre, px'],
                ['sum', 'y(400, t)', 's400', 'sum of all waves at X = 400 px, px']
            ]
        },
        {
            title: 'Two waves of one frequency: phasors, equations (5) and (6)',
            where: 'lines() — the phasor sum of the waves that share a frequency',
            math: 'C e<sup>iψ</sup> = ⟦A|A<sub>1</sub>⟧ e<sup>i⟦phi|φ<sub>1</sub>⟧</sup> + A<sub>2</sub> e<sup>iφ<sub>2</sub></sup> &nbsp; (5)<br>C<sup>2</sup> = A<sub>1</sub><sup>2</sup> + A<sub>2</sub><sup>2</sup> + 2A<sub>1</sub>A<sub>2</sub> cos(φ<sub>1</sub> − φ<sub>2</sub>) &nbsp; (6)',
            note: 'The curves never use (5): the sum curve of step 4 adds the sines point by point and gets the same answer the long way. The page uses (5) in one place, the spectrum. For every wave in a group of equal frequency, <code>g.re</code> collects A<sub>i</sub> cos φ<sub>i</sub> and <code>g.im</code> collects A<sub>i</sub> sin φ<sub>i</sub>, the real and imaginary parts of the arrow A<sub>i</sub>e<sup>iφ<sub>i</sub></sup> in px. After the loop the pair (<code>g.re</code>, <code>g.im</code>) is the tip of the tip-to-tail chain of Figure 2, that is C e<sup>iψ</sup>. On the last line, <code>Math.hypot(g.re, g.im)</code> is the length of that arrow, √(re² + im²), which is C in px; written out for two waves it is (6). In step, φ<sub>1</sub> = φ<sub>2</sub>, it gives A<sub>1</sub> + A<sub>2</sub>; half a turn apart, |A<sub>1</sub> − A<sub>2</sub>|. The angle ψ is never computed, because a stem shows only a length. You can watch (6) at work: press One wave, then Add wave +, and drag the Phase of Wave 2 to 1.00 π. The nearest slider step, 3.15 rad, misses π by 0.0084 rad, the stem falls to 0.17 px by (6), and the Peak |y| on screen readout, shown here as the peak, falls from 40.0 px to 0.2 px.',
            code: `g.re += ⟦A|wv.A⟧ * Math.cos(⟦phi|wv.phi⟧);
g.im += wv.A * Math.sin(wv.phi);
...
return { nu: g.nu, A: g.nu === 0 ? Math.abs(g.im) : Math.hypot(g.re, g.im), colour: g.n > 1 ? T.ink : g.colour };`,
            syms: [
                ['A', 'A<sub>1</sub>', 'waves[0].A', 'length of the first arrow, px'],
                ['phi', 'φ<sub>1</sub>', 'waves[0].phi', 'its angle, in units of π rad'],
                ['An', 'A<sub>i</sub>', 'waves[i].A', 'all amplitudes now loaded, px'],
                ['pk', 'peak', 'peak', 'Peak |y| on screen, px; close to C when all waves share one frequency and one speed']
            ]
        },
        {
            title: 'Beats: equations (7), (8) and (9)',
            where: 'draw() — beat length and envelope speed of Waves 1 and 2; the Beats button',
            math: 'A sin a + A sin b = 2A cos((a − b)/2) · sin((a + b)/2) &nbsp; (7)<br>⟦bl|λ<sub>beat</sub>⟧ = 2π/|Δk| = 200/|f<sub>1</sub> − f<sub>2</sub>| px, &nbsp; T<sub>beat</sub> = 1/|ν<sub>1</sub> − ν<sub>2</sub>| &nbsp; (8)<br>⟦venv|v<sub>env</sub>⟧ = Δω/Δk = 200 (f<sub>1</sub>s<sub>1</sub> − f<sub>2</sub>s<sub>2</sub>)/(f<sub>1</sub> − f<sub>2</sub>) px/s &nbsp; (9)',
            note: 'The identity (7) is not in the code: the upper panel shows the envelope because it is already contained in the plain sum of step 4. The code writes down two numbers that follow from it, for Waves 1 and 2 only. <code>waves[0]</code> and <code>waves[1]</code> are Waves 1 and 2, so <code>waves[0].f</code> is f<sub>1</sub> and <code>waves[1].s</code> is s<sub>2</sub>. The first line is (8): with Δk = k<sub>1</sub> − k<sub>2</sub> = 2π(f<sub>1</sub> − f<sub>2</sub>)/200 rad/px from (2), 2π/|Δk| is 200/|f<sub>1</sub> − f<sub>2</sub>| in px, and <code>Math.abs</code> supplies the absolute value, so λ<sub>beat</sub> is positive whichever wave is higher. The second line is the first row of (9) with Δω/Δk worked out, in px/s; its sign is the envelope’s direction, positive to the right. Both are stored as <code>NaN</code>, and the Now column says so, when there are fewer than two waves or f<sub>1</sub> = f<sub>2</sub>, where there is no beat. The page computes neither T<sub>beat</sub> nor the carrier speed of the second row of (9). The Beats button loads two waves of Amplitude 18 px with Frequencies 1.00 and 1.25 and the default Phase 0 and Speed 1, so λ<sub>beat</sub> = 200/0.25 = 800 px, exactly the width of the view, and v<sub>env</sub> = 200 px/s, the speed of both waves. Exercise 4.1 runs on the second line: with Wave 2 at Speed 0.50 it gives 200 (1 − 0.625)/(−0.25) = −300 px/s, an envelope running to the left.',
            code: `ds.set('bl', NW > 1 && waves[0].f !== waves[1].f ? ⟦bl|200 / Math.abs(waves[0].f - waves[1].f)⟧ : NaN);
ds.set('venv', NW > 1 && waves[0].f !== waves[1].f ? ⟦venv|200 * (waves[0].f * waves[0].s - waves[1].f * waves[1].s) / (waves[0].f - waves[1].f)⟧ : NaN);
...
document.getElementById('p-beats').addEventListener('click', function () { preset([{ A: 18, f: 1 }, { A: 18, f: 1.25 }]); });`,
            syms: [
                ['fn', 'f<sub>i</sub>', 'waves[i].f', 'Frequencies now loaded'],
                ['bl', 'λ<sub>beat</sub>', '200 / |f₁ − f₂|', 'beat length of Waves 1 and 2, px'],
                ['venv', 'v<sub>env</sub>', '200 (f₁s₁ − f₂s₂)/(f₁ − f₂)', 'envelope speed of Waves 1 and 2, px/s; negative means to the left'],
                ['v', 'v<sub>1</sub>', '200 * waves[0].s', 'phase speed of Wave 1, px/s, for comparison']
            ]
        },
        {
            title: 'A square wave from four sines: equations (10) and (11)',
            where: 'the Square wave button',
            math: 'sq(x) = (4/π) (sin x + sin 3x/3 + sin 5x/5 + sin 7x/7 + …) &nbsp; (10)<br>Σ<sub>n = 1, 3, 5, 7</sub> (30 px/n) sin nx ≈ H sq(x), &nbsp; H = (π/4) × 30 px = 23.56 px &nbsp; (11)<br>⟦An|A<sub>n</sub>⟧ = 30/n px, &nbsp; ⟦fn|f<sub>n</sub>⟧ = 0.4 n, &nbsp; x = 2π × 0.4 (X/200 − t)',
            note: 'The button builds the first four odd terms of (10) as four waves. For each n of 1, 3, 5 and 7, <code>A</code> is 30/n px rounded to 0.1 px, which gives 30, 10, 6 and 4.3 px (30/7 = 4.29), and <code>f</code> is 2n/5 = 0.4 n, which gives 0.4, 1.2, 2.0 and 2.8. Phase and Speed keep their defaults, 0 and 1. With x = 2π × 0.4 (X/200 − t), wave n of (1) is (30 px/n) sin nx, the nth term of (10) multiplied by 30 px = 4H/π, so the sum of step 4 is H sq(x) up to the missing terms. The list stops at n = 7 because n = 9 would need a Frequency of 3.6, above the slider’s top value of 3 (<code>FMAX</code>). The derivations (12) to (16), which explain the amplitudes 4/(nπ) and the overshoot of 8.95 % at the jumps, have no line of code; the page only adds the four sines. One detail can puzzle: the Amplitude slider moves in whole pixels, so the card of Wave 4 shows 4 px, while <code>w.A</code>, the sum and the store keep 4.3 px.',
            code: `document.getElementById('p-square').addEventListener('click', function () {
preset([1, 3, 5, 7].map(function (n) { return { ⟦An|A: Math.round(30 / n * 10) / 10⟧, ⟦fn|f: n * 2 / 5⟧ }; }));
});`,
            syms: [
                ['An', 'A<sub>n</sub>', 'waves[i].A', 'amplitudes now loaded, px'],
                ['fn', 'f<sub>n</sub>', 'waves[i].f', 'Frequencies now loaded'],
                ['N', 'N', 'waves.length', 'terms of (10) on the bench']
            ]
        },
        {
            title: 'The spectrum: equation (17)',
            where: 'lines() — one stem per distinct frequency',
            math: '⟦hl|ν<sub>i</sub>⟧ = f<sub>i</sub> s<sub>i</sub>, &nbsp; C<sub>ν</sub> = | Σ<sub>i: ν<sub>i</sub> = ν</sub> A<sub>i</sub> e<sup>iφ<sub>i</sub></sup> | &nbsp; (17)<br>for ν = 0: &nbsp; C<sub>0</sub> = | Σ A<sub>i</sub> sin φ<sub>i</sub> |',
            note: 'At the left edge of the view, X = 0, wave i arrives as A<sub>i</sub> sin(φ<sub>i</sub> − 2πν<sub>i</sub>t), so the spectrum is built from the slider values alone; the curves are never measured. <code>lines()</code> walks through the waves. <code>nu</code> is ν<sub>i</sub> = f<sub>i</sub>s<sub>i</sub> in Hz, rounded to 10<sup>−6</sup> Hz as in step 3, and <code>groups[nu]</code> looks up the group of waves already found at that frequency. If there is none, the second line opens one with an empty arrow (<code>re</code> = <code>im</code> = 0) and the colour of its first wave, and appends it to the list <code>out</code>, so the stems come in order of first appearance. Each wave then adds its arrow to its group, as in step 5, and <code>g.n</code> counts the waves in the group. The return line turns each group into a stem whose height <code>A</code> is C<sub>ν</sub> of (17) in px, the length of the summed arrow; a stem shared by several waves is drawn in ink, a single wave’s stem in that wave’s colour. The case ν = 0 is separate: a wave with Speed 0 does not oscillate but lifts the point X = 0 by the constant A<sub>i</sub> sin φ<sub>i</sub>, so its stem is |Σ A<sub>i</sub> sin φ<sub>i</sub>| = |<code>g.im</code>|. Parseval’s theorem (18) follows from these heights; the page does not compute it.',
            code: `var groups = {}, out = [];
waves.forEach(function (wv) {
var ⟦hl|nu = Math.round(wv.f * wv.s * 1e6) / 1e6⟧, g = groups[nu];
if (!g) { g = groups[nu] = { nu: nu, re: 0, im: 0, n: 0, colour: wv.colour }; out.push(g); }
...
g.n++;
...
return { nu: g.nu, A: g.nu === 0 ? Math.abs(g.im) : Math.hypot(g.re, g.im), colour: g.n > 1 ? T.ink : g.colour };`,
            syms: [
                ['hl', 'ν<sub>1</sub>', 'wv.f * wv.s', 'frequency of Wave 1 at a fixed point, Hz'],
                ['fn', 'f<sub>i</sub>', 'waves[i].f', 'Frequencies now loaded'],
                ['An', 'A<sub>i</sub>', 'waves[i].A', 'amplitudes now loaded, px; a lone wave’s stem has this height']
            ]
        },
        {
            title: 'A ceiling that always holds: equation (19)',
            where: 'draw() — Σ A, the peak and their ratio; the clock callback — the two readouts',
            math: '| Σ<sub>i</sub> y<sub>i</sub> | ≤ Σ<sub>i</sub> |y<sub>i</sub>| ≤ ⟦sA|Σ<sub>i</sub> A<sub>i</sub>⟧ &nbsp; (19)<br>⟦pk|peak⟧ = max<sub>j</sub> |y(X<sub>j</sub>, t)|, &nbsp; ⟦ratio|peak / Σ A<sub>i</sub>⟧ ≤ 1',
            note: 'No sine exceeds its amplitude, so the sum of the waves can never exceed the sum of their amplitudes; that is (19), the triangle inequality. The first line adds the Amplitudes, <code>v.A</code> for each wave <code>v</code>, into <code>sum_A</code>, which is Σ A<sub>i</sub> in px. In the sum loop of step 4, <code>pk</code> keeps the largest |y| met so far among the samples, and after the loop <code>peak</code> holds it: the largest displacement in px on the screen in this frame. The next line stores it with its ratio to the ceiling, a plain number. By (19) the ratio is never above 1, and it comes to 1 only where all crests coincide: with One wave both readouts show 20.0 px, while the stored peak is a few thousandths of a pixel lower, because the samples miss the exact crest. In the Square wave preset the crests never coincide, since sin 3x = −1 wherever sin x = 1, and the ratio stays near 27.9/50.3 = 0.55. The last block rewrites the two readouts under the plot, Sum of amplitudes and Peak |y| on screen, on every eighth frame only, 7.5 times a second at 60 frames a second, so that you can read them; the store itself is updated every frame. The same ceiling, rounded up to 10 px, sets the height of the sum panel (step 12), which is why the sum curve never leaves it.',
            code: `... ⟦sA|ds.set('sum_A', waves.reduce(function (a, v) { return a + v.A; }, 0))⟧;
...
⟦pk|pk = Math.max(pk, Math.abs(v))⟧;
...
⟦pk|peak = pk⟧;
...
ds.set('peak', peak); ⟦ratio|ds.set('ratio', ds.get('sum_A') > 0 ? peak / ds.get('sum_A') : NaN)⟧;
...
if ((frames - 1) % 8 === 0) {
document.getElementById('r-sum').textContent = ⟦sA|ds.get('sum_A')⟧.toFixed(1) + ' px';
document.getElementById('r-peak').textContent = ⟦pk|peak⟧.toFixed(1) + ' px';
}`,
            syms: [
                ['sA', 'Σ A<sub>i</sub>', 'sum_A', 'the ceiling, Sum of amplitudes, px'],
                ['pk', 'peak', 'peak', 'largest |y| among the samples of this frame, px'],
                ['ratio', 'peak / Σ A<sub>i</sub>', 'ratio', 'never above 1']
            ]
        },
        {
            title: 'The clock: t in equation (1)',
            where: 'the Sim.clock callback — once per frame',
            math: '⟦t|t⟧ ← t + ⟦dt|Δt⟧, &nbsp; Δt ≤ 0.05 s<br>then (1) at the new t, for every sample of every wave',
            note: 'There is no differential equation to step forward: (1) gives every wave at every place and time directly, so the page only has to know t. <code>Sim.clock</code> calls this function once per display frame with <code>dt</code>, the real time Δt since the previous frame in s, and <code>simT += dt</code> advances t, the time used inside <code>y</code> of step 2. The cap Δt ≤ 0.05 s sits in the shared script <code>sim.js</code>, not in this page: when the browser draws fewer than 20 frames a second, the motion slows down rather than jumping. While paused, <code>dt</code> is 0 and t stands still, but the frame is still redrawn, so dragging a slider still changes the picture. The store line keeps t and Δt for the Data panel, where you can read them. Then <code>draw()</code> evaluates (1) at every sample (steps 4 and 11) and <code>drawSpectrum()</code> redraws the stems. Because t enters only through (1), the waves move at their stated speeds on any screen and at any frame rate. In the Now column, y<sub>1</sub>(400, t) and y(400, t) change only because t grows; press Pause and they stop.',
            code: `var clk = Sim.clock(function (⟦dt|dt⟧) {
⟦t|simT += dt⟧;
...
ds.set('t', simT); ds.set('dt', dt); ...
draw();
drawSpectrum();`,
            syms: [
                ['y1', 'y<sub>1</sub>(400, t)', 'y4[0]', 'Wave 1 at the centre, px; moves only because t grows'],
                ['sum', 'y(400, t)', 's400', 'the sum at the centre, px']
            ]
        },
        {
            title: 'Sampling the view: one point per screen pixel',
            where: 'draw() — the plot width, the samples and the component loop',
            math: '⟦X|X<sub>j</sub>⟧ = 800 j/⟦M|M⟧ px, &nbsp; j = 0, 1, …, M, &nbsp; M = (plot width in screen px) − 58<br>⟦dX|ΔX⟧ = 800/M px, &nbsp; chord error ≈ A k<sup>2</sup> ΔX<sup>2</sup>/8',
            note: '<code>box.w</code> is the width of the plot on your screen in CSS pixels. The plot keeps 44 px on the left for the tick labels and 14 px on the right, so <code>right - left</code> is the plot width minus 58, and <code>samples</code>, the note’s M, is that number rounded, never below 2. The view always shows <code>WORLD_W</code> = 800 px of the medium, so sample i sits at X = 800 i/M px and the spacing is ΔX = 800/M px, stored as <code>dX</code>. The code calls the sample counter i; the note calls it j. The two lines of the component loop evaluate (1) at each sample for each wave: <code>py</code> is the screen height of the point (step 12), and the second line stores y<sub>i</sub>(X) and that height. <code>y</code> is called twice there and once more in the sum loop of step 4, so a frame costs 3N(M + 1) sines: 8 556 for the Square wave preset at M = 712, which a 1440 × 900 window gives. Each value is exact to double precision, about 16 significant digits. The only approximation is in the drawing, a chain of straight segments between samples, which cuts under a crest by about A k² ΔX²/8: for the shortest wave (Frequency 3, λ = 66.7 px) at the full 40 px, 0.06 px in that window and 0.32 px on a phone 390 px wide, where M = 298.',
            code: `var w = box.w, h = box.h, left = 44, right = w - 14, top1 = 30, gap = 44;
...
var ⟦M|samples = Math.max(2, Math.round(right - left))⟧;
...
ds.set('M', samples); ⟦dX|ds.set('dX', WORLD_W / samples)⟧; ...
...
var ⟦X|X = i / samples * WORLD_W⟧, py = mid2 - y(wv, X) / compRange * hComp / 2;
Yc[wi * MP + i] = y(wv, X); PYc[wi * MP + i] = py;`,
            syms: [
                ['M', 'M', 'samples', 'sample steps across the plot, one per screen pixel'],
                ['dX', 'ΔX', 'WORLD_W / samples', 'medium between two samples, px'],
                ['N', 'N', 'waves.length', 'waves evaluated at each sample']
            ]
        },
        {
            title: 'From the medium to the screen: equation (20)',
            where: 'nice(), draw() and panel() — the two panels of the plot',
            math: '⟦R|R⟧ = max(20, 10⌈Σ A<sub>i</sub>/10⌉) px, &nbsp; ⟦Rc|R<sub>c</sub>⟧ = max(20, 10⌈max A<sub>i</sub>/10⌉) px<br>y<sub>screen</sub> = y<sub>mid</sub> − (y/R) · h/2 &nbsp; (20)<br>sample j in screen column 44 + j',
            note: 'Each panel has its own vertical range. <code>nice</code> rounds a length up to the next 10 px and never returns less than 20 px. <code>sumRange</code> is R, the ceiling Σ A<sub>i</sub> of (19) rounded up, so the sum can never leave its panel; <code>compRange</code> is R<sub>c</sub>, from the largest single amplitude. <code>hSum</code> and <code>hComp</code> are the panel heights h in screen pixels: the sum panel gets 56 % of the height left after the margins of 30, 44 and 14 px, the component panel the rest. <code>panel()</code> draws the grid and returns each panel’s axis, <code>mid1</code> and <code>mid2</code>, the y<sub>mid</sub> of (20). The <code>py</code> line and the <code>pts.push</code> line are (20) for a component and for the sum: the displacement in px of the medium, divided by its range, times half the panel height, counted from the axis. Screen y grows downwards, hence the minus sign. Horizontally, sample i is drawn in screen column <code>left + i</code> = 44 + i, so the 800 px of the medium fill the plot width. The two directions have different scales. In the Square wave preset at 1440 × 900, R = 60 px over h = 220.1 screen pixels draws 1 px of displacement 1.83 pixels tall, while 1 px along the medium is 0.89 pixels wide, so the curves look about twice as steep as they are.',
            code: `function nice(v) { return Math.max(20, Math.ceil(v / 10) * 10); }
...
var hSum = (h - top1 - gap - 14) * 0.56, top2 = top1 + hSum + gap, hComp = h - top2 - 14;
...
var ⟦R|sumRange = nice(waves.reduce(function (a, v) { return a + v.A; }, 0))⟧;
var ⟦Rc|compRange = nice(waves.reduce(function (a, v) { return Math.max(a, v.A); }, 0))⟧;
...
var mid1 = panel(top1, hSum, ⟦R|sumRange⟧, 'SUM', left, right, 'y = Σ y_{i}');
var mid2 = panel(top2, hComp, ⟦Rc|compRange⟧, 'COMPONENTS', left, right, 'y_{i}');
...
var X = i / samples * WORLD_W, py = mid2 - y(wv, X) / ⟦Rc|compRange⟧ * hComp / 2;
...
if (i === 0) ctx.moveTo(left + i, py); else ctx.lineTo(left + i, py);
...
pts.push(mid1 - v / ⟦R|sumRange⟧ * hSum / 2);`,
            syms: [
                ['R', 'R', 'sumRange', 'range of the sum panel, px'],
                ['Rc', 'R<sub>c</sub>', 'compRange', 'range of the component panel, px'],
                ['sA', 'Σ A<sub>i</sub>', 'sum_A', 'the ceiling that R rounds up, px']
            ]
        },
        {
            title: 'The spectrum on screen',
            where: 'drawSpectrum() — stem positions and heights',
            math: 'x<sub>stem</sub> = 44 + (⟦hl|ν⟧ / ⟦fmax|6 Hz⟧) · (w − 58), &nbsp; stem height ∝ C<sub>ν</sub><br>full panel height = max(40 px, tallest C<sub>ν</sub>) &nbsp; (Section 8)',
            note: '<code>spec.w</code> is the panel width w in CSS pixels. The axis runs from <code>left</code> = 44 to <code>right</code> = w − 14, so <code>right - left</code> is w − 58, as in the note. The function <code>X</code> in this place is not a position along the medium: it maps a frequency <code>nu</code> in Hz to a screen column, 0 Hz at the left end and <code>NUMAX</code> = 6 Hz at the right, the largest ν = f s the sliders allow, 3 × 2. <code>amax</code> is the stem height that fills the panel: 40 px, the largest single amplitude, or the tallest stem if that is taller. For each stem of step 8, <code>x</code> is its column and <code>yTop</code> the top of its line: <code>base</code> is the axis, 24 px above the bottom, and the stem fills the fraction C<sub>ν</sub>/<code>amax</code> of the space up to 14 px below the top. The dot at <code>yTop</code> and the stem’s colour follow in the code. A stem is a line without width; a real analyser, or an ear, listening for a finite time T could not separate frequencies closer than about 1/T.',
            code: `var w = spec.w, h = spec.h, left = 44, right = w - 14, base = h - 24, top = 14;
var X = function (nu) { return left + nu / ⟦fmax|NUMAX⟧ * (right - left); };
...
var ls = lines(), amax = Math.max(40, ls.reduce(function (m, g) { return Math.max(m, g.A); }, 0));
...
var x = X(⟦hl|wv.nu⟧), yTop = base - wv.A / amax * (base - top);`,
            syms: [
                ['hl', 'ν<sub>1</sub>', 'f₁ s₁', 'where the stem of Wave 1 stands, Hz'],
                ['fmax', 'ν<sub>max</sub>', 'NUMAX', 'right end of the axis'],
                ['An', 'A<sub>i</sub>', 'waves[i].A', 'amplitudes now loaded, px']
            ]
        }
    ]
};
