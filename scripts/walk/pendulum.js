/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.pendulum = {
    intro: 'Eight steps from the Lagrangian to the dots on the screen. Every formula sits next to the exact lines that compute it, and the table shows what those symbols hold right now in the running pendulum. Hover or tap a symbol to see it in all three places at once.',
    steps: [
        {
            title: 'The state vector',
            where: 'restart() — the initial condition',
            math: '⟦s|<b>s</b>⟧ = (⟦t1|θ<sub>1</sub>⟧, ⟦t2|θ<sub>2</sub>⟧, ⟦o1|ω<sub>1</sub>⟧, ⟦o2|ω<sub>2</sub>⟧)',
            note: 'Two second-order equations become four first-order ones: angles and angular velocities together fix the future completely. Angles are measured from the downward vertical and converted from degrees to radians exactly once, here.',
            code: `⟦s|state⟧ = [⟦t1|th1.value * Math.PI / 180⟧, ⟦t2|th2.value * Math.PI / 180⟧, ⟦o1|w1.value⟧, ⟦o2|w2.value⟧];`,
            syms: [
                ['t1', 'θ<sub>1</sub>', 'state[0]', 'upper rod angle, rad'],
                ['t2', 'θ<sub>2</sub>', 'state[1]', 'lower rod angle, rad'],
                ['o1', 'ω<sub>1</sub>', 'state[2]', 'upper angular velocity, rad/s'],
                ['o2', 'ω<sub>2</sub>', 'state[3]', 'lower angular velocity, rad/s']
            ]
        },
        {
            title: 'Angle difference and the shared denominator',
            where: 'deriv(s) — lines 1–2',
            math: '⟦d|δ⟧ = θ<sub>1</sub> − θ<sub>2</sub><br>⟦den|D′⟧ = 2m<sub>1</sub> + ⟦m2|m<sub>2</sub>⟧ − m<sub>2</sub> cos 2⟦d|δ⟧',
            note: 'D′ is the Cramer determinant D = l<sub>1</sub>l<sub>2</sub>(m<sub>1</sub> + m<sub>2</sub> sin²δ) from the derivation, scaled: D′ = 2D/(l<sub>1</sub>l<sub>2</sub>) = 2(m<sub>1</sub> + m<sub>2</sub> sin²δ), using 2 sin²δ = 1 − cos 2δ. It is never zero; its smallest value is 2m<sub>1</sub>, reached when the rods are aligned (sin δ = 0).',
            code: `var t1 = s[0], t2 = s[1], o1 = s[2], o2 = s[3], ⟦d|d = t1 - t2⟧;
var ⟦den|den = 2 * m1 + m2 - m2 * Math.cos(2 * d)⟧;`,
            syms: [
                ['d', 'δ', 'd', 'θ₁ − θ₂, rad'],
                ['den', 'D′', 'den', 'shared denominator = 2(m₁ + m₂ sin²δ), kg'],
                ['m2', 'm<sub>2</sub>', 'm2', 'lower bob mass (m₁ = 1 kg)']
            ]
        },
        {
            title: 'Upper angular acceleration α₁',
            where: 'deriv(s) — the a1 line',
            math: '⟦a1|α<sub>1</sub>⟧ = [ −g(2m<sub>1</sub>+m<sub>2</sub>) sin θ<sub>1</sub> − m<sub>2</sub>g sin(θ<sub>1</sub>−2θ<sub>2</sub>) − 2 sin δ · m<sub>2</sub>(⟦o2|ω<sub>2</sub>⟧²l<sub>2</sub> + ⟦o1|ω<sub>1</sub>⟧²l<sub>1</sub> cos δ) ] / (l<sub>1</sub>⟦den|D′⟧)',
            note: 'This is Cramer’s rule on (E1)–(E2) in the derivation, after the two trigonometric identities. The terms in order: the gravity torque on the whole chain, the gravity pull the lower bob passes through the joint, and the centrifugal coupling through ω². Each term in the formula is one term in the code, in the same order.',
            code: `var ⟦a1|a1⟧ = (-g * (2 * m1 + m2) * Math.sin(t1) - m2 * g * Math.sin(t1 - 2 * t2)
    - 2 * Math.sin(d) * m2 * (⟦o2|o2 * o2⟧ * l2 + ⟦o1|o1 * o1⟧ * l1 * Math.cos(d))) / (l1 * ⟦den|den⟧);`,
            syms: [
                ['a1', 'α<sub>1</sub>', 'a1', 'upper angular acceleration, rad/s²'],
                ['o1', 'ω<sub>1</sub>', 'o1', 'rad/s'],
                ['o2', 'ω<sub>2</sub>', 'o2', 'rad/s'],
                ['den', 'D′', 'den', 'kg']
            ]
        },
        {
            title: 'Lower angular acceleration α₂',
            where: 'deriv(s) — the a2 line and the return',
            math: '⟦a2|α<sub>2</sub>⟧ = 2 sin δ [ ⟦o1|ω<sub>1</sub>⟧²l<sub>1</sub>(m<sub>1</sub>+m<sub>2</sub>) + g(m<sub>1</sub>+m<sub>2</sub>) cos θ<sub>1</sub> + ⟦o2|ω<sub>2</sub>⟧²l<sub>2</sub>m<sub>2</sub> cos δ ] / (l<sub>2</sub>⟦den|D′⟧)<br>d<b>s</b>/dt = (ω<sub>1</sub>, ω<sub>2</sub>, α<sub>1</sub>, α<sub>2</sub>)',
            note: 'The whole right-hand side of the ODE is this one returned array: the first two slots say "angles change at the angular velocities", the last two are the accelerations just computed.',
            code: `var ⟦a2|a2⟧ = (2 * Math.sin(d) * (⟦o1|o1 * o1⟧ * l1 * (m1 + m2) + g * (m1 + m2) * Math.cos(t1)
    + ⟦o2|o2 * o2⟧ * l2 * m2 * Math.cos(d))) / (l2 * ⟦den|den⟧);
return [o1, o2, ⟦a1|a1⟧, ⟦a2|a2⟧];`,
            syms: [
                ['a1', 'α<sub>1</sub>', 'a1', 'rad/s²'],
                ['a2', 'α<sub>2</sub>', 'a2', 'lower angular acceleration, rad/s²'],
                ['den', 'D′', 'den', 'kg']
            ]
        },
        {
            title: 'One Runge–Kutta 4 step',
            where: 'rk4(s, h)',
            math: '⟦k1|k<sub>1</sub>⟧ = f(<b>s</b>), ⟦k2|k<sub>2</sub>⟧ = f(<b>s</b> + ½h k<sub>1</sub>)<br>⟦k3|k<sub>3</sub>⟧ = f(<b>s</b> + ½h k<sub>2</sub>), ⟦k4|k<sub>4</sub>⟧ = f(<b>s</b> + h k<sub>3</sub>)<br><b>s</b><sub>n+1</sub> = <b>s</b><sub>n</sub> + ⟦h|h⟧/6 (k<sub>1</sub> + 2k<sub>2</sub> + 2k<sub>3</sub> + k<sub>4</sub>)',
            note: 'Four slope samples across the interval, weighted 1 : 2 : 2 : 1 like Simpson’s rule. The local error is O(h⁵) and the global error O(h⁴), so halving h cuts the error by about 16. All four slopes of one stage use the same input state: updating θ₁ before computing α₂ would silently turn RK4 into a different, less accurate method, which is why rk4() builds separate trial arrays s2, s3 and s4.',
            code: `var ⟦k1|k1 = deriv(s)⟧, i, s2 = [], s3 = [], s4 = [], out = [];
for (i = 0; i < 4; i++) s2[i] = s[i] + h / 2 * k1[i];
var ⟦k2|k2 = deriv(s2)⟧;
for (i = 0; i < 4; i++) s3[i] = s[i] + h / 2 * k2[i];
var ⟦k3|k3 = deriv(s3)⟧;
for (i = 0; i < 4; i++) s4[i] = s[i] + ⟦h|h⟧ * k3[i];
var ⟦k4|k4 = deriv(s4)⟧;
for (i = 0; i < 4; i++) out[i] = s[i] + ⟦h|h / 6⟧ * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);`,
            syms: [
                ['k1', 'k<sub>1</sub>', 'deriv(s)', 'slope at the start: (ω₁, ω₂, α₁, α₂)'],
                ['h', 'h', 'H', 'time step, s']
            ]
        },
        {
            title: 'How many steps per frame',
            where: 'Sim.clock callback',
            math: '⟦acc|τ⟧ ← τ + Δt · speed<br>⟦n|n⟧ = min(⌊τ / h⌋, 600), τ ← τ − n h',
            note: 'The screen refreshes at an uneven Δt (about 1/60 s); physics advances in equal steps h = 1/600 s. The leftover τ carries into the next frame, so on an ordinary screen simulated time keeps pace with wall time × speed. Two safety caps make it fall behind rather than freeze on a slow device: one frame counts at most 0.05 s, and at most 600 steps run per frame, after which the leftover is cut to one step. A fixed h keeps the integrator’s accuracy the same on every device.',
            code: `⟦acc|acc += dt * speed.value⟧;
var ⟦n|n = Math.min(Math.floor(acc / H), 600)⟧;
acc = Math.min(acc - n * H, H);
for (var i = 0; i < n; i++) {
    state = rk4(state, ⟦h|H⟧);
    ...
    simT += H;
}`,
            syms: [
                ['h', 'h', 'H', 's'],
                ['n', 'n', 'n', 'RK4 steps in the last frame'],
                ['acc', 'τ', 'acc', 'unspent time carried over, s'],
                ['t', 't', 'simT', 'simulated time, s']
            ]
        },
        {
            title: 'Energy as the accuracy check',
            where: 'energy(s) and readouts()',
            math: '⟦kin|T⟧ = ½(m<sub>1</sub>+m<sub>2</sub>)l<sub>1</sub>²ω<sub>1</sub>² + ½m<sub>2</sub>l<sub>2</sub>²ω<sub>2</sub>² + m<sub>2</sub>l<sub>1</sub>l<sub>2</sub>ω<sub>1</sub>ω<sub>2</sub> cos δ<br>⟦pot|V⟧ = −(m<sub>1</sub>+m<sub>2</sub>)g l<sub>1</sub> cos θ<sub>1</sub> − m<sub>2</sub>g l<sub>2</sub> cos θ<sub>2</sub><br>⟦drift|ε⟧ = (⟦E|E⟧ − E<sub>0</sub>) / [(m<sub>1</sub>+m<sub>2</sub>)g l<sub>1</sub> + m<sub>2</sub>g l<sub>2</sub>]',
            note: 'The exact motion conserves E = T + V, so any change is pure numerical error. It is divided by the depth of the potential well, not by E₀, because E₀ can be zero and the ratio would blow up.',
            code: `var ⟦kin|kin⟧ = 0.5 * (m1 + m2) * l1 * l1 * s[2] * s[2] + 0.5 * m2 * l2 * l2 * s[3] * s[3]
    + m2 * l1 * l2 * s[2] * s[3] * Math.cos(s[0] - s[1]);
var ⟦pot|pot⟧ = -(m1 + m2) * g * l1 * Math.cos(s[0]) - m2 * g * l2 * Math.cos(s[1]);
return kin + pot;
...
var ⟦drift|drift⟧ = (⟦E|E⟧ - E0) / ((m1 + m2) * g * l1 + m2 * g * l2);`,
            syms: [
                ['kin', 'T', 'kin', 'kinetic energy, J'],
                ['pot', 'V', 'pot', 'potential energy, J'],
                ['E', 'E', 'energy(state)', 'total, J'],
                ['E0', 'E<sub>0</sub>', 'E0', 'total at restart, J'],
                ['drift', 'ε', 'drift', 'relative error, dimensionless']
            ]
        },
        {
            title: 'From angles to pixels',
            where: 'layout() and pos(s)',
            math: '⟦scale|σ⟧ = (min(W, H)/2 − 34) / (l<sub>1</sub> + l<sub>2</sub>)<br>x<sub>1</sub> = o<sub>x</sub> + σ l<sub>1</sub> sin θ<sub>1</sub>, ⟦y1|y<sub>1</sub>⟧ = o<sub>y</sub> + σ l<sub>1</sub> cos θ<sub>1</sub><br>x<sub>2</sub> = x<sub>1</sub> + σ l<sub>2</sub> sin θ<sub>2</sub>, y<sub>2</sub> = y<sub>1</sub> + σ l<sub>2</sub> cos θ<sub>2</sub>',
            note: 'Screen y grows downward, so “+ cos θ” puts a hanging bob below the pivot with no sign flip. σ is in pixels per metre and is chosen so the fully stretched pendulum just fits, with 34 px left for the degree labels.',
            code: `⟦scale|scale = (Math.min(box.w, box.h) / 2 - 34) / (l1 + l2)⟧;
...
var x1 = ox + l1 * scale * Math.sin(s[0]), ⟦y1|y1 = oy + l1 * scale * Math.cos(s[0])⟧;
return [x1, y1, x1 + l2 * scale * Math.sin(s[1]), y1 + l2 * scale * Math.cos(s[1])];`,
            syms: [
                ['scale', 'σ', 'scale', 'pixels per metre'],
                ['y1', 'y<sub>1</sub>', 'pos(state)[1]', 'upper bob, px from top'],
                ['l2', 'l<sub>2</sub>', 'l2', 'lower rod, m (l₁ = 1 m)']
            ]
        }
    ]
};
