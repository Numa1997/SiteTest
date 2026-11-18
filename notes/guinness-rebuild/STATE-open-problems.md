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
   Page built on Kaggle v11 committed; LIVE on main da39ef8 (curl: id="stage", dataset.js, data.css served; script has defineData).
   BUG found by v13 screenshot: overlay grew the grid (ResizeObserver loop, "This simulation stopped", giant figure). Fixed by a CSS
   rule in the page (d795e8a), live. v14 PROOF, FAIL 0: 3 rides x 1440 and 390 px, checks 19/19, read-backs 15/15, book OK, no banner,
   no console errors; Read values off: overlay 0 px, strip hidden; on: pinned the cart, words changed 2 times in 3 s, strip below figure.
   Screenshots (not committed) sent to the owner. docs/files.md from v14 committed. PROBLEM 2 DONE.
3. Fig. 16 dataset — DONE 18 Nov ~14:12 UTC: numakoudsie/fig16-guinness-cart-control (private, CC BY 4.0), READY, 25 files
   (23 outputs of GPU v2/v8/v9 + README + manifest), all 23 sizes equal the manifest. Made via api.kaggle.com StartBlobUpload + PUT +
   CreateDataset (connector has no create). Records in notes/inventory/datasets/fig16-guinness-cart-control/; docs updated.
   docs/files.md lags by these 3 record files: regenerate in the next Kaggle CPU run.
4. 3D close-up frame times — CLOSED AS NOT MEASURABLE ON KAGGLE (owner said go; GPU v16, 3.3 GPU-min): headless Chromium got only
   software WebGL (SwiftShader, llvmpipe), never the T4. Close-up own cost 5-7 ms JS + 1-2 ms render call per picture; 2D drawing
   dominates. Report notes/guinness-rebuild/frames/; docs updated; speed handed to the look session (it owns the drawing).
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

## Joint integration (18 Nov ~17:00 UTC)
- Look session relayed the owner: "Resolve the split ... Complete both works. Merge them into a functioning animation already."
- Agreed: one integration branch claude/guinness-realism; main gets one merge of both works after panel16_check and frames_check pass
  on it. It merged main 6aa30fc; its 9a6e8ef adds deck_px_* into this.deckStore (cart16-view.js) and a physically based pint3d-view.js.
- Mine to merge into it: dbef006 (run_b task free_wall_1.0). After panel16_check passes there: update fig16 docs (deck pixels recorded).
- Problem 5 GPU run waits for the owner's yes to ~20 T4-min (0.33 GPU-h, 40-min hard limit); not overlapping its GPU work.
- 18 Nov ~18:10 UTC: the look session's panel16 v1 on its branch hung >2 h (its software-WebGL 3D scene blocks the page). Fix pushed to
  claude/guinness-realism as 6ec7f73 (my files): guinness16-play.js ?no3d=1 skips the 3D close-ups; panel16_check loads with no3d=1 and
  has a 25-min limit. Its edit to guinness16-play.js (setCart/setPose for close.b) reviewed: fine. My CPU v18 runs panel16_check on the
  joint branch (30-min limit). Merge to main = one merge of claude/guinness-realism after it passes.
