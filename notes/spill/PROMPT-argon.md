# Brief: a pint of Guinness on a cart, with the spill computed as one continuous liquid

Written 19 November 2026 by the session that holds the work (session_01DGmqipAnEdVvBLCf7CLGmT), at the owner's request, for an
independent physicist and numerical analyst. It says everything that exists, every number measured, and where the work so far is weak.
Read it whole. Repository: github.com/Numa1997/SiteTest, branch `claude/guinness-open-problems` (same as `main` for these files,
except commits after 12c2e3a1, which are on the branch only).

## 1. The goal, in the owner's words and in physics

The site Phyein Usul (phyeinusul.com) shows lecture-note figures built on stored, precomputed simulations. Fig. 12 and Fig. 16 carry
a full pint of Guinness (stout with its head of foam) on a cart over a road with a kerb. The owner wants:
- the spillage **computed**, not drawn: the stout that leaves the glass must stay a liquid (one model, no switch of equations at the
  rim), run down the outside of the glass, land on the cart, spread, and fall off its edge;
- "no discontinuities in the model": the same equations inside and outside the glass;
- the physical conditions accounted for: the air (headwind drag, splash), surface tension, wetting, the head of foam;
- everything computed on Kaggle (owner's account; GPU: NVIDIA T4, 16 GB, float64 at 1/32 speed); nothing computed in a reader's
  browser; the page only plays stored frames.

Physically: incompressible Navier-Stokes with a free surface, in the non-inertial frame of a glass that translates and (Fig. 16) pitches,
inside a measured tulip pint glass, with a deformable head of foam lying on the stout, coupled both ways to a cart whose dynamics and
controller are given.

## 2. What exists and works (stored rides, the "old model")

`tools/fig12/kaggle/stout_jax.py` (about 1300 lines, JAX). Header comment, verbatim in substance:
- APIC particles (Jiang et al. 2015) on a staggered MAC grid; the curved glass by open fractions of every cell face (Batty, Bertails &
  Bridson 2007); pressure by preconditioned conjugate gradients (divergence-free velocity); free surface as a level set built from the
  particles (Zhu & Bridson 2005, kernel 2 dx, radius 0.9 dx, with mirror images in the glass wall); p = 0 on the surface by the
  ghost-fluid rule (Enright, Nguyen, Gibou & Fedkiw 2003); closed faces take the liquid's velocity by extrapolation (free slip on the
  grid); a Stokes layer (0.44 mm, below the grid) brakes the liquid at the wall at rate sqrt(nu omega / 2) per unit wall area;
  viscosity nu explicit on the grid. Computed in the glass's frame (gravity minus the glass's acceleration; Fig. 16 adds the rotating
  frame's forces, `frame_accel`).
- The head: a sheet of thickness h_f on each column of the cavity, liquid fraction PHI_F = 0.27, its weight and mass on the stout
  (run 8 model). Its spill over the rim becomes ballistic "lumps" (`head_spill`).
- Over the rim (old model): a particle outside the glass's radius stops being fluid and flies ballistically (a discontinuity). Drops
  that land are frozen.
- Grid 1.5 mm, ~420 000 particles at ppc 2, cells about 57 x 57 x 113 = 0.37 M. Float32 fluid, float64 sums and cart.
- Constants: NU_STOUT = 2.06e-3/1007 m^2/s (Guinness at 6 C), rho 1007 kg/m^3, GAMMA = 0.0442 N/m (degassed Guinness, 20 C),
  HEAD0 = 19 mm, OMEGA = 2 pi 3.42 rad/s (first sloshing mode), PHI_F = 0.27.
- Measured numerical damping: zeta 0.0152 at 1.5 mm, 0.0090 at 1.0 mm; real stout ~0.0055 (`notes/guinness-rebuild/audit.md`, F).
- Carts: Fig. 12 `stout_jax.Cart` (one wheel); Fig. 16 `tools/fig16/kaggle/cart4.py` (four wheels, deck 310 x 124 mm, pitch, actuators,
  LQR + Kalman, `run16.py` drives it; `make_advance16`).
- Stored results (public/data/fig16/2026-11-14 and -15, public/data/fig12/2026-11-14-run10): Fig. 16 kerb control off spills 75.6 g
  stout + 14.4 mL head in 4 s; five bumps off 77.2 g + 14.6 mL; one bump off 39.6 g + 11.2 mL; kerb control on 0.039 mL head only.
  GPU time: Fig. 12 ~45 s of T4 per simulated second; Fig. 16 run 5 ~153 s per simulated second.

## 3. The continuous model (new, branch code, not used by any stored ride)

