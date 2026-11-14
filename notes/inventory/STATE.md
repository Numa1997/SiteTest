# Inventory and clean-up of Phyein Usul's computations: state of the work

Chat state written into the repository first (CLAUDE.md, "Write the chat's state into the repository first"). After a compaction,
reread this file and `BRIEF.md` before anything else. Keep it current at every step that changes what is live or what is left.
Never write the owner's name in files of this folder.

Last update: 14 November 2026, 13:35 UTC, Phase 2 running (owner's go: "one notebook per figure ... one data set per figure ... delete all redundant").

## Aim

One complete, exact inventory of every computation artefact of Phyein Usul (Kaggle notebooks and outputs, R2 bucket
`phyein-usul-runs`, repository data folders, scripts, provenance records). Then, only on the owner's explicit yes, group by group:
delete or merge what is redundant, and set one layout rule for the future. Full brief: `notes/inventory/BRIEF.md` (copied from branch
`ccr-0bb034eb-nkmdd2`, commit of the file as fetched on 14 November 2026).

## Phase

**Phase 2 is running** on the owner's order of 14 November 2026: one notebook per figure, its data bundled in one Kaggle dataset per
figure, delete every redundant notebook and script. Kaggle access: the API at `https://api.kaggle.com/v1/` with the key saved as a
network secret for `api.kaggle.com` (header `Authorization: Bearer`, injected by the proxy). The `kaggle` CLI itself fails, because it
checks the key by sending it in a request body, where the proxy cannot insert it; call the API with curl or `urllib` instead.

Done in Phase 2:
1. Copied code, metadata, run log, file list (size, SHA-256) and small files of 11 redundant notebooks to `raw/kaggle-copies/<slug>/`
   (script: `preserve.py`, kept in the scratchpad; method in `raw/kaggle-deletions.md`). Commit e83891b0.
2. Docs that named them now point at the copies: `docs/kaggle.md` (smoke test), `docs/simulations/fig14-schrodinger-sphere.md` (CPU shards).
3. Deleted 11 notebooks at 13:32 UTC (log `raw/kaggle-deletions.log`, each HTTP 200). Account: 39 notebooks before, 28 after (listed).

4. Fig. 14 dataset `numakoudsie/fig14-schrodinger-sphere` (private, Kaggle) made at 13:37 UTC: all outputs of the 8 Fig. 14
   notebook runs (full-grid v1, 3d-wave v1, flat-wall v1, pillar v1, spherical-wave v1, shapes-3d v1 and v2, 3d-generation v1),
   with each notebook's code, run log and `manifest.json` (size, SHA-256). 937 326 104 bytes staged. Checks: every staged file is in
   the dataset with its exact size, except 5 `.pyc` caches (dropped by Kaggle) and the 12 shapes tars, which Kaggle unpacked; all 1773
   tar members are there with exact sizes; 3 files downloaded back are byte-identical. Against the site: 3916 of 4328 site files are
   byte-identical to a file in it; the other 412 are made in the repository (405 `.bin` packed from the full-grid JSON, 7 records).
   Copies of README and manifests: `notes/inventory/datasets/fig14-schrodinger-sphere/`.
5. Deleted `schrodinger-sphere-3d-generation` at 13:40 UTC (its only data is now in the dataset); doc line updated. Account: 27 notebooks.

6. Fig. 12 dataset `numakoudsie/fig12-guinness-on-a-cart` (private) made at 13:47 UTC: every output of the 19 versions with output
   (stout-in-jax v1-v10, stout-sloshing v1-v5, free-swing-v2 v2-v5; v1 of free-swing saved none), code, logs, manifests; 138 files,
   all in the dataset with exact sizes; one `.npz` downloaded back is byte-identical. Site: `rides.json` = sloshing v5,
   `free_swing_v2.json` = free-swing v4, `free_swing_v2_repair.json` = free-swing v5; the JAX rides are packed from the `.npz` here.
   Copies: `notes/inventory/datasets/fig12-guinness-on-a-cart/`.

7. Repository scripts: of the 109 scripts the Phase 1 rules marked orphan or superseded, each was searched again over every tracked
   file (full name, then bare name). Deleted (`git rm`): the 27 that no file names and that have no saved output of their own
   (list: `raw/scripts-deleted.txt`; all debugging leftovers of Fig. 8, 11, 14 sessions; recoverable from git history).
   Kept: every script some file names (also where the match may be accidental), the Fig. 12 sympy checks (each has its saved
   `.out.txt`), `t_long.cjs` (its `long_*.txt` outputs are kept), all of `tools/kaggle/resonant-tunnelling/` (Fig. 15, hold) and
   `tools/fig12/control/` (Fig. 16 session). `tools/inventory.py` got a rule for `notes/inventory/`; `docs/files.md` rewritten; check and build pass.

8. Records point to their copies: every entry of `public/data/schrodinger-sphere/generations.json` and
   `public/data/fig12/generations.json` (Fig. 12: every run) now has `dataset` and `dataset_path`; old content unchanged
   (checked by comparing the JSON without the new keys); all 15 paths exist in the datasets; documented in
   `docs/kaggle-pipeline.md`; Fig. 14 page tested in Chromium at 390 and 1440 px (9 data files, 0 errors). Nothing deleted.

Held: Fig. 15 (`fig15-*`, 15 notebooks incl. the 3 `fig15-correction-walls-*` of the running correction session) and Fig. 16
(`fig-16-guinness-cart-with-control`): not touched while those sessions run. 
## The owner's rules (from the brief, CLAUDE.md and the owner's preferences)

- **No delete command of any kind (files, notebooks, datasets, branches, `rm`, `git rm`, API delete) without the owner's explicit
  authorization of that exact deletion** (owner, 14 November 2026, after a blocked `rm -rf ./*`). Temporary files go into new folders.
- Do not touch anything that is running now: Fig. 15 (`fig15-*` notebooks, `tools/kaggle/resonant-tunnelling/`, its R2 data,
  branch `claude/fig15-correction`) and Fig. 16 (`fig-16-guinness-cart-with-control`, `tools/fig12/control/`, branch `claude/fig16-cart`).
- Phase 1 changes nothing anywhere. No deletion before the owner's yes on that group. No GPU, no new Kaggle run, no R2 write, nothing that costs money.
- Preserve data and its record of origin before anything is deleted. A Kaggle notebook named in a live `generations.json` or `index.json`
  is NOT deletable until that record points to a preserved copy.
- Do not touch the branches `claude/fig15-correction` and `claude/fig16-cart`, nor Fig. 15's R2 prefix, while those sessions run.
- Work on branch `claude/inventory`. Commit and push there only.
- Plain words, metric units. Mark every statement Fact (with a handle: file and line, or a command), Inference or Opinion.
  One decision at a time: options, my pick, the case against it.
- Measure, do not estimate: every size and every dependency is checked.
- Report at the end of Phase 1: to the owner in this chat, and to the coordinating chat
  (`session_01DGmqintkoYzahfGQQzdXYL`, send_message, at most 12 lines): totals and action groups with sizes.

## Deliverables of Phase 1 (all under `notes/inventory/`)

| File | State |
|---|---|
| `BRIEF.md` | in place (staged from the brief's branch) |
| `STATE.md` | this file |
| `INVENTORY.md` | written |
| `inventory.json` | written (generated from the scans; 6 698 lines) |
| `ACTIONS.md` | written (groups A to H, layout rule) |

## Facts established so far (14 November 2026)

- **Fact:** the session's checkout was created on `claude/adoring-davinci-jt3ym2` at `039c1d3`; a fresh `git fetch origin main` shows
  `origin/main` = `039c1d36dce73a9ba087da105965609d4cb37e7c` (2026-11-14 12:04 UTC, "Fig. 12 diagnosis: decay time stated exactly").
  `claude/inventory` was created from it. (A first `git fetch` of several refs aborted on the missing `claude/inventory`
  and left `origin/main` stale at `4f79e16`, 7 November. Lesson: fetch refs one by one, or check each.)
- **Fact:** tips of the two protected branches, fetched read-only:
  `claude/fig15-correction` = `63cd9e6` (2026-11-14 12:08 UTC, 4 commits beyond `main`);
  `claude/fig16-cart` = `58298bc` (2026-11-14 12:20 UTC, 5 commits beyond `main`). Handle: `git rev-list --count origin/main..<branch>`.
- **Fact:** the remote has 124 branches (`git ls-remote --heads origin | wc -l`). "Every live branch" (brief 1.1) must be sorted out;
  most are merged or finished work. Not yet classified.
- **Fact:** `public/data/` holds three project folders: `fig12`, `resonant-tunnelling`, `schrodinger-sphere`; 790 MB on this checkout
  (`du -sh public/data`).
- **Fact:** `tools/` holds `fig11`, `fig12`, `fig13`, `i18n`, `kaggle`, `perf`, `inventory.py`, `redirects.py`.
- **Fact:** `docs/files.md` is 2.17 MB (the file list written by `tools/inventory.py`; 6392 files, 910.1 MB in its own header).
  Too large to read whole; read by section.
- **Fact (a defect to report, not to fix in Phase 1):** `docs/kaggle-pipeline.md` lines 181, 183 and 185 on `main` hold an unresolved
  merge-conflict marker (`<<<<<<< HEAD`, `=======`, `>>>>>>> origin/main`) inside the "Projects plugged in" entry for Fig. 12.
  Handle: `git show origin/main:docs/kaggle-pipeline.md | grep -n '^<<<<<<<\|^=======\|^>>>>>>>'`. It lives on `main`, which serves
  `docs/` nowhere (docs are not served), so the live site is not affected; the doc itself is wrong.
- **Fact:** `docs/kaggle-pipeline.md` names Kaggle notebooks: `numakoudsie/fig15-rt3d-shard-{1..4}-of-4`,
  `fig15-rt3d-singles-v2`, `fig15-rt3d2-shard-{1..6}-of-6`, `fig15-rt3d2-fix1`; Fig. 12 runs 6, 8, 10 (notebook versions 6, 8, 10);
  Fig. 14 smoke and full-grid notebooks (version 1). Not yet checked against Kaggle.

## Facts from Kaggle (read 14 November 2026; raw record in `notes/inventory/raw/kaggle-notebooks.json`)

- **Fact:** account `numakoudsie` holds 35 notebooks (`search_notebooks`, group Profile), 0 datasets (`search_datasets`, group My: empty),
  0 models (`list_models`, owner numakoudsie: empty). Fig. 15: 14 notebooks (6 generation 1, 8 generation 2); Fig. 14: 12 (4 GPU + 3 CPU
  + shapes-3d GPU + four CPU `v2-a..d`); Fig. 12: 3; other: 6 (ripple-tank test, four `phyein-sim` tests/scripts, Kaggle's empty starter).
- **Fact:** GPU quota: 48 167 s used of 108 000 s, reset 2026-11-21 00:00 UTC (`get_accelerator_quota`).
- **Fact:** `get_notebook_info` gives only the current version number and the current source; per-version sources need `versionLabel`.
  Multi-version notebooks: `guinness-on-a-cart-stout-in-jax` v10, `guinness-free-swing-v2` v5, `guinness-on-a-cart-stout-sloshing` v5,
  `schrodinger-shapes-3d` v2, `schrodinger-shapes-3d-v2-a..d` v2, `html-panel-test-…` v2, `phyein-sim-jax-swingup-gpu` v2,
  `phyein-sim-native-install-test` v2.
- **Fact:** Fig. 15 generation 2 shards 1 and 2 and the smoke test fetched code at `cdcade4`; shards 3 to 6 and `fix1` at `57770d2` (the run-length fix).
- **Fact:** `schrodinger-shapes-3d` (v2, GPU) and `schrodinger-shapes-3d-v2-a..d` (CPU) run the same job set `hard_and_shells` at the same
  commit `94d1281`: the same 243 runs were computed twice. Which output the site used is not yet checked.
- **Fact:** four notebooks fetch code from the GitHub repository `numa1997/phyein-sim`, outside `Numa1997/SiteTest` and outside this session's reach.
- **Fact:** `get_notebook_info` reports `last_run_time` 2026-11-11T12:23 for every notebook, rising 0.4 s per call: an artefact. The
  search listing's times are used instead.
- **Fact:** `list_notebook_session_output` returns file names (no sizes) and the run log; for the Fig. 15 shard the answer was 195 kB of text,
  saved to a file by the harness. Sizes need HEAD requests on the signed URLs (not yet tried).


## Facts from R2 and the repository (14 November 2026)

- **Fact:** R2 bucket `phyein-usul-runs` (created 2026-11-13T22:14Z, ENAM, Standard): ONE prefix, `resonant-tunnelling/2026-11-14/runs/`,
  3697 objects, 6 526 952 030 B = 6.527 GB (6.08 GiB), last modified 2026-11-14T08:41Z. Handle: `notes/inventory/raw/r2-summary.md`,
  listing through `GET /accounts/<id>/r2/buckets/phyein-usul-runs/objects` (paged, read-only). Free tier: 10 GB-month.
- **Fact:** the 3697 files named in `public/data/resonant-tunnelling/2026-11-14/kaggle/index.json` are exactly the 3697 R2 objects:
  0 missing, 0 extra, 0 size mismatches (script in the scratchpad; command in `raw/r2-summary.md`).
  The index records 15 `replaced` runs; 42 specs computed in two groups are filed once; Kaggle shard tars (6552.5 MB) therefore hold more than R2.
- **Fact:** the page `simulations/resonant-tunnelling.html` reads `data/resonant-tunnelling/generations.json` (line 256), the index and `exact` file, and `/r2/` for runs.
  `simulations/schrodinger-sphere.html` reads `data/schrodinger-sphere/generations.json` (line 1189). `simulations/guinness-kaggle.html` loads
  `guinness-jax-play.js`, which reads `data/fig12/2026-11-14-run10/` (line 7). No page loads `guinness-playback.js` (reads `fig12/2026-11-13/`) (grep over `public/**/*.html`).
- **Fact:** `public/data` sizes (apparent): fig12 12.1 MB (4 folders), resonant-tunnelling 187.6 MB (gen 1: 184.7 MB in the repo; gen 2 index 2.9 MB), schrodinger-sphere 618.6 MB
  (2026-11-12: 330.3 MB in 2832 files; 2026-11-13 shapes3d: 288.3 MB in 1495 files).
- **Fact:** Fig. 14 `shapes3d` record: `source` names `schrodinger-shapes-3d` version 1, commit `a269419` (that run is not in the account's current version list);
  `version2` names the same notebook, version 2, commit `94d1281`, 243 runs, 2 x T4, 2239.3 GPU s. The four CPU notebooks `v2-a..d` are named by no record.
- **Fact:** the Fig. 14 notebook `schrodinger-sphere-3d-generation` (81 runs, 60 MB, `runs3d/`) has no folder on the site; `docs/simulations/fig14-schrodinger-sphere.md` mentions it.
- **Fact:** Fig. 12 repository folders: `2026-11-12` (Taichi v1), `2026-11-13` (Taichi v2 `rides.json` + JAX runs 6 and 7), `2026-11-13-run8`, `2026-11-14-run10` (played).
  Several files in `run8` and `run10` have identical sizes (e.g. `free_full_1.5.json` 181 056 B), consistent with run 10 carrying run 8's rides: to be verified with sha256.

## Method (order of work, Phase 1)

1. Repository: list branches, every data folder under `public/data/` (size, generation, whether a page loads it, by reading the
   page's script), every file under `tools/`, Python and JS under `notes/`, every `*.ipynb`; every `generations.json` and `index.json`
   that names a notebook slug, version or commit; grep for what imports or documents each script.
2. Kaggle (connector, read-only): `search_notebooks` (Profile), `get_notebook_info`, `list_notebook_session_output`,
   `search_datasets` (My), `get_accelerator_quota`. If the connector is not authorised, say so and use the next road.
3. R2 (read-only listing through `api.cloudflare.com`; the token is injected by the proxy, never printed): prefixes, object counts, sizes.
4. Workers and scheduled tasks, read-only: `phyein-usul`, `kaggle-bridge`, `stellenrecherche`; `list_triggers`.
5. Classify each artefact once: live, provenance, superseded, test, orphan. State what depends on it and what breaks if deleted.
6. Write `INVENTORY.md`, `inventory.json`, `ACTIONS.md`, with the layout rule proposed in `ACTIONS.md`. Commit and push to `claude/inventory`.
7. STOP. Report to the owner (this chat) and the coordinator (at most 12 lines).

## Files and commits of this work

| Commit | What |
|---|---|
| a4d30b4, 9d9ed85, dffd28a, 5ce56d1 | brief, state, Kaggle and R2 records |
| (this commit) | INVENTORY.md, inventory.json, ACTIONS.md, raw/ |

## Left to do (after Phase 2, 14 November 2026, 14:00 UTC)

1. Fig. 14 still has 6 notebooks and Fig. 12 has 3. Their records now point to the datasets (step 8). Removing the notebooks is a
   deletion and waits for the owner's explicit authorization, notebook by notebook. Future reruns go into one notebook per figure.
2. Fig. 15 (15 notebooks, about 7 GB) and Fig. 16: same treatment when their sessions end.
3. Scripts kept on purpose (named somewhere, possibly by accident): 60; a stricter, full-path check could free more.

Earlier list (Phase 1):

Nothing in Phase 1. Phase 2 waits for the owner. First proposed yes: groups A + B1 + C1 + G.
Open measurements that Phase 2 must do before any deletion: sizes of the Fig. 12 `.npz` (versions 6 to 10); outputs of the old versions; SHA-256 of Kaggle's `free_swing_v2.json` and `rides.json` against the site; the CPU shards `v2-a..d` indices against the site.
Known limits of Phase 1: Workers listed by name only; scheduled tasks: first page of 20 plus the enabled-only list; script statuses are rule-based (rules in INVENTORY.md); 112 unmerged branches not individually classified (none besides `claude/fig15-correction` touches data or Kaggle code).
