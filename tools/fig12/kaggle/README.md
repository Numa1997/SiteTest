# Fig. 12 OpenFOAM cases on Kaggle

The user's direction (12 November 2026): compute the stout's data on the user's Kaggle account, keep it saved there,
and bring it to the website later. GitHub's workflow (`.github/workflows/fig12-openfoam.yml`) stays in place; Kaggle
runs the same case files with the same code.

## Files

- `make_notebook.py`: writes one self-contained Kaggle notebook for one case of `notes/fig12/of-request.json` (or a
  case already run on GitHub, `notes/fig12/of-runs/<name>/case.json`), pinned to a full commit of this repository:
  ```sh
  python3 tools/fig12/kaggle/make_notebook.py swing-slip-coarse --commit <40-character sha>
  python3 tools/fig12/kaggle/make_notebook.py swing-slip-coarse --set name=test --set end=0.05   # a short test
  ```
  The notebook: environment check (cores, memory, OS, disk); OpenFOAM 13 from dl.openfoam.org with the workflow's own
  commands (Kaggle runs Ubuntu 24.04, "noble"), Node if missing, and the ordinary user `foam` (OpenFOAM refuses to
  compile the case's coded monitor as root); a sparse clone of `tools/fig12` and `public/scripts` at the pinned commit
  (Kaggle's `save_notebook` drops attached data, issue Kaggle/kaggle-cli#1140); `tools/fig12/of/make_case.py`;
  `tools/fig12/of/run.sh` on all cores with a progress line every 3 minutes and the monitors copied out during the
  run; then the outputs.
- `notebooks/<case>.ipynb`: the generated notebooks, exactly the text sent to Kaggle.
- `compare.py`: one case on two machines, column by column (time steps are adaptive, so one run is interpolated onto
  the other's times; rows at the same time are also compared exactly), then both through
  `tools/fig12/of/analyse_swing.py`, with the wall times.

## Outputs, in `/kaggle/working/<case>/`

The layout of `notes/fig12/of-runs/<case>/`: `stoutMonitor.dat.gz`, `cartMonitor.dat.gz` (cart rides),
`log.foamRun.tail.gz`, `walltime`, `case.json`; plus `surface/` (the mesh and `alpha.stout` at every written time, from
which the free surface is drawn; the compact playback packs are Phase 2), `params.json`, `timing.json` (cores, OS,
OpenFOAM version, mesh cells, wall time per stage), `progress.log` and `SHA256SUMS.txt`. The notebook ends with an error
if the solver failed or the monitor stops before the end time.

## Measured

- Local test (this repository's container, 4 cores, 12 November 2026): the coarse slip case cut to 0.05 s ran through
  every cell in 15 s; mesh 67,008 cells (stout and air); against the GitHub run of the same case over the same 0.05 s,
  every monitor column agreed within 1·10⁻⁸ in absolute terms.
- Kaggle: see `notes/fig12/handoff-fig12-guinness.md`, section 10, and `notes/fig12/of-runs/index.json`.

## Rules

Every launch on Kaggle needs a run card and the user's yes (skill `kaggle-gpu-run`); notebooks are private; no
token anywhere; a failed run is reported, never relaunched without a yes. The OpenFOAM runs use CPU sessions only
(`enableGpu` false), which spend no GPU hours.
