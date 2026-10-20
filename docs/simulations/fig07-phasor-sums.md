# Fig. 7 · Phasor Sums

| | |
|---|---|
| Page | [public/simulations/phasor-sums.html](../../public/simulations/phasor-sums.html) (1 479 lines, 261 179 bytes) |
| Walkthrough | [public/scripts/walk/phasors.js](../../public/scripts/walk/phasors.js) (key `phasors`, 8 steps) |
| Thumbnail | [public/images/sims/phasor-sums.webp](../../public/images/sims/phasor-sums.webp) (800 × 500 px: the 3-petal rose with its two arms and circles) |
| Catalog entry | [public/scripts/catalog.js#L150](../../public/scripts/catalog.js#L150) (`id: 'phasor-sums'`, `fig: 7`, field `methods`, stage 2) |

Links of the form `[L816]` point into `phasor-sums.html`.

The reader sees a chain of arms on a canvas. Each arm turns at a steady rate about the tip of the one before it,
and the tip of the last arm, the pen, leaves a burgundy trail. One card per arm sets its radius, angular frequency,
phase and "bounce curve" ([L973–986](../../public/simulations/phasor-sums.html#L973-L986)). Ten presets load roses,
beats, a trefoil, a star and Spirograph-like curves ([L669–680](../../public/simulations/phasor-sums.html#L669-L680)).
A *Final shape* view draws the whole closed curve at once and morphs it when a slider moves. An audio file can drive
the radii ("Auto Dance"), and a performance of slider changes can be recorded, replayed and saved as JSON. The page
opens on the 3-petal rose ([L1471](../../public/simulations/phasor-sums.html#L1471)).

## The physics in one picture

Everyday picture: a fairground ride whose cars spin on the ends of a turning arm, Ptolemy's epicycles, a Spirograph,
or the 50 Hz mains voltage drawn as a turning arrow (lecture note section 1,
[L244–250](../../public/simulations/phasor-sums.html#L244-L250)).

Model: each arm has a prescribed angle that increases at constant angular velocity. Placing
an arm on a moving tip adds its arrow to that tip's position, so the pen is a sum of complex numbers (note section 3,
[L315–320](../../public/simulations/phasor-sums.html#L315-L320)). Everything on screen is kinematics.

The equations the code evaluates:

$$x(t) = \sum_{k=1}^{N} A'_k \cos(\omega_k t + \varphi_k), \qquad y(t) = \sum_{k=1}^{N} A'_k \sin(\omega_k t + \varphi_k), \qquad z = x + iy$$

with $A'_k = A_k\, m_k$ ([L817–821](../../public/simulations/phasor-sums.html#L817-L821),
[L949](../../public/simulations/phasor-sums.html#L949)). $A_k$ is the stored radius, a scale-free length (only ratios
matter; the picture is scaled to fit). $\omega_k$ is the angular frequency in rad/s, $\varphi_k$ the phase in rad,
$t$ the phasor time in s. $m_k$ is the dance multiplier, exactly 1 while Auto Dance is off
([L943](../../public/simulations/phasor-sums.html#L943)).

Closure and symmetry use integers $w_k = \mathrm{round}(100\,\omega_k)$ over the arms with $A_k > 0$
([L830](../../public/simulations/phasor-sums.html#L830)):

$$G = \gcd_k w_k, \quad g = G/100\ \mathrm{rad/s}, \quad T = 2\pi/g; \qquad M = \gcd_k (w_k - w_1), \quad q = M/\gcd(w_1, M)$$

([L832–835](../../public/simulations/phasor-sums.html#L832-L835)). $T$ in s is a common repeat time for the listed active arms; cancelling equal-frequency terms can shorten the pen's true period. The integer $q$ describes the listed-arm rotational symmetry. The time average of the squared distance, for distinct
frequencies, is $\langle |z|^2 \rangle = \sum_k A_k^2$ ([L1159](../../public/simulations/phasor-sums.html#L1159)).

The lecture note derives these: Euler's formula (section 2, eqs. 1–5), the model (section 3, eq. 6, velocity eq. 7),
roses and beats (section 4, eqs. 8–11), closure and symmetry (section 5, eqs. 12–13), Parseval (section 6, eqs. 14–15),
morphing as a low-pass filter (section 7.1, eq. 16) and the screen mapping (section 8, eq. 17).

## How the code computes it

**State** ([L704–707](../../public/simulations/phasor-sums.html#L704-L707)). `phasors` holds the stored list, one
object `{ amp, freq, phase, color, curve }` per card. `live` is a per-frame copy with the danced radius. `t` is phasor
time in s. `trail` is the list of past pen positions. `finalPath` holds the exact samples of the closed curve,
`morphPath` the samples as drawn. `fitR` is the radius the Live view is fitted to.

**Method: closed form, no integrator.** The sum is evaluated directly at the current $t$; nothing is integrated, so
no error accumulates from frame to frame (note section 7, [L600](../../public/simulations/phasor-sums.html#L600)).
Each frame costs $N$ cosines and $N$ sines in `sumAt()` ([L813–825](../../public/simulations/phasor-sums.html#L813-L825)),
called twice per frame with the same arguments: once for the new trail point
([L1327](../../public/simulations/phasor-sums.html#L1327)) and once in `draw()`
([L1119](../../public/simulations/phasor-sums.html#L1119)).

Period and symmetry are found exactly because the sliders move in steps of 0.01 rad/s
([L971](../../public/simulations/phasor-sums.html#L971)): $100\,\omega$ is an integer and Euclid's algorithm `gcd()`
([L806–810](../../public/simulations/phasor-sums.html#L806-L810)) works on integers.

**Frame loop**, the `Sim.clock` callback ([L1316–1351](../../public/simulations/phasor-sums.html#L1316-L1351)), in order:

1. `real` = wall time since the last frame, capped at 0.05 s ([L1317](../../public/simulations/phasor-sums.html#L1317)).
   The clock's own `dt` is the same cap but 0 while paused ([sim.js:179–181](../../public/scripts/sim.js#L179-L181)).
2. `analyse(real)`: audio bands, beat detection, burst decay ([L903–936](../../public/simulations/phasor-sums.html#L903-L936)).
3. `perform(real)`: record a snapshot every 50 ms, or replay ([L1184–1214](../../public/simulations/phasor-sums.html#L1184-L1214)).
4. `buildLive()`: copy the list with the dance multipliers ([L939–956](../../public/simulations/phasor-sums.html#L939-L956)).
   This runs even while paused, so with Auto Dance on the arms still breathe when time stands still.
5. Speed: `lastSpeed = speed.value * speedFactor()` ([L1324](../../public/simulations/phasor-sums.html#L1324)).
6. Live view only, and only when `dt > 0`: `t += dt * lastSpeed`, push $z(t)$ onto `trail`, cut the trail to the
   *Trail length* slider ([L1325–1331](../../public/simulations/phasor-sums.html#L1325-L1331)).
7. Final view only: `morphStep()` moves every drawn sample the fraction $\alpha$ toward the exact one
   ([L863–869](../../public/simulations/phasor-sums.html#L863-L869), [L1336](../../public/simulations/phasor-sums.html#L1336)).
   This also runs while paused.
8. `fit(real)`: the fit radius jumps up at once and relaxes down with a time constant of 0.6 s
   ([L1055–1059](../../public/simulations/phasor-sums.html#L1055-L1059)). The target is `reach()`: $\sum |A'_k|$ or the
   farthest trail point, whichever is larger ([L1049–1054](../../public/simulations/phasor-sums.html#L1049-L1054)).
9. Write the frame scalars into the store ([L1338–1342](../../public/simulations/phasor-sums.html#L1338-L1342)), then `draw()`.
10. Every 0.1 s: `readouts()`, and while replaying, `syncList()` and `formula()`
    ([L1344–1349](../../public/simulations/phasor-sums.html#L1344-L1349)). Then `hud()` paints the audio meters.

**Drawing** (`draw()`, [L1082–1153](../../public/simulations/phasor-sums.html#L1082-L1153)). A point $(x, y)$ goes to the
pixel $(c_x + s\,x,\ c_y - s\,y)$ with $(c_x, c_y)$ the canvas centre
([L1077](../../public/simulations/phasor-sums.html#L1077)). In the Live view
$s = 0.44\,\min(w,h)/\max(R_\text{fit}, 0.05)\times\text{zoom}$ ([L1060](../../public/simulations/phasor-sums.html#L1060),
[L1104](../../public/simulations/phasor-sums.html#L1104)). The trail is drawn in 12 chunks with opacity
$0.18 + 0.82\,(c+1)/12$, so 0.25 for the oldest ([L1107–1114](../../public/simulations/phasor-sums.html#L1107-L1114)).
Then each arm: its circle in `T.rose` about the joint it turns on, its arm and a 3 px dot in the card's colour
([L1121–1145](../../public/simulations/phasor-sums.html#L1121-L1145)); the pen is a 5.5 px burgundy dot with a 2 px
outline in the card colour `T.card` (`#fffaf3`; the paper colour is `T.paper`) ([L1146–1152](../../public/simulations/phasor-sums.html#L1146-L1152)). In the Final view the
scale uses the largest $|z|$ of the drawn path instead of $R_\text{fit}$
([L1061–1065](../../public/simulations/phasor-sums.html#L1061-L1065)), and the path is drawn as a 6 px pale-rose band
under a 1.8 px burgundy line ([L1096–1101](../../public/simulations/phasor-sums.html#L1096-L1101)).

**Precomputation.** `refinal(snap)` ([L844–861](../../public/simulations/phasor-sums.html#L844-L861)) samples the closed
curve at $n+1$ times $t_i = i\,T_\text{span}/n$. The span comes from `spanNow()`
([L838–842](../../public/simulations/phasor-sums.html#L838-L842)): with *Draw one full period* on and $g > 0$ it is
$\min(2\pi/g,\ 60\cdot 2\pi)$ s, otherwise the *Span* slider times $2\pi$ s. The sample count is
$n = \max(1500, \min(12000, \mathrm{round}(700\,T_\text{span}/2\pi)))$
([L846](../../public/simulations/phasor-sums.html#L846)). `refinal()` runs on every card edit (through `edited()`,
[L1031–1037](../../public/simulations/phasor-sums.html#L1031-L1037)), on the span controls and on entering the Final view
([L1260](../../public/simulations/phasor-sums.html#L1260)). It snaps `morphPath` to the new curve when asked, when
morphing is off, or when the sample count changed, because then there is nothing to blend
([L854–856](../../public/simulations/phasor-sums.html#L854-L856)). Every edit also resets `t = 0` and clears the trail.

**Audio** (lecture note section 8.1). `ensureAudio()` builds a Web Audio analyser with `fftSize = 2048` and smoothing
0.8 ([L876–883](../../public/simulations/phasor-sums.html#L876-L883)). Bands are averages of byte bins divided by 255:
bass 20–150 Hz, mid 150–4000 Hz, high 4–16 kHz, each smoothed by `e += 0.15 (raw − e)` per frame
([L906–915](../../public/simulations/phasor-sums.html#L906-L915)). A beat is a raw bass level more than 35 % above the
previous frame's, above 0.22, at least 280 ms after the last beat; it sets `burst = 1 + d_burst`, which falls back
linearly over 10 frames, and the tempo is 60 000 over the median of the last 8 intervals in ms
([L917–935](../../public/simulations/phasor-sums.html#L917-L935)). In `buildLive()`, arms with $|\omega|$ at or below
the median of all $|\omega_k|$ get
$m = 1 + \mathrm{ease}(\text{bass})\,d_\text{bass}\,(1 - 0.7\,|\omega|/|\omega|_\text{max})$, faster arms
$m = 1 + \text{high}\cdot d_\text{high}$, and both are multiplied by `burst`
([L945–947](../../public/simulations/phasor-sums.html#L945-L947)). The easing curves are written inline in `EASE`
([L683–697](../../public/simulations/phasor-sums.html#L683-L697)). The mid band speeds up time by
$1 + \text{mid}\cdot d_\text{speed}$ ([L957](../../public/simulations/phasor-sums.html#L957)). The stored $A, \omega,
\varphi$ are never changed by the dance.

**Record and replay** ([L1178–1251](../../public/simulations/phasor-sums.html#L1178-L1251)). A snapshot
`{ t, d, p: [{ a, f, h, c }] }` of the whole list is taken every 50 ms against the audio time, or against wall time
without audio ([L1179–1182](../../public/simulations/phasor-sums.html#L1179-L1182)). Replay finds the last snapshot not
later than the current time and moves each value the fraction $\min(1, \Delta t/0.05)$ toward it per frame
([L1195–1207](../../public/simulations/phasor-sums.html#L1195-L1207)); if the number of circles differs it reloads the list
outright. Export writes `phasor-performance.json` as `{ v: 1, timeline }`
([L1232–1233](../../public/simulations/phasor-sums.html#L1232-L1233)); import accepts that object or a bare array
([L1246](../../public/simulations/phasor-sums.html#L1246)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `EASE.*` (6 curves) | [683–697](../../public/simulations/phasor-sums.html#L683-L697) | Easing curves for the bass response: Linear, Bounce, Elastic, Back, Sine, Expo. |
| `$` | [699](../../public/simulations/phasor-sums.html#L699) | `document.getElementById`. |
| `wrap` | [799](../../public/simulations/phasor-sums.html#L799) | Angle into $[0, 2\pi)$; applied to every phase that `load()` takes in. |
| `clamp01` | [800](../../public/simulations/phasor-sums.html#L800) | Clamp to $[0, 1]$. |
| `median` | [801–805](../../public/simulations/phasor-sums.html#L801-L805) | Median of an array (beat intervals, $|\omega_k|$). |
| `gcd` | [806–810](../../public/simulations/phasor-sums.html#L806-L810) | Euclid's algorithm on integers. |
| `sumAt` | [813–825](../../public/simulations/phasor-sums.html#L813-L825) | The phasor sum and each arm's $(\Delta x, \Delta y)$ at one time; an optional angles array receives the live angle at its calculation. |
| `structure` | [828–836](../../public/simulations/phasor-sums.html#L828-L836) | $G$, $g$, $M$, $q$ and the active count from `round(100 ω)`. |
| `spanNow` | [838–842](../../public/simulations/phasor-sums.html#L838-L842) | Time span of the Final shape. |
| `refinal` | [844–861](../../public/simulations/phasor-sums.html#L844-L861) | Samples the exact curve, snaps or keeps the morph path, writes `final_*`, `path_*`, `n_path`, `span`, `dev`, `scale_final`. |
| `morphStep` | [863–869](../../public/simulations/phasor-sums.html#L863-L869) | One low-pass step of the drawn path toward the exact one. |
| `ensureAudio` | [876–883](../../public/simulations/phasor-sums.html#L876-L883) | Creates the AudioContext and analyser once. |
| `loadAudio` | [884–896](../../public/simulations/phasor-sums.html#L884-L896) | Plays a chosen file through the analyser (object URL; nothing uploaded). |
| `audioControl` | [897–902](../../public/simulations/phasor-sums.html#L897-L902) | Play, pause, stop. |
| `analyse` (with inner `band`) | [903–936](../../public/simulations/phasor-sums.html#L903-L936) | Band levels, beat detection, BPM, burst and beat-pulse decay. |
| `buildLive` | [939–956](../../public/simulations/phasor-sums.html#L939-L956) | Danced copy `live`; writes the `arm` arrays, `N`, `dance`, `burst`. |
| `speedFactor` | [957](../../public/simulations/phasor-sums.html#L957) | $1 + \text{mid}\cdot d_\text{speed}$ while dancing, else 1. |
| `paintRange` | [965–968](../../public/simulations/phasor-sums.html#L965-L968) | Sets `--p` on a card slider for its filled track. |
| `ctl` | [969–972](../../public/simulations/phasor-sums.html#L969-L972) | HTML for one card slider. |
| `renderList` | [973–986](../../public/simulations/phasor-sums.html#L973-L986) | Rebuilds all cards. |
| `syncList` | [987–996](../../public/simulations/phasor-sums.html#L987-L996) | Moves the card sliders to the list (during replay). |
| `#plist` input / change / click | [997–1016](../../public/simulations/phasor-sums.html#L997-L1016) | Card slider edits, bounce-curve choice, remove a card. |
| `recolour` | [1018](../../public/simulations/phasor-sums.html#L1018) | Colours by position from `COLS`. |
| `formula` | [1019–1029](../../public/simulations/phasor-sums.html#L1019-L1029) | Prints eq. (6) with the stored numbers via `katex.render`, HTML fallback. |
| `typeset` listener | [1030](../../public/simulations/phasor-sums.html#L1030) | Re-renders the formula once KaTeX has loaded. |
| `edited` | [1031–1037](../../public/simulations/phasor-sums.html#L1031-L1037) | After any list change: clear trail, `t = 0`, `refinal`, formula, readouts. |
| `load` | [1038–1044](../../public/simulations/phasor-sums.html#L1038-L1044) | Loads `[A, ω, φ, curve]` triples. |
| `reach` | [1049–1054](../../public/simulations/phasor-sums.html#L1049-L1054) | Outermost point drawn in the Live view. |
| `fit` | [1055–1059](../../public/simulations/phasor-sums.html#L1055-L1059) | Grow-at-once, relax-over-0.6-s fit radius. |
| `baseScale`, `finalScale` | [1060–1065](../../public/simulations/phasor-sums.html#L1060-L1065) | Pixels per unit for the two views. |
| `axes`, `polyline` | [1066–1081](../../public/simulations/phasor-sums.html#L1066-L1081) | Axis lines; a stroked run of points. |
| `draw` | [1082–1153](../../public/simulations/phasor-sums.html#L1082-L1153) | Paints one frame and writes the drawing variables; in the Live view its arm loop ([1121–1123](../../public/simulations/phasor-sums.html#L1121-L1123)) stores each arm's radius, step, partial sum and joint position. |
| `readouts` | [1156–1168](../../public/simulations/phasor-sums.html#L1156-L1168) | Writes `E`, `G`, `g`, `M`, `q`, `n_active`, `period`; fills the readouts and caption. |
| `hud` | [1169–1175](../../public/simulations/phasor-sums.html#L1169-L1175) | Beat dot, BPM, three level meters. |
| `recTime`, `snapshot`, `status`, `perform` | [1179–1214](../../public/simulations/phasor-sums.html#L1179-L1214) | Recording clock, one snapshot, status line, record/replay step. |
| Performance buttons | [1215–1251](../../public/simulations/phasor-sums.html#L1215-L1251) | Record, Stop, Replay, Export JSON, Import JSON. |
| `setMode` | [1254–1262](../../public/simulations/phasor-sums.html#L1254-L1262) | Live or Final view. |
| Other control listeners | [1263–1291](../../public/simulations/phasor-sums.html#L1263-L1291) | View buttons, Clear trail, Add, Randomise, presets, switches, audio file and drop zone. |
| `Sim.live` | [1294–1313](../../public/simulations/phasor-sums.html#L1294-L1313) | Formatted store values for the walkthrough. |
| clock callback | [1316–1351](../../public/simulations/phasor-sums.html#L1316-L1351) | The frame loop above. |
| `pixelAt`, `rgbText`, `lum` | [1355–1357](../../public/simulations/phasor-sums.html#L1355-L1357) | Read one canvas pixel; describe it; its luminance. |
| `isLive`, `trailAt`, `pathAt` | [1358–1360](../../public/simulations/phasor-sums.html#L1358-L1360) | Data-panel helpers from stored values. |
| `activeW`, `structureNow`, `sumNow`, `armInputs` | [1361–1364](../../public/simulations/phasor-sums.html#L1361-L1364) | Recompute from stored inputs, for Check only. |
| `phasorRound` | [1366–1369](../../public/simulations/phasor-sums.html#L1366-L1369) | Length of one recorded round: $T$ at Speed 0, else $\min(T, 20\cdot s_f)$. |
| `Sim.data` hooks | [1370–1468](../../public/simulations/phasor-sums.html#L1370-L1468) | `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `play`, `about`. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Radius A (per card) | generated, `data-f="amp"` | 0–2, step 0.01 | `phasors[i].amp` → `edited(false)` ([L978](../../public/simulations/phasor-sums.html#L978), [L997–1005](../../public/simulations/phasor-sums.html#L997-L1005)) |
| Angular frequency ω (per card) | `data-f="freq"` | −32 to 32 rad/s, step 0.01 | `phasors[i].freq` ([L979](../../public/simulations/phasor-sums.html#L979)) |
| Phase φ (per card) | `data-f="phase"` | 0–6.28 rad, step 0.01 | `phasors[i].phase` ([L980](../../public/simulations/phasor-sums.html#L980)) |
| Bounce curve (per card) | `data-curve` select | Linear (default) … Expo | `phasors[i].curve`, the `EASE` used for the bass ([L1006–1008](../../public/simulations/phasor-sums.html#L1006-L1008)) |
| × on a card | `data-rm` | — | Removes the arm, recolours ([L1009–1016](../../public/simulations/phasor-sums.html#L1009-L1016)) |
| Add circle | `add` | A = 0.5, ω = old N + 1, φ = 0 | [L1266–1270](../../public/simulations/phasor-sums.html#L1266-L1270) |
| Randomise | `random` | 2–6 arms, A 0.15–1.25, ω from a fixed list, φ 0–2π | [L1271–1276](../../public/simulations/phasor-sums.html#L1271-L1276) |
| Live / Final shape | `m-live`, `m-final` | Live | `setMode()` ([L1254–1264](../../public/simulations/phasor-sums.html#L1254-L1264)) |
| Play / Pause | `play` | playing (paused under reduced motion) | `Sim.playButton` ([L1352](../../public/simulations/phasor-sums.html#L1352), [sim.js:177](../../public/scripts/sim.js#L177)) |
| Clear trail | `clear` | — | `trail = []` ([L1265](../../public/simulations/phasor-sums.html#L1265)) |
| Speed | `speed` | 0–4, step 0.01, default 1 | read each frame into `lastSpeed` ([L112](../../public/simulations/phasor-sums.html#L112), [L1324](../../public/simulations/phasor-sums.html#L1324)) |
| Zoom | `zoom` | 0.3–1, default 1 | multiplies both scales ([L116](../../public/simulations/phasor-sums.html#L116), [L1104](../../public/simulations/phasor-sums.html#L1104)) |
| Trail length | `trail` | 100–6000, step 100, default 2400 | trail cut ([L120](../../public/simulations/phasor-sums.html#L120), [L1329–1330](../../public/simulations/phasor-sums.html#L1329-L1330)) |
| Component circles / Tip-to-tail vectors | `sw-circles`, `sw-vectors` | on / on | circle and arm drawing ([L1124](../../public/simulations/phasor-sums.html#L1124), [L1131](../../public/simulations/phasor-sums.html#L1131)) |
| Draw one full period | `sw-auto` | on | `spanNow()`; disables `span` ([L1281](../../public/simulations/phasor-sums.html#L1281)) |
| Span (if not one period) | `span` | 1–24 × 2π s, default 4, disabled | `spanNow()`, `refinal(false)` ([L131](../../public/simulations/phasor-sums.html#L131), [L791](../../public/simulations/phasor-sums.html#L791)) |
| Smooth morphing | `sw-morph` | on | α = slider or 1; change snaps ([L864](../../public/simulations/phasor-sums.html#L864), [L1282](../../public/simulations/phasor-sums.html#L1282)) |
| Morph rate α | `morph` | 0.02–0.35, default 0.08 | `morphStep()` ([L136](../../public/simulations/phasor-sums.html#L136)) |
| Presets | `presets`, `data-preset` | rose3 … flower | `load(PRESETS[...])` ([L1277–1280](../../public/simulations/phasor-sums.html#L1277-L1280)) |
| Audio file / drop zone | `afile`, `drop` | — | `loadAudio()` ([L1284–1288](../../public/simulations/phasor-sums.html#L1284-L1288)) |
| Audio Play / Pause / Stop | `a-play`, `a-pause`, `a-stop` | — | `audioControl()` ([L1289–1291](../../public/simulations/phasor-sums.html#L1289-L1291)) |
| Auto Dance | `dance` | off | `danceOn` ([L1283](../../public/simulations/phasor-sums.html#L1283)) |
| Bass drive / Speed drive / Beat burst / High drive | `d-bass`, `d-speed`, `d-burst`, `d-high` | 0–3, step 0.05; 1.5 / 1 / 0.6 / 0.6 | dance formulas ([L174–186](../../public/simulations/phasor-sums.html#L174-L186)) |
| Record / Stop / Replay / Export / Import | `rec`, `rec-stop`, `rec-play`, `rec-export`, `rec-import` (+ hidden `rec-file`) | — | [L1215–1251](../../public/simulations/phasor-sums.html#L1215-L1251) |

Readouts ([L206–212](../../public/simulations/phasor-sums.html#L206-L212)), filled by `readouts()` every 0.1 s:
`r-n` (circles), `r-z` ($|z|$ with the danced radii, [L1157](../../public/simulations/phasor-sums.html#L1157)),
`r-period` ($2\pi/g$, or "point" when $g = 0$), `r-fold` ("∞ (circle)" for one active arm, else `q`-fold), `r-energy`
($\sum A_k^2$). The caption carries `cap-mode` and `cap-t`.

## What the page writes into the data store

`Sim.dataset({ title: 'Phasor sums', attrs: { figure: 7, page, curves, length_unit } })`
([L710](../../public/simulations/phasor-sums.html#L710)); 73 variables declared at
[L711–786](../../public/simulations/phasor-sums.html#L711-L786) (count measured in headless Chromium). Dims: `arm`
(one per card, resized in `buildLive()` [L952](../../public/simulations/phasor-sums.html#L952) and `draw()`
[L1117](../../public/simulations/phasor-sums.html#L1117)), `path` ($n+1$ samples,
[L857](../../public/simulations/phasor-sums.html#L857)), `trail` ([L1333](../../public/simulations/phasor-sums.html#L1333)).
How `dim`, `var`, `alloc` and `set` work is in [dataset.md](../scripts/dataset.md).

| Group (as in `Sim.data.groups`) | Variables | Written at |
|---|---|---|
| Circles | `N`; `A`, `omega`, `phi`, `curve`, `mul`, `A_live` [arm]; `n_active` | [955](../../public/simulations/phasor-sums.html#L955); [954](../../public/simulations/phasor-sums.html#L954); [1160](../../public/simulations/phasor-sums.html#L1160) |
| The sum z(t) | `t`; `x`, `y`, `absz`, `absz2`; `E` | [1339](../../public/simulations/phasor-sums.html#L1339); [1120](../../public/simulations/phasor-sums.html#L1120) (Live view only); [1160](../../public/simulations/phasor-sums.html#L1160) |
| Arms and joints | `ang` [arm]; `A_arm`, `vx`, `vy`, `jx`, `jy`, `px`, `py` [arm]; `tip_px`, `tip_py` | [818](../../public/simulations/phasor-sums.html#L818), inside `sumAt()`, into the array that `draw()` passes at [1119](../../public/simulations/phasor-sums.html#L1119); [1123](../../public/simulations/phasor-sums.html#L1123), the arm loop of `draw()`; [1120](../../public/simulations/phasor-sums.html#L1120) (Live view only) |
| Structure | `G`, `g`, `period`, `M`, `q` | [1160](../../public/simulations/phasor-sums.html#L1160) |
| Final shape | `n_path`, `span`; `final_x`, `final_y` [path]; `path_x`, `path_y` [path]; `dev`, `scale_final`; `span_slider`, `auto`, `morph_on`, `morph_slider`, `alpha` | [860](../../public/simulations/phasor-sums.html#L860); [859](../../public/simulations/phasor-sums.html#L859); [859](../../public/simulations/phasor-sums.html#L859), [1094](../../public/simulations/phasor-sums.html#L1094); [860](../../public/simulations/phasor-sums.html#L860), [1084](../../public/simulations/phasor-sums.html#L1084), [1095](../../public/simulations/phasor-sums.html#L1095); [1340](../../public/simulations/phasor-sums.html#L1340) |
| Trail | `trail_max`, `trail_len`; `trail_x`, `trail_y` [trail] | [1339](../../public/simulations/phasor-sums.html#L1339); [1335](../../public/simulations/phasor-sums.html#L1335) |
| Dance and audio | `dance`, `burst`; `bass`, `mid`, `high`, `bpm`, `beat`; `d_bass`, `d_speed`, `d_burst`, `d_high` | [955](../../public/simulations/phasor-sums.html#L955); [1320](../../public/simulations/phasor-sums.html#L1320); [1341](../../public/simulations/phasor-sums.html#L1341) |
| Time and drawing | `dt`, `spd`, `sf`, `zoom`; `mode`, `cx`, `cy`, `box_w`, `box_h`; `fitR`, `scale`; `circles`, `vectors`; `fps`, `frames`, `playing` | [1339](../../public/simulations/phasor-sums.html#L1339); [1084](../../public/simulations/phasor-sums.html#L1084); [1105](../../public/simulations/phasor-sums.html#L1105) (Live view only); [1341](../../public/simulations/phasor-sums.html#L1341); [1342](../../public/simulations/phasor-sums.html#L1342) |

Each variable's `computed_in` attribute names that place ([L726–733](../../public/simulations/phasor-sums.html#L726-L733)): `ang` "sumAt(), with the
live-view output array"; `vx`, `vy` "sumAt(), read in draw()", since `sumAt()` computes them and the arm loop stores them;
`A_arm`, `jx`, `jy`, `px`, `py` "draw(), the arm loop", where they are computed.

Measured at load on a 1440 px wide window: `box_w × box_h` = 770 × 601, `scale` = 132.22 px per unit for the 3-petal
rose (`fitR` = 2), `n_path` = 1500, `period` = π s, `q` = 3; on a 390 px window 356 × 356 and 78.32 px per unit.

**One round** (`Sim.data.round`, [L1463–1465](../../public/simulations/phasor-sums.html#L1463-L1465)): the time variable
is `t`; the length is `phasorRound()` ([L1366–1369](../../public/simulations/phasor-sums.html#L1366-L1369)). Let $T = 2\pi/g$ be the time after which the
figure closes ($2\pi$ s when $g = 0$) and $s_f$ the stored speed `sf`. Phasor time runs $s_f$ times as fast as real time, so
for $s_f > 0$ a round is $\min(T, 20\,s_f)$ of phasor time, which never takes more than 20 s of real time. At $s_f = 0$ the
length is the full figure, $T$; phasor time does not run then, so recording is blocked and the Record box says why: "Set
Speed above 0: phasor time does not advance at Speed 0." ([L1465](../../public/simulations/phasor-sums.html#L1465)). It is also blocked in the Final view. The label
says "one full figure" or "part of the figure", with the length ([L1464](../../public/simulations/phasor-sums.html#L1464)). Columns: `x`, `y`, `absz`, `sf`; the
point followed is the pen. If Speed becomes 0 during a round, the panel says why it is waiting; raising Speed resumes the
same round.
How rounds are recorded and saved: [datalog.md](../scripts/datalog.md).

**Data-panel hooks.** `probe` pins the nearest joint, the pen or a trail point within 12 px in the Live view, or a
path point in the Final view ([L1385–1398](../../public/simulations/phasor-sums.html#L1385-L1398)). `check` recomputes
34 variables from stored inputs only ([L1415–1456](../../public/simulations/phasor-sums.html#L1415-L1456)). `drawn`
reads pixels back for `tip_px`, `px`, `path_x`, `trail_x`; each test first requires alpha > 0, then a dark colour
where it expects one ([L1457–1462](../../public/simulations/phasor-sums.html#L1457-L1462)). The file base name is
`fig7-phasor-sums` ([L1371](../../public/simulations/phasor-sums.html#L1371)).

**`Sim.live()`** ([L1294–1313](../../public/simulations/phasor-sums.html#L1294-L1313)) returns formatted strings read
from the store: `t, N, x, y, absz, absz2, E, G, g, Tc, M, q, dt, spd, sf, n, span, alpha, dev, bass, mid, high,
burst, dance`, and for arm 1 `A, w, ph, ang, x1, y1, mul, Ar` ("no circles" when the list is empty). These are the
keys the walkthrough tables use.

## Page structure

Head ([L1–42](../../public/simulations/phasor-sums.html#L1-L42)): `styles/sim.css` (which imports the self-hosted fonts,
KaTeX CSS and `paper.css`, [sim.css:7–9](../../public/styles/sim.css#L7-L9)), `styles/data.css`, `styles/fold.css`, an
inline favicon and an inline `<style>` for the cards, selects, drop zone, meters and formula box
([L15–41](../../public/simulations/phasor-sums.html#L15-L41)). See [styles.md](../styles.md).

Body: the top bar: one span holding the Phyein Usul logo (a link to `../index.html` with
`../images/phyein-usul-mark.svg`, 87 × 48) and "← All simulations" ([L45](../../public/simulations/phasor-sums.html#L45)), then the hand-written Fig. links
1–10 ([L44–59](../../public/simulations/phasor-sums.html#L44-L59));
the head ([L63–67](../../public/simulations/phasor-sums.html#L63-L67)); the figure `#stage` with canvas `#field` and
its caption ([L71–79](../../public/simulations/phasor-sums.html#L71-L79)); the card list `#plist` and formula box
([L81–96](../../public/simulations/phasor-sums.html#L81-L96)); the controls aside with readouts and legend
([L99–218](../../public/simulations/phasor-sums.html#L99-L218)); the lecture note
([L221–650](../../public/simulations/phasor-sums.html#L221-L650)); the walkthrough host `#walk`
(`data-walk="phasors"`, [L652](../../public/simulations/phasor-sums.html#L652)); the footer. `datalog.js` adds the data
tab, the *Read values* switch in the caption and the reading strip under `#stage`
([datalog.js:567–590](../../public/scripts/datalog.js#L567-L590)).

Scripts, in load order: `fold.js`, `sim.js`, `dataset.js` ([L660–662](../../public/simulations/phasor-sums.html#L660-L662)), the page script
([L663–1475](../../public/simulations/phasor-sums.html#L663-L1475)), `datalog.js`
([L1476](../../public/simulations/phasor-sums.html#L1476)). `sim.js` loads the walkthrough file named by
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
([L460–530](../../public/simulations/phasor-sums.html#L460-L530)); Figure 5 $|z|^2$ for the Star
([L544–594](../../public/simulations/phasor-sums.html#L544-L594)). Its curves sit in a group ([L574–583](../../public/simulations/phasor-sums.html#L574-L583)) clipped by `f7clipc4`, a rectangle
from x = 64 to 699 ([L547](../../public/simulations/phasor-sums.html#L547)), so the dashed marker of the full period at x = 698, 1.4 units wide
([L579](../../public/simulations/phasor-sums.html#L579)), shows whole.

## Where the drawing and the store differ

The page states this in its `about` paragraph, shown in the data panel
([L1467](../../public/simulations/phasor-sums.html#L1467), [datalog.js:165](../../public/scripts/datalog.js#L165)):

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
  [817–822](../../public/simulations/phasor-sums.html#L817-L822), [830–835](../../public/simulations/phasor-sums.html#L830-L835),
  [846](../../public/simulations/phasor-sums.html#L846), [866–867](../../public/simulations/phasor-sums.html#L866-L867),
  [944–949](../../public/simulations/phasor-sums.html#L944-L949), [1158–1159](../../public/simulations/phasor-sums.html#L1158-L1159),
  [1324–1326](../../public/simulations/phasor-sums.html#L1324-L1326). Change both together; add store taps after a quoted
  line, never inside a quoted run.
- **Formulas live three times.** In the code, in the `formula` string of each `ds.var` declaration, and in `check`.
  `structure()` is repeated as `structureNow()` ([L1362](../../public/simulations/phasor-sums.html#L1362)), `sumAt()` as
  `sumNow()` ([L1363](../../public/simulations/phasor-sums.html#L1363)), the dance multiplier in `check.mul`
  ([L1416–1422](../../public/simulations/phasor-sums.html#L1416-L1422)), the sample count and span in `check.n_path` and
  `check.span` ([L1446–1447](../../public/simulations/phasor-sums.html#L1446-L1447)), the 0.44 scale in
  `check.scale_final` and `check.scale` ([L1452–1453](../../public/simulations/phasor-sums.html#L1452-L1453)).
- **The 0.01 step is load-bearing.** `round(100 ω)` in `structure()` and `activeW()` assumes the ω slider step of 0.01
  ([L971](../../public/simulations/phasor-sums.html#L971)). Changing the step needs a new integer scale in both places
  and in lecture note section 5.
- **Numbers quoted in the note.** Slider ranges (note [L319](../../public/simulations/phasor-sums.html#L319)), sample
  rule and trail default (section 7, [L602–603](../../public/simulations/phasor-sums.html#L602-L603)), morph default
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
   ([L1205](../../public/simulations/phasor-sums.html#L1205)), so a recorded change from 6.2 to 0.1 rad sweeps the arm
   backwards through almost a full turn over about 50 ms.
9. Fixed on 2026-10-15: `computed_in` of `A_arm`, `jx`, `jy`, `px`, `py` reads "draw(), the arm loop" again
   ([L726](../../public/simulations/phasor-sums.html#L726), [L730–733](../../public/simulations/phasor-sums.html#L730-L733)); Batch D ([ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)) had labelled them `sumAt()`, which computes only the angles and
   the steps (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
10. Fixed on 2026-10-15: `phasorRound()` no longer raises Speed to 0.05. At Speed 0 a round is the full figure and recording
    is blocked with its reason in view; for Speed above 0 the round is $\min(T, 20\cdot s_f)$, never more than 20 s of real
    time ([L1366–1369](../../public/simulations/phasor-sums.html#L1366-L1369)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
11. Fixed on 2026-10-15: the clip rectangle `f7clipc4` of note Figure 5 is 1 unit wider (x 64 + 635), so the dashed marker at
    x = 698 is no longer cut in half ([L547](../../public/simulations/phasor-sums.html#L547), [L579](../../public/simulations/phasor-sums.html#L579)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).

## Teaching revision · 15 October 2026

A stationary pen need not make a cusp. The listed-arm common period can exceed the pen period after cancellations; the note explains both. Arm rotations are prescribed kinematics, not uncoupled physical rods. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).
