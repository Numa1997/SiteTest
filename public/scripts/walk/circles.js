/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.circles = {
    intro: 'Seven steps from “every source sends out rings” to one coloured pixel. The numbers in the table are read at the centre of the field, live, from the same arrays the picture is drawn from.',
    steps: [
        {
            title: 'Wave number and damping',
            where: 'precompute() — line 1',
            math: '⟦k|k⟧ = 2π / ⟦lam|λ⟧, &nbsp; ⟦g|γ⟧ = (damping slider) / R, &nbsp; R = 300 px',
            note: 'k turns a distance into a phase angle: one wavelength of travel adds 2π. γ is an attenuation per pixel; dividing the slider by R = 300 px means the slider value is the number of e-foldings the amplitude loses over 300 px.',
            code: `var ⟦k|k = 2 * Math.PI / lambda.value⟧, ⟦g|g = damp.value / R⟧;
var ⟦N|n = sources.length⟧, ⟦norm|norm = 1 / Math.max(1, n)⟧;`,
            syms: [
                ['lam', 'λ', 'lambda.value', 'wavelength, px'],
                ['k', 'k', 'k', 'wave number, rad/px'],
                ['g', 'γ', 'g', 'attenuation, 1/px'],
                ['N', 'N', 'n', 'number of sources'],
                ['norm', '1/N', 'norm', 'keeps |ψ| ≤ 1']
            ]
        },
        {
            title: 'Distance from a source to a grid point',
            where: 'precompute() — the two inner loops',
            math: 'x = (i + ½)⟦dx|Δx⟧ − x<sub>s</sub>, &nbsp; y = (j + ½)Δy − y<sub>s</sub><br>⟦r|r⟧ = √(x² + y²)',
            note: 'The field lives on a fixed world 800 px wide, sampled on a coarse grid of cols × rows cells; (i + ½) puts each sample at the centre of its cell. Sources sit 10 px above the bottom edge, so y<sub>s</sub> = worldH − 10.',
            code: `var ⟦dx|dx = WORLD_W / cols⟧, dy = worldH / rows, sy = worldH - SOURCE_LIFT;
...
var y = (j + 0.5) * dy - sy, y2 = y * y;
var x = (i + 0.5) * dx - sx;
var ⟦r|r = Math.sqrt(x * x + y2)⟧;`,
            syms: [
                ['dx', 'Δx', 'dx', 'world pixels per grid cell'],
                ['grid', 'cols × rows', 'cols, rows', 'grid size'],
                ['r', 'r', 'r', 'centre point → source 1, px']
            ]
        },
        {
            title: 'Amplitude and phase from one source',
            where: 'precompute() — innermost loop',
            math: '⟦a|a⟧ = e<sup>−γr</sup> / N, &nbsp; ⟦ph|φ⟧ = k r',
            note: 'The ring from source s at distance r has amplitude a and a phase lag kr behind the source: the crest you see at r left the source r/v seconds ago. The factor 1/N keeps the sum between −1 and 1 however many sources you add.',
            code: `var ⟦a|a = Math.exp(-g * r) * norm⟧, ⟦ph|ph = k * r⟧;`,
            syms: [
                ['a', 'a', 'a', 'amplitude from source 1 at the centre'],
                ['ph', 'φ', 'ph', 'phase kr, rad'],
                ['r', 'r', 'r', 'px']
            ]
        },
        {
            title: 'Two maps that hold all of space',
            where: 'precompute() — the accumulation',
            math: 'ψ = Σ<sub>s</sub> a<sub>s</sub> cos(k r<sub>s</sub> − ωt) = ⟦C|C⟧ cos ωt + ⟦S|S⟧ sin ωt<br>C = Σ<sub>s</sub> a<sub>s</sub> cos k r<sub>s</sub>, &nbsp; S = Σ<sub>s</sub> a<sub>s</sub> sin k r<sub>s</sub>',
            note: 'From cos(A − B) = cos A cos B + sin A sin B with A = kr, B = ωt. All sources share one ω, so time factors out of the whole sum. C and S are computed once per change, not once per frame.',
            code: `⟦C|sumC[p] += a * Math.cos(ph)⟧;
⟦S|sumS[p] += a * Math.sin(ph)⟧;`,
            syms: [
                ['C', 'C', 'sumC[p]', 'cosine map at the centre'],
                ['S', 'S', 'sumS[p]', 'sine map at the centre']
            ]
        },
        {
            title: 'The field at this instant',
            where: 'render() — per pixel, every frame',
            math: '⟦psi|ψ⟧ = C · ⟦c|cos ωt⟧ + S · ⟦s|sin ωt⟧, &nbsp; clipped to [−1, 1]',
            note: 'Two multiplications and one addition per grid point, whatever N is. The clip only matters by rounding: with 1/N normalisation and e<sup>−γr</sup> ≤ 1, |ψ| never exceeds 1.',
            code: `var ⟦c|c = Math.cos(omegaT)⟧, ⟦s|s = Math.sin(omegaT)⟧, d = img.data;
...
var ⟦psi|v = sumC[p] * c + sumS[p] * s⟧;
if (v > 1) v = 1; else if (v < -1) v = -1;`,
            syms: [
                ['c', 'cos ωt', 'c', ''],
                ['s', 'sin ωt', 's', ''],
                ['psi', 'ψ', 'v', 'field at the centre, between −1 and 1']
            ]
        },
        {
            title: 'The clock',
            where: 'Sim.clock callback',
            math: '⟦wt|ωt⟧ ← ωt + 2π ⟦f|f⟧ Δt, &nbsp; v = f λ',
            note: 'Δt is the real time between frames, so a 1 Hz setting completes one full cycle per second on any screen. The phase speed readout is just f λ in px/s.',
            code: `⟦wt|omegaT += 2 * Math.PI * freq.value * dt⟧;
...
document.getElementById('r-v').textContent = Math.round(⟦f|freq.value⟧ * lambda.value) + ' px/s';`,
            syms: [
                ['f', 'f', 'freq.value', 'frequency, Hz'],
                ['wt', 'ωt', 'omegaT', 'phase, rad (grows without bound)'],
                ['v', 'v', 'freq × λ', 'phase speed, px/s']
            ]
        },
        {
            title: 'A number becomes a colour',
            where: 'the LUT builder and render()',
            math: '⟦idx|n⟧ = round(127.5 ψ + 127.5) ∈ {0, …, 255}<br>colour = mid + (end − mid) · |a<sub>n</sub>|<sup>0.8</sup>, &nbsp; a<sub>n</sub> = n/127.5 − 1',
            note: 'ψ = −1 maps to ink, 0 to cream, +1 to burgundy. The exponent 0.8 < 1 lifts small |ψ| slightly, so the weak far field is still visible. All 256 colours are computed once at start-up.',
            code: `var a = i / 127.5 - 1, s = Math.pow(Math.abs(a), 0.8), end = a < 0 ? neg : pos;
for (var c = 0; c < 3; c++) LUT[i * 3 + c] = Math.round(mid[c] + (end[c] - mid[c]) * s);
...
var ⟦idx|idx = Math.round(v * 127.5 + 127.5) * 3⟧;`,
            syms: [
                ['psi', 'ψ', 'v', 'at the centre'],
                ['idx', 'n', 'idx / 3', 'colour-table entry'],
                ['rgb', 'colour', 'LUT[idx…]', 'RGB at the centre']
            ]
        }
    ]
};
