# Chapter 8 "The whole machine": derivation and number check

Reviewer's check of `public/portfolios/electron-beam/index.html`, `#ch08`. Sources:
- text `portfolios-src/electron-beam/text/ch08.py`;
- module `physics/ch08.js`, which calls `ch02.js`, `ch04.js`, `ch05.js` and `ch07.js`;
- checks `derive/ch08.py` and `derive/ch08_probe.cjs`;
- data `data/ch08/derive_results.json`.

Date: 9 November 2026. Scope: chapter 8 only. No repository file other than this one was changed. No repository script was
run (`derive/ch08.py` writes `data/ch08`, so I did not run it). I did not read `referee-ch08.md` or the plan.

## How it was checked

- **Equations.** I re-derived (8.1) and (8.2) and the chapter's other formulas in SymPy 1.14 with my own script, `sym8.py`.
  It covers:
  - the defocus disc and its FW50;
  - the quadrature blur rule and its limits;
  - the current at fixed condensers;
  - the probe's scaling with landing voltage and C_c;
  - the counting-law sensitivities, the dose and the dose-limited current, with units from `sympy.physics.units`;
  - Problems 1 to 3.

  All 24 symbolic checks pass.
- **Numbers.** I recomputed every `[data-n^="ch08."]` span of `#ch08` in headless Chromium. That is 71 spans with 63 different
  keys. The run used Playwright and `/usr/bin/google-chrome`, with the built page's own modules:
  - `EB.ch08.compute` on `EB.core.withDefaults(EB.contract, …)`;
  - the one-error-at-a-time runs, done as the probe does them;
  - the traced defocus through `EB.ch04.paraxial`.

  Each value was formatted with `EB.core.fmt` at the `sig` set in `text/ch08.py` and compared with the DOM text: **71 of 71
  identical**. There were no page errors. The only console error was a font CORS refusal under `file://`. I also read the check
  table, the equation numbers (8.1) and (8.2) and both `\eqref`s from the DOM; they resolve correctly.
- **Probes of the prose.** Further runs in Chromium, from the same modules:
  - α_opt and the source outputs against each input;
  - the probe against tip radius with the current held fixed;
  - σ_CD against V_land with each chapter 6 yield frozen in turn;
  - the window on finer lines (41 voltages at 1 pA, 27 currents at 5 kV, 25 V steps from 1.95 to 2.35 kV);
  - chapter 6 run fresh at 800 V;
  - the W4 grid interpolation on 40 draws for all four source quantities;
  - timings.
- **Method.** I read `physics/ch08.js` against §8.1–§8.5 sentence by sentence (table D below).
- **Sources.** Only one claim needed an outside source: the resist-dose remark. The MediaWiki API refused a plain request
  (rate limit). The same API answered with a generic user agent (article "Electron-beam lithography"). No web-search tool is
  available to this agent.

Scripts and outputs are in the scratchpad, not in the repository:
`/tmp/claude-0/-home-user-SiteTest/c8b76f47-83f6-5259-bec8-4485c7f5a448/scratchpad/ch08d/work/`
- `sym8.py`: the derivations.
- `run8.cjs`: all page numbers, the DOM comparison, W1–W4 redone. Output in `chromium_out.json`.
- `run8b.cjs`: the probes of the prose. Output in `chromium_out_b.json`.
- `run8c.cjs`: the window's jump and its monotonicity.
- `run8d.cjs` and `run8e.cjs`: the W4 grid on 40 draws.

## Summary

Every number on the page is what the page's code computes (71 of 71). Both numbered equations are right, with the right units
and limits. (8.2) is in fact exact to first order: the paraxial ray depends only on B²/V*. The traced ray also matches the
second-order term −3C_cε².

What is wrong is mostly the prose around the numbers.

1. **Example 8.3 says "Higher voltage helps too in this model: at 1 pA, 0.45 nm at 1.4 kV".** The number it cites contradicts
   it: 0.45 nm at 1.4 kV is worse than the 0.37 nm at 0.5 kV in the sentence before. At 1 pA, σ_CD falls to 0.33 nm at
   0.63 kV, rises to 0.57 nm at 2.13 kV, and only then falls, to 0.063 nm at 5 kV.
