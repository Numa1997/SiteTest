# Proposed actions (Phase 1 output; nothing here has been done)

Nothing below happens without the owner's explicit yes, group by group (brief, section 2). Every group says: the exact artefacts, why,
what it frees, what it breaks and how that is prevented, and whether it can be undone. Facts have a handle in `INVENTORY.md`,
`inventory.json` or `raw/`. Marks: **Fact**, **Inference**, **Opinion**.

Three limits that shape the order (Facts):
- The Kaggle connector has **no delete operation** (its tools: save, create session, cancel, upload dataset file; no delete). Kaggle deletions are therefore by hand on kaggle.com; I give exact URLs and a safe order.
- The Fig. 15 correction session and Fig. 16 session are running: **no touch** of `claude/fig15-correction`, `claude/fig16-cart`, Fig. 15's R2 prefix, and (my reading) the Fig. 15 notebooks and generation-1 folder.
- Phase 2 needs R2 writes for "archive" groups; the brief allows them only after a yes.

## Order (safest first)

A (tests) then B (duplicates) then C (merge docs defect and scripts) then D (archive small data) then E (Fig. 12 and Fig. 14 notebooks after preserving) then F (Fig. 15, only after the correction session has filed). Opinion: do A, B and C together as the first yes; they carry almost no risk.

## Group A: delete test notebooks on Kaggle (9)

- **Artefacts** (`https://www.kaggle.com/code/numakoudsie/<slug>`): `notebookddfec594b7`; `html-panel-test-ripple-tank-computed-on-kaggle`; `phyein-sim-native-install-test`; `phyein-sim-run-case`; `phyein-sim-run-case-fem`; `phyein-sim-jax-swingup-gpu`; `fig15-rt3d-smoke`; `fig15-rt3d2-smoke`; `schrodinger-sphere-gpu-smoke-test`.
- **Reason:** each is a one-off test; no record names any of them (checked in the three `generations.json`, the Fig. 15 `index.json`, `fig12/index-jax.json`).
- **Frees:** 9 of 35 notebooks; outputs small (the largest, `ripple_tank.html`, is 15.8 MB).
- **Breaks:** one thing. `docs/kaggle-pipeline.md` ("Measured numbers") quotes the timings of the smoke notebook (1.61 ms per split-step, 2.6 ms with measurements). **Prevention:** first copy that notebook's `timing.json` into `notes/inventory/raw/` with its SHA-256, and cite it in the doc.
- **Undo:** no (Kaggle delete is final). **Inference:** the first six are re-creatable from their sources in this repository or from `numa1997/phyein-sim`; the smoke tests from `tools/kaggle/**/*smoke.ipynb`.
- The scripts of `phyein-sim` live in a different GitHub repository; I do not touch it.

## Group B: delete duplicate and orphan notebooks on Kaggle (4 + 1)

- **B1 artefacts:** `schrodinger-shapes-3d-v2-a`, `-b`, `-c`, `-d`.
- **Reason:** they computed the same 243 runs (61+61+61+60) as `schrodinger-shapes-3d` v2 (GPU), at the same commit `94d1281`, on CPU in 8 475 to 11 097 s each. The site holds the GPU output (243 of 243 SHA-256 equal). No record names a to d.
- **Frees:** 4 notebooks, about 118 MB of Kaggle output.
- **Breaks:** nothing live. **Prevention:** before deleting, I check the four index files against the site's SHA-256 (not done yet; the a to d outputs may differ at float level from the GPU ones, which would not matter because the site uses the GPU ones).
- **Undo:** no; reproducible only by another 3 h of CPU time each.
- **B2 artefact:** `schrodinger-sphere-3d-generation` (81 runs, 60 MB, `runs3d/`). On no page, in no record. **Decision for the owner:** archive its output to R2 (60 MB) and then delete, or delete. Option 1 costs 60 MB of R2 (61 % becomes 61.6 % of the free tier). Opinion: archive; the 3D cloud may be wanted for a later Fig. 14 view. Case against: nothing reads it and `wave3d` replaced it.

