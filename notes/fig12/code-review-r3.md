# Fig. 12 · code review, round 3 (the cart version)

Reviewed 5 November 2026 at commit `5b7d09a` ("Fig. 12 cart version (checkpoint)"): `public/simulations/beer-slosh.html`
(classic script lines 540–1258, module 1259–1427) against `tools/fig12/plant.py`, `controller3.py`, `road.py`, `geom.py`,
`modes3d.py`, `build_modes3d.py` and the shipped `public/scripts/slosh-modes.js` (format 3, quick mesh: 13 radial nodes).
Line numbers are those of the file at that commit. Every "reproduced" item ran in headless Chromium (Playwright, SwiftShader,
1440 × 900) against `http://localhost:8765/`. The probe scripts are in the session scratchpad (`r3/t1.cjs` … `t3.cjs`), not in
the repository. No repository file was changed.

What matches: `assemble()` 783–806 is `plant.assemble` term by term (rigid masses, the liquid's centre of mass at
Z_floor + 0.55 (Z_s − Z_floor), M[x,ψ], M[z,ψ], M[ψ,ψ] with J_ry and 2 m_l h_g z_cm, the strut outer products, the inverted-pendulum
term, the modal rows with (1 + κ), the couplings ρQN, ρQN h_g + ρQ_ry N and −gρQN). `design()` 836–894 is `controller3.design`
(state layout d_f, d_r, ζ_f, ζ_r, a_n | ẋ_c, ż_b, ψ̇, ż_f, ż_r, ȧ_n; ψ = (d_r − d_f + ζ_r − ζ_f)/(l_f + l_r); the ZOH by one matrix
exponential; the Riccati iteration; the cost on η_rim, ψ, ż_b, u). `ctlState()` 895–901 is `ctl_state`. `control()` skyhook signs
are right (front corner rate ż_b − l_f ψ̇). `deriv()` 914–928 has the road through k_t z + c_t v ż′, the actuators with the right
signs on body, pitch and wheels, and the parametric term ρ N z̈_O a_n clamped at −0.8 g with z̈_O lagging one substep, as
`controller3.simulate` does. Index use (IX … IA, np_ = 4 + nx) is consistent everywhere. The cylinder record (708–728) has the
stored layout: `field[k][level][node][Φ | ∂_r | ∂_z][cos | sin]`, `psi[k] = [c[], s[]]`, I_w, I_b, I_s pre-divided by E. The
read-backs test alpha before colour (1171–1172). Nothing on the 3D view reacts to the pointer merely crossing it.

## Findings, by severity

### 1. The mode data changes sign from fill to fill; the interpolation between fills cancels the slosh (bug, high)

- **Where**: `public/scripts/slosh-modes.js` (the data), `interpGlass()` 694–707 (the linear interpolation), `modes3d.solve`
  182–186 (the sign rule that was meant to prevent this).
- **Problem**: within each stored fill the shape and the couplings are consistent (Q_x ψ_rim > 0 always), but the overall sign of
  a mode flips between neighbouring fills. For (1, c, 1) the rim value at θ = 0 is +1 at 300 mL, −1 at 320–360, +1 at 380, −1 at
  400–460, +1 at 480, −1 at 500–540, +1 at 560–576. `interpGlass()` interpolates ψ, Q_x, Q_y, Q_rx, Q_ry linearly between the two
  fills around V, so halfway between two fills of opposite sign the mode shape, its rim value and its couplings are all zero.
- **Evidence**: from the file, Q_x(1,c,1) and Σ_k c_k(s = 1): 480 mL +0.03306 / +1.0000; 500 mL −0.03273 / −1.0000. On the page
  (V slider, 5 mL steps): at 490 mL `M[k].Qx` = 0.00017 m (0.5 % of its value), `rim_n` = 5 × 10⁻⁶, the LQR gain on a₁ = 0.1 N/m
  (16 864 N/m at 480 mL). Reader-visible: the 40 N "along the road" shove gives a peak rim wave of 8.88 mm at 480 mL, 2.58 at
  485, **0.73 at 490**, 2.54 at 495, 8.80 at 500. Affected slider positions, x-type (1,1): 305–315, 365–375, 385–395, 465–475,
  485–495, 545–555; y-type (1,1): 325–335, 405–415, 465–475, 485–495, 505–515, 525–535, 545–555, 565; (1, c, 2): 425–435,
  565–570. The data panel cannot see this: `rim_n`, `Qx` are stored and the checks recompute from them.
