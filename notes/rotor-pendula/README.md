# Rotor Pendula: the working record

What was built, from which scripts, and what is still open. The page itself is built from
`portfolios-src/rotor-pendula/` (see its README); this folder holds the models and the sources behind the numbers.

## The question
A second, lighter blade is hinged at the tip of a wind-turbine blade and turns in the rotor plane; a generator at the hinge
brakes it. How much power does it deliver, who pays for it, and can the wind's disorder (gusts, a bending and shaking blade)
give it more?

Until 24 October 2026 the study modelled a different machine, a point pendulum (0.1 kg on 0.2 m) at 30, 60 or 90 % of the
blade on six rotors, and a double pendulum. Numa asked for the second blade at the tip; the study is being rebuilt for it on the
branch `rotor-second-blade`. The earlier scripts are listed under "Being ported" until each is replaced or deleted.

## The setup (`derive/setup.py`)
- Turbine: NREL 5 MW reference (Jonkman et al. 2009): rotor radius 63 m, hub radius 1.5 m, peak C_p 0.482 at tip-speed
  ratio 7.55. Steady winds 6, 8, 10 m/s in region 2: Omega = 7.55 v / 63 m (6.9 to 11.4 rpm). `dossier-turbine.md`.
- The second blade: a thin uniform rod, l = 1 m (a modelling choice), m = 1 kg (`design.py`: the mass of the 1-2-5 series
  at which the maxon RE 25 + GP 32 C takes the largest share of P*, 36.8 %). I = m l^2/3, first moment m l/2.
  Hinge at r_p = 63 m. Air on the second blade is left out (the hinge moves at 45 to 76 m/s).
- Generator: maxon RE 25 + GP 32 C, ratios 3.7 to 492 (`dossier-generator.md`). Sensor need 37.6 uW (`sensor.py`,
  `dossier-sensor.md`).

## Decisions for Numa
- (a) How to size the second blade. Default in use: by the generator (1 kg on 1 m). Options: by the sensor (0.1 kg on 1 m),
  or a real-size tip blade (3 m, 10 kg) with a larger generator (needs a new primary source).

## Models, by layer (`derive/`)
| Layer | What it adds | Scripts | Output |
|---|---|---|---|
| L0 | the second blade derived twice; small swings, best brake, P* = m g^2 l / [8 Omega (r_p - 2l/3)] | `blade.py` | |
| L1 | full nonlinear motion, Radau IIA engine (`engine.RigidBlade`), chaos | `engine.py`, `L1_blade.py`, `L1_chaos_blade.py` | `L1_blade.json`, `L1_chaos_blade.json` |
| L2 | gusts on the NREL 5 MW turbine with its controller | `L2_run.py`, `L2_scales.py`, `turbulence.py` | `L2_run_nrel.json`, `L2_run_k2.json`, `L2_scales.json` |
| L3 | the blade sags and shakes at the tip; the shaking ceiling | `L3_sag.py`, `L3_sag_tip.py`, `L3_shake2.py`, `power_theorem.py`, `nrel5mw.py` | `L3_sag_tip.json`, `L3_shake2.json` |
| L4 | real geared generator: losses, friction, reflected inertia | `L4_generator.py`, `L4_full.py`, `L4_check.py`, `L4_converge.py`, `design.py` | `L4_*.json`, `design.json` |

Every script prints PASS/FAIL lines and exits 1 on a failure. A check tests the numerics or a derived prediction; a physical
outcome (regular or chaotic, a gain or a loss) is printed as a result, never as a pass. Outputs are copied into
`portfolios-src/rotor-pendula/data/`, and `tools/make_numbers.py` turns them into every number on the page.

## Results (second blade, 1 kg on 1 m)
- Best power at the best brake: 268, 201 and 161 mW at 6, 8 and 10 m/s by (2.5); the full equation gives 267, 201 and 161 mW
  (within 0.31 %). The rotor pays every joule: the trail identity holds to 1e-12 in all nine runs.
- Chaos (`L1_chaos_blade.py`, 3 winds x 3 brakes x 8 starts): every exponent negative, every start ends on one regular swing;
  each exponent equals the decay rate of the braked centrifugal spring, 2 pi max Re s with s^2 + kappa s + R = 0, within 1.2 %.
- Through the RE 25 + GP 32 C (ratio 492), full equation: 106, 75.5 and 57.2 mW to the load (formula 104, 74, 56); 35 to 39 %
  of what the rotor pays reaches the load, 40 % (1 - eta) stays in the gears, 14 to 15 % is friction.
- Gusts (IEC class A, 8 m/s, NREL controller): -1.99 % (mean speed +2.60 %, which alone gives -2.55 %; wander +0.53 %); with
  the k Omega^2 law: +0.77 %.
- Sag at the tip: 431 to 467 mm; +17 to +18 % in the drive, but the tip section's turn takes most of it back: net +2.2 to +3.5 %.
- White-noise shaking: a rod draws at most (S/2)(3/4)m, three quarters of a point mass's ceiling.

## Queue
1. Pull request #43: Numa's "merge"; then the joint push with the Fig. 11 session.

The Newton question (closed, 24 October 2026). `L4_check.py` at 2000 steps per turn stops Newton at its cap of 12 in 1939
of 240000 steps (its log says FAIL). `portfolios-src/rotor-pendula/tools/check_newton.js` reran the 16 settings on the
page's own engine in Node (5 minutes; Python needed 41 minutes for one pass): it reproduces the Python run to 1e-14; with
the cap at 40 no step of the measured turns stays unconverged (17 in the start-up turns do); the cap of 12 changes the powers
by at most 8e-12; 4000 steps per turn and a band of 3e-4 change them by at most 2.7e-4. The results stand.

Done (24 October 2026): every model run for the second blade; `make_numbers.py`, `typed_numbers.py`, `check_numbers.py` (PASS),
`check_physics.py`; the notes, chapters 0 to 8; the simulation page's physics text and six worked solutions
(`tools/sim_solutions.js`); `check_sim.js`, `check_sim_browser.js` and `check_combined.py` at 360 to 1440 px (all pass); the
Portfolios entry and its German and Arabic translations.

## Sources (`dossier-*.md`)
`dossier-turbine.md` (NREL 5 MW, OpenFAST blade file), `dossier-generator.md` (maxon catalogue),
`dossier-edgewise.md` (blade edgewise mode), `dossier-harvesting.md`, `dossier-sensor.md` (ADXL362 Rev. D, CC2652R SWRS207J).

## Open
- Air on the second blade (lift and drag at 45 to 76 m/s): the next model.
- Bench test of the gear drag and the back-driven efficiency.
- Converting the low, slow load voltage into a supply.
