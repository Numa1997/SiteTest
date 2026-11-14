# Fig. 12 lecture note: report (14 November 2026)

## What was done
- **The note** of `public/simulations/guinness-kaggle.html` was rewritten from scratch on run 10's data: 14 sections,
  52 numbered equations, 6 figures, 8 tables, 12 Problems, 18 sources in order of first citation. Source:
  `notes/fig12/note/paper.html`.
- **Every number is printed by a script.** `tools/fig12/kaggle/note_numbers.py` prints them from the stored files (decoded as the
  page decodes them), the run summaries, the glass table and the solver itself (imported: `Geometry`, `road_table`, `Cart` driven
  alone over each road, `slosh_lqr`, `susp_lqr`, `observer_design`). It also draws all six figures as SVG from the same data.
  `--check` lists numbers typed by hand in the source; only labels (section numbers, the scale bar) remain.
  `build_note.py` fills the source into the page.
- **The controllers' design numbers were recomputed with β_h = 1.241.** The gains the code gives equal those stored with run 10.
- **New physics, compared with the old note:**
  - Newton's law in the glass's frame, derived.
  - Why APIC keeps a linear flow that plain PIC smears.
  - The foam's edge friction turned into a predicted damping ratio: 0.47 against 0.425 computed.
  - The head's mass changing both the frequency and the drive coefficient, derived together.
  - The skyhook.
  - The kerb limit stated plainly: up to 82 N from the road against at most 11.25 N from the motor at 1.5 m/s.
  - Assumptions named: surface tension left out (Bond number 101), small swings (kq ≈ 0.6 in the rides), no pitch.
- **Dropped:**
  - Run 3's story and numbers (data not stored).
  - The one-mode prediction table (its code was not stored).
  - Citing the other Fig. 12 page as a source.
  - Run history in the prose: it now sits in one openable box.

## The readers
- **Round 1:**
  - Owner reader: 70 marks.
  - Student reader: 95 marks.
  - Derivation checker: 13 wrong, 8 unverifiable.
  - Main errors found:
    - the motor's force at speed (11.25 N, not 15 N);
    - the kerb's touch point (x = 1.437 m, so the sudden loss is 0.28 m/s and the wall rises 11.1 mm);
    - one claim about the 25 mm bump;
    - rounding;
    - equation order;
    - about a dozen symbols with two meanings.
  - All fixed. Each answer is in `notes/fig12/readers/round1-answers.md`.
- **Round 2 (fresh readers), the last by the owner's word of 14 November ("don't loop too many times"):**
  - Owner reader: 68 marks.
  - Student reader: 89 marks.
  - Derivation checker: 196 of 213 rows verified, 6 wrong, 11 unverifiable.
  - Errors found:
    - a garbled sentence;
    - the kerb surge numbers;
    - the sign of the pseudo-force on the foam;
    - a factor of 2 in the plain-PIC estimate;
    - where the controllers' plant came from;
    - two method details.
  - All fixed, plus the assumptions above. Answers are in `round2-answers.md`.
  - Not pursued:
    - three extra figures the student reader asked for;
    - some index letters reused across passages.

## Publishing
- **Page:** the player points at `public/data/fig12/2026-11-14-run10/`, with an entry in `generations.json`. Two small page-text
  fixes: "All eight readings", and "the in-browser version of Fig. 12".
- **Docs:** `docs/simulations/fig12-beer-slosh.md` and `docs/kaggle-pipeline.md` updated; `docs/files.md` regenerated.
- **Merge:** another session had already switched the page to run 10 on `main` (d6fc137). Merged: kept this note, took its
  generation entry. `main` fast-forwarded to 16d9b23.
- **Tests, built page in headless Chromium at 1440 and 390 px:**
  - 0 KaTeX errors in 1636 formulas;
  - no sideways scroll;
  - no console errors;
  - the ride table filled.
- **Live check (phyeinusul.com, Chromium):**
  - the new note is served;
  - the page fetches `2026-11-14-run10/index-jax.json` and the default ride, both answering 200;
  - the readings run;
  - the table shows 13.6 and 13.9 mm with the speed held and 1.0 mm with joint control, as the note says;
  - 0 KaTeX errors.
  - The only console error is Cloudflare's own analytics beacon, blocked by the site's security policy; it is not from this page.
