# Fig. 2 · Double Pendulum

| | |
|---|---|
| Page | [public/simulations/Double Pendulum.html](../../public/simulations/Double%20Pendulum.html) (870 lines, 105 641 bytes) |
| Walkthrough | [public/scripts/walk/pendulum.js](../../public/scripts/walk/pendulum.js) (137 lines, 8 steps, key `pendulum`) |
| Thumbnail | [public/images/sims/double-pendulum.webp](../../public/images/sims/double-pendulum.webp) (WebP, 800 × 500 px, 12.5 kB; the pendulum, its fading trail and the protractor) |
| Catalog entry | [public/scripts/catalog.js#L65](../../public/scripts/catalog.js#L65) (`id: 'double-pendulum'`, `fig: 2`, `field: 'mechanics'`, `stage: 2`, lines 64–80) |

Links written `Lnnn` point into the page file; links to other files carry the file name.

The reader sees a pendulum hanging from a pivot at the centre of the figure: an upper rod with a burgundy bob and a lower rod with
a second burgundy bob, inside a faint protractor marked every 30° ([L43–51](../../public/simulations/Double%20Pendulum.html#L43-L51), [L569–595](../../public/simulations/Double%20Pendulum.html#L569-L595)). Released from θ₁ = 120°,
θ₂ = 150° ([L84](../../public/simulations/Double%20Pendulum.html#L84), [L88](../../public/simulations/Double%20Pendulum.html#L88)), it whips round in a way that never repeats; the lower bob leaves a burgundy trail that fades in about
1.4 s. A switch adds a pale "chaos twin" started 0.001 rad away, and a readout shows how far the two lower bobs have drifted apart
([L61](../../public/simulations/Double%20Pendulum.html#L61), [L103](../../public/simulations/Double%20Pendulum.html#L103)). Sliders set the mass and length ratios, the starting angles and angular velocities, and a time scale
([L62–97](../../public/simulations/Double%20Pendulum.html#L62-L97)); every slider except the time scale restarts the motion. The caption shows the simulated time; readouts show the
energy and its numerical drift ([L49](../../public/simulations/Double%20Pendulum.html#L49), [L100–104](../../public/simulations/Double%20Pendulum.html#L100-L104)). Under the figure sit the Data panel and the Read values switch (added by
`datalog.js`), the walkthrough ([L381](../../public/simulations/Double%20Pendulum.html#L381)) and the lecture note ([L114–379](../../public/simulations/Double%20Pendulum.html#L114-L379)).

## The physics in one picture

**Everyday picture.** Let your arm hang and swing it: the upper arm turns about the shoulder, the forearm about the elbow, and
the hand draws a path that neither joint alone would draw ([L140](../../public/simulations/Double%20Pendulum.html#L140)). Started gently, a double pendulum rocks regularly; started
high, it flips over the top and never settles. Nothing is random, yet two starts a thousandth of a radian apart end in unrelated
places within seconds: deterministic chaos ([L141–142](../../public/simulations/Double%20Pendulum.html#L141-L142)).

**Model.** Two point masses on rigid, massless rods in one vertical plane, no friction, no air ([L182](../../public/simulations/Double%20Pendulum.html#L182)). The upper mass and rod
are fixed at m₁ = 1 kg and l₁ = 1 m, and g = 9.81 m/s² ([L396](../../public/simulations/Double%20Pendulum.html#L396), [L184](../../public/simulations/Double%20Pendulum.html#L184)). Angles are measured from the downward vertical,
counter-clockwise positive ([L176](../../public/simulations/Double%20Pendulum.html#L176)). The state is the four numbers (θ₁, θ₂, ω₁, ω₂) ([L184](../../public/simulations/Double%20Pendulum.html#L184)). The note derives the equations
of motion from the Lagrangian L = T − V with the Euler–Lagrange equation (note §4, [L201–222](../../public/simulations/Double%20Pendulum.html#L201-L222)).

**What the code evaluates.** Positions, with the pivot at the origin and y upward ([L662–663](../../public/simulations/Double%20Pendulum.html#L662-L663)):

$$x_1 = l_1\sin\theta_1, \quad y_1 = -l_1\cos\theta_1, \quad x_2 = x_1 + l_2\sin\theta_2, \quad y_2 = y_1 - l_2\cos\theta_2 .$$

Energy, in `energy(s)` ([L499–504](../../public/simulations/Double%20Pendulum.html#L499-L504)):

$$T = \tfrac12 (m_1+m_2)\,l_1^2\omega_1^2 + \tfrac12 m_2 l_2^2\omega_2^2 + m_2 l_1 l_2\,\omega_1\omega_2\cos(\theta_1-\theta_2),$$

$$V = -(m_1+m_2)\,g\,l_1\cos\theta_1 - m_2\,g\,l_2\cos\theta_2 .$$

The angular accelerations, in `deriv(s)` ([L479–487](../../public/simulations/Double%20Pendulum.html#L479-L487)), with $\delta = \theta_1 - \theta_2$ and the shared denominator
$D' = 2m_1 + m_2 - m_2\cos 2\delta = 2(m_1 + m_2\sin^2\delta) > 0$:

$$\alpha_1 = \frac{-g(2m_1+m_2)\sin\theta_1 - m_2 g\sin(\theta_1 - 2\theta_2) - 2\sin\delta\; m_2\left(\omega_2^2 l_2 + \omega_1^2 l_1\cos\delta\right)}{l_1 D'},$$

$$\alpha_2 = \frac{2\sin\delta\left(\omega_1^2 l_1 (m_1+m_2) + g(m_1+m_2)\cos\theta_1 + \omega_2^2 l_2 m_2\cos\delta\right)}{l_2 D'} .$$

These are eq. (9) of the note ([L220](../../public/simulations/Double%20Pendulum.html#L220)), obtained from the linear system (8) by Cramer's rule ([L218–219](../../public/simulations/Double%20Pendulum.html#L218-L219)). With the state
$s = (\theta_1, \theta_2, \omega_1, \omega_2)$ and $F(s) = (\omega_1, \omega_2, \alpha_1, \alpha_2)$, one step of the classical
fourth-order Runge–Kutta method with $h = 1/600$ s is ([L488–498](../../public/simulations/Double%20Pendulum.html#L488-L498), note eq. 13):

$$k_1 = F(s), \quad k_2 = F\left(s + \tfrac h2 k_1\right), \quad k_3 = F\left(s + \tfrac h2 k_2\right), \quad k_4 = F(s + h k_3), \quad s \leftarrow s + \tfrac h6\left(k_1 + 2k_2 + 2k_3 + k_4\right).$$

The energy check divides the change of $E = T + V$ by the depth of the potential well, not by $E_0$, which can be near zero
([L660](../../public/simulations/Double%20Pendulum.html#L660)):

$$\varepsilon = \frac{E - E_0}{(m_1+m_2)\,g\,l_1 + m_2\,g\,l_2} .$$

| Symbol | Code | Unit | Meaning |
|---|---|---|---|
| $\theta_1, \theta_2$ | `state[0]`, `state[1]` | rad | rod angles from the downward vertical |
| $\omega_1, \omega_2$ | `state[2]`, `state[3]` | rad/s | angular velocities |
| $\alpha_1, \alpha_2$ | `a1`, `a2` in `deriv` | rad/s² | angular accelerations |
| $m_1, m_2$ | `m1 = 1`, `m2` | kg | bob masses; m₂ = m₁ e^slider ([L531](../../public/simulations/Double%20Pendulum.html#L531)) |
| $l_1, l_2$ | `l1 = 1`, `l2` | m | rod lengths; l₂ = l₁ e^slider ([L532](../../public/simulations/Double%20Pendulum.html#L532)) |
| $g$ | `g = 9.81` | m/s² | gravitational acceleration ([L396](../../public/simulations/Double%20Pendulum.html#L396)) |
| $\delta$, $D'$ | `d`, `den` | rad, kg | angle between the rods, shared denominator |
| $h$ | `H = 1/600` | s | RK4 step ([L396](../../public/simulations/Double%20Pendulum.html#L396)) |
| $T, V, E, E_0$ | `kin`, `pot`, `energy(s)`, `E0` | J | kinetic, potential, total, total at restart |
| $\varepsilon$ | `drift` | 1 | relative energy error |
| $\sigma$ | `scale` | px/m | pixels per metre on screen ([L513](../../public/simulations/Double%20Pendulum.html#L513)) |
| $d$ | `sep` | m | distance between the two lower bobs (twin on) ([L670](../../public/simulations/Double%20Pendulum.html#L670)) |

## How the code computes it

**State.** `state` is a plain array [θ₁, θ₂, ω₁, ω₂] in rad and rad/s, set from the sliders by `restart()` ([L533](../../public/simulations/Double%20Pendulum.html#L533)); `twin`
is a second such array or `null` ([L534](../../public/simulations/Double%20Pendulum.html#L534)). `E0` is the energy at restart ([L535](../../public/simulations/Double%20Pendulum.html#L535)); `simT` the simulated time and `acc` the
unspent time carried between frames ([L536–537](../../public/simulations/Double%20Pendulum.html#L536-L537)). `m2` and `l2` come from the log-scale sliders ([L531–532](../../public/simulations/Double%20Pendulum.html#L531-L532)). For drawing:
`ox`, `oy` (pivot) and `scale` (σ) ([L511–513](../../public/simulations/Double%20Pendulum.html#L511-L513)); the offscreen canvas `trail` that holds the fading path ([L400](../../public/simulations/Double%20Pendulum.html#L400)); `prevA`,
`prevB`, the last pixel positions of the two pendulums, from which the next trail segment starts ([L402](../../public/simulations/Double%20Pendulum.html#L402)). `frames`, `lastN` and
`fps` count frames, steps and frame rate ([L402–403](../../public/simulations/Double%20Pendulum.html#L402-L403)).

**Method.** RK4 at a fixed step h = 1/600 s ([L396](../../public/simulations/Double%20Pendulum.html#L396)). Its error over a fixed time scales as h⁴ (note §7, [L348](../../public/simulations/Double%20Pendulum.html#L348)). A fixed step
keeps the accuracy the same on every device ([pendulum.js:86](../../public/scripts/walk/pendulum.js#L86)). RK4 does not conserve energy exactly, so the page shows the
drift ε rather than hiding it ([L351](../../public/simulations/Double%20Pendulum.html#L351), [L639](../../public/simulations/Double%20Pendulum.html#L639)). `rk4()` builds separate trial arrays `s2`, `s3`, `s4`, so all four slopes of a
step use their own input state ([L489–496](../../public/simulations/Double%20Pendulum.html#L489-L496)). Measured in this session (1280 px window, default start, headless Chromium):
ε = −2.4 × 10⁻⁸ at t = 21.2 s, n = 10 steps per frame at 60 frames per second, energy E = 18.3057 J. Over the first 20 s
of the default start ε stays within ±5 × 10⁻⁸: read once per frame, its largest value is +4.710 × 10⁻⁸ at t = 8.665 s, its most negative
−3.185 × 10⁻⁸ at t = 19.13 s; step by step the peak is +5.0006 × 10⁻⁸ at t = 8.668 s (derivation check, 20 October 2026). The step is fixed,
but which step a frame reads depends on the frame times, so the per-frame peak varies between runs (4.71 to 4.99 × 10⁻⁸). The note says so ([L351](../../public/simulations/Double%20Pendulum.html#L351)).

**Sub-stepping.** Real frame times are uneven; the physics advances in equal steps. Each frame ([L700–703](../../public/simulations/Double%20Pendulum.html#L700-L703)):

$$\tau \leftarrow \tau + \Delta t \cdot \text{speed}, \qquad n = \min\left(\lfloor \tau / h \rfloor, 600\right), \qquad \tau \leftarrow \min(\tau - n h,\ h).$$

The leftover τ carries into the next frame, so simulated time keeps pace with wall time × speed. Because `Sim.clock` caps Δt at
0.05 s ([sim.js:179](../../public/scripts/sim.js#L179)) and the time scale is at most 1.5 ([L64](../../public/simulations/Double%20Pendulum.html#L64)), n is at most 46; the 600 cap never acts (see Notes).

**Frame loop** (`Sim.clock` callback, [L698–722](../../public/simulations/Double%20Pendulum.html#L698-L722)), in order:
1. If playing (Δt > 0): accumulate τ and choose n ([L700–703](../../public/simulations/Double%20Pendulum.html#L700-L703)). For each of the n steps: advance `state` by one RK4 step, compute
   its pixel positions, paint one trail segment of the lower bob, remember the position ([L705–708](../../public/simulations/Double%20Pendulum.html#L705-L708)); if the twin is on, do the
   same for it in rose ([L709–714](../../public/simulations/Double%20Pendulum.html#L709-L714)); add h to the simulated time ([L715](../../public/simulations/Double%20Pendulum.html#L715)). After the steps, dim the whole trail layer ([L717](../../public/simulations/Double%20Pendulum.html#L717)).
2. `diagnostics(dt)`: write every derived number of the final state into the store ([L719](../../public/simulations/Double%20Pendulum.html#L719), [L650–680](../../public/simulations/Double%20Pendulum.html#L650-L680)).
3. `draw()`: clear, protractor, trail image, twin, pendulum, pivot dot ([L720](../../public/simulations/Double%20Pendulum.html#L720), [L622–632](../../public/simulations/Double%20Pendulum.html#L622-L632)).
4. Every sixth frame, `readouts()` copies E, ε, the separation and the time from the store into the DOM ([L721](../../public/simulations/Double%20Pendulum.html#L721), [L635–646](../../public/simulations/Double%20Pendulum.html#L635-L646)).

While paused `Sim.clock` passes Δt = 0 ([sim.js:181](../../public/scripts/sim.js#L181)): no steps and no fading, but `diagnostics()` and `draw()` still run every
frame.

**`diagnostics(dt)`** ([L650–680](../../public/simulations/Double%20Pendulum.html#L650-L680)) evaluates `deriv` once more at the final state for the stored slopes and accelerations
([L651](../../public/simulations/Double%20Pendulum.html#L651)), copies the state ([L652](../../public/simulations/Double%20Pendulum.html#L652)), then computes and stores δ, D′, α₁, α₂ ([L655](../../public/simulations/Double%20Pendulum.html#L655)), the mass matrix M and its determinant,
the generalised momenta ([L656–658](../../public/simulations/Double%20Pendulum.html#L656-L658)), E, V, T = E − V, L = T − V and ε ([L659–661](../../public/simulations/Double%20Pendulum.html#L659-L661)), positions and speeds in metres
([L662–665](../../public/simulations/Double%20Pendulum.html#L662-L665)), bob pixel positions ([L666–667](../../public/simulations/Double%20Pendulum.html#L666-L667)), the twin separation ([L668–676](../../public/simulations/Double%20Pendulum.html#L668-L676)) and the clock and integrator scalars
([L677–679](../../public/simulations/Double%20Pendulum.html#L677-L679)).

**Precomputation and caching.** There are no tables. The path is cached as pixels on the `trail` canvas: one segment per RK4
step ([L550–559](../../public/simulations/Double%20Pendulum.html#L550-L559)), dimmed each frame by drawing a black rectangle in `destination-out` mode with alpha 1 − 0.992^(60Δt)
([L560–567](../../public/simulations/Double%20Pendulum.html#L560-L567), [L717](../../public/simulations/Double%20Pendulum.html#L717)), so its brightness halves every ln 2/(60 × 0.00803) ≈ 1.4 s of real time ([L359](../../public/simulations/Double%20Pendulum.html#L359)). The trail is cleared
by Restart, by any restarting slider, by *Clear trail* and by a resize ([L516–521](../../public/simulations/Double%20Pendulum.html#L516-L521), [L541](../../public/simulations/Double%20Pendulum.html#L541), [L548](../../public/simulations/Double%20Pendulum.html#L548), [L527](../../public/simulations/Double%20Pendulum.html#L527)). `layout()`
recomputes pivot and scale on restart and on resize ([L510–515](../../public/simulations/Double%20Pendulum.html#L510-L515)).

## Function map

All functions live in the one inline script ([L392–866](../../public/simulations/Double%20Pendulum.html#L392-L866)), wrapped in an immediately invoked function ([L393](../../public/simulations/Double%20Pendulum.html#L393)).

| Function | Lines | What it does |
|---|---|---|
| `ratio(v)` | [L467](../../public/simulations/Double%20Pendulum.html#L467) | Slider text for the log-scale ratios: e^v as "1.00", or "1/x.xx" below 1. |
| `deg(v)` | [L468](../../public/simulations/Double%20Pendulum.html#L468) | Slider text in degrees. |
| `rads(v)` | [L469](../../public/simulations/Double%20Pendulum.html#L469) | Slider text in rad/s. |
| speed slider `format` | [L477](../../public/simulations/Double%20Pendulum.html#L477) | Slider text "1.00×". |
| `deriv(s)` | [L479–487](../../public/simulations/Double%20Pendulum.html#L479-L487) | Right-hand side of the equations: returns (ω₁, ω₂, α₁, α₂). |
| `rk4(s, h)` | [L488–498](../../public/simulations/Double%20Pendulum.html#L488-L498) | One classical RK4 step; returns the new state. |
| `energy(s)` | [L499–504](../../public/simulations/Double%20Pendulum.html#L499-L504) | Kinetic plus potential energy of a state. |
| `pos(s)` | [L505–508](../../public/simulations/Double%20Pendulum.html#L505-L508) | Pixel positions [x₁, y₁, x₂, y₂] of the two bobs (screen y down). |
| `layout()` | [L510–515](../../public/simulations/Double%20Pendulum.html#L510-L515) | Pivot at the canvas centre; σ = (min(W, H)/2 − 34)/(l₁ + l₂); stores them. |
| `clearTrail()` | [L516–521](../../public/simulations/Double%20Pendulum.html#L516-L521) | Clears the trail canvas and forgets the last positions. |
| `resize()` | [L522–528](../../public/simulations/Double%20Pendulum.html#L522-L528) | Fits the canvas, resizes the trail canvas to device pixels, `layout()`, `clearTrail()`. |
| `restart()` | [L530–542](../../public/simulations/Double%20Pendulum.html#L530-L542) | Reads all sliders, sets m₂, l₂, the state, the twin, E₀, t = 0, τ = 0; stores the parameters; `layout()`, `clearTrail()`. |
| twin `change` handler | [L543–546](../../public/simulations/Double%20Pendulum.html#L543-L546) | Twin on: copy of the current state with θ₁ + 0.001 rad; off: `null`. |
| Restart / Clear handlers | [L547–548](../../public/simulations/Double%20Pendulum.html#L547-L548) | `restart` and `clearTrail`. |
| `segment(prev, p, colour, width)` | [L550–559](../../public/simulations/Double%20Pendulum.html#L550-L559) | One trail segment of the lower bob. |
| `fade(a)` | [L560–567](../../public/simulations/Double%20Pendulum.html#L560-L567) | Removes the fraction a of every trail pixel's opacity. |
| `drawProtractor()` | [L569–595](../../public/simulations/Double%20Pendulum.html#L569-L595) | Outer circle at l₁ + l₂, dashed circle at l₁, ticks and labels every 30°. |
| `drawPendulum(s, ghost)` | [L597–620](../../public/simulations/Double%20Pendulum.html#L597-L620) | Rods and bobs; bob 1 radius 8 px, bob 2 radius clamp(8 ∛(m₂/m₁), 4, 17) px; ghost = twin in rose. |
| `draw()` | [L622–632](../../public/simulations/Double%20Pendulum.html#L622-L632) | One picture, in painting order. |
| `readouts()` | [L635–646](../../public/simulations/Double%20Pendulum.html#L635-L646) | Caption time, E, ε and the separation, read from the store. |
| `diagnostics(dt)` | [L650–680](../../public/simulations/Double%20Pendulum.html#L650-L680) | Writes the store (above). |
| `f4(v, u)` | [L683](../../public/simulations/Double%20Pendulum.html#L683) | Four-decimal formatting for `Sim.live`. |
| `Sim.live()` | [L684–696](../../public/simulations/Double%20Pendulum.html#L684-L696) | Strings for the walkthrough's "Now" column, read from the store. |
| clock callback | [L698–722](../../public/simulations/Double%20Pendulum.html#L698-L722) | The frame loop above. |
| `sliderCheck(input, label, scale)` | [L727](../../public/simulations/Double%20Pendulum.html#L727) | Check record for a slider value, optionally × π/180. |
| `bobPixel(name, x, y)` | [L728–737](../../public/simulations/Double%20Pendulum.html#L728-L737) | Reads the screen pixel at a bob's stored centre; passes for burgundy, or for the pivot dot or bob 2's rim painted over it; tests alpha first. |
| `alphaCheck(which)` | [L753–759](../../public/simulations/Double%20Pendulum.html#L753-L759) | Recomputes α₁ or α₂ from the stored state. |
| `stateInputs()` | [L760](../../public/simulations/Double%20Pendulum.html#L760) | The stored state and parameters, as check inputs. |
| `kinetic()`, `potential()` | [L761–762](../../public/simulations/Double%20Pendulum.html#L761-L762) | T and V recomputed from the stored state. |
| `nearest(x, y)` | [L763–767](../../public/simulations/Double%20Pendulum.html#L763-L767) | Bob 2, bob 1 or the pivot, whichever is nearest within 28 px. |
| `Sim.data.playing`, `.play` | [L770](../../public/simulations/Double%20Pendulum.html#L770), [L853](../../public/simulations/Double%20Pendulum.html#L853) | Clock state and start, for the round recorder. |
| `Sim.data.rowLabel`, `.colLabel`, `.at` | [L780–782](../../public/simulations/Double%20Pendulum.html#L780-L782) | Row, column and unit labels for the arrays `y`, `dydt`, `y_twin`, `M`. |
| `Sim.data.probe(x, y)` | [L783](../../public/simulations/Double%20Pendulum.html#L783) | What lies at a point: `{ what: … }` with 'bob 2', 'bob 1' or 'pivot', from `nearest()`. |
| `Sim.data.inspect(ref)` | [L784–790](../../public/simulations/Double%20Pendulum.html#L784-L790) | Values for a bob (angle, ω, α, position, speed, momentum, separation) or for the whole system at the pivot. |
| `Sim.data.locate(name, idx)` | [L791–796](../../public/simulations/Double%20Pendulum.html#L791-L796) | Where a state component or M is drawn. |
| `Sim.data.check.*` | [L798–841](../../public/simulations/Double%20Pendulum.html#L798-L841) | One function per variable: formula, stored inputs, recomputed value. |
| `Sim.data.drawn.*` | [L844–849](../../public/simulations/Double%20Pendulum.html#L844-L849) | Pixel read-back at bob 1 and bob 2 for θ and the pixel positions. |
| `Sim.data.round.label`, `.length`, `.point` | [L851–852](../../public/simulations/Double%20Pendulum.html#L851-L852) | What one recorded round is. |

The twin screen scalars `x1_twin_px`, `y1_twin_px`, `x2_twin_px`, `y2_twin_px` are written immediately after `pos(twin)` in `diagnostics()`; all four are undefined when the twin is off. They are shown in the Chaos twin group. Check recomputes the screen mapping from the stored twin state, lengths, pivot and scale; the picture read-back tests alpha before the rose colour and explains overlap by the main bobs.

| Additional function | Line | Role |
|---|---|---|
| `twinPositionCheck(which)` | [738](../../public/simulations/Double%20Pendulum.html#L738) | Independent mapping of stored twin angles to a screen coordinate. |
| `twinPixel(bob)` | [745](../../public/simulations/Double%20Pendulum.html#L745) | Alpha-first pixel read-back at the twin bob centre. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Pause / Play | `play` | starts playing unless the reader prefers reduced motion ([sim.js:177](../../public/scripts/sim.js#L177)) | `Sim.playButton` toggles the clock ([L723](../../public/simulations/Double%20Pendulum.html#L723)). |
| Restart | `restart` | — | `restart()` from the current slider values ([L547](../../public/simulations/Double%20Pendulum.html#L547), [L530–542](../../public/simulations/Double%20Pendulum.html#L530-L542)). |
| Clear trail | `clear` | — | `clearTrail()` ([L548](../../public/simulations/Double%20Pendulum.html#L548)). |
| Chaos twin | `twin` (checkbox) | off ([L61](../../public/simulations/Double%20Pendulum.html#L61)) | On: twin = current state with θ₁ + 0.001 rad, so mid-run it starts from where the pendulum is now; off: no twin ([L543–546](../../public/simulations/Double%20Pendulum.html#L543-L546)). Restart re-creates it from the starting state ([L534](../../public/simulations/Double%20Pendulum.html#L534)). |
| Time scale | `speed` | 0.25–1.5, step 0.05, default 1 ([L64](../../public/simulations/Double%20Pendulum.html#L64)) | Read every frame as simulated seconds per real second ([L700](../../public/simulations/Double%20Pendulum.html#L700)); does not restart. |
| Mass ratio m₂/m₁ | `mass` | −2.3 to 2.3, step 0.05, default 0 ([L72](../../public/simulations/Double%20Pendulum.html#L72)); m₂ = e^slider kg, 0.100–9.97 kg | `restart()` ([L471](../../public/simulations/Double%20Pendulum.html#L471), [L531](../../public/simulations/Double%20Pendulum.html#L531)). |
| Length ratio l₂/l₁ | `length` | −1.6 to 1.6, step 0.05, default 0 ([L76](../../public/simulations/Double%20Pendulum.html#L76)); l₂ = e^slider m, 0.202–4.95 m | `restart()` ([L472](../../public/simulations/Double%20Pendulum.html#L472), [L532](../../public/simulations/Double%20Pendulum.html#L532)); also changes σ. |
| Angle θ₁ | `th1` | −180° to 180°, step 1°, default 120° ([L84](../../public/simulations/Double%20Pendulum.html#L84)) | `restart()`; converted to rad once ([L533](../../public/simulations/Double%20Pendulum.html#L533)). |
| Angle θ₂ | `th2` | −180° to 180°, step 1°, default 150° ([L88](../../public/simulations/Double%20Pendulum.html#L88)) | `restart()`. |
| Angular velocity ω₁ | `w1` | −5 to 5 rad/s, step 0.1, default 0 ([L92](../../public/simulations/Double%20Pendulum.html#L92)) | `restart()`. |
| Angular velocity ω₂ | `w2` | −5 to 5 rad/s, step 0.1, default 0 ([L96](../../public/simulations/Double%20Pendulum.html#L96)) | `restart()`. |

Readouts: `r-e` shows E to three decimals in J ([L638](../../public/simulations/Double%20Pendulum.html#L638)); `r-drift` shows ε with one decimal in exponent form, or "0" below
10⁻¹² ([L639](../../public/simulations/Double%20Pendulum.html#L639)); `r-sep` shows the separation in m, or "twin off" ([L640–645](../../public/simulations/Double%20Pendulum.html#L640-L645)); `cap-t` in the caption shows t to 0.1 s
([L637](../../public/simulations/Double%20Pendulum.html#L637)). The caption also carries "RK4, h = 1/600 s" typeset by KaTeX ([L48](../../public/simulations/Double%20Pendulum.html#L48), [sim.js:384–390](../../public/scripts/sim.js#L384-L390)). Measured with the twin
on from the default start: separation 2.456 m after t = 6.03 s.

## What the page writes into the data store

The store is created by `Sim.dataset({ title: 'Double pendulum', attrs: {...} })` ([L406](../../public/simulations/Double%20Pendulum.html#L406); see
[dataset.md](../scripts/dataset.md)). Its attributes hold the fixed constants: `figure: 2`, `page`, `g`, `m1`, `l1`, `EPS`, `H`,
`integrator` and `units: 'SI: kg, m, s, rad'`. Dimensions: `q = 4` for state vectors ([L414](../../public/simulations/Double%20Pendulum.html#L414)), `a = 2` and `b = 2` for the mass
matrix ([L426–427](../../public/simulations/Double%20Pendulum.html#L426-L427)). The running page holds 56 variables: 4 arrays and 52 scalars. Every value is written once per frame in
`diagnostics()`, except the parameters (written by `restart()`) and the layout (written by `layout()`).

| Array | Dims, type | Written at |
|---|---|---|
| `y` (state), `dydt` (ω₁, ω₂, α₁, α₂), `y_twin` (zeros while the twin is off) | (q), Float64 | [L652](../../public/simulations/Double%20Pendulum.html#L652) |
| `M` (mass matrix, T = ½ ωᵀ M ω) | (a, b), Float64 | [L656](../../public/simulations/Double%20Pendulum.html#L656) |

Scalars, by the place that writes them:
- `restart()`: `m2`, `l2`, `E0`, `th1_0`, `th2_0`, `w1_0`, `w2_0` ([L538–539](../../public/simulations/Double%20Pendulum.html#L538-L539)).
- `layout()`: `scale`, `ox`, `oy` ([L514](../../public/simulations/Double%20Pendulum.html#L514)).
- `diagnostics()`: `th1`, `th2`, `w1`, `w2` ([L654](../../public/simulations/Double%20Pendulum.html#L654)); `delta`, `den`, `alpha1`, `alpha2` ([L655](../../public/simulations/Double%20Pendulum.html#L655)); `detM`, `p1`, `p2`
  ([L658](../../public/simulations/Double%20Pendulum.html#L658)); `E`, `V`, `T`, `L`, `drift` ([L661](../../public/simulations/Double%20Pendulum.html#L661)); `x1`, `y1`, `x2`, `y2` ([L663](../../public/simulations/Double%20Pendulum.html#L663)); `v1`, `v2` ([L665](../../public/simulations/Double%20Pendulum.html#L665)); `x1_px`, `y1_px`,
  `x2_px`, `y2_px` ([L667](../../public/simulations/Double%20Pendulum.html#L667)); `twin_on` ([L668](../../public/simulations/Double%20Pendulum.html#L668)); `sep`, `log10sep` ([L672](../../public/simulations/Double%20Pendulum.html#L672), or `undefined` when the twin is off, [L674](../../public/simulations/Double%20Pendulum.html#L674));
  `t`, `steps`, `n`, `acc`, `speed` ([L677](../../public/simulations/Double%20Pendulum.html#L677)); `dt`, `fps`, `frames`, `playing` ([L679](../../public/simulations/Double%20Pendulum.html#L679)).

- `diagnostics()`: `x1_twin_px`, `y1_twin_px`, `x2_twin_px`, `y2_twin_px` ([L671](../../public/simulations/Double%20Pendulum.html#L671)), immediately after `pos(twin)`; undefined while the twin is off.

Two stored values are derived in a particular way: T is stored as E − V ([L659](../../public/simulations/Double%20Pendulum.html#L659)), and the separation is the distance between the
two bob-2 pixel positions divided by σ ([L670](../../public/simulations/Double%20Pendulum.html#L670)). Both equal the direct formulas up to rounding; the checks recompute them
directly ([L820](../../public/simulations/Double%20Pendulum.html#L820), [L838](../../public/simulations/Double%20Pendulum.html#L838)).

The panel spec `Sim.data` ([L768–855](../../public/simulations/Double%20Pendulum.html#L768-L855); see [datalog.md](../scripts/datalog.md)) lists seven groups ([L771–779](../../public/simulations/Double%20Pendulum.html#L771-L779)), labels the
rows of `y`, `dydt`, `y_twin` and `M` as θ₁, θ₂, ω₁, ω₂ ([L780–782](../../public/simulations/Double%20Pendulum.html#L780-L782)) and saves as `fig2-double-pendulum` ([L769](../../public/simulations/Double%20Pendulum.html#L769)). Its `about`
paragraph says what differs between store and picture ([L854](../../public/simulations/Double%20Pendulum.html#L854)).

**One round** (`Sim.data.round`, [L851–852](../../public/simulations/Double%20Pendulum.html#L851-L852)) is ten seconds of simulated time `t`. Columns charted: `th1`, `th2`, `w1`, `w2`,
`E`, `drift`, `sep`; the recorder also copies every numeric scalar, and follows bob 2 unless another point is pinned. With at most
600 samples the interval is 10/600 s ([datalog.js:744](../../public/scripts/datalog.js#L744), [datalog.js:773](../../public/scripts/datalog.js#L773)). Every restart sets t back to 0, so moving a
restarting slider during a round puts t below the round's start and the recorder ends it ("the clock was reset",
[datalog.js:795](../../public/scripts/datalog.js#L795)).

**`Sim.live()`** ([L684–696](../../public/simulations/Double%20Pendulum.html#L684-L696)) returns formatted strings under the keys `t1`, `t2`, `o1`, `o2`, `d`, `den`, `m2`, `l2`, `a1`,
`a2`, `k1`, `h`, `n`, `acc`, `t`, `kin`, `pot`, `E`, `E0`, `drift`, `scale`, `y1`; all read from the store except `h`, the constant
`H`. The walkthrough polls it every 200 ms unless "Hold the numbers" is on ([sim.js:314–326](../../public/scripts/sim.js#L314-L326)).

**Proof, measured in this session** (1280 px window, default start, paused after about 3 s; stored value against the page's own
`check` functions): α₁, α₂, T, V, E, ε, x₂, y₂, x₂ px, y₂ px, det M and p_θ₁ were identical, difference 0, because store and
check use the same float64 expressions. The screen pixels at the stored centres of bob 1 and bob 2 were rgb(122, 31, 43), the
burgundy fill.

## Page structure

**Head** ([L3–15](../../public/simulations/Double%20Pendulum.html#L3-L15)): title "Double Pendulum Chaos · Numa Koudsie" and description ([L8–9](../../public/simulations/Double%20Pendulum.html#L8-L9)); the security policy and referrer rule
([L5–6](../../public/simulations/Double%20Pendulum.html#L5-L6), see [build-and-deploy.md](../build-and-deploy.md#security)); stylesheets in order `../styles/sim.css`, `../styles/data.css`, `../styles/fold.css` ([L11–13](../../public/simulations/Double%20Pendulum.html#L11-L13)); an inline SVG
favicon ([L14](../../public/simulations/Double%20Pendulum.html#L14)). No inline style. See [styles.md](../styles.md).

**Body**, top to bottom:
- Top bar: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`, 87 × 48) and
  "← All simulations" ([L18](../../public/simulations/Double%20Pendulum.html#L18)), then the hand-written Fig. 1–10 links ([L17–32](../../public/simulations/Double%20Pendulum.html#L17-L32)); a `<noscript>` message ([L35](../../public/simulations/Double%20Pendulum.html#L35)).
- Heading: "Fig. 2 · classical mechanics · chaos", the title, the lede ([L36–40](../../public/simulations/Double%20Pendulum.html#L36-L40)).
- The figure: `#stage` with aspect ratio 4 : 3, and 1 : 1.05 below 900 px ([L44](../../public/simulations/Double%20Pendulum.html#L44), [sim.css:213–215](../../public/styles/sim.css#L213-L215)); the canvas `#pend`
  ([L45](../../public/simulations/Double%20Pendulum.html#L45)); the caption with `cap-t` ([L47–50](../../public/simulations/Double%20Pendulum.html#L47-L50)). The canvas is transparent where nothing is drawn, so the stage's grid
  background shows through ([L623](../../public/simulations/Double%20Pendulum.html#L623), [sim.css:68](../../public/styles/sim.css#L68)). `datalog.js` adds the Read values switch to the caption and the reading
  strip under the stage ([datalog.js:567–591](../../public/scripts/datalog.js#L567-L591)).
- The control panel ([L53–111](../../public/simulations/Double%20Pendulum.html#L53-L111)): Run (buttons, twin switch, time scale), Coupling (two ratios), Initial conditions (four
  sliders), readouts, legend.
- The lecture note `<article class="paper" id="paper">` ([L114–379](../../public/simulations/Double%20Pendulum.html#L114-L379)).
- The walkthrough host `<section class="walk" id="walk" data-walk="pendulum">` ([L381](../../public/simulations/Double%20Pendulum.html#L381)).
- Footer ([L384–387](../../public/simulations/Double%20Pendulum.html#L384-L387)).
- Scripts in load order: `../scripts/fold.js`, `../scripts/sim.js`, `../scripts/dataset.js` ([L389–391](../../public/simulations/Double%20Pendulum.html#L389-L391)), the page's own script
  ([L392–866](../../public/simulations/Double%20Pendulum.html#L392-L866)), then `../scripts/datalog.js` ([L867](../../public/simulations/Double%20Pendulum.html#L867)). `sim.js` loads `../scripts/walk/pendulum.js` from the `data-walk` key
  ([sim.js:402–411](../../public/scripts/sim.js#L402-L411)). See [sim.md](../scripts/sim.md), [fold.md](../scripts/fold.md), [walk.md](../scripts/walk.md),
  [pages.md](../pages.md).

The script ends by calling `restart()`, `resize()`, `diagnostics(0)` and registering the resize observer ([L861–864](../../public/simulations/Double%20Pendulum.html#L861-L864)).

**Walkthrough** ([pendulum.js](../../public/scripts/walk/pendulum.js), 8 steps). A script run in this session confirmed that
every quoted line is identical, after trimming indentation, to the page line listed.

| Step | Title | Page lines quoted |
|---|---|---|
| 1 | The state vector | [L533](../../public/simulations/Double%20Pendulum.html#L533) |
| 2 | Angle difference and the shared denominator | [L480–481](../../public/simulations/Double%20Pendulum.html#L480-L481) |
| 3 | Upper angular acceleration α₁ | [L482–483](../../public/simulations/Double%20Pendulum.html#L482-L483) |
| 4 | Lower angular acceleration α₂ | [L484–486](../../public/simulations/Double%20Pendulum.html#L484-L486) |
| 5 | One Runge–Kutta 4 step | [L489–496](../../public/simulations/Double%20Pendulum.html#L489-L496) |
| 6 | How many steps per frame | [L700–705](../../public/simulations/Double%20Pendulum.html#L700-L705), [L715](../../public/simulations/Double%20Pendulum.html#L715) |
| 7 | Energy as the accuracy check | [L500–503](../../public/simulations/Double%20Pendulum.html#L500-L503), [L660](../../public/simulations/Double%20Pendulum.html#L660) |
| 8 | From angles to pixels | [L513](../../public/simulations/Double%20Pendulum.html#L513), [L506–507](../../public/simulations/Double%20Pendulum.html#L506-L507) |

**Lecture note** "The double pendulum: exact laws, unpredictable motion": abstract ([L119](../../public/simulations/Double%20Pendulum.html#L119)), contents ([L122–135](../../public/simulations/Double%20Pendulum.html#L122-L135)), nine
sections, 13 numbered display equations (1)–(13) plus one unnumbered display ([L210](../../public/simulations/Double%20Pendulum.html#L210)), three inline SVG figures, one summary box,
two exercises and three references. Section 4 carries ★.

| § | id | Title | Lines | Equations | Figures, boxes |
|---|---|---|---|---|---|
| 1 | `p-swing` | A pendulum on a pendulum | [L137–178](../../public/simulations/Double%20Pendulum.html#L137-L178) | — | Figure 1, geometry ([L143–177](../../public/simulations/Double%20Pendulum.html#L143-L177)) |
| 2 | `p-model` | The model | [L180–185](../../public/simulations/Double%20Pendulum.html#L180-L185) | (1) positions | — |
| 3 | `p-energy` | Energy | [L187–199](../../public/simulations/Double%20Pendulum.html#L187-L199) | (2) velocities, (3) T, (4) V | box "Energy is conserved" ([L195–198](../../public/simulations/Double%20Pendulum.html#L195-L198)) |
| 4 | `p-lagrange` | From energy to motion ★ | [L201–222](../../public/simulations/Double%20Pendulum.html#L201-L222) | (5) Euler–Lagrange, unnumbered derivatives, (6), (7), (8) linear system, (9) α₁, α₂ | §4.1–4.4 ([L204](../../public/simulations/Double%20Pendulum.html#L204), [L208](../../public/simulations/Double%20Pendulum.html#L208), [L213](../../public/simulations/Double%20Pendulum.html#L213), [L216](../../public/simulations/Double%20Pendulum.html#L216)); check note ([L221](../../public/simulations/Double%20Pendulum.html#L221)) |
| 5 | `p-modes` | Small swings: two normal modes | [L224–275](../../public/simulations/Double%20Pendulum.html#L224-L275) | (10), (11) normal-mode frequencies | Figure 2, the two modes ([L231–270](../../public/simulations/Double%20Pendulum.html#L231-L270)); Exercise 5.1 |
| 6 | `p-chaos` | Chaos | [L277–342](../../public/simulations/Double%20Pendulum.html#L277-L342) | (12) Lyapunov exponent | Figure 3, twin separation on a log scale ([L280–334](../../public/simulations/Double%20Pendulum.html#L280-L334)); Exercise 6.1 |
| 7 | `p-rk4` | Solving it step by step | [L344–354](../../public/simulations/Double%20Pendulum.html#L344-L354) | (13) RK4 | — |
| 8 | `p-screen` | From metres to pixels | [L356–360](../../public/simulations/Double%20Pendulum.html#L356-L360) | — | — |
| 9 | `p-limits` | What the model leaves out | [L362–376](../../public/simulations/Double%20Pendulum.html#L362-L376) | — | §9.1 Further reading ([L370–375](../../public/simulations/Double%20Pendulum.html#L370-L375)) |

## Where the drawing and the store differ

The page states the main point in `about` ([L854](../../public/simulations/Double%20Pendulum.html#L854)): rods and bobs are drawn at the stored pixel positions, so picture and store
agree to the pixel; the trail is not stored.
- **Trail.** Painted segment by segment at every RK4 step and faded each frame ([L707](../../public/simulations/Double%20Pendulum.html#L707), [L712](../../public/simulations/Double%20Pendulum.html#L712), [L717](../../public/simulations/Double%20Pendulum.html#L717)); it is not kept as an
  array. To keep a trajectory, record a round.
- **Sub-steps.** The store holds the state at the end of each frame only ([L652](../../public/simulations/Double%20Pendulum.html#L652)). At 60 frames per second about ten RK4 states
  per frame reach the trail but not the store.
- **Bob sizes.** Bob 1 has radius 8 px; bob 2 has 8 ∛(m₂/m₁) px clamped to 4–17 px ([L599](../../public/simulations/Double%20Pendulum.html#L599)). The clamp acts below
  m₂ = 0.125 kg and above 9.6 kg, inside the slider's range of 0.100–9.97 kg.
- **Readout rate.** The readouts and the caption time are rewritten every sixth frame, about ten times a second ([L721](../../public/simulations/Double%20Pendulum.html#L721)); the
  store changes every frame. ε is shown with two significant figures ([L639](../../public/simulations/Double%20Pendulum.html#L639)).
- **Twin.** The twin is drawn in rose with thinner rods and no rim ([L600–618](../../public/simulations/Double%20Pendulum.html#L600-L618)); its state (`y_twin`), four screen coordinates and the separation are
  stored. `locate` reads the twin’s stored coordinates and returns `null` while the twin is off.

## How to change it safely

- **Walkthrough excerpts.** `pendulum.js` quotes [L480–486](../../public/simulations/Double%20Pendulum.html#L480-L486), [L489–496](../../public/simulations/Double%20Pendulum.html#L489-L496), [L500–503](../../public/simulations/Double%20Pendulum.html#L500-L503), [L506–507](../../public/simulations/Double%20Pendulum.html#L506-L507), [L513](../../public/simulations/Double%20Pendulum.html#L513), [L533](../../public/simulations/Double%20Pendulum.html#L533), [L660](../../public/simulations/Double%20Pendulum.html#L660),
  [L700–705](../../public/simulations/Double%20Pendulum.html#L700-L705) and [L715](../../public/simulations/Double%20Pendulum.html#L715). Keep them character for character, or change `pendulum.js` in the same edit. Insert store taps after a
  quoted line, never inside a quoted pair (AGENTS.md).
- **`Sim.live()` keys** must match the `syms` keys of `pendulum.js` (listed above).
- **Formulas live in several places.** The accelerations are in `deriv()` ([L482–485](../../public/simulations/Double%20Pendulum.html#L482-L485)), in the store attributes
  ([L424–425](../../public/simulations/Double%20Pendulum.html#L424-L425)), in `alphaCheck()` ([L756–757](../../public/simulations/Double%20Pendulum.html#L756-L757)), in the walkthrough and in the note's eq. (9) ([L220](../../public/simulations/Double%20Pendulum.html#L220)). The energy is in
  `energy()` ([L500–502](../../public/simulations/Double%20Pendulum.html#L500-L502)), `kinetic()`/`potential()` ([L761–762](../../public/simulations/Double%20Pendulum.html#L761-L762)), the attributes ([L432–433](../../public/simulations/Double%20Pendulum.html#L432-L433)) and eqs. (3)–(4). The pixel map
  is in `pos()` and `layout()` ([L506–507](../../public/simulations/Double%20Pendulum.html#L506-L507), [L513](../../public/simulations/Double%20Pendulum.html#L513)), the checks ([L831–835](../../public/simulations/Double%20Pendulum.html#L831-L835)), the attributes ([L444–452](../../public/simulations/Double%20Pendulum.html#L444-L452)) and note §8
  ([L358](../../public/simulations/Double%20Pendulum.html#L358)). The bob-2 radius is in `drawPendulum()` ([L599](../../public/simulations/Double%20Pendulum.html#L599)) and `bobPixel()` ([L730](../../public/simulations/Double%20Pendulum.html#L730)). The expected colours in `bobPixel()`
  (122, 31, 43) and (90, 80, 75) are `Sim.theme.accent` and `Sim.theme.ink3` ([L729–732](../../public/simulations/Double%20Pendulum.html#L729-L732), [sim.js:16](../../public/scripts/sim.js#L16), [sim.js:12](../../public/scripts/sim.js#L12)).
- **Constants quoted in text.** h = 1/600 s appears in the caption ([L48](../../public/simulations/Double%20Pendulum.html#L48)), the note (§7, Figure 3) and the panel group note
  ([L778](../../public/simulations/Double%20Pendulum.html#L778)); 0.001 rad appears on the twin switch ([L61](../../public/simulations/Double%20Pendulum.html#L61)) and in the note. Change them together with `H` and `EPS` ([L396](../../public/simulations/Double%20Pendulum.html#L396)).
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
default start, λ ≈ 1.45 s⁻¹ (rescaling every 0.1 s over 20 000 s), with e^1.45 ≈ 4.3 and e^14.5 ≈ 2 × 10⁶ ([L335](../../public/simulations/Double%20Pendulum.html#L335), [L337](../../public/simulations/Double%20Pendulum.html#L337));
§7 says that the slider caps the time scale, that the drift creeps by about −7 × 10⁻⁸ a minute (−7.2 × 10⁻⁷ after ten
simulated minutes in Chromium), and that the step fails for a heavy lower bob: ε reaches −3.6 × 10⁻⁴ in 20 s at m₂/m₁ = 10
([L350](../../public/simulations/Double%20Pendulum.html#L350), [L351](../../public/simulations/Double%20Pendulum.html#L351)); §8 defines σ, the
pivot and W × H, draws the bobs with σ, names the two protractor circles and Δt, and writes the half-life as
ln 2/(60 |ln 0.992|) ([L358](../../public/simulations/Double%20Pendulum.html#L358), [L359](../../public/simulations/Double%20Pendulum.html#L359)); the three references link to pages opened that day ([L372–374](../../public/simulations/Double%20Pendulum.html#L372-L374)).

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig02/`), the lead made only these changes, each on its existing line, so no line link moved: equations (5), (8), (9) and (13) broken over two or three lines so their numbers show at 1440 px ([L206](../../public/simulations/Double%20Pendulum.html#L206)); (8) ([L218](../../public/simulations/Double%20Pendulum.html#L218)); (9) ([L220](../../public/simulations/Double%20Pendulum.html#L220)); (13) ([L347](../../public/simulations/Double%20Pendulum.html#L347)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

## Second check round · 20 October 2026

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig02/`), each change on its existing line: §5: the matrix whose determinant must vanish written out, and why ([L228](../../public/simulations/Double%20Pendulum.html#L228)); §6: why two nearby starts part (linear small swings; balancing near the top) ([L335](../../public/simulations/Double%20Pendulum.html#L335)); §6: the rough and full Lyapunov rates in one sentence; "much of what that energy allows" ([L337](../../public/simulations/Double%20Pendulum.html#L337)); §9: the Lyapunov time defined ([L368](../../public/simulations/Double%20Pendulum.html#L368)); equations (6), (9), (11) reflowed so their numbers show at 1600 px ([L212](../../public/simulations/Double%20Pendulum.html#L212)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.

From the Fig. 2 derivation check (65 verified, 4 wrong, 1 unverifiable; `notes/fig02/check.md`): abstract: 600 steps a second, sixty frames a second ([L119](../../public/simulations/Double%20Pendulum.html#L119)); §7: drift peak +5.0 × 10⁻⁸ step by step, +4.7 × 10⁻⁸ as the readout samples it ([L351](../../public/simulations/Double%20Pendulum.html#L351)); §8: the trail as the canvas really fades it (half in 1.6 s, then a faint haze at a quarter opacity) ([L359](../../public/simulations/Double%20Pendulum.html#L359)); §9: the computed path stays true for 15–20 Lyapunov times, 11–14 s ([L368](../../public/simulations/Double%20Pendulum.html#L368)). The trail's haze is a page defect, reported in the audit, not changed.
