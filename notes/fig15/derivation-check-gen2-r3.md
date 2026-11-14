# Fig. 15 note: derivation and number check, round 3

Checked version: `public/scripts/resonant-note.js` at commit f8e0926 (md5 bab23176…; the file changed three times while this check ran, and everything below is re-checked against f8e0926).
Tools: SymPy 1.14 (scratchpad `derive_sym.py`), NumPy with the repository's own `tm.py`/`iv.py`, the page rendered in headless Chrome (port 9437). All 32 equation tags render, there are 0 KaTeX errors, and the page shows no JS errors.
NUM block: `gen2_numbers.py` was re-run without `--write`. All 272 keys match the NUM block exactly.

## A. Equations

| Eq. | Verdict |
|---|---|
| (1) | verified. Standard TDSE; the units hbar = m = 1 reduction is correct. |
| (2) | verified (SymPy: the three brackets add up exactly). **The text around it is wrong**: it says the leftover f(t) is "removed by multiplying its factor by the phase e^{-i∫f dt}". The bracket is iġ/g + ½g''/g, so multiplying by φ(t) adds iφ̇/φ, and the phase that cancels f is **e^{+i∫f dt}** (SymPy: e^{-i∫f} doubles f to 2f, e^{+i∫f} gives 0). |
| (3) | verified. SymPy confirms that g ∝ (1+it/2σ²)^{-1/2} exp[-y²/4σ²(1+it/2σ²)] solves (2) exactly, and that the variance of \|g\|² is σ²(1+(t/2σ²)²). Units: ħt/(mσ²) is dimensionless. |
| (4) | verified. |
| (5) | verified (SymPy solve of the two matching conditions). |
| (6) | verified. The centre-referenced product gives M = [[w, γ],[γ*, w*]], w = e^{ikd}[cosh κd + i(κ²−k²)/(2kκ) sinh κd], γ = i(κ²+k²)/(2kκ) sinh κd, and \|w\|²−\|γ\|² = 1 (SymPy, exact). The new written-out product (step in, diag(e^{κd},e^{−κd}), step out, and (1±iκ/k)(1±k/iκ) = 2 ± i(κ/k−k/κ)) is also verified. Numerically r = γ* t agrees with tm.py to 1e-16. |
| (7) | verified (SymPy, exact). |
| (8) | verified. Limits d→0 gives T→1 and V0→∞ gives T→0. |
| (9) | verified. SymPy: T(8)/T(9) → 1 as d→∞. |
| (10) | verified, in the note's stated phase convention: t₂(10) = t₂(global, tm.py) · e^{iks}, and \|t₂\| agrees with tm.py to 1e-15 at E = 0.5, 0.735, 1.1. The new sentence in the section 4 lead, "(M diag(e^{-iks},e^{iks}) M)₁₁ = 1/t₂", is also verified numerically in the same convention. |
| (11) | verified. Leading order of T_aT_b/(1−√(R_aR_b))² is 4T_aT_b/(T_a+T_b)², and it equals 1 iff T_a = T_b. |
| (12) | verified (definition). |
| (13) | verified (SymPy: \|1−Re^{iθ}\|² = (1−R)²+4R sin²(θ/2)). |
| (14) | verified. |
| (15) | verified. The half width from (13) is T/(√R θ'), so Γ = 2T/(√R θ'). |
| (16) | verified to the order stated. SymPy: −2 ln R − 2T/√R = −T³/12 + O(T⁴), which matches "agree up to terms of order T³". |
| (17) | verified, together with the new remark that 1/√R = 1.081 accounts for most of the 10 % shortfall. The rest, about 2 %, comes from ħθ' = 4.45 against 2L_eff/v = 4.55. Units check out. |
| (18) | verified (definition). Recomputed independently by quadrature (section B). |
| (19) | verified. SymPy: the Lorentzian area is πΓ/2, and (πΓ/2)/(√(2π)σ_E) = √(π/8)Γ/σ_E. |
| (20) | verified. SymPy nsolve reproduces every finite-well level in the table: 0.744; 0.395, 1.445; 0.241, 0.933, 1.878; 0.162, 0.638, 1.377. |
| (21) | verified. Units check out, and the value 0.649 is right. |
| (22) | verified. ½tr P = Re(w e^{-iks}) = cos(ks+φ)/√T, all three equal to 1e-16. |
| (23) | verified. 1/\|(P^N)₁₁\|² equals tm.py for N = 2…5 to 1e-14. The N = 1 limit and the zeros at β = jπ/N are correct. |
| (24) | verified. |
| (25) | verified against `rt3d2.py` `chunk()`: halfV · ifft(kin · fft(·)) · halfV, kin = exp(−½i K² Δt), then the mask. Δt = 0.01. |
| (26) | verified, both algebraically (exact at u = 0 and u = 1) and line by line against `interp()` in resonant-tunnelling.html: rotate ψ_{f+1} by e^{iEΔt}, mix, multiply by e^{−iEδ}. |
| (27) | verified (rates add). Limit τ_side→∞ gives τ_walls. |
| (28) | verified as an order-of-magnitude estimate. Units mR²/ħ are a time. |
| (29) | verified against `rt3d2.vbias` and `iv.T_biased`: linear between the outer faces, 0 on the left, −V_b on the right. |
| (30) | verified. SymPy gives ∫₀^∞dx/(1+e^{x−c}) = ln(1+e^c). The density of states 2d²k/(2π)² = (m*/πħ²)dE⊥ is right. Units are 1/area. |
| (31) | verified. The prefactor is e·(1/2πħ)·(m*k_BT/πħ²) = e m* k_BT/(2π²ħ³), with units current per area. It matches `iv.supply` and `iv_curve`. |
| (32) | verified against `file_rt3d2.py`: trapezoid over the filed energies, needing ≥ 5 per voltage, E_F = 1, kT = 0.05. Walls use the twin T, discs use T_far. |

