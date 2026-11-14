# Fig. 15 lecture note: derivation and number check, round 6

The note checked is `public/scripts/resonant-note.js` at HEAD 8cc9769 (03:28 UTC). It was committed while this check ran. I first read ada0993, then diffed it sentence by sentence against HEAD and checked every changed sentence again. The equations (1)–(32) are identical in both versions.

How each item was checked:
- **Equations.** Re-derived in SymPy 1.14, and checked against my own transfer-matrix code. That code is independent of tm.py: its own barrier matrices, its own staircase for the bias, its own I–V integral (scratchpad `derive_check.py`, output in `derive_out.txt`).
- **The NUM block.** `python3 notes/fig15/gen2_numbers.py` (print only, no `--write`) reproduces all 297 values exactly.
- **Run data.** The run-derived values were read again by hand from `2026-11-14/kaggle/index.json`. The generation-1 numbers of section 11 were read from `2026-11-13/kaggle/index.json` and by running `notes/fig15/gen1_profile_check.py`.
- **Rendered page.** The page was served on 127.0.0.1:9671 and rendered in headless Chrome 153 (`--dump-dom`). The rendered text (`paper_text.txt`) has KaTeX typeset, no `undefined`, `NaN` or `null`, and the tables filled.
- **Numerical method.** Compared line by line with `rt3d2.py`, `rt3d2_run.py`, `file_rt3d2.py`, `iv.py`, `exact1d.py`, `rt3d-worker.js`, `rt3d-view.js` and the page's `interp()`.

## Errors, ranked by severity

1. **Section 10, run length (method mismatch, medium).** The note says each run lasts "the packet's flight past the barriers plus three times the longest lifetime its energies can meet". That is the rule of the current `rt3d2.py`: the trailing edge, `+2 sx/v`, and a resonance scan of E±4σ_E±0.3 kept only inside E±4σ_E.
   - All 1237 filed runs come from shards 1–2 at commit cdcade4 (`index.json` notebooks). There the rule is `t_end = (x_r + 20 − x_0)/v + 3 τ_est`: the packet *centre's* flight, with τ_est scanned only over E±4σ_E, so peaks at the window edge could be missed.
   - The note mentions the older rule only for the running-example long packets.
   - Correct form: "The runs filed so far (parts 1–2) last the flight of the packet's centre to 20 a past the last face plus 3 τ_est (τ_est from the resonances inside E ± 4σ_E). Later parts add the trailing edge, 2σ_x/v. The 15 runs this lengthens by more than 15 % (FIX1) are to be rerun."
   - The quoted range 30–517 is correct for the filed runs.
2. **Section 13, the supply function (physics imprecision, minor).** "Below E_F it grows as E falls" holds only for E_F − eV_b ≲ E ≲ E_F, where S ≈ (E_F − E)/k_BT. Below E_F − eV_b the net supply saturates at S ≈ eV_b/k_BT, because the "more sideways states" argument applies to both leads and cancels in the difference.
   - The quoted cases are inside the growing range, so the numbers stand: level 0.29 > 0.125 at V_b = 0.875, and level 0.10 > −0.25 at V_b = 1.25.
   - Correct form: "Between E_F − eV_b and E_F it grows as E falls; further down it stays at eV_b/k_BT."
3. **Section 12, Shells (minor factual slip).** The note says the shells are "centred … at x = 0, where the walls and discs are centred too". That is true for pairs and for ten barriers. `rt3d2.centres()` puts single barriers and rows of three and five at c = 0.25, so that their faces fall on cell boundaries.
   - Correct form: "where the pairs of walls and discs are centred too".
4. **Section 13, "a different third at neighbouring voltages" (minor).** At neighbouring voltages half the filed energies are shared. For example V_b = 0.125 and 0.25 share 0.20, 0.50, 0.80 and 1.10. The filed third moves by one energy step (0.05) per voltage step. The repeat every 0.75 is correct.
   - Correct form: "shifted by one energy step at each voltage step, so neighbouring voltages share half their energies; the same third comes back every 0.75".
