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
