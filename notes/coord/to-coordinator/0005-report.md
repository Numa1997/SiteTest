# 0005 report: done. enable_ls_extend fixed (49839c5), identity bit for bit at 1.5 mm, full 0004 audit run; results in 0004-report.md

23 Nov 2026, 22:27 UTC. GPU 0 s. Kaggle CPU step4-energy-audit-cpu: v3 smoke 21:24:35-21:33:47 UTC, v4 full 21:34:12-22:16:24 UTC.
- Fix (Fact): stout_jax.py:827, the right side indexed by [new]; recorded in STATE-projection-fix.md as a pre-existing bug fix.
- Identity (Fact, full_v4/default_path_identity.json and smoke_v3/): 5acb718 vs current at 1.5 mm, 3 steps, all state arrays identical bit
  for bit; motion identical with audit on. PASS.
- All 0004 marks, numbers and the candidates proved or refuted: notes/coord/to-coordinator/0004-report.md (top section).
- Stopped, as instructed. Nothing tuned, no fix applied beyond the one line.
