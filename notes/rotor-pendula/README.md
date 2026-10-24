# Rotor Pendula: the working record

What was built, from which scripts, and what is still open. The page itself is built from
`portfolios-src/rotor-pendula/` (see its README); this folder holds the models and the sources behind the numbers.

## The question
A pendulum hangs from a turbine blade, and a small generator brakes its swing. How much power does it deliver, and can
the wind's disorder (gusts, a bending and shaking blade) give it more?

## The setup (chosen for these notes)
- Pendulum: 0.1 kg on 0.2 m. Double pendulum: the same mass and reach split in two (0.05 kg on 0.1 m, twice).
- Rotor: tip-speed ratio 7 at a wind of 8 m/s, so the rotor radius is 56 m/s ÷ Ω.
- Six rotor speeds (400, 200, 100, 20, 14, 8 rpm) × three pivots (30, 60, 90 % of the blade) = 18 mountings.
- Brake: the small-swing best brake, κ* = |R − 1| for the single pendulum (2.4) and the double's own small-swing
  optimum (`L1_map.py`, `kappa_star`).
- Large turbine: NREL 5 MW reference (Jonkman et al. 2009). Generator: maxon RE 25 + GP 32 C (catalogue pages 153, 430–431).

## Models, by layer (`derive/`)
| Layer | What it adds | Scripts | Output |
|---|---|---|---|
| L0 | small-swing theory, best brake, P* = m L g²/(4Ω\|r_p − L\|) | `L0_single.py` (SymPy), `L0_r2.py`, `scales.py` | `L0_r2.json` |
| L1 | full nonlinear single and double, Radau IIA engine, chaos | `engine.py`, `L1_double.py`, `L1_engine_check.py`, `L1_chaos.py`, `L1_map.py`, `L1_map_g70.py` | `L1_mountings.json`, `L1_chaos.json`, `L1_map*.json` |
| L2 | gusts on the NREL 5 MW turbine with its controller | `L2_*.py` | `L2_run*.json`, `L2_scales.json` |
| L3 | the blade sags and shakes; tuned rod | `L3_sag*.py`, `L3_shake2.py`, `nrel5mw.py` | `L3_sag*.json`, `L3_shake2.json`, `L3_shake_model.json` |
| L4 | real geared generator: losses, friction, reflected inertia | `L4_*.py` | `L4_*.json` |

Every script prints PASS/FAIL lines and exits 1 on a failure. Their outputs are copied into
`portfolios-src/rotor-pendula/data/`, and `tools/make_numbers.py` turns them into every number on the page.

## Results
- The 18 mountings deliver 9.55–57.1 mW (single). The double delivers 0.635–0.735 times as much.
- Chaos appears only near R = 1, where no real mounting sits; there the best regular setting beats it.
- White-noise shaking is capped at S·M/2. Gusts change the power by a few per cent, with the sign set by the controller.
  The blade's sag changes it by −0.8 to +2.1 %.
- A tuned long rod is not shown to work: gravity detunes it by ±9.6 % every turn.
- With the real generator on a large turbine, the load gets 1.8–9.0 mW, at least 47 times the sensor's 37.6 µW.

## Sources (`dossier-*.md`)
`dossier-turbine.md` (NREL 5 MW, OpenFAST blade file), `dossier-generator.md` (maxon catalogue),
`dossier-edgewise.md` (blade edgewise mode), `dossier-harvesting.md` (sensor power).

## Open
- Print the equations of the blade-shaking model and of the double pendulum in the notes.
- Time-domain run of the tuned rod with gravity kept whole.
- Bench test of the gear drag and the back-driven efficiency.
- Converting the low, slow load voltage (0.13–0.55 V peak) into a supply.
