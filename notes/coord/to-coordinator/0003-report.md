# 0003 report: 4.5 Part C RAN. f_d and zeta PASS; energy closure FAILS (sinks 51 % above the mechanical loss). Stopped, nothing tuned.

23 Nov 2026, 20:10 UTC. Branch claude/guinness-projection-fix.

## Launch (Fact)
- Quota before: 1 840.149 s used of 108 000 s. Cost line: about 15 GPU-min, limit 60.
- 19:51:55 UTC push of v4 of `step4-slosh-head-offline` with enableGpu true, enableInternet false, NO machineShape field: accepted
  at the first try. Built by tools/spill/build_l45_offline.py at 5acb7181 (four files byte-identical; sha256 printed again on Kaggle,
  same). Kaggle filled in machine_shape NvidiaTeslaT4 by itself. RUNNING at 19:52:26 UTC (31 s), COMPLETE at 20:05:35 UTC.
- GPU: JAX device cuda:0 on Kaggle's T4 shape; the log does not name the card. GPU used 753.8 s = 12.6 min (quota after 2 593.9 s).
- Run: 1 957 steps to 1.5008 s, never cut; stepping 660 s, 0.337 s a step.
- Outputs, under new names so the 22 Nov (pre-fix) files stay: notes/spill/step4/slosh_head_fix.jsonl, slosh_head_fix_summary.json,
  slosh_head_fix.log, slosh_head_fix_kaggle_log.json.

## Part C marks (Fact, slosh_head_fix_summary.json; marks fixed before the run)
| mark | number | result |
| f_d over 0.2-1.2 s in [2.70, 3.15] Hz | 2.815 Hz | PASS |
| zeta over 0.2-1.2 s in [0.13, 0.33] (derived, provisional) | 0.143 | PASS |
| zeta 0.6-1.2 s greater than zeta 0.2-0.6 s | 0.183 > 0.132 | PASS |
| energy closure 0.2-1.0 s: abs(sinks / (-dE_mech) - 1) < 0.25 | +0.514 | FAIL |
| -dE_mech >= sinks within 2 % | sinks = 1.514 x (-dE_mech) | FAIL |
| books < 1e-6 | stout 0, head 1.86e-8 | PASS |
| real crossings 0 | 0 | PASS |
| in solid 0 from step 1 | 0 | PASS |
| it < 600 | 268 | PASS |
| converged (res < 1e-5 or below the floor) | all steps, res max 9.9994e-6 | PASS |
Set-up check (not a mark): peak wall amplitude 11.32 mm, inside 8-12 mm.
Energy 0.2-1.0 s: -dE_mech 1.260 mJ; E_wall_foam 0.313 mJ, E_plastic 1.580 mJ, E_wall_stout 0.014 mJ; sinks 1.908 mJ.
Against 22 Nov (before the friction fix): zeta 0.118 -> 0.143 over 0.2-1.2 s; f_d 2.797 -> 2.815 Hz. Head and stout stayed in the glass.

## Inference (not tested)
- The plastic term alone (1.580 mJ) is larger than the whole mechanical loss (1.260 mJ). Energy cannot be dissipated that was never
  there, so either E_plastic is overcounted or a store is missing from E_mech. Two candidates: (a) a convention factor in
  e_plastic = sum V_p s gp dt (s and gp must be a work-conjugate pair, e.g. s = sqrt(tau:tau / 2) with gp = sqrt(2 D_p:D_p); a
  mismatch gives a factor 2 or sqrt 2); (b) the foam's stored elastic energy is not in E_mech; at most about 0.4 mJ (s up to ~50 Pa,
  G 166 Pa, head volume 8.9e-5 m^3), not enough alone for 0.65 mJ.
- The damping marks pass, so the fix moved zeta into the derived range; the energy books are what is in question, not the motion.

## Not done
- Part D (HANDOFF-step5.md): not written, because not every mark passes.
- Nothing tuned or rerun.

## Needs the owner
- Decide the next step on the energy closure: audit the e_plastic convention and the elastic store on CPU (no GPU), or accept
  closure as a raw number. Marks stay as they are.

## Clean up
- Deleted: scratch save/cpu/out JSON files in the session scratchpad.
- Kept: notebook step4-slosh-head-offline (latest version is this run; needed until the closure question is settled); the 22 Nov
  slosh_head* files (old result, kept until the new one is accepted).

Where we are: 4.5 Part C ran; f_d and zeta pass, energy closure fails; superseded by the 0004 audit.
Next, if you say yes: nothing further under 0003; see 0004.
