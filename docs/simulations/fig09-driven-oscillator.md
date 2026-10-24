# Fig. 9 · Driven Oscillator

| | |
|---|---|
| Page | [public/simulations/driven-oscillator.html](../../public/simulations/driven-oscillator.html) (1690 lines, 287497 bytes) |
| Walkthrough | [public/scripts/walk/driven.js](../../public/scripts/walk/driven.js) (14 steps, key `driven`) |
| Thumbnail | [public/images/sims/driven-oscillator.webp](../../public/images/sims/driven-oscillator.webp) (WebP, 800 × 500 px, 23.7 kB) |
| Catalog entry | [public/scripts/catalog.js#L183](../../public/scripts/catalog.js#L183-L199) (`id: 'driven-oscillator'`, `fig: 9`, `field: 'control'`, `stage: 1`, lines 183–199) |

A block of mass 1 kg sits on a spring and a damper and is pushed from its other side by a moving-coil drive: a coil on a
tube fixed to the block sits in the gap of a magnet, and the force on the block is $F = B\ell I$ with $B\ell = 10$ T·m. In
open loop the current source drives $I_0\cos\Omega t$, a push that does not care where the block is. With the controller
on, a PID controller $u = K_p(r-x) + K_i\int(r-x)\,dt - K_d\dot x$ adds its force through the same coil and holds the block
at an equilibrium it decides (lecture note §9, equations (12)–(16)). The reader sets the spring constant $k$ (the natural
frequency $f_0 = \sqrt{k/m}/2\pi$ follows), the damping ratio, the push amplitude and frequency, the target $r$ and the
three gains (presets Off, P, PD, PID), presses **Solve**, or grabs the block and drags it: while held, the clock stops, the
controller pulls against the hand and its integral keeps adding up (windup); on release the page solves a new run from the
released $x(0)$, $\dot x(0)$, $z(0)$. It
watches the stored run play back: the block with the three forces on it as arrows, the coil and its current, the damper with
its oil shaded by the heat it makes, energy bars $W_\text{in}$, $W_\text{loss}$, $E$, the controller box with its three
parts, the previous run as an outlined block and a dotted curve at the same scale, a moving window chart of $x(t)$, a strip
of the whole 60 s run, a force profile ($u$ with its P, I, D parts, the push, $-kx$, $-c\dot x$ over the same window), and a
frequency response: in its default linear view the amplitude function $A(f) = F_0|G|$ (or $F_0|H|$ with the loop on) in
metres and the phase difference $\varphi(f)$, from an even grid of 1281 frequencies; a button switches to the Bode view
(per newton, log axes, 241 frequencies). The closed loop is drawn in ink, the bare plant dashed behind it. The page never integrates
while the reader watches. It solves the whole run first with the classical fourth-order Runge–Kutta method (RK4), writes
every sample into its dataset, and each frame then draws one stored row.

In this page, a link such as [L771](../../public/simulations/driven-oscillator.html#L771) points to a line of
`driven-oscillator.html`. Other files are named in the link text.

## The physics in one picture

**What you would see.** Push a child on a swing. Pushed at the wrong moments it barely moves; pushed in time with its own
rhythm it swings high. At first the swing also rings at its own rhythm, so two rhythms beat against each other; after a
while only the pusher's rhythm is left.

**The model.** Three forces act along the floor: the spring $-kx$, the damper $-c\dot x$ and the driver $F(t)$. Newton's
second law gives $m\ddot x + c\dot x + kx = F_0\cos\Omega t$. The time $t$ appears on its own inside the cosine: the clock
belongs to someone else. The lecture note derives this in sections 1–2
([L204](../../public/simulations/driven-oscillator.html#L204), [L241](../../public/simulations/driven-oscillator.html#L241)),
the exact solution in section 3 ([L251](../../public/simulations/driven-oscillator.html#L251)), resonance and phase in
section 4, the transfer function in section 5, beats in section 6 and the energy balance in section 7.

**What the code evaluates.** The sliders give $f_0$, $\zeta$, $F_0$ and $f$; `solve()` turns them into the constants of the
equation of motion ([L771](../../public/simulations/driven-oscillator.html#L771)):

$$\omega_0 = 2\pi f_0,\qquad k = m\,\omega_0^2,\qquad c = 2\zeta m\,\omega_0,\qquad \Omega = 2\pi f .$$

The right-hand side of the ODE is `accel()` ([L767–L769](../../public/simulations/driven-oscillator.html#L767-L769)):

$$\dot x = v,\qquad \dot v = a(t, x, v) = \frac{F_0\cos\Omega t - c\,v - k\,x}{m} .$$

Along the run the page also integrates the work of the driver and the heat of the damper
([L803–L804](../../public/simulations/driven-oscillator.html#L803-L804)) and stores the energy and the two powers at each
sample ([L791](../../public/simulations/driven-oscillator.html#L791)):

$$W_\text{in} = \int_0^T F v\,\mathrm dt,\quad W_\text{loss} = \int_0^T c\,v^2\,\mathrm dt,\quad E = \tfrac12 m v^2 + \tfrac12 k x^2,\quad P_\text{in} = F v,\quad P_\text{loss} = c v^2 .$$

The exact solution is used only to grade the numbers, never to draw them. `steady()`
([L716–L719](../../public/simulations/driven-oscillator.html#L716-L719)) gives the steady amplitude and phase lag, and
`exact()` ([L720–L725](../../public/simulations/driven-oscillator.html#L720-L725)) adds the transient that starts the block
from rest:

$$X = \frac{F_0/m}{\sqrt{(\omega_0^2-\Omega^2)^2 + (2\zeta\omega_0\Omega)^2}},\qquad \varphi = \operatorname{atan2}(2\zeta\omega_0\Omega,\ \omega_0^2-\Omega^2),$$

$$x_\text{exact}(t) = X\cos(\Omega t-\varphi) + e^{-\zeta\omega_0 t}\left(C_1\cos\omega_d t + C_2\sin\omega_d t\right),\quad C_1 = -X\cos\varphi,\quad C_2 = \frac{\zeta\omega_0 C_1 - X\Omega\sin\varphi}{\omega_d},\quad \omega_d = \omega_0\sqrt{1-\zeta^2}.$$

Further derived numbers ([L834–L843](../../public/simulations/driven-oscillator.html#L834-L843)): $\tau = 1/(\zeta\omega_0)$,
$Q = 1/(2\zeta)$, $f_r = f_0\sqrt{1-2\zeta^2}$ when $\zeta < 1/\sqrt2$ (else 0), $|G(i\Omega)| = X/F_0$, and the energy balance
$|E(T)-E(0)-(W_\text{in}-W_\text{loss})|/W_\text{in}$. The Bode plot evaluates $|G(i\Omega)| = 1/(m\sqrt{(\omega_0^2-\Omega^2)^2+(2\zeta\omega_0\Omega)^2})$
and $\varphi(\Omega)$ in degrees at 241 frequencies $f_j = 0.05\cdot 40^{j/240}$ Hz, from 0.05 to 2 Hz
([L863–L870](../../public/simulations/driven-oscillator.html#L863-L870)).

| Symbol | Meaning | Unit | In code |
|---|---|---|---|
| $m$ | mass, fixed at 1 | kg | `M` ([L539](../../public/simulations/driven-oscillator.html#L539)) |
| $x$, $v$ | displacement from rest, velocity | m, m/s | `x`, `v` |
| $f_0$, $\omega_0$ | natural frequency | Hz, rad/s | `f0.value`, `w0` |
| $\zeta$ | damping ratio (0 = no damping, 1 = no ringing) | 1 | `zeta.value` |
| $k$, $c$ | spring constant, damping coefficient | N/m, kg/s | `p.k`, `p.c` |
| $F_0$, $f$, $\Omega$ | force amplitude, drive frequency | N, Hz, rad/s | `p.F0`, `fd.value`, `p.W` |
| $E$, $P_\text{in}$, $P_\text{loss}$ | energy, driver power, damper power | J, W, W | `Es`, `Pin`, `Ploss` |
| $h$ | RK4 step | s | `H` = 0.001 |

With the defaults ($f_0 = 0.5$ Hz, $\zeta = 0.05$, $F_0 = 1$ N, $f = 0.45$ Hz) the store holds, measured in headless
Chromium: $k = 9.8696$ N/m, $c = 0.31416$ kg/s, $X = 0.48194$ m, $\varphi = 25.346°$, $\tau = 6.366$ s, $Q = 10$,
$f_r = 0.49875$ Hz, $W_\text{in} = 19.0317$ J, $W_\text{loss} = 17.9256$ J, largest RK4 error $5.26\times10^{-12}$ m and
energy balance $1.27\times10^{-12}$.

## How the code computes it

### Constants and state

One line fixes the run ([L539](../../public/simulations/driven-oscillator.html#L539)):
`M = 1` kg, `H = 0.001` s, `TEND = 60` s, `EVERY = 10`, and `NS = TEND / H / EVERY + 1`. In JavaScript `60 / 0.001` is
exactly 60 000, so `NS` is exactly 6 001 (checked in Node). The page keeps four pieces of its own state
([L546](../../public/simulations/driven-oscillator.html#L546)): `playT` (playback time, s), `iNow` (row on screen),
`fps` and `solved` (the slider values of the last solve, or `null`).

### 1 Solve: classical RK4 over the whole run

`solve()` ([L770–L850](../../public/simulations/driven-oscillator.html#L770-L850)) works on the state vector
$s = (x, v)$ with the slope $f(t, s) = (v,\ a(t, x, v))$. It starts from rest, $x = v = 0$ at $t = 0$
([L786](../../public/simulations/driven-oscillator.html#L786)). One step of size $h$ samples the slope four times: at the
start, twice at the middle and at the end ([L797–L800](../../public/simulations/driven-oscillator.html#L797-L800)):

$$k_1 = f(t, s),\quad k_2 = f(t+\tfrac h2, s+\tfrac h2 k_1),\quad k_3 = f(t+\tfrac h2, s+\tfrac h2 k_2),\quad k_4 = f(t+h, s+h k_3),$$
$$s(t+h) = s + \tfrac h6\,(k_1 + 2k_2 + 2k_3 + k_4) .$$

In the code the $x$-components of the slopes are the velocities `v, v2, v3, v4` and the $v$-components are the
accelerations `a1 … a4`; the update is [L806–L807](../../public/simulations/driven-oscillator.html#L806-L807). The two
work integrals are quadratures (their slopes do not feed back), carried with the same RK4 weights and the same stage
velocities, with the force evaluated at $t$, $t+h/2$ and $t+h$
([L802–L804](../../public/simulations/driven-oscillator.html#L802-L804)). Time is set from the step count,
`t = (step + 1) * H` ([L808](../../public/simulations/driven-oscillator.html#L808)), so it does not collect round-off by
repeated addition.

Why RK4 with $h = 1$ ms: the code does not state the reason. What can be measured is the margin. The fastest natural motion
allowed by the sliders is $\omega_0 = 2\pi\cdot1.5 = 9.42$ rad/s, so $\omega_0 h \le 0.0094$ rad per step, deep inside the
region where RK4 is stable and its error per step scales as $(\omega_0 h)^5$. With the defaults the largest difference to
the exact solution over the run is $5.26\times10^{-12}$ m and the energy balance holds to $1.27\times10^{-12}$ (measured).

### 2 Store: every tenth state

The loop runs `step = 0 … 60 000` ([L788](../../public/simulations/driven-oscillator.html#L788)). At the top of each pass,
before the step, every tenth state is written straight into the dataset arrays
([L789–L794](../../public/simulations/driven-oscillator.html#L789-L794)): `ts`, `xs`, `vs`, `Fs`, `Es`, `Pin`, `Ploss`. So
row $n$ holds the state at exactly $t_n = n\cdot 10h = n \cdot 10$ ms. After storing step 60 000 the loop stops without a
further step ([L795](../../public/simulations/driven-oscillator.html#L795)): 60 000 RK4 steps, 6 001 rows.

Two passes over the stored rows follow. The first ([L810–L818](../../public/simulations/driven-oscillator.html#L810-L818))
fills `xex` with the exact solution and finds the largest error `err`, the largest $|x|$ (`xmax`, which sets the drawing
scale) and the largest $|x|$ for $t_n \ge 50$ s (`Xm`, "Measured, last 10 s"). The second
([L819–L827](../../public/simulations/driven-oscillator.html#L819-L827)) fills `xqs` $= F_n/k$, the drive phase
`ph` $= \Omega t_n \bmod 2\pi$ and the chart half-height `ylim`. Then the arrays are marked changed
([L828](../../public/simulations/driven-oscillator.html#L828)) and every scalar is written
([L829–L844](../../public/simulations/driven-oscillator.html#L829-L844)).

The arrays come from `ds.alloc(name)` ([L784–L785](../../public/simulations/driven-oscillator.html#L784-L785)), which
allocates a new typed array only when the length changes ([dataset.js:67](../../public/scripts/dataset.js#L67)); a re-solve
overwrites the same `Float64Array`s in place. Memory, measured from the live store: 10 arrays × 6 001 × 8 B = 480 080 B for
the run, plus 3 × 241 × 8 B = 5 784 B for the Bode curves, 485 864 B in all. One solve took 6–17 ms in headless Chromium
(`solve_ms`, measured with `performance.now()` at [L770](../../public/simulations/driven-oscillator.html#L770) and
[L844](../../public/simulations/driven-oscillator.html#L844)).

Last, `solve()` records the settings it used in `solved` ([L845](../../public/simulations/driven-oscillator.html#L845)),
recomputes the Bode curves (`bode()`, [L859–L885](../../public/simulations/driven-oscillator.html#L859-L885)), rewrites the
readouts, sets `playT = 0` and starts the clock ([L846–L849](../../public/simulations/driven-oscillator.html#L846-L849)).

### When the run is solved again

Only twice: once at load ([L1680](../../public/simulations/driven-oscillator.html#L1680)) and whenever **Solve** is pressed
([L1388](../../public/simulations/driven-oscillator.html#L1388)). A slider only calls `markStale()`
([L699–L704](../../public/simulations/driven-oscillator.html#L699-L704),
[L887–L892](../../public/simulations/driven-oscillator.html#L887-L892)), which compares the four sliders with `solved`, sets
the `stale` flag and rewrites the status line in burgundy; the old run keeps playing, and its settings are named in the
status text ([L893–L903](../../public/simulations/driven-oscillator.html#L893-L903)).

### 3 Play: the frame loop, in order

`Sim.clock` ([sim.js:176–197](../../public/scripts/sim.js#L176-L197)) calls the page's tick on every
`requestAnimationFrame`, with $\Delta t$ capped at 0.05 s and $\Delta t = 0$ while paused. Each tick:

1. returns if nothing has been solved; updates the smoothed frame rate; advances `playT += speed · Δt`; at 60 s clamps and
   pauses; stores `fps` and `playing`; marks step "3 play" ([L1333–L1348](../../public/simulations/driven-oscillator.html#L1333-L1348));
2. `frame()` ([L1320–L1332](../../public/simulations/driven-oscillator.html#L1320-L1332)) picks the nearest stored row,
   $n = \operatorname{round}(t_\text{play}/10\,\text{ms})$ clamped to 0 … 6 000, writes `i_now`, `t_play` and the six
   `*_now` copies of row $n$ into the store, moves the **Stored run** slider and the caption time, then calls `draw()`;
3. `draw()` ([L1192–L1250](../../public/simulations/driven-oscillator.html#L1192-L1250)) sets the window width
   $T_w = \text{clamp}(4/f, 6, 20)$ s and its left edge $t_0 = \text{clamp}(t_n - 0.7T_w, 0, 60 - T_w)$, gets the layout
   from `geom()`, turns $x_n$ into the block position `bx = eqX + xs[i] * sc` and $F_n$ into the arrow length, stores these
   pixel values, clears the canvas and draws `drawMechanism`, `drawWindow` and `drawOverview` in that order.

Nothing in this chain integrates; the only arithmetic turns metres, seconds and newtons into pixels. Because the clock calls
the tick every animation frame even while paused (with $\Delta t = 0$), the figure is redrawn at the display rate in both
states; one `frame()` took about 1.5 ms (measured over 200 seek events at a 1 440 px wide window).

### Precomputation and caching

- The Bode canvas is not redrawn per frame: only after a solve ([L884](../../public/simulations/driven-oscillator.html#L884)),
  on resize ([L1683](../../public/simulations/driven-oscillator.html#L1683)) and when fonts are ready
  ([L1684](../../public/simulations/driven-oscillator.html#L1684)).
- `geom()` ([L919–L946](../../public/simulations/driven-oscillator.html#L919-L946)) is recomputed on every call; it reads
  `xmax`, `win_t0`, `win_T` and `ylim` from the store, so `draw()` must store the window before calling it
  ([L1195–L1196](../../public/simulations/driven-oscillator.html#L1195-L1196)).
- For the data panel's Check of $W_\text{in}$ and $W_\text{loss}$, `fullReplay()` reruns the whole 60 s once and caches the
  result under a key made of the four settings ([L1427–L1433](../../public/simulations/driven-oscillator.html#L1427-L1433)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `steady(w0, z, W, F)` | [716–719](../../public/simulations/driven-oscillator.html#L716-L719) | Exact steady amplitude $X$ and phase lag $\varphi$, equation (4) of the note. |
| `exact(t, w0, z, W, st)` | [720–725](../../public/simulations/driven-oscillator.html#L720-L725) | Exact $x(t)$ from rest, equation (5); used only to measure the RK4 error. |
| `control()` | [728–731](../../public/simulations/driven-oscillator.html#L728-L731) | The controller force $u = K_p(r-x) + K_i z - K_d v$, equation (12). |
| `closed()` | [732–736](../../public/simulations/driven-oscillator.html#L732-L736) | Closed-loop steady amplitude and phase, (16). |
| `equilibrium()` | [737](../../public/simulations/driven-oscillator.html#L737) | Equilibrium (14). |
| `matmul()` | [738](../../public/simulations/driven-oscillator.html#L738) | Matrix product (for `expm`). |
| `expm()` | [739–749](../../public/simulations/driven-oscillator.html#L739-L749) | Matrix exponential by scaling and squaring. |
| `exactClosed()` | [750–764](../../public/simulations/driven-oscillator.html#L750-L764) | Exact closed-loop solution sample by sample; grades RK4 when the controller is on. |
| `accel(t, x, v, u, p)` | [767–769](../../public/simulations/driven-oscillator.html#L767-L769) | Right-hand side: $(F_0\cos\Omega t + u - cv - kx)/m$. |
| `solve()` | [775–850](../../public/simulations/driven-oscillator.html#L775-L850) | Solve and store the whole run (see above). |
| `setSpan()` | [852–856](../../public/simulations/driven-oscillator.html#L852-L856) | Sets the held drawing span, `ylim`, `held`. |
| `fitScale()` | [857](../../public/simulations/driven-oscillator.html#L857) | **Fit scale**: span ← need. |
| `bode()` | [859–885](../../public/simulations/driven-oscillator.html#L859-L885) | Fills `fb`, `Gmag`, `Gphase` (241 points) and redraws the Bode plot. |
| `markStale()` | [887–892](../../public/simulations/driven-oscillator.html#L887-L892) | Sets `stale` when a slider differs from the last solve. |
| `status()` | [893–903](../../public/simulations/driven-oscillator.html#L893-L903) | Writes the status line and the "1 solve / 2 store" marks. |
| `readouts()` | [904–915](../../public/simulations/driven-oscillator.html#L904-L915) | Writes the six readouts and the Bode caption $f_r$. |
| `geom()` | [919–946](../../public/simulations/driven-oscillator.html#L919-L946) | Layout from canvas size and store: mechanism, window chart, overview strip, dial; mapping functions `wx`, `wy`, `ox`, `oy`, `inWin`. |
| `arrow(c, …)` | [947–955](../../public/simulations/driven-oscillator.html#L947-L955) | Draws a straight arrow with a filled head. |
| `spring(c, …)` | [956–962](../../public/simulations/driven-oscillator.html#L956-L962) | Draws a zigzag spring. |
| `label(c, sym, value, …)` | [963–973](../../public/simulations/driven-oscillator.html#L963-L973) | A symbol in Latin Modern via `Sim.tex`, then its value in IBM Plex Mono. |
| `drawMechanism(c, g, i, bx, cap, gx)` | [974–1031](../../public/simulations/driven-oscillator.html#L974-L1031) | Wall, floor, rest line, spring, damper (oil shaded by $P_\text{loss}$), outlined previous block, block on wheels, then `drawCoil`, `drawForces`, `drawEnergy`, `drawController`; ruler, target dot, equilibrium line. |
| `drawCoil()` | [1032–1061](../../public/simulations/driven-oscillator.html#L1032-L1061) | Magnet, coil tube and winding, current dots and crosses, current source and leads. |
| `drawForces()` | [1063–1079](../../public/simulations/driven-oscillator.html#L1063-L1079) | The three force arrows over the block. |
| `drawController()` | [1096–1114](../../public/simulations/driven-oscillator.html#L1096-L1114) | The controller box: value read, P, I, D, u bars, command line. |
| `drawEnergy()` | [1115–1126](../../public/simulations/driven-oscillator.html#L1115-L1126) | The three energy bars. |
| `drawWindow(c, g, i)` | [1127–1170](../../public/simulations/driven-oscillator.html#L1127-L1170) | Window chart: ticks, $\pm X$, $F/k$, $x$ faint ahead and dark behind, cursor, key. |
| `drawOverview(c, g, i)` | [1171–1191](../../public/simulations/driven-oscillator.html#L1171-L1191) | Strip of the whole run with the window band shaded. |
| `draw()` | [1192–1210](../../public/simulations/driven-oscillator.html#L1192-L1210) | One frame of the main canvas. |
| `bodeGeom()` | [1252–1265](../../public/simulations/driven-oscillator.html#L1252-L1265) | Bode layout: two panels side by side (stacked below 560 px), log $f$ axis 0.05–2 Hz, three decades of $\lvert G\rvert$, 0–180°. |
| `drawBode()` | [1266–1301](../../public/simulations/driven-oscillator.html#L1266-L1301) | Draws both panels, the $f_0$ line, the curves, the dot at the exact value and the ring at the measured one. |
| `Sim.live()` | [1304–1318](../../public/simulations/driven-oscillator.html#L1304-L1318) | Formatted store values for the walkthrough's "Now" column. |
| `frame()` | [1320–1332](../../public/simulations/driven-oscillator.html#L1320-L1332) | Picks the stored row for `playT`, copies it to the `*_now` scalars, draws. |
| `chartPos(n)`, `chartPosQ(n)` | [1397–1400](../../public/simulations/driven-oscillator.html#L1397-L1400) | Screen point of $x_n$ (or $F_n/k$) on the window chart, else on the overview strip. |
| `chartPosQ()` | [1401–1404](../../public/simulations/driven-oscillator.html#L1401-L1404) |  |
| `loopParams()` | [1405](../../public/simulations/driven-oscillator.html#L1405) | The eight settings of the last solve, for the checks. |
| `fullReplay()` | [1428–1433](../../public/simulations/driven-oscillator.html#L1428-L1433) | Cached `rk4Replay(6000)`. |
| `sliderCheck`, `at`, `neutralInk`, `readBack` | [1434](../../public/simulations/driven-oscillator.html#L1434) | Small helpers for the data panel's Check (slider value, row on screen, dark-ink test, pixel read-back). |
| `at()` | [1435–1437](../../public/simulations/driven-oscillator.html#L1435-L1437) |  |
| `neutralInk()` | [1438](../../public/simulations/driven-oscillator.html#L1438) |  |
| `readBack()` | [1439–1442](../../public/simulations/driven-oscillator.html#L1439-L1442) |  |
| `prevParams()` | [1443–1446](../../public/simulations/driven-oscillator.html#L1443-L1446) | Plant and loop of the previous run. |
| `mutedInk()` | [1447](../../public/simulations/driven-oscillator.html#L1447) | Pixel test: grey ink. |
| `chartPosPrev()` | [1448–1451](../../public/simulations/driven-oscillator.html#L1448-L1451) | Where sample n of the previous run is drawn. |
| `roseInk()` | [1452](../../public/simulations/driven-oscillator.html#L1452) | Pixel test: rose. |
| `ctrlBar()` | [1453](../../public/simulations/driven-oscillator.html#L1453) | Where a controller bar ends. |
| `tanInk()` | [1454](../../public/simulations/driven-oscillator.html#L1454) | Pixel test: brown. |
| `arrowPoint()` | [1455](../../public/simulations/driven-oscillator.html#L1455) | Mid-point of a force arrow. |
| `barPoint()` | [1456](../../public/simulations/driven-oscillator.html#L1456) | End of an energy bar. |
| `arrowBack()` | [1457–1461](../../public/simulations/driven-oscillator.html#L1457-L1461) | Read-back of a force arrow. |
| `blockPixel()` | [1462–1466](../../public/simulations/driven-oscillator.html#L1462-L1466) | Reads back a pixel inside the burgundy block. |
| `Sim.data` (object) | [1467–1678](../../public/simulations/driven-oscillator.html#L1467-L1678) | The data-panel contract: groups, colours, `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `about`. |
| `ctrlHead()` | [1086–1090](../../public/simulations/driven-oscillator.html#L1086-L1090) | Header of the controller box: one word on narrow screens. |
| `ctrlWidth()` | [1091–1095](../../public/simulations/driven-oscillator.html#L1091-L1095) | Width of the controller box, measured from its header. |
| `sliderParams()` | [770–774](../../public/simulations/driven-oscillator.html#L770-L774) | The plant and loop parameters from the sliders (used by `solve` and the hand). |
| `pointerX()` | [1351](../../public/simulations/driven-oscillator.html#L1351) | Pointer position in css px of the main canvas. |
| `holdState()` | [1352–1363](../../public/simulations/driven-oscillator.html#L1352-L1363) | The state while your hand holds the block: controller force, hand force, status line; then `draw()`. |
| `release()` | [1378–1383](../../public/simulations/driven-oscillator.html#L1378-L1383) | Ends a hold and calls `solve({x, v, z})`. |
| `capArrow()` | [1062](../../public/simulations/driven-oscillator.html#L1062) | Caps a force arrow at 1.6 A<sub>px</sub> (drawn with a break mark). |
| `ctrlScale()` | [1080–1085](../../public/simulations/driven-oscillator.html#L1080-L1085) | Scale of the controller bars: the run’s, or while held the largest force now. |
| `forceGeom()` | [1214–1218](../../public/simulations/driven-oscillator.html#L1214-L1218) | Layout of the force-profile canvas. |
| `forceCurves()` | [1219–1224](../../public/simulations/driven-oscillator.html#L1219-L1224) | Which force series the profile draws (controller parts only when on). |
| `drawForceProfile()` | [1225–1250](../../public/simulations/driven-oscillator.html#L1225-L1250) | Draws the force profile for the present row. |
| `setView()` | [1391](../../public/simulations/driven-oscillator.html#L1391) | Switches the frequency response between the linear view and the Bode view. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Solve | `solve` | button | Calls `solve()` ([L1388](../../public/simulations/driven-oscillator.html#L1388)). |
| Pause / Play | `play` | button | Toggles the clock via `Sim.playButton` ([L1387](../../public/simulations/driven-oscillator.html#L1387), [sim.js:199](../../public/scripts/sim.js#L199)). |
| From t = 0 | `restart` | button | `playT = 0` and play ([L1389](../../public/simulations/driven-oscillator.html#L1389)). |
| Stored run | `seek` | 0–6000, step 1, default 0 ([L100](../../public/simulations/driven-oscillator.html#L100)) | Sets `playT = n · 10 ms` and draws ([L713](../../public/simulations/driven-oscillator.html#L713)); follows the playback ([L1329](../../public/simulations/driven-oscillator.html#L1329)). |
| Playback speed | `speed` | 0.25–4, step 0.25, default 1 ([L104](../../public/simulations/driven-oscillator.html#L104)) | Multiplies $\Delta t$ ([L1343](../../public/simulations/driven-oscillator.html#L1343)). Does not mark the run stale. |
| Spring constant $k$ | `kspring` | 1.5–90 N/m, step 0.01, default 9.87 | Sets $k$; $f_0 = \sqrt{k/m}/2\pi$ is shown beside it and used by the rest of the code; marks stale. |
| Damping ratio $\zeta$ | `zeta` | 0.01–0.9, step 0.01, default 0.05 ([L116](../../public/simulations/driven-oscillator.html#L116)) | $c$ at the next solve; marks stale. The maximum 0.9 keeps $\omega_d$ real in `exact()`. |
| Force amplitude $F_0$ | `F0` | 0–5 N, step 0.1, default 1 ([L124](../../public/simulations/driven-oscillator.html#L124)) | `p.F0`; marks stale. At 0 the drive arrow is hidden and `Gm_drive` is NaN ([L841](../../public/simulations/driven-oscillator.html#L841)). |
| Drive frequency $f$ | `fd` | 0.05–1.5 Hz, step 0.01, default 0.45 ([L128](../../public/simulations/driven-oscillator.html#L128)) | $\Omega$ at the next solve; marks stale. |
| Fit scale | `fit` | button | `fitScale()`: span ← need, redraw. |
| Linear / Bode, log | `view-amp`, `view-bode` | buttons, default Linear | `setView()`: amplitude function and phase difference on linear axes, or the Bode plot. |
| The block itself | canvas `osc` | press and drag | Hold: the controller acts on your hand's position; release: `solve({x, v, z})` from that state. |
| Off / P / PD / PID | `[data-gains]` | buttons | Set $(K_p, K_i, K_d)$ to (0,0,0), (20,0,0), (20,0,4), (20,10,4) and mark stale. |
| Target position $r$ | `r` | −0.5–0.5 m, step 0.01, default 0.3 | `p.r`; marks stale. |
| Proportional gain $K_p$ | `Kp` | 0–60 N/m, step 0.5, default 0 | `p.Kp`; marks stale. |
| Integral gain $K_i$ | `Ki` | 0–60 N/(m·s), step 0.5, default 0 | `p.Ki`; marks stale. |
| Derivative gain $K_d$ | `Kd` | 0–12 kg/s, step 0.1, default 0 | `p.Kd`; marks stale. |
| Read values | added by datalog.js | switch, off | Appended to the first figure caption ([datalog.js:588–590](../../public/scripts/datalog.js#L588-L590)); see [datalog.md](../scripts/datalog.md). |

## What the page writes into the data store

The store is made at [L549](../../public/simulations/driven-oscillator.html#L549):
`Sim.dataset({ title: 'Driven oscillator', attrs: { figure: 9, page, equation, start } })`. It has two dimensions,
`n` = 6 001 stored rows ([L590](../../public/simulations/driven-oscillator.html#L590)) and `b` = 241 Bode frequencies
([L684](../../public/simulations/driven-oscillator.html#L684)), and 127 variables: 100 scalars and 27 `Float64Array`s, all
declared at [L550–L689](../../public/simulations/driven-oscillator.html#L550-L689) (counted in the live store). The shared
store itself is described in [dataset.md](../scripts/dataset.md). Each variable carries `symbol`, `units`, `long_name`,
`computed_in`, often `formula`, and `digits`. Listed by the panel groups of
[L1470–L1481](../../public/simulations/driven-oscillator.html#L1470-L1481):

| Group | Variables | Written at |
|---|---|---|
| Parameters | `m`, `f0`, `zeta`, `F0`, `fd`, `r`, `Kp`, `Ki`, `Kd`, `ctrl_on` | see the function map (`solve()`, `frame()`, `draw()`, `bode()`, `setSpan()`) |
| Closed loop | `x_eq`, `F_eq`, `zeta_cl`, `margin`, `stable`, `t_blow`, `H_drive` | see the function map (`solve()`, `frame()`, `draw()`, `bode()`, `setSpan()`) |
| Derived physics | `omega0`, `k`, `c`, `Omega`, `tau`, `Q`, `BL`, `I0`, `xst`, `X`, `phi`, `phi_deg`, `G_drive`, `fr` | see the function map (`solve()`, `frame()`, `draw()`, `bode()`, `setSpan()`) |
| Solver | `h`, `steps`, `solve_ms`, `err_max`, `Xm`, `Gm_drive`, `Win`, `Wloss`, `balance`, `stale` | see the function map (`solve()`, `frame()`, `draw()`, `bode()`, `setSpan()`) |
| Stored run | `ts`, `xs`, `vs`, `zs`, `Fpush`, `us`, `uP`, `uI`, `uD`, `Fs`, `Is`, `Fdamp`, `Fspr`, `xqs`, `ph`, `Es`, `Pin`, `Ploss`, `Wc`, `Qc`, `xex` | see the function map (`solve()`, `frame()`, `draw()`, `bode()`, `setSpan()`) |
| Previous run | `has_prev`, `prev_f0`, `prev_zeta`, `prev_F0`, `prev_fd`, `prev_r`, `prev_Kp`, `prev_Ki`, `prev_Kd`, `xs_prev`, `xmax_prev`, `ratio` | see the function map (`solve()`, `frame()`, `draw()`, `bode()`, `setSpan()`) |
| Playback | `i_now`, `t_play`, `x_now`, `v_now`, `u_now`, `uP_now`, `uI_now`, `uD_now`, `F_now`, `I_now`, `Fc_now`, `Fk_now`, `ph_now`, `E_now`, `Pin_now`, `Ploss_now`, `Wc_now`, `Qc_now` | see the function map (`solve()`, `frame()`, `draw()`, `bode()`, `setSpan()`) |
| Bode plot | `fb`, `Gmag`, `Gphase`, `Hmag`, `Hphase` | see the function map (`solve()`, `frame()`, `draw()`, `bode()`, `setSpan()`) |
| Drawing | `xmax`, `need`, `span_before`, `fitted`, `span`, `held`, `ylim`, `amp_px`, `px_per_m`, `px_per_N`, `eq_px`, `block_px`, `block_y`, `ghost_shown`, `ghost_px`, `coil_px`, `Fd_px`, `Fc_px`, `Fk_px`, `r_px`, `xeq_px`, `Wscale`, `uscale`, `Ploss_max`, `win_t0`, `win_T`, `box_w`, `box_h`, `fps`, `playing` | see the function map (`solve()`, `frame()`, `draw()`, `bode()`, `setSpan()`) |

The `*_now` scalars are copies of row `i_now`, so a recorded round has scalar columns to follow.
`Sim.data.colour` shades the `xs` and `Fs` table cells with `Sim.colourMap`
([L1482](../../public/simulations/driven-oscillator.html#L1482), defined in
[datalog.js:71](../../public/scripts/datalog.js#L71)); this is presentation only.

**One round** (`Sim.data.round`, [L1671–L1673](../../public/simulations/driven-oscillator.html#L1671-L1673)) is one drive
period, $1/f$ seconds of the stored run, timed by `t_play`. Its columns are `x_now`, `v_now`, `u_now`, `F_now`, `Fc_now`, `Fk_now`, `E_now`, `Pin_now`;
the default point is the block. Recording is refused when fewer than $1/f$ seconds of the run remain ("press From t = 0").
The panel samples every frame of the round, at most 600 samples ([datalog.js:744](../../public/scripts/datalog.js#L744)).

**`Sim.live()`** ([L1304–L1318](../../public/simulations/driven-oscillator.html#L1304-L1318)) returns formatted strings read from
the store, for the keys the walkthrough uses: `k`, `c`, `W`, `w0`, `h`, `steps`, `n`, `t`, `x`, `v`, `F`, `E`, `X`, `phi`,
`err`, `Win`, `Wloss`, `bal`, `bx`, `sc`, `I0`, `I`, `BL`, `Fc`, `Fk`, `fN`, `span`, `Wc`, `Qc`, `u`, `r`, `Kp`, `Ki`, `Kd`, `z`, `xeq`. The walkthrough polls it every 200 ms
([sim.js:326](../../public/scripts/sim.js#L326)).

**Check and read-back.** `Sim.data.check` ([L1518–L1617](../../public/simulations/driven-oscillator.html#L1518-L1617))
recomputes every stored value from its stored inputs; for the ODE solution (`xs`, `vs`) and the run integrals (`Win`,
`Wloss`) it reruns the same RK4 from $t = 0$ (`rk4Replay`, up to 60 000 steps). `Sim.data.drawn`
([L1618–L1670](../../public/simulations/driven-oscillator.html#L1618-L1670)) reads pixels back: the burgundy block, the
three force arrows (or their absence below 2 px), the energy bars, the controller's $u$ bar, the target dot, the equilibrium line, the previous run's dotted curve, $x_n$ and $F_n/k$ on the charts, and the Bode curves and dots (plant dashed grey when the loop is on).
`probe` ([L1483–L1492](../../public/simulations/driven-oscillator.html#L1483-L1492)) pins the block when the click is within
40 px across and 34 px up or down of its centre, otherwise the nearest stored sample within 16 px (outside the window chart
only every fifth sample is tried). How the panel uses these hooks is in [datalog.md](../scripts/datalog.md).

## Page structure

**Head** ([L3–L26](../../public/simulations/driven-oscillator.html#L3-L26)): title "Driven Oscillator · Numa Koudsie",
description, the security policy and referrer rule ([build-and-deploy.md](../build-and-deploy.md#security)), then the stylesheets `../styles/sim.css`, `../styles/data.css`,
`../styles/fold.css` ([L11–L13](../../public/simulations/driven-oscillator.html#L11-L13)), an inline SVG favicon, and a
small inline style for the solve box (`.solve`, `.solve__steps`, `.solve__status`, `.seek`,
[L15–L25](../../public/simulations/driven-oscillator.html#L15-L25)). Styles are described in [styles.md](../styles.md).

**Body**, in order:
- `header.sim-top`: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`,
  87 × 48) and the back link "← All simulations" ([L29](../../public/simulations/driven-oscillator.html#L29)), then the hand-written Fig. 1–10 links, Fig. 9
  marked `aria-current` ([L28–L43](../../public/simulations/driven-oscillator.html#L28-L43));
- `.sim__head`: "Fig. 9 · control systems · forced oscillations", the `h1` and the lede
  ([L47–L51](../../public/simulations/driven-oscillator.html#L47-L51));
- `.sim__grid`: the main figure `#stage` with `canvas#osc` and a caption holding the equation and `#cap-t`
  ([L55–L63](../../public/simulations/driven-oscillator.html#L55-L63)); the Bode figure `#stage-bode` with `canvas#bode` and
  `#cap-res` ([L64–L80](../../public/simulations/driven-oscillator.html#L64-L80)); the control panel `aside.panel` with the
  solve box, the sliders, six readouts and a legend ([L83–L177](../../public/simulations/driven-oscillator.html#L83-L177)).
  The **Read values** switch is added to the first caption by datalog.js;
- `article.paper#paper`, the lecture note ([L180–L522](../../public/simulations/driven-oscillator.html#L180-L522)):
  abstract; ten sections `.psec` — 01 A push from outside, 02 The model, 03 The exact solution ★ (3.1 The steady state,
  3.2 The transient), 04 Resonance and phase, 05 The control engineer's view ★, 06 The start: beats and decay, 07 Where the
  energy goes, 08 Solve first, then play, 09 On screen, 10 What the model leaves out (10.1 Further reading, four items, each
  with a link). Nine numbered equations, `\tag{1}`–`\tag{8}` and `\tag{6a}` (the completed square that locates the
  resonance peak, [L361](../../public/simulations/driven-oscillator.html#L361)). Four figures with five inline SVGs: Figure 1 the plant sketch
  ([L209–L238](../../public/simulations/driven-oscillator.html#L209-L238)), Figure 2 amplitude and phase against $f/f_0$ for
  four damping ratios (two SVGs, [L269–L357](../../public/simulations/driven-oscillator.html#L269-L357)), Figure 3 the block
  diagram ([L376–L394](../../public/simulations/driven-oscillator.html#L376-L394)), Figure 4 the default run
  ([L400–L448](../../public/simulations/driven-oscillator.html#L400-L448)). Two exercise boxes, 4.1 and 6.1;
- `section#walk` with `data-walk="driven"` ([L524](../../public/simulations/driven-oscillator.html#L524)), filled by
  `sim.js` from `walk/driven.js` ([sim.js:402–411](../../public/scripts/sim.js#L402-L411)); see [walk.md](../scripts/walk.md);
- footer; then the scripts in load order: `fold.js`, `sim.js`, `dataset.js`, the page's inline script, `datalog.js`
  ([L532–L1687](../../public/simulations/driven-oscillator.html#L532-L1687)). Folds are described in
  [fold.md](../scripts/fold.md), the shared helpers in [sim.md](../scripts/sim.md).

The walkthrough's seven steps quote these page lines: step 1 [L771](../../public/simulations/driven-oscillator.html#L771);
step 2 [L767–L769](../../public/simulations/driven-oscillator.html#L767-L769); step 3
[L797–L800](../../public/simulations/driven-oscillator.html#L797-L800) and
[L806–L807](../../public/simulations/driven-oscillator.html#L806-L807); step 4
[L789–L794](../../public/simulations/driven-oscillator.html#L789-L794); step 5
[L803–L804](../../public/simulations/driven-oscillator.html#L803-L804) and
[L843](../../public/simulations/driven-oscillator.html#L843); step 6
[L717–L718](../../public/simulations/driven-oscillator.html#L717-L718) and
[L815](../../public/simulations/driven-oscillator.html#L815); step 7
[L1343](../../public/simulations/driven-oscillator.html#L1343), [L1321](../../public/simulations/driven-oscillator.html#L1321),
[L1197](../../public/simulations/driven-oscillator.html#L1197). All seven excerpts match the page text at present.

## Where the drawing and the store differ

The page states the differences in `Sim.data.about` ([L1675](../../public/simulations/driven-oscillator.html#L1675)), which
the data panel prints. In detail:

- **Nearest row, no interpolation.** `t_play` runs continuously, but the picture shows row
  $\operatorname{round}(t_\text{play}/10\,\text{ms})$ ([L1321](../../public/simulations/driven-oscillator.html#L1321)). The
  caption shows the row's time `ts[i]`, not `t_play` ([L1330](../../public/simulations/driven-oscillator.html#L1330)).
- **Overview strip thinned.** The strip of the whole run draws every `stride`-th row,
  `stride = max(1, floor(NS / (2 × strip width)))` ([L1173](../../public/simulations/driven-oscillator.html#L1173)): every 4th
  row at a 770 px canvas, every 10th at 356 px. The window chart draws every row between its edges
  ([L1129](../../public/simulations/driven-oscillator.html#L1129)).
- **Drawing scale is held between runs.** `span` (m) is the half-range the screen shows: it starts at the first run's
  `need = max(xmax, F0/k, |r|)`, grows only when a later run needs more, and **Fit scale** sets it to the present run
  (`setSpan()`). So `px_per_m = amp / span` is the same for consecutive runs unless one overflows, and a run with more
  damping really swings less on screen next to the dotted previous run. The force arrows use `px_per_N = 2 px_per_m / k`.
- **Previous run.** `xs_prev` is a copy of `xs` taken at the start of `solve()`, with the previous settings in `prev_*`;
  its Check reruns RK4 with those settings. The outlined block is left out at instants when it lies outside the span.
- **Your hand.** `pointerdown` on the block (within half a block width + 10 px) starts a hold: the clock keeps ticking but
  `holdState()` replaces the playback; the hand's position is clamped to ±`span`, its speed is smoothed over about 50 ms,
  the controller's memory `z` grows by $(r - x)\,\Delta t$ in wall-clock time, and `hand_now` $= kx + c\dot x - F$. Nothing
  is stored while held. `pointerup` calls `solve({x, v, z})`; the start is stored as `x0`, `v0`, `z0`, and every check
  (`rk4Replay`, `exact`, `exactClosed`, the previous run's replay) starts from it. The canvas has `touch-action: pan-y`, so
  vertical swipes still scroll on phones.
- **Spring constant.** The slider `kspring` (1.5–90 N/m, step 0.01, default 9.87) sets $k$; the page keeps an object `f0`
  whose `value` is $\sqrt{k/m}/2\pi$, so the rest of the code is unchanged.
- **Controller.** The RK4 state is $(x, v, z)$ with $z = \int (r-x)\,dt$; `control()` is evaluated at all four stages. The
  exact solution that grades RK4 is `exactClosed()` when any gain is above zero: particular solution (16) plus the free
  motion propagated with the matrix exponential of the loop's state matrix (`expm`, scaling and squaring). An unstable loop
  is solved until $|x| > 1000$ m (`t_blow`); the rest of the run holds that state.
- **Old item, superseded:** *Drawing scale changes with the run.* The block travels at most `amp = 0.11 × W0` pixels either side of rest, where
  `W0` is the width between wall and right margin, so `px_per_m = amp / xmax` differs from run to run
  ([L929](../../public/simulations/driven-oscillator.html#L929), [L931](../../public/simulations/driven-oscillator.html#L931)).
  The ruler under the floor shows $\pm$`xmax` in metres ([L1022](../../public/simulations/driven-oscillator.html#L1022)).
- **Force arrow.** Its length is $F_n/F_0 \cdot L_F$ with $L_F = \min(88, 0.12\,w)$ px; arrows shorter than 2 px are not
  drawn ([L1014](../../public/simulations/driven-oscillator.html#L1014)).
- **Dial.** The arm points at the stored $\Omega t_n \bmod 2\pi$ ([L1027](../../public/simulations/driven-oscillator.html#L1027)).
- **Bode plot.** The dot sits at the exact $|G(i\Omega)|$ and $\varphi$; the ring is the amplitude measured from the last
  10 s of the stored run, per newton ([L1296–L1298](../../public/simulations/driven-oscillator.html#L1296-L1298)). With the
  defaults they differ by 0.03 % (0.48194 against 0.48209 m/N), the remains of the transient.
- **Rounding.** Canvas labels and readouts round (for example $F$ to 2 decimals, $x$ to 3); the store keeps full doubles.

## How to change it safely

- **Run length, step and storage stride.** `TEND`, `H` and `EVERY` ([L539](../../public/simulations/driven-oscillator.html#L539))
  determine `NS`. Keep `TEND / H` and `TEND / H / EVERY` whole numbers, because `step === TEND / H` and `step % EVERY` decide
  the last row ([L788–L795](../../public/simulations/driven-oscillator.html#L788-L795)). These places repeat the numbers by
  hand and must change with them: the seek slider `max="6000"` ([L100](../../public/simulations/driven-oscillator.html#L100));
  the `formula` texts "n · 10 h", "t_n ≥ 50 s", "round(t_play / 10h)" ([L591](../../public/simulations/driven-oscillator.html#L591),
  [L618](../../public/simulations/driven-oscillator.html#L618), [L622](../../public/simulations/driven-oscillator.html#L622));
  the group note "every 10 ms of the 60 s" ([L1476](../../public/simulations/driven-oscillator.html#L1476)); the check text
  "at most 6000" ([L1599](../../public/simulations/driven-oscillator.html#L1599)); the 10 s tick step of the overview
  ([L1189](../../public/simulations/driven-oscillator.html#L1189)); the walkthrough's "step / 10", "60 000 steps" and
  "6 001 rows" ([driven.js:57–58](../../public/scripts/walk/driven.js#L57-L58)); the lecture note section 8
  ([L466–L468](../../public/simulations/driven-oscillator.html#L466-L468)) and `about`.
- **The integrator exists twice.** `solve()` ([L797–L808](../../public/simulations/driven-oscillator.html#L797-L808)) and
  `rk4Replay()` ([L1412–L1423](../../public/simulations/driven-oscillator.html#L1412-L1423)) must stay identical, line for line,
  or the data panel's Check of `xs`, `vs`, `Win` and `Wloss` will no longer agree with the store.
- **Walkthrough excerpts.** The seven excerpts listed under Page structure are quoted verbatim in `walk/driven.js`. If one
  of those page lines changes, change the excerpt in the same edit. Insert new code after a quoted line, never inside a
  quoted group (AGENTS.md).
- **Taps stay where values are computed.** Write a new number into the store at the line that computes it, declare it with
  `ds.var` next to its relatives, add it to a group in `Sim.data.groups`, and give it a `check` (and a `drawn` if it is on
  screen). Do not compute numbers inside `draw*()` beyond the metre-to-pixel conversion.
- **Lecture-note numbers.** Sections 2–9 quote values for the default sliders ([L112–L128](../../public/simulations/driven-oscillator.html#L112-L128)),
  and Figures 2 and 4 are static SVGs computed from the page's formulas. Changing a default or the physics means
  recomputing them.
- **Damping limit.** `exact()` divides by $\omega_d = \omega_0\sqrt{1-\zeta^2}$; the slider stops at 0.9. Allowing
  $\zeta \ge 1$ needs a different exact solution (section 10 says so, [L508](../../public/simulations/driven-oscillator.html#L508)).
- **Frequency range.** The Bode axis covers 0.05–2 Hz ([L864](../../public/simulations/driven-oscillator.html#L864),
  [L1260](../../public/simulations/driven-oscillator.html#L1260)); raising the $f_0$ or $f$ slider beyond 2 Hz would put the
  marks outside it.
- **Re-test** in a browser at a wide and a phone-width window: no console error; status line after load; readouts with the
  defaults ($X$ = 0.482 m, error about $5\times10^{-12}$ m, balance about $10^{-12}$); move a slider and see the stale
  status; Solve; drag **Stored run**; open the Data panel, Check `xs` at a row, `Win`, `balance`, and a `drawn` value; switch
  on **Read values** and pin the block; record one round.

## Notes for maintainers

1. Fixed on 2026-10-15: both log axes read 0.1, 0.32, 1, 3.2, 10; their endpoints agree with gains 1.01005 and 0.0101005 (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
2. Fixed on 2026-10-15: both phase-lag references round the stored 25.34617594° to 25.3° (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
3. Fixed on 2026-10-15: the note gives the actual geometry and measured desktop/phone fractions (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
4. Fixed on 2026-10-15: the readout and walkthrough read stored phi_deg (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
5. Fixed on 2026-10-15: the unread frame counter and overwritten sw initializer were removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
6. **Redraw while paused.** The clock calls the tick on every animation frame with $\Delta t = 0$ while paused
   ([sim.js:178–185](../../public/scripts/sim.js#L178-L185)), and the tick always calls `frame()`
   ([L1347](../../public/simulations/driven-oscillator.html#L1347)), so a paused page still redraws about 60 times a second
   (about 1.5 ms per frame measured) and rewrites `#cap-t` each time ([L1330](../../public/simulations/driven-oscillator.html#L1330)).
7. Fixed on 2026-10-15: the note gives the measured default solve time of 9.5–12.4 ms and states that timing depends on the machine (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
8. **AGENTS.md** said the load order dataset.js → page → datalog.js holds for "all eight figures"; this page (Fig. 9)
   follows it too. Corrected to "all ten figures" on 14 October 2026.


## Teaching revision · 15 October 2026

The note separates undamped natural frequency from damped ringing, interprets the complex denominator as spring, inertia and quadrature damping, and uses the damped ringing frequency for the approximate default beat time. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16: the paragraph reading the complex denominator had been placed between "(2) turns into algebra:" and equation (3); it now follows (3) and ends "gives the form in (3)" ([L257](../../public/simulations/driven-oscillator.html#L257)). See the [audit of the revision](../research-theory-audit.md).

Fixed on 2026-10-16 (second repairs): the Millennium Bridge is back as the counter-example to a prescribed force (the walkers' steps fed back on the sway); the beat-time sentence is one sentence again ([L208](../../public/simulations/driven-oscillator.html#L208)). See the [audit of the revision](../research-theory-audit.md).

## Teaching revision · 20 October 2026

Judged section by section against [notes/STANDARD.md](../../notes/STANDARD.md); the verdicts and measurements are in
[notes/fig09/plan.md](../../notes/fig09/plan.md). Sections 1, 2 and 8, the text of section 6 and the limits in section 10 were left as they were. Filled in: the step from (3)
to (4), with `atan2` named and the real part justified ([L258](../../public/simulations/driven-oscillator.html#L258)); the
roots $s = -\zeta\omega_0 \pm i\omega_0\sqrt{1-\zeta^2}$ of the free equation, which give $\tau$, $\omega_d$ and the meaning of
$\zeta = 1$, and the two starting conditions behind $C_1$, $C_2$ ([L261](../../public/simulations/driven-oscillator.html#L261));
the completed square (6a) that places the peak at $\Omega_r = \omega_0\sqrt{1-2\zeta^2}$, with $f_r = 0.4987$ Hz now named as a
frequency in hertz ([L360–L362](../../public/simulations/driven-oscillator.html#L360-L362)); the sign of the poles' real part,
$-1/\tau$ ([L374](../../public/simulations/driven-oscillator.html#L374)); the origin of $\tfrac12 c\,\Omega^2X^2$
([L459](../../public/simulations/driven-oscillator.html#L459)). Corrected: Exercise 6.1 said the transient "hardly shows" at
$f = 0.20$ Hz; the force switches on at full strength, so the ringing starts as large as the steady motion (measured at
$\zeta = 0.01$: $\sqrt{C_1^2+C_2^2} = 1.00005\,X$, $|x|$ up to $0.224$ m $= 1.85\,X$ at 5 s)
([L451](../../public/simulations/driven-oscillator.html#L451)); section 9 described one 60 s chart, but the dashed $F/k$ and
$\pm X$ belong to the moving window ($\operatorname{clamp}(4/f, 6, 20)$ s, 8.9 s with the defaults) above the 60 s strip
([L475](../../public/simulations/driven-oscillator.html#L475)). Further reading now links every item and adds Feynman,
Vol. I, chapters 23 and 24 ([L513–L517](../../public/simulations/driven-oscillator.html#L513-L517)).

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig09/`), the lead made only these changes, each on its existing line, so no line link moved: §2: ω_d no longer used before ζ is defined ([L245](../../public/simulations/driven-oscillator.html#L245)); §3.2: the ringing written before its constants are fixed ([L261](../../public/simulations/driven-oscillator.html#L261)); §5: X(s), F(s) named as transforms ([L372](../../public/simulations/driven-oscillator.html#L372)); Figure 3: the plant box widened so G(s) fits ([L382](../../public/simulations/driven-oscillator.html#L382)); §9: every run drawn at its own scale; compare runs on the ruler ([L475](../../public/simulations/driven-oscillator.html#L475)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

## Second check round · 20 October 2026

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig09/`), each change on its existing line: §3.1: the driving term, not the force, is the real part of (F₀/m)e^{iΩt} ([L255](../../public/simulations/driven-oscillator.html#L255)); equation (3) reflowed so its number shows at 1600 px ([L256](../../public/simulations/driven-oscillator.html#L256)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.
