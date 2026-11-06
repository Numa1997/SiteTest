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
second (measured in headless Chromium on the build machine: 0.15–0.18 at 4 mm).

## Files

| File | Job |
|---|---|
| `public/simulations/beer-slosh.html` | the page: figure, controls, readouts, lecture note, store and data panel; the run loop (`Sim.clock`, 28 ms of solving per frame) |
| `public/scripts/stout-cart.js` | the solver: `Fluid` (APIC on a MAC grid, wall R(z), spillage), `Road`, `Cart` (motor, controller, suspension, hand), `World` (coupling, drops). Runs in the browser and in Node |
| `public/scripts/guinness-glass.js` | the glass's inner radius every 0.5 mm, written by `tools/fig12/glass_profile.py`; do not edit |
| `public/scripts/stout-view.js` | the drawing (canvas 2D); reads the solver's state and computes nothing physical |
| `tools/fig12/glass_profile.py`, `irish-imperial-pint.svg`, `glass_profile.json` | the glass measured from dimensions.com's section and scaled to 160 × 85 mm |
| `tools/fig12/check.cjs` | offline checks: `node tools/fig12/check.cjs rest|tilt|cyltilt|cylfreq|freq|spill [dx] [steps/s]` |
| `notes/fig12/test.cjs` | browser test (desktop, phone): run, push with and without the speed loop, drag, no errors, no sideways scroll |
| `notes/fig12/panel-test.cjs`, `panel-test2.cjs`, `spill-test.cjs` | data panel: every check and read-back; on a bump at three widths, Read values, a round, Save, idle; while spilling |
| `notes/fig12/clip.html`, `clip.cjs` | renders a clip of the run (PNG frames, MP4) |
| `public/images/sims/beer-slosh.webp` | catalog thumbnail, 800 × 500 |

## The glass

dimensions.com's "Irish Imperial Pint Glass" (the tulip; a 16 oz glass, 149.2 mm, 3 in) has a dimensioned section. Its inner
outline was measured from the SVG rendered at 4× (the widest outer diameter measures 76.6 mm against the stated 76.2 mm) and
scaled to the Guinness imperial glass as retailers list it, 160 mm × 85 mm widest: heights × 1.0724, radii × 1.1096. Result: inner
radius 28 mm low, 39.3 mm widest (113 mm up), 37.5 mm at the rim (147.5 mm); brim volume 530.7 ml (an imperial pint is 568 ml:
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
  the rim in the step; m_ℓ falls as it spills.
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
- With a particle radius of 1 spacing the stout could not hold a steady tilt (centre of mass 15 % of exact, also on the version
  then live): on a tilted surface many cells hold particles but read φ ≥ 0, were forced liquid at φ ≈ 0, and the ghost-fluid
  coefficient kicked them every step, driving a circulation down the high wall. 1.8 spacings removes it (`check.cjs cyltilt`).
- The wall must be met along its normal: radial projection in the rounded bottom corner drained the pint (0.37 m/s at rest).
- Wall images need the test `z < z_rim`, not `R < R_box` (the cylinder lost them: 3.12 Hz instead of 3.39).
- A level-set extension into wall cells (constant or linear) and a particle-density volume correction were tried and rejected:
  both broke the free swing (measured); the volume correction exists, off (`volumeCorrection: 0`).

## Checks (measured)

| Test | Expected | Measured |
|---|---|---|
| tulip at rest 1 s | no flow | fastest particle 3.2 mm/s (4 mm), 3.7 mm/s (3 mm) |
| straight glass R 40 mm, h 100 mm, free swing | 3.382 Hz | 3.235 Hz at 3 mm (−4.3 %), 3.176 Hz at 4 mm (−6.1 %) |
| steady push 2 m/s², centre of mass, straight | −0.815 mm | +3.6 % at 3 mm, +18.2 % at 4 mm |
| steady push 2 m/s², the tulip | −0.877 mm | +6.1 % at 3 mm |
| the tulip's free swing | no closed form | 3.263 Hz at 3 mm, 3.214 Hz at 4 mm |
| spill book-keeping | equal | 102.1 g left = 102.1 g counted |
| 1 cm bump at 1 m/s, front − back wall peak | — | 23.8 mm open loop, 3.9 mm speed control |
| same, heave peak | — | 3.74 m/s² passive, 1.48 m/s² skyhook |

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

The exact imperial glass shape; foam; surface tension (it would raise f₁₁ by 0.78 % with σ = 0.072 N/m); the wall boundary layer
and so the real damping; swirl that breaks the mirror symmetry; air drag on drops; measured motor and sensor data (the drive's
numbers are a plausible small motor); pitch and roll of the cart.
