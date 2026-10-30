# Fig. 7 · Phasor Sums

| | |
|---|---|
| Page | [public/simulations/phasor-sums.html](../../public/simulations/phasor-sums.html) (1 480 lines, 264 053 bytes) |
| Walkthrough | [public/scripts/walk/phasors.js](../../public/scripts/walk/phasors.js) (351 lines, 13 steps, key `phasors`) |
| Thumbnail | [public/images/sims/phasor-sums.webp](../../public/images/sims/phasor-sums.webp) (800 × 500 px, 12.2 kB: the 3-petal rose with its two arms and circles) |
| Catalog entry | [public/scripts/catalog.js#L150](../../public/scripts/catalog.js#L150) (`id: 'phasor-sums'`, `fig: 7`, field `methods`, stage 2) |

Links of the form `[L816]` point into `phasor-sums.html`.

The reader sees a chain of arms on a canvas. Each arm turns at a steady rate about the tip of the one before it,
and the tip of the last arm, the pen, leaves a burgundy trail. One card per arm sets its radius, angular frequency,
phase and "bounce curve" ([L974–987](../../public/simulations/phasor-sums.html#L974-L987)). Ten presets load roses,
beats, a trefoil, a star and Spirograph-like curves ([L670–681](../../public/simulations/phasor-sums.html#L670-L681)).
A *Final shape* view draws the whole closed curve at once and morphs it when a slider moves. An audio file can drive
the radii ("Auto Dance"), and a performance of slider changes can be recorded, replayed and saved as JSON. The page
opens on the 3-petal rose ([L1472](../../public/simulations/phasor-sums.html#L1472)).

## The physics in one picture

Everyday picture: a fairground ride whose cars spin on the ends of a turning arm, Ptolemy's epicycles, a Spirograph,
or the 50 Hz mains voltage drawn as a turning arrow (lecture note section 1,
[L245–251](../../public/simulations/phasor-sums.html#L245-L251)).

Model: each arm has a prescribed angle that increases at constant angular velocity. Placing
an arm on a moving tip adds its arrow to that tip's position, so the pen is a sum of complex numbers (note section 3,
[L316–320](../../public/simulations/phasor-sums.html#L316-L320)). Everything on screen is kinematics.

The equations the code evaluates:

$$x(t) = \sum_{k=1}^{N} A'_k \cos(\omega_k t + \varphi_k), \qquad y(t) = \sum_{k=1}^{N} A'_k \sin(\omega_k t + \varphi_k), \qquad z = x + iy$$

with $A'_k = A_k\, m_k$ ([L818–822](../../public/simulations/phasor-sums.html#L818-L822),
[L950](../../public/simulations/phasor-sums.html#L950)). $A_k$ is the stored radius, a scale-free length (only ratios
matter; the picture is scaled to fit). $\omega_k$ is the angular frequency in rad/s, $\varphi_k$ the phase in rad,
$t$ the phasor time in s. $m_k$ is the dance multiplier, exactly 1 while Auto Dance is off
([L944](../../public/simulations/phasor-sums.html#L944)).

Closure and symmetry use integers $w_k = \mathrm{round}(100\,\omega_k)$ over the arms with $A_k > 0$
([L831](../../public/simulations/phasor-sums.html#L831)):

$$G = \gcd_k w_k, \quad g = G/100\ \mathrm{rad/s}, \quad T = 2\pi/g; \qquad M = \gcd_k (w_k - w_1), \quad q = M/\gcd(w_1, M)$$

([L833–836](../../public/simulations/phasor-sums.html#L833-L836)). $T$ in s is a common repeat time for the listed active arms; cancelling equal-frequency terms can shorten the pen's true period. The integer $q$ describes the listed-arm rotational symmetry. The time average of the squared distance, for distinct
frequencies, is $\langle |z|^2 \rangle = \sum_k A_k^2$ ([L1160](../../public/simulations/phasor-sums.html#L1160)).

The lecture note derives these: Euler's formula (section 2, eqs. 1–5), the model (section 3, eq. 6, velocity eq. 7),
roses and beats (section 4, eqs. 8–11), closure and symmetry (section 5, eqs. 12–13), Parseval (section 6, eqs. 14–15),
morphing as a low-pass filter (section 7.1, eq. 16) and the screen mapping (section 8, eq. 17).

## How the code computes it

**State** ([L705–708](../../public/simulations/phasor-sums.html#L705-L708)). `phasors` holds the stored list, one
object `{ amp, freq, phase, color, curve }` per card. `live` is a per-frame copy with the danced radius. `t` is phasor
time in s. `trail` is the list of past pen positions. `finalPath` holds the exact samples of the closed curve,
`morphPath` the samples as drawn. `fitR` is the radius the Live view is fitted to.

**Method: closed form, no integrator.** The sum is evaluated directly at the current $t$; nothing is integrated, so
no error accumulates from frame to frame (note section 7, [L601](../../public/simulations/phasor-sums.html#L601)).
Each frame costs $N$ cosines and $N$ sines in `sumAt()` ([L814–826](../../public/simulations/phasor-sums.html#L814-L826)),
called twice per frame with the same arguments: once for the new trail point
([L1328](../../public/simulations/phasor-sums.html#L1328)) and once in `draw()`
([L1120](../../public/simulations/phasor-sums.html#L1120)).

Period and symmetry are found exactly because the sliders move in steps of 0.01 rad/s
([L972](../../public/simulations/phasor-sums.html#L972)): $100\,\omega$ is an integer and Euclid's algorithm `gcd()`
([L807–811](../../public/simulations/phasor-sums.html#L807-L811)) works on integers.

**Frame loop**, the `Sim.clock` callback ([L1317–1352](../../public/simulations/phasor-sums.html#L1317-L1352)), in order:

1. `real` = wall time since the last frame, capped at 0.05 s ([L1318](../../public/simulations/phasor-sums.html#L1318)).
   The clock's own `dt` is the same cap but 0 while paused ([sim.js:179–181](../../public/scripts/sim.js#L179-L181)).
2. `analyse(real)`: audio bands, beat detection, burst decay ([L904–937](../../public/simulations/phasor-sums.html#L904-L937)).
3. `perform(real)`: record a snapshot every 50 ms, or replay ([L1185–1215](../../public/simulations/phasor-sums.html#L1185-L1215)).
4. `buildLive()`: copy the list with the dance multipliers ([L940–957](../../public/simulations/phasor-sums.html#L940-L957)).
   This runs even while paused, so with Auto Dance on the arms still breathe when time stands still.
5. Speed: `lastSpeed = speed.value * speedFactor()` ([L1325](../../public/simulations/phasor-sums.html#L1325)).
6. Live view only, and only when `dt > 0`: `t += dt * lastSpeed`, push $z(t)$ onto `trail`, cut the trail to the
   *Trail length* slider ([L1326–1332](../../public/simulations/phasor-sums.html#L1326-L1332)).
7. Final view only: `morphStep()` moves every drawn sample the fraction $\alpha$ toward the exact one
   ([L864–870](../../public/simulations/phasor-sums.html#L864-L870), [L1337](../../public/simulations/phasor-sums.html#L1337)).
   This also runs while paused.
8. `fit(real)`: the fit radius jumps up at once and relaxes down with a time constant of 0.6 s
   ([L1056–1060](../../public/simulations/phasor-sums.html#L1056-L1060)). The target is `reach()`: $\sum |A'_k|$ or the
   farthest trail point, whichever is larger ([L1050–1055](../../public/simulations/phasor-sums.html#L1050-L1055)).
9. Write the frame scalars into the store ([L1339–1343](../../public/simulations/phasor-sums.html#L1339-L1343)), then `draw()`.
10. Every 0.1 s: `readouts()`, and while replaying, `syncList()` and `formula()`
    ([L1345–1350](../../public/simulations/phasor-sums.html#L1345-L1350)). Then `hud()` paints the audio meters.

**Drawing** (`draw()`, [L1083–1154](../../public/simulations/phasor-sums.html#L1083-L1154)). A point $(x, y)$ goes to the
pixel $(c_x + s\,x,\ c_y - s\,y)$ with $(c_x, c_y)$ the canvas centre
([L1078](../../public/simulations/phasor-sums.html#L1078)). In the Live view
$s = 0.44\,\min(w,h)/\max(R_\text{fit}, 0.05)\times\text{zoom}$ ([L1061](../../public/simulations/phasor-sums.html#L1061),
[L1105](../../public/simulations/phasor-sums.html#L1105)). The trail is drawn in 12 chunks with opacity
$0.18 + 0.82\,(c+1)/12$, so 0.25 for the oldest ([L1108–1115](../../public/simulations/phasor-sums.html#L1108-L1115)).
Then each arm: its circle in `T.rose` about the joint it turns on, its arm and a 3 px dot in the card's colour
([L1122–1146](../../public/simulations/phasor-sums.html#L1122-L1146)); the pen is a 5.5 px burgundy dot with a 2 px
outline in the card colour `T.card` (`#fffaf3`; the paper colour is `T.paper`) ([L1147–1153](../../public/simulations/phasor-sums.html#L1147-L1153)). In the Final view the
scale uses the largest $|z|$ of the drawn path instead of $R_\text{fit}$
([L1062–1066](../../public/simulations/phasor-sums.html#L1062-L1066)), and the path is drawn as a 6 px pale-rose band
under a 1.8 px burgundy line ([L1097–1102](../../public/simulations/phasor-sums.html#L1097-L1102)).

**Precomputation.** `refinal(snap)` ([L845–862](../../public/simulations/phasor-sums.html#L845-L862)) samples the closed
curve at $n+1$ times $t_i = i\,T_\text{span}/n$. The span comes from `spanNow()`
([L839–843](../../public/simulations/phasor-sums.html#L839-L843)): with *Draw one full period* on and $g > 0$ it is
$\min(2\pi/g,\ 60\cdot 2\pi)$ s, otherwise the *Span* slider times $2\pi$ s. The sample count is
$n = \max(1500, \min(12000, \mathrm{round}(700\,T_\text{span}/2\pi)))$
([L847](../../public/simulations/phasor-sums.html#L847)). `refinal()` runs on every card edit (through `edited()`,
[L1032–1038](../../public/simulations/phasor-sums.html#L1032-L1038)), on the span controls and on entering the Final view
([L1261](../../public/simulations/phasor-sums.html#L1261)). It snaps `morphPath` to the new curve when asked, when
morphing is off, or when the sample count changed, because then there is nothing to blend
([L855–857](../../public/simulations/phasor-sums.html#L855-L857)). Every edit also resets `t = 0` and clears the trail.

**Audio** (lecture note section 8.1). `ensureAudio()` builds a Web Audio analyser with `fftSize = 2048` and smoothing
0.8 ([L877–884](../../public/simulations/phasor-sums.html#L877-L884)). Bands are averages of byte bins divided by 255:
bass 20–150 Hz, mid 150–4000 Hz, high 4–16 kHz, each smoothed by `e += 0.15 (raw − e)` per frame
([L907–916](../../public/simulations/phasor-sums.html#L907-L916)). A beat is a raw bass level more than 35 % above the
previous frame's, above 0.22, at least 280 ms after the last beat; it sets `burst = 1 + d_burst`, which falls back
linearly over 10 frames, and the tempo is 60 000 over the median of the last 8 intervals in ms
([L918–936](../../public/simulations/phasor-sums.html#L918-L936)). In `buildLive()`, arms with $|\omega|$ at or below
the median of all $|\omega_k|$ get
$m = 1 + \mathrm{ease}(\text{bass})\,d_\text{bass}\,(1 - 0.7\,|\omega|/|\omega|_\text{max})$, faster arms
$m = 1 + \text{high}\cdot d_\text{high}$, and both are multiplied by `burst`
([L946–948](../../public/simulations/phasor-sums.html#L946-L948)). The easing curves are written inline in `EASE`
([L684–698](../../public/simulations/phasor-sums.html#L684-L698)). The mid band speeds up time by
$1 + \text{mid}\cdot d_\text{speed}$ ([L958](../../public/simulations/phasor-sums.html#L958)). The stored $A, \omega,
\varphi$ are never changed by the dance.

**Record and replay** ([L1179–1252](../../public/simulations/phasor-sums.html#L1179-L1252)). A snapshot
`{ t, d, p: [{ a, f, h, c }] }` of the whole list is taken on the first frame at least 50 ms after the last one, since the
counter restarts at 0 ([L1188–1191](../../public/simulations/phasor-sums.html#L1188-L1191)): every third or fourth frame at
60 frames per second, 58 ms apart on average (104 snapshots in 6 s, measured in headless Chromium). Its time is the audio
time, or wall time without audio ([L1180–1183](../../public/simulations/phasor-sums.html#L1180-L1183)). Replay finds the last snapshot not
later than the current time and moves each value the fraction $\min(1, \Delta t/0.05)$ toward it per frame
([L1196–1208](../../public/simulations/phasor-sums.html#L1196-L1208)); if the number of circles differs it reloads the list
outright. Export writes `phasor-performance.json` as `{ v: 1, timeline }`
([L1233–1234](../../public/simulations/phasor-sums.html#L1233-L1234)); import accepts that object or a bare array
([L1247](../../public/simulations/phasor-sums.html#L1247)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `EASE.*` (6 curves) | [684–698](../../public/simulations/phasor-sums.html#L684-L698) | Easing curves for the bass response: Linear, Bounce, Elastic, Back, Sine, Expo. |
| `$` | [700](../../public/simulations/phasor-sums.html#L700) | `document.getElementById`. |
| `wrap` | [800](../../public/simulations/phasor-sums.html#L800) | Angle into $[0, 2\pi)$; applied to every phase that `load()` takes in. |
| `clamp01` | [801](../../public/simulations/phasor-sums.html#L801) | Clamp to $[0, 1]$. |
| `median` | [802–806](../../public/simulations/phasor-sums.html#L802-L806) | Median of an array (beat intervals, $|\omega_k|$). |
| `gcd` | [807–811](../../public/simulations/phasor-sums.html#L807-L811) | Euclid's algorithm on integers. |
| `sumAt` | [814–826](../../public/simulations/phasor-sums.html#L814-L826) | The phasor sum and each arm's $(\Delta x, \Delta y)$ at one time; an optional angles array receives the live angle at its calculation. |
| `structure` | [829–837](../../public/simulations/phasor-sums.html#L829-L837) | $G$, $g$, $M$, $q$ and the active count from `round(100 ω)`. |
| `spanNow` | [839–843](../../public/simulations/phasor-sums.html#L839-L843) | Time span of the Final shape. |
| `refinal` | [845–862](../../public/simulations/phasor-sums.html#L845-L862) | Samples the exact curve, snaps or keeps the morph path, writes `final_*`, `path_*`, `n_path`, `span`, `dev`, `scale_final`. |
| `morphStep` | [864–870](../../public/simulations/phasor-sums.html#L864-L870) | One low-pass step of the drawn path toward the exact one. |
| `ensureAudio` | [877–884](../../public/simulations/phasor-sums.html#L877-L884) | Creates the AudioContext and analyser once. |
| `loadAudio` | [885–897](../../public/simulations/phasor-sums.html#L885-L897) | Plays a chosen file through the analyser (object URL; nothing uploaded). |
| `audioControl` | [898–903](../../public/simulations/phasor-sums.html#L898-L903) | Play, pause, stop. |
| `analyse` (with inner `band`) | [904–937](../../public/simulations/phasor-sums.html#L904-L937) | Band levels, beat detection, BPM, burst and beat-pulse decay. |
| `buildLive` | [940–957](../../public/simulations/phasor-sums.html#L940-L957) | Danced copy `live`; writes the `arm` arrays, `N`, `dance`, `burst`. |
| `speedFactor` | [958](../../public/simulations/phasor-sums.html#L958) | $1 + \text{mid}\cdot d_\text{speed}$ while dancing, else 1. |
| `paintRange` | [966–969](../../public/simulations/phasor-sums.html#L966-L969) | Sets `--p` on a card slider for its filled track. |
| `ctl` | [970–973](../../public/simulations/phasor-sums.html#L970-L973) | HTML for one card slider. |
| `renderList` | [974–987](../../public/simulations/phasor-sums.html#L974-L987) | Rebuilds all cards. |
| `syncList` | [988–997](../../public/simulations/phasor-sums.html#L988-L997) | Moves the card sliders to the list (during replay). |
| `#plist` input / change / click | [998–1017](../../public/simulations/phasor-sums.html#L998-L1017) | Card slider edits, bounce-curve choice, remove a card. |
| `recolour` | [1019](../../public/simulations/phasor-sums.html#L1019) | Colours by position from `COLS`. |
| `formula` | [1020–1030](../../public/simulations/phasor-sums.html#L1020-L1030) | Prints eq. (6) with the stored numbers via `katex.render`, HTML fallback. |
| `typeset` listener | [1031](../../public/simulations/phasor-sums.html#L1031) | Re-renders the formula once KaTeX has loaded. |
| `edited` | [1032–1038](../../public/simulations/phasor-sums.html#L1032-L1038) | After any list change: clear trail, `t = 0`, `refinal`, formula, readouts. |
| `load` | [1039–1045](../../public/simulations/phasor-sums.html#L1039-L1045) | Loads `[A, ω, φ, curve]` triples. |
| `reach` | [1050–1055](../../public/simulations/phasor-sums.html#L1050-L1055) | Outermost point drawn in the Live view. |
| `fit` | [1056–1060](../../public/simulations/phasor-sums.html#L1056-L1060) | Grow-at-once, relax-over-0.6-s fit radius. |
| `baseScale`, `finalScale` | [1061–1066](../../public/simulations/phasor-sums.html#L1061-L1066) | Pixels per unit for the two views. |
| `axes`, `polyline` | [1067–1082](../../public/simulations/phasor-sums.html#L1067-L1082) | Axis lines; a stroked run of points. |
| `draw` | [1083–1154](../../public/simulations/phasor-sums.html#L1083-L1154) | Paints one frame and writes the drawing variables; in the Live view its arm loop ([1122–1124](../../public/simulations/phasor-sums.html#L1122-L1124)) stores each arm's radius, step, partial sum and joint position. |
| `readouts` | [1157–1169](../../public/simulations/phasor-sums.html#L1157-L1169) | Writes `E`, `G`, `g`, `M`, `q`, `n_active`, `period`; fills the readouts and caption. |
| `hud` | [1170–1176](../../public/simulations/phasor-sums.html#L1170-L1176) | Beat dot, BPM, three level meters. |
| `recTime`, `snapshot`, `status`, `perform` | [1180–1215](../../public/simulations/phasor-sums.html#L1180-L1215) | Recording clock, one snapshot, status line, record/replay step. |
| Performance buttons | [1216–1252](../../public/simulations/phasor-sums.html#L1216-L1252) | Record, Stop, Replay, Export JSON, Import JSON. |
| `setMode` | [1255–1263](../../public/simulations/phasor-sums.html#L1255-L1263) | Live or Final view. |
| Other control listeners | [1264–1292](../../public/simulations/phasor-sums.html#L1264-L1292) | View buttons, Clear trail, Add, Randomise, presets, switches, audio file and drop zone. |
| `Sim.live` | [1295–1314](../../public/simulations/phasor-sums.html#L1295-L1314) | Formatted store values for the walkthrough. |
| clock callback | [1317–1352](../../public/simulations/phasor-sums.html#L1317-L1352) | The frame loop above. |
| `pixelAt`, `rgbText`, `lum` | [1356–1358](../../public/simulations/phasor-sums.html#L1356-L1358) | Read one canvas pixel; describe it; its luminance. |
| `isLive`, `trailAt`, `pathAt` | [1359–1361](../../public/simulations/phasor-sums.html#L1359-L1361) | Data-panel helpers from stored values. |
| `activeW`, `structureNow`, `sumNow`, `armInputs` | [1362–1365](../../public/simulations/phasor-sums.html#L1362-L1365) | Recompute from stored inputs, for Check only. |
| `phasorRound` | [1367–1370](../../public/simulations/phasor-sums.html#L1367-L1370) | Length of one recorded round: $T$ at Speed 0, else $\min(T, 20\cdot s_f)$. |
| `Sim.data` hooks | [1371–1469](../../public/simulations/phasor-sums.html#L1371-L1469) | `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `play`, `about`. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Radius A (per card) | generated, `data-f="amp"` | 0–2, step 0.01 | `phasors[i].amp` → `edited(false)` ([L979](../../public/simulations/phasor-sums.html#L979), [L998–1006](../../public/simulations/phasor-sums.html#L998-L1006)) |
| Angular frequency ω (per card) | `data-f="freq"` | −32 to 32 rad/s, step 0.01 | `phasors[i].freq` ([L980](../../public/simulations/phasor-sums.html#L980)) |
| Phase φ (per card) | `data-f="phase"` | 0–6.28 rad, step 0.01 | `phasors[i].phase` ([L981](../../public/simulations/phasor-sums.html#L981)) |
| Bounce curve (per card) | `data-curve` select | Linear (default) … Expo | `phasors[i].curve`, the `EASE` used for the bass ([L1007–1009](../../public/simulations/phasor-sums.html#L1007-L1009)) |
| × on a card | `data-rm` | — | Removes the arm, recolours ([L1010–1017](../../public/simulations/phasor-sums.html#L1010-L1017)) |
| Add circle | `add` | A = 0.5, ω = old N + 1, φ = 0 | [L1267–1271](../../public/simulations/phasor-sums.html#L1267-L1271) |
| Randomise | `random` | 2–6 arms, A 0.15–1.25, ω from a fixed list, φ 0–2π | [L1272–1277](../../public/simulations/phasor-sums.html#L1272-L1277) |
| Live / Final shape | `m-live`, `m-final` | Live | `setMode()` ([L1255–1265](../../public/simulations/phasor-sums.html#L1255-L1265)) |
| Play / Pause | `play` | playing (paused under reduced motion) | `Sim.playButton` ([L1353](../../public/simulations/phasor-sums.html#L1353), [sim.js:177](../../public/scripts/sim.js#L177)) |
| Clear trail | `clear` | — | `trail = []` ([L1266](../../public/simulations/phasor-sums.html#L1266)) |
| Speed | `speed` | 0–4, step 0.01, default 1 | read each frame into `lastSpeed` ([L113](../../public/simulations/phasor-sums.html#L113), [L1325](../../public/simulations/phasor-sums.html#L1325)) |
| Zoom | `zoom` | 0.3–1, default 1 | multiplies both scales ([L117](../../public/simulations/phasor-sums.html#L117), [L1105](../../public/simulations/phasor-sums.html#L1105)) |
| Trail length | `trail` | 100–6000, step 100, default 2400 | trail cut ([L121](../../public/simulations/phasor-sums.html#L121), [L1330–1331](../../public/simulations/phasor-sums.html#L1330-L1331)) |
| Component circles / Tip-to-tail vectors | `sw-circles`, `sw-vectors` | on / on | circle and arm drawing ([L1125](../../public/simulations/phasor-sums.html#L1125), [L1132](../../public/simulations/phasor-sums.html#L1132)) |
| Draw one full period | `sw-auto` | on | `spanNow()`; disables `span` ([L1282](../../public/simulations/phasor-sums.html#L1282)) |
| Span (if not one period) | `span` | 1–24 × 2π s, default 4, disabled | `spanNow()`, `refinal(false)` ([L132](../../public/simulations/phasor-sums.html#L132), [L792](../../public/simulations/phasor-sums.html#L792)) |
| Smooth morphing | `sw-morph` | on | α = slider or 1; change snaps ([L865](../../public/simulations/phasor-sums.html#L865), [L1283](../../public/simulations/phasor-sums.html#L1283)) |
| Morph rate α | `morph` | 0.02–0.35, default 0.08 | `morphStep()` ([L137](../../public/simulations/phasor-sums.html#L137)) |
| Presets | `presets`, `data-preset` | rose3 … flower | `load(PRESETS[...])` ([L1278–1281](../../public/simulations/phasor-sums.html#L1278-L1281)) |
| Audio file / drop zone | `afile`, `drop` | — | `loadAudio()` ([L1285–1289](../../public/simulations/phasor-sums.html#L1285-L1289)) |
| Audio Play / Pause / Stop | `a-play`, `a-pause`, `a-stop` | — | `audioControl()` ([L1290–1292](../../public/simulations/phasor-sums.html#L1290-L1292)) |
| Auto Dance | `dance` | off | `danceOn` ([L1284](../../public/simulations/phasor-sums.html#L1284)) |
| Bass drive / Speed drive / Beat burst / High drive | `d-bass`, `d-speed`, `d-burst`, `d-high` | 0–3, step 0.05; 1.5 / 1 / 0.6 / 0.6 | dance formulas ([L175–187](../../public/simulations/phasor-sums.html#L175-L187)) |
| Record / Stop / Replay / Export / Import | `rec`, `rec-stop`, `rec-play`, `rec-export`, `rec-import` (+ hidden `rec-file`) | — | [L1216–1252](../../public/simulations/phasor-sums.html#L1216-L1252) |

Readouts ([L207–213](../../public/simulations/phasor-sums.html#L207-L213)), filled by `readouts()` every 0.1 s:
`r-n` (circles), `r-z` ($|z|$ with the danced radii, [L1158](../../public/simulations/phasor-sums.html#L1158)),
`r-period` ($2\pi/g$, or "point" when $g = 0$), `r-fold` ("∞ (circle)" for one active arm, else `q`-fold), `r-energy`
($\sum A_k^2$). The caption carries `cap-mode` and `cap-t`.

## What the page writes into the data store

`Sim.dataset({ title: 'Phasor sums', attrs: { figure: 7, page, curves, length_unit } })`
([L711](../../public/simulations/phasor-sums.html#L711)); 73 variables declared at
[L712–787](../../public/simulations/phasor-sums.html#L712-L787) (count measured in headless Chromium). Dims: `arm`
(one per card, resized in `buildLive()` [L953](../../public/simulations/phasor-sums.html#L953) and `draw()`
[L1118](../../public/simulations/phasor-sums.html#L1118)), `path` ($n+1$ samples,
[L858](../../public/simulations/phasor-sums.html#L858)), `trail` ([L1334](../../public/simulations/phasor-sums.html#L1334)).
How `dim`, `var`, `alloc` and `set` work is in [dataset.md](../scripts/dataset.md).

| Group (as in `Sim.data.groups`) | Variables | Written at |
|---|---|---|
| Circles | `N`; `A`, `omega`, `phi`, `curve`, `mul`, `A_live` [arm]; `n_active` | [956](../../public/simulations/phasor-sums.html#L956); [955](../../public/simulations/phasor-sums.html#L955); [1161](../../public/simulations/phasor-sums.html#L1161) |
| The sum z(t) | `t`; `x`, `y`, `absz`, `absz2`; `E` | [1340](../../public/simulations/phasor-sums.html#L1340); [1121](../../public/simulations/phasor-sums.html#L1121) (Live view only); [1161](../../public/simulations/phasor-sums.html#L1161) |
| Arms and joints | `ang` [arm]; `A_arm`, `vx`, `vy`, `jx`, `jy`, `px`, `py` [arm]; `tip_px`, `tip_py` | [819](../../public/simulations/phasor-sums.html#L819), inside `sumAt()`, into the array that `draw()` passes at [1120](../../public/simulations/phasor-sums.html#L1120); [1124](../../public/simulations/phasor-sums.html#L1124), the arm loop of `draw()`; [1121](../../public/simulations/phasor-sums.html#L1121) (Live view only) |
| Structure | `G`, `g`, `period`, `M`, `q` | [1161](../../public/simulations/phasor-sums.html#L1161) |
| Final shape | `n_path`, `span`; `final_x`, `final_y` [path]; `path_x`, `path_y` [path]; `dev`, `scale_final`; `span_slider`, `auto`, `morph_on`, `morph_slider`, `alpha` | [861](../../public/simulations/phasor-sums.html#L861); [860](../../public/simulations/phasor-sums.html#L860); [860](../../public/simulations/phasor-sums.html#L860), [1095](../../public/simulations/phasor-sums.html#L1095); [861](../../public/simulations/phasor-sums.html#L861), [1085](../../public/simulations/phasor-sums.html#L1085), [1096](../../public/simulations/phasor-sums.html#L1096); [1341](../../public/simulations/phasor-sums.html#L1341) |
| Trail | `trail_max`, `trail_len`; `trail_x`, `trail_y` [trail] | [1340](../../public/simulations/phasor-sums.html#L1340); [1336](../../public/simulations/phasor-sums.html#L1336) |
| Dance and audio | `dance`, `burst`; `bass`, `mid`, `high`, `bpm`, `beat`; `d_bass`, `d_speed`, `d_burst`, `d_high` | [956](../../public/simulations/phasor-sums.html#L956); [1321](../../public/simulations/phasor-sums.html#L1321); [1342](../../public/simulations/phasor-sums.html#L1342) |
| Time and drawing | `dt`, `spd`, `sf`, `zoom`; `mode`, `cx`, `cy`, `box_w`, `box_h`; `fitR`, `scale`; `circles`, `vectors`; `fps`, `frames`, `playing` | [1340](../../public/simulations/phasor-sums.html#L1340); [1085](../../public/simulations/phasor-sums.html#L1085); [1106](../../public/simulations/phasor-sums.html#L1106) (Live view only); [1342](../../public/simulations/phasor-sums.html#L1342); [1343](../../public/simulations/phasor-sums.html#L1343) |

Each variable's `computed_in` attribute names that place ([L727–734](../../public/simulations/phasor-sums.html#L727-L734)): `ang` "sumAt(), with the
live-view output array"; `vx`, `vy` "sumAt(), read in draw()", since `sumAt()` computes them and the arm loop stores them;
`A_arm`, `jx`, `jy`, `px`, `py` "draw(), the arm loop", where they are computed.

Measured at load on a 1440 px wide window: `box_w × box_h` = 770 × 601, `scale` = 132.22 px per unit for the 3-petal
rose (`fitR` = 2), `n_path` = 1500, `period` = π s, `q` = 3; on a 390 px window 356 × 356 and 78.32 px per unit.

**One round** (`Sim.data.round`, [L1464–1464](../../public/simulations/phasor-sums.html#L1464-L1464)): the time variable
is `t`; the length is `phasorRound()` ([L1367–1370](../../public/simulations/phasor-sums.html#L1367-L1370)). Let $T = 2\pi/g$ be the time after which the
figure closes ($2\pi$ s when $g = 0$) and $s_f$ the stored speed `sf`. Phasor time runs $s_f$ times as fast as real time, so
for $s_f > 0$ a round is $\min(T, 20\,s_f)$ of phasor time, which never takes more than 20 s of real time. At $s_f = 0$ the
length is the full figure, $T$; phasor time does not run then, so recording is blocked and the Record box says why: "Set
Speed above 0: phasor time does not advance at Speed 0." ([L1466](../../public/simulations/phasor-sums.html#L1466)). It is also blocked in the Final view. The label
says "one full figure" or "part of the figure", with the length ([L1466](../../public/simulations/phasor-sums.html#L1466)). Columns: `x`, `y`, `absz`, `sf`; the
point followed is the pen. If Speed becomes 0 during a round, the panel says why it is waiting; raising Speed resumes the
same round.
How rounds are recorded and saved: [datalog.md](../scripts/datalog.md).

**Data-panel hooks.** `probe` pins the nearest joint, the pen or a trail point within 12 px in the Live view, or a
path point in the Final view ([L1386–1399](../../public/simulations/phasor-sums.html#L1386-L1399)). `check` recomputes
34 variables from stored inputs only ([L1416–1457](../../public/simulations/phasor-sums.html#L1416-L1457)). `drawn`
reads pixels back for `tip_px`, `px`, `path_x`, `trail_x`; each test first requires alpha > 0, then a dark colour
where it expects one ([L1458–1463](../../public/simulations/phasor-sums.html#L1458-L1463)). The file base name is
`fig7-phasor-sums` ([L1372](../../public/simulations/phasor-sums.html#L1372)).

**`Sim.live()`** ([L1295–1314](../../public/simulations/phasor-sums.html#L1295-L1314)) returns formatted strings read
from the store: `t, N, x, y, absz, absz2, E, G, g, Tc, M, q, dt, spd, sf, n, span, alpha, dev, bass, mid, high,
burst, dance`, and for arm 1 `A, w, ph, ang, x1, y1, mul, Ar` ("no circles" when the list is empty). These are the
keys the walkthrough tables use.

## Page structure

Head ([L1–42](../../public/simulations/phasor-sums.html#L1-L42)): `styles/sim.css` (which imports the self-hosted fonts,
KaTeX CSS and `paper.css`, [sim.css:8–9](../../public/styles/sim.css#L8-L9)), `styles/data.css`, `styles/fold.css`, an
inline favicon and an inline `<style>` for the cards, selects, drop zone, meters and formula box
([L15–41](../../public/simulations/phasor-sums.html#L15-L41)). See [styles.md](../styles.md).

Body: the top bar: one span holding the Phyein Usul logo (a link to `../index.html` with
`../images/phyein-usul-mark.svg`, 87 × 48) and "← All simulations" ([L45](../../public/simulations/phasor-sums.html#L45)), then the hand-written Fig. links
1–11 ([L44–60](../../public/simulations/phasor-sums.html#L44-L60));
the head ([L64–68](../../public/simulations/phasor-sums.html#L64-L68)); the figure `#stage` with canvas `#field` and
its caption ([L72–80](../../public/simulations/phasor-sums.html#L72-L80)); the card list `#plist` and formula box
([L82–97](../../public/simulations/phasor-sums.html#L82-L97)); the controls aside with readouts and legend
([L100–219](../../public/simulations/phasor-sums.html#L100-L219)); the lecture note
([L222–651](../../public/simulations/phasor-sums.html#L222-L651)); the walkthrough host `#walk`
(`data-walk="phasors"`, [L653](../../public/simulations/phasor-sums.html#L653)); the footer. `datalog.js` adds the data
tab, the *Read values* switch in the caption and the reading strip under `#stage`
([datalog.js:874–897](../../public/scripts/datalog.js#L874-L897)).

Scripts, in load order: `fold.js`, `sim.js`, `dataset.js` ([L661–663](../../public/simulations/phasor-sums.html#L661-L663)), the page script
([L664–1476](../../public/simulations/phasor-sums.html#L664-L1476)), `datalog.js`
([L1477](../../public/simulations/phasor-sums.html#L1477)). `sim.js` loads the walkthrough file named by
`data-walk` ([sim.js:483–489](../../public/scripts/sim.js#L483-L489)) and typesets the note with KaTeX
([sim.js:418–446](../../public/scripts/sim.js#L418-L446)); see [sim.md](../scripts/sim.md), [walk.md](../scripts/walk.md),
[fold.md](../scripts/fold.md).

Lecture note "Phasor sums: circles riding on circles": 9 sections (`.psec`): 1 Circles riding on circles; 2 A turning
arrow: Euler's formula (2.1, 2.2 ★, 2.3); 3 The model (3.1); 4 Two arms: roses and beats (4.1, 4.2, box "One formula,
two pictures", Exercise 4.1); 5 When the curve closes ★ (5.1, Exercise 5.1); 6 The average size of the curve; 7 How
the page computes it (7.1); 8 From the plane to pixels, and from sound to radii (8.1); 9 What the model leaves out
(9.1 Further reading, 4 references). 17 numbered display equations (counted in the rendered page). Five figures,
all inline SVG: Figure 1 Euler's formula ([L265–306](../../public/simulations/phasor-sums.html#L265-L306)); Figure 2 the
Spirograph preset as a chain ([L322–371](../../public/simulations/phasor-sums.html#L322-L371)); Figure 3 beats
([L395–439](../../public/simulations/phasor-sums.html#L395-L439)); Figure 4 two plates, 3-petal rose and Star
([L461–531](../../public/simulations/phasor-sums.html#L461-L531)); Figure 5 $|z|^2$ for the Star
([L545–595](../../public/simulations/phasor-sums.html#L545-L595)). Its curves sit in a group ([L575–584](../../public/simulations/phasor-sums.html#L575-L584)) clipped by `f7clipc4`, a rectangle
from x = 64 to 699 ([L548](../../public/simulations/phasor-sums.html#L548)), so the dashed marker of the full period at x = 698, 1.4 units wide
([L580](../../public/simulations/phasor-sums.html#L580)), shows whole.

## Where the drawing and the store differ

The page states this in its `about` paragraph, shown in the data panel
([L1468](../../public/simulations/phasor-sums.html#L1468), [datalog.js:229](../../public/scripts/datalog.js#L229)):

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
  [818–823](../../public/simulations/phasor-sums.html#L818-L823), [831–836](../../public/simulations/phasor-sums.html#L831-L836),
  [847](../../public/simulations/phasor-sums.html#L847), [867–868](../../public/simulations/phasor-sums.html#L867-L868),
  [945–950](../../public/simulations/phasor-sums.html#L945-L950), [1159–1160](../../public/simulations/phasor-sums.html#L1159-L1160),
  [1325–1327](../../public/simulations/phasor-sums.html#L1325-L1327). Change both together; add store taps after a quoted
  line, never inside a quoted run.
- **Formulas live three times.** In the code, in the `formula` string of each `ds.var` declaration, and in `check`.
  `structure()` is repeated as `structureNow()` ([L1363](../../public/simulations/phasor-sums.html#L1363)), `sumAt()` as
  `sumNow()` ([L1364](../../public/simulations/phasor-sums.html#L1364)), the dance multiplier in `check.mul`
  ([L1417–1423](../../public/simulations/phasor-sums.html#L1417-L1423)), the sample count and span in `check.n_path` and
  `check.span` ([L1447–1448](../../public/simulations/phasor-sums.html#L1447-L1448)), the 0.44 scale in
  `check.scale_final` and `check.scale` ([L1453–1454](../../public/simulations/phasor-sums.html#L1453-L1454)).
- **The 0.01 step is load-bearing.** `round(100 ω)` in `structure()` and `activeW()` assumes the ω slider step of 0.01
  ([L972](../../public/simulations/phasor-sums.html#L972)). Changing the step needs a new integer scale in both places
  and in lecture note section 5.
- **Numbers quoted in the note.** Slider ranges (note [L320](../../public/simulations/phasor-sums.html#L320)), sample
  rule and trail default (section 7, [L603–604](../../public/simulations/phasor-sums.html#L603-L604)), morph default
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
   ([L1206](../../public/simulations/phasor-sums.html#L1206)), so a recorded change from 6.2 to 0.1 rad sweeps the arm
   backwards through almost a full turn over about 50 ms.
9. Fixed on 2026-10-15: `computed_in` of `A_arm`, `jx`, `jy`, `px`, `py` reads "draw(), the arm loop" again
   ([L727](../../public/simulations/phasor-sums.html#L727), [L731–734](../../public/simulations/phasor-sums.html#L731-L734)); Batch D ([ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)) had labelled them `sumAt()`, which computes only the angles and
   the steps (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
10. Fixed on 2026-10-15: `phasorRound()` no longer raises Speed to 0.05. At Speed 0 a round is the full figure and recording
    is blocked with its reason in view; for Speed above 0 the round is $\min(T, 20\cdot s_f)$, never more than 20 s of real
    time ([L1367–1370](../../public/simulations/phasor-sums.html#L1367-L1370)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
11. Fixed on 2026-10-15: the clip rectangle `f7clipc4` of note Figure 5 is 1 unit wider (x 64 + 635), so the dashed marker at
    x = 698 is no longer cut in half ([L548](../../public/simulations/phasor-sums.html#L548), [L580](../../public/simulations/phasor-sums.html#L580)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).

## Teaching revision · 15 October 2026

A stationary pen need not make a cusp. The listed-arm common period can exceed the pen period after cancellations; the note explains both. Arm rotations are prescribed kinematics, not uncoupled physical rods. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig07/`), the lead made only these changes, each on its existing line, so no line link moved: §2.1: a parenthesis using symbols defined later removed ([L262](../../public/simulations/phasor-sums.html#L262)); §4: the beat length rises and falls at the full difference rate ([L382](../../public/simulations/phasor-sums.html#L382)); §4.1: why odd n gives n petals ([L390](../../public/simulations/phasor-sums.html#L390)); §4.2: why the law of cosines has a plus ([L440](../../public/simulations/phasor-sums.html#L440)); §7.1: blends are not the curves of the in-between settings ([L610](../../public/simulations/phasor-sums.html#L610)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

## Second check round · 20 October 2026

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig07/`), each change on its existing line: §7.1: blends are in-between curves for a change of radius, not for frequency or phase ([L610](../../public/simulations/phasor-sums.html#L610)); §8.1: the beat burst as the code applies it (1 + 0.9 d_burst, ten frames) ([L625](../../public/simulations/phasor-sums.html#L625)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.

## Parameter curves · 30 October 2026

The one global slider, Speed, changes only the pace. The physics is on the circle cards, whose sliders restart the figure
at every step of 0.01. So the page loads [`scripts/curve.js`](../scripts/curve.md) after `dataset.js` ([L663](../../public/simulations/phasor-sums.html#L663)) and gives
it, besides Speed, Circle 2's radius and angular frequency through a wrapper with `live` handlers ([L798](../../public/simulations/phasor-sums.html#L798)): a curve turns
Circle 2 without the restart, time and the trail run on, and turning ω₂ also shifts φ₂ by (ω₂ − ω₂′) t at each step so
that arm 2 does not jump; the running total is stored as `dphi2` and Circle 2's Phase slider shows it. A hand on a card
restarts as before. The curve steps after `perform()` in the clock ([L1322](../../public/simulations/phasor-sums.html#L1322)). Each example presses its preset itself.
Plan and numbers from a research agent; its number scripts rerun by me and reproduce exactly.

| Example | Knob, curve, preset | Numbers |
|---|---|---|
| Trefoil: through the cusps of the deltoid | A₂ 0.25 → 0.75 in 30 s, straight; Trefoil | the pen can stop only where A₁\|ω₁\| = A₂\|ω₂\| (equation 7): at A₂ = 0.50, 15 s in, it draws the three cusps of the deltoid (Wikipedia, "Deltoid curve"); beyond, retrograde loops, the motion epicycles were made for (§1; Wikipedia, "Deferent and epicycle") |
| Tune by beats until they vanish | ω₂ 6 → 5 rad/s in 40 s, straight; Beating pair | \|z\| swells every 2π/\|ω₁ − ω₂\| s (equation 10): 6.3 s, 12.6 s at 5.50, 62.8 s at 5.10; the Period readout (equation 12) jumps, 628 s at 5.99, 12.57 s at 5.50 |
| Unequal arms: the petals let go of the centre | A₂ 1 → 0 in 12 s, minimum jerk; 3-petal rose | the pen stays between \|A₁ − A₂\| and A₁ + A₂ (equation 11): a hole of radius 0.10, 0.50, 0.90 at 3, 6, 9 s; ⟨\|z\|²⟩ = Σ A² 2 → 1 (equation 15); Period 3.14 → 1.57 s |
| Fast forward: the trail turns into chords | speed 0.25 → 4× in 16 s, exponential; 3-petal rose | the trail's chords sag as l²/8r (Wikipedia, "Sagitta (geometry)"): 0.00069, 0.0028, 0.011 at 1×, 2×, 4× at 60 frames a second, 0.09 → 1.5 px on a 1440 px screen (§7) |

New in the store: `zdot`, the pen's speed, `Tb12`, the beat period of circles 1 and 2, and `dphi2` ([L770](../../public/simulations/phasor-sums.html#L770)), with checks;
the round wraps into the rest of a running curve ([L1464](../../public/simulations/phasor-sums.html#L1464)); `about` explains the restart-free turning and the phase shift
([L1468](../../public/simulations/phasor-sums.html#L1468)); `curve.extend(Sim.data)` runs before the first resize ([L1471](../../public/simulations/phasor-sums.html#L1471)). Headless Chromium, English and Arabic:
every example runs, the curve's checks agree with the store, the chart's dot reads back burgundy, no page errors, no
sideways scroll. The walkthrough check finds all 158 quoted lines.
