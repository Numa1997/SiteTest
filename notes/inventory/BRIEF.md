# Inventory and clean-up of Phyein Usul's computations: brief

Written 14 November 2026 by the coordinating chat (session_01DGmqintkoYzahfGQQzdXYL) for the session the owner deploys.
Never write the owner's name.

## 0. Why this exists

The owner can no longer see where anything is. One figure (Fig. 15) alone has 14 Kaggle notebooks over two generations, and the
account holds 35 notebooks in all. Data sits in four places:
- Kaggle notebook outputs;
- the Cloudflare R2 bucket `phyein-usul-runs`;
- the repository;
- temporary session scratchpads.

Scripts exist in several versions side by side. Your job:
1. **Phase 1:** make one complete, exact inventory.
2. **Phase 2:** with the owner's yes, delete or merge everything redundant, and set one clean layout rule for the future.

## 1. Phase 1: the inventory (read-only; change nothing anywhere)

### 1.1 What to list: every artefact, with no exception

- **Kaggle** (account `numakoudsie`; Kaggle connector: `search_notebooks` with group Profile, `get_notebook_info`,
  `list_notebook_session_output`, `search_datasets` with group My, `get_accelerator_quota`):
  - every notebook: slug, title, figure, purpose, every version, its run date, the commit of the code it fetched, and whether it
    succeeded;
  - its output files and their size;
  - every dataset, and every model if any.
- **R2** (bucket `phyein-usul-runs`, read-only listing through api.cloudflare.com; the token is already on this environment, so
  never print it): every key prefix, the object count and the size per prefix.
- **The repository** (`Numa1997/SiteTest`, `main` plus every live branch): every data folder under `public/data/`, with its size,
  generation and whether the live site reads it. Follow each page's script to the files it loads; don't guess.
- **Scripts:** every file under `tools/`, the Python and JS files under `notes/`, and the notebooks `*.ipynb`. For each:
  - what it does;
  - which figure and which generation it belongs to;
  - whether anything live imports, calls or documents it (grep across the repository and the docs);
  - whether a newer file replaces it.
- **Generations and provenance:** every `generations.json` and every `index.json` that names a notebook slug, version or commit.
  These are the proof of where each stored run was computed. A Kaggle notebook named there is NOT deletable until that record
  points to a preserved copy.
- **Scheduled tasks and Workers, read-only:** `list_triggers`, and the Cloudflare Workers (`phyein-usul`, `kaggle-bridge`,
  `stellenrecherche`), name and purpose only. Touch none.

### 1.2 How to classify

Give each artefact exactly one status:

| Status | Meaning |
|---|---|
| **live** | the live site plays it or a live page needs it |
| **provenance** | not played, but a live record names it as the source of live data |
| **superseded** | replaced by a newer generation or file, with that file named |
| **test** | a smoke test, an experiment or a one-off |
| **orphan** | nothing refers to it and nothing replaces it |

For each, state what depends on it, and what would break if it were deleted.

### 1.3 Deliverables (commit and push on your branch `claude/inventory`)

- **`notes/inventory/INVENTORY.md`**, written for the owner: one section per figure (Figs. 1–15, then Fig. 16 in progress), plus
  "Shared" and "Tests".
  - Each section has a table: artefact, where, size, status, depends-on, proposed action.
  - At the top: the totals per place (Kaggle notebooks, R2 GB, repository MB) and one paragraph per figure in plain words.
- **`notes/inventory/inventory.json`**: the same data, machine-readable.
- **`notes/inventory/ACTIONS.md`**: the proposed actions, grouped. For each action give:
  - the exact artefacts;
  - the reason;
  - what it frees;
  - what it breaks, and how that is prevented;
  - whether it can be undone.

  The groups:
  - delete (Kaggle notebooks, repository files, R2 prefixes);
  - merge (scripts into one maintained version);
  - archive (move data the site doesn't play, keeping its record);
  - keep.

**STOP after Phase 1.** Report to the owner in your chat and to the coordinator (send_message, at most 12 lines): the totals and the
action groups with their sizes.

## 2. Phase 2: only on the owner's explicit yes, group by group

### 2.1 Order of work

1. **Preserve before deleting.** Any data whose only copy is a Kaggle output must first be copied to its permanent home (R2 or the
   repository, by the house pipeline in `docs/kaggle-pipeline.md`), and its SHA-256 checked.
2. **Rewrite the provenance records** that name a notebook you will delete. Point them to the preserved copy and keep the original
   slug, version and commit as history. Nothing may lose its record of origin.
3. **Delete.**
   - If the Kaggle connector has no delete operation, give the owner an exact list of notebook URLs to delete by hand on
     kaggle.com, in a safe order.
   - Never delete an R2 object the live index refers to.
   - Never delete anything on the branches of running sessions: `claude/fig15-correction` (the Fig. 15 correction) and
     `claude/fig16-cart` (Fig. 16).
   - Do not touch Fig. 15's R2 prefix until the correction session has filed its new generation.
4. **Merge the scripts.**
   - One maintained solver, runner and filer per figure. Superseded versions are removed from `tools/`, and the git history keeps
     them.
   - Every doc that names a removed file is updated in the same commit. `tools/inventory.py`, `docs/files.md` and the docs pages
     must say what the code now does.

### 2.2 The layout rule for the future (propose it in Phase 1; apply it in Phase 2)

- **Per figure:** one Kaggle notebook per figure and generation, or the fewest the work needs. Kaggle runs at most two GPU sessions
  at once, so two shard notebooks may be the honest minimum. Use notebook versions instead of new slugs for reruns and fixes.
- **Naming:** `fig<N>-<gen date>[-shard-k]`.
- **Write it** into `docs/kaggle-pipeline.md`.

### 2.3 Checks after every change to the repository

- `npm run build`;
- `python3 tools/inventory.py --check`;
- the address check `tools/perf/addresses.cjs`;
- every affected page in headless Chromium at 390 and 1440 px, with no errors.

Merge to `main` as CLAUDE.md says, then verify the live site.

## 3. How you work

- **Read first:** `CLAUDE.md`, `AGENTS.md`, `docs/kaggle-pipeline.md`, `docs/usul.md` and `docs/files.md`.
- **First:** write `notes/inventory/STATE.md` (aim, phase, files, commits, these rules), commit and push it. Keep it current.
- **The owner:** BSc in physics (computational and theoretical).
  - Plain words and metric units.
  - Mark Fact (with a handle), Inference and Opinion.
  - One decision at a time, with options, your pick and the case against it.
- **Forbidden:**
  - no GPU, no new Kaggle run, no R2 write;
  - no deletion of any kind before the owner's yes on that group;
  - nothing that costs money.
- **Measure, don't estimate:** every size and every dependency is checked, not assumed.
