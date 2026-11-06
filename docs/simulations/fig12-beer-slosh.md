# Fig. 12 · A Pint of Guinness on a One-Wheel Cart (`public/simulations/beer-slosh.html`)

Rebuilt from zero on 6 November 2026 after Numa rejected the previous Fig. 12 (modal sloshing in a Blender-sculpted glass, LQR,
three languages). Nothing of it is reused. The page is **English only**: `tools/i18n/build.py` lists it in `ENGLISH_ONLY`, so no
German or Arabic page is generated, and links to it from the German and Arabic pages point at the English page.

## What the page does

A pint of stout in the Guinness tulip glass rides a cart with one wheel, one spring and one damper over cosine bumps (25 cm
long, one every 2 m, height 0–25 mm). The stout is a live three-dimensional incompressible Navier–Stokes computation in the
glass's frame, in the measured shape of the glass, open at the top: stout that rises over the rim spills, falls freely and lands
on the body or the road. The cart follows Newton's laws with a DC gear motor on a current-controlled drive, a PI speed loop
(or open loop), an optional skyhook active suspension, and the reader's push (buttons, ← →) or hand (drag the cart). The two
are coupled both ways. Grid 4 mm (default, faster) or 3 mm (`?grid=3`, closer). The caption shows the seconds simulated per
second (measured in headless Chromium on the 4-core build machine, 4 mm: 0.31 with 4 threads, 0.24 with one, 0.17 before the
speed-up of 6 November 2026; see "Speed").

## Files

