# Fig. 15 note: derivation and number check, round 4

Checked version: `public/scripts/resonant-note.js` at commit 95824f5 (md5 b9a52cab…), index.json md5 2e517468… (1237 runs).
The page was served from `public/` on port 9977 and rendered in headless Chrome. All 32 equation tags render, there are 0 KaTeX errors, and there are no page or console errors. The rendered text is in scratchpad `r4/note.txt`.
NUM block: `gen2_numbers.py` was re-run without `--write`. All 280 keys match the NUM block exactly (scratchpad `r4/cmp.py`).
Tools, re-run this round: SymPy 1.14 (`derive_sym.py`), NumPy checks against the repository's `tm.py`, `iv.py` and `exact1d.py` (`check_eqs.py`, `check_iv2.py`, `num.py`, `r4/tend.py`), and the repository's `notes/fig15/derive.py` (24/24 checks pass).
Code files (`rt3d2.py`, `rt3d2_run.py`, `file_rt3d2.py`, `resonant-tunnelling.html`) have not changed since round 3 (`git diff f8e0926` touches only the note, `gen2_numbers.py` and the notes folder). The method-against-code comparison of round 3 therefore still holds, and its spot checks were repeated.

## A. Equations

| Eq. | Verdict |
|---|---|
| (1) | verified |
| (2) | verified (SymPy: the three brackets sum exactly). The gauge-phase sign is now e^{+i∫f dt}, which is correct: the bracket gains iφ̇/φ = −f. |
| (3) | verified (SymPy: the free Gaussian solves (2), and the variance is σ²(1+(t/2σ²)²)). Units are dimensionless. |
| (4) | verified |
| (5) | verified (SymPy solve) |
| (6) | verified (SymPy: w, γ, M₂₁ = γ*, M₂₂ = w*, \|w\|²−\|γ\|² = 1. The written-out product and (1±iκ/k)(1±k/iκ) = 2±i(κ/k−k/κ) also check.) |
| (7) | verified (SymPy, exact) |
| (8) | verified. Limits: d→0 gives 1, V0→∞ gives 0. |
| (9) | verified (T(8)/T(9) → 1 as d→∞) |
| (10) | verified. The series equals tm.py to 7.7e-15 over 300 energies. The text's "one part in 10⁹" is derive.py's tolerance (tested at V0 = 3, s = 2.343); it is a true bound. |
| (11) | verified (leading order 4TaTb/(Ta+Tb)²; equality iff Ta = Tb) |
| (12) | verified (definition) |
| (13) | verified (SymPy). The midway value T²/(1+R)² also checks. |
| (14) | verified |
| (15) | verified (FWHM from (13) = 2T/(√R θ')) |
| (16) | verified. −2 ln R − 2T/√R = −T³/12 + O(T⁴). |
| (17) | verified. Units: an energy. |
| (18) | verified (definition; recomputed by quadrature) |
| (19) | verified (SymPy: area πΓ/2, so √(π/8)Γ/σ_E) |
| (20) | verified (even: −k tan(kL/2) = −κ; odd: k cot = −κ; nsolve reproduces all the table's levels) |
| (21) | verified (0.649) |
| (22) | verified (Re(w e^{−iks}) = cos(ks+φ)/√T to 1e-16) |
| (23) | verified (T_N formula against tm.py, N = 2, 3, 4, 5, 10: 2.3e-12; P^N = U_{N−1}P − U_{N−2}I to 1e-14) |
| (24) | verified |
| (25) | verified against `rt3d2.run` (halfV, kin = exp(−½iK²Δt), mask). Local error scales as Δt³ (2.3e-3, 2.9e-4, 3.7e-5). |
| (26) | verified (exact at u = 0 and u = 1; matches `interp()` in the page) |
| (27) | verified |
| (28) | verified as an estimate; mR²/ħ is a time |
| (29) | verified against `rt3d2.vbias` and `iv.T_biased` |
| (30) | verified (SymPy: ∫₀^∞ dx/(1+e^{x−c}) = ln(1+e^c); 2d²k/(2π)² = m*/(πħ²) dE⊥) |
| (31) | verified (prefactor e m* k_BT/(2π²ħ³)); matches `iv.iv_curve` |
| (32) | verified. It equals the stored J_runs to 4e-16 (walls and discs). |

All equations are right. The errors are in the text around them (section D).

## B. Numbers (all re-checked this round; the round-3 values were reproduced unless noted)

| Number (section) | Verdict |
|---|---|
| 14 in a hundred (abstract); T = 0.144, \|w\|² 6.95, sinh 2.351, \|r\| 0.925 (3) | verified |
| k 1.212, 2π/k 5.18, κ 1.591, e^{−κd} 0.204 (2) | verified |
| σ⊥(40) = 7.3; 3.7 at t ≈ 13 (2, 12) | verified (7.31; 3.70; the centre arrives at 12.99) |
| Ex. 3.1: sinh 12.0, 4·144/3.72, 6.4e-3, 22× | verified (12.017, 6.397e-3, ×22.5) |
| (9) gives 0.154 | verified (0.1545) |
| \|t₂\|² = 1.000; Example 4.1 table 2.1 … 99.9 % | verified, all seven entries |
| θ mod 2π = 5.6e-9; L_eff 2.76, λ/2 2.59 | verified |
| ħθ' 4.45, 2L_eff/v 4.55; 0.3108 / 0.3111 / 0.2879; 1/√R 1.08 | verified |
| Γ(15) 0.0699, exact 0.0704, τ 14.2, "about three round trips", (17) 0.0633, v 1.21 | verified |
| T/(2−T) = 0.078 | verified (0.0776) |
| σ_E 0.202, (19) 0.218, exact 0.196, one barrier 0.149 | verified (quadrature 0.1959, 0.1494) |
| box_long 2.67, σ_E 0.051, FWHM 0.119 | verified |
| "rises from 0.196 to 0.54" | verified (quadrature 0.5399; the round-3 error is fixed) |
| long walls: 5 runs filed, best 0.51 at 0.713 | verified (twin T 0.5098) |
| long walls: exact average 0.499 at 0.713 | **wrong, because** it is a linear interpolation of the 0.01-grid Tbar table (0.4986). Quadrature (exact1d.tbar, nk 4001) gives 0.4997, and the run's own stored T_exact is 0.499716. Correct: **0.500**. |
| "stopped more than 15 % before the present rule would end them" | verified. Present `t_end_of` / filed t_end = 1.20–1.64 for the five runs; all five are in `FIX1`. |
| "changes the share by a few per cent" | verified (T_far 0.525 against twin 0.510) |
| d = 2 long: 0.0225 at 0.7215 | verified (twin 0.022473) |
| d = 2 long: exact 0.0318 | **wrong, because** it is the same linear interpolation (0.03183). Quadrature gives 0.03190, and the run's stored T_exact is 0.031899. Correct: **0.0319**. |
| d = 2 long: "The run lasts less than one lifetime" | **wrong, because** t_end = 509.4 against τ = 344, which is 1.48 τ. What is under one lifetime is the decay stretch the fit sees, 169.0 → 509.4 = 340 (0.99 τ). |
| d = 2 long: "accounts for much of the shortfall" | verified, but only about 40 %. 0.00736 is still in the well, half of it ≈ 0.0037 would leave forward, and the shortfall is 0.0094. |
| (19) 0.0359 against exact 0.0351 at 0.744 (d = 2) | verified |
| Spacing table: E_r, finite well, hard box, Γ, τ | verified. "0.16" for s = 5.5 is printed without its third digit (0.160); this is cosmetic. |
| "within a hundredth / a few hundredths" | verified (0.009 max; 0.041 max) |
| s = 4.5: peak above the top at 2.028, width 0.314 | verified (Er 2.02799, FWHM 0.31439; T(1.878) = 0.43). The round-3 error is fixed. |
| P3_5 run τ 65.2 against 58.3, 12 % | verified |
| first resonance below 0.30 for s = 4.5, 5.5; second near 0.931 / 0.633 | verified |
| Opacity table; 22×, 24×, "within a quarter" | verified |
| E_r 0.735 / 0.742 / 0.744 / 0.877 / 0.64 | verified |
| d = 2 short run: 213, fit from 91, 210 | verified |
| band 0.59–0.955, gap 1.126, band 2 2.082, mid 0.773, width 0.365 | verified |
| N3/N5/N10 peak lists; 0.02–0.17 apart; TN_check 2.3e-12 | verified |
| N10: 0.129 (exact 0.158), gap 0.0218 (exact 0.032); "for walls, their 1D twins"; "rises above about 1.8" | verified (4 + 4 runs; 0.098 at 1.8 from 0.022 at 1.55) |
| 0.59 rad/step; ~1 ns per point-step; 3 million points | verified (0.592; 192·128² = 3.1 M) |
| 3739 runs, group counts, 47 / 25 energies, 2.1e-5, 30–517, caps 60 / 150 / 30 | verified (jobs() with stub jax) |
| six parts, 2 T4 each; 1237 filed from 2 parts; 5.9 h | verified (index) |
| Section 11 (gen 1): 1.8e-4, 0.186 / 0.196, 22 %, 0.056 / 0.071, 3.0 / 2.4 / 5.8 %, 15.1 / 15.3 / 14.2, 0.179 | verified (unchanged data; round-3 recomputation stands) |
| Discs: E 0.65; walls τ 15.1, T 0.176; R2 τ 1.99, τ_side 2.28, T 0.936; one disc R4 0.678, R6 0.415; R² column | verified (15.12; 0.17565; 1.985; 2.285; 0.93584; 0.67827; 0.41466) |
| "the energy nearest the resonance filed so far; the runs at 0.75 … are still to come" | **imprecise.** True for walls (filed: 0.65, then 0.85). But the disc pairs R = 4 and R = 6 at 0.75 are filed (τ 3.69 and 9.06), and R = 2 is filed at 0.70. |
| "shorter even than one round trip" (R = 2) | verified (1.99 against 2L_eff/v ≈ 4.8 at 0.65) |
| Shell table 66.9 @0.30, ≥110 @0.35, 63.2 @0.40, ≥104 @0.45, 16 runs each | verified |
| "Two of them … less than one lifetime"; ≥ only on the s = 3.5 rows | verified (windows 0.67 τ and 0.59 τ; the s = 2.5 rows have 1.76 τ and 1.94 τ). The round-3 error is fixed. |
| "falls at the lowest energy filed so far for that pair" | verified (best E = min E in all four). The round-3 error is fixed. |
| GaAs table 2.75 nm, 4.13 nm, 300 meV, 110 meV, 10.6 meV, 62 fs; 87 K | verified |
| 0.30 eV for x = 0.35 | unverifiable here, because Vurgaftman et al. was not opened. From their parameters as recalled (bowing, VBO 0.53x) ΔEc ≈ 0.29 eV, so plausible. |
| Er under bias 0.735 / 0.483 / 0.226; Tpk 1 / 0.877 / 0.559 | verified |
| Peak 0.875 (131 mV), valley 1.825 (274 mV), PVR 4.3 | verified (iv_curve against stored: 5e-9) |
| supply 14.2 / 18.0; area 0.103 / 0.073 / 0.041; products 1.04 / 0.74 | verified as numbers (window ±0.25 around the peak, not stated in the note). See error 1 for the reason given for them. |
| 170 / 500 diode runs; "a different third at each" | verified (round 3; data unchanged) |
| Figure 1 E/V0 0.5 drawn against 0.37 true; Figure 3 to scale | verified (round 3; figure code unchanged) |
| 1.92 THz (Maekawa 2016) | unverifiable here, because the paper was not opened. It matches the published title. |

## C. Description of the method against the code

Unchanged since round 3, and it matches, with one remaining detail. Section 11 says the disc share is read "at the last frame before any of the wave reaches the absorbing border". `file_rt3d2.summary` takes the last frame with less than 1e-3 of the box's probability in the end borders (|x| > inner).
Spot checks repeated: `fit_tau` (60 % → 5 %, first contiguous stretch, at least 6 points), `T_far = (right + well/2)/norm`, `tau_est` and `t_end_of` (flight of the trailing edge to 20 a past the last face, plus 3τ, caps 60 / 150, shells 30), and the twin T for walls.

## D. Errors, ranked by severity

1. **Section 13, "Roughly, the current is the area…": wrong physical reason.** The text says the area under the peak shrinks "because at low energy the electron is slow and meets the barriers less often (a narrower peak, by (17))". The exact tilted transmission (iv.T_biased, nper 100 and 400 agree) shows the opposite.
   - The peak gets **wider** as the bias rises: FWHM 0.0704 (V_b = 0), 0.0726 (0.5), 0.0772 (0.875), 0.0846 (1.25).
   - Its height falls: 1, 0.877, 0.652, 0.343.
   - The area falls only because the peak gets lower; (π/2)Γ·T_pk tracks it: 0.111, 0.079, 0.046.
   - **Correct form:** "…because the tilt makes the pair unequal, so the peak is lower (by (11)): 0.65 at V_b = 0.875 and 0.34 at 1.25. Its width even grows a little, 0.070 → 0.077 → 0.085, since the tilt lowers the second barrier more than the slower electron narrows the peak."
2. **Section 6, d = 2 long packet: "The run lasts less than one lifetime".** The run lasts 509.4 against τ = 344, which is 1.5 τ. **Correct form:** "The run stops 509 time units in, about one lifetime after the trapped wave peaks (the fit runs from t = 169 to the end, 0.99 τ), and ends with 0.0074 of the packet still between the walls. Half of that would still leave forward, which is about 40 % of the shortfall."
3. **Section 6, long packets: two exact averages read by linear interpolation of the 0.01 grid.** This is the flaw that round 3 fixed for 0.540, but it remains in `gen2_numbers.py` line 201 (`{tag}_long_exact`).
   - At E = 0.713, **0.500**, not 0.499 (quadrature 0.4997; the run's stored T_exact is 0.499716).
   - At E = 0.7215 (d = 2), **0.0319**, not 0.0318 (0.031899).
   - Fix: use exact1d.tbar with SIG0 = 12, or the run's `twin.T_exact`.
4. **Section 12, discs: "(the energy nearest the resonance filed so far; the runs at 0.75, closer to it, are still to come)".** This holds only for walls. The disc pairs of radius 4 and 6 at 0.75 are filed (τ = 3.69 and 9.06), and radius 2 is filed at 0.70 (τ 1.94). **Correct form:** "(the energy nearest the resonance at which walls are filed so far; the walls' run at 0.75 is still to come)". Optionally quote the filed 0.75 disc lifetimes, which already show the trend R2 < R4 < R6 < walls.
5. **Section 11, disc share: "at the last frame before any of the wave reaches the absorbing border".** The code takes the last frame with less than 10⁻³ of the probability in the end borders. **Correct form:** "…before more than a thousandth of the wave has reached the absorbing border…". This is minor, and carried from round 3.
6. **Section 7, spacing table: "0.16" for s = 5.5.** It should be printed as 0.160, like its neighbours (the r3 rounding drops the trailing zero). This is cosmetic.

Side note, not in the note itself: the page's caption `#gain-note` (resonant-tunnelling.html line 169) still says "the start packet's peak is height 1". The code scales by the run's largest stored peak, as the note correctly says.
