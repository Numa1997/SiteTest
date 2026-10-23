---
name: rotor-pendula-loop
description: Rebuild the Rotor Pendula portfolio around a new question, whether double pendula on turbine blades can turn chaotic wind to their advantage, autonomously, as a master agent that loops, deploys cheap role-bound subagents, and commits no physics that has not passed three gates.
---

# Rotor Pendula: chaos against chaotic wind. Work until done, and commit no bullshit physics

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

- The Rotor Pendula portfolio is Sol's corrected study of a pendulum hung from a point on a turning wind-turbine blade, braked by a
  generator at its pivot, as a power supply for a blade sensor. Its AppDeploy app is gone (0 apps; source unreadable). Never use
  AppDeploy.
- What survives is in the repository `Numa1997/SiteTest`: the built copy served at `public/portfolios/rotor-pendula/` (with Sol's
  report and the 181 files of his delivery), and its text recovered as HTML with TeX in `notes/rotor-pendula/baseline/` (overview,
  theory, results, simulate, checks, report). A blind audit of the old version may be at `notes/rotor-pendula/skeptic-baseline-r1.md`,
  a dossier on the reference turbine at `notes/rotor-pendula/dossier-turbine.md`. These are on the branch `claude/awesome-ritchie-qiy1zo`;
  if your checkout lacks them, run
  `git fetch origin claude/awesome-ritchie-qiy1zo && git checkout origin/claude/awesome-ritchie-qiy1zo -- notes/rotor-pendula/`.
- **Start afresh** with the new question of section 4. Sol's uniform-rotation results are the reference and must be reproduced or
  their change explained: the linear optimum κ = |R − 1| with P* = M L g² / (4 Ω |r_p − L|); the 18 mountings giving 9.55–57.1 mW; the
  double-to-single ratio 0.64–0.74 at equal mass and reach; the rotor's share ≤ 7.2 × 10⁻⁵. Sol's report stays word for word.
- A first derivation exists in `notes/rotor-pendula/derive/L0_single.py` (SymPy, all PASS): the single pendulum's equation of motion
  with the rotor angle φ(t) left free, the energy book d(T+V)/dt = τ_rot φ̇ − c θ̇² (the rotor pays for every joule), the blade-angle form,
  and Sol's 57.1 mW reproduced (57.13 mW). Check it, then build on it.
- Another agent works in the same repository at the same time, on the Droplet Collection portfolio. Section 3 says which files are
  yours. If its work causes a conflict or an error on your side, stop, note it, and let it finish.

---

## 1. The master loop

### 1.1 How the loop is kept alive

Right after writing `notes/rotor-pendula/done.md` (section 3), set the goal:

```
/goal Rotor Pendula is complete when every item of notes/rotor-pendula/done.md is ticked with its evidence printed in this
conversation: all check scripts print PASS; the skeptic's final report passes all six thresholds of physics-model-loop section
7.3; the browser check passes at 360, 390, 1024 and 1440 px; the pull request into main is open and NOT merged;
notes/rotor-pendula/status.md has no open item except "Decisions for Numa". Never merge, never touch Cloudflare or AppDeploy,
never edit droplet files. Or stop after 200 turns and report where things stand.
```

If `/goal` is unavailable: never end a turn while the queue has an item you can act on; while waiting on a subagent or a long
command, use `Monitor` or `ScheduleWakeup` instead of ending idle; if a turn must end with work left, schedule
`send_later` ("Resume from notes/rotor-pendula/status.md") and cancel it when done.

### 1.2 What every turn does

1. Read `notes/rotor-pendula/status.md`.
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
outside `notes/rotor-pendula/`. Run them in the background and keep working; never state a result that has not arrived. Briefs: the
four parts of physics-model-loop section 9 (objective, output, tools and sources, boundaries).

---

## 3. Files, branch, the other agent

