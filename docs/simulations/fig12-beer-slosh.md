# Fig. 12 · A Pint of Guinness on a One-Wheel Cart (`public/simulations/beer-slosh.html`)

Rebuilt from zero on 6 November 2026 after Numa rejected the previous Fig. 12 (modal sloshing in a Blender-sculpted glass, LQR,
three languages). Nothing of it is reused. The page is **English only**: `tools/i18n/build.py` lists it in `ENGLISH_ONLY`, so no
German or Arabic page is generated, and links to it from the German and Arabic pages point at the English page.

## What the page does

A cart with one wheel, one spring and one damper carries a pint of stout over cosine bumps (25 cm long, one every 2 m). The stout is
a live three-dimensional incompressible Navier–Stokes computation in the frame of the glass; the cart follows Newton's laws; the two
are coupled both ways. The reader can push the cart forward or back (buttons or ← →), set the push force, the bump height and the
cruising speed, pause and start again. The caption shows how many seconds of simulated time pass per real second (measured in
headless Chromium on the build machine: 0.19 on desktop and phone viewports).

## Files

| File | Job |
|---|---|
| `public/simulations/beer-slosh.html` | the page: figure, controls, readouts, lecture note; the run loop (`Sim.clock`, 28 ms of solving per frame) |
| `public/scripts/stout-cart.js` | the solver: `Fluid` (APIC on a MAC grid), `Road`, `Cart`, `World` (coupling). Runs in the browser and in Node |
| `public/scripts/stout-view.js` | the drawing (canvas 2D); reads the solver's state and computes nothing physical |
| `tools/fig12/check.cjs` | offline checks: `node tools/fig12/check.cjs rest|freq|tilt` |
| `notes/fig12/test.cjs` | browser test (desktop and 390 px phone): run advances, push works, no errors, no sideways scroll |
| `notes/fig12/clip.html`, `clip.cjs` | renders a clip of the run (PNG frames, MP4) |
| `public/images/sims/beer-slosh.webp` | catalog thumbnail, 800 × 500, a frame of the page |

## The model

- **Stout**: Du/Dt = −∇p/ρ + ν∇²u + g − a_g(t), ∇·u = 0, p = 0 on the free surface, no flow through the wall and bottom (free slip).
  a_g is the glass's mean acceleration over the step, handed from the cart. Glass: upright cylinder R = 4 cm, fill 10 cm (503 g),
  box height 13.2 cm (a lid the liquid should not reach). ρ = 1000 kg/m³, ν = 10⁻⁶ m²/s (water's).
- **Symmetry**: forcing in the x–z plane, round glass, so the flow is mirror-symmetric about y = 0; only y ≥ 0 is solved (v = 0 on
  y = 0; the level set and the column heights use mirror images).
- **Cart**: x, z_b, z_w; rigid wheel R_w = 4 cm whose axle follows the envelope z_a(x) of the road; radial tyre
  N = max(0, k_t(z_a − z_w) + c_t(ż_a − ż_w)); horizontal road force −N z_a'(x); spring k = 600 N/m, damper c = 8 N s/m, tyre
  k_t = 2·10⁴ N/m, c_t = 5 N s/m; body and glass 1.5 kg + stout; wheel 0.3 kg (disc); drag c_x = 2 N s/m with a constant drive
  c_x v₀; the reader's push. Symplectic Euler at 0.1 ms.
- **Coupling**: the stout's reaction is −dP/dt, P its momentum relative to the glass (both halves), lagged one fluid step; its rigid part
  (weight, carried mass) is in the cart's masses.

## The numerical method (`stout-cart.js`)

APIC transfers (Jiang et al. 2015), 2 × 2 × 2 particles per cell (30 498 in the half glass at 4 mm); MAC grid 20 × 10 × 33 at 4 mm;
fluid step 5 ms on the page. Wall: open fractions of the cell faces (slivers under 10 % closed); faces closed by the wall are filled by
extrapolation so particles sliding along it are not braked (free slip). Free surface: Zhu–Bridson level set from the particles (with
mirror images in y = 0 and in the wall), ghost-fluid pressure, θ ≥ 0.05; a cell holding particles counts as liquid with φ ≥ −0.05 dx.
Pressure by PCG with MIC(0), warm-started. Velocity extrapolated three layers into the air.

**Settings found by measurement (6 November 2026), keep them:**
- φ for particle-holding cells −0.05 dx, not −0.5 dx: −0.5 dx shifted the free swing to 4.26 Hz on the 4 mm grid.
- Time step: at rest on 4 mm with a broken surface setting, Δt = 1/100 s gave 0.18 m/s of spurious flow and 1/400 s 0.014 m/s; with the
  settings above 4 mm and Δt = 1/200 s is clean and swings at the right frequency. 5 mm with Δt = 1/100 s is wrong (2.68 Hz).
- The particle separation step (`relax`) exists but is off: not needed, and slow.

## Checks (measured)

| Test | Expected | Measured |
|---|---|---|
| rest 1.5 s, 4 mm, Δt 2.5 ms | no flow | fastest particle 11 mm/s, surface 0.46 mm rms |
| free swing, 4 mm, Δt 5 ms | 3.382 Hz (linear theory, ξ = 1.8412, h = 10 cm) | 3.390 Hz, damping ratio 0.019 |
| free swing, 3 mm, Δt 2.5 ms | 3.382 Hz | 3.354 Hz, damping ratio 0.005 |
| depth at rest from the particle columns | 100 mm | 99.5–100.6 mm |
| browser test (`notes/fig12/test.cjs`) | runs, push works | 0.19 s/s; push → speed 0.99 → 1.77 m/s in 2.5 s; no errors; 0 px overflow at 1440 and 390 px |

## The drawing (`stout-view.js`) and where it differs from the store

- The surface drawn is the **column height**: particle volume (dx/2)³ over each grid column divided by its open area, both smoothed by
  the same 3 × 3 binomial filter (`Fluid.columnHeights`). Within 2.5 cells of the wall the height is extended linearly along the radius
  from 2.5 and 4 cells in, because cut columns hold too few particles. Overturning waves and drops cannot show.
- **The head is drawn, not simulated**: a 12 mm cream layer on the computed surface.
- The glass is seen from 14° above; the readouts are rewritten every 15 frames (about four times a second).

## Not in the model

Tulip shape of the real glass; foam; surface tension; spilling (lid at the box top); the wall boundary layer and so real damping (the
numerical damping is larger: ζ = 0.019 at 4 mm); swirl that breaks the mirror symmetry; pitch and roll of the cart. No data panel yet.
