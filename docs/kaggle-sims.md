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
| Fig. 1, Wave interference (`wave_interference`) | [tools/sims/wave_interference.py](../tools/sims/wave_interference.py) | 64 files, 16.2 MB: the distance table of a fixed 250 × 250 grid, a ring's angle for each λ = 16 … 64 px and height for each γ = 0 … 0.60, a cosine table; the page adds the rings of the reader's sources ([fig01-wave-sources.md](simulations/fig01-wave-sources.md)) | `simulations/Circular Wave Interference Visualization.html`, its own loader (`stored()`), not `bg-scenes.js` |

## Pipeline B in the page

`sceneData(name, file)` in `bg-scenes.js` reads `data/sims/generations.json`, takes the newest entry of that simulation, downloads
`data/sims/<name>/<date>/<file>`, computes its SHA-256 in the browser (`crypto.subtle`) and compares it with the entry; only a matching file is handed to
the scene. A file is 4 bytes of label, a uint32 header length, a JSON header (parameters, checks, column names and units), then
int16 frames. Until the data has arrived, or if the check fails, the scene draws nothing in that place.

Barton's pendulums (`barton.bin`, columns θ_d, L_d, x_bar, θ_0…θ_7 at 30 frames a second, one exact loop of 64.98 s): every bar
on the page starts at its own random moment of the loop and hangs a random choice of the eight stored pendulums in random order;
each frame the page draws the stored frame nearest in time. It integrates nothing.

## Keys

- **`KAGGLE_API_TOKEN`**, a repository secret (GitHub → repository Settings → Secrets and variables → Actions). The official Kaggle
  tool (`pip install kaggle==2.2.5 six`; that version imports `six` without installing it, seen on the first real run, 21 November 2026) reads it from the environment. GitHub never shows a secret again, never prints it in logs, and
  does not give it to copies (forks) of the repository.
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
