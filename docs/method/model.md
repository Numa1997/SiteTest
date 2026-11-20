# How Phyein Usul is built: the model behind the repository

This page describes the method by which the website phyeinusul.com was built, as it can be read out of the repository
`Numa1997/SiteTest` and its history. It is written so that a later session, or the owner, can build on the method without
the history that produced it.

**How this page was made.** Read on 20 November 2026 from a fresh copy of the public repository at commit `12c2e3a`
(18 November 2026, 22:26 UTC): the README, `AGENTS.md`, `CLAUDE.md`, the pages of `docs/` named below, `notes/STANDARD.md`,
`wrangler.jsonc`, `worker/r2.js`, `public/_headers`, and the log of all 1,341 commits. The order in which the site was
built is in [trajectory.md](trajectory.md); what a rebuild needs is in [rebuild.md](rebuild.md).
Each statement below is one of three kinds. A **fact** names the file or command that shows it. An **inference** is a
conclusion drawn from several facts. Where a sentence is an inference it says so.

---

## 1. The model in one picture

Think of a printing house with one manuscript room. Everything a reader ever sees is printed from manuscripts kept in that
one room. Some sheets are written by hand (the English pages). Others are never written by hand: a machine sets them from
the manuscripts (the German and Arabic pages, four of the research projects, the file list). A proofreader who did not
write the sheet checks it against the manuscript before it leaves. The press at the door prints whatever the room holds
the moment a sheet is filed under "main", and nobody carries sheets to the press by hand.

```
   written by hand                 made by a generator               checked                    served
 ┌──────────────────┐   tools/…   ┌──────────────────────┐  tests  ┌──────────────┐  merge   ┌─────────────────┐
 │ index.html       │ ──────────▶ │ public/de, public/ar │ ──────▶ │ real browser │ ───────▶ │ main            │
 │ public/*.html    │             │ public/portfolios/   │         │ --check runs │  into    │  │ Cloudflare    │
 │ public/scripts   │             │ docs/files.md        │         │ 3-way proof  │          │  ▼ builds dist/ │
 │ portfolios-src/  │             │ public/_redirects    │         └──────────────┘          │ phyeinusul.com  │
 │ i18n/ tables     │             │ *.rtl.css            │                                   └─────────────────┘
 └──────────────────┘             └──────────────────────┘
          ▲                                                                                   heavy runs, computed
          └── docs/ and notes/ are brought up to date in the same change                      elsewhere: Kaggle ─▶
                                                                                              public/data/ or R2
```

In one sentence: **one source, generated copies, a check before every door, and a door that opens by itself.**

---

## 2. Structure: what lives where, and why

| Layer | Where | Rule that governs it |
|---|---|---|
| Pages written by hand | `index.html`, `public/simulations.html`, `public/portfolios.html`, `public/simulations/*.html` | Each simulation page is one self-contained HTML file with its own script inline. |
| Shared machinery | `public/scripts/` (`sim.js`, `dataset.js`, `datalog.js`, `fold.js`, `catalog.js`, `walk/`), `public/styles/` | Loaded in a fixed order: folds, helpers, data store, the page's own script, the data panel (`docs/architecture.md`). |
| Generated pages | `public/de/`, `public/ar/`, `public/portfolios/<name>/`, `*.rtl.css`, `public/_redirects`, `docs/files.md` | Never edited by hand. Edit the source and run the generator; each generator has a `--check` that fails when its output is stale. |
| Sources of generated pages | `portfolios-src/<name>/`, `i18n/<lang>/` tables | Not served to visitors. |
| Stored computation | `public/data/<project>/<date>/`, the R2 bucket `phyein-usul-runs` | A run file never changes; a new run gets a new name. Each file's SHA-256 is listed in an index in the repository. |
| Work records | `notes/` | Not served. Plans, checks, referee reports, handoff and state files of each piece of work. |
| Explanation | `docs/` (44 pages), `README.md` | A change is not done until the page of `docs/` that describes the changed file says what the code now does. |
| Maintenance scripts | `tools/` | `inventory.py` (file list), `redirects.py` (addresses), `i18n/build.py` (translations), `perf/`, `kaggle/`. |
| Deployment settings | `wrangler.jsonc`, `worker/r2.js`, `public/_headers`, `vite.config.ts`, `package.json` | See section 4. |
| Instructions for sessions | `AGENTS.md` (project facts), `CLAUDE.md` (working method), `.claude/agents/` (four roles) | Read by a session before it works here. |

Facts on size (counted in the copy read): 6,683 tracked files, of which 4,835 lie under `public/`. Of those, 4,437 are
`.bin` run files, 79 are HTML pages (17 each under `de/` and `ar/`), 84 are scripts and 80 are font files.

### Anatomy of one simulation page

