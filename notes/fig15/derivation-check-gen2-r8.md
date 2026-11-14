# Fig. 15 lecture note: derivation and number check, generation 2, round 8

Checked version: `public/scripts/resonant-note.js` at commit 1cc135d (md5 04a7a723…, 14 Nov 2026 09:02 UTC). An earlier dump, taken
before that commit landed mid-check, still had "12 % at s = 3.5" in sections 11 and 14, and a dangling "Counting that half" in
section 6. Commits e066f11 and 1cc135d fixed both, so they are not listed below.

How I checked:
- The note is rendered in headless Chrome (Playwright, `/usr/bin/google-chrome`, page served from `public/`). The result is 1010
  KaTeX blocks, 0 KaTeX errors, 0 unrendered delimiters, 0 page errors, and tags (1)–(32) in order. The text was also produced by
  running the script with a stub DOM, and the two match.
- The NUM block equals a fresh run of `notes/fig15/gen2_numbers.py` (all 326 keys identical), so it is not stale.
- Each equation is re-derived in SymPy (`sym.py` in the scratchpad).
- Each 1D number is recomputed with my own transfer-matrix code, written from scratch with global-x matching and not using
  `tm.py` or `iv.py`.
- Each run-based number is recomputed by reading `2026-11-14/kaggle/index.json` and `2026-11-13/kaggle/index.json` directly.
- The method text is compared line by line with `rt3d2.py`, `rt3d2_run.py`, `file_rt3d2.py`, the inline page script of
  `resonant-tunnelling.html` and `rt3d-view.js`.

## Errors found

| # | Where | What is wrong | Correct result, and how checked |
|---|---|---|---|
| 1 | §13, "Put the exact single-energy T at the same 25 energies into the same sum and the curve goes wrong: its top moves to V_b = 1.125 and its ratio to 16.7, because the peak of T … is seen or missed by chance" | The stored curve `iv[flat].J_exact_single_energy_same_points` in the index was computed with **barriers of height 3, not 2**. `file_rt3d2.py` imports `iv` and calls `iv.T_biased_vec` without setting `iv.V0` or `iv.D`, so the module default `V0 = 3.0` applies. (`exact1d.py` and `gen2_numbers.py` both set `iv.V0 = 2.0`.) Re-running `iv.T_biased_vec` with V0 = 3 reproduces the stored curve to 3×10⁻¹⁷; with V0 = 2 it differs by up to 0.74. | For V0 = 2 the sum over the same 25 energies peaks at **V_b = 0.75**, has its valley at **1.75**, and has a peak-to-valley ratio of **4.8** (4.81). Two independent computations agree: `iv.py` with V0 = 2 gives 4.8108, and my own staircase transfer matrix gives 4.8109. So the single-energy sum peaks where the runs do (0.75) and its ratio is a little above the exact 4.3; it does not "go wrong" to 1.125 and 16.7. The sentence and its conclusion ("the spread is also what lets 25 energies suffice") need rewriting. The stored index value is also wrong, but nothing on the page draws it (no reference in `public/`). |
| 2 | §13, "the peak of T, 0.071 wide" (NUM `fw_b0`) | This is a 0.0005-step grid estimate. The same paragraph gives Γ = 0.0704 for the same zero-bias peak. | **0.0704** (0.070). Bisected FWHM of my own T(E) at V_b = 0 is 0.070405, the same as Γ. |
| 3 | §13, "The products, 1.04 at V_b = 0.875 and 0.74 at 1.25" | These are computed in JS from the rounded NUM values: 0.073 × 14.2 and 0.041 × 18.0. | **1.03 and 0.73**. Unrounded area × supply is 0.07304 × 14.154 = 1.034 and 0.04053 × 18.04 = 0.731 (own staircase, ±0.25 window, same as the script). Only the last digit changes; the argument stands. |
| 4 | §9, "and in the gap, between 1.05 and 1.6, 0.0237 (exact 0.0351)" | The average is taken over the 11 runs at E = 1.10 … 1.60. The script uses band top + 0.1 = 1.055 as the lower limit, so E = 1.05 is not included. | Say "between 1.1 and 1.6". The values are right: 11-run mean 0.02368, exact 0.0351 (own quadrature, converged: 0.03507). |

Everything else checks (tables below). Minor wording point, not an error: §6 says "we give the share with that half added in
brackets", but the d = 2 sentences then give no bracketed values. Those would be 0.0226 at 0.7432 and 0.0262 at 0.7215.

