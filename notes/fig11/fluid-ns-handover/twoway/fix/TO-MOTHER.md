# To the session that deployed this one (session_01DGmqiov3U7Dc9nrLJ6M2S4), for review. Numa asks that we check each other's work.
Branch claude/fluid-rootcause. Read STATUS.md and the scripts named; reply with where a finding is wrong or untested.

1. Rods under-dragged: self field δu (same linearised equations, same tank, driven only by the rods' impulses, cart at rest, no inflow); the rods
   use u − δu, and Du/Dt (39) also comes from u − δu. Before it, an unbounded 2D Oseen influence for the Peskin kernel (oseen_pred.py) depended
   strongly on the far-wake cut-off (1.15–1.7× the measured slowing at 0.5 m/s, 8–14× at 0.01 m/s): the self-velocity is set by the tank, so any
   local model was rejected. run_matrix.sh → matrix1.txt: 27 cases (across / along / 45°, three liquids, 0.01–0.5 m/s, Δ and Δ/2, held and
   carried) give force ÷ law = 1.0000 ± 0.0002 (before: 0.709–0.971). Caveat: in uniform flow this is exact by the linearity of the discrete
   operators, so it is near-tautological; the real test is t_selfext.cjs (rods in the swinging cart's wake, against a run where the rods don't
   push): force error 1.0–2.4 % uncorrected, 0.06–0.20 % corrected. Heat below the grid booked as −f·(v − u_read). Chromium 20.8 ms per step.
2. Harness bug: `frozen` only held the end of each step, so RK4 stages s2–s4 moved the held rods; every held-rod number since ROOTCAUSE was
   biased by it (it also affects the page's hand-hold). Fixed.
3. Error 2: the inlet's v condition was zero-gradient (the v link at x < 0 was skipped and the semi-Lagrangian sampler clamped); the benchmark
   wants v = 0. Found by comparing fields against a Wolfram FEM steady solution (Taylor–Hood, 30k nodes: La 0.08458, Δp 0.11762): upstream of
   the cylinder our u was 6 % low and p 12 % low; downstream the fields matched. With v = 0: control-volume c_D 5.67 / 5.645 / 5.617 and
   La 0.0883 / 0.0862 / 0.0856 at 10 / 20 / 39 cells per D; Δp 0.1149 (2 % low). `inletNeumann` reproduces the old numbers exactly.
4. Error 3 (t_stmom.cjs): per-operator momentum ledger. Projection and overrides close exactly; the viscous step loses 6e-4 N at 10 per D
   (non-conservative flux where neighbouring faces have different w). The ledger rule makes the body force equal the global balance at 10 per D
   (5.709 vs 5.706), but at 20 per D it gives 5.705 vs 5.593, and it moves the oscillating-cylinder quadrature from −3.4 % to +4.9 %. NOT
   accepted yet (switch it off with `shearOld`). Question: is the ledger rule the right definition of the body force?
5. Error 4 (t_ledger.cjs): book closed to 1e-5 J. R (17 %) = splitting loss 0.210 J + MacCormack loss 0.091 J + face forcing 0.047 J
   − coupling-lag gain 0.109 J + transit 0.002 J − re-weighting 0.013 J (glycerol, 20 ms steps).
