# Fig. 7 · Phasor Sums

| | |
|---|---|
| Page | [public/simulations/phasor-sums.html](../../public/simulations/phasor-sums.html) (1 477 lines, 259 831 bytes) |
| Walkthrough | [public/scripts/walk/phasors.js](../../public/scripts/walk/phasors.js) (key `phasors`, 8 steps) |
| Thumbnail | [public/images/sims/phasor-sums.webp](../../public/images/sims/phasor-sums.webp) (800 × 500 px: the 3-petal rose with its two arms and circles) |
| Catalog entry | [public/scripts/catalog.js#L150](../../public/scripts/catalog.js#L150) (`id: 'phasor-sums'`, `fig: 7`, field `methods`, stage 2) |

Links of the form `[L816]` point into `phasor-sums.html`.

The reader sees a chain of arms on a canvas. Each arm turns at a steady rate about the tip of the one before it,
and the tip of the last arm, the pen, leaves a burgundy trail. One card per arm sets its radius, angular frequency,
phase and "bounce curve" ([L972–985](../../public/simulations/phasor-sums.html#L972-L985)). Ten presets load roses,
beats, a trefoil, a star and Spirograph-like curves ([L668–679](../../public/simulations/phasor-sums.html#L668-L679)).
A *Final shape* view draws the whole closed curve at once and morphs it when a slider moves. An audio file can drive
the radii ("Auto Dance"), and a performance of slider changes can be recorded, replayed and saved as JSON. The page
opens on the 3-petal rose ([L1470](../../public/simulations/phasor-sums.html#L1470)).

## The physics in one picture

Everyday picture: a fairground ride whose cars spin on the ends of a turning arm, Ptolemy's epicycles, a Spirograph,
or the 50 Hz mains voltage drawn as a turning arrow (lecture note section 1,
[L244–250](../../public/simulations/phasor-sums.html#L244-L250)).

Model: each arm is a rigid rotor turning at constant angular velocity; no arm exerts a force on another. Mounting
an arm on a moving tip adds its arrow to that tip's position, so the pen is a sum of complex numbers (note section 3,
[L315–320](../../public/simulations/phasor-sums.html#L315-L320)). Everything on screen is kinematics.

The equations the code evaluates:

$$x(t) = \sum_{k=1}^{N} A'_k \cos(\omega_k t + \varphi_k), \qquad y(t) = \sum_{k=1}^{N} A'_k \sin(\omega_k t + \varphi_k), \qquad z = x + iy$$

with $A'_k = A_k\, m_k$ ([L816–820](../../public/simulations/phasor-sums.html#L816-L820),
[L948](../../public/simulations/phasor-sums.html#L948)). $A_k$ is the stored radius, a scale-free length (only ratios
matter; the picture is scaled to fit). $\omega_k$ is the angular frequency in rad/s, $\varphi_k$ the phase in rad,
$t$ the phasor time in s. $m_k$ is the dance multiplier, exactly 1 while Auto Dance is off
([L942](../../public/simulations/phasor-sums.html#L942)).

Closure and symmetry use integers $w_k = \mathrm{round}(100\,\omega_k)$ over the arms with $A_k > 0$
([L829](../../public/simulations/phasor-sums.html#L829)):

$$G = \gcd_k w_k, \quad g = G/100\ \mathrm{rad/s}, \quad T = 2\pi/g; \qquad M = \gcd_k (w_k - w_1), \quad q = M/\gcd(w_1, M)$$

([L831–834](../../public/simulations/phasor-sums.html#L831-L834)). $T$ in s is the period after which the curve
closes; $q$ is the order of its rotational symmetry. The time average of the squared distance, for distinct
frequencies, is $\langle |z|^2 \rangle = \sum_k A_k^2$ ([L1158](../../public/simulations/phasor-sums.html#L1158)).

The lecture note derives these: Euler's formula (section 2, eqs. 1–5), the model (section 3, eq. 6, velocity eq. 7),
roses and beats (section 4, eqs. 8–11), closure and symmetry (section 5, eqs. 12–13), Parseval (section 6, eqs. 14–15),
morphing as a low-pass filter (section 7.1, eq. 16) and the screen mapping (section 8, eq. 17).

## How the code computes it

**State** ([L703–706](../../public/simulations/phasor-sums.html#L703-L706)). `phasors` holds the stored list, one
object `{ amp, freq, phase, color, curve }` per card. `live` is a per-frame copy with the danced radius. `t` is phasor
time in s. `trail` is the list of past pen positions. `finalPath` holds the exact samples of the closed curve,
`morphPath` the samples as drawn. `fitR` is the radius the Live view is fitted to.

**Method: closed form, no integrator.** The sum is evaluated directly at the current $t$; nothing is integrated, so
no error accumulates from frame to frame (note section 7, [L599](../../public/simulations/phasor-sums.html#L599)).
Each frame costs $N$ cosines and $N$ sines in `sumAt()` ([L812–824](../../public/simulations/phasor-sums.html#L812-L824)),
called twice per frame with the same arguments: once for the new trail point
([L1326](../../public/simulations/phasor-sums.html#L1326)) and once in `draw()`
([L1118](../../public/simulations/phasor-sums.html#L1118)).

Period and symmetry are found exactly because the sliders move in steps of 0.01 rad/s
([L970](../../public/simulations/phasor-sums.html#L970)): $100\,\omega$ is an integer and Euclid's algorithm `gcd()`
([L805–809](../../public/simulations/phasor-sums.html#L805-L809)) works on integers.

**Frame loop**, the `Sim.clock` callback ([L1315–1350](../../public/simulations/phasor-sums.html#L1315-L1350)), in order:

1. `real` = wall time since the last frame, capped at 0.05 s ([L1316](../../public/simulations/phasor-sums.html#L1316)).
   The clock's own `dt` is the same cap but 0 while paused ([sim.js:179–181](../../public/scripts/sim.js#L179-L181)).
2. `analyse(real)`: audio bands, beat detection, burst decay ([L902–935](../../public/simulations/phasor-sums.html#L902-L935)).
3. `perform(real)`: record a snapshot every 50 ms, or replay ([L1183–1213](../../public/simulations/phasor-sums.html#L1183-L1213)).
4. `buildLive()`: copy the list with the dance multipliers ([L938–955](../../public/simulations/phasor-sums.html#L938-L955)).
   This runs even while paused, so with Auto Dance on the arms still breathe when time stands still.
5. Speed: `lastSpeed = speed.value * speedFactor()` ([L1323](../../public/simulations/phasor-sums.html#L1323)).
6. Live view only, and only when `dt > 0`: `t += dt * lastSpeed`, push $z(t)$ onto `trail`, cut the trail to the
   *Trail length* slider ([L1324–1330](../../public/simulations/phasor-sums.html#L1324-L1330)).
7. Final view only: `morphStep()` moves every drawn sample the fraction $\alpha$ toward the exact one
   ([L862–868](../../public/simulations/phasor-sums.html#L862-L868), [L1335](../../public/simulations/phasor-sums.html#L1335)).
   This also runs while paused.
8. `fit(real)`: the fit radius jumps up at once and relaxes down with a time constant of 0.6 s
   ([L1054–1058](../../public/simulations/phasor-sums.html#L1054-L1058)). The target is `reach()`: $\sum |A'_k|$ or the
   farthest trail point, whichever is larger ([L1048–1053](../../public/simulations/phasor-sums.html#L1048-L1053)).
9. Write the frame scalars into the store ([L1337–1341](../../public/simulations/phasor-sums.html#L1337-L1341)), then `draw()`.
10. Every 0.1 s: `readouts()`, and while replaying, `syncList()` and `formula()`
    ([L1343–1348](../../public/simulations/phasor-sums.html#L1343-L1348)). Then `hud()` paints the audio meters.

**Drawing** (`draw()`, [L1081–1152](../../public/simulations/phasor-sums.html#L1081-L1152)). A point $(x, y)$ goes to the
pixel $(c_x + s\,x,\ c_y - s\,y)$ with $(c_x, c_y)$ the canvas centre
([L1076](../../public/simulations/phasor-sums.html#L1076)). In the Live view
$s = 0.44\,\min(w,h)/\max(R_\text{fit}, 0.05)\times\text{zoom}$ ([L1059](../../public/simulations/phasor-sums.html#L1059),
[L1103](../../public/simulations/phasor-sums.html#L1103)). The trail is drawn in 12 chunks with opacity
$0.18 + 0.82\,(c+1)/12$, so 0.25 for the oldest ([L1106–1113](../../public/simulations/phasor-sums.html#L1106-L1113)).
Then each arm: its circle in `T.rose` about the joint it turns on, its arm and a 3 px dot in the card's colour
([L1120–1144](../../public/simulations/phasor-sums.html#L1120-L1144)); the pen is a 5.5 px burgundy dot with a 2 px
outline in the paper colour `T.card` ([L1145–1151](../../public/simulations/phasor-sums.html#L1145-L1151)). In the Final view the
scale uses the largest $|z|$ of the drawn path instead of $R_\text{fit}$
([L1060–1064](../../public/simulations/phasor-sums.html#L1060-L1064)), and the path is drawn as a 6 px pale-rose band
under a 1.8 px burgundy line ([L1095–1100](../../public/simulations/phasor-sums.html#L1095-L1100)).

**Precomputation.** `refinal(snap)` ([L843–860](../../public/simulations/phasor-sums.html#L843-L860)) samples the closed
curve at $n+1$ times $t_i = i\,T_\text{span}/n$. The span comes from `spanNow()`
([L837–841](../../public/simulations/phasor-sums.html#L837-L841)): with *Draw one full period* on and $g > 0$ it is
$\min(2\pi/g,\ 60\cdot 2\pi)$ s, otherwise the *Span* slider times $2\pi$ s. The sample count is
$n = \max(1500, \min(12000, \mathrm{round}(700\,T_\text{span}/2\pi)))$
([L845](../../public/simulations/phasor-sums.html#L845)). `refinal()` runs on every card edit (through `edited()`,
[L1030–1036](../../public/simulations/phasor-sums.html#L1030-L1036)), on the span controls and on entering the Final view
([L1259](../../public/simulations/phasor-sums.html#L1259)). It snaps `morphPath` to the new curve when asked, when
morphing is off, or when the sample count changed, because then there is nothing to blend
([L853–855](../../public/simulations/phasor-sums.html#L853-L855)). Every edit also resets `t = 0` and clears the trail.

**Audio** (lecture note section 8.1). `ensureAudio()` builds a Web Audio analyser with `fftSize = 2048` and smoothing
0.8 ([L875–882](../../public/simulations/phasor-sums.html#L875-L882)). Bands are averages of byte bins divided by 255:
bass 20–150 Hz, mid 150–4000 Hz, high 4–16 kHz, each smoothed by `e += 0.15 (raw − e)` per frame
([L905–914](../../public/simulations/phasor-sums.html#L905-L914)). A beat is a raw bass level more than 35 % above the
previous frame's, above 0.22, at least 280 ms after the last beat; it sets `burst = 1 + d_burst`, which falls back
linearly over 10 frames, and the tempo is 60 000 over the median of the last 8 intervals in ms
([L916–934](../../public/simulations/phasor-sums.html#L916-L934)). In `buildLive()`, arms with $|\omega|$ at or below
the median of all $|\omega_k|$ get
$m = 1 + \mathrm{ease}(\text{bass})\,d_\text{bass}\,(1 - 0.7\,|\omega|/|\omega|_\text{max})$, faster arms
$m = 1 + \text{high}\cdot d_\text{high}$, and both are multiplied by `burst`
([L944–946](../../public/simulations/phasor-sums.html#L944-L946)). The easing curves are written inline in `EASE`
([L682–696](../../public/simulations/phasor-sums.html#L682-L696)). The mid band speeds up time by
$1 + \text{mid}\cdot d_\text{speed}$ ([L956](../../public/simulations/phasor-sums.html#L956)). The stored $A, \omega,
\varphi$ are never changed by the dance.

**Record and replay** ([L1177–1250](../../public/simulations/phasor-sums.html#L1177-L1250)). A snapshot
`{ t, d, p: [{ a, f, h, c }] }` of the whole list is taken every 50 ms against the audio time, or against wall time
without audio ([L1178–1181](../../public/simulations/phasor-sums.html#L1178-L1181)). Replay finds the last snapshot not
later than the current time and moves each value the fraction $\min(1, \Delta t/0.05)$ toward it per frame
([L1194–1206](../../public/simulations/phasor-sums.html#L1194-L1206)); if the number of circles differs it reloads the list
outright. Export writes `phasor-performance.json` as `{ v: 1, timeline }`
([L1231–1232](../../public/simulations/phasor-sums.html#L1231-L1232)); import accepts that object or a bare array
([L1245](../../public/simulations/phasor-sums.html#L1245)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `EASE.*` (6 curves) | [682–696](../../public/simulations/phasor-sums.html#L682-L696) | Easing curves for the bass response: Linear, Bounce, Elastic, Back, Sine, Expo. |
| `$` | [698](../../public/simulations/phasor-sums.html#L698) | `document.getElementById`. |
| `wrap` | [798](../../public/simulations/phasor-sums.html#L798) | Angle into $[0, 2\pi)$; applied to every phase that `load()` takes in. |
| `clamp01` | [799](../../public/simulations/phasor-sums.html#L799) | Clamp to $[0, 1]$. |
| `median` | [800–804](../../public/simulations/phasor-sums.html#L800-L804) | Median of an array (beat intervals, $|\omega_k|$). |
| `gcd` | [805–809](../../public/simulations/phasor-sums.html#L805-L809) | Euclid's algorithm on integers. |
| `sumAt` | [812–824](../../public/simulations/phasor-sums.html#L812-L824) | The phasor sum and each arm's $(\Delta x, \Delta y)$ at one time; an optional angles array receives the live angle at its calculation. |
| `structure` | [827–835](../../public/simulations/phasor-sums.html#L827-L835) | $G$, $g$, $M$, $q$ and the active count from `round(100 ω)`. |
| `spanNow` | [837–841](../../public/simulations/phasor-sums.html#L837-L841) | Time span of the Final shape. |
| `refinal` | [843–860](../../public/simulations/phasor-sums.html#L843-L860) | Samples the exact curve, snaps or keeps the morph path, writes `final_*`, `path_*`, `n_path`, `span`, `dev`, `scale_final`. |
| `morphStep` | [862–868](../../public/simulations/phasor-sums.html#L862-L868) | One low-pass step of the drawn path toward the exact one. |
| `ensureAudio` | [875–882](../../public/simulations/phasor-sums.html#L875-L882) | Creates the AudioContext and analyser once. |
| `loadAudio` | [883–895](../../public/simulations/phasor-sums.html#L883-L895) | Plays a chosen file through the analyser (object URL; nothing uploaded). |
| `audioControl` | [896–901](../../public/simulations/phasor-sums.html#L896-L901) | Play, pause, stop. |
| `analyse` (with inner `band`) | [902–935](../../public/simulations/phasor-sums.html#L902-L935) | Band levels, beat detection, BPM, burst and beat-pulse decay. |
| `buildLive` | [938–955](../../public/simulations/phasor-sums.html#L938-L955) | Danced copy `live`; writes the `arm` arrays, `N`, `dance`, `burst`. |
| `speedFactor` | [956](../../public/simulations/phasor-sums.html#L956) | $1 + \text{mid}\cdot d_\text{speed}$ while dancing, else 1. |
| `paintRange` | [964–967](../../public/simulations/phasor-sums.html#L964-L967) | Sets `--p` on a card slider for its filled track. |
| `ctl` | [968–971](../../public/simulations/phasor-sums.html#L968-L971) | HTML for one card slider. |
| `renderList` | [972–985](../../public/simulations/phasor-sums.html#L972-L985) | Rebuilds all cards. |
| `syncList` | [986–995](../../public/simulations/phasor-sums.html#L986-L995) | Moves the card sliders to the list (during replay). |
| `#plist` input / change / click | [996–1015](../../public/simulations/phasor-sums.html#L996-L1015) | Card slider edits, bounce-curve choice, remove a card. |
| `recolour` | [1017](../../public/simulations/phasor-sums.html#L1017) | Colours by position from `COLS`. |
| `formula` | [1018–1028](../../public/simulations/phasor-sums.html#L1018-L1028) | Prints eq. (6) with the stored numbers via `katex.render`, HTML fallback. |
| `typeset` listener | [1029](../../public/simulations/phasor-sums.html#L1029) | Re-renders the formula once KaTeX has loaded. |
| `edited` | [1030–1036](../../public/simulations/phasor-sums.html#L1030-L1036) | After any list change: clear trail, `t = 0`, `refinal`, formula, readouts. |
| `load` | [1037–1043](../../public/simulations/phasor-sums.html#L1037-L1043) | Loads `[A, ω, φ, curve]` triples. |
| `reach` | [1048–1053](../../public/simulations/phasor-sums.html#L1048-L1053) | Outermost point drawn in the Live view. |
| `fit` | [1054–1058](../../public/simulations/phasor-sums.html#L1054-L1058) | Grow-at-once, relax-over-0.6-s fit radius. |
| `baseScale`, `finalScale` | [1059–1064](../../public/simulations/phasor-sums.html#L1059-L1064) | Pixels per unit for the two views. |
| `axes`, `polyline` | [1065–1080](../../public/simulations/phasor-sums.html#L1065-L1080) | Axis lines; a stroked run of points. |
| `draw` | [1081–1152](../../public/simulations/phasor-sums.html#L1081-L1152) | Paints one frame and writes the drawing variables; in the Live view its arm loop ([1120–1122](../../public/simulations/phasor-sums.html#L1120-L1122)) stores each arm's radius, step, partial sum and joint position. |
| `readouts` | [1155–1167](../../public/simulations/phasor-sums.html#L1155-L1167) | Writes `E`, `G`, `g`, `M`, `q`, `n_active`, `period`; fills the readouts and caption. |
| `hud` | [1168–1174](../../public/simulations/phasor-sums.html#L1168-L1174) | Beat dot, BPM, three level meters. |
| `recTime`, `snapshot`, `status`, `perform` | [1178–1213](../../public/simulations/phasor-sums.html#L1178-L1213) | Recording clock, one snapshot, status line, record/replay step. |
| Performance buttons | [1214–1250](../../public/simulations/phasor-sums.html#L1214-L1250) | Record, Stop, Replay, Export JSON, Import JSON. |
| `setMode` | [1253–1261](../../public/simulations/phasor-sums.html#L1253-L1261) | Live or Final view. |
| Other control listeners | [1262–1290](../../public/simulations/phasor-sums.html#L1262-L1290) | View buttons, Clear trail, Add, Randomise, presets, switches, audio file and drop zone. |
| `Sim.live` | [1293–1312](../../public/simulations/phasor-sums.html#L1293-L1312) | Formatted store values for the walkthrough. |
| clock callback | [1315–1350](../../public/simulations/phasor-sums.html#L1315-L1350) | The frame loop above. |
| `pixelAt`, `rgbText`, `lum` | [1354–1356](../../public/simulations/phasor-sums.html#L1354-L1356) | Read one canvas pixel; describe it; its luminance. |
| `isLive`, `trailAt`, `pathAt` | [1357–1359](../../public/simulations/phasor-sums.html#L1357-L1359) | Data-panel helpers from stored values. |
| `activeW`, `structureNow`, `sumNow`, `armInputs` | [1360–1363](../../public/simulations/phasor-sums.html#L1360-L1363) | Recompute from stored inputs, for Check only. |
| `phasorRound` | [1365–1368](../../public/simulations/phasor-sums.html#L1365-L1368) | Length of one recorded round: $T$ at Speed 0, else $\min(T, 20\cdot s_f)$. |
| `Sim.data` hooks | [1369–1467](../../public/simulations/phasor-sums.html#L1369-L1467) | `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `play`, `about`. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Radius A (per card) | generated, `data-f="amp"` | 0–2, step 0.01 | `phasors[i].amp` → `edited(false)` ([L977](../../public/simulations/phasor-sums.html#L977), [L996–1004](../../public/simulations/phasor-sums.html#L996-L1004)) |
| Angular frequency ω (per card) | `data-f="freq"` | −32 to 32 rad/s, step 0.01 | `phasors[i].freq` ([L978](../../public/simulations/phasor-sums.html#L978)) |
| Phase φ (per card) | `data-f="phase"` | 0–6.28 rad, step 0.01 | `phasors[i].phase` ([L979](../../public/simulations/phasor-sums.html#L979)) |
| Bounce curve (per card) | `data-curve` select | Linear (default) … Expo | `phasors[i].curve`, the `EASE` used for the bass ([L1005–1007](../../public/simulations/phasor-sums.html#L1005-L1007)) |
| × on a card | `data-rm` | — | Removes the arm, recolours ([L1008–1015](../../public/simulations/phasor-sums.html#L1008-L1015)) |
| Add circle | `add` | A = 0.5, ω = old N + 1, φ = 0 | [L1265–1269](../../public/simulations/phasor-sums.html#L1265-L1269) |
| Randomise | `random` | 2–6 arms, A 0.15–1.25, ω from a fixed list, φ 0–2π | [L1270–1275](../../public/simulations/phasor-sums.html#L1270-L1275) |
| Live / Final shape | `m-live`, `m-final` | Live | `setMode()` ([L1253–1263](../../public/simulations/phasor-sums.html#L1253-L1263)) |
| Play / Pause | `play` | playing (paused under reduced motion) | `Sim.playButton` ([L1351](../../public/simulations/phasor-sums.html#L1351), [sim.js:177](../../public/scripts/sim.js#L177)) |
| Clear trail | `clear` | — | `trail = []` ([L1264](../../public/simulations/phasor-sums.html#L1264)) |
| Speed | `speed` | 0–4, step 0.01, default 1 | read each frame into `lastSpeed` ([L112](../../public/simulations/phasor-sums.html#L112), [L1323](../../public/simulations/phasor-sums.html#L1323)) |
| Zoom | `zoom` | 0.3–1, default 1 | multiplies both scales ([L116](../../public/simulations/phasor-sums.html#L116), [L1103](../../public/simulations/phasor-sums.html#L1103)) |
| Trail length | `trail` | 100–6000, step 100, default 2400 | trail cut ([L120](../../public/simulations/phasor-sums.html#L120), [L1328–1329](../../public/simulations/phasor-sums.html#L1328-L1329)) |
| Component circles / Tip-to-tail vectors | `sw-circles`, `sw-vectors` | on / on | circle and arm drawing ([L1123](../../public/simulations/phasor-sums.html#L1123), [L1130](../../public/simulations/phasor-sums.html#L1130)) |
| Draw one full period | `sw-auto` | on | `spanNow()`; disables `span` ([L1280](../../public/simulations/phasor-sums.html#L1280)) |
| Span (if not one period) | `span` | 1–24 × 2π s, default 4, disabled | `spanNow()`, `refinal(false)` ([L131](../../public/simulations/phasor-sums.html#L131), [L790](../../public/simulations/phasor-sums.html#L790)) |
| Smooth morphing | `sw-morph` | on | α = slider or 1; change snaps ([L863](../../public/simulations/phasor-sums.html#L863), [L1281](../../public/simulations/phasor-sums.html#L1281)) |
| Morph rate α | `morph` | 0.02–0.35, default 0.08 | `morphStep()` ([L136](../../public/simulations/phasor-sums.html#L136)) |
| Presets | `presets`, `data-preset` | rose3 … flower | `load(PRESETS[...])` ([L1276–1279](../../public/simulations/phasor-sums.html#L1276-L1279)) |
| Audio file / drop zone | `afile`, `drop` | — | `loadAudio()` ([L1283–1287](../../public/simulations/phasor-sums.html#L1283-L1287)) |
| Audio Play / Pause / Stop | `a-play`, `a-pause`, `a-stop` | — | `audioControl()` ([L1288–1290](../../public/simulations/phasor-sums.html#L1288-L1290)) |
| Auto Dance | `dance` | off | `danceOn` ([L1282](../../public/simulations/phasor-sums.html#L1282)) |
| Bass drive / Speed drive / Beat burst / High drive | `d-bass`, `d-speed`, `d-burst`, `d-high` | 0–3, step 0.05; 1.5 / 1 / 0.6 / 0.6 | dance formulas ([L174–186](../../public/simulations/phasor-sums.html#L174-L186)) |
| Record / Stop / Replay / Export / Import | `rec`, `rec-stop`, `rec-play`, `rec-export`, `rec-import` (+ hidden `rec-file`) | — | [L1214–1250](../../public/simulations/phasor-sums.html#L1214-L1250) |

Readouts ([L206–212](../../public/simulations/phasor-sums.html#L206-L212)), filled by `readouts()` every 0.1 s:
`r-n` (circles), `r-z` ($|z|$ with the danced radii, [L1156](../../public/simulations/phasor-sums.html#L1156)),
`r-period` ($2\pi/g$, or "point" when $g = 0$), `r-fold` ("∞ (circle)" for one active arm, else `q`-fold), `r-energy`
($\sum A_k^2$). The caption carries `cap-mode` and `cap-t`.

## What the page writes into the data store

`Sim.dataset({ title: 'Phasor sums', attrs: { figure: 7, page, curves, length_unit } })`
([L709](../../public/simulations/phasor-sums.html#L709)); 73 variables declared at
[L710–785](../../public/simulations/phasor-sums.html#L710-L785) (count measured in headless Chromium). Dims: `arm`
(one per card, resized in `buildLive()` [L951](../../public/simulations/phasor-sums.html#L951) and `draw()`
[L1116](../../public/simulations/phasor-sums.html#L1116)), `path` ($n+1$ samples,
[L856](../../public/simulations/phasor-sums.html#L856)), `trail` ([L1332](../../public/simulations/phasor-sums.html#L1332)).
How `dim`, `var`, `alloc` and `set` work is in [dataset.md](../scripts/dataset.md).

| Group (as in `Sim.data.groups`) | Variables | Written at |
|---|---|---|
| Circles | `N`; `A`, `omega`, `phi`, `curve`, `mul`, `A_live` [arm]; `n_active` | [954](../../public/simulations/phasor-sums.html#L954); [953](../../public/simulations/phasor-sums.html#L953); [1159](../../public/simulations/phasor-sums.html#L1159) |
| The sum z(t) | `t`; `x`, `y`, `absz`, `absz2`; `E` | [1338](../../public/simulations/phasor-sums.html#L1338); [1119](../../public/simulations/phasor-sums.html#L1119) (Live view only); [1159](../../public/simulations/phasor-sums.html#L1159) |
| Arms and joints | `ang` [arm]; `A_arm`, `vx`, `vy`, `jx`, `jy`, `px`, `py` [arm]; `tip_px`, `tip_py` | [817](../../public/simulations/phasor-sums.html#L817), inside `sumAt()`, into the array that `draw()` passes at [1118](../../public/simulations/phasor-sums.html#L1118); [1122](../../public/simulations/phasor-sums.html#L1122), the arm loop of `draw()`; [1119](../../public/simulations/phasor-sums.html#L1119) (Live view only) |
| Structure | `G`, `g`, `period`, `M`, `q` | [1159](../../public/simulations/phasor-sums.html#L1159) |
| Final shape | `n_path`, `span`; `final_x`, `final_y` [path]; `path_x`, `path_y` [path]; `dev`, `scale_final`; `span_slider`, `auto`, `morph_on`, `morph_slider`, `alpha` | [859](../../public/simulations/phasor-sums.html#L859); [858](../../public/simulations/phasor-sums.html#L858); [858](../../public/simulations/phasor-sums.html#L858), [1093](../../public/simulations/phasor-sums.html#L1093); [859](../../public/simulations/phasor-sums.html#L859), [1083](../../public/simulations/phasor-sums.html#L1083), [1094](../../public/simulations/phasor-sums.html#L1094); [1339](../../public/simulations/phasor-sums.html#L1339) |
| Trail | `trail_max`, `trail_len`; `trail_x`, `trail_y` [trail] | [1338](../../public/simulations/phasor-sums.html#L1338); [1334](../../public/simulations/phasor-sums.html#L1334) |
| Dance and audio | `dance`, `burst`; `bass`, `mid`, `high`, `bpm`, `beat`; `d_bass`, `d_speed`, `d_burst`, `d_high` | [954](../../public/simulations/phasor-sums.html#L954); [1319](../../public/simulations/phasor-sums.html#L1319); [1340](../../public/simulations/phasor-sums.html#L1340) |
| Time and drawing | `dt`, `spd`, `sf`, `zoom`; `mode`, `cx`, `cy`, `box_w`, `box_h`; `fitR`, `scale`; `circles`, `vectors`; `fps`, `frames`, `playing` | [1338](../../public/simulations/phasor-sums.html#L1338); [1083](../../public/simulations/phasor-sums.html#L1083); [1104](../../public/simulations/phasor-sums.html#L1104) (Live view only); [1340](../../public/simulations/phasor-sums.html#L1340); [1341](../../public/simulations/phasor-sums.html#L1341) |

Each variable's `computed_in` attribute names that place ([L725–732](../../public/simulations/phasor-sums.html#L725-L732)): `ang` "sumAt(), with the
live-view output array"; `vx`, `vy` "sumAt(), read in draw()", since `sumAt()` computes them and the arm loop stores them;
`A_arm`, `jx`, `jy`, `px`, `py` "draw(), the arm loop", where they are computed.

Measured at load on a 1440 px wide window: `box_w × box_h` = 770 × 601, `scale` = 132.22 px per unit for the 3-petal
rose (`fitR` = 2), `n_path` = 1500, `period` = π s, `q` = 3; on a 390 px window 356 × 356 and 78.32 px per unit.

**One round** (`Sim.data.round`, [L1462–1464](../../public/simulations/phasor-sums.html#L1462-L1464)): the time variable
is `t`; the length is `phasorRound()` ([L1365–1368](../../public/simulations/phasor-sums.html#L1365-L1368)). Let $T = 2\pi/g$ be the time after which the
figure closes ($2\pi$ s when $g = 0$) and $s_f$ the stored speed `sf`. Phasor time runs $s_f$ times as fast as real time, so
for $s_f > 0$ a round is $\min(T, 20\,s_f)$ of phasor time, which never takes more than 20 s of real time. At $s_f = 0$ the
length is the full figure, $T$; phasor time does not run then, so recording is blocked and the Record box says why: "Set
Speed above 0: phasor time does not advance at Speed 0." ([L1464](../../public/simulations/phasor-sums.html#L1464)). It is also blocked in the Final view. The label
says "one full figure" or "part of the figure", with the length ([L1463](../../public/simulations/phasor-sums.html#L1463)). Columns: `x`, `y`, `absz`, `sf`; the
point followed is the pen. If Speed becomes 0 during a round, the panel says why it is waiting; raising Speed resumes the
same round.
How rounds are recorded and saved: [datalog.md](../scripts/datalog.md).

**Data-panel hooks.** `probe` pins the nearest joint, the pen or a trail point within 12 px in the Live view, or a
path point in the Final view ([L1384–1397](../../public/simulations/phasor-sums.html#L1384-L1397)). `check` recomputes
34 variables from stored inputs only ([L1414–1455](../../public/simulations/phasor-sums.html#L1414-L1455)). `drawn`
reads pixels back for `tip_px`, `px`, `path_x`, `trail_x`; each test first requires alpha > 0, then a dark colour
where it expects one ([L1456–1461](../../public/simulations/phasor-sums.html#L1456-L1461)). The file base name is
`fig7-phasor-sums` ([L1370](../../public/simulations/phasor-sums.html#L1370)).

**`Sim.live()`** ([L1293–1312](../../public/simulations/phasor-sums.html#L1293-L1312)) returns formatted strings read
from the store: `t, N, x, y, absz, absz2, E, G, g, Tc, M, q, dt, spd, sf, n, span, alpha, dev, bass, mid, high,
burst, dance`, and for arm 1 `A, w, ph, ang, x1, y1, mul, Ar` ("no circles" when the list is empty). These are the
keys the walkthrough tables use.

## Page structure

Head ([L1–42](../../public/simulations/phasor-sums.html#L1-L42)): `styles/sim.css` (which imports the Google Fonts,
KaTeX CSS and `paper.css`, [sim.css:7–9](../../public/styles/sim.css#L7-L9)), `styles/data.css`, `styles/fold.css`, an
inline favicon and an inline `<style>` for the cards, selects, drop zone, meters and formula box
([L15–41](../../public/simulations/phasor-sums.html#L15-L41)). See [styles.md](../styles.md).

Body: the top bar with the hand-written Fig. links 1–10 ([L44–59](../../public/simulations/phasor-sums.html#L44-L59));
the head ([L63–67](../../public/simulations/phasor-sums.html#L63-L67)); the figure `#stage` with canvas `#field` and
its caption ([L71–79](../../public/simulations/phasor-sums.html#L71-L79)); the card list `#plist` and formula box
([L81–96](../../public/simulations/phasor-sums.html#L81-L96)); the controls aside with readouts and legend
([L99–218](../../public/simulations/phasor-sums.html#L99-L218)); the lecture note
([L221–649](../../public/simulations/phasor-sums.html#L221-L649)); the walkthrough host `#walk`
(`data-walk="phasors"`, [L651](../../public/simulations/phasor-sums.html#L651)); the footer. `datalog.js` adds the data
tab, the *Read values* switch in the caption and the reading strip under `#stage`
([datalog.js:567–590](../../public/scripts/datalog.js#L567-L590)).

Scripts, in load order: `fold.js`, `sim.js`, `dataset.js`, the page script
([L662–1474](../../public/simulations/phasor-sums.html#L662-L1474)), `datalog.js`
([L659–1475](../../public/simulations/phasor-sums.html#L659-L1475)). `sim.js` loads the walkthrough file named by
`data-walk` ([sim.js:404–410](../../public/scripts/sim.js#L404-L410)) and typesets the note with KaTeX
([sim.js:339–367](../../public/scripts/sim.js#L339-L367)); see [sim.md](../scripts/sim.md), [walk.md](../scripts/walk.md),
[fold.md](../scripts/fold.md).

Lecture note "Phasor sums: circles riding on circles": 9 sections (`.psec`): 1 Circles riding on circles; 2 A turning
arrow: Euler's formula (2.1, 2.2 ★, 2.3); 3 The model (3.1); 4 Two arms: roses and beats (4.1, 4.2, box "One formula,
two pictures", Exercise 4.1); 5 When the curve closes ★ (5.1, Exercise 5.1); 6 The average size of the curve; 7 How
the page computes it (7.1); 8 From the plane to pixels, and from sound to radii (8.1); 9 What the model leaves out
(9.1 Further reading, 4 references). 17 numbered display equations (counted in the rendered page). Five figures,
all inline SVG: Figure 1 Euler's formula ([L264–305](../../public/simulations/phasor-sums.html#L264-L305)); Figure 2 the
Spirograph preset as a chain ([L321–370](../../public/simulations/phasor-sums.html#L321-L370)); Figure 3 beats
([L394–438](../../public/simulations/phasor-sums.html#L394-L438)); Figure 4 two plates, 3-petal rose and Star
([L459–529](../../public/simulations/phasor-sums.html#L459-L529)); Figure 5 $|z|^2$ for the Star
([L543–593](../../public/simulations/phasor-sums.html#L543-L593)). Its curves sit in a group ([L573–582](../../public/simulations/phasor-sums.html#L573-L582)) clipped by `f7clipc4`, a rectangle
from x = 64 to 699 ([L546](../../public/simulations/phasor-sums.html#L546)), so the dashed marker of the full period at x = 698, 1.4 units wide
([L578](../../public/simulations/phasor-sums.html#L578)), shows whole.

## Where the drawing and the store differ

The page states this in its `about` paragraph, shown in the data panel
([L1466](../../public/simulations/phasor-sums.html#L1466), [datalog.js:165](../../public/scripts/datalog.js#L165)):

- **Trail.** `trail_x`, `trail_y` are history: the pen at the end of each past frame, spaced by $\Delta t$ times the
  speed, joined by straight segments and faded in 12 chunks. With Auto Dance on, old points were made with old radii.
- **Morphing.** In the Final view `path_x`, `path_y` lag `final_x`, `final_y`; `dev` is the largest gap. The curves in
  between are point-by-point blends, not curves any phasor list draws.
- **Fit radius.** `fitR` relaxes over 0.6 s; it is history, not a formula of the current frame.
- **Dance.** The arms are drawn with `A_live`, while `E` and the period use the stored `A`.
- **Readouts** refresh every 0.1 s; the store refreshes every frame. Values in the panel are rounded; the store keeps
  full doubles.
- **Pixels.** The pen dot has radius 5.5 px, so the pixel at `tip_px`, `tip_py` is its fill; the trail and path are
  1.8 px strokes that circles or arms may cover.

## How to change it safely

- **Walkthrough excerpts.** `phasors.js` quotes these page lines verbatim (checked by script):
  [816–821](../../public/simulations/phasor-sums.html#L816-L821), [829–834](../../public/simulations/phasor-sums.html#L829-L834),
  [845](../../public/simulations/phasor-sums.html#L845), [865–866](../../public/simulations/phasor-sums.html#L865-L866),
  [943–948](../../public/simulations/phasor-sums.html#L943-L948), [1157–1158](../../public/simulations/phasor-sums.html#L1157-L1158),
  [1323–1325](../../public/simulations/phasor-sums.html#L1323-L1325). Change both together; add store taps after a quoted
  line, never inside a quoted run.
- **Formulas live three times.** In the code, in the `formula` string of each `ds.var` declaration, and in `check`.
  `structure()` is repeated as `structureNow()` ([L1361](../../public/simulations/phasor-sums.html#L1361)), `sumAt()` as
  `sumNow()` ([L1362](../../public/simulations/phasor-sums.html#L1362)), the dance multiplier in `check.mul`
  ([L1415–1421](../../public/simulations/phasor-sums.html#L1415-L1421)), the sample count and span in `check.n_path` and
  `check.span` ([L1445–1446](../../public/simulations/phasor-sums.html#L1445-L1446)), the 0.44 scale in
  `check.scale_final` and `check.scale` ([L1451–1452](../../public/simulations/phasor-sums.html#L1451-L1452)).
- **The 0.01 step is load-bearing.** `round(100 ω)` in `structure()` and `activeW()` assumes the ω slider step of 0.01
  ([L970](../../public/simulations/phasor-sums.html#L970)). Changing the step needs a new integer scale in both places
  and in lecture note section 5.
- **Numbers quoted in the note.** Slider ranges (note [L319](../../public/simulations/phasor-sums.html#L319)), sample
  rule and trail default (section 7, [L601–602](../../public/simulations/phasor-sums.html#L601-L602)), morph default
  (section 7.1), audio rules (section 8.1) and the presets (sections 3.1–6, Figures 2–5) are all written into the note
  and its SVG figures. Changing a preset or a constant means recomputing those figures and numbers.
- **Fig. links** at the top ([L48–57](../../public/simulations/phasor-sums.html#L48-L57)) are hand-written on every page.
- **Re-test**: open the page in headless Chromium, check there are no console errors; in the data panel run Check on
  `x`, `ang`, `px`, `tip_px` and `final_x`; record one round; confirm the walkthrough "Now" column fills; switch to
  Final shape and move a card slider to see the morph and `dev` fall to 0.

## Notes for maintainers

1. Fixed on 2026-10-15: all four real SVG clip paths have unique ids; computed clip-path is active, with identical phone pixels and only 28 edge pixels changed on desktop (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
2. Fixed on 2026-10-15: the morph gap description says every sample (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
3. Fixed on 2026-10-15: the multiplier is named live[i].mul (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
4. Fixed on 2026-10-15: the walkthrough reads stored effective alpha; Smooth morphing off shows 1.00 even with the slider at 0.08 (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
5. Fixed on 2026-10-15: sumAt writes each live angle into the allocated ang array; draw does not recompute it (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
6. Fixed on 2026-10-15: Speed 0 has an explicit recording guard and waiting reason; a running round resumes after Speed is raised (commit [9d3175f](https://github.com/Numa1997/SiteTest/commit/9d3175f2cf50d0ad3f8792f1ee173e8ce56bab53)).
7. Fixed on 2026-10-15: the uncalled nz helper was removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
8. **Replay does not wrap phases.** `perform()` moves each phase linearly toward the snapshot
   ([L1204](../../public/simulations/phasor-sums.html#L1204)), so a recorded change from 6.2 to 0.1 rad sweeps the arm
   backwards through almost a full turn over about 50 ms.
9. Fixed on 2026-10-15: `computed_in` of `A_arm`, `jx`, `jy`, `px`, `py` reads "draw(), the arm loop" again
   ([L725](../../public/simulations/phasor-sums.html#L725), [L729–732](../../public/simulations/phasor-sums.html#L729-L732)); Batch D ([ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)) had labelled them `sumAt()`, which computes only the angles and
   the steps (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
10. Fixed on 2026-10-15: `phasorRound()` no longer raises Speed to 0.05. At Speed 0 a round is the full figure and recording
    is blocked with its reason in view; for Speed above 0 the round is $\min(T, 20\cdot s_f)$, never more than 20 s of real
    time ([L1365–1368](../../public/simulations/phasor-sums.html#L1365-L1368)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
11. Fixed on 2026-10-15: the clip rectangle `f7clipc4` of note Figure 5 is 1 unit wider (x 64 + 635), so the dashed marker at
    x = 698 is no longer cut in half ([L546](../../public/simulations/phasor-sums.html#L546), [L578](../../public/simulations/phasor-sums.html#L578)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