## Equations

| Eq. | Verdict | How |
|---|---|---|
| (1) | verified | Standard TDSE; units ħ = m = 1 give iψ_t = −½∇²ψ + Vψ. E_u = ħ²/ma² and t_u = ma²/ħ are dimensionally consistent. |
| separation argument before (2), including the phase e^{+i∫f dt} | verified | SymPy: the product χ g(y) g(z) with χ obeying (2) gives zero residual in (1). Multiplying by e^{i∫f} adds −f to i ġ/g. |
| (2) | verified | SymPy residual 0 |
| free Gaussian g(y,t) (in-line) | verified | SymPy: residual 0, with and without ħ and m |
| (3) | verified | SymPy: variance of \|g\|² is σ²(1 + (ħt/2mσ²)²). Limits: t = 0 gives σ⊥; large t grows linearly. |
| (4) | verified | χ'' = −2(E − V)χ in flat regions |
| (5) | verified | SymPy solve of the two continuity equations |
| (6), with w and γ referred to the centre | verified | SymPy symbolic product with global-x matching: M₀₀ = w, M₀₁ = γ, M₁₀ = γ*, M₁₁ = w*, det = 1, \|w\|² − \|γ\|² = 1 |
| top-left element, 2 ± i(κ/k − k/κ) identity | verified | SymPy |
| (7) | verified | SymPy: (1 + η²)sinh² = V0² sinh²/(4E(V0 − E)) with k² + κ² = 2V0 and k²κ² = 4E(V0 − E) |
| (8) | verified | Limits d → 0 give T → 1 (SymPy). As V0 → ∞, T → 0. R = \|γ\|²/\|w\|² = 1 − T from (6). |
| (9) | verified | SymPy: ratio of (8) to (9) → 1 as d → ∞ |
| (10) | verified | SymPy geometric sum. Numerically, series and matrix product agree to 1×10⁻¹⁵ at 4 energies (own code). |
| (11) | verified | SymPy small-T limit gives 4TaTb/(Ta + Tb)²; the inequality follows from (Ta − Tb)² ≥ 0 |
| (12) | verified | r²e^{2iks} = R e^{iθ} |
| (13) | verified | SymPy: (1 − Re^{iθ})(1 − Re^{−iθ}) = (1 − R)² + 4R sin²(θ/2) |
| (14) | verified | Own code: θ(E_r)/2π = 1.1×10⁻¹⁰ |
| (15) | verified | SymPy: (4R/T²)(θ'²/4)(E − E_r)² = (E − E_r)²/(Γ/2)² with Γ = 2T/(√R θ') |
| (16) | verified | SymPy: −2 ln R − 2T/√R = −T³/12 + … (agree to order T³, as stated). Units: ħ/energy = time. |
| (17) | verified | Units: ħv/L is an energy. Limits as stated. |
| phase average 1/√(1+F) = T/(1+R) (in-line) | verified | SymPy integral over u; numeric check at F = 3 gives 0.5 |
| (18) | verified | Definition; the run energy label is k0²/2 (rt3d2.py: k0 = √(2E)) |
| (19) | verified | SymPy: Lorentzian area πΓ/2 times 1/(√(2π)σ_E) = √(π/8) Γ/σ_E |
| (20) | verified | SymPy: χ'/χ at L/2 is −k tan(kL/2) for even and k cot(kL/2) for odd, set equal to −κ |
| (21) | verified | Units ħ²/(mL²) is an energy |
| (22) | verified | SymPy: Re(e^{−iφ}e^{−iks}/√T) = cos(ks + φ)/√T |
| (23) and Cayley–Hamilton P^N = U_{N−1}P − U_{N−2}I | verified | SymPy for N = 2, 3, 5, 10 on a determinant-1 matrix of form (6). Own code: (23) against direct product, max deviation 8×10⁻¹³ over 251 energies. |
| (24) | verified | P maps right to left amplitudes, so its eigenvalue is e^{−iqs}; λ + 1/λ = 2 cos qs |
| (25) | verified | Matches `rt3d2.run`: halfV · ifft(kin · fft(·)) · halfV, kin = e^{−iK²Δt/2}, Δt = 0.01. Error orders are standard Strang. |
| (26) | verified | SymPy: exact for a single-energy wave e^{−iEt}. The page code (`interp()`, cp = cos Eτ, sp = −sin Eτ, rr = e^{iEΔt}ψ_{f+1}) implements it line for line. |
| (27) | verified | Rates add; units consistent. A model, not derived. |
| (28) | verified (order of magnitude, as stated) | Units mRW/ħ = time |
| (29) | verified | `rt3d2.vbias`: −bias · clip((x − x_l)/(x_r − x_l), 0, 1) from the first to the last outer face |
| (30) | verified | SymPy: 2·2πk dk/(2π)² = (m/πħ²)dE⊥; ∫dx/(1 + e^{x−c}) = ln(1 + e^c), checked at c = 2 and c = −3 |
| (31) | verified | SymPy prefactor e m* kT/(2π²ħ³) = e · (m* kT/πħ²) · 1/(2πħ); v dk/2π = dE/(2πħ) |
| (32) | verified | `file_rt3d2.py`: np.trapezoid(T · supply, E) over the 25 stored energies, with twin T for walls and T_far for discs. Recomputed from the index runs: identical. |

