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

In this page, a link such as [L773](../../public/simulations/driven-oscillator.html#L773) points to a line of
`driven-oscillator.html`. Other files are named in the link text.

## The physics in one picture

**What you would see.** Push a child on a swing. Pushed at the wrong moments it barely moves; pushed in time with its own
rhythm it swings high. At first the swing also rings at its own rhythm, so two rhythms beat against each other; after a
while only the pusher's rhythm is left.

**The model.** Three forces act along the floor: the spring $-kx$, the damper $-c\dot x$ and the driver $F(t)$. Newton's
second law gives $m\ddot x + c\dot x + kx = F_0\cos\Omega t$. The time $t$ appears on its own inside the cosine: the clock
belongs to someone else. The lecture note derives this in sections 1–2
([L206](../../public/simulations/driven-oscillator.html#L206), [L243](../../public/simulations/driven-oscillator.html#L243)),
the exact solution in section 3 ([L253](../../public/simulations/driven-oscillator.html#L253)), resonance and phase in
section 4, the transfer function in section 5, beats in section 6 and the energy balance in section 7.

**What the code evaluates.** The sliders give $f_0$, $\zeta$, $F_0$ and $f$; `solve()` turns them into the constants of the
equation of motion ([L773](../../public/simulations/driven-oscillator.html#L773)):

$$\omega_0 = 2\pi f_0,\qquad k = m\,\omega_0^2,\qquad c = 2\zeta m\,\omega_0,\qquad \Omega = 2\pi f .$$

The right-hand side of the ODE is `accel()` ([L769–L771](../../public/simulations/driven-oscillator.html#L769-L771)):

$$\dot x = v,\qquad \dot v = a(t, x, v) = \frac{F_0\cos\Omega t - c\,v - k\,x}{m} .$$

Along the run the page also integrates the work of the driver and the heat of the damper
([L805–L806](../../public/simulations/driven-oscillator.html#L805-L806)) and stores the energy and the two powers at each
sample ([L793](../../public/simulations/driven-oscillator.html#L793)):

$$W_\text{in} = \int_0^T F v\,\mathrm dt,\quad W_\text{loss} = \int_0^T c\,v^2\,\mathrm dt,\quad E = \tfrac12 m v^2 + \tfrac12 k x^2,\quad P_\text{in} = F v,\quad P_\text{loss} = c v^2 .$$

The exact solution is used only to grade the numbers, never to draw them. `steady()`
([L718–L721](../../public/simulations/driven-oscillator.html#L718-L721)) gives the steady amplitude and phase lag, and
`exact()` ([L722–L727](../../public/simulations/driven-oscillator.html#L722-L727)) adds the transient that starts the block
from rest:

$$X = \frac{F_0/m}{\sqrt{(\omega_0^2-\Omega^2)^2 + (2\zeta\omega_0\Omega)^2}},\qquad \varphi = \operatorname{atan2}(2\zeta\omega_0\Omega,\ \omega_0^2-\Omega^2),$$

$$x_\text{exact}(t) = X\cos(\Omega t-\varphi) + e^{-\zeta\omega_0 t}\left(C_1\cos\omega_d t + C_2\sin\omega_d t\right),\quad C_1 = -X\cos\varphi,\quad C_2 = \frac{\zeta\omega_0 C_1 - X\Omega\sin\varphi}{\omega_d},\quad \omega_d = \omega_0\sqrt{1-\zeta^2}.$$

Further derived numbers ([L836–L845](../../public/simulations/driven-oscillator.html#L836-L845)): $\tau = 1/(\zeta\omega_0)$,
$Q = 1/(2\zeta)$, $f_r = f_0\sqrt{1-2\zeta^2}$ when $\zeta < 1/\sqrt2$ (else 0), $|G(i\Omega)| = X/F_0$, and the energy balance
$|E(T)-E(0)-(W_\text{in}-W_\text{loss})|/W_\text{in}$. The Bode plot evaluates $|G(i\Omega)| = 1/(m\sqrt{(\omega_0^2-\Omega^2)^2+(2\zeta\omega_0\Omega)^2})$
and $\varphi(\Omega)$ in degrees at 241 frequencies $f_j = 0.05\cdot 40^{j/240}$ Hz, from 0.05 to 2 Hz
([L865–L872](../../public/simulations/driven-oscillator.html#L865-L872)).

| Symbol | Meaning | Unit | In code |
|---|---|---|---|
| $m$ | mass, fixed at 1 | kg | `M` ([L541](../../public/simulations/driven-oscillator.html#L541)) |
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

One line fixes the run ([L541](../../public/simulations/driven-oscillator.html#L541)):
`M = 1` kg, `H = 0.001` s, `TEND = 60` s, `EVERY = 10`, and `NS = TEND / H / EVERY + 1`. In JavaScript `60 / 0.001` is
exactly 60 000, so `NS` is exactly 6 001 (checked in Node). The page keeps four pieces of its own state
([L548](../../public/simulations/driven-oscillator.html#L548)): `playT` (playback time, s), `iNow` (row on screen),
`fps` and `solved` (the slider values of the last solve, or `null`).

### 1 Solve: classical RK4 over the whole run

`solve()` ([L772–L852](../../public/simulations/driven-oscillator.html#L772-L852)) works on the state vector
$s = (x, v)$ with the slope $f(t, s) = (v,\ a(t, x, v))$. It starts from rest, $x = v = 0$ at $t = 0$
([L788](../../public/simulations/driven-oscillator.html#L788)). One step of size $h$ samples the slope four times: at the
start, twice at the middle and at the end ([L799–L802](../../public/simulations/driven-oscillator.html#L799-L802)):

$$k_1 = f(t, s),\quad k_2 = f(t+\tfrac h2, s+\tfrac h2 k_1),\quad k_3 = f(t+\tfrac h2, s+\tfrac h2 k_2),\quad k_4 = f(t+h, s+h k_3),$$
$$s(t+h) = s + \tfrac h6\,(k_1 + 2k_2 + 2k_3 + k_4) .$$

In the code the $x$-components of the slopes are the velocities `v, v2, v3, v4` and the $v$-components are the
accelerations `a1 … a4`; the update is [L808–L809](../../public/simulations/driven-oscillator.html#L808-L809). The two
work integrals are quadratures (their slopes do not feed back), carried with the same RK4 weights and the same stage
velocities, with the force evaluated at $t$, $t+h/2$ and $t+h$
([L804–L806](../../public/simulations/driven-oscillator.html#L804-L806)). Time is set from the step count,
`t = (step + 1) * H` ([L810](../../public/simulations/driven-oscillator.html#L810)), so it does not collect round-off by
repeated addition.

Why RK4 with $h = 1$ ms: the code does not state the reason. What can be measured is the margin. The fastest natural motion
allowed by the sliders is $\omega_0 = 2\pi\cdot1.5 = 9.42$ rad/s, so $\omega_0 h \le 0.0094$ rad per step, deep inside the
region where RK4 is stable and its error per step scales as $(\omega_0 h)^5$. With the defaults the largest difference to
the exact solution over the run is $5.26\times10^{-12}$ m and the energy balance holds to $1.27\times10^{-12}$ (measured).

### 2 Store: every tenth state

The loop runs `step = 0 … 60 000` ([L790](../../public/simulations/driven-oscillator.html#L790)). At the top of each pass,
before the step, every tenth state is written straight into the dataset arrays
([L791–L796](../../public/simulations/driven-oscillator.html#L791-L796)): `ts`, `xs`, `vs`, `Fs`, `Es`, `Pin`, `Ploss`. So
row $n$ holds the state at exactly $t_n = n\cdot 10h = n \cdot 10$ ms. After storing step 60 000 the loop stops without a
further step ([L797](../../public/simulations/driven-oscillator.html#L797)): 60 000 RK4 steps, 6 001 rows.

Two passes over the stored rows follow. The first ([L812–L820](../../public/simulations/driven-oscillator.html#L812-L820))
fills `xex` with the exact solution and finds the largest error `err`, the largest $|x|$ (`xmax`, which sets the drawing
scale) and the largest $|x|$ for $t_n \ge 50$ s (`Xm`, "Measured, last 10 s"). The second
([L821–L829](../../public/simulations/driven-oscillator.html#L821-L829)) fills `xqs` $= F_n/k$, the drive phase
`ph` $= \Omega t_n \bmod 2\pi$ and the chart half-height `ylim`. Then the arrays are marked changed
([L830](../../public/simulations/driven-oscillator.html#L830)) and every scalar is written
([L831–L846](../../public/simulations/driven-oscillator.html#L831-L846)).

The arrays come from `ds.alloc(name)` ([L786–L787](../../public/simulations/driven-oscillator.html#L786-L787)), which
allocates a new typed array only when the length changes ([dataset.js:67](../../public/scripts/dataset.js#L67)); a re-solve
overwrites the same `Float64Array`s in place. Memory, measured from the live store: 10 arrays × 6 001 × 8 B = 480 080 B for
the run, plus 3 × 241 × 8 B = 5 784 B for the Bode curves, 485 864 B in all. One solve took 6–17 ms in headless Chromium
(`solve_ms`, measured with `performance.now()` at [L772](../../public/simulations/driven-oscillator.html#L772) and
[L846](../../public/simulations/driven-oscillator.html#L846)).

Last, `solve()` records the settings it used in `solved` ([L847](../../public/simulations/driven-oscillator.html#L847)),
recomputes the Bode curves (`bode()`, [L861–L887](../../public/simulations/driven-oscillator.html#L861-L887)), rewrites the
readouts, sets `playT = 0` and starts the clock ([L848–L851](../../public/simulations/driven-oscillator.html#L848-L851)).

### When the run is solved again

Only twice: once at load ([L1684](../../public/simulations/driven-oscillator.html#L1684)) and whenever **Solve** is pressed
([L1392](../../public/simulations/driven-oscillator.html#L1392)). A slider only calls `markStale()`
([L701–L706](../../public/simulations/driven-oscillator.html#L701-L706),
[L889–L894](../../public/simulations/driven-oscillator.html#L889-L894)), which compares the four sliders with `solved`, sets
the `stale` flag and rewrites the status line in burgundy; the old run keeps playing, and its settings are named in the
status text ([L895–L905](../../public/simulations/driven-oscillator.html#L895-L905)).

### 3 Play: the frame loop, in order

`Sim.clock` ([sim.js:176–197](../../public/scripts/sim.js#L176-L197)) calls the page's tick on every
`requestAnimationFrame`, with $\Delta t$ capped at 0.05 s and $\Delta t = 0$ while paused. Each tick:

1. returns if nothing has been solved; updates the smoothed frame rate; advances `playT += speed · Δt`; at 60 s clamps and
   pauses; stores `fps` and `playing`; marks step "3 play" ([L1337–L1352](../../public/simulations/driven-oscillator.html#L1337-L1352));
2. `frame()` ([L1324–L1336](../../public/simulations/driven-oscillator.html#L1324-L1336)) picks the nearest stored row,
   $n = \operatorname{round}(t_\text{play}/10\,\text{ms})$ clamped to 0 … 6 000, writes `i_now`, `t_play` and the six
   `*_now` copies of row $n$ into the store, moves the **Stored run** slider and the caption time, then calls `draw()`;
3. `draw()` ([L1194–L1254](../../public/simulations/driven-oscillator.html#L1194-L1254)) sets the window width
   $T_w = \text{clamp}(4/f, 6, 20)$ s and its left edge $t_0 = \text{clamp}(t_n - 0.7T_w, 0, 60 - T_w)$, gets the layout
   from `geom()`, turns $x_n$ into the block position `bx = eqX + xs[i] * sc` and $F_n$ into the arrow length, stores these
   pixel values, clears the canvas and draws `drawMechanism`, `drawWindow` and `drawOverview` in that order.

Nothing in this chain integrates; the only arithmetic turns metres, seconds and newtons into pixels. Because the clock calls
the tick every animation frame even while paused (with $\Delta t = 0$), the figure is redrawn at the display rate in both
states; one `frame()` took about 1.5 ms (measured over 200 seek events at a 1 440 px wide window).

### Precomputation and caching

- The Bode canvas is not redrawn per frame: only after a solve ([L886](../../public/simulations/driven-oscillator.html#L886)),
  on resize ([L1687](../../public/simulations/driven-oscillator.html#L1687)) and when fonts are ready
  ([L1688](../../public/simulations/driven-oscillator.html#L1688)).
- `geom()` ([L921–L948](../../public/simulations/driven-oscillator.html#L921-L948)) is recomputed on every call; it reads
  `xmax`, `win_t0`, `win_T` and `ylim` from the store, so `draw()` must store the window before calling it
  ([L1197–L1198](../../public/simulations/driven-oscillator.html#L1197-L1198)).
- For the data panel's Check of $W_\text{in}$ and $W_\text{loss}$, `fullReplay()` reruns the whole 60 s once and caches the
  result under a key made of the four settings ([L1431–L1437](../../public/simulations/driven-oscillator.html#L1431-L1437)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `steady(w0, z, W, F)` | [718–721](../../public/simulations/driven-oscillator.html#L718-L721) | Exact steady amplitude $X$ and phase lag $\varphi$, equation (4) of the note. |
| `exact(t, w0, z, W, st)` | [722–727](../../public/simulations/driven-oscillator.html#L722-L727) | Exact $x(t)$ from rest, equation (5); used only to measure the RK4 error. |
| `control()` | [730–733](../../public/simulations/driven-oscillator.html#L730-L733) | The controller force $u = K_p(r-x) + K_i z - K_d v$, equation (12). |
| `closed()` | [734–738](../../public/simulations/driven-oscillator.html#L734-L738) | Closed-loop steady amplitude and phase, (16). |
| `equilibrium()` | [739](../../public/simulations/driven-oscillator.html#L739) | Equilibrium (14). |
| `matmul()` | [740](../../public/simulations/driven-oscillator.html#L740) | Matrix product (for `expm`). |
| `expm()` | [741–751](../../public/simulations/driven-oscillator.html#L741-L751) | Matrix exponential by scaling and squaring. |
| `exactClosed()` | [752–766](../../public/simulations/driven-oscillator.html#L752-L766) | Exact closed-loop solution sample by sample; grades RK4 when the controller is on. |
| `accel(t, x, v, u, p)` | [769–771](../../public/simulations/driven-oscillator.html#L769-L771) | Right-hand side: $(F_0\cos\Omega t + u - cv - kx)/m$. |
| `solve()` | [777–852](../../public/simulations/driven-oscillator.html#L777-L852) | Solve and store the whole run (see above). |
| `setSpan()` | [854–858](../../public/simulations/driven-oscillator.html#L854-L858) | Sets the held drawing span, `ylim`, `held`. |
| `fitScale()` | [859](../../public/simulations/driven-oscillator.html#L859) | **Fit scale**: span ← need. |
| `bode()` | [861–887](../../public/simulations/driven-oscillator.html#L861-L887) | Fills `fb`, `Gmag`, `Gphase` (241 points) and redraws the Bode plot. |
| `markStale()` | [889–894](../../public/simulations/driven-oscillator.html#L889-L894) | Sets `stale` when a slider differs from the last solve. |
| `status()` | [895–905](../../public/simulations/driven-oscillator.html#L895-L905) | Writes the status line and the "1 solve / 2 store" marks. |
| `readouts()` | [906–917](../../public/simulations/driven-oscillator.html#L906-L917) | Writes the six readouts and the Bode caption $f_r$. |
| `geom()` | [921–948](../../public/simulations/driven-oscillator.html#L921-L948) | Layout from canvas size and store: mechanism, window chart, overview strip, dial; mapping functions `wx`, `wy`, `ox`, `oy`, `inWin`. |
| `arrow(c, …)` | [949–957](../../public/simulations/driven-oscillator.html#L949-L957) | Draws a straight arrow with a filled head. |
| `spring(c, …)` | [958–964](../../public/simulations/driven-oscillator.html#L958-L964) | Draws a zigzag spring. |
| `label(c, sym, value, …)` | [965–975](../../public/simulations/driven-oscillator.html#L965-L975) | A symbol in Latin Modern via `Sim.tex`, then its value in IBM Plex Mono. |
| `drawMechanism(c, g, i, bx, cap, gx)` | [976–1033](../../public/simulations/driven-oscillator.html#L976-L1033) | Wall, floor, rest line, spring, damper (oil shaded by $P_\text{loss}$), outlined previous block, block on wheels, then `drawCoil`, `drawForces`, `drawEnergy`, `drawController`; ruler, target dot, equilibrium line. |
| `drawCoil()` | [1034–1063](../../public/simulations/driven-oscillator.html#L1034-L1063) | Magnet, coil tube and winding, current dots and crosses, current source and leads. |
| `drawForces()` | [1065–1081](../../public/simulations/driven-oscillator.html#L1065-L1081) | The three force arrows over the block. |
| `drawController()` | [1098–1116](../../public/simulations/driven-oscillator.html#L1098-L1116) | The controller box: value read, P, I, D, u bars, command line. |
| `drawEnergy()` | [1117–1128](../../public/simulations/driven-oscillator.html#L1117-L1128) | The three energy bars. |
| `drawWindow(c, g, i)` | [1129–1172](../../public/simulations/driven-oscillator.html#L1129-L1172) | Window chart: ticks, $\pm X$, $F/k$, $x$ faint ahead and dark behind, cursor, key. |
| `drawOverview(c, g, i)` | [1173–1193](../../public/simulations/driven-oscillator.html#L1173-L1193) | Strip of the whole run with the window band shaded. |
| `draw()` | [1194–1212](../../public/simulations/driven-oscillator.html#L1194-L1212) | One frame of the main canvas. |
| `bodeGeom()` | [1256–1269](../../public/simulations/driven-oscillator.html#L1256-L1269) | Bode layout: two panels side by side (stacked below 560 px), log $f$ axis 0.05–2 Hz, three decades of $\lvert G\rvert$, 0–180°. |
| `drawBode()` | [1270–1305](../../public/simulations/driven-oscillator.html#L1270-L1305) | Draws both panels, the $f_0$ line, the curves, the dot at the exact value and the ring at the measured one. |
| `Sim.live()` | [1308–1322](../../public/simulations/driven-oscillator.html#L1308-L1322) | Formatted store values for the walkthrough's "Now" column. |
| `frame()` | [1324–1336](../../public/simulations/driven-oscillator.html#L1324-L1336) | Picks the stored row for `playT`, copies it to the `*_now` scalars, draws. |
| `chartPos(n)`, `chartPosQ(n)` | [1401–1404](../../public/simulations/driven-oscillator.html#L1401-L1404) | Screen point of $x_n$ (or $F_n/k$) on the window chart, else on the overview strip. |
| `chartPosQ()` | [1405–1408](../../public/simulations/driven-oscillator.html#L1405-L1408) |  |
| `loopParams()` | [1409](../../public/simulations/driven-oscillator.html#L1409) | The eight settings of the last solve, for the checks. |
| `fullReplay()` | [1432–1437](../../public/simulations/driven-oscillator.html#L1432-L1437) | Cached `rk4Replay(6000)`. |
| `sliderCheck`, `at`, `neutralInk`, `readBack` | [1438](../../public/simulations/driven-oscillator.html#L1438) | Small helpers for the data panel's Check (slider value, row on screen, dark-ink test, pixel read-back). |
| `at()` | [1439–1441](../../public/simulations/driven-oscillator.html#L1439-L1441) |  |
| `neutralInk()` | [1442](../../public/simulations/driven-oscillator.html#L1442) |  |
| `readBack()` | [1443–1446](../../public/simulations/driven-oscillator.html#L1443-L1446) |  |
| `prevParams()` | [1447–1450](../../public/simulations/driven-oscillator.html#L1447-L1450) | Plant and loop of the previous run. |
| `mutedInk()` | [1451](../../public/simulations/driven-oscillator.html#L1451) | Pixel test: grey ink. |
| `chartPosPrev()` | [1452–1455](../../public/simulations/driven-oscillator.html#L1452-L1455) | Where sample n of the previous run is drawn. |
| `roseInk()` | [1456](../../public/simulations/driven-oscillator.html#L1456) | Pixel test: rose. |
| `ctrlBar()` | [1457](../../public/simulations/driven-oscillator.html#L1457) | Where a controller bar ends. |
| `tanInk()` | [1458](../../public/simulations/driven-oscillator.html#L1458) | Pixel test: brown. |
| `arrowPoint()` | [1459](../../public/simulations/driven-oscillator.html#L1459) | Mid-point of a force arrow. |
| `barPoint()` | [1460](../../public/simulations/driven-oscillator.html#L1460) | End of an energy bar. |
| `arrowBack()` | [1461–1465](../../public/simulations/driven-oscillator.html#L1461-L1465) | Read-back of a force arrow. |
| `blockPixel()` | [1466–1470](../../public/simulations/driven-oscillator.html#L1466-L1470) | Reads back a pixel inside the burgundy block. |
| `Sim.data` (object) | [1471–1682](../../public/simulations/driven-oscillator.html#L1471-L1682) | The data-panel contract: groups, colours, `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `about`. |
| `ctrlHead()` | [1088–1092](../../public/simulations/driven-oscillator.html#L1088-L1092) | Header of the controller box: one word on narrow screens. |
| `ctrlWidth()` | [1093–1097](../../public/simulations/driven-oscillator.html#L1093-L1097) | Width of the controller box, measured from its header. |
| `sliderParams()` | [772–776](../../public/simulations/driven-oscillator.html#L772-L776) | The plant and loop parameters from the sliders (used by `solve` and the hand). |
| `pointerX()` | [1355](../../public/simulations/driven-oscillator.html#L1355) | Pointer position in css px of the main canvas. |
| `holdState()` | [1356–1367](../../public/simulations/driven-oscillator.html#L1356-L1367) | The state while your hand holds the block: controller force, hand force, status line; then `draw()`. |
| `release()` | [1382–1387](../../public/simulations/driven-oscillator.html#L1382-L1387) | Ends a hold and calls `solve({x, v, z})`. |
| `capArrow()` | [1064](../../public/simulations/driven-oscillator.html#L1064) | Caps a force arrow at 1.6 A<sub>px</sub> (drawn with a break mark). |
| `ctrlScale()` | [1082–1087](../../public/simulations/driven-oscillator.html#L1082-L1087) | Scale of the controller bars: the run’s, or while held the largest force now. |
| `forceGeom()` | [1216–1220](../../public/simulations/driven-oscillator.html#L1216-L1220) | Layout of the force-profile canvas. |
| `forceCurves()` | [1221–1226](../../public/simulations/driven-oscillator.html#L1221-L1226) | Which force series the profile draws (controller parts only when on). |
| `drawForceProfile()` | [1227–1254](../../public/simulations/driven-oscillator.html#L1227-L1254) | Draws the force profile for the present row. |
| `setView()` | [1395](../../public/simulations/driven-oscillator.html#L1395) | Switches the frequency response between the linear view and the Bode view. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Solve | `solve` | button | Calls `solve()` ([L1392](../../public/simulations/driven-oscillator.html#L1392)). |
| Pause / Play | `play` | button | Toggles the clock via `Sim.playButton` ([L1391](../../public/simulations/driven-oscillator.html#L1391), [sim.js:199](../../public/scripts/sim.js#L199)). |
| From t = 0 | `restart` | button | `playT = 0` and play ([L1393](../../public/simulations/driven-oscillator.html#L1393)). |
| Stored run | `seek` | 0–6000, step 1, default 0 ([L102](../../public/simulations/driven-oscillator.html#L102)) | Sets `playT = n · 10 ms` and draws ([L715](../../public/simulations/driven-oscillator.html#L715)); follows the playback ([L1333](../../public/simulations/driven-oscillator.html#L1333)). |
| Playback speed | `speed` | 0.25–4, step 0.25, default 1 ([L106](../../public/simulations/driven-oscillator.html#L106)) | Multiplies $\Delta t$ ([L1347](../../public/simulations/driven-oscillator.html#L1347)). Does not mark the run stale. |
| Spring constant $k$ | `kspring` | 1.5–90 N/m, step 0.01, default 9.87 | Sets $k$; $f_0 = \sqrt{k/m}/2\pi$ is shown beside it and used by the rest of the code; marks stale. |
| Damping ratio $\zeta$ | `zeta` | 0.01–0.9, step 0.01, default 0.05 ([L118](../../public/simulations/driven-oscillator.html#L118)) | $c$ at the next solve; marks stale. The maximum 0.9 keeps $\omega_d$ real in `exact()`. |
| Force amplitude $F_0$ | `F0` | 0–5 N, step 0.1, default 1 ([L126](../../public/simulations/driven-oscillator.html#L126)) | `p.F0`; marks stale. At 0 the drive arrow is hidden and `Gm_drive` is NaN ([L843](../../public/simulations/driven-oscillator.html#L843)). |
| Drive frequency $f$ | `fd` | 0.05–1.5 Hz, step 0.01, default 0.45 ([L130](../../public/simulations/driven-oscillator.html#L130)) | $\Omega$ at the next solve; marks stale. |
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

The store is made at [L551](../../public/simulations/driven-oscillator.html#L551):
`Sim.dataset({ title: 'Driven oscillator', attrs: { figure: 9, page, equation, start } })`. It has two dimensions,
`n` = 6 001 stored rows ([L592](../../public/simulations/driven-oscillator.html#L592)) and `b` = 241 Bode frequencies
([L686](../../public/simulations/driven-oscillator.html#L686)), and 127 variables: 100 scalars and 27 `Float64Array`s, all
declared at [L552–L691](../../public/simulations/driven-oscillator.html#L552-L691) (counted in the live store). The shared
store itself is described in [dataset.md](../scripts/dataset.md). Each variable carries `symbol`, `units`, `long_name`,
`computed_in`, often `formula`, and `digits`. Listed by the panel groups of
[L1474–L1485](../../public/simulations/driven-oscillator.html#L1474-L1485):

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
([L1486](../../public/simulations/driven-oscillator.html#L1486), defined in
[datalog.js:71](../../public/scripts/datalog.js#L71)); this is presentation only.

**One round** (`Sim.data.round`, [L1675–L1677](../../public/simulations/driven-oscillator.html#L1675-L1677)) is one drive
period, $1/f$ seconds of the stored run, timed by `t_play`. Its columns are `x_now`, `v_now`, `u_now`, `F_now`, `Fc_now`, `Fk_now`, `E_now`, `Pin_now`;
the default point is the block. Recording is refused when fewer than $1/f$ seconds of the run remain ("press From t = 0").
The panel samples every frame of the round, at most 600 samples ([datalog.js:744](../../public/scripts/datalog.js#L744)).

**`Sim.live()`** ([L1308–L1322](../../public/simulations/driven-oscillator.html#L1308-L1322)) returns formatted strings read from
the store, for the keys the walkthrough uses: `k`, `c`, `W`, `w0`, `h`, `steps`, `n`, `t`, `x`, `v`, `F`, `E`, `X`, `phi`,
`err`, `Win`, `Wloss`, `bal`, `bx`, `sc`, `I0`, `I`, `BL`, `Fc`, `Fk`, `fN`, `span`, `Wc`, `Qc`, `u`, `r`, `Kp`, `Ki`, `Kd`, `z`, `xeq`. The walkthrough polls it every 200 ms
([sim.js:326](../../public/scripts/sim.js#L326)).

**Check and read-back.** `Sim.data.check` ([L1522–L1621](../../public/simulations/driven-oscillator.html#L1522-L1621))
recomputes every stored value from its stored inputs; for the ODE solution (`xs`, `vs`) and the run integrals (`Win`,
`Wloss`) it reruns the same RK4 from $t = 0$ (`rk4Replay`, up to 60 000 steps). `Sim.data.drawn`
([L1622–L1674](../../public/simulations/driven-oscillator.html#L1622-L1674)) reads pixels back: the burgundy block, the
three force arrows (or their absence below 2 px), the energy bars, the controller's $u$ bar, the target dot, the equilibrium line, the previous run's dotted curve, $x_n$ and $F_n/k$ on the charts, and the Bode curves and dots (plant dashed grey when the loop is on).
`probe` ([L1487–L1496](../../public/simulations/driven-oscillator.html#L1487-L1496)) pins the block when the click is within
40 px across and 34 px up or down of its centre, otherwise the nearest stored sample within 16 px (outside the window chart
only every fifth sample is tried). How the panel uses these hooks is in [datalog.md](../scripts/datalog.md).

## Page structure

**Head** ([L3–L27](../../public/simulations/driven-oscillator.html#L3-L27)): title "Driven Oscillator · Numa Koudsie",
description, the security policy and referrer rule ([build-and-deploy.md](../build-and-deploy.md#security)), then the stylesheets `../styles/sim.css`, `../styles/data.css`,
`../styles/fold.css` ([L11–L13](../../public/simulations/driven-oscillator.html#L11-L13)), an inline SVG favicon, and a
small inline style for the solve box (`.solve`, `.solve__steps`, `.solve__status`, `.seek`,
[L15–L26](../../public/simulations/driven-oscillator.html#L15-L26)). Styles are described in [styles.md](../styles.md).

**Body**, in order:
- `header.sim-top`: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`,
  87 × 48) and the back link "← All simulations" ([L30](../../public/simulations/driven-oscillator.html#L30)), then the hand-written Fig. 1–10 links, Fig. 9
  marked `aria-current` ([L29–L44](../../public/simulations/driven-oscillator.html#L29-L44));
- `.sim__head`: "Fig. 9 · control systems · forced oscillations", the `h1` and the lede
  ([L48–L52](../../public/simulations/driven-oscillator.html#L48-L52));
- `.sim__grid`: the main figure `#stage` with `canvas#osc` and a caption holding the equation and `#cap-t`
  ([L56–L64](../../public/simulations/driven-oscillator.html#L56-L64)); the Bode figure `#stage-bode` with `canvas#bode` and
  `#cap-res` ([L65–L82](../../public/simulations/driven-oscillator.html#L65-L82)); the control panel `aside.panel` with the
  solve box, the sliders, six readouts and a legend ([L85–L179](../../public/simulations/driven-oscillator.html#L85-L179)).
  The **Read values** switch is added to the first caption by datalog.js;
- `article.paper#paper`, the lecture note ([L182–L524](../../public/simulations/driven-oscillator.html#L182-L524)):
  abstract; ten sections `.psec` — 01 A push from outside, 02 The model, 03 The exact solution ★ (3.1 The steady state,
  3.2 The transient), 04 Resonance and phase, 05 The control engineer's view ★, 06 The start: beats and decay, 07 Where the
  energy goes, 08 Solve first, then play, 09 On screen, 10 What the model leaves out (10.1 Further reading, four items, each
  with a link). Nine numbered equations, `\tag{1}`–`\tag{8}` and `\tag{6a}` (the completed square that locates the
  resonance peak, [L363](../../public/simulations/driven-oscillator.html#L363)). Four figures with five inline SVGs: Figure 1 the plant sketch
  ([L211–L240](../../public/simulations/driven-oscillator.html#L211-L240)), Figure 2 amplitude and phase against $f/f_0$ for
  four damping ratios (two SVGs, [L271–L359](../../public/simulations/driven-oscillator.html#L271-L359)), Figure 3 the block
  diagram ([L378–L396](../../public/simulations/driven-oscillator.html#L378-L396)), Figure 4 the default run
  ([L402–L450](../../public/simulations/driven-oscillator.html#L402-L450)). Two exercise boxes, 4.1 and 6.1;
- `section#walk` with `data-walk="driven"` ([L526](../../public/simulations/driven-oscillator.html#L526)), filled by
  `sim.js` from `walk/driven.js` ([sim.js:402–411](../../public/scripts/sim.js#L402-L411)); see [walk.md](../scripts/walk.md);
- footer; then the scripts in load order: `fold.js`, `sim.js`, `dataset.js`, the page's inline script, `datalog.js`
  ([L534–L1691](../../public/simulations/driven-oscillator.html#L534-L1691)). Folds are described in
  [fold.md](../scripts/fold.md), the shared helpers in [sim.md](../scripts/sim.md).

The walkthrough's seven steps quote these page lines: step 1 [L773](../../public/simulations/driven-oscillator.html#L773);
step 2 [L769–L771](../../public/simulations/driven-oscillator.html#L769-L771); step 3
[L799–L802](../../public/simulations/driven-oscillator.html#L799-L802) and
[L808–L809](../../public/simulations/driven-oscillator.html#L808-L809); step 4
[L791–L796](../../public/simulations/driven-oscillator.html#L791-L796); step 5
[L805–L806](../../public/simulations/driven-oscillator.html#L805-L806) and
[L845](../../public/simulations/driven-oscillator.html#L845); step 6
[L719–L720](../../public/simulations/driven-oscillator.html#L719-L720) and
[L817](../../public/simulations/driven-oscillator.html#L817); step 7
[L1347](../../public/simulations/driven-oscillator.html#L1347), [L1325](../../public/simulations/driven-oscillator.html#L1325),
[L1199](../../public/simulations/driven-oscillator.html#L1199). All seven excerpts match the page text at present.

## Where the drawing and the store differ

The page states the differences in `Sim.data.about` ([L1679](../../public/simulations/driven-oscillator.html#L1679)), which
the data panel prints. In detail:

- **Nearest row, no interpolation.** `t_play` runs continuously, but the picture shows row
  $\operatorname{round}(t_\text{play}/10\,\text{ms})$ ([L1325](../../public/simulations/driven-oscillator.html#L1325)). The
  caption shows the row's time `ts[i]`, not `t_play` ([L1334](../../public/simulations/driven-oscillator.html#L1334)).
- **Overview strip thinned.** The strip of the whole run draws every `stride`-th row,
  `stride = max(1, floor(NS / (2 × strip width)))` ([L1175](../../public/simulations/driven-oscillator.html#L1175)): every 4th
  row at a 770 px canvas, every 10th at 356 px. The window chart draws every row between its edges
  ([L1131](../../public/simulations/driven-oscillator.html#L1131)).
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
  ([L931](../../public/simulations/driven-oscillator.html#L931), [L933](../../public/simulations/driven-oscillator.html#L933)).
  The ruler under the floor shows $\pm$`xmax` in metres ([L1024](../../public/simulations/driven-oscillator.html#L1024)).
- **Force arrow.** Its length is $F_n/F_0 \cdot L_F$ with $L_F = \min(88, 0.12\,w)$ px; arrows shorter than 2 px are not
  drawn ([L1016](../../public/simulations/driven-oscillator.html#L1016)).
- **Dial.** The arm points at the stored $\Omega t_n \bmod 2\pi$ ([L1029](../../public/simulations/driven-oscillator.html#L1029)).
- **Bode plot.** The dot sits at the exact $|G(i\Omega)|$ and $\varphi$; the ring is the amplitude measured from the last
  10 s of the stored run, per newton ([L1300–L1302](../../public/simulations/driven-oscillator.html#L1300-L1302)). With the
  defaults they differ by 0.03 % (0.48194 against 0.48209 m/N), the remains of the transient.
- **Rounding.** Canvas labels and readouts round (for example $F$ to 2 decimals, $x$ to 3); the store keeps full doubles.

## How to change it safely

- **Run length, step and storage stride.** `TEND`, `H` and `EVERY` ([L541](../../public/simulations/driven-oscillator.html#L541))
  determine `NS`. Keep `TEND / H` and `TEND / H / EVERY` whole numbers, because `step === TEND / H` and `step % EVERY` decide
  the last row ([L790–L797](../../public/simulations/driven-oscillator.html#L790-L797)). These places repeat the numbers by
  hand and must change with them: the seek slider `max="6000"` ([L102](../../public/simulations/driven-oscillator.html#L102));
  the `formula` texts "n · 10 h", "t_n ≥ 50 s", "round(t_play / 10h)" ([L593](../../public/simulations/driven-oscillator.html#L593),
  [L620](../../public/simulations/driven-oscillator.html#L620), [L624](../../public/simulations/driven-oscillator.html#L624));
  the group note "every 10 ms of the 60 s" ([L1480](../../public/simulations/driven-oscillator.html#L1480)); the check text
  "at most 6000" ([L1603](../../public/simulations/driven-oscillator.html#L1603)); the 10 s tick step of the overview
  ([L1191](../../public/simulations/driven-oscillator.html#L1191)); the walkthrough's "step / 10", "60 000 steps" and
  "6 001 rows" ([driven.js:57–58](../../public/scripts/walk/driven.js#L57-L58)); the lecture note section 8
  ([L468–L470](../../public/simulations/driven-oscillator.html#L468-L470)) and `about`.
- **The integrator exists twice.** `solve()` ([L799–L810](../../public/simulations/driven-oscillator.html#L799-L810)) and
  `rk4Replay()` ([L1416–L1427](../../public/simulations/driven-oscillator.html#L1416-L1427)) must stay identical, line for line,
  or the data panel's Check of `xs`, `vs`, `Win` and `Wloss` will no longer agree with the store.
- **Walkthrough excerpts.** The seven excerpts listed under Page structure are quoted verbatim in `walk/driven.js`. If one
  of those page lines changes, change the excerpt in the same edit. Insert new code after a quoted line, never inside a
  quoted group (AGENTS.md).
- **Taps stay where values are computed.** Write a new number into the store at the line that computes it, declare it with
  `ds.var` next to its relatives, add it to a group in `Sim.data.groups`, and give it a `check` (and a `drawn` if it is on
  screen). Do not compute numbers inside `draw*()` beyond the metre-to-pixel conversion.
- **Lecture-note numbers.** Sections 2–9 quote values for the default sliders ([L114–L130](../../public/simulations/driven-oscillator.html#L114-L130)),
  and Figures 2 and 4 are static SVGs computed from the page's formulas. Changing a default or the physics means
  recomputing them.
- **Damping limit.** `exact()` divides by $\omega_d = \omega_0\sqrt{1-\zeta^2}$; the slider stops at 0.9. Allowing
  $\zeta \ge 1$ needs a different exact solution (section 10 says so, [L510](../../public/simulations/driven-oscillator.html#L510)).
- **Frequency range.** The Bode axis covers 0.05–2 Hz ([L866](../../public/simulations/driven-oscillator.html#L866),
  [L1264](../../public/simulations/driven-oscillator.html#L1264)); raising the $f_0$ or $f$ slider beyond 2 Hz would put the
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
   ([L1351](../../public/simulations/driven-oscillator.html#L1351)), so a paused page still redraws about 60 times a second
   (about 1.5 ms per frame measured) and rewrites `#cap-t` each time ([L1334](../../public/simulations/driven-oscillator.html#L1334)).
7. Fixed on 2026-10-15: the note gives the measured default solve time of 9.5–12.4 ms and states that timing depends on the machine (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
8. **AGENTS.md** said the load order dataset.js → page → datalog.js holds for "all eight figures"; this page (Fig. 9)
   follows it too. Corrected to "all ten figures" on 14 October 2026.


## Teaching revision · 15 October 2026

The note separates undamped natural frequency from damped ringing, interprets the complex denominator as spring, inertia and quadrature damping, and uses the damped ringing frequency for the approximate default beat time. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16: the paragraph reading the complex denominator had been placed between "(2) turns into algebra:" and equation (3); it now follows (3) and ends "gives the form in (3)" ([L259](../../public/simulations/driven-oscillator.html#L259)). See the [audit of the revision](../research-theory-audit.md).

Fixed on 2026-10-16 (second repairs): the Millennium Bridge is back as the counter-example to a prescribed force (the walkers' steps fed back on the sway); the beat-time sentence is one sentence again ([L210](../../public/simulations/driven-oscillator.html#L210)). See the [audit of the revision](../research-theory-audit.md).

## Teaching revision · 20 October 2026

Judged section by section against [notes/STANDARD.md](../../notes/STANDARD.md); the verdicts and measurements are in
[notes/fig09/plan.md](../../notes/fig09/plan.md). Sections 1, 2 and 8, the text of section 6 and the limits in section 10 were left as they were. Filled in: the step from (3)
to (4), with `atan2` named and the real part justified ([L260](../../public/simulations/driven-oscillator.html#L260)); the
roots $s = -\zeta\omega_0 \pm i\omega_0\sqrt{1-\zeta^2}$ of the free equation, which give $\tau$, $\omega_d$ and the meaning of
$\zeta = 1$, and the two starting conditions behind $C_1$, $C_2$ ([L263](../../public/simulations/driven-oscillator.html#L263));
the completed square (6a) that places the peak at $\Omega_r = \omega_0\sqrt{1-2\zeta^2}$, with $f_r = 0.4987$ Hz now named as a
frequency in hertz ([L362–L364](../../public/simulations/driven-oscillator.html#L362-L364)); the sign of the poles' real part,
$-1/\tau$ ([L376](../../public/simulations/driven-oscillator.html#L376)); the origin of $\tfrac12 c\,\Omega^2X^2$
([L461](../../public/simulations/driven-oscillator.html#L461)). Corrected: Exercise 6.1 said the transient "hardly shows" at
$f = 0.20$ Hz; the force switches on at full strength, so the ringing starts as large as the steady motion (measured at
$\zeta = 0.01$: $\sqrt{C_1^2+C_2^2} = 1.00005\,X$, $|x|$ up to $0.224$ m $= 1.85\,X$ at 5 s)
([L453](../../public/simulations/driven-oscillator.html#L453)); section 9 described one 60 s chart, but the dashed $F/k$ and
$\pm X$ belong to the moving window ($\operatorname{clamp}(4/f, 6, 20)$ s, 8.9 s with the defaults) above the 60 s strip
([L477](../../public/simulations/driven-oscillator.html#L477)). Further reading now links every item and adds Feynman,
Vol. I, chapters 23 and 24 ([L515–L519](../../public/simulations/driven-oscillator.html#L515-L519)).

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig09/`), the lead made only these changes, each on its existing line, so no line link moved: §2: ω_d no longer used before ζ is defined ([L247](../../public/simulations/driven-oscillator.html#L247)); §3.2: the ringing written before its constants are fixed ([L263](../../public/simulations/driven-oscillator.html#L263)); §5: X(s), F(s) named as transforms ([L374](../../public/simulations/driven-oscillator.html#L374)); Figure 3: the plant box widened so G(s) fits ([L384](../../public/simulations/driven-oscillator.html#L384)); §9: every run drawn at its own scale; compare runs on the ruler ([L477](../../public/simulations/driven-oscillator.html#L477)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

## Second check round · 20 October 2026

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig09/`), each change on its existing line: §3.1: the driving term, not the force, is the real part of (F₀/m)e^{iΩt} ([L257](../../public/simulations/driven-oscillator.html#L257)); equation (3) reflowed so its number shows at 1600 px ([L258](../../public/simulations/driven-oscillator.html#L258)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.
