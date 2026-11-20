# Fig. 16 spill: the flight as an exact linear map, the rim source as the only unknown (20 Nov 2026)

Written by the reviewing session for the working session, on the owner's order. **Nothing here has been run.** Every claim is
marked Fact (with a handle), Inference or Opinion. Read section 0, then do section 9 in order, one step per yes.
This replaces the picture-pair transport in `tools/fig16/derived/derive_liquid.py` (optimal transport, crossing windows,
arrival velocities). It keeps everything already proven (section 1).

## 0. Why the present route keeps failing (Inference)

1. It derives a velocity from two neighbouring pictures. A piece of liquid is in the air for 10 to 16 pictures (section 6),
   so nine tenths of the information about its velocity is thrown away, and what is left is dominated by sampling noise.
2. Its checks compare one noisy subsample with another, so every verdict is limited by a noise floor (129 % at 5 mm).
3. The only noise-free data in the stored ride are the counters `nact, nfly, nstuck, nlanded`: all N = 1 001 952 markers,
   241 pictures, balance 0.0000 g (Fact: `STATE-derived-20-nov.md`, result 1). They were used for totals only. Their *time
   curves* are a time-of-flight measurement of the whole spill and were never used.

The cure: stop reconstructing the flight. The flight is known exactly. Only the launch at the rim is unknown, and it is a
small unknown that every picture and every counter constrains at once.

## 1. Kept as proven (Fact, handles in `STATE-derived-20-nov.md`)

Counters close exactly. The stored flight integrates the full frame equation (`stout_jax.py:381-391, 871-875`). 90 to 98.5 %
of the 75.57 g leaves the lip. The deck model `puddle_ideal.py` passes mass and the incline. Rules R1 to R19 of the handoff.

## 2. The physical setup

A glass glued to a cart. The cart hits a kerb, pitches and decelerates. Seen from the glass, gravity swings and jumps, and a
tongue of stout is thrown over the rim. Once a piece of stout has left the rim it touches nothing: air on both sides, so the
pressure in it is atmospheric and its gradient is zero. Each piece then moves like a thrown stone, seen from a frame that
accelerates and turns. That is the whole flight. Air drag is absent in the stored ride and stays absent (R5).

Symbols. Glass frame: x along the cart, y across, z up, origin on the glass's inner floor. S = (0, 0, z_S) is the point the
frame turns about, z_S = h_g − FLOOR_ABOVE_DECK (`run16.py`, summary `zS`). ω(t) pitch rate, α = dω/dt. g_x(t), g_z(t):
effective gravity at S (stored `gx, gz`). X = x, Z = z − z_S. R_rim, z_rim: rim radius and height (`guinness-glass.js`).
m_p marker mass. Q(t) = −m_p d(nact)/dt: mass over the rim per time (exact).

## 3. The flight equation is linear, so one 4×4 matrix carries every piece of liquid

From `frame_accel` (`stout_jax.py:381-391`), term by term:

    dvx/dt = g_x + α Z + ω² X + 2 ω vz        (uniform part, Euler, centrifugal, Coriolis)
    dvz/dt = g_z − α X + ω² Z − 2 ω vx
    dvy/dt = 0                                 (the frame turns about y only)

Every term is of first degree in (X, Z, vx, vz). With the state s = (X, Z, vx, vz):

    ds/dt = A(t) s + b(t),      A = [[0, 0, 1, 0], [0, 0, 0, 1], [ω², α, 0, 2ω], [−α, ω², −2ω, 0]],   b = (0, 0, g_x, g_z)
    y(t) = y0 + vy0 (t − t0)

Let Ψ(t) solve dΨ/dt = A Ψ, Ψ(0) = 1 (the fundamental matrix), and p(t) = ∫₀ᵗ Ψ(τ)⁻¹ b(τ) dτ. Then (variation of constants;
check by differentiating):

    s(t) = Ψ(t) [ Ψ(t0)⁻¹ s0 + p(t) − p(t0) ]                                                              (1)

**Consequence.** Integrate one 4×4 system once along the ride (Ψ and p at each picture time and at sub-steps). After that the
position of any piece of liquid at any time is two matrix products. No per-marker integration, no time-window rule.

