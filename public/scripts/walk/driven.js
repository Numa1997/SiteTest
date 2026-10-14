/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.driven = {
    intro: 'Seven steps from the sliders to the block on screen. The run is solved once and stored; the live column shows the stored sample on screen now.',
    steps: [
        {
            title: 'From the sliders to k, c and Ω',
            where: 'solve(), first line',
            math: '⟦w0|ω<sub>0</sub>⟧ = 2π f<sub>0</sub>, &nbsp; ⟦k|k⟧ = m ω<sub>0</sub>², &nbsp; ⟦c|c⟧ = 2ζ m ω<sub>0</sub>, &nbsp; ⟦W|Ω⟧ = 2π f',
            note: 'The sliders speak the language of the experiment (how fast it rings, how quickly it dies away); the equation of motion needs a stiffness and a friction coefficient. With m = 1 kg the two languages differ only by factors of 2π.',
            code: `var ⟦w0|w0 = 2 * Math.PI * f0.value⟧, p = { ⟦k|k: M * w0 * w0⟧, ⟦c|c: 2 * zeta.value * M * w0⟧, ⟦W|W: 2 * Math.PI * fd.value⟧, F0: F0.value };`,
            syms: [
                ['w0', 'ω<sub>0</sub>', 'w0', 'rad/s'],
                ['k', 'k', 'p.k', 'N/m'],
                ['c', 'c', 'p.c', 'kg/s'],
                ['W', 'Ω', 'p.W', 'rad/s']
            ]
        },
        {
            title: 'Newton’s second law, solved for the acceleration',
            where: 'accel()',
            math: 'm ẍ = F<sub>0</sub> cos Ωt − c ẋ − k x &nbsp;⇒&nbsp; ẍ = (F<sub>0</sub> cos Ωt − c v − k x) / m',
            note: 'Three forces act on the block: the driver, the damper and the spring. The time t appears explicitly: this is what makes the system driven rather than free.',
            code: `function accel(t, x, v, p) {
return (p.F0 * Math.cos(p.W * t) - p.c * v - p.k * x) / M;
}`,
            syms: [
                ['k', 'k', 'p.k', 'N/m'],
                ['c', 'c', 'p.c', 'kg/s'],
                ['W', 'Ω', 'p.W', 'rad/s']
            ]
        },
        {
            title: 'One Runge–Kutta step',
            where: 'solve(), inside the loop',
            math: 'k₁ = f(t, s), k₂ = f(t + h/2, s + h k₁/2), k₃ = f(t + h/2, s + h k₂/2), k₄ = f(t + h, s + h k₃)<br>s(t + ⟦h|h⟧) = s + (h/6)(k₁ + 2k₂ + 2k₃ + k₄), &nbsp; s = (x, v)',
            note: 'The state is the pair (x, v); its slope is (v, a). The slope is sampled four times per step, at the start, twice in the middle and at the end. With the default settings the largest error over the 60 s run is about 5 × 10⁻¹² m: see “RK4 vs exact”.',
            code: `var a1 = accel(t, x, v, p), x2 = x + 0.5 * H * v, v2 = v + 0.5 * H * a1;
var a2 = accel(t + 0.5 * H, x2, v2, p), x3 = x + 0.5 * H * v2, v3 = v + 0.5 * H * a2;
var a3 = accel(t + 0.5 * H, x3, v3, p), x4 = x + H * v3, v4 = v + H * a3;
var a4 = accel(t + H, x4, v4, p);
...
x += H / 6 * (v + 2 * v2 + 2 * v3 + v4);
v += H / 6 * (a1 + 2 * a2 + 2 * a3 + a4);`,
            syms: [
                ['h', 'h', 'H', 's'],
                ['steps', 'steps', 'TEND / H', 'per solve']
            ]
        },
        {
            title: 'Store every tenth state',
            where: 'solve(), top of the loop',
            math: '⟦n|n⟧ = step / 10, &nbsp; ⟦t|t<sub>n</sub>⟧ = n · 10h<br>⟦F|F<sub>n</sub>⟧ = F<sub>0</sub> cos Ωt<sub>n</sub>, &nbsp; ⟦E|E<sub>n</sub>⟧ = ½ m v<sub>n</sub>² + ½ k x<sub>n</sub>²',
            note: 'The integrator takes 60 000 steps, but a sample every 10 ms is plenty for drawing: 6 001 rows of the table, each written at the moment the state is known. The animation never computes a state of its own.',
            code: `if (step % EVERY === 0) {
ts[n] = t; xs[n] = x; vs[n] = v; Fs[n] = p.F0 * Math.cos(p.W * t);
Es[n] = 0.5 * M * v * v + 0.5 * p.k * x * x; Pin[n] = Fs[n] * v; Ploss[n] = p.c * v * v;
n++;
}`,
            syms: [
                ['n', 'n', 'n', 'sample on screen'],
                ['t', 't<sub>n</sub>', 'ts[n]', 's'],
                ['x', 'x<sub>n</sub>', 'xs[n]', 'm'],
                ['v', 'v<sub>n</sub>', 'vs[n]', 'm/s'],
                ['F', 'F<sub>n</sub>', 'Fs[n]', 'N'],
                ['E', 'E<sub>n</sub>', 'Es[n]', 'J']
            ]
        },
        {
            title: 'Energy bookkeeping',
            where: 'solve(), inside the loop and after it',
            math: '⟦Win|W<sub>in</sub>⟧ = ∫ F v dt, &nbsp; ⟦Wloss|W<sub>loss</sub>⟧ = ∫ c v² dt<br>E(T) − E(0) = W<sub>in</sub> − W<sub>loss</sub> &nbsp; (⟦bal|balance⟧)',
            note: 'The two integrals ride along in the same Runge–Kutta step as x and v. The work–energy theorem then becomes a test of the whole computation: the energy gained must equal the work put in minus the heat made.',
            code: `win += H / 6 * (Fa * v + 2 * Fm * v2 + 2 * Fm * v3 + Fb * v4);
wloss += H / 6 * p.c * (v * v + 2 * v2 * v2 + 2 * v3 * v3 + v4 * v4);
...
ds.set('balance', win > 0 ? Math.abs(Es[NS - 1] - Es[0] - (win - wloss)) / win : 0);`,
            syms: [
                ['Win', 'W<sub>in</sub>', 'win', 'J over the run'],
                ['Wloss', 'W<sub>loss</sub>', 'wloss', 'J over the run'],
                ['bal', 'balance', '', 'relative error']
            ]
        },
        {
            title: 'The exact answer, to measure the error',
            where: 'steady() and solve()',
            math: '⟦X|X⟧ = (F<sub>0</sub>/m) / √((ω<sub>0</sub>² − Ω²)² + (2ζω<sub>0</sub>Ω)²), &nbsp; ⟦phi|φ⟧ = atan2(2ζω<sub>0</sub>Ω, ω<sub>0</sub>² − Ω²)<br>⟦err|error⟧ = max<sub>n</sub> |x<sub>n</sub> − x<sub>exact</sub>(t<sub>n</sub>)|',
            note: 'This equation can also be solved with pencil and paper: a steady oscillation at the driver’s frequency plus a dying free oscillation. The page uses the exact solution only to grade the numerical one, never to draw.',
            code: `var X = (F / M) / Math.sqrt(Math.pow(w0 * w0 - W * W, 2) + Math.pow(2 * z * w0 * W, 2));
return { X: X, phi: Math.atan2(2 * z * w0 * W, w0 * w0 - W * W) };
...
err = Math.max(err, Math.abs(xs[n] - xex[n]));`,
            syms: [
                ['X', 'X', 'st.X', 'steady amplitude, m'],
                ['phi', 'φ', 'st.phi', 'phase lag'],
                ['err', 'error', 'err', 'largest over the run']
            ]
        },
        {
            title: 'Playback picks a stored sample',
            where: 'the clock, frame() and draw()',
            math: 't<sub>play</sub> ← t<sub>play</sub> + speed · Δt, &nbsp; ⟦n|n⟧ = round(t<sub>play</sub> / 10h)<br>⟦bx|x<sub>block</sub>⟧ = x<sub>eq</sub> + ⟦x|x<sub>n</sub>⟧ · ⟦sc|px/m⟧',
            note: 'Each frame rounds the playback time to the nearest stored sample and draws that sample as it is, without interpolation. Moving the “Stored run” slider jumps to any sample; the motion is already known everywhere.',
            code: `playT += speed.value * dt;
...
var i = Math.min(NS - 1, Math.max(0, Math.round(playT / (EVERY * H))));
...
var bx = m.eqX + xs[i] * m.sc;`,
            syms: [
                ['n', 'n', 'i', 'sample on screen'],
                ['x', 'x<sub>n</sub>', 'xs[i]', 'm'],
                ['sc', 'px/m', 'sc', 'drawing scale'],
                ['bx', 'x<sub>block</sub>', 'bx', 'css px']
            ]
        }
    ]
};
