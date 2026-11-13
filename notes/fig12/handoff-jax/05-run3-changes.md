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

## Run 3 (notebook version 3, commit eb7471f): the guard stopped it, and why

The pint at rest, 2 s at 1.5 mm on the T4: no stout and no head lost, but the surface was 4.62 mm off at worst (limit 0.75 mm)
and 0.484 mm root mean square (limit 0.375 mm). About 100 columns read low by 1-3 cells, none high, first at the glass, then
spreading inward in blocks of 2-4 columns. The session stopped before any ride (74 ms a step, about 260 s of quota).

The read-out was not the cause. The stout was moving. Energy books of the pint at rest (`rest.npz`, run 3):

| t | potential energy lost | kinetic energy | "dissipated" by the glass, skin and head |
|---|---|---|---|
| 0.1 s | 2.4 uJ | 0.32 uJ | 57.5 uJ |
| 1.0 s | 235 uJ | 1.69 uJ | 405.5 uJ |
| 2.0 s | 629 uJ | 2.99 uJ | 773.7 uJ |

A pint at rest has nothing to dissipate. Two faults, both found by one step from rest at 4 mm (`step1.py`, scratch):

1. **The head lay only on columns whose centre is inside the glass.** The columns at the glass whose centre is outside but
   which hold stout got no head, so the head's weight, rho_f g h_f = 272 x 9.81 x 0.019 = 51 Pa, pressed the inner columns and
   not these. The stout was squeezed up into them: after one step from rest the fastest stout moved at 10.9 mm/s with the head
   and 0.61 mm/s without it (models "full" and "wall"/"inviscid"). Particles per column at 0.1 s confirmed it: the columns at
   the glass lost 7-9 particles each (1.3-1.7 mm of stout). Fix: the head lies on every column whose horizontal face at the
   fill is open (`afill`, from the glass's face fractions), and every head volume (start, spill, lumps, the cart's load)
   counts hf x afill x dx^2. Head: 91.31 mL against pi R_fill^2 x 19 mm = 91.25 mL. One step from rest: 0.61 mm/s, the same
   as without the head.
2. **The thin layers braked gravity.** The glass's Stokes layer, the skin and the head acted on the face velocities after
   gravity's kick of the step (dt g, about 20 mm/s at dt = 2 ms) had been added; the pressure step then cancels that kick
   everywhere except where it had been braked, which acts as a spurious push. The stresses now act on the velocity the stout
   has, and the body force is added after them, just before the pressure step.

4 mm, 1 s at rest, CPU, before and after both fixes: "dissipated" 233 -> 9.5 uJ, kinetic energy 2.6 -> 0.75 uJ, surface worst
1.63 -> 0.97 mm (0.24 cell), root mean square 0.82 -> 0.43 mm (0.11 cell); nothing spilled. What remains (0.6 mm/s in the
first step at the corner of the surface and the glass, and a slow mean drop of the read surface, -0.35 mm at 1 s) is the
method's own: it is the same with no friction and no head.

Also changed for run 4 (commits 183347c, 490b55d): the surface read-out takes the body from the 0.9 dx field and the surface
from the 0.505 dx field in the top three cells of that body (a column where the 0.505 dx field finds no surface there falls
back to the body's top less 0.68 cell, and is counted per frame as `nfallback`); the rest task stores the particles at 0.5 s
and 2 s (`rest_particles_15.npz`, `rest_particles_60.npz`) so any read-out can be checked afterwards.

## Runs 4, 5 and 6 (13 November 2026, evening)

- **Run 4** (version 4, commit 490b55d). Rest guard passed (0.54 mm, rms 0.125 mm). All rides ran. Free swing with the head:
  rings at 2.900 Hz, decays in 0.104 s, natural frequency 3.277 +- 0.034 Hz, damping ratio 0.465 (the summary's "0.526" was
  1/(tau w_d); `fit_swing` now reports f, f0 and zeta = 1/(tau w0)). Gate C predicted that the head stops the swing within about
  one period, and research/verification.md check 3 that a sliding Guinness head arrests a free slosh within about one period.
  Not stored, for one fault seen in the pictures: 84 "drops" along the glass in the pint at rest. Columns whose centre is outside
  the glass at the fill but inside lower down (the tulip is widest at 116 mm, 39.3 mm) read their surface at 120 mm, where their
  centre leaves the glass, and their stout above that as drops. Fix (commit 4c10527): such a column has no surface value, and a
  drop must stand 1.5 dx above its column and the eight around it. At the start: 0 drops, every column within 0.25 mm.
- **Run 5** (version 5): computed nothing. The budget guessed 1340 s for the free swing without the head (no rate measured yet
  in that session) against 900 s allowed, and skipped it. About 1 minute of quota.
- **Run 6** (version 6, commit 4c10527): stored on the page. Every check of `check_run.py` passed. Rest 0.54 mm, rms 0.125 mm,
  books 24.5 uJ lost, 0.33 uJ kinetic, 8.4 uJ dissipated. Free swing without the head: 3.331 Hz (-2.6 %), zeta 0.0160 against
  0.0055 from the glass and viscosity, so the method adds about 0.0105. With the head: 3.278 Hz natural, zeta 0.47. Rides: five
  bumps lean 9.8 mm, no spill; kerb lean 19.7 mm, 4.08 mL of head from 0.67 s, 0.008 g of stout from 1.00 s; 25 mm bump 6.9 mm.
  1373 s on the T4.

Gate E's swing check now reads the natural frequency of the swing without the head (3 % of 3.421 Hz). With the head the model
gives weight but no inertia, so its natural frequency is the bare stout's; a real head's mass would lower it to about 3.07 Hz
(the note, section 11). That, and the method's own loss (0.0105, twice the glass's), are the next model's work.
