# Prompt for the droplet agent: Droplet Collection, rebuilt from first principles

Paste everything below the line into a fresh Claude Code session on `Numa1997/SiteTest`.

---

Load the skills `physics-model-loop`, `physics-simulation-study` and `phyein-usul-physics-content` before anything else, and
follow them. The loop and its three gates are the method of this task; this prompt only gives the study. Also use `sympy`,
`wolfram-language`, `theoretical-physicist`, `unslop` and `verification-before-completion` where the loop says so. Read
`CLAUDE.md` and `AGENTS.md`.

## 0. The ground, as of 23 October 2026

- The study is Numa's Bachelor thesis, *Collisional Ice Multiplication Processes in Clouds* (N. Koudsie, Leipzig 2022), remodelled
  in October 2026 as the Droplet Collection portfolio. Its AppDeploy app is gone (the account lists 0 apps; the source cannot be
  read). Do not use AppDeploy at all.
- What survives is in this repository: the built, minified copy served at `public/portfolios/droplet-collection/` (live on
  phyeinusul.com), and its text recovered as HTML with TeX in `notes/droplets/baseline/` (overview, theory, results, simulate,
  checks). `notes/droplets/skeptic-baseline-r1.md`, if present, is a blind audit of that old version. Both were made on the branch
  `claude/awesome-ritchie-qiy1zo`; if your checkout lacks them, bring them in with
  `git fetch origin claude/awesome-ritchie-qiy1zo && git checkout origin/claude/awesome-ritchie-qiy1zo -- notes/droplets/`.
- **Start afresh.** You build a new study from first principles. The baseline is a reference to check against, not a text to copy:
  every headline number of the old version (6 / 14 min to 50 / 90 % of the mass above 40 µm with the extended kernel, 3 / 5 min with
  the thesis kernel, 2.1 % fall-speed error against Gunn and Kinzer from 0.3 mm, 10⁻⁷ mass error against Golovin, the critical
  Stokes numbers 1/12 and 1.21) must be reproduced by your model or its change explained on the page.
- Another agent works in the same repository at the same time on the Rotor Pendula portfolio. Section 6 says which files are yours.

## 1. The question and the observable

How does a warm cloud of small droplets turn into rain-sized drops by gravitational collection, how fast, and which physical
ingredient decides the speed? Then: what do collisions involving ice add (the thesis subject)?

Observables, each in SI units with its uncertainty:
1. The mean-field growth time: minutes until 50 % and 90 % of the liquid mass sits in drops of radius r ≥ 40 µm, for the test cloud
   of the thesis (300 cm⁻³ droplets of 8 µm, 1 cm⁻³ collectors of 40 µm, 10 °C, 850 hPa).
2. The time until the first drops of radius 100 µm (and 1 mm) appear in a given volume of cloud, with its spread over an ensemble of
   stochastic runs. This is not observable 1: rain begins with the luckiest drops, not the average one.
3. For the ice part, the number of ice particles produced per cm³ per minute, with the physical source of every rate.

Before any model, write a Fermi estimate of observables 1 and 2 (one collector sweeping a cloud of liquid water content about
0.3 g/m³ at its fall speed) and keep it on the first page of `notes/droplets/status.md`. Every later result is compared with it.

## 2. Scales and dominant balance (recompute every number; these were computed on 23 October 2026 with μ = 1.8 × 10⁻⁵ Pa s, ρ_air = 1.2 kg/m³, σ = 0.072 N/m, T = 280 K)

- Fall speed: Stokes gives 1.21 cm/s at r = 10 µm (Re = 0.016), 0.30 m/s at 50 µm (Re = 2.0), 1.21 m/s at 100 µm (Re = 16), outside
  its validity. The fall-speed law must change with size, and the text says where (Re = 1 near 40 µm).
- Inertia: a 10 µm droplet's response time τ_p = 2ρ_w r²/(9μ) is 1.2 ms; the Kolmogorov time √(ν/ε) at ε = 10⁻² m²/s³ is 39 ms,
  so the Stokes number is 0.03 (0.010–0.10 for ε = 10⁻³ to 10⁻¹ m²/s³).
