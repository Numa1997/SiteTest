# Project 07 · audit by the finisher (branch `eb/finisher`)

Marks: **Fact** (with a handle: file:line, commit, or a command to rerun), **Inference** (my reasoning), **Opinion** (my judgment).
Started 9 November 2026. Each round adds a section.

## 0. How the branches came together

- **Fact.** `eb/finisher` = `ccr-cc3b1649-gefitf` + `eb/scaffold` (841bea3) + `eb/librarian` (82fdd4f) + `eb/ch02` (a1a0dc7) + `eb/ch01` (13b193d) + `origin/main`.
  Conflicts: `tools/inventory.py` (both rule blocks kept, librarian's first), `data/ch02/README.md` (both kept), `notes/electron-beam/requests.md` (both kept), `docs/files.md` (regenerated).
- **Fact.** `eb/ch01` (S3) did not exist at my fetches at the start; it appeared later (commit 13b193d, 20:09 UTC). By then I had drafted my own
  `physics/ch01.js`, `ref/ch01.py` and `derive/ch01.py`. I set my drafts aside (not committed) and took S3's files, because S3 owned them (PLAN.md §7)
  and its version comes with the chapter text, which mine did not.
- **Fact (comparison).** Both solvers integrate the same equation, `du/dt = (q/m)(E + u×B/γ)`, with Boris and RK4. The trap I had hit in my draft (reading
  the Boris energy from the average of two half-step velocities, which shrinks |u| by cos(Ωh/2) and shows a false drift of 1.4×10⁻³) is avoided in S3's code:
  it synchronises with a half step, `u = borisKick(uh, E, B, h/2)` (`physics/ch01.js`, after the loop), and computes γ−1 without cancellation.
  My draft also had a total-energy diagnostic (kinetic + qφ) for E ≠ 0; S3's `energy_drift` is the kinetic change, and its contract meaning says so. Nothing in my
  draft is better in a way that matters, so nothing of it was kept.

## 1. Infrastructure the finisher changed

- **Fact.** Chapter 2 was written before the scaffold (own `build()` returning numbered HTML, CSS and a figure script). `eb_lib.py` now accepts such a
  "legacy" chapter: it strips the outer article, renames `sec-x` ids to `ch02-x`, typesets `\( \)` and `\[ \]` with the site's KaTeX, and adds the CSS and
  script. New optional chapter keys `css`, `ui_js`, `sim_html` for custom panels (README "How a chapter plugs in").
- **Fact.** `physics/ch02.js` and `ref/ch02.py` gained the contract interface (`compute(p)` with `r_t, V_ex, phi, T, p, t_clean, k_f` →
  `I_e, B_r, dE, d_v, theta_cov`), using the chapter's stated assumptions (H₂ at 300 K, κs = 0.535, N_s = 10¹⁹ m⁻², E_d = 1.9 eV, Δφ_ads = 1.0 eV) and
  its patch model. Parity: worst relative gap 3.4×10⁻¹¹ (`python3 portfolios-src/electron-beam/checks/check_parity.py`).
- **Fact.** Contract defaults of stage ch02 were 100 nm, 4 kV, 4.55 eV: an apex field of 8 V/nm and a current of 3.9 mA, far from any working
  cold emitter. Now 50 nm, 1 kV, k = 5, 4.5 eV (chapter 2's cold preset): 4 V/nm, I_e = 70 nA, B_r = 1.6×10⁸ A m⁻² sr⁻¹ V⁻¹, ΔE = 0.214 eV, d_v = 1.3 nm.
- **Fact.** The template now links `styles/sim.css` (which imports the fonts, KaTeX CSS and paper.css), because chapter 2's figure uses the site's
  `.stage`, `.panel`, `.btn`, `.switch` classes. Chapter 2's live figure was restacked: in the 760 px text column its three plots were 245 px wide and
  unreadable (screenshot looked at, 1440 px).
- **Fact.** `checks/check_page.cjs` counted SVG paths clipped inside a figure as "wide elements"; it now ignores elements inside `svg`.
- **Fact.** `checks/check_numbers.py` crashed on chapter 2 (no `sections`). It now skips the legacy chapter with the reason, and
  `checks/list_legacy_numerals.py` lists its 140 typed numerals.
- **Fact.** S3's contract request applied by hand (`t_run`, `x_end`, `y_end`, `z_end`, `theta_end`); the patch file no longer applied because of the ch02 default change.

## 2. Chapters 0 to 2: what I checked and fixed

- **Fact.** `derive/ch01.py`: all checks pass; `derive/ch02.py`: 19 of 19. `check_parity.py`: ch00, ch01, ch02 PASS. `check_numbers.py`: 425 numbers, browser =
  Python; PASS. `selftest.py`: PASS. `check_page.cjs`: PASS at 360, 390, 1024, 1440 px, 1050 formulas, 0 KaTeX errors, 0 page errors, no sideways scroll, no request
  outside the site.
- **Fact, fixed.** Contract `d_opt` said "smallest half-pitch … λ/(2NA)". Abbe's λ/(2NA) is the smallest *period*; the half-pitch is half of it. S3 had flagged
  this and its chapter 0 text is already right. Reworded in `contract.json` and in the comment of `physics/ch00.js`. `ratio_opt` compares that period with a line
  width, so the threshold is 2 for equal lines and spaces, not 1: reworded.
- **Fact, fixed.** Chapter 2 typed "a 4 % correction" (temperature factor): computed now, 3.7 %. It said hydrogen-like adsorbates leave a hot tip "in about a second
  near 700 K"; with its own assumed E_d = 1.9 eV and ν₀ = 10¹³ s⁻¹ the residence time there is 4.8 s. Now computed and printed ("within seconds … 1/k_d = 4.8 s").
- **Fact, checked, stays.** "the current falls by 10 % in a few hours" at 10⁻⁹ Pa: the chapter's model gives 5.1 h. The other typed numerals in chapter 2 are
  section numbers, citation data, preset inputs and values quoted from named sources (`checks/list_legacy_numerals.py`).
- **Fact, fixed.** Chapter 1's live canvas: at its real width (406 px) the two view titles overprinted. Shortened and clipped to their own view (drawing only).
- **Inference.** Chapter 2's B_r is the brightness of the emitting patch (from the transverse-energy distribution), not of an operating gun; the chapter says so in §2.8
  and defers comparison with published B_r to chapter 3. Chapter 3 must keep that promise.
- **Fact.** Chapter 2's Dyke & Trolan (1953) data could not be read (APS 403); the chapter uses Ayari et al. 2023 (CC BY 4.0) instead and says so.
  The librarian's Li et al. 2025 nanotip set is CC BY-NC-ND; it stays in the repository and is not shown on the page.

## 3. Blind reviews of chapters 0 to 2, and what was done

Four blind reviews (repo agents `referee` and `derivation-checker`, given only the page path and chapter): `notes/electron-beam/review/`.
Every claim below was checked by me before it was acted on; the fix commit is 85c847d unless said otherwise.

### The worst finding: chapter 1 printed "−200 %"
- **Fact.** The page said "The gap of −200 % is not a numerical error", "within 200.0 % of the solver" and "The method returns it to 200 %".
  Cause: `physics/ch01.js` takes `E_field` as the y component of E and `B_field` as the z component of B; §1.3 of the text puts
  E = (0, −E, 0) and B = (0, 0, −B_p); `text/ch01.py` passed +E and +B_p, so every computed spot and angle had the wrong sign and Figures 1.1 and
  1.2 bent the wrong way. Fixed by passing −E and −B_p (commit c8a8de9). The page now reads 0.39 % and 0.62 %, which is S3's own reported result.
- **Inference.** S3's report says "e/m to 0.62 %"; the merged branch printed −200 %. Either S3 tested a different contract or the sign changed
  late in its session. Whichever, the published number would have been wrong; this is exactly the failure a blind referee is for.

### Chapter 1, other errors confirmed and fixed
- Deflection error of a ½mv² calculation: the text used 1/v² (8.9 % at 30 kV); a deflection goes as 1/(pv), giving 2.8 % and 0.19 %.
- The 1 % speed criterion was solved for v/v_NR = 0.99 instead of 1/1.01: 6830 V, not 6900 V.
- RK4 "energy, predicted" column was the loss of u², not of kinetic energy; with the factor (γ+1)/(2γ) it now equals the measured column in every row.
- R(iθ) printed where R(−iθ) is meant.
- "Thomson gives no cause" for his second method: false. His paper, after Table II: the coils' field outside the plates is reversed, "the effective
  value of H will be smaller … so that the values of m/e are larger" (read in Giunta's transcription). Now quoted.
- Promises of a "field solver in chapter 4" removed: the project has none, and the guide says so.
- Three "checks" were italic questions with answers (STANDARD forbids Q&A): now statements.
- A raw "eq:loop" label, "uniform over a region long compared with the offset" (backwards), N printed as 16.0, Boris noise 1e−16 → 1e−15,
  "loses half its energy" (it is half of u⊥²), "RK4 prediction within a few per cent" (it is about ten at N = 16), Qin et al. stated as proving more than volume preservation,
  Figure 1.5 "mean of each row" (each group), the Giunta source as a link.
- Open (minor, named here, not fixed): symbols reused across sections (L, φ, θ, T, R, I, a, Ω, α); m9 (signed vs unsigned Ω), m11 (the e/m decomposition is an identity
  because the run stops at l/v₀), m13 (one SymPy check is a tautology).

### Chapter 0
- "For electrons the diffraction limit … is not what stops us": wrong for a low-kV probe. At α of a few mrad the diffraction blur λ/α is a few nanometres
  at 1 kV, comparable with the lines. Rewritten; chapter 5 balances it.
- p (pitch and momentum) separated in the one paragraph where both appear; the simulation caption says period, not half-pitch.

### Chapter 2, errors confirmed and fixed
- Example 2.4 printed the exact v (0.6538) and e^−10.66 but quoted J₀ = 1.13×10⁸ A/m², which is the value with Forbes' v (0.6560). Recomputed both
  (1.165×10⁸ and 1.125×10⁸); the example now uses Forbes' v throughout and says why.
- The text said the code uses D = e^−G; it uses D = 1/(1+e^G) with a linear continuation of G above the barrier top. Stated.
- "48 Gauss–Legendre points": true only for G at one energy; 64 for v(f), 24 in the energy integral. Stated.
- The f ≈ 0.8 breakdown was explained by fly-over; at f = 0.8 the top is still 0.475 eV above E_F. Corrected.
- "Exact within the model" for the FN formula: it is first order in w and evaluated with Forbes' v and t. Corrected.
- Triangular d is 0.184 eV; 0.175 eV is with t(f). Both now printed with their meaning. Peak condition: exists for d > kT, below E_F for d > 2kT.
- "ln J varies as F^17": J varies as F^17.5. The brightness paragraph credited the small area; brightness is J over transverse energy, the small area makes the virtual source small.
- "Covered in a fraction of a second at 10⁻⁴ Pa": the chapter's own table says about 1 s (H₂) and 3.5 s (CO).
- ν₀ rendered as "u₀" (a raw newline in the source). A_R printed as 1.20173e+06. "Example 2.2" → 2.3. The radius "130 nm" was typed and disagreed with the computed 131.5 nm.
- The figure's apex is on a log scale of the slider, not to scale; the FN sweep has 13 voltages; the dashed line is a least-squares fit; the rose curve is θ = 1.
- Cho 2014: the chapter now says that the patch model reproduces the 1/p scaling of τ₉₀, not the flat-then-fall shape of his curve.
- References to PLAN.md and the S4 preview harness removed from the page; the B_r readout has its unit.
- Open (named, not fixed): symbol reuse (k for the field factor and in kT; d; κ; a; b; f; s; t; ρ); the cap integral F(ϑ) = F₀cos ϑ is used before it is introduced;
  no separate "numerical method" passage (STANDARD item 5); the 2.9 fit frees both ζ and the area, and the cosine-cap model would predict a larger area at the fitted radius
  (referee's estimate ×4), not discussed; the flash of 1000 K is adequate only for the single assumed E_d; Applied's press release is quoted from PLAN.md, not re-opened by S4.
  **Opinion.** None of these is a wrong number on the page; they are teaching and completeness gaps. I list them rather than rewrite a chapter of 8 700 words.

### Layout
- Upper-case readout labels turned KaTeX symbols into capitals (λ → Λ): fixed in the template. Readouts were cut with an ellipsis: they wrap now.
- Long display equations scroll inside their box; the scrollbar is now visible. At 360 and 390 px no element runs past the screen (checked in Chromium).

## 4. Chapters 3 to 5: built by the finisher, and how each is checked
- **Chapter 3** (acceleration, brightness, energy spread): `physics/ch03.js` closed formulas; no Python twin needed (PLAN.md §4) but one exists and agrees to 3×10⁻¹⁶.
  `derive/ch03.py` D1–D9 (momentum, limits of λ, deceleration, Liouville with z as time, B/V* invariance, 1/ln 2 for a Gaussian source, solid angle, ΔE unchanged).
- **Chapter 4** (the lens): RK4 paraxial ray in τ with z = a tan τ, bisection for the excitation that focuses on the wafer, C_s from rays traced through the third-order
  field, C_c by a central difference. `derive/ch04.py` L1–L8 (SymPy) and N1–N5 (numerics): Glaser's focal length to 1.4×10⁻⁷ (the finite start of the ray),
  C_c and C_s each against its perturbation integral (C_s 4.18897 mm both ways), rotation, α³ scaling.
- **Chapter 5** (the spot): closed formulas and a golden-section search. `derive/ch05.py` P1–P10, including first-principles checks of the FW50 coefficients
  (Airy 0.535 λ/α, spherical 0.177 C_sα³) and Joy's worked example.
- Run: `python3 derive/ch0N.py`, `python3 checks/check_parity.py`, `python3 checks/check_numbers.py`, `node checks/check_page.cjs` (all pass, 9 November 2026).

## 5. Blind reviews of chapters 4 and 5, and what was done
Reports: `review/referee-ch04.md`, `review/derivations-ch04.md`, `review/referee-ch05.md`, `review/derivations-ch05.md`. Every number on both pages matched
the reviewers' independent recomputation; the problems were in physics, wording and one coefficient.

### The worst finding: a coefficient I misread (chapter 5)
**Fact.** Bronsgeest et al. (2008) print Eq. 19 as d_A = 0.66×10⁻⁹/(α√V_p), metres and volts. I had read it as 0.66 λ/α. With λ√V = 1.226 nm·V^½ it is
0.538 λ/α; the Airy disc holds half its current inside 0.535 λ/α (computed, check P7); 0.66 λ/α holds 64 %. Re-read in full on 9 November 2026 (TU Delft copy, via Exa).
**Consequences fixed.** Every FW50 size and optimum angle in chapter 5 moved by about 10–20 % (default spot 6.48 → 5.32 nm at 5 mrad; optimum 5.27 nm at 8.13 mrad →
4.11 nm at 8.67 mrad). The "disagreement inside Bronsgeest et al." that the page reported (their I_AI against their Eqs. 6 and 19, "a factor close to 1/ln 2") was my
misreading, not theirs: with 0.54 their Eqs. reproduce 1.07×10⁻¹⁸ B against the quoted 1.08×10⁻¹⁸ B (check P6). The paragraph is gone.

### Chapter 5, other findings confirmed and fixed
- The chromatic term used the FWHM where the paper uses the FW50 of the energy distribution. Chapter 2 now exports `dE50` (both twins, interpolated as the
  derivation checker asked: 0.157 eV for the cold source, 0.267 eV for the Schottky preset); chapter 5 uses it in the FW50 convention and the FWHM in the classic one.
- Check P1's printed coefficients were typed by hand and wrong (1.0 and 0.93); now computed: 1.09 (λ/C_s)^¼ and 1.29 λ^¾ C_s^¼.
- Check P7 (energy FW50) took the next grid point up; now the module's interpolated value, checked against a 16× resampling.
- "Condensers demagnify the source more": wrong for this source. 10 pA at 5 mrad needs a total magnification of 0.63 from the 1.30 nm virtual source; the objective
  alone (0.018) would give 8.3 fA. Stated on the page.
- "A thousand times the current costs a factor of a few": it is 1.5; the source image becomes the largest part only above 1.8 nA. "At low voltage the lens, not the
  source, sets the spot" rewritten. The default optimum is named as the diffraction–chromatic balance (the P2 case).
- Problem 3's premise (similar chromatic weight) was false; the Schottky preset's values are now printed. Problem 2 no longer contradicts itself.
- §5.4: our lens is larger in C_s than all but one published value (not "inside the range"); Joy's 0.61 λ/α is a radius used beside a diameter; his formulas are
  smallest at 2.60 mrad (12.9 nm), and the page no longer guesses why he took 5 mrad. A manufacturer's resolution claim (Hitachi SU9600, 0.4 nm at 30 kV) is quoted as such.
- λ, V*, B_r defined in the chapter; a physical reason for λ/α and for the chromatic miss; the derivative step to α⁸ = A²/(3B²); radius and diameter of the
  spherical blur kept apart; the root-power sum explained as far as the paper allows ("the powers are simply those that give a good approximation"), split into two
  displays so it no longer overflows.
- Simulation: the plot now spans 0.1–100 mrad (the slider is inside it), the legend sits below the plot, tick labels no longer collide, readouts for d_A, d_S, d_C,
  d_I, the menu label is plain words, ΔE₅₀ and ΔE are separate sliders, the caption warns about Coulomb interactions above about 1 nA.
- Limits added: gun and condenser aberrations at large current, fifth-order aberration, retarding-field overlap, Coulomb interactions. A sources paragraph with links.
- Parity: at 100 V the two optimum searches part at 2×10⁻⁹; the stated tolerance is now 10⁻⁸ and the case is in the test set.
- Not verified: the chromatic coefficient 0.6 is taken from the paper (the derivation checker reproduced 0.601; I did not rerun that); Joy 2006 could not be re-opened
  (J-STAGE 502), so his quotes rest on the earlier excerpt.

### Chapter 4, findings confirmed and fixed
- **The simulation failed silently**: at settings where no single-crossing excitation focuses on the wafer (6.8 % of slider settings, per the referee) it showed a
  nonsense lens. The solver now stops with a plain message (both twins); checked at a = 20 mm, WD = 0.5 mm, u = 10 mm.
- **f is not the focal length that sets the image here**: the wafer at 1.5a sits in 31 % of the peak field (21 mT). The page now says f describes the asymptotes
  and that the solver focuses the real ray for that reason.
- **Ampère**: "real lenses lose some of NI in the iron" mixed B and H. A loop closed in vacuum gives ∫B dz = μ₀NI exactly; the iron shapes B(z), saturation near 2 T
  limits the peak. Rewritten.
- **Skew rays**: the derivation covered only rays from the axis while the Key result claimed all rays. Added the complex-coordinate derivation w = u e^{iθ} for every
  paraxial ray, verified in SymPy (check L8); the reversed "linearity" sentence replaced by the g, h argument for point-to-point imaging.
- Glaser's substitution now includes y = r sin ψ; k² and ω restated where Example 4.1 uses them; the angle is ψ (φ is the potential), the integration variable τ.
- The C_c proof now shows the second ray, the constant Wronskian and the integration limits; the B⁴ term is attributed to the motion, not only the field.
- Example 4.3: diffraction (0.61λ/α = 5.3 nm) is larger than the chromatic miss at 5 mrad; said so. Example 4.2: iron saturates near 2 T, not 1 T; this lens needs 0.43 T at 30 kV.
- The V_land slider: the lens is computed at the landing voltage (no retarding field); the caption and the hand-over say so. The hand-over no longer claims M is passed on.
- Busch cited (record found, text not read); Hawkes and Kasper cited as not opened, with our numerical agreement as the check. Lead backslashes, the raw heading
  "C_s and C_c" and raw SymPy output in the checks table fixed. Figure 4.1 redrawn: gap in the bore wall, field lines, electron path, labels readable at 360 px.

## 6. Chapters 6 and 7: built by the finisher, blind reviews, and what was done
**Chapter 6** (Monte Carlo after Joy 1991, Lin and Joy 2005; both read in full; Joy et al. 1996 Table 2 read). Checks M1–M12; stored runs through Node.
Every number reproduced in the derivation check. Fixed after the reviews:
- **Code**: the near-axis branch of the direction rotation turned about z instead of about the direction, off by up to 4.5 mrad (fired 49 times per run at
  30 kV). Replaced by one exact construction; the check now covers directions along and near each axis (error 3×10⁻¹⁶). All Monte Carlo numbers moved slightly.
- Example 6.2 (silicon at 800 V) read as if gold's δ + η were 1; now: silicon's δ + η = 1.00, so 800 V is the model's crossover for silicon; gold's 2.2.
- The "many losses per free path" premise fails at the default (21.6 eV per elastic path, about one free-electron plasmon, 16.6 eV): stated.
- Built-in agreement named (screening fitted to backscattering, ε and λ_s fitted to yields); Sommerfeld parameter Zα/β (1.8 Si, 10.3 Au); gold's mean free path
  (0.09 nm) below the atomic spacing (0.26 nm); gold's trend wrong (measured η rises, ours falls), with Joy's own sentence on the Mott cross-section.
- δ compared both ways with the universal law (now written out, Eq. 6.x) and with Lin and Joy's Monte Carlo; "must lie" removed.
- Derivations added: Rutherford from the orbit (check M2), the integral and the inversion behind Eq. 6, 78 500 = 2π(e²/4πε₀)²N_A and 1.166 = √(e/2)
  (check M8), 1024 against 2mc² = 1022 keV stated. Random numbers renamed ξ (R is the range). Problem 1 uses the exact median 2a/(1+2a).
- A section on scanning (deflection angle eB ℓ/p, field of view, a field below the Earth's) — the chapter title promised it.
- Checks that only compare are marked "recorded", not "pass". u_η and u_δ are readouts. Figures' labels larger.
- Not verified by the derivation checker (its access was refused): Joy 1991's quotations. I read that paper in full myself earlier this session (Exa fetch).

**Chapter 7** (line profile, shot noise, threshold rule, error propagation and Monte Carlo, throughput). Checks C1–C8. Every number reproduced. Fixed:
- Problem 2 asked to explain a dependence on t_ov that does not exist; rewritten (at fixed σ_CD, t_d N is fixed; time N·t_dN + t_ov).
- Problem 1's premise ("more than √2") false at the default (interpolation averages two pixels); rewritten to ask for both effects.
- The Key result claimed four times the dose when the lines are quadrupled; dose does not depend on the number of lines. And the law holds at fixed pixel size. Fixed.
- Monte Carlo agreement claimed too broadly: at the blunt probe (Example 7.4) the Monte Carlo is 11 % below; now stated, the repeats raised from 1000 to 4000,
  the cause of the usual few-per-cent excess named (the noisy peak jumps between flat top pixels), and the module stops below 5 % edge contrast.
- Neighbouring periods: the code added two per side; now 2 + ceil(5σ_b/p), and a zero-height line stops with its own message.
- Symbols: counts are k (N is lines), floor level S_floor, wall ends x₁, x₂. The model's values (δ, η, σ_s, σ_b, λ_s, aspect ratio, blur/space) are stated.
- "Collects 3200 electrons" was beam electrons landing; corrected. Biases explained (sidewall projection and blur), the fin's 64 % stated.
- Labels: the I_p slider no longer claims chapter 5 sets the probe from it; the caption says probe size and current are independent here and coupled in chapter 8.
- Limits: grazing incidence, the edge effect, shadowing, materials, detector noise. Sources paragraph. Applied's page: re-read 9 November 2026, recorded in
  `sources/applied-public.md` (the reviewers could not reach it: 403 to curl).

## 7. Chapter 8, the core-width change, chapter 9, the reading guide, the Drive, the last pass
**Chapter 8** (the whole chain; sensitivities, tolerance Monte Carlo, process window). Checks W1–W6. Both blind reviews
(`review/referee-ch08.md`, `review/derivations-ch08.md`) found the same serious fault:
- Example 8.3 said higher landing voltage helps; its own numbers (0.37 nm at 0.5 kV against 0.45 nm at 1.4 kV, 1 pA) said the reverse, and the map
  jumped by factors 2 to 3 between grid points above 2 kV. The cause was in chapter 6: the fitted core width of the secondary signal fell to 1.6 pm above
  10 kV, smaller than an atom. **Fix in chapter 6**: the secondaries' own sideways travel (escape depth λ_s) is added in quadrature to the core width, so the
  core cannot fall below about λ_s. The map is now smooth, and the example now says what the map shows: at a given current, low voltage is better.
- Tip changes now move the current (nominal = the default tip); the aperture is held fixed in the tolerance Monte Carlo (it was re-optimised per draw);
  checks W2 and W4 widened to the core and halo widths and to B_r, ΔE₅₀, d_v; W6 added (the V^−3/4 law). 2 of 300 tolerance draws fall outside the grid;
  stated on the page.
- No Python twin for chapter 8 (it only chains the other modules, each of which has one); stated as a limit.

**Chapter 9** (what the project shows, its limits, what was checked) and the **reading guide** (what each chapter shows, models, leaves out, its numbers):
prose only, no new numbers; every number they quote is pulled from the chapter stores by `{{num:chNN.name}}`.

**Drive (Numa's Leipzig, Oldenburg and Groningen folders), 11 November 2026.** Searched by full text (electron microscope, electron optics,
Elektronenoptik, Rutherford, Bethe, field emission, Busch) and by title (Reimer, Hawkes, Goldstein, Kruit, Optik/optics, Scanning, Monte Carlo).
No electron-optics or SEM book is there. What is there and could back textbook steps: Landau and Lifshitz vol. 2 and Demtröder's *Atoms, Molecules
and Photons* (Rutherford scattering), Nolting's electrodynamics, Sólyom vol. 2 (electrons in solids). None was opened; the second-hand citations
(Hawkes and Kasper's C_s integral, Kanaya–Okayama via Goldstein, Barth and Kruit, Reimer, Busch) stay marked as such on the pages. The personal
documents in the Groningen folder were not opened.

**Last readability pass.** No question-and-answer format anywhere (0 headings or paragraphs ending in "?"). Every abbreviation is spelled out at
first use in reading order; the one exception found (CD-SEM in chapter 5, before chapter 7 defines CD) is fixed. Long sentences (over 40 words) remain:
about one in seven in chapters 1–4, fewer later; left for Numa's own edit, since shortening them is a matter of his voice.
