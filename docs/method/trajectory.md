# The build film of Phyein Usul: trajectory, moves and laws

This page records how the website was built, in the order it was built, as read from the commit history of
`Numa1997/SiteTest` before that history is removed. It has three parts. The **trajectory** is the film: what was laid,
when, and in what order. The **moves** are the operations that repeat, written as functions with an input, an output and
a gate. The **laws** are the standing rules, each with the event that produced it.

**How this page was made.** On 20 November 2026 the subject line of every one of the 1,070 non-merge commits was read in
the order the commits were made (29 August 2024 to 18 November 2026, head `12c2e3a`), together with the date on which
each of 281 surviving pages, scripts, tools and doc pages first appeared. Check it with
`git log --reverse --no-merges --format='%ad %s'`. **Limits:** the subject lines were read to their first 150
characters, the changes inside each commit were not opened, and the 271 merge commits were counted but not read one by
one. Statements marked *inference* are conclusions drawn from several commits; everything else is a fact with its date.

---

## 1. The trajectory, in eight reels

| Reel | Dates | Commits | What it is |
|---|---|---|---|
| 1 | 29 Aug – 11 Nov 2024 | 38 | Bricks laid by hand |
| 2 | 16 Jan – 17 Sep 2026 | 14 | Three skins |
| 3 | 6 – 16 Oct 2026 | 44 | The frame |
| 4 | 20 – 22 Oct 2026 | 39 | The door and the standard |
| 5 | 23 – 30 Oct 2026 | 214 | The factory day and the studies |
| 6 | 31 Oct – 5 Nov 2026 | 64 | Speed, motion and fit |
| 7 | 5 – 11 Nov 2026 | 224 | Heavy physics in the browser, and its limit |
| 8 | 12 – 18 Nov 2026 | 433 | Compute elsewhere, play here |

### Reel 1 · Bricks laid by hand (2024)

Each file goes up through GitHub's web page as its own commit. A file is created without its ending, then renamed to
`.html` in a second commit (four times). `index.html` is edited more than twenty times, once per new link. By
11 November 2024 six simulations stand: transverse and longitudinal waves, wave interference, water waves, the double
slit, circular wave interference and the double pendulum. There is no shared code, no documentation and no build.

### Reel 2 · Three skins (January to September 2026)

The content stays and the look is replaced three times: a black and red theme with a particle background (16 January),
a blue and green theme with a banner (7 March), then paper and burgundy (17 September). On 17 September four layouts
follow one another within 37 minutes (plain document, cards, editorial with a live double pendulum). One commit reads
"Restore all six simulations to their original files": a restyling had reached into the simulations and was undone.

### Reel 3 · The frame (6 to 16 October 2026)

- **6 Oct.** The version of the site built as an app elsewhere (its 30th version) is moved into the repository. With it
  arrive `public/`, the Vite build, the shared script `sim.js`, the stylesheets and the first instruction file.
- **13 Oct.** The data panel is built on Fig. 1, then on all eight simulations 19 minutes later. The same evening the
  store arrives: "every simulation writes its numbers into a dataset store".
- **14 Oct.** The hover readout is replaced by the Read values tool. The catalog page, the folds and the whole of
  `docs/` appear on this one day, and the commit "Make the repository the documented source" turns the repository from
  a copy into the source.
- **15 Oct.** The first audit, in five batches A to E, each ending "verify in Chromium".
- **16 Oct.** Security: a content policy on every page, fonts served by the site itself.

### Reel 4 · The door and the standard (20 to 22 October)

- **20 Oct.** The site moves to Cloudflare. The same afternoon the four roles (teacher, derivation checker, referee,
  walkthrough keeper) and the note standard are created, and all ten lecture notes are judged and repaired by evening.
  The day ends with "Correct the review's own record after an independent audit".
- **21 Oct.** The walkthroughs are rebuilt to follow the new notes. The Fig. 2 note is rewritten as a textbook chapter
  and becomes the new standard. Cloudflare begins to deploy `main` by itself.