## Numbers

| § | Number in the note | Recomputed | Verdict |
|---|---|---|---|
| Abstract | 14 in a hundred; grids up to 512 × 128 × 128 | T = 0.1439; boxes in index (192/256/512) × 128 × 128 | verified |
| 1 | about 4 % per glass surface | ((1.5 − 1)/(1.5 + 1))² = 0.04 | verified |
| Fig. 1 | E/V0 true 0.37; stored E 0.30 … 2.60 (47); diode down to 0.10 | 0.3675; index energies | verified |
| 2 | x0 14 before the first face; long 4σx = 48 | `x0_of` = face − max(14, 4σx) | verified |
| 2 | σ⊥(40) = 7.3 | 7.31 | verified |
| 2 | k = 1.212, λ = 5.18, κ = 1.591, e^{−κd} = 0.204 | 1.2124, 5.1825, 1.5906, 0.2038 | verified |
| 2 | E/V0 = 0.37, κd = 1.59, σ_E/Γ = 2.9 | 0.367, 1.591, 2.87 | verified |
| 3 | sinh 1.591 = 2.351, \|w\|² = 6.95, T = 0.144, \|r\| = 0.925 | 2.3515, 6.948, 0.14393, 0.9252 | verified |
| 3 Ex. 3.1 | sinh 3.18 = 12.0, 4 · 0.735 · 1.265 = 3.72, T = 6.4×10⁻³, 22.5 | 12.017, 3.719, 6.397×10⁻³, 22.50 | verified |
| 3 | (9) gives 0.154 against 0.144 | 0.1545 | verified |
| 4 | (10) = matrix to 1 part in 10⁹; \|t₂\|² = 1.000 | 1×10⁻¹⁵; 0.999996 | verified |
| 4 Ex. 4.1 | 2.1, 7.1, 13.9, 36.8, 67.1, 92.5, 99.9 % | 2.07, 7.14, 13.89, 36.77, 67.08, 92.50, 99.93 % | verified |
| 5 | θ = 2πn to 10⁻⁸; ρ = −3.03 | 1.1×10⁻¹⁰ (own code, peak by minimisation); −3.031 | verified |
| 5 | 1/κ = 0.63, L_eff = 2.76, half wavelength 2.59 | 0.629, 2.757, 2.591 | verified |
| 5 | ħθ' = 4.45, 2L_eff/v = 4.55 | 4.454, 4.549 | verified |
| 5 | 0.3108, 0.3111, 0.2879; 1/√R = 1.08 | 0.31082, 0.31113, 0.28787; 1.081 | verified |
| 5 | Γ(15) = 0.0699; exact Γ = 0.0704; τ = 14.2, "about three round trips"; (17) 0.0633 with v = 1.21, L_eff = 2.76 | 0.06986; 0.070405; 14.20, 3.19 round trips; 0.06329 | verified |
| 5 | wide gap T/(2 − T) = 0.078 | 0.0775 | verified |
| 6 | σ_E = 0.202; (19) 0.218; exact (18) 0.196; one barrier 0.149 | 0.2021; 0.2183; 0.19591; 0.14940 (own quadrature) | verified |
| 6 | long: box 2.67×, FWHM 0.119, σ_E 0.051, exact at peak 0.54 | 512/192 = 2.667; 0.1190; 0.0505; 0.5399 | verified |
| 6 | 15 long runs; nearest E = 0.7346 passes 0.488 (0.49) vs 0.54 | index: 0.48770, well 0.00697 → 0.4912; exact at 0.7346: 0.5397 | verified |
| 6 | best E = 0.713: 0.524 (0.53) vs 0.5 | 0.52406, well 0.00719 → 0.5277; exact 0.4997 | verified |
| 6 | d = 2: Γ = 0.00291; nearest 0.7432: 0.0197 vs 0.0351; best 0.7215: 0.0225 vs 0.0319; 509; 0.00736; 39 % | 0.002911; 0.01966, exact 0.03513; 0.02247, exact 0.03190; 509.44; 0.007357; 0.00368/0.00943 = 39.0 % | verified |
| 6 | (19) at E_r = 0.744 for d = 2: 0.0359 vs exact 0.0351 | 0.03589 vs 0.03514 | verified |
| 7 | e^{−2κd} = 0.04; (21) 0.649 vs 0.735 | 0.0415; 0.6491 | verified |
| 7 table | s = 2.5: 0.735 / 0.744 / 2.193 / 0.0704 / 14.2 | 0.7349 / 0.7440 / 2.1932 / 0.07040 / 14.20 | verified |
| 7 table | s = 3.5: 0.388, 1.486 / 0.395, 1.445 / 0.79 / 0.0172 / 58.3 | 0.3881, 1.4856 / 0.3946, 1.4455 / 0.7896 / 0.01716 / 58.29 | verified |
| 7 table | s = 4.5: 0.238, 0.931 / 0.241, 0.933, 1.878 / 0.403 / 0.00606 / 165 | 0.2379, 0.9306 / 0.2414, 0.9325, 1.8778 / 0.4028 / 0.006065 / 164.9 | verified |
| 7 table | s = 5.5: 0.160, 0.633, 1.397 / 0.162, 0.638, 1.377 / 0.244 / 0.00267 / 375 | 0.1603, 0.6331, 1.3967 / 0.1623, 0.6379, 1.3769 / 0.2437 / 0.002665 / 375.2 | verified |
| 7 | peak above barrier at 2.028, width 0.314 | 2.0280, 0.3144 | verified |
| 7 | "within a hundredth", "a few hundredths" | max 0.009 for the lowest; 0.041 and 0.020 near the top | verified |
| 7 | run s = 3.5 at E = 0.4: 68.4 vs 58.3, 17 % | index τ 68.366; 68.366/58.29 = 1.173 | verified |
| 7 | 4.5 and 5.5: first resonance below 0.30 | 0.238 and 0.160 | verified |
| 8 table | V0 = 1.5: 0.64, 1.31, 0.248, 0.116, 0.0930, 8.6 | 0.6405, 1.311, 0.2485, 0.1163, 0.09296, 8.60 | verified |
| 8 table | V0 = 2: 0.735, 1.59, 0.144, 0.0704, 0.0633, 14.2 | as §5 | verified |
| 8 table | V0 = 3: 0.877, 2.06, 0.0526, 0.0291, 0.0282, 34.4 | 0.8772, 2.060, 0.05259, 0.02906, 0.02820, 34.41 | verified |
| 8 table | d = 1.5: 0.742, 2.38, 0.0316, 0.0142, 0.0139, 70.4 | 0.7421, 2.379, 0.03156, 0.01421, 0.01393, 70.39 | verified |
| 8 table | d = 2: 0.744, 3.17, 0.00657, 0.00291, 0.00290, 344 | 0.7436, 3.170, 0.006568, 0.002911, 0.002900, 343.5 | verified |
| 8 | 22× more opaque, 24× narrower; (17) within a quarter | 21.9, 24.2; worst 0.093/0.116 = 0.80 | verified |
| 8 | d = 2 run: E 0.75, lasts 217, fit from 92.7, τ 210 | index t_end 216.91, t0 92.65, τ 209.54 | verified |
| 9 | band 0.59–0.955, width 0.365, midpoint 0.773, gap 1.126, second band 2.082 | 0.58983, 0.95522, 0.36539, 0.77253, 1.12635, 2.08158 | verified |
| 9 | peaks N = 3, 5, 10 (all listed values) | own peak search and ξ = cos(jπ/N) roots agree to 4 decimals; T_N ≥ 1 − 4×10⁻¹¹ at each | verified |
| 9 | (23) vs product 2.3×10⁻¹² | own code 8×10⁻¹³ (a different implementation; both at round-off) | verified |
| 9 | peaks 0.02 to 0.17 apart; spread 0.2 | 0.018 (N = 10) to 0.173 (N = 3) | verified |
| 9 | ten walls band 0.143 (exact 0.174) | 8 runs 0.60–0.95: 0.14346; exact 0.1745 (converged quadrature) | verified |
| 9 | ten walls gap 0.0237 (exact 0.0351), "between 1.05 and 1.6" | 0.02368 and 0.0351, but over 1.10–1.60 | wrong, because of the window (error 4) |
| 9 | rises above about 1.8 | twin T: 0.057 at 1.7, 0.098 at 1.8, 0.226 at 2.0 | verified |
| 10 | 0.5 a grid, 192/256/512 × 128 × 128, 96 a × 64 a | index dx 0.5, boxes | verified |
| 10 | faces halfway between grid points; shell = points within d/2 | `centres()` puts faces on odd multiples of 0.25; `geometry()` | verified |
| 10 | border: outer tenth, sin^{1/8}(πe/2W), every step | `setup()`: W = max(4, n//10), m = sin(πe/2W)^0.125, `p * mask` each step | verified |
| 10 | Δt = 0.01; three million points or more | index dt 0.01; 192·128·128 = 3.15 M | verified |
| 10 | 0.92 ns per point per step | Σ wall / Σ(points × steps) = 0.9218 ns | verified |
| 10 | 3739 runs; 1128, 188, 564, 376, 423, 1000, 60 and their make-up | index group counts and structure lists match exactly | verified |
| 10 | start share ≤ 2.1×10⁻⁵ | max 2.093×10⁻⁵ | verified |
| 10 | run length rule; caps 60, 150, shells 30 | `t_end_of`, `tau_est`. Stored t_end of 25 later-commit runs matches the rule within one frame step. | verified |
| 10 | first third used older rule; 15 rerun | 1237/3739 = 33 % on commit cdcade4; replaced = 15; FIX1 list of 15; sampled old runs lengthen by 1.5–15.7 % | verified |
| 10 | 30 to 537 time units | 29.85 and 537.3 | verified |
| 10 | 7 notebooks, pairs of T4, 18.6 h; "twice that" single-GPU | Σ sweep_s = 18.56 h; Σ per-run wall = 35.6 h (1.92×) | verified |
| 10 | 42 duplicates; 3697 filed | index | verified |
| 10 | 200 frames; z = 0, y ≥ 0; 8-bit \|ψ\| of frame peak; arg 8-bit; below 3 steps drawn −π | `run()`: qa, qp, qp[qa < 3] = 0; page maps 0 to −π | verified |
| 10 | border one cell off mirror symmetry (even number of points) | y = −32 … 31.5; mask symmetric in index, not in y | verified |
| 10 box | 0.2 % of peak; 0.012 rad; 1025-step colour table; clip ±1.25 | 0.5/255 = 0.196 %; π/255 = 0.0123; LUT 1025 in rt3d-view.js; clamp ±1.25 in buildSheet | verified |
| Reading the figures | one scale = largest value of the run; × 4 when below 0.25; Fig. 15b divided by total | peakMax = max(peaks); drawPT `big = max < 0.25`; drawProfile divides by Σ prof·dx | verified |
| 11 | 115 earlier runs; sep 1.8×10⁻⁴ | gen-1 index: 115; 1.797×10⁻⁴ | verified |
| 11 | 0.186 vs 0.196 (5 %); +22 % at 0.4; 0.0564 vs 0.0706 (−20 %) at 1.2 | 0.186134, 0.195912, +5.3 %; 1.223; 0.799 | verified |
| 11 | 3.0 %, 2.4 %, 5.8 %, 66 % | `gen1_profile_check.py` rerun: 0.0300, 0.0243, 0.0584, 0.664 | verified |
| 11 | τ 15.1 (3D), 15.3 (twin), 14.2; 6–8 %; 17 % at s = 3.5 | 15.112, 15.33; +6.4 %, +7.9 %; 17.3 % | verified |
| 11 | 1/κ = 0.63 = 1.3 spacings; two points thick | 1.26; d/dx = 2 | verified |
| 11 | lifetime fit 60 % → 5 %; T_far rule (thousandth at end borders, + half the well, ÷ total) | `fit_tau`, `summary` in file_rt3d2.py | verified |
| 11 | T_far 0.179 vs twin 0.186, 4 % | 0.17933, 3.7 % | verified |
| 12 | σ⊥ 3.6 at t ≈ 12 | 3.56 at 11.5 | verified |
| 12 | R = 2 share 0.926 at 0.75 | 0.92606 | verified |
| 12 table | walls 15.1 / 0.187 | τ 15.138, twin 0.186957 | verified |
| 12 table | R 12: 12.9, 85.9, 36, 0.183, 0.16 | 12.87, 85.90, 0.18347, 0.15992 | verified |
| 12 table | R 9: 12.6, 73.6, 27, 0.231, 0.206 | 12.557, 73.65, 0.23118, 0.20573 | verified |
| 12 table | R 6: 9.06, 22.6, 18, 0.438, 0.414 | 9.058, 22.55, 0.43754, 0.41417 | verified |
| 12 table | R 4: 3.69, 4.87, 12, 0.689, 0.674 | 3.687, 4.874, 0.68857, 0.67424 | verified |
| 12 table | R 2: 1.88, 2.15, 4, 0.926, 0.932 | 1.881, 2.148, 0.92606, 0.93154 | verified |
| 12 | within a factor of about 3; grows less 2→4, more 4→6; 76.1 and 88.5 from rounded | ratios 0.54–2.7; ×2.27 vs ×3, ×4.6 vs ×1.5; 76.10, 88.54 | verified |
| 12 shells | 66.9 / ≥ 112 / 89.2 / ≥ 125, all at 0.30, 47 runs each; ≥ only for s = 3.5 | 66.893, 112.484 (window 92 < τ, ends at t_end), 89.192, 125.462 (window 85 < τ); all at E = 0.3 | verified |
| 13 | a = 2.75 nm, 4.13 nm, 300, 110, 10.6 meV, 62 fs, 4.39 fs | 2.754, 4.130, 300, 110.2, 10.56, 62.3, 4.388 | verified |
| 13 | E_F = 1.0 (150 meV), k_BT = 0.05 (87 K); 131 mV, 274 mV | 87.0 K; 131.25, 273.75 | verified |
| 13 | peaks 0.735, 0.483, 0.226; heights 1, 0.877, 0.559 | own staircase: 0.7349, 0.4826, 0.2261; 1.000, 0.8769, 0.5592 | verified |
| 13 | exact I–V peak 0.875, valley 1.825, ratio 4.3 | own Tsu–Esaki: 0.875, 1.825, 4.32 | verified |
| 13 | levels 0.29 and 0.1; supply 14.2 and 18 | 0.2905, 0.0981; 14.15, 18.04 | verified |
| 13 | areas 0.103, 0.073, 0.041; heights 0.65, 0.34; widths 0.077, 0.085 | 0.1030, 0.0730, 0.0405; 0.652, 0.343; 0.0772, 0.0846 | verified |
| 13 | products 1.04 and 0.74 | 1.034 and 0.731 | wrong, because of rounding (error 3) |
| 13 | runs' curve peak 0.75, valley 1.625, ratio 4.4; one step earlier, valley 0.2 earlier | recomputed from 500 runs: 0.75, 1.625, 4.37 | verified |
| 13 | single-energy T at 25 energies: top 1.125, ratio 16.7 | with V0 = 2: top 0.75, valley 1.75, ratio 4.81 | wrong, because the stored curve used V0 = 3 (error 1) |
| 13 | peak of T 0.071 wide | 0.0704 | wrong, because of a grid estimate (error 2) |
| 13 | discs R 6: 3.46 at 0.75, 2.82 at 2.375, ratio 1.2; walls top 0.96 | 3.4617, 2.8210, 1.227; 0.9597 | verified |
| Fig. 3 | 44 px per unit; drop 0.795; dashed level 0.727; level under bias 0.327; collector E_F 0.20 | SVG coordinates; own T peak at V_b = 0.8 interpolates to about 0.33 | verified |
| 14 | 6–8 % (17 % at s = 3.5); box 64 a | as §11; 128 × 0.5 | verified |
| Problems | Γ = 10.6 meV; L_eff = 2.76 a = 7.6 nm; R 2 τ 1.88, walls 15.1 | 7.59 nm; index | verified |
| 13 | 0.30 eV offset for 35 % Al | Not re-derived from Vurgaftman 2001 in this round; quoted as "about" | unverifiable, because the paper was not re-read here (round 6 checked it) |
