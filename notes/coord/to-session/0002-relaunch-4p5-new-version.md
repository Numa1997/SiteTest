# 0002: run test 4.5 Part C as a new version of `step4-slosh-head-offline` (from the coordinator, 23 Nov 2026, 19:05 UTC)

## Facts (checked today)
- The owner looked at Kaggle: nothing is running on the account.
- `numakoudsie/step4-slosh-head-offline` v1 page shows "Queued...", 0 B output, saved 17:39 UTC, never started. The
  connector returns an empty status for it.
- GPU quota at 18:45 UTC: 1 840 s used of 108 000 s, reset 28 Nov 00:00 UTC.
- Branch head before this file: b2558f9.

## Do this
1. Read the quota fresh and state the GPU cost in one line.
2. Push a new version (v2) of the same notebook `step4-slosh-head-offline`. Do not create a new notebook. Same content as
   v1: internet OFF, GPU T4, code embedded at commit 5acb718 and checked byte-identical, STEP45=1, SUBRUN=full, DX=0.0015.
3. Poll the status every 30 s for 5 minutes, with UTC times. If it has not started by then, stop and report; do not wait.
4. When it finishes: download the outputs, commit them under `notes/spill/step4/`, update `STATE-projection-fix.md`, and
   report every Part C mark (code handoff section 5) as PASS or FAIL with its number. Marks are fixed; tune nothing. If
   zeta is below 0.13 while energy closure passes, stop and report.
5. If every mark passes, do Part D: write `notes/spill/HANDOFF-step5.md`.
6. Limit: 60 GPU-minutes.

## Clean up (owner's standing rule)
Delete whatever this instruction creates once it is no longer needed: scratch files, temporary branches, smoke versions.
Keep the notebook until 4.5 has a committed result. In the report, list what was deleted, what was kept and why; any
Kaggle deletion goes under "Needs the owner".

## Report
`notes/coord/to-coordinator/0002-report.md`, committed and pushed.