| File | Job |
|---|---|
| `public/simulations/beer-slosh.html` | the page: figure, controls, readouts, lecture note, store and data panel; the run loop (`Sim.clock`, 28 ms of solving per frame) |
| `public/scripts/stout-cart.js` | the solver: `Fluid` (APIC on a MAC grid, wall R(z), spillage), `Road`, `Cart` (motor, controller, suspension, hand), `World` (coupling, drops). Runs in the browser and in Node |
| `public/scripts/guinness-glass.js` | the glass's inner radius every 0.5 mm, written by `tools/fig12/glass_profile.py`; do not edit |
| `public/scripts/stout-view.js` | the drawing (canvas 2D) through a pinhole camera (22° down, turned 18° to the front, 2.2 m away) that rides with the cart; the surface as a bicubic Catmull–Rom spline through the column heights (16 × 64 polar points; beyond R(h) − 3.5 Δx extended over a 3.5 Δx baseline: the drawn edge at rest varies by 2.1 mm instead of 5.3 mm; the lean readout and `eta_front`, `eta_back`, `dw` stay the solver's `columnHeightAt`), lit by one light; the stout's colour by Beer–Lambert across the glass (a drawing constant); drops as 8 ms streaks. Reads the solver's state and computes nothing physical; writes the camera's constants and the drawn points into the store, and the page's checks recompute every point from them (`proj`, `hDraw` in the page) |
| `tools/fig12/glass_profile.py`, `irish-imperial-pint.svg`, `glass_profile.json` | the glass measured from dimensions.com's section and scaled to 160 × 85 mm |
| `tools/fig12/check.cjs` | offline checks: `node tools/fig12/check.cjs rest|tilt|cyltilt|cylfreq|freq|spill [dx] [steps/s]` |
| `tools/fig12/theory.cjs` | every closed-form number of the lecture note, from the page's constants: ξ₁₁ (series for J₀, J₁), f₁₁, tilt and centre of mass, sloshing mass, Bond, Reynolds, damping (Abramson eq. 4.10b), quarter car, drive, PI poles, crossover and margin, \|S\| at the swing frequency, skyhook transmissibility |
| `tools/fig12/study.cjs` | one run of the parameter study through `World.advance` with the page's options: `node tools/fig12/study.cjs <bump mm> <off|speed> <0|1> [dx] [s]`; `SERIES=file.json` also saves a_x, a_z and the lean every step |
| `tools/fig12/energy.cjs` | the cart's energy book over a bump (`Cart` alone): `node tools/fig12/energy.cjs [bump mm]` |
| `tools/fig12/figures.cjs` | writes `notes/fig12/fig-glass.svg` and `fig-bump.svg`, the note's two figures (pasted into the page) |
| `tools/fig12/profile.cjs` | time of one fluid step by phase: `node tools/fig12/profile.cjs [dx] [steps]` |
| `tools/fig12/same.cjs` | fingerprint of the state after 1 s with a push (SHA-256 of particles, φ, pressure): a speed-up must not change it |
| `notes/fig12/shots.cjs` | screenshots at 1280 and 390 px, deviceScaleFactor 2 (at rest, swinging after a push, spilling), and the note opened: KaTeX errors, sideways scroll |
| `notes/fig12/runs/` | the saved output of every check and study run quoted in the note (6 November 2026) |
| `notes/fig12/check.md`, `referee.md` | the independent derivation check and the blind referee report on the lecture note |
| `notes/fig12/test.cjs` | browser test (desktop, phone): run, push with and without the speed loop, drag, no errors, no sideways scroll |
| `notes/fig12/panel-test.cjs`, `panel-test2.cjs`, `spill-test.cjs` | data panel: every check and read-back; on a bump at three widths, Read values, a round, Save, idle; while spilling |
| `public/scripts/stout-pool.js`, `stout-worker.js` | the solver's loops shared over worker threads (shared memory; same numbers) |
| `notes/fig12/serve.cjs` | serves `public/` with the isolation headers Cloudflare sends for this page (tests with threads) |
| `notes/fig12/threads-test.cjs` | in Chromium: the threaded solver gives the single-thread numbers to the last digit; threads named in the readout |
| `notes/fig12/clip.html`, `clip.cjs` | renders a clip of the run (PNG frames, MP4) |
| `public/images/sims/beer-slosh.webp` | catalog thumbnail, 800 × 500 |

## The glass

dimensions.com's "Irish Imperial Pint Glass" (the tulip; a 16 oz glass, 149.2 mm, 3 in) has a dimensioned section. Its inner
outline was measured from the SVG rendered at 4× (the widest outer diameter measures 76.6 mm against the stated 76.2 mm) and
scaled to the Guinness imperial glass as retailers list it, 160 mm × 85 mm widest: heights × 1.0724, radii × 1.1096. Result: inner
radius 28 mm low, 39.3 mm widest (116 mm up; within 0.02 mm of that from 114.5 to 118 mm), 37.5 mm at the rim (147.5 mm); brim volume 530.7 ml (an imperial pint is 568 ml:
the stretched US glass is the uncertainty, stated on the page). Fill 125 mm: 426.6 g of stout.

## The model

- **Stout**: Du/Dt = −∇p/ρ + ν∇²u + g − a_g(t), ∇·u = 0; p = 0 on the free surface; no flow through the wall r = R(z) and the floor
  (free slip). ρ = 1000 kg/m³, ν = 10⁻⁶ m²/s (water's). Above the rim no wall: a particle above the rim and outside the rim radius
  has spilled.
- **Symmetry**: only y ≥ 0 is solved (v = 0 on y = 0).
- **Cart**: x, z_b, z_w; rigid wheel R_w = 4 cm whose axle follows the envelope z_a(x); radial tyre N = max(0, k_t(z_a − z_w) +
  c_t(ż_a − ż_w)); road force −N z_a′; spring 600 N/m, damper 8 N s/m, tyre 2·10⁴ N/m and 5 N s/m; body and glass 1.5 kg + stout;
  wheel 0.3 kg; drag c_x = 2 N s/m; M_x includes the wheel's and the rotor's rolling inertia (2.50 kg with a full glass).
- **Motor**: gear ratio 10, K_m = 0.02 N m/A, R_a = 2 Ω, J_m = 2·10⁻⁶ kg m², 12 V, current limit 3 A; F_m = b i with b = 5 N/A;
  the current follows the command with τ_i = 2 ms, clipped to ±I_max and to (±V_max − e)/R_a.
- **Controller** (every 1 ms): open loop i = c_x v₀/b; speed loop i = i₀ + K_p(v₀ − ẋ) + K_i∫(v₀ − ẋ)dt with K_p = M_x ω_c/b,
  K_i = K_p ω_c/4, ω_c = 2π·8 Hz (25.1 A/(m/s), 316 A/m); the integral stops while the current is limited.
- **Suspension**: u_s,cmd = −c_sky ż_b, c_sky = 2·0.7·√(k M_s) = 47.6 N s/m, ±40 N, lag 5 ms.
- **Hand**: clip(300 (x_hand − x) − 30 ẋ, ±25 N) while dragging.
- **Coupling**: the stout's reaction is −(ΔP + P_spill)/Δt, P its momentum relative to the glass, P_spill the momentum carried over
  the rim in the step; m_ℓ falls as it spills. It is handed over as an impulse J = −(ΔP + P_spill): the next fluid step, of length h,
  applies J/h (equal to the old force when the steps are equal). `World.advance` cuts an interval that the CFL limit shortens into
  equal steps. Both since 6 November 2026, see "Found by measurement".
- **Drops**: each spilled particle (and its mirror image) falls freely from the glass's position and velocity plus its own until
  it meets the body's top or the road.

## The numerical method (`stout-cart.js`)

APIC (2 × 2 × 2 particles per cell: 25 666 in the half glass at 4 mm, 61 407 at 3 mm); MAC grid 20 × 10 × 45 at 4 mm; fluid step
5 ms. Wall: open fractions of the cell faces with R at the face's height (slivers under 10 % closed); faces closed by the wall filled
by extrapolation (free slip); a particle outside the wall goes back onto it along the wall's normal. Wall-cut cells are liquid when
they share an open face with liquid beside them or with liquid well below the surface above them. Free surface: Zhu–Bridson level set
with mirror images in y = 0 and in the wall; **particle radius 1.8 spacings**; ghost-fluid pressure, θ ≥ 0.05; a cell holding
particles counts as liquid with φ ≥ −0.05 dx. Pressure by PCG with MIC(0), warm-started.

**Found by measurement, 6 November 2026, keep:**
- The coupling handed the cart the force −(ΔP + P_spill)/h_last and applied it over the next step: after a step cut short by the
  CFL limit, `World.advance` took the rest as a sliver (0.02 ms measured), and the force measured over the sliver acted over the
  next 5 ms step, an impulse about 260 times too large (heave 36.2 m/s² in one step over a 25 mm bump in open loop; `study.cjs 25
  off`). Fixed by handing over the impulse and cutting the interval into equal steps; the 25 mm open-loop run now reads a_x 3.58,
  heave 7.63 m/s², 11.9 g spilled. Every run without a shortened step is unchanged to the last digit (all 10 mm runs; `same.cjs`
  tests `Fluid` alone and still prints `7747da757ea9d800`; the 123 panel checks still pass).
- With a particle radius of 1 spacing the stout could not hold a steady tilt (centre of mass 15 % of exact, also on the version
  then live): on a tilted surface many cells hold particles but read φ ≥ 0, were forced liquid at φ ≈ 0, and the ghost-fluid
  coefficient kicked them every step, driving a circulation down the high wall. 1.8 spacings removes it (`check.cjs cyltilt`).
- The wall must be met along its normal: radial projection in the rounded bottom corner drained the pint (0.37 m/s at rest).
- Wall images need the test `z < z_rim`, not `R < R_box` (the cylinder lost them: 3.12 Hz instead of 3.39).
- A level-set extension into wall cells (constant or linear) and a particle-density volume correction were tried and rejected:
  both broke the free swing (measured); the volume correction exists, off (`volumeCorrection: 0`).

## Speed (measured 6 November 2026)

One fluid step at 4 mm (25 649 particles, 9 000 cells), Node on the build machine, `profile.cjs`, 200 steps, three runs
alternating old and new code: 24.7–26.1 ms before, 17.5–20.2 ms after. In headless Chromium (`World.advance` timed on the
running page, 10 s): 26.7 → 19.0 ms per step, 0.171 → 0.237 s simulated per s; drawing takes 1.6 ms a frame, the solver 90 % of
the time. After: level set ≈ 4.6 ms, pressure ≈ 4.4 ms (33 CG iterations), advection and wall ≈ 4.9 ms, transfers ≈ 4.2 ms.

The changes compute the same numbers in the same order: `same.cjs` prints `sha256 7747da757ea9d800` (np 21 948, 3 718 spilled,
6 462 CG iterations over 200 steps) before and after; at 3 mm, `node tools/fig12/same.cjs 0.003`, `c1469868437cbd69` (np 52 464,
8 943 spilled, 7 411 CG iterations) before and after. Browser tests after: `test.cjs`, `spill-test.cjs`, `panel-test2.cjs`
(123 checks, none differ; no errors).

- Level set: the "near an empty cell" test and a new "particle within reach" test are 2-cell dilations of masks, done axis by axis
  (15 reads a cell instead of 125). A cell with no particle in its 5 × 5 × 5 block gets φ = 3 dx without a search: that is what the
  search returned there. Each particle's wall image (factor (2R − r)/r) and whether it has one are computed once per step
  (`levelSetParticles`), not once per pair. The particles are copied in cell order so the search reads memory in sequence. Cells
  of the block whose nearest point is 2 dx or more away are skipped unless one of their particles has a wall image; mirror images
  are skipped from the third row (y ≥ 2.5 dx) on. All of these drop only terms that fail the test d² < R_k².
  (`phiCell`; `phiAt` is the plain version, used when `kernel` is not 2.)
- Pressure: the conjugate gradient loops run over a list of the liquid cells (about 4 000 of 9 000), with each cell's
  six neighbour bits; the products A·pc of the MIC(0) sweeps are formed once per solve.
- Advection: one sampling closure per velocity component (same formula as `Fluid.sample`, without its dispatch).
- Tried and dropped: one pass over the particles for all three components in the transfers (slower, 2.7 against 2.2 ms).

### Threads (6 November 2026)

`public/scripts/stout-pool.js` and `stout-worker.js` share four loops of each step with `navigator.hardwareConcurrency − 1` worker
threads (at most 7) plus the page's own thread: the level-set search (every P-th cell of the list), grid-to-particle and advection
(contiguous particle ranges), particle-to-grid (each thread owns a slab of grid layers with about equal particle counts and adds,
in particle order, every term that lands in its slab, so each grid value gets the same terms in the same order). The arrays the
threads touch are made in shared memory (`new Fluid({shared: true})`, `Fluid.mk`); the store holds the same shared particle
arrays (`World.attach`). The page's thread spins on a shared counter until the workers are done (a page's thread may not block);
a worker whose share throws still counts itself done and the page goes on alone. Off with `?threads=1`; off where the browser
gives no shared memory (no `crossOriginIsolated`): the page then runs exactly as before.

Shared memory needs a cross-origin-isolated page: `public/_headers` sends `Cross-Origin-Embedder-Policy: require-corp` for
`/simulations/beer-slosh.html`, `/simulations/beer-slosh` and `/scripts/stout-worker.js` (the site already sends
`Cross-Origin-Opener-Policy: same-origin` everywhere; the page loads nothing from other origins). The worker script needs it too:
without it Chrome silently starts no worker in the isolated page (found on the live site after the first deploy, which ran on one
thread). `notes/fig12/serve.cjs` serves `public/` with the headers `public/_headers` gives each path, as Cloudflare does.

Measured in headless Chromium on the 4-core build machine (`pagerate`, 10 s of the running page, two runs each): 1 thread
18.6–19.1 ms a step, 0.235–0.240 s simulated per s; 4 threads 14.3–14.4 ms, 0.306–0.310 s/s. Per parallel task (4 threads, 100
steps): search 1.0 ms, grid-to-particle 0.6, particle-to-grid 1.2, advection 1.3 ms on the page's thread, then 0.5–0.7 ms
waiting for the workers. Identity: `notes/fig12/threads-test.cjs` runs the `same.cjs` case in the page with 1 thread and with 4
and prints the same line as Node (`sha256 7747da757ea9d800` at 4 mm).

What stays serial: the pressure solve (≈ 4.4 ms; the MIC(0) sweeps run cell after cell, and splitting its sums would change
their order), the bins, the wall pass and the extrapolation (≈ 3 ms). So a step cannot fall much below about 8–10 ms on any
number of cores (inference from the phase times): about half real time at best on this grid.

## Checks (measured 6 November 2026, Node, Δt = 5 ms; outputs in `notes/fig12/runs/`)

| Test (`check.cjs …`) | Exact | 5 mm | 4 mm | 3 mm | 2.5 mm |
|---|---|---|---|---|---|
| `cylfreq`: R 40 mm, h 100 mm | 3.382 Hz | 3.098 (−8.4 %) | 3.176 (−6.1 %) | 3.235 (−4.3 %) | 3.252 (−3.8 %) |
| same, damping ratio | 0.0035 (theory) – 0.0053 (experiment) | 0.026 | 0.016 | 0.005 | 0.005 |
| `freq`: the tulip | ≈ 3.41 Hz inferred | 3.119 | 3.214 | 3.263 | 3.277 |
| same, damping ratio | | 0.030 | 0.008 | 0.002 | 0.005 |
| `cyltilt`: centre of mass, 2 m/s² | −0.815 mm | +7.6 % | +18.2 % | +3.6 % | +1.6 % |
| `tilt`: the tulip | −0.877 mm | +12.0 % | +2.0 % | +6.1 % | −3.4 % |
| `rest`: fastest particle after 1 s | 0 | | 3.2 mm/s | 4.3 mm/s | |
| `spill`: 25 m/s² for 0.12 s | left = counted | | 101.3 = 101.3 g | 105.3 = 105.3 g | |

The tulip "≈ 3.41 Hz" divides each grid's tulip frequency by the cylinder's error on that grid (3.42, 3.41, 3.41 Hz at 4, 3, 2.5 mm),
against 3.421 Hz for a deep cylinder of the surface radius R(h) = 39.1 mm (`theory.cjs`): an inference. Energy book of the cart
(`energy.cjs`): without losses E = 4.366 J holds to 2·10⁻⁴ J over a 10 mm bump, 1.7·10⁻³ J over 25 mm; with the dampers, E minus their
work to 5·10⁻⁴ J. Coupling check: after a 10 mm bump in open loop the lean swings with amplitude 18.5 mm at 3.214 Hz; the
equivalent-mass momentum (ρπR³/ξ²) q̇ predicts a cart ripple of 0.0834 m/s², the fitted ripple is 0.0829 m/s², in phase within 9°.

## Parameter study (`study.cjs`, 2.3 s, set speed 1 m/s, one bump, 4 mm; 3 mm in brackets)

| Bump | Drive | Suspension | Lean (front − back) | \|a_gx\| max | heave \|a_gz\| max | Spilled | \|A(f₁₁)\| |
|---|---|---|---|---|---|---|---|
| 0 | open | passive | 1.2 mm (reading noise) | 0 | 0 | 0 | 0.0003 m/s |
| 0 | speed | passive | 1.2 mm | 0 | 0 | 0 | 0.0001 m/s |
| 10 mm | open | passive | 25.0 (24.5) mm | 1.24 | 3.66 | 0 | 0.164 m/s |
| 10 mm | speed | passive | 5.8 (5.6) mm | 0.53 | 3.74 | 0 | 0.045 m/s |
| 10 mm | open | skyhook | 24.2 (23.1) mm | 1.19 | 1.38 | 0 | 0.167 m/s |
| 10 mm | speed | skyhook | 6.0 (6.2) mm | 0.59 | 1.48 | 0 | 0.047 m/s |
| 25 mm | open | passive | 60.7 mm | 3.58 | 7.63 | 11.9 g | 0.442 m/s |
| 25 mm | speed | passive | 29.9 mm | 1.41 | 9.39 | 0 | 0.116 m/s |

Accelerations in m/s². |A(f₁₁)| is the Fourier amplitude of a_gx at 3.214 Hz (3.263 Hz on 3 mm). The linear estimate of what the
speed loop lets through at the swing frequency is |S| = 0.39; measured: 0.28 (|A|), 0.23 (lean). The figure 3.9 mm for the
speed-controlled lean in earlier notes was not reproduced: with fixed 5 ms steps the peak over the run is 5.8 mm (4.0 mm before
1.5 s), about 1 mm of which is reading noise. The smallest tyre load at a step's end was 4.4 N: the wheel did not leave the road.

Open (6 November 2026): the one-mode swing equation (17), driven by the measured jolt (t < 0.7 s), predicts a lean of 22.1 mm in
open loop (solver: 18.5 mm fitted after the bump, followed swing by swing) and 7.8 mm with speed control (solver: 1.3 mm fitted,
at the reading noise). Why the solver's stout swings so much less under speed control is not established. Not the grid: the 3 mm
runs give the same ratios (21.7 vs 17.5 mm open loop, 7.8 vs 1.2 mm speed control; series in `notes/fig12/runs/`). Not the stout's push on the cart: with it switched off (`node notes/fig12/nopush.cjs
<speed|off> 0`) the solver leaves 17.4 mm (predicted 21.6) in open loop and 1.4 mm (predicted 7.9) with speed control.

## The store and the data panel

One store (`Sim.dataset`), written where computed: `Cart.forces` and `Cart.sample` (state, forces, motor current, command,
reachable current, voltage, back-EMF, suspension force and command, the samples the controller used), `World.advance` (the fluid
step, momenta, spill momentum, the stout's push), `World.attach` (particles `px, py, pz` and column heights `h_col` are the store's
arrays), `StoutView` (the drawn surface `eta_draw`, front and back heights, pixels). Checks recompute every derived value from stored
inputs (the motor's and controller's formulas, the envelope from the road written out again, the poured mass by integrating the
profile, the column heights by counting the stored particles and inverting the glass's column table); state and constants are read
from the live solver. Read-backs: the head's cream at the front and back wall, the axle hub, the body's outline. Measured: 128 checks
(123 while spilling, `spill-test.cjs`), none differ; read-backs all true.

## Not in the model

The exact imperial glass shape; foam; surface tension (it would raise f₁₁ by 0.77 % with σ = 0.072 N/m at R = 40 mm, 0.78 % to first order); the wall boundary layer
and so the real damping; swirl that breaks the mirror symmetry; air drag on drops; measured motor and sensor data (the drive's
numbers are a plausible small motor); pitch and roll of the cart.

## The lecture note (rewritten 6 November 2026)

Sixteen sections, equations (1)–(49), two inline SVG figures from `tools/fig12/figures.cjs`, Key-result boxes, worked examples with
the page's numbers, Problems at the end of §15. §3 the stout in the glass's frame (the fictitious force, boundary conditions, mirror
symmetry, the quasi-static tilt); §4 ★ linear sloshing of a cylinder (potential flow, Bessel, ξ₁₁ = 1.8412, the dispersion relation,
the forced mode and the equivalent spring and mass, Abramson eq. 6.27; the tulip); §5 Froude, Bond, Reynolds, the boundary layer and
the damping (Abramson eq. 4.10b, Stephens et al. 1962); §6 the quarter car (envelope, the road's normal, M_x, energy, frequencies);
§7 the DC motor; §8 the PI loop and the sensitivity S(s); §9 the skyhook; §10 the coupling derived from Newton's law for the stout
with spill; §11 ★ the numerical method (Chorin, MAC, APIC, cut cells, Zhu–Bridson level set, ghost fluid, PCG with MIC(0), CFL);
§12 checks; §13 the parameter study. Every number is printed by `theory.cjs`, `check.cjs`, `study.cjs` or `energy.cjs`. Sources were
downloaded and read at the sections cited; Karnopp et al. (1974) only in its abstract (the paper could not be obtained).

## The live model and the controllers (6 November 2026)

**Default: the live model** (`ModalFluid` in `stout-cart.js`; the page without a query string, or `?model=live`). The stout as its
first three sloshing modes m = 1, n = 1–3 of a cylinder of radius R(h) (note, eq. 54): frequencies 3.421, 5.821, 7.365 Hz; damping
ζ₁ = 0.0053 (Abramson eq. 4.10b, K = 5.23), ζₙ = ζ₁ √(ω₁/ωₙ); forced by the glass's acceleration, with ω² scaled by 1 + a_z/g;
symplectic Euler, 0.5 ms substeps. Surface and momentum by eq. (55); the stout's push on the cart through the same coupling as the
3D model. The pour: a sharp-crested weir, C_d (2/3)√(2g) D^{3/2} per unit rim length, C_d = 0.62 (the Francis equation, USBR
Water Measurement Manual ch. 7 §9, eq. 7-4: 3.33 ft^½/s = 0.623 in SI), integrated round the rim; the volume is subtracted (the fill
falls, the modes' crest shrinks by that volume), not drawn. The page advances it by the clock's real time: 1.00 s simulated per s.
The column grid of the 3D solver is filled from the modes (`h_col`), so the store and the drawing read alike; no particles.
`?grid=4` and `?grid=3` run the 3D solver as before (buttons "3D · 4 mm", "3D · 3 mm").

Against the 3D solver (4 mm), one bump at 1 m/s (`MODAL=1 node tools/fig12/study.cjs …`): lean 24.7 vs 25.0 mm (10 mm, open loop),
7.6 vs 5.8 (10 mm, PI), 73.9 vs 60.7 and spilled 9.9 vs 11.9 g (25 mm, open loop), 25.4 vs 29.9 mm (25 mm, PI).

**Controllers** (`Cart.sample`, every 1 ms): `off`, `speed` (PI, as before), `preview` (PI plus i_ff = (M_s + m_w) g z_a′(x + ẋ τ_i)/b,
note eq. 50), `slosh` (LQR on x = (δv, q₁, q̇₁, ξ), note eqs. 51–53; Bryson weights 0.05 m/s, 2 mm, 2 mm·ω, 0.02 m, 3 A; Riccati
flow integrated in `Cart.lqrGains`: K = (75.0, −1939, −38.8, −150); closed-loop poles −12.0 ± 8.8j, −2.6, −244 s⁻¹, swing damping
ratio 0.81; live model only, the swing read as an ideal sensor). Lean over one bump, live model: 10 mm 24.7 / 7.6 / 0.8 / 0.4 mm,
25 mm 73.9 (9.9 g spilled) / 25.4 / 5.9 / 1.3 mm for off / PI / preview / slosh; largest current ≤ 2.32 A.

**Live charts** (`StoutView.drawCharts`, drawing only, from the numbers the page records each frame): the last 4 s of the lean and
the motor current with the rim as the limit; the first mode's phase portrait (q₁, q̇₁/ω₁) with the rim as vertical lines.

**Tests** (`notes/fig12/`; `QUERY='?grid=4'` runs them on the 3D solver): live model, `panel-test2.cjs` 151 checks and
`spill-test.cjs` 151 checks, none differ, read-backs true; 3D, 133 and 133, none differ; `threads-test.cjs` identical;
`ctrl-shots.cjs` screenshots each controller over the 25 mm bump (`live-*.png`, not committed: `notes/.gitignore`).
