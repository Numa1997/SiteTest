/* From symbols to code, Fig. 1 (circular wave interference); loaded by sim.js from the page's data-walk key "circles".
   Each step pairs a numbered equation of the page's lecture note with the lines of this page's code that evaluate it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which the page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.circles = {
    intro: 'Nine steps from the lecture note to the pixels, in the note’s order: what the page remembers, the equations (2) to (8), how the page plays them from tables computed once on Kaggle, with two maps, a clock and a grid (18), and how a number becomes a colour (19). Each step sets a numbered equation of the note beside the lines of this page’s script that evaluate it; a line that is only “...” stands for page lines left out. Lengths are pixels of the field, which is always 800 px wide; times are seconds. The “Now” column is read live from the page’s data store at the centre cell of the grid, the same arrays the picture is drawn from. Two names differ from the note: the code counts the sources with s, because i and j count the columns and rows of the grid, and the code’s a is a stored height, counted in steps of 1/65535.',
    steps: [
        {
            title: 'The state: sources, sliders and one phase',
            where: 'top of the script, and the three sliders',
            math: 'state = { x<sub>1</sub>, …, x<sub>⟦N|N⟧</sub>; &nbsp;⟦lam|λ⟧, ⟦f|f⟧, γ; &nbsp;⟦wt|ωt⟧ }<br>x<sub>i</sub> = 800 px · u<sub>i</sub>; &nbsp; at the start u = (0.25, 0.75), ωt = 0',
            note: 'Nothing on this page is integrated step by step. Equation (6) gives the field at every point in closed form, so the page only has to remember what enters it: the list of source positions, the three slider values and the one phase ωt that all sources share. The first line fixes the scales of the model of Section 2: the field is 800 px wide (WORLD_W), the damping length R of equation (5) is 300 px, at most 24 sources are kept, and every source sits SOURCE_LIFT = 10 px above the bottom edge. DEFAULT is the initial condition, two sources at the fractions 0.25 and 0.75 of the width, that is x<sub>1</sub> = 200 px and x<sub>2</sub> = 600 px, the Reset pair of Section 5; omegaT = 0 starts the clock at ωt = 0. The sliders hold λ in px (lambda.value), f in Hz (freq.value) and the dimensionless γ (damp.value). Wavelength and Damping call changed(), which asks load() for the stored rings on either side of the slider’s wavelength and damping and rebuilds the maps of step 4 once they have arrived; Frequency calls only readouts(), because f enters only through ωt and never changes the shape of the pattern.',
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
            where: 'the model tools/sims/wave_interference2.py, and superpose(): the loops over sources, rows and columns',
            math: '⟦r|r<sub>i</sub>⟧ = √((x − x<sub>i</sub>)² + (y − y<sub>s</sub>)²) &nbsp;&nbsp;(2)<br>x − x<sub>i</sub> = m · 1.6 px, &nbsp; y − y<sub>s</sub> = (row from the bottom + ½) ⟦dx|Δx⟧ − 10 px, &nbsp; m = |2 · column + 1 − q|',
            note: 'Equation (2) is Pythagoras: the straight-line distance from source i to the point P = (x, y). The page no longer takes this square root. The grid is fixed: 250 columns of Δx = 3.2 px, and rows of the same height counted up from the bottom edge. A source sits on one of 501 places 1.6 px apart, q = 0 … 500, so the horizontal gap from column i to place q is |2i + 1 − q| half-cells, and the vertical gap of a row is the same for every source. Every distance that can occur is therefore one entry of a single table r(row, m), 250 × 500 numbers, which the model computed once on Kaggle and stored in two halves, dist_lo.bin (rows 0 to 124) and dist_hi.bin. In the code, q is the source’s place, jb is the grid row counted from the bottom, h picks the half that holds it, row is where that row starts in its half, and e is the entry for this source and this point. rr[e] is the distance r<sub>i</sub> in px; it is kept for the data panel, because the field itself needs only the angle and the height of step 3, which are stored at the same entry e. The “Now” value is r<sub>1</sub>, from the centre cell to the first source.',
            code: `var CELL = 3.2, NI = 250, NJ = 250, NM = 500, HALF = 125, PLACES = 500, PITCH = 1.6, TURN = 2 * Math.PI / 65536;
...
for (var s = 0; s < n; s++) {
var q = Math.round(sources[s] * PLACES), p = 0;
...
for (var j = 0; j < rows; j++) {
var jb = rows - 1 - j, h = jb < HALF ? 0 : 1, row = (jb - h * HALF) * NM, rr = RING.tab(0, h), A0 = RING.tab(1, h), A1 = RING.tab(2, h), H0 = RING.tab(3, h), H1 = RING.tab(4, h);
for (var i = 0; i < cols; i++, p++) {
var e = row + Math.abs(2 * i + 1 - q);
...
if (s === 0) { r1[p] = ⟦r|rr[e]⟧; a1[p] = a / 65535 * norm; ph1[p] = na * TURN; }`,
            syms: [
                ['dx', 'Δx', 'CELL', 'width of one grid cell, px'],
                ['grid', 'cols × rows', 'cols, rows', 'grid cells across and down'],
                ['r', 'r<sub>1</sub>', 'rr[e]', 'centre cell to source 1, px']
            ]
        },
        {
            title: 'One ring: its phase kr and its height a',
            where: 'superpose(): the stored rings and heights on either side of the sliders, read at entry e and blended',
            math: '⟦k|k⟧ = ω / v = 2π / ⟦lam|λ⟧ &nbsp;&nbsp;(3)<br>ψ<sub>i</sub> = a<sub>i</sub> cos(⟦ph|k r<sub>i</sub>⟧ − ωt), &nbsp; a<sub>i</sub> = e<sup>−γ r<sub>i</sub>/R</sup> = e<sup>−⟦g|g⟧ r<sub>i</sub></sup>, &nbsp; R = 300 px &nbsp;&nbsp;(5)<br>k r = (1 − t) k<sub>n</sub> r + t k<sub>n+1</sub> r, &nbsp; t = (k − k<sub>n</sub>) / (k<sub>n+1</sub> − k<sub>n</sub>)',
            note: 'k is the wave number of equation (3), in rad/px: the phase a ring gains per pixel of travel, one full turn 2π per wavelength. g is the attenuation per pixel, γ/R in 1/px. The Damping slider γ counts the factors of e that a ring loses over R = 300 px, so at γ = 0.15 a ring keeps e<sup>−0.15</sup> = 0.861 of its height after 300 px. Equation (5) was evaluated once on Kaggle, in double precision, at every entry of the distance table, for 118 wave numbers k<sub>n</sub> evenly spaced from 2π/64 to 2π/16 per px and for the dampings 0, 0.025, …, 0.6. Each value is stored as a whole number from 0 to 65535: the angle k r reduced to one turn in steps of 2π/65536, the height in steps of 1/65535. The angle k r grows in proportion to k, so for a wavelength between two stored ones it is exactly the straight-line blend of the two stored angles, with weight t; the nodes are close enough that the two never differ by half a turn or more, so the difference is taken the short way round, ((A1 − n0 + 32768) & 65535) − 32768, and Math.round puts the blend back on a whole step. The height is blended the same way with weight u; that blend is not exact, but off by at most 0.0011. A0, A1 are the stored angles and H0, H1 the stored heights on either side, na is the blended angle and a the blended height of ring i. The constant −π/4 and the 1/√r fall-off of the true ring (4) are left out on purpose, as Section 3.1 of the note explains.',
            code: `var t = RING.t, u = RING.u, cosT = G.cos, sy = worldH - SOURCE_LIFT;
ds.set('k', ⟦k|2 * Math.PI / RING.lam⟧); ds.set('g', ⟦g|RING.gam / R⟧); ds.set('lambda', ⟦lam|RING.lam⟧); ds.set('damp', RING.gam); ds.set('N', n); ds.set('norm', norm); ds.set('y_s', sy);
...
var n0 = A0[e], ⟦ph|na = (n0 + Math.round(t * (((A1[e] - n0 + 32768) & 65535) - 32768))) & 65535⟧, ⟦a|a = H0[e] + u * (H1[e] - H0[e])⟧;`,
            syms: [
                ['lam', 'λ', 'RING.lam', 'wavelength, px'],
                ['k', 'k', '2π / λ', 'wave number, rad/px'],
                ['g', 'g = γ/R', 'γ / R', 'attenuation per pixel, 1/px'],
                ['ph', 'k r<sub>1</sub>', 'na · 2π/65536', 'phase lag of ring 1 at the centre cell, reduced to one turn, rad'],
                ['a', 'a<sub>1</sub>/N', 'a / 65535 · norm', 'height of ring 1 at the centre cell, divided by N']
            ]
        },
        {
            title: 'Adding the rings: a sum of arrows',
            where: 'superpose(): the normalisation, the accumulation, the amplitude',
            math: 'ψ = (1/⟦N|N⟧) Σ<sub>i</sub> a<sub>i</sub> cos(k r<sub>i</sub> − ωt) &nbsp;&nbsp;(6)<br>U = (1/N) Σ<sub>i</sub> a<sub>i</sub> e<sup>ik r<sub>i</sub></sup> = ⟦C|C⟧ + i⟦S|S⟧, &nbsp; ⟦A|A⟧ = √(C² + S²) &nbsp;&nbsp;(7)',
            note: 'This is superposition, equation (6): the field is the sum of the rings, divided by the number of sources N so that the colours mean the same whatever N is. It is the one piece of arithmetic left to the page, because the reader chooses the sources and their combinations have no end. norm is 1/N; Math.max(1, n) only avoids a division by zero when the list is empty. Each ring is the real part of a turning arrow, and the page adds the arrows, not the waves. The arrow of ring i has the length a<sub>i</sub>/N and the angle kr<sub>i</sub>. Its two components come from a third stored table, cosT, the cosine of each of the 65536 angle steps in steps of 1/32767: cosT[na] is cos kr<sub>i</sub>, and the entry a quarter turn back, (na − 16384) & 65535, is sin kr<sub>i</sub>, because sin θ = cos(θ − π/2) (& 65535 wraps a negative step round the turn). w = (1/N)/(65535 × 32767) undoes both counts at once. After the last source, sumC[p] is C and sumS[p] is S of equation (7), without units. ampl[p] is the amplitude A = |U|, zero on the calm lines; the data panel shows it, the picture does not. Compared with the field computed straight from (6), as this page did before, C and S differ only by the rounding of the stored numbers and the height blend (the model measures it on Kaggle; see the page’s doc).',
            code: `var ⟦N|n = sources.length⟧, ⟦norm|norm = 1 / Math.max(1, n)⟧, w = norm / (65535 * 32767); if (rows > HALF * RING.np) { load(); return; }
...
sumC.fill(0);
sumS.fill(0);
...
⟦C|sumC[p] += a * cosT[na] * w⟧;
⟦S|sumS[p] += a * cosT[(na - 16384) & 65535] * w⟧;
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
            note: 'A crest of ring i keeps kr<sub>i</sub> − ωt fixed, so it moves outward at dr/dt = ω/k = fλ, equation (8). The first line writes v = freq.value × λ, the wavelength of the rings in use, into the store, in px/s, together with ω = 2πf in rad/s and the period T = 1/f in s. The second line shows v, rounded, as the Speed readout beside the figure. At the defaults, 1.1 Hz × 30 px = 33 px/s, with one crest leaving each source every 0.909 s. This is the speed of each ring, not always of the crests you see: where two rings cross at an angle, the crests of their sum slide along faster, 1.55 v = 51 px/s straight up the middle between the two Reset sources (Section 4 of the note). readouts() runs whenever a slider moves, so the readout always follows f and λ.',
            code: `ds.set('v', ⟦f|freq.value⟧ * ⟦lam|ds.get('lambda')⟧); ds.set('omega', 2 * Math.PI * freq.value); ds.set('T', 1 / freq.value);
document.getElementById('r-v').textContent = Math.round(⟦v|ds.get('v')⟧) + ' px/s';`,
            syms: [
                ['f', 'f', 'freq.value', 'frequency, Hz'],
                ['lam', 'λ', "ds.get('lambda')", 'wavelength, px'],
                ['v', 'v', "ds.get('v')", 'speed of each ring, px/s']
            ]
        },
        {
            title: 'Two maps and a turning phase',
            where: 'render(): every frame, the loop over grid points',
            math: '⟦psi|ψ⟧ = ⟦C|C⟧ ⟦c|cos ωt⟧ + ⟦S|S⟧ ⟦s|sin ωt⟧ &nbsp;&nbsp;(18)<br>C = (1/N) Σ<sub>i</sub> a<sub>i</sub> cos k r<sub>i</sub>, &nbsp; S = (1/N) Σ<sub>i</sub> a<sub>i</sub> sin k r<sub>i</sub>; &nbsp; ψ clipped to [−1, 1]',
            note: 'Expanding cos(kr<sub>i</sub> − ωt) = cos kr<sub>i</sub> cos ωt + sin kr<sub>i</sub> sin ωt splits space from time, equation (18). The split is exact, not an approximation, because every source shares the one ω. So the work per source, reading an angle and a height at every point, is done only in superpose() (step 4), when the sources, λ or γ change. On every frame the page takes one cosine and one sine of the shared phase, c = cos ωt and s = sin ωt from omegaT, and each grid point p then costs two multiplications and an addition, whatever N is. The code’s v here is the field ψ at point p, not the speed of step 5. It is clipped to [−1, 1], a guard against rounding only, since equation (6) already keeps |ψ| ≤ 1, and stored in psi[p], the map that the data panel reads and step 9 colours.',
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
            note: 'This is the page’s whole time stepping, and it makes no error of its own: ψ depends on time only through ωt, so advancing the phase is all there is to do. Sim.clock calls the function once per frame with dt, the real time Δt in s since the last frame, capped at 0.05 s, and omegaT advances by 2πf Δt in rad. A 1.1 Hz setting therefore runs at 1.1 cycles per second on any screen that draws at least 20 frames a second; on a slower screen the waves run slow, but their shape is unchanged. While the page is paused, dt is 0 and nothing moves. omegaT grows without bound; only its cosine and sine are used (step 6). Nothing at all is drawn until the stored files have arrived (RING, the rings in use, is still empty). After that, a change of the sources, λ or γ sets the dirty flag, and the maps C and S are rebuilt once from the stored tables: 4NP stored numbers read for P grid points, 1 808 000 for Line of 16 on a wide screen (P = 250 × 113), measured at 8–44 ms, against 0.6–0.7 ms for a frame.',
            code: `var clk = Sim.clock(function (dt, t) {
...
if (!RING) return;
if (dirty) { superpose(); redraw = true; }
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
            math: 'field height = 800 px · h / w, &nbsp; cols = 250, &nbsp; rows = min(250, ⌈field height / Δx⌉)<br>⟦dx|Δx⟧ = Δy = 800 px / 250 = 3.2 px',
            note: 'w and h are the canvas width and height in css pixels (box.w and box.h). The field is always 800 px wide, so its height worldH follows from the shape of the canvas: 360 px on a wide screen, 800 px on a square phone canvas. The grid is the one the stored tables were computed on, the same on every screen: 250 columns of 3.2 px, and as many rows of 3.2 px, counted up from the bottom edge, as it takes to reach the top, at most 250. Measured in headless Chromium: 250 × 113 = 28 250 points in windows 1100–1600 px wide (the top row is cut in part), 250 × 250 = 62 500 on a phone 390 px wide. At the shortest wavelength, 16 px, that is 5 points per wavelength, more than the two needed to show a wave at all. C, S and ψ are kept as 32-bit floats, about seven significant figures.',
            code: `worldH = WORLD_W * box.h / box.w;
⟦grid|cols = NI⟧;
⟦grid|rows = Math.min(NJ, Math.ceil(worldH / CELL - 1e-9))⟧;`,
            syms: [
                ['grid', 'cols × rows', 'cols, rows', 'grid cells across and down'],
                ['dx', 'Δx', 'dx', 'width of one grid cell, px']
            ]
        },
        {
            title: 'A number becomes a colour',
            where: 'the colour-table builder (once, at start-up) and render()',
            math: '⟦idx|n⟧ = round(127.5 ⟦psi|ψ⟧ + 127.5) ∈ {0, …, 255}<br>⟦rgb|c⟧ = c<sub>0</sub> + (c<sub>±</sub> − c<sub>0</sub>) |ψ|<sup>0.8</sup> &nbsp;&nbsp;(19)',
            note: 'Equation (19) is built once into a table of 256 colours. neg, mid and pos are c<sub>−</sub> ink, c<sub>0</sub> cream and c<sub>+</sub> burgundy, as red, green and blue from 0 to 255. Row i of the table stands for the field value ψ = i/127.5 − 1; the code calls that value a, which here has nothing to do with the height a of step 3. s = |ψ|<sup>0.8</sup> says how far from cream the colour lies, end picks c<sub>+</sub> for a crest and c<sub>−</sub> for a trough, and the inner line mixes the three channels. The power 0.8 lifts small values a little, so that the weak far field stays visible: ψ = 0.1 is drawn 0.158 of the way from cream. In render(), ψ (the code’s v) picks row n = round(127.5ψ + 127.5); idx is 3n, the place of that row in the flat table, and its three channels are copied into the image d. One step of the table is Δψ = 2/255 = 0.0078, so the picture carries ψ to about one part in 128, while the store keeps float32. Last, the image, one pixel per grid point, is stretched over the canvas with smoothing, its bottom row on the bottom edge. This is where the drawing differs from the store: the store holds one value per cell, and a screen pixel between two cells shows a blend of both. The colours show the signed height at this instant, so a calm line stays cream in every frame and a loud band flickers between ink and burgundy once per period.',
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
ctx.drawImage(off, 0, box.h - rows * CELL * box.w / WORLD_W, box.w, rows * CELL * box.w / WORLD_W);`,
            syms: [
                ['psi', 'ψ', 'v', 'field at the centre cell'],
                ['idx', 'n', 'idx / 3', 'row of the colour table at the centre cell'],
                ['rgb', 'c', 'LUT[idx … idx + 2]', 'colour drawn at the centre cell']
            ]
        }
    ]
};
