# Fig. 9 · Driven Oscillator

| | |
|---|---|
| Page | [public/simulations/driven-oscillator.html](../../public/simulations/driven-oscillator.html) (1 934 lines, 327 290 bytes) |
| Walkthrough | [public/scripts/walk/driven.js](../../public/scripts/walk/driven.js) (290 lines, 14 steps, key `driven`) |
| Thumbnail | [public/images/sims/driven-oscillator.webp](../../public/images/sims/driven-oscillator.webp) (WebP, 800 × 500 px, 23.7 kB) |
| Catalog entry | [public/scripts/catalog.js#L183](../../public/scripts/catalog.js#L183-L199) (`id: 'driven-oscillator'`, `fig: 9`, `field: 'control'`, `stage: 1`, lines 183–199) |

A block of mass 1 kg sits on a spring and a damper and is pushed from its other side by a moving-coil drive: a coil on a
tube fixed to the block sits in the gap of a magnet, and the force on the block is $F = B\ell I$ with $B\ell = 10$ T·m. In
open loop the current source drives $I_0\cos\Omega t$, a push that does not care where the block is. With the controller
on, a PID controller $u = K_p(r-x) + K_i\int(r-x)\,dt - K_d\dot x$ adds its force through the same coil and holds the block
at an equilibrium it decides (lecture note §9, equations (12)–(16)). A **Take control** box above the figure (preset buttons, the target $r$, the three gains, and a hint that says what a
drag will do) leads the hand experiment; the target can also be set by dragging a flag on the ruler, and a new $r$ is solved
at once from the state on screen. The reader sets the spring constant $k$ (the natural
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
(per newton, log axes, 241 frequencies). The closed loop is drawn in ink, the bare plant dashed behind it. A phase
portrait plots the run as a path in the $(x, \dot x)$ plane with the fixed point $x^*$, the steady orbit (21), one strobe dot
per drive period (the Poincaré section) and arrows of the free flow (17); its caption gives the eigenvalues (18) or (20), the
kind of fixed point and the per-period multiplier $|\mu|$. The lecture note's §11 derives all of these. The page is up to
1560 px wide, like every simulation since 30 October 2026, and the block's travel $A_\text{px}$ is fitted to the canvas: as large as the coil
drive, which needs about $3A_\text{px}$ to the right of the block, leaves room for. The page never integrates
while the reader watches. It solves the whole run first with the classical fourth-order Runge–Kutta method (RK4), writes
every sample into its dataset, and each frame then draws one stored row.

In this page, a link such as [L887](../../public/simulations/driven-oscillator.html#L887) points to a line of
`driven-oscillator.html`. Other files are named in the link text.

## The physics in one picture

**What you would see.** Push a child on a swing. Pushed at the wrong moments it barely moves; pushed in time with its own
rhythm it swings high. At first the swing also rings at its own rhythm, so two rhythms beat against each other; after a
while only the pusher's rhythm is left.

**The model.** Three forces act along the floor: the spring $-kx$, the damper $-c\dot x$ and the driver $F(t)$. Newton's
second law gives $m\ddot x + c\dot x + kx = F_0\cos\Omega t$. The time $t$ appears on its own inside the cosine: the clock
belongs to someone else. The lecture note derives this in sections 1–2
([L243](../../public/simulations/driven-oscillator.html#L243), [L280](../../public/simulations/driven-oscillator.html#L280)),
the exact solution in section 3 ([L290](../../public/simulations/driven-oscillator.html#L290)), resonance and phase in
section 4, the transfer function in section 5, beats in section 6 and the energy balance in section 7.

**What the code evaluates.** The sliders give $f_0$, $\zeta$, $F_0$ and $f$; `solve()` turns them into the constants of the
equation of motion ([L887](../../public/simulations/driven-oscillator.html#L887)):

$$\omega_0 = 2\pi f_0,\qquad k = m\,\omega_0^2,\qquad c = 2\zeta m\,\omega_0,\qquad \Omega = 2\pi f .$$

The right-hand side of the ODE is `accel()` ([L883–L885](../../public/simulations/driven-oscillator.html#L883-L885)):

$$\dot x = v,\qquad \dot v = a(t, x, v) = \frac{F_0\cos\Omega t - c\,v - k\,x}{m} .$$

Along the run the page also integrates the work of the driver and the heat of the damper
([L919–L920](../../public/simulations/driven-oscillator.html#L919-L920)) and stores the energy and the two powers at each
sample ([L907](../../public/simulations/driven-oscillator.html#L907)):

$$W_\text{in} = \int_0^T F v\,\mathrm dt,\quad W_\text{loss} = \int_0^T c\,v^2\,\mathrm dt,\quad E = \tfrac12 m v^2 + \tfrac12 k x^2,\quad P_\text{in} = F v,\quad P_\text{loss} = c v^2 .$$

The exact solution is used only to grade the numbers, never to draw them. `steady()`
([L817–L820](../../public/simulations/driven-oscillator.html#L817-L820)) gives the steady amplitude and phase lag, and
`exact()` ([L821–L826](../../public/simulations/driven-oscillator.html#L821-L826)) adds the transient that starts the block
from rest:

$$X = \frac{F_0/m}{\sqrt{(\omega_0^2-\Omega^2)^2 + (2\zeta\omega_0\Omega)^2}},\qquad \varphi = \operatorname{atan2}(2\zeta\omega_0\Omega,\ \omega_0^2-\Omega^2),$$

$$x_\text{exact}(t) = X\cos(\Omega t-\varphi) + e^{-\zeta\omega_0 t}\left(C_1\cos\omega_d t + C_2\sin\omega_d t\right),\quad C_1 = -X\cos\varphi,\quad C_2 = \frac{\zeta\omega_0 C_1 - X\Omega\sin\varphi}{\omega_d},\quad \omega_d = \omega_0\sqrt{1-\zeta^2}.$$

Further derived numbers ([L959–L968](../../public/simulations/driven-oscillator.html#L959-L968)): $\tau = 1/(\zeta\omega_0)$,
$Q = 1/(2\zeta)$, $f_r = f_0\sqrt{1-2\zeta^2}$ when $\zeta < 1/\sqrt2$ (else 0), $|G(i\Omega)| = X/F_0$, and the energy balance
$|E(T)-E(0)-(W_\text{in}-W_\text{loss})|/W_\text{in}$. The Bode plot evaluates $|G(i\Omega)| = 1/(m\sqrt{(\omega_0^2-\Omega^2)^2+(2\zeta\omega_0\Omega)^2})$
and $\varphi(\Omega)$ in degrees at 241 frequencies $f_j = 0.05\cdot 40^{j/240}$ Hz, from 0.05 to 2 Hz
([L1002–L1009](../../public/simulations/driven-oscillator.html#L1002-L1009)).

| Symbol | Meaning | Unit | In code |
|---|---|---|---|
| $m$ | mass, fixed at 1 | kg | `M` ([L606](../../public/simulations/driven-oscillator.html#L606)) |
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

One line fixes the run ([L606](../../public/simulations/driven-oscillator.html#L606)):
`M = 1` kg, `H = 0.001` s, `TEND = 60` s, `EVERY = 10`, and `NS = TEND / H / EVERY + 1`. In JavaScript `60 / 0.001` is
exactly 60 000, so `NS` is exactly 6 001 (checked in Node). The page keeps four pieces of its own state
([L613](../../public/simulations/driven-oscillator.html#L613)): `playT` (playback time, s), `iNow` (row on screen),
`fps` and `solved` (the slider values of the last solve, or `null`).

### 1 Solve: classical RK4 over the whole run

`solve()` ([L886–L975](../../public/simulations/driven-oscillator.html#L886-L975)) works on the state vector
$s = (x, v)$ with the slope $f(t, s) = (v,\ a(t, x, v))$. It starts from rest, $x = v = 0$ at $t = 0$
([L902](../../public/simulations/driven-oscillator.html#L902)). One step of size $h$ samples the slope four times: at the
start, twice at the middle and at the end ([L913–L916](../../public/simulations/driven-oscillator.html#L913-L916)):

$$k_1 = f(t, s),\quad k_2 = f(t+\tfrac h2, s+\tfrac h2 k_1),\quad k_3 = f(t+\tfrac h2, s+\tfrac h2 k_2),\quad k_4 = f(t+h, s+h k_3),$$
$$s(t+h) = s + \tfrac h6\,(k_1 + 2k_2 + 2k_3 + k_4) .$$

In the code the $x$-components of the slopes are the velocities `v, v2, v3, v4` and the $v$-components are the
accelerations `a1 … a4`; the update is [L922–L923](../../public/simulations/driven-oscillator.html#L922-L923). The two
work integrals are quadratures (their slopes do not feed back), carried with the same RK4 weights and the same stage
velocities, with the force evaluated at $t$, $t+h/2$ and $t+h$
([L918–L920](../../public/simulations/driven-oscillator.html#L918-L920)). Time is set from the step count,
`t = (step + 1) * H` ([L924](../../public/simulations/driven-oscillator.html#L924)), so it does not collect round-off by
repeated addition.

Why RK4 with $h = 1$ ms: the code does not state the reason. What can be measured is the margin. The fastest natural motion
allowed by the sliders is $\omega_0 = 2\pi\cdot1.5 = 9.42$ rad/s, so $\omega_0 h \le 0.0094$ rad per step, deep inside the
region where RK4 is stable and its error per step scales as $(\omega_0 h)^5$. With the defaults the largest difference to
the exact solution over the run is $5.26\times10^{-12}$ m and the energy balance holds to $1.27\times10^{-12}$ (measured).

### 2 Store: every tenth state

The loop runs `step = 0 … 60 000` ([L904](../../public/simulations/driven-oscillator.html#L904)). At the top of each pass,
before the step, every tenth state is written straight into the dataset arrays
([L905–L910](../../public/simulations/driven-oscillator.html#L905-L910)): `ts`, `xs`, `vs`, `Fs`, `Es`, `Pin`, `Ploss`. So
row $n$ holds the state at exactly $t_n = n\cdot 10h = n \cdot 10$ ms. After storing step 60 000 the loop stops without a
further step ([L911](../../public/simulations/driven-oscillator.html#L911)): 60 000 RK4 steps, 6 001 rows.

Two passes over the stored rows follow. The first ([L926–L934](../../public/simulations/driven-oscillator.html#L926-L934))
fills `xex` with the exact solution and finds the largest error `err`, the largest $|x|$ (`xmax`, which sets the drawing
scale) and the largest $|x|$ for $t_n \ge 50$ s (`Xm`, "Measured, last 10 s"). The second
([L935–L943](../../public/simulations/driven-oscillator.html#L935-L943)) fills `xqs` $= F_n/k$, the drive phase
`ph` $= \Omega t_n \bmod 2\pi$ and the chart half-height `ylim`. Then the arrays are marked changed
([L944](../../public/simulations/driven-oscillator.html#L944)) and every scalar is written
([L945–L968](../../public/simulations/driven-oscillator.html#L945-L968)).

The arrays come from `ds.alloc(name)` ([L900–L901](../../public/simulations/driven-oscillator.html#L900-L901)), which
allocates a new typed array only when the length changes ([dataset.js:67](../../public/scripts/dataset.js#L67)); a re-solve
overwrites the same `Float64Array`s in place. Memory, measured from the live store: 10 arrays × 6 001 × 8 B = 480 080 B for
the run, plus 3 × 241 × 8 B = 5 784 B for the Bode curves, 485 864 B in all. One solve took 6–17 ms in headless Chromium
(`solve_ms`, measured with `performance.now()` at [L886](../../public/simulations/driven-oscillator.html#L886) and
[L969](../../public/simulations/driven-oscillator.html#L969)).

Last, `solve()` records the settings it used in `solved` ([L970](../../public/simulations/driven-oscillator.html#L970)),
recomputes the Bode curves (`bode()`, [L998–L1024](../../public/simulations/driven-oscillator.html#L998-L1024)), rewrites the
readouts, sets `playT = 0` and starts the clock ([L971–L974](../../public/simulations/driven-oscillator.html#L971-L974)).

### When the run is solved again

Only twice: once at load ([L1923](../../public/simulations/driven-oscillator.html#L1923)) and whenever **Solve** is pressed
([L1611](../../public/simulations/driven-oscillator.html#L1611)). A slider only calls `markStale()`
([L785–L790](../../public/simulations/driven-oscillator.html#L785-L790),
[L1026–L1031](../../public/simulations/driven-oscillator.html#L1026-L1031)), which compares the four sliders with `solved`, sets
the `stale` flag and rewrites the status line in burgundy; the old run keeps playing, and its settings are named in the
status text ([L1032–L1042](../../public/simulations/driven-oscillator.html#L1032-L1042)).

### 3 Play: the frame loop, in order

`Sim.clock` ([sim.js:176–197](../../public/scripts/sim.js#L176-L197)) calls the page's tick on every
`requestAnimationFrame`, with $\Delta t$ capped at 0.05 s and $\Delta t = 0$ while paused. Each tick:

1. returns if nothing has been solved; updates the smoothed frame rate; advances `playT += speed · Δt`; at 60 s clamps and
   pauses; stores `fps` and `playing`; marks step "3 play" ([L1546–L1561](../../public/simulations/driven-oscillator.html#L1546-L1561));
2. `frame()` ([L1533–L1545](../../public/simulations/driven-oscillator.html#L1533-L1545)) picks the nearest stored row,
   $n = \operatorname{round}(t_\text{play}/10\,\text{ms})$ clamped to 0 … 6 000, writes `i_now`, `t_play` and the six
   `*_now` copies of row $n$ into the store, moves the **Stored run** slider and the caption time, then calls `draw()`;
3. `draw()` ([L1349–L1463](../../public/simulations/driven-oscillator.html#L1349-L1463)) sets the window width
   $T_w = \text{clamp}(4/f, 6, 20)$ s and its left edge $t_0 = \text{clamp}(t_n - 0.7T_w, 0, 60 - T_w)$, gets the layout
   from `geom()`, turns $x_n$ into the block position `bx = eqX + xs[i] * sc` and $F_n$ into the arrow length, stores these
   pixel values, clears the canvas and draws `drawMechanism`, `drawWindow` and `drawOverview` in that order.

Nothing in this chain integrates; the only arithmetic turns metres, seconds and newtons into pixels. Because the clock calls
the tick every animation frame even while paused (with $\Delta t = 0$), the figure is redrawn at the display rate in both
states; one `frame()` took about 1.5 ms (measured over 200 seek events at a 1 440 px wide window).

### Precomputation and caching

- The Bode canvas is not redrawn per frame: only after a solve ([L1023](../../public/simulations/driven-oscillator.html#L1023)),
  on resize ([L1927](../../public/simulations/driven-oscillator.html#L1927)) and when fonts are ready
  ([L1928](../../public/simulations/driven-oscillator.html#L1928)).
- `geom()` ([L1059–L1090](../../public/simulations/driven-oscillator.html#L1059-L1090)) is recomputed on every call; it reads
  `xmax`, `win_t0`, `win_T` and `ylim` from the store, so `draw()` must store the window before calling it
  ([L1352–L1353](../../public/simulations/driven-oscillator.html#L1352-L1353)).
- For the data panel's Check of $W_\text{in}$ and $W_\text{loss}$, `fullReplay()` reruns the whole 60 s once and caches the
  result under a key made of the four settings ([L1651–L1657](../../public/simulations/driven-oscillator.html#L1651-L1657)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `steady(w0, z, W, F)` | [817–820](../../public/simulations/driven-oscillator.html#L817-L820) | Exact steady amplitude $X$ and phase lag $\varphi$, equation (4) of the note. |
| `exact(t, w0, z, W, st)` | [821–826](../../public/simulations/driven-oscillator.html#L821-L826) | Exact $x(t)$ from rest, equation (5); used only to measure the RK4 error. |
| `control()` | [829–832](../../public/simulations/driven-oscillator.html#L829-L832) | The controller force $u = K_p(r-x) + K_i z - K_d v$, equation (12). |
| `closed()` | [833–837](../../public/simulations/driven-oscillator.html#L833-L837) | Closed-loop steady amplitude and phase, (16). |
| `equilibrium()` | [853](../../public/simulations/driven-oscillator.html#L853) | Equilibrium (14). |
| `matmul()` | [854](../../public/simulations/driven-oscillator.html#L854) | Matrix product (for `expm`). |
| `expm()` | [855–865](../../public/simulations/driven-oscillator.html#L855-L865) | Matrix exponential by scaling and squaring. |
| `exactClosed()` | [866–880](../../public/simulations/driven-oscillator.html#L866-L880) | Exact closed-loop solution sample by sample; grades RK4 when the controller is on. |
| `accel(t, x, v, u, p)` | [883–885](../../public/simulations/driven-oscillator.html#L883-L885) | Right-hand side: $(F_0\cos\Omega t + u - cv - kx)/m$. |
| `solve()` | [891–975](../../public/simulations/driven-oscillator.html#L891-L975) | Solve and store the whole run (see above). |
| `setSpan()` | [990–995](../../public/simulations/driven-oscillator.html#L990-L995) | Sets the held drawing span, `ylim`, `held`. |
| `fitScale()` | [996](../../public/simulations/driven-oscillator.html#L996) | **Fit scale**: span ← need. |
| `bode()` | [998–1024](../../public/simulations/driven-oscillator.html#L998-L1024) | Fills `fb`, `Gmag`, `Gphase` (241 points) and redraws the Bode plot. |
| `markStale()` | [1026–1031](../../public/simulations/driven-oscillator.html#L1026-L1031) | Sets `stale` when a slider differs from the last solve. |
| `status()` | [1032–1042](../../public/simulations/driven-oscillator.html#L1032-L1042) | Writes the status line and the "1 solve / 2 store" marks. |
| `readouts()` | [1043–1055](../../public/simulations/driven-oscillator.html#L1043-L1055) | Writes the six readouts and the Bode caption $f_r$. |
| `geom()` | [1059–1090](../../public/simulations/driven-oscillator.html#L1059-L1090) | Layout from canvas size and store: mechanism, window chart, overview strip, dial; mapping functions `wx`, `wy`, `ox`, `oy`, `inWin`. |
| `arrow(c, …)` | [1091–1099](../../public/simulations/driven-oscillator.html#L1091-L1099) | Draws a straight arrow with a filled head. |
| `spring(c, …)` | [1100–1106](../../public/simulations/driven-oscillator.html#L1100-L1106) | Draws a zigzag spring. |
| `label(c, sym, value, …)` | [1107–1117](../../public/simulations/driven-oscillator.html#L1107-L1117) | A symbol in Latin Modern via `Sim.tex`, then its value in IBM Plex Mono. |
| `drawMechanism(c, g, i, bx, cap, gx)` | [1118–1187](../../public/simulations/driven-oscillator.html#L1118-L1187) | Wall, floor, rest line, spring, damper (oil shaded by $P_\text{loss}$), outlined previous block, block on wheels, then `drawCoil`, `drawForces`, `drawEnergy`, `drawController`; ruler, target dot, equilibrium line. |
| `drawCoil()` | [1188–1217](../../public/simulations/driven-oscillator.html#L1188-L1217) | Magnet, coil tube and winding, current dots and crosses, current source and leads. |
| `drawForces()` | [1219–1236](../../public/simulations/driven-oscillator.html#L1219-L1236) | The three force arrows over the block. |
| `drawController()` | [1253–1271](../../public/simulations/driven-oscillator.html#L1253-L1271) | The controller box: value read, P, I, D, u bars, command line. |
| `drawEnergy()` | [1272–1283](../../public/simulations/driven-oscillator.html#L1272-L1283) | The three energy bars. |
| `drawWindow(c, g, i)` | [1284–1327](../../public/simulations/driven-oscillator.html#L1284-L1327) | Window chart: ticks, $\pm X$, $F/k$, $x$ faint ahead and dark behind, cursor, key. |
| `drawOverview(c, g, i)` | [1328–1348](../../public/simulations/driven-oscillator.html#L1328-L1348) | Strip of the whole run with the window band shaded. |
| `draw()` | [1349–1368](../../public/simulations/driven-oscillator.html#L1349-L1368) | One frame of the main canvas. |
| `bodeGeom()` | [1465–1478](../../public/simulations/driven-oscillator.html#L1465-L1478) | Bode layout: two panels side by side (stacked below 560 px), log $f$ axis 0.05–2 Hz, three decades of $\lvert G\rvert$, 0–180°. |
| `drawBode()` | [1479–1514](../../public/simulations/driven-oscillator.html#L1479-L1514) | Draws both panels, the $f_0$ line, the curves, the dot at the exact value and the ring at the measured one. |
| `Sim.live()` | [1517–1531](../../public/simulations/driven-oscillator.html#L1517-L1531) | Formatted store values for the walkthrough's "Now" column. |
| `frame()` | [1533–1545](../../public/simulations/driven-oscillator.html#L1533-L1545) | Picks the stored row for `playT`, copies it to the `*_now` scalars, draws. |
| `chartPos(n)`, `chartPosQ(n)` | [1621–1624](../../public/simulations/driven-oscillator.html#L1621-L1624) | Screen point of $x_n$ (or $F_n/k$) on the window chart, else on the overview strip. |
| `chartPosQ()` | [1625–1628](../../public/simulations/driven-oscillator.html#L1625-L1628) |  |
| `loopParams()` | [1629](../../public/simulations/driven-oscillator.html#L1629) | The eight settings of the last solve, for the checks. |
| `fullReplay()` | [1652–1657](../../public/simulations/driven-oscillator.html#L1652-L1657) | Cached `rk4Replay(6000)`. |
| `sliderCheck`, `at`, `neutralInk`, `readBack` | [1658](../../public/simulations/driven-oscillator.html#L1658) | Small helpers for the data panel's Check (slider value, row on screen, dark-ink test, pixel read-back). |
| `at()` | [1659–1661](../../public/simulations/driven-oscillator.html#L1659-L1661) |  |
| `neutralInk()` | [1662](../../public/simulations/driven-oscillator.html#L1662) |  |
| `readBack()` | [1663–1666](../../public/simulations/driven-oscillator.html#L1663-L1666) |  |
| `prevParams()` | [1667–1670](../../public/simulations/driven-oscillator.html#L1667-L1670) | Plant and loop of the previous run. |
| `mutedInk()` | [1671](../../public/simulations/driven-oscillator.html#L1671) | Pixel test: grey ink. |
| `chartPosPrev()` | [1672–1675](../../public/simulations/driven-oscillator.html#L1672-L1675) | Where sample n of the previous run is drawn. |
| `roseInk()` | [1676](../../public/simulations/driven-oscillator.html#L1676) | Pixel test: rose. |
| `ctrlBar()` | [1677](../../public/simulations/driven-oscillator.html#L1677) | Where a controller bar ends. |
| `tanInk()` | [1678](../../public/simulations/driven-oscillator.html#L1678) | Pixel test: brown. |
| `arrowPoint()` | [1679](../../public/simulations/driven-oscillator.html#L1679) | Mid-point of a force arrow. |
| `barPoint()` | [1680](../../public/simulations/driven-oscillator.html#L1680) | End of an energy bar. |
| `arrowBack()` | [1681–1685](../../public/simulations/driven-oscillator.html#L1681-L1685) | Read-back of a force arrow. |
| `blockPixel()` | [1686–1690](../../public/simulations/driven-oscillator.html#L1686-L1690) | Reads back a pixel inside the burgundy block. |
| `Sim.data` (object) | [1691–1921](../../public/simulations/driven-oscillator.html#L1691-L1921) | The data-panel contract: groups, colours, `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `about`. |
| `ctrlHead()` | [1243–1247](../../public/simulations/driven-oscillator.html#L1243-L1247) | Header of the controller box: one word on narrow screens. |
| `ctrlWidth()` | [1248–1252](../../public/simulations/driven-oscillator.html#L1248-L1252) | Width of the controller box, measured from its header. |
| `sliderParams()` | [886–890](../../public/simulations/driven-oscillator.html#L886-L890) | The plant and loop parameters from the sliders (used by `solve` and the hand). |
| `pointerX()` | [1564](../../public/simulations/driven-oscillator.html#L1564) | Pointer position in css px of the main canvas. |
| `holdState()` | [1565–1576](../../public/simulations/driven-oscillator.html#L1565-L1576) | The state while your hand holds the block: controller force, hand force, status line; then `draw()`. |
| `release()` | [1600–1606](../../public/simulations/driven-oscillator.html#L1600-L1606) | Ends a hold and calls `solve({x, v, z})`. |
| `capArrow()` | [1218](../../public/simulations/driven-oscillator.html#L1218) | Caps a force arrow at 1.6 A<sub>px</sub> (drawn with a break mark). |
| `ctrlScale()` | [1237–1242](../../public/simulations/driven-oscillator.html#L1237-L1242) | Scale of the controller bars: the run’s, or while held the largest force now. |
| `forceGeom()` | [1372–1376](../../public/simulations/driven-oscillator.html#L1372-L1376) | Layout of the force-profile canvas. |
| `forceCurves()` | [1377–1382](../../public/simulations/driven-oscillator.html#L1377-L1382) | Which force series the profile draws (controller parts only when on). |
| `drawForceProfile()` | [1383–1410](../../public/simulations/driven-oscillator.html#L1383-L1410) | Draws the force profile for the present row. |
| `setView()` | [1614](../../public/simulations/driven-oscillator.html#L1614) | Switches the frequency response between the linear view and the Bode view. |
| `eigen()` | [838–852](../../public/simulations/driven-oscillator.html#L838-L852) | Eigenvalues of the free motion and the kind of fixed point, §11. |
| `field()` | [977–989](../../public/simulations/driven-oscillator.html#L977-L989) | Arrow grid of the free flow and the height of the phase portrait. |
| `phaseGeom()` | [1414–1418](../../public/simulations/driven-oscillator.html#L1414-L1418) | Layout of the phase portrait. |
| `drawPhase()` | [1419–1454](../../public/simulations/driven-oscillator.html#L1419-L1454) | Draws the phase portrait for the present row. |
| `eigText()` | [1459–1463](../../public/simulations/driven-oscillator.html#L1459-L1463) | Caption of the phase portrait: eigenvalues, kind, |μ|. |
| `takeHint()` | [798–807](../../public/simulations/driven-oscillator.html#L798-L807) | The take-control hint and the highlighted preset. |
| `fromNow()` | [811](../../public/simulations/driven-oscillator.html#L811) | The state on screen, the start of a run after a new target. |
| `flagToR()` | [1590](../../public/simulations/driven-oscillator.html#L1590) | Converts a flag position on the ruler to r. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Solve | `solve` | button | Calls `solve()` ([L1611](../../public/simulations/driven-oscillator.html#L1611)). |
| Pause / Play | `play` | button | Toggles the clock via `Sim.playButton` ([L1610](../../public/simulations/driven-oscillator.html#L1610), [sim.js:199](../../public/scripts/sim.js#L199)). |
| From t = 0 | `restart` | button | `playT = 0` and play ([L1612](../../public/simulations/driven-oscillator.html#L1612)). |
| Stored run | `seek` | 0–6000, step 1, default 0 ([L162](../../public/simulations/driven-oscillator.html#L162)) | Sets `playT = n · 10 ms` and draws ([L814](../../public/simulations/driven-oscillator.html#L814)); follows the playback ([L1542](../../public/simulations/driven-oscillator.html#L1542)). |
| Playback speed | `speed` | 0.25–4, step 0.25, default 1 ([L166](../../public/simulations/driven-oscillator.html#L166)) | Multiplies $\Delta t$ ([L1556](../../public/simulations/driven-oscillator.html#L1556)). Does not mark the run stale. |
| Spring constant $k$ | `kspring` | 1.5–90 N/m, step 0.01, default 9.87 | Sets $k$; $f_0 = \sqrt{k/m}/2\pi$ is shown beside it and used by the rest of the code; marks stale. |
| Damping ratio $\zeta$ | `zeta` | 0.01–0.9, step 0.01, default 0.05 ([L178](../../public/simulations/driven-oscillator.html#L178)) | $c$ at the next solve; marks stale. The maximum 0.9 keeps $\omega_d$ real in `exact()`. |
| Force amplitude $F_0$ | `F0` | 0–5 N, step 0.1, default 1 ([L186](../../public/simulations/driven-oscillator.html#L186)) | `p.F0`; marks stale. At 0 the drive arrow is hidden and `Gm_drive` is NaN ([L966](../../public/simulations/driven-oscillator.html#L966)). |
| Drive frequency $f$ | `fd` | 0.05–1.5 Hz, step 0.01, default 0.45 ([L190](../../public/simulations/driven-oscillator.html#L190)) | $\Omega$ at the next solve; marks stale. |
| Fit scale | `fit` | button | `fitScale()`: span ← need, redraw. |
| Linear / Bode, log | `view-amp`, `view-bode` | buttons, default Linear | `setView()`: amplitude function and phase difference on linear axes, or the Bode plot. |
| The block itself | canvas `osc` | press and drag | Hold: the controller acts on your hand's position; release: `solve({x, v, z})` from that state. |
| Off / P / PD / PID | `[data-gains]` | buttons | Set $(K_p, K_i, K_d)$ to (0,0,0), (20,0,0), (20,0,4), (20,10,4) and mark stale. |
| Target position $r$ | `r` (in the Take control box) | −0.5–0.5 m, step 0.01, default 0.3 | `p.r`; on release of the slider (`change`) the page solves at once from the state on screen; the flag on the ruler sets it too. |
| Proportional gain $K_p$ | `Kp` | 0–60 N/m, step 0.5, default 0 | `p.Kp`; marks stale. |
| Integral gain $K_i$ | `Ki` | 0–60 N/(m·s), step 0.5, default 0 | `p.Ki`; marks stale. |
| Derivative gain $K_d$ | `Kd` | 0–12 kg/s, step 0.1, default 0 | `p.Kd`; marks stale. |
| Read values | added by datalog.js | switch, off | Appended to the first figure caption ([datalog.js:895–897](../../public/scripts/datalog.js#L895-L897)); see [datalog.md](../scripts/datalog.md). |

## What the page writes into the data store

The store is made at [L616](../../public/simulations/driven-oscillator.html#L616):
`Sim.dataset({ title: 'Driven oscillator', attrs: { figure: 9, page, equation, start } })`. It has two dimensions,
`n` = 6 001 stored rows ([L657](../../public/simulations/driven-oscillator.html#L657)) and `b` = 241 Bode frequencies
([L769](../../public/simulations/driven-oscillator.html#L769)), and 127 variables: 100 scalars and 27 `Float64Array`s, all
declared at [L617–L774](../../public/simulations/driven-oscillator.html#L617-L774) (counted in the live store). The shared
store itself is described in [dataset.md](../scripts/dataset.md). Each variable carries `symbol`, `units`, `long_name`,
`computed_in`, often `formula`, and `digits`. Listed by the panel groups of
[L1694–L1706](../../public/simulations/driven-oscillator.html#L1694-L1706):

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

**The ledger** (24 October 2026). The data panel shows this store as a bookkeeper; its layout is
[scripts/ledger/driven-oscillator.js](../../public/scripts/ledger/driven-oscillator.js), loaded on the line that loads the panel
([L1931](../../public/simulations/driven-oscillator.html#L1931)). Headline: $x$, $\dot x$, $F$, $u$, $E$, $W_\text{in}$, $W_\text{loss}$. Sections: what you set (the sliders,
$k$ among them, and the start your hand gave), what follows from it, the state now, the stored run, the previous run, the curves
of the figures, the solver and the drawing; the last four start folded. Two books, each balanced by the page and again by the
panel:

| Book | Rows | Closing line | Residual stored | Measured |
|---|---|---|---|---|
| Energy | $E(0) + W_\text{in} - W_\text{loss}$ | $E$ | `bal_now` | about $3\times10^{-13}$ of the flows |
| Newton’s second law | $F + F_c + F_k$ | $m\,a$ | `fres_now` | 3 to $8\times10^{-5}$ of the flows |

For them the page stores five more numbers, each on a line that already existed, so no line number moved: `as`, the
acceleration measured from the stored velocities by a central difference, $a_n = (v_{n+1} - v_{n-1})/2\Delta t$, one-sided at
the two ends (declared [L674](../../public/simulations/driven-oscillator.html#L674), allocated [L936](../../public/simulations/driven-oscillator.html#L936), written [L938](../../public/simulations/driven-oscillator.html#L938)); `E0`, the energy at $t = 0$
([L969](../../public/simulations/driven-oscillator.html#L969)); and `ma_now`, `bal_now`, `fres_now`, written with the other playback values ([L1542](../../public/simulations/driven-oscillator.html#L1542), declared
[L704](../../public/simulations/driven-oscillator.html#L704)). The Newton book misses by the error of the central difference, of order $(\Omega\Delta t)^2/6$. While your
hand holds the block, or after a run that blew up, both books say they are paused instead of giving a verdict. The ledger file
also adds checks the page lacked: each of the 16 `*_now` numbers against its stored row (or "from the drag" while held), `as`,
`ma_now`, `E0`, `bal_now`, `fres_now`, `stable` and `fp_kind`; all answer "identical" (measured 24 October 2026).
`Sim.data.colour` shades the `xs` and `Fs` table cells with `Sim.colourMap`
([L1707](../../public/simulations/driven-oscillator.html#L1707), defined in
[datalog.js:103](../../public/scripts/datalog.js#L103)); this is presentation only.

**One round** (`Sim.data.round`, [L1914–L1916](../../public/simulations/driven-oscillator.html#L1914-L1916)) is one drive
period, $1/f$ seconds of the stored run, timed by `t_play`. Its columns are `x_now`, `v_now`, `u_now`, `F_now`, `Fc_now`, `Fk_now`, `E_now`, `Pin_now`;
the default point is the block. Recording is refused when fewer than $1/f$ seconds of the run remain ("press From t = 0").
The panel samples every frame of the round, at most 600 samples ([datalog.js:1052](../../public/scripts/datalog.js#L1052)).

**`Sim.live()`** ([L1517–L1531](../../public/simulations/driven-oscillator.html#L1517-L1531)) returns formatted strings read from
the store, for the keys the walkthrough uses: `k`, `c`, `W`, `w0`, `h`, `steps`, `n`, `t`, `x`, `v`, `F`, `E`, `X`, `phi`,
`err`, `Win`, `Wloss`, `bal`, `bx`, `sc`, `I0`, `I`, `BL`, `Fc`, `Fk`, `fN`, `span`, `Wc`, `Qc`, `u`, `r`, `Kp`, `Ki`, `Kd`, `z`, `xeq`. The walkthrough polls it every 200 ms
([sim.js:403](../../public/scripts/sim.js#L403)).

**Check and read-back.** `Sim.data.check` ([L1744–L1858](../../public/simulations/driven-oscillator.html#L1744-L1858))
recomputes every stored value from its stored inputs; for the ODE solution (`xs`, `vs`) and the run integrals (`Win`,
`Wloss`) it reruns the same RK4 from $t = 0$ (`rk4Replay`, up to 60 000 steps). `Sim.data.drawn`
([L1859–L1913](../../public/simulations/driven-oscillator.html#L1859-L1913)) reads pixels back: the burgundy block, the
three force arrows (or their absence below 2 px), the energy bars, the controller's $u$ bar, the target dot, the equilibrium line, the previous run's dotted curve, $x_n$ and $F_n/k$ on the charts, and the Bode curves and dots (plant dashed grey when the loop is on).
`probe` ([L1708–L1717](../../public/simulations/driven-oscillator.html#L1708-L1717)) pins the block when the click is within
40 px across and 34 px up or down of its centre, otherwise the nearest stored sample within 16 px (outside the window chart
only every fifth sample is tried). How the panel uses these hooks is in [datalog.md](../scripts/datalog.md).

## Page structure

**Head** ([L3–L43](../../public/simulations/driven-oscillator.html#L3-L43)): title "Driven Oscillator · Numa Koudsie",
description, the security policy and referrer rule ([build-and-deploy.md](../build-and-deploy.md#security)), then the stylesheets `../styles/sim.css`, `../styles/data.css`,
`../styles/fold.css` ([L11–L12](../../public/simulations/driven-oscillator.html#L11-L12)), an inline SVG favicon, and a
small inline style for the solve box (`.solve`, `.solve__steps`, `.solve__status`, `.seek`,
[L15–L42](../../public/simulations/driven-oscillator.html#L15-L42)). Styles are described in [styles.md](../styles.md).

**Body**, in order:
- `header.sim-top`: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`,
  87 × 48) and the back link "← All simulations" ([L46](../../public/simulations/driven-oscillator.html#L46)), then the hand-written Fig. 1–11 links, Fig. 9
  marked `aria-current` ([L45–L61](../../public/simulations/driven-oscillator.html#L45-L61));
- `.sim__head`: "Fig. 9 · control systems · forced oscillations", the `h1` and the lede
  ([L65–L69](../../public/simulations/driven-oscillator.html#L65-L69));
- `.sim__grid`: the main figure `#stage` with `canvas#osc` and a caption holding the equation and `#cap-t`
  ([L107–L115](../../public/simulations/driven-oscillator.html#L107-L115)); the Bode figure `#stage-bode` with `canvas#bode` and
  `#cap-res` ([L116–L142](../../public/simulations/driven-oscillator.html#L116-L142)); the control panel `aside.panel` with the
  solve box, the sliders, six readouts and a legend ([L145–L213](../../public/simulations/driven-oscillator.html#L145-L213)).
  The **Read values** switch is added to the first caption by datalog.js;
- `article.paper#paper`, the lecture note ([L216–L589](../../public/simulations/driven-oscillator.html#L216-L589)):
  abstract; thirteen sections `.psec` (counted 29 October 2026) — 01 A push from outside, 02 The model, 03 The exact
  solution ★ (3.1 The steady state, 3.2 The transient), 04 Resonance and phase, 05 The control engineer's view ★, 06 The
  start: beats and decay, 07 Where the energy goes, 08 Solve first, then play, 09 The driver: a coil in a magnet, 10 Closing
  the loop, 11 Phase space and stable points, 12 On screen, 13 What the model leaves out (13.1 Further reading, five items,
  each with a link). Twenty-two numbered equations, `\tag{1}`–`\tag{21}` and `\tag{6a}` (the completed square that locates the
  resonance peak, [L400](../../public/simulations/driven-oscillator.html#L400)). Four figures with five inline SVGs: Figure 1 the plant sketch
  ([L248–L277](../../public/simulations/driven-oscillator.html#L248-L277)), Figure 2 amplitude and phase against $f/f_0$ for
  four damping ratios (two SVGs, [L308–L396](../../public/simulations/driven-oscillator.html#L308-L396)), Figure 3 the block
  diagram ([L415–L433](../../public/simulations/driven-oscillator.html#L415-L433)), Figure 4 the default run
  ([L439–L487](../../public/simulations/driven-oscillator.html#L439-L487)). Two exercise boxes, 4.1 and 6.1;
- `section#walk` with `data-walk="driven"` ([L591](../../public/simulations/driven-oscillator.html#L591)), filled by
  `sim.js` from `walk/driven.js` ([sim.js:481–490](../../public/scripts/sim.js#L481-L490)); see [walk.md](../scripts/walk.md);
- footer; then the scripts in load order: `fold.js`, `sim.js`, `dataset.js`, the page's inline script, `datalog.js`
  ([L599–L1930](../../public/simulations/driven-oscillator.html#L599-L1930)). Folds are described in
  [fold.md](../scripts/fold.md), the shared helpers in [sim.md](../scripts/sim.md).

The walkthrough's seven steps quote these page lines: step 1 [L887](../../public/simulations/driven-oscillator.html#L887);
step 2 [L883–L885](../../public/simulations/driven-oscillator.html#L883-L885); step 3
[L913–L916](../../public/simulations/driven-oscillator.html#L913-L916) and
[L922–L923](../../public/simulations/driven-oscillator.html#L922-L923); step 4
[L905–L910](../../public/simulations/driven-oscillator.html#L905-L910); step 5
[L919–L920](../../public/simulations/driven-oscillator.html#L919-L920) and
[L969](../../public/simulations/driven-oscillator.html#L969); step 6
[L818–L819](../../public/simulations/driven-oscillator.html#L818-L819) and
[L931](../../public/simulations/driven-oscillator.html#L931); step 7
[L1556](../../public/simulations/driven-oscillator.html#L1556), [L1534](../../public/simulations/driven-oscillator.html#L1534),
[L1354](../../public/simulations/driven-oscillator.html#L1354). All seven excerpts match the page text at present.

## Where the drawing and the store differ

The page states the differences in `Sim.data.about` ([L1918](../../public/simulations/driven-oscillator.html#L1918)), which
the data panel prints. In detail:

- **Nearest row, no interpolation.** `t_play` runs continuously, but the picture shows row
  $\operatorname{round}(t_\text{play}/10\,\text{ms})$ ([L1534](../../public/simulations/driven-oscillator.html#L1534)). The
  caption shows the row's time `ts[i]`, not `t_play` ([L1543](../../public/simulations/driven-oscillator.html#L1543)).
- **Overview strip thinned.** The strip of the whole run draws every `stride`-th row,
  `stride = max(1, floor(NS / (2 × strip width)))` ([L1330](../../public/simulations/driven-oscillator.html#L1330)): every 4th
  row at a 770 px canvas, every 10th at 356 px. The window chart draws every row between its edges
  ([L1286](../../public/simulations/driven-oscillator.html#L1286)).
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
- **Phase space.** `eigen(p)` returns the roots of $m\lambda^2 + (c+K_d)\lambda + (k+K_p)$, or with $K_i > 0$ of the cubic
  (the real root by Newton from $-a_0/a_1$, the pair from the remaining quadratic), and the kind of fixed point;
  `solve()` stores them with $|\mu| = e^{\max\mathrm{Re}\,\lambda/f}$, the orbit `orb_x`, `orb_v` (181 points) and the strobe
  flags; `field()` stores the arrow grid (15 × 11) and the portrait's height `vlim` whenever the span changes.
- **Target flag.** A press within 16 px of the flag on the ruler drags $r$ (rounded to 0.01 m, clamped to the slider's range);
  on release, and on the `change` event of the $r$ slider, the page solves from the row on screen (`fromNow()`).
- **Spring constant.** The slider `kspring` (1.5–90 N/m, step 0.01, default 9.87) sets $k$; the page keeps an object `f0`
  whose `value` is $\sqrt{k/m}/2\pi$, so the rest of the code is unchanged.
- **Controller.** The RK4 state is $(x, v, z)$ with $z = \int (r-x)\,dt$; `control()` is evaluated at all four stages. The
  exact solution that grades RK4 is `exactClosed()` when any gain is above zero: particular solution (16) plus the free
  motion propagated with the matrix exponential of the loop's state matrix (`expm`, scaling and squaring). An unstable loop
  is solved until $|x| > 1000$ m (`t_blow`); the rest of the run holds that state.
- **Old item, superseded:** *Drawing scale changes with the run.* The block travels at most `amp = 0.11 × W0` pixels either side of rest, where
  `W0` is the width between wall and right margin, so `px_per_m = amp / xmax` differs from run to run
  ([L1069](../../public/simulations/driven-oscillator.html#L1069), [L1075](../../public/simulations/driven-oscillator.html#L1075)).
  The ruler under the floor shows $\pm$`xmax` in metres ([L1172](../../public/simulations/driven-oscillator.html#L1172)).
- **Force arrow.** Its length is $F_n/F_0 \cdot L_F$ with $L_F = \min(88, 0.12\,w)$ px; arrows shorter than 2 px are not
  drawn ([L1164](../../public/simulations/driven-oscillator.html#L1164)).
- **Dial.** The arm points at the stored $\Omega t_n \bmod 2\pi$ ([L1177](../../public/simulations/driven-oscillator.html#L1177)).
- **Bode plot.** The dot sits at the exact $|G(i\Omega)|$ and $\varphi$; the ring is the amplitude measured from the last
  10 s of the stored run, per newton ([L1509–L1511](../../public/simulations/driven-oscillator.html#L1509-L1511)). With the
  defaults they differ by 0.03 % (0.48194 against 0.48209 m/N), the remains of the transient.
- **Rounding.** Canvas labels and readouts round (for example $F$ to 2 decimals, $x$ to 3); the store keeps full doubles.

## How to change it safely

- **Run length, step and storage stride.** `TEND`, `H` and `EVERY` ([L606](../../public/simulations/driven-oscillator.html#L606))
  determine `NS`. Keep `TEND / H` and `TEND / H / EVERY` whole numbers, because `step === TEND / H` and `step % EVERY` decide
  the last row ([L904–L911](../../public/simulations/driven-oscillator.html#L904-L911)). These places repeat the numbers by
  hand and must change with them: the seek slider `max="6000"` ([L162](../../public/simulations/driven-oscillator.html#L162));
  the `formula` texts "n · 10 h", "t_n ≥ 50 s", "round(t_play / 10h)" ([L658](../../public/simulations/driven-oscillator.html#L658),
  [L685](../../public/simulations/driven-oscillator.html#L685), [L689](../../public/simulations/driven-oscillator.html#L689));
  the group note "every 10 ms of the 60 s" ([L1701](../../public/simulations/driven-oscillator.html#L1701)); the check text
  "at most 6000" ([L1840](../../public/simulations/driven-oscillator.html#L1840)); the 10 s tick step of the overview
  ([L1346](../../public/simulations/driven-oscillator.html#L1346)); the walkthrough's "step / 10", "60 000 steps" and
  "6 001 rows" ([driven.js:169–170](../../public/scripts/walk/driven.js#L169-L170)); the lecture note section 8
  ([L505–L507](../../public/simulations/driven-oscillator.html#L505-L507)) and `about`.
- **The integrator exists twice.** `solve()` ([L913–L924](../../public/simulations/driven-oscillator.html#L913-L924)) and
  `rk4Replay()` ([L1636–L1647](../../public/simulations/driven-oscillator.html#L1636-L1647)) must stay identical, line for line,
  or the data panel's Check of `xs`, `vs`, `Win` and `Wloss` will no longer agree with the store.
- **Walkthrough excerpts.** The seven excerpts listed under Page structure are quoted verbatim in `walk/driven.js`. If one
  of those page lines changes, change the excerpt in the same edit. Insert new code after a quoted line, never inside a
  quoted group (AGENTS.md).
- **Taps stay where values are computed.** Write a new number into the store at the line that computes it, declare it with
  `ds.var` next to its relatives, add it to a group in `Sim.data.groups`, and give it a `check` (and a `drawn` if it is on
  screen). Do not compute numbers inside `draw*()` beyond the metre-to-pixel conversion.
- **Lecture-note numbers.** Sections 2–9 quote values for the default sliders ([L174–L190](../../public/simulations/driven-oscillator.html#L174-L190)),
  and Figures 2 and 4 are static SVGs computed from the page's formulas. Changing a default or the physics means
  recomputing them.
- **Damping limit.** `exact()` divides by $\omega_d = \omega_0\sqrt{1-\zeta^2}$; the slider stops at 0.9. Allowing
  $\zeta \ge 1$ needs a different exact solution (section 10 says so, [L575](../../public/simulations/driven-oscillator.html#L575)).
- **Frequency range.** The Bode axis covers 0.05–2 Hz ([L1003](../../public/simulations/driven-oscillator.html#L1003),
  [L1473](../../public/simulations/driven-oscillator.html#L1473)); raising the $f_0$ or $f$ slider beyond 2 Hz would put the
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
   ([L1560](../../public/simulations/driven-oscillator.html#L1560)), so a paused page still redraws about 60 times a second
   (about 1.5 ms per frame measured) and rewrites `#cap-t` each time ([L1543](../../public/simulations/driven-oscillator.html#L1543)).
7. Fixed on 2026-10-15: the note gives the measured default solve time of 9.5–12.4 ms and states that timing depends on the machine (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
8. **AGENTS.md** said the load order dataset.js → page → datalog.js holds for "all eight figures"; this page (Fig. 9)
   follows it too. Corrected to "all ten figures" on 14 October 2026.


## Teaching revision · 15 October 2026

The note separates undamped natural frequency from damped ringing, interprets the complex denominator as spring, inertia and quadrature damping, and uses the damped ringing frequency for the approximate default beat time. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16: the paragraph reading the complex denominator had been placed between "(2) turns into algebra:" and equation (3); it now follows (3) and ends "gives the form in (3)" ([L296](../../public/simulations/driven-oscillator.html#L296)). See the [audit of the revision](../research-theory-audit.md).

Fixed on 2026-10-16 (second repairs): the Millennium Bridge is back as the counter-example to a prescribed force (the walkers' steps fed back on the sway); the beat-time sentence is one sentence again ([L247](../../public/simulations/driven-oscillator.html#L247)). See the [audit of the revision](../research-theory-audit.md).

## Teaching revision · 20 October 2026

Judged section by section against [notes/STANDARD.md](../../notes/STANDARD.md); the verdicts and measurements are in
[notes/fig09/plan.md](../../notes/fig09/plan.md). Sections 1, 2 and 8, the text of section 6 and the limits in section 10 were left as they were. Filled in: the step from (3)
to (4), with `atan2` named and the real part justified ([L297](../../public/simulations/driven-oscillator.html#L297)); the
roots $s = -\zeta\omega_0 \pm i\omega_0\sqrt{1-\zeta^2}$ of the free equation, which give $\tau$, $\omega_d$ and the meaning of
$\zeta = 1$, and the two starting conditions behind $C_1$, $C_2$ ([L300](../../public/simulations/driven-oscillator.html#L300));
the completed square (6a) that places the peak at $\Omega_r = \omega_0\sqrt{1-2\zeta^2}$, with $f_r = 0.4987$ Hz now named as a
frequency in hertz ([L399–L401](../../public/simulations/driven-oscillator.html#L399-L401)); the sign of the poles' real part,
$-1/\tau$ ([L413](../../public/simulations/driven-oscillator.html#L413)); the origin of $\tfrac12 c\,\Omega^2X^2$
([L498](../../public/simulations/driven-oscillator.html#L498)). Corrected: Exercise 6.1 said the transient "hardly shows" at
$f = 0.20$ Hz; the force switches on at full strength, so the ringing starts as large as the steady motion (measured at
$\zeta = 0.01$: $\sqrt{C_1^2+C_2^2} = 1.00005\,X$, $|x|$ up to $0.224$ m $= 1.85\,X$ at 5 s)
([L490](../../public/simulations/driven-oscillator.html#L490)); section 9 described one 60 s chart, but the dashed $F/k$ and
$\pm X$ belong to the moving window ($\operatorname{clamp}(4/f, 6, 20)$ s, 8.9 s with the defaults) above the 60 s strip
([L514](../../public/simulations/driven-oscillator.html#L514)). Further reading now links every item and adds Feynman,
Vol. I, chapters 23 and 24 ([L580–L584](../../public/simulations/driven-oscillator.html#L580-L584)).

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig09/`), the lead made only these changes, each on its existing line, so no line link moved: §2: ω_d no longer used before ζ is defined ([L284](../../public/simulations/driven-oscillator.html#L284)); §3.2: the ringing written before its constants are fixed ([L300](../../public/simulations/driven-oscillator.html#L300)); §5: X(s), F(s) named as transforms ([L411](../../public/simulations/driven-oscillator.html#L411)); Figure 3: the plant box widened so G(s) fits ([L421](../../public/simulations/driven-oscillator.html#L421)); §9: every run drawn at its own scale; compare runs on the ruler ([L514](../../public/simulations/driven-oscillator.html#L514)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

## Second check round · 20 October 2026

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig09/`), each change on its existing line: §3.1: the driving term, not the force, is the real part of (F₀/m)e^{iΩt} ([L294](../../public/simulations/driven-oscillator.html#L294)); equation (3) reflowed so its number shows at 1600 px ([L295](../../public/simulations/driven-oscillator.html#L295)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.

## Layout · 30 October 2026

As on Fig. 11, from a page width of 1200 px (a 1280 px window) the grid has three columns: the "Take control" box (presets,
target r, the three gains) on the left, the four figures in the middle, the panel on the right. Both side columns are
`position: sticky` and scroll inside themselves when taller than the window. CSS only, appended to line 39 of the page's own
`<style>` (the first column's wrapper becomes `display: contents`; its section and four figures are placed in the grid); no
HTML moved and the page keeps 1934 lines. Below 1200 px the page is as before, with the panel now pinned beside the figures
from 901 px (`sim.css`, for every page). Computed from the CSS, not yet measured in a browser: the main figure is 696 × 531 px at
1440 × 900 (1052 × 802 before), the price of having every knob beside it. See [../styles.md](../styles.md), "Simulation pages use
the whole screen".

