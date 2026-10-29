# Fig. 2 · derivation and number check

Page: `public/simulations/Double Pendulum.html`, the note between `<article class="paper" id="paper">` and `</article>`, as committed at
`effcec1` (the working file equals HEAD; the page code is unchanged since `468c139`, only the note text moved). Checked by the
derivation-checker, independently: `notes/fig02/plan.md` and the other files in `notes/fig02/` were not opened.

How it was checked
- Algebra: SymPy 1.14. Every numbered equation re-derived from the Lagrangian; equalities proved exactly (trigonometric numerators
  rewritten in exponentials and simplified to 0), not only sampled.
- Numbers: `deriv()`, `rk4()`, `energy()` and the constants line are cut out of the page source verbatim and run in Node 22, and the same
  runs repeated in headless Chromium 1194 inside the built page (`OUT_DIR=/tmp/fig02-check-dist npm run build`, built file
  byte-identical to the source page), with `requestAnimationFrame` replaced by a driven clock so that frames arrive at chosen times. Store
  values read with `Sim.data.ds.get(...)`, readouts from the DOM, pixels with `getImageData` (alpha checked before colour).
- Links: `curl -L` through the session proxy (all three answered 200). Chapter numbers: Firecrawl search and scrape (roads named per row).
- Scripts and outputs: `/tmp/claude-0/-home-user/7e6e5ff1-31fb-553b-b515-5cc83cb8412c/scratchpad/f2/` (`derive.py`, `derive2.py`,
  `el.py`, `page.cjs`, `numbers.cjs`, `numbers2.cjs`, `bursts.cjs`, `horizon.cjs`, `browser.cjs`, `browser2.cjs`, `render.cjs`,
  `trail-60s.png`).

Default start throughout: θ₁ = 120°, θ₂ = 150°, ω₁ = ω₂ = 0, m₂/m₁ = l₂/l₁ = 1, so E₀ = 18.3057 J and E_scale = 29.43 J.

## Equations

