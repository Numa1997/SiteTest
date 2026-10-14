/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.tl = {
    intro: 'Seven steps from one sine function to two rows of moving beads. The live column follows the burgundy particle in the middle of each row, the one you can switch on with “Follow one particle”.',
    steps: [
        {
            title: 'One wave function for both rows',
            where: 'the clock and readouts()',
            math: '⟦xi|ξ(X, t)⟧ = A sin(⟦k|k⟧X − ⟦wt|ωt⟧)<br>k = 2π/λ, &nbsp; ω = 2π⟦f|f⟧, &nbsp; ⟦v|v⟧ = ω/k = f λ, &nbsp; ⟦T|T⟧ = 1/f',
            note: 'ξ is the displacement of the particle whose rest position is X. The same function drives both rows; the only difference is the direction of ξ, across the travel (transverse) or along it (longitudinal).',
            code: `⟦wt|omegaT += 2 * Math.PI * freq.value * dt⟧;
...
var ⟦v|v = freq.value * lambda.value⟧;
document.getElementById('r-t').textContent = (⟦T|1 / freq.value⟧).toFixed(2) + ' s';
document.getElementById('r-k').textContent = (⟦k|2 * Math.PI / lambda.value⟧).toFixed(4) + ' /px';`,
            syms: [
                ['xi', 'ξ', 'A sin(kX − ωt)', 'at the followed bead, world px'],
                ['f', 'f', 'freq.value', 'Hz'],
                ['k', 'k', '2π / lambda.value', 'rad/px'],
                ['wt', 'ωt', 'omegaT', 'phase, rad'],
                ['v', 'v', 'v', 'phase speed, px/s'],
                ['T', 'T', '1 / freq.value', 'period, s']
            ]
        },
        {
            title: 'The transverse row',
            where: 'draw() — transverse beads',
            math: '⟦X|X<sub>i</sub>⟧ = i · 640/(N − 1)<br>⟦yi|y<sub>i</sub>⟧ = y<sub>T</sub> − A s sin(k X<sub>i</sub> − ωt)',
            note: 'Each bead keeps its x and moves only up and down. The minus sign is because screen y points down: a positive ξ lifts the bead. s converts world pixels to screen pixels (next steps).',
            code: `⟦X|X = i * LENGTH / (N - 1)⟧;
...
ctx.arc(left + X * s, ⟦yi|yT - A * s * Math.sin(k * X - omegaT)⟧, isF ? 6.5 : 4.5, 0, Math.PI * 2);`,
            syms: [
                ['X', 'X<sub>i</sub>', 'X', 'rest position of the followed bead, world px'],
                ['phase', 'kX − ωt', '', 'its phase, reduced to (−π, π]'],
                ['xi', 'ξ', 'A sin(kX − ωt)', 'its displacement, world px'],
                ['yi', 'y<sub>i</sub>', '', 'its screen height, px from top']
            ]
        },
        {
            title: 'Where the crests are',
            where: 'draw() — the tan crest markers',
            math: 'crest: kX − ωt = π/2 + 2πn &nbsp;⇒&nbsp; ⟦xc|X<sub>c</sub>⟧ = (π/2 + ωt)/k mod λ',
            note: 'The double “% λ + λ) % λ” is a true modulo that stays positive even when the argument is negative. From X<sub>c</sub> the loop steps by λ across the row. X<sub>c</sub> grows at dX<sub>c</sub>/dt = ω/k = v: the crest travels at the phase speed.',
            code: `var ⟦xc|crest = (((Math.PI / 2 + omegaT) / k) % lambda.value + lambda.value) % lambda.value⟧;
for (X = crest; X <= LENGTH; X += lambda.value) marker(left + X * s, yT - A * s - 8);`,
            syms: [
                ['xc', 'X<sub>c</sub>', 'crest', 'first crest, world px'],
                ['v', 'v', 'f λ', 'px/s']
            ]
        },
        {
            title: 'The longitudinal row',
            where: 'longAmp() and draw() — longitudinal beads',
            math: '⟦AL|A<sub>L</sub>⟧ = min(A, 0.8/k)<br>⟦xl|x<sub>i</sub>⟧ = X<sub>i</sub> + A<sub>L</sub> sin(k X<sub>i</sub> − ωt)',
            note: 'The same ξ, now added along the direction of travel. The bead oscillates about X<sub>i</sub> left and right; nothing travels to the end of the row, only the pattern does.',
            code: `function longAmp() { return ⟦AL|Math.min(amp.value, 0.8 * lambda.value / (2 * Math.PI))⟧; }
...
⟦xl|px = left + (X + AL * Math.sin(k * X - omegaT)) * s⟧;`,
            syms: [
                ['AL', 'A<sub>L</sub>', 'longAmp()', 'longitudinal amplitude, world px'],
                ['A', 'A', 'amp.value', 'slider amplitude, px'],
                ['xl', 'x<sub>i</sub>', 'X + AL sin(…)', 'followed bead, world px']
            ]
        },
        {
            title: 'Why the amplitude is capped',
            where: 'longAmp() — the 0.8',
            math: 'dx/dX = 1 + ⟦AkL|A<sub>L</sub>k⟧ cos(kX − ωt) ≥ 1 − A<sub>L</sub>k<br>⟦rho|ρ/ρ<sub>0</sub>⟧ = 1 / (1 + A<sub>L</sub>k cos(kX − ωt))',
            note: 'dx/dX is the local spacing of neighbours relative to rest. If A<sub>L</sub>k reached 1 the spacing would drop to zero and beads would pass through each other, which a real medium cannot do. With A<sub>L</sub>k ≤ 0.8 the tightest spacing is 20 % of rest and the densest point is 5 × the rest density.',
            code: `return Math.min(amp.value, ⟦AkL|0.8 * lambda.value / (2 * Math.PI)⟧);   // 0.8 / k`,
            syms: [
                ['AkL', 'A<sub>L</sub>k', 'longAmp() · k', 'must stay below 1'],
                ['rho', 'ρ/ρ<sub>0</sub>', '', 'density at the followed bead']
            ]
        },
        {
            title: 'Compressions and their shading',
            where: 'draw() — gradient and compression markers',
            math: 'densest: cos(kX − ωt) = −1 &nbsp;⇒&nbsp; ⟦xp|X<sub>p</sub>⟧ = (π + ωt)/k mod λ<br>X<sub>p</sub> − X<sub>c</sub> = (π/2)/k = λ/4',
            note: 'So each compression sits a quarter wavelength ahead of a crest of the same ξ, in the direction of travel. The background band darkens as ⟦comp|max(0, −cos(kX − ωt))⟧, sampled at 65 points across the row.',
            code: `var ⟦comp|comp = Math.max(0, -Math.cos(k * X - omegaT))⟧;
grad.addColorStop(X / LENGTH, 'rgba(122, 31, 43, ' + (0.03 + 0.2 * comp).toFixed(3) + ')');
...
var ⟦xp|comp0 = (((Math.PI + omegaT) / k) % lambda.value + lambda.value) % lambda.value⟧;`,
            syms: [
                ['xp', 'X<sub>p</sub>', 'comp0', 'first compression, world px'],
                ['xc', 'X<sub>c</sub>', 'crest', 'first crest, world px'],
                ['comp', '', 'comp', 'shading at the followed bead, 0 to 1']
            ]
        },
        {
            title: 'World pixels into screen pixels',
            where: 'draw() — line 1',
            math: '⟦s|s⟧ = (W − 44)/640, &nbsp; x<sub>screen</sub> = 22 + X s<br>⟦yT|y<sub>T</sub>⟧ = 0.3 H, &nbsp; y<sub>L</sub> = 0.77 H',
            note: 'The row is always 640 world pixels long, so λ = 160 px shows four wavelengths on every screen. 22 px margins on each side give the 44.',
            code: `var w = box.w, h = box.h, left = 22, right = w - 22, ⟦s|s = (right - left) / LENGTH⟧;
...
var ⟦yT|yT = h * 0.3⟧, yL = h * 0.77, follow = Math.floor((N - 1) / 2);`,
            syms: [
                ['s', 's', 's', 'screen px per world px'],
                ['yT', 'y<sub>T</sub>', 'yT', 'transverse axis, px from top']
            ]
        }
    ]
};
