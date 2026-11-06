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
