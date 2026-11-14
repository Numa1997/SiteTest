# Fig. 15 lecture note: derivation check, round 5

**Version checked.** `public/scripts/resonant-note.js` was rewritten while this check was running. It started at commit c346801 and changed in ada0993 ("fix round-5 marks"); HEAD is now a20d017. Everything below applies to the **current file (ada0993)**. I re-rendered it in Node and in headless Chromium (port 9071) and diffed it against the c346801 text. Where something from c346801 is already fixed, I say so.

## Methods

- **SymPy** (`derive_check.py`): every equation with algebra behind it, derived independently.
- **Independent 1D solver** (`indep.py`, `indep2.py`): a global-coordinate linear system for the matching conditions. It does not use tm.py or its edge/flight matrices.
- **Independent biased solver** (`airy_iv.py`): exact Airy-function solutions on the linear ramp, with no staircase. It does not use iv.py.
- **Generator re-run**: `notes/fig15/gen2_numbers.py`. All 297 NUM entries come out byte-identical to the NUM block.
- **Data read directly**: the generation-1 numbers from `2026-11-13/kaggle/index.json` and `gen1_profile_check.py`; the generation-2 claims from `2026-11-14/kaggle/index.json`. I also ran `rt3d2_run.py jobs()` and `rt3d2.t_end_of`, with jax stubbed out.
- **Page in Chromium**: the note renders all of tags (1)–(32) with no KaTeX errors. The numbers in the DOM are the NUM values.
- **Page code**: `resonant-tunnelling.html`, `rt3d-view.js` and `rt3d-worker.js`, read against the method description.

## Errors, ranked by severity

None of the 32 equations is wrong. All the errors are in quoted numbers or wording.

1. **§11, "21 % less, 0.056 against 0.071 at E = 1.2" is wrong.**
   - The index has twin T = 0.05639 and exact T̄ = 0.070597.
   - 1 − 0.05639/0.070597 = 0.201, so the right figure is **20 % less**. The 21 % comes from dividing the rounded values.
2. **§13, "a different third at each [voltage]" is wrong as stated.**
   - The filed energy sets repeat every 0.75 in voltage. For example, 0.125, 0.875, 1.625 and 2.375 all have {0.20, 0.25, 0.50, 0.55, 0.80, 0.85, 1.10, 1.15}.
   - Correct form: "a different third at neighbouring voltages; the same third comes back every 0.75 in voltage".
3. **§10 and the "Where the picture differs" box: "ψ(x,−y,0) = ψ(x,y,0) exactly" is not exact on the grid.**
   - The y axis runs from −32 to 31.5 (128 points) and the absorbing mask is `m[-W:] = m[:W][::-1]`, so the mask is not mirror-symmetric. For example, m(−31.5) = 0.775 while m(+31.5) = 0.
   - The mirror symmetry is exact only in the interior. It is broken by about one cell inside the side border.
   - Correct form: "exact for the wave inside the side border (|y| < 26); the border itself is one cell off mirror symmetry, which matters only for the small part of the wave that reaches it".
4. **§6, "half of that would still leave forward, which accounts for much of the shortfall" (d = 2 long packet) is overstated.**
   - Half of 0.00736 is 0.0037.
   - The shortfall is 0.0319 − 0.0225 = 0.0094.
   - So it accounts for **about two fifths** of the shortfall, not "much of" it.
5. **§5, "a whole multiple of 2π to within 5.6×10⁻⁹" quotes root-finding noise.**
   - For a symmetric pair, θ(E_r) = 0 exactly; here n = 0 and ρ = −ks = −3.03, both verified.
   - The residual depends only on how precisely E_r was located. My independent solver gives 1.3×10⁻⁸.
   - Suggested form: "to within 10⁻⁸ (the precision of the root search)".
6. **(32), "in units of e m* k_BT/(2π²ħ³)" is missing a factor.** The sum carries a dE, so the unit is e m* k_BT E_u/(2π²ħ³). exact1d.py itself multiplies by `pref * EuJ`. This is cosmetic in natural units.

Already fixed in ada0993: the long packet now starts 48 before the barriers (4σ_x), the arrival time reads t ≈ 12, and the stray full stop in the U₋₁ line is gone.

## Equations

