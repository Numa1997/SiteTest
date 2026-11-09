# Chapter 3 "Acceleration, brightness, energy spread": independent check of equations, numbers and method

Page checked: `public/portfolios/electron-beam/index.html`, element `#ch03` (built 9 Nov 2026 20:42; its rendered text matches `text/ch03.py`).
Inputs read: `text/ch03.py`, `physics/ch03.js`, `ref/ch03.py`, `derive/ch03.py`, `data/ch03/derive_results.json`, `physics/ch02.js` (how `B_r` and `dE` are made),
`ref/ch02.py`, `contract.json`, `data/ch02/source_properties_williams_carter.csv`, `sources/bibliography.md` (Bronsgeest entry).

How the check was done:

- **Equations.** Each of the 8 numbered equations and the 3 unnumbered displays was re-derived in SymPy 1.14 (my own script, not `derive/ch03.py`):
  energy conservation from γmc² + qφ, p² from E² = (pc)² + (mc²)², the two limits of λ, the series of λ_NR/λ, the non-paraxial angle ratio,
  the Liouville divergence in the full 4-D transverse phase space with A_x, A_y and A_z, the Jacobian d²p⊥ = p² cosθ dΩ, the Gaussian FW50 integral,
  the truncated Gaussian and the top-hat of Problem 3, and the cone solid angle.
- **Numbers.** All 60 entries of `NUMS` were recomputed in headless Chromium (Playwright) from the built page's own modules, `window.EB.ch03.compute` and
  `window.EB.ch02.compute` with `EB.core.withDefaults`, formatted with `EB.core.fmt`, and compared with `#ch03.innerText`. Every value shown on the page is
  reproduced digit for digit. Independently, the wavelengths and V* were recomputed in mpmath (30 digits) from CODATA 2018, and the two chapter 2 presets
  from `ref/ch02.py` (NumPy): the agreement is within 2×10⁻¹⁴ relative. `check_parity.py`: ch03 JS against Python, largest difference 2.9×10⁻¹⁶.
- **Method.** `physics/ch03.js` against `ref/ch03.py` and the text, line by line. The simulation was drawn in Chromium at the page's own size and,
  through the module's `draw`, at 1000 × 437 px (wide layout) for 5 kV → 800 V, 1 kV → 1 kV and 1 kV → 30 kV.
- **Source.** Bronsgeest et al. 2008 could not be opened. `repository.tudelft.nl` reset the connection (curl, three tries) and answered 503
  (Playwright request client). The TU Delft resolver answered 503, `pubs.aip.org` 403, `avs.scitation.org` returned a 93-byte HTML stub, the Wayback
  copy (web.archive.org, snapshot 2023-11-09) reset the connection, and CORE answered with a browser challenge. OpenAlex and Semantic Scholar list only
  these copies. What the note attributes to the paper is therefore marked unverifiable. The project's `sources/bibliography.md` (the librarian read it
  in full) agrees with Eqs. 5, 6, 15–16 and the 3×10⁸ limit, but that is a secondary record.

Scripts (scratchpad): `work/sym3.py`, `js/run3.cjs` (numbers), `js/shot3.cjs`, `js/wide3.cjs` (drawings).

## 1. Numbered equations

