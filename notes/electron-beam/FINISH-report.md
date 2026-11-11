# Project 07, "The Electron Beam, from Tip to Measurement": finish report

Finisher session, 11 November 2026. Live: <https://phyeinusul.com/portfolios/electron-beam/index.html>
(backup: <https://numa1997.github.io/SiteTest/portfolios/electron-beam/index.html>). Full audit trail: `AUDIT.md` §0–§7.

## Facts (each with a way to check it)
- Ten chapters (0–9) and a reading guide are on `main` and live. Chapters 0–2 were built by sessions S1–S4 and audited here; chapters 3–9,
  the guide and the Projects entry were written in this session. Check: `git log --oneline -- portfolios-src/electron-beam`.
- Every simulation (chapters 1–8) is a JavaScript module with a Python twin, except chapter 8, which only chains the others.
  Checks that pass on the last build: `python3 portfolios-src/electron-beam/checks/check_parity.py`, `check_numbers.py`, `selftest.py`,
  `derive/ch04.py`…`derive/ch08.py`, and the page check `node portfolios-src/electron-beam/checks/check_page.cjs` at 360, 390, 1024 and 1440 px.
- Every chapter from 0 to 8 had two blind reviews (a referee reading as the target reader, a derivation checker recomputing every number). Reports are in
  `review/`; what each found and what was changed is in `AUDIT.md` §3, §5, §6, §7.
- Errors the reviews caught that I had made: a misread coefficient (0.66 for 0.54, Bronsgeest et al. Eq. 19); a lens solver that drew a nonsense focus;
  a 4.5 mrad error in the Monte Carlo's direction rotation; an Example 8.3 whose own numbers contradicted its claim. All fixed; see `AUDIT.md`.
- Applied Materials appears only in chapter 0, as cited public claims from its own pages (read 9 November 2026, recorded in `sources/applied-public.md`).
  No logo, no claim of affiliation, no claim to model its tools.
- Drive: no electron-optics or SEM book in the Leipzig, Oldenburg or Groningen folders (`AUDIT.md` §7).

## What the project shows
One chain from tip to measured number, each link derived, coded twice, and checked: field emission and the energy spread (ch. 1–2), brightness and
the source image (ch. 3), a magnetic lens solved from its field with its C_s and C_c (ch. 4), the probe size against current (ch. 5), a single-scattering
Monte Carlo of the beam in silicon, aluminium, copper and gold (ch. 6), a line-width measurement with shot noise and its error budget (ch. 7), and the
whole machine with sensitivities, a tolerance Monte Carlo and a process window (ch. 8).

## What it leaves out (stated on the pages)
Mott cross-sections (Rutherford is used; gold's backscattering trend is wrong for that reason), charging, contamination, detector physics beyond a
collection efficiency, electron-electron interactions in the column, 3D lens fields from real pole pieces, real tool data. The tolerance spreads in
chapter 8 are assumed, not measured.

## What could not be verified
- Hawkes and Kasper (C_s integral), Goldstein (Kanaya–Okayama range), Reimer, Barth and Kruit, Busch: cited from secondary sources, not opened; our
  numbers agree with the formulas as quoted, which is a check of the arithmetic, not of the quotation.
- Joy 1991's quotations: the derivation checker could not reach the paper; I read it in full earlier in this session.
- The two Workday job pages were not reopened in this session.

## Inferences
- The chain is internally consistent: the same numbers come out of the JavaScript, the Python twins and the stored runs, and the pages read them from the
  store. That proves the code does what the text says; it does not prove the models match a real column.
- The weakest link is chapter 6's signal widths (a fitted core and halo, plus the escape depth), and chapter 8's conclusions about voltage rest on them.

## Opinions
- The project fits card 225 (electron optics, multiphysics simulation) well and card 267 (particle-beam technology, control) reasonably: chapter 8's
  sensitivities and tolerance analysis are the part closest to control work.
- What would raise it most: one comparison with measured data (published SEM line profiles or backscatter yields), and Mott cross-sections for gold.
- Long sentences remain in chapters 1–4; shortening them is best done in Numa's own voice.

## Three sentences for the application
I built this project together with the AI assistant Claude, which wrote much of the code and the text under my direction.
The physics and the ideas are mine: the choice of models and the chain from tip to measurement.
Every number on the pages is computed twice, in JavaScript and Python, and each chapter was reviewed blind before publication.