- **21–22 Oct.** Research projects 03 (Hydraulic Press) and 04 (Iron, Cotton and the Head) are added with their source.

### Reel 5 · The factory day and the studies (23 to 30 October)

- **23 Oct, 89 commits.** Three lines of work advance in the same minutes. *Translation:* the generator at 12:34, the
  ten simulation pages in German and Arabic by 13:59, then independent reviews applied in the evening, about 2,100
  corrections by the counts in the commit messages. *Rotor Pendula* and *Droplet Collection:* each climbs a ladder of
  models (L0, L1, …), each rung with a written contract, a skeptic's objections answered, and three gates. An
  "Inventory" commit follows each batch of new files.
- **24 Oct.** The data panel becomes a bookkeeper (headline, ledger, balanced books), piloted on Figs. 9 and 10. Fig. 11
  is born in a fixed order: page, note, walkthrough and catalog entry; then docs; then German and Arabic; then its
  ledger.
- **28 Oct.** Rotor Pendula is rewritten for a newcomer and read blind twice. The home page index is tried in four
  forms within 2 hours 17 minutes. A section "How this site is made" is added and removed 48 minutes later.
- **29 Oct.** The docs are measured against the code again ("2 384 line references remapped"). Four changes to the pages
  are reverted the same afternoon ("Pages back as they were before 29 October"). The app the site came from is removed.
- **30 Oct.** Parameter curves: Fig. 1 first, then Figs. 2 and 3, then "fixes from the first real-browser check", then
  the remaining eight, then their German and Arabic strings.

### Reel 6 · Speed, motion and fit (31 October to 5 November)

Loading speed is measured, changed in six steps and measured again on the live site, with two rounds of code review and
"claims review" between. Short addresses move to `_redirects`. Long equations wrap. Pages slide into one another. A
"tune by eye" skill is added to the repository on 1 November and removed the same day at the owner's request. On
3 November a new page takes the number Fig. 11; on 4 November the numbers are swapped back and the new page becomes
project 05. Project 05 gets a data panel with "honesty tests".

### Reel 7 · Heavy physics in the browser, and its limit (5 to 11 November)

- **Fig. 12, 5–7 Nov.** Within 20 hours the figure takes five forms: a carried pint, a waiter, a cart, a one-wheel cart,
  then a "restart brief" and a rebuild as a three-dimensional Navier–Stokes solution. It then gains worker threads, a
  real-time modal model, a Kalman filter, a nonlinear model and, in 30 minutes around midnight, a port to the graphics
  chip. Each addition to its note is followed by a referee commit and a derivation-check commit.
- **Project 05, 6 Nov.** A second session works on the fluid and reports to the first through files: a handover, a
  root-cause study, and "Findings for review by the deploying session".
- **Fig. 13, 8–12 Nov.** A chaos map, then films. On 9 November a 29 MB video stops the whole deploy; the films are then
  computed live in the browser instead of stored.
- **Project 07, 9–11 Nov.** Plan and brief, then a "librarian" who gathers data with its provenance, then a scaffold
  (contract, physics core, build, checks), then chapters 0 to 9 in under eight hours, each followed by "fixes after its
  blind reviews". Two days later the text is edited chapter by chapter by a "voice" pass and a "rhythm" pass.
- **The poem page, 10–13 Nov.** The Arabic translation goes through ten versions; one commit restores the first.

### Reel 8 · Compute elsewhere, play here (12 to 18 November)

- **12 Nov.** The first solver for Kaggle is committed at 17:16; its test notebook is "pinned" to that exact commit; its
  speed is measured at 17:23; the full grid of 405 runs follows; the Fig. 14 page that plays them stands at 18:57. The
  data is filed on the site under its date of generation.
- **13 Nov.** Fig. 12's control is derived twice (SymPy and SciPy, then Wolfram reproduces every number) before it is
  ported to JAX behind "Gate B1". The JAX runs are numbered; a "rest guard" stops a run whose pint at rest stirs itself.
  Fig. 15 starts from a brief and a file of "every mistake made on Fig. 14". Its second generation plans 3,739 runs in
  six shards, too large for the repository, so the run store (R2) is built.
