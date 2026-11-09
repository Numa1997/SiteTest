# Chapter 7 "Detect and measure": derivation and number check

Reviewer's check of `public/portfolios/electron-beam/index.html`, `#ch07` (source `portfolios-src/electron-beam/text/ch07.py`;
module `physics/ch07.js`, twin `ref/ch07.py`, checks `derive/ch07.py`, data `data/ch07/derive_results.json`). 9 November 2026.
Chapter 7 only. No repository file other than this one was changed. No repository script that writes into the repository was run.

How it was checked:
- **Equations.** I re-derived (7.1) to (7.6) in SymPy 1.14 with my own script, not `derive/ch07.py`:
  - (7.1): the secant law with θ = 90° − β.
  - (7.2): a box convolved with a Gaussian, its zero-width limit, and the quadrature sum of two Gaussian blurs.
  - The FW50 of a round Gaussian, and its 1-D marginal.
  - (7.3): the compound Poisson moments, from probability generating functions.
  - (7.4) and (7.5): the derivatives of the interpolated threshold crossing, and the scale invariance of the rule.
  - (7.6) and the dose: units with `sympy.physics.units`.
  - Problem 2: worked out in closed form.
- **Numbers.** I recomputed every `[data-n^="ch07."]` span of `#ch07` (29 spans, 27 keys) in headless Chromium (Playwright,
  `/usr/bin/google-chrome`) from the built page's own modules:
  - `EB.ch07.compute` with `EB.core.withDefaults(EB.contract, …)`, and `EB.ch05.compute` for `c5_dp`;
  - each value formatted with the page's `EB.core.fmt` at the number's `sig`, then compared with the DOM text.

  Expressions (`ex`) are evaluated on the unrounded module outputs, as `eb_lib.py` does (lines 219–228). No page errors. The only
  console error is a font CORS refusal under `file://`. The check table, the equation numbers (7.1)–(7.6) and the C6 detail were
  read from the DOM as well.
- **Parity.** I compared `physics/ch07.js` in Node with `ref/ch07.py` (run with `-B`, no bytecode written) on the module's 5 cases
  plus 3 more.
- **Method.** I read `physics/ch07.js` against §7.2–§7.6 sentence by sentence. On scratch copies I measured:
  - which pixels carry the error-propagation derivatives;
  - Monte Carlo runs of 40 000 repeats, with the peak pixel free and with it fixed;
  - the effect of cutting the periodic sum at ±2 periods;
  - the counts collected per position.
- **Sources.** The Applied Materials product page (the 95 % and 100-million quotations) could not be opened. A plain request
  returned 403. The Wayback Machine and a reader proxy were refused by this session's permission classifier ("bot-check
  circumvention"), and I did not try again. No web-search tool is available to this agent. So both quotations are unverifiable
  below.

Scripts (scratchpad `/tmp/claude-0/-home-user-SiteTest/c8b76f47-83f6-5259-bec8-4485c7f5a448/scratchpad/ch07d/work/`, not in the
repository):
- `sym7.py`: the derivations.
- `run7.cjs`: the numbers in Chromium. Output in `chromium_out.json`.
- `par7.cjs` + `par7.py`: parity.
- `exp7.cjs`, `exp7b.cjs`, `exp7c.cjs`: the Monte Carlo against error propagation, and the pixel derivatives.
- `trunc.cjs`, `trunc2.cjs` with `ch07_k.js`, a copy of the module with a settable range for the periodic sum: truncation,
  Problem 3, and the collected counts.

## Errors found (summary)

None changes an equation. None changes a number as the code computes it: all 29 spans match. Five statements are wrong:

1. **Problem 2 is wrong: the optimum does not depend on t_ov, and there is no interior optimum.**
   - From (7.5), a required σ_CD fixes t_d N = A (with A = K/(I_p σ²)). The time per site is then N²t_d + t_ov = N·A + t_ov.
   - That time grows linearly with N, so the most measurements per hour come from the smallest N the field allows, with
     t_d = A/N. SymPy gives d(time)/dN = A > 0.
   - t_ov only adds a constant, so it cannot move the optimum. It decides how much the choice matters: with t_ov = 1 s, the
     difference is small.
   - Fix: ask for the best N and t_d (answer: the smallest N and the longest dwell). Then ask why t_ov makes the choice nearly
     irrelevant, instead of why it changes the answer.
