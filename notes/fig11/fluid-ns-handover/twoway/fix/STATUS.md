# Handover 2, status (session of 6 November 2026, continued)

## Error 1, rods under-dragged: FIXED (test-proven, not yet on the page's text)
Cause settled earlier: the rods read water their own push slowed. Discriminating experiment (fix/oseen_pred.py on fix/t_selfprof.cjs
profiles): an unbounded linear Oseen influence of the Peskin-smeared forces predicts 1.15–1.7× the measured slowing at 0.5 m/s and 8–14×
at 0.01 m/s, and depends strongly on the far-wake cut-off: the self-velocity is set by the tank (blockage, inflow, walls), so no local
influence matrix can reach ±1 % without a fitted constant. Fix built instead: the self field δu (twoway.js `selfField`, on by default),
the same linearised equations in the same tank, driven only by the rods' impulses, cart at rest and no inflow in it; the rods use u − δu,
and Du/Dt of (39) is taken from u − δu too.
- fix/run_matrix.sh → fix/matrix1.txt: 27 cases (across/along/45°, glycerol/honey/water, U 0.01–0.5, Δ and Δ/2, held and carried):
  force ÷ law = 1.0000 ± 0.0002 (base 0.709–0.971; along the stream in honey 0.709).
- fix/t_selfext.cjs → fix/ext1.txt: in the swinging cart's wake, against the truly undisturbed water (rods not pushing): force error
  1.0–2.4 % uncorrected, 0.06–0.20 % corrected.
- Energy book: rods' heat below the grid booked as −f·(v − u_read) (the law's heat less the rod's own resolved wake); t_book R unchanged.
- Cost: shadow advection reuses the main MacCormack points; shadow pressure tol 1e-2 (no change to any printed digit); main tol 1e-3
  (fix/t_tol.cjs: m_a within 1.3e-4, F_c within 4 mN, state within 6 µm; divergence 2.9e-3 / 7.9e-3 s⁻¹); measure() windowed
  (fix/t_measwin.cjs: bit-identical, 0.28 ms instead of 1.49). Chromium (fix/chrome_cost.cjs): 20.8 ms median glycerol, 22.4 water breeze
  (base before: 20.7).

## New errors found and fixed
- Test harness `frozen`: RK4 stages moved the held rods (only the step's end was held): every held-rod number since ROOTCAUSE was biased
  (honey 0.931 → 0.941 base after the fix). Also affects the page's "hand holds the rods" (held machine now held in every stage).
- Rods along the stream under-dragged up to 29 % (honey), not 3–7 % as the page says; fixed by the self field.
- Du/Dt (39) at a held rod contained the rod's own deceleration of the water (double count); fixed with the self field.

## Next
2. Benchmark not converging (validate La/Δp measurement on spectral/ns2.cjs first). 3. Momentum identity test. 4. Energy remainder.
5. Audit list. Then page 13.6, panel, docs, de/ar, Chromium, hon.cjs 5/5, merge.

## Errors 2–4 (later the same day)
- Error 2, root cause: the inlet's v was zero-gradient (the benchmark and the Wolfram FEM reference use v = 0). Fixed (v = 0 where a stream enters).
  Control-volume c_D 5.67 / 5.645 / 5.617 and La 0.0883 / 0.0862 / 0.0856 at 10 / 20 / 39 cells per D; Δp 0.1149 (−2 %). t_stprobe.cjs, st_160_*.txt.
- Error 3, root cause: the body's viscous force was the ghost-link flux weighted by the face fraction w, which misses the (1 − w) share of the
  wall shear: an error that does not shrink with the grid. Seen from the water's side, it is the viscous step's non-conservation of Σ w u
  (t_stmom.cjs: −6e-4 N at 10 per D). Fix ACCEPTED: the ledger rule (the body's viscous force = Σ w Δu of the viscous step, less the lid,
  floor and ends). c_D read on the body 5.709 / 5.705 / 5.638 against the control volume's 5.67 / 5.645 / 5.617 (old rule: 5.444 / 5.535 / 5.264).
  Independent check, from Gemini's derivation (G1): the unweighted ghost flux and the ledger must agree within O(Δ); measured 5.825 / 5.746 against
  5.709 / 5.705 (gap 0.116 → 0.041). The rest of the gap to the global balance is semi-Lagrangian non-conservation (about 2e-4 N, also present
  without a body).
- Oscillating cylinder (t_oscstokes.cjs): reference 3.020 / 1.249 confirmed independently (Gemini's G3 derivation). The solver does not converge
  to it with either rule (8 cells per radius: ledger 2.960 / 1.318, old 2.902 / 1.216): an open floor of the test, suspected confinement in the box.
- Error 4: t_ledger.cjs closes the energy book to 1e-5 J. R in glycerol, 20 ms steps (17.1 %) = splitting loss 0.210 + advection 0.092 +
  face forcing 0.047 − coupling lag 0.109 + transit 0.002 − re-weighting 0.013 J. Honey: R 7.7 % (splitting loss 0.084 J, advection 0.008 J).
