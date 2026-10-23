/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.pendulum = {
    intro: 'Thirteen steps from the model of the lecture note to the dots on the screen, in the order of the note: the fixed numbers and the starting state (§2), the positions (1) and the energies (3) and (4), the parts of Lagrange’s derivation the page keeps (§4) and the accelerations (9) it evaluates, the chaos twin of §6, the Runge–Kutta step (13) and the clock of §7, and the drawing of §8. Each step sets an equation of the note, with its number, beside the lines of this page’s script that evaluate it, copied character for character; a line that is only “...” stands for page lines left out. The table gives each symbol, its name in the code, its value in the running pendulum now, and its meaning with its unit. The small-swing modes (10) and (11) have no code of their own: they are what the same equations do when the angles are small. Hover over or tap a symbol to light it in all three places.',
    steps: [
        {
            title: 'The fixed numbers and the starting state',
            where: 'top of the script, and restart() — the starting state',
            math: 'm<sub>1</sub> = 1 kg, l<sub>1</sub> = 1 m, g = 9.81 m/s², ⟦h|h⟧ = 1/600 s<br>⟦m2|m<sub>2</sub>⟧ = m<sub>1</sub> e<sup>slider</sup>, ⟦l2|l<sub>2</sub>⟧ = l<sub>1</sub> e<sup>slider</sup><br>⟦s|s⟧ = (⟦t1|θ<sub>1</sub>⟧, ⟦t2|θ<sub>2</sub>⟧, ⟦o1|ω<sub>1</sub>⟧, ⟦o2|ω<sub>2</sub>⟧)',
            note: 'Section 2 fixes the upper bob and rod at m<sub>1</sub> = 1 kg and l<sub>1</sub> = 1 m, with g = 9.81 m/s². The first line holds them as the plain numbers m1, l1 and g in SI units, together with H, the time step h = 1/600 s of step 9, and EPS = 0.001 rad, the head start of the chaos twin in step 8. The mass and length sliders do not hold m<sub>2</sub> and l<sub>2</sub> themselves but the natural logarithms of the ratios m<sub>2</sub>/m<sub>1</sub> and l<sub>2</sub>/l<sub>1</sub>: m2 = m1 * Math.exp(mass.value) turns the slider position into the lower mass in kilograms, so that equal slider steps multiply the ratio by equal factors, and the next line does the same for the lower rod length l2 in metres. The last line builds the state s of §2 and §7 as the array state. The two angle sliders are read in degrees and converted to radians here, once, so state[0] = θ<sub>1</sub> and state[1] = θ<sub>2</sub> are in rad, measured from the downward vertical and counter-clockwise positive; state[2] = ω<sub>1</sub> and state[3] = ω<sub>2</sub> come from their sliders in rad/s. These four numbers are all the integrator ever advances. The Now column shows the state as it is now, not as it started.',
            code: `var g = 9.81, m1 = 1, l1 = 1, EPS = 0.001, ⟦h|H = 1 / 600⟧;
...
⟦m2|m2 = m1 * Math.exp(mass.value)⟧;
⟦l2|l2 = l1 * Math.exp(len.value)⟧;
⟦s|state⟧ = [⟦t1|th1.value * Math.PI / 180⟧, ⟦t2|th2.value * Math.PI / 180⟧, ⟦o1|w1.value⟧, ⟦o2|w2.value⟧];`,
            syms: [
                ['m2', 'm<sub>2</sub>', 'm2', 'lower bob mass, kg (m<sub>1</sub> = 1 kg)'],
                ['l2', 'l<sub>2</sub>', 'l2', 'lower rod length, m (l<sub>1</sub> = 1 m)'],
                ['t1', 'θ<sub>1</sub>', 'state[0]', 'upper rod angle from the downward vertical, rad'],
                ['t2', 'θ<sub>2</sub>', 'state[1]', 'lower rod angle from the downward vertical, rad'],
                ['o1', 'ω<sub>1</sub>', 'state[2]', 'upper angular velocity, rad/s'],
                ['o2', 'ω<sub>2</sub>', 'state[3]', 'lower angular velocity, rad/s'],
                ['h', 'h', 'H', 'time step, s']
            ]
        },
        {
            title: 'Where the bobs are',
            where: 'diagnostics() — the bob positions in metres, once per frame',
            math: 'x<sub>1</sub> = l<sub>1</sub> sin ⟦t1|θ<sub>1</sub>⟧, y<sub>1</sub> = −l<sub>1</sub> cos ⟦t1|θ<sub>1</sub>⟧<br>x<sub>2</sub> = x<sub>1</sub> + ⟦l2|l<sub>2</sub>⟧ sin ⟦t2|θ<sub>2</sub>⟧, y<sub>2</sub> = y<sub>1</sub> − ⟦l2|l<sub>2</sub>⟧ cos ⟦t2|θ<sub>2</sub>⟧<span style="font-style:normal;margin-left:1.5em">(1)</span>',
            note: 'Equation (1) puts the pivot at the origin with y pointing up. In diagnostics(), s is the current state, so s[0] is θ<sub>1</sub> and s[1] is θ<sub>2</sub> in rad. The first line gives x1 and y1, the coordinates of bob 1 in metres; the second stores them and computes those of bob 2, x1 + l2 * Math.sin(s[1]) and y1 - l2 * Math.cos(s[1]), also in metres. The minus sign in y1 = -l1 * Math.cos(s[0]) is the minus sign of (1): a hanging bob, θ<sub>1</sub> = 0, sits at y<sub>1</sub> = −1 m, one rod length below the pivot. These numbers go to the data panel only. The picture is drawn by a separate pixel mapping, step 12, which uses the same sines and cosines with the direction of y turned round. The Now column has no entry for the metre positions; it shows the angles and the length they are built from.',
            code: `var x1 = l1 * Math.sin(⟦t1|s[0]⟧), y1 = -l1 * Math.cos(⟦t1|s[0]⟧);
ds.set('x1', x1); ds.set('y1', y1); ds.set('x2', x1 + ⟦l2|l2⟧ * Math.sin(⟦t2|s[1]⟧)); ds.set('y2', y1 - ⟦l2|l2⟧ * Math.cos(⟦t2|s[1]⟧));`,
            syms: [
                ['t1', 'θ<sub>1</sub>', 's[0]', 'upper rod angle, rad'],
                ['t2', 'θ<sub>2</sub>', 's[1]', 'lower rod angle, rad'],
                ['l2', 'l<sub>2</sub>', 'l2', 'lower rod length, m']
            ]
        },
        {
            title: 'Kinetic and potential energy',
            where: 'energy(s), and the line of diagnostics() that stores T and V',
            math: '⟦kin|T⟧ = ½m<sub>1</sub>l<sub>1</sub>²ω<sub>1</sub>² + ½m<sub>2</sub>[l<sub>1</sub>²ω<sub>1</sub>² + l<sub>2</sub>²ω<sub>2</sub>² + 2l<sub>1</sub>l<sub>2</sub>ω<sub>1</sub>ω<sub>2</sub> cos(θ<sub>1</sub> − θ<sub>2</sub>)]<span style="font-style:normal;margin-left:1.5em">(3)</span><br>  = ½(m<sub>1</sub>+m<sub>2</sub>)l<sub>1</sub>²ω<sub>1</sub>² + ½m<sub>2</sub>l<sub>2</sub>²ω<sub>2</sub>² + m<sub>2</sub>l<sub>1</sub>l<sub>2</sub>ω<sub>1</sub>ω<sub>2</sub> cos(θ<sub>1</sub> − θ<sub>2</sub>)<br>⟦pot|V⟧ = −(m<sub>1</sub>+m<sub>2</sub>)g l<sub>1</sub> cos θ<sub>1</sub> − m<sub>2</sub>g l<sub>2</sub> cos θ<sub>2</sub><span style="font-style:normal;margin-left:1.5em">(4)</span><br>⟦E|E⟧ = T + V',
            note: 'Each line is an equation of §3 in SI units. In energy(s), s[2] and s[3] are ω<sub>1</sub> and ω<sub>2</sub> in rad/s, and s[0] − s[1] is θ<sub>1</sub> − θ<sub>2</sub> in rad. kin is (3) with the bracket multiplied out, as in the second line of the formula: the first term gathers ½m<sub>1</sub>l<sub>1</sub>²ω<sub>1</sub>² and ½m<sub>2</sub>l<sub>1</sub>²ω<sub>1</sub>² into ½(m<sub>1</sub>+m<sub>2</sub>)l<sub>1</sub>²ω<sub>1</sub>², because the lower bob is carried along by the upper rod; the second term is the lower bob’s own swing about the elbow; the third is the cross term, the passenger walking on the train, which makes the two speeds add fully when the rods point the same way and not at all when they are at right angles. pot is (4) letter for letter, with V = 0 at the height of the pivot. Both are in joules, and the function returns E = T + V. The last line, in diagnostics(), is what the Now column reads: it calls energy(s) for E, writes V out again, and stores T as E − V, which equals kin to rounding error.',
            code: `var ⟦kin|kin⟧ = 0.5 * (m1 + m2) * l1 * l1 * s[2] * s[2] + 0.5 * m2 * l2 * l2 * s[3] * s[3]
    + m2 * l1 * l2 * s[2] * s[3] * Math.cos(s[0] - s[1]);
var ⟦pot|pot⟧ = -(m1 + m2) * g * l1 * Math.cos(s[0]) - m2 * g * l2 * Math.cos(s[1]);
return kin + pot;
...
var ⟦E|E = energy(s)⟧, ⟦pot|V = -(m1 + m2) * g * l1 * Math.cos(s[0]) - m2 * g * l2 * Math.cos(s[1])⟧, ⟦kin|T = E - V⟧;`,
            syms: [
                ['kin', 'T', 'kin; stored as T = E - V', 'kinetic energy, J'],
                ['pot', 'V', 'pot; stored as V', 'potential energy, zero at the pivot, J'],
                ['E', 'E', 'energy(s)', 'total energy, J']
            ]
        },
        {
            title: 'Generalised momenta and the matrix of (8)',
            where: 'diagnostics() — the mass matrix, its determinant and the momenta',
            math: 'p<sub>1</sub> = ∂L/∂ω<sub>1</sub> = (m<sub>1</sub>+m<sub>2</sub>)l<sub>1</sub>²⟦o1|ω<sub>1</sub>⟧ + m<sub>2</sub>l<sub>1</sub>l<sub>2</sub>⟦o2|ω<sub>2</sub>⟧ cos ⟦d|δ⟧<br>p<sub>2</sub> = ∂L/∂ω<sub>2</sub> = m<sub>2</sub>l<sub>2</sub>²⟦o2|ω<sub>2</sub>⟧ + m<sub>2</sub>l<sub>1</sub>l<sub>2</sub>⟦o1|ω<sub>1</sub>⟧ cos ⟦d|δ⟧<br>det M = m<sub>2</sub>l<sub>1</sub>l<sub>2</sub> · det = m<sub>2</sub>l<sub>1</sub>²l<sub>2</sub>²(m<sub>1</sub> + m<sub>2</sub> sin²δ) > 0<span style="font-style:normal;margin-left:1.5em">(8)</span>',
            note: 'The page does not solve the Euler–Lagrange equation (5); the derivation of §4 is done once, on paper, and the page evaluates its result (9) in steps 5 to 7. What diagnostics() does keep, for the data panel, are the pieces of §4.1 and of (8). The first line takes the current state, d = s[0] - s[1] is the angle δ between the rods in rad, and c is cos δ. The array Mm holds, row by row and in kg m², the matrix M of the kinetic energy, T = ½(ω<sub>1</sub>, ω<sub>2</sub>) M (ω<sub>1</sub>, ω<sub>2</sub>)<sup>T</sup>: Mm[0] = (m<sub>1</sub>+m<sub>2</sub>)l<sub>1</sub>², the off-diagonal Mm[1] = Mm[2] = m<sub>2</sub>l<sub>1</sub>l<sub>2</sub> cos δ, and Mm[3] = m<sub>2</sub>l<sub>2</sub>². The note writes no letter for this matrix; M is the store’s name. Multiplied by the angular velocities s[2] = ω<sub>1</sub> and s[3] = ω<sub>2</sub>, it gives p1 and p2, the generalised momenta ∂L/∂ω<sub>i</sub> of §4.1 in kg m²/s; p1 is exactly the p<sub>1</sub> the note writes, an angular momentum that already contains the lower mass. Dividing the first row of M by l<sub>1</sub> and the second by m<sub>2</sub>l<sub>2</sub> gives the matrix on the left of (8), so detM = M<sub>00</sub>M<sub>11</sub> − M<sub>01</sub>² is m<sub>2</sub>l<sub>1</sub>l<sub>2</sub> times the det of (8), in kg² m⁴. It is positive for every state, which is why (8) always has exactly one solution. The Now column shows the inputs; p<sub>1</sub>, p<sub>2</sub> and det M are in the data panel.',
            code: `var s = state, k = deriv(s), ⟦d|d = s[0] - s[1]⟧, c = Math.cos(⟦d|d⟧), i;
...
Mm[0] = (m1 + m2) * l1 * l1; Mm[1] = m2 * l1 * l2 * c; Mm[2] = Mm[1]; Mm[3] = m2 * l2 * l2;
...
ds.set('detM', Mm[0] * Mm[3] - Mm[1] * Mm[2]); ds.set('p1', Mm[0] * ⟦o1|s[2]⟧ + Mm[1] * ⟦o2|s[3]⟧); ds.set('p2', Mm[2] * ⟦o1|s[2]⟧ + Mm[3] * ⟦o2|s[3]⟧);`,
            syms: [
                ['d', 'δ', 'd', 'angle between the rods, θ<sub>1</sub> − θ<sub>2</sub>, rad'],
                ['o1', 'ω<sub>1</sub>', 's[2]', 'upper angular velocity, rad/s'],
                ['o2', 'ω<sub>2</sub>', 's[3]', 'lower angular velocity, rad/s'],
                ['m2', 'm<sub>2</sub>', 'm2', 'lower bob mass, kg'],
                ['l2', 'l<sub>2</sub>', 'l2', 'lower rod length, m']
            ]
        },
        {
            title: 'The angle between the rods and the shared denominator',
            where: 'deriv(s) — its first two lines',
            math: '⟦d|δ⟧ = ⟦t1|θ<sub>1</sub>⟧ − ⟦t2|θ<sub>2</sub>⟧<br>⟦den|D′⟧ = 2m<sub>1</sub> + ⟦m2|m<sub>2</sub>⟧ − m<sub>2</sub> cos 2δ = 2(m<sub>1</sub> + m<sub>2</sub> sin²δ) = 2 det/(l<sub>1</sub>l<sub>2</sub>)',
            note: 'deriv(s) is the function F of §7: it takes a state and returns how fast each of its four numbers is changing. Its first line unpacks the state into t1 = θ<sub>1</sub> and t2 = θ<sub>2</sub> in rad and o1 = ω<sub>1</sub> and o2 = ω<sub>2</sub> in rad/s, and forms d, the angle δ between the rods. The second line computes the bracket that stands under both fractions of (9). The note gives it no letter; D′ is the store’s name for it. With the first identity of §4.4, 2 sin²δ = 1 − cos 2δ, it equals 2(m<sub>1</sub> + m<sub>2</sub> sin²δ), which is the det of (8) with the two lengths divided out and doubled; its unit is kg. Because sin²δ is never negative, den is never smaller than 2m<sub>1</sub> = 2 kg, the value it takes when sin δ = 0, the rods in one line, straight or folded back. The divisions in the next two steps are therefore always safe.',
            code: `var ⟦t1|t1 = s[0]⟧, ⟦t2|t2 = s[1]⟧, ⟦o1|o1 = s[2]⟧, ⟦o2|o2 = s[3]⟧, ⟦d|d = t1 - t2⟧;
var ⟦den|den = 2 * m1 + m2 - m2 * Math.cos(2 * d)⟧;`,
            syms: [
                ['t1', 'θ<sub>1</sub>', 't1', 'upper rod angle, rad'],
                ['t2', 'θ<sub>2</sub>', 't2', 'lower rod angle, rad'],
                ['d', 'δ', 'd', 'angle between the rods, rad'],
                ['den', 'D′', 'den', 'shared denominator of (9), 2(m<sub>1</sub> + m<sub>2</sub> sin²δ), kg'],
                ['m2', 'm<sub>2</sub>', 'm2', 'lower bob mass, kg (m<sub>1</sub> = 1 kg)']
            ]
        },
        {
            title: 'The upper angular acceleration α₁',
            where: 'deriv(s) — the a1 line',
            math: '⟦a1|α<sub>1</sub>⟧ = [−g(2m<sub>1</sub>+m<sub>2</sub>) sin θ<sub>1</sub> − m<sub>2</sub>g sin(θ<sub>1</sub>−2θ<sub>2</sub>) − 2m<sub>2</sub> sin δ (⟦o2|ω<sub>2</sub>⟧²l<sub>2</sub> + ⟦o1|ω<sub>1</sub>⟧²l<sub>1</sub> cos δ)] / (l<sub>1</sub>⟦den|D′⟧)<span style="font-style:normal;margin-left:1.5em">(9)</span>',
            note: 'This is the first line of (9). It comes from the system (8) by Cramer’s rule and the first two identities of §4.4, 2 sin²δ = 1 − cos 2δ and 2 sin θ<sub>2</sub> cos δ = sin θ<sub>1</sub> − sin(θ<sub>1</sub> − 2θ<sub>2</sub>). The code is the formula term by term, in the same order. The first two terms, -g * (2 * m1 + m2) * Math.sin(t1) and - m2 * g * Math.sin(t1 - 2 * t2), are the pull of gravity, which grows as the rods tilt away from the vertical. The third, - 2 * Math.sin(d) * m2 * (o2 * o2 * l2 + o1 * o1 * l1 * Math.cos(d)), carries the squares of the angular velocities: it is the push and pull the rods give each other when they turn, and it vanishes when they are in one line. The whole is divided by l1 * den, which is l<sub>1</sub>D′. The result a1 is α<sub>1</sub> in rad/s², with g = 9.81 m/s², m1 = 1 kg and l1 = 1 m.',
            code: `var ⟦a1|a1⟧ = (-g * (2 * m1 + m2) * Math.sin(t1) - m2 * g * Math.sin(t1 - 2 * t2)
    - 2 * Math.sin(d) * m2 * (⟦o2|o2 * o2⟧ * l2 + ⟦o1|o1 * o1⟧ * l1 * Math.cos(d))) / (l1 * ⟦den|den⟧);`,
            syms: [
                ['a1', 'α<sub>1</sub>', 'a1', 'upper angular acceleration, rad/s²'],
                ['o1', 'ω<sub>1</sub>', 'o1', 'upper angular velocity, rad/s'],
                ['o2', 'ω<sub>2</sub>', 'o2', 'lower angular velocity, rad/s'],
                ['den', 'D′', 'den', 'shared denominator, kg']
            ]
        },
        {
            title: 'The lower angular acceleration α₂ and the whole right-hand side',
            where: 'deriv(s) — the a2 line and the return',
            math: '⟦a2|α<sub>2</sub>⟧ = 2 sin δ [⟦o1|ω<sub>1</sub>⟧²l<sub>1</sub>(m<sub>1</sub>+m<sub>2</sub>) + g(m<sub>1</sub>+m<sub>2</sub>) cos θ<sub>1</sub> + ⟦o2|ω<sub>2</sub>⟧²l<sub>2</sub>m<sub>2</sub> cos δ] / (l<sub>2</sub>⟦den|D′⟧)<span style="font-style:normal;margin-left:1.5em">(9)</span><br>ds/dt = F(s) = (⟦o1|ω<sub>1</sub>⟧, ⟦o2|ω<sub>2</sub>⟧, ⟦a1|α<sub>1</sub>⟧, ⟦a2|α<sub>2</sub>⟧)',
            note: 'The first line is the second line of (9). Its common factor 2 sin δ comes from the third identity of §4.4, sin θ<sub>1</sub> cos δ − sin θ<sub>2</sub> = cos θ<sub>1</sub> sin δ, so α<sub>2</sub> is zero whenever the rods are in one line. Inside the bracket, o1 * o1 * l1 * (m1 + m2) and o2 * o2 * l2 * m2 * Math.cos(d) are the terms in the squared angular velocities and g * (m1 + m2) * Math.cos(t1) is the gravity term; the division by l2 * den is the division by l<sub>2</sub>D′, and a2 is α<sub>2</sub> in rad/s². The return line is the whole right-hand side F(s) of §7 as one array, in the same order as the state: its first two entries say that the angles change at the rates o1 = ω<sub>1</sub> and o2 = ω<sub>2</sub> in rad/s, its last two are the accelerations a1 and a2 just computed. Step 9 calls this function four times per step.',
            code: `var ⟦a2|a2⟧ = (2 * Math.sin(d) * (⟦o1|o1 * o1⟧ * l1 * (m1 + m2) + g * (m1 + m2) * Math.cos(t1)
    + ⟦o2|o2 * o2⟧ * l2 * m2 * Math.cos(d))) / (l2 * ⟦den|den⟧);
return [⟦o1|o1⟧, ⟦o2|o2⟧, ⟦a1|a1⟧, ⟦a2|a2⟧];`,
            syms: [
                ['a2', 'α<sub>2</sub>', 'a2', 'lower angular acceleration, rad/s²'],
                ['a1', 'α<sub>1</sub>', 'a1', 'upper angular acceleration, rad/s²'],
                ['den', 'D′', 'den', 'shared denominator, kg'],
                ['k1', 'F(s)', 'deriv(s)', 'the returned array (ω<sub>1</sub>, ω<sub>2</sub> in rad/s; α<sub>1</sub>, α<sub>2</sub> in rad/s²)']
            ]
        },
        {
            title: 'The chaos twin and the distance d(t)',
            where: 'restart() — the twin’s start; diagnostics() — the distance between the lower bobs',
            math: 'θ′<sub>1</sub>(0) = ⟦t1|θ<sub>1</sub>⟧(0) + 0.001 rad, θ′<sub>2</sub>(0) = θ<sub>2</sub>(0), ω′<sub>i</sub>(0) = ω<sub>i</sub>(0)<br>⟦sep|d⟧(t) = |(x<sub>2</sub> − x′<sub>2</sub>, y<sub>2</sub> − y′<sub>2</sub>)| ≈ d<sub>0</sub> e<sup>λt</sup>',
            note: 'Section 6 follows two pendulums whose upper angles start 0.001 rad apart, and the page does exactly that. When the Chaos twin switch is on, restart() makes a second state, twin, a copy of state with EPS = 0.001 rad added to θ<sub>1</sub> only; the clock of step 10 advances it with the same rk4 and the same h. Once per frame, diagnostics() takes the pixel positions of the two lower bobs, p[2], p[3] for the main pendulum and q[2], q[3] for the twin (step 12), measures the distance between them with Math.hypot, and divides by the scale σ in px/m to turn it back into metres. Because the mapping to pixels is a shift and one common scale, this is the same distance as in metres: sep is d(t) of §6 and Figure 3, in m, shown as the Twin separation readout. log10sep is its base-10 logarithm, which rises roughly along a straight line, of slope λ/ln 10, while the motion is chaotic. The page computes d(t) only. The largest Lyapunov exponent (12), λ ≈ 1.46 per second, was computed for the note by a separate long run, not by this page. The Now column has no entry for d; it is in the data panel.',
            code: `twin = twinBox.checked ? [⟦t1|state[0]⟧ + EPS, state[1], state[2], state[3]] : null;
...
var q = pos(twin), ⟦sep|sep = Math.hypot(p[2] - q[2], p[3] - q[3]) / scale⟧;
...
ds.set('sep', sep); ds.set('log10sep', sep > 0 ? Math.log(sep) / Math.LN10 : undefined);`,
            syms: [
                ['t1', 'θ<sub>1</sub>', 'state[0]', 'upper rod angle of the main pendulum, rad'],
                ['scale', 'σ', 'scale', 'pixels per metre, px/m']
            ]
        },
        {
            title: 'One Runge–Kutta step',
            where: 'rk4(s, h)',
            math: '⟦k1|k<sub>1</sub>⟧ = F(s), ⟦k2|k<sub>2</sub>⟧ = F(s + ½h k<sub>1</sub>)<br>⟦k3|k<sub>3</sub>⟧ = F(s + ½h k<sub>2</sub>), ⟦k4|k<sub>4</sub>⟧ = F(s + h k<sub>3</sub>)<br>s(t + ⟦h|h⟧) = s + h/6 (k<sub>1</sub> + 2k<sub>2</sub> + 2k<sub>3</sub> + k<sub>4</sub>)<span style="font-style:normal;margin-left:1.5em">(13)</span>',
            note: 'rk4(s, h) is (13) line by line, with s the state array and h the step in seconds; the clock calls it with H = 1/600 s, and deriv is F. k1 is the slope at the start of the step. s2 = s + (h/2)k1 is a trial state half a step ahead, and k2 is the slope there; s3 is a second half-step trial built with k2, and k3 its slope; s4 is a full step ahead built with k3, and k4 the slope at the end. The last line takes the weighted mean of the four slopes, weights 1 : 2 : 2 : 1 divided by 6, and moves the state by h times it, giving s(t + h) in out. Each entry keeps the unit of its state entry, rad or rad/s, because every k has the unit of the state per second and is multiplied by a time. The trial states are separate arrays, so all four entries of one stage are computed from the same input; changing θ<sub>1</sub> in place before α<sub>2</sub> was computed would be a different and less accurate method. As §7 says, the error of one step shrinks like h⁵ and the error accumulated over a fixed time like h⁴, so halving h makes the result about sixteen times more accurate.',
            code: `var ⟦k1|k1 = deriv(s)⟧, i, s2 = [], s3 = [], s4 = [], out = [];
for (i = 0; i < 4; i++) s2[i] = s[i] + h / 2 * k1[i];
var ⟦k2|k2 = deriv(s2)⟧;
for (i = 0; i < 4; i++) s3[i] = s[i] + h / 2 * k2[i];
var ⟦k3|k3 = deriv(s3)⟧;
for (i = 0; i < 4; i++) s4[i] = s[i] + ⟦h|h⟧ * k3[i];
var ⟦k4|k4 = deriv(s4)⟧;
for (i = 0; i < 4; i++) out[i] = s[i] + ⟦h|h / 6⟧ * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);`,
            syms: [
                ['k1', 'k<sub>1</sub>', 'k1 = deriv(s)', 'slope at the start of the step: (ω<sub>1</sub>, ω<sub>2</sub>, α<sub>1</sub>, α<sub>2</sub>) in rad/s and rad/s²'],
                ['h', 'h', 'h (called with H)', 'time step, s']
            ]
        },
        {
            title: 'How many steps each frame takes',
            where: 'Sim.clock callback — the step loop',
            math: '⟦acc|τ⟧ ← τ + Δt × (time scale)<br>⟦n|n⟧ = min(⌊τ / h⌋, 600), τ ← min(τ − n h, h)<br>s ← s(t + ⟦h|h⟧) and ⟦t|t⟧ ← t + h, n times',
            note: 'The screen refreshes at an uneven rate, while (13) wants equal steps h. The clock hands the callback dt, the real time since the last frame in seconds, the Δt of §8: about 1/60 s, and never more than 0.05 s, where the clock caps it. The first line multiplies it by the Time scale slider, speed.value, and adds it to acc, the simulated time τ not yet spent, in s. n is the number of whole steps H = h = 1/600 s that fit into it, with the 600-step guard of §7; lastN keeps it for the store, and acc keeps the remainder, never more than one step. The loop then calls rk4 n times on state, the main pendulum, and adds H to simT, the simulated time t in s, once per step; the lines left out advance the twin of step 8 in the same way and draw the trail segments of step 13. With Δt at most 0.05 s and the Time scale at most 1.5, τ is at most 0.075 s plus one carried step, so n is at most 46 and the guard cannot act. On a 60 Hz screen at Time scale 1, n is about 10, the ten steps per frame of §7. Note the letters: H in the code is the step h, not the figure height H of §8; τ is the store’s name for acc.',
            code: `⟦acc|acc += dt * speed.value⟧;
var ⟦n|n = Math.min(Math.floor(acc / H), 600)⟧;
lastN = n;
acc = Math.min(acc - n * H, H);
for (var i = 0; i < n; i++) {
    state = rk4(state, ⟦h|H⟧);
    ...
    ⟦t|simT += H⟧;
}`,
            syms: [
                ['acc', 'τ', 'acc', 'simulated time carried to the next frame, s'],
                ['n', 'n', 'n (stored as lastN)', 'RK4 steps taken in the last frame'],
                ['h', 'h', 'H', 'time step, s'],
                ['t', 't', 'simT', 'simulated time since restart, s']
            ]
        },
        {
            title: 'Energy drift as the accuracy check',
            where: 'restart() — the starting energy; diagnostics() — the drift',
            math: '⟦E0|E<sub>0</sub>⟧ = E at restart<br>⟦drift|ε⟧ = (⟦E|E⟧ − E<sub>0</sub>) / E<sub>scale</sub>, E<sub>scale</sub> = (m<sub>1</sub>+m<sub>2</sub>)g l<sub>1</sub> + m<sub>2</sub>g l<sub>2</sub>',
            note: 'With no friction, (3) and (4) keep E = T + V fixed, so any change in the computed E is the integrator’s own error (§3, “Energy is conserved”; §7). restart() stores the starting energy E0 in J, from the same energy() as step 3. Every frame, diagnostics() recomputes E from the current state and divides E − E0 by E<sub>scale</sub>, the depth of the potential well in J, written out as (m1 + m2) * g * l1 + m2 * g * l2. The note gives the ratio no letter; ε is the store’s name, and the page shows it as the Energy drift readout. It is signed and has no unit. Dividing by E<sub>0</sub> instead would fail, because E<sub>0</sub> can be close to zero. What to expect, measured for §7: within ±5 × 10⁻⁸ over the first 20 s of the default start; then a slow, steady creep downward of about 7 × 10⁻⁸ a minute; and up to −3.6 × 10⁻⁴ within 20 s at mass ratio 10, where steps of h are too coarse for the sharp kicks the heavy bob gives the light rod.',
            code: `⟦E0|E0 = energy(state)⟧;
...
var ⟦drift|drift⟧ = (⟦E|E⟧ - E0) / ((m1 + m2) * g * l1 + m2 * g * l2);`,
            syms: [
                ['E0', 'E<sub>0</sub>', 'E0', 'total energy at restart, J'],
                ['E', 'E', 'E = energy(s)', 'total energy now, J'],
                ['drift', 'ε', 'drift', 'energy error relative to the well depth, dimensionless']
            ]
        },
        {
            title: 'From metres to pixels',
            where: 'layout() — scale and pivot; pos(s) — the bobs on screen',
            math: '⟦scale|σ⟧ = (min(W, H)/2 − 34) / (l<sub>1</sub> + l<sub>2</sub>), x<sub>0</sub> = W/2, y<sub>0</sub> = H/2<br>x<sub>1</sub> px = x<sub>0</sub> + σl<sub>1</sub> sin θ<sub>1</sub>, ⟦y1|y<sub>1</sub> px⟧ = y<sub>0</sub> + σl<sub>1</sub> cos θ<sub>1</sub><br>x<sub>2</sub> px = x<sub>1</sub> px + σ⟦l2|l<sub>2</sub>⟧ sin θ<sub>2</sub>, y<sub>2</sub> px = y<sub>1</sub> px + σl<sub>2</sub> cos θ<sub>2</sub>',
            note: 'layout() sets up the picture of §8. box.w and box.h are the width W and height H of the figure in CSS pixels; ox and oy are the pivot (x<sub>0</sub>, y<sub>0</sub>) at its centre (the store still calls them o<sub>x</sub>, o<sub>y</sub>); scale is σ in px/m, chosen so that the fully stretched pendulum, l<sub>1</sub> + l<sub>2</sub> metres long, ends 34 px short of the nearer edge, room for the protractor’s degree labels, which sit 18 px outside its circle. pos(s) turns a state into four screen coordinates in px, counted from the left and from the top: x1, y1 for bob 1, then the two entries for bob 2. Here x1 and y1 are local pixel variables of pos(), not the metre x<sub>1</sub>, y<sub>1</sub> of (1). Compared with (1), x is only shifted and scaled, but screen y points down, so the minus signs of (1) turn into plus signs: + l1 * scale * Math.cos(s[0]) puts a hanging bob below the pivot. These pixel positions are what the rods, the bobs, the trail and the twin distance of step 8 are drawn and measured from, and the data panel checks that the pixel at each stored bob centre is burgundy.',
            code: `ox = box.w / 2;
oy = box.h / 2;
⟦scale|scale = (Math.min(box.w, box.h) / 2 - 34) / (l1 + l2)⟧;
...
var x1 = ox + l1 * scale * Math.sin(s[0]), ⟦y1|y1 = oy + l1 * scale * Math.cos(s[0])⟧;
return [x1, y1, x1 + ⟦l2|l2⟧ * scale * Math.sin(s[1]), y1 + l2 * scale * Math.cos(s[1])];`,
            syms: [
                ['scale', 'σ', 'scale', 'pixels per metre, px/m'],
                ['y1', 'y<sub>1</sub> px', 'pos(state)[1]', 'bob 1 as drawn, px from the top'],
                ['l2', 'l<sub>2</sub>', 'l2', 'lower rod length, m (l<sub>1</sub> = 1 m)']
            ]
        },
        {
            title: 'Bob sizes and the fading trail',
            where: 'drawPendulum(s, ghost) — the bob radii; Sim.clock callback — the trail',
            math: 'r<sub>1</sub> = 8 px, r<sub>2</sub> = 8 (⟦m2|m<sub>2</sub>⟧/m<sub>1</sub>)<sup>1/3</sup> px, clamped to 4–17 px<br>trail opacity × (1 − 0.008)<sup>60 Δt</sup> each frame, half-life ln 2 / (60 |ln 0.992|) ≈ 1.4 s',
            note: 'The second paragraph of §8, in code. drawPendulum() gives bob 1 the radius r1 = 8 px and bob 2 the radius r2 = 8 (m<sub>2</sub>/m<sub>1</sub>)<sup>1/3</sup> px, so that its volume grows in proportion to its mass, as for balls of one material; Math.max and Math.min clamp it to 4–17 px. The size is for the eye only: in the model the masses are points. Inside the step loop of step 10, pos(state) gives bob 2’s new screen position pa, and segment() draws a 1.5 px burgundy line to it from the previous position, on a separate transparent trail canvas, one segment per RK4 step. Once per frame, after the loop, fade() erases the fraction 1 − 0.992<sup>60Δt</sup> of what is on that canvas, with dt = Δt the real frame time in s. The fading therefore follows real time, not the frame rate: at 60 frames a second it is 0.8 % per frame, and the brightness would halve every 1.4 s. Here the drawing departs from the formula: the canvas stores opacity in steps of 1/255, the small fading steps round away, and the trail falls to half in about 1.6 s and then stops near a quarter of its opacity, as §8 reports.',
            code: `var r1 = 8, r2 = Math.max(4, Math.min(17, 8 * Math.cbrt(⟦m2|m2⟧ / m1)));
...
var pa = pos(state);
segment(prevA, pa, 'rgba(122, 31, 43, 0.85)', 1.5);
...
fade(1 - Math.pow(1 - 0.008, dt * 60));`,
            syms: [
                ['m2', 'm<sub>2</sub>', 'm2', 'lower bob mass, kg (m<sub>1</sub> = 1 kg)'],
                ['scale', 'σ', 'scale', 'pixels per metre, px/m, used by pos()']
            ]
        }
    ]
};