## B. Numbers

### Fixed numbers in the text

| Number (section) | Verdict |
|---|---|
| k = 1.212, 2π/k = 5.18, κ = 1.591, e^{−κd} = 0.204 (2) | verified (1.2124, 5.182, 1.5906, 0.2038) |
| a = 2.75 nm (2, 13) | verified (2.7536 nm) |
| sinh(1.591) = 2.351, \|w\|² = 6.95, T = 0.144, \|r\| = 0.925 (3) | verified (2.3514, 6.947, 0.14395, 0.9252) |
| Ex. 3.1: sinh(3.18) = 12.0, T = 6.4e-3, "twenty-two times" | verified (12.017, 6.397e-3, ratio 22.5) |
| (9) gives 0.154 (V2D1_Tthick) | verified |
| \|t₂\|² = 1.000 at 0.735 (4) | verified (0.999996) |
| Example 4.1 table: 2.1, 7.1, 13.9, 36.8, 67.1, 92.5, 99.9 % | verified, all seven entries |
| 0.144² = 2.1 % | verified |
| θ mod 2π = 5.6e-9 (5) | verified (gen2 re-run) |
| L_eff = 2.76 against λ/2 = 2.59 (5) | verified (2.757, 2.591) |
| ħθ' = 4.45, 2L_eff/v = 4.55, Γ(15) = 0.0699 | verified |
| −2 ln R = 0.3108, 2T/√R = 0.3111, 2T = 0.2879 | verified |
| 1/√R = 1.08 (new) | verified (1.081) |
| Γ = 0.0704, τ = 14.2, "about three round trips" | verified (0.07040; 14.20; 14.2/4.45 = 3.2) |
| (17) with v = 1.21, L_eff = 2.76 gives 0.0633 | verified |
| T/(2−T) = 0.144/1.856 = 0.078 | verified (0.0776) |
| spread_t40 = 7.3; 3.7 at t ≈ 13 (12) | verified (7.31; 3.70). In gen 2 the packet reaches the structure centre at 15.75/v = 13.0 for E = 0.735. |
| σ_E = 0.202, (19) gives 0.218, exact 0.196 (6) | verified (direct quadrature 0.1959) |
| One barrier alone passes 0.149 (6) | verified (0.1494, direct quadrature) |
| box_long 2.67, σ_E(long) = 0.051, FWHM 0.119 | verified |
| V2D1_Tbar12 = 0.538 ("rises from 0.196 to 0.538") | **wrong, because** the value is a linear interpolation of the stored 0.01-step Tbar table at the top of a peaked curve. Direct quadrature of (18) at the unrounded E_r gives **0.540**. |
| V2D2: (19) 0.0359 against exact 0.035 at E_r = 0.744 | verified (quadrature 0.0351) |
| V2D1_long: 0.51 at 0.713, exact 0.499; V2D2_long: 0.0225 at 0.7215, exact 0.0318 | values verified (quadrature 0.4997, 0.0319). See errors 3 and 4 for the sentences built on them. |
| Spacing table (7): E_r lists, Γ, τ, hard box, Eeff 0.649 | verified (gen2 re-run plus SymPy finite well) |
| "finite well within a hundredth / a few hundredths" | verified (largest gaps 0.009 and 0.041) |
| "1.878 for s = 4.5 has no sharp resonance beside it … the peak washes out" | **imprecise**: tm.py shows a full T = 1 peak at E = 2.028, FWHM about 0.31 (T > 0.5 from 1.90 to 2.21). It is broad and pushed above V0, but it does not wash out. |
| P3_5 run: τ 65.2 against 58.3, 12 % (7) | verified (window 2.3 τ) |
| Opacity table (8), "22× more opaque, 24× narrower", "(17) within a quarter" | verified (worst Gest/Γ = 0.80 at V0 = 1.5) |
| E_r 0.735 / 0.742 / 0.744 / 0.877 / 0.64 | verified |
| d = 2 run: t_end 213, fit from 91, τ_fit 210 against 344 | verified (window 0.58 τ) |
| Band 0.59–0.955, gap 1.126, band 2 at 2.082, midpoint 0.773, width 0.365 | verified |
| N3/N5/N10 peak lists; T_N ≥ 1 − 1e-9 at each | verified |
| TN_check 2.3e-12 | verified (re-run) |
| "peaks 0.02 to 0.17 apart" | verified (0.018 to 0.173) |
| N10 band 0.129 (exact 0.158), gap 0.0218 (exact 0.032) | verified (quadrature 0.1580, 0.0320). These are the 1D twin's T, not the 3D runs (see error 7). |
| 0.59 rad per step (diagonal mode) | verified (3(2π)²·0.01/2 = 0.592) |
| "about one nanosecond per grid point per step" | verified (index median 0.95 ns, 5–95 % range 0.88–1.09) |
| 3739 runs; A 1128, B 188, C 564, D 376, E 423, F 1000, G 60 | verified (ran `jobs()` with stubbed jax) |
| run_tmin 30, run_tmax 517, start_in_max 2.1e-5 | verified (index 29.85, 517.4, 2.09e-5) |
| six parts, two T4 each; 1237 runs from 2 parts; 5.9 h | verified (2 notebooks, devices = 2, Σsweep_s = 21350 s) |
| Grid 192/256/512 × 128 × 128, dx 0.5, faces on odd multiples of 0.25, absorbing outer tenth sin^(1/8) | verified against `rt3d2.setup`, `centres` and `jobs` |
| Run length: flight plus 3τ, cap 60 / 150, shells 30 | verified against `tau_est` and `t_end_of` |
| Storage: 8-bit levels, 0.2 %, 0.012 rad, phase dropped below 3 levels and drawn as −π, 1025-step LUT, clip ±1.25 | verified against `rt3d2.run`, `rt3d-worker.js` and `buildSheet` |
| Fit window 60 % → 5 % (or to the end); T_far = (P_right + P_well/2)/P_box | verified against `fit_tau` and `summary`. Detail: "before any of the wave reaches the border" is in code "while < 1e-3 of it is in the border". |
| Section 11 (gen 1): 1.8e-4, 0.186 against 0.196 (5 %), +22 % at 0.4, 0.056 against 0.071 at 1.2, τ 15.1 / 15.3 against 14.2 (6–8 %), T_far 0.179 (4 %) | verified from 2026-11-13 index.json |
| Section 11: 3.0 %, 2.4 %, 5.8 % | verified (re-ran `gen1_profile_check.py`: 0.0300, 0.0243, 0.0584) |
| Discs: disc_E 0.65, walls τ 15.1, T 0.176; R2 τ 1.99, T 0.936, τ_side 2.28; one disc R4 0.678, R6 0.415 | verified (index) |
| "walls give 15.1 here, as the earlier batch did at 0.735" | verified (15.12 and 15.11) |
| Shell table: 66.9 @0.30, ≥110 @0.35, ≥63.2 @0.40, ≥104 @0.45, 16 runs each | values verified. See errors 5 and 6 for the sentence about them. |
| GaAs table: 2.75 nm, 4.13 nm, 300 meV, 110 meV, 10.6 meV, 62 fs | verified (CODATA via SciPy constants and by hand) |
| 0.30 eV offset for x = 0.35 | unverifiable here: Vurgaftman et al. was not opened. The usual 65:35 split gives about 0.28 eV, so "about 0.30 eV" is plausible. |
| Er under bias 0.735 / 0.483 / 0.226; Tpk 1.0 / 0.877 / 0.559 | verified (nper 200 agrees with 60 to 1e-5) |
| Figure 3 at V_b = 0.8: every coordinate to scale (44 px/unit), level drawn at 0.327 | verified (tm/iv peak 0.329) |
| iv_exact: peak 0.875 (131 mV), valley 1.825 (274 mV), PVR 4.3 | verified. Recomputed `iv_curve`: max \|J − stored\| = 5e-9. Converged in energy grid (nE 4000 changes J by 3e-6). |
| sup 14.2 / 18.0, area 0.103 / 0.073 / 0.041, products 1.04 / 0.74 | verified |
| E_F = 1.0 (150 meV), k_BT = 0.05 (87 K) | verified (87.03 K) |
| iv_walls_nruns 170 / 500, "a different third at each" voltage | verified (8–12 per voltage, rotating subsets) |
| Figure 1: E/V0 drawn at 0.5, true 0.37 | verified (57/115 = 0.50; 0.3675) |
| Figure 2 axes and T = 1 line | verified |
| 1.92 THz (Maekawa 2016) | not checked against the paper; it matches the published title |

