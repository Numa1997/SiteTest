# 0001: relaunch test 4.5 with internet OFF (from the coordinator, 23 Nov 2026, 17:30 UTC)

## Facts (tested on this Kaggle account today)
- GPU runs with internet ON stay "Queued" and never start: step4-slosh-head v2 (8 h), v3, a fresh notebook, and a 3-line probe.
- GPU runs with internet OFF start at once: a probe got 2 x T4 and finished in under 1 minute, twice.
- Queued runs hold the account's 2 batch GPU slots ("Maximum batch GPU session count of 2 reached").
- step4-slosh-head v2 and v3 are cancelled. `step4-slosh-head-r` (the coordinator's relaunch) may still be queued and hold one slot; one slot is free.

## Do this
1. Relaunch test 4.5 at commit 5acb718 as a new notebook with internet OFF. Put stout_jax.py, rest_variants.py and every
   file they import inside the notebook text itself. No downloads, no pip.
2. If it has not started within 5 minutes, stop and report. Do not wait for hours.
3. When it finishes: report every Part C mark as PASS or FAIL, then go on to Part D (the handoff file) if all pass.
4. From now on every GPU launch uses internet OFF with embedded code. Record this in the state file and the handoff.
