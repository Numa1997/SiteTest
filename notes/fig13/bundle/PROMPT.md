# Spirographs in Momentum Space: a study and a page for Phyein Usul

You are a Claude Code session working in Numa's repository `Numa1997/SiteTest`. Its `main` branch is the live site https://phyeinusul.com, which Cloudflare builds and deploys on every merge. Read `CLAUDE.md` and `AGENTS.md` first; their rules apply to everything below.

## 0. The three aims

- **Numa's aim.** He saw a picture in a YouTube video and could not stop thinking about it. It is a 10 × 10 grid of strange, beautiful curves (glowing spheres, wire-frame tori, bowls with a slit, rosettes) over a blue-grey X-shaped fractal. He wants to understand these curves completely, and to have them on his website as learning material of his own. That means a living animation and a lecture note that teach the physics, in his design, as rich and exotic as the original, with proper credit to the people who made it.
- **The previous session's aim (done).** Identify the picture, find the exact equations, reproduce the curves from the physics and hand everything over. It found the source, read the source code, reproduced the grid and checked the numbers. It also produced a prototype whose physics is right but whose drawing Numa judged "horrendous" next to the original.
- **Your aim.** Study this topic until you own it: derive every curve type from the physics and test every claim by computation. Then build our own, deeper version of the study on his site, at a visual standard at least as high as the video's, and publish it.

## 1. Where the material is

Everything the previous session made is on the branch **`fig13-study-bundle`**, in **`notes/fig13/bundle/`**, both unpacked and as `fig13-bundle.zip`. **Do not merge that branch.** It is a working archive, not site content. Read it without touching your work branch, for example:

```bash
git fetch origin fig13-study-bundle
git worktree add ../fig13-bundle origin/fig13-study-bundle   # read-only copy beside the repo
ls ../fig13-bundle/notes/fig13/bundle
```

Contents (see its `README.md`):

- `prototype/simulations/momentum-spirographs.html` and `fig13-map.png`: a working page in the house design. Physics is correct; drawing is not up to standard.
- `compute/`:
  - `sim.py`: NumPy tip paths and the chaos map;
  - `map2png.py`;
  - `shot.cjs`: Playwright screenshots, readback, JS tips.
- `data/`:
  - `paths.npz`: tip paths of the 10 × 10 grid, 12 s, 900 points per second;
  - `map.npz`: chaos map 384 × 216;
  - `js_tips.json`.
- `screenshots/`: the prototype page, figure and schematic. These show what **not** to settle for.
- `sources/swaptube/`: 2swap's code (Unlicense, public domain, LICENSE included). It holds the 2025-07-17 versions of PendulumScene, PendulumGridScene, PendulumFractal.cu and PendulumHelpers, and the deleted project file of the video (`DoublePendulum.oldproject_ae50d62-parent.cpp`, the momentum-space part at about lines 410–545).

**The visual reference is not in the repo**, because the repo is public and the frame belongs to 2swap. Watch it yourself: **2swap, "Double Pendulums are Chaoticn't"**, https://www.youtube.com/watch?v=dtjb2OhEQcU, chapter "Momentum Space" (6:10–7:28). The grid is on screen from about 7:08 to 7:20 ("Here's some spirographs from all over momentum-space."). Grab frames there for your own side-by-side comparisons, but never commit or publish them.

## 2. What is established (Fact = checked against source code, a computation or a real browser)

- **The system.** It is a compound double pendulum: two equal uniform rods of mass m and length l, angles θ₁ and θ₂ from the downward vertical, conjugate momenta p₁ and p₂. With Δ = θ₁ − θ₂ (from swaptube `PendulumHelpers`, m = 1 kg, l = 1 m, g = 9.8 m/s², RK4):
  - θ̇₁ = 6/(m l²) · (2p₁ − 3 cos Δ · p₂)/(16 − 9 cos²Δ)
  - θ̇₂ = 6/(m l²) · (8p₂ − 3 cos Δ · p₁)/(16 − 9 cos²Δ)
  - ṗ₁ = −½ m l² (θ̇₁θ̇₂ sin Δ + 3(g/l) sin θ₁)
  - ṗ₂ = −½ m l² (−θ̇₁θ̇₂ sin Δ + (g/l) sin θ₂)
