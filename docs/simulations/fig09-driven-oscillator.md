# Fig. 9 · Driven Oscillator

| | |
|---|---|
| Page | [public/simulations/driven-oscillator.html](../../public/simulations/driven-oscillator.html) (1 113 lines, 183 130 bytes) |
| Walkthrough | [public/scripts/walk/driven.js](../../public/scripts/walk/driven.js) (14 steps, key `driven`) |
| Thumbnail | [public/images/sims/driven-oscillator.webp](../../public/images/sims/driven-oscillator.webp) (WebP, 800 × 500 px, 23.7 kB) |
| Catalog entry | [public/scripts/catalog.js#L183](../../public/scripts/catalog.js#L183-L199) (`id: 'driven-oscillator'`, `fig: 9`, `field: 'control'`, `stage: 1`, lines 183–199) |

A block of mass 1 kg sits on a spring and a damper and is pushed from its other side by a moving-coil drive: a coil on a
tube fixed to the block sits in the gap of a magnet, and the force on the block is $F = B\ell I$ with $B\ell = 10$ T·m. In
open loop the current source drives $I_0\cos\Omega t$, a push that does not care where the block is. With the controller
on, a PID controller $u = K_p(r-x) + K_i\int(r-x)\,dt - K_d\dot x$ adds its force through the same coil and holds the block
at an equilibrium it decides (lecture note §9, equations (12)–(16)). The reader sets the natural frequency, the damping
ratio, the push amplitude and frequency, the target $r$ and the three gains (presets Off, P, PD, PID), presses **Solve**, and
watches the stored run play back: the block with the three forces on it as arrows, the coil and its current, the damper with
its oil shaded by the heat it makes, energy bars $W_\text{in}$, $W_\text{loss}$, $E$, the controller box with its three
parts, the previous run as an outlined block and a dotted curve at the same scale, a moving window chart of $x(t)$, a strip
of the whole 60 s run, and a Bode plot with the closed loop $H(i\Omega)$ in ink and the bare plant dashed behind it. The page never integrates
while the reader watches. It solves the whole run first with the classical fourth-order Runge–Kutta method (RK4), writes
every sample into its dataset, and each frame then draws one stored row.

In this page, a link such as [L738](../../public/simulations/driven-oscillator.html#L738) points to a line of
`driven-oscillator.html`. Other files are named in the link text.

## The physics in one picture

**What you would see.** Push a child on a swing. Pushed at the wrong moments it barely moves; pushed in time with its own
rhythm it swings high. At first the swing also rings at its own rhythm, so two rhythms beat against each other; after a
while only the pusher's rhythm is left.

**The model.** Three forces act along the floor: the spring $-kx$, the damper $-c\dot x$ and the driver $F(t)$. Newton's
second law gives $m\ddot x + c\dot x + kx = F_0\cos\Omega t$. The time $t$ appears on its own inside the cosine: the clock
belongs to someone else. The lecture note derives this in sections 1–2
([L196](../../public/simulations/driven-oscillator.html#L196), [L233](../../public/simulations/driven-oscillator.html#L233)),
the exact solution in section 3 ([L243](../../public/simulations/driven-oscillator.html#L243)), resonance and phase in
section 4, the transfer function in section 5, beats in section 6 and the energy balance in section 7.

**What the code evaluates.** The sliders give $f_0$, $\zeta$, $F_0$ and $f$; `solve()` turns them into the constants of the
equation of motion ([L738](../../public/simulations/driven-oscillator.html#L738)):

$$\omega_0 = 2\pi f_0,\qquad k = m\,\omega_0^2,\qquad c = 2\zeta m\,\omega_0,\qquad \Omega = 2\pi f .$$

The right-hand side of the ODE is `accel()` ([L733–L735](../../public/simulations/driven-oscillator.html#L733-L735)):

$$\dot x = v,\qquad \dot v = a(t, x, v) = \frac{F_0\cos\Omega t - c\,v - k\,x}{m} .$$

Along the run the page also integrates the work of the driver and the heat of the damper
([L763–L764](../../public/simulations/driven-oscillator.html#L763-L764)) and stores the energy and the two powers at each
sample ([L751](../../public/simulations/driven-oscillator.html#L751)):

$$W_\text{in} = \int_0^T F v\,\mathrm dt,\quad W_\text{loss} = \int_0^T c\,v^2\,\mathrm dt,\quad E = \tfrac12 m v^2 + \tfrac12 k x^2,\quad P_\text{in} = F v,\quad P_\text{loss} = c v^2 .$$

The exact solution is used only to grade the numbers, never to draw them. `steady()`
([L684–L687](../../public/simulations/driven-oscillator.html#L684-L687)) gives the steady amplitude and phase lag, and
`exact()` ([L688–L691](../../public/simulations/driven-oscillator.html#L688-L691)) adds the transient that starts the block
from rest:

$$X = \frac{F_0/m}{\sqrt{(\omega_0^2-\Omega^2)^2 + (2\zeta\omega_0\Omega)^2}},\qquad \varphi = \operatorname{atan2}(2\zeta\omega_0\Omega,\ \omega_0^2-\Omega^2),$$

$$x_\text{exact}(t) = X\cos(\Omega t-\varphi) + e^{-\zeta\omega_0 t}\left(C_1\cos\omega_d t + C_2\sin\omega_d t\right),\quad C_1 = -X\cos\varphi,\quad C_2 = \frac{\zeta\omega_0 C_1 - X\Omega\sin\varphi}{\omega_d},\quad \omega_d = \omega_0\sqrt{1-\zeta^2}.$$

Further derived numbers ([L792–L801](../../public/simulations/driven-oscillator.html#L792-L801)): $\tau = 1/(\zeta\omega_0)$,
$Q = 1/(2\zeta)$, $f_r = f_0\sqrt{1-2\zeta^2}$ when $\zeta < 1/\sqrt2$ (else 0), $|G(i\Omega)| = X/F_0$, and the energy balance
$|E(T)-E(0)-(W_\text{in}-W_\text{loss})|/W_\text{in}$. The Bode plot evaluates $|G(i\Omega)| = 1/(m\sqrt{(\omega_0^2-\Omega^2)^2+(2\zeta\omega_0\Omega)^2})$
and $\varphi(\Omega)$ in degrees at 241 frequencies $f_j = 0.05\cdot 40^{j/240}$ Hz, from 0.05 to 2 Hz
([L821–L828](../../public/simulations/driven-oscillator.html#L821-L828)).

| Symbol | Meaning | Unit | In code |
|---|---|---|---|
| $m$ | mass, fixed at 1 | kg | `M` ([L528](../../public/simulations/driven-oscillator.html#L528)) |
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

One line fixes the run ([L528](../../public/simulations/driven-oscillator.html#L528)):
`M = 1` kg, `H = 0.001` s, `TEND = 60` s, `EVERY = 10`, and `NS = TEND / H / EVERY + 1`. In JavaScript `60 / 0.001` is
exactly 60 000, so `NS` is exactly 6 001 (checked in Node). The page keeps four pieces of its own state
([L535](../../public/simulations/driven-oscillator.html#L535)): `playT` (playback time, s), `iNow` (row on screen),
`fps` and `solved` (the slider values of the last solve, or `null`).

### 1 Solve: classical RK4 over the whole run

`solve()` ([L736–L808](../../public/simulations/driven-oscillator.html#L736-L808)) works on the state vector
$s = (x, v)$ with the slope $f(t, s) = (v,\ a(t, x, v))$. It starts from rest, $x = v = 0$ at $t = 0$
([L746](../../public/simulations/driven-oscillator.html#L746)). One step of size $h$ samples the slope four times: at the
start, twice at the middle and at the end ([L757–L760](../../public/simulations/driven-oscillator.html#L757-L760)):

$$k_1 = f(t, s),\quad k_2 = f(t+\tfrac h2, s+\tfrac h2 k_1),\quad k_3 = f(t+\tfrac h2, s+\tfrac h2 k_2),\quad k_4 = f(t+h, s+h k_3),$$
$$s(t+h) = s + \tfrac h6\,(k_1 + 2k_2 + 2k_3 + k_4) .$$

In the code the $x$-components of the slopes are the velocities `v, v2, v3, v4` and the $v$-components are the
accelerations `a1 … a4`; the update is [L766–L767](../../public/simulations/driven-oscillator.html#L766-L767). The two
work integrals are quadratures (their slopes do not feed back), carried with the same RK4 weights and the same stage
velocities, with the force evaluated at $t$, $t+h/2$ and $t+h$
([L762–L764](../../public/simulations/driven-oscillator.html#L762-L764)). Time is set from the step count,
`t = (step + 1) * H` ([L768](../../public/simulations/driven-oscillator.html#L768)), so it does not collect round-off by
repeated addition.

Why RK4 with $h = 1$ ms: the code does not state the reason. What can be measured is the margin. The fastest natural motion
allowed by the sliders is $\omega_0 = 2\pi\cdot1.5 = 9.42$ rad/s, so $\omega_0 h \le 0.0094$ rad per step, deep inside the
region where RK4 is stable and its error per step scales as $(\omega_0 h)^5$. With the defaults the largest difference to
the exact solution over the run is $5.26\times10^{-12}$ m and the energy balance holds to $1.27\times10^{-12}$ (measured).

### 2 Store: every tenth state

The loop runs `step = 0 … 60 000` ([L748](../../public/simulations/driven-oscillator.html#L748)). At the top of each pass,
before the step, every tenth state is written straight into the dataset arrays
([L749–L754](../../public/simulations/driven-oscillator.html#L749-L754)): `ts`, `xs`, `vs`, `Fs`, `Es`, `Pin`, `Ploss`. So
row $n$ holds the state at exactly $t_n = n\cdot 10h = n \cdot 10$ ms. After storing step 60 000 the loop stops without a
further step ([L755](../../public/simulations/driven-oscillator.html#L755)): 60 000 RK4 steps, 6 001 rows.

Two passes over the stored rows follow. The first ([L770–L778](../../public/simulations/driven-oscillator.html#L770-L778))
fills `xex` with the exact solution and finds the largest error `err`, the largest $|x|$ (`xmax`, which sets the drawing
scale) and the largest $|x|$ for $t_n \ge 50$ s (`Xm`, "Measured, last 10 s"). The second
([L779–L786](../../public/simulations/driven-oscillator.html#L779-L786)) fills `xqs` $= F_n/k$, the drive phase
`ph` $= \Omega t_n \bmod 2\pi$ and the chart half-height `ylim`. Then the arrays are marked changed
([L787](../../public/simulations/driven-oscillator.html#L787)) and every scalar is written
([L788–L802](../../public/simulations/driven-oscillator.html#L788-L802)).

The arrays come from `ds.alloc(name)` ([L744–L745](../../public/simulations/driven-oscillator.html#L744-L745)), which
allocates a new typed array only when the length changes ([dataset.js:67](../../public/scripts/dataset.js#L67)); a re-solve
overwrites the same `Float64Array`s in place. Memory, measured from the live store: 10 arrays × 6 001 × 8 B = 480 080 B for
the run, plus 3 × 241 × 8 B = 5 784 B for the Bode curves, 485 864 B in all. One solve took 6–17 ms in headless Chromium
(`solve_ms`, measured with `performance.now()` at [L737](../../public/simulations/driven-oscillator.html#L737) and
[L802](../../public/simulations/driven-oscillator.html#L802)).

Last, `solve()` records the settings it used in `solved` ([L803](../../public/simulations/driven-oscillator.html#L803)),
recomputes the Bode curves (`bode()`, [L817–L831](../../public/simulations/driven-oscillator.html#L817-L831)), rewrites the
readouts, sets `playT = 0` and starts the clock ([L804–L807](../../public/simulations/driven-oscillator.html#L804-L807)).

### When the run is solved again

Only twice: once at load ([L1485](../../public/simulations/driven-oscillator.html#L1485)) and whenever **Solve** is pressed
([L1218](../../public/simulations/driven-oscillator.html#L1218)). A slider only calls `markStale()`
([L669–L672](../../public/simulations/driven-oscillator.html#L669-L672),
[L833–L838](../../public/simulations/driven-oscillator.html#L833-L838)), which compares the four sliders with `solved`, sets
the `stale` flag and rewrites the status line in burgundy; the old run keeps playing, and its settings are named in the
status text ([L839–L849](../../public/simulations/driven-oscillator.html#L839-L849)).

### 3 Play: the frame loop, in order

`Sim.clock` ([sim.js:176–197](../../public/scripts/sim.js#L176-L197)) calls the page's tick on every
`requestAnimationFrame`, with $\Delta t$ capped at 0.05 s and $\Delta t = 0$ while paused. Each tick:

1. returns if nothing has been solved; updates the smoothed frame rate; advances `playT += speed · Δt`; at 60 s clamps and
   pauses; stores `fps` and `playing`; marks step "3 play" ([L1208–L1216](../../public/simulations/driven-oscillator.html#L1208-L1216));
2. `frame()` ([L1196–L1207](../../public/simulations/driven-oscillator.html#L1196-L1207)) picks the nearest stored row,
   $n = \operatorname{round}(t_\text{play}/10\,\text{ms})$ clamped to 0 … 6 000, writes `i_now`, `t_play` and the six
   `*_now` copies of row $n$ into the store, moves the **Stored run** slider and the caption time, then calls `draw()`;
3. `draw()` ([L1114–L1131](../../public/simulations/driven-oscillator.html#L1114-L1131)) sets the window width
   $T_w = \text{clamp}(4/f, 6, 20)$ s and its left edge $t_0 = \text{clamp}(t_n - 0.7T_w, 0, 60 - T_w)$, gets the layout
   from `geom()`, turns $x_n$ into the block position `bx = eqX + xs[i] * sc` and $F_n$ into the arrow length, stores these
   pixel values, clears the canvas and draws `drawMechanism`, `drawWindow` and `drawOverview` in that order.

Nothing in this chain integrates; the only arithmetic turns metres, seconds and newtons into pixels. Because the clock calls
the tick every animation frame even while paused (with $\Delta t = 0$), the figure is redrawn at the display rate in both
states; one `frame()` took about 1.5 ms (measured over 200 seek events at a 1 440 px wide window).

### Precomputation and caching

- The Bode canvas is not redrawn per frame: only after a solve ([L830](../../public/simulations/driven-oscillator.html#L830)),
  on resize ([L1487](../../public/simulations/driven-oscillator.html#L1487)) and when fonts are ready
  ([L1488](../../public/simulations/driven-oscillator.html#L1488)).
- `geom()` ([L865–L892](../../public/simulations/driven-oscillator.html#L865-L892)) is recomputed on every call; it reads
  `xmax`, `win_t0`, `win_T` and `ylim` from the store, so `draw()` must store the window before calling it
  ([L1117–L1118](../../public/simulations/driven-oscillator.html#L1117-L1118)).
- For the data panel's Check of $W_\text{in}$ and $W_\text{loss}$, `fullReplay()` reruns the whole 60 s once and caches the
  result under a key made of the four settings ([L1253–L1259](../../public/simulations/driven-oscillator.html#L1253-L1259)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `steady(w0, z, W, F)` | [684–687](../../public/simulations/driven-oscillator.html#L684-L687) | Exact steady amplitude $X$ and phase lag $\varphi$, equation (4) of the note. |
| `exact(t, w0, z, W, st)` | [688–691](../../public/simulations/driven-oscillator.html#L688-L691) | Exact $x(t)$ from rest, equation (5); used only to measure the RK4 error. |
| `control()` | [694–697](../../public/simulations/driven-oscillator.html#L694-L697) | The controller force $u = K_p(r-x) + K_i z - K_d v$, equation (12). |
| `closed()` | [698–702](../../public/simulations/driven-oscillator.html#L698-L702) | Closed-loop steady amplitude and phase, (16). |
| `equilibrium()` | [703–715](../../public/simulations/driven-oscillator.html#L703-L715) | Equilibrium (14). |
| `matmul()` | [704–715](../../public/simulations/driven-oscillator.html#L704-L715) | Matrix product (for `expm`). |
| `expm()` | [705–715](../../public/simulations/driven-oscillator.html#L705-L715) | Matrix exponential by scaling and squaring. |
| `exactClosed()` | [716–730](../../public/simulations/driven-oscillator.html#L716-L730) | Exact closed-loop solution sample by sample; grades RK4 when the controller is on. |
| `accel(t, x, v, u, p)` | [733–735](../../public/simulations/driven-oscillator.html#L733-L735) | Right-hand side: $(F_0\cos\Omega t + u - cv - kx)/m$. |
| `solve()` | [736–808](../../public/simulations/driven-oscillator.html#L736-L808) | Solve and store the whole run (see above). |
| `setSpan()` | [810–814](../../public/simulations/driven-oscillator.html#L810-L814) | Sets the held drawing span, `ylim`, `held`. |
| `fitScale()` | [815–831](../../public/simulations/driven-oscillator.html#L815-L831) | **Fit scale**: span ← need. |
| `bode()` | [817–831](../../public/simulations/driven-oscillator.html#L817-L831) | Fills `fb`, `Gmag`, `Gphase` (241 points) and redraws the Bode plot. |
| `markStale()` | [833–838](../../public/simulations/driven-oscillator.html#L833-L838) | Sets `stale` when a slider differs from the last solve. |
| `status()` | [839–849](../../public/simulations/driven-oscillator.html#L839-L849) | Writes the status line and the "1 solve / 2 store" marks. |
| `readouts()` | [850–861](../../public/simulations/driven-oscillator.html#L850-L861) | Writes the six readouts and the Bode caption $f_r$. |
| `geom()` | [865–892](../../public/simulations/driven-oscillator.html#L865-L892) | Layout from canvas size and store: mechanism, window chart, overview strip, dial; mapping functions `wx`, `wy`, `ox`, `oy`, `inWin`. |
| `arrow(c, …)` | [893–901](../../public/simulations/driven-oscillator.html#L893-L901) | Draws a straight arrow with a filled head. |
| `spring(c, …)` | [902–908](../../public/simulations/driven-oscillator.html#L902-L908) | Draws a zigzag spring. |
| `label(c, sym, value, …)` | [909–919](../../public/simulations/driven-oscillator.html#L909-L919) | A symbol in Latin Modern via `Sim.tex`, then its value in IBM Plex Mono. |
| `drawMechanism(c, g, i, bx, cap, gx)` | [920–977](../../public/simulations/driven-oscillator.html#L920-L977) | Wall, floor, rest line, spring, damper (oil shaded by $P_\text{loss}$), outlined previous block, block on wheels, then `drawCoil`, `drawForces`, `drawEnergy`, `drawController`; ruler, target dot, equilibrium line. |
| `drawCoil()` | [978–1006](../../public/simulations/driven-oscillator.html#L978-L1006) | Magnet, coil tube and winding, current dots and crosses, current source and leads. |
| `drawForces()` | [1007–1017](../../public/simulations/driven-oscillator.html#L1007-L1017) | The three force arrows over the block. |
| `drawController()` | [1018–1036](../../public/simulations/driven-oscillator.html#L1018-L1036) | The controller box: value read, P, I, D, u bars, command line. |
| `drawEnergy()` | [1037–1048](../../public/simulations/driven-oscillator.html#L1037-L1048) | The three energy bars. |
| `drawWindow(c, g, i)` | [1049–1092](../../public/simulations/driven-oscillator.html#L1049-L1092) | Window chart: ticks, $\pm X$, $F/k$, $x$ faint ahead and dark behind, cursor, key. |
| `drawOverview(c, g, i)` | [1093–1113](../../public/simulations/driven-oscillator.html#L1093-L1113) | Strip of the whole run with the window band shaded. |
| `draw()` | [1114–1131](../../public/simulations/driven-oscillator.html#L1114-L1131) | One frame of the main canvas. |
| `bodeGeom()` | [1133–1144](../../public/simulations/driven-oscillator.html#L1133-L1144) | Bode layout: two panels side by side (stacked below 560 px), log $f$ axis 0.05–2 Hz, three decades of $\lvert G\rvert$, 0–180°. |
| `drawBode()` | [1145–1177](../../public/simulations/driven-oscillator.html#L1145-L1177) | Draws both panels, the $f_0$ line, the curves, the dot at the exact value and the ring at the measured one. |
| `Sim.live()` | [1180–1194](../../public/simulations/driven-oscillator.html#L1180-L1194) | Formatted store values for the walkthrough's "Now" column. |
| `frame()` | [1196–1207](../../public/simulations/driven-oscillator.html#L1196-L1207) | Picks the stored row for `playT`, copies it to the `*_now` scalars, draws. |
| `chartPos(n)`, `chartPosQ(n)` | [1223–1226](../../public/simulations/driven-oscillator.html#L1223-L1226) | Screen point of $x_n$ (or $F_n/k$) on the window chart, else on the overview strip. |
| `chartPosQ()` | [1227–1230](../../public/simulations/driven-oscillator.html#L1227-L1230) |  |
| `loopParams()` | [1231–1252](../../public/simulations/driven-oscillator.html#L1231-L1252) | The eight settings of the last solve, for the checks. |
| `fullReplay()` | [1254–1259](../../public/simulations/driven-oscillator.html#L1254-L1259) | Cached `rk4Replay(6000)`. |
| `sliderCheck`, `at`, `neutralInk`, `readBack` | [1260–1266](../../public/simulations/driven-oscillator.html#L1260-L1266) | Small helpers for the data panel's Check (slider value, row on screen, dark-ink test, pixel read-back). |
| `at()` | [1261–1266](../../public/simulations/driven-oscillator.html#L1261-L1266) |  |
| `neutralInk()` | [1262–1266](../../public/simulations/driven-oscillator.html#L1262-L1266) |  |
| `readBack()` | [1263–1266](../../public/simulations/driven-oscillator.html#L1263-L1266) |  |
| `prevParams()` | [1267–1270](../../public/simulations/driven-oscillator.html#L1267-L1270) | Plant and loop of the previous run. |
| `mutedInk()` | [1271–1275](../../public/simulations/driven-oscillator.html#L1271-L1275) | Pixel test: grey ink. |
| `chartPosPrev()` | [1272–1275](../../public/simulations/driven-oscillator.html#L1272-L1275) | Where sample n of the previous run is drawn. |
| `roseInk()` | [1276–1285](../../public/simulations/driven-oscillator.html#L1276-L1285) | Pixel test: rose. |
| `ctrlBar()` | [1277–1285](../../public/simulations/driven-oscillator.html#L1277-L1285) | Where a controller bar ends. |
| `tanInk()` | [1278–1285](../../public/simulations/driven-oscillator.html#L1278-L1285) | Pixel test: brown. |
| `arrowPoint()` | [1279–1285](../../public/simulations/driven-oscillator.html#L1279-L1285) | Mid-point of a force arrow. |
| `barPoint()` | [1280–1285](../../public/simulations/driven-oscillator.html#L1280-L1285) | End of an energy bar. |
| `arrowBack()` | [1281–1285](../../public/simulations/driven-oscillator.html#L1281-L1285) | Read-back of a force arrow. |
| `blockPixel()` | [1286–1290](../../public/simulations/driven-oscillator.html#L1286-L1290) | Reads back a pixel inside the burgundy block. |
| `Sim.data` (object) | [1291–1483](../../public/simulations/driven-oscillator.html#L1291-L1483) | The data-panel contract: groups, colours, `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `about`. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Solve | `solve` | button | Calls `solve()` ([L1218](../../public/simulations/driven-oscillator.html#L1218)). |
| Pause / Play | `play` | button | Toggles the clock via `Sim.playButton` ([L1217](../../public/simulations/driven-oscillator.html#L1217), [sim.js:199](../../public/scripts/sim.js#L199)). |
| From t = 0 | `restart` | button | `playT = 0` and play ([L1219](../../public/simulations/driven-oscillator.html#L1219)). |
| Stored run | `seek` | 0–6000, step 1, default 0 ([L92](../../public/simulations/driven-oscillator.html#L92)) | Sets `playT = n · 10 ms` and draws ([L681](../../public/simulations/driven-oscillator.html#L681)); follows the playback ([L1204](../../public/simulations/driven-oscillator.html#L1204)). |
| Playback speed | `speed` | 0.25–4, step 0.25, default 1 ([L96](../../public/simulations/driven-oscillator.html#L96)) | Multiplies $\Delta t$ ([L1211](../../public/simulations/driven-oscillator.html#L1211)). Does not mark the run stale. |
| Natural frequency $f_0$ | `f0` | 0.2–1.5 Hz, step 0.01, default 0.5 ([L104](../../public/simulations/driven-oscillator.html#L104)) | $\omega_0$, $k$, $c$ at the next solve ([L738](../../public/simulations/driven-oscillator.html#L738)); marks stale. |
| Damping ratio $\zeta$ | `zeta` | 0.01–0.9, step 0.01, default 0.05 ([L108](../../public/simulations/driven-oscillator.html#L108)) | $c$ at the next solve; marks stale. The maximum 0.9 keeps $\omega_d$ real in `exact()`. |
| Force amplitude $F_0$ | `F0` | 0–5 N, step 0.1, default 1 ([L116](../../public/simulations/driven-oscillator.html#L116)) | `p.F0`; marks stale. At 0 the drive arrow is hidden and `Gm_drive` is NaN ([L799](../../public/simulations/driven-oscillator.html#L799)). |
| Drive frequency $f$ | `fd` | 0.05–1.5 Hz, step 0.01, default 0.45 ([L120](../../public/simulations/driven-oscillator.html#L120)) | $\Omega$ at the next solve; marks stale. |
| Fit scale | `fit` | button | `fitScale()`: span ← need, redraw. |
| Off / P / PD / PID | `[data-gains]` | buttons | Set $(K_p, K_i, K_d)$ to (0,0,0), (20,0,0), (20,0,4), (20,10,4) and mark stale. |
| Target position $r$ | `r` | −0.5–0.5 m, step 0.01, default 0.3 | `p.r`; marks stale. |
| Proportional gain $K_p$ | `Kp` | 0–60 N/m, step 0.5, default 0 | `p.Kp`; marks stale. |
| Integral gain $K_i$ | `Ki` | 0–60 N/(m·s), step 0.5, default 0 | `p.Ki`; marks stale. |
| Derivative gain $K_d$ | `Kd` | 0–12 kg/s, step 0.1, default 0 | `p.Kd`; marks stale. |
| Read values | added by datalog.js | switch, off | Appended to the first figure caption ([datalog.js:588–590](../../public/scripts/datalog.js#L588-L590)); see [datalog.md](../scripts/datalog.md). |

## What the page writes into the data store

The store is made at [L538](../../public/simulations/driven-oscillator.html#L538):
`Sim.dataset({ title: 'Driven oscillator', attrs: { figure: 9, page, equation, start } })`. It has two dimensions,
`n` = 6 001 stored rows ([L572](../../public/simulations/driven-oscillator.html#L572)) and `b` = 241 Bode frequencies
([L662](../../public/simulations/driven-oscillator.html#L662)), and 127 variables: 100 scalars and 27 `Float64Array`s, all
declared at [L539–L667](../../public/simulations/driven-oscillator.html#L539-L667) (counted in the live store). The shared
store itself is described in [dataset.md](../scripts/dataset.md). Each variable carries `symbol`, `units`, `long_name`,
`computed_in`, often `formula`, and `digits`. Listed by the panel groups of
[L1294–L1304](../../public/simulations/driven-oscillator.html#L1294-L1304):

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
([L1305](../../public/simulations/driven-oscillator.html#L1305), defined in
[datalog.js:71](../../public/scripts/datalog.js#L71)); this is presentation only.

**One round** (`Sim.data.round`, [L1476–L1478](../../public/simulations/driven-oscillator.html#L1476-L1478)) is one drive
period, $1/f$ seconds of the stored run, timed by `t_play`. Its columns are `x_now`, `v_now`, `u_now`, `F_now`, `Fc_now`, `Fk_now`, `E_now`, `Pin_now`;
the default point is the block. Recording is refused when fewer than $1/f$ seconds of the run remain ("press From t = 0").
The panel samples every frame of the round, at most 600 samples ([datalog.js:744](../../public/scripts/datalog.js#L744)).

**`Sim.live()`** ([L1180–L1194](../../public/simulations/driven-oscillator.html#L1180-L1194)) returns formatted strings read from
the store, for the keys the walkthrough uses: `k`, `c`, `W`, `w0`, `h`, `steps`, `n`, `t`, `x`, `v`, `F`, `E`, `X`, `phi`,
`err`, `Win`, `Wloss`, `bal`, `bx`, `sc`, `I0`, `I`, `BL`, `Fc`, `Fk`, `fN`, `span`, `Wc`, `Qc`, `u`, `r`, `Kp`, `Ki`, `Kd`, `z`, `xeq`. The walkthrough polls it every 200 ms
([sim.js:326](../../public/scripts/sim.js#L326)).

**Check and read-back.** `Sim.data.check` ([L1341–L1428](../../public/simulations/driven-oscillator.html#L1341-L1428))
recomputes every stored value from its stored inputs; for the ODE solution (`xs`, `vs`) and the run integrals (`Win`,
`Wloss`) it reruns the same RK4 from $t = 0$ (`rk4Replay`, up to 60 000 steps). `Sim.data.drawn`
([L1429–L1475](../../public/simulations/driven-oscillator.html#L1429-L1475)) reads pixels back: the burgundy block, the
three force arrows (or their absence below 2 px), the energy bars, the controller's $u$ bar, the target dot, the equilibrium line, the previous run's dotted curve, $x_n$ and $F_n/k$ on the charts, and the Bode curves and dots (plant dashed grey when the loop is on).
`probe` ([L1306–L1315](../../public/simulations/driven-oscillator.html#L1306-L1315)) pins the block when the click is within
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
  `#cap-res` ([L64–L72](../../public/simulations/driven-oscillator.html#L64-L72)); the control panel `aside.panel` with the
  solve box, the sliders, six readouts and a legend ([L75–L169](../../public/simulations/driven-oscillator.html#L75-L169)).
  The **Read values** switch is added to the first caption by datalog.js;
- `article.paper#paper`, the lecture note ([L172–L511](../../public/simulations/driven-oscillator.html#L172-L511)):
  abstract; ten sections `.psec` — 01 A push from outside, 02 The model, 03 The exact solution ★ (3.1 The steady state,
  3.2 The transient), 04 Resonance and phase, 05 The control engineer's view ★, 06 The start: beats and decay, 07 Where the
  energy goes, 08 Solve first, then play, 09 On screen, 10 What the model leaves out (10.1 Further reading, four items, each
  with a link). Nine numbered equations, `\tag{1}`–`\tag{8}` and `\tag{6a}` (the completed square that locates the
  resonance peak, [L353](../../public/simulations/driven-oscillator.html#L353)). Four figures with five inline SVGs: Figure 1 the plant sketch
  ([L201–L230](../../public/simulations/driven-oscillator.html#L201-L230)), Figure 2 amplitude and phase against $f/f_0$ for
  four damping ratios (two SVGs, [L261–L349](../../public/simulations/driven-oscillator.html#L261-L349)), Figure 3 the block
  diagram ([L368–L386](../../public/simulations/driven-oscillator.html#L368-L386)), Figure 4 the default run
  ([L392–L440](../../public/simulations/driven-oscillator.html#L392-L440)). Two exercise boxes, 4.1 and 6.1;
- `section#walk` with `data-walk="driven"` ([L513](../../public/simulations/driven-oscillator.html#L513)), filled by
  `sim.js` from `walk/driven.js` ([sim.js:402–411](../../public/scripts/sim.js#L402-L411)); see [walk.md](../scripts/walk.md);
- footer; then the scripts in load order: `fold.js`, `sim.js`, `dataset.js`, the page's inline script, `datalog.js`
  ([L521–L1491](../../public/simulations/driven-oscillator.html#L521-L1491)). Folds are described in
  [fold.md](../scripts/fold.md), the shared helpers in [sim.md](../scripts/sim.md).

The walkthrough's seven steps quote these page lines: step 1 [L738](../../public/simulations/driven-oscillator.html#L738);
step 2 [L733–L735](../../public/simulations/driven-oscillator.html#L733-L735); step 3
[L757–L760](../../public/simulations/driven-oscillator.html#L757-L760) and
[L766–L767](../../public/simulations/driven-oscillator.html#L766-L767); step 4
[L749–L754](../../public/simulations/driven-oscillator.html#L749-L754); step 5
[L763–L764](../../public/simulations/driven-oscillator.html#L763-L764) and
[L801](../../public/simulations/driven-oscillator.html#L801); step 6
[L685–L686](../../public/simulations/driven-oscillator.html#L685-L686) and
[L775](../../public/simulations/driven-oscillator.html#L775); step 7
[L1211](../../public/simulations/driven-oscillator.html#L1211), [L1197](../../public/simulations/driven-oscillator.html#L1197),
[L1119](../../public/simulations/driven-oscillator.html#L1119). All seven excerpts match the page text at present.

## Where the drawing and the store differ

The page states the differences in `Sim.data.about` ([L1480](../../public/simulations/driven-oscillator.html#L1480)), which
the data panel prints. In detail:

- **Nearest row, no interpolation.** `t_play` runs continuously, but the picture shows row
  $\operatorname{round}(t_\text{play}/10\,\text{ms})$ ([L1197](../../public/simulations/driven-oscillator.html#L1197)). The
  caption shows the row's time `ts[i]`, not `t_play` ([L1205](../../public/simulations/driven-oscillator.html#L1205)).
- **Overview strip thinned.** The strip of the whole run draws every `stride`-th row,
  `stride = max(1, floor(NS / (2 × strip width)))` ([L1095](../../public/simulations/driven-oscillator.html#L1095)): every 4th
  row at a 770 px canvas, every 10th at 356 px. The window chart draws every row between its edges
  ([L1051](../../public/simulations/driven-oscillator.html#L1051)).
- **Drawing scale is held between runs.** `span` (m) is the half-range the screen shows: it starts at the first run's
  `need = max(xmax, F0/k, |r|)`, grows only when a later run needs more, and **Fit scale** sets it to the present run
  (`setSpan()`). So `px_per_m = amp / span` is the same for consecutive runs unless one overflows, and a run with more
  damping really swings less on screen next to the dotted previous run. The force arrows use `px_per_N = 2 px_per_m / k`.
- **Previous run.** `xs_prev` is a copy of `xs` taken at the start of `solve()`, with the previous settings in `prev_*`;
  its Check reruns RK4 with those settings. The outlined block is left out at instants when it lies outside the span.
- **Controller.** The RK4 state is $(x, v, z)$ with $z = \int (r-x)\,dt$; `control()` is evaluated at all four stages. The
  exact solution that grades RK4 is `exactClosed()` when any gain is above zero: particular solution (16) plus the free
  motion propagated with the matrix exponential of the loop's state matrix (`expm`, scaling and squaring). An unstable loop
  is solved until $|x| > 1000$ m (`t_blow`); the rest of the run holds that state.
- **Old item, superseded:** *Drawing scale changes with the run.* The block travels at most `amp = 0.11 × W0` pixels either side of rest, where
  `W0` is the width between wall and right margin, so `px_per_m = amp / xmax` differs from run to run
  ([L875](../../public/simulations/driven-oscillator.html#L875), [L877](../../public/simulations/driven-oscillator.html#L877)).
  The ruler under the floor shows $\pm$`xmax` in metres ([L968](../../public/simulations/driven-oscillator.html#L968)).
- **Force arrow.** Its length is $F_n/F_0 \cdot L_F$ with $L_F = \min(88, 0.12\,w)$ px; arrows shorter than 2 px are not
  drawn ([L960](../../public/simulations/driven-oscillator.html#L960)).
- **Dial.** The arm points at the stored $\Omega t_n \bmod 2\pi$ ([L973](../../public/simulations/driven-oscillator.html#L973)).
- **Bode plot.** The dot sits at the exact $|G(i\Omega)|$ and $\varphi$; the ring is the amplitude measured from the last
  10 s of the stored run, per newton ([L1172–L1174](../../public/simulations/driven-oscillator.html#L1172-L1174)). With the
  defaults they differ by 0.03 % (0.48194 against 0.48209 m/N), the remains of the transient.
- **Rounding.** Canvas labels and readouts round (for example $F$ to 2 decimals, $x$ to 3); the store keeps full doubles.

## How to change it safely

- **Run length, step and storage stride.** `TEND`, `H` and `EVERY` ([L528](../../public/simulations/driven-oscillator.html#L528))
  determine `NS`. Keep `TEND / H` and `TEND / H / EVERY` whole numbers, because `step === TEND / H` and `step % EVERY` decide
  the last row ([L748–L755](../../public/simulations/driven-oscillator.html#L748-L755)). These places repeat the numbers by
  hand and must change with them: the seek slider `max="6000"` ([L92](../../public/simulations/driven-oscillator.html#L92));
  the `formula` texts "n · 10 h", "t_n ≥ 50 s", "round(t_play / 10h)" ([L573](../../public/simulations/driven-oscillator.html#L573),
  [L600](../../public/simulations/driven-oscillator.html#L600), [L604](../../public/simulations/driven-oscillator.html#L604));
  the group note "every 10 ms of the 60 s" ([L1299](../../public/simulations/driven-oscillator.html#L1299)); the check text
  "at most 6000" ([L1410](../../public/simulations/driven-oscillator.html#L1410)); the 10 s tick step of the overview
  ([L1111](../../public/simulations/driven-oscillator.html#L1111)); the walkthrough's "step / 10", "60 000 steps" and
  "6 001 rows" ([driven.js:57–58](../../public/scripts/walk/driven.js#L57-L58)); the lecture note section 8
  ([L458–L460](../../public/simulations/driven-oscillator.html#L458-L460)) and `about`.
- **The integrator exists twice.** `solve()` ([L757–L768](../../public/simulations/driven-oscillator.html#L757-L768)) and
  `rk4Replay()` ([L1238–L1249](../../public/simulations/driven-oscillator.html#L1238-L1249)) must stay identical, line for line,
  or the data panel's Check of `xs`, `vs`, `Win` and `Wloss` will no longer agree with the store.
- **Walkthrough excerpts.** The seven excerpts listed under Page structure are quoted verbatim in `walk/driven.js`. If one
  of those page lines changes, change the excerpt in the same edit. Insert new code after a quoted line, never inside a
  quoted group (AGENTS.md).
- **Taps stay where values are computed.** Write a new number into the store at the line that computes it, declare it with
  `ds.var` next to its relatives, add it to a group in `Sim.data.groups`, and give it a `check` (and a `drawn` if it is on
  screen). Do not compute numbers inside `draw*()` beyond the metre-to-pixel conversion.
- **Lecture-note numbers.** Sections 2–9 quote values for the default sliders ([L104–L120](../../public/simulations/driven-oscillator.html#L104-L120)),
  and Figures 2 and 4 are static SVGs computed from the page's formulas. Changing a default or the physics means
  recomputing them.
- **Damping limit.** `exact()` divides by $\omega_d = \omega_0\sqrt{1-\zeta^2}$; the slider stops at 0.9. Allowing
  $\zeta \ge 1$ needs a different exact solution (section 10 says so, [L497](../../public/simulations/driven-oscillator.html#L497)).
- **Frequency range.** The Bode axis covers 0.05–2 Hz ([L822](../../public/simulations/driven-oscillator.html#L822),
  [L1141](../../public/simulations/driven-oscillator.html#L1141)); raising the $f_0$ or $f$ slider beyond 2 Hz would put the
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
   ([L1215](../../public/simulations/driven-oscillator.html#L1215)), so a paused page still redraws about 60 times a second
   (about 1.5 ms per frame measured) and rewrites `#cap-t` each time ([L1205](../../public/simulations/driven-oscillator.html#L1205)).
7. Fixed on 2026-10-15: the note gives the measured default solve time of 9.5–12.4 ms and states that timing depends on the machine (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
8. **AGENTS.md** said the load order dataset.js → page → datalog.js holds for "all eight figures"; this page (Fig. 9)
   follows it too. Corrected to "all ten figures" on 14 October 2026.


## Teaching revision · 15 October 2026

The note separates undamped natural frequency from damped ringing, interprets the complex denominator as spring, inertia and quadrature damping, and uses the damped ringing frequency for the approximate default beat time. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16: the paragraph reading the complex denominator had been placed between "(2) turns into algebra:" and equation (3); it now follows (3) and ends "gives the form in (3)" ([L249](../../public/simulations/driven-oscillator.html#L249)). See the [audit of the revision](../research-theory-audit.md).

Fixed on 2026-10-16 (second repairs): the Millennium Bridge is back as the counter-example to a prescribed force (the walkers' steps fed back on the sway); the beat-time sentence is one sentence again ([L200](../../public/simulations/driven-oscillator.html#L200)). See the [audit of the revision](../research-theory-audit.md).

## Teaching revision · 20 October 2026

Judged section by section against [notes/STANDARD.md](../../notes/STANDARD.md); the verdicts and measurements are in
[notes/fig09/plan.md](../../notes/fig09/plan.md). Sections 1, 2 and 8, the text of section 6 and the limits in section 10 were left as they were. Filled in: the step from (3)
to (4), with `atan2` named and the real part justified ([L250](../../public/simulations/driven-oscillator.html#L250)); the
roots $s = -\zeta\omega_0 \pm i\omega_0\sqrt{1-\zeta^2}$ of the free equation, which give $\tau$, $\omega_d$ and the meaning of
$\zeta = 1$, and the two starting conditions behind $C_1$, $C_2$ ([L253](../../public/simulations/driven-oscillator.html#L253));
the completed square (6a) that places the peak at $\Omega_r = \omega_0\sqrt{1-2\zeta^2}$, with $f_r = 0.4987$ Hz now named as a
frequency in hertz ([L352–L354](../../public/simulations/driven-oscillator.html#L352-L354)); the sign of the poles' real part,
$-1/\tau$ ([L366](../../public/simulations/driven-oscillator.html#L366)); the origin of $\tfrac12 c\,\Omega^2X^2$
([L451](../../public/simulations/driven-oscillator.html#L451)). Corrected: Exercise 6.1 said the transient "hardly shows" at
$f = 0.20$ Hz; the force switches on at full strength, so the ringing starts as large as the steady motion (measured at
$\zeta = 0.01$: $\sqrt{C_1^2+C_2^2} = 1.00005\,X$, $|x|$ up to $0.224$ m $= 1.85\,X$ at 5 s)
([L443](../../public/simulations/driven-oscillator.html#L443)); section 9 described one 60 s chart, but the dashed $F/k$ and
$\pm X$ belong to the moving window ($\operatorname{clamp}(4/f, 6, 20)$ s, 8.9 s with the defaults) above the 60 s strip
([L467](../../public/simulations/driven-oscillator.html#L467)). Further reading now links every item and adds Feynman,
Vol. I, chapters 23 and 24 ([L502–L506](../../public/simulations/driven-oscillator.html#L502-L506)).

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig09/`), the lead made only these changes, each on its existing line, so no line link moved: §2: ω_d no longer used before ζ is defined ([L237](../../public/simulations/driven-oscillator.html#L237)); §3.2: the ringing written before its constants are fixed ([L253](../../public/simulations/driven-oscillator.html#L253)); §5: X(s), F(s) named as transforms ([L364](../../public/simulations/driven-oscillator.html#L364)); Figure 3: the plant box widened so G(s) fits ([L374](../../public/simulations/driven-oscillator.html#L374)); §9: every run drawn at its own scale; compare runs on the ruler ([L467](../../public/simulations/driven-oscillator.html#L467)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

## Second check round · 20 October 2026

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig09/`), each change on its existing line: §3.1: the driving term, not the force, is the real part of (F₀/m)e^{iΩt} ([L247](../../public/simulations/driven-oscillator.html#L247)); equation (3) reflowed so its number shows at 1600 px ([L248](../../public/simulations/driven-oscillator.html#L248)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.
