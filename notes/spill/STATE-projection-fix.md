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
- 20 Nov 18:54:05-19:07:42 UTC: Step 3 full run (code 9fbc0edf), Kaggle step3-lip-full, T4, 13 min 37 s, script ~692 s (slosh 474 s
  at 0.379 s/step, overflow 159 s at 0.529 s/step). Step 3 GPU (3 sessions): 1 089 s = 18.2 min; 150.8 min left until 21 Nov 00:00 UTC.

## Step 3 results (Fact; notes/spill/step3/step3_full_*_summary.json, *.jsonl, full.log)
slosh (bare stout, 1.0 m/s^2 for 0.146 s, free to 2.5 s): fit of ring 13 from 0.546 s: f = 3.3209 Hz (f0 3.3212), -2.93 % of
3.421 Hz -> PASS (inside 3 % by 0.07 %); zeta 0.0134, amplitude 6.0 mm, fit rms 0.070 mm. The old model at 1.5 mm gave 3.326 Hz.
Ceiling 0, crossings 0, in solid 0, it <= 285, res < 1e-5, z max 132.5 mm (no overflow), mean height 72.695 -> 72.641 mm.
overflow (5.0 m/s^2 for 0.2 s, to 0.6 s): stout above the rim from step 38 (0.076 s), over the lip from step 52; up to 18 930 above
the rim and 18 262 on the outside's side; 16 385 particles left the grid (fell off the deck). Ceiling 0 (z max 178.1 mm, top 228 mm),
in solid 0 at every step, it <= 311, res < 1e-5. CROSSINGS 10 -> FAIL of the mark "0 crossings below the rim": 1-2 per step at
steps 78-99 (t 0.156-0.198 s) only, while 3 700-18 900 particles were above the rim; none before the spill or after step 99.
Inference (not proven): the crossing test counts a side change with both positions below z = rim (147.5 mm). With the rounded lip,
stout sliding over the lip's shoulder sits below 147.5 mm (lip surface at r = R_m +- 0.8 mm is z = 147.21 mm, plus 0.15 mm offset)
while it passes r = R_m: a legal pass over the top that the test reads as a crossing. The test was written for the square rim.
To prove: rerun overflow logging each crossing's old and new positions and whether the segment between them passes through the
glass (about 4 GPU-min). Stopped here for the owner (a pass mark failed).

