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
([L1410–1411](../../public/simulations/draw-decompose.html#L1410-L1411)).

## The physics in one picture

Everyday picture: a bead sliding at constant speed along a wire bent into the drawn shape; a music equaliser that
splits a sound into tones; JPEG and MP3, which drop the small components (lecture note section 1,
[L160–165](../../public/simulations/draw-decompose.html#L160-L165)).

Model: the closed curve, traced at constant speed, is a $2\pi$-periodic complex function $z(t)$ of the loop parameter
$t = 2\pi s/L$ (arc length $s$, total length $L$), and so a Fourier series of circles that turn a whole number $k$ of
times per loop (note section 2, [L214–216](../../public/simulations/draw-decompose.html#L214-L216)). This is Fig. 7 run
backwards: the shape is given and the circles follow.

The equations the code evaluates, in order. Lengths are scale-free units (1 unit = 0.46 of the shorter canvas side
while drawing, [L729](../../public/simulations/draw-decompose.html#L729)); $t$ is the loop phase in rad; $T_\text{loop}$ is in s.

1. Arc length of the stroke points $p_j$, $s_i = \sum_{j \le i} |p_j - p_{j-1}|$, $L = s_\text{last}$, spacing
   $\Delta s = L/(N-1)$, and sample $n$ by linear interpolation at distance $n\,\Delta s$, with $N = 256$
   ([L735–751](../../public/simulations/draw-decompose.html#L735-L751)).
2. Centring: $\bar x = \frac1N \sum_n r_{n,x}$, $\bar y$ likewise, $z_n = r_n - (\bar x + i\bar y)$, and
   $\langle |z|^2 \rangle = \frac1N \sum_n |z_n|^2$ ([L786–792](../../public/simulations/draw-decompose.html#L786-L792)).
3. The transform for $k = -60, \dots, 60$, $k \ne 0$, with $z_n = x_n + i y_n$ and $a_n = 2\pi k n/N$ in rad
   ([L756–765](../../public/simulations/draw-decompose.html#L756-L765)):

$$\mathrm{Re}\,c_k = \frac1N \sum_{n=0}^{N-1} \left(x_n \cos a_n + y_n \sin a_n\right), \qquad \mathrm{Im}\,c_k = \frac1N \sum_{n=0}^{N-1} \left(y_n \cos a_n - x_n \sin a_n\right)$$

4. Radius $|c_k|$ and starting angle $\arg c_k = \mathrm{atan2}(\mathrm{Im}, \mathrm{Re})$, then sorting by $|c_k|$,
   largest first ([L766–768](../../public/simulations/draw-decompose.html#L766-L768)).
5. The chain of the first $K$ ranks, and the clock ([L771–781](../../public/simulations/draw-decompose.html#L771-L781),
   [L1277](../../public/simulations/draw-decompose.html#L1277)):

$$z_K(t) = \sum_{\text{rank} < K} |c_k|\, e^{i(kt + \arg c_k)}, \qquad t \leftarrow t + \frac{2\pi\,\Delta t}{T_\text{loop}}$$

6. Parseval and the measured error, with $\tilde z_n = z_K(2\pi n/N)$
   ([L817–827](../../public/simulations/draw-decompose.html#L817-L827)):

$$\text{kept} = \sum_{\text{rank} < K} |c_k|^2, \qquad e_P = \sqrt{\max(0, \langle |z|^2\rangle - \text{kept})}, \qquad e = \sqrt{\frac1N \sum_n |\tilde z_n - z_n|^2}$$

The lecture note derives the series and the coefficient as an average (sections 2–3, eqs. 1–3), the DFT, exact
orthogonality on the samples and aliasing (section 4, eqs. 4–7), Parseval and the error (section 5, eqs. 8–10), the
$1/k$ and $1/k^2$ decay at jumps and corners (section 6, eqs. 11–14), the per-frame sum (section 7, eq. 15) and the
screen scale (section 8, eq. 16).

## How the code computes it

**Constants and state** ([L625–636](../../public/simulations/draw-decompose.html#L625-L636)). `NS = 256` samples,
`KMAX = 60`. `stroke` is the current shape's raw points, `samples` the centred $z_n$, `coefs` the sorted
coefficients `{ k, re, im, amp, phase }`, `full` the 601-point K-term curve. `meanZ2`, `kept`, `err`, `errP` hold the
energies and errors. `t` is the loop phase, `trail` the pen history. `extR` is the outermost radius drawn over a loop,
`viewR` the radius the view is fitted to. `draft` is the stroke being drawn; `zoom`, `panX`, `panY` set the view;
`ptrs` and `pinch` track pointers.

**Method.** A direct DFT, not an FFT: 120 frequencies × 256 samples = 30 720 complex products, done once per shape
([L754–769](../../public/simulations/draw-decompose.html#L754-L769)); the note explains the choice in section 4.3
([L318](../../public/simulations/draw-decompose.html#L318)). Only $|k| \le 60$, below $N/2 = 128$, is computed, so each
coefficient is one true coefficient plus small aliases (note section 4.2). Playback evaluates the chain in closed form,
so there is no integration error and the pen returns to the same place after every loop. Sorting by radius makes the
first $K$ the least-squares best choice of $K$ circles (note box "Keep the largest circles",
[L328–331](../../public/simulations/draw-decompose.html#L328-L331)).

**Once per shape**, `decompose(pts, name)` ([L783–810](../../public/simulations/draw-decompose.html#L783-L810)):
resample with `resamp()`; centre; compute $\langle|z|^2\rangle$; write `stroke_*`, `r_*`, `z_*`, `L`, `step`, `mx`,
`my`, `E`; run `dft()`; write the sorted coefficient arrays; set the K slider's maximum to the number of coefficients
(120) and clamp K; reset `t = 0` and the trail; switch to `mode = 'play'`; call `rebuild()`. Presets enter the same
pipeline as a drawing: `param()` gives 1201 points of a parametric curve
([L855–862](../../public/simulations/draw-decompose.html#L855-L862)), `poly()` 100 points per polygon edge plus the
closing point ([L863–871](../../public/simulations/draw-decompose.html#L863-L871)); the shapes are in `SHAPES`
([L872–892](../../public/simulations/draw-decompose.html#L872-L892)).

**Whenever K changes**, `rebuild()` ([L813–852](../../public/simulations/draw-decompose.html#L813-L852)) computes `kept`,
`errP`, the truncated series at the 256 sample times with the pointwise error `e_i` and `err`, the share `cap`, the
601-point `full` curve at $t = 2\pi i/600$, and `extR`: the larger of the farthest sample and, over 256 phases around
the loop, every circle's centre distance plus its radius
([L837–848](../../public/simulations/draw-decompose.html#L837-L848)). It clears the trail, then calls `readouts()` and
`spectrum()`.

**Frame loop**, the `Sim.clock` callback ([L1271–1289](../../public/simulations/draw-decompose.html#L1271-L1289)), in order:

1. `real` = wall time since the last frame, capped at 0.05 s ([L1272](../../public/simulations/draw-decompose.html#L1272)).
2. `viewR` jumps up to `extR` at once, or relaxes down toward it with a time constant of 0.4 s
   ([L1274–1275](../../public/simulations/draw-decompose.html#L1274-L1275)).
3. Playing and `dt > 0` only: advance `t`, evaluate the chain, push `{ x, y, t }` onto the trail, and drop points older
   than $0.98 \cdot 2\pi$ of phase, so the trail covers just under one loop
   ([L1276–1281](../../public/simulations/draw-decompose.html#L1276-L1281)).
4. Write the trail arrays and the frame scalars ([L1282–1287](../../public/simulations/draw-decompose.html#L1282-L1287)),
   then `draw()`.

`draw()` ([L1049–1195](../../public/simulations/draw-decompose.html#L1049-L1195)) evaluates the chain again at the
same `t` ([L1052](../../public/simulations/draw-decompose.html#L1052)). The scale is $S = 0.46\min(w,h)$ while drawing
([L729](../../public/simulations/draw-decompose.html#L729)) and $S/\max(1, R_\text{view})\times\text{zoom}$ while
playing ([L907](../../public/simulations/draw-decompose.html#L907)). The origin sits at the canvas centre, shifted so
that the pen (Follow the pen) or the pan point is in the middle
([L1053–1057](../../public/simulations/draw-decompose.html#L1053-L1057)). Order of painting: axes with TeX names "Im z",
"Re z" and a "px per unit of z" line ([L1066–1077](../../public/simulations/draw-decompose.html#L1066-L1077)). In
drawing mode: the draft in burgundy, a dashed line from its end back to its start, a ring at the start and a dot at
the end ([L1082–1109](../../public/simulations/draw-decompose.html#L1082-L1109)). While playing: the 256 samples as a
closed dashed ink line, the full curve in pink `#c9707e`, the trail in 24 segments with opacity
$0.12 + 0.88\,(c+1)/24$ ([L1112–1135](../../public/simulations/draw-decompose.html#L1112-L1135)); then each arm in rank
order: its rose circle when the radius exceeds 1.5 px, its arrow in one of four colours `VEC`, dashed for odd ranks
below 12, with a head when longer than 8 px and a rank number for the first 12 when longer than 16 px and the place is
free ([L1141–1177](../../public/simulations/draw-decompose.html#L1141-L1177)); dashed lines from the pen to both axes;
the pen, a 5 px burgundy dot ([L1178–1194](../../public/simulations/draw-decompose.html#L1178-L1194)).

`spectrum()` ([L1197–1240](../../public/simulations/draw-decompose.html#L1197-L1240)) draws Fig. 8b once per rebuild and
on resize: bar $k$ at $x = 18 + (k+60)/120\,(w-36)$, top at $y = b - |c_k|/|c|_\text{max}\,(b-10)$ with base
$b = h - 22$, burgundy for ranks below K, tan otherwise.

**Pointer** ([L903–1006](../../public/simulations/draw-decompose.html#L903-L1006)). While drawing, `world()` maps a
pointer to units with $S$ and the canvas centre ([L903–906](../../public/simulations/draw-decompose.html#L903-L906));
a point is added when it lies more than 0.006 units from the last one
([L957](../../public/simulations/draw-decompose.html#L957)), and *Decompose & play* needs at least 12 points
([L919](../../public/simulations/draw-decompose.html#L919), [L986](../../public/simulations/draw-decompose.html#L986)).
While playing, a drag pans (and turns Follow the pen off, starting the pan at the pen), two pointers pinch-zoom, and
the wheel zooms by $e^{-0.0015\,\Delta y}$ about the cursor, or about the pen while following it ([L960–1006](../../public/simulations/draw-decompose.html#L960-L1006)).
Zoom is clamped to $[1, 10^{1.8}]$ ([L908–911](../../public/simulations/draw-decompose.html#L908-L911)).

## Function map

| Function | Lines | What it does |
|---|---|---|
| `$` | [626](../../public/simulations/draw-decompose.html#L626) | `document.getElementById`. |
| `S` | [729](../../public/simulations/draw-decompose.html#L729) | Base scale $0.46\min(w,h)$, px per unit. |
| `resamp` | [735–751](../../public/simulations/draw-decompose.html#L735-L751) | Equal arc-length resampling to N points; sets `arcLen`. |
| `dft` | [754–769](../../public/simulations/draw-decompose.html#L754-L769) | Direct DFT for $-60 \le k \le 60$, $k \ne 0$; sorted by radius. |
| `chainAt` | [771–781](../../public/simulations/draw-decompose.html#L771-L781) | Sum of the first n ranks at loop phase `time`, with each arm's parts. |
| `decompose` | [783–810](../../public/simulations/draw-decompose.html#L783-L810) | The once-per-shape pipeline. |
| `rebuild` | [813–852](../../public/simulations/draw-decompose.html#L813-L852) | Everything that depends on K. |
| `param`, `poly` | [855–871](../../public/simulations/draw-decompose.html#L855-L871) | Points of a parametric curve; points along a polygon. |
| `SHAPES.*` | [872–892](../../public/simulations/draw-decompose.html#L872-L892) | heart, star, square, eight, trefoil, wave. |
| `#presets` click | [894–900](../../public/simulations/draw-decompose.html#L894-L900) | Loads a preset through `play()`. |
| `world` | [903–906](../../public/simulations/draw-decompose.html#L903-L906) | Pointer to drawing units. |
| `viewScale` | [907](../../public/simulations/draw-decompose.html#L907) | Playing scale. |
| `setZoom` | [908–911](../../public/simulations/draw-decompose.html#L908-L911) | Clamped zoom; moves the slider. |
| `setMode` | [912–926](../../public/simulations/draw-decompose.html#L912-L926) | Drawing or playing: tool rows, cursor, hint. |
| `startDraw` | [927–930](../../public/simulations/draw-decompose.html#L927-L930) | Empty draft, drawing mode. |
| `play` | [931–935](../../public/simulations/draw-decompose.html#L931-L935) | Reset pan, decompose, playing mode. |
| canvas `mousedown`, `pointerdown`, `pointermove` | [936–981](../../public/simulations/draw-decompose.html#L936-L981) | Draw, or pan and pinch. |
| `endPointer` (+ `pointerup`, `pointercancel`) | [982–994](../../public/simulations/draw-decompose.html#L982-L994) | End a stroke or a gesture. |
| canvas `wheel` | [995–1006](../../public/simulations/draw-decompose.html#L995-L1006) | Zoom about the cursor. |
| Button and switch listeners | [1007–1024](../../public/simulations/draw-decompose.html#L1007-L1024) | New drawing, Clear, Cancel, Decompose & play, Restart loop, Reset view, Follow the pen. |
| `line` | [1027–1035](../../public/simulations/draw-decompose.html#L1027-L1035) | Strokes a run of points. |
| `labelFree` | [1038–1042](../../public/simulations/draw-decompose.html#L1038-L1042) | Keeps arrow numbers from overlapping. |
| `axisName` | [1043–1048](../../public/simulations/draw-decompose.html#L1043-L1048) | TeX axis label on a pale ground. |
| `draw` | [1049–1195](../../public/simulations/draw-decompose.html#L1049-L1195) | Paints one frame and writes the drawing variables. |
| `spectrum` | [1197–1240](../../public/simulations/draw-decompose.html#L1197-L1240) | Fig. 8b and `spec_x`, `spec_y`, `c_max`. |
| `readouts` | [1242–1252](../../public/simulations/draw-decompose.html#L1242-L1252) | Readouts and captions. |
| `Sim.live` | [1255–1268](../../public/simulations/draw-decompose.html#L1255-L1268) | Formatted store values for the walkthrough. |
| clock callback | [1271–1289](../../public/simulations/draw-decompose.html#L1271-L1289) | The frame loop above. |
| `pixelAt`, `rgbText`, `lum` | [1293–1295](../../public/simulations/draw-decompose.html#L1293-L1295) | Read a pixel of either canvas; describe it; luminance. |
| `playing`, `toScreen` | [1296–1297](../../public/simulations/draw-decompose.html#L1296-L1297) | Data-panel helpers from stored values. |
| `chainNow`, `dftOne`, `nearest`, `armInputs` | [1298–1301](../../public/simulations/draw-decompose.html#L1298-L1301) | Recompute from stored inputs (Check); nearest stored point. |
| `Sim.data` hooks | [1302–1405](../../public/simulations/draw-decompose.html#L1302-L1405) | `probe`, `inspect`, `locate`, `check`, `drawn`, `round`, `play`, `about`. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| New drawing | `redraw` | — | `startDraw()` ([L1007](../../public/simulations/draw-decompose.html#L1007)) |
| Decompose & play | `go` | needs ≥ 12 draft points | `play(draft, 'your drawing')`, starts the clock ([L1010–1016](../../public/simulations/draw-decompose.html#L1010-L1016)) |
| Clear | `clear-draft` | — | empties the draft ([L1008](../../public/simulations/draw-decompose.html#L1008)) |
| Cancel | `cancel` | disabled with no shape | back to the current shape ([L1009](../../public/simulations/draw-decompose.html#L1009)) |
| Play / Pause | `play` | playing (paused under reduced motion) | `Sim.playButton` ([L1290](../../public/simulations/draw-decompose.html#L1290), [sim.js:177](../../public/scripts/sim.js#L177)) |
| Restart loop | `reset-t` | — | `t = 0`, trail cleared ([L1017](../../public/simulations/draw-decompose.html#L1017)) |
| Presets | `presets`, `data-shape` | heart (at load) | `SHAPES[s]()` then `play()` ([L894–900](../../public/simulations/draw-decompose.html#L894-L900)) |
| Circles K | `K` | 1–120, step 1, default 24 | `rebuild()` on input ([L101](../../public/simulations/draw-decompose.html#L101), [L723](../../public/simulations/draw-decompose.html#L723)) |
| Time per loop | `loop` | 4–30 s, step 1, default 12 | $T_\text{loop}$ in the clock ([L105](../../public/simulations/draw-decompose.html#L105), [L1277](../../public/simulations/draw-decompose.html#L1277)) |
| Zoom | `zoom` | 0–1.8, step 0.01, default 0 (shown as $10^v$: 1× to 63×) | `zoom = 10^v` ([L109](../../public/simulations/draw-decompose.html#L109), [L727](../../public/simulations/draw-decompose.html#L727)) |
| Follow the pen | `sw-follow` | off | view centre on the pen; turning it off pans to the pen ([L1019–1024](../../public/simulations/draw-decompose.html#L1019-L1024)) |
| Reset view | `reset-view` | — | pan 0, zoom 1, follow off ([L1018](../../public/simulations/draw-decompose.html#L1018)) |
| Component circles / Tip-to-tail vectors / Your drawing / Full K-term curve | `sw-circles`, `sw-vectors`, `sw-orig`, `sw-full` | on / on / on / off | what `draw()` paints ([L1112](../../public/simulations/draw-decompose.html#L1112), [L1119](../../public/simulations/draw-decompose.html#L1119), [L1144](../../public/simulations/draw-decompose.html#L1144), [L1151](../../public/simulations/draw-decompose.html#L1151)) |
| Pointer on the figure | `field` | — | draw (drawing mode); pan, pinch, wheel zoom (playing) |

Readouts ([L121–128](../../public/simulations/draw-decompose.html#L121-L128)), filled by `readouts()`: `r-N` (static
text "256" in the HTML), `r-K` ("K of 120"), `r-cap` (kept share in %), `r-k1` (frequency of the largest circle, with
sign), `r-err`, `r-errp` ([L1242–1252](../../public/simulations/draw-decompose.html#L1242-L1252)). Captions: `cap-mode`,
`cap-src`, `cap-k`.

## What the page writes into the data store

`Sim.dataset({ title: 'Draw and decompose', attrs: { figure: 8, page, NS, KMAX, length_unit } })`
([L639](../../public/simulations/draw-decompose.html#L639)); 74 variables declared at
[L640–720](../../public/simulations/draw-decompose.html#L640-L720) (count measured in headless Chromium). Dims: `stroke`
(raw points), `draft`, `n` (256 samples), `k` (120 coefficients in sorted order, so row $j$ is rank $j$), `full` (601),
`arm` (K), `trail`. See [dataset.md](../scripts/dataset.md).

| Group (as in `Sim.data.groups`) | Variables | Written at |
|---|---|---|
| The stroke | `source`; `mode`, `drawing`; `stroke_x/y` [stroke]; `draft_x/y` [draft]; `N`; `L`, `step`, `mx`, `my`, `E`; `r_x/y`, `z_x/y` [n] | [803](../../public/simulations/draw-decompose.html#L803); [1058](../../public/simulations/draw-decompose.html#L1058); [795](../../public/simulations/draw-decompose.html#L795); [1064](../../public/simulations/draw-decompose.html#L1064); [721](../../public/simulations/draw-decompose.html#L721); [797](../../public/simulations/draw-decompose.html#L797); [796](../../public/simulations/draw-decompose.html#L796) |
| Coefficients | `c_k`, `c_re`, `c_im`, `c_amp`, `c_phase` [k]; `K`, `kept`, `cap`, `errP`, `err`; `zr_x/y`, `e_i` [n]; `full_x/y` [full]; `extR` | [801](../../public/simulations/draw-decompose.html#L801); [827](../../public/simulations/draw-decompose.html#L827); [824](../../public/simulations/draw-decompose.html#L824); [834](../../public/simulations/draw-decompose.html#L834); [848](../../public/simulations/draw-decompose.html#L848) |
| The chain now | `t`, `loop_s`; `A_arm`, `ang`, `vx`, `vy`, `jx`, `jy`, `px`, `py` [arm]; `x`, `y`; `tip_px`, `tip_py` | [1287](../../public/simulations/draw-decompose.html#L1287); [1143](../../public/simulations/draw-decompose.html#L1143); [1060](../../public/simulations/draw-decompose.html#L1060); [1187](../../public/simulations/draw-decompose.html#L1187) |
| Trail | `trail_t`, `trail_x`, `trail_y` [trail] | [1285](../../public/simulations/draw-decompose.html#L1285) |
| Spectrum panel | `c_max`; `spec_x`, `spec_y` [k]; `sbox_w`, `sbox_h` | [1225](../../public/simulations/draw-decompose.html#L1225); [1228](../../public/simulations/draw-decompose.html#L1228); [1199](../../public/simulations/draw-decompose.html#L1199) |
| View and drawing | `viewR`, `dt`, `fps`, `frames`, `playing`; `zoom`, `panX`, `panY`, `follow`, `S_fit`, `scale`, `cx`, `cy`, `box_w`, `box_h`; `circles`, `vectors`, `orig`, `full` | [1287](../../public/simulations/draw-decompose.html#L1287); [1058](../../public/simulations/draw-decompose.html#L1058); [1059](../../public/simulations/draw-decompose.html#L1059) |

`mode`, `t` and `loop_s` are also written once at start-up ([L1406](../../public/simulations/draw-decompose.html#L1406)).
Measured at load on a 1440 px window for the heart: `L` = 5.42763, `E` = 0.515045, and at K = 24 `err` =
0.005405966670666 and `errP` = 0.005405966670687; `extR` = 0.9435, so the scale is $S$ itself, 276.46 px per unit
on a 770 × 601 canvas.

**One round** (`Sim.data.round`, [L1401–1401](../../public/simulations/draw-decompose.html#L1401-L1401)): the time
variable is `t` (rad), the length is $2\pi$, one loop of the circles, which takes `loop_s` seconds; columns `x`, `y`;
the point followed is the pen. Recording is blocked unless a shape is playing. See [datalog.md](../scripts/datalog.md).

**Data-panel hooks.** `probe` ([L1315–1325](../../public/simulations/draw-decompose.html#L1315-L1325)) pins, while
drawing, the nearest draft point within 10 px; while playing, a joint or the pen within 10 px, else (each within 8 px)
a sample if *Your drawing* is on, a point of the full curve if it is on, or a trail point. `check` recomputes 40
variables from stored inputs only, including a fresh one-frequency DFT `dftOne()` for `c_re`, `c_im`
([L1346–1392](../../public/simulations/draw-decompose.html#L1346-L1392)). `drawn` reads pixels back for `tip_px`, `px`,
`full_x`, `trail_x` on the figure and `spec_y` on the spectrum canvas, alpha first
([L1393–1399](../../public/simulations/draw-decompose.html#L1393-L1399)). Read values works on `#stage` only, so the
spectrum panel is not pinnable ([datalog.js:849](../../public/scripts/datalog.js#L849)). While Read values is on,
`datalog.js` stops the canvas's own pointer handlers in the capture phase, so a click pins instead of drawing or panning
([datalog.js:924–947](../../public/scripts/datalog.js#L924-L947)); the wheel is not intercepted. File base name:
`fig8-draw-decompose` ([L1302](../../public/simulations/draw-decompose.html#L1302)).

**`Sim.live()`** ([L1255–1268](../../public/simulations/draw-decompose.html#L1255-L1268)) returns, from the store:
`N, L, ds, mx, my, K, tot, E, kept, cap, err, errP, t, tl, src`, and for rank 0 `k1, re, im, A, ph`, plus the pen
`x, y` and the first centred sample `z0` ("no shape yet" before the first decomposition).

## Page structure

Head ([L1–23](../../public/simulations/draw-decompose.html#L1-L23)): `styles/sim.css` (the self-hosted fonts, KaTeX CSS and
`paper.css` by `@import`, [sim.css:8–9](../../public/styles/sim.css#L8-L9)), `styles/data.css`, `styles/fold.css`, an
inline favicon and a short inline `<style>`: crosshair cursor, `touch-action: none` on the canvas, no text selection on
the stage, the preset grid, the hint, and `[hidden]` forced to `display: none`
([L15–22](../../public/simulations/draw-decompose.html#L15-L22)). See [styles.md](../styles.md).

Body: the top bar: one span holding the Phyein Usul logo (a link to `../index.html` with
`../images/phyein-usul-mark.svg`, 87 × 48) and "← All simulations" ([L26](../../public/simulations/draw-decompose.html#L26)), then the hand-written Fig. links
([L25–41](../../public/simulations/draw-decompose.html#L25-L41)); the
head ([L45–49](../../public/simulations/draw-decompose.html#L45-L49)); Fig. 8a, `#stage` with canvas `#field`, caption
with `#cap-mode`, `#cap-src` ([L53–61](../../public/simulations/draw-decompose.html#L53-L61)); Fig. 8b, `#spec-stage`
with canvas `#spec`, caption with `#cap-k` ([L62–70](../../public/simulations/draw-decompose.html#L62-L70)); the
controls aside: Shape group with hint, `#run-tools`, `#draw-tools` and presets, Reconstruction group, readouts, legend
([L73–134](../../public/simulations/draw-decompose.html#L73-L134)); the lecture note
([L137–609](../../public/simulations/draw-decompose.html#L137-L609)); the walkthrough host `#walk` (`data-walk="dft"`,
[L611](../../public/simulations/draw-decompose.html#L611)); the footer.

Scripts, in load order: `fold.js`, `sim.js`, `dataset.js` ([L619–621](../../public/simulations/draw-decompose.html#L619-L621)), the page script
([L622–1413](../../public/simulations/draw-decompose.html#L622-L1413)), `datalog.js`
([L1414](../../public/simulations/draw-decompose.html#L1414)). `sim.js` fetches `walk/dft.js` from `data-walk`
and typesets the note ([sim.js:418–446](../../public/scripts/sim.js#L418-L446), [sim.js:481–490](../../public/scripts/sim.js#L481-L490));
the canvas labels use `Sim.tex` from `sim.js`. See [sim.md](../scripts/sim.md), [walk.md](../scripts/walk.md),
[fold.md](../scripts/fold.md), [pages.md](../pages.md).

Lecture note "Drawing with circles: the Fourier series of a closed curve": 9 sections: 1 A drawing made of circles;
2 The model; 3 Each circle is an average; 4 From an integral to 256 samples ★ (4.1 orthogonality, 4.2 aliasing, 4.3 the
sum the page computes); 5 Parseval's theorem and the error (box "Keep the largest circles", Exercise 5.1); 6 Corners
cost circles ★ (6.1, 6.2, Exercise 6.1); 7 What the page computes (7.1 Accuracy); 8 From units to pixels; 9 What the
model leaves out (9.1 Further reading, 4 references). 16 numbered display equations (counted in the rendered page).
Five figures, all inline SVG: Figure 1 three circles tip to tail ([L166–209](../../public/simulations/draw-decompose.html#L166-L209));
Figure 2 a raw stroke and its 16-point resampling ([L218–290](../../public/simulations/draw-decompose.html#L218-L290));
Figure 3 relative RMS error against K for heart and square ([L335–381](../../public/simulations/draw-decompose.html#L335-L381));
Figure 4 two plates, heart and square at K = 3, 10, 50 ([L382–474](../../public/simulations/draw-decompose.html#L382-L474));
Figure 5 $|c_k|$ against $|k|$ for four presets ([L495–553](../../public/simulations/draw-decompose.html#L495-L553)).

## Where the drawing and the store differ

The page's `about` paragraph ([L1403](../../public/simulations/draw-decompose.html#L1403)), shown in the data panel
([datalog.js:229](../../public/scripts/datalog.js#L229)), says this; the code adds detail:

- **Dashed original** is the 256 stored samples $z_n$ joined by straight segments and closed
  ([L1116](../../public/simulations/draw-decompose.html#L1116)); the raw stroke `stroke_x/y` is stored but not drawn
  while playing.
- **Full curve** is the stored 601 points joined by straight segments.
- **Trail** is history: the pen at the end of each past frame over just under one loop, faded in 24 segments. Changing K
  clears it ([L849](../../public/simulations/draw-decompose.html#L849)).
- **Small circles are hidden**: a circle under 1.5 px radius is not drawn, an arrow under 8 px gets no head, and only
  the first 12 arrows are numbered, where room allows ([L1144](../../public/simulations/draw-decompose.html#L1144),
  [L1161](../../public/simulations/draw-decompose.html#L1161), [L1169](../../public/simulations/draw-decompose.html#L1169)).
  The store keeps all K arms.
- **View scale** follows `viewR`, which relaxes over 0.4 s; `scale` is a smoothed quantity, not a formula of the
  current frame.
- **Spectrum bars** are normalised to the largest radius and redrawn only on rebuild or resize.

## How to change it safely

- **Walkthrough excerpts.** `dft.js` quotes these page lines verbatim (checked by script):
  [738–739](../../public/simulations/draw-decompose.html#L738-L739), [742](../../public/simulations/draw-decompose.html#L742),
  [760–766](../../public/simulations/draw-decompose.html#L760-L766), [768](../../public/simulations/draw-decompose.html#L768),
  [774–777](../../public/simulations/draw-decompose.html#L774-L777), [788–789](../../public/simulations/draw-decompose.html#L788-L789),
  [792](../../public/simulations/draw-decompose.html#L792), [817–818](../../public/simulations/draw-decompose.html#L817-L818),
  [823](../../public/simulations/draw-decompose.html#L823), [826](../../public/simulations/draw-decompose.html#L826),
  [1277](../../public/simulations/draw-decompose.html#L1277). Change both together; add taps after a quoted line.
- **`NS` is not the only 256.** The static readout `r-N` ([L122](../../public/simulations/draw-decompose.html#L122)) and
  the 256 phases of the `extR` scan ([L839](../../public/simulations/draw-decompose.html#L839),
  [L1370](../../public/simulations/draw-decompose.html#L1370)) are literals, and the note quotes 256 throughout.
- **`KMAX` appears as literals** in the K slider maximum ([L101](../../public/simulations/draw-decompose.html#L101)), the
  spectrum ticks ([L1209](../../public/simulations/draw-decompose.html#L1209)), the Fig. 8b caption
  ([L67](../../public/simulations/draw-decompose.html#L67)) and the `spec_x` formula strings
  ([L698](../../public/simulations/draw-decompose.html#L698), [L1386](../../public/simulations/draw-decompose.html#L1386)).
- **Spectrum geometry** (pad 18, base $h - 22$, top 10) is repeated in `check.spec_x`, `check.spec_y` and the metadata
  ([L1386–1387](../../public/simulations/draw-decompose.html#L1386-L1387), [L698–699](../../public/simulations/draw-decompose.html#L698-L699)).
- **The 0.46 scale** is in `S()`, the dataset attrs, `check.S_fit` and note eq. (16)
  ([L729](../../public/simulations/draw-decompose.html#L729), [L639](../../public/simulations/draw-decompose.html#L639),
  [L1388](../../public/simulations/draw-decompose.html#L1388)).
- **Formulas live twice** for Check: `chainAt()` as `chainNow()`, `dft()` as `dftOne()`, the `extR` scan as
  `check.extR` ([L1298–1299](../../public/simulations/draw-decompose.html#L1298-L1299),
  [L1367–1372](../../public/simulations/draw-decompose.html#L1367-L1372)).
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

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig08/`), each change on its existing line: §4: the samples are spaced L/(N − 1) apart ([L304](../../public/simulations/draw-decompose.html#L304)); §5: the opening sentence corrected (all N coefficients redraw the samples; (5) holds among N neighbouring frequencies) ([L323](../../public/simulations/draw-decompose.html#L323)); Figure 4 caption: fewer circles only down to an error of about 10⁻³ ([L473](../../public/simulations/draw-decompose.html#L473)); §9: moment of inertia per unit mass ([L596](../../public/simulations/draw-decompose.html#L596)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.
