# Fig. 9 · Driven Oscillator

| | |
|---|---|
| Page | [public/simulations/driven-oscillator.html](../../public/simulations/driven-oscillator.html) (1 108 lines, 178 kB) |
| Walkthrough | [public/scripts/walk/driven.js](../../public/scripts/walk/driven.js) (121 lines, 7 steps) |
| Thumbnail | [public/images/sims/driven-oscillator.webp](../../public/images/sims/driven-oscillator.webp) (800 × 500 px) |
| Catalog entry | [public/scripts/catalog.js#L183](../../public/scripts/catalog.js#L183-L199) (`id: 'driven-oscillator'`, `fig: 9`) |

A block of mass 1 kg sits on a spring and a damper and is pushed by a force $F_0\cos\Omega t$ that does not care where the
block is. The reader sets the natural frequency, the damping ratio, the force amplitude and the drive frequency, presses
**Solve**, and watches the stored run play back: the block, the force arrow, a turning dial for the driver, a moving window
chart of $x(t)$, a strip of the whole 60 s run, and a Bode plot with the present drive marked. The page never integrates
while the reader watches. It solves the whole run first with the classical fourth-order Runge–Kutta method (RK4), writes
every sample into its dataset, and each frame then draws one stored row.

In this page, a link such as [L567](../../public/simulations/driven-oscillator.html#L567) points to a line of
`driven-oscillator.html`. Other files are named in the link text.

## The physics in one picture

**What you would see.** Push a child on a swing. Pushed at the wrong moments it barely moves; pushed in time with its own
rhythm it swings high. At first the swing also rings at its own rhythm, so two rhythms beat against each other; after a
while only the pusher's rhythm is left.

**The model.** Three forces act along the floor: the spring $-kx$, the damper $-c\dot x$ and the driver $F(t)$. Newton's
second law gives $m\ddot x + c\dot x + kx = F_0\cos\Omega t$. The time $t$ appears on its own inside the cosine: the clock
belongs to someone else. The lecture note derives this in sections 1–2
([L164](../../public/simulations/driven-oscillator.html#L164), [L201](../../public/simulations/driven-oscillator.html#L201)),
the exact solution in section 3 ([L211](../../public/simulations/driven-oscillator.html#L211)), resonance and phase in
section 4, the transfer function in section 5, beats in section 6 and the energy balance in section 7.

**What the code evaluates.** The sliders give $f_0$, $\zeta$, $F_0$ and $f$; `solve()` turns them into the constants of the
equation of motion ([L567](../../public/simulations/driven-oscillator.html#L567)):

$$\omega_0 = 2\pi f_0,\qquad k = m\,\omega_0^2,\qquad c = 2\zeta m\,\omega_0,\qquad \Omega = 2\pi f .$$

The right-hand side of the ODE is `accel()` ([L562–L564](../../public/simulations/driven-oscillator.html#L562-L564)):

$$\dot x = v,\qquad \dot v = a(t, x, v) = \frac{F_0\cos\Omega t - c\,v - k\,x}{m} .$$

Along the run the page also integrates the work of the driver and the heat of the damper
([L584–L585](../../public/simulations/driven-oscillator.html#L584-L585)) and stores the energy and the two powers at each
sample ([L574](../../public/simulations/driven-oscillator.html#L574)):

$$W_\text{in} = \int_0^T F v\,\mathrm dt,\quad W_\text{loss} = \int_0^T c\,v^2\,\mathrm dt,\quad E = \tfrac12 m v^2 + \tfrac12 k x^2,\quad P_\text{in} = F v,\quad P_\text{loss} = c v^2 .$$

The exact solution is used only to grade the numbers, never to draw them. `steady()`
([L552–L555](../../public/simulations/driven-oscillator.html#L552-L555)) gives the steady amplitude and phase lag, and
`exact()` ([L556–L559](../../public/simulations/driven-oscillator.html#L556-L559)) adds the transient that starts the block
from rest:

$$X = \frac{F_0/m}{\sqrt{(\omega_0^2-\Omega^2)^2 + (2\zeta\omega_0\Omega)^2}},\qquad \varphi = \operatorname{atan2}(2\zeta\omega_0\Omega,\ \omega_0^2-\Omega^2),$$

$$x_\text{exact}(t) = X\cos(\Omega t-\varphi) + e^{-\zeta\omega_0 t}\left(C_1\cos\omega_d t + C_2\sin\omega_d t\right),\quad C_1 = -X\cos\varphi,\quad C_2 = \frac{\zeta\omega_0 C_1 - X\Omega\sin\varphi}{\omega_d},\quad \omega_d = \omega_0\sqrt{1-\zeta^2}.$$

Further derived numbers ([L605–L611](../../public/simulations/driven-oscillator.html#L605-L611)): $\tau = 1/(\zeta\omega_0)$,
$Q = 1/(2\zeta)$, $f_r = f_0\sqrt{1-2\zeta^2}$ when $\zeta < 1/\sqrt2$ (else 0), $|G(i\Omega)| = X/F_0$, and the energy balance
$|E(T)-E(0)-(W_\text{in}-W_\text{loss})|/W_\text{in}$. The Bode plot evaluates $|G(i\Omega)| = 1/(m\sqrt{(\omega_0^2-\Omega^2)^2+(2\zeta\omega_0\Omega)^2})$
and $\varphi(\Omega)$ in degrees at 241 frequencies $f_j = 0.05\cdot 40^{j/240}$ Hz, from 0.05 to 2 Hz
([L623–L628](../../public/simulations/driven-oscillator.html#L623-L628)).

| Symbol | Meaning | Unit | In code |
|---|---|---|---|
| $m$ | mass, fixed at 1 | kg | `M` ([L469](../../public/simulations/driven-oscillator.html#L469)) |
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

One line fixes the run ([L469](../../public/simulations/driven-oscillator.html#L469)):
`M = 1` kg, `H = 0.001` s, `TEND = 60` s, `EVERY = 10`, and `NS = TEND / H / EVERY + 1`. In JavaScript `60 / 0.001` is
exactly 60 000, so `NS` is exactly 6 001 (checked in Node). The page keeps five pieces of its own state
([L475](../../public/simulations/driven-oscillator.html#L475)): `playT` (playback time, s), `iNow` (row on screen), `frames`,
`fps` and `solved` (the slider values of the last solve, or `null`).

### 1 Solve: classical RK4 over the whole run

`solve()` ([L565–L618](../../public/simulations/driven-oscillator.html#L565-L618)) works on the state vector
$s = (x, v)$ with the slope $f(t, s) = (v,\ a(t, x, v))$. It starts from rest, $x = v = 0$ at $t = 0$
([L570](../../public/simulations/driven-oscillator.html#L570)). One step of size $h$ samples the slope four times: at the
start, twice at the middle and at the end ([L579–L582](../../public/simulations/driven-oscillator.html#L579-L582)):

$$k_1 = f(t, s),\quad k_2 = f(t+\tfrac h2, s+\tfrac h2 k_1),\quad k_3 = f(t+\tfrac h2, s+\tfrac h2 k_2),\quad k_4 = f(t+h, s+h k_3),$$
$$s(t+h) = s + \tfrac h6\,(k_1 + 2k_2 + 2k_3 + k_4) .$$

In the code the $x$-components of the slopes are the velocities `v, v2, v3, v4` and the $v$-components are the
accelerations `a1 … a4`; the update is [L586–L587](../../public/simulations/driven-oscillator.html#L586-L587). The two
work integrals are quadratures (their slopes do not feed back), carried with the same RK4 weights and the same stage
velocities, with the force evaluated at $t$, $t+h/2$ and $t+h$
([L583–L585](../../public/simulations/driven-oscillator.html#L583-L585)). Time is set from the step count,
`t = (step + 1) * H` ([L588](../../public/simulations/driven-oscillator.html#L588)), so it does not collect round-off by
repeated addition.

Why RK4 with $h = 1$ ms: the code does not state the reason. What can be measured is the margin. The fastest natural motion
allowed by the sliders is $\omega_0 = 2\pi\cdot1.5 = 9.42$ rad/s, so $\omega_0 h \le 0.0094$ rad per step, deep inside the
region where RK4 is stable and its error per step scales as $(\omega_0 h)^5$. With the defaults the largest difference to
the exact solution over the run is $5.26\times10^{-12}$ m and the energy balance holds to $1.27\times10^{-12}$ (measured).

### 2 Store: every tenth state

The loop runs `step = 0 … 60 000` ([L571](../../public/simulations/driven-oscillator.html#L571)). At the top of each pass,
before the step, every tenth state is written straight into the dataset arrays
([L572–L576](../../public/simulations/driven-oscillator.html#L572-L576)): `ts`, `xs`, `vs`, `Fs`, `Es`, `Pin`, `Ploss`. So
row $n$ holds the state at exactly $t_n = n\cdot 10h = n \cdot 10$ ms. After storing step 60 000 the loop stops without a
further step ([L577](../../public/simulations/driven-oscillator.html#L577)): 60 000 RK4 steps, 6 001 rows.

Two passes over the stored rows follow. The first ([L590–L596](../../public/simulations/driven-oscillator.html#L590-L596))
fills `xex` with the exact solution and finds the largest error `err`, the largest $|x|$ (`xmax`, which sets the drawing
scale) and the largest $|x|$ for $t_n \ge 50$ s (`Xm`, "Measured, last 10 s"). The second
([L597–L602](../../public/simulations/driven-oscillator.html#L597-L602)) fills `xqs` $= F_n/k$, the drive phase
`ph` $= \Omega t_n \bmod 2\pi$ and the chart half-height `ylim`. Then the arrays are marked changed
([L603](../../public/simulations/driven-oscillator.html#L603)) and every scalar is written
([L604–L612](../../public/simulations/driven-oscillator.html#L604-L612)).

The arrays come from `ds.alloc(name)` ([L568–L569](../../public/simulations/driven-oscillator.html#L568-L569)), which
allocates a new typed array only when the length changes ([dataset.js:67](../../public/scripts/dataset.js#L67)); a re-solve
overwrites the same `Float64Array`s in place. Memory, measured from the live store: 10 arrays × 6 001 × 8 B = 480 080 B for
the run, plus 3 × 241 × 8 B = 5 784 B for the Bode curves, 485 864 B in all. One solve took 6–17 ms in headless Chromium
(`solve_ms`, measured with `performance.now()` at [L566](../../public/simulations/driven-oscillator.html#L566) and
[L612](../../public/simulations/driven-oscillator.html#L612)).

Last, `solve()` records the settings it used in `solved` ([L613](../../public/simulations/driven-oscillator.html#L613)),
recomputes the Bode curves (`bode()`, [L620–L631](../../public/simulations/driven-oscillator.html#L620-L631)), rewrites the
readouts, sets `playT = 0` and starts the clock ([L614–L617](../../public/simulations/driven-oscillator.html#L614-L617)).

### When the run is solved again

Only twice: once at load ([L1100](../../public/simulations/driven-oscillator.html#L1100)) and whenever **Solve** is pressed
([L919](../../public/simulations/driven-oscillator.html#L919)). A slider only calls `markStale()`
([L544–L547](../../public/simulations/driven-oscillator.html#L544-L547),
[L633–L637](../../public/simulations/driven-oscillator.html#L633-L637)), which compares the four sliders with `solved`, sets
the `stale` flag and rewrites the status line in burgundy; the old run keeps playing, and its settings are named in the
status text ([L638–L645](../../public/simulations/driven-oscillator.html#L638-L645)).

### 3 Play: the frame loop, in order

`Sim.clock` ([sim.js:177–198](../../public/scripts/sim.js#L177-L198)) calls the page's tick on every
`requestAnimationFrame`, with $\Delta t$ capped at 0.05 s and $\Delta t = 0$ while paused. Each tick:

1. returns if nothing has been solved; updates the smoothed frame rate; advances `playT += speed · Δt`; at 60 s clamps and
   pauses; stores `fps` and `playing`; marks step "3 play" ([L909–L917](../../public/simulations/driven-oscillator.html#L909-L917));
2. `frame()` ([L899–L908](../../public/simulations/driven-oscillator.html#L899-L908)) picks the nearest stored row,
   $n = \operatorname{round}(t_\text{play}/10\,\text{ms})$ clamped to 0 … 6 000, writes `i_now`, `t_play` and the six
   `*_now` copies of row $n$ into the store, moves the **Stored run** slider and the caption time, then calls `draw()`;
3. `draw()` ([L829–L842](../../public/simulations/driven-oscillator.html#L829-L842)) sets the window width
   $T_w = \text{clamp}(4/f, 6, 20)$ s and its left edge $t_0 = \text{clamp}(t_n - 0.7T_w, 0, 60 - T_w)$, gets the layout
   from `geom()`, turns $x_n$ into the block position `bx = eqX + xs[i] * sc` and $F_n$ into the arrow length, stores these
   pixel values, clears the canvas and draws `drawMechanism`, `drawWindow` and `drawOverview` in that order.

Nothing in this chain integrates; the only arithmetic turns metres, seconds and newtons into pixels. Because the clock calls
the tick every animation frame even while paused (with $\Delta t = 0$), the figure is redrawn at the display rate in both
states; one `frame()` took about 1.5 ms (measured over 200 seek events at a 1 440 px wide window).

### Precomputation and caching

- The Bode canvas is not redrawn per frame: only after a solve ([L630](../../public/simulations/driven-oscillator.html#L630)),
  on resize ([L1102](../../public/simulations/driven-oscillator.html#L1102)) and when fonts are ready
  ([L1103](../../public/simulations/driven-oscillator.html#L1103)).
- `geom()` ([L659–L682](../../public/simulations/driven-oscillator.html#L659-L682)) is recomputed on every call; it reads
  `xmax`, `win_t0`, `win_T` and `ylim` from the store, so `draw()` must store the window before calling it
  ([L832–L833](../../public/simulations/driven-oscillator.html#L832-L833)).
- For the data panel's Check of $W_\text{in}$ and $W_\text{loss}$, `fullReplay()` reruns the whole 60 s once and caches the
  result under a key made of the four settings ([L950–L956](../../public/simulations/driven-oscillator.html#L950-L956)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `steady(w0, z, W, F)` | [552–555](../../public/simulations/driven-oscillator.html#L552-L555) | Exact steady amplitude $X$ and phase lag $\varphi$, equation (4) of the note. |
| `exact(t, w0, z, W, st)` | [556–559](../../public/simulations/driven-oscillator.html#L556-L559) | Exact $x(t)$ from rest, equation (5); used only to measure the RK4 error. |
| `accel(t, x, v, p)` | [562–564](../../public/simulations/driven-oscillator.html#L562-L564) | Right-hand side: $(F_0\cos\Omega t - cv - kx)/m$. |
| `solve()` | [565–618](../../public/simulations/driven-oscillator.html#L565-L618) | Solve and store the whole run (see above). |
| `bode()` | [620–631](../../public/simulations/driven-oscillator.html#L620-L631) | Fills `fb`, `Gmag`, `Gphase` (241 points) and redraws the Bode plot. |
| `markStale()` | [633–637](../../public/simulations/driven-oscillator.html#L633-L637) | Sets `stale` when a slider differs from the last solve. |
| `status()` | [638–645](../../public/simulations/driven-oscillator.html#L638-L645) | Writes the status line and the "1 solve / 2 store" marks. |
| `readouts()` | [646–655](../../public/simulations/driven-oscillator.html#L646-L655) | Writes the six readouts and the Bode caption $f_r$. |
| `geom()` | [659–682](../../public/simulations/driven-oscillator.html#L659-L682) | Layout from canvas size and store: mechanism, window chart, overview strip, dial; mapping functions `wx`, `wy`, `ox`, `oy`, `inWin`. |
| `arrow(c, …)` | [683–691](../../public/simulations/driven-oscillator.html#L683-L691) | Draws a straight arrow with a filled head. |
| `spring(c, …)` | [692–698](../../public/simulations/driven-oscillator.html#L692-L698) | Draws a zigzag spring. |
| `label(c, sym, value, …)` | [699–709](../../public/simulations/driven-oscillator.html#L699-L709) | A symbol in Latin Modern via `Sim.tex`, then its value in IBM Plex Mono. |
| `drawMechanism(c, g, i, bx, fpx)` | [710–767](../../public/simulations/driven-oscillator.html#L710-L767) | Wall, floor, rest line, spring, damper, block on wheels, force arrow, ruler with $x$, driver dial. |
| `drawWindow(c, g, i)` | [768–808](../../public/simulations/driven-oscillator.html#L768-L808) | Window chart: ticks, $\pm X$, $F/k$, $x$ faint ahead and dark behind, cursor, key. |
| `drawOverview(c, g, i)` | [809–828](../../public/simulations/driven-oscillator.html#L809-L828) | Strip of the whole run with the window band shaded. |
| `draw()` | [829–842](../../public/simulations/driven-oscillator.html#L829-L842) | One frame of the main canvas. |
| `bodeGeom()` | [844–855](../../public/simulations/driven-oscillator.html#L844-L855) | Bode layout: two panels side by side (stacked below 560 px), log $f$ axis 0.05–2 Hz, three decades of $\lvert G\rvert$, 0–180°. |
| `drawBode()` | [856–885](../../public/simulations/driven-oscillator.html#L856-L885) | Draws both panels, the $f_0$ line, the curves, the dot at the exact value and the ring at the measured one. |
| `Sim.live()` | [888–897](../../public/simulations/driven-oscillator.html#L888-L897) | Formatted store values for the walkthrough's "Now" column. |
| `frame()` | [899–908](../../public/simulations/driven-oscillator.html#L899-L908) | Picks the stored row for `playT`, copies it to the `*_now` scalars, draws. |
| clock tick (anonymous) | [909–917](../../public/simulations/driven-oscillator.html#L909-L917) | Advances `playT`, stops at 60 s, calls `frame()`. |
| `chartPos(n)`, `chartPosQ(n)` | [923–930](../../public/simulations/driven-oscillator.html#L923-L930) | Screen point of $x_n$ (or $F_n/k$) on the window chart, else on the overview strip. |
| `rk4Replay(n)` | [931–949](../../public/simulations/driven-oscillator.html#L931-L949) | The same RK4 rerun from $t=0$ to row $n$; the Check of `xs`, `vs`, `Win`, `Wloss`. |
| `fullReplay()` | [950–956](../../public/simulations/driven-oscillator.html#L950-L956) | Cached `rk4Replay(6000)`. |
| `sliderCheck`, `at`, `neutralInk`, `readBack` | [957–963](../../public/simulations/driven-oscillator.html#L957-L963) | Small helpers for the data panel's Check (slider value, row on screen, dark-ink test, pixel read-back). |
| `blockPixel()` | [964–968](../../public/simulations/driven-oscillator.html#L964-L968) | Reads back a pixel inside the burgundy block. |
| `Sim.data` (object) | [969–1098](../../public/simulations/driven-oscillator.html#L969-L1098) | The data-panel contract: groups, colours, `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `about`. |
| start-up | [1100–1103](../../public/simulations/driven-oscillator.html#L1100-L1103) | `solve()`, resize observers, redraw when fonts are ready. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Solve | `solve` | button | Calls `solve()` ([L919](../../public/simulations/driven-oscillator.html#L919)). |
| Pause / Play | `play` | button | Toggles the clock via `Sim.playButton` ([L918](../../public/simulations/driven-oscillator.html#L918), [sim.js:200](../../public/scripts/sim.js#L200)). |
| From t = 0 | `restart` | button | `playT = 0` and play ([L920](../../public/simulations/driven-oscillator.html#L920)). |
| Stored run | `seek` | 0–6000, step 1, default 0 ([L90](../../public/simulations/driven-oscillator.html#L90)) | Sets `playT = n · 10 ms` and draws ([L549](../../public/simulations/driven-oscillator.html#L549)); follows the playback ([L905](../../public/simulations/driven-oscillator.html#L905)). |
| Playback speed | `speed` | 0.25–4, step 0.25, default 1 ([L94](../../public/simulations/driven-oscillator.html#L94)) | Multiplies $\Delta t$ ([L912](../../public/simulations/driven-oscillator.html#L912)). Does not mark the run stale. |
| Natural frequency $f_0$ | `f0` | 0.2–1.5 Hz, step 0.01, default 0.5 ([L102](../../public/simulations/driven-oscillator.html#L102)) | $\omega_0$, $k$, $c$ at the next solve ([L567](../../public/simulations/driven-oscillator.html#L567)); marks stale. |
| Damping ratio $\zeta$ | `zeta` | 0.01–0.9, step 0.01, default 0.05 ([L106](../../public/simulations/driven-oscillator.html#L106)) | $c$ at the next solve; marks stale. The maximum 0.9 keeps $\omega_d$ real in `exact()`. |
| Force amplitude $F_0$ | `F0` | 0–5 N, step 0.1, default 1 ([L114](../../public/simulations/driven-oscillator.html#L114)) | `p.F0`; marks stale. At 0 the arrow is hidden and `Gm_drive` is NaN ([L609](../../public/simulations/driven-oscillator.html#L609)). |
| Drive frequency $f$ | `fd` | 0.05–1.5 Hz, step 0.01, default 0.45 ([L118](../../public/simulations/driven-oscillator.html#L118)) | $\Omega$ at the next solve; marks stale. |
| Read values | added by datalog.js | switch, off | Appended to the first figure caption ([datalog.js:587–589](../../public/scripts/datalog.js#L587-L589)); see [datalog.md](../scripts/datalog.md). |

## What the page writes into the data store

The store is made at [L478](../../public/simulations/driven-oscillator.html#L478):
`Sim.dataset({ title: 'Driven oscillator', attrs: { figure: 9, page, equation, start } })`. It has two dimensions,
`n` = 6 001 stored rows ([L497](../../public/simulations/driven-oscillator.html#L497)) and `b` = 241 Bode frequencies
([L539](../../public/simulations/driven-oscillator.html#L539)), and 62 variables: 49 scalars and 13 `Float64Array`s, all
declared at [L479–L542](../../public/simulations/driven-oscillator.html#L479-L542) (counted in the live store). The shared
store itself is described in [dataset.md](../scripts/dataset.md). Each variable carries `symbol`, `units`, `long_name`,
`computed_in`, often `formula`, and `digits`. Listed by the panel groups of
[L972–L980](../../public/simulations/driven-oscillator.html#L972-L980):

| Group | Variables | Written at |
|---|---|---|
| Parameters | `m`, `f0`, `zeta`, `F0`, `fd` | [L604](../../public/simulations/driven-oscillator.html#L604) (in `solve()`, so they are the values of the last solve) |
| Derived physics | `omega0`, `k`, `c`, `Omega`, `tau`, `Q`; `X`, `phi`, `fr`; `G_drive`; `phi_deg` | [L605](../../public/simulations/driven-oscillator.html#L605), [L606](../../public/simulations/driven-oscillator.html#L606), [L608](../../public/simulations/driven-oscillator.html#L608), [L609](../../public/simulations/driven-oscillator.html#L609) |
| Solver | `h`, `steps`, `err_max`, `Xm`; `Gm_drive`; `Win`, `Wloss`; `balance`; `solve_ms`, `stale` | [L607](../../public/simulations/driven-oscillator.html#L607), [L609–L612](../../public/simulations/driven-oscillator.html#L609-L612); `stale` also in `markStale()` [L635](../../public/simulations/driven-oscillator.html#L635) |
| Stored run (dim `n`) | `ts` (coordinate), `xs`, `vs`, `Fs`, `Es`, `Pin`, `Ploss`; `xex`; `xqs`, `ph` | [L573–L574](../../public/simulations/driven-oscillator.html#L573-L574); [L592](../../public/simulations/driven-oscillator.html#L592); [L599–L600](../../public/simulations/driven-oscillator.html#L599-L600) |
| Playback | `i_now`, `t_play`, `x_now`, `v_now`, `F_now`, `E_now`, `Pin_now`, `ph_now` | `frame()`, [L902–L904](../../public/simulations/driven-oscillator.html#L902-L904) |
| Bode plot (dim `b`) | `fb` (coordinate), `Gmag`, `Gphase` | `bode()`, [L625–L627](../../public/simulations/driven-oscillator.html#L625-L627) |
| Drawing | `xmax`, `ylim` | [L607](../../public/simulations/driven-oscillator.html#L607) |
| | `win_T`, `win_t0`; `px_per_m`, `amp_px`, `eq_px`, `block_px`, `block_y`, `Fmax_px`, `F_px`, `box_w`, `box_h` | `draw()`, [L832](../../public/simulations/driven-oscillator.html#L832), [L836–L837](../../public/simulations/driven-oscillator.html#L836-L837) |
| | `fps`, `playing` | clock tick, [L914](../../public/simulations/driven-oscillator.html#L914) |

The `*_now` scalars are copies of row `i_now`, so a recorded round has scalar columns to follow.
`Sim.data.colour` shades the `xs` and `Fs` table cells with `Sim.colourMap`
([L981](../../public/simulations/driven-oscillator.html#L981), defined in
[datalog.js:67](../../public/scripts/datalog.js#L67)); this is presentation only.

**One round** (`Sim.data.round`, [L1093–L1095](../../public/simulations/driven-oscillator.html#L1093-L1095)) is one drive
period, $1/f$ seconds of the stored run, timed by `t_play`. Its columns are `x_now`, `v_now`, `F_now`, `E_now`, `Pin_now`;
the default point is the block. Recording is refused when fewer than $1/f$ seconds of the run remain ("press From t = 0").
The panel samples every frame of the round, at most 600 samples ([datalog.js:743](../../public/scripts/datalog.js#L743)).

**`Sim.live()`** ([L888–L897](../../public/simulations/driven-oscillator.html#L888-L897)) returns formatted strings read from
the store, for the keys the walkthrough uses: `k`, `c`, `W`, `w0`, `h`, `steps`, `n`, `t`, `x`, `v`, `F`, `E`, `X`, `phi`,
`err`, `Win`, `Wloss`, `bal`, `bx`, `sc`. The walkthrough polls it every 200 ms
([sim.js:400](../../public/scripts/sim.js#L400)).

**Check and read-back.** `Sim.data.check` ([L1004–L1051](../../public/simulations/driven-oscillator.html#L1004-L1051))
recomputes every stored value from its stored inputs; for the ODE solution (`xs`, `vs`) and the run integrals (`Win`,
`Wloss`) it reruns the same RK4 from $t = 0$ (`rk4Replay`, up to 60 000 steps). `Sim.data.drawn`
([L1052–L1092](../../public/simulations/driven-oscillator.html#L1052-L1092)) reads pixels back: the burgundy block, the
force arrow (or its absence below 2 px), the dial arm, $x_n$ and $F_n/k$ on the charts, and the Bode curves and dots.
`probe` ([L982–L991](../../public/simulations/driven-oscillator.html#L982-L991)) pins the block when the click is within
40 px across and 34 px up or down of its centre, otherwise the nearest stored sample within 16 px (outside the window chart
only every fifth sample is tried). How the panel uses these hooks is in [datalog.md](../scripts/datalog.md).

## Page structure

**Head** ([L3–L25](../../public/simulations/driven-oscillator.html#L3-L25)): title "Driven Oscillator · Numa Koudsie",
description, preconnect to Google Fonts, then the stylesheets `../styles/sim.css`, `../styles/data.css`,
`../styles/fold.css` ([L11–L13](../../public/simulations/driven-oscillator.html#L11-L13)), an inline SVG favicon, and a
small inline style for the solve box (`.solve`, `.solve__steps`, `.solve__status`, `.seek`,
[L15–L24](../../public/simulations/driven-oscillator.html#L15-L24)). Styles are described in [styles.md](../styles.md).

**Body**, in order:
- `header.sim-top` with the back link and the hand-written Fig. 1–10 links, Fig. 9 marked `aria-current`
  ([L27–L42](../../public/simulations/driven-oscillator.html#L27-L42));
- `.sim__head`: "Fig. 9 · control systems · forced oscillations", the `h1` and the lede
  ([L46–L50](../../public/simulations/driven-oscillator.html#L46-L50));
- `.sim__grid`: the main figure `#stage` with `canvas#osc` and a caption holding the equation and `#cap-t`
  ([L54–L62](../../public/simulations/driven-oscillator.html#L54-L62)); the Bode figure `#stage-bode` with `canvas#bode` and
  `#cap-res` ([L63–L71](../../public/simulations/driven-oscillator.html#L63-L71)); the control panel `aside.panel` with the
  solve box, the sliders, six readouts and a legend ([L74–L137](../../public/simulations/driven-oscillator.html#L74-L137)).
  The **Read values** switch is added to the first caption by datalog.js;
- `article.paper#paper`, the lecture note ([L140–L452](../../public/simulations/driven-oscillator.html#L140-L452)):
  abstract; ten sections `.psec` — 01 A push from outside, 02 The model, 03 The exact solution ★ (3.1 The steady state,
  3.2 The transient), 04 Resonance and phase, 05 The control engineer's view ★, 06 The start: beats and decay, 07 Where the
  energy goes, 08 Solve first, then play, 09 On screen, 10 What the model leaves out (10.1 Further reading). Eight numbered
  equations, `\tag{1}`–`\tag{8}`. Four figures with five inline SVGs: Figure 1 the plant sketch
  ([L169–L198](../../public/simulations/driven-oscillator.html#L169-L198)), Figure 2 amplitude and phase against $f/f_0$ for
  four damping ratios (two SVGs, [L228–L316](../../public/simulations/driven-oscillator.html#L228-L316)), Figure 3 the block
  diagram ([L333–L351](../../public/simulations/driven-oscillator.html#L333-L351)), Figure 4 the default run
  ([L357–L405](../../public/simulations/driven-oscillator.html#L357-L405)). Two exercise boxes, 4.1 and 6.1;
- `section#walk` with `data-walk="driven"` ([L454](../../public/simulations/driven-oscillator.html#L454)), filled by
  `sim.js` from `walk/driven.js` ([sim.js:476–486](../../public/scripts/sim.js#L476-L486)); see [walk.md](../scripts/walk.md);
- footer; then the scripts in load order: `fold.js`, `sim.js`, `dataset.js`, the page's inline script, `datalog.js`
  ([L462–L1106](../../public/simulations/driven-oscillator.html#L462-L1106)). Folds are described in
  [fold.md](../scripts/fold.md), the shared helpers in [sim.md](../scripts/sim.md).

The walkthrough's seven steps quote these page lines: step 1 [L567](../../public/simulations/driven-oscillator.html#L567);
step 2 [L562–L564](../../public/simulations/driven-oscillator.html#L562-L564); step 3
[L579–L582](../../public/simulations/driven-oscillator.html#L579-L582) and
[L586–L587](../../public/simulations/driven-oscillator.html#L586-L587); step 4
[L572–L576](../../public/simulations/driven-oscillator.html#L572-L576); step 5
[L584–L585](../../public/simulations/driven-oscillator.html#L584-L585) and
[L611](../../public/simulations/driven-oscillator.html#L611); step 6
[L553–L554](../../public/simulations/driven-oscillator.html#L553-L554) and
[L593](../../public/simulations/driven-oscillator.html#L593); step 7
[L912](../../public/simulations/driven-oscillator.html#L912), [L900](../../public/simulations/driven-oscillator.html#L900),
[L834](../../public/simulations/driven-oscillator.html#L834). All seven excerpts match the page text at present.

## Where the drawing and the store differ

The page states the differences in `Sim.data.about` ([L1097](../../public/simulations/driven-oscillator.html#L1097)), which
the data panel prints. In detail:

- **Nearest row, no interpolation.** `t_play` runs continuously, but the picture shows row
  $\operatorname{round}(t_\text{play}/10\,\text{ms})$ ([L900](../../public/simulations/driven-oscillator.html#L900)). The
  caption shows the row's time `ts[i]`, not `t_play` ([L906](../../public/simulations/driven-oscillator.html#L906)).
- **Overview strip thinned.** The strip of the whole run draws every `stride`-th row,
  `stride = max(1, floor(NS / (2 × strip width)))` ([L811](../../public/simulations/driven-oscillator.html#L811)): every 4th
  row at a 770 px canvas, every 10th at 356 px. The window chart draws every row between its edges
  ([L770](../../public/simulations/driven-oscillator.html#L770)).
- **Drawing scale changes with the run.** The block travels at most `amp = 0.11 × W0` pixels either side of rest, where
  `W0` is the width between wall and right margin, so `px_per_m = amp / xmax` differs from run to run
  ([L669](../../public/simulations/driven-oscillator.html#L669), [L672](../../public/simulations/driven-oscillator.html#L672)).
  The ruler under the floor shows $\pm$`xmax` in metres ([L753](../../public/simulations/driven-oscillator.html#L753)).
- **Force arrow.** Its length is $F_n/F_0 \cdot L_F$ with $L_F = \min(88, 0.12\,w)$ px; arrows shorter than 2 px are not
  drawn ([L744](../../public/simulations/driven-oscillator.html#L744)).
- **Dial.** The arm points at the stored $\Omega t_n \bmod 2\pi$ ([L758](../../public/simulations/driven-oscillator.html#L758)).
- **Bode plot.** The dot sits at the exact $|G(i\Omega)|$ and $\varphi$; the ring is the amplitude measured from the last
  10 s of the stored run, per newton ([L880–L882](../../public/simulations/driven-oscillator.html#L880-L882)). With the
  defaults they differ by 0.03 % (0.48194 against 0.48209 m/N), the remains of the transient.
- **Rounding.** Canvas labels and readouts round (for example $F$ to 2 decimals, $x$ to 3); the store keeps full doubles.

## How to change it safely

- **Run length, step and storage stride.** `TEND`, `H` and `EVERY` ([L469](../../public/simulations/driven-oscillator.html#L469))
  determine `NS`. Keep `TEND / H` and `TEND / H / EVERY` whole numbers, because `step === TEND / H` and `step % EVERY` decide
  the last row ([L571–L577](../../public/simulations/driven-oscillator.html#L571-L577)). These places repeat the numbers by
  hand and must change with them: the seek slider `max="6000"` ([L90](../../public/simulations/driven-oscillator.html#L90));
  the `formula` texts "n · 10 h", "t_n ≥ 50 s", "round(t_play / 10h)" ([L498](../../public/simulations/driven-oscillator.html#L498),
  [L513](../../public/simulations/driven-oscillator.html#L513), [L517](../../public/simulations/driven-oscillator.html#L517));
  the group note "every 10 ms of the 60 s" ([L976](../../public/simulations/driven-oscillator.html#L976)); the check text
  "at most 6000" ([L1039](../../public/simulations/driven-oscillator.html#L1039)); the 10 s tick step of the overview
  ([L826](../../public/simulations/driven-oscillator.html#L826)); the walkthrough's "step / 10", "60 000 steps" and
  "6 001 rows" ([driven.js:57–58](../../public/scripts/walk/driven.js#L57-L58)); the lecture note section 8
  ([L423–L425](../../public/simulations/driven-oscillator.html#L423-L425)) and `about`.
- **The integrator exists twice.** `solve()` ([L579–L588](../../public/simulations/driven-oscillator.html#L579-L588)) and
  `rk4Replay()` ([L937–L946](../../public/simulations/driven-oscillator.html#L937-L946)) must stay identical, line for line,
  or the data panel's Check of `xs`, `vs`, `Win` and `Wloss` will no longer agree with the store.
- **Walkthrough excerpts.** The seven excerpts listed under Page structure are quoted verbatim in `walk/driven.js`. If one
  of those page lines changes, change the excerpt in the same edit. Insert new code after a quoted line, never inside a
  quoted group (AGENTS.md).
- **Taps stay where values are computed.** Write a new number into the store at the line that computes it, declare it with
  `ds.var` next to its relatives, add it to a group in `Sim.data.groups`, and give it a `check` (and a `drawn` if it is on
  screen). Do not compute numbers inside `draw*()` beyond the metre-to-pixel conversion.
- **Lecture-note numbers.** Sections 2–8 quote values for the default sliders ([L102–L118](../../public/simulations/driven-oscillator.html#L102-L118)),
  and Figures 2 and 4 are static SVGs computed from the page's formulas. Changing a default or the physics means
  recomputing them.
- **Damping limit.** `exact()` divides by $\omega_d = \omega_0\sqrt{1-\zeta^2}$; the slider stops at 0.9. Allowing
  $\zeta \ge 1$ needs a different exact solution (section 10 says so, [L441](../../public/simulations/driven-oscillator.html#L441)).
- **Frequency range.** The Bode axis covers 0.05–2 Hz ([L624](../../public/simulations/driven-oscillator.html#L624),
  [L852](../../public/simulations/driven-oscillator.html#L852)); raising the $f_0$ or $f$ slider beyond 2 Hz would put the
  marks outside it.
- **Re-test** in a browser at a wide and a phone-width window: no console error; status line after load; readouts with the
  defaults ($X$ = 0.482 m, error about $5\times10^{-12}$ m, balance about $10^{-12}$); move a slider and see the stale
  status; Solve; drag **Stored run**; open the Data panel, Check `xs` at a row, `Win`, `balance`, and a `drawn` value; switch
  on **Read values** and pin the block; record one round.

## Notes for maintainers

1. **Figure 2 of the lecture note has wrong axis labels.** The horizontal axis of both SVGs runs from $f/f_0 = 0.1$ to 10
   on a log scale (the drawn curves give $X/(F_0/k) = 1.01$ at the left edge and 0.0101 at the right edge, as equation (4)
   does for $\zeta = 0.05$ at $f/f_0 = 0.1$ and 10), but the tick labels read "−1.00, −0.50, 1, 0.50, 1.00"
   ([L241–L249](../../public/simulations/driven-oscillator.html#L241-L249),
   [L285–L293](../../public/simulations/driven-oscillator.html#L285-L293)). They should read 0.1, 0.32, 1, 3.2, 10.
2. **Phase lag rounded wrongly in the note.** Sections 3 and 6 give $\varphi = 25.4°$
   ([L222](../../public/simulations/driven-oscillator.html#L222), [L404](../../public/simulations/driven-oscillator.html#L404));
   the store holds 25.346° and the readout shows 25.3°.
3. **Section 9 does not match the drawing code.** It says the rest position is at 40 % of the width and the largest
   displacement spans 27 % ([L432](../../public/simulations/driven-oscillator.html#L432)). The code puts rest at
   `wallX + 0.42 W0 + bw/2` and allows `0.11 W0` either side ([L669–L671](../../public/simulations/driven-oscillator.html#L669-L671));
   measured: rest at 47.8 % and span 20.1 % of a 770 px canvas, 50.0 % and 19.4 % of a 356 px canvas. The store's own
   description of `amp_px` ([L527](../../public/simulations/driven-oscillator.html#L527)) matches the code.
4. **Small recomputations for display.** `readouts()` and `Sim.live()` convert `phi` to degrees
   ([L649](../../public/simulations/driven-oscillator.html#L649), [L893](../../public/simulations/driven-oscillator.html#L893))
   although `phi_deg` is stored ([L609](../../public/simulations/driven-oscillator.html#L609)). The values agree; the house
   rule is that the display only reads.
5. **Dead code.** `frames` is counted ([L911](../../public/simulations/driven-oscillator.html#L911)) but never read.
   In `label()`, `sw = 0;` is overwritten on the next statement ([L703–L704](../../public/simulations/driven-oscillator.html#L703-L704)).
6. **Redraw while paused.** The clock calls the tick on every animation frame with $\Delta t = 0$ while paused
   ([sim.js:179–186](../../public/scripts/sim.js#L179-L186)), and the tick always calls `frame()`
   ([L916](../../public/simulations/driven-oscillator.html#L916)), so a paused page still redraws about 60 times a second
   (about 1.5 ms per frame measured) and rewrites `#cap-t` each time ([L906](../../public/simulations/driven-oscillator.html#L906)).
7. **Solve time.** Section 8 says solving "takes a few tens of milliseconds"
   ([L423](../../public/simulations/driven-oscillator.html#L423)); measured here 6–17 ms (machine dependent).
8. **AGENTS.md** says the load order dataset.js → page → datalog.js holds for "all eight figures" (AGENTS.md line 64);
   this page (Fig. 9) follows it too, so the count is out of date.
