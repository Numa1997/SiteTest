/* From symbols to code — Fig. 8, draw and decompose.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live() in draw-decompose.html. */
window.WALK = window.WALK || {};

window.WALK.dft = {
    intro: 'Nine steps from a pen stroke to a chain of circles and the pixels that show it, in the order of the lecture note: the samples, the centre, the sums (4) and (7), the sort, Parseval (8) to (10), the clock and the chain (15), and the screen (16). Each step puts the note’s equation beside the lines of this page that compute it, and the table shows what those symbols hold now for the shape on screen. Draw something new and the numbers change.',
    steps: [
        {
            title: 'The stroke, resampled at equal arc length',
            where: 'end of the page script; the pointermove handler; resamp(pts, N)',
            math: 's<sub>i</sub> = Σ<sub>j≤i</sub> |p<sub>j</sub> − p<sub>j−1</sub>|, &nbsp; ⟦L|L⟧ = s<sub>last</sub>, &nbsp; ⟦ds|Δs⟧ = L / (⟦N|N⟧ − 1)<br>r<sub>n</sub> = the point a distance nΔs along the stroke, &nbsp; n = 0, 1, …, N − 1<br>t = 2πs / L, &nbsp; so t<sub>n</sub> ≈ 2πn / N &emsp; (sections 2 and 7)',
            note: 'The page starts with the Heart preset: SHAPES.heart() returns 1 201 points of a parametric heart, and play() sends them through the same pipeline as a drawing. When you draw, the pointermove handler keeps a pointer position only if it lies more than 0.006 units from the last one kept. The units are the page’s scale-free units, one unit being 0.46 of the shorter side of the figure. These points are the stroke points p<sub>j</sub> of the note.<br><br>In resamp() the first loop adds the length of each straight piece, Math.hypot of its x and y steps, to tot, and arcDistances keeps the running sum s<sub>i</sub>. After that loop tot is the total length L, stored as arcLen. The spacing Δs is step = tot / (N − 1) with N = NS = 256, so the last sample lands on the end of the stroke. For each sample number i (the note’s n), tgt = i · step is the distance wanted, the skipped lines find the straight piece that contains it, and res.push() places r<sub>n</sub> on that piece by linear interpolation.<br><br>Equal spacing makes the loop parameter t = 2πs/L of section 2 proportional to the distance travelled, so the bead, and later the pen, moves at constant speed. Because the spacing is L/(N − 1) and not L/N, the last sample repeats the first on a closed shape, and t<sub>n</sub> is very nearly, not exactly, 2πn/N (section 7.1).',
            code: `stroke = SHAPES.heart();
play(stroke, 'heart');
...
if (Math.hypot(p.x - l.x, p.y - l.y) > 0.006) draft.push(p);
...
⟦L|tot += Math.hypot(pts[i].x - pts[i - 1].x, pts[i].y - pts[i - 1].y)⟧;
arcDistances.push(tot);
...
var ⟦ds|step = tot / (N - 1)⟧, res = [{ x: pts[0].x, y: pts[0].y }], j = 0;
for (i = 1; i < ⟦N|N⟧; i++) {
    var tgt = i * step;
    ...
    res.push({ x: pts[j].x + f * (pts[j + 1].x - pts[j].x), y: pts[j].y + f * (pts[j + 1].y - pts[j].y) });
}
⟦L|arcLen = tot⟧;`,
            syms: [
                ['src', 'shape', 'source', 'the stroke being decomposed: a preset or your drawing'],
                ['N', 'N', 'NS', 'number of samples'],
                ['L', 'L', 'arcLen (tot in resamp())', 'length of the stroke; units'],
                ['ds', 'Δs', 'step', 'arc length between neighbouring samples; units']
            ]
        },
        {
            title: 'Centring: c₀ and the mean squared radius',
            where: 'decompose(pts, name)',
            math: '⟦mx|x̄⟧ + i⟦my|ȳ⟧ = (1/N) Σ<sub>n</sub> r<sub>n</sub>, &nbsp; ⟦z0|z<sub>n</sub>⟧ = x<sub>n</sub> + iy<sub>n</sub> = r<sub>n</sub> − (x̄ + iȳ)<br>⟦E|⟨|z|²⟩⟧ = (1/N) Σ<sub>n</sub> |z<sub>n</sub>|² &emsp; (8), left side',
            note: 'The term with k = 0 is the circle that does not turn. By (3), c<sub>0</sub> is the average of z over one loop, the centre of mass of the uniform wire of section 1. The page uses the finite sample mean instead. The first two lines add up the resampled points r<sub>n</sub> (r is the array that resamp() returned), and dividing by NS = N gives meanX = x̄ and meanY = ȳ, in units. This approximates the wire’s centre of mass but is not equal to it, because the resampling repeats the endpoint (sections 2 and 7.1).<br><br>The samples line subtracts the mean from every point, so samples[n] is the centred z<sub>n</sub> = x<sub>n</sub> + iy<sub>n</sub> that every later step uses. Its mean is zero, so c<sub>0</sub> = 0 and the transform can skip k = 0.<br><br>The last three lines add x<sub>n</sub>² + y<sub>n</sub>² over the samples and divide by N: meanZ2 is ⟨|z|²⟩, the left side of Parseval’s theorem (8), in square units. For equal point masses at the centred samples it is exactly their moment of inertia divided by their total mass, I/m, and only approximately that of a uniform wire. The circles share this quantity out between them (step 5).',
            code: `meanX = 0; meanY = 0;
r.forEach(function (p) { meanX += p.x; meanY += p.y; });
⟦mx|meanX /= NS⟧; ⟦my|meanY /= NS⟧;
⟦z0|samples⟧ = r.map(function (p) { return { x: p.x - meanX, y: p.y - meanY }; });
meanZ2 = 0;
samples.forEach(function (p) { meanZ2 += p.x * p.x + p.y * p.y; });
⟦E|meanZ2 /= NS⟧;`,
            syms: [
                ['mx', 'x̄', 'meanX', 'mean x of the resampled points r<sub>n</sub>, before centring; units'],
                ['my', 'ȳ', 'meanY', 'mean y of the same points; units'],
                ['z0', 'z<sub>0</sub>', 'samples[0]', 'the first centred sample, x<sub>0</sub> + iy<sub>0</sub>; units'],
                ['E', '⟨|z|²⟩', 'meanZ2', 'mean squared distance of the samples from the centre, I/m of equal masses at the samples; square units']
            ]
        },
        {
            title: 'Each circle is an average: the sums (4) and (7)',
            where: 'dft(z), called as dft(samples) in decompose()',
            math: 'c<sub>k</sub> = (1/N) Σ<sub>n=0</sub><sup>N−1</sup> z<sub>n</sub> e<sup>−2πikn/N</sup>, &nbsp; −60 ≤ ⟦k1|k⟧ ≤ 60, &nbsp; k ≠ 0 &emsp; (4)<br>⟦re|Re c<sub>k</sub>⟧ = (1/N) Σ<sub>n</sub> (x<sub>n</sub> cos a<sub>n</sub> + y<sub>n</sub> sin a<sub>n</sub>)<br>⟦im|Im c<sub>k</sub>⟧ = (1/N) Σ<sub>n</sub> (y<sub>n</sub> cos a<sub>n</sub> − x<sub>n</sub> sin a<sub>n</sub>), &nbsp; a<sub>n</sub> = 2πkn/N &emsp; (7)',
            note: 'Section 3 says why one coefficient is an average. Turn the picture backwards at k turns per loop, which is what multiplying by e<sup>−ikt</sup> does, and the circle that turns at that rate stands still, while every other circle points in all directions equally often and averages away: that is (2) and (3). A computer replaces the integral (3) by the sum (4) over the N samples.<br><br>In dft(), z is the array samples, z[n].x and z[n].y are x<sub>n</sub> and y<sub>n</sub> in units, and N = z.length = 256. The outer loop runs over the frequencies k from −KMAX = −60 to 60 and skips k = 0, which gives the 120 coefficients. Staying far below N/2 = 128 keeps each computed coefficient close to the true one; the small difference is the aliases of (6).<br><br>Inside, a = TAU · k · n / N is the angle a<sub>n</sub> of (7) in radians, and c and s are its cosine and sine (this c is cos a<sub>n</sub>, not a coefficient). Since e<sup>−ia</sup> = cos a − i sin a, the product z<sub>n</sub> e<sup>−ia<sub>n</sub></sup> has the real part x<sub>n</sub> cos a<sub>n</sub> + y<sub>n</sub> sin a<sub>n</sub> and the imaginary part y<sub>n</sub> cos a<sub>n</sub> − x<sub>n</sub> sin a<sub>n</sub>. The two += lines add exactly these, the two lines of (7), and dividing by N finishes the average: 120 × 256 = 30 720 complex products, once per shape. The table shows the coefficient that the sort of step 4 puts first.',
            code: `var N = z.length, out = [];
for (var ⟦k1|k⟧ = -KMAX; k <= KMAX; k++) {
    if (k === 0) continue;
    var re = 0, im = 0;
    for (var n = 0; n < N; n++) {
        var a = TAU * k * n / N, c = Math.cos(a), s = Math.sin(a);
        ⟦re|re += z[n].x * c + z[n].y * s⟧;
        ⟦im|im += z[n].y * c - z[n].x * s⟧;
    }
    ⟦re|re /= N⟧;
    ⟦im|im /= N⟧;`,
            syms: [
                ['tot', 'number of c<sub>k</sub>', 'coefs.length', 'coefficients computed, for −60 ≤ k ≤ 60 without 0'],
                ['k1', 'k', 'coefs[0].k', 'turns per loop of the largest circle; negative is clockwise'],
                ['re', 'Re c<sub>k</sub>', 'coefs[0].re', 'real part of the largest coefficient; units'],
                ['im', 'Im c<sub>k</sub>', 'coefs[0].im', 'imaginary part of the largest coefficient; units']
            ]
        },
        {
            title: 'One circle per coefficient, sorted by size',
            where: 'dft(z), the end; decompose() sets the K slider',
            math: 'c<sub>k</sub> = ⟦A||c<sub>k</sub>|⟧ e<sup>i ⟦ph|arg c<sub>k</sub>⟧</sup>, &nbsp; |c<sub>k</sub>| = √((Re c<sub>k</sub>)² + (Im c<sub>k</sub>)²), &nbsp; arg c<sub>k</sub> = atan2(Im c<sub>k</sub>, Re c<sub>k</sub>)<br>sort by |c<sub>k</sub>|, largest first; the first ⟦K|K⟧ form the set S &emsp; (box under (9))',
            note: 'Section 2 writes each coefficient in polar form, c<sub>k</sub> = |c<sub>k</sub>| e<sup>i arg c<sub>k</sub></sup>, so that its term c<sub>k</sub> e<sup>ikt</sup> = |c<sub>k</sub>| e<sup>i(kt + arg c<sub>k</sub>)</sup> is an arm of length |c<sub>k</sub>| that starts at the angle arg c<sub>k</sub> and turns k times per loop, anticlockwise for k &gt; 0 and clockwise for k &lt; 0. The push line stores both forms: amp = Math.hypot(re, im) is the radius |c<sub>k</sub>| in units, and phase = Math.atan2(im, re) is the starting angle arg c<sub>k</sub> in radians, between −π and π.<br><br>The sort orders the 120 circles by radius, largest first, and decompose() keeps the sorted list as coefs, so the index into coefs is the rank. The K slider gets coefs.length = 120 as its maximum, and K.set keeps its value in range.<br><br>The box under (9) says why largest first: by (9) the squared error is the sum of the squared radii left out, so among the 120 circles the page computes, the K largest come closest to the samples in the least-squares sense. This is not a search over all 256 DFT bins. Each coefficient was computed on its own (section 3), so changing K recomputes no coefficient; it only decides how many of this fixed list are drawn.',
            code: `out.push({ k: k, re: re, im: im, ⟦A|amp: Math.hypot(re, im)⟧, ⟦ph|phase: Math.atan2(im, re)⟧ });
}
return out.sort(function (a, b) { return b.amp - a.amp; });
...
coefs = dft(samples);
...
K.el.max = coefs.length;
⟦K|K.set(Math.min(K.value, coefs.length))⟧;`,
            syms: [
                ['A', '|c<sub>k</sub>|', 'coefs[0].amp', 'radius of the largest circle; units'],
                ['ph', 'arg c<sub>k</sub>', 'coefs[0].phase', 'its starting angle; rad'],
                ['k1', 'k', 'coefs[0].k', 'its turns per loop'],
                ['K', 'K', 'K.value', 'circles in use, the size of the set S'],
                ['tot', 'number of c<sub>k</sub>', 'coefs.length', 'circles to choose from']
            ]
        },
        {
            title: 'Parseval: the share the K circles carry',
            where: 'rebuild(), run whenever K or the shape changes',
            math: '⟦E|⟨|z|²⟩⟧ = (1/N) Σ<sub>n</sub> |z<sub>n</sub>|² = Σ<sub>k</sub> |c<sub>k</sub>|² &emsp; (8)<br>share kept = ⟦cap|Σ<sub>k∈S</sub> |c<sub>k</sub>|² / ⟨|z|²⟩⟧, &nbsp; with ⟦kept|Σ<sub>k∈S</sub> |c<sub>k</sub>|²⟧ over the ⟦K|K⟧ largest &emsp; (10)',
            note: 'Square the discrete series and average it over the samples: every cross term between two different frequencies vanishes by (5), and what is left is Parseval’s theorem (8). The mean squared radius ⟨|z|²⟩ of step 2 splits into one share |c<sub>k</sub>|² per circle, with no cross terms; acoustics and optics call the same bookkeeping energy. The sum in (8) runs over N = 256 neighbouring frequencies, and the page computes only the 120 with 0 &lt; |k| ≤ 60, which is why even K = 120 does not reach 100 %.<br><br>In rebuild(), n is the number of circles K read from the slider, and the loop adds the squared radii of ranks 0 to n − 1. Those ranks are the set S, so kept is Σ<sub>k∈S</sub> |c<sub>k</sub>|² in square units. The last line stores kept and the share 100 · kept / meanZ2 in percent, the panel’s readout “⟨|z|²⟩ kept”.<br><br>The share is not the error: by (10) the relative RMS error is the square root of one minus the share. For the heart one circle keeps 94.3 %, yet the relative error is √0.057 = 24 %.',
            code: `var ⟦K|n = K.value⟧, i;
kept = 0;
for (i = 0; i < n; i++) ⟦kept|kept += coefs[i].amp * coefs[i].amp⟧;
...
ds.set('K', n); ds.set('kept', kept); ds.set('errP', errP); ds.set('err', err); ⟦cap|ds.set('cap', 100 * kept / meanZ2)⟧;`,
            syms: [
                ['K', 'K', 'n = K.value', 'circles kept'],
                ['kept', 'Σ<sub>k∈S</sub> |c<sub>k</sub>|²', 'kept', 'squared radii of the kept circles, added; square units'],
                ['E', '⟨|z|²⟩', 'meanZ2', 'the whole they share, from step 2; square units'],
                ['cap', 'share kept', '100 * kept / meanZ2', 'the share, in percent']
            ]
        },
        {
            title: 'The error, predicted and measured: equation (9)',
            where: 'rebuild(), continued',
            math: '⟦err|e<sub>K</sub>⟧² = (1/N) Σ<sub>n</sub> |z<sub>n</sub> − z̃<sub>n</sub>|², &nbsp; z̃<sub>n</sub> = Σ<sub>k∈S</sub> c<sub>k</sub> e<sup>2πikn/N</sup><br>e<sub>K</sub>² = Σ<sub>k∉S</sub> |c<sub>k</sub>|² = ⟨|z|²⟩ − Σ<sub>k∈S</sub> |c<sub>k</sub>|², &nbsp; so &nbsp; ⟦errP|e<sub>K</sub> = √(⟨|z|²⟩ − Σ<sub>k∈S</sub> |c<sub>k</sub>|²)⟧ &emsp; (9)',
            note: 'The difference between the samples and the redrawn curve is the sum of the dropped circles, so Parseval (8) applied to that difference gives (9): the squared RMS error at the samples equals the sum of the squared radii left out. The page computes this number by two independent routes.<br><br>The first line is the prediction: errP is the square root of meanZ2 − kept, that is √(⟨|z|²⟩ − Σ<sub>k∈S</sub> |c<sub>k</sub>|²), and Math.max(0, …) stops rounding from making the difference slightly negative.<br><br>The loop is the measurement. For every sample number i (the note’s n) chainAt() evaluates the K-term series at the sample’s parameter t<sub>n</sub> = 2πn/N, which is z̃<sub>n</sub>, with the same arm sum that draws the pen (step 7). The next line adds the squared distance |z<sub>n</sub> − z̃<sub>n</sub>|² to e2, and the skipped lines store z̃<sub>n</sub> and the distance itself. Dividing by NS and taking the root gives err = e<sub>K</sub> in units.<br><br>When the two readouts agree, the transform, the sort and the reconstruction are all right. For the default heart they agree to within 3 parts in 10<sup>10</sup> for every K, and the rest comes from subtracting two nearly equal numbers in (9). The RMS compares sample n with the series at the same parameter; it says nothing about the curve between the samples, where a truncated series can overshoot (section 6.2).',
            code: `⟦errP|errP = Math.sqrt(Math.max(0, meanZ2 - kept))⟧;
var e2 = 0;
...
for (i = 0; i < NS; i++) {
    var z = chainAt(TAU * i / NS, n);
    e2 += Math.pow(z.x - samples[i].x, 2) + Math.pow(z.y - samples[i].y, 2);
    ...
}
⟦err|err = Math.sqrt(e2 / NS)⟧;`,
            syms: [
                ['errP', 'e<sub>K</sub> (Parseval)', 'errP', 'RMS error predicted from the dropped squared radii; units'],
                ['err', 'e<sub>K</sub> (measured)', 'err', 'RMS distance between the samples and the K-term series; units'],
                ['kept', 'Σ<sub>k∈S</sub> |c<sub>k</sub>|²', 'kept', 'from step 5; square units'],
                ['E', '⟨|z|²⟩', 'meanZ2', 'from step 2; square units']
            ]
        },
        {
            title: 'The clock and the chain: equation (15)',
            where: 'the Sim.clock callback; chainAt(time, n)',
            math: '⟦t|t⟧ ← t + 2π Δt / ⟦tl|T<sub>loop</sub>⟧, &emsp; z(t) = Σ<sub>rank &lt; ⟦K|K⟧</sub> |c<sub>k</sub>| e<sup>i(kt + arg c<sub>k</sub>)</sup> = ⟦x|x⟧ + i⟦y|y⟧ &emsp; (15)<br>arm j: θ<sub>j</sub> = k<sub>j</sub> t + arg c<sub>k<sub>j</sub></sub>, &nbsp; |c<sub>k<sub>j</sub></sub>| (cos θ<sub>j</sub> + i sin θ<sub>j</sub>) &emsp; (Figure 1)',
            note: 'Every frame the clock hands over dt, the real time since the last frame in seconds, at most 0.05 s and 0 while paused: this is the Δt of (15). The first line inside the test advances the loop parameter t, in radians, by 2π · dt / loop.value, where loop.value is T<sub>loop</sub>, the Time per loop slider in seconds (12 s by default). So t is not a clock reading; it grows by 2π in every loop.<br><br>chainAt(t, K.value) then evaluates the sum (15) in closed form. Its loop walks the sorted coefs by rank i from 0 to K − 1. For each circle, ang = k · t + arg c<sub>k</sub> is the arm’s angle θ<sub>j</sub> of Figure 1 in radians, vx and vy are the arm |c<sub>k</sub>|(cos θ<sub>j</sub>, sin θ<sub>j</sub>) in units, and x and y add the arms tip to tail. Each partial sum is a joint of the chain, and the last one, x + iy, is the pen.<br><br>Nothing is integrated, so no error builds up: after every loop the pen returns to the same place. Fig. 7 runs the same sum with circles you choose by hand; here the transform has chosen them. The trail line keeps the pen position and its t at the end of each frame, the history the burgundy trail is drawn from (step 9).',
            code: `if (mode === 'play' && dt > 0) {
    ⟦t|t⟧ += TAU * dt / ⟦tl|loop.value⟧;
    var z = chainAt(t, ⟦K|K.value⟧);
    trail.push({ x: z.x, y: z.y, t: t });
...
for (var i = 0; i < n; i++) {
    var c = coefs[i], ang = c.k * time + c.phase;
    var vx = c.amp * Math.cos(ang), vy = c.amp * Math.sin(ang);
    ⟦x|x += vx⟧;
    ⟦y|y += vy⟧;
    ...`,
            syms: [
                ['t', 't', 't', 'loop parameter, 2π per loop; rad'],
                ['tl', 'T<sub>loop</sub>', 'loop.value', 'time per loop; s'],
                ['K', 'K', 'K.value', 'number of arms in the chain'],
                ['x', 'x', 'z.x', 'the pen, real part; units'],
                ['y', 'y', 'z.y', 'the pen, imaginary part; units']
            ]
        },
        {
            title: 'From units to pixels: equation (16)',
            where: 'rebuild(), the outer radius; S(), viewScale() and the clock; line() and draw()',
            math: 'pixels per unit = 0.46 min(w, h) / max(1, R<sub>view</sub>) × zoom &emsp; (16)<br>R = max( max<sub>n</sub> |z<sub>n</sub>|, max over the loop of |joint| + ⟦A||c<sub>k</sub>|⟧ ); &nbsp; R<sub>view</sub> jumps up to R and relaxes down with a time constant of 0.4 s<br>on screen: (c<sub>x</sub> + ⟦x|x⟧ · scale, c<sub>y</sub> − ⟦y|y⟧ · scale) in CSS pixels',
            note: 'The coefficients live in scale-free units, one unit being 0.46 of the shorter side of the figure at zoom 1, with y pointing up (section 8). After each rebuild the page finds the outermost point that will be drawn over a whole loop, extR, the R of section 8. The first quoted line takes the farthest centred sample from the origin. The second, inside a loop over 256 instants and all K circles, takes the distance of each circle’s centre, a joint of the chain, from the origin plus that circle’s radius.<br><br>S() is 0.46 · min(w, h) with box.w and box.h the figure’s size in CSS pixels, the pixels per unit at zoom 1, and viewScale() divides it by max(1, viewR) and multiplies by zoom, which is (16). The two clock lines make viewR, the R<sub>view</sub> of (16), follow R: it jumps up at once when R grows, and when you lower K it moves down by the fraction 1 − e<sup>−Δt/(0.4 s)</sup> of the gap each frame. At zoom 1 nothing leaves the figure, but the stored scale is therefore a smoothed quantity, not a formula of the current frame.<br><br>The last two lines turn a point in units into a screen point in CSS pixels, for every curve and for every arm: x times the scale is added to the position cx of the origin, and y times the scale is subtracted from cy, because screen y grows downwards while the note’s y points up. The origin sits at the centre of the figure unless you pan or switch on Follow the pen. Zoom and pan change only the view, never the coefficients.',
            code: `samples.forEach(function (p) { extR = Math.max(extR, Math.hypot(p.x, p.y)); });
...
extR = Math.max(extR, Math.hypot(jx, jy) + ⟦A|cm.amp⟧);
...
function S() { return Math.min(box.w, box.h) * 0.46; }
...
function viewScale() { return S() / Math.max(1, viewR) * zoom; }
...
if (extR > viewR) viewR = extR;
else viewR += (extR - viewR) * (1 - Math.exp(-real / 0.4));
...
var px = cx + pts[i].x * s, py = cy - pts[i].y * s;
...
var nx = ox + p.vx * s, ny = oy - p.vy * s;`,
            syms: [
                ['x', 'x', 'cur.x', 'the pen, real part, in units; drawn at cx + x · scale px'],
                ['y', 'y', 'cur.y', 'the pen, imaginary part, in units; drawn at cy − y · scale px'],
                ['A', '|c<sub>k</sub>|', 'coefs[0].amp', 'radius of the largest circle in units; on screen p.amp · s px']
            ]
        },
        {
            title: 'What is drawn: trail, circles and Fig. 8b',
            where: 'draw(), the trail and the arm loop; spectrum()',
            math: 'trail: the pen at the end of each frame over the last 0.98 of a loop, 24 pieces, opacity 0.16 … 1<br>circle j: radius |c<sub>k<sub>j</sub></sub>| × scale about joint j − 1, drawn if larger than 1.5 px<br>Fig. 8b: stem at k, height ∝ |c<sub>k</sub>| / ⟦A|max |c<sub>k</sub>|⟧, burgundy if rank &lt; ⟦K|K⟧, tan if not &emsp; (section 8)',
            note: 'The trail is history, not a formula. Each frame of step 7 pushed the pen position with its t, and the while line drops points older than 0.98 of a loop, so the trail never quite closes on itself. It is drawn in nseg = 24 pieces, and the globalAlpha line gives piece c the opacity 0.12 + 0.88 (c + 1)/24, from 0.16 for the oldest to 1 for the newest, so the trail fades with age.<br><br>Each rose circle is drawn about its joint with the radius p.amp · s, that is |c<sub>k</sub>| times the scale of step 8, in CSS pixels, but only when that radius exceeds 1.5 px: the smallest circles are in the store and in the sum, they are only not outlined.<br><br>In Fig. 8b, max is the largest radius, coefs[0].amp after the sort. A stem’s x places it at its frequency k, mapped from −60 … 60 onto the panel width w less 18 px of padding on each side, and its top y lies |c<sub>k</sub>| / max · (base − 10) px above the base line, so the largest circle always reaches the top. The colour line paints the first K ranks burgundy, the circles in use, and the rest tan. The dashed original and the pink full curve are the stored z<sub>n</sub> and 601 points of the K-term series, joined by straight lines with line() of step 8.',
            code: `while (trail.length && trail[0].t < t - TAU * 0.98) trail.shift();
...
ctx.globalAlpha = 0.12 + 0.88 * (c + 1) / nseg;
...
if (swCircles.checked && p.amp * s > 1.5) {
    ...
    ctx.arc(ox, oy, p.amp * s, 0, TAU);
...
var ⟦A|max = coefs[0].amp || 1⟧, ⟦K|n = K.value⟧;
...
var x = pad + (c.k + KMAX) / (2 * KMAX) * (w - 2 * pad), y = base - c.amp / max * (base - 10);
...
sctx.strokeStyle = rank < n ? T.accent : T.tanInk;`,
            syms: [
                ['A', 'max |c<sub>k</sub>|', 'max = coefs[0].amp', 'the largest radius, the full height of Fig. 8b; units'],
                ['K', 'K', 'n = K.value', 'stems drawn burgundy'],
                ['k1', 'k', 'coefs[0].k', 'position of the tallest stem'],
                ['tot', 'number of c<sub>k</sub>', 'coefs.length', 'stems in Fig. 8b']
            ]
        }
    ]
};
