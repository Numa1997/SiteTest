# Fig. 14 lecture note: independent check

Page: `public/simulations/schrodinger-sphere.html`, `article#paper` (lines 137 to 591), at commit `0c22270`.
Checked on 12 November 2026 by a reader who did not write the note and did not read `notes/fig14/plan.md`.

How it was checked:
- **Equations:** each one was derived again in SymPy 1.14. The scripts sit in the session scratchpad, not in the repository.
  They check substitution into the PDE, Fourier transforms, Gaussian integrals, the four matching equations solved symbolically,
  limits, and the commutators applied to arbitrary functions. BCH (19) was checked with random Hermitian matrices against `scipy.linalg.logm`.
- **Stored numbers:** read from the stored files in `public/data/schrodinger-sphere/2026-11-12/`, with my own reader for the
  `SPHC`/`SPHW` format (header, then a zlib body). That covers 405 sphere cuts, 81 true-3D files and 585 flat-wall files.
- **Solver numbers:** the page's own solver `tools/kaggle/schrodinger-sphere/solver.py` was loaded unchanged and run on this
  workspace's CPU (JAX 0.8 CPU, 64-bit and 32-bit). `pillar.py` and `flat.py` were imported unchanged. The live worker
  `public/scripts/schrodinger-live-worker.js` was run unchanged in Node through `vm`.
- **The page:** served from `public/` and driven in headless Chromium (Playwright, `/usr/bin/google-chrome`, SwiftShader WebGL),
  reading `window.__fig14.ds` and the readout elements. KaTeX rendered with 0 errors, and the equation tags run (1) to (24).
- **Classical ensemble:** my own code, not the author's `classical.py`. It flies 400 000 balls drawn from the packet's
  position and wave-number spreads, with reflection or refraction at the sphere. Results are counted in slabs at the stored end time.

Verdicts are "verified", "wrong, because …" (with the correct result) or "unverifiable, because …". Line numbers are those of the HTML file.

## Summary of errors (details in the rows below)

| # | line | error | correct |
|---|---|---|---|
| E1 | 553 | Default readouts at the last frame are given as 0.239, 0.631, 0.126, 0.0039. | At R = 4 the page plays the true-3D file, which has 32 frames, ends at t = 13.33 after 1333 steps, and reads **0.239, 0.633, 0.123, 0.0048** (measured in Chromium). |
| E2 | 552 | The views paragraph does not say that the R = 4 true-3D files hold 32 frames, one every 0.43 at the default. | The time slider, the Fig. 14b curves and the readouts at R = 4 come from those 32 frames, not from the 48 frames of section 8. |
| E3 | 551 | "the potential (2)" | The potential is equation **(3)**. |
| E4 | 552 | The box is given as "\|y\|, \|z\| < 16". | The drawn points run from −16 to 15.5: **−16 ≤ y, z < 16**. |
| E5 | 552 | "the levels stop at 255" | True for the spun cuts. The R = 4 true-3D files store Re ψ as levels **−127 … 127**, and 72 of the 81 runs clip at ±127. |
| E6 | 552 | "0.9 levels rms and 17 at worst, at the moment of impact" | The worst difference, 16.7, is at t = 6.72 (impact), where the rms is 0.62. The largest rms, 0.89, comes later, at t ≈ 10.6 to 11.0. |
| E7 | 555, 558, 564 | The pillar is described as available on the page and "solved on Kaggle", with its loss "shown as lost". | No pillar data is on the site: `generations.json` has no pillar generation and there is no `pillar/` folder. The Pillar button is **disabled** ("Not stored yet"). |
| E8 | 555 | "flat wall \|x\| < a/2" uses the unit of length *a* as the wall thickness. | The thickness is a slider value from 0.5 to 3 (in units of a), and the page labels it "Wall thickness a 1.0 a". Use d, as in section 4. |
| E9 | 564 | "about 4 % of the probability over a run" | This holds near R = 4 only: E = 2 gives 4.0 %, E = 2.5 gives 3.7 %. E = 4.5, R = 2 loses 0.3 %, and E = 0.5, R = 6 loses 26 % (border included). |
| E10 | 555 | "easier to compute … the reason is the same as for the sphere's rotational symmetry" | The sphere was computed in full 3D. Its symmetry was used only to store and draw the wave. |
| E11 | 533 | "the 405 files take 46.4 MB; the phase picture … stays with the Kaggle notebook" | The 405 cut files now hold both \|ψ\| and arg ψ and take **62.7 MB**. The page uses the phase. |
| E12 | 375 | The border absorbed "0.4 % to 7 %" in the Table 2 runs. | **0.07 % to 6.9 %** (0.0007 for 4.5, 4, 2; 0.0689 for 2.5, 8, 6). |
| E13 | 362 | "The same curves are drawn live in Fig. 14b" | At the default (R = 4), Fig. 14b draws the 32-frame curves of the true-3D run, not these 48-frame curves. |
| E14 | 286 | "the same to the four digits stored" | The file stores σ_y = 3.716324, six decimals. (11) gives 3.716277: they agree to 4.7e-5. |

## Equations

