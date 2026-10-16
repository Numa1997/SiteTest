/* From symbols to code — one file per simulation, loaded by sim.js from the page's data-walk key.
   Each step pairs an equation with the lines of this site's code that compute it.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live(), which each page defines next to its own state. */
window.WALK = window.WALK || {};

window.WALK.turbine = {
    intro: 'Seven steps from the wind to the blades on screen. Two minutes are solved once and stored; the live column shows the stored sample on screen now.',
    steps: [
        {
            title: 'How much of the wind the blades catch',
            where: 'cp()',
            math: '⟦cp|c<sub>p</sub>⟧(⟦lam|λ⟧) = c₁ (c₂/λ<sub>i</sub> − c₄) e<sup>−c₅/λ<sub>i</sub></sup> + c₆ λ, &nbsp; 1/λ<sub>i</sub> = 1/λ − 0.035<br>c₁…c₆ = 0.5176, 116, 5, 21, 0.0068 &nbsp; (blades at zero pitch)',
            note: 'An empirical fit to measured rotor curves (Heier). It peaks at λ<sub>opt</sub> = 8.1 with c<sub>p,max</sub> = 0.48, below the Betz limit 16/27 that no rotor can beat. The page clips it at zero, where the fit stops being physical.',
            code: `function cp(lam) {
if (lam <= 0.05) return 0;
var inv = 1 / lam - 0.035;
if (inv <= 0) return 0;
var li = 1 / inv;
return Math.max(0, C1 * (C2 / li - C4) * Math.exp(-C5 / li) + C6 * lam);
}`,
            syms: [
                ['lam', 'λ', 'w * R / v', 'tip speed / wind speed'],
                ['cp', 'c<sub>p</sub>', 'cp(lam)', 'share of the wind’s power'],
                ['lopt', 'λ<sub>opt</sub>', 'from optimum()', 'best ratio'],
                ['cpmax', 'c<sub>p,max</sub>', 'from optimum()', 'best share']
            ]
        },
        {
            title: 'The torque of the wind',
            where: 'tauAero()',
            math: 'P<sub>aero</sub> = ½ ρ A v³ c<sub>p</sub>(λ), &nbsp; ⟦ta|τ<sub>aero</sub>⟧ = P<sub>aero</sub> / ⟦w|ω⟧',
            note: '½ρAv³ is the kinetic energy that the air carries through the rotor disc each second. The blades turn a share c<sub>p</sub> of it into shaft power, and power divided by angular speed is torque.',
            code: `function tauAero(w, v) {
return w > 1e-6 ? 0.5 * RHO * AREA * v * v * v * cp(w * R / v) / w : 0;
}`,
            syms: [
                ['v', 'v', 'wind(t, c)', 'm/s'],
                ['w', 'ω', 'w', 'rad/s'],
                ['ta', 'τ<sub>aero</sub>', 'tauAero(w, v)', 'N m']
            ]
        },
        {
            title: 'The controller sets the generator torque',
            where: 'tauGen()',
            math: 'follow the wind: ⟦tg|τ<sub>gen</sub>⟧ = ⟦Kopt|K<sub>opt</sub>⟧ ω², &nbsp; K<sub>opt</sub> = ½ ρ π R⁵ c<sub>p,max</sub> / λ<sub>opt</sub>³<br>hold speed: τ<sub>gen</sub> = τ<sub>0</sub> + ⟦Kp|K<sub>p</sub>⟧(ω − ⟦wref|ω<sub>ref</sub>⟧) + ⟦Ki|K<sub>i</sub>⟧ ∫(ω − ω<sub>ref</sub>) dt',
            note: 'The generator is the only handle the controller has. Braking with K<sub>opt</sub>ω² balances the wind exactly when λ = λ<sub>opt</sub>, so the rotor settles at the best tip-speed ratio for any wind. The PI law instead brakes harder when the rotor is too fast and less when too slow, and its integral removes any lasting error. The torque is clipped to 0 … 1.2 MN m.',
            code: `function tauGen(w, I, c) {
if (c.ctrl === 'opt') return Math.min(TMAX, ds.get('K_opt') * w * w);
return Math.min(TMAX, Math.max(0, c.tau0 + c.Kp * (w - c.wref) + c.Ki * I));
}`,
            syms: [
                ['tg', 'τ<sub>gen</sub>', 'tauGen(w, I, c)', 'N m'],
                ['Kopt', 'K<sub>opt</sub>', "ds.get('K_opt')", 'N m s²'],
                ['wref', 'ω<sub>ref</sub>', 'c.wref', 'rad/s'],
                ['Kp', 'K<sub>p</sub>', 'c.Kp', 'N m s'],
                ['Ki', 'K<sub>i</sub>', 'c.Ki', 'N m']
            ]
        },
        {
            title: 'Tuning the PI controller',
            where: 'solve(), before the loop',
            math: 'J δω̈ + (K<sub>p</sub> − ⟦dtd|∂τ<sub>aero</sub>/∂ω⟧) δω̇ + K<sub>i</sub> δω = 0 &nbsp;≡&nbsp; δω̈ + 2ζ<sub>c</sub>ω<sub>n</sub> δω̇ + ω<sub>n</sub>² δω = 0<br>K<sub>i</sub> = J ω<sub>n</sub>², &nbsp; K<sub>p</sub> = 2ζ<sub>c</sub>ω<sub>n</sub>J + ∂τ<sub>aero</sub>/∂ω, &nbsp; ω<sub>n</sub> = 0.6 rad/s, ζ<sub>c</sub> = 0.8',
            note: 'Near the target speed a small speed error δω obeys a damped-oscillator equation, the same one as in Fig. 9. The gains are chosen so that it has a natural frequency of 0.6 rad/s and a damping ratio of 0.8: an error dies within a few seconds, without ringing.',
            code: `var dtd = (tauAero(c.wref + 1e-4, c.v0) - tauAero(c.wref - 1e-4, c.v0)) / 2e-4;
c.Kp = 2 * ZC * WN * J + dtd; c.Ki = J * WN * WN;`,
            syms: [
                ['dtd', '∂τ<sub>aero</sub>/∂ω', 'dtd', 'N m s, from a central difference'],
                ['Kp', 'K<sub>p</sub>', 'c.Kp', 'N m s'],
                ['Ki', 'K<sub>i</sub>', 'c.Ki', 'N m']
            ]
        },
        {
            title: 'Newton’s law for a rotation, stepped with RK4',
            where: 'rates() and solve()',
            math: 'J dω/dt = τ<sub>aero</sub> − τ<sub>gen</sub>, &nbsp; dI/dt = ω − ω<sub>ref</sub><br>carried along: dE<sub>gen</sub>/dt = τ<sub>gen</sub>ω, dE<sub>aero</sub>/dt = τ<sub>aero</sub>ω, ds<sub>air</sub>/dt = v, dθ/dt = ω',
            note: 'Two torques act on the rotor; their difference speeds it up or slows it down. The integral I stops growing while the torque is clipped (anti-windup). Energies, the distance the air has moved and the rotor angle are integrated in the same RK4 steps, so the energy balance is a test of the whole computation.',
            code: `return [(a - g) / J, dI, g * w, a * w, 0.5 * RHO * AREA * v * v * v, v, w];
...
var k1 = rates(t, w, I, c);
var k2 = rates(t + H / 2, w + H / 2 * k1[0], I + H / 2 * k1[1], c);
var k3 = rates(t + H / 2, w + H / 2 * k2[0], I + H / 2 * k2[1], c);
var k4 = rates(t + H, w + H * k3[0], I + H * k3[1], c);
w += H / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]);`,
            syms: [
                ['w', 'ω', 'w', 'rad/s'],
                ['ta', 'τ<sub>aero</sub>', 'a', 'N m'],
                ['tg', 'τ<sub>gen</sub>', 'g', 'N m'],
                ['Eg', 'E<sub>gen</sub>', 'y[0]', 'energy so far'],
                ['bal', 'balance', '', 'relative error of E<sub>aero</sub> = E<sub>gen</sub> + ΔE<sub>rot</sub>']
            ]
        },
        {
            title: 'Store every second state',
            where: 'solve(), top of the loop',
            math: '⟦n|n⟧ = step / 2, &nbsp; ⟦t|t<sub>n</sub>⟧ = n · 2h, &nbsp; ⟦Pg|P<sub>gen</sub>⟧ = τ<sub>gen</sub> ω',
            note: 'The integrator takes 12 000 steps of 10 ms; every second state is written into the dataset, 6 001 rows that hold everything the picture needs, including the rotor angle θ and the air travel s<sub>air</sub>.',
            code: `ts[n] = t; vw[n] = v; om[n] = w; rp[n] = w * 60 / (2 * Math.PI); th[n] = y[4]; lam[n] = w * R / v; cpv[n] = cp(lam[n]);
ta[n] = tauAero(w, v); tg[n] = tauGen(w, I, c); Pg[n] = tg[n] * w; Pa[n] = ta[n] * w; Eg[n] = y[0]; sw[n] = y[3]; Ic[n] = I; vt[n] = w * R;`,
            syms: [
                ['n', 'n', 'n', 'sample on screen'],
                ['t', 't<sub>n</sub>', 'ts[n]', 's'],
                ['Pg', 'P<sub>gen</sub>', 'Pg[n]', 'W'],
                ['th', 'θ', 'th[n]', 'rad']
            ]
        },
        {
            title: 'Playback draws a stored sample',
            where: 'frame() and draw()',
            math: 'n = round(t<sub>play</sub> / 2h); &nbsp; blade b at angle ⟦th|θ<sub>n</sub>⟧ + 2πb/3',
            note: 'The blades turn because the stored angle θ changes from row to row, not because the page integrates anything while you watch. The dashes of the air move with the stored air travel, 5 px per metre of air.',
            code: `var i = Math.min(NS - 1, Math.max(0, Math.round(playT / (EVERY * H))));
...
bladePath(c, g, th + b * 2 * Math.PI / 3);`,
            syms: [
                ['n', 'n', 'i', 'sample on screen'],
                ['th', 'θ<sub>n</sub>', 'th', 'rad']
            ]
        }
    ]
};
