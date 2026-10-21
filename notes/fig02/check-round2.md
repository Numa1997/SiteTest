# Fig. 2 lecture note: independent check, round 2

Page: `public/simulations/Double Pendulum.html`, the `<article id="paper">` (lines 114–406, uncommitted rewrite).
Checked 21 Oct 2026 by a reader who did not write the note. `plan.md` was not read.

## How it was checked

- **Equations.** Every numbered equation and every unnumbered step between them was re-derived in SymPy 1.14 from the
  positions (1) alone. The Lagrangian was built from the time-dependent angles, and the Euler–Lagrange equations,
  momenta, determinant, Cramer solution, identities, small-angle limit, normal modes and RK4 order all come from that
  construction. Each difference to the note's printed form is exactly 0. For the α₂ line, the exact zero needed a rewrite
  to exponentials, and 2 000 random points agree to 1.3 × 10⁻¹². Units were checked by dimension symbols. The limits
  checked were m₂ → 0, m₁ → ∞, l₁ → 0, l₂ → 0, δ = 0 and δ = 90°.
- **Numbers.** These come from the page's own code, run in headless Chromium (Playwright, chromium-1194). The page is
  served from `public/`. `deriv`, `rk4` and `energy` are cut out of the page's inline script text at run time and
  executed unchanged; the CSP was bypassed only so that this extraction could run. Live-page figures (store values and
  readout text) were recorded on the running page, both with real requestAnimationFrame and with an exact 60 Hz fake
  clock. Trail fading was measured on a real Chromium canvas with the page's `fade()` operations.
- **Scripts (outside the repository):**
  `/tmp/claude-0/-home-claude/28515d04-9164-54bd-9b9e-d1d29616215d/scratchpad/r2/` holds `derive.py`, `num.py`,
  `work.py`, `lim.py` (SymPy), `run.cjs`, `run2.cjs`, `run3.cjs` (the page's integrator in Chromium), `live.cjs` (the
  live page) and `trail.cjs` (canvas fading). Outputs are in `run-out.json` and `run2-out.json`.

Summary: **3 wrong**, **2 unverifiable from the page**, everything else verified. A few verified rows carry a remark.

## Equations

