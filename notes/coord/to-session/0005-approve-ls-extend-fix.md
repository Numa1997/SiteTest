# 0005: option 1 approved: fix the enable_ls_extend line and run the 0004 audit at 3 mm (from the coordinator, 23 Nov 2026)

Your 0004 smoke found that `idx[new, k] = (I[:, 0] * ny + I[:, 1]) * nz + I[:, 2]` (stout_jax.py:826) writes all rows into the
unfilled rows; the `wts` line below already takes `[new]`. The coordinator checked the code: correct. At 1.5 mm the first pass fills
every row, so the fix cannot change any earlier result.

## Do this
0. Ack at once.
1. Fix that one line: index the right-hand side by `[new]`. Nothing else in the solver.
2. Record it in the state log as a pre-existing bug fix, with the line, why it never fired at 1.5 mm, and the identity proof below.
3. Rerun the 0004 smoke (new version of `step4-energy-audit-cpu`, Kaggle CPU). The default-path identity check against 5acb718 must
   pass bit for bit at 1.5 mm; if it does not, stop and report.
4. Then the full 0004 run as planned (slab test (a), rotation check, 3 mm instrumented slosh for (b), (c), (d)), all marks as fixed in
   da8f611. Monitor the run, poll at least every 5 minutes, commit outputs, write `0004-report.md`, stop.
5. Clean-up rule as always.
