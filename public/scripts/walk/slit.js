/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.slit = {
    intro: 'Seven steps from two holes in a wall to the bright or dark verdict. The numbers are the ones behind the figure you are looking at; move a slider and watch every row change together.',
    steps: [
        {
            title: 'Where everything sits',
            where: 'compute() — lines 1–3',
            math: '⟦S1|S<sub>1</sub>⟧ = (X<sub>0</sub> − b/2, Y<sub>0</sub>), &nbsp; S<sub>2</sub> = (X<sub>0</sub> + b/2, Y<sub>0</sub>)<br>⟦P|P⟧ = (X<sub>0</sub> − ⟦d|d⟧ tan ⟦a|α⟧, Y<sub>0</sub> − d)',
            note: 'The barrier is the horizontal line y = Y₀ = 370 in the drawing’s coordinates, with the slit midpoint at X₀ = 300. SVG’s y axis points down, so the screen, a distance d beyond the barrier, sits at Y₀ − d. P lies on the ray from the midpoint at angle α to the normal.',
            code: `var ⟦d|d = dS.value⟧, ⟦a|a = aS.value * DEG⟧, ⟦b|b = bS.value⟧;
var ⟦S1|S1 = { x: X0 - b / 2, y: Y0 }⟧, S2 = { x: X0 + b / 2, y: Y0 };
var ⟦P|P = { x: X0 - d * Math.tan(a), y: Y0 - d }⟧;`,
            syms: [
                ['d', 'd', 'dS.value', 'barrier → screen, px'],
                ['a', 'α', 'aS.value', 'viewing angle'],
                ['b', 'b', 'bS.value', 'slit separation, px'],
                ['P', 'P', 'P', 'point on the screen, SVG px']
            ]
        },
        {
            title: 'Two paths and their exact difference',
            where: 'compute() — L1, L2 and ds',
            math: '⟦L1|L<sub>1</sub>⟧ = |P − S<sub>1</sub>|, &nbsp; ⟦L2|L<sub>2</sub>⟧ = |P − S<sub>2</sub>|<br>⟦ds|δs⟧ = L<sub>2</sub> − L<sub>1</sub> = (L<sub>2</sub>² − L<sub>1</sub>²)/(L<sub>1</sub> + L<sub>2</sub>) = 2bd tan α / (L<sub>1</sub> + L<sub>2</sub>)',
            note: 'No approximation here: with x = d tan α, L₂² − L₁² = (x + b/2)² − (x − b/2)² = 2bx, and dividing by L₁ + L₂ gives the right-hand form. The code uses the right-hand form: near the axis L₁ ≈ L₂, and subtracting them directly would lose significant digits. The table checks it against the direct difference.',
            code: `var ⟦L1|L1 = dist(S1, P)⟧, ⟦L2|L2 = dist(S2, P)⟧;
...
return { ..., L1: L1, L2: L2, Q: Q, ⟦ds|ds: 2 * b * d * Math.tan(a) / (L1 + L2)⟧ };`,
            syms: [
                ['L1', 'L<sub>1</sub>', 'L1', 'px'],
                ['L2', 'L<sub>2</sub>', 'L2', 'px'],
                ['ds', 'δs', 'ds', 'exact path difference, px'],
                ['dsid', 'L₂ − L₁', 'L2 - L1', 'direct subtraction, same number']
            ]
        },
        {
            title: 'The burgundy bar: point Q',
            where: 'compute() — ux, uy and Q',
            math: '⟦u|û⟧ = (S<sub>2</sub> − P) / L<sub>2</sub>, &nbsp; ⟦Q|Q⟧ = P + L<sub>1</sub> û<br>|S<sub>2</sub>Q| = L<sub>2</sub> − L<sub>1</sub> = δs',
            note: 'Q is where the circle about P through S₁ meets the longer path. Everything from P to Q is common to both paths, so the leftover stretch S₂Q, drawn as the thick burgundy bar, is exactly δs.',
            code: `var ⟦u|ux = (S2.x - P.x) / L2, uy = (S2.y - P.y) / L2⟧;
var ⟦Q|Q = { x: P.x + ux * L1, y: P.y + uy * L1 }⟧;`,
            syms: [
                ['u', 'û', '(ux, uy)', 'unit vector P → S₂'],
                ['Q', 'Q', 'Q', 'SVG px'],
                ['S2Q', '|S₂Q|', 'dist(S2, Q)', 'equals δs, px']
            ]
        },
        {
            title: 'Phase difference and brightness',
            where: 'readouts() and Iexact(th)',
            math: '⟦phi|φ⟧ = 2π δs / ⟦lam|λ⟧<br>⟦I|I/I<sub>0</sub>⟧ = cos²(φ/2) = cos²(π δs / λ)',
            note: 'Two equal waves shifted by φ add to an amplitude 2A cos(φ/2); intensity goes as amplitude squared, and dividing by the peak (2A)² gives cos²(φ/2). The dot on the lower curve sits at this value.',
            code: `var G = geo, ⟦m|ratio = G.ds / G.lambda⟧, ⟦phi|phi = 2 * Math.PI * ratio⟧;
...
var c = Math.cos(Math.PI * (2 * G.b * x / (l1 + l2)) / G.lambda);
⟦I|return c * c⟧;`,
            syms: [
                ['lam', 'λ', 'G.lambda', 'wavelength, px'],
                ['m', 'δs/λ', 'ratio', 'path difference in wavelengths'],
                ['phi', 'φ', 'phi', 'phase difference'],
                ['I', 'I/I<sub>0</sub>', 'Iexact(G.a)', 'brightness at P, 0 to 1']
            ]
        },
        {
            title: 'Far field: the textbook curve',
            where: 'drawPattern() — I(th), the solid burgundy curve',
            math: 'd ≫ b: &nbsp; ⟦ff|δs ≈ b sin α⟧<br>⟦Iff|I<sub>far</sub>(θ)⟧ = cos²(π b sin θ / λ)',
            note: 'When the screen is far away the two paths are nearly parallel and δs → b sin α. The solid curve uses this; the dashed ink curve uses the exact δs at the actual d. Shrink d and watch the two peel apart at large angles.',
            code: `var ⟦Iff|I = function (th) { var c = Math.cos(Math.PI * G.b * Math.sin(th) / G.lambda); return c * c; }⟧;
...
document.getElementById('r-ff').textContent = (⟦ff|G.b * Math.sin(G.a)⟧).toFixed(2) + ' px';`,
            syms: [
                ['ff', 'b sin α', 'G.b * Math.sin(G.a)', 'far-field δs, px'],
                ['ds', 'δs', 'G.ds', 'exact, px'],
                ['Iff', 'I<sub>far</sub>(α)', 'I(G.a)', 'far-field brightness at α'],
                ['I', 'I/I<sub>0</sub>', 'Iexact(G.a)', 'exact brightness at α']
            ]
        },
        {
            title: 'Fringe orders on the pattern',
            where: 'drawPattern() — the m = … labels',
            math: 'bright: ⟦sinm|sin θ<sub>m</sub> = m λ / b⟧, &nbsp; m = 0, 1, 2, … while sin θ<sub>m</sub> ≤ sin 30°',
            note: 'Setting δs = mλ in the far-field form gives the bright directions. The loop stops at the edge of the plotted range, 30°.',
            code: `for (var m = 0; ⟦sinm|m * G.lambda / G.b⟧ <= Math.sin(amax); m++) {
    var tm = Math.asin(m * G.lambda / G.b);
    s += text(X(tm), yt - 8, 'm=' + m, 'svg-mono');
}`,
            syms: [
                ['sinm', 'λ/b', 'G.lambda / G.b', 'sin θ₁, spacing of the orders'],
                ['t1', 'θ<sub>1</sub>', 'Math.asin(λ/b)', 'first bright fringe']
            ]
        },
        {
            title: 'The verdict line',
            where: 'readouts() — the three-way test',
            math: '⟦fr|f⟧ = δs/λ − ⌊δs/λ⌋<br>bright if f < 0.08 or f > 0.92; &nbsp; dark if |f − ½| < 0.08; &nbsp; otherwise partial',
            note: 'f is how far P is through the current fringe cycle. A tolerance of 0.08 wavelengths corresponds to cos²(0.08π) ≈ 0.94 at the edge of “bright” and ≈ 0.06 at the edge of “dark”, so the label is honest to within 6 % of the full brightness.',
            code: `var ⟦fr|f = ratio - Math.floor(ratio)⟧, verdict;
if (f < 0.08 || f > 0.92) verdict = 'Constructive · bright fringe, m = ' + Math.round(ratio);
else if (Math.abs(f - 0.5) < 0.08) verdict = 'Destructive · dark fringe between m = ' + ...;
else verdict = 'Partial · I/I₀ = ' + Math.pow(Math.cos(phi / 2), 2).toFixed(2);`,
            syms: [
                ['fr', 'f', 'f', 'fraction of a wavelength'],
                ['verdict', '', 'verdict', 'what the panel says']
            ]
        }
    ]
};
