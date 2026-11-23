# 0001 report: 4.5 relaunched with internet OFF; NOT STARTED after 5 minutes, stopped as instructed

23 Nov 2026, 17:45 UTC. Branch claude/guinness-projection-fix.

## Done (Fact)
- Notebook `numakoudsie/step4-slosh-head-offline` v1, saved 17:39:31 UTC. GetKernel reads back: enableInternet false, enableGpu
  true, machineShape NvidiaTeslaT4.
- Code embedded in the notebook text (zlib + base64), at commit 5acb7181643f01d86d6aa0c71e5a85d194a840bf:
  tools/fig12/kaggle/stout_jax.py, tools/spill/rest_variants.py, tools/fig12/kaggle/run_b.py (4.5 reads its fit_swing as text),
  public/scripts/guinness-glass.js (the glass profile). Each decoded file checked byte-identical to `git show 5acb718:<file>` before
  launch. No downloads, no pip. Env: STEP45=1, SUBRUN=full, DX=0.0015.
- Status polled every 30 s: empty (queued) from 17:39:38 to 17:44:47 UTC. Monitor stopped at 17:44:43 with "NOT STARTED after 5 min".
- GPU used: 0 s. Quota before: 1 824 s used of 108 000 s (reset 28 Nov 00:00 UTC).
- Other notebooks at 17:44:47 UTC: step4-slosh-head = CANCEL_ACKNOWLEDGED; step4-slosh-head-r = empty status (queued, or never ran).
- State file updated with the internet-off rule (commit 721d9bc).

## Inference
- Internet off was not enough this time. One likely cause: step4-slosh-head-r is still queued and holds one of the 2 batch GPU slots
  (0001 says it may), and the offline run waits on the other slot. I cannot see slots or cancel runs from the API.

## Not done
- No result for 4.5, so no Part C marks and no Part D.
- step4-slosh-head-offline v1 is left as it is (still queued). It is not cancelled: the API cannot cancel.

## Needs the owner
- Look at Kaggle, Your Work, Active Events: cancel `step4-slosh-head-r` if it is queued, and decide whether to keep
  `step4-slosh-head-offline` v1 queued (it will start by itself when a slot frees) or cancel it so this session relaunches it.
