# The scenes pipeline: Kaggle computes, GitHub stores, Cloudflare serves

Built 20 November 2026. The living scenes on the site's pages (`public/scripts/bg-scenes.js`, [scripts/bg-scenes.md](scripts/bg-scenes.md))
are to play data computed by a reference model on Kaggle, not physics computed in the visitor's browser. This page explains, in
plain words, every piece that moves that data, where it lives, and why it is needed. The plan for the scenes themselves:
[notes/scenes/PLAN.md](../notes/scenes/PLAN.md).

## The chain in one picture

A kitchen that cooks each dish once. The recipe is written in the repository (GitHub). Pressing one button sends the order to
the oven (Kaggle); the dish comes back, a checker compares it with the label the oven printed on it (SHA-256), and only a dish
that matches is put on the shelf (the repository's `public/data/scenes/`). The shop window (Cloudflare) refreshes itself whenever
the shelf changes. Nothing is cooked again unless someone presses the button again.

**Data is generated once per scene** (owner, 20 November 2026). A scene that should look different on every visit gets its variety
from that one generation: the model computes a set of runs from different random starts (each start recorded by its seed), all in
the same Kaggle run, and the page picks one of the stored runs, and a random point in it, each time it is opened. The browser picks;
it computes no physics.

| Step | What happens | Where | Who does it |
|---|---|---|---|
| 1 | The scene's model `tools/scenes/<scene>.py` is on `main` | GitHub | a person or a session |
| 2 | The workflow **Scenes on Kaggle** is started by hand with the scene's name | GitHub Actions, [.github/workflows/scenes-kaggle.yml](../.github/workflows/scenes-kaggle.yml) | the owner or a session, once per scene |
| 3 | It pushes a new version of the private CPU notebook `numakoudsie/scenes-living-backgrounds`; the notebook downloads the model from GitHub at exactly that commit and runs it | Kaggle | [tools/scenes/pipeline.py](../tools/scenes/pipeline.py) step 1-2, [tools/scenes/kaggle_scenes.py](../tools/scenes/kaggle_scenes.py) |
| 4 | It waits for the run (asking Kaggle every 20 s, at most 30 min) | GitHub Actions | `pipeline.py` step 3 |
| 5 | It downloads the run's output and checks every file's size and SHA-256 against `index-<scene>.json`, which the notebook wrote on Kaggle; any difference stops everything | GitHub Actions | `pipeline.py` step 4 |
| 6 | It copies the files to `public/data/scenes/<date of generation>/` and adds the run to `public/data/scenes/generations.json` (scene, date, notebook, version, commit, files with SHA-256, run time) | the repository | `pipeline.py` step 5 |
| 7 | It commits as `github-actions[bot]` and pushes to `main` | GitHub | the workflow's last step |
| 8 | Cloudflare Workers Builds sees the push, builds and publishes the site; the files appear at `https://phyeinusul.com/data/scenes/<date>/…` | Cloudflare | Cloudflare, by itself (since 21 October 2026) |
| 9 | The scene reads `generations.json`, downloads its newest file, checks its SHA-256 in the browser and plays it | the visitor's browser | `bg-scenes.js` |

The output also stays on Kaggle with the notebook version that made it (the notebook page, tab Output).

## How to start it

One way only, by hand: GitHub, tab Actions, "Scenes on Kaggle", button "Run workflow", type the scene's name (for example
`barton`). There is no timer and no automatic rerun. Two starts never overlap (`concurrency: scenes-kaggle`): each is a new
version of the same notebook, so a second one waits for the first.

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

With a stand-in for the Kaggle tool that runs the notebook here: a good run stores 3 files and a generation; a run whose
`barton.bin` has one flipped bit stops with "barton.bin: size or SHA-256 differs from the index" and stores nothing; a refused
push stops with "Kaggle did not accept the push". The first real run follows once the secret is in place.
