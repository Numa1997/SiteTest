# Prompt for a new session: a computational physicist rebuilds the Guinness simulations (Fig. 12 and Fig. 16)

Written 14 November 2026 by the Fig. 16 session (branch `claude/fig16-cart`). You are a new session. Everything you need is in this
prompt and in the repository `Numa1997/SiteTest`. Read this whole prompt, then the files in section 3, before any work.

## 0. The mission, in the owner's words

"The animation is absolute shit. Terrible quality, and probably bad and shit and lazy physics. Nothing looks real. The wheels run in
the opposite direction for some reason. Way way fast. And no fluid motion. No ability to turn control on or off. This applies both to
the Guinness simulations. We need a computational physicist on this mission."

You are that computational physicist. Your job: make both Guinness figures physically right and visibly real.
- **Fig. 12**, A Pint of Guinness on a One-Wheel Cart, computed on Kaggle: `public/simulations/guinness-kaggle.html`.
- **Fig. 16**, A Pint of Guinness on a Cart Built to Carry It (live since 14 November 2026): `public/simulations/guinness-cart-control.html`.
- Also the in-browser Fig. 12, `public/simulations/beer-slosh.html`, which shares the drawing code.

A visitor must see:
- a real pint;
- stout that visibly sloshes, with a head of foam that moves;
- wheels that roll correctly;
- carts whose parts visibly work;
- a switch that turns control on and off and shows the difference.

Every number must be honest physics computed on Kaggle's GPU.

## 1. The owner and the rules (binding)

- The owner holds a BSc in physics (computational and theoretical).
  - Metric units; define every term at first use.
  - Mark Fact (with a handle: file and line, link, or a command), Inference and Opinion.
  - Give the mechanism of each result in one line.
- Talk plainly. Short sentences. No walls of text, no option lists for things already decided, no apology floods. When the owner is
  angry: shrink the turn, say where things stand in one line, fix the problem.
- **Show, don't tell.** Pictures and working pages, not paragraphs. Screenshots of every change, at 390 and 1440 px.
- **Everything physical is computed on Kaggle, in the owner's notebooks.** Nothing physical is computed in your environment, and no
  physics runs in the browser: the page only plays stored data. A syntax or name check of code is fine.
- **GPU runs need the owner's explicit yes on a bill before launch:** runs × measured seconds per step × steps, as GPU-hours and as a
  share of the weekly 30 h, read with `get_accelerator_quota` first. CPU-only Kaggle notebooks cost no GPU quota; use them for anything
  that needs no GPU.
- **Report only to the owner, in your chat.** There is no coordinating chat. Never message other sessions.
- **Use everything the mother project (Fig. 12) already has** before writing anything new: code, data, notes, notebooks, drawings.
  The owner was furious when a home-made glass replaced Fig. 12's Guinness glass.
- **"Not a single atom of data if it's not needed."** Reuse stored data where it is valid; compute fresh only what must be fresh.
- **CLAUDE.md:** write your state file first (`notes/guinness-rebuild/STATE.md`) and keep it current. Persist: one empty search is not
  proof. Build when the request is clear. Every number on a page goes into the page's store and is proved three ways: stored value,
  formula recomputed from stored inputs, pixel read back.
- **Publishing:** a finished change, checked against `main` and tested in a real browser, is merged and published without asking
  (Cloudflare builds every push to `main`). The owner said not to verify the live site this time unless asked.
- **Never touch:** the Cloudflare Workers, R2, `public/de/`, `public/ar/`, `scripts/i18n/` or `*.rtl.css` by hand. Fig. 15's files are
  another session's; registering a figure (one nav link) is the only allowed edit there.
- **Commit trailers:** as your session's system reminder says. No model names in code, commits or PRs.

## 2. The complaints, with what is already known about each

1. **The wheels run backwards and far too fast.** Inference, to verify first.
   - The spoke angle is drawn as `ang = -c.x / Rw` (`public/scripts/stout-view.js:144`; Fig. 16: `wheelAng: -D2.x[k2] / G16.Rw` at
     `public/scripts/guinness16-play.js:97`, drawn at `public/scripts/cart16-view.js:70`). First check the sign against the camera:
     the angle is measured in the (x, z) plane, and the face is seen from −y or +y depending on the azimuth.
   - The main effect is likely the wagon-wheel stroboscope. Stored pictures come 30 a second; at 1.5 m/s a 40 mm wheel turns 37.5 rad/s,
     that is 72° per picture, while its 5 spokes repeat every 72°. So the spokes alias: they look still, slow, or backwards. At 1.0 m/s
     they turn 48° per picture against 72° symmetry.
   - Fix: draw the wheel's turning at the display rate from the stored position (the wheel's angle is kinematics, not stored physics;
     say so on the page), use an asymmetric rim mark, add motion blur, or all three. Prove the result with a frame-by-frame screenshot
     strip.
