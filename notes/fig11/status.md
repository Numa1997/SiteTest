# Fig. 11 rescue (swing-up) · status

Question (Numa, 3–4 Nov 2026): the rods must not stay down after a fall or a strong flick; every parameter must be explained or derived; check the physics against sources and Wolfram.

## Done, with evidence
- Equations of motion (9): Wolfram Euler–Lagrange from scratch minus page's D, C, G, H = {0,0,0}; Moysis 2016 eqs. (2)–(9) identical (opened 4 Nov).
- Linearisation, fall rates 10.388/4.101 1/s, Kalman rank 6, LQR gains (7.071, −504.022, 625.893, 15.316, −14.687, 97.935): Wolfram RiccatiSolve identical to all printed digits.
- RK4 1 ms against NDSolve 30 digits: 2.5e−6 rad after 2 s of free whirling, order 4 (ratio 18).
- Energy law dE_p/dt = −a𝒫: Wolfram Simplify → 0; one-rod limit = Åström–Furuta eq. (3).
- Catch level c*: random sampling gave ~127 (wrong); climb + Wolfram FindMaximum: 30.56–30.69 at 30, 60, 200 N; page 31.4, hand-over at 0.9 c*.
- Node study: direct planning 16/40; calm-then-plan 24/24 of the rest.
- Browser (frame driver, 8 ms planning per frame): earlier run 40/40 random states balanced, 42/42 on 7 other machine settings (before the c* fix); rerun pending.

## Open
- Browser rerun after the c* fix (r2-random, r2-machines).
- DE/AR translations (agent), ingest, build --check.
- Blind skeptic, gate 3 round 1: notes/fig11/skeptic-gate3-r1.md.
- Commit, PR, merge (Numa said YES to merging, 4 Nov 01:56), verify live.

## Decisions for Numa
- none open.
