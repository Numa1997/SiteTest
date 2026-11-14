# Kaggle output sizes, measured exactly (14 November 2026)
Method: one signed link per notebook version (`download_notebook_output`), then a one-byte range request per file; the size is the total in `Content-Range`. Read-only; no file body was downloaded except small `summary.json` / `index.json` files.

## guinness-on-a-cart-stout-in-jax (Fig. 12)

| Version | Files | Bytes | MB |
|---|---|---|---|
| v1 | 9 | 1282738 | 1.28 |
| v2 | 5 | 1522646 | 1.52 |
| v3 | 3 | 592014 | 0.59 |
| v4 | 9 | 29343536 | 29.34 |
| v5 | 1 | 122 | 0.00 |
| v6 | 10 | 30335778 | 30.34 |
| v7 | 10 | 29706851 | 29.71 |
| v8 | 13 | 35471074 | 35.47 |
| v9 | 3 | 1122370 | 1.12 |
| v10 | 10 | 29653359 | 29.65 |
| all ten | 73 | 159030488 | 159.03 |

Per file (bytes, path):

```
v1
      6237  2026-11-13/summary.json
      5601  2026-11-13/progress.log
     25661  2026-11-13/rest.npz
    139269  2026-11-13/free_full_1.5.npz
    107188  2026-11-13/free_inviscid_1.5.npz
     85963  2026-11-13/free_inviscid_2.npz
     83242  2026-11-13/free_inviscid_3.npz
    237265  2026-11-13/ride_bump25.npz
    592312  2026-11-13/ride_resonant.npz
v2
      3292  2026-11-13/summary.json
     15307  2026-11-13/progress.log
     72866  2026-11-13/rest.npz
    243426  2026-11-13/free_full_1.5.npz
   1187755  2026-11-13/ride_resonant.npz
v3
      1271  2026-11-13/summary.json
       672  2026-11-13/progress.log
    590071  2026-11-13/rest.npz
v4
      5535  2026-11-13/summary.json
      4117  2026-11-13/progress.log
    585029  2026-11-13/rest.npz
  10679146  2026-11-13/rest_particles_15.npz
  10697870  2026-11-13/rest_particles_60.npz
   1445868  2026-11-13/free_full_1.5.npz
   2311082  2026-11-13/ride_bump25.npz
   2387501  2026-11-13/ride_resonant.npz
   1227388  2026-11-13/ride_sharp30.npz
v5
       122  2026-11-13/progress.log
v6
      6864  2026-11-13/summary.json
      5143  2026-11-13/progress.log
    553456  2026-11-13/rest.npz
  10679151  2026-11-13/rest_particles_15.npz
  10697298  2026-11-13/rest_particles_60.npz
   1364669  2026-11-13/free_full_1.5.npz
   1419906  2026-11-13/free_wall_1.5.npz
   2188962  2026-11-13/ride_bump25.npz
   2272240  2026-11-13/ride_resonant.npz
   1148089  2026-11-13/ride_sharp30.npz
v7
      9189  2026-11-13/summary.json
      4948  2026-11-13/progress.log
    553248  2026-11-13/rest.npz
  10679353  2026-11-13/rest_particles_15.npz
  10697167  2026-11-13/rest_particles_60.npz
   2182097  2026-11-13/ride_bump25_joint.npz
   2192172  2026-11-13/ride_resonant_joint.npz
   1127208  2026-11-13/ride_sharp30_joint.npz
   1140413  2026-11-13/ride_sharp30_preview.npz
   1121056  2026-11-13/ride_sharp30_slosh.npz
v8
     16640  2026-11-13/summary.json
     10071  2026-11-13/progress.log
    553058  2026-11-13/rest.npz
  10677318  2026-11-13/rest_particles_15.npz
  10697099  2026-11-13/rest_particles_60.npz
   1363381  2026-11-13/free_full_1.5.npz
   2186976  2026-11-13/ride_bump25.npz
   2182432  2026-11-13/ride_bump25_joint.npz
   2254824  2026-11-13/ride_resonant.npz
   2191778  2026-11-13/ride_resonant_joint.npz
   1122026  2026-11-13/ride_sharp30.npz
   1110782  2026-11-13/ride_sharp30_joint.npz
   1104689  2026-11-13/ride_sharp30_slosh.npz
v9
      2078  2026-11-14/summary.json
       996  2026-11-14/progress.log
   1119296  2026-11-14/ride_sharp30_preview.npz
v10
     11533  2026-11-14/summary.json
    552905  2026-11-14/rest.npz
  10677572  2026-11-14/rest_particles_15.npz
  10696755  2026-11-14/rest_particles_60.npz
   2185246  2026-11-14/ride_bump25_joint.npz
   2193147  2026-11-14/ride_resonant_joint.npz
   1113680  2026-11-14/ride_sharp30_joint.npz
   1121054  2026-11-14/ride_sharp30_preview.npz
   1095227  2026-11-14/ride_sharp30_slosh.npz
      6240  2026-11-14/progress.log
```