Switched on by `Geometry(R, dzp, fill, dx, body=(hx, hy, z_top))`; with `body=None` the old model is bit-for-bit unchanged.
- The grid covers the cart's body/deck around the glass (rectangular nx x ny since 19 Nov; Fig. 16 deck 0.155 x 0.062 m half-sizes,
  top at z = -0.030 m below the glass's inner floor; Fig. 12 body 0.11 x 0.06, top -0.014) up to 30 mm above the rim.
- Solids: glass wall from R(z) to R(max(z, 8 mm)) + 2.5 mm for 0 < z < rim; foot r < R_out for z_top < z <= 0; body below z_top.
- Face open fractions from 4 x 4 samples of "not solid"; face rule (latest, 6aab9eb0): below the rim every cell is assigned to the
  cavity's side or the outside by the majority of its open 2 x 2 x 2 sub-samples; faces between different sides are closed; above the
  rim nothing is closed.
- Level set built in `lsdom`: inside the cavity the old rule (cells half a cell from the inner wall), every open cell elsewhere; mirror
  images only for particles inside the cavity.
- Surface tension (`tension`): Young-Laplace jump p = gamma kappa, kappa = div(grad phi / |grad phi|) by central differences of the
  particle level set, clipped to |kappa| <= 2/dx, applied as the ghost-fluid surface pressure where no head lies and |phi| < 2 dx.
- Air drag (`air_drag`): headwind = minus the glass's velocity; Schiller-Naumann C_D(Re); local size d = 4/|kappa| in [dx, 10 mm];
  force through a one-sided smoothed surface delta on liquid outside the cavity.
- Particles (`_g2p_cont`): no free flight; contact with glass/foot/body puts a particle back on its side (inside: to the floor and to
  R(z) - dx/10; outside: to R_out + dx/10; above: onto the rim) and removes the normal velocity; leaving the grid = fallen off the cart.
- Head: still the old sheet on the cavity's columns (restricted to the glass's columns since 40be8553); its spill still ballistic lumps.
  This is still a discontinuity. Not designed.
- Fig. 16 wiring: `run16.py` with CONT=1 (deck solid, headwind (-v, -vzc) without rotating it into the pitched glass axes, books counting
  stout on the deck as on the cart), DX and END settings.

## 4. Every test and its numbers (all on Kaggle)

| test (notebook, version) | commit | grid | result |
|---|---|---|---|
| continuous-spill-smoke-2mm-b v1 | 6a41be3 (square grid, Fig. 12 body, model "wall", no head) | 2 mm | pint at rest 0.5 s: surface 125.01 mm, 0 lost; shove: books exact |
| continuous-spill-drag v1 | 036b81d | 2 mm | drag 0.0805 vs law 0.1197 m/s^2: FAIL |
| continuous-spill-drag v2 | 06bd5ed (one-sided delta) | 2 mm | 0.1063 vs 0.1197 m/s^2 (-11 %): PASS (gate 25 %) |
| continuous-spill-fig16-gpu v1 | 4da114de | 6 mm | "surface list full" after 2 frames; surface 124.8 -> 120.2 mm (grid too coarse) |
| v2, v3 | 37a39b7c, 40be8553 | 2 mm | Fig. 16 deck, model "full": pint at rest sank 125.0 -> 115.6 mm in 0.3 s; guard stopped |
| v4 (rest_variants.py) | c7847905 (face rule cc51c2c) | 2 mm, 0.3 s | A F12 body wall 112.3 mm; B F12 full 112.3; C deck wall 111.1; D deck full 110.7; E old model 125.0; 100-560 particles left the cavity |
| v5 | 6aab9eb0 (one side per cell) | 2 mm, 0.3 s | A 124.78, B 124.69, C 124.77, D 124.80 mm (ranges 124.4-125.0), 0 lost, 0 outside; E 125.00; mean particle height 72.74 -> 72.4-72.5 mm |
| v6 (run16 CONT=1) | 6aab9eb0 | 2 mm | rest guard PASS (max 0.34 mm, rms 0.22 mm in 0.3 s); kerb_off 0.3 s ran, 86.5 ms/step |
| v7 (run16 CONT=1 full) | 6aab9eb0 | 1.5 mm | rest 2 s: max 6.2 mm, rms 5.2 mm off level: guard FAIL (limit 0.75 / 0.375 mm); 350 ms/step; no ride computed |
| v8 (rest_variants D, F no tension, E) | 7d29ec55 | 1.5 mm, 1 s | RUNNING at the time of writing: is surface tension what settles the pint? |

So: the new model holds a pint at rest for 0.3 s to 0.2-0.3 mm, but drifts several millimetres over 2 s at 1.5 mm, while the old
model holds exactly. The cause is not found.

## 5. My holes and shortcomings (the owner's verdict: bad physics, no intuition; these are the specific failures)

