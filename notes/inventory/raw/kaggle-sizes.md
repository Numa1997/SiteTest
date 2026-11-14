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