## Fig. 12, the two Taichi notebooks (exact bytes)

| Notebook, version | Files (bytes) | Total |
|---|---|---|
| guinness-on-a-cart-stout-sloshing v1 | progress.log 1 392; rides.json 271 590; timing.json 667; animation.html 279 930; ride.mp4 78 383 (all at the output root) | 631 962 |
| … v2 | progress.log 4 269; timing.json 775; guinness.html 354 818 | 359 862 |
| … v3 | progress.log 8 662; timing.json 804; guinness.html 788 718 | 798 184 |
| … v4 (ERROR) | progress.log only, not measured | |
| … v5 | 2026-11-13/progress.log 6 232; rides.json 1 795 977; timing.json 850 | 1 803 059 |
| guinness-free-swing-v2 v2 | 2026-11-12/progress.log 2 057; free_swing_v2.json 33 749 | 35 806 |
| … v3 | progress.log 1 752; free_swing_v2.json 114 289 | 116 041 |
| … v4 | progress.log 5 438; free_swing_v2.json 1 019 274 | 1 024 712 |
| … v5 | progress.log 2 671; free_swing_v2.json 339 570 | 342 241 |

Both Taichi notebooks together: 5.11 MB. All of Fig. 12 on Kaggle (three notebooks, all versions): 164.1 MB.

## Fig. 12: is the site's data the same as Kaggle's? (SHA-256, files downloaded and hashed on 14 November 2026)

| Site file (`public/data/fig12/`) | Kaggle file | SHA-256 | Result |
|---|---|---|---|
| `2026-11-13/rides.json` (1 795 977 B) | stout-sloshing v5 `2026-11-13/rides.json` | 5619dd27…6680a | **identical** |
| `2026-11-12/free_swing_v2.json` (1 019 274 B) | free-swing-v2 **v4** `2026-11-12/free_swing_v2.json` | fac49421…99344 | **identical** |
| `2026-11-12/free_swing_v2_repair.json` (339 570 B) | free-swing-v2 **v5** `2026-11-12/free_swing_v2.json` | 28d8b6d9…29abd | **identical** |
| `2026-11-12/rides.json` (715 166 B) | no Kaggle file has these bytes: the site's `2026-11-12/index.json` says it was taken out of stout-sloshing v3's `guinness.html` and records that file's SHA-256 | 8a2551ef…10b83 for `guinness.html` | v3 `guinness.html` downloaded and hashed: **matches the record** (788 718 B) |

Consequence (Fact): for the Taichi generations the site already holds byte-identical copies of the three result files, and the record
(`2026-11-12/index.json`) names notebook, version and commit for each. Not on the site: v1's `animation.html`, `ride.mp4`, `rides.json`
(the very first test), v2's and v3's `guinness.html`, the free-swing results of v2 and v3, and every `progress.log`.

The JAX notebook is different: the site holds packed `.json` rides (0.2 to 0.4 MB each), Kaggle holds the raw `.npz` (1.1 to 2.4 MB per ride,
10.7 MB per particle snapshot). The raw files exist only on Kaggle: 159.03 MB in 73 files over ten versions.

