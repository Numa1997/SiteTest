# Home page scenes fix: state of the session (23 November 2026)

Read this first after a compaction. The task is in `scenes-fix-handoff.md` beside this file (the user's handoff, Parts 1 to 3),
plus one step the user added on 23 November 2026, 22:03: **a page that shows every background scene on its own, each with its
controls and parameters to play with** (planned in `notes/sims/PLAN.md` line 24, never built).

## Rules of the user for this work
- Refer to the user as "the user". Commits in the name and e-mail of the last human commit on main (Numa Koudsie
  <numakoudsie@gmail.com>), no Claude attribution anywhere.
- Every run of a model happens on Kaggle, never locally; Kaggle runs need no fresh yes; monitor each run.
- Measure, never guess: headless Chromium at 1920, 1600, 1100 (and 390 for the final test).
- Another session may edit tools/sims/registry.json, docs/kaggle-sims.md, notes/sims/PLAN.md, tools/inventory.py, docs/files.md:
  fetch and rebase before merging, keep their lines, regenerate docs/files.md.
- No personal connectors, no scheduled tasks. Clean up scratch files and branches; never delete old work before the new is verified.
- Step 5: show before/after screenshots and films and WAIT for the user's yes before publishing.

## Decisions
- Pendulums: (b) two or three pendulums coupled by a weak spring (beats), not a Newton's cradle: a steel collision lasts under a
  millisecond, so at 30 frames/s the hand-over falls between frames; the beat moves the swing from bob to bob over seconds.

## Branch and progress
- Branch `scenes-fix` from main f987b10, pushed. Kaggle notebook numakoudsie/phyein-usul-simulations versions 7 and 8 = preview runs
  of coupled.py from the branch (commits f946601, 8c1bc4f); outputs not committed; the official run happens when the model lands on main.
- [x] before: notes/home/scenes/before (PNG not committed; counts.json committed)
- [x] step 1 forest slower (YEAR 120, GROW 50, SEED .04, FEED .25, START 3)
- [x] step 2 coupled pendulums: tools/sims/coupled.py, registry entry (barton keeps its model, no page), rails player
- [x] step 3 corners: clouds in the open sky (clouds(), band(), join(), puffs())
- [x] step 4 home note details.bgs-note, DE + AR
- [x] step 4b scenes.html, 12 scenes, knob tables K, scenes roots and pairs; English only
- [x] step 5 tests clean (check.cjs); screenshots shown to the user; WAITING for the yes
- [ ] step 6 merge (fetch, rebase, inventory), watch "Simulations on Kaggle" for coupled, verify live; delete branch and scratch
  (PNG folders); barton.py and its data stay until coupled is verified live, then ask the user.
- Known, not ours: `tools/i18n/build.py --check` fails on "{n} shown here" (fold.js), already on main.
