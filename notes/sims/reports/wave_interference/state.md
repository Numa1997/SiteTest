# Fig. 1, Wave interference: state (23 November 2026, 20:35 UTC)

- Live: the page plays generation 1 (`wave_interference`, data commit 6be1fd7): λ in whole pixels, γ in steps of 0.05.
- Measured weakness of generation 1: between whole wavelengths the field is off by up to 0.65 (at λ = 30.5 px, 89 % of points a wrong
  colour); during the live λ sweep "Calm lines, one pair at a time", 51 % of frames showed an older λ (download lag), longest wait
  276 frames, 24 of 49 stored λ shown.
- Generation 2 (`tools/sims/wave_interference2.py`, PR 180) is computed on Kaggle and on `main` (data commit 17db10b): ring angles at
  118 k nodes (exact blend), heights at γ step 0.025, every table split into bottom/top halves.
- This branch (`kaggelize/wave_interference2-page`) switches the page to generation 2: code, walkthrough quotes (53 lines match) and the
  registry probe are done. Left: German and Arabic strings for the changed texts, note §8/§10 numbers from the Kaggle checks, the
  page's doc, PLAN row, inventory, then merge and live check (headless Chromium sweep: stale frames, field against the old page).
- Old work kept until generation 2 is verified live: generation 1 model, registry entry and data.

- 20:55 UTC: page switch complete on the branch (translations, docs, view fix: figure pinned on narrow portrait screens); merging, then the live check.
- 21:30 UTC: generation 2 verified live (verify_live passed; live sweep 2.8 % of 1 837 frames behind, longest 25 frames, 1 725 distinct λ; three proofs at the centre cell hold). Generation 1 removed (model, registry entry, data, generations entry).