2. **No fluid motion.**
   - The stored surface is a height per column on a 1.5 mm grid, 30 pictures a second, drawn in canvas 2D as a lit sheet with the head as
     a layer (`stout-view2.js`, `stout-view.js` drawGlass). With good control the tilt is about 0.5–2.6 mm, which is invisible at page
     scale.
   - Without control (Fig. 12 kerb: 20–25 mm tilt; Fig. 16 kerb off: 55 mm, head and stout spilled) there is motion, but it is choppy at
     30 fps and flat-shaded.
   - Options to study, measure and propose:
     - a real 3D render of the liquid: WebGL via the vendored three.js `public/vendor/three/three.module.min.js` and
       `MarchingCubes.js`, used already in `public/scripts/marching.js`, `rt3d-view.js`, `wave3d-view.js`;
     - refraction or Beer–Lambert colour (see `notes/fig12/realism.md`);
     - the head drawn as a foam with its stored thickness;
     - drops and lumps as particles;
     - storing more pictures per second (60–120) or a subset of particles for splashes;
     - a magnified inset or exaggeration scale only if clearly labelled.
   - Respect the rule "no interpolation between stored frames" for physics; the owner decides any exception.
3. **No on/off switch for control.** Fig. 12 offers rides by name; Fig. 16 offers a ride list.
   - Needed: one switch, control on and off, on the same road, crossfading at the same ride time
     (`public/scripts/kaggle-flow.js` has the house cross-fade and governor; `docs/kaggle-pipeline.md` describes them), with both rides
     visible side by side or overlaid.
   - Missing data: Fig. 16 has the kerb both ways, but the gentle roads with control on only, and its kerb-off ride stopped at 0.77 s
     because the drop list was full (`M_drops=16384` at `tools/fig12/kaggle/stout_jax.py:215`). Compute what is missing.
4. **"Probably lazy physics."** Audit it; do not defend it. Known weak points, each with its handle:
   - **Numerical damping of the fluid method.** Bare stout fitted at ζ = 0.016 against about 0.0055 from physics; it grows with grid
     size (inviscid 6 mm gives 0.078). See `notes/fig12/handoff-jax/07-diagnosis.md` item 1, and the Fig. 12 note's limits section
     (`notes/fig12/note/paper.html`, rendered in `guinness-kaggle.html`).
   - **Bulking.** After violent jolts the mean surface rises 0.85–1.44 mm with no particle lost (07-diagnosis.md).
   - **Run-to-run scatter on the kerb.** ±2.7 mm lean, ±0.3 mm tilt, ±0.05 mL spill (unordered GPU sums). Never measured for Fig. 16.
   - **The carts are planar:** both wheels of an axle meet the same road, no roll, no yaw. Fig. 12's cart is one wheel with no pitch.
   - **Fig. 16's tilting glass:** only the uniform effective gravity of the mode's point S is applied; the rotating frame's forces that
     vary across the glass (θ̈ r, θ̇² r, Coriolis) are omitted (`tools/fig16/kaggle/cart4.py` header).
   - **The stout's push on the cart** measured 75.7 g against 55.8 g from cylinder theory (`notes/fig16/model.md` section 2); not
     explained.
   - **Fig. 16's controller saturates on the kerb:** motors at 8 A, actuators 46 of 50 N; the struts' bump stops at ±30 mm. The
     estimator uses ideal sensors for every state but the swing.
   - **Drawing offsets in Fig. 16:** the deck's drawn height uses an arbitrary +0.098 m (`guinness16-play.js:96`); the drawn geometry
     (`cart16-view.js`, constant `G`) is not the simulated geometry (`cart4.py` `CART4`). Make them one geometry.
   - **The parts are drawn but not driven:** springs that do not visibly compress with stored strokes, actuators without force arrows
     that read clearly. Every part must be driven by stored data.

