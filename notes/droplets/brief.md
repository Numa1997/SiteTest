---
name: droplet-collection-loop
description: Rebuild the Droplet Collection portfolio (Numa's Bachelor thesis on how cloud droplets grow into rain) from first principles, autonomously, as a master agent that loops, deploys cheap role-bound subagents, and commits no physics that has not passed three gates.
---

# Droplet Collection: work until done, and commit no bullshit physics

First load the skills `physics-model-loop`, `physics-simulation-study` and `phyein-usul-physics-content`, and read `CLAUDE.md` and
`AGENTS.md`. This prompt applies them to one study. Where this prompt and the skills agree, follow both; where this prompt is more
specific, follow this prompt.

The task has three layers:
1. **The master loop** (sections 1 to 3): you keep working, turn after turn, deploying a few subagents, until the completion
   condition holds. Numa is not asked step by step.
2. **The physics** (sections 4 to 6): the question, the scales, the ladder of models from the simplest to the full one.
3. **The gates and the judge** (sections 7 and 8): nothing is committed until it is motivated, derived twice and attacked by a
   blind skeptic.

## 0. The ground (23 October 2026)

- The study is Numa's Bachelor thesis, *Collisional Ice Multiplication Processes in Clouds* (N. Koudsie, Leipzig 2022), remodelled
  in October 2026 as the Droplet Collection portfolio. Its AppDeploy app is gone: the account lists 0 apps and the source cannot be
  read. Never use AppDeploy.
- What survives is in the repository `Numa1997/SiteTest`: the built, minified copy served at `public/portfolios/droplet-collection/`
  (live on phyeinusul.com), and its text recovered as HTML with TeX in `notes/droplets/baseline/` (overview, theory, results,
  simulate, checks). A blind audit of that old version may be at `notes/droplets/skeptic-baseline-r1.md`. These files are on the branch
  `claude/awesome-ritchie-qiy1zo`; if your checkout lacks them, run
  `git fetch origin claude/awesome-ritchie-qiy1zo && git checkout origin/claude/awesome-ritchie-qiy1zo -- notes/droplets/`.
- **Start afresh.** You build a new study from first principles. The baseline is something to check against, not a text to copy.
  Every headline number of the old version must be reproduced by your model, or its change explained on the page: 6 / 14 min to
  50 / 90 % of the mass above 40 µm with the extended kernel, 3 / 5 min with the thesis kernel, 2.1 % largest fall-speed error against
  Gunn and Kinzer from 0.3 mm, 10⁻⁷ mass error against Golovin's exact solution, critical Stokes numbers 1/12 (potential flow) and
  1.21 (creeping flow).
- Another agent works in the same repository at the same time, on the Rotor Pendula portfolio. Section 3 says which files are yours.
  If its work causes a conflict or an error on your side, stop, note it, and let it finish.

---

## 1. The master loop

### 1.1 How the loop is kept alive

Right after writing `notes/droplets/done.md` (section 3), set the goal:

```
/goal Droplet Collection is complete when every item of notes/droplets/done.md is ticked with its evidence printed in this
conversation: all check scripts print PASS; the skeptic's final report passes all six thresholds of physics-model-loop section
7.3; the browser check passes at 360, 390, 1024 and 1440 px; the pull request into main is open and NOT merged;
notes/droplets/status.md has no open item except "Decisions for Numa". Never merge, never touch Cloudflare or AppDeploy, never edit
rotor-pendula files. Or stop after 200 turns and report where things stand.
```

If `/goal` is unavailable: never end a turn while the queue has an item you can act on; while waiting on a subagent or a long
command, use `Monitor` or `ScheduleWakeup` instead of ending idle; if a turn must end with work left, schedule
`send_later` ("Resume from notes/droplets/status.md") and cancel it when done.

### 1.2 What every turn does

1. Read `notes/droplets/status.md`.
2. Take the first open item. Do it yourself if it is coupled work (model, derivation, code, text); delegate it if it is reading,
   judging or mechanical checking (section 2).
3. Pass it through its gate (section 7).
4. Print the evidence in the conversation (check scripts' PASS/FAIL lines, the skeptic's verdict table, browser summary, commit
   hash): the goal's evaluator sees only the conversation.
5. Update `status.md`: tick what is done with its evidence, add what you found, re-order the queue.
6. Send Numa one or two plain sentences of progress, and continue.

### 1.3 When the loop stops for Numa

Only for: merging into `main` or anything irreversible (prepare it, then stop and ask); a decision only he can make (it changes the
question, the scope or the public claim: log it under "Decisions for Numa", ask once, keep working on everything else with the
stated default); missing input only he can give; a gate failing three rounds in a row (adopt the model that claims less, say on the
page that it is provisional and why, log both sides, continue). If Numa writes, his message comes first.

---

## 2. Subagents

| Role | Model | Deployed for | Never does |
|---|---|---|---|
| Scout | sonnet | Reading primary sources on one question; a dossier | Code, edits outside its dossier |
| Skeptic | opus | Blind attack on a contract or on finished pages | Read your plan, status or the dossiers' conclusions |
| Checker | sonnet (opus if it misses errors) | Re-deriving equations twice (SymPy and Wolfram), recomputing numbers from the model's code | Change any file but its report |
| Runner | haiku | Builds, check scripts, Playwright screenshots and error counts | Judge physics, fix anything |

At most three at once; none for a job you finish in about ten tool calls; they never start subagents, never commit, never write
outside `notes/droplets/`. Run them in the background and keep working; never state a result that has not arrived. Briefs: the four
parts of physics-model-loop section 9 (objective, output, tools and sources, boundaries).

---

## 3. Files, branch, the other agent

- Yours: `notes/droplets/` (`done.md`, `status.md`, `contract-L<k>.md`, `dossier-<topic>.md`, `skeptic-<gate>-L<k>-r<N>.md`,
  `check-L<k>.md`, `runner-r<N>.md`), `portfolios-src/droplets/`, `public/portfolios/droplet-collection/`.
- Not yours: anything about rotor pendula (`notes/rotor-pendula/`, `portfolios-src/rotor-pendula/`,
  `public/portfolios/rotor-pendula/`), the ten simulation pages and their notes.
- Shared: `public/portfolios.html` (only the `droplet-collection` article), `docs/portfolios.md` (only its droplet parts), `docs/files.md`
  (regenerated by `python3 tools/inventory.py`, never by hand). Before each commit, `git fetch origin` and look at what changed.
- Work on the branch the session gives you, never on `main`. Push it; open a pull request into `main` at the end; never merge.
  Never touch Cloudflare or any connector.
- `done.md`, written first and never weakened: (1) source in `portfolios-src/droplets/`, the served copy generated by its build
  script, same address; (2) nothing correct in the baseline lost, its headline numbers reproduced or the change explained;
  (3) every ladder level has a contract that passed Gate 1 and a check that passed Gate 2; (4) Gate 3 passed on all six thresholds;
  (5) number script PASS; (6) independent physics checks PASS; (7) browser check at 360, 390, 1024, 1440 px PASS with screenshots;
  (8) Portfolios page and docs updated, `python3 tools/inventory.py --check` passes; (9) branch pushed, pull request open, not merged.

---

## 4. The physics: question, observables, scales

### 4.1 The question and the observables

How does a warm cloud of small droplets turn into rain-sized drops by gravitational collection, how fast, and which physical
ingredient decides the speed? Then: what do collisions involving ice add (the thesis subject)?

1. **Mean-field growth time:** minutes until 50 % and 90 % of the liquid mass sits in drops of radius r ≥ 40 µm, for the thesis cloud
   (300 cm⁻³ droplets of 8 µm, 1 cm⁻³ collectors of 40 µm, 10 °C, 850 hPa).
2. **Time to the first large drops:** until the first drops of 100 µm (and 1 mm) appear in a stated volume of cloud, with its spread
   over an ensemble of stochastic runs. Rain begins with the luckiest drops, not the average one.
3. **Ice:** ice particles produced per cm³ per minute, each rate with its physical source.

Before any model, write a Fermi estimate of 1 and 2 (one collector sweeping a cloud of about 0.3 g/m³ liquid water at its fall speed)
on the first page of `status.md`. Every later result is compared with it.

### 4.2 Scales and the dominant balance (computed 23 October 2026 with μ = 1.8 × 10⁻⁵ Pa s, ρ_air = 1.2 kg/m³, σ = 0.072 N/m, T = 280 K; recompute)

- **Fall speed.** Stokes gives 1.21 cm/s at r = 10 µm (Re = 0.016), 0.30 m/s at 50 µm (Re = 2.0), 1.21 m/s at 100 µm (Re = 16), outside
  its own validity. The fall-speed law must change with size near Re = 1 (r ≈ 40 µm), and the text says where.
- **Inertia.** A 10 µm droplet's response time τ_p = 2ρ_w r²/(9μ) is 1.2 ms; the Kolmogorov time √(ν/ε) at ε = 10⁻² m²/s³ is 39 ms:
  Stokes number 0.03 (0.010 to 0.10 for ε = 10⁻³ to 10⁻¹ m²/s³). The droplet almost follows the smallest eddies.
- **Thermal noise.** Surface energy 4πr²σ = 9.0 × 10⁻¹¹ J is 2.3 × 10¹⁰ kT: thermal fluctuations play no role, and the equilibrium fate
  (one big drop) says nothing about the rate.
- **Counting.** A 40 µm collector must swallow about (100/8)³ ≈ 2000 droplets of 8 µm to reach 100 µm, but the first few collisions
  take most of the time. Few events decide the outcome: relative fluctuations of order 1/√N with N small are physics, not noise.

### 4.3 Level of description, laws, closures

- Mean field (the stochastic collection equation) is right for observable 1; it is wrong for observable 2, where the master equation
  itself must be sampled.
- Conservation first: mass is conserved by collection; number falls by one per merger; ice reactions say which moment they keep.
- Every closure (drag law, collision efficiency, coalescence efficiency, fragment numbers) is named as a closure, with its source
  (derived here, measured by whom, fitted to what) and its validity range in terms of the groups above.
- **Forbidden as laws of motion:** energy minimisation, gradient descent, Metropolis sampling, maximum entropy. Rain formation is
  driven and irreversible; its dynamics are kinetics (rates, master equation, conservation laws). Equilibrium may say where a drop ends
  up, never how fast.
- **Stochastic honesty:** Gillespie's algorithm samples the master equation exactly (τ = −ln(u₁)/a₀; event j where the cumulative rate
  first exceeds u₂a₀). Results are ensembles: means with standard errors over a stated number of runs, distributions where the spread
  matters, the seeds. Any turbulent noise has a source, an amplitude from cited flow statistics and a correlation time.

