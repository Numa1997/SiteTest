# The lecture-note review: `notes/` and `.claude/agents/`

On 20 October 2026 Numa asked for the ten lecture notes at the end of the simulation pages to be checked and, where they
were unclear or wrong, repaired; his rule was "judge first, change only what needs it, never overload the simulations"
([notes/STANDARD.md](../notes/STANDARD.md), "Numa's verdicts"). This page describes the files that review left behind. None of
them is part of the website: the build serves `public/` and `index.html` only, and nothing in `public/` refers to them.

What happened next (29 October 2026): on 21 October 2026 Numa replaced "judge first" by a full rewrite of every note as a
textbook chapter (the last verdict in [notes/STANDARD.md](../notes/STANDARD.md)); Fig. 11 joined on 24 October 2026, so the
site has eleven notes. `STATUS.md` and the `figNN/*.md` files are the records of 20 October and are not kept up to date;
`notes/fig11/` holds only the scripts of its note. `notes/` also holds the working records of the two studies rebuilt here
and of the home page (table below).

## The team, `.claude/agents/`

Four agent definitions for Claude Code, one file each; Claude Code offers them as agent types when a session opens this
repository.

| File | Role |
|---|---|
| [physics-teacher.md](../.claude/agents/physics-teacher.md) | Writes the lecture note of one page: since Numa's verdict of 21 October 2026 it rewrites the whole note as a textbook chapter (until then it judged each section and repaired only those judged "needs work"); its plan goes to `notes/figNN/plan.md`. |
| [derivation-checker.md](../.claude/agents/derivation-checker.md) | Re-derives every numbered equation (SymPy) and recomputes every number from the page's own code, without reading the teacher's plan; writes `check.md`. |
| [referee.md](../.claude/agents/referee.md) | Reads the rendered note blind, as a school student and as a graduate; writes `referee.md` with real obstacles (A), matters of taste (B) and overloaded passages (C). |
| [walkthrough-keeper.md](../.claude/agents/walkthrough-keeper.md) | Checks by script that the walkthrough quotes the page's code character for character, and that its formulas match the note; writes `walk.md`. It never edits the walkthrough. |

## The record, `notes/`

| Path | What it holds |
|---|---|
| [STANDARD.md](../notes/STANDARD.md) | The standard every note is judged against, Numa's decisions, and his verdicts, which override the rest. |
| [STATUS.md](../notes/STATUS.md) | What is done (one row of check results per figure) and what waits for Numa. |
| [verify.mjs](../notes/verify.mjs) | The lead's check of the eleven pages in headless Chromium (Fig. 11 added to its list on 29 October 2026) at 1440 × 900, 1600 × 900 and 390 × 844: console and KaTeX errors, sideways scroll, folds, equation numbers, links in the reading lists, and display equations wider than their box. On 29 October 2026 it finds no console or KaTeX error on any page, and display equations wider than their box (the box then scrolls sideways) at 1600 × 900 on Figs. 2, 6, 8, 9 and 11, where the data panel opens beside the note, and at 1440 × 900 Fig. 2's (8). Run after `OUT_DIR=/tmp/lead-dist npm run build` as `node notes/verify.mjs /tmp/lead-dist`. |
| [walkcheck.cjs](../notes/walkcheck.cjs) | Searches every quoted code line of the eleven walkthroughs in its page (29 October 2026: 753 of 758 found; for the other five, the page now passes their text through `_t(…)`, and the walkthroughs of Figs. 3, 4 and 5 still quote the line without it), by the recipe of [scripts/walk.md](scripts/walk.md). Run as `node notes/walkcheck.cjs`. |
| [.gitignore](../notes/.gitignore) | Keeps the agents' screenshots out of the repository; the scripts beside them reproduce them. |
| `figNN/plan.md` | The teacher's verdict on each section of the note of Fig. NN and what it changed. |
| `figNN/check.md` | The derivation checker's table: one row per equation and per number, "verified", "wrong, because …" or "unverifiable, because …". |
| `figNN/referee.md` | The blind referee's report. |
| `figNN/walk.md` | The walkthrough check: counts of quoted lines found verbatim, and every mismatch with its exact old → new text. These fixes wait for Numa's word, because walkthrough files change only with his explicit permission. |
| `droplets/` | The working record of the Droplet Collection rebuild (23 October 2026): brief, definition of done, status, the derivation contracts and checks per model level, skeptic and review rounds, sources. |
| `rotor-pendula/` | The working record of the Rotor Pendula rebuild (24 to 29 October 2026): `README.md` (the setup, the models and the scripts in `derive/`), sources (`dossier-*.md`), teaching notes. |
| `home/` | Two scripts that measure the home page in Chromium (index panel, column width, characters per line, sideways scroll). |
| other files in `figNN/` | The scripts each agent wrote to measure the numbers it states (Node scripts that run the page's own functions or drive the built page in Chromium, Python with SymPy or NumPy), and their saved output. |

What the review found and changed, per figure, is in [research-theory-audit.md](research-theory-audit.md), section
"Lecture notes · 20 October 2026", and in the "Teaching revision" and "Repair round" entries of each page's doc in
[simulations/](simulations/).
