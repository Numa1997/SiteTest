# Fig. 15 generation-2 lecture note: working state

Branch `claude/fig15-gen2-note` (from `claude/fig15-resonant-tunnelling`). Never merge to main, never open a PR: the Fig. 15
session merges this branch into its own and publishes. A chat that lost its context rereads this file first.

## Aim
Extend the generation-1 note (two walls, discs, shells, 115 runs) so it teaches the whole generation-2 parameter space the page
walks: spacing P, height V0 and thickness D, N = 3, 5, 10 barriers (bands), discs R 2-12 and shells R 3, 5, the diode under bias
(Fig. 15e from the stored bias runs, Tsu-Esaki, E_F = 1.0, kT = 0.05), long packets. Keep what is still true.

## Files I own (nothing else)
- `public/scripts/resonant-note.js` (fills `<article id="paper">`)
- in `public/simulations/resonant-tunnelling.html`: the lead paragraph and `<meta name="description">` only
- `notes/fig15/gen2_numbers.py` (reads the index, prints every number the note quotes with its run file)
- `docs/simulations/fig15-resonant-tunnelling.md` (sections about the note only)
- this file

## Rules
- Every number quoted is read from stored data via gen2_numbers.py; each number in one easy place in the note.
- Cases not yet in the index (shards 3-6): sentences true either way; refresh when the full index lands (~08:30 UTC 14 Nov,
  `git fetch origin claude/fig15-resonant-tunnelling`).
- LaTeX-like lecture note, everyday picture -> model -> maths; numbered equations and figures; no Q&A; short sentences.
- Never write the site owner's name or e-mail anywhere.
- After drafting: derivation-checker, referee, walkthrough-keeper (if a walk key exists); fix; npm run build; headless Chromium
  check (KaTeX renders, no page errors), screenshots 390 and 1440 px.
- Commit messages end with Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Done
- (14 Nov 01:30) branch created, this file.
- gen2_numbers.py: prints every number with its source; `--write` fills the NUM and FIG2 blocks of resonant-note.js.
  Exact parts from tm.py/iv.py (finite-well levels, widths, band edges via xi = Re(e^{-ikP}/t), T_N formula check 2e-12).
- Note drafted (commit 9bbf6f7): 14 sections, eqs (1)-(27), Figures 1-3; byline without the owner's name (task rule).
- Page lead + meta description rewritten for gen 2.
- Built; headless Chromium at 1440/390: 589 KaTeX, 0 errors, eqs (1)-(27), no page errors, no overflow. Figure 3 labels fixed.
  Screenshots in scratchpad/shots (open folds first: the 'Expand all' button).
- No walkthrough key for this page (no data-walk attribute): walkthrough-keeper not needed.

## Left
3. derivation-checker (running; report -> notes/fig15/derivation-check-gen2.md), then referee; fix; docs section.
4. Refresh numbers with the full index.
5. Write "READY at <commit>".
