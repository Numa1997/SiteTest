# Fig. 15 lecture note: derivation and number check, generation 2, round 9

Checked version: `public/scripts/resonant-note.js` at commit 8aa4802 (md5 bc284a97…, 14 Nov 2026 09:16 UTC), with
`notes/fig15/gen2_numbers.py` at the same commit.
The render and the NUM comparison ran at 09:19 UTC, against those committed files. After 09:26 UTC, another session began
editing `resonant-note.js`, `gen2_numbers.py` and `referee.md` in the working tree (md5 of the note now 24af09c9…). Those
changes add a V0 = 3 long-packet table, add digits to the d = 1 bracketed values and reword §1 and §6. They are uncommitted and
were **not** checked here.

How I checked:
- I rendered the page in headless Chromium (Playwright, page served from `public/`). It has 1010 KaTeX blocks, 0 KaTeX errors,
  0 unrendered delimiters, no NaN/undefined/null in the text, 0 page errors, and tags (1)–(32) in order.
- The NUM block is identical to a fresh run of `gen2_numbers.py`: 335 keys, all equal. The only difference is that six band/gap lists
  are tuples in Python and arrays in JSON, which is the same data.
- Since round 8 (1cc135d), only these parts of the note changed: the d = 2 long-packet bracketed values (§6), the gap window (§9),
  the diode products (§13), and the same-energy diode paragraph (§13). No equation, no method text and no code file
  (`rt3d2.py`, `rt3d2_run.py`, the page, `rt3d-view.js`) changed. `file_rt3d2.py` now sets `iv.V0 = 2` before filing; the note
  does not depend on that.
- I re-derived the equations in SymPy myself (`r9/sym9.py` in the scratchpad).
- I recomputed every changed number from scratch, and also the core 1D numbers. For this I wrote three new pieces of code. None of
  them uses `tm.py` or `iv.py`:
  - an ODE integration (scipy DOP853) of χ'' = −2(E − V)χ through the biased pair;
  - a staircase transfer matrix with global-x matching, with slices aligned to the barrier faces;
  - an N-barrier transfer matrix with a k-space packet average.
- I recomputed the run-based numbers by reading `2026-11-14/kaggle/index.json` directly.
- Numbers whose text and NUM value have not changed since round 8 were checked independently in round 8. I confirmed that their
  values are unchanged and recomputed the ones marked "r9" below.

## Errors found

None. All four errors from round 8 are fixed correctly:

| Round-8 error | Now in the note | Check this round |
|---|---|---|
| 1. Same-energy diode sum computed at V0 = 3 | "top at V_b = 0.75 as the runs do, its valley at 1.75 and a ratio of 4.8" | ODE integration, V0 = 2, same 25 energies, same trapezoid and supply: peak 0.75, valley 1.75, ratio 4.811 |
| 2. "0.071 wide" | "0.0704 wide" | ODE: zero-bias FWHM 0.070405 |
| 3. Products 1.04, 0.74 | 1.03, 0.73 | Staircase: 0.07298 × 14.154 = 1.033; 0.04058 × 18.039 = 0.732 |
| 4. Gap "between 1.05 and 1.6" | "between 1.1 and 1.6" | Index: the 11 ten-wall runs used have E = 1.10 … 1.60, mean 0.02368 |

Two minor points. Neither is an error.
- §13, "the peak of T, 0.0704 wide": this is the zero-bias width. Near the diode's top (V_b = 0.75 to 0.875) the peak is 0.077 wide.
  The argument is the same either way.
- In the same-energy sum, the top at 0.75 beats 0.875 by only 0.4 % (1.0759 against 1.0715, own ODE). The sentence "comes from
  the coarse steps in energy" is supported by the computation, but by a narrow margin.

Data observation, not in the note: `index.json` `iv[flat].J_exact_single_energy_same_points` still holds the V0 = 3 values (for example
0.0841 at V_b = 0.125, against 0.2494 at V0 = 2). Nothing in `public/` reads it, and `gen2_numbers.py` no longer uses it.

## Equations

