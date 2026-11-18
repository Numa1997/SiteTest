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

## What is left
1. The lecture note (`public/scripts/resonant-note.js`) still describes generation 2026-11-14: method, gate and numbers.
   The writer chat (session_01DGmqiqazJ9UxECtFYiespR) is idle since 14 Nov.
2. The data panel's variables do not yet carry T_ref, T_unc, status; the source line under the figure does.
3. The correction code lives only on `claude/fig15-correction`, not on `main`.
4. Not verified by this chat: the 475 biased walls against an independent transfer matrix (hand-off 8.6 point 1);
   Guinness run 10 in a browser.
5. The gate tolerance max(0.005, 1 %) is still not confirmed by the owner.
6. The 313 provisional runs: a longer run would settle them; that is new GPU time, the owner's decision.
7. The R2 token is no longer needed for Fig. 15 once the owner accepts this generation.
8. Storage: about 0.97 GB above R2's 10 GB free tier, about 0.015 USD per month.
