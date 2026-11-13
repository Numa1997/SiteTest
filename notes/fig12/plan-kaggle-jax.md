# Plan: the lecture note of the Kaggle page of Fig. 12, rewritten for the JAX solver (13 November 2026)

Page: `public/simulations/guinness-kaggle.html`, only inside `<article class="paper" id="paper">`. Doc: the Kaggle part of
`docs/simulations/fig12-beer-slosh.md`, and `docs/kaggle-pipeline.md`. Standard: `notes/STANDARD.md`, verdict of 21 October 2026
(Taylor's *Classical Mechanics*: every step shown, symbols defined where they first appear, Key result boxes, numbered worked
examples with the page's numbers, Problems at the end, ★ on the heavy parts with their results restated). The page has no
walkthrough (`data-walk` is absent), so there is no walkthrough file to keep in step.

Why: the old note described the Taylor solver of 12 November (water's viscosity, no head, a polar surface of 17 rings, a live
preview, hollow speed dots, "version 5"). None of that is on the page any more. The page plays rides computed by
`tools/fig12/kaggle/stout_jax.py` (run by `run_b.py`, packed by `pack_ride.py`, drawn by `guinness-jax-play.js` and
`stout-view2.js`). Run 4 is computing; its packed data (`public/data/fig12/2026-11-13/index-jax.json`) is not in the repository
yet, so the results section gives its method and leaves one paragraph, marked `<!-- RESULTS-RUN4 -->`, for the numbers.

## The chapter, section by section

1. **A full pint on a bumpy floor.** The everyday picture: the surface rocks a few times a second; steps in time with it
   build it up; the head, lying 3.5 mm below the rim, is what leaves first. What the page shows (stored rides, nothing
   computed here) and the road map of the chapter.
2. **The pint, measured.** Glass profile R(z) (`guinness-glass.js`), fill 125 mm, R at the fill 39.1 mm, rim 147.5 mm; stout
   1007 kg/m³, 2.06 mPa s, ν = 2.05 × 10⁻⁶ m²/s (Benilov et al.); head 19 mm, R32 = 34 µm, liquid fraction 0.27, γ 44.2 mN/m,
   E∞ 18.7 mN/m (Völp & Willenbacher, Table 2). Table of inputs with their sources. Example: the head's weight, 51 Pa, 5.1 mm
   of stout; its volume and mass.
3. **The swing of the surface ★.** Potential flow, eqs. (2)–(5), f11 = 3.421 Hz (the old section 3, kept, re-derived in SymPy).
   Then the mode driven by the glass's push and heave: q̈ + ω²(1 + a_z/g)q = −β a, β = 2ξ tanh(ξh/R)/(ξ² − 1) = 1.541, derived
   by projecting r cos θ on J1 (wall share 2/(ξ² − 1) = 0.837). Example: the steady push that lifts the wall by a given height.
4. **Three thin layers the grid cannot see.** The Stokes layer derived (★): δ = √(2ν/ω) = 0.44 mm; the wall stress has an
   in-phase part ρ√(νω/2)u, which is exactly what the code applies, and a reactive part. Damping of the mode from the energy
   integrals (★): ζ_wall = δ(ξ² + 1)/(4R(ξ² − 1)) = 0.0051, which is Miles's constant 3.50 (Stephens et al. print 3.52;
   their experiments 5.23, ζ = 0.0077); the skin under the surface, 0.0051; the bulk, 0.0004. Key result: the bare stout rings
   with ζ ≈ 0.011.
5. **The head of foam.** What a foam is; generalized Laplace pressure 2400 Pa; G0 = 166 Pa, τy = 5.4 Pa; Tcholakova's flow law
   (11.7 Pa at 10 s⁻¹); the head as a sheet in vertical shear (`head_sheet`), its implicit equation; Cantat's wall friction
   (9.7 Pa at 10 mm/s) over h_eff = 9.9 mm; the head's weight on the stout; the spill rule ρ_f(|g|e/2 + a_out e) ≥ τy,
   e* = 4.06 mm at rest. A rough balance (labelled as such): the yield stress can hold a swing of about 0.5 mm at the wall.
6. **The cart, and who pushes whom.** The cart of Fig. 12 in one paragraph (numbers from `CART_COMMON`), the glass's frame
   (g − a_g), the coupling F = −dP/dt from Newton's third law, the impulse book (telescoping sum, so impulse = −P exactly;
   the cart feels each step's push one step later). The four tasks of `run_b.py`. Example: the cart carrying a frozen pint on
   each road (peak push, heave, the undamped swing each road would leave in the first mode).