2. **"More current always helps"** is false in 5 of the 182 current steps of the map, all at the top right (≥ 3.5 kV,
   ≥ 0.34 nA). At 5 kV, σ_CD is smallest, 0.0057 nm, near 0.35–0.45 nA. It rises to the quoted 0.0066 nm at 1 nA because the
   probe grows from 1.2 to 2.3 nm.
3. **"The sharp core … narrows with voltage"** is true only above about 1 kV. The stored core width grows from 1.26 nm at
   0.5 kV to 2.31 nm at 1 kV.
4. **"The landing voltage enters with 0.52, through the falling secondary yield and the growing halo."** At 800 V the main cause
   is the growing core width (stored core: S = +0.76 against V). Freezing it turns σ_CD's sensitivity from +0.52 to −0.43.
   Freezing the halo changes it only to +0.517, and freezing δ to +0.37.
5. **"(check W4: within 0.5 % of direct runs)"** holds only for the 5 draws W4 looks at (0.46 %).
   - Over the 38 in-grid draws among the first 40, B_r is off by up to 0.70 %.
   - Draws beyond ±3σ are clamped to the grid edge without saying so: 2 of the 300 Monte Carlo draws, off by 1.8 % and 2.4 %.
6. **"Each is normal"**: the tip radius is drawn log-normal, not normal (ln r_t has standard deviation ln 1.03). The grid also
   clamps r_t and p at ±3σ.
