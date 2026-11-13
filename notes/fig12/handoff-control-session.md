# Brief for a new session: the Guinness cart WITH control, computed on Kaggle's GPU

Written 13 November 2026 by the session that built the page "A pint of Guinness on a one-wheel cart, computed on Kaggle"
(Fig. 12 on Kaggle). You are a new session. Everything you need is in this brief and in the repository; you cannot ask the old
session. Read this whole brief first, then `CLAUDE.md`, `AGENTS.md`, `docs/simulations/fig12-beer-slosh.md`,
`docs/kaggle-pipeline.md`, `docs/usul.md`, and the lecture notes of `public/simulations/beer-slosh.html` and
`public/simulations/guinness-kaggle.html`.

Marks used below: **Fact** (measured or read, with a handle), **Inference**, **Opinion**, **Open** (not known; find out).

---

## 0. The one aim

The user, 13 November 2026: "The whole point of this project is to control the Guinness while coming up on top of the bumps."

Produce a **working animation on the live site** (<https://phyeinusul.com/simulations/guinness-kaggle>) that plays rides
computed on the Kaggle GPU **with the controller inside the loop**, beside the rides without control that already exist:
same road, same speed, with and without control, so a visitor sees the stout stay flat when the controller works.

The physics the user stated and you must respect: control cannot be painted onto stored rides afterwards. The controller
changes the cart's push at every instant, the stout answers, the cart feels the stout back. It is one coupled system; each
controlled ride is a new solution with the controller running inside the cart loop of the GPU solver.

The route the user asked for, in this order:
1. **Derive and check** the model and the controllers exactly (Wolfram: the Wolfram connector and the skills
   `wolfram-language`, `wolfram-physics`; SymPy for the algebra you keep in the repository).
2. **Implement in Python with JAX on Kaggle's GPU** (skill `jax-differentiable-physics`, `kaggle-gpu-run`).
3. **Pipeline** between Kaggle and the website (`docs/kaggle-pipeline.md`, the Worker `kaggle-bridge`).
4. **A working animation**, live, tested in a real browser.

---

## 1. The user and how to work with them

- Call them "the user". Never write their name in anything sent outside. They hold a BSc in physics (computational and
  theoretical). Define each term at first use. Metric units only. Short sentences, everyday words, no marketing words.
- Mark Fact / Inference / Opinion. Give a handle on every claim (file and line, link, or a command they could run).
- No tables in chat. At most about 12 lines per message. One decision at a time, and only real ones.
- The user's yes is needed only for: **a GPU budget** (one budget, one yes, with the arithmetic cells x steps x time per
  cell-step, minutes, share of the weekly 30 h), **deploying code to the Worker `kaggle-bridge`**, and **spending money**.
  Building, testing, committing, merging to `main` and publishing need no yes. Do not put options in front of the user for
  things already decided. Do not ask physics questions: the physics chapter is closed (section 4).
- Before any computation over a minute: one plain line on what the machine does, then the time arithmetic. A progress line at
  least every 10 minutes. Afterwards: predicted beside measured.
- End every message with `Where we are:` (one sentence) and `Next, if you say yes:` (one sentence).
- When the user is angry: shrink the turn, state where things stand in one line, fix the problem. No apology floods.
- Never send messages to other sessions. Relays from the user's coordinating chat are one-way; do not reply to them.
- Never ask for, print, log or store the Kaggle token. Kaggle notebooks stay private.
- Commit trailers: the ones your own session's system reminder gives you. No model names in code or commits.
- After file changes: `python3 tools/inventory.py` then `python3 tools/inventory.py --check`;
  `python3 tools/i18n/build.py --check`; `npm run build`; delete `package-lock.json`. A stop hook requires committing and
  pushing uncommitted work.

### The user's vision, the same for every project (keep as a checklist)

1. Every number the page shows is computed on Kaggle, on the GPU. The page computes nothing physical; it draws stored data in
   the house design (`docs/styles.md`).
2. The data lives in two places, named by the date of generation: on the site (`public/data/fig12/<YYYY-MM-DD>/`) and with
   its Kaggle notebook.
3. A data panel proves each value three ways: stored value, formula recomputed from stored inputs, pixel read back.
4. The controls show what is computed and what is not (solid band and filled dots against hatching and hollow dots).
5. Well before the edge of the computed data the control grows heavier and the animation slower, smoothly.
6. Past the edge a live preview from the browser, labelled as a preview, carries on while Kaggle computes the next block
   through the Cloudflare Worker `kaggle-bridge`.
7. When Kaggle's block arrives it cross-fades in at the same ride time. "Absolutely no discontinuities."
8. Only when the speed has reached zero does a pop-up appear, and it shows the pipeline.
9. A visitor who would over-use the GPU needs special access, granted the way the job site (Stellen) grants it.
10. No interpolation between runs. Lecture note to `notes/STANDARD.md`, docs that say what the code does, catalogue entry,
    tested in a real browser at 360, 390, 1024 and 1440 px.

