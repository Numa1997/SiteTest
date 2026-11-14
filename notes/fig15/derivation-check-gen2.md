# Fig. 15, generation-2 note: independent check

Checked: `public/scripts/resonant-note.js` as committed at `692e546` (branch `claude/fig15-gen2-note`), 27 numbered equations.

How it was checked:
- Every equation was re-derived in SymPy 1.14, or checked numerically against `tm.py` / `iv.py` where a closed form needs numbers. Scripts are in the session scratchpad: `check_eqs.py`, `check_iv.py`, `check_iv2.py`.
- The page ran in headless Chrome (Playwright, served from `public/`). It printed no errors and set equation tags (1)–(27). The note's text was read back from the page with the TeX source of each formula.
- `notes/fig15/gen2_numbers.py` was re-run. All 235 NUM values match what it computes now.
- The method description was compared line by line with `rt3d2.py`, `rt3d2_run.py`, `file_rt3d2.py`, `iv.py`, `exact1d.py` and the page script (interpolation and drawing).
- I did not read `plan.md`.

Verdicts are "verified", "wrong, because …" or "unverifiable, because …".

## Errors, ranked by severity

1. **§13, the current from the runs (`iv_walls_Vp/Vv/pvr` = 0.5 / 1.375 / 5.0; `iv_disc6_*` = 0.875 / 1.875 / 1.8).** These numbers come from how the energies were sampled, not from the physics.
   - Each voltage has only 8–9 of its 25 energies filed. The filed energies come in pairs about 0.25 apart.
   - The integration window also changes with voltage. At V = 0.625 and 1.375 it starts at E = 0.30, so it leaves out E = 0.10–0.25, where the sunken level now sits.
   - The index's own check shows this. The exact single-energy T integrated on the same sparse points (`J_exact_single_energy_same_points`) peaks at V = 0.25. The dense exact curve peaks at 0.875.
   - The packet-averaged exact current on the full 25-energy grid is what the runs curve should converge to. It peaks at V = 0.875, has its valley at 1.75 and a ratio of 3.8.
   - Correct form: do not quote a peak, valley or ratio for the runs curve until every voltage has all 25 energies. Until then, say that each voltage has 8–9 of 25 energies, so the shape is not yet meaningful.
   - Eq. (27)'s sentence "runs at the 25 energies … give T̄_i" should say "the energies filed so far".
2. **§12, "the runs at E = 0.65, the stored energy nearest the resonance".** Wrong.
   - The planned grid holds 0.70 and 0.75. 0.75 is the nearest, 0.015 from E_r = 0.735, and `gen2_numbers.py` itself aims for 0.75.
   - 0.65 is only the nearest energy *filed so far*. It is 0.085 below E_r, more than Γ = 0.070.
   - Correct form: "the filed energy nearest the resonance (0.70 and 0.75 are still to come)".
3. **§6, long packet "on a box four times longer along the flight".** Wrong.
   - Long packets use Nx = 512 against 192 (`rt3d2_run.py`, group G). That is 256 a against 96 a, 2.67 times longer.
   - Correct form: "a box 256 a long instead of 96 a".
4. **§6, "σ_E = 0.051, now narrower than the peak".** This compares a standard deviation with a full width.
   - The packet's energy FWHM is 2.355 × 0.051 = 0.119. That is still wider than Γ = 0.070, which is why T̄ is only 0.54 and not near 1.
   - Correct form: "its spread σ_E = 0.051 is now smaller than Γ, though its full width (0.12) is not".
5. **§12, shell lifetimes (66.9, 110, 63.2, 104).** These are quoted without the caveat §8 gives for d = 2.
   - The shell runs have a fixed τ estimate of 30. Each run is the flight time plus 90.
   - For R = 3, s = 3.5 the fit window is 73–147, and it ends at the end of the run. P_in has fallen only to 30 % of its peak, so τ = 110 comes from less than one lifetime. The same holds for R = 5 at both gaps: their windows also end at the end of the run.
   - The R = 3, s = 2.5 maximum sits at E = 0.30, the bottom edge of the grid.
   - Correct form: add that the s = 3.5 lifetimes, and both R = 5 ones, are fitted over windows cut short by the end of the run, as in §8.
