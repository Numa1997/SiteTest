# Fig. 12 in JAX: what changed before run 3, and the checks it passed (13 November 2026, afternoon)

Written by the session "Guinness cart: JAX solver, fix and run". Overrides 03 and 04 where they differ.

## Inputs, checked against the research session's complete handover

The user pasted the research session's full file (all numbers, the grid-solver equations, every Wolfram output). Checked line by
line against `tools/fig12/kaggle/stout_jax.py`:

- Stout 1007 kg/m³, 2.06 mPa s; head 19 mm, R32 34 µm, liquid fraction 0.27 (272 kg/m³), γ 44.2 mN/m, E∞ 18.7 mN/m, Φc 0.635,
  G0 166.44 Pa, τy 5.415 Pa; Cantat Z 0.18 and l/r_m 0.004 (the liquid-fraction-0.25 values, held beyond 0.25); Stokes wall layer
  at 3.42 Hz; skin the same again. All as in the handover.
- One input was wrong: the head's flow law kept only the films term of Tcholakova et al. 2008. The handover (part B2) gives
  films and menisci: τ/(γ/R) = 0.7 Ca^0.47 Φ^(5/6)/(1−Φ)^0.5 + 8 Ca^0.7 Φ^(5/6)/(1−Φ)^0.15. At 10 1/s the two are 7.5 and 4.2 Pa;
  the code now gives 11.72 Pa against the handover's 11.816 Pa (wolfram/05). Fixed in `foam_flow_stress`, used by the sheet and
  by the wall cap.
- Not in the model, as before: the contact line's friction (×1.5–2.4 on the wall damping), the film left on the glass, drainage.

## The surface read-out: four tries, one kept

Rest check (`gate_rest.py`, 4 mm grid, 1 s at rest, this session's CPU), in order:

1. Count the particles in each column against the seeding lattice (commit 250fee8). Exact at t = 0 (0.000 mm everywhere), but by
   1 s columns were off by up to ±7.6 mm while the stout's kinetic energy was 6e-6 J (waves of about 0.5 mm): particles wander
   between columns by ±8 in a 4 mm column. Head kept.
2. Same, plus a step that spreads crowded particles (a Poisson solve for a displacement, once per frame). With the cell's share
   taken from the glass's volume it pulled stout to the wall: 11.6 mm, 6.8 mL of head lost. With the share from the lattice:
   5.5 mm, 0.21 mL lost. Including the wall cells changed nothing. Dropped.
3. Level set with radius 0.505 dx for both pressure and read-out: gaps at the glass, −13 to +7 mm there, 12 particles out of
   the glass, 2.2 mL of head lost. Dropped.
4. **Kept** (commit 49a77e1): the pressure step's level set at 0.9 dx (closes the gaps at the glass), the read-out from the same
   field with radius 0.505 dx (phr + 0.395 dx), read from the top down over a run of three stout cells. The radius is derived:
   for the seeding lattice (h = dx/2, hz ≈ dx/2) the kernel-weighted centroid lies 0.505 dx below the top, and the code's own
   read-out between cell centres then reads −0.09…+0.02 cell for every position of the top (0.9 dx reads +0.5…+1.0 cell).

   Result at 1 s: head 91.20 → 91.20 mL, 0.000 mL spilled; no stout left; kinetic energy 5.7e-6 J; surface within 1.72 mm
   (0.43 cell) everywhere inside, by radius: centre −0.95 mm mean, outer ring −0.28 mm mean, worst −2.96 mm at the glass.
   Fails the old 0.2-cell line; passes everything else.

Also changed: the seeding now ends exactly at the fill (layers every hz = fill / round(fill / h); before, 124 mm on a 4 mm grid).

## The guard in the GPU run

`run_b.py`: the first task is the pint at rest, 2 s at 1.5 mm. If any column inside the glass is more than 0.5 cell (0.75 mm)
from the fill, or the root mean square is above 0.25 cell, or any head or stout is lost, the session stops before any ride
("stop the run if it does not have proper numbers", the user). A list overflow (near-surface particles or drops) now stops a task
instead of warning. The whole script ran end to end on the CPU at 6 mm for two frames per task (rest, guard, two rides, free
swing, summary) before launch.