## Fig. 14 (exact bytes; per-run bytes from each notebook's own `index.json`, the rest by range request)

| Notebook, version | What | Files | Bytes | MB |
|---|---|---|---|---|
| schrodinger-sphere-full-grid v1 | `runs/` 405 JSON (cut z = 0 with amplitude **and phase**) | 405 | 159 325 619 | 159.3 |
| … | + `schrodinger_sphere_preview.html` 17 809 324; index.json 67 945; progress.log 33 248; panel_template.html 12 426; solver.py 3 067; pack.py 1 004; timing.json 47 | 7 | 17 927 061 | 17.9 |
| … total | | 412 | 177 252 680 | 177.3 |
| schrodinger-sphere-3d-generation v1 | `2026-11-12/runs3d/` 81 .bin (full 3D cloud, 64³, 48 frames) | 81 | 59 664 248 | 59.7 |
| … | + index.json 23 422; timing.json 47; progress.log 7 162; solver.py 3 761 | 4 | 34 392 | |
| schrodinger-sphere-3d-wave v1 | `2026-11-12/wave3d/` 81 .bin | 81 | 100 985 150 | 101.0 |
| schrodinger-flat-wall v1 | `2026-11-12/flat/` 585 .bin | 585 | 51 929 764 | 51.9 |
| schrodinger-pillar v1 | `2026-11-12/pillar/` 585 .bin (+ gz.bin) | 585 | 106 234 675 | 106.2 |
| schrodinger-spherical-wave v1 | `2026-11-12/radial/` 1 170 .bin | 1 170 | 7 538 677 | 7.5 |
| schrodinger-shapes-3d **v1** | six tars: coin 82 606 080; tube 84 101 120; spil 97 239 040; sphere 28 794 880; soff 10 813 440; sslab 9 400 320 (1 458 runs + 36 wave files; run bytes in index 310 238 128) | 6 tars | 312 954 880 | 313.0 |
| … | + index.json 448 251; runs.jsonl 498 458; timing.json 176; progress.log 163 504; shapes3d_run.py 8 858; solver3d.py 6 891 | 6 | 1 126 138 | 1.1 |
| schrodinger-shapes-3d **v2** | six tars: coin 7 178 240; tube 6 666 240; spil 78 080 000; sphere 9 082 880; soff 8 980 480; sslab 8 437 760 (243 runs + 36 wave files; run bytes 117 885 686) | 6 tars | 118 425 600 | 118.4 |
| … | + index.json 80 929; runs.jsonl 88 571; timing.json 174; progress.log 27 925; shapes3d_run.py 9 452; solver3d.py 7 601 | 6 | 214 652 | 0.2 |
| schrodinger-sphere-gpu-smoke-test v1 | schrodinger_sphere.html 2 770 505; timing.json 1 735; progress.log 1 837; solver.py 3 067; pack.py 1 004; panel_template.html 12 426 | 6 | 2 790 574 | 2.8 |

Fig. 14 on Kaggle without the four CPU shard notebooks: 935.4 MB (the four CPU shards add about 118 MB, see `kaggle-outputs.md`).

## Fig. 14: is the site's data the same as Kaggle's? (every run compared by SHA-256, 14 November 2026)

Method: each notebook's `index.json` was downloaded from Kaggle and compared, run by run, with the site's index of the same part;
then every file on disk under `public/data/schrodinger-sphere/` was hashed and compared with the site's own index.

