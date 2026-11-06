/* From symbols to code — Fig. 12, A Pint of Stout on a Suspension (beer-slosh.html).
   Each step pairs an equation of the lecture note with the lines of the page's script that compute it, copied character for character.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), defined in the page next to its state. */
window.WALK = window.WALK || {};

window.WALK.slosh = {
    intro: 'Ten steps from the lecture note to the moving cart, in the order the page uses them: the calm surface for a given volume (section 2), the viscosity at the chosen temperature, the frequency of each mode with its head (11), the five damping terms (14–18), the shape of the surface from the stored modes (section 5), the road under the wheels (section 10), the one linear system of cart and stout (19), its right-hand side for the Runge–Kutta step, the two control laws (section 11), and the design of the LQR gains (20). The code is the page’s own; the numbers in the last column are its state now.',
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
            title: 'The road under the wheels',
            where: 'zRoad(s): the profile at a distance s along the road',
            math: 'bump: z<sub>r</sub> = ½h<sub>r</sub>[1 − cos(2π s/0.5 m)],  kerb: ½h<sub>r</sub>[1 + tanh(s/0.0125 m)],  cobbles: h<sub>r</sub> sin²(π s/0.1 m),  rough: ISO 8608 class C;  ⟦zrf|z<sub>rf</sub>⟧ = z<sub>r</sub>(vt + x<sub>c</sub> + l<sub>f</sub>)',
            note: 'Every feature starts 1 m down the road, at s = 1 m, so x = s − 1 m here. The cart’s centre is at s = vt + x<sub>c</sub>; the front wheel reads the road l<sub>f</sub> ahead of it and the rear wheel l<sub>r</sub> behind. The road’s rate of rise under a wheel, which the tyre damping needs, is a centred difference over 0.1 mm.',
            code: `function zRoad(s) {                              // height of the road at distance s along it (m); the feature starts at s = 1 m
    var h = P.hr, x = s - 1.0;
    switch (P.road) {
        case 'bump': return x > 0 && x < 0.5 ? 0.5 * h * (1 - Math.cos(2 * Math.PI * x / 0.5)) : 0;
        case 'kerb': return 0.5 * h * (1 + Math.tanh(x / 0.0125));
        case 'cobbles': var L = 0.10; return x > 0 ? h * Math.pow(Math.sin(Math.PI * x / L), 2) : 0;`,
            syms: [['zrf', 'z<sub>rf</sub>', 'road.zf', 'road under the front wheel now, mm']]
        },
        {
            title: 'Cart and stout as one system',
            where: 'assemble(): the matrices of (19), term by term',
            math: 'M<sub>c</sub> q̈ + C<sub>c</sub> q̇ + K<sub>c</sub> q = F,  M<sub>a<sub>n</sub>a<sub>n</sub></sub> = (ρN<sub>n</sub>/λ<sub>n</sub>)(1 + κ<sub>n</sub>),  M<sub>a<sub>n</sub>x</sub> = ρ⟦Q|Q<sub>n</sub>⟧N<sub>n</sub>,  M<sub>a<sub>n</sub>β</sub> = ρQ<sub>n</sub>N<sub>n</sub>(h<sub>g</sub> − κ<sub>n</sub>/λ<sub>n</sub>) + ρ⟦Qry|Q<sub>rn</sub>⟧N<sub>n</sub>,  K<sub>a<sub>n</sub>β</sub> = −gρQ<sub>n</sub>N<sub>n</sub><span class="walk__eq">(19)</span>',
            note: 'The second derivatives of the three energies of section 10, written in by hand. For each mode: its generalised mass mu with the head, its damping from γ<sub>n</sub>, its stiffness from ω<sub>n</sub>²; the coupling to the cart’s motion along x through Q<sub>n</sub>, to the pitch through h<sub>g</sub> (the glass foot swings with the body) and through the Stokes–Joukowski coupling Q<sub>rn</sub>, and the tilt’s sideways gravity in K. The same entries appear transposed: the stout pushes back. An independent SymPy script takes the same second derivatives and agrees to the last digit (check_plant.py).',
            code: `M.forEach(function (md, k) {
    var i = IA + k, mu = P.rho * md.N / md.lam, kap = muA[k];
    Mm[i][i] = mu * (1 + kap); Cm[i][i] = 2 * mu * (1 + kap) * gam[k]; Km[i][i] = mu * omA[k] * omA[k] * (1 + kap);
    var cx = P.rho * ⟦Q|md.Qx⟧ * md.N, cy = P.rho * md.Qy * md.N;
    Mm[i][IX] = Mm[IX][i] = cx; Mm[i][IY] = Mm[IY][i] = cy;
    Mm[i][IP] = Mm[IP][i] = cx * (P.hg - kap / md.lam) + P.rho * ⟦Qry|md.Qry⟧ * md.N;   // x_O carries h_g β; the rotation drives the stout through χ_y and lifts the head at x′ by −βx′ (the −κ/λ)
    Km[i][IP] = Km[IP][i] = -g * cx;                               // the tilt: the stout's weight along the tilted surface
});
Mi = inv(Mm);`,
            syms: [['Q', 'Q<sub>11</sub>', 'QxA[k]', 'coupling to a sideways acceleration, mm'], ['Qry', 'Q<sub>r,11</sub>', 'QryA[k]', 'coupling to a pitch acceleration, mm²'], ['ml', 'm<sub>l</sub>', 'ds.get(\'m_liq\')', 'mass of the stout, kg']]
        },
        {
            title: 'The right-hand side of the step',
            where: 'deriv(t, y, out): what the Runge–Kutta step integrates',
            math: 'q̈ = M⁻¹[F − C q̇ − K q],  F ∋ k<sub>t</sub>z<sub>r</sub> + c<sub>t</sub>ż<sub>r</sub> (wheels),  ±u<sub>f</sub>, ±u<sub>r</sub> (actuators),  F<sub>push</sub>;  the pumping −ρN<sub>n</sub>⟦az|z̈<sub>O</sub>⟧a<sub>n</sub>',
            note: 'The forces: the road through the tyres, the two actuators pushing up on the body (and down on their wheels, with their lever arms on the pitch), and your push along the chosen axis. Then the dense solve by the precomputed inverse of M. The vertical acceleration of the glass foot stiffens or softens every mode by ρN<sub>n</sub>z̈<sub>O</sub>, the Faraday term of (12); it is taken from the previous substep, one millisecond behind, and held at −0.8g when the stout would leave the floor. The accelerations of the cart ⟦ax|ẍ<sub>O</sub>⟧ and ⟦psi|β⟧ reach the stout only through M and K: nothing is added by hand.',
            code: `Fv[IF] = P.kt * zf + P.ct * vf; Fv[IR] = P.kt * zr + P.ct * vr;
Fv[IZ] += Ct.uf + Ct.ur; Fv[IP] += -P.lf * Ct.uf + P.lr * Ct.ur; Fv[IF] -= Ct.uf; Fv[IR] -= Ct.ur;
var Fp = t < push.until ? push.F : 0; if (push.axis === 'x') Fv[IX] += Fp; else if (push.axis === 'y') Fv[IY] += Fp; else Fv[IZ] -= Fp;
for (i = 0; i < n; i++) { var r = Fv[i]; for (j = 0; j < n; j++) r -= Cm[i][j] * y[n + j] + Km[i][j] * y[j]; rhs[i] = r; }
var azc = Math.max(-0.8 * g, ⟦az|azO⟧);              // the vertical acceleration of the glass stiffens or softens every mode (Faraday); z̈_O lags one substep. Below −0.8 g the stout would leave the floor and the model has failed: the softening is held there, and the page says so
for (var k = 0; k < NM; k++) rhs[IA + k] -= P.rho * M[k].N * azc * y[IA + k];
for (i = 0; i < n; i++) { var a = 0; for (j = 0; j < n; j++) a += Mi[i][j] * rhs[j]; out[n + i] = a; }`,
            syms: [['ax', 'ẍ<sub>O</sub>', 'ds.get(\'ax\')', 'acceleration of the glass foot along x, m/s²'], ['az', 'z̈<sub>O</sub>', 'azO', 'its vertical acceleration, m/s²'], ['psi', 'β', 'qA[IP]', 'tilt of the glass, °'], ['t', 't', 'tSim', 'simulated time, s'], ['h', 'Δt', 'h', 'step']]
        },
        {
            title: 'The two control laws',
            where: 'control(): every T<sub>s</sub>, the forces held until the next look',
            math: 'skyhook: ⟦uf|u<sub>f</sub>⟧ = −c<sub>sky</sub>(ż<sub>b</sub> − l<sub>f</sub>β̇), u<sub>r</sub> = −c<sub>sky</sub>(ż<sub>b</sub> + l<sub>r</sub>β̇);  LQR: u = −K x,  |u| ≤ Bℓ ⟦I|I⟧<sub>max</sub>',
            note: 'The skyhook damps the absolute velocity of each corner of the body. The LQR reads the state of section 11 from the cart’s coordinates: strut deflections, tyre deflections (wheel height minus the road under it), the x-modes and the rates, in ctlState(), and multiplies by the gains. Both are clipped to what the moving coils can give, Bℓ I<sub>max</sub>.',
            code: `var Fm = P.Bl * P.Imax, uf = 0, ur = 0;
if (P.law === 'skyhook') { uf = -P.csky * (qdA[IZ] - P.lf * qdA[IP]); ur = -P.csky * (qdA[IZ] + P.lr * qdA[IP]); }   // each corner of the body damped against the sky
else if (P.law === 'lqr' && Ct.ok) { var x = ctlState(); for (var i = 0; i < Ct.n; i++) { uf -= Ct.K[0][i] * x[i]; ur -= Ct.K[1][i] * x[i]; } }
⟦uf|Ct.uf = Math.max(-Fm, Math.min(Fm, uf))⟧; Ct.ur = Math.max(-Fm, Math.min(Fm, ur));`,
            syms: [['uf', 'u<sub>f</sub>', 'Ct.uf', 'front actuator force now, N'], ['I', 'I', 'ds.get(\'I_now\')', 'actuator current, the larger, A']]
        },
        {
            title: 'Designing the gains',
            where: 'design(): the zero-order hold and the discrete Riccati equation',
            math: 'A<sub>d</sub> = e<sup>AT<sub>s</sub></sup>, B<sub>d</sub> from the same exponential;  S ← Q + A<sub>d</sub><sup>T</sup> S (A<sub>d</sub> − B<sub>d</sub>K),  K = (R + B<sub>d</sub><sup>T</sup>SB<sub>d</sub>)⁻¹B<sub>d</sub><sup>T</sup>SA<sub>d</sub>;  ⟦tau|τ<sub>cl</sub>⟧ = −T<sub>s</sub>/ln max|z|<span class="walk__eq">(20)</span>',
            note: 'The matrices A and B of the design model are built by evaluating the linear map dyn() on each unit state in turn. One matrix exponential of [[A, B], [0, 0]]T<sub>s</sub> gives the held-force map. The Riccati iteration starts from S = Q and stops when S changes by less than 10⁻¹¹ of its size, about a thousand iterations; an independent solver in SciPy gives the same gains to 6×10⁻¹². The slowest closed-loop motion comes from the eigenvalues of A<sub>d</sub> − B<sub>d</sub>K, found as the roots of its characteristic polynomial.',
            code: `var E = expm(Mx), Ad = E.slice(0, n).map(function (r) { return r.slice(0, n); }), Bd = E.slice(0, n).map(function (r) { return [r[n], r[n + 1]]; });
...
for (it = 0; it < 6000; it++) {
    var SB = mmul(S, Bd), BSB = mmul(BdT, SB), G2 = [[BSB[0][0] + Rw, BSB[0][1]], [BSB[1][0], BSB[1][1] + Rw]], Gi = inv(G2);
    var BSA = mmul([SB.map(function (r) { return r[0]; }), SB.map(function (r) { return r[1]; })], Ad);   // Bdᵀ S Ad, 2×n
    K = mmul(Gi, BSA);
...
⟦tau|Ct.tau = -P.Ts / Math.log(rad)⟧; ds.set('tau_cl', Ct.tau);`,
            syms: [['tau', 'τ<sub>cl</sub>', 'Ct.tau', 'slowest time constant of the closed loop, s'], ['fz', 'f<sub>z</sub>', 'ds.get(\'f_heave\')', 'heave frequency of the body, Hz'], ['fp', 'f<sub>β</sub>', 'ds.get(\'f_pitch\')', 'pitch frequency, Hz']]
        }
    ]
};
