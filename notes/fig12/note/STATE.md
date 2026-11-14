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

## Owner's word, 14 Nov 2026 (overrides the brief's 'repeat until no stops')
- "Don't loop too many times." Round 2 is the last reader round: fix its real errors and clear stops, then publish.

## What is live
- phyeinusul.com plays run 8 (`public/data/fig12/2026-11-13-run8/`) with the old note. Unchanged by this session so far.

## Progress
- [x] STATE.md written and pushed
- [x] Read round-0 reader files, existing note, scripts, solver constants
- [x] note_numbers.py rewritten: reads run 10 folder, decodes stored files, runs the cart alone (cached in
      notes/fig12/note/cart-alone.json), designs the controllers with stout_jax's own functions (beta_h 1.241: K equals the
      stored gains), draws Figures 1-6 as SVG. --check now runs on the SOURCE and lists hand-typed numbers (only labels left).
- [x] paper.html rewritten (14 sections, eqs. 1-52, Figures 1-6, Tables 1-8, 12 Problems); built, KaTeX 0 errors at 1440/390 px
      (test script /tmp/claude-0/test.cjs; parts drafted in /tmp/claude-0/p*.html, now merged).
- Symbols changed for one-symbol-one-meaning: x_e (schedule error), F_a (active force), k_s,c_s (spring), d_t (tyre compression),
  z_s (stroke), lambda_h=m_s/rho, mu_g (grip), X (Riccati), f (noise), d (distance from wall), Ca_f/Ca_w, j imaginary unit.
- Run 3 story and its numbers dropped (data not stored); one-mode Table 7 dropped (code not stored); other Fig. 12 page no longer cited.
- [x] Round 1: owner 70, student 95, checker 13 wrong; all answered in notes/fig12/readers/round1-answers.md, fixed
- [ ] Round 2 (fresh readers) running
- [x] Prepared: DIR -> 2026-11-14-run10, generations.json entry, readings note 'eight', hero line (commit da9260a)
- [ ] Publish (DIR, generations.json, docs, inventory, build, Chromium, main, live)
- [ ] REPORT.md

## Commits on this branch (newest first)
- (next) round-1 fixes
- 0e6dd63 state file
- (start) 8109801 hand-off prompt