- **The picture (the old project file, lines about 479–517).**
  - 10 × 10 pendulums, all started at θ₁ = θ₂ = 0, with p₁ = ((i + ½)/10 − ½)·40·(16/9) and p₂ = −((j + ½)/10 − ½)·40. So p₁ spans ±35.6 and p₂ spans ±20 kg·m²/s.
  - Each cell draws the **path of the tip of the lower rod**: on screen, x = l(sin θ₁ + sin θ₂) and y = l(cos θ₁ + cos θ₂), with y pointing down. The pivot is at the cell centre, and the arm length on screen is the cell height/5.
  - The paths are thin white lines (`line_thickness/4`) on black, 30 RK4 steps per frame of 1/(30·30.01) s at 30 fps (real time).
  - The trail loses 2/255 of its alpha per frame, so it lives about 4.3 s.
- **The X-shaped background (PendulumGridScene, PendulumFractal.cu).**
  - Each pixel is a pendulum started at θ = 0 with that pixel's (p₁, p₂), plus a twin whose θ₁ is nudged by 10⁻⁴ rad.
  - The map is the mean 4-D distance between the twins over 4000 steps of 0.05/30 s, coloured black → blue → white, shown under the curves at 30 % opacity.
  - Bright means chaos. It is a finite-time Lyapunov-type map.
- **A bug in swaptube that does not change his pictures.** `compute_kinetic_energy` is the point-mass formula, and its potential is twice the rod potential. Both are used only for colouring. The correct rod energy is T = (m l²/6)(4θ̇₁² + θ̇₂² + 3θ̇₁θ̇₂ cos Δ) and V = (m g l/2)(4 − 3 cos θ₁ − cos θ₂). p·q̇ = 2T holds to machine precision at θ = 0 for all 100 cells.
- **The step size.** At 2swap's step (1.11 ms), the median cell keeps its energy to 1.4 × 10⁻⁴ over 12 s, but the worst cell drifts by 11.5 %. At 1/9000 s the worst drift is 1.6 × 10⁻⁶. Use the finer step or better.
- **The prototype.** The JS tips agree with the independent NumPy run to 5.8 × 10⁻⁸ m at t = 6 s for all 100 pendulums, and the page has no errors. Its chaos map is a blocky precomputed PNG, valid only at the default parameters.

## 3. Why the prototype looks bad, and the visual standard

The bar is the video frame, not the prototype. The physics agrees to 10⁻⁸ m, so **the gap is in the drawing.** Test these likely causes against the frame; do not assume them:

- **Glow versus ink.** White hairlines on black add up. Where all petals cross near the pivot, light piles up and reads as a lit sphere. Dark ink on paper does the opposite: crossings saturate to a black blot. Render each cell as a **long exposure**: accumulate the time the tip spends per pixel, weighted by age for the fading trail, in a float buffer, then tone-map it (log or a soft curve) into the house palette so density grows smoothly and never clips. Also try a dark "night plate" (ink-black ground, paper-coloured light). Show both to Numa and let him choose (skill `tune-with-numa`).
- **Line weight and sampling.** Use antialiased hairlines of about 0.5–0.8 device px. Measure segment length on screen and keep it under about 1 px, so fast cells stay curves and not polygons.
- **The fading trail is the 3-D effect.** Newer strokes over older ones give the bowls their rim and slit. Weight by age continuously, not in 16 coarse bins.
- **Clutter.** Rods drawn on every cell compete with the curves. They should be off by default.
- **Size and timing.** Cells are about 108 px tall at 1080p in the video. Render at the device-pixel ratio, and compare cell for cell at the same (p₁, p₂) and the same moment (about 4 s into the overlay).

## 4. Our own version: the family and the enhanced scope

**The family.** Build on the general double pendulum, so that 2swap's rods and Numa's **Fig. 2 "Double Pendulum"** (`public/simulations/Double Pendulum.html`: point masses m₁, m₂ on massless rods l₁, l₂) are two limits of one model. Link i has mass mᵢ, length lᵢ, centre of mass at aᵢ from its upper joint, and moment of inertia Iᵢ about it:

- T = ½(m₁a₁² + I₁ + m₂l₁²)θ̇₁² + ½(m₂a₂² + I₂)θ̇₂² + m₂l₁a₂ θ̇₁θ̇₂ cos Δ
- V = −g[(m₁a₁ + m₂l₁) cos θ₁ + m₂a₂ cos θ₂]