1. I tried to fix the look of the spill by drawing tricks (merging drops into blobs) before the physics; it fixed nothing.
2. I diagnose by trial runs on the GPU instead of analysis: four GPU runs to find two bugs a careful reading should have found.
3. I merged another session's untested commit (cc51c2c, face rule) and it broke hydrostatics; I did not test before merging.
4. I estimated GPU cost on the wrong deck size (square grid on 310 mm) and had to correct it.
5. I ran a 6 mm check that could never pass (the pint is a few cells across); a waste.
6. Surface tension is applied explicitly as a ghost-fluid jump with curvature from a noisy particle level set, clipped at 2/dx. This is
   the classic set-up for parasitic currents; I did not use a balanced-force formulation (Francois et al. 2006; Popinet 2009, 2018),
   height functions, or a curvature estimate with known error, and did not check the capillary time step dt < sqrt(rho dx^3/(2 pi
   gamma)) (3.5 ms at 1.5 mm; the solver steps at <= 2 ms) beyond noting it. At the wall the contact angle is not modelled at all; the
   contact line is free slip with a clipped curvature, which is not physics.
7. Volume conservation: APIC with a particle level set does not conserve the liquid's volume by itself; the old model has an optional
   volume correction (vol_corr, off in stored rides). The new model's slow settling may be volume loss through the level set / pressure
   coupling at cut cells, not surface tension. I have not measured the liquid's volume (from the level set) over time, only the surface
   height and the particles' mean height.
8. The face rule "one side per cell by majority" is an ad hoc fix; cut cells straddling a wall thinner than two cells really hold two
   disconnected fluids, which one pressure per cell cannot represent. A correct treatment (thicker wall in the grid, finer grid near the
   wall, or a cut-cell method that splits cells) was not considered properly.
9. The contact rule moves particles out of solids and removes their normal velocity: not momentum-conserving, no restitution, no
   wetting. A drop landing on the deck has no splash model (Riboux & Gordillo 2014 noted, not coded), no contact angle, no spreading law.
10. The head of foam: still a sheet with ballistic lumps; its rheology (yield stress, drainage) is not modelled; its spill is still a
    discontinuity.
11. The wind ignores the deck's pitch; drag only outside the cavity.
12. Dissolved nitrogen and CO2, the stout's temperature dependence (surface tension measured at 20 C, stout served at 6 C): not used.
13. No convergence study of the continuous model in dx; no analytic benchmarks for it (static drop / Laplace pressure, capillary wave
    dispersion, dam break, sloshing frequency with the new walls).

## 6. What is asked of you

1. Find, by analysis, why the continuous model's pint at rest drifts (section 4) and give the correct formulation. Show the math.
2. Give a sound, implementable formulation for: the glass wall thinner than two cells; surface tension without parasitic currents,
   with a contact angle on glass and deck; the liquid landing on and spreading over the deck, and falling off its edge; the head of foam
   as a continuum on and with the stout (no ballistic lumps); air drag on liquid outside the glass; splash only where the published
   criteria say it happens.
3. For each: the equations, the discretisation on this staggered APIC grid, the stability limits, the analytic checks that prove it
   (with expected numbers), and the cost on a T4 for a 4 s ride at 1.5 mm (deck grid about 213 x 89 x 151 = 2.9 M cells).
4. Say plainly where this approach (APIC + level set at 1.5 mm) cannot reach the owner's goal, and what would.

## 7. Where everything is

- Solver: `tools/fig12/kaggle/stout_jax.py` (Geometry, Stout, tension, air_drag, _g2p_cont, pressure, level_set, surface, observe).
- Fig. 16 runner: `tools/fig16/kaggle/run16.py`, cart `tools/fig16/kaggle/cart4.py`, packer `tools/fig16/kaggle/pack16.py`.
- Fig. 12 runner: `tools/fig12/kaggle/run_b.py`.
- Tests: `tools/spill/smoke_cpu.py`, `rest_diag.py`, `drag_check.py`, `rest_variants.py`.
- History: `notes/spill/STATE.md`, `notes/spill/HANDOFF.md`, `notes/guinness-merge/LOG-18-nov.md`, `notes/guinness-rebuild/audit.md`.
- Glass profile: `public/scripts/guinness-glass.js` (R every 0.5 mm, from `tools/fig12/glass_profile.py`).
- Docs: `docs/simulations/fig16-guinness-cart-control.md`, `docs/simulations/fig12-beer-slosh.md`, `docs/kaggle-pipeline.md`.
- Kaggle notebooks (owner's account): continuous-spill-fig16-gpu (versions 1-8), continuous-spill-drag, continuous-spill-smoke*,
  fig-16-guinness-cart-with-control, guinness-on-a-cart-stout-in-jax. Kaggle dataset: numakoudsie/fig16-guinness-cart-control.

## 8. The owner's rules

Every computation on Kaggle (CPU free; GPU: state the cost first); no physics in the browser; stored frames only on the page; metric
units; derive, never assert; checks with numbers; short plain reports; never write the owner's name.
