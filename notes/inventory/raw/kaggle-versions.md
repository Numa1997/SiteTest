# Kaggle: every version of every notebook (read 14 November 2026, read-only)

Method. Status: `get_notebook_session_status` (version label format `v<N>`; labels `6` or `Version 6` are refused). Source and commit:
`get_notebook_info` with the same label. File names and run time: `list_notebook_files` with the same label (its `size` field is NOT
a file size: it returns 650 to 713 for every file, tar or log alike, and is ignored here; its `creation_date` is the minute the
version was started). Sizes: `download_notebook_output` returns one signed link for a file of a version; the same link with another
file path serves every other file of that version; a one-byte range request (`curl -r 0-0`) returns the exact size in `Content-Range`
(HEAD requests answer 404). Nothing is downloaded except small index or summary files.

## Status of the current version of all 35 notebooks

34 of 35: **COMPLETE**. `notebookddfec594b7`: "No runs found for this kernel" (never run). Nothing was running or queued on the account
at the time of the check (14 November 2026, after 12:30 UTC).

## Status of every older version

| Notebook | Versions | Status per version |
|---|---|---|
| guinness-on-a-cart-stout-in-jax | 10 | v1 to v10: all COMPLETE |
| guinness-on-a-cart-stout-sloshing | 5 | v1 COMPLETE, v2 COMPLETE, v3 COMPLETE, **v4 ERROR**, v5 COMPLETE |
| guinness-free-swing-v2 | 5 | **v1 ERROR**, v2 COMPLETE, v3 COMPLETE, v4 COMPLETE, v5 COMPLETE |
| schrodinger-shapes-3d | 2 | v1 COMPLETE, v2 COMPLETE |
| schrodinger-shapes-3d-v2-a, -b, -c, -d | 2 each | **v1 ERROR** (all four), v2 COMPLETE (all four) |
| html-panel-test-ripple-tank-computed-on-kaggle | 2 | v1 COMPLETE, v2 COMPLETE |
| phyein-sim-jax-swingup-gpu | 2 | **v1 ERROR**, v2 COMPLETE |
| phyein-sim-native-install-test | 2 | v1 COMPLETE, v2 COMPLETE |
| all other 26 notebooks | 1 each | v1 COMPLETE (the starter: never run) |

Total versions on the account: 10 + 5 + 5 + 2 + 8 + 2 + 2 + 2 + 25 (single-version notebooks that ran) = 61 runs, of which 8 ended in ERROR
(Kaggle gives an empty failure message for each). The 8 failed versions hold no result anyone uses.

## Files and start time of every version (names from `list_notebook_files`; it drops folder names)

### guinness-on-a-cart-stout-in-jax (Fig. 12, JAX solver). All ten versions COMPLETE.

| Version | Started (UTC) | Output files |
|---|---|---|
| v1 | 13 Nov 02:01 | free_full_1.5.npz, free_inviscid_1.5.npz, free_inviscid_2.npz, free_inviscid_3.npz, rest.npz, ride_bump25.npz, ride_resonant.npz, summary.json, progress.log |
| v2 | 13 Nov 03:33 | free_full_1.5.npz, rest.npz, ride_resonant.npz, summary.json, progress.log |
| v3 | 13 Nov 17:34 | rest.npz, summary.json, progress.log |
| v4 | 13 Nov 18:21 | free_full_1.5.npz, rest.npz, rest_particles_15.npz, rest_particles_60.npz, ride_bump25.npz, ride_resonant.npz, ride_sharp30.npz, summary.json, progress.log |
| v5 | 13 Nov 18:55 | progress.log only (the run produced no data file) |
| v6 = run 6 | 13 Nov 19:04 | free_full_1.5.npz, free_wall_1.5.npz, rest.npz, rest_particles_15.npz, rest_particles_60.npz, ride_bump25.npz, ride_resonant.npz, ride_sharp30.npz, summary.json, progress.log |
| v7 = run 7 | 13 Nov 20:20 | rest.npz, rest_particles_15.npz, rest_particles_60.npz, ride_bump25_joint.npz, ride_resonant_joint.npz, ride_sharp30_joint.npz, ride_sharp30_preview.npz, ride_sharp30_slosh.npz, summary.json, progress.log |
| v8 = run 8 | 13 Nov 23:34 | free_full_1.5.npz, rest.npz, rest_particles_15.npz, rest_particles_60.npz, ride_bump25.npz, ride_bump25_joint.npz, ride_resonant.npz, ride_resonant_joint.npz, ride_sharp30.npz, ride_sharp30_joint.npz, ride_sharp30_slosh.npz, summary.json, progress.log (folder `2026-11-13/`) |
| v9 = run 9 | 14 Nov 00:16 | ride_sharp30_preview.npz, summary.json, progress.log |
| v10 = run 10 | 14 Nov 08:01 | rest.npz, rest_particles_15.npz, rest_particles_60.npz, ride_bump25_joint.npz, ride_resonant_joint.npz, ride_sharp30_joint.npz, ride_sharp30_preview.npz, ride_sharp30_slosh.npz, summary.json, progress.log (folder `2026-11-14/`) |

