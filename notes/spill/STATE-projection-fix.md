# Bowl-base drain test of the projection solver: chat state (read first after any compaction)

Branch `claude/guinness-projection-fix`, cut from 7d29ec55 (the v8 code) on 20 Nov 2026.
The one-model MPM work (branch `claude/guinness-one-model`, head 58c1a98) is PAUSED: keep it, do not delete it.
Open item there (outside review, round 2 B): in mpm2d.py, at a node with sd <= 0 where stout and head both scatter, the stout's
infinite no-slip coefficient also clamps the head's tangential velocity.

## The task (owner, 20 Nov 2026)
One diagnostic test deciding between the two solvers. Hypothesis (outside review, two rounds): at 1.5 mm, empty cut cells beside the
bowl-shaped base read as air (stout_jax.py wallcut radial bound; ls_inherit), the ghost-fluid projection drains liquid into them,
and _g2p_cont clamps particles back into the cavity: the pint at rest compresses (v8: mean particle height 72.69 -> 67.74 mm in 1 s).
Predicted: about 36 such cells at 1.5 mm.

Test: tools/spill/rest_variants.py, DRAIN=1, case F (Fig. 16 deck, model "full", gamma = 0, dx = 1.5 mm), dt = 2 ms, at rest.
1. Smoke: 3 steps on the T4, all logging present. Quota read fresh first; cost stated.
2. Sub-run 1: baseline code, 0.2 s. Every step: it, res, n_drain_faces (theta > 0 faces joining liquid and non-liquid below
   z = 0.11 m), mean particle height, median surface, particles outside the cavity.
3. Sub-run 2: 1.0 s, one change: on solid cells (centre in the glass, with an open face) phi_liq(x) = phi_liq(x - phi_glass n_s),
   replacing wallcut / ls_inherit there (stout_jax.py Stout.enable_ls_extend, switch ls_extend, off by default).

Pass marks (fixed before the runs), sub-run 2: n_drain_faces == 0 at every step; it < 600 and res < 1e-5 at every step;
|mean height(1 s) - mean height(0)| < 0.05 mm; |median surface(1 s) - 125.0 mm| < 0.2 mm; 0 particles outside.
Decision: sub-run 2 passes -> explanation confirmed, report and stop. Sub-run 2 fails with n_drain_faces == 0, or sub-run 1 shows
it == 600 -> explanation refuted, report the logs and stop. No further fixes.