## Group C: repair the document defect and merge scripts (repository)

- **C1 Defect:** `docs/kaggle-pipeline.md` lines 181 to 185 (`<<<<<<< HEAD` ... `>>>>>>> origin/main`). Fix by keeping the "run 10's controlled rides with run 8's other rides" wording (the newer one). Frees 0; breaks nothing; undo by git.
- **C2 Fig. 15 scripts, one maintained set.** Keep `rt3d2.py`, `rt3d2_run.py`, `file_rt3d2.py`, `build_rt3d2.py`, `tm.py`, `iv.py`, `exact1d.py`. Remove generation 1's `rt3d.py`, `rt3d_run.py`, `file_rt3d.py`, `build_rt3d.py` and the 5 generation-1 notebook sources (`rt3d_all_{0..3}of4.ipynb`, `rt3d_singles_v2.ipynb`). **Not now:** `rt3d.py` is referenced by 13 other files under `tools/` and 3 live files; an import check is needed first, and Fig. 15 is on hold (the correction session may edit these files). Hold until F.
- **C3 Fig. 15 shard notebooks:** `rt3d2_all_{0..5}of6.ipynb` are six files identical except one number; `build_rt3d2.py` already writes them. Remove the six, regenerate on demand. Frees 9 kB. Hold with C2.
- **C4 Fig. 12 Taichi scripts:** remove `solver.py`, `rides.py`, `free_swing.py`, `free_params.py`, `env.py`, `store_rides.py` (62 kB) from `tools/fig12/kaggle/`; the JAX files `stout_jax.py`, `run_b.py`, `pack_ride.py`, `check_run.py` replace them. The Kaggle notebooks of 12 to 13 Nov fetch them at commits `70703de` and `3d6f61a`; git history keeps those files. **Prevention:** tag those two commits (see Group G) so they cannot be lost. Docs naming them (`docs/simulations/fig12-beer-slosh.md`, `docs/files.md`) updated in the same commit.
- **C5 Fig. 14 builders:** eight `build_*.py` (flat, pillar, radial, shapes3d, full, smoke, 3d, wave; 48 kB) become one parametrised `build_notebook.py`; the eight `.ipynb` sources are generated. Frees about 40 kB; the value is fewer files to read.
- **C6 Orphan scripts (95):** the `orphan` rows of `inventory.json` (46 under `notes/fig11`, 8 under `tools/`, the rest spread over `notes/fig01` to `fig15`, `home`, `droplets`, `electron-beam`, `rotor-pendula`). Proposal: the owner reviews the list in two minutes; then delete them (git history keeps them). Frees 251 kB; breaks nothing referenced.
- After every repository change: `npm run build`, `python3 tools/inventory.py --check`, `tools/perf/addresses.cjs`, and a browser check of affected pages at 390 and 1440 px (brief 2.3). **Undo:** git revert.

## Group D: archive small data the site does not play (repository to R2 or tag)

- **D1 Fig. 12 `public/data/fig12/2026-11-13-run8/`** (2.7 MB, 11 files). 5 files are byte-identical to files in `2026-11-14-run10/`, 6 are replaced by run 10's corrected controllers. The raw `.npz` of run 8 are on Kaggle (v8) only, and `generations.json` names run 8. **Prevention:** keep `index-jax.json` of run 8 and its record in `generations.json`; copy the 6 distinct files to R2 `fig12/2026-11-13-run8/` with SHA-256 before removing them from `public/`.
- **D2 Fig. 12 `2026-11-12/` and `2026-11-13/`** (2.1 MB and 4.6 MB). Opinion: **keep**; they cost 6.7 MB and are "kept for the record" by the generation file.
- **Frees:** 2.7 MB from the deploy (trivial). **Undo:** yes (copy back from R2; git history).
- Honest value: small. The reason to do D1 is tidiness, not space.

## Group E: delete provenance notebooks on Kaggle after preserving (Fig. 12 and Fig. 14)

