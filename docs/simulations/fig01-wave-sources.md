# Fig. 1 · Wave Interference

| | |
|---|---|
| Page | [public/simulations/Circular Wave Interference Visualization.html](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html) (908 lines, 206 578 bytes; since 23 November 2026 it plays data computed once on Kaggle, see below) |
| Walkthrough | [public/scripts/walk/circles.js](../../public/scripts/walk/circles.js) (181 lines, 9 steps, key `circles`) |
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
a dense row merge into one straight ripple: Huygens' principle.

**Model.** The water height ψ(x, y, t) obeys the two-dimensional wave equation, which is linear, so the waves of several sources
simply add. The page measures lengths in pixels of a field that is always 800 px wide; time is in seconds. The model on Kaggle
states the same lengths in metres by choosing a field 0.40 m wide (1 px = 0.5 mm); nothing in the picture depends on that choice,
only on k r and γ r/R. All sources oscillate in step at one frequency, the medium is non-dispersive, the edges do not reflect, and
the sources do not disturb each other. Instead of the true $1/\sqrt{r}$ fall-off of a ring the page uses an exponential damping that
stays finite at the source (note §3.1).

| Symbol | Meaning | Unit |
|---|---|---|
| $x_q = 1.6\,q$ | place of a source on the source line, q = 0 … 500 | px |
| $(i, j)$ | grid column from the left, row from the top; cells of $\Delta x = \Delta y = 3.2$ px | 1 |
| $m = \lvert 2i + 1 - q\rvert$ | horizontal gap from column i to place q, in half-cells | 1 |
| $r(j_b, m)$ | stored distance from a source place to a cell, row $j_b$ counted up from the bottom | px |
| $\lambda$, $k = 2\pi/\lambda$ | wavelength (stored nodes 16, 17, …, 64 px), wave number | px, rad/px |
| $\gamma$, $g = \gamma/R$, $R = 300$ px | damping (stored nodes 0, 0.05, …, 0.60), attenuation per pixel | 1, 1/px |
| $n$ | stored angle of a ring, $k r$ reduced to one turn, in steps of $2\pi/65536$ | 1 |
| $h$ | stored height of a ring, $e^{-g r}$, in steps of $1/65535$ | 1 |
| $f$, $\omega = 2\pi f$ | frequency (slider, continuous) and angular frequency | Hz, rad/s |
| $C, S, A, \psi$ | the two maps, the amplitude and the field, $\lvert\psi\rvert \le 1$ | 1 |

**What the code evaluates.** Each ring was computed once by the model `tools/sims/wave_interference.py` (on Kaggle) and is
stored; the page adds the rings of the sources the reader chose (superposition, note eq. 6) with no `cos`, `sin`, `exp` or
`sqrt` of the field:

$$C = \frac1N\sum_s \frac{h_s}{65535}\,\frac{\mathrm{cos}[n_s]}{32767}, \qquad S = \frac1N\sum_s \frac{h_s}{65535}\,\frac{\mathrm{cos}[n_s - 16384]}{32767}, \qquad A = \sqrt{C^2 + S^2},$$

where cos[·] is the stored table round(32767 cos(2π n/65536)) and the entry a quarter turn back gives the sine
([L656–657](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L656-L657)). On every frame the field is formed from one shared phase ([L669](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L669), [L675](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L675), [L762](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L762)):

$$\psi = C\cos\omega t + S\sin\omega t, \quad \text{clipped to } [-1, 1], \qquad \omega t \leftarrow \omega t + 2\pi f\,\Delta t .$$

This is $\psi = \frac{1}{N}\sum_s e^{-g r_s}\cos(k r_s - \omega t)$, the note's eqs. (5)–(7), up to the rounding of the stored numbers: against
the float64 sum straight from it, C and S differ by at most 5.9 × 10⁻⁵ over all 637 node pairs (model check), and by at most
5.1 × 10⁻⁵ against the page as it computed live until 23 November 2026, cell by cell on the same 250 × 250 grid in headless Chromium.
The colour of a cell is row $\operatorname{round}(127.5\,\psi + 127.5)$ of a 256-entry table ([L566–574](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L566-L574); note eq. 19).

