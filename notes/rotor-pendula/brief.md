# Prompt for the rotor agent: Double pendula on turbine blades, chaos against chaotic wind

Paste everything below the line into a fresh Claude Code session on `Numa1997/SiteTest` (or follow it in the session that wrote it).

---

Load the skills `physics-model-loop`, `physics-simulation-study` and `phyein-usul-physics-content` before anything else, and
follow them. The loop and its three gates are the method of this task; this prompt only gives the study. Also use `sympy`,
`wolfram-language`, `theoretical-physicist`, `unslop` and `verification-before-completion` where the loop says so. Read
`CLAUDE.md` and `AGENTS.md`.

## 0. The ground, as of 23 October 2026

- The Rotor Pendula portfolio is Sol's corrected study of a pendulum hung from a point on a turning wind-turbine blade, braked by
  a generator at its pivot, as a power supply for a blade sensor. Its AppDeploy app is gone (0 apps; source unreadable). Do not use
  AppDeploy at all.
- What survives is in this repository: the built copy served at `public/portfolios/rotor-pendula/` (with Sol's report and the 181
  files of his delivery), and its text recovered as HTML with TeX in `notes/rotor-pendula/baseline/` (overview, theory, results,
  simulate, checks, report). `notes/rotor-pendula/skeptic-baseline-r1.md` is a blind audit of that old version.
- **Start afresh** with a new question (section 1). Sol's results are the reference at uniform rotation: the linear optimum
  κ = |R − 1| with P* = M L g² / (4 Ω |r_p − L|), the 18 mountings giving 9.55–57.1 mW, the double-to-single ratio 0.64–0.74 at equal
  mass and reach, the rotor's share ≤ 7.2 × 10⁻⁵. Reproduce them, or explain on the page why they change. Sol's report stays word
  for word.
- Another agent works in the same repository at the same time on the Droplet Collection portfolio. Section 6 says which files are
  yours.

## 1. The question and the observables

Wind is turbulent. Can a pendulum on a blade, and in particular a double pendulum whose motion is chaotic, turn that randomness to
its advantage: harvest more, or more reliably, than a single pendulum of the same mass and reach? Who pays for the energy, and what
does the pendulum do to the blade?

Observables, each with its uncertainty over a stated ensemble of 10-minute turbulent wind records (the averaging time of IEC
61400-1):
1. Mean electrical power P̄ delivered to the load.
2. Reliability: the 5 % quantile of the 10-minute mean power, and the fraction of 10-minute periods that cover the sensor node's need
   (37.6 µW in the old study; re-derive it from the two datasheets).
3. The cost: the share of the rotor's power, and the change in the blade's in-plane vibration amplitude (a pendulum is also a
   vibration absorber).

Before any model, write a Fermi estimate of observable 1 for each energy source in section 2 and keep it on the first page of
`notes/rotor-pendula/status.md`.

## 2. Scales and dominant balance (computed on 23 October 2026 for the old study's 18 mountings: M = 0.1 kg, L = 0.2 m, tip-speed ratio 7, wind 8 m/s; recompute)

- **Order tuning.** For the single pendulum, θ̈ + γθ̇ + (r_p/L) Ω² sin θ + (g/L) cos(Ωt + θ) = 0 at uniform rotation. Its own frequency is
  Ω√R with R = r_p/L, and gravity pushes once per turn, at Ω. Both scale with Ω, so a slow change of rotor speed does not detune the
  pendulum from gravity's push. In blade-angle time the equation depends only on R, G = g/(Ω²L), κ = c/(ML²Ω) and ε = Ω̇/Ω².
- **Far from resonance.** Across the 18 mountings R runs from 2.0 to 301, so the pendulum's own frequency (1.3–16 Hz) lies 1.4 to 17
  times above the once-per-turn push (0.13–6.7 Hz). Sol's resonance at r_p = L would put the pivot 20 cm from the hub.
- **Where the wind's randomness can enter.** (a) Rotor speed: low-pass filtered by the rotor's inertia (compute its time constant and
  ε for a cited reference turbine); order tuning predicts little effect; test it. (b) Blade in-plane (edgewise) vibration, excited by
  gravity once per turn and by rotationally sampled turbulence: on the large rotors the pendulum's own frequency (1.3–3.7 Hz) lies in
  the band of the first edgewise blade modes (about 1.1 Hz for the NREL 5-MW blade; read Jonkman et al. 2009, NREL/TP-500-38060).
  The blade's mode has a fixed frequency while the pendulum's moves with Ω: a tuned single pendulum detunes as the wind changes
  the rotor speed. This is where a broadband, chaotic harvester could win. (c) Turbulence intensity: IEC class A at 8 m/s gives
  σ_u = 1.86 m/s, I = 0.23; Kaimal length scale 340 m, integral time 42.5 s (verify from the standard).
- **Upper bound from gravity alone.** A bob held hanging while the blade turns round it takes torque at most M g L at relative speed Ω:
  164–411 mW on the large rotors. Any harvest from gravity is below this.
- **Dropped terms need their numbers.** The blade carries the pivot through the air at r_p Ω = 17–50 m/s: compute the drag on an
  exposed bob against its weight and decide whether it must sit inside the blade shell. Pivot friction, bearing losses, Coriolis
  (in-plane motion: no work, but compute its share of the rod tension).

## 3. The power theorem (derive it before any chaos claim)

