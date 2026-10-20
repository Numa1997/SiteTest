# Status of the ten notes

Rule in force: judge first, change only what needs it (notes/STANDARD.md, "Numa's verdicts"). State on 20 October 2026, 21:00
UTC: every check is complete and every finding is repaired, except the walkthrough fixes and the page faults, which wait for
Numa (docs/research-theory-audit.md, "Lecture notes · 20 October 2026").

| Fig. | Teacher: clear / needing work | Derivation check: verified / wrong / unverifiable | Blind referee: clear / needing work | Walkthrough quotes | Walkthrough mismatches (listed in walk.md) |
|---|---|---|---|---|---|
| 1 | 9 / 3 | 111 / 2 / 1 | 8 / 3 | 17 / 17 | 6 |
| 2 | 6 / 6 | 65 / 4 / 1 | 6 / 3 | 31 / 31 | 8 |
| 3 | 7 / 4 | 119 / 0 / 0 | 8 / 2 | 24 / 24 | 2 |
| 4 | 4 / 6 | 107 / 0 / 0 | 6 / 3 | 16 / 16 | 3 |
| 5 | 8 / 4 | 116 / 2 / 0 | 8 / 2 | 21 / 21 | 5 |
| 6 | 6 / 4 | 79 / 3 / 0 | 7 / 2 | 19 / 19 | 7 |
| 7 | 7 / 4 | 100 / 3 / 1 | 6 / 3 | 26 / 26 | 5 |
| 8 | 6 / 5 | 90 / 5 / 0 | 8 / 1 | 22 / 22 | 10 |
| 9 | 4 / 7 | 86 / 1 / 1 | 6 / 4 | 24 / 24 | 4 |
| 10 | 2 / 9 | 91 / 4 / 1 | 8 / 2 | 26 / 26 | 4 |

All wrong rows and real obstacles are repaired in the notes, except the Fig. 7 Auto Dance fault, which is in the page's
security policy. Checks after the last repair: `node notes/verify.mjs /tmp/lead-dist` (1440 × 900, 1600 × 900, 390 × 844),
`node notes/walkcheck.cjs` (226/226), pages byte-identical to `db1a24b` outside the notes, `python3 tools/inventory.py --check`.

Baseline before any change (20 October 2026, headless Chromium, 1440 × 900 and 390 × 844, all folds open): all ten pages
0 console errors, 0 KaTeX errors, 0 px sideways scroll; 37 references in all, none with a link.
