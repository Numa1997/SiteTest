# Fig. 15, Resonant Tunnelling: state of generation 2

Written 13 November 2026, 23:45 UTC, so that the work survives a context compaction; last updated 14 November 2026, 00:30 UTC.
A chat that has lost its context rereads this file first and continues from "Next".

## What is live
- <https://phyeinusul.com/simulations/resonant-tunnelling.html>: generation 1 (115 3D runs, merge 12e710a9, live since
  13 Nov 19:55 UTC). Nothing of generation 2 is on `main` yet; it lives on branch `claude/fig15-resonant-tunnelling`.

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
  - shard 1 `numakoudsie/fig15-rt3d2-shard-1-of-6`, launched 20:24 UTC, commit cdcade4: DONE, 624 runs, 0 failed,
    621 files, SHA-256 0 bad; downloaded
  - shard 2 `numakoudsie/fig15-rt3d2-shard-2-of-6`, launched 20:48 UTC, commit cdcade4: DONE, 623 runs, 0 failed,
    620 files, SHA-256 0 bad; downloaded
  - shard 3 launched 14 Nov 00:12 UTC (kernel 144885421, version 1); due about 03:40 UTC
  - shard 3: DONE, 623 runs, 0 failed; filed and uploaded (14 Nov 03:55): 1853 runs, 3.24 GB in R2
  - shard 4 launched 14 Nov 01:22 UTC (kernel 144897867); due about 04:50 UTC. Check-in scheduled 05:00 UTC.
  - shard 5 launched 14 Nov 03:52 UTC (kernel 144916686); due about 07:20 UTC. Then fix1; shard 6 after shard 4.
  - Kaggle output paths since shard 3: `2026-11-14/rt3d2/*` (the runner's date), not `2026-11-13/`.
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

## Where things are (this container; lost if the container is replaced, then download again from Kaggle)
- Scratchpad: `/tmp/claude-0/-home-user-SiteTest/27c35645-8316-5eb3-8583-c6488d96fcdb/scratchpad/`
  - `kaggle_g2/<slug>/`: each notebook's output (`rt3d2_all_<i>of6.tar`, `index.json`, `runs.jsonl`, `timing.json`,
    `progress.log`, `done.txt`, `urls.txt`). Download: `list_notebook_session_output` (too big for the reply: it is saved to a
    tool-results file; read the `files` list with python), keep `2026-11-13/rt3d2/*` and `progress.log`, fetch with curl.
  - Check: every .bin in the tar must hash to one of the SHA-256 the notebook's index gives for its name.
  - `kaggle_g2/smoke/`: smoke test output. `work/page_gen1.html`: copy of the generation-1 page.
  - `work/addresses_worker.{log,json}`: the address check of 13 Nov.
