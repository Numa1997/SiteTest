# Fig. 16 one-model spill: chat state (read this first after any compaction)

Branch `claude/guinness-one-model`, cut from `main` 12c2e3a on 20 Nov 2026. Kept current at every step that changes what is
live or what is left.

## Aim (the brief of 20 Nov 2026, condensed)
One solver for the pint of stout with its head on the four-wheel cart, kerb ride, control off, inside and outside the glass.
No stitching, no hand rules. Stored frames at 60 per second for the existing Fig. 16 player. Replaces the "derived spill" work.

- Stout: incompressible viscous liquid, parameters rho, nu, gamma.
- Head: same liquid as a jammed wet foam, density (1 - phi) rho, phi = 0.73, Herschel-Bulkley yield stress sigma_y
  (start 10 Pa, sweep 0 to 50 Pa).
- Solids: glass inside and outside, its foot, deck 310 x 124 mm at z = -30 mm; glued, fully wetted.
- Frame: stored cart motion of `kerb_off.npz` (Kaggle dataset fig16-guinness-cart-control), prescribed, impulse-exact at the
  kerb (differenced velocities, not the 60 Hz gx, gz samples).
- Must come out of the equations: splash falling back, film down the outer wall, landing splash, spreading, falling off.

## Solver choice (pending; documentation checked 20 Nov)
Documentation result (DualSPHysics repo, master, read 20 Nov):
- (a) GPU: the non-Newtonian multiphase code is a separate source tree `src_mphase/DSPH_v5.0_NNewtonian/source/` with CUDA
  kernels (`JSphGpu_NN_ker.cu`) and a `-gpu` option (`doc/help/DualSPHysics5.0_NNewtonian_Help.out:41`). No prebuilt
  binary: `bin/linux` holds only the v5.4 tools (`bin/linux/VERSION_INFO.txt`). Must be compiled; its Makefile defaults to
  CUDA 9.2 (`Makefile:59`). Phases: up to nine liquids, each with its own density, viscosity and yield stress
  (`doc/xml_format/_FmtXML_MphaseNNewtonian.xml:8-21`); no air phase. tau_yield is specific (Pa m3/kg), i.e. sigma_y / rho.
- (c) Surface tension: none in the non-Newtonian code (0 matches for tension/cohesion/CSF in the XML format and the GPU
  kernel). It exists only in the separate LiquidGas v4.0 code (example 06_SurfaceTension, `examples/Examples_mphase_liquidgas.pdf`),
  which is Newtonian water-air.
- (b) Kaggle install: not yet tested.
First choice DualSPHysics 5. Check (a) multiphase non-Newtonian on GPU, (b) installs on Kaggle, (c) surface tension.
If (a) or (b) fails: OpenFOAM multiphaseInterFoam (stout, head, air) on GitHub runners.

## DECISION 20 Nov (owner): no DualSPHysics. Own solver in JAX, tools/fig16/mpm/
MLS-MPM, APIC, explicit, float32. One material law, gas fraction phi per particle (fixed): density (1-phi) rho_l; stiff EOS,
sound speed c (start 50 m/s, >= 10 x max speed, report density error); Newtonian nu for phi < 0.64; head phi = 0.73
Herschel-Bulkley sigma_y (10 Pa, sweep 0-50), Papanastasiou-regularised (Yue et al. 2015 "Continuum Foam"); gamma not in v1
(count isolated particles every run). Solids by signed distance: glass inner+outer+foot, deck; unilateral grid boundary
(may leave, never enter), no-slip in contact. Thin wall (2.5 mm < 2 cells at 1.5 mm): side-tagged CPIC transfers (Hu et al.
2018). Frame: stout_jax.py frame_accel + impulse-exact b, om, al of tools/fig16/derived/flight_map.py (only reuse from the
old branch). Order: A (2-D planar, Kaggle CPU) tests 0-4; B (3-D GPU) smoke + tests 5-7; C kerb ride 4 s, checkpoints
0.1 s, books per picture; D frames 60/s, surface from particles, docs, merge and publish.
The DualSPHysics ladder below is superseded by this order (A.0 to C).

## Validation ladder (old, superseded)
1. Pint at rest 2 s: surface moves < 0.2 mm, nothing leaves.
2. First sloshing mode: omega^2 = g k tanh(k h), k = 1.841 / R, within 3 %.
3. Film on 2 degree incline: u = g sin(a) h^2 / (3 nu), within 5 %.
4. Viscous spreading: R = 0.894 (g V^3 t / 3 nu)^(1/8), R^8 slope within 10 %.
5. Head slab on tilt: holds while rho_f g h sin(a) < sigma_y, flows above.
6. Mass to 0.1 % every run; resolution halved once: spilled mass changes < 5 %.
Then the kerb ride. Known limit to report: deck film thinner than the particle size.

## Rules in force
- Every action needs the owner's yes, one step per turn (R11). Exception from the brief: when finished and tested, merge to
  main and publish without asking.
- Nothing computed in the container; Kaggle or GitHub runners only (R1). Smoke run before every full run. GPU: read quota,
  state cost in one line first. Every run: time estimate, live monitor (clock and elapsed), results to file per stage, outputs
  committed (R3, R12).
- No physics in the browser (R7). No renumbering (R6). Delete nothing (R9). Ideal deck, no contact angle (R13). Spill is a
  liquid, compared as fields (R14).
- May change: tools/fig16/sph/** (new), notes/spill/** (new files), docs/simulations/fig16-*.md, tools/inventory.py; at
  integration the Fig. 16 player, viewer scripts and page source.
- Never: Workers, R2, public/de/, public/ar/, scripts/i18n/, *.rtl.css, branch claude/guinness-realism, figure numbers;
  no assistant or model name in any commit; never the owner's name.
- Branch claude/guinness-open-problems: abandoned; do not build on it, merge it or delete it. History only:
  notes/HANDOFF-guinness-19-nov.md and notes/spill/DERIVATION-flight-inversion.md live there, not on main.
- Each turn: Fact (handle) / Inference / Opinion, metric units, ends with "Where we are:" and "Next, if you say yes:".

## Log
- 20 Nov: step 0 report given. Session "Fig. 16 derived spill: continue from handoff" (session_01DGmqiqE4iJRHF2gkZVo1Dv)
  archived on the owner's order.
- 20 Nov: branch created, this file written.
- 20 Nov: documentation check done (above). Superseded by the owner's MPM decision.
- 20 Nov: owner's MPM decision recorded. Plan for A.0 sent; waiting for yes.

## What is live
Unchanged: main 12c2e3a, Fig. 12 and Fig. 16 play stored Kaggle rides.

## What is left
Everything from the solver check onwards.
