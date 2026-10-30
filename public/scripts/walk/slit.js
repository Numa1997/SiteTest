/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.slit = {
    intro: 'Eleven steps through the lecture note, in its order, from the four sliders to the moving wavelets. Each step sets one numbered equation of the note, with the same symbols and the same number, beside the lines of this page’s script that evaluate it, and the Now column shows the values behind the figure you are looking at. Nothing is stepped forward in time: every slider move recomputes everything from closed formulas. Lengths are in pixels (px) of the drawing; only the ratios b/λ and d/b and the angle matter.',
    steps: [
        {
            title: 'Where the slits and P sit · (1)',
            where: 'top of the script — X0, Y0, DEG; the four sliders; compute() — its first three lines',
            math: '⟦S1|S<sub>1</sub>⟧ = (−⟦b|b⟧/2, 0), &nbsp; S<sub>2</sub> = (b/2, 0), &nbsp; ⟦P|P⟧ = (−⟦d|d⟧ tan ⟦a|α⟧, d) &emsp;<span style="font-style:normal">(1)</span><br>on the screen: x → X<sub>0</sub> + x, &nbsp; y → Y<sub>0</sub> − y, &nbsp; X<sub>0</sub> = 300, Y<sub>0</sub> = 370',
            note: 'The whole state of this page is four slider values: the distance d from the wall to P, the angle α of P from the normal to the wall, the slit separation b and the wavelength λ. Each slider calls update() when it moves, and nothing else changes the geometry. The first quoted line fixes the drawing’s frame: the wall lies at y = Y0 = 370, the midpoint M between the slits at x = X0 = 300, and DEG = π/180 converts degrees to radians. compute() then reads the sliders into d (px), a (the angle α in radians) and b (px) and places the slits and P by equation (1). The drawing’s y axis points down, so the note’s point (x, y) is drawn at (X0 + x, Y0 − y): S1 sits b/2 left of M, S2 b/2 right of it, and P lies d above the wall and d tan α to the left, on the side of S₁, as in the note.',
            code: `var X0 = 300, Y0 = 370, LEFT = 40, RIGHT = 560, DEG = Math.PI / 180;
...
var dS = Sim.slider('d', { format: function (v) { return v.toFixed(0) + ' px'; }, onInput: update });
var aS = Sim.slider('alpha', { format: function (v) { return v.toFixed(1) + '°'; }, onInput: update });
var bS = Sim.slider('b', { format: function (v) { return v.toFixed(0) + ' px'; }, onInput: update });
var lS = Sim.slider('lambda', { format: function (v) { return v.toFixed(1) + ' px'; }, onInput: update });
...
var ⟦d|d = dS.value⟧, ⟦a|a = aS.value * DEG⟧, ⟦b|b = bS.value⟧;
var ⟦S1|S1 = { x: X0 - b / 2, y: Y0 }⟧, S2 = { x: X0 + b / 2, y: Y0 };
var ⟦P|P = { x: X0 - d * Math.tan(a), y: Y0 - d }⟧;`,
            syms: [
                ['d', 'd', 'dS.value', 'distance from the wall to the observation line through P, px'],
                ['a', 'α', 'aS.value * DEG', 'direction of P from the normal; radians in the code, shown in degrees'],
                ['b', 'b', 'bS.value', 'slit separation, px'],
                ['lam', 'λ', 'lS.value', 'wavelength, px (used from step 5 on)'],
                ['S1', 'S<sub>1</sub>', 'S1', 'slit 1 in the drawing, (X₀ − b/2, Y₀), px'],
                ['P', 'P', 'P', 'the watched point in the drawing, (X₀ − d tan α, Y₀ − d), px']
            ]
        },
        {
            title: 'Two path lengths · (2)',
            where: 'dist(p, q); compute() — L1 and L2',
            math: '⟦L1|L<sub>1</sub>⟧ = |S<sub>1</sub>P| = √[(d tan α − b/2)² + d²]<br>⟦L2|L<sub>2</sub>⟧ = |S<sub>2</sub>P| = √[(d tan α + b/2)² + d²] &emsp;<span style="font-style:normal">(2)</span>',
            note: 'Each path is the straight line from a slit to P, and its length is Pythagoras’ theorem applied to the coordinates of step 1. dist(p, q) does exactly that: Math.hypot returns the square root of the sum of the squared horizontal and vertical separations of the two points. For S1 and P these separations are d tan α − b/2 and d, the two terms under the root in (2), so L1 in the code is L₁ of the note, in px; for S2 the first term becomes d tan α + b/2, and L2 is L₂. The flipped y axis does not matter, because only squares enter. The second line writes both lengths into the page’s data store, from which the readouts Path S₁P and Path S₂P and the Now column read them. At the defaults (d = 200 px, α = 20°, b = 40 px) they are 206.85 px and 220.48 px.',
            code: `function dist(p, q) { return Math.hypot(p.x - q.x, p.y - q.y); }
...
var ⟦L1|L1 = dist(S1, P)⟧, ⟦L2|L2 = dist(S2, P)⟧;
ds.set('L1', L1); ds.set('L2', L2);`,
            syms: [
                ['L1', 'L<sub>1</sub>', 'L1', 'path length S₁ → P, px'],
                ['L2', 'L<sub>2</sub>', 'L2', 'path length S₂ → P, px'],
                ['P', 'P', 'P', 'the watched point, px']
            ]
        },
        {
            title: 'The exact path difference · (3)',
            where: 'compute() — deltaS; storeDerived() — the direct difference',
            math: '⟦ds|δs⟧ = L<sub>2</sub> − L<sub>1</sub> = (L<sub>2</sub>² − L<sub>1</sub>²) / (L<sub>1</sub> + L<sub>2</sub>) = 2 b d tan α / (L<sub>1</sub> + L<sub>2</sub>) &emsp;<span style="font-style:normal">(3)</span><br>check: ⟦dsid|L<sub>2</sub> − L<sub>1</sub>⟧ computed directly',
            note: 'δs is how much further the wave from S₂ has travelled. Subtracting two square roots is awkward, but subtracting the squares of (2) is easy: the d² and the b²/4 cancel, and (d tan α + b/2)² − (d tan α − b/2)² = 2bd tan α. Dividing by L₁ + L₂ gives the right-hand side of (3), with no approximation. The variable deltaS is δs in px, computed from that right-hand side, and is stored under the name ds. The code avoids L2 − L1 on purpose: near the centre line the two lengths are almost equal, and subtracting two nearly equal numbers throws away significant digits, while 2bd tan α is exactly zero at α = 0. storeDerived() still stores the direct difference as ds_direct, so the two can be compared in the table; over every slider setting they differ by at most 1.4 × 10⁻¹³ px.',
            code: `var ⟦ds|deltaS = 2 * b * d * Math.tan(a) / (L1 + L2)⟧;
ds.set('ds', deltaS);
...
ds.set('ds_direct', ⟦dsid|G.L2 - G.L1⟧); ...`,
            syms: [
                ['ds', 'δs', 'deltaS', 'exact path difference by (3), px'],
                ['dsid', 'L<sub>2</sub> − L<sub>1</sub>', 'G.L2 - G.L1', 'the same number by direct subtraction, px'],
                ['L1', 'L<sub>1</sub>', 'L1', 'px'],
                ['L2', 'L<sub>2</sub>', 'L2', 'px']
            ]
        },
        {
            title: 'The far-field shortcut · (4)',
            where: 'storeDerived() — ff; readouts() — r-ff',
            math: 'P far from the slits: L<sub>1</sub> + L<sub>2</sub> ≈ 2r = 2d / cos α<br>⟦ff|δs ≈ b sin α⟧ &emsp;<span style="font-style:normal">(4)</span><br>★ δs = b sin α [1 − b² cos²α / (8r²) + …] &emsp;<span style="font-style:normal">(5)</span>',
            note: 'When P is far from the slits compared with b, both paths are close to the distance r = d/cos α from M to P, so L₁ + L₂ ≈ 2d/cos α. Put into (3), the d cancels and tan α cos α = sin α, which is (4). The code evaluates (4) as ff = G.b * Math.sin(G.a), in px, with the same b and α (in radians) as step 1, and stores it as b_sin_a, together with the error δs − b sin α as ds_err; the readout b sin α prints it with two decimals. The page does not compute the correction (5) of Section 4.1 ★. It says that the shortcut is always a little too long, by the fraction b² cos²α/(8r²): at the defaults, 13.6808 px against the exact 13.6277 px, 0.39 % too long.',
            code: `var ⟦ff|ff = G.b * Math.sin(G.a)⟧;
...
ds.set('b_sin_a', ff); ds.set('ds_err', G.ds - ff); ...
...
document.getElementById('r-ff').textContent = ds.get('b_sin_a').toFixed(2) + ' px';`,
            syms: [
                ['ff', 'b sin α', 'ff', 'far-field path difference (4), px'],
                ['ds', 'δs', 'G.ds', 'exact path difference (3), px'],
                ['d', 'd', 'G.d', 'distance from the wall, px']
            ]
        },
        {
            title: 'The phase difference · (6)',
            where: 'end of compute() — the object G; storeDerived() — ratio, phi; readouts() — r-phi',
            math: 'E = E<sub>0</sub> cos(kL<sub>1</sub> − ωt) + E<sub>0</sub> cos(kL<sub>2</sub> − ωt) = 2E<sub>0</sub> cos(Δφ/2) cos(k(L<sub>1</sub> + L<sub>2</sub>)/2 − ωt)<br>⟦phi|Δφ⟧ = k δs = 2π δs / ⟦lam|λ⟧, &nbsp; k = 2π/λ &emsp;<span style="font-style:normal">(6)</span><br>⟦m|δs/λ⟧: the path difference counted in wavelengths',
            note: 'Each wave arrives at P with the phase kL, the wavenumber k = 2π/λ times the distance it has travelled. Adding the two cosines with cos A + cos B = 2 cos((A − B)/2) cos((A + B)/2) leaves one oscillation at the frequency of the light, whose amplitude 2E₀ cos(Δφ/2) depends only on the phase difference Δφ = k δs. The page never builds the field E itself; it needs only Δφ. λ reaches the code as G.lambda, the Wavelength slider value in px, packed into the object G at the end of compute() before storeDerived(G) is called. There ratio is δs/λ, a pure number, and phi is Δφ = 2π · ratio in radians. The store also keeps Δφ/π as phi_pi, which the readout Phase Δφ and the Now column show: at the defaults δs/λ = 1.0095 and Δφ = 2.019 π, one whole wavelength and a little more.',
            code: `var G = { d: d, a: a, b: b, ⟦lam|lambda: lS.value⟧, S1: S1, S2: S2, P: P, L1: L1, L2: L2, Q: Q, ds: deltaS };
storeDerived(G);
...
var ⟦m|ratio = G.ds / G.lambda⟧, ⟦phi|phi = 2 * Math.PI * ratio⟧;
...
ds.set('phi_pi', phi / Math.PI);
...
document.getElementById('r-phi').textContent = ds.get('phi_pi').toFixed(2) + ' π';`,
            syms: [
                ['lam', 'λ', 'G.lambda', 'wavelength, px'],
                ['ds', 'δs', 'G.ds', 'exact path difference, px'],
                ['m', 'δs/λ', 'ratio', 'path difference in wavelengths'],
                ['phi', 'Δφ', 'phi', 'phase difference; radians in the code, shown in units of π']
            ]
        },
        {
            title: 'Brightness · (7)',
            where: 'storeDerived() — I and I_far_P',
            math: '⟦I|I/I<sub>0</sub>⟧ = cos²(Δφ/2) = cos²(π δs / λ) &emsp;<span style="font-style:normal">(7)</span><br>far-field value at P: ⟦Iff|cos²(π b sin α / λ)⟧',
            note: 'No eye or camera follows 5 × 10¹⁴ oscillations a second; they record the intensity, the time average of E². The average of cos² over a period is ½, so I ∝ 2E₀² cos²(Δφ/2), and dividing by I₀ = 2E₀², the intensity where the two waves arrive in step, gives (7): 1 on a bright fringe, 0 on a dark one. The first call on the quoted line stores I/I₀ as I, a pure number, from phi of step 5; Math.pow(…, 2) is the square. The second evaluates the same law with the far-field b sin α of step 4 in place of δs and stores it as I_far_P, so the two can be compared at P. The rest of the line stores the verdict of step 9. At the defaults δs is 1.0095 λ, so P sits almost on the top of the first bright fringe and I/I₀ = 0.9991.',
            code: `ds.set('I', ⟦I|Math.pow(Math.cos(phi / 2), 2)⟧); ds.set('I_far_P', ⟦Iff|Math.pow(Math.cos(Math.PI * ff / G.lambda), 2)⟧); ds.set('verdict', verdict);`,
            syms: [
                ['phi', 'Δφ', 'phi', 'phase difference, in units of π'],
                ['I', 'I/I<sub>0</sub>', "'I'", 'brightness at P with the exact δs, 0 to 1'],
                ['Iff', 'I/I<sub>0</sub> far field', "'I_far_P'", 'brightness at P with b sin α in place of δs']
            ]
        },
        {
            title: 'Bright and dark directions · (8), (9)',
            where: 'drawPattern() — the orders m; storeDerived() — θ₁ and λd/b',
            math: 'bright: δs = mλ, &nbsp; dark: δs = (m + ½)λ, &nbsp; m = 0, 1, 2, … &emsp;<span style="font-style:normal">(8)</span><br>far field, δs = b sin θ: &nbsp; ⟦sinm|sin θ<sub>m</sub> = mλ / b⟧, &nbsp; ⟦t1|θ<sub>1</sub>⟧ = arcsin(λ/b)<br>spacing on a far screen: Δy = λD / b &emsp;<span style="font-style:normal">(9)</span>; &nbsp; on the page D → d',
            note: 'P is bright when the two paths differ by a whole number m of wavelengths, the order, and dark half-way between. θ is any direction measured from the normal, the horizontal axis of the plot under the figure; with the far-field δs = b sin θ the bright directions are sin θ<sub>m</sub> = mλ/b. In drawPattern(), nm counts the orders that fit in the plot’s 30°: m runs while mλ/b ≤ sin 30°, with a tolerance of 10⁻⁹ so that an order lying exactly on the edge is kept. For each order, tm is θ<sub>m</sub> in radians; mS[m] stores sin θ<sub>m</sub>, mT[m] the angle in degrees and mX[m] = d tan θ<sub>m</sub>, where that direction meets the observation line, in px. The test m < nm inside the loop is always true. storeDerived() keeps the first order on its own, sin θ₁ = λ/b and θ₁ in degrees, or NaN when λ > b and there is no first order, and stores λd/b, the small-angle spacing (9) with the page’s d in place of the screen distance D. At the defaults that spacing is 67.5 px, but θ₁ = 19.72° lies outside the small-angle range, and d tan θ₁ = 71.7 px.',
            code: `var nm = Math.floor(Math.sin(amax) * G.b / G.lambda + 1e-9) + 1;
...
for (var m = 0; m < nm; m++) {
    var tm = Math.asin(m * G.lambda / G.b);
    if (m < nm) { mS[m] = ⟦sinm|m * G.lambda / G.b⟧; mT[m] = tm / DEG; mX[m] = G.d * Math.tan(tm); }
...
var sl = G.lambda / G.b;
ds.set('sin_theta1', sl); ds.set('theta1', ⟦t1|sl <= 1 ? Math.asin(sl) / DEG : NaN⟧);
ds.set('fringe_px', G.lambda * G.d / G.b); ...`,
            syms: [
                ['sinm', 'sin θ<sub>1</sub> = λ/b', 'sl', 'first order; the orders are spaced by this in sin θ'],
                ['t1', 'θ<sub>1</sub>', 'Math.asin(sl) / DEG', 'first bright direction, °'],
                ['lam', 'λ', 'G.lambda', 'wavelength, px'],
                ['b', 'b', 'G.b', 'slit separation, px'],
                ['d', 'd', 'G.d', 'distance from the wall, px']
            ]
        },
        {
            title: 'The point Q: one δs, three ways',
            where: 'compute() — ux, uy and Q; drawShapes() — the burgundy bar; storeDerived() — |S₂Q|',
            math: '⟦u|û⟧ = (S<sub>2</sub> − P) / L<sub>2</sub>, &nbsp; ⟦Q|Q⟧ = P + L<sub>1</sub> û<br>⟦S2Q||S<sub>2</sub>Q|⟧ = L<sub>2</sub> − L<sub>1</sub> = δs',
            note: 'Section 8 and Figure 1 turn δs into a length you can see. Walk from P towards S₂ a distance L₁: the point Q you reach lies on the circle about P through S₁, so the stretch from P to Q is as long as the whole path from S₁. What is left of the longer path, from Q to S₂, is the path difference. ux and uy are the components of the unit vector û from P towards S₂, pure numbers, and Q is P plus L₁ times û, in px of the drawing. drawShapes() draws S₂Q as the thick burgundy bar, and the dashed arc through S₁, only when δs > 0.05 px, so nothing is drawn on the centre line. storeDerived() then measures the bar as dist(G.S2, G.Q) and stores it beside the direct difference L₂ − L₁. With deltaS of step 3 these are three routes to the same number, and the table shows them side by side.',
            code: `var ⟦u|ux = (S2.x - P.x) / L2, uy = (S2.y - P.y) / L2⟧;
var ⟦Q|Q = { x: P.x + ux * L1, y: P.y + uy * L1 }⟧;
ds.set('ux', ux); ds.set('uy', uy);
...
if (G.ds > 0.05) {
...
    s += line(G.S2, G.Q, 'stroke="' + T.accent + '" stroke-width="5" stroke-linecap="round"');
...
ds.set('ds_direct', ⟦dsid|G.L2 - G.L1⟧); ds.set('S2Q', ⟦S2Q|dist(G.S2, G.Q)⟧);`,
            syms: [
                ['u', 'û', '(ux, uy)', 'unit vector from P towards S₂'],
                ['Q', 'Q', 'Q', 'end of the bar in the drawing, px'],
                ['S2Q', '|S<sub>2</sub>Q|', 'dist(G.S2, G.Q)', 'length of the burgundy bar, px'],
                ['dsid', 'L<sub>2</sub> − L<sub>1</sub>', 'G.L2 - G.L1', 'direct subtraction, px'],
                ['ds', 'δs', 'deltaS', 'from (3), px']
            ]
        },
        {
            title: 'The verdict under the readouts',
            where: 'storeDerived() — the three-way test; readouts() — the verdict line',
            math: '⟦fr|f⟧ = δs/λ − ⌊δs/λ⌋<br>Constructive if f < 0.08 or f > 0.92; &nbsp; Destructive if |f − ½| < 0.08; &nbsp; otherwise Partial, with I/I<sub>0</sub> from <span style="font-style:normal">(7)</span>',
            note: 'f is how far P has come through the current fringe cycle: 0 on a bright fringe and ½ on a dark one, by (8). The code takes f as ratio minus its floor, with ratio = δs/λ from step 5, and chooses one of three sentences. Within 0.08 of a whole number it names the bright order, the nearest whole number to δs/λ. Within 0.08 of a half it names the two orders on either side of the dark fringe. Otherwise it prints the intensity (7), rounded to two decimals. A tolerance of 0.08 wavelengths means cos²(0.08π) ≈ 0.94 at the edge of Constructive and sin²(0.08π) ≈ 0.06 at the edge of Destructive, so each label is right to within 6 % of the peak brightness. The sentence is stored as verdict (step 6), and the line under the readouts shows exactly the stored text.',
            code: `var ⟦fr|f = ratio - Math.floor(ratio)⟧, verdict;
if (f < 0.08 || f > 0.92) verdict = 'Constructive · bright fringe, m = ' + Math.round(ratio);
else if (Math.abs(f - 0.5) < 0.08) verdict = 'Destructive · dark fringe between m = ' + Math.floor(ratio) + ' and ' + (Math.floor(ratio) + 1);
else verdict = 'Partial · I/I₀ = ' + Math.pow(Math.cos(phi / 2), 2).toFixed(2);
...
document.getElementById('verdict').textContent = ⟦verdict|ds.get('verdict')⟧;`,
            syms: [
                ['m', 'δs/λ', 'ratio', 'path difference in wavelengths'],
                ['fr', 'f', 'f', 'fraction of the current fringe cycle'],
                ['verdict', 'verdict', 'verdict', 'the sentence under the readouts']
            ]
        },
        {
            title: 'The intensity plot: 301 directions',
            where: 'drawPattern() — the scales, I(th), Iexact(th), the 301 samples and the dot at α',
            math: 'θ<sub>i</sub> = 30° · i / 300, &nbsp; i = 0, 1, …, 300<br>solid: ⟦Iff|I<sub>far</sub>(θ)⟧ = cos²(π b sin θ / λ)<br>dashed: I<sub>exact</sub>(θ) = cos²(π δs(θ) / λ), &nbsp; δs(θ) = 2bx / (l<sub>1</sub> + l<sub>2</sub>), &nbsp; x = d tan θ &emsp;<span style="font-style:normal">(2), (3)</span><br>dot: at θ = ⟦a|α⟧, height ⟦I|I/I<sub>0</sub>⟧',
            note: 'The plot under the figure asks, for every direction θ from 0° to 30° in steps of 0.1°, how bright the far-field law makes it and how bright it really is at the page’s distance d. I(th) is the far-field law, the solid burgundy curve. Iexact(th) puts a point on the observation line at x = d tan θ from the centre line, finds its two path lengths l1 and l2 by (2) and its path difference by the cancellation-free form (3), and squares the cosine; that is the dashed ink curve. Where the two curves part, the far field is failing; shrink d and they separate at large angles. th is θ in radians; each sample is stored as theta (in degrees), I_far and I_exact. The scale X maps 0° to 30° onto x = 56 to 556, and Y maps I/I₀ = 0 to 1 onto y = 142 to 24, upwards on the screen. The dot is drawn at θ = α and at the height Iexact(G.a), which is the I/I₀ of step 6 for P itself. The Now column shows that value and the far-field value at α, I_far_P of step 6, which uses the same formula as I(th).',
            code: `var G = geo, x0 = 56, x1 = 556, yb = 142, yt = 24, amax = 30 * DEG;
var X = function (th) { return x0 + (th / amax) * (x1 - x0); };
var Y = function (I) { return yb - I * (yb - yt); };
var ⟦Iff|I = function (th) { var c = Math.cos(Math.PI * G.b * Math.sin(th) / G.lambda); return c * c; }⟧;
/* exact path difference for a point at distance d in direction th */
var Iexact = function (th) {
    var x = G.d * Math.tan(th), l1 = Math.hypot(x - G.b / 2, G.d), l2 = Math.hypot(x + G.b / 2, G.d);
    var c = Math.cos(Math.PI * (2 * G.b * x / (l1 + l2)) / G.lambda);
    return c * c;
};
...
for (var i = 0; i <= 300; i++) {
    var th = amax * i / 300, If = I(th), Ie = Iexact(th);
    thA[i] = th / DEG; IfA[i] = If; IeA[i] = Ie; IdA[i] = Ie - If;
...
var ⟦a|xa = X(G.a)⟧;
...
s += dot({ x: xa, y: Y(⟦I|Iexact(G.a)⟧) }, 5.5, T.accent, T.card);`,
            syms: [
                ['a', 'α', 'G.a', 'direction of P, where the dot sits'],
                ['I', 'I/I<sub>0</sub>', "'I'", 'dashed curve at α, the height of the dot: Iexact(G.a), stored as I in step 6'],
                ['Iff', 'I<sub>far</sub>(α)', "'I_far_P'", 'solid curve at α: I(G.a), stored as I_far_P in step 6'],
                ['d', 'd', 'G.d', 'distance used by the dashed curve, px'],
                ['lam', 'λ', 'G.lambda', 'wavelength, px']
            ]
        },
        {
            title: 'The moving wavelets',
            where: 'drawWaves() — the arcs and the plane wave; the Sim.clock callback — the phase',
            math: 'ϕ ← (ϕ + 0.8 Δt) mod 1, &nbsp; Δt the time since the last frame, s<br>r<sub>n</sub> = (n + ϕ)⟦lam|λ⟧, &nbsp; n = 0, 1, 2, … while r<sub>n</sub> < 430<br>opacity 0.55 (1 − r/430)',
            note: 'The only thing that moves is an illustration (Section 9). ϕ is the animation phase, a fraction of a period between 0 and 1; it is not the phase difference Δφ of step 5. Each frame the clock passes the real time dt since the previous frame, in seconds and never more than 0.05 s, and phase grows by 0.8 dt, so the arcs advance 0.8 wavelengths per second, 10.8 px/s at the default λ = 13.5 px. drawWaves() draws around each slit rose semicircles of radius r = (n + ϕ)λ out to maxR = 430 px, skipping any smaller than 1 px, and fades each as 0.55 (1 − r/430) to suggest that a wavelet weakens as it spreads. Below the wall it draws straight lines one wavelength apart, shifted by the same phase, as the incoming plane wave. The geometry, the readouts and the plot of the earlier steps do not change while this runs; real green light oscillates about 7 × 10¹⁴ times faster.',
            code: `var G = geo, ⟦lam|lam = G.lambda⟧, s = '<g clip-path="url(#above)">', maxR = 430, rr = [];
[G.S1, G.S2].forEach(function (S) {
    for (var r = phase * lam; r < maxR; r += lam) {
        if (r < 1) continue;
        if (S === G.S1) rr.push(r);
        var op = (0.55 * (1 - r / maxR)).toFixed(3);
...
for (var y = Y0 + (1 - phase) * lam; y < 440; y += lam) {
...
var clk = Sim.clock(function (dt, t) {
    if (dt > 0) {
        phase = (phase + dt * 0.8) % 1;`,
            syms: [
                ['lam', 'λ', 'lam', 'wavelength: the spacing of the arcs and of the plane-wave lines, px']
            ]
        }
    ]
};
