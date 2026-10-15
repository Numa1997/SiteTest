# Fig. 1 · Wave Interference

| | |
|---|---|
| Page | [public/simulations/Circular Wave Interference Visualization.html](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html) (905 lines, 188 869 bytes) |
| Walkthrough | [public/scripts/walk/circles.js](../../public/scripts/walk/circles.js) (110 lines, key `circles`) |
| Thumbnail | [public/images/sims/wave-sources.webp](../../public/images/sims/wave-sources.webp) (WebP, 800 × 500 px, 36.5 kB; a still of the two-source field) |
| Catalog entry | [public/scripts/catalog.js#L48](../../public/scripts/catalog.js#L48) (`id: 'wave-sources'`, `fig: 1`, `field: 'optics'`, `stage: 1`, lines 47–63) |

Links written `Lnnn` point into the page file; links to other files carry the file name.

The reader sees a wide field of cream, burgundy and dark-ink bands: the height ψ of a water surface at this instant, around
point sources that sit on one line 10 px above the bottom edge ([L47–48](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L47-L48), [L512](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L512)). The page opens with two sources at
x = 200 and 600 px ([L513](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L513)) and the bands run outward at the speed v = fλ. A click on the field adds a source at that
horizontal position ([L716–719](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L716-L719)); buttons give a row of 16, five random sources, the two defaults, or none
([L59–65](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L59-L65)); three sliders set the wavelength, frequency and damping ([L70–81](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L70-L81)). Under the figure sit the Data panel and
the Read values switch (added by `datalog.js`), the walkthrough "From symbols to code" ([L497](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L497)) and the lecture note
([L98–495](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L98-L495)).

## The physics in one picture

**Everyday picture.** Throw a handful of pebbles into a pond in a line, all at once. Each makes a ring. Where a crest of one
ring meets a crest of another the water rises higher; where a crest meets a trough it stays flat. A little way off, the rings of
a dense row merge into one straight ripple: Huygens' principle ([L124–126](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L124-L126)).

**Model.** The water height ψ(x, y, t) obeys the two-dimensional wave equation, which is linear, so the waves of several sources
simply add ([L190–192](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L190-L192)). The page measures lengths in pixels of a field that is always 800 px wide and fixes no scale in metres
([L193](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L193)); time is in seconds. All sources oscillate in step at one frequency, the medium is non-dispersive, the edges do not
reflect, and the sources do not disturb each other ([L196–201](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L196-L201)). Instead of the true $1/\sqrt{r}$ fall-off of a ring the page uses
an exponential damping that stays finite at the source (note §3.1, [L273–275](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L273-L275)).

**What the code evaluates.** For a grid point at the centre of cell (j, i), with $\Delta x = 800/\text{cols}$ and
$\Delta y = \text{worldH}/\text{rows}$ ([L630](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L630)):

$$x = \left(i + \tfrac12\right)\Delta x, \qquad y = \left(j + \tfrac12\right)\Delta y, \qquad r_s = \sqrt{(x - x_s)^2 + (y - y_s)^2}$$

([L641–644](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L641-L644)). Each source contributes an amplitude and a phase ([L628–629](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L628-L629), [L645](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L645)):

$$a_s = \frac{e^{-g r_s}}{N}, \qquad g = \frac{\gamma}{R}, \qquad R = 300\ \text{px}, \qquad \varphi_s = k r_s, \qquad k = \frac{2\pi}{\lambda}.$$

Because every source shares one angular frequency ω, the time dependence factors out of the sum exactly (note eq. 18,
[L452–454](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L452-L454)). The page builds two time-independent maps and the amplitude ([L647–648](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L647-L648), [L652](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L652)):

$$C = \sum_s a_s \cos k r_s, \qquad S = \sum_s a_s \sin k r_s, \qquad A = \sqrt{C^2 + S^2},$$

and on every frame forms the field from one shared phase ([L660](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L660), [L664–665](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L664-L665), [L762](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L762)):

$$\psi = C\cos\omega t + S\sin\omega t, \quad \text{clipped to } [-1, 1], \qquad \omega t \leftarrow \omega t + 2\pi f\,\Delta t .$$

This is $\psi = \frac{1}{N}\sum_s e^{-g r_s}\cos(k r_s - \omega t)$, the note's eqs. (5)–(7). The speed readout is
$v = f\lambda$ ([L712](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L712), [L711](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L711)). The colour of a cell is row $n = \operatorname{round}(127.5\,\psi + 127.5)$ of a 256-entry table
whose channels are $c = c_0 + (c_\pm - c_0)\,|\psi|^{0.8}$ ([L588–589](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L588-L589), [L667](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L667); note eq. 19).

| Symbol | Code | Unit | Meaning |
|---|---|---|---|
| $x, y$ | `xs[q]`, `ys[q]` | px of the field | cell centre, from the top-left corner, y downward ([L619–620](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L619-L620)) |
| $x_s$ | `sources[s] * WORLD_W` | px | source position; the list stores fractions $u_s$ of the width ([L637](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L637)) |
| $y_s$ | `sy = worldH - SOURCE_LIFT` | px | height of every source, 10 px above the bottom ([L630](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L630)) |
| $r_s$ | `r` | px | distance from cell to source ([L644](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L644)) |
| $\lambda$ | `lambda.value` | px | wavelength (slider) |
| $k$ | `k` | rad/px | wave number $2\pi/\lambda$ ([L628](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L628)) |
| $\gamma$ | `damp.value` | 1 (e-foldings over $R$) | damping (slider) |
| $g$ | `g` | 1/px | attenuation per pixel $\gamma/R$ ([L628](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L628)) |
| $N$ | `n`, `norm = 1/max(1, n)` | 1 | number of sources, at most 24 ([L629](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L629), [L512](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L512)) |
| $f$, $\omega$ | `freq.value`, `2π f` | Hz, rad/s | frequency (slider) and angular frequency ([L711](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L711)) |
| $\omega t$ | `omegaT` | rad | shared phase, accumulated, never wrapped ([L762](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L762)) |
| $\Delta t$ | `dt` | s | real time between frames, capped at 0.05 s ([sim.js:180](../../public/scripts/sim.js#L180)) |
| $C, S, A, \psi$ | `sumC`, `sumS`, `ampl`, `psi` | 1 | the maps and the field, $\lvert\psi\rvert \le 1$ |

## How the code computes it

**State.** `sources` is an array of fractions $u_s$ of the width, newest 24 kept ([L520](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L520), [L702](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L702)). `omegaT` is the shared
phase; `dirty` asks for a rebuild of the maps, `redraw` for one more picture while paused ([L521](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L521)). `cols`, `rows`, `worldH` give
the grid ([L519](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L519)). The maps `sumC`, `sumS`, `ampl`, the field `psi` and the source-1 maps `r1`, `a1`, `ph1` are Float32 arrays
owned by the data store and handed out by `ds.alloc` ([L611–617](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L611-L617)). `off` is an offscreen canvas with one pixel per cell, `img` its
ImageData with alpha preset to 255 ([L518](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L518), [L605–608](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L605-L608)). `LUT` is the 256 × 3 colour table ([L584](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L584)).

**Method.** A closed form, not a time integration. Space and time separate exactly, so the expensive part (one `sqrt`, `exp`,
`cos` and `sin` per source per cell) runs only when the geometry changes, and a frame costs two multiplications and one addition
per cell whatever N is ([L664](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L664)). There is no stability question. The only time error is the 0.05 s cap on Δt
([sim.js:180](../../public/scripts/sim.js#L180)): on a slow device the pattern runs slower, it is not distorted.

**Frame loop** (`Sim.clock` callback, [L756–767](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L756-L767)), in order:
1. Keep the play time, count frames, smooth the frame rate as fps ← fps + (1/Δt − fps)/10 ([L757–758](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L757-L758)); store `t`, `dt`,
   `fps`, `frames`, `playing` ([L759](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L759)).
2. If `dirty`, run `precompute()` and ask for a redraw ([L760](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L760)).
3. If playing (Δt > 0) or a redraw is pending: advance `omegaT` by 2πfΔt ([L762](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L762)), store it ([L763](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L763)), `render()` ([L764](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L764)).

`Sim.clock` calls the callback on every animation frame, with Δt = 0 while paused ([sim.js:176–186](../../public/scripts/sim.js#L176-L186)); a paused page therefore
draws nothing unless a slider or button asked for a redraw.

**`precompute()`** ([L627–657](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L627-L657)): computes `k`, `g`, `n`, `norm`, `dx`, `dy`, `sy` and stores them ([L628–631](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L628-L631)); resizes
dimension `s` and allocates `u`, `x_s` ([L632–633](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L632-L633)); zeroes `sumC`, `sumS` ([L634–635](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L634-L635)); loops sources, then rows, then
columns, accumulating $a\cos\varphi$ and $a\sin\varphi$ and keeping $r$, $a$, $\varphi$ of the first source ([L636–651](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L636-L651)); fills
`A` ([L652](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L652)); zeroes the source-1 maps when there is no source ([L653](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L653)); marks the arrays changed and records build count, time
and the number of `cos` + `sin` calls, 2NP ([L654–655](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L654-L655)).

**`render()`** ([L659–699](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L659-L699)): takes cos ωt and sin ωt once ([L660](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L660)); for every cell forms ψ, clips it, stores it, picks the
colour row and writes RGB into `img` ([L663–672](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L663-L672)); puts the small image on `off` and stretches it over the canvas with
`imageSmoothingQuality = 'high'` ([L673–676](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L673-L676)); paints each source as a cream glow of radius 20 px and a burgundy dot of radius
5.5 px with a 2 px cream rim ([L678–695](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L678-L695)); stores the centre-cell value, its colour row and colour, the render count and time
([L696–698](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L696-L698)).

**Precomputation and caching.**
- The colour table is built once at start-up ([L585–592](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L585-L592)).
- The maps are rebuilt only when `dirty` is set: by λ and γ through `changed()` ([L594](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L594), [L596](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L596), [L598](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L598)), by any source change
  through `setSources()` ([L701–704](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L701-L704)) and by `resize()` ([L624](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L624)). `changed()` only sets the flag, so several slider events
  within one frame cost one rebuild. The frequency slider calls `readouts()` only ([L595](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L595)): f changes the speed of the
  pattern, never its shape.
- Grid size: cols = clamp(round(box.w/1.1), 60, 360), rows = max(30, round(cols · box.h/box.w)), worldH = 800 · box.h/box.w
  ([L602–604](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L602-L604)). Resizes are debounced by 80 ms ([sim.js:142–150](../../public/scripts/sim.js#L142-L150), [L901](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L901)).

Measured in headless Chromium in this session (viewport height 900 px):

| Window width | Canvas (css px) | cols × rows | Points P |
|---|---|---|---|
| 1280 and 1440 px | 770 × 347 | 360 × 162 | 58 320 |
| 1600 px | 630 × 284 | 360 × 162 | 58 320 |
| 880 px | 814 × 814 | 360 × 360 | 129 600 |
| 390 px | 356 × 356 | 324 × 324 | 104 976 |

At 1280 px one rebuild for the two default sources took 15.2 ms and one frame 1.1 ms; *Line of 16* at 1440 px is
1 866 240 `cos` + `sin` calls and took 86.7 ms in one run. At λ = 16 px the grid gives 7.2 points per wavelength on the wide screen
(Δx = 2.22 px) and 6.5 on the phone (Δx = 2.47 px).

## Function map

All functions live in the one inline script ([L508–903](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L508-L903)), wrapped in an immediately invoked function ([L509](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L509)).

| Function | Lines | What it does |
|---|---|---|
| colour-table builder (anonymous) | [L585–591](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L585-L591) | Fills `LUT`: for row i, a = i/127.5 − 1, s = \|a\|^0.8, each channel `mid + (end − mid) · s`, end = ink for a < 0, burgundy otherwise. |
| slider `format` callbacks | [L594–596](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L594-L596) | Text for the `<output>` beside each slider: "30 px", "1.10 Hz", "0.15". |
| `changed()` | [L598](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L598) | Marks the maps stale and refreshes the readouts. |
| `resize()` | [L600–625](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L600-L625) | Fits the canvas, sets the grid, sizes the offscreen image, reallocates every grid array in the store, writes cell-centre coordinates and grid scalars, marks the maps stale. |
| `precompute()` | [L627–657](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L627-L657) | Builds C, S, A and the source-1 maps (see above). |
| `render()` | [L659–699](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L659-L699) | Turns C, S and ωt into ψ and pixels; draws the source dots. |
| `setSources(list)` | [L701–704](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L701-L704) | Keeps the newest 24 entries and calls `changed()`. |
| `readouts()` | [L706–714](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L706-L714) | Writes source count, caption count and speed into the DOM; stores λ, f, γ, v, ω, T; asks for a redraw. |
| canvas `click` handler | [L716–719](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L716-L719) | Adds a source at the clicked fraction of the width. |
| *Line of 16* handler | [L720–724](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L720-L724) | Sixteen sources at u = 0.08 + 0.84 n/15. |
| *Add 5 random* handler | [L725–729](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L725-L729) | Appends five at u uniform in [1/6, 5/6]. |
| *Reset* handler | [L730–733](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L730-L733) | ωt = 0, sources back to `DEFAULT`. |
| *Clear* handler | [L734](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L734) | Empty source list. |
| `Sim.live()` | [L737–754](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L737-L754) | Strings for the walkthrough's "Now" column, read from the store at the centre cell. |
| clock callback | [L756–767](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L756-L767) | The frame loop above. |
| `cellIndex(j, i)` | [L771](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L771) | Flat index j · cols + i. |
| `cellCentre(j, i)` | [L772](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L772) | Cell centre in css px of the canvas. |
| `lut(v)` | [L773](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L773) | Colour-table entry for a value, for shading table cells in the panel. |
| `sliderCheck(input, label)` | [L774](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L774) | Check record for a slider value. |
| `sumAt(p, trig)` | [L776–787](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L776-L787) | Re-sums one cell from stored inputs (`x`, `y`, `k`, `g`, `norm`, `x_s`, `y_s`) for the C and S checks. |
| `pixelCheck(p)` | [L789–797](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L789-L797) | Reads pixel (i, j) of the offscreen image and compares it with the table row for the stored ψ; also reports the screen pixel at the cell centre. |
| `Sim.data.playing`, `.play` | [L800](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L800), [L895](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L895) | Clock state and start, for the panel's round recorder. |
| `Sim.data.probe(x, y)` | [L817–821](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L817-L821) | The cell under a point of the canvas. |
| `Sim.data.inspect(ref)` | [L822–827](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L822-L827) | Values of ψ, C, S, A (and r₁, a₁, φ₁ when there is a source) at a cell, with its centre. |
| `Sim.data.locate(name, idx)` | [L828–835](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L828-L835) | Where an array element is drawn: cell centre, source dot, column or row. |
| `Sim.data.check.*` | [L837–881](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L837-L881) | One function per variable: formula, stored inputs, recomputed value. |
| `Sim.data.drawn.psi`, `.psi_c`, `.u` | [L885–891](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L885-L891) | Read-back from the picture: the cell pixel, the centre cell, the screen pixel at a source dot. |
| `Sim.data.round.label`, `.length`, `.point` | [L893–894](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L893-L894) | What one recorded round is. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Pause / Play | `play` | starts playing unless the reader prefers reduced motion ([sim.js:178](../../public/scripts/sim.js#L178)) | `Sim.playButton` toggles the clock and relabels the button ([L768](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L768), [sim.js:200–208](../../public/scripts/sim.js#L200-L208)). |
| Line of 16 | `line` | — | Replaces the sources by 16 at x = 64 + 44.8 n px ([L720–724](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L720-L724)). |
| Add 5 random | `random` | — | Appends 5 sources between 133.3 and 666.7 px; the list keeps the newest 24 ([L725–729](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L725-L729), [L702](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L702)). |
| Reset | `reset` | — | ωt = 0 and two sources at 200 and 600 px ([L730–733](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L730-L733), [L513](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L513)). |
| Clear | `clear` | — | No sources ([L734](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L734)); the caption then reads "no sources · click the field" ([L709](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L709)). |
| Click on the field | `field` (canvas) | — | Adds a source at the clicked x ([L716–719](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L716-L719)). While Read values is on, `datalog.js` stops the click in the capture phase ([datalog.js:618–641](../../public/scripts/datalog.js#L618-L641)). Measured: with Read values on a click left N = 16; off, the same click made N = 17. |
| Wavelength λ | `lambda` | 16–64 px, step 1, default 30 ([L72](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L72)) | `changed()`: k and the maps are rebuilt ([L594](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L594), [L628](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L628)). |
| Frequency f | `freq` | 0.2–2 Hz, step 0.05, default 1.1 ([L76](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L76)) | `readouts()` only; enters through ωt ([L595](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L595), [L762](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L762)). |
| Damping γ | `damp` | 0–0.6, step 0.01, default 0.15 ([L80](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L80)) | `changed()`: g = γ/300 px and the maps are rebuilt ([L596](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L596), [L628](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L628)). |

Readouts: `r-n` shows the number of sources, with "(max)" at 24 ([L708](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L708)); `r-v` shows round(fλ) px/s ([L712](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L712)); `cap-count`
in the caption shows "2 sources" ([L709](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L709)). The legend's colour bar is the CSS gradient of [sim.css:128](../../public/styles/sim.css#L128).

## What the page writes into the data store

The store is created by `Sim.dataset({ title: 'Wave interference', attrs: {...} })` ([L526](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L526); see
[dataset.md](../scripts/dataset.md)). Its attributes are `figure: 1`, `page`, `WORLD_W: 800`, `R: 300`, `MAX_SOURCES: 24`,
`SOURCE_LIFT: 10` and `length_unit`. Dimensions: `s` (sources, resized in `precompute()`, [L632](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L632)), `j` and `i` (rows and columns,
set in `resize()`, [L609–610](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L609-L610)), `n = 256` and `c = 3` for the colour table ([L556–557](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L556-L557)). The running page holds 50 variables:
12 arrays and 38 scalars.

| Array | Dims, type | Written at |
|---|---|---|
| `u` (coordinate), `x_s` | (s), Float64 | [L638–639](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L638-L639), when sources change |
| `x`, `y` (coordinates) | (i), (j), Float64 | [L619–620](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L619-L620), in `resize()` |
| `C`, `S` | (j, i), Float32 | [L647–648](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L647-L648), at each rebuild |
| `A` | (j, i), Float32 | [L652](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L652) |
| `r1`, `a1`, `ph1` | (j, i), Float32 | [L646](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L646); source 1 is `sources[0]`, the oldest kept; zeroed when N = 0 ([L653](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L653)) |
| `psi` | (j, i), Float32 | [L666](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L666), every drawn frame |
| `LUT` | (n, c), Uint8Clamped | [L589](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L589), once |

Scalars, by the place that writes them:
- `readouts()`: `lambda`, `f`, `damp`, `v`, `omega`, `T` ([L712–711](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L712-L712)).
- `precompute()`: `k`, `g`, `N`, `norm`, `dx`, `dy`, `y_s` ([L631](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L631)); `builds`, `build_ms`, `trig_calls` ([L655](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L655)).
- `resize()`: `cols`, `rows`, `P`, `worldH`, `box_w`, `box_h`, `dpr`, `j_c`, `i_c` ([L621–623](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L621-L623)).
- `render()`: `cos_wt`, `sin_wt` ([L662](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L662)); `psi_c`, `n_c`, `rgb_c` ([L697](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L697)); `renders`, `draw_ms` ([L698](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L698)).
- clock callback: `t`, `dt`, `fps`, `frames`, `playing` ([L759](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L759)); `omegaT` ([L763](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L763)).

The panel spec `Sim.data` ([L798–897](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L798-L897); see [datalog.md](../scripts/datalog.md)) lists six groups ([L801–808](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L801-L808)), shades
ψ, C and S table cells with the page's own colour table and A, a₁ with `Sim.colourMap` ([L809–814](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L809-L814), [datalog.js:71–77](../../public/scripts/datalog.js#L71-L77)), and
saves as `fig1-wave-interference` ([L799](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L799)). Its `about` paragraph states what differs between store and picture ([L896](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L896)).

**One round** (`Sim.data.round`, [L893–894](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L893-L894)) is one period of the sources, T = 1/f, measured on the play time `t`. Columns
charted: `omegaT`, `cos_wt`, `sin_wt`, `psi_c`; the recorder also copies every numeric scalar. Unless the reader has pinned a
point, the round follows the cell j = ⌊rows/2⌋, i = ⌊0.72 cols⌋ ([L894](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L894), [datalog.js:766](../../public/scripts/datalog.js#L766)). The recorder keeps at most 600
samples, one every T/600 ([datalog.js:747](../../public/scripts/datalog.js#L747), [datalog.js:776](../../public/scripts/datalog.js#L776)). *Reset* sets ωt to 0 but not `t`, so it does not end a round.

**`Sim.live()`** ([L737–754](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L737-L754)) returns formatted strings under the keys `lam`, `k`, `g`, `N`, `norm`, `dx`, `grid`, `C`, `S`,
`c`, `s`, `psi`, `f`, `wt`, `v`, `idx`, `rgb`, `r`, `a`, `ph`, all read at the centre cell pc = j_c · cols + i_c. The walkthrough
polls it every 200 ms unless "Hold the numbers" is on ([sim.js:388–400](../../public/scripts/sim.js#L388-L400)).

**Proof, measured in this session** (1280 px window, paused, two default sources, centre cell; stored value against the
page's own `check` function, which recomputes in float64 from stored inputs):

| Variable | Stored − recomputed |
|---|---|
| C | 2.7 × 10⁻¹¹ |
| S | 1.4 × 10⁻⁸ |
| A | 2.0 × 10⁻⁸ |
| ψ | 2.5 × 10⁻⁹ |
| r₁ | −7.9 × 10⁻⁶ px (of 262.79 px) |
| a₁, φ₁ | 1.2 × 10⁻⁸, −5.3 × 10⁻⁸ rad |

These gaps are float32 storage rounding, nothing else. The pixel read back from the offscreen image was rgb(164, 158, 152),
identical to table row 79 for ψ = −0.3775; the screen pixel at source 1 was rgb(122, 31, 43), the burgundy dot.

## Page structure

**Head** ([L3–18](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L3-L18)): title "Wave Interference · Numa Koudsie" and description ([L6–7](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L6-L7)); preconnects to Google Fonts
([L9–10](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L9-L10)); stylesheets in order `../styles/sim.css`, `../styles/data.css`, `../styles/fold.css` ([L11–13](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L11-L13)), where `sim.css`
imports the fonts, KaTeX's CSS and `paper.css`; an inline SVG favicon ([L14](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L14)); one inline rule, `#field { cursor: crosshair; }`
([L15–17](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L15-L17)). See [styles.md](../styles.md).

**Body**, top to bottom:
- Top bar with "← All simulations" and the hand-written Fig. 1–10 links ([L20–35](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L20-L35)); a `<noscript>` message ([L38](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L38)).
- Heading: "Fig. 1 · wave optics · Huygens' principle", the title, the lede ([L39–43](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L39-L43)).
- The figure: `#stage` with aspect ratio 8 : 3.6, square below 900 px ([L47](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L47), [sim.css:68](../../public/styles/sim.css#L68), [sim.css:287–289](../../public/styles/sim.css#L287-L289)); the canvas
  `#field` ([L48](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L48)); the caption with `cap-count` ([L50–53](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L50-L53)). `datalog.js` adds the Read values switch to this caption and the
  reading strip under the stage ([datalog.js:570–594](../../public/scripts/datalog.js#L570-L594)).
- The control panel ([L56–95](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L56-L95)): Sources buttons, Waves sliders, the legend with colour bar, the readouts.
- The lecture note `<article class="paper" id="paper">` ([L98–495](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L98-L495)), summarised below.
- The walkthrough host `<section class="walk" id="walk" data-walk="circles">` ([L497](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L497)).
- Footer ([L500–503](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L500-L503)).
- Scripts in load order: `../scripts/fold.js`, `../scripts/sim.js`, `../scripts/dataset.js` ([L505–507](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L505-L507)), the page's own script
  ([L508–903](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L508-L903)), then `../scripts/datalog.js` ([L904](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L904)). `sim.js` loads `../scripts/walk/circles.js` from the `data-walk` key once
  the DOM is ready ([sim.js:476–486](../../public/scripts/sim.js#L476-L486)) and KaTeX for the note ([sim.js:413–442](../../public/scripts/sim.js#L413-L442)). See [sim.md](../scripts/sim.md),
  [fold.md](../scripts/fold.md), [walk.md](../scripts/walk.md), [pages.md](../pages.md).

**Walkthrough** ([circles.js](../../public/scripts/walk/circles.js), 7 steps). Each step quotes page lines; a script run in
this session confirmed that every quoted line is identical, after trimming indentation, to the page line listed.

| Step | Title | Page lines quoted |
|---|---|---|
| 1 | Wave number and damping | [L628–629](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L628-L629) |
| 2 | Distance from a source to a grid point | [L630](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L630), [L641](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L641), [L643–644](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L643-L644) |
| 3 | Amplitude and phase from one source | [L645](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L645) |
| 4 | Two maps that hold all of space | [L647–648](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L647-L648) |
| 5 | The field at this instant | [L660](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L660), [L664–665](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L664-L665) |
| 6 | The clock | [L762](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L762), [L712](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L712) |
| 7 | A number becomes a colour | [L588–589](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L588-L589), [L667](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L667) |

**Lecture note** "Circular waves that add up to a straight one": abstract ([L103](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L103)), contents ([L106–120](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L106-L120)), ten sections, 19
numbered display equations (1)–(19), four inline SVG figures, two exercises, one summary box and four references. Sections 3, 6
and 7.1 carry ★ (heavier mathematics).

| § | id | Title | Lines | Equations | Figures, boxes |
|---|---|---|---|---|---|
| 1 | `p-pond` | Pebbles in a row | [L122–186](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L122-L186) | — | Figure 1, Huygens' construction for nine sources ([L128–185](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L128-L185)) |
| 2 | `p-model` | The model | [L188–263](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L188-L263) | (1) wave equation, (2) distance | Figure 2, page coordinates and path difference s sin θ ([L203–262](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L203-L262)) |
| 3 | `p-ring` | One source, one ring ★ | [L265–276](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L265-L276) | (3) Bessel, (4) far field, (5) the page's ring | §3.1 ([L272](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L272)) |
| 4 | `p-add` | Adding the rings | [L278–288](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L278-L288) | (6) sum, (7) phasors C + iS, (8) v = fλ | — |
| 5 | `p-two` | Two sources: calm hyperbolae | [L290–302](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L290-L302) | (9), (10) calm lines | Exercise 5.1 |
| 6 | `p-row` | A row: one beam and its side beams ★ | [L304–375](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L304-L375) | (11)–(14) array factor, grating lobes, steering | Figure 3, far-field \|F\| of Line of 16 ([L314–363](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L314-L363)); box; Exercise 6.1 |
| 7 | `p-front` | Near the row: the front straightens | [L377–448](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L377-L448) | (15) Fraunhofer, (16)–(17) Fresnel zone | Figure 4, A along the centre row ([L383–439](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L383-L439)); §7.1 ★ ([L441](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L441)) |
| 8 | `p-numerics` | Two maps and a turning phase | [L450–462](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L450-L462) | (18) C and S | — |
| 9 | `p-screen` | From numbers to colours | [L464–472](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L464-L472) | (19) colour table | — |
| 10 | `p-limits` | What the model leaves out | [L474–492](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L474-L492) | — | §10.1 Further reading ([L485–491](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L485-L491)) |

The plotted curves of Figures 3 and 4 are single SVG paths of 10–23 kB each on one line ([L349–350](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L349-L350), [L422–425](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L422-L425)).

## Where the drawing and the store differ

- **Colour steps.** ψ reaches the screen through 256 colours, one step Δψ = 2/255 ≈ 0.0078 ([L667](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L667)); the store keeps float32,
  about seven significant figures ([L551](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L551)). The page says so in `about` ([L896](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L896)) and in the note ([L469](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L469)).
- **Tone curve.** Colours follow |ψ|^0.8, which lifts small values ([L588](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L588)). The legend's colour bar is a straight linear
  gradient between the same three colours ([sim.css:128](../../public/styles/sim.css#L128)), so its mid-tones are slightly paler than the field's.
- **Smoothing.** The image has one pixel per cell and is stretched over the canvas with smoothing ([L674–676](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L674-L676)); a screen pixel
  near a cell edge is a blend of neighbours. `pixelCheck` reads the offscreen image, which is exact, and reports the blended
  screen pixel only as a note ([L789–797](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L789-L797)).
- **Only ψ is drawn.** C, S, A, r₁, a₁ and φ₁ are stored but not painted ([L664–671](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L664-L671)); the note says the amplitude A is not
  drawn ([L470](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L470)).
- **Source dots.** Each source covers the field under a cream glow of radius 20 px and a 5.5 px dot ([L681–694](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L681-L694)).
- **Clipping.** ψ is clipped to [−1, 1] before storing and drawing ([L665](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L665)); this only guards rounding, since |ψ| ≤ 1 already.

## How to change it safely

- **Walkthrough excerpts.** `circles.js` quotes [L588–589](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L588-L589), [L628–630](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L628-L630), [L641](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L641), [L643–645](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L643-L645), [L647–648](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L647-L648), [L660](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L660),
  [L664–665](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L664-L665), [L667](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L667), [L712](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L712) and [L762](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L762). Keep these lines character for character, or change `circles.js` in the same edit.
  Insert new store taps after a quoted line, never inside a quoted pair (AGENTS.md).
- **`Sim.live()` keys** must match the `syms` keys of `circles.js` (listed above). A missing key shows "—".
- **Formulas live in several places.** The grid formula is in `resize()` ([L602–603](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L602-L603)), in the store attributes ([L559–560](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L559-L560)),
  in `check.cols` / `check.rows` ([L877–878](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L877-L878)) and in the note §8 ([L458](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L458)). The colour table's three colours are in the builder
  ([L586](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L586)), in `check.LUT` ([L870](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L870)), in `datalog.js` `NEG`/`MID`/`POS` ([datalog.js:70](../../public/scripts/datalog.js#L70)), in the expected dot colour of
  `drawn.u` ([L889](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L889)) and in the colour bar ([sim.css:128](../../public/styles/sim.css#L128)). The sum is in `precompute()` and again in `sumAt()` ([L776–787](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L776-L787));
  change both.
- **Numbers quoted by the note** come from the code: R = 300 px (eq. 5), the 10 px lift, the defaults 30 px / 1.1 Hz / 0.15, the
  presets 200/600 px and 64–736 px, the cap of 24. Change the note with them.
- **The catalog** entry's `equation`, `model`, `method` and `controls` ([catalog.js:56–59](../../public/scripts/catalog.js#L56-L59)) describe this page.
- **Re-test** after any change: open the Data panel and press Check on C, S, A, ψ, r1 (stored, recomputed, pixel); switch Read
  values on, pin a cell, confirm a click does not add a source, switch it off and confirm it does; record one round; watch the
  walkthrough's Now column update; resize between 390 px and 1440 px.

## Notes for maintainers

1. Fixed on 2026-10-15: §8 now gives the measured 360 × 162 desktop and 324 × 324 phone grids, 7.2 and 6.48 samples per shortest wavelength, and 1 866 240 trigonometric calls for 16 sources (commit `:/^Batch B: correct notes and layout; verify measured figures in Chromium$`).
2. Fixed on 2026-10-15: the walkthrough consistently uses γ for the slider and g = γ/R for attenuation per pixel (commit `:/^Batch C: align walkthroughs and metadata; verify excerpts and stored values$`).
3. Fixed on 2026-10-15: the speed readout reads stored v and its walkthrough quotes that line (commit `:/^Batch D: store computed results once; verify values and pixel readbacks$`).
4. Fixed on 2026-10-15: the source-dot readback checks alpha before RGB (commit `:/^Batch D: store computed results once; verify values and pixel readbacks$`).
5. **Apostrophe.** The catalog `subject` uses "Huygens’" ([catalog.js:54](../../public/scripts/catalog.js#L54)); the page's subject line uses a straight
   apostrophe ([L40](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L40)).
