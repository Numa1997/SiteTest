# Fig. 9 · Driven Oscillator

| | |
|---|---|
| Page | [public/simulations/driven-oscillator.html](../../public/simulations/driven-oscillator.html) (1 113 lines, 183 071 bytes) |
| Walkthrough | [public/scripts/walk/driven.js](../../public/scripts/walk/driven.js) (121 lines, 7 steps, key `driven`) |
| Thumbnail | [public/images/sims/driven-oscillator.webp](../../public/images/sims/driven-oscillator.webp) (WebP, 800 × 500 px, 23.7 kB) |
| Catalog entry | [public/scripts/catalog.js#L183](../../public/scripts/catalog.js#L183-L199) (`id: 'driven-oscillator'`, `fig: 9`, `field: 'control'`, `stage: 1`, lines 183–199) |

A block of mass 1 kg sits on a spring and a damper and is pushed by a force $F_0\cos\Omega t$ that does not care where the
block is. The reader sets the natural frequency, the damping ratio, the force amplitude and the drive frequency, presses
**Solve**, and watches the stored run play back: the block, the force arrow, a turning dial for the driver, a moving window
chart of $x(t)$, a strip of the whole 60 s run, and a Bode plot with the present drive marked. The page never integrates
while the reader watches. It solves the whole run first with the classical fourth-order Runge–Kutta method (RK4), writes
every sample into its dataset, and each frame then draws one stored row.

In this page, a link such as [L571](../../public/simulations/driven-oscillator.html#L571) points to a line of
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
equation of motion ([L571](../../public/simulations/driven-oscillator.html#L571)):

$$\omega_0 = 2\pi f_0,\qquad k = m\,\omega_0^2,\qquad c = 2\zeta m\,\omega_0,\qquad \Omega = 2\pi f .$$

The right-hand side of the ODE is `accel()` ([L566–L568](../../public/simulations/driven-oscillator.html#L566-L568)):

$$\dot x = v,\qquad \dot v = a(t, x, v) = \frac{F_0\cos\Omega t - c\,v - k\,x}{m} .$$

Along the run the page also integrates the work of the driver and the heat of the damper
([L588–L589](../../public/simulations/driven-oscillator.html#L588-L589)) and stores the energy and the two powers at each
sample ([L578](../../public/simulations/driven-oscillator.html#L578)):

$$W_\text{in} = \int_0^T F v\,\mathrm dt,\quad W_\text{loss} = \int_0^T c\,v^2\,\mathrm dt,\quad E = \tfrac12 m v^2 + \tfrac12 k x^2,\quad P_\text{in} = F v,\quad P_\text{loss} = c v^2 .$$

The exact solution is used only to grade the numbers, never to draw them. `steady()`
([L556–L559](../../public/simulations/driven-oscillator.html#L556-L559)) gives the steady amplitude and phase lag, and
`exact()` ([L560–L563](../../public/simulations/driven-oscillator.html#L560-L563)) adds the transient that starts the block
from rest:

$$X = \frac{F_0/m}{\sqrt{(\omega_0^2-\Omega^2)^2 + (2\zeta\omega_0\Omega)^2}},\qquad \varphi = \operatorname{atan2}(2\zeta\omega_0\Omega,\ \omega_0^2-\Omega^2),$$

$$x_\text{exact}(t) = X\cos(\Omega t-\varphi) + e^{-\zeta\omega_0 t}\left(C_1\cos\omega_d t + C_2\sin\omega_d t\right),\quad C_1 = -X\cos\varphi,\quad C_2 = \frac{\zeta\omega_0 C_1 - X\Omega\sin\varphi}{\omega_d},\quad \omega_d = \omega_0\sqrt{1-\zeta^2}.$$

Further derived numbers ([L609–L615](../../public/simulations/driven-oscillator.html#L609-L615)): $\tau = 1/(\zeta\omega_0)$,
$Q = 1/(2\zeta)$, $f_r = f_0\sqrt{1-2\zeta^2}$ when $\zeta < 1/\sqrt2$ (else 0), $|G(i\Omega)| = X/F_0$, and the energy balance
$|E(T)-E(0)-(W_\text{in}-W_\text{loss})|/W_\text{in}$. The Bode plot evaluates $|G(i\Omega)| = 1/(m\sqrt{(\omega_0^2-\Omega^2)^2+(2\zeta\omega_0\Omega)^2})$
and $\varphi(\Omega)$ in degrees at 241 frequencies $f_j = 0.05\cdot 40^{j/240}$ Hz, from 0.05 to 2 Hz
([L627–L632](../../public/simulations/driven-oscillator.html#L627-L632)).

| Symbol | Meaning | Unit | In code |
|---|---|---|---|
| $m$ | mass, fixed at 1 | kg | `M` ([L473](../../public/simulations/driven-oscillator.html#L473)) |
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

One line fixes the run ([L473](../../public/simulations/driven-oscillator.html#L473)):
`M = 1` kg, `H = 0.001` s, `TEND = 60` s, `EVERY = 10`, and `NS = TEND / H / EVERY + 1`. In JavaScript `60 / 0.001` is
exactly 60 000, so `NS` is exactly 6 001 (checked in Node). The page keeps four pieces of its own state
([L479](../../public/simulations/driven-oscillator.html#L479)): `playT` (playback time, s), `iNow` (row on screen),
`fps` and `solved` (the slider values of the last solve, or `null`).

### 1 Solve: classical RK4 over the whole run

`solve()` ([L569–L622](../../public/simulations/driven-oscillator.html#L569-L622)) works on the state vector
$s = (x, v)$ with the slope $f(t, s) = (v,\ a(t, x, v))$. It starts from rest, $x = v = 0$ at $t = 0$
([L574](../../public/simulations/driven-oscillator.html#L574)). One step of size $h$ samples the slope four times: at the
start, twice at the middle and at the end ([L583–L586](../../public/simulations/driven-oscillator.html#L583-L586)):

$$k_1 = f(t, s),\quad k_2 = f(t+\tfrac h2, s+\tfrac h2 k_1),\quad k_3 = f(t+\tfrac h2, s+\tfrac h2 k_2),\quad k_4 = f(t+h, s+h k_3),$$
$$s(t+h) = s + \tfrac h6\,(k_1 + 2k_2 + 2k_3 + k_4) .$$

In the code the $x$-components of the slopes are the velocities `v, v2, v3, v4` and the $v$-components are the
accelerations `a1 … a4`; the update is [L590–L591](../../public/simulations/driven-oscillator.html#L590-L591). The two
work integrals are quadratures (their slopes do not feed back), carried with the same RK4 weights and the same stage
velocities, with the force evaluated at $t$, $t+h/2$ and $t+h$
([L587–L589](../../public/simulations/driven-oscillator.html#L587-L589)). Time is set from the step count,
`t = (step + 1) * H` ([L592](../../public/simulations/driven-oscillator.html#L592)), so it does not collect round-off by
repeated addition.

Why RK4 with $h = 1$ ms: the code does not state the reason. What can be measured is the margin. The fastest natural motion
allowed by the sliders is $\omega_0 = 2\pi\cdot1.5 = 9.42$ rad/s, so $\omega_0 h \le 0.0094$ rad per step, deep inside the
region where RK4 is stable and its error per step scales as $(\omega_0 h)^5$. With the defaults the largest difference to
the exact solution over the run is $5.26\times10^{-12}$ m and the energy balance holds to $1.27\times10^{-12}$ (measured).

### 2 Store: every tenth state

The loop runs `step = 0 … 60 000` ([L575](../../public/simulations/driven-oscillator.html#L575)). At the top of each pass,
before the step, every tenth state is written straight into the dataset arrays
([L576–L580](../../public/simulations/driven-oscillator.html#L576-L580)): `ts`, `xs`, `vs`, `Fs`, `Es`, `Pin`, `Ploss`. So
row $n$ holds the state at exactly $t_n = n\cdot 10h = n \cdot 10$ ms. After storing step 60 000 the loop stops without a
further step ([L581](../../public/simulations/driven-oscillator.html#L581)): 60 000 RK4 steps, 6 001 rows.

Two passes over the stored rows follow. The first ([L594–L600](../../public/simulations/driven-oscillator.html#L594-L600))
fills `xex` with the exact solution and finds the largest error `err`, the largest $|x|$ (`xmax`, which sets the drawing
scale) and the largest $|x|$ for $t_n \ge 50$ s (`Xm`, "Measured, last 10 s"). The second
([L601–L606](../../public/simulations/driven-oscillator.html#L601-L606)) fills `xqs` $= F_n/k$, the drive phase
`ph` $= \Omega t_n \bmod 2\pi$ and the chart half-height `ylim`. Then the arrays are marked changed
([L607](../../public/simulations/driven-oscillator.html#L607)) and every scalar is written
([L608–L616](../../public/simulations/driven-oscillator.html#L608-L616)).

The arrays come from `ds.alloc(name)` ([L572–L573](../../public/simulations/driven-oscillator.html#L572-L573)), which
allocates a new typed array only when the length changes ([dataset.js:67](../../public/scripts/dataset.js#L67)); a re-solve
overwrites the same `Float64Array`s in place. Memory, measured from the live store: 10 arrays × 6 001 × 8 B = 480 080 B for
the run, plus 3 × 241 × 8 B = 5 784 B for the Bode curves, 485 864 B in all. One solve took 6–17 ms in headless Chromium
(`solve_ms`, measured with `performance.now()` at [L570](../../public/simulations/driven-oscillator.html#L570) and
[L616](../../public/simulations/driven-oscillator.html#L616)).

Last, `solve()` records the settings it used in `solved` ([L617](../../public/simulations/driven-oscillator.html#L617)),
recomputes the Bode curves (`bode()`, [L624–L635](../../public/simulations/driven-oscillator.html#L624-L635)), rewrites the
readouts, sets `playT = 0` and starts the clock ([L618–L621](../../public/simulations/driven-oscillator.html#L618-L621)).

### When the run is solved again

Only twice: once at load ([L1104](../../public/simulations/driven-oscillator.html#L1104)) and whenever **Solve** is pressed
([L923](../../public/simulations/driven-oscillator.html#L923)). A slider only calls `markStale()`
([L548–L551](../../public/simulations/driven-oscillator.html#L548-L551),
[L637–L641](../../public/simulations/driven-oscillator.html#L637-L641)), which compares the four sliders with `solved`, sets
the `stale` flag and rewrites the status line in burgundy; the old run keeps playing, and its settings are named in the
status text ([L642–L649](../../public/simulations/driven-oscillator.html#L642-L649)).

### 3 Play: the frame loop, in order

`Sim.clock` ([sim.js:176–197](../../public/scripts/sim.js#L176-L197)) calls the page's tick on every
`requestAnimationFrame`, with $\Delta t$ capped at 0.05 s and $\Delta t = 0$ while paused. Each tick:

1. returns if nothing has been solved; updates the smoothed frame rate; advances `playT += speed · Δt`; at 60 s clamps and
   pauses; stores `fps` and `playing`; marks step "3 play" ([L913–L921](../../public/simulations/driven-oscillator.html#L913-L921));
2. `frame()` ([L903–L912](../../public/simulations/driven-oscillator.html#L903-L912)) picks the nearest stored row,
   $n = \operatorname{round}(t_\text{play}/10\,\text{ms})$ clamped to 0 … 6 000, writes `i_now`, `t_play` and the six
   `*_now` copies of row $n$ into the store, moves the **Stored run** slider and the caption time, then calls `draw()`;
3. `draw()` ([L833–L846](../../public/simulations/driven-oscillator.html#L833-L846)) sets the window width
   $T_w = \text{clamp}(4/f, 6, 20)$ s and its left edge $t_0 = \text{clamp}(t_n - 0.7T_w, 0, 60 - T_w)$, gets the layout
   from `geom()`, turns $x_n$ into the block position `bx = eqX + xs[i] * sc` and $F_n$ into the arrow length, stores these
   pixel values, clears the canvas and draws `drawMechanism`, `drawWindow` and `drawOverview` in that order.

Nothing in this chain integrates; the only arithmetic turns metres, seconds and newtons into pixels. Because the clock calls
the tick every animation frame even while paused (with $\Delta t = 0$), the figure is redrawn at the display rate in both
states; one `frame()` took about 1.5 ms (measured over 200 seek events at a 1 440 px wide window).

### Precomputation and caching

- The Bode canvas is not redrawn per frame: only after a solve ([L634](../../public/simulations/driven-oscillator.html#L634)),
  on resize ([L1106](../../public/simulations/driven-oscillator.html#L1106)) and when fonts are ready
  ([L1107](../../public/simulations/driven-oscillator.html#L1107)).
- `geom()` ([L663–L686](../../public/simulations/driven-oscillator.html#L663-L686)) is recomputed on every call; it reads
  `xmax`, `win_t0`, `win_T` and `ylim` from the store, so `draw()` must store the window before calling it
  ([L836–L837](../../public/simulations/driven-oscillator.html#L836-L837)).
- For the data panel's Check of $W_\text{in}$ and $W_\text{loss}$, `fullReplay()` reruns the whole 60 s once and caches the
  result under a key made of the four settings ([L954–L960](../../public/simulations/driven-oscillator.html#L954-L960)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `steady(w0, z, W, F)` | [556–559](../../public/simulations/driven-oscillator.html#L556-L559) | Exact steady amplitude $X$ and phase lag $\varphi$, equation (4) of the note. |
| `exact(t, w0, z, W, st)` | [560–563](../../public/simulations/driven-oscillator.html#L560-L563) | Exact $x(t)$ from rest, equation (5); used only to measure the RK4 error. |
| `accel(t, x, v, p)` | [566–568](../../public/simulations/driven-oscillator.html#L566-L568) | Right-hand side: $(F_0\cos\Omega t - cv - kx)/m$. |
| `solve()` | [569–622](../../public/simulations/driven-oscillator.html#L569-L622) | Solve and store the whole run (see above). |
| `bode()` | [624–635](../../public/simulations/driven-oscillator.html#L624-L635) | Fills `fb`, `Gmag`, `Gphase` (241 points) and redraws the Bode plot. |
| `markStale()` | [637–641](../../public/simulations/driven-oscillator.html#L637-L641) | Sets `stale` when a slider differs from the last solve. |
| `status()` | [642–649](../../public/simulations/driven-oscillator.html#L642-L649) | Writes the status line and the "1 solve / 2 store" marks. |
| `readouts()` | [650–659](../../public/simulations/driven-oscillator.html#L650-L659) | Writes the six readouts and the Bode caption $f_r$. |
| `geom()` | [663–686](../../public/simulations/driven-oscillator.html#L663-L686) | Layout from canvas size and store: mechanism, window chart, overview strip, dial; mapping functions `wx`, `wy`, `ox`, `oy`, `inWin`. |
| `arrow(c, …)` | [687–695](../../public/simulations/driven-oscillator.html#L687-L695) | Draws a straight arrow with a filled head. |
| `spring(c, …)` | [696–702](../../public/simulations/driven-oscillator.html#L696-L702) | Draws a zigzag spring. |
| `label(c, sym, value, …)` | [703–713](../../public/simulations/driven-oscillator.html#L703-L713) | A symbol in Latin Modern via `Sim.tex`, then its value in IBM Plex Mono. |
| `drawMechanism(c, g, i, bx, fpx)` | [714–771](../../public/simulations/driven-oscillator.html#L714-L771) | Wall, floor, rest line, spring, damper, block on wheels, force arrow, ruler with $x$, driver dial. |
| `drawWindow(c, g, i)` | [772–812](../../public/simulations/driven-oscillator.html#L772-L812) | Window chart: ticks, $\pm X$, $F/k$, $x$ faint ahead and dark behind, cursor, key. |
| `drawOverview(c, g, i)` | [813–832](../../public/simulations/driven-oscillator.html#L813-L832) | Strip of the whole run with the window band shaded. |
| `draw()` | [833–846](../../public/simulations/driven-oscillator.html#L833-L846) | One frame of the main canvas. |
| `bodeGeom()` | [848–859](../../public/simulations/driven-oscillator.html#L848-L859) | Bode layout: two panels side by side (stacked below 560 px), log $f$ axis 0.05–2 Hz, three decades of $\lvert G\rvert$, 0–180°. |
| `drawBode()` | [860–889](../../public/simulations/driven-oscillator.html#L860-L889) | Draws both panels, the $f_0$ line, the curves, the dot at the exact value and the ring at the measured one. |
| `Sim.live()` | [892–901](../../public/simulations/driven-oscillator.html#L892-L901) | Formatted store values for the walkthrough's "Now" column. |
| `frame()` | [903–912](../../public/simulations/driven-oscillator.html#L903-L912) | Picks the stored row for `playT`, copies it to the `*_now` scalars, draws. |
| clock tick (anonymous) | [913–921](../../public/simulations/driven-oscillator.html#L913-L921) | Advances `playT`, stops at 60 s, calls `frame()`. |
| `chartPos(n)`, `chartPosQ(n)` | [927–934](../../public/simulations/driven-oscillator.html#L927-L934) | Screen point of $x_n$ (or $F_n/k$) on the window chart, else on the overview strip. |
| `rk4Replay(n)` | [935–953](../../public/simulations/driven-oscillator.html#L935-L953) | The same RK4 rerun from $t=0$ to row $n$; the Check of `xs`, `vs`, `Win`, `Wloss`. |
| `fullReplay()` | [954–960](../../public/simulations/driven-oscillator.html#L954-L960) | Cached `rk4Replay(6000)`. |
| `sliderCheck`, `at`, `neutralInk`, `readBack` | [961–967](../../public/simulations/driven-oscillator.html#L961-L967) | Small helpers for the data panel's Check (slider value, row on screen, dark-ink test, pixel read-back). |
| `blockPixel()` | [968–972](../../public/simulations/driven-oscillator.html#L968-L972) | Reads back a pixel inside the burgundy block. |
| `Sim.data` (object) | [973–1102](../../public/simulations/driven-oscillator.html#L973-L1102) | The data-panel contract: groups, colours, `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `about`. |
| start-up | [1104–1107](../../public/simulations/driven-oscillator.html#L1104-L1107) | `solve()`, resize observers, redraw when fonts are ready. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Solve | `solve` | button | Calls `solve()` ([L923](../../public/simulations/driven-oscillator.html#L923)). |
| Pause / Play | `play` | button | Toggles the clock via `Sim.playButton` ([L922](../../public/simulations/driven-oscillator.html#L922), [sim.js:199](../../public/scripts/sim.js#L199)). |
| From t = 0 | `restart` | button | `playT = 0` and play ([L924](../../public/simulations/driven-oscillator.html#L924)). |
| Stored run | `seek` | 0–6000, step 1, default 0 ([L90](../../public/simulations/driven-oscillator.html#L90)) | Sets `playT = n · 10 ms` and draws ([L553](../../public/simulations/driven-oscillator.html#L553)); follows the playback ([L909](../../public/simulations/driven-oscillator.html#L909)). |
| Playback speed | `speed` | 0.25–4, step 0.25, default 1 ([L94](../../public/simulations/driven-oscillator.html#L94)) | Multiplies $\Delta t$ ([L916](../../public/simulations/driven-oscillator.html#L916)). Does not mark the run stale. |
| Natural frequency $f_0$ | `f0` | 0.2–1.5 Hz, step 0.01, default 0.5 ([L102](../../public/simulations/driven-oscillator.html#L102)) | $\omega_0$, $k$, $c$ at the next solve ([L571](../../public/simulations/driven-oscillator.html#L571)); marks stale. |
| Damping ratio $\zeta$ | `zeta` | 0.01–0.9, step 0.01, default 0.05 ([L106](../../public/simulations/driven-oscillator.html#L106)) | $c$ at the next solve; marks stale. The maximum 0.9 keeps $\omega_d$ real in `exact()`. |
| Force amplitude $F_0$ | `F0` | 0–5 N, step 0.1, default 1 ([L114](../../public/simulations/driven-oscillator.html#L114)) | `p.F0`; marks stale. At 0 the arrow is hidden and `Gm_drive` is NaN ([L613](../../public/simulations/driven-oscillator.html#L613)). |
| Drive frequency $f$ | `fd` | 0.05–1.5 Hz, step 0.01, default 0.45 ([L118](../../public/simulations/driven-oscillator.html#L118)) | $\Omega$ at the next solve; marks stale. |
| Read values | added by datalog.js | switch, off | Appended to the first figure caption ([datalog.js:588–590](../../public/scripts/datalog.js#L588-L590)); see [datalog.md](../scripts/datalog.md). |

## What the page writes into the data store

The store is made at [L482](../../public/simulations/driven-oscillator.html#L482):
`Sim.dataset({ title: 'Driven oscillator', attrs: { figure: 9, page, equation, start } })`. It has two dimensions,
`n` = 6 001 stored rows ([L501](../../public/simulations/driven-oscillator.html#L501)) and `b` = 241 Bode frequencies
([L543](../../public/simulations/driven-oscillator.html#L543)), and 62 variables: 49 scalars and 13 `Float64Array`s, all
declared at [L483–L546](../../public/simulations/driven-oscillator.html#L483-L546) (counted in the live store). The shared
store itself is described in [dataset.md](../scripts/dataset.md). Each variable carries `symbol`, `units`, `long_name`,
`computed_in`, often `formula`, and `digits`. Listed by the panel groups of
[L976–L984](../../public/simulations/driven-oscillator.html#L976-L984):

| Group | Variables | Written at |
|---|---|---|
| Parameters | `m`, `f0`, `zeta`, `F0`, `fd` | [L608](../../public/simulations/driven-oscillator.html#L608) (in `solve()`, so they are the values of the last solve) |
| Derived physics | `omega0`, `k`, `c`, `Omega`, `tau`, `Q`; `X`, `phi`, `fr`; `G_drive`; `phi_deg` | [L609](../../public/simulations/driven-oscillator.html#L609), [L610](../../public/simulations/driven-oscillator.html#L610), [L612](../../public/simulations/driven-oscillator.html#L612), [L613](../../public/simulations/driven-oscillator.html#L613) |
| Solver | `h`, `steps`, `err_max`, `Xm`; `Gm_drive`; `Win`, `Wloss`; `balance`; `solve_ms`, `stale` | [L611](../../public/simulations/driven-oscillator.html#L611), [L613–L616](../../public/simulations/driven-oscillator.html#L613-L616); `stale` also in `markStale()` [L639](../../public/simulations/driven-oscillator.html#L639) |
| Stored run (dim `n`) | `ts` (coordinate), `xs`, `vs`, `Fs`, `Es`, `Pin`, `Ploss`; `xex`; `xqs`, `ph` | [L577–L578](../../public/simulations/driven-oscillator.html#L577-L578); [L596](../../public/simulations/driven-oscillator.html#L596); [L603–L604](../../public/simulations/driven-oscillator.html#L603-L604) |
| Playback | `i_now`, `t_play`, `x_now`, `v_now`, `F_now`, `E_now`, `Pin_now`, `ph_now` | `frame()`, [L906–L908](../../public/simulations/driven-oscillator.html#L906-L908) |
| Bode plot (dim `b`) | `fb` (coordinate), `Gmag`, `Gphase` | `bode()`, [L629–L631](../../public/simulations/driven-oscillator.html#L629-L631) |
| Drawing | `xmax`, `ylim` | [L611](../../public/simulations/driven-oscillator.html#L611) |
| | `win_T`, `win_t0`; `px_per_m`, `amp_px`, `eq_px`, `block_px`, `block_y`, `Fmax_px`, `F_px`, `box_w`, `box_h` | `draw()`, [L836](../../public/simulations/driven-oscillator.html#L836), [L840–L841](../../public/simulations/driven-oscillator.html#L840-L841) |
| | `fps`, `playing` | clock tick, [L918](../../public/simulations/driven-oscillator.html#L918) |

The `*_now` scalars are copies of row `i_now`, so a recorded round has scalar columns to follow.
`Sim.data.colour` shades the `xs` and `Fs` table cells with `Sim.colourMap`
([L985](../../public/simulations/driven-oscillator.html#L985), defined in
[datalog.js:71](../../public/scripts/datalog.js#L71)); this is presentation only.

**One round** (`Sim.data.round`, [L1097–L1099](../../public/simulations/driven-oscillator.html#L1097-L1099)) is one drive
period, $1/f$ seconds of the stored run, timed by `t_play`. Its columns are `x_now`, `v_now`, `F_now`, `E_now`, `Pin_now`;
the default point is the block. Recording is refused when fewer than $1/f$ seconds of the run remain ("press From t = 0").
The panel samples every frame of the round, at most 600 samples ([datalog.js:744](../../public/scripts/datalog.js#L744)).

**`Sim.live()`** ([L892–L901](../../public/simulations/driven-oscillator.html#L892-L901)) returns formatted strings read from
the store, for the keys the walkthrough uses: `k`, `c`, `W`, `w0`, `h`, `steps`, `n`, `t`, `x`, `v`, `F`, `E`, `X`, `phi`,
`err`, `Win`, `Wloss`, `bal`, `bx`, `sc`. The walkthrough polls it every 200 ms
([sim.js:326](../../public/scripts/sim.js#L326)).

**Check and read-back.** `Sim.data.check` ([L1008–L1055](../../public/simulations/driven-oscillator.html#L1008-L1055))
recomputes every stored value from its stored inputs; for the ODE solution (`xs`, `vs`) and the run integrals (`Win`,
`Wloss`) it reruns the same RK4 from $t = 0$ (`rk4Replay`, up to 60 000 steps). `Sim.data.drawn`
([L1056–L1096](../../public/simulations/driven-oscillator.html#L1056-L1096)) reads pixels back: the burgundy block, the
force arrow (or its absence below 2 px), the dial arm, $x_n$ and $F_n/k$ on the charts, and the Bode curves and dots.
`probe` ([L986–L995](../../public/simulations/driven-oscillator.html#L986-L995)) pins the block when the click is within
40 px across and 34 px up or down of its centre, otherwise the nearest stored sample within 16 px (outside the window chart
only every fifth sample is tried). How the panel uses these hooks is in [datalog.md](../scripts/datalog.md).

## Page structure

**Head** ([L3–L25](../../public/simulations/driven-oscillator.html#L3-L25)): title "Driven Oscillator · Numa Koudsie",
description, the security policy and referrer rule ([build-and-deploy.md](../build-and-deploy.md#security)), then the stylesheets `../styles/sim.css`, `../styles/data.css`,
`../styles/fold.css` ([L11–L13](../../public/simulations/driven-oscillator.html#L11-L13)), an inline SVG favicon, and a
small inline style for the solve box (`.solve`, `.solve__steps`, `.solve__status`, `.seek`,
[L15–L24](../../public/simulations/driven-oscillator.html#L15-L24)). Styles are described in [styles.md](../styles.md).

**Body**, in order:
- `header.sim-top`: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`,
  87 × 48) and the back link "← All simulations" ([L28](../../public/simulations/driven-oscillator.html#L28)), then the hand-written Fig. 1–10 links, Fig. 9
  marked `aria-current` ([L27–L42](../../public/simulations/driven-oscillator.html#L27-L42));
- `.sim__head`: "Fig. 9 · control systems · forced oscillations", the `h1` and the lede
  ([L46–L50](../../public/simulations/driven-oscillator.html#L46-L50));
- `.sim__grid`: the main figure `#stage` with `canvas#osc` and a caption holding the equation and `#cap-t`
  ([L54–L62](../../public/simulations/driven-oscillator.html#L54-L62)); the Bode figure `#stage-bode` with `canvas#bode` and
  `#cap-res` ([L63–L71](../../public/simulations/driven-oscillator.html#L63-L71)); the control panel `aside.panel` with the
  solve box, the sliders, six readouts and a legend ([L74–L137](../../public/simulations/driven-oscillator.html#L74-L137)).
  The **Read values** switch is added to the first caption by datalog.js;
- `article.paper#paper`, the lecture note ([L140–L456](../../public/simulations/driven-oscillator.html#L140-L456)):
  abstract; ten sections `.psec` — 01 A push from outside, 02 The model, 03 The exact solution ★ (3.1 The steady state,
  3.2 The transient), 04 Resonance and phase, 05 The control engineer's view ★, 06 The start: beats and decay, 07 Where the
  energy goes, 08 Solve first, then play, 09 On screen, 10 What the model leaves out (10.1 Further reading, four items, each
  with a link). Nine numbered equations, `\tag{1}`–`\tag{8}` and `\tag{6a}` (the completed square that locates the
  resonance peak, [L321](../../public/simulations/driven-oscillator.html#L321)). Four figures with five inline SVGs: Figure 1 the plant sketch
  ([L169–L198](../../public/simulations/driven-oscillator.html#L169-L198)), Figure 2 amplitude and phase against $f/f_0$ for
  four damping ratios (two SVGs, [L229–L317](../../public/simulations/driven-oscillator.html#L229-L317)), Figure 3 the block
  diagram ([L336–L354](../../public/simulations/driven-oscillator.html#L336-L354)), Figure 4 the default run
  ([L360–L408](../../public/simulations/driven-oscillator.html#L360-L408)). Two exercise boxes, 4.1 and 6.1;
- `section#walk` with `data-walk="driven"` ([L458](../../public/simulations/driven-oscillator.html#L458)), filled by
  `sim.js` from `walk/driven.js` ([sim.js:402–411](../../public/scripts/sim.js#L402-L411)); see [walk.md](../scripts/walk.md);
- footer; then the scripts in load order: `fold.js`, `sim.js`, `dataset.js`, the page's inline script, `datalog.js`
  ([L466–L1110](../../public/simulations/driven-oscillator.html#L466-L1110)). Folds are described in
  [fold.md](../scripts/fold.md), the shared helpers in [sim.md](../scripts/sim.md).

The walkthrough's seven steps quote these page lines: step 1 [L571](../../public/simulations/driven-oscillator.html#L571);
step 2 [L566–L568](../../public/simulations/driven-oscillator.html#L566-L568); step 3
[L583–L586](../../public/simulations/driven-oscillator.html#L583-L586) and
[L590–L591](../../public/simulations/driven-oscillator.html#L590-L591); step 4
[L576–L580](../../public/simulations/driven-oscillator.html#L576-L580); step 5
[L588–L589](../../public/simulations/driven-oscillator.html#L588-L589) and
[L615](../../public/simulations/driven-oscillator.html#L615); step 6
[L557–L558](../../public/simulations/driven-oscillator.html#L557-L558) and
[L597](../../public/simulations/driven-oscillator.html#L597); step 7
[L916](../../public/simulations/driven-oscillator.html#L916), [L904](../../public/simulations/driven-oscillator.html#L904),
[L838](../../public/simulations/driven-oscillator.html#L838). All seven excerpts match the page text at present.

## Where the drawing and the store differ

The page states the differences in `Sim.data.about` ([L1101](../../public/simulations/driven-oscillator.html#L1101)), which
the data panel prints. In detail:

- **Nearest row, no interpolation.** `t_play` runs continuously, but the picture shows row
  $\operatorname{round}(t_\text{play}/10\,\text{ms})$ ([L904](../../public/simulations/driven-oscillator.html#L904)). The
  caption shows the row's time `ts[i]`, not `t_play` ([L910](../../public/simulations/driven-oscillator.html#L910)).
- **Overview strip thinned.** The strip of the whole run draws every `stride`-th row,
  `stride = max(1, floor(NS / (2 × strip width)))` ([L815](../../public/simulations/driven-oscillator.html#L815)): every 4th
  row at a 770 px canvas, every 10th at 356 px. The window chart draws every row between its edges
  ([L774](../../public/simulations/driven-oscillator.html#L774)).
- **Drawing scale changes with the run.** The block travels at most `amp = 0.11 × W0` pixels either side of rest, where
  `W0` is the width between wall and right margin, so `px_per_m = amp / xmax` differs from run to run
  ([L673](../../public/simulations/driven-oscillator.html#L673), [L676](../../public/simulations/driven-oscillator.html#L676)).
  The ruler under the floor shows $\pm$`xmax` in metres ([L757](../../public/simulations/driven-oscillator.html#L757)).
- **Force arrow.** Its length is $F_n/F_0 \cdot L_F$ with $L_F = \min(88, 0.12\,w)$ px; arrows shorter than 2 px are not
  drawn ([L748](../../public/simulations/driven-oscillator.html#L748)).
- **Dial.** The arm points at the stored $\Omega t_n \bmod 2\pi$ ([L762](../../public/simulations/driven-oscillator.html#L762)).
- **Bode plot.** The dot sits at the exact $|G(i\Omega)|$ and $\varphi$; the ring is the amplitude measured from the last
  10 s of the stored run, per newton ([L884–L886](../../public/simulations/driven-oscillator.html#L884-L886)). With the
  defaults they differ by 0.03 % (0.48194 against 0.48209 m/N), the remains of the transient.
- **Rounding.** Canvas labels and readouts round (for example $F$ to 2 decimals, $x$ to 3); the store keeps full doubles.

## How to change it safely

- **Run length, step and storage stride.** `TEND`, `H` and `EVERY` ([L473](../../public/simulations/driven-oscillator.html#L473))
  determine `NS`. Keep `TEND / H` and `TEND / H / EVERY` whole numbers, because `step === TEND / H` and `step % EVERY` decide
  the last row ([L575–L581](../../public/simulations/driven-oscillator.html#L575-L581)). These places repeat the numbers by
  hand and must change with them: the seek slider `max="6000"` ([L90](../../public/simulations/driven-oscillator.html#L90));
  the `formula` texts "n · 10 h", "t_n ≥ 50 s", "round(t_play / 10h)" ([L502](../../public/simulations/driven-oscillator.html#L502),
  [L517](../../public/simulations/driven-oscillator.html#L517), [L521](../../public/simulations/driven-oscillator.html#L521));
  the group note "every 10 ms of the 60 s" ([L980](../../public/simulations/driven-oscillator.html#L980)); the check text
  "at most 6000" ([L1043](../../public/simulations/driven-oscillator.html#L1043)); the 10 s tick step of the overview
  ([L830](../../public/simulations/driven-oscillator.html#L830)); the walkthrough's "step / 10", "60 000 steps" and
  "6 001 rows" ([driven.js:57–58](../../public/scripts/walk/driven.js#L57-L58)); the lecture note section 8
  ([L426–L428](../../public/simulations/driven-oscillator.html#L426-L428)) and `about`.
- **The integrator exists twice.** `solve()` ([L583–L592](../../public/simulations/driven-oscillator.html#L583-L592)) and
  `rk4Replay()` ([L941–L950](../../public/simulations/driven-oscillator.html#L941-L950)) must stay identical, line for line,
  or the data panel's Check of `xs`, `vs`, `Win` and `Wloss` will no longer agree with the store.
- **Walkthrough excerpts.** The seven excerpts listed under Page structure are quoted verbatim in `walk/driven.js`. If one
  of those page lines changes, change the excerpt in the same edit. Insert new code after a quoted line, never inside a
  quoted group (AGENTS.md).
- **Taps stay where values are computed.** Write a new number into the store at the line that computes it, declare it with
  `ds.var` next to its relatives, add it to a group in `Sim.data.groups`, and give it a `check` (and a `drawn` if it is on
  screen). Do not compute numbers inside `draw*()` beyond the metre-to-pixel conversion.
- **Lecture-note numbers.** Sections 2–9 quote values for the default sliders ([L102–L118](../../public/simulations/driven-oscillator.html#L102-L118)),
  and Figures 2 and 4 are static SVGs computed from the page's formulas. Changing a default or the physics means
  recomputing them.
- **Damping limit.** `exact()` divides by $\omega_d = \omega_0\sqrt{1-\zeta^2}$; the slider stops at 0.9. Allowing
  $\zeta \ge 1$ needs a different exact solution (section 10 says so, [L444](../../public/simulations/driven-oscillator.html#L444)).
- **Frequency range.** The Bode axis covers 0.05–2 Hz ([L628](../../public/simulations/driven-oscillator.html#L628),
  [L856](../../public/simulations/driven-oscillator.html#L856)); raising the $f_0$ or $f$ slider beyond 2 Hz would put the
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
   ([L920](../../public/simulations/driven-oscillator.html#L920)), so a paused page still redraws about 60 times a second
   (about 1.5 ms per frame measured) and rewrites `#cap-t` each time ([L910](../../public/simulations/driven-oscillator.html#L910)).
7. Fixed on 2026-10-15: the note gives the measured default solve time of 9.5–12.4 ms and states that timing depends on the machine (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
8. **AGENTS.md** said the load order dataset.js → page → datalog.js holds for "all eight figures"; this page (Fig. 9)
   follows it too. Corrected to "all ten figures" on 14 October 2026.


## Teaching revision · 15 October 2026

The note separates undamped natural frequency from damped ringing, interprets the complex denominator as spring, inertia and quadrature damping, and uses the damped ringing frequency for the approximate default beat time. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16: the paragraph reading the complex denominator had been placed between "(2) turns into algebra:" and equation (3); it now follows (3) and ends "gives the form in (3)" ([L217](../../public/simulations/driven-oscillator.html#L217)). See the [audit of the revision](../research-theory-audit.md).

Fixed on 2026-10-16 (second repairs): the Millennium Bridge is back as the counter-example to a prescribed force (the walkers' steps fed back on the sway); the beat-time sentence is one sentence again ([L168](../../public/simulations/driven-oscillator.html#L168)). See the [audit of the revision](../research-theory-audit.md).

## Teaching revision · 20 October 2026

Judged section by section against [notes/STANDARD.md](../../notes/STANDARD.md); the verdicts and measurements are in
[notes/fig09/plan.md](../../notes/fig09/plan.md). Sections 1, 2 and 8, the text of section 6 and the limits in section 10 were left as they were. Filled in: the step from (3)
to (4), with `atan2` named and the real part justified ([L218](../../public/simulations/driven-oscillator.html#L218)); the
roots $s = -\zeta\omega_0 \pm i\omega_0\sqrt{1-\zeta^2}$ of the free equation, which give $\tau$, $\omega_d$ and the meaning of
$\zeta = 1$, and the two starting conditions behind $C_1$, $C_2$ ([L221](../../public/simulations/driven-oscillator.html#L221));
the completed square (6a) that places the peak at $\Omega_r = \omega_0\sqrt{1-2\zeta^2}$, with $f_r = 0.4987$ Hz now named as a
frequency in hertz ([L320–L322](../../public/simulations/driven-oscillator.html#L320-L322)); the sign of the poles' real part,
$-1/\tau$ ([L334](../../public/simulations/driven-oscillator.html#L334)); the origin of $\tfrac12 c\,\Omega^2X^2$
([L419](../../public/simulations/driven-oscillator.html#L419)). Corrected: Exercise 6.1 said the transient "hardly shows" at
$f = 0.20$ Hz; the force switches on at full strength, so the ringing starts as large as the steady motion (measured at
$\zeta = 0.01$: $\sqrt{C_1^2+C_2^2} = 1.00005\,X$, $|x|$ up to $0.224$ m $= 1.85\,X$ at 5 s)
([L411](../../public/simulations/driven-oscillator.html#L411)); section 9 described one 60 s chart, but the dashed $F/k$ and
$\pm X$ belong to the moving window ($\operatorname{clamp}(4/f, 6, 20)$ s, 8.9 s with the defaults) above the 60 s strip
([L435](../../public/simulations/driven-oscillator.html#L435)). Further reading now links every item and adds Feynman,
Vol. I, chapters 23 and 24 ([L448–L451](../../public/simulations/driven-oscillator.html#L448-L451)).

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig09/`), the lead made only these changes, each on its existing line, so no line link moved: §2: ω_d no longer used before ζ is defined ([L205](../../public/simulations/driven-oscillator.html#L205)); §3.2: the ringing written before its constants are fixed ([L221](../../public/simulations/driven-oscillator.html#L221)); §5: X(s), F(s) named as transforms ([L332](../../public/simulations/driven-oscillator.html#L332)); Figure 3: the plant box widened so G(s) fits ([L342](../../public/simulations/driven-oscillator.html#L342)); §9: every run drawn at its own scale; compare runs on the ruler ([L435](../../public/simulations/driven-oscillator.html#L435)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).