---

## 2. Skills and access

Load the skill before the work it covers. Check each name against what your session lists; use only what exists.

- Agent loop: `orchestrating-agent-loops` (first, to size the task), `physics-model-loop`, `verification-before-completion`,
  `pushback-proof-answers`.
- Physics and maths: `physics-simulation-study`, `theoretical-fluids-and-pdes`, `theoretical-physicist`, `sympy`,
  `math-skill`, `socratic-physics` (to attack your own model), `feynman-technique` (for the note).
- Wolfram: `wolfram-language`, `wolfram-physics`, `wolfram-modelica-build`, `wolfram-modelica-analyze`, and the Wolfram
  connector (`mcp__Wolfram__WolframLanguageEvaluator`, `WolframAlpha`).
- Control: `phyein-usul-first-principles-control`.
- Numerics: `jax-differentiable-physics`, `kaggle-gpu-run`, `physics-simulation-toolchain`, `openfoam-cfd` (the witness runs),
  `fem-multiphysics` only if needed.
- The site: `phyein-usul-data-panel`, `phyein-usul-bookkeeper`, `phyein-usul-physics-content`, `phyein-usul-smooth-site`,
  `phyein-usul-i18n`, `tune-with-numa` (anything judged by eye).
- Cloudflare: `wrangler`, `cf-cli`; the Cloudflare connector. Web: `web-tool-ladder`.
- Repository agents (`.claude/agents`): `physics-teacher`, `derivation-checker`, `referee`, `walkthrough-keeper`.

Access needed: GitHub repository `Numa1997/SiteTest` (push to a working branch, merge to `main`); the Kaggle connector
(`mcp__Kaggle__*`); Cloudflare (read; **any deploy to `kaggle-bridge` needs the user's yes, shown the exact code and what it
can spend; never touch the Workers `phyein-usul` or `stellenrecherche`**); Wolfram.

---

## 3. What exists (do not redo)

**Live page**: `public/simulations/guinness-kaggle.html` with `public/scripts/guinness-playback.js` (playback, store, data
panel hooks, phase space of the first sloshing mode), `guinness-preview-worker.js` (the labelled live preview, the site's
coarse solver in a Web Worker), `kaggle-flow.js` + `kaggle-flow.css` (the shared speed control: solid and hatched parts,
heavier near the edge, governor slow-down, cross-fade, pop-up only at zero speed), `stout-view.js` (the 3D pint drawing),
`guinness-glass.js` (the glass profile R(z), 296 radii every 0.5 mm, rim at 147.5 mm). Catalogue card in `catalog.js`,
three languages. Lecture note inside the page (`<article class="paper">`), refereed and derivation-checked.

**Stored data**:
- `public/data/fig12/2026-11-12/rides.json`: solver v1, **over-damped**, kept for the record. Also there:
  `free_swing_v2.json`, `free_swing_v2_repair.json` (tests of solver v2), all in `index.json` with SHA-256.
- `public/data/fig12/2026-11-13/`: the three rides without the slosh controller, solver v2 (see its `index.json` for
  notebook version, commit, measured times). **These are your baseline.**
- Format of `rides.json`: `{fill, nr: 16, nth: 64, q: 0.0002, fps: 30, ml, rides: [...]}`; each ride
  `{road, v0, n, x[], v[], zb[], zw[], lean[] (mm), spill[] (g), road_x0, road_dx, road_zr[], frames}`; `frames` is
  base64 of zlib of uint8 `[n][17][64]`, surface height = `fill + (byte - 128) * q` on the polar grid r = R(fill) i_r/16,
  theta = 2 pi j/64.

