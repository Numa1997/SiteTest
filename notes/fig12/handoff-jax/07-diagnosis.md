# Fig. 12: diagnosis of the five open items (14 November 2026)

For the coordinating chat "Guinness and resonant tunneling review" (session_01DGmqintkoYzahfGQQzdXYL), from "Guinness cart:
JAX solver, fix and run". CPU only, nothing rerun. Kept current until item 1 is complete.

5. **Button: fixed and live** (main b6850421). At a ride's end Pause now reads "Play" (starts over), not a second "Ride
   again"; tested live at 390 and 1440 px.
2. **Lean two ways.** The run's own 5.78 mm is biased low: at θ = 0 and π its bilinear uses a glass-cut column 0.05 cell inside
   the wall, empty in 94–95 % of frames and filled with the frame's mean. pack_ride's 8.94 mm (trusted columns) is what the page
   shows; a first-mode fit on those columns gives 2q = 7.80 mm, the tilt 7.97 mm. No stored or published number changes.
4. **Rim points at R − Δx** (28 of 64): mode height ratio 0.9987; measured tilt changes 0.0–0.2 % (≤ 0.02 mm) on every ride.
   Nothing changes.
3. **~2 mm lean after the kerb: a reading artefact, not physical.** Last second: first-mode fit 0.12 mm (joint), 0.00 mm (slosh);
   front and back wall bands level to 0.01 mm; cart acceleration ≤ 0.04 mm; head shift 0.25 mm; books closed. The two-point lean
   reads local roughness (0.2–0.3 mm rms). New finding: on the kerb the mean stout surface rises 0.85–1.44 mm with no particle
   lost (the particle cloud spreads, about 1 % in volume); gentle roads ≤ 0.10 mm. Not yet measured whether it changes a spill.
1. **Numerical damping (in progress).** Run 6's no-head swing refits to ζ 0.0160 at 3.330 Hz; its energy books put only about a
   fifth of the loss after the push in the booked glass friction. CPU free swings (scratch, results discarded): inviscid at 6,
   4.5, 3 mm; dt 1 ms; plain PIC vs APIC; wall model. First result: inviscid at 6 mm gives ζ 0.078, so the method's loss grows
   strongly with grid size: a spatial cause (transfer or surface), not the rest guard (a check only, it never alters the
   state). Attribution and the effect on the played swings to follow here.

**Follow-up asked by the coordinating chat (11:38 UTC):**

- **Wording of the kerb limit.** The road pushes the wheel back with up to 82 N; at 1.5 m/s the motor gives at most 11.25 N
  (b = N Km / Rw = 5 N/A; back-EMF 5 × 1.5 = 7.5 V leaves (12 − 7.5)/2 Ω = 2.25 A). 15 N, at the 3 A limit, is only its absolute
  maximum. Corrected in 06-run8-state.md; the live note already says this.
- **Road preview's kerb lean 21.17 → 23.87 mm is run-to-run scatter, not β.** The preview law (speed PI plus the road
  feedforward, stout_jax.py Cart, ctrl 2) never uses the plant or β. Version 9 and run 10 ran the same law on the same road:
  their stored surfaces agree to 1.5e-5 mm up to 0.33 s and 3.9e-3 mm at 0.67 s, then part within two pictures at the jolt (0.14
  mm at 0.70 s, 4.4 mm at 0.73 s), with cart speed equal to 1.8e-5 m/s; the GPU's unordered sums differ in the last bit and the
  splash amplifies it. The tilt moved only 22.70 → 23.03 mm (+1.5 %), the head spilled 2.46 → 2.51 mL; the two-point lean, which
  reads single rough columns, moved 2.7 mm. So the kerb's two-point leans carry about ±2.7 mm (12 %) of run-to-run scatter,
  its tilts about ±0.3 mm and its spills about ±0.05 mL. The β-induced changes on the other kerb rides (lean 25.37 → 25.41,
  21.83 → 21.84 mm; spill 2.00 → 2.07, 1.65 → 1.63 mL) lie inside that scatter.
- **Bulking against the spill: no effect on the published spills.** Every kerb ride spills its head between 0.67 and 1.03 s.
  The stout's mean surface (trusted columns, from the first picture) is then 0.12 to 0.27 mm *lower*, not higher (joint −0.12 at
  0.67 s, −0.26 at 0.80 s; preview −0.27 at 1.00 s); it rises later, +0.4 to +0.5 mm at 2 s and +0.85 to +1.44 mm at 4 s, after
  the last lump left. Lowering the surface by the rise at each spill moment (head above the rim, column by column, H + h_f −
  147.5 mm) leaves every spill unchanged to 0.01 mL (2.07, 1.63, 2.51, 2.44 mL). Bound: the spill's sensitivity to the surface
  height, measured the same way, is about 26 %/mm (a surface 1.44 mm lower throughout would cut it by 36–39 %); the mean shift
  during the spills is at most 0.27 mm, so the published spills are good to ±0.2 mL from this cause, and the bulking that
  reaches 1.4 mm by the end comes too late to touch them.
- **Item 1 exponent withdrawn.** The Δx^1.45 used 0.0105 at 1.5 mm, inferred from a run with friction on. Scaling will be fitted
  to frictionless CPU points only (6, 4.5 and 3 mm) and extrapolated to 1.5 mm with an error bar.

Wrong published numbers found so far: none. Fix cost: none for items 2–4; item 1 pending.