2. **Problem 1, "more than √2 times this for the width", is false at the default.**
   - Module error propagation at the default: σ_CD = 1.29 σ_S/|S′|, with σ_S the pixel noise at the right crossing (pixel at 14.5 nm)
     and S′ = −0.793 counts/nm between the crossing pixels. That is less than √2 = 1.41.
   - The cause: linear interpolation splits the crossing between two independent pixels with weights f and 1 − f
     (f = 0.78 at the default). That shrinks the crossing noise per edge to √(f² + (1 − f)²) = 0.81 of σ_S/|S′|.
   - Threshold noise from the floor and peak pixels adds back only part of that.
   - Fin-like line: 1.34. Blunt probe (Example 7.3): 1.50, the only setting checked where the premise holds.
   - Fix: "Why can the module's error propagation give less than √2 times this, and when more?" Or state the setting.
3. **§7.4, Example 7.1: "collects 3200 electrons per position across" counts the beam electrons, not collected ones.**
   - 3200 is n̄N = 6.24 × 512 = 3196: the primaries that land per position over the 512 lines.
   - The detector collects n̄N·η_cY: 2145 at the floor and 4689 at the edge peak (from `setup`).
   - Fix: "which brings 3200 beam electrons to each position across (about 2100 to 4700 of them counted)".
4. **§7.5, "Most of them are zero": at the default exactly half are non-zero.**
   - Non-zero derivatives at the default: 20 of the 40 pixels of the period. That is 10 floor pixels, 2 × 3 peak pixels and
     2 × 2 crossing pixels. For the fin-like line it is 22 of 40.
   - The floor alone is a quarter of the period (the middle half of the 20 nm space).
   - Fix: "Only the pixels at the two threshold crossings, those that set the peak levels and those of the floor take part, about
     half of them here."
5. **§7.5, "the Monte Carlo being slightly larger, as the curvature of the profile near the threshold makes it": at the default,
   the reason given is not the main one.**
   - With 40 000 repeats instead of 1000, the default MC/EP ratio is 1.025 ± 0.004, not 1.050. The page's 1000-repeat value
     (0.285 nm) sits 2 % above the converged 0.278 nm, within its own ±2.2 %.
   - Fixing the peak pixel to its noise-free position lowers the ratio to 1.008. So about two thirds of the excess comes from the
     rule's choice of peak pixel. That choice jumps between noisy realisations: the two top pixels of each edge peak have equal
     means (9.15834 counts), and the argmax moves in 80 % of the 1000 page repeats. It is a discontinuity of the rule, which
     first-order propagation cannot see.
   - Fin-like line: 1.041 → 1.013 with the peak fixed. At t_d = 10 ns fixing the peak does not help (1.042 → 1.044), so there
     the nonlinearity of the threshold rule dominates.
   - At high counts the gap closes: 0.996 at t_d = 10 µs, 0.994 at 100 µs. That fits a noise-driven effect of either kind.
   - Fix: "slightly larger, mostly because the noisy peak picks a different pixel from time to time, which first-order
     propagation does not see".

Remarks (true statements that could mislead, or code limits not stated in the text):
- **Blunt probe, Example 7.3: first-order σ_CD and the Monte Carlo disagree by 11 %, the other way round.**
  - Error propagation gives 1.886 nm, shown as "1.9". The module's own Monte Carlo gives 1.678 nm (1000 repeats) and 1.674 nm
    (40 000 repeats).
  - The ratio 0.888 is outside the "within 10 %" of C6, and the Monte Carlo is smaller there, not larger. One line's SNR is 0.25,
    and the mean of the found widths is biased by −1.0 nm. First order is not reliable at this setting.
  - The conclusion "a larger probe costs … in precision" stands either way (×5.9 to ×6.9).
  - Suggest quoting both values, or adding this setting to C6 with the ratio shown.