6. **§6, long-packet result 0.51 (`V2D1_long_T`).** All five long-packet runs of the running example (E 0.583 … 0.843) are in `FIX1` in `rt3d2_run.py`. That is the project's own list of runs that ran more than 15 % too short (101.5 against 122.1 for E = 0.713). They are filed and not yet replaced (`replaced: []`).
   - The value is close to the exact packet average at that energy (0.4997), so the claim stands.
   - Correct form: the note should say these runs are due to be rerun.
7. **§7, "the finite well matches the resonances to a few thousandths".** This holds for the first level only.
   - Second level at s = 3.5: 1.486 against 1.445 (0.041).
   - Third level at s = 5.5: 1.397 against 1.377. The resonance 1.397 is missing from the table, although the finite-well column lists 1.377.
   - Correct form: "the lowest level to a few thousandths, the levels near the barrier top to a few hundredths". Also list 1.397 for s = 5.5.
8. **§13, "the electron meets the first barrier with less energy below its top than the second, so the first is more opaque".** The wording is backwards.
   - The ramp lowers the second barrier, so E lies *further* below the first barrier's top.
   - Correct form: "the electron's energy lies further below the first barrier's top than below the second's, so the first is more opaque".
9. **§4 after (10), "the wave piles up behind the more opaque barrier and leaks back out through the other".** This fits only the case where the far barrier is the opaque one.
   - In the diode the entrance barrier is the opaque one. There the loss comes from the trapped wave being too weak to cancel the prompt reflection.
   - Correct form: "the leaks no longer balance, and the reflected waves no longer cancel".
10. **§8, "(13) … with the single-barrier transmission T of (8)".** The table's Γ from (13) uses the exact T of (7), for example 0.144 and not 0.154.
    - Correct form: "T of (7)". If (8) is used, Γ ≈ 0.0679 for the running example.
11. **§5, "The electron bounces about three times before it gets out".** It makes about three *round trips* in τ (14.2 / 4.55 = 3.1). That is about six hits on a barrier (vτ/L_eff = 6.2).
    - Correct form: "makes about three round trips".
12. **Minor.**
    - §9: "0.735 is its middle". The band's middle in energy is 0.773. 0.735 is where ξ = 0. Say "the middle of the band in ξ".
    - §9: "peaks 0.02 to 0.1 apart". N = 3 peaks are 0.173 apart. Say "0.02 to 0.17".
    - §10: "barrier faces lie exactly halfway between grid points". True for walls and discs, not for spherical shells.
    - Ex. 3.1: "twenty times smaller". The ratio is 22.5.

## One row per equation

