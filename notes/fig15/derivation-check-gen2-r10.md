# Fig. 15 lecture note: derivation and number check, generation 2, round 10

Checked version: `public/scripts/resonant-note.js` at commit ad6738d (md5 7d06b8d8…), with `notes/fig15/gen2_numbers.py` at the
same commit. The branch head moved while I worked: 4bae4a5 → eb4147d → ad6738d → 01902ee. The last commit (01902ee, "READY at
ad6738d") changes only `NOTE_STATE.md`, so the note at the head is the note at ad6738d. I did the first full pass at 4bae4a5. I then
re-rendered at ad6738d, diffed the rendered text sentence by sentence, and re-checked every changed sentence and number.

How I checked:
- I rendered the page in headless Chromium (Playwright, page served from `public/`, all `<details>` opened). Result: 1086 KaTeX
  blocks, 0 KaTeX errors, tags (1)–(32) in order, 0 page errors, and no NaN, undefined, null or "to come" in the text.
- The NUM block is identical to a fresh run of `gen2_numbers.py` (382 keys, all equal). FIG2 is identical to the script's SVG.
- I re-derived the equations in SymPy myself (scratchpad `r10/sym.py`).
- I recomputed the 1D numbers with my own code. None of it uses `tm.py`, `iv.py` or `exact1d.py`:
  - a global-x transfer matrix, with faces aligned to the slices for the bias;
  - a vectorised staircase;
  - a DOP853 ODE integration under bias;
  - a k-space packet average converged in the number of points.
- I recomputed the run numbers from `2026-11-14/kaggle/index.json` directly.
- The run files are not reachable: `/r2/…` answers 404. So for the trapped-wave comparison I re-ran the page's own 1D twin solver,
  `rt3d2.run1d`, with each run's spec and step count. It reproduces the index's twin T and R to 1×10⁻⁶ for all 9 runs I re-ran.
- I verified the earlier-batch numbers of section 11 from `2026-11-13/kaggle/index.json` and by running
  `notes/fig15/gen1_profile_check.py`.

## Errors found

1. **Side-border loss of the trapped wave: 19 %, 40 %, 45 % (section 11; repeated in section 7 as "40 %" and section 8 as
   "45 %").** Wrong, because the comparison mixes two regions.
   - `gen2_numbers.py` (keys `sl_*`) compares the 3D `end.well`, which is the probability between the inner faces only, with the
     twin's `1 − T − R`, which is everything between the outer faces, including the inside of both barriers.
   - Compared over the same region (the twin profile at the last frame, integrated between the inner faces, from `rt3d2.run1d`
     re-run), the 3D trapped share is lower by:

     | Run | Twin, well only | 3D well | 3D below twin | Note says |
     |---|---|---|---|---|
     | E = 0.75, t = 78 | 0.005135 | 0.004852 | **5.5 %** | 19 % |
     | s = 3.5, E = 0.40 | 0.008956 | 0.005754 | **36 %** | 40 % |
     | d = 2, E = 0.75 | 0.007164 | 0.004609 | **36 %** | 45 % |

   - For the running example, most of the "19 %" is the probability inside the barriers: 0.00087 of the twin's 0.00601.
   - The qualitative point stands: the side border shortens 3D lifetimes, and more so in long runs. But the running example loses
     about 5 %, not about a fifth.
   - Also: "(time 219)" is given for the long runs of sections 7 and 8 together. The section 8 run (d = 2) ends at 217, as section 8
     itself says.

2. **Section 10, grid accuracy: "from 0.32 to 0.92 times for d = 2, s = 3.5".** Wrong, because the lower bound is 0.30.
   - At E = 0.95 the twin passes 0.001747 and the converged exact packet average is 0.005878, a ratio of 0.297. With 4001, 20001 and
     80001 k-points I get 0.0058783, 0.0058784 and 0.0058784.
   - The index's `twin.T_exact` (`rt3d2_run.T_packet`, 1201 k-points over ±8σ_k) gives 0.005502 there. That grid has a step of
     about 0.0027 in energy, as wide as this resonance (Γ = 0.0029), so it undersamples the peak.
   - The upper bound 0.92 (0.918 at 2.60) is right. The other two ranges are right with converged exact values: 0.80–1.37 for the
     running example and 0.69–1.80 for V0 = 3.

3. **Section 10: "the waves the runs actually carry, with k up to about 2.3, turn by less than 0.03 rad per step".** Wrong,
   because 2.3 is only the mean wave number at the highest stored energy (√5.2 = 2.28).
   - The packet holds k up to about k0 + 3σ_k = 2.78, which turns by 0.039 rad per step.
   - The diode runs (E up to 1.30, bias up to 2.375) carry transmitted waves with k = √(2·3.675) = 2.71 at the mean energy, which
     turns by 0.037 rad. Their 3σ tail reaches k ≈ 3.0, which turns by 0.046 rad.
   - Correct: k up to about 3, turning by less than about 0.05 rad per step. The conclusion (far below the 0.2 rad limit) is
     unchanged.

4. **Section 12, Key result: "1.14 at radius 12".** Wrong, because from the stored shares the ratio is 0.18347/0.15992 = 1.147,
   which rounds to **1.15**.
   - The JS computes the ratio from the 3-digit NUM values: 0.183/0.160 = 1.144.
   - Radius 6 (1.056 → 1.06) and radius 2 (0.994 → 0.99) are right either way.

5. **Section 9: "Above about 1.8 the share rises again".** Wrong as to where the rise starts.
   - The ten-wall share is lowest at E = 1.40 (0.0115). From there it rises: 0.0127 at 1.45, 0.0161 at 1.5, 0.0220 at 1.55,
     0.0306 at 1.6, 0.0984 at 1.8.
   - Three and five walls behave the same way, with their minimum also at 1.40.
   - Correct: the share rises again above about 1.4 (it reaches 0.1 near 1.8). Note that the gap average "between 1.1 and 1.6"
     already includes the start of this rise.

Everything else checks.

## Equations

| Eq. | Verdict | How |
|---|---|---|
| (1) | verified | Units: ħ∂ψ/∂t and ħ²∇²ψ/2m are both energies × ψ. With ħ = m = 1 it becomes i∂tψ = −½∇²ψ + Vψ. E_u = ħ²/ma², t_u = ma²/ħ consistent. |
| separation, phase removal | verified | SymPy: the product χgg solves (1) when each factor solves (2) (residual 0); i∂t(e^{iF}c) = e^{iF}(iċ − fc) (residual 0). |
| (2) | verified | SymPy: the spreading Gaussian g ∝ (1+it/2σ²)^{-1/2}exp[−y²/4σ²(1+it/2σ²)] solves i g_t = −½g_yy (residual 0). |
| (3) | verified | SymPy: variance of \|g\|² is σ²(1 + (t/2σ²)²); units ħt/mσ² dimensionless; t = 0 gives σ⊥. |
| (4) | verified | χ'' = −2(E − V)χ in flat regions. |
| (5) | verified | SymPy solve of continuity of χ, χ' (residual 0). |
| (6) | verified | SymPy product W_k(−d/2)⁻¹W_{iκ}(−d/2)W_{iκ}(d/2)⁻¹W_k(d/2): M00 = w = e^{ikd}[cosh κd + iη sinh κd], M01 = γ = i(κ²+k²)/(2kκ) sinh κd, M10 = γ*, M11 = w*, det 1, \|w\|² − \|γ\|² = 1 (all residual 0). Face-referred top-left element and the identity (1 ± iκ/k)(1 ± k/iκ) = 2 ± i(κ/k − k/κ) also residual 0. |
| (7) | verified | SymPy: cosh² + η² sinh² with k = √2E, κ = √2(V0−E) equals (7) (residual 0). |
| (8) | verified | T = 1/\|w\|² from (6) with D = 0; SymPy limit d → 0 gives 1; V0 → ∞: sinh² ~ e^{2κd} beats the prefactor ~ V0/4E. R = 1 − T from \|w\|² − \|γ\|² = 1. |
| (9) | verified | SymPy: (8)/(9) → 1 as d → ∞. |
| (10) | verified | Geometric series; own code: matches the transfer-matrix product to 2×10⁻¹⁵ at E = 0.4, 0.735, 1.2. |
| (11) | verified | SymPy: leading term of T_aT_b/(1 − √R_aR_b)² for small T is 4T_aT_b/(T_a+T_b)²; (T_a+T_b)² − 4T_aT_b = (T_a−T_b)². |
| (12) | verified | Definition. |
| (13) | verified | SymPy: \|1 − Re^{iθ}\|² = (1−R)² + 4R sin²(θ/2) and the resulting form (residual 0); midway value T²/(1+R)². |
| (14) | verified | Own code: θ(E_r) = 9×10⁻⁹ rad from 0 (n = 0 with ρ = −3.031). |
| (15) | verified | SymPy: the expanded term equals (E−E_r)²/(Γ/2)² with Γ = 2T/(√R θ'). |
| (16) | verified | SymPy: −2 ln R − 2T/√R = −T³/12 − T⁴/8 + …: agree to order T³ as stated. ħ/Γ is a time. |
| (17) | verified | ħv/L_eff is an energy; limits T → 0, R → 0 as stated. Single-step phase −2 arctan(κ/k) has dk-rate 2/κ (SymPy, residual 0). |
| phase average 1/√(1+F) | verified | SymPy: (1/π)∫du/[1+(1+F)u²] = 1/√(1+F); dθ = 2du/(1+u²); 1+F = (1+R)²/T²; T²/(1−R²) = T/(1+R). |
| (18) | verified | Definition; own packet average 0.19591 at E_r. |
| (19) | verified | SymPy: ∫Lorentzian/(√(2π)σ_E) = √(π/8)Γ/σ_E. |
| (20) | verified | SymPy: χ'/χ at L/2 is −k tan(kL/2) (even), k cot(kL/2) (odd). |
| (21) | verified | Units ħ²/mL² is an energy; own value 0.649. |
| (22) | verified | SymPy: Re(e^{−iφ}e^{−iks}/√T) = cos(ks+φ)/√T; ½ tr P = Re(w e^{−iks}) since the trace is w e^{−iks} + w* e^{iks}. |
| (23) | verified | SymPy: P^N = U_{N−1}(ξ)P − U_{N−2}(ξ)I for N = 2, 3, 4, 5 on a general det-1 matrix; U_4(cos β) = sin 5β/sin β; own code agrees with the direct product to 1.9×10⁻¹³ (N = 2, 3, 5, 10; 251 energies). |
| (24) | verified | SymPy: characteristic polynomial λ² − 2ξλ + 1. |
| (25) | verified | `rt3d2.run`: halfV · ifftn(kin · fftn(·)) · halfV, then mask; Δt = 0.01. |
| (26) | verified | SymPy: exact for a wave e^{−iEt}φ (residual 0); page `interp()` implements it line by line (cr, ci = e^{iEΔt}; cp, sp = e^{−iEδ}). |
| (27) | verified | Rates add; a model, stated as such. |
| (28) | verified (order of magnitude) | mRW/ħ is a time; R², then 3R scaling as stated. |
| (29) | verified | `rt3d2.vbias`: linear drop from the first to the last outer face, 0 left, −bias right. |
| (30) | verified | SymPy: 2·2πk dk/(2π)² ÷ (ħ²k dk/m) = m/πħ²; ∫₀^∞dx/(1+e^{x−c}) = ln(1+e^c). |
| (31) | verified | SymPy prefactor (m kT/πħ²)/(2πħ) = m kT/(2π²ħ³); supply → ln(1+e^{c}) as eV_b → ∞ (the "levels off" sentence). |
| (32) | verified | Trapezoid over the 25 stored energies; recomputed from the 500 runs per structure (rows below). |
| radial equation, shells | verified | SymPy: (1/r²)(r²f')' = (1/r)(rf)''. |

## Numbers

| § | Number in the note | Recomputed (own code unless stated) | Verdict |
|---|---|---|---|
| Abstract | 14 in a hundred; 512 × 128 × 128 | T = 0.14395; index boxes (192, 256, 512) × 128 × 128 | verified |
| 1 | about 4 % per glass surface | ((1.5−1)/(1.5+1))² = 0.04 | verified |
| Fig. 1 | E/V0 0.37; energies 0.30…2.60; 0.70, 0.75; diode to 0.10 | 0.3675; `EGRID`, `EBIAS` | verified |
| 2 | a = 2.75 nm | ħ/√(0.067 m_e · 150 meV) = 2.754 nm | verified |
| 2 | x0 14 before the face; σ 3; long σ 12, 48 before | `x0_of`: max(14, 4σx) | verified |
| 2 | σ⊥(40) = 7.3; σ_xσ_k = ½ | 7.31; Fourier pair | verified |
| 2 | k 1.212, 2π/k 5.18, κ 1.591, e^{−κd} 0.204; κd 1.59; σ_E/Γ 2.9 | 1.21244, 5.1823, 1.59060, 0.20380; 2.870 | verified |
| 3 | sinh 2.351, \|w\|² 6.95, T 0.144 (14.4 %), \|r\| 0.925 | 2.35144, 6.9469, 0.143950, 0.92523 | verified |
| 3 Ex. 3.1 | sinh(3.18) 12.0, 3.72, 6.4×10⁻³, 22.5 | 12.017, 3.7191, 6.397×10⁻³, 22.50 | verified |
| 3 | (9) gives 0.154 | 0.15448 | verified |
| 4 | agreement 10⁻⁹; \|t₂\|² 1.000 | 2×10⁻¹⁵ (own); T₂(E_r) = 1 − 4×10⁻¹⁵ | verified |
| 4 Ex. 4.1 | 2.1, 7.1, 13.9, 36.8, 67.1, 92.5, 99.9 %; 0.144² = 2.1 % | 2.07, 7.14, 13.89, 36.77, 67.08, 92.50, 99.93 % | verified |
| 5 | phase within 10⁻⁸; ρ = −3.03, n = 0; 2ρ ≈ −2π | 9×10⁻⁹; −3.0310 | verified |
| 5 | 1/κ 0.63; L_eff 2.76; half-wavelength 2.59; within 7 % | 0.6287; 2.7574; 2.5913; 6.4 % | verified |
| 5 | ħθ' 4.45; 2L_eff/v 4.55 | 4.4538; 4.5487 | verified |
| 5 | 0.3108, 0.3111; 0.2879; 1/√R 1.08 | 0.31082, 0.31113; 0.28787; 1.0808 | verified |
| 5 | Γ(15) 0.0699; exact 0.0704; τ 14.2; about three round trips | 0.069858; FWHM 0.0704047; 14.204; 14.20/4.454 = 3.19 | verified |
| 5 | (17): v 1.21, L_eff 2.76, 0.0633 | 1.2124, 2.757, 0.063286 | verified |
| 5 | T/(2−T) = 0.144/1.856 = 0.078; about half of one barrier | 0.07755; 0.54 | verified |
| 6 | σ_E 0.202; about three times Γ; (19) 0.218; exact 0.196; 11 % high | 0.20206; 2.87; 0.21835; 0.19591; 11.5 % | verified |
| 6 | one barrier 0.149; about a third more; factor of seven | 0.14940; 1.311; 6.95 | verified |
| 6 | 512 vs 192, 2.67×; FWHM 0.119; σ_E 0.051; σ_E/Γ 0.7; 0.196 → 0.54 | 2.667; 0.11895; 0.050516; 0.717; 0.5399 | verified |
| 6 | long table, share through: 0.488, 0.524, 0.0197, 0.0225, 0.188, 0.257 | index twin T: 0.487703, 0.524056, 0.019661, 0.022473, 0.187836, 0.257495 | verified |
| 6 | with half the twin's trapped wave: 0.493, 0.529, 0.0272, 0.0318, 0.193, 0.265 | T + (1−T−R)/2 from the index: 0.49274, 0.52929, 0.02718, 0.03181, 0.19306, 0.26510 | verified |
| 6 | exact average: 0.540, 0.500, 0.0351, 0.0319, 0.271, 0.195 | own packet average (σx = 12): 0.53972, 0.49972, 0.03513, 0.03190, 0.27106, 0.19512 | verified |
| 6 | V0 = 3: 36 % above, 29 % below | 0.26510/0.19512 = 1.359; 0.19306/0.27106 = 0.712 | verified |
| 6 | d = 2: Γ 0.00291; 509 > 344; 0.0187 trapped; 0.0318 vs 0.0319; nearest 23 % low | 0.0029115; t_end 509.44; 0.01868; 0.03181/0.03190; 0.02718/0.03513 = 0.774 | verified |
| 6 | 3D trapped part lost in long runs ("much") | twin well-only vs 3D well (re-run twin): 18–19 % (running example), 54 % (d = 2), 29 % (V0 = 3) | verified |
| 6 | (19) at 0.744: 0.0359; exact 0.0351 | 0.03590; 0.03514 | verified |
| 7 | e^{−2κd} 0.04; (21) 0.649 vs 0.735 | 0.0415; 0.6491 | verified |
| 7 | table: resonances, finite well (20), hard box, Γ, τ for s = 2.5…5.5 | own: 0.7349; 0.3881, 1.4856; 0.2379, 0.9306; 0.1603, 0.6331, 1.3967; finite well 0.744; 0.3946, 1.4455; 0.2414, 0.9325, 1.8778; 0.1623, 0.6379, 1.3769; box 2.193, 0.790, 0.403, 0.244; Γ 0.0704, 0.01716, 0.006065, 0.002665; τ 14.2, 58.3, 164.9, 375.2 | verified |
| 7 | 2.028 spread 0.314; hundredths / few hundredths | 2.02799, 0.31439; differences ≤ 0.009 and ≤ 0.041 | verified |
| 7 | run 0.4: 68.4 vs 58.3, 17 %; 0.931, 0.633 | index τ 68.366; 1.1735 | verified |
| 7 | **40 % side-border loss** | 36 % (same region) | **wrong**, see error 1 |
| 8 | table V0, d rows: E_r, κd, T, Γ exact, Γ(17), τ | own: 0.6405/1.311/0.2485/0.1163/0.0930/8.60; 0.7349/1.591/0.1439/0.0704/0.0633/14.2; 0.8772/2.060/0.05259/0.02906/0.0282/34.4; 0.7421/2.379/0.03156/0.01421/0.01393/70.4; 0.7436/3.170/0.006568/0.002911/0.00290/343.5 | verified |
| 8 | 22×, 24×; within a quarter | 21.9, 24.2; worst ratio 0.799 | verified |
| 8 | 0.735, 0.742, 0.744; 0.877; 0.64 | as above | verified |
| 8 | d = 2 run: 217, 92.7, 210; window 124, about 0.4 lifetime | index t_end 216.91, t0 92.65, τ 209.54; 124.3, 0.36 | verified |
| 8 | **45 % below the twin's** | 36 % (same region) | **wrong**, see error 1 |
| 9 | band 0.59–0.955; gap 1.126; 2.082; band 0.365 wide, midpoint 0.773 | own Kronig–Penney: 0.58983, 0.95522, 2.08158; 1.12635; 0.36539; 0.7725 | verified |
| 9 | peaks N = 3, 5, 10; ξ(0.735) = 0; 0.02 to 0.17 apart; 2.3×10⁻¹² | own peak search: same 2 + 4 + 9 values; ξ = 3×10⁻⁵; spacings 0.018–0.173; own direct product vs (23) 1.9×10⁻¹³ (both at round-off) | verified |
| 9 | 8 band runs 0.6–0.95 mean 0.143 (exact 0.174); 11 gap runs 1.1–1.6 mean 0.0237 (exact 0.0351) | index: 0.143462 (exact 0.17439); 0.023682 (exact 0.035061) | verified |
| 9 | **"Above about 1.8 the share rises again"** | minimum 0.0115 at 1.40, rising from 1.45 | **wrong**, see error 5 |
| 10 | 0.5 a; 96 a, 64 a; 256, 512; outer tenth; sin^{1/8}(πℓ/2b) | `setup`: W = max(4, n//10), m = sin(½πe/W)^0.125 | verified |
| 10 | Δt 0.01; about 10 points per wavelength (5.5 at 2.60); k 6.28, 0.2 rad; diagonal 0.6 rad | 10.4, 5.51; 0.197, 0.592 | verified |
| 10 | **k up to about 2.3, less than 0.03 rad** | about 3, up to 0.046 rad | **wrong**, see error 3 |
| 10 | three million points; 0.92 ns | 3.15×10⁶; 0.9218 | verified |
| 10 | group counts 1128/188/564/376/423/1000/60 = 3739; 47 and 25 energies; 60/150/30 caps | index groups: identical; `jobs`, `tau_est` | verified |
| 10 | 2.1×10⁻⁵; 15 reruns; 30–537; 6 + 1 parts on T4 pairs; 18.6 h; 35.6 h; 42 (21 × 2); 3697 | 2.093×10⁻⁵; 15; 29.85–537.3; 7 notebooks, Tesla T4 × 2; 18.565; 35.599; 42; 3697 | verified |
| 10 | 200 frames; 0.2 % of the peak; 0.012 rad; 3 steps = 1.2 %; 1025 steps; ±1.25 | `run`, `rt3d-view.js` LUT, page `buildSheet` | verified |
| 11 | 115 runs; 15.1; 1.8×10⁻⁴; 0.186 vs 0.196 (5 %); 22 % at 0.4; 0.0564 vs 0.0706 | 2026-11-13 index: 115; 15.112; 1.797×10⁻⁴; 0.186134/0.195912; 1.223; 0.05639/0.070597 | verified |
| 11 | 3.0 %, 2.4 %, 5.8 %, 66 % | ran `gen1_profile_check.py`: 0.0300, 0.0243, 0.0584, 0.664 | verified |
| 11 | 15.1, 15.3 vs 14.2: 6–8 %; 1/κ 0.63 = 1.3 grid spacings; two grid points thick | 15.112, 15.33; 6.4 %, 7.9 % | verified |
| 11 | **19 % below the twin's (t = 78); 40 % and 45 % (time 219)** | 5.5 %, 36 %, 36 %; the d = 2 run ends at 217 | **wrong**, see error 1 |
| 11 | ratios 0.8–1.37; V0 = 3 0.69–1.8 | own converged exact: 0.800–1.368; 0.695–1.802 | verified |
| 11 | **d = 2: 0.32–0.92** | 0.297–0.918 | **wrong**, see error 2 |
| 11 | 60 %–5 % fit; T_far rule; 0.1785 vs 0.1870, 4.5 %; about 5 % | `fit_tau`, `summary`; index 0.1785, 0.186957, 4.52 % | verified |
| 12 | 39 % within 3, 86 % within 6; 3.6 at t ≈ 12; 1.2 | 0.393, 0.865; 3.56 at 11.5 | verified |
| 12 | disc table: τ, τ_side, R·min(R, 3), pair, one disc | index: 12.87/85.9/36/0.1835/0.1599; 12.557/73.6/27/0.2312/0.2057; 9.058/22.55/18/0.4375/0.4142; 3.687/4.874/12/0.6886/0.6742; 1.881/2.148/4/0.9261/0.9315; walls 15.138/0.18696/0.15403 | verified |
| 12 | 76.1, 88.5 from rounded; within a factor of about 3; 2→4 less, 4→6 more | 76.10, 88.54; ratios 0.41–2.73; 2.27 vs 3, 4.63 vs 1.5 | verified |
| 12 | 1.88 and 3.69 shorter than a round trip 4.45 | yes | verified |
| 12 | **ratios 1.14**, 1.06, 0.99; difference near 0.02 | 1.147, 1.056, 0.994; 0.0235, 0.0255, 0.0234 | **1.14 wrong**, see error 4; rest verified |
| 12 | shells: single 42.2 (3, 0.35), ≥ 103 (5, 0.3); pairs 66.9, ≥ 112, 89.2, ≥ 125 at 0.30, 47 runs; ≥ marks | index; fit window ends at t_end and spans less than τ for exactly the three marked | verified |
| 13 | table: 2.75, 4.13 nm; 300, 110, 10.6 meV; 62 fs; 4.39 fs | a = 2.754 nm; 150 × 0.735 = 110.3; 150 × 0.0704 = 10.56; ħ/E_u = 4.388 fs; 14.2 × 4.388 = 62.3 | verified |
| 13 | peaks 0.735, 0.483, 0.226; heights 1, 0.877, 0.559 | staircase aligned to faces (700 cells) and ODE: 0.7349, 0.4826, 0.2233 (1181-point grid search; ODE agrees); heights 1.000, 0.8769, 0.557 | verified |
| 13 | E_F 1.0, kT 0.05 (87 K); 131 mV, 274 mV | 7.5 meV / k_B = 87.0 K; 150 × 0.875, 150 × 1.825 | verified |
| 13 | exact curve top 0.875, valley 1.825, ratio 4.3 | own staircase Tsu–Esaki, 0.025 V steps: 0.875, 1.825, 4.319 | verified |
| 13 | levels 0.29, 0.1; supply 14.2, 18; areas 0.103, 0.073, 0.041; heights 1, 0.65, 0.34; widths 0.0704, 0.077, 0.085; products 1.03, 0.73 | 0.2905, 0.0980; 14.154, 18.038; 0.10298, 0.07298, 0.04055; 1.000, 0.652, 0.342; 0.0705, 0.0773, 0.0846; 1.0329, 0.7314 | verified |
| 13 | runs: 0.75, 1.625, 4.4 (500 runs); same-energy sum 0.75, 1.75, 4.8; 0.0704; 0.05 apart | index runs: 0.75, 1.625, 4.367 (n = 500); own staircase: 0.75, 1.75, 4.811 | verified |
| 13 | discs: 3.46 at 0.75, 2.82 at 2.375, 1.2; walls 0.96; several times | 3.4617, 2.8210, 1.227; 0.9597; 3.6× | verified |
| Fig. 3 | V_b = 0.8, E_F = 1, levels and offsets | SVG: 44 px per unit; drop 35 px = 0.80; level drawn at 0.327 vs own peak 0.329; collector 0.2 = E_F − eV_b | verified |
| 14 | 6–8 %; 17 %; 64 a | as above | verified |
| Problems | Γ 10.6 meV; L_eff 2.76 a = 7.6 nm; 110 meV; τ 1.88, 15.1 | 7.60 nm | verified |
| 13 | 0.30 eV offset for 35 % Al (Vurgaftman et al. 2001); 1.92 THz (Maekawa et al. 2016) | not re-read this round | unverifiable, because the sources were not read here (1.92 THz matches the cited title) |

## Numerical method against code

The method text matches the code line by line:
- `rt3d2.py`:
  - the grid and box;
  - faces on odd multiples of 0.25;
  - the absorbing border sin^{1/8} in the outer tenth (0 at the outermost point, 1 inside);
  - the Strang step and mask;
  - the packet start;
  - storage on z = 0, half y ≥ 0, with 8-bit |ψ| and arg ψ, the phase code 0 (−π) below 3 levels, and the probability along x and the
    region probabilities;
  - `run1d` on the same x grid and step.
- `rt3d2_run.py`:
  - the group sizes;
  - the energy grids;
  - the run length: flight of the trailing edge plus 3τ, with τ capped at 60, 150 or 30;
  - the 15 FIX1 reruns.
- `file_rt3d2.py`:
  - the 60 %–5 % lifetime fit, or to the end of the run;
  - T_far as the last frame before 10⁻³ reaches the end borders, (right + well/2)/norm;
  - the twin T;
  - the trapezoid J.
- The page `interp()` is equation (26), and the profiles are mixed linearly. In `buildSheet`, the scale is the largest stored peak,
  the height is clipped at ±1.25 and the colour comes from the 1025-step table. The border is one cell off mirror symmetry
  (n = 128, the axis runs from −32 to 31.5).

The one mismatch between the text and the numbers is the trapped-share comparison of error 1: `gen2_numbers.py` sets `sl_*` from
`end.well` (between the inner faces) against the twin's `1 − T − R` (between the outer faces).
