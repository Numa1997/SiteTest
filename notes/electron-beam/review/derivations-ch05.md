# Chapter 5 "The spot": derivation and number check

Reviewer's check of `public/portfolios/electron-beam/index.html`, `#ch05` (source `portfolios-src/electron-beam/text/ch05.py`;
solver `physics/ch05.js`, twin `ref/ch05.py`, checks `derive/ch05.py`, `data/ch05/derive_results.json`, `data/ch05/README.md`,
`data/ch05/objective_lens_cs_cc.csv`). 9 November 2026.

How it was checked:
- Equations re-derived in SymPy 1.14 (my own script, not `derive/ch05.py`): (5.1) solved for d_I, the cone solid angle, the Gaussian
  FW50 step behind B_pr = B_r/ln 2; P1 and P2 minimised symbolically with the second-derivative test; the disc of least confusion
  solved exactly; units with `sympy.physics.units`.
- The FW50 coefficients of (5.3) recomputed from first principles with SciPy: encircled energy of the Airy pattern, 1 − J₀(v)² − J₁(v)²;
  geometric FW50 of spherical aberration at its best plane (4×10⁵ rays, uniform current over the aperture); geometric FW50 of chromatic
  aberration for a Gaussian and a uniform energy distribution (2×10⁶ rays), referred to the FW50 of the energy distribution.
- Numbers: all 33 entries of `NUMS` recomputed in headless Chromium 153 (Playwright) from the built page's own modules
  (`EB.ch05/ch04/ch02.compute` with `EB.core.withDefaults(EB.contract, …)`, formatted with `EB.core.fmt`) and compared with every
  `[data-n="ch05.…"]` span of `#ch05`. No page errors. Closed forms (P4, P5, Problem 1, Joy) recomputed in mpmath (30 digits).
  Figure 5.1 recomputed with `ref/ch05.py` and compared with the page's SVG polylines point by point.
- Parity: `physics/ch05.js` in Node against `ref/ch05.py` on the module's four cases plus three more.
- Sources: Bronsgeest et al. 2008 could **not** be opened. Roads tried: `repository.tudelft.nl` (curl, twice, and Chromium's request
  client: connection reset at the proxy tunnel, `recentRelayFailures` names the host), `pubs.aip.org` PDF (403), `avs.scitation.org`
  PDF (403, 93-byte stub), CORE download (403 challenge; CORE API full text "not available for public API users"), Wayback (no snapshot
  of any copy), OpenAlex/Unpaywall/Semantic Scholar (only these copies), Semantic Scholar snippet search (429), Europe PMC full-text
  search (no open hit). Joy 2006 (J-STAGE PDF): 502 twice. So quotations of both papers are checked against physics and the project's
  own records only.

Scripts (scratchpad, not in the repository): `work/sym5.py`, `work/fw50.py`, `work/run5.cjs` (numbers in Chromium), `work/fig5.py`,
`work/corr5.py`, `work/par5.cjs`.

## Errors found (summary)

