# Fig. 2 · Double pendulum · plan

Page `public/simulations/Double Pendulum.html`, note L114–379. Judged against notes/STANDARD.md §4 and "Numa's verdicts".
Every number in the note was recomputed first (scripts in this folder; results below). The equation numbering does not change.
Every edit stays on the line it starts on, so the page keeps its 870 lines and no line link in the doc moves.

## Verdicts

| Part | Verdict | Exact place, and why |
|---|---|---|
| Header, abstract (L115–120) | clear, leave it | |
| §1 A pendulum on a pendulum (L137–178), Figure 1 | needs work | L141 "the energy stays fixed to better than one part in ten million" is said without limit. Measured, it holds for the first minute or so only: \|ε\| first passes 10⁻⁷ at t = 82.8 s in Chromium (73.1 s in Node), and after ten minutes ε = −7.2 × 10⁻⁷. Figure 1 geometry checked (both rods 150 units, 35° and 70°): clear. |
| §2 The model (L180–185) | clear, leave it | |
| §3 Energy (L187–199), box | clear, leave it | Eqs. (2)–(4) checked in SymPy. |
| §4 From energy to motion ★ (L201–222) | needs work, one step | L219 names the identities that bring Cramer's rule to (9), but only those for α₁. α₂ needs sin θ₁ cos δ − sin θ₂ = cos θ₁ sin δ, which is where its common factor sin δ comes from; the note skips it. Eqs. (5)–(9) otherwise checked in SymPy; the L221 check (8 × 10⁻¹⁴) reproduced in order of size (1.2 × 10⁻¹⁴ to 1.7 × 10⁻¹³ over five seeds of 10 000 states). δ for a variation and δ = θ₁ − θ₂ side by side in §4.1: each use is clear in place; taste, left. |
| §5 Small swings (L224–275), Figure 2, Exercise 5.1 | clear, leave it | ω₋ = 2.397, ω₊ = 5.787 rad/s, periods 2.621 s and 1.086 s, u₂/u₁ = ±√2 (SymPy). Exercise: the page's integrator gives 2.623 s for (5°, 7°) and 1.101 s for (5°, −7°). |
| §6 Chaos (L277–342), Figure 3, Exercise 6.1 | needs work | L335 "the line rises at about 1.7 per second, so the distance doubles roughly every 0.4 s and reaches 0.1 m after 4.1 s": no reading of the curve gives 1.7, and 1.7 from 1 mm would reach 0.1 m at 2.7 s, not 4.1 s. Measured: a least-squares line through ln d up to the 0.1 m crossing (4.06 s) rises at 1.38 s⁻¹, doubling in 0.50 s; the full-state Lyapunov exponent of this start, by the rescaling method the note describes, is 1.45 s⁻¹ (1.44–1.46 over 20 000 s). L337 builds on 1.7: e^1.7 ≈ 5.5, 5.5¹⁰ ≈ 2 × 10⁷. Figure 3 itself is right: recomputed with the page's code, every plotted point agrees to 0.05 px (the SVG's rounding); low-energy maximum 1.44 mm; d(5 s) = 1.00 m. |
| §7 Solving it step by step (L344–354) | needs work | (a) L350 "The clock caps a frame at 0.05 s and the Time scale at 1.5": the clock (sim.js L179) caps the frame; the slider (L64) caps the Time scale. (b) L351 gives the drift for the first 20 s only. The standard asks where the method fails and what error to expect. Measured: the drift creeps on, about −7 × 10⁻⁸ per minute (−7.2 × 10⁻⁷ after 600 s); at mass ratio 10 it reaches −3.6 × 10⁻⁴ in 20 s; with both ratios at the top and the start θ₁ = 90°, θ₂ = −90°, ω₁ = 5, ω₂ = −5 rad/s, −0.13 (readout "−1.3e-1"). The h⁴ claim checked: halving h cuts the state error 15–18 times. "+4.7 × 10⁻⁸ at t ≈ 8.7 s" re-measured in Chromium: 4.710 × 10⁻⁸ at 8.665 s (per RK4 step the peak is 5.0 × 10⁻⁸ at 8.668 s, between two frames); kept. |
| §8 From metres to pixels (L356–360) | needs work | L358 "the masses are drawn at (x₀ + l sin θ, y₀ + l cos θ)" adds metres to pixels (σ missing); x₀, y₀, W, H are never defined; the two protractor circles are unexplained. L359: Δt is undefined, and "60 × 0.00803" comes from nowhere (0.00803 = −ln 0.992). Bob radii and the 1.44 s half-life checked against the code. |
| §9 What the model leaves out (L362–369) | clear, leave it | |
| §9.1 Further reading (L370–375) | needs work | None of the three references has a link. |

