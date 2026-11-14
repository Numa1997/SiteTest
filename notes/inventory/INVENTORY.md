# Inventory of Phyein Usul's computations

Phase 1, read-only. Written 14 November 2026 from `origin/main` = `039c1d3`. Every number below was measured on that day; the raw
records are in `notes/inventory/raw/` and every row is in `inventory.json`. No Kaggle notebook, R2 object, repository file or branch
was changed.

How to read the marks: **Fact** has a handle you can run; **Inference** is my reasoning from facts; **Opinion** is my judgment.

## Totals

| Place | Count | Size | Handle |
|---|---|---|---|
| Kaggle notebooks (account `numakoudsie`) | 35 (24 GPU, 11 CPU); 0 datasets; 0 models | outputs measured **at least 7.3 GB** (Fig. 15 gen. 2 tars 6.55 GB; Fig. 14 0.72 GB; Fig. 12 and Fig. 15 gen. 1 outputs not measured) | `raw/kaggle-notebooks.json`, `raw/kaggle-outputs.md` |
| Kaggle GPU quota | 48 167 s used of 108 000 s (45 %), reset 2026-11-21 00:00 UTC | | `get_accelerator_quota` |
| R2 bucket `phyein-usul-runs` | 1 prefix, 3 697 objects | **6.527 GB** (6.08 GiB; free tier 10 GB: 61 %) | `raw/r2-summary.md` |
| Repository `Numa1997/SiteTest` | 907.3 MB tracked (6 392 files in `docs/files.md`) | `public/data` **818.3 MB** = 90 % of it | `git ls-files`, `du` |
| Scripts and notebooks | 462 files (194 under `tools/`, the rest under `notes/`) | 1.9 MB | `scripts.json` rules below |
| Cloudflare Workers | 3: `phyein-usul`, `kaggle-bridge`, `stellenrecherche` | | `workers_list` |
| Scheduled tasks | at least 20 (the first page; more exist); **1 enabled** (filtered list) | | `list_triggers` |
| Remote branches | 126 (13 merged into `main`, 112 not) | | `git branch -r --merged` |

Statuses of the 462 scripts (rule-based, see "How statuses were set"): 19 live, 257 provenance, 14 superseded, 77 test, 95 orphan.
Statuses of the 35 Kaggle notebooks: 19 provenance, 9 test, 5 orphan, 2 superseded, none "live" (the site never calls Kaggle).

## The picture in one paragraph

Think of a kitchen after a busy week. Kaggle is the oven room: 35 trays, most of them still holding the baked goods. The site and R2
are the shelf: what visitors are served. The repository `tools/` and `notes/` are the recipe drawers. What the owner cannot see is
which trays are the only copy of something, which are copies of what is already on the shelf, and which were only test bakes. This
inventory answers exactly that, by comparing hashes and sizes, not by guessing.

## Findings that decide what can be cleaned (all Facts)

1. **R2 is exact.** The 3 697 files named in `public/data/resonant-tunnelling/2026-11-14/kaggle/index.json` are the 3 697 objects in R2: 0 missing, 0 extra, 0 size differences. Nothing in R2 is redundant.
2. **Fig. 15 generation 2 is fully preserved off Kaggle** (R2 + index with SHA-256). The Kaggle shard tars (6 552.5 MB) hold the same runs plus 42 duplicates and the 15 replaced runs. The notebooks are still named as origin by the index: provenance, not deletable until the record says where the preserved copy is. The correction session is running: HOLD.
3. **Fig. 14 `shapes3d`: the live data equals the GPU notebook's output.** 243 of 243 corrected runs and 36 of 36 wave files have the same SHA-256 as the site. The four CPU notebooks `schrodinger-shapes-3d-v2-a..d` computed the same 243 runs again (61+61+61+60), took 8 475 to 11 097 s each on CPU, and no record names them.
4. **Fig. 14 `schrodinger-sphere-3d-generation` (81 runs, 60 MB) is on no page and in no record** (the page reads `wave3d`, from `schrodinger-sphere-3d-wave`).
5. **Fig. 14 `schrodinger-sphere-full-grid` holds the phase data** (159 MB on Kaggle against about 63 MB of amplitude on the site, per `docs/kaggle-pipeline.md`): its Kaggle output is the only copy of that phase.
6. **Fig. 12 raw `.npz` of runs 6 to 10 exist only on Kaggle** (versions 6 to 10 of one notebook). The site holds packed JSON per ride.
7. **Fig. 12 repository folders:** the page plays only `2026-11-14-run10/` (`guinness-jax-play.js` line 7). `2026-11-13-run8/` has 5 files byte-identical to `run10/`; the other 6 are replaced by run 10's corrected controllers.
8. **Fig. 15 generation 1 (115 runs, about 185 MB in the repository) is not played** (the page reads only `kind === 'rt3d2'`, `resonant-tunnelling.html` line 259). One file of that folder, `derived/exact-1d.json`, is still read.
9. **Nine commits that Kaggle notebooks pin are on no branch of the clone** (`c705a42`, `10dc1d6`, `5941f63`, `7083b64`, `76c7ce0`, `89f6e9d`, `13dda4c`, `70703de`, `3d6f61a`). Each still answers on raw.githubusercontent.com today (HTTP 200). Inference: GitHub may drop unreferenced commits one day; a tag would pin them.
10. **A defect in a document:** `docs/kaggle-pipeline.md` lines 181 to 185 hold an unresolved merge-conflict marker on `main`.
11. **`kaggle-bridge` Worker holds starter code only** (docs say so); modified 2026-11-12.
12. **Only one branch touches data or Kaggle code besides `main`:** `claude/fig15-correction` (18 files). Not touched.