- Yours: `notes/rotor-pendula/` (`done.md`, `status.md`, `contract-L<k>.md`, `dossier-<topic>.md`, `skeptic-<gate>-L<k>-r<N>.md`,
  `check-L<k>.md`, `runner-r<N>.md`, `derive/`), `portfolios-src/rotor-pendula/`, `public/portfolios/rotor-pendula/`.
- Not yours: anything about droplets (`notes/droplets/`, `portfolios-src/droplets/`, `public/portfolios/droplet-collection/`), the
  ten simulation pages and their notes.
- Shared: `public/portfolios.html` (only the `rotor-pendula` article), `docs/portfolios.md` (only its rotor parts), `docs/files.md`
  (regenerated by `python3 tools/inventory.py`, never by hand). Before each commit, `git fetch origin` and look at what changed.
- Work on the branch the session gives you, never on `main`. Push it; open a pull request into `main` at the end; never merge.
  Never touch Cloudflare or any connector.
- `done.md`, written first and never weakened: (1) source in `portfolios-src/rotor-pendula/`, the served copy generated by its build
  script, same address, Sol's report and delivery kept; (2) Sol's headline numbers reproduced or the change explained; (3) every ladder
  level has a contract that passed Gate 1 and a check that passed Gate 2; (4) Gate 3 passed on all six thresholds; (5) number script
  PASS; (6) independent physics checks PASS; (7) browser check at 360, 390, 1024, 1440 px PASS with screenshots; (8) Portfolios page
  and docs updated, `python3 tools/inventory.py --check` passes; (9) branch pushed, pull request open, not merged.
- Default in force (a decision for Numa): the portfolio has two parts, Sol's uniform-rotation study (Part I, reproduced and checked)
  and the turbulent-wind study (Part II, new).

---

## 4. The physics: question, observables, scales

### 4.1 The question and the observables

Wind is turbulent. Can a pendulum on a blade, and in particular a double pendulum whose motion is chaotic, turn that randomness to
its advantage: harvest more, or more reliably, than a single pendulum of the same mass and reach? Who pays for the energy, and what
does the pendulum do to the blade?

Each observable comes with its uncertainty over a stated ensemble of 10-minute turbulent wind records (the averaging time of IEC
61400-1):
1. Mean electrical power P̄ delivered to the load.
2. Reliability: the 5 % quantile of the 10-minute mean power, and the fraction of 10-minute periods that cover the sensor node's need
   (37.6 µW in the old study; re-derive it from the two datasheets).
3. The cost: the share of the rotor's power, and the change in the blade's in-plane vibration amplitude (a pendulum is also a
   vibration absorber).

Before any model, write a Fermi estimate of observable 1 for each energy source of 4.2 on the first page of `status.md`.

### 4.2 Scales and the dominant balance (computed 23 October 2026 for Sol's 18 mountings: M = 0.1 kg, L = 0.2 m, tip-speed ratio 7, wind 8 m/s; recompute)

- **Order tuning.** At uniform rotation the single pendulum obeys θ̈ + γθ̇ + (r_p/L)Ω² sin θ + (g/L) cos(Ωt + θ) = 0. Its own frequency
  is Ω√R with R = r_p/L, and gravity pushes once per turn, at Ω. Both scale with Ω, so a slow change of rotor speed does not detune
  the pendulum from gravity's push. In blade-angle time the equation depends only on R, G = g/(Ω²L), κ = c/(ML²Ω) and ε = Ω̇/Ω².
- **Far from resonance.** Across the 18 mountings R runs from 2.0 to 301, so the pendulum's own frequency (1.3–16 Hz) lies 1.4 to 17
  times above the once-per-turn push (0.13–6.7 Hz). Sol's resonance at r_p = L would put the pivot 20 cm from the hub.
