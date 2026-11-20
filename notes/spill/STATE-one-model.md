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

### Additions 20 Nov (owner)
- phi_body for stout particles (start 0.03): density (1 - phi_body) rho_l.
- Head at walls: Navier slip, slip length l_s (start: free slip for head, no-slip for stout); test A.3 run both ways,
  difference reported.
- Stage E after the ride: surface tension gamma by continuum surface force on the grid. Test: drop of radius R at rest holds
  2 gamma / R within 10 % and stays round. Then the ride again with gamma on.
- Air drag: switch, off by default, quadratic in relative speed; not tuned now.
- Every parameter named in the docs with symbol, value, source or "assumed".

### Parameter table (keep current; copy into the docs)
| symbol | meaning | value | source |
|---|---|---|---|
| rho_l | liquid density | 1007 kg/m3 | run16.py:22 (Fig. 16 rides) |
| phi_body | gas fraction of the stout body | 0.03 | owner, assumed |
| phi_head | gas fraction of the head | 0.73 | stout_jax.py:57 (PHI_F = 0.27) |
| nu | stout kinematic viscosity | 2.06e-3/1007 m2/s | Benilov et al., arXiv 1205.5233 (stout_jax.py:33) |
| sigma_y | head yield stress | 10 Pa, sweep 0-50 | owner start; old model derived 5.4 Pa (stout_jax.py:66) |
| m | Papanastasiou regularisation time | 0.2 s | assumed (explicit viscous step limit) |
| K_hb, n_hb | head Herschel-Bulkley consistency, index | 5.0 Pa s^0.27, 0.27 | Yue et al. 2015 Table I, "pie" (275 kg/m3, nearest density); assumed for the head |
| c | sound speed of the stiff equation of state | 50 m/s | owner start |
| l_s | Navier slip length | stout 0, head infinite (free slip) | owner start |
| gamma | surface tension | 0 in v1; 0.0442 N/m in stage E | Voelp & Willenbacher 2021 (stout_jax.py:51) |
| C_d | air drag coefficient | switch off | not tuned |
| dx | grid spacing | 1.5 mm | owner |

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
- 20 Nov: owner's MPM decision recorded. Plan for A.0 sent.
- 20 Nov: owner's additions recorded (phi_body, Navier slip, stage E gamma, air-drag switch). Waiting for yes to write code.
- 20 Nov: owner's corrections: implicit wall friction v_t <- v_t/(1 + dt eta A/(m (l_s + d))); Laplace test with gravity off,
  R >= 8 cells, mean pressure inner half vs outside, noise reported, INCONCLUSIVE if noise > jump; A.0 control built to leak
  (liquid both sides, b_x = 5 m/s2 for 0.2 s). Yes to write mpm2d.py and a0_wall.py, run nothing.
- 20 Nov: Yue et al. 2015 read (PDF, cs.columbia.edu/~yonghao/tog15/yue-mpm-shear-dependent-flow.pdf): their law is
  ELASTO-viscoplastic (shear modulus mu, return map on b_e, implicit backward Euler; Table I: kappa 109 kPa, mu 0.08-50 kPa),
  not a Papanastasiou viscosity. Version 1 follows the owner's Papanastasiou form; flagged to the owner.
- 20 Nov: written tools/fig16/mpm/mpm2d.py, a0_wall.py (syntax parsed only; nothing run). Waiting for the owner's review.

## What is live
Unchanged: main 12c2e3a, Fig. 12 and Fig. 16 play stored Kaggle rides.

## What is left
Everything from the solver check onwards.
