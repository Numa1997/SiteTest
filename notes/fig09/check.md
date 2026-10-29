# Fig. 9 · Driven oscillator · derivation check

Independent check of the lecture note in `public/simulations/driven-oscillator.html`
(between `<article class="paper" id="paper">` and `</article>`), file as at commit 468c139.
The file is unchanged at 6df11fb, and the working tree is clean for this file. The page script is byte-identical
to 127a8d2, so the numbers measured before the lead's last round still hold. I re-ran them on the current file and got
the same stored values, bit for bit.

I did not read `notes/fig09/plan.md` or any teacher report or script in `notes/fig09/`.

## How the check was done

- **Algebra.** SymPy 1.14 re-derives each numbered equation and each derivation step in the text, substitutes the results
  back into the ODE, and solves the initial-value problem with `dsolve` at the default parameters. Units are checked with
  `sympy.physics.units`. Limiting cases are taken with `sympy.limit`.
- **Numbers.** Built with `OUT_DIR=/tmp/fig09-check-dist npm run build`. The built page is byte-identical to the
  source. It was served by a small Node static server and driven by Playwright with headless Chromium
  (`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`). The whole store `Sim.data.ds` was read back for the default run and
  for each exercise setting, which the script set through the page's own sliders and *Solve* button.
- **Independent rerun.** RK4 was reimplemented in Python (float64) from the note's description. It gives `xs`, `vs`,
  `W_in` and `W_loss` bit-identical to the page's store. The exact solution (4)–(5) was recomputed in Python and gives the
  same `err_max`, 5.259404023405523e-12 m.
- **Static figures.** The SVG paths of Figures 2 and 4 were parsed, mapped back through their axes, and compared
  with equation (4) and with the stored run.
- **Canvas layout.** The canvas was measured at eight viewport widths (360–1600 px; canvas widths 326–834 px).
- **References.** Each link was opened with curl. Where curl got a 403, I used Firecrawl scrape. Each cited chapter was
  checked against the source; the road taken is given per row.

## Equations and derivation steps

