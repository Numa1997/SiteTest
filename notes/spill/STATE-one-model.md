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

## Solver choice (pending)
First choice DualSPHysics 5. Check (a) multiphase non-Newtonian on GPU, (b) installs on Kaggle, (c) surface tension.
If (a) or (b) fails: OpenFOAM multiphaseInterFoam (stout, head, air) on GitHub runners.

## Validation ladder (pass marks fixed before each run)
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
- 20 Nov: branch created, this file written. Next: DualSPHysics 5 documentation check for (a) and (c).

## What is live
Unchanged: main 12c2e3a, Fig. 12 and Fig. 16 play stored Kaggle rides.

## What is left
Everything from the solver check onwards.
