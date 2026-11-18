# Fig. 12, Guinness on a cart: all Kaggle outputs

Phyein Usul (phyeinusul.com), Fig. 12. Every output file of every version of the three Kaggle notebooks behind this figure, copied
byte for byte on 14 November 2026. Layout: `<notebook>/v<version>/output/` (the run's files as Kaggle saved them), `run.log`, and
`manifest.json` (size and SHA-256 of every file). `source-current-version` is the notebook's code; the exact code of each run is
pinned by the commit named in the site's `public/data/fig12/generations.json`.

| Notebook | Version | Files | Bytes |
|---|---|---|---|
| guinness-free-swing-v2 | 2 | 2 | 35 806 |
| guinness-free-swing-v2 | 3 | 2 | 116 041 |
| guinness-free-swing-v2 | 4 | 2 | 1 024 712 |
| guinness-free-swing-v2 | 5 | 2 | 342 241 |
| guinness-on-a-cart-stout-in-jax | 1 | 9 | 1 282 738 |
| guinness-on-a-cart-stout-in-jax | 2 | 5 | 1 522 646 |
| guinness-on-a-cart-stout-in-jax | 3 | 3 | 592 014 |
| guinness-on-a-cart-stout-in-jax | 4 | 9 | 29 343 536 |
| guinness-on-a-cart-stout-in-jax | 5 | 1 | 122 |
| guinness-on-a-cart-stout-in-jax | 6 | 10 | 30 335 778 |
| guinness-on-a-cart-stout-in-jax | 7 | 10 | 29 706 851 |
| guinness-on-a-cart-stout-in-jax | 8 | 13 | 35 471 074 |
| guinness-on-a-cart-stout-in-jax | 9 | 3 | 1 122 370 |
| guinness-on-a-cart-stout-in-jax | 10 | 10 | 29 653 359 |
| guinness-on-a-cart-stout-in-jax | 11 | 2 | 14 073 |
| guinness-on-a-cart-stout-in-jax | 12 | 2 | 14 066 |
| guinness-on-a-cart-stout-sloshing | 1 | 5 | 631 962 |
| guinness-on-a-cart-stout-sloshing | 2 | 3 | 359 862 |
| guinness-on-a-cart-stout-sloshing | 3 | 3 | 798 184 |
| guinness-on-a-cart-stout-sloshing | 4 | 1 | 2 007 |
| guinness-on-a-cart-stout-sloshing | 5 | 3 | 1 803 059 |

Total: 100 files, 164 172 501 bytes. Version 1 of guinness-free-swing-v2 saved no output.

Checked against the site: `2026-11-13/rides.json` = stout-sloshing v5; `2026-11-12/free_swing_v2.json` = free-swing-v2 v4;
`2026-11-12/free_swing_v2_repair.json` = free-swing-v2 v5 (byte-identical). The site's JAX rides (runs 6 to 10) are packed in the
repository from the `.npz` files here; the `.npz` exist only in this dataset.

Added 18 November 2026 (dataset version 2): versions 11 and 12 of guinness-on-a-cart-stout-in-jax, run 15 November 2026, the
damping-grid study (`tools/fig12/kaggle/damping_grid.py`, commit 758df533; `damping/damping.json` and `progress.log`); version 12's
code is in `v12/source.ipynb`. `source-current-version.ipynb` stays the code of version 10, the run the site plays.

Added 18 November 2026: `v<version>/source.ipynb`, the exact code of every version of every notebook in this dataset except
guinness-on-a-cart-stout-in-jax (kept on Kaggle), fetched with the Kaggle API (GetKernel, versionLabel) before the old notebooks were
deleted. The one notebook of the figure is now fig-14-schrodinger-sphere / fig-12-guinness-on-a-cart; it runs every job from this code.
