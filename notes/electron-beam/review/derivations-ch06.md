# Chapter 6 "Scan and hit": derivation and number check

Reviewer's check of `public/portfolios/electron-beam/index.html`, `#ch06` (source `portfolios-src/electron-beam/text/ch06.py`;
module `physics/ch06.js`, twin `ref/ch06.py`, checks `derive/ch06.py`, data `data/ch06/derive_results.json`, `data/ch06/mc_runs.json`,
`data/ch06/*.csv`, `data/ch06/README.md`). 9 November 2026. Chapter 6 only.

How it was checked:
- Equations re-derived in SymPy 1.14 with my own script, not `derive/ch06.py`. (6.1) came from the classical orbit
  b = k/(pv) cot(φ/2) through dσ/dΩ = (b/sin φ)|db/dφ|. I integrated the screened form and inverted its cumulative fraction for (6.6),
  checked the pv identity and its limits, recomputed the constants of (6.3) and (6.5) from CODATA with `sympy.physics.units`, and derived
  the escape integral in closed form. I also integrated the Joy–Luo path length to test the exponent claim behind (6.7).
- Numbers: every `[data-n="ch06.…"]` span of `#ch06` (44 spans, 42 keys) was recomputed in headless Chromium 153 (Playwright) from the
  built page's own modules: `EB.ch06.compute` with `EB.core.withDefaults(EB.contract, …)`, plus `EB.ch06.mfp/stop/Jkev` and `EB.core.C`.
  The 48 stored runs behind the figures (4 materials × 12 energies, 2000 electrons each) were rerun in Chromium as well. The
  database means, the ESTAR ratios and Lin and Joy's law were recomputed from the CSV files. Each value was formatted with the page's `fmt`
  and compared with the DOM text. No page errors (the only console error is a font CORS refusal under `file://`).
- Figures 6.1 and 6.2: the page's SVG polylines were compared with the Chromium runs mapped through the stated axes. The ESTAR table
  on the page was compared with the recomputation.
- Parity: `physics/ch06.js` in Node was compared with `ref/ch06.py` on the module's 5 cases plus 2 more, including the drawn paths. I also ran the repository's
  `checks/check_parity.py`.
- Method: `physics/ch06.js` lines 67–124 were read against the note's §6.4 and §6.6 sentence by sentence. On a scratch copy I counted
  how often the near-axis branch of `turn` fires and what changes when it is made exact.
