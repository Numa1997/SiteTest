# Kaggle account `numakoudsie`: report for the session that organises it

Written 24 November 2026 by the session that read the account. Every statement is marked **Fact** (with its source),
**Inference** (reasoning from facts), **Opinion**, or **Unverified**. Nothing on Kaggle was changed by this session.
Companion files: `notes/inventory/KAGGLE.md` (the raw listing), `notes/skills/phyein-usul-kaggle-presentation/SKILL.md`
(the rules, committed on branch `branch/fervent-galileo-x0t3vu`).

## 1. The goal
Numa is applying for jobs. The Kaggle profile must be **presentable and organised**: consistent names, real descriptions,
nothing embarrassing, nothing leaking. Numa's words, repeatedly: simple requirement, do the right thing, no big production.

## 2. Rules from Numa (binding)
1. **Nothing goes public unless Numa names that exact item.** Numa said on 24 Nov: "the datasets are not ready to be made public".
2. **Fig. 12, Fig. 16 and anything Guinness never go public** until Numa says they are finished.
3. **No new runs.** No CPU or GPU runs "to see what happens". The data already exists (section 4).
4. **Find the data where it already is.** The website holds it (Cloudflare R2, served by the Worker at `/r2/`). Do not recompute or
   re-copy what is already stored. If it cannot be reached, say so, and name the other road.
5. **Nothing deleted unless Numa names the item.** (Constitution: every action needs an explicit yes for that action.)
6. One step per turn, then hand back. Each proposal: what, why, effect, cost, undoable or not.
7. Metric units. Plain words. Numa has a BSc in Physics; define terms.
8. Mark Fact, Inference, Opinion. Never state an unchecked thing as fact.
9. Read `CLAUDE.md`, `AGENTS.md`, `docs/kaggle-pipeline.md` (line 193) and the skills `kaggle-gpu-run`,
   `phyein-usul-kaggle-pregenerate` BEFORE the first Kaggle action.
10. The Kaggle key lives in the GitHub repository secret `KAGGLE_API_TOKEN`; the workflow "Simulations on Kaggle" uses it.
    `api.kaggle.com` is also listed in this environment as proxy-authenticated (no key needed). **Unverified** what that allows.

## 3. What is on Kaggle now (Fact: connector calls `search_datasets`, `search_notebooks`, `list_dataset_tree_files`, 24 Nov)

### Datasets: 8, all private
| Ref | Title | Subtitle | Size | Version |
|---|---|---|---|---|
| fig1-wave-interference | Fig. 1 Wave Interference: simulation data | set | 35 MB | 1 |
| fig2-double-pendulum | Fig. 2 Double Pendulum: simulation data | set | 6.8 GB | 2 |
| fig12-guinness-on-a-cart | Fig 12 Guinness on a cart data | EMPTY | 161 MB | 3 |
| fig14-schrodinger-sphere | Fig 14 Schrodinger sphere data | EMPTY | 872 MB | 2 |
| fig15-resonant-tunnelling | Fig. 15 Resonant Tunnelling: simulation data | set | 26.7 GB | 1 |
| fig16-guinness-cart-control | Fig 16 Guinness cart with control data | EMPTY | 103 MB | 1 |
| phyein-usul-barton | Barton's pendulums: simulation data | set | 43 kB | 2 |
| phyein-usul-coupled | Coupled pendulums: simulation data | set | 7 kB | 1 |
All 8 use licence CC BY 4.0 and Kaggle's default grey cover image. An earlier message said 9 datasets; that was wrong.

### Notebooks: 32 (privacy flag not returned by the call; an earlier read said all private, **Unverified** now)
- Tidy (4): `phyein-usul-simulations` ("Phyein Usul simulations"), `fig-12-guinness-on-a-cart`, `fig-14-schrodinger-sphere`,
  `fig-16-guinness-cart-with-control`.
- Fig. 15 working (20): `fig15-correction-walls-gpu`, `fig15-correction-2d-1..4-of-4`, `fig15-correction-2d-shells-1..2-of-2`,
  `fig15-rt3d-shard-1..4-of-4`, `fig15-rt3d-singles-v2`, `fig15-rt3d2-shard-1..6-of-6`, `fig15-rt3d2-fix1`,
  `fig15-filer-2026-11-18`.
- Guinness / Fig. 12 and 16 working (8): `guinness-on-a-cart-stout-in-jax`, `guinness-realism-fig12`, `-fig16`, `-panel16`,
  `-render`, `fig-16-cart-diagnostics-cpu`, `step4-energy-audit-cpu`, `step4-slosh-head-offline`.

## 4. Where the Fig. 15 data is
- **Fact:** website store, Cloudflare R2, keys `resonant-tunnelling/2026-11-18/runs/<file>`: 2,782 objects, 4,439,713,712 bytes
  (`notes/fig15/coordinator-2026-11-18/r2_upload.log`, 2,782 OK lines). Generation 2026-11-14 remains: 3,697 objects, 6.18 GB
  (`notes/fig15/COORDINATOR_STATE.md:17-20`). The live page animates these.
- **Fact:** Kaggle dataset `fig15-resonant-tunnelling` (26.7 GB, v1, created 24 Nov, one job copied outputs, no simulation ran, per the
  earlier session) has 20 folders, one per notebook output, named exactly like the notebooks, including `fig15-filer-2026-11-18`.