| eq. | statement | verdict | units / limiting case checked |
|---|---|---|---|
| 3.1 | E₀ = (γ−1)mc² = eV, γ = 1 + eV/mc² | verified: γmc² − eφ conserved, φ: 0 → V and γ = 1 at the start give γ = 1 + eV/mc². (γmv)² = p² of 3.2 also checked | J. V → 0 gives γ → 1 |
| — (unnumbered) | (pc)² = (mc² + eV)² − (mc²)² = (eV)² + 2eVmc² | verified | J² |
| 3.2 | p² = 2meV(1 + eV/2mc²) ≡ 2meV*, V* = V(1 + eV/2mc²) | verified (p² − 2meV* = 0) | kg² m² s⁻²; V* in V; V* → V for eV ≪ mc² |
| 3.3 | λ = h/p = h/√(2meV*) | verified. Limits: λ√V → h/√(2me) (V → 0); λV → hc/e (V → ∞) | m |
| 3.4 | α_land/α = p_acc/p_land = √(V*_acc/V*_land) | verified for small angles. With p_z = √(p² − p⊥²) exactly, the ratio is p_a/p_l + (p⊥²/6)(p_a/p_l³ − 1/(p_a p_l)) + O(p⊥⁴), so the paraxial form is first order, as the text says. This relies on p⊥ being conserved, which holds only without the radial fringe field (the text states this model limit) | dimensionless; equal voltages give 1 |
| 3.5 | B = dI/(dA dΩ) | verified (definition) | A m⁻² sr⁻¹ |
| — (unnumbered) | H(x, p_x; z) = −p_z = −√(P(x,z)² − (p_x − qA_x)²) | verified as the one-dimensional form: dx/dz = ∂H/∂p_x = (p_x − qA_x)/p_z. The general Hamiltonian is −√(P² − (p_x−qA_x)² − (p_y−qA_y)²) − qA_z. The −qA_z term is dropped; it is zero for electrostatic fields and for round magnetic lenses in the azimuthal gauge, and it does not change the conclusion | kg m s⁻¹ |
| — (unnumbered) | ∂ₓ∂H/∂p_x − ∂_{p_x}∂H/∂x = 0 | verified in full 4-D (x, y, p_x, p_y) with arbitrary P, A_x, A_y and A_z: the divergence simplifies to 0 | — |
| 3.6 | B_r = B/V* conserved | verified: dA d²p⊥ is invariant (Liouville), and d²p⊥ = p² cosθ dΩ (SymPy Jacobian), so B/p² is invariant to O(θ²); p² = 2meV* | A m⁻² sr⁻¹ V⁻¹ |
| 3.7 | I_p = B_pr V* (πd²/4) πα² | verified in form and units: 2π(1 − cos α) = πα² − πα⁴/12. Units A m⁻² sr⁻¹ V⁻¹ · V · m² · sr = A. Attribution to Bronsgeest Eq. 6 unverifiable (paper not reachable). Per the project's bibliography, the paper writes V_p, not V*: a 0.08 % difference at 800 V | A |
| 3.8 | B_pr = B_r/ln 2 = 1.4427 B_r | verified: I_tot = πσ²J₀, I(R) = πσ²J₀(1 − e^{−R²/σ²}), R₅₀² = σ² ln 2, I_tot/(πR₅₀²) = J₀/ln 2. 1/ln 2 = 1.442695 | same units as B_r |

## 2. Numbers (headless Chromium, page modules)

All values below appear on the page exactly as listed. "Value" is the unrounded result in the display unit.

