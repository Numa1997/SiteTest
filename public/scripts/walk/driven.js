/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state.
   Fig. 9, driven oscillator: the steps follow the lecture note's order and its equation numbers (1)–(8). */
window.WALK = window.WALK || {};

(function () {
    // upright type inside the italic formula: function names, units and equation numbers, as TeX sets them
    function up(s) { return '<span style="font-style:normal">' + s + '</span>'; }
    function tag(n) { return ' &emsp; ' + up('(' + n + ')'); }

    window.WALK.driven = {
        intro: 'Fourteen steps from the lecture note to the code of this page, in the order of the note: the state and its start, the equation of motion and its parameters, the exact solution with its resonance and transfer function, then the Runge–Kutta solver, the energy check, the stored run, the playback, the controller that closes the loop, and the two pictures. Each step sets an equation of the note, with its number, beside the lines of this page that evaluate it, quoted character for character; a line that reads “...” stands for page lines left out. Point at a coloured symbol and the same quantity lights up in the formula, the code and the table. The “Now” column is read from the page’s data store five times a second: the quantities of the motion (n, t, x, v, F, E) show the stored sample on screen at this moment, everything else belongs to the whole solved run.',
        steps: [
            {
                title: 'The state and the start',
                where: 'top of the script, the constants; solve(), just before the loop',
                math: 'state (⟦x|x⟧, ⟦v|v⟧), &nbsp; ⟦v|v⟧ = ẋ, &nbsp; m = 1 ' + up('kg') + '<br>x(0) = 0, &nbsp; ẋ(0) = 0, &nbsp; t = 0 &emsp; ' + up('(§2)'),
                note: 'The first quoted line fixes the constants of the whole page. M is the mass m = 1 kg, H is the time step h = 1 ms of the solver, TEND is the length of the run, 60 s, EVERY = 10 says that every tenth step is kept for drawing, and NS = 60 / 0.001 / 10 + 1 = 6 001 is the number of stored samples. Equation (1) of the next step is of second order in time, so the block at one instant is described by two numbers: the displacement x in metres, measured from the rest position, and the velocity ẋ, which the code calls v, in metres per second. The second quoted line starts the run. After Solve it starts as §2 of the note does, with the block at rest in its rest position, x(0) = 0 and ẋ(0) = 0, at the clock time t = 0 s; after you drag the block and let go, p.x0, p.v0 and p.z0 are the position, the speed of your hand and the controller’s memory at the release (§9). The same line also sets to zero the two work integrals win and wloss of step 9 and the counter n of stored samples of step 10.',
                code: `var M = 1, ⟦h|H = 0.001⟧, TEND = 60, EVERY = 10, NS = TEND / H / EVERY + 1;
...
var ⟦t|t = 0⟧, ⟦x|x = p.x0⟧, ⟦v|v = p.v0⟧, z = p.z0, win = 0, wloss = 0, n = 0, step, blew = NaN;`,
                syms: [
                    ['x', 'x', 'x', 'displacement from rest, m; Now: the stored sample on screen'],
                    ['v', 'v = ẋ', 'v', 'velocity, m/s; Now: the stored sample on screen'],
                    ['t', 't', 't', 'time, s; Now: the playback time'],
                    ['h', 'h', 'H', 'time step of the solver, s']
                ]
            },
            {
                title: 'Equation (1): Newton’s second law',
                where: 'accel(), just above solve()',
                math: 'm ẍ + ⟦c|c⟧ ẋ + ⟦k|k⟧ x = ⟦F|F<sub>0</sub> ' + up('cos') + ' Ωt⟧' + tag(1) + '<br>⟹ &nbsp; ẍ = (F<sub>0</sub> ' + up('cos') + ' ⟦W|Ω⟧t − c v − k x) / m',
                note: 'Equation (1) adds the three forces along the floor: the driver F<sub>0</sub> cos Ωt, the damper −c ẋ and the spring −k x. The solver needs only the acceleration, so the code solves (1) for ẍ and nothing else. accel(t, x, v, p) receives the clock time t in s, the state x in m and v in m/s, and the plant’s numbers in the object p of step 3: p.F0 is the force amplitude F<sub>0</sub> in N, p.W the drive angular frequency Ω in rad/s, p.c the damping coefficient c in kg/s and p.k the stiffness k in N/m; M is the mass m = 1 kg. The return line takes the drive force, subtracts the damper force and the spring force, and divides by the mass: newtons divided by kilograms, an acceleration in m/s². The time t appears on its own inside the cosine, and that is what makes the system driven: the force does not care where the block is, only what the clock says.',
                code: `function accel(t, x, v, u, p) {
return (⟦F|p.F0 * Math.cos(p.W * t)⟧ + u - ⟦c|p.c⟧ * v - ⟦k|p.k⟧ * x) / M;
}`,
                syms: [
                    ['F', 'F<sub>0</sub> cos Ωt', 'p.F0 * Math.cos(p.W * t)', 'drive force, N; Now: at the sample on screen'],
                    ['c', 'c', 'p.c', 'damping coefficient, kg/s'],
                    ['k', 'k', 'p.k', 'spring stiffness, N/m'],
                    ['W', 'Ω', 'p.W', 'drive angular frequency, rad/s']
                ]
            },
            {
                title: 'Equation (2): from the sliders to k, c and Ω',
                where: 'solve(), second line, after the timer starts',
                math: 'ẍ + 2ζ⟦w0|ω<sub>0</sub>⟧ ẋ + ω<sub>0</sub>² x = (F<sub>0</sub>/m) ' + up('cos') + ' Ωt' + tag(2) + '<br>⟦w0|ω<sub>0</sub>⟧ = √(k/m) = 2π f<sub>0</sub>, &nbsp; ζ = c / (2√(km))<br>⟹ &nbsp; ⟦k|k⟧ = m ω<sub>0</sub>², &nbsp; ⟦c|c⟧ = 2ζ m ω<sub>0</sub>, &nbsp; ⟦W|Ω⟧ = 2π f',
                note: 'Equation (2) is (1) divided by m and written with two numbers that describe the plant directly: the natural angular frequency ω<sub>0</sub> = √(k/m), at which the block would ring if there were no damper, and the damping ratio ζ = c/(2√(km)), which says how quickly the ringing dies. The sliders speak this language: they set f<sub>0</sub> = ω<sub>0</sub>/2π in Hz, ζ (a pure number), F<sub>0</sub> in N and the drive frequency f = Ω/2π in Hz, read as f0.value, zeta.value, F0.value and fd.value. The quoted line translates them back into the quantities of (1). w0 is ω<sub>0</sub> = 2π f<sub>0</sub> in rad/s. p.k is k = m ω<sub>0</sub>², the definition of ω<sub>0</sub> solved for k, in N/m. p.c is c = 2ζ m ω<sub>0</sub>, the definition of ζ solved for c with √(km) = m ω<sub>0</sub>, in kg/s. p.W is Ω = 2π f in rad/s and p.F0 is F<sub>0</sub> in N. With the defaults f<sub>0</sub> = 0.5 Hz and ζ = 0.05, so k = (2π · 0.5 Hz)² · 1 kg = 9.87 N/m and c = 2 · 0.05 · 1 kg · π s⁻¹ = 0.314 kg/s, the values in §2 of the note.',
                code: `var ⟦w0|w0 = 2 * Math.PI * f0.value⟧, p = { ⟦k|k: M * w0 * w0⟧, ⟦c|c: 2 * zeta.value * M * w0⟧, ⟦W|W: 2 * Math.PI * fd.value⟧, F0: F0.value };`,
                syms: [
                    ['w0', 'ω<sub>0</sub>', 'w0', 'natural angular frequency, rad/s'],
                    ['k', 'k', 'p.k', 'spring stiffness, N/m'],
                    ['c', 'c', 'p.c', 'damping coefficient, kg/s'],
                    ['W', 'Ω', 'p.W', 'drive angular frequency, rad/s']
                ]
            },
            {
                title: 'Equations (3) and (4): the steady state',
                where: 'steady(), called in solve() after the loop',
                math: '(ω<sub>0</sub>² − Ω² + 2iζω<sub>0</sub>Ω) Z = F<sub>0</sub>/m, &nbsp; Z = X e<sup>−iφ</sup>' + tag(3) + '<br>⟦X|X⟧ = (F<sub>0</sub>/m) / √((⟦w0|ω<sub>0</sub>⟧² − ⟦W|Ω⟧²)² + (2ζω<sub>0</sub>Ω)²), &nbsp; ⟦phi|φ⟧ = ' + up('atan2') + '(2ζω<sub>0</sub>Ω, ω<sub>0</sub>² − Ω²)' + tag(4),
                note: 'Once the start has died away, the block moves at the driver’s own frequency, x<sub>p</sub>(t) = X cos(Ωt − φ). Equation (3) finds the complex amplitude Z by turning each time derivative into a factor iΩ, and dividing by the complex denominator divides by its length and turns back by its angle; that is (4). steady(w0, z, W, F) receives ω<sub>0</sub> in rad/s as w0, ζ as z, Ω in rad/s as W and F<sub>0</sub> in N as F. The first line inside is the amplitude X of (4) in metres: F / M is F<sub>0</sub>/m, the first Math.pow is (ω<sub>0</sub>² − Ω²)², where the spring and the inertia pull against each other, and the second is (2ζω<sub>0</sub>Ω)², the damper’s share. The return line hands back X and the phase lag φ in radians. Math.atan2(y, x) is the angle of the point (x, y), here the angle of the denominator of (3), and it lies between 0 and π because its first argument 2ζω<sub>0</sub>Ω is positive. The last quoted line, in solve(), keeps both as st.X and st.phi. With the defaults X = 0.482 m and φ = 0.442 rad = 25.3°; the table shows φ in degrees, converted once in solve() as φ · 180/π.',
                code: `function steady(w0, z, W, F) {
var ⟦X|X = (F / M) / Math.sqrt(Math.pow(w0 * w0 - W * W, 2) + Math.pow(2 * z * w0 * W, 2))⟧;
return { X: X, ⟦phi|phi: Math.atan2(2 * z * w0 * W, w0 * w0 - W * W)⟧ };
}
...
var on = p.Kp > 0 || p.Ki > 0 || p.Kd > 0, st = on ? closed(p) : steady(⟦w0|w0⟧, zeta.value, ⟦W|p.W⟧, p.F0), xe = equilibrium(p), err = 0, xm = 0, xmax = 1e-9;`,
                syms: [
                    ['X', 'X', 'st.X', 'steady amplitude, m'],
                    ['phi', 'φ', 'st.phi', 'phase lag of x behind F, rad; shown in degrees'],
                    ['w0', 'ω<sub>0</sub>', 'w0', 'natural angular frequency, rad/s'],
                    ['W', 'Ω', 'p.W', 'drive angular frequency, rad/s']
                ]
            },
            {
                title: 'Equation (5): the exact motion from rest',
                where: 'exact(), called for every stored sample in solve()',
                math: 'x(t) = ⟦X|X⟧ ' + up('cos') + '(⟦W|Ω⟧t − ⟦phi|φ⟧) + e<sup>−t/τ</sup>(C<sub>1</sub> ' + up('cos') + ' ω<sub>d</sub>t + C<sub>2</sub> ' + up('sin') + ' ω<sub>d</sub>t)<br>C<sub>1</sub> = −X ' + up('cos') + ' φ, &nbsp; C<sub>2</sub> = (ζω<sub>0</sub> C<sub>1</sub> − XΩ ' + up('sin') + ' φ) / ω<sub>d</sub>' + tag(5) + '<br>ω<sub>d</sub> = ⟦w0|ω<sub>0</sub>⟧√(1 − ζ²), &nbsp; τ = 1/(ζω<sub>0</sub>)',
                note: 'Equation (5) adds to the steady motion of (4) a free ringing of the plant, a solution of (2) with the right-hand side set to zero, and chooses the ringing’s two constants so that the block starts where the run starts, x(0) = x0 and ẋ(0) = v0 (both zero after Solve). exact(t, w0, z, W, st, x0, v0) receives the time t in s, ω<sub>0</sub> as w0 in rad/s, ζ as z, Ω as W in rad/s, and st, the X and φ of step 4. The first line computes the damped ringing frequency ω<sub>d</sub> = ω<sub>0</sub>√(1 − ζ²) as wd in rad/s, and the constants C<sub>1</sub> and C<sub>2</sub> of (5), both in metres. The return line is x(t) of (5) in metres: st.X * Math.cos(W * t - st.phi) is the steady part, and Math.exp(-z * w0 * t) is the decay e<sup>−t/τ</sup>, because ζω<sub>0</sub>t = t/τ with τ = 1/(ζω<sub>0</sub>). With the defaults ω<sub>d</sub> = 3.138 rad/s (f<sub>d</sub> = 0.499 Hz), τ = 6.37 s, C<sub>1</sub> = −0.436 m and C<sub>2</sub> = −0.208 m. The page evaluates (5) at the 6 001 stored times only as a ruler for the numerical run of step 8 (the grading is step 10); it never draws (5).',
                code: `function exact(t, w0, z, W, st, x0, v0) {
var wd = w0 * Math.sqrt(1 - z * z), C1 = x0 - st.X * Math.cos(st.phi), C2 = (v0 + z * w0 * C1 - st.X * W * Math.sin(st.phi)) / wd;
return ⟦X|st.X⟧ * Math.cos(⟦W|W⟧ * t - ⟦phi|st.phi⟧) + Math.exp(-z * w0 * t) * (C1 * Math.cos(wd * t) + C2 * Math.sin(wd * t));
}`,
                syms: [
                    ['X', 'X', 'st.X', 'steady amplitude, m'],
                    ['phi', 'φ', 'st.phi', 'phase lag, rad; shown in degrees'],
                    ['W', 'Ω', 'W', 'drive angular frequency, rad/s'],
                    ['w0', 'ω<sub>0</sub>', 'w0', 'natural angular frequency, rad/s']
                ]
            },
            {
                title: 'Equations (6) and (6a): the quality factor and the peak',
                where: 'solve(), where the results are written into the store',
                math: 'X(ω<sub>0</sub>) = F<sub>0</sub>/(2ζ⟦k|k⟧) = ⟦Q|Q⟧ F<sub>0</sub>/k, &nbsp; ⟦Q|Q⟧ = 1/(2ζ)' + tag(6) + '<br>(ω<sub>0</sub>² − Ω²)² + (2ζω<sub>0</sub>Ω)² = [Ω² − ω<sub>0</sub>²(1 − 2ζ²)]² + 4ζ²(1 − ζ²)ω<sub>0</sub><sup>4</sup>' + tag('6a') + '<br>⟦fr|f<sub>r</sub>⟧ = f<sub>0</sub>√(1 − 2ζ²) &nbsp; for ζ &lt; 1/√2, &nbsp; ⟦tau|τ⟧ = 1/(ζ⟦w0|ω<sub>0</sub>⟧)',
                note: 'Set Ω = ω<sub>0</sub> in (4): the spring term and the inertia term cancel, only the damper limits the motion, and X = (F<sub>0</sub>/m)/(2ζω<sub>0</sub>²) = F<sub>0</sub>/(2ζk). Measured against the static stretch F<sub>0</sub>/k, that is an amplification by the quality factor Q = 1/(2ζ), a pure number. Completing the square in (6a) shows that the denominator of (4) is smallest, and the amplitude largest, where the square bracket vanishes, at Ω<sub>r</sub> = ω<sub>0</sub>√(1 − 2ζ²); divided by 2π that is f<sub>r</sub> in Hz. For ζ ≥ 1/√2 the bracket cannot vanish and there is no peak. The two quoted calls store exactly these numbers. In the first line, 1 / (zeta.value * w0) is the decay time τ of (5) in s and 1 / (2 * zeta.value) is Q. The second line stores f<sub>r</sub> = f<sub>0</sub>√(1 − 2ζ²) in Hz while ζ is below Math.SQRT1_2 = 1/√2 ≈ 0.707, and 0 otherwise, which the caption of the Bode plot shows as “no resonance peak”. With the defaults Q = 10, τ = 6.37 s and f<sub>r</sub> = 0.4987 Hz; Q appears in the readout “Quality factor Q”, f<sub>r</sub> in the caption of the Bode plot. The page takes the peak from this formula; it does not search for it numerically.',
                code: `... ds.set('tau', ⟦tau|1 / (zeta.value * w0)⟧); ds.set('Q', ⟦Q|1 / (2 * zeta.value)⟧);
... ds.set('fr', ⟦fr|zeta.value < Math.SQRT1_2 ? f0.value * Math.sqrt(1 - 2 * zeta.value * zeta.value) : 0⟧);`,
                syms: [
                    ['w0', 'ω<sub>0</sub>', 'w0', 'natural angular frequency, rad/s'],
                    ['k', 'k', 'p.k', 'spring stiffness, N/m']
                ]
            },
            {
                title: 'Equation (7): the transfer function and the Bode plot',
                where: 'bode(), called at the end of solve(); and solve() for the dot at the drive frequency',
                math: 'X(s) = G(s) F(s), &nbsp; G(s) = 1 / (ms² + cs + k)' + tag(7) + '<br>s = iΩ: &nbsp; G(iΩ) = ⟦X|X⟧ e<sup>−i⟦phi|φ⟧</sup> / F<sub>0</sub><br>|G(iΩ)| = 1 / (m √((⟦w0|ω<sub>0</sub>⟧² − Ω²)² + (2ζω<sub>0</sub>Ω)²)), &nbsp; ' + up('arg') + ' G(iΩ) = −φ',
                note: 'Equation (7) is the control engineer’s summary of (1): the Laplace transform turns each time derivative into a factor s, and the output is the input multiplied by G(s). Setting s = iΩ and comparing with (3) gives G(iΩ) = X e<sup>−iφ</sup>/F<sub>0</sub>, so |G(iΩ)| is the steady amplitude per newton of force, in m/N, and its angle is the phase lag with a minus sign. bode() first reads ω<sub>0</sub> in rad/s and ζ back from the store as w0 and z. Its loop then evaluates (7) at 241 frequencies spaced evenly on a logarithmic axis from 0.05 Hz to 0.05 · 40 = 2 Hz: f is the frequency of the sweep in Hz and W = 2πf its angular frequency in rad/s, a sweep variable, not the drive Ω of the run. fb[j] keeps the frequency, G[j] is |G(iΩ)| in m/N, the same expression as X of step 4 with F<sub>0</sub> = 1 N, and P[j] is φ in degrees. These two arrays are the two curves of the Bode plot. The last quoted line, in solve(), evaluates |G(iΩ)| at the drive frequency itself, which places the filled dot; with the defaults it is 0.482 m/N, X/F<sub>0</sub> with F<sub>0</sub> = 1 N. The ring around the dot does not come from (7): it is the largest |x| of the numerical run in its last 10 s, divided by F<sub>0</sub>, and the two coincide once the run has settled.',
                code: `var ⟦w0|w0 = ds.get('omega0')⟧, z = ds.get('zeta');
...
for (var j = 0; j < 241; j++) {
var f = 0.05 * Math.pow(40, j / 240), W = 2 * Math.PI * f;
fb[j] = f;
⟦G|G[j] = 1 / (M * Math.sqrt(Math.pow(w0 * w0 - W * W, 2) + Math.pow(2 * z * w0 * W, 2)))⟧;
P[j] = Math.atan2(2 * z * w0 * W, w0 * w0 - W * W) * 180 / Math.PI;
}
...
ds.set('G_drive', ⟦X|1 / (M * Math.sqrt(Math.pow(w0 * w0 - p.W * p.W, 2) + Math.pow(2 * zeta.value * w0 * p.W, 2)))⟧);`,
                syms: [
                    ['w0', 'ω<sub>0</sub>', 'w0', 'natural angular frequency, rad/s'],
                    ['W', 'Ω', 'p.W', 'drive angular frequency of the run, rad/s (in bode(), W is the sweep)'],
                    ['X', 'X', 'st.X', 'steady amplitude, m; equal to |G(iΩ)| · F<sub>0</sub>'],
                    ['phi', 'φ', 'st.phi', 'phase lag, shown in degrees']
                ]
            },
            {
                title: 'The fourth-order Runge–Kutta step (§8)',
                where: 'solve(), the loop over the time steps',
                math: 'a(t, x, v) = ẍ from (1), &nbsp; ⟦h|h⟧ = 1 ' + up('ms') + ', &nbsp; ⟦steps|N⟧ = 60 ' + up('s') + ' / h<br>a<sub>1</sub> = a(t, x, v), &nbsp; x<sub>2</sub> = x + (h/2) v, &nbsp; v<sub>2</sub> = v + (h/2) a<sub>1</sub><br>a<sub>2</sub> = a(t + h/2, x<sub>2</sub>, v<sub>2</sub>), &nbsp; x<sub>3</sub> = x + (h/2) v<sub>2</sub>, &nbsp; v<sub>3</sub> = v + (h/2) a<sub>2</sub><br>a<sub>3</sub> = a(t + h/2, x<sub>3</sub>, v<sub>3</sub>), &nbsp; x<sub>4</sub> = x + h v<sub>3</sub>, &nbsp; v<sub>4</sub> = v + h a<sub>3</sub><br>a<sub>4</sub> = a(t + h, x<sub>4</sub>, v<sub>4</sub>)<br>x(t + h) = x + (h/6)(v + 2v<sub>2</sub> + 2v<sub>3</sub> + v<sub>4</sub>), &nbsp; v(t + h) = v + (h/6)(a<sub>1</sub> + 2a<sub>2</sub> + 2a<sub>3</sub> + a<sub>4</sub>)',
                note: 'The page also solves (1) numerically, so that the exact (5) can grade the result. The fourth-order Runge–Kutta method advances the state (x, v) one time step h = 1 ms at a time, and it needs the rate of change of the state, which is (v, a): the velocity is how fast x changes, and the acceleration a(t, x, v) of step 2 is how fast v changes. It asks for that rate four times per step: a<sub>1</sub> at the start, a<sub>2</sub> and a<sub>3</sub> at the middle of the step, each from a trial state built with the rate found just before, and a<sub>4</sub> at the end. In the code H is h in s, x and v are the state in m and m/s, x2, v2 to x4, v4 are the trial states, and a1 to a4 the four accelerations in m/s², each from accel() with the force at its own instant t, t + h/2 or t + h. The two update lines move x and v by h times a weighted average of the four rates, with weights 1, 2, 2, 1 over 6; this average agrees with the Taylor series of the true motion up to h⁴, so the error of one step shrinks like h⁵ and the error over the run like h⁴. The last line sets the clock to (step + 1) · H instead of adding H again and again, so the time carries no rounding drift. The loop runs over TEND / H = 60 000 steps, 60 s; at the last value of step it only stores the final sample (step 10) and stops. The lines left out in the middle are the work integrals of step 9.',
                code: `for (step = 0; step <= ⟦steps|TEND / H⟧; step++) {
...
if (step === TEND / H) break;
// RK4 on (x, v, z, W_in, W_loss); z = ∫(r − x) dt is the controller's memory, u its force at each stage
var u1 = control(x, v, z, p), a1 = accel(t, x, v, u1, p), x2 = x + 0.5 * ⟦h|H⟧ * v, v2 = v + 0.5 * H * a1, z2 = z + 0.5 * H * (p.r - x);
var u2 = control(x2, v2, z2, p), a2 = accel(t + 0.5 * H, x2, v2, u2, p), x3 = x + 0.5 * H * v2, v3 = v + 0.5 * H * a2, z3 = z + 0.5 * H * (p.r - x2);
var u3 = control(x3, v3, z3, p), a3 = accel(t + 0.5 * H, x3, v3, u3, p), x4 = x + H * v3, v4 = v + H * a3, z4 = z + H * (p.r - x3);
var u4 = control(x4, v4, z4, p), a4 = accel(t + H, x4, v4, u4, p);
...
x += H / 6 * (v + 2 * v2 + 2 * v3 + v4);
v += H / 6 * (a1 + 2 * a2 + 2 * a3 + a4);
t = (step + 1) * H;`,
                syms: [
                    ['h', 'h', 'H', 'time step, s'],
                    ['steps', 'N', 'TEND / H', 'time steps in one solve']
                ]
            },
            {
                title: 'Equation (8): where the energy goes',
                where: 'solve(), inside the loop and after it',
                math: 'E = ½ m ẋ² + ½ k x²<br>E(T) − E(0) = ⟦Win|W<sub>in</sub>⟧ − ⟦Wloss|W<sub>loss</sub>⟧, &nbsp; W<sub>in</sub> = ∫<sub>0</sub><sup>T</sup> F ẋ d<span style="font-style:normal">t</span>, &nbsp; W<sub>loss</sub> = ∫<sub>0</sub><sup>T</sup> c ẋ² d<span style="font-style:normal">t</span>' + tag(8) + '<br>⟦bal|balance⟧ = |E(T) − E(0) − (W<sub>in</sub> − W<sub>loss</sub>)| / W<sub>in</sub>',
                note: 'The coil does work at the rate P<sub>in</sub> = F ẋ, with F the outside push plus the controller’s u, and the damper turns energy into heat at the rate P<sub>loss</sub> = c ẋ². Equation (8) says that the stored energy E changes over the run, T = 60 s, by the difference of their integrals. The code integrates both inside the same Runge–Kutta step as the motion and with the same weights 1, 2, 2, 1. Fa, Fm and Fb are the drive force in N at the start, the middle and the end of the step, and v, v2, v3, v4 are the four velocities of step 8, so Fa * v and the other products are powers in W, and H / 6 times their weighted sum is the work of one step in J. win is W<sub>in</sub> and wloss is W<sub>loss</sub>, both in J, and p.c is c in kg/s. After the loop both are stored, and Es[NS - 1] − Es[0] is E(T) − E(0), taken from the stored energies of step 10. The last line stores by how much (8) misses, as a fraction of W<sub>in</sub>. The work–energy theorem holds exactly for the true motion, so this one number tests the whole computation. With the defaults W<sub>in</sub> = 19.03 J, W<sub>loss</sub> = 17.93 J and E(T) − E(0) = 1.11 J, and the balance is 1.3 × 10⁻¹², the readout “Energy balance”.',
                code: `var Fa = p.F0 * Math.cos(p.W * t), Fm = p.F0 * Math.cos(p.W * (t + 0.5 * H)), Fb = p.F0 * Math.cos(p.W * (t + H));
⟦Win|win⟧ += H / 6 * ((Fa + u1) * v + 2 * (Fm + u2) * v2 + 2 * (Fm + u3) * v3 + (Fb + u4) * v4);
⟦Wloss|wloss⟧ += H / 6 * p.c * (v * v + 2 * v2 * v2 + 2 * v3 * v3 + v4 * v4);
...
ds.set('Win', win); ds.set('Wloss', wloss);
ds.set('balance', ⟦bal|win > 0 ? Math.abs(Es[NS - 1] - Es[0] - (win - wloss)) / win : 0⟧);`,
                syms: [
                    ['Win', 'W<sub>in</sub>', 'win', 'work done by the driver over the run, J'],
                    ['Wloss', 'W<sub>loss</sub>', 'wloss', 'heat made by the damper over the run, J'],
                    ['bal', 'balance', "ds.set('balance', …)", 'how far (8) misses, relative to W<sub>in</sub>']
                ]
            },
            {
                title: 'Store every tenth state, and grade it against (5)',
                where: 'solve(), top of the time loop; then the loop over the stored samples',
                math: '⟦n|n⟧ = step / 10, &nbsp; ⟦t|t<sub>n</sub>⟧ = n · 10h = n · 10 ' + up('ms') + '<br>⟦F|F<sub>n</sub>⟧ = F<sub>0</sub> ' + up('cos') + ' Ωt<sub>n</sub>, &nbsp; ⟦E|E<sub>n</sub>⟧ = ½ m v<sub>n</sub>² + ½ k x<sub>n</sub>², &nbsp; P<sub>in,n</sub> = F<sub>n</sub> v<sub>n</sub>, &nbsp; P<sub>loss,n</sub> = c v<sub>n</sub>²<br>⟦err|error⟧ = ' + up('max') + '<sub>n</sub> |⟦x|x<sub>n</sub>⟧ − x(t<sub>n</sub>)|, &nbsp; x(t) from (5)',
                note: 'Sixty thousand states are far more than a picture needs, so the page keeps every tenth one. When step is a multiple of EVERY = 10, the first quoted block writes one row of the data store, at the moment that state is known: ts[n] is the time t<sub>n</sub> in s, xs[n] and vs[n] are the displacement in m and the velocity in m/s, Fs[n] is the drive force F<sub>n</sub> in N, Es[n] is the energy of the oscillator, kinetic plus spring, in J, and Pin[n] and Ploss[n] are the powers of the driver and of the damper in W, all at the same instant. Then n counts on to the next row. The run fills 6 001 rows, one every 10 ms from 0 s to 60 s. After the time loop, the second block evaluates the exact motion (5) of step 5 at every stored time, xex[n] in m, and keeps the largest difference from the Runge–Kutta displacement as err, in m. With the defaults it is 5.3 × 10⁻¹² m, the readout “RK4 vs exact”: over the whole minute the solver agrees with the pencil-and-paper answer to a few picometres. The playback of step 11 reads these rows and computes no state of its own.',
                code: `if (step % EVERY === 0) {
⟦t|ts[n] = t⟧; ⟦x|xs[n] = x⟧; vs[n] = v; zs[n] = z; ⟦F|Fpush[n] = p.F0 * Math.cos(p.W * t)⟧;
⟦E|Es[n] = 0.5 * M * v * v + 0.5 * p.k * x * x⟧; Pin[n] = Fs[n] * v; Ploss[n] = p.c * v * v;
⟦n|n++⟧;
}
...
for (n = 0; n < NS; n++) {
if (!on) xex[n] = exact(ts[n], w0, zeta.value, p.W, st, p.x0, p.v0);
⟦err|err = Math.max(err, Math.abs(xs[n] - xex[n]))⟧;
...`,
                syms: [
                    ['n', 'n', 'n', 'row of the store; Now: the row on screen'],
                    ['t', 't<sub>n</sub>', 'ts[n]', 'time of the row, s; Now: the playback time'],
                    ['x', 'x<sub>n</sub>', 'xs[n]', 'displacement, m'],
                    ['v', 'v<sub>n</sub>', 'vs[n]', 'velocity, m/s'],
                    ['F', 'F<sub>n</sub>', 'Fs[n]', 'drive force, N'],
                    ['E', 'E<sub>n</sub>', 'Es[n]', 'energy of the oscillator, J'],
                    ['err', 'error', 'err', 'largest |x<sub>n</sub> − x(t<sub>n</sub>)| over the run, m']
                ]
            },
            {
                title: 'Playback reads one stored row (§8)',
                where: 'the clock, then frame()',
                math: 't<sub>play</sub> ← t<sub>play</sub> + speed · Δt<br>⟦n|n⟧ = ' + up('round') + '(⟦t|t<sub>play</sub>⟧ / 10 ' + up('ms') + '), &nbsp; shown: ⟦x|x<sub>n</sub>⟧, ⟦v|v<sub>n</sub>⟧, ⟦F|F<sub>n</sub>⟧, ⟦E|E<sub>n</sub>⟧',
                note: 'Because the driver’s force is known for all time in advance, the whole run is fixed the moment Solve is pressed, and watching it is only looking it up. On every animation frame the clock adds the real time since the last frame, dt in s, times the speed slider to the playback time playT, which is t<sub>play</sub> in s, and stops the clock at 60 s. frame() then turns t<sub>play</sub> into the nearest stored row, i = round(t<sub>play</sub> / (EVERY · H)) = round(t<sub>play</sub> / 10 ms), held between the rows 0 and 6 000, and copies that row’s x, v, F, E, P<sub>in</sub> and drive phase into the store as the values shown now. Nothing is interpolated, so the block, the charts, the data panel and the “Now” column of this walkthrough all show the same row, and the “Stored run” slider can jump to any instant. The time in the table is t<sub>play</sub> itself; to its two decimals it equals t<sub>n</sub> = n · 10 ms of the row on screen.',
                code: `⟦t|playT⟧ += speed.value * dt;
if (playT > TEND) { playT = TEND; clk.set(false); }
...
var ⟦n|i = Math.min(NS - 1, Math.max(0, Math.round(playT / (EVERY * H))))⟧;
iNow = i;
ds.set('i_now', i); ds.set('t_play', playT);
ds.set('x_now', ⟦x|ds.get('xs')[i]⟧); ds.set('v_now', ⟦v|ds.get('vs')[i]⟧); ds.set('F_now', ⟦F|ds.get('Fs')[i]⟧);
ds.set('E_now', ⟦E|ds.get('Es')[i]⟧); ds.set('Pin_now', ds.get('Pin')[i]); ds.set('ph_now', ds.get('ph')[i]);`,
                syms: [
                    ['n', 'n', 'i', 'stored row shown now'],
                    ['t', 't<sub>play</sub>', 'playT', 'playback time, s'],
                    ['x', 'x<sub>n</sub>', "ds.get('xs')[i]", 'displacement shown now, m'],
                    ['v', 'v<sub>n</sub>', "ds.get('vs')[i]", 'velocity shown now, m/s'],
                    ['F', 'F<sub>n</sub>', "ds.get('Fs')[i]", 'drive force shown now, N'],
                    ['E', 'E<sub>n</sub>', "ds.get('Es')[i]", 'energy shown now, J']
                ]
            },
            {
                title: 'Closing the loop: the controller’s force and where the block comes to rest (§9)',
                where: 'control(), equilibrium() and closed(); then the RK4 loop in solve()',
                math: '⟦u|u⟧ = ⟦Kp|K<sub>p</sub>⟧(⟦r|r⟧ − x) + ⟦Ki|K<sub>i</sub>⟧⟦z|z⟧ − ⟦Kd|K<sub>d</sub>⟧ ẋ, &nbsp; ż = r − x &nbsp; (12)<br>⟦xeq|x*⟧ = K<sub>p</sub> r / (k + K<sub>p</sub>) if K<sub>i</sub> = 0, &nbsp; x* = r if K<sub>i</sub> &gt; 0 &nbsp; (14)<br>stable iff (c + K<sub>d</sub>)(k + K<sub>p</sub>) &gt; m K<sub>i</sub> &nbsp; (15)',
                note: 'With the controller on, the coil’s current is no longer decided in advance: control() computes the force u of (12) from the block’s present position x and speed v and from the memory z = ∫(r − x) dt, which the solver carries as a third state next to x and v. The gains are read from the sliders as p.Kp in N/m, p.Ki in N/(m·s) and p.Kd in kg/s, the target as p.r in m. Inside the RK4 loop the controller is evaluated at each of the four stages (u1 to u4), so that the force seen by the block is always the force the controller would give for that intermediate state, and z advances with the same weights as x and v. The coil then carries F = F<sub>0</sub> cos Ωt + u, stored as Fs[n]; the open-loop push alone is kept in Fpush[n], and u with its three parts in us, uP, uI and uD, so that the controller box on the screen and the data panel can show who is doing the pushing. equilibrium() is (14): without integral action the block stops where K<sub>p</sub>(r − x*) = k x*, with it at r. The Routh–Hurwitz test (15) is stored as margin, and stable is its sign; the readout says “unstable” and, when the run blew up, at what time the solver stopped. closed() is the steady swing (16) about x*, which replaces (4) as the exact answer the page grades RK4 against; exactClosed() adds the free motion with the matrix exponential of the loop’s state matrix. With the presets K<sub>p</sub> = 20 N/m, K<sub>d</sub> = 4 kg/s and r = 0.30 m, x* = 0.201 m without integral action; with K<sub>i</sub> = 10 N/(m·s) the block reaches 0.300 m, and the integral part alone ends up carrying the 2.96 N that hold the spring.',
                code: `function control(x, v, z, p) {
...
return ⟦Kp|p.Kp⟧ * (⟦r|p.r⟧ - x) + ⟦Ki|p.Ki⟧ * ⟦z|z⟧ - ⟦Kd|p.Kd⟧ * v;
...
function equilibrium(p) { return p.Ki > 0 ? p.r : p.Kp * p.r / (p.k + p.Kp); }
...
var u1 = control(x, v, z, p), a1 = accel(t, x, v, u1, p), x2 = x + 0.5 * H * v, v2 = v + 0.5 * H * a1, z2 = z + 0.5 * H * (p.r - x);
...
z += H / 6 * ((p.r - x) + 2 * (p.r - x2) + 2 * (p.r - x3) + (p.r - x4));
...
uP[n] = p.Kp * (p.r - x); uI[n] = p.Ki * z; uD[n] = -p.Kd * v; ⟦u|us[n] = control(x, v, z, p)⟧; Fs[n] = Fpush[n] + us[n];
...
ds.set('x_eq', ⟦xeq|xe⟧); ds.set('F_eq', p.k * xe); ds.set('t_blow', blew); ds.set('margin', (p.c + p.Kd) * (p.k + p.Kp) - M * p.Ki); ds.set('stable', (p.c + p.Kd) * (p.k + p.Kp) - M * p.Ki > 0);`,
                syms: [
                    ['u', 'u', 'us[n]', 'force the controller asks of the coil, N; Now: the row on screen'],
                    ['r', 'r', 'p.r', 'target position, m'],
                    ['Kp', 'K<sub>p</sub>', 'p.Kp', 'proportional gain, N/m'],
                    ['Ki', 'K<sub>i</sub>', 'p.Ki', 'integral gain, N/(m·s)'],
                    ['Kd', 'K<sub>d</sub>', 'p.Kd', 'derivative gain, kg/s'],
                    ['z', 'z', 'z', 'the controller’s memory ∫(r − x) dt, m·s; Now: the row on screen'],
                    ['xeq', 'x*', 'xe', 'equilibrium the loop holds, m']
                ]
            },
            {
                title: 'On screen: the coil, the forces and the block (§9)',
                where: 'the constants and solve(); then setSpan(), geom() and draw()',
                math: '⟦I|I<sub>n</sub>⟧ = F<sub>n</sub> / (⟦BL|Bℓ⟧), &nbsp; F<sub>c, n</sub> = −c v<sub>n</sub>, &nbsp; F<sub>k, n</sub> = −k x<sub>n</sub> &nbsp; (9)<br>⟦sc|px/m⟧ = A<sub>px</sub> / ⟦span|span⟧, &nbsp; ⟦fN|px/N⟧ = 2 ⟦sc|px/m⟧ / k<br>⟦bx|x<sub>block</sub>⟧ = x<sub>eq</sub> + ⟦x|x<sub>n</sub>⟧ · ⟦sc|px/m⟧, &nbsp; arrow = force · ⟦fN|px/N⟧',
                note: 'Equation (9) of the note is the coil’s force, F = Bℓ I. The page reads it the other way round: the slider sets F<sub>0</sub>, and the current the source must drive is I = F/(Bℓ), stored for every row as Is[n] in A. BL is the force constant Bℓ = 10 T·m = 10 N/A, so the default F<sub>0</sub> = 1 N needs I<sub>0</sub> = 0.1 A. In the same loop solve() stores the two other forces on the block, the damper’s −c v<sub>n</sub> and the spring’s −k x<sub>n</sub>, in N, so that the drawing has only to read them. The canvas is in CSS pixels, so the drawing needs a scale, and §9 says that it is kept from run to run: need is the half-range this run needs, the larger of its largest swing max |x<sub>n</sub>| and F<sub>0</sub>/k, in m, and setSpan() keeps the old span unless the new run needs more; Fit scale sets the span to need. In geom(), m.amp is A<sub>px</sub> = 0.11 W<sub>0</sub>, where W<sub>0</sub> is the width between the wall and the right margin in px, m.sc = A<sub>px</sub> / span is the scale in px/m, and m.fN = 2 px/m / k is the scale of the force arrows in px/N: a force is drawn twice as long as the stretch of the spring that would carry it. In draw(), bx = x<sub>eq</sub> + x<sub>n</sub> · px/m places the block, the coil’s tube follows it on its rod, and the three arrows over the block are the stored forces times px/N. The drawing differs from the store only by these two scales.',
                code: `var ⟦BL|BL = 10⟧;   // the coil's force constant Bℓ in T·m = N/A: B = 1 T in the magnet's gap, ℓ = 10 m of wire
...
⟦I|Is[n]⟧ = Fs[n] / BL; Fdamp[n] = -p.c * vs[n]; Fspr[n] = -p.k * xs[n];
...
setSpan(had ? Math.max(before, ds.get('need')) : ds.get('need'), before, false);
...
⟦sc|g.m.sc⟧ = g.m.amp / ds.get(⟦span|'span'⟧);
⟦fN|g.m.fN⟧ = 2 * g.m.sc / ds.get('k');
...
var ⟦bx|bx⟧ = m.eqX + ⟦x|ds.get('x_now')⟧ * ⟦sc|m.sc⟧;
...
ds.set('Fd_px', ds.get('F_now') * m.fN); ds.set('Fc_px', ds.get('Fc_now') * m.fN); ds.set('Fk_px', ds.get('Fk_now') * m.fN);`,
                syms: [
                    ['BL', 'Bℓ', 'BL', 'force constant of the coil, T·m = N/A'],
                    ['I', 'I<sub>n</sub>', 'Is[n]', 'current in the coil, A; Now: the row on screen'],
                    ['span', 'span', "ds.get('span')", 'half-range the screen shows, kept from run to run, m'],
                    ['sc', 'px/m', 'm.sc', 'drawing scale on this screen, css px per m'],
                    ['fN', 'px/N', 'm.fN', 'scale of the force arrows, css px per N'],
                    ['bx', 'x<sub>block</sub>', 'bx', 'centre of the block from the canvas’s left edge, css px'],
                    ['x', 'x<sub>n</sub>', "ds.get('x_now')", 'displacement shown now (a stored row, or your hand while you hold the block), m']
                ]
            },
            {
                title: 'On screen: the energy bars and the window chart (§9)',
                where: 'solve(), in the RK4 loop; then draw() and drawWindow()',
                math: '⟦Wc|W<sub>in, n</sub>⟧ = ∫<sub>0</sub><sup>t<sub>n</sub></sup> F v dt, &nbsp; ⟦Qc|W<sub>loss, n</sub>⟧ = ∫<sub>0</sub><sup>t<sub>n</sub></sup> c v² dt, &nbsp; E<sub>n</sub> = W<sub>in, n</sub> − W<sub>loss, n</sub> &nbsp; (8)<br>T<sub>window</sub> = ' + up('clamp') + '(4/f, 6 ' + up('s') + ', 20 ' + up('s') + '), &nbsp; guides at ±⟦X|X⟧ from (4)',
                note: 'The bars at the top keep the books of (8) while the run plays. The RK4 loop already carries the coil’s work win and the damper’s heat wloss along with the motion (step 9), so solve() only has to write their values at every stored row into Wc[n] and Qc[n], in J. Each frame fills the first bar to W<sub>in, n</sub>, the second to W<sub>loss, n</sub> and the third to the stored energy E<sub>n</sub>, all three as fractions of the largest of them over the run; the third is the difference of the first two, to the accuracy of step 9. The damper’s oil is shaded by P<sub>loss, n</sub> = c v<sub>n</sub>² as a fraction of its largest value in the run. Below, the window chart follows the present row. draw() makes it four drive periods wide, Tw = 4/f in s, but never less than 6 s or more than 20 s (8.9 s with f = 0.45 Hz), and lets its left edge t0 trail the present instant by 0.7 of its width, except near the start and the end of the run. Inside it, x(t) is drawn from the stored xs, F(t)/k from the stored xqs, the previous run, dotted, from xs_prev, and the last quoted line draws the two dashed rose guides at ±X, the steady amplitude of (4) read from the store. Once the start of (5) has died away, the crests of x(t) touch these guides.',
                code: `Es[n] = 0.5 * M * v * v + 0.5 * p.k * x * x; Pin[n] = Fs[n] * v; Ploss[n] = p.c * v * v; ⟦Wc|Wc[n] = win⟧; ⟦Qc|Qc[n] = wloss⟧;
...
var Tw = Math.min(20, Math.max(6, 4 / ds.get('fd'))), t0 = Math.min(TEND - Tw, Math.max(0, ts[i] - 0.7 * Tw));
...
[['W_{in}', ds.get('Wc_now'), BURG], ['W_{loss}', ds.get('Qc_now'), T.tanInk], ['E', ds.get('E_now'), T.ink2]].forEach(function (e, k) {
...
c.fillStyle = e[2]; c.fillRect(x0, y, Math.max(0, Math.min(1, e[1] / W)) * bw, 8);
...
c.beginPath(); c.moveTo(p.L, g.wy(xe + ⟦X|X⟧)); c.lineTo(p.R, g.wy(xe + X)); c.moveTo(p.L, g.wy(xe - X)); c.lineTo(p.R, g.wy(xe - X)); c.stroke();`,
                syms: [
                    ['Wc', 'W<sub>in, n</sub>', 'Wc[n]', 'work of the coil since t = 0, J; Now: the row on screen'],
                    ['Qc', 'W<sub>loss, n</sub>', 'Qc[n]', 'heat of the damper since t = 0, J; Now: the row on screen'],
                    ['X', 'X', "ds.get('X')", 'steady amplitude, the dashed guides, m']
                ]
            }
        ]
    };
})();