- **Why**: the rule in `modes3d.solve` works on a synthetic ring (−cos θ and −sin θ both flip), so the shipped file was built
  without it or before it. It is the quick-mesh file (13 radial nodes; the production build has 17).
- **Fix**: (a) guard in the page regardless of the data: in `interpGlass()`, before mixing `a` and `b`, compute the sign
  σ = sign(Σ_k Σ_j (c_a c_b + s_a s_b)) over the ψ components and flip `b`'s ψ, Q_x, Q_y, Q_rx, Q_ry by σ when σ < 0 (same for the
  field fill `f`). (b) In `build_modes3d.py`, after the solve, print and assert the sign continuity of each (m, o, n) across fills,
  and rebuild. (c) Add a data-panel check that the normalisation holds for every mode: max_θ |ψ_k(1, θ)| = 1 — it is 0 at
  490 mL today. (d) Add 490 mL to `regress.cjs` (shove peak within 10 % of 500 mL).

### 2. The 3D body pitches the wrong way (bug, high)

- **Where**: module line 1383, `cart.rotation.z = q[S.IP]`.
- **Problem**: the page's ψ is "front down positive" (`plant.py` lines 7–8, the store's `psi` long_name, the readout "Tilt of the
  glass", `ctlState`'s d_f = z_b − l_f ψ − z_f). The mapping is z_three = −y_physics (line 1273), so a rotation by ψ about
  y_physics is a rotation by **−ψ** about z_three. three.js's `makeRotationZ(θ)` sends (l_f, 0) to (l_f cos θ, l_f sin θ): with
  `rotation.z = +ψ` the front goes **up**. The glass, the tray and the strut tops follow the wrong tilt; the wheels (drawn from
  z_f, z_r) do not, so on a bump the front wheel rises while the body's front dips, and the struts stretch and shrink the wrong way.
- **Evidence** (reproduced): ψ = +0.1 rad set in the store, two renders: world y of the frame's front corner 0.2399 m, rear
  0.1601 m; from the physics (0.20 + z_b ∓ 0.4 × 0.1) front 0.160, rear 0.240. Glass foot drawn at x = 0.0745 m; physics
  x_O = d_g + h_g ψ = 0.125 m (0.075 would be d_g − h_g ψ). Readout at the same moment: "Tilt of the glass +5.73°" (front down).
- **Fix**: `cart.rotation.z = -q[S.IP]`. Then `axisScreen()`'s axes and the arrows are unaffected (they do not use the body's
  rotation). Add a read-back the panel can run: the glass group's world matrix against (d_g + h_g ψ, h_g − d_g ψ, −ψ), so the
  3D view is no longer the one picture that is "not read back" (`about`, 1238).

### 3. `design()` runs 113 ms on every slider event (performance, medium)

- **Where**: 1121 (`cartSl`), 1127 (`ctlSl`), the Riccati loop 872–880.
- **Problem**: `Sim.slider` fires `onInput` on every `input` event, i.e. every pixel of a drag. Each call rebuilds A, B, the
  exponential and iterates the Riccati equation to 10⁻¹¹; with `mmul` allocating a fresh matrix per product that is 1129
  iterations × ~5 matrix products of 13 × 13. The clock caps dt at 50 ms (`sim.js` 179), so each event also loses 60 ms of
  simulated time and the picture stalls at about 8 frames a second while M_b, k, c, σ_η, σ_ψ, σ_v, σ_u, I_max or T_s is dragged.
  `I_max` does not enter the design at all (it is only the clamp in `control()`), and the design is recomputed in passive and
  skyhook mode too.
- **Evidence** (reproduced): five `input` events on `se`: 113.0 ms each, `Ct.iters` = 1129, n = 13.
- **Fix**: debounce: mark the design dirty on `input` and run it once per animation frame (or on `change`), skip it for `I_max`,
  and only when `P.law === 'lqr'` (run it on switching to LQR). Faster convergence: start the iteration from the previous S instead
  of Q (a slider moves a little), or use the doubling (Anderson–Moore) recursion, which converges in about 20 steps; keep `Ct.iters`
  in the store. Also set `Ct.ok = isFinite(K[0][0]) && it < 6000` so a non-converged design is not used silently.

### 4. A pinch that starts during a push leaves the push on for ever (bug, medium, touch devices)