1. **(5.3), and everything computed from it: the FW50 diffraction coefficient is 0.54, not 0.66.** The FW50 diameter of an Airy
   pattern (the diameter holding half the current) is **0.535 λ/α** (encircled energy 1 − J₀² − J₁² = ½ at v = 1.680); a diameter
   0.66 λ/α holds 64 % of the current, not 50 %. The two other coefficients check out the same way (geometric FW50 of spherical
   aberration at its best plane 0.177 C_sα³ against 0.18; chromatic, Gaussian energy distribution, 0.601 C_cα ΔE_FW50/E against 0.6),
   so the 0.66 is the odd one out. Bronsgeest et al.'s own number confirms it: (π²/4)(0.54)²(h²/2me) B = **1.082×10⁻¹⁸ B**, exactly
   their quoted I_AI = 1.08×10⁻¹⁸ B. The correct form is d_A = 0.54 λ/α (the value Barth and Kruit and Kruit's group use; the paper
   itself could not be opened here, so the attribution of 0.66 to "Eqs. 18 to 21" is most likely a misreading of 0.54). Consequences
   (all from the page's code with 0.54; module, twin, contract text and `derive/ch05.py` P6 all carry 0.66):
   | number | page (0.66) | with 0.54 |
   |---|---|---|
   | d_A at 5 mrad (Example 5.1) | 5.72 nm | 4.68 nm |
   | d_p at 5 mrad | 6.48 nm | 5.54 nm |
   | optimum angle / smallest d_p (default) | 8.13 mrad / 5.27 nm | 7.42 mrad / 4.81 nm |
   | quadrature sum over FW50 | 1.7 | 1.9 |
   | 1 pA | 5.2 nm at 8.0 mrad | 4.7 nm at 7.2 mrad |
   | 1 nA | 7.4 nm at 11 mrad | 7.1 nm at 11 mrad |
   | immersion lens | 1.2 nm at 28 mrad | 1.1 nm at 26 mrad |
   | 30 kV | 0.64 nm at 8.3 mrad | 0.56 nm at 7.9 mrad |
   Figure 5.1 and the simulation's readouts move by the same amounts (about 10 %).
2. **§5.4 and check P6: the "disagreement inside Bronsgeest et al." does not exist.** It is an artefact of error 1. With d_A = 0.54 λ/α,
   Eqs. 6 and 19 give I_AI = 1.082×10⁻¹⁸ B (exact λ), equal to the quoted 1.08×10⁻¹⁸ B; the explanation "as if the quoted number counted
   only the current inside the FW50 disc" (factor ln 2) should go. The P6 row and the sentence "One disagreement we found inside Bronsgeest
   et al. … We use Eq. 6 as printed" should be replaced by an agreement check.
3. **Check P1 detail (checks table): both coefficients are wrong.** With A = 1.22λ, B = C_s/2: α_opt = (1.22²·4/3)^(1/8)(λ/C_s)^(1/4)
   = **1.09 (λ/C_s)^(1/4)** (page: "≈ 1.0"), and d_min = (4/3)^(1/2)3^(1/8)(1.22)^(3/4)(1/2)^(1/4) λ^(3/4)C_s^(1/4)
   = **1.29 λ^(3/4)C_s^(1/4)** (page: "≈ 0.93"). SymPy and a direct numerical minimisation agree (1.08945, 1.29307).
4. **Check P7 (§5.2: "FW50 0.160 eV", factor "0.743⁻¹"): the FW50 is biased by one grid step.** `derive/ch05.py` takes
   `searchsorted(cdf, cdf[i] + 0.5)`, the first node at or beyond the half, so every interval is too long by up to one grid step (2.85 meV
   near the peak). Interpolating the same CDF gives **FW50 = 0.1570 eV**, ratio **0.731** (FWHM 0.2147 eV unchanged); converged on a
   4× and 16× finer grid (0.15703 eV). The page should read "FW50 0.157 eV", "a factor 0.731⁻¹" (1.37).
5. **Example 5.2: "A thousand times the current costs a factor of a few in size" is wrong.** 1 pA → 1 nA takes the smallest probe from
   5.16 to 7.38 nm, a factor **1.43**. And "at large current the source image takes over" does not hold at 1 nA: at the optimum
   d_I = 3.6 nm is still smaller than d_C = 5.2 nm; d_I becomes the largest term only above about **4.5 nA** (cold source, default lens).
6. **Problem 3: the premise "the chromatic term enters both with similar weight" is false.** Chapter 2's Schottky preset has
   ΔE = 0.425 eV against 0.215 eV for the cold source, so its chromatic term is twice as large. At 0.1 pA, where d_I is negligible,
   the figure's gap (7.26 against 5.13 nm) is entirely the energy spread. The cold source wins on both brightness (2.2×10⁸ against
   1.7×10⁷) and energy spread.

