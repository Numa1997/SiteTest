# Guinness, 18 November 2026: what each session did (one log, both sessions; times UTC)

Sessions: PAGES = session_01DGmqipAnEdVvBLCf7CLGmT (branch claude/guinness-open-problems, merges to main = the live site).
SOLVER = session_01DGmqioyaYR5VnnZaKfpEhD (branch claude/continuous-spill, never merged, nothing of it is live).
Split agreed 21:30: SOLVER edits only tools/fig12/kaggle/stout_jax.py and run_b.py's solver calls; PAGES edits pages, drawing,
notes on the site, docs. Neither edits the other's files.

## Live on the site (PAGES)
| time | what | commit |
|---|---|---|
| ~19:00 | Wheels: blur only over the angle really turned (max 0.12 rad), one gold spoke | d18338a4, main e1a72d71 |
| ~21:55 | The Guinness pages told apart: titles, strip under the title, Fig. 16 panes labelled | 77af541f, main 75343c8a |
| pending test | In-browser Fig. 12 page beer-slosh.html deleted; its address forwards to guinness-kaggle | f5fc0639 (Kaggle CPU v23) |

## Tried by PAGES, not live
- Spill drawn by merging drops per 5 mm cube (146f6bbe): tested, looked no better, not merged.

## SOLVER: the continuous spill model (stout stays liquid over the rim, down the glass, onto the cart), all on Kaggle CPU, no GPU
| time | what | commit |
|---|---|---|
| 19:18 | one model inside and outside the glass | 214fd3df |
| 19:33-20:47 | three faults found by PAGES' review (wall leak and no surface outside; mirror images; surface near outer walls) and two by its own tests (floor-corner leak; wall-column reading), all fixed | f885e961, 71ef8836, c8fb9670, f315e4aa, 6a41be3c, 86bbb880 |
| ~22:00 | 2 mm test ALL PASS: pint at rest 125.01 mm, 0 lost, 0 outside; shove spills as one liquid, books exact | 6a41be3c |
| 22:02-22:10 | air drag coded; its check FAILED (0.0805 vs 0.1197 m/s^2); fix written, not run | 036b81d2, 06bd5ed6 |
| 22:11 | STOPPED by the owner: no recompute, no GPU, animation from stored rides first | 50319a6a |
| 21:30 | 2 mm test at cc51c2c (continuous-spill-smoke-2mm-c) launched before the stop; finishes on its own, result pending | cc51c2c6 |

## 22:20-22:30: the solver session stopped for good
- It pushed notes/spill/HANDOFF.md (58d05855); it was interrupted and archived. All work is now the pages session's.
- claude/continuous-spill merged into claude/guinness-open-problems (tools and notes only; no page changes). claude/guinness-realism
  NOT merged (the look the owner rejected), pending the owner's decision.
- The deletion of beer-slosh.html is live (main 4748e5c2): its addresses answer 301 to guinness-kaggle.html (curl).

## Owner's decisions today
- No recompute (the stored rides stay); no renumbering of figures; no physics in the browser (beer-slosh deleted).
- First a working animation from the stored rides; air resistance and the air's parameters after that. The owner checks the animation.

## SOLVER, earlier the same day: the look of the figures (branch claude/guinness-realism, never merged, nothing live)
- 17:30-18:30: before pictures of both pages (Kaggle CPU guinness-realism-fig12 v2, 24 pictures; -fig16 v2, 16).
- One path-traced frame in Blender, Kaggle GPU guinness-realism-render v1, 6.5 T4-minutes (commit 67ea2ae): the only GPU use of
  either session today.
- A live-3D pint and Fig. 16 cart (pint3d-view.js, cart3d.js, one hook in guinness16-play.js; commits 9a6e8ef, 00ce483, c856f68),
  CPU screenshots fig16 v3-v5. The owner rejected that look. PAGES' deck-pixel lines for cart16-view.js are on that branch only.
- Both SOLVER branches merge into main 75343c8 with 0 conflicts (git merge-tree); neither is merged.
