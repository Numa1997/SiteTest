/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.turbine = {
    intro: 'Thirteen steps from the power in the wind to the blades on the screen, in the order of the lecture note: the turbine and its power coefficient, equations (1) to (5); the rotor’s equation of motion and its energy balance, (6) and (7); the two controllers, (8) to (10); the wind; the solve, the store and the playback of section 8; the picture of section 9. Pressing Solve integrates the two minutes once and stores them, and the Now column shows the stored row that is on the screen at this moment.',
    steps: [
        {
            title: 'Power and torque of the wind · (1), (2)',
            where: 'the constants at the top of the page script; tauAero()',
            math: '⟦A|A⟧ = π⟦R|R⟧² = 5027 m², &nbsp; ⟦rho|ρ⟧ = 1.225 kg/m³<br>⟦Pw|P<sub>wind</sub>⟧ = ½ ρ A ⟦v|v⟧³ &emsp;(1)<br>P<sub>aero</sub> = ⟦cp|c<sub>p</sub>⟧ · ½ ρ A v³, &nbsp; ⟦ta|τ<sub>aero</sub>⟧ = P<sub>aero</sub> / ⟦w|ω⟧ &emsp;(2)',
            note: 'Equation (1) counts the energy the air brings: each second a slab of air of length v and mass ρAv crosses the disc, and each kilogram carries ½v² of kinetic energy. The first quoted line fixes the turbine: RHO is the air density ρ = 1.225 kg/m³, R the blade length R = 40 m, and AREA the swept disc A = πR² = 5027 m²; the other constants of that line are used in later steps. tauAero(w, v) receives the rotor speed ω in rad/s and the wind speed v in m/s and returns the wind’s torque τ<sub>aero</sub> in N m. Inside it, 0.5 * RHO * AREA * v * v * v is P<sub>wind</sub> of (1) in watts; multiplied by cp(w * R / v), the share c<sub>p</sub> at the tip-speed ratio of step 2, it becomes P<sub>aero</sub>, and the division by w turns power into torque, as in (2). The test w &gt; 1e-6 returns zero torque for a rotor at rest, where the division by ω would fail; none of the page’s runs comes near it.',
            code: `var ⟦rho|RHO = 1.225⟧, ⟦R|R = 40⟧, J = 4.0e6, ⟦A|AREA = Math.PI * R * R⟧, TMAX = 1.2e6, WN = 0.6, ZC = 0.8;
...
function ⟦ta|tauAero⟧(⟦w|w⟧, ⟦v|v⟧) {
return w > 1e-6 ? ⟦Pw|0.5 * RHO * AREA * v * v * v⟧ * ⟦cp|cp(w * R / v)⟧ / ⟦w|w⟧ : 0;
}`,
            syms: [
                ['v', 'v', 'v', 'wind speed at the rotor, m/s'],
                ['w', 'ω', 'w', 'angular speed of the rotor, rad/s'],
                ['cp', 'c<sub>p</sub>', 'cp(w * R / v)', 'share of P<sub>wind</sub> the blades turn into shaft power'],
                ['ta', 'τ<sub>aero</sub>', 'tauAero(w, v)', 'torque of the wind on the rotor, N m']
            ]
        },
        {
            title: 'Tip-speed ratio and the power coefficient · (5)',
            where: 'the constants at the top of the page script; cp()',
            math: '⟦lam|λ⟧ = ωR / v<br>⟦cp|c<sub>p</sub>⟧(λ) = c₁ (c₂/⟦li|λ<sub>i</sub>⟧ − c₄) e<sup>−c₅/λ<sub>i</sub></sup> + c₆ λ, &nbsp; ⟦inv|1/λ<sub>i</sub> = 1/λ − 0.035⟧ &emsp;(5)<br>⟦C|c₁ = 0.5176, c₂ = 116, c₄ = 5, c₅ = 21, c₆ = 0.0068⟧ &nbsp; (blades at zero pitch)',
            note: 'The tip-speed ratio λ = ωR/v is the speed of the blade tips in units of the wind speed, a pure number; tauAero() passes it to cp() as w * R / v. The constants line holds Heier’s coefficients as C1, C2, C4, C5 and C6, the names of the note: this form of the fit has no c₃. Inside cp(lam), inv is 1/λ<sub>i</sub> and li is λ<sub>i</sub>, and the return line is (5) term by term; its last term is C6 * lam, c₆λ, the version that peaks at the quoted optimum. Three guards keep the fit where it means something. Below λ = 0.05 the function returns zero, so the page gives no torque at a standstill (section 6.1). If λ reaches 1/0.035 ≈ 28.6, 1/λ<sub>i</sub> would be zero or negative, and the function again returns zero. Math.max(0, …) clips the negative values the fit gives above λ = 13.4, where Figure 2 shows the curve reaching zero.',
            code: `var ⟦C|C1 = 0.5176, C2 = 116, C4 = 5, C5 = 21, C6 = 0.0068⟧;
...
function cp(⟦lam|lam⟧) {
if (lam <= 0.05) return 0;
var ⟦inv|inv = 1 / lam - 0.035⟧;
if (inv <= 0) return 0;
var ⟦li|li = 1 / inv⟧;
return Math.max(0, ⟦cp|C1 * (C2 / li - C4) * Math.exp(-C5 / li) + C6 * lam⟧);
}`,
            syms: [
                ['lam', 'λ', 'lam', 'tip-speed ratio ωR/v of the row on screen, no unit'],
                ['cp', 'c<sub>p</sub>', 'cp(lam)', 'power coefficient of that row, no unit']
            ]
        },
        {
            title: 'The best ratio, below the Betz limit · (4)',
            where: 'optimum(), run once when the page loads; drawCp(), the dashed lines',
            math: '⟦lopt|λ<sub>opt</sub>⟧ = arg max<sub>λ</sub> c<sub>p</sub>(λ), scanned from 0.5 to 14 in steps of 0.001<br>⟦cpmax|c<sub>p,max</sub>⟧ = c<sub>p</sub>(λ<sub>opt</sub>) = 0.4800 at λ<sub>opt</sub> = 8.100<br>⟦betz|c<sub>p,Betz</sub> = 4 · ⅓ · (⅔)² = 16/27 ≈ 0.593⟧ &emsp;(4)',
            note: 'optimum() walks along the curve of step 2 in steps of 0.001 from λ = 0.5 to 14 and keeps the largest value it meets: best becomes c<sub>p,max</sub> and lbest becomes λ<sub>opt</sub>, both pure numbers, stored as cp_max and lam_opt. The scan finds c<sub>p,max</sub> = 0.4800 at λ<sub>opt</sub> = 8.100, the numbers of section 4 of the note. The Betz limit (4) is not recomputed: its derivation from Bernoulli’s equation and the momentum balance, (3), lives in the note, and the code stores only its result, 16/27, as cp_betz. The quoted line of drawCp() uses the stored numbers to draw the dashed horizontal line at c<sub>p</sub> = 16/27 and the dashed vertical line at λ<sub>opt</sub> in the c<sub>p</sub> figure. The gap between the peak of the curve and the Betz line, 0.593 − 0.480, is what a real rotor of this shape gives up against the ideal disc of section 3. The last call of the optimum line computes K<sub>opt</sub>, equation (8), taken up in step 6.',
            code: `function optimum() {
var best = 0, lbest = 0;
for (var l = 0.5; l <= 14; l += 0.001) { var c = cp(l); if (c > best) { best = c; lbest = l; } }
ds.set('lam_opt', ⟦lopt|lbest⟧); ds.set('cp_max', ⟦cpmax|best⟧); ds.set('cp_betz', ⟦betz|16 / 27⟧); ds.set('K_opt', 0.5 * RHO * Math.PI * Math.pow(R, 5) * best / Math.pow(lbest, 3));
...
c.beginPath(); c.moveTo(G.L, Y(ds.get('cp_betz'))); c.lineTo(G.R, Y(ds.get('cp_betz'))); c.moveTo(X(ds.get('lam_opt')), G.top); c.lineTo(X(ds.get('lam_opt')), G.bot); c.stroke(); c.setLineDash([]);`,
            syms: [
                ['lopt', 'λ<sub>opt</sub>', 'lbest', 'tip-speed ratio of the largest c<sub>p</sub>, no unit'],
                ['cpmax', 'c<sub>p,max</sub>', 'best', 'the largest c<sub>p</sub> of the fit, no unit'],
                ['cp', 'c<sub>p</sub>', 'cpv[n]', 'c<sub>p</sub> of the row on screen, to compare with both']
            ]
        },
        {
            title: 'Newton’s second law for the rotor · (6)',
            where: 'the constants at the top of the page script; rates()',
            math: '⟦J|J⟧ ⟦dw|dω/dt⟧ = ⟦ta|τ<sub>aero</sub>⟧(⟦w|ω⟧, ⟦v|v⟧(t)) − ⟦tg|τ<sub>gen</sub>⟧ &emsp;(6)<br>J = 4.0 × 10⁶ kg m²',
            note: 'rates(t, w, I, c) is the right-hand side of the whole system: given the time t in s, the rotor speed w (ω, in rad/s), the controller’s memory I and the run’s settings c, it returns the rate of change of every integrated quantity. Its first line evaluates the two torques of (6): v is the wind at this instant from wind(t, c), step 9, which depends on time alone; g is the generator torque from tauGen(w, I, c), steps 6 and 7, which depends on the measured speed; a is the wind’s torque from step 1. The two calls show the note’s two time dependences: the wind is a drive, the generator torque is feedback. The first entry of the returned array, (a - g) / J, is (6) divided by J = 4.0 × 10⁶ kg m², the angular acceleration dω/dt in rad/s². The second entry, dI, belongs to the controller (step 7); the other five are the integrands of the energies, the air travel and the rotor angle (steps 5 and 12). The two lines left out compute dI.',
            code: `var RHO = 1.225, R = 40, ⟦J|J = 4.0e6⟧, AREA = Math.PI * R * R, TMAX = 1.2e6, WN = 0.6, ZC = 0.8;
...
function rates(t, ⟦w|w⟧, I, c) {
var ⟦v|v = wind(t, c)⟧, ⟦tg|g = tauGen(w, I, c)⟧, ⟦ta|a = tauAero(w, v)⟧, e = w - c.wref;
...
return [⟦dw|(a - g) / J⟧, dI, g * w, a * w, 0.5 * RHO * AREA * v * v * v, v, w];
}`,
            syms: [
                ['w', 'ω', 'w', 'angular speed of the rotor, rad/s'],
                ['v', 'v', 'v', 'wind speed, m/s'],
                ['ta', 'τ<sub>aero</sub>', 'a', 'torque of the wind, drives, N m'],
                ['tg', 'τ<sub>gen</sub>', 'g', 'torque of the generator, brakes, N m']
            ]
        },
        {
            title: 'The energy balance · (7)',
            where: 'rates(), entries 3 and 4; solve(), the loop and after it',
            math: 'τ<sub>aero</sub>ω = τ<sub>gen</sub>ω + d(½Jω²)/dt &nbsp; ⟹ &nbsp; ⟦Ea|E<sub>aero</sub>⟧ = ⟦Eg|E<sub>gen</sub>⟧ + Δ(½Jω²) &emsp;(7)<br>E<sub>gen</sub> = ∫<sub>0</sub><sup>t</sup> τ<sub>gen</sub>ω dt′, &nbsp; E<sub>aero</sub> = ∫<sub>0</sub><sup>t</sup> τ<sub>aero</sub>ω dt′, &nbsp; Δ(½Jω²) = ⟦KE|½Jω(T)²⟧ − ⟦KE0|½Jω(0)²⟧<br>⟦bal|balance⟧ = |E<sub>aero</sub> − E<sub>gen</sub> − Δ(½Jω²)| / E<sub>aero</sub>',
            note: 'Multiplying (6) by ω turns torques into powers: the wind’s power τ<sub>aero</sub>ω either goes into the generator or changes the rotor’s kinetic energy ½Jω². The third and fourth entries of rates() are these two powers in W, g * w = τ<sub>gen</sub>ω and a * w = τ<sub>aero</sub>ω. The array y holds the five carried integrals, all starting at zero: y[0] = E<sub>gen</sub> and y[1] = E<sub>aero</sub> in J, y[2] = E<sub>wind</sub>, the integral of the fifth entry ½ρAv³ of (1), y[3] = s<sub>air</sub> in m and y[4] = θ in rad. The loop over j adds to each one the RK4 average of its rate, with the same weights as ω (step 10). After the run, KE0 and KE are ½Jω² at t = 0 and at T = 120 s. The next lines store the captured share 100 E<sub>aero</sub>/E<sub>wind</sub> in per cent, the three energies, the mean generator power E<sub>gen</sub>/T in W, and the relative error of (7). With the default settings that error is about 10⁻¹²: whatever the integration loses or gains is a millionth of a millionth of the energy the wind delivered, so the balance tests the whole computation.',
            code: `return [(a - g) / J, dI, ⟦Eg|g * w⟧, ⟦Ea|a * w⟧, 0.5 * RHO * AREA * v * v * v, v, w];
...
var y = [0, 0, 0, 0, 0], n = 0, ⟦KE0|KE0 = 0.5 * J * w * w⟧, step, j;
...
for (j = 0; j < 5; j++) y[j] += H / 6 * (k1[j + 2] + 2 * k2[j + 2] + 2 * k3[j + 2] + k4[j + 2]);
...
var ⟦KE|KE = 0.5 * J * om[NS - 1] * om[NS - 1]⟧;
...
ds.set('captured_pct', 100 * y[1] / y[2]);
ds.set('Ea', ⟦Ea|y[1]⟧); ds.set('Ew', y[2]); ds.set('Eg_end', ⟦Eg|y[0]⟧); ds.set('P_mean', y[0] / TEND);
ds.set('balance', ⟦bal|Math.abs(y[1] - y[0] - (KE - KE0)) / y[1]⟧);`,
            syms: [
                ['Eg', 'E<sub>gen</sub>', 'y[0], stored as Eg[n]', 'energy into the generator up to the row on screen, J (shown in kWh)'],
                ['bal', 'balance', 'balance', 'relative error of (7) over the whole run, no unit'],
                ['ta', 'τ<sub>aero</sub>', 'a', 'torque of the wind, N m'],
                ['tg', 'τ<sub>gen</sub>', 'g', 'torque of the generator, N m'],
                ['w', 'ω', 'w', 'angular speed of the rotor, rad/s']
            ]
        },
        {
            title: 'Follow the wind: the optimal-torque law · (8)',
            where: 'optimum(), the K_opt call; tauGen(), first line',
            math: 'τ<sub>aero</sub>|<sub>λ<sub>opt</sub></sub> = (½ρπR²c<sub>p,max</sub> / ω) (ωR / λ<sub>opt</sub>)³ = ⟦Kopt|K<sub>opt</sub>⟧ ⟦w|ω⟧², &nbsp; K<sub>opt</sub> = ρπR⁵c<sub>p,max</sub> / (2λ<sub>opt</sub>³) &emsp;(8)<br>⟦tg|τ<sub>gen</sub>⟧ = min(⟦TMAX|τ<sub>max</sub>⟧, K<sub>opt</sub>ω²), &nbsp; τ<sub>max</sub> = 1.2 MN m',
            note: 'If the rotor runs at λ<sub>opt</sub>, the wind speed follows from the rotor speed, v = ωR/λ<sub>opt</sub>, and the wind’s torque (2) becomes K<sub>opt</sub>ω², a function of the one quantity the controller can measure. In the optimum line, the K_opt expression is (8) with c<sub>p,max</sub> = best and λ<sub>opt</sub> = lbest from step 3: 0.5 * RHO * Math.PI * Math.pow(R, 5) is ½ρπR⁵, and the result, 1.78 × 10⁵ N m s², is stored as K_opt. The first line of tauGen(w, I, c) is the follow-the-wind controller: when the run’s setting c.ctrl is \'opt\', the generator brakes with K<sub>opt</sub>ω² in N m, never more than TMAX = 1.2 MN m, the generator’s limit. That limit would be reached only at ω = 2.60 rad/s, 24.8 turns per minute, which none of the runs of section 7 reaches. In steady wind a speed error dies away with the relaxation time J/(3K<sub>opt</sub>ω<sub>*</sub>) ≈ 4.62 s of section 6.1, and the rotor settles at λ<sub>opt</sub>; when the wind changes, it needs those few seconds to catch up, so λ wanders around 8.1 instead of staying on it.',
            code: `var RHO = 1.225, R = 40, J = 4.0e6, AREA = Math.PI * R * R, ⟦TMAX|TMAX = 1.2e6⟧, WN = 0.6, ZC = 0.8;
...
ds.set('lam_opt', lbest); ds.set('cp_max', best); ds.set('cp_betz', 16 / 27); ds.set('K_opt', ⟦Kopt|0.5 * RHO * Math.PI * Math.pow(R, 5) * best / Math.pow(lbest, 3)⟧);
...
function ⟦tg|tauGen⟧(⟦w|w⟧, I, c) {
if (c.ctrl === 'opt') return Math.min(⟦TMAX|TMAX⟧, ⟦Kopt|ds.get('K_opt')⟧ * w * w);`,
            syms: [
                ['Kopt', 'K<sub>opt</sub>', "ds.get('K_opt')", 'gain of the optimal-torque law, N m s²'],
                ['tg', 'τ<sub>gen</sub>', 'tauGen(w, I, c)', 'generator torque of the row on screen, N m'],
                ['w', 'ω', 'w', 'angular speed of the rotor, rad/s'],
                ['lam', 'λ', 'lam[n]', 'tip-speed ratio now; stays at λ<sub>opt</sub> only in steady wind'],
                ['lopt', 'λ<sub>opt</sub>', "ds.get('lam_opt')", 'the target of this law, no unit']
            ]
        },
        {
            title: 'Hold speed: the PI law · (9)',
            where: 'solve(), before the loop; tauGen(), second line; rates()',
            math: '⟦tg|τ<sub>gen</sub>⟧ = ⟦tau0|τ<sub>0</sub>⟧ + ⟦Kp|K<sub>p</sub>⟧(⟦w|ω⟧ − ⟦wref|ω<sub>ref</sub>⟧) + ⟦Ki|K<sub>i</sub>⟧ ⟦I|∫<sub>0</sub><sup>t</sup>(ω − ω<sub>ref</sub>) dt′⟧ &emsp;(9)<br>τ<sub>0</sub> = τ<sub>aero</sub>(ω<sub>ref</sub>, v(0)), &nbsp; ω<sub>ref</sub> = 2π n<sub>ref</sub> / (60 s)<br>⟦dI|dI/dt⟧ = ω − ω<sub>ref</sub>, held at 0 while τ<sub>gen</sub> sits at 0 or at τ<sub>max</sub>',
            note: 'The hold-speed controller compares the measured speed with a target. In solve(), the target comes from the rpm slider: wref is n<sub>ref</sub> turns per minute times 2π/60, ω<sub>ref</sub> in rad/s, 1.5708 rad/s for 15 rpm. The next line sets tau0, τ<sub>0</sub> in N m, to the wind’s torque at the target speed and the wind at t = 0, so the run starts in balance with nothing yet to remember. The return line of tauGen() is (9): I, in rad, is the controller’s memory ∫(ω − ω<sub>ref</sub>) dt′, and the torque is clipped to the range from 0, no braking, to TMAX = 1.2 MN m. In rates(), raw is the same torque before clipping and e = w - c.wref the speed error in rad/s. dI, the rate of change of I, equals e, except when the torque already sits at a limit and the error would push it further, or when the controller is \'opt\', which has no memory; then dI is zero and I stops growing. That is the anti-windup of section 6.2. The gains K<sub>p</sub> and K<sub>i</sub> are chosen in step 8.',
            code: `var c = { ctrl: ctrl, prof: prof, v0: v0.value, dv: dv.value, ⟦wref|wref: rpm.value * 2 * Math.PI / 60⟧ };
⟦tau0|c.tau0 = tauAero(c.wref, wind(0, c))⟧;
...
return Math.min(TMAX, Math.max(0, ⟦tg|c.tau0 + c.Kp * (w - c.wref) + c.Ki * I⟧));
...
var raw = c.tau0 + c.Kp * e + c.Ki * I;
var ⟦dI|dI = c.ctrl === 'opt' || (raw <= 0 && e < 0) || (raw >= TMAX && e > 0) ? 0 : e⟧;`,
            syms: [
                ['tg', 'τ<sub>gen</sub>', 'tauGen(w, I, c)', 'generator torque of the row on screen, N m'],
                ['wref', 'ω<sub>ref</sub>', 'c.wref', 'target rotor speed, rad/s'],
                ['w', 'ω', 'w', 'angular speed of the rotor, rad/s'],
                ['Kp', 'K<sub>p</sub>', 'c.Kp', 'proportional gain, N m s'],
                ['Ki', 'K<sub>i</sub>', 'c.Ki', 'integral gain, N m (per radian of accumulated error)']
            ]
        },
        {
            title: 'Choosing the gains · (10)',
            where: 'the constants at the top of the page script; solve(), before the loop',
            math: 'J δω̈ + (⟦Kp|K<sub>p</sub>⟧ − ⟦dtd|∂τ<sub>aero</sub>/∂ω⟧) δω̇ + ⟦Ki|K<sub>i</sub>⟧ δω = 0 &nbsp;⟺&nbsp; δω̈ + 2⟦ZC|ζ<sub>c</sub>⟧⟦WN|ω<sub>n</sub>⟧ δω̇ + ω<sub>n</sub>² δω = 0 &emsp;(10)<br>K<sub>i</sub> = Jω<sub>n</sub>², &nbsp; K<sub>p</sub> = 2ζ<sub>c</sub>ω<sub>n</sub>J + ∂τ<sub>aero</sub>/∂ω, &nbsp; ω<sub>n</sub> = 0.6 rad/s, &nbsp; ζ<sub>c</sub> = 0.8<br>∂τ<sub>aero</sub>/∂ω ≈ [τ<sub>aero</sub>(⟦wref|ω<sub>ref</sub>⟧ + δ, v<sub>0</sub>) − τ<sub>aero</sub>(ω<sub>ref</sub> − δ, v<sub>0</sub>)] / 2δ, &nbsp; δ = 10⁻⁴ rad/s',
            note: 'Near the target, a small speed error δω = ω − ω<sub>ref</sub> obeys (10), a damped oscillator like the one of Fig. 9; matching its two coefficients to a natural frequency ω<sub>n</sub> and a damping ratio ζ<sub>c</sub> gives the two gains. WN and ZC in the constants line are ω<sub>n</sub> = 0.6 rad/s and ζ<sub>c</sub> = 0.8. The first quoted line of solve() measures the slope ∂τ<sub>aero</sub>/∂ω as a central difference: the wind’s torque at the target speed plus and minus 10⁻⁴ rad/s, at the mean wind v<sub>0</sub>, divided by 2 × 10⁻⁴ rad/s; dtd is in N m s. The second line is the pair of gain formulas, c.Kp in N m s and c.Ki in N m. At 15 turns per minute in an 8 m/s wind, dtd = −2.48 × 10⁵ N m s, a torque that falls slightly with speed and so damps the rotor by itself; then K<sub>p</sub> = 3.84 × 10⁶ − 0.25 × 10⁶ = 3.59 × 10⁶ N m s and K<sub>i</sub> = 1.44 × 10⁶ N m. Because ζ<sub>c</sub> is a little below 1, an error swings once past zero before it dies, by a few per cent: after the step of the Step wind the rotor runs 0.39 rpm above the target, then dips 0.01 rpm below it. The gains are tuned for the linearised rotor in steady wind; torque limits and large changes of the wind take it outside that approximation.',
            code: `var RHO = 1.225, R = 40, J = 4.0e6, AREA = Math.PI * R * R, TMAX = 1.2e6, ⟦WN|WN = 0.6⟧, ⟦ZC|ZC = 0.8⟧;
...
var ⟦dtd|dtd = (tauAero(c.wref + 1e-4, c.v0) - tauAero(c.wref - 1e-4, c.v0)) / 2e-4⟧;
⟦Kp|c.Kp = 2 * ZC * WN * J + dtd⟧; ⟦Ki|c.Ki = J * WN * WN⟧;`,
            syms: [
                ['dtd', '∂τ<sub>aero</sub>/∂ω', 'dtd', 'slope of the wind’s torque at ω<sub>ref</sub> and v<sub>0</sub>, N m s'],
                ['Kp', 'K<sub>p</sub>', 'c.Kp', 'proportional gain, N m s'],
                ['Ki', 'K<sub>i</sub>', 'c.Ki', 'integral gain, N m'],
                ['wref', 'ω<sub>ref</sub>', 'c.wref', 'target rotor speed, rad/s']
            ]
        },
        {
            title: 'The wind, a known function of time',
            where: 'the turbulence table built once; wind()',
            math: 'turbulent: ⟦v|v⟧(t) = max(0.5 m/s, v<sub>0</sub> + Δv · Σ<sub>k=0</sub><sup>15</sup> ⟦a|a<sub>k</sub>⟧ sin(2π⟦f|f<sub>k</sub>⟧t + φ<sub>k</sub>) / ⟦N|N⟧)<br>f<sub>k</sub> = 0.005 Hz · 100<sup>k/15</sup>, &nbsp; a<sub>k</sub> = f<sub>k</sub><sup>−1/3</sup>, &nbsp; N = (Σ<sub>k</sub> a<sub>k</sub>²/2)<sup>1/2</sup><br>step: v = v<sub>0</sub> + Δv · min(1, max(0, (t − 30 s)/2 s))<br>gust: v = v<sub>0</sub> − 0.37 Δv sin(3πs/T)(1 − cos(2πs/T)), &nbsp; s = t − 30 s, 0 ≤ s ≤ T = 10.5 s<br>steady: v = v<sub>0</sub>',
            note: 'The wind is the drive of section 7: a function of time alone, fixed before the run, that the rotor cannot change. wind(t, w) takes the time t in s and the run’s settings, here called w (the same object as c elsewhere, not the rotor speed): w.prof picks the profile, w.v0 is the mean wind v<sub>0</sub> and w.dv the slider Δv, both in m/s. The turbulent wind of Figure 4 is a sum of sixteen sine waves. The loop at the top builds their frequencies TF, f<sub>k</sub> in Hz, spaced evenly on a logarithmic scale from 0.005 Hz to 0.5 Hz, and their amplitudes TA, falling as f<sup>−1/3</sup>; the phases PHASES are fixed numbers, so every solve sees the same two minutes of weather. Each sine has mean square a<sub>k</sub>²/2, so dividing the sum by TNORM = N gives it a standard deviation of 1 over a long time, and Δv becomes the standard deviation σ. Over the 120 s of the run it comes out at 1.30 m/s for σ = 1.5 m/s, because the slowest wave, with a period of 200 s, does not complete a cycle. max(0.5, …) keeps the wind above 0.5 m/s, so that λ = ωR/v stays finite. The step rises linearly by Δv between t = 30 s and 32 s. The gust has the IEC shape of the reading list: from t = 30 s it dips by 0.27 Δv, rises to 0.74 Δv above v<sub>0</sub> at 35.25 s, dips again and is back at v<sub>0</sub> after 10.5 s.',
            code: `for (var q = 0; q < 16; q++) { ⟦f|TF.push(0.005 * Math.pow(100, q / 15))⟧; ⟦a|TA.push(Math.pow(TF[q], -1 / 3))⟧; }
var ⟦N|TNORM = Math.sqrt(TA.reduce(function (s, a) { return s + a * a / 2; }, 0))⟧;
function wind(t, w) {
if (w.prof === 'gust') {
var s = t - 30;
return s >= 0 && s <= 10.5 ? w.v0 - 0.37 * w.dv * Math.sin(3 * Math.PI * s / 10.5) * (1 - Math.cos(2 * Math.PI * s / 10.5)) : w.v0;
}
if (w.prof === 'step') return w.v0 + w.dv * Math.min(1, Math.max(0, (t - 30) / 2));
if (w.prof === 'turb') {
var u = 0;
for (var k = 0; k < 16; k++) u += TA[k] * Math.sin(2 * Math.PI * TF[k] * t + PHASES[k]);
return ⟦v|Math.max(0.5, w.v0 + w.dv * u / TNORM)⟧;
}
return w.v0;
}`,
            syms: [
                ['v', 'v', 'wind(t, c), stored as vw[n]', 'wind speed of the row on screen, m/s'],
                ['t', 't', 't', 'time, s; shown is the playback time now']
            ]
        },
        {
            title: 'The start and one RK4 step',
            where: 'the constants at the top of the page script; solve(), the loop',
            math: 'state ⟦s|<b>s</b>⟧ = (⟦w|ω⟧, ⟦I|I⟧); &nbsp; <b>s</b>(0) = (λ<sub>opt</sub>v(0)/R, 0) when following the wind, (⟦wref|ω<sub>ref</sub>⟧, 0) when holding speed<br>⟦k1|<b>k</b>₁⟧ = <b>f</b>(t, <b>s</b>), &nbsp; ⟦k2|<b>k</b>₂⟧ = <b>f</b>(t + h/2, <b>s</b> + h/2 · <b>k</b>₁), &nbsp; ⟦k3|<b>k</b>₃⟧ = <b>f</b>(t + h/2, <b>s</b> + h/2 · <b>k</b>₂), &nbsp; ⟦k4|<b>k</b>₄⟧ = <b>f</b>(t + h, <b>s</b> + h <b>k</b>₃)<br><b>s</b>(t + h) = <b>s</b>(t) + h/6 · (<b>k</b>₁ + 2<b>k</b>₂ + 2<b>k</b>₃ + <b>k</b>₄), &nbsp; ⟦H|h = 10 ms⟧, 12 000 steps to 120 s',
            note: 'This is the numerical method of section 8. The state that RK4 advances is s = (ω, I): w in rad/s and the controller’s memory I in rad; f is rates() of step 4. H is the step h = 0.01 s and TEND = 120 s the length of the run, so the loop takes TEND / H = 12 000 steps. The start line sets the initial condition in balance: when following the wind, ω(0) = λ<sub>opt</sub>v(0)/R, the speed at the best tip-speed ratio; when holding speed, ω(0) = ω<sub>ref</sub>, where τ<sub>0</sub> already balances the wind; in both cases I(0) = 0. Each pass of the loop first stores the state when a row is due (step 11) and stops after the last row. Then k1 to k4 are four calls of rates(): at the start of the step, twice at its midpoint with the state moved half a step along the previous slope, and at its end. Index [0] of each is dω/dt and index [1] is dI/dt, and the weighted mean (k₁ + 2k₂ + 2k₃ + k₄)/6 moves ω and I one step on. The five carried quantities y do not enter rates(), so adding them up with the same weights leaves the solution unchanged; t is recomputed from the step count instead of being summed, so no rounding piles up in the time. RK4’s error shrinks like h⁴: solving the defaults with h = 5 ms changes the stored rotor speed by at most 2 × 10⁻¹¹ rpm, and with h = 20 ms by 16 times as much.',
            code: `var ⟦H|H = 0.01⟧, TEND = 120, EVERY = 2, NS = TEND / H / EVERY + 1, NL = 271;
...
var t = 0, ⟦w|w = c.ctrl === 'opt' ? ds.get('lam_opt') * wind(0, c) / R : c.wref⟧, ⟦I|I = 0⟧;
...
for (step = 0; step <= TEND / H; step++) {
...
if (step === TEND / H) break;
// RK4 on (ω, I) with the energies, the air travel and the rotor angle carried along
var ⟦k1|k1 = rates(t, w, I, c)⟧;
var ⟦k2|k2 = rates(t + H / 2, w + H / 2 * k1[0], I + H / 2 * k1[1], c)⟧;
var ⟦k3|k3 = rates(t + H / 2, w + H / 2 * k2[0], I + H / 2 * k2[1], c)⟧;
var ⟦k4|k4 = rates(t + H, w + H * k3[0], I + H * k3[1], c)⟧;
⟦w|w += H / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])⟧;
⟦I|I += H / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])⟧;
for (j = 0; j < 5; j++) y[j] += H / 6 * (k1[j + 2] + 2 * k2[j + 2] + 2 * k3[j + 2] + k4[j + 2]);
t = (step + 1) * H;
}`,
            syms: [
                ['w', 'ω', 'w', 'angular speed of the rotor, rad/s'],
                ['wref', 'ω<sub>ref</sub>', 'c.wref', 'start value when holding speed, rad/s'],
                ['lopt', 'λ<sub>opt</sub>', "ds.get('lam_opt')", 'sets the start value when following the wind, no unit']
            ]
        },
        {
            title: 'Store every second state',
            where: 'solve(), top of the loop',
            math: 'row ⟦n|n⟧ = step / 2 = 0 … 6000, &nbsp; ⟦t|t<sub>n</sub>⟧ = n · 2h<br>⟦lam|λ<sub>n</sub>⟧ = ω<sub>n</sub>R / v<sub>n</sub>, &nbsp; ⟦cp|c<sub>p</sub>(λ<sub>n</sub>)⟧, &nbsp; ⟦ta|τ<sub>aero</sub>(ω<sub>n</sub>, v<sub>n</sub>)⟧, &nbsp; ⟦tg|τ<sub>gen</sub>(ω<sub>n</sub>, I<sub>n</sub>)⟧<br>⟦Pg|P<sub>gen</sub>⟧ = τ<sub>gen</sub>ω, &nbsp; P<sub>aero</sub> = τ<sub>aero</sub>ω, &nbsp; n<sub>rot</sub> = 60 s · ω / 2π, &nbsp; ⟦th|θ<sub>n</sub>⟧, ⟦Eg|E<sub>gen,n</sub>⟧',
            note: 'Every second step, when step % EVERY is 0, the solver writes one row into the dataset: 6 001 rows from t = 0 to 120 s, one every 2h = 20 ms. Each array is a column of the store: ts holds t<sub>n</sub> in s, vw the wind in m/s, om the rotor speed ω in rad/s and rp the same in turns per minute, th the rotor angle θ = y[4] in rad, counted on from zero and not wrapped, lam the tip-speed ratio and cpv the power coefficient. The second line evaluates the two torques with the same functions the integrator uses, at the stored state, and from them the two powers in W: Pg = τ<sub>gen</sub>ω is the generator power of section 5, the black curve of the bottom chart, and Pa = τ<sub>aero</sub>ω the rose curve behind it. Eg and sw are the carried integrals E<sub>gen</sub> in J and s<sub>air</sub> in m, Ic the controller’s memory I in rad and vt the tip speed ωR in m/s. Everything the picture shows is in these rows; playback only reads them.',
            code: `for (step = 0; step <= TEND / H; step++) {
if (step % EVERY === 0) {
var v = wind(t, c);
⟦t|ts[n] = t⟧; vw[n] = v; om[n] = w; rp[n] = w * 60 / (2 * Math.PI); ⟦th|th[n] = y[4]⟧; ⟦lam|lam[n] = w * R / v⟧; ⟦cp|cpv[n] = cp(lam[n])⟧;
⟦ta|ta[n] = tauAero(w, v)⟧; ⟦tg|tg[n] = tauGen(w, I, c)⟧; ⟦Pg|Pg[n] = tg[n] * w⟧; Pa[n] = ta[n] * w; ⟦Eg|Eg[n] = y[0]⟧; sw[n] = y[3]; Ic[n] = I; vt[n] = w * R;
⟦n|n++⟧;
}`,
            syms: [
                ['n', 'n', 'n', 'index of the row on screen now'],
                ['t', 't<sub>n</sub>', 'ts[n]', 'time of the row, s; shown is the playback time, within 10 ms of it'],
                ['lam', 'λ<sub>n</sub>', 'lam[n]', 'tip-speed ratio, no unit'],
                ['cp', 'c<sub>p</sub>', 'cpv[n]', 'power coefficient, no unit'],
                ['ta', 'τ<sub>aero</sub>', 'ta[n]', 'torque of the wind, N m'],
                ['tg', 'τ<sub>gen</sub>', 'tg[n]', 'torque of the generator, N m'],
                ['Pg', 'P<sub>gen</sub>', 'Pg[n]', 'power into the generator, W'],
                ['th', 'θ<sub>n</sub>', 'th[n]', 'rotor angle, rad, not wrapped to one turn'],
                ['Eg', 'E<sub>gen</sub>', 'Eg[n]', 'energy into the generator so far, J (shown in kWh)']
            ]
        },
        {
            title: 'Play: the rotor draws a stored row',
            where: 'the clock; frame(); drawScene()',
            math: 't<sub>play</sub> ← t<sub>play</sub> + speed · Δt, &nbsp; ⟦n|n⟧ = round(⟦t|t<sub>play</sub>⟧ / 2h), kept in 0 … 6000<br>blade b = 0, 1, 2 at the angle ⟦th|θ<sub>n</sub>⟧ + 2πb/3, &nbsp; air dashes shifted by −5 px/m · ⟦sw|s<sub>air,n</sub>⟧',
            note: 'Nothing is integrated while you watch. The clock adds the real time between frames, dt in s and never more than 0.05 s, times the speed slider to the playback time playT. frame() turns playT into the row index i, the stored row nearest in time, and keeps it between 0 and NS − 1 = 6000; i_now and t_play go into the store, and Sim.live() reads this very row for the Now column. drawScene() then reads that row: th is the stored angle θ<sub>n</sub> in rad and v the wind in m/s, while w and r here are the canvas width and the blade length in px, not the rotor speed. The dashes of the grey air streaks are shifted by the stored air travel s<sub>air</sub> times 5 px per metre (px_per_m_air), so they move exactly as far as the stored wind says. The three blades are drawn 2π/3 apart from θ, so they turn exactly as fast as the solution; blade 0, drawn last, is the burgundy one, so the turning can be followed. Section 9 names where the drawing differs from the model: the disc is foreshortened to 50 % across, and the air passes the rotor without slowing down.',
            code: `playT += speed.value * dt;
...
var ⟦n|i = Math.min(NS - 1, Math.max(0, Math.round(playT / (EVERY * H))))⟧;
iNow = i;
ds.set('i_now', i); ds.set('t_play', ⟦t|playT⟧);
...
var w = g.w, r = g.r, ⟦th|th = ds.get('th')[i]⟧, v = ds.get('vw')[i], k;
// the air: dashes that travel with the stored distance the air has moved, ∫ v dt
var off = -⟦sw|ds.get('sw')[i]⟧ * ds.get('px_per_m_air');
...
bladePath(c, g, ⟦th|th⟧ + b * 2 * Math.PI / 3);`,
            syms: [
                ['n', 'n', 'i', 'index of the row on screen'],
                ['t', 't<sub>play</sub>', 'playT', 'playback time in the stored run, s'],
                ['th', 'θ<sub>n</sub>', 'th', 'stored rotor angle that the blades are drawn at, rad'],
                ['v', 'v', 'v', 'stored wind speed, written at the top left, m/s']
            ]
        },
        {
            title: 'The charts and the c<sub>p</sub> figure',
            where: 'drawStrip(), the power chart; drawCp(), the operating point',
            math: 'operating point (⟦lam|λ<sub>n</sub>⟧, ⟦cp|c<sub>p</sub>(λ<sub>n</sub>)⟧) on the curve c<sub>p</sub>(λ) of (5); trail: rows n − 150 … n, every third, the last 3 s<br>bottom chart: ⟦Pg|P<sub>gen</sub>⟧ = τ<sub>gen</sub>ω in black, ⟦Pa|P<sub>aero</sub> = τ<sub>aero</sub>ω⟧ in rose; their difference is d(½Jω²)/dt, as in (7)',
            note: 'Below the rotor, three charts draw stored columns over the whole run: the wind vw, the rotor speed rpm with the target dashed, and the generator power Pg, dark up to the present row and pale after it. In the power chart, the first three quoted lines draw the rose curve of P<sub>aero</sub> from the column Pa, using every stride-th row so that there are about two points per pixel. Where the rose curve lies above the black one, the rotor is storing kinetic energy, and where it lies below, returning it, as (7) says. In drawCp(), n0 is the row 150 rows, 3 s, before the present one; the trail joins every third stored point (λ<sub>n</sub>, c<sub>p</sub>) from there to now, and the burgundy dot of radius 6 px marks the present operating point. X and Y turn λ and c<sub>p</sub> into px, with λ from 0 to 14 across and c<sub>p</sub> from 0 to 0.65 up. When following the wind the dot stays near the peak at λ<sub>opt</sub>; when holding speed it slides along the curve with every change of the wind.',
            code: `var pa = ds.get('Pa');
c.strokeStyle = ROSE; c.lineWidth = 1.3;
c.beginPath(); for (n = 0; n < NS; n += stride) { if (n) c.lineTo(g.sx(ts[n]), g.sy('Pa', ⟦Pa|pa[n]⟧)); else c.moveTo(g.sx(ts[n]), g.sy('Pa', pa[n])); } c.stroke();
...
var n0 = Math.max(0, i - 150);
c.beginPath(); for (n = n0; n <= i; n += 3) { if (n === n0) c.moveTo(X(lam[n]), Y(cpv[n])); else c.lineTo(X(lam[n]), Y(cpv[n])); } c.lineTo(X(lam[i]), Y(cpv[i])); c.stroke();
c.fillStyle = BURG; c.beginPath(); c.arc(⟦lam|X(lam[i])⟧, ⟦cp|Y(cpv[i])⟧, 6, 0, Math.PI * 2); c.fill();`,
            syms: [
                ['lam', 'λ<sub>n</sub>', 'lam[i]', 'tip-speed ratio of the dot, no unit'],
                ['cp', 'c<sub>p</sub>', 'cpv[i]', 'power coefficient of the dot, no unit'],
                ['Pg', 'P<sub>gen</sub>', 'Pg[n]', 'generator power of the row on screen, W (shown in kW)'],
                ['lopt', 'λ<sub>opt</sub>', "ds.get('lam_opt')", 'where the peak and the dashed vertical line are']
            ]
        }
    ]
};
