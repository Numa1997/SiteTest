/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.water = {
    intro: 'Twelve steps from the page’s state to the dots on the screen, in the order of the lecture note. Sections 03 and 04 of the note set up Laplace’s equation (4) and the conditions (6), (8) and (9) at the edges of the water, and Section 05 solves them on paper. The code starts from that solution, so the first equation it evaluates is the dispersion relation (13). Each step pairs one numbered equation of the note with the lines that compute it. Lengths in the code are field pixels, with 100 px = 1 m. The Now column follows the burgundy parcel at the surface, the middle one of the top layer.',
    steps: [
        {
            title: 'What the page keeps: λ, a and the phase ωt',
            where: 'top of the script, k() and readouts() — constants, initial condition, wave number',
            math: '⟦k|k⟧ = 2π / ⟦lam|λ⟧ &nbsp;(rad/px), &nbsp; ⟦km|k<sub>m</sub>⟧ = 100 k &nbsp;(rad/m) &emsp;(22)<br>⟦wt|ωt⟧ = 0 when the page opens',
            note: 'The page stores no field of water. Everything it draws follows from what you set, the wavelength λ, the amplitude A and, with dispersion off, the frequency f, and from one number that runs, the phase ωt. The first quoted line fixes the units: PX_PER_M = 100 is the scale 100 px = 1 m, G = 9.81 is g in m/s², DZ = 56 is the spacing of the layers in px, and WORLD_W = 800 is the width W<sub>field</sub> of the field in px. The second line is the initial condition: omegaT, the phase ωt in rad, starts at 0, so in the first frame every parcel sits at the phase θ = kX<sub>0</sub> that its rest position alone gives it. The function k() turns the wavelength slider, lambda.value in px, into the wave number k = 2π/λ of Section 02, in rad/px. The last line stores it twice, as k in rad/px and as k<sub>m</sub> = 100 k in rad/m, because the dispersion relation needs metres. At the default λ = 260 px = 2.6 m, k<sub>m</sub> = 2.42 rad/m.',
            code: `var WORLD_W = 800, DZ = 56, PX_PER_M = 100, G = 9.81;
...
var ⟦wt|omegaT = 0⟧, fps = 0, frames = 0;
...
function ⟦k|k()⟧ { return 2 * Math.PI / ⟦lam|lambda.value⟧; }
...
ds.set('k', kk); ds.set('k_m', ⟦km|kk * PX_PER_M⟧); ...`,
            syms: [
                ['lam', 'λ', 'lambda.value', 'wavelength, px (÷ 100 for m)'],
                ['k', 'k', 'k()', 'wave number, rad/px'],
                ['km', 'k<sub>m</sub>', 'kk * PX_PER_M', 'the same wave number, rad/m'],
                ['wt', 'ωt', 'omegaT', 'phase, rad; 0 at the start']
            ]
        },
        {
            title: 'Gravity fixes the frequency: ω² = gk (13)',
            where: 'f() and readouts() — the frequency from the wavelength',
            math: '⟦om|ω⟧² = g ⟦km|k<sub>m</sub>⟧ &emsp;(13) &nbsp;⇒&nbsp; ⟦f|f⟧ = √(g k<sub>m</sub>) / 2π &emsp;(22)',
            note: 'The page never computes the potential φ. What the solution of Section 05 leaves for the code is condition (13): a wave of wave number k can exist on deep water only if it oscillates at ω = √(gk). In f(), G is g in m/s² and k() * PX_PER_M is k<sub>m</sub> in rad/m, so Math.sqrt(G * k() * PX_PER_M) is ω in rad/s, and dividing by 2 * Math.PI gives f in Hz. The comment above the function records what Section 08 says: f is computed here at full precision, and the Frequency slider only displays it, rounded to 0.01 Hz. With the Deep-water dispersion switch off (dispBox.checked false), f() returns the slider value freq.value instead, and the picture is no longer a water wave. The last line, in readouts(), turns f back into ω = 2πf in rad/s for the store and for the Stokes drift of step 10. At the default λ = 2.6 m this gives ω = 4.87 rad/s and f = 0.775 Hz.',
            code: `/* exact deep-water frequency; the slider only displays it in 0.01 Hz steps */
function ⟦f|f()⟧ {
return dispBox.checked ? Math.sqrt(G * ⟦km|k() * PX_PER_M⟧) / (2 * Math.PI) : freq.value;
}
...
var kk = k(), ff = f(), aa = a(), ⟦om|om = 2 * Math.PI * ff⟧, am = aa / PX_PER_M;`,
            syms: [
                ['lam', 'λ', 'lambda.value', 'wavelength, px'],
                ['km', 'k<sub>m</sub>', 'k() * PX_PER_M', 'wave number, rad/m'],
                ['f', 'f', 'f()', 'frequency, Hz, at full precision']
            ]
        },
        {
            title: 'Phase speed and period (14)',
            where: 'readouts() — the Phase speed and Period readouts',
            math: '⟦c|c⟧ = ω/k = ⟦cdeep|√(g/k)⟧ = f λ, &nbsp; ⟦T|T⟧ = 2π/ω = 1/f &emsp;(14)',
            note: 'Equation (14) says how fast the crests run. The page computes it as you would measure it, distance per time: f() * lambda.value is f λ in px/s, and dividing by PX_PER_M gives c in m/s. Because ω = 2πf and k = 2π/λ, f λ is the same number as ω/k, and with dispersion on it equals √(g/k) from (13). The last quoted line stores both forms, c and c_deep = Math.sqrt(G / (kk * PX_PER_M)), with k in rad/m, so the data panel can compare them; they agree while dispersion is on. The Phase speed readout shows c to 0.01 m/s, and the Period readout shows T = 1/f in s. At the default λ = 2.6 m, c = 2.01 m/s and T = 1.29 s; four times the wavelength gives twice the speed.',
            code: `var ⟦c|c = f() * lambda.value / PX_PER_M⟧;
document.getElementById('r-c').textContent = c.toFixed(2) + ' m/s';
...
document.getElementById('r-t').textContent = (⟦T|1 / f()⟧).toFixed(2) + ' s';
...
... ds.set('T', 1 / ff); ds.set('c', c); ds.set('c_deep', ⟦cdeep|Math.sqrt(G / (kk * PX_PER_M))⟧); ...`,
            syms: [
                ['lam', 'λ', 'lambda.value', 'wavelength, px'],
                ['f', 'f', 'f()', 'frequency, Hz'],
                ['c', 'c', 'c', 'phase speed, m/s'],
                ['T', 'T', '1 / f()', 'period, s']
            ]
        },
        {
            title: 'Group speed: half the phase speed (15)',
            where: 'readouts() — stored, not drawn',
            math: '⟦cg|c<sub>g</sub>⟧ = dω/dk = ½ √(g/k) = ⟦c|c⟧ / 2 &emsp;(15)',
            note: 'The group velocity (15) is the speed at which a group of crests travels, and with it the energy. The page draws a single wave that never ends, so it has no groups and c<sub>g</sub> cannot be watched. The quoted line only stores it, as c / 2 in m/s, the deep-water form of (15), and the data panel shows it as a prediction. With the dispersion switch off the line stores no number (NaN, shown as —): (15) rests on ω² = gk, and the note says that c<sub>g</sub> = c/2 then no longer applies.',
            code: `... ds.set('c', c); ds.set('c_deep', Math.sqrt(G / (kk * PX_PER_M))); ⟦cg|ds.set('cg', dispBox.checked ? c / 2 : NaN);⟧`,
            syms: [
                ['c', 'c', 'c', 'phase speed, m/s'],
                ['cg', 'c<sub>g</sub>', 'dispBox.checked ? c / 2 : NaN', 'group speed in deep water, m/s (not drawn); undefined with dispersion off']
            ]
        },
        {
            title: 'The velocity under the wave (16)',
            where: 'draw() — ω for the frame, and the parcel loop',
            math: '⟦u|u⟧ = a⟦om|ω⟧ e<sup>kz<sub>0</sub></sup> cos ⟦th|θ⟧, &nbsp; ⟦w|w⟧ = aω e<sup>kz<sub>0</sub></sup> sin θ, &nbsp; with ⟦r|a e<sup>kz<sub>0</sub></sup>⟧ = r and θ = k⟦X0|x<sub>0</sub>⟧ − ωt &emsp;(16)',
            note: 'The potential (12) found in Section 05 has the velocity (16) as its slopes, by (3). The page evaluates (16) in the linear way of Section 06: at each parcel’s rest position (x<sub>0</sub>, z<sub>0</sub>), not where the parcel actually is. In draw(), om is ω in rad/s, from the same f() as step 2. In the parcel loop, th is the phase θ = kx<sub>0</sub> − ωt in rad, with kk = k in rad/px, X0 = x<sub>0</sub> in px and omegaT = ωt. The variable r is the factor a e<sup>kz<sub>0</sub></sup>, the orbit radius of the layer, computed in the layer loop around this one (step 7). The last line stores u and w for every parcel q = jN + i, in px/s because r is in px. They move nothing: the positions come in closed form in the next step, and the velocities are stored so that the data panel can show them. Under a crest, θ = 0, u is forward and w is zero. At the surface and the defaults, aω = 1.17 m/s, slower than the crest at 2.01 m/s.',
            code: `var NP = count.value, NL = layers.value, ⟦om|om = 2 * Math.PI * f()⟧, q;
...
⟦th|th = kk * X0 - omegaT⟧;
...
... ⟦u|uM[q] = r * om * Math.cos(th)⟧; ⟦w|wM[q] = r * om * Math.sin(th)⟧; ...`,
            syms: [
                ['X0', 'x<sub>0</sub>', 'X0', 'rest position of the followed parcel, px'],
                ['th', 'θ', 'th', 'its phase, shown reduced to (−π, π]'],
                ['r', 'r = a e<sup>kz<sub>0</sub></sup>', 'r (j = 0)', 'orbit radius at the surface, z<sub>0</sub> = 0, px']
            ]
        },
        {
            title: 'Every parcel runs on a circle (17)',
            where: 'draw() — the parcel loop, positions',
            math: '⟦px|ξ⟧ = x − x<sub>0</sub> = −r sin ⟦th|θ⟧, &nbsp; ⟦pz|ζ⟧ = z − z<sub>0</sub> = r cos θ<br>θ = k⟦X0|x<sub>0</sub>⟧ − ωt, &nbsp; r = a e<sup>kz<sub>0</sub></sup> &emsp;(17)',
            note: 'Integrating (16) in time at the fixed rest position gives (17): each parcel swings −r sin θ sideways and r cos θ up and down, a quarter cycle apart, which together make a circle of radius r around (x<sub>0</sub>, z<sub>0</sub>). The loop runs over the N parcels of one layer, N being set by Particles per layer. X0 is x<sub>0</sub> in px, the X<sub>0</sub> of Section 08: the rest positions are spread evenly from 30 px to W<sub>field</sub> − 30 px. th is θ, as in step 5. The last line stores, for each parcel, its rest position, its phase, and the displacements ξ = x − x<sub>0</sub> (xiM) and ζ = z − z<sub>0</sub> (zeM) in px, with ζ counted upward as in the note. Under a crest, θ = 0, the parcel is at the top of its circle. As time runs, θ falls, so the parcel moves forward at the top of its circle and backward at the bottom: clockwise, like the gull of Section 01.',
            code: `for (var i = 0; i < N; i++) {
var ⟦X0|X0 = 30 + i * (WORLD_W - 60) / (N - 1)⟧, cx = X0 * s;
⟦th|th = kk * X0 - omegaT⟧;
...
X0A[i] = X0; thM[q] = th; ⟦px|xiM[q] = -r * Math.sin(th)⟧; ⟦pz|zeM[q] = r * Math.cos(th)⟧; ...`,
            syms: [
                ['X0', 'x<sub>0</sub>', 'X0', 'rest position of the followed parcel, px'],
                ['th', 'θ', 'th', 'its phase, shown reduced to (−π, π]'],
                ['px', 'ξ', 'xiM[q]', 'its horizontal displacement x − x<sub>0</sub> now, px'],
                ['pz', 'ζ', 'zeM[q]', 'its vertical displacement z − z<sub>0</sub> now, upward, px']
            ]
        },
        {
            title: 'The circles shrink with depth (18)',
            where: 'draw() — the layer loop; then readouts() — the deepest layer',
            math: '⟦r|r⟧(⟦z0|z<sub>0</sub>⟧) = a e<sup>kz<sub>0</sub></sup>, &nbsp; z<sub>0</sub> = −56 j px, &nbsp; j = 0, 1, …, layers − 1 &emsp;(18)',
            note: 'Equation (18) is the factor e<sup>kz</sup> of the potential (12), seen in the parcels: the circles shrink by a factor e for every λ/2π of depth. The outer loop runs over the layers j. z0 is the rest height z<sub>0</sub> in px: 0 at the surface and 56 px = 0.56 m lower for each layer (DZ = 56), negative below the calm level as in the note. r is (18) in px. Here A is the variable of draw() that holds a(), the capped amplitude a of step 9, not the Amplitude slider. The next line stores, per layer, the radius, the depth in m (−z0 / 100) and the screen height of the orbit centres (step 12). In readouts(), deep is the radius of the deepest layer as a fraction of a, e<sup>−k · 56 px · (layers − 1)</sup>, shown by the Deepest orbit readout, and r1 is the radius one layer down. At the defaults each layer’s radius is 0.258 times the one above, 24, 6.2, 1.6, 0.41 and 0.11 px, and the fifth layer, 2.24 m down, keeps 0.45 % of a.',
            code: `for (var j = 0; j < L; j++) {
var ⟦z0|z0 = -j * DZ⟧, ⟦r|r = A * Math.exp(kk * z0)⟧, cy = ys - z0 * s;
rL[j] = r; zL[j] = -z0 / PX_PER_M; cyL[j] = cy;
...
var ⟦deep|deep = Math.exp(-k() * DZ * (layers.value - 1))⟧;
...
ds.set('deep', deep); ⟦r1|ds.set('r1', aa * Math.exp(-kk * DZ))⟧; ...`,
            syms: [
                ['r', 'r(0) = a', 'rL[0]', 'orbit radius of the surface layer, j = 0, px'],
                ['r1', 'r(−56 px)', 'aa * Math.exp(-kk * DZ)', 'orbit radius one layer down, j = 1, px'],
                ['z0', 'z<sub>0</sub>, deepest', '-j * DZ, j = layers − 1', 'rest height of the deepest layer, px'],
                ['deep', 'r/a, deepest', 'deep', 'its orbit radius as a fraction of a']
            ]
        },
        {
            title: 'The surface is the top row of parcels (19)',
            where: 'draw() — the surface line',
            math: 'x = ⟦X|x<sub>0</sub>⟧ − ⟦a|a⟧ sin ⟦th|θ⟧, &nbsp; ⟦eta|η⟧ = a cos θ, &nbsp; θ = kx<sub>0</sub> − ωt &emsp;(19)<br>x<sub>0</sub> from −60 px to W<sub>field</sub> + 60 px, every 3 px',
            note: 'Setting z<sub>0</sub> = 0 in (17) gives the surface (19): the line through all surface parcels at once, as the rest position x<sub>0</sub> runs along the sea. The page draws this line twice, once to fill the water body and once as the accent line; the quoted loop is the first, and the second is the same. X is x<sub>0</sub> in px, stepped by 3 px from 60 px left of the field to 60 px right of it (WORLD_W is W<sub>field</sub>), so that the ends of the line lie outside the frame. th is θ, and A is the capped amplitude a. sx and sy are already screen coordinates, by (23) of step 12: (X − a sin θ) times s is x, and ys − a cos θ times s puts the height η above the calm line, upward on the screen. These points are drawn but not stored, and they are not parcels. The curve is a trochoid: crests sharper and troughs flatter than the sine (10), the two agreeing as ak → 0. The Now value of η is the stored ζ of the followed surface parcel, which by (19) is the surface height there.',
            code: `for (⟦X|X = -60; X <= WORLD_W + 60; X += 3⟧) {
th = kk * X - omegaT;
var sx = (X - ⟦a|A⟧ * Math.sin(th)) * s, ⟦eta|sy = ys - A * Math.cos(th) * s⟧;
if (X === -60) ctx.moveTo(sx, sy); else ctx.lineTo(sx, sy);
}`,
            syms: [
                ['a', 'a', 'A = a()', 'amplitude used, px'],
                ['th', 'θ', 'th', 'phase of the followed parcel, rad'],
                ['eta', 'η', 'zeM[q], top row', 'surface height at the followed parcel, px']
            ]
        },
        {
            title: 'The amplitude cap that keeps (19) from folding',
            where: 'a() and readouts() — the Steepness readout',
            math: 'dx/dx<sub>0</sub> = 1 − ⟦ak|ak⟧ cos θ &nbsp;(Section 6.2)<br>⟦a|a⟧ = min(⟦A|A⟧, 0.9/⟦k|k⟧) &nbsp;⇒&nbsp; ak ≤ 0.9',
            note: 'Differentiating (19) along the surface gives dx/dx<sub>0</sub> = 1 − ak cos θ, which measures how closely neighbouring surface parcels crowd together. At ak = 1 it vanishes at the crest, θ = 0: the crest becomes a cusp, and beyond that the line would loop through itself. a() keeps the model short of that point. amp.value is the Amplitude slider, the note’s A in px, and 0.9 / k() is the largest amplitude allowed at this wave number, in px, so a never exceeds A and ak never exceeds 0.9. Every other line that needs the amplitude calls a(), so what you see always uses the capped value. The Steepness ak readout shows a k, a pure number (px times rad/px), and adds “(cap)” when a is below A. The last line stores a, whether the cap is active, and ak. At λ = 260 px an amplitude of 50 px would give ak = 1.21; the cap holds a at 37.2 px. Real waves break near ak ≈ 0.44, so the steeper shapes the page allows are already an idealisation.',
            code: `function ⟦a|a()⟧ { return Math.min(⟦A|amp.value⟧, 0.9 / ⟦k|k()⟧); }
...
document.getElementById('r-ak').textContent = (⟦ak|a() * k()⟧).toFixed(2) + (a() < amp.value ? _t(' (cap)') : '');
...
ds.set('a', aa); ds.set('cap', aa < amp.value); ds.set('ak', aa * kk); ...`,
            syms: [
                ['A', 'A', 'amp.value', 'Amplitude slider, px'],
                ['k', 'k', 'k()', 'wave number, rad/px'],
                ['a', 'a', 'a()', 'amplitude used, px'],
                ['ak', 'ak', 'a() * k()', 'steepness, at most 0.9']
            ]
        },
        {
            title: 'Stokes drift: stored, not drawn (21)',
            where: 'readouts() — the stored drift at the surface',
            math: '⟦us|U<sub>S</sub>⟧ = ⟦a|a⟧² ⟦om|ω⟧ ⟦km|k⟧ e<sup>2kz<sub>0</sub></sup> = c (⟦ak|ak⟧)² e<sup>2kz<sub>0</sub></sup>, &nbsp; taken at z<sub>0</sub> = 0 &emsp;(21)',
            note: 'Equation (21) is the slow forward drift that the closed circles of (17) leave out. The page leaves it out of the picture on purpose and stores only its value at the surface, as theory. The quoted lines compute it in SI units: om is ω in rad/s, kk * PX_PER_M is k in rad/m, and am = aa / PX_PER_M is a in m, so om * kk * PX_PER_M * am * am is a²ωk in m/s at z<sub>0</sub> = 0, where e<sup>2kz<sub>0</sub></sup> = 1. The data panel lists it as u<sub>S</sub>. At the default ak = 0.58 it gives 0.68 m/s, a third of c, far outside the small steepness for which (21) was derived. At a moderate ak = 0.2 it gives 0.081 m/s, which Figure 4 of the note confirms to within 3.6 %.',
            code: `var kk = k(), ff = f(), aa = a(), ⟦om|om = 2 * Math.PI * ff⟧, am = aa / PX_PER_M;
...
... ⟦us|ds.set('stokes', om * kk * PX_PER_M * am * am);⟧`,
            syms: [
                ['a', 'a', 'aa', 'amplitude used, px (am = aa / 100 in m)'],
                ['km', 'k', 'kk * PX_PER_M', 'wave number, rad/m'],
                ['f', 'f', 'ff', 'frequency, Hz (ω = 2πf)'],
                ['ak', 'ak', 'aa * kk', 'steepness']
            ]
        },
        {
            title: 'The clock: only the phase is stepped (22)',
            where: 'Sim.clock callback — once per frame',
            math: '⟦wt|ωt⟧ ← ωt + 2π ⟦f|f⟧ ⟦dt|Δt⟧ &emsp;(22)',
            note: 'The positions (17) are known in closed form, so the page integrates nothing except the phase. Sim.clock calls this function once per animation frame with dt, the time Δt in s since the last frame (capped at 0.05 s by the clock, and 0 while paused), and t, the play time in s. The first line inside adds 2π f Δt to omegaT, the phase ωt in rad, with the exact f() of step 2, not the rounded slider value. Adding up the phase, rather than computing ωt from t, keeps the motion smooth when you move a slider and f changes. While f stays constant the sum equals 2πf t up to rounding, so no error builds up however long the page runs. The store then keeps ωt and the number of periods completed, ωt / 2π, and draw() evaluates (17), (18) and (19) afresh for the new phase.',
            code: `var clk = Sim.clock(function (⟦dt|dt⟧, t) {
⟦wt|omegaT += 2 * Math.PI * f() * dt⟧;
...
ds.set('omegaT', omegaT); ds.set('periods', omegaT / (2 * Math.PI)); ...
draw();
});`,
            syms: [
                ['f', 'f', 'f()', 'frequency, Hz, at full precision'],
                ['wt', 'ωt', 'omegaT', 'phase, rad']
            ]
        },
        {
            title: 'From field pixels to screen pixels (23)',
            where: 'draw() — its first three lines, the layer loop and the parcel loop',
            math: '⟦s|s⟧ = W / W<sub>field</sub>, &nbsp; ⟦ys|y<sub>s</sub>⟧ = max(a s + 34, 0.28 H)<br>⟦xs|x<sub>screen</sub>⟧ = (⟦X0|X<sub>0</sub>⟧ + ⟦px|ξ⟧) s, &nbsp; ⟦yscr|y<sub>screen</sub>⟧ = y<sub>s</sub> + 56 j s − ⟦pz|ζ⟧ s &emsp;(23)',
            note: 'Equation (23) carries the field, measured in px with 100 px = 1 m, onto your screen. The first line picks W<sub>field</sub>: 800 px (8 m), or 400 px (4 m) when the canvas is narrower than 560 screen pixels, so that the wave is not drawn tiny on a phone. In the next line w and h are the canvas width W and height H in screen pixels, and s = w / WORLD_W is the number of screen pixels per field pixel. ys is the calm level y<sub>s</sub>, measured down from the top of the canvas: at 28 % of the height, or lower when a crest, a s high, would otherwise come within 34 px of the top. In the layer loop, cy = ys − z0 * s puts the orbit centres of layer j at y<sub>s</sub> + 56 j s, since z0 = −56 j. In the parcel loop, px and py are x<sub>screen</sub> and y<sub>screen</sub>: the rest position plus ξ, times s, and the centre height minus ζ s, minus because screen y points down while ζ points up. Two lines decide what is drawn, not what is stored. A layer whose orbit centres lie less than 8 px above the bottom edge (visible false) is computed and stored but not drawn. With Show orbits on, an orbit circle is drawn only while its radius on screen, r s, exceeds 1.2 px. Each parcel is a dot at (px, py), which the canvas spreads over neighbouring pixels when the position falls between them.',
            code: `WORLD_W = box.w < 560 ? 400 : 800;
var w = box.w, h = box.h, ⟦s|s = w / WORLD_W⟧, kk = k(), A = a();
var ⟦ys|ys = Math.max(A * s + 34, h * 0.28)⟧, X, th;
...
var z0 = -j * DZ, r = A * Math.exp(kk * z0), cy = ys - z0 * s;
...
var visible = cy <= h - 8;
...
var ⟦xs|px = (X0 - r * Math.sin(th)) * s⟧, ⟦yscr|py = cy - r * Math.cos(th) * s⟧;
...
if (orbitsBox.checked && r * s > 1.2) {`,
            syms: [
                ['s', 's', 's', 'screen px per field px'],
                ['ys', 'y<sub>s</sub>', 'ys', 'calm level, screen px from the top'],
                ['X0', 'X<sub>0</sub>', 'X0', 'rest position of the followed parcel, field px'],
                ['px', 'ξ', 'xiM[q]', 'its horizontal displacement, field px'],
                ['pz', 'ζ', 'zeM[q]', 'its vertical displacement, upward, field px']
            ]
        }
    ]
};