Rule from the brief: a notebook named by a live record is deletable only after the record points to a preserved copy.

- **E1 Fig. 12 Taichi notebooks** `guinness-on-a-cart-stout-sloshing` (v5, `rides.json` 1.80 MB) and `guinness-free-swing-v2` (v5, `free_swing_v2.json` 0.3 MB). Preserved copies already on the site: `fig12/2026-11-13/rides.json` (1 795 977 B, same size as Kaggle's 1.80 MB) and `fig12/2026-11-12/free_swing_v2_repair.json` (339 570 B, about the 0.3 MB). **Prevention:** compare SHA-256 of the Kaggle files against the site's before deleting; rewrite `fig12/generations.json` to add `preserved: <path>` and keep slug, version, commit as history. Frees 2 notebooks. Undo: no.
- **E2 Fig. 12 JAX notebook** `guinness-on-a-cart-stout-in-jax` (10 versions). **Keep.** Its versions 6 to 10 hold the only raw `.npz` of runs 6 to 10; it is the current notebook and costs nothing. Option: copy the `.npz` of v6, v8, v10 (12 + 12 + 10 files; sizes unmeasured) to R2 `fig12/<date>/raw/` first; then it could go. Opinion: keep.
- **E3 Fig. 14, six notebooks** (`schrodinger-sphere-full-grid`, `-3d-wave`, `schrodinger-flat-wall`, `schrodinger-pillar`, `schrodinger-spherical-wave`, `schrodinger-shapes-3d`). The site holds their data (amplitude; 405 runs 62.7 MB etc.). **One exception:** `full-grid` also holds the phase (159 MB on Kaggle against 62.7 MB on the site), which no page reads. **Decision for the owner, one at a time:** (a) keep these six (no cost), (b) save the phase data to R2 (159 MB) then delete, (c) delete and accept losing the phase data. Opinion: (a). Case against: six notebooks stay in the account for nothing visible.
- **Frees:** up to 8 notebooks and about 0.55 GB of Kaggle output. **Breaks:** the provenance of Fig. 14 data unless the records are rewritten first (`schrodinger-sphere/generations.json`, `shapes3d/index.json` source and version2 blocks) to name the preserved copy.

## Group F: Fig. 15 (HOLD until the correction session has filed its new generation)

- **F1** Kaggle: `fig15-rt3d2-shard-1..6-of-6`, `fig15-rt3d2-fix1` (7 notebooks, 6 552.5 MB of tars + 0.1 GB) and the generation-1 five (`fig15-rt3d-shard-1..4-of-4`, `fig15-rt3d-singles-v2`). **Fact:** all 3 697 generation-2 files are in R2 (sizes equal), indexed with SHA-256. **After** the hold: rewrite the index `notebooks` block to add `preserved: R2 key prefix`, keep slug, version, commit as history, then delete by hand. Frees 12 notebooks and about 6.7 GB of Kaggle output. Undo: no.
- **F2** Repository: `public/data/resonant-tunnelling/2026-11-13/kaggle/` (115 runs, 184.7 MB, generation 1, not played). Move the runs to R2 `resonant-tunnelling/2026-11-13/runs/`, keep `derived/exact-1d.json` (live) and the index. Frees 184.7 MB of the deploy (20 % of the repository). R2 grows 6.527 to 6.71 GB (67 % of the free tier). Undo: yes.
- **F3** R2 prefix `resonant-tunnelling/2026-11-14/runs/`: keep. Nothing is redundant.
- **F4** The 15 `replaced` runs: the old versions exist only inside the tars of shards 1 and 2 on Kaggle; deleting those notebooks loses them. The index records them under `replaced`. They are superseded by design.

## Group G: pin the commits that Kaggle notebooks fetch (safety, no deletion)

Nine commits are on no branch of the clone (`c705a42`, `10dc1d6`, `5941f63`, `7083b64`, `76c7ce0`, `89f6e9d`, `13dda4c`, `70703de`, `3d6f61a`). Today each serves its files (HTTP 200). Propose lightweight tags `kaggle/<notebook-slug>` at every commit a notebook or record names (20 commits), so the proof of origin cannot disappear. Frees 0; breaks nothing; undo: delete the tag. Opinion: do this early, it is the cheapest protection in the whole plan.

## Group H: keep (named so nothing is touched by accident)

R2 prefix `resonant-tunnelling/2026-11-14/runs/`; `public/data/schrodinger-sphere/**` (618.6 MB, all loaded by the page); `public/data/fig12/2026-11-14-run10/`; the three `generations.json`; the Fig. 15 generation-2 index; Workers `phyein-usul` and `stellenrecherche`; the scheduled task `trig_01QPpDyUsC3M8uFbcr13B1EJ` until the R2 key is deleted; the Fig. 12 JAX notebook; all derivation scripts in `notes/` and `tools/` marked provenance (257); live tools (19).
Worker `kaggle-bridge` (starter code only): **decision for the owner:** keep for the planned bridge, or delete. Opinion: keep; it is empty and free.

## Totals if everything proposed were done (Facts as measured; Inference where noted)

| Place | Before | After A, B, C (non-F parts), D, E1, G | After F as well |
|---|---|---|---|
| Kaggle notebooks | 35 | 19 (A 9, B1 4, B2 1, E1 2 removed) | 7 (F1 removes 12) |
| Kaggle output (measured part) | at least 7.3 GB | about 7.1 GB | about 0.4 GB |
| R2 | 6.527 GB | 6.527 GB (6.59 GB if B2 is archived there) | about 6.77 GB |
| Repository (tracked) | 907.3 MB | about 907 MB | about 722 MB (F2 moves 184.7 MB out) |
| Scripts and notebooks | 462 | 346 if all 95 orphans go, 441 if none do | 15 fewer (F: Fig. 15 generation 1 and shard notebook sources) |

## The layout rule for the future (proposal; to be written into `docs/kaggle-pipeline.md` in Phase 2)

1. **One notebook per figure and generation, or the fewest the work needs.** Kaggle allows two GPU sessions at once, so two shard notebooks are the honest minimum for large sweeps. A rerun or a fix is a new **version** of the same notebook, not a new slug.
2. **Names:** `fig<N>-<gen date>` and, for shards, `fig<N>-<gen date>-shard-<k>` (example: `fig15-2026-11-14-shard-3`). No `smoke`, `test`, `v2-a` slugs stay after the run they served; a smoke test is deleted the day its numbers are copied into the repository.
3. **One home per artefact:** code in `tools/kaggle/fig<N>/` (one solver, one runner, one filer, one notebook builder per figure); data the page plays in `public/data/fig<N>/<gen date>/` (small) or R2 `fig<N>/<gen date>/runs/` (large); the record of origin in that folder's `index.json` (`notebook`, `version`, `commit`, `sha256`, and **`preserved`**, the path of the copy that remains if the notebook is deleted).
4. **Provenance pinned:** every notebook's commit gets a tag `kaggle/fig<N>-<gen date>[-shard-k]`.
5. **Superseded data:** when a generation is replaced, its runs move to the archive prefix (R2 `fig<N>/<gen date>/`), the page keeps only the index; scripts of the old generation are removed from `tools/` the same commit, git history keeps them, and every doc that names them is updated (`tools/inventory.py --check` fails otherwise).
6. **Scratch is not an archive:** session scratchpads are never the only copy; a run is "done" when its SHA-256 is in the index and the data is in its home.
7. **Inventory is regenerated, not hand-kept:** `tools/inventory.py` gains a section that lists notebooks and R2 prefixes named in the indices (proposal, Phase 2).

## What I need from the owner (one decision at a time)

First yes, offered as one group: **A + B1 + C1 + G** (nine test notebooks to delete by hand, four duplicate notebooks, the doc defect, 20 tags). Everything else waits for its own yes.
