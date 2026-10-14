# Fig. 2 · Double Pendulum

| | |
|---|---|
| Page | [public/simulations/Double Pendulum.html](../../public/simulations/Double%20Pendulum.html) (843 lines, 97 kB) |
| Walkthrough | [public/scripts/walk/pendulum.js](../../public/scripts/walk/pendulum.js) (137 lines, 8 steps, key `pendulum`) |
| Thumbnail | [public/images/sims/double-pendulum.webp](../../public/images/sims/double-pendulum.webp) (WebP, 800 × 500 px, 12.5 kB; the pendulum, its fading trail and the protractor) |
| Catalog entry | [public/scripts/catalog.js#L65](../../public/scripts/catalog.js#L65) (`id: 'double-pendulum'`, `fig: 2`, `field: 'mechanics'`, `stage: 2`, lines 64–80) |

Links written `Lnnn` point into the page file; links to other files carry the file name.

The reader sees a pendulum hanging from a pivot at the centre of the figure: an upper rod with a burgundy bob and a lower rod with
a second burgundy bob, inside a faint protractor marked every 30° ([L43–51](../../public/simulations/Double%20Pendulum.html#L43-L51), [L565–591](../../public/simulations/Double%20Pendulum.html#L565-L591)). Released from θ₁ = 120°,
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

**What the code evaluates.** Positions, with the pivot at the origin and y upward ([L658–659](../../public/simulations/Double%20Pendulum.html#L658-L659)):

$$x_1 = l_1\sin\theta_1, \quad y_1 = -l_1\cos\theta_1, \quad x_2 = x_1 + l_2\sin\theta_2, \quad y_2 = y_1 - l_2\cos\theta_2 .$$

Energy, in `energy(s)` ([L495–500](../../public/simulations/Double%20Pendulum.html#L495-L500)):

$$T = \tfrac12 (m_1+m_2)\,l_1^2\omega_1^2 + \tfrac12 m_2 l_2^2\omega_2^2 + m_2 l_1 l_2\,\omega_1\omega_2\cos(\theta_1-\theta_2),$$

$$V = -(m_1+m_2)\,g\,l_1\cos\theta_1 - m_2\,g\,l_2\cos\theta_2 .$$

The angular accelerations, in `deriv(s)` ([L475–483](../../public/simulations/Double%20Pendulum.html#L475-L483)), with $\delta = \theta_1 - \theta_2$ and the shared denominator
$D' = 2m_1 + m_2 - m_2\cos 2\delta = 2(m_1 + m_2\sin^2\delta) > 0$:

$$\alpha_1 = \frac{-g(2m_1+m_2)\sin\theta_1 - m_2 g\sin(\theta_1 - 2\theta_2) - 2\sin\delta\; m_2\left(\omega_2^2 l_2 + \omega_1^2 l_1\cos\delta\right)}{l_1 D'},$$

$$\alpha_2 = \frac{2\sin\delta\left(\omega_1^2 l_1 (m_1+m_2) + g(m_1+m_2)\cos\theta_1 + \omega_2^2 l_2 m_2\cos\delta\right)}{l_2 D'} .$$

These are eq. (9) of the note ([L220](../../public/simulations/Double%20Pendulum.html#L220)), obtained from the linear system (8) by Cramer's rule ([L218–219](../../public/simulations/Double%20Pendulum.html#L218-L219)). With the state
$s = (\theta_1, \theta_2, \omega_1, \omega_2)$ and $F(s) = (\omega_1, \omega_2, \alpha_1, \alpha_2)$, one step of the classical
fourth-order Runge–Kutta method with $h = 1/600$ s is ([L484–494](../../public/simulations/Double%20Pendulum.html#L484-L494), note eq. 13):

$$k_1 = F(s), \quad k_2 = F\left(s + \tfrac h2 k_1\right), \quad k_3 = F\left(s + \tfrac h2 k_2\right), \quad k_4 = F(s + h k_3), \quad s \leftarrow s + \tfrac h6\left(k_1 + 2k_2 + 2k_3 + k_4\right).$$

The energy check divides the change of $E = T + V$ by the depth of the potential well, not by $E_0$, which can be near zero
([L656](../../public/simulations/Double%20Pendulum.html#L656)):

$$\varepsilon = \frac{E - E_0}{(m_1+m_2)\,g\,l_1 + m_2\,g\,l_2} .$$

| Symbol | Code | Unit | Meaning |
|---|---|---|---|
| $\theta_1, \theta_2$ | `state[0]`, `state[1]` | rad | rod angles from the downward vertical |
| $\omega_1, \omega_2$ | `state[2]`, `state[3]` | rad/s | angular velocities |
| $\alpha_1, \alpha_2$ | `a1`, `a2` in `deriv` | rad/s² | angular accelerations |
| $m_1, m_2$ | `m1 = 1`, `m2` | kg | bob masses; m₂ = m₁ e^slider ([L527](../../public/simulations/Double%20Pendulum.html#L527)) |
| $l_1, l_2$ | `l1 = 1`, `l2` | m | rod lengths; l₂ = l₁ e^slider ([L528](../../public/simulations/Double%20Pendulum.html#L528)) |
| $g$ | `g = 9.81` | m/s² | gravitational acceleration ([L396](../../public/simulations/Double%20Pendulum.html#L396)) |
| $\delta$, $D'$ | `d`, `den` | rad, kg | angle between the rods, shared denominator |
| $h$ | `H = 1/600` | s | RK4 step ([L396](../../public/simulations/Double%20Pendulum.html#L396)) |
| $T, V, E, E_0$ | `kin`, `pot`, `energy(s)`, `E0` | J | kinetic, potential, total, total at restart |
| $\varepsilon$ | `drift` | 1 | relative energy error |
| $\sigma$ | `scale` | px/m | pixels per metre on screen ([L509](../../public/simulations/Double%20Pendulum.html#L509)) |
| $d$ | `sep` | m | distance between the two lower bobs (twin on) ([L666](../../public/simulations/Double%20Pendulum.html#L666)) |

## How the code computes it

**State.** `state` is a plain array [θ₁, θ₂, ω₁, ω₂] in rad and rad/s, set from the sliders by `restart()` ([L529](../../public/simulations/Double%20Pendulum.html#L529)); `twin`
is a second such array or `null` ([L530](../../public/simulations/Double%20Pendulum.html#L530)). `E0` is the energy at restart ([L531](../../public/simulations/Double%20Pendulum.html#L531)); `simT` the simulated time and `acc` the
unspent time carried between frames ([L532–533](../../public/simulations/Double%20Pendulum.html#L532-L533)). `m2` and `l2` come from the log-scale sliders ([L527–528](../../public/simulations/Double%20Pendulum.html#L527-L528)). For drawing:
`ox`, `oy` (pivot) and `scale` (σ) ([L507–509](../../public/simulations/Double%20Pendulum.html#L507-L509)); the offscreen canvas `trail` that holds the fading path ([L400](../../public/simulations/Double%20Pendulum.html#L400)); `prevA`,
`prevB`, the last pixel positions of the two pendulums, from which the next trail segment starts ([L402](../../public/simulations/Double%20Pendulum.html#L402)). `frames`, `lastN` and
`fps` count frames, steps and frame rate ([L402–403](../../public/simulations/Double%20Pendulum.html#L402-L403)).

**Method.** RK4 at a fixed step h = 1/600 s ([L396](../../public/simulations/Double%20Pendulum.html#L396)). Its error over a fixed time scales as h⁴ (note §7, [L348](../../public/simulations/Double%20Pendulum.html#L348)). A fixed step
keeps the accuracy the same on every device ([pendulum.js:86](../../public/scripts/walk/pendulum.js#L86)). RK4 does not conserve energy exactly, so the page shows the
drift ε rather than hiding it ([L351](../../public/simulations/Double%20Pendulum.html#L351), [L635](../../public/simulations/Double%20Pendulum.html#L635)). `rk4()` builds separate trial arrays `s2`, `s3`, `s4`, so all four slopes of a
step use their own input state ([L485–492](../../public/simulations/Double%20Pendulum.html#L485-L492)). Measured in this session (1280 px window, default start, headless Chromium):
ε = −2.4 × 10⁻⁸ at t = 21.2 s, n = 10 steps per frame at 60 frames per second, energy E = 18.3057 J.

**Sub-stepping.** Real frame times are uneven; the physics advances in equal steps. Each frame ([L694–697](../../public/simulations/Double%20Pendulum.html#L694-L697)):

$$\tau \leftarrow \tau + \Delta t \cdot \text{speed}, \qquad n = \min\left(\lfloor \tau / h \rfloor, 600\right), \qquad \tau \leftarrow \min(\tau - n h,\ h).$$

The leftover τ carries into the next frame, so simulated time keeps pace with wall time × speed. Because `Sim.clock` caps Δt at
0.05 s ([sim.js:180](../../public/scripts/sim.js#L180)) and the time scale is at most 1.5 ([L64](../../public/simulations/Double%20Pendulum.html#L64)), n is at most 46; the 600 cap never acts (see Notes).

**Frame loop** (`Sim.clock` callback, [L692–716](../../public/simulations/Double%20Pendulum.html#L692-L716)), in order:
1. If playing (Δt > 0): accumulate τ and choose n ([L694–697](../../public/simulations/Double%20Pendulum.html#L694-L697)). For each of the n steps: advance `state` by one RK4 step, compute
   its pixel positions, paint one trail segment of the lower bob, remember the position ([L699–702](../../public/simulations/Double%20Pendulum.html#L699-L702)); if the twin is on, do the
   same for it in rose ([L703–708](../../public/simulations/Double%20Pendulum.html#L703-L708)); add h to the simulated time ([L709](../../public/simulations/Double%20Pendulum.html#L709)). After the steps, dim the whole trail layer ([L711](../../public/simulations/Double%20Pendulum.html#L711)).
2. `diagnostics(dt)`: write every derived number of the final state into the store ([L713](../../public/simulations/Double%20Pendulum.html#L713), [L646–674](../../public/simulations/Double%20Pendulum.html#L646-L674)).
3. `draw()`: clear, protractor, trail image, twin, pendulum, pivot dot ([L714](../../public/simulations/Double%20Pendulum.html#L714), [L618–628](../../public/simulations/Double%20Pendulum.html#L618-L628)).
4. Every sixth frame, `readouts()` copies E, ε, the separation and the time from the store into the DOM ([L715](../../public/simulations/Double%20Pendulum.html#L715), [L631–642](../../public/simulations/Double%20Pendulum.html#L631-L642)).

While paused `Sim.clock` passes Δt = 0 ([sim.js:182](../../public/scripts/sim.js#L182)): no steps and no fading, but `diagnostics()` and `draw()` still run every
frame.

**`diagnostics(dt)`** ([L646–674](../../public/simulations/Double%20Pendulum.html#L646-L674)) evaluates `deriv` once more at the final state for the stored slopes and accelerations
([L647](../../public/simulations/Double%20Pendulum.html#L647)), copies the state ([L648](../../public/simulations/Double%20Pendulum.html#L648)), then computes and stores δ, D′, α₁, α₂ ([L651](../../public/simulations/Double%20Pendulum.html#L651)), the mass matrix M and its determinant,
the generalised momenta ([L652–654](../../public/simulations/Double%20Pendulum.html#L652-L654)), E, V, T = E − V, L = T − V and ε ([L655–657](../../public/simulations/Double%20Pendulum.html#L655-L657)), positions and speeds in metres
([L658–661](../../public/simulations/Double%20Pendulum.html#L658-L661)), bob pixel positions ([L662–663](../../public/simulations/Double%20Pendulum.html#L662-L663)), the twin separation ([L664–670](../../public/simulations/Double%20Pendulum.html#L664-L670)) and the clock and integrator scalars
([L671–673](../../public/simulations/Double%20Pendulum.html#L671-L673)).

**Precomputation and caching.** There are no tables. The path is cached as pixels on the `trail` canvas: one segment per RK4
step ([L546–555](../../public/simulations/Double%20Pendulum.html#L546-L555)), dimmed each frame by drawing a black rectangle in `destination-out` mode with alpha 1 − 0.992^(60Δt)
([L556–563](../../public/simulations/Double%20Pendulum.html#L556-L563), [L711](../../public/simulations/Double%20Pendulum.html#L711)), so its brightness halves every ln 2/(60 × 0.00803) ≈ 1.4 s of real time ([L359](../../public/simulations/Double%20Pendulum.html#L359)). The trail is cleared
by Restart, by any restarting slider, by *Clear trail* and by a resize ([L512–517](../../public/simulations/Double%20Pendulum.html#L512-L517), [L537](../../public/simulations/Double%20Pendulum.html#L537), [L544](../../public/simulations/Double%20Pendulum.html#L544), [L523](../../public/simulations/Double%20Pendulum.html#L523)). `layout()`
recomputes pivot and scale on restart and on resize ([L506–511](../../public/simulations/Double%20Pendulum.html#L506-L511)).

## Function map

All functions live in the one inline script ([L392–840](../../public/simulations/Double%20Pendulum.html#L392-L840)), wrapped in an immediately invoked function ([L393](../../public/simulations/Double%20Pendulum.html#L393)).

| Function | Lines | What it does |
|---|---|---|
| `ratio(v)` | [L463](../../public/simulations/Double%20Pendulum.html#L463) | Slider text for the log-scale ratios: e^v as "1.00", or "1/x.xx" below 1. |
| `deg(v)` | [L464](../../public/simulations/Double%20Pendulum.html#L464) | Slider text in degrees. |
| `rads(v)` | [L465](../../public/simulations/Double%20Pendulum.html#L465) | Slider text in rad/s. |
| speed slider `format` | [L473](../../public/simulations/Double%20Pendulum.html#L473) | Slider text "1.00×". |
| `deriv(s)` | [L475–483](../../public/simulations/Double%20Pendulum.html#L475-L483) | Right-hand side of the equations: returns (ω₁, ω₂, α₁, α₂). |
| `rk4(s, h)` | [L484–494](../../public/simulations/Double%20Pendulum.html#L484-L494) | One classical RK4 step; returns the new state. |
| `energy(s)` | [L495–500](../../public/simulations/Double%20Pendulum.html#L495-L500) | Kinetic plus potential energy of a state. |
| `pos(s)` | [L501–504](../../public/simulations/Double%20Pendulum.html#L501-L504) | Pixel positions [x₁, y₁, x₂, y₂] of the two bobs (screen y down). |
| `layout()` | [L506–511](../../public/simulations/Double%20Pendulum.html#L506-L511) | Pivot at the canvas centre; σ = (min(W, H)/2 − 34)/(l₁ + l₂); stores them. |
| `clearTrail()` | [L512–517](../../public/simulations/Double%20Pendulum.html#L512-L517) | Clears the trail canvas and forgets the last positions. |
| `resize()` | [L518–524](../../public/simulations/Double%20Pendulum.html#L518-L524) | Fits the canvas, resizes the trail canvas to device pixels, `layout()`, `clearTrail()`. |
| `restart()` | [L526–538](../../public/simulations/Double%20Pendulum.html#L526-L538) | Reads all sliders, sets m₂, l₂, the state, the twin, E₀, t = 0, τ = 0; stores the parameters; `layout()`, `clearTrail()`. |
| twin `change` handler | [L539–542](../../public/simulations/Double%20Pendulum.html#L539-L542) | Twin on: copy of the current state with θ₁ + 0.001 rad; off: `null`. |
| Restart / Clear handlers | [L543–544](../../public/simulations/Double%20Pendulum.html#L543-L544) | `restart` and `clearTrail`. |
| `segment(prev, p, colour, width)` | [L546–555](../../public/simulations/Double%20Pendulum.html#L546-L555) | One trail segment of the lower bob. |
| `fade(a)` | [L556–563](../../public/simulations/Double%20Pendulum.html#L556-L563) | Removes the fraction a of every trail pixel's opacity. |
| `drawProtractor()` | [L565–591](../../public/simulations/Double%20Pendulum.html#L565-L591) | Outer circle at l₁ + l₂, dashed circle at l₁, ticks and labels every 30°. |
| `drawPendulum(s, ghost)` | [L593–616](../../public/simulations/Double%20Pendulum.html#L593-L616) | Rods and bobs; bob 1 radius 8 px, bob 2 radius clamp(8 ∛(m₂/m₁), 4, 17) px; ghost = twin in rose. |
| `draw()` | [L618–628](../../public/simulations/Double%20Pendulum.html#L618-L628) | One picture, in painting order. |
| `readouts()` | [L631–642](../../public/simulations/Double%20Pendulum.html#L631-L642) | Caption time, E, ε and the separation, read from the store. |
| `diagnostics(dt)` | [L646–674](../../public/simulations/Double%20Pendulum.html#L646-L674) | Writes the store (above). |
| `f4(v, u)` | [L677](../../public/simulations/Double%20Pendulum.html#L677) | Four-decimal formatting for `Sim.live`. |
| `Sim.live()` | [L678–690](../../public/simulations/Double%20Pendulum.html#L678-L690) | Strings for the walkthrough's "Now" column, read from the store. |
| clock callback | [L692–716](../../public/simulations/Double%20Pendulum.html#L692-L716) | The frame loop above. |
| `sliderCheck(input, label, scale)` | [L721](../../public/simulations/Double%20Pendulum.html#L721) | Check record for a slider value, optionally × π/180. |
| `bobPixel(name, x, y)` | [L722–731](../../public/simulations/Double%20Pendulum.html#L722-L731) | Reads the screen pixel at a bob's stored centre; passes for burgundy, or for the pivot dot or bob 2's rim painted over it; tests alpha first. |
| `alphaCheck(which)` | [L732–738](../../public/simulations/Double%20Pendulum.html#L732-L738) | Recomputes α₁ or α₂ from the stored state. |
| `stateInputs()` | [L739](../../public/simulations/Double%20Pendulum.html#L739) | The stored state and parameters, as check inputs. |
| `kinetic()`, `potential()` | [L740–741](../../public/simulations/Double%20Pendulum.html#L740-L741) | T and V recomputed from the stored state. |
| `nearest(x, y)` | [L742–746](../../public/simulations/Double%20Pendulum.html#L742-L746) | Bob 2, bob 1 or the pivot, whichever is nearest within 28 px. |
| `Sim.data.playing`, `.play` | [L749](../../public/simulations/Double%20Pendulum.html#L749), [L831](../../public/simulations/Double%20Pendulum.html#L831) | Clock state and start, for the round recorder. |
| `Sim.data.rowLabel`, `.colLabel`, `.at` | [L759–761](../../public/simulations/Double%20Pendulum.html#L759-L761) | Row, column and unit labels for the arrays `y`, `dydt`, `y_twin`, `M`. |
| `Sim.data.probe(x, y)` | [L762](../../public/simulations/Double%20Pendulum.html#L762) | What lies at a point: `{ what: … }` with 'bob 2', 'bob 1' or 'pivot', from `nearest()`. |
| `Sim.data.inspect(ref)` | [L763–769](../../public/simulations/Double%20Pendulum.html#L763-L769) | Values for a bob (angle, ω, α, position, speed, momentum, separation) or for the whole system at the pivot. |
| `Sim.data.locate(name, idx)` | [L770–774](../../public/simulations/Double%20Pendulum.html#L770-L774) | Where a state component or M is drawn. |
| `Sim.data.check.*` | [L776–819](../../public/simulations/Double%20Pendulum.html#L776-L819) | One function per variable: formula, stored inputs, recomputed value. |
| `Sim.data.drawn.*` | [L822–827](../../public/simulations/Double%20Pendulum.html#L822-L827) | Pixel read-back at bob 1 and bob 2 for θ and the pixel positions. |
| `Sim.data.round.label`, `.length`, `.point` | [L829–830](../../public/simulations/Double%20Pendulum.html#L829-L830) | What one recorded round is. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Pause / Play | `play` | starts playing unless the reader prefers reduced motion ([sim.js:178](../../public/scripts/sim.js#L178)) | `Sim.playButton` toggles the clock ([L717](../../public/simulations/Double%20Pendulum.html#L717)). |
| Restart | `restart` | — | `restart()` from the current slider values ([L543](../../public/simulations/Double%20Pendulum.html#L543), [L526–538](../../public/simulations/Double%20Pendulum.html#L526-L538)). |
| Clear trail | `clear` | — | `clearTrail()` ([L544](../../public/simulations/Double%20Pendulum.html#L544)). |
| Chaos twin | `twin` (checkbox) | off ([L61](../../public/simulations/Double%20Pendulum.html#L61)) | On: twin = current state with θ₁ + 0.001 rad, so mid-run it starts from where the pendulum is now; off: no twin ([L539–542](../../public/simulations/Double%20Pendulum.html#L539-L542)). Restart re-creates it from the starting state ([L530](../../public/simulations/Double%20Pendulum.html#L530)). |
| Time scale | `speed` | 0.25–1.5, step 0.05, default 1 ([L64](../../public/simulations/Double%20Pendulum.html#L64)) | Read every frame as simulated seconds per real second ([L694](../../public/simulations/Double%20Pendulum.html#L694)); does not restart. |
| Mass ratio m₂/m₁ | `mass` | −2.3 to 2.3, step 0.05, default 0 ([L72](../../public/simulations/Double%20Pendulum.html#L72)); m₂ = e^slider kg, 0.100–9.97 kg | `restart()` ([L467](../../public/simulations/Double%20Pendulum.html#L467), [L527](../../public/simulations/Double%20Pendulum.html#L527)). |
| Length ratio l₂/l₁ | `length` | −1.6 to 1.6, step 0.05, default 0 ([L76](../../public/simulations/Double%20Pendulum.html#L76)); l₂ = e^slider m, 0.202–4.95 m | `restart()` ([L468](../../public/simulations/Double%20Pendulum.html#L468), [L528](../../public/simulations/Double%20Pendulum.html#L528)); also changes σ. |
| Angle θ₁ | `th1` | −180° to 180°, step 1°, default 120° ([L84](../../public/simulations/Double%20Pendulum.html#L84)) | `restart()`; converted to rad once ([L529](../../public/simulations/Double%20Pendulum.html#L529)). |
| Angle θ₂ | `th2` | −180° to 180°, step 1°, default 150° ([L88](../../public/simulations/Double%20Pendulum.html#L88)) | `restart()`. |
| Angular velocity ω₁ | `w1` | −5 to 5 rad/s, step 0.1, default 0 ([L92](../../public/simulations/Double%20Pendulum.html#L92)) | `restart()`. |
| Angular velocity ω₂ | `w2` | −5 to 5 rad/s, step 0.1, default 0 ([L96](../../public/simulations/Double%20Pendulum.html#L96)) | `restart()`. |

Readouts: `r-e` shows E to three decimals in J ([L634](../../public/simulations/Double%20Pendulum.html#L634)); `r-drift` shows ε with one decimal in exponent form, or "0" below
10⁻¹² ([L635](../../public/simulations/Double%20Pendulum.html#L635)); `r-sep` shows the separation in m, or "twin off" ([L636–641](../../public/simulations/Double%20Pendulum.html#L636-L641)); `cap-t` in the caption shows t to 0.1 s
([L633](../../public/simulations/Double%20Pendulum.html#L633)). The caption also carries "RK4, h = 1/600 s" typeset by KaTeX ([L48](../../public/simulations/Double%20Pendulum.html#L48), [sim.js:458–464](../../public/scripts/sim.js#L458-L464)). Measured with the twin
on from the default start: separation 2.456 m after t = 6.03 s.

## What the page writes into the data store

The store is created by `Sim.dataset({ title: 'Double pendulum', attrs: {...} })` ([L406](../../public/simulations/Double%20Pendulum.html#L406); see
[dataset.md](../scripts/dataset.md)). Its attributes hold the fixed constants: `figure: 2`, `page`, `g`, `m1`, `l1`, `EPS`, `H`,
`integrator` and `units: 'SI: kg, m, s, rad'`. Dimensions: `q = 4` for state vectors ([L414](../../public/simulations/Double%20Pendulum.html#L414)), `a = 2` and `b = 2` for the mass
matrix ([L426–427](../../public/simulations/Double%20Pendulum.html#L426-L427)). The running page holds 52 variables: 4 arrays and 48 scalars. Every value is written once per frame in
`diagnostics()`, except the parameters (written by `restart()`) and the layout (written by `layout()`).

| Array | Dims, type | Written at |
|---|---|---|
| `y` (state), `dydt` (ω₁, ω₂, α₁, α₂), `y_twin` (zeros while the twin is off) | (q), Float64 | [L648](../../public/simulations/Double%20Pendulum.html#L648) |
| `M` (mass matrix, T = ½ ωᵀ M ω) | (a, b), Float64 | [L652](../../public/simulations/Double%20Pendulum.html#L652) |

Scalars, by the place that writes them:
- `restart()`: `m2`, `l2`, `E0`, `th1_0`, `th2_0`, `w1_0`, `w2_0` ([L534–535](../../public/simulations/Double%20Pendulum.html#L534-L535)).
- `layout()`: `scale`, `ox`, `oy` ([L510](../../public/simulations/Double%20Pendulum.html#L510)).
- `diagnostics()`: `th1`, `th2`, `w1`, `w2` ([L650](../../public/simulations/Double%20Pendulum.html#L650)); `delta`, `den`, `alpha1`, `alpha2` ([L651](../../public/simulations/Double%20Pendulum.html#L651)); `detM`, `p1`, `p2`
  ([L654](../../public/simulations/Double%20Pendulum.html#L654)); `E`, `V`, `T`, `L`, `drift` ([L657](../../public/simulations/Double%20Pendulum.html#L657)); `x1`, `y1`, `x2`, `y2` ([L659](../../public/simulations/Double%20Pendulum.html#L659)); `v1`, `v2` ([L661](../../public/simulations/Double%20Pendulum.html#L661)); `x1_px`, `y1_px`,
  `x2_px`, `y2_px` ([L663](../../public/simulations/Double%20Pendulum.html#L663)); `twin_on` ([L664](../../public/simulations/Double%20Pendulum.html#L664)); `sep`, `log10sep` ([L667](../../public/simulations/Double%20Pendulum.html#L667), or `undefined` when the twin is off, [L669](../../public/simulations/Double%20Pendulum.html#L669));
  `t`, `steps`, `n`, `acc`, `speed` ([L671](../../public/simulations/Double%20Pendulum.html#L671)); `dt`, `fps`, `frames`, `playing` ([L673](../../public/simulations/Double%20Pendulum.html#L673)).

Two stored values are derived in a particular way: T is stored as E − V ([L655](../../public/simulations/Double%20Pendulum.html#L655)), and the separation is the distance between the
two bob-2 pixel positions divided by σ ([L666](../../public/simulations/Double%20Pendulum.html#L666)). Both equal the direct formulas up to rounding; the checks recompute them
directly ([L798](../../public/simulations/Double%20Pendulum.html#L798), [L816](../../public/simulations/Double%20Pendulum.html#L816)).

The panel spec `Sim.data` ([L747–833](../../public/simulations/Double%20Pendulum.html#L747-L833); see [datalog.md](../scripts/datalog.md)) lists seven groups ([L750–758](../../public/simulations/Double%20Pendulum.html#L750-L758)), labels the
rows of `y`, `dydt`, `y_twin` and `M` as θ₁, θ₂, ω₁, ω₂ ([L759–761](../../public/simulations/Double%20Pendulum.html#L759-L761)) and saves as `fig2-double-pendulum` ([L748](../../public/simulations/Double%20Pendulum.html#L748)). Its `about`
paragraph says what differs between store and picture ([L832](../../public/simulations/Double%20Pendulum.html#L832)).

**One round** (`Sim.data.round`, [L829–830](../../public/simulations/Double%20Pendulum.html#L829-L830)) is ten seconds of simulated time `t`. Columns charted: `th1`, `th2`, `w1`, `w2`,
`E`, `drift`, `sep`; the recorder also copies every numeric scalar, and follows bob 2 unless another point is pinned. With at most
600 samples the interval is 10/600 s ([datalog.js:743](../../public/scripts/datalog.js#L743), [datalog.js:770](../../public/scripts/datalog.js#L770)). Every restart sets t back to 0, so moving a
restarting slider during a round puts t below the round's start and the recorder ends it ("the clock was reset",
[datalog.js:791](../../public/scripts/datalog.js#L791)).

**`Sim.live()`** ([L678–690](../../public/simulations/Double%20Pendulum.html#L678-L690)) returns formatted strings under the keys `t1`, `t2`, `o1`, `o2`, `d`, `den`, `m2`, `l2`, `a1`,
`a2`, `k1`, `h`, `n`, `acc`, `t`, `kin`, `pot`, `E`, `E0`, `drift`, `scale`, `y1`; all read from the store except `h`, the constant
`H`. The walkthrough polls it every 200 ms unless "Hold the numbers" is on ([sim.js:388–400](../../public/scripts/sim.js#L388-L400)).

**Proof, measured in this session** (1280 px window, default start, paused after about 3 s; stored value against the page's own
`check` functions): α₁, α₂, T, V, E, ε, x₂, y₂, x₂ px, y₂ px, det M and p_θ₁ were identical, difference 0, because store and
check use the same float64 expressions. The screen pixels at the stored centres of bob 1 and bob 2 were rgb(122, 31, 43), the
burgundy fill.

## Page structure

**Head** ([L3–15](../../public/simulations/Double%20Pendulum.html#L3-L15)): title "Double Pendulum Chaos · Numa Koudsie" and description ([L6–7](../../public/simulations/Double%20Pendulum.html#L6-L7)); preconnects to Google Fonts
([L9–10](../../public/simulations/Double%20Pendulum.html#L9-L10)); stylesheets in order `../styles/sim.css`, `../styles/data.css`, `../styles/fold.css` ([L11–13](../../public/simulations/Double%20Pendulum.html#L11-L13)); an inline SVG
favicon ([L14](../../public/simulations/Double%20Pendulum.html#L14)). No inline style. See [styles.md](../styles.md).

**Body**, top to bottom:
- Top bar with "← All simulations" and the hand-written Fig. 1–10 links ([L17–32](../../public/simulations/Double%20Pendulum.html#L17-L32)); a `<noscript>` message ([L35](../../public/simulations/Double%20Pendulum.html#L35)).
- Heading: "Fig. 2 · classical mechanics · chaos", the title, the lede ([L36–40](../../public/simulations/Double%20Pendulum.html#L36-L40)).
- The figure: `#stage` with aspect ratio 4 : 3, and 1 : 1.05 below 900 px ([L44](../../public/simulations/Double%20Pendulum.html#L44), [sim.css:287–289](../../public/styles/sim.css#L287-L289)); the canvas `#pend`
  ([L45](../../public/simulations/Double%20Pendulum.html#L45)); the caption with `cap-t` ([L47–50](../../public/simulations/Double%20Pendulum.html#L47-L50)). The canvas is transparent where nothing is drawn, so the stage's grid
  background shows through ([L619](../../public/simulations/Double%20Pendulum.html#L619), [sim.css:68](../../public/styles/sim.css#L68)). `datalog.js` adds the Read values switch to the caption and the reading
  strip under the stage ([datalog.js:566–590](../../public/scripts/datalog.js#L566-L590)).
- The control panel ([L53–111](../../public/simulations/Double%20Pendulum.html#L53-L111)): Run (buttons, twin switch, time scale), Coupling (two ratios), Initial conditions (four
  sliders), readouts, legend.
- The lecture note `<article class="paper" id="paper">` ([L114–379](../../public/simulations/Double%20Pendulum.html#L114-L379)).
- The walkthrough host `<section class="walk" id="walk" data-walk="pendulum">` ([L381](../../public/simulations/Double%20Pendulum.html#L381)).
- Footer ([L384–387](../../public/simulations/Double%20Pendulum.html#L384-L387)).
- Scripts in load order: `../scripts/fold.js`, `../scripts/sim.js`, `../scripts/dataset.js` ([L389–391](../../public/simulations/Double%20Pendulum.html#L389-L391)), the page's own script
  ([L392–840](../../public/simulations/Double%20Pendulum.html#L392-L840)), then `../scripts/datalog.js` ([L841](../../public/simulations/Double%20Pendulum.html#L841)). `sim.js` loads `../scripts/walk/pendulum.js` from the `data-walk` key
  ([sim.js:476–486](../../public/scripts/sim.js#L476-L486)). See [sim.md](../scripts/sim.md), [fold.md](../scripts/fold.md), [walk.md](../scripts/walk.md),
  [pages.md](../pages.md).

The script ends by calling `restart()`, `resize()`, `diagnostics(0)` and registering the resize observer ([L835–838](../../public/simulations/Double%20Pendulum.html#L835-L838)).

**Walkthrough** ([pendulum.js](../../public/scripts/walk/pendulum.js), 8 steps). A script run in this session confirmed that
every quoted line is identical, after trimming indentation, to the page line listed.

| Step | Title | Page lines quoted |
|---|---|---|
| 1 | The state vector | [L529](../../public/simulations/Double%20Pendulum.html#L529) |
| 2 | Angle difference and the shared denominator | [L476–477](../../public/simulations/Double%20Pendulum.html#L476-L477) |
| 3 | Upper angular acceleration α₁ | [L478–479](../../public/simulations/Double%20Pendulum.html#L478-L479) |
| 4 | Lower angular acceleration α₂ | [L480–482](../../public/simulations/Double%20Pendulum.html#L480-L482) |
| 5 | One Runge–Kutta 4 step | [L485–492](../../public/simulations/Double%20Pendulum.html#L485-L492) |
| 6 | How many steps per frame | [L694–699](../../public/simulations/Double%20Pendulum.html#L694-L699), [L709](../../public/simulations/Double%20Pendulum.html#L709) |
| 7 | Energy as the accuracy check | [L496–499](../../public/simulations/Double%20Pendulum.html#L496-L499), [L656](../../public/simulations/Double%20Pendulum.html#L656) |
| 8 | From angles to pixels | [L509](../../public/simulations/Double%20Pendulum.html#L509), [L502–503](../../public/simulations/Double%20Pendulum.html#L502-L503) |

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

The page states the main point in `about` ([L832](../../public/simulations/Double%20Pendulum.html#L832)): rods and bobs are drawn at the stored pixel positions, so picture and store
agree to the pixel; the trail is not stored.
- **Trail.** Painted segment by segment at every RK4 step and faded each frame ([L701](../../public/simulations/Double%20Pendulum.html#L701), [L706](../../public/simulations/Double%20Pendulum.html#L706), [L711](../../public/simulations/Double%20Pendulum.html#L711)); it is not kept as an
  array. To keep a trajectory, record a round.
- **Sub-steps.** The store holds the state at the end of each frame only ([L648](../../public/simulations/Double%20Pendulum.html#L648)). At 60 frames per second about ten RK4 states
  per frame reach the trail but not the store.
- **Bob sizes.** Bob 1 has radius 8 px; bob 2 has 8 ∛(m₂/m₁) px clamped to 4–17 px ([L595](../../public/simulations/Double%20Pendulum.html#L595)). The clamp acts below
  m₂ = 0.125 kg and above 9.6 kg, inside the slider's range of 0.100–9.97 kg.
- **Readout rate.** The readouts and the caption time are rewritten every sixth frame, about ten times a second ([L715](../../public/simulations/Double%20Pendulum.html#L715)); the
  store changes every frame. ε is shown with two significant figures ([L635](../../public/simulations/Double%20Pendulum.html#L635)).
- **Twin.** The twin is drawn in rose with thinner rods and no rim ([L596–614](../../public/simulations/Double%20Pendulum.html#L596-L614)); only its state (`y_twin`) and the separation are
  stored.

## How to change it safely

- **Walkthrough excerpts.** `pendulum.js` quotes [L476–482](../../public/simulations/Double%20Pendulum.html#L476-L482), [L485–492](../../public/simulations/Double%20Pendulum.html#L485-L492), [L496–499](../../public/simulations/Double%20Pendulum.html#L496-L499), [L502–503](../../public/simulations/Double%20Pendulum.html#L502-L503), [L509](../../public/simulations/Double%20Pendulum.html#L509), [L529](../../public/simulations/Double%20Pendulum.html#L529), [L656](../../public/simulations/Double%20Pendulum.html#L656),
  [L694–699](../../public/simulations/Double%20Pendulum.html#L694-L699) and [L709](../../public/simulations/Double%20Pendulum.html#L709). Keep them character for character, or change `pendulum.js` in the same edit. Insert store taps after a
  quoted line, never inside a quoted pair (AGENTS.md).
- **`Sim.live()` keys** must match the `syms` keys of `pendulum.js` (listed above).
- **Formulas live in several places.** The accelerations are in `deriv()` ([L478–481](../../public/simulations/Double%20Pendulum.html#L478-L481)), in the store attributes
  ([L424–425](../../public/simulations/Double%20Pendulum.html#L424-L425)), in `alphaCheck()` ([L735–736](../../public/simulations/Double%20Pendulum.html#L735-L736)), in the walkthrough and in the note's eq. (9) ([L220](../../public/simulations/Double%20Pendulum.html#L220)). The energy is in
  `energy()` ([L496–498](../../public/simulations/Double%20Pendulum.html#L496-L498)), `kinetic()`/`potential()` ([L740–741](../../public/simulations/Double%20Pendulum.html#L740-L741)), the attributes ([L432–433](../../public/simulations/Double%20Pendulum.html#L432-L433)) and eqs. (3)–(4). The pixel map
  is in `pos()` and `layout()` ([L502–503](../../public/simulations/Double%20Pendulum.html#L502-L503), [L509](../../public/simulations/Double%20Pendulum.html#L509)), the checks ([L809–813](../../public/simulations/Double%20Pendulum.html#L809-L813)), the attributes ([L444–448](../../public/simulations/Double%20Pendulum.html#L444-L448)) and note §8
  ([L358](../../public/simulations/Double%20Pendulum.html#L358)). The bob-2 radius is in `drawPendulum()` ([L595](../../public/simulations/Double%20Pendulum.html#L595)) and `bobPixel()` ([L724](../../public/simulations/Double%20Pendulum.html#L724)). The expected colours in `bobPixel()`
  (122, 31, 43) and (90, 80, 75) are `Sim.theme.accent` and `Sim.theme.ink3` ([L723–726](../../public/simulations/Double%20Pendulum.html#L723-L726), [sim.js:12](../../public/scripts/sim.js#L12), [sim.js:16](../../public/scripts/sim.js#L16)).
- **Constants quoted in text.** h = 1/600 s appears in the caption ([L48](../../public/simulations/Double%20Pendulum.html#L48)), the note (§7, Figure 3) and the panel group note
  ([L757](../../public/simulations/Double%20Pendulum.html#L757)); 0.001 rad appears on the twin switch ([L61](../../public/simulations/Double%20Pendulum.html#L61)) and in the note. Change them together with `H` and `EPS` ([L396](../../public/simulations/Double%20Pendulum.html#L396)).
- **The catalog** entry's `equation`, `model`, `method` and `controls` ([catalog.js:73–76](../../public/scripts/catalog.js#L73-L76)) describe this page.
- **Re-test** after any change: Check α₁, α₂, E, ε and x₂ px in the Data panel (stored, recomputed, pixel); watch ε stay near
  10⁻⁸ for 20 s from the default start; switch the twin on and see the separation grow; record one round; pin bob 2 with Read
  values; resize between 390 px and 1440 px.

## Notes for maintainers

1. **The 600-step cap cannot act.** `n = Math.min(Math.floor(acc / H), 600)` and `acc = Math.min(acc - n * H, H)`
   ([L695](../../public/simulations/Double%20Pendulum.html#L695), [L697](../../public/simulations/Double%20Pendulum.html#L697)). Δt is capped at 0.05 s by `Sim.clock` ([sim.js:180](../../public/scripts/sim.js#L180)) and the time scale at 1.5 ([L64](../../public/simulations/Double%20Pendulum.html#L64)), so τ never
   exceeds 0.075 + h and n never exceeds 46. The note ([L350](../../public/simulations/Double%20Pendulum.html#L350)), the walkthrough step 6 note ([pendulum.js:86](../../public/scripts/walk/pendulum.js#L86)) and the store
   attribute of `n` ([L455](../../public/simulations/Double%20Pendulum.html#L455)) describe the cap as a working safety limit. Harmless dead guard.
2. **Drift sign.** The note says the Drift readout "measures |E − E₀|" ([L351](../../public/simulations/Double%20Pendulum.html#L351)); the code stores and shows the signed
   ε = (E − E₀)/E_scale ([L656](../../public/simulations/Double%20Pendulum.html#L656), [L635](../../public/simulations/Double%20Pendulum.html#L635)). Measured: −2.4 × 10⁻⁸ at 21 s, shown with its minus sign.
3. **"Every RK4 step" in the store attributes.** `y` and `y_twin` say `updates: 'every RK4 step'` and `th1`…`w2` say
   `computed_in: 'rk4()'` ([L415](../../public/simulations/Double%20Pendulum.html#L415), [L417](../../public/simulations/Double%20Pendulum.html#L417), [L418–421](../../public/simulations/Double%20Pendulum.html#L418-L421)); the store is written once per frame in `diagnostics()` ([L648](../../public/simulations/Double%20Pendulum.html#L648),
   [L650](../../public/simulations/Double%20Pendulum.html#L650)), and the intermediate steps are not stored.
4. **Equation labels in the walkthrough.** Step 3 says "Cramer's rule on (E1)–(E2) in the derivation" ([pendulum.js:40](../../public/scripts/walk/pendulum.js#L40)); the
   note numbers these equations (6) and (7) and the system (8) ([L212](../../public/simulations/Double%20Pendulum.html#L212), [L215](../../public/simulations/Double%20Pendulum.html#L215), [L218](../../public/simulations/Double%20Pendulum.html#L218)).
5. **`locate` for the twin.** `locate('y_twin', idx)` returns the main pendulum's bob positions, not the twin's ([L771](../../public/simulations/Double%20Pendulum.html#L771)).
6. **Bob size.** Note §8 says each mass has radius proportional to m^(1/3) ([L359](../../public/simulations/Double%20Pendulum.html#L359)); the code clamps bob 2 to 4–17 px
   ([L595](../../public/simulations/Double%20Pendulum.html#L595)), which departs from the rule at both ends of the mass slider.
