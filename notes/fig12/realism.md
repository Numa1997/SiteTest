# Fig. 12, realism: the plan in mathematics (6 November 2026)

Numa's brief: a curvy surface, a better-looking drink, a 3D camera, a controller designed by control theory that holds
the stout steady, a stable foam head, spilling that visibly leaves the glass and is counted, phase spaces with their
constraints, and all of it grounded in real observations. This note says, in formulas, what each of these means for
the page, what is drawing and what is physics, and what has to be read first. Nothing here is built yet.

Notation is that of the lecture note on the page: glass frame (x along the road, y across, z up), inner radius R(z),
fill h = 125 mm, rim z_rim = 147.5 mm, surface height η(x, y, t) above the floor, first mode height q(t) at the front
wall, ω₁₁ the swing frequency, β = 2ξ tanh(ξh/R)/(ξ² − 1) = 1.54, cart speed v, motor current i, b = 5 N/A, M_x = 2.50 kg.

## 1. The picture: a 3D camera, a smooth lit surface, a dark drink (drawing only, no new physics)

What exists: the solver's column heights h_ji on the 20 × 10 grid, read on a polar grid of 9 × 48 points and drawn as
flat polygons from 14° above. What changes: how those stored numbers are drawn. The store keeps them; the picture
only reads.

**Camera.** A pinhole camera at elevation ε (about 22°) and azimuth φ (about 25°, so the far wall and the surface's
depth both show), focal length f. A point P = (x, y, z) in the glass frame maps to camera coordinates by two
rotations and a translation, then to the screen by

    (X, Y) = f · (p_c,x / p_c,z,  p_c,y / p_c,z),        p_c = R_ε R_φ (P − P_cam).

The cart and road share the camera, so the whole scene is one consistent view.

**The surface as a smooth sheet.** The column heights are volume-exact per column but piecewise constant. For the
drawing, interpolate them with a bicubic Catmull–Rom spline, η̃(x, y), which is C¹: the surface then bends instead of
stepping. The spline passes through the column values, so what is drawn at each column centre is exactly the stored
number (the panel's read-back stays true). Its gradient gives the unit normal for lighting,

    n = (−∂η̃/∂x, −∂η̃/∂y, 1) / √(1 + |∇η̃|²).

**Lighting.** One light direction l, viewer direction e, reflection r = 2(n·l)n − l; Phong's model
I = I_a + I_d max(0, n·l) + I_s max(0, r·e)^p. Realism comes from the specular term sliding over the curved surface as
it tilts.

**The drink's colour.** Stout is nearly opaque, ruby only where thin. Along the view ray through the liquid of path
length ℓ, Beer–Lambert transmission T = exp(−κℓ) mixes the ruby of thin edges into the black of the body; ℓ is found
from the glass's section R(z) and the surface. κ is a drawing constant to be tuned by eye with Numa (the skill
`tune-with-numa`), not a physical number.

**Spilling visibly.** The drops already exist (every particle that crosses the rim, with its mirror image, falls under
gravity). They are drawn as isolated dots. Instead: a sheet. Build the drops' level set with the same Zhu–Bridson
kernel the solver uses for the liquid, φ_d(x) = |x − x̄| − r_d, render its zero set in the camera as a translucent
sheet or ribbon running over the rim, with single drops where they separate. The counted mass m_spilled = 2 m_p × (drops)
is unchanged and stays in the readout and the store; a thin bar on the glass can show the liquid level falling
(h now = V⁻¹(m_ℓ/ρ)).

## 2. The foam head (physics, calibrated to a measurement)

The page draws a 12 mm cream layer on the computed surface. A real head is a few millimetres of wet foam, a
viscoelastic solid at small strain, and it damps sloshing strongly: that is Numa's observation, and it is the subject
of A. Sauret, F. Boulogne, J. Cappello, E. Dressaire and H. A. Stone, "Damping of liquid sloshing by foam", Phys. Fluids
27, 022103 (2015). That paper must be read before any number is taken from it; nothing is quoted here from memory.

**Model.** A tangential drag on the liquid within a layer of thickness d_f under the surface, standing for the foam
dragging on the liquid it rides on:

    ∂u_∥/∂t = … − u_∥ / τ_f      for  η − d_f < z < η,

applied to the particles in that layer each step (one line in `Fluid.forces`); u_∥ is the velocity along the surface.

**What it does to the mode (derived).** The mode's velocity decays with depth as e^{k(z−h)}, so its kinetic energy
density goes as e^{2k(z−h)}. The layer holds the fraction ∫_{h−d_f}^h e^{2k(z−h)} dz / ∫_0^h e^{2k(z−h)} dz ≈ 2k d_f
of the kinetic energy when d_f ≪ 1/k. A velocity that decays as e^{−t/τ_f} loses energy at the rate 2/τ_f; over a
cycle the kinetic energy averages half the total E; so

    dE/dt = −(2/τ_f)(2k d_f)(E/2) = −(2k d_f/τ_f) E,    and with E ∝ e^{−2ζωt}:    ζ_foam = k d_f / (ω τ_f).

Given a measured ζ_foam from Sauret et al. (for a comparable foam depth; stout's own foam has not been measured for this
page, and the note will say so), choose τ_f = k d_f / (ω ζ_foam). Check: `check.cjs freq` with the layer on must give
that damping ratio, and the frequency must not move by more than the layer's share, 2k d_f.

**Drawing the head.** The head sits on the liquid and is drawn as a layer of constant thickness on η̃; a foam that
damps the surface is calm because the surface is. No separate foam dynamics are invented.

## 3. The controller that holds the stout steady (control theory, the main new physics)