- **Where**: 1356 (`pointers.size === 2` → `drag = pinch`), 1371 (`up`).
- **Problem**: with pointer A pushing the body (`drag.kind === 'push'`, `push.until = 1e9`), a second finger turns `drag` into a
  pinch without zeroing the push. When either finger lifts, `up` sees a pinch (or `drag === null`) and never calls `S.setPush(0)`.
  The cart is then pushed with the last force until the reader drags the body again (`restart` clears it too).
- **Evidence** (reproduced with `setPointerCapture` stubbed so synthetic pointer events reach the handler): A down on the body,
  move 40 px → F = 35.5 N; B down, B move (view zooms: dist 1.55 → 1.43); B up → F = 35.5 N; A up → F = 35.5 N,
  `push.until` = 10⁹, `is-grab` already removed. `pointercancel` and `lostpointercapture` go through the same `up`, so they do not
  help.
- **Fix**: at the start of a pinch, if the current drag is a push, call `S.setPush(0)` and clear the hint; in `up`, zero the push
  whenever `push.until === 1e9` regardless of `drag.kind`. (Also: `setPush` resets `peak` on every `pointermove`, so "highest wave
  since the last reset" during a push is only the wave since the last mouse movement; reset it once, on `pointerdown`.)

### 5. Restarting under LQR after a kerb kicks the cart with the old road height (bug, medium)

- **Where**: `restart()` 947–951 and `ctlState()` 897 (`road.zf`, `road.zr`).
- **Problem**: `road.zf/zr` are written only in `deriv()`. `restart()` zeroes the state but not `road`, and `control()` runs at the
  first `step()` before any `deriv()`, so the first sample sees ζ_f = z_f − z_rf = −(old road height) and the gains on ζ
  (−4382 and 2648 N/m) answer with a force that is held for one T_s.
- **Evidence** (reproduced): LQR, kerb (20 mm), 3 s; `restart()`; first sample u_f = −34.7 N, u_r = −36.5 N (a clean restart:
  −0.0006 N); the next sample +3.4 N. That is a 0.7 N·s impulse on a 26 kg body, a visible jolt at t = 0, and the same after
  cobbles or the rough road, whose height at the end of a run is arbitrary.
- **Fix**: in `restart()` set `road.zf = zRoad(P.lf)`, `road.zr = zRoad(−P.lr)` (both 0 for every profile), or call `deriv` once
  before the first `control()`.

### 6. The rough road starts with a step and a derivative spike (bug, medium-low)

- **Where**: `zRoad()` 815 (`case 'rough'`), `dzRoad()` 824; the same in `road.iso_random` (`np.where(x > x0, z, 0)`).
- **Problem**: the sum of 120 sinusoids with fixed phases is −5.37 mm at x = 0⁺, so the road has a step there (rms of the profile
  6.9 mm, so the step is of the profile's own size, a small kerb that ISO 8608 does not contain). The central difference over
  100 µm straddles it: dz/ds = −53.7, times v = 1.5 m/s gives a tyre rate of −80 m/s and a c_t spike of 1600 N for whichever RK4
  stage lands within ±50 µm of s = 1 m. Also, `h_road` (the slider, set to 30 mm by `ROAD_H.rough`) is not used by this profile.
- **Evidence** (reproduced, passive, v = 1.5): front-wheel speed in the first 5 cm of the feature 0.74 m/s, later on the same
  road at most 0.12 m/s (6 ×). `zRoad(2.0)` = −8.48 mm with h_road = 1 mm and with 30 mm.
- **Fix**: subtract the profile's value at x = 0 (or window it in over 0.2 m), and either scale the rough profile by h_road/30 mm
  or leave the slider at its old value and say in the hint that the rough road has its own height. Do the same in `road.py`.

### 7. The store's `K` is labelled for three x-modes; there are two (doc, medium-low)

- **Where**: 616, the long_name "(d_f, d_r, ζ_f, ζ_r, a₁, a₂, a₃, ẋ_c, ż_b, ψ̇, ż_f, ż_r, ȧ₁, ȧ₂, ȧ₃)".
- **Problem**: the data has nx = 2 x-type modes ((1, c, 1), (1, c, 2)), so n = 13 and the layout is (d_f, d_r, ζ_f, ζ_r, a₁, a₂,
  ẋ_c, ż_b, ψ̇, ż_f, ż_r, ȧ₁, ȧ₂, 0, 0, 0). A reader takes K[6] = −44.8 for the gain on a₃; it is the gain on ẋ_c.
- **Evidence**: `ds.get('K')` = [775.3, −959.2, −4382.5, 2647.5, −16830.8, −15448.5, −44.8, 171.6, −249.6, 9.4, −8.0, 96.1,
  −215.8, 0, 0, 0]; `Ct.n` = 13, `Ct.nx` = 2.
- **Fix**: build the long_name from `Ct.ax` in `design()` (the panel reads attrs live) or write "a₁..a_nx, then the rates".
  Related: `tau_cl` = 1.928 s is M_rig/c_x = 1.915 s, the cart coasting along x, which the actuators barely touch (K on ẋ_c is
  −44.8 N per m/s). The readout "slowest time constant of the closed loop" therefore reports the rolling resistance, not the
  suspension. Either leave ẋ_c out of the design state (it is uncontrollable from u_f, u_r up to the small M[x,ψ] coupling) or
  report the slowest eigenvalue among the modes with a nonzero share in z_b, ψ, a_n.

### 8. The wheel over the 3D view takes the page scroll (usability, medium-low)

- **Where**: 1373 (`wheel`, `preventDefault`, `{ passive: false }`); CSS line 33 (`touch-action: none`).
- **Problem**: every wheel event over the canvas zooms and is prevented, so a reader scrolling the page with the pointer over
  the figure (16:10, full column width) is stopped there and zooms instead. On a phone a swipe that starts on the view cannot
  scroll either. Round 2 (item 13) flagged the same on the old page and it was changed to Shift+wheel; the new page reverted
  to the plain wheel and the instructions (line 83) now promise it.
- **Evidence** (reproduced): pointer over the canvas, wheel +300: `scrollY` 240 → 240, `view.dist` 1.55 → 2.22.
- **Fix**: zoom on Ctrl/⌘+wheel (the browser's own zoom gesture, which `preventDefault` may take) or on Shift+wheel, and let a plain
  wheel scroll; `touch-action: pan-y` so a vertical swipe scrolls and a horizontal one turns; say so in step 2 of the instructions.

### 9. The struts are drawn from the previous frame's body pose (bug, low)

- **Where**: 1388, `applyMatrix4(cart.matrixWorld)`.
- **Problem**: `cart.position` and `cart.rotation.z` are set at 1383, but `cart.matrixWorld` is only updated inside
  `renderer.render()` at the end of the frame, so the strut top is one frame stale (and at the identity on the first frame,
  before any render). The wheel end is current. On a bump at 60 Hz the mismatch is the body's travel in one frame (a few mm);
  with finding 2 fixed it is still there.
- **Evidence** (reproduced): after a render with ψ = 0.1, set ψ = 0, z_b = 0.05 and render once: strut `scale.y` front 0.160,
  rear 0.080; the frame corner to the wheel centre is 0.170 for both.
- **Fix**: `cart.updateMatrixWorld(true)` right after setting its position and rotation, or compute the top as
  `cart.position + cart.quaternion · (lx, 0, sz·WB/2)`. Dead code on 1389–1390: `st.g.lookAt;` (an expression statement that does
  nothing) and `st.damper.scale.set(1, 1, 1)`.

### 10. `axisScreen()` projects a point one metre away; near the camera it flips (bug, low)

- **Where**: 1348–1350.
- **Problem**: the screen direction of the push axis is taken from the projection of `cart.position + 1 m`. With the camera at
  0.5–1.0 m (zoomed in) and the axis pointing at it, that point is behind the camera or strongly foreshortened: the sign of the
  drag direction inverts, or `pxm` (pixels per metre) is 10 × too large and the hand's stiffness 10 × too small.
- **Evidence** (reproduced): az = π/2, dist 0.5: the 1 m point projects to NDC y = +2.89 (behind the camera); the local direction
  from a 5 cm offset is −0.113 (opposite sign). az = π/2, dist 1.0: NDC Δy = −11.35 for 1 m against −0.057 × 20 = −1.13 for the
  5 cm offset scaled, i.e. 10 × off.
- **Fix**: use a short offset (0.05 m) and scale `pxm` by 20, or project the direction with the camera's view matrix (the derivative
  of the projection at the cart).

### 11. The straight glass carries the tulip's liquid mass and inertia and no pitch coupling (model gap, low)

- **Where**: `cylinder()` 724 (`Qrx: 0, Qry: 0`), `assemble()` 785 (`fill.V_liq`, `fill.J_ry` are the tulip's at that V).
- **Problem**: the "straight" option keeps R and D of the tulip's surface but a cylinder of that radius and depth holds
  π R² D = 0.476 L, not V. The sloshing modes are exact, but the rigid part of the liquid (m_l, J_ry, z_cm) is the tulip's, and
  the rotational forcing of the m = 1 modes is set to zero although for a cylinder it is not (for the tulip Q_ry/(Q_x h_g) = 0.29, so
  29 % of the pitch forcing of the slosh is missing in the comparison).
- **Evidence**: with `cyl` at 300 mL, `m_liq` = 0.302 kg, ρ π R² D = 0.479 kg; `M[0].Qry` = 0, `M[0].Qx` = 0.0331.
- **Fix**: either say in `about` that the straight glass is the tulip's liquid in a straight wall (modes only), or compute
  V = π R² D, J_ry and Q_ry for the cylinder (Q_ry has a closed form from the Stokes–Joukowski series; or solve it once offline with
  `modes3d` on a straight wall and store it).

### 12. At low fills the stored field rows below the floor are drawn on the floor (drawing, low)

- **Where**: `gridPos()` 979 (`Math.max(ZF, …)`), `cylinder()` 716–723.
- **Problem**: the field grid of the 500 mL fill reaches 136 mm below its surface; at 300 mL the stout is 97 mm deep, so rows with
  d > D are clamped to Z_floor and drawn there, one on top of another, with velocities that belong to a deeper point (tulip) or to
  a mirrored depth (cylinder, where cosh(k(D − d)) is even in D − d and sinh changes sign).
- **Evidence** (reproduced, 300 mL): drawn rows at z = 8.0 (floor), 14.9, 40.4, … mm. Cylinder, ȧ₁ = 10 mm/s: the floor row
  reads u = (0.22, 0, −0.20) mm/s, a vertical velocity through the floor (row 15, near the surface: 6.9 mm/s).
- **Fix**: skip rows with d > D (or draw them at depth d·D/D_field). Line 718 holds a dead expression
  (`… * 0 - fz[i] + … * 0`) overwritten on 719; delete it.

### 13. Small things (nits)

- `hist` points carry `qA[IZ]` (1058) that `drawTrace` never reads.
- `deriv()` 917: the tyre rate uses v alone; the wheel's ground speed is v + ẋ_c (up to ±0.3 m/s under the hand, 20 %), small
  because c_t = 20 N·s/m.
- `readouts()` 1090 reads `P.hd` where the store has `h_dome`.
- `restart()` does not write `u_f`, `u_r`, `z_rf`, `z_rr` to the store; they show the last run's values until the next sample/frame.
- `Ct.ok` (881) ignores non-convergence (see 3).
- Per frame the 3D surface costs about 7 ms of script on this machine: 1224 `etaAt` calls at 5.1 µs each (each loops the 14
  modes with a `for … in` over the ψ components and interpolates), plus `Rin` with a linear search over 81 profile points. Tabulate
  per frame, per mode and component, the radial profiles at the 17 radii and cos/sin at the 72 angles; the surface then costs
  under 1 ms. (`step()` is 8.5 µs on the smooth road, 95 µs on the rough one: 720 sines per `deriv`; fine either way.) While
  paused the clock still redraws the cut, the trace and the 3D view every frame (dt = 0): skip the draws unless the view moved.
- The German and Arabic pages (`public/de|ar/simulations/beer-slosh.html`) are still the old shaker page (they have `wsl`, no
  cart), as `status.md` says; none of this applies to them until they are rebuilt.

## What the data panel's checks cannot catch, and what would

- Finding 1: a check `max_θ |ψ_k(1, θ)| = 1` for every mode (the normalisation the data promises).
- Finding 2 and 9: a read-back of the 3D view's glass group (world matrix) against (d_g + h_g ψ, h_g − d_g ψ, −ψ) and of a strut's
  length against its two ends.
- Finding 5: a check that at t = 0 `u_f = u_r = 0` when the state is zero.
- Finding 6: a check `z_road(1 m⁺) = 0` for every profile.
- Finding 3: `Ct.iters` in the store with a check `iters < 6000`.