| Eq. | What it is | Verdict |
|---|---|---|
| (1) | Time-dependent Schrödinger equation; in natural units i∂ₜψ = −½∇²ψ + Vψ | verified (standard; units E_u = ħ²/ma², t_u = ma²/ħ are consistent) |
| (2) | Separation ψ = χ g g | verified: the three-bracket argument is correct; multiplying by e^{i∫f} subtracts f from the bracket (checked) |
| (3) | σ⊥(t) = σ⊥√(1+(ħt/2mσ⊥²)²) | verified: SymPy shows that the quoted g solves i g_t = −½ g_yy, and that the variance of \|g\|² is σ²(1+(t/2σ²)²) |
| (4) | k = √(2E), κ = √(2(V₀−E)) | verified |
| (5) | Edge matrix | verified: SymPy solve of the two continuity conditions |
| (6) | M = [[w,γ],[γ*,w*]], \|w\|²−\|γ\|² = 1; the explicit w and γ | verified: the SymPy product step·cross·step gives w = e^{ikd}[cosh κd + i(κ²−k²)/(2kκ) sinh κd] and γ = +i(κ²+k²)/(2kκ) sinh κd exactly, with M₂₁ = γ*, M₂₂ = w* and det = 1 |
| (7) | \|w\|² = 1 + V₀² sinh²κd / (4E(V₀−E)) | verified (SymPy) |
| (8) | T = 1/\|w\|², R = 1−T | verified |
| (9) | T ≈ 16E(V₀−E)/V₀² · e^{−2κd} | verified: leading term of (8) as κd → ∞; the limits d → 0 and V₀ → ∞ are correct |
| (10) | t₂ = t² e^{iks}/(1 − r² e^{2iks}) | verified: round-trip factor re-derived; agreement with the direct solve is 10⁻¹⁵ (the note's "one part in 10⁹" is a safe bound); the extra e^{iks} belongs to the mixed reference points stated |
| (11) | \|t₂\|²_peak ≈ 4T_aT_b/(T_a+T_b)² | verified (SymPy series to leading order in T) |
| (12) | θ = 2ρ + 2ks | verified (matches the r²e^{2iks} round trip) |
| (13) | T₂ = 1/(1 + (4R/T²) sin²(θ/2)) | verified (SymPy); the midway value T²/(1+R)² is also verified |
| (14) | θ(E_r) = 2πn | verified; n = 0 with ρ ∈ (−π, π], ρ = −3.031 |
| (15) | Lorentzian, Γ = 2T/(√R θ′) | verified: the SymPy series of (13) minus the Lorentzian vanishes to O(δ⁴); units correct (θ′ is 1/energy) |
| (16) | τ = ħ/Γ | verified; −2 ln R − 2T/√R = −T³/12 + …, as claimed (order T³) |
| (17) | Γ ≈ ħvT/L_eff | verified: follows from (15) with t_rt = 2L_eff/v and 1/√R dropped; units are an energy; the step-phase rate 2/κ is verified in SymPy |
| (18) | T̄ = ∫\|φ\|² T dk | verified (definition; σ_k = 1/2σ_x is correct for the std of \|ψ\|²) |
| (19) | T̄_peak ≈ √(π/8) Γ/σ_E | verified (SymPy) |
| (20) | k tan(kL/2) = κ (even), −k cot(kL/2) = κ (odd) | verified: matching of ψ′/ψ at x = L/2 |
| (21) | E_n ≈ n²π²ħ²/(2mL_eff²) | verified |
| (22) | ξ = Re(w e^{−iks}) = cos(ks+φ)/√T | verified: algebra checked; numerically, the roots of ξ = cos(jπ/N) give T_N = 1 to 10⁻¹³ |
| (23) | T_N = [1 + (R/T) U_{N−1}(ξ)²]⁻¹ | verified: Cayley–Hamilton recursion; SymPy confirms U_n is the Chebyshev polynomial of the second kind |
| (24) | cos qs = ξ | verified (eigenvalue e^{−iqs} of P, det P = 1) |
| (25) | Strang split | verified against the code: rt3d2.py `chunk` does halfV, fftn, kin = e^{−iK²Δt/2}, ifftn, halfV, then the mask |
| (26) | Frame blending | verified against the code: page `interp()`, (1−s)ψ_f + s e^{iEΔt}ψ_{f+1}, then × e^{−iEsΔt} |
| (27) | 1/τ = 1/τ_walls + 1/τ_side | verified (independent rates add) |
| (28) | τ_side ~ mRW/ħ | verified: units are time; R² and R regimes as stated (order-of-magnitude estimate) |
| (29) | Linear ramp between the outer faces | verified against iv.py `T_biased` and rt3d2.py `vbias` |
| (30) | Supply integral | verified: SymPy ∫₀^∞ dx/(1+e^{x−c}) = ln(1+e^c); the state count m*/(πħ²) dE⊥ and the rate dE/(2πħ) are correct |
| (31) | Tsu–Esaki J | verified: the prefactor follows from (30) × e/(2πħ); units A/m² |
| (32) | Trapezoid sum | verified against the code (file_rt3d2.py `np.trapezoid` over the filed energies); units statement missing E_u (error 6) |

## Numbers

| Where | Number | Verdict |
|---|---|---|
| Abstract, §3 | T = 0.144 ("14 in a hundred"), \|w\|² = 6.95, sinh 1.591 = 2.351, \|r\| = 0.925 | verified (0.14395 at 0.735; \|r\| = 0.9252) |
| §2 | k = 1.212, λ = 5.18, κ = 1.591, e^{−κd} = 0.204, E/V₀ = 0.37, s/λ = 0.48, σ_E/Γ = 2.9 | verified |
| §2, §12 | σ⊥(40) = 7.3, σ⊥ = 3.6 at arrival, t ≈ 12 (11.55), x₀ 14 before the face, 48 for the long packet | verified (rt3d2 `x0_of`: −15.75 and −49.75) |
| Fig. 1 | E/V₀ drawn near 0.5 | verified (57/115 = 0.50 in the SVG) |
| Ex. 3.1 | sinh 3.18 = 12.0, T = 6.4×10⁻³, "twenty-two times" | verified (ratio 22.5) |
| §3 | (9) gives 0.154 | verified (0.1545) |
| §4 | \|t₂\|² = 1.000; series table 2.1, 7.1, 13.9, 36.8, 67.1, 92.5, 99.9 % | verified (all digits) |
| §5 | 5.6×10⁻⁹ | wrong in detail (error 5): noise, my solver gives 1.3×10⁻⁸ |
| §5 | L_eff 2.76, 1/κ 0.63, half-wavelength 2.59, ρ = −3.03 | verified |
| §5 | ħθ′ = 4.45, 2L_eff/v = 4.55 | verified |
| §5 | 0.3108, 0.3111, 0.2879 | verified |
| §5 | Γ(15) = 0.0699, exact 0.0704, τ 14.2, three round trips (3.19) | verified |
| §5 | (17) 0.0633, 1/√R 1.08, v 1.21 | verified |
| §5 | Wide-gap average 0.078 | verified (0.0775) |
| §6 | σ_E 0.202 / 0.051, FWHM 0.119, box 2.67 | verified |
| §6 | (19) 0.218, T̄ 0.196, one barrier 0.149 | verified (0.2183, 0.1959, 0.1494) |
| §6 | T̄₁₂ 0.54; long run 0.51 at 0.713, exact 0.5; 5 of 15 filed; 0.0286 trapped; peak run not filed | verified (exact 0.4997; index has 5 runs, no 0.7346) |
| §6 | d = 2: Γ 0.00291, 0.0225 at 0.7215, exact 0.0319, 509, 0.00736, (19) 0.0359 vs 0.0351, E_r 0.744 | verified; "much of the shortfall" overstated (error 4) |
| §7 | Table: E_r, finite-well levels, hard box, Γ, τ, all four rows | verified independently (my solver and my own bisection) |
| §7 | (21) 0.649; 2.028 and 0.314 above the top; e^{−2κd} 0.04 | verified |
| §7 | Run 3.5 apart: E 0.35, τ 65.2 vs 58.3, 12 % | verified (index; 0.40 not filed) |
| §8 | Table, all 5 rows (E_r, κd, T, Γ exact, Γ(17), τ) | verified independently |
| §8 | 22× / 24×; within a quarter (worst 0.093/0.116 = 0.80) | verified |
| §8 | d = 2 run: E 0.7, t_end 213, t₀ 91, τ 210 | verified (index: 212.93, 90.95, 209.66) |
| §9 | Band 0.59–0.955, width 0.365, gap 1.126, second band 2.082, midpoint 0.773, ξ(E_r) = 0 | verified independently |
| §9 | Peaks for N = 3, 5, 10 | verified (T_N = 1 to 10⁻¹³) |
| §9 | TN_check 2.3×10⁻¹² | verified (generator re-run) |
| §9 | Spacings 0.02–0.17 | verified (0.018, 0.173) |
| §9 | N = 10 band mean 0.129 (exact 0.158), gap mean 0.0218 (exact 0.032) | verified (index) |
| §10 | 3739 = 1128 + 188 + 564 + 376 + 423 + 1000 + 60; 47 / 25 energies; 20 voltages; long packets 4 × 15 | verified (`jobs()` run) |
| §10 | 2.1×10⁻⁵; 30–517; 1237; 2 parts; 5.9 h | verified (index: sweep_s sum 21350 s) |
| §10 | 192/256/512 × 128², 96 a / 64 a, outer tenth, 0.59 rad/step, ~1 ns, 3.1 M points, 200 frames | verified (code) |
| §10 | 0.2 %, 0.012 rad, < 3 levels drawn as −π, 1025 colour steps, clip ±1.25 | verified (code and worker) |
| §10 | "exactly" (mirror symmetry) | wrong in detail (error 3) |
| §11 (gen-1) | 115 runs, 1.8×10⁻⁴ | verified (index) |
| §11 (gen-1) | 0.186 vs 0.196, 5 % | verified (index) |
| §11 (gen-1) | 22 % more at 0.4 | verified (index) |
| §11 (gen-1) | 21 % less at 1.2 | wrong (error 1): 20 % less |
| §11 (gen-1) | 3.0 %, 2.4 %, 5.8 %, 66 % | verified (re-ran `gen1_profile_check.py`) |
| §11 (gen-1) | τ 15.1 / 15.3 vs 14.2, 6–8 % | verified (6.4 %, 7.9 %) |
| §11 (gen-1) | T_far 0.179, 4 % | verified (3.7 %) |
| §11 | Fit window 60 %→5 %, T_far rule, regions, Fig. 15b/c/d descriptions | verified against `file_rt3d2.py` and the page code |
| §12 | Disc table and text: R = 2 τ 1.99, T 0.936, τ_side 2.28; walls 15.1 / 0.176 at 0.65; one disc 0.678 / 0.415; estimates 36, 27, 18, 12, 4; 0.70 and 0.75 not filed | verified (index) |
| §12 | Shells: 66.9 / 0.3, ≥ 110 / 0.35, 63.2 / 0.4, ≥ 104 / 0.45, 16 runs each; the two ≥ cuts; maximum at the lowest filed energy | verified (index) |
| §12 | "within about 3.6 of the axis" for the shells | verified approximately (it is σ⊥ at arrival for E = 0.735; it varies with E) |
| §13 | a = 2.75 nm, 4.13 nm, 300 / 110 meV, 10.6 meV, 62 fs, 87 K, 131 / 274 mV | verified (CODATA via SciPy) |
| §13 | 0.30 eV offset for 35 % Al | unverifiable here (paper not opened); consistent with the usual ~0.65 ΔE_g |
| §13 | Bias peaks 0.735 / 0.483 / 0.226, heights 1 / 0.877 / 0.559 | verified (Airy-exact: 0.4828 / 0.8769, 0.2262 / 0.5592) |
| §13 | Areas 0.103 / 0.073 / 0.041; levels 0.29 / 0.1; supply 14.2 / 18; heights 0.65 / 0.34; widths 0.071 / 0.077 / 0.085; products 1.04 / 0.74 | verified (Airy-exact values; 0.103 from the generator) |
| §13 | I–V: peak 0.875, valley 1.825, PVR 4.3 | verified (Airy-exact curve agrees with stored `exact-1d.json` to 1.4×10⁻⁵ relative) |
| §13 | 170 of 500, about a third per voltage | verified |
| §13 | "a different third at each" | wrong (error 2) |
| §13 | Fig. 3 at V_b = 0.8: level ≈ 0.335 > E_F − eV_b = 0.2 | verified |
| Problems | 62 fs for Γ = 10.6 meV | verified |
