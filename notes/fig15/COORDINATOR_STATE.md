# Fig. 15: state of the coordinating chat (18 November 2026)

Session: session_01DGmqinbgPZhEHKndFyAjfV, branch `ccr-50505ef7-n3t4yu`. Reread this file first after a compaction.

## Aim
File the corrected Fig. 15 data that already existed on Kaggle (1,088 walls, 2,327 discs, 282 shells) and make it live, with
no new computation. Keep the other chats in order.

## The owner's rules
- Reuse before computing: keep what passes, exact answers, exact reductions, correction by difference, GPU last.
- Fact / Inference / Opinion with a handle. Another chat's claim is never Fact.
- Nothing runs in the coordinator's container: runs happen on Kaggle or on the live site. (The R2 relay ran here by the
  owner's choice, because the R2 token exists only in this environment.)
- No GPU, no R2 write, no change to `main` without a yes that names it. Never write the owner's name.

## What is live (Fact, checked on the live site in headless Chromium, 1440 x 1000)
- `main` d6db0aa5: the page plays generation 2026-11-18 by default; the 2,782 replaced files of 2026-11-14 are deleted from R2 (6.18 GB in 3,697 objects remain).
  Walls, discs and shells, three energies each, in both views: no page error, no failed request.
- R2: 2,782 replaced run files under `resonant-tunnelling/2026-11-18/runs/`, 4,439,713,712 bytes; SHA-256 checked against
  the branch records and R2's MD5 against the bytes sent. Generation 2026-11-14 untouched (6.53 GB). Total about 10.97 GB.
- Kaggle: `numakoudsie/fig15-filer-2026-11-18` v4 (CPU) filed it; `numakoudsie/fig15-filer-dry` v1 is the dry run.
  Filer: `tools/kaggle/resonant-tunnelling/correction/file_corrected.py` on `claude/fig15-correction`, commit 12b8fd09.
- Counts: walls 170 kept, 918 rebuilt (exact). Discs 745 kept, 1,582 replaced by the (x, rho) run. Shells 282 replaced,
  not gated (the stored shell index has no transmission). Provisional (T_unc > 0.005): 72 discs, 241 shells.

## Decisions the owner made
- Shells: option B. File all, write T_unc, mark T_unc > 0.005 "provisional" for discs and shells alike.
- Upload: option A, relay through this container.

## Done on 18 Nov, after the first state (Fact, live site unless said)
- Home page counters read the real lists: "7 projects, 4 shown here" (article.proj on portfolios.html), "16 figures, 11
  shown here" (distinct fig in catalog.js). main 2edfa37d; checked live at 1440 and 390 px.
- R2: the 2,782 replaced 2026-11-14 files deleted (log `coordinator-2026-11-18/r2_delete.log`); the bucket's object list
  sums to 6,184,011,989 bytes in 3,697 objects.
- main 808c91ab: the correction code (tools/kaggle/resonant-tunnelling/correction/, 22 files) and the correction records
  and logs (notes/fig15/) are on main; the data panel shows status, T_ref, T_old, error, gate, T_unc, drift,
  provisional, checked live on a wall, a disc and a shell; stale sentences about generation 2026-11-14 corrected.
- Guinness run 10: the live Fig. 12 page loads 2026-11-14-run10/index-jax.json and its ride, no error.
- The Fig. 15 writer (session_01DGmqiqazJ9UxECtFYiespR) ordered to rewrite the note for 2026-11-18: numbers from the new
  index, sections 10-11 rewritten, 6-9, 12, 13 made true, one referee and one derivation-checker round, merge, reply.

## What is left
1. The lecture note: the writer's work, under way.
2. The biased walls (475): an independent check is written (`coordinator-2026-11-18/biased_walls_check.py`, own transfer
   matrix over thin slices of the ramp, packet average, 12 biased and 3 unbiased walls) but its Kaggle CPU launch was
   refused by the session's permission check; it needs a yes that names it.
3. The owner's decisions: the gate tolerance; whether the 313 provisional runs get longer runs (new GPU time); deleting
   the R2 token from the Default environment.