---

## 5. The ladder (one effect per level, each justified by a computed number)

- **L0, one collector, continuous collection.** One drop falls through a uniform cloud of identical droplets: Stokes fall speed,
  collision efficiency 1, dm/dt = E π(R + r)² Δv ρ_l·LWC. Solve it analytically (with Stokes speed the radius blows up in finite time:
  say why and what stops it). The baseline for every later level.
- **L1, fall speed from a drag balance.** Weight against drag with C_D(Re): which law, derived limit or measured fit, by whom, over
  what Re range. Reproduce Gunn and Kinzer (1949) with its stated error.
- **L2, collision efficiency from trajectories.** Integrate the small droplet's motion in the flow around the collector (Stokes flow,
  potential flow, then the interpolation in Re you justify), find the grazing trajectory, build the efficiency table yourself in code
  that is part of the study (the old table had no generator). Reproduce the critical Stokes numbers 1/12 and 1.21.
- **L3, coalescence efficiency.** Contact is not merger. Derive the energy ratio that decides it (Weber number), adopt a measured law
  with source and range (for example Low and List 1982, Beard and Ochs 1984), show its effect on observable 1.
- **L4, the population, mean field.** Derive the SCE from binary gains and losses; a number- and mass-conserving scheme (two-bin
  remapping, Bott 1998, or a stated alternative); mass conserved to machine precision; Golovin's exact solution passed with the observed
  order of convergence. Say plainly that it is an equation for the mean.