## 3. Read first (in this order)

- `CLAUDE.md`, `AGENTS.md` (layout, boundaries), `docs/styles.md` (house design), `notes/STANDARD.md` (lecture notes),
  `docs/kaggle-pipeline.md` (Kaggle → site, storage, layout rule of 14 November: one notebook and one dataset per figure).
- **Fig. 12:**
  - `docs/simulations/fig12-beer-slosh.md`;
  - the pages `public/simulations/guinness-kaggle.html` and `beer-slosh.html`;
  - the scripts `public/scripts/guinness-jax-play.js`, `guinness-playback.js`, `stout-view.js`, `stout-view2.js`, `stout-gpu-view.js`,
    `stout-cart.js` (the site's cart, controllers, Observer, ModalFluid and NMFluid), `guinness-glass.js`.
- **Fig. 12 solver and notes:**
  - `tools/fig12/kaggle/stout_jax.py` (the JAX fluid: APIC, cut cells, level set, head of foam, `Cart`, `slosh_lqr`, `susp_lqr`,
    `observer_design`);
  - `run_b.py`, `pack_ride.py`, `check_run.py`, `note_numbers.py`, `build_note.py`;
  - `tools/fig12/control/cartctl.py` and `derive.py` (the reduced plant in JAX and the derivations);
  - `notes/fig12/handoff-control-session.md` (physics, the old session's mistakes, how a Kaggle launch is built: read section 6 and
    section 8);
  - `notes/fig12/handoff-jax/06-run8-state.md` and `07-diagnosis.md`;
  - `notes/fig12/realism.md`; `notes/fig12/research/` (verification, data for the solver, materials);
  - `notes/fig12/readers/` (what readers stumbled on).
- **Fig. 12 data:** `public/data/fig12/2026-11-14-run10/` and `2026-11-13-run8/` (index-jax.json lists each ride with its measured
  numbers and SHA-256).
- **Fig. 16:**
  - `notes/fig16/STATE.md` (read whole), `BRIEF.md`, `model.md`, `concepts.md`;
  - the page and its scripts `public/scripts/guinness16-play.js`, `cart16-view.js`;
  - the Kaggle code `tools/fig16/kaggle/` (`cart4.py`, `run16.py`, `modal4.py`, `diag16.py`, `pack16.py`, `nb_cell.py`);
  - the design model `tools/fig16/slosh_model.py`, `fit.json`, `validation.json`;
  - the data `public/data/fig16/2026-11-14/`; the run's summary `notes/fig16/run16-v2-summary.json`;
  - `docs/simulations/fig16-guinness-cart-control.md`; the prototypes `notes/fig16/proto/`.
- **Other figures for method and rendering:**
  - Fig. 14 `public/simulations/schrodinger-sphere.html` and Fig. 15 `resonant-tunnelling.html` (3D WebGL rendering of stored Kaggle
    data, `rt3d-view.js`, `wave3d-view.js`, `marching.js`);
  - Fig. 9 `driven-oscillator.html` (the house standard for control pages: take-control box, hand drag, force arrows, energy bars,
    phase portrait);
  - the data panel `public/scripts/datalog.js`, `dataset.js`, `docs/scripts/`.

## 4. Kaggle

- **Notebooks** (private, user numakoudsie):
  - `guinness-on-a-cart-stout-in-jax` (Fig. 12, versions up to 10);
  - `fig-16-guinness-cart-with-control` (Fig. 16: version 1 smoke test, version 2 rides, 19 min on a T4);
  - `fig-16-cart-diagnostics-cpu` (CPU).
- **Datasets:** `numakoudsie/fig12-guinness-on-a-cart` (all Fig. 12 runs' outputs). Fig. 16's dataset is not made yet (layout rule).
- **Measured cost:** about 85–95 ms per fluid step at 1.5 mm on a T4 (1,001,952 particles, 370,386 cells); 2,040 steps per 4 s ride.
- **Quota:** 108,000 s a week, resets Saturday 00:00 UTC. At most 2 GPU sessions at once.
- **How to launch:** a one-cell notebook fetching code at a pinned commit from raw.githubusercontent.com (`tools/fig16/kaggle/nb_cell.py`).
  - Smoke test on a 6 mm grid first (`CODECHECK`).
  - Set `sessionTimeoutSeconds` to the estimate × 1.5.
  - Write each result to disk the moment it exists.
  - Poll status at most once a minute; give the owner a progress line every 10 minutes.
  - `cancel_notebook_session` is denied; keep timeouts tight.

## 5. Skills, agents and connectors to use

- **Skills (load with the Skill tool before the work they cover):**
  - Physics: `physics-simulation-study`, `physics-model-loop`, `theoretical-fluids-and-pdes`, `theoretical-physicist`,
    `socratic-physics` (attack your own model), `sympy`, `math-skill`, `wolfram-language`, `wolfram-physics`,
    `wolfram-modelica-build`, `wolfram-modelica-analyze`.
  - Numerics: `jax-differentiable-physics`, `kaggle-gpu-run`, `physics-simulation-toolchain`, `openfoam-cfd` (an independent witness
    of the slosh, as Fig. 12 started on branch `origin/ccr-76841c15-le08bl`), `fem-multiphysics`, `scientific-coding`.
  - Control: `phyein-usul-first-principles-control`.
  - The site: `phyein-usul-data-panel`, `phyein-usul-bookkeeper`, `phyein-usul-physics-content`, `phyein-usul-smooth-site`,
    `phyein-usul-i18n`, `tune-with-numa` (anything judged by eye), `frontend-design`, `dataviz`.
  - Method: `verification-before-completion`, `pushback-proof-answers`, `orchestrating-agent-loops`, `superpowers:systematic-debugging`.
  - Research: `web-tool-ladder`, `deep-research`, `paper-review`.
- **Repository agents** (`.claude/agents/`): `physics-teacher` (lecture notes to STANDARD.md), `derivation-checker`, `referee`,
  `walkthrough-keeper`. Give each only the figure number and page path.
- **Connectors:**
  - Kaggle (`mcp__Kaggle__*`) and Wolfram (`mcp__Wolfram__*`).
  - Literature: Consensus; Firecrawl research search (`firecrawl_research_*`: sloshing, foam damping, preview control papers); Exa,
    TinyFish, Nimble, Tavily, WebSearch and WebFetch (try them in turn; CLAUDE.md lists the order).
  - The Stack Exchange API (api.stackexchange.com/2.3) when a site blocks you.
- **Literature to read whole:**
  - sloshing: Ibrahim, *Liquid Sloshing Dynamics* (2005); Abramson, NASA SP-106; Dodge, *The New Dynamic Behavior of Liquids in Moving
    Containers* (2000);
  - foam damping: Sauret et al., Phys. Fluids 27, 022103 (2015); Cantat, Phys. Fluids 25, 031303 (2013);
  - APIC: Jiang et al. 2015;
  - preview control: Tomizuka 1975;
  - slosh-free motion: anti-slosh trajectory and tilting-tray work (Feddema et al. 1997; Moriello et al. 2018; Reinhold et al.
    2019, "waiter motion").

## 6. What done means (gates)

1. **Audit first, in writing** (`notes/guinness-rebuild/audit.md`).
   - Every physics shortcut of both figures, with its handle, its size measured from stored data or a Kaggle run, and its fix or
     its justified acceptance.
   - The wheel sign and aliasing proven with a screenshot strip.
   - Show the owner, one decision at a time, before the big compute.
2. **One geometry.** The drawn carts are the simulated carts, from one parameter file.
3. **The fluid looks like a fluid.**
   - Real 3D rendering of the stored surface and head.
   - Drops and lumps visible.
   - Enough stored pictures per second that motion is smooth (measure frame pacing at 390 and 1440 px).
   - Show before and after.
4. **Control switch:**
   - On and off for every road in both figures.
   - Cross-faded at the same ride time.
   - The data for every pair computed on Kaggle (bill first).
5. **Physics fixes computed on Kaggle with the owner's yes:**
   - the rotating-frame forces for Fig. 16;
   - the drop list large enough for the uncontrolled kerb;
   - run-to-run scatter measured;
   - numerical damping reduced or bounded with grid convergence.
6. **Pages:**
   - data panel with the three-way proof;
   - lecture notes rewritten and refereed (two rounds at most unless a round finds a wrong equation);
   - docs, inventory, i18n check, redirects;
   - tested in Chromium at 390 and 1440 px;
   - merged and published.
7. **Report to the owner in a few lines with pictures.** End each turn with "Where we are" and "Next, if you say yes".