- Kaggle allows two GPU sessions at once for the whole account (other sessions' notebooks count). Quota 30 h a week,
  resets Saturday 00:00 UTC.

## Files of generation 2 (all on the branch)
- `tools/kaggle/resonant-tunnelling/rt3d2.py` solver, `rt3d2_run.py` runner (job list, `JOBSEL`, `SHARD`, `FIX1`),
  `build_rt3d2.py` writes the loaders, `rt3d2_{smoke,all_<i>of6,fix1}.ipynb` loaders, `file_rt3d2.py` filer
  (`python3 file_rt3d2.py <src with one folder per slug> <date> <runs destination>`), `read_rt3d.py`, `tm.py`, `iv.py`.
- `public/simulations/resonant-tunnelling.html` the gen-2 page; `public/scripts/rt3d-view.js`, `public/scripts/rt3d-worker.js`.
- `worker/r2.js`, `wrangler.jsonc` the Worker; `tools/inventory.py`, `docs/files.md` registered.
- Data to come: `public/data/resonant-tunnelling/<date>/kaggle/index.json` and a gen-2 entry (kind `rt3d2`) in
  `public/data/resonant-tunnelling/generations.json`; the run files go to R2, not to the repository.

## Commits on the branch (oldest first)
cdcade4 solver and job list · 17d45c7 loaders at cdcade4, filer draft · f87277d gen-2 page · 6314da1 Worker ·
a39e2cc run length counts the trailing edge · 57770d2 JOBSEL fix1 · 8324006 loaders 3-6 and fix1 at 57770d2 ·
c80244e inventory · 923b43f filer per-notebook commit, replaced record · c21bd7e nosniff · a425911 .gitignore ·
4a12490 this file · then: filer dedupe and I-V by spec; page guard for a missing gen-2 index.

## Done
- R2 token saved (14 Nov 01:20 UTC) on the Default environment, injected by the proxy for api.cloudflare.com; tested
  (put, get, delete a probe). Account id in scratchpad `cf_account_id`. Uploader `scratchpad/r2/up.sh <file> <prefix>`
  (PUT, checks R2's etag = MD5, retries; log lines `OK key bytes md5`). Upload only from the filer's destination folder
  (the filer decides which copy of a spec computed twice is kept).
- Generation date 2026-11-14: keys `resonant-tunnelling/2026-11-14/runs/<file>`; generations.json has the rt3d2 entry.
- Shards 1-2 filed (1237 runs, 2.15 GB) and uploaded: 1237 OK, 0 failed (`scratchpad/r2/up_shards12.log`).
- Page checked on the real shard 1-2 data (local server `scratchpad/srv.py` maps /r2/ to the files): no errors at
  390 and 1440 px. Its lead and meta description still speak of generation 1: rewrite with the note.
- Filer fixed (14 Nov): a spec computed in two groups (A and F at bias 0; three such names per shard) is filed once with
  `groups` and `also_computed`, not as a replacement; only a fix notebook replaces; the I-V takes the diode's points by spec.
- Page guard (14 Nov): the page reads only a generation of kind `rt3d2`; without one it says so instead of failing.
- Generation 1 live since 13 Nov 19:55 UTC (115 runs, merge 12e710a9).
- Gen-2 solver, runner, loaders, filer `file_rt3d2.py` (SHA-256, per-notebook commit, replaced-run record, I-V, exact curves).
- Gen-2 page on the branch (chips for shape, N, R, V0/D, P, sigma_x; bias slider; Fig. 15b-e), tested on the smoke runs.
- Worker `worker/r2.js` and `wrangler.jsonc`, checked with `wrangler deploy --dry-run` and `wrangler dev`.

## The writing session (14 Nov 01:33 UTC)
- A separate cloud session writes the lecture note on branch `claude/fig15-gen2-note` (its own state file
  `notes/fig15/NOTE_STATE.md`; "READY at <commit>" when done). It owns `public/scripts/resonant-note.js`, the page's lead and
  meta description, `notes/fig15/gen2_numbers.py`, and the note sections of the Fig. 15 doc. Merge that branch into this one
  before the final check; then rerun its gen2_numbers.py on the full index and refresh the numbers if needed.

## Finishing each shard
- Download into `scratchpad/kaggle_g2/<slug>/` (see above), then `scratchpad/after_shard.sh`: files ALL shards again (the filer
  asserts every SHA-256), uploads what is new or changed (MD5 against the upload logs), prints keys in R2 and GB filed.

## Measured on the page (14 Nov, local server, headless Chromium without GPU)
- Index of 1237 runs: 1.02 MB, 169 kB gzipped; full batch about 3 MB, about 0.5 MB gzipped. Parsed once at load.
- One run file 1.7 MB (192 box), 3.3-3.4 MB (256, 512). A loaded run now holds 4-10 MB (8-bit levels), 6 kept.
- Page work per frame 1.5-3 ms (interpolate + sheet, WebGL submit, charts); the frame rate in headless Chromium (50-125 ms)
  is the software renderer, not the page. A chip switch: 160-280 ms locally until the new run plays.
- A fast drag over 20 energies: settles 0.3 s after release (one file in flight at a time).

## Left (Next = the first open item)
1. Shards 4-6 and the fix job (two at a time as slots free; check-ins by `send_later`); download each, check SHA-256.
2. File with `file_rt3d2.py` (date of filing), add the generation to `generations.json`.
3. Upload the run files to R2; measure the GB. The token: `request_credential` for api.cloudflare.com (an R2 Admin
   Read & Write token; it is saved on the Default environment). Upload: PUT
   `/client/v4/accounts/<account id>/r2/buckets/phyein-usul-runs/objects/<key>`; account id from GET /client/v4/accounts.
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