| # | Equation (section) | Verdict | Evidence |
|---|---|---|---|
| E1 | (1) positions, §2 | verified | SymPy: \|r₁\| = l₁, \|r₂ − r₁\| = l₂; θ = 0 hangs straight down; θ > 0 puts the bob at +x, i.e. counter-clockwise from the downward vertical as Fig. 1 says. Units m. |
| E2 | (2) velocities, §3 | verified | Time derivatives of (1), exact. Units m/s. |
| E3 | (3) kinetic energy, §3 | verified | ½m₁v₁² + ½m₂v₂² from (2) equals (3) exactly. The §3 limits also hold: θ₁ = θ₂ gives v₂² = (l₁ω₁ + l₂ω₂)²; rods at right angles give v₂² = l₁²ω₁² + l₂²ω₂². Units J. |
| E4 | (4) potential energy, §3 | verified | m g y with y up, zero at the pivot. Lowest value −E_scale at θ₁ = θ₂ = 0. |
| E5 | (5) Euler–Lagrange, §4.1 (now set with `gathered`) | verified | Same content as before the reflow. Cross-check: SymPy `euler_equations(L)` returns exactly −l₁·(6) and −m₂l₂·(7). |
| E6 | p₁ = ∂L/∂ω₁ (§4.1), ∂L/∂ω₂ (§4.3), the three lines of §4.2, d(cos δ)/dt = −sin δ (ω₁ − ω₂) | verified | Each line exact in SymPy; the ω₁ω₂ coefficient of both Euler–Lagrange expressions is 0, as the text says. |
| E7 | (6), §4.2 (now on two lines) | verified | Equals (Euler–Lagrange for θ₁)/l₁ exactly. Units kg·m/s² on every term. |
| E8 | (7), §4.3 | verified | Equals (Euler–Lagrange for θ₂)/(m₂l₂) exactly. Units m/s². |
| E9 | (8) linear system and det = l₁l₂(m₁ + m₂ sin²δ) > 0, §4.4 (reflowed) | verified | Rows of (8) are (6) and (7); determinant exact; positive because m₁ > 0. |
| E10 | The three identities of §4.4: 2 sin²δ = 1 − cos 2δ; 2 sin θ₂ cos δ = sin θ₁ − sin(θ₁ − 2θ₂); sin θ₁ cos δ − sin θ₂ = cos θ₁ sin δ | verified | All exact. With the third one the Cramer numerator for α₂ becomes l₁ sin δ [(m₁+m₂)l₁ω₁² + (m₁+m₂)g cos θ₁ + m₂l₂ω₂² cos δ], proved exactly: this is the common factor sin δ the text names. |
| E11 | (9) α₁, α₂, §4.4 (α₂ now on two lines) | verified | Cramer's rule on (8) equals (9) exactly, both components. (9) equals the page's `deriv()` symbol for symbol. dE/dt = 0 exactly along (9). Units: every numerator term kg·m/s², denominator kg·m, so 1/s². Limits: m₂ → 0 gives α₁ → −(g/l₁) sin θ₁ (single pendulum) and α₂ → equation (7) for a test mass on a moving pivot; m₁ → ∞ gives the same pair. |
| E12 | eqnote: (9) agrees with a direct numerical solve of (8) to rounding error | verified | 10 000 random states (angles in ±π, ω in ±10 rad/s, m₂ and l₂ over the slider ranges), page `deriv()` against Gaussian elimination on (8): worst norm-wise relative difference 2.1 × 10⁻¹⁴, worst single component 7.7 × 10⁻¹³ (3.7 × 10⁻¹³ leaving out components below 10⁻³ of the vector). Rounding level. |
| E13 | eqnote figure "worst relative difference 8 × 10⁻¹⁴" | unverifiable, because | the sampling ranges and the measure of difference are not stated; my run brackets it (2.1 × 10⁻¹⁴ norm-wise, 7.7 × 10⁻¹³ component-wise), so the conclusion holds but the figure itself cannot be reproduced. |
| E14 | (10) small-angle equations, §5 | verified | First-order expansion of (6) and (7) at m₁ = m₂, l₁ = l₂ = l gives the two rows of (10) exactly (row 1 after dividing by m l, row 2 after dividing by l). |
| E15 | §5 bracket [ (g/l)diag(2,1) − ω²((2,1),(1,1)) ] u = 0 and 2(g/l − ω²)² = ω⁴ (new text) | verified | Determinant of the bracket minus (2(g/l − ω²)² − ω⁴) simplifies to 0. |
| E16 | (11) ω∓² = (2 ∓ √2) g/l; ω₋ = 2.40, ω₊ = 5.79 rad/s | verified | Roots exact; numerically 2.3972 and 5.7874 rad/s at g = 9.81, l = 1 m. |
| E17 | §5 u₂/u₁ = 2(g/l − ω²)/ω² = ±√2; "about 1.4 times as far"; ω₊/ω₋ irrational | verified | Row 1 and row 2 of the bracket give the same ratio, +√2 (slow) and −√2 (fast); √2 = 1.414; ω₊/ω₋ = 1 + √2 = 2.4142, irrational. |
| E18 | (12) largest Lyapunov exponent, §6 | verified | Standard definition, limits in the right order (d₀ → 0 inside, t → ∞ outside); units 1/s. Limit check with the page's code: regular start 10°, 10° gives 0.0055 /s over 500 s and 0.0023 /s over 2000 s, falling towards 0; chaotic default start 1.455 /s (N18). |
| E19 | (13) RK4, §7 (reflowed to three lines) | verified | Line by line equal to `rk4()`: s₂ = s + h/2·k₁, s₃ = s + h/2·k₂, s₄ = s + h·k₃, out = s + h/6·(k₁ + 2k₂ + 2k₃ + k₄); F(s) = (ω₁, ω₂, α₁, α₂) is what `deriv()` returns. |
| E20 | §7 "one-step error like h⁵, accumulated like h⁴: halving the step makes it sixteen times more accurate" | verified | Page code against a reference at h/32: one-step error ratio on halving 31.98, 31.99; error after 10 s from 10°, 10°: ratios 16.7, 16.3, 16.2 (h = 1/150 … 1/1200); after 1 s from the default start: 16.2, 15.1, 15.4. |
| E21 | §3 box "E = T + V never changes" | verified | dE/dt = 0 exactly along (9) (E11). |

## Numbers and statements