| Part on the site | Runs | Kaggle source | Same SHA-256 | Different | Missing on site | Site files that differ from the site index |
|---|---|---|---|---|---|---|
| `2026-11-12/wave3d/` | 81 | schrodinger-sphere-3d-wave v1 | **81** | 0 | 0 | 0 of 81 |
| `2026-11-12/flat/` | 585 | schrodinger-flat-wall v1 | **585** | 0 | 0 | 0 of 585 |
| `2026-11-12/pillar/` (+ gz.bin) | 585 | schrodinger-pillar v1 | **585** (gz.bin equal too) | 0 | 0 | 0 of 585 |
| `2026-11-12/radial/` | 1 170 | schrodinger-spherical-wave v1 | **1 170** | 0 | 0 | 0 of 1 170 |
| `2026-11-13/shapes3d/` | 1 458 (+36 wave) | schrodinger-shapes-3d v1, with v2 laid over it | **1 215 from v1 + 243 from v2 = 1 458**; wave files 36 of 36 | 0 | 0 | 0 of 1 458 |
| `2026-11-12/` sphere (405 .bin) | 405 | schrodinger-sphere-full-grid v1 | not comparable byte for byte: the site stores a converted, amplitude-only form (`to_site_axisym.py`); the Kaggle JSON also holds the phase | | | |

Consequences (Facts):
1. For wave3d, flat wall, pillar, spherical wave and shapes3d the site holds a **byte-identical** copy of everything those notebooks produced
   that is in use. Their Kaggle outputs are a second copy, not the only one.
2. `schrodinger-shapes-3d` **v1** holds 243 runs that v2 replaced (the runs whose start wave was wrong). Those 243 old files exist only
   in v1's tars on Kaggle; they are superseded by design and recorded as such in the site index (`version2`).
3. `schrodinger-sphere-full-grid` holds the only copy of the sphere runs **with phase** (159.3 MB in 405 JSON files) and of the 17.8 MB
   preview panel.
4. `schrodinger-sphere-3d-generation` (59.7 MB, 81 runs) is on no page and in no site record; Kaggle is its only copy.
5. A copy of the smoke test's `timing.json` (1 735 B; the source of "1.61 ms per split-step" in `docs/kaggle-pipeline.md`) is now kept in
   `notes/inventory/raw/kaggle-copies/` with its SHA-256, so the cited numbers no longer depend on that notebook.

## Fig. 14, the four CPU shard notebooks `schrodinger-shapes-3d-v2-a..d` (v2 each; exact bytes)

| Notebook | Runs | Six tars (bytes) | Run bytes in its index | CPU sweep |
|---|---|---|---|---|
| v2-a | 61 | 29 532 160 | 29 373 238 | 9 305 s |
| v2-b | 61 | 31 682 560 | 31 504 909 | 9 582 s |
| v2-c | 61 | 29 634 560 | 29 477 976 | 8 468 s |
| v2-d | 60 | 27 187 200 | 27 025 208 | 11 061 s |
| all four | 243 | 118 036 480 (118.0 MB) | 117 381 331 | 38 416 s = 10.7 h of CPU |

Compared with the site and with the GPU run of the same job (Facts):
- The four CPU notebooks produced exactly the same set of 243 run files as `schrodinger-shapes-3d` v2 (same names).
- **None** of the 243 is byte-identical to the GPU file, and none is on the site: the site uses the GPU output (243 of 243).
  Inference: CPU and GPU floating-point results differ in the last digits, which changes the compressed bytes; the two sets are the same
  physics computed twice, not copies of each other.
- No record anywhere names these four notebooks.

## Fig. 15 (exact bytes; every file by range request; per-file list in `kaggle-fig15-files.json`)

