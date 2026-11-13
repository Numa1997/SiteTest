# Fig. 12 in JAX: the physical model as coded on 13 November 2026, what is checked and what is not

The code: `tools/fig12/kaggle/stout_jax.py` at commit `80f4700` (later commits change no physics). Numbers: `notes/fig12/research/data-for-solver.md`.
Status words: **run** = executed on Kaggle and its result read; **linted only** = never executed anywhere.

## 1. The stout (run, twice)

Incompressible Navier–Stokes with a free surface, in the glass's frame (every particle feels gravity minus the glass's acceleration).
- Particles (8 per cell) carry the stout; a staggered grid of 1.5 mm carries pressure (APIC transfer both ways).
- The curved glass enters through the open fraction of each cell face.
- Pressure: preconditioned conjugate gradients, tolerance 1e-5, up to 600 iterations (105 to 203 used per step).
- Free surface: a level set built from the particles; pressure set on the surface itself (ghost fluid).
- Viscosity 2.05e-6 m²/s, explicit.
- Glass boundary layer (0.44 mm, below the grid): a drag rate sqrt(nu omega / 2) per wall area.

Measured on Kaggle: 3.33–3.34 Hz against 3.42 Hz expected (2.5 % low). **The method itself loses a damping ratio of about 0.020 at 1.5 mm**
(0.023 at 2 mm, 0.049 at 3 mm) with no friction at all: four times the real wall damping of 0.0055. Not fixed. With the head on
this matters less (the head should dominate), but for bare stout it is too lossy. Ideas not tried: FLIP/APIC blend, more particles
near the surface, a tighter pressure tolerance, float64 sums.

## 2. The surface that cannot stretch (run once, effect not separated)

Beer's surface carries a protein skin (dilatational elasticity 18.7 mN/m for Guinness). Under the head, and on bare stout, the
surface cannot stretch, so it acts as a lid without slip: a second boundary layer. Coded as the same drag rate on the horizontal
velocity of the top liquid cells. Expected: damping ratio +0.0051. Not measured separately.

## 3. The head (linted only in its present form)

What it is: a wet foam of the stout's own bubbles. Inputs: Sauter radius 34 µm, liquid fraction 0.27 (derived, not measured),
surface tension 44.2 mN/m, surface elasticity 18.7 mN/m, thickness 19 mm. From these: density 272 kg/m³, yield stress 5.4 Pa,
modulus 166 Pa (not used yet).

State: one thickness h_f per column of the grid (57 × 57). Coded behaviour:
1. **Weight.** It presses on the stout's surface with rho_f h_f |g_eff| (set in the pressure solve and in the projection).
2. **Shear resistance (`head_sheet`).** The head rides on the stout, so each column of head moves up and down with the stout
   under it. Neighbouring columns moving at different speeds shear the head between them; it resists with its yield stress plus
   its viscous stress (Herschel–Bulkley, Tcholakova 2008 eq. 54, films term). Picture: a thick layer of whipped cream on a cup
   of coffee; tilt the cup and the cream holds the coffee's surface flat until the push exceeds what the cream can carry.
   Solved implicitly on the columns each step; the change goes onto the top two cells of stout; the pressure solve passes it down.
3. **Friction on the glass.** At the wall the head's edge rubs with Cantat's law, capped by what the foam itself can carry,
   over the height the head actually slides (about 9.9 mm of the 19 mm).
4. **Spill.** Where the head's top stands above the rim at the wall, the part above the rim breaks off once its weight and outward
   push exceed its yield stress, and flies as a lump. Lumps and drops that come down on the cart's body stay there.

Not in the model (say so on the page):
- The head does not flow sideways across the surface; its thickness changes only by spilling.
- No film left on the glass (lacing): the film thickness is derived (6.5–140 µm) but not coded.
- No drainage or collapse: about 0.6 mm in a 20 s ride.
- No bubbles in the stout: a settled pint has under 0.1 % gas.
- The contact line's own friction (measured to add ×1.5–2.4 to wall damping for water) is not coded.
- Drops are single particles in free flight; they do not merge, break, or wet the glass.

## 4. The cart (run)

A port of `Cart` in `public/scripts/stout-cart.js`: one wheel, tyre spring, suspension spring and damper, DC motor with a speed
loop (PI), in float64, sub-stepped at 0.1 ms. The stout pushes back with minus the rate of change of its momentum; the head's mass
rides with the glass. Checked in run 2: impulse and momentum balance to seven decimal places.

## 5. What the two runs showed

- Run 1 (version 1, water, no head): speed and numerical damping measured. No use for the page.
- Run 2 (version 2, full model with the faults listed in `01-mistakes-and-rules.md`): the stout does spill over the back rim on
  five 20 mm bumps at 1.0 m/s (9.04 g). The drawing code works on real data. No use for the page.

Pictures: `run2-frame000.png`, `run2-frame058.png` (the new drawing on run 2's faulty data), `live-page-head-spikes.png`
(the live page's fault, seen at 01:45 UTC).

## 6. What the next run must answer

1. Does the pint at rest stay flat to 0.3 mm with the head on, and lose no head? (Gate E)
2. Does the free swing now die within about a period, as Gate C predicts and as Sauret reported for a carried Guinness?
3. With the head resisting, do the 20 mm bumps still spill, or does it take the sharp 30 mm bump at 1.5 m/s?
   The user wants real spillage: the roads for the data runs are chosen from this answer.
4. The time per step with the larger lists, for the data budget.