**The plant.** Cart plus first mode, from (35) and (17) of the note, with the mode's damping ζ:

    M_x δv̇ = b δi − c_x δv + F_d(t)                       (F_d: the road's push and everything else)
    q̈ = −ω² q − 2ζω q̇ − β δv̇
    ξ̇ = v₀ − v                                             (the speed error's integral)

Substituting δv̇ from the first line makes it a linear system ẋ = A x + B u + E F_d with x = (δv, q, q̇, ξ), u = δi:

    A = [ −c_x/M_x        0        0      0 ]      B = [  b/M_x    ]      E = [ 1/M_x     ]
        [    0            0        1      0 ]          [   0       ]          [   0       ]
        [ βc_x/M_x      −ω²     −2ζω     0 ]          [ −βb/M_x   ]          [ −β/M_x    ]
        [   −1            0        0      0 ]          [   0       ]          [   0       ]

The lean the page can measure is Δη = 2q (front wall minus back). A real cart would carry a level probe or a camera
for it; the page reads it from its own store, and the note will say the sensor is ideal.

**Three controllers, chosen on the page, each with its analysis in the note.**

(a) *PI speed loop* (exists): u = K_p(v₀ − v) + K_i ξ. Rejection of F_d at ω₁₁ by |S(jω₁₁)| = 0.39.

(b) *Road preview feedforward* (the waiter who sees the step coming). The road ahead is known, z_r(x), so the push it
will give is known: F̂_road(t) = −N̂ z_a′(x(t)), with N̂ the static load (M_s + m_w)g or, better, the tyre load from the
quarter-car solved ahead along the known road. Command i_ff(t) = −F̂_road(t + τ_i)/b, advanced by the current lag.
Then a_g = (F_road − F̂_road)/M_x, the error of the estimate only. The current needed over a 10 mm bump is 2.7 N / 5 N/A
= 0.55 A, inside the 3 A limit; over 25 mm the dynamic load matters. Added to (a).

(c) *Slosh-state feedback* (LQR). u = −K x with K from the cost J = ∫ (x^T Q x + r u²) dt, Q weighting q and q̇ (hold the
stout) and ξ (hold the speed), r the current's cost. K solves the algebraic Riccati equation; the closed-loop poles
are eig(A − BK). The note gives the poles, the gain on the lean (A per mm) and the transfer |q/F_d|(jω) for each
controller on one plot: that is the analysis "according to control theory". Sampling 1 ms, the current limit and
anti-windup as now.

**Why (b) beats everything a feedback loop can do, in one line.** A feedback loop acts after the glass has already
moved; preview acts before. Only the estimate's error reaches the stout. The honest limit: it needs the road ahead,
which a real cart would get from a camera or a map; the reader's pushes are not previewable, and against them (c) is
the better tool.

(d) *Shaped pushes* (optional): the reader's push command passed through a zero-vibration shaper, two impulses half
a period apart, so that a push does not ring the stout. Standard input shaping; cheap to add.

## 4. Phase spaces and their constraints (new panel figures, drawn from the store)

1. **The slosh mode, (q, q̇).** The trajectory of the first mode, with q read as Δη/2 and q̇ by differencing the
   store. The constraint: the rim, |q| = z_rim − h = 22.5 mm, drawn as two vertical lines; a trajectory that crosses
   them is spilling. One portrait per controller, so the reader sees the loop shrink.
2. **The drive, (v, i).** The feasible set of the drive is the parallelogram |i| ≤ I_max, |R_a i + b v| ≤ V_max
   (the current limit and the voltage left over the back-EMF). The controller's path is drawn inside it; where it
   touches the edge the controller is saturated, and anti-windup is at work.
3. **The cart's heave, (z_b − z_b,rest, ż_b)** with the skyhook on and off.

Each is a live inline chart reading the store, in the house chart style, and each also appears as a static figure in
the note from a saved run.

## 5. The boundary conditions, said plainly

The solver's conditions stay: no flow through the wall and floor (free slip), p = 0 at the free surface, mirror
symmetry y → −y, open rim. The fictitious force −a_g(t) is the only effect of the glass's translation, and it is
exact: the glass does not rotate (lecture note, §3.1). The foam layer of §2 adds a dissipative term in a thin band under
the surface. The no-slip wall layer (0.3 mm) stays unresolved; the note says so and gives its damping estimate.

## 6. What must be read first (none of it quoted yet)

- Sauret, Boulogne, Cappello, Dressaire, Stone, "Damping of liquid sloshing by foam", Phys. Fluids 27, 022103 (2015):
  the foam damping, its measured decay rates, how they scale with foam thickness.
- H. C. Mayer, R. Krechetnikov, "Walking with coffee: why does it spill?", Phys. Rev. E 85, 046117 (2012): measured
  sloshing of a drink carried by a person, the natural frequencies, how spilling starts. The "external source of
  intuitive experience" for the doorstep.
- R. A. Ibrahim, *Liquid Sloshing Dynamics* (2005), the chapter on slosh suppression and control, for (c) and (d).
- A reference for LQR and for input shaping (Singer & Seering 1990 for zero-vibration shapers).

## 7. Order of work, each step tested in the browser before the next

1. The 3D camera and the smooth lit surface, Beer–Lambert colour, the spill sheet (drawing; store unchanged).
2. The controllers (b) and (c) in `Cart`, selectable; the plant matrices and gains printed by `theory.cjs`; the
   lecture note's §8 extended with the analysis; the parameter study rerun.
3. The foam layer after reading Sauret et al.; calibration by `check.cjs freq`; note §5 and §14 updated.
4. The phase-space charts; the data panel's ledger extended with q, q̇, the feasible-set test.
5. Docs, inventory, screenshots, merge.

The one decision that changes the work: whether the foam enters the physics (step 3) or stays drawn.