Uniform rods have aᵢ = lᵢ/2 and Iᵢ = mᵢlᵢ²/12. Equal rods must reproduce 2swap's equations exactly; check with SymPy or Wolfram. Point masses have aᵢ = lᵢ, Iᵢ = 0. Derive the Hamiltonian by Legendre transform with the 2 × 2 mass matrix and implement the general Hamilton equations. Every parameter stays a symbol in the note and a control on the page: m₁, m₂, l₁, l₂, the rod/point choice, g, the momentum range P and the grid size N.

**What the study must explain, each with computed evidence:**

- **Low energy (centre).** Two coupled oscillations, the normal modes ω₊ and ω₋. Derive them for the general model and show the cups and Lissajous-like cells as their superposition. Check measured frequencies against the formula.
- **High energy (corners).** Gravity is a small perturbation. With g = 0 the total angular momentum is conserved, the system is integrable, and the tip draws a two-frequency rosette whose petals pass through the pivot whenever the arms fold. Derive it, and account for petal counts and the tip radius.
- **The chaotic X.** Find where it lies and why it has its shape, using the energy at θ = 0, E = ½ pᵀM⁻¹p (ellipses in the (p₁, p₂) plane), and the threshold for the arms to go over the top. Compare our map with Poincaré sections and a proper largest Lyapunov exponent. Say plainly what is explained and what is only observed.
- **Why "spirograph" fits.** Regular orbits lie on invariant tori (KAM). The tip path is a curve winding on a torus, projected to the plane, like a sum of two rotations. Chaos is where the tori break.
- **Across the family:** rods versus point masses, m₂/m₁ and l₂/l₁.

**The enhanced scope (beyond the video):**

1. **Probe.** Click a cell or a point of the chaos map to pin one pendulum, following the data-cursor rule in `CLAUDE.md` (no reaction to the pointer merely passing over). It opens large: long-exposure tip path, the moving rods, (p₁, p₂), energy, a regular or chaotic verdict, and measured frequencies.
2. **Zoom and pan momentum space**, like the video's camera push-in, to hunt exotic cells near the edge of the X.
3. **One orbit, three views:**
   - the tip path (the spirograph);
   - (θ₁, θ₂) drawn on a 3-D torus, which is where the wire-frame tori come from;
   - a Poincaré section (a closed curve for a torus, a scatter for chaos).
