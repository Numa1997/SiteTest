# Status of the ten notes

Updated by the lead. Rule in force: judge first, change only what needs it (notes/STANDARD.md, "Numa's verdicts").
State on 20 October 2026, 17:00 UTC. At 16:10 UTC every running agent stopped on the account's usage limit (it resets at
19:50 UTC); the lead made the repair rounds itself from the reports that had been written by then.

| Fig. | Teacher: sections clear / needing work | Lead's review | Derivation check | Blind referee | Walkthrough | Repair round (lead) |
|---|---|---|---|---|---|---|
| 1 | 9 clear / 3 needing work | all kept | stopped by the limit | stopped by the limit | quotes 17/17 (lead's script); symbols not yet checked | none yet |
| 2 | 6 clear / 6 needing work | kept; one clause cut (a third failure case of RK4) | stopped by the limit | stopped by the limit | quotes 31/31 (lead's script); symbols not yet checked | equations (5), (8), (9), (13) reflowed so their numbers show |
| 3 | 7 clear / 4 needing work | all kept | 119 verified, 0 wrong | 8 clear, 2 needing work | 24/24 quoted; 2 symbol mismatches listed | 67.5 px vs the exact 72 px; single-photon reason; sign-free distance in §8 |
| 4 | 4 clear / 6 needing work | all kept | stopped by the limit | 6 clear, 3 needing work, 4 overloaded | 16/16 quoted; 3 mismatches listed | 4 obstacles fixed; 2 overloaded passages trimmed |
| 5 | 8 clear / 4 needing work | all kept | stopped by the limit | 8 clear, 2 needing work | 21/21 quoted; 5 mismatches listed | 2 obstacles and 2 physics gaps fixed |
| 6 | 6 clear / 4 needing work | all kept | 79 verified, 3 wrong | 7 clear, 2 needing work | 19/19 quoted; 7 mismatches, 2 silent elisions listed | the 3 wrong rows and 2 obstacles fixed; (5) reflowed |
| 7 | 7 clear / 4 needing work | all kept | stopped by the limit | 6 clear, 3 needing work | 26/26 quoted; 5 mismatches listed | 5 obstacles fixed |
| 8 | 6 clear / 5 needing work | all kept | stopped by the limit | 8 clear, 1 needing work | 22/22 quoted; 10 mismatches listed | §5 made readable without the ★ section |
| 9 | 4 clear / 7 needing work | all kept | stopped by the limit | 6 clear, 4 needing work | quotes 24/24 (lead's script); keeper's report written | 4 obstacles fixed; Figure 3 label fits; §9 trimmed |
| 10 | 2 clear / 9 needing work | all kept | stopped by the limit | stopped by the limit | quotes 26/26 (lead's script); symbols not yet checked | equations (3), (10) reflowed |

Checks run by the lead after the repair rounds, all passing:
- `node notes/verify.mjs /tmp/lead-dist`: the ten pages at 1440 × 900 and 390 × 844, no console or KaTeX errors, no sideways
  scroll, every fold opens, every numbered equation present, no display equation wider than its box at 1440 px.
- `node notes/walkcheck.cjs`: 226 of 226 quoted code lines found verbatim in their pages.
- Every page byte-identical to `db1a24b` outside `<article id="paper">`; no shared script, style or other page changed.
- `python3 tools/inventory.py --check`.

Open:
- Derivation checks for Figs. 1, 2, 4, 5, 7, 8, 9, 10 and blind referees for Figs. 1, 2, 10: to resume after 19:50 UTC.
- Walkthrough symbol fixes (all figures): listed in `figNN/walk.md`, waiting for Numa's word on editing walkthrough files.
- Code findings, report only: see `docs/research-theory-audit.md`, section "Lecture notes · 20 October 2026".

Baseline before any change (20 October 2026, headless Chromium, 1440 × 900 and 390 × 844, all folds open): all ten pages
0 console errors, 0 KaTeX errors, 0 px sideways scroll; 37 references in all, none with a link.