- Thermal noise: the droplet's surface energy 4πr²σ = 9.0 × 10⁻¹¹ J is 2.3 × 10¹⁰ kT. Its equilibrium fate says nothing about its rate.
- Counting: a 40 µm collector must swallow about (100/8)³ ≈ 2000 droplets of 8 µm to reach 100 µm, but the first few collisions
  take most of the time. Few events decide the outcome, so relative fluctuations of order 1/√N with N small are physics, not noise.

## 3. The ladder (one effect per level, each justified by a computed number; section 5 of physics-model-loop)

- **L0, one collector, continuous collection.** One drop falls through a uniform cloud of identical droplets, Stokes fall speed,
  collision efficiency 1, continuous growth dm/dt = E π(R+r)² Δv ρ_l LWC. Solve it analytically (with Stokes speed the radius
  blows up in finite time; say why and what stops it). This is the baseline every level is compared with.
- **L1, fall speed from a drag balance.** Replace Stokes by the balance of weight and drag with a drag coefficient C_D(Re); say which
  C_D law (derived limit, measured fit, by whom, over what Re range), and reproduce Gunn and Kinzer (1949) with its stated error.
- **L2, collision efficiency from trajectories.** Integrate the small droplet's equation of motion in the flow around the collector
  (Stokes flow and potential flow, then the interpolation in Re you choose and justify), find the grazing trajectory, and build the
  efficiency table yourself, in code that is part of the study (the old table had no generator; that must not happen again).
  Reproduce the critical Stokes numbers 1/12 (potential flow) and 1.21 (creeping flow).
- **L3, coalescence efficiency.** Contact is not merger. Derive the energy ratio that decides it (Weber number), adopt a measured law
  with its source and range (for example Low and List 1982, Beard and Ochs 1984), and show by how much it changes observable 1.
- **L4, the population: stochastic collection equation (mean field).** Derive the SCE from binary gains and losses, conserve mass to
  machine precision with a number- and mass-conserving scheme (two-bin remapping, Bott 1998 flux method, or a stated alternative),
  pass the Golovin exact solution with the observed order of convergence. State plainly that it is an equation for the mean.
- **L5, the stochastic process itself.** The SCE is the mean of a master equation. Sample that master equation exactly (Gillespie's
  algorithm for a small volume; a super-droplet Monte Carlo such as Shima et al. 2009 for a large one), check that its ensemble mean
  recovers L4, and compute observable 2 with its spread over a stated number of runs and seeds. Read Telford (1955), Gillespie (1972,
  1975) and Kostinski and Shaw (2005) whole. This level is the main new physics of the study.
- **L6, turbulence.** With the Stokes number of section 2, decide by a computed number whether turbulent shear (Saffman and Turner
  1956), droplet clustering and enhanced relative velocity (for example Ayala, Rosa and Wang 2008; review Grabowski and Wang 2013)
  change observables 1 or 2 by more than their uncertainty. If they do, add them as one closure with its source and range; if not,
  keep it as a stated check that they are negligible. Any turbulent noise has a source, an amplitude from cited flow statistics and a
  correlation time (physics-model-loop 4.6).
- **L7, ice.** Only now: the reaction channels of the thesis (riming, ice-ice and ice-graupel collisions, fragmentation), each rate
  from a cited measurement or derivation with its validity range (for example Hallett and Mossop 1974, Vardiman 1978, Phillips, Yano
  and Khain 2017, the review by Field et al. 2017). Mass and number books: which moment each reaction conserves, and which it changes.

A level whose effect on the observables is smaller than their uncertainty does not enter; it appears as a check.

**Forbidden as laws of motion** (physics-model-loop 4.5 and 8): energy minimisation, gradient descent, Metropolis sampling and
maximum entropy. Rain formation is driven and irreversible; its dynamics are kinetics. Equilibrium may be quoted only to say where
a drop would end up, never how fast.

## 4. Predictions that could come out wrong (write them into the contracts before computing)

