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
phase and "bounce curve" ([L971–984](../../public/simulations/phasor-sums.html#L971-L984)). Ten presets load roses,
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

with $A'_k = A_k\, m_k$ ([L816–819](../../public/simulations/phasor-sums.html#L816-L819),
[L947](../../public/simulations/phasor-sums.html#L947)). $A_k$ is the stored radius, a scale-free length (only ratios
matter; the picture is scaled to fit). $\omega_k$ is the angular frequency in rad/s, $\varphi_k$ the phase in rad,
$t$ the phasor time in s. $m_k$ is the dance multiplier, exactly 1 while Auto Dance is off
([L941](../../public/simulations/phasor-sums.html#L941)).

Closure and symmetry use integers $w_k = \mathrm{round}(100\,\omega_k)$ over the arms with $A_k > 0$
([L828](../../public/simulations/phasor-sums.html#L828)):

$$G = \gcd_k w_k, \quad g = G/100\ \mathrm{rad/s}, \quad T = 2\pi/g; \qquad M = \gcd_k (w_k - w_1), \quad q = M/\gcd(w_1, M)$$

([L830–833](../../public/simulations/phasor-sums.html#L830-L833)). $T$ in s is the period after which the curve
closes; $q$ is the order of its rotational symmetry. The time average of the squared distance, for distinct
frequencies, is $\langle |z|^2 \rangle = \sum_k A_k^2$ ([L1157](../../public/simulations/phasor-sums.html#L1157)).

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
Each frame costs $N$ cosines and $N$ sines in `sumAt()` ([L812–823](../../public/simulations/phasor-sums.html#L812-L823)),
called twice per frame with the same arguments: once for the new trail point
([L1325](../../public/simulations/phasor-sums.html#L1325)) and once in `draw()`
([L1114](../../public/simulations/phasor-sums.html#L1114)).

Period and symmetry are found exactly because the sliders move in steps of 0.01 rad/s
([L969](../../public/simulations/phasor-sums.html#L969)): $100\,\omega$ is an integer and Euclid's algorithm `gcd()`
([L805–809](../../public/simulations/phasor-sums.html#L805-L809)) works on integers.

**Frame loop**, the `Sim.clock` callback ([L1314–1349](../../public/simulations/phasor-sums.html#L1314-L1349)), in order:

1. `real` = wall time since the last frame, capped at 0.05 s ([L1315](../../public/simulations/phasor-sums.html#L1315)).
   The clock's own `dt` is the same cap but 0 while paused ([sim.js:180–182](../../public/scripts/sim.js#L180-L182)).
2. `analyse(real)`: audio bands, beat detection, burst decay ([L901–934](../../public/simulations/phasor-sums.html#L901-L934)).
3. `perform(real)`: record a snapshot every 50 ms, or replay ([L1182–1212](../../public/simulations/phasor-sums.html#L1182-L1212)).
4. `buildLive()`: copy the list with the dance multipliers ([L937–954](../../public/simulations/phasor-sums.html#L937-L954)).
   This runs even while paused, so with Auto Dance on the arms still breathe when time stands still.
5. Speed: `lastSpeed = speed.value * speedFactor()` ([L1322](../../public/simulations/phasor-sums.html#L1322)).
6. Live view only, and only when `dt > 0`: `t += dt * lastSpeed`, push $z(t)$ onto `trail`, cut the trail to the
   *Trail length* slider ([L1323–1329](../../public/simulations/phasor-sums.html#L1323-L1329)).
7. Final view only: `morphStep()` moves every drawn sample the fraction $\alpha$ toward the exact one
   ([L861–867](../../public/simulations/phasor-sums.html#L861-L867), [L1334](../../public/simulations/phasor-sums.html#L1334)).
   This also runs while paused.
8. `fit(real)`: the fit radius jumps up at once and relaxes down with a time constant of 0.6 s
   ([L1053–1057](../../public/simulations/phasor-sums.html#L1053-L1057)). The target is `reach()`: $\sum |A'_k|$ or the
   farthest trail point, whichever is larger ([L1047–1052](../../public/simulations/phasor-sums.html#L1047-L1052)).
9. Write the frame scalars into the store ([L1336–1340](../../public/simulations/phasor-sums.html#L1336-L1340)), then `draw()`.
10. Every 0.1 s: `readouts()`, and while replaying, `syncList()` and `formula()`
    ([L1342–1347](../../public/simulations/phasor-sums.html#L1342-L1347)). Then `hud()` paints the audio meters.

**Drawing** (`draw()`, [L1080–1151](../../public/simulations/phasor-sums.html#L1080-L1151)). A point $(x, y)$ goes to the
pixel $(c_x + s\,x,\ c_y - s\,y)$ with $(c_x, c_y)$ the canvas centre
([L1075](../../public/simulations/phasor-sums.html#L1075)). In the Live view
$s = 0.44\,\min(w,h)/\max(R_\text{fit}, 0.05)\times\text{zoom}$ ([L1058](../../public/simulations/phasor-sums.html#L1058),
[L1102](../../public/simulations/phasor-sums.html#L1102)). The trail is drawn in 12 chunks with opacity
$0.18 + 0.82\,(c+1)/12$, so 0.25 for the oldest ([L1105–1112](../../public/simulations/phasor-sums.html#L1105-L1112)).
Then each arm: its circle in `T.rose` about the joint it turns on, its arm and a 3 px dot in the card's colour
([L1119–1143](../../public/simulations/phasor-sums.html#L1119-L1143)); the pen is a 5.5 px burgundy dot with a 2 px
outline in the paper colour `T.card` ([L1144–1150](../../public/simulations/phasor-sums.html#L1144-L1150)). In the Final view the
scale uses the largest $|z|$ of the drawn path instead of $R_\text{fit}$
([L1059–1063](../../public/simulations/phasor-sums.html#L1059-L1063)), and the path is drawn as a 6 px pale-rose band
under a 1.8 px burgundy line ([L1094–1099](../../public/simulations/phasor-sums.html#L1094-L1099)).

**Precomputation.** `refinal(snap)` ([L842–859](../../public/simulations/phasor-sums.html#L842-L859)) samples the closed
curve at $n+1$ times $t_i = i\,T_\text{span}/n$. The span comes from `spanNow()`
([L836–840](../../public/simulations/phasor-sums.html#L836-L840)): with *Draw one full period* on and $g > 0$ it is
$\min(2\pi/g,\ 60\cdot 2\pi)$ s, otherwise the *Span* slider times $2\pi$ s. The sample count is
$n = \max(1500, \min(12000, \mathrm{round}(700\,T_\text{span}/2\pi)))$
([L844](../../public/simulations/phasor-sums.html#L844)). `refinal()` runs on every card edit (through `edited()`,
[L1029–1035](../../public/simulations/phasor-sums.html#L1029-L1035)), on the span controls and on entering the Final view
([L1258](../../public/simulations/phasor-sums.html#L1258)). It snaps `morphPath` to the new curve when asked, when
morphing is off, or when the sample count changed, because then there is nothing to blend
([L852–854](../../public/simulations/phasor-sums.html#L852-L854)). Every edit also resets `t = 0` and clears the trail.

**Audio** (lecture note section 8.1). `ensureAudio()` builds a Web Audio analyser with `fftSize = 2048` and smoothing
0.8 ([L874–881](../../public/simulations/phasor-sums.html#L874-L881)). Bands are averages of byte bins divided by 255:
bass 20–150 Hz, mid 150–4000 Hz, high 4–16 kHz, each smoothed by `e += 0.15 (raw − e)` per frame
([L904–913](../../public/simulations/phasor-sums.html#L904-L913)). A beat is a raw bass level more than 35 % above the
previous frame's, above 0.22, at least 280 ms after the last beat; it sets `burst = 1 + d_burst`, which falls back
linearly over 10 frames, and the tempo is 60 000 over the median of the last 8 intervals in ms
([L915–933](../../public/simulations/phasor-sums.html#L915-L933)). In `buildLive()`, arms with $|\omega|$ at or below
the median of all $|\omega_k|$ get
$m = 1 + \mathrm{ease}(\text{bass})\,d_\text{bass}\,(1 - 0.7\,|\omega|/|\omega|_\text{max})$, faster arms
$m = 1 + \text{high}\cdot d_\text{high}$, and both are multiplied by `burst`
([L943–945](../../public/simulations/phasor-sums.html#L943-L945)). The easing curves are written inline in `EASE`
([L682–696](../../public/simulations/phasor-sums.html#L682-L696)). The mid band speeds up time by
$1 + \text{mid}\cdot d_\text{speed}$ ([L955](../../public/simulations/phasor-sums.html#L955)). The stored $A, \omega,
\varphi$ are never changed by the dance.

**Record and replay** ([L1176–1249](../../public/simulations/phasor-sums.html#L1176-L1249)). A snapshot
`{ t, d, p: [{ a, f, h, c }] }` of the whole list is taken every 50 ms against the audio time, or against wall time
without audio ([L1177–1180](../../public/simulations/phasor-sums.html#L1177-L1180)). Replay finds the last snapshot not
later than the current time and moves each value the fraction $\min(1, \Delta t/0.05)$ toward it per frame
([L1193–1205](../../public/simulations/phasor-sums.html#L1193-L1205)); if the number of circles differs it reloads the list
outright. Export writes `phasor-performance.json` as `{ v: 1, timeline }`
([L1230–1231](../../public/simulations/phasor-sums.html#L1230-L1231)); import accepts that object or a bare array
([L1244](../../public/simulations/phasor-sums.html#L1244)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `EASE.*` (6 curves) | [682–696](../../public/simulations/phasor-sums.html#L682-L696) | Easing curves for the bass response: Linear, Bounce, Elastic, Back, Sine, Expo. |
| `$` | [698](../../public/simulations/phasor-sums.html#L698) | `document.getElementById`. |
| `wrap` | [798](../../public/simulations/phasor-sums.html#L798) | Angle into $[0, 2\pi)$; applied to every phase that `load()` takes in. |
| `clamp01` | [799](../../public/simulations/phasor-sums.html#L799) | Clamp to $[0, 1]$. |
| `median` | [800–804](../../public/simulations/phasor-sums.html#L800-L804) | Median of an array (beat intervals, $|\omega_k|$). |
| `gcd` | [805–809](../../public/simulations/phasor-sums.html#L805-L809) | Euclid's algorithm on integers. |
| `sumAt` | [812–823](../../public/simulations/phasor-sums.html#L812-L823) | The phasor sum and each arm's $(\Delta x, \Delta y)$ at one time. |
| `structure` | [826–834](../../public/simulations/phasor-sums.html#L826-L834) | $G$, $g$, $M$, $q$ and the active count from `round(100 ω)`. |
| `spanNow` | [836–840](../../public/simulations/phasor-sums.html#L836-L840) | Time span of the Final shape. |
| `refinal` | [842–859](../../public/simulations/phasor-sums.html#L842-L859) | Samples the exact curve, snaps or keeps the morph path, writes `final_*`, `path_*`, `n_path`, `span`, `dev`, `scale_final`. |
| `morphStep` | [861–867](../../public/simulations/phasor-sums.html#L861-L867) | One low-pass step of the drawn path toward the exact one. |
| `ensureAudio` | [874–881](../../public/simulations/phasor-sums.html#L874-L881) | Creates the AudioContext and analyser once. |
| `loadAudio` | [882–894](../../public/simulations/phasor-sums.html#L882-L894) | Plays a chosen file through the analyser (object URL; nothing uploaded). |
| `audioControl` | [895–900](../../public/simulations/phasor-sums.html#L895-L900) | Play, pause, stop. |
| `analyse` (with inner `band`) | [901–934](../../public/simulations/phasor-sums.html#L901-L934) | Band levels, beat detection, BPM, burst and beat-pulse decay. |
| `buildLive` | [937–954](../../public/simulations/phasor-sums.html#L937-L954) | Danced copy `live`; writes the `arm` arrays, `N`, `dance`, `burst`. |
| `speedFactor` | [955](../../public/simulations/phasor-sums.html#L955) | $1 + \text{mid}\cdot d_\text{speed}$ while dancing, else 1. |
| `paintRange` | [963–966](../../public/simulations/phasor-sums.html#L963-L966) | Sets `--p` on a card slider for its filled track. |
| `ctl` | [967–970](../../public/simulations/phasor-sums.html#L967-L970) | HTML for one card slider. |
| `renderList` | [971–984](../../public/simulations/phasor-sums.html#L971-L984) | Rebuilds all cards. |
| `syncList` | [985–994](../../public/simulations/phasor-sums.html#L985-L994) | Moves the card sliders to the list (during replay). |
| `#plist` input / change / click | [995–1014](../../public/simulations/phasor-sums.html#L995-L1014) | Card slider edits, bounce-curve choice, remove a card. |
| `recolour` | [1016](../../public/simulations/phasor-sums.html#L1016) | Colours by position from `COLS`. |
| `formula` | [1017–1027](../../public/simulations/phasor-sums.html#L1017-L1027) | Prints eq. (6) with the stored numbers via `katex.render`, HTML fallback. |
| `typeset` listener | [1028](../../public/simulations/phasor-sums.html#L1028) | Re-renders the formula once KaTeX has loaded. |
| `edited` | [1029–1035](../../public/simulations/phasor-sums.html#L1029-L1035) | After any list change: clear trail, `t = 0`, `refinal`, formula, readouts. |
| `load` | [1036–1042](../../public/simulations/phasor-sums.html#L1036-L1042) | Loads `[A, ω, φ, curve]` triples. |
| `reach` | [1047–1052](../../public/simulations/phasor-sums.html#L1047-L1052) | Outermost point drawn in the Live view. |
| `fit` | [1053–1057](../../public/simulations/phasor-sums.html#L1053-L1057) | Grow-at-once, relax-over-0.6-s fit radius. |
| `baseScale`, `finalScale` | [1058–1063](../../public/simulations/phasor-sums.html#L1058-L1063) | Pixels per unit for the two views. |
| `axes`, `polyline` | [1064–1079](../../public/simulations/phasor-sums.html#L1064-L1079) | Axis lines; a stroked run of points. |
| `draw` | [1080–1151](../../public/simulations/phasor-sums.html#L1080-L1151) | Paints one frame and writes the drawing variables. |
| `readouts` | [1154–1166](../../public/simulations/phasor-sums.html#L1154-L1166) | Writes `E`, `G`, `g`, `M`, `q`, `n_active`, `period`; fills the readouts and caption. |
| `hud` | [1167–1173](../../public/simulations/phasor-sums.html#L1167-L1173) | Beat dot, BPM, three level meters. |
| `recTime`, `snapshot`, `status`, `perform` | [1177–1212](../../public/simulations/phasor-sums.html#L1177-L1212) | Recording clock, one snapshot, status line, record/replay step. |
| Performance buttons | [1213–1249](../../public/simulations/phasor-sums.html#L1213-L1249) | Record, Stop, Replay, Export JSON, Import JSON. |
| `setMode` | [1252–1260](../../public/simulations/phasor-sums.html#L1252-L1260) | Live or Final view. |
| Other control listeners | [1261–1289](../../public/simulations/phasor-sums.html#L1261-L1289) | View buttons, Clear trail, Add, Randomise, presets, switches, audio file and drop zone. |
| `Sim.live` | [1292–1311](../../public/simulations/phasor-sums.html#L1292-L1311) | Formatted store values for the walkthrough. |
| clock callback | [1314–1349](../../public/simulations/phasor-sums.html#L1314-L1349) | The frame loop above. |
| `pixelAt`, `rgbText`, `lum` | [1353–1355](../../public/simulations/phasor-sums.html#L1353-L1355) | Read one canvas pixel; describe it; its luminance. |
| `isLive`, `trailAt`, `pathAt` | [1356–1358](../../public/simulations/phasor-sums.html#L1356-L1358) | Data-panel helpers from stored values. |
| `activeW`, `structureNow`, `sumNow`, `armInputs` | [1359–1362](../../public/simulations/phasor-sums.html#L1359-L1362) | Recompute from stored inputs, for Check only. |
| `nz` | [1363](../../public/simulations/phasor-sums.html#L1363) | Unused (see notes). |
| `phasorRound` | [1365–1368](../../public/simulations/phasor-sums.html#L1365-L1368) | Length of one recorded round. |
| `Sim.data` hooks | [1369–1467](../../public/simulations/phasor-sums.html#L1369-L1467) | `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `play`, `about`. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Radius A (per card) | generated, `data-f="amp"` | 0–2, step 0.01 | `phasors[i].amp` → `edited(false)` ([L976](../../public/simulations/phasor-sums.html#L976), [L995–1003](../../public/simulations/phasor-sums.html#L995-L1003)) |
| Angular frequency ω (per card) | `data-f="freq"` | −32 to 32 rad/s, step 0.01 | `phasors[i].freq` ([L977](../../public/simulations/phasor-sums.html#L977)) |
| Phase φ (per card) | `data-f="phase"` | 0–6.28 rad, step 0.01 | `phasors[i].phase` ([L978](../../public/simulations/phasor-sums.html#L978)) |
| Bounce curve (per card) | `data-curve` select | Linear (default) … Expo | `phasors[i].curve`, the `EASE` used for the bass ([L1004–1006](../../public/simulations/phasor-sums.html#L1004-L1006)) |
| × on a card | `data-rm` | — | Removes the arm, recolours ([L1007–1014](../../public/simulations/phasor-sums.html#L1007-L1014)) |
| Add circle | `add` | A = 0.5, ω = old N + 1, φ = 0 | [L1264–1268](../../public/simulations/phasor-sums.html#L1264-L1268) |
| Randomise | `random` | 2–6 arms, A 0.15–1.25, ω from a fixed list, φ 0–2π | [L1269–1274](../../public/simulations/phasor-sums.html#L1269-L1274) |
| Live / Final shape | `m-live`, `m-final` | Live | `setMode()` ([L1252–1262](../../public/simulations/phasor-sums.html#L1252-L1262)) |
| Play / Pause | `play` | playing (paused under reduced motion) | `Sim.playButton` ([L1350](../../public/simulations/phasor-sums.html#L1350), [sim.js:178](../../public/scripts/sim.js#L178)) |
| Clear trail | `clear` | — | `trail = []` ([L1263](../../public/simulations/phasor-sums.html#L1263)) |
| Speed | `speed` | 0–4, step 0.01, default 1 | read each frame into `lastSpeed` ([L112](../../public/simulations/phasor-sums.html#L112), [L1322](../../public/simulations/phasor-sums.html#L1322)) |
| Zoom | `zoom` | 0.3–1, default 1 | multiplies both scales ([L116](../../public/simulations/phasor-sums.html#L116), [L1102](../../public/simulations/phasor-sums.html#L1102)) |
| Trail length | `trail` | 100–6000, step 100, default 2400 | trail cut ([L120](../../public/simulations/phasor-sums.html#L120), [L1327–1328](../../public/simulations/phasor-sums.html#L1327-L1328)) |
| Component circles / Tip-to-tail vectors | `sw-circles`, `sw-vectors` | on / on | circle and arm drawing ([L1122](../../public/simulations/phasor-sums.html#L1122), [L1129](../../public/simulations/phasor-sums.html#L1129)) |
| Draw one full period | `sw-auto` | on | `spanNow()`; disables `span` ([L1279](../../public/simulations/phasor-sums.html#L1279)) |
| Span (if not one period) | `span` | 1–24 × 2π s, default 4, disabled | `spanNow()`, `refinal(false)` ([L131](../../public/simulations/phasor-sums.html#L131), [L790](../../public/simulations/phasor-sums.html#L790)) |
| Smooth morphing | `sw-morph` | on | α = slider or 1; change snaps ([L862](../../public/simulations/phasor-sums.html#L862), [L1280](../../public/simulations/phasor-sums.html#L1280)) |
| Morph rate α | `morph` | 0.02–0.35, default 0.08 | `morphStep()` ([L136](../../public/simulations/phasor-sums.html#L136)) |
| Presets | `presets`, `data-preset` | rose3 … flower | `load(PRESETS[...])` ([L1275–1278](../../public/simulations/phasor-sums.html#L1275-L1278)) |
| Audio file / drop zone | `afile`, `drop` | — | `loadAudio()` ([L1282–1286](../../public/simulations/phasor-sums.html#L1282-L1286)) |
| Audio Play / Pause / Stop | `a-play`, `a-pause`, `a-stop` | — | `audioControl()` ([L1287–1289](../../public/simulations/phasor-sums.html#L1287-L1289)) |
| Auto Dance | `dance` | off | `danceOn` ([L1281](../../public/simulations/phasor-sums.html#L1281)) |
| Bass drive / Speed drive / Beat burst / High drive | `d-bass`, `d-speed`, `d-burst`, `d-high` | 0–3, step 0.05; 1.5 / 1 / 0.6 / 0.6 | dance formulas ([L174–186](../../public/simulations/phasor-sums.html#L174-L186)) |
| Record / Stop / Replay / Export / Import | `rec`, `rec-stop`, `rec-play`, `rec-export`, `rec-import` (+ hidden `rec-file`) | — | [L1213–1249](../../public/simulations/phasor-sums.html#L1213-L1249) |

Readouts ([L206–212](../../public/simulations/phasor-sums.html#L206-L212)), filled by `readouts()` every 0.1 s:
`r-n` (circles), `r-z` ($|z|$ with the danced radii, [L1155](../../public/simulations/phasor-sums.html#L1155)),
`r-period` ($2\pi/g$, or "point" when $g = 0$), `r-fold` ("∞ (circle)" for one active arm, else `q`-fold), `r-energy`
($\sum A_k^2$). The caption carries `cap-mode` and `cap-t`.

## What the page writes into the data store

`Sim.dataset({ title: 'Phasor sums', attrs: { figure: 7, page, curves, length_unit } })`
([L709](../../public/simulations/phasor-sums.html#L709)); 73 variables declared at
[L710–785](../../public/simulations/phasor-sums.html#L710-L785) (count measured in headless Chromium). Dims: `arm`
(one per card, resized in `buildLive()` [L950](../../public/simulations/phasor-sums.html#L950) and `draw()`
[L1116](../../public/simulations/phasor-sums.html#L1116)), `path` ($n+1$ samples,
[L855](../../public/simulations/phasor-sums.html#L855)), `trail` ([L1331](../../public/simulations/phasor-sums.html#L1331)).
How `dim`, `var`, `alloc` and `set` work is in [dataset.md](../scripts/dataset.md).

| Group (as in `Sim.data.groups`) | Variables | Written at |
|---|---|---|
| Circles | `N`; `A`, `omega`, `phi`, `curve`, `mul`, `A_live` [arm]; `n_active` | [953](../../public/simulations/phasor-sums.html#L953); [952](../../public/simulations/phasor-sums.html#L952); [1158](../../public/simulations/phasor-sums.html#L1158) |
| The sum z(t) | `t`; `x`, `y`, `absz`, `absz2`; `E` | [1337](../../public/simulations/phasor-sums.html#L1337); [1118](../../public/simulations/phasor-sums.html#L1118) (Live view only); [1158](../../public/simulations/phasor-sums.html#L1158) |
| Arms and joints | `A_arm`, `ang`, `vx`, `vy`, `jx`, `jy`, `px`, `py` [arm]; `tip_px`, `tip_py` | [1121](../../public/simulations/phasor-sums.html#L1121); [1118](../../public/simulations/phasor-sums.html#L1118) (Live view only) |
| Structure | `G`, `g`, `period`, `M`, `q` | [1158](../../public/simulations/phasor-sums.html#L1158) |
| Final shape | `n_path`, `span`; `final_x`, `final_y` [path]; `path_x`, `path_y` [path]; `dev`, `scale_final`; `span_slider`, `auto`, `morph_on`, `morph_slider`, `alpha` | [858](../../public/simulations/phasor-sums.html#L858); [857](../../public/simulations/phasor-sums.html#L857); [857](../../public/simulations/phasor-sums.html#L857), [1092](../../public/simulations/phasor-sums.html#L1092); [858](../../public/simulations/phasor-sums.html#L858), [1082](../../public/simulations/phasor-sums.html#L1082), [1093](../../public/simulations/phasor-sums.html#L1093); [1338](../../public/simulations/phasor-sums.html#L1338) |
| Trail | `trail_max`, `trail_len`; `trail_x`, `trail_y` [trail] | [1337](../../public/simulations/phasor-sums.html#L1337); [1333](../../public/simulations/phasor-sums.html#L1333) |
| Dance and audio | `dance`, `burst`; `bass`, `mid`, `high`, `bpm`, `beat`; `d_bass`, `d_speed`, `d_burst`, `d_high` | [953](../../public/simulations/phasor-sums.html#L953); [1318](../../public/simulations/phasor-sums.html#L1318); [1339](../../public/simulations/phasor-sums.html#L1339) |
| Time and drawing | `dt`, `spd`, `sf`, `zoom`; `mode`, `cx`, `cy`, `box_w`, `box_h`; `fitR`, `scale`; `circles`, `vectors`; `fps`, `frames`, `playing` | [1337](../../public/simulations/phasor-sums.html#L1337); [1082](../../public/simulations/phasor-sums.html#L1082); [1103](../../public/simulations/phasor-sums.html#L1103) (Live view only); [1339](../../public/simulations/phasor-sums.html#L1339); [1340](../../public/simulations/phasor-sums.html#L1340) |

Measured at load on a 1440 px wide window: `box_w × box_h` = 770 × 601, `scale` = 132.22 px per unit for the 3-petal
rose (`fitR` = 2), `n_path` = 1500, `period` = π s, `q` = 3; on a 390 px window 356 × 356 and 78.32 px per unit.

**One round** (`Sim.data.round`, [L1462–1464](../../public/simulations/phasor-sums.html#L1462-L1464)): the time variable
is `t`; the length is `phasorRound()` = $\min(T, 20\cdot s_f)$ of phasor time, with $T = 2\pi/g$ (or $2\pi$ s when
$g = 0$) and $s_f$ the stored speed `sf` floored at 0.05
([L1365–1368](../../public/simulations/phasor-sums.html#L1365-L1368)), so at most about 20 s of real time. Columns:
`x`, `y`, `absz`, `sf`; the point followed is the pen. Recording is blocked in the Final view and at Speed 0, where phasor time does not run. If Speed becomes 0 during a round, the panel says why it is waiting; raising Speed resumes the same round.
How rounds are recorded and saved: [datalog.md](../scripts/datalog.md).

**Data-panel hooks.** `probe` pins the nearest joint, the pen or a trail point within 12 px in the Live view, or a
path point in the Final view ([L1384–1397](../../public/simulations/phasor-sums.html#L1384-L1397)). `check` recomputes
34 variables from stored inputs only ([L1414–1455](../../public/simulations/phasor-sums.html#L1414-L1455)). `drawn`
reads pixels back for `tip_px`, `px`, `path_x`, `trail_x`; each test first requires alpha > 0, then a dark colour
where it expects one ([L1456–1461](../../public/simulations/phasor-sums.html#L1456-L1461)). The file base name is
`fig7-phasor-sums` ([L1370](../../public/simulations/phasor-sums.html#L1370)).

**`Sim.live()`** ([L1292–1311](../../public/simulations/phasor-sums.html#L1292-L1311)) returns formatted strings read
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
([datalog.js:566–589](../../public/scripts/datalog.js#L566-L589)).

Scripts, in load order: `fold.js`, `sim.js`, `dataset.js`, the page script
([L662–1474](../../public/simulations/phasor-sums.html#L662-L1474)), `datalog.js`
([L659–1475](../../public/simulations/phasor-sums.html#L659-L1475)). `sim.js` loads the walkthrough file named by
`data-walk` ([sim.js:479–485](../../public/scripts/sim.js#L479-L485)) and typesets the note with KaTeX
([sim.js:413–441](../../public/scripts/sim.js#L413-L441)); see [sim.md](../scripts/sim.md), [walk.md](../scripts/walk.md),
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
([L543–593](../../public/simulations/phasor-sums.html#L543-L593)).

## Where the drawing and the store differ

The page states this in its `about` paragraph, shown in the data panel
([L1466](../../public/simulations/phasor-sums.html#L1466), [datalog.js:164](../../public/scripts/datalog.js#L164)):

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
  [816–820](../../public/simulations/phasor-sums.html#L816-L820), [828–833](../../public/simulations/phasor-sums.html#L828-L833),
  [844](../../public/simulations/phasor-sums.html#L844), [864–865](../../public/simulations/phasor-sums.html#L864-L865),
  [942–947](../../public/simulations/phasor-sums.html#L942-L947), [1156–1157](../../public/simulations/phasor-sums.html#L1156-L1157),
  [1322–1324](../../public/simulations/phasor-sums.html#L1322-L1324). Change both together; add store taps after a quoted
  line, never inside a quoted run.
- **Formulas live three times.** In the code, in the `formula` string of each `ds.var` declaration, and in `check`.
  `structure()` is repeated as `structureNow()` ([L1360](../../public/simulations/phasor-sums.html#L1360)), `sumAt()` as
  `sumNow()` ([L1361](../../public/simulations/phasor-sums.html#L1361)), the dance multiplier in `check.mul`
  ([L1415–1421](../../public/simulations/phasor-sums.html#L1415-L1421)), the sample count and span in `check.n_path` and
  `check.span` ([L1445–1446](../../public/simulations/phasor-sums.html#L1445-L1446)), the 0.44 scale in
  `check.scale_final` and `check.scale` ([L1451–1452](../../public/simulations/phasor-sums.html#L1451-L1452)).
- **The 0.01 step is load-bearing.** `round(100 ω)` in `structure()` and `activeW()` assumes the ω slider step of 0.01
  ([L969](../../public/simulations/phasor-sums.html#L969)). Changing the step needs a new integer scale in both places
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

1. Fixed on 2026-10-15: all four real SVG clip paths have unique ids; computed clip-path is active, with identical phone pixels and only 28 edge pixels changed on desktop (commit `:/^Batch B: correct notes and layout; verify measured figures in Chromium$`).
2. **Walkthrough says "every 7th sample"** for `dev` ([phasors.js:109](../../public/scripts/walk/phasors.js#L109)); the
   code measures every sample ([L857](../../public/simulations/phasor-sums.html#L857),
   [L1092](../../public/simulations/phasor-sums.html#L1092)).
3. **Walkthrough names `l.mul`** ([phasors.js:127](../../public/scripts/walk/phasors.js#L127)); no `l` exists in the
   page. The value is `live[i].mul` ([L947](../../public/simulations/phasor-sums.html#L947)), stored as `mul`.
4. **`Sim.live().alpha` reads `morph_slider`** ([L1299](../../public/simulations/phasor-sums.html#L1299)), not `alpha`
   ([L1338](../../public/simulations/phasor-sums.html#L1338)). With Smooth morphing off the walkthrough shows the slider
   value while the code uses α = 1 ([L862](../../public/simulations/phasor-sums.html#L862)).
5. **`ang` is not tapped where it is computed.** Its metadata says "sumAt(), read in draw()"
   ([L726](../../public/simulations/phasor-sums.html#L726)), but `sumAt()` keeps its angle local
   ([L816](../../public/simulations/phasor-sums.html#L816)) and `draw()` evaluates `live[i].freq * t + live[i].phase`
   a second time ([L1121](../../public/simulations/phasor-sums.html#L1121)). Same inputs, same value; it is a second
   evaluation rather than a store tap at the computing line.
6. Fixed on 2026-10-15: Speed 0 has an explicit recording guard and waiting reason; a running round resumes after Speed is raised (commit `:/^Batch A: fix simulation and recording faults; verify in Chromium$`).
7. **`nz()` is never called** ([L1363](../../public/simulations/phasor-sums.html#L1363)).
8. **Replay does not wrap phases.** `perform()` moves each phase linearly toward the snapshot
   ([L1203](../../public/simulations/phasor-sums.html#L1203)), so a recorded change from 6.2 to 0.1 rad sweeps the arm
   backwards through almost a full turn over about 50 ms.