## Changes (only these)

1. §1 L141: add "over the first twenty seconds" to the energy sentence.
2. §4.4 L219: name the third identity, sin θ₁ cos δ − sin θ₂ = cos θ₁ sin δ (expand sin θ₂ = sin(θ₁ − δ)), for α₂.
3. §6 L335: the measured rise, 1.4 per second up to the 0.1 m crossing at 4.1 s, doubling every half second.
   L337: the rough 1.4 against the full calculation, λ ≈ 1.45 per second; the practical meaning with e^1.45 ≈ 4.3 and
   e^14.5 ≈ 2 × 10⁶.
4. §7 L350: "the slider caps the Time scale". L351: two sentences after the 20 s figure: the steady creep, then the heavy-bob
   failure, both measured in Chromium. The cause: when the rods pass within a few degrees of a straight line, the heavy bob
   kicks the light upper rod (|α₁| up to 1335 rad/s² at mass ratio 10, against 75 for equal masses; 88 % of the energy error
   comes from 1 % of the steps, all with |δ| ≤ 7°).
5. §8 L358–359: σ, the pivot (x₀, y₀) and the W × H figure named; bob 1 at (x₀ + σl₁ sin θ₁, y₀ + σl₁ cos θ₁), bob 2 a further
   (σl₂ sin θ₂, σl₂ cos θ₂); the two circles; Δt defined; ln 2/(60 |ln 0.992|).
6. §9.1 L372–374: links to pages opened in this session: Google Books for Taylor (2005) and Strogatz (2nd ed., ISBN
   9780813349107); Elsevier's page for Landau and Lifshitz, 3rd ed. The publisher page of Taylor (uscibooks.aip.org) did not
   open by any road (curl, Firecrawl, TinyFish, Exa, the Wayback Machine: connection reset or 503). Contents checked: Taylor's
   chapters 7, 11 and 12 from a library catalogue's contents note (Yachay Tech Koha record, ISBN 9781891389221); Landau and
   Lifshitz §5 Problem 1 "A coplanar double pendulum" read in the Internet Archive's text of the third English edition
   (preface dated Moscow 1976).

## How the numbers were measured

- `derive.py` (SymPy): eqs. (3), (4), (6), (7), (8), (9) and the three identities; (10)–(11).
- `eq9_check.py` (NumPy): (9) against a solve of (8), 10 000 random states, five seeds.
- `measure.cjs`, `measure2.cjs`, `measure3.cjs`, `fit.cjs`, `where.cjs`, `modes.cjs`, `lyap_long.cjs` (Node): the page's own
  `deriv`, `rk4`, `energy`, copied line for line, h = 1/600 s.
- `chromium.cjs` (Playwright, Chromium 1194, dist/ served on 127.0.0.1:8702): the store's `drift`, `t`, `sep`, `w1` read every
  frame after the page's own frame callback; real clock for 21.8 s (1280 frames, n = 10, 60.0 fps); Playwright's fake clock for ten
  simulated minutes and for the slider extremes; health at 1440 × 900 and 390 × 844.
