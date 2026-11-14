# Fig. 12 lecture note: the writer session's state

Written first, kept current, reread after any compaction (CLAUDE.md). Brief: `notes/fig12/handoff-note-writer.md` (everything after "---").

## Aim
Rewrite the lecture note of `public/simulations/guinness-kaggle.html` (the `<article class="paper" id="paper">`, source
`notes/fig12/note/paper.html`) so a BSc-physics reader reads it start to finish without one stop. Every number printed by
`tools/fig12/kaggle/note_numbers.py` from the stored runs (run 10 controlled rides, run 8 swing and speed-held rides) and filled
in by `tools/fig12/kaggle/build_note.py`. Referee rounds (owner + student) and the derivation-checker until no stops. Then switch
the page to run 10 (`DIR` in `public/scripts/guinness-jax-play.js`), `generations.json`, docs, build, Chromium test, fast-forward
`main`, verify live, write `notes/fig12/note/REPORT.md`.

## Rules (from the brief and CLAUDE.md)
- Branch `claude/fig12-note`. Never touch the solver, controllers, data, Kaggle, Cloudflare Workers. No other figures.
- No model names in code, commits or PRs. Do not message other sessions.
- Every number from the script; define every term and symbol at first use, one symbol one meaning; number equations;
  no forward references; no run history in running prose (one openable paragraph); kerb limit stated plainly.
- House style: Taylor-like chapter, Key result boxes, worked examples, Problems, ★ on heavy parts with results restated.
- Readers: `referee` agents given only "Fig. 12" + page path + output file; `derivation-checker` alongside. Marks and answers in
  `notes/fig12/readers/roundN-*.md`.
- Report to owner once at the end: plain short words, no tables, no option lists.

## What is live
- phyeinusul.com plays run 8 (`public/data/fig12/2026-11-13-run8/`) with the old note. Unchanged by this session so far.

## Progress
- [ ] STATE.md written and pushed
- [ ] Read round-0 reader files, existing note, scripts, solver constants
- [ ] Extend note_numbers.py (run 10, beta 1.241, design numbers via stout_jax)
- [ ] Rewrite paper.html
- [ ] Reader rounds
- [ ] Publish (DIR, generations.json, docs, inventory, build, Chromium, main, live)
- [ ] REPORT.md

## Commits on this branch (newest first)
- (start) 8109801 hand-off prompt
