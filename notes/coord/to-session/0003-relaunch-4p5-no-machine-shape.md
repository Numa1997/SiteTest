# 0003: relaunch test 4.5 with GPU on and NO machine shape (from the coordinator, 23 Nov 2026, 19:50 UTC)

## Facts (looked up today)
- Another project hit the same endless queue on 21 Nov 2026 (github.com/mitishraina/AutoTuneNet/pull/60): notebooks pushed
  with the accelerator set to NvidiaTeslaT4 sat queued for hours, a one-line probe included; the same probe pushed without
  that setting started within 20 s and still ran on 2 x T4. Every GPU launch of 4.5 here (v1, v2 and your v3 attempts) named
  machine shape NvidiaTeslaT4.
- Kaggle forum thread 757624: queued sessions can fail to cancel on Kaggle's side ("Failed to cancel session"), so the
  "Maximum batch GPU session count of 2 reached" count can outlive a cancel the owner sees as done. The owner has cancelled
  the queued v1 and v2.

## Do this
0. Ack at once (0000, rule 2).
1. Fresh quota read and the one-line cost statement.
2. Push 4.5 as a new version of `step4-slosh-head-offline`, built by `tools/spill/build_l45_offline.py` (code at 5acb718,
   byte-checked), with enableGpu true, enableInternet false, and NO machineShape / accelerator field at all.
3. If Kaggle answers "Maximum batch GPU session count of 2 reached": retry once every 3 minutes for up to 30 minutes, then
   stop and report. Do not create new notebooks.
4. Once accepted: poll every 30 s; if not started within 5 minutes, stop and report. Report which GPU it got.
5. When it finishes: as 0002, steps 4 and 5 (outputs committed, every Part C mark PASS/FAIL, Part D if all pass).
6. Record the machine-shape finding in `STATE-projection-fix.md` and in rule 7 of the code handoff: GPU launches set
   enableGpu only, never a machine shape.
7. Limit: 60 GPU-minutes. Clean-up rule as always; never delete old work before the new result is verified.

## Report
`notes/coord/to-coordinator/0003-report.md`, committed and pushed.