A page reads from top to bottom as five parts (`docs/architecture.md`): the figure, the controls, the lecture note
(`<article class="paper" id="paper">`), the walkthrough "From symbols to code", and the data panel. Adding a simulation
means four things (`AGENTS.md`): the page file, one entry in `SIMULATIONS` in `scripts/catalog.js`, a thumbnail, and its
number in the figure links at the top of the other pages.

---

## 3. Method: the principles that recur

These are the rules that appear again and again in the instruction files and the commit log. Sections 3.1 to 3.6 are
facts, each with the file that states it. Section 3.7 is an inference.

**3.1 One source, and copies are made, not written.** English is the only source of text; `tools/i18n/build.py` writes
German and Arabic from it, "so a translation can never silently describe an older page" (`docs/i18n.md`). The same holds
for four research projects (`portfolios-src/<name>/…/build*.py --site`), for the address table and for the file list.

**3.2 The number is written where it is computed.** The picture is a lab notebook (`docs/architecture.md`): the
simulation writes each value into one store (`Sim.dataset()`) at the line that computes it, and the data panel only reads
that store. Nothing is computed a second time for display.

**3.3 Every shown number is proved three ways.** The stored value, the formula recomputed from the stored inputs, and the
pixel read back from the picture, at the same frame (`CLAUDE.md`, "A data table is a pipeline"). A read-back test first
checks that something was drawn at all.

**3.4 Measure, never estimate.** Numbers in a note come from running the page's own code in a real browser (headless
Chromium), equations are re-derived (SymPy or Wolfram), and only sources that were opened are cited (`CLAUDE.md`,
`notes/STANDARD.md`).

**3.5 The author does not grade the work.** Four roles, one file each in `.claude/agents/`: the physics teacher writes a
lecture note; the derivation checker re-derives every equation without reading the teacher's plan; the referee reads the
rendered note blind, as a school student and as a graduate; the walkthrough keeper compares quoted code with the page,
character for character. Each writes its report into `notes/figNN/`.

**3.6 The owner's verdicts override everything written before them.** `notes/STANDARD.md` keeps them dated and in his
words. The verdict of 21 October 2026 replaced "judge first, smallest change" with a full rewrite of every note as a
textbook chapter in the manner of J. R. Taylor's *Classical Mechanics*.

**3.7 The repository is the memory (inference).** A session's context is lost when the chat is compacted or ends. The
method answers this by writing state into files: each chat "first writes its full state into the repository" (`CLAUDE.md`,
rule of 14 November 2026), and 113 files under `notes/` carry handoff, handover, state or coordinator in their names. The
inference is that `notes/` and `docs/` together are meant to replace both a session's memory and the commit history as the
record of why things are as they are.

---

## 4. Deployment: how a file reaches a visitor

**The chain (facts, `docs/usul.md`, `wrangler.jsonc`).**

1. A commit arrives on the branch `main` of the GitHub repository.
2. Cloudflare Workers Builds, connected to that repository since 21 October 2026, starts by itself and runs
   `npm run build` and then `npx wrangler deploy`.
3. `npm run build` is `vite build`: it takes the root `index.html` as the entry page and copies everything under
   `public/` unchanged into `dist/`.
4. `wrangler deploy` publishes `dist/` as the static assets of the Worker `phyein-usul`, reachable at `phyeinusul.com`,
   `www.phyeinusul.com` and a `workers.dev` address.
5. The Worker's one script, `worker/r2.js`, answers only `GET` and `HEAD` under `/r2/` for keys of one fixed pattern, from
   the R2 bucket; every other request is a static file.
6. GitHub Pages republishes `main` as it is, without the build, at `numa1997.github.io/SiteTest/`, kept as a backup.

So **merging into `main` is publishing**. There is no server code beyond that one script, no database and no login.

**Each deploy is a version that can be rolled back.** Cloudflare lists them under Workers → phyein-usul → Deployments
(`docs/usul.md`). This is a second history, independent of git.

**Ways the door has failed (facts, each dated in `docs/usul.md`).**

| What happened | When | What the docs prescribe |
|---|---|---|
| A file over 25 MiB made the whole deploy fail; the live site kept the old version. | 9 November 2026 | `find public -size +24M` must print nothing before a merge. |
| A merge started no build at all. | 6 and 9 November 2026 | Check the commit's check-runs for "Workers Builds"; retry the build in the dashboard; reconnect the repository if needed. |
| The same commit was pushed to a branch and to `main`; the check failed in the same second. | 12 November 2026 | Any new commit on `main`, or Retry build. |

**Security as built (facts).** Every page carries a Content-Security-Policy meta tag that admits the site's own files
only; response headers come from `public/_headers`; fonts and KaTeX are served by the site itself. A fresh comparison on
20 November 2026 found 57 of 57 sampled live files byte-identical to the repository.

---

## 5. Updates: how a change travels

The path, as `README.md` and `AGENTS.md` state it:

