/* From symbols to code — Fig. 7, phasor sums.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live() in phasor-sums.html. Values for "arm 1" refer to the first circle card. */
window.WALK = window.WALK || {};

window.WALK.phasors = {
    intro: 'Thirteen steps through the model of the lecture note, in its order: the list of circles, one arm (5), the sum (6), the period (12), the symmetry (13), the average size (14) and (15), the clock, the sampled final shape and its morph (16), the scale (17), the pixels, and the music. Each step sets an equation of the note beside the lines of this page that evaluate it. The Now column reads the store of the running figure; values for arm 1 belong to Circle 1.',
    steps: [
        {
            title: 'The state: a list of circles',
            where: 'the preset table, wrap(), the slider handler, edited() and load() · note section 3',
            math: 'state: ⟦N|N⟧ triples (⟦A|A<sub>k</sub>⟧, ⟦w|ω<sub>k</sub>⟧, ⟦ph|φ<sub>k</sub>⟧), &nbsp; k = 1, …, N, &nbsp; 0 ≤ φ<sub>k</sub> &lt; 2π<br>initial condition: ⟦t|t⟧ = 0',
            note: 'Before anything moves, the figure is a list. Each circle card holds one triple: the radius A<sub>k</sub>, a pure number because the plot is scaled to fit (step 10), the angular frequency ω<sub>k</sub> in rad/s and the phase φ<sub>k</sub> in rad. In the code the list is the array <code>phasors</code>, and arm k is <code>phasors[k]</code> with the fields <code>amp</code>, <code>freq</code> and <code>phase</code>. A preset is a list of such triples. <code>load()</code> copies it and folds every phase into 0 ≤ φ &lt; 2π with <code>wrap()</code>, so the −π/2 of the 3-petal rose becomes 3π/2 = 4.712 rad, the same direction; then <code>edited()</code> sets the clock back to t = 0 s and empties the trail. Moving a slider writes the new number into the same triple and calls <code>edited()</code> as well. The page opens on the 3-petal rose. Nothing else is state: the position of the pen is not carried from one frame to the next, it is computed afresh from this list and t.',
            code: `rose3: [[1, 4, -PI / 2], [1, -2, PI / 2]],
...
function wrap(v) { return ((v % TAU) + TAU) % TAU; }
...
p[el.dataset.f] = parseFloat(el.value);
...
function edited(snap) {
    trail = [];
    ⟦t|t = 0⟧;
    refinal(snap);
    formula();
    readouts();
}
function load(list) {
    ⟦N|phasors⟧ = list.map(function (p, i) {
        return { ⟦A|amp: p[0]⟧, ⟦w|freq: p[1]⟧, ⟦ph|phase: wrap(p[2] || 0)⟧, color: COLS[i % COLS.length], curve: p[3] || 'Linear' };
    });
    renderList();
    edited(true);
}
...
load(PRESETS.rose3);`,
            syms: [
                ['N', 'N', 'phasors.length', 'number of circle cards'],
                ['A', 'A<sub>1</sub>', 'phasors[0].amp', 'stored radius of arm 1, no unit'],
                ['w', 'ω<sub>1</sub>', 'phasors[0].freq', 'angular frequency of arm 1, rad/s'],
                ['ph', 'φ<sub>1</sub>', 'phasors[0].phase', 'phase of arm 1 at t = 0, rad'],
                ['t', 't', 't', 'phasor time, s; 0 after every edit, then advanced by the clock (step 7)']
            ]
        },
        {
            title: 'One arm: a phasor',
            where: 'sumAt(), the loop over the arms · note (5), section 2.3',
            math: 'z<sub>1</sub>(t) = ⟦Ar|A<sub>1</sub>⟧ e<sup>i⟦ang|(ω<sub>1</sub>t + φ<sub>1</sub>)⟧</sup> = ⟦x1|A<sub>1</sub> cos(ω<sub>1</sub>t + φ<sub>1</sub>)⟧ + i ⟦y1|A<sub>1</sub> sin(ω<sub>1</sub>t + φ<sub>1</sub>)⟧ &emsp;(5)',
            note: 'Equation (5) is one arm on its own. Euler’s formula (3) splits the turning arrow into two real numbers, and these are what the computer works with: the reach to the right, A cos θ, and the reach up, A sin θ, of the tip of the arm, measured from the joint it turns about. The angle θ = ωt + φ grows at a steady ω radians per second from φ at t = 0; that steady growth is all that uniform circular motion means. In the code <code>ang</code> is θ<sub>k</sub> in rad, <code>p.freq</code> is ω<sub>k</sub> in rad/s, <code>time</code> is t in s and <code>p.phase</code> is φ<sub>k</sub> in rad; <code>vx</code> and <code>vy</code> are the real and the imaginary part of the arm. The angles are also written into the array the caller hands in, which is where the Now column reads θ<sub>1</sub>. In the Live view the list handed to <code>sumAt()</code> is the drawn copy of step 13, so <code>p.amp</code> is A′<sub>1</sub>; with Auto Dance off A′<sub>1</sub> = A<sub>1</sub> exactly, and the x of arm 1 below equals A<sub>1</sub> cos θ<sub>1</sub> from the two rows above it.',
            code: `function sumAt(time, list, angles) {
...
    for (var k = 0; k < list.length; k++) {
        var p = list[k];
        var ⟦ang|ang⟧ = ⟦w|p.freq⟧ * ⟦t|time⟧ + ⟦ph|p.phase⟧;
        if (angles) angles[k] = ang;
        var ⟦x1|vx⟧ = ⟦Ar|p.amp⟧ * Math.cos(ang), ⟦y1|vy⟧ = p.amp * Math.sin(ang);`,
            syms: [
                ['Ar', 'A<sub>1</sub>', 'p.amp', 'radius of arm 1 as drawn (A′<sub>1</sub> of step 13); equals the stored A<sub>1</sub> while Auto Dance is off'],
                ['w', 'ω<sub>1</sub>', 'p.freq', 'angular frequency of arm 1, rad/s'],
                ['ph', 'φ<sub>1</sub>', 'p.phase', 'phase of arm 1, rad'],
                ['t', 't', 'time', 'phasor time, s'],
                ['ang', 'ω<sub>1</sub>t + φ<sub>1</sub>', 'ang', 'angle of arm 1 now, rad, not wrapped'],
                ['x1', 'Re z<sub>1</sub>', 'vx', 'reach of arm 1 to the right'],
                ['y1', 'Im z<sub>1</sub>', 'vy', 'reach of arm 1 upward']
            ]
        },
        {
            title: 'Tip to tail: the sum',
            where: 'sumAt(), the running sum; draw(), the call for this frame · note (6), section 3',
            math: '⟦x|x⟧ + i⟦y|y⟧ = z(t) = Σ<sub>k=1</sub><sup>⟦N|N⟧</sup> A<sub>k</sub> e<sup>i(ω<sub>k</sub>t + φ<sub>k</sub>)</sup> &emsp;(6)<br>⟦absz||z|⟧ = √(x² + y²)',
            note: 'Mounting an arm on the tip of the one before means adding its arrow to that tip, so the pen is the running sum of all the arrows, equation (6). The loop starts from x = y = 0, the origin, adds the <code>vx</code> and <code>vy</code> of each arm in turn, and after the last arm <code>x</code> and <code>y</code> are Re z and Im z. Each stage of the running sum is a joint z<sub>k</sub> of the chain; <code>draw()</code> keeps the same running sums as <code>jx</code>, <code>jy</code> (step 11). Addition does not care about order, so swapping two cards changes the chain but not the pen. In the Live view <code>draw()</code> calls <code>sumAt()</code> once per frame at the clock time t with the drawn copies, and stores x, y and the distance of the pen from the centre, |z| = √(x² + y²). This is the whole of the model: the roses of (9), the beats of (10) and the two-arm distance (11) are consequences of (6) that the page never evaluates separately, and the velocity (7) is not computed at all.',
            code: `var x = 0, y = 0, parts = [];
for (var k = 0; k < ⟦N|list.length⟧; k++) {
...
    ⟦x|x += vx⟧;
    ⟦y|y += vy⟧;
    parts.push({ vx: vx, vy: vy, amp: p.amp, color: p.color });
}
return { x: x, y: y, parts: parts };
...
var cur = sumAt(t, live, ANG);
ds.set('x', cur.x); ds.set('y', cur.y); ds.set('absz', ⟦absz|Math.hypot(cur.x, cur.y)⟧); ...`,
            syms: [
                ['N', 'N', 'list.length', 'number of arms'],
                ['x', 'Re z', 'x', 'pen, reach to the right'],
                ['y', 'Im z', 'y', 'pen, reach upward'],
                ['absz', '|z|', 'Math.hypot(cur.x, cur.y)', 'distance of the pen from the centre']
            ]
        },
        {
            title: 'When the curve closes',
            where: 'gcd() and structure(); readouts() stores T · note (12), section 5',
            math: '⟦Tc|T⟧ = 2π / ⟦g|g⟧, &nbsp; g = gcd(ω<sub>1</sub>, …, ω<sub>N</sub>) &emsp;(12)<br>in the code: g = ⟦G|G⟧ / 100, &nbsp; G = gcd(round(100ω<sub>k</sub>)) over the arms with A<sub>k</sub> &gt; 0',
            note: 'Every arm is back where it started when every ω<sub>k</sub>T is a whole multiple of 2π, and then z(t + T) = z(t). The pen can come back sooner when arms of the same frequency cancel (section 5: e<sup>it</sup> − e<sup>it</sup> + e<sup>2it</sup> repeats after π s, while (12) gives 2π s); the Period readout ignores that and uses every arm with A &gt; 0. The sliders move in steps of 0.01 rad/s, so 100ω<sub>k</sub> is a whole number; <code>Math.round()</code> removes the rounding of the multiplication, since 0.29 × 100 comes out as 28.999999999999996 in floating point. So <code>G</code> is g counted in units of 0.01 rad/s, and <code>gcd()</code> is Euclid’s algorithm: replace the pair by the smaller number and the remainder of the division, until the remainder is zero. For the 3-petal rose 100ω = 400 and −200, so G = 200, g = 2 rad/s and T = π s = 3.142 s. When no arm has A &gt; 0, or every ω is 0, g = 0 and no period exists; the Now cell then shows —.',
            code: `function gcd(a, b) {
    a = Math.abs(a); b = Math.abs(b);
    while (b) { var r = a % b; a = b; b = r; }
    return a;
}
...
function structure(list) {
    var w = [];
    list.forEach(function (p) { if (p.amp > 0) w.push(Math.round(p.freq * 100)); });
    var G = 0, M = 0;
    w.forEach(function (x) { ⟦G|G = gcd(G, x)⟧; });
...
    return { n: w.length, G: G, ⟦g|g: G / 100⟧, M: M, q: q };
}
...
... ds.set('period', ⟦Tc|st.g > 0 ? TAU / st.g : NaN⟧);`,
            syms: [
                ['G', 'G', 'G', 'gcd of round(100ω<sub>k</sub>): g in units of 0.01 rad/s, an integer'],
                ['g', 'g', 'G / 100', 'largest common frequency, rad/s'],
                ['Tc', 'T', 'TAU / st.g', 'shortest time that repeats every arm with A &gt; 0, s']
            ]
        },
        {
            title: 'Rotational symmetry',
            where: 'structure(), after the gcd of step 4 · note (13), section 5.1',
            math: 'z(t + τ) = Σ<sub>k=1</sub><sup>N</sup> A<sub>k</sub> e<sup>i(ω<sub>k</sub>t + φ<sub>k</sub>)</sup> e<sup>iω<sub>k</sub>τ</sup> &emsp;(13)<br>τ = 2π/M, &nbsp; ⟦M|M⟧ = gcd(ω<sub>2</sub> − ω<sub>1</sub>, …, ω<sub>N</sub> − ω<sub>1</sub>), &nbsp; ω<sub>1</sub>/M = p/q &nbsp;⇒&nbsp; ⟦q|q⟧-fold symmetry',
            note: 'Waiting a time τ multiplies arm k by its own factor e<sup>iω<sub>k</sub>τ</sup>, equation (13). When all these factors are equal, the whole sum is multiplied by one number e<sup>iβ</sup>, and the curve is the old one turned rigidly by the angle β. They are all equal when every difference (ω<sub>j</sub> − ω<sub>1</sub>)τ is a whole multiple of 2π, first at τ = 2π/M, and the turn is then β = 2π ω<sub>1</sub>/M. Writing ω<sub>1</sub>/M = p/q in lowest terms, repeated turns by 2πp/q reach every multiple of 2π/q: the curve has q-fold symmetry. The code works in the integers of step 4: <code>w[i] - w[0]</code> is 100(ω<sub>i</sub> − ω<sub>1</sub>), so its <code>M</code> is the note’s M counted in units of 0.01 rad/s (for the Star the note’s M = 5 rad/s is the code’s M = 500). The factor 100 cancels in the ratio, so <code>q = M / gcd(w[0], M)</code> is the denominator of ω<sub>1</sub>/M in lowest terms either way: for the 3-petal rose M = 600 and gcd(400, 600) = 200, so q = 3. With one active arm there is no difference to take and the Now cell shows —; with several arms all at one frequency M = 0 and the code writes q = 0, the 0-fold of section 9, although a circle is mapped onto itself by every turn.',
            code: `for (var i = 1; i < w.length; i++) ⟦M|M = gcd(M, w[i] - w[0])⟧;
var ⟦q|q = M ? M / gcd(w[0], M) : 0⟧;`,
            syms: [
                ['M', 'M', 'M', 'gcd of the frequency differences in units of 0.01 rad/s: the code’s integer is 100 M'],
                ['q', 'q', 'q', 'order of the rotational symmetry']
            ]
        },
        {
            title: 'The average size: Parseval',
            where: 'readouts(), the sum of squares; draw(), |z|² this frame · note (14) and (15), section 6',
            math: '⟦absz2||z(t)|²⟧ = Σ<sub>k</sub> A<sub>k</sub>² + 2 Σ<sub>j&lt;k</sub> A<sub>j</sub>A<sub>k</sub> cos((ω<sub>j</sub> − ω<sub>k</sub>)t + φ<sub>j</sub> − φ<sub>k</sub>) &emsp;(14)<br>⟨|z|²⟩<sub>t</sub> = ⟦E|Σ<sub>k=1</sub><sup>N</sup> A<sub>k</sub>²⟧ &nbsp; (all ω<sub>k</sub> different) &emsp;(15)',
            note: 'Write |z|² = z z̄ and multiply out the two sums of (6): each arm with itself gives A<sub>k</sub>², and each pair of different arms gives a cosine that runs at the difference of their frequencies, equation (14). Over a long time a cosine of nonzero frequency averages to zero, so only the squares survive, (15). This is Parseval’s theorem: the power of a mixture of different frequencies is the sum of the separate powers. The code adds up <code>p.amp * p.amp</code> over the stored list into <code>e</code>, the ⟨|z|²⟩ = ΣA² readout, and <code>draw()</code> stores x² + y² of the pen this frame as |z(t)|². For two arms (14) is the triangle rule (11). For the Star ΣA² = 1.2824, while |z(t)|² swings between 0.1024 and 2.8224. Two cautions. <code>e</code> uses the stored A<sub>k</sub> while |z(t)|² uses the drawn A′<sub>k</sub>, the same numbers with Auto Dance off. And with two equal frequencies the cross term does not oscillate, so <code>e</code> is then no longer the average.',
            code: `var e = 0;
phasors.forEach(function (p) { ⟦E|e += p.amp * p.amp⟧; });
...
... ds.set('absz2', ⟦absz2|cur.x * cur.x + cur.y * cur.y⟧); ...`,
            syms: [
                ['E', 'Σ A<sub>k</sub>²', 'e', 'time average of |z|² when all ω<sub>k</sub> differ'],
                ['absz2', '|z(t)|²', 'cur.x * cur.x + cur.y * cur.y', 'squared distance of the pen now']
            ]
        },
        {
            title: 'The clock: nothing is integrated',
            where: 'speedFactor(); the Sim.clock callback, once per frame · note section 7',
            math: '⟦t|t⟧ ← t + ⟦dt|Δt⟧ · ⟦sf|s⟧, &nbsp; s = ⟦spd|speed⟧ · (1 + ⟦mid|mid⟧ · d<sub>speed</sub>) with Auto Dance on, &nbsp; s = speed with it off<br>trail ← trail + z(t)',
            note: 'Because (6) gives the pen at any time directly, the page integrates nothing: each frame it moves the clock and evaluates N cosines and N sines again. <code>dt</code> is handed in by <code>Sim.clock</code>: the real time since the previous frame in s, capped at 0.05 s so that a tab coming back from the background does not jump, and 0 while paused. <code>lastSpeed</code> is s: the Speed slider, 0 to 4, times <code>speedFactor()</code>, which is 1 + mid · d<sub>speed</sub> with Auto Dance on (mid the smoothed mid-band level of step 12, d<sub>speed</sub> the Speed drive) and exactly 1 with it off. Time runs only in the Live view. The new pen position is pushed onto <code>trail</code>, and the oldest points are dropped beyond the Trail length, 100 to 6000 points, by default 2400, which is 40 s at 60 frames per second. No error builds up from frame to frame: every point is the exact z(t) up to rounding, and the rounding of an angle ω<sub>k</sub>t stays below 10<sup>−11</sup> rad even for ω = 32 rad/s after 1000 s.',
            code: `function speedFactor() { return danceOn ? 1 + ⟦mid|clamp01(energy.mid)⟧ * dSpeed.value : 1; }
...
var clk = Sim.clock(function (⟦dt|dt⟧) {
...
    buildLive();
    lastDt = dt;
    ⟦sf|lastSpeed = speed.value * speedFactor()⟧;
    if (mode === 'live' && dt > 0) {
        ⟦t|t += dt * lastSpeed⟧;
        var z = sumAt(t, live);
        trail.push({ x: z.x, y: z.y });
        var max = trailS.value;
        if (trail.length > max) trail.splice(0, trail.length - max);
    }`,
            syms: [
                ['dt', 'Δt', 'dt', 'real time since the last frame, capped at 50 ms; 0 while paused'],
                ['spd', 'speed', 'speed.value', 'Speed slider, ×'],
                ['mid', 'mid', 'energy.mid', 'smoothed mid-band level, 0 to 1'],
                ['sf', 's', 'lastSpeed', 'speed used this frame, ×'],
                ['t', 't', 't', 'phasor time, s']
            ]
        },
        {
            title: 'The final shape: the curve sampled at once',
            where: 'spanNow() and refinal() · note section 7, Final shape',
            math: 't<sub>i</sub> = i ⟦span|T<sub>span</sub>⟧ / ⟦n|n⟧, &nbsp; i = 0, 1, …, n; &nbsp; q<sub>i</sub> = z(t<sub>i</sub>) from (6)<br>T<sub>span</sub> = min(⟦Tc|T⟧, 60 · 2π s) with Draw one full period on, Span · 2π s with it off<br>n = 700 T<sub>span</sub> / (2π s), clamped to 1500 … 12 000',
            note: 'The Final shape view does not wait for the pen: <code>refinal()</code> samples the whole curve at once from (6), at n + 1 equally spaced times from t<sub>0</sub> = 0 to t<sub>n</sub> = T<sub>span</sub>, so the last sample lands back on the first when T<sub>span</sub> is a period (to 3 × 10<sup>−15</sup> for the Star, which is rounding). <code>spanNow()</code> gives T<sub>span</sub> = <code>sp</code> in s: with Draw one full period on, the period T = 2π/g of step 4, but at most 60 · 2π s = 377 s, so a period of 628 s is drawn only in part; with it off, the Span slider, 1 to 24, times 2π s. The number of samples is 700 per 2π s, clamped to between 1500 and 12 000, so every preset gets n = 1500 and the 61-petal rose of Exercise 5.1, T = 62.83 s, gets 7000. These samples use the stored list <code>phasors</code>, not the dancing copies; they are the exact points q<sub>i</sub> = <code>finalPath[i]</code> of the next step.',
            code: `function spanNow() {
    var s = structure(phasors);
    if (swAuto.checked && s.g > 0) return Math.min(⟦Tc|TAU / s.g⟧, 60 * TAU);
    return spanS.value * TAU;
}

function refinal(snap) {
    var ⟦span|sp = spanNow()⟧;
    var ⟦n|n = Math.max(1500, Math.min(12000, Math.round(sp / TAU * 700)))⟧;
    finalPath = new Array(n + 1);
    for (var i = 0; i <= n; i++) {
        var z = sumAt(i / n * sp, phasors);
        finalPath[i] = { x: z.x, y: z.y };
    }
    finalN = n;
    finalSpan = sp;`,
            syms: [
                ['Tc', 'T', 'TAU / s.g', 'period of step 4, s'],
                ['span', 'T<sub>span</sub>', 'sp', 'time covered by the sampled curve, s'],
                ['n', 'n', 'n', 'number of intervals; the curve has n + 1 samples']
            ]
        },
        {
            title: 'Morphing is a low-pass filter',
            where: 'refinal(), the copy; morphStep(); draw(), the remaining gap; the clock calls morphStep() · note (16), section 7.1',
            math: 'p<sub>i</sub> ← p<sub>i</sub> + ⟦alpha|α⟧ (q<sub>i</sub> − p<sub>i</sub>) &nbsp;⇒&nbsp; p<sub>i</sub><sup>(m)</sup> − q<sub>i</sub> = (1 − α)<sup>m</sup> (p<sub>i</sub><sup>(0)</sup> − q<sub>i</sub>) &emsp;(16)<br>remaining gap: ⟦dev|max<sub>i</sub> |p<sub>i</sub> − q<sub>i</sub>|⟧',
            note: 'When a slider moves while the Final shape view is open, <code>refinal()</code> computes the new exact samples q<sub>i</sub> = <code>finalPath[i]</code> at once, but the curve on the screen is <code>morphPath</code>, the points p<sub>i</sub>. Each frame <code>morphStep()</code> moves every p<sub>i</sub> the fraction α of its remaining distance to q<sub>i</sub>, so after m frames the gap is (1 − α)<sup>m</sup> of what it was, equation (16). That is a first-order low-pass filter with a time constant of −1/ln(1 − α) frames: 12.0 frames, or 0.20 s at 60 frames per second, for the default α = 0.08, and the gap is below 1 % after 56 frames. <code>a</code> is α: the Morph rate slider, 0.02 to 0.35, or 1 with Smooth morphing off, which snaps at once. If the number of samples changes there is nothing to pair point with point, and <code>refinal()</code> copies the new curve straight in. <code>draw()</code> measures the largest gap still left, in plot units; it is 0 once the curve has settled. The curves in between are point-by-point blends of the old and the new curve; only for a change of radius are they curves that some in-between setting would draw, because (6) is linear in each A<sub>k</sub>.',
            code: `if (snap || !swMorph.checked || morphPath.length !== finalPath.length) {
    morphPath = finalPath.map(function (p) { return { x: p.x, y: p.y }; });
}
...
function morphStep() {
    var ⟦alpha|a = swMorph.checked ? morph.value : 1⟧;
    for (var i = 0; i < finalPath.length; i++) {
        morphPath[i].x += (finalPath[i].x - morphPath[i].x) * a;
        morphPath[i].y += (finalPath[i].y - morphPath[i].y) * a;
    }
}
...
for (var mi = 0; mi < MPn; mi++) { ... ⟦dev|dev = Math.max(dev, Math.hypot(morphPath[mi].x - FXp[mi], morphPath[mi].y - FYp[mi]))⟧; }
...
if (mode === 'final') morphStep();`,
            syms: [
                ['alpha', 'α', 'a', 'fraction of the remaining gap closed per frame; 1 with Smooth morphing off'],
                ['dev', 'max |p<sub>i</sub> − q<sub>i</sub>|', 'dev', 'largest gap still left between drawn and exact curve, plot units'],
                ['n', 'n', 'finalN', 'intervals of the sampled curve']
            ]
        },
        {
            title: 'The scale: fitting the curve into the canvas',
            where: 'reach(), fit(), baseScale(), finalScale(); draw(), the live scale · note (17), section 8',
            math: 's = 0.44 min(w, h) / max(R, 0.05) · zoom &emsp;(17)<br>Live view: R ≥ Σ<sub>k</sub> |A′<sub>k</sub>| and ≥ the farthest trail point; &nbsp; R ← R + (R<sub>target</sub> − R)(1 − e<sup>−Δt/0.6 s</sup>) when shrinking',
            note: 'Equation (17) fits the picture to the canvas. <code>box.w</code> and <code>box.h</code> are its width w and height h in CSS pixels, and <code>fitR</code> is R, how far from the origin anything is drawn: the larger of Σ|A′<sub>k</sub>|, which by the triangle inequality bounds every joint and every circle edge, and the farthest point still on the trail, which was drawn with older radii. The factor 0.44 puts R at 88 % of the way from the centre to the nearer edge. <code>fit()</code> lets R grow at once when something would leave the canvas, and shrink back with a time constant of 0.6 s, so the picture neither spills over nor jitters; the floor 0.05 avoids dividing by zero when every radius is 0. Zoom, 0.3× to 1×, only zooms out. In the Final shape view R is the largest |p<sub>i</sub>| of the curve as drawn. s is in pixels per plot unit: on a screen 1440 px wide the canvas measures 770 × 601 CSS pixels, so the 3-petal rose, with R = 2, is drawn at 132 px per unit.',
            code: `function reach() {
    var r = 0, i;
    for (i = 0; i < live.length; i++) r += Math.abs(⟦Ar|live[i].amp⟧);
    for (i = 0; i < trail.length; i++) r = Math.max(r, Math.hypot(trail[i].x, trail[i].y));
    return r;
}
function fit(dt) {
    var target = Math.max(reach(), 0.05);
    if (target > fitR || !fitR) fitR = target;
    else fitR += (target - fitR) * (1 - Math.exp(-dt / 0.6));
}
function baseScale() { return Math.min(box.w, box.h) * 0.44 / Math.max(fitR, 0.05); }
function finalScale() {
    var m = 0;
    for (var i = 0; i < morphPath.length; i++) m = Math.max(m, Math.hypot(morphPath[i].x, morphPath[i].y));
    return Math.min(box.w, box.h) * 0.44 / Math.max(m, 0.05) * zoom.value;
}
...
var s = baseScale() * zoom.value;`,
            syms: [
                ['N', 'N', 'live.length', 'number of arms summed in Σ|A′<sub>k</sub>|'],
                ['Ar', 'A′<sub>1</sub>', 'live[0].amp', 'drawn radius of arm 1, the first term of Σ|A′<sub>k</sub>|'],
                ['absz', '|z|', 'Math.hypot(…)', 'distance of the pen from the centre now; each trail point was such a distance']
            ]
        },
        {
            title: 'Equation to screen: arms, circles, trail, pen',
            where: 'polyline(); draw(), the trail and the arm loop · note section 8',
            math: 'z = x + iy &nbsp;↦&nbsp; pixel (c<sub>x</sub> + s ⟦x|x⟧, c<sub>y</sub> − s ⟦y|y⟧)<br>joint k: z<sub>k</sub> = Σ<sub>m≤k</sub> A′<sub>m</sub> e<sup>i⟦ang|θ<sub>m</sub>⟧</sup>, &nbsp; circle of radius ⟦Ar||A′<sub>k</sub>|⟧ s about z<sub>k−1</sub>',
            note: 'A point z = x + iy goes to the pixel (c<sub>x</sub> + s x, c<sub>y</sub> − s y): <code>cx</code>, <code>cy</code> is the centre of the canvas, s the scale of step 10, and the minus sign is there because the canvas counts y downward while the imaginary axis points up. The arm loop walks the chain from the centre: each joint is the previous one plus the arm’s <code>vx</code>, <code>vy</code> times s, which is the partial sum z<sub>k</sub> of step 3 in pixels, while <code>jx</code>, <code>jy</code> keep the same sums in plot units. Around each joint the next arm’s circle is drawn in thin rose with the radius |A′<sub>k</sub>| s; the arm is a 2 px line in the colour of its card with a dot of radius 3 px at its tip; the pen is a burgundy dot of radius 5.5 px at (c<sub>x</sub> + s x, c<sub>y</sub> − s y). The trail is drawn in twelve pieces whose opacity rises from about 0.25 for the oldest to 1 for the newest. Two places where the drawing differs from the model: the trail joins the frame positions with straight segments, which stray from the true curve by at most 0.0007 plot units (0.09 px) for the 3-petal rose at 1.00× and 60 frames per second, and sixteen times more at 4.00×; and while Auto Dance is on the older trail points were drawn with older radii, so the trail is no longer one closed curve.',
            code: `var px = cx + pts[i].x * s, py = cy - pts[i].y * s;
...
var w = box.w, h = box.h, cx = w / 2, cy = h / 2;
...
for (var c = 0; c < chunks && len > 1; c++) {
    var a = Math.floor(c * (len - 1) / chunks), b = Math.floor((c + 1) * (len - 1) / chunks) + 1;
    ctx.globalAlpha = 0.18 + 0.82 * (c + 1) / chunks;
    polyline(trail, cx, cy, s, a, Math.min(len, b + 1));
}
...
cur.parts.forEach(function (p, i) {
    var nx = ox + p.vx * s, ny = oy - p.vy * s;
    VX[i] = p.vx; VY[i] = p.vy; jx += p.vx; jy += p.vy; ...
...
        ctx.arc(ox, oy, Math.abs(⟦Ar|p.amp⟧ * s), 0, TAU);
...
        ctx.arc(nx, ny, 3, 0, TAU);
...
ctx.arc(cx + ⟦x|cur.x⟧ * s, cy - ⟦y|cur.y⟧ * s, 5.5, 0, TAU);`,
            syms: [
                ['x', 'x', 'cur.x', 'pen, reach to the right, plot units'],
                ['y', 'y', 'cur.y', 'pen, reach upward, plot units'],
                ['ang', 'θ<sub>1</sub>', 'ANG[0]', 'angle of arm 1, rad'],
                ['Ar', '|A′<sub>1</sub>|', 'p.amp', 'drawn radius of arm 1; its circle has |A′<sub>1</sub>| s pixels']
            ]
        },
        {
            title: 'Auto Dance: sound into three levels and a beat',
            where: 'ensureAudio(), the analyser; analyse(), once per frame · note section 8.1',
            math: 'e<sub>raw</sub> = (mean of the bins in the band) / 255, &nbsp; e ← e + 0.15 (e<sub>raw</sub> − e) &nbsp; for ⟦bass|bass⟧, ⟦mid|mid⟧, ⟦high|high⟧<br>on a beat: ⟦burst|burst⟧ = 1 + 0.9 d<sub>burst</sub>, falling by 0.1 d<sub>burst</sub> per frame, back to 1 on the tenth frame',
            note: 'The analyser of the Web Audio API takes a fast Fourier transform of 2048 samples, smoothed over time with a constant of 0.8, and reports 1024 frequency bins as bytes from 0 to 255. Each bin is <code>bin</code> = sampling rate / 2048 wide, 21.5 Hz at 44.1 kHz. <code>band()</code> averages the bins between two frequencies and divides by 255, so each raw level lies between 0 and 1; the bass band, 20 to 150 Hz, is bins 1 to 7. Mid is 150 Hz to 4 kHz, high 4 to 16 kHz. Each level is then smoothed once per frame with the same rule as the morph (16), with the fraction 0.15, so on a 120 Hz screen the levels respond twice as fast as on a 60 Hz one. A beat is declared when the raw bass <code>rb</code> rises more than 35 % above the previous frame’s, exceeds 0.22 and comes at least 280 ms after the last beat. The beat sets <code>burst</code> to 1 + d<sub>burst</sub>, with d<sub>burst</sub> the Beat burst slider, and starts a count of 10 frames; the countdown below runs in the same frame, so the radii are multiplied by 1 + 0.9 d<sub>burst</sub> on the beat frame, and the factor falls by 0.1 d<sub>burst</sub> each frame until it is 1 on the tenth. Without a song playing every level stays 0 and the burst stays 1.',
            code: `audio.an.fftSize = 2048;
audio.an.smoothingTimeConstant = 0.8;
...
if (audio.an) {
    audio.an.getByteFrequencyData(audio.data);
    var bin = audio.ctx.sampleRate / audio.an.fftSize, data = audio.data;
    var band = function (lo, hi) {
        var a = Math.max(1, Math.floor(lo / bin)), b = Math.min(data.length - 1, Math.ceil(hi / bin)), s = 0, c = 0;
        for (var i = a; i <= b; i++) { s += data[i]; c++; }
        return c ? s / c / 255 : 0;
    };
    var rb = band(20, 150), rm = band(150, 4000), rh = band(4000, 16000);
    ⟦bass|energy.bass += (rb - energy.bass) * 0.15⟧;
    ⟦mid|energy.mid += (rm - energy.mid) * 0.15⟧;
    ⟦high|energy.high += (rh - energy.high) * 0.15⟧;
    var now = performance.now();
    if (rb > prevBass * 1.35 && rb > 0.22 && now - lastBeat > 280) {
...
        burstFrames = 10;
        ⟦burst|burst = 1 + dBurst.value⟧;
    }
    prevBass = rb;
}
...
if (burstFrames > 0) {
    burstFrames--;
    ⟦burst|burst = burstFrames > 0 ? 1 + dBurst.value * burstFrames / 10 : 1⟧;
}`,
            syms: [
                ['bass', 'bass', 'energy.bass', 'smoothed level 20–150 Hz, 0 to 1'],
                ['mid', 'mid', 'energy.mid', 'smoothed level 150–4000 Hz, 0 to 1'],
                ['high', 'high', 'energy.high', 'smoothed level 4–16 kHz, 0 to 1'],
                ['burst', 'burst', 'burst', 'beat factor on every radius, 1 between beats']
            ]
        },
        {
            title: 'Auto Dance: levels into radii',
            where: 'buildLive(), once per frame before the clock moves · note section 8.1',
            math: '⟦Ar|A′⟧ = ⟦A|A⟧ · ⟦mul|m⟧<br>|ω| ≤ median |ω<sub>k</sub>|: &nbsp; m = [1 + ease(⟦bass|bass⟧) · d<sub>bass</sub> · (1 − 0.7 |ω| / |ω|<sub>max</sub>)] · ⟦burst|burst⟧<br>faster arms: &nbsp; m = (1 + ⟦high|high⟧ · d<sub>high</sub>) · burst; &nbsp; Auto Dance off: m = 1',
            note: 'Arms whose |ω| is at or below the median of all the |ω<sub>k</sub>| breathe with the bass: m = 1 + ease(bass) · d<sub>bass</sub> · (1 − 0.7 |ω|/|ω|<sub>max</sub>), with ease the Bounce curve chosen on the card, <code>EASE[p.curve]</code>, and d<sub>bass</sub> the Bass drive, <code>dBass</code>, 0 to 3, by default 1.5, so the slowest arms swing most. Faster arms follow the treble, m = 1 + high · d<sub>high</sub>, with d<sub>high</sub> the High drive, <code>dHigh</code>. Every factor is then multiplied by the burst of step 12. The result is a new list <code>live</code>, the drawn copies A′<sub>k</sub> = A<sub>k</sub> m with the same ω<sub>k</sub> and φ<sub>k</sub>, from which steps 2, 3, 7, 10 and 11 draw. The stored list <code>phasors</code> is never written here, so switching Auto Dance off returns the exact curve; only Replay of a recording moves the stored numbers themselves. With Auto Dance off m = 1, and without a song playing m = 1 as well, since every ease curve gives 0 at 0.',
            code: `function buildLive() {
    var absF = phasors.map(function (p) { return Math.abs(p.freq); });
    var maxAbs = Math.max.apply(null, [1e-6].concat(absF)), med = median(absF);
    live = phasors.map(function (p, i) {
        var mul = 1;
        if (danceOn) {
            if (absF[i] <= med) mul = 1 + EASE[p.curve](clamp01(⟦bass|energy.bass⟧)) * dBass.value * (1 - 0.7 * absF[i] / maxAbs);
            else mul = 1 + clamp01(⟦high|energy.high⟧) * dHigh.value;
            ⟦mul|mul *= burst⟧;
        }
        return { ⟦Ar|amp: p.amp * mul⟧, freq: p.freq, phase: p.phase, color: p.color, mul: mul };
    });`,
            syms: [
                ['dance', 'on/off', 'danceOn', 'Auto Dance switch'],
                ['bass', 'bass', 'energy.bass', 'smoothed bass level, 0 to 1'],
                ['high', 'high', 'energy.high', 'smoothed treble level, 0 to 1'],
                ['burst', 'burst', 'burst', 'beat factor, 1 between beats'],
                ['mul', 'm', 'live[0].mul', 'factor on the radius of arm 1'],
                ['A', 'A', 'phasors[0].amp', 'stored radius of arm 1, never changed by the dance'],
                ['Ar', 'A′', 'live[0].amp', 'drawn radius of arm 1']
            ]
        }
    ]
};