| # | Location | Item | Verdict |
|---|---|---|---|
| E1 | §2, eq. (1) | x₁ = l₁ sin θ₁, y₁ = −l₁ cos θ₁, x₂ = x₁ + l₂ sin θ₂, y₂ = y₁ − l₂ cos θ₂ | verified. Matches the figure convention (θ from the downward vertical, x right, y up) and code lines 689–690. |
| E2 | §2 | θ₁ = 0 gives y₁ = −l₁; θ₁ = 90° gives x₁ = l₁, y₁ = 0; two degrees of freedom | verified |
| E3 | §3.1, eq. (2) | velocity components | verified (SymPy difference 0) |
| E4 | §3.1 | v₁² = l₁²ω₁² | verified |
| E5 | §3.1, unnumbered | v₂² = l₁²ω₁² + l₂²ω₂² + 2l₁l₂ω₁ω₂ cos(θ₁−θ₂), via cos a cos b + sin a sin b = cos(a−b) | verified |
| E6 | §3.2, eq. (3) | T | verified. Units kg m²/s² = J. The limits l₂ = 0 and m₂ = 0 give the single-pendulum T. |
| E7 | §3.2, eq. (4) | V = −(m₁+m₂) g l₁ cos θ₁ − m₂ g l₂ cos θ₂ | verified. Matches code lines 529 and 686. |
| E8 | §3.2 | δ = 0: speeds add, v₂ = l₁ω₁ + l₂ω₂; δ = 90°: Pythagoras | verified. Strictly, v₂ = \|l₁ω₁ + l₂ω₂\|. |
| E9 | §3 box | E = T + V is conserved | verified. dE/dt along (9) is exactly 0 in SymPy. |
| E10 | §3 box (★) | h = Σ ωᵢ ∂L/∂ωᵢ − L = 2T − (T − V) = T + V; every term of T is quadratic in the ωᵢ | verified |
| E11 | §3 box, "salad bowl" paragraph, and §4 intro ("they act along the rods, at right angles to every motion the rods allow, and so do no work") | rods steer the balls without doing work; only gravity changes speeds | **wrong, because** it holds only for the rod forces taken together. Rod 1 is always at right angles to ball 1's velocity. Rod 2 is not at right angles to ball 2's velocity: SymPy gives v₂ · (unit vector along rod 2) = −l₁ω₁ sin δ ≠ 0. So rod 2 does work on ball 2 at rate −T₂ l₁ω₁ sin δ (T₂ is the rod tension) and the opposite work on ball 1, and only the sum is zero, because rod 2's length is fixed. Correct statement: "the rod forces do no work in total: rod 1 always pushes at right angles to ball 1's path, and whatever rod 2 gives to one ball it takes from the other, because its length never changes". The energy conclusion E = T + V is unaffected. |
| E12 | §4.1, unnumbered δS | first variation of S | verified |
| E13 | §4.1 | integration by parts; the boundary term vanishes because δθᵢ(t₀) = δθᵢ(t₁) = 0 | verified |
| E14 | §4.1, eq. (5) | d/dt ∂L/∂ωᵢ − ∂L/∂θᵢ = 0, and the localised-wiggle argument | verified |
| E15 | §4.1, unnumbered p₁ | p₁ = (m₁+m₂)l₁²ω₁ + m₂l₁l₂ω₂ cos δ, "an angular momentum" | verified. SymPy: p₁ = r₁ × (m₁v₁ + m₂v₂) exactly, and p₁ + p₂ is the total angular momentum about the pivot. |
| E16 | §4.2 | d/dt cos δ = −sin δ (ω₁ − ω₂) | verified |
| E17 | §4.2, three-line display | ∂L/∂ω₁, its time derivative, ∂L/∂θ₁ | verified (each difference 0) |
| E18 | §4.2 | the ω₁ω₂ terms cancel on subtraction | verified. What remains, +m₂l₁l₂ω₂² sin δ, is moved to the right-hand side. |
| E19 | §4.2, eq. (6) | first equation of motion after division by l₁ | verified |
| E20 | §4.3 | ∂L/∂ω₂ = m₂l₂²ω₂ + m₂l₁l₂ω₁ cos δ | verified |
| E21 | §4.3, eq. (7) | second equation after division by m₂l₂ | verified. Limit l₁ → 0 gives α₂ = −(g/l₂) sin θ₂. |
| E22 | §4.4, eq. (8) | matrix form equals (6) and (7); det = l₁l₂(m₁ + m₂ sin²δ) > 0 | verified |
| E23 | §4.4 | the three identities: 2 sin²δ = 1 − cos 2δ; 2 sin θ₂ cos δ = sin θ₁ − sin(θ₁ − 2θ₂); sin θ₁ cos δ − sin θ₂ = cos θ₁ sin δ | verified. The third identity does supply the common factor sin δ of α₂ (checked through the Cramer numerator). |
| E24 | §4.4, eq. (9) | α₁ and α₂ in closed form | verified. They equal the exact solve of (8) symbolically, and code lines 508–512 match the formula term by term. |
| E25 | §4.4 | units: every term is in 1/s², and the masses cancel | verified |
| E26 | §4.4 | m₂ = 0 gives α₁ = −(g/l₁) sin θ₁ | verified. Also m₁ → ∞ gives the same α₁, as it should. |
| E27 | §5 | linearised (6)/(ml): 2θ̈₁ + θ̈₂ = −2(g/l)θ₁; (7)/l: θ̈₁ + θ̈₂ = −(g/l)θ₂ | verified. The series expansion of (9) also equals the inverse-matrix form of (10). |
| E28 | §5, eq. (10) | matrix form | verified |
| E29 | §5, bracket equation | [ (g/l) diag(2,1) − ω² ((2,1),(1,1)) ] u = 0 | verified |
| E30 | §5, determinant chain | 2(g/l − ω²)² − ω⁴ = 0, so g/l − ω² = ±ω²/√2, so ω² = (g/l)/(1 ± 1/√2) | verified |
| E31 | §5 | multiplying by √2(√2 ∓ 1) gives (2 ∓ √2)g/l | verified. (1 + 1/√2)·√2(√2 − 1) = 1. |
| E32 | §5, eq. (11) | ω∓² = (2 ∓ √2)g/l | verified. Remark: ω without an index (mode frequency) shares its letter with the angular speeds ωᵢ; this is not an error. |
| E33 | §5 | u₂/u₁ = 2(g/l − ω²)/ω² = ±√2; ω₊/ω₋ = 1 + √2 is irrational | verified |
| E34 | §6, eq. (12) | λ = lim_{t→∞} lim_{d₀→0} (1/t) ln(d/d₀), and the order of the limits | verified. Remark: the four-number distance mixes rad and rad/s; this is harmless, because λ does not depend on the norm (confirmed numerically below, N13). |
| E35 | §7 | F(s) = (ω₁, ω₂, α₁, α₂) | verified. Matches `deriv` return, line 513. |
| E36 | §7, eq. (13) | RK4 stages and weights | verified line by line against `rk4`, lines 515–525. |
| E37 | §7 | weights 1, 2, 2, 1 are Simpson's rule; local error h⁵, global h⁴ | verified. SymPy on y′ = ky: RK4 − e^{kh} = −(kh)⁵/120 + O(h⁶). |
| E38 | §7 | Euler: s(t+h) = s + hF(s) gains energy | verified. The page's `deriv` with Euler at h = 1/600 from 10°, 10° gains 0.053 J in 10 s. |
| E39 | §7, bullet 2 | E_scale = (m₁+m₂)gl₁ + m₂gl₂ | verified. Matches line 687. Remark: it is the depth of the valley measured from the pivot level (V_min = −E_scale); the full top-to-bottom range is 2E_scale. |
| E40 | §8 | σ = (min(W,H)/2 − 34)/(l₁+l₂); pivot at (W/2, H/2); screen positions with + cos | verified against `layout()` and `pos()` |
| E41 | §8 | per-picture dimming factor (1 − 0.008)^{60Δt}; half-life ln 2/(60 \|ln 0.992\|) | verified. `fade()` removes 1 − 0.992^{60Δt} with `destination-out`, so the alpha is multiplied by 0.992^{60Δt}. |
| E42 | §8 | r₂ = 8(m₂/m₁)^{1/3}, clamped to [4, 17] px; r₁ = 8 px | verified (line 626). The clamps are active at both slider ends: 8·0.100^{1/3} = 3.7 and 8·9.97^{1/3} = 17.2. |

