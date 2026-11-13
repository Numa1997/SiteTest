# Fig. 15, Resonant Tunnelling: state of generation 2

Written 13 November 2026, 23:45 UTC, so that the work survives a context compaction. Updated as steps finish.

## Aim
The whole parameter space of resonant tunnelling, computed in 3D on Kaggle GPUs and animated on the page
(<https://phyeinusul.com/simulations/resonant-tunnelling.html>). Energy and resonances resolved finely; walls, discs
(R 2, 4, 6, 9, 12) and shells (R 3, 5); height, thickness and spacing ranges; 3, 5 and 10 barriers in a row; the device
under bias V(x) - eV x / L with the I-V curve built from the runs; long packets. Same pipeline as generation 1:
3D split-step, SHA-256 per file, index.json with notebook, version and commit, meshed sheet with glass barriers,
one brightness scale per run, smooth playback.

## The batch (3739 runs, approved by the owner; walls in full 3D too)
- Solver `tools/kaggle/resonant-tunnelling/rt3d2.py`, runner `rt3d2_run.py`, loaders built by `build_rt3d2.py`.
- Groups: A pairs 1128, B shells 188, C heights/thicknesses 564, D singles 376, E N = 3, 5, 10: 423, F bias 1000, G long packets 60.
- Six shards `J[i::6]`, two at a time (Kaggle allows two GPU sessions):
  - shard 1 `numakoudsie/fig15-rt3d2-shard-1-of-6`, launched 20:24 UTC, commit cdcade4
  - shard 2 `numakoudsie/fig15-rt3d2-shard-2-of-6`, launched 20:48 UTC, commit cdcade4
  - shards 3-6 `numakoudsie/fig15-rt3d2-shard-{3..6}-of-6`, loaders `rt3d2_all_{2..5}of6.ipynb`, commit 57770d2
  - fix job `numakoudsie/fig15-rt3d2-fix1`, loader `rt3d2_fix1.ipynb`, commit 57770d2: reruns the 15 runs of shards 1-2
    whose run length at cdcade4 was more than 15 % short (`FIX1` in rt3d2_run.py).
- Each shard about 3.3-3.5 h. Check-in scheduled 23:50 UTC (13 Nov) to launch the next pair.
- Smoke test `numakoudsie/fig15-rt3d2-smoke` v1: 4/4 runs, 0.96-0.99 ns per cell-step, walls vs 1D twin 1.8e-4.

## R2 (run files are too big for the repository)
- The owner switched R2 on (13 Nov, about 22:20 UTC). Bucket `phyein-usul-runs` created (ENAM).
- Upload token: one R2 token asked once through the secure form; never printed, logged or committed.
  Bucket-scoped object tokens work only with the S3 API, so the form needs an R2 token for api.cloudflare.com.
- Keys `resonant-tunnelling/<date>/runs/<file>.bin`; served by the site's Worker at `/r2/<key>` (`worker/r2.js`,
  binding `RUNS` in `wrangler.jsonc`; everything else falls through to the static assets unchanged).
- Keep the total under the free 10 GB and state the measured GB; beyond that, tell the owner the cost first
  ($0.015 per GB-month).
- Before the Worker change reaches `main`: `tools/perf/addresses.cjs` against a local build with the Worker.
  Run 13 Nov 22:15: 239 of 239 addresses right, 83 of 83 links reach 200; one page error on the gen-2 page with
  only gen-1 data present (to be made robust). Touch no other Worker.

## Done
- Generation 1 live since 13 Nov 19:55 UTC (115 runs, merge 12e710a9).
- Gen-2 solver, runner, loaders, filer `file_rt3d2.py` (SHA-256, per-notebook commit, replaced-run record, I-V, exact curves).
- Gen-2 page on the branch (chips for shape, N, R, V0/D, P, sigma_x; bias slider; Fig. 15b-e), tested on the smoke runs.
- Worker `worker/r2.js` and `wrangler.jsonc`, checked with `wrangler deploy --dry-run` and `wrangler dev`.

## Left
1. Shards 3-6 and the fix job; download each output, check SHA-256.
2. File with `file_rt3d2.py` (date of filing), add the generation to `generations.json`.
3. Upload the run files to R2; measure the GB.
4. Finish the page against the real data; screenshots at 390 and 1440 px; frame times.
5. Lecture note and docs for the new parameter space (spacing, superlattice bands, side leak against R, I-V from runs,
   long packets); `docs/simulations/fig15-resonant-tunnelling.md`, `docs/kaggle-pipeline.md`, `docs/usul.md` (Worker).
6. Address check again, merge to `main`, verify live (including the `/r2/` cache header), report once.

## Rules (the owner's)
- Everything computed on Kaggle GPUs, in 3D; no CPU stand-ins.
- Every GPU launch needs a bill and the owner's yes (this batch and the fix job are approved).
- Never write the owner's name or e-mail into outside requests; never print or commit a token.
- Merge and publish without asking once finished, checked against `main` and tested in a real browser; then verify live.
- Report in one line at each pair's launch and once when live.