| Notebook (v1 each) | Tar | Tar bytes | All output files | Runs in its index | Run bytes in its index |
|---|---|---|---|---|---|
| fig15-rt3d-smoke | `2026-11-13/rt3d/rt3d.tar` | 2 928 640 | 2 974 313 | 2 | 2 920 642 |
| fig15-rt3d-shard-1-of-4 | `rt3d.tar` | 46 080 000 | 46 150 037 | 29 | 46 026 549 |
| fig15-rt3d-shard-2-of-4 | `rt3d.tar` | 46 141 440 | 46 211 440 | 29 | 46 083 699 |
| fig15-rt3d-shard-3-of-4 | `rt3d.tar` | 46 223 360 | 46 293 268 | 29 | 46 162 432 |
| fig15-rt3d-shard-4-of-4 | `rt3d.tar` | 45 066 240 | 45 135 216 | 28 | 45 007 922 |
| fig15-rt3d-singles-v2 | `rt3d.tar` | 31 938 560 | 32 000 712 | 20 | 31 897 836 |
| **generation 1 total** | | | **218 764 986 (218.8 MB)** | 137 | |
| fig15-rt3d2-smoke | `2026-11-13/rt3d2/rt3d2_smoke.tar` | 6 891 520 | 6 954 323 | 4 (per its title) | |
| fig15-rt3d2-shard-1-of-6 | `2026-11-13/rt3d2/rt3d2_all_0of6.tar` | 1 081 016 320 | 1 081 780 336 | 624 | 1 085 804 508 |
| fig15-rt3d2-shard-2-of-6 | `2026-11-13/rt3d2/rt3d2_all_1of6.tar` | 1 076 592 640 | 1 077 355 186 | 623 | 1 081 385 012 |
| fig15-rt3d2-shard-3-of-6 | `2026-11-14/rt3d2/rt3d2_all_2of6.tar` | 1 099 632 640 | 1 100 396 663 | 623 | 1 104 671 908 |
| fig15-rt3d2-shard-4-of-6 | `2026-11-14/rt3d2/rt3d2_all_3of6.tar` | 1 093 980 160 | 1 094 744 748 | 623 | 1 101 025 972 |
| fig15-rt3d2-shard-5-of-6 | `2026-11-14/rt3d2/rt3d2_all_4of6.tar` | 1 098 752 000 | 1 099 515 892 | 623 | 1 105 775 834 |
| fig15-rt3d2-shard-6-of-6 | `2026-11-14/rt3d2/rt3d2_all_5of6.tar` | 1 102 458 880 | 1 103 221 356 | 623 | 1 109 491 312 |
| fig15-rt3d2-fix1 | `2026-11-14/rt3d2/rt3d2_fix1.tar` | 42 967 040 | 43 036 981 | 15 | 42 935 263 |
| **generation 2 total** | | | **6 607 005 485 (6 607.0 MB)** | 3 754 + 4 | 6 631 089 809 |

Note: each shard's index lists a few more run bytes than its tar holds (for example shard 1: 1 085.8 MB in the index, 1 081.0 MB in the tar,
624 runs in the index, 621 files in the tar per its own log): a spec computed twice inside one shard keeps one file name, so the tar holds
the later copy only. Not checked further; the files in use are verified below.

## Fig. 15: is the site's and R2's data the same as Kaggle's? (SHA-256, each shard's `index.json` downloaded)

Generation 2 (`public/data/resonant-tunnelling/2026-11-14/kaggle/index.json`, 3 697 runs, files in R2):

