# 0002 report: v3 NOT launched; Kaggle refused, "Maximum batch GPU session count of 2 reached"

23 Nov 2026, 19:20 UTC. Branch claude/guinness-projection-fix (head a326275 when read, ack eb143b1).

## Done (Fact)
- Quota read 19:18 UTC (get_accelerator_quota): GPU 1 840.149 s used of 108 000 s, 0 s reserved, reset 28 Nov 00:00 UTC.
- Notebook `numakoudsie/step4-slosh-head-offline` (GetKernel): current_version_number 2, source "__SRC__" (the broken v2),
  enable_internet false, enable_gpu true, NvidiaTeslaT4. Session status: empty (queued). v1's source cannot be read back
  (GetKernel with versionLabel 1: "Not found").
- v3 source rebuilt by the new tools/spill/build_l45_offline.py (the old launcher was in a lost scratchpad): stout_jax.py,
  rest_variants.py, run_b.py, guinness-glass.js embedded (zlib + base64) at 5acb7181643f01d86d6aa0c71e5a85d194a840bf, each decoded
  file checked byte-identical to `git show 5acb718:<file>`; 8375a2f is an ancestor of 5acb718. 97 844 bytes. Env STEP45=1,
  SUBRUN=full, DX=0.0015. No downloads, no pip.
- Cost line before launch: about 15 GPU-min (4.5 v1 on 22 Nov used 858 s), well inside the 60 GPU-min limit.
- 19:19:31 UTC, SaveKernel (slug numakoudsie/step4-slosh-head-offline, GPU T4, internet off) answered:
  {"error":"Maximum batch GPU session count of 2 reached."}. No version 3 was created; 0 GPU-s used.

## Inference
- The two batch GPU slots are held by the two queued versions of this notebook: v1 (queued since 17:39 UTC) and v2 (the
  "__SRC__" version saved 19:06 UTC). The owner sees "nothing running" because queued sessions do not show as running.
- If v2 ever starts it fails at once (NameError on __SRC__) and frees its slot; v1 would run the correct code (it is the same
  code as v3), so if v1 starts on its own, Part C runs anyway.

## Not done
- No 4.5 result, so no Part C marks and no Part D.
- No polling: nothing was launched.

## Needs the owner
- In Kaggle, Your Work, View Active Events: stop BOTH queued sessions of `step4-slosh-head-offline` (v1 and v2). Then this
  session relaunches it as a new version (source ready, rebuilt by `python3 tools/spill/build_l45_offline.py OUT.py`), and
  watches it for 5 minutes. Alternative: stop only v2 and leave v1 queued, since v1 carries the right code.

## Clean up
- Deleted: the scratch files save.json and l45check.py in the session scratchpad.
- Kept: the notebook (4.5 has no result yet); tools/spill/build_l45_offline.py in the repo (it is how the launch is reproduced).