| Eq. | Verdict | How |
|---|---|---|
| (1) | verified | Standard TDSE. With ħ = m = 1 it becomes iψ_t = −½∇²ψ + Vψ. E_u = ħ²/ma² and t = ma²/ħ are consistent. |
| separation argument and phase e^{+i∫f dt} | verified | The product form makes each bracket a function of t alone. d/dt e^{i∫f} brings down −f in i ġ/g. |
| (2) | verified | Follows from the separation. SymPy: the free Gaussian g solves i g_t = −½ g_yy (residual 0). |
| free Gaussian g(y,t) (in-line) | verified | SymPy residual 0 |
| (3) | verified | SymPy: the variance of \|g\|² is σ²(1 + (t/2σ²)²). Units ħt/mσ² are dimensionless. At t = 0 it gives σ⊥. |
| (4) | verified | χ'' = −2(E − V)χ in flat regions |
| (5) | verified | SymPy solve of the continuity of χ and χ' |
| (6), w and γ referred to the centre | verified | SymPy product W_k(−d/2)⁻¹W_q(−d/2)W_q(d/2)⁻¹W_k(d/2): M₀₀ = w and M₀₁ = γ exactly, det = 1 |
| top-left element identity | verified | Contained in the same symbolic product |
| (7) | verified | Using cosh² + η² sinh² with k = √(2E), κ = √(2(V0 − E)): residual 1.8×10⁻¹⁵ at three parameter sets |
| (8) | verified | T = 1/\|w\|². SymPy limit d → 0 gives 1. R = 1 − T from \|w\|² − \|γ\|² = 1. |
| (9) | verified | SymPy: (8)/(9) → 1 as d → ∞ |
| (10) | verified | Geometric sum of bounces. Agrees with (13) and with the matrix product numerically (round 8; unchanged). |
| (11) | verified | SymPy small-T limit gives 4TaTb/(Ta + Tb)² ≤ 1 |
| (12) | verified | Definition r²e^{2iks} = Re^{iθ} |
| (13) | verified | SymPy identity (1 − Re^{iθ})(1 − Re^{−iθ}) = (1 − R)² + 4R sin²(θ/2) |
| (14) | verified | Resonance condition θ = 2πn |
| (15) | verified | SymPy: Lorentzian with Γ = 2T/(√R θ') |
| (16) | verified | SymPy: −2 ln R − 2T/√R = −T³/12 + O(T⁴), as the note states. ħ/Γ is a time. |
| (17) | verified | ħv/L_eff is an energy. Limits as stated. |
| phase average 1/√(1+F) | verified | Numerical quadrature at F = 3 gives 0.5 = 1/√4 |
| (18) | verified | Definition. The packet average was recomputed with my own k-space code (0.19591 at E = 0.735). |
| (19) | verified | SymPy: ∫ Lorentzian / (√(2π)σ_E) = √(π/8) Γ/σ_E |
| (20) | verified | SymPy: χ'/χ at L/2 is −k tan(kL/2) (even) and k cot(kL/2) (odd) |
| (21) | verified | ħ²/(mL²) is an energy |
| (22) | verified | SymPy: Re(e^{−iφ}e^{−iks}/√T) = cos(ks + φ)/√T |
| (23) | verified | SymPy: P^N = U_{N−1}(ξ)P − U_{N−2}(ξ)I for N = 2, 3, 5 on a general determinant-1 matrix |
| (24) | verified | λ + 1/λ = 2cos qs = trace P = 2ξ |
| (25) | verified | Strang split, matches `rt3d2.run` (unchanged since round 8) |
| (26) | verified | Exact for e^{−iEt}. The page `interp()` code is unchanged since round 8. |
| (27) | verified | Rates add. A model, not derived. |
| (28) | verified (order of magnitude) | mRW/ħ is a time |
| (29) | verified | `rt3d2.vbias` (unchanged). My ODE and staircase use the same linear drop from the first to the last outer face. |
| (30) | verified | SymPy: 2·2πk dk/(2π)² = (m/πħ²)dE⊥ and ∫₀^∞ dE⊥/(1 + e^{(E⊥−c)/kT}) = kT ln(1 + e^{c/kT}) |
| (31) | verified | SymPy prefactor: (m kT/πħ²)/(2πħ) = m kT/(2π²ħ³) |
| (32) | verified | Trapezoid over the 25 stored energies. Recomputed from the 500 index runs: identical (see §13 rows). |

## Numbers

"r9" means recomputed independently this round. "r8, unchanged" means the text and NUM value are identical to round 8, where they
were recomputed independently.

| § | Number in the note | Recomputed | Verdict |
|---|---|---|---|
| Abstract | 14 in a hundred; up to 512 × 128 × 128 | T = 0.14395 (r9); index boxes | verified |
| 1 | about 4 % per glass surface | 0.04 (r9) | verified |
| Fig. 1 | E/V0 true 0.37; stored E 0.30 … 2.60; diode down to 0.10 | 0.3675 (r9); index | verified |
| 2 | x0 14 before the face; 4σx = 48 | r8, unchanged | verified |
| 2 | σ⊥(40) = 7.3 | 7.31 (r9) | verified |
| 2 | k = 1.212, λ = 5.18, κ = 1.591, e^{−κd} = 0.204 | 1.2124, 5.1823, 1.5906, 0.2038 (r9) | verified |
| 2 | 0.37, κd = 1.59, σ_E/Γ = 2.9 | 0.367, 1.591, 2.870 (r9) | verified |
| 3 | sinh 2.351, \|w\|² 6.95, T 0.144, \|r\| 0.925 | 2.3514, 6.947, 0.14395, 0.9252 (r9) | verified |
| 3 Ex. 3.1 | 12.0, 3.72, 6.4×10⁻³, 22.5 | 12.017, 3.719, 6.397×10⁻³, 22.50 (r9) | verified |
| 3 | (9) gives 0.154 | 0.1545 (r9) | verified |
| 4 | (10) = matrix; \|t₂\|² = 1.000; Ex. 4.1 percentages | own N-barrier code T₂(0.735) = 0.999997 (r9); rest r8, unchanged | verified |
| 5 | θ = 2πn; ρ; 1/κ, L_eff, ħθ', 2L_eff/v; 0.3108 …; 1/√R | r8, unchanged | verified |
| 5 | Γ exact 0.0704; τ = 14.2 | FWHM 0.070405 (r9, ODE and staircase); 1/Γ = 14.20 (r9) | verified |
| 5 | Γ(15) 0.0699; (17) 0.0633; T/(2 − T) 0.078 | r8, unchanged | verified |
| 6 | σ_E 0.202; (19) 0.218; exact (18) 0.196; one barrier 0.149 | 0.2021, 0.2183, 0.19591 (r9); 0.149 r8, unchanged | verified |
| 6 | long packet: 2.67×, FWHM 0.119, σ_E 0.051, exact 0.54 | r8, unchanged | verified |
| 6 | d = 1 long: 0.7346 → 0.488 (0.49) vs 0.54; 0.713 → 0.524 (0.53) vs 0.5 | r8, unchanged | verified |
| 6 | d = 2 long: nearest 0.7432 passes 0.0197 **(0.023)** vs 0.0351; best 0.7215 0.0225 **(0.026)** vs 0.0319 | index (r9): 0.019661 + 0.005909/2 = 0.02262 → 0.023; 0.022473 + 0.007357/2 = 0.02615 → 0.026; 0.7215 is the largest share of the 15 runs | verified |
| 6 | d = 2: 509; lifetime 344; 0.00736; 39 % | index t_end 509.44, well 0.007357 (r9); 0.00368/0.00943 = 39.0 % (r9); 344 r8 | verified |
| 6 | (19) at 0.744: 0.0359 vs 0.0351 | r8, unchanged | verified |
| 7 | e^{−2κd}, (21), the s table, 2.028/0.314, 68.4 vs 58.3 (17 %) | r8, unchanged | verified |
| 8 | V0/d table; 22×, 24×; d = 2 run 0.75/217/92.7/210 | r8, unchanged | verified |
| 9 | band 0.59–0.955, gap 1.126, 2.082; N = 3, 5, 10 peaks; 2.3×10⁻¹² | r8, unchanged | verified |
| 9 | ten walls band 0.143 (exact 0.174) | exact 0.17446 (r9, own packet average over the 8 band energies) | verified |
| 9 | ten walls gap **between 1.1 and 1.6**, 0.0237 (exact 0.0351) | index: 11 runs E = 1.10 … 1.60, mean 0.023682 (r9); exact 0.035072 (r9, own code) | verified |
| 9 | rises above about 1.8 | r8, unchanged | verified |
| 10 | grid, border, Δt, run counts, 0.92 ns, 3739/3697/42/15, 30–537, GPU hours, 8-bit storage | r8, unchanged; NUM identical to a fresh run | verified |
| Reading the figures | scales, × 4 rule, Fig. 15b normalisation | r8 (page code unchanged) | verified |
| 11 | 115 runs; 0.186 vs 0.196; 3.0/2.4/5.8/66 %; τ 15.1/15.3/14.2; 0.179 vs 0.186 | r8, unchanged | verified |
| 12 | σ⊥ 3.6 at t ≈ 12; disc table; shells | 3.56 at 11.5 (r9); rest r8, unchanged | verified |
| 13 | a = 2.75 nm and the unit conversions | a = 2.754 nm (r9, m* = 0.067, E_u = 150 meV); rest r8 | verified |
| 13 | E_F 1.0, kT 0.05; 131 mV, 274 mV | 150 × 0.875, 150 × 1.825 | verified |
| 13 | exact I–V top 0.875, valley 1.825, ratio 4.3 | own staircase Tsu–Esaki, 0.025 V grid (r9): 0.875, 1.825, 4.320 | verified |
| 13 | levels 0.29 and 0.1; supply 14.2 and 18 | 0.2905, 0.0981; 14.154, 18.039 (r9) | verified |
| 13 | areas 0.103, 0.073, 0.041; heights 1, 0.65, 0.34; widths 0.0704, 0.077, 0.085 | 0.1030, 0.0730, 0.0406; 1.000, 0.652, 0.342; 0.0704, 0.0772, 0.0846 (r9) | verified |
| 13 | products **1.03** and **0.73** | 1.033 and 0.732 (r9) | verified |
| 13 | runs' curve: top 0.75, valley 1.625, ratio 4.4 | from the 500 index runs (r9): 0.75, 1.625, 4.367 | verified |
| 13 | one voltage step (0.125) before the exact top | 0.875 − 0.75 | verified |
| 13 | same-energy sum: top **0.75**, valley **1.75**, ratio **4.8** | ODE integration at V0 = 2 (r9): 0.75, 1.75, 4.811 | verified |
| 13 | peak of T **0.0704** wide; energies 0.05 apart | 0.070405 (r9); stored energy step 0.05 | verified |
| 13 | "valley 1.625 against 1.75, ratio 4.4 against 4.8" | as above (r9) | verified |
| 13 | discs R 6: 3.46 at 0.75, 2.82 at 2.375, ratio 1.2; walls top 0.96 | from the 500 disc runs (r9): 3.4617, 2.8210, 1.227; 0.9597 | verified |
| Fig. 3 | drawn levels and offsets | r8 (SVG unchanged) | verified |
| 14 | 6–8 % (17 % at s = 3.5); box 64 a | r8, unchanged | verified |
| Problems | Γ = 10.6 meV; L_eff 7.6 nm; τ values | r8, unchanged | verified |
| 13 | 0.30 eV offset for 35 % Al | Not re-read from Vurgaftman et al. (2001) this round; the note says "about" | unverifiable, because the source was not re-read here (round 6 checked it) |

## Numerical method against code

No code changed since round 8, and the method text did not change either. The line-by-line comparison of round 8 still holds:
- `rt3d2.py`: Strang split, Δt = 0.01, border mask sin^{1/8}, faces on odd multiples of 0.25.
- `rt3d2_run.py`: run lengths.
- `file_rt3d2.py`: twin T, T_far, the 60 % lifetime-fit rule, trapezoid J.
- The page `interp()` and `rt3d-view.js`.

The new diode paragraph says the same-energy sum uses "the same trapezoid sum … at the same 25 energies". That matches
`gen2_numbers.py` (trapezoid of `iv.T_biased_vec × iv.supply` over `c['energies']`, with `assert iv.V0 == 2.0`) and my
independent recomputation.