| Notebook | Runs in its index | Site index has the same SHA | Site has a different SHA (another notebook's copy is used) |
|---|---|---|---|
| shard 1 | 624 | 614 | 10 |
| shard 2 | 623 | 608 | 15 |
| shard 3 | 623 | 616 | 7 |
| shard 4 | 623 | 615 | 8 |
| shard 5 | 623 | 616 | 7 |
| shard 6 | 623 | 613 | 10 |
| fix1 | 15 | 15 | 0 |
| sum | 3 754 | **3 697** | 57 |

- **Every one of the 3 697 runs in the site index (= the 3 697 R2 objects) has its SHA-256 in a Kaggle shard index**, and the site index names
  exactly the notebook whose copy it uses (614 + 608 + 616 + 615 + 616 + 613 + 15 = 3 697).
- 57 run files exist in two copies on Kaggle with different bytes: 42 specs computed in two job groups and the 15 runs that `fix1` recomputed.
  One copy of each is in use; the other 57 exist only on Kaggle (6 631.1 MB in the Kaggle indexes against 6 527.0 MB in R2: 104.1 MB).
  The 15 replaced ones are recorded in the site index under `replaced` with their old SHA-256.
- Not verified here: the SHA-256 of the R2 objects themselves (that would mean downloading 6.5 GB). Their sizes match the index
  (`raw/r2-summary.md`), and the page checks each file's SHA-256 in the browser when it loads one.

Generation 1 (`public/data/resonant-tunnelling/2026-11-13/kaggle/`, 115 runs, in the repository):

| Notebook | Runs | Same SHA as the site | Different SHA |
|---|---|---|---|
| fig15-rt3d-shard-1-of-4 | 29 | 24 | 5 |
| fig15-rt3d-shard-2-of-4 | 29 | 24 | 5 |
| fig15-rt3d-shard-3-of-4 | 29 | 24 | 5 |
| fig15-rt3d-shard-4-of-4 | 28 | 23 | 5 |
| fig15-rt3d-singles-v2 | 20 | 20 | 0 |
| fig15-rt3d-smoke | 2 | 0 | 2 |

- **All 115 site runs are byte-identical to a Kaggle run** (95 from the four shards + 20 from singles-v2), and all 115 files on disk
  match the site index (184 592 414 B).
- The 20 single-barrier runs of the four shards (5 per shard) are the ones `singles-v2` replaced: they exist only in the shard tars on Kaggle,
  and the site index records why under `replaced`.
- The smoke notebook's 2 runs are different bytes from the site's files of the same name.

## Test notebooks (exact bytes)

| Notebook | Files (bytes) | Total |
|---|---|---|
| html-panel-test-ripple-tank-computed-on-kaggle v2 | ripple_tank.html 15 848 816 | 15.85 MB |
| phyein-sim-jax-swingup-gpu v2 | smoke/: result.json 2 067, swingup.png 58 750, swingup_data.json 5 481, timing.json 252; full/: result.json 19 640, swingup.png 60 673, swingup_data.json 5 470, timing.json 258 | 152 591 B |
| phyein-sim-run-case v1 (OpenFOAM cavity, N = 32) | commit.txt 41 (`da387cb3de8bc2a86f56a857f752888904793f4f`, repository phyein-sim), timing.json 401, run0/log.icoFoam 3 898 360, 13 small case files (about 10 kB); some time-folder files not measured | about 3.9 MB |
| phyein-sim-run-case-fem v1 (beam, CalculiX, 12 modes) | commit.txt 41 (same commit), timing.json 2 147, run0/beam.frd 2 542 908, beam.inp 251 409, beam.dat 4 558, run.py 8 169, result.json 1 729, small logs; beam.12d and spooles.out are empty (HTTP 416) | about 2.8 MB |
| phyein-sim-native-install-test v2 | probe.json 353 | 353 B |
| notebookddfec594b7 | no output | 0 |

Results recorded in those outputs (Facts): the OpenFOAM cavity case passed its check (largest error 0.0042 against Ghia, Ghia & Shin 1982,
tolerance 0.01; 9.0 s; install 61 s); the beam case ran in 19.4 s (install 131 s; first bending mode 66.93 Hz against 66.84 Hz from
Euler-Bernoulli theory). Both ran the code of `numa1997/phyein-sim` at commit `da387cb`.

## Whole account: measured output per group

| Group | Notebooks | Versions with output | Bytes | MB |
|---|---|---|---|---|
| Fig. 12 | 3 | 18 | 164 142 355 | 164.1 |
| Fig. 14 (GPU and CPU originals) | 8 | 9 | about 935.4 MB | 935.4 |
| Fig. 14 CPU duplicates (v2-a..d) | 4 | 4 | 118 136 000 (tars + small files) | 118.1 |
| Fig. 15 generation 1 | 6 | 6 | 218 764 986 | 218.8 |
| Fig. 15 generation 2 | 8 | 8 | 6 613 959 808 | 6 614.0 |
| Tests | 6 | 6 | about 22.7 MB | 22.7 |
| **All** | **35** | **51** | | **about 8 073 MB (8.07 GB)** |

Not measured: the outputs of the 8 failed versions (their logs only) and of the first versions of the two-version test notebooks.