**Free check.** tr A = 0, so det Ψ(t) = 1 for all t (Liouville's formula, d(det Ψ)/dt = tr A · det Ψ). Physically: the flight
conserves phase-space volume, the Coriolis force does no work and does not compress. The integrator must return
|det Ψ − 1| < 1e-9.

**The kerb (Inference).** The stored g_x, g_z are samples at 60 per second and miss part of the shock (Fact: 2.75 m/s² rms
miss within 0.1 s of t = 0.72 s, `fig16-puddle-test` v2). Only the time integral of b matters in (1). So build b so that its
integral over each picture interval equals the change of the velocity of S, turned into the glass frame, taken from the
stored cart state (`v, vzc, om, th`), plus gravity. The shock then enters as the right impulse even though its shape is
unknown. Derive that expression from `cart4.py` and write it down before coding it.

## 4. The only unknown: the source at the rim

The solver releases a marker when it is outside the cavity at r > R_rim, or above the grid top (`stout_jax.py:865-867`,
`leave = act & (over | top)`). So the launch surface is known: the cylinder r = R_rim, z ≥ z_rim (plus the grid's top plane).
Coordinates on it: azimuth θ and height ζ above the rim. Launch time t0.

Unknown fields on that surface:

    q(t0, θ, ζ) ≥ 0     mass per time, angle and height        with  ∫∫ q dθ dζ = Q(t0)   exactly, from the books     (2)
    u(t0, θ, ζ)         the velocity with which that liquid leaves (3 components)

**Assumption A1 (cold sheet).** Liquid leaving one place of the rim at one instant has one velocity: the tongue is a coherent
sheet, not a spray. What breaks it: two populations at one (t0, θ, ζ). The hold-out test of section 7 detects that; the
remedy is one extra unknown, a velocity spread σ(t0).

**Size of the unknown (Opinion, tunable).** Mirror symmetry in y (the ride is planar): q, u_r, u_z even in θ, u_θ odd. Use
cosines up to order 4 in θ, linear in ζ, linear splines in t0 with one knot per picture while Q > 0 (about 30 knots). That
is of order 10³ numbers. First guess: u_r = Q/(ρ b h_rim) and q ∝ h_rim from the stored surface H (the lip test's numbers,
`lip_detach.py`: median 0.42 m/s), u_z = ∂H/∂t at the rim.

## 5. The forward model: what the stored ride would show for a given source

For a source (q, u): take fixed quadrature nodes (t0, θ, ζ) with weights q dθ dζ dt0, carry each with (1), and apply the
*stored solver's own* rules: freeze when crossing z = −14 mm inside |x| < 110 mm, |y| < 60 mm (`stout_jax.py:876`); count as
landed below z = −250 mm (`:878`). This gives predictions of everything that is stored:

    N̂_fly(t_j), N̂_stuck(t_j), N̂_landed(t_j)                   the three counters, per picture
    M̂_jc                                                       mass in flight in cell c of a coarse grid, per picture j
    F̂_c                                                        frozen mass per cell of the old plane, at the end

The model is differentiable in (q, u) once crossings are written with crossing times, not with yes/no tests.

## 6. Why the source is well determined (Inference, numbers to be recomputed by the session)

Fall from the rim to z = −14 mm: H₁ = z_rim + 0.014 m. With no launch speed, T₁ = √(2H₁/g) ≈ 0.17 s for H₁ ≈ 0.14 m, that is
10 pictures; to −250 mm about 0.28 s, 16 pictures. Each (t0, θ) cohort has 3 unknown velocity components and is seen in 10 to
16 pictures plus three exact counters: overdetermined about tenfold.
Sensitivities: ∂x_land/∂u_x = T₁ ≈ 0.17 s, so a 10 mm landing cell resolves 0.06 m/s. ∂T₁/∂u_z ≈ −T₁/(g T₁) = −0.10 s per m/s,
so one picture (17 ms) resolves 0.17 m/s, and the exact counter curves resolve far finer.

## 7. Estimation and the test, with the noise where it belongs

**Statistics (Fact about the data).** Picture j lists a fraction λ_j = listed/ndrops of the markers. A listed count in a cell
is then a Poisson variable with mean λ_j M_jc / m_p. This is the same statistical problem as emission tomography: unknown
non-negative source, linear transport, Poisson counts (Shepp & Vardi 1982, IEEE Trans. Med. Imaging 1, 113). The estimator is
maximum Poisson likelihood, not L1 distance. Use only pictures with a complete listing (ndrops ≤ m_drops); a truncated listing
is taken by index and is biased (`stout_jax.py:1076`, `run16.py:176`). Losing those pictures costs little here, because each
cohort is seen in many pictures.

**Fit on** (i) the listed in-flight markers of the EVEN complete pictures, on 10 mm cells, Poisson likelihood; (ii) N_fly(t).
Minimise

    J = Σ_{j even, c} [ λ_j M̂_jc/m_p − n_jc ln(λ_j M̂_jc/m_p) ] + Σ_j (N̂_fly − N_fly)²/(2 s²) + μ ‖D(q, u)‖² + μ_b ‖u − u_b‖²

subject to (2) exactly (parametrise q as Q times a normalised share). D: first differences in t0 and θ. Choose μ by the
discrepancy principle: the largest μ for which the Poisson deviance per datum is about 1 (Morozov). This is variational data
assimilation with a perfect model and the boundary source as control (Le Dimet & Talagrand 1986, Tellus 38A, 97).
The gradient comes from automatic differentiation (JAX); minimiser L-BFGS.

**Test on what the fit never saw:**
- T1, exact, no noise floor: the curves N_stuck(t) and N_landed(t), all 241 pictures. PASS if the largest deviation is at
  most 5 % of the final value (1.6 g of 32.29 g; 2.2 g of 43.28 g) and the half-rise times agree within one picture.
- T2: the ODD pictures' fields, as deviance per datum; PASS if at most 1.5 (1 is perfect, the noise is in the likelihood).
- T3: the final frozen field F̂_c against the stored frozen markers, 10 mm cells, same deviance mark.
Marks are Opinion; the owner fixes them before the run.

**Twin first (the step that ends the wasted runs).** Before any real data: choose a source by hand, produce fake pictures and
counters with the forward model and the same thinning λ_j, run the fit on them, and compare the recovered deck fluxes with
the known ones. PASS if within 5 % per 20 mm cell-second. A method that cannot recover a known answer is not run on the ride.

## 8. The corrected ride: the same source, the right geometry

With the fitted source, carry the liquid again with (1), now with what the stored solver lacked:
1. The glass is solid outside: a path that meets the outer wall below the rim joins the wall film. Liquid whose lip number
   D < 1 (`lip_detach.py`) joins it at once. Film on the wall: u = g_t h²/(3ν), to the foot of the glass, then the deck.
2. Fig. 16's deck: the plane z = −30 mm, 310 × 124 mm. Per deck cell and time: mass flux ṁ and tangential momentum flux
   ṁ u_t, by crossing time, with no window. What passes the edge is off the deck.
3. The head (14.4 mL, density 0.27 ρ): the same chain, its source constrained by `foam_spill`.
The total is 75.57 g by constraint (2). T1 to T3 are what make the positions and times believable.

Deck (already built): ∂h/∂t + ∇·(h ū) = ṁ/ρ;  ∂(hū)/∂t + ∇·(β h ū ū) = −g_n h ∇h + h a_t − 3ν ū/h + ṁ u_t/ρ, deck-frame
a_t impulse-exact as in section 3, free outflow at the edges. State β as used in `puddle_ideal.py`.

## 9. Order of work (each step one yes; time estimate and live monitor for every Kaggle run)

1. `flight_map.py`: Ψ, p from the stored ride. Checks: det Ψ = 1; with ω = 0 and constant g, (1) is the parabola; with
   constant ω and b = 0, (1) equals a straight inertial line turned by −ωt (fixes the sign convention). Seconds on CPU.
2. Forward model and the twin of section 7. No ride data needed beyond the frame. About a minute on CPU.
3. The fit on the stored ride; T1, T2, T3. Estimate: 10³ unknowns, 10⁴ nodes, 241 pictures, all matrix products: minutes on
   Kaggle CPU. A GPU is not needed and would not improve the answer (Opinion).
4. Section 8: `deck_source.npz` from the fitted source; then the deck stage; mass on and off the deck at 4 s.
5. Outputs committed, docs section, player.

## 10. Assumptions, and what would break each

| | assumption | broken if | seen in |
|---|---|---|---|
| A1 | one launch velocity per (t0, θ, ζ) | spray, rebound | T2 deviance > 1.5 |
| A2 | b impulse-exact at 60 per second is enough | liquid in flight during the shock is displaced by its shape | T1 half-rise times near t = 0.72 s |
| A3 | complete pictures are unbiased samples | the thinning is not even | quarters-against-halves ratio ≠ 1.41 |
| A4 | launch surface r = R_rim | many markers leave through the grid top | count them in step 1; add the top plane |
| A5 | the stored solver's in-glass flow is right | (not testable from outside; the owner's premise) | — |

## Sources
Liouville's formula and variation of constants: any ODE text, e.g. Arnold, Ordinary Differential Equations, §27.
Shepp & Vardi 1982, doi 10.1109/TMI.1982.4307558. Le Dimet & Talagrand 1986, doi 10.3402/tellusa.v38i2.11706.
Viscous spreading check: Huppert 1982, J. Fluid Mech. 121, 43, doi 10.1017/S0022112082001797.
Tools: JAX (autodiff, jit), SciPy L-BFGS-B, NumPy. All open source, all on Kaggle's image.