## Fig. 1 to Fig. 10

No Kaggle notebook, no R2 object, no data folder. Their only computation artefacts are working scripts under `notes/figNN/` that
produced the numbers in each lecture note (derivations, measurements, screenshots). Each is described in `docs/files.md`.

| Fig. | Where | Files | Size | Status (count) |
|---|---|---|---|---|
| 1 | `notes/fig01/` | 4 | 18.9 kB | 2 test, 2 orphan |
| 2 | `notes/fig02/` | 11 | 37.8 kB | 5 provenance, 3 test, 3 orphan |
| 3 | `notes/fig03/` | 2 | 13.9 kB | 2 test |
| 4 | `notes/fig04/` | 3 | 19.0 kB | 1 provenance, 2 test |
| 5 | `notes/fig05/` | 3 | 12.2 kB | 1 provenance, 2 orphan |
| 6 | `notes/fig06/` | 3 | 11.7 kB | 3 orphan |
| 7 | `notes/fig07/` | 6 | 10.9 kB | 3 provenance, 1 test, 2 orphan |
| 8 | `notes/fig08/` | 9 | 26.2 kB | 2 provenance, 1 test, 6 orphan |
| 9 | `notes/fig09/` | 5 | 19.1 kB | 4 provenance, 1 test |
| 10 | `notes/fig10/` | 3 | 14.2 kB | 2 test, 1 orphan |

Depends on them: the lecture notes quote their numbers; the live pages do not run them. Deleting one breaks nothing on the site; it
removes the means to reproduce a number in a note. **Opinion:** keep the derivations; the `orphan` ones are one-off screenshots
or timing probes and can go after a look.

## Fig. 11, Double Pendulum under Control (and projects 05 and 06)

135 files (132 under `notes/fig11/`, 3 under `tools/fig11/`; 505 kB: 57 provenance, 32 test, 46 orphan). 46 of them are referenced by nothing:
mostly `t_*.cjs` probes from the fluid hand-over (`fluid-ns-handover/`) and per-project `shots.cjs`. No Kaggle, no R2, no data folder.
The notebook `notes/fig11/fluid-ns-handover/waterlily/project05_fluid_step1_validation.ipynb` (18.8 kB) is referenced by nothing.
Proposed: keep derivations, archive the 46 unreferenced probes (a list is in `inventory.json`).

## Fig. 12, the Guinness pint on a cart