## Numbers

| # | Location | Number in the note | Verdict |
|---|---|---|---|
| N1 | §1 | "in the first twenty seconds the total energy changes by less than one part in ten million" | verified. The largest value in 20 s is 5.0 × 10⁻⁸ of E_scale and 8.0 × 10⁻⁸ of E₀ = 18.306 J. |
| N2 | §1 and §6 | 0.001 rad is about 1 mm at the end of a 1 m rod | verified |
| N3 | §1 | "completely unrelated places within five seconds" | verified. The lower-ball separation reaches 1.00 m at t = 5.0 s; the reach of the pendulum is 2 m. |
| N4 | §1 | weather forecasts fade "after about two weeks" | unverifiable from the page, because it is an outside fact. It agrees with the usual literature value. |
| N5 | §1 | Galileo "four hundred years ago" | unverifiable from the page (history). It is about right: his pendulum work is c. 1602. |
| N6 | §2 | 2π ≈ 6.28; 1° ≈ 0.0175 rad | verified |
| N7 | §2 | m₁ = 1 kg, l₁ = 1 m, g = 9.81 m/s² | verified (code line 423) |
| N8 | Fig. 1 | drawn angles | verified. Rod 1 is at 35.0°, rod 2 at 70.0°, both 150 px long, and the arcs end at 34.9° and 70.0°. "Counter-clockwise positive" agrees with x = l sin θ for x right and y up. |
| N9 | §4 | Lagrange "in the 1780s", Hamilton later | verified as history. *Mécanique analytique* appeared in 1788 and Hamilton's principle in 1834–35. Lagrange already used the method from about 1760. |
| N10 | §4.4 note | "10 000 random states … worst relative difference 8 × 10⁻¹⁴" | verified in substance: rounding level, order 10⁻¹⁴. My own draws of 10 000 states, with m₂/m₁ and l₂/l₁ across the slider ranges, give 1.7 × 10⁻¹⁴ and 5.3 × 10⁻¹⁴ under norm-relative measures. A component-by-component measure reaches 7 × 10⁻¹², when one α is near zero. The exact figure 8 × 10⁻¹⁴ depends on the draw and the metric, and the note names neither. |
| N11 | §5 | at 10°: θ = 0.1745, sin θ = 0.1736, "half a percent apart" | verified (0.51 %) |
| N12 | §5, eq. (11) and Fig. 2 | ω₋ = 2.40 rad/s, ω₊ = 5.79 rad/s, periods 2.62 s and 1.09 s | verified: 2.3972, 5.7874, 2.6211 and 1.0857 |
| N13 | §5 | u₂/u₁ = +√2 ≈ 1.41 (slow), −√2 (fast) | verified |
| N14 | Fig. 2 | drawing | verified. Slow mode: θ₁ = 12.0°, θ₂ = 17.0°, ratio 1.42. Fast mode: 12.0° and −17.0°. The pale copy is the mirror image, the opposite turning point. |
| N15 | Ex. 5.1 | 5°, 7° ≈ √2 × 5°; period near 2.6 s; θ₂ = −7° is "twice as fast … and a little more" | verified. With the page's code, ten swings give 2.623 s and 1.100 s; the ratio is 2.38, against 1 + √2 = 2.41 from (11). |
| N16 | Fig. 3 | both curves come from the page's equations at h = 1/600 | verified. Recomputing with the page's `deriv`/`rk4`, sampled every 0.05 s and mapped with 31.7 px/s and 51.2 px/decade, reproduces all 401 + 401 SVG points to within 0.05 px, which is the SVG's 0.1 px rounding. |
| N17 | Fig. 3 caption | low energy "stays below about 1.5 mm for the whole 20 s" | verified. The largest value is 1.435 mm. |
| N18 | Fig. 3 caption | high energy grows to the size of the pendulum | verified. The separation reaches 1 m at 5.0 s and then stays at the 1–2 m scale. |
| N19 | §6 | growth "in bursts, most strongly while the lower rod is near the top" | verified. The local growth rate of a tiny state difference, averaged by the position of rod 2, is 2.34 /s with cos θ₂ < −0.5 (near the top), 0.67 and 0.77 /s in the middle bands, and 1.60 /s with cos θ₂ > 0.5. |
| N20 | §6 | separation reaches 0.1 m "after 4.1 s"; straight-line fit gives λ ≈ 1.4 /s; "doubles roughly every half second" | verified. First 0.1 m at t = 4.10 s; a least-squares fit of ln d over 0–4.1 s (83 points) gives 1.38 /s; ln 2/1.4 = 0.50 s. The fit method is not named in the note: the endpoint slope ln(100)/4.1 would give 1.12. |
| N21 | §6 | full Lyapunov run "with the page's equations and step, shrinking the change back every 0.1 s over 20 000 s … gives λ ≈ 1.45 per second" | **wrong, because** exactly that procedure gives **λ = 1.464**, which rounds to **1.46**. The settings were d₀ = 10⁻⁸, renormalised every 0.1 s, 20 000 s; the author's own `notes/fig02/lyap_long.cjs` uses the same settings. Other starting directions give 1.4639–1.4643. Eight 2 500 s blocks give 1.464 ± 0.005 (standard error). The value 1.45 appears only with h/2 over 10 000 s (1.448). Correct text: "λ ≈ 1.46 per second". All the consequences in N22–N24 survive this change at the precision quoted. |
| N22 | §6 | e^{1.45} ≈ 4.3 per second | verified: 4.26, and e^{1.464} = 4.32 |
| N23 | §6 | ten seconds further needs e^{14.5} ≈ 2 × 10⁶; 1 mm becomes "half a nanometre, the width of a few atoms" | verified: 1.98 × 10⁶ gives 0.50 nm; with λ = 1.464, 2.3 × 10⁶ gives 0.44 nm. Both are a few atomic diameters. |
| N24 | §9 | 1/λ ≈ 0.7 s; 15–20 Lyapunov times = 10–14 s | verified (0.69 s; 10.3–13.8 s). Measured directly: the page's step and an h/4 reference run of the default start differ in lower-ball position by 1 mm at 10.9 s, 1 cm at 12.1 s and 10 cm at 14.3 s. |
| N25 | §6 | "a drift of a few parts in 10⁸" | verified (5.0 × 10⁻⁸ in 20 s) |
| N26 | Ex. 6.1 | from 10°, 10° "its separation readout stays near 10⁻³ m" | verified, loosely. It stays below 1.44 mm and is between 0.3 mm and 3 mm for 84 % of the time, but dips to 1.1 × 10⁻⁵ m (below 10⁻⁴ m 5.5 % of the time). |
| N27 | Ex. 6.1 | from 120°, 150° the twin "peels away within a few seconds" | verified (1 cm at 2.4 s, 10 cm at 4.1 s) |
| N28 | §7 | h = 1/600 s, "ten steps for every picture, at sixty pictures a second" | verified at 60 Hz. Live page: n = 10 per frame, with an occasional 9 when the remainder is carried over. A 120 Hz screen would take 5 per picture; the note assumes 60 Hz here and in §8. |
| N29 | §7, bullet 1 | frame time capped at 0.05 s; Time scale ≤ 1.5; "at most 46 steps … for one picture"; the 600 cap is never reached | verified as a bound. `Sim.clock` caps dt at 0.05 s (sim.js line 179), the slider max is 1.5, and the carried remainder is below h. So 46 is a true upper bound. The reachable maximum is actually 45: 0.075 s is exactly 45 h and the remainder is strictly less than h. A 2 × 10⁶-frame emulation of the clock loop never exceeded 45. |
| N30 | §7, bullet 2 | 20 s of the default start "stays within ±5 × 10⁻⁸"; step-by-step maximum +5.0 × 10⁻⁸ at t ≈ 8.7 s | verified to the digits given: maximum +5.0006 × 10⁻⁸ at t = 8.668 s, minimum −3.3 × 10⁻⁸ at 19.1 s. Taken strictly, the maximum exceeds 5 × 10⁻⁸ by 0.01 %; "about ±5 × 10⁻⁸" would be exact. |
| N31 | §7, bullet 2 | "the readout, which samples once a picture, shows about +4.7 × 10⁻⁸ there" | **wrong, because** the Drift readout text is rewritten only every sixth picture (`if (frames++ % 6 === 0) readouts()`, line 748), which is ten times a second. The spike at 8.67 s lasts about one picture: the step-by-step drift is 1.8 × 10⁻⁸ at 8.658 s, 5.0 × 10⁻⁸ at 8.667 s and 2.6 × 10⁻⁸ at 8.675 s. So the readout usually misses it. In three Chromium runs the readout near 8.7 s showed −1.5 × 10⁻⁸, −1.7 × 10⁻⁸ and +4.7 × 10⁻⁸. Over the six possible phases of the readout, the largest value shown in 20 s ranges from 0.9 × 10⁻⁸ to 5.0 × 10⁻⁸. What samples once a picture is the store (data panel): in those runs it held 4.71 × 10⁻⁸, 4.71 × 10⁻⁸ and 4.20 × 10⁻⁸ at the spike (step-aligned 60 Hz frames: 4.99 × 10⁻⁸). Correct text, roughly: "the readout is rewritten ten times a second and usually misses this brief spike; the data panel, which stores every picture, holds about +4.7 × 10⁻⁸ there". |
| N32 | §7, bullet 2 | drift creeps down "by about 7 × 10⁻⁸ a minute: after ten minutes … about −7 × 10⁻⁷" | verified: −7.1 × 10⁻⁸ at 60 s, −1.49 × 10⁻⁷ at 120 s, … −7.19 × 10⁻⁷ at 600 s, close to a straight line. The step sequence is independent of frame timing, so the live page gives the same values. |
| N33 | §7, bullet 3 | mass ratio "at its top value of 10" | verified, approximately. The slider maximum 2.3 gives m₂/m₁ = e^{2.3} = 9.97, and the page displays "9.97". |
| N34 | §7, bullet 3 | kicks "each time the rods pass within a few degrees of a straight line" | verified, loosely. The acceleration peaks come in pairs at δ ≈ ±9° to ±12° from straight (for example 11.2° and −11.7° at the largest peak, t = 2.51 s). "About ten degrees" would be more exact than "a few". |
| N35 | §7, bullet 3 | "up to about 1300 rad/s² against 75 rad/s² for equal masses" | verified for the upper rod, which the sentence names. Step-by-step max \|α₁\| is 1335 rad/s² at ratio 9.97 and 75.3 rad/s² for equal masses (frame-sampled: 1323 and 72.5). For comparison, the lower rod reaches \|α₂\| = 1388 and 97.7. |
| N36 | §7, bullet 3 | "drift reaches −3.6 × 10⁻⁴ within 20 s"; h too coarse | verified. Frame-sampled and readout minimum −3.62 × 10⁻⁴ (the step-by-step extreme is −3.67 × 10⁻⁴ at 19.42 s). The coarseness is confirmed by halving: h/2 gives −1.46 × 10⁻⁵ and h/4 gives −4.1 × 10⁻⁷. |
| N37 | §7 | "halving the step makes the result sixteen times more accurate" | verified. The state error at t = 1 s against an h/16 reference shrinks by 15.4 from h to h/2. |
| N38 | §8 | protractor every 30° from the downward vertical, circle of radius σ(l₁+l₂), dashed circle of radius σl₁ | verified (lines 596–622) |
| N39 | §8 | ideal trail half-life ≈ 1.4 s | verified (1.438 s) |
| N40 | §8 | quantised trail: "falls to half in about 1.6 s and then stops fading at about a quarter of its strength" | verified at 60 pictures a second only. On a real Chromium canvas a 0.85-alpha segment (alpha 217) is at half at 1.60 s and stops at alpha 63 after 2.35 s; that is 29 % of its start and 25 % of full opacity. The behaviour depends on frame rate: at 120 Hz or 144 Hz it never reaches half and stops at alpha 127 (59 %) after about 0.7 s; at 30 Hz it halves at 1.5 s and stops at alpha 31 (14 %). The sentence should say it describes 60 pictures a second. |
| N41 | §8 | ball 1 radius 8 px, ball 2 clamped to 4–17 px | verified (see E42) |
| N42 | §7, bullet 4 | mass, length, angle and angular-speed sliders restart; the Time scale slider does not | verified (lines 498–504) |

