# Kaggle notebook outputs (read 14 November 2026, read-only)

Source: `list_notebook_session_output` per notebook (current version only), file counts from the listing, sizes and run counts from
each notebook's own run log (the listing gives no file sizes). "session" is the last log time of the notebook run in seconds.
The listing is capped at 500 files per page; a `next_page_token` marks a longer list.

## Fig. 14 (generation 2026-11-12 and 2026-11-13)

| Notebook (current version) | Output files | Stored (log) | Runs | Session |
|---|---|---|---|---|
| schrodinger-sphere-full-grid (v1, GPU x2) | 412: `runs/` 405 JSON + index, pack.py, panel_template.html, solver.py, timing.json, preview html | 159 MB | 405 | 926 s |
| schrodinger-sphere-3d-generation (v1, GPU x2) | 85: `2026-11-12/runs3d/` 81 .bin + index, timing, progress.log, solver.py | 60 MB | 81 | 237 s |
| schrodinger-sphere-3d-wave (v1, GPU x2) | 84: `2026-11-12/wave3d/` 81 .bin + index, progress.log, solver.py | 101 MB | 81 | 260 s |
| schrodinger-flat-wall (v1, CPU) | >500 (page full): `2026-11-12/flat/*.bin` | 51.9 MB | 585 | 834 s |
| schrodinger-pillar (v1, CPU) | >500: `2026-11-12/pillar/*.bin` + index, gz.bin | 106.2 MB | 585 | 1739 s |
| schrodinger-spherical-wave (v1, CPU) | >500: `2026-11-12/radial/*.bin` + index | 7.5 MB | 1170 | 1521 s |
| schrodinger-shapes-3d (v2, GPU x2) | 12: `2026-11-13/shapes3d/` six tars (sphere 9.1, coin 7.2, tube 6.7, soff 9.0, sslab 8.4, spil 78.1 MB), index.json, runs.jsonl, timing.json, progress.log, run script, solver3d.py | 118.5 MB | 243 | 1227 s |
| schrodinger-shapes-3d-v2-a (v2, CPU) | 12, same layout | tars 2.4+1.8+1.6+2.3+2.1+19.3 = 29.5 MB | 61 | 9332 s |
| schrodinger-shapes-3d-v2-b (v2, CPU) | 12 | 2.2+1.9+1.6+2.0+2.1+21.8 = 31.6 MB | 61 | 9608 s |
| schrodinger-shapes-3d-v2-c (v2, CPU) | 12 | 2.2+1.8+1.8+2.2+2.1+19.5 = 29.6 MB | 61 | 8495 s |
| schrodinger-shapes-3d-v2-d (v2, CPU) | 12 | 2.2+1.8+1.6+2.5+2.1+16.9 = 27.1 MB | 60 | 11097 s |