7. **How the computer does it.** Particles and grid (370,386 cells, 1,001,952 particles, 7.93 per cell), APIC transfers
   (Jiang et al. eqs. 12–14), the order of one step as `Stout.step` runs it, cut-cell face fractions (Batty et al.), pressure by
   preconditioned conjugate gradients (tolerance 10⁻⁵, at most 600 iterations), the ghost-fluid surface, the level set of Zhu &
   Bridson and the two radii (0.9 dx and 0.505 dx, the second derived), the surface read-out, time step (2 ms, CFL 0.8, 17 steps
   a stored frame at rest), the cart's 0.1 ms sub-steps, precision.
8. **A pint at rest must stay at rest.** The lesson of run 3: in equilibrium the pressure cancels gravity exactly, so nothing
   moves and nothing is dissipated; the energy books of run 3 (`rest.npz`) showed 0.77 mJ "dissipated" against 0.63 mJ of
   potential energy lost; the two causes (the head pressing only the inner columns; the thin layers braking gravity's kick
   before the pressure step could cancel it), each explained as physics; the guard; the same check on this machine before and
   after the fixes.
9. **Playing the stored rides.** What one stored frame holds and in what steps; frame k = round(30 T), never blended, real
   time, stop at the end; SHA-256; words four times a second; what is drawn from data and what is drawing.
10. **What the computed rides show.** Predictions first (from sections 3–6), then the method by which each number is read from
    the stored data; one paragraph with `<!-- RESULTS-RUN4 -->` for the measured numbers.
11. **Limits, and the next model.** What is left out (the head's inertia: it would lower f11 to about 3.07 Hz, derived; the
    contact line; the film on the glass; drainage; bubbles; drops as single particles; the method's own damping); the
    controller as the next step. Problems.
12. **Sources.** Only those opened: Benilov et al. (extract), Völp & Willenbacher (KIT copy, Table 2), Stephens et al. (NTRS
    PDF, eqs. 1–3, 13), Abramson SP-106 ch. 4 (extract), Bongarzone & Gallaire (extract, eq. 17), Cantat (extract), Tcholakova et
    al. (extract), Sauret et al. (extract), KegWorks (extract), Watamura et al. (extract), Jiang et al. (PDF), Zhu & Bridson (PDF),
    Batty et al. (PDF), the Fig. 12 note.

Figures (inline SVG in the house chart style, plotted from the page's own numbers): the glass to scale with stout, head and rim;
the Stokes layer's velocity profile at four phases against one grid cell; run 3's energy books against time.

## The numbers, and how each is measured

| Number | How |
|---|---|
| R(z), R(125 mm) = 39.1 mm, rim 147.5 mm, volume 426.6 mL, 429.6 g | `Geometry` and `glass_volume` of `stout_jax.py` run on this machine's CPU at dx = 1.5 mm |
| 57 × 57 × 114 = 370,386 cells; 1,001,952 particles; 7.93 per cell; head on 2217 columns, 91.31 mL, 24.8 g | `Stout(G, "full")` on the CPU |
| ν, δ, √(νω/2), f11, f12, f13, β, ζ_wall, ζ_skin, ζ_bulk, the Miles constant | SymPy and SciPy script: the mode, the Stokes layer and the energy integrals re-derived and evaluated |
| G0, τy, flow stress, wall stress at 1–100 mm/s, h_eff, e* | the functions of `stout_jax.py` called directly |
| the cart's push, heave and the undamped swing per road | `Cart` of `stout_jax.py` run alone (frozen load, F = 0) at 0.1 ms sub-steps, 2 ms steps |
| run 3's books | read from run 3's stored `rest.npz` (Kaggle output) |
| one step from rest, old and new code; books over 0.1 s | `Stout.step` of commit `eb7471f` (run 3) and of the present code, CPU, dx = 1.5 mm |
| the read-out radius 0.505 dx | Zhu & Bridson's φ over an ideal seeded lattice, read between cell centres as the code reads it |
| the player: frame rule, rate, words per second, the end | the built page (`npm run build`) in headless Chromium (Playwright), with run 2's packed files served in place of run 4's |
| the note renders | the built page at 390 and 1440 px: KaTeX errors, numbered equations, sideways scroll |

Run 4's numbers (rest guard, free swing f and ζ, lean, spill, timing) are left to the paragraph marked `<!-- RESULTS-RUN4 -->`.