4. **An atlas of exotic curves.** Scan momentum space finely offline with a generator script in `tools/` (for example 400 × 225 cells). Classify the orbits by frequency ratio, rotation number and Lyapunov estimate. Present a curated gallery: p:q locked rosettes, knotted librations, bowls, tori, sticky orbits at the chaos edge. Each tile is labelled, and clicking it loads it in the probe.
5. **The family view:** the same grid for point masses (Fig. 2's model) and for other mass and length ratios.

## 5. Step 0: study, then stop and report

1. Read `CLAUDE.md`, `AGENTS.md`, `docs/styles.md`, `docs/usul.md`, `notes/STANDARD.md`, Fig. 2's page and its doc in `docs/simulations/`, and the whole bundle. Run `git fetch origin main` and see what other sessions changed.
2. Watch 2swap's chapter (6:10–7:28) and the Drew's Campfire video it credits. Read the swaptube files; the full repo history is at github.com/2swap/swaptube.
3. Derive the general model, check that it reduces to 2swap's equations, and reproduce his 10 × 10 grid.
4. Render three or four cells with the long-exposure method, side by side with the same cells from frames you grabbed yourself.
5. Decide where it goes. The default is a new **Fig. 13** page (for example `public/simulations/momentum-spirographs.html`), linked both ways with Fig. 2. If a section on Fig. 2 serves better, say why.
6. Report to Numa in plain short sentences: what you learned, the visual comparison, where it goes, the plan for section 4, the files you will change, and what you could not verify. **Then wait for his go.**

## 6. Building (after his go)

- **The figure.** A live animation rendered to the standard of section 3, with a chaos map in the house palette that follows the parameters or says plainly that it does not. Options: a progressive Web Worker at modest resolution, or precomputed maps from a committed generator in `tools/` with the parameters recorded. Measure on a phone-class device (4× CPU slowdown) and pick. Then add the probe, zoom, three views, atlas and family view.
- **Controls:** Play/Pause, Restart, show rods, show chaos map, trail length τ, grid N, momentum range P, model (rods or point masses), m₂/m₁, l₂/l₁, g.
- **The lecture note** goes in `<article class="paper" id="paper">`, to `notes/STANDARD.md`. Start from everyday experience (a child kicked on a swing, a twirled baton), then the model, then the mathematics. Derive every step from the physical setup; bring no term from nowhere. Numbered equations, `Key result` boxes, worked examples with the page's own numbers, Problems at the end. Drawn figures of the mechanism: the general link with mᵢ, lᵢ, aᵢ, Iᵢ; the normal modes; one cell explained; the energy ellipses. No question-and-answer format.
- **"Sources and thanks"**, warm and specific, crediting only what you have verified:
  - 2swap, "Double Pendulums are Chaoticn't" (2025), and the swaptube renderer. Say plainly that the momentum-space spirograph picture is his idea, and that this page is our own re-derivation and implementation.
  - Drew's Campfire, "Order Within Chaos in the Double Pendulum" and "Pushing Simulations to the LIMIT to Find Order in Chaos" (8jVogdTJESw).
  - Cruz Godar (colour scheme, https://cruzgodar.com/gallery).
  - Ricky Reuser's interactive version on Observable.
  - The energy paper linked in 2swap's description (famaf.unc.edu.ar; find and read it).

  No frames of the video on the site.
- **Data tab, if added:** the pipeline rules in `CLAUDE.md` (store where computed; prove by stored value, recomputed formula and pixel readback, with alpha checked first).
- **Bookkeeping:** `catalog.js` entry, 800 × 500 webp thumbnail, the Fig. nav on every simulation page (it wraps on phones), `tools/redirects.py`, `python3 tools/inventory.py`, i18n (`tools/i18n/build.py`, as the repo does for new pages), and `docs/simulations/fig13-*.md`. A change is not done until the docs say what the code now does.

## 7. Checks

- Run the build: `npm install && npm run build`.
- In headless Chromium at 390 × 844 and 1440 × 900, check:
  - 0 KaTeX errors, 0 page errors, no sideways scroll;
  - JS tips against an independent NumPy or Wolfram run (quote the maximum difference);
  - energy drift for every cell;
  - the equal-rod limit against 2swap's equations;
  - a side-by-side contact sheet of our cells against frames from the video at the same (p₁, p₂) and time.
- Use the repo's reviewer agents one at a time: `derivation-checker`, `referee`, and `walkthrough-keeper` if there is a walkthrough.

## 8. Publish

Per `CLAUDE.md`: when finished, checked against the other sessions' work on `main` and tested in a real browser, merge and publish without asking. **The one gate for this page is the look.** Once Numa has approved the side-by-side comparison, publish. Then verify live with `curl -sL "https://phyeinusul.com/simulations/<page>?v=$RANDOM" | grep -c "<a sentence you added>"`, and report in a few lines with screenshots. Never merge the `fig13-study-bundle` branch.

## 9. Skills

- `anthropic-skills:phyein-usul-physics-content`
- `anthropic-skills:phyein-usul-smooth-site`
- `anthropic-skills:phyein-usul-data-panel`
- `anthropic-skills:phyein-usul-i18n`
- `anthropic-skills:phyein-usul-bookkeeper`
- `anthropic-skills:physics-simulation-study`
- `anthropic-skills:physics-model-loop`
- `anthropic-skills:theoretical-physicist`
- `anthropic-skills:feynman-technique`
- `anthropic-skills:wolfram-language`
- `anthropic-skills:sympy`
- `anthropic-skills:unslop` (all new prose)
- `anthropic-skills:tune-with-numa` (anything judged by eye: one attempt, then show him)
- `anthropic-skills:verification-before-completion`
- `anthropic-skills:find-image-source` (if he saved it)

## 10. How to talk to Numa

He has a BSc in Physics (computational and theoretical). Reply in English, metric units only, short plain sentences in connected prose. Physical pictures first, then the calculus. Mark statements Fact (with a file and line, a link or a command), Inference or Opinion. Use Wolfram for computations, and loop twice over every conclusion. Never claim work you did not do. Send short progress messages, with no long silent stretches. When wrong, say so in one line and fix it.