Smaller points, not errors in the physics: Problem 2 asks for the change "at the optimum angle" and "at a fixed angle" in one sentence
(at fixed angle d_I grows ×10); the parity sentence "about 10⁻¹²" holds for the module's four parity cases (1.2×10⁻¹²) but not in
general (1.9×10⁻⁹ at V_land = 100 V, above the module's own tolerance of 10⁻⁹), because d_p is flat at its minimum and α_opt is only
defined to about √ε ≈ 10⁻⁸ in double precision; the knife-edge ratio "1.76" is 1.746 for a Gaussian probe.

## Equations

| Item | Verdict | Notes |
|---|---|---|
| §5.1 blur sizes: λ/α, C_sα³, C_cα ΔE/(eV*) | verified | Orders of magnitude; units m. |
| (5.1) I_p = B_pr V*(πd_I²/4)(πα²), d_I = √(4I_p/(π²B_pr V*α²)) | verified | SymPy solve. Units: A m⁻² sr⁻¹ V⁻¹ · V · m² · sr = A. Small-angle solid angle: 2π(1 − cos α) = πα² − πα⁴/12. Same as chapter 3's (3.7). |
| B_pr = B_r/ln 2 | verified | Gaussian source: I_tot/(πR₅₀²) = J₀/ln 2 (SymPy). d_I is then the FW50 diameter of the source image. Remark: the 'rss' convention adds this FW50 d_I in quadrature with full-width terms, one more inconsistency of that convention. |
| Key-result box: d_A, d_I ∝ 1/α; d_C ∝ α; d_S ∝ α³ | verified | From (5.1)–(5.3). |
| (5.2) quadrature sum with 1.22λ/α, ½C_sα³, C_c(ΔE/eV*)α, d_I | verified | Units: each term m (ΔE/(eV*) dimensionless, J/(C·V)). Limits: each term alone returns itself. |
| "Airy disc out to its first dark ring" = 1.22λ/α | verified | First zero of J₁ at v = 3.8317: diameter 1.2197 λ/α. |
| "Airy disc to its first zero holds 84 %" | verified | 1 − J₀² − J₁² = 0.8378. |
| Disc of least confusion: diameter ½C_sα³, "a little before the paraxial image" | verified | SymPy: at Δz = −¾C_sα², r(α) = +C_sα³/4, r(α/2) = −C_sα³/4, so the width is C_sα³/2, toward the lens. "Half as wide as the miss C_sα³" is right if "miss" is the radial miss at the paraxial plane (the paraxial disc is 2C_sα³ wide). |
| Chromatic term C_cα ΔE/(eV*) = "spread of focus across the energy width" | verified | Rays with δ ∈ [−ΔE/2E, ΔE/2E] miss by C_cαδ: diameter C_cαΔE/E. |
| "a disc of least confusion holds all of it" | verified | Geometric. |
| (5.3) d_p = √(((d_A⁴+d_S⁴)^{1.3/4} + d_I^{1.3})^{2/1.3} + d_C²) | verified (form) | Units m; each term alone returns itself. The form is the Barth–Kruit rule as commonly quoted; the paper could not be opened. |
| (5.3) d_A = 0.66 λ/α | **wrong, because** the FW50 of the Airy pattern is 0.535 λ/α and Bronsgeest's own I_AI = 1.08×10⁻¹⁸ B needs 0.54 | Error 1. Correct: d_A = 0.54 λ/α. |
| (5.3) d_S = 0.18 C_sα³ | verified | Geometric FW50 at the best plane (Δz = −0.375 C_sα²): 0.1768 C_sα³. Attribution to the paper unverifiable. |
| (5.3) d_C = 0.6 C_c(ΔE/eV*)α, ΔE the FW50 | verified | Geometric FW50 for a Gaussian energy distribution 0.601, uniform 0.586 (× C_cα ΔE_FW50/E). Bronsgeest writes V_p, the note V*: 0.08 % at 800 V. |
| "Their ΔE is the FW50; we feed the FWHM … our chromatic term is on the safe side" | verified (direction) | FWHM > FW50, so d_C is overestimated; the factor is 0.731⁻¹, not 0.743⁻¹ (error 4). |
| §5.3 α⁸ = A²/(3B²) for A²/α² + B²α⁶ | verified | SymPy; f″ > 0 there. |
| "optimum grows only as the fourth root of λ/C_s" | verified | α_opt = (A²/3B²)^{1/8} with A ∝ λ, B ∝ C_s. Twice C_s: angle × 0.84. |
| α = √(A/K), d = √(2AK) for A/α and Kα | verified | SymPy. |
| "at low voltage … the spot scales as the square root of C_c times the energy spread" | verified | d_min = √(2·1.22λ·C_cΔE/(eV*)). |
| Problem 1: d_min = (4/3)^{1/2}3^{1/8}A^{3/4}B^{1/4} | verified | SymPy: 2·3^{5/8}/3 · A^{3/4}B^{1/4}, the same. Default lens, 800 V, rss: 5.557 nm. |
| Problem 2 | verified, with a remark | d_I ∝ √I_p: ×10 at fixed angle. The sentence asks "at the optimum angle" and "at a fixed angle" at once. |
| Problem 3 | **wrong, because** the Schottky preset's ΔE (0.425 eV) is twice the cold one (0.215 eV), so the chromatic term does not enter "with similar weight" | Error 6. |
| Check P1 detail: α_opt ≈ 1.0(λ/C_s)^{1/4}, d_min ≈ 0.93 λ^{3/4}C_s^{1/4} | **wrong, because** the coefficients are 1.089 and 1.293 | Error 3. |
| Check P3: width ½C_sα³ at Δz = −¾C_sα² | verified | Exact (SymPy), as above. |
| Check P6: (π²/4)(0.66)²λ²V B | **wrong, because** the coefficient is 0.54: (π²/4)(0.54)²λ²V B = 1.082×10⁻¹⁸ B | Error 2. Algebra of I_AI from Eq. 6 with d_I = d_A is right. |

## Numbers (page value read from the DOM; recomputed with the page's own modules in Chromium)

All 30 numbers shown in `#ch05` are reproduced digit for digit by the page's code. The verdicts below are about whether the number is right.

| Number on page | Page | Recomputed | Verdict |
|---|---|---|---|
| C_s (ch04 module) | 4.19 mm | 4.188968 | verified; ch04 at 30 kV gives the same C_s and C_c (4.188968, 2.847594 mm), which supports Example 5.3's "same lens geometry". Chapter 5 itself uses the rounded contract values 4.19 and 2.85 mm. |
| C_c | 2.85 mm | 2.847594 | verified |
| B_r (ch02) | 2.13 × 10⁸ | 2.12602×10⁸ | verified (chapter 5 uses the contract's 2.13×10⁸; 0.2 % apart) |
| ΔE (ch02) | 0.215 eV | 0.2147259 | verified |
| d_A, FW50, 5 mrad | 5.72 nm | 5.72137 | **wrong, because** of 0.66 (error 1): 4.68 nm |
| d_S, FW50 | 0.0943 nm | 0.094275 | verified (0.18·4.19 mm·(5 mrad)³) |
| d_C, FW50 | 2.29 nm | 2.29290 | verified (with FWHM input, as stated) |
| d_I | 0.812 nm | 0.811742 | verified |
| d_p, 5 mrad | 6.48 nm | 6.48477 | **wrong, because** of error 1: 5.54 nm |
| α_opt FW50 | 8.13 mrad | 8.13135 | **wrong** (error 1): 7.42 mrad |
| d_p at optimum | 5.27 nm | 5.27428 | **wrong** (error 1): 4.81 nm |
| "Diffraction dominates at this angle" | – | d_A 5.72 of 6.48 nm | verified (still true with 0.54: 4.68 of 5.54) |
| rss d_p, 5 mrad | 11.3 nm | 11.2774 | verified |
| rss d_p at optimum | 9.08 nm | 9.07922 | verified |
| rss optimum | 8.14 mrad | 8.13621 | verified |
| rss/FW50 | 1.7 | 1.7214 | **wrong** (error 1): 1.9 |
| 1 pA | 5.2 nm at 8.0 mrad | 5.1569, 7.9508 | **wrong** (error 1): 4.7 nm at 7.2 mrad |
| 1 nA | 7.4 nm at 11 mrad | 7.3828, 11.2438 | **wrong** (error 1): 7.1 nm at 11 mrad (10.8) |
| "a thousand times the current costs a factor of a few" | – | 7.38/5.16 = 1.43 | **wrong, because** the factor is 1.4 (error 5) |
| "at large current the source image takes over" | – | at 1 nA: d_I 3.6, d_C 5.2, d_A 2.5 nm | **wrong at 1 nA, because** d_I is the largest term only above ≈ 4.5 nA (error 5) |
| immersion lens (C_s 0.2, C_c 0.1 mm) | 1.2 nm at 28 mrad | 1.2464, 27.674 | **wrong** (error 1): 1.1 nm at 26 mrad. "The lens, not the source, sets the spot": verified (d_I 0.15 of 1.25 nm). |
| 30 kV | 0.64 nm at 8.3 mrad | 0.64013, 8.2846 | **wrong** (error 1): 0.56 nm at 7.9 mrad. "Shorter wavelength and smaller relative energy spread both help": verified. |
| P4 closed form | 10.99 mrad | 10.98716 (mpmath 10.9871588077) | verified |
| P5 closed form | 8.318 mrad | 8.317860 (mpmath 8.3178595368) | verified |
| "reproduces the closed form of P1 to seven digits" | – | checks P4, P5 pass at 10⁻⁷ | verified |
| FW50 of the energy distribution | 0.160 eV | 0.15961 (derive) | **wrong, because** of the grid bias (error 4): 0.157 eV |
| FWHM | 0.215 eV | 0.21473 | verified (my own half-maximum search 0.21470) |
| FW50/FWHM | 0.743 | 0.74331 | **wrong** (error 4): 0.731 |
| Joy recomputed | 18.1 nm | 18.11394 (mpmath 18.1139357) | verified; λ(1 kV) = 0.038764 nm |
| Joy: "at his own optimum … the sum is smaller" | – | diffraction = chromatic at 2.600 mrad, 12.86 nm (true quadrature minimum 2.600 mrad, 12.86 nm) | verified |
| Checks table P1–P8 detail figures | as shown | equal to `derive_results.json` | P1 detail wrong (error 3), P6 premise wrong (error 2), P7 values wrong (error 4); P2–P5, P8 verified |
| P6: 1.617×10⁻¹⁸ B, 1.548×10⁻¹⁸ B, 0.698 | as shown | arithmetic right | **wrong premise** (error 2): with 0.54, 1.082×10⁻¹⁸ B |
| Simulation readouts | 6.48 nm, 0.812 nm, 8.13 mrad, 5.27 nm | same | same as Example 5.1 (error 1 applies) |
| Figure 5.1 | 2 × 41 points | `ref/ch05.py`: max 0.05 px from the SVG | verified as a plot of the code; all points inside the axes (5.1–12.1 nm cold, 7.3–31.7 nm Schottky). Moves with error 1. Remark: the figure's cold source uses t_clean = 0 (B_r 2.17×10⁸), Example 5.1 the default (2.13×10⁸); 5.273 vs 5.274 nm at 10 pA. |

## Quotations and literals

| Quotation | Verdict |
|---|---|
| Bronsgeest et al., JVST B 26, 949 (2008), Eqs. 18–21: 1.3 exponent, 0.18, 0.6 | unverifiable against the paper (not reachable, roads above); 0.18 and 0.6 agree with my first-principles FW50 values; the root-power-sum form matches the standard quotation. |
| Bronsgeest et al.: d_A = 0.66 λ/α | wrong, almost certainly a misreading (error 1). |
| Bronsgeest et al.: I_AI = 1.08×10⁻¹⁸ B | consistent with 0.54 and Eq. 6 (1.082×10⁻¹⁸); the paper's text unverifiable. |
| Bronsgeest et al.: FW50 = 1.76 × the 25–75 % edge width "for any of the probe shapes they tried" | unverifiable (paper not reachable). For a Gaussian probe the ratio is 2√(2 ln 2)/(2√2 erf⁻¹(½)) = 1.746. |
| Barth and Kruit, Optik 101, 101 (1996): FW50 fit to wave-optical calculations | unverifiable (abstract only, as the note says). |
| Joy, J. Surf. Sci. Nanotechnol. 4, 369 (2006): C_s = C_c = 5 mm, 4 mm WD, 1 keV, 0.7 eV, 0.61λ/α, "about 18 nm" at 4–5 mrad | unverifiable against the paper (J-STAGE 502); agrees with `data/ch05/README.md` and the CSV (both from an excerpt). The README rightly notes 0.61 λ/α is a radius. |
| Tsuno et al. (1995) C_s 0.2 mm, C_c 0.1 mm, calculated | verified against the project CSV (row "combined lens with specimen immersed in the electrostatic field", from the abstract). |
| "0.17 to 5 mm in C_s" | verified against the CSV (0.168 to 5 mm among lenses; the 0.1 mm row is a requirement, not a lens). |
| "magnetic immersion lenses reach a few tenths of a millimetre" | verified loosely: 0.168 mm (magnetic immersion objective, Ultramicroscopy 2002 excerpt); Tsuno's magnetic immersion minimum is 1.0 mm, and the 0.2 mm row is a combined electrostatic–magnetic lens. |
| Scherzer: round static lenses have C_s, C_c that cannot be made zero | verified as the standard statement (also needs charge-free fields, as the README's CEOS quote says). |

## Numerical method against the code

| Text | Code | Verdict |
|---|---|---|
| "golden-section search on ln α" (page); header "over [0.1, 100] mrad, 80 steps" | `lo = ln 1e-4`, `hi = ln 1e-1`, g = (√5−1)/2, 80 iterations, returns exp of the midpoint; the update rules are the standard ones | verified. d_p is unimodal in ln α (rss: d_p² is a sum of exponentials in ln α, convex). Iterations past about 40 only resolve rounding: the minimum is quadratic, so α_opt is defined to ≈ 10⁻⁸ relative. Over the 128 corners of the slider ranges the optimum stays inside the bracket except one (C_s = C_c = 0.1 mm, 100 V, 10 nA, ΔE = 0.01 eV, B_r = 10⁶, fw50), where it returns the edge, 100 mrad, without a warning; optima above 50 mrad also fall outside the plotted range and the unclipped "optimum" dot is drawn outside the frame. Remark, not an error in the text. |
| (5.1) in code | `Bpr = B_r/LN2`, `dI = sqrt(4 I_p/(π² Bpr Vs α²))` | verified |
| (5.2) in code ('rss') | 1.22 λ/α, 0.5 C_sα³, C_c·rel·α, quadrature with dI | verified |
| (5.3) in code ('fw50') | 0.66 λ/α, 0.18 C_sα³, 0.6 C_c·rel·α, `inner = (dA⁴+dS⁴)^{1.3/4} + dI^{1.3}`, `sqrt(inner^{2/1.3} + dC²)` | matches the text (both carry error 1) |
| λ, V*, rel | λ = h/√(2m_e e V*), V* = V(1 + eV/2mc²), rel = ΔE/(eV*) | verified (λ(800 V) = 43.3437 pm, mpmath) |
| "With the chromatic term and the current switched off" (P4) | `I_p = 1e-30`, `C_c = 1e-12`, 'rss' | verified; P5 uses `C_s = 1e-12` |
| Parity: "10⁻¹⁵ in the closed formulas" | measured 1.1×10⁻¹⁶ (d_p), 6.7×10⁻¹⁶ (curve) | verified |
| Parity: "about 10⁻¹² in the optimum angle" | module cases: ≤ 1.2×10⁻¹²; V_land = 100 V: 1.9×10⁻⁹ | verified for the tested cases; not general (remark above) |
| Simulation caption: probe (wine) and four parts, log axes, "optimum" dot | `draw`: series colours, `X` log over 0.5–50 mrad, `mark(alpha_opt, d_p_opt, …, 'optimum')` and 'now' | verified |
| Figure 5.1: "computed with the same formulas as the simulation (ref/ch05.py)" | `fig_curve` calls `R5.optimum` and `R5.terms` | verified |