| eq | line | statement | verdict | how |
|---|---|---|---|---|
| (1) | 213 | Born rule and normalisation | verified | This is a definition. (5) integrates to 1 in SymPy. |
| (2) | 216 | time-dependent Schrödinger equation | verified | Units: ħ²/m·∇² and V both carry J; iħ∂t carries J. |
| (3) | 221 | V = V0 inside \|r\| < R | verified | It matches `solver.py`: `np.where(X**2+Y**2+Z**2 < R**2, V0, 0)`. |
| (4) | 223 | dimensionless form | verified | Substituting x = aX, t = (ma²/ħ)T, E = (ħ²/ma²)ε gives i∂Tψ = −½∇²ψ + εψ. |
| (5) | 231 | starting packet | verified | SymPy gives norm 1. It is the same as `solver.py` line `psi = (2*pi*s0**2)**-0.75*exp(...)`. |
| (6) | 257 | ω = k²/2 | verified | SymPy: substituting the plane wave gives ω = k²/2. With units restored, ħω = (ħk)²/2m. |
| (7) | 262 | \|φ(k)\|² = √(2σ0²/π) e^{−2σ0²(k−k0)²} | verified | The SymPy Fourier transform of the 1D packet matches, ratio 1. Its norm is 1. |
| (8) | 264 | σxσk = ½ | verified | SymPy variance of (7): σk = 1/(2σ0). |
| (9) | 267 | ⟨E⟩ = k0²/2 + 3/(8σ0²) | verified | SymPy: ⟨kx²⟩ = k0² + 1/(4σ0²), and the y and z axes add σk² each. |
| (10) | 271 | ψ(x,t) as a Fourier integral | verified | The closed form of (10) satisfies (4): SymPy residual 0. |
| (11) | 280 | σ(t) = σ0√(1+(t/2σ0²)²) | verified | \|ψ\|² equals the spreading Gaussian to 7e-17 at 50 random points. Variance σ0² + t²/4σ0², exact in SymPy. Limits: t → 0 gives σ0; σ0 → ∞ gives a constant width. |
| 3.3 steps | 272–275 | expansion; ∫e^{−αq²+iβq} = √(π/α)e^{−β²/4α}; Re(1/α) = 1/[σ0²(1+τ²)] | verified | SymPy, each step zero residual. |
| (12) | 293 | u″ = −2(E−V)u | verified | Substitute ψ = u e^{−iEt} into (4). |
| (13) | 296 | κ = √(2(V0−E)) | verified | From (12) with E < V0. |
| 4.2 matching | 301–308 | four equations; C, D; the cosh/sinh line; T = 4k²κ²/[4k²κ² + (κ²+k²)² sinh²κd] | verified | SymPy solves the 4×4 system symbolically. C and D match (difference 0). The cosh/sinh rewrite has difference 0. \|t\|² equals the stated T at random points. κ²+k² = 2V0 and 4k²κ² = 16E(V0−E). |
| (14) | 312 | rectangular-barrier T, both branches | verified | (14) follows from the 4.2 result with difference 0. The E > V0 branch follows by κ → ik′, difference 0. The limit E → V0 gives 1/(1+V0d²/2) from both sides. V0 → 0 gives T → 1. It matches `T1D` in the page and a direct 4×4 numerical solve to 1.55e-15. |
| (15) | 327 | f_aimed = 1 − e^{−R²/2σ0²} | verified | SymPy integral. |
| (16) | 329 | θ = π − 2 arcsin(b/R) | verified | Geometry of specular reflection. θ > π/2 if and only if b < R/√2. |
| (17) | 487 | k_max = π/Δx = 6.28 | verified | Δx = 0.5. `np.fft.fftfreq(128, 0.5)` gives n = −64 … 63. |
| (18) | 491 | Strang step | verified | Line by line, it matches `solver.py` `body`: `p = halfV*p; p = ifftn(kin*fftn(p)); p = halfV*p`, then `p*mask`. |
| (19) | 500 | H_eff = H + Δt²/24([V,[V,T]] + 2[T,[V,T]]) | verified | Random 6×6 Hermitian matrices: ‖H_eff − H − corr‖/‖corr‖ = 6.2e-2, 1.5e-2, 3.7e-3, 9.3e-4 for Δt = 0.2 … 0.025, so it falls as Δt². The opposite sign gives 2.0. The bracket is Hermitian. |
| [V,[V,T]] | 502 | equals −\|∇V\|² | verified | SymPy on an arbitrary f(x,y,z) gives residual 0. [T,[V,T]] vanishes for constant V. |
| (20) | 516 | m = sin(πj/2W)^{1/8}, W = 12 | verified | Matches `solver.py` `setup`, with W = max(4, N//10) = 12 = 6 a. Values 0, 0.775, 0.845, …, 0.990, 0.996, 0.999, as stated. |
| (21) | 521 | P_lost = 1 − Σ\|ψ\|²Δx³ | verified | The page computes `lost = 1 − q[1]` from the stored norm. |
| (22) | 557 | ψ = φ(x,y,t) g(z,t) with the two equations | verified | SymPy: substituting into (4) and using both equations leaves residual 0. (5) equals φ(x,y,0)·g(z,0), ratio 1. Units are consistent. This holds because H = H_xy + H_z, not merely because [p̂z, H] = 0, which the text also invokes. |
| g(z,t) | 558 | (2πσ0²)^{-1/4}(1+it/2σ0²)^{-1/2}exp[−z²/(4σ0²(1+it/2σ0²))] | verified | Reading "it/2σ0²" as it/(2σ0²), the SymPy residual of i g_t + g_zz/2 is 0. The norm is 1.000000 at t = 0, 5, 13.16 and 29.61 (numerical quadrature). The written form "it/2σ0²" is ambiguous; it/(2σ0²) is meant. |
| (23) | 560 | ψ = χ(x,t) g(y,t) g(z,t) | verified | SymPy residual 0. `flat.py` stores χ(x)·g(ρ)g(0), which equals χ g(y)g(z) for a Gaussian g. |
| (24) | 562 | T_packet = ∫₀^∞ \|φ(k)\|² T(k²/2) dk | verified | Dimensionless. The weight dropped below k = 0 is ≤ 9.9e-10 (k0 = 1). My scipy `quad` of (24) with (7) and (14) matches the `T_packet` in all 540 finite flat-wall headers to 5.0e-7. |
| CN scheme | 563 | (1 + i/2 ΔtĤ)χ^{n+1} = (1 − i/2 ΔtĤ)χ^n, keeps the norm | verified | Matches `flat.py` (`A = 1 + iHΔt/2`, `B = 1 − iHΔt/2`, `solve_banded`). All 540 finite runs end with norm 1.000000. The stated reason ("each other's complex conjugates") is not sufficient alone. For a real non-symmetric H, A⁻¹Ā is not unitary (‖U†U−1‖ = 8.5 in a test). The norm is kept because Ĥ is Hermitian, here real symmetric, so the factors are Hermitian adjoints that commute. |

## Numbers, sections 1 to 2

| line | number | verdict | how |
|---|---|---|---|
| 165 | 1D wall: 2.5 parts in ten million | verified | (14) with d = 8 gives 2.5008e-7. |
| 165 | end of stored run: 63 % ahead, 24 % behind, 13 % beside | verified | From the stored cut `e4_v5_r2.bin`: 0.630915, 0.239096, 0.126125. The page at the default shows the true-3D file instead: 63.3 %, 23.9 %, 12.3 % (see E1). |
| 168–203 | Figure 1 geometry: 64 a box, 6 a frame, x0 = −14, rings at 0.5/1/1.5/2 σ0, R = 4, 10 a bar | verified | At 340 px / 64 a = 5.3125 px per a: frame 31.9 px, packet at 135.6, rings 8.0/15.9/23.9/31.9, sphere 21.2, bar 53.1 px. All match the SVG. |
| 217 | ħ = 1.0546e-34 J s | verified | CODATA value 1.054571817e-34. |
| 227 | energy unit 7.62 eV | verified | ħ²/(m_e a²), a = 0.1 nm, gives 7.620 eV. |
| 227 | time unit 8.64e-17 s | verified | 8.638e-17 s. |
| 227 | E = 2.5 → 19.0 eV; V0 = 3 → 22.9 eV | verified | 19.05 and 22.86 eV. |
| 227 | 13.16 → 1.14e-15 s | verified | 1.137e-15 s. |
| 237–246 | Table 1: E grid, V0 grid, R grid | verified | Same as `index.json` `Es`, `Vs`, `Rs`. |
| 241 | k0 1 to 3, default 2.236 | verified | √(2E). |
| 242 | λ 6.28 to 2.09, default 2.81 | verified | 2π/k0. |
| 243 | k0σ0 3 to 9, default 6.71 | verified | |
| 244 | k0R 2 to 18, default 8.94 | verified | |
| 245 | R/σ0 0.67 to 2, default 1.33 | verified | |
| 246 | E/V0 0.06 to ∞, default 0.83 | verified | The minimum is 0.5/8 = 0.0625. |
| 249 | 405 combinations | verified | 9 × 9 × 5, and 405 runs in `index.json`. |

## Numbers, section 3

| line | number | verdict | how |
|---|---|---|---|
| 268 | 3/(8σ0²) = 0.042 | verified | 0.041667. |
| 268 | ⟨k²⟩/2 = 2.541667 on the page's grid | verified | FFT of the packet on the 128-point, Δx = 0.5 grid. The packet is separable, so three 1D FFTs were used: 2.541667. |
| 268 | width k0σk = 0.37 | verified | 0.3727. |
| 283 | spreading rate 1/(2σ0) after t ≈ 2σ0² | verified | dσ/dt → 1/(2σ0) from (11). |
| 286 | k0 = 2.236, λ = 2.81, speed 2.236, spreading time 18 | verified | |
| 286 | travel 29.4 a, from −14 to 15.4 | verified | 29.43, end at 15.43. |
| 286 | width 3.716 a by (11) | verified | 3.7163. |
| 286 | stored σ_y = 3.7163 at the end, "the same to the four digits stored" | wrong, because the file stores six decimals (σ_y = 3.716324 in `e4_v0_r2.bin`) | The stored and formula values agree to 4.7e-5 (formula 3.716277). |
| 286 | 45 free runs follow (11) to 9.4e-5 at every frame | verified | 45 runs with V0 = 0; the largest \|σ_y − (11)\| is 9.37e-5. |
| 286 | E = 0.5: t = 29.61, width 5.78 a | verified | Stored: 29.61, σ_y = 5.7752; (11) gives 5.7753. |

## Numbers, section 4

| line | number | verdict | how |
|---|---|---|---|
| 318 | κ = 1, penetration 1 a = two grid points | verified | |
| 318 | sinh 8 = 1490 | verified | 1490.48. |
| 318 | T = 2.50e-7 | verified | 2.5008e-7. |
| 318 | thick-wall 2.22 e^{−16} = 2.50e-7 | verified | 16·2.5·0.5/9 = 2.222. |
| 318 | largest (14) with E < V0 on the page grid: 1.34e-3 at E = 0.5, V0 = 1, R = 2 | verified | Search over the 9×9×5 grid gives 1.3410e-3 at (0.5, 1, 2). |
| 318 | E = 4.5, V0 = 4, R = 2: k′ = 1, k′d = 4, sin²4 = 0.573, T = 0.495 | verified | T = 0.4955. |

## Numbers, section 5

| line | number | verdict | how |
|---|---|---|---|
| 328 | f_aimed(R = 4) = 0.589; four in ten miss | verified | 0.5889. |
| 330 | backward fraction 0.359 | verified | 1 − e^{−16/36} = 0.3588. |
| 331 | 400 000 balls; spreads σ0 and 1/(2σ0) are the packet's own | verified | The Wigner function of (5) is that product Gaussian. |
| 364 | Fig. 2 four acts: inside up to 0.76 at t = 6.16 | verified | Stored cut: 0.7597 at 6.16. |
| 364 | behind lowest 0.18 at t = 7.0 | verified | 0.1800 at 7.00. |
| 364 | behind rises again to 0.24 | verified | 0.2391 at the end. |
| 364 | ahead overtakes behind at 7.84 | verified | First frame with ahead > behind is t = 7.84 (0.2018 > 0.1896). |
| 364 | settles at 0.63; inside 0.126 at the end | verified | 0.6309; 0.1261. |
| 352–355 | Figure 2 polylines | verified | All four curves, 48 points each, agree with x = 64 + 634 t/13.16 and y = 278 − 242 P to 0.05 px. |
| 362 | "The same curves are drawn live in Fig. 14b" | wrong, because at the default (R = 4) the page plays the true-3D file `wave3d/e4_v5_r2.bin` | That file has 32 frames, 0.43 apart, ending at 13.33 with ahead 0.633. Its curves are close to these but not the same. |
| 368 | Table 2, 2.5/3/4: classical 0.312 / 0.577, quantum 0.239 / 0.631, T 2.5e-7 | verified | My ensemble (seeds 0 to 5) gives 0.3125 / 0.5771; stored 0.239 / 0.631; (14) gives 2.50e-7. |
| 369 | 2.5/8/4: 0.316 / 0.577, 0.277 / 0.597, 3e-23 | verified | Ensemble 0.317 / 0.576. The 0.0015 difference is within sampling and model detail. Stored 0.277 / 0.597. (14) gives 3.09e-23. |
| 370 | 2.5/8/2: 0.093 / 0.886, 0.084 / 0.897, 1e-11 | verified | Ensemble 0.092 / 0.887; stored 0.084 / 0.897; 1.03e-11. |
| 371 | 2.5/8/6: 0.570 / 0.253, 0.458 / 0.256, 9e-35 | verified | Ensemble 0.571 / 0.253; stored 0.458 / 0.256; 9.26e-35. |
| 372 | 4.5/4/2: 0.075 / 0.899, 0.049 / 0.930, 0.495 | verified | Ensemble 0.075 / 0.900; stored 0.049 / 0.930; 0.4955. |
| 375 | border absorbed "0.4 % to 7 %" in these runs | wrong, because the stored losses are 0.39 %, 0.70 %, 0.13 %, 6.89 % and 0.07 % | The range is **0.07 % to 6.9 %**. |
| 376 | wave sends 0.07 less back, 0.05 more ahead | verified | 0.312 − 0.239 = 0.073; 0.631 − 0.577 = 0.054. |
| 376 | λ/(2R) = 0.35 rad ≈ 20° | verified | 0.351 rad = 20.1°. |
| 398 | Figure 3 dotted slab curve | verified | The 321 points match (14) with d = 8 to within 1.8 px. The largest gaps sit on the steep flanks of the resonances, where the coordinates are rounded to 0.1 px. |
| 399–458 | Figure 3 quantum points (R = 2, 4, 6) | verified | They equal stored `ahead` to within 1.9e-4. |
| 399–458 | Figure 3 classical points | verified | They match my ensemble to ±0.002 at all 27 points. Examples: R = 4 gives 0.999, 0.996, 0.939, 0.806, 0.668, 0.577, 0.575, 0.575, 0.575 against 0.999, 0.996, 0.940, 0.807, 0.668, 0.578, 0.577, 0.576, 0.577 read from the SVG. |
| 470 | behind 0.239 at V0 = 3, 0.277 at V0 = 8 | verified | Stored. |
| 470 | 1/κ = 1 a at V0 = 3, 0.30 a at V0 = 8 | verified | 1.000 and 0.302. |
| 470 | 11 % above V0; 0.113 from the non-central χ² | verified | `scipy.stats.ncx2.sf(216, 3, 180)` = 0.1133. |
| 473 | at most 1.3e-3 | verified | 1.34e-3, as above. |
| 477 | 58.9 %, 35.9 % | verified | |
| 477 | classical 31.2 / 57.7 / 11.1 % | verified | Ensemble 31.25 / 57.71 / 11.04 % (mean of five seeds). |
| 477 | quantum 23.9 / 63.1 / 12.6 / 0.4 % | verified | Stored cut. |
| 477 | slab 0.000 025 % | verified | 2.5e-7. |

## Numbers, section 6

| line | number | verdict | how |
|---|---|---|---|
| 483 | the page computes nothing; frames from `solver.py` | verified | True for stored runs. Outside the stored grid the page runs the live worker (section 8.1). |
| 485 | L = 64, N = 128, 2 097 152 points, Δx = 0.5, x from −32 to 31.5 | verified | `setup(128, 64.0)`. |
| 485 | k_n = 2πn/L, n = −64 … 63 | verified | `fftfreq`. |
| 488 | e^{−8} = 3e-4 | verified | 3.35e-4. Note that this is for \|φ\|², the weights of (7). |
| 488 | k0 + 4σk = 3.67 at E = 4.5, 58 % of k_max, 4.2 points per wavelength | verified | 3.667; 0.584; 4.19. |
| 492 | Δt = 0.01; about 1300 steps by default | verified | `index.json` dt = 0.01; the default run has 1316 steps. |
| 492 | quoted loop body | verified | Identical to `solver.py`, followed by `p * mask`. |
| 497 | 64-bit: norm change 3.6e-13 in 1500 steps, border off | verified | `solver.py` CPU, complex128, E = 2, V0 = 3, R = 4, no mask, 1500 steps: +3.69e-13. That is rounding-level. The note does not name the run. |
| 497 | 32-bit: −3.3e-4 in 1500 steps, ≈ 2e-7 per step | verified | complex64, same run: −3.332e-4, which is 2.2e-7 per step. |
| 497 | T4 runs lose ≈ 4.6e-7 per step before the border | verified | Stored default: 1 − norm = 1.53e-4 at frame 12 (336 steps), or 4.55e-7 per step. |
| 503 | order test diffs 1.21e-3, 2.99e-4, 7.45e-5, 1.86e-5 | verified | 64-bit, border off, E = 2, V0 = 3, R = 4, t = 7.28, Δt = 0.04 … 0.0025: 1.2106e-3, 2.9896e-4, 7.4520e-5, 1.8616e-5. |
| 503 | ratios 4.0 | verified | 4.05, 4.01, 4.01. |
| 503 | error at Δt = 0.01 ≈ 4/3 × 7.45e-5 = 1.0e-4 | verified | 9.93e-5. |
| 503 | behind changes by 6e-6 when Δt is halved | verified | 6.0e-6 between Δt = 0.01 and 0.005 at t = 7.28. |
| 507 | 0.197 rad, 0.067 rad, 0.08 rad | verified | 0.197, 0.0672, 0.080. |
| 509 | ahead 0.62780 on Kaggle | verified | Stored `e3_v5_r2.bin` end: 0.62780. |
| 509 | 0.62802 CPU 32-bit | verified | My run of `solver.run`, complex64: 0.628017. |
| 509 | 0.62821 64-bit | verified | complex128: 0.628214. |
| 509 | 256³: 0.62483 ahead, 0.24923 behind; 128³: 0.62802, 0.24887 | verified | `solver.run` on `setup(256, 64.0)`, 32-bit, CPU here: ahead 0.624829, behind 0.249231. On 128³: 0.628017, 0.248865. |
| 509 | grid effect 3e-3 | verified | 0.628017 − 0.624829 = 3.19e-3. |
| 509 | "computed here in 5 minutes" | unverifiable, because timing depends on the machine | It took 6.6 min here. |
| 509 | the default recomputed matches the stored curves to 3.4e-4 at every frame | verified | complex64 rerun of E = 2.5, V0 = 3, R = 4: the largest difference over 48 frames in norm, behind and ahead is 3.33e-4. |

## Numbers, section 7

| line | number | verdict | how |
|---|---|---|---|
| 515 | W = 12 points = 6 a | verified | `solver.py`. |
| 517 | mask values 0, 0.775, 0.845, … 0.990, 0.996, 0.999 | verified | Computed from (20). |
| 518 | border on, Δt 0.01 → 0.005: lost +8e-4, behind −5e-4 by t = 14.57 | verified | 64-bit runs to t = 14.57: lost +8.2e-4, behind −5.1e-4. |
| 522 | default P_lost 1.5e-4 after 336 steps | verified | Stored frame 12: 1.53e-4. |
| 522 | 64-bit loses 3.5e-6 in 300 steps | verified | complex128 with the mask, 300 steps: 3.49e-6. |
| 522 | default P_lost at the end 0.0039 | verified | 0.003864 in the stored cut. The page at the default shows 0.0048 from the true-3D file (E1). |
| 522 | E = 2: stored 0.0047, 64-bit 0.0040, about 85 % real | verified | Stored 0.0047; my 64-bit run 0.00399; 0.0040/0.0047 = 0.85. |
| 523 | over 405 runs, end P_lost from 7e-4 to 0.123 | verified | 7.19e-4 (E = 4, V0 = 1.5, R = 3) to 0.1226. |
| 523 | largest at E = 0.5, V0 = 8, R = 6, t = 29.61 | verified | |
| 523 | frames 0 to 12 within 5.2e-4 of 1 | verified | Largest \|1 − norm\| is 5.17e-4. |
| 526 | Example 7.1 summary | verified | It restates the rows above. |

## Numbers, section 8

| line | number | verdict | how |
|---|---|---|---|
| 532 | 1000 to 3000 steps | verified | 987 to 2961. |
| 532 | T4: 1.61 ms per step, 2.6 ms with the measurements | unverifiable, because no T4 GPU is available here | |
| 532 | 0.77 ns per point | verified | 1.61e-3/128³ = 0.768 ns. |
| 532 | 880.8 s on two cards, 2.3 s to 6.9 s per run | verified | `index.json`: `sweep_s` 880.8, `gpus` 2, walls 2.31 to 6.90. |
| 533 | n_target = round(30/(k0Δt)), s = ⌊n/47⌋ | verified | Same as `solver.py`: `steps = int(round(travel/k0/dt)); per = steps//(nframes-1)`. |
| 533 | default 1342, s = 28, 1316 steps, t = 13.16, every 0.28 | verified for the stored cut | The page at R = 4 plays the 32-frame true-3D file instead: 1342//31 = 43, so 1333 steps, t = 13.33, every 0.43. |
| 533 | stored per frame: norm, behind, ahead, σ_y | verified | `measure` in `solver.py`. |
| 533 | \|ψ\| in z = 0 at 128×128 points, 0 to 255 | verified | Arg ψ is stored too. |
| 533 | 405 files take 46.4 MB; the phase stays with the notebook | wrong, because the cut files now hold both levels (\|ψ\| then arg ψ, read by `load()` as `c.A` and `c.P`) | The 405 files take **62.7 MB**. The true-3D files add 101.0 MB and the flat-wall files 51.9 MB. |
| 533 | SHA-256 checked | verified | In Chromium, `sha_ok` = true for the default true-3D file and the flat-wall file. |
| 535 | extra stops: E to 6, V0 to 12, R 1 to 8 | verified | `EXTRA` in the page. The sphere's V0 control also offers −4, −2, −1 and "hard", which section 8.1 does not mention. |
| 535 | 64³, L = 64π/(k0 + 0.67) when k0 + 0.67 > π, i.e. E > 3.05 | verified | Worker line `L = 64·min(1, π/(√(2E)+0.67))`; the threshold is E = 3.054. |
| 535 | Δt ≈ 0.04, a whole number of steps per frame | verified | Worker `per = round(frameDt/dt0)`. |
| 539 | 2.5/3/4: 0.272/0.239, 0.622/0.631, 0.035 | verified | Worker in Node, unchanged. |
| 540 | 2/3/4: 0.269/0.249, 0.628/0.628, 0.023 | verified | Same method. |
| 541 | 0.5/8/6: 0.403/0.388, 0.271/0.272, 0.076 | verified | Same method. |
| 542 | 4.5/4/2: 0.068/0.049, 0.891/0.930, 0.039 | verified | Same method. |
| 545 | 11.6 s to 35.6 s per run | verified, machine-dependent | 13.5 s to 35.0 s here. |
| 546 | up to 0.03 more behind; up to 0.08 at some frame | verified | 0.033; 0.076. |

## Section 09: the screen (lines 551 to 553)

| line | statement or number | verdict | how |
|---|---|---|---|
| 551 | L̂x commutes with Ĥ; (5) has L̂xψ = 0; ψ = ψ(x, ρ, t) | verified | Both (5) and V depend on y² + z² only. |
| 551 | "the potential (2)" | wrong, because (2) is the Schrödinger equation | The potential is **(3)**. |
| 551 | stored plane z = 0, half y = ρ ≥ 0, 128 × 64 points, 0.5 a | verified | `to_site_axisym.py` keeps rows 64 to 127. Headers: `nx` 128, `nr` 64, `step` 0.5. |
| 551 | q = round(255\|ψ\|/\|ψ\|_peak), with the peak of the first frame | verified | `solver.py`: `amp0 = sl.max()` at frame 0, in the plane z = 0. |
| 551 | p, 256 steps from −π to π | verified | Encode `round((φ+π)/2π·255) % 256`; decode `p/255·2π − π`. Not stated: p = 0 and Re ψ is taken as 0 where q < 3 (`reAt`). |
| 551 | box 48 a × 32 a, Re ψ = (q/255)cos(phase), x at the stored point, ρ linear between two stored values | verified | `field3d`. In Chromium at R = 3, 4400 sampled voxels equal this formula from the stored levels to 3e-8. |
| 552 | four views under *View* | verified | Chips: Sheets, Surface, Cutaway, Fog. |
| 552 | Sheets: Re ψ = ±c, wine crests and slate troughs, c = 0.3 × largest \|Re ψ\| in the box at that moment | verified | `ISO = 0.3`; `iso/remax` = 0.300 in Chromium, and `remax` equals max \|F\|. Colours are `WINE`/`SLATE` in `wave3d-view.js`. |
| 552 | wine sheets one wavelength 2π/k0 apart | verified | Holds for the incoming packet, where Re ψ ∝ cos(k0x − ωt). It is only approximate where the reflected wave overlaps. |
| 552 | marching cubes: cubes of 8 points straddling c, triangles placed by linear interpolation along the edges | verified | `marching()` uses `edgeTable`/`triTable` and `t = (level − val[a])/(val[b] − val[a])`. |
| 552 | Cutaway: same with a quarter removed | verified | Two clipping planes with `clipIntersection` remove y > 0, z > 0. |
| 552 | Surface: plane z = 0 lifted by Re ψ | verified | `plane0` takes index 32, which is z = 0. Height is (Re ψ / max\|Re ψ\|) × 6 a. |
| 552 | Fog: opacity grows with (Re ψ)² along the line of sight | verified | `volume-view.js`: a = 1 − exp(−κ (Re ψ)² Δs), and troughs at 0.35 of that. |
| 552 | all four views on the same box, −24 ≤ x < 24 and \|y\|, \|z\| < 16, 0.5 a apart | wrong, because the drawn points are y, z = −16 + 0.5 j for j = 0 … 63 (`Y3 = −16`) | The box is **−16 ≤ y, z < 16**. Fog draws the same field rounded to 8-bit levels (`fogVolume`), not the identical floats. |
| 552 | R = 4: Kaggle stored Re ψ on every point of that box from the full 3D run | verified | The `wave3d/` generation has 81 runs, all at R = 4, on 96 × 64 × 64 points, x from −24, y and z from −16. Chromium confirms that the default draws it (source line "true 3D data", `entry().wave` true). |
| 552 | (omission) the R = 4 true-3D files hold 32 frames, not 48 | wrong, because the paragraph says nothing about it, and so line 553 and section 8 do not describe what the page plays at R = 4 | Headers: `n` 32, `steps` 1333, frame interval 0.43 by default. The time slider maximum is 31 in Chromium. |
| 552 | other radii: the spun half-plane | verified | Also used at R = 4 while the true-3D file loads (`entry()`), and for the flat wall. |
| 552 | symmetry: run E = 2, V0 = 1.5, R = 4; rms 0.9 levels of 127, worst 17, "at the moment of impact" | wrong in part, because the two figures belong to different times | From `wave3d/e3_v3_r2.bin`, every voxel off the plane with ρ ≤ 15.5 against the plane z = 0 interpolated at its ρ: the worst is 16.7 at t = 6.72 (impact), where the rms is 0.62. The largest rms, 0.89, is at t ≈ 10.6 to 11.0. |
| 552 | "the levels stop at 255 … crests are clipped" | wrong for the true-3D files, because at R = 4 the stored Re ψ levels run from −127 to 127 of the first frame's peak \|ψ\| | Clipping at ±127 happens after frame 0 in 72 of the 81 true-3D runs (30 658 voxels). At frame 14 of the default the largest \|Re ψ\| drawn is exactly 1 = 127/127. For the spun cuts, 255 is right. |
| 552 | stored frame at or before the playback time, never blended | verified | `frameOf` = ⌊tPhys/frameDt⌋. The cross-fade happens only on a change of run, source or shape (`snapshot`). |
| 552 | readouts and Fig. 14b from Kaggle's whole ψ | verified | `readouts()` and `drawPlot()` read the stored `curves`. |
| 553 | Fig. 14b colours and dashes | verified | `drawPlot`: `#1c1518` solid, `#b07a6a` [4,3], `#7a1f2b` solid, `#8b8079` [2,3]. |
| 553 | defaults, last frame: 0.239, 0.631, 0.126, 0.0039 | wrong, because at R = 4 the page plays `wave3d/e4_v5_r2.bin`, 32 frames | Measured in headless Chromium, the readouts are **0.239, 0.633, 0.123, 0.0048**, with caption "t = 13.33 · frame 32 of 32" and source "1333 steps". The quoted values are those of the 48-frame cut. |
| 553 | guide: (14) with d = 2R and an E < V0 warning | verified | `T1D(E, V0, 2R)`; the readout says "E < V₀, forbidden classically · T = 0.000". |
| 553 | the panel checks inside, lost, σ_free (11), T1D (14) | verified | `Sim.data.check` has k0, inside, lost, sigma_free, T1D and t. |

## Section 9.1: other barriers (lines 554 to 564)

| line | statement or number | verdict | how |
|---|---|---|---|
| 555 | sphere can be replaced by a pillar | wrong, because the Pillar button is disabled with the title "Not stored yet" (Chromium) | `generations.json` lists sphere, wave3d and flat (slab) only. There is no `pillar/` folder and no `gz.bin`. Only Sphere and Flat wall work. |
| 555 | flat wall "\|x\| < a/2" | wrong, because *a* is already the unit of length (section 2.2) | The thickness is a parameter from 0.5 to 3 (in units of a; `index.json` `As`), and the page reads "Wall thickness a 1.0 a". Write \|x\| < d/2, with d as in section 4. |
| 555 | soft, hard (V0 → ∞), well (V0 < 0) for each shape | verified for the flat wall | Flat V0 values: −4, −2, −1, 0 … 8 and 1e6 (hard). For the pillar there is no data. |
| 555 | "easier to compute … the reason is the same as for the sphere's rotational symmetry" | wrong, because the sphere was computed in full 3D on 128³ points | Its symmetry was used only to store and draw. For the pillar and the wall, the translation symmetry lowers the dimension of the computation itself. |
| 556 | p̂z commutes with Ĥ; Ĥ splits | verified | This is the additive split that (22) needs. |
| 557 | (22) | verified | See the equations table. |
| 558 | g(z,t) solves its equation and has norm 1 (SymPy) | verified | See the equations table. |
| 558 | Kaggle solved φ on 128² points with the method of section 6; the page draws φ at every z weighted by g(z) | unverifiable, because no pillar run is stored or served | The code path (`field3d`, pillar branch: Re(φ·g(z)/g(0,0)), nearest z sample of `gz.bin`) never runs. Also, `pillar.py` differs from section 6/7: Δt = 0.0025 (hard 0.0005, not 0.01). Its border is a finite absorber, m^{Δt/0.01}, never 0, applied as two half-steps. |
| 560 | (23) | verified | See the equations table. |
| 561 | the flat wall is the 1D problem of section 4 | verified | `flat.py` uses V(x) only. |
| 562 | (24) | verified | See the equations table. |
| 563 | Δx = 0.05 a, Crank–Nicolson | verified | `flat.py` `dx = 0.05`, `solve_banded` with A = 1 + iHΔt/2 and B = 1 − iHΔt/2. A fourth-order Laplacian is used; the note does not say so. |
| 563 | stored on the same half-plane as the sphere | verified | Flat headers: `nx` 128, `nr` 64, `x0` −32, `step` 0.5. Chromium source line: "stored: the cut through the axis". |
| 563 | 510 stored runs end with inside < 0.002 | verified | Of the 540 finite runs, 510 end with norm − behind − ahead < 0.002. |
| 563 | there, ahead equals (24) to 0.0045 | verified | 0.00450. The worst case is E = 0.5, V0 = 0, a = 1 (ahead 0.9955, T = 1): the slow packet's tail is still behind the wall, so no wall physics is involved. |
| 563 | (14) agrees with the matching equations to 1.6e-15 | verified | My 4×4 solve over E = 0.05 … 6 (120 values) × 11 heights × 5 thicknesses gives 1.55e-15. Over the stored grid it is 8.9e-16. |
| 563 | hard wall lets through at most 1e-6 | verified | The largest stored `ahead` over the 45 hard runs is 1e-6, which is the curve's rounding unit. |
| 564 | hard wall: points inside removed, ψ = 0 at the face built into the second derivative | verified | `flat.py`: wall = inside ∪ face; odd ghost `H[2, L0−1] += 0.5 c[4]` and `H[2, R0+1] += 0.5 c[0]`. |
| 564 | pillar: ψ set to 0 inside after every step | verified, code only | `pillar.py`: `phi = half*phi*keep`. |
| 564 | about 4 % lost over a run | wrong as a general statement, because the loss depends strongly on the run | `pillar.py` run here, hard column. E = 2, R = 4: 4.0 % (border alone 0.1 %). E = 2.5, R = 4: 3.7 %. E = 4.5, R = 2: 0.3 %. E = 0.5, R = 6: 26 % including the border. "About 4 % for R = 4" is right. |
| 564 | "which the page shows as lost" | unverifiable, because the page cannot show the pillar (see line 555) | |
| 564 | halving Δt changes ahead of the pillar by < 1e-3 | verified | `pillar.py`, E = 2, R = 4. Finite (V0 = 3), Δt 0.0025 → 0.00125: 2.8e-7. Hard, 0.0005 → 0.00025: 9.1e-5. |
| 564 | coin and tube buttons shown but not active | verified | Disabled in Chromium. The Pillar button is disabled too, which the note does not say. |

## Section 10

| line | number | verdict | how |
|---|---|---|---|
| 570 | 12.6 % still beside the sphere | verified | Stored cut 0.1261. The page at the default shows 12.3 % (E1). |
| 571 | k0R = 8.94, about nine partial waves | verified | |
| 575 | P10.2: √2 at t = 2σ0² | verified | From (11). |
| 577 | P10.4: 0.084, 0.277, 0.458 | verified | Stored, for E = 2.5, V0 = 8. |
| 579 | P10.6: E > 3.05 | verified | 3.054. The box for E = 6 is 48.6 a. |
