# Fig. 10 · Wind Turbine Control

| | |
|---|---|
| Page | [public/simulations/wind-turbine.html](../../public/simulations/wind-turbine.html) (1 154 lines, 174 597 bytes) |
| Walkthrough | [public/scripts/walk/turbine.js](../../public/scripts/walk/turbine.js) (121 lines, 7 steps, key `turbine`) |
| Thumbnail | [public/images/sims/wind-turbine.webp](../../public/images/sims/wind-turbine.webp) (WebP, 800 × 500 px, 15.4 kB) |
| Catalog entry | [public/scripts/catalog.js#L200](../../public/scripts/catalog.js#L200-L216) (`id: 'wind-turbine'`, `fig: 10`, `field: 'control'`, `stage: 2`, lines 200–216) |

A three-bladed rotor with 40 m blades turns in a wind that changes with time. A generator brakes it, and a controller sets
how hard: either hold the rotor at a target speed (a PI controller) or let it follow the wind at the best tip-speed ratio
(the optimal-torque law). The reader picks the controller, the target speed, one of four winds (steady, gust, step,
turbulent), the mean wind and the size of the change, presses **Solve**, and watches two stored minutes play back: the
turning rotor in passing air, a table of the present values, three strip charts (wind, rotor speed, power) and the
operating point on the power-coefficient curve. As in Fig. 9, the whole run is solved first with the classical fourth-order
Runge–Kutta method (RK4) and stored; each frame then draws one stored row. Nothing is integrated while the reader watches.

In this page, a link such as [L696](../../public/simulations/wind-turbine.html#L696) points to a line of
`wind-turbine.html`. Other files are named in the link text.

## The physics in one picture

**What you would see.** A paper windmill held out of a car window spins faster the faster the car goes. A turbine is the
same toy, scaled up, with a brake on its shaft. Brake too little and it races; brake too hard and it slows until the wind
slips past. The brake is the generator, and the power it takes is the electricity.

**The model.** The rotor is one rigid body with moment of inertia $J$. Two torques act on it: the wind's, which drives, and
the generator's, which brakes. Newton's law for a rotation is

$$J\,\frac{\mathrm d\omega}{\mathrm dt} = \tau_\text{aero}(\omega, v(t)) - \tau_\text{gen} .$$

The wind $v(t)$ is a function of time alone (a drive, as in Fig. 9). The generator torque is chosen from the measured
$\omega$ (feedback). The lecture note covers the power in the wind (section 2,
[L211](../../public/simulations/wind-turbine.html#L211)), the Betz limit 16/27 (section 3), the tip-speed ratio and the
power-coefficient fit (section 4), this equation and its energy form (section 5), the two controllers (section 6) and their
comparison (section 7).

**What the code evaluates.** The tip-speed ratio is $\lambda = \omega R/v$. The power coefficient is Heier's fit with the
blades at zero pitch, `cp()` ([L643–L649](../../public/simulations/wind-turbine.html#L643-L649)):

$$c_p(\lambda) = \max\!\left(0,\ c_1\left(\frac{c_2}{\lambda_i}-c_4\right)e^{-c_5/\lambda_i} + c_6\lambda\right),\qquad \frac1{\lambda_i} = \frac1\lambda - 0.035,$$

with $c_1 = 0.5176$, $c_2 = 116$, $c_4 = 5$, $c_5 = 21$, $c_6 = 0.0068$
([L556](../../public/simulations/wind-turbine.html#L556)); it returns 0 for $\lambda \le 0.05$ and when
$1/\lambda - 0.035 \le 0$. The fit becomes negative above $\lambda = 13.40$, where the `max` clips it to 0 (measured). The
aerodynamic torque is `tauAero()` ([L650–L652](../../public/simulations/wind-turbine.html#L650-L652)):

$$\tau_\text{aero}(\omega, v) = \frac{\tfrac12\rho A v^3\,c_p(\omega R/v)}{\omega}\quad(\omega > 10^{-6}\ \text{rad/s, else } 0),\qquad A = \pi R^2 .$$

`optimum()` ([L653–L661](../../public/simulations/wind-turbine.html#L653-L661)) scans $\lambda$ from 0.5 to 14 in steps of
0.001 and stores $\lambda_\text{opt} = 8.100$ and $c_{p,\max} = 0.48001$, then the optimal-torque gain
$K_\text{opt} = \tfrac12\rho\pi R^5 c_{p,\max}/\lambda_\text{opt}^3 = 1.78\times10^5$ N m s².

The generator torque is `tauGen()` ([L681–L684](../../public/simulations/wind-turbine.html#L681-L684)):

$$\text{follow the wind:}\quad \tau_\text{gen} = \min(\tau_\max,\ K_\text{opt}\,\omega^2),$$
$$\text{hold speed:}\quad \tau_\text{gen} = \min\!\big(\tau_\max,\ \max(0,\ \tau_0 + K_p(\omega-\omega_\text{ref}) + K_i I)\big),\qquad \dot I = \omega - \omega_\text{ref} .$$

The integral $I$ (unit rad) stops growing while the torque sits at a limit (anti-windup): its rate is 0 when following the
wind, when the unclipped torque is $\le 0$ and the error is negative, or when it is $\ge \tau_\max$ and the error is positive
([L687–L688](../../public/simulations/wind-turbine.html#L687-L688)). The PI gains come from linearising the rotor equation
around the target in the mean wind, a damped oscillator with natural frequency $\omega_n$ and damping ratio $\zeta_c$
([L698–L699](../../public/simulations/wind-turbine.html#L698-L699)):

$$K_i = J\omega_n^2,\qquad K_p = 2\zeta_c\omega_n J + \frac{\partial\tau_\text{aero}}{\partial\omega}\Big|_{\omega_\text{ref},\,v_0},\qquad \tau_0 = \tau_\text{aero}(\omega_\text{ref}, v(0)),$$

where the slope is a central difference with $\delta\omega = 10^{-4}$ rad/s, and $\tau_0$ makes the run start in balance
([L697](../../public/simulations/wind-turbine.html#L697)).

The wind `wind(t, w)` ([L666–L678](../../public/simulations/wind-turbine.html#L666-L678)) is one of four profiles, all
functions of time only:

| Profile | $v(t)$ | Lines |
|---|---|---|
| steady | $v_0$ | [L677](../../public/simulations/wind-turbine.html#L677) |
| gust | $v_0 - 0.37\,\Delta v\,\sin(3\pi s/T)\,(1-\cos(2\pi s/T))$ for $0 \le s = t-30\ \text{s} \le T = 10.5$ s, else $v_0$ (the IEC gust shape cited in the note) | [L667–L670](../../public/simulations/wind-turbine.html#L667-L670) |
| step | $v_0 + \Delta v\cdot\text{clamp}((t-30\ \text{s})/2\ \text{s}, 0, 1)$: a 2 s ramp starting at 30 s | [L671](../../public/simulations/wind-turbine.html#L671) |
| turbulent | $\max\!\big(0.5,\ v_0 + \Delta v\,u(t)/N\big)$, $u = \sum_{k=0}^{15} a_k\sin(2\pi f_k t + \phi_k)$, $f_k = 0.005\cdot100^{k/15}$ Hz, $a_k = f_k^{-1/3}$, $N = \sqrt{\sum a_k^2/2}$, fixed phases $\phi_k$ | [L557](../../public/simulations/wind-turbine.html#L557), [L664–L665](../../public/simulations/wind-turbine.html#L664-L665), [L672–L676](../../public/simulations/wind-turbine.html#L672-L676) |

$N$ is the root mean square of the sum over a long time, so $\Delta v$ is the standard deviation $\sigma$ of the wind; over
the 120 s run the default wind measures 1.30 m/s for $\sigma = 1.5$ m/s, as the Figure 4 caption says.

| Symbol | Meaning | Value or unit | In code |
|---|---|---|---|
| $\rho$ | air density | 1.225 kg/m³ | `RHO` ([L554](../../public/simulations/wind-turbine.html#L554)) |
| $R$, $A$ | blade length, swept area | 40 m, 5 026.5 m² | `R`, `AREA` |
| $J$ | moment of inertia of rotor and drive train | 4.0 × 10⁶ kg m² | `J` |
| $\tau_\max$ | largest generator torque | 1.2 × 10⁶ N m | `TMAX` |
| $\omega_n$, $\zeta_c$ | PI design: natural frequency, damping ratio | 0.6 rad/s, 0.8 | `WN`, `ZC` |
| $\omega$, $\theta$ | rotor speed, rotor angle | rad/s, rad | `w`, `y[4]` |
| $v$, $v_0$, $\Delta v$ | wind speed, mean wind, size of change | m/s | `v`, `v0.value`, `dv.value` |
| $\omega_\text{ref}$ | target speed, from the rpm slider | rad/s | `c.wref` |
| $\tau_\text{aero}$, $\tau_\text{gen}$ | torques | N m | `a`, `g` in `rates()` |
| $I$ | the controller's memory, $\int(\omega-\omega_\text{ref})\,\mathrm dt$ | rad | `I` |
| $h$ | RK4 step | 0.01 s | `H` ([L555](../../public/simulations/wind-turbine.html#L555)) |

## How the code computes it

### Constants and state

[L554–L557](../../public/simulations/wind-turbine.html#L554-L557) hold the turbine, the controller design and the run:
`H = 0.01` s, `TEND = 120` s, `EVERY = 2`, `NS = TEND / H / EVERY + 1`, `NL = 271`. In JavaScript `120 / 0.01` is exactly
12 000, so `NS` is exactly 6 001 (checked in Node). The page's own state is
[L563](../../public/simulations/wind-turbine.html#L563): `playT`, `iNow`, `frames`, `fps`, `solved`, the controller
`ctrl = 'pi'`, the wind profile `prof = 'turb'` and `AIRPX = 5` (pixels per metre of air in the drawing).

### 1 Solve: RK4 on a seven-component state

`solve()` ([L693–L739](../../public/simulations/wind-turbine.html#L693-L739)) first collects the settings into `c`
([L696](../../public/simulations/wind-turbine.html#L696)), computes $\tau_0$, the aerodynamic slope and the gains
([L697–L699](../../public/simulations/wind-turbine.html#L697-L699)) and allocates 15 arrays
([L700–L701](../../public/simulations/wind-turbine.html#L700-L701)). The run starts in balance
([L702–L703](../../public/simulations/wind-turbine.html#L702-L703)): when following the wind at
$\omega = \lambda_\text{opt}v(0)/R$, when holding speed at $\omega = \omega_\text{ref}$ with $\tau_\text{gen} = \tau_0$;
$I = 0$, and the start energy $\tfrac12J\omega^2$ is kept as `KE0`.

The right-hand side is `rates(t, w, I, c)` ([L685–L690](../../public/simulations/wind-turbine.html#L685-L690)). It returns
seven slopes:

$$\frac{\mathrm d}{\mathrm dt}\big(\omega,\ I,\ E_\text{gen},\ E_\text{aero},\ E_\text{wind},\ s_\text{air},\ \theta\big) = \Big(\frac{\tau_\text{aero}-\tau_\text{gen}}{J},\ \dot I,\ \tau_\text{gen}\omega,\ \tau_\text{aero}\omega,\ \tfrac12\rho A v^3,\ v,\ \omega\Big).$$

Only $\omega$ and $I$ feed back into the slopes; the other five are quadratures (running integrals) kept in the array `y`.
One step ([L713–L720](../../public/simulations/wind-turbine.html#L713-L720)) evaluates `rates` four times, at $t$, twice at
$t+h/2$ and at $t+h$, advancing only $(\omega, I)$ between the stages, and then updates all seven with the RK4 weights
$\tfrac h6(k_1+2k_2+2k_3+k_4)$. Time is set from the step count, `t = (step + 1) * H`
([L720](../../public/simulations/wind-turbine.html#L720)). Note that `tauGen` reads $K_\text{opt}$ from the store at every
stage ([L682](../../public/simulations/wind-turbine.html#L682)), so `optimum()` must have run first.

Why RK4 with $h = 10$ ms: the code does not state the reason. What can be measured is the margin. When holding speed the
linearised error equation (equation (10) of the note) has eigenvalues of modulus $\omega_n = 0.6$ s⁻¹ with damping ratio
0.8; when following the wind the relaxation rate at the optimum is 0.11–0.30 s⁻¹ for winds of 4–11 m/s (computed with the
page's own functions). So $|\lambda| h \le 0.01$, far inside RK4's stable region, and the fastest wind component (0.5 Hz) gets 200 steps
per period. The torque clipping and the anti-windup switch make the right-hand side non-smooth at the limits; the code does
nothing special there. With the defaults the energy balance $E_\text{aero} = E_\text{gen} + \Delta(\tfrac12 J\omega^2)$ holds
to $8.2\times10^{-13}$ (measured; between 0 and $8.2\times10^{-13}$ for all eight combinations of controller and wind).

### 2 Store: every second state

The loop runs `step = 0 … 12 000` ([L704](../../public/simulations/wind-turbine.html#L704)). At the top of each pass, before
the step, every second state is written into the dataset ([L705–L710](../../public/simulations/wind-turbine.html#L705-L710)):
time, wind, $\omega$, rpm, $\theta$, $\lambda$, $c_p$, both torques, both powers, $E_\text{gen}$, $s_\text{air}$, $I$ and
the tip speed $\omega R$. The derived columns are computed at that moment with the same `cp`, `tauAero` and `tauGen` the
integrator uses. Row $n$ is the state at $t_n = n\cdot 2h = n\cdot 20$ ms. After storing step 12 000 the loop stops
([L711](../../public/simulations/wind-turbine.html#L711)): 12 000 RK4 steps, 6 001 rows.

After the loop: arrays marked changed ([L722](../../public/simulations/wind-turbine.html#L722)); chart ranges from the run's
extremes ([L723–L726](../../public/simulations/wind-turbine.html#L723-L726)); the final kinetic energy
([L727](../../public/simulations/wind-turbine.html#L727)); settings, gains, energies, mean power and the balance
([L728–L734](../../public/simulations/wind-turbine.html#L728-L734)); the `solved` snapshot, readouts, `playT = 0` and play
([L735–L738](../../public/simulations/wind-turbine.html#L735-L738)).

The arrays come from `ds.alloc`, which reuses an array when its length is unchanged
([dataset.js:67](../../public/scripts/dataset.js#L67)), so a re-solve overwrites them in place. Memory, measured from the
live store: 15 arrays × 6 001 × 8 B = 720 120 B for the run plus 2 × 271 × 8 B = 4 336 B for the $c_p$ curve, 724 456 B in
all. One solve took 10–46 ms in headless Chromium (`solve_ms`, [L695](../../public/simulations/wind-turbine.html#L695),
[L734](../../public/simulations/wind-turbine.html#L734)).

### When the run is solved again

At load, `optimum()` then `solve()` ([L1161–L1162](../../public/simulations/wind-turbine.html#L1161-L1162)); afterwards only
when **Solve** is pressed ([L968](../../public/simulations/wind-turbine.html#L968)). `optimum()` never runs again. Sliders
([L636–L638](../../public/simulations/wind-turbine.html#L636-L638)) and the two button groups
([L977](../../public/simulations/wind-turbine.html#L977)) only call `markStale()`
([L741–L745](../../public/simulations/wind-turbine.html#L741-L745)), which compares controller, wind, $v_0$, $\Delta v$ and,
when holding speed, the target with `solved`, sets `stale` and rewrites the status line
([L747–L754](../../public/simulations/wind-turbine.html#L747-L754)). The old run keeps playing.

### 3 Play: the frame loop, in order

`Sim.clock` ([sim.js:177–198](../../public/scripts/sim.js#L177-L198)) calls the tick on every `requestAnimationFrame`, with
$\Delta t \le 0.05$ s, and $\Delta t = 0$ while paused. Each tick:

1. returns if nothing is solved; smooths the frame rate; advances `playT += speed · Δt`; at 120 s clamps and pauses; stores
   `fps` and `playing`; marks "3 play" ([L958–L966](../../public/simulations/wind-turbine.html#L958-L966));
2. `frame()` ([L947–L957](../../public/simulations/wind-turbine.html#L947-L957)) picks row
   $n = \operatorname{round}(t_\text{play}/20\,\text{ms})$, clamped to 0 … 6 000, writes `i_now`, `t_play` and the six
   `*_now` copies of row $n$, moves the seek slider and the caption time, then calls `draw()` and `drawCp()`;
3. `draw()` ([L890–L904](../../public/simulations/wind-turbine.html#L890-L904)) gets the layout from `geom()`, stores the hub
   position, the blade length in pixels and the canvas size, clears, and draws `drawScene` and three `drawStrip` calls
   (wind, rotor speed, power), then the time cursor and labels;
4. `drawCp()` ([L910–L933](../../public/simulations/wind-turbine.html#L910-L933)) redraws the second canvas: grid, Betz and
   $\lambda_\text{opt}$ lines, the stored $c_p$ curve, the trail and dot of the operating point, and rewrites `#cap-op`.

No step of this chain integrates; the only arithmetic turns metres, seconds, radians and watts into pixels. Because the clock
ticks every animation frame, the figure is redrawn at the display rate even while paused; one `frame()` took about 1.4 ms
(measured over 200 seek events at a 1 440 px wide window).

### Precomputation and caching

- The $c_p$ curve (`lamL`, `cpL`, 271 points from $\lambda$ = 0.5 to 14.0) is computed once in `optimum()`
  ([L657–L659](../../public/simulations/wind-turbine.html#L657-L659)).
- The 16 frequencies and amplitudes of the turbulent wind and their norm are computed once at load
  ([L664–L665](../../public/simulations/wind-turbine.html#L664-L665)).
- `fullReplay()` reruns the whole 120 s once for the data panel's Check of $E_\text{aero}$, $E_\text{wind}$ and
  $E_\text{gen}(T)$ and caches the result under the run's settings ([L1013–L1017](../../public/simulations/wind-turbine.html#L1013-L1017)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `cp(lam)` | [643–649](../../public/simulations/wind-turbine.html#L643-L649) | Heier's power coefficient, clipped at 0. |
| `tauAero(w, v)` | [650–652](../../public/simulations/wind-turbine.html#L650-L652) | Aerodynamic torque $\tfrac12\rho Av^3c_p/\omega$. |
| `optimum()` | [653–661](../../public/simulations/wind-turbine.html#L653-L661) | Scans $\lambda$ for the peak; stores $\lambda_\text{opt}$, $c_{p,\max}$, 16/27, $K_\text{opt}$, the curve, and $\rho$, $R$, $J$. |
| (wind tables) | [664–665](../../public/simulations/wind-turbine.html#L664-L665) | `TF`, `TA`, `TNORM` of the turbulent wind. |
| `wind(t, w)` | [666–678](../../public/simulations/wind-turbine.html#L666-L678) | The four wind profiles. |
| `tauGen(w, I, c)` | [681–684](../../public/simulations/wind-turbine.html#L681-L684) | Generator torque of the chosen controller, clipped to 0 … $\tau_\max$. |
| `rates(t, w, I, c)` | [685–690](../../public/simulations/wind-turbine.html#L685-L690) | The seven slopes, with anti-windup. |
| `solve()` | [693–739](../../public/simulations/wind-turbine.html#L693-L739) | Solve and store the two minutes (see above). |
| `markStale()` | [741–745](../../public/simulations/wind-turbine.html#L741-L745) | Sets `stale` when a control differs from the last solve. |
| `status()` | [747–754](../../public/simulations/wind-turbine.html#L747-L754) | Status line and "1 solve / 2 store" marks; names from `NAMES` ([L746](../../public/simulations/wind-turbine.html#L746)). |
| `readouts()` | [755–763](../../public/simulations/wind-turbine.html#L755-L763) | Mean power, energy in kWh, rotor-speed range, captured share, balance, solve time. |
| `geom()` | [767–782](../../public/simulations/wind-turbine.html#L767-L782) | Layout: scene height, rotor radius and hub, six air lines, three strips, ranges, maps `sx`, `sy`. |
| `label(c, sym, value, …)` | [783–793](../../public/simulations/wind-turbine.html#L783-L793) | A symbol via `Sim.tex`, then its value in IBM Plex Mono. |
| `bladePath(c, g, a)` | [794–801](../../public/simulations/wind-turbine.html#L794-L801) | Outline of one blade at angle `a`, horizontal shortened by `K`. |
| `drawScene(c, g, i)` | [802–852](../../public/simulations/wind-turbine.html#L802-L852) | Air streaks, ground, tower, nacelle, swept disc, three blades, spinner, wind label and arrow, value table. |
| `drawStrip(c, g, i, name, …)` | [853–889](../../public/simulations/wind-turbine.html#L853-L889) | One strip chart: ticks, target line, $P_\text{aero}$ under $P_\text{gen}$, faint future, dark past, dot, title and value. |
| `draw()` | [890–904](../../public/simulations/wind-turbine.html#L890-L904) | One frame of the main canvas. |
| `cpGeom()` | [906–909](../../public/simulations/wind-turbine.html#L906-L909) | Layout of the $c_p$ chart: $\lambda$ 0–14, $c_p$ 0–0.65. |
| `drawCp()` | [910–933](../../public/simulations/wind-turbine.html#L910-L933) | The $c_p$ chart with the operating point and a 3 s trail. |
| `Sim.live()` | [936–945](../../public/simulations/wind-turbine.html#L936-L945) | Formatted store values for the walkthrough. |
| `frame()` | [947–957](../../public/simulations/wind-turbine.html#L947-L957) | Picks the stored row, copies it to the `*_now` scalars, draws both canvases. |
| clock tick (anonymous) | [958–966](../../public/simulations/wind-turbine.html#L958-L966) | Advances `playT`, stops at 120 s, calls `frame()`. |
| `segmented(id, set)` | [970–979](../../public/simulations/wind-turbine.html#L970-L979) | Button group: sets `aria-pressed`, calls `set`, marks stale. |
| `controls()` | [981–985](../../public/simulations/wind-turbine.html#L981-L985) | Greys the target slider unless holding speed, greys $\Delta v$ for steady wind, relabels it (`DVL`, [L980](../../public/simulations/wind-turbine.html#L980)). |
| `stripPos(name, n)` | [992–995](../../public/simulations/wind-turbine.html#L992-L995) | Screen point of row $n$ on the strip that shows `name` (`STRIP_OF`, [L991](../../public/simulations/wind-turbine.html#L991)). |
| `rk4Replay(n)` | [996–1011](../../public/simulations/wind-turbine.html#L996-L1011) | The same RK4 rerun from $t = 0$ to row $n$; the Check of `om`, `Ictl`, `th`, `sw`, `Eg`. |
| `fullReplay()` | [1013–1017](../../public/simulations/wind-turbine.html#L1013-L1017) | Cached `rk4Replay(6000)`. |
| `at`, `maxOf`, `minOf`, `neutralInk`, `isRose`, `readBack` | [1018–1026](../../public/simulations/wind-turbine.html#L1018-L1026) | Small helpers for Check and read-back. |
| `bladePixel()` | [1027–1032](../../public/simulations/wind-turbine.html#L1027-L1032) | Reads back a pixel 60 % along the burgundy blade. |
| `stripDot(name, label)`, `stripCurve(name, label)` | [1033–1045](../../public/simulations/wind-turbine.html#L1033-L1045) | Read-back of the dot and of a curve sample on a strip. |
| `airPixel()` | [1046–1053](../../public/simulations/wind-turbine.html#L1046-L1053) | Read-back of a dash on the second air line. |
| `Sim.data` (object) | [1054–1159](../../public/simulations/wind-turbine.html#L1054-L1159) | The data-panel contract. |
| start-up | [1161–1165](../../public/simulations/wind-turbine.html#L1161-L1165) | `optimum()`, `solve()`, resize observers, redraw when fonts are ready. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Solve | `solve` | button | `solve()` ([L968](../../public/simulations/wind-turbine.html#L968)). |
| Pause / Play | `play` | button | Toggles the clock via `Sim.playButton` ([L967](../../public/simulations/wind-turbine.html#L967)). |
| From t = 0 | `restart` | button | `playT = 0` and play ([L969](../../public/simulations/wind-turbine.html#L969)). |
| Stored run | `seek` | 0–6000, step 1, default 0 ([L94](../../public/simulations/wind-turbine.html#L94)) | `playT = n · 20 ms`, draw ([L640](../../public/simulations/wind-turbine.html#L640)); follows playback ([L953](../../public/simulations/wind-turbine.html#L953)). |
| Playback speed | `speed` | 0.5–8, step 0.5, default 1 ([L98](../../public/simulations/wind-turbine.html#L98)) | Multiplies $\Delta t$ ([L961](../../public/simulations/wind-turbine.html#L961)). |
| Controller | `ctrl` (buttons `data-v="pi"` / `"opt"`) | Hold speed (default, [L105](../../public/simulations/wind-turbine.html#L105), [L563](../../public/simulations/wind-turbine.html#L563)) / Follow the wind | `ctrl` ([L986](../../public/simulations/wind-turbine.html#L986)), used by `tauGen` and the start speed; marks stale. |
| Target rotor speed | `rpm` | 8–21 rpm, step 0.5, default 15 ([L110](../../public/simulations/wind-turbine.html#L110)) | $\omega_\text{ref} = \text{rpm}\cdot2\pi/60$ at the next solve ([L696](../../public/simulations/wind-turbine.html#L696)); greyed and not marking stale when following the wind ([L742](../../public/simulations/wind-turbine.html#L742), [L982](../../public/simulations/wind-turbine.html#L982)). |
| Wind | `prof` (buttons `steady`, `gust`, `step`, `turb`) | Turbulent (default, [L120](../../public/simulations/wind-turbine.html#L120), [L563](../../public/simulations/wind-turbine.html#L563)) | `prof` ([L987](../../public/simulations/wind-turbine.html#L987)), read by `wind()`; marks stale. |
| Mean wind speed $v_0$ | `v0` | 4–11 m/s, step 0.1, default 8 ([L124](../../public/simulations/wind-turbine.html#L124)) | `c.v0`; marks stale. |
| Turbulence σ / Gust size / Step size | `dv` | 0–4 m/s, step 0.1, default 1.5 ([L128](../../public/simulations/wind-turbine.html#L128)) | `c.dv`; label set by `controls()`; unused for steady wind; marks stale. |
| Read values | added by datalog.js | switch, off | Appended to the first figure caption ([datalog.js:591–593](../../public/scripts/datalog.js#L591-L593)); see [datalog.md](../scripts/datalog.md). |

## What the page writes into the data store

The store is made at [L566](../../public/simulations/wind-turbine.html#L566):
`Sim.dataset({ title: 'Wind turbine control', attrs: { figure: 10, page, equation, cp_model } })`. It has two dimensions,
`n` = 6 001 rows ([L591](../../public/simulations/wind-turbine.html#L591)) and `L` = 271 points of the $c_p$ curve
([L620](../../public/simulations/wind-turbine.html#L620)), and 66 variables: 49 scalars and 17 `Float64Array`s, declared at
[L567–L634](../../public/simulations/wind-turbine.html#L567-L634) (counted in the live store). The store is described in
[dataset.md](../scripts/dataset.md). By the panel groups of [L1057–L1066](../../public/simulations/wind-turbine.html#L1057-L1066):

| Group | Variables | Written at |
|---|---|---|
| Turbine | `rho`, `R`, `J`; `lam_opt`, `cp_max`, `cp_betz`, `K_opt` | `optimum()`, [L660](../../public/simulations/wind-turbine.html#L660); [L656](../../public/simulations/wind-turbine.html#L656) |
| Settings | `ctrl`, `profile`, `v0`, `dv`, `w_ref`; `rpm_ref` | [L728](../../public/simulations/wind-turbine.html#L728); [L725](../../public/simulations/wind-turbine.html#L725) |
| Controller | `dtau_dw`, `Kp`, `Ki`, `tau0` | [L729](../../public/simulations/wind-turbine.html#L729) |
| Stored run (dim `n`) | `ts` (coordinate), `vw`, `om`, `rpm`, `th`, `lam`, `cpv`; `ta`, `tg`, `Pg`, `Pa`, `Eg`, `sw`, `Ictl`, `vtip` | [L707](../../public/simulations/wind-turbine.html#L707); [L708](../../public/simulations/wind-turbine.html#L708) |
| Energy | `Ea`, `Ew`, `Eg_end`, `P_mean`; `balance`; `solve_ms`, `stale` | [L732](../../public/simulations/wind-turbine.html#L732); [L733](../../public/simulations/wind-turbine.html#L733); [L734](../../public/simulations/wind-turbine.html#L734), `stale` also [L743](../../public/simulations/wind-turbine.html#L743) |
| Playback | `i_now`, `t_play`, `v_now`, `rpm_now`, `P_now`, `lam_now`, `cp_now`, `th_now` | `frame()`, [L950–L952](../../public/simulations/wind-turbine.html#L950-L952) |
| Power curve (dim `L`) | `lamL` (coordinate), `cpL` | `optimum()`, [L658](../../public/simulations/wind-turbine.html#L658) |
| Drawing | `v_hi`, `rpm_lo`, `rpm_hi`; `P_hi`, `px_per_m_air` | [L725](../../public/simulations/wind-turbine.html#L725); [L726](../../public/simulations/wind-turbine.html#L726) |
| | `hub_x`, `hub_y`, `r_px`, `box_w`, `box_h` | `draw()`, [L892](../../public/simulations/wind-turbine.html#L892) |
| | `fps`, `playing` | clock tick, [L963](../../public/simulations/wind-turbine.html#L963) |

$E_\text{aero}$ and $E_\text{wind}$ are kept only as run totals; $E_\text{gen}$ is stored at every row (`Eg`) and as a total.
With the defaults (hold speed, turbulent wind) the store holds: $E_\text{aero}$ = 88.97 MJ, $E_\text{wind}$ = 200.90 MJ,
$E_\text{gen}(T)$ = 89.04 MJ (24.73 kWh), mean power 742 kW, $K_p = 3.592\times10^6$ N m s,
$\partial\tau_\text{aero}/\partial\omega = -2.480\times10^5$ N m s, $K_i = 1.44\times10^6$ N m, $\tau_0 = 3.343\times10^5$ N m.

**One round** (`Sim.data.round`, [L1154–L1156](../../public/simulations/wind-turbine.html#L1154-L1156)) is one turn of the
rotor at the present speed, $60/n_\text{rot}$ seconds of the stored run (4.0 s at 15 rpm), timed by `t_play`. Columns:
`v_now`, `rpm_now`, `P_now`, `lam_now`, `cp_now`, `th_now`; the default point is the rotor. Recording is refused when the run
ends before one more turn. The panel samples every frame of the round, at most 600 samples
([datalog.js:747](../../public/scripts/datalog.js#L747)).

**`Sim.live()`** ([L936–L945](../../public/simulations/wind-turbine.html#L936-L945)) returns formatted strings read from the
store for the walkthrough keys `lam`, `cp`, `lopt`, `cpmax`, `Kopt`, `v`, `w`, `ta`, `tg`, `Pg`, `wref`, `Kp`, `Ki`, `dtd`,
`n`, `t`, `th`, `Eg`, `bal`; row-valued keys use `i_now`. The walkthrough polls it every 200 ms
([sim.js:400](../../public/scripts/sim.js#L400)).

`rpm_ref` is the raw rpm input captured by `solve()`, rather than a round-trip conversion of `w_ref`. Check of `w_ref` converts this stored input; changing the live target cannot change the check of an already solved run. All 27 target values from 8 to 21 turns per minute were checked and were bit-identical.

**Check and read-back.** `Sim.data.check` ([L1086–L1134](../../public/simulations/wind-turbine.html#L1086-L1134)) recomputes
each value from stored inputs; the integrated quantities (`om`, `Ictl`, `th`, `sw`, `Eg`) are checked by rerunning the same
RK4 to row $n$, the totals by `fullReplay()`, and `lam_opt` by repeating the scan. `Sim.data.drawn`
([L1135–L1153](../../public/simulations/wind-turbine.html#L1135-L1153)) reads back the burgundy blade, the dots and curves
of the strips ($P_\text{aero}$ with a rose-colour test), a dash of the air, the operating point and the $c_p$ curve. `probe`
([L1067–L1074](../../public/simulations/wind-turbine.html#L1067-L1074)) pins the rotor when the click falls inside the drawn
disc ellipse, otherwise the nearest stored sample within 14 px on the three strips (every second row is tried). `locate`
maps quantities that have no chart of their own to a strip that does (`STRIP_OF`: $\omega$, $\lambda$, $c_p$, $\theta$ to the
rotor-speed strip, the torques to the power strip, [L991](../../public/simulations/wind-turbine.html#L991)).

## Page structure

**Head** ([L3–L29](../../public/simulations/wind-turbine.html#L3-L29)): title "Wind Turbine Control · Numa Koudsie",
description, preconnect to Google Fonts, stylesheets `../styles/sim.css`, `../styles/data.css`, `../styles/fold.css`
([L11–L13](../../public/simulations/wind-turbine.html#L11-L13)), inline SVG favicon, and an inline style for the solve box,
the seek slider, the segmented buttons `.seg` and the greyed control `.ctl.is-off`
([L15–L28](../../public/simulations/wind-turbine.html#L15-L28)). Styles are described in [styles.md](../styles.md).

**Body**, in order:
- `header.sim-top` with the Fig. 1–10 links, Fig. 10 marked `aria-current` ([L31–L46](../../public/simulations/wind-turbine.html#L31-L46));
- `.sim__head`: "Fig. 10 · control systems · wind energy", `h1`, lede ([L50–L54](../../public/simulations/wind-turbine.html#L50-L54));
- `.sim__grid`: the main figure `#stage` with `canvas#wt` and a caption with the equation and `#cap-t`
  ([L58–L66](../../public/simulations/wind-turbine.html#L58-L66)); the operating-point figure `#stage-cp` with `canvas#cp`
  and `#cap-op` ([L67–L75](../../public/simulations/wind-turbine.html#L67-L75)); `aside.panel` with the solve box, the
  controller and wind groups, six readouts and a legend ([L78–L147](../../public/simulations/wind-turbine.html#L78-L147)).
  **Read values** is added to the first caption by datalog.js;
- `article.paper#paper` ([L150–L537](../../public/simulations/wind-turbine.html#L150-L537)): abstract; ten sections — 01 From
  wind to electricity, 02 The power in the wind, 03 The Betz limit ★, 04 Tip-speed ratio, 05 The rotor's equation of motion,
  06 Two controllers ★ (6.1 Follow the wind: the optimal-torque law, 6.2 Hold speed: a PI controller), 07 Same wind, two
  answers, 08 Solve first, then play, 09 On screen, 10 What the model leaves out (10.1 Further reading). Ten numbered
  equations, `\tag{1}`–`\tag{10}`. Four figures with six inline SVGs: Figure 1 the stream tube
  ([L179–L208](../../public/simulations/wind-turbine.html#L179-L208)), Figure 2 the $c_p$ curve
  ([L239–L290](../../public/simulations/wind-turbine.html#L239-L290)), Figure 3 the control loop
  ([L301–L332](../../public/simulations/wind-turbine.html#L301-L332)), Figure 4 wind, rotor speed and power for both
  controllers (three SVGs, [L352–L481](../../public/simulations/wind-turbine.html#L352-L481)). A Betz-limit box
  ([L227–L230](../../public/simulations/wind-turbine.html#L227-L230)), a table of all eight controller–wind combinations
  ([L483–L495](../../public/simulations/wind-turbine.html#L483-L495)) and exercise 7.1;
- `section#walk` with `data-walk="turbine"` ([L539](../../public/simulations/wind-turbine.html#L539)), filled from
  `walk/turbine.js` by `sim.js` ([sim.js:476–486](../../public/scripts/sim.js#L476-L486)); see [walk.md](../scripts/walk.md);
- footer; scripts in load order: `fold.js`, `sim.js`, `dataset.js`, the inline page script, `datalog.js`
  ([L547–L1168](../../public/simulations/wind-turbine.html#L547-L1168)). See [sim.md](../scripts/sim.md) and
  [fold.md](../scripts/fold.md).

The walkthrough quotes: step 1 [L643–L649](../../public/simulations/wind-turbine.html#L643-L649); step 2
[L650–L652](../../public/simulations/wind-turbine.html#L650-L652); step 3
[L681–L684](../../public/simulations/wind-turbine.html#L681-L684); step 4
[L698–L699](../../public/simulations/wind-turbine.html#L698-L699); step 5
[L689](../../public/simulations/wind-turbine.html#L689) and [L713–L717](../../public/simulations/wind-turbine.html#L713-L717);
step 6 [L707–L708](../../public/simulations/wind-turbine.html#L707-L708) (the second line only in part, see the notes);
step 7 [L948](../../public/simulations/wind-turbine.html#L948) and [L826](../../public/simulations/wind-turbine.html#L826).
The table in section 7 ([L486–L493](../../public/simulations/wind-turbine.html#L486-L493)) was reproduced exactly, all eight
rows, by solving each combination in the page (measured).

## Where the drawing and the store differ

The page states this in `Sim.data.about` ([L1158](../../public/simulations/wind-turbine.html#L1158)). In detail:

- **Nearest row, no interpolation.** The picture shows row $\operatorname{round}(t_\text{play}/20\,\text{ms})$
  ([L948](../../public/simulations/wind-turbine.html#L948)); the caption shows `ts[i]` to one decimal
  ([L954](../../public/simulations/wind-turbine.html#L954)).
- **Rotor seen at an angle.** The swept disc and each blade have their horizontal extent multiplied by `K = 0.5`
  ([L766](../../public/simulations/wind-turbine.html#L766), [L796](../../public/simulations/wind-turbine.html#L796),
  [L823](../../public/simulations/wind-turbine.html#L823)). Blade 1 (burgundy) is at the stored $\theta$, the others at
  $\theta + 2\pi/3$ and $\theta + 4\pi/3$ ([L825–L829](../../public/simulations/wind-turbine.html#L825-L829)). The blade
  outline, tower and nacelle are a sketch in units of the drawn radius, not to scale.
- **Air streaks.** Six dashed lines with fixed 16 px dashes and 22 px gaps; their offset is $-s_\text{air}\times5$ px/m, each
  line 15 px further into the pattern than the one above ([L766](../../public/simulations/wind-turbine.html#L766),
  [L774](../../public/simulations/wind-turbine.html#L774), [L805–L807](../../public/simulations/wind-turbine.html#L805-L807)).
  They pass through the rotor unchanged; the slowing of the air is not drawn.
- **Wind arrow** at the top left: $6 + 3.2\,v$ px long ([L835](../../public/simulations/wind-turbine.html#L835)).
- **Strips thinned and clamped.** Each strip draws every `stride`-th row, `stride = max(1, floor(NS / (2 × strip width)))`
  ([L854](../../public/simulations/wind-turbine.html#L854)): every 4th row at a 770 px canvas, every 10th at 356 px. Values are
  clamped to the strip's range ([L780](../../public/simulations/wind-turbine.html#L780)); the ranges come from the run's own
  extremes, so with the stored run nothing is clamped.
- **$c_p$ chart.** Axes 0–14 and 0–0.65 ([L908](../../public/simulations/wind-turbine.html#L908)); the trail is the last 150
  rows (3 s), every third row ([L925–L926](../../public/simulations/wind-turbine.html#L925-L926)).
- **Rounding.** The value table rounds ($n_\text{rot}$ to 2 decimals, torques to whole kN m, power to whole kW,
  [L839–L851](../../public/simulations/wind-turbine.html#L839-L851)); on narrow screens it shows four rows instead of seven.

## How to change it safely

- **Run length, step and stride.** `TEND`, `H`, `EVERY` ([L555](../../public/simulations/wind-turbine.html#L555)) give `NS`.
  Keep `TEND / H` and `TEND / H / EVERY` whole numbers. Change with them: seek `max="6000"`
  ([L94](../../public/simulations/wind-turbine.html#L94)); formula texts "n · 2h" and "round(t_play / 2h)"
  ([L592](../../public/simulations/wind-turbine.html#L592), [L612](../../public/simulations/wind-turbine.html#L612)); group
  note "every 20 ms of the 120 s" ([L1061](../../public/simulations/wind-turbine.html#L1061)); check text "at most 6000"
  ([L1125](../../public/simulations/wind-turbine.html#L1125)); time labels every 20 s
  ([L902](../../public/simulations/wind-turbine.html#L902)); the 150-row trail
  ([L925](../../public/simulations/wind-turbine.html#L925)); the walkthrough step 6 note and step 7 formula
  ([turbine.js:96–97](../../public/scripts/walk/turbine.js#L96-L97), [turbine.js:110](../../public/scripts/walk/turbine.js#L110));
  the note's sections 8 and 9 ([L507–L509](../../public/simulations/wind-turbine.html#L507-L509),
  [L515](../../public/simulations/wind-turbine.html#L515)) and `about`.
- **The integrator exists twice.** The start state and the step in `solve()`
  ([L702](../../public/simulations/wind-turbine.html#L702), [L713–L720](../../public/simulations/wind-turbine.html#L713-L720))
  and in `rk4Replay()` ([L999](../../public/simulations/wind-turbine.html#L999),
  [L1001–L1008](../../public/simulations/wind-turbine.html#L1001-L1008)) must stay identical, or the Checks of the integrated
  columns will disagree.
- **Order at start-up.** `optimum()` must run before `solve()` ([L1161–L1162](../../public/simulations/wind-turbine.html#L1161-L1162)):
  `solve()` reads `lam_opt` for the start speed and `tauGen` reads `K_opt` from the store.
- **Defaults in two places.** `ctrl = 'pi'` and `prof = 'turb'` ([L563](../../public/simulations/wind-turbine.html#L563)) must
  match the buttons marked `aria-pressed="true"` ([L105](../../public/simulations/wind-turbine.html#L105),
  [L120](../../public/simulations/wind-turbine.html#L120)).
- **Physics constants are quoted elsewhere.** $c_1$…$c_6$ ([L556](../../public/simulations/wind-turbine.html#L556)) also
  appear in the `cp_model` attribute ([L566](../../public/simulations/wind-turbine.html#L566)), walkthrough step 1
  ([turbine.js:13](../../public/scripts/walk/turbine.js#L13)) and the note ([L237–L238](../../public/simulations/wind-turbine.html#L237-L238)).
  `WN` and `ZC` appear in the note ([L346](../../public/simulations/wind-turbine.html#L346)) and walkthrough step 4
  ([turbine.js:63–64](../../public/scripts/walk/turbine.js#L63-L64)). `AIRPX`, `K` and `DASH` appear in `about`, in the
  `airPixel` note ([L1052](../../public/simulations/wind-turbine.html#L1052)) and in walkthrough step 7
  ([turbine.js:111](../../public/scripts/walk/turbine.js#L111)).
- **The turbulent wind is fixed.** `PHASES` ([L557](../../public/simulations/wind-turbine.html#L557)) make every solve use the
  same turbulence; Figure 4 and the section 7 table depend on them. Changing the phases, the wind, the controller or the
  turbine means recomputing those numbers and SVGs.
- **Walkthrough excerpts.** Keep the page lines listed under Page structure identical to `walk/turbine.js`; insert new code
  after a quoted line, never inside a quoted group (AGENTS.md).
- **Taps.** Write each new number into the store where it is computed, declare it with `ds.var`, add it to a group, and give
  it a `check` (and a `drawn` if it is on screen).
- **Re-test** in a browser at a wide and a phone-width window: no console error; with the defaults the readouts show 742 kW,
  24.73 kWh, 14.4–15.7 rpm, 44.3 %, balance below $10^{-12}$; switch controller and wind and see the stale status; Solve
  each; drag **Stored run**; open the Data panel and Check `om` at a row, `Ea`, `balance`, `th_now` (blade read-back) and
  `sw` (air dash); pin the rotor with **Read values**; record one round.

## Notes for maintainers

1. Fixed on 2026-10-15: the note gives K = 0.5, 5 px/m airflow and the fixed 16 px / 22 px dash pattern (commit `:/^Batch B: correct notes and layout; verify measured figures in Chromium$`).
2. Fixed on 2026-10-15: the quoted storage line includes Ic[n] and vt[n] (commit `:/^Batch C: align walkthroughs and metadata; verify excerpts and stored values$`).
3. Fixed on 2026-10-15: w_ref is checked against the saved rpm input, including Follow the wind; all target steps recompute identically after live controls change (commit `:/^Batch A: fix simulation and recording faults; verify in Chromium$`).
4. Fixed on 2026-10-15: the Figure 2 labels render p and opt as SVG subscripts (commit `:/^Batch B: correct notes and layout; verify measured figures in Chromium$`).
5. Fixed on 2026-10-15: solve stores h, steps, rpm_min, rpm_max and captured_pct; displays only read them (commit `:/^Batch D: store computed results once; verify values and pixel readbacks$`).
6. **Dead code.** `frames` is counted ([L960](../../public/simulations/wind-turbine.html#L960)) but never read.
7. **Redraw while paused.** The clock ticks every animation frame with $\Delta t = 0$ while paused
   ([sim.js:179–186](../../public/scripts/sim.js#L179-L186)) and the tick always calls `frame()`
   ([L965](../../public/simulations/wind-turbine.html#L965)), so both canvases are redrawn about 60 times a second while
   paused (about 1.4 ms per frame measured), and `#cap-op` and `#cap-t` are rewritten each frame
   ([L932](../../public/simulations/wind-turbine.html#L932), [L954](../../public/simulations/wind-turbine.html#L954)).
8. **AGENTS.md** said the load order dataset.js → page → datalog.js holds for "all eight figures"; this page (Fig. 10)
   follows it too. Corrected to "all ten figures" on 14 October 2026.

Batch D store additions in `solve()`: `h` (s), `steps` (count), `rpm_min` and `rpm_max` (turns per minute), and `captured_pct` (%). They appear in the Energy group, have recomputation checks and DOM readbacks. The step readback infers h from the visible sampling interval and EVERY = 2. The speed range is the sampled run range, independent of the wider chart bounds. `readouts()` no longer computes these results.