- **L5, the stochastic process itself.** The SCE is the mean of a master equation. Sample it exactly (Gillespie for a small volume; a
  super-droplet Monte Carlo such as Shima et al. 2009 for a large one); check that the ensemble mean recovers L4; compute observable 2
  with its spread. Read Telford (1955), Gillespie (1972, 1975) and Kostinski and Shaw (2005) whole. This is the main new physics.
- **L6, turbulence.** From the Stokes number of 4.2, decide by a computed number whether turbulent shear (Saffman and Turner 1956),
  clustering and enhanced relative velocity (Ayala, Rosa and Wang 2008; review Grabowski and Wang 2013) change observable 1 or 2 by more
  than their uncertainty. If yes, add one closure with source and range; if no, keep it as a stated check.
- **L7, ice.** The thesis channels (riming, ice-ice and ice-graupel collisions, fragmentation), each rate from a cited measurement or
  derivation with its range (for example Hallett and Mossop 1974, Vardiman 1978, Phillips, Yano and Khain 2017, review Field et al.
  2017), with the mass and number books.

A level whose effect is below the observables' uncertainty does not enter; it stays as a check. No level is skipped.

---

## 6. Predictions that could come out wrong (into the contracts before computing)

- With L5 the first 100 µm drops in 1 m³ of cloud appear earlier than the mean-field time of L4, by a factor you predict from the
  Fermi estimate. If the ensemble shows no gap, find out why before going on.