- **The periodic sum is cut at ±2 periods** (`yieldAt`, line 39: `for (let k = -2; k <= 2; k++)`). The text says "the walls of the
  neighbouring lines are added too".
  - At the default this is exact: identical to 4 digits with ±50 periods.
  - Within the panel's slider ranges it is not. Cases measured (d_p, pitch, CD → CD_meas, σ_CD from the cut sum):
    - d_p = 30 nm, pitch 15 nm, CD 5 nm: 9.1 nm and 32.5 nm;
    - d_p = 50 nm, pitch 20 nm: 11.6 nm and 25.0 nm.

    The full periodic sum stops in both cases with "blurred away" or "no edges".
  - With σ_sig = 30 nm (contract range up to 2 µm, not a slider of this panel), the cut sum gives CD 26.2 nm and σ_CD 334 nm,
    where the full sum stops.
  - The shown values are absurd (σ_CD larger than the pitch), so a reader is warned indirectly. Still, the code does not do what
    the sentence says once σ_b ≳ pitch/2.
  - Fix in code: sum until the Gaussian tail is negligible (|k|·p > |x| + 8σ_b + p). Or say "the two nearest periods on each side".
- **BSE counted as Poisson.** In (7.3), m = η_c(δ + η) treats the backscattered electrons as Poisson too. A primary backscatters
  at most once, so their count is Bernoulli, with variance q(1 − q) and q = η_cη = 0.12. That lowers Var N per primary by
  q² = 0.0144. At the floor (m = 0.671) this is 1.3 % in variance and 0.6 % in σ. Negligible, but not stated. The text's caveat
  covers only the secondaries.
- **The key result's "four times the dose"** holds for the dwell-time and current routes. Halving σ_CD through N, the number of lines,
  leaves the dose per area unchanged. But N is also the pixels per line, so it multiplies the frame time N²t_d by 16, not 4.
- **Notation.** N is the count of a pixel in (7.3) and the number of lines in (7.4)–(7.6); (7.4) has both (Var N_i / N). b is a
  wall end in (7.2) and the floor level in §7.4. Neither is wrong, but both are easy to misread.
- **Pixels are point samples.** The profile is sampled at pixel centres (`setup`, line 53), not averaged over the pixel. That
  is fine at Δx = 1 nm against σ_b = 4.50 nm. The text does not say it.
- **"Sharp" in C7** is d_p = σ_s = 0.1 nm with 0.25 nm pixels, not a vanishing probe. 21.040 against 21.048 nm, as stated.

## Equations