| Artefact | Where | Size | Status | Depends on it | Proposed |
|---|---|---|---|---|---|
| `guinness-on-a-cart-stout-in-jax` (10 versions; v10 = run 10) | Kaggle | v10: 10 files (npz + summary), 1 494 s | provenance | `fig12/generations.json` names runs 6 to 10 | keep |
| raw `.npz` of runs 6 to 9 (v6 to v9; v8 has 12 files) | Kaggle, inside that notebook | not measured | provenance (only copy) | nothing live; reproduces the packed JSON | keep, or copy to R2 `fig12/` first |
| `guinness-on-a-cart-stout-sloshing` (v5), `guinness-free-swing-v2` (v5) | Kaggle | 1.8 MB, 0.3 MB | superseded by the JAX notebook | `fig12/generations.json` (generations 2026-11-12, 2026-11-13) | delete after the record is rewritten |
| `public/data/fig12/2026-11-14-run10/` | repo | 2.7 MB, 11 files | **live** | `guinness-jax-play.js` | keep |
| `public/data/fig12/2026-11-13-run8/` | repo | 2.7 MB, 11 files | superseded by run10 (5 files identical) | `generations.json` | archive |
| `public/data/fig12/2026-11-13/`, `2026-11-12/` | repo | 4.6 MB, 2.1 MB | superseded | nothing live | keep (small) or archive |
| Scripts: JAX solver `tools/fig12/kaggle/stout_jax.py`, `run_b.py`, `pack_ride.py`, `check_run.py`, `gate_rest.py`, `note_numbers.py`, `build_note.py` | repo | 176 kB | provenance | notebook v6 to v10, page note | keep |
| Scripts: Taichi solver `solver.py`, `rides.py`, `free_swing.py`, `free_params.py`, `env.py` | repo | 62 kB | superseded by `stout_jax.py` / `run_b.py` | notebooks of 12 to 13 Nov at pinned commits (in git history) | merge (remove) |
| other `tools/fig12/*.cjs`, `.py`, `control/`, and `notes/fig12/` | repo | 453 kB for all of `tools/fig12` and `notes/fig12` | 42 provenance, 5 superseded, 13 test, 10 orphan | figure page and note | keep derivations, review orphans |

## Fig. 13, the butterfly and the gift pages

29 files under `tools/fig13/` (177 kB, all provenance). No Kaggle, R2 or data. Nothing to clean here.

## Fig. 14, the wave packet and shapes

| Artefact | Where | Size | Status | Depends on it | Proposed |
|---|---|---|---|---|---|
| `schrodinger-sphere-full-grid` v1 (405 runs) | Kaggle | 159 MB, 926 s | provenance; **only copy of the phase data** | `generations.json` entry 1 | keep, or save phase data first |
| `schrodinger-sphere-3d-wave` v1 (81 runs) | Kaggle | 101 MB | provenance | `generations.json` (wave3d) | keep or delete after rewrite |
| `schrodinger-flat-wall`, `schrodinger-pillar`, `schrodinger-spherical-wave` v1 | Kaggle | 51.9, 106.2, 7.5 MB | provenance | `generations.json` | same |
| `schrodinger-shapes-3d` v2 (GPU; v1 also named) | Kaggle | 118.5 MB, 243 runs | provenance; v2 equals site | `shapes3d/index.json` | keep until rewritten |
| `schrodinger-shapes-3d-v2-a..d` | Kaggle | 4 x about 30 MB | **orphan (duplicate)** | none | delete |
| `schrodinger-sphere-3d-generation` v1 | Kaggle | 60 MB, 81 runs | **orphan** | none | archive to R2 or delete |
| `schrodinger-sphere-gpu-smoke-test` v1 | Kaggle | small | test, but its timing numbers are cited in `docs/kaggle-pipeline.md` | docs | keep numbers, then delete |
| `public/data/schrodinger-sphere/2026-11-12/` (405 + 585 + 585 + 1 170 + 81 runs) | repo | 330.3 MB, 2 832 files | **live** | `schrodinger-sphere.html` line 1189 | keep |
| `public/data/schrodinger-sphere/2026-11-13/shapes3d/` | repo | 288.3 MB, 1 495 files | **live** | same | keep |
| `tools/kaggle/schrodinger-*` and `schrodinger-sphere` | repo | 188 kB, 40 files (32 provenance, 3 test, 5 orphan) | builders, solvers, converters, 8 notebook sources | notebooks fetch `solver.py`, `pack.py`, `flat.py`, `pillar.py`, `radial.py`, `solver3d.py`, `shapes3d_run.py` at pinned commits | merge the 8 `build_*.py` into one parametrised builder |

## Fig. 15, resonant tunnelling in 3D (a correction is running: nothing here is touched)