## Rules
- (Owner, 20 Nov 18:4x UTC) While writing code with no Kaggle run active: a one-line status every 10 minutes (clock time, what I am doing, expected time of the next launch).
Kaggle only; time estimate, live monitor (clock and elapsed), results to file per sub-run, outputs committed, run times at the end.
Commit author: the repository owner's git identity; no assistant or model names; no co-author lines. Never: main, Workers, R2,
public/de/, public/ar/, scripts/i18n/, *.rtl.css. May change: tools/spill/rest_variants.py, stout_jax.py (sub-run 2, behind the
switch), notes/spill/*.

## Note for later (do not act now)
If the projection route goes ahead: (a) the sloshing check uses the solver's free mode 3.42 Hz (stout_jax.py:37), not
PLANT_F0 = 2.915 Hz (cart4.py:78, a fitted controller model); (b) the factor in the plastic return map (G dt gdot vs 2 G dt gdot)
is fixed by the tilted-slab test, not assumed.

## Log
- 20 Nov: branch created; switch and logging written (code read only, syntax parsed). Next: quota, smoke run.
- 20 Nov 04:26-04:39 UTC: runs done (T4). Code 40b112b9 (switch) / outputs in notes/spill/drain/.

## Results (Fact; files notes/spill/drain/drain_full_{base,ext}.jsonl, *_summary.json, full.log)
| run | launched | finished | total | script |
|---|---|---|---|---|
| smoke (3 steps each code) | 04:26:19 | 04:29:35 | 3 min 16 s | 86 s |
| full v1 | 04:30:49 | 04:33:40 | 2 min 51 s | crashed in the new logging (vertical-face histogram shape), before step 1 |
| full v2 (base 0.2 s, ext 1.0 s) | 04:34:10 | 04:39:15 | 5 min 5 s | 212 s (base 76 s, ext 109 s) |
GPU used about 11 min (quota read 04:2x: 195 min left of 1 800).

Sub-run 1 (baseline, 0.2 s): it 192-274 (never 600), res max 9.9995e-6; mean particle height 72.695 -> 71.881 mm (-0.81 mm,
-4.1 mm/s); median surface 124.938 -> 124.315 mm; outside 0. n_drain_faces 15 111-15 194.
Sub-run 2 (extension, 1.0 s): it max 211 (mostly 3-30), res max 9.9992e-6; mean height 72.695 -> 72.691 mm (-0.004 mm);
median surface 124.938 -> 124.869 mm; outside: 1 particle at one step (t = 0.872 s), else 0. n_drain_faces 15 109-15 116.
Where the drain faces are (step 1): base: 14 595 "other" (no solid-centred cell, not both cells in the cavity), 599 touching a
solid-centred cell, 0 inside the cavity; layer z = 0.75 mm holds 36 faces in base and 0 with the extension; ext: 14 595 other,
517 solid. The "other" faces sit in every layer from 0.75 mm up (about 170-230 per layer) and do not change between the codes.

Pass marks of sub-run 2: n_drain_faces == 0 every step FAIL (15 109-15 116); it < 600 PASS (211); res < 1e-5 PASS (9.9992e-6);
|mean height change| < 0.05 mm PASS (0.004); |surface - 125.0| < 0.2 mm PASS (0.131); 0 outside FAIL (1 at one step).
Verdict by the owner's rule: sub-run 2 did not pass; neither refutation condition holds (n_drain_faces is not 0; sub-run 1 never
reached it = 600). Waiting for the owner.

# Step 2: side visibility (owner's go, 20 Nov 2026: "keep going until finish line or an error comes up")

## The task (plan delivered 20 Nov as a system notice; owner said go)
Below the rim (z < 0.1475 m) particles, mirror images and solid extension may touch only grid cells on their own side of the glass
wall; the velocity is extrapolated into unknown faces once per side and each particle reads its side's copy. Switch S.enable_side_vis()
(stout_jax.py; off = unchanged). Test: rest_variants.py STEP2=1, three cases at dx 1.5 mm, dt 2 ms, case F, enable_ls_extend on:
rest_2s (2.0 s), push_tagged (outer band 15 mm wide beyond R_out, deck to 0.060 m, bx = 5 m/s^2 for 0.2 s, 0.5 s, side_vis on),
push_untagged (same, side_vis off: negative control). Smoke (5 steps per case) first, then full. Stop and report after Step 2.

## Pass marks (from the plan, table 2.3)
rest_2s: n_drain_bowl == 0, n_phantom_out == 0, n_drain_total == 0 every step; it < 600, res < 1e-5; outside_strict == 0 (every
stray particle logged in step2_*_stray.jsonl). Mean height change and median surface: THRESHOLDS LOST IN PASTING, owner to give;
values are reported raw (Step 1 used 0.05 mm and 0.2 mm). push_tagged: crossings below the rim == 0. push_untagged: crossings or
phantom bleed (n_phantom_hi: outside-side liquid cells with z_c in 0.075 m .. rim, above the band) > 0.

## Choices made in the code (say so in the report)
- Side of a cell or face centre: Geometry.side_of. Open points: the region holding them (cavity below the rim = True). Points in the
  glass: the nearer open surface in the (r, z) section. Equal to the plan's R_mid(z) rule for open points above the floor; differs only
  inside the glass's foot and thick bowl base, where the radial mid-line does not follow the wall.
- Side of a particle: r < R_mid(min(z, rim)) (above the rim: the rim's mid-radius), so particles above the rim write into the
  matching side below it.
- "Merged above the rim": both velocity copies keep every known face above the rim; unknown faces there are filled per copy.
- outside_strict uses z > -1e-5 m (the plan wrote z > 0) so the floor gets the same 1e-5 m tolerance as the wall.
- Band particles carry the pint's particle mass; K = N (no cap); nsel logged and flagged if it reaches K.

## Log
- 20 Nov ~18:30 UTC: code written (syntax parsed only; no run in the container).
- 20 Nov 18:17:01-18:21:32 UTC: smoke (code a49b6481), Kaggle step2-side-smoke, T4, 4 min 31 s total, script 184.5 s. Outputs in
  notes/spill/step2/. rest_2s 5 steps: n_drain_bowl 0, n_drain_total 0 (Step 1: 15 109-15 194), n_phantom_out 0, outside 0/0 after
  step 1 (t = 0: 280, strict 231, seed jitter), it 31-250, res < 1e-5. push_tagged: n_phantom_hi 0, crossings 0; push_untagged:
  n_phantom_hi 10 081-10 112 (the control discriminates), crossings 0. Extension: 17 240 cells, unresolved 0. Band 766 880
  particles; nsel 0.69 M < K. Step time about 0.2 s (rest), 0.4 s (push).
- 20 Nov 18:21:50 UTC: full run launched (Kaggle step2-side-full, T4). Quota before: 185 min left of 1 800 (resets 21 Nov 00:00 UTC).
- 20 Nov 18:21:50-18:34:10 UTC: full run done (code a49b6481), Kaggle step2-side-full, T4. Outputs notes/spill/step2/step2_full_*.
  GPU used by smoke + full: 966.8 s = 16.1 min (quota 96 893.7 s -> 97 860.5 s used; 169 min left until 21 Nov 00:00 UTC).

## Step 2 results (Fact; files notes/spill/step2/step2_full_*_summary.json, *.jsonl, full.log)
| run | launched | running | finished | total | script |
|---|---|---|---|---|---|
| smoke (5 steps x 3) | 18:17:01 | 18:17:07 | 18:21:32 | 4 min 31 s | 184.5 s |
| full | 18:21:50 | 18:21:55 | 18:34:10 | 12 min 20 s | 627.2 s (rest 258 s at 0.258 s/step; push 152 s and 144 s, 0.58-0.61 s/step) |

rest_2s (2.0 s, 1000 steps, side_vis on): n_drain_bowl 0, n_drain_total 0, n_phantom_out 0 at every step (Step 1 ext: 15 109-15 116
drain faces); it max 250 (step 1, then 24-84), res max 9.99999e-6; mean height 72.6948 -> 72.6892 mm (-0.0056 mm; range 72.6882-72.6948);
median surface 124.938 -> 124.973 mm at 2.0 s (|H - 125| = 0.027 mm; range 124.865-124.973, minimum near 1 s, then back up);
outside_strict 0 every step; outside 1 at one step (219, t = 0.438 s): particle 996282 at z 124.27 mm, r - R(z) = -2.5e-9 m in
float64 (inside the wall), counted outside by the float32 check: rounding at the wall, not penetration. Extension 17 240 cells,
unresolved 0. All six pass marks with thresholds PASS; the two without thresholds reported above.

push_tagged (side_vis on) / push_untagged (off), 0.5 s: crossings below the rim 0 / 0. Both pints spill over the rim: first pint
particle outside at step 61 (t = 0.122 s), at z = 147.6-147.9 mm (rim 147.5 mm), r 37.5-37.9 mm; outside up to 3 494 / 5 166 pint
particles, every one counted by the strict test too; none changed side while below the rim (crossings 0), so all went over the rim.
n_phantom_hi (outside-side liquid cells, z_c 75 mm .. rim): tagged 0 until step 68 (after the spill began at step 61), max 4 946;
untagged 10 112 from step 1 (before any spill), max 15 940. The control discriminates (pass); tagged crossings 0 (pass).
Caveat (Inference): after step 61 n_phantom_hi in push_tagged also counts the real spilled stout running down the outside, so it is
not a clean phantom count there; before the spill it is 0 with side_vis and about 10 100 without.

Decision rule of the plan: all pass marks hold; the one outside > 0 is wall grazing (2.5 nm, float32) -> commit, report, stop for
the owner's yes before Step 3. The 1e-5 m guard in _g2p_cont (plan 2.4) is not made yet: it is a code change for the owner to approve.

# Step 3: taller grid, rounded lip, bare stout (owner: "sure go ahead", 20 Nov 2026, after the Step 2 report)
Two Step 2 thresholds (mean height change, median surface) are still not given; the owner did not answer that part.

## Code (stout_jax.py, all behind arguments or switches whose defaults keep the old behaviour)
- Geometry(top=0.03, lip=0.0): grid height above the rim; rounded lip = disc of radius lip about (R_m, z_c), z_c = rim - lip (attribute zlip),
  R_m = R(z_c) + WALL/2 (lip = WALL/2 = 1.25 mm is a half-round top, rim height unchanged). Geometry.glass (glass alone, with lip) and
  Geometry.section_lines (the (r, z) section as the cavity's and the outside's polylines) now serve solid(), side_of() and
  enable_ls_extend (same polygon as before when lip = 0).
- _g2p_cont: a particle that a step puts in the lip goes out along the disc's radius to lip + 0.1 dx and loses its velocity into it.
- Stout.wall_guard (plan 2.4): after the collisions a cavity particle within 1e-5 m of the inner wall is put 1e-5 m inside it.

## Test: rest_variants.py STEP3=1 (Fig. 16 deck, model "wall" = no head, gamma 0, dx 1.5 mm, dt 2 ms, top rim + 0.08 m, lip 1.25 mm,
side_vis + extension + guard on)
- slosh: rest 0.3 s, push 1.0 m/s^2 for 0.146 s (damping_grid.py's push), free to 2.5 s; ring 13 cos part every 5 steps; fit_swing
  (run_b.py) from 0.546 s. Pass: |f / 3.421 Hz - 1| < 3 %; 0 ceiling hits; 0 crossings; 0 particles deeper than 1e-5 m in a solid.
- overflow: push 5.0 m/s^2 for 0.2 s, to 0.6 s. Pass: 0 ceiling hits (z >= top - dx), 0 crossings below the rim, 0 in solid, stout over.
- Note (Fact): 3.421 Hz is the upright cylinder of R(fill) = 39.1 mm (notes/fig12/handoff-control-session.md:151). The tulip measured
  0.7-1.2 % above the cylinder on each of four grids (notes/fig12/check.md:169); the old JAX model at 1.5 mm, inviscid, gave 3.326 Hz
  (notes/fig12/damping-grid.json, -2.8 %). So the 3 % mark is reachable but tight at 1.5 mm.

## Log
- 20 Nov ~19:05 UTC: Step 3 code written (syntax parsed only).
- 20 Nov 18:45:41-18:47:29 UTC: Step 3 smoke v1 (code 31ce6a31) crashed before step 1 (Geometry.__init__): the lip's centre height,
  named zc, was overwritten by the existing cell-centre array Geometry.zc. Renamed zlip. Log notes/spill/step3/smoke_v1.log.
- 20 Nov 18:47:59-18:53:47 UTC: Step 3 smoke v2 (code 9fbc0edf), Kaggle step3-lip-smoke v2, T4, 5 min 48 s (queue 2 min), script
  149 s. Grid 211 x 87 x 176, top 228.0 mm; lip about (R_m 38.792 mm, z_c 146.250 mm); extension 17 272 cells, unresolved 0. Both
  cases: in solid 0 after step 1 (231 at t = 0: seed jitter), ceiling 0, crossings 0, it <= 311, res < 1e-5. About 0.33 s a step.
- 20 Nov 18:54:05 UTC: Step 3 full run launched (Kaggle step3-lip-full, T4).