| eq. | content | verdict |
|---|---|---|
| (7.1) | δ(1/sin β − 1) h tan β = δh(1/cos β − tan β) | **verified**. Secant law with θ = 90° − β: cos θ = sin β (SymPy), so the wall yield per projected length is δ/sin β. Excess × w: the difference of the two sides is 0 (SymPy). Units: yield × length (m). Limits: β → 0 gives δh, with series δh(1 − β + β²/2 …); β → 90° (flat) gives 0. The derivative δh(sin β − 1)/cos²β ≤ 0, so steeper walls give more excess. Default 22.0 nm (δ = 0.76, h = 30 nm, β = 2°); fin 38.0 nm. 1/sin 2° = 28.7, "many times the flat value", right. |
| (7.2) | Y(x) = δ + η + Σ δh(1/cos β − tan β)/w [Φ((x−a)/σ_b) − Φ((x−b)/σ_b)] | **verified**. ∫ₐᵇ g_σ(x − x′)dx′ = Φ((x−a)/σ) − Φ((x−b)/σ) (SymPy, exact). The blurred excess integrates to the excess of (7.1). Limit w → 0: the zero-width limit is the excess × Gaussian (SymPy). The code's branch for b − a < 10⁻⁶σ_b is this limit. Far from walls, Y → δ + η. Dimensionless. Geometry as in the code: walls [±CD/2 − w/2, ±CD/2 + w/2], bottom width CD + w = 21.048 nm. Periodic images: the code adds only k = −2…2 (see remarks). |
| inline | σ_p = d_p/2.355 for a round Gaussian of FW50 d_p | **verified**. Enclosed fraction 1 − e^(−R²/2σ²) = ½ gives R₅₀ = σ√(2 ln 2), so the diameter is 2.35482σ (SymPy). The marginal of an isotropic 2-D Gaussian along any line has the same σ (SymPy). Chapter 6's σ_sig is the rms of one lateral coordinate (`ch06.js` line 21), so it is the right σ_s. Treating chapter 5's FW50 probe as Gaussian is the stated model choice. |
| inline | σ_b² = σ_p² + σ_s² | **verified**. The convolution of two Gaussians (SymPy). Default σ_p = 2.2507 nm, σ_b = 4.5029 nm. |
| inline | Φ by A&S 7.1.26, error 1.5×10⁻⁷ | **verified**: coefficients as A&S. Largest |erf error| 1.394×10⁻⁷ at x = 0.045 (grid step 10⁻⁴, −6…6). Error in Φ is half that. |
| (7.3) | ⟨N⟩ = n̄m, Var N = n̄(m + m²) | **verified**. From the generating function G(t) = exp(n̄(e^(m(t−1)) − 1)): mean n̄m, variance n̄m(m + 1) (SymPy). Same result as the law of total variance. Limit m → 0: Var → ⟨N⟩ (plain Poisson). Fano factor 1 + m, "amplified", right. Poisson statistics of the yield: an assumption, stated as one. BSE as Poisson: see remarks (−1.3 % in variance). |
| inline | n̄ = I_p t_d/e; D = I_p t_d/Δx² | **verified**. n̄ = 6.2415. D = 1 C m⁻² = 100 µC cm⁻² (sympy units). |
| inline | SNR = (N_edge − N_floor)/√Var N_floor | **verified** as what the code computes (lines 111–113): maximum of the expected profile minus the pixel at the period edge (x = −19.5 nm), over that pixel's one-line standard deviation. |
| (7.4) | σ²_CD = Σ(∂f/∂S_i)² Var N_i/N | **verified** as first-order propagation for independent pixels (shot noise is independent from pixel to pixel). Units m²/count² × count² = m². Crossing derivatives (SymPy): ∂x_c/∂S_i = Δx(T − S_j)/(S_i − S_j)² and ∂x_c/∂S_j = Δx(S_i − T)/(S_i − S_j)². They sum to Δx/(S_i − S_j) = 1/\|S′\|, and ∂x_c/∂T = −1/S′. So "near a crossing the derivative is 1/\|S′\|" is the sum over the two pixels; each pixel alone carries the share f or 1 − f. Measured at the default: 0.986 and 0.276 nm/count, sum 1.261 = 1/0.793. Floor pixels: −0.1262 each = −2 · ½ · (1/10) · 1.261, right. "Most of them are zero": **wrong, because** 20 of 40 are non-zero (summary item 4). |
| (7.5) | σ_CD ∝ (I_p t_d N)^(−1/2) | **verified**. The rule is invariant under S → cS (crossing difference 0 in SymPy; b, peak and T scale alike), so ∂f/∂S ∝ 1/n̄. With Var ∝ n̄ and the 1/N, every term ∝ 1/(n̄N). Slopes in Chromium: t_d −0.49999999995, I_p −0.49999999995, N −0.5. The 10⁻¹⁰ comes from the absolute 10⁻¹² in the step h. Holds with d_p fixed, as in this chapter's panel (no coupling of I_p to d_p in `app.js`). |
| (7.6) | Ṅ_m = 1/(N²t_d + t_ov) | **verified**. Units s⁻¹ (3508.04 h⁻¹ at the default, sympy units). Limit t_ov → 0: 1/(N²t_d) = 1.373×10⁵ h⁻¹. As code line 116. |
| key result | halving σ needs 4× electrons, 4× time or current, 4× dose | **verified** for the t_d and I_p routes; the N route differs (remarks). |
| Problem 1 | edge scatter σ_S/\|S′\| for a fixed threshold; "more than √2 times" for the width | **first part verified** (x_c = x₀ − δS/S′ to first order). **Second part wrong at the default, because** the module gives 1.29× (fin 1.34×; blunt probe 1.50×). Summary item 2. |
| Problem 2 | optimum dwell at fixed σ_CD, "why the answer depends on t_ov" | **wrong, because** time per site = N·t_dN + t_ov rises linearly in N at fixed σ, so the optimum is the smallest N, independent of t_ov (summary item 1). |
| Problem 3 | current for σ_CD = 0.1 nm, and its dose | **verified as solvable**. I_p = 10 pA × (0.27135/0.1)² = 73.6 pA, dose 736 µC cm⁻² (EP 0.100 nm; that run's MC 0.107 nm). |

## Numbers (page value read from the DOM; recomputed with the page's own modules in Chromium)

All 29 spans match the recomputation, formatted with the page's `fmt`.

| key | page | recomputed (raw) | verdict |
|---|---|---|---|
| d_n | 6.2 | 6.241509 | verified (I_p t_d/e) |
| d_dose | 100 µC cm⁻² | 100.0000 | verified |
| d_snr | 1.9 | 1.878237 | verified |
| d_rows_e | 3200 | 3195.65 (= n̄ × 512) | number **verified**; the wording "collects … electrons" is **wrong, because** these are landed beam electrons. Collected: 2145 (floor) to 4689 (edge peak). Summary item 3. |
| cd_sharp | 21.04 nm | 21.040263 | verified (d_p = σ_s = 0.1 nm, Δx = 0.25 nm) |
| cd_bottom | 21.05 nm | 21.047623 (= 20 + 30 tan 2°) | verified |
| d_cdm | 28.6 nm | 28.562563 | verified |
| d_bias | 8.6 nm | 8.562563 | verified |
| d_sig (twice) | 0.27 nm | 0.271353 | verified |
| d_sigmc | 0.29 nm | 0.285016 (1000 repeats, seed 7072026) | verified as the code's output. The converged value (40 000 repeats) is 0.278 nm, which would show as 0.28. The page's value is 2 % high, within the ±2.2 % of 1000 repeats. |
| slope_t | −0.500 | −0.49999999995 | verified |
| t10_sig | 0.086 nm | 0.0858093 | verified |
| t10_ratio | 3.16 | 3.16227766027 | verified (√10 = 3.16227766017; equal to 10 digits, not just "close") |
| t10_snr | 5.9 | 5.939508 | verified (= 1.8782 × √10) |
| t10_dose | 1000 µC cm⁻² | 1000.000 | verified |
| t10_mph | 2900 | 2852.29 (= 3600/(512² × 1 µs + 1 s)) | verified |
| fin_snr | 4.2 | 4.244309 | verified |
| fin_cdm | 24.6 nm | 24.644891 | verified |
| fin_sig | 0.19 nm | 0.193594 | verified (MC: 0.2076 with 1000 repeats, 0.2015 with 40 000) |
| c5_dp | 5.3 nm | 5.317448 (`EB.ch05` at its defaults) | verified |
| bl_cdm | 29.0 nm | 28.986474 | verified |
| bl_sig | 1.9 nm | 1.885816 | verified as first-order propagation. The module's own MC gives 1.678 nm (40 000 repeats: 1.674), 11 % lower. Remarks. |
| d_tframe (twice) | 26 ms | 26.2144 | verified |
| d_mph | 3500 | 3508.04 | verified |
| d_mph_noov | 1.4 × 10⁵ | 137 329.1 | verified |
| amat_us | 36 µs | 36 | verified (arithmetic) |
| amat_per_image | 730 | 728.18 | verified (arithmetic). With the model's 1 s overhead per site, a site would need 28 500 widths, a stronger form of the same point. |

Check table (§7.7), read from the DOM and recomputed independently:

| check | page | verdict |
|---|---|---|
| C1 | compound Poisson, n̄(m + m²) | verified (generating function, see (7.3)) |
| C2 | R₅₀ = σ√(2 ln 2), d = 2.355σ = FWHM | verified |
| C3 | (7.1) identity and limit δh | verified |
| C4 | largest difference 1.4×10⁻⁷ | verified (1.394×10⁻⁷) |
| C5 | slopes −0.500 (t_d, I_p, N_px) | verified (Chromium, same points) |
| C6 | 0.271/0.285, 0.086/0.091, 0.858/0.873, 0.543/0.549, 0.194/0.208 nm | verified: ratios 1.050, 1.062, 1.017, 1.012, 1.072, all 1000 repeats valid. Converged ratios (40 000 repeats): 1.025, 1.013, 1.042, 1.012, 1.041. "MC itself carries about 2 %": 1/√(2·999) = 2.2 %, right. |
| C7 | 21.040 against 21.048 nm; default 28.56 nm | verified |
| C8 | n̄ = 6.242, D = 100.0 µC cm⁻² | verified |
| parity | "agree to about 10⁻¹⁰" | verified. Largest relative difference 2.3×10⁻¹⁰, in σ_CD (finite differences amplify last-bit differences), case d_p = 20 nm, σ_s = 10 nm, pitch 100 nm. σ_CD_mc agrees to 1.2×10⁻¹¹ or better, on 8 cases. |

Quoted and literal values:

| item | verdict |
|---|---|
| "captures 95% of back-scattered electrons" (Applied Materials, PROVision 10 page) | **unverifiable, because** the product page returned 403 and the other routes were refused (see header). The page uses it only as a quoted claim, not as an input; the contract agrees. |
| "up to 100 million accurate, actionable measurements per hour", cold-field-emission column | **unverifiable**, same reason. The arithmetic built on it is verified above. |
| dose of ~100 µC cm⁻² "the order of the dose that exposes an electron-beam resist" | **unverifiable, because** no source is given or opened. It is plausible: resist doses run from a few to thousands of µC cm⁻² depending on resist and voltage. |
| defaults δ = 0.76, η = 0.24, σ_s = 3.9 nm "chapter 6's silicon at 800 V" | verified against chapter 6's module at its defaults (0.7618, 0.2435, 3.941 nm, from my chapter 6 run). The chapter 6 files are being changed by another session in the working tree, and that was not re-run here. |
| SNR 1.9 "the edges barely stand out"; floor not flat at 40 nm pitch | verified: the yield at the space centre is 1.342 against the flat 1.000, so neighbouring walls overlap as stated |

## Numerical method: note against code (physics/ch07.js)

| note says | code | verdict |
|---|---|---|
| walls lean by β, project to w = h tan β; line width CD at half height | `yieldAt` lines 36–46: walls [c ∓ (cd ± w)/2] | matches |
| flat δ + η, excess spread over w and blurred by σ_b, Φ via A&S 7.1.26 | lines 28–33, 38–43; zero-width branch for b − a < 10⁻⁶σ_b | matches |
| "the walls of the neighbouring lines are added too" | k = −2…2 only (line 39) | matches at the default; **not** once σ_b ≳ pitch/2 (remarks) |
| σ_p = d_p/2.355, σ_b² = σ_p² + σ_s² | line 50: d_p/(2√(2 ln 2)) | matches |
| n̄ = I_p t_d/e; mean n̄m, variance n̄(m + m²), m = η_cY | lines 51–55 | matches; profile point-sampled at pixel centres, n = round(p/Δx) = 40 (not stated) |
| N lines averaged, variance / N | line 92 (`/ N`), line 95 (`z / N`) | matches |
| floor = mean of the middle half of the space | line 63: \|x\| ≥ p/2 − (p − CD)/4 (10 pixels at the default) | matches |
| peak = mean of 3 pixels around the maximum (of each half) | lines 66–68, indices clamped at the ends | matches |
| threshold half-way; walk outwards; first point below; linear interpolation | lines 68–72 (strict <) | matches |
| CD = distance between the edges | line 74, line 84 | matches |
| derivatives by perturbing each pixel of the noise-free profile and rerunning the rule | lines 87–93, forward difference, h = 10⁻⁶\|S_i\| + 10⁻¹² | matches |
| "repeats the whole measurement 1000 times on noisy profiles", standard deviation of the widths | lines 95–107: NMC = 1000, seed 7072026, Box–Muller Gaussian noise of variance Var/N on the *averaged* profile; sample s.d. with ok − 1; failed repeats dropped (none failed at the six settings checked) | matches. The Gaussian (not compound-Poisson) noise is stated under "What the model leaves out", but not in §7.5. |
| SNR of one line | lines 109–113 | matches |
| time per site N²t_d + t_ov | line 116 | matches |
| dose I_p t_d/Δx² | line 117 | matches |
| stops when the profile varies by < 0.1 % | line 83 | not in the text (only in `LITERALS`); fine |
| ref/ch07.py mirrors the module | read side by side; same branches, same RNG via `ref/ch06.rng`, `Math.round` reproduced as floor(x + 0.5) | matches; parity 2.3×10⁻¹⁰ |