- **Where the wind's randomness can enter.** (a) Rotor speed: low-pass filtered by the rotor's inertia (compute its time constant and
  ε for a cited reference turbine); order tuning predicts little effect; test it. (b) Blade in-plane (edgewise) vibration, excited by
  gravity once per turn and by rotationally sampled turbulence: on the large rotors the pendulum's own frequency (1.3–3.7 Hz) lies in
  the band of the first edgewise blade modes (about 1.1 Hz for the NREL 5-MW blade; read Jonkman et al. 2009, NREL/TP-500-38060).
  The blade mode has a fixed frequency while the pendulum's moves with Ω, so a tuned single pendulum detunes as the wind changes the
  rotor speed. This is where a broadband, chaotic harvester could win. (c) Turbulence: IEC class A at 8 m/s gives σ_u = 1.86 m/s,
  I = 0.23; Kaimal length scale 340 m, integral time 42.5 s (verify from the standard).
- **Upper bound from gravity alone.** A bob held hanging while the blade turns round it takes torque at most M g L at relative speed Ω:
  164–411 mW on the large rotors.
- **Dropped terms need their numbers.** The blade carries the pivot through the air at r_pΩ = 17–50 m/s: compute the drag on an exposed
  bob against its weight and decide whether it must sit inside the blade shell. Pivot friction and bearing losses; Coriolis (in-plane
  motion: no work, but compute its share of the rod tension); the parametric term (g/L)θ sin Ωt, whose size relative to the centrifugal
  stiffness is 1/Γ with Γ = r_pΩ²/g = 1.4–215 (not small on the slowest rotors).

### 4.3 The power theorem (derive it before any chaos claim)

If the pivot is shaken along a unit vector e with white-noise acceleration of intensity S, every mass feels −m_i a(t) e, and the
generalised force is −a(t) b(q) with b_k = Σ m_i e·∂x_i/∂q_k. The noise enters only the momentum equation with a coefficient
independent of the momenta, so Itô and Stratonovich agree, and Itô's rule on the kinetic energy gives the mean injected power
P_in = (S/2)⟨b^T M(q)⁻¹ b⟩, whatever the stiffness, damping, gravity, nonlinearity or chaos. The effective mass b^T M⁻¹ b is a
mass-weighted projection, so it never exceeds the total mass, and a pendulum chain reaches that bound only when every rod is
perpendicular to e. **No dynamics, chaotic or not, draws more mean power from white noise than (S/2)·M_total, and chaotic wandering
can only lower ⟨m_eff⟩.** Prove it in SymPy for the single and double pendulum, and check it by Monte Carlo (Euler–Maruyama
ensembles, small and large swings: dissipated power = (S/2)⟨m_eff⟩ within 3 %). Chaos can matter only for coloured forcing, where the
absorbed power is ∫ S_a(ω) Re Y(ω) dω with Y the effective mobility (for a chaotic system, its linear response in Ruelle's sense). The
precise form of the idea is therefore: does the double pendulum's broadband response overlap a narrow, wandering forcing spectrum (the
fixed blade mode against the moving Ω√R) better than a tuned single pendulum, at equal mass, reach and best damping?

### 4.4 Method rules for this study

- Lagrangian mechanics with the rotor angle φ(t) left free, so the Euler terms of a changing rotor speed come out of the derivation,
  not bolted on; the generator as Rayleigh's dissipation function with dE/dt = −2F (plus the rotor's input) as the energy book.
- Symplectic or energy-checked integration, with the time step from the fastest timescale and a convergence test (observed order).
- Chaos is a claim about ensembles: largest Lyapunov exponents over many initial conditions, with spreads, as a map over (G, R, κ).
  Never one trajectory.
- Wind noise has a source (IEC turbulence model), an amplitude, a correlation time or spectrum (Ornstein–Uhlenbeck or Kaimal), and
  results are ensembles with standard errors and seeds.

---

## 5. The ladder (one effect per level, each justified by a computed number)

- **L0, single pendulum, uniform rotation, small swing, gravity drive.** Lagrangian, Rayleigh dissipation, linear response P(κ), its
  optimum, order tuning in blade-angle time. Analytic. Reproduce Sol's formula and his 57.1 mW. (Started: `derive/L0_single.py`.)