For a mechanical system driven by an additive white-noise force, the mean power injected is fixed by the noise intensity and the mass
matrix alone (Itô calculus on the kinetic energy): stiffness, damping, nonlinearity and chaos cannot change it. So **no dynamics,
chaotic or not, draws more mean power from white noise.** Derive it, check it in SymPy and in a simulation, and state it on the page.
Chaos can matter only for coloured forcing, where the absorbed power is ∫ S_F(ω) Re Y(ω) dω with Y the system's mobility (for a
chaotic system, its linear response in the sense of Ruelle). The precise form of the idea is therefore: does the double pendulum's
broadband response overlap a wandering, narrow forcing spectrum (the blade mode against the moving Ω√R) better than a tuned
single pendulum does, at equal mass, reach and best damping? For multiplicative noise (the Euler term carries cos θ), state Itô or
Stratonovich and why.

## 4. The ladder (one effect per level, each justified by a computed number)

- **L0, single pendulum, uniform rotation, small swing, gravity drive.** Lagrangian, Rayleigh dissipation F = ½cθ̇² with dE/dt = −2F
  as the energy book, the linear response, P(κ), its optimum, order tuning in blade-angle time. Analytic. Reproduce Sol's formula and
  his 57.1 mW.
- **L1, nonlinear single and double pendulum, uniform rotation.** Full equations from the Lagrangian (SymPy and Wolfram, two routes),
  a symplectic or energy-checked integrator with a convergence test, the largest Lyapunov exponent over an ensemble of initial
  conditions as a map over (G, R, κ): where is the double pendulum chaotic and where regular? Reproduce the ratio 0.64–0.74.
- **L2, rotor speed from turbulent wind.** Wind as an Ornstein–Uhlenbeck process or a Kaimal-spectrum synthesis with the IEC
  parameters; a one-state rotor J Ω̇ = Q_aero(v, Ω) − Q_gen(Ω) with a cited C_p(λ) and the usual below-rated control Q_gen = kΩ²; the
  Euler terms Ω̇ in the Lagrangian. Ensembles of 10-minute records. Expected small (order tuning): show by how much.
- **L3, blade in-plane vibration.** One edgewise modal degree of freedom (frequency, modal mass and damping from the reference
  turbine), forced by gravity and by rotationally sampled turbulence, carrying the pivot, with the pendulum's reaction on the blade.
  The power theorem as the bound. Single (tuned at mean Ω), double regular and double chaotic, each at its best damping: this is the
  main test of the study.
- **L4, the generator as an electrical machine.** EMF constant, coil resistance and load give the Rayleigh function and the
  efficiency, replacing the old study's assumed 50 % conversion; only if L3 leaves a result worth converting.

A level whose effect is smaller than the uncertainty of the observables does not enter; it stays as a stated check.

## 5. Predictions that could come out wrong (into the contracts before computing)

- Rotor-speed turbulence (L2) changes the single pendulum's mean power by less than 1 %, because of order tuning.
- Under L3 forcing with Ω wandering by the IEC amount, the double pendulum in its chaotic regime delivers a higher 5 % quantile of
  10-minute power than the best tuned single pendulum of equal mass and reach. **If the ensemble says otherwise by more than two
  standard errors, the claim is dropped and the page says so, with the physics.** That outcome is as publishable as the other.
- No configuration exceeds the power theorem's bound for the white-noise part of the forcing.

## 6. Files, branch and the other agent

- Yours: `notes/rotor-pendula/` (`done.md`, `status.md`, contracts, dossiers, reports), `portfolios-src/rotor-pendula/`,
  `public/portfolios/rotor-pendula/` (generated by the build script; keep Sol's report and delivery files).
- Not yours: anything about droplets (`notes/droplets/` except reading, `portfolios-src/droplets/`,
  `public/portfolios/droplet-collection/`), the ten simulation pages and their notes.
- Shared: `public/portfolios.html` (edit only the `rotor-pendula` article), `docs/portfolios.md` (only its rotor sections),
  `docs/files.md` (regenerated by `python3 tools/inventory.py`). Before each commit: `git fetch origin` and look at what changed.
  If a conflict or a failing build comes from the other agent's work, stop, note it under "Decisions for Numa", and let it finish.
- Branch `claude/awesome-ritchie-qiy1zo`. Push it; open a pull request into `main` at the end; never merge. Never touch Cloudflare
  or any connector.
- Default in force (a decision for Numa): the portfolio becomes two parts, Sol's uniform-rotation study (Part I, reproduced and
  checked) and the turbulent-wind study (Part II, new).

## 7. The goal line

```
/goal Rotor Pendula is complete when every item of notes/rotor-pendula/done.md is ticked with its evidence printed in this
conversation: all check scripts print PASS; the skeptic's final report passes all six thresholds of physics-model-loop section 7.3;
the browser check passes at 360, 390, 1024 and 1440 px; the pull request into main is open and NOT merged;
notes/rotor-pendula/status.md has no open item except "Decisions for Numa". Never merge, never touch Cloudflare or AppDeploy, never
edit droplet files. Or stop after 200 turns and report where things stand.
```

## 8. First three actions

1. Rewrite `notes/rotor-pendula/status.md` for this question, with the Fermi estimates of section 2.
2. Launch two scouts (sonnet): one on the reference turbine (Jonkman et al. 2009: rotor inertia, edgewise mode, C_p curve, control law;
   IEC 61400-1 turbulence model), one on nonlinear and chaotic energy harvesting under random excitation (Halvorsen 2008 on
   broadband random vibration; reviews of bistable and pendulum harvesters; centrifugal pendulum absorbers on blades).
3. While they read, derive L0 and the power theorem yourself, check both in SymPy, write contract L0 and send it to a blind skeptic.
