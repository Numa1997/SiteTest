# Fig. 16, a pint of Guinness on a cart built to carry it: Kaggle outputs

Phyein Usul (phyeinusul.com/simulations/guinness-cart-control), Fig. 16. Every output file of the three versions of the Kaggle GPU notebook numakoudsie/fig-16-guinness-cart-with-control that the page plays, copied byte for byte on 18 November 2026 (23 files, 103 476 921 bytes). Layout: fig-16-guinness-cart-with-control/v<version>/output/<date>/<file>; manifest.json gives the size and SHA-256 of every file; README.md lists the versions.

- Version 2 (14 November 2026, code at commit 2041127): resonant_full, bump25_full.
- Version 8 (15 November 2026, run 5): kerb_off, resonant_off, bump25_off. The run's code commit is not stored in its outputs; the page's files were packed from it at commit 0054020 (public/data/fig16/2026-11-15/index-16.json). The README's "see summary.json" for this row is wrong: summary.json does not name it.
- Version 9 (18 November 2026, code at commit 5c45658): kerb_full, kerb_full_seed2 (area probes, audit M3).

Each .npz is one task of tools/fig16/kaggle/run16.py in github.com/Numa1997/SiteTest; the page's ride files are packed from them by tools/fig16/kaggle/pack16.py (format conversion only).
