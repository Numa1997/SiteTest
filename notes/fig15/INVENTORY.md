# Fig. 15 (resonant tunnelling): inventory of everything, 13–15 November 2026

Everything every session produced for Fig. 15, with what is wrong in it. Written 15 Nov at the owner's order; no computation was run to
write it (counts are read from files already in the repository or from Kaggle's own listings). Companion files:
`CORRECTION_LOG.md` (the correction session, every mistake), `HISTORY_COMMITS.txt` (all 114 commits, one per line, with session id).

## 1. The sessions

Fact (`HISTORY_COMMITS.txt`, `Claude-Session` trailers; 114 commits on Fig. 15 paths, 20 on 13 Nov, 92 on 14 Nov, 2+ on 15 Nov):

| Session | Commits | Work |
|---|---|---|
| session_01DGmqiodVZQkg4UwuNJqcxS | 3 | 13 Nov: the brief and lessons for Fig. 15 (`BRIEF.md`, `LESSONS.md`) |
| session_01DGmqimPtCe2EEcSkNkjwPC | 33 | 13–14 Nov: page, lecture note, generation 1 (rt3d) and generation 2 (rt3d2) on Kaggle, filing, R2 |
| session_01DGmqiojNWvbk4vZik2e4oW | 10 | 14 Nov: coordination, audits, derivation checks of the note |
| session_01DGmqiqazJ9UxECtFYiespR | 12 | 14 Nov: the first correction session (exact walls on CPU, 2D solver draft, wall T for all 1,088) |
| session_01DGmqiqhCMW3FREtBievpnu | 25+ | 14–15 Nov: this correction session (see `CORRECTION_LOG.md`) |
| (no trailer) | 31 | commits written without the session line |

## 2. The generations and what is wrong with them

| Generation | Runs | Where | GPU | State |
|---|---|---|---|---|
| 2026-11-13 "rt3d" | 115 | `public/data/resonant-tunnelling/2026-11-13/` | Fact: 2,493 s of per-run time (sum of `wall` in its index) | filed; superseded |
| 2026-11-14 "rt3d2" | 3,697 (1,088 walls, 2,327 discs, 282 shells) | index in repo; 6.53 GB of files in R2 `phyein-usul-runs/resonant-tunnelling/2026-11-14/runs/` | Fact: 128,155 s = 35.6 h of per-run time (sum of `wall`; two runs at a time per notebook) | **live on the page since 14 Nov 10:04, and wrong** |
| 2026-11-15 (corrected) | 0 filed | new files only inside Kaggle notebook outputs | see `CORRECTION_LOG.md` | **never filed** |

What is wrong with the live generation 2 (all measured, handles in the brief and in `correction/`):
- D1: barriers sampled on the 0.5 a grid; a 1 a barrier is 2 points, so resonances sit in the wrong place.
- D2: the side border absorbs the trapped wave; lifetimes too short.
- D4: norm lost from t = 0 (0.46 % by t = 90); cause unknown.
- D5: the sin^(1/8) border reflects, more for smaller dt.
- Fact (`correction/walls_T.json`, reproduced by the GPU walls to 6.8e-7): **918 of 1,088 stored walls fail** the gate
  |T − T_exact| ≤ max(0.005, 1 % T). Fact (`correction/classify_2d/classify_2d_summary.json`): **1,582 of 2,327 stored discs fail**
  against the (x, rho) recompute; median error 0.0128, largest 0.438. The 282 stored shells were never compared correctly (§4).

## 3. Code, by role

`tools/kaggle/resonant-tunnelling/` (generation 1 and 2; 34 files):
- solvers: `rt3d.py` (gen 1), `rt3d2.py` (gen 2, 3D Strang split-step, complex64, the source of D1–D5), `cn.py`, `check_cn.py`,
  `exact1d.py`, `tm.py` (transfer matrices), `iv.py` (diode current), `recon.py`, `real_units.py`, `b1_first.py`, `b1_survey.py`,
  `extract_t.py`, `pack.py`;
- runners and loaders: `rt3d_run.py`, `rt3d2_run.py`, `build_rt3d.py`, `build_rt3d2.py`, the notebooks `rt3d_*.ipynb`,
  `rt3d2_*.ipynb`;
- filers and reader: `file_rt3d.py`, `file_rt3d2.py`, `read_rt3d.py`.

`tools/kaggle/resonant-tunnelling/correction/` (22 files):
- exact walls: `exact_wall.py` (reference), `exact_wall_jax.py` (JAX), `wall_gpu_run.py` (batched GPU runner, tracker, calibration),
  `rebuild_wall.py` (RT3C writer), `rebuild_walls_all.py` (CPU batch, stopped at 488), `wall_T_all.py`, `wall_curves.py`,
  `wall_proof.py`, `walls_all.json`, `walls_left.json`, `walls_gpu.ipynb`, `walls_gpu.ipynb.tmpl`;
- (x, rho) discs and shells: `axisym.py`, `axisym_jax.py`, `rt2d_run.py`, `rt2d_smoke.py`, `rt2d_shellconv.py`, `build_rt2d.py`,
  `make_jobs_2d.py`, `jobs_2d.json`;
- comparison and filing: `classify_2d.py` (run), `file_corrected.py` (written, **never run**).

Bugs found in this code during the correction session (all fixed on the branch, each one cost a Kaggle run):
`axisym_jax.py` dtype carry (crash, 17ffd02); `rt2d_run.py` dropped the loader's grid (141 shells on the wrong grid, 07ac9bf);
`file_corrected.shell_T_old` blocked by the site with HTTP 403 (a7cf734); `classify_2d.py` unset status (b9ccf3a).

## 4. Data, by file

In the repository (`notes/fig15/correction/`):
- `walls_T.json` (exact T for 1,088 walls, CPU, first correction session); `walls_rebuild.jsonl` (curve gates of 488 CPU walls; their
  files were not kept).
- `walls_runs.jsonl` (1,088 GPU walls: T_ref, T_w, carried, closure, SHA-256 of each new file), `walls_summary.json` (13 identical
  group checks).
- `rt2d_runs/discs_*-of-4.jsonl` (2,327 discs), `rt2d_runs/shells-*-of-2.jsonl` (282 shells): T_ref, T_unc, drift, steps, SHA-256.
- `classify_2d/` (every disc and shell: T_old, T_ref, error, gate, status; and the 2,064-job recompute list).
- `kaggle_outputs/<notebook>/` (every small output of this session's notebooks: progress logs, summaries, timings, smoke and
  convergence records, Kaggle's own run log).

Known defects in this data:
- Shells: the "T_old" used for stored shells (P outside the sphere / P in the box) counts the reflected wave too, so the
  "282 fail" in `classify_2d` means nothing. The stored index never had a shell transmission number.
- Discs and shells: computed in complex64; norm drift 0.2–0.4 % (brief limit 0.1 %). Measured gap to complex128 on T: discs ≤ 6e-4,
  one shell 0.0012 (0.627703 vs 0.628891, `kaggle_outputs/2d-shellconv/progress.log`).
- Shells: T_unc (the undecided share split half and half) is 0.004–0.05 per shell.
- The new RT3C files (≈5.9 GB) exist only in the Kaggle outputs: `fig15-correction-walls-gpu` (walls.tar 1,275 MB),
  `fig15-correction-2d-1..4-of-4` (≈1,075 MB each), `fig15-correction-2d-shells-1-of-2` v2 and `-2-of-2` (≈220 MB each).

## 5. Kaggle notebooks (all private, account numakoudsie; Fact: `search_notebooks`, 15 Nov)

Generation 1 (13 Nov): `fig15-rt3d-smoke`, `fig15-rt3d-shard-1..4-of-4`, `fig15-rt3d-singles-v2`.
Generation 2 (13–14 Nov): `fig15-rt3d2-smoke`, `fig15-rt3d2-shard-1..6-of-6`, `fig15-rt3d2-fix1`.
First correction session (14 Nov): `fig15-correction-walls-exact` (stopped by the owner).
This correction session (14–15 Nov): `fig15-correction-walls-gpu` (v1 never started, v2 all walls), `fig15-correction-walls-calib`
(v1 no readable output, v2 never ran, v3 calibration), `fig15-correction-2d-smoke` (v1 crashed, v2 complete),
`fig15-correction-2d-1..4-of-4`, `fig15-correction-2d-shellconv`, `fig15-correction-2d-shells-1-of-2` (v1 wrong grid, v2 good),
`fig15-correction-2d-shells-2-of-2`, `fig15-correction-classify-2d` (CPU; v1 HTTP 403, v2 complete).

## 6. Money and GPU, as far as it can be counted

- Kaggle GPU quota (30 h a week): Fact, 48,167 s used at 13:10 14 Nov, 85,460 s at 00:15 15 Nov; the counter covers every notebook
  on the account (other figures ran in the same hours) and cannot be split per notebook.
- Generation 2 alone: Fact, 35.6 h of per-run GPU time (sum over its index).
- R2: Fact, 6.53 GB stored (free tier 10 GB); nothing was added by the correction.
- Claude usage (tokens, plan): not visible to me; I cannot give a figure.

## 7. Where Fig. 15 stands

The page still plays generation 2, which is wrong for most walls and most discs. Correct replacements exist for all 1,088 walls (exact)
and, in complex64, for all 2,327 discs and 282 shells, but none is filed, uploaded or shown. Nothing on `main`, the live site, the
Workers or R2 was changed by the correction sessions.
