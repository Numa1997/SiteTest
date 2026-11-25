# 0007 report: blocks 1-4 pasted verbatim, commit 2f7615f

25 Nov 2026 (UTC). Nothing run; no code written.
- Block 1: tools/fig12/kaggle/stout_jax.py, module function evp_return_map (old lines 127-157) replaced; now at line 127.
- Block 2: tools/fig12/kaggle/stout_jax.py, new method Stout.evp_grad inserted directly above Stout.step (line 1387).
- Block 3: tools/fig12/kaggle/stout_jax.py, Stout.step (old lines 1382-1462, ending "return s, diag") replaced; now at line 1401.
- Block 4: tools/spill/audit_0004.py replaced whole.
- Check (Fact): each pasted region compared with the instruction's block by diff: identical, all four. Old text was where the blocks said.

Where we are: the fix is in the repository behind the flags evp_consistent and evp_hw (default off), at 2f7615f; the coordinator launches the test.
Next, if you say yes: commit the test's outputs when they come back, and report.