5. **Section 6, the d = 2 long-packet run (unverifiable, wording loose).** The note says the run "stops 509 time units after it starts, about one lifetime after the trapped wave peaks".
   - The run-length rule ends it 3 × 150 = 450 after the packet centre passes 20 a beyond the last face (t ≈ 61). The trapped wave fills while the packet passes.
   - So the end is roughly 1.3–1.4 τ (τ = 344) after the peak, unless the peak is later than t ≈ 120.
   - The curves are not in the local data, so this cannot be checked here. "About 1.3 lifetimes" is safer, or measure the peak time from the run file.

Nothing else is wrong. Every equation (1)–(32) re-derives as written.

## Equations

| Eq. | What was checked | Verdict |
|---|---|---|
| (1) | Units: in natural units ħ = m = 1 it becomes i∂ₜψ = −½∇²ψ + Vψ, as stated. | verified |
| (2) | SymPy: ψ = χ g(y) g(z) with χ, g obeying (2) leaves a residual of exactly 0 in (1). The removable time-only bracket and the phase e^{+i∫f dt} are correct. | verified |
| (3) and the stated g | SymPy: g = (1+it/2σ²)^{-1/2} exp[−y²/(4σ²(1+it/2σ²))] solves i g_t = −½ g_yy (residual 0). The variance of \|g\|² is σ²(1+(t/2σ²)²) exactly. Limit t→0 gives σ. Units: ħt/(mσ²) is dimensionless. Spread of sideways wave numbers 1/(2σ): correct. | verified |
| (4) | From −½χ'' + Vχ = Eχ. | verified |
| (5) | SymPy solve of continuity of χ and χ' reproduces the matrix exactly. | verified |
| (6) | SymPy product edge·diag(e^{κd}, e^{−κd})·edge, referred to the centre: M = [[w, γ], [γ*, w*]] with w = e^{ikd}[cosh κd + i(κ²−k²)/(2kκ) sinh κd] and γ = i(κ²+k²)/(2kκ) sinh κd. Both residuals are 0, det M = 1, and \|w\|² − \|γ\|² = 1. The ★ identities (1±iκ/k)(1±k/iκ) = 2 ± i(κ/k − k/κ) and 1 + η² = (κ²+k²)²/4k²κ² also hold. The conjugation and current arguments are sound. | verified |
| (7) | SymPy: \|w\|² − [1 + V₀² sinh²κd/(4E(V₀−E))] = 0, using κ² + k² = 2V₀ and k²κ² = 4E(V₀−E). | verified |
| (8) | T = 1/\|w\|², r = γ*/w, R = \|γ\|²/\|w\|² = 1 − T. Limits d→0 (T→1) and V₀→∞ (T→0) are correct. | verified |
| (9) | SymPy: lim_{d→∞} T_exact / [16E(V₀−E)/V₀² e^{−2κd}] = 1. | verified |
| (10) | Series against my own matrix product at E = 0.4, 0.735 and 1.3: equal to 12 digits. The symmetric-barrier r from the right equals r from the left, referred to the centre. | verified |
| (11) | SymPy series of T_aT_b/(1−√(R_aR_b))² to lowest order in T gives 4T_aT_b/(T_a+T_b)². The bound ≤ 1 follows from (T_a−T_b)² ≥ 0. | verified |
| (12) | θ = arg(r²) + 2ks for equal barriers. At E_r numerically θ = 1.9×10⁻⁸, i.e. 0 to the precision of the peak search. | verified |
| (13) | \|1−Re^{iθ}\|² = (1−R)² + 4R sin²(θ/2). Agrees with the exact matrix to 12 digits at 3 energies. Midway value T²/(1+R)² is correct. | verified |
| (14) | Follows from (13) (sin(θ/2) = 0 ⇒ T₂ = 1). | verified |
| (15) | SymPy: (4R/T²)(θ'(E−E_r)/2)² − (E−E_r)²/(Γ/2)² = 0 with Γ = 2T/(√R θ'). Half height at ±Γ/2. | verified |
| (16) | R^{2t/t_rt} = e^{−t/τ} gives 1/τ = −2 ln R/t_rt. SymPy: −2 ln(1−T) − 2T/√(1−T) = −T³/12 + …, so the claim "agree up to order T³" is right and τ = ħ/Γ follows. The step-phase rate d[−2 arctan(κ/k)]/dk = 2/κ (SymPy) supports L_eff = s − d + 2/κ. | verified |
| (17) | From (15) with t_rt ≈ 2L_eff/v and the factor 1/√R dropped. Units: ħv/L is an energy. Limits T→0 and R→0 are correct. | verified |
| (18) | Average over \|φ(k)\|² with σ_k = 1/(2σ_x): matches the Gaussian of ψ₀ (SD of \|ψ\|² = σ_x). Same weights as `exact1d.tbar` and `file_rt3d2` exact. | verified |
| (19) | SymPy: ∫(Γ/2)²/(x²+(Γ/2)²)dx / √(2π) = √(π/8) Γ. The Jacobian remark dE = ħ²k dk/m is correct. | verified |
| (20) | Even: χ'/χ = −k tan(kL/2) = −κ. Odd: k cot(kL/2) = −κ. The roots I solved for agree with the table. | verified |
| (21) | Hard walls at 1/κ inside each barrier give k = nπ/L_eff. Units are correct with ħ and m written out. | verified |
| (22) | tr P = w e^{−iks} + w* e^{iks} = 2 Re(w e^{−iks}) = 2cos(ks+φ)/√T. Numerical match to 10 digits, and det P = 1. | verified |
| (23) | Cayley–Hamilton P² = 2ξP − I, P^N = U_{N−1}P − U_{N−2}I, \|γ_N\|² = U²_{N−1} R/T. Agrees with the direct product for N = 2, 3, 5, 10 to 12 digits. N = 1 gives T. | verified |
| (24) | The eigenvalues of P have \|λ\| = 1 and cos(arg λ) = ξ inside the band (checked at E = 0.7). | verified |
| (25) | Matches `rt3d2.run`: halfV·p, ifftn(kin·fftn(p)) with kin = exp(−½i K² dt), halfV·p, then the border mask. Local error O(Δt³), global O(Δt²). The fastest diagonal mode turns by 0.592 rad per step. | verified |
| (26) | Matches the page's `interp()` (resonant-tunnelling.html lines 313–322): e^{iEΔt_f}ψ_{f+1}, linear blend, then e^{−iEδ}. | verified |
| (27) | Independent rates add. τ_side(R = 2) = 1/(1/1.985 − 1/15.12) = 2.28. | verified |
| (28) | Order-of-magnitude estimate. Units mRW/ħ are a time. R² and R regimes are correct. | verified |
| (29) | Same ramp as `iv.T_biased` (Uramp from x_l to x_r) and `rt3d2.vbias` (clip 0..1). | verified |
| (30) | SymPy: ∫₀^∞ dx/(1+e^{x−c}) = ln(1+e^c). Transverse density 2·2πk dk/(2π)² per dE = m/(πħ²). | verified |
| (31) | Flux per transverse state dE/(2πħ) times (30) gives the prefactor e m* k_BT/(2π²ħ³). Units: A m⁻². | verified |
| (32) | Matches `file_rt3d2.py` line 130: np.trapezoid(T·supply(E, V), E) with E_F = 1, kT = 0.05, walls using the twin T. The unit e m* k_BT E_u/(2π²ħ³) is consistent with (31). | verified |

