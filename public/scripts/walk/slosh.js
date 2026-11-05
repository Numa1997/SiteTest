/* From symbols to code — Fig. 12, A Pint of Stout, Carried (beer-slosh.html).
   Each step pairs an equation of the lecture note with the lines of the page's script that compute it, copied character for character.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), defined in the page next to its state. */
window.WALK = window.WALK || {};

window.WALK.slosh = {
    intro: 'Eight steps from the lecture note to the moving stout, in the order the page uses them: the calm surface for a given volume (section 2), the viscosity at the chosen temperature, the frequency of each mode with surface tension and the head (11), the damping terms of section 7, (16) and (18) with the skin, bulk and contact-line terms beside them, the modal equation (12), the Runge–Kutta step, the height of the stout at the wall, and the velocity in the cut (section 8). Each step sets the equation beside the lines of this page’s script that evaluate it, copied character for character; a line that is only “...” stands for page lines left out. The table gives each symbol, its name in the code, its value now, and its meaning with its unit. Hover over or tap a symbol to light it in all three places.',
    steps: [
        {
            title: 'The calm surface',
            where: 'interpTulip(): from the precomputed fills, whenever a slider moves',
            math: 'V = ∫<sub>Z<sub>floor</sub></sub><sup>⟦zs|Z<sub>s</sub>⟧</sup> π R<sub>i</sub>(Z)² dZ,  ⟦a|R⟧ = R<sub>i</sub>(Z<sub>s</sub>)',
            note: 'The offline script tools/fig12/build_modes.py solved the volume integral for 30 fills, from 300 to 590 mL, and stored the height Z<sub>s</sub> of the calm surface and its radius R for each, in metres. The page finds the two stored fills on either side of the volume V you set and interpolates linearly between them; w is the weight of the upper one.',
            code: `var vs = MD.vols_mL, i = 0; while (i < vs.length - 2 && vs[i + 1] < P.V) i++;
var w = Math.max(0, Math.min(1, (P.V - vs[i]) / (vs[i + 1] - vs[i]))), A = MD.fills[i], B = MD.fills[i + 1];
⟦zs|geo.zs = A.zs + w * (B.zs - A.zs)⟧; ⟦a|geo.a = A.a + w * (B.a - A.a)⟧;`,
            syms: [['V', 'V', 'P.V', 'volume of stout, mL'], ['zs', 'Z<sub>s</sub>', 'geo.zs', 'height of the calm surface above the foot, m'], ['a', 'R', 'geo.a', 'radius of the calm surface, m']]
        },
        {
            title: 'The viscosity at your temperature',
            where: 'setup()',
            math: 'μ = μ<sub>6</sub> μ<sub>w</sub>(T)/μ<sub>w</sub>(6 °C),  ⟦nu|ν⟧ = μ/ρ,  M<sub>f</sub> = ε<sub>f</sub> ρ h<sub>f</sub>',
            note: 'μ<sub>6</sub> = 2.06 mPa·s is the measured viscosity of Guinness at 6 °C [3]. The page scales it with temperature as water’s viscosity scales, from Vogel’s equation μ<sub>w</sub> = 2.414×10⁻⁵ · 10<sup>247.8/(T − 140)</sup> Pa·s with T in kelvin. M<sub>f</sub> is the mass of the head per square metre of surface, in kg/m².',
            code: `function muWater(T) { return 2.414e-5 * Math.pow(10, 247.8 / (T + 273.15 - 140)); }   // Vogel equation for water, Pa·s
...
var mu = P.mu6 * muWater(P.T) / muWater(6), ⟦nu|nu = mu / P.rho⟧, Mf = P.ef * P.rho * P.hf;`,
            syms: [['nu', 'ν', 'nu', 'kinematic viscosity, m²/s']]
        },
        {
            title: 'The frequency of each mode',
            where: 'setup(): one pass over the kept modes',
            math: '⟦om|ω<sub>n</sub>⟧² = (g ⟦lam|λ<sub>n</sub>⟧ + σλ<sub>n</sub>³/ρ)/(1 + κ<sub>n</sub>),  κ<sub>n</sub> = M<sub>f</sub>λ<sub>n</sub>/ρ,  ⟦f1|f<sub>n</sub>⟧ = ω<sub>n</sub>/2π<span style="font-style:normal;margin-left:1.5em">(11)</span>',
            note: 'λ<sub>n</sub> = ω²/g is the eigenvalue the finite-element program found for the bare mode, in 1/m. The surface tension raises ω² by the fraction σλ²/(ρg); the head, riding on the surface as an added mass, lowers it by the factor 1 + κ<sub>n</sub>. The values in the table are those of the slowest mode, (1,1).',
            code: `muA[k] = Mf * md.lam / P.rho;
⟦om|omA[k] = Math.sqrt((g * md.lam + P.sig * Math.pow(md.lam, 3) / P.rho) / (1 + muA[k]))⟧;
⟦f1|fA[k] = omA[k] / (2 * Math.PI)⟧;`,
            syms: [['lam', 'λ<sub>11</sub>', 'md.lam', 'eigenvalue of the slowest mode, 1/m'], ['om', 'ω<sub>11</sub>', 'omA[k]', 'its angular frequency, rad/s'], ['f1', 'f<sub>11</sub>', 'fA[k]', 'its frequency, Hz']]
        },
        {
            title: 'Where the energy goes',
            where: 'setup(): each damping term on its own',
            math: '⟦gw|γ<sub>w</sub>⟧ = ½(νω/2)<sup>½</sup>(I<sub>w</sub>+I<sub>b</sub>)/E (16),  ⟦gs|γ<sub>s</sub>⟧ = c<sub>s</sub> ½(νω/2)<sup>½</sup>I<sub>s</sub>/E,  ⟦gb|γ<sub>b</sub>⟧ = 2νλ²,<br>⟦gf|γ<sub>f</sub>⟧ = c<sub>f</sub>(u<sub>f</sub>/R)(1 − e<sup>−λh<sub>f</sub></sup>) (18),  ⟦gam|γ⟧ = γ<sub>w</sub> + γ<sub>s</sub> + γ<sub>b</sub> + γ<sub>c</sub> + γ<sub>f</sub>',
            note: 'md.Iw, md.Ib and md.Is are the wall, floor and surface integrals of (16), already divided by the energy integral E by the offline program, in 1/m. sq is ½(νω/2)<sup>½</sup> in m/s. Each rate is an amplitude decay rate in 1/s; the damping ratio is ζ = γ/ω.',
            code: `var sq = 0.5 * Math.sqrt(nu * omA[k] / 2);
⟦gw|gw[k] = P.wall ? sq * (md.Iw + md.Ib) : 0⟧;
⟦gs|gs[k] = P.cs * sq * md.Is⟧;
⟦gb|gb[k] = 2 * nu * md.lam * md.lam⟧;
gcA[k] = P.gc;
⟦gf|gf[k] = P.kf * (U_F / geo.a) * (1 - Math.exp(-md.lam * P.hf))⟧;
⟦gam|gam[k] = gw[k] + gs[k] + gb[k] + gcA[k] + gf[k]⟧;
zeta[k] = gam[k] / omA[k];`,
            syms: [['gw', 'γ<sub>w</sub>', 'gw[k]', 'wall and floor layers, 1/s'], ['gs', 'γ<sub>s</sub>', 'gs[k]', 'surface skin, 1/s'], ['gb', 'γ<sub>b</sub>', 'gb[k]', 'viscous loss in the interior of the stout, 1/s'], ['gf', 'γ<sub>f</sub>', 'gf[k]', 'head friction on the wall, 1/s'], ['gam', 'γ<sub>11</sub>', 'gam[k]', 'total amplitude decay rate of the slowest mode, 1/s'], ['zeta', 'ζ<sub>11</sub>', 'zeta[k]', 'its damping ratio']]
        },
        {
            title: 'The modal equation',
            where: 'deriv(t, y, out): the right-hand side for the Runge–Kutta step',
            math: 'ä<sub>n</sub> + 2γ<sub>n</sub>ȧ<sub>n</sub> + ω<sub>n</sub>²(1 + z̈<sub>g</sub>/g) a<sub>n</sub> = −λ<sub>n</sub>Q<sub>n</sub> ⟦ax|ẍ<sub>g</sub>⟧/(1 + κ<sub>n</sub>)<span style="font-style:normal;margin-left:1.5em">(12)</span>',
            note: 'AX and AZ are the glass’s sideways and vertical accelerations, the hand’s follower plus the shaker, in m/s². O2 is the spring constant ω<sub>n</sub>²(1 + z̈/g) per unit mass, including surface tension and the head; Fc and Fs are the pushes on the cos and sin copies of an m = 1 mode. For each mode the state holds the wall amplitude a (m) and its rate ȧ (m/s).',
            code: `var AX = ax + sx, AY = ay, AZ = az + sz;      // the glass's whole acceleration: hand plus shaker
...
var md = M[k], O2 = (lamA[k] * (g + AZ) + P.sig * Math.pow(lamA[k], 3) / P.rho) / (1 + muA[k]), G2 = 2 * gam[k];
var Fc = md.m === 1 ? -lamA[k] * QA[k] * AX / (1 + muA[k]) : 0, Fs = md.m === 1 ? -lamA[k] * QA[k] * AY / (1 + muA[k]) : 0;
...
out[vc] = -G2 * y[vc] - O2 * y[ic] + Fc;`,
            syms: [['ax', 'ẍ', 'AX', 'sideways acceleration of the glass now, m/s²'], ['az', 'z̈', 'AZ', 'vertical acceleration of the glass now, m/s²'], ['Q', 'Q<sub>11</sub>', 'QA[k]', 'coupling of the slowest mode to ẍ, m']]
        },
        {
            title: 'One Runge–Kutta step',
            where: 'step(): called once per millisecond of simulated time',
            math: 'y<sub>n+1</sub> = y<sub>n</sub> + (⟦h|h⟧/6)(k<sub>1</sub> + 2k<sub>2</sub> + 2k<sub>3</sub> + k<sub>4</sub>)',
            note: 'The state y holds the glass position and velocity and, for each of the 14 oscillators, its amplitude and rate. The four slopes k<sub>1</sub> … k<sub>4</sub> are the classical fourth-order Runge–Kutta stages. With h = 1 ms the fastest mode kept has ωh = 0.04 (section 9).',
            code: `var i, A0 = deriv(tSim, Y, k1);
for (i = 0; i < NY; i++) Yt[i] = Y[i] + 0.5 * h * k1[i]; deriv(tSim + 0.5 * h, Yt, k2);
for (i = 0; i < NY; i++) Yt[i] = Y[i] + 0.5 * h * k2[i]; deriv(tSim + 0.5 * h, Yt, k3);
for (i = 0; i < NY; i++) Yt[i] = Y[i] + h * k3[i]; deriv(tSim + h, Yt, k4);
for (i = 0; i < NY; i++) Y[i] += ⟦h|h⟧ / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);`,
            syms: [['h', 'h', 'h', 'time step, s'], ['t', 't', 'tSim', 'simulated time, s']]
        },
        {
            title: 'The stout at the wall',
            where: 'etaWall(th) and wallScan(): every frame',
            math: '⟦eta|η<sub>max</sub>⟧ = max<sub>θ</sub> Σ<sub>n</sub> (a<sub>c,n</sub> cos mθ + a<sub>s,n</sub> sin mθ), since ψ<sub>n</sub>(R) = 1',
            note: 'Every surface shape was scaled to 1 at the wall, so the height of the stout at the wall in direction θ is just the sum of the amplitudes with their angular factors. The page looks in 72 directions for the highest point; the head’s top lies h<sub>f</sub> above it, and the rim at 160 mm.',
            code: `function etaWall(th) { var s = 0; for (var k = 0; k < NK; k++) { var m = M[k].m; s += aO[k] * Math.cos(m * th) + (m ? aO[NK + k] * Math.sin(m * th) : 0); } return s; }
...
for (var q = 0; q < 72; q++) { var th = 2 * Math.PI * q / 72, e = etaWall(th); if (e > best) { best = e; bt = th; } }
var zl = geo.zs + best, zf = zl + P.hf;`,
            syms: [['eta', 'η<sub>max</sub>', 'best', 'highest stout at the wall above the calm level, m']]
        },
        {
            title: 'The velocity in the cut',
            where: 'fieldAt(i, j, th): at grid point (i, j) of the cut at angle θ',
            math: '<b>u</b> = Σ<sub>n</sub> (ȧ<sub>n</sub>/λ<sub>n</sub>) ∇(Φ<sub>n</sub> cos mθ)',
            note: 'F holds Φ, ∂Φ/∂r and ∂Φ/∂z of the mode on the 12 × 20 grid of the cut, from the finite-element solution. c and s are ȧ/λ of the cos and sin copies, so that C and S combine them for the direction of the cut. The page draws (u<sub>r</sub>, u<sub>z</sub>) as arrows and u<sub>θ</sub> as rings.',
            code: `var m = M[k].m, F = M[k].field, c = vO[k] / lamA[k], s = m ? vO[NK + k] / lamA[k] : 0;
var C = c * Math.cos(m * th) + s * Math.sin(m * th), S = -c * Math.sin(m * th) + s * Math.cos(m * th);
ur += C * F[o + 1]; uz += C * F[o + 2]; ut += j ? m * S * F[o] / r : (m === 1 ? S * F[o + 1] : 0);   // on the axis Φ/r → ∂Φ/∂r for m = 1, and → 0 for m ≥ 2`,
            syms: [['umax', '|u|<sub>max</sub>', 'umax', 'largest speed among the arrows of the cut, m/s']]
        }
    ]
};
