/* From symbols to code — Fig. 12, A Pint of Stout on a Suspension (beer-slosh.html), the one-wheel cart.
   Each step pairs an equation of the lecture note with the lines of the page's script that compute it, copied character for character.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), defined in the page next to its state. */
window.WALK = window.WALK || {};

window.WALK.slosh = {
    intro: 'Ten steps from the lecture note to the moving cart, in the order the page uses them: the calm surface for a given volume (section 2), the viscosity at the chosen temperature, the frequency of each mode with its head (11), the five damping terms (14–18), the shape of the surface from the stored modes (section 5), the road and the path of the axle over it (19a), the one system of cart and stout (20), the road’s kick in the right-hand side of the Runge–Kutta step (19b), the two control laws (section 11), and the design of the LQR gains (21). The code is the page’s own; the numbers in the last column are its state now.',
    steps: [
        {
            title: 'The calm surface',
            where: 'interpGlass(): from the precomputed fills, whenever a slider moves',
            math: '⟦V|V⟧ = ∫<sub>Z<sub>floor</sub></sub><sup>⟦zs|Z<sub>s</sub>⟧</sup> A<sub>i</sub>(Z) dZ,  ⟦a|R⟧ = R<sub>i</sub>(Z<sub>s</sub>)',
            note: 'The offline script tools/fig12/build_modes3d.py solved the volume integral for 15 fills, from 300 to 576 mL, over the sculpted cavity, and stored the height Z<sub>s</sub> of the calm surface and the radius R of its round part for each, in metres. The page takes the two stored fills on either side of the chosen volume and interpolates linearly between them, with the weight w; the same weight blends every number of every mode.',
            code: `var vs = MD.vols_mL, i = 0; while (i < vs.length - 2 && vs[i + 1] < ⟦V|P.V⟧) i++;
var w = Math.max(0, Math.min(1, (P.V - vs[i]) / (vs[i + 1] - vs[i]))), A = MD.fills[i], B = MD.fills[i + 1];
⟦zs|geo.zs = A.zs + w * (B.zs - A.zs)⟧; ⟦a|geo.a = A.a + w * (B.a - A.a)⟧;`,
            syms: [['V', 'V', 'P.V', 'volume of stout, mL'], ['zs', 'Z<sub>s</sub>', 'geo.zs', 'height of the calm surface above the foot, m'], ['a', 'R', 'geo.a', 'radius of the calm surface, m']]
        },
        {
            title: 'The viscosity at your temperature',
            where: 'setup()',
            math: 'μ = μ<sub>6</sub> μ<sub>w</sub>(T)/μ<sub>w</sub>(6 °C),  ⟦nu|ν⟧ = μ/ρ,  M<sub>f</sub> = ε<sub>f</sub> ρ h<sub>f</sub>',
            note: 'μ<sub>6</sub> = 2.06 mPa·s is the measured viscosity of Guinness at 6 °C [3]. The page scales it with temperature as water’s viscosity scales, from Vogel’s equation μ<sub>w</sub> = 2.414×10⁻⁵ Pa·s × 10<sup>247.8 K/(T − 140 K)</sup> with T in kelvin: an inference, since beer is mostly water. M<sub>f</sub> is the head’s mass per area of surface, the liquid fraction ε<sub>f</sub> times the density times the head’s thickness.',
            code: `function muWater(T) { return 2.414e-5 * Math.pow(10, 247.8 / (T + 273.15 - 140)); }   // Vogel equation for water, Pa·s
...
var mu = P.mu6 * muWater(P.T) / muWater(6), ⟦nu|nu = mu / P.rho⟧, Mf = P.ef * P.rho * P.hf;`,
            syms: [['nu', 'ν', 'nu', 'kinematic viscosity, m²/s']]
        },
        {
            title: 'The frequency of each mode',
            where: 'setup(): one pass over the 14 modes',
            math: '⟦om|ω<sub>n</sub>⟧² = (g ⟦lam|λ<sub>n</sub>⟧ + σλ<sub>n</sub>³/ρ)/(1 + κ<sub>n</sub>),  κ<sub>n</sub> = M<sub>f</sub>λ<sub>n</sub>/ρ,  ⟦f1|f<sub>n</sub>⟧ = ω<sub>n</sub>/2π<span class="walk__eq">(11)</span>',
            note: 'λ<sub>n</sub> = ω²/g is the eigenvalue the three-dimensional finite-element program found for the bare mode, in 1/m. The surface tension raises ω² by the fraction σλ²/(ρg); the head, riding on the surface as an added mass, divides it by 1 + κ. The shape ψ<sub>n</sub> at the front of the rim, rimA[k], is kept for the controller’s cost.',
            code: `rimA[k] = psiAt(k, 1, 0);
muA[k] = Mf * md.lam / P.rho;
⟦om|omA[k] = Math.sqrt((g * md.lam + P.sig * Math.pow(md.lam, 3) / P.rho) / (1 + muA[k]))⟧;
⟦f1|fA[k] = omA[k] / (2 * Math.PI)⟧;`,
            syms: [['lam', 'λ<sub>11</sub>', 'md.lam', 'eigenvalue of the slowest mode along x, 1/m'], ['om', 'ω<sub>11</sub>', 'omA[k]', 'its angular frequency, rad/s'], ['f1', 'f<sub>11</sub>', 'fA[k]', 'its frequency, Hz']]
        },
        {
            title: 'Where the energy goes',
            where: 'setup(): each damping term on its own',
            math: '⟦gw|γ<sub>w</sub>⟧ = ½(νω/2)<sup>½</sup>(I<sub>w</sub>+I<sub>b</sub>)/E<sub>Φ</sub> (16),  ⟦gs|γ<sub>s</sub>⟧ = c<sub>s</sub> ½(νω/2)<sup>½</sup>I<sub>s</sub>/E<sub>Φ</sub>,  ⟦gb|γ<sub>v</sub>⟧ = 2νλ²,  γ<sub>c</sub>,  ⟦gf|γ<sub>f</sub>⟧ = c<sub>f</sub>(u<sub>f</sub>/R)(1 − e<sup>−λh<sub>f</sub></sup>) (18),  ⟦gam|γ⟧ = Σ,  ⟦zeta|ζ⟧ = γ/ω',
            note: 'md.Iw, md.Ib and md.Is are the wall, floor and surface integrals of (16), already divided by the energy integral E<sub>Φ</sub> by the offline program, in 1/m, evaluated on the real sculpted wall. sq is ½(νω/2)<sup>½</sup> in m/s. Each rate is an amplitude decay rate in 1/s; their sum is the total, and divided by ω it is the damping ratio. U_F = 0.016 m/s is the foam wall friction of Sauret and co-workers [1].',
            code: `var sq = 0.5 * Math.sqrt(nu * omA[k] / 2);
⟦gw|gw[k] = P.wall ? sq * (md.Iw + md.Ib) : 0⟧;
⟦gs|gs[k] = P.cs * sq * md.Is⟧;
⟦gb|gb[k] = 2 * nu * md.lam * md.lam⟧;
gcA[k] = P.gc;
⟦gf|gf[k] = P.kf * (U_F / geo.a) * (1 - Math.exp(-md.lam * P.hf))⟧;
⟦gam|gam[k] = gw[k] + gs[k] + gb[k] + gcA[k] + gf[k]⟧;
⟦zeta|zeta[k] = gam[k] / omA[k]⟧;`,
            syms: [['gw', 'γ<sub>w</sub>', 'gw[k]', 'wall and floor layers, 1/s'], ['gs', 'γ<sub>s</sub>', 'gs[k]', 'surface skin, 1/s'], ['gb', 'γ<sub>v</sub>', 'gb[k]', 'viscous loss in the interior of the stout, 1/s'], ['gf', 'γ<sub>f</sub>', 'gf[k]', 'head friction on the wall, 1/s'], ['gam', 'γ<sub>11</sub>', 'gam[k]', 'total, slowest mode, 1/s'], ['zeta', 'ζ<sub>11</sub>', 'zeta[k]', 'damping ratio']]
        },
        {
            title: 'The shape of the surface',
            where: 'psiAt(k, s, th), etaWall(th): the stored mode shapes',
            math: 'ψ<sub>k</sub>(s, θ) = Σ<sub>j</sub> [c<sub>j</sub>(s) cos jθ + d<sub>j</sub>(s) sin jθ],  ⟦eta|η(rim, θ)⟧ = Σ<sub>k</sub> a<sub>k</sub> ψ<sub>k</sub>(1, θ)',
            note: 'The program stores each mode’s surface shape as a few angular Fourier components at 17 radial nodes, s = r/R from 0 to 1 (section 5): one component for a body of revolution, three for the sculpted glass. The page interpolates the components linearly in s and sums them with the mode’s amplitude a<sub>k</sub>; at s = 1 that is the stout’s height at the rim, which the trace plots and the controller watches.',
            code: `function psiAt(k, s, th) {
    var md = M[k], x = s * (NSN - 1), j = Math.min(NSN - 2, Math.floor(x)), w = x - j, tot = 0;
    for (var kk in md.psi) { var cs = md.psi[kk], c = cs[0][j] + w * (cs[0][j + 1] - cs[0][j]), sn = cs[1][j] + w * (cs[1][j + 1] - cs[1][j]), K = +kk; tot += c * Math.cos(K * th) + sn * Math.sin(K * th); }
    return tot;
}
...
function etaWall(th) { var s = 0; for (var k = 0; k < NM; k++) s += aO[k] * psiAt(k, 1, th); return s; }`,
            syms: [['eta', 'η<sub>max</sub>', 'ds.get(\'eta_w\')', 'highest stout at the rim now, mm']]
        },
        {
            title: 'The road, and the axle’s path over it',
            where: 'buildRoad(): the road on a 2 mm grid, and the envelope the axle follows',
            math: '⟦za|z<sub>a</sub>⟧(X) = max<sub>|X − x′| ≤ R<sub>w</sub></sub>[⟦zr|z<sub>r</sub>⟧(x′) + (R<sub>w</sub>² − (X − x′)²)<sup>½</sup>] − R<sub>w</sub><span class="walk__eq">(19a)</span>',
            note: 'The wheel’s rim rolls on the road, so the axle follows the curve swept by the centre of a circle of radius R<sub>w</sub> rolled along the profile. On a gentle hump that is the profile itself; at a kerb the rim meets the edge before the axle is over it, and the axle climbs on a circle round the edge. The page samples the road every 2 mm (bump, kerb, cobbles and the ISO 8608 rough road, each starting at X = 1 m) and takes the maximum over the 81 grid points under the wheel. The slope of this path sets the direction of the road’s push, which is square to the path.',
            code: `for (i = 0; i < NRD; i++) ZR[i] = zProfile(i * ROAD_DX);
for (k = -m; k <= m; k++) lift.push(Math.sqrt(Math.max(0, P.Rw * P.Rw - k * ROAD_DX * k * ROAD_DX)) - P.Rw);
for (i = 0; i < NRD; i++) { var best = -1e9; for (k = -m; k <= m; k++) { var j = Math.min(NRD - 1, Math.max(0, i + k)), v = ZR[j] + lift[k + m]; if (v > best) best = v; } ZA[i] = best; }`,
            syms: [['zr', 'z<sub>r</sub>', 'road.zr', 'road surface under the axle now, mm'], ['za', 'z<sub>a</sub>', 'road.za', 'the axle’s path there, mm'], ['slope', 'z<sub>a</sub>′', 'road.slope', 'its slope now']]
        },
        {
            title: 'Cart and stout as one system',
            where: 'assemble(): the matrices of (20), term by term',
            math: 'M<sub>c</sub> q̈ + C<sub>c</sub> q̇ + K<sub>c</sub> q = F,  q = (x<sub>c</sub>, z<sub>b</sub>, z<sub>w</sub>, a<sub>n</sub>),  M<sub>a<sub>n</sub>a<sub>n</sub></sub> = (ρN<sub>n</sub>/λ<sub>n</sub>)(1 + κ<sub>n</sub>),  M<sub>a<sub>n</sub>x</sub> = ρ⟦Q|Q<sub>n</sub>⟧N<sub>n</sub><span class="walk__eq">(20)</span>',
            note: 'The second derivatives of the three energies of section 10, written in by hand. The whole cart, ⟦M|M⟧ = M<sub>s</sub> + m<sub>w</sub>, moves along the road; the body on its spring and damper, the wheel on its tyre. For each mode: its generalised mass with the head, its damping from γ<sub>n</sub>, its stiffness from ω<sub>n</sub>², and the one coupling to the cart, through Q<sub>n</sub> along the road; the same entry appears transposed, so the stout pushes back. The tray stays level, so there is no tilt term, and lifting the glass couples to no wave (∫ψ<sub>n</sub> dS = 0).',
            code: `Mm[IX][IX] = Mtot; Cm[IX][IX] = P.cx + P.cd;                   // everything moves along the road together; rolling resistance and the drive hold the speed
Mm[IZ][IZ] = Ms; Mm[IW][IW] = P.mw;
Km[IZ][IZ] += P.k; Km[IW][IW] += P.k; Km[IZ][IW] -= P.k; Km[IW][IZ] -= P.k;   // the strut: k_s (z_b − z_w)² / 2
Cm[IZ][IZ] += P.c; Cm[IW][IW] += P.c; Cm[IZ][IW] -= P.c; Cm[IW][IZ] -= P.c;   // and its damper
Km[IW][IW] += P.kt; Cm[IW][IW] += P.ct;                             // the tyre's linear part; the road's share comes in as a force
M.forEach(function (md, k) {
    var i = IA + k, mu = P.rho * md.N / md.lam, kap = muA[k];
    Mm[i][i] = mu * (1 + kap); Cm[i][i] = 2 * mu * (1 + kap) * gam[k]; Km[i][i] = mu * omA[k] * omA[k] * (1 + kap);
    Mm[i][IX] = Mm[IX][i] = P.rho * ⟦Q|md.Qx⟧ * md.N;                    // the push along the road drives the x-modes, and they push back; the tray never tilts, so no turn and no tilt terms
});`,
            syms: [['M', 'M', 'Mtot', 'the whole cart, kg'], ['Q', 'Q<sub>11</sub>', 'QxA[k]', 'coupling to an acceleration along the road, mm'], ['ml', 'm<sub>l</sub>', 'ds.get(\'m_liq\')', 'mass of the stout, kg']]
        },
        {
            title: 'The kick, in the right-hand side of the step',
            where: 'deriv(t, y, out): what the Runge–Kutta step integrates',
            math: '⟦N|N⟧ = Mg + k<sub>t</sub>(z<sub>a</sub> − z<sub>w</sub>) + c<sub>t</sub>(ż<sub>a</sub> − ż<sub>w</sub>) ≥ 0,  ⟦kick|F<sub>kick</sub>⟧ = −N z<sub>a</sub>′<span class="walk__eq">(19b)</span>;  q̈ = M<sub>c</sub>⁻¹[F − C<sub>c</sub>q̇ − K<sub>c</sub>q],  pumping −ρN<sub>n</sub>⟦az|z̈<sub>O</sub>⟧a<sub>n</sub>',
            note: 'The tyre load is the cart’s weight plus what the tyre’s spring and damper add; a tyre cannot pull, so a negative load means the wheel has left the road: the load is set to zero and the linear tyre’s pull is cancelled on the wheel. The road pushes along the normal of the axle’s path, so its horizontal part is −N times the slope: back on the way up, forward on the way down. That kick, the drive motor and your push act on x<sub>c</sub>; the strut actuator on the body and the wheel. Then the dense solve by the precomputed inverse of M<sub>c</sub>, and the pumping term of (12), taken from the previous substep and held at −0.8 g. The acceleration ⟦ax|ẍ<sub>O</sub>⟧ reaches the stout through the coupling in M<sub>c</sub> alone.',
            code: `var X = P.v * t + y[IX], za = zAxle(X), sl = slopeAxle(X), zad = (P.v + y[n + IX]) * sl;   // the axle rides its path at the cart's speed
var N = Mtot * g + P.kt * (za - y[IW]) + P.ct * (zad - y[n + IW]), Fw = 0;   // the tyre load: the weight plus the tyre's spring and damper
if (N < 0) { Fw = -N; N = 0; }                   // a tyre cannot pull: the wheel has left the road, and the linear tyre's pull is cancelled
var kick = -N * sl;                               // the road's push on the wheel is normal to the surface, from the contact point to the axle: its horizontal part
...
Fv[IX] = kick + Ct.um + (t < push.until ? push.Fx : 0);
Fv[IZ] = Ct.us - (t < push.until ? push.Fz : 0);
Fv[IW] = -Ct.us + P.kt * za + P.ct * zad + Fw;
for (i = 0; i < n; i++) { var r = Fv[i]; for (j = 0; j < n; j++) r -= Cm[i][j] * y[n + j] + Km[i][j] * y[j]; rhs[i] = r; }
var azc = Math.max(-0.8 * g, ⟦az|azO⟧);              // the vertical acceleration of the glass stiffens or softens every mode (Faraday); z̈_O lags one substep. Below −0.8 g the stout would leave the floor and the model has failed: the softening is held there, and the page says so
for (var k = 0; k < NM; k++) rhs[IA + k] -= P.rho * M[k].N * azc * y[IA + k];`,
            syms: [['N', 'N', 'road.N', 'tyre load now, N'], ['kick', 'F<sub>kick</sub>', 'road.kick', 'the road’s push along the road now, N'], ['ax', 'ẍ<sub>O</sub>', 'ds.get(\'ax\')', 'acceleration of the glass along the road, m/s²'], ['az', 'z̈<sub>O</sub>', 'azO', 'its vertical acceleration, m/s²'], ['t', 't', 'tSim', 'simulated time, s'], ['h', 'Δt', 'h', 'step']]
        },
        {
            title: 'The two control laws',
            where: 'control(): every T<sub>s</sub>, the forces held until the next look',
            math: 'skyhook: ⟦us|u<sub>s</sub>⟧ = −c<sub>sky</sub>ż<sub>b</sub>, u<sub>m</sub> = 0;  LQR: (u<sub>s</sub>, ⟦um|u<sub>m</sub>⟧) = −K x,  |u| ≤ Bℓ ⟦I|I⟧<sub>max</sub>',
            note: 'The skyhook damps the body’s absolute velocity with the strut actuator and leaves the drive alone. The LQR reads the state of section 11 from the cart’s coordinates in ctlState(): the strut deflection, the tyre deflection (the wheel’s height minus the axle’s road height), the two x-modes and the rates, and multiplies by the two rows of gains, one for the strut and one for the drive motor. Both forces are clipped to what a moving coil can give, Bℓ I<sub>max</sub>.',
            code: `var Fm = P.Bl * P.Imax, us = 0, um = 0;
if (P.law === 'skyhook') us = -P.csky * qdA[IZ];                    // the body damped against the sky; the drive stays the plain one
else if (P.law === 'lqr' && Ct.ok) { var x = ctlState(); for (var i = 0; i < Ct.n; i++) { us -= Ct.K[0][i] * x[i]; um -= Ct.K[1][i] * x[i]; } }
⟦us|Ct.us = Math.max(-Fm, Math.min(Fm, us))⟧; ⟦um|Ct.um = Math.max(-Fm, Math.min(Fm, um))⟧;`,
            syms: [['us', 'u<sub>s</sub>', 'Ct.us', 'strut actuator force now, N'], ['um', 'u<sub>m</sub>', 'Ct.um', 'drive motor force now, N'], ['I', 'I', 'ds.get(\'I_now\')', 'actuator current, the larger, A']]
        },
        {
            title: 'Designing the gains',
            where: 'designNow(): the zero-order hold and the discrete Riccati equation',
            math: 'A<sub>d</sub> = e<sup>AT<sub>s</sub></sup>, B<sub>d</sub> from the same exponential;  P ← W + A<sub>d</sub><sup>T</sup> P (A<sub>d</sub> − B<sub>d</sub>K),  K = (W<sub>u</sub> + B<sub>d</sub><sup>T</sup>PB<sub>d</sub>)⁻¹B<sub>d</sub><sup>T</sup>PA<sub>d</sub>;  ⟦tau|τ<sub>cl</sub>⟧ = −T<sub>s</sub>/ln max|z|<span class="walk__eq">(21)</span>',
            note: 'The matrices A and B of the design model are built by evaluating the linear map dyn() on each unit state in turn, with the two actuators as the two columns of B. One matrix exponential of [[A, B], [0, 0]]T<sub>s</sub> gives the held-force map. The Riccati iteration (S in the code is P of the note) starts from the weights, or from the last solution, and stops when it changes by less than 10⁻¹¹ of its size; an independent solver in SciPy gives the same gains to 2×10⁻⁹. The slowest closed-loop motion comes from the eigenvalues of A<sub>d</sub> − B<sub>d</sub>K, found as the roots of its characteristic polynomial.',
            code: `var E = expm(Mx), Ad = E.slice(0, n).map(function (r) { return r.slice(0, n); }), Bd = E.slice(0, n).map(function (r) { return [r[n], r[n + 1]]; });
...
for (it = 0; it < 6000; it++) {
    var SB = mmul(S, Bd), BSB = mmul(BdT, SB), G2 = [[BSB[0][0] + Rw[0], BSB[0][1]], [BSB[1][0], BSB[1][1] + Rw[1]]], Gi = inv(G2);
    var BSA = mmul([SB.map(function (r) { return r[0]; }), SB.map(function (r) { return r[1]; })], Ad);   // Bdᵀ S Ad, 2×n
    K = mmul(Gi, BSA);
...
⟦tau|Ct.tau = -P.Ts / Math.log(rad)⟧; ds.set('tau_cl', Ct.tau);`,
            syms: [['tau', 'τ<sub>cl</sub>', 'Ct.tau', 'slowest time constant of the closed loop, s'], ['fz', 'f<sub>z</sub>', 'ds.get(\'f_heave\')', 'heave frequency of the body, Hz'], ['fhop', 'f<sub>hop</sub>', 'ds.get(\'f_hop\')', 'hop frequency of the wheel, Hz']]
        }
    ]
};
