/* From symbols to code — Fig. 11, Balancing Two Rods on a Cart (double-inverted-pendulum.html).
   Each step pairs an equation of the lecture note with the lines of the page's script that compute it, copied character for character.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), defined in the page next to its state. */
window.WALK = window.WALK || {};

window.WALK.dipc = {
    intro: 'Fifteen steps from the lecture note to the moving picture, in the order the page uses them: the constants of the machine (6) and (7), the matrix D of (5), the equations of motion (9), the Runge–Kutta step (18), the linearisation (10) and (11), the fall rates (12) and (13), the controller from the Riccati equation (15) and (16), the machine between two looks (16a), (16b) and (16f), the gains for the loop period (16g) and (16h), the sampled and limited push, the flick (17), the certified catch level (19a), calming (21), the planned swing-up with its tracking law (24), and the family of moving equilibria (25) with the glide (26). Each step sets the equation beside the lines of this page’s script that evaluate it, copied character for character; a line that is only “...” stands for page lines left out. The table gives each symbol, its name in the code, its value now, and its meaning with its unit. Hover over or tap a symbol to light it in all three places.',
    steps: [
        {
            title: 'The constants of the machine',
            where: 'par(): read from the sliders whenever one moves',
            math: '⟦d1|d<sub>1</sub>⟧ = m<sub>0</sub>+m<sub>1</sub>+m<sub>2</sub>, d<sub>2</sub> = (½m<sub>1</sub>+m<sub>2</sub>)L<sub>1</sub>, d<sub>3</sub> = ½m<sub>2</sub>L<sub>2</sub>,<br>d<sub>4</sub> = (⅓m<sub>1</sub>+m<sub>2</sub>)L<sub>1</sub>², d<sub>5</sub> = ½m<sub>2</sub>L<sub>1</sub>L<sub>2</sub>, d<sub>6</sub> = ⅓m<sub>2</sub>L<sub>2</sub>²<span style="font-style:normal;margin-left:1.5em">(6)</span><br>⟦f1|f<sub>1</sub>⟧ = (½m<sub>1</sub>+m<sub>2</sub>)L<sub>1</sub>g, f<sub>2</sub> = ½m<sub>2</sub>L<sub>2</sub>g<span style="font-style:normal;margin-left:1.5em">(7)</span>',
            note: 'The masses m<sub>0</sub>, m<sub>1</sub>, m<sub>2</sub> in kg and the lengths L<sub>1</sub>, L<sub>2</sub> in m are read from their sliders, and the eight constants of the note are computed once, in the order of (6) and (7): the array d holds d<sub>1</sub> … d<sub>6</sub> (d[0] is d<sub>1</sub>, because arrays count from 0), in kg, kg m and kg m², and the array f holds f<sub>1</sub>, f<sub>2</sub> in N m. G is g = 9.81 m/s², fixed at the top of the script together with the Runge–Kutta step H = h = 1 ms and the weights Q of (14). Every other function reads only p.d and p.f, so a slider changes the physics everywhere at once. With a medium (section 13), par also builds p.fl, the medium’s density and viscosity and the drag constants of (33)–(34), and takes the buoyancy (37) off f: the rods weigh less in water.',
            code: `var TH = Sim.theme, G = 9.81, H = 0.001, Q = [50, 50, 50, 20, 700, 700];
...
function par() { var m0 = sl.m0.value, m1 = sl.m1.value, m2 = sl.m2.value, L1 = sl.L1.value, L2 = sl.L2.value, fl = fluidPar(L1, L2), bA = fl ? fl.rho * Math.PI * ROD_R * ROD_R * G : 0, ma = fl ? { mu: CA_ROD * fl.rho * Math.PI * ROD_R * ROD_R, mc: solved() ? fl.rho * CART_B * CART_A2 : fl.rho * CART_VE * CART_KX / (2 - CART_KX) } : null;   // solved: the cart fills the tank's depth, so its added mass is the 2D one (13.6)
return { m0: m0, m1: m1, m2: m2, L1: L1, L2: L2, ⟦d1|d: [m0 + m1 + m2⟧, (m1 / 2 + m2) * L1, m2 * L2 / 2, (m1 / 3 + m2) * L1 * L1, m2 * L1 * L2 / 2, m2 * L2 * L2 / 3], ⟦f1|f: [(m1 / 2 + m2) * L1 * G⟧ - bA * (L1 * L1 / 2 + L1 * L2), m2 * L2 * G / 2 - bA * L2 * L2 / 2], fl: fl, ma: ma }; }   // f with the buoyancy (37) of the medium, ma its added mass (38)`,
            syms: [['d1', 'd<sub>1</sub>', 'p.d[0]', 'everything that moves with the cart, kg'], ['f1', 'f<sub>1</sub>', 'p.f[0]', 'gravity’s torque factor of the lower rod, N m']]
        },
        {
            title: 'The matrix of the kinetic energy',
            where: 'Dm(p, a, b): D at the angles a = θ<sub>1</sub>, b = θ<sub>2</sub>',
            math: 'T = ½ θ̇<sup>T</sup> D(θ) θ̇,  D = [[d<sub>1</sub>, d<sub>2</sub> cos ⟦t1|θ<sub>1</sub>⟧, d<sub>3</sub> cos ⟦t2|θ<sub>2</sub>⟧], [d<sub>2</sub> cos θ<sub>1</sub>, d<sub>4</sub>, d<sub>5</sub> cos(θ<sub>1</sub> − θ<sub>2</sub>)], [d<sub>3</sub> cos θ<sub>2</sub>, d<sub>5</sub> cos(θ<sub>1</sub> − θ<sub>2</sub>), d<sub>6</sub>]]<span style="font-style:normal;margin-left:1.5em">(5)</span>',
            note: 'Dm returns the 3 × 3 matrix D of (5) as an array of three rows. c1, c2 and c12 are the three cosines that appear in it, computed once each. The diagonal holds the constant inertias d<sub>1</sub>, d<sub>4</sub>, d<sub>6</sub>; the off-diagonal places hold the couplings, which shrink as the rods lean, because a leaning rod turns partly up and down instead of sideways. D is symmetric, as every kinetic-energy matrix is, and positive definite, so it can always be inverted: that is what the next step relies on. With a medium, addedMass adds the matrix of the water each rod carries (38), which depends on the angles too: only motion across a rod drags water along.',
            code: `function Dm(p, a, b) { var d = p.d, c1 = Math.cos(a), c2 = Math.cos(b), c12 = Math.cos(a - b), M = [[d[0], d[1] * c1, d[2] * c2], [d[1] * c1, d[3], d[4] * c12], [d[2] * c2, d[4] * c12, d[5]]]; if (p.ma) addedMass(M, p, c1, c2, c12); return M; }`,
            syms: [['t1', 'θ<sub>1</sub>', 's[1]', 'lower rod angle from the upward vertical, rad'], ['t2', 'θ<sub>2</sub>', 's[2]', 'upper rod angle from the upward vertical, rad']]
        },
        {
            title: 'The equations of motion',
            where: 'rhs(p, s, u, t): the right-hand side ṡ = f(s, u, t)',
            math: 'D(θ) ⟦acc|θ̈⟧ = H ⟦u|u⟧ − C(θ, θ̇) θ̇ − G(θ)<span style="font-style:normal;margin-left:1.5em">(9)</span><br>C θ̇ = (−d<sub>2</sub> sin θ<sub>1</sub> θ̇<sub>1</sub>² − d<sub>3</sub> sin θ<sub>2</sub> θ̇<sub>2</sub>², d<sub>5</sub> sin(θ<sub>1</sub>−θ<sub>2</sub>) θ̇<sub>2</sub>², −d<sub>5</sub> sin(θ<sub>1</sub>−θ<sub>2</sub>) θ̇<sub>1</sub>²)<br>G = (0, −f<sub>1</sub> sin θ<sub>1</sub>, −f<sub>2</sub> sin θ<sub>2</sub>)',
            note: 'The state s holds six numbers: s[0] = x in m, s[1] = θ<sub>1</sub> and s[2] = θ<sub>2</sub> in rad, and their rates s[3] = ẋ in m/s, s[4] = θ̇<sub>1</sub> and s[5] = θ̇<sub>2</sub> in rad/s. rhs returns how fast each of them changes. The page never forms the matrix C: it multiplies it by θ̇ on paper first (the second line of the formula, which is (8a), (8) and (8b) read off) and computes the three products directly as Cq, in N. Gv is the gravity vector G in N m. solve3 then solves the 3 × 3 linear system D θ̈ = Hu − Cθ̇ − G for the accelerations q = (ẍ, θ̈<sub>1</sub>, θ̈<sub>2</sub>) by Gaussian elimination with pivoting, which is cheaper and more accurate than forming D<sup>−1</sup>. The force u enters only the first row, because H = (1, 0, 0): the motor pushes the cart and nothing else. With a medium, fluidQ adds the fluid’s generalised forces Q of (35), in N and N m, to the right-hand side; the extra argument t is the time, because a flow can change from moment to moment.',
            code: `function rhs(p, s, u, t) { var a = s[1], b = s[2], ad = s[4], bd = s[5], d = p.d, sab = Math.sin(a - b), Qf = p.fl ? fluidQ(p, s, t) : null;
var Cq = [-d[1] * Math.sin(a) * ad * ad - d[2] * Math.sin(b) * bd * bd, d[4] * sab * bd * bd, -d[4] * sab * ad * ad];   // C θ̇, row by row
var Gv = [0, -p.f[0] * Math.sin(a), -p.f[1] * Math.sin(b)];
if (Qf) { Gv[0] -= Qf[0]; Gv[1] -= Qf[1]; Gv[2] -= Qf[2]; }   // (35): the fluid's Q on the right of (9), moved to the left with G
var ⟦acc|q = solve3(Dm(p, a, b), [u - Cq[0] - Gv[0], -Cq[1] - Gv[1], -Cq[2] - Gv[2]])⟧, k = [s[3], s[4], s[5], q[0], q[1], q[2]]; k.P = Qf ? Qf[3] : 0;
return k; }`,
            syms: [['acc', 'θ̈', 'q', 'accelerations (ẍ, θ̈₁, θ̈₂), m/s² and rad/s²'], ['u', 'u', 'u', 'motor force on the cart, N']]
        },
        {
            title: 'One Runge–Kutta step',
            where: 'rk4(p, s, u, h, t), called from step() every 1 ms of simulated time',
            math: 'k<sub>1</sub> = f(s<sub>n</sub>), k<sub>2</sub> = f(s<sub>n</sub> + ½h k<sub>1</sub>), k<sub>3</sub> = f(s<sub>n</sub> + ½h k<sub>2</sub>), k<sub>4</sub> = f(s<sub>n</sub> + h k<sub>3</sub>)<br>s<sub>n+1</sub> = s<sub>n</sub> + ⟦h|h⟧/6 (k<sub>1</sub> + 2k<sub>2</sub> + 2k<sub>3</sub> + k<sub>4</sub>)<span style="font-style:normal;margin-left:1.5em">(18)</span>',
            note: 'rk4 evaluates the slope of step 3 four times, at the start of the step, twice at its middle and at its end, and advances the state by their weighted mean. add(s, k, h) is the state s moved along the slope k for a time h. The force u is the same in all four evaluations, because the sampled controller holds it constant between its samples. The screen asks for a new picture about 60 times a second; step() runs as many 1 ms steps as real time has passed since the last picture (acc collects the time), so the simulation keeps real time whatever the frame rate. The time t goes along, so that a changing flow is taken at the start, the middle and the end of the step; rk4.W is the fluid’s work in the step, summed with the same weights as the state, for the energy book.',
            code: `function rk4(p, s, u, h, t) { var k1 = rhs(p, s, u, t), k2 = rhs(p, add(s, k1, h / 2), u, t + h / 2), k3 = rhs(p, add(s, k2, h / 2), u, t + h / 2), k4 = rhs(p, add(s, k3, h), u, t + h);
rk4.W = h / 6 * (k1.P + 2 * k2.P + 2 * k3.P + k4.P);   // the fluid's work in the step, (36), with the weights RK4 gives the state
return s.map(function (v, i) { return v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]); }); }
...
s = rk4(p, s, u, H, tSim); Wfl += rk4.W; tSim += H;`,
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
            note: 'Hm is the 12 × 12 Hamiltonian matrix of §7.1 and R is ρ. The loop replaces Z by the mean of Z and its inverse until nothing changes by more than 10<sup>−12</sup> in total; the limit is the matrix sign W. Lm and Rm are the two 12 × 6 blocks of the last equation, and P = (Lm<sup>T</sup>Lm)<sup>−1</sup>Lm<sup>T</sup>Rm is its least-squares solution. The last line is (16): K<sub>j</sub> = Σ<sub>i</sub> B<sub>i</sub>P<sub>ij</sub>/ρ. The gains are recomputed for every slider change, so the controller always knows the machine it holds. P is returned too, made exactly symmetric, because the catch level of §9 is built from it.',
            code: `for (i = 0; i < n; i++) for (j = 0; j < n; j++) { Hm[i][j] = A[i][j]; Hm[i][n + j] = -B[i][0] * B[j][0] / R; Hm[n + i][j] = -(i === j ? Q[i] : 0); Hm[n + i][n + j] = -A[j][i]; }
...
for (var it = 0; it < 100; it++) { var Zi = inv(Z), dn = 0, Zn = zeros(12, 12);
for (i = 0; i < 12; i++) for (j = 0; j < 12; j++) { Zn[i][j] = 0.5 * (Z[i][j] + Zi[i][j]); dn += Math.abs(Zn[i][j] - Z[i][j]); } Z = Zn; if (dn < 1e-12) break; }
...
var P = mul(inv(mul(Lt, Lm)), mul(Lt, Rm)), K = [];
for (j = 0; j < n; j++) { var s = 0; for (i = 0; i < n; i++) s += B[i][0] * P[i][j]; K.push(s / R); }
for (i = 0; i < n; i++) for (j = 0; j < i; j++) P[i][j] = P[j][i] = (P[i][j] + P[j][i]) / 2;
return { K: ⟦K|K⟧, P: P }; }`,
            syms: [['K', 'K', 'K', 'gains on (x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂), N/m, N/rad, N s/m, N s/rad']]
        },
        {
            title: 'The machine between two looks',
            where: 'sampledModel(A, B, R, T), called by redesign() whenever a slider moves',
            math: 'e<sup>Ā T<sub>s</sub></sup> = [[⟦Phi|Φ⟧, ⟦Gam|Γ⟧], [0, 1]],  Ā = [[A, B], [0, 0]]<span style="font-style:normal;margin-left:1.5em">(16b)</span><br>exp([[−Ā<sup>T</sup>, Q̄], [0, Ā]] T<sub>s</sub>) = [[F<sub>11</sub>, F<sub>12</sub>], [0, F<sub>22</sub>]],  [[Q<sub>d</sub>, N<sub>d</sub>], [N<sub>d</sub><sup>T</sup>, ⟦Rd|R<sub>d</sub>⟧]] = F<sub>22</sub><sup>T</sup>F<sub>12</sub><span style="font-style:normal;margin-left:1.5em">(16f)</span>',
            note: 'Ab is the 7 × 7 matrix Ā of §7.2: A and B side by side, a last row of zeros for the rule u̇ = 0 that says the force is held. One call of expm() (scaling and squaring: halve until small, 18 terms of the series, square back) gives e<sup>Ā T</sup>, whose top six rows are Φ and Γ of (16a). C is the 14 × 14 block matrix of Van Loan’s identity: −Ā<sup>T</sup> T in the upper-left corner, Ā T in the lower right, and Q̄ T = diag(Q, ρ) T in the upper right, where the loop puts Q[i] on the diagonal and R = ρ in the last place. A second exponential gives F; F12 and F22 are its two right-hand blocks, and Mi = F22<sup>T</sup>F12 is the 7 × 7 matrix of (16f), made exactly symmetric on the next page line. Its upper-left 6 × 6 block is Q<sub>d</sub>, its last column N<sub>d</sub>, its corner R<sub>d</sub>: the exact cost of one period with the force held.',
            code: `function sampledModel(A, B, R, T) {   // (16b): Φ and Γ from one exponential; (16f): the exact sampled cost Q_d, N_d, R_d from another (Van Loan)
...
var E = expm(Ab.map(function (r) { return r.map(function (v) { return v * T; }); }));
for (i = 0; i < 7; i++) for (j = 0; j < 7; j++) { C[i][j] = -Ab[j][i] * T; C[7 + i][7 + j] = Ab[i][j] * T; }
for (i = 0; i < 6; i++) C[i][7 + i] = Q[i] * T; C[6][13] = R * T;
var F = expm(C), F12 = F.slice(0, 7).map(function (r) { return r.slice(7); }), F22 = F.slice(7).map(function (r) { return r.slice(7); }), Mi = mul(tp(F22), F12);`,
            syms: [['Phi', 'Φ', 'Phi', 'where the machine drifts on its own in one period, e<sup>A T<sub>s</sub></sup>'], ['Gam', 'Γ', 'Gam', 'what one newton held for one period does to the state'], ['Rd', 'R<sub>d</sub>', 'Rd', 'cost of one newton held for one period, ≈ ρ T<sub>s</sub>']]
        },
        {
            title: 'The gains for the loop period',
            where: 'dlqr(A, B, R, T) and redesign(), whenever a slider or the switch Gains designed for moves',
            math: 'P = Q<sub>d</sub> + Φ<sup>T</sup>PΦ − (Φ<sup>T</sup>PΓ + N<sub>d</sub>)(R<sub>d</sub> + Γ<sup>T</sup>PΓ)<sup>−1</sup>(Γ<sup>T</sup>PΦ + N<sub>d</sub><sup>T</sup>)<span style="font-style:normal;margin-left:1.5em">(16g)</span><br>⟦K|K<sub>d</sub>⟧ = (R<sub>d</sub> + Γ<sup>T</sup>PΓ)<sup>−1</sup>(Γ<sup>T</sup>PΦ + N<sub>d</sub><sup>T</sup>)<span style="font-style:normal;margin-left:1.5em">(16h)</span><br>⟦lam||λ|⟧ = lim ‖(Φ − ΓK)<sup>n</sup>‖<sup>1/n</sup>',
            note: 'The first line removes the cross term: Ak = Φ − ΓR<sub>d</sub><sup>−1</sup>N<sub>d</sub><sup>T</sup>, Gk = ΓR<sub>d</sub><sup>−1</sup>Γ<sup>T</sup>, Hk = Q<sub>d</sub> − N<sub>d</sub>R<sub>d</sub><sup>−1</sup>N<sub>d</sub><sup>T</sup>, the Â, G, Q̂ of §7.5. The loop is the doubling algorithm: Wi = (I + G<sub>k</sub>H<sub>k</sub>)<sup>−1</sup>, then the three recursions of the note, each step doubling the number of periods H looks ahead; it stops when H changes by less than 10<sup>−13</sup> of itself, and H is P. The last two lines are (16h): GP = Γ<sup>T</sup>P, den = R<sub>d</sub> + Γ<sup>T</sup>PΓ (a number, since there is one motor), num = Γ<sup>T</sup>PΦ + N<sub>d</sub><sup>T</sup>. In redesign() the switch chooses: gmode = \'sampled\' takes these gains, otherwise lqr() of the step before. Either way the page forms the sampled loop Φ − ΓK and takes its largest factor per look with specRad(), stored once as lamNow and shown in the panel; −T<sub>s</sub>/ln|λ| is the settling time beside it.',
            code: `var Ak = madd(Phi, mul(Gam, tp(Nd)), -1 / Rd), Gk = mul(Gam, tp(Gam)).map(function (r) { return r.map(function (v) { return v / Rd; }); }), Hk = madd(S.Qd, mul(Nd, tp(Nd)), -1 / Rd);
for (var it = 0; it < 60; it++) { var Wi = inv(madd(eye(6), mul(Gk, Hk), 1)), AW = mul(Ak, Wi);
var An = mul(AW, Ak), Gn = madd(Gk, mul(mul(AW, Gk), tp(Ak)), 1), Hn = madd(Hk, mul(mul(tp(Ak), Hk), mul(Wi, Ak)), 1), dh = 0, hn = 0;
...
var GP = mul(tp(Gam), Hk), den = Rd + mul(GP, Gam)[0][0], num = madd(mul(GP, Phi), tp(Nd), 1)[0];
return { ⟦K|K: num.map(function (v) { return v / den; })⟧, P: Hk, Phi: Phi, Gam: Gam }; }
...
p = par(); var L = linear(p), Rr = Math.pow(10, sR.value), Ts = sT.value / 1000, Lq = gmode === 'sampled' ? dlqr(L.A, L.B, Rr, Ts) : lqr(L.A, L.B, Rr); K = Lq.K; Pm = Lq.P; Smod = sampledModel(L.A, L.B, Rr, Ts);
...
var lam = ⟦lam|lamNow = specRad(Acl)⟧, sg = fallRates(p);`,
            syms: [['K', 'K<sub>d</sub>', 'K', 'gains in use on (x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂), N/m, N/rad, N s/m, N s/rad'], ['lam', '|λ|', 'lamNow', 'largest factor per look of the sampled loop; below 1 the loop holds']]
        },
        {
            title: 'The push: sampled and limited',
            where: 'control() and step()',
            math: '⟦u|u⟧ = clip(−K(s − s<sup>∗</sup>(t)), ±u<sub>max</sub>), held for ⟦Ts|T<sub>s</sub>⟧',
            note: 'err() forms the error e = s − s<sup>∗</sup>(t), measured from the reference equilibrium of the moment: refXV(t) gives its place and speed (a resting place at the target of the buttons, a cruise, or a glide; the last step), and the angles are first brought into −π…π, so a rod that has turned over once is upright again. lqrU() multiplies the error by −K and clips the result to ±u<sub>max</sub> from the slider: the motor cannot push harder. step() asks for a new u only when the simulated time tSim has reached the next sampling instant tCtl, then moves tCtl on by the period: T<sub>s</sub> from the slider while balancing, 10 ms while calming or tracking; between samples the old u is held, exactly the zero-order hold of §7.2. Before that, supervise() decides which law is in charge (the steps below).',
            code: `function err(st, t) { var e = wrapState(st), rv = refXV(t); e[0] -= rv[0]; e[3] -= rv[1]; return e; }   // the state measured from the reference equilibrium
...
function lqrU(st, t) { var e = err(st, t), v = 0; for (var i = 0; i < 6; i++) v -= K[i] * e[i]; return clampF(v); }
...
supervise();
if (tSim >= tCtl - 1e-9) { ⟦u|u = control()⟧; tCtl += period(); }
s = rk4(p, s, u, H, tSim); Wfl += rk4.W; tSim += H;`,
            syms: [['u', 'u', 'u', 'motor force now, N'], ['Ts', 'T<sub>s</sub>', 'Ts', 'loop period, s']]
        },
        {
            title: 'The flick',
            where: 'flick(J), from the two Flick buttons',
            math: 'Δθ̇ = D<sup>−1</sup> (1, L<sub>1</sub> cos θ<sub>1</sub>, L<sub>2</sub> cos θ<sub>2</sub>)<sup>T</sup> ⟦J|J⟧<span style="font-style:normal;margin-left:1.5em">(17)</span>',
            note: 'The right-hand side is the generalised impulse of a horizontal blow J at the top end, in N s. Solving with D at the current angles gives the jump of the three rates, which is added to s[3], s[4] and s[5]; the positions do not jump. A blow to the right sets the cart moving right, the lower rod turning left and the upper rod turning right, the same pattern the note derives.',
            code: `var dq = solve3(Dm(p, s[1], s[2]), [⟦J|J⟧, p.L1 * Math.cos(s[1]) * J, p.L2 * Math.cos(s[2]) * J]);
s[3] += dq[0]; s[4] += dq[1]; s[5] += dq[2]; nextCheck = tSim; abandon(); }`,
            syms: [['J', 'J', 'J', 'impulse of the blow at the top end, N s']]
        },
        {
            title: 'Where the balancer is certain to win',
            where: 'Wof(st, t) and catchGen(), recomputed with the gains between frames by think(); supervise() every 0.1 s',
            math: '⟦W|W⟧ = (s − s<sup>∗</sup>)<sup>T</sup> P (s − s<sup>∗</sup>)<span style="font-style:normal;margin-left:1.5em">(19)</span><br>⟦c|c*⟧ = largest c with W(F(s)) &lt; W(s) for every s with 0 &lt; W(s) ≤ c<span style="font-style:normal;margin-left:1.5em">(19a)</span>',
            note: 'Wof() is the cost (19) still to pay from the state st, measured from the reference of the moment. catchGen() is a generator: think() runs it a few milliseconds between frames, and while it runs the page has no c* and skips the checks that need it. It writes P = LL<sup>T</sup> (Cholesky); a point x = L<sup>−T</sup>(√c · d) with |d| = 1 then lies on the surface W = c. dW() is one loop period of the true equations from that point with the clipped push held, F(s) of (19a), and returns W(F(s)) − W(s). jacobi() finds the eigenvectors of the linear fall per look in the coordinates d; the three weakest are where the search climbs first, both ways and on every shell, then from the worst six of 1500 random directions spread over the shells W = c, 0.7c, 0.4c, 0.15c. The bisection halves the interval from 1 to 10<sup>4</sup> thirteen times on a logarithmic scale. supervise() uses c*: outside it, the equations are run 4 s ahead with the balancer in charge, and if the state is still outside c* then, the rescue starts.',
            code: `function Wof(st, t) { return quad(Pm, err(st, t)); }   // the remaining LQR cost (19); below cLevel the balancer is certain to catch
...
var x = backsolve(Lc, dir.map(function (a) { return a * Math.sqrt(c); })), uu = 0, a;
...
for (a = 0; a < 6; a++) y[a] = x[a]; stepF(p, y, uu, h, n, y); return Wq(y) - Wq(x); }
...
var eg = jacobi(Mz), order = [0, 1, 2, 3, 4, 5].sort(function (a, b) { return eg.vals[a] - eg.vals[b]; }), weak = order.slice(0, 3).map(function (o) { return eg.vecs[o]; });
...
for (var bi = 0; bi < 13; bi++) { var mid = Math.sqrt(lo * hi); if (yield* safe(mid)) lo = mid; else hi = mid; }
...
if (Wof(s, tSim) > cLevel) {   // outside the certified region: ask the model whether the balancer still wins within 4 s
var pr = run({ s: s, t: tSim, tc: tCtl, u: u }, tSim + 4, lqrU);
if (Wof(pr.s, pr.t) > cLevel) { if (rescue) { mode = 'calm'; xc = rolling ? s[0] : xref; ref = { kind: 'fixed', x: xc }; log.push({ t: tSim, ev: 'rescue' }); startAttempt(); } else { lost = true; u = 0; } } } }`,
            syms: [['W', 'W', 'W', 'remaining balancing cost now'], ['c', 'c*', 'c', 'certified catch level']]
        },
        {
            title: 'Calming: draining the rods’ energy',
            where: 'calmU(st), every 10 ms while the mode is calm',
            math: 'd⟦Ep|E<sub>p</sub>⟧/dt = −a 𝒫,  𝒫 = d<sub>2</sub> cos θ<sub>1</sub> θ̇<sub>1</sub> + d<sub>3</sub> cos θ<sub>2</sub> θ̇<sub>2</sub><span style="font-style:normal;margin-left:1.5em">(21)</span><br>a = k𝒫 − 4(x − x<sub>c</sub>) − 4ẋ,  |a| ≤ 8 m/s²',
            note: 'P here is the rods’ turning momentum 𝒫 of (21), in kg m/s. With k = CALM_K = 2 the cart accelerates with the rods’ momentum, so their energy (20) can only fall; the two other terms keep the cart near its post x<sub>c</sub>. uFor() turns the wanted acceleration into a motor force: rows 2 and 3 of (9) give the angular accelerations for that a, row 1 then gives u.',
            code: `var d = p.d, P = d[1] * Math.cos(st[1]) * st[4] + d[2] * Math.cos(st[2]) * st[5];
var a = Math.max(-8, Math.min(8, CALM_K * P - 4 * (st[0] - xc) - 4 * st[3])); return clampF(uFor(st, a)); }`,
            syms: [['Ep', 'E<sub>p</sub>', 'Ep', 'energy of the rods now, J']]
        },
        {
            title: 'Plan, track, catch',
            where: 'startAttempt(), PlanJob(...).work(ms) between frames, trackU() every 10 ms',
            math: 'minimise Σ |residuals (22)|² over z<sub>1…M</sub>, u<sub>0…M−1</sub><br>⟦u|u⟧<sub>k</sub> = u<sup>plan</sup><sub>k</sub> − K<sub>k</sub>(s<sub>k</sub> − s<sup>plan</sup><sub>k</sub>)<span style="font-style:normal;margin-left:1.5em">(24)</span>',
            note: 'startAttempt() runs the calming law hp seconds ahead (3 s at first) with run(), the same loop that moves the machine, and plans from the state it finds there, with the cart’s post xc subtracted. The plan is made a few milliseconds per frame. When the clock reaches that moment, supervise() checks that the machine is where the prediction said, to 10<sup>−6</sup>, and switches to tracking. trackU() looks up the plan’s force, state and gain K<sub>k</sub> of (23) for the current 10 ms step; if the state has strayed more than 0.5 from the plan it calms again, and when W falls below 0.9 c* the balancer takes over. The plan’s last residual on the cart’s speed carries the weight lim.vw: 0.3 with Stop the cart, as in (22), and 0 with Keep rolling, so the plan may end on any member of the family (25).',
            code: `var pr = run({ s: s, t: tSim, tc: tCtl, u: u }, tSim + hp, calmU), s0 = pr.s.slice(); s0[0] -= xc;
...
var k = Math.round((tSim - tPlan) / 0.01); if (k >= tv.n) return 'end';
var v = tv.un[k], dev = 0; for (var j = 0; j < 6; j++) { var e = s[j] - (j === 0 ? xc : 0) - tv.nom[6 * k + j]; dev += e * e; v -= tv.Kt[6 * k + j] * e; }
...
R[ri] = WT * lim.vw * Xv[t0 + 3]; if (wantJ) { cols[0] = t0 + 3; vals[0] = WT * lim.vw; acc(1, R[ri]); } ri++;   // lim.vw = 0: the plan may arrive moving (25)`,
            syms: [['u', 'u', 'u', 'motor force now, N']]
        },
        {
            title: 'Moving equilibria and the glide',
            where: 'refXV(t), Wred(st), the hand-over in supervise(), the target buttons',
            math: 's<sup>∗</sup>(t) = (x<sub>0</sub> + vt, 0, 0, v, 0, 0),  u<sup>∗</sup> = 0<span style="font-style:normal;margin-left:1.5em">(25)</span><br>e(τ) = (e<sub>0</sub> + (v + ωe<sub>0</sub>)τ) e<sup>−ωτ</sup>,  e = ⟦xr|x<sub>ref</sub>⟧ − x<sub>target</sub>,  ω = 0.5 s<sup>−1</sup><span style="font-style:normal;margin-left:1.5em">(26)</span><br>⟦Wr|W<sub>red</sub>⟧ = W with the x and ẋ errors set to zero',
            note: 'ref is the member of the family (25) the balancer holds. refXV(t) returns its place and speed at time t: for a fixed place, the place and 0; for a cruise, x<sub>0</sub> + vτ and v; for a glide, (26) written out, with b = v + ωe<sub>0</sub> so that e = (e<sub>0</sub> + bτ)e<sup>−ωτ</sup> and its speed (b − ω(e<sub>0</sub> + bτ))e<sup>−ωτ</sup>. GLIDE is ω. When a swing-up is caught with Keep rolling on, the hand-over tests Wred(), the cost (19) with the cart’s place and speed errors left out, and then sets the reference to a cruise at the place and speed the cart has at that moment. A target button, pressed while the reference moves, starts a glide from the reference’s present place and speed to the resting member at the target; pressed at rest, it moves the target in one step, as before.',
            code: `function refXV(t) { if (ref.kind === 'fixed') return [ref.x, 0];
var tau = t - ref.t0; if (ref.kind === 'cruise') return [ref.x + ref.v * tau, ref.v];
var ex = Math.exp(-GLIDE * tau), b = ref.v + GLIDE * ref.e0; return [ref.target + (ref.e0 + b * tau) * ex, (b - GLIDE * (ref.e0 + b * tau)) * ex]; }
...
function Wred(st) { return quad(Pm, [0, wrapAngle(st[1]), wrapAngle(st[2]), 0, st[4], st[5]]); }   // (19) about the moving equilibrium the cart is on now (25)
...
if (mode === 'track' && cLevel && tSim - tPlan > 0.05 && (rolling ? ⟦Wr|Wred(s)⟧ : Wof(s, tSim)) < 0.9 * cLevel) {   // inside the certified region, with 10 % to spare for what the search may miss: hand over
...
if (rolling) ref = { kind: 'cruise', x: s[0], v: s[3], t0: tSim, brake: true };   // keep the speed it arrived with: a moving equilibrium (25), then brake it away bite by bite (27)
...
else { var rv = refXV(tSim); ref = { kind: 'glide', target: tg, e0: rv[0] - tg, v: rv[1], t0: tSim }; }   // moving: glide along the family of equilibria (26)`,
            syms: [['xr', 'x<sub>ref</sub>', 'refXV(tSim)[0]', 'place of the reference equilibrium now, m'], ['Wr', 'W<sub>red</sub>', 'Wred(s)', 'remaining cost about the moving equilibrium the cart is on']]
        },
        {
            title: 'Braking to rest, one certified bite at a time',
            where: 'govern(), called by control() at every look while the cart brakes after a rolling catch',
            math: 'W(e + Δ e<sub>4</sub>) = W(e) + 2Δ (Pe)<sub>4</sub> + Δ<sup>2</sup> P<sub>44</sub><span style="font-style:normal;margin-left:1.5em">(27)</span><br>Δ<sub>max</sub> = [−(Pe)<sub>4</sub> + √((Pe)<sub>4</sub><sup>2</sup> − P<sub>44</sub>(W(e) − γc<sup>∗</sup>))] / P<sub>44</sub>,  ⟦eps|ε⟧ = √(γc<sup>∗</sup>/P<sub>44</sub>),  γ = 0.5<span style="font-style:normal;margin-left:1.5em">(27a)</span>',
            note: 'Lowering the reference speed by Δ at a look changes nothing in the machine but adds Δ to the error in ẋ, which the balancer cannot tell from a shove. The code first moves the reference to the cart (the error in x becomes zero, which (25) allows), forms the error e with the present speed, and takes the largest bite toward zero that keeps W within γc<sup>∗</sup>. After the bite the reference is again a member of (25), so the certificate (19a) holds over the next period. If no bite fits, the old reference stays. At zero speed the reference becomes a fixed place where the cart stands.',
            code: `function govern() {   // (27): at a look, put the reference at the cart and take the largest bite of its speed toward zero with W ≤ γ c* (a reference governor)
...
var v0 = refXV(tSim)[1], sg = v0 > 0 ? 1 : -1, e = wrapState(s), Pe4 = 0, i; e[0] = 0; e[3] -= v0;   // the error from the member of (25) at the cart with the present speed
for (i = 0; i < 6; i++) Pe4 += Pm[3][i] * e[i];
var disc = Pe4 * Pe4 - Pm[3][3] * (quad(Pm, e) - GAMMA * cLevel); if (disc < 0) return;   // no bite fits: the old reference stays, and the certificate goes on
var hi = (-sg * Pe4 + Math.sqrt(disc)) / Pm[3][3], lo = (-sg * Pe4 - Math.sqrt(disc)) / Pm[3][3], D = Math.min(Math.abs(v0), hi);
if (D < Math.max(0, lo)) return;
bite = D; vBefore = v0; var vn = v0 - sg * D;
if (vn === 0) { ref = { kind: 'fixed', x: s[0] }; xref = s[0]; } else ref = { kind: 'cruise', x: s[0], v: vn, t0: tSim, brake: true }; }`,
            syms: [['eps', 'ε', 'Math.sqrt(GAMMA * cLevel / Pm[3][3])', 'certified bite of speed from rest at γ = 0.5, m/s']]
        }
    ]
};
