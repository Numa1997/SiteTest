# Can Phyein Usul be rebuilt? What exists, what is missing, what was saved

This page answers one question for the repository `Numa1997/SiteTest`: if only the latest version is kept and the
history is removed, can the whole work be recovered, repeated and reproduced? It was written on 20 November 2026 from
tests run on a fresh copy of the repository at commit `12c2e3a` (18 November 2026). The method is described in
[model.md](model.md) and the order in which the site was built in [trajectory.md](trajectory.md).

**The answer in one paragraph.** The site as visitors see it can be recovered from the latest version alone. The method
can be repeated from the documents, with gaps in the tooling. The stored simulation data can be recomputed after the
history is removed only from the solver code saved in [`tools/kaggle/pinned-code/`](../../tools/kaggle/pinned-code/),
because Kaggle downloads that code from GitHub by commit id and those ids disappear with the history.

The three words mean different things here:

- **Recover:** get the site back exactly as it is now, after a loss.
- **Repeat:** do the same kind of work again, for example add a new figure, and arrive at the same quality.
- **Reproduce:** run a stored computation again and get the same files, byte for byte or within a stated tolerance.

---

## 1. Recover: what the site consists of, and where each part lives

| Part | Where it lives | In the latest version? | Evidence | Gap |
|---|---|---|---|---|
| Pages, scripts, styles, drawings | repository, `index.html` and `public/` | yes | 202 of 202 built files are byte-identical to the live site (20 November 2026) | none found |
| Stored runs of Figs. 12, 14, 16 and Fig. 15's indexes | repository, `public/data/` (807 MB, 4,500 files) | yes | each generation has an index with sizes and SHA-256 | not compared with the live site |
| Stored runs of Fig. 15 that the page plays | Cloudflare R2 bucket `phyein-usul-runs`, 3,697 files, 4.44 GB (generation 2026-11-18) | **no** | `generations.json`; the page reads them under `/r2/` | the only copy outside R2 is on Kaggle; not checked |
| Build settings | `package.json`, `package-lock.json`, `vite.config.ts`, `wrangler.jsonc`, `public/_headers`, `public/_redirects`, `worker/r2.js` | yes | read; built | none found |
| Cloudflare setup | Cloudflare dashboard: the Worker, two custom domains, the link to GitHub, the R2 bucket and its binding | **no**, described in [usul.md](../usul.md) | read | the steps are prose, not a script |
| Kaggle notebooks and datasets | Kaggle account, private: one notebook and one dataset per figure | **no**, listed in `notes/inventory/` and [kaggle-pipeline.md](../kaggle-pipeline.md) | read | private; cannot be checked from outside |
| Secrets (Kaggle token, R2 token) | Cloudflare and the session proxy | no, by design | the docs say they are never written down | must be issued again after a loss |
| Earlier versions, deleted pages | git history only | no | for example the in-browser Fig. 12 page deleted on 18 November | lost with the history, by the owner's choice |

**The build test of 20 November 2026.** `npm ci` from `package-lock.json`, then `npm run build`, gave 4,836 files, none
above 24 MB. Every built `.html`, `.js`, `.css` and `.svg` file outside `data/` (202 files, `index.html` included) was
fetched from phyeinusul.com and compared by SHA-256: all 202 are identical. The data files were not compared.

---

## 2. Repeat: can the same work be done again from what is written?

**What is there.** The instruction files, the pages of `docs/`, the note standard, four role files, 113 handoff and
state files, and the two pages beside this one: the model, and the trajectory with its twelve moves.

**What the repository's own checks said about commit `12c2e3a`.** Three checks exist; they were run on a fresh copy.

| Check | Command | Result on 20 November 2026 |
|---|---|---|
| Addresses | `python3 tools/redirects.py --check` | passes: 178 rules, up to date |
| File list | `python3 tools/inventory.py --check` | failed ("docs/files.md is out of date"); regenerated in the commit that added this page |
| Translations | `python3 tools/i18n/build.py --check` | **fails:** the German and Arabic `wind-turbine.html` are stale; one string of `fold.js` has no German and no Arabic |

**What a newcomer would still have to guess.**

- **No list of Python or Node packages.** The tools import numpy, scipy, jax, matplotlib, sympy, playwright, skimage,
  PIL and numba; the check scripts need Playwright with Chromium and katex. No file names them or their versions.