**GPU code** (`tools/fig12/kaggle/`): `solver.py` (Taichi 1.7.4 solver v2 and the cart, the function `run`), `rides.py`,
`free_params.py`, `env.py`, `free_swing.py`, `free_swing_fit.py`, `store_rides.py`. Analysis: `tools/fig12/kaggle_decay.py`
(direct least-squares decay fit; `--selftest`), `tools/fig12/cart_damping.cjs` (the cart's own damping, reduced model).

**Kaggle notebooks** (private, user `numakoudsie`): `guinness-on-a-cart-stout-sloshing` (the rides; version 3 = solver v1,
version 5 = solver v2) and `guinness-free-swing-v2` (versions 4 and 5 = the free-swing tests).

**Witness runs**: OpenFOAM cases on branch `origin/ccr-76841c15-le08bl`, `notes/fig12/of-runs/` and
`tools/fig12/of/analyse_swing.py`. Not converged (the slip and no-slip pairs had different time steps).

---

## 4. The physics. The chapter is closed: use this model, bring no new one

The model is the one in the Fig. 12 lecture note (`beer-slosh.html`) and `docs/simulations/fig12-beer-slosh.md`. Do not
propose new foam or friction models and do not ask the user physics questions. Your job is to **reproduce** it and to
**control** it. Check every formula below with Wolfram or SymPy before you use it; where this brief and the note differ,
the note wins and you say so.

### 4.1 The stout (frame of the glass)

Incompressible Navier-Stokes with a free surface, in the accelerating frame of the glass:

    Du/Dt = -grad(p)/rho + nu lap(u) + g - a_g(t),     div(u) = 0,
    p = 0 on the free surface;  u.n = 0 on the wall r = R(z) and on the floor.

rho = 1007 kg/m^3 on Kaggle (the note's site model uses 1000), nu = 1.0e-6 m^2/s (the note's value), fill h = 0.125 m,
stout mass m_l = 0.4296 kg, radius at the fill R = 0.0391 m, narrowest radius 0.0277 m at z = 0.0305 m (the tulip's waist),
R(0) = 0.0163 m. a_g = (a_x, 0, a_z) is the glass's acceleration, which is the cart body's.

### 4.2 The first sloshing mode (what the controller fights)

Linear theory, upright cylinder of radius R, depth h, first antisymmetric mode, xi = 1.841184 (first zero of J1'):

    omega_11^2 = (g xi / R) tanh(xi h / R)   ->   omega_11 = 21.49 rad/s,  f_11 = 3.421 Hz.

Surface shape eta = q(t) J1(xi r/R)/J1(xi) cos(theta), q the height at the wall. Under a horizontal push the mode obeys a
driven oscillator (note eq. 17 and eqs. 54-55; coupling constant beta = 1.541 in the note's normalisation, **read it there**):

    q'' + 2 zeta omega_11 q' + omega_11^2 (1 + a_z/g) q = -(coupling) a_x .

Textbook value to check against the note: for a deep cylinder the wall height answers a steady a_x with the first mode's
share 2/(xi^2 - 1) = 0.837 of the full tilt R a_x/g. The heave a_z enters **parametrically** (it changes the stiffness), the
push a_x **additively**. Higher modes of the same family: 5.821 and 7.365 Hz. Breaking: the linear model fails when the wall
amplitude reaches g/omega^2 = 21.2 mm.

Damping (settled values):
- wall boundary layer (Stokes layer delta = sqrt(2 nu/omega) = 0.31 mm): logarithmic decrement
  Lambda = K nu^(1/2) R^(-3/4) g^(-1/4), K = 3.52 (laminar theory) or 5.23 (measured, NASA TN D-1367);
  zeta = Lambda/(2 pi) = **0.0036 to 0.0053**;
- the head of foam, from Sauret et al. (Phys. Fluids 27, 022103, 2015) scaled to the pint: **zeta_f = 0.019 to 0.037**
  (Fig. 12 note, section 14);
- the cart itself (speed loop and drag take energy from the swing): **zeta_cart = 0.0067 to 0.0074**
  (`node tools/fig12/cart_damping.cjs`, then `python3 tools/fig12/kaggle_decay.py --modal`).

### 4.3 The cart (the plant the controller acts on)

States x, z_b (body), z_w (wheel), their speeds, motor current i, active force u_s. Parameters (the dict `CART_COMMON` in
`tools/fig12/kaggle/solver.py`, a line-by-line port of `Cart` in `public/scripts/stout-cart.js`):

    M_b = 1.5 kg (body and glass), m_w = 0.3 kg, R_w = 0.04 m, I_w = 2.4e-4 kg m^2,
    spring k = 600 N/m, damper c = 8 N s/m, tyre k_t = 2e4 N/m, c_t = 5 N s/m, drag c_x = 2 N s/m, L_s = 0.135 m,
    gear N = 10, K_m = 0.02 N m/A, R_a = 2 ohm, J_m = 2e-6 kg m^2, V_max = 12 V, I_max = 3 A, tau_i = 2 ms,
    controller sample T_s = 1 ms, active force limit U_max = 40 N with lag tau_u = 5 ms, friction mu = 0.8.

    b = N K_m / R_w = 5 N/A                     (motor force per ampere)
    M_x = M_b + m_l + m_w + (I_w + N^2 J_m)/R_w^2 = 2.50 kg   (with a full glass)
    road: the axle of a rigid wheel follows the envelope z_a(x); tyre N = max(0, k_t (z_a - z_w) + c_t (z_a' x' - z_w'));
    M_x x'' = -N z_a'(x) + clip(b i, +-mu N) - c_x x' + F_x
    M_s z_b'' = F_S - M_s g + F_z,   m_w z_w'' = -F_S - m_w g + N,   M_s = M_b + m_l,
    F_S = -k (z_b - z_w - L_s) - c (z_b' - z_w') + u_s
    i follows the command with lag tau_i, clipped to +-I_max and to (+-V_max - K_m N x'/R_w)/R_a.

**The coupling** (the stout's push on the cart): F = -(dP/dt), P the stout's momentum relative to the glass, plus what
spills; handed over as an impulse per fluid step; the cart is sub-stepped at 0.1 ms inside each fluid step. The glass's
acceleration over the step, a_x = dv_x/dt and a_z = dv_zb/dt, drives the fluid in the next step.

### 4.4 The controllers that already exist on the site (port these first; invent nothing before that)

All in `Cart.sample` of `public/scripts/stout-cart.js` (about lines 1560 to 1625), documented in
`docs/simulations/fig12-beer-slosh.md` (sections "The live model and the controllers", "Part 1 ... control through sensors",
"Part B: motor and active suspension, one design") and in the Fig. 12 note sections 8.4 to 8.6:

1. `off`: i = c_x v_0 / b.
2. `speed` (PI): i = i_0 + K_p (v_0 - x') + K_i int(v_0 - x') dt, K_p = M_x omega_c / b = 25.18 A/(m/s),
   K_i = K_p omega_c / 4 = 316.4 A/m, omega_c = 2 pi 8 Hz; the integral stops while the current is limited.
   **This is what the stored rides use.** It holds the speed; it does not calm the stout.
3. `preview`: PI plus the feed-forward i_ff = (M_s + m_w) g z_a'(x + x' tau_i) / b (note eq. 50): cancel the road's push
   one current lag ahead. **Already in the Kaggle port** (`ctrl = 2` in `Cart.sample` of `solver.py`).
4. Skyhook suspension: u_s = -c_sky z_b', c_sky = 2 x 0.7 sqrt(k M_s) = 47.6 N s/m. **Already in the Kaggle port** (`susp`).
5. `slosh`: LQR on (delta v, q_1, q_1', xi) (note eqs. 51-53). Bryson weights 0.05 m/s, 2 mm, 2 mm x omega, 0.02 m, 3 A.
   Gains for the 3D plant K = (76.7, -1934, -41.3, -150); swing poles -11.3 +- 7.5j 1/s (damping ratio 0.83). It acts on an
   **estimate**: a Kalman filter (`Observer`) on z = (v, q, q') fed by the measured current, the speed every 1 ms and two
   height probes at the wall (theta = 0 and pi; y_q = (eta_front - eta_back)/2) once per fluid step; noise model
   W_F = 0.5 N^2 s, W_a = 0.002 m^2 s^-3, sigma_v = 2 mm/s, sigma_q = 0.8 mm; exact zero-order-hold discretisation,
   Van Loan Q_d, Joseph form. **Not yet ported to Kaggle.**
6. `joint` (Part B): the slosh LQR + the current that cancels the heave's parametric term,
   i_par = -M_x omega^2 (a_z/g) q / (beta b), + a suspension LQR K_s = (-502.6, 11.6, -6.1, 612.6) on
   (stroke, z_b', z_w', tyre compression). **Not yet ported.**

Measured on the site (browser solvers, one bump at 1 m/s): lean 24.7 / 7.6 / 0.8 / 0.4 mm for off / PI / preview / slosh
over a 10 mm bump; 73.9 (9.9 g spilled) / 25.4 / 5.9 / 1.3 mm over a 25 mm bump. With the 3D browser solver the slosh
feedback keeps the lean under 3.2 mm over the 25 mm bump (open loop 61, PI 35). These are your targets to reproduce.

Other control work on the site to read for method and for what the user accepts: `docs/simulations/fig11-pendulum-control.md`,
`fig11-double-inverted-pendulum.md`, `fig10-wind-turbine.md`, `fig09-driven-oscillator.md` and their pages.

**Controller rate against fluid step.** The controller samples every 1 ms, the fluid steps every 2 ms, the cart every
0.1 ms. The probes are read once per fluid step. Keep these three clocks exactly as the site has them, and store them.

---

## 5. Solver v2 on Kaggle: what it does, what it measures, where it falls short

Method (`tools/fig12/kaggle/solver.py`, class `Stout`, Taichi 1.7.4, float32, CUDA): APIC particles (8 per cell) on a
staggered grid; cut-cell face fractions for the curved glass (4 x 4 sub-samples per face); pressure by Jacobi-preconditioned
conjugate gradients (tolerance 1e-5 on the max norm, up to 600 iterations); free surface as a level set from the particles
(Zhu & Bridson 2005: phi = |x - xbar| - r, kernel radius 2 dx, r = 0.9 dx, with wall images), carried into the cells cut by
the glass; ghost-fluid pressure p = 0 on the surface itself (theta = phi_c/(phi_c - phi_n), floor 0.05); faces closed by the
glass are filled by extrapolation (free slip on the grid), only the flat floor holds w = 0; explicit viscosity; the wall's
Stokes layer as a drag rate gamma = sqrt(nu omega/2) x (wall area per cell volume) on the faces next to the glass; the foam
as a force per length of contact line Lambda(v) = Lambda_0 (|v|/0.1 m/s)^(-1/3), Lambda_0 = C rho/(2 k_S) = 0.260 kg/(m s)
(C = 2.35 cm/s, k_S = 45.5 /m), on the liquid within 2 dx of the surface next to the glass, speed floor 5 mm/s.

**Measured** (free swing: glass held still, one half-sine push of 1 m/s^2 for 0.146 s, 4.5 s of free swing;
`python3 tools/fig12/kaggle/free_swing_fit.py`):

    grid    no friction   wall only   wall + foam     frequency
    3 mm        -          0.014        0.036          3.22-3.28 Hz
    2 mm      0.025        0.015        0.024          3.25-3.31 Hz
    1.5 mm    0.023        0.015        0.018          3.29-3.33 Hz      (damping ratio zeta, ring 13)

- Solver v1 (the 12 November rides) gave zeta 0.10 to 0.14. **Cause found**: it held the velocity on faces closed by the
  glass at zero, a no-slip wall one cell thick; and it put p = 0 at the centre of the first air cell.
- Times on Kaggle's T4: 3 mm 45-60 ms a step (55,738 cells), 2 mm 71-75 ms (166,496), 1.5 mm 90-100 ms (370,386 cells,
  1,002,808 particles), about 165 pressure iterations a step at 1.5 mm. A 20 s ride (10,000 steps of 2 ms) takes 15 min.

**Shortcomings you inherit. State them wherever the data is shown.**
1. **Numerical damping.** With no friction at all the swing still dies at zeta about 0.015 to 0.025; the settled wall value
   is 0.0036 to 0.0053. So the solver's own loss is 3 to 5 times the wall's, and it is as large as the foam term.
2. **Scatter.** Runs that should differ only by the wall term differ by +-0.005. Another particle seed moved zeta from
   0.015-0.018 to 0.025.
3. **It is not a clean exponential.** Half the push gave zeta 0.011-0.016; the amplitude falls fast first and slowly later.
4. **A smaller time step made it worse**: dt = 1 ms gave 0.035 against 0.025 at 2 ms (more particle-grid transfers per swing).
5. **Frequency 3 % low** (3.29-3.33 Hz against 3.421), rising slowly with resolution.
6. **Energy books do not close.** The particles' potential energy drifts down by 0.1 to 3 mJ in 5 s while the swing holds
   about 0.13 mJ. The foam term mostly damps spurious small currents.
7. **Float32**, and the pressure tolerance is on the max norm.
8. The Stokes drag assumes the swing's own frequency (single-frequency form of the stress); on a road that forces other
   frequencies it is approximate.
9. The stored surface near the wall: rings beyond R - 3.5 dx are a straight extension along the radius, not data. The
   waist error of v1 (rings 11-12 eight millimetres low at rest) is fixed in `polar_surface_fixed`.

**What this means for control (Inference):** a controller that raises the swing's damping ratio to 0.3-0.8 is judged against
an uncontrolled zeta of about 0.02-0.03 (with the cart's 0.007). The solver's extra 0.015 flatters the uncontrolled ride a
little and matters little for the controlled one. Say this on the page in one sentence.

**Open, for your JAX solver:** reach a numerical loss below the wall's 0.005 on the free swing, with the frequency within
1 % of 3.421 Hz, and show both converge with the grid. Ideas the old session did not test (each is one GPU experiment):
a FLIP/APIC blend, more particles per cell near the surface, a tighter pressure tolerance and a proper preconditioner
(multigrid or incomplete Cholesky), float64 on the reductions, a purely grid-based level-set method with no particles.

---

## 6. The mistakes of the old session. Do not repeat them

1. **Lost a finished ride to a missing import.** `rides.py` used `base64` without importing it; 15 min of GPU computed
   ride 1, then the save crashed. Rule: run a name check on the exact concatenation Kaggle will execute before every launch
   (`python3 -m pyflakes`), and **write each result to disk the moment it exists**.
2. **A racing reduction.** `s = ti.max(s, ...)` inside a parallel loop is a data race on the GPU; the pressure solver
   stopped after about 10 iterations and the stout blew up. Use the framework's reductions (`ti.atomic_max`; in JAX,
   `jnp.max`).
3. **A read-only path on Kaggle**: `/kaggle/src` cannot be written; use `/tmp` or `/kaggle/working`.
4. **Wrong times told to the user.** A launch time was quoted from memory and was 6 min off; the user's clock is Berlin
   (UTC+1). Read the clock (`date -u`) and Kaggle's own log before quoting a time; give both UTC and Berlin.
5. **Went back to the CPU to develop.** The user: "absolutely nothing back to CPU". Develop and test on the Kaggle GPU with
   short launches (a 3 mm grid, one second of stout, about 3 min in all). A syntax and name check on the CPU is fine.
6. **Opened the literature after the physics was closed**, and proposed water's viscosity be replaced. The model is the
   note's. Do not reopen it.
7. **Asked the user to choose between options** when they had already said what they wanted. Decide and do; ask only for
   GPU budgets, bridge deploys and money.
8. **Fitted a decay with a band-pass filter** (biased). Use `kaggle_decay.fit_decay`, and run its `--selftest`.
9. **Ignored the cart's own damping** when judging the rides; measure it (`cart_damping.cjs`).
10. **Published a surface reconstruction that was wrong near the waist** (the base of each column ignored that the tulip
    closes and opens again). Check the stored surface at rest: every ring must read the fill height.
11. **Kaggle shows no log and no files while a run is going.** Budget for it: tell the user when the run ends, and push
    progress out of the notebook only once the bridge exists (test T2 in `docs/kaggle-pipeline.md`).
12. **Cloudflare's zero-second build refusal** (`docs/usul.md`, 12 November): a commit pushed to a branch and then to `main`
    as the same commit can be refused instantly with no build. Check the "Workers Builds: phyein-usul" check on the `main`
    commit; if it failed in zero seconds, one further commit on `main` starts the real build. Always verify the LIVE page.
13. Smaller ones: a script named `bisect.py` shadowed the standard library; `python3 -I` hides installed packages; the
    site's scripts cannot be `require`d from Node (ESM package), load them with `new Function('module', ...)` as the
    `tools/fig12/*.cjs` scripts do; never chain `sleep` to wait, run the wait in the background.

---

## 7. The work, in order, with gates

### Stage A. Exact model and controllers (Wolfram + SymPy; no GPU)
- Derive omega_11, the mode's forced equation with its coupling constant for THIS glass and fill, the damping numbers, the
  linearised cart + first mode plant, its controllability from the motor current and from u_s (the note says the swing is
  not controllable from u_s linearly; confirm), the LQR gains (continuous Riccati) and the Kalman filter's discrete
  matrices (exact zero-order hold, Van Loan). Reproduce the site's numbers: K = (76.7, -1934, -41.3, -150), poles
  -11.3 +- 7.5j, K_s = (-502.6, 11.6, -6.1, 612.6), filter gain 0.143 and 2.19 1/s.
- **Gate A**: every number above reproduced to the digits given, or the difference explained. Keep the derivation as a
  SymPy script in `tools/fig12/control/` whose output is committed.

### Stage B. JAX on Kaggle (skill `jax-differentiable-physics`)
- B1. The reduced plant in JAX (cart + three modes + controller + filter), float64, `lax.scan`, differentiable. Gate:
  matches `stout-cart.js`'s live model over the stored road (lean over one bump 24.7 / 7.6 / 0.8 / 0.4 mm for
  off / PI / preview / slosh) and Stage A's poles.
- B2. The 3D stout in JAX on the GPU, with the cart, controller and filter **inside the time loop**. The user asked for
  JAX. Fixed-size arrays, `jit`, `lax.while_loop` for the pressure solve, `segment_sum` or scatter-add for particle to grid.
  **Opinion of the old session:** port solver v2's algorithm first and prove it equal to the Taichi one on the free swing,
  then improve it (section 5, "Open"). The case against: a rewrite costs days and GPU minutes before the first controlled
  ride; the Taichi solver v2 already runs at 15 min a ride and its cart port already carries `preview` and skyhook. If the
  JAX solver is not through its gates within the first budget, generate the first controlled rides with the Taichi solver
  (adding the filter and the LQR to its `Cart`), publish them, and say on the page which solver made which ride.
- **Gate B** (all on the GPU, short launches): (1) at rest for 2 s, every ring of the stored surface within 0.3 mm of the
  fill and no spurious lean; (2) free swing: frequency within 2 % of 3.421 Hz, numerical zeta stated with its grid
  convergence; (3) volume kept within 0.1 %; (4) the coupling: stout's momentum change equals minus the impulse on the
  cart, to rounding; (5) the uncontrolled ride at 1.0 m/s agrees with the stored 2026-11-13 ride within stated error;
  (6) time per step measured, then the budget arithmetic redone from the measurement.

### Stage C. The controlled rides
- Same road ("gentle road: hump, dip, ripples, bump": cosine bumps at 1.5 m (+10 mm, 0.6 m long), 3.5 m (-8 mm, 0.6 m),
  5.75 / 6.25 / 6.75 / 7.25 m (+5 mm, 0.5 m), 9.0 m (+10 mm, 0.25 m)), same speeds 0.5, 1.0, 1.5 m/s, 20 s, 30 frames/s.
- Control modes, in this order: `preview` (+ skyhook), `slosh` (LQR on the Kalman estimate), `joint`.
- Store per ride, besides the baseline's fields: the control mode, the gains, the motor current i and its command, the
  active force u_s, the two probe readings and y_q, the estimate (v, q, q') and the true q read from the surface
  (`kaggle_decay.py`, ring 13), a_x and a_z of the glass, and the three clocks. One file per (road, speed, control) block.
- **Gate C**: lean and spill beside the baseline for every speed; current within +-3 A and voltage within 12 V at every
  sample; the swing's damping ratio after the last bump measured with `fit_decay`; nothing claimed that the data does not
  show. If a controller does worse than the baseline somewhere, publish that too and say why.

### Stage D. Site and pipeline
- New generation folder `public/data/fig12/<date>/` with `index.json` (notebook, version, GPU, solver commit, measured
  times, SHA-256 per file) and the same files kept in the notebook's output under the same date. Tell the user the size
  before committing data.
- The page: a control switch (off / speed-hold / preview / slosh / joint) built like the speed control of `kaggle-flow.js`:
  filled where computed, hollow where not; switching control cross-fades at the same ride time; the with-and-without view
  the user asked for; the motor current and active force drawn from stored data. Nothing reacts to the pointer merely
  crossing a figure. Data panel extended (`phyein-usul-data-panel`, `phyein-usul-bookkeeper`): every new stored value
  proved three ways. The lecture note gains the control sections (teacher, derivation-checker, referee, walkthrough-keeper
  agents; `notes/STANDARD.md`). Docs, inventory, i18n (`ENGLISH_ONLY` holds this page today).
- `kaggle-bridge` (`docs/kaggle-pipeline.md`): today it holds Cloudflare's starter code and the secret
  `KAGGLE_API_TOKEN`; the pages run with `BRIDGE_URL = null`. Open tests: T1 (a Worker holding the token starts a notebook
  run with parameters, reads status, fetches output) and T2 (the notebook pushes progress and results out). Design there:
  `POST /v1/{project}/block`, store first, one queue, identical requests share one job, a daily GPU cap the user chooses,
  the weekly quota read before every launch, the grant behind Cloudflare Access like the job site. The Schrodinger session
  works on the same Worker design; do not message it; the user coordinates. **Deploy only with the user's yes.**
- **Gate D (done means)**: live page plays with and without control at 360, 390, 1024, 1440 px, no console errors, no
  sideways scroll, no jump anywhere; data panel all checks agreeing; docs say what the code does; merged to `main`;
  the LIVE page verified in a real browser, screenshots shown to the user.

---

## 8. Kaggle: how a launch is built

1. Code lives in the repository and is pushed to the working branch. The notebook is ONE small cell that downloads the
   files from `raw.githubusercontent.com/Numa1997/SiteTest/<commit>/tools/...` at a **pinned commit**, writes them to
   `/tmp/...` (so tracebacks and kernel sources resolve) and `exec`s them in order. See any version of the two notebooks.
2. `mcp__Kaggle__save_notebook` with `request`: `slug` (existing) or `newTitle`, `text` (the whole .ipynb JSON as a string),
   `language: "python"`, `kernelType: "notebook"`, `isPrivate: true`, `enableGpu: true`, `enableInternet: true`,
   `kernelExecutionType: "SaveAndRunAll"`, `sessionTimeoutSeconds` = estimate x 1.5, each with its `has...: true` flag.
3. First lines of the run: `nvidia-smi`, stop if no GPU. Print the plan and the time arithmetic. Log a progress line a
   minute to `/kaggle/working/<date>/progress.log`. Save every result as it is finished.
4. Wait with a background `sleep`, poll `get_notebook_session_status` at most once a minute, read
   `list_notebook_session_output` when it ends (the log and the file links), download with `curl`, check sizes.
5. Never relaunch a failed run without telling the user what failed and what changed. `cancel_notebook_session` is denied
   in this workspace: a wrong run burns until its timeout, so keep timeouts tight.
6. Quota: 30 GPU hours a week (108,000 s), read it with `get_accelerator_quota` before every budget; it resets Saturday
   00:00 UTC. On 13 November about 15,500 s were used.

---

## 9. The first GPU budget to put before the user (one yes)

Redo this arithmetic from your own measured time per step before you show it. With the Taichi solver v2's measured
90 ms a step at 1.5 mm:

- smoke launches while porting (3 mm grid, 1 s of stout): up to 6 x 4 min = 24 min;
- Gate B on the JAX solver (rest, free swing on 3, 2 and 1.5 mm, one baseline ride): about 45 min;
- controlled rides: 3 speeds x 3 control modes x 10,000 steps x 90 ms = 9 x 15 min = 135 min;
- total about 205 min = 3.4 h, 11 % of the weekly 30 h.

If the JAX solver's step is slower or faster, the ride minutes scale with it; say the new number.

---

## 10. First message to the user

Three or four plain lines: what you read, the stages A to D with the first visible result and when, and the one budget of
section 9 with its arithmetic for one yes. Then start Stage A at once (it needs no GPU and no yes).

---

## 11. Added 13 November 2026, about 00:45 UTC: what the user demands of the control (their words first)

"The control on the cart MUST BE RATHER SOPHISTICATED AND CANNOT BE JUST ONE DAMN SPRING. I wanna see a sophisticated system
of engineering physics live in action, mathematically sound, beautiful, complete, and computationally optimised and fitting."
"I wanna see all of the engineering components in that animation, a proper correct and detailed treatment. Again,
mathematically complete system, no bullshit."

What that means for your work. These are requirements, not options.

**The system that runs inside the GPU loop is the whole one, all parts together** (the `joint` design of section 4.4 as the
floor, not the ceiling):
- the motor loop: state feedback (LQR) on the estimated swing and speed, with integral action;
- the estimator: a Kalman filter fed by two height probes on the glass wall, the speed encoder and the measured current,
  with the heave put into its model; sensor noise switched on, seeded, and stored;
- the road preview feed-forward that cancels the bump's push one current lag ahead;
- the active suspension with its own LQR on (stroke, body speed, wheel speed, tyre compression), read from a stroke sensor,
  two accelerometers and the axle load cell;
- the current that cancels the heave's parametric term in the swing's equation;
- every limit real: current +-3 A, supply 12 V with the back-EMF, active force +-40 N with its 5 ms lag, tyre grip mu N,
  the 1 ms sample, the 2 ms current lag. Saturation handled (anti-windup) and shown when it happens.
Beyond that floor, and only after it is reproduced: tune the weights through the differentiable JAX model of Stage B1
(gradient of a stated cost: lean, spill, current, stroke) and say what the tuning changed; a finite-horizon preview
controller (model-predictive, using the known road ahead) is the natural next design if the floor leaves lean on the table.
Every design choice gets one line of why and the strongest case against.

**Mathematically complete** (Stage A's output, in the lecture note and checked by the derivation-checker and the referee):
- the closed loop written as ONE state-space system: first mode(s) of the stout, cart (x, z_b, z_w), motor current,
  actuator lag, filter states, integrator; continuous form, then the exact discrete forms at the three clocks (1 ms control,
  2 ms fluid, 0.1 ms cart);
- controllability and observability, with ranks and the physical reading (what the motor can steer, what the suspension
  cannot, which sensor sees which state);
- the Riccati equations for both regulators and the filter, their solutions, the closed-loop poles;
- stability margins of the motor loop (gain and phase margin, the delay it tolerates) and what the 1 ms sample and the
  2 ms lag cost; the separation principle and where it stops holding (breaking at a wall amplitude of 21.2 mm, saturation);
- the parametric term: the swing under heave is a Mathieu-type equation; say where the cancellation is exact and where not;
- each number verified by Wolfram and by an independent numerical route, and stored so the data panel proves it three ways.

**Every engineering component is in the animation, drawn where it sits and doing what it does** (drawing from stored data
only; `stout-view.js` already draws part of this for Fig. 12, read it first):
- motor, gearbox, wheel and tyre (its compression), spring, damper, the active-force actuator with an arrow for its force;
- the sensors: the two wall probes with their readings, the speed encoder, the body accelerometer, the stroke gauge,
  the axle load cell;
- the signals, live beside the cart: motor current and its command against +-3 A, the voltage against 12 V, the active
  force against +-40 N, the estimate of the swing against the true swing read from the stored surface, the road ahead
  that the preview reads, the phase space of the first mode with and without control;
- a block diagram of the loop that lights up the path a signal takes (probe -> filter -> regulator -> motor -> cart ->
  stout -> probe), in the house design. Nothing reacts to the pointer merely crossing a figure.

**Computationally optimised and fitting**: measure before you tune. State the time per step and where it goes (pressure
solve, particle transfers, level set), choose the grid from a convergence study and not from habit, use float64 only where
it is shown to matter, and store only what the page and the proofs need (say the size of every file before committing).

**Order (the user, 13 November)**: the old session first finishes and installs the "before control" animation (the three
baseline rides of `public/data/fig12/2026-11-13/`, live on main), and then tells you where to go from there. Build on those
rides; they are the "without control" side of your comparison.