- With L5, the time for the first 100 µm drops in 1 m³ of cloud is shorter than the mean-field time of L4 by a factor you predict
  from the Fermi estimate; if the ensemble shows no such gap, find out why before going on.
- The kernel (L1-L3) changes observable 1 more than the bookkeeping (GCE against SCE) does. The baseline claimed this; test it.
- Turbulence at ε = 10⁻² m²/s³ changes observable 1 by less than X %. Choose X from the literature before you compute.

## 5. What the finished study looks like

The standard of `physics-simulation-study` (the Hydraulic Press Study in `portfolios-src/hydraulics/` is the reference; open it):
source in `portfolios-src/droplets/`; the model in one physics block that Node can run; a textbook that derives every equation the
solver integrates, with Picture, Working, Check and "In our cloud" boxes; a simulation page; worked problems; a number script
(every quoted number found in the text, computed by the model); independent Python checks (constants retyped, SciPy re-integration,
SymPy derivations); a browser check at 360, 390, 1024 and 1440 px (0 KaTeX errors, 0 page errors, no sideways scroll). The served
copy at `public/portfolios/droplet-collection/` is generated by the build script and keeps that address; the old bundle stays served
until the new one passes every gate. House design and interaction rules: `CLAUDE.md`.

## 6. Files, branch and the other agent

- Yours: `notes/droplets/` (write `done.md` from this prompt first, then `status.md`, contracts, dossiers, reports),
  `portfolios-src/droplets/`, `public/portfolios/droplet-collection/`.
- Not yours: anything about rotor pendula (`notes/rotor-pendula/`, `portfolios-src/rotor-pendula/`,
  `public/portfolios/rotor-pendula/`), the ten simulation pages and their notes.
- Shared: `public/portfolios.html` (edit only the `droplet-collection` article), `docs/portfolios.md` (only its droplet sections),
  `docs/files.md` (regenerated by `python3 tools/inventory.py`; never hand-edit). Before each commit: `git fetch origin` and look at
  what changed. If a merge conflict or a failing build comes from the other agent's work, stop, write it under "Decisions for Numa",
  and let it finish; do not edit its files.
- Work on the branch the session gives you, never on `main`. Push your branch; open a pull request into `main` at the end; never merge.
  Never touch Cloudflare or any connector.

## 7. The goal line (set it right after writing done.md)

```
/goal Droplet Collection is complete when every item of notes/droplets/done.md is ticked with its evidence printed in this
conversation: all check scripts print PASS; the skeptic's final report passes all six thresholds of physics-model-loop section 7.3;
the browser check passes at 360, 390, 1024 and 1440 px; the pull request into main is open and NOT merged; notes/droplets/status.md
has no open item except "Decisions for Numa". Never merge, never touch Cloudflare or AppDeploy, never edit rotor-pendula files.
Or stop after 200 turns and report where things stand.
```

## 8. First three actions

1. Write `notes/droplets/done.md` as a checklist of nine items: (1) source in `portfolios-src/droplets/`, served copy generated;
   (2) nothing correct in the baseline lost, its headline numbers reproduced or the change explained; (3) every ladder level with a
   contract that passed Gate 1 and a check that passed Gate 2; (4) Gate 3 passed on all six thresholds; (5) number script PASS;
   (6) independent physics checks PASS; (7) browser check at four widths PASS with screenshots; (8) Portfolios page and docs
   updated, `python3 tools/inventory.py --check` passes; (9) branch pushed, pull request open and not merged. Then `status.md`
   with the Fermi estimate.
2. Launch two scouts (sonnet): one on fall speed and collision efficiency (Gunn and Kinzer 1949, Beard 1976, Hall 1980, Pinsky, Khain
   and Shapiro 2001), one on the stochastic process (Telford 1955, Gillespie 1972 and 1975, Kostinski and Shaw 2005, Shima et al.
   2009, Alfonso et al. on the validity of the SCE). Each writes a dossier and returns five lines.
3. While they read, write and derive contract L0 yourself, solve it analytically, check it in SymPy and Wolfram, and send it to a
   blind skeptic.
