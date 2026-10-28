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

## Sizing (decided 24 October 2026; was decision (a))
The study keeps 1 kg on 1 m, now shown against the range of real tip devices (`derive/sizes.py`, notes section 7.6, Table 5):
lengths 0.5 to 3 m (retrofit tip extensions, about 3 m with 1 m past the old tip, Vestas US 10 927 809; pivoting tip brakes
5-20 % of the radius, US 8 403 641) and 1, 3, 10, 30 kg/m (the NREL blade is 10.3 kg/m at its tip, 115 kg in its outer 3 m).
Over that range P* at 6 m/s runs from 66.7 mW to 74 W, in proportion to m l/2; the swing stays 0.214-0.220 rad (it is
g/(Omega^2 r_p)/sqrt 2 for any short blade); tau* runs from 0.87 to 936 N m, so the RE 25 + GP 32 C levels off at 94-107 mW
(6 m/s) above about 0.5 kg m; the heaviest add 8.3 kN at the tip (the blade's own outer 3 m: 10.1 kN). The sensor never
limits (worst case 311 x its need). So the size is set by the generator and the structure: 1 kg on 1 m is the lightest the
catalogue generator serves fully.

## Models, by layer (`derive/`)
| Layer | What it adds | Scripts | Output |
|---|---|---|---|
| L0 | the second blade derived twice; small swings, best brake, P* = m g^2 l / [8 Omega (r_p - 2l/3)] | `blade.py` | |
| L1 | full nonlinear motion, Radau IIA engine (`engine.RigidBlade`), chaos | `engine.py`, `L1_blade.py`, `L1_chaos_blade.py` | `L1_blade.json`, `L1_chaos_blade.json` |
| L2 | gusts on the NREL 5 MW turbine with its controller | `L2_run.py`, `L2_scales.py`, `turbulence.py` | `L2_run_nrel.json`, `L2_run_k2.json`, `L2_scales.json` |
| L3 | the blade sags and shakes at the tip; the shaking ceiling | `L3_sag.py`, `L3_sag_tip.py`, `L3_shake2.py`, `power_theorem.py`, `nrel5mw.py` | `L3_sag_tip.json`, `L3_shake2.json` |
| L4 | real geared generator: losses, friction, reflected inertia; sizes | `L4_generator.py`, `L4_full.py`, `L4_check.py`, `L4_converge.py`, `design.py`, `sizes.py` | `L4_*.json`, `design.json`, `sizes.json` |
| L5 | the air on the second blade, three shapes | `L5_air.py` | `L5_air.json` |
| L6 | a turbulent wind field over the disc (IEC Kaimal spectra, IEC coherence for u, TurbSim's smooth-model default for v and w, Veers synthesis with a seeded generator the Wind tab copies), checked against its own statistics and L2's disc averaging; the rotor and the second blade solved in it with the air at its middle; reference record for `tools/check_wind.js` | `L6_wind.py` | `L6_wind.json`, `L6_wind_ref.json` |
| L0' | the double pendulum of chapter 1: the site's Fig. 2 engine free (Lyapunov 1.44 /s over 3000 s), the first arm held (chaotic starts against Gamma for equal arms and for the 1 m rod at 63 m, braked and unbraked), the reduction's energy check, once-per-turn snapshots (Poincaré sections) of equal arms and of the rod at 6 m/s with the chaotic band's edges predicted (adiabatic invariant, separatrix action) and measured | `portfolios-src/rotor-pendula/tools/double_pendulum.js` (Node) | `portfolios-src/rotor-pendula/data/L0_double.json` |

Every script prints PASS/FAIL lines and exits 1 on a failure. A check tests the numerics or a derived prediction; a physical
outcome (regular or chaotic, a gain or a loss) is printed as a result, never as a pass. Outputs are copied into
`portfolios-src/rotor-pendula/data/`, and `tools/make_numbers.py` turns them into every number on the page.

## The notes as one story (28 October 2026)
The lecture notes were reordered and rewritten as one text with the double pendulum as its spine: Part I (chapters 1–5: the
double pendulum held by the wind, the turning frame, the brake, big swings and the bill, the generator), Part II (chapters 6–8:
the wind, including the turbulent field of L6, the air, the blade's sag and vibration and the shaking ceiling), Part III
(chapter 9). Equation numbers changed; the simulation page's references were renumbered with them. An independent derivation
check (SymPy) confirmed (1.1)–(1.8), the Euler torque, (2.3), (4.1)–(4.4) and (6.5)–(6.9) and found three faults, fixed: the
spectrum of (6.8) is scaled to the kept band (72 % of the Kaimal variance at 8 m/s lies in 1/256–1 Hz), the Kaimal knee is at
U/(6L), and the shaft torque in section 4.2 carries the first arm's weight too.

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
- Double pendulum (chapter 1): free, Lambda = 1.44 /s (3000 s; 1.51 over the first 200 s); held, equal arms (R = 1, resonance) chaotic from 1 to 6 of 9 starts at
  every Gamma from 0.1 to 31.6; the 1 m rod at 63 m (R = 94.5) unbraked: regular in its bowl, chaotic only from the two starts
  near the hilltop above Gamma = 3.6; braked at kappa*: all exponents about -6.4 per turn.
- Why the held rod is calm (chapter 1.5, 6 m/s, unbraked): the hilltop's height runs from 22.8 to 42.4 J once per turn; the
  adiabatic estimate puts the chaotic band at swings beyond 139 deg (computed: 132 to 134 deg) and, passing the bowl's bottom,
  at theta' = 18.6 to 20.6 per turn (computed: 18.4 to 20.4 forwards, 20.9 backwards); exponents in the band 1.10 to 1.23 per turn.
- Turbulent field (L6, 8 m/s, class A, record 1): rotor speed sd 11.8 %; second blade 200 mW against 205 mW in steady sheared
  wind; streamlined 197 mW; small wing 287 mW steady (formula (7.2) +44 %, solved +40 %) and 420 mW in the gusts.

## Queue
1. Pull request for section 7.6 (the range of sizes): Numa's "merge".

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
