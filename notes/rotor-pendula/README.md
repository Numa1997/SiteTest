# Rotor Pendula: the working record

What was built, from which scripts, and what is still open. The page itself is built from
`portfolios-src/rotor-pendula/` (see its README); this folder holds the models and the sources behind the numbers.

## The question
A pendulum hangs inside a turbine blade, and a small generator brakes its swing. How much power does it deliver to a blade
sensor, and can the wind's disorder (gusts, a bending and shaking blade) or a chaotic double pendulum give it more?

## The setup (`derive/setup.py`, written once and imported by every script)
- Turbine: the NREL 5 MW reference turbine (Jonkman et al. 2009): rotor radius 63 m, peak power coefficient 0.482 at
  tip-speed ratio 7.55. In region 2 a steady wind v turns the rotor at Omega = 7.55 v / 63 m.
- Three steady winds, 6, 8 and 10 m/s (6.9, 9.2 and 11.4 rpm), times three pivots at 30, 60 and 90 % of the radius: nine mountings.
- Rod 0.1 m, so the device fits in a box about 20 cm across inside the blade at every pivot (the thinnest section, at 90 %, is
  0.41 m thick and 2.26 m wide).
- Bob 0.5 kg, sized by `derive/design.py`: the smallest mass of the 1-2-5 series whose worst mounting still gives the sensor ten
  times its need through the real generator, with twice the catalogue friction and 50 % gear efficiency.
- Double pendulum: the same mass and reach, 0.25 kg on 0.05 m, twice.
- Brakes: the single's best brake kappa* = |R - 1| (2.4); the double's own small-swing optimum (`L1_map.py`, `kappa_star`).
- Sensor need, 37.6 uW, added up in `derive/sensor.py` from the ADXL362 (Rev. G, Table 1) and CC2652R (SWRS207J, 8.5-8.6) datasheets:
  accelerometer at 100 Hz, radio chip in standby, and once a second 1 ms of computing and 1 ms of sending.

## Models, by layer (`derive/`)
| Layer | What it adds | Scripts | Output |
|---|---|---|---|
| L0 | small-swing theory, best brake, P* = m L g²/(4Ω\|r_p − L\|), tilted hinge, trail | `L0_single.py` (SymPy), `L0_r2.py` | `L0_r2.json` |
| L1 | full nonlinear single and double, Radau IIA engine, chaos | `engine.py`, `L1_double.py`, `L1_engine_check.py`, `L1_chaos.py`, `L1_map.py`, `L1_map_g70.py` | `L1_mountings.json`, `L1_chaos.json`, `L1_map*.json` |
| power theorem | white-noise shaking feeds at most S M/2 | `power_theorem.py` (SymPy), `power_theorem_mc.py` | `mc_full.log` |
| L2 | gusts on the NREL 5 MW turbine with its controller | `turbulence.py`, `L2_run.py`, `L2_scales.py` | `L2_run_*.json`, `L2_scales.json` |
| L3 | the blade sags and shakes; tuned rod | `nrel5mw.py`, `L3_sag*.py`, `L3_shake_model.py`, `L3_shake2.py` | `L3_*.json` |
| L4 | real geared generator: losses, friction, reflected inertia; the bob's size | `L4_generator.py`, `L4_full.py`, `L4_scan.py`, `L4_check.py`, `L4_converge.py`, `L4_stick.py`, `L4_sensitivity.py`, `design.py` | `L4_*.json`, `design.json` |

Every script prints PASS/FAIL lines and exits 1 on a failure. Their outputs are copied into
`portfolios-src/rotor-pendula/data/`, and `tools/make_numbers.py` turns them into every number on the page.

## Results
- The nine mountings deliver 17.7–88.6 mW of mechanical power (single pendulum); at each pivot the power falls as 1/v as the
  wind rises. The double gives 0.735 times as much at every mounting.
- Chaos appears only at resonance (R = 1), where no real mounting sits; there the best regular brake beats every chaotic one.
  On the extended map (R up to 600, G up to 200) every run is regular from R = 2 on.
- White-noise shaking is capped at S M/2. Gusts change the power by about −2 % with the turbine's full controller and a
  little under +1 % with a pure square law. The blade's sag changes it by a few per cent at most.
- A tuned long rod is not shown to work: gravity detunes it by ±9.6 % of its frequency every turn.
- The real generator (maxon RE 25 + GP 32 C) brings the load several milliwatts at every mounting, about a hundred times the
  sensor's need at the weakest; see Table 4 of the notes for the numbers.

## Sources (`dossier-*.md`)
`dossier-turbine.md` (NREL 5 MW, OpenFAST blade file), `dossier-generator.md` (maxon catalogue),
`dossier-edgewise.md` (blade edgewise mode), `dossier-harvesting.md` (harvesting literature).

## Open
- Print the equations of the blade-shaking model and of the double pendulum in the notes.
- Time-domain run of the tuned rod with gravity kept whole.
- Bench test of the gear drag, the back-driven efficiency and the gear play, starting at the weakest mounting (10 m/s, 90 %).
- Converting the low, slow load voltage into a supply.