| Artefact | Where | Size | Status | Depends on it | Proposed |
|---|---|---|---|---|---|
| `fig15-rt3d2-shard-1..6-of-6`, `fix1` | Kaggle | tars 1 076 to 1 103 MB each, 6 552.5 MB; sessions 10 773 to 11 559 s; fix1 594 s | provenance | `2026-11-14 kaggle/index.json` (notebook, version, commit per run) | **HOLD**; later delete after record rewrite |
| `resonant-tunnelling/2026-11-14/runs/` | R2 | 3 697 objects, 6.527 GB | **live** | page via `/r2/` | keep; **HOLD** |
| `public/data/resonant-tunnelling/2026-11-14/kaggle/index.json` | repo | 2.9 MB | **live** | page, note | keep |
| `fig15-rt3d-shard-1..4-of-4`, `fig15-rt3d-singles-v2` | Kaggle | 29+29+29+28+20 runs, 271 to 383 s each | provenance (generation 1, not played) | `generations.json` entry 1 | HOLD; later delete after record rewrite |
| `public/data/resonant-tunnelling/2026-11-13/` | repo | 184.7 MB, 116 files + `derived/exact-1d.json` | superseded (runs); **live** (`exact-1d.json`) | page reads `exact-1d.json` | HOLD; then archive the runs to R2 |
| `fig15-rt3d-smoke`, `fig15-rt3d2-smoke` | Kaggle | tiny | test | none | delete |
| `tools/kaggle/resonant-tunnelling/` | repo | 201 kB, 42 files (23 provenance, 9 superseded, 4 test, 6 orphan) | gen. 1 and gen. 2 side by side | notebooks fetch `rt3d2.py`, `tm.py`, `rt3d2_run.py`, `rt3d.py`, `rt3d_run.py` at pinned commits | merge: one maintained solver, runner, filer |

## Fig. 16, the cart (in progress, branch `claude/fig16-cart`)

No notebook, no R2 prefix, no data folder exists yet; the branch holds 5 commits beyond `main` and touches no data or Kaggle file.
Not touched.

## Shared

| Artefact | Where | Size | Status | Proposed |
|---|---|---|---|---|
| `tools/inventory.py`, `redirects.py`, `i18n/`, `perf/` | repo | 213 kB, 19 files | live (build and check tools in `AGENTS.md`) | keep |
| `notes/droplets`, `rotor-pendula`, `electron-beam`, `lucretius`, `home`, `verify.mjs`, `walkcheck.cjs` | repo | 350 kB, 78 files | provenance (58), test (11), orphan (9) | keep derivations; review the orphans |
| `docs/kaggle-pipeline.md` lines 181 to 185 | repo | merge-conflict marker | defect | fix in Phase 2 |
| Worker `phyein-usul` | Cloudflare | | live | keep |
| Worker `kaggle-bridge` | Cloudflare | | starter code only | decide: keep for the bridge or delete |
| Worker `stellenrecherche` | Cloudflare | | outside scope (job list) | not touched |
| Scheduled task `trig_01QPpDyUsC3M8uFbcr13B1EJ` | Claude | | the only enabled one; fires 2026-11-15 09:00 UTC | keep until the R2 key is deleted |
| 112 unmerged remote branches | GitHub | | not computation artefacts | out of scope; not listed here |

## Tests

| Artefact | Where | Status | Proposed |
|---|---|---|---|
| `notebookddfec594b7` (Kaggle's empty starter, no output) | Kaggle | test | delete |
| `html-panel-test-ripple-tank-computed-on-kaggle` v2 (121 runs, `ripple_tank.html` 15.8 MB) | Kaggle | test (the first test of "compute on Kaggle, play on the site") | delete |
| `phyein-sim-native-install-test` v2, `phyein-sim-run-case`, `phyein-sim-run-case-fem`, `phyein-sim-jax-swingup-gpu` v2 | Kaggle | test; they fetch code from the GitHub repository `numa1997/phyein-sim`, outside this repository | delete (the repository `phyein-sim` is not touched) |
| three smoke notebooks (`fig15-rt3d-smoke`, `fig15-rt3d2-smoke`, `schrodinger-sphere-gpu-smoke-test`) | Kaggle | test | delete (keep the timing numbers cited in the docs) |

## How statuses were set

Fact-based rules, applied to each file: **live** = a build or check tool that `AGENTS.md` or `docs/` names; **provenance** = the file
produced, checks or derives a number or run stored on the site, or a Kaggle notebook fetches it at a pinned commit; **superseded** =
a newer file does the same job (named in `inventory.json`); **test** = measurement, screenshot, check or smoke script; **orphan** =
no file under `public/`, `tools/`, `notes/`, `docs/` (not counting `docs/files.md`, which lists everything) names it. The
referrer scan is by file name and path; it can miss a call built from string pieces. **Inference:** the 95 orphans need a quick human
look before any deletion; the list is the `orphan` rows of `inventory.json`.