1. Change the source in the repository, on a branch.
2. Run the generators the change touches: `tools/i18n/build.py` after an English page changes,
   `tools/redirects.py` after a page is added, renamed or removed, a project's own `build*.py --site`.
3. Build (`npm run build`) and test in a real browser, on a desktop and a phone-sized window.
4. Bring the pages of `docs/` up to date, then run `python3 tools/inventory.py`, which rewrites `docs/files.md` and fails
   if any file is undescribed.
5. Commit, merge into `main`. Since 3 November 2026 the rule in `CLAUDE.md` is: when a change is finished, checked against
   the other sessions' work on `main` and tested, merge and publish without asking, then verify the live site.

**Several sessions at once (facts from the log).** The repository holds 152 remote branches: 79 named after the session that
made them, and the rest named after their work (`lucretius-…`, `rotor-…`, `fig11-…`, `arabic-…`). 128 are already merged
into `main` and 24 are not. 271 of the 1,341 commits are merges, and pull request numbers run up to #161. Sessions merge
`main` into their branch before merging back ("Merge main into the session branch").

**Shape of a commit message (inference from the last 25).** A subject line names the piece of work first, then what
changed and often a measured number, for example "Continuous spill: air drag through a one-sided smoothed surface delta,
so the summed force equals frontal area times pressure (drag check 1 gave 67 % of the law)". The log was being used as a
dated lab journal.

---

## 6. Heavy computation: bake elsewhere, serve from the shelf

The picture in `docs/kaggle-pipeline.md` is a bakery that bakes at night: Kaggle's graphics cards compute a block of runs
ahead of time, and the website only hands out what is stored. The rules stated there:

- **Store first.** A page plays back stored runs; where a run is missing it shows a rough live preview and says so.
- **Named by the date of generation.** `public/data/<project>/<YYYY-MM-DD>/` with an `index.json` holding the notebook
  reference, the solver's git commit and each file's size and SHA-256. Nothing already published is rewritten.
- **One notebook and one dataset per figure** on Kaggle (rule of 14 November 2026).
- **Compact on the site, full on Kaggle.** Symmetry is used before storing three-dimensional fields.
- **Too large for the repository goes to R2**, served under `/r2/`, and the page checks each file's hash against the
  index in the repository, so the bucket needs no trust of its own.
- A page cannot order a new run: the on-demand Worker `kaggle-bridge` was dropped on 20 November 2026 (owner's decision).

---

## 7. The history in numbers, before it is removed

| Period | Commits | What the log shows |
|---|---|---|
| August 2024 to March 2026 | 52 | Files uploaded by hand through GitHub's web page: the first simulations, `index.html`. |
| September 2026 | 11 | Work resumes. |
| October 2026 | 393 | `public/` and the Vite build (6 Oct), `docs/` and `tools/` (14 Oct), the move to Cloudflare (20 Oct), automatic deploys (21 Oct), `notes/` and the four roles (20 Oct), `portfolios-src/` (21 Oct), German and Arabic (23 Oct). |
| November 2026 (to the 18th) | 885 | Figs. 12 to 16, the Kaggle pipeline (12 Nov), the R2 run store (13 to 14 Nov). Busiest day: 14 November, 156 commits. |

**What the history holds that the files do not.**

- The dated sequence of commit messages, which served as a journal (section 5).
- Every earlier state of every file. The live site's earlier states are also kept by Cloudflare as deploy versions.
- The targets of commit references in the text: `docs/`, the README and the instruction files name a seven-character
  commit hash 32 times, and `notes/` 95 times (for example `3dffa3b`, `bf4edf8`, `f831bbf`). After the history is
  replaced these names point at nothing.

**What the history does not hold alone.** The dated decisions, the failure cases and the measurements are written out in
`docs/` and `notes/`; this page was assembled almost wholly from those files, and the log added only the counts of
sections 5 and 7.

---

## 8. Where the repository does not yet follow its own model

Facts seen while reading, stated without a remedy:

- **No lockfile until 20 November 2026.** `package.json` uses `^` ranges, so each Cloudflare build could install newer
  versions of the build tools than the last one did. `package-lock.json` pins them since that day ([rebuild.md](rebuild.md)).
- **Counts in the README disagree with each other.** Its opening says "ten interactive simulations", its table of paths
  says "twelve simulation pages", and its list stops at Fig. 11, while `docs/simulations/` describes figures up to 16.
- **`AGENTS.md` is one dense block.** Its 94 lines hold several thousand words in a few paragraphs; the method is in
  there, but a reader cannot find a rule without reading all of it.
- **The backup serves everything.** GitHub Pages publishes the whole repository unbuilt, `notes/` and the instruction
  files included (`docs/build-and-deploy.md` says so).
- **Branches outlive their work.** 128 merged branches are still on GitHub.