- **Inference:** the Kaggle dataset therefore already holds the raw archives and the filer's output. I did not open its files.
- **Fact:** it is organised by notebook name, not by generation or by what the figure shows.
- **Inference** (from `notes/fig15/STATE.md`, `COORDINATOR_LOG.md`): generation 1 = `rt3d-*` (13 Nov), generation 2 = `rt3d2-*`
  (14 Nov), correction 2026-11-18 = `correction-*` plus the filer.

## 5. The "weird links": exactly what they are
- **Fact** (`notes/fig15/COORDINATOR_LOG.md:45-56, 120-131`): notebook `fig15-filer-2026-11-18`, versions v3 and v4, contains seven
  temporary download links (`https://www.kaggleusercontent.com/kf/...` with an access code) to the output archives of the
  seven correction notebooks (`walls.tar` 1,215 MB, four disc archives about 1,025 MB, two shell archives 210 MB).
- **Why:** the connector's `save_notebook` silently drops attached inputs (Kaggle/kaggle-cli issue #1140; `docs/kaggle-pipeline.md:193`;
  skill `kaggle-gpu-run` line 51). v1 and v2 failed that way. The session worked round it with links instead of reading those documents.
- **What a link is:** a bearer ticket. Whoever holds the address downloads the file without logging in, until it expires.
- **Fact:** not in this repository (searched). The notebook is private, so only Numa sees them.
- **Inference:** they have probably expired. **Unverified:** how long Kaggle's links last, and whether these still work.
- **Inference:** they guard no data that is not also in the Fig. 15 dataset (its folders carry the same notebook names).
- **Unverified:** whether Kaggle can delete a single notebook version. If not, a clean new version leaves v3 and v4 in history.
- **Consequence:** this notebook can never go public; deleting it is the only certain removal. Numa has not decided; Numa
  rejected all three options offered (delete, re-run, leave) as "shit" and demanded the real data on Kaggle, not links.
- Also on Kaggle: `fig15-filer-dry` v1 (dry run; not in the notebook list returned, check) and v1's empty index output.

## 6. What the previous sessions got wrong (do not repeat)
1. Ran a Kaggle job for Fig. 15 and explained it badly; Numa asked why the data was not simply taken from the website.
   The job only copied Kaggle outputs into one dataset (rule "one dataset per figure"), but the site's copy in R2 was the other source;
   the session said the job "can't read" R2 without testing. Always state which source answered, and try the website's store first.
2. Said "nothing is regenerated" and "public can't be reversed" as facts without checking (the second is now sourced, see 8).
3. Counted 9 datasets; there are 8.
4. Proposed renaming Fig 12/14/16 to "Fig. N Name: simulation data" as the plan. Numa answered **NO**. Do not propose cosmetic renames
   as the plan. **Open:** Numa did not say why. Likely because it is not the real organisation, and Fig 12/16 are Guinness (never public).
5. Offered A/B/C options each with a flaw; B was a CPU re-run, which Numa forbids.
6. Many turns of questions instead of doing the read-only step first. Read-only inventory steps should simply be done.

## 7. Task for the next session (proposal; Numa decides)
Order, one step per turn, each with Numa's yes:
1. Read `CLAUDE.md`, `AGENTS.md`, `docs/kaggle-pipeline.md`, both skills, this report, `KAGGLE.md`.
2. **Test capability once, read-only:** can the session act on Kaggle beyond the connector (via `api.kaggle.com`, proxy-authenticated,
   or the workflow with `KAGGLE_API_TOKEN`)? Try a GET (for example list own kernels). Report what works: edit metadata, change
   visibility, delete a notebook, create a dataset version. If the answer is "no", say so plainly and stop.
3. **Open the Fig. 15 dataset files** (sizes only) and show Numa how it maps to R2 and to generations. Propose a structure
   (**Opinion**: by generation, with a README folder; raw archives kept but not the first thing a visitor meets). Nothing is moved before approval.
4. **Decide the filer notebook** with Numa: delete, or keep private. Show the facts in section 5 first.
5. **Working notebooks** (28): keep private; Numa decides names and whether any may be hidden or deleted.
6. **Tidy notebooks and datasets**: Numa decides which to polish, which to make public and when. Only items Numa names.
7. **Attach test** (tiny notebook, seconds, no GPU) to close the one open point in the skill: does the command-line push keep attached data.
8. Update the skill and `KAGGLE.md` after every change; commit and push on the session branch.

## 8. Verified evidence, with links
- Kaggle launch post: owner can switch a dataset from private to public "at any time" in Settings, Sharing:
  https://www.kaggle.com/discussions/product-feedback/50755 . It says nothing about public to private.
- Community answer (user, 7 years old, not Kaggle staff): public to private is one-way; escape is delete and re-upload:
  https://www.kaggle.com/discussions/product-feedback/153402 . Treat public as one-way. Not confirmed by staff.
- Command-line tool metadata has `dataset_sources` and `kernel_sources`:
  https://www.kaggle.com/code/citerne/from-local-dev-rtx-6000-kaggle-cli-guide . Source-name resolution pitfall:
  https://github.com/Kaggle/kaggle-api/issues/433 . **Unverified** on this account.

## 9. Checks anyone can run without a session
- Read `notes/fig15/COORDINATOR_LOG.md` lines 40-56 and 120-131.
- `grep -c OK notes/fig15/coordinator-2026-11-18/r2_upload.log` gives 2782.
- Open https://www.kaggle.com/numakoudsie while logged out: a visitor sees only public items (**Fact**, stated by Kaggle's model of
  private items; currently there should be none).
