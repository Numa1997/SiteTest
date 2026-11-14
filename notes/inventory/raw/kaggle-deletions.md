# Kaggle notebooks deleted (14 November 2026)

Order of the owner, 14 November 2026: "delete all redundant". Each notebook below was first copied to `kaggle-copies/<slug>/`:
`source.*` (the code of its current version), `metadata.json`, `run.log` (when the API returned one), `manifest.json` (every output file
with its size in bytes; SHA-256 for the text files) and `output/` (text files up to 2 MB: index, timing, logs, solver code).
Large binary outputs (tars, `.html` panels, `.npz`) were not kept: none is used by the site or by any record (checked by grep over the
repository and by SHA-256 against the site, see `kaggle-sizes.md`).

| Notebook | Why redundant | Kept here |
|---|---|---|
| notebookddfec594b7 | empty draft, no output | source |
| html-panel-test-ripple-tank-computed-on-kaggle | test of an HTML panel computed on Kaggle; not on the site | source, file list |
| phyein-sim-native-install-test | install probe (no DNS for github.com, conda) | source, probe.json |
| phyein-sim-run-case | test run of the case runner | source, small outputs |
| phyein-sim-run-case-fem | test run, FEM variant | source, small outputs |
| phyein-sim-jax-swingup-gpu | GPU test of a JAX swing-up | source, small outputs |
| schrodinger-sphere-gpu-smoke-test | GPU smoke test; its timing is quoted in docs/kaggle.md | source, timing.json, logs |
| schrodinger-shapes-3d-v2-a … d | CPU copies of the 243 runs the GPU notebook `schrodinger-shapes-3d` v2 made; output never used | source, index.json, timing.json, logs |

Deletion: `POST https://api.kaggle.com/v1/kernels.KernelsApiService/DeleteKernel` with `{"userName", "kernelSlug"}`; responses in
`kaggle-deletions.log`. Listing before: 39 notebooks; after: 28.