| number (key) | page shows | value recomputed | verdict |
|---|---|---|---|
| mc² (mc2_keV) | 510.999 keV | 510.99895 | verified |
| cold ΔE, §3.1 and §3.6 (cold_dE) | 0.215 eV | 0.2147259 | verified (ch02 module; ref/ch02.py the same) |
| 1 % threshold (V_1pct_kV) | 20.5 kV | 20.5422 (exact: eV/mc² = 201/5000) | verified |
| V* at 1 kV (vs_1k) | 1000.98 V | 1000.9785 | verified |
| λ at 1 kV (lam_1k) | 38.76 pm | 38.764034 (mpmath 38.764034) | verified |
| NR error at 1 kV (nrerr_1k) | 0.049 % | 0.04891 | verified |
| V (v_30k) | 30000 V | — | verified (given) |
| V*/V at 30 kV (vs_ratio_30k) | 1.02935 | 1.0293543 | verified |
| γ at 30 kV (g_30k) | 1.05871 | 1.0587085 | verified |
| λ at 30 kV (lam_30k) | 6.979 pm | 6.9790816 | verified |
| NR error at 30 kV (nrerr_30k) | 1.5 % | 1.4571 | verified |
| λ at 100 kV (lam_100k) | 3.701 pm | 3.7014366 | verified |
| NR error at 100 kV (nrerr_100k) | 4.8 % | 4.7782 | verified |
| V (v_300k) | 3.00 × 10⁵ V | — | verified (given) |
| λ at 300 kV (lam_300k) | 1.969 pm | 1.9687489 | verified |
| hc/eV at 300 kV (lam_ur_300k) | 4.13 pm | 4.1328 | verified |
| α ratio 5 kV → 800 V (dec_mag) | 2.51 | 2.50513 | verified |
| λ at 5 kV (dec_lam_col) | 17.3 pm | 17.30201 | verified |
| λ at 800 V (dec_lam_land) | 43.3 pm | 43.34374 | verified |
| default 1 kV → 800 V (def_mag) | 1.118 | 1.118143 | verified (contract defaults V_acc = 1000, V_land = 800) |
| 1/ln 2 (ln2inv) | 1.4427 | 1.4426950 | verified |
| cold B_r (cold_Bd) | 2.17 × 10⁸ A m⁻² sr⁻¹ V⁻¹ | 2.170237×10⁸ | verified (ch02 defaults with t_clean = 0: r_t = 50 nm, V_ex = 1 kV, k_f = 5, so F = 4 V/nm as stated) |
| cold B_pr (cold_Bp) | 3.13 × 10⁸ | 3.130990×10⁸ | verified (unit missing on the page, see W5) |
| V* at 800 V (vs_land_def) | 800.63 V | 800.62622 | verified |
| I_p cold (Ip_pA) | 15 pA | 15.4629 (hand check: 3.131e8 · 800.63 · 7.854e−19 · 7.854e−5 = 1.546e−11 A) | verified |
| electrons per µs (electrons_per_us) | 97 | 96.512 | verified |
| I_p Schottky (Ip_sch_pA) | 1.2 pA | 1.19059 | verified |
| cold/Schottky B_pr (cold_over_sch) | 13 | 12.988 | verified |
| Schottky ΔE (sch_dE) | 0.43 eV | 0.425096 | verified (preset r_t = 0.5 µm, V_ex = 2 kV, k_f = 8, T = 1800 K, φ = 2.9 eV) |
| ΔE/eV at 1 kV (rel_spread_1k) | 2.1×10⁻⁴ | 2.1473 | verified |
| ΔE/eV at 800 V (rel_spread_land) | 2.7×10⁻⁴ | 2.6841 | verified |
| V* at 100 kV (vs_100k) | 1.09785 × 10⁵ V | 109784.756 | verified |
| correction over V (nrc_pct_100k) | 9.8 % | 9.7848 | verified |
| table: model B_pr cold / Schottky | 3.13 × 10⁸ / 2.41 × 10⁷ | 3.13099×10⁸ / 2.41074×10⁷ | verified |
| table: W&C B/V* cold / Schottky | 9.11 × 10⁷ / 4.55 × 10⁷ | 9.10873×10⁷ / 4.55437×10⁷ | verified (from 1×10¹³ and 5×10¹² A m⁻² sr⁻¹ at 100 kV, as in `data/ch02/...williams_carter.csv`) |
| table: model/book (ratio_cold, ratio_sch) | 3.4 / 0.53 | 3.4374 / 0.52933 | verified |
| table: model ΔE / book ΔE | 0.215, 0.43 / 0.300, 0.700 | 0.21473, 0.42510 / literals | verified (book values unverifiable against the book itself, see S3) |
| Schottky B_pr / 3×10⁸ (sch_vs_limit) | 0.080 | 0.080358 | verified |
| Problem 1 constant (lam_const) | 1226.4 | 1226.426 (mpmath 1226.426) | verified |
| Problem 2 (not stated on the page) | — | factor 5.516, so 1 mrad → 5.5 mrad | (for the editor) |
| 61 plotted voltages, 10 V to 1 MV | — | code: i = 0…60, V = 10^(1+5i/60) | verified |
| parity tolerance 10⁻¹⁴ | — | `tolerance.rel = 1e-14`; measured 2.9×10⁻¹⁶ | verified |

## 3. Statements around the equations (wording and physics)