## Method description against the code

| Claim | Verdict |
|---|---|
| Grid 0.5 a. 192×128×128 (96 a × 64 a); 256 points for ten barriers; 512 for long packets. | verified (`rt3d2_run.spec`, `jobs`) |
| Faces halfway between grid points (odd multiples of 0.25 a); shells are the points within d/2 of the radius. | verified (`centres`, `geometry`) |
| Absorbing border in the outer tenth, falling from 1 to 0 each step. | verified (W = max(4, n//10), sin^{1/8}, applied after every step) |
| Strang split, Δt = 0.01, complex64, about 1 ns per cell-step. | verified |
| Packet 14 a before the first face, or 4σ_x if larger (48 for σ_x = 12). | verified (`x0_of`) |
| Run length "flight past the barriers + 3 × the longest lifetime, cap 60 / 150, shells 30". | **wrong for the filed runs**, see error 1. The caps (60/150/30) are verified. |
| 200 frames; \|ψ\| in 8-bit levels of the frame's peak; arg ψ in steps of 2π/255; phase dropped where the level is < 3 and drawn as −π; plane z = 0, half y ≥ 0. | verified (`run`, `rt3d-worker.js` lines 6–35) |
| Rounding at most 0.2 % of the peak and 0.012 rad. | verified (0.5/255 = 0.196 %, π/255 = 0.0123) |
| 1D twin on the same x grid, mask and step; it counts what the border absorbed. | verified (`run1d`) |
| Mirror symmetry is exact except one cell off inside the side border. | verified (y grid −32 … 31.5; mask m[1] ≠ m[127]) |
| τ fit: from 60 % to 5 % of the peak, or to the end of the run. | verified (`fit_tau`; it also keeps only the first contiguous stretch and needs ≥ 6 points) |
| T_far: (right + well/2)/norm at the last frame before 10⁻³ reaches the end borders. | verified (`summary`) |
| For discs, "between" means between the planes and within the radius. | verified (`geometry`) |
| Colour table of 1025 steps; height clipped at ±1.25; 15b/15c curves blended linearly. | verified (`rt3d-view.js` lines 47–48; page lines 332, 433) |
| 3739 runs = A 1128 + B 188 + C 564 + D 376 + E 423 + F 1000 + G 60. | verified (`jobs()` counts; G has one resonance below 2.2 for each of the 4 structures) |
| Six parts on two T4 each; 1237 filed from 2 parts; 5.9 h. | verified ((10654.6 + 10695.4)/3600 = 5.93) |

## Numbers

Unless marked otherwise, "own" means computed by me independently, "NUM" means the NUM block (regenerated identically), and "index" means `index.json`.

| Where | Number in the note | Recomputed | Verdict |
|---|---|---|---|
| Abstract | 14 in a hundred | T = 0.14395 | verified |
| Abstract | grids up to 512×128×128 | code | verified |
| §1 | glass reflects about 4 % | ((1.5−1)/(1.5+1))² = 0.04 | verified |
| Fig. 1 | E/V₀ drawn near 0.5, true 0.37 | SVG (185−128)/115 = 0.50; 0.735/2 = 0.3675 | verified |
| Fig. 1 | runs at 0.30 … 2.60; diode from 0.10 | EGRID, EBIAS | verified |
| §2 | start 14 before face, 48 for the long packet | `x0_of` | verified |
| §2 | σ_x = σ_⊥ = 3 | spec sx = sp = 3 | verified |
| §2 | σ_⊥(40) = 7.3 | 7.311 | verified |
| §2 box | k = 1.212, 2π/k = 5.18, κ = 1.591, e^{−κd} = 0.204 | 1.2124, 5.182, 1.5906, 0.2038 | verified |
| §2 box | E/V₀ = 0.37 | 0.3675 | verified |
| §2 box | κd = 1.59 | 1.5906 | verified |
| §2 box | σ_E/Γ = 2.9 | 0.2021/0.07040 = 2.87 | verified |
| §3 key | sinh(1.591) = 2.351, \|w\|² = 6.95, T = 0.144 (14.4 %), \|r\| = 0.925 | 2.3514, 6.947, 0.14395, 0.9252 | verified |
| Ex. 3.1 | sinh(3.18) = 12.0, T = 6.4×10⁻³, 22 times smaller | 12.017, 6.397×10⁻³, 22.5 | verified |
| §3 | (9) gives 0.154 against 0.144 | 0.15448 | verified |
| §4 | matrix and series agree to 10⁻⁹ | agree to 10⁻¹² (own) | verified |
| §4 key | \|t₂\|² = 1.000 at 0.735 | 0.9999965 at 0.735; 1 − 10⁻¹⁴ at E_r = 0.734935 | verified |
| Ex. 4.1 | 2.1, 7.1, 13.9, 36.8, 67.1, 92.5, 99.9 % | identical (own partial sums) | verified |
| §4 | 0.144² = 2.1 % | 0.0207 | verified |
| §5 | E_r = 0.735 | 0.734935 | verified |
| §5 | θ a multiple of 2π to within 10⁻⁸ | 1.9×10⁻⁸ (own search), 5.6×10⁻⁹ (NUM). Both are set by the peak-search precision. | verified |
| §5 | ρ = −3.03, n = 0 | −3.0309; θ ≈ 0 | verified |
| §5 | 1/κ = 0.63, L_eff 2.76, half-wavelength 2.59 | 0.6287, 2.757, 2.591 | verified |
| §5 | ħθ' = 4.45, 2L_eff/v = 4.55 | 4.4538, 4.5487 | verified |
| §5 | −2 ln R = 0.3108, 2T/√R = 0.3111, 2T = 0.2879 | 0.31082, 0.31113, 0.28787 | verified |
| §5 | 1/√R = 1.08 | 1.0808 | verified |
| §5 key | Γ(15) = 0.0699, exact Γ = 0.0704, τ = 14.2, about 3 round trips | 0.069858, 0.070405, 14.204, 3.19 | verified |
| §5 key | v = 1.21, L_eff = 2.76, (17) gives 0.0633 | 1.2124, 2.7574, 0.06329 | verified |
| §5 | phase average T/(1+R) = 0.144/1.856 = 0.078 | 0.07756 | verified |
| §6 key | σ_E = 0.202 | 0.20206 | verified |
| §6 key | (19) gives 0.218; exact average 0.196 | 0.21835; 0.19591 | verified |
| §6 key | one barrier passes 0.149 | 0.14942 | verified |
| §6 | box 2.67 times longer | 512/192 | verified |
| §6 | σ_E(long) = 0.051, FWHM 0.119 | 0.05052, 0.11895 | verified |
| §6 | exact average 0.196 → 0.54 | 0.19591 → 0.53990 | verified |
| §6 | 5 long runs of 15; best passes 0.51 at E = 0.713; exact 0.5 | index: twin T 0.509842 at 0.713; NUM exact 0.5 (r3 of tbar) | verified |
| §6 | 0.0286 still trapped | index end.well 0.028631 | verified |
| §6 | peak run not yet filed | filed E 0.583 … 0.843, not 0.735 | verified |
| §6 | Γ(d = 2) = 0.00291 | 0.0029112 | verified |
| §6 | d = 2 long packet passes 0.0225 at E = 0.7215; exact 0.0319 | index twin T 0.022473; NUM | verified |
| §6 | run stops at 509 | index t_end 509.44 | verified |
| §6 | "about one lifetime after the trapped wave peaks" | peak time not in local data; the rule suggests ~1.3–1.4 τ | unverifiable, because the curves are on R2, not local (error 5) |
| §6 | 0.00736 trapped; half of it is "about two fifths of the shortfall" | 0.003679/(0.0319 − 0.0225) = 0.39 | verified |
| §6 | E_r(d = 2) = 0.744; (19) gives 0.0359; exact 0.0351 | 0.74358; 0.035903; 0.035136 | verified |
| §7 | e^{−2κd} = 0.04 | 0.0415 | verified |
| §7 | (21) gives 0.649 | 0.649 | verified |
| §7 table s = 2.5 | 0.735 / 0.744 / 2.193 / 0.0704 / 14.2 | identical (own) | verified |
| §7 table s = 3.5 | 0.388, 1.486 / 0.395, 1.445 / 0.790 / 0.0172 / 58.3 | identical (own) | verified |
| §7 table s = 4.5 | 0.238, 0.931 / 0.241, 0.933, 1.878 / 0.403 / 0.00606 / 165 | identical (own) | verified |
| §7 table s = 5.5 | 0.160, 0.633, 1.397 / 0.162, 0.638, 1.377 / 0.244 / 0.00267 / 375 | identical (own) | verified |
| §7 | above-top peak 2.028, width 0.314 | 2.0280, FWHM 0.3145 | verified |
| §7 | 3D run at E = 0.35, τ = 65.2, exact 58.3, 12 % longer | index tau 65.221; 58.29; +11.9 % | verified |
| §7 | second resonances near 0.931 and 0.633; 0.30 is the lowest run energy | own; EGRID | verified |
| §8 table V₀ = 1.5 | 0.64 / 1.31 / 0.248 / 0.116 / 0.0930 / 8.6 | 0.6405 / 1.311 / 0.2485 / 0.1163 / 0.09296 / 8.596 | verified |
| §8 table V₀ = 2 | 0.735 / 1.59 / 0.144 / 0.0704 / 0.0633 / 14.2 | identical (own) | verified |
| §8 table V₀ = 3 | 0.877 / 2.06 / 0.0526 / 0.0291 / 0.0282 / 34.4 | identical (own) | verified |
| §8 table d = 1.5 | 0.742 / 2.38 / 0.0316 / 0.0142 / 0.0139 / 70.4 | identical (own) | verified |
| §8 table d = 2 | 0.744 / 3.17 / 0.00657 / 0.00291 / 0.00290 / 344 | identical (own) | verified |
| §8 key | 22 times more opaque, 24 times narrower, 344 instead of 14.2 | 21.9, 24.2 | verified |
| §8 key | (17) gets every width within a quarter | worst ratio 0.80 | verified |
| §8 | d = 2 run: t_end 213, t₀ = 91, τ = 210 | index 212.93, 90.95, 209.664 | verified |
| §9 | band 0.590–0.955; gap 1.126; second band 2.082; width 0.365; midpoint 0.773 | 0.5898, 0.9552, 1.1264, 2.0816, 0.3654, 0.7725 | verified |
| §9 | ξ = 0 at 0.735 | −2.5×10⁻⁸ at E_r | verified |
| §9 | N = 3 peaks 0.657, 0.830; N = 5 0.614, 0.685, 0.791, 0.902; N = 10 nine values | identical (own); T_N = 1 to 10⁻¹⁴ | verified |
| §9 | (23) agrees to 2.3×10⁻¹² at 251 energies | NUM regenerates; own agreement ~10⁻¹² | verified |
| §9 | peaks 0.02 to 0.17 apart | 0.018 … 0.173 | verified |
| §9 | ten-wall runs: band 0.129 (exact 0.158), gap 0.0218 (exact 0.032) | mean of the 4 index twin T values; NUM | verified |
| §10 | 3739 runs; group counts | `jobs()` | verified |
| §10 | start share in barrier at most 2.1×10⁻⁵ | index max 2.093×10⁻⁵ | verified |
| §10 | runs from 30 to 517 | index 29.85 … 517.4 | verified |
| §10 | 1237 runs, 2 parts, 5.9 h | index | verified |
| §10 | three million points or more | 192·128·128 = 3.15 M | verified |
| §11 | 115 runs in the earlier batch | 2026-11-13 index: 115 | verified |
| §11 | 3D vs twin at most 1.8×10⁻⁴ | sep_check_max 1.797×10⁻⁴ (E = 0.735) | verified |
| §11 | twin 0.186, exact 0.196, 5 % | 0.186134, 0.195912, 5.3 % | verified |
| §11 | 22 % more at E = 0.4 | 0.042364/0.034651 = 1.223 | verified |
| §11 | 20 % less, 0.0564 vs 0.0706 at 1.2 | 0.05639/0.070597 = 0.799 | verified |
| §11 | 3.0 % / 2.4 % / 5.8 % / 66 % | gen1_profile_check.py: 0.0300 / 0.0243 / 0.0584 / 0.664 | verified |
| §11 | τ 15.1 (3D), 15.3 (twin) vs 14.2, 6–8 % | 15.112, 15.33; +6.4 %, +7.9 % | verified |
| §11 | T_far 0.179 vs 0.186, 4 % | 0.17933; 3.7 % | verified |
| §12 | 3.6 at t ≈ 12 (14 at about 1.2) | 3.564; 14/1.2124 = 11.5 | verified |
| §12 | R = 2: 0.936 at E = 0.65 | index T_far 0.93584 | verified |
| §12 | walls 15.1 at 0.65 | index 15.12 | verified |
| §12 table | walls 0.176 | index twin 0.17565 | verified |
| §12 table | R = 2: τ 1.99, τ_side 2.28, estimate 4 | 1.985; 2.28; 2·2 | verified |
| §12 table | one disc R = 4: 0.678; R = 6: 0.415 | index 0.67827, 0.41466 | verified |
| §12 table | estimates 12, 18, 27, 36 | R·min(R, 3) | verified |
| §12 key | R = 2 shorter than one round trip | 1.99 < 4.45 | verified |
| §12 shells | 66.9 @ 0.30; ≥ 110 @ 0.35; 63.2 @ 0.40; ≥ 104 @ 0.45; 16 runs each | index; cut flags right for (3, 3.5) and (5, 3.5) only | verified |
| §12 shells | "several times walls"; each at the lowest filed energy; wider s lives longer | 4–7×; minE = taumax_E for all four | verified |
| §13 | a = 2.75 nm; well 4.13 nm; 300 meV; 110 meV; 10.6 meV; 62 fs; 4.39 fs | 2.7536; 4.130; 110.2; 10.56; 62.3; 4.388 | verified |
| §13 | ΔE_c ≈ 0.30 eV at 35 % Al | Vurgaftman 2001 parameters at 0 K give 0.29 eV | verified (to the stated "about") |
| §13 | E_F = 1.0 = 150 meV; k_BT = 0.05 = 87 K | 87.03 K | verified |
| §13 | peaks 0.735, 0.483, 0.226; heights 1.0, 0.877, 0.559 | own staircase 0.7349, 0.4826, 0.2261; 1.000, 0.8769, 0.5592 | verified |
| §13 | levels 0.29, 0.10; supply 14.2, 18.0 | 0.291, 0.098; 14.15, 18.04 | verified |
| §13 | areas 0.103, 0.073, 0.041 | 0.1030, 0.0730, 0.0405 | verified |
| §13 | peak heights 1, 0.65, 0.34; widths 0.071, 0.077, 0.085 | 1.000, 0.652, 0.342; 0.071, 0.077, 0.085 | verified |
| §13 | area "a little less than πΓ/2" | 0.103 < 0.1106 | verified |
| §13 | products 1.04, 0.74 | 1.037, 0.738 | verified |
| §13 | exact I–V: peak 0.875 (131 mV), valley 1.825 (274 mV), PVR 4.3 | own I–V: 0.875, 1.825, 4.32 | verified |
| §13 | 170 of 500 wall runs, "about a third"; repeats every 0.75 | index: 170; 8–12 of 25 per voltage; period 6 × 0.125 | verified |
| §13 | "a different third at neighbouring voltages" | neighbours share half their energies | wrong, because of the overlap (error 4) |
| §13 | "below E_F it grows as E falls" | saturates below E_F − eV_b | wrong, because it is incomplete (error 2) |
| Fig. 3 | V_b = 0.8, E_r 0.735, E_F 1, levels drawn to scale | SVG: 44 px per unit; collector drop 0.795; dashed level 0.727; lit level 0.327; collector E_F 0.2 | verified |
| Fig. 2 | strips, band shading 0.590–0.955, x range 0.3–1.3 | gen2_numbers FIG2 code | verified |
| §13 box | 1.92 THz (Maekawa 2016) | the cited paper's title | verified |
| §14 | lifetimes 6–8 % long; box 64 a wide | as §11; 128 × 0.5 | verified |
| Problem 3 | L_eff = 2.76 a = 7.6 nm | 7.59 nm | verified |
| §12 shells | "centred at x = 0, where the walls and discs are centred too" | single barriers and rows of 3 and 5 sit at 0.25 | wrong, because of the centres (error 3) |
| §10 | run-length rule | old rule for all filed runs | wrong, because of the commit (error 1) |
