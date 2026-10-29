# Fig. 10 · Wind Turbine Control

| | |
|---|---|
| Page | [public/simulations/wind-turbine.html](../../public/simulations/wind-turbine.html) (1 172 lines, 187 918 bytes) |
| Walkthrough | [public/scripts/walk/turbine.js](../../public/scripts/walk/turbine.js) (281 lines, 13 steps, key `turbine`) |
| Thumbnail | [public/images/sims/wind-turbine.webp](../../public/images/sims/wind-turbine.webp) (WebP, 800 × 500 px, 15.4 kB) |
| Catalog entry | [public/scripts/catalog.js#L200](../../public/scripts/catalog.js#L200-L233) (`id: 'wind-turbine'`, `fig: 10`, `field: 'control'`, `stage: 2`, lines 200–216) |

A three-bladed rotor with 40 m blades turns in a wind that changes with time. A generator brakes it, and a controller sets
how hard: either hold the rotor at a target speed (a PI controller) or let it follow the wind at the best tip-speed ratio
(the optimal-torque law). The reader picks the controller, the target speed, one of four winds (steady, gust, step,
turbulent), the mean wind and the size of the change, presses **Solve**, and watches two stored minutes play back: the
turning rotor in passing air, a table of the present values, three strip charts (wind, rotor speed, power) and the
operating point on the power-coefficient curve. As in Fig. 9, the whole run is solved first with the classical fourth-order
Runge–Kutta method (RK4) and stored; each frame then draws one stored row. Nothing is integrated while the reader watches.

In this page, a link such as [L697](../../public/simulations/wind-turbine.html#L697) points to a line of
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
[L212](../../public/simulations/wind-turbine.html#L212)), the Betz limit 16/27 (section 3), the tip-speed ratio and the
power-coefficient fit (section 4), this equation and its energy form (section 5), the two controllers (section 6) and their
comparison (section 7).

**What the code evaluates.** The tip-speed ratio is $\lambda = \omega R/v$. The power coefficient is Heier's fit with the
blades at zero pitch, `cp()` ([L644–L650](../../public/simulations/wind-turbine.html#L644-L650)):

$$c_p(\lambda) = \max\!\left(0,\ c_1\left(\frac{c_2}{\lambda_i}-c_4\right)e^{-c_5/\lambda_i} + c_6\lambda\right),\qquad \frac1{\lambda_i} = \frac1\lambda - 0.035,$$

with $c_1 = 0.5176$, $c_2 = 116$, $c_4 = 5$, $c_5 = 21$, $c_6 = 0.0068$
([L557](../../public/simulations/wind-turbine.html#L557)); it returns 0 for $\lambda \le 0.05$ and when
$1/\lambda - 0.035 \le 0$. The fit becomes negative above $\lambda = 13.40$, where the `max` clips it to 0 (measured). The
aerodynamic torque is `tauAero()` ([L651–L653](../../public/simulations/wind-turbine.html#L651-L653)):

$$\tau_\text{aero}(\omega, v) = \frac{\tfrac12\rho A v^3\,c_p(\omega R/v)}{\omega}\quad(\omega > 10^{-6}\ \text{rad/s, else } 0),\qquad A = \pi R^2 .$$

`optimum()` ([L654–L662](../../public/simulations/wind-turbine.html#L654-L662)) scans $\lambda$ from 0.5 to 14 in steps of
0.001 and stores $\lambda_\text{opt} = 8.100$ and $c_{p,\max} = 0.48001$, then the optimal-torque gain
$K_\text{opt} = \tfrac12\rho\pi R^5 c_{p,\max}/\lambda_\text{opt}^3 = 1.78\times10^5$ N m s².

The generator torque is `tauGen()` ([L682–L685](../../public/simulations/wind-turbine.html#L682-L685)):

$$\text{follow the wind:}\quad \tau_\text{gen} = \min(\tau_\max,\ K_\text{opt}\,\omega^2),$$
$$\text{hold speed:}\quad \tau_\text{gen} = \min\!\big(\tau_\max,\ \max(0,\ \tau_0 + K_p(\omega-\omega_\text{ref}) + K_i I)\big),\qquad \dot I = \omega - \omega_\text{ref} .$$

The integral $I$ (unit rad) stops growing while the torque sits at a limit (anti-windup): its rate is 0 when following the
wind, when the unclipped torque is $\le 0$ and the error is negative, or when it is $\ge \tau_\max$ and the error is positive
([L688–L689](../../public/simulations/wind-turbine.html#L688-L689)). The PI gains come from linearising the rotor equation
around the target in the mean wind, a damped oscillator with natural frequency $\omega_n$ and damping ratio $\zeta_c$
([L699–L700](../../public/simulations/wind-turbine.html#L699-L700)):

$$K_i = J\omega_n^2,\qquad K_p = 2\zeta_c\omega_n J + \frac{\partial\tau_\text{aero}}{\partial\omega}\Big|_{\omega_\text{ref},\,v_0},\qquad \tau_0 = \tau_\text{aero}(\omega_\text{ref}, v(0)),$$

where the slope is a central difference with $\delta\omega = 10^{-4}$ rad/s, and $\tau_0$ makes the run start in balance
([L698](../../public/simulations/wind-turbine.html#L698)).

The wind `wind(t, w)` ([L667–L679](../../public/simulations/wind-turbine.html#L667-L679)) is one of four profiles, all
functions of time only:

| Profile | $v(t)$ | Lines |
|---|---|---|
| steady | $v_0$ | [L678](../../public/simulations/wind-turbine.html#L678) |
| gust | $v_0 - 0.37\,\Delta v\,\sin(3\pi s/T)\,(1-\cos(2\pi s/T))$ for $0 \le s = t-30\ \text{s} \le T = 10.5$ s, else $v_0$ (the IEC gust shape cited in the note) | [L668–L671](../../public/simulations/wind-turbine.html#L668-L671) |
| step | $v_0 + \Delta v\cdot\text{clamp}((t-30\ \text{s})/2\ \text{s}, 0, 1)$: a 2 s ramp starting at 30 s | [L672](../../public/simulations/wind-turbine.html#L672) |
| turbulent | $\max\!\big(0.5,\ v_0 + \Delta v\,u(t)/N\big)$, $u = \sum_{k=0}^{15} a_k\sin(2\pi f_k t + \phi_k)$, $f_k = 0.005\cdot100^{k/15}$ Hz, $a_k = f_k^{-1/3}$, $N = \sqrt{\sum a_k^2/2}$, fixed phases $\phi_k$ | [L558](../../public/simulations/wind-turbine.html#L558), [L665–L666](../../public/simulations/wind-turbine.html#L665-L666), [L673–L677](../../public/simulations/wind-turbine.html#L673-L677) |

$N$ is the root mean square of the sum over a long time, so $\Delta v$ is the standard deviation $\sigma$ of the wind; over
the 120 s run the default wind measures 1.30 m/s for $\sigma = 1.5$ m/s, as the Figure 4 caption says.

| Symbol | Meaning | Value or unit | In code |
|---|---|---|---|
| $\rho$ | air density | 1.225 kg/m³ | `RHO` ([L555](../../public/simulations/wind-turbine.html#L555)) |
| $R$, $A$ | blade length, swept area | 40 m, 5 026.5 m² | `R`, `AREA` |
| $J$ | moment of inertia of rotor and drive train | 4.0 × 10⁶ kg m² | `J` |
| $\tau_\max$ | largest generator torque | 1.2 × 10⁶ N m | `TMAX` |
| $\omega_n$, $\zeta_c$ | PI design: natural frequency, damping ratio | 0.6 rad/s, 0.8 | `WN`, `ZC` |
| $\omega$, $\theta$ | rotor speed, rotor angle | rad/s, rad | `w`, `y[4]` |
| $v$, $v_0$, $\Delta v$ | wind speed, mean wind, size of change | m/s | `v`, `v0.value`, `dv.value` |
| $\omega_\text{ref}$ | target speed, from the rpm slider | rad/s | `c.wref` |
| $\tau_\text{aero}$, $\tau_\text{gen}$ | torques | N m | `a`, `g` in `rates()` |
| $I$ | the controller's memory, $\int(\omega-\omega_\text{ref})\,\mathrm dt$ | rad | `I` |
| $h$ | RK4 step | 0.01 s | `H` ([L556](../../public/simulations/wind-turbine.html#L556)) |

## How the code computes it

### Constants and state

[L555–L558](../../public/simulations/wind-turbine.html#L555-L558) hold the turbine, the controller design and the run:
`H = 0.01` s, `TEND = 120` s, `EVERY = 2`, `NS = TEND / H / EVERY + 1`, `NL = 271`. In JavaScript `120 / 0.01` is exactly
12 000, so `NS` is exactly 6 001 (checked in Node). The page's own state is
[L564](../../public/simulations/wind-turbine.html#L564): `playT`, `iNow`, `fps`, `solved`, the controller
`ctrl = 'pi'`, the wind profile `prof = 'turb'` and `AIRPX = 5` (pixels per metre of air in the drawing).

### 1 Solve: RK4 on a seven-component state

`solve()` ([L694–L740](../../public/simulations/wind-turbine.html#L694-L740)) first collects the settings into `c`
([L697](../../public/simulations/wind-turbine.html#L697)), computes $\tau_0$, the aerodynamic slope and the gains
([L698–L700](../../public/simulations/wind-turbine.html#L698-L700)) and allocates 15 arrays
([L701–L701](../../public/simulations/wind-turbine.html#L701-L701)). The run starts in balance
([L703–L704](../../public/simulations/wind-turbine.html#L703-L704)): when following the wind at
$\omega = \lambda_\text{opt}v(0)/R$, when holding speed at $\omega = \omega_\text{ref}$ with $\tau_\text{gen} = \tau_0$;
$I = 0$, and the start energy $\tfrac12J\omega^2$ is kept as `KE0`.

The right-hand side is `rates(t, w, I, c)` ([L686–L691](../../public/simulations/wind-turbine.html#L686-L691)). It returns
seven slopes:

$$\frac{\mathrm d}{\mathrm dt}\big(\omega,\ I,\ E_\text{gen},\ E_\text{aero},\ E_\text{wind},\ s_\text{air},\ \theta\big) = \Big(\frac{\tau_\text{aero}-\tau_\text{gen}}{J},\ \dot I,\ \tau_\text{gen}\omega,\ \tau_\text{aero}\omega,\ \tfrac12\rho A v^3,\ v,\ \omega\Big).$$

Only $\omega$ and $I$ feed back into the slopes; the other five are quadratures (running integrals) kept in the array `y`.
One step ([L714–L721](../../public/simulations/wind-turbine.html#L714-L721)) evaluates `rates` four times, at $t$, twice at
$t+h/2$ and at $t+h$, advancing only $(\omega, I)$ between the stages, and then updates all seven with the RK4 weights
$\tfrac h6(k_1+2k_2+2k_3+k_4)$. Time is set from the step count, `t = (step + 1) * H`
([L721](../../public/simulations/wind-turbine.html#L721)). Note that `tauGen` reads $K_\text{opt}$ from the store at every
stage ([L683](../../public/simulations/wind-turbine.html#L683)), so `optimum()` must have run first.

Why RK4 with $h = 10$ ms: the code does not state the reason; the note gives it in section 8, item 1 ([L508](../../public/simulations/wind-turbine.html#L508)). What can be measured is the margin. When holding speed the
linearised error equation (equation (10) of the note) has eigenvalues of modulus $\omega_n = 0.6$ s⁻¹ with damping ratio
0.8; when following the wind the relaxation rate at the optimum is 0.11–0.30 s⁻¹ for winds of 4–11 m/s (computed with the
page's own functions). So $|\lambda| h \le 0.01$, far inside RK4's stable region, and the fastest wind component (0.5 Hz) gets 200 steps
per period. The torque clipping and the anti-windup switch make the right-hand side non-smooth at the limits; the code does
nothing special there. With the defaults the energy balance $E_\text{aero} = E_\text{gen} + \Delta(\tfrac12 J\omega^2)$ holds
to $8.2\times10^{-13}$ (measured; between 0 and $8.2\times10^{-13}$ for all eight combinations of controller and wind). The step study, run in the page itself with only L555 changed: solving again with $h = 5$ ms (`EVERY = 4`, so the 6 001 rows fall at the same times) changes the stored $\omega$ by at most $2.0\times10^{-11}$ rpm (defaults), and $h = 20$ ms changes it 16.0 times as much, the factor $2^4$ of a fourth-order method; no run of the section 7 table brings the generator torque to 0 or to $\tau_\max$ (largest 916 kN m, smallest 32 kN m, both with hold speed in turbulent wind). Scripts: `notes/fig10/measure.cjs`, `notes/fig10/cp_checks.cjs`.

### 2 Store: every second state

The loop runs `step = 0 … 12 000` ([L705](../../public/simulations/wind-turbine.html#L705)). At the top of each pass, before
the step, every second state is written into the dataset ([L706–L711](../../public/simulations/wind-turbine.html#L706-L711)):
time, wind, $\omega$, rpm, $\theta$, $\lambda$, $c_p$, both torques, both powers, $E_\text{gen}$, $s_\text{air}$, $I$ and
the tip speed $\omega R$. The derived columns are computed at that moment with the same `cp`, `tauAero` and `tauGen` the
integrator uses. Row $n$ is the state at $t_n = n\cdot 2h = n\cdot 20$ ms. After storing step 12 000 the loop stops
([L712](../../public/simulations/wind-turbine.html#L712)): 12 000 RK4 steps, 6 001 rows.

After the loop: arrays marked changed ([L722](../../public/simulations/wind-turbine.html#L722)); chart ranges from the run's
extremes ([L724–L727](../../public/simulations/wind-turbine.html#L724-L727)); the final kinetic energy
([L728](../../public/simulations/wind-turbine.html#L728)); settings, gains, energies, mean power and the balance
([L729–L734](../../public/simulations/wind-turbine.html#L729-L734)); the `solved` snapshot, readouts, `playT = 0` and play
([L736–L739](../../public/simulations/wind-turbine.html#L736-L739)).

The arrays come from `ds.alloc`, which reuses an array when its length is unchanged
([dataset.js:67](../../public/scripts/dataset.js#L67)), so a re-solve overwrites them in place. Memory, measured from the
live store: 15 arrays × 6 001 × 8 B = 720 120 B for the run plus 2 × 271 × 8 B = 4 336 B for the $c_p$ curve, 724 456 B in
all. One solve took 10–46 ms in headless Chromium (`solve_ms`, [L696](../../public/simulations/wind-turbine.html#L696),
[L734](../../public/simulations/wind-turbine.html#L734)).

### When the run is solved again

At load, `optimum()` then `solve()` ([L1162–L1163](../../public/simulations/wind-turbine.html#L1162-L1163)); afterwards only
when **Solve** is pressed ([L969](../../public/simulations/wind-turbine.html#L969)). `optimum()` never runs again. Sliders
([L638–L639](../../public/simulations/wind-turbine.html#L638-L639)) and the two button groups
([L978](../../public/simulations/wind-turbine.html#L978)) only call `markStale()`
([L742–L746](../../public/simulations/wind-turbine.html#L742-L746)), which compares controller, wind, $v_0$, $\Delta v$ and,
when holding speed, the target with `solved`, sets `stale` and rewrites the status line
([L748–L755](../../public/simulations/wind-turbine.html#L748-L755)). The old run keeps playing.

### 3 Play: the frame loop, in order

`Sim.clock` ([sim.js:176–197](../../public/scripts/sim.js#L176-L197)) calls the tick on every `requestAnimationFrame`, with
$\Delta t \le 0.05$ s, and $\Delta t = 0$ while paused. Each tick:

1. returns if nothing is solved; smooths the frame rate; advances `playT += speed · Δt`; at 120 s clamps and pauses; stores
   `fps` and `playing`; marks "3 play" ([L959–L967](../../public/simulations/wind-turbine.html#L959-L967));
2. `frame()` ([L948–L958](../../public/simulations/wind-turbine.html#L948-L958)) picks row
   $n = \operatorname{round}(t_\text{play}/20\,\text{ms})$, clamped to 0 … 6 000, writes `i_now`, `t_play` and the six
   `*_now` copies of row $n$, moves the seek slider and the caption time, then calls `draw()` and `drawCp()`;
3. `draw()` ([L891–L905](../../public/simulations/wind-turbine.html#L891-L905)) gets the layout from `geom()`, stores the hub
   position, the blade length in pixels and the canvas size, clears, and draws `drawScene` and three `drawStrip` calls
   (wind, rotor speed, power), then the time cursor and labels;
4. `drawCp()` ([L911–L934](../../public/simulations/wind-turbine.html#L911-L934)) redraws the second canvas: grid, Betz and
   $\lambda_\text{opt}$ lines, the stored $c_p$ curve, the trail and dot of the operating point, and rewrites `#cap-op`.

No step of this chain integrates; the only arithmetic turns metres, seconds, radians and watts into pixels. Because the clock
ticks every animation frame, the figure is redrawn at the display rate even while paused; one `frame()` took about 1.4 ms
(measured over 200 seek events at a 1 440 px wide window).

### Precomputation and caching

- The $c_p$ curve (`lamL`, `cpL`, 271 points from $\lambda$ = 0.5 to 14.0) is computed once in `optimum()`
  ([L658–L660](../../public/simulations/wind-turbine.html#L658-L660)).
- The 16 frequencies and amplitudes of the turbulent wind and their norm are computed once at load
  ([L665–L666](../../public/simulations/wind-turbine.html#L665-L666)).
- `fullReplay()` reruns the whole 120 s once for the data panel's Check of $E_\text{aero}$, $E_\text{wind}$ and
  $E_\text{gen}(T)$ and caches the result under the run's settings ([L1014–L1018](../../public/simulations/wind-turbine.html#L1014-L1018)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `cp(lam)` | [644–650](../../public/simulations/wind-turbine.html#L644-L650) | Heier's power coefficient, clipped at 0. |
| `tauAero(w, v)` | [651–653](../../public/simulations/wind-turbine.html#L651-L653) | Aerodynamic torque $\tfrac12\rho Av^3c_p/\omega$. |
| `optimum()` | [654–662](../../public/simulations/wind-turbine.html#L654-L662) | Scans $\lambda$ for the peak; stores $\lambda_\text{opt}$, $c_{p,\max}$, 16/27, $K_\text{opt}$, the curve, and $\rho$, $R$, $J$. |
| (wind tables) | [665–666](../../public/simulations/wind-turbine.html#L665-L666) | `TF`, `TA`, `TNORM` of the turbulent wind. |
| `wind(t, w)` | [667–679](../../public/simulations/wind-turbine.html#L667-L679) | The four wind profiles. |
| `tauGen(w, I, c)` | [682–685](../../public/simulations/wind-turbine.html#L682-L685) | Generator torque of the chosen controller, clipped to 0 … $\tau_\max$. |
| `rates(t, w, I, c)` | [686–691](../../public/simulations/wind-turbine.html#L686-L691) | The seven slopes, with anti-windup. |
| `solve()` | [694–740](../../public/simulations/wind-turbine.html#L694-L740) | Solve and store the two minutes (see above); also stores `h`, `steps` ([695](../../public/simulations/wind-turbine.html#L695)), `rpm_min`, `rpm_max`, `captured_pct` ([731–732](../../public/simulations/wind-turbine.html#L731-L732)). |
| `markStale()` | [742–746](../../public/simulations/wind-turbine.html#L742-L746) | Sets `stale` when a control differs from the last solve. |
| `status()` | [748–755](../../public/simulations/wind-turbine.html#L748-L755) | Status line, from the stored `steps` and `solve_ms`, and "1 solve / 2 store" marks; names from `NAMES` ([L746](../../public/simulations/wind-turbine.html#L746)). |
| `readouts()` | [756–764](../../public/simulations/wind-turbine.html#L756-L764) | Mean power, energy in kWh, rotor-speed range (`rpm_min`–`rpm_max`), captured share (`captured_pct`), balance, solve time, all read from the store; computes nothing. |
| `geom()` | [768–783](../../public/simulations/wind-turbine.html#L768-L783) | Layout: scene height, rotor radius and hub, six air lines, three strips, ranges, maps `sx`, `sy`. |
| `label(c, sym, value, …)` | [784–794](../../public/simulations/wind-turbine.html#L784-L794) | A symbol via `Sim.tex`, then its value in IBM Plex Mono. |
| `bladePath(c, g, a)` | [795–802](../../public/simulations/wind-turbine.html#L795-L802) | Outline of one blade at angle `a`, horizontal shortened by `K`. |
| `drawScene(c, g, i)` | [803–853](../../public/simulations/wind-turbine.html#L803-L853) | Air streaks, ground, tower, nacelle, swept disc, three blades, spinner, wind label and arrow, value table. |
| `drawStrip(c, g, i, name, …)` | [854–890](../../public/simulations/wind-turbine.html#L854-L890) | One strip chart: ticks, target line, $P_\text{aero}$ under $P_\text{gen}$, faint future, dark past, dot, title and value. |
| `draw()` | [891–905](../../public/simulations/wind-turbine.html#L891-L905) | One frame of the main canvas. |
| `cpGeom()` | [907–910](../../public/simulations/wind-turbine.html#L907-L910) | Layout of the $c_p$ chart: $\lambda$ 0–14, $c_p$ 0–0.65. |
| `drawCp()` | [911–934](../../public/simulations/wind-turbine.html#L911-L934) | The $c_p$ chart with the operating point and a 3 s trail. |
| `Sim.live()` | [937–946](../../public/simulations/wind-turbine.html#L937-L946) | Formatted store values for the walkthrough. |
| `frame()` | [948–958](../../public/simulations/wind-turbine.html#L948-L958) | Picks the stored row, copies it to the `*_now` scalars, draws both canvases. |
| clock tick (anonymous) | [959–967](../../public/simulations/wind-turbine.html#L959-L967) | Advances `playT`, stops at 120 s, calls `frame()`. |
| `segmented(id, set)` | [971–980](../../public/simulations/wind-turbine.html#L971-L980) | Button group: sets `aria-pressed`, calls `set`, marks stale. |
| `controls()` | [982–986](../../public/simulations/wind-turbine.html#L982-L986) | Greys the target slider unless holding speed, greys $\Delta v$ for steady wind, relabels it (`DVL`, [L981](../../public/simulations/wind-turbine.html#L981)). |
| `stripPos(name, n)` | [993–996](../../public/simulations/wind-turbine.html#L993-L996) | Screen point of row $n$ on the strip that shows `name` (`STRIP_OF`, [L992](../../public/simulations/wind-turbine.html#L992)). |
| `rk4Replay(n)` | [997–1012](../../public/simulations/wind-turbine.html#L997-L1012) | The same RK4 rerun from $t = 0$ to row $n$; the Check of `om`, `Ictl`, `th`, `sw`, `Eg`. |
| `fullReplay()` | [1014–1018](../../public/simulations/wind-turbine.html#L1014-L1018) | Cached `rk4Replay(6000)`. |
| `at`, `maxOf`, `minOf`, `neutralInk`, `isRose`, `readBack` | [1020–1027](../../public/simulations/wind-turbine.html#L1020-L1027) | Small helpers for Check and read-back. |
| `bladePixel()` | [1028–1033](../../public/simulations/wind-turbine.html#L1028-L1033) | Reads back a pixel 60 % along the burgundy blade. |
| `stripDot(name, label)`, `stripCurve(name, label)` | [1034–1046](../../public/simulations/wind-turbine.html#L1034-L1046) | Read-back of the dot and of a curve sample on a strip. |
| `airPixel()` | [1047–1054](../../public/simulations/wind-turbine.html#L1047-L1054) | Read-back of a dash on the second air line. |
| `Sim.data` (object) | [1055–1160](../../public/simulations/wind-turbine.html#L1055-L1160) | The data-panel contract. |
| start-up | [1162–1166](../../public/simulations/wind-turbine.html#L1162-L1166) | `optimum()`, `solve()`, resize observers, redraw when fonts are ready. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Solve | `solve` | button | `solve()` ([L969](../../public/simulations/wind-turbine.html#L969)). |
| Pause / Play | `play` | button | Toggles the clock via `Sim.playButton` ([L968](../../public/simulations/wind-turbine.html#L968)). |
| From t = 0 | `restart` | button | `playT = 0` and play ([L970](../../public/simulations/wind-turbine.html#L970)). |
| Stored run | `seek` | 0–6000, step 1, default 0 ([L95](../../public/simulations/wind-turbine.html#L95)) | `playT = n · 20 ms`, draw ([L641](../../public/simulations/wind-turbine.html#L641)); follows playback ([L954](../../public/simulations/wind-turbine.html#L954)). |
| Playback speed | `speed` | 0.5–8, step 0.5, default 1 ([L99](../../public/simulations/wind-turbine.html#L99)) | Multiplies $\Delta t$ ([L962](../../public/simulations/wind-turbine.html#L962)). |
| Controller | `ctrl` (buttons `data-v="pi"` / `"opt"`) | Hold speed (default, [L106](../../public/simulations/wind-turbine.html#L106), [L563](../../public/simulations/wind-turbine.html#L563)) / Follow the wind | `ctrl` ([L987](../../public/simulations/wind-turbine.html#L987)), used by `tauGen` and the start speed; marks stale. |
| Target rotor speed | `rpm` | 8–21 rpm, step 0.5, default 15 ([L111](../../public/simulations/wind-turbine.html#L111)) | $\omega_\text{ref} = \text{rpm}\cdot2\pi/60$ at the next solve ([L697](../../public/simulations/wind-turbine.html#L697)); greyed and not marking stale when following the wind ([L743](../../public/simulations/wind-turbine.html#L743), [L983](../../public/simulations/wind-turbine.html#L983)). |
| Wind | `prof` (buttons `steady`, `gust`, `step`, `turb`) | Turbulent (default, [L121](../../public/simulations/wind-turbine.html#L121), [L563](../../public/simulations/wind-turbine.html#L563)) | `prof` ([L988](../../public/simulations/wind-turbine.html#L988)), read by `wind()`; marks stale. |
| Mean wind speed $v_0$ | `v0` | 4–11 m/s, step 0.1, default 8 ([L125](../../public/simulations/wind-turbine.html#L125)) | `c.v0`; marks stale. |
| Turbulence σ / Gust size / Step size | `dv` | 0–4 m/s, step 0.1, default 1.5 ([L129](../../public/simulations/wind-turbine.html#L129)) | `c.dv`; label set by `controls()`; unused for steady wind; marks stale. |
| Read values | added by datalog.js | switch, off | Appended to the first figure caption ([datalog.js:895–897](../../public/scripts/datalog.js#L895-L897)); see [datalog.md](../scripts/datalog.md). |

## What the page writes into the data store

The store is made at [L567](../../public/simulations/wind-turbine.html#L567):
`Sim.dataset({ title: 'Wind turbine control', attrs: { figure: 10, page, equation, cp_model } })`. It has two dimensions,
`n` = 6 001 rows ([L592](../../public/simulations/wind-turbine.html#L592)) and `L` = 271 points of the $c_p$ curve
([L621](../../public/simulations/wind-turbine.html#L621)), and 66 variables: 49 scalars and 17 `Float64Array`s, declared at
[L568–L635](../../public/simulations/wind-turbine.html#L568-L635) (counted in the live store). The store is described in
[dataset.md](../scripts/dataset.md). By the panel groups of [L1058–L1067](../../public/simulations/wind-turbine.html#L1058-L1067):

| Group | Variables | Written at |
|---|---|---|
| Turbine | `rho`, `R`, `J`; `lam_opt`, `cp_max`, `cp_betz`, `K_opt` | `optimum()`, [L661](../../public/simulations/wind-turbine.html#L661); [L657](../../public/simulations/wind-turbine.html#L657) |
| Settings | `ctrl`, `profile`, `v0`, `dv`, `w_ref`; `rpm_ref` | [L729](../../public/simulations/wind-turbine.html#L729); [L726](../../public/simulations/wind-turbine.html#L726) |
| Controller | `dtau_dw`, `Kp`, `Ki`, `tau0` | [L730](../../public/simulations/wind-turbine.html#L730) |
| Stored run (dim `n`) | `ts` (coordinate), `vw`, `om`, `rpm`, `th`, `lam`, `cpv`; `ta`, `tg`, `Pg`, `Pa`, `Eg`, `sw`, `Ictl`, `vtip` | [L707](../../public/simulations/wind-turbine.html#L707); [L709](../../public/simulations/wind-turbine.html#L709) |
| Energy | `h`, `steps` | `solve()`, [L695](../../public/simulations/wind-turbine.html#L695), before the loop: the RK4 step $H$ = 0.01 s and $T_\text{end}/H$ = 12 000 steps |
| | `rpm_min`, `rpm_max` | `solve()`, [L731](../../public/simulations/wind-turbine.html#L731): the smallest and largest stored `rpm` (`minOf`, `maxOf`, [L1020–L1021](../../public/simulations/wind-turbine.html#L1020-L1021)) |
| | `captured_pct` | `solve()`, [L732](../../public/simulations/wind-turbine.html#L732): $100\,E_\text{aero}/E_\text{wind}$ |
| | `Ea`, `Ew`, `Eg_end`, `P_mean`; `balance`; `solve_ms`, `stale` | [L733](../../public/simulations/wind-turbine.html#L733); [L734](../../public/simulations/wind-turbine.html#L734); [L734](../../public/simulations/wind-turbine.html#L734), `stale` also [L744](../../public/simulations/wind-turbine.html#L744) |
| Playback | `i_now`, `t_play`, `v_now`, `rpm_now`, `P_now`, `lam_now`, `cp_now`, `th_now` | `frame()`, [L951–L952](../../public/simulations/wind-turbine.html#L951-L952) |
| Power curve (dim `L`) | `lamL` (coordinate), `cpL` | `optimum()`, [L659](../../public/simulations/wind-turbine.html#L659) |
| Drawing | `v_hi`, `rpm_lo`, `rpm_hi`; `P_hi`, `px_per_m_air` | [L726](../../public/simulations/wind-turbine.html#L726); [L727](../../public/simulations/wind-turbine.html#L727) |
| | `hub_x`, `hub_y`, `r_px`, `box_w`, `box_h` | `draw()`, [L893](../../public/simulations/wind-turbine.html#L893) |
| | `fps`, `playing` | clock tick, [L964](../../public/simulations/wind-turbine.html#L964) |

$E_\text{aero}$ and $E_\text{wind}$ are kept only as run totals; $E_\text{gen}$ is stored at every row (`Eg`) and as a total.
With the defaults (hold speed, turbulent wind) the store holds: $E_\text{aero}$ = 88.97 MJ, $E_\text{wind}$ = 200.90 MJ,
$E_\text{gen}(T)$ = 89.04 MJ (24.73 kWh), mean power 742 kW, $K_p = 3.592\times10^6$ N m s,
$\partial\tau_\text{aero}/\partial\omega = -2.480\times10^5$ N m s, $K_i = 1.44\times10^6$ N m, $\tau_0 = 3.343\times10^5$ N m.

**One round** (`Sim.data.round`, [L1156–L1156](../../public/simulations/wind-turbine.html#L1156-L1156)) is one turn of the
rotor at the present speed, $60/n_\text{rot}$ seconds of the stored run (4.0 s at 15 rpm), timed by `t_play`. Columns:
`v_now`, `rpm_now`, `P_now`, `lam_now`, `cp_now`, `th_now`; the default point is the rotor. Recording is refused when the run
ends before one more turn. The panel samples every frame of the round, at most 600 samples
([datalog.js:1052](../../public/scripts/datalog.js#L1052)).

**`Sim.live()`** ([L937–L946](../../public/simulations/wind-turbine.html#L937-L946)) returns formatted strings read from the
store for the walkthrough keys `lam`, `cp`, `lopt`, `cpmax`, `Kopt`, `v`, `w`, `ta`, `tg`, `Pg`, `wref`, `Kp`, `Ki`, `dtd`,
`n`, `t`, `th`, `Eg`, `bal`; row-valued keys use `i_now`. The walkthrough polls it every 200 ms
([sim.js:403](../../public/scripts/sim.js#L403)).

`rpm_ref` is the raw rpm input captured by `solve()`, rather than a round-trip conversion of `w_ref`. Check of `w_ref` converts this stored input; changing the live target cannot change the check of an already solved run. All 27 target values from 8 to 21 turns per minute were checked and were bit-identical.

**Check and read-back.** `Sim.data.check` ([L1087–L1135](../../public/simulations/wind-turbine.html#L1087-L1135)) recomputes
each value from stored inputs; the integrated quantities (`om`, `Ictl`, `th`, `sw`, `Eg`) are checked by rerunning the same
RK4 to row $n$, the totals by `fullReplay()`, and `lam_opt` by repeating the scan. `Sim.data.drawn`
([L1136–L1154](../../public/simulations/wind-turbine.html#L1136-L1154)) reads back the burgundy blade, the dots and curves
of the strips ($P_\text{aero}$ with a rose-colour test), a dash of the air, the operating point and the $c_p$ curve.
It also reads the text on screen: `rpm_min`, `rpm_max` and `captured_pct` against the readouts `r-rpm` and `r-eff`
([L1138–L1140](../../public/simulations/wind-turbine.html#L1138-L1140)), `steps` against the status line, and `h` from the sampling interval the status line states, "one every 20 ms",
divided by `EVERY` = 2 ([L1136–L1137](../../public/simulations/wind-turbine.html#L1136-L1137)). While a control has changed and the run is not solved again, the status line asks for a
new solve and shows neither number. `drawn.h` and `drawn.steps` then return `ok: null` by design, and the panel shows the
neutral "Not in the picture at the moment, so there is nothing to read back." rather than a failure
([datalog.js:836](../../public/scripts/datalog.js#L836)). `probe`
([L1068–L1075](../../public/simulations/wind-turbine.html#L1068-L1075)) pins the rotor when the click falls inside the drawn
disc ellipse, otherwise the nearest stored sample within 14 px on the three strips (every second row is tried). `locate`
maps quantities that have no chart of their own to a strip that does (`STRIP_OF`: $\omega$, $\lambda$, $c_p$, $\theta$ to the
rotor-speed strip, the torques to the power strip, [L992](../../public/simulations/wind-turbine.html#L992)).


**The ledger** (24 October 2026). The data panel shows this store as a bookkeeper; its layout is
[scripts/ledger/wind-turbine.js](../../public/scripts/ledger/wind-turbine.js), loaded on the line that loads the panel
([L1169](../../public/simulations/wind-turbine.html#L1169)). Headline: $v$, $n_\text{rot}$, $\lambda$, $c_p$, $P_\text{gen}$, $E_\text{gen}$. Sections: what you set,
the turbine, what follows from it, the state now, the stored run, over the whole run, the power curve, the solver and the
drawing; the last three start folded. One book, the energy statement (7) of the note at every stored sample:
$K(0) + E_\text{aero}(t) - E_\text{gen}(t) = K(t)$ with $K = \tfrac12 J\omega^2$; residual `ebal_now`, measured about
$1.5\times10^{-13}$ of the flows. For it the page stores, each on a line that already existed: `Eas`, the wind's work so far at
every stored sample, the solver's own integral $y_1$ (declared [L606](../../public/simulations/wind-turbine.html#L606), allocated [L702](../../public/simulations/wind-turbine.html#L702), written
[L708](../../public/simulations/wind-turbine.html#L708)); `K0` ([L735](../../public/simulations/wind-turbine.html#L735)); and `Ea_now`, `Eg_now`, `K_now`, `ebal_now` with the other playback values
([L953](../../public/simulations/wind-turbine.html#L953), declared [L620](../../public/simulations/wind-turbine.html#L620)). There is no force book: the step and gust winds make $\dot\omega$ jump, and a
difference across a jump misses by half the jump. The ledger file adds checks of the 8 `*_now` numbers against their rows, and
of `K_now`, `K0` and `ebal_now`; all answer "identical".

## Page structure

**Head** ([L3–L29](../../public/simulations/wind-turbine.html#L3-L29)): title "Wind Turbine Control · Numa Koudsie",
description, the security policy and referrer rule ([build-and-deploy.md](../build-and-deploy.md#security)), stylesheets `../styles/sim.css`, `../styles/data.css`, `../styles/fold.css`
([L11–L12](../../public/simulations/wind-turbine.html#L11-L12)), inline SVG favicon, and an inline style for the solve box,
the seek slider, the segmented buttons `.seg` and the greyed control `.ctl.is-off`
([L15–L28](../../public/simulations/wind-turbine.html#L15-L28)). Styles are described in [styles.md](../styles.md).

**Body**, in order:
- `header.sim-top`: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`,
  87 × 48) and "← All simulations" ([L32](../../public/simulations/wind-turbine.html#L32)), then the Fig. 1–11 links, Fig. 10 marked `aria-current`
  ([L31–L47](../../public/simulations/wind-turbine.html#L31-L47));
- `.sim__head`: "Fig. 10 · control systems · wind energy", `h1`, lede ([L51–L55](../../public/simulations/wind-turbine.html#L51-L55));
- `.sim__grid`: the main figure `#stage` with `canvas#wt` and a caption with the equation and `#cap-t`
  ([L59–L67](../../public/simulations/wind-turbine.html#L59-L67)); the operating-point figure `#stage-cp` with `canvas#cp`
  and `#cap-op` ([L68–L76](../../public/simulations/wind-turbine.html#L68-L76)); `aside.panel` with the solve box, the
  controller and wind groups, six readouts and a legend ([L79–L148](../../public/simulations/wind-turbine.html#L79-L148)).
  **Read values** is added to the first caption by datalog.js;
- `article.paper#paper` ([L151–L538](../../public/simulations/wind-turbine.html#L151-L538)): abstract; ten sections — 01 From
  wind to electricity, 02 The power in the wind, 03 The Betz limit ★, 04 Tip-speed ratio, 05 The rotor's equation of motion,
  06 Two controllers ★ (6.1 Follow the wind: the optimal-torque law, 6.2 Hold speed: a PI controller), 07 Same wind, two
  answers, 08 Solve first, then play, 09 On screen, 10 What the model leaves out (10.1 Further reading). Ten numbered
  equations, `\tag{1}`–`\tag{10}`. Four figures with six inline SVGs: Figure 1 the stream tube
  ([L180–L209](../../public/simulations/wind-turbine.html#L180-L209)), Figure 2 the $c_p$ curve
  ([L240–L291](../../public/simulations/wind-turbine.html#L240-L291)), whose axis title "power coefficient c<sub>p</sub>" stands at y = 27 ([L277](../../public/simulations/wind-turbine.html#L277)); measured,
  its box spans y = 14.4 to 36.1, so the subscript p clears the dashed Betz line at y = 38.8 ([L279](../../public/simulations/wind-turbine.html#L279)), Figure 3 the control loop
  ([L302–L333](../../public/simulations/wind-turbine.html#L302-L333)), Figure 4 wind, rotor speed and power for both
  controllers (three SVGs, [L353–L482](../../public/simulations/wind-turbine.html#L353-L482)). A Betz-limit box
  ([L228–L231](../../public/simulations/wind-turbine.html#L228-L231)), a table of all eight controller–wind combinations
  ([L484–L496](../../public/simulations/wind-turbine.html#L484-L496)) and exercise 7.1;
- `section#walk` with `data-walk="turbine"` ([L540](../../public/simulations/wind-turbine.html#L540)), filled from
  `walk/turbine.js` by `sim.js` ([sim.js:481–490](../../public/scripts/sim.js#L481-L490)); see [walk.md](../scripts/walk.md);
- footer; scripts in load order: `fold.js`, `sim.js`, `dataset.js`, the inline page script, `datalog.js`
  ([L548–L1168](../../public/simulations/wind-turbine.html#L548-L1168)). See [sim.md](../scripts/sim.md) and
  [fold.md](../scripts/fold.md).

The walkthrough quotes: step 1 [L644–L650](../../public/simulations/wind-turbine.html#L644-L650); step 2
[L651–L653](../../public/simulations/wind-turbine.html#L651-L653); step 3
[L682–L685](../../public/simulations/wind-turbine.html#L682-L685); step 4
[L699–L700](../../public/simulations/wind-turbine.html#L699-L700); step 5
[L690](../../public/simulations/wind-turbine.html#L690) and [L714–L718](../../public/simulations/wind-turbine.html#L714-L718);
step 6 [L709–L709](../../public/simulations/wind-turbine.html#L709-L709) (the second line only in part, see the notes);
step 7 [L949](../../public/simulations/wind-turbine.html#L949) and [L827](../../public/simulations/wind-turbine.html#L827).
The table in section 7 ([L487–L494](../../public/simulations/wind-turbine.html#L487-L494)) was reproduced exactly, all eight
rows, by solving each combination in the page (measured).

## Where the drawing and the store differ

The page states this in `Sim.data.about` ([L1158](../../public/simulations/wind-turbine.html#L1158)). In detail:

- **Nearest row, no interpolation.** The picture shows row $\operatorname{round}(t_\text{play}/20\,\text{ms})$
  ([L949](../../public/simulations/wind-turbine.html#L949)); the caption shows `ts[i]` to one decimal
  ([L955](../../public/simulations/wind-turbine.html#L955)).
- **Rotor seen at an angle.** The swept disc and each blade have their horizontal extent multiplied by `K = 0.5`
  ([L767](../../public/simulations/wind-turbine.html#L767), [L797](../../public/simulations/wind-turbine.html#L797),
  [L824](../../public/simulations/wind-turbine.html#L824)). Blade 1 (burgundy) is at the stored $\theta$, the others at
  $\theta + 2\pi/3$ and $\theta + 4\pi/3$ ([L826–L830](../../public/simulations/wind-turbine.html#L826-L830)). The blade
  outline, tower and nacelle are a sketch in units of the drawn radius, not to scale.
- **Air streaks.** Six dashed lines with fixed 16 px dashes and 22 px gaps; their offset is $-s_\text{air}\times5$ px/m, each
  line 15 px further into the pattern than the one above ([L767](../../public/simulations/wind-turbine.html#L767),
  [L775](../../public/simulations/wind-turbine.html#L775), [L806–L808](../../public/simulations/wind-turbine.html#L806-L808)).
  They pass through the rotor unchanged; the slowing of the air is not drawn.
- **Wind arrow** at the top left: $6 + 3.2\,v$ px long ([L836](../../public/simulations/wind-turbine.html#L836)).
- **Strips thinned and clamped.** Each strip draws every `stride`-th row, `stride = max(1, floor(NS / (2 × strip width)))`
  ([L855](../../public/simulations/wind-turbine.html#L855)): every 4th row at a 770 px canvas, every 10th at 356 px. Values are
  clamped to the strip's range ([L781](../../public/simulations/wind-turbine.html#L781)); the ranges come from the run's own
  extremes, so with the stored run nothing is clamped.
- **$c_p$ chart.** Axes 0–14 and 0–0.65 ([L909](../../public/simulations/wind-turbine.html#L909)); the trail is the last 150
  rows (3 s), every third row ([L926–L927](../../public/simulations/wind-turbine.html#L926-L927)).
- **Rounding.** The value table rounds ($n_\text{rot}$ to 2 decimals, torques to whole kN m, power to whole kW,
  [L840–L852](../../public/simulations/wind-turbine.html#L840-L852)); on narrow screens it shows four rows instead of seven.

## How to change it safely

- **Run length, step and stride.** `TEND`, `H`, `EVERY` ([L556](../../public/simulations/wind-turbine.html#L556)) give `NS`.
  Keep `TEND / H` and `TEND / H / EVERY` whole numbers. Change with them: seek `max="6000"`
  ([L95](../../public/simulations/wind-turbine.html#L95)); formula texts "n · 2h" and "round(t_play / 2h)"
  ([L593](../../public/simulations/wind-turbine.html#L593), [L613](../../public/simulations/wind-turbine.html#L613)); group
  note "every 20 ms of the 120 s" ([L1061](../../public/simulations/wind-turbine.html#L1061)); check text "at most 6000"
  ([L1126](../../public/simulations/wind-turbine.html#L1126)); time labels every 20 s
  ([L903](../../public/simulations/wind-turbine.html#L903)); the 150-row trail
  ([L926](../../public/simulations/wind-turbine.html#L926)); the walkthrough step 6 note and step 7 formula
  ([turbine.js:96–97](../../public/scripts/walk/turbine.js#L96-L97), [turbine.js:110](../../public/scripts/walk/turbine.js#L110));
  the note's sections 8 and 9 ([L509–L510](../../public/simulations/wind-turbine.html#L509-L510),
  [L515](../../public/simulations/wind-turbine.html#L515)) and `about`.
- **The integrator exists twice.** The start state and the step in `solve()`
  ([L703](../../public/simulations/wind-turbine.html#L703), [L714–L721](../../public/simulations/wind-turbine.html#L714-L721))
  and in `rk4Replay()` ([L1000](../../public/simulations/wind-turbine.html#L1000),
  [L1002–L1009](../../public/simulations/wind-turbine.html#L1002-L1009)) must stay identical, or the Checks of the integrated
  columns will disagree.
- **Order at start-up.** `optimum()` must run before `solve()` ([L1162–L1163](../../public/simulations/wind-turbine.html#L1162-L1163)):
  `solve()` reads `lam_opt` for the start speed and `tauGen` reads `K_opt` from the store.
- **Defaults in two places.** `ctrl = 'pi'` and `prof = 'turb'` ([L563](../../public/simulations/wind-turbine.html#L563)) must
  match the buttons marked `aria-pressed="true"` ([L106](../../public/simulations/wind-turbine.html#L106),
  [L121](../../public/simulations/wind-turbine.html#L121)).
- **Physics constants are quoted elsewhere.** $c_1$…$c_6$ ([L557](../../public/simulations/wind-turbine.html#L557)) also
  appear in the `cp_model` attribute ([L567](../../public/simulations/wind-turbine.html#L567)), walkthrough step 1
  ([turbine.js:13](../../public/scripts/walk/turbine.js#L13)) and the note ([L238–L239](../../public/simulations/wind-turbine.html#L238-L239)).
  `WN` and `ZC` appear in the note ([L346](../../public/simulations/wind-turbine.html#L346)) and walkthrough step 4
  ([turbine.js:63–64](../../public/scripts/walk/turbine.js#L63-L64)). `AIRPX`, `K` and `DASH` appear in `about`, in the
  `airPixel` note ([L1053](../../public/simulations/wind-turbine.html#L1053)) and in walkthrough step 7
  ([turbine.js:111](../../public/scripts/walk/turbine.js#L111)).
- **The turbulent wind is fixed.** `PHASES` ([L558](../../public/simulations/wind-turbine.html#L558)) make every solve use the
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

1. Fixed on 2026-10-15: the note gives K = 0.5, 5 px/m airflow and the fixed 16 px / 22 px dash pattern (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
2. Fixed on 2026-10-15: the quoted storage line includes Ic[n] and vt[n] (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
3. Fixed on 2026-10-15: w_ref is checked against the saved rpm input, including Follow the wind; all target steps recompute identically after live controls change (commit [9d3175f](https://github.com/Numa1997/SiteTest/commit/9d3175f2cf50d0ad3f8792f1ee173e8ce56bab53)).
4. Fixed on 2026-10-15: the Figure 2 labels render p and opt as SVG subscripts (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
5. Fixed on 2026-10-15: solve stores h, steps, rpm_min, rpm_max and captured_pct; displays only read them (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
6. Fixed on 2026-10-15: the unread frame counter was removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
7. **Redraw while paused.** The clock ticks every animation frame with $\Delta t = 0$ while paused
   ([sim.js:178–185](../../public/scripts/sim.js#L178-L185)) and the tick always calls `frame()`
   ([L966](../../public/simulations/wind-turbine.html#L966)), so both canvases are redrawn about 60 times a second while
   paused (about 1.4 ms per frame measured), and `#cap-op` and `#cap-t` are rewritten each frame
   ([L932](../../public/simulations/wind-turbine.html#L932), [L955](../../public/simulations/wind-turbine.html#L955)).
8. **AGENTS.md** said the load order dataset.js → page → datalog.js holds for "all eight figures"; this page (Fig. 10)
   follows it too. Corrected to "all ten figures" on 14 October 2026.
9. Fixed on 2026-10-15: in note Figure 2 the axis title "power coefficient c<sub>p</sub>" moved from y = 31 to y = 27, so its
   subscript p clears the Betz line at y = 38.8; the title box now spans y = 14.4 to 36.1 ([L277](../../public/simulations/wind-turbine.html#L277)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
10. Fixed on 2026-10-15: while the run is stale, the Checks of `h` and `steps` show "not in the picture" instead of a burgundy ✕:
    `drawn.h` and `drawn.steps` return `ok: null` there by design ([L1136–L1137](../../public/simulations/wind-turbine.html#L1136-L1137)), and the panel now honours it
    ([datalog.js:836](../../public/scripts/datalog.js#L836)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).

Batch D store additions in `solve()`: `h` (s), `steps` (count), `rpm_min` and `rpm_max` (turns per minute), and `captured_pct` (%). They appear in the Energy group, have recomputation checks and DOM readbacks. The step readback infers h from the visible sampling interval and EVERY = 2. The speed range is the sampled run range, independent of the wider chart bounds. `readouts()` no longer computes these results.


## Teaching revision · 15 October 2026

The false global monotonicity argument is replaced by a local restoring torque slope of −3 K ω at the maximum-power operating point. The note explains proportional braking and integral memory before selecting gains, and uses relative airflow rather than a solid-wall blade analogy. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16: "the linearised equation below" pointed at (10), which is above ([L346](../../public/simulations/wind-turbine.html#L346)); and the conclusion that no global argument exists is replaced by the sign of the net torque on each side of $\lambda_\text{opt}$ ([L340](../../public/simulations/wind-turbine.html#L340)): $c_p/\lambda^3$ is not monotone, but it stays above its value at $\lambda_\text{opt}$ for smaller $\lambda$ and below it for larger, so in steady wind the rotor returns from any start at which it is turning. See the [audit of the revision](../research-theory-audit.md).

Fixed on 2026-10-16 (second repairs): the $c_p$ paragraph has its two pictures back (too slow lets the air through, too fast acts like a wall) with the angle of attack as the mechanism behind both ([L235](../../public/simulations/wind-turbine.html#L235)). See the [audit of the revision](../research-theory-audit.md).

## Teaching revision · 20 October 2026

Judged section by section against `notes/STANDARD.md` (plan and verdicts in `notes/fig10/plan.md`); sections 5 and 10 and the abstract were left as they were. Changes, all inside existing lines, so no line of the page moved and every link above still holds: $\omega$ and $R$ named in section 1 ([L178](../../public/simulations/wind-turbine.html#L178)) and $\rho$ in section 2 ([L214](../../public/simulations/wind-turbine.html#L214)); the Betz derivation now writes the two Bernoulli equations, says why Bernoulli does not hold across the disc, and divides by $v - v_w$ in the open, and the root $a = 1$ is named ([L224–L226](../../public/simulations/wind-turbine.html#L224-L226)); section 4 says why $c_p$ depends on $\omega$ and $v$ only through $\lambda$ (the relative wind meets the blade at $\tan\phi = (R/r)/\lambda$, 7.04° at the tip at $\lambda = 8.1$, [L235](../../public/simulations/wind-turbine.html#L235)); section 6.1 defines $\omega_*$ and gives the step to the slope $-K_\text{opt}\omega_*$ ([L340](../../public/simulations/wind-turbine.html#L340)); section 6.2 defines $\tau_0$, writes the linearised equation before it is differentiated into (10), and replaces "without ringing" by the measured Step-run overshoot of 0.39 rpm and dip of 0.01 rpm ($\zeta_c = 0.8 < 1$; [L345–L346](../../public/simulations/wind-turbine.html#L345-L346)); section 7 glosses $\Delta v$ and separates $c_p$ after the step (0.427, measured) from the whole-run share 0.437 ([L483](../../public/simulations/wind-turbine.html#L483), [L497](../../public/simulations/wind-turbine.html#L497)); section 8 adds the step study above ([L508](../../public/simulations/wind-turbine.html#L508)); section 9 names the rose $P_\text{aero}$ curve ([L516](../../public/simulations/wind-turbine.html#L516)); the four references have links to pages that were opened ([L530–L533](../../public/simulations/wind-turbine.html#L530-L533)). Heier's book itself could not be opened; its link is the publisher's description at the Library of Congress. Walkthrough step 4 still says "without ringing" ([turbine.js:64](../../public/scripts/walk/turbine.js#L64)); it was not edited.

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig10/`), the lead made only these changes, each on its existing line, so no line link moved: equations (3) and (10) broken over two lines so their numbers show at 1440 px ([L225](../../public/simulations/wind-turbine.html#L225)); (10) ([L346](../../public/simulations/wind-turbine.html#L346)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

## Second check round · 20 October 2026

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig10/`), each change on its existing line: Figure 1: the tip speed drawn out of the page ([L198](../../public/simulations/wind-turbine.html#L198)); Figure 3: labels fit, subscripts set ([L307](../../public/simulations/wind-turbine.html#L307)); §2: power is torque times angular speed ([L217](../../public/simulations/wind-turbine.html#L217)); §4: the inflow angle 7° for the undisturbed wind, about 6° for the slowed air; one repeated sentence removed ([L235](../../public/simulations/wind-turbine.html#L235)); §6.1: the code, not the fit, gives no torque at a standstill ([L340](../../public/simulations/wind-turbine.html#L340)); §6.2 and §7: the Step wind is a 2 s ramp; overshoot 0.39 rpm ([L347](../../public/simulations/wind-turbine.html#L347)); equation (8) reflowed so its number shows at 1600 px ([L340](../../public/simulations/wind-turbine.html#L340)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.