| where | statement | verdict |
|---|---|---|
| W1, Example 3.1 | "at 300 kV the electron is half-way between the two limits" | **wrong, because** the exact λ is not between the two limiting values: it is below both. λ/λ_NR = √(2mc²/(eV+2mc²)) < 1 and λ/λ_UR = √(eV/(eV+2mc²)) < 1 for every V. At 300 kV: exact 1.969 pm, school formula 2.239 pm (+13.7 %), photon form 4.133 pm (+110 %). Nor is it half-way in energy: (eV)²/(2eVmc²) = eV/2mc² = 0.29. Correct form, for example: "at 300 kV neither limit will do: the school formula is 14 % too long and the photon formula twice too long; the exact λ is shorter than both, because p² = 2meV + (eV/c)² exceeds each term". |
| W2, §3.7 | "both gaps lie within the factor of two the table itself carries" | **wrong, because** the cold-source gap is a factor 3.4 (model 3.13×10⁸ against book 9.11×10⁷), outside a factor of two. Only the Schottky gap (1/0.53 = 1.9) lies within it. Correct form: "the Schottky gap (a factor 1.9) lies within the factor of two the table carries; the cold-source model is 3.4 times the book value, which is what one expects of a clean-surface model with no Coulomb interactions (see below)". |
| W3, simulation caption (and `physics/ch03.js` ui.caption) | "the beam narrowing to the anode and opening again if it is slowed before the wafer" | **wrong, because** `draw` draws a cone that *widens* from the tip apex (half-width 0) to half-width 0.6·a₁ at the anode. From the anode to the wafer it widens to 0.6·a₂, with a₂ = min(0.36·gw, a₁·ang_mag). Without deceleration (ang_mag = 1) the beam is drawn *parallel* after the anode, so the drawn angle falls to zero rather than staying the same. With deceleration the drawn angle grows, but not by ang_mag: the end widths, not the angles, scale with it. Checked by drawing at 1000 × 437 px for 5 kV → 800 V and 1 kV → 1 kV. Correct caption, for example: "Left: the gun drawn (schematic): the beam spreads from the tip to the anode and spreads further after it when it is slowed before the wafer; its width at the wafer grows with α_land/α." Alternatively, change `draw` so that the post-anode half-angle is ang_mag times the pre-anode one. |
| W4, lead paragraph | "Liouville\\'s theorem" | **wrong (typo), because** the lead is a raw string `r'…Liouville\'s…'`, so the page shows a literal backslash: "Liouville\'s theorem". Correct: "Liouville's theorem" (write the lead with double quotes, or without `r`). |
| W5, Example 3.3 and §3.7 | "B_pr = 3.13 × 10⁸" and "a practical brightness of about 3×10⁸" | **incomplete, because** no unit is given. Correct: append A m⁻² sr⁻¹ V⁻¹ to both. |
| W6, §3.8 | "Every number in this chapter's text is produced by one of them, or by chapter 2's module, and checked against the other" | **overstated, because** several numbers come from neither module. mc², h/√(2me) and 1/ln 2 are computed in `text/ch03.py` from CODATA. The Williams & Carter values and 3×10⁸ are quoted literals (listed in `LITERALS`/`const`). Correct form: "Every computed number … is produced by one of them, by chapter 2's module, or from CODATA constants; quoted values are marked as such." |
| W7, §3.2 | "every non-relativistic formula of electron optics in which V stands for p²/(2me) becomes exact when V is replaced by V*" | verified, with the qualifier as written: it holds for formulas in which V enters only through p (λ, rigidity, brightness, the angle ratio). It does not hold for the paraxial ray equation, where the field V′ and V″ appear with factors of γ. The qualifier "in which V stands for p²/(2me)" covers this, but a reader may miss it. |
| W8, §3.1 and Fig. 3.1 | "Measured from the Fermi level, every electron then gains exactly eV"; figure label "tip: U = 0 (Fermi level)" | verified as an idealisation: the kinetic energy in the column is eV plus the electron's energy relative to the tip's Fermi level, if the potential V is the vacuum potential difference. With V the applied (Fermi-level) voltage, contact potentials shift it by a few eV (≈0.5 % at 1 kV). The sketch also leaves out the tunnelling barrier. Both are covered by "on the scale of what follows" and "not to scale". |
| W9, §3.3 | wafer "held at a potential V_acc − V_land below the column" | verified |
| W10, §3.4 | dΩ = d²p⊥/p², "So dA dΩ p² is conserved" | verified to first order: the exact relation is d²p⊥ = p² cosθ dΩ (SymPy Jacobian), so the invariant with B = dI/(dA dΩ) is paraxial. Check D6's title "(exactly, relativistically)" means exact in V*, not in angle. |
| W11, Example 3.1 | "A low-voltage scanning microscope … can use the school formula to a fraction of a per cent" | verified: 0.049 % at 1 kV, 0.24 % at 5 kV, 0.49 % at 10 kV |
| W12, Example 3.3 | "half the spot diameter at the same angle means a quarter of the current" | verified (I_p ∝ d², eq. 3.7) |
| W13, §3.7 | "The energy spreads of the model are smaller than the book's, by about a third for both" | verified, loosely: 28 % smaller for the cold source (0.215 against 0.3 eV) and 39 % for Schottky (0.425 against 0.7 eV) |
| W14, §3.7 | "The brightness agrees in order of magnitude for both sources, the model being higher for the cold source and lower for the Schottky preset" | verified (3.4 and 0.53) |
| W15, §3.7 | "The cold source at 3.13 × 10⁸ would sit above that mark" | verified, but only by 4 % (3.13 against 3.0×10⁸), and the mark is quoted for Schottky sources. Applying it to a cold emitter is the author's extrapolation, and the text should say so. |
| W16, §3.5 | "B_r = e j(ε_t=0)/π, which for the exponential distribution … equals eJ/(π⟨ε_t⟩)" | verified: `physics/ch02.js` computes B_r = e·jt0/π with jt0 the numerical j at ε_t = 0, and for j ∝ e^{−ε_t/d} the identity holds. An exponential ε_t distribution gives a Gaussian in p⊥, hence a Gaussian virtual source, which is what 3.8 needs. |
| W17, §3.5 | "It holds as long as the electrons do not push each other between the tip and the extractor" | verified as a necessary condition. It also needs the transverse-energy distribution to be exponential (Maxwellian in p⊥); for chapter 2's numerically computed j(ε_t) that is approximately, not exactly, the case. |
| W18, Problem 3 | top-hat practical brightness → 2 × axial as R → 0 | verified mathematically: a top-hat gives exactly 2. A Gaussian cut at R_c gives a ratio → 2 as R_c → 0 and → 1/ln 2 as R_c → ∞. 2 is an upper bound for any profile with J ≤ J₀, since I/2 ≤ J₀πR₅₀². "Which is the upper limit Bronsgeest et al. quote": unverifiable (paper not reachable; the project's bibliography entry does not record it). |
| W19, Example 3.3 | "Chapter 7 shows that a few thousand electrons per pixel are needed for a clean edge" | unverifiable, because chapter 7 does not exist yet (`text/ch07.py` absent) |
| W20, §3.1 | "an extractor a fraction of a millimetre away" | unverifiable from the code (no extractor distance in the model; chapter 2 uses F = V_ex/(k_f r_t)) |
| W21, §3.7 | Williams & Carter values "good to a factor of about two" | unverifiable, because it is the author's judgement; the book gives no uncertainty |

## 4. Quoted sources

| quotation | verdict |
|---|---|
| S1 Bronsgeest et al. 2008 define the practical brightness as total angular current density over the area of the FW50 disk; Eq. 6 for I_p | unverifiable, because the paper could not be fetched (roads tried listed above). Consistent with `sources/bibliography.md`, which records Eq. 5 B = 4I′/(π d_v² V) and Eq. 6 I_p = πα_p² V_p (π/4) d_I² B. Note the paper's V_p against the note's V* (eq. 3.7 row). |
| S2 "1.44 ej/(π⟨ε_t⟩) (their Eqs. 15 and 16)" and the phrase "a surprising, new result" | unverifiable, for the same reason. The bibliography records B = 1.44 e j/(π kT) and 1.44 e j/(π d) for Eqs. 15–16, consistent with the note's ⟨ε_t⟩ = kT or d. The quoted phrase is not recorded there and could not be checked. |
| S3 Williams & Carter, ch. 5, Table 5.1: B = 10¹³ (cold), 5×10¹² (Schottky) A m⁻² sr⁻¹ at 100 kV; ΔE = 0.3, 0.7 eV | unverifiable against the book (not open access). The values match the project's digitised CSV and my recollection of the 2nd-edition table. |
| S4 Coulomb interactions important for Schottky above B_pr ≈ 3×10⁸ (Bronsgeest, citing van Veen et al. 2001) | unverifiable (paper not reachable). The bibliography records it with unit A m⁻² sr⁻¹ V⁻¹. |

## 5. Numerical method against the code

| text | code | verdict |
|---|---|---|
| "physics/ch03.js and ref/ch03.py evaluate the same closed formulas" | `vstar`, `lam`, `lamNR`/`lam_nr`, `compute` match line by line: E₀ = eV, γ = 1 + eV/mc², V*, λ, V*_land, λ_land, ang_mag = √(V*/V*_land), the curve of 61 points | verified |
| "agree to the last bits of a 64-bit number (tolerance 10⁻¹⁴)" | `tolerance.rel = 1e-14`; check_parity: 2.9×10⁻¹⁶ on 4 cases × 8 outputs | verified |
| Plot: "exact (wine) and without relativity (grey, dashed)" | `line(2, '#8b8079', [5,4])` is λ_NR, `line(1, '#7a1f2b', [])` is λ; log axes 10 V–1 MV, 400 pm–0.8 pm, both curves inside | verified |
| "with the column and landing values marked" | `dot(p.V_acc, out.lambda_e, 'column'); dot(p.V_land, out.lambda_land, 'landing')` | verified. At the default (1 kV, 800 V) and whenever V_acc ≈ V_land the two labels print on top of each other ("laodlng" in the screenshot). |
| Caption: beam "narrowing to the anode and opening again" | see W3 | **wrong** (W3) |
| Layout | at a 1440 px window the canvas is 406 × 178 CSS px, so `draw` takes the narrow branch (w < 560): the gun is squeezed into 75 px, and "extractor" is written across the tip | observation, not an equation error |
| derive/ch03.py D6 | sets dA d²p⊥ = K at both planes by construction, so B₁/p₁² − B₂/p₂² = 0 is a tautology; the physics is in D5 and the d²p⊥ = p² dΩ step, which no check covers | the check passes trivially. The table's claim "B/V* is the same at every plane" rests on D5 and the paraxial dΩ, not on D6. |
| derive/ch03.py D8 | the comment says "units and form", but only the cone's solid-angle series is checked | the units were checked here instead (eq. 3.7 row) |
| derive/ch03.py D9 | (E_a + eV) − (E_b + eV) = E_a − E_b | trivial; correct |

## 6. Summary of errors

1. Example 3.1: "at 300 kV the electron is half-way between the two limits" is wrong. The exact λ = 1.969 pm is shorter than both limits (2.239 pm and 4.133 pm).
2. §3.7: "both gaps lie within the factor of two" is wrong. The cold source is off by 3.4×; only the Schottky source (1.9×) lies within two.
3. Simulation caption: "narrowing to the anode and opening again" is wrong. The drawn beam widens from the tip to the anode, runs parallel after it without deceleration, and its drawn angle does not scale by α_land/α.
4. Lead: a literal backslash shows on the page in "Liouville\'s".
5. Units missing on B_pr = 3.13×10⁸ and on the 3×10⁸ limit.
6. §3.8 overstates that every number comes from a module (constants and literals do not).

All eight numbered equations are correct, with correct units and limits. Every module-computed number on the page is reproduced exactly. The Bronsgeest quotations (Eq. 6, Eqs. 15–16, "a surprising, new result", the upper limit 2, the 3×10⁸ limit) are unverifiable here because the paper could not be reached.
