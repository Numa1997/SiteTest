# Fig. 14, Schrödinger sphere: all Kaggle outputs

Phyein Usul (phyeinusul.com), Fig. 14. Every output file of every Kaggle notebook run that made this figure's data, copied
byte for byte on 14 November 2026. Layout: `<notebook>/v<version>/output/` (the run's files as Kaggle saved them),
`run.log`, and `manifest.json` (size and SHA-256 of every file). `source-current-version` is the notebook's code;
the exact code of each run is pinned by the commit named in the site's `public/data/schrodinger-sphere/generations.json`.

| Notebook | Version | Files | Bytes |
|---|---|---|---|
| schrodinger-flat-wall | 1 | 589 | 52 106 974 |
| schrodinger-pillar | 1 | 592 | 106 636 503 |
| schrodinger-shapes-3d | 1 | 12 | 314 081 018 |
| schrodinger-shapes-3d | 2 | 12 | 118 640 252 |
| schrodinger-sphere-3d-generation | 1 | 85 | 59 698 640 |
| schrodinger-sphere-3d-wave | 1 | 84 | 101 020 191 |
| schrodinger-sphere-full-grid | 1 | 412 | 177 252 680 |
| schrodinger-spherical-wave | 1 | 1175 | 7 889 846 |

Total: 2961 files, 937 326 104 bytes.

Checked against the site: 3916 of the 4328 site files are byte-identical to a file here (or to a member of a shapes3d tar).
The other 412 are made in the repository: 405 `.bin` packed from `schrodinger-sphere-full-grid/v1/output/runs/*.json`, 7 index and record files.
`schrodinger-sphere-3d-generation` v1 is not used by the site; it is kept because this is its only copy.
