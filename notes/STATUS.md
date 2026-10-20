# Status of the ten notes

Rule in force: judge first, change only what needs it (notes/STANDARD.md, "Numa's verdicts").
Corrected on 20 October 2026, 22:00 UTC, after an independent audit of this record.

## What is done

- The ten lecture notes were judged section by section and repaired where needed (teachers' verdicts in `figNN/plan.md`).
- Each note then had one derivation check, one blind referee reading and one walkthrough check. Every wrong row and every
  real obstacle they found is repaired in the note, except Fig. 7 §8.1 (Auto Dance; a page fault, below).
- The lines repaired after a check were verified by the lead, not by a second independent check.

| Fig. | Derivation check: verified / wrong / unverifiable | Referee: sections needing work | Walkthrough: quoted lines found verbatim |
|---|---|---|---|
| 1 | 111 / 2 / 1 | 3 | 17 / 17 |
| 2 | 65 / 4 / 1 | 3 | 31 / 31 |
| 3 | 119 / 0 / 0 | 2 | 24 / 24 |
| 4 | 107 / 0 / 0 | 3 | 16 / 16 |
| 5 | 116 / 2 / 0 | 2 | 21 / 21 |
| 6 | 79 / 3 / 0 | 2 | 19 / 19 |
| 7 | 100 / 3 / 1 | 3 | 26 / 26 |
| 8 | 90 / 5 / 0 | 1 | 22 / 22 |
| 9 | 86 / 1 / 1 | 4 | 24 / 24 |
| 10 | 91 / 4 / 1 | 2 | 26 / 26 |

Checks after the last repair, all passing: `node notes/verify.mjs /tmp/lead-dist` (1440 × 900, 1600 × 900, 390 × 844),
`node notes/walkcheck.cjs` (226/226), pages byte-identical to `db1a24b` outside the notes, `python3 tools/inventory.py --check`.

## What is not done (waits for Numa)

- The walkthrough panels ("From symbols to code", `public/scripts/walk/*.js`) were not edited: they change only with Numa's
  permission. Each uses some symbols or claims that differ from its repaired note, and six excerpts skip page lines without
  `...`. Proposed fixes: `figNN/walk.md` (audited against the current notes on 20 October; 11 of them touch code lines).
- Page faults found by the checks, not fixed because page code needs Numa's yes: listed in docs/research-theory-audit.md,
  "Lecture notes · 20 October 2026", under "Open, for Numa". The most visible: Auto Dance (Fig. 7) does nothing, live too.

## Baseline before any change

20 October 2026, headless Chromium, 1440 × 900 and 390 × 844, all folds open: all ten pages 0 console errors, 0 KaTeX errors,
0 px sideways scroll; 36 references in all, none with a link (now 40, all linked).
