# Open problems of the Guinness rebuild (Fig. 12, Fig. 16): this session's state

Session: session_01DGmqipAnEdVvBLCf7CLGmT, started 18 November 2026. Branch: `claude/guinness-open-problems` (from main 81e6fe2).
Reread this file first after any compaction. Brief: `notes/guinness-rebuild/HANDOFF-open-problems.md` (read whole).

## Aim
Close the six open problems of the handoff, one at a time, in its order. Merge finished work to main; verify live with curl.

## Binding rules (owner)
- Nothing runs in this container: no python, node, npm, browsers, agents. Read, edit, git, curl downloads, Kaggle tools only.
  Every computation, build, check or browser test runs in a Kaggle notebook on the owner's account; download outputs and commit them.
- CPU work on Kaggle: no need to ask. A new GPU run: state it to the owner in one line with its cost first.
- Never touch the Workers, R2, public/de/, public/ar/, scripts/i18n/, *.rtl.css. No model names in commits. Never write the owner's name.
- Reports: short turns, metric units, Fact (with handle) / Inference / Opinion, mechanism in one line,
  end with "Where we are:" and "Next, if you say yes:".

## Problems (status)
1. inventory --check and docs/files.md — DONE, merged (main 56b5241).
2. Fig. 16 data panel — BUILT (commit a8b8dcc, owner said "Go for it" to option 1 + the message): store and ledger in
   guinness16-play.js; page src gets data.css, dataset.js, id="stage"; proof tools/fig16/kaggle/panel16_check.py; docs updated.
   Deck pixels: asked the look session to record them in this.deckStore (NOT ds) in cart16-view.js; until then "not recorded".
   PROVED on CPU v11 (1440 px, rides kerb_full t=0.62, kerb_off 0.40, resonant_full 2.0): checks 19/19, read-backs 15/15, head book OK;
   deck pixels "not recorded" (look session). Pointer test: v11 out of memory in the test, v12 shell quoting error, v13 slow.
   Page built on Kaggle v11 committed and merged to main.
3. Fig. 16's own Kaggle dataset — open.
4. 3D close-up smoothness on a Kaggle GPU machine — open.
5. Fig. 12 bare swing at 1.0 mm — optional; GPU (~10 min): ask the owner first.
6. Fig. 12 lecture note to STANDARD.md — only if the owner wants it.

## Kaggle runs of this session
- CPU `numakoudsie/fig-16-cart-diagnostics-cpu` version 9 (18 Nov): git clone of this branch, `inventory.py --check`, then regenerate;
  outputs inventory.log, files.md. Status: COMPLETE; files.md downloaded, diff reviewed (2 new notes files, 3 sizes, counts), committed.
- CPU same notebook version 10 (18 Nov): clone branch, node --check, panel16_check.py, inventory. Outputs: run.log, panel16.log,
  panel16-report.json, 4 screenshots, guinness-cart-control.html, files.md.

## Commits
- this file; docs/files.md from CPU v9 (state-file size line set by hand with the script's rule, bytes/1000 to 0.1 kB).
- Info (04:20 UTC, session_01DGmqin2AFu75ELh8fAbGr9): session_01DGmqioyaYR5VnnZaKfpEhD works on the look of Figs. 12 and 16 (stout-view*.js,
  guinness-glass.js, cart16-view.js, pint3d-view.js); it will propose a file split. Do not edit those files before agreeing it.
- File split agreed (04:23 UTC, with the owner's yes per that session): look session edits stout-view.js, stout-view2.js, guinness-glass.js,
  cart16-view.js, drawing parts of pint3d-view.js. Mine: Fig. 16 panel, page HTML and src, frame-time work, Kaggle dataset, inventory.
  Message them before touching any of theirs.