- Sources:
  - Lin and Joy 2005: opened in full (my own download from psec.uchicago.edu; Eqs. 1–3, 12 and 13 and Table 1 read on the
    rendered page).
  - Joy et al. 1996: read from a full-text copy already in this session's scratchpad (`scratchpad/joy/joy1996.txt`). My own downloads
    from digitalcommons.usu.edu returned 403.
  - Joy 1991: **not opened**. Roads tried:
    - digitalcommons PDF with curl: 403.
    - The same PDF through headless Chromium: refused by the session's permission classifier as bot-check circumvention; not retried.
    - Wayback snapshot (exists, 19 July 2024): over http, "Blocked by egress policy"; over https, refused by the permission classifier.
    - OpenAlex API: 429, daily budget used up.
    - CORE API: 429.

  So every statement attributed to Joy 1991 (quotations, equation numbers 1, 4, 6, 12, Bishop's fit) is marked unverifiable below.
  The physics of those formulas is re-derived independently.

Scripts (scratchpad `/tmp/claude-0/-home-user-SiteTest/c8b76f47-83f6-5259-bec8-4485c7f5a448/scratchpad/ch06d/work/`, not in the
repository): `sym6.py` (derivations), `run6.cjs` + `cmp6.py` (numbers in Chromium), `fig6.py` (figures, per-energy comparison),
`par6.cjs` (parity, near-axis rotation), `near.cjs` + `ch06_probe.js` (branch count and effect), `ch5.cjs` (chapter 5 probe size),
`sim6.cjs` (simulation readouts), `ch06_probe2.js` (step counts).

## Errors found (summary)

None changes a number shown on the page. Four statements are wrong or only approximately true:

1. **(6.3), second equality: 1024 stands for 2mc², which is 1022.0 keV.** 1024 is the value Joy prints, and the code uses it. The page
   writes "=" between $(E+mc^2)/(E+2mc^2)$ and $(E+511)/(E+1024)$. The page names the other gap in the same line (5.21 against 5.18,
   +0.51 %) but not this one. Effect of 1024 against 1022: σ_E lower by 0.39 % (0.8 keV) to 0.36 % (100 keV). Together with the
   constant, the page's σ_E is 0.12 to 0.15 % above the exact Rutherford-with-pv value. λ_el(100 keV, Si) would be 105.35 nm instead of
   105.19 nm, so the shown "105" stands. Fix: write "≈", or say "1024 as Joy prints it (2mc² = 1022 keV)".
2. **§6.4 step 4 and check M4: the rotation is not "built from c without that division" for every direction.**
   - `turn` (physics/ch06.js line 58) has a second branch: for |c_z| > 0.99999 it returns
     `[sin φ cos ψ, sin φ sin ψ, ±cos φ]`. That turns about the z axis, not about c, so the angle to c is off by up to the tilt of c,
     arccos 0.99999 = 4.5 mrad. Measured on 20 000 tilted cases: largest angle error 4.46×10⁻³ rad.
   - M4's random directions reach this branch with probability about 10⁻⁵ per case, so M4 does not test it. The note's "makes exactly the
     angle φ" is therefore not true for this branch.
   - Measured effect is nil at the page's precision. Off-axis use of the branch: 0, 49 and 1 times in 0.09, 1.18 and 0.23 million turns
     (Si 800 V, Si 30 kV, Au 800 V). With an exact near-axis rotation, η and δ are unchanged to 4 digits and r90(Si, 30 kV) moves from
     6547.18 to 6547.06 nm.
   - Fix: build ê₁, ê₂ from (c_x, c_y)/√(c_x² + c_y²) in that branch as well (exact to 3×10⁻¹⁶, tested), keeping the axis case
     c = (0, 0, ±1). Or say in the text that near the axis the rotation is taken about z.
3. **Problem 1: "half of the elastic turns are smaller than the angle with 1 − cos φ = 2a" is true only to first order in a.**
   The cumulative fraction of the screened law is F(x) = (1+a)x/(x+2a) with x = 1 − cos φ. So:
   - F(2a) = (1+a)/2, which is 51.2 % for silicon at 800 eV;
   - the exact median is x = 2a/(1+2a).

   The body text's "half of the turns are smaller than about 2√a" is fine. Exact median 0.309 rad against 2√a = 0.316 rad at 0.8 keV;
   both are 0.0515 rad at 30 keV. Fix: "about half", or ask for the exact median 2a/(1+2a).
4. **§6.3, "with it the formula stays positive": not down to zero energy.** With k = 0.85 the logarithm of (6.5) is positive only for
   E > J(1/1.166 − k) = 0.0076 J, which is 1.3 eV in silicon and 6.1 eV in gold (Joy et al. 1996 say the same: the sign change moves to
   J(0.857 − k)). At E = 0 the argument is 0.991. The claim holds over the whole simulated range (E ≥ 50 eV). Fix: "stays positive
   down to a few electronvolts".

Remarks (statements that are true but could mislead, or gaps outside the chapter text):
- **Gold δ at 800 V is too high as well, not only η.** Example 6.1 gives δ(Au) = 1.5 and flags only η as too high. Lin and Joy's own
  δ_max for gold is 1.28 (at 0.50 keV), and their universal law gives 1.16 at 0.8 keV. The simulated gold δ is 1.37–1.47 between 0.5 and 1 keV.
- §6.5, "At higher energy ours is smaller": true at 20 keV for all four elements. At 2 keV it is true for Si, Al and Cu, but gold is
  larger (1.049 ± 0.018 against 0.94; M10 shows it, Figure 6.2 shows it).
- Lin and Joy's universal law (their Eq. 12, quoted correctly) peaks exactly at E = E_max but with value 1.28(1 − e^−1.614) = 1.025 δ_max,
  not δ_max. This is in the paper itself; the page reproduces it faithfully.
- Lin and Joy print their Eq. 13 without ρ (mass stopping power, 78 500 Z/(AE) …). The page's (6.5) has ρ and keV/cm, which is the
  correct per-length form (2π(e²/4πε₀)² N_A = 78 457 keV² cm² mol⁻¹). This is an attribution detail, not an error.
- `data/ch06/README.md` calls the universal law "the paper's Eq. 5". In the paper it is Eq. 12 (Eq. 5 is the constant-stopping-power
  yield δ = 0.5(E/εR)(λ/R)…(1 − e^−R/λ)). The page says Eq. 12, which is right. The README is outside chapter 6's text and was not changed.
- §6.1 says the nuclei are "tens of thousands of times heavier" than the electron. Si is 51 197 m_e and Al 49 180 m_e, but Cu is
  1.16×10⁵ m_e and Au 3.59×10⁵ m_e. The silicon numbers given are right.
- Parity "about 10⁻⁹": the repository check reports 1.2×10⁻⁹. That is the relative difference of one drawn-path coordinate of size
  2.6×10⁻⁵ nm (absolute difference 3×10⁻¹⁴ nm). All scalar readouts agree to 2.6×10⁻¹⁴ on 7 cases, and the drawn paths to
  ≤ 1.7×10⁻¹⁰ nm absolute. The module's tolerance note says r90 and V_int differ "by about 1e-9 (measured)"; I measured ≤ 3×10⁻¹⁴ for them.

## Equations

| eq. | content | verdict |
|---|---|---|
| (6.1) | dσ/dΩ = (Ze²/4πε₀)² (pv)⁻² (1 − cos φ)⁻² | **verified.** From b = k/(pv) cot(φ/2): (b/sin φ)\|db/dφ\| − (6.1) = 0 (SymPy, exact). With pv = 2E it equals (k/4E)²/sin⁴(φ/2), the textbook form, as stated. Units: (J m)²/J² = m². Diverges as φ → 0, as stated. |
| (6.2) | a = 3.4×10⁻³ Z^0.67/(E/keV) | **verified** as dimensionless and as used by the code (`screen`); a → 0 as E → ∞ (screening matters less for fast electrons). Si: a = 0.0249 at 0.8 keV ("a few hundredths", right), 6.6×10⁻⁴ at 30 keV. The constant and its attribution (Bishop 1976 via Joy) are **unverifiable, because** Joy 1991 could not be opened (see header). |
| (6.3) | σ_E = (Ze²/4πε₀)² π/(a(1+a)) E⁻² ((E+mc²)/(E+2mc²))² = 5.21×10⁻²¹ Z²/E² · 4π/(a(1+a)) · ((E+511)/(E+1024))² cm² | **first equality verified**: ∫dΩ (1−cos φ+2a)⁻² = π/(a(1+a)) (SymPy), and 1/(pv)² = E⁻²((E+mc²)/(E+2mc²))² exactly. Limits: pv/(2E) → 1 for E ≪ mc², pv/E → 1 for E ≫ mc². Units cm². **Second equality wrong in the last digits, because** 2mc² = 1022.0 keV, not 1024 (σ 0.36–0.39 % low), and 5.21 is 0.51 % above (e²/4πε₀)²/4 = 5.1837×10⁻²¹ keV² cm² (the page states this one). Correct: 5.18×10⁻²¹ … ((E+511)/(E+1022))². No shown number changes. |
| (6.4) | λ_el = A/(N_A ρ σ_E) | **verified**: n = N_A ρ/A; units g mol⁻¹/(mol⁻¹ g cm⁻³ cm²) = cm (sympy.units). The code is the same with ×10⁷ to nm. |
| (6.5) | −dE/ds = 78 500 ρZ/(AE) ln(1.166(E+kJ)/J) keV/cm, k = 0.85 | **verified**: 2π(e²/4πε₀)² N_A = 78 457 keV² cm² mol⁻¹ (page 78 500, rounded); units keV/cm with ρ in g cm⁻³, A in g mol⁻¹, E in keV. 1.166 = √(e/2) = 1.1658. Ratio of the logarithms → 1 as E → ∞ (Bethe limit). Without kJ the log is negative below J/1.166 (Si 148 eV), as stated. Matches Lin and Joy's printed Eq. 13 (opened), with ρ added for the per-length form, and Joy et al. 1996 Eq. 2 (copy read). The "stays positive" sentence is only approximately true (summary item 4). |
| J | J = (9.76Z + 58.5Z^−0.19) eV | **verified** numerically (Si 172.07, Au 796.54 eV; within 2.5 % of ESTAR's 173, 166, 322, 790 eV for Si, Al, Cu, Au). Equation number "Joy's Eq. 12" **unverifiable, because** Joy 1991 was not opened. |
| (6.6) | cos φ = 1 − 2aR₂/(1 + a − R₂) | **verified**: cumulative fraction F(x) = (1+a)x/(x+2a), x = 1 − cos φ; F = R gives x = 2aR/(1+a−R) exactly. Limits: R = 0 → φ = 0; R = 1 → x = 2, φ = π. |
| (6.7) | R_KO = 27.6 A E^1.67/(Z^0.89 ρ) nm | **verified** as the code's formula and as an empirical law whose constant carries the units (A in g mol⁻¹, ρ in g cm⁻³, E in keV; 27.6 nm = 0.0276 µm). The text's exponent argument checks out: integrating the Joy–Luo stopping power gives a local exponent d ln s/d ln E of 1.48 (0.8 keV), 1.63 (3 keV) and 1.79 (30 keV) in silicon, so the logarithm alone brings 2 down to about 1.67 in this range. The role of scattering in the exponent is a qualitative claim, not tested. Quotation from Goldstein et al. **unverifiable, because** not opened (the page says so). |
| inline | pv = E(E+2mc²)/(E+mc²) | **verified** (SymPy, from pc = √((E+mc²)² − (mc²)²), v/c = pc/(E+mc²)). |
| inline | s = −λ_el ln R₁; 10 % of paths longer than 2.3λ_el | **verified**: P(s > x) = e^−x/λ; e^−2.3 = 0.1003. |
| inline | u_η = √(η(1−η)/N) | **verified** (binomial standard error); 0.0096 for η = 0.2435, N = 2000. |
| inline | SE rate (1/ε)\|dE/ds\|, escape ½e^−z/λs | **verified** against Lin and Joy Eqs. 1–3 (opened): n = (1/ε)dE/ds, p(z) = K exp(−z/λ), K = 0.5 "assuming that SE are scattered symmetrically". Dimensionless product. Exact step integral s λ_s/Δz (e^−zA/λs − e^−zB/λs), limit s e^−zA/λs as Δz → 0 (SymPy). |
| inline | universal law δ/δ_max = 1.28 x^−0.67 (1 − exp(−1.614 x^1.67)) | **verified** as Lin and Joy's Eq. 12 (opened). Note its maximum value is 1.025, at x = 1. |
| inline | V_int = (2/3)π r90³ | **verified** (hemisphere). |
| inline | c′ = c cos φ + sin φ (ê₁ cos ψ + ê₂ sin ψ) | **verified** for the general branch of `turn`: ê₁ = (c_x c_z, c_y c_z, −(1−c_z²))/√(1−c_z²) and ê₂ = (−c_y, c_x, 0)/√(1−c_z²) are orthonormal and ⊥ c. **Wrong for the near-axis branch** (summary item 2). |
| Problem 1 | half the turns below 1 − cos φ = 2a, ≈ 2√a | **wrong as an exact statement, because** F(2a) = (1+a)/2 (51.2 % for Si at 0.8 keV); the exact median is 1 − cos φ = 2a/(1+2a). 2√a: 0.316 rad (18.1°) at 0.8 keV and 0.0515 rad (2.95°) at 30 keV; exact medians 0.309 and 0.0515 rad. |
| Problem 2 | ∫E dE/c = E²/(2c) | **verified** (SymPy). |

## Numbers (page value read from the DOM; recomputed with the page's own modules in Chromium)

All 44 spans match the recomputation, formatted with the page's `fmt`. The stored `mc_runs.json` agrees with a fresh Chromium run to
5×10⁻¹³ relative.

| key | page | recomputed (raw) | verdict |
|---|---|---|---|
| joy_const | 5.18 | 5.18374×10⁻²¹ keV² cm² | verified |
| mfp_Si_08 | 1.0 nm | 1.02166 | verified |
| mfp_Si_30 | 35 nm | 35.412 | verified |
| mfp_Si_100 | 105 nm | 105.195 | verified (exact 1022/5.18 constants give 105.35; still 105) |
| J_Si | 172 eV | 172.072 | verified |
| J_Au | 797 eV | 796.544 | verified |
| es_mid_lo | 0.93 | 0.92760 (Si 30 keV) | verified |
| es_mid_hi | 1.05 | 1.04825 | verified |
| es_lo_hi | 2.3 (gold at 1 keV) | 2.3102, Au at 1 keV | verified (ESTAR 12.24, Joy–Luo 28.28 MeV cm² g⁻¹) |
| es_100 | 0.78 | 0.78142 (max 0.78608) | verified |
| es_100_beta | 0.77 | 0.76789 | verified (β² = 0.3006, 2T/mc² = 0.3914) |
| eb_Si_lo_mc | 0.24 | 0.242625 | verified |
| eb_Si_lo_n | 5 | 5 | verified |
| eb_Si_lo_me | 0.24 | 0.2380 | verified |
| eb_Au_hi_mc | 0.56 | 0.56375 | verified |
| eb_Au_hi_me | 0.49 | 0.49381 | verified |
| eb_Au_lo_mc | 0.64 | 0.64475 | verified |
| eb_Au_lo_me | 0.34 | 0.3443 | verified |
| eb_Cu_lo_mc | 0.42 | 0.42125 | verified |
| eb_Cu_lo_me | 0.31 | 0.31441 | verified |
| d_delta (×2) | 0.76 | 0.761814 | verified |
| d_udelta (×2) | 0.01 | 0.009947 | verified |
| law_Si_08 | 0.76 | 0.763386 | verified |
| dc_Si_mc20 | 0.054 | 0.054048 | verified |
| dc_Si_lj20 | 0.080 | 0.08 (Table 1) | verified against the opened paper |
| dc_Au_mc20 | 0.18 | 0.175287 | verified |
| dc_Au_lj20 | 0.37 | 0.37 (Table 1) | verified against the opened paper |
| d_eta | 0.24 | 0.2435 | verified |
| d_ueta | 0.01 | 0.009597 | verified |
| au_eta (×2) | 0.65 | 0.6475 | verified |
| au_delta | 1.5 | 1.49290 (± 0.027) | verified (see remark: above gold's δ_max) |
| d_sum | 1.0 | 1.00531 | verified |
| d_R | 22 nm | 21.885 | verified |
| d_r90 | 14 nm | 14.419 | verified |
| d_sig | 3.9 nm | 3.9409 | verified; "same order as the probe of chapter 5": the ch05 default d_p = 5.32 nm (Chromium), right |
| k_Rum | 9.3 µm | 9.3062 | verified |
| k_r90um | 6.5 µm | 6.5472 | verified |
| k_sigum | 1.4 µm | 1.4138 | verified |
| vol_ratio | 9 × 10⁷ | 9.362×10⁷ | verified (from unrounded r90; (6.5 µm/14 nm)³ from the rounded values would give 1.0×10⁸) |
| sig_ratio | 360 | 358.74 | verified |
| au_R | 4.0 nm | 3.9680 | verified |

Literal numbers in the text:

| number | verdict |
|---|---|
| silicon nucleus "about 50 000" times m_e | verified: 28.0855 u/m_e = 51 197 |
| "one part in 10 000" of the energy per elastic hit | verified: largest fraction 4m/M = 7.8×10⁻⁵ (1 in 12 800) for Si; less for heavier nuclei |
| "a few hundredths" (a, Si, 800 eV) | verified: 0.0249 |
| "half a per cent" (5.21 against 5.18) | verified: 0.51 % |
| "within 3 %" (J against ESTAR) | verified: largest gap 2.5 % (Cu) |
| 0.795 (Si), 0.832 (Au), Joy et al. 1996 Table 2 | verified in the 1996 text (copy read; Table 2 "silicon 0.795 … gold 0.832") |
| 90 eV, 2.7 nm (Si); 35 eV, 0.5 nm (Au), Lin and Joy Table 1 | verified in the opened paper (also Al 32/1.7 and Cu 35/0.6 used by the code) |
| δ_max, E_max used for the law (Si 0.89, 0.45 keV; Au 1.28, 0.50 keV) | verified in Table 1 |
| "parity about 10⁻⁹" | verified as the repository check's figure (1.2×10⁻⁹); see remark: the readouts agree to 3×10⁻¹⁴ |
| "20 000 random cases" (M4) | verified (derive/ch06.py); see summary item 2 for what they miss |
| "2000 electrons", "40 paths", "three escape depths" (simulation caption) | verified against NEL, NPATH and the drawing (3·λ_s) |
| "not, in principle, suitable for incident beam energies below 1 keV"; "few hundred ångström" (M8) | unverifiable, because Joy 1991 could not be opened (roads in the header) |
| Si and Al "within the spread of the measurements at all energies" | verified within the statistical error. Per energy, the simulation lies inside the range of measurements within ×1.3 in energy, except Si at 0.5 keV (0.267 ± 0.010 against 0.241–0.255) and Al at 30 keV (0.164 ± 0.008 against 0.130–0.162), both within about 1.2 standard errors |
| "copper lies between" | verified: overstatement factor at low energy Si 1.02, Cu 1.34, Au 1.87 |

Figures and tables:
- Figure 6.1: 4 polylines, at most 0.09 px from the Chromium runs. 355 database circles.
- Figure 6.2: the law and MC polylines are at most 0.10 px from the recomputation; the squares are Lin and Joy's Table 1 values.
- ESTAR table: 12 rows, all equal to the recomputation.
- Simulation readouts at the default: η 0.243, δ 0.762, R 21.9 nm, r90 14.4 nm, σ_s 3.94 nm, equal to the module.
- Checks table, M1–M10: every detail value reproduced (M9 bands and M10 values from the Chromium runs; M6, M7 and M8 from the module
  functions).

## Numerical method: note against code (physics/ch06.js)

| note says | code | verdict |
|---|---|---|
| starts at the point of impact, heading straight in, energy E | x = y = z = 0, c = (0, 0, 1), E = E0 (l. 77) | verified |
| 1. free path s = −λ_el ln R₁ | `-lam * Math.log(1 - rnd())`, λ at the step's starting energy (l. 81–82) | verified: 1 − R₁ has the same distribution and avoids ln 0 |
| 2. move s, lose s\|dE/ds\| by (6.5) | dE = S·s with S at the starting energy (l. 99) | verified |
| cut at the surface; backscattered if E > 50 eV | zn < 0 → s = −z/c_z, exit (l. 84); `bs = E > EMIN` (l. 103) | verified. The energy cut comes after the surface cut and overrides it, so an electron that would reach the surface with E ≤ 50 eV counts as stopped, consistent with the note |
| cut where E reaches 50 eV, the electron stops | `S*s >= E − EMIN` → s = (E − EMIN)/S, dead (l. 86) | verified |
| 3. turn by (6.6), ψ = 2πR₃ | a at the energy after the step; R₂ then R₃ (l. 105–107) | verified |
| 4. rotation c′ = c cos φ + sin φ(ê₁ cos ψ + ê₂ sin ψ), "built from c without that division" | general branch: yes (l. 60–61); for \|c_z\| > 0.99999 a rotation about z (l. 58) | **wrong in the near-axis branch** (summary item 2). Effect on shown numbers: none |
| runs until it leaves or stops | yes, plus a guard of 200 000 steps (l. 80) | verified (guard not mentioned; never reached: the longest electron takes 2107 steps, Au at 30 kV; measured for all four materials at 0.5 and 30 kV) |
| 2000 electrons, mulberry32 seeded per electron | NEL = 2000; `core.rng(SEED + 7919 i)` (l. 29, 76) | verified |
| u_η = √(η(1−η)/N); u_δ from the spread of contributions | l. 114, 122 | verified |
| SE weights along every step, exact per straight piece, in and out | `escInt` per part; steps lying entirely deeper than 12 λ_s skipped (l. 89); a step is split into ≤ 200 parts of ≤ 0.5 λ_s for the lateral moment | verified. "Every step" omits the 12 λ_s cut (weight < e⁻¹² = 6×10⁻⁶ per unit path, negligible) |
| σ_s: rms of one lateral coordinate of the birth points of escaping SE, weighted by escape probability | √(Σ w x²/Σ w), w = generation × escape, x at the midpoint of each part, about the point of impact (l. 93–95, 122) | verified (the birth density ∝ \|dE/ds\| is in w, as "points where secondaries are born" implies) |
| r90: hemisphere holding 90 % of the energy left in the wafer | energy of each step put at its midpoint, 4000 bins up to 3R, linear interpolation in the crossing bin, overflow into the last bin (l. 99–100, 115–119) | verified. The midpoint placement and binning are in the module header, not in the note (detail). The 50 eV left by each stopped electron is not counted (negligible) |
| V_int = (2/3)π r90³ | l. 121 | verified |
| default 800 V on silicon | contract defaults V_land = 800, material Si | verified |
