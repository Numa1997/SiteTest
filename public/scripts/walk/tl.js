/* From symbols to code — Fig. 4, Transverse and longitudinal waves. Loaded by sim.js from the page's data-walk key "tl".
   Each step pairs one numbered equation of the page's lecture note with the lines of the page's code that evaluate it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which the page defines next to its own state. */
window.WALK = window.WALK || {};

(function () {
    /* an equation number and an upright word inside the italic formula column */
    function eq(n) { return '<span style="font-style: normal; margin-left: 0.9em">(' + n + ')</span>'; }
    function rm(t) { return '<span style="font-style: normal">' + t + '</span>'; }
    /* a note with `code names` set in the house mono face */
    function n(t) {
        return t.replace(/`([^`]*)`/g, function (m, c) {
            return '<code style="font-family: var(--mono); font-size: 0.88em">' + c.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</code>';
        });
    }

    window.WALK.tl = {
        intro: 'Eleven steps through the lecture note in its own order: the particles and the starting state, the wave formula (1) and its speed (2), the particle velocity (3), the wave equation (5) that the formula solves, the density (10), compressions (11) and amplitude cap (12) of the lower row, the clock (16), and the map (17) from the medium to the screen. Each step quotes the lines of this page that evaluate the equation; a line “...” stands for page lines left out. The Now column follows the particle in the middle of each row, the one drawn in burgundy when “Follow one particle” is on. Section 6, the energy, has no step, because the page computes no energy.',
        steps: [
            {
                title: 'The medium, its particles and the starting state',
                where: 'top of the script; draw(), lines 2 and 3 and the transverse loop',
                math: '0 ≤ X ≤ 640 px, &nbsp; ⟦X|X<sub>i</sub>⟧ = i · 640/(N − 1), &nbsp; i = 0, 1, …, N − 1<br>' +
                      'i<sub>follow</sub> = ⌊(N − 1)/2⌋, &nbsp; ⟦wt|ωt⟧ = 0 ' + rm('when the page opens'),
                note: n('Section 2 labels every particle by its rest position X, the place where it sits when there is no wave. The medium is `LENGTH = 640` px of the drawing long. `N = count.value` is the number of particles in each row, 26 by default, and the loop line `X = i * LENGTH / (N - 1)` spreads them evenly from X = 0 to X = 640 px, so at the default neighbours rest 640/25 = 25.6 px apart. `follow` picks the middle particle, number 12 when they are counted from 0, at X = 307.2 px: the burgundy one, and the one the Now column reads. The only quantity the page carries from one frame to the next is `omegaT`, the phase ωt of the source in radians. It is 0 when the page opens, which is the first frame drawn in Figure 1 of the note; step 9 shows how it grows. Everything else is computed afresh from the sliders in every frame.'),
                code: `var LENGTH = 640;
...
var ⟦wt|omegaT = 0⟧, fps = 0, frames = 0;
...
var k = 2 * Math.PI / lambda.value, N = count.value, A = amp.value, AL = longAmp();
var yT = h * 0.3, yL = h * 0.77, follow = Math.floor((N - 1) / 2);
...
⟦X|X = i * LENGTH / (N - 1)⟧;`,
                syms: [
                    ['X', 'X<sub>i</sub>', 'X', 'rest position of the followed particle, px'],
                    ['wt', 'ωt', 'omegaT', 'phase of the source, rad, counted from 0 at page load']
                ]
            },
            {
                title: 'Equation (1): one formula for every particle',
                where: 'draw(), lines 2 and 9 and the transverse loop',
                math: '⟦xi|ξ(X, t)⟧ = ⟦A|A⟧ sin(⟦phase|kX − ωt⟧)' + eq(1) + '<br>' +
                      '⟦k|k⟧ = 2π/λ, &nbsp; ⟦om|ω⟧ = 2π⟦f|f⟧',
                note: n('This is the whole model in one formula. `lambda.value` is the wavelength λ in px and `freq.value` the frequency f in Hz, both read from the sliders. From them the code makes the wavenumber `k = 2 * Math.PI / lambda.value`, in rad per px, and the angular frequency `om = 2 * Math.PI * freq.value`, in rad/s. `A = amp.value` is the amplitude A in px. Inside the loop over the particles, `phA[i] = k * X - omegaT` stores the phase kX − ωt of particle i, which says where in its cycle it is now, and `xiA[i] = A * Math.sin(k * X - omegaT)` stores its displacement ξ in px, across the direction of travel in the upper row. There is no force and no acceleration in this code: the page evaluates (1) at every particle in every frame. The stored phase keeps growing with ωt; the Now column shows it reduced to the range from −π to π.'),
                code: `var ⟦k|k = 2 * Math.PI / lambda.value⟧, N = count.value, ⟦A|A = amp.value⟧, AL = longAmp();
...
var sA = ds.alloc('sL'), ... ⟦om|om = 2 * Math.PI * freq.value⟧;
...
Xa[i] = X; ⟦phase|phA[i] = k * X - omegaT⟧; ⟦xi|xiA[i] = A * Math.sin(k * X - omegaT)⟧; ...`,
                syms: [
                    ['A', 'A', 'amp.value', 'amplitude set by the slider, px'],
                    ['f', 'f', 'freq.value', 'frequency, Hz'],
                    ['k', 'k', '2 * Math.PI / lambda.value', 'wavenumber, rad/px'],
                    ['wt', 'ωt', 'omegaT', 'phase of the source, rad'],
                    ['phase', 'kX − ωt', 'phA[i]', 'phase of the followed particle, rad'],
                    ['xi', 'ξ', 'xiA[i]', 'its displacement in the upper row, px']
                ]
            },
            {
                title: 'Equation (2): the pattern moves at v, and so do the crests',
                where: 'readouts(), and draw() — the tan crest markers',
                math: 'kX − ωt = ' + rm('const') + ' &nbsp;⇒&nbsp; ⟦v|v⟧ = dX/dt = ω/k = fλ' + eq(2) + '<br>' +
                      '⟦T|T⟧ = 1/f, &nbsp; ' + rm('crest at') + ' kX − ωt = π/2: &nbsp; ⟦xc|X<sub>c</sub>⟧ = (π/2 + ωt)/k + nλ',
                note: n('Every feature of the wave is a place of fixed phase; a crest is where the phase is π/2. To keep kX − ωt fixed while ωt grows, X has to grow at the rate ω/k, which is equation (2): in one period T = 1/f the pattern moves on by one wavelength. The code computes the speed as `v = freq.value * lambda.value`, in px/s, and shows it in the Speed readout: 0.50 Hz × 220 px = 110 px/s at the default. `1 / freq.value` is the period T in s, shown in the Period readout. `crest` solves kX − ωt = π/2 for X and gives X<sub>c</sub> in px of the medium. The double `% lambda.value + lambda.value) % lambda.value` is a remainder that stays between 0 and λ even when its argument is negative, so `crest` is the first crest from the left end. The `for` loop then steps on by λ and draws a tan triangle 8 px above the highest point of the wave at every crest. Since `crest` grows with `omegaT`, the triangles move at v.'),
                code: `var ⟦v|v = freq.value * lambda.value⟧;
document.getElementById('r-v').textContent = Math.round(v) + ' px/s';
...
document.getElementById('r-t').textContent = (⟦T|1 / freq.value⟧).toFixed(2) + ' s';
...
var ⟦xc|crest = (((Math.PI / 2 + omegaT) / k) % lambda.value + lambda.value) % lambda.value⟧;
for (X = crest; X <= LENGTH; X += lambda.value) marker(left + X * s, yT - A * s - 8);`,
                syms: [
                    ['v', 'v', 'v', 'speed of the pattern, px/s'],
                    ['T', 'T', '1 / freq.value', 'period, s'],
                    ['f', 'f', 'freq.value', 'frequency, Hz'],
                    ['xc', 'X<sub>c</sub>', 'crest', 'first crest from the left end, px']
                ]
            },
            {
                title: 'Equation (3): how fast each particle moves',
                where: 'draw() — the transverse and the longitudinal loop',
                math: '⟦u|u⟧ = ∂ξ/∂t = −Aω cos(kX − ωt)<br>' +
                      '∂ξ/∂X = Ak cos(kX − ωt), &nbsp; u = −v ∂ξ/∂X' + eq(3),
                note: n('Differentiating (1) at a fixed rest position X gives the velocity u of that particle; differentiating at a fixed time gives the slope of the snapshot. The page stores u for every particle. `vxA[i] = -A * om * Math.cos(k * X - omegaT)` is u = ∂ξ/∂t of the upper row in px/s, and `vsA[i]` is the same with the lower row’s amplitude A<sub>L</sub> = `AL` (steps 6 and 8) in place of A. The largest value is Aω, 26 px × 3.14 rad/s = 81.7 px/s at the default. It depends on A and f but not on λ, and its ratio to the wave speed is Aω/v = Ak = 0.743 at the default: the particles move more slowly than the pattern. These velocities are only stored, not drawn; the Data panel lists them for every particle as ∂ξ/∂t and ∂s/∂t. The slope ∂ξ/∂X returns in step 6 as the stretch of the lower row.'),
                code: `... ⟦u|vxA[i] = -A * om * Math.cos(k * X - omegaT)⟧; yiA[i] = yT - xi;
...
sA[i] = AL * Math.sin(k * X - omegaT); xA[i] = X + sA[i]; ⟦u|vsA[i] = -AL * om * Math.cos(k * X - omegaT)⟧;`,
                syms: [
                    ['phase', 'kX − ωt', 'phA[i]', 'phase of the followed particle, rad'],
                    ['A', 'A', 'amp.value', 'amplitude of the upper row, px'],
                    ['AL', 'A<sub>L</sub>', 'AL', 'amplitude of the lower row, px']
                ]
            },
            {
                title: 'Equations (5) and (9): the wave equation that (1) solves',
                where: 'readouts() — the speed, the wavenumber and ω',
                math: '∂²ξ/∂t² = v² ∂²ξ/∂X²' + eq(5) + '<br>' +
                      'ξ = g(X − vt) + h(X + vt)' + eq(9) + '<br>' +
                      rm('equation (1):') + ' g(z) = A sin kz, &nbsp; h = 0, &nbsp; ⟦om|ω⟧ = ⟦v|v⟧⟦k|k⟧',
                note: n('Section 4 derives the wave equation (5) from Newton’s second law, with v = √(F/μ) for a string, √(E/ρ) for a rod and √(γp/ρ) for a gas, and Section 4.4 shows that any shape moving as g(X − vt) solves it. The page holds no tension, mass or modulus, and it integrates no differential equation. It draws the exact solution (1), which is the case g(z) = A sin kz, h = 0 of (9), and (1) solves (5) exactly when ω = vk. In `readouts()` this holds for every slider setting: `kk` = 2π/λ in rad/px and `om` = 2πf in rad/s both come from the sliders, so `om / kk` = fλ, the same product as `v = freq.value * lambda.value` in px/s. The page therefore never picks v; it follows from f and λ, which amounts to choosing a new medium every time one of those sliders moves. The energy of Section 6, equations (13) to (15), is not computed anywhere in the code.'),
                code: `var ⟦v|v = freq.value * lambda.value⟧;
...
var ⟦k|kk = 2 * Math.PI / lambda.value⟧, ⟦om|om = 2 * Math.PI * freq.value⟧;`,
                syms: [
                    ['v', 'v', 'v', 'speed of the pattern, px/s'],
                    ['k', 'k', 'kk', 'wavenumber, rad/px'],
                    ['f', 'f', 'freq.value', 'frequency, Hz']
                ]
            },
            {
                title: 'Equation (10): positions and density in the lower row',
                where: 'draw() — the longitudinal loop',
                math: '⟦xl|x⟧ = X + ξ, &nbsp; ⟦sL|ξ⟧ = ⟦AL|A<sub>L</sub>⟧ sin(kX − ωt)<br>' +
                      '⟦rho|ρ/ρ<sub>0</sub>⟧ = 1/(1 + ∂ξ/∂X) = 1/(1 + ⟦AkL|A<sub>L</sub>k⟧ cos(kX − ωt))' + eq(10),
                note: n('In the lower row the same phase moves each particle along the line, to x = X + ξ (Section 2), with the amplitude A<sub>L</sub> = `AL = longAmp()` of step 8 in place of A. `sA[i]` is this displacement ξ in px (the Data panel calls it s, which is not the scale s of step 10), and `xA[i] = X + sA[i]` is the position x of the particle in px of the medium. Two particles that rest dX apart are now dX (1 + ∂ξ/∂X) apart. The matter between them is the same, so the density goes as the inverse of that spacing: `rhoA[i]` is ρ/ρ<sub>0</sub> of (10), the density relative to rest, a pure number. The code uses the exact form, not the linearised second line of (10), 1 − A<sub>L</sub>k cos(kX − ωt). At the default A<sub>L</sub>k = 0.743, so ρ/ρ<sub>0</sub> runs from 1/(1 + 0.743) = 0.574 in the rarefactions to 1/(1 − 0.743) = 3.88 at the compression centres.'),
                code: `X = i * LENGTH / (N - 1);
...
⟦sL|sA[i] = AL * Math.sin(k * X - omegaT)⟧; ⟦xl|xA[i] = X + sA[i]⟧; ...
⟦rho|rhoA[i] = 1 / (1 + AL * k * Math.cos(k * X - omegaT))⟧; ...`,
                syms: [
                    ['AL', 'A<sub>L</sub>', 'AL', 'amplitude of the lower row, px'],
                    ['phase', 'kX − ωt', 'phA[i]', 'phase of the followed particle, rad'],
                    ['xl', 'x', 'xA[i]', 'its position in the lower row, px'],
                    ['AkL', 'A<sub>L</sub>k', 'ALk', 'largest stretch, no unit, below 0.8'],
                    ['rho', 'ρ/ρ<sub>0</sub>', 'rhoA[i]', 'density at the followed particle relative to rest']
                ]
            },
            {
                title: 'Equation (11): where the compressions are',
                where: 'draw() — the compression markers',
                math: rm('densest at') + ' cos(kX − ωt) = −1: &nbsp; ⟦xp|X<sub>p</sub>⟧ = (π + ωt)/k + nλ<br>' +
                      'X<sub>p</sub> − ⟦xc|X<sub>c</sub>⟧ = (π − π/2)/k = λ/4' + eq(11),
                note: n('The density (10) is largest where cos(kX − ωt) = −1, at phase π. There ξ = A<sub>L</sub> sin π = 0: the particles just behind have been pushed forward and those just ahead pulled back, so both crowd towards that point. `comp0` solves kX − ωt = π for X, with the same positive remainder as `crest` in step 3, and is the first compression centre X<sub>p</sub> from the left end, in px of the medium. The loop steps on by λ and draws a tan triangle 6 px (`COMPRESSION_GAP`) above the shaded band, whose half-height is `band` = 34 px. Compared with `crest`, the only change is π in place of π/2, so each compression sits (π/2)/k = λ/4 ahead of a crest, 55 px at the default λ = 220 px, in the direction of travel. In the Now column X<sub>p</sub> − X<sub>c</sub> is λ/4, or λ/4 − λ for the moments when X<sub>p</sub> has already wrapped round to the start of the row.'),
                code: `var ⟦xp|comp0 = (((Math.PI + omegaT) / k) % lambda.value + lambda.value) % lambda.value⟧;
for (X = comp0; X <= LENGTH; X += lambda.value) marker(left + X * s, yL - band - COMPRESSION_GAP);`,
                syms: [
                    ['xp', 'X<sub>p</sub>', 'comp0', 'first compression centre from the left end, px'],
                    ['xc', 'X<sub>c</sub>', 'crest', 'first crest from the left end, px']
                ]
            },
            {
                title: 'Equation (12): the cap on the lower amplitude',
                where: 'longAmp() and readouts()',
                math: '⟦AL|A<sub>L</sub>⟧ = min(⟦A|A⟧, 0.8/k) = min(A, 0.8λ/2π)' + eq(12) + '<br>' +
                      '1 + ∂ξ/∂X ≥ 1 − ⟦AkL|A<sub>L</sub>k⟧ ≥ 0.2',
                note: n('The spacing factor 1 + ∂ξ/∂X of step 6 is smallest at the compression centres, where it is 1 − A<sub>L</sub>k. If A<sub>L</sub>k reached 1 it would drop to zero, and beyond that particles would pass through their neighbours, which no medium allows; by (3) that is the same as a particle moving forward faster than the wave. `longAmp()` therefore returns the smaller of the slider amplitude `amp.value`, which is A in px, and `0.8 * lambda.value / (2 * Math.PI)`, which is 0.8/k in px. So A<sub>L</sub>k never exceeds 0.8: the tightest spacing is 20 % of the rest spacing and the densest point 5 times the rest density. `readouts()` writes A<sub>L</sub>, rounded, into the Longit. A readout and adds “(cap)” when `al < amp.value`, and stores the product A<sub>L</sub>k as `ALk`. At the default the cap is 0.8 × 220 px/2π = 28.0 px, above A = 26 px, so both rows have the same amplitude; at λ = 110 px the cap is 14.0 px and the readout shows “14 px (cap)”. The upper row has no such limit.'),
                code: `function longAmp() { return ⟦AL|Math.min(amp.value, 0.8 * lambda.value / (2 * Math.PI))⟧; }
...
var al = longAmp();
document.getElementById('r-al').textContent = al.toFixed(0) + ' px' + (al < amp.value ? ' (cap)' : '');
...
ds.set('Ak', amp.value * kk); ⟦AkL|ds.set('ALk', al * kk)⟧; ...`,
                syms: [
                    ['AL', 'A<sub>L</sub>', 'longAmp()', 'amplitude of the lower row, px'],
                    ['A', 'A', 'amp.value', 'amplitude set by the slider, px'],
                    ['AkL', 'A<sub>L</sub>k', 'al * kk', 'largest stretch, no unit, at most 0.8']
                ]
            },
            {
                title: 'Equation (16): the clock advances the phase',
                where: 'the Sim.clock callback, once per screen frame',
                math: '⟦wt|ωt⟧ ← ωt + 2π⟦f|f⟧ Δt' + eq(16),
                note: n('This is the only step in time the page takes. `Sim.clock` calls the function once per screen frame with `dt`, the real time Δt in s since the previous frame. The line adds 2πf Δt to `omegaT`, so the phase ωt grows at the rate ω = 2πf in rad/s, and `draw()` then evaluates (1) afresh at every particle and redraws both rows. Because (1) is the exact solution, no error builds up in the shape of the wave; what remains is the rounding of double-precision arithmetic. Adding up the phase, rather than computing 2πf t from the clock time t, keeps the wave continuous when the Frequency slider moves: only the rate changes, not the phase already reached. The clock in sim.js passes `dt` = 0 while paused and never more than 0.05 s, so after a stall the wave resumes instead of leaping ahead; at the top frequency, 2 Hz, that is at most 0.63 rad per frame. On a device set to reduce motion the clock starts paused.'),
                code: `var clk = Sim.clock(function (dt, t) {
⟦wt|omegaT += 2 * Math.PI * freq.value * dt⟧;
...
draw();`,
                syms: [
                    ['wt', 'ωt', 'omegaT', 'phase of the source, rad'],
                    ['f', 'f', 'freq.value', 'frequency, Hz']
                ]
            },
            {
                title: 'Equation (17): pixels of the medium into screen pixels',
                where: 'draw(), lines 1 to 3, the transverse discs and the longitudinal loop',
                math: '⟦s|s⟧ = (W − 44)/640, &nbsp; ⟦xu|x<sub>upper</sub>⟧ = 22 + sX,<br>' +
                      '⟦xlow|x<sub>lower</sub>⟧ = 22 + s(X + ξ)' + eq(17) + '<br>' +
                      '⟦yi|y⟧ = ⟦yT|y<sub>T</sub>⟧ − sξ, &nbsp; y<sub>T</sub> = 0.3 H, &nbsp; y<sub>L</sub> = 0.77 H',
                note: n('The model lives in a medium 640 px long; the canvas is W = `box.w` wide and H = `box.h` high in screen pixels, and changes with the window. `LEFT = 22` px is the margin on each side, so 44 px are lost and `s = (right - left) / LENGTH` is the scale (W − 44)/640, screen px per px of the medium: 1.134 on the 770 px wide canvas of a 1440 px window, 0.4875 on the 356 px canvas of a phone. The rest line of the upper row is `yT`, 30 % of the height from the top; the lower row runs along `yL`, at 77 %. A transverse disc is drawn at x<sub>upper</sub> = `left + X * s` and at height y<sub>T</sub> − sξ, with a minus sign because screen y points down, so a positive ξ lifts the disc. A longitudinal disc is drawn at `px`, which is x<sub>lower</sub> = 22 + s(X + ξ), on the line `yL`, and does not move up or down. The discs have a radius of 4.5 px in the upper row and 4 px in the lower, 6.5 px for the followed particle. Every particle is drawn at exactly the screen position the page stores for it.'),
                code: `var LEFT = 22, BAND = 34, COMPRESSION_GAP = 6;
function draw() {
var w = box.w, h = box.h, left = LEFT, right = w - LEFT, ⟦s|s = (right - left) / LENGTH⟧;
...
var ⟦yT|yT = h * 0.3⟧, yL = h * 0.77, follow = Math.floor((N - 1) / 2);
...
ctx.arc(⟦xu|left + X * s⟧, ⟦yi|yT - A * s * Math.sin(k * X - omegaT)⟧, isF ? 6.5 : 4.5, 0, Math.PI * 2);
...
⟦xlow|px = left + (X + AL * Math.sin(k * X - omegaT)) * s⟧;
...
ctx.arc(px, yL, isFollowed ? 6.5 : 4, 0, Math.PI * 2);`,
                syms: [
                    ['s', 's', 's', 'screen px per px of the medium'],
                    ['X', 'X', 'X', 'rest position of the followed particle, px'],
                    ['yT', 'y<sub>T</sub>', 'yT', 'rest line of the upper row, screen px from the top'],
                    ['yi', 'y', 'yiA[i]', 'height of the followed disc, screen px from the top']
                ]
            },
            {
                title: 'The curve and the shading: where the picture differs from the numbers',
                where: 'draw() — the burgundy curve and the band behind the lower row',
                math: rm('curve:') + ' y = y<sub>T</sub> − sA sin(kX − ωt), &nbsp; X = 0, 3, …, 639 px ' + rm('and') + ' 640 px<br>' +
                      rm('tint opacity') + ' = 0.03 + 0.2 ⟦comp|max(0, −cos(kX − ωt))⟧, &nbsp; X = 0, 10, …, 640 px',
                note: n('Two things on the canvas are drawn through extra sample points that are not particles and are not stored. The thin burgundy curve of the upper row is (1) evaluated every 3 px of the medium, 214 points from X = 0 to 639 px, plus a last one at the right end, X = 640 px: 215 points in all. Behind the lower row a band 68 px tall (twice `BAND`) is tinted burgundy with opacity 0.03 + 0.2 `comp`, where `comp` = max(0, −cos(kX − ωt)) is 1 at a compression centre and 0 across the half wavelength around each rarefaction. It is set at 65 points, one every 640/64 = 10 px, and the canvas gradient blends linearly between them. The tint is a guide to where the compressions are, not a plot of the density: it is symmetric and stops at an opacity of 0.23, while the stored density (10) is lopsided, 3.88 at the compressions and 0.574 in the rarefactions at the default. It is also laid out by rest position X, while the particles sit at X + ξ; the two agree at the compression centres, where ξ = 0. The faithful picture of the density is the crowding of the bars. The page also stores `comp` at every particle, `compA[i]`, and that is the value in the Now column.'),
                code: `for (X = 0; X <= LENGTH; X += 3) {
var y = yT - A * s * Math.sin(k * X - omegaT);
...
ctx.lineTo(right, yT - A * s * Math.sin(k * LENGTH - omegaT));
...
for (X = 0; X <= LENGTH; X += LENGTH / 64) {
var ⟦comp|comp = Math.max(0, -Math.cos(k * X - omegaT))⟧;
grad.addColorStop(X / LENGTH, 'rgba(122, 31, 43, ' + (0.03 + 0.2 * comp).toFixed(3) + ')');
}
ctx.fillStyle = grad;
ctx.fillRect(left, yL - band, right - left, band * 2);
...
... ⟦comp|compA[i] = Math.max(0, -Math.cos(k * X - omegaT))⟧; xlA[i] = px;`,
                syms: [
                    ['comp', 'max(0, −cos(kX − ωt))', 'compA[i]', 'shading at the followed particle, 0 to 1'],
                    ['phase', 'kX − ωt', 'phA[i]', 'phase of the followed particle, rad'],
                    ['rho', 'ρ/ρ<sub>0</sub>', 'rhoA[i]', 'the stored density there, for comparison']
                ]
            }
        ]
    };
})();
