# Open problems of the Guinness rebuild (Fig. 12, Fig. 16): this session's state

Session: session_01DGmqipAnEdVvBLCf7CLGmT, started 18 November 2026. Branch: `claude/guinness-open-problems` (from main 81e6fe2).
Reread this file first after any compaction. Brief: `notes/guinness-rebuild/HANDOFF-open-problems.md` (read whole).

## Aim
Close the six open problems of the handoff, one at a time, in its order. Merge finished work to main; verify live with curl.

## Binding rules (owner)
- Nothing runs in this container: no python, node, npm, browsers, agents. Read, edit, git, curl downloads, Kaggle tools only.
  Every computation, build, check or browser test runs in a Kaggle notebook on the owner's account; download outputs and commit them.
- CPU work on Kaggle: no need to ask. A new GPU run: state it to the owner in one line with its cost first.
- Never touch the Workers, R2, public/de/, public/ar/, scripts/i18n/, *.rtl.css. No model names in commits. Never write the owner's name.
- Reports: short turns, metric units, Fact (with handle) / Inference / Opinion, mechanism in one line,
  end with "Where we are:" and "Next, if you say yes:".

## Problems (status)
1. inventory --check and docs/files.md — IN PROGRESS. The rules for diag_burst.py, damping_grid.py, check_pint3d.cjs exist
   (tools/inventory.py lines 85-90). Plan: CPU notebook git-clones main, runs `tools/inventory.py --check`; on failure runs it
   without --check and returns docs/files.md.
2. Fig. 16 data panel with the three-way proof — open.
3. Fig. 16's own Kaggle dataset — open.
4. 3D close-up smoothness on a Kaggle GPU machine — open.
5. Fig. 12 bare swing at 1.0 mm — optional; GPU (~10 min): ask the owner first.
6. Fig. 12 lecture note to STANDARD.md — only if the owner wants it.

## Kaggle runs of this session
- CPU `numakoudsie/fig-16-cart-diagnostics-cpu` version 9 (18 Nov): git clone of this branch, `inventory.py --check`, then regenerate;
  outputs inventory.log, files.md. Status: RUNNING at launch; fetch, review the diff, commit docs/files.md.

## Commits
- this file.