- **No single table of generators.** There are 38 build, pack and file scripts under `tools/` and `portfolios-src/`.
  Their commands are spread over `AGENTS.md`, the README and eight doc pages.
- **Rules that live outside the repository.** Several commits refer to skills ("data-panel skill", "physics-model-loop
  prompt"); only one file sits under `notes/skills/`.

**The build tools are pinned since 20 November 2026.** Until then there was no lockfile and each build took the newest
allowed versions. `package-lock.json` now fixes vite 6.4.6, tailwindcss 3.4.19, postcss 8.5.33, autoprefixer 10.7.0,
typescript 5.9.3 and their dependencies, 141 packages in all.

---

## 3. Reproduce: can a stored run be computed again?

**The mechanism.** A Kaggle notebook does not carry its solver. Its first cell downloads the solver from GitHub at one
exact commit, by an address of the form `raw.githubusercontent.com/Numa1997/SiteTest/<commit id>/tools/kaggle/…`. The
index beside each stored generation records that commit id. This is what lets anyone rerun a job "with the exact code
that made the data" ([kaggle-pipeline.md](../kaggle-pipeline.md)).

**What the history removal does to it (measured 20 November 2026).**

- 37 different commits are named by full id in data indexes, notebook builders, the inventory and the docs.
- For 31 of them, the solver folders at that commit differ from the latest version. Rerunning with the latest code
  would not be the same computation.
- The inventory of 14 November (`notes/inventory/INVENTORY.md`, finding 9) already notes that nine pinned commits sit
  on no branch and answer only because GitHub has not yet cleaned them up.
- After the history is replaced by one commit, all 37 ids are in that position. When GitHub drops them, the addresses
  stop answering.

**What is saved in `tools/kaggle/pinned-code/`.** For each of the 37 commits, every file of the solver folders as it
was at that commit:

- 99 file versions that differ from the tree of `12c2e3a`, 1.77 MB, each under the first seven characters of its commit
  id, at its original path;
- [`manifest.json`](../../tools/kaggle/pinned-code/manifest.json), which lists, per commit, every solver file with its
  SHA-256 and where its exact bytes are: `latest` (the same file in the tree of `12c2e3a`) or `archive` (saved here);
- a verification pass on 20 November 2026: 99 of 99 archived files hash to their manifest entry.

Folders covered: `tools/kaggle/resonant-tunnelling`, `tools/kaggle/schrodinger-sphere`,
`tools/kaggle/schrodinger-shapes`, `tools/fig12`, `tools/fig16`, and `public/scripts/guinness-glass.js`.

A file marked `latest` is only guaranteed while the solver file it names stays as it was at `12c2e3a`. Before such a
file is changed, its present version belongs in the archive too.

**What this does not yet fix.** The notebooks on Kaggle still ask GitHub for the old addresses. To rerun a job after the
removal, a notebook has to read this archive instead. No notebook was changed. Six of the 37 ids (all of 15 October) are
cited by doc pages as line references, not by notebooks; those links stop working with the history.

---

## 4. Verdict by part

| Part | Recover | Repeat | Reproduce |
|---|---|---|---|
| Simulation pages, Figs. 1 to 11 | yes | yes, from `add_figure` and the docs | computed in the page; nothing stored |
| German and Arabic pages | yes | yes, generator present | **not exact:** two stale pages |
| Research project pages | yes | generators present; not run in this test | not tested |
| Lecture notes | yes | the standard and the roles are written | Fig. 12's numbers come from a script; others by hand |
| Figs. 12, 14, 16 stored runs | yes | pipeline documented | only with the archive of section 3 |
| Fig. 15 stored runs | **depends on R2 and Kaggle** | pipeline documented | only with the archive of section 3 |
| Deployment | yes, by redoing the dashboard steps | documented as prose | not applicable |
| Reasons and decisions | yes, in `docs/` and `notes/` | — | — |

---

## 5. What still stands between the present state and "fully rebuildable"

Stated as facts, in the order they would block a rebuild:

1. The translation check fails (two stale pages, one string without German and Arabic).
2. The Kaggle notebooks fetch their solver by commit id and have not been pointed at the archive.
3. No file lists the Python and Node packages with versions.
4. No single page lists every generator with its command, its inputs and its outputs.
5. Fig. 15's played runs have no verified second copy outside R2.
6. The Cloudflare setup is described in prose and has never been replayed from the description.
7. The stored data files of a fresh build have not been compared with the live site.
