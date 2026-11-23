/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.pendulum = {
    intro: 'Thirteen steps from the model of the lecture note to the dots on the screen. Since November 2026 the motion is not computed in your browser: the model tools/sims/double_pendulum.py computed every stored start once, on Kaggle, and the page downloads, checks and plays the result. So some steps quote the model (Python, run on Kaggle) and the others quote the page (JavaScript, run here), each marked under its title, copied character for character; a line that is only “...” stands for lines left out. In the order of the note: the stored grid and the run the sliders choose (§2, §7), the check of the file, one stored frame, the positions (1) and energies (3) and (4) of that frame, the matrix of (8), the accelerations (9) as the model computes them, the chaos twin of §6, the DOP853 step and the energy check of §7, the playing clock and the cubic between frames, and the drawing of §8. The table gives each symbol, its name in the code, its value in the frame played now, and its meaning with its unit. The small-swing modes (10) and (11) have no code of their own. Hover over or tap a symbol to light it in all three places.',
    steps: [
        {
            title: 'The stored grid and the run the sliders choose',
            where: 'the page: restart() and start(): which file and which run in it',
            math: '⟦m2|m<sub>2</sub>⟧ = m<sub>1</sub> e<sup>ln(m₂/m₁)</sup>, ln(m₂/m₁) ∈ {−2.3, 0, 2.3}; ⟦l2|l<sub>2</sub>⟧ = l<sub>1</sub> e<sup>ln(l₂/l₁)</sup>, ln(l₂/l₁) ∈ {−1.6, 0, 1.6}<br>θ<sub>1</sub>(0), θ<sub>2</sub>(0) ∈ {−150°, −120°, …, 180°}, ω<sub>1</sub>(0) = ω<sub>2</sub>(0) = 0<br>file ⟦file|dp_<i>ij</i>_<i>kk</i>.bin⟧: cell (i, j), θ<sub>1</sub> index k; run in it: θ<sub>2</sub> index',
            note: 'Section 2 fixes m<sub>1</sub> = 1 kg, l<sub>1</sub> = 1 m and g = 9.81 m/s². The model computed 1296 starts: three lower masses, three lower rod lengths, and both starting angles on the protractor marks every 30°, each released from rest. The mass and length sliders hold the natural logarithms of the ratios, as before, and now move only between the stored values; the angle sliders move in steps of 30°. restart() first downloads double_pendulum.json, the model’s summary, whose params hold the grid. nearestIndex() finds the grid position of each slider (−180° is the same position as 180°, so it reads as 180°), and the name of the file is built from the mass index, the length index and the two-digit θ<sub>1</sub> index; inside that file the twelve runs follow θ<sub>2</sub>, so run is the θ<sub>2</sub> index. When the file has arrived and passed its check, start() reads m<sub>2</sub> and l<sub>2</sub> in kg and m from the file’s own header, never from the sliders, and sets the played time back to zero.',
            code: `SUM = s.json; var p = SUM.params, a1 = th1.value <= -180 ? 180 : th1.value, a2 = th2.value <= -180 ? 180 : th2.value;
var ⟦file|name = 'dp_' + nearestIndex(p.ln_m, mass.value) + nearestIndex(p.ln_l, len.value) + '_' + ('0' + nearestIndex(p.th_deg, a1)).slice(-2) + '.bin'⟧;
want = name; run = nearestIndex(p.th_deg, a2); ds.set('file', name);
...
P = d; ⟦m2|m2 = h.cell.m2⟧; ⟦l2|l2 = h.cell.l2⟧; m1 = h.m1; l1 = h.l1; g = h.g; S = r0.S; tau = 0;`,
            syms: [
                ['file', 'file', 'name', 'the stored file played now'],
                ['m2', 'm<sub>2</sub>', 'm2', 'lower bob mass, kg (m<sub>1</sub> = 1 kg)'],
                ['l2', 'l<sub>2</sub>', 'l2', 'lower rod length, m (l<sub>1</sub> = 1 m)']
            ]
        },
        {
            title: 'The file and its fingerprint',
            where: 'the page: load(name)',
            math: 'SHA-256(file) = the fingerprint in generations.json ⇒ the file is used; otherwise nothing is drawn<br>file = “DPN1”, header length (4 bytes), header (JSON), frames (2-byte integers)',
            note: 'generations.json, written by the Kaggle line, names the newest generation of the model and, for every file it made, its size and its SHA-256: a 64-character fingerprint that changes if a single bit of the file changes. load() downloads the file, computes its SHA-256 in the browser with crypto.subtle and compares the two. Only a file that matches is used; any other ends in the sentence the figure shows instead of a picture, and the page never falls back to computing. The second line reads the file: after four letters of label comes the length of the header in bytes, then the header itself, written as JSON (the cell, the frame rate, the steps of every column and one entry per run with its starting energy and its energy check), and then the frames, as 2-byte whole numbers. The Now column shows the date of the Kaggle run and whether the fingerprint matched.',
            code: `if (hex(d) !== e.files[name].sha256) throw new Error(name + ': SHA-256 differs from generations.json');
...
var hl = new DataView(buf).getUint32(4, true), hdr = JSON.parse(new TextDecoder().decode(new Uint8Array(buf, 8, hl)));`,
            syms: [
                ['sha', 'SHA-256', 'hex(d)', 'the file’s fingerprint, compared with generations.json'],
                ['gdate', 'date', 'e.date', 'date of the Kaggle run that made the file']
            ]
        },
        {
            title: 'One stored frame',
            where: 'the page: frame(k)',
            math: '⟦k|k⟧ = the frame read now; value = stored integer × its step<br>angles: step 10<sup>−4</sup> rad; ω, α: the file’s own steps; log<sub>10</sub> d: step 2 × 10<sup>−4</sup>',
            note: 'Every frame of a run holds nine numbers: θ<sub>1</sub>, θ<sub>2</sub>, ω<sub>1</sub>, ω<sub>2</sub>, α<sub>1</sub>, α<sub>2</sub>, the twin’s two angles and the logarithm of the twin distance. Each is stored as a whole number of small steps, so that it fits in 2 bytes. frame(k) finds frame k of the chosen run (runs follow one another, each with the same number of frames) and multiplies each integer by its step, from the header’s scale: angles in steps of 10<sup>−4</sup> rad, which at the end of a 1 m rod is 0.1 mm; angular velocities and accelerations in steps the model chose for each file so that its largest value fits. The rounding is at most half a step; the data panel shows what it does to the energy as ε<sub>2 B</sub>. The angles are stored folded into −π … π; the page unfolds them in step 11. The Now column shows the frame and its numbers.',
            code: `var h = P.hdr, sc = h.scale, o = (run * h.frames + ⟦k|k⟧) * C, F = P.F;
return [F[o] * sc.th, F[o + 1] * sc.th, F[o + 2] * sc.w, F[o + 3] * sc.w, F[o + 4] * sc.a, F[o + 5] * sc.a, F[o + 6] * sc.th, F[o + 7] * sc.th, F[o + 8] * sc.log10d];`,
            syms: [
                ['k', 'k', 'k', 'the stored frame read now'],
                ['t1', 'θ<sub>1</sub>', 'F[o] * sc.th', 'upper rod angle of frame k, rad'],
                ['t2', 'θ<sub>2</sub>', 'F[o + 1] * sc.th', 'lower rod angle of frame k, rad'],
                ['o1', 'ω<sub>1</sub>', 'F[o + 2] * sc.w', 'upper angular velocity of frame k, rad/s'],
                ['o2', 'ω<sub>2</sub>', 'F[o + 3] * sc.w', 'lower angular velocity of frame k, rad/s']
            ]
        },
        {
            title: 'Where the bobs are',
            where: 'the page: bookkeeping(s), the bob positions in metres',
            math: 'x<sub>1</sub> = l<sub>1</sub> sin ⟦t1|θ<sub>1</sub>⟧, y<sub>1</sub> = −l<sub>1</sub> cos ⟦t1|θ<sub>1</sub>⟧<br>x<sub>2</sub> = x<sub>1</sub> + ⟦l2|l<sub>2</sub>⟧ sin ⟦t2|θ<sub>2</sub>⟧, y<sub>2</sub> = y<sub>1</sub> − ⟦l2|l<sub>2</sub>⟧ cos ⟦t2|θ<sub>2</sub>⟧<span style="font-style:normal;margin-left:1.5em">(1)</span>',
            note: 'Equation (1) puts the pivot at the origin with y pointing up. In bookkeeping(), s is the stored frame of step 3, so s[0] is θ<sub>1</sub> and s[1] is θ<sub>2</sub> in rad. The first line gives x1 and y1, the coordinates of bob 1 in metres; the second stores them and computes those of bob 2, also in metres. The minus sign in y1 = -l1 * Math.cos(s[0]) is the minus sign of (1): a hanging bob, θ<sub>1</sub> = 0, sits at y<sub>1</sub> = −1 m. These are closed formulas of the stored numbers: nothing is moved forward in time. They go to the data panel; the picture is drawn by a separate pixel mapping, step 12.',
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
            where: 'the page: bookkeeping(s), the energies of the stored frame',
            math: '⟦kin|T⟧ = ½(m<sub>1</sub>+m<sub>2</sub>)l<sub>1</sub>²ω<sub>1</sub>² + ½m<sub>2</sub>l<sub>2</sub>²ω<sub>2</sub>² + m<sub>2</sub>l<sub>1</sub>l<sub>2</sub>ω<sub>1</sub>ω<sub>2</sub> cos(θ<sub>1</sub> − θ<sub>2</sub>)<span style="font-style:normal;margin-left:1.5em">(3)</span><br>⟦pot|V⟧ = −(m<sub>1</sub>+m<sub>2</sub>)g l<sub>1</sub> cos θ<sub>1</sub> − m<sub>2</sub>g l<sub>2</sub> cos θ<sub>2</sub><span style="font-style:normal;margin-left:1.5em">(4)</span><br>⟦E|E⟧ = T + V',
            note: 'Each line is an equation of §3 in SI units, evaluated for the stored frame: s[2] and s[3] are ω<sub>1</sub> and ω<sub>2</sub> in rad/s, and c is cos(θ<sub>1</sub> − θ<sub>2</sub>), computed in step 6. kin is (3) with the bracket multiplied out: the first term gathers the upper bob and the lower bob carried along by the upper rod, the second is the lower bob’s own swing about the elbow, the third is the cross term, which makes the two speeds add fully when the rods point the same way and not at all when they are at right angles. pot is (4) letter for letter, with V = 0 at the height of the pivot. Both are in joules. E = T + V of the frame differs from the model’s starting energy E<sub>0</sub> only by the rounding of the stored numbers to 2 bytes; the data panel shows that difference as ε<sub>2 B</sub>, and the model’s own error in step 10.',
            code: `var ⟦kin|kin⟧ = 0.5 * (m1 + m2) * l1 * l1 * s[2] * s[2] + 0.5 * m2 * l2 * l2 * s[3] * s[3] + m2 * l1 * l2 * s[2] * s[3] * c;
var ⟦pot|pot⟧ = -(m1 + m2) * g * l1 * Math.cos(s[0]) - m2 * g * l2 * Math.cos(s[1]);
ds.set('T', kin); ds.set('V', pot); ds.set('L', kin - pot); ds.set('E', ⟦E|kin + pot⟧); ds.set('eps_store', (kin + pot - ds.get('E0')) / S);`,
            syms: [
                ['kin', 'T', 'kin', 'kinetic energy of the frame, J'],
                ['pot', 'V', 'pot', 'potential energy, zero at the pivot, J'],
                ['E', 'E', 'kin + pot', 'total energy of the frame, J'],
                ['E0', 'E<sub>0</sub>', 'ds.get(\'E0\')', 'starting energy, computed by the model, J']
            ]
        },
        {
            title: 'Generalised momenta and the matrix of (8)',
            where: 'the page: bookkeeping(s), the mass matrix, its determinant and the momenta',
            math: 'p<sub>1</sub> = ∂L/∂ω<sub>1</sub> = (m<sub>1</sub>+m<sub>2</sub>)l<sub>1</sub>²⟦o1|ω<sub>1</sub>⟧ + m<sub>2</sub>l<sub>1</sub>l<sub>2</sub>⟦o2|ω<sub>2</sub>⟧ cos ⟦d|δ⟧<br>p<sub>2</sub> = ∂L/∂ω<sub>2</sub> = m<sub>2</sub>l<sub>2</sub>²⟦o2|ω<sub>2</sub>⟧ + m<sub>2</sub>l<sub>1</sub>l<sub>2</sub>⟦o1|ω<sub>1</sub>⟧ cos ⟦d|δ⟧<br>det M = m<sub>2</sub>l<sub>1</sub>l<sub>2</sub> · det = m<sub>2</sub>l<sub>1</sub>²l<sub>2</sub>²(m<sub>1</sub> + m<sub>2</sub> sin²δ) > 0<span style="font-style:normal;margin-left:1.5em">(8)</span>',
            note: 'The derivation of §4 is done once, on paper; the model evaluates its result (9) in step 7. What the page keeps, for the data panel, are the pieces of §4.1 and of (8), for the stored frame. d = s[0] - s[1] is the angle δ between the rods in rad and c is cos δ. The array Mm holds, row by row and in kg m², the matrix M of the kinetic energy, T = ½(ω<sub>1</sub>, ω<sub>2</sub>) M (ω<sub>1</sub>, ω<sub>2</sub>)<sup>T</sup>: Mm[0] = (m<sub>1</sub>+m<sub>2</sub>)l<sub>1</sub>², the off-diagonal Mm[1] = Mm[2] = m<sub>2</sub>l<sub>1</sub>l<sub>2</sub> cos δ, and Mm[3] = m<sub>2</sub>l<sub>2</sub>². Multiplied by the angular velocities s[2] = ω<sub>1</sub> and s[3] = ω<sub>2</sub>, it gives p1 and p2, the generalised momenta of §4.1 in kg m²/s. detM = M<sub>00</sub>M<sub>11</sub> − M<sub>01</sub>² is m<sub>2</sub>l<sub>1</sub>l<sub>2</sub> times the det of (8), in kg² m⁴; it is positive for every state, which is why (8) always has exactly one solution.',
            code: `var ⟦d|d = s[0] - s[1]⟧, c = Math.cos(⟦d|d⟧);
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
            title: 'The two angular accelerations',
            where: 'the model (Python, run on Kaggle): accel(s, m2, l2) in tools/sims/double_pendulum.py',
            math: '⟦den|D′⟧ = 2m<sub>1</sub> + ⟦m2|m<sub>2</sub>⟧ − m<sub>2</sub> cos 2δ = 2(m<sub>1</sub> + m<sub>2</sub> sin²δ)<br>⟦a1|α<sub>1</sub>⟧ = [−g(2m<sub>1</sub>+m<sub>2</sub>) sin θ<sub>1</sub> − m<sub>2</sub>g sin(θ<sub>1</sub>−2θ<sub>2</sub>) − 2m<sub>2</sub> sin δ (ω<sub>2</sub>²l<sub>2</sub> + ω<sub>1</sub>²l<sub>1</sub> cos δ)] / (l<sub>1</sub>D′)<br>⟦a2|α<sub>2</sub>⟧ = 2 sin δ [ω<sub>1</sub>²l<sub>1</sub>(m<sub>1</sub>+m<sub>2</sub>) + g(m<sub>1</sub>+m<sub>2</sub>) cos θ<sub>1</sub> + ω<sub>2</sub>²l<sub>2</sub>m<sub>2</sub> cos δ] / (l<sub>2</sub>D′)<span style="font-style:normal;margin-left:1.5em">(9)</span>',
            note: 'This is (9), as the model on Kaggle evaluates it; the page no longer does. The model is written in Python with NumPy, where np.sin and np.cos are the sine and cosine, M1 is m<sub>1</sub> = 1 kg, L1 is l<sub>1</sub> = 1 m and G is g = 9.81 m/s². The first line unpacks the state into t1 = θ<sub>1</sub>, t2 = θ<sub>2</sub> in rad and o1 = ω<sub>1</sub>, o2 = ω<sub>2</sub> in rad/s, and forms d, the angle δ between the rods. den is the bracket under both fractions; with 2 sin²δ = 1 − cos 2δ it equals 2(m<sub>1</sub> + m<sub>2</sub> sin²δ), never less than 2 kg, so the divisions are always safe. In a1 the first two terms are the pull of gravity, the third carries the squares of the angular velocities, the push and pull the rods give each other when they turn. a2 carries the common factor 2 sin δ, so α<sub>2</sub> is zero whenever the rods are in one line. The model stores both for every frame, and the page shows them; the data panel recomputes them from the stored θ and ω as a check.',
            code: `t1, t2, o1, o2 = s[0], s[1], s[2], s[3]; ⟦d|d = t1 - t2⟧
⟦den|den = 2 * M1 + m2 - m2 * np.cos(2 * d)⟧
⟦a1|a1⟧ = (-G * (2 * M1 + m2) * np.sin(t1) - m2 * G * np.sin(t1 - 2 * t2) - 2 * np.sin(d) * m2 * (o2 * o2 * l2 + o1 * o1 * L1 * np.cos(d))) / (L1 * den)
⟦a2|a2⟧ = (2 * np.sin(d) * (o1 * o1 * L1 * (M1 + m2) + G * (M1 + m2) * np.cos(t1) + o2 * o2 * l2 * m2 * np.cos(d))) / (l2 * den)`,
            syms: [
                ['d', 'δ', 'd', 'angle between the rods, rad'],
                ['den', 'D′', 'den', 'shared denominator of (9), kg'],
                ['a1', 'α<sub>1</sub>', 'a1', 'upper angular acceleration, rad/s² (stored)'],
                ['a2', 'α<sub>2</sub>', 'a2', 'lower angular acceleration, rad/s² (stored)'],
                ['m2', 'm<sub>2</sub>', 'm2', 'lower bob mass, kg']
            ]
        },
        {
            title: 'The chaos twin and the distance d(t)',
            where: 'the model (Python, run on Kaggle): one_file(), the twin and its distance',
            math: 'θ′<sub>1</sub>(0) = θ<sub>1</sub>(0) + 0.001 rad, θ′<sub>2</sub>(0) = θ<sub>2</sub>(0), ω′<sub>i</sub>(0) = 0<br>⟦sep|d⟧(t) = |(x<sub>2</sub> − x′<sub>2</sub>, y<sub>2</sub> − y′<sub>2</sub>)| ≈ d<sub>0</sub> e<sup>λt</sup>',
            note: 'Section 6 follows two pendulums whose upper angles start 0.001 rad apart, and the model does exactly that for every stored start: y0 is the start, and tw is the same equations solved from y0 with EPS = 0.001 rad added to θ<sub>1</sub> only. Y and Z are the two runs sampled at the frames; bob2() gives the lower bob of each in metres, by (1), and np.hypot their distance d, in m. The model stores log<sub>10</sub> d for every frame, and the page shows 10 to that power as the Twin separation readout, and the twin’s two angles to draw it. While the motion is chaotic, log<sub>10</sub> d rises roughly along a straight line of slope λ/ln 10; for the default start the model measured λ = 1.38 per second.',
            code: `y0 = [th1, math.radians(th2d), 0.0, 0.0]; s = solve(m2, l2, y0); tw = solve(m2, l2, [th1 + EPS] + y0[1:])
...
x, y = bob2(Y[0], Y[1], l2); xt, yt = bob2(Z[0], Z[1], l2); ⟦sep|d = np.hypot(x - xt, y - yt)⟧`,
            syms: [
                ['sep', 'd', 'd', 'distance between the two lower bobs, m (stored as log<sub>10</sub> d)']
            ]
        },
        {
            title: 'Solving it step by step: DOP853',
            where: 'the model (Python, run on Kaggle): solve()',
            math: 'ds/dt = F(s) = (ω<sub>1</sub>, ω<sub>2</sub>, α<sub>1</sub>, α<sub>2</sub>)<br>each step accepted only if its estimated error ≤ 10<sup>−10</sup> × |s| + 10<sup>−12</sup>; otherwise a shorter step',
            note: '§7 explains why no formula gives the angles at a later time, and how RK4 walks forward in steps of fixed length, which is what this page did until November 2026. The model uses SciPy’s solve_ivp with the method DOP853 (Dormand and Prince, order 8): it looks at the slope twelve times per step, estimates the error of every step, and shortens the step whenever that estimate exceeds the tolerance, relative rtol = 10<sup>−10</sup> plus absolute atol = 10<sup>−12</sup>. rhs_factory(m2, l2) is the function F of §7, with the accelerations of step 7. The solution runs from 0 to T_RUN = 20 s; dense_output keeps a continuous curve between the steps, which the model then samples at the frames, 20 to 100 times a second, more where the motion is fast.',
            code: `def solve(m2, l2, y0, rtol=RTOL, atol=ATOL):
    return solve_ivp(rhs_factory(m2, l2), (0, T_RUN), y0, method="DOP853", rtol=rtol, atol=atol, dense_output=True)`,
            syms: [
                ['fd', 'f', 'h.fps', 'stored frames per second of this file']
            ]
        },
        {
            title: 'Energy drift as the accuracy check',
            where: 'the model (Python, run on Kaggle): one_file(), the energy of every run',
            math: '⟦E0|E<sub>0</sub>⟧ = E at t = 0<br>⟦drift|ε<sub>max</sub>⟧ = max |E − E<sub>0</sub>| / E<sub>scale</sub>, E<sub>scale</sub> = (m<sub>1</sub>+m<sub>2</sub>)g l<sub>1</sub> + m<sub>2</sub>g l<sub>2</sub>',
            note: 'With no friction, (3) and (4) keep E = T + V fixed, so any change in the computed E is the method’s own error (§3, §7). The model computes E at the frames (E) and at every step DOP853 took (Ed), and stores, per run, the starting energy E<sub>0</sub> in J and the largest change divided by E<sub>scale</sub>, the energy needed to lift both bobs from the bottom to the pivot; dividing by E<sub>0</sub> instead would fail, because E<sub>0</sub> can be close to zero. The page shows E<sub>0</sub> as the Energy E readout and ε<sub>max</sub> as the Energy drift readout: for the default start 2.0 × 10<sup>−9</sup>, and never more than 6.2 × 10<sup>−9</sup> over all 1296 stored runs.',
            code: `E = energy(Y, m2, l2); Ed = energy(s.y, m2, l2); S = (M1 + m2) * G * L1 + m2 * G * l2
runs.append(dict(th2_deg=th2d, E0=float(E[0]), S=S, drift_max=float(np.abs(Ed - Ed[0]).max() / S),`,
            syms: [
                ['E0', 'E<sub>0</sub>', 'E0', 'starting energy of the run, J'],
                ['drift', 'ε<sub>max</sub>', 'drift_max', 'largest energy error of the run, relative to E<sub>scale</sub>']
            ]
        },
        {
            title: 'Playing: the clock and the cubic between frames',
            where: 'the page: the Sim.clock callback and anglesAt(t)',
            math: '⟦t|t⟧ ← t + Δt × (time scale), back to 0 after 20 s<br>⟦k|k⟧ = ⌊t f⟧, ⟦u|u⟧ = t f − k<br>⟦d1|θ(t)⟧ = h<sub>00</sub>(u) θ<sub>k</sub> + h<sub>10</sub>(u) ω<sub>k</sub>/f + h<sub>01</sub>(u) θ<sub>k+1</sub> + h<sub>11</sub>(u) ω<sub>k+1</sub>/f',
            note: 'The clock hands the callback dt, the real time since the last picture in seconds (at most 0.05 s), and the page adds dt times the Time scale slider to tau, the time t in the stored run; after the last frame the run starts again from t = 0. anglesAt(t) finds the stored frame k at or before t, f being the file’s frames per second, and u, how far t has gone towards frame k + 1. Between the two frames it draws each angle on a cubic through both stored angles with the stored angular velocities as slopes (Hermite interpolation; h<sub>00</sub> … h<sub>11</sub> are its four standard weights, written out in herm()). Because the stored angles are folded into −π … π, p1 first adds the whole turn that brings θ<sub>k+1</sub> next to θ<sub>k</sub>, guessed from the mean angular velocity. The model checked that the lower bob drawn this way stays within 0.2 % of l<sub>1</sub> + l<sub>2</sub> of its true path. The trail gets one segment for every 1/600 s of the run.',
            code: `var t0 = tau, t1 = ⟦t|tau + dt * speed.value⟧, T = (P.hdr.frames - 1) / P.hdr.fps;
...
var h = P.hdr, f = Math.max(0, t * h.fps), ⟦k|k = Math.min(Math.floor(f), h.frames - 2)⟧, ⟦u|u = f - k⟧, a = frame(k), b = frame(k + 1), dh = 1 / h.fps, out = [0, 0, 0, 0, k, u];
...
var p1 = a[i] + wrapd(b[i] - a[i] - (a[i + 2] + b[i + 2]) / 2 * dh) + (a[i + 2] + b[i + 2]) / 2 * dh;
⟦d1|out[i] = herm(a[i], p1, a[i + 2] * dh, b[i + 2] * dh, u)⟧;`,
            syms: [
                ['t', 't', 'tau', 'time in the stored run, played now, s'],
                ['k', 'k', 'k', 'the stored frame at or before t'],
                ['u', 'u', 'u', 'fraction of the way to frame k + 1'],
                ['d1', 'θ<sub>1</sub> drawn', 'out[0]', 'upper rod angle as drawn, rad'],
                ['d2', 'θ<sub>2</sub> drawn', 'out[1]', 'lower rod angle as drawn, rad']
            ]
        },
        {
            title: 'From metres to pixels',
            where: 'the page: layout(), scale and pivot; pos(a, b), the bobs on screen',
            math: '⟦scale|σ⟧ = (min(W, H)/2 − 34) / (l<sub>1</sub> + l<sub>2</sub>), x<sub>0</sub> = W/2, y<sub>0</sub> = H/2<br>x<sub>1</sub> px = x<sub>0</sub> + σl<sub>1</sub> sin θ<sub>1</sub>, ⟦y1|y<sub>1</sub> px⟧ = y<sub>0</sub> + σl<sub>1</sub> cos θ<sub>1</sub><br>x<sub>2</sub> px = x<sub>1</sub> px + σ⟦l2|l<sub>2</sub>⟧ sin θ<sub>2</sub>, y<sub>2</sub> px = y<sub>1</sub> px + σl<sub>2</sub> cos θ<sub>2</sub>',
            note: 'layout() sets up the picture of §8. box.w and box.h are the width W and height H of the figure in CSS pixels; ox and oy are the pivot at its centre; scale is σ in px/m, chosen so that the fully stretched pendulum ends 34 px short of the nearer edge, room for the protractor’s labels (before a file has arrived, l2 || 1 stands in for l<sub>2</sub>). pos(a, b) turns the two drawn angles of step 11 into four screen coordinates in px, counted from the left and from the top: x1, y1 for bob 1, then bob 2. Screen y points down, so the minus signs of (1) turn into plus signs. These pixel positions are what the rods, the bobs and the trail are drawn from, and the data panel checks that the pixel at each stored bob centre is burgundy.',
            code: `ox = box.w / 2;
oy = box.h / 2;
⟦scale|scale = (Math.min(box.w, box.h) / 2 - 34) / (l1 + (l2 || 1))⟧;
...
var x1 = ox + l1 * scale * Math.sin(a), ⟦y1|y1 = oy + l1 * scale * Math.cos(a)⟧;
return [x1, y1, x1 + ⟦l2|l2⟧ * scale * Math.sin(b), y1 + l2 * scale * Math.cos(b)];`,
            syms: [
                ['scale', 'σ', 'scale', 'pixels per metre, px/m'],
                ['y1', 'y<sub>1</sub> px', 'pos(…)[1]', 'bob 1 as drawn, px from the top'],
                ['l2', 'l<sub>2</sub>', 'l2', 'lower rod length, m (l<sub>1</sub> = 1 m)']
            ]
        },
        {
            title: 'Bob sizes and the fading trail',
            where: 'the page: drawPendulum(p, ghost), the bob radii; the Sim.clock callback, the trail',
            math: 'r<sub>1</sub> = 8 px, r<sub>2</sub> = 8 (⟦m2|m<sub>2</sub>⟧/m<sub>1</sub>)<sup>1/3</sup> px, clamped to 4–17 px<br>trail opacity × (1 − 0.008)<sup>60 Δt</sup> each frame, half-life ln 2 / (60 |ln 0.992|) ≈ 1.4 s',
            note: 'The second paragraph of §8, in code. drawPendulum() gives bob 1 the radius r1 = 8 px and bob 2 the radius r2 = 8 (m<sub>2</sub>/m<sub>1</sub>)<sup>1/3</sup> px, so that its volume grows in proportion to its mass, as for balls of one material; Math.max and Math.min clamp it to 4–17 px. The size is for the eye only: in the model the masses are points. In the clock, anglesAt() gives the drawn angles at every 1/600 s of the run that the picture covers, pos() the lower bob’s position pa, and segment() draws a 1.5 px burgundy line to it from the previous one, on a separate transparent trail canvas. Once per picture, fade() erases the fraction 1 − 0.992<sup>60Δt</sup> of that canvas, with dt = Δt the real frame time in s, so the fading follows real time. The canvas stores opacity in steps of 1/255, the small fading steps round away, and the trail falls to half in about 1.6 s and then stops near a quarter of its opacity, as §8 reports.',
            code: `var r1 = 8, r2 = Math.max(4, Math.min(17, 8 * Math.cbrt(⟦m2|m2⟧ / m1)));
...
var A = anglesAt(t0 + (t1 - t0) * i / n), pa = pos(A[0], A[1]);
segment(prevA, pa, 'rgba(122, 31, 43, 0.85)', 1.5); prevA = pa;
...
fade(1 - Math.pow(1 - 0.008, dt * 60));`,
            syms: [
                ['m2', 'm<sub>2</sub>', 'm2', 'lower bob mass, kg (m<sub>1</sub> = 1 kg)'],
                ['scale', 'σ', 'scale', 'pixels per metre, px/m, used by pos()']
            ]
        }
    ]
};