| Eq. | Content | Verdict |
|---|---|---|
| (1) | TDSE; natural units ħ = m = 1 | verified (units: E in ħ²/ma², t in ma²/ħ) |
| (2) | separation for V = V(x) | verified (SymPy: residual of (1) for χ g g equals the sum of the residuals of (2); this is sufficient) |
| (3) | k = √(2E), κ = √(2(V0−E)) | verified (SymPy) |
| (4) | edge matrix | verified (SymPy solve of the matching conditions) |
| (5) | M = [[w, z],[z*, w*]], \|w\|² − \|z\|² = 1 | verified (symbolic square barrier with centre reference: rows paired, det M = 1) |
| (6) | \|w\|² = 1 + V0² sinh²(κd)/(4E(V0−E)) | verified (SymPy, exact identity) |
| (7) | T = 1/\|w\|², R = 1 − T | verified (T matches tm.py to 1e-16) |
| (8) | thick-barrier limit 16E(V0−E)/V0² e^{−2κd} | verified (SymPy limit; 0.1545 → 0.154) |
| (9) | t₂ = t² e^{iks}/(1 − r² e^{2iks}) | verified. It needs z purely imaginary for a centred symmetric barrier (SymPy: Re z = 0). It agrees with tm.py to 7.7e-15, so "one part in 10⁹" is a safe bound. |
| (10) | peak value of an unequal pair, T_aT_b/(1−√(R_aR_b))², approx 4T_aT_b/(T_a+T_b)² | verified (numerical unequal pair, d = 1 and 1.3: exact peak 0.81467, Fabry–Pérot 0.81467, (10) 0.833). The physical explanation that follows is wrong: item 9. |
| (11) | Breit–Wigner | verified as an approximation. The exact curve is lopsided: at E_r ∓ Γ/2 it is 0.459 and 0.533. |
| (12) | τ = ħ/Γ | verified (standard; units) |
| (13) | 1/τ ≈ vT/L_eff | verified dimensionally and against the table (within 20 %). The source of T is mislabelled in §8 (item 10); the "three bounces" wording is item 11. |
| (14) | T̄ = ∫\|φ\|² T dk, σ_k = 1/(2σ_x), σ_E ≈ k0σ_k | verified (SymPy Fourier transform of the Gaussian; T̄ = 0.1959 recomputed) |
| (15) | T̄ ≈ √(π/8) Γ/σ_E | verified (SymPy: Lorentzian area πΓ/2 times 1/(√(2π)σ_E)) |
| (16) | finite well, even and odd | verified (SymPy log-derivatives; levels recomputed) |
| (17) | E_n ≈ n²π²ħ²/(2mL_eff²) | verified (dimension; hard-wall form) |
| (18) | ξ = ½ tr P = Re(w e^{−iks}) = cos(ks+φ)/√T | verified (SymPy trace; numeric: cos(ks+φ) correct, cos(ks−φ) wrong) |
| (19) | T_N = [1 + (R/T) U_{N−1}²]^{−1} | verified (Cayley–Hamilton identity to 1e-14; U_4(cos θ) = sin 5θ/sin θ in SymPy; agrees with tm.py to 2.3e-12 for N = 2, 3, 4, 5, 10) |
| (20) | cos qs = ξ | verified (eigenvalues λ + 1/λ = 2ξ; band edges recomputed 0.5898, 0.9552, 2.0816) |
| (21) | Strang split, local error O(Δt³) | verified (random Hermitian test: the error falls 7.9× and 8.0× per halving of Δt). It matches `rt3d2.py` (halfV, e^{−iK²Δt/2}, halfV; Δt = 0.01). |
| (22) | interpolation in the turning frame | verified (exact for e^{−iEt}). It matches the page's `interp()` line by line: f+1 frame times e^{+iEΔt_f}, then e^{−iEτ}. |
| (23) | rates add | verified (independent decay channels) |
| (24) | τ_side ~ mR²/ħ | verified (units are time; it is an order of magnitude, as the note says) |
| (25) | linear ramp between the outer faces | verified (`iv.py` Uramp and `rt3d2.vbias` are identical) |
| (26) | Tsu–Esaki formula and supply function | verified (SymPy: transverse density m*/πħ² per area; ∫dE⊥ f = kT ln(1+e^{(E_F−E)/kT}); prefactor e m* kT/(2π²ħ³)) |
| (27) | trapezoid J_runs | verified as a formula: it reproduces the stored `J_runs` to 4e-16. The numbers drawn from it are wrong: item 1. |
| unnumbered | ∫ over E⊥ in §13 | verified (SymPy) |

## One row per number

