# Inventory and clean-up of Phyein Usul's computations: state of the work

Chat state written into the repository first (CLAUDE.md, "Write the chat's state into the repository first"). After a compaction,
reread this file and `BRIEF.md` before anything else. Keep it current at every step that changes what is live or what is left.
Never write the owner's name in files of this folder.

Last update: 14 November 2026, start of Phase 1.

## Aim

One complete, exact inventory of every computation artefact of Phyein Usul (Kaggle notebooks and outputs, R2 bucket
`phyein-usul-runs`, repository data folders, scripts, provenance records). Then, only on the owner's explicit yes, group by group:
delete or merge what is redundant, and set one layout rule for the future. Full brief: `notes/inventory/BRIEF.md` (copied from branch
`ccr-0bb034eb-nkmdd2`, commit of the file as fetched on 14 November 2026).

## Phase

**Phase 1 (read-only), in progress.** Nothing is deleted or changed anywhere outside this folder. Phase 2 starts only on the
owner's yes to a named group of actions.

## The owner's rules (from the brief, CLAUDE.md and the owner's preferences)

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
| `INVENTORY.md` | not started |
| `inventory.json` | not started |
| `ACTIONS.md` | not started |

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
| (none yet) | `BRIEF.md` staged, `STATE.md` written; first commit pending |

## Left to do

Everything in the Method list above. Nothing has been inventoried yet.