| # | Claim (section) | Verdict | Evidence |
|---|---|---|---|
| N1 | Abstract: "explains how the page solves the equations, step by step, sixty times a second" | wrong, because | the page takes 600 RK4 steps per simulated second (h = 1/600 s, 10 steps per frame) and redraws about sixty times a second; "sixty" is the frame rate, not the stepping rate, and §7 says so correctly. Correct: "… solves the equations in steps of 1/600 s and draws the result sixty times a second". Minor. |
| N2 | §1 "over the first twenty seconds the energy stays fixed to better than one part in ten million" | verified | Largest \|E − E₀\| over 0–20 s, every step: 5.0 × 10⁻⁸ of E_scale, 8.0 × 10⁻⁸ of \|E₀\|. Both below 10⁻⁷. Same in Node and in Chromium. |
| N3 | §1 "a thousandth of a radian, one millimetre at the end of a one-metre rod" | verified | 0.001 rad × 1 m; the starting distance of the two lower bobs is 1.000 × 10⁻³ m. |
| N4 | §1 "end up in unrelated places within five seconds" | verified | Distance of the lower bobs at t = 5 s: 1.00 m (the pendulum spans 2 m). |
| N5 | §1 "the lower arm whips over the top" (high-angle start) | verified | θ₂ passes through ±180° ten times in the first 20 s (range −485° to +1245°). |
| N6 | §1 weather forecasts limited to about two weeks | verified | Zhang et al., J. Atmos. Sci. 76, 1077 (2019), read on journals.ametsoc.org via Firecrawl: "the ultimate limit of midlatitude day-to-day weather predictability is about 2 weeks". |
| N7 | §2 m₁ = 1 kg, l₁ = 1 m, g = 9.81 m/s²; sliders set m₂/m₁ and l₂/l₁ | verified | Code: `var g = 9.81, m1 = 1, l1 = 1`; `m2 = m1 * Math.exp(mass.value)`, `l2 = l1 * Math.exp(len.value)`. |
| N8 | Figure 1 geometry | verified | Rods 150.0 px each at θ₁ = 35.0°, θ₂ = 70.0°; angle arcs end at 34.9° and 70.0°; bobs to the right for positive angles, consistent with (1). |
| N9 | Figure 2 drawing and labels: 2.40 rad/s, period 2.62 s; 5.79 rad/s, period 1.09 s; ±√2 | verified | Slow mode drawn at 12.0° and 17.0° (ratio 1.42), fast mode 12.0° and −17.0°; 2π/2.3972 = 2.621 s, 2π/5.7874 = 1.086 s. |
| N10 | Exercise 5.1: 7° ≈ √2 × 5°; period near 2.6 s; with −7° "twice as fast as before and a little more" | verified | √2 × 5° = 7.07°. Page code, ten swings: 5°, 7° gives 2.623 s; 5°, −7° gives 1.101 s; ratio 2.38 (theory 1 + √2 = 2.41). |
| N11 | §6 Figure 3 "computed with the same equations and the same time step as the page" | verified | All 401 points of both curves recomputed with the page's `rk4()` at h = 1/600 s, every 0.05 s: largest difference 0.05 px (the SVG's 0.1 px rounding). |
| N12 | Figure 3 caption: low energy stays below about 1.5 mm for 20 s | verified | Largest distance 1.436 mm, at t = 15.79 s. |
| N13 | Figure 3 caption: high energy grows until as large as the pendulum | verified | 0.073 m at 4 s, 1.0 m at 5 s, largest 3.97 m (4 m is the most possible). |
| N14 | §6 new paragraph "Why do the two part?": small swings keep the gap's size; large swings grow it in bursts, most strongly while the lower rod is near the top | verified | Regular start: exponent → 0 (E18). Default start, renormalised full-state twin over 2000 s: growth rate 2.17 /s while the lower rod is within 45° of upright (19 % of the time) against 1.27 /s elsewhere; in the first 20 s, 36 % of the steps shrink the gap and the best 10 % of steps account for more than the whole net growth. |
| N15 | §6 "the distance reaches 0.1 m after 4.1 s" | verified | First step with d ≥ 0.1 m: t = 4.057 s (Node and Chromium per step; 4.065 s on 60-fps frames). |
| N16 | §6 "a straight line laid through it … gives λ ≈ 1.4 per second" | verified | Least-squares line of ln d against t over 0–4.057 s: slope 1.384 /s (every step), 1.376 /s (0.05 s grid). |
| N17 | §6 "doubles roughly every half second" | verified | ln 2 / 1.384 = 0.50 s. |
| N18 | §6 full calculation "shrinking the change back every 0.1 s over 20 000 s … λ ≈ 1.45 per second" | verified | Page code, full-state twin renormalised every 0.1 s for 20 000 s: 1.4552 /s (d₀ = 10⁻⁸), 1.4551 /s (d₀ = 10⁻⁶); every 0.5 s with d₀ = 10⁻⁹: 1.4552 /s. Running average 1.439 at 2000 s, 1.444 at 5000 s, 1.448 at 10 000 s, 1.455 at 20 000 s. |
| N19 | §6 "the 1.4 read off Figure 3 … was not far off" | verified | 1.38 against 1.455. |
| N20 | §6 e^1.45 ≈ 4.3 | verified | 4.263. |
| N21 | §6 e^14.5 ≈ 2 × 10⁶ | verified | 1.98 × 10⁶. |
| N22 | §6 "the trajectory wanders over much of what that energy allows" | verified | Qualitative; the run goes over the top repeatedly (N5) and its exponent is positive; "much of" leaves room for regular islands. |
| N23 | §6 "a drift of a few parts in 10⁸" | verified | First 20 s: between −3.3 × 10⁻⁸ and +5.0 × 10⁻⁸. |
| N24 | Exercise 6.1: from 10°, 10° the separation readout stays near 10⁻³ m | verified | 85 % of the time between 0.3 and 1.5 mm, 95 % above 0.1 mm; brief dips (down to 1.1 × 10⁻⁵ m) when the two bobs cross. |
| N25 | Exercise 6.1: from 120°, 150° the twin peels away within a few seconds | verified | 4.6 cm at 3 s (6 px at σ = 127.5 px/m), 7.3 cm at 4 s, 1 m at 5 s. |
| N26 | §7 "h = 1/600 s, ten steps per frame at sixty frames a second" | verified | Code `H = 1 / 600`. 60-fps frames: 10 steps each in exact arithmetic; in Chromium with 16.67 ms frames the floating carry gives 9, 10 or 11, averaging 10. |
| N27 | §7 frame cap 0.05 s, Time scale cap 1.5, "no more than 46 steps can be requested; the 600-step guard cannot act" | verified | `sim.js`: `dt = Math.min(…, 0.05)`; slider `max="1.5"`; `acc = Math.min(acc - n * H, H)`. Worst case dt = 0.05 s at 1.5×: 45 steps every frame, and 45 even when the carry is exactly h; 46 is a safe upper bound, 600 is never reached. |
| N28 | §7 Drift = (E − E₀)/E_scale, E_scale = (m₁+m₂)gl₁ + m₂gl₂, "depth of the potential well" | verified | Code line `drift = (E - E0) / ((m1 + m2) * g * l1 + m2 * g * l2)`; E_scale is the depth of V below the pivot level (V_min = −E_scale). |
| N29 | §7 "Over the first 20 s of the default start it stays within ±5 × 10⁻⁸" | verified | To two figures: per step it peaks at +5.0006 × 10⁻⁸ (t = 8.668 s) and bottoms at −3.28 × 10⁻⁸ (t = 19.135 s). |
| N30 | §7 "its largest value is +4.7 × 10⁻⁸, at t ≈ 8.7 s" | wrong, because | the largest value is +5.0 × 10⁻⁸ (5.0006 × 10⁻⁸ at t = 8.668 s, same in Node and Chromium). +4.7 × 10⁻⁸ is what a frame two steps off the peak samples: the stored drift is read once per frame, so its 20-s maximum is 4.99 × 10⁻⁸ for frames of exactly 10 steps and 4.71 × 10⁻⁸ for frames alternating 16.0 and 17.3 ms (both measured in Chromium). Correct: "its largest value is +5.0 × 10⁻⁸, at t ≈ 8.7 s". The time is right. |
| N31 | §7 "RK4 leaks energy … creeps downward almost in a straight line, by about 7 × 10⁻⁸ a minute: after ten minutes it reads about −7 × 10⁻⁷" | verified | In Chromium, page running at 60 fps: −0.71, −1.49, −2.23, −3.08, −3.63, −4.50, −5.03, −5.64, −6.51, −7.19 × 10⁻⁷ at minutes 1–10; readout "−7.2e−7"; least-squares slope −7.1 × 10⁻⁸ per minute. Remark: only the first digit is robust. Node 22 runs the same code to −8.0 × 10⁻⁷ (slope −8.3 × 10⁻⁸ per minute) because last-bit differences in Math.sin/cos grow chaotically, and starts moved by 10⁻¹² rad give −7.2 to −8.4 × 10⁻⁷. |
| N32 | §7 "Put the mass ratio at its top value of 10" | verified | Rounded: slider max 2.3 gives m₂/m₁ = e^2.3 = 9.974, shown as "9.97". All heavy-bob numbers below are for 9.974 (exactly 10 would give 1436 rad/s² and −4.9 × 10⁻⁴). |
| N33 | §7 "each time the rods pass within a few degrees of a straight line, the heavy bob gives the light upper rod a sharp kick" | verified | All 46 episodes with \|α₁\| > 300 rad/s² in 20 s happen as δ crosses 0 (rods in line, stretched out), none near δ = π; closest approach in each episode 2–7°, the acceleration peaking 9–12° either side of the line. |
| N34 | §7 "angular accelerations up to about 1300 rad/s² against 75 rad/s² for equal masses" | verified | Largest \|α₁\| per step over 20 s: 1335 rad/s² (m₂/m₁ = 9.974), 75.3 rad/s² (equal masses). (For the lower rod: 1388 and 97.7.) |
| N35 | §7 "steps of h are too coarse to follow it" | verified | Halving the step cuts the 20-s drift from −3.67 × 10⁻⁴ to −1.37 × 10⁻⁵ (h/2) and −4.8 × 10⁻⁷ (h/4): factors of 27 and 28, faster than the h⁴ law, as for an under-resolved feature. |
| N36 | §7 "The drift then reaches −3.6 × 10⁻⁴ within 20 s" | verified | Per step: minimum −3.67 × 10⁻⁴ at t = 19.42 s, −3.62 × 10⁻⁴ at 20 s; Chromium readout at 20 s "−3.6e−4". |
| N37 | §7 "Moving a mass, length, angle or angular-velocity slider restarts the motion …; the Time scale slider does not" | verified | `onInput: restart` on the six sliders, none on `speed`. |
| N38 | §8 pivot at the centre; σ = (min(W, H)/2 − 34)/(l₁ + l₂) | verified | Chromium, 1440 × 900 window: canvas 770 × 578, σ = (289 − 34)/2 = 127.5 px/m = stored `scale`; o_x = 385, o_y = 289. |
| N39 | §8 bob 1 at (x₀ + σl₁ sin θ₁, y₀ + σl₁ cos θ₁), bob 2 a further (σl₂ sin θ₂, σl₂ cos θ₂) | verified | Recomputed from the stored state, equal to the stored pixel positions to the last digit; the pixel at each centre is rgb(122, 31, 43) with alpha 255. |
| N40 | §8 protractor every 30° from the downward vertical, faint circle of radius σ(l₁ + l₂), dashed circle of radius σl₁ | verified | Code loop `a += 30` with (sin a, cos a): 0° at the bottom, 90° on the right. Pixel scans along three rays find the circles at r = 254.5–256 px (σ(l₁+l₂) = 255) and 126–128.5 px (σl₁ = 127.5). |
| N41 | §8 trail on its own layer, one segment per RK4 step, dimmed every frame by (1 − 0.008)^{60Δt} | verified | Code: `segment()` inside the step loop; `fade(1 - Math.pow(1 - 0.008, dt * 60))` with `destination-out`. Remark: Δt is the clock's dt, capped at 0.05 s and 0 while paused. |
| N42 | §8 "Its brightness therefore halves every ln 2/(60 \|ln 0.992\|) ≈ 1.4 s of real time" | wrong, because | the formula gives 1.438 s, but the canvas does not do it: it stores alpha in 8 bits and rounds. Measured in Chromium with the page's own fade code at 60 fps: alpha 217 (the trail's 0.85) falls by exactly 2/255 a frame, then 1/255 a frame, reaches half after 1.6 s, and stops at 63/255 after 2.35 s, for ever (the twin's 0.9 trail also stops at 63). On the running page, after 60 s of the default start, 56 045 canvas pixels (13 % of 770 × 578) sit at alpha 63, a permanent pink haze over everywhere bob 2 has been (`trail-60s.png`); only Clear trail or a restart removes it. Correct: the trail falls to half in about 1.6 s and then stays at about a quarter opacity; the 1.4 s is only the intended rate. |
| N43 | §8 bob 1 radius 8 px; bob 2 radius 8(m₂/m₁)^{1/3} clamped to 4–17 px | verified | Code `r2 = Math.max(4, Math.min(17, 8 * Math.cbrt(m2 / m1)))`; at the slider ends the formula gives 3.72 and 17.22, so both clamps act. Measured burgundy fill extents 6 px at m₂/m₁ = 1 and 16 px at 9.974 (radius 8 and 17 under the 2 px cream rim). |
| N44 | §9 "1/λ ≈ 0.7 s" | verified | 1/1.455 = 0.687 s. |
| N45 | §9 "After a few Lyapunov times (1/λ ≈ 0.7 s each) the computed path is no longer the exact path from that start" | wrong, because | the page's path stays close to the exact one far longer: compared with a run at h/8 (4096 times more accurate), bob 2 differs by 1 µm only at 4.6 s, by 1 mm at 10.9 s and by 10 cm at 14.3 s, that is about 16 to 21 Lyapunov times before the difference is visible. The step error starts near 10⁻¹² m and must grow by about 10⁹ to reach 1 mm, which at λ = 1.455 /s takes of order ln(10⁹)/1.455 ≈ 14 s (measured 10.9 s). "A few Lyapunov times" (2–3 s) is how long a millimetre start difference takes, not the integration error. Correct: "After some fifteen to twenty Lyapunov times (1/λ ≈ 0.7 s each; 11–14 s for the default start) …". |
| N46 | §7 method description against the code, line by line | verified | State order (θ₁, θ₂, ω₁, ω₂) as in `state`; F as in `deriv()`; RK4 as in `rk4()` (E19); frame loop `acc += dt * speed.value; n = Math.min(Math.floor(acc / H), 600); acc = Math.min(acc - n * H, H)`; `simT += H` per step; drift as N28; restart rules as N37. No mismatch. |

## References

| # | Reference | Verdict | Evidence |
|---|---|---|---|
| R1 | Taylor, *Classical Mechanics*, University Science Books 2005, link to Google Books, chapters 7, 11, 12 | verified | Link: curl → HTTP 200, page "Classical Mechanics – John Robert Taylor – Google Books", University Science Books, 2005, ISBN 9781891389221. Chapters: the Google Books page shows no contents and the publisher page (uscibooks.aip.org) reset the connection to curl and to Firecrawl, so the road was Firecrawl search: three independent contents listings agree on 7 "Lagrange's Equations", 11 "Coupled Oscillators and Normal Modes" (p. 417), 12 "Nonlinear Mechanics and Chaos" (p. 457). Book itself not opened. |
| R2 | Landau & Lifshitz, *Mechanics*, 3rd ed., Pergamon 1976, link to Elsevier shop, §5 problem 1 | verified | Link: curl → HTTP 200, "Mechanics – 3rd Edition", Volume 1, January 1, 1976, L. D. Landau, E. M. Lifshitz (the e-book record lists 1982). §5 problem 1: Firecrawl search, text excerpts of the book (dokumen.pub copy: "The Lagrangian for a system of particles §5 1. A coplanar double pendulum (Fig. 1)"), Elsevier ScienceDirect topic page with the same text, and the physlib source header "Section: 5 … Problem: 1 Coplanar Double Pendulum". |
| R3 | Strogatz, *Nonlinear Dynamics and Chaos*, 2nd ed., Westview Press 2015, link to Google Books | verified | Link: curl → HTTP 200, 2nd edition, ISBN 9780813349107. The Google Books record names Avalon Publishing, 2014 (release 29 July 2014); Westview Press is the imprint (Amazon: Westview Press; Open Library: Westview Press, 3 March 2015). No chapter cited. |

Outside this check's remit, seen in passing: all thirteen equation tags render, in order, with no KaTeX errors at 1440 and 390 px;
at 390 px every display except (12) is wider than its box (for example (9): 466 px in a 297 px box) and scrolls sideways.

Summary: 65 verified, 4 wrong (N1, N30, N42, N45), 1 unverifiable (E13).
