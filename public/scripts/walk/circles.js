/* From symbols to code, Fig. 1 (circular wave interference); loaded by sim.js from the page's data-walk key "circles".
   Each step pairs a numbered equation of the page's lecture note with the lines of this page's code that evaluate it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which the page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.circles = {
    intro: 'Nine steps from the lecture note to the pixels, in the note’s order: what the page remembers, the equations (2) to (8), how the page evaluates them with two maps, a clock and a grid (18), and how a number becomes a colour (19). Each step sets a numbered equation of the note beside the lines of this page’s script that evaluate it; a line that is only “...” stands for page lines left out. Lengths are pixels of the field, which is always 800 px wide; times are seconds. The “Now” column is read live from the page’s data store at the centre cell of the grid, the same arrays the picture is drawn from. Two names differ from the note: the code counts the sources with s, because i and j count the columns and rows of the grid, and the code’s a already carries the factor 1/N.',
    steps: [
        {
            title: 'The state: sources, sliders and one phase',
            where: 'top of the script, and the three sliders',
            math: 'state = { x<sub>1</sub>, …, x<sub>⟦N|N⟧</sub>; &nbsp;⟦lam|λ⟧, ⟦f|f⟧, γ; &nbsp;⟦wt|ωt⟧ }<br>x<sub>i</sub> = 800 px · u<sub>i</sub>; &nbsp; at the start u = (0.25, 0.75), ωt = 0',
            note: 'Nothing on this page is integrated step by step. Equation (6) gives the field at every point in closed form, so the page only has to remember what enters it: the list of source positions, the three slider values and the one phase ωt that all sources share. The first line fixes the scales of the model of Section 2: the field is 800 px wide (WORLD_W), the damping length R of equation (5) is 300 px, at most 24 sources are kept, and every source sits SOURCE_LIFT = 10 px above the bottom edge. DEFAULT is the initial condition, two sources at the fractions 0.25 and 0.75 of the width, that is x<sub>1</sub> = 200 px and x<sub>2</sub> = 600 px, the Reset pair of Section 5; omegaT = 0 starts the clock at ωt = 0. The sliders hold λ in px (lambda.value), f in Hz (freq.value) and the dimensionless γ (damp.value). Wavelength and Damping call changed(), which marks the maps of step 4 as stale; Frequency calls only readouts(), because f enters only through ωt and never changes the shape of the pattern.',
            code: `var WORLD_W = 800, R = 300, MAX_SOURCES = 24, SOURCE_LIFT = 10;
var DEFAULT = [0.25, 0.75];
...
var ⟦N|sources⟧ = DEFAULT.slice();
var ⟦wt|omegaT = 0⟧, dirty = true, redraw = true;
...
var ⟦lam|lambda⟧ = Sim.slider('lambda', { format: function (v) { return v.toFixed(1) + ' px'; }, onInput: changed });
var ⟦f|freq⟧ = Sim.slider('freq', { format: function (v) { return v.toFixed(2) + ' Hz'; }, onInput: readouts });
var damp = Sim.slider('damp', { format: function (v) { return v.toFixed(2); }, onInput: changed });`,
            syms: [
                ['N', 'N', 'sources.length', 'number of sources, at most 24'],
                ['lam', 'λ', 'lambda.value', 'wavelength, px'],
                ['f', 'f', 'freq.value', 'frequency of every source, Hz'],
                ['wt', 'ωt', 'omegaT', 'phase shared by all sources, rad']
            ]
        },
        {
            title: 'Distance from a source to a grid point',
            where: 'precompute(): the loops over sources, rows and columns',
            math: '⟦r|r<sub>i</sub>⟧ = √((x − x<sub>i</sub>)² + (y − y<sub>s</sub>)²) &nbsp;&nbsp;(2)<br>x = (column + ½) ⟦dx|Δx⟧, &nbsp; y = (row + ½) Δy, &nbsp; y<sub>s</sub> = field height − 10 px',
            note: 'Equation (2) is Pythagoras: the straight-line distance from source i to the point P = (x, y), with x to the right and y downwards from the top-left corner. The page evaluates it only at the centres of a grid of cols × rows cells (step 8). dx = Δx = 800 px / cols and dy = Δy = worldH / rows are the cell sizes in px, and the 0.5 in (i + 0.5) and (j + 0.5) puts each sample in the middle of its cell. sy is y<sub>s</sub>, the height of the source line, 10 px above the bottom edge. The outer loop runs over the sources, s = 0 … N − 1, so the code’s s is the note’s source index i less one, and sx = sources[s] × 800 is x<sub>i</sub> in px. The code’s x and y are not the coordinates of P but its offsets from the source, x − x<sub>i</sub> and y − y<sub>s</sub>; y² is computed once per row because it is the same for every column. r is r<sub>i</sub> in px. The “Now” value is r<sub>1</sub>, from the centre cell to the first source.',
            code: `var ⟦dx|dx = WORLD_W / cols⟧, dy = worldH / rows, sy = worldH - SOURCE_LIFT;
...
for (var s = 0; s < n; s++) {
var sx = sources[s] * WORLD_W, p = 0;
...
for (var j = 0; j < rows; j++) {
var y = (j + 0.5) * dy - sy, y2 = y * y;
for (var i = 0; i < cols; i++, p++) {
var x = (i + 0.5) * dx - sx;
var ⟦r|r = Math.sqrt(x * x + y2)⟧;`,
            syms: [
                ['dx', 'Δx', 'dx', 'width of one grid cell, px'],
                ['grid', 'cols × rows', 'cols, rows', 'grid cells across and down'],
                ['r', 'r<sub>1</sub>', 'r', 'centre cell to source 1, px']
            ]
        },
        {
            title: 'One ring: its phase kr and its height a',
            where: 'precompute(): the first line, and the innermost loop',
            math: '⟦k|k⟧ = ω / v = 2π / ⟦lam|λ⟧ &nbsp;&nbsp;(3)<br>ψ<sub>i</sub> = a<sub>i</sub> cos(⟦ph|k r<sub>i</sub>⟧ − ωt), &nbsp; a<sub>i</sub> = e<sup>−γ r<sub>i</sub>/R</sup> = e<sup>−⟦g|g⟧ r<sub>i</sub></sup>, &nbsp; R = 300 px &nbsp;&nbsp;(5)<br>code’s a: &nbsp;⟦a|a<sub>i</sub>/N⟧',
            note: 'k is the wave number of equation (3), in rad/px: the phase a ring gains per pixel of travel, one full turn 2π per wavelength. g is the attenuation per pixel, γ/R in 1/px. The Damping slider γ counts the factors of e that a ring loses over R = 300 px, so at the default γ = 0.15 a ring keeps e<sup>−0.15</sup> = 0.861 of its height after 300 px. The innermost line is equation (5) at one grid point: ph = k r is the phase lag kr<sub>i</sub> of ring i behind its source, in rad, and Math.exp(-g * r) is its height a<sub>i</sub>, without units. The code multiplies that height at once by norm = 1/N, the factor of equation (6) (step 4), so the code’s a is a<sub>i</sub>/N, not a<sub>i</sub>: it is the length of the arrow that source i contributes in equation (7). With the default two sources, the “Now” value of a is half the note’s a<sub>1</sub>. The constant −π/4 and the 1/√r fall-off of the true ring (4) are left out on purpose, as Section 3.1 of the note explains.',
            code: `var ⟦k|k⟧ = 2 * Math.PI / ⟦lam|lambda.value⟧, ⟦g|g = damp.value / R⟧;
...
var ⟦a|a = Math.exp(-g * r) * norm⟧, ⟦ph|ph = k * r⟧;`,
            syms: [
                ['lam', 'λ', 'lambda.value', 'wavelength, px'],
                ['k', 'k', 'k', 'wave number, rad/px'],
                ['g', 'g = γ/R', 'g', 'attenuation per pixel, 1/px'],
                ['ph', 'k r<sub>1</sub>', 'ph', 'phase lag of ring 1 at the centre cell, rad'],
                ['a', 'a<sub>1</sub>/N', 'a', 'height of ring 1 at the centre cell, already divided by N']
            ]
        },
        {
            title: 'Adding the rings: a sum of arrows',
            where: 'precompute(): the normalisation, the accumulation, the amplitude',
            math: 'ψ = (1/⟦N|N⟧) Σ<sub>i</sub> a<sub>i</sub> cos(k r<sub>i</sub> − ωt) &nbsp;&nbsp;(6)<br>U = (1/N) Σ<sub>i</sub> a<sub>i</sub> e<sup>ik r<sub>i</sub></sup> = ⟦C|C⟧ + i⟦S|S⟧, &nbsp; ⟦A|A⟧ = √(C² + S²) &nbsp;&nbsp;(7)',
            note: 'This is superposition, equation (6): the field is the sum of the rings, divided by the number of sources N so that the colours mean the same whatever N is. norm is 1/N; Math.max(1, n) only avoids a division by zero when the list is empty. Each ring is the real part of a turning arrow, and the page adds the arrows, not the waves. sumC and sumS are emptied before each rebuild. Then, for every source and every grid point p, the arrow of length a<sub>i</sub>/N (the code’s a) at the angle kr<sub>i</sub> (the code’s ph) is added component by component. After the last source, sumC[p] is C and sumS[p] is S of equation (7), the real and imaginary parts of U, both without units. ampl[p] is the amplitude A = |U|, how far point p can move up and down; it is zero on the calm lines. The page stores A as the map A of the data panel but does not draw it. Because every a<sub>i</sub> ≤ 1, |ψ| ≤ A ≤ 1.',
            code: `var ⟦N|n = sources.length⟧, ⟦norm|norm = 1 / Math.max(1, n)⟧;
...
sumC.fill(0);
sumS.fill(0);
...
⟦C|sumC[p] += a * Math.cos(ph)⟧;
⟦S|sumS[p] += a * Math.sin(ph)⟧;
...
for (p = 0; p < sumC.length; p++) ⟦A|ampl[p] = Math.sqrt(sumC[p] * sumC[p] + sumS[p] * sumS[p])⟧;`,
            syms: [
                ['N', 'N', 'n', 'number of sources'],
                ['norm', '1/N', 'norm', 'normalisation of equation (6)'],
                ['C', 'C', 'sumC[p]', 'real part of U at the centre cell'],
                ['S', 'S', 'sumS[p]', 'imaginary part of U at the centre cell']
            ]
        },
        {
            title: 'The speed of each ring',
            where: 'readouts(): the Speed readout',
            math: '⟦v|v⟧ = ω / k = ⟦f|f⟧ ⟦lam|λ⟧ &nbsp;&nbsp;(8)<br>ω = 2π f, &nbsp; T = 1 / f',
            note: 'A crest of ring i keeps kr<sub>i</sub> − ωt fixed, so it moves outward at dr/dt = ω/k = fλ, equation (8). The first line writes v = freq.value × lambda.value into the store, in px/s, together with ω = 2πf in rad/s and the period T = 1/f in s. The second line shows v, rounded, as the Speed readout beside the figure. At the defaults, 1.1 Hz × 30 px = 33 px/s, with one crest leaving each source every 0.909 s. This is the speed of each ring, not always of the crests you see: where two rings cross at an angle, the crests of their sum slide along faster, 1.55 v = 51 px/s straight up the middle between the two Reset sources (Section 4 of the note). readouts() runs whenever a slider moves, so the readout always follows f and λ.',
            code: `ds.set('v', ⟦f|freq.value⟧ * ⟦lam|lambda.value⟧); ds.set('omega', 2 * Math.PI * freq.value); ds.set('T', 1 / freq.value);
document.getElementById('r-v').textContent = Math.round(⟦v|ds.get('v')⟧) + ' px/s';`,
            syms: [
                ['f', 'f', 'freq.value', 'frequency, Hz'],
                ['lam', 'λ', 'lambda.value', 'wavelength, px'],
                ['v', 'v', "ds.get('v')", 'speed of each ring, px/s']
            ]
        },
        {
            title: 'Two maps and a turning phase',
            where: 'render(): every frame, the loop over grid points',
            math: '⟦psi|ψ⟧ = ⟦C|C⟧ ⟦c|cos ωt⟧ + ⟦S|S⟧ ⟦s|sin ωt⟧ &nbsp;&nbsp;(18)<br>C = (1/N) Σ<sub>i</sub> a<sub>i</sub> cos k r<sub>i</sub>, &nbsp; S = (1/N) Σ<sub>i</sub> a<sub>i</sub> sin k r<sub>i</sub>; &nbsp; ψ clipped to [−1, 1]',
            note: 'Expanding cos(kr<sub>i</sub> − ωt) = cos kr<sub>i</sub> cos ωt + sin kr<sub>i</sub> sin ωt splits space from time, equation (18). The split is exact, not an approximation, because every source shares the one ω. So the expensive part, one cosine and one sine per source per point, is done only in precompute() (step 4), when the sources, λ or γ change. On every frame the page takes one cosine and one sine of the shared phase, c = cos ωt and s = sin ωt from omegaT, and each grid point p then costs two multiplications and an addition, whatever N is. The code’s v here is the field ψ at point p, not the speed of step 5. It is clipped to [−1, 1], a guard against rounding only, since equation (6) already keeps |ψ| ≤ 1, and stored in psi[p], the map that the data panel reads and step 9 colours.',
            code: `var ⟦c|c = Math.cos(omegaT)⟧, ⟦s|s = Math.sin(omegaT)⟧, d = img.data;
...
for (var p = 0, q = 0; p < sumC.length; p++, q += 4) {
var ⟦psi|v⟧ = ⟦C|sumC[p]⟧ * c + ⟦S|sumS[p]⟧ * s;
if (v > 1) v = 1; else if (v < -1) v = -1;
psi[p] = v;`,
            syms: [
                ['C', 'C', 'sumC[p]', 'cosine map at the centre cell'],
                ['S', 'S', 'sumS[p]', 'sine map at the centre cell'],
                ['c', 'cos ωt', 'c', 'cosine of the shared phase'],
                ['s', 'sin ωt', 's', 'sine of the shared phase'],
                ['psi', 'ψ', 'v', 'field at the centre cell, between −1 and 1']
            ]
        },
        {
            title: 'The clock, and when the maps are rebuilt',
            where: 'Sim.clock callback, once per frame',
            math: '⟦wt|ωt⟧ ← ωt + 2π ⟦f|f⟧ Δt, &nbsp; Δt ≤ 0.05 s',
            note: 'This is the page’s whole time stepping, and it makes no error of its own: ψ depends on time only through ωt, so advancing the phase is all there is to do. Sim.clock calls the function once per frame with dt, the real time Δt in s since the last frame, capped at 0.05 s, and omegaT advances by 2πf Δt in rad. A 1.1 Hz setting therefore runs at 1.1 cycles per second on any screen that draws at least 20 frames a second; on a slower screen the waves run slow, but their shape is unchanged. While the page is paused, dt is 0 and nothing moves. omegaT grows without bound; only its cosine and sine are used (step 6). Before that, the dirty flag set by changed() (step 1) rebuilds the maps C and S once: 2NP cosines and sines for P grid points, 1 866 240 for Line of 16 on a wide screen, measured at 59–98 ms, against 0.9–1.6 ms for a frame.',
            code: `var clk = Sim.clock(function (dt, t) {
...
if (dirty) { precompute(); redraw = true; }
if (dt > 0 || redraw) {
⟦wt|omegaT⟧ += 2 * Math.PI * ⟦f|freq.value⟧ * dt;
ds.set('omegaT', omegaT);
render();`,
            syms: [
                ['f', 'f', 'freq.value', 'frequency, Hz'],
                ['wt', 'ωt', 'omegaT', 'shared phase, rad; grows without bound']
            ]
        },
        {
            title: 'The grid the maps live on',
            where: 'resize(): whenever the canvas changes size',
            math: 'cols = min(360, max(60, round(w / 1.1))), &nbsp; rows = max(30, round(cols · h / w))<br>field height = 800 px · h / w, &nbsp; ⟦dx|Δx⟧ = 800 px / cols',
            note: 'w and h are the canvas width and height in css pixels (box.w and box.h). The canvas gets about one column per 1.1 css pixels, at least 60 and at most 360, and rows in the same proportion as the canvas, so the cells are square. The field is always 800 px wide, so its height worldH follows from the shape of the canvas: 360.5 px on a wide screen, 800 px on a square phone canvas. Measured in headless Chromium, the grid is 360 × 162 = 58 320 points in windows 1280–1600 px wide and 324 × 324 = 104 976 on a phone 390 px wide. At the shortest wavelength, 16 px, Δx = 2.22 px gives 7.2 points per wavelength on the wide screen (6.48 on the phone), more than the two needed to show a wave at all. C, S and ψ are stored as 32-bit floats, about seven significant figures.',
            code: `⟦grid|cols⟧ = Math.max(60, Math.min(360, Math.round(box.w / 1.1)));
⟦grid|rows⟧ = Math.max(30, Math.round(cols * box.h / box.w));
worldH = WORLD_W * box.h / box.w;`,
            syms: [
                ['grid', 'cols × rows', 'cols, rows', 'grid cells across and down'],
                ['dx', 'Δx', 'dx', 'width of one grid cell, px']
            ]
        },
        {
            title: 'A number becomes a colour',
            where: 'the colour-table builder (once, at start-up) and render()',
            math: '⟦idx|n⟧ = round(127.5 ⟦psi|ψ⟧ + 127.5) ∈ {0, …, 255}<br>⟦rgb|c⟧ = c<sub>0</sub> + (c<sub>±</sub> − c<sub>0</sub>) |ψ|<sup>0.8</sup> &nbsp;&nbsp;(19)',
            note: 'Equation (19) is built once into a table of 256 colours. neg, mid and pos are c<sub>−</sub> ink, c<sub>0</sub> cream and c<sub>+</sub> burgundy, as red, green and blue from 0 to 255. Row i of the table stands for the field value ψ = i/127.5 − 1; the code calls that value a, which here has nothing to do with the height a of step 3. s = |ψ|<sup>0.8</sup> says how far from cream the colour lies, end picks c<sub>+</sub> for a crest and c<sub>−</sub> for a trough, and the inner line mixes the three channels. The power 0.8 lifts small values a little, so that the weak far field stays visible: ψ = 0.1 is drawn 0.158 of the way from cream. In render(), ψ (the code’s v) picks row n = round(127.5ψ + 127.5); idx is 3n, the place of that row in the flat table, and its three channels are copied into the image d. One step of the table is Δψ = 2/255 = 0.0078, so the picture carries ψ to about one part in 128, while the store keeps float32. Last, the image, one pixel per grid point, is stretched over the canvas with smoothing. This is where the drawing differs from the store: the store holds one value per cell, and a screen pixel between two cells shows a blend of both. The colours show the signed height at this instant, so a calm line stays cream in every frame and a loud band flickers between ink and burgundy once per period.',
            code: `var neg = [58, 50, 46], mid = [255, 250, 243], pos = [122, 31, 43];
for (var i = 0; i < 256; i++) {
var a = i / 127.5 - 1, s = Math.pow(Math.abs(a), 0.8), end = a < 0 ? neg : pos;
for (var c = 0; c < 3; c++) ⟦rgb|LUT[i * 3 + c] = Math.round(mid[c] + (end[c] - mid[c]) * s)⟧;
...
var ⟦idx|idx⟧ = Math.round(⟦psi|v⟧ * 127.5 + 127.5) * 3;
...
d[q] = LUT[idx];
d[q + 1] = LUT[idx + 1];
d[q + 2] = LUT[idx + 2];
...
octx.putImageData(img, 0, 0);
ctx.imageSmoothingEnabled = true;
ctx.imageSmoothingQuality = 'high';
ctx.drawImage(off, 0, 0, box.w, box.h);`,
            syms: [
                ['psi', 'ψ', 'v', 'field at the centre cell'],
                ['idx', 'n', 'idx / 3', 'row of the colour table at the centre cell'],
                ['rgb', 'c', 'LUT[idx … idx + 2]', 'colour drawn at the centre cell']
            ]
        }
    ]
};