- **14 Nov, 156 commits, the busiest day.** The Fig. 15 note passes ten reader rounds between 02:01 and 10:02, each
  logged in a state file, and is released as "READY at" a named commit. 3,697 runs (6.53 GB) are filed. Fig. 12's note
  is rebuilt so that every number is printed by a script from the stored runs. Fig. 16 is born from a brief and a state
  file. A separate session inventories every Kaggle notebook and matches each stored file to its origin by SHA-256.
- **15 Nov.** Fig. 16 runs 3 to 5. Audits are lettered (F to M). The note's own measurements find a sign error in the
  cart model, and run 5 repeats the rides with it corrected.
- **18 Nov.** Fig. 16's data panel is proved on Kaggle (19 of 19 checks). A corrected generation of Fig. 15 is filed as
  a preview, made the default, and the 2,782 files it replaces are deleted at the owner's order. A continuous spill
  model is built in 18 commits and stopped by the owner's decision. The in-browser Fig. 12 page is deleted: "no physics
  in the browser". The day ends with a joint log of both sessions and a handoff.

---

## 2. The moves

Each move is a function: what goes in, what comes out, the steps in order, and the gate that must pass.

| Move | Input → output | Steps, in the order the commits show | Gate | Seen |
|---|---|---|---|---|
| `pilot_then_rollout(feature)` | one idea → the same feature on every page | build on one figure; check in a real browser; fix; apply to the rest in groups | the pilot works on the live page | data panel (13 Oct), Taylor note (21 Oct), bookkeeper (24 Oct), parameter curves (30 Oct), control switch and 3D close-up (15 Nov) |
| `add_figure(n)` | a physics idea → a registered figure | page, note, walkthrough, catalog entry; docs; German; Arabic; ledger; redirects and inventory | translation check and inventory check pass | Figs. 11, 12, 14, 15, 16; projects 05, 06 |
| `translate(change)` | an English change → three languages | commit English marked "translations pending"; German; Arabic; regenerate pages; independent review; apply its corrections | generator `--check` finds nothing untranslated | every change after 23 Oct |
| `write_note(figure)` | a page → a textbook chapter | plan; write; derivation check; blind referee and two readers; fix; repeat by rounds; "READY at" a commit | checker and referee have no open finding, or the owner ends the rounds | all notes; ten rounds for Fig. 15, three for Fig. 12 |
| `study(project)` | a question → a research project page | brief; ladder of models L0…Ln, a contract per rung; skeptic rounds; Gate 1 model, Gate 2 equations, Gate 3 reader; generate the served page; Projects entry; translations | "n of n equations right", reader gate passed | Rotor Pendula, Droplet Collection, project 07 |
| `compute_elsewhere(figure)` | a solver → stored runs a page can play | solver; smoke notebook pinned to a commit; measure speed and accuracy; full batch in shards; file by generation date with SHA-256; page plays stored runs; one dataset per figure | every file's hash checked | Figs. 12, 14, 15, 16 |
| `numbered_run(k)` | a model change → a trusted run | change one thing; guard that stops a bad run; check script; pack; record | "ALL PASS", otherwise a diagnosis and run k+1 | Fig. 12 runs to 10, Fig. 16 runs 3 to 6 |
| `correct_data(generation)` | a found error → replaced data | new generation filed as a preview address; made default; note rewritten; old files deleted only on the owner's order | page and note agree with the new index | Fig. 15, 18 Nov |
| `audit(scope)` | what the docs say → what is true | measure; list differences; repair; record with a date | recount matches | 15, 20, 29 Oct; audits F–M; the Kaggle inventory |
| `register(files)` | new files → a complete file list | inventory rule; regenerate `docs/files.md` | `inventory.py --check` passes | after nearly every batch |
| `hand_over(session)` | one session's knowledge → the next session | brief; state file kept current; mistakes and rules; launch gates; a log | the next session starts from the file alone | from 23 Oct; a standing rule from 14 Nov |
| `try_and_choose(look)` | a visual question → the owner's choice | several variants within the hour; the owner picks, or the first is restored | the owner's word | 17 Sep layouts, home index, poem translations and backgrounds |