- **L1, nonlinear single and double pendulum, uniform rotation.** Full equations by two routes (SymPy and Wolfram), Lyapunov maps over
  (G, R, κ): where is the double pendulum chaotic and where regular? Reproduce the ratio 0.64–0.74.
- **L2, rotor speed from turbulent wind.** Wind as Ornstein–Uhlenbeck or Kaimal synthesis with IEC parameters; a one-state rotor
  J Ω̇ = Q_aero(v, Ω) − kΩ² with a cited C_p(λ) and control constant; the Euler terms in the Lagrangian. Ensembles of 10-minute
  records. Expected small (order tuning): show by how much.
- **L3, blade in-plane vibration.** One edgewise modal degree of freedom (frequency, modal mass, damping from the reference turbine),
  forced by gravity and rotationally sampled turbulence, carrying the pivot, with the pendulum's reaction on the blade. The power
  theorem as the bound. Single (tuned at mean Ω), double regular and double chaotic, each at its best damping: the main test.
- **L4, the generator as an electrical machine.** EMF constant, coil resistance and load give the Rayleigh function and the efficiency,
  replacing the old assumed 50 % conversion; only if L3 leaves a result worth converting.

A level whose effect is below the observables' uncertainty does not enter; it stays as a check. No level is skipped.

---

## 6. Predictions that could come out wrong (into the contracts before computing)

- Rotor-speed turbulence (L2) changes the single pendulum's mean power by less than 1 %, because of order tuning.
- Under L3 forcing, with Ω wandering by the IEC amount, the double pendulum in its chaotic regime delivers a higher 5 % quantile of
  10-minute power than the best tuned single pendulum of equal mass and reach. **If the ensemble says otherwise by more than two
  standard errors, the claim is dropped and the page says so, with the physics.** That outcome is as publishable as the other.
- No configuration exceeds the power theorem's bound for the white-noise part of the forcing.

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

Everything in physics-model-loop section 8, and: "chaos helps" claimed from one trajectory or without the power theorem; a resonance
used that no real mounting reaches; constant rotor speed assumed under turbulent wind without its number; an assumed conversion
efficiency; an exposed bob at 50 m/s with its drag ignored; the parametric term dropped where 1/Γ is not small; noise without source,
amplitude and spectrum; a mean without its spread.

## 9. The finished study

The standard of `physics-simulation-study`; the reference is `portfolios-src/hydraulics/` (open it). Source in
`portfolios-src/rotor-pendula/`: the model in one physics block that Node can run; a textbook deriving every equation the integrator
uses (Picture, Working, Check and "On our blade" boxes; numbered equations; motivation from everyday experience first: a child on a
swing in a turning carousel, a cup of coffee carried on a bumpy bus); a simulation page; worked problems; a number script; independent
Python checks (constants retyped, SciPy re-integration, SymPy derivations); a browser check at 360, 390, 1024 and 1440 px. The served
copy keeps its address, is generated by the build script, and keeps Sol's report and delivery. The old bundle stays served until the
new one passes every gate. House design and interaction rules: `CLAUDE.md`.

## 10. First actions

1. Write `done.md` (section 3), set the goal (1.1), write `status.md` with the Fermi estimates.
2. Launch two scouts (sonnet), unless their dossiers already exist: the reference turbine (Jonkman et al. 2009: rotor inertia, edgewise
   mode, C_p curve, control law; IEC 61400-1 turbulence model); nonlinear and chaotic energy harvesting under random excitation
   (Halvorsen 2008 on broadband random vibration; reviews of bistable and pendulum harvesters; centrifugal pendulum absorbers on blades).
3. While they read, check `derive/L0_single.py`, derive and check the power theorem (4.3), write contract L0 and send it to a blind
   skeptic.

## 11. Talking to Numa

A one-line progress message at each gate, each finished level and each subagent return. Connected prose, metric units, terms
defined at first use. Mark facts (with a source he can open), inferences and opinions. When one of his ideas fails the method, say so
once with the physics and build the honest version. At a stop: "Where we are:" and "Next, if you say yes:", one sentence each.
