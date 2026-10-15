# Fig. 8 · Draw & Decompose

| | |
|---|---|
| Page | [public/simulations/draw-decompose.html](../../public/simulations/draw-decompose.html) (1 415 lines, 213 105 bytes) |
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
while drawing, [L727](../../public/simulations/draw-decompose.html#L727)); $t$ is the loop phase in rad; $T_\text{loop}$ is in s.

1. Arc length of the stroke points $p_j$, $s_i = \sum_{j \le i} |p_j - p_{j-1}|$, $L = s_\text{last}$, spacing
   $\Delta s = L/(N-1)$, and sample $n$ by linear interpolation at distance $n\,\Delta s$, with $N = 256$
   ([L733–749](../../public/simulations/draw-decompose.html#L733-L749)).
2. Centring: $\bar x = \frac1N \sum_n r_{n,x}$, $\bar y$ likewise, $z_n = r_n - (\bar x + i\bar y)$, and
   $\langle |z|^2 \rangle = \frac1N \sum_n |z_n|^2$ ([L784–790](../../public/simulations/draw-decompose.html#L784-L790)).
3. The transform for $k = -60, \dots, 60$, $k \ne 0$, with $z_n = x_n + i y_n$ and $a_n = 2\pi k n/N$ in rad
   ([L754–763](../../public/simulations/draw-decompose.html#L754-L763)):

$$\mathrm{Re}\,c_k = \frac1N \sum_{n=0}^{N-1} \left(x_n \cos a_n + y_n \sin a_n\right), \qquad \mathrm{Im}\,c_k = \frac1N \sum_{n=0}^{N-1} \left(y_n \cos a_n - x_n \sin a_n\right)$$

4. Radius $|c_k|$ and starting angle $\arg c_k = \mathrm{atan2}(\mathrm{Im}, \mathrm{Re})$, then sorting by $|c_k|$,
   largest first ([L764–766](../../public/simulations/draw-decompose.html#L764-L766)).
5. The chain of the first $K$ ranks, and the clock ([L769–779](../../public/simulations/draw-decompose.html#L769-L779),
   [L1275](../../public/simulations/draw-decompose.html#L1275)):

$$z_K(t) = \sum_{\text{rank} < K} |c_k|\, e^{i(kt + \arg c_k)}, \qquad t \leftarrow t + \frac{2\pi\,\Delta t}{T_\text{loop}}$$

6. Parseval and the measured error, with $\tilde z_n = z_K(2\pi n/N)$
   ([L815–825](../../public/simulations/draw-decompose.html#L815-L825)):

$$\text{kept} = \sum_{\text{rank} < K} |c_k|^2, \qquad e_P = \sqrt{\max(0, \langle |z|^2\rangle - \text{kept})}, \qquad e = \sqrt{\frac1N \sum_n |\tilde z_n - z_n|^2}$$

The lecture note derives the series and the coefficient as an average (sections 2–3, eqs. 1–3), the DFT, exact
orthogonality on the samples and aliasing (section 4, eqs. 4–7), Parseval and the error (section 5, eqs. 8–10), the
$1/k$ and $1/k^2$ decay at jumps and corners (section 6, eqs. 11–14), the per-frame sum (section 7, eq. 15) and the
screen scale (section 8, eq. 16).

## How the code computes it

**Constants and state** ([L623–634](../../public/simulations/draw-decompose.html#L623-L634)). `NS = 256` samples,
`KMAX = 60`. `stroke` is the current shape's raw points, `samples` the centred $z_n$, `coefs` the sorted
coefficients `{ k, re, im, amp, phase }`, `full` the 601-point K-term curve. `meanZ2`, `kept`, `err`, `errP` hold the
energies and errors. `t` is the loop phase, `trail` the pen history. `extR` is the outermost radius drawn over a loop,
`viewR` the radius the view is fitted to. `draft` is the stroke being drawn; `zoom`, `panX`, `panY` set the view;
`ptrs` and `pinch` track pointers.

**Method.** A direct DFT, not an FFT: 120 frequencies × 256 samples = 30 720 complex products, done once per shape
([L752–767](../../public/simulations/draw-decompose.html#L752-L767)); the note explains the choice in section 4.3
([L316](../../public/simulations/draw-decompose.html#L316)). Only $|k| \le 60$, below $N/2 = 128$, is computed, so each
coefficient is one true coefficient plus small aliases (note section 4.2). Playback evaluates the chain in closed form,
so there is no integration error and the pen returns to the same place after every loop. Sorting by radius makes the
first $K$ the least-squares best choice of $K$ circles (note box "Keep the largest circles",
[L326–329](../../public/simulations/draw-decompose.html#L326-L329)).

**Once per shape**, `decompose(pts, name)` ([L781–808](../../public/simulations/draw-decompose.html#L781-L808)):
resample with `resamp()`; centre; compute $\langle|z|^2\rangle$; write `stroke_*`, `r_*`, `z_*`, `L`, `step`, `mx`,
`my`, `E`; run `dft()`; write the sorted coefficient arrays; set the K slider's maximum to the number of coefficients
(120) and clamp K; reset `t = 0` and the trail; switch to `mode = 'play'`; call `rebuild()`. Presets enter the same
pipeline as a drawing: `param()` gives 1201 points of a parametric curve
([L853–860](../../public/simulations/draw-decompose.html#L853-L860)), `poly()` 100 points per polygon edge plus the
closing point ([L861–869](../../public/simulations/draw-decompose.html#L861-L869)); the shapes are in `SHAPES`
([L870–890](../../public/simulations/draw-decompose.html#L870-L890)).

**Whenever K changes**, `rebuild()` ([L811–850](../../public/simulations/draw-decompose.html#L811-L850)) computes `kept`,
`errP`, the truncated series at the 256 sample times with the pointwise error `e_i` and `err`, the share `cap`, the
601-point `full` curve at $t = 2\pi i/600$, and `extR`: the larger of the farthest sample and, over 256 phases around
the loop, every circle's centre distance plus its radius
([L835–846](../../public/simulations/draw-decompose.html#L835-L846)). It clears the trail, then calls `readouts()` and
`spectrum()`.

**Frame loop**, the `Sim.clock` callback ([L1269–1287](../../public/simulations/draw-decompose.html#L1269-L1287)), in order:

1. `real` = wall time since the last frame, capped at 0.05 s ([L1270](../../public/simulations/draw-decompose.html#L1270)).
2. `viewR` jumps up to `extR` at once, or relaxes down toward it with a time constant of 0.4 s
   ([L1272–1273](../../public/simulations/draw-decompose.html#L1272-L1273)).
3. Playing and `dt > 0` only: advance `t`, evaluate the chain, push `{ x, y, t }` onto the trail, and drop points older
   than $0.98 \cdot 2\pi$ of phase, so the trail covers just under one loop
   ([L1274–1279](../../public/simulations/draw-decompose.html#L1274-L1279)).
4. Write the trail arrays and the frame scalars ([L1280–1285](../../public/simulations/draw-decompose.html#L1280-L1285)),
   then `draw()`.

`draw()` ([L1047–1193](../../public/simulations/draw-decompose.html#L1047-L1193)) evaluates the chain again at the
same `t` ([L1050](../../public/simulations/draw-decompose.html#L1050)). The scale is $S = 0.46\min(w,h)$ while drawing
([L727](../../public/simulations/draw-decompose.html#L727)) and $S/\max(1, R_\text{view})\times\text{zoom}$ while
playing ([L905](../../public/simulations/draw-decompose.html#L905)). The origin sits at the canvas centre, shifted so
that the pen (Follow the pen) or the pan point is in the middle
([L1051–1055](../../public/simulations/draw-decompose.html#L1051-L1055)). Order of painting: axes with TeX names "Im z",
"Re z" and a "px per unit of z" line ([L1064–1076](../../public/simulations/draw-decompose.html#L1064-L1076)). In
drawing mode: the draft in burgundy, a dashed line from its end back to its start, a ring at the start and a dot at
the end ([L1080–1107](../../public/simulations/draw-decompose.html#L1080-L1107)). While playing: the 256 samples as a
closed dashed ink line, the full curve in pink `#c9707e`, the trail in 24 segments with opacity
$0.12 + 0.88\,(c+1)/24$ ([L1110–1133](../../public/simulations/draw-decompose.html#L1110-L1133)); then each arm in rank
order: its rose circle when the radius exceeds 1.5 px, its arrow in one of four colours `VEC`, dashed for odd ranks
below 12, with a head when longer than 8 px and a rank number for the first 12 when longer than 16 px and the place is
free ([L1139–1175](../../public/simulations/draw-decompose.html#L1139-L1175)); dashed lines from the pen to both axes;
the pen, a 5 px burgundy dot ([L1176–1192](../../public/simulations/draw-decompose.html#L1176-L1192)).

`spectrum()` ([L1195–1238](../../public/simulations/draw-decompose.html#L1195-L1238)) draws Fig. 8b once per rebuild and
on resize: bar $k$ at $x = 18 + (k+60)/120\,(w-36)$, top at $y = b - |c_k|/|c|_\text{max}\,(b-10)$ with base
$b = h - 22$, burgundy for ranks below K, tan otherwise.

**Pointer** ([L901–1004](../../public/simulations/draw-decompose.html#L901-L1004)). While drawing, `world()` maps a
pointer to units with $S$ and the canvas centre ([L901–904](../../public/simulations/draw-decompose.html#L901-L904));
a point is added when it lies more than 0.006 units from the last one
([L955](../../public/simulations/draw-decompose.html#L955)), and *Decompose & play* needs at least 12 points
([L917](../../public/simulations/draw-decompose.html#L917), [L984](../../public/simulations/draw-decompose.html#L984)).
While playing, a drag pans (and turns Follow the pen off, starting the pan at the pen), two pointers pinch-zoom, and
the wheel zooms by $e^{-0.0015\,\Delta y}$ about the cursor, or about the pen while following it ([L958–1004](../../public/simulations/draw-decompose.html#L958-L1004)).
Zoom is clamped to $[1, 10^{1.8}]$ ([L906–909](../../public/simulations/draw-decompose.html#L906-L909)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `$` | [624](../../public/simulations/draw-decompose.html#L624) | `document.getElementById`. |
| `S` | [727](../../public/simulations/draw-decompose.html#L727) | Base scale $0.46\min(w,h)$, px per unit. |
| `resamp` | [733–749](../../public/simulations/draw-decompose.html#L733-L749) | Equal arc-length resampling to N points; sets `arcLen`. |
| `dft` | [752–767](../../public/simulations/draw-decompose.html#L752-L767) | Direct DFT for $-60 \le k \le 60$, $k \ne 0$; sorted by radius. |
| `chainAt` | [769–779](../../public/simulations/draw-decompose.html#L769-L779) | Sum of the first n ranks at loop phase `time`, with each arm's parts. |
| `decompose` | [781–808](../../public/simulations/draw-decompose.html#L781-L808) | The once-per-shape pipeline. |
| `rebuild` | [811–850](../../public/simulations/draw-decompose.html#L811-L850) | Everything that depends on K. |
| `param`, `poly` | [853–869](../../public/simulations/draw-decompose.html#L853-L869) | Points of a parametric curve; points along a polygon. |
| `SHAPES.*` | [870–890](../../public/simulations/draw-decompose.html#L870-L890) | heart, star, square, eight, trefoil, wave. |
| `#presets` click | [892–898](../../public/simulations/draw-decompose.html#L892-L898) | Loads a preset through `play()`. |
| `world` | [901–904](../../public/simulations/draw-decompose.html#L901-L904) | Pointer to drawing units. |
| `viewScale` | [905](../../public/simulations/draw-decompose.html#L905) | Playing scale. |
| `setZoom` | [906–909](../../public/simulations/draw-decompose.html#L906-L909) | Clamped zoom; moves the slider. |
| `setMode` | [910–924](../../public/simulations/draw-decompose.html#L910-L924) | Drawing or playing: tool rows, cursor, hint. |
| `startDraw` | [925–928](../../public/simulations/draw-decompose.html#L925-L928) | Empty draft, drawing mode. |
| `play` | [929–933](../../public/simulations/draw-decompose.html#L929-L933) | Reset pan, decompose, playing mode. |
| canvas `mousedown`, `pointerdown`, `pointermove` | [934–979](../../public/simulations/draw-decompose.html#L934-L979) | Draw, or pan and pinch. |
| `endPointer` (+ `pointerup`, `pointercancel`) | [980–992](../../public/simulations/draw-decompose.html#L980-L992) | End a stroke or a gesture. |
| canvas `wheel` | [993–1004](../../public/simulations/draw-decompose.html#L993-L1004) | Zoom about the cursor. |
| Button and switch listeners | [1005–1022](../../public/simulations/draw-decompose.html#L1005-L1022) | New drawing, Clear, Cancel, Decompose & play, Restart loop, Reset view, Follow the pen. |
| `line` | [1025–1033](../../public/simulations/draw-decompose.html#L1025-L1033) | Strokes a run of points. |
| `labelFree` | [1036–1040](../../public/simulations/draw-decompose.html#L1036-L1040) | Keeps arrow numbers from overlapping. |
| `axisName` | [1041–1046](../../public/simulations/draw-decompose.html#L1041-L1046) | TeX axis label on a pale ground. |
| `draw` | [1047–1193](../../public/simulations/draw-decompose.html#L1047-L1193) | Paints one frame and writes the drawing variables. |
| `spectrum` | [1195–1238](../../public/simulations/draw-decompose.html#L1195-L1238) | Fig. 8b and `spec_x`, `spec_y`, `c_max`. |
| `readouts` | [1240–1250](../../public/simulations/draw-decompose.html#L1240-L1250) | Readouts and captions. |
| `Sim.live` | [1253–1266](../../public/simulations/draw-decompose.html#L1253-L1266) | Formatted store values for the walkthrough. |
| clock callback | [1269–1287](../../public/simulations/draw-decompose.html#L1269-L1287) | The frame loop above. |
| `pixelAt`, `rgbText`, `lum` | [1291–1293](../../public/simulations/draw-decompose.html#L1291-L1293) | Read a pixel of either canvas; describe it; luminance. |
| `playing`, `toScreen` | [1294–1295](../../public/simulations/draw-decompose.html#L1294-L1295) | Data-panel helpers from stored values. |
| `chainNow`, `dftOne`, `nearest`, `armInputs` | [1296–1299](../../public/simulations/draw-decompose.html#L1296-L1299) | Recompute from stored inputs (Check); nearest stored point. |
| `Sim.data` hooks | [1300–1404](../../public/simulations/draw-decompose.html#L1300-L1404) | `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `play`, `touchProbe`, `about`. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| New drawing | `redraw` | — | `startDraw()` ([L1005](../../public/simulations/draw-decompose.html#L1005)) |
| Decompose & play | `go` | needs ≥ 12 draft points | `play(draft, 'your drawing')`, starts the clock ([L1008–1014](../../public/simulations/draw-decompose.html#L1008-L1014)) |
| Clear | `clear-draft` | — | empties the draft ([L1006](../../public/simulations/draw-decompose.html#L1006)) |
| Cancel | `cancel` | disabled with no shape | back to the current shape ([L1007](../../public/simulations/draw-decompose.html#L1007)) |
| Play / Pause | `play` | playing (paused under reduced motion) | `Sim.playButton` ([L1288](../../public/simulations/draw-decompose.html#L1288), [sim.js:178](../../public/scripts/sim.js#L178)) |
| Restart loop | `reset-t` | — | `t = 0`, trail cleared ([L1015](../../public/simulations/draw-decompose.html#L1015)) |
| Presets | `presets`, `data-shape` | heart (at load) | `SHAPES[s]()` then `play()` ([L892–898](../../public/simulations/draw-decompose.html#L892-L898)) |
| Circles K | `K` | 1–120, step 1, default 24 | `rebuild()` on input ([L100](../../public/simulations/draw-decompose.html#L100), [L721](../../public/simulations/draw-decompose.html#L721)) |
| Time per loop | `loop` | 4–30 s, step 1, default 12 | $T_\text{loop}$ in the clock ([L104](../../public/simulations/draw-decompose.html#L104), [L1275](../../public/simulations/draw-decompose.html#L1275)) |
| Zoom | `zoom` | 0–1.8, step 0.01, default 0 (shown as $10^v$: 1× to 63×) | `zoom = 10^v` ([L108](../../public/simulations/draw-decompose.html#L108), [L725](../../public/simulations/draw-decompose.html#L725)) |
| Follow the pen | `sw-follow` | off | view centre on the pen; turning it off pans to the pen ([L1017–1022](../../public/simulations/draw-decompose.html#L1017-L1022)) |
| Reset view | `reset-view` | — | pan 0, zoom 1, follow off ([L1016](../../public/simulations/draw-decompose.html#L1016)) |
| Component circles / Tip-to-tail vectors / Your drawing / Full K-term curve | `sw-circles`, `sw-vectors`, `sw-orig`, `sw-full` | on / on / on / off | what `draw()` paints ([L1110](../../public/simulations/draw-decompose.html#L1110), [L1117](../../public/simulations/draw-decompose.html#L1117), [L1142](../../public/simulations/draw-decompose.html#L1142), [L1149](../../public/simulations/draw-decompose.html#L1149)) |
| Pointer on the figure | `field` | — | draw (drawing mode); pan, pinch, wheel zoom (playing) |

Readouts ([L120–127](../../public/simulations/draw-decompose.html#L120-L127)), filled by `readouts()`: `r-N` (static
text "256" in the HTML), `r-K` ("K of 120"), `r-cap` (kept share in %), `r-k1` (frequency of the largest circle, with
sign), `r-err`, `r-errp` ([L1240–1250](../../public/simulations/draw-decompose.html#L1240-L1250)). Captions: `cap-mode`,
`cap-src`, `cap-k`.

## What the page writes into the data store

`Sim.dataset({ title: 'Draw and decompose', attrs: { figure: 8, page, NS, KMAX, length_unit } })`
([L637](../../public/simulations/draw-decompose.html#L637)); 74 variables declared at
[L638–718](../../public/simulations/draw-decompose.html#L638-L718) (count measured in headless Chromium). Dims: `stroke`
(raw points), `draft`, `n` (256 samples), `k` (120 coefficients in sorted order, so row $j$ is rank $j$), `full` (601),
`arm` (K), `trail`. See [dataset.md](../scripts/dataset.md).

| Group (as in `Sim.data.groups`) | Variables | Written at |
|---|---|---|
| The stroke | `source`; `mode`, `drawing`; `stroke_x/y` [stroke]; `draft_x/y` [draft]; `N`; `L`, `step`, `mx`, `my`, `E`; `r_x/y`, `z_x/y` [n] | [801](../../public/simulations/draw-decompose.html#L801); [1056](../../public/simulations/draw-decompose.html#L1056); [793](../../public/simulations/draw-decompose.html#L793); [1062](../../public/simulations/draw-decompose.html#L1062); [719](../../public/simulations/draw-decompose.html#L719); [795](../../public/simulations/draw-decompose.html#L795); [794](../../public/simulations/draw-decompose.html#L794) |
| Coefficients | `c_k`, `c_re`, `c_im`, `c_amp`, `c_phase` [k]; `K`, `kept`, `cap`, `errP`, `err`; `zr_x/y`, `e_i` [n]; `full_x/y` [full]; `extR` | [799](../../public/simulations/draw-decompose.html#L799); [825](../../public/simulations/draw-decompose.html#L825); [822](../../public/simulations/draw-decompose.html#L822); [832](../../public/simulations/draw-decompose.html#L832); [846](../../public/simulations/draw-decompose.html#L846) |
| The chain now | `t`, `loop_s`; `A_arm`, `ang`, `vx`, `vy`, `jx`, `jy`, `px`, `py` [arm]; `x`, `y`; `tip_px`, `tip_py` | [1285](../../public/simulations/draw-decompose.html#L1285); [1141](../../public/simulations/draw-decompose.html#L1141); [1058](../../public/simulations/draw-decompose.html#L1058); [1185](../../public/simulations/draw-decompose.html#L1185) |
| Trail | `trail_t`, `trail_x`, `trail_y` [trail] | [1283](../../public/simulations/draw-decompose.html#L1283) |
| Spectrum panel | `c_max`; `spec_x`, `spec_y` [k]; `sbox_w`, `sbox_h` | [1223](../../public/simulations/draw-decompose.html#L1223); [1226](../../public/simulations/draw-decompose.html#L1226); [1197](../../public/simulations/draw-decompose.html#L1197) |
| View and drawing | `viewR`, `dt`, `fps`, `frames`, `playing`; `zoom`, `panX`, `panY`, `follow`, `S_fit`, `scale`, `cx`, `cy`, `box_w`, `box_h`; `circles`, `vectors`, `orig`, `full` | [1285](../../public/simulations/draw-decompose.html#L1285); [1056](../../public/simulations/draw-decompose.html#L1056); [1057](../../public/simulations/draw-decompose.html#L1057) |

`mode`, `t` and `loop_s` are also written once at start-up ([L1405](../../public/simulations/draw-decompose.html#L1405)).
Measured at load on a 1440 px window for the heart: `L` = 5.42763, `E` = 0.515045, and at K = 24 `err` =
0.005405966670666 and `errP` = 0.005405966670687; `extR` = 0.9435, so the scale is $S$ itself, 276.46 px per unit
on a 770 × 601 canvas.

**One round** (`Sim.data.round`, [L1398–1400](../../public/simulations/draw-decompose.html#L1398-L1400)): the time
variable is `t` (rad), the length is $2\pi$, one loop of the circles, which takes `loop_s` seconds; columns `x`, `y`;
the point followed is the pen. Recording is blocked unless a shape is playing. See [datalog.md](../scripts/datalog.md).

**Data-panel hooks.** `probe` ([L1313–1323](../../public/simulations/draw-decompose.html#L1313-L1323)) pins, while
drawing, the nearest draft point within 10 px; while playing, a joint or the pen within 10 px, else (each within 8 px)
a sample if *Your drawing* is on, a point of the full curve if it is on, or a trail point. `check` recomputes 40
variables from stored inputs only, including a fresh one-frequency DFT `dftOne()` for `c_re`, `c_im`
([L1344–1390](../../public/simulations/draw-decompose.html#L1344-L1390)). `drawn` reads pixels back for `tip_px`, `px`,
`full_x`, `trail_x` on the figure and `spec_y` on the spectrum canvas, alpha first
([L1391–1397](../../public/simulations/draw-decompose.html#L1391-L1397)). Read values works on `#stage` only, so the
spectrum panel is not pinnable ([datalog.js:541](../../public/scripts/datalog.js#L541)). While Read values is on,
`datalog.js` stops the canvas's own pointer handlers in the capture phase, so a click pins instead of drawing or panning
([datalog.js:614–637](../../public/scripts/datalog.js#L614-L637)); the wheel is not intercepted. File base name:
`fig8-draw-decompose` ([L1301](../../public/simulations/draw-decompose.html#L1301)).

**`Sim.live()`** ([L1253–1266](../../public/simulations/draw-decompose.html#L1253-L1266)) returns, from the store:
`N, L, ds, mx, my, K, tot, E, kept, cap, err, errP, t, tl, src`, and for rank 0 `k1, re, im, A, ph`, plus the pen
`x, y` and the first centred sample `z0` ("no shape yet" before the first decomposition).

## Page structure

Head ([L1–23](../../public/simulations/draw-decompose.html#L1-L23)): `styles/sim.css` (Google Fonts, KaTeX CSS and
`paper.css` by `@import`, [sim.css:7–9](../../public/styles/sim.css#L7-L9)), `styles/data.css`, `styles/fold.css`, an
inline favicon and a short inline `<style>`: crosshair cursor, `touch-action: none` on the canvas, no text selection on
the stage, the preset grid, the hint, and `[hidden]` forced to `display: none`
([L15–22](../../public/simulations/draw-decompose.html#L15-L22)). See [styles.md](../styles.md).

Body: the top bar with the hand-written Fig. links ([L25–40](../../public/simulations/draw-decompose.html#L25-L40)); the
head ([L44–48](../../public/simulations/draw-decompose.html#L44-L48)); Fig. 8a, `#stage` with canvas `#field`, caption
with `#cap-mode`, `#cap-src` ([L52–60](../../public/simulations/draw-decompose.html#L52-L60)); Fig. 8b, `#spec-stage`
with canvas `#spec`, caption with `#cap-k` ([L61–69](../../public/simulations/draw-decompose.html#L61-L69)); the
controls aside: Shape group with hint, `#run-tools`, `#draw-tools` and presets, Reconstruction group, readouts, legend
([L72–133](../../public/simulations/draw-decompose.html#L72-L133)); the lecture note
([L136–607](../../public/simulations/draw-decompose.html#L136-L607)); the walkthrough host `#walk` (`data-walk="dft"`,
[L609](../../public/simulations/draw-decompose.html#L609)); the footer.

Scripts, in load order: `fold.js`, `sim.js`, `dataset.js`, the page script
([L620–1412](../../public/simulations/draw-decompose.html#L620-L1412)), `datalog.js`
([L617–1413](../../public/simulations/draw-decompose.html#L617-L1413)). `sim.js` fetches `walk/dft.js` from `data-walk`
and typesets the note ([sim.js:413–441](../../public/scripts/sim.js#L413-L441), [sim.js:476–486](../../public/scripts/sim.js#L476-L486));
the canvas labels use `Sim.tex` from `sim.js`. See [sim.md](../scripts/sim.md), [walk.md](../scripts/walk.md),
[fold.md](../scripts/fold.md), [pages.md](../pages.md).

Lecture note "Drawing with circles: the Fourier series of a closed curve": 9 sections: 1 A drawing made of circles;
2 The model; 3 Each circle is an average; 4 From an integral to 256 samples ★ (4.1 orthogonality, 4.2 aliasing, 4.3 the
sum the page computes); 5 Parseval's theorem and the error (box "Keep the largest circles", Exercise 5.1); 6 Corners
cost circles ★ (6.1, 6.2, Exercise 6.1); 7 What the page computes (7.1 Accuracy); 8 From units to pixels; 9 What the
model leaves out (9.1 Further reading, 4 references). 16 numbered display equations (counted in the rendered page).
Five figures, all inline SVG: Figure 1 three circles tip to tail ([L165–208](../../public/simulations/draw-decompose.html#L165-L208));
Figure 2 a raw stroke and its 16-point resampling ([L217–289](../../public/simulations/draw-decompose.html#L217-L289));
Figure 3 relative RMS error against K for heart and square ([L333–379](../../public/simulations/draw-decompose.html#L333-L379));
Figure 4 two plates, heart and square at K = 3, 10, 50 ([L380–472](../../public/simulations/draw-decompose.html#L380-L472));
Figure 5 $|c_k|$ against $|k|$ for four presets ([L493–551](../../public/simulations/draw-decompose.html#L493-L551)).

## Where the drawing and the store differ

The page's `about` paragraph ([L1403](../../public/simulations/draw-decompose.html#L1403)), shown in the data panel
([datalog.js:164](../../public/scripts/datalog.js#L164)), says this; the code adds detail:

- **Dashed original** is the 256 stored samples $z_n$ joined by straight segments and closed
  ([L1114](../../public/simulations/draw-decompose.html#L1114)); the raw stroke `stroke_x/y` is stored but not drawn
  while playing.
- **Full curve** is the stored 601 points joined by straight segments.
- **Trail** is history: the pen at the end of each past frame over just under one loop, faded in 24 segments. Changing K
  clears it ([L847](../../public/simulations/draw-decompose.html#L847)).
- **Small circles are hidden**: a circle under 1.5 px radius is not drawn, an arrow under 8 px gets no head, and only
  the first 12 arrows are numbered, where room allows ([L1142](../../public/simulations/draw-decompose.html#L1142),
  [L1159](../../public/simulations/draw-decompose.html#L1159), [L1167](../../public/simulations/draw-decompose.html#L1167)).
  The store keeps all K arms.
- **View scale** follows `viewR`, which relaxes over 0.4 s; `scale` is a smoothed quantity, not a formula of the
  current frame.
- **Spectrum bars** are normalised to the largest radius and redrawn only on rebuild or resize.

## How to change it safely

- **Walkthrough excerpts.** `dft.js` quotes these page lines verbatim (checked by script):
  [736–737](../../public/simulations/draw-decompose.html#L736-L737), [740](../../public/simulations/draw-decompose.html#L740),
  [758–764](../../public/simulations/draw-decompose.html#L758-L764), [766](../../public/simulations/draw-decompose.html#L766),
  [772–775](../../public/simulations/draw-decompose.html#L772-L775), [786–787](../../public/simulations/draw-decompose.html#L786-L787),
  [790](../../public/simulations/draw-decompose.html#L790), [815–816](../../public/simulations/draw-decompose.html#L815-L816),
  [821](../../public/simulations/draw-decompose.html#L821), [824](../../public/simulations/draw-decompose.html#L824),
  [1275](../../public/simulations/draw-decompose.html#L1275). Change both together; add taps after a quoted line.
- **`NS` is not the only 256.** The static readout `r-N` ([L121](../../public/simulations/draw-decompose.html#L121)) and
  the 256 phases of the `extR` scan ([L837](../../public/simulations/draw-decompose.html#L837),
  [L1368](../../public/simulations/draw-decompose.html#L1368)) are literals, and the note quotes 256 throughout.
- **`KMAX` appears as literals** in the K slider maximum ([L100](../../public/simulations/draw-decompose.html#L100)), the
  spectrum ticks ([L1207](../../public/simulations/draw-decompose.html#L1207)), the Fig. 8b caption
  ([L66](../../public/simulations/draw-decompose.html#L66)) and the `spec_x` formula strings
  ([L696](../../public/simulations/draw-decompose.html#L696), [L1384](../../public/simulations/draw-decompose.html#L1384)).
- **Spectrum geometry** (pad 18, base $h - 22$, top 10) is repeated in `check.spec_x`, `check.spec_y` and the metadata
  ([L1384–1385](../../public/simulations/draw-decompose.html#L1384-L1385), [L696–697](../../public/simulations/draw-decompose.html#L696-L697)).
- **The 0.46 scale** is in `S()`, the dataset attrs, `check.S_fit` and note eq. (16)
  ([L727](../../public/simulations/draw-decompose.html#L727), [L637](../../public/simulations/draw-decompose.html#L637),
  [L1386](../../public/simulations/draw-decompose.html#L1386)).
- **Formulas live twice** for Check: `chainAt()` as `chainNow()`, `dft()` as `dftOne()`, the `extR` scan as
  `check.extR` ([L1296–1297](../../public/simulations/draw-decompose.html#L1296-L1297),
  [L1365–1370](../../public/simulations/draw-decompose.html#L1365-L1370)).
- **`resamp()` has a local `ds`** ([L734](../../public/simulations/draw-decompose.html#L734)) that hides the dataset;
  a store write added inside `resamp()` would call the local array. Write in `decompose()` instead.
- **Numbers quoted in the note** come from the presets and defaults: square side 1.4, heart $L = 5.428$, default K = 24
  and $T_\text{loop} = 12$ s, the 0.006 drawing threshold, the error values in sections 5–7 and Figures 3–5. Changing a
  preset, NS or KMAX means recomputing them.
- **Re-test**: no console errors in headless Chromium; Heart at K = 24 should still give `err` and `errP` agreeing within
  the 3 parts in $10^{10}$ the note quotes ([L330](../../public/simulations/draw-decompose.html#L330)); run Check on `c_re`, `kept`, `err`, `px`, `spec_y`; draw a stroke with Read values off, then on
  (a click must pin, not draw); record one round.

## Notes for maintainers

1. **`touchProbe` is dead.** `Sim.data.touchProbe` ([L1402](../../public/simulations/draw-decompose.html#L1402)) is not
   read anywhere in `datalog.js` (no match for `touchProbe`).
2. **`c_max` is mislabelled.** Its metadata and check say "|c_0| or 1"
   ([L695](../../public/simulations/draw-decompose.html#L695), [L1383](../../public/simulations/draw-decompose.html#L1383)),
   but the value is `coefs[0].amp`, the radius of rank 0, the largest circle
   ([L1221](../../public/simulations/draw-decompose.html#L1221)). The $k = 0$ coefficient is never computed
   ([L755](../../public/simulations/draw-decompose.html#L755)).
3. **Walkthrough step 5 overstates exactness.** It says the sum "hits sample n of your drawing exactly when K includes
   every coefficient" ([dft.js:76](../../public/scripts/walk/dft.js#L76)). The page computes only 120 of the 256
   frequencies ([L754](../../public/simulations/draw-decompose.html#L754)). Measured for the heart at K = 120: `err` =
   4.91 × 10⁻⁴, a relative error of 0.068 %, as the lecture note itself states
   ([L590](../../public/simulations/draw-decompose.html#L590)).
4. **Metadata says `L` and `step` are computed in `resamp()`** ([L648–649](../../public/simulations/draw-decompose.html#L648-L649)),
   but they are written in `decompose()` from `arcLen` ([L795](../../public/simulations/draw-decompose.html#L795)), and
   `resamp()` shadows the dataset name `ds` ([L734](../../public/simulations/draw-decompose.html#L734)).
5. Fixed on 2026-10-15: the thumbnail was retaken from .stage__canvas in Chromium at 1440 × 900, device scale 2, and saved as 800 × 500 WebP (commit `:/^Batch B: correct notes and layout; verify measured figures in Chromium$`).