7. **"With the condensers left at their setting the current scales as B_r d_v² … at the same magnification"** clashes with the
   page's rule that the aperture is always set to α_opt. At a fixed setting the current also scales as α². The module leaves out
   the α², and so changes the magnification implicitly (chapter 5's d_I ∝ d_v/α). This matters because α_opt itself moves:
   S(α_opt, r_t) = 0.36, S(α_opt, WD) = −0.44, S(α_opt, V_land) = 0.25.
8. Smaller items:
   - "loses some 15 %" is 14.2 % in the module.
   - "−0.48 … a little less than −0.5": −0.48 is above −0.5.
   - "These numbers equal those of the separate chapters (W1 and W2)": δ and f_core do not equal chapter 6 at 800 V. They are
     interpolated: 0.747 against a fresh 0.757 ± 0.009, and 85.5 % against 86.2 %.
   - The key result says "exponents near one half"; the lens half-width gives 0.07 and V_land on the probe −0.75.
   - "300 µC cm⁻², about the dose that exposes a sensitive resist": a sensitive commercial resist needs less than 10 µC cm⁻².
     300 µC cm⁻² is the PMMA class.
9. **Not a statement on the page, but visible in its map.** σ_CD jumps by 25 % between 2.125 and 2.150 kV (1 pA: 0.574 to
   0.428 nm; 10 pA: 0.174 to 0.139 nm between 2.10 and 2.15 kV). Over the same step, every input chapter 8 hands to chapter 7
   (d_p, δ, η, core, f_core, halo, CD_meas) changes smoothly by about 1–3 %. The step is inside chapter 7's σ_CD. I did not
   check chapter 7 here. The map's 2.5–3 kV wiggle (0.23 to 0.31 to 0.095 nm at 1 pA) has the same look.

## A. Equations

| # | Equation / formula | Verdict |
|---|---|---|
| (8.1) | S_yx = (x/y)∂y/∂x = ∂ln y/∂ln x | verified. SymPy: substitute x = e^U, identical. Dimensionless. For y = y₀xⁿ, S = n (the page's sentence). |
| (8.1), method | the module's (ln y(1.01x) − ln y(0.99x)) / ln(1.01/0.99) | verified. Exact for any power law. For y = e^{cx} it gives cx(1 − h²/3 + …), so the error is O(h²) = 3·10⁻⁵ relative at h = 1 %. For N_px the steps are rounded to 517 and 507, and the code divides by the actual ln(517/507). |
| (8.1), "S = −0.5 … half a per cent less", "S = 16 … sixteen per cent more" | readings of (8.1) | verified, to first order. |
| (8.2) | Δz = 2C_c ε | verified. The paraxial equation r″ = −(e/8mV*)B²r depends on B²/V* only, so B → B(1+ε) is exactly V* → V*/(1+ε)². Then ΔV*/V* = −2ε + 3ε² − …, and with C_c = focus shift per relative change of V* (chapter 4 computes it image-side: \|Δr\|/(2d)·M), Δz = 2C_cε − 3C_cε² + …. Units: m = m · 1. Limits: ε → 0 or C_c → 0 give Δz → 0. Second order predicts traced/model = 0.999850 at ε = 10⁻⁴; the traced ray gives 0.999867. ε = −10⁻⁵ traces to −56.9526 nm, so the relation is symmetric. |
| unnumbered | uniform disc of radius α\|Δz\| | verified. Paraxially a ray of slope α is at α Δz at distance Δz from focus (tan α ≈ α). A uniformly filled aperture maps linearly, so the disc is uniform. |
| unnumbered, Problem 2 | FW50 of a uniform disc = √2 ρ (half inside ρ/√2) | verified. ∫₀^R 2πs/(πρ²) ds = ½ gives R = ρ/√2. |
| unnumbered | d_p → √(d_p² + 2α²Δz²) (code line 48) | verified as the stated rule. It is the quadrature sum of d_p and √2 α\|Δz\|. Limits: Δz → 0 gives d_p; d_p → 0 gives the disc FW50. For small Δz the growth is α²Δz²/d_p. From that, the lens drift alone (Δz sd 56.95 nm) gives a probe sd of √2·α²σ²/d_p = 0.084 nm (page 0.087, from 300 draws); the wafer alone gives 0.010 nm (page 0.008). "Exact for neither shape": agreed. |
| unnumbered | I ∝ B_r d_v² at fixed condensers; source image ∝ d_v | **wrong as stated together with α = α_opt.** SymPy: I = B_r V*(πM²d_v²/4)(πα²) scales as B_r d_v² only at fixed M **and** fixed α; it also scales as α². The module re-optimises α at every call and leaves out α² (line 46). Chapter 5's d_I = √(4I/(π²B_prV*α²)) then scales as d_v/α, not d_v, so M is not "the same magnification". At fixed α both statements hold (verified symbolically). In numbers, a column truly at a fixed setting would show S(I, r_t) ≈ −15.29 + 2·0.36 = −14.6, S(I, WD) ≈ −0.88, S(I, V_land) ≈ +0.49 and S(I, a) ≈ −0.13, against the table's −15, 0, 0, 0. This is not self-consistent, because α_opt depends on I, but it shows the size. The conclusions survive. The sentence should say that the source acceptance, not the condensers, is held fixed. |
| unnumbered | apex field F = V_ex/(k r_t) | verified against `ch02.js` line 165 (k_f = 5, so F = 4 V nm⁻¹ at the defaults). |
| unnumbered | "field emission rises with the field almost as steeply as an exponential" | verified. Murphy–Good at 0 K, φ = 4.500 eV, F = 4 V/nm: d ln J/d ln F = 2 + (bφ^{3/2}/F)(1 − f/6) − 2f t′/t = 17.46. The module gives S(B_r, V_ex) = 16.36 (B_r = e j_t0/π, `ch02.js` l. 153, the current density per unit transverse energy, which rises a little more slowly than J) and S(B_r, r_t) = −16.36. d_v (S = 0.53 to r_t, −0.03 to V_ex) gives the rest: −16.36 + 2·0.53 = −15.29 and 16.36 − 2·0.035 = 16.29, which are the table's −15 and 16. |
| unnumbered | probe's −0.75 to V_land "(shorter wavelength, smaller relative energy spread)" | verified. With diffraction and source image ∝ V^{−1/2}/α and chromatic ∝ α/V, the minimum is ∝ V^{−3/4} (SymPy). At the default optimum d_A = 2.70, d_C = 2.91, d_I = 0.47 and d_S = 0.49 nm, so the module's −0.7498 is this law. The same algebra gives d_p ∝ C_c^{1/2}: S(d_p, WD) = 0.4378 equals ½S(C_c, WD) = 0.4377, and S(d_p, a) = 0.0672 equals ½·0.1356 = 0.0678. |
| unnumbered (W5) | σ_CD ∝ (t_d N)^{−1/2}; rate = 1/(N²t_d + t_ov), so S_td = −t_f/(t_f + t_ov) and S_N = −2t_f/(t_f + t_ov) | verified. −0.025545 and −0.051090 (module −0.025544, −0.051088). Rate 3508.0 per hour. |
| unnumbered | dose = I_p t_d / p_x²; dose-limited current I = D_max p_x²/t_d | verified with units. 10 pA × 100 ns / (1 nm)² = 1 C m⁻² = 100 µC cm⁻². 300 µC cm⁻² × (1 nm)² / 100 ns = 3.0·10⁻¹¹ A = 30 pA. |
| Problem 1 | S = a, b for y = x₁^a x₂^b; relative error √(a²s₁² + b²s₂²) | verified, to first order in s. For the asked estimate: 15.29 × 3 % = 46 % linear. The log-normal current from the Monte Carlo's draw would give √(e^{(15.29 ln1.03)²} − 1) = 48 %. |
| Problem 3 | extraction voltage restoring I after r_t × 1.05 | verified as answerable. The module (bisection in Chromium) gives V_ex = 1046.87 V. The table's estimate 1000·1.05^{15.29/16.29} = 1046.86 V agrees. |

## B. Numbers (all recomputed in headless Chromium from the built page; "shown" is the DOM text)

| key | shown | page code gives | verdict |
|---|---|---|---|
| o_aopt | 8.67 mrad | 8.66930 | verified |
| o_dp | 4.11 nm | 4.11309 | verified (W1: the chain by hand gives the same to 6·10⁻¹⁴) |
| o_delta | 0.75 | 0.74725 | verified as the module's value. The claim that it equals chapter 6's value is wrong: see C1. |
| o_fcore | 86 % | 85.516 | verified (chapter 6 run fresh at 800 V: 86.2 %) |
| o_cdm | 26.3 nm | 26.3462 | verified |
| o_cd | 0.11 nm | 0.113159 | verified (by hand 0.1131588393, difference 2·10⁻¹¹ relative) |
| o_dose | 100 µC cm⁻² | 100.000 | verified (units checked in SymPy) |
| o_mph | 3500 per hour | 3508.04 | verified (2 significant figures) |
| s_dp_r_t | −0.31 | −0.31381 | verified |
| s_I_r_t (×2) | −15 | −15.2923 | verified |
| s_cd_r_t (×2) | 7.3 | 7.32823 | verified |
| s_mph_r_t | 0 | 0 | verified (exactly 0 by construction) |
| s_dp_V_ex | 0.34 | 0.33784 | verified |
| s_I_V_ex (×2) | 16 | 16.2939 | verified |
| s_cd_V_ex | −7.8 | −7.80474 | verified |
| s_mph_V_ex | 0 | 0 | verified |
| s_dp_p | 0 | 0 | verified. Pressure changes only B_r (`ch02.js` line 243), and d_I ∝ √(I/B_r) is unchanged, so the result is exactly 0. |
| s_I_p | −0.021 | −0.020584 | verified |
| s_cd_p | 0.010 | 0.010292 | verified |
| s_mph_p | 0 | 0 | verified |
| s_dp_V_land (×2) | −0.75 | −0.74984 | verified |
| s_I_V_land | 0 | 0 | verified (by construction; but see A, current at fixed condensers) |
| s_cd_V_land (×2) | 0.52 | 0.52309 | verified as a number; the explanation in the text is wrong (C4) |
| s_mph_V_land | 0 | 0 | verified |
| s_dp_I_p | 0.023 | 0.023310 | verified |
| s_I_I_p | 1.0 | 1.00000 | verified |
| s_cd_I_p (×2) | −0.48 | −0.47639 | verified; the wording around it is wrong (C5) |
| s_mph_I_p | 0 | 0 | verified |
| s_dp_WD (×2) | 0.44 | 0.43781 | verified |
| s_I_WD | 0 | 0 | verified |
| s_cd_WD | 0.44 | 0.44346 | verified |
| s_mph_WD | 0 | 0 | verified |
| s_dp_a_lens | 0.067 | 0.067189 | verified |
| s_I_a_lens | 0 | 0 | verified |
| s_cd_a_lens | 0.068 | 0.068061 | verified |
| s_mph_a_lens | 0 | 0 | verified |
| s_dp_t_d | 0 | 0 | verified |
| s_I_t_d | 0 | 0 | verified |
| s_cd_t_d | −0.50 | −0.50000 | verified |
| s_mph_t_d (×2) | −0.026 | −0.025544 | verified (closed form −0.025545) |
| s_dp_N_px | 0 | 0 | verified |
| s_I_N_px | 0 | 0 | verified |
| s_cd_N_px | −0.50 | −0.50000 | verified |
| s_mph_N_px | −0.051 | −0.051088 | verified (closed form −0.051090) |
| s_dp_eta_c | 0 | 0 | verified |
| s_I_eta_c | 0 | 0 | verified |
| s_cd_eta_c | −0.21 | −0.21473 | verified |
| s_mph_eta_c | 0 | 0 | verified |
| def_dz | 57.0 nm | 56.9511 (traced); 2C_cε = 56.9519 | verified. The span shows the traced value; the formula gives the same to 3 figures. |
| tol_dp | 0.10 nm | 0.100749 | verified |
| tol_p95 | 0.17 nm | 0.166873 | verified. The code takes sorted[⌊0.95·300⌋] = sorted[285], so 14 of 300 draws (4.7 %) lie above it. "In 5 % of them" is fine at this rounding. |
| tol_yield | 87 % | 86.667 (260 of 300) | verified |
| te_rt_yield | 89 % | 89.0 | verified |
| te_rt_dp | 0.038 nm | 0.038261 | verified. "Through the current" is right: with the current held fixed, S(d_p, r_t) is +0.043 instead of −0.314. |
| te_NI_dp | 0.087 nm | 0.087250 | verified (analytic estimate 0.084, see A) |
| te_z_dp | 0.008 nm | 0.0082380 | verified |
| pw_ll | 0.37 nm | 0.365267 | verified |
| pw_lh | 0.019 nm | 0.019153 | verified |
| pw_hl | 0.063 nm | 0.062635 | verified |
| pw_hh | 0.0066 nm | 0.0065988 | verified as a number. It is not the best value at 5 kV (0.0057 nm near 0.35–0.45 nA; C2). |
| pw_l_mid | 0.45 nm | 0.445061 | verified as a number. It disproves the sentence it supports (C3). |
| V_mid | 1.4 kV | 1.44713 (500·10^{6/13} V) | verified |
| I_dose | 30 pA | 30.000 | verified. Note: `text/ch08.py` types it as the literal `3.0*1e-18/1e-7*1e12`, not from the stored inputs (dose_max, FIX.px, t_d), so it will not follow a change of defaults. `draw()` line 128 likewise hard-codes p_x² = 10⁻¹⁸ instead of `FIX.px²`. The values are equal today. |
| literal "2000 electrons per point between 0.5 and 30 kV" | | `data/ch06/mc_runs.json` note "N = 2000 electrons each"; table E 0.5–30 keV | verified |
| literals 3 %, 0.5, 10⁻⁵, 20 nm, 0.15 nm, 300 µC cm⁻², 300 draws, 5 × 5, 14 by 14, 0.5–5 kV, 1 pA–1 nA, 800 V, 10 pA, 100 ns, 512, 1 nm pixels, 20 nm line, 10⁻⁹ Pa, an hour | | contract defaults (tol_rt 0.03, tol_p 0.5, tol_NI 1e-5, tol_z 2e-8, spec_cd 1.5e-10, dose_max 3.0 C m⁻², V_land 800, I_p 1e-11, t_d 1e-7, N_px 512, cd 2e-8, p 1e-9, t_clean 3600); NTOL 300, NPW 14, FIX.px 1e-9, t_ov 1 | verified |
| "one-second overhead per site" | | FIX.t_ov = 1 s; frame 26.2 ms | verified |
| "some 15 %" (blunting by 1 %) | | module: −14.18 % for r_t × 1.01; power law at S = −15.29: −14.1 % | **wrong, because** 15 % is the linearised S. The module's change is 14 %. |
| "fifteen to sixteen times" | | 15.29 and 16.29 | verified |
| "only three times the default current" | | 30 / 10 | verified |
| "(check W4: within 0.5 % of direct runs)" | | 0.46 % on the 5 checked draws; 0.70 % worst over the 38 in-grid draws among the first 40; 1.84 % and 2.42 % for draws 6 and 20, which lie beyond 3σ and are clamped | **wrong, because** the bound holds only for the 5 draws W4 samples. Correct: within 0.7 % inside the grid, up to 2.4 % for the clamped draws. W4 also tests only B_r; dE, dE50 and d_v are within 0.12 % over the same 40 draws. The interpolation errors are almost all negative (mean −0.35 % over the 38 in-grid draws): log-bilinear interpolation is biased low here. |
| "takes up to a second per setting" (chapter 6) | | 0.042 s at 0.8 kV, 0.40 s at 30 kV in this Chromium | verified as an upper bound (depends on the machine) |
| "Chapter 2 is too slow to run 300 times" | | 29 ms per run, so about 9 s for 300 | verified as a judgement (measured) |
| check table W1–W5 | | redone in Chromium: W1 identical; W2 deviations ≤ 1.9σ (δ at 12 kV); W3 as shown; W4 0.0046; W5 −0.500, −0.500, −0.0255 | verified. Note: W2's detail also lists core and halo, which the pass test does not use (core at 1.2 kV 2.30 against 2.49 nm, halo at 12 kV 425 against 408 nm). |
| equation numbers | (8.1), (8.2) | DOM `#eq-sens8` → (8.1), `#eq-defocus8` → (8.2); both references resolve | verified |

## C. Statements in the prose

| # | Statement | Verdict |
|---|---|---|
| C1 | "These numbers equal those of the separate chapters with the same inputs (checks W1 and W2)" (Example 8.1) | **wrong, because** only the chain's d_p, α_opt, σ_CD, CD_meas, dose and rate are equal (W1, to 2·10⁻¹¹). δ and f_core come from the stored-run interpolation. Chapter 6's module at 800 V gives δ = 0.757 ± 0.009 (shown would be 0.76, not 0.75) and f_core = 86.2 % (page 85.5 %). W2 does not test 800 V and tests agreement within 3σ, not equality. Correct: "equal … (W1); the yields agree with chapter 6's own runs within their statistical error (W2)". |
| C2 | "More current always helps, by the counting law." (Example 8.3) | **wrong, because** σ_CD rises with current in 5 grid steps: 3.51 kV 0.0106 → 0.0135 nm; 4.19 kV 0.0075 → 0.0077 → 0.0112 nm; 5 kV 0.0057 → 0.0058 → 0.0066 nm. On a finer line at 5 kV the minimum is 0.0057 nm near 0.35–0.45 nA, because the probe grows from 1.2 to 2.3 nm. Correct: "more current helps up to a few hundred pA; at the top right the growing probe wins". |
| C3 | "Higher voltage helps too in this model: at 1 pA, 0.45 nm at 1.4 kV." | **wrong, because** 0.45 nm at 1.4 kV is worse than 0.37 nm at 0.5 kV. At 1 pA, σ_CD is 0.365 (0.50 kV), 0.327 (0.63), 0.425 (1.0), 0.445 (1.45), 0.574 (2.13), 0.428 (2.15), 0.230 (2.51), 0.269 (2.81), 0.171 (2.98) and 0.063 nm (5.0 kV). Voltage helps only above about 2.2 kV. In the 14 × 14 grid, σ_CD rises with voltage in 3–8 of the 13 steps of every current column. |
| C4 | "The landing voltage enters with 0.52, through the falling secondary yield and the growing halo." | **wrong, because** at 800 V the main driver is the growing core width (S = +0.76). Freezing each chapter 6 quantity at its 800 V value gives σ_CD's S(V_land) = −0.43 (core frozen), 0.37 (δ), 0.33 (f_core), 0.517 (halo) and 0.544 (η). So the core width contributes about +0.95, f_core +0.19, δ +0.15, and the halo almost nothing. The shrinking probe contributes −0.76 (all yields frozen). Correct: "through the widening core of the secondary signal, helped by the falling yield and core fraction". |
| C5 | "−0.48 for the current, a little less than −0.5 because a larger current also enlarges the probe slightly" | **wrong, because** −0.476 is a little *more* than −0.5; it is smaller in size. The reason given is right: S(d_p, I_p) = +0.023. |
| C6 | "the precision follows the counting law of chapter 7 exactly: −0.5 for the dwell time and for the number of lines (check W5)" | verified (−0.49999998, −0.5000000) |
| C7 | "the field at the apex is V_ex/(k r_t), and field emission rises with the field almost as steeply as an exponential" | verified (see A) |
| C8 | "Through the number of electrons, the same sensitivity reaches the precision: σ_CD answers the tip radius with 7.3" | verified. −0.476 × −15.29 = 7.28; the rest, +0.04, comes through the probe. |
| C9 | "the rate hardly moves at all … the one-second overhead per site dominates" | verified (t_frame 26.2 ms against t_ov 1 s) |
| C10 | Key result: "probe current … fifteen to sixteen times as much as the tip radius or the extraction voltage" | verified |
| C11 | Key result: "The optics and the scan settings follow power laws with exponents near one half." | **wrong in part, because** the scan settings (t_d, N: −0.50), the current (−0.48) and the working distance (0.44) are near ½ in size. The lens half-width gives 0.067 (d_p) and 0.068 (σ_CD), the landing voltage −0.75 on the probe, and η_c −0.21 on σ_CD. |
| C12 | "the tip radius alone … spreads the probe by 0.038 nm, through the current" | verified (S(d_p, r_t) = −0.31 at fixed condensers, +0.043 at fixed current) |
| C13 | "the lens drift alone spreads the probe most … but costs little precision" | verified (σ_CD 95th percentile 0.119 nm against 0.113 nominal; yield 100 %) |
| C14 | "the pressure … does nearly nothing" | verified (probe sd about 10⁻²³ m, which is round-off; σ_CD 95th percentile 0.1145 nm; S(I, p) = −0.021 for a ln-spread of 0.5) |
| C15 | "The sharp core of the secondary signal narrows with voltage while the halo moves out into a uniform background" | **wrong in part, because** the stored core width (Si) is 1.26, 1.76, 2.31, 2.29, 2.09, 0.72 and 0.15 nm at 0.5, 0.7, 1, 1.5, 2, 3 and 5 kV: it widens up to 1 kV and narrows only above about 1.5 kV. The halo part is right (8.6 nm at 0.8 kV, 94 nm at 5 kV). |
| C16 | "(we assume 300 µC cm⁻², about the dose that exposes a sensitive resist)" | **wrong, because** a sensitive resist exposes at far lower dose. Wikipedia, "Electron-beam lithography" (read through the MediaWiki API; a secondary source): the commercial mask resist FEP-171 "would use doses less than 10 μC/cm²". PMMA, a classic *insensitive* resist, is exposed up to about 1000 µC cm⁻². 300 µC cm⁻² is PMMA-class. The value itself is labelled an assumption, which is fine; the comparison is not. |
| C17 | "Lithographers draw a process window: the region of focus and exposure in which a pattern prints within specification" | verified (standard definition; no number) |
| C18 | Checks text: "it adds no physics of its own beyond (8.2) and the current at fixed condensers" | verified with a note: it also adds the √2 α\|Δz\| quadrature blur rule (stated in §8.3) and the interpolations of chapters 2 and 6 |
| C19 | "the coupling of landing voltage and lens (the lens here is computed without a retarding field, chapter 4)" | verified. The code also always computes the lens at V_land = 800 V (line 42), which the text does not say. It is harmless: C_s and C_c at 500, 800, 2000 and 5000 V agree to 1·10⁻¹⁰ relative, because refocusing makes them independent of V. |
| C20 | "Chapter 2's cold tip … the pressure, at 10⁻⁹ Pa an hour after cleaning" | verified (T = 300 K, p = 1e-9 Pa, t_clean = 3600 s) |

## D. Numerical method: text against `physics/ch08.js`, line by line

| Text | Code | Verdict |
|---|---|---|
| chapter 2 gives B_r, ΔE₅₀, d_v | l. 41 `src` → `ch02.compute`; chain uses `s.B_r`, `s.dE`, `s.dE50`, `s.d_v` (l. 46–47) | matches |
| chapter 4 gives C_s, C_c for the lens geometry | l. 42 `ch04.compute({…, V_land: 800})` | matches (fixed 800 V, harmless, C19) |
| chapter 5 gives the smallest probe and its angle; aperture always at α_opt | l. 47–48 `ch05.compute(…, probe_convention 'fw50')`, uses `alpha_opt`, `d_p_opt` | matches |
| chapter 6 not rerun; stored runs (2000 electrons, 0.5–30 kV), interpolated | l. 21 table, l. 34–40: clamped to 0.5–30 keV, interpolated in ln E; log-linear for δ, core, halo; linear for η, f_core | matches (the text does not say which quantities are interpolated linearly and which in log) |
| chapter 7 gives σ_CD, dose, rate | l. 52–53 `ch07.compute(…, {mc: false})` | matches. σ_CD is chapter 7's error propagation, not its Monte Carlo; the text does not say which. |
| current at fixed condensers ∝ B_r d_v²; source image ∝ d_v | l. 46 `Ibeam = I_p·(B_r d_v²)/(B_r d_v²)_nom`; the source image follows from chapter 5's d_I | matches the formula; the physical claim is wrong with α re-optimised (A) |
| sensitivities by central differences of ±1 % | l. 62–68: up ×1.01, down ×0.99, S = Δln y / ln(up/dn); N_px rounded (517/507) | matches |
| table at the defaults, 10 inputs × 4 outputs | l. 24–25, l. 69 (output-major order, read by `sens(o, i)` in text/ch08.py) | matches |
| 300 draws, fixed random numbers | l. 26 `NTOL = 300, SEED = 8082026`; l. 77 mulberry32 + Box–Muller | matches |
| tip radius "relative spread of 3 %", "each is normal" | l. 81, 98: ln r normal, sd ln(1.03) (log-normal r) | **does not match "normal"** (C/summary 6). Also not stated: clamping beyond ±3σ (l. 88; expected 1.6 draws in 300, actually 2). |
| ln pressure spread 0.5 | l. 81, 98 | matches |
| excitation drift 10⁻⁵ → Δz = 2C_cε; wafer height adds | l. 99 `dz = 2·C_c·tol_NI·z_i + tol_z·z_z` | matches |
| 5 × 5 grid of chapter 2, interpolated | l. 78–93: nodes at ±1.5σ, ±3σ; bilinear in ln of B_r, dE, dE50, d_v | matches. The header's "bilinearly in ln r and ln p" is right too: u and v are linear in ln r and ln p. |
| probe grows to √(d_p² + 2α²Δz²) | l. 48 | matches |
| precision worse than X in 5 % of draws | l. 106, 110: sorted[⌊0.95 n⌋] | matches (14 of 300 above) |
| yield = share of draws with σ_CD ≤ spec | l. 102, 110 | matches |
| window: σ_CD over 0.5–5 kV × 1 pA–1 nA, 14 × 14, best angle at each point | l. 72–75: V = 500·10^{i/13}, I = 10⁻¹²·1000^{j/13}, nominal source, Δz = 0 | matches |
| wine = within spec; dashed = dose limit; dot = present setting | l. 124 (wine if v ≤ spec), l. 128–129 (I_max = D_max·10⁻¹⁸/t_d), l. 131–132 | matches (p_x² hard-coded as 10⁻¹⁸) |
| one-at-a-time runs (Example 8.2) | `derive/ch08_probe.cjs` l. 274–279: the other three spreads set to 0 | matches (redone in Chromium, identical to 8 figures) |
| W4 "at the same random draws" | probe l. 257–271: same seed, four draws per sample, first 5 samples, \|z\| < 3 only | matches, but it tests only B_r and only 5 draws (B, "W4") |
