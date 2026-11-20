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
