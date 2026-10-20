# Fig. 8 · Draw & Decompose

| | |
|---|---|
| Page | [public/simulations/draw-decompose.html](../../public/simulations/draw-decompose.html) (1 416 lines, 216 511 bytes) |
| Walkthrough | [public/scripts/walk/dft.js](../../public/scripts/walk/dft.js) (key `dft`, 6 steps) |
| Thumbnail | [public/images/sims/draw-decompose.webp](../../public/images/sims/draw-decompose.webp) (800 × 500 px: the heart, its dashed samples and the chain of circles) |
| Catalog entry | [public/scripts/catalog.js#L167](../../public/scripts/catalog.js#L167) (`id: 'draw-decompose'`, `fig: 8`, field `methods`, stage 2) |

Links of the form `[L781]` point into `draw-decompose.html`.

The reader draws one closed stroke on the figure, or picks one of six preset shapes. The page resamples the stroke
at 256 points, takes its discrete Fourier transform, sorts the 120 circles it finds by radius and plays them as a
chain of rotating arms whose last tip redraws the shape. The *Circles K* slider sets how many of the largest circles
are used. A second panel, Fig. 8b, shows the amplitude spectrum, with the circles in use in burgundy. While it plays,
the reader can pan, zoom (slider, wheel or pinch) and follow the pen. Readouts compare the error measured at the
samples with the error predicted by Parseval's theorem. The page opens on the heart
([L1409–1410](../../public/simulations/draw-decompose.html#L1409-L1410)).

## The physics in one picture

Everyday picture: a bead sliding at constant speed along a wire bent into the drawn shape; a music equaliser that
splits a sound into tones; JPEG and MP3, which drop the small components (lecture note section 1,
[L159–164](../../public/simulations/draw-decompose.html#L159-L164)).

Model: the closed curve, traced at constant speed, is a $2\pi$-periodic complex function $z(t)$ of the loop parameter
$t = 2\pi s/L$ (arc length $s$, total length $L$), and so a Fourier series of circles that turn a whole number $k$ of
times per loop (note section 2, [L213–216](../../public/simulations/draw-decompose.html#L213-L216)). This is Fig. 7 run
backwards: the shape is given and the circles follow.

The equations the code evaluates, in order. Lengths are scale-free units (1 unit = 0.46 of the shorter canvas side
while drawing, [L728](../../public/simulations/draw-decompose.html#L728)); $t$ is the loop phase in rad; $T_\text{loop}$ is in s.

1. Arc length of the stroke points $p_j$, $s_i = \sum_{j \le i} |p_j - p_{j-1}|$, $L = s_\text{last}$, spacing
   $\Delta s = L/(N-1)$, and sample $n$ by linear interpolation at distance $n\,\Delta s$, with $N = 256$
   ([L734–750](../../public/simulations/draw-decompose.html#L734-L750)).
2. Centring: $\bar x = \frac1N \sum_n r_{n,x}$, $\bar y$ likewise, $z_n = r_n - (\bar x + i\bar y)$, and
   $\langle |z|^2 \rangle = \frac1N \sum_n |z_n|^2$ ([L785–791](../../public/simulations/draw-decompose.html#L785-L791)).
3. The transform for $k = -60, \dots, 60$, $k \ne 0$, with $z_n = x_n + i y_n$ and $a_n = 2\pi k n/N$ in rad
   ([L755–764](../../public/simulations/draw-decompose.html#L755-L764)):

$$\mathrm{Re}\,c_k = \frac1N \sum_{n=0}^{N-1} \left(x_n \cos a_n + y_n \sin a_n\right), \qquad \mathrm{Im}\,c_k = \frac1N \sum_{n=0}^{N-1} \left(y_n \cos a_n - x_n \sin a_n\right)$$

4. Radius $|c_k|$ and starting angle $\arg c_k = \mathrm{atan2}(\mathrm{Im}, \mathrm{Re})$, then sorting by $|c_k|$,
   largest first ([L765–767](../../public/simulations/draw-decompose.html#L765-L767)).
5. The chain of the first $K$ ranks, and the clock ([L770–780](../../public/simulations/draw-decompose.html#L770-L780),
   [L1276](../../public/simulations/draw-decompose.html#L1276)):

$$z_K(t) = \sum_{\text{rank} < K} |c_k|\, e^{i(kt + \arg c_k)}, \qquad t \leftarrow t + \frac{2\pi\,\Delta t}{T_\text{loop}}$$

6. Parseval and the measured error, with $\tilde z_n = z_K(2\pi n/N)$
   ([L816–826](../../public/simulations/draw-decompose.html#L816-L826)):

$$\text{kept} = \sum_{\text{rank} < K} |c_k|^2, \qquad e_P = \sqrt{\max(0, \langle |z|^2\rangle - \text{kept})}, \qquad e = \sqrt{\frac1N \sum_n |\tilde z_n - z_n|^2}$$

The lecture note derives the series and the coefficient as an average (sections 2–3, eqs. 1–3), the DFT, exact
orthogonality on the samples and aliasing (section 4, eqs. 4–7), Parseval and the error (section 5, eqs. 8–10), the
$1/k$ and $1/k^2$ decay at jumps and corners (section 6, eqs. 11–14), the per-frame sum (section 7, eq. 15) and the
screen scale (section 8, eq. 16).

## How the code computes it

**Constants and state** ([L624–635](../../public/simulations/draw-decompose.html#L624-L635)). `NS = 256` samples,
`KMAX = 60`. `stroke` is the current shape's raw points, `samples` the centred $z_n$, `coefs` the sorted
coefficients `{ k, re, im, amp, phase }`, `full` the 601-point K-term curve. `meanZ2`, `kept`, `err`, `errP` hold the
energies and errors. `t` is the loop phase, `trail` the pen history. `extR` is the outermost radius drawn over a loop,
`viewR` the radius the view is fitted to. `draft` is the stroke being drawn; `zoom`, `panX`, `panY` set the view;
`ptrs` and `pinch` track pointers.

**Method.** A direct DFT, not an FFT: 120 frequencies × 256 samples = 30 720 complex products, done once per shape
([L753–768](../../public/simulations/draw-decompose.html#L753-L768)); the note explains the choice in section 4.3
([L317](../../public/simulations/draw-decompose.html#L317)). Only $|k| \le 60$, below $N/2 = 128$, is computed, so each
coefficient is one true coefficient plus small aliases (note section 4.2). Playback evaluates the chain in closed form,
so there is no integration error and the pen returns to the same place after every loop. Sorting by radius makes the
first $K$ the least-squares best choice of $K$ circles (note box "Keep the largest circles",
[L327–330](../../public/simulations/draw-decompose.html#L327-L330)).

**Once per shape**, `decompose(pts, name)` ([L782–809](../../public/simulations/draw-decompose.html#L782-L809)):
resample with `resamp()`; centre; compute $\langle|z|^2\rangle$; write `stroke_*`, `r_*`, `z_*`, `L`, `step`, `mx`,
`my`, `E`; run `dft()`; write the sorted coefficient arrays; set the K slider's maximum to the number of coefficients
(120) and clamp K; reset `t = 0` and the trail; switch to `mode = 'play'`; call `rebuild()`. Presets enter the same
pipeline as a drawing: `param()` gives 1201 points of a parametric curve
([L854–861](../../public/simulations/draw-decompose.html#L854-L861)), `poly()` 100 points per polygon edge plus the
closing point ([L862–870](../../public/simulations/draw-decompose.html#L862-L870)); the shapes are in `SHAPES`
([L871–891](../../public/simulations/draw-decompose.html#L871-L891)).

**Whenever K changes**, `rebuild()` ([L812–851](../../public/simulations/draw-decompose.html#L812-L851)) computes `kept`,
`errP`, the truncated series at the 256 sample times with the pointwise error `e_i` and `err`, the share `cap`, the
601-point `full` curve at $t = 2\pi i/600$, and `extR`: the larger of the farthest sample and, over 256 phases around
the loop, every circle's centre distance plus its radius
([L836–847](../../public/simulations/draw-decompose.html#L836-L847)). It clears the trail, then calls `readouts()` and
`spectrum()`.

**Frame loop**, the `Sim.clock` callback ([L1270–1288](../../public/simulations/draw-decompose.html#L1270-L1288)), in order:

1. `real` = wall time since the last frame, capped at 0.05 s ([L1271](../../public/simulations/draw-decompose.html#L1271)).
2. `viewR` jumps up to `extR` at once, or relaxes down toward it with a time constant of 0.4 s
   ([L1273–1274](../../public/simulations/draw-decompose.html#L1273-L1274)).
3. Playing and `dt > 0` only: advance `t`, evaluate the chain, push `{ x, y, t }` onto the trail, and drop points older
   than $0.98 \cdot 2\pi$ of phase, so the trail covers just under one loop
   ([L1275–1280](../../public/simulations/draw-decompose.html#L1275-L1280)).
4. Write the trail arrays and the frame scalars ([L1281–1286](../../public/simulations/draw-decompose.html#L1281-L1286)),
   then `draw()`.

`draw()` ([L1048–1194](../../public/simulations/draw-decompose.html#L1048-L1194)) evaluates the chain again at the
same `t` ([L1051](../../public/simulations/draw-decompose.html#L1051)). The scale is $S = 0.46\min(w,h)$ while drawing
([L728](../../public/simulations/draw-decompose.html#L728)) and $S/\max(1, R_\text{view})\times\text{zoom}$ while
playing ([L906](../../public/simulations/draw-decompose.html#L906)). The origin sits at the canvas centre, shifted so
that the pen (Follow the pen) or the pan point is in the middle
([L1052–1056](../../public/simulations/draw-decompose.html#L1052-L1056)). Order of painting: axes with TeX names "Im z",
"Re z" and a "px per unit of z" line ([L1065–1077](../../public/simulations/draw-decompose.html#L1065-L1077)). In
drawing mode: the draft in burgundy, a dashed line from its end back to its start, a ring at the start and a dot at
the end ([L1081–1108](../../public/simulations/draw-decompose.html#L1081-L1108)). While playing: the 256 samples as a
closed dashed ink line, the full curve in pink `#c9707e`, the trail in 24 segments with opacity
$0.12 + 0.88\,(c+1)/24$ ([L1111–1134](../../public/simulations/draw-decompose.html#L1111-L1134)); then each arm in rank
order: its rose circle when the radius exceeds 1.5 px, its arrow in one of four colours `VEC`, dashed for odd ranks
below 12, with a head when longer than 8 px and a rank number for the first 12 when longer than 16 px and the place is
free ([L1140–1176](../../public/simulations/draw-decompose.html#L1140-L1176)); dashed lines from the pen to both axes;
the pen, a 5 px burgundy dot ([L1177–1193](../../public/simulations/draw-decompose.html#L1177-L1193)).

`spectrum()` ([L1196–1239](../../public/simulations/draw-decompose.html#L1196-L1239)) draws Fig. 8b once per rebuild and
on resize: bar $k$ at $x = 18 + (k+60)/120\,(w-36)$, top at $y = b - |c_k|/|c|_\text{max}\,(b-10)$ with base
$b = h - 22$, burgundy for ranks below K, tan otherwise.

**Pointer** ([L902–1005](../../public/simulations/draw-decompose.html#L902-L1005)). While drawing, `world()` maps a
pointer to units with $S$ and the canvas centre ([L902–905](../../public/simulations/draw-decompose.html#L902-L905));
a point is added when it lies more than 0.006 units from the last one
([L956](../../public/simulations/draw-decompose.html#L956)), and *Decompose & play* needs at least 12 points
([L918](../../public/simulations/draw-decompose.html#L918), [L985](../../public/simulations/draw-decompose.html#L985)).
While playing, a drag pans (and turns Follow the pen off, starting the pan at the pen), two pointers pinch-zoom, and
the wheel zooms by $e^{-0.0015\,\Delta y}$ about the cursor, or about the pen while following it ([L959–1005](../../public/simulations/draw-decompose.html#L959-L1005)).
Zoom is clamped to $[1, 10^{1.8}]$ ([L907–910](../../public/simulations/draw-decompose.html#L907-L910)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `$` | [625](../../public/simulations/draw-decompose.html#L625) | `document.getElementById`. |
| `S` | [728](../../public/simulations/draw-decompose.html#L728) | Base scale $0.46\min(w,h)$, px per unit. |
| `resamp` | [734–750](../../public/simulations/draw-decompose.html#L734-L750) | Equal arc-length resampling to N points; sets `arcLen`. |
| `dft` | [753–768](../../public/simulations/draw-decompose.html#L753-L768) | Direct DFT for $-60 \le k \le 60$, $k \ne 0$; sorted by radius. |
| `chainAt` | [770–780](../../public/simulations/draw-decompose.html#L770-L780) | Sum of the first n ranks at loop phase `time`, with each arm's parts. |
| `decompose` | [782–809](../../public/simulations/draw-decompose.html#L782-L809) | The once-per-shape pipeline. |
| `rebuild` | [812–851](../../public/simulations/draw-decompose.html#L812-L851) | Everything that depends on K. |
| `param`, `poly` | [854–870](../../public/simulations/draw-decompose.html#L854-L870) | Points of a parametric curve; points along a polygon. |
| `SHAPES.*` | [871–891](../../public/simulations/draw-decompose.html#L871-L891) | heart, star, square, eight, trefoil, wave. |
| `#presets` click | [893–899](../../public/simulations/draw-decompose.html#L893-L899) | Loads a preset through `play()`. |
| `world` | [902–905](../../public/simulations/draw-decompose.html#L902-L905) | Pointer to drawing units. |
| `viewScale` | [906](../../public/simulations/draw-decompose.html#L906) | Playing scale. |
| `setZoom` | [907–910](../../public/simulations/draw-decompose.html#L907-L910) | Clamped zoom; moves the slider. |
| `setMode` | [911–925](../../public/simulations/draw-decompose.html#L911-L925) | Drawing or playing: tool rows, cursor, hint. |
| `startDraw` | [926–929](../../public/simulations/draw-decompose.html#L926-L929) | Empty draft, drawing mode. |
| `play` | [930–934](../../public/simulations/draw-decompose.html#L930-L934) | Reset pan, decompose, playing mode. |
| canvas `mousedown`, `pointerdown`, `pointermove` | [935–980](../../public/simulations/draw-decompose.html#L935-L980) | Draw, or pan and pinch. |
| `endPointer` (+ `pointerup`, `pointercancel`) | [981–993](../../public/simulations/draw-decompose.html#L981-L993) | End a stroke or a gesture. |
| canvas `wheel` | [994–1005](../../public/simulations/draw-decompose.html#L994-L1005) | Zoom about the cursor. |
| Button and switch listeners | [1006–1023](../../public/simulations/draw-decompose.html#L1006-L1023) | New drawing, Clear, Cancel, Decompose & play, Restart loop, Reset view, Follow the pen. |
| `line` | [1026–1034](../../public/simulations/draw-decompose.html#L1026-L1034) | Strokes a run of points. |
| `labelFree` | [1037–1041](../../public/simulations/draw-decompose.html#L1037-L1041) | Keeps arrow numbers from overlapping. |
| `axisName` | [1042–1047](../../public/simulations/draw-decompose.html#L1042-L1047) | TeX axis label on a pale ground. |
| `draw` | [1048–1194](../../public/simulations/draw-decompose.html#L1048-L1194) | Paints one frame and writes the drawing variables. |
| `spectrum` | [1196–1239](../../public/simulations/draw-decompose.html#L1196-L1239) | Fig. 8b and `spec_x`, `spec_y`, `c_max`. |
| `readouts` | [1241–1251](../../public/simulations/draw-decompose.html#L1241-L1251) | Readouts and captions. |
| `Sim.live` | [1254–1267](../../public/simulations/draw-decompose.html#L1254-L1267) | Formatted store values for the walkthrough. |
| clock callback | [1270–1288](../../public/simulations/draw-decompose.html#L1270-L1288) | The frame loop above. |
| `pixelAt`, `rgbText`, `lum` | [1292–1294](../../public/simulations/draw-decompose.html#L1292-L1294) | Read a pixel of either canvas; describe it; luminance. |
| `playing`, `toScreen` | [1295–1296](../../public/simulations/draw-decompose.html#L1295-L1296) | Data-panel helpers from stored values. |
| `chainNow`, `dftOne`, `nearest`, `armInputs` | [1297–1300](../../public/simulations/draw-decompose.html#L1297-L1300) | Recompute from stored inputs (Check); nearest stored point. |
| `Sim.data` hooks | [1301–1404](../../public/simulations/draw-decompose.html#L1301-L1404) | `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `play`, `about`. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| New drawing | `redraw` | — | `startDraw()` ([L1006](../../public/simulations/draw-decompose.html#L1006)) |
| Decompose & play | `go` | needs ≥ 12 draft points | `play(draft, 'your drawing')`, starts the clock ([L1009–1015](../../public/simulations/draw-decompose.html#L1009-L1015)) |
| Clear | `clear-draft` | — | empties the draft ([L1007](../../public/simulations/draw-decompose.html#L1007)) |
| Cancel | `cancel` | disabled with no shape | back to the current shape ([L1008](../../public/simulations/draw-decompose.html#L1008)) |
| Play / Pause | `play` | playing (paused under reduced motion) | `Sim.playButton` ([L1289](../../public/simulations/draw-decompose.html#L1289), [sim.js:177](../../public/scripts/sim.js#L177)) |
| Restart loop | `reset-t` | — | `t = 0`, trail cleared ([L1016](../../public/simulations/draw-decompose.html#L1016)) |
| Presets | `presets`, `data-shape` | heart (at load) | `SHAPES[s]()` then `play()` ([L893–899](../../public/simulations/draw-decompose.html#L893-L899)) |
| Circles K | `K` | 1–120, step 1, default 24 | `rebuild()` on input ([L100](../../public/simulations/draw-decompose.html#L100), [L722](../../public/simulations/draw-decompose.html#L722)) |
| Time per loop | `loop` | 4–30 s, step 1, default 12 | $T_\text{loop}$ in the clock ([L104](../../public/simulations/draw-decompose.html#L104), [L1276](../../public/simulations/draw-decompose.html#L1276)) |
| Zoom | `zoom` | 0–1.8, step 0.01, default 0 (shown as $10^v$: 1× to 63×) | `zoom = 10^v` ([L108](../../public/simulations/draw-decompose.html#L108), [L726](../../public/simulations/draw-decompose.html#L726)) |
| Follow the pen | `sw-follow` | off | view centre on the pen; turning it off pans to the pen ([L1018–1023](../../public/simulations/draw-decompose.html#L1018-L1023)) |
| Reset view | `reset-view` | — | pan 0, zoom 1, follow off ([L1017](../../public/simulations/draw-decompose.html#L1017)) |
| Component circles / Tip-to-tail vectors / Your drawing / Full K-term curve | `sw-circles`, `sw-vectors`, `sw-orig`, `sw-full` | on / on / on / off | what `draw()` paints ([L1111](../../public/simulations/draw-decompose.html#L1111), [L1118](../../public/simulations/draw-decompose.html#L1118), [L1143](../../public/simulations/draw-decompose.html#L1143), [L1150](../../public/simulations/draw-decompose.html#L1150)) |
| Pointer on the figure | `field` | — | draw (drawing mode); pan, pinch, wheel zoom (playing) |

Readouts ([L120–127](../../public/simulations/draw-decompose.html#L120-L127)), filled by `readouts()`: `r-N` (static
text "256" in the HTML), `r-K` ("K of 120"), `r-cap` (kept share in %), `r-k1` (frequency of the largest circle, with
sign), `r-err`, `r-errp` ([L1241–1251](../../public/simulations/draw-decompose.html#L1241-L1251)). Captions: `cap-mode`,
`cap-src`, `cap-k`.

## What the page writes into the data store

`Sim.dataset({ title: 'Draw and decompose', attrs: { figure: 8, page, NS, KMAX, length_unit } })`
([L638](../../public/simulations/draw-decompose.html#L638)); 74 variables declared at
[L639–719](../../public/simulations/draw-decompose.html#L639-L719) (count measured in headless Chromium). Dims: `stroke`
(raw points), `draft`, `n` (256 samples), `k` (120 coefficients in sorted order, so row $j$ is rank $j$), `full` (601),
`arm` (K), `trail`. See [dataset.md](../scripts/dataset.md).

| Group (as in `Sim.data.groups`) | Variables | Written at |
|---|---|---|
| The stroke | `source`; `mode`, `drawing`; `stroke_x/y` [stroke]; `draft_x/y` [draft]; `N`; `L`, `step`, `mx`, `my`, `E`; `r_x/y`, `z_x/y` [n] | [802](../../public/simulations/draw-decompose.html#L802); [1057](../../public/simulations/draw-decompose.html#L1057); [794](../../public/simulations/draw-decompose.html#L794); [1063](../../public/simulations/draw-decompose.html#L1063); [720](../../public/simulations/draw-decompose.html#L720); [796](../../public/simulations/draw-decompose.html#L796); [795](../../public/simulations/draw-decompose.html#L795) |
| Coefficients | `c_k`, `c_re`, `c_im`, `c_amp`, `c_phase` [k]; `K`, `kept`, `cap`, `errP`, `err`; `zr_x/y`, `e_i` [n]; `full_x/y` [full]; `extR` | [800](../../public/simulations/draw-decompose.html#L800); [826](../../public/simulations/draw-decompose.html#L826); [823](../../public/simulations/draw-decompose.html#L823); [833](../../public/simulations/draw-decompose.html#L833); [847](../../public/simulations/draw-decompose.html#L847) |
| The chain now | `t`, `loop_s`; `A_arm`, `ang`, `vx`, `vy`, `jx`, `jy`, `px`, `py` [arm]; `x`, `y`; `tip_px`, `tip_py` | [1286](../../public/simulations/draw-decompose.html#L1286); [1142](../../public/simulations/draw-decompose.html#L1142); [1059](../../public/simulations/draw-decompose.html#L1059); [1186](../../public/simulations/draw-decompose.html#L1186) |
| Trail | `trail_t`, `trail_x`, `trail_y` [trail] | [1284](../../public/simulations/draw-decompose.html#L1284) |
| Spectrum panel | `c_max`; `spec_x`, `spec_y` [k]; `sbox_w`, `sbox_h` | [1224](../../public/simulations/draw-decompose.html#L1224); [1227](../../public/simulations/draw-decompose.html#L1227); [1198](../../public/simulations/draw-decompose.html#L1198) |
| View and drawing | `viewR`, `dt`, `fps`, `frames`, `playing`; `zoom`, `panX`, `panY`, `follow`, `S_fit`, `scale`, `cx`, `cy`, `box_w`, `box_h`; `circles`, `vectors`, `orig`, `full` | [1286](../../public/simulations/draw-decompose.html#L1286); [1057](../../public/simulations/draw-decompose.html#L1057); [1058](../../public/simulations/draw-decompose.html#L1058) |

`mode`, `t` and `loop_s` are also written once at start-up ([L1405](../../public/simulations/draw-decompose.html#L1405)).
Measured at load on a 1440 px window for the heart: `L` = 5.42763, `E` = 0.515045, and at K = 24 `err` =
0.005405966670666 and `errP` = 0.005405966670687; `extR` = 0.9435, so the scale is $S$ itself, 276.46 px per unit
on a 770 × 601 canvas.

**One round** (`Sim.data.round`, [L1399–1401](../../public/simulations/draw-decompose.html#L1399-L1401)): the time
variable is `t` (rad), the length is $2\pi$, one loop of the circles, which takes `loop_s` seconds; columns `x`, `y`;
the point followed is the pen. Recording is blocked unless a shape is playing. See [datalog.md](../scripts/datalog.md).

**Data-panel hooks.** `probe` ([L1314–1324](../../public/simulations/draw-decompose.html#L1314-L1324)) pins, while
drawing, the nearest draft point within 10 px; while playing, a joint or the pen within 10 px, else (each within 8 px)
a sample if *Your drawing* is on, a point of the full curve if it is on, or a trail point. `check` recomputes 40
variables from stored inputs only, including a fresh one-frequency DFT `dftOne()` for `c_re`, `c_im`
([L1345–1391](../../public/simulations/draw-decompose.html#L1345-L1391)). `drawn` reads pixels back for `tip_px`, `px`,
`full_x`, `trail_x` on the figure and `spec_y` on the spectrum canvas, alpha first
([L1392–1398](../../public/simulations/draw-decompose.html#L1392-L1398)). Read values works on `#stage` only, so the
spectrum panel is not pinnable ([datalog.js:542](../../public/scripts/datalog.js#L542)). While Read values is on,
`datalog.js` stops the canvas's own pointer handlers in the capture phase, so a click pins instead of drawing or panning
([datalog.js:615–638](../../public/scripts/datalog.js#L615-L638)); the wheel is not intercepted. File base name:
`fig8-draw-decompose` ([L1302](../../public/simulations/draw-decompose.html#L1302)).

**`Sim.live()`** ([L1254–1267](../../public/simulations/draw-decompose.html#L1254-L1267)) returns, from the store:
`N, L, ds, mx, my, K, tot, E, kept, cap, err, errP, t, tl, src`, and for rank 0 `k1, re, im, A, ph`, plus the pen
`x, y` and the first centred sample `z0` ("no shape yet" before the first decomposition).

## Page structure

Head ([L1–23](../../public/simulations/draw-decompose.html#L1-L23)): `styles/sim.css` (the self-hosted fonts, KaTeX CSS and
`paper.css` by `@import`, [sim.css:7–9](../../public/styles/sim.css#L7-L9)), `styles/data.css`, `styles/fold.css`, an
inline favicon and a short inline `<style>`: crosshair cursor, `touch-action: none` on the canvas, no text selection on
the stage, the preset grid, the hint, and `[hidden]` forced to `display: none`
([L15–22](../../public/simulations/draw-decompose.html#L15-L22)). See [styles.md](../styles.md).

Body: the top bar: one span holding the Phyein Usul logo (a link to `../index.html` with
`../images/phyein-usul-mark.svg`, 87 × 48) and "← All simulations" ([L26](../../public/simulations/draw-decompose.html#L26)), then the hand-written Fig. links
([L25–40](../../public/simulations/draw-decompose.html#L25-L40)); the
head ([L44–48](../../public/simulations/draw-decompose.html#L44-L48)); Fig. 8a, `#stage` with canvas `#field`, caption
with `#cap-mode`, `#cap-src` ([L52–60](../../public/simulations/draw-decompose.html#L52-L60)); Fig. 8b, `#spec-stage`
with canvas `#spec`, caption with `#cap-k` ([L61–69](../../public/simulations/draw-decompose.html#L61-L69)); the
controls aside: Shape group with hint, `#run-tools`, `#draw-tools` and presets, Reconstruction group, readouts, legend
([L72–133](../../public/simulations/draw-decompose.html#L72-L133)); the lecture note
([L136–608](../../public/simulations/draw-decompose.html#L136-L608)); the walkthrough host `#walk` (`data-walk="dft"`,
[L610](../../public/simulations/draw-decompose.html#L610)); the footer.

Scripts, in load order: `fold.js`, `sim.js`, `dataset.js` ([L618–620](../../public/simulations/draw-decompose.html#L618-L620)), the page script
([L621–1412](../../public/simulations/draw-decompose.html#L621-L1412)), `datalog.js`
([L1413](../../public/simulations/draw-decompose.html#L1413)). `sim.js` fetches `walk/dft.js` from `data-walk`
and typesets the note ([sim.js:339–367](../../public/scripts/sim.js#L339-L367), [sim.js:402–411](../../public/scripts/sim.js#L402-L411));
the canvas labels use `Sim.tex` from `sim.js`. See [sim.md](../scripts/sim.md), [walk.md](../scripts/walk.md),
[fold.md](../scripts/fold.md), [pages.md](../pages.md).

Lecture note "Drawing with circles: the Fourier series of a closed curve": 9 sections: 1 A drawing made of circles;
2 The model; 3 Each circle is an average; 4 From an integral to 256 samples ★ (4.1 orthogonality, 4.2 aliasing, 4.3 the
sum the page computes); 5 Parseval's theorem and the error (box "Keep the largest circles", Exercise 5.1); 6 Corners
cost circles ★ (6.1, 6.2, Exercise 6.1); 7 What the page computes (7.1 Accuracy); 8 From units to pixels; 9 What the
model leaves out (9.1 Further reading, 4 references). 16 numbered display equations (counted in the rendered page).
Five figures, all inline SVG: Figure 1 three circles tip to tail ([L165–208](../../public/simulations/draw-decompose.html#L165-L208));
Figure 2 a raw stroke and its 16-point resampling ([L217–289](../../public/simulations/draw-decompose.html#L217-L289));
Figure 3 relative RMS error against K for heart and square ([L334–380](../../public/simulations/draw-decompose.html#L334-L380));
Figure 4 two plates, heart and square at K = 3, 10, 50 ([L381–473](../../public/simulations/draw-decompose.html#L381-L473));
Figure 5 $|c_k|$ against $|k|$ for four presets ([L494–552](../../public/simulations/draw-decompose.html#L494-L552)).

## Where the drawing and the store differ

The page's `about` paragraph ([L1403](../../public/simulations/draw-decompose.html#L1403)), shown in the data panel
([datalog.js:165](../../public/scripts/datalog.js#L165)), says this; the code adds detail:

- **Dashed original** is the 256 stored samples $z_n$ joined by straight segments and closed
  ([L1115](../../public/simulations/draw-decompose.html#L1115)); the raw stroke `stroke_x/y` is stored but not drawn
  while playing.
- **Full curve** is the stored 601 points joined by straight segments.
- **Trail** is history: the pen at the end of each past frame over just under one loop, faded in 24 segments. Changing K
  clears it ([L848](../../public/simulations/draw-decompose.html#L848)).
- **Small circles are hidden**: a circle under 1.5 px radius is not drawn, an arrow under 8 px gets no head, and only
  the first 12 arrows are numbered, where room allows ([L1143](../../public/simulations/draw-decompose.html#L1143),
  [L1160](../../public/simulations/draw-decompose.html#L1160), [L1168](../../public/simulations/draw-decompose.html#L1168)).
  The store keeps all K arms.
- **View scale** follows `viewR`, which relaxes over 0.4 s; `scale` is a smoothed quantity, not a formula of the
  current frame.
- **Spectrum bars** are normalised to the largest radius and redrawn only on rebuild or resize.

## How to change it safely

- **Walkthrough excerpts.** `dft.js` quotes these page lines verbatim (checked by script):
  [737–738](../../public/simulations/draw-decompose.html#L737-L738), [741](../../public/simulations/draw-decompose.html#L741),
  [759–765](../../public/simulations/draw-decompose.html#L759-L765), [767](../../public/simulations/draw-decompose.html#L767),
  [773–776](../../public/simulations/draw-decompose.html#L773-L776), [787–788](../../public/simulations/draw-decompose.html#L787-L788),
  [791](../../public/simulations/draw-decompose.html#L791), [816–817](../../public/simulations/draw-decompose.html#L816-L817),
  [822](../../public/simulations/draw-decompose.html#L822), [825](../../public/simulations/draw-decompose.html#L825),
  [1276](../../public/simulations/draw-decompose.html#L1276). Change both together; add taps after a quoted line.
- **`NS` is not the only 256.** The static readout `r-N` ([L121](../../public/simulations/draw-decompose.html#L121)) and
  the 256 phases of the `extR` scan ([L838](../../public/simulations/draw-decompose.html#L838),
  [L1369](../../public/simulations/draw-decompose.html#L1369)) are literals, and the note quotes 256 throughout.
- **`KMAX` appears as literals** in the K slider maximum ([L100](../../public/simulations/draw-decompose.html#L100)), the
  spectrum ticks ([L1208](../../public/simulations/draw-decompose.html#L1208)), the Fig. 8b caption
  ([L66](../../public/simulations/draw-decompose.html#L66)) and the `spec_x` formula strings
  ([L697](../../public/simulations/draw-decompose.html#L697), [L1385](../../public/simulations/draw-decompose.html#L1385)).
- **Spectrum geometry** (pad 18, base $h - 22$, top 10) is repeated in `check.spec_x`, `check.spec_y` and the metadata
  ([L1385–1386](../../public/simulations/draw-decompose.html#L1385-L1386), [L697–698](../../public/simulations/draw-decompose.html#L697-L698)).
- **The 0.46 scale** is in `S()`, the dataset attrs, `check.S_fit` and note eq. (16)
  ([L728](../../public/simulations/draw-decompose.html#L728), [L638](../../public/simulations/draw-decompose.html#L638),
  [L1387](../../public/simulations/draw-decompose.html#L1387)).
- **Formulas live twice** for Check: `chainAt()` as `chainNow()`, `dft()` as `dftOne()`, the `extR` scan as
  `check.extR` ([L1297–1298](../../public/simulations/draw-decompose.html#L1297-L1298),
  [L1366–1371](../../public/simulations/draw-decompose.html#L1366-L1371)).
- **Resampling distances** use the local array `arcDistances`; `ds` remains the dataset. The length is calculated in `resamp()` and stored by `decompose()`.
- **Numbers quoted in the note** come from the presets and defaults: square side 1.4, heart $L = 5.428$, default K = 24
  and $T_\text{loop} = 12$ s, the 0.006 drawing threshold, the error values in sections 5–7 and Figures 3–5. Changing a
  preset, NS or KMAX means recomputing them.
- **Re-test**: no console errors in headless Chromium; Heart at K = 24 should still give `err` and `errP` agreeing within
  the 3 parts in $10^{10}$ the note quotes ([L331](../../public/simulations/draw-decompose.html#L331)); run Check on `c_re`, `kept`, `err`, `px`, `spec_y`; draw a stroke with Read values off, then on
  (a click must pin, not draw); record one round.

## Notes for maintainers

1. Fixed on 2026-10-15: the unread touchProbe hook was removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
2. Fixed on 2026-10-15: c_max identifies the largest coefficient at rank 0 rather than the omitted zero-frequency coefficient (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
3. Fixed on 2026-10-15: the walkthrough distinguishes the 120 computed frequencies from a full 256-coefficient DFT; the K = 120 heart residual is 0.000491411444 (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
4. Fixed on 2026-10-15: L and step metadata describe calculation and storage; arcDistances replaces the local name that hid the dataset (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
5. Fixed on 2026-10-15: the thumbnail was retaken from .stage__canvas in Chromium at 1440 × 900, device scale 2, and saved as 800 × 500 WebP (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).


## Teaching revision · 15 October 2026

The note distinguishes continuous coefficients from sampled coefficients, RMS at corresponding samples from nearest-outline distance, and the best K-term fit within the 120 computed components from a full-transform optimum. Wire analogies are stated as sampling approximations. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16: the paragraph "Keep the two meanings separate" had been placed between "normalised by 1/N:" and equation (4), which it cites; it now follows (4) ([L305](../../public/simulations/draw-decompose.html#L305)). See the [audit of the revision](../research-theory-audit.md).

Fixed on 2026-10-16 (second repairs): the RMS sentence reads "it says nothing about the curve between the samples" ([L331](../../public/simulations/draw-decompose.html#L331)). See the [audit of the revision](../research-theory-audit.md).

## Repair round · 20 October 2026

After the independent referee and derivation checks (`notes/fig08/`), the lead made only these changes, each on its existing line, so no line link moved: §5: one sentence recalls the two facts from the ★ Section 4 it uses ([L322](../../public/simulations/draw-decompose.html#L322)). Checked in headless Chromium at 1440 × 900 and 390 × 844: no console or KaTeX errors, no sideways scroll, no display equation wider than its box at 1440 px (`notes/verify.mjs`).

## Second check round · 20 October 2026

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig08/`), each change on its existing line: §4: the samples are spaced L/(N − 1) apart ([L303](../../public/simulations/draw-decompose.html#L303)); §5: the opening sentence corrected (all N coefficients redraw the samples; (5) holds among N neighbouring frequencies) ([L322](../../public/simulations/draw-decompose.html#L322)); Figure 4 caption: fewer circles only down to an error of about 10⁻³ ([L472](../../public/simulations/draw-decompose.html#L472)); §9: moment of inertia per unit mass ([L595](../../public/simulations/draw-decompose.html#L595)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.
