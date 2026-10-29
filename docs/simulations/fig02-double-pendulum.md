# Fig. 2 · Double Pendulum

| | |
|---|---|
| Page | [public/simulations/Double Pendulum.html](../../public/simulations/Double%20Pendulum.html) (870 lines, 105 641 bytes) |
| Walkthrough | [public/scripts/walk/pendulum.js](../../public/scripts/walk/pendulum.js) (137 lines, 8 steps, key `pendulum`) |
| Thumbnail | [public/images/sims/double-pendulum.webp](../../public/images/sims/double-pendulum.webp) (WebP, 800 × 500 px, 12.5 kB; the pendulum, its fading trail and the protractor) |
| Catalog entry | [public/scripts/catalog.js#L65](../../public/scripts/catalog.js#L65) (`id: 'double-pendulum'`, `fig: 2`, `field: 'mechanics'`, `stage: 2`, lines 64–80) |

Links written `Lnnn` point into the page file; links to other files carry the file name.

The reader sees a pendulum hanging from a pivot at the centre of the figure: an upper rod with a burgundy bob and a lower rod with
a second burgundy bob, inside a faint protractor marked every 30° ([L44–52](../../public/simulations/Double%20Pendulum.html#L44-L52), [L631–657](../../public/simulations/Double%20Pendulum.html#L631-L657)). Released from θ₁ = 120°,
θ₂ = 150° ([L85](../../public/simulations/Double%20Pendulum.html#L85), [L89](../../public/simulations/Double%20Pendulum.html#L89)), it whips round in a way that never repeats; the lower bob leaves a burgundy trail that fades in about
1.4 s. A switch adds a pale "chaos twin" started 0.001 rad away, and a readout shows how far the two lower bobs have drifted apart
([L62](../../public/simulations/Double%20Pendulum.html#L62), [L104](../../public/simulations/Double%20Pendulum.html#L104)). Sliders set the mass and length ratios, the starting angles and angular velocities, and a time scale
([L63–98](../../public/simulations/Double%20Pendulum.html#L63-L98)); every slider except the time scale restarts the motion. The caption shows the simulated time; readouts show the
energy and its numerical drift ([L50](../../public/simulations/Double%20Pendulum.html#L50), [L101–105](../../public/simulations/Double%20Pendulum.html#L101-L105)). Under the figure sit the Data panel and the Read values switch (added by
`datalog.js`), the walkthrough ([L443](../../public/simulations/Double%20Pendulum.html#L443)) and the lecture note ([L115–441](../../public/simulations/Double%20Pendulum.html#L115-L441)).

## The physics in one picture

**Everyday picture.** Let your arm hang and swing it: the upper arm turns about the shoulder, the forearm about the elbow, and
the hand draws a path that neither joint alone would draw ([L140](../../public/simulations/Double%20Pendulum.html#L140)). Started gently, a double pendulum rocks regularly; started
high, it flips over the top and never settles. Nothing is random, yet two starts a thousandth of a radian apart end in unrelated
places within seconds: deterministic chaos ([L141–142](../../public/simulations/Double%20Pendulum.html#L141-L142)).

**Model.** Two point masses on rigid, massless rods in one vertical plane, no friction, no air ([L182](../../public/simulations/Double%20Pendulum.html#L182)). The upper mass and rod
are fixed at m₁ = 1 kg and l₁ = 1 m, and g = 9.81 m/s² ([L458](../../public/simulations/Double%20Pendulum.html#L458), [L184](../../public/simulations/Double%20Pendulum.html#L184)). Angles are measured from the downward vertical,
counter-clockwise positive ([L177](../../public/simulations/Double%20Pendulum.html#L177)). The state is the four numbers (θ₁, θ₂, ω₁, ω₂) ([L184](../../public/simulations/Double%20Pendulum.html#L184)). The note derives the equations
of motion from the Lagrangian L = T − V with the Euler–Lagrange equation (note §4, [L217–263](../../public/simulations/Double%20Pendulum.html#L217-L263)).

**What the code evaluates.** Positions, with the pivot at the origin and y upward ([L724–725](../../public/simulations/Double%20Pendulum.html#L724-L725)):

$$x_1 = l_1\sin\theta_1, \quad y_1 = -l_1\cos\theta_1, \quad x_2 = x_1 + l_2\sin\theta_2, \quad y_2 = y_1 - l_2\cos\theta_2 .$$

Energy, in `energy(s)` ([L561–566](../../public/simulations/Double%20Pendulum.html#L561-L566)):

$$T = \tfrac12 (m_1+m_2)\,l_1^2\omega_1^2 + \tfrac12 m_2 l_2^2\omega_2^2 + m_2 l_1 l_2\,\omega_1\omega_2\cos(\theta_1-\theta_2),$$

$$V = -(m_1+m_2)\,g\,l_1\cos\theta_1 - m_2\,g\,l_2\cos\theta_2 .$$

The angular accelerations, in `deriv(s)` ([L541–549](../../public/simulations/Double%20Pendulum.html#L541-L549)), with $\delta = \theta_1 - \theta_2$ and the shared denominator
$D' = 2m_1 + m_2 - m_2\cos 2\delta = 2(m_1 + m_2\sin^2\delta) > 0$:

$$\alpha_1 = \frac{-g(2m_1+m_2)\sin\theta_1 - m_2 g\sin(\theta_1 - 2\theta_2) - 2\sin\delta\; m_2\left(\omega_2^2 l_2 + \omega_1^2 l_1\cos\delta\right)}{l_1 D'},$$

$$\alpha_2 = \frac{2\sin\delta\left(\omega_1^2 l_1 (m_1+m_2) + g(m_1+m_2)\cos\theta_1 + \omega_2^2 l_2 m_2\cos\delta\right)}{l_2 D'} .$$

These are eq. (9) of the note ([L220](../../public/simulations/Double%20Pendulum.html#L220)), obtained from the linear system (8) by Cramer's rule ([L218–219](../../public/simulations/Double%20Pendulum.html#L218-L219)). With the state
$s = (\theta_1, \theta_2, \omega_1, \omega_2)$ and $F(s) = (\omega_1, \omega_2, \alpha_1, \alpha_2)$, one step of the classical
fourth-order Runge–Kutta method with $h = 1/600$ s is ([L550–560](../../public/simulations/Double%20Pendulum.html#L550-L560), note eq. 13):

$$k_1 = F(s), \quad k_2 = F\left(s + \tfrac h2 k_1\right), \quad k_3 = F\left(s + \tfrac h2 k_2\right), \quad k_4 = F(s + h k_3), \quad s \leftarrow s + \tfrac h6\left(k_1 + 2k_2 + 2k_3 + k_4\right).$$

The energy check divides the change of $E = T + V$ by the depth of the potential well, not by $E_0$, which can be near zero
([L722](../../public/simulations/Double%20Pendulum.html#L722)):

$$\varepsilon = \frac{E - E_0}{(m_1+m_2)\,g\,l_1 + m_2\,g\,l_2} .$$

| Symbol | Code | Unit | Meaning |
|---|---|---|---|
| $\theta_1, \theta_2$ | `state[0]`, `state[1]` | rad | rod angles from the downward vertical |
| $\omega_1, \omega_2$ | `state[2]`, `state[3]` | rad/s | angular velocities |
| $\alpha_1, \alpha_2$ | `a1`, `a2` in `deriv` | rad/s² | angular accelerations |
| $m_1, m_2$ | `m1 = 1`, `m2` | kg | bob masses; m₂ = m₁ e^slider ([L593](../../public/simulations/Double%20Pendulum.html#L593)) |
| $l_1, l_2$ | `l1 = 1`, `l2` | m | rod lengths; l₂ = l₁ e^slider ([L594](../../public/simulations/Double%20Pendulum.html#L594)) |
| $g$ | `g = 9.81` | m/s² | gravitational acceleration ([L458](../../public/simulations/Double%20Pendulum.html#L458)) |
| $\delta$, $D'$ | `d`, `den` | rad, kg | angle between the rods, shared denominator |
| $h$ | `H = 1/600` | s | RK4 step ([L458](../../public/simulations/Double%20Pendulum.html#L458)) |
| $T, V, E, E_0$ | `kin`, `pot`, `energy(s)`, `E0` | J | kinetic, potential, total, total at restart |
| $\varepsilon$ | `drift` | 1 | relative energy error |
| $\sigma$ | `scale` | px/m | pixels per metre on screen ([L575](../../public/simulations/Double%20Pendulum.html#L575)) |
| $d$ | `sep` | m | distance between the two lower bobs (twin on) ([L732](../../public/simulations/Double%20Pendulum.html#L732)) |

## How the code computes it

**State.** `state` is a plain array [θ₁, θ₂, ω₁, ω₂] in rad and rad/s, set from the sliders by `restart()` ([L595](../../public/simulations/Double%20Pendulum.html#L595)); `twin`
is a second such array or `null` ([L596](../../public/simulations/Double%20Pendulum.html#L596)). `E0` is the energy at restart ([L597](../../public/simulations/Double%20Pendulum.html#L597)); `simT` the simulated time and `acc` the
unspent time carried between frames ([L598–599](../../public/simulations/Double%20Pendulum.html#L598-L599)). `m2` and `l2` come from the log-scale sliders ([L593–594](../../public/simulations/Double%20Pendulum.html#L593-L594)). For drawing:
`ox`, `oy` (pivot) and `scale` (σ) ([L573–575](../../public/simulations/Double%20Pendulum.html#L573-L575)); the offscreen canvas `trail` that holds the fading path ([L462](../../public/simulations/Double%20Pendulum.html#L462)); `prevA`,
`prevB`, the last pixel positions of the two pendulums, from which the next trail segment starts ([L464](../../public/simulations/Double%20Pendulum.html#L464)). `frames`, `lastN` and
`fps` count frames, steps and frame rate ([L464–465](../../public/simulations/Double%20Pendulum.html#L464-L465)).

**Method.** RK4 at a fixed step h = 1/600 s ([L458](../../public/simulations/Double%20Pendulum.html#L458)). Its error over a fixed time scales as h⁴ (note §7, [L348](../../public/simulations/Double%20Pendulum.html#L348)). A fixed step
keeps the accuracy the same on every device ([pendulum.js:86](../../public/scripts/walk/pendulum.js#L86)). RK4 does not conserve energy exactly, so the page shows the
drift ε rather than hiding it ([L351](../../public/simulations/Double%20Pendulum.html#L351), [L701](../../public/simulations/Double%20Pendulum.html#L701)). `rk4()` builds separate trial arrays `s2`, `s3`, `s4`, so all four slopes of a
step use their own input state ([L551–558](../../public/simulations/Double%20Pendulum.html#L551-L558)). Measured in this session (1280 px window, default start, headless Chromium):
ε = −2.4 × 10⁻⁸ at t = 21.2 s, n = 10 steps per frame at 60 frames per second, energy E = 18.3057 J. Over the first 20 s
of the default start ε stays within ±5 × 10⁻⁸: read once per frame, its largest value is +4.710 × 10⁻⁸ at t = 8.665 s, its most negative
−3.185 × 10⁻⁸ at t = 19.13 s; step by step the peak is +5.0006 × 10⁻⁸ at t = 8.668 s (derivation check, 20 October 2026). The step is fixed,
but which step a frame reads depends on the frame times, so the per-frame peak varies between runs (4.71 to 4.99 × 10⁻⁸). The note says so ([L351](../../public/simulations/Double%20Pendulum.html#L351)).

**Sub-stepping.** Real frame times are uneven; the physics advances in equal steps. Each frame ([L762–765](../../public/simulations/Double%20Pendulum.html#L762-L765)):

$$\tau \leftarrow \tau + \Delta t \cdot \text{speed}, \qquad n = \min\left(\lfloor \tau / h \rfloor, 600\right), \qquad \tau \leftarrow \min(\tau - n h,\ h).$$

The leftover τ carries into the next frame, so simulated time keeps pace with wall time × speed. Because `Sim.clock` caps Δt at
0.05 s ([sim.js:179](../../public/scripts/sim.js#L179)) and the time scale is at most 1.5 ([L65](../../public/simulations/Double%20Pendulum.html#L65)), n is at most 46; the 600 cap never acts (see Notes).

**Frame loop** (`Sim.clock` callback, [L760–784](../../public/simulations/Double%20Pendulum.html#L760-L784)), in order:
1. If playing (Δt > 0): accumulate τ and choose n ([L762–765](../../public/simulations/Double%20Pendulum.html#L762-L765)). For each of the n steps: advance `state` by one RK4 step, compute
   its pixel positions, paint one trail segment of the lower bob, remember the position ([L767–770](../../public/simulations/Double%20Pendulum.html#L767-L770)); if the twin is on, do the
   same for it in rose ([L771–776](../../public/simulations/Double%20Pendulum.html#L771-L776)); add h to the simulated time ([L777](../../public/simulations/Double%20Pendulum.html#L777)). After the steps, dim the whole trail layer ([L779](../../public/simulations/Double%20Pendulum.html#L779)).
2. `diagnostics(dt)`: write every derived number of the final state into the store ([L781](../../public/simulations/Double%20Pendulum.html#L781), [L712–742](../../public/simulations/Double%20Pendulum.html#L712-L742)).
3. `draw()`: clear, protractor, trail image, twin, pendulum, pivot dot ([L782](../../public/simulations/Double%20Pendulum.html#L782), [L684–694](../../public/simulations/Double%20Pendulum.html#L684-L694)).
4. Every sixth frame, `readouts()` copies E, ε, the separation and the time from the store into the DOM ([L783](../../public/simulations/Double%20Pendulum.html#L783), [L697–708](../../public/simulations/Double%20Pendulum.html#L697-L708)).

While paused `Sim.clock` passes Δt = 0 ([sim.js:181](../../public/scripts/sim.js#L181)): no steps and no fading, but `diagnostics()` and `draw()` still run every
frame.

**`diagnostics(dt)`** ([L712–742](../../public/simulations/Double%20Pendulum.html#L712-L742)) evaluates `deriv` once more at the final state for the stored slopes and accelerations
([L713](../../public/simulations/Double%20Pendulum.html#L713)), copies the state ([L714](../../public/simulations/Double%20Pendulum.html#L714)), then computes and stores δ, D′, α₁, α₂ ([L717](../../public/simulations/Double%20Pendulum.html#L717)), the mass matrix M and its determinant,
the generalised momenta ([L718–720](../../public/simulations/Double%20Pendulum.html#L718-L720)), E, V, T = E − V, L = T − V and ε ([L721–723](../../public/simulations/Double%20Pendulum.html#L721-L723)), positions and speeds in metres
([L724–727](../../public/simulations/Double%20Pendulum.html#L724-L727)), bob pixel positions ([L728–729](../../public/simulations/Double%20Pendulum.html#L728-L729)), the twin separation ([L730–738](../../public/simulations/Double%20Pendulum.html#L730-L738)) and the clock and integrator scalars
([L739–741](../../public/simulations/Double%20Pendulum.html#L739-L741)).

**Precomputation and caching.** There are no tables. The path is cached as pixels on the `trail` canvas: one segment per RK4
step ([L612–621](../../public/simulations/Double%20Pendulum.html#L612-L621)), dimmed each frame by drawing a black rectangle in `destination-out` mode with alpha 1 − 0.992^(60Δt)
([L622–629](../../public/simulations/Double%20Pendulum.html#L622-L629), [L779](../../public/simulations/Double%20Pendulum.html#L779)), so its brightness halves every ln 2/(60 × 0.00803) ≈ 1.4 s of real time ([L359](../../public/simulations/Double%20Pendulum.html#L359)). The trail is cleared
by Restart, by any restarting slider, by *Clear trail* and by a resize ([L578–583](../../public/simulations/Double%20Pendulum.html#L578-L583), [L603](../../public/simulations/Double%20Pendulum.html#L603), [L610](../../public/simulations/Double%20Pendulum.html#L610), [L589](../../public/simulations/Double%20Pendulum.html#L589)). `layout()`
recomputes pivot and scale on restart and on resize ([L572–577](../../public/simulations/Double%20Pendulum.html#L572-L577)).

## Function map

All functions live in the one inline script ([L454–928](../../public/simulations/Double%20Pendulum.html#L454-L928)), wrapped in an immediately invoked function ([L455](../../public/simulations/Double%20Pendulum.html#L455)).

| Function | Lines | What it does |
|---|---|---|
| `ratio(v)` | [L529](../../public/simulations/Double%20Pendulum.html#L529) | Slider text for the log-scale ratios: e^v as "1.00", or "1/x.xx" below 1. |
| `deg(v)` | [L530](../../public/simulations/Double%20Pendulum.html#L530) | Slider text in degrees. |
| `rads(v)` | [L531](../../public/simulations/Double%20Pendulum.html#L531) | Slider text in rad/s. |
| speed slider `format` | [L539](../../public/simulations/Double%20Pendulum.html#L539) | Slider text "1.00×". |
| `deriv(s)` | [L541–549](../../public/simulations/Double%20Pendulum.html#L541-L549) | Right-hand side of the equations: returns (ω₁, ω₂, α₁, α₂). |
| `rk4(s, h)` | [L550–560](../../public/simulations/Double%20Pendulum.html#L550-L560) | One classical RK4 step; returns the new state. |
| `energy(s)` | [L561–566](../../public/simulations/Double%20Pendulum.html#L561-L566) | Kinetic plus potential energy of a state. |
| `pos(s)` | [L567–570](../../public/simulations/Double%20Pendulum.html#L567-L570) | Pixel positions [x₁, y₁, x₂, y₂] of the two bobs (screen y down). |
| `layout()` | [L572–577](../../public/simulations/Double%20Pendulum.html#L572-L577) | Pivot at the canvas centre; σ = (min(W, H)/2 − 34)/(l₁ + l₂); stores them. |
| `clearTrail()` | [L578–583](../../public/simulations/Double%20Pendulum.html#L578-L583) | Clears the trail canvas and forgets the last positions. |
| `resize()` | [L584–590](../../public/simulations/Double%20Pendulum.html#L584-L590) | Fits the canvas, resizes the trail canvas to device pixels, `layout()`, `clearTrail()`. |
| `restart()` | [L592–604](../../public/simulations/Double%20Pendulum.html#L592-L604) | Reads all sliders, sets m₂, l₂, the state, the twin, E₀, t = 0, τ = 0; stores the parameters; `layout()`, `clearTrail()`. |
| twin `change` handler | [L605–608](../../public/simulations/Double%20Pendulum.html#L605-L608) | Twin on: copy of the current state with θ₁ + 0.001 rad; off: `null`. |
| Restart / Clear handlers | [L609–610](../../public/simulations/Double%20Pendulum.html#L609-L610) | `restart` and `clearTrail`. |
| `segment(prev, p, colour, width)` | [L612–621](../../public/simulations/Double%20Pendulum.html#L612-L621) | One trail segment of the lower bob. |
| `fade(a)` | [L622–629](../../public/simulations/Double%20Pendulum.html#L622-L629) | Removes the fraction a of every trail pixel's opacity. |
| `drawProtractor()` | [L631–657](../../public/simulations/Double%20Pendulum.html#L631-L657) | Outer circle at l₁ + l₂, dashed circle at l₁, ticks and labels every 30°. |
| `drawPendulum(s, ghost)` | [L659–682](../../public/simulations/Double%20Pendulum.html#L659-L682) | Rods and bobs; bob 1 radius 8 px, bob 2 radius clamp(8 ∛(m₂/m₁), 4, 17) px; ghost = twin in rose. |
| `draw()` | [L684–694](../../public/simulations/Double%20Pendulum.html#L684-L694) | One picture, in painting order. |
| `readouts()` | [L697–708](../../public/simulations/Double%20Pendulum.html#L697-L708) | Caption time, E, ε and the separation, read from the store. |
| `diagnostics(dt)` | [L712–742](../../public/simulations/Double%20Pendulum.html#L712-L742) | Writes the store (above). |
| `f4(v, u)` | [L745](../../public/simulations/Double%20Pendulum.html#L745) | Four-decimal formatting for `Sim.live`. |
| `Sim.live()` | [L746–758](../../public/simulations/Double%20Pendulum.html#L746-L758) | Strings for the walkthrough's "Now" column, read from the store. |
| clock callback | [L760–784](../../public/simulations/Double%20Pendulum.html#L760-L784) | The frame loop above. |
| `sliderCheck(input, label, scale)` | [L727](../../public/simulations/Double%20Pendulum.html#L727) | Check record for a slider value, optionally × π/180. |
| `bobPixel(name, x, y)` | [L790–799](../../public/simulations/Double%20Pendulum.html#L790-L799) | Reads the screen pixel at a bob's stored centre; passes for burgundy, or for the pivot dot or bob 2's rim painted over it; tests alpha first. |
| `alphaCheck(which)` | [L815–821](../../public/simulations/Double%20Pendulum.html#L815-L821) | Recomputes α₁ or α₂ from the stored state. |
| `stateInputs()` | [L822](../../public/simulations/Double%20Pendulum.html#L822) | The stored state and parameters, as check inputs. |
| `kinetic()`, `potential()` | [L823–824](../../public/simulations/Double%20Pendulum.html#L823-L824) | T and V recomputed from the stored state. |
| `nearest(x, y)` | [L825–829](../../public/simulations/Double%20Pendulum.html#L825-L829) | Bob 2, bob 1 or the pivot, whichever is nearest within 28 px. |
| `Sim.data.playing`, `.play` | [L832](../../public/simulations/Double%20Pendulum.html#L832), [L915](../../public/simulations/Double%20Pendulum.html#L915) | Clock state and start, for the round recorder. |
| `Sim.data.rowLabel`, `.colLabel`, `.at` | [L842–844](../../public/simulations/Double%20Pendulum.html#L842-L844) | Row, column and unit labels for the arrays `y`, `dydt`, `y_twin`, `M`. |
| `Sim.data.probe(x, y)` | [L845](../../public/simulations/Double%20Pendulum.html#L845) | What lies at a point: `{ what: … }` with 'bob 2', 'bob 1' or 'pivot', from `nearest()`. |
| `Sim.data.inspect(ref)` | [L846–852](../../public/simulations/Double%20Pendulum.html#L846-L852) | Values for a bob (angle, ω, α, position, speed, momentum, separation) or for the whole system at the pivot. |
| `Sim.data.locate(name, idx)` | [L853–858](../../public/simulations/Double%20Pendulum.html#L853-L858) | Where a state component or M is drawn. |
| `Sim.data.check.*` | [L860–903](../../public/simulations/Double%20Pendulum.html#L860-L903) | One function per variable: formula, stored inputs, recomputed value. |
| `Sim.data.drawn.*` | [L906–911](../../public/simulations/Double%20Pendulum.html#L906-L911) | Pixel read-back at bob 1 and bob 2 for θ and the pixel positions. |
| `Sim.data.round.label`, `.length`, `.point` | [L851–852](../../public/simulations/Double%20Pendulum.html#L851-L852) | What one recorded round is. |

The twin screen scalars `x1_twin_px`, `y1_twin_px`, `x2_twin_px`, `y2_twin_px` are written immediately after `pos(twin)` in `diagnostics()`; all four are undefined when the twin is off. They are shown in the Chaos twin group. Check recomputes the screen mapping from the stored twin state, lengths, pivot and scale; the picture read-back tests alpha before the rose colour and explains overlap by the main bobs.

| Additional function | Line | Role |
|---|---|---|
| `twinPositionCheck(which)` | [800](../../public/simulations/Double%20Pendulum.html#L800) | Independent mapping of stored twin angles to a screen coordinate. |
| `twinPixel(bob)` | [807](../../public/simulations/Double%20Pendulum.html#L807) | Alpha-first pixel read-back at the twin bob centre. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Pause / Play | `play` | starts playing unless the reader prefers reduced motion ([sim.js:177](../../public/scripts/sim.js#L177)) | `Sim.playButton` toggles the clock ([L785](../../public/simulations/Double%20Pendulum.html#L785)). |
| Restart | `restart` | — | `restart()` from the current slider values ([L609](../../public/simulations/Double%20Pendulum.html#L609), [L592–604](../../public/simulations/Double%20Pendulum.html#L592-L604)). |
| Clear trail | `clear` | — | `clearTrail()` ([L610](../../public/simulations/Double%20Pendulum.html#L610)). |
| Chaos twin | `twin` (checkbox) | off ([L62](../../public/simulations/Double%20Pendulum.html#L62)) | On: twin = current state with θ₁ + 0.001 rad, so mid-run it starts from where the pendulum is now; off: no twin ([L605–608](../../public/simulations/Double%20Pendulum.html#L605-L608)). Restart re-creates it from the starting state ([L596](../../public/simulations/Double%20Pendulum.html#L596)). |
| Time scale | `speed` | 0.25–1.5, step 0.05, default 1 ([L65](../../public/simulations/Double%20Pendulum.html#L65)) | Read every frame as simulated seconds per real second ([L762](../../public/simulations/Double%20Pendulum.html#L762)); does not restart. |
| Mass ratio m₂/m₁ | `mass` | −2.3 to 2.3, step 0.05, default 0 ([L73](../../public/simulations/Double%20Pendulum.html#L73)); m₂ = e^slider kg, 0.100–9.97 kg | `restart()` ([L533](../../public/simulations/Double%20Pendulum.html#L533), [L593](../../public/simulations/Double%20Pendulum.html#L593)). |
| Length ratio l₂/l₁ | `length` | −1.6 to 1.6, step 0.05, default 0 ([L77](../../public/simulations/Double%20Pendulum.html#L77)); l₂ = e^slider m, 0.202–4.95 m | `restart()` ([L534](../../public/simulations/Double%20Pendulum.html#L534), [L594](../../public/simulations/Double%20Pendulum.html#L594)); also changes σ. |
| Angle θ₁ | `th1` | −180° to 180°, step 1°, default 120° ([L85](../../public/simulations/Double%20Pendulum.html#L85)) | `restart()`; converted to rad once ([L595](../../public/simulations/Double%20Pendulum.html#L595)). |
| Angle θ₂ | `th2` | −180° to 180°, step 1°, default 150° ([L89](../../public/simulations/Double%20Pendulum.html#L89)) | `restart()`. |
| Angular velocity ω₁ | `w1` | −5 to 5 rad/s, step 0.1, default 0 ([L93](../../public/simulations/Double%20Pendulum.html#L93)) | `restart()`. |
| Angular velocity ω₂ | `w2` | −5 to 5 rad/s, step 0.1, default 0 ([L97](../../public/simulations/Double%20Pendulum.html#L97)) | `restart()`. |

Readouts: `r-e` shows E to three decimals in J ([L700](../../public/simulations/Double%20Pendulum.html#L700)); `r-drift` shows ε with one decimal in exponent form, or "0" below
10⁻¹² ([L701](../../public/simulations/Double%20Pendulum.html#L701)); `r-sep` shows the separation in m, or "twin off" ([L702–707](../../public/simulations/Double%20Pendulum.html#L702-L707)); `cap-t` in the caption shows t to 0.1 s
([L699](../../public/simulations/Double%20Pendulum.html#L699)). The caption also carries "RK4, h = 1/600 s" typeset by KaTeX ([L49](../../public/simulations/Double%20Pendulum.html#L49), [sim.js:463–469](../../public/scripts/sim.js#L463-L469)). Measured with the twin
on from the default start: separation 2.456 m after t = 6.03 s.

## What the page writes into the data store

The store is created by `Sim.dataset({ title: 'Double pendulum', attrs: {...} })` ([L468](../../public/simulations/Double%20Pendulum.html#L468); see
[dataset.md](../scripts/dataset.md)). Its attributes hold the fixed constants: `figure: 2`, `page`, `g`, `m1`, `l1`, `EPS`, `H`,
`integrator` and `units: 'SI: kg, m, s, rad'`. Dimensions: `q = 4` for state vectors ([L476](../../public/simulations/Double%20Pendulum.html#L476)), `a = 2` and `b = 2` for the mass
matrix ([L488–489](../../public/simulations/Double%20Pendulum.html#L488-L489)). The running page holds 56 variables: 4 arrays and 52 scalars. Every value is written once per frame in
`diagnostics()`, except the parameters (written by `restart()`) and the layout (written by `layout()`).

| Array | Dims, type | Written at |
|---|---|---|
| `y` (state), `dydt` (ω₁, ω₂, α₁, α₂), `y_twin` (zeros while the twin is off) | (q), Float64 | [L714](../../public/simulations/Double%20Pendulum.html#L714) |
| `M` (mass matrix, T = ½ ωᵀ M ω) | (a, b), Float64 | [L718](../../public/simulations/Double%20Pendulum.html#L718) |

Scalars, by the place that writes them:
- `restart()`: `m2`, `l2`, `E0`, `th1_0`, `th2_0`, `w1_0`, `w2_0` ([L600–601](../../public/simulations/Double%20Pendulum.html#L600-L601)).
- `layout()`: `scale`, `ox`, `oy` ([L576](../../public/simulations/Double%20Pendulum.html#L576)).
- `diagnostics()`: `th1`, `th2`, `w1`, `w2` ([L716](../../public/simulations/Double%20Pendulum.html#L716)); `delta`, `den`, `alpha1`, `alpha2` ([L717](../../public/simulations/Double%20Pendulum.html#L717)); `detM`, `p1`, `p2`
  ([L720](../../public/simulations/Double%20Pendulum.html#L720)); `E`, `V`, `T`, `L`, `drift` ([L723](../../public/simulations/Double%20Pendulum.html#L723)); `x1`, `y1`, `x2`, `y2` ([L725](../../public/simulations/Double%20Pendulum.html#L725)); `v1`, `v2` ([L727](../../public/simulations/Double%20Pendulum.html#L727)); `x1_px`, `y1_px`,
  `x2_px`, `y2_px` ([L729](../../public/simulations/Double%20Pendulum.html#L729)); `twin_on` ([L730](../../public/simulations/Double%20Pendulum.html#L730)); `sep`, `log10sep` ([L734](../../public/simulations/Double%20Pendulum.html#L734), or `undefined` when the twin is off, [L736](../../public/simulations/Double%20Pendulum.html#L736));
  `t`, `steps`, `n`, `acc`, `speed` ([L739](../../public/simulations/Double%20Pendulum.html#L739)); `dt`, `fps`, `frames`, `playing` ([L741](../../public/simulations/Double%20Pendulum.html#L741)).

- `diagnostics()`: `x1_twin_px`, `y1_twin_px`, `x2_twin_px`, `y2_twin_px` ([L733](../../public/simulations/Double%20Pendulum.html#L733)), immediately after `pos(twin)`; undefined while the twin is off.

Two stored values are derived in a particular way: T is stored as E − V ([L721](../../public/simulations/Double%20Pendulum.html#L721)), and the separation is the distance between the
two bob-2 pixel positions divided by σ ([L732](../../public/simulations/Double%20Pendulum.html#L732)). Both equal the direct formulas up to rounding; the checks recompute them
directly ([L882](../../public/simulations/Double%20Pendulum.html#L882), [L900](../../public/simulations/Double%20Pendulum.html#L900)).

The panel spec `Sim.data` ([L830–917](../../public/simulations/Double%20Pendulum.html#L830-L917); see [datalog.md](../scripts/datalog.md)) lists seven groups ([L833–841](../../public/simulations/Double%20Pendulum.html#L833-L841)), labels the
rows of `y`, `dydt`, `y_twin` and `M` as θ₁, θ₂, ω₁, ω₂ ([L842–844](../../public/simulations/Double%20Pendulum.html#L842-L844)) and saves as `fig2-double-pendulum` ([L769](../../public/simulations/Double%20Pendulum.html#L769)). Its `about`
paragraph says what differs between store and picture ([L854](../../public/simulations/Double%20Pendulum.html#L854)).

**One round** (`Sim.data.round`, [L851–852](../../public/simulations/Double%20Pendulum.html#L851-L852)) is ten seconds of simulated time `t`. Columns charted: `th1`, `th2`, `w1`, `w2`,
`E`, `drift`, `sep`; the recorder also copies every numeric scalar, and follows bob 2 unless another point is pinned. With at most
600 samples the interval is 10/600 s ([datalog.js:1052](../../public/scripts/datalog.js#L1052), [datalog.js:1081](../../public/scripts/datalog.js#L1081)). Every restart sets t back to 0, so moving a
restarting slider during a round puts t below the round's start and the recorder ends it ("the clock was reset",
[datalog.js:1103](../../public/scripts/datalog.js#L1103)).

**`Sim.live()`** ([L746–758](../../public/simulations/Double%20Pendulum.html#L746-L758)) returns formatted strings under the keys `t1`, `t2`, `o1`, `o2`, `d`, `den`, `m2`, `l2`, `a1`,
`a2`, `k1`, `h`, `n`, `acc`, `t`, `kin`, `pot`, `E`, `E0`, `drift`, `scale`, `y1`; all read from the store except `h`, the constant
`H`. The walkthrough polls it every 200 ms unless "Hold the numbers" is on ([sim.js:391–403](../../public/scripts/sim.js#L391-L403)).

**Proof, measured in this session** (1280 px window, default start, paused after about 3 s; stored value against the page's own
`check` functions): α₁, α₂, T, V, E, ε, x₂, y₂, x₂ px, y₂ px, det M and p_θ₁ were identical, difference 0, because store and
check use the same float64 expressions. The screen pixels at the stored centres of bob 1 and bob 2 were rgb(122, 31, 43), the
burgundy fill.

## Page structure

**Head** ([L3–15](../../public/simulations/Double%20Pendulum.html#L3-L15)): title "Double Pendulum Chaos · Numa Koudsie" and description ([L8–9](../../public/simulations/Double%20Pendulum.html#L8-L9)); the security policy and referrer rule
([L5–6](../../public/simulations/Double%20Pendulum.html#L5-L6), see [build-and-deploy.md](../build-and-deploy.md#security)); stylesheets in order `../styles/sim.css`, `../styles/data.css`, `../styles/fold.css` ([L11–12](../../public/simulations/Double%20Pendulum.html#L11-L12)); an inline SVG
favicon ([L14](../../public/simulations/Double%20Pendulum.html#L14)). No inline style. See [styles.md](../styles.md).

**Body**, top to bottom:
- Top bar: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`, 87 × 48) and
  "← All simulations" ([L18](../../public/simulations/Double%20Pendulum.html#L18)), then the hand-written Fig. 1–10 links ([L17–33](../../public/simulations/Double%20Pendulum.html#L17-L33)); a `<noscript>` message ([L36](../../public/simulations/Double%20Pendulum.html#L36)).
- Heading: "Fig. 2 · classical mechanics · chaos", the title, the lede ([L37–41](../../public/simulations/Double%20Pendulum.html#L37-L41)).
- The figure: `#stage` with aspect ratio 4 : 3, and 1 : 1.05 below 900 px ([L45](../../public/simulations/Double%20Pendulum.html#L45), [sim.css:213–215](../../public/styles/sim.css#L213-L215)); the canvas `#pend`
  ([L46](../../public/simulations/Double%20Pendulum.html#L46)); the caption with `cap-t` ([L48–51](../../public/simulations/Double%20Pendulum.html#L48-L51)). The canvas is transparent where nothing is drawn, so the stage's grid
  background shows through ([L685](../../public/simulations/Double%20Pendulum.html#L685), [sim.css:68](../../public/styles/sim.css#L68)). `datalog.js` adds the Read values switch to the caption and the reading
  strip under the stage ([datalog.js:874–898](../../public/scripts/datalog.js#L874-L898)).
- The control panel ([L54–112](../../public/simulations/Double%20Pendulum.html#L54-L112)): Run (buttons, twin switch, time scale), Coupling (two ratios), Initial conditions (four
  sliders), readouts, legend.
- The lecture note `<article class="paper" id="paper">` ([L115–441](../../public/simulations/Double%20Pendulum.html#L115-L441)).
- The walkthrough host `<section class="walk" id="walk" data-walk="pendulum">` ([L443](../../public/simulations/Double%20Pendulum.html#L443)).
- Footer ([L446–449](../../public/simulations/Double%20Pendulum.html#L446-L449)).
- Scripts in load order: `../scripts/fold.js`, `../scripts/sim.js`, `../scripts/dataset.js` ([L451–453](../../public/simulations/Double%20Pendulum.html#L451-L453)), the page's own script
  ([L454–928](../../public/simulations/Double%20Pendulum.html#L454-L928)), then `../scripts/datalog.js` ([L929](../../public/simulations/Double%20Pendulum.html#L929)). `sim.js` loads `../scripts/walk/pendulum.js` from the `data-walk` key
  ([sim.js:481–490](../../public/scripts/sim.js#L481-L490)). See [sim.md](../scripts/sim.md), [fold.md](../scripts/fold.md), [walk.md](../scripts/walk.md),
  [pages.md](../pages.md).

The script ends by calling `restart()`, `resize()`, `diagnostics(0)` and registering the resize observer ([L923–926](../../public/simulations/Double%20Pendulum.html#L923-L926)).

**Walkthrough** ([pendulum.js](../../public/scripts/walk/pendulum.js), 8 steps). A script run in this session confirmed that
every quoted line is identical, after trimming indentation, to the page line listed.

| Step | Title | Page lines quoted |
|---|---|---|
| 1 | The state vector | [L595](../../public/simulations/Double%20Pendulum.html#L595) |
| 2 | Angle difference and the shared denominator | [L542–543](../../public/simulations/Double%20Pendulum.html#L542-L543) |
| 3 | Upper angular acceleration α₁ | [L544–545](../../public/simulations/Double%20Pendulum.html#L544-L545) |
| 4 | Lower angular acceleration α₂ | [L546–548](../../public/simulations/Double%20Pendulum.html#L546-L548) |
| 5 | One Runge–Kutta 4 step | [L551–558](../../public/simulations/Double%20Pendulum.html#L551-L558) |
| 6 | How many steps per frame | [L762–767](../../public/simulations/Double%20Pendulum.html#L762-L767), [L777](../../public/simulations/Double%20Pendulum.html#L777) |
| 7 | Energy as the accuracy check | [L562–565](../../public/simulations/Double%20Pendulum.html#L562-L565), [L722](../../public/simulations/Double%20Pendulum.html#L722) |
| 8 | From angles to pixels | [L575](../../public/simulations/Double%20Pendulum.html#L575), [L568–569](../../public/simulations/Double%20Pendulum.html#L568-L569) |

**Lecture note** "The double pendulum: exact laws, unpredictable motion": abstract ([L119](../../public/simulations/Double%20Pendulum.html#L119)), contents ([L123–136](../../public/simulations/Double%20Pendulum.html#L123-L136)), nine
sections, 13 numbered display equations (1)–(13) plus one unnumbered display ([L210](../../public/simulations/Double%20Pendulum.html#L210)), three inline SVG figures, one summary box,
two exercises and three references. Section 4 carries ★.

| § | id | Title | Lines | Equations | Figures, boxes |
|---|---|---|---|---|---|
| 1 | `p-swing` | A pendulum on a pendulum | [L138–179](../../public/simulations/Double%20Pendulum.html#L138-L179) | — | Figure 1, geometry ([L144–178](../../public/simulations/Double%20Pendulum.html#L144-L178)) |
| 2 | `p-model` | The model | [L181–189](../../public/simulations/Double%20Pendulum.html#L181-L189) | (1) positions | — |
| 3 | `p-energy` | Energy | [L191–215](../../public/simulations/Double%20Pendulum.html#L191-L215) | (2) velocities, (3) T, (4) V | box "Energy is conserved" ([L211–214](../../public/simulations/Double%20Pendulum.html#L211-L214)) |
| 4 | `p-lagrange` | From energy to motion ★ | [L217–263](../../public/simulations/Double%20Pendulum.html#L217-L263) | (5) Euler–Lagrange, unnumbered derivatives, (6), (7), (8) linear system, (9) α₁, α₂ | §4.1–4.4 ([L204](../../public/simulations/Double%20Pendulum.html#L204), [L208](../../public/simulations/Double%20Pendulum.html#L208), [L213](../../public/simulations/Double%20Pendulum.html#L213), [L246](../../public/simulations/Double%20Pendulum.html#L246)); check note ([L221](../../public/simulations/Double%20Pendulum.html#L221)) |
| 5 | `p-modes` | Small swings: two normal modes | [L265–327](../../public/simulations/Double%20Pendulum.html#L265-L327) | (10), (11) normal-mode frequencies | Figure 2, the two modes ([L279–318](../../public/simulations/Double%20Pendulum.html#L279-L318)); Exercise 5.1 |
| 6 | `p-chaos` | Chaos | [L329–400](../../public/simulations/Double%20Pendulum.html#L329-L400) | (12) Lyapunov exponent | Figure 3, twin separation on a log scale ([L332–386](../../public/simulations/Double%20Pendulum.html#L332-L386)); Exercise 6.1 |
| 7 | `p-rk4` | Solving it step by step | [L402–412](../../public/simulations/Double%20Pendulum.html#L402-L412) | (13) RK4 | — |
| 8 | `p-screen` | From metres to pixels | [L414–418](../../public/simulations/Double%20Pendulum.html#L414-L418) | — | — |
| 9 | `p-limits` | What the model leaves out | [L420–438](../../public/simulations/Double%20Pendulum.html#L420-L438) | — | §9.1 Further reading ([L432–437](../../public/simulations/Double%20Pendulum.html#L432-L437)) |

## Where the drawing and the store differ

The page states the main point in `about` ([L854](../../public/simulations/Double%20Pendulum.html#L854)): rods and bobs are drawn at the stored pixel positions, so picture and store
agree to the pixel; the trail is not stored.
- **Trail.** Painted segment by segment at every RK4 step and faded each frame ([L769](../../public/simulations/Double%20Pendulum.html#L769), [L774](../../public/simulations/Double%20Pendulum.html#L774), [L779](../../public/simulations/Double%20Pendulum.html#L779)); it is not kept as an
  array. To keep a trajectory, record a round.
- **Sub-steps.** The store holds the state at the end of each frame only ([L714](../../public/simulations/Double%20Pendulum.html#L714)). At 60 frames per second about ten RK4 states
  per frame reach the trail but not the store.
- **Bob sizes.** Bob 1 has radius 8 px; bob 2 has 8 ∛(m₂/m₁) px clamped to 4–17 px ([L661](../../public/simulations/Double%20Pendulum.html#L661)). The clamp acts below
  m₂ = 0.125 kg and above 9.6 kg, inside the slider's range of 0.100–9.97 kg.
- **Readout rate.** The readouts and the caption time are rewritten every sixth frame, about ten times a second ([L783](../../public/simulations/Double%20Pendulum.html#L783)); the
  store changes every frame. ε is shown with two significant figures ([L701](../../public/simulations/Double%20Pendulum.html#L701)).
- **Twin.** The twin is drawn in rose with thinner rods and no rim ([L662–680](../../public/simulations/Double%20Pendulum.html#L662-L680)); its state (`y_twin`), four screen coordinates and the separation are
  stored. `locate` reads the twin’s stored coordinates and returns `null` while the twin is off.

## How to change it safely

- **Walkthrough excerpts.** `pendulum.js` quotes [L542–548](../../public/simulations/Double%20Pendulum.html#L542-L548), [L551–558](../../public/simulations/Double%20Pendulum.html#L551-L558), [L562–565](../../public/simulations/Double%20Pendulum.html#L562-L565), [L568–569](../../public/simulations/Double%20Pendulum.html#L568-L569), [L575](../../public/simulations/Double%20Pendulum.html#L575), [L595](../../public/simulations/Double%20Pendulum.html#L595), [L722](../../public/simulations/Double%20Pendulum.html#L722),
  [L762–767](../../public/simulations/Double%20Pendulum.html#L762-L767) and [L777](../../public/simulations/Double%20Pendulum.html#L777). Keep them character for character, or change `pendulum.js` in the same edit. Insert store taps after a
  quoted line, never inside a quoted pair (AGENTS.md).
- **`Sim.live()` keys** must match the `syms` keys of `pendulum.js` (listed above).
- **Formulas live in several places.** The accelerations are in `deriv()` ([L544–547](../../public/simulations/Double%20Pendulum.html#L544-L547)), in the store attributes
  ([L486–487](../../public/simulations/Double%20Pendulum.html#L486-L487)), in `alphaCheck()` ([L818–819](../../public/simulations/Double%20Pendulum.html#L818-L819)), in the walkthrough and in the note's eq. (9) ([L220](../../public/simulations/Double%20Pendulum.html#L220)). The energy is in
  `energy()` ([L562–564](../../public/simulations/Double%20Pendulum.html#L562-L564)), `kinetic()`/`potential()` ([L823–824](../../public/simulations/Double%20Pendulum.html#L823-L824)), the attributes ([L494–495](../../public/simulations/Double%20Pendulum.html#L494-L495)) and eqs. (3)–(4). The pixel map
  is in `pos()` and `layout()` ([L568–569](../../public/simulations/Double%20Pendulum.html#L568-L569), [L575](../../public/simulations/Double%20Pendulum.html#L575)), the checks ([L893–897](../../public/simulations/Double%20Pendulum.html#L893-L897)), the attributes ([L506–514](../../public/simulations/Double%20Pendulum.html#L506-L514)) and note §8
  ([L358](../../public/simulations/Double%20Pendulum.html#L358)). The bob-2 radius is in `drawPendulum()` ([L661](../../public/simulations/Double%20Pendulum.html#L661)) and `bobPixel()` ([L792](../../public/simulations/Double%20Pendulum.html#L792)). The expected colours in `bobPixel()`
  (122, 31, 43) and (90, 80, 75) are `Sim.theme.accent` and `Sim.theme.ink3` ([L791–794](../../public/simulations/Double%20Pendulum.html#L791-L794), [sim.js:16](../../public/scripts/sim.js#L16), [sim.js:12](../../public/scripts/sim.js#L12)).
- **Constants quoted in text.** h = 1/600 s appears in the caption ([L49](../../public/simulations/Double%20Pendulum.html#L49)), the note (§7, Figure 3) and the panel group note
  ([L778](../../public/simulations/Double%20Pendulum.html#L778)); 0.001 rad appears on the twin switch ([L62](../../public/simulations/Double%20Pendulum.html#L62)) and in the note. Change them together with `H` and `EPS` ([L458](../../public/simulations/Double%20Pendulum.html#L458)).
- **The catalog** entry's `equation`, `model`, `method` and `controls` ([catalog.js:73–76](../../public/scripts/catalog.js#L73-L76)) describe this page.
- **Re-test** after any change: Check α₁, α₂, E, ε and x₂ px in the Data panel (stored, recomputed, pixel); watch ε stay within
  ±5 × 10⁻⁸ for 20 s from the default start; switch the twin on and see the separation grow; record one round; pin bob 2 with Read
  values; resize between 390 px and 1440 px.

## Notes for maintainers

1. Fixed on 2026-10-15: the note, walkthrough and n metadata explain why the 600-step guard cannot act under the current 46-step upper bound (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
2. Fixed on 2026-10-15: the note describes signed energy drift; Chromium gives −2.416 × 10⁻⁸ near 21 s (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
3. Fixed on 2026-10-15: the state-vector and angle/velocity metadata state that diagnostics stores once per frame (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
4. Fixed on 2026-10-15: the walkthrough cites lecture-note equations (6)–(8) (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
5. Fixed on 2026-10-15: y_twin locates the twin’s four stored screen coordinates; stored and recomputed coordinates are identical and the pixels are rose (commit [9d3175f](https://github.com/Numa1997/SiteTest/commit/9d3175f2cf50d0ad3f8792f1ee173e8ce56bab53)).
6. Fixed on 2026-10-15: the note states the 4–17 px bob-2 radius clamp (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
7. Fixed on 2026-10-15: the note's drift sentence said ε stays below 3 × 10⁻⁸ over the first 20 s; measured, it reaches
   +4.710 × 10⁻⁸ at t = 8.665 s (and −3.185 × 10⁻⁸ at 19.13 s). It now reads "stays within ±5 × 10⁻⁸: its largest value is
   +4.7 × 10⁻⁸, at t ≈ 8.7 s" ([L351](../../public/simulations/Double%20Pendulum.html#L351)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).


## Teaching revision · 15 October 2026

The note distinguishes energy accuracy from long-time trajectory accuracy, identifies bob separation as a finite-time projection rather than a full-state Lyapunov calculation, and requires separate convergence checks for statistics. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16 (second repairs): the Lyapunov paragraphs say that the limit defines the exponent and the rescaling algorithm computes it, that the 1.7 s⁻¹ is a finite-time estimate from two of the four coordinates, and that a small energy drift proves the integrator, not the positions; the limits item says the computed path is a faithful example, not the exact one ([L335](../../public/simulations/Double%20Pendulum.html#L335)). See the [audit of the revision](../research-theory-audit.md).

Teaching pass, 20 October 2026 (notes/fig02/plan.md; the note's lines only, no line moved, numbering unchanged): the energy
sentence of §1 is limited to the first twenty seconds ([L141](../../public/simulations/Double%20Pendulum.html#L141)); §4.4 names the identity sin θ₁ cos δ − sin θ₂ = cos θ₁ sin δ
that gives α₂ its factor sin δ ([L219](../../public/simulations/Double%20Pendulum.html#L219)); the Lyapunov paragraphs replace the unsupported 1.7 s⁻¹ with the measured line
through Figure 3's high-energy curve, λ ≈ 1.4 s⁻¹ up to the 0.1 m crossing at 4.06 s, and the full-state exponent of the
default start, λ ≈ 1.46 s⁻¹ (rescaling every 0.1 s over 20 000 s), with e^1.46 ≈ 4.3 and e^14.6 ≈ 2 × 10⁶ ([L336](../../public/simulations/Double%20Pendulum.html#L336), [L338](../../public/simulations/Double%20Pendulum.html#L338));
§7 says that the slider caps the time scale, that the drift creeps by about −7 × 10⁻⁸ a minute (−7.2 × 10⁻⁷ after ten
simulated minutes in Chromium), and that the step fails for a heavy lower bob: ε reaches −3.6 × 10⁻⁴ in 20 s at m₂/m₁ = 10
([L350](../../public/simulations/Double%20Pendulum.html#L350), [L351](../../public/simulations/Double%20Pendulum.html#L351)); §8 defines σ, the
pivot and W × H, draws the bobs with σ, names the two protractor circles and Δt, and writes the half-life as
ln 2/(60 |ln 0.992|) ([L358](../../public/simulations/Double%20Pendulum.html#L358), [L359](../../public/simulations/Double%20Pendulum.html#L359)); the three references link to pages opened that day ([L433–435](../../public/simulations/Double%20Pendulum.html#L433-L435)).

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig02/`), the lead made only these changes, each on its existing line, so no line link moved: equations (5), (8), (9) and (13) broken over two or three lines so their numbers show at 1440 px ([L206](../../public/simulations/Double%20Pendulum.html#L206)); (8) ([L218](../../public/simulations/Double%20Pendulum.html#L218)); (9) ([L220](../../public/simulations/Double%20Pendulum.html#L220)); (13) ([L406](../../public/simulations/Double%20Pendulum.html#L406)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

## Second check round · 20 October 2026

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig02/`), each change on its existing line: §5: the matrix whose determinant must vanish written out, and why ([L228](../../public/simulations/Double%20Pendulum.html#L228)); §6: why two nearby starts part (linear small swings; balancing near the top) ([L335](../../public/simulations/Double%20Pendulum.html#L335)); §6: the rough and full Lyapunov rates in one sentence; "much of what that energy allows" ([L337](../../public/simulations/Double%20Pendulum.html#L337)); §9: the Lyapunov time defined ([L368](../../public/simulations/Double%20Pendulum.html#L368)); equations (6), (9), (11) reflowed so their numbers show at 1600 px ([L212](../../public/simulations/Double%20Pendulum.html#L212)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.

From the Fig. 2 derivation check (65 verified, 4 wrong, 1 unverifiable; `notes/fig02/check.md`): abstract: 600 steps a second, sixty frames a second ([L119](../../public/simulations/Double%20Pendulum.html#L119)); §7: drift peak +5.0 × 10⁻⁸ step by step, +4.7 × 10⁻⁸ as the readout samples it ([L351](../../public/simulations/Double%20Pendulum.html#L351)); §8: the trail as the canvas really fades it (half in 1.6 s, then a faint haze at a quarter opacity) ([L359](../../public/simulations/Double%20Pendulum.html#L359)); §9: the computed path stays true for 15–20 Lyapunov times, 11–14 s ([L368](../../public/simulations/Double%20Pendulum.html#L368)). The trail's haze is a page defect, reported in the audit, not changed.