Composed, publishing one change is: **verify live ∘ merge ∘ register ∘ document ∘ translate ∘ gate ∘ build**, read from
right to left.

---

## 3. The laws, and the event behind each

| Date | Law | What produced it |
|---|---|---|
| 17 Sep | A restyling never reaches into a simulation. | "Restore all six simulations to their original files." |
| 13 Oct | A number is written into the store where it is computed. | The first data panel recomputed for display; the store replaced it the same day. |
| 14 Oct | Nothing on a running figure reacts to the pointer passing over it. | The hover readout was replaced by the Read values tool. |
| 16 Oct | The site loads nothing from another site. | The security pass; fonts moved onto the site. |
| 20 Oct | The walkthrough files change only on the owner's word. | The first review of the notes. |
| 20 Oct | The reviewer's own record is audited too. | "Correct the review's own record after an independent audit." |
| 21 Oct | Every note is a textbook chapter with every step shown. | The owner's verdict on the first round of notes. |
| 23 Oct | A generated page is never edited by hand. | The translation generator. |
| 29 Oct | The docs describe the present; a past statement gets a dated correction. | The re-measurement of the docs. |
| 3 Nov | A finished and tested change is merged and published without asking. | The owner's rule of that day. |
| 9 Nov | No served file above 24 MB. | A 29 MB video stopped a deploy. |
| 12 Nov | Stored data is filed by its date of generation and never rewritten. | The first Kaggle generation. |
| 14 Nov | A session writes its state into the repository before anything else. | Long runs that outlived a chat's memory. |
| 14 Nov | One notebook and one dataset per figure. | The Kaggle inventory found 35 notebooks. |
| 14 Nov | Nothing is deleted without the owner's explicit word. | Eleven notebooks had been deleted by a session. |
| 15 Nov | Tests and builds run on Kaggle, not in the session's own environment. | The owner's rule of that day. |
| 18 Nov | No physics is computed in the reader's browser. | The in-browser Fig. 12 page was deleted. |

---

## 4. The shape of the path (inference)

Four things move in one direction across the eight reels.

- **Where the physics is computed moves away from the reader.** Live in the page (2024); solved first, then played back
  (Figs. 9 to 11, October); worker threads and the graphics chip in the page (6–7 November); Kaggle's machines with
  stored runs (12 November); "no physics in the browser" (18 November).
- **Where the truth lives moves into the repository.** "The application comes first, the repository second"
  (13 October); "the documented source" (14 October); the move to Cloudflare (20 October); the app removed (29 October).
- **How sessions are organised grows in layers.** One session; four roles (20 October); parallel sessions with handoff
  prompts (23 October); a deploying session that judges another's findings (6 November); a coordinator with state files
  and logs (14–18 November).
- **The owner's decisions move from single steps to standing rules.** A word for each merge (October); "merge without
  asking" (3 November); rules on deletion, on cost and on where code may run (14–18 November).

The tempo rises with it: 38 commits in ten weeks of 2024, 393 in October 2026, 885 in the first 18 days of November.

---

## 5. The skeleton, as one loop

```
 brief ─▶ state file ─▶ pilot ─▶ gate ─▶ rollout ─▶ translate ─▶ register ─▶ document ─▶ merge ─▶ verify live
   ▲                      │        │                                                                    │
   │                      └─ fail ─┘  (diagnose, change one thing, run again)                           │
   └──────────── lessons file ◀── audit ◀───────────────────────────────────────────────────────────────┘
```

A piece of work enters at the brief, cannot pass a gate it fails, and leaves a lessons file that the next brief starts
from. Fig. 15 is the clearest full pass: it began on 13 November from "every mistake made on Fig. 14", went live on
14 November, was audited the same day, and its corrected generation replaced the first on 18 November.
