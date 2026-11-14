# Fig. 12 in JAX: state before run 8 (13 November 2026, 22:20 UTC)

Written by the session "Guinness cart: JAX solver, fix and run" before its context compacts.

## The aim

Control the pint of Guinness on the one-wheel cart over the bumps. All data comes from the JAX solver on Kaggle's GPU
(notebook numakoudsie/guinness-on-a-cart-stout-in-jax), stored, and played on the live page
https://phyeinusul.com/simulations/guinness-kaggle (public/simulations/guinness-kaggle.html). The browser computes no physics.

## What is live (main at e89a0c6)

- Run 6 (notebook version 6, commit 4c10527): the three rides with the speed held only (ride_resonant, ride_sharp30,
  ride_bump25) and the free swings with and without the head (free_full_1.5, free_wall_1.5).
- Run 7 (version 7, commit 87e3720): the same roads with the site's controllers ported into stout_jax.Cart (joint on all three;
  slosh LQR and road preview on the kerb). Port checked against the JS cart: notes/fig12/handoff-jax/portcheck.txt.
- Data: public/data/fig12/2026-11-13/index-jax.json and the ten files it lists (each names its version and commit); only the
  columns more than one cell inside the glass are stored (tools/fig12/kaggle/pack_ride.py).
- Corrected leans (read from the trusted columns as the page draws them): speed held only 17.3 / 34.1 / 10.6 mm (five bumps,
  kerb, 25 mm bump), tilts 15.1 / 27.6 / 9.0. Joint control: 1.05 / 30.0 / 0.89 mm. Kerb spill: head 4.08 mL with the speed held,
  2.74 to 3.66 mL with control; stout 0.008 g (19 particles) with the speed held, 0 with control.
- The note (sections 1-13): section 10 results of run 6, section 11 the controllers and run 7 (Tables 7 and 8), section 12
  limits (the head has weight but no mass: with its mass the first mode falls to about 3.07 Hz).
- public/data/fig12/generations.json lists the JAX generation (runs 6, 7) as played.
- Run notes: notes/fig12/handoff-jax/05-run3-changes.md (runs 3 to 7 and the lean correction).

## The run-8 order (relayed from the user's coordinating chat, 22:04 and 22:25 UTC; asked here for a yes at 22:10 UTC)

1. Mass books per frame: stout in the glass (initial minus particles that left, 0.429 mg each) and head in the glass (91.3 mL
   minus the lumps broken off), stored per frame; check glass + spilled = initial per frame; print the largest error.
   Found: the solver already conserves both exactly; the stored stout_g at 0.01 g hides the kerb's 0.008 g (429.583 and
   429.575 both print 429.58). The head's thickness is stored per column per frame and the page draws it: at the kerb 181
   columns thin, some by the full 19 mm. So items 1 and 2 are packing and readings work only (no GPU).
2. The head thinning on screen: already so (above); show "stout in glass" and "head in glass" readings falling as they spill.
3. The head's mass in the solver: 272 kg/m3, 19 mm (5.17 kg/m2), inertia on the columns it rests on, not only weight. Check the
   free swing on the CPU first: near 3.07 Hz (note section 12: omega^2 = g k tanh(kh) / (1 + m_s k tanh(kh)/rho)).
4. Recompute on Kaggle every ride the page plays (run 6's three, run 7's five) and both free swings with the new head and the
   per-frame books; arithmetic in one line; under 1.5 GPU hours (estimate: about 2,600 s of T4 time, about 5,300 quota s).
5. Store as run 8 (keep 6 and 7), update generations.json, the note (sections 9 to 12), the docs, the page's readings; merge;
   check live. Report once when live: books closed, the new frequency, the new leans and spills with and without control.

## Done of it (14 November 2026, 00:40 UTC)

All five items. The head's mass is in `Stout.pressure` (Robin condition, the head's own vertical velocity `wh` as state);
CPU check at 6 mm 2.737 Hz against 2.722 Hz predicted. Run 8 (notebook version 8, commit 96e8a1d) and version 9 (commit
726d51a, the kerb with the preview, skipped by run 8's budget) passed every check; books closed in every frame (0 particles,
at most 1.3e-8 mL). Swing with the head's mass 2.915 Hz (2.957 expected), zeta 0.425; the controllers designed on it.
Leans (trusted columns), speed held -> control: five bumps 13.9 -> 0.95 mm (joint); 25 mm bump 8.9 -> 0.76 mm (joint);
kerb 24.3 mm, 2.44 mL of head -> joint 25.4 mm, 2.00 mL; slosh 21.8 mm, 1.65 mL; preview 21.2 mm, 2.46 mL; no stout spilled.
Stored in public/data/fig12/2026-11-13-run8/ (runs 6, 7 kept in 2026-11-13/); generations.json, the note (5.6, 7.3, 9 to
12, abstract), docs/simulations/fig12-beer-slosh.md, docs/kaggle-pipeline.md and docs/files.md updated. Open point found after
the run: the controllers' beta is still the bare stout's 1.541; with the head carried it should be 1.241 (note section 10).

## Files that matter

tools/fig12/kaggle/stout_jax.py (solver, Cart with controllers, Stout.prepare/probes), run_b.py (tasks: RUNSET=control for
run 7's set; TASKS for run 6's), pack_ride.py, check_run.py, nb/run_b_cell.py (notebook cell template), portcheck/;
public/scripts/guinness-jax-play.js, stout-view2.js; docs/simulations/fig12-beer-slosh.md; docs/kaggle-pipeline.md.

## The user's rules for this chat

Plain short words. No tables, no apologies, no recaps, no option lists, no "Where we are" lines. Mark facts with a handle.
Never put data from a run that failed its checks under public/. Before every GPU run: one line with what, where, how long, cost.
