/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state.
   Fig. 12, Furuta pendulum: the steps follow the lecture note's order and its equation numbers (1)–(20). */
window.WALK = window.WALK || {};

(function () {
    // upright type inside the italic formula: function names, units and equation numbers, as TeX sets them
    function up(s) { return '<span style="font-style:normal">' + s + '</span>'; }
    function tag(n) { return ' &emsp; ' + up('(' + n + ')'); }

    window.WALK.furuta = {
        intro: 'Nine steps from the lecture note to the code of this page, in the order of the note: the inertias and the energies, the motor, the equations of motion, the linear model at the top and the controllability test, the Riccati equation and the gains, the swing-up, the voltage that gives the arm its acceleration, the hand-over, and the solver with its energy books. Each step sets an equation of the note, with its number, beside the lines of this page that evaluate it, quoted character for character. Point at a coloured symbol and the same quantity lights up in the formula, the code and the table. The “Now” column is read from the page’s data store five times a second: the quantities of the motion show the stored sample on screen at this moment, everything else belongs to the whole solved run.',
        steps: [
            {
                title: 'Equations (2) and (3): the inertias and the energy',
                where: 'derive() and energy(), under the rig constants',
                math: 'T = ½(⟦J0|J<sub>0</sub>⟧ + ⟦Jp|J<sub>p</sub>⟧ ' + up('sin') + '²α) φ̇² + ⟦hc|h⟧ ' + up('cos') + ' α φ̇α̇ + ½J<sub>p</sub>α̇², &nbsp; J<sub>0</sub> = J<sub>r</sub> + m<sub>p</sub>⟦r|r⟧², &nbsp; J<sub>p</sub> = ⅓m<sub>p</sub>L², &nbsp; h = ½m<sub>p</sub>rL' + tag(2) + '<br>U = ⟦G|G⟧ ' + up('cos') + ' α, &nbsp; G = ½m<sub>p</sub>gL' + tag(3),
                note: 'derive() turns the arm length r from its slider into the constants of (2) and (3): J_r = m_a r²/3 + J_h for the arm, hub and rotor, J₀ with the rod’s mass at the tip, J_p for the rod about its hinge, the coupling h, the gravity scale G, and Δ = J₀J_p − h². energy() is T + U for the state y = (φ, α, φ̇, α̇); s and c are sin α and cos α. The energy is not needed to solve the motion; it is one side of the books of step 9.',
                code: `p.Jr = MA * p.r * p.r / 3 + JH; p.J0 = p.Jr + MP * p.r * p.r; p.Jp = MP * LP * LP / 3;
p.h = MP * p.r * LP / 2; p.G = MP * G * LP / 2; p.D = p.J0 * p.Jp - p.h * p.h;
...
return 0.5 * (p.J0 + p.Jp * s * s) * y[2] * y[2] + p.h * c * y[2] * y[3] + 0.5 * p.Jp * y[3] * y[3] + p.G * c;`,
                syms: [
                    ['r', 'r', 'p.r', 'arm length, m'],
                    ['J0', 'J<sub>0</sub>', 'p.J0', 'arm’s inertia with the rod’s mass at the tip, kg m²'],
                    ['Jp', 'J<sub>p</sub>', 'p.Jp', 'rod’s inertia about its hinge, kg m²'],
                    ['hc', 'h', 'p.h', 'coupling between arm and rod, kg m²'],
                    ['G', 'G', 'p.G', 'gravity scale of the rod, J']
                ]
            },
            {
                title: 'Equations (4) and (6): the motor',
                where: 'rhs() and the last lines of drive()',
                math: 'V<sub>m</sub> = R⟦I|I⟧ + Λ İ + kφ̇, &nbsp; τ = kI' + tag(4) + '<br>Λ → 0: &nbsp; I = (⟦V|V<sub>m</sub>⟧ − kφ̇)/R, &nbsp; ⟦tau|τ⟧ = (k/R)(V<sub>m</sub> − kφ̇)' + tag(6),
                note: 'The winding’s inductance is dropped (its time Λ/R = 0.5 ms is short against the pendulum’s 0.143 s), so the current follows the voltage at once: I = (V_m − kφ̇)/R, with y[2] = φ̇ and KM = k = 0.10 N m/A, RM = R = 4 Ω. In drive() the controller’s wish is first clipped to the amplifier’s limit ±V_max; sat records whether it had to be. accel() then uses the torque KM * I.',
                code: `function rhs(p, y, Vm) { var I = (Vm - KM * y[2]) / RM, a = accel(p, y, I); return [y[2], y[3], a[0], a[1]]; }
...
var V = Math.max(-p.Vmax, Math.min(p.Vmax, want));
return { V: V, I: (V - KM * y[2]) / RM, sat: Math.abs(want) > p.Vmax ? 1 : 0 };`,
                syms: [
                    ['V', 'V<sub>m</sub>', 'V', 'motor voltage, V; Now: the stored sample on screen'],
                    ['I', 'I', 'I', 'motor current, A'],
                    ['tau', 'τ', 'KM * I', 'motor torque, N m']
                ]
            },
            {
                title: 'Equation (7): Lagrange’s equations, solved for the accelerations',
                where: 'accel(), under derive()',
                math: 'M(α) q̈ = f(q, q̇) + (τ, 0)' + tag(7) + '<br>M = ((J<sub>0</sub> + J<sub>p</sub> ' + up('sin') + '²α, h ' + up('cos') + ' α), (h ' + up('cos') + ' α, J<sub>p</sub>))',
                note: 'a11, a12 and a22 are the entries of the mass matrix M at the present α. r1 is the arm’s row of (7): the motor’s torque KM * I, the bearing’s friction and the two speed terms; r2 is the rod’s row: the centrifugal term, gravity G sin α, which tips the rod away from the top, and the hinge’s friction. Cramer’s rule solves the 2 × 2 system in the return line for (φ̈, α̈). The coupling a12 = h cos α is the motor’s only handle on the pendulum.',
                code: `var s = Math.sin(y[1]), c = Math.cos(y[1]), w = y[2], v = y[3];
var a11 = p.J0 + p.Jp * s * s, a12 = p.h * c, a22 = p.Jp;
var r1 = KM * I - BR * w - 2 * p.Jp * s * c * w * v + p.h * s * v * v;
var r2 = p.Jp * s * c * w * w + p.G * s - BP * v;
var det = a11 * a22 - a12 * a12;
return [(a22 * r1 - a12 * r2) / det, (a11 * r2 - a12 * r1) / det];`,
                syms: [
                    ['ph', 'φ', 'y[0]', 'arm angle, rad; Now: the stored sample on screen'],
                    ['al', 'α', 'y[1]', 'pendulum angle from straight up, rad']
                ]
            },
            {
                title: 'Equations (9) and (11): the linear model at the top and the controllability test',
                where: 'linearise() and rankOf()',
                math: 'ỹ̇ = A ỹ + B V<sub>m</sub>, &nbsp; A = ∂f/∂y, B = ∂f/∂V<sub>m</sub> at (φ*, 0, 0, 0)' + tag(9) + '<br>𝒞 = [B, AB, A²B, A³B], &nbsp; ' + up('rank') + ' 𝒞 = ⟦rank|4⟧' + tag(11),
                note: 'linearise() builds A and B by central differences of the full equations of motion, nudging each of the four state numbers and the voltage by 10⁻⁶ in both directions; the result agrees with the closed form (9). rankOf() stacks B, AB, A²B, A³B as columns, scales each to unit length and counts the pivots of Gaussian elimination. The fastest growth rate of A at the top, about 9.5 per second, is how fast the pendulum falls.',
                code: `for (j = 0; j < 4; j++) { var yp = y0.slice(), ym = y0.slice(); yp[j] += e; ym[j] -= e; var fp = rhs(p, yp, 0), fm = rhs(p, ym, 0); for (i = 0; i < 4; i++) A[i][j] = (fp[i] - fm[i]) / (2 * e); }
var bp = rhs(p, y0, e), bm = rhs(p, y0, -e); for (i = 0; i < 4; i++) B[i][0] = (bp[i] - bm[i]) / (2 * e);`,
                syms: [
                    ['rank', 'rank 𝒞', 'rankOf(L.A, L.B)', 'rank of the controllability matrix'],
                    ['grow', 'λ<sub>+</sub>', 'max Re λ(A)', 'growth rate at the top without control, 1/s']
                ]
            },
            {
                title: 'Equations (16) and (17): the Riccati equation and the gains',
                where: 'lqr()',
                math: 'A<sup>T</sup>P + PA − ρ<sup>−1</sup>PBB<sup>T</sup>P + Q = 0' + tag(16) + '<br>⟦K|K⟧ = ρ<sup>−1</sup>B<sup>T</sup>P' + tag(17),
                note: 'The Riccati equation is solved through the 8 × 8 Hamiltonian matrix Hm, whose blocks are A, −BBᵀ/ρ, −Q and −Aᵀ (here R in the code is the weight ρ, not the winding’s resistance, and Qd holds the diagonal of Q: w_φ, w_α, 0.5, 2). The iteration Z ← ½(Z + Z⁻¹) converges to the matrix sign function, and P follows from its blocks by least squares. The last line is (17). The closed-loop eigenvalues, of A − BK, are all real and negative; the slowest is the decay rate in the readouts.',
                code: `Hm[i][j] = A[i][j]; Hm[i][n + j] = -B[i][0] * B[j][0] / R; Hm[n + i][j] = -(i === j ? Qd[i] : 0); Hm[n + i][n + j] = -A[j][i];
...
for (i = 0; i < 2 * n; i++) for (j = 0; j < 2 * n; j++) { Zn[i][j] = 0.5 * (Z[i][j] + Zi[i][j]); dn += Math.abs(Zn[i][j] - Z[i][j]); }
...
var P = mul(inv(mul(Lt, Lm)), mul(Lt, Rm)), K = [];
...
for (j = 0; j < n; j++) { var s = 0; for (i = 0; i < n; i++) s += B[i][0] * P[i][j]; ⟦K|K.push(s / R)⟧; }`,
                syms: [
                    ['K', 'K', 'K', 'gains on (φ − φ*, α, φ̇, α̇), V/rad and V s/rad'],
                    ['slow', 'max Re λ', 'design()', 'slowest decay once caught, 1/s']
                ]
            },
            {
                title: 'Equations (12) and (13): the swing-up pumps energy',
                where: 'penEnergy() and drive(), the swing-up branch',
                math: '⟦Ep|E<sub>p</sub>⟧ = ½J<sub>p</sub>α̇² + G ' + up('cos') + ' α' + tag(12) + '<br>u = ' + up('sat') + '<sub>a<sub>max</sub></sub>[k<sub>E</sub>(E<sub>p</sub> − G) α̇ ' + up('cos') + ' α] − k<sub>φ</sub>(φ − φ*) − k<sub>ω</sub>φ̇' + tag(13),
                note: 'E_p is the pendulum’s energy as if its hinge stood still: −G hanging at rest, +G standing at rest at the top. The first line of drive()’s swing-up branch asks for an arm acceleration uE that feeds energy in while E_p < G and out while E_p > G, clipped at AMAX = 30 rad/s². The second adds a soft spring KPHI and damper KW that keep the arm near φ*; wrap() takes the nearest angle. With uE alone, ½(E_p − G)² can only fall.',
                code: `function penEnergy(p, y) { return 0.5 * p.Jp * y[3] * y[3] + p.G * Math.cos(y[1]); }   // (12): the pendulum alone, as if its hinge stood still
...
var uE = Math.max(-AMAX, Math.min(AMAX, p.kE * (penEnergy(p, y) - p.G) * v * c));
var u = uE - KPHI * wrap(y[0] - p.phs) - KW * w;`,
                syms: [
                    ['Ep', 'E<sub>p</sub>', 'penEnergy(p, y)', 'pendulum energy, J; Now: the stored sample on screen'],
                    ['G', 'G', 'p.G', 'its value at rest at the top, J']
                ]
            },
            {
                title: 'Equation (14): the voltage that gives the arm the acceleration u',
                where: 'drive(), the swing-up branch, after (13)',
                math: '⟦tau|τ⟧ = (J<sub>0</sub> + J<sub>p</sub> ' + up('sin') + '²α − h² ' + up('cos') + '²α/J<sub>p</sub>) u + …, &nbsp; ⟦V|V<sub>m</sub>⟧ = Rτ/k + kφ̇' + tag(14),
                note: 'add is α̈ from the rod’s row of (7) with φ̈ = u. Put into the arm’s row, it gives the torque tau that makes φ̈ = u exactly: collocated partial feedback linearisation. The last line inverts the motor’s law (6). The voltage is clipped to ±V_max afterwards (step 2); while it is clipped, the arm’s acceleration is no longer u.',
                code: `var add = (-p.h * c * u + p.Jp * s * c * w * w + p.G * s - BP * v) / p.Jp;
var tau = (p.J0 + p.Jp * s * s) * u + p.h * c * add + 2 * p.Jp * s * c * w * v - p.h * s * v * v + BR * w;
want = RM * tau / KM + KM * w;`,
                syms: [
                    ['tau', 'τ', 'tau', 'torque the arm needs, N m'],
                    ['V', 'V<sub>m</sub>', 'want', 'voltage before the clip, V']
                ]
            },
            {
                title: 'Equations (18) and (19): the catch and the hand-over',
                where: 'catchVolt(), decide() and design()',
                math: 'V<sub>m</sub> = −K ỹ, &nbsp; 𝒱<sub>c</sub> = ⟦Ly|ỹ<sup>T</sup>Pỹ⟧, &nbsp; 𝒱̇<sub>c</sub> = −ỹ<sup>T</sup>(Q + ρK<sup>T</sup>K)ỹ < 0' + tag(18) + '<br>swing-up → catch when ỹ<sup>T</sup>Pỹ < ⟦cin|c<sub>in</sub>⟧ = c/2; &nbsp; catch → swing-up when ỹ<sup>T</sup>Pỹ > c<sub>out</sub> = c' + tag(19),
                note: 'catchVolt() is the LQR law: minus the gains times the error ỹ = (φ − φ*, α, φ̇, α̇), angles taken as the nearest to the goal. decide() is the supervisor of (19), called once every millisecond: it compares the Lyapunov value ỹᵀPỹ with the two levels. c is measured once per design by measureC(): 240 starts spread over the surface ỹᵀPỹ = c, the catch alone for 3 s, and twelve halvings of the interval.',
                code: `function catchVolt(p, d, y) { var e = err(p, y), V = 0; for (var j = 0; j < 4; j++) V -= d.K[j] * e[j]; return V; }
...
var L = lyap(d, err(p, y));
return caught ? L <= d.cout : L < d.cin;
...
d.c = designCache[key].c; d.cin = 0.5 * d.c; d.cout = d.c; d.ms = designCache[key].ms;`,
                syms: [
                    ['Ly', 'ỹ<sup>T</sup>Pỹ', 'L', 'the catch’s bowl; Now: the stored sample on screen'],
                    ['cin', 'c<sub>in</sub>', 'd.cin', 'hand-over level']
                ]
            },
            {
                title: 'Equation (20): RK4 and the energy books',
                where: 'stepRK4(), run() and solve()',
                math: 'E(0) + W<sub>in</sub> − H<sub>R</sub> − H<sub>b</sub> − E(t<sub>end</sub>) = ⟦bal|0⟧' + tag(20) + '<br>W<sub>in</sub> = ∫V<sub>m</sub>I dt, &nbsp; H<sub>R</sub> = ∫RI² dt, &nbsp; H<sub>b</sub> = ∫(b<sub>r</sub>φ̇² + b<sub>p</sub>α̇²) dt',
                note: 'Each RK4 stage evaluates the drive and the accelerations and carries three more rates: the electrical power V_m I, the winding’s heat R I² and the bearings’ heat. They are summed with the same RK4 weights as the state, so the books are integrated as accurately as the motion. run() lets the supervisor decide once a millisecond (per = 1 at δt = 1 ms, 2 at δt/2; in the code the step is h, and H its default). At the end solve() closes the book (20); with the defaults it is a few times 10⁻¹¹ J. The same run with δt/2 grades the stored one.',
                code: `k.push([ys[2], ys[3], a[0], a[1], dr.V * dr.I, RM * dr.I * dr.I, BR * ys[2] * ys[2] + BP * ys[3] * ys[3]]);
...
var out = []; for (i = 0; i < 4; i++) out.push(y[i] + h / 6 * (k[0][i] + 2 * k[1][i] + 2 * k[2][i] + k[3][i]));
acc.W += h / 6 * (k[0][4] + 2 * k[1][4] + 2 * k[2][4] + k[3][4]);
...
if ((step - 1) % per === 0) caught = decide(p, d, y, caught);
...
ds.set('balance', Es[0] + Win[NS - 1] - QR[NS - 1] - Qb[NS - 1] - Es[NS - 1]);`,
                syms: [
                    ['bal', 'balance', 'balance', 'the energy book at the end, J'],
                    ['err', '|y<sub>δt</sub> − y<sub>δt/2</sub>|', 'err_half', 'largest difference from the half-step run'],
                    ['h', 'δt', 'H', 'RK4 step, s'],
                    ['steps', 'steps', 'TEND / H', 'RK4 steps in one run']
                ]
            }
        ]
    };
})();
