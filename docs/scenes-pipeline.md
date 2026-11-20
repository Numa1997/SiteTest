# The scenes pipeline: Kaggle computes, GitHub stores, Cloudflare serves

Built 20 November 2026. The living scenes on the site's pages (`public/scripts/bg-scenes.js`, [scripts/bg-scenes.md](scripts/bg-scenes.md))
are to play data computed by a reference model on Kaggle, not physics computed in the visitor's browser. This page explains, in
plain words, every piece that moves that data, where it lives, and why it is needed. The plan for the scenes themselves:
[notes/scenes/PLAN.md](../notes/scenes/PLAN.md).

## Two pipelines

**Pipeline A makes a scene's data, once.** It runs when a scene's model is added or changed on `main`, and never otherwise (no
timer). The model is written in the repository; a GitHub Action sends it to Kaggle; Kaggle computes the scene's whole data in one
run (for a random scene: many runs from different random starts, each recorded by its seed); the Action checks the result against
the fingerprints Kaggle printed (SHA-256) and commits it to `public/data/scenes/`; Cloudflare publishes. Nobody carries anything.

**Pipeline B shows it, on every visit.** No Action, no Kaggle, no computing: the page downloads the stored file, checks its
SHA-256, picks a random start in it (for a random scene also one of the stored runs), and a drawing function in
`public/scripts/bg-scenes.js` animates it. So every visit looks different and nothing is computed again.

Kaggle cannot animate: it only produces files. The picture is always drawn by the page.

## Pipeline A, step by step

| Step | What happens | Where | Who does it |
|---|---|---|---|
| 1 | The scene's model `tools/scenes/<scene>.py` is added or changed on `main` | GitHub | a person or a session |
| 2 | The workflow **Scenes on Kaggle** starts | GitHub Actions, [.github/workflows/scenes-kaggle.yml](../.github/workflows/scenes-kaggle.yml) | GitHub, by itself |
| 3 | It pushes a new version of the private CPU notebook `numakoudsie/scenes-living-backgrounds`; the notebook downloads the model from GitHub at exactly that commit and runs it | Kaggle | [tools/scenes/pipeline.py](../tools/scenes/pipeline.py) step 1-2, [tools/scenes/kaggle_scenes.py](../tools/scenes/kaggle_scenes.py) |
| 4 | It waits for the run (asking Kaggle every 20 s, at most 30 min) | GitHub Actions | `pipeline.py` step 3 |
| 5 | It downloads the run's output and checks every file's size and SHA-256 against `index-<scene>.json`, which the notebook wrote on Kaggle; any difference stops everything | GitHub Actions | `pipeline.py` step 4 |
| 6 | It copies the files to `public/data/scenes/<date of generation>/` and adds the run to `public/data/scenes/generations.json` (scene, date, notebook, version, commit, files with SHA-256, run time) | the repository | `pipeline.py` step 5 |
| 7 | It commits as `github-actions[bot]` and pushes to `main` | GitHub | the workflow's last step |
| 8 | Cloudflare Workers Builds sees the push, builds and publishes the site; the files appear at `https://phyeinusul.com/data/scenes/<date>/…` | Cloudflare | Cloudflare, by itself (since 21 October 2026) |
| 9 | Pipeline B (below) plays it | the visitor's browser | `bg-scenes.js` |

The output also stays on Kaggle with the notebook version that made it (the notebook page, tab Output).

## How pipeline A starts

By itself, when a file `tools/scenes/<scene>.py` is added or changed on `main` (not `pipeline.py` or `kaggle_scenes.py`, which are
the machinery); only the changed scenes are computed. It can also be started by hand: GitHub, tab Actions, "Scenes on Kaggle",
"Run workflow", the scene's name. Two starts never overlap (`concurrency: scenes-kaggle`).

## Pipeline B in the page

`sceneData(name, file)` in `bg-scenes.js` reads `data/scenes/generations.json`, takes the newest entry of that scene, downloads
the file, computes its SHA-256 in the browser (`crypto.subtle`) and compares it with the entry; only a matching file is handed to
the scene. A file is 4 bytes of label, a uint32 header length, a JSON header (parameters, checks, column names and units), then
int16 frames. Until the data has arrived, or if the check fails, the scene draws nothing in that place.

Barton's pendulums (`barton.bin`, columns θ_d, L_d, x_bar, θ_0…θ_7 at 30 frames a second, one exact loop of 64.98 s): every bar
on the page starts at its own random moment of the loop and hangs a random choice of the eight stored pendulums in random order;
each frame the page draws the stored frame nearest in time. It integrates nothing.

## Keys

- **`KAGGLE_API_TOKEN`**, a repository secret (GitHub → repository Settings → Secrets and variables → Actions). The official Kaggle
  tool (`pip install kaggle==2.2.5`) reads it from the environment. GitHub never shows a secret again, never prints it in logs, and
  does not give it to copies (forks) of the repository.
- **No GitHub key is needed**: GitHub gives every workflow run its own short-lived token; `permissions: contents: write` lets it
  commit to this repository and nothing else.

## Costs

- GitHub Actions: free; standard runners are free in public repositories, and this repository is public (checked 20 November 2026).
- Kaggle: the scenes run on CPU, which does not use the 30 GPU hours a week.
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

A failed run leaves the site exactly as it was. GitHub e-mails the repository owner about failed workflow runs.

## Tested (20 November 2026)

Pipeline A, with a stand-in for the Kaggle tool that runs the notebook here: a good run stores 3 files and a generation; a run whose
`barton.bin` has one flipped bit stops with "barton.bin: size or SHA-256 differs from the index" and stores nothing; a refused
push stops with "Kaggle did not accept the push". Pipeline B, in headless Chromium with that data: both files load, the SHA-256
matches, the pendulums play at 30 frames a second (English and Arabic home page); with one bit flipped in `barton.bin` the scene
reports "SHA-256 differs from generations.json" and draws no pendulums. Not yet tested: a real Kaggle run, and whether a commit
made by the workflow sets off Cloudflare's build as a person's commit does. Both are tested by the first real run, which needs
the secret.
