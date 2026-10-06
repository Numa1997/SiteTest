/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.water = {
    intro: 'Seven steps from the deep-water dispersion relation to the circling dots. The live column follows the burgundy parcel at the surface and in each layer below it.',
    steps: [
        {
            title: 'Pixels into metres, then ω² = gk',
            where: 'k() and f()',
            math: '⟦k|k⟧ = 2π/λ &nbsp;(rad/px), &nbsp; ⟦km|k<sub>m</sub>⟧ = 100 · k &nbsp;(rad/m)<br>ω² = g k<sub>m</sub> &nbsp;⇒&nbsp; ⟦f|f⟧ = √(g k<sub>m</sub>) / 2π',
            note: 'The drawing uses 100 px = 1 m, so a wave number per pixel is 100 times larger per metre. With “deep-water dispersion” on, f is computed exactly from λ; the slider only shows it rounded to 0.01 Hz. With it off, f is whatever you set, and the wave is no longer a real water wave.',
            code: `function ⟦k|k()⟧ { return 2 * Math.PI / lambda.value; }
function ⟦f|f()⟧ {
    return dispBox.checked ? Math.sqrt(G * ⟦km|k() * PX_PER_M⟧) / (2 * Math.PI) : freq.value;
}`,
            syms: [
                ['lam', 'λ', 'lambda.value', 'wavelength, px (÷100 for m)'],
                ['k', 'k', 'k()', 'rad/px'],
                ['km', 'k<sub>m</sub>', 'k() * PX_PER_M', 'rad/m'],
                ['f', 'f', 'f()', 'frequency, Hz']
            ]
        },
        {
            title: 'Phase speed and period',
            where: 'readouts()',
            math: '⟦c|c⟧ = f λ = ω/k = √(g/k<sub>m</sub>), &nbsp; ⟦T|T⟧ = 1/f<br>⟦cg|c<sub>g</sub>⟧ = dω/dk = c/2',
            note: 'Longer waves are faster: c ∝ √λ. That is dispersion, and it is why swell from a distant storm arrives long waves first. The group speed, at which energy travels, is half the phase speed in deep water.',
            code: `var ⟦c|c = f() * lambda.value / PX_PER_M⟧;
document.getElementById('r-c').textContent = c.toFixed(2) + ' m/s';
document.getElementById('r-t').textContent = (⟦T|1 / f()⟧).toFixed(2) + ' s';`,
            syms: [
                ['c', 'c', 'c', 'phase speed, m/s'],
                ['T', 'T', '1 / f()', 'period, s'],
                ['cg', 'c<sub>g</sub>', 'c / 2', 'group speed, m/s (not drawn)']
            ]
        },
        {
            title: 'One parcel, one circle',
            where: 'draw() — the parcel loop',
            math: '⟦th|θ⟧ = k X<sub>0</sub> − ωt<br>⟦px|x⟧ = X<sub>0</sub> − r sin θ, &nbsp; z = z<sub>0</sub> + r cos θ',
            note: 'Each parcel circles its rest point (X₀, z₀) once per period, clockwise as seen here. At θ = 0 it is at the top of its circle moving forward at rω: under a crest the water moves with the wave; under a trough (θ = π) it moves backward. Screen y points down, so +r cos θ becomes −r cos θ in py.',
            code: `var X0 = 30 + i * (WORLD_W - 60) / (N - 1), cx = X0 * s;
⟦th|th = kk * X0 - omegaT⟧;
var ⟦px|px = (X0 - r * Math.sin(th)) * s⟧, py = cy - r * Math.cos(th) * s;`,
            syms: [
                ['X0', 'X<sub>0</sub>', 'X0', 'rest position of the followed parcel, px'],
                ['th', 'θ', 'th', 'its phase, reduced to (−π, π]'],
                ['px', 'x − X<sub>0</sub>', '−r sin θ', 'horizontal offset now, px'],
                ['pz', 'z − z<sub>0</sub>', 'r cos θ', 'vertical offset now, px']
            ]
        },
        {
            title: 'Orbits shrink with depth',
            where: 'draw() — the layer loop and readouts()',
            math: '⟦z0|z<sub>0</sub>⟧ = −56 j px, &nbsp; j = 0, 1, …, layers − 1<br>⟦r|r⟧ = a e<sup>k z<sub>0</sub></sup>',
            note: 'The velocity potential of a deep-water wave decays as e<sup>kz</sup>, so orbit radii do too. At one wavelength down, r/a = e<sup>−2π</sup> ≈ 0.19 %: the sea is calm a wavelength below the surface.',
            code: `var ⟦z0|z0 = -j * DZ⟧, ⟦r|r = A * Math.exp(kk * z0)⟧, cy = ys - z0 * s;
...
var ⟦deep|deep = Math.exp(-k() * DZ * (layers.value - 1))⟧;`,
            syms: [
                ['r', 'r<sub>0</sub>', 'r (j = 0)', 'surface orbit radius, px'],
                ['r1', 'r<sub>1</sub>', 'r (j = 1)', 'first layer below, px'],
                ['z0', 'z<sub>deep</sub>', '−56 (layers − 1)', 'deepest layer shown, px'],
                ['deep', 'r/a', 'deep', 'deepest layer, fraction of a']
            ]
        },
        {
            title: 'The surface is the top layer of parcels',
            where: 'draw() — the surface path',
            math: 'x = X − a sin(kX − ωt), &nbsp; ⟦eta|η⟧ = a cos(kX − ωt), &nbsp; X ∈ [−60, 860]',
            note: 'Tracing every surface parcel at once gives a trochoid: sharper crests, flatter troughs than a sine, and it becomes a sine when ak → 0. Starting 60 px outside the frame hides the ends of the curve.',
            code: `for (X = -60; X <= WORLD_W + 60; X += 3) {
    th = kk * X - omegaT;
    var sx = (X - A * Math.sin(th)) * s, ⟦eta|sy = ys - A * Math.cos(th) * s⟧;
    ...
}`,
            syms: [
                ['eta', 'η', 'a cos θ', 'surface height at the followed parcel, px'],
                ['a', 'a', 'a()', 'amplitude, px']
            ]
        },
        {
            title: 'Steepness limit',
            where: 'a()',
            math: '⟦a|a⟧ = min(A<sub>slider</sub>, 0.9/k) &nbsp;⇒&nbsp; ⟦ak|ak⟧ ≤ 0.9',
            note: 'dx/dX = 1 − ak cos θ on the surface. At ak = 1 the crest (θ = 0) folds into a cusp and beyond it the curve loops through itself. Real waves break well before that, at ak ≈ 0.44 (Stokes limit), so shapes above that steepness are already an idealisation.',
            code: `function ⟦a|a()⟧ { return Math.min(amp.value, 0.9 / k()); }
...
document.getElementById('r-ak').textContent = (⟦ak|a() * k()⟧).toFixed(2) + (a() < amp.value ? ' (cap)' : '');`,
            syms: [
                ['A', 'A<sub>slider</sub>', 'amp.value', 'px'],
                ['a', 'a', 'a()', 'amplitude used, px'],
                ['ak', 'ak', 'a() * k()', 'steepness']
            ]
        },
        {
            title: 'The clock and the picture',
            where: 'Sim.clock and draw() — line 1',
            math: '⟦wt|ωt⟧ ← ωt + 2π f Δt<br>⟦s|s⟧ = W / 800, &nbsp; ⟦ys|y<sub>s</sub>⟧ = max(a s + 34, 0.28 H)',
            note: 'ωt uses the exact f(), not the rounded slider value, so c and the motion stay consistent to machine precision. The rest level y<sub>s</sub> sits low enough that the tallest crest still clears the top by 34 px.',
            code: `⟦wt|omegaT += 2 * Math.PI * f() * dt⟧;
...
var w = box.w, h = box.h, ⟦s|s = w / WORLD_W⟧, kk = k(), A = a();
var ⟦ys|ys = Math.max(A * s + 34, h * 0.28)⟧, X, th;`,
            syms: [
                ['wt', 'ωt', 'omegaT', 'rad'],
                ['s', 's', 's', 'screen px per world px'],
                ['ys', 'y<sub>s</sub>', 'ys', 'rest level, px from top']
            ]
        }
    ]
};
