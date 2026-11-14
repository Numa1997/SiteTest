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

Wrong published numbers found so far: none. Fix cost: none for items 2–4; item 1 pending.
