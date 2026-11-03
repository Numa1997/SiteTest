/* From symbols to code — Fig. 11, Balancing Two Rods on a Cart (double-inverted-pendulum.html).
   Each step pairs an equation of the lecture note with the lines of the page's script that compute it, copied character for character.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), defined in the page next to its state. */
window.WALK = window.WALK || {};

window.WALK.dipc = {
    intro: 'Nine steps from the lecture note to the moving picture, in the order the page uses them: the constants of the machine (6) and (7), the matrix D of (5), the equations of motion (9), the Runge–Kutta step (18), the linearisation (10) and (11), the fall rates (12) and (13), the controller from the Riccati equation (15) and (16), the sampled and limited push, and the flick (17). Each step sets the equation beside the lines of this page’s script that evaluate it, copied character for character; a line that is only “...” stands for page lines left out. The table gives each symbol, its name in the code, its value now, and its meaning with its unit. Hover over or tap a symbol to light it in all three places.',
    steps: [
        {
            title: 'The constants of the machine',
            where: 'par(): read from the sliders whenever one moves',
            math: '⟦d1|d<sub>1</sub>⟧ = m<sub>0</sub>+m<sub>1</sub>+m<sub>2</sub>, d<sub>2</sub> = (½m<sub>1</sub>+m<sub>2</sub>)L<sub>1</sub>, d<sub>3</sub> = ½m<sub>2</sub>L<sub>2</sub>,<br>d<sub>4</sub> = (⅓m<sub>1</sub>+m<sub>2</sub>)L<sub>1</sub>², d<sub>5</sub> = ½m<sub>2</sub>L<sub>1</sub>L<sub>2</sub>, d<sub>6</sub> = ⅓m<sub>2</sub>L<sub>2</sub>²<span style="font-style:normal;margin-left:1.5em">(6)</span><br>⟦f1|f<sub>1</sub>⟧ = (½m<sub>1</sub>+m<sub>2</sub>)L<sub>1</sub>g, f<sub>2</sub> = ½m<sub>2</sub>L<sub>2</sub>g<span style="font-style:normal;margin-left:1.5em">(7)</span>',
            note: 'The masses m<sub>0</sub>, m<sub>1</sub>, m<sub>2</sub> in kg and the lengths L<sub>1</sub>, L<sub>2</sub> in m are read from their sliders, and the eight constants of the note are computed once, in the order of (6) and (7): the array d holds d<sub>1</sub> … d<sub>6</sub> (d[0] is d<sub>1</sub>, because arrays count from 0), in kg, kg m and kg m², and the array f holds f<sub>1</sub>, f<sub>2</sub> in N m. G is g = 9.81 m/s², fixed at the top of the script together with the Runge–Kutta step H = h = 1 ms, the weights Q of (14) and the angle LOST = 60° at which the controller gives up. Every other function reads only p.d and p.f, so a slider changes the physics everywhere at once.',
            code: `var TH = Sim.theme, G = 9.81, H = 0.001, Q = [50, 50, 50, 20, 700, 700], LOST = Math.PI / 3;
...
function par() { var m0 = sl.m0.value, m1 = sl.m1.value, m2 = sl.m2.value, L1 = sl.L1.value, L2 = sl.L2.value;
return { m0: m0, m1: m1, m2: m2, L1: L1, L2: L2, ⟦d1|d: [m0 + m1 + m2⟧, (m1 / 2 + m2) * L1, m2 * L2 / 2, (m1 / 3 + m2) * L1 * L1, m2 * L1 * L2 / 2, m2 * L2 * L2 / 3], ⟦f1|f: [(m1 / 2 + m2) * L1 * G⟧, m2 * L2 * G / 2] }; }`,
            syms: [['d1', 'd<sub>1</sub>', 'p.d[0]', 'everything that moves with the cart, kg'], ['f1', 'f<sub>1</sub>', 'p.f[0]', 'gravity’s torque factor of the lower rod, N m']]
        },
        {
            title: 'The matrix of the kinetic energy',
            where: 'Dm(p, a, b): D at the angles a = θ<sub>1</sub>, b = θ<sub>2</sub>',
            math: 'T = ½ θ̇<sup>T</sup> D(θ) θ̇,  D = [[d<sub>1</sub>, d<sub>2</sub> cos ⟦t1|θ<sub>1</sub>⟧, d<sub>3</sub> cos ⟦t2|θ<sub>2</sub>⟧], [d<sub>2</sub> cos θ<sub>1</sub>, d<sub>4</sub>, d<sub>5</sub> cos(θ<sub>1</sub> − θ<sub>2</sub>)], [d<sub>3</sub> cos θ<sub>2</sub>, d<sub>5</sub> cos(θ<sub>1</sub> − θ<sub>2</sub>), d<sub>6</sub>]]<span style="font-style:normal;margin-left:1.5em">(5)</span>',
            note: 'Dm returns the 3 × 3 matrix D of (5) as an array of three rows. c1, c2 and c12 are the three cosines that appear in it, computed once each. The diagonal holds the constant inertias d<sub>1</sub>, d<sub>4</sub>, d<sub>6</sub>; the off-diagonal places hold the couplings, which shrink as the rods lean, because a leaning rod turns partly up and down instead of sideways. D is symmetric, as every kinetic-energy matrix is, and positive definite, so it can always be inverted: that is what the next step relies on.',
            code: `function Dm(p, a, b) { var d = p.d, c1 = Math.cos(a), c2 = Math.cos(b), c12 = Math.cos(a - b); return [[d[0], d[1] * c1, d[2] * c2], [d[1] * c1, d[3], d[4] * c12], [d[2] * c2, d[4] * c12, d[5]]]; }`,
            syms: [['t1', 'θ<sub>1</sub>', 's[1]', 'lower rod angle from the upward vertical, rad'], ['t2', 'θ<sub>2</sub>', 's[2]', 'upper rod angle from the upward vertical, rad']]
        },
        {
            title: 'The equations of motion',
            where: 'rhs(p, s, u): the right-hand side ṡ = f(s, u)',
            math: 'D(θ) ⟦acc|θ̈⟧ = H ⟦u|u⟧ − C(θ, θ̇) θ̇ − G(θ)<span style="font-style:normal;margin-left:1.5em">(9)</span><br>C θ̇ = (−d<sub>2</sub> sin θ<sub>1</sub> θ̇<sub>1</sub>² − d<sub>3</sub> sin θ<sub>2</sub> θ̇<sub>2</sub>², d<sub>5</sub> sin(θ<sub>1</sub>−θ<sub>2</sub>) θ̇<sub>2</sub>², −d<sub>5</sub> sin(θ<sub>1</sub>−θ<sub>2</sub>) θ̇<sub>1</sub>²)<br>G = (0, −f<sub>1</sub> sin θ<sub>1</sub>, −f<sub>2</sub> sin θ<sub>2</sub>)',
            note: 'The state s holds six numbers: s[0] = x in m, s[1] = θ<sub>1</sub> and s[2] = θ<sub>2</sub> in rad, and their rates s[3] = ẋ in m/s, s[4] = θ̇<sub>1</sub> and s[5] = θ̇<sub>2</sub> in rad/s. rhs returns how fast each of them changes. The page never forms the matrix C: it multiplies it by θ̇ on paper first (the second line of the formula, which is (8a), (8) and (8b) read off) and computes the three products directly as Cq, in N. Gv is the gravity vector G in N m. solve3 then solves the 3 × 3 linear system D θ̈ = Hu − Cθ̇ − G for the accelerations q = (ẍ, θ̈<sub>1</sub>, θ̈<sub>2</sub>) by Gaussian elimination with pivoting, which is cheaper and more accurate than forming D<sup>−1</sup>. The force u enters only the first row, because H = (1, 0, 0): the motor pushes the cart and nothing else.',
            code: `function rhs(p, s, u) { var a = s[1], b = s[2], ad = s[4], bd = s[5], d = p.d, sab = Math.sin(a - b);
var Cq = [-d[1] * Math.sin(a) * ad * ad - d[2] * Math.sin(b) * bd * bd, d[4] * sab * bd * bd, -d[4] * sab * ad * ad];   // C θ̇, row by row
var Gv = [0, -p.f[0] * Math.sin(a), -p.f[1] * Math.sin(b)];
var ⟦acc|q = solve3(Dm(p, a, b), [u - Cq[0] - Gv[0], -Cq[1] - Gv[1], -Cq[2] - Gv[2]])⟧;
return [s[3], s[4], s[5], q[0], q[1], q[2]]; }`,
            syms: [['acc', 'θ̈', 'q', 'accelerations (ẍ, θ̈₁, θ̈₂), m/s² and rad/s²'], ['u', 'u', 'u', 'motor force on the cart, N']]
        },
        {
            title: 'One Runge–Kutta step',
            where: 'rk4(p, s, u, h), called from step() every 1 ms of simulated time',
            math: 'k<sub>1</sub> = f(s<sub>n</sub>), k<sub>2</sub> = f(s<sub>n</sub> + ½h k<sub>1</sub>), k<sub>3</sub> = f(s<sub>n</sub> + ½h k<sub>2</sub>), k<sub>4</sub> = f(s<sub>n</sub> + h k<sub>3</sub>)<br>s<sub>n+1</sub> = s<sub>n</sub> + ⟦h|h⟧/6 (k<sub>1</sub> + 2k<sub>2</sub> + 2k<sub>3</sub> + k<sub>4</sub>)<span style="font-style:normal;margin-left:1.5em">(18)</span>',
            note: 'rk4 evaluates the slope of step 3 four times, at the start of the step, twice at its middle and at its end, and advances the state by their weighted mean. add(s, k, h) is the state s moved along the slope k for a time h. The force u is the same in all four evaluations, because the sampled controller holds it constant between its samples. The screen asks for a new picture about 60 times a second; step() runs as many 1 ms steps as real time has passed since the last picture (acc collects the time), so the simulation keeps real time whatever the frame rate.',
            code: `function rk4(p, s, u, h) { var k1 = rhs(p, s, u), k2 = rhs(p, add(s, k1, h / 2), u), k3 = rhs(p, add(s, k2, h / 2), u), k4 = rhs(p, add(s, k3, h), u);
return s.map(function (v, i) { return v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]); }); }
...
s = rk4(p, s, u, H); tSim += H;`,
            syms: [['h', 'h', 'H', 'Runge–Kutta step, s']]
        },
        {
            title: 'The linear model near the top',
            where: 'linear(p): A and B of (11)',
            math: 'D<sub>0</sub> θ̈ = F θ + H u,  F = diag(0, f<sub>1</sub>, f<sub>2</sub>)<span style="font-style:normal;margin-left:1.5em">(10)</span><br>A = [[0, I], [D<sub>0</sub><sup>−1</sup>F, 0]],  B = [[0], [D<sub>0</sub><sup>−1</sup>H]]<span style="font-style:normal;margin-left:1.5em">(11)</span>',
            note: 'Di is D<sub>0</sub><sup>−1</sup>, the inverse of D at θ = 0. A is 6 × 6: its upper-right block is the identity (the first three rates of the state are its last three entries), A[i][i + 3] = 1. Its lower-left block is D<sub>0</sub><sup>−1</sup>F; because F has zeros in its first column, only the columns for θ<sub>1</sub> and θ<sub>2</sub> are non-zero, Di[i][1] f<sub>1</sub> and Di[i][2] f<sub>2</sub>. B is the first column of D<sub>0</sub><sup>−1</sup>, placed in the lower half, since D<sub>0</sub><sup>−1</sup>H picks out that column. The note checks this matrix against the one printed by Moysis.',
            code: `function linear(p) { var Di = inv(Dm(p, 0, 0)), A = zeros(6, 6), B = zeros(6, 1), i;
for (i = 0; i < 3; i++) { A[i][i + 3] = 1; A[i + 3][1] = Di[i][1] * p.f[0]; A[i + 3][2] = Di[i][2] * p.f[1]; B[i + 3][0] = Di[i][0]; } return { A: A, B: B }; }`,
            syms: []
        },
        {
            title: 'How fast the rods fall',
            where: 'fallRates(p), shown in the panel as “Fall rates, controller off”',
            math: 'M = [[d<sub>4</sub> − d<sub>2</sub>²/d<sub>1</sub>, d<sub>5</sub> − d<sub>2</sub>d<sub>3</sub>/d<sub>1</sub>], [·, d<sub>6</sub> − d<sub>3</sub>²/d<sub>1</sub>]]<span style="font-style:normal;margin-left:1.5em">(12)</span><br>det M σ<sup>4</sup> − (M<sub>11</sub>f<sub>2</sub> + M<sub>22</sub>f<sub>1</sub>) σ² + f<sub>1</sub>f<sub>2</sub> = 0  →  ⟦sig|σ⟧<span style="font-style:normal;margin-left:1.5em">(13)</span>',
            note: 'M11, M12 and M22 are the entries of the reduced matrix (12) in kg m², what is left of the rods’ inertia once the cart’s recoil is taken out. a, b and c are the coefficients of the quadratic (13) in σ², and the two roots come from the school formula; their square roots are the two fall rates in 1/s, the larger first. The panel also shows 1/σ, the time in which a lean grows by the factor e.',
            code: `function fallRates(p) {   // (12)–(13)
var d = p.d, M11 = d[3] - d[1] * d[1] / d[0], M12 = d[4] - d[1] * d[2] / d[0], M22 = d[5] - d[2] * d[2] / d[0];
var a = M11 * M22 - M12 * M12, b = -(M11 * p.f[1] + M22 * p.f[0]), c = p.f[0] * p.f[1], disc = Math.sqrt(b * b - 4 * a * c);
return [⟦sig|Math.sqrt((-b + disc) / (2 * a))⟧, Math.sqrt((-b - disc) / (2 * a))]; }`,
            syms: [['sig', 'σ', 'sg[0]', 'faster fall rate with the controller off, 1/s']]
        },
        {
            title: 'The gains from the Riccati equation',
            where: 'lqr(A, B, R), called by redesign() whenever a slider moves',
            math: 'Z = [[A, −ρ<sup>−1</sup>BB<sup>T</sup>], [−Q, −A<sup>T</sup>]],  Z ← ½(Z + Z<sup>−1</sup>) → W<br>[W<sub>12</sub>; W<sub>22</sub>+I] P = −[W<sub>11</sub>+I; W<sub>21</sub>]<span style="font-style:normal;margin-left:1.5em">(15)</span><br>⟦K|K⟧ = ρ<sup>−1</sup>B<sup>T</sup>P<span style="font-style:normal;margin-left:1.5em">(16)</span>',
            note: 'Hm is the 12 × 12 Hamiltonian matrix of §7.1 and R is ρ. The loop replaces Z by the mean of Z and its inverse until nothing changes by more than 10<sup>−12</sup> in total; the limit is the matrix sign W. Lm and Rm are the two 12 × 6 blocks of the last equation, and P = (Lm<sup>T</sup>Lm)<sup>−1</sup>Lm<sup>T</sup>Rm is its least-squares solution. The last line is (16): K<sub>j</sub> = Σ<sub>i</sub> B<sub>i</sub>P<sub>ij</sub>/ρ. The gains are recomputed for every slider change, so the controller always knows the machine it holds.',
            code: `for (i = 0; i < n; i++) for (j = 0; j < n; j++) { Hm[i][j] = A[i][j]; Hm[i][n + j] = -B[i][0] * B[j][0] / R; Hm[n + i][j] = -(i === j ? Q[i] : 0); Hm[n + i][n + j] = -A[j][i]; }
...
for (var it = 0; it < 100; it++) { var Zi = inv(Z), dn = 0, Zn = zeros(12, 12);
for (i = 0; i < 12; i++) for (j = 0; j < 12; j++) { Zn[i][j] = 0.5 * (Z[i][j] + Zi[i][j]); dn += Math.abs(Zn[i][j] - Z[i][j]); } Z = Zn; if (dn < 1e-12) break; }
...
var P = mul(inv(mul(Lt, Lm)), mul(Lt, Rm)), K = [];
for (j = 0; j < n; j++) { var s = 0; for (i = 0; i < n; i++) s += B[i][0] * P[i][j]; K.push(s / R); } return ⟦K|K⟧; }`,
            syms: [['K', 'K', 'K', 'gains on (x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂), N/m, N/rad, N s/m, N s/rad']]
        },
        {
            title: 'The push: sampled and limited',
            where: 'control() and step()',
            math: '⟦u|u⟧ = clip(−K(s − s<sub>ref</sub>), ±u<sub>max</sub>), held for ⟦Ts|T<sub>s</sub>⟧',
            note: 'control() forms the error e = s − s<sub>ref</sub> (only x has a target, xref, set by the buttons), multiplies by −K and clips the result to ±u<sub>max</sub> from the slider: the motor cannot push harder. It returns 0 when the controller is off or the run is lost. step() asks for a new u only when the simulated time tSim has reached the next sampling instant tCtl, then moves tCtl on by T<sub>s</sub>; between samples the old u is held, exactly the zero-order hold of §7.2. When a rod passes 60° the run is lost, u is set to 0, and the equations keep being solved, so the rods fall all the way and swing on.',
            code: `var e = s.slice(); e[0] -= xref; var v = 0; for (var i = 0; i < 6; i++) v -= K[i] * e[i];
var F = sF.value; return Math.max(-F, Math.min(F, v)); }
...
if (tSim >= tCtl - 1e-9) { ⟦u|u = control()⟧; tCtl += ⟦Ts|Ts⟧; }
...
if (!lost && (Math.abs(s[1]) > LOST || Math.abs(s[2]) > LOST)) { lost = true; u = 0; }`,
            syms: [['u', 'u', 'u', 'motor force now, N'], ['Ts', 'T<sub>s</sub>', 'Ts', 'loop period, s']]
        },
        {
            title: 'The flick',
            where: 'flick(J), from the two Flick buttons',
            math: 'Δθ̇ = D<sup>−1</sup> (1, L<sub>1</sub> cos θ<sub>1</sub>, L<sub>2</sub> cos θ<sub>2</sub>)<sup>T</sup> ⟦J|J⟧<span style="font-style:normal;margin-left:1.5em">(17)</span>',
            note: 'The right-hand side is the generalised impulse of a horizontal blow J at the top end, in N s. Solving with D at the current angles gives the jump of the three rates, which is added to s[3], s[4] and s[5]; the positions do not jump. A blow to the right sets the cart moving right, the lower rod turning left and the upper rod turning right, the same pattern the note derives.',
            code: `var dq = solve3(Dm(p, s[1], s[2]), [⟦J|J⟧, p.L1 * Math.cos(s[1]) * J, p.L2 * Math.cos(s[2]) * J]);
s[3] += dq[0]; s[4] += dq[1]; s[5] += dq[2]; }`,
            syms: [['J', 'J', 'J', 'impulse of the blow at the top end, N s']]
        }
    ]
};