Fact: `shapes-3d` (GPU) and `v2-a..d` (CPU) ran the same job set `hard_and_shells` at commit `94d1281`; 61+61+61+60 = 243 = the GPU run. Same runs twice.
Fact: GPU time of `schrodinger-shapes-3d`: 1192 s sweep on 2 T4 (the log's own estimate 0.76 GPU hours).

## Fig. 12

| Notebook | Output | Session |
|---|---|---|
| guinness-on-a-cart-stout-in-jax v10 (run 10) | 10 files in `2026-11-14/`: `rest.npz`, `rest_particles_15.npz`, `rest_particles_60.npz`, `ride_bump25_joint.npz`, `ride_resonant_joint.npz`, `ride_sharp30_joint.npz`, `ride_sharp30_preview.npz`, `ride_sharp30_slosh.npz`, `summary.json`, `progress.log`; sizes not given | 1494 s (24.9 min), 2 T4 |
| guinness-free-swing-v2 v5 | `2026-11-12/free_swing_v2.json` (0.3 MB), `progress.log` | 665 s |
| guinness-on-a-cart-stout-sloshing v5 | `2026-11-13/rides.json` (1.80 MB), `timing.json`, `progress.log` | 2660 s (44 min) |

Not yet read: outputs of older versions (v6, v8 of the JAX notebook; v1-v4 of the Taichi ones). The site's run 8 and run 6 data were
packed from those outputs; whether the raw `.npz` exist anywhere else is to be checked.

## Others

- `phyein-sim-native-install-test` v2: `probe.json`; session 112 s; result: no DNS for github.com, dl.openfoam.com, conda; jax 0.11.1 CPU only.
- `html-panel-test-ripple-tank-…` v2: `ripple_tank.html` (15.8 MB); session 161 s; 121 runs in 136.5 s.
- `notebookddfec594b7`: no output (listing: Not found).


## Fig. 15 (read from the same listings and logs)

| Notebook (v1 each) | Output | Runs | Session |
|---|---|---|---|
| rt3d-shard-1-of-4 | 10 files: `2026-11-13/rt3d/` tar + index.json + runs.jsonl + timing, progress.log, 3 .py, 2 .pyc (`__pycache__`) | 29 | 376 s |
| rt3d-shard-2-of-4 | same layout | 29 | 383 s |
| rt3d-shard-3-of-4 | same | 29 | 369 s |
| rt3d-shard-4-of-4 | same | 28 | 352 s |
| rt3d-singles-v2 | same | 20 | 271 s |
| rt3d2-shard-1-of-6 | 11 files: `2026-11-13/rt3d2/` `rt3d2_all_0of6.tar` 1081.0 MB (621 files), index, runs.jsonl, done.txt, progress.log, .py, .pyc | 624 | 10773 s |
| rt3d2-shard-2-of-6 | `rt3d2_all_1of6.tar` 1076.6 MB (620 files) | 623 | 10813 s |
| rt3d2-shard-3-of-6 | `rt3d2_all_2of6.tar` 1099.6 MB (620 files); folder `2026-11-14/rt3d2/` | 623 | 11559 s |
| rt3d2-shard-4-of-6 | `rt3d2_all_3of6.tar` 1094.0 MB (619 files) | 623 | 11506 s |
| rt3d2-shard-5-of-6 | `rt3d2_all_4of6.tar` 1098.8 MB (619 files) | 623 | 11391 s |
| rt3d2-shard-6-of-6 | `rt3d2_all_5of6.tar` 1102.5 MB (619 files) | 623 | 11354 s |
| rt3d2-fix1 | 11 files, 15 runs | 15 | 594 s |

Fact: generation 2 shard tars on Kaggle total 6552.5 MB; runs 624 + 5 x 623 = 3739.
Fact: generation 1 runs 29+29+29+28 = 115 (+ 20 in singles-v2); the shard sizes of generation 1 are not in the logs.
Fact: generation-2 shard folders are dated by the day the shard ended: shards 1, 2: `2026-11-13`; shards 3-6, fix1: `2026-11-14`.

## Older versions (label format `v<N>` works for `get_notebook_info` and `list_notebook_session_output`; `6`, `8`, `Version 8` do not)

- guinness-on-a-cart-stout-in-jax **v8** (run 8, commit 96e8a1d): output `2026-11-13/`: 12 files: `free_full_1.5.npz`, `rest.npz`, `rest_particles_15.npz`, `rest_particles_60.npz`, `ride_bump25.npz`, `ride_bump25_joint.npz`, `ride_resonant.npz`, `ride_resonant_joint.npz`, `ride_sharp30.npz`, `ride_sharp30_joint.npz`, `ride_sharp30_slosh.npz`, `summary.json` (+ progress.log); session 2370 s. Skipped inside the run for budget: `ride_sharp30_preview`, `free_wall_1.5`.
- The raw `.npz` of runs 6 to 10 are on Kaggle only; the site holds packed `.json` of each ride (about 0.2 to 0.4 MB each).
- Not listed: outputs of v1-v7, v9 (JAX); v1-v4 (stout-sloshing); v1-v4 (free-swing-v2); v1 of shapes-3d.