| Where | Number | Verdict |
|---|---|---|
| abstract / §3 | 14 in a hundred, 14.4 % | verified (0.14395) |
| §2 box | k = 1.212, 2π/k = 5.18, κ = 1.591, e^{−κd} = 0.204 | verified |
| §3 | κd = 1.591, sinh = 2.351, \|w\|² = 6.947, T = 0.144, \|r\| = 0.925 | verified. With the rounded inputs the displayed expression gives 6.945; 6.947 is the unrounded value. |
| Ex. 3.1 | sinh(3.18) = 12.0, T = 6.4e-3, "twenty times" | verified (6.40e-3). The ratio is 22.5: item 12. |
| §3 | (8) gives 0.154 | verified |
| §4 | \|t₂\|² = 1.000 at 0.735 | verified |
| Ex. 4.1 | 2.1, 7.1, 13.9, 36.8, 67.1, 92.5, 99.9 % | verified (2.07, 7.14, 13.89, 36.78, 67.09, 92.50, 99.93) |
| §4 | 0.144² = 2.1 % | verified |
| §5 | E_r = 0.735, Γ = 0.0704, τ = 14.2 | verified (0.73493, 0.070405, 14.204) |
| §5 | v = 1.21, L_eff = 2.76, Γ ≈ 0.0633 | verified |
| §5 | "bounces about three times" | wrong: item 11 |
| §6 | σ_E = 0.202 (short), 0.051 (long), "about three times Γ" | verified (0.2021, 0.0505; ratio 2.87) |
| §6 | (15) 0.218; exact 0.196; one barrier 0.149 | verified (0.2183, 0.1959, 0.1494) |
| §6 | 0.196 → 0.538 | verified (index interpolation 0.538; a finer integral gives 0.540) |
| §6 | 5 long runs, best 0.51 | verified (twin 0.5098, file …E0.713). The run is on the too-short list: item 6. |
| §6 | d = 2 long packet 0.0225 | verified (twin 0.02247, …E0.722) |
| §6 | (15) for d = 2: 0.0359; exact 0.035 | verified (0.0359, 0.0351) |
| §6 | "box four times longer" | wrong: item 3 |
| §6 | "σ_E … narrower than the peak" | wrong: item 4 |
| §7 table | E_r, finite well, hard box, Γ, τ for s = 2.5 … 5.5 | verified; the s = 5.5 resonance 1.397 is missing (item 7) |
| §7 | "a few thousandths" | wrong for the upper levels: item 7 |
| §7 | 3D run s = 3.5, E = 0.35, τ = 65.2 against 58.3 | verified (65.221; the fit window ends at the end of the run, where P_in is at 6 %) |
| §7 | 4.5 and 5.5: E1 < 0.30; second near 0.931, 0.633 | verified |
| §8 table | E_r, κd, T, Γ exact, Γ (13), τ for 5 structures | verified (all reproduced by tm.py) |
| §8 | 22× more opaque, 24× narrower, τ = 344 against 14.2 | verified (21.9, 24.2) |
| §8 | "(13) within a quarter" | verified (worst case V0 = 1.5: 0.093 against 0.116, 20 %) |
| §8 | 0.735, 0.742, 0.744; 0.877; 0.64 | verified |
| §8 | run E = 0.7: lasts 213, fit from 91 gives 210 | verified (212.93, 90.95, 209.66) |
| §9 | TN_check 2.3e-12 at 251 energies | verified |
| Fig. 2 / §9 | band 0.59–0.955, gap 1.126, band 2 at 2.082, width 0.365 | verified |
| §9 | peaks N = 3, 5, 10 | verified |
| §9 | "0.735 is its middle"; "0.02 to 0.1 apart" | wrong: item 12 |
| §9 | ten walls: band 0.129, gap 0.0218 | verified (means of 4 twin values each) |
| §10 | 192×128×128 at 0.5 a = 96 a × 64 a; 256; 512 | verified (index: 1169 / 48 / 20 runs) |
| §10 | outer tenth, mask from 1 to 0 | verified (W = n//10 a side, sin^{1/8}, applied every step) |
| §10 | Δt = 0.01, two FFTs, 3.1 M points, about 1 ns per point | verified (NS = 1.0e-9 per cell-step, measured) |
| §10 | 3739 planned; A 1128, B 188, C 564, D 376, E 423, F 1000, G 60 | verified (`jobs()` run: 3739) |
| §10 | 47 energies 0.30–2.60; 25 energies 0.10–1.30 | verified |
| §10 | six parts, two T4 each; 1237 runs, 2 parts, 5.9 h | verified (sweep_s 10654.6 + 10695.4 s) |
| §10 | 200 frames, z = 0 half-plane, 8-bit levels, p(x,t), regions, 1D twin, SHA-256 checked by the page | verified (`rt3d2.run`, `rt3d-worker.js` crypto.subtle.digest) |
| §10 | mirror ψ(x,−y) = ψ(x,y); one height scale per run | verified (page: j = \|jj − 63\|, S = peakMax) |
| §10 | "same method and grid as Fig. 14" | unverifiable, because the Fig. 14 code was outside this check |
| §11 | 115 gen-1 runs; 1.8e-4 | verified (1.797e-4 at E = 0.735) |
| §11 | 0.186 against 0.196, 5 %; 22 % more at 0.4; 0.056 against 0.071 at 1.2, 20 % | verified (largest shortfall is 20.1 % at E = 1.2) |
| §11 | profiles differ by 3–4 % of the peak, up to 10 % late | unverifiable, because it needs the time-dependent exact profiles, which are not in the index |
| §11 | τ 15.1 (3D), 15.3 (twin), 14.2 exact; 6–8 % | verified |
| §11 | 0.179 against 0.186, 4 % | verified (T_far 0.17933) |
| §11 | 60 % → 5 % fit; T_far rule | verified (`fit_tau`, `summary`) |
| §11 | "twice as fine … twice the steps" | unverifiable, because the step error of the split also depends on how sharp the barrier edge is on the grid; it is not established |
| §12 | 2σ⊥ = 6 | verified (σ⊥ = 3 for \|ψ\|²) |
| §12 | E = 0.65 "nearest the resonance" | wrong: item 2 |
| §12 table | walls τ 15.1, T 0.176; R = 2: τ 1.99, τ_side 2.28, T 0.936; one disc R = 4 0.678, R = 6 0.415 | verified. τ_side from the rounded table values is 2.29. |
| §12 | "lifetime and share approach walls as R grows" | unverifiable, because only R = 2 has a filed pair run |
| §12 shells | 66.9 @ 0.30, 110 @ 0.35, 63.2 @ 0.40, 104 @ 0.45, 16 runs each | verified as stored; weakly measured: item 5 |
| §13 table | 2.75 nm, 4.13 nm, 300 meV, 110 meV, 10.6 meV, 62 fs | verified (a = 2.7536 nm; 110.2 meV; 10.56 meV; 62.3 fs) |
| §13 | peak at 0.735 / 0.483 / 0.226, height 1.0 / 0.877 / 0.559 | verified (same at nper = 60 and 200) |
| §13 | E_F = 1.0 (150 meV), k_BT = 0.05 (87 K) | verified (87.03 K); it matches `exact1d.py`. `iv.py`'s own default E_F = 1.4 is not used. |
| §13 | exact peak 0.875, valley 1.825, ratio 4.3 | verified (`iv_curve` recomputed to 5e-9 of the stored curve; also with a 3000-point energy grid) |
| §13 | "peak comes before … because the peak transmission falls" | unverifiable as stated. The area under the peak, which sets the current, falls only 18 % from V = 0 to 1 while the peak height falls 44 %. The threshold T → 0 as E → 0 matters too. |
| §13 runs | walls 0.5 / 1.375 / 5.0 from 170 of 500; discs 0.875 / 1.875 / 1.8 | the arithmetic is verified; as results they are wrong: item 1 |
| §13 | "near 2 THz" | verified against the cited 1.92 THz (Maekawa et al. 2016) |

## Notes

- The caller named this file. The standing instruction names `check.md`. I wrote only this file and changed no repository file.
- While I was checking, another session edited `notes/fig15/gen2_numbers.py` to add Fabry–Pérot numbers. The working tree was clean again by the end. The 235 NUM keys the committed note uses all reproduce.
