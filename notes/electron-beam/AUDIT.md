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

## 3. Blind reviews of chapters 0 to 2

(filled in when the referee and derivation-checker reports are in: `notes/electron-beam/review/`)
