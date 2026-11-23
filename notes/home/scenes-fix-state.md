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
- Branch `scenes-fix` from main f987b10.
- [ ] before: screenshots and 60 s films at 1920, 1600, 1100
- [ ] step 1 forest slower
- [ ] step 2 coupled pendulums: model tools/sims/coupled.py, registry entry, player; Kaggle run from the branch
- [ ] step 3 corners
- [ ] step 4 "what you see" notes, EN then DE/AR
- [ ] step 4b scenes page with controls
- [ ] step 5 test, show, wait
- [ ] step 6 publish, docs, clean up
