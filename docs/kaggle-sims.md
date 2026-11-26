# Simulations on Kaggle: computed once, stored in GitHub, served by Cloudflare, played by the page

Built 20 November 2026. Every simulation on the site (the numbered figures, the projects and the living scenes behind the pages) is to play data
computed once by a reference model on Kaggle, not physics computed in the visitor's browser. Renamed from "the scenes pipeline"
on 21 November 2026 (owner) when it became the line for all simulations; the first simulation through it was Barton's pendulums. This page explains, in
plain words, every piece that moves that data, where it lives, and why it is needed. The plan for the scenes themselves:
[notes/sims/PLAN.md](../notes/sims/PLAN.md).

## Two pipelines

**Pipeline A makes a simulation's data, once.** It runs when a simulation's model is added or changed on `main`, and never otherwise (no
timer). The model is written in the repository; a GitHub Action sends it to Kaggle; Kaggle computes the simulation's whole data in one
run (for a random one: many runs from different random starts, each recorded by its seed); the Action checks the result against
the fingerprints Kaggle printed (SHA-256) and commits it to `public/data/sims/<sim>/<date>/`; Cloudflare publishes. Nobody carries anything.

**Pipeline B shows it, on every visit.** No Action, no Kaggle, no computing: the page downloads the stored file, checks its
SHA-256, picks a random start in it (for a random simulation also one of the stored runs), and the page's drawing code animates it
(for the background scenes `public/scripts/bg-scenes.js`). So every visit looks different and nothing is computed again.

Kaggle cannot animate: it only produces files. The picture is always drawn by the page.

## Pipeline A, step by step

| Step | What happens | Where | Who does it |
|---|---|---|---|
| 1 | The scene's model `tools/sims/<sim>.py` is added or changed on `main` | GitHub | a person or a session |
| 2 | The workflow **Simulations on Kaggle** starts | GitHub Actions, [.github/workflows/sims-kaggle.yml](../.github/workflows/sims-kaggle.yml) | GitHub, by itself |
| 3 | It pushes a new version of the private CPU notebook `numakoudsie/phyein-usul-simulations`; the notebook downloads the model from GitHub at exactly that commit and runs it | Kaggle | [tools/sims/pipeline.py](../tools/sims/pipeline.py) step 1-2, [tools/sims/kaggle_sims.py](../tools/sims/kaggle_sims.py) |
| 4 | It waits for the run (asking Kaggle every 20 s, at most 30 min) | GitHub Actions | `pipeline.py` step 3 |
| 5 | It downloads the run's output and checks every file's size and SHA-256 against `index-<sim>.json`, which the notebook wrote on Kaggle; any difference stops everything | GitHub Actions | `pipeline.py` step 4 |
| 6 | It copies the files to `public/data/sims/<sim>/<date of generation>/` and adds the run to `public/data/sims/generations.json` (simulation, date, notebook, version, commit, files with SHA-256, run time) | the repository | `pipeline.py` step 5 |
| 7 | It commits as `github-actions[bot]` and pushes to `main` | GitHub | the workflow's last step |
| 8 | Cloudflare Workers Builds sees the push, builds and publishes the site; the files appear at `https://phyeinusul.com/data/sims/<sim>/<date>/…` | Cloudflare | Cloudflare, by itself (since 21 October 2026) |
| 9 | Pipeline B (below) plays it | the visitor's browser | `bg-scenes.js` |
| 10 | A second job waits until the live site lists the new generation, downloads the files from phyeinusul.com and compares their SHA-256, then opens every live page that plays the scene in headless Chromium and requires: no page errors, the file loaded, the scene reports it checked and from the same commit. The result is written to the run's summary page | GitHub Actions, [tools/sims/verify_live.py](../tools/sims/verify_live.py), pages listed in [tools/sims/registry.json](../tools/sims/registry.json) | GitHub, by itself |

The output also stays on Kaggle with the notebook version that made it (the notebook page, tab Output).

## The registry of simulations