| # | Item | Verdict |
|---|------|---------|
| E1 | (1) m ẍ + c ẋ + k x = F₀ cos Ωt | verified. Newton's law with −kx, −cẋ and F(t). Every term has units kg m s⁻². |
| E2 | (2) ẍ + 2ζω₀ẋ + ω₀²x = (F₀/m) cos Ωt | verified. SymPy: (1)/m − (2) = 0 with ω₀ = √(k/m) and ζ = c/(2√(km)), i.e. c = 2ζmω₀ (the code's `c`). Every term has units m s⁻². |
| E3 | ω₀ = √(k/m), "the angular frequency at which the block would ring with no damper" (new wording) | verified. For c = 0 the roots of s² + ω₀² are ±iω₀. Units s⁻¹. |
| E4 | ζ = c/(2√(km)); ζ = 0 rings forever, ζ = 1 no ringing | verified. Dimensionless. At ζ = 0 the roots are ±iω₀ (no decay). At ζ = 1 there is a double real root −ω₀. |
| E5 | (3) (ω₀² − Ω² + 2iζω₀Ω) Z = F₀/m ⇒ Z = …= X e^{−iφ} | verified. SymPy: substituting Z e^{iΩt} into the complex form of (2) gives exactly this factor. |
| E6 | §3.1: "write the force as the real part of (F₀/m) e^{iΩt}" | **wrong, because** (F₀/m)e^{iΩt} has units of acceleration (N/kg = m s⁻²). Its real part is F(t)/m, the right side of (2), not the force. The algebra after it is right. Only the noun is off by the factor m, which is hidden on the page because m = 1 kg. Correct: "write the force as the real part of F₀e^{iΩt}, so the right side of (2) is the real part of (F₀/m)e^{iΩt}", or "write the driving term F₀cos Ωt/m as the real part of (F₀/m)e^{iΩt}". |
| E7 | Physical denominator k − mΩ² + icΩ; dividing by m gives the form in (3) | verified. SymPy: (k − mΩ² + icΩ)/m − (ω₀² − Ω² + 2iζω₀Ω) = 0. Acceleration = −Ω² × displacement at the drive frequency. |
| E8 | Complex division: X = (F₀/m)/|D|, φ = arg D, 0° < φ < 180° because Im D = 2ζω₀Ω > 0; atan2(y, x) = angle of (x, y) | verified. Symbolically, |Z| = X. Numerically, Z = X e^{−iφ} with φ = atan2(2ζω₀Ω, ω₀² − Ω²) ∈ (0, π) in 2000 random cases (ω₀ 0.2–10, ζ 0.001–0.99, Ω 0.01–30), including Ω > ω₀. |
| E9 | Real coefficients ⇒ real part solves the real problem; x_p = Re X e^{i(Ωt−φ)} = X cos(Ωt − φ) | verified. SymPy: Re(X e^{i(Ωt−φ)}) − X cos(Ωt−φ) = 0 for real t. |
| E10 | (4) X = (F₀/m)/√((ω₀²−Ω²)² + (2ζω₀Ω)²), φ = atan2(2ζω₀Ω, ω₀²−Ω²) | verified. SymPy: X cos(Ωt−φ), with cos φ and sin φ taken from (4), satisfies (2) identically. Units: X in m, the atan2 arguments both s⁻². Limits: Ω → 0 gives X → F₀/k and φ → 0. Ω → ∞ gives X·mΩ²/F₀ → 1 and φ → π. Ω = ω₀ gives φ = π/2. ζ → 0 at Ω = ω₀/2 gives X → F₀/(m(ω₀² − Ω²)). The code's `steady()` is the same formula. |
| E11 | 3.2: x = e^{st} ⇒ s² + 2ζω₀s + ω₀² = 0, s = −ζω₀ ± iω₀√(1−ζ²) | verified. SymPy roots agree once 0 < ζ < 1 is imposed (writing ζ = √(1−y²)). 1000 random numeric cases put the residual at ≤ 1e-9. |
| E12 | τ = 1/(ζω₀); ω_d = ω₀√(1−ζ²) | verified. Units s and s⁻¹. ω_d is now first defined here (§2 no longer uses it). The code uses the same: `Math.exp(-z*w0*t)`, `wd = w0*Math.sqrt(1-z*z)`. |
| E13 | At ζ = 1 the imaginary part vanishes; ζ measures c against c = 2√(km) | verified. SymPy: ζ(c = 2√(km)) = 1. |
| E14 | Ringing written as e^{−t/τ}(C₁ cos ω_d t + C₂ sin ω_d t) (new line) | verified. SymPy: it satisfies the free equation identically. Units: C₁ and C₂ in m. |
| E15 | Initial conditions: X cos φ + C₁ = 0 and XΩ sin φ − ζω₀C₁ + ω_dC₂ = 0 | verified. SymPy: x(0) and ẋ(0) of the general form give exactly these two expressions. |
| E16 | (5) x(t) = X cos(Ωt−φ) + e^{−t/τ}(C₁ cos ω_d t + C₂ sin ω_d t), C₁ = −X cos φ, C₂ = (ζω₀C₁ − XΩ sin φ)/ω_d | verified. SymPy solves the two conditions for C₁ and C₂ and gets the same results. At the defaults, (5) minus `dsolve` with x(0) = ẋ(0) = 0 is below 1e-160 at 11 times from 0 to 60 s. Limit ζ = 0 at Ω = 0.9ω₀: (5) reduces exactly to X₀(cos Ωt − cos ω₀t), the undamped beat. Matches `exact()` in the code. |
| E17 | (6) X(ω₀) = F₀/(2ζk) = Q F₀/k, Q = 1/(2ζ) | verified. SymPy: X(Ω = ω₀) = F₀/(2ζmω₀²). Units m. Limit ζ → 0 gives ∞. |
| E18 | (6a) (ω₀²−Ω²)² + (2ζω₀Ω)² = [Ω² − ω₀²(1−2ζ²)]² + 4ζ²(1−ζ²)ω₀⁴ | verified. SymPy: the expanded difference is 0. Every term has units s⁻⁴. ζ → 0 gives (Ω² − ω₀²)² on both sides. |
| E19 | Ω_r = ω₀√(1−2ζ²) where the bracket vanishes | verified. SymPy: the only positive critical point of the denominator in Ω is ω₀√(1−2ζ²). The peak height there is F₀/(2ζk√(1−ζ²)), consistent and not stated. The code's `fr` is the same formula. |
| E20 | For ζ ≥ 1/√2 the bracket cannot vanish for any drive; the denominator is smallest at Ω = 0; the amplitude only falls; no peak | verified. With u = Ω², d/du of the denominator is 2(u − ω₀²(1−2ζ²)) > 0 for every u > 0 when ζ ≥ 1/√2, so the denominator rises monotonically from Ω = 0. At ζ = 1/√2 exactly the bracket is Ω², which vanishes only at Ω = 0 (no drive), so "for any drive" holds. The code agrees: ζ = 0.70 gives f_r = 0.071 Hz, and ζ = 0.71 gives the caption "no resonance peak (ζ ≥ 0.71)". |
| E21 | Phase: φ ≈ 0 below, φ = 90° at resonance (force largest when block fastest), φ → 180° above | verified. φ(Ω = ω₀) = π/2 exactly. ẋ = XΩ cos Ωt is then in phase with F, so P = Fẋ is largest. The note uses "resonance" for Ω = ω₀ throughout (eq. (6)). At the amplitude peak Ω_r the lag is 87.1° for ζ = 0.05; the text does not claim otherwise. |
| E22 | (7) X(s) = G(s)F(s), G(s) = 1/(ms² + cs + k); X(s) and F(s) are transforms, not the amplitude X (new line) | verified. SymPy: L{m f″ + c f′ + k f} = (ms² + cs + k) L{f} for f(0) = f′(0) = 0, checked on a test function. Units: G in s²/kg = m/N, and G(0) = 1/k (static limit). |
| E23 | Poles s = −ζω₀ ± iω_d; real part = −1/τ; both in the left half-plane ⇒ stable | verified. The roots of ms² + cs + k with c = 2ζmω₀ and k = mω₀² equal E11. Re s = −ζω₀ = −1/τ < 0 for ζ > 0. The sign ("decay rate with a minus sign") is right. |
| E24 | G(iΩ) = X e^{−iφ}/F₀ | verified. SymPy: G(iΩ) − Z/F₀ = 0. |
| E25 | Bode plot: \|G(iΩ)\| and φ against the drive frequency on logarithmic axes | verified. In `bodeGeom()`, x ∝ ln f (0.05 to 2 Hz, 241 log-spaced points) and the \|G\| axis ∝ log₁₀\|G\|. The phase axis is linear in degrees, as usual for a Bode plot. "Logarithmic axes" holds for the frequency axis and the magnitude axis. |
| E26 | (8) E(T) − E(0) = ∫F ẋ dt − ∫c ẋ² dt, E = ½mẋ² + ½kx² | verified. SymPy: dE/dt on solutions of (1) is Fẋ − cẋ². Every term has units J. |
| E27 | ⟨P_in⟩ = ⟨P_loss⟩ = ½cΩ²X² (speed amplitude ΩX, ⟨sin²⟩ = ½) | verified. SymPy: ⟨c ẋ_p²⟩ over one period is ½cΩ²X² and ⟨F ẋ_p⟩ is ½F₀XΩ sin φ. The two are equal once X and φ from (4) are inserted. Units W. Agrees with Feynman (24.4), ⟨P⟩ = ½γmω²x₀². |

## Numbers

All stored values were read from `Sim.data.ds` in headless Chromium after the page's own `solve()`.

| # | Number in the note | Recomputed | Verdict |
|---|---|---|---|
| N1 | m = 1 kg | `M = 1` | verified |
| N2 | Defaults f₀ = 0.5 Hz, ζ = 0.05, F₀ = 1 N, f = 0.45 Hz | slider `value` attributes 0.5, 0.05, 1, 0.45; stored the same | verified |
| N3 | k = 9.87 N/m | 9.869604401 | verified |
| N4 | c = 0.314 kg/s | 0.314159265 | verified |
| N5 | x(0) = 0, ẋ(0) = 0 | `x = 0, v = 0` before the loop; xs[0] = vs[0] = 0 | verified |
| N6 | τ = 6.37 s (§3.2) | 6.366198 | verified |
| N7 | X = 0.482 m | 0.48193572 (readout "0.482 m") | verified |
| N8 | φ = 25.3° | 25.346176° (readout "25.3°") | verified |
| N9 | Q = 10 | 10 (readout "10.0") | verified |
| N10 | static stretch 0.101 m | F₀/k = 0.10132118 | verified |
| N11 | 1.01 m at resonance | Q F₀/k = 1.0132118. With f = f₀ the page stores X = 1.0132118 and measures 1.0131257 | verified |
| N12 | f_r = 0.4987 Hz | 0.49874843 (Bode caption shows "0.499 Hz") | verified |
| N13 | f_d = ω_d/2π = 0.499 Hz | 0.49937461 | verified |
| N14 | 1/\|f − f_d\| = 20.25 s | 20.2533 s. In the stored run the beat minima fall at 19.04 and 39.05 s (spacing 20.01 s); the peak picking can only resolve ±0.55 s (half a drive period) | verified |
| N15 | with f₀ in its place, 20 s | 1/\|0.45 − 0.5\| = 20.000 s | verified |
| N16 | first swell 0.596 m at t = 8.0 s | largest stored \|x\| = 0.596151 m at t = 7.99 s (x is negative there). Later swells: 0.4865 m at 29.05 s, 0.4821 m at 50.16 s | verified |
| N17 | τ = 6.4 s (§6) | 6.366 s, rounded | verified |
| N18 | after half a minute only ±X = ±0.482 m is left | max \|x − X cos(Ωt−φ)\| over t ≥ 30 s is 0.0042 m (0.9 % of X); over t ≥ 40 s it is 0.00088 m | verified |
| N19 | Fig. 4: default run, RK4 h = 1 ms, plotted every 50 ms | x(t) path: 1201 points, Δt = 50 ms. Mapped back through the axes it matches stored `xs` to ≤ 3.2e-4 m, the 0.05 px rounding of the SVG. ±X lines at ±0.48178 m (0.1 px rounding). The dashed F(t)/k curve has 601 points (every 100 ms) and matches stored `xqs` to ≤ 3.0e-4 m. "Every 50 ms" describes the run x(t), which is what the caption says | verified |
| N20 | Fig. 4: lag φ = 25.3°, motion 4.76 times larger than F/k | X k/F₀ = 4.756515 | verified |
| N21 | Fig. 2: amplitude and phase from (4) for ζ = 0.05, 0.1, 0.2, 0.5 | 400 points per curve at f/f₀ = 0.1·100^{j/399}. Every point lies within 0.07 px of (4) for amplitude and within 0.05 px for phase. Drawn peaks 10.00, 5.02, 2.55, 1.16 against exact 1/(2ζ√(1−ζ²)) = 10.01, 5.03, 2.55, 1.15 | verified |
| N22 | Fig. 2 tick labels 0.32 and 3.2 | 10^{∓0.5} = 0.316, 3.16, placed at half decades | verified |
| N23 | ⟨P⟩ = 0.292 W | ½cΩ²X² = 0.291664 W. From the stored run over the last 5 drive periods: mean P_in = 0.29161 W, mean P_loss = 0.29175 W | verified |
| N24 | W_in = 19.03 J | 19.0317286 J. Python RK4 gives it bit-identical; the trapezoid rule over stored P_in gives 19.03169 J | verified |
| N25 | W_loss = 17.93 J | 17.9256419 J (trapezoid over stored P_loss: 17.92563 J) | verified |
| N26 | E(T) − E(0) = 1.11 J | 1.1060867 J. W_in − W_loss = 1.1060867 J; the rounded 19.03 − 17.93 gives 1.10 only by rounding | verified |
| N27 | (8) holds to 1.3×10⁻¹² of W_in | `balance` = 1.27355e-12 (readout "1.3e−12") | verified |
| N28 | t = 0 to 60 s in 60 000 steps of h = 1 ms | `H = 0.001, TEND = 60`; the loop performs exactly 60 000 RK4 steps (break at step = 60 000); `steps` = 60000 | verified |
| N29 | default solve took 9.5–12.4 ms in headless Chromium | **unverifiable, because** it is machine- and load-dependent (the note says so). Here, on a shared machine: first solve after a fresh load 10.6–27.0 ms over 12 loads, and 105 ms in one load under heavy load; warm re-solves 2.5–9.9 ms over 30 runs. The stated range overlaps these measurements but cannot be reproduced as a fixed number | unverifiable |
| N30 | 6 001 rows, one every 10 ms | `NS = 6001`, `ts` step 0.01 s, ts[6000] = 60 s | verified |
| N31 | largest RK4 − exact difference 5×10⁻¹² m | `err_max` = 5.2594e-12 m (readout "5.3e−12 m"). Recomputed in Python from the stored xs and an independent (5): identical | verified |
| N32 | n = round(t_play / 10 ms) | `Math.round(playT / (EVERY * H))`, clamped to 0…6000 | verified |
| N33 | window = four drive periods, not less than 6 s, not more than 20 s; 8.9 s with the defaults | `Tw = min(20, max(6, 4/f))`; stored `win_T` = 8.8889 s | verified |
| N34 | strip of the whole 60 s with the window shaded | `drawOverview()`: 0–60 s axis, fill `rgba(122,31,43,0.07)` from win_t0 to win_t0 + Tw | verified |
| N35 | §9 (new): the block rests near the middle of the canvas | eq_px / box_w = 47.7–50.7 % at canvas widths 326, 356, 380, 630, 690, 702, 770, 834 px (770 px: 47.75 %; 356 px: 49.97 %) | verified |
| N36 | §9 (new): every run at its own scale; largest swing spans about a fifth of the width, whatever the amplitude; ruler under the block gives metres | 2·amp_px / box_w = 19.2–20.3 % at the same eight widths. amp = 0.11·W₀ and px/m = amp / max\|x\|, so the scale is set per run. The ruler under the floor is labelled ∓max\|x\| m (screenshot at 1280 px: "−0.60 · 0 · +0.60 m" for max\|x\| = 0.596 m) | verified |
| N37 | Exercise 4.1: f = f₀ = 0.50 Hz; Measured, last 10 s vs Q F₀/k; φ | measured 1.0131 m (readout "1.013 m") vs Q F₀/k = 1.0132 m (readout "1.013 m"); φ = 90.0° | verified |
| N38 | Exercise 4.1: ζ = 0.2, factor by which the amplitude fell | X = 0.25330 m; ratio 4.000 exact (Q 10 → 2.5), 3.9997 measured | verified |
| N39 | Exercise 6.1: ζ = 0.01, the beats last for the whole minute | τ = 31.8 s. The stored-run envelope still swings between 0.38 and 0.64 m in the last 20 s (swells at 8.97, 30.03, 50.03 s) | verified |
| N40 | Exercise 6.1: time between two swells vs 1/\|f − f₀\| | measured swell spacings 21.06 s and 20.00 s vs 20.00 s (1/\|f − f_d\| = 20.01 s at ζ = 0.01) | verified |
| N41 | Exercise 6.1: f = 0.20 Hz, no slow beats; the ringing starts as large as the steady motion, explained by C₁ | φ = 0.55°, C₁ = −X cos φ = −0.120610 m, C₂ = −0.001666 m, X = 0.120615 m; √(C₁² + C₂²)/X = 1.00005. The beat between 0.2 and 0.5 Hz has period 3.3 s, shorter than the 5 s drive period, so there are no slow beats | verified |
| N42 | Exercise 6.1: the force switches on at full strength at t = 0 | F(0) = F₀ cos 0 = F₀; stored Fs[0] = 1 N | verified |
| N43 | §10: the page covers ζ ≤ 0.9 only | `zeta` slider min 0.01, max 0.9, step 0.01 | verified |
| N44 | §1: Millennium Bridge swayed on its opening day in 2000 | opened 10 June 2000 and swayed that day by synchronous lateral excitation (Wikipedia article and Penn State AE failures page, via Firecrawl search) | verified |
| N45 | Cross-references: Fig. 2 = double pendulum, integrated while you watch; Fig. 10 = controller on a wind turbine | `Double Pendulum.html` calls `rk4(state, H)` inside `Sim.clock`; `wind-turbine.html` compares generator-torque controllers | verified |

## Figure 3 (box widened)

| # | Item | Verdict |
|---|---|---|
| F3 | Box 274–514 (width 240), "G(s) = 1 / (ms² + cs + k)" inside | verified. Measured with getBBox in Chromium at eight widths: the text spans x = 296–499.3, leaving 14.7 px to the right edge. The input arrow tip is at 272 against the box at 274. The output line starts at 514, the box edge. The labels "output, the motion" (526–630.9) and "x(t)" (550–578) clear the box. The block diagram matches (7). |

## Numerical method: note against code, line by line

| # | Note says | Code | Verdict |
|---|---|---|---|
| M1 | "The fourth-order Runge–Kutta method advances (x, ẋ)" | lines 583–591: the classical RK4 stages k₁…k₄ for x′ = v, v′ = a(t, x, v); `accel()` = (F₀ cos Ωt − cv − kx)/M | verified |
| M2 | "from t = 0 to 60 s in 60 000 steps of h = 1 ms" | `for (step = 0; step <= TEND/H; step++)`, `break` at step = 60 000; `t = (step+1)*H` (no accumulated rounding) | verified |
| M3 | "carrying W_in and W_loss along in the same steps" | lines 587–589: the RK4 quadrature of F v and c v² with the same stage velocities v, v₂, v₃, v₄ and F at t, t + h/2, t + h. This is exactly RK4 applied to the augmented system | verified |
| M4 | "Every tenth state is written … together with F, E, P_in and P_loss: 6 001 rows, one every 10 ms" | lines 576–580 (`step % EVERY === 0`, EVERY = 10). The store also keeps t, v and, after the loop, F/k and Ωt mod 2π. The note does not claim it keeps nothing else | verified |
| M5 | "The exact solution (5) is stored next to it only to measure the error" | lines 594–600: `xex[n] = exact(...)`, `err = max\|xs − xex\|`; xex feeds no drawing | verified |
| M6 | "Each frame converts the playback time into the nearest stored row … draws that row as it is. Nothing is interpolated or recomputed" | `frame()` line 904; `draw()` uses xs[i], Fs[i], ph[i]; the window and strip draw stored samples only. The only arithmetic is the metres/seconds-to-pixels mapping | verified |
| M7 | "When you move a slider after solving, the page says so and keeps playing the old run" | measured: after moving f to 0.6 the status reads "A slider moved. The run below is still the one for f₀ = 0.50 Hz, ζ = 0.05, F₀ = 1.0 N, f = 0.45 Hz…", and the stored fd and win_T are unchanged | verified |
| M8 | "Measured, last 10 s" and the Bode ring "from the last 10 s of the run" | `if (ts[n] >= TEND - 10) xm = max(xm, \|xs[n]\|)`; ring at `Gm_drive = Xm/F0` | verified |
| M9 | Bode: filled dot from (4), ring from the run; they coincide once settled | dot at `G_drive` = 1/(m\|D\|) and `phi_deg`; ring at `Gm_drive` (0.48209 vs 0.48194 m/N at the defaults) | verified |
| M10 | §9: arrow ∝ F/F₀; dial at top right turning at Ω with horizontal shadow ∝ F; window x(t) dark up to now and pale after; F/k dashed burgundy; ±X dashed rose | `fpx = Fs[i]/F0 · fmax`; dial at (w − r − 24, r + 16), arm angle ph = Ωt mod 2π, shadow point cx + r cos Ωt; ink for n ≤ i, FAINT for n ≥ i; F/k dash [6,4] in rgba(122,31,43,.85); ±X dash in `T.rose`. The arrow is drawn just above the block, starting at its centre | verified |

## References

| # | Reference | Road taken | Verdict |
|---|---|---|---|
| R1 | Taylor, *Classical Mechanics*, University Science Books 2005, ch. 5 | curl → 200. The Google Books page names John Robert Taylor, University Science Books, 2005, 786 pp. Chapter 5 is "Oscillations", with 5.4 Damped Oscillators, 5.5 Driven Damped Oscillations, 5.6 Resonance (contents page henry.pha.jhu.edu/chapters.html, found via Firecrawl search, and a Scribd excerpt giving pp. 179 and 187) | verified |
| R2 | French, *Vibrations and Waves*, W. W. Norton 1971 (now CRC Press), ch. 4 | curl → 200. The Routledge page says "1st Edition … A.P. French, Copyright 1971 … by CRC Press" and its contents list "4 Forced vibrations and resonance". The Open Library API lists the 1971 first publication by W. W. Norton (M.I.T. Introductory Physics Series) | verified |
| R3 | Åström & Murray, *Feedback Systems*, Princeton 2008, ch. 8; free electronic edition | curl → 200, a 408-page PDF, v2.10b of 22 Feb 2009, "Copyright © 2008 by Princeton University Press". Chapter 8 is "Transfer Functions": 8.2 Derivation of the Transfer Function (frequency response, 24 mentions in the chapter), 8.4 The Bode Plot, Example 8.1 Damped oscillator | verified |
| R4 | Feynman Lectures Vol. I ch. 23, Resonance (complex method) | curl → 403 (bot block, not proof of a dead link). Firecrawl scrape → 200, "23 Resonance": 23–1 complex numbers and harmonic motion, 23–2 the forced oscillator with damping, where x̂ = F̂/(m(ω₀² − ω² + iγω)) | verified |
| R5 | Feynman Lectures Vol. I ch. 24, Transients (mean power, dying free motion) | curl → 403. Firecrawl scrape → 200, "24 Transients": 24–1 gives ⟨P⟩ = ½γmω²x₀² (24.4), the note's ½cΩ²X²; 24–2 covers damped oscillations, x = A₀e^{−γt/2} cos ω₀t | verified |

## Summary

88 rows: **86 verified / 1 wrong / 1 unverifiable.**

- Wrong: E6, where "the force" is (F₀/m)e^{iΩt}, off by a factor of m in units. A one-word fix; the mathematics around it is right.
- Unverifiable: N29, the solve time 9.5–12.4 ms, because it depends on the machine.
- Everything else matches: the SymPy derivations, the units and limits, the numbers in the store, an independent Python rerun, and the pixels of Figures 2 and 4.