# Task A: close Step 3 (instruction notes: uploaded PROMPT-for-ClaudeCode-step3verify-step4.md, section 5; owner's yes 20 Nov ~21:00 UTC)
Step 2's two height marks are now given (instruction section 3): 0.05 mm and 0.2 mm; Step 2's -0.0056 mm and 0.027 mm PASS.
Rules added (instruction section 4): dt = min(2e-3, 0.8 dx/vmax, elastic limit) in every test from Step 4 on (Task A keeps 2 ms on
purpose); pass marks written with abs( ), never "|" in tables; each check in its own guarded block.
Task A code (diagnostic only): Stout.diag_g2p (state carries xprop, the position before _g2p_cont's collisions, and g2p_glass; motion
unchanged); rest_variants.py STEP3_VERIFY=1 (overflow of STEP3 exactly; old test unchanged; phi_glass at 17 points per step for
particles within 5 mm of the glass; verdicts REAL_CROSSING / LIP_CHORD_CLIP / CLEAR / SHALLOW_OTHER). Outputs notes/spill/step3_verify/.
Pass marks (fixed): old_cross_count = 10 at steps 78-99; real_crossing_count = 0; n_in_solid_max = 0, it_max < 600, res_max < 1e-5;
every flagged particle logged with its verdict.
Choices: z_cross is where the step crosses the side test's mid-radius R_mid(min(z, rim)) (Stout.p_side), which near the lip is
R_m within about 0.05 mm; "side changes below z_rim" means both ends below z_rim; counts are particle-steps within 5 mm of the glass;
SHALLOW_OTHER = phi_min in [-6.25e-4, 0) that is neither a lip-chord clip nor real (the instruction's three classes do not cover it).
Risk: the GPU's scatter order is not deterministic, so the reproduction of exactly 10 old-test events can miss by chance.
- 20 Nov 21:04:05-21:07:05 UTC: Task A smoke (code 8f672e62), Kaggle task-a-verify-smoke, T4, 3 min 0 s, script 80 s. 5 steps:
  old cross 0, real 0, in solid 0 after step 1, it <= 311, res < 1e-5; step 1 "other" 280 = the seed-jitter particles in the foot moved
  out (phi_min -0.20 mm, not real); about 290 000 particles within 5 mm of the glass; about 0.7 s a step.
- 20 Nov 21:07:18 UTC: Task A full run launched (Kaggle task-a-verify-full, T4).
- 20 Nov 21:07:18-21:13:24 UTC: Task A full run (code 8f672e62), Kaggle task-a-verify-full, T4, 6 min 6 s, script 242 s
  (0.81 s/step). Task A GPU (smoke + full): 506.7 s = 8.4 min; 142.4 min left until 21 Nov 00:00 UTC.

## Task A results (Fact; notes/spill/step3_verify/summary.json, flagged_particles.jsonl, steps.jsonl, full.log)
All pass marks PASS: old_cross_count 10 at steps 78, 84, 87 (2), 89, 90, 91, 92 (2), 99 (same steps and counts as Step 3);
real_crossing_count 0; n_in_solid_max 0; it_max 311; res_max 9.995e-6; all 10 flagged particles logged; none capped.
The 10: all LIP_CHORD_CLIP, hit_g2p false, both ends in open air above the lip (z 147.40-147.50 mm; z_lip 146.25 mm), step length
0.48-0.83 mm (ds/dx 0.32-0.55), chord dips into the crest by 0.002-0.039 mm, crossing height 147.459-147.498 mm (rim crest 147.5).
Over the run (particle-steps within 5 mm of the glass): LIP_CHORD_CLIP 116 (steps 60-127), SHALLOW_OTHER 294 (280 = the seed-jitter
particles moved out of the foot at step 1, phi_min -0.20 mm; 14 later, all shallower than 0.068 mm), REAL 0; deepest dip after
step 1: 0.068 mm. hit_g2p: 379 442 particle-steps (contacts the collision resolved).
Step length: ds/dx > 1 at every step from 89 to 300; max 4.11 (6.17 mm in one 2 ms step, step 186, vmax 3.07 m/s): the fixed
2 ms step lets the fastest stout move more than the wall's thickness per step. No penetration followed here, but rule 8 (dt limited
by 0.8 dx / vmax) is needed from Step 4 on.
Code check at 9cecadc: dt fixed 2 ms (rest_variants.py step3_run, dt = 0.002); old test rest_variants.py:333 (Step 2's copy :219);
lip solid stout_jax.py:204, outline section_lines :208-219, extension polygon from section_lines; _g2p_cont at lip > 0: from_top is
off, a particle inside the lip's disc goes out along the disc's radius to lip + 0.1 dx; a particle in the shell below z_lip goes to
the side its old position was nearer (from_in / from_out).
Reproduction: the run follows Step 3 exactly to step ~113, then drifts (GPU scatter order; vmax 3.07 m/s here, 2.34 m/s in Step 3).
Decision rule: real_crossing_count = 0 -> Step 3 CLOSED (PASS). Waiting for the owner's yes before Task B (Step 4).

# Task B: Step 4, the head as an elasto-viscoplastic foam (owner's yes 21 Nov 2026 ~13:50 UTC)
Quota reset 21 Nov 00:00 UTC: 1 800 GPU-min fresh (read before every GPU run).
## Code so far
- stout_jax.py: tch_coeffs / EVP_A1 / EVP_A2 (foam_flow_stress written in gdot), RHO_HEAD = PHI_F x 1007 = 271.89, sym_pack /
  sym_unpack / det3, evp_tau (G dev(be)), evp_return_map (instruction B.1: trial f be f^T normalised, yield test on s_tr, 6 Newton
  steps in u = gp^0.47 from an upper bound, 5 Newton steps for c from above). Not yet wired into Stout (that comes after 4.1-4.3).
- tools/spill/step4_slab.py: tests 4.1-4.3, Kaggle CPU. Periodic 8 x 8 x 24 slab, dx 1.5 mm, foam 0..19 mm on the pint's lattice
  (6 400 particles), MAC trilinear weights and APIC as Stout with periodic x, y, no-slip floor by mirror faces, free top. The slab
  holds w = 0 (exact for a laterally uniform incompressible slab: the pressure carries rho g cos(alpha)), so only the tangential
  gravity g sin(alpha) drives it; the pressure step and variable density are tested in 4.4/4.5, not here.
## Prediction written before any run (Inference), test 4.2
The column is undamped below yield (no viscosity in pure foam). A linear ramp of 0.25 s leaves ringing of amplitude
u_s |sin(w Tr/2)| / (w Tr/2) = 0.12 u_s = 2.6e-5 m (w = 2 pi / T1, T1 = 0.0971 s). The marks use instantaneous values: u(h, 4.0 s)
can then sit anywhere in [1.90e-4, 2.43e-4] m against the window [1.948e-4, 2.380e-4] m, and the "creep" u(4.0) - u(0.5) can reach
5.2e-5 m against the 5e-5 m mark with no plastic creep at all. The marks may be badly defined for an undamped column; the run also
reports means over whole periods (supplementary, not marks) so the owner can decide.
- 21 Nov 13:57:57-13:59:16 UTC: slab smoke v1 (code 647f1956, Kaggle CPU, step4-slab-smoke, 1 min 19 s, script 4 s): all three tests blew
  up within 10 steps (vmax 23 m/s, det_dev 1e8): failure mode 1 of B.7. The deviatoric force was divided by the face's own mass, which at
  the foam's free surface is a sliver of a cell. Fix as instruction B.3.5: u += dt F_dev / max(M_f, m_floor), m_floor = 0.05 rho_h dx^3.
  References in that log match the instruction: A1 2.53178, A2 0.84796, tau_v(10/s) 11.7217 Pa, c_s 0.78241 m/s, T1 9.71363e-2 s,
  v_h 1.41705e-3 m/s, z_y 6.333 mm, u_s 1.2363e-4 m (4.1) and 2.1635e-4 m (4.2).
- 21 Nov 14:00:04-14:01:27 UTC: slab smoke v2 (code b8d894ef, CPU, 1 min 23 s): stable, 20 steps each; 4.1 n_yielded 0, det_dev
  3.6e-7, s_max 2.76 Pa; 4.3 yields one layer (256) by step 20. v1 outputs kept in notes/spill/step4/smoke_v1/.
- 21 Nov 14:01:51 UTC: slab full run launched (Kaggle CPU, step4-slab-full).
- 21 Nov 14:01:51-14:04:41 UTC: slab full run v1 (code b8d894ef, CPU, 2 min 50 s). FAIL, outputs in notes/spill/step4/full_v1/:
  4.1: n_yielded 256 (one layer), s_max 8.52 Pa (exact max 2 tau_b = 4.33 Pa), T_fit 0.1007 s (mark [0.09228, 0.1020] PASS),
  cycle mean 1.464e-4 m (mark [1.137e-4, 1.335e-4] FAIL), det_dev 8.3e-7 PASS. 4.2: yields one layer, drifts to 1.30e-3 m (FAIL all).
  4.3: v(h) 7.25e-3 m/s (ref 1.417e-3, 5.1 x; FAIL), shear concentrated in the bottom 1 mm; uniformity 0.0003 (PASS).
  Inference: a harness bug at the floor. The mirror floor (faces at -dx/2, +dx/2, u(-z) = -u(z)) gives the first face above the floor
  the wall's support from half a cell of particles only, so the bottom layer must carry about twice the true stress (8.5 = 2 x 4.3 Pa).
  Fix (v2): faces on the floor, z = 0, hold u = 0 (Z0 = -2.5 dx). Marks unchanged. The return map itself is not changed.
- 21 Nov 14:06:02-14:07:41 UTC: slab smoke v3 (code 54953ba7, CPU): stable, no yield; 4.1 s_max at step 20 halved (1.35 vs 2.76 Pa).
- 21 Nov 14:08:00-14:11:00 UTC: slab full run v2 (code 54953ba7, Kaggle CPU step4-slab-full v2, 3 min 0 s). GPU used today: 0.

## Tests 4.1-4.3 results, v2 (Fact; notes/spill/step4/slab_4.*_full_summary.json, *_series.npz, slab_full.log)
4.1 elastic step (0.4 tau_y, 0.5 s): n_yielded 0 PASS; T1 0.09674 s by fit (0.09683 by up-crossings), mark [0.09228, 0.1020] PASS
  (-0.41 % of 0.09714); cycle-mean top displacement 1.2273e-4 m, mark [1.137e-4, 1.335e-4] PASS (-0.73 % of 1.2363e-4);
  max abs(det be - 1) 6.0e-7 PASS; s_max 4.21 Pa (exact peak 2 tau_b = 4.33 Pa). All PASS.
4.2 sub-yield hold (0.7 tau_y, ramp 0.25 s, 4.0 s): n_yielded 0 PASS; creep abs(u(4.0) - u(0.5)) 4.9e-6 m < 5e-5 PASS;
  u(h, 4.0 s) 1.9027e-4 m, mark [1.948e-4, 2.380e-4] FAIL. As predicted before the run: ringing 2.65e-5 m (predicted 2.6e-5) about the
  mean; mean over the last two periods 2.1432e-4 m (-0.94 % of 2.1635e-4); creep of the period means 1.8e-7 m. The instantaneous mark
  is badly defined for an undamped column (rule 5): the raw numbers are reported, the owner decides.
4.3 plug flow (1.5 tau_y, 0.5 s): v(h) mean over 0.4-0.5 s 1.2953e-3 m/s (std 9.7e-5), mark [1.247e-3, 1.587e-3] PASS (-8.6 % of
  1.4170e-3; a factor-2 return map would give 2.83e-3); plug uniformity 0.00064 < 0.05 PASS. The whole profile sits 8-10 % below the
  exact one (yield height and shape right). det_dev 9.5e-7, Newton residual 1.5e-7.
Decision (B.6): 4.4 and 4.5 wait until 4.1-4.3 pass; 4.2 fails one mark that was flagged before the run as badly defined. Stopped for
the owner. Nothing is wired into Stout yet.

## Owner, 21 Nov ~17:15 UTC: rerun 4.2 with a half-cosine ramp over a whole number of T1 (marks unchanged); rerun 4.3 at dx = 0.75 mm
on CPU (does the 8.6 % shortfall shrink?); then wire the foam into Stout for 4.4, smoke first.
Prediction before the run (Inference): half-cosine over n T1 leaves ringing u_s / (4 n^2 - 1); n = ceil(0.25 s / T1) = 3, Tr = 0.2914 s,
ringing 2.9 % of u_s = 6.2e-6 m, so u(h, 4.0 s) should fall in [2.10e-4, 2.23e-4] m. (A linear ramp over a whole number of periods
would leave none: sin(w Tr / 2) = 0.) Code: step4_slab.py RAMP=cos, DX env (NZ scales, files tagged _dx0.75mm). v2 outputs kept in
notes/spill/step4/full_v2/.
- 21 Nov 17:19:33-17:20:51 UTC: rerun smoke (code 7e5a35db, CPU): 4.2 RAMP=cos and 4.3 at dx 0.75 mm (13 056 particles, 51 layers,
  dt 3.83e-4 s) both exit 0. Full reruns launched 17:21:43 UTC (CPU, step4-slab-full v3).
## Foam wired into Stout (head_mode = "evp"; "sheet" unchanged), written 17:21-17:23 UTC, not yet run
- seed_head: head particles FILL <= z < FILL + HEAD0 on the pint's lattice (hz = HEAD0 / round(HEAD0 / (dx/2)), top exactly 144 mm);
  V_head = integral of pi R(z)^2; m_head = RHO_HEAD V_head / N_head. State carries is_head and be (N x 6), so resort keeps them.
- p2g_evp: momentum, mass M, sum of weights (occupancy, still `mass`), V_f, V_hf, F_dev = -sum V_p tau_p . grad w; rho_f = clip(M/V_f,
  rho_h, rho), beta = rho / rho_f, f_h = V_hf / V_f.
- step: viscosity x (1 - f_h); friction_evp implicit u / (1 + dt lambda), lambda = (a_f / rho_f)[(1 - f_h) rho g_s + f_h tau_w(|u|) /
  max(|u|, 1e-4)]; then u += dt F_dev / max(M_f, m_floor); air drag x beta; pressure coefficients x beta, divergence volume-based,
  update u - beta grad p; after G2P evp_return_map on head particles; diag n_yielded, gp_max, s_max, det range, physical momentum.
- head_sheet, head_spill, the head's weight and Robin load, and the skin are off in "evp".
- rest_variants.py STEP4=1: test 4.4 harness (marks of B.5 4.4).
- 21 Nov 17:21:43-17:25:04 UTC: full reruns (code 7e5a35db, CPU, 3 min 21 s). 4.2 half-cosine over 3 T1 (0.2914 s): n_yielded 0 PASS;
  creep 6.6e-6 m PASS; u(h, 4.0 s) 2.1101e-4 m, mark [1.948e-4, 2.380e-4] PASS; ringing 6.26e-6 m (predicted 6.18e-6). 4.2 PASS.
  4.3 at dx 0.75 mm: v(h, 0.4-0.5 s) 1.5300e-3 m/s = +8.0 % (1.5 mm: -8.6 %), both inside the 12 % mark; uniformity 0.0003 PASS.
  Neither grid is steady at 0.5 s: top speed by 0.1 s windows, 1.5 mm 1.468 / 1.333 / 1.295e-3, 0.75 mm 1.663 / 1.556 / 1.530e-3 m/s,
  still falling 2-3 % per 0.1 s. Diagnostic (not a mark): 4.3 run to 2.0 s at both grids (T43=2), CPU.
  4.1-4.3 all PASS at 1.5 mm -> gate for 4.4 open.
- 21 Nov 17:26:02-17:29:02 UTC: diagnostic 4.3 to 2.0 s (code 853578c8, CPU step4-plug-2s, 3 min 0 s). Steady top speed (last 0.1 s):
  1.5 mm 1.2842e-3 m/s (-9.4 %), steady from ~0.6 s; 0.75 mm 1.5264e-3 m/s (+7.7 %), steady from ~0.5 s; plug uniform (< 3e-4).
  Fact: the error does not shrink with refinement, it changes sign. Inference: not a simple O(dx) error; candidates the yield height's
  place in a cell (z_y/dx = 4.2 and 8.4) and the steep flow law (gdot^0.47) sampled once per cell. Not blocking 4.4 (inside the mark).
- 21 Nov 17:26:02 UTC: 4.4 smoke launched (T4, step4-pint-head-smoke, code 853578c8). Quota: reset, 1 800 GPU-min until 28 Nov.
- 21 Nov 17:26:02 and 17:56:38 UTC: 4.4 smoke (T4, step4-pint-head-smoke v1 and v2, code 853578c8) never started: GetKernelSessionStatus
  and the Kaggle connector's get_notebook_session_status both return empty, no log, GPU quota 0 s used at 18:27 UTC; CPU kernels launched
  at the same minute ran normally. Stopped for the owner (no blind retries). 4.4 code is untested on the GPU.

## Instruction "step4-diag-and-cpu-smoke" (owner, 21 Nov ~19:55 UTC): CPU only, no GPU launch, no physics change in stout_jax.py
Part A: 4.3 diagnostic with h = 0.018 m (whole layers) and no vertical jitter, 2.0 s: C1 1.5 mm 1.5 tau_y (exact 1.3424e-3), C2 0.75 mm
(same), C3 1.5 mm 1.6 tau_y (exact 2.1454e-3); quadrature numbers (V_cell_k / (A dx), k = 0..4; M_tot / (rho_h A h); M_top / (rho_h A dx);
mass floor acted?) also for the original 0.019 m seeds. Marks: C1 abs(err) < 0.025; C2 abs(err) < 0.010 and abs(err_C2) < 0.5 abs(err_C1);
C3 abs(err) < 0.025; C1, C2 abs(V_cell_0 / (A dx) - 1) < 1e-3 and abs(M_tot / (rho_h A h) - 1) < 1e-4. Refutation: C1 or C2 error >= 0.03
with V_cell_0 within 1e-3 and the floor never acting -> stop. Code: step4_slab.py (HH, JITZ, FRAC43, QUAD_ONLY, n_floor, v over the last
0.2 s), step4_diag43.py (runner, diag_4p3.json).
Part B: 4.4 smoke on Kaggle CPU, 5 steps, resort forced at step 3 (rest_variants.py STEP4=1 CPU_SMOKE=1 RESORT_AT=3); marks: all finite;
it < 600, res < 1e-5; drain bowl, phantom, in solid 0 every step; max abs(det be - 1) < 1e-5; books < 1e-6 incl. across the resort;
head mean height across the resort within 1e-5 m. Output smoke_4p4_cpu.json. The two queued GPU sessions are left alone (owner decides).
Answer (Fact, code reading + arithmetic): the pint uses the same rounded layering. seed_lattice: hz = fill / round(fill / (dx/2)):
fill 0.125 m / 0.75 mm = 166.67 -> 167 layers, hz 0.7485 mm, per-cell volume 2 hz / dx = 0.9980 (-0.20 %). seed_head: 0.019 / 0.75 mm
= 25.33 -> 25 layers, hz 0.760 mm, 1.0133 (+1.33 %).
- 21 Nov 19:57:56-20:04:09 UTC: Part B, 4.4 smoke on Kaggle CPU (code 58765350, step4-pint-head-cpu-smoke, 6 min 13 s, script 298 s).
  Fact (notes/spill/step4/smoke_4p4_cpu.json): N 1 207 016 (stout 1 001 952, head 205 064), m_p head 1.1738e-7 kg, V_head 88.527 cm^3.
  All marks PASS: finite; it <= 269, res <= 9.934e-6; drain bowl 0, phantom 0, in solid 0 every step (254 at t = 0, seed jitter, moved
  out by step 1); max abs(det be - 1) 4.8e-7; books 0 (stout and head) incl. after the resort at step 3; head mean height across the
  resort 134.3844 mm -> 134.3844 mm (difference 0.0). No yielding, s_max 0.37 Pa. CPU time per step 79 s (compile), then 32-58 s.
- 21 Nov 19:59:47-20:04:12 UTC: Part A full (code 58765350, CPU step4-diag43-full, 4 min 24 s). Fact (notes/spill/step4/diag_4p3.json):
  steady plug speed (last 0.2 s of 2.0 s): C1 1.3490e-3 m/s, err +0.49 % PASS (< 2.5 %); C2 1.3668e-3, err +1.81 % FAIL (< 1.0 %), and
  abs(err_C2) < 0.5 abs(err_C1) FAIL; C3 2.1593e-3, err +0.65 % PASS (< 2.5 %). V_cell_0 / (A dx) = 1.000 and M_tot / (rho_h A h) = 1.000
  for C1 and C2 PASS. Mass floor never acted (n_floor 0). Refutation rule not triggered (errors < 3 %).
  Inference: the layering explains the bulk of 4.3's -9.4 % / +7.7 % (they fall to +0.5 % / +1.8 % with whole layers), but the
  remainder grows on the finer grid (+1.8 % against +0.5 %): a second, smaller error that does not converge. Stopped for the owner.

## Instruction "step4-seed-fix-gpu-smoke" (owner, 21 Nov ~20:35 UTC)
Decided: 4.3 explained (README notes/spill/step4/README-4p3.md, documented limit; no more runs). Use GPU T4 x2 (no P100). Keep
HEAD0 = 0.019 m at every grid. Stout seed unchanged (-0.20 % known offset).
Part 1 (code, written 20:40-20:41 UTC): seed_head at exactly hl = dx/2: n_full = floor(HEAD0 / hl) full layers + a top layer of
HEAD0 - n_full hl (0.25 mm at 1.5 mm); each particle carries hl^2 x its layer's thickness, in the state (pvol, pmass); books weighted
by particle mass; diagnostic n_floor / n_floor_head (faces where m_floor acts). CPU seed check: tools/spill/step4_seedcheck.py.
Marks: abs(V_cell / dx^3 - 1) < 1e-3 in interior foam cells; V_head equal to the glass volume FILL..FILL + HEAD0 within 1e-6.
Predictions before the run (Inference): (1) the lattice keeps particles 0.25 hl inside the wall, so particles at hl^3 cover about
pi (R - 0.25 hl)^2 per layer: V_head about 0.5 hl / R = 0.96 % short of the glass volume (the V_head mark may fail); (2) with the seed's
vertical jitter (0.3 of the layer) single cells scatter by about +-12 % while layer means stay near 1 (the per-cell mark may fail);
without vertical jitter every interior cell holds exactly 1.
Part 2: one 4.4 GPU smoke (T4 x2), 5 steps, resort at step 3, only after the two stale queued runs are gone; marks as the CPU smoke
plus parity: abs(stout mean height GPU - CPU) < 1e-5 m, abs(head mean height GPU - CPU) < 5e-4 m (the CPU smoke used the v1 head
seed: predicted head-mean difference about +0.24 mm from the re-seeding alone). Then stop for the owner's yes.
- 21 Nov 20:42:00-20:43:44 UTC: seed check v1 (code 08502d64, CPU): top_count wrong (np.isclose default atol 1e-8 > particle volumes);
  outputs kept in notes/spill/step4/seedcheck_v1/. v2 (code 6db80bc1, CPU step4-seedcheck v2, 20:44:32-20:46:05 UTC, 1 min 33 s).
## Part 1 results (Fact; notes/spill/step4/seedcheck.json)
Head at dx 1.5 mm: 25 full layers + a 0.25 mm top layer; N_head 213 048, top layer 7 876 particles, 1.1076e-6 m^3; V_head (particles)
8.76645e-5 m^3 against the glass's 8.85274e-5 m^3 between FILL and FILL + HEAD0: ratio 0.99025 (-0.975 %; predicted -0.96 %);
m_head0 0.0238351 kg.
Interior foam cells (19 371 cells, z range inside FILL .. FILL + 25 hl, centre > 2 dx inside the wall):
- with the seed's vertical jitter (0.3 of the layer, as now): mean 1.00012, each cell 0.5 .. 1.5 (std 0.148); layer means within 0.0055.
- without vertical jitter: every cell 1.0000000 (deviation 1e-16).
Marks: abs(V_cell / dx^3 - 1) < 1e-3: FAIL with the jitter (each cell 0.5; layer means 0.0055), PASS without it.
       V_head within 1e-6 of the glass volume: FAIL (0.99025).
Stout (unchanged, for comparison): Vp = V / N = 1.0112 x hl^2 hz, so interior stout cells hold 1.011 cell volumes on average (the
uniform V / N spreads the wall inset's 1 % deficit over every particle), layering 0.9980; i.e. the known -0.20 % is in fact about
+1.1 % net in the interior.
Both Part 1 marks fail as predicted before the run: the instruction's two requirements (interior cells at exactly one cell volume, and
the head's total equal to the glass volume) cannot both hold with particles kept 0.25 hl inside the wall and uniform volumes. Stopped
before Part 2 (no GPU launch): which normalisation to use is the owner's decision. The stale GPU session step4-pint-head-smoke still
returns an empty status (cannot tell whether it is gone).

## Owner, 21 Nov ~20:55 UTC: option 2
Each wall-ring head particle carries its true share, the strip between it and the wall in its own layer (per layer from the glass
radius), so the total matches the glass by construction. No vertical jitter for the head, sideways kept. New seed-check marks:
abs(V_cell / dx^3 - 1) < 1e-3 in interior foam cells (not cut by the wall or the stout-foam interface); wall-ring volume factor in
[1.0, 1.5] in every layer; total head volume against the glass FILL..FILL + HEAD0 within 1e-4. README stout note corrected (net +1.1 %
interior, harmless). Then rerun the seed check on CPU; if it passes, the single 4.4 GPU smoke once the queue is clear.
Code (20:56 UTC): seed_head v3 (ring = lattice points with a 4-neighbour outside the mask; factor = 1 + (V_layer_glass - n t hl^2) /
(n_ring t hl^2)); seed check v3 (glass volume integrated independently, 200 001 points).
- 21 Nov 20:57:17-20:59:11 UTC: seed check v3 (code 6ccb2d7a, CPU step4-seedcheck v3, 1 min 54 s). All marks PASS (Fact,
  notes/spill/step4/seedcheck.json; v2 outputs in seedcheck_v2/): interior foam cells (19 371) abs(V_cell / dx^3 - 1) max 1.8e-14;
  wall-ring factor 1.196 .. 1.345 in every layer (in [1.0, 1.5]); head volume 8.852745e-5 m^3 against the glass's 8.852745e-5 m^3
  integrated independently: ratio 1 - 2.6e-11 (mark 1e-4). N_head 213 048; ring 280-292 particles per layer; top layer 7 876 particles,
  0.25 mm, factor 1.288; m_head0 0.0240697 kg. (With a vertical jitter of 0.3 the per-cell mark would fail: 0.5 .. 1.5.)
  Next: the single 4.4 GPU smoke once the two stale queued runs are confirmed cancelled (the API cannot cancel or see them).
- 21 Nov ~20:53-20:55 UTC: one stale queued GPU run (step4-pint-head-smoke, latest version 2, code 853578c8: old head seed, no resort)
  started by itself and completed; GPU quota 300.3 s used (5.0 min of 1 800). Outputs kept in notes/spill/step4/stale_gpu_853578c/.
  Fact: 5 steps, it <= 269, res <= 9.62e-6, drain/phantom/in-solid 0, det 0.9999996 .. 1.0000005, books 0; stout mean height
  72.6948003 mm (CPU smoke 72.6948 mm), head 134.38436 mm; wall 35.23 s at step 1 (compile and set-up), then 0.34 s per step.
  Whether version 1 is still queued cannot be seen from the API. Waiting for the owner's confirmation before the new GPU smoke.
- 21 Nov 21:31:50-21:34:35 UTC: 4.4 GPU smoke (code 5074138e, Kaggle step4-pint-head-smoke v3, T4, 2 min 45 s, script 81 s).
  GPU 154.2 s = 2.6 min (quota 300.3 -> 454.5 s used; 1 792 min left until 28 Nov 00:00 UTC).
  Fact (notes/spill/step4/smoke_4p4_gpu.json): N 1 215 000 (stout 1 001 952, head 213 048, seed v3), m_head0 0.0240697 kg,
  V_head = glass volume (8.852745e-5 m^3). All marks PASS: finite; it <= 268, res <= 9.902e-6; drain bowl, phantom, in solid 0 from
  step 1 (260 at t = 0: the stout's seed jitter and the wall ring, moved out by step 1); max abs(det be - 1) 4.8e-7; books stout 0,
  head 1.9e-8 (constant from step 1: the head masses stored in float32 against m_head0 summed in float64), same across the resort;
  head mean height across the resort 134.61815 mm before and after (difference 0); parity with the CPU smoke: stout 7.1e-11 m (mark 1e-5),
  head +2.34e-4 m (mark 5e-4; the seed change alone, predicted about +0.35 mm). m_floor acted on at most 9 faces, all head faces
  (f_h > 0.5) (report, not a mark). Step times 36.57 s (set-up and compile), 0.36, 1.68 (with the resort), 0.22, 0.32 s.
  H_top at t = 0 reads 144.182 mm (4.4's mark: within 0.3 mm of 144 mm). No yielding (s_max 0.35 Pa).
  Estimates (Inference, 0.30 s a step without compile or resort): full 4.4, 1.0 s, about 1 304 steps: about 7 min of stepping, about
  8 GPU-min with set-up; full 4.5, 1.5 s, about 1 960 steps if speed does not cut dt: about 10 min stepping, 11-13 GPU-min.
  Waiting for the owner's yes before full 4.4.
- 21 Nov 21:37 UTC, owner, before any 4.4 number: the H_top mark is judged as drift, abs(H_top(t) - H_top(0)) < 3e-4 m (H_top(0) =
  144.182 mm carries a 0.18 mm offset of the surface finder, the level-set kernel); the absolute abs(H_top - 0.144 m) is reported too.
  The harness's summary has H_top0_mm and H_top1_mm; the drift mark is evaluated from them (and the per-step H_top_mm) in the report.
- 21 Nov 21:36:27 launch, 22:17:21 running (41 min in Kaggle's queue), 22:25:58 complete: full 4.4 (code 0da19017, step4-pint-head-rest,
  T4). Stepping 370 s, 0.284 s a step with the logging. GPU 511.7 s = 8.5 min (quota 966.2 s used; 1 784 min left).
## Test 4.4 results (Fact; notes/spill/step4/pint_head_rest_summary.json, pint_head_rest.jsonl)
1 305 steps to 1.0 s. n_drain_bowl 0 and n_phantom_out 0 every step PASS; it_max 542 < 600 PASS (1 304 regular steps <= 268);
res < 1e-5 every step FAIL: one step, the last (1 305), res 0.332 after 542 iterations, all other 1 304 steps < 1e-5.
That step has dt = 7.8e-6 s (the harness cuts the last step to land on 1.0 s: dt = min(..., T - t), rest_variants.py:650), 1 % of the
normal 7.67e-4 s. Inference: its pressure right-hand side is about 100 x smaller and the float32 conjugate gradient stops on
breakdown before reaching 1e-5 relative; a harness artefact, not a solver drift (nothing else moves at that step: vmax 3.3e-5 m/s).
stout mean height drift +1.03e-6 m < 5e-5 PASS; head mean height drift +5.3e-7 m < 1e-4 PASS; H_top drift (owner's rule, decided
before the numbers) max over the run 6.3e-7 m, end 6.3e-7 m < 3e-4 PASS; H_top absolute 144.1825 mm, abs(H_top - 0.144) 1.83e-4 m.
Books stout 0, head 1.9e-8 (float32 storage) PASS; real crossings 0, old crossings 0 PASS; in solid 0 PASS; ceiling 0.
No yielding (s_max 0.92 Pa, below tau_y 5.4 Pa); det be 0.9999996 .. 1.0000005; vmax 8.4e-4 m/s; ds/dx max 0.64 (step 1).
m_floor acted on at most 9 faces (head faces). Stopped for the owner: one mark fails on the harness's cut last step.

## Owner, 22 Nov ~00:20 UTC: 4.4 PASSES on its 1 304 full steps (option 1)
The cut step: step 1 305 of the full 4.4, dt 7.8e-6 s (1 % of 7.67e-4 s), made by the harness to land on T = 1.0 s
(dt = min(..., T - t), rest_variants.py:650 at 0da19017). Its right-hand side was about 100 x smaller while the warm start p_prev came
from a full step (the solver's p dt / rho scales with dt), so the float32 conjugate gradient broke down at 542 iterations, residual
0.332 relative. Not a solver drift: the 1 304 full steps all reached < 1e-5 with <= 268 iterations, and nothing moved at that step.
Rules from now on (owner): (1) every harness (4.5, the ride): never shorten dt to hit an end or frame time; take the frame at the first
step that reaches it and record its true time. Done: step4_run, step45_run (dt = min(2e-3, 0.8 dx / vmax, 0.40 dx / c_s)), and
make_advance(cut_to_frame=False by default; True only to rerun old figures bit for bit; advance already returns the true t).
(2) the pressure solver also stops when the absolute residual max |r| < atol: Stout.atol = 1e-10 (solver units m^2/s, b = -div dx).
Why 1e-10: a residual r leaves a cell's net outflow wrong by r / dx and its volume by r dt / dx^2 per step; at dx 1.5 mm, dt 7.67e-4 s,
1 300 steps a second, even with every cell erring the same way the pint's height would move 5.5 um per second, ten times below 4.4's
50 um mark. The step's diag now carries res (relative), res_abs, bnorm (max |b|) and conv = res < tol or res_abs < atol; marks use conv.
(Inference, untested: whether 1e-10 would have closed the cut step is unknown, its bnorm was not logged; the no-cut rule removes it.)
## Test 4.5 set-up (22 Nov, written before any run)
rest_variants.py STEP45=1: as 4.4, plus a half-sine push A sin(pi (t - t0) / tau) along x, A = 3.4 m/s^2, tau = 0.15 s, t0 = 0.05 s,
free to 1.5 s; ring 13's cos part of the top surface every step; fit (run_b fit_swing) over t0 + tau .. t0 + tau + 0.5 s (first three
half-cycles); marks f_d in [2.75, 3.15] Hz, zeta in [0.32, 0.52], books < 1e-6, 0 real crossings, 0 in solid from step 1; the peak
wall amplitude aimed at 8-12 mm is logged (set-up check, not a mark). Push sized (Inference): Step 3's 1 m/s^2 x 0.146 s gave 6.0 mm
(gain about 63 mm per m/s of the pulse's Fourier weight); half-sine 0.15 s at 3.0 Hz weighs 0.078 s per m/s^2; zeta 0.45 keeps about 0.6
of the undamped peak: A = 10 / (0.6 x 63 x 0.078) = 3.4 m/s^2, uncertain by about +-30 %. Prediction (Inference): the foam's top is
3.5 mm below the rim (144 vs 147.5 mm); a 10 mm swing will likely carry foam over the rim at the wall (logged as head_outside).
- 22 Nov 00:29:32-00:35:19 UTC: 4.5 CPU smoke (code 13c4c9f9, step4-slosh-head-cpu-smoke, 5 min 47 s). All smoke marks PASS: finite,
  all converged (it <= 268, res <= 9.997e-6), books 0 / 1.9e-8, in solid 0, real crossings 0, det within 4.8e-7; 31.7-67.2 s a step.
  Fact: at rest the absolute residual at the relative stop is 0.96-1.13e-10 (bnorm about 1.1e-5 m^2/s), i.e. at the floor atol 1e-10:
  the floor and the relative test coincide at rest; 1e-11 would act only on near-empty right-hand sides (option for the owner).
- 22 Nov 00:35:50 UTC: full 4.5 launched (T4, step4-slosh-head); quota before: 966.2 s used (1 784 min left); estimate 13-14 GPU-min.
- 22 Nov 00:35:50 launch, 00:36:02 running, 00:50:44 complete: full 4.5 (code 13c4c9f9, step4-slosh-head, T4, 14 min 54 s; stepping
  712 s, 0.364 s a step). GPU 857.9 s = 14.3 min (quota 1 824.1 s used; 1 770 min left until 28 Nov 00:00 UTC).
## Test 4.5 results (Fact; notes/spill/step4/slosh_head_summary.json, slosh_head.jsonl, slosh_head.log)
1 957 steps to 1.5008 s (no cut). Push 3.4 m/s^2 half-sine 0.15 s from 0.05 s; peak wall (ring 13) amplitude 11.74 mm (set-up window
8-12 mm: yes). Fit over the first three half-cycles (0.20-0.70 s): f_d 2.814 Hz (f0 2.831), zeta 0.111, A 11.66 mm, rms 0.14 mm.
Long fit 0.2-1.2 s: f_d 2.797 Hz, zeta 0.118. Zero crossings 0.304, 0.479, 0.660, 0.830, 1.028, 1.212 s.
Marks: f_d in [2.75, 3.15] PASS; zeta in [0.32, 0.52] FAIL (0.111); books stout 0, head 1.9e-8 PASS; real crossings 0 PASS; in solid 0
PASS. Also: all steps converged (it <= 268, res <= 9.9997e-6), ceiling 0, no head or stout over the rim (head_outside 0), vmax 0.25 m/s,
ds/dx <= 0.64, det be 0.999999 .. 1.0000007.
B.6 rule: zeta < 0.25 with 4.1-4.3 passing -> stop and report n_yielded, H_top and the wall dissipation; no parameter changed.
Time series (Fact): n_yielded 0 to 0.065 s; 6 177 at 0.08 s, 167 814 at 0.11 s, 207 431 at 0.14 s (of 213 048: nearly the whole head),
> 50 % of the head yielded in 57 % of the steps, 109 826 at 1.0 s, 3 655 at 1.4 s, 534 at 1.5 s. s_max up to 56.7 Pa (0.17 s) and 68.7 Pa
overall; gp_max up to 136 1/s. Median top surface H_top 143.91-144.90 mm (144.18 at rest). Wall dissipation (cumulative ewall):
0.302 mJ in 0.05-0.20 s, 0.621 mJ in 0.20-0.50 s, 0.283 mJ in 0.5-1.0 s, 0.032 mJ in 1.0-1.5 s; 1.240 mJ total. Mass floor active on up
to 4 266 faces during the motion (9 at rest).
Inference (not tested): the old model's 2.915 Hz / zeta 0.425 (cart4.py:77-78, "run 8's measured swing with the head (free_full_1.5,
ring 13)") came from model "full": the 2-D head sheet plus the skin (the surface that cannot stretch, a Stokes-layer stress on every top
liquid cell). Step 4 switches the skin off with head_mode "evp" (instruction B.3.10). The skin may be most of the old 0.425.

# Instruction "step4-close" (owner, 23 Nov 2026 ~08:40 UTC): fix the wall-friction dilution, rerun 4.5, write the handoff
Settled (reviewer, in code at 045fb72): friction_evp's lam = af / rho_f [...] decelerates a wall face as if it held a full cell; a cut
face holds M_f = alpha_open rho_f dx^3, so only alpha_open A tau is applied; the logged wall energy uses rho_f dx^3 too. The 4.5 damping
mark [0.32, 0.52] is withdrawn (built on PLANT_ZETA 0.425, a simulation number); new provisional range [0.13, 0.33] (derived, Neon).
Part A (audit, CPU, before any change): rest_variants.py STEP45_AUDIT=1 -> notes/spill/step4/diag_4p5_energy.json.
Part B code (23 Nov ~08:43 UTC, committed while the Part A audit runs from aa6d57b): friction_evp lambda = A_f / max(M_f, m_floor)
[(1 - f_h) rho g_s + f_h tau_w / max(|u|, 1e-4)], A_f = af dx^3; energy 0.5 M_f (u0^2 - u^2), split stout layer / head Cantat by their
parts of lambda (diag e_wall_stout, e_wall_foam); plastic dissipation diag e_plastic = sum over yielded head particles V_p s_new gp dt.
The non-evp friction path (Stout.friction, used in Steps 1-3) keeps the old per-full-cell convention: not changed now; open item for
the handoff. 4.5 harness: KE and PE with each particle's mass; fits over 0.2-1.2, 0.2-0.6, 0.6-1.2 s; energy closure 0.2-1.0 s; Part C
marks; smoke mark abs(A_applied_new / A_grid - 1) < 0.02 from wall_audit at t = 0.
- 23 Nov 08:42:38-08:46:23 UTC: Part A audit (code aa6d57b, CPU step4-wall-audit). Fact (diag_4p5_energy.json), band 125-143.75 mm, t = 0:
  A_geom 4.550e-3 m^2; u faces 1 790, A_grid 2.77e-3, A_applied 1.90e-3 (0.685), alpha_open mean 0.763 (0.128-1.141); v the same (0.684);
  w faces 1 848, A_grid 4.08e-3, A_applied 2.01e-3 (0.494), alpha_open mean 0.529 (0.075-1.085); m_floor on wall faces 4 / 4 / 1, on free
  faces 0. After one step the same. A_applied_new (fixed formula) = A_grid. Energy from the old slosh_head.jsonl at the swing's extremes
  (approximate PE from mean heights): per half-cycle dE_mech -0.326 / -0.153 / -0.080 / -0.035 mJ against logged ewall 0.222 / 0.128 /
  0.068 / 0.033 mJ.
- 23 Nov 08:46:55-08:54:02 UTC: Part B CPU smoke of 4.5 (code 5acb7181): all marks PASS: finite; it <= 268, res <= 9.73e-6; A_applied_new /
  A_grid = 1.000; books 0 / 1.9e-8; in solid 0. Energy logs live (E_wall_foam 1.3e-11 J, E_wall_stout 8.5e-14 J at rest; E_plastic 0).
- 23 Nov 08:55:42 UTC: Part C launched: Kaggle numakoudsie/step4-slosh-head version 2 (T4, code 5acb7181, launcher l45g.py in the
  session scratchpad). Quota before: 1 824 s used of 108 000 s. Queued (empty status) at least until 09:25 UTC.
- 23 Nov 13:56 UTC: the Part C run is still queued after 5 h (status empty, no session output, no GPU time used). Not relaunched or
  cancelled; that is the owner's call (the API cannot cancel).
- 23 Nov 16:38 UTC: the Part C run (v2) was cancelled from outside this session after 7.7 h queued, never started (status
  CANCEL_REQUESTED 16:38:11, CANCEL_ACKNOWLEDGED 16:38:14; no outputs, no GPU time). Not relaunched; waiting for the owner.
- 23 Nov 17:39:31 UTC (coordinator instruction 0001, notes/coord/to-session/): 4.5 relaunched as a NEW notebook
  numakoudsie/step4-slosh-head-offline v1, internet OFF, T4, with stout_jax.py, rest_variants.py, run_b.py and guinness-glass.js
  embedded in the notebook text at commit 5acb7181 (checked byte-identical before launch). No downloads, no pip.
- STANDING RULE (coordinator, 23 Nov): every GPU launch uses internet OFF with the code embedded in the notebook. Kaggle queues
  internet-on GPU runs indefinitely on this account; queued runs hold the 2 batch GPU slots. If a run has not started within 5 min, stop
  and report. The coordinator channel is notes/coord/ (rules in to-session/0000-channel-rules.md; reports go to to-coordinator/).
- 23 Nov 19:18 UTC (instruction 0002, new code session): quota 1 840 s used of 108 000 s. step4-slosh-head-offline is at v2 with
  source "__SRC__" (coordinator's broken save, 19:06 UTC); status empty (queued). v1's source cannot be read back, so the launcher was
  rebuilt as tools/spill/build_l45_offline.py (four files at 5acb7181, checked byte-identical).
- 23 Nov 19:19:31 UTC: SaveKernel for v3 refused: "Maximum batch GPU session count of 2 reached." Not launched, 0 GPU-s.
  Inference: queued v1 and v2 hold both slots. Report notes/coord/to-coordinator/0002-report.md; the owner must stop them in the browser.
- 23 Nov 19:25-19:27 UTC: v3 GPU pushes refused twice more (same error); a CPU no-op version (v3, enableGpu false) ran at once
  (RUNNING 19:27:10, COMPLETE 19:27:25), so only GPU launches were blocked.
- RULE (instruction 0003, 23 Nov 19:50 UTC): GPU launches set enableGpu only, never a machine shape or accelerator field. Every 4.5
  GPU launch so far named NvidiaTeslaT4 and sat queued; another project saw the same and a push without the field started in 20 s
  (github.com/mitishraina/AutoTuneNet/pull/60). The owner cancelled the queued v1 and v2. Rule 7 of the code handoff updated.
- 23 Nov 19:51:55 UTC (instruction 0003): 4.5 Part C pushed as v4 with enableGpu only (no machine shape): accepted at once, RUNNING
  19:52:26, COMPLETE 20:05:35 UTC (code 5acb7181, cuda:0 on Kaggle's T4 shape). GPU 753.8 s (quota 2 593.9 s used).
## Test 4.5 Part C results (Fact; notes/spill/step4/slosh_head_fix_summary.json, slosh_head_fix.jsonl, slosh_head_fix.log)
1 957 steps to 1.5008 s. f_d 2.815 Hz PASS; zeta 0.2-1.2 s 0.143 PASS (in [0.13, 0.33]); zeta 0.6-1.2 s 0.183 > 0.2-0.6 s 0.132 PASS;
energy closure 0.2-1.0 s +0.514 FAIL (sinks 1.908 mJ vs -dE_mech 1.260 mJ; E_plastic 1.580, E_wall_foam 0.313, E_wall_stout 0.014 mJ);
sinks <= loss within 2 % FAIL; books 0 / 1.86e-8, real crossings 0, in solid 0, it max 268, all converged PASS. Peak wall 11.32 mm.
Inference: E_plastic alone exceeds the mechanical loss: overcount (s, gp convention) or missing elastic store. Stopped; nothing tuned.