[tools/sims/registry.json](../tools/sims/registry.json) names, for every simulation that plays Kaggle data, the files its model writes
and the live pages that play it, with a small probe the check runs in the page. A new simulation is added there, beside its model and
its player, and step 10 checks it from then on.

## How pipeline A starts

By itself, when a simulation's model `tools/sims/<sim>.py` is added or changed on `main`. Only files whose name is a simulation in
`tools/sims/registry.json` count; the other files in that folder are the machinery (`pipeline.py`, `kaggle_sims.py`,
`verify_live.py`). Only the changed simulations are computed. It can also be started by hand: GitHub, tab Actions, "Simulations on Kaggle",
"Run workflow", the scene's name. Two starts never overlap (`concurrency: sims-kaggle`).

## Figures on the line

| Simulation | Model | What is stored | Page that plays it |
|---|---|---|---|
| Home page, right margin, and `scenes.html` S3: paper globes on threads in a wind with a Kármán vortex street (`windpend`, since 25 November 2026) | [tools/sims/windpend.py](../tools/sims/windpend.py) | `windpend.bin`, 10.3 kB: one settled period of 4.69 s, three angles at 30 frames a second, then 41 streamlines of 96 points; header with parameters and checks (settled after 14 to 17 periods, energy balance 1e-11, div u / grad u 5e-11, largest swing 0.35 rad, smallest gap between globes 0.78 m) | `bg-scenes.js`, `windDraw()`, scenes `rails` and `wind` |
| No page since 25 November 2026 (was the home page's right margin from 23 November): two pendulums tied by a spring (`coupled`) | [tools/sims/coupled.py](../tools/sims/coupled.py) | `coupled.bin`, 4.2 kB: one exactly closing loop of 27.09 s, θ₁ and θ₂ at 30 frames a second; header with parameters, k solved by shooting, checks (energy kept to 4e-13, loop residual 5e-13 rad, swing crossed at 13.54 s against 13.51 s from 2π/(ω₂ − ω₁) ÷ 2, smallest gap between the bobs 0.42 m) | `bg-scenes.js`, scenes `rails` and `pairs` |
| Fig. 1, Wave interference (`wave_interference2`; generation 1 removed after 2 passed the live check) | [tools/sims/wave_interference2.py](../tools/sims/wave_interference2.py) | 290 files, 36.5 MB: the distance table of a fixed 250 × 250 grid, a ring's angle at 118 wave numbers (the page blends two neighbours exactly) and its height at γ = 0 … 0.6 in steps of 0.025, a cosine table; every table in a bottom and a top half ([fig01-wave-sources.md](simulations/fig01-wave-sources.md)) | `simulations/Circular Wave Interference Visualization.html`, its own loader (`stored()`, `load()`) |

## Pipeline B in the page

`sceneData(name, file)` in `bg-scenes.js` reads `data/sims/generations.json`, takes the newest entry of that simulation, downloads
`data/sims/<name>/<date>/<file>`, computes its SHA-256 in the browser (`crypto.subtle`) and compares it with the entry; only a matching file is handed to
the scene. A file is 4 bytes of label, a uint32 header length, a JSON header (parameters, checks, column names and units), then
int16 frames. Until the data has arrived, or if the check fails, the scene draws nothing in that place.

Paper globes in a wind (`windpend.bin`; after the header all numbers are int16: first the frames, columns θ₁ to θ₃ in 1e-4 rad,
evenly spaced over one settled period, the spacing `dt` in the header; then, from `lines.offset_int16`, the streamlines, row l
holding η of line l in mm at ξ − c t = j λ / points). A beam ξ below the top plays the stored frame of the time t − ξ / c, and
the lines are drawn shifted by c t: the wind only slides, so this is exact (the model's docstring, equation (4)). The page
integrates nothing. The spring-coupled pendulums (`coupled.bin`) played here from 23 to 25 November 2026 and Barton's pendulums
(`barton.bin`) before them; both models and their data stay, and `registry.json` lists no page for them.

Both pendulum models were first run before publishing, from their branches, as versions of the same notebook (Kaggle connector,
CPU; `coupled` as versions 7 to 9, `windpend` as versions 11 and 12), to film the result; those outputs were never committed. The
data the site plays is the one the workflow makes when a model lands on `main`.

## Keys

- **`KAGGLE_API_TOKEN`**, a repository secret (GitHub → repository Settings → Secrets and variables → Actions). The official Kaggle
  tool (`pip install kaggle==2.2.5 six`; that version imports `six` without installing it, seen on the first real run, 21 November 2026) reads it from the environment. GitHub never shows a secret again, never prints it in logs, and
  does not give it to copies (forks) of the repository.
- **`R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`** (since 25 November 2026), repository secrets for entries with
  `"store": "r2"`: an R2 API token with Object Read & Write on the bucket `phyein-usul-runs` only, made by the owner in the Cloudflare
  dashboard (R2 Object Storage → Manage API tokens). [tools/sims/r2.py](../tools/sims/r2.py) reads them from the environment and never
  prints them; without them an r2 entry stops at once with "the repository secrets R2_... are missing".
- **No GitHub key is needed**: GitHub gives every workflow run its own short-lived token; `permissions: contents: write` lets it
  commit to this repository and nothing else.

## Costs

- GitHub Actions: free; standard runners are free in public repositories, and this repository is public (checked 20 November 2026).
- Kaggle: these simulations run on CPU, which does not use the 30 GPU hours a week.
- Cloudflare: publishing is part of the existing setup; the data files are small (Barton's pendulums: 40 kB).

## What can go wrong, and what then happens

| Problem | What the workflow does |
|---|---|
| The secret is missing | stops at once: "the repository secret KAGGLE_API_TOKEN is missing" |
| Kaggle refuses the push (the tool still exits with 0) | `pipeline.py` reads the answer; without "version N successfully pushed" it stops |
| The run fails or is cancelled on Kaggle | stops with Kaggle's state; nothing is committed |
| No result within 30 min | stops; nothing is committed |
| A downloaded file differs from the index | stops naming the file; nothing is committed |
| Someone else pushed to `main` meanwhile | pulls, puts the data commit on top, pushes (three tries) |

A failed run leaves the site exactly as it was. GitHub e-mails the repository owner about failed workflow runs. A rerun on the
same day replaces that day's entry in `generations.json`, so each scene has one entry per date.

| The live site does not list the new data within 15 min, a live file differs, or a page does not play it | step 10 fails and names what failed; the data stays committed, so the cause is on the site's side |

## Tested (20 November 2026)

Pipeline A, with a stand-in for the Kaggle tool that runs the notebook here: a good run stores 3 files and a generation; a run whose
`barton.bin` has one flipped bit stops with "barton.bin: size or SHA-256 differs from the index" and stores nothing; a refused
push stops with "Kaggle did not accept the push". Pipeline B, in headless Chromium with that data: both files load, the SHA-256
matches, the pendulums play at 30 frames a second (English and Arabic home page); with one bit flipped in `barton.bin` the scene
reports "SHA-256 differs from generations.json" and draws no pendulums. Not yet tested: a real Kaggle run, and whether a commit
made by the workflow sets off Cloudflare's build as a person's commit does. Both are tested by the first real run, which needs
the secret.

## First real runs (21 November 2026)

The first automatic run stopped before reaching Kaggle: `kaggle` 2.2.5 imports `six` without installing it (fixed, PR 166). The
second run, started by hand: Kaggle accepted notebook version 1 at 19:16:33 UTC, finished in 41 s (the model 8 s), both files
matched their SHA-256, the data was committed by github-actions[bot] and was live within about a minute; the live home page
downloaded it, checked it and played it on 24 bars. `verify_live.py` passed against that live data and failed, as it should, when
asked for a commit that was never published.

Merging step 10 then set off a wrong run: the workflow took every changed `.py` file in `tools/sims/` for a scene, so the new
`verify_live.py` was sent to Kaggle as one (notebook version 2, ended in error, a few seconds of CPU, no GPU). Since then only
names listed in `registry.json` count, in the workflow and in `pipeline.py`. The run started by hand right after (version 3)
passed every step, step 10 included: published 15 s after the commit, live file SHA-256 equal, the live home page played it.

## Renamed for all simulations (21 November 2026)

The owner asked for one line for every simulation, not only the background scenes. Renamed: `tools/scenes/` → `tools/sims/`,
`scenes.json` → `registry.json` (key `sims`), workflow "Scenes on Kaggle" → **"Simulations on Kaggle"**
(`.github/workflows/sims-kaggle.yml`, input `sim`), notebook `numakoudsie/scenes-living-backgrounds` →
**`numakoudsie/phyein-usul-simulations`** (a new notebook; the old one stays on Kaggle until the owner deletes it), data
`public/data/scenes/<date>/` → **`public/data/sims/<sim>/<date>/`**, guide `docs/scenes-pipeline.md` → this file. The old data was
removed and Barton's pendulums were computed again through the renamed line.

## Large data, the GPU, and saving without clashes (23 November 2026)

Three things the line could not do were added after the double pendulum's first run (run 45254099718): Kaggle computed and
checked its 108 files, and the save then failed.

**Saving without clashes.** The save used to be "commit the data, `git pull --rebase`, push". While Kaggle computed (ten minutes),
another session merged into `main`; both changes had rewritten `docs/files.md`, the generated list of every file, git could not
combine them and the run stopped with nothing saved. [tools/sims/land.py](../tools/sims/land.py) now does the save: it keeps the new
generation's folder and its entry aside, takes the newest `main` exactly as it is, puts the folder back, adds the entry to
`main`'s own `generations.json` (every other entry stays), generates `docs/files.md` again instead of merging it, commits and
pushes; if `main` moved again meanwhile it starts over (five tries). Tested by replaying the clash in a test repository: the old
way stopped at "CONFLICT (content): Merge conflict in docs/files.md", the new way landed on the first try with the other
session's files kept.

**The GPU.** A registry entry may say `"gpu": true` (the notebook is then pushed with Kaggle's GPU switched on; this spends the
account's 30 weekly GPU hours) and `"timeout_s"` (how long the line waits for Kaggle; default 1800). The workflow job itself may
run for up to six hours.

**Large data.** GitHub keeps a repository small: files of some MB are fine, gigabytes are not. A registry entry may say
`"store": "release"` and name, in `"release_files"`, the file patterns that are large (for example `"*.pack"`). After the SHA-256
check, `pipeline.py` attaches those files to a GitHub release named `sims-<sim>-<date>` (a release holds up to 1000 files of
under 2 GiB each, with no limit on total size or traffic, GitHub's documentation "About releases"), compares each file's size in
the release with the index, and commits only the small files: `index-<sim>.json` (every file's size and SHA-256) and the model's
summary. The generation in `generations.json` records `release`, `release_files` and `gpu`. The site's Worker
([worker/r2.js](../worker/r2.js)) serves a release file under `/rel/<tag>/<file>` and passes a `Range` request through, so a page
downloads only the bytes it needs and checks them against the fingerprint it has from the repository. The live check
(`verify_live.py`, step 2b) asks every release file for its first 1024 bytes through `/rel/` and requires the right total size.
No new key is needed: the workflow's own token may write releases (`permissions: contents: write`).

`double_pendulum_smoke` ([tools/sims/double_pendulum_smoke.py](../tools/sims/double_pendulum_smoke.py)) is the test of all three: a small
part of the double pendulum's grid (240 starts with their twins, one pack) computed by the same code as the full run
([tools/sims/dp_engine.py](../tools/sims/dp_engine.py): JAX on the GPU, the page's own RK4 at h = 1/600 s in 64-bit numbers).

`double_pendulum_gpu` ([tools/sims/double_pendulum_gpu.py](../tools/sims/double_pendulum_gpu.py), added 23 November 2026 after the test passed) is
the full run of Fig. 2 through the same path: 360 000 starts with their twins, 25 packs in the release
`sims-double_pendulum_gpu-<date>`. A start the page's fixed step cannot follow (numbers no longer finite) is stored as zeros and
marked `"finite": false` in its file's header; the summary counts them as `runs_not_finite`. The page does not play this data yet.

**A fault of the `/rel/` path, found on the full run (23 November 2026).** The live check of run 45261988429 failed although the data
was saved and correct: one of the 25 packs answered 404 through `/rel/`, and a minute later answered normally; a second pass failed
on another pack. About one request in twenty to GitHub's release download came back as an error. Since then the Worker tries three
times and, if all fail, answers 502 with GitHub's status in the header `x-upstream-status`; the live check tries each file three
times and names the file and the status. This is one more reason the data moves to R2 (notes/sims/ENGINE-PROMPT.md).

## Every data set also on Kaggle, as a dataset (23 November 2026)

The user's rule: whatever its size, every run's data also stays on Kaggle, where it was made. Until this evening the engine kept it only
as the output of a notebook version, which the Kaggle site does not list as a dataset. Since then
[tools/sims/dataset.py](../tools/sims/dataset.py) files it:

- after every run (step 6 of `pipeline.py`): the whole output is checked against `index-<sim>.json` by size and SHA-256 and uploaded as
  a version of the figure's private dataset, named in the registry entry as `dataset` (`numakoudsie/fig1-wave-interference`,
  `numakoudsie/fig2-double-pendulum`, the rule of docs/kaggle-pipeline.md: one dataset per figure, `fig<N>-<topic>`); a simulation
  without a figure (Barton's pendulums) gets `numakoudsie/phyein-usul-<sim>`. Laid out as docs/kaggle-pipeline.md says:
  `phyein-usul-simulations/v<notebook version>/output/` for the files, and beside it the run's log and a `manifest.json` (size and
  SHA-256 of every file, the code's commit); the generation in `generations.json` records `dataset`,
  `dataset_path` and `dataset_note`. If Kaggle refuses, the computed data is still saved and the entry records `dataset_error`;
- for runs made before: Actions → Simulations on Kaggle → Run workflow, mode `dataset`, the simulation's name and the notebook version
  (in its `generations.json` entry, field `version`). The output is fetched again from Kaggle, which keeps every version's output.

A dataset version holds only what was uploaded with it. So that the newest version always holds every run of the figure, the
runs already in the dataset are downloaded and uploaded again beside the new one; run the filings of one figure one after another,
never two at once. The Kaggle tool packs each top-level folder into an archive of its contents, and Kaggle unpacks that at the
dataset's root, so the tree is wrapped in one more folder. The first filing (Barton's pendulums, 23 November 2026, 22:2x Berlin
time) lacked that wrapper and landed flat at the root of `numakoudsie/phyein-usul-barton`; the next filing leaves those flat files
out of the newest version (they stay in version 1). The filing waits until the dataset's version number has risen and that version
is ready, for up to 3 hours: Kaggle's "ready" alone reports the previous version while it still unpacks a new one (the first filing
of the 7 GB Fig. 2 run, 23 November 2026, 22:37 Berlin time, was reported ready after 30 s and was not there yet). Measured on that
run: download of the 7.05 GB output from Kaggle 5 s (about 100 MB/s on the GitHub runner), upload of the 6.57 GB archive 80 s, and
Kaggle's unpacking between 5 and 8 minutes (absent at 22:41, version 2 present at 22:44; it holds 34 files, the 25 packs of v6 and
the smoke run v5, pack bytes 7 056 399 034 = 7 053 765 604 + 2 633 430). A second filing started at 22:43 failed because
Kaggle answered "Not Found" to the whole-dataset download while it was still preparing the new version; it changed nothing.
**Figures made before the engine** (Fig. 15 first, 24 November 2026). Their runs live only as outputs of their own notebooks on
Kaggle. [tools/sims/file_figure.py](../tools/sims/file_figure.py), started by Run workflow with mode `figure` and the figure's key
(`fig15`) as the simulation, files them into the figure's dataset: for each notebook named in
[tools/sims/figure_datasets.json](../tools/sims/figure_datasets.json) and each of its versions (version 1, 2, ... until Kaggle has no
more), the code as it ran (`code/`), the whole output (`output/`), the log and a `manifest.json` with every file's size and SHA-256,
and how many of them are byte-identical to the files the site's index names. Each notebook is its own top-level folder of the
upload, so the runner needs room for the figure's data plus one notebook's archive. It only creates a dataset; it refuses one
that exists. The dataset's record line (`RECORD {...}` in the log) is copied into the figure's `generations.json` by the session.

**What the dataset page says** (the user's rule of 24 November 2026). Each filing also writes the dataset's subtitle and description
from the registry entry (`figure`, `page_url`, `dataset_title`, `dataset_subtitle`, `dataset_about`) and the records: the figure, its
page, what was computed, a table of every run in the dataset (folder, model, date, files, size, code commit), the layout and the
licence. No internal names stand alone and the description is never empty. The first filings of 23 November had a subtitle
built from the model's file name ("Every run of the website's double_pendulum_gpu model ...") and no description; Run workflow
with mode `dataset`, the simulations' names and version `card` rewrites the card of existing datasets without uploading anything.
The Kaggle connector cannot do it: it refuses every licence it is given ("The licenses array must specify exactly one license").
The Kaggle tool's update refuses the licence name the upload takes (`CC-BY-4.0`: "You've specified an invalid license"), so the
card is set on the dataset's own downloaded metadata, whose licence entry is kept as Kaggle wrote it, and `isPrivate` is set
to true every time: the update reads a missing `isPrivate` as false and would make the dataset public.

Before the next filing into a dataset this large, make the download of earlier runs per folder (`kaggle datasets download -f`)
and retry it while Kaggle answers "Not Found".
Kaggle's limits: 200 GB per dataset, 200 GB of private datasets in all, 50 files at the top level ([Kaggle's dataset
documentation](https://www.kaggle.com/docs/datasets)). Filing uses its own concurrency group per simulation, so it never waits behind
a Kaggle run.

## The data in Cloudflare R2 (25 November 2026)

From 25 November 2026 a registry entry can say `"store": "r2"`. Its data then goes into the Cloudflare R2 bucket `phyein-usul-runs`
and not into the repository; the site's Worker serves it under `/r2/` ([worker/r2.js](../worker/r2.js)), and pages read it through
[public/scripts/simdata.js](../public/scripts/simdata.js). Entries without `"store"` (barton, coupled, wave_interference2) and
`"store": "release"` entries work exactly as before.

**Run addresses.** A run's address is `<date>-v<version>`: the UTC day the notebook wrote in its index and the Kaggle notebook
version (for a sharded run, the version of shard 1). Its files are the R2 objects `sims/<sim>/<run>/<file>`, or
`sims/<sim>/<run>/shard-<i>-of-<n>/<file>` for a run cut into n shards. A rerun on the same day gets a new address, so an object, once
stored, is never replaced: the Worker caches every `/r2/` address for a year as immutable, and new bytes under an old address would
reach some readers and not others. The repository keeps only `public/data/sims/<sim>/<run>/index-<sim>.json` (every file with its
size, SHA-256 and shard, the notebook versions, card, libraries, the model's `checks_passed`) and the small files the entry names in
`"repo_files"`. The entry in `generations.json` carries `run`, `store: "r2"`, `versions`, `shards`, `format` and every file's size and
SHA-256; a rerun adds an entry and never replaces one.

**Storing with proof** ([tools/sims/r2.py](../tools/sims/r2.py)). Before an upload the key is asked for (HEAD). If R2 already holds the
same size and SHA-256 there (kept as the object's metadata `sha256`), nothing is sent ("already stored"; collecting twice is harmless).
If it holds anything else, the run stops: a key is never overwritten. After the upload the whole object is downloaded again as a stream
and its size and SHA-256 compared with the index; a difference deletes the bad object and stops the run. Each network call is tried
up to four times, after 2, 8 and 30 s, on a network error or a 5xx answer; a 4xx answer is not tried again. A run whose model reports
`checks_passed: false` is refused before anything is uploaded.

**Shards.** A large model can say `"shards": n`; its run function is then called as `run(out_dir, shard=i, shards=n)` and computes its
own part of the parameter grid. Each shard is one Kaggle notebook version, so each version's output stays below Kaggle's working
folder (about 20 GB). The engine takes the shards one after another: push, wait, download that version, check, upload to R2, file into
the Kaggle dataset, delete the local copy, next. The runner (about 30 GB free) never holds more than one shard. A failed shard stops
the run; the shards already stored stay, and collect mode finishes the run.

**Waiting.** An error answer from `kaggle kernels status`, or one that cannot be read, is tried again with growing waits for up to
10 minutes; only a real "error" or "cancel" state stops the run. The time limit `timeout_s` counts from the first poll that reports the
run as running: time spent in Kaggle's queue is not the model's fault (`"queue_s"`, default 5 hours, bounds the queue).

**Collect mode.** Run workflow with mode = collect, sim = the simulation, version = the notebook version (for a sharded run the versions
of the missing shards, comma-separated, in shard order) and shard = the shard of the first. It downloads those versions' stored output
(`kaggle kernels output <notebook>/<version>`) and carries it through the same checks, upload, index, generation and dataset filing,
without computing again.

**The status file** `public/data/sims/status/<sim>.json` says where the newest run stands: `queued` (pushed), `running`, `saved`
(landed on main, with the data commit), `live_ok` (the live check passed) or `failed` (with one sentence why), with the notebook
version(s), shard, card, times in UTC (queued, started, ended; queue and run seconds), bytes stored and the log address on Kaggle.
Kaggle does not report progress during a run, so the file says so. The expected duration comes only from a measured benchmark,
`public/data/sims/bench/<sim>.json`; without one the file says that there is none. It is pushed to main at every change of state by
the workflow's identity (commit message "Simulation status: <sim> <state>"); each push is a small commit that Cloudflare publishes.

**Landing without disturbing the run** ([tools/sims/land.py](../tools/sims/land.py)). Every push to main (the data and every status
change) is built in a separate git worktree of the newest main, made once per runner and reset for each push, never in the run's own
checkout; `docs/files.md` is generated again there; if main moved meanwhile, it starts again on the newest main (five tries).

**The live check** ([tools/sims/verify_live.py](../tools/sims/verify_live.py)) for an r2 run: it waits until the live
`generations.json` lists the run, downloads and hashes every file through `/r2/` while the total stays at most 100 MB, and asks every
other file for its first 1 MiB with a Range header, requiring 206 and a Content-Range total equal to its size. The result goes into
the status file. `--site` points it at another origin (the local test).

**The test model** `sims_smoke` ([tools/sims/sims_smoke.py](../tools/sims/sims_smoke.py), registry `"manual": true`: computed only by
Run workflow, never by a merge) writes two small files whose bytes depend only on the shard, and returns `checks_passed: false` when
the environment variable `SIMS_SMOKE_FAIL` is 1. Its data goes to the private dataset `numakoudsie/phyein-usul-sims-smoke`.

**The local test** `python3 tools/sims/test_engine_r2.py` ([tools/sims/test_engine_r2.py](../tools/sims/test_engine_r2.py)) runs the
whole line on one machine with nothing real touched: a bare git repository as origin (holding the parts of this repository the engine
reads and writes), a local S3 server (moto) as R2, a stand-in for the Kaggle tool that runs the pushed notebook text locally, and a
local web server for the live check. Its 12 cases: one-shard run; three shards; same-day rerun; a file altered after the index
(refused, nothing uploaded, status failed); a different object at the key (refused, unchanged) and the same object (skipped);
`checks_passed` false (refused); collect mode; two status errors; a long queue; another commit pushed to main during the run (kept);
a repo-store entry (barton, as before); the live check (passes, then fails on a replaced object). Result on 25 November 2026:
12 passed, 0 failed, 67.9 s wall time on the cloud session's machine.

**Disk.** The step that frees about 30 GB on the runner runs only for entries with `"free_disk": true` (the two release entries of
the double pendulum have it).