Versions 1 to 5 are named by no record on the site (`fig12/generations.json` names runs 6, 7, 8, 9, 10 only): they are the development runs before run 6.

### guinness-on-a-cart-stout-sloshing (Fig. 12, Taichi solver)

| Version | Started (UTC) | Status | Output files |
|---|---|---|---|
| v1 | 12 Nov 15:40 | COMPLETE | animation.html, ride.mp4, rides.json, timing.json, progress.log |
| v2 | 12 Nov 17:02 | COMPLETE | guinness.html, timing.json, progress.log |
| v3 | 12 Nov 17:57 | COMPLETE | guinness.html, timing.json, progress.log (the notebook's own text says v3 made the over-damped rides of 12 Nov with solver v1) |
| v4 | 12 Nov 23:56 | ERROR | progress.log only (missing import, per the v5 notebook text) |
| v5 | 13 Nov 00:15 | COMPLETE | 2026-11-13/rides.json (1.80 MB), timing.json, progress.log |

### guinness-free-swing-v2 (Fig. 12, Taichi solver v2, free swing)

| Version | Started (UTC) | Status | Output files |
|---|---|---|---|
| v1 | not listed | ERROR | none |
| v2 | 12 Nov 22:42 | COMPLETE | free_swing_v2.json, progress.log |
| v3 | 12 Nov 22:46 | COMPLETE | free_swing_v2.json, progress.log |
| v4 | 12 Nov 22:50 | COMPLETE | free_swing_v2.json, progress.log |
| v5 | 12 Nov 23:42 | COMPLETE | 2026-11-12/free_swing_v2.json (0.3 MB), progress.log (the "repair round": seed 2, dt 1 ms, half push) |

### schrodinger-shapes-3d (Fig. 14)

| Version | Started (UTC) | Status | Output files |
|---|---|---|---|
| v1 | 13 Nov 00:58 | COMPLETE | coin.tar, soff.tar, sphere.tar, spil.tar, sslab.tar, tube.tar, index.json, runs.jsonl, timing.json, progress.log, shapes3d_run.py, solver3d.py (the full 1458-run job; record: commit a269119, sweep 3992.8 s) |
| v2 | 13 Nov 03:01 | COMPLETE | same twelve names (the 243 corrected runs, commit 94d1281) |

### Other tests (current version)

- phyein-sim-jax-swingup-gpu v2 (12 Nov 06:22): two folders (`smoke/`, `full/`), each with result.json, swingup.png, swingup_data.json, timing.json. v1: ERROR.
- phyein-sim-run-case v1 (12 Nov 06:08): commit.txt, timing.json and an OpenFOAM case folder `run0/` (fields U, p, phi; logs log.Allrun, log.blockMesh, log.icoFoam; blockMeshDict, controlDict, fvSchemes, fvSolution; horizontal_U.xy, vertical_U.xy; result.json; walltime_s): 25 files.
- phyein-sim-run-case-fem v1 (12 Nov 06:11): commit.txt, timing.json, `run0/` with beam.12d, beam.cvg, beam.dat, beam.frd, beam.inp, beam.sta, spooles.out, log.run, run.py, result.json, walltime_s: 13 files. (These file types are CalculiX output, although the notebook's comment names DOLFINx.)
