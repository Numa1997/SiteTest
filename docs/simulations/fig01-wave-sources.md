# Fig. 1 · Wave Interference

| | |
|---|---|
| Page | [public/simulations/Circular Wave Interference Visualization.html](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html) (907 lines, 192 669 bytes) |
| Walkthrough | [public/scripts/walk/circles.js](../../public/scripts/walk/circles.js) (110 lines, key `circles`) |
| Thumbnail | [public/images/sims/wave-sources.webp](../../public/images/sims/wave-sources.webp) (WebP, 800 × 500 px, 36.5 kB; a still of the two-source field) |
| Catalog entry | [public/scripts/catalog.js#L48](../../public/scripts/catalog.js#L48) (`id: 'wave-sources'`, `fig: 1`, `field: 'optics'`, `stage: 1`, lines 47–63) |

Links written `Lnnn` point into the page file; links to other files carry the file name.

The reader sees a wide field of cream, burgundy and dark-ink bands: the height ψ of a water surface at this instant, around
point sources that sit on one line 10 px above the bottom edge ([L48–49](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L48-L49), [L513](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L513)). The page opens with two sources at
x = 200 and 600 px ([L514](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L514)) and each source's rings run outward at the speed v = fλ (where rings cross at an angle, the crests of their sum run faster; note §4). A click on the field adds a source at that
horizontal position ([L717–720](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L717-L720)); buttons give a row of 16, five random sources, the two defaults, or none
([L60–66](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L60-L66)); three sliders set the wavelength, frequency and damping ([L71–82](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L71-L82)). Under the figure sit the Data panel and
the Read values switch (added by `datalog.js`), the walkthrough "From symbols to code" ([L498](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L498)) and the lecture note
([L99–496](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L99-L496)).

## The physics in one picture

**Everyday picture.** Throw a handful of pebbles into a pond in a line, all at once. Each makes a ring. Where a crest of one
ring meets a crest of another the water rises higher; where a crest meets a trough it stays flat. A little way off, the rings of
a dense row merge into one straight ripple: Huygens' principle ([L125–127](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L125-L127)).

**Model.** The water height ψ(x, y, t) obeys the two-dimensional wave equation, which is linear, so the waves of several sources
simply add ([L192–192](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L192-L192)). The page measures lengths in pixels of a field that is always 800 px wide and fixes no scale in metres
([L194](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L194)); time is in seconds. All sources oscillate in step at one frequency, the medium is non-dispersive, the edges do not
reflect, and the sources do not disturb each other ([L197–202](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L197-L202)). Instead of the true $1/\sqrt{r}$ fall-off of a ring the page uses
an exponential damping that stays finite at the source (note §3.1, [L274–276](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L274-L276)).

**What the code evaluates.** For a grid point at the centre of cell (j, i), with $\Delta x = 800/\text{cols}$ and
$\Delta y = \text{worldH}/\text{rows}$ ([L631](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L631)):

$$x = \left(i + \tfrac12\right)\Delta x, \qquad y = \left(j + \tfrac12\right)\Delta y, \qquad r_s = \sqrt{(x - x_s)^2 + (y - y_s)^2}$$

([L642–645](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L642-L645)). Each source contributes an amplitude and a phase ([L629–630](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L629-L630), [L646](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L646)):

$$a_s = \frac{e^{-g r_s}}{N}, \qquad g = \frac{\gamma}{R}, \qquad R = 300\ \text{px}, \qquad \varphi_s = k r_s, \qquad k = \frac{2\pi}{\lambda}.$$

Because every source shares one angular frequency ω, the time dependence factors out of the sum exactly (note eq. 18,
[L453–455](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L453-L455)). The page builds two time-independent maps and the amplitude ([L648–649](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L648-L649), [L653](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L653)):

$$C = \sum_s a_s \cos k r_s, \qquad S = \sum_s a_s \sin k r_s, \qquad A = \sqrt{C^2 + S^2},$$

and on every frame forms the field from one shared phase ([L661](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L661), [L665–666](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L665-L666), [L763](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L763)):

$$\psi = C\cos\omega t + S\sin\omega t, \quad \text{clipped to } [-1, 1], \qquad \omega t \leftarrow \omega t + 2\pi f\,\Delta t .$$

This is $\psi = \frac{1}{N}\sum_s e^{-g r_s}\cos(k r_s - \omega t)$, the note's eqs. (5)–(7). The speed readout is
$v = f\lambda$ ([L713](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L713), [L712](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L712)). The colour of a cell is row $n = \operatorname{round}(127.5\,\psi + 127.5)$ of a 256-entry table
whose channels are $c = c_0 + (c_\pm - c_0)\,|\psi|^{0.8}$ ([L589–590](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L589-L590), [L668](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L668); note eq. 19).

| Symbol | Code | Unit | Meaning |
|---|---|---|---|
| $x, y$ | `xs[q]`, `ys[q]` | px of the field | cell centre, from the top-left corner, y downward ([L620–621](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L620-L621)) |
| $x_s$ | `sources[s] * WORLD_W` | px | source position; the list stores fractions $u_s$ of the width ([L638](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L638)) |
| $y_s$ | `sy = worldH - SOURCE_LIFT` | px | height of every source, 10 px above the bottom ([L631](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L631)) |
| $r_s$ | `r` | px | distance from cell to source ([L645](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L645)) |
| $\lambda$ | `lambda.value` | px | wavelength (slider) |
| $k$ | `k` | rad/px | wave number $2\pi/\lambda$ ([L629](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L629)) |
| $\gamma$ | `damp.value` | 1 (e-foldings over $R$) | damping (slider) |
| $g$ | `g` | 1/px | attenuation per pixel $\gamma/R$ ([L629](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L629)) |
| $N$ | `n`, `norm = 1/max(1, n)` | 1 | number of sources, at most 24 ([L630](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L630), [L513](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L513)) |
| $f$, $\omega$ | `freq.value`, `2π f` | Hz, rad/s | frequency (slider) and angular frequency ([L712](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L712)) |
| $\omega t$ | `omegaT` | rad | shared phase, accumulated, never wrapped ([L763](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L763)) |
| $\Delta t$ | `dt` | s | real time between frames, capped at 0.05 s ([sim.js:179](../../public/scripts/sim.js#L179)) |
| $C, S, A, \psi$ | `sumC`, `sumS`, `ampl`, `psi` | 1 | the maps and the field, $\lvert\psi\rvert \le 1$ |

## How the code computes it

**State.** `sources` is an array of fractions $u_s$ of the width, newest 24 kept ([L521](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L521), [L703](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L703)). `omegaT` is the shared
phase; `dirty` asks for a rebuild of the maps, `redraw` for one more picture while paused ([L522](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L522)). `cols`, `rows`, `worldH` give
the grid ([L520](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L520)). The maps `sumC`, `sumS`, `ampl`, the field `psi` and the source-1 maps `r1`, `a1`, `ph1` are Float32 arrays
owned by the data store and handed out by `ds.alloc` ([L612–618](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L612-L618)). `off` is an offscreen canvas with one pixel per cell, `img` its
ImageData with alpha preset to 255 ([L519](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L519), [L606–609](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L606-L609)). `LUT` is the 256 × 3 colour table ([L585](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L585)).

**Method.** A closed form, not a time integration. Space and time separate exactly, so the expensive part (one `sqrt`, `exp`,
`cos` and `sin` per source per cell) runs only when the geometry changes, and a frame costs two multiplications and one addition
per cell whatever N is ([L665](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L665)). There is no stability question. The only time error is the 0.05 s cap on Δt
([sim.js:179](../../public/scripts/sim.js#L179)): on a slow device the pattern runs slower, it is not distorted.

**Frame loop** (`Sim.clock` callback, [L757–768](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L757-L768)), in order:
1. Keep the play time, count frames, smooth the frame rate as fps ← fps + (1/Δt − fps)/10 ([L758–759](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L758-L759)); store `t`, `dt`,
   `fps`, `frames`, `playing` ([L760](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L760)).
2. If `dirty`, run `precompute()` and ask for a redraw ([L761](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L761)).
3. If playing (Δt > 0) or a redraw is pending: advance `omegaT` by 2πfΔt ([L763](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L763)), store it ([L764](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L764)), `render()` ([L765](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L765)).

`Sim.clock` calls the callback on every animation frame, with Δt = 0 while paused ([sim.js:175–185](../../public/scripts/sim.js#L175-L185)); a paused page therefore
draws nothing unless a slider or button asked for a redraw.

**`precompute()`** ([L628–658](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L628-L658)): computes `k`, `g`, `n`, `norm`, `dx`, `dy`, `sy` and stores them ([L629–632](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L629-L632)); resizes
dimension `s` and allocates `u`, `x_s` ([L633–634](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L633-L634)); zeroes `sumC`, `sumS` ([L635–636](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L635-L636)); loops sources, then rows, then
columns, accumulating $a\cos\varphi$ and $a\sin\varphi$ and keeping $r$, $a$, $\varphi$ of the first source ([L637–652](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L637-L652)); fills
`A` ([L653](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L653)); zeroes the source-1 maps when there is no source ([L654](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L654)); marks the arrays changed and records build count, time
and the number of `cos` + `sin` calls, 2NP ([L655–656](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L655-L656)).

**`render()`** ([L660–700](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L660-L700)): takes cos ωt and sin ωt once ([L661](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L661)); for every cell forms ψ, clips it, stores it, picks the
colour row and writes RGB into `img` ([L664–673](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L664-L673)); puts the small image on `off` and stretches it over the canvas with
`imageSmoothingQuality = 'high'` ([L674–677](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L674-L677)); paints each source as a cream glow of radius 20 px and a burgundy dot of radius
5.5 px with a 2 px cream rim ([L679–696](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L679-L696)); stores the centre-cell value, its colour row and colour, the render count and time
([L697–699](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L697-L699)).

**Precomputation and caching.**
- The colour table is built once at start-up ([L586–593](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L586-L593)).
- The maps are rebuilt only when `dirty` is set: by λ and γ through `changed()` ([L595](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L595), [L597](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L597), [L599](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L599)), by any source change
  through `setSources()` ([L702–705](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L702-L705)) and by `resize()` ([L625](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L625)). `changed()` only sets the flag, so several slider events
  within one frame cost one rebuild. The frequency slider calls `readouts()` only ([L596](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L596)): f changes the speed of the
  pattern, never its shape.
- Grid size: cols = clamp(round(box.w/1.1), 60, 360), rows = max(30, round(cols · box.h/box.w)), worldH = 800 · box.h/box.w
  ([L603–605](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L603-L605)). Resizes are debounced by 80 ms ([sim.js:141–149](../../public/scripts/sim.js#L141-L149), [L902](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L902)).

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

All functions live in the one inline script ([L509–904](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L509-L904)), wrapped in an immediately invoked function ([L510](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L510)).

| Function | Lines | What it does |
|---|---|---|
| colour-table builder (anonymous) | [L586–592](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L586-L592) | Fills `LUT`: for row i, a = i/127.5 − 1, s = \|a\|^0.8, each channel `mid + (end − mid) · s`, end = ink for a < 0, burgundy otherwise. |
| slider `format` callbacks | [L595–597](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L595-L597) | Text for the `<output>` beside each slider: "30 px", "1.10 Hz", "0.15". |
| `changed()` | [L599](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L599) | Marks the maps stale and refreshes the readouts. |
| `resize()` | [L601–626](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L601-L626) | Fits the canvas, sets the grid, sizes the offscreen image, reallocates every grid array in the store, writes cell-centre coordinates and grid scalars, marks the maps stale. |
| `precompute()` | [L628–658](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L628-L658) | Builds C, S, A and the source-1 maps (see above). |
| `render()` | [L660–700](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L660-L700) | Turns C, S and ωt into ψ and pixels; draws the source dots. |
| `setSources(list)` | [L702–705](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L702-L705) | Keeps the newest 24 entries and calls `changed()`. |
| `readouts()` | [L707–715](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L707-L715) | Writes source count, caption count and speed into the DOM; stores λ, f, γ, v, ω, T; asks for a redraw. |
| canvas `click` handler | [L717–720](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L717-L720) | Adds a source at the clicked fraction of the width. |
| *Line of 16* handler | [L721–725](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L721-L725) | Sixteen sources at u = 0.08 + 0.84 n/15. |
| *Add 5 random* handler | [L726–730](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L726-L730) | Appends five at u uniform in [1/6, 5/6]. |
| *Reset* handler | [L731–734](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L731-L734) | ωt = 0, sources back to `DEFAULT`. |
| *Clear* handler | [L735](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L735) | Empty source list. |
| `Sim.live()` | [L738–755](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L738-L755) | Strings for the walkthrough's "Now" column, read from the store at the centre cell. |
| clock callback | [L757–768](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L757-L768) | The frame loop above. |
| `cellIndex(j, i)` | [L772](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L772) | Flat index j · cols + i. |
| `cellCentre(j, i)` | [L773](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L773) | Cell centre in css px of the canvas. |
| `lut(v)` | [L774](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L774) | Colour-table entry for a value, for shading table cells in the panel. |
| `sliderCheck(input, label)` | [L774](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L774) | Check record for a slider value. |
| `sumAt(p, trig)` | [L777–788](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L777-L788) | Re-sums one cell from stored inputs (`x`, `y`, `k`, `g`, `norm`, `x_s`, `y_s`) for the C and S checks. |
| `pixelCheck(p)` | [L790–798](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L790-L798) | Reads pixel (i, j) of the offscreen image and compares it with the table row for the stored ψ; also reports the screen pixel at the cell centre. |
| `Sim.data.playing`, `.play` | [L801](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L801), [L896](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L896) | Clock state and start, for the panel's round recorder. |
| `Sim.data.probe(x, y)` | [L818–822](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L818-L822) | The cell under a point of the canvas. |
| `Sim.data.inspect(ref)` | [L823–828](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L823-L828) | Values of ψ, C, S, A (and r₁, a₁, φ₁ when there is a source) at a cell, with its centre. |
| `Sim.data.locate(name, idx)` | [L829–836](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L829-L836) | Where an array element is drawn: cell centre, source dot, column or row. |
| `Sim.data.check.*` | [L838–882](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L838-L882) | One function per variable: formula, stored inputs, recomputed value. |
| `Sim.data.drawn.psi`, `.psi_c`, `.u` | [L886–892](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L886-L892) | Read-back from the picture: the cell pixel, the centre cell, the screen pixel at a source dot. |
| `Sim.data.round.label`, `.length`, `.point` | [L895–895](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L895-L895) | What one recorded round is. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Pause / Play | `play` | starts playing unless the reader prefers reduced motion ([sim.js:177](../../public/scripts/sim.js#L177)) | `Sim.playButton` toggles the clock and relabels the button ([L769](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L769), [sim.js:199–207](../../public/scripts/sim.js#L199-L207)). |
| Line of 16 | `line` | — | Replaces the sources by 16 at x = 64 + 44.8 n px ([L721–725](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L721-L725)). |
| Add 5 random | `random` | — | Appends 5 sources between 133.3 and 666.7 px; the list keeps the newest 24 ([L726–730](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L726-L730), [L703](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L703)). |
| Reset | `reset` | — | ωt = 0 and two sources at 200 and 600 px ([L731–734](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L731-L734), [L514](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L514)). |
| Clear | `clear` | — | No sources ([L735](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L735)); the caption then reads "no sources · click the field" ([L709](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L709)). |
| Click on the field | `field` (canvas) | — | Adds a source at the clicked x ([L717–720](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L717-L720)). While Read values is on, `datalog.js` stops the click in the capture phase ([datalog.js:924–947](../../public/scripts/datalog.js#L924-L947)). Measured: with Read values on a click left N = 16; off, the same click made N = 17. |
| Wavelength λ | `lambda` | 16–64 px, step 1, default 30 ([L73](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L73)) | `changed()`: k and the maps are rebuilt ([L595](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L595), [L629](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L629)). |
| Frequency f | `freq` | 0.2–2 Hz, step 0.05, default 1.1 ([L77](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L77)) | `readouts()` only; enters through ωt ([L596](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L596), [L763](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L763)). |
| Damping γ | `damp` | 0–0.6, step 0.01, default 0.15 ([L81](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L81)) | `changed()`: g = γ/300 px and the maps are rebuilt ([L597](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L597), [L629](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L629)). |

Readouts: `r-n` shows the number of sources, with "(max)" at 24 ([L708](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L708)); `r-v` shows the stored `v` rounded, in px/s ([L713](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L713)); `cap-count`
in the caption shows "2 sources" ([L709](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L709)). The legend's colour bar is the CSS gradient of [sim.css:128](../../public/styles/sim.css#L128).

## What the page writes into the data store

The store is created by `Sim.dataset({ title: 'Wave interference', attrs: {...} })` ([L527](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L527); see
[dataset.md](../scripts/dataset.md)). Its attributes are `figure: 1`, `page`, `WORLD_W: 800`, `R: 300`, `MAX_SOURCES: 24`,
`SOURCE_LIFT: 10` and `length_unit`. Dimensions: `s` (sources, resized in `precompute()`, [L633](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L633)), `j` and `i` (rows and columns,
set in `resize()`, [L610–611](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L610-L611)), `n = 256` and `c = 3` for the colour table ([L557–558](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L557-L558)). The running page holds 50 variables:
12 arrays and 38 scalars.

| Array | Dims, type | Written at |
|---|---|---|
| `u` (coordinate), `x_s` | (s), Float64 | [L639–640](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L639-L640), when sources change |
| `x`, `y` (coordinates) | (i), (j), Float64 | [L620–621](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L620-L621), in `resize()` |
| `C`, `S` | (j, i), Float32 | [L648–649](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L648-L649), at each rebuild |
| `A` | (j, i), Float32 | [L653](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L653) |
| `r1`, `a1`, `ph1` | (j, i), Float32 | [L647](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L647); source 1 is `sources[0]`, the oldest kept; zeroed when N = 0 ([L654](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L654)) |
| `psi` | (j, i), Float32 | [L667](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L667), every drawn frame |
| `LUT` | (n, c), Uint8Clamped | [L590](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L590), once |

Scalars, by the place that writes them:
- `readouts()`: `lambda`, `f`, `damp`, `v`, `omega`, `T` ([L711–712](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L711-L712)). `v` = f λ, the phase speed in px/s, is declared at [L541](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L541) and written at [L712](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L712); the `r-v` readout shows it rounded, read back from the store ([L713](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L713)), and the walkthrough quotes that line.
- `precompute()`: `k`, `g`, `N`, `norm`, `dx`, `dy`, `y_s` ([L632](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L632)); `builds`, `build_ms`, `trig_calls` ([L656](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L656)).
- `resize()`: `cols`, `rows`, `P`, `worldH`, `box_w`, `box_h`, `dpr`, `j_c`, `i_c` ([L622–624](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L622-L624)).
- `render()`: `cos_wt`, `sin_wt` ([L663](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L663)); `psi_c`, `n_c`, `rgb_c` ([L698](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L698)); `renders`, `draw_ms` ([L699](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L699)).
- clock callback: `t`, `dt`, `fps`, `frames`, `playing` ([L760](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L760)); `omegaT` ([L764](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L764)).

The panel spec `Sim.data` ([L799–898](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L799-L898); see [datalog.md](../scripts/datalog.md)) lists six groups ([L802–809](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L802-L809)), shades
ψ, C and S table cells with the page's own colour table and A, a₁ with `Sim.colourMap` ([L810–815](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L810-L815), [datalog.js:103–109](../../public/scripts/datalog.js#L103-L109)), and
saves as `fig1-wave-interference` ([L799](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L799)). Its `about` paragraph states what differs between store and picture ([L896](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L896)).

**One round** (`Sim.data.round`, [L895–895](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L895-L895)) is one period of the sources, T = 1/f, measured on the play time `t`. Columns
charted: `omegaT`, `cos_wt`, `sin_wt`, `psi_c`; the recorder also copies every numeric scalar. Unless the reader has pinned a
point, the round follows the cell j = ⌊rows/2⌋, i = ⌊0.72 cols⌋ ([L895](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L895), [datalog.js:1071](../../public/scripts/datalog.js#L1071)). The recorder keeps at most 600
samples, one every T/600 ([datalog.js:1052](../../public/scripts/datalog.js#L1052), [datalog.js:1081](../../public/scripts/datalog.js#L1081)). *Reset* sets ωt to 0 but not `t`, so it does not end a round.

**`Sim.live()`** ([L738–755](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L738-L755)) returns formatted strings under the keys `lam`, `k`, `g`, `N`, `norm`, `dx`, `grid`, `C`, `S`,
`c`, `s`, `psi`, `f`, `wt`, `v`, `idx`, `rgb`, `r`, `a`, `ph`, all read at the centre cell pc = j_c · cols + i_c. The walkthrough
polls it every 200 ms unless "Hold the numbers" is on ([sim.js:391–403](../../public/scripts/sim.js#L391-L403)).

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

**Head** ([L3–18](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L3-L18)): title "Wave Interference · Numa Koudsie" and description ([L8–9](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L8-L9)); the security policy and referrer rule
([L5–6](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L5-L6), see [build-and-deploy.md](../build-and-deploy.md#security)); stylesheets in order `../styles/sim.css`, `../styles/data.css`, `../styles/fold.css` ([L11–12](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L11-L12)), where `sim.css`
imports the self-hosted fonts, KaTeX's CSS and `paper.css`; an inline SVG favicon ([L14](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L14)); one inline rule, `#field { cursor: crosshair; }`
([L15–17](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L15-L17)). See [styles.md](../styles.md).

**Body**, top to bottom:
- Top bar: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`, 87 × 48) and
  "← All simulations" ([L21](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L21)), then the hand-written Fig. 1–10 links ([L20–36](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L20-L36)); a `<noscript>` message ([L39](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L39)).
- Heading: "Fig. 1 · wave optics · Huygens' principle", the title, the lede ([L40–44](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L40-L44)).
- The figure: `#stage` with aspect ratio 8 : 3.6, square below 900 px ([L48](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L48), [sim.css:68](../../public/styles/sim.css#L68), [sim.css:213–215](../../public/styles/sim.css#L213-L215)); the canvas
  `#field` ([L49](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L49)); the caption with `cap-count` ([L51–54](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L51-L54)). `datalog.js` adds the Read values switch to this caption and the
  reading strip under the stage ([datalog.js:874–898](../../public/scripts/datalog.js#L874-L898)).
- The control panel ([L57–96](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L57-L96)): Sources buttons, Waves sliders, the legend with colour bar, the readouts.
- The lecture note `<article class="paper" id="paper">` ([L99–496](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L99-L496)), summarised below.
- The walkthrough host `<section class="walk" id="walk" data-walk="circles">` ([L498](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L498)).
- Footer ([L501–504](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L501-L504)).
- Scripts in load order: `../scripts/fold.js`, `../scripts/sim.js`, `../scripts/dataset.js` ([L506–508](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L506-L508)), the page's own script
  ([L509–904](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L509-L904)), then `../scripts/datalog.js` ([L905](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L905)). `sim.js` loads `../scripts/walk/circles.js` from the `data-walk` key once
  the DOM is ready ([sim.js:481–490](../../public/scripts/sim.js#L481-L490)) and KaTeX for the note ([sim.js:418–447](../../public/scripts/sim.js#L418-L447)). See [sim.md](../scripts/sim.md),
  [fold.md](../scripts/fold.md), [walk.md](../scripts/walk.md), [pages.md](../pages.md).

**Walkthrough** ([circles.js](../../public/scripts/walk/circles.js), 7 steps). Each step quotes page lines; a script run in
this session confirmed that every quoted line is identical, after trimming indentation, to the page line listed.

| Step | Title | Page lines quoted |
|---|---|---|
| 1 | Wave number and damping | [L629–630](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L629-L630) |
| 2 | Distance from a source to a grid point | [L631](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L631), [L642](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L642), [L644–645](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L644-L645) |
| 3 | Amplitude and phase from one source | [L646](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L646) |
| 4 | Two maps that hold all of space | [L648–649](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L648-L649) |
| 5 | The field at this instant | [L661](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L661), [L665–666](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L665-L666) |
| 6 | The clock | [L763](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L763), [L713](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L713) |
| 7 | A number becomes a colour | [L589–590](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L589-L590), [L668](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L668) |

**Lecture note** "Circular waves that add up to a straight one": abstract ([L104](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L104)), contents ([L107–121](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L107-L121)), ten sections, 19
numbered display equations (1)–(19), four inline SVG figures, two exercises, one summary box and five references, each linked to the publisher, a lending copy or an online edition. Sections 3, 6
and 7.1 carry ★ (heavier mathematics).

| § | id | Title | Lines | Equations | Figures, boxes |
|---|---|---|---|---|---|
| 1 | `p-pond` | Pebbles in a row | [L123–187](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L123-L187) | — | Figure 1, Huygens' construction for nine sources ([L129–186](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L129-L186)) |
| 2 | `p-model` | The model | [L189–264](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L189-L264) | (1) wave equation, (2) distance | Figure 2, page coordinates and path difference s sin θ ([L204–263](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L204-L263)) |
| 3 | `p-ring` | One source, one ring ★ | [L266–277](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L266-L277) | (3) Bessel, (4) far field, (5) the page's ring | §3.1 ([L273](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L273)) |
| 4 | `p-add` | Adding the rings | [L279–289](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L279-L289) | (6) sum, (7) phasors C + iS, (8) v = fλ | — |
| 5 | `p-two` | Two sources: calm hyperbolae | [L291–303](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L291-L303) | (9), (10) calm lines | Exercise 5.1 |
| 6 | `p-row` | A row: one beam and its side beams ★ | [L305–376](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L305-L376) | (11)–(14) array factor, grating lobes, steering | Figure 3, far-field \|F\| of Line of 16 ([L315–364](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L315-L364)); box; Exercise 6.1 |
| 7 | `p-front` | Near the row: the front straightens | [L378–449](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L378-L449) | (15) Fraunhofer, (16)–(17) Fresnel zone | Figure 4, A along the centre row ([L384–440](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L384-L440)); §7.1 ★ ([L442](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L442)) |
| 8 | `p-numerics` | Two maps and a turning phase | [L451–463](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L451-L463) | (18) C and S | — |
| 9 | `p-screen` | From numbers to colours | [L465–473](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L465-L473) | (19) colour table | — |
| 10 | `p-limits` | What the model leaves out | [L475–493](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L475-L493) | — | §10.1 Further reading ([L486–492](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L486-L492)) |

The plotted curves of Figures 3 and 4 are single SVG paths of 10–23 kB each on one line ([L350–351](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L350-L351), [L423–426](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L423-L426)).

## Where the drawing and the store differ

- **Colour steps.** ψ reaches the screen through 256 colours, one step Δψ = 2/255 ≈ 0.0078 ([L668](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L668)); the store keeps float32,
  about seven significant figures ([L552](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L552)). The page says so in `about` ([L896](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L896)) and in the note ([L470](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L470)).
- **Tone curve.** Colours follow |ψ|^0.8, which lifts small values ([L589](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L589)). The legend's colour bar is a straight linear
  gradient between the same three colours ([sim.css:128](../../public/styles/sim.css#L128)), so its mid-tones are slightly paler than the field's.
- **Smoothing.** The image has one pixel per cell and is stretched over the canvas with smoothing ([L675–677](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L675-L677)); a screen pixel
  near a cell edge is a blend of neighbours. `pixelCheck` reads the offscreen image, which is exact, and reports the blended
  screen pixel only as a note ([L790–798](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L790-L798)).
- **Only ψ is drawn.** C, S, A, r₁, a₁ and φ₁ are stored but not painted ([L665–672](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L665-L672)); the note says the amplitude A is not
  drawn ([L471](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L471)).
- **Source dots.** Each source covers the field under a cream glow of radius 20 px and a 5.5 px dot ([L682–695](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L682-L695)).
- **Clipping.** ψ is clipped to [−1, 1] before storing and drawing ([L666](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L666)); this only guards rounding, since |ψ| ≤ 1 already.

## How to change it safely

- **Walkthrough excerpts.** `circles.js` quotes [L589–590](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L589-L590), [L629–631](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L629-L631), [L642](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L642), [L644–646](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L644-L646), [L648–649](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L648-L649), [L661](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L661),
  [L665–666](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L665-L666), [L668](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L668), [L713](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L713) and [L763](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L763). Keep these lines character for character, or change `circles.js` in the same edit.
  Insert new store taps after a quoted line, never inside a quoted pair (AGENTS.md).
- **`Sim.live()` keys** must match the `syms` keys of `circles.js` (listed above). A missing key shows "—".
- **Formulas live in several places.** The grid formula is in `resize()` ([L603–604](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L603-L604)), in the store attributes ([L560–561](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L560-L561)),
  in `check.cols` / `check.rows` ([L878–879](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L878-L879)) and in the note §8 ([L458](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L458)). The colour table's three colours are in the builder
  ([L587](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L587)), in `check.LUT` ([L871](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L871)), in `datalog.js` `NEG`/`MID`/`POS` ([datalog.js:102](../../public/scripts/datalog.js#L102)), in the expected dot colour of
  `drawn.u` ([L890](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L890)) and in the colour bar ([sim.css:128](../../public/styles/sim.css#L128)). The sum is in `precompute()` and again in `sumAt()` ([L777–788](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L777-L788));
  change both.
- **Numbers quoted by the note** come from the code: R = 300 px (eq. 5), the 10 px lift, the defaults 30 px / 1.1 Hz / 0.15, the
  presets 200/600 px and 64–736 px, the cap of 24. Change the note with them.
- **The catalog** entry's `equation`, `model`, `method` and `controls` ([catalog.js:56–59](../../public/scripts/catalog.js#L56-L59)) describe this page.
- **Re-test** after any change: open the Data panel and press Check on C, S, A, ψ, r1 (stored, recomputed, pixel); switch Read
  values on, pin a cell, confirm a click does not add a source, switch it off and confirm it does; record one round; watch the
  walkthrough's Now column update; resize between 390 px and 1440 px.

## Notes for maintainers

1. Fixed on 2026-10-15: §8 now gives the measured 360 × 162 desktop and 324 × 324 phone grids, 7.2 and 6.48 samples per shortest wavelength, and 1 866 240 trigonometric calls for 16 sources (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
2. Fixed on 2026-10-15: the walkthrough consistently uses γ for the slider and g = γ/R for attenuation per pixel (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
3. Fixed on 2026-10-15: the speed readout reads stored v and its walkthrough quotes that line (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
4. Fixed on 2026-10-15: the source-dot readback checks alpha before RGB (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
5. **Apostrophe.** The catalog `subject` uses "Huygens’" ([catalog.js:54](../../public/scripts/catalog.js#L54)); the page's subject line uses a straight
   apostrophe ([L41](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L41)).


## Teaching revision · 15 October 2026

The note distinguishes the chosen ring field from a physical two-dimensional wave-equation solution before the derivation; kr = 1 is a crossover, not an asymptotic accuracy guarantee. The colour is instantaneous signed displacement, not the amplitude map. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).

Fixed on 2026-10-16 (second repairs): the opening says in plain words what the figure adds and what it simplifies, and the $kr \gg 1$ caveat gives the size of the first correction, a phase lag of $1/(8kr)$ ([L190](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L190)). See the [audit of the revision](../research-theory-audit.md).

## Second check round · 20 October 2026

From the derivation checks and blind referees that ran after the usage limit lifted (`notes/fig01/`), each change on its existing line: §4: k, ω and aᵢ defined where (6) uses them, not only in the ★ Section 3 ([L283](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L283)); §7: opens by recalling the beam directions of the ★ Section 6 ([L380](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L380)); §10: dispersion contrasted correctly (in water the frequency fixes the wavelength) ([L479](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L479)). Checked with `notes/verify.mjs` at 1440 × 900, 1600 × 900 and 390 × 844.

From the Fig. 1 derivation check (111 verified, 2 wrong, 1 unverifiable; `notes/fig01/check.md`): §3: the first correction to the far-field ring is a phase lead, not a lag (the 16 October wording had the sign reversed; the size, 0.01 rad, was right) ([L272](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L272)); §6: the damping changes (12) by at most 0.04 at the default λ and up to 0.06 over the slider (0.03 came from a 0.1° grid) ([L309](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L309)).