## Description of the numerical method against the code

| # | Note says | Code | Verdict |
|---|---|---|---|
| M1 | state s = (θ₁, θ₂, ω₁, ω₂); F = (ω₁, ω₂, α₁, α₂) by (9) | `state` array; `deriv` returns `[o1, o2, a1, a2]` | verified |
| M2 | RK4 as in (13) | `rk4`, lines 515–525 | verified line by line |
| M3 | each picture advances real time × Time scale, in steps of h | `acc += dt * speed.value; n = min(floor(acc/H), 600)`; remainder carried as `acc = min(acc − nH, H)` | verified. The note does not mention that the remainder is carried to the next picture; this is not wrong. |
| M4 | frame time ≤ 0.05 s | sim.js line 179 | verified |
| M5 | trail: one segment per RK4 step on its own layer, dimmed every picture | `segment()` inside the step loop; `fade()` once per frame | verified |
| M6 | twin started with θ₁ + 0.001 rad, same integrator | `restart()` and the switch handler; `rk4(twin, H)` in the same loop | verified. Remark: switching the twin on mid-run starts it from the current state + 0.001 rad, not from the start. Exercise 6.1 is still right, because setting the angles afterwards restarts both pendulums. |
| M7 | separation d between the lower balls | `hypot(p₂ − q₂)/scale`, from the pixel positions divided by σ | verified. This is the distance in metres. |
| M8 | Drift readout = (E − E₀)/E_scale, "samples once a picture" | the value is computed every frame in `diagnostics()`; the text is written every 6th frame | the formula is verified; the sampling claim is wrong (N31). The panel label reads "Energy drift" where the note writes "the *Drift* readout"; this is a small wording difference. |

## References (§9.1)

| # | Item | Verdict |
|---|---|---|
| R1 | Taylor, *Classical Mechanics* (2005), chapters 7, 11 and 12 with the titles given | verified from my knowledge of the table of contents; the book was not opened |
| R2 | Landau and Lifshitz, *Mechanics*, 3rd ed. (1976), §5 problem 1, plane double pendulum | verified from my knowledge; not opened |
| R3 | Strogatz, *Nonlinear Dynamics and Chaos*, 2nd ed., Westview (2015) | verified from my knowledge; not opened |
