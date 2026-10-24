# Fig. 11 · Double Pendulum under Control

| | |
|---|---|
| Page | [public/simulations/pendulum-control.html](../../public/simulations/pendulum-control.html) (about 1 350 lines) |
| Walkthrough | [public/scripts/walk/pendcontrol.js](../../public/scripts/walk/pendcontrol.js) (147 lines, 9 steps, key `pendcontrol`) |
| Thumbnail | [public/images/sims/pendulum-control.webp](../../public/images/sims/pendulum-control.webp) (WebP, 800 × 500 px, 14 kB) |
| Catalog entry | [public/scripts/catalog.js#L217](../../public/scripts/catalog.js#L217-L234) (`id: 'pendulum-control'`, `fig: 11`, `field: 'control'`, `stage: 2`) |
| Translations | `public/de/simulations/pendulum-control.html`, `public/ar/simulations/pendulum-control.html`, written by `tools/i18n/build.py` from `i18n/<lang>/simulations__pendulum-control.html.json` |

**The aim of the page:** the cart, and only the cart, brings the double pendulum back to equilibrium. A double pendulum
hangs from a fixed pivot. A strut of two sliding tubes with a spring inside ties its lower ball to a cart on a rail, and the
moving coil of Fig. 9 pushes the cart. The reader switches the controller on (Off, Gentle, Firm), chooses where the cart
should rest (the target `r`, a slider or a flag on the ruler), grabs a ball or the cart, pulls it anywhere and lets go; the
controller, which can push only the cart, brings the whole chain back to rest. As in Figs. 9 and 10, the whole run is solved
first with RK4 and stored; each frame draws one stored row.

In this page, a link such as [L572](../../public/simulations/pendulum-control.html#L572) points to a line of
`pendulum-control.html`. Other files are named in the link text.

## The physics in one picture

**What you would see.** A crane driver steadying a load on a hook moves only the trolley. Here the trolley is the cart, the
hook and the load are the two balls, and the cable is the strut: it pulls along its own line and nothing else.

**The model** (lecture note §2–§4). Generalised coordinates `q = (θ1, θ2, X)`: the two absolute angles from straight down
and the cart's position. Three holonomic constraints (two rods, the rail) leave three degrees of freedom from six. The strut
is a massless two-force member: it adds no coordinate, only the potential `½ ks (ℓ − L0)²`, and two unilateral constraints,
its stops at `ℓmin = 0.5 m` (tubes pushed together) and `ℓmax = 0.95 m` (collar at the stop). The Lagrangian (2)–(4) with the
coil's term `κ X q̇e` gives `M(q) q̈ + C q̇ + ∇V = (0, 0, F)`, (5). The coil is driven by a current source, `F = κ I`,
`κ = 10 N/A`, limited to `|I| ≤ Imax` (3 A by default, so 30 N).

**The key physics** (§6–§7). Linearised about the hanging rest, the strut's spring stiffness drops out; only its pull at rest
`N0` couples cart and chain, through the "guitar string" term `½ (N0/ℓ0)(l1 θ1 + l2 θ2 − X)²`. With `N0 = 0` the
controllability rank falls from 6 to 2. A strut that pushes (`N0 < 0`) makes the hanging rest unstable on its own.

**The controller** (§8). Full-state feedback `F = F* − K(y − y*)`, clamped to `±κ Imax`, with `K` from LQR: the Riccati
equation (13) solved by the sign function of the Hamiltonian matrix, `K = ρ⁻¹ Bᵀ P`. A PD loop on the cart alone was measured
and rejected in the note: its best slowest decay is 0.009 1/s against LQR's 0.60 1/s.

## Numbers, measured (24 October 2026)

| Quantity | Value | How it was obtained |
|---|---|---|
| Free frequencies at the hanging rest, defaults | 1.71, 5.05, 10.00 rad/s | SymPy/SciPy generalised eigenproblem of (8); the page's `eig()` of `A` agrees |
| Rest for `r = 0.30 m` | θ1* = 5.78°, θ2* = 8.36°, ℓ* = 0.681 m, N* = 6.12 N, F* = 1.59 N | `equilibrium()`, checked against a Python Newton solve |
| Gains, defaults | K = (19.22, −201.70, 120.09, 0.04, 0.52, 22.14) | `lqr()`; SciPy `solve_continuous_are` gives the same |
| Closed-loop eigenvalues, defaults | −14.98, −1.83 ± 6.58i, −1.19 ± 11.65i, −1.13 1/s | `eig()` of `A − BK` |
| Region of attraction, sampled | 43 of 43 admissible starts settle within 0.01; median 5.7 s, 90 % within 7.9 s | Node sweep with the page's core, targets −0.4 … 0.4 m, rods up to ±60°, cart up to 0.8 m off |
| RK4 vs half step | ~1e−11 from rest, ~4e−10 after a drag, ~3e−6 when the coil saturates | `err_half`, measured in headless Chromium |
| Energy book at the end | ~3e−11 to 7e−10 J | `balance` |
| Solve time | ~250 ms (two runs, h and h/2) | `solve_ms`, headless Chromium on this machine |

## Function map

| Lines | Function | What it does |
|---|---|---|
| [L442](../../public/simulations/pendulum-control.html#L442) | `ds` | the store: parameters, the rig's constants, rest and controller, start, solver, stored run (dimension `n`, 1501 rows), playback and drawing |
| [L565](../../public/simulations/pendulum-control.html#L565) | `rig()` | the parameters of one run, read from the sliders at the moment of solving; `L0 = ℓ0 − N0/ks`, `Fmax = κ Imax` |
| [L572](../../public/simulations/pendulum-control.html#L572) | `strut()` | ball 2, the strut's length ℓ, ℓ̇, ∂ℓ/∂q and its pull N (spring plus a touched stop) |
| [L582](../../public/simulations/pendulum-control.html#L582) | `accel()` | (5) solved for q̈: Cramer's rule on the 2 × 2 pendulum block, one division for the cart |
| [L591](../../public/simulations/pendulum-control.html#L591) | `energy()` | T + V of (2) and (3), with a touched stop's elastic energy |
| [L599](../../public/simulations/pendulum-control.html#L599) | `equilibrium()` | the rest at X = r, (7), by Newton's method; its holding force F* |
| [L626](../../public/simulations/pendulum-control.html#L626) | `linearise()` | A and B of (9) by central differences of the full equations |
| [L633](../../public/simulations/pendulum-control.html#L633) | `lqr()` | (13)–(14) by the matrix sign function |
| [L655](../../public/simulations/pendulum-control.html#L655) | `eig()` | eigenvalues: Faddeev–LeVerrier polynomial, Durand–Kerner roots |
| [L676](../../public/simulations/pendulum-control.html#L676) | `rankOf()` | rank of the controllability matrix (10) |
| [L690](../../public/simulations/pendulum-control.html#L690) | `design()` | rest, linear model, gains, open and closed eigenvalues, rank |
| [L696](../../public/simulations/pendulum-control.html#L696) | `control()` | (11): `F* − K(y − y*)`, clamped; 0 with the controller off |
| [L703](../../public/simulations/pendulum-control.html#L703) | `stepRK4()` | one RK4 step of the closed loop; the coil's work and the stops' heat ride along |
| [L717](../../public/simulations/pendulum-control.html#L717) | `run()` | the whole 30 s, handing every `every`-th state to a callback |
| [L728](../../public/simulations/pendulum-control.html#L728) | `solve(from)` | design, solve at h, store, solve again at h/2 for the error, settle time, books, scales |
| [L831](../../public/simulations/pendulum-control.html#L831) | `geom()` | the rig's scale (px/m) and the chart areas |
| [L852](../../public/simulations/pendulum-control.html#L852) | `drawRig()` | pivot, pale rest pose, magnet, rail, cart and coil, strut (two tubes and the stop), rods and balls, force arrows, ruler and flag, energy bars |
| [L941](../../public/simulations/pendulum-control.html#L941), [L950](../../public/simulations/pendulum-control.html#L950) | `chartGeom()`, `drawChart()` | the 10 s window chart of θ1, θ2, X and the strip of the whole run (coil at its limit, strut at a stop) |
| [L1000](../../public/simulations/pendulum-control.html#L1000) | `drawForces()` | F, F*, ±κ Imax and N over the run |
| [L1039](../../public/simulations/pendulum-control.html#L1039) | `drawPhase()` | the three phase-space shadows with the fixed point and the state now |
| [L1080](../../public/simulations/pendulum-control.html#L1080) | `frame()` | copies the stored sample nearest to the playback time into the `*_now` values |
| [L1106](../../public/simulations/pendulum-control.html#L1106) | `pose()` | the hand: ball 1 turns the upper rod, ball 2 bends both rods (two-link inverse kinematics), the cart slides; poses beyond the stops are refused |
| [L1127](../../public/simulations/pendulum-control.html#L1127) | `holdState()` | while held: the clock stops, the controller's force for the held pose is shown, nothing is stored |
| [L1158](../../public/simulations/pendulum-control.html#L1158) | `release()` | solve a new run from the released pose and the hand's smoothed speeds (about 50 ms) |
| [L1208](../../public/simulations/pendulum-control.html#L1208) | `Sim.data` | the data panel's hooks |

## The store and its checks

Groups (in the panel's order): Parameters, The rig, Rest and controller, Start of the run, Solver, Stored run, Playback,
Drawing. Every derived scalar and every array has a check that recomputes it from stored inputs only:

- the stored state arrays (`th1`, `th2`, `Xs`, `w1`, `w2`, `vX`) and the work and heat integrals (`Wc`, `Qs`) by rerunning the
  same RK4 from the stored start `y0s` to sample n (`replay()`, [L1180](../../public/simulations/pendulum-control.html#L1180));
- `Fs`, `Is`, `Ns`, `ells`, `Es` from the stored state at row n with the page's pure functions;
- the rest, the gains, the eigenvalues and the rank by redesigning from the stored parameters (`storedDesign()`,
  [L1179](../../public/simulations/pendulum-control.html#L1179));
- `err_half` by solving the run again with h/2; `t_settle`, `t_sat`, `t_stop`, the chart scales and `E_rest` from the stored arrays;
- the `*_now` values against the stored arrays at `i_now` (or as "set by your hand" while a ball or the cart is held).

Read-backs from the picture (alpha before colour): ball 1 and ball 2 (burgundy fill), the cart under its hinge, the target
flag, the coil-force arrow, and θ1, θ2, X on the window chart (`ok: null` for samples outside the 10 s window). Measured on
24 October 2026 at 1400 px: 152 checks agree to 10⁻⁹ relative, 8 read-backs find ink, none differ.

One recorded round is two seconds of the stored run (`t_play`, sampled), blocked in the last two seconds. What the drawing
leaves out of the store is listed in `about`: the tubes, stop marker, wheels, magnet and coil are schematic, the outer tube is
drawn 0.5 m long and the inner tube fills the rest.