- The kernel (L1 to L3) changes observable 1 more than the bookkeeping (GCE against SCE). The old study claimed this; test it.
- Turbulence at ε = 10⁻² m²/s³ changes observable 1 by less than X %; choose X from the literature before you compute.

---

## 7. The three gates

- **Gate 1, Motivate (before code for a level):** `contract-L<k>.md` with the question and observable; the picture and the formal
  mechanism; the model (variables, laws, closures); at least two rejected alternatives and why; assumptions, each with its computed
  dimensionless number and where it fails; exact solutions, limits and measurements it must reproduce; a prediction that could fail;
  what is derived, cited or chosen, and the price. A blind skeptic attacks it; answer every objection inside the contract.
- **Gate 2, Derive (before an equation or number enters the text):** every numbered equation by two independent routes (SymPy and
  Wolfram, or two physical routes), units, sign, one known limit; exact solutions reproduced in code. The checker writes
  `check-L<k>.md`; every "wrong" is fixed, every "unverifiable" said so in the text.
- **Gate 3, Attack (before commit):** all runner checks and the number script pass; the skeptic reads the rendered pages blind, as a
  strong second-year student and as Numa. Six thresholds, each must pass: motivated, honest, derived, checked, sourced, readable.
  At most three rounds per gate, then section 1.3.

## 8. The skeptic's list, plus this study's traps

Everything in physics-model-loop section 8, and: a stored table without the code that made it; a fitted fall-speed or efficiency law
used beyond its measured range; the 40 µm threshold sold as rain; a mean-field curve presented as the time of the first rain; a
single stochastic run; ice rates without a measurement behind them; the equilibrium tools of 4.3 used as dynamics.

## 9. The finished study

The standard of `physics-simulation-study`; the reference is `portfolios-src/hydraulics/` (open it). Source in
`portfolios-src/droplets/`: the model in one physics block that Node can run; a textbook deriving every equation the solver
integrates (Picture, Working, Check and "In our cloud" boxes; numbered equations; motivation from everyday experience first); a
simulation page; worked problems; a number script; independent Python checks (constants retyped, SciPy re-integration, SymPy
derivations); a browser check at 360, 390, 1024 and 1440 px. The served copy keeps its address and is generated by the build script.
The old bundle stays served until the new one passes every gate. House design and interaction rules: `CLAUDE.md`.

## 10. First actions

1. Write `done.md` (section 3), set the goal (1.1), write `status.md` with the Fermi estimate.
2. Launch two scouts (sonnet): fall speed and collision efficiency (Gunn and Kinzer 1949, Beard 1976, Hall 1980, Pinsky, Khain and
   Shapiro 2001); the stochastic process (Telford 1955, Gillespie 1972 and 1975, Kostinski and Shaw 2005, Shima et al. 2009, Alfonso
   et al. on the validity of the SCE). Each writes a dossier and returns five lines.
3. While they read, write contract L0, derive and solve it, check it in SymPy and Wolfram, and send it to a blind skeptic.

## 11. Talking to Numa

A one-line progress message at each gate, each finished level and each subagent return. Connected prose, metric units, terms
defined at first use. Mark facts (with a source he can open), inferences and opinions. When one of his ideas fails the method, say so
once with the physics and build the honest version. At a stop: "Where we are:" and "Next, if you say yes:", one sentence each.