## How the data is stored and loaded (since 23 November 2026)

Until 23 November 2026 the page computed every ring in the visitor's browser. Now the model
[`tools/sims/wave_interference.py`](../../tools/sims/wave_interference.py) computes them once on Kaggle (pipeline A of
[kaggle-sims.md](../kaggle-sims.md)), the workflow stores them under `public/data/sims/wave_interference/<date>/`, and the page
only reads them. The study and the measured numbers: [notes/sims/reports/wave_interference/study.md](../../notes/sims/reports/wave_interference/study.md).

| File | Content | Bytes |
|---|---|---|
| `geometry.bin` | header (every parameter, the node lists, the model's checks); r(j_b, m) float32, 250 × 500; cosine table int16, 65 536 | 632 640 |
| `ring_l016.bin` … `ring_l064.bin` (49) | angle n of a ring at every stored distance, uint16, 250 × 500, one file per wavelength | 250 244 – 250 260 each |
| `damp_g000.bin` … `damp_g060.bin` (13) | height h of a ring at every stored distance, uint16, 250 × 500, one file per damping | 250 188 – 250 208 each |
| `wave_interference.json` | the geometry header again, readable | 3 353 |

All 64 files: 16 150 677 bytes, computed on Kaggle on 23 November 2026 (notebook `numakoudsie/phyein-usul-simulations` version 2, code commit 5f98017, 171 s on 4 CPUs; committed by the workflow as 6be1fd7). Each `.bin` is 4 bytes of label `WIF1`, a uint32 header length, a JSON
header padded to a multiple of 4 bytes, then the little-endian array.

**`stored(file)`** ([L585–600](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L585-L600)): reads `data/sims/generations.json` once and takes the newest entry of `wave_interference`
([L588](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L588)); downloads `data/sims/wave_interference/<date>/<file>`, computes its SHA-256 with `crypto.subtle` and refuses it unless it
equals the entry's ([L593](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L593)); parses the header and hands out typed arrays, checking that the stored grid is the grid the page
draws ([L595](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L595)). The address is resolved from `scripts/sim.js`, so the German and Arabic pages find the same files ([L583](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L583)).
`window.__simData` reports the generation, the files in use, `sha_ok` and any error for the live check ([L584](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L584)).

**`load()`** ([L602–609](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L602-L609)): asks for `geometry.bin` and the ring and damping files of the nodes nearest the two sliders
(`node()`, [L601](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L601)); a reply for nodes the reader has already left is dropped ([L605](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L605)); once all three are checked, the
maps are marked stale and the waiting sentence ([L49](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L49)) is hidden ([L606](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L606)). On a failure the sentence says why and the
field stays empty ([L608](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L608)). The page opens with `geometry.bin` + `ring_l030.bin` + `damp_g015.bin` = 1 133 076 bytes; each other
node costs one more file of about 250 kB, downloaded and checked once per visit.

## How the code computes it

**State.** `sources` is an array of fractions $u_s$ of the width, each moved to the nearest stored place q/500
(`place()`, [L699](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L699)), newest 24 kept ([L701](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L701)). The fixed grid and lattice are named in one line: `CELL = 3.2`,
`NI = NJ = 250`, `NM = 500`, `PLACES = 500`, `PITCH = 1.6` ([L515](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L515)). `G`, `RING`, `DAMP` hold the three stored files in use
([L526](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L526)). The maps `sumC`, `sumS`, `ampl`, the field `psi` and the source-1 maps `r1`, `a1`, `ph1` are Float32 arrays owned
by the data store.

**Method.** No physics is evaluated in the browser: the rings come from the stored tables, and the page adds them. Space and time
separate exactly, so the per-source work (an angle and a height read per source per cell) runs only when the sources or the
nodes change, and a frame costs two multiplications and one addition per cell whatever N is. The only time error is the 0.05 s
cap on Δt ([sim.js:179](../../public/scripts/sim.js#L179)): on a slow device the pattern runs slower, it is not distorted.

**Frame loop** (`Sim.clock` callback, [L755–767](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L755-L767)), in order:
1. Keep the play time, count frames, smooth the frame rate, step a running parameter curve.
2. Draw nothing until the stored files have arrived ([L759](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L759)).
3. If `dirty`, run `superpose()` and ask for a redraw ([L760](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L760)).
4. If playing (Δt > 0) or a redraw is pending: advance `omegaT` by 2πfΔt ([L762](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L762)), store it, `render()`.

**`resize()`** ([L611–636](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L611-L636)): worldH = 800 · box.h/box.w; cols = 250; rows = min(250, ⌈worldH/3.2⌉) ([L614–615](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L614-L615));
reallocates every grid array; cell centres x = (i + ½) · 3.2 and y = worldH − (rows − j − ½) · 3.2, rows counted up from the bottom
edge as the stored tables are ([L631](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L631)).

**`superpose()`** ([L638–666](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L638-L666)): norm = 1/max(1, N) and w = norm/(65535 · 32767) ([L639](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L639)); k, g, λ and γ from the
headers of the stored files ([L641](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L641)); for each source its place q ([L647](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L647)), for each cell the table entry
e = (rows − 1 − j) · 500 + |2i + 1 − q| ([L653](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L653)); keeps r, a, φ of the first source ([L655](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L655)); accumulates the two components
([L656–657](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L656-L657)); A = √(C² + S²) ([L661](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L661)); records build count, time and the stored numbers read, 2NP ([L664](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L664)).

**`render()`** ([L668–697](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L668-L697)): unchanged in kind: ψ per cell, colour row, image; the image is stretched over the canvas with its
bottom row on the bottom edge, so on a wide screen the top row is cut in part ([L685](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L685)); then the source dots.

Measured in headless Chromium (23 November 2026, local data):

| Window width | Canvas (css px) | cols × rows | Points P | Line of 16: rebuild, frame |
|---|---|---|---|---|
| 1600 px | 550 × 248 | 250 × 113 | 28 250 | 2.8–26 ms (904 000 reads), 0.6–0.8 ms |
| 1100 px | 690 × 311 | 250 × 113 | 28 250 | — |
| 390 px | 356 × 356 | 250 × 250 | 62 500 | 6.6–40 ms (2 000 000 reads), 1.2–1.7 ms |

The first rebuild of a visit is the slowest (the script is still being compiled). At λ = 16 px the grid gives 5 points per
wavelength on every screen.

## Function map

All functions live in the one inline script ([L510–904](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L510-L904)).

| Function | Lines | What it does |
|---|---|---|
| colour-table builder (anonymous) | [L567–573](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L567-L573) | Fills `LUT`: for row i, a = i/127.5 − 1, s = \|a\|^0.8, each channel `mid + (end − mid) · s`. |
| slider `format` callbacks | [L576–578](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L576-L578) | "30 px", "1.10 Hz", "0.15". |
| `changed()` | [L580](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L580) | Asks `load()` for the files of the new nodes and refreshes the readouts. |
| `stored(file)` | [L585–600](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L585-L600) | Downloads one stored file of the newest generation, checks its SHA-256, parses it. |
| `node(v, lo, hi, step)` | [L601](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L601) | The stored node nearest a slider value. |
| `load()` | [L602–609](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L602-L609) | Puts the files of the current nodes in use once all three are checked; reports a failure in the waiting sentence. |
| `resize()` | [L611–636](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L611-L636) | Fits the canvas, sets the grid rows, reallocates the grid arrays, writes cell centres and grid scalars. |
| `superpose()` | [L638–666](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L638-L666) | Builds C, S, A and the source-1 maps from the stored tables. |
| `render()` | [L668–697](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L668-L697) | Turns C, S and ωt into ψ and pixels; draws the source dots. |
| `place(u)` | [L699](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L699) | The nearest of the 501 stored source places. |
| `setSources(list)` | [L700–703](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L700-L703) | Moves each source to a stored place, keeps the newest 24, marks the maps stale. |
| `readouts()` | [L705–713](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L705-L713) | Source count, caption count and speed v = f λ (λ of the stored ring in use). |
| click, *Line of 16*, *Add 5 random*, *Reset*, *Clear* | [L715–733](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L715-L733) | As before; every new source goes through `place()`. |
| `Sim.live()` | [L736–753](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L736-L753) | Strings for the walkthrough's "Now" column, read from the store at the centre cell. |
| clock callback | [L755–767](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L755-L767) | The frame loop above. |
| `sumAt(p, shift)` | [L776–786](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L776-L786) | Re-sums one cell from the stored angles and heights, for the C and S checks. |
| `pixelCheck(p)` | [L788–796](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L788-L796) | Pixel (i, j) of the offscreen image against the table row for the stored ψ, alpha first. |
| `Sim.data` | [L797–897](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L797-L897) | The panel spec: groups ([L800](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L800)), probe, inspect, locate, checks ([L836–882](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L836-L882)), read-backs ([L883–892](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L883-L892)), `about` ([L896](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L896)). |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Pause / Play | `play` | starts playing | toggles the clock |
| Line of 16 | `line` | — | 16 sources at x = 64 + 44.8 n px, all exactly on stored places q = 40 + 28 n ([L719–723](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L719-L723)) |
| Add 5 random | `random` | — | 5 sources between 133.3 and 666.7 px, each moved to the nearest stored place ([L724–728](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L724-L728)) |
| Reset | `reset` | — | ωt = 0 and two sources at 200 and 600 px, places 125 and 375 ([L729–732](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L729-L732)) |
| Clear | `clear` | — | no sources ([L733](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L733)) |
| Click on the field | `field` | — | a source at the nearest stored place to the click ([L715–718](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L715-L718)) |
| Wavelength λ | `lambda` | 16–64 px, step 1, default 30 ([L73](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L73)) | `changed()`: the ring file of the nearest node is loaded and the maps rebuilt |
| Frequency f | `freq` | 0.2–2 Hz, step 0.05, default 1.1 ([L77](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L77)) | `readouts()` only; enters through ωt; needs no stored data |
| Damping γ | `damp` | 0–0.6, step 0.05, default 0.15 ([L81](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L81)) | `changed()`: the damping file of the nearest node is loaded and the maps rebuilt |
| Curve · a knob that moves by itself | built by `curve.js` | five examples, your own curve | moves a slider exactly; λ and γ then use the nearest stored node |

Readouts: `r-n` (number of sources), `r-v` (stored `v` rounded, [L711](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L711)), `cap-count` in the caption.

## What the page writes into the data store

The store is created by `Sim.dataset(...)` ([L529](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L529); see [dataset.md](../scripts/dataset.md)); declarations run to [L563](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L563).
New since 23 November 2026: the group **Stored data** with `gen` (date and commit of the generation), `files` (the three files in
use), `sha_ok` and `bytes` (stored bytes downloaded), written by `stored()` and `load()`; `reads` (stored numbers read in one
rebuild, 2NP) replaces `trig_calls`. `lambda` and `damp` are now the stored nodes in use, read from the file headers, and `k` and `g`
come from those headers too. `ph1` is the stored angle within one turn (0 to 2π), no longer k r unwrapped.

Checks in the panel (stored value, formula recomputed from stored inputs, pixel read back): C and S re-sum the stored angles and
heights at the cell (`sumAt`); r₁ is recomputed from the coordinates with Pythagoras, a₁ = e^(−g r₁)/N and φ₁ = k r₁ mod 2π from the
formula, so those three checks show the rounding of the stored numbers (at most 4.8 × 10⁻⁵ rad and 7.6 × 10⁻⁶ before the factor
1/N); λ and γ are checked as the node nearest the slider.

**One round** (`Sim.data.round`, [L893–894](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L893-L894)) is one period of the sources, T = 1/f, measured on the play time `t`; while a parameter curve runs it is the rest of the
curve's run instead (`curve.round`, [L893](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L893)). Columns charted: `omegaT`, `cos_wt`, `sin_wt`, `psi_c`, `n_calm`, and during a curve `cv_p`, `cv_set`; the recorder also copies every numeric scalar. Unless the reader has pinned a
point, the round follows the cell j = ⌊rows/2⌋, i = ⌊0.72 cols⌋ ([L894](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L894), [datalog.js:1071](../../public/scripts/datalog.js#L1071)). The recorder keeps at most 600
samples, one every T/600 ([datalog.js:1052](../../public/scripts/datalog.js#L1052), [datalog.js:1081](../../public/scripts/datalog.js#L1081)). *Reset* sets ωt to 0 but not `t`, so it does not end a round.

**`Sim.live()`** ([L736–753](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L736-L753)) returns formatted strings under the keys `lam`, `k`, `g`, `N`, `norm`, `dx`, `grid`, `C`, `S`,
`c`, `s`, `psi`, `f`, `wt`, `v`, `idx`, `rgb`, `r`, `a`, `ph`, all read at the centre cell pc = j_c · cols + i_c. The walkthrough
polls it every 200 ms unless "Hold the numbers" is on ([sim.js:391–403](../../public/scripts/sim.js#L391-L403)).

**Proof, measured 23 November 2026** (headless Chromium, 1600 px window, local data from the model, paused, two default
sources, centre cell j = 56, i = 125 at x = 401.6 px, y = 179.9 px; stored value against the page's own `check` function, which
recomputes from the stored inputs):

| Variable | Stored | Stored − recomputed | What the gap is |
|---|---|---|---|
| C | 0.0901492 | 2.6 × 10⁻⁹ | float32 sum against the float64 re-sum of the same stored terms |
| S | −0.8436636 | −9.5 × 10⁻⁹ | the same |
| A | 0.8484664 | 1.6 × 10⁻⁸ | float32 |
| ψ | −0.8118278 | −1.9 × 10⁻⁸ | float32 |
| r₁ | 264.22565 px | −1.4 × 10⁻⁵ px | float32 storage of the distance table |
| a₁ | 0.4381247 | 3.6 × 10⁻⁶ | the height's step of 1/65535, halved by 1/N (at most 3.8 × 10⁻⁶) |
| φ₁ | 5.0738330 rad | 2.5 × 10⁻⁵ rad | the angle's step of 2π/65536 (at most 4.8 × 10⁻⁵ rad) |

The pixel read back from the offscreen image was rgb(88, 81, 76), identical to table row 24 for ψ = −0.8118; the screen pixel at
source 1 was rgb(122, 31, 43), the burgundy dot. The whole maps C and S in the browser are identical, bit for bit in all 28 250
cells, to the page's sum as the model emulates it in NumPy (`page_sum` in the model) from the same stored files.

## Page structure

**Head** ([L3–18](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L3-L18)): title "Wave Interference · Numa Koudsie" and description ([L8–9](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L8-L9)); the security policy and referrer rule
([L5–6](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L5-L6), see [build-and-deploy.md](../build-and-deploy.md#security)); stylesheets in order `../styles/sim.css`, `../styles/data.css`, `../styles/fold.css` ([L11–12](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L11-L12)), where `sim.css`
imports the self-hosted fonts, KaTeX's CSS and `paper.css`; an inline SVG favicon ([L14](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L14)); one inline rule, `#field { cursor: crosshair; }`
([L15–17](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L15-L17)). See [styles.md](../styles.md).

**Body**, top to bottom:
- Top bar: one span holding the Phyein Usul logo (a link to `../index.html` with `../images/phyein-usul-mark.svg`, 87 × 48) and
  "← All simulations" ([L21](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L21)), then the hand-written Fig. 1–11 links ([L20–36](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L20-L36)); a `<noscript>` message ([L39](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L39)).
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

**Walkthrough** ([circles.js](../../public/scripts/walk/circles.js), 9 steps). Each step quotes page lines; on 23 November 2026,
after the move to stored data, a script confirmed that all 53 quoted lines are identical, after trimming indentation, to lines of
the page (steps 1–5, 7–9 were rewritten or adjusted: the distance, the ring and the sum now quote `superpose()` and the stored
tables, the grid quotes the fixed 250-column grid, the clock quotes `if (!RING) return;`).

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

- **Stored rings.** The rings are not computed on the page: their angles and heights are whole numbers stored by the model, in steps
  of 2π/65536 and 1/65535, at λ = 16, 17, …, 64 px and γ = 0, 0.05, …, 0.60, on a fixed grid of 3.2 px cells with sources on places
  1.6 px apart. Against the exact sum of (6), C and S differ by at most 6 × 10⁻⁵ and the drawn colour by one table step at about
  0.1 % of cells and instants. The page says so in `about` and in note §8.
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

- **The stored data.** The grid (250 × 250 cells of 3.2 px), the source places (501, 1.6 px apart) and the node lists are fixed by
  the model `tools/sims/wave_interference.py` and repeated in the page's constants line; `stored()` refuses a geometry file whose grid
  differs. Changing any of them means changing the model, which reruns it on Kaggle when merged (docs/kaggle-sims.md), and the page
  together. Line numbers in the dated sections below refer to the page as it was on their date.
- **Walkthrough excerpts.** `circles.js` quotes 53 lines of the page script, among them the constants line ([L515](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L515)), the
  slider lines ([L576–578](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L576-L578)), `superpose()` ([L638–666](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L638-L666)), the grid lines of `resize()`
  ([L613–615](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L613-L615)), the speed line ([L710](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L710)), the clock ([L759–762](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L759-L762)) and the colour lines of `render()`.
  Keep these lines character for character, or change the walkthrough with them; check with a script that every quoted line is a
  page line. Insert new store taps after a quoted line, never inside a quoted pair (AGENTS.md).
- **`Sim.live()` keys** must match the `syms` keys of `circles.js`. A missing key shows "—".
- **Formulas live in several places.** The grid is in the constants line, in `resize()`, in the store attributes, in `check.cols` /
  `check.rows` and in the note §8; the colour table's three colours are in the builder, in `check.LUT`, in `datalog.js`
  `NEG`/`MID`/`POS` ([datalog.js:102](../../public/scripts/datalog.js#L102)), in `drawn.u` and in the colour bar ([sim.css:128](../../public/styles/sim.css#L128)).
  The sum is in `superpose()` and again in `sumAt()` ([L776–787](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L776-L787)); change both.
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

## Parameter curves · 30 October 2026

Numa asked for every animation to let a parameter follow a curve while the figure runs, with the reader's own curve as an
option and well-known curves as examples; Fig. 1 came first. The engine is [`scripts/curve.js`](../scripts/curve.md); this
page loads it after `dataset.js` ([L508](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L508)) and builds it right after `changed()` ([L599](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L599)) with three knobs (λ, f, γ) and
five examples. Its time advances in the clock callback, before the maps are rebuilt ([L760](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L760)). Every edit is on an existing
line; the page keeps 909 lines and the walkthrough's 51 quoted lines are all found (`node notes/walkcheck.cjs`).

The examples, each tied to the note's own equations; every number was computed, none estimated:

| Example | Knob, curve | What it shows | Numbers and where they come from |
|---|---|---|---|
| Calm lines, one pair at a time | λ 64 → 16 px in 30 s, steady in 1/λ | By (10), the calm lines of two sources s apart are the m with \|m + ½\| λ < s: n = 2⌈s/λ − ½⌉ of them, a number that grows with 1/λ. Steady in 1/λ, a new pair arrives at even intervals. In a real ripple tank (λ = v/f) this is a steady rise in frequency. | 12 → 50 lines with Reset's s = 400 px. On the slider's 0.1 px steps, 19 pairs arrive one at a time, 1.48–1.74 s apart (median 1.60 s); on 1 px steps the gaps were 1.0–2.3 s with one double jump, which is why the step became 0.1 px. The count was checked against a brute-force count of sign changes of cos(πΔr/λ) on a far semicircle (six cases, all equal), and against the note's 26 at 30 px and 14 at 60 px. |
| Exponential sweep: slow, then a rush | λ 64 → 16 px in 30 s, exponential | Equal time per halving of λ, as in Farina's swept sine. | 12 → 24 → 50 lines: 6 new pairs in the first 15 s, 13 in the second. At λ = 32 px exactly, s/λ − ½ = 12 and the 13th pair lies on the sources' line, so the count is 24, not 26: the formula uses ⌈ ⌉ for that reason. |
| Exercise 5.1, done smoothly | λ 30 → 60 px in 6 s, minimum jerk | The note's Exercise 5.1 by itself. Far out, calm line m leaves at sin θ = (m + ½) λ / s from the vertical, so every line swings outward as λ grows. | 26 → 14 lines; θ₀, θ₁, θ₂ = 2.1°, 6.5°, 10.8° at 30 px and 4.3°, 13.0°, 22.0° at 60 px. |
| Calm lines fill in | γ 0 → 0.6 in 8 s, minimum jerk | Cancellation needs equal amplitudes; with damping the nearer source wins and a motion of \|a₁ − a₂\|/2 survives (§5). | §5 gives the residue: 0.071 at γ = 0.15 and 0.162 at 0.6 along the centre row. |
| Frequency alone: the calm lines stay | f 0.2 → 2 Hz in 20 s, exponential | In (9) the envelope cos(kΔr/2) has no ω: the calm lines stay where they are while the water flickers faster and the rings run faster, v = fλ (8). | — |

New in the store, written in `precompute()` with the maps ([L656](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L656)) and declared at [L541](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L541): `s2`, the spacing of the two
sources (NaN unless there are exactly two), and `n_calm` = 2⌈s/λ − ½⌉ (NaN likewise), both in the group Derived physics
([L804](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L804)), each with a Check from the stored inputs ([L838](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L838)). `n_calm` is not drawn as a number; the calm lines are the
cream lines of ψ, and its attribute `drawn_note` says so. The curve's own eighteen variables, checks and read-backs come from
`curve.extend(Sim.data)` ([L898](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L898)); the round becomes the rest of a running curve ([L894–895](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L894-L895)); the
`about` paragraph gains one sentence: the simulation now follows p(u) itself, put on the slider exactly ([L897](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L897)). `lambda` is now shown with one decimal ([L528](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L528)).

Tested in jsdom with the page's real scripts (36 checks pass; see [curve.md](../scripts/curve.md)), and in German and
Arabic (no English left in the tool, no page errors). Not yet seen in a real browser: the session's hook refused headless
Chromium.

### Exact values on the sliders · 30 October 2026

A curve now puts its exact value on the slider instead of the nearest step, so the thumb glides and the page follows p(u)
itself; a hand on the slider puts it back on its steps ([curve.md](../scripts/curve.md), "Exact values on the slider"). On this page: the `about` sentence says so ([L897](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L897)); the λ label rounds to 0.1 px ([L595](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L595); it printed the raw value,
which under a curve read "36.1039222 px"), and the walkthrough line that quotes it was updated. With λ continuous the
number of calm lines changes exactly when s/λ crosses a half-integer, so "Calm lines, one pair at a time" no longer
inherits a rhythm from the slider's steps.
