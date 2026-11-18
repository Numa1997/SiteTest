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
| 19:33-20:47 | four faults found by PAGES' review and fixed: leaking wall, no surface outside, mirror images, floor corner, wall rule | f885e961, 71ef8836, c8fb9670, f315e4aa, 6a41be3c, 86bbb880 |
| ~22:00 | 2 mm test ALL PASS: pint at rest 125.01 mm, 0 lost, 0 outside; shove spills as one liquid, books exact | 6a41be3c |
| 22:02-22:10 | air drag coded; its check FAILED (0.0805 vs 0.1197 m/s^2); fix written, not run | 036b81d2, 06bd5ed6 |
| 22:11 | STOPPED by the owner: no recompute, no GPU, animation from stored rides first | 50319a6a |

## Owner's decisions today
- No recompute (the stored rides stay); no renumbering of figures; no physics in the browser (beer-slosh deleted).
- First a working animation from the stored rides; air resistance and the air's parameters after that. The owner checks the animation.