## C. Description of the method against the code

All matches, except errors 2 and 7 below: rt3d2.py (grid, mask, Strang order, placement, shells, regions, twin), rt3d2_run.py (jobs, run length, sp = 3), file_rt3d2.py (T_far, τ fit, J_runs, exact Tbar) and the page (SHA-256 check, mirror half, (26), linear blend of 15b/15c, ×4 rule, dashed disc curve).

## D. Errors, ranked by severity

1. **Section 2, after (2): wrong sign of the gauge phase.** "removed by multiplying its factor by the phase e^{−i∫f dt}" should read **e^{+i∫f dt}**. With the bracket iġ/g + ½g''/g = f(t), the factor φ adds iφ̇/φ, so φ = e^{+i∫f dt} gives f − f = 0 (SymPy check). The minus sign gives 2f.
2. **Section 1, "Reading the figures", Fig. 15b: wrong description of the dashed curve.** The note says "the exact one-dimensional answer for walls dashed in black". The code (`drawPX`, `run.prof1d`) draws the 1D *twin*: the split-step solution on the same grid and step (`rt3d2.run1d`). Section 11 itself says the twin differs from the exact 1D packet by up to 3.0 % of the run peak (5.8 % of the frame peak). Correct form: "the one-dimensional twin computed on the same grid (section 10), dashed in black".
3. **Section 6, long packets: wrong reason in the parenthesis.** "the share is read before any of the wave reaches the border, so it changes little". For walls the share is the 1D twin's T, read at the **end** of the run and counting what the border absorbed (section 11, `through()`). It is not T_far. The run at 0.713 ended at t = 101.5 with 0.029 still between the walls. Its T_far, which adds half the trapped wave, is 0.525 against the twin's 0.510. Correct form: the share is the twin's transmitted part at the end of the run; about 3 % of the packet was still trapped when it stopped, so the full rerun should pass about 0.52 rather than 0.51.
4. **Section 6, d = 2 long packet: a missing cause.** "passes only 0.0225 … against 0.0318: σ_E is still much wider than Γ …" leaves out that the run ended (t = 509 against τ = 344) with 0.0074 still in the well. That is a third of what had passed, and half of it would still leave forward. T_far reads 0.0276. The second cause (σ_E > Γ) explains why the exact average is low, not why the run falls short of it. Correct form: add that about 0.004 was still trapped at the end, so the run's final share is about 0.026, and only the rest of the gap (about 18 %) is the grid's.
5. **Section 12, shells: false for one row.** "where the fit window reaches the end of the run … the lifetime rests on less than one lifetime of decay". This holds for R = 3, s = 3.5 (window 0.67 τ) and R = 5, s = 3.5 (0.59 τ). It does not hold for R = 5, s = 2.5: the window runs from 22.6 to 145.3, which is 1.94 τ, and that row is marked "≥ 63.2" anyway. Correct form: either flag only the rows with (t1−t0) < τ, or say "rests on less than two lifetimes of decay". Then "Most of them" becomes "two of the four".
6. **Section 12, shells: "so the longest-lived states may lie below 0.30, out of its reach".** For three of the four shell pairs the lowest energy filed so far is 0.35, 0.40 or 0.45, not 0.30. The maximum sits at the lowest *filed* energy in each case. Correct form: "falls at the lowest energy filed so far for each pair (0.30–0.45), so longer-lived states may lie lower still".
7. **Section 9, ten walls: "the 3D runs inside the band pass on average 0.129 … in the gap 0.0218".** These numbers are the 1D twin's T (`gen2_numbers.through` returns `twin.T` for walls), not read from the 3D runs. Section 11 says so for Fig. 15d, but this sentence does not. Correct form: "the runs (their 1D twins, equal to the 3D walls by section 2) pass …".
8. **Section 6, "The exact average at the peak rises from 0.196 to 0.538": wrong number.** It should be **0.540**. The 0.538 is a linear interpolation of the stored 0.01-step Tbar table; direct quadrature of (18) at E_r = 0.73493 gives 0.5399.
9. **Section 7: "1.878 for s = 4.5 has no sharp resonance beside it … the peak washes out".** tm.py shows a full T = 1 peak at 2.028, FWHM about 0.31. Correct form: "its resonance is pushed above the barrier top, to 2.03, and is broad (FWHM about 0.3)".
10. **Section 13: a typographical fault.** "lower than the left by an energy \(eV_b\) Here −e is …" is missing its full stop (or the opening parenthesis of the old version). It shows up in the rendered page as "eV_b Here".

Side note, not in the note itself: the page's gain caption (`setGainNote`) says "the start packet's peak is height 1". The code scales by `peakMax`, the largest stored peak of the run, and the note describes that correctly ("the largest value the run reaches is height 1"). The two agree only when the first frame holds the largest peak.
