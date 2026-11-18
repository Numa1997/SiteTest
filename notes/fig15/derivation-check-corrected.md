# Fig. 15 lecture note, corrected generation: derivation and number check

Checked: `public/scripts/resonant-note.js` at 960a5df (md5 a870330841c9…; unchanged at 1a6f98d, which only touches `referee.md`),
with `notes/fig15/gen2_numbers.py` at the same commit. I did not read `plan.md`. I ran no solver over any run (owner's rule).

How I checked:
- **NUM block.** I ran `gen2_numbers.py` without `--write`, with `PYTHONDONTWRITEBYTECODE=1` so no file changed. It reads the stored
  indexes and json files and evaluates tm.py, iv.py and `exact1d.tbar` (quadratures, not runs). All 515 keys are identical to the
  NUM block in the note.
- **Independent recomputation.** I recomputed the section 10 and 11 numbers myself, without the script, from:
  - `2026-11-18/kaggle/index.json` and `summary.json`;
  - `2026-11-14/kaggle/index.json`;
  - `notes/fig15/audit/twin_sources.json` and `twin_converge.json`.
- **Equations.** I re-derived the equations in SymPy, with small numerical checks using my own transfer matrix. The scripts are in
  the scratchpad (`sym.py`, `tmx.py`); none of them uses tm.py.
- **Method against code.** I read the method description against the code, line by line:
  - `correction/exact_wall.py` and `wall_gpu_run.py`;
  - `axisym.py`, `axisym_jax.py` and `rt2d_run.py`;
  - `file_corrected.py` and `classify_2d.py`;
  - `file_rt3d2.py` and `rt3d2_run.py`;
  - `audit/twin_sources.py` and `twin_converge.py`.
- **Rendering.** I rendered the page in headless Chrome 153 (puppeteer-core, served from `public/`, all `<details>` opened).
  Result: 1219 KaTeX blocks, 0 KaTeX errors, 0 page errors, and no NaN, undefined, null or "to come" in the text.
  - Tag order as rendered: (1)…(25), (25a)…(25e), **(26), (25f)**, (27)…(32).

## Errors found

1. **(25e) shows a stray semicolon.** It renders as "max(0.005, ;0.01 T_ref)".
   - The JS string holds `\;`. JavaScript turns that into a plain `;` before KaTeX sees it (resonant-note.js line 269).
   - Fix: write `\\;` there.
2. **The equation numbers are out of order.** (26) is in section 10 and comes before (25f), which is in section 11.
   - The reader sees …(25e), (26), (25f), (27).
   - Fix: renumber, for example (25f) → (26a) or (27), or move the page-blend equation's number after it.
3. **"A smaller time step … change[s] nothing to three digits".** This is said in section 11 ("A smaller time step and a box twice as
   long change nothing to three digits") and in section 10 ("a step four times smaller changes the first batch's results by nothing
   to three digits"). It is wrong for the running example's short packet.
   - In `twin_sources.json` the stored 0.186991 becomes 0.184662 at Δt = 0.0025: a change of −0.0023, or 1.2 %.
   - The note's own table shows this (0.187 against 0.185).
   - With cell averages at Δx = 0.0625, the change is 0.1956 → 0.2009 (`twin_converge.json`).
   - For the two long packets the claim holds: 0.19213 → 0.19229 and 0.17793 → 0.17789. The V0 = 3 peak moves 0.82756 → 0.82751.
   - Correct statement: a step four times smaller changes the long-packet results by at most 2×10⁻⁴. It changes the short packet by
     0.002, a quarter of that run's error of 0.0098 (exact 0.19683). So the time step is not the main cause.
4. **"the rule itself reads about 1 % long" (section 11).** The note computes this from rounded values: Math.round(100·(14.4/14.2 − 1)) = 1.
   - Unrounded, the fitted τ is 14.438 (index). ħ/Γ is 14.204 (Γ = 0.070405, my own transfer matrix).
   - So the rule reads 1.65 % long. Correct: "about 2 %".
5. **"The shares before, inside and beyond the barriers come from the probability current through the barrier faces … a check, not
   something put in" (section 10).** Only the shares before and beyond come from the current.
   - The share inside is ∫|χ|² on a fine Simpson grid between the faces: `Pst` in `wall_gpu_run.py` `core`, and THEORY_AND_CODE §4.2.
   - That is why the sum is a real check. If all three came from the current, they would add to 1 by construction.
   - Correct: "the shares before and beyond come from the current through the outer faces, integrated over time; the share inside is
     |χ|² integrated between the faces; the three add up to 1 within 2.6×10⁻⁵."
6. **"The walls under a voltage … no second, independent calculation has checked them" (section 10).** One biased wall was checked.
   - The (x, ρ) code's wall limit at V_b = 2.125, E = 0.5 gave 0.039134 against the exact 0.039048, a difference of 8.6×10⁻⁵
     (CORRECTION_LOG §7, THEORY_AND_CODE §9.3).
   - Correct: "one of the 475 biased walls was checked by the independent (x, ρ) code and agrees to 9×10⁻⁵; the others have no second
     calculation."
7. **"for V0 = 3 between 0.66 and 1.76 times" (section 11, "Over the stored energies").** This range quietly leaves out energies where
   T_ref < 10⁻³ (the filter in `gen2_numbers.py`).
   - At E = 0.30 (T_ref = 5.1×10⁻⁴) the ratio is 1.84.
   - Either say "where at least a thousandth gets through", or give 0.66–1.84.
   - For the running example and for d = 2 the filter changes nothing at the quoted precision (1.12 still rounds to 1.1).

Lesser points of wording. These are not wrong numbers:
- **(25a) under bias.** "Together these states can build any packet that starts on the left" holds only up to the right-incident
  states with −eV_b < E < 0, which only fade into the left side. Their share is at most the start packet's share inside a barrier,
  ≤ 2.1×10⁻⁵. THEORY_AND_CODE §3.4 says so; the note does not.
- **(25d) justification.** "What is still between the faces … will leave by one side or the other" explains P_M but not A_M. A_M was
  already absorbed by the side border while its x was between the faces. T_unc = ½(P_M + A_M) still bounds the error, because the
  true split of P_M + A_M lies between 0 and 1.
- "by up to 0.44 and 0.44" (section 11) reads oddly. Both maxima really are 0.44 (0.4352 walls, 0.4382 discs).

For the caller, not an error of the note: THEORY_AND_CODE §10.2 and CORRECTION_LOG §3.2 describe a 0.002 safety margin, with "545
kept". The filed index (`file_corrected.py` GATE) uses (25e) with no margin and keeps 745 discs. The note matches the index. But 200
of the 745 kept discs pass the gate by less than 0.002, which is about the (x, ρ) T's own convergence (0.0019). Those two docs are
stale on this point.

## Equations

| Eq. | What I did | Verdict |
|---|---|---|
| (1) | Units: ħ∂ψ/∂t and (ħ²/m)∇²ψ are both energy × ψ | verified |
| (2) | SymPy: χ(x,t)g(y,t) solves (1) when V = V(x) and each factor solves its own equation | verified |
| (3) | SymPy: the free Gaussian h solves iħ∂h = −(ħ²/2m)h″, and the exponent of \|h\|² gives σ⊥(t)² = σ⊥²(1 + (ħt/2mσ⊥²)²) | verified |
| (4) | E = k²/2 and V0 − E = κ²/2 with ħ = m = 1 | verified |
| (5) | SymPy: solved continuity of ψ and ψ′ for A, B | verified |
| (6), (7), (8) | Formula against my transfer matrix at (E, V0, d) = (0.735, 2, 1), (0.4, 3, 1.5), (1.2, 2, 2): agrees to 10⁻¹⁵ | verified |
| (9) | Ratio to (8) is 1.00005 at κd = 5; large-κd limit of (8) | verified |
| (10) | SymPy geometric series: Σ q²ⁿ = 1/(1 − q²) | verified |
| (11) | SymPy: exact peak TaTb/(1 − √(RaRb))² to leading order in T gives 4TaTb/(Ta + Tb)² | verified |
| (12)–(14) | Round-trip phase; (13) is the Airy form T²/((1 − R)² + 4R sin²(θ/2)) with R = 1 − T (SymPy) | verified |
| (15) | SymPy: FWHM of 1/(1 + (4R/T²)(θ′δE/2)²) is 2T/(√R θ′) | verified |
| (16) | τ = ħ/Γ; units are time | verified |
| (17) | Units: ħvT/L_eff is an energy | verified |
| (18) | Packet average; with \|φ\|² = \|G\|²/2π I find ∫\|G\|²dk/2π = 1 (SymPy) | verified |
| (19) | SymPy: Lorentzian area πΓ/2 times the Gaussian peak density 1/(√(2π)σ_E) gives √(π/8)Γ/σ_E | verified |
| (20), (21) | Finite-well conditions; SymPy: infinite-well n²π²ħ²/(2mL²) | verified |
| (22)–(24) | Chebyshev formula against my own N-barrier transfer matrix, N = 2, 3, 5, 10, 101 energies from 0.1 to 2.6: largest difference 7×10⁻⁹ | verified |
| (25) | Strang split; numerical BCH test on random Hermitian K, V: local error 1.2e-2, 1.6e-3, 2.0e-4 at dt = 0.1, 0.05, 0.025 (falls 8× per halving, so O(Δt³) per step and O(Δt²) per unit time) | verified |
| (25a) | Normalisation: ⟨ψ⁻_k\|ψ⁻_k′⟩ = 2π δ(k_R − k_R′) = 2π(k_R/k)δ(k − k′), since dk_R/dk = k/k_R (SymPy). So the closure weight is k/k_R and c± = ⟨ψ±\|χ0⟩. Dimensions: c ~ L^½, integrand ~ L^−½. At t = 0 it gives χ0; at V_b = 0, k_R = k. Matches `exact_wall.py` (Scatter, G, kgrid) and `wall_gpu_run.py` `core` | verified (bias caveat above) |
| (25b) | Parseval in k_R: ∫\|∫dk/2π A e^{ik_R x}\|²dx = ∫dk/2π (k_R/k)\|A\|². Numerical check at V_b = 0.7: 0.0421221535 both ways. At V_b = 0, c₋ ≈ t′*G(−k) ≈ 0 and c₊ ≈ G(k), giving (18). Code: `T_inf = Σ w/2π \|cP t + (k/kR) cM r′\|² kR/k` | verified |
| (25c) | SymPy: Cartesian ∇² of an axisymmetric function equals ∂x² + ∂ρ² + ρ⁻¹∂ρ; J0(kρ) is an eigenfunction with −k²; norm weight 2πρ. Limit: a disc wider than the radial range gives the wall, 0.196539 against 0.196820 (log). Code: `axisym.py` qdht with T(T²)^−½ (exactly orthogonal), M = T diag T, cell-averaged V | verified |
| (25d) | Same as `axisym_jax.py` lines 95 and 97: T = P_R + A_R + ½(P_M + A_M), with M meaning x between the faces at any ρ. Limit: once P_M, A_M → 0, T_unc → 0. Provisional iff T_unc > 0.005: all 2609 discs and shells in the index agree | verified (wording caveat above) |
| (25e) | Recomputed for every run: kept iff the gate passes, for 170/1088 walls and 745/2327 discs; error = T_old − T_ref to 10⁻¹⁶; shells not gated (T_old null) | formula verified; **rendering wrong** (error 1) |
| (25f) | SymPy: E ∝ L_eff⁻² gives δE/E = −2δL/L. Exact check with my transfer matrix at V0 = 3: dE/dL = −0.7116 against −2E/L_eff = −0.7101 | verified; **numbering out of order** (error 2) |
| (26) | SymPy: for ψ = φe^{−iEt} the blend reproduces φe^{−iE(t_f+δ)} exactly | verified |
| (27), (28) | Rates add; mRW/ħ has units of time | verified |
| (29) | Piecewise ramp, continuous at x_l and x_r | verified |
| (30) | SymPy: ∫₀^∞ dE⊥ /(1 + e^{(E+E⊥−E_F)/kT}) − kT ln(1 + e^{(E_F−E)/kT}) simplifies to 0 | verified |
| (31) | Tsu–Esaki form; units: e m kT/ħ³ × energy = C m⁻² s⁻¹ | verified |
| (32) | Trapezoid sum of (31) over the run energies; same as `gen2_numbers.py` and the index J_runs | verified |

## Numbers: sections 10 and 11 (the new text)

| Number | Recomputed from | Verdict |
|---|---|---|
| 192×128×128; 256; 512; 96 a, 64 a | 2026-11-14 boxes by N and σx (2838+376+141+141 at 192, 141 at 256, 60 at 512) | verified |
| λ 5.18, about 10 points; 5.5 at E = 2.60; k = 6.28; 0.2 rad; 0.6 rad; < 0.05 rad at k = 3 | 2π/√1.47 = 5.18, /0.5 = 10.4; 2.755/0.5 = 5.5; π²/0.01·0.005 = 0.197; ×3 = 0.59; 9·0.005 = 0.045 | verified |
| "three million points or more" | 192·128·128 = 3.15 M | verified |
| 0.92 ns | Σ wall / Σ(box·steps), 2026-11-14 = 0.9218 | verified |
| "nothing to three digits" (section 10) | twin_sources.json | **wrong** (error 3) |
| 3739 planned; 1128/188/564/376/423/1000/60 | 4·6·47, 2·2·47, 4·3·47, 8·47, 3·3·47, 2·20·25, 4·15; sum 3739 | verified |
| 42 duplicates; 3697 runs | 21 energies (0.30–1.30) × 2; 3739 − 42; index length 3697 | verified |
| 2.1×10⁻⁵ start share | max start_in_barrier 2.093e-5 | verified |
| 15 reruns; t 30–537 | `replaced` has 15 entries; t_end 29.85, 537.3 | verified |
| 18.6 h; 35.6 h | Σ sweep_s / 3600; Σ wall / 3600 = 35.60 | verified |
| 2000 slices, 8000 → 8×10⁻⁹ | THEORY §3.2 (CORRECTION_STATE measurement); code `segments(nslice=2000)` gives "about" 2000 (≥ 4 per segment) | verified against the record |
| dk 5×10⁻⁴; halving → ≤ 3×10⁻⁶ | `kgrid(dk=5e-4)`; THEORY §3.4 | verified against the record |
| closure 2.6×10⁻⁵ over 1088 walls | all 1088 walls have closure_max; max 2.586e-5 | number verified; **sentence wrong** (error 5) |
| cell 0.0625 a; radial range 64 a (discs), 160 a (shells) | `rt2d_run.py` GRID; THEORY §8.2 | verified |
| at most 0.0019 under refinement | CORRECTION_LOG §7: largest change 0.001898 (R12 N10, hx 0.125) | verified |
| 0.1965 against 0.1968 | 0.196539 / 0.196820 (log §7) | verified |
| drift up to 0.0048 | index: discs max 0.004807, shells 0.004199 | verified |
| c64 against c128: 6×10⁻⁴ discs, 0.0012 shell | log §7: 0.000582 (R6), 0.000605 (R12); shell 0.628891 − 0.627703 = 0.00119 | verified (largest disc gap is 6.05e-4) |
| T_unc > 0.005 → provisional: 72/2327 discs, 241/282 shells; up to 0.028 and 0.038 | index: 72, 241; max T_unc 0.02758, 0.03842 | verified |
| 170/1088 walls, 745/2327 discs kept; 918 and 1582 replaced; 282 shells | index status counts and gate recomputed | verified |
| median error 0.014 walls, 0.013 discs; max 0.44, 0.44 | 0.013607, 0.012759; 0.43519, 0.43820 | verified |
| "no second, independent calculation" (biased walls) | CORRECTION_LOG §7 | **wrong** (error 6) |
| 200 frames; 0.2 % of peak; 0.012 rad; 3 steps = 1.2 % | 0.5/255 = 0.196 %; π/255 = 0.0123; 3/255 = 1.18 %; `quantize` in rt2d_run.py | verified |
| 0.78–1.4 (running example) | T_old/T_ref: 0.7837–1.3953 | verified |
| 0.66–1.76 (V0 = 3) | 0.6647–1.7560 where T_ref > 10⁻³; 1.8356 at E = 0.30 | **incomplete** (error 7) |
| 0.66–1.1 (d = 2, s = 3.5) | 0.6550–1.1048 (1.1245 with the filtered energies) | verified |
| audit table, 3 rows × 6 columns | twin_sources.json, all 18 values to 3 digits | verified |
| "change nothing to three digits" (section 11) | row 3: 0.187 → 0.185 | **wrong** (error 3) |
| 0.0368, 0.0629, 0.0718, 0.0745; exact 0.0763 | twin_converge.json run 1 at dt 0.01 | verified |
| peaks 0.878 exact, 0.828 first grid; 0.905, 0.885, 0.880 | 0.87809, 0.82756, 0.90543, 0.88519, 0.87998 | verified |
| κ 2.06; L_eff 2.47; 5.8 %; 0.071 a; "a seventh" | 2.0601; 2.4708; 5.755 %; 0.0711; 0.142 of 0.5. Exact transfer matrix: a geometric widening of 0.073 gives 0.8276 | verified |
| "more than its own width" | shift 0.050 > Γ(V0 = 3) = 0.0291 | verified |
| 1.8×10⁻⁴ (3D against twin) | 2026-11-14 E = 0.75: sep_check_max 1.791e-4, defined in rt3d2_run.py:137 as max\|p3 − p1\|/max p1 over all frames | verified |
| 60 %–5 % fit rule; regions per shape | `file_rt3d2.fit_tau`; `file_corrected.summary` (shells: core + gap) | verified |
| τ 14.4 at E = 0.75 against ħ/Γ 14.2 | 14.438 (rebuilt run); 1/0.070405 = 14.204 | verified |
| "about 1 % long" | 1.65 % | **wrong** (error 4) |
| 15.1 in 3D | 2026-11-14 E = 0.75 τ = 15.138 | verified |
| 15.3 in its twin | needs the twin curve inside the run file, which is not in the repository | unverifiable here (round r8 measured 15.33) |
| 6–8 % | 15.138/14.204 = +6.6 %; 15.33/14.204 = +7.9 % | verified |
| box: 313 provisional; at most 0.038 | 0 + 72 + 241; max T_unc 0.0384 | verified |

## Numbers elsewhere in the note

| Item | Verdict |
|---|---|
| All 515 NUM keys | Identical to a fresh read-only run of `gen2_numbers.py` on the stored files. I read the script's correction part (counts, gate, T_unc, drift, closure, audit, pk, ge, gq, discs, shells, long packets) line by line; the logic matches the index fields. verified |
| Section 7 and 8 sentences that depend on kept/rebuilt status (P3_5 kept, V2D2 kept) | the index status matches the branch taken in the text. verified |
| Section 12 shells: "between 0.017 and 0.036 still inside" | sh*_unc 0.017, 0.024, 0.026, 0.036. verified |
| Section 13 diode: "4 of its 500 runs provisional"; "about 4 times" the walls' top current 0.99 | iv_disc6_prov 4; 3.9/0.99 = 3.94. verified |
| Equations and numbers not changed since c0ae537 | checked in round r10 (`derivation-check-gen2-r10.md`); NUM still identical, equations re-derived above |
