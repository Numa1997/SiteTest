# public/scripts/datalog.js

| | |
|---|---|
| File | [public/scripts/datalog.js](../../public/scripts/datalog.js), 1084 lines, 76.7 kB (76 675 bytes) |
| Loaded by | the ten simulation pages, last, after the page's own script (line numbers in the load-order table of [sim.md](sim.md#load-order-on-the-pages)); styles in [styles/data.css](../../public/styles/data.css), linked in each page's head (for example [Double Pendulum.html:12](../../public/simulations/Double%20Pendulum.html#L12)) |
| Reads | `Sim.data` (the page's contract, below) and through it the page's dataset ([datalog.js:39-40](../../public/scripts/datalog.js#L39-L40)) |
| Defines | `Sim.colourMap` ([datalog.js:67](../../public/scripts/datalog.js#L67)), `window.__dataPanel` ([datalog.js:1083](../../public/scripts/datalog.js#L1083)) |
| Adds to the page | `button.dp-tab` and `aside#data-panel.dp` at the end of `<body>` ([datalog.js:167-168](../../public/scripts/datalog.js#L167-L168)); `canvas.dp-overlay` inside `#stage`, `div.dp-read` right after `#stage`, `button.dp-readbtn` in the figure caption ([datalog.js:567-589](../../public/scripts/datalog.js#L567-L589)) |

`datalog.js` is the data panel: a variable explorer in the manner of Spyder's, fed by the page's one store
([dataset.md](dataset.md)). It shows every variable at one caught instant (Variables), repaints them every frame only when
the reader switches Live on, opens arrays as tables copied at one instant, lets the reader pin a point of the figure and read
its values (Read values), checks any value three ways (Check: stored, recomputed, read back from the picture), records one
round of the running simulation (Record), and saves everything as a NumPy archive with CSV and a README (Save). It never
computes physics and never writes to the store. When nobody is looking it does no work at all
([datalog.js:1-36](../../public/scripts/datalog.js#L1-L36)).

## How it works

### The picture

Think of an assistant who sits beside the experiment with a camera, a probe and a chart recorder, and does nothing until
asked. Opening the panel takes one photograph of every dial (Variables). Catch now takes another. Live turns the camera into
a video, which costs the most. Read values puts a probe on one point of the apparatus; the probe's reading is written on a
card under the apparatus, four times a second. Record switches the chart recorder on for one round, then off. Check takes one
dial, works its number out again by hand from the other dials, and looks at the apparatus to see that it shows the same.
Save hands over the notebook.

### Start-up, in source order

1. If the page did not define `Sim.data` with a `ds`, the file returns and the page has no panel
   ([datalog.js:39-40](../../public/scripts/datalog.js#L39-L40)).
2. It defines its helpers and `Sim.colourMap` ([datalog.js:43-74](../../public/scripts/datalog.js#L43-L74)), then reads the
   store through short accessors `V`, `A`, `sym`, `digitsOf`, `unitOf` ([datalog.js:77-92](../../public/scripts/datalog.js#L77-L92)).
3. It lists the variables to show: the names in `Sim.data.groups`, in order, that exist in the store
   ([datalog.js:93-94](../../public/scripts/datalog.js#L93-L94)).
4. It reads what one round is, `R` ([datalog.js:97-100](../../public/scripts/datalog.js#L97-L100)), the time variable `TV`
   ([datalog.js:101](../../public/scripts/datalog.js#L101)) and the round's chart columns, the numeric scalars of
   `round.columns` other than time ([datalog.js:108](../../public/scripts/datalog.js#L108)).
5. It builds the tab button and the panel: header (kicker, Save, Close, title), the Record box, two tabs (Variables, Rounds),
   four panes (`vars`, `array`, `check`, `rounds`) and an explanation "How the numbers and the picture are tied" that ends with
   the page's own `about` paragraph ([datalog.js:117-165](../../public/scripts/datalog.js#L117-L165)).
6. It writes the Variables ledger once ([datalog.js:187-209](../../public/scripts/datalog.js#L187-L209)).
7. If the page has `#stage` and `Sim.data` has `probe` and `inspect`, it adds the Read values button, the overlay canvas and
   the strip, with their pointer listeners ([datalog.js:566-639](../../public/scripts/datalog.js#L566-L639)).
8. It restores the reader's choices from `localStorage` and opens the panel if it was open last time, or, the first time, if
   the window is at least 1500 px wide ([datalog.js:1070-1075](../../public/scripts/datalog.js#L1070-L1075)).
9. Two animation frames later, after the simulation has drawn twice, it catches the first instant, so the ledger shows a real
   frame and not the empty start ([datalog.js:1077](../../public/scripts/datalog.js#L1077)).

### The loop that runs only when needed

The panel has one `requestAnimationFrame` loop, and it runs only while `wanted()` is true: a round is recording, Read values
is on with a pin or an outline showing, a table cell's position is being shown in the figure, the panel is open with Live on,
or a marker still has to be wiped ([datalog.js:1059](../../public/scripts/datalog.js#L1059)). Any action that may need it calls
`kick()`, which starts the loop if it is not running ([datalog.js:1060](../../public/scripts/datalog.js#L1060)). Each frame does,
in order: record one sample, draw the probe overlay, repaint the open view if Live is on, and either request the next frame or
stop and wipe the overlay ([datalog.js:1061-1067](../../public/scripts/datalog.js#L1061-L1067)).

Animation-frame callbacks run in the order they were requested. The page's clock requests its next frame inside its own
callback ([sim.js:185](../../public/scripts/sim.js#L185)), before any later `kick()` can, so in every frame the panel reads
the store after the simulation has written it, as the comment says ([datalog.js:1057](../../public/scripts/datalog.js#L1057)).

Measured in headless Chromium on Fig. 2 (window 1600 × 1000, panel open at load): with Live off and Read values off,
`__dataPanel.running()` is `false`; with Read values switched on but nothing pinned, it is still `false`.

### Variables: one caught instant

Each group becomes a numbered section; each variable a row with its symbol, long name, value, a type label (`array of
float64`, or the scalar type), its shape (`q 4 × …`) and its variable name with `computed_in`
([datalog.js:188-202](../../public/scripts/datalog.js#L188-L202)). A scalar row ends in a Check button; an array row shows a
128 × 34 px thumbnail (a line for 1-D, a heat map for 2-D) and its range, and opens as a table
([datalog.js:220-278](../../public/scripts/datalog.js#L220-L278)). The heat map uses the page's `colour` function for that
variable or else `Sim.colourMap` with a symmetric limit $\max(|\min|, |\max|)$ ([datalog.js:245-249](../../public/scripts/datalog.js#L245-L249)).
Min, max and mean skip NaN and infinite values and are cached until the variable's version changes
([datalog.js:212-219](../../public/scripts/datalog.js#L212-L219)).

`catchNow(why)` records the time and the reason, re-copies an open table, re-runs an open Check and repaints
([datalog.js:299-304](../../public/scripts/datalog.js#L299-L304)). It is called when the panel opens, on Catch now, when Live is
switched off, and at the end of a round ([datalog.js:1025](../../public/scripts/datalog.js#L1025),
[1037](../../public/scripts/datalog.js#L1037), [1041](../../public/scripts/datalog.js#L1041),
[838](../../public/scripts/datalog.js#L838)). The line above the ledger says which instant is shown, for example
"Values at t = 3.41 s · caught when the panel opened" ([datalog.js:293-298](../../public/scripts/datalog.js#L293-L298)).
With Live on, `paint(false)` runs every frame: values every frame, thumbnails at most every 250 ms and only when the version
moved ([datalog.js:279-291](../../public/scripts/datalog.js#L279-L291)).

### Arrays as tables

Opening an array copies it (`slice()`) at one instant, so every cell shows the same frame
([datalog.js:374-379](../../public/scripts/datalog.js#L374-L379)). A 2-D variable is shown as rows × columns. A 1-D variable is
shown together with every other 1-D variable over the same dimension, coordinates first, one column each, from `ds.along`
([datalog.js:375](../../public/scripts/datalog.js#L375), [dataset.js:102](../../public/scripts/dataset.js#L102)). Above the table:
shape, min, max and mean, or the list of variables along the dimension, and "Copied at t = …"
([datalog.js:421-435](../../public/scripts/datalog.js#L421-L435)).

The table is virtual: only the cells inside the scrolled window exist in the DOM. Cells are 74 × 28 px (108 px wide for 1-D),
the row header 56 px (64 px for 1-D), the column header 32 px ([datalog.js:308](../../public/scripts/datalog.js#L308),
[datalog.js:393](../../public/scripts/datalog.js#L393)). On every scroll or resize `layout()` works out the first and last
visible row and column, rebuilds only if that window changed, and `fill()` writes a cell's text and background only when
they changed ([datalog.js:318-345](../../public/scripts/datalog.js#L318-L345)). Measured on Fig. 1 (window 1600 × 1000): the
162 × 360 array `C`, 58 320 numbers, was shown with 80 cell elements and 18 header elements, 104 elements in the whole table.

Pointing at a cell (mouse over or click) shows its index and value with a Check button under the table and, if the page has
`locate`, marks where that element is drawn in the figure with a ring: for 0.6 s after a hover, 3 s after a click or tap
([datalog.js:355-362](../../public/scripts/datalog.js#L355-L362), [datalog.js:453-457](../../public/scripts/datalog.js#L453-L457),
[datalog.js:675-685](../../public/scripts/datalog.js#L675-L685)).

### Read values

Off, the figure behaves as if this file were absent. On, the gesture belongs to the reading: the panel's listeners run in the
capture phase and stop the event before the page's own handlers see it, so a click does not add a source or start a drawing
([datalog.js:614-637](../../public/scripts/datalog.js#L614-L637)).

- **Pin.** A press asks the page's `probe(x, y)` what lies under the pointer. If nothing does, it tries 8 points on a ring
  12 px out, then 8 on a ring 22 px out, so a finger finds a small moving object ([datalog.js:549-555](../../public/scripts/datalog.js#L549-L555)).
  A drag keeps re-pinning ([datalog.js:625](../../public/scripts/datalog.js#L625)). A press on empty space says "Nothing to pin
  there" ([datalog.js:696](../../public/scripts/datalog.js#L696)).
- **Marker.** Every frame the overlay is wiped and the pin is drawn at `inspect(ref).at`, so it rides on the moving object: a
  ring of radius 11 px with a light halo and four ticks out to 18 px ([datalog.js:648-656](../../public/scripts/datalog.js#L648-L656),
  [datalog.js:671-674](../../public/scripts/datalog.js#L671-L674)). Only the rectangles drawn last frame are cleared, unless
  there are more than six ([datalog.js:640-646](../../public/scripts/datalog.js#L640-L646)).
- **Words.** The title and values go into a strip under the figure, between the figure and its caption, so they never cover
  it ([datalog.js:572-579](../../public/scripts/datalog.js#L572-L579)). They are rewritten at most every 250 ms
  ([datalog.js:686](../../public/scripts/datalog.js#L686)); the row structure is rebuilt only when the list of rows changes,
  otherwise only changed numbers are written ([datalog.js:701-713](../../public/scripts/datalog.js#L701-L713)). Each value that
  names a dataset variable is a button that opens Check. The same values appear in the panel under "Pinned point"
  ([datalog.js:716-735](../../public/scripts/datalog.js#L716-L735)).
- **Outline before a click.** With a mouse, moving shows nothing. Resting 0.3 s outlines, with a thin dark ring of radius 9 px,
  what a click would pin ([datalog.js:626-631](../../public/scripts/datalog.js#L626-L631), [datalog.js:667-670](../../public/scripts/datalog.js#L667-L670)).
- **Stop.** The button again, or Esc ([datalog.js:590](../../public/scripts/datalog.js#L590), [datalog.js:638](../../public/scripts/datalog.js#L638)).

Measured on Fig. 2 (window 1600 × 1000, device pixel ratio 1, figure 630 × 472.5 px, overlay 297 990 pixels):

| Situation | Overlay pixels painted | Strip |
|---|---|---|
| Read off, pointer swept across the figure (41 moves, 16 ms apart) | 0 | hidden |
| Read on, same sweep | 0 | hint only |
| Read on, pointer resting on the pivot for 0.1 s | 0 | hint only |
| Read on, resting 0.45 s | 144 (outline ring) | hint only, no values |
| Clicked: pivot pinned, simulation running | 446 (0.15 % of the figure) | 6 rows, below the figure (strip top 736.5 px = figure bottom), no overlap |

Over 3 s of a pinned, running simulation (181 frames), the strip's values changed in 11 batches: 3.7 rewrites per second,
within the 4 per second the code allows.

### Check: three answers from one frame

`openCheck(name, idx)` shows one value of one variable ([datalog.js:479-487](../../public/scripts/datalog.js#L479-L487)), and
`runCheck()` writes three sections, all from the same frame ([datalog.js:496-535](../../public/scripts/datalog.js#L496-L535)):

1. **Stored in the dataset**: the value, its variable name and index, type, `computed_in`, `updates`, `formula`.
2. **Recomputed now, from the stored inputs**: the page's `check[name](idx)` returns a formula, a table of inputs and a value;
   `agreement()` compares it with the stored value ([datalog.js:488-495](../../public/scripts/datalog.js#L488-L495)). With
   $d = |\text{stored} - \text{recomputed}|$ and $s = \max(|\text{stored}|, |\text{recomputed}|)$, the two agree when
   $$d \le 2\times10^{-6}\,s + 10^{-7}$$
   for a `float32` array and
   $$d \le 10^{-9}\,s + 10^{-12}$$
   otherwise. The verdict says "identical" when $d = 0$, otherwise "agree to $n$ significant figures; the rest is float32
   storage" (or "rounding"), with $n = \lfloor -\log_{10}(d/s) \rfloor$; a larger gap reads "DIFFER by …". Strings and
   booleans are compared as text; two non-finite values are "both undefined now". Without a `check` entry the section shows the
   attribute `source` or says the value is an input read from a control.
3. **Read back from the picture**: the page's `drawn[name](idx)` returns what it read (a pixel colour, an SVG attribute),
   what the store predicts, `ok` and a note. Without one, the section shows `drawn_note` or says the value enters the picture
   only through arrays computed from it.

Measured on Fig. 2: the denominator `den` (stored 3.3590 kg, recomputed 3.358995) and the energy `E` (18.305709 J) are
"identical"; the bob position `x2_px` (332.6 css px) is "identical" and "The picture shows this value."

### Record one round

A round is what the page says it is, in `Sim.data.round` ([datalog.js:21-23](../../public/scripts/datalog.js#L21-L23)):

| Fig. | One round | Time variable | Mode | Can be blocked | Line |
|---|---|---|---|---|---|
| 1 | one period of the sources, $T$ | `t` | sampled | no | [L892](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L892) |
| 2 | ten seconds of simulated motion | `t` | sampled | no | [L829](../../public/simulations/Double%20Pendulum.html#L829) |
| 3 | ten seconds of slider changes | `wall` | `'change'` | no | [L910](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L910) |
| 4 | one period, $T$ | `t` | sampled | no | [L1071](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1071) |
| 5 | one period, $T$ | `t` | sampled | no | [L875](../../public/simulations/water-wave.html#L875) |
| 6 | one repeat of the pattern, at most 20 s | `t` | sampled | no | [L947](../../public/simulations/wave-interference.html#L947) |
| 7 | one full figure (or part of it) in phasor time | `t` | sampled | yes, in the final-shape view | [L1462](../../public/simulations/phasor-sums.html#L1462) |
| 8 | one loop of the circles | `t` | sampled | yes, until a shape is decomposed | [L1398](../../public/simulations/draw-decompose.html#L1398) |
| 9 | one drive period $1/f$ of the stored run | `t_play` | sampled | yes, near the end of the run | [L1093](../../public/simulations/driven-oscillator.html#L1093) |
| 10 | one rotor turn of the stored run | `t_play` | sampled | yes, near the end of the run | [L1138](../../public/simulations/wind-turbine.html#L1138) |

`startRound()` ([datalog.js:755-778](../../public/scripts/datalog.js#L755-L778)) refuses with the page's reason if `blocked`
returns one, presses Play if the simulation is paused, chooses the point to follow (the pinned point, else `round.point()`),
and prepares one buffer per numeric scalar of the whole store (`scalarNames()`, every scalar of type `float`, `int` or
`bool`), one per row of the followed point, and two for time. It also notes the first group's scalars as the round's
parameters. In sampled mode the target spacing is the round length over 600; in change mode it is zero.

`recordFrame()` runs once per frame while recording ([datalog.js:786-815](../../public/scripts/datalog.js#L786-L815)). It reads
the time variable (or `performance.now()` if there is none, [datalog.js:102](../../public/scripts/datalog.js#L102)); the first
frame sets $t_0$, and the elapsed time is $t - t_0$. A frame is taken when

- sampled mode: it is the first, or at least $0.999 \cdot L/600$ after the last taken one, or the round has ended;
- change mode: the joined values of `round.columns` differ from the last frame's.

At most 600 samples are taken (`MAXS`, [datalog.js:743](../../public/scripts/datalog.js#L743)). A taken frame stores $t$, the
elapsed time, every numeric scalar (booleans as 1 or 0, anything else not numeric as NaN), and each row of the followed point,
or NaN when the page's rows for that point changed shape ([datalog.js:799-807](../../public/scripts/datalog.js#L799-L807)). The
progress bar is repainted every 125 ms ([datalog.js:811-813](../../public/scripts/datalog.js#L811-L813)). The round ends when
the elapsed time reaches $L$ (or, in change mode, at 600 samples), when Stop is pressed, or when time runs backwards because
the page restarted ("the clock was reset", [datalog.js:791](../../public/scripts/datalog.js#L791)). A round with fewer than two
samples is dropped with a message ([datalog.js:823](../../public/scripts/datalog.js#L823)).

`finishRound()` turns the buffers into `Float64Array` series: time first, then one per chart column, then one per row of the
followed point, keyed `<variable>[_<index>]_at_point` ([datalog.js:816-842](../../public/scripts/datalog.js#L816-L842)). The
last five rounds are kept ([datalog.js:834](../../public/scripts/datalog.js#L834)); the panel opens on the Rounds tab. Each
round shows: chips to switch rounds, the parameters at the start, one chart per quantity that changed (black lines for the
followed point, burgundy for the rest), one line for quantities that stayed constant or were undefined, and a collapsible
table of every sample ([datalog.js:881-916](../../public/scripts/datalog.js#L881-L916)). Pointing at a chart draws a cursor on
every chart at the nearest sample and lists all values at it ([datalog.js:927-939](../../public/scripts/datalog.js#L927-L939)).

Measured on Fig. 2: a 10 s round gave 600 samples from 601 frames, 15 series (time, 7 columns, 7 rows of the followed bob) and
48 recorded scalars; the last sample sits at 9.983 s.

### Save: what goes into the files

| Button | File name | Contents | Lines |
|---|---|---|---|
| Save (panel header) | `<file>-<stamp>.zip` | the store via `ds.npz`: one `.npy` per array, `dataset.json`; then `round-<n>.csv` for each kept round and `README.txt` | [999-1003](../../public/scripts/datalog.js#L999-L1003) |
| Save this round | `<file>-round-<n>-<stamp>.zip` | a new dataset with dimension `sample`, coordinate `time_into_round`, one `float64` variable per series and per recorded scalar, attributes (page, round label, samples, frames, time caught, time variable, followed point, `start_<parameter>`); plus `round.csv` and `README.txt` | [964-973](../../public/scripts/datalog.js#L964-L973) |
| CSV | `<file>-round-<n>-<stamp>.csv` | the round as CSV | [963](../../public/scripts/datalog.js#L963) |

`<file>` is `Sim.data.file` (for example `fig2-double-pendulum`, [Double Pendulum.html:748](../../public/simulations/Double%20Pendulum.html#L748));
`<stamp>` is the UTC time as `YYYY-MM-DDTHH-MM-SS` ([datalog.js:957](../../public/scripts/datalog.js#L957)). The download goes
through a temporary object URL that is revoked after 4 s ([datalog.js:948-956](../../public/scripts/datalog.js#L948-L956)).

The CSV ([datalog.js:941-947](../../public/scripts/datalog.js#L941-L947)) has the header `sample,time_into_round,` then the series
keys, then every other recorded scalar; one row per sample, numbers written with `String(v)` (full double precision), NaN as an
empty cell, `\n` line ends. Units are not in the CSV; they are in the round archive's `dataset.json`.

The README ([datalog.js:977-998](../../public/scripts/datalog.js#L977-L998)) names the page and the time, explains the layout and
gives Python to load the archive with `zipfile`, `json` and NumPy, and to build an xarray `Dataset`.

### The .npz writer, byte by byte

The writer lives in `dataset.js` ([dataset.js:112-181](../../public/scripts/dataset.js#L112-L181)); the panel is its only caller.
An `.npz` is nothing but a zip archive whose members are `.npy` files. This one is written by hand, uncompressed, so it needs
no library.

**One `.npy` file per array** (`npy`, [dataset.js:114-127](../../public/scripts/dataset.js#L114-L127)), NumPy format version 1.0:

| Bytes | Content |
|---|---|
| 0-5 | magic string `\x93NUMPY` ([dataset.js:121](../../public/scripts/dataset.js#L121)) |
| 6-7 | version 1, 0 |
| 8-9 | header length $h$, unsigned 16-bit little-endian ([dataset.js:122-123](../../public/scripts/dataset.js#L122-L123)) |
| 10 … 9 + h | an ASCII Python dictionary, for example `{'descr': '<f8', 'fortran_order': False, 'shape': (4,), }`, padded with spaces and ended by `\n` ([dataset.js:116-119](../../public/scripts/dataset.js#L116-L119)) |
| 10 + h … | the array's raw bytes, copied from memory ([dataset.js:125](../../public/scripts/dataset.js#L125)) |

- `descr` is the type from the `DTYPES` table, for example `<f8` for `Float64Array` ([dataset.md](dataset.md#types)).
- `fortran_order: False` says the bytes are in C (row-major) order, which is how the store keeps 2-D arrays: the last index
  runs fastest.
- `shape` comes from the variable's dimensions; a 1-D shape gets the trailing comma Python needs for a one-element tuple
  ([dataset.js:116](../../public/scripts/dataset.js#L116)).
- The padding makes the data start on a multiple of 64 bytes: the number of spaces is
  $(64 - (10 + \ell + 1) \bmod 64) \bmod 64$, where $\ell$ is the dictionary's length and the $+1$ is the final newline
  ([dataset.js:117](../../public/scripts/dataset.js#L117)).

**The zip** (`zip`, [dataset.js:143-160](../../public/scripts/dataset.js#L143-L160)). For each member, in order: a 30-byte local
header, the UTF-8 name, the data. Then a 46-byte central-directory record plus name per member, then a 22-byte end record. All
integers are little-endian ([dataset.js:145-146](../../public/scripts/dataset.js#L145-L146)).

| Record | Fields as written |
|---|---|
| Local header ([L151](../../public/scripts/dataset.js#L151)) | signature `50 4B 03 04`; version needed 20 (zip 2.0); flags `0x0800` (bit 11: the name is UTF-8); method 0 (stored, no compression); DOS time; DOS date; CRC-32; compressed size = uncompressed size = data length; name length; extra length 0 |
| Central record ([L153](../../public/scripts/dataset.js#L153)) | signature `50 4B 01 02`; version made by 20; version needed 20; flags `0x0800`; method 0; time; date; CRC-32; both sizes; name length; extra, comment, disk number, internal and external attributes all 0; offset of the local header |
| End record ([L158](../../public/scripts/dataset.js#L158)) | signature `50 4B 05 06`; disk numbers 0; number of entries (twice); size of the central directory; its offset; comment length 0 |

- The CRC-32 uses the reflected polynomial `0xEDB88320` with a 256-entry table built once; the register starts at
  `0xFFFFFFFF` and is inverted at the end ([dataset.js:128-141](../../public/scripts/dataset.js#L128-L141)).
- The DOS time is $2048\,h + 32\,m + \lfloor s/2 \rfloor$ and the DOS date $512\,(y - 1980) + 32\,M + d$, from the browser's
  local clock, the same for all members ([dataset.js:147-148](../../public/scripts/dataset.js#L147-L148)).
- Member order: the arrays in declaration order, `dataset.json`, then the extra files ([dataset.js:163-179](../../public/scripts/dataset.js#L163-L179)).

**`dataset.json`** ([dataset.js:162-178](../../public/scripts/dataset.js#L162-L178)) holds `title`, `attrs`, `dims`, `coords`
(names of the coordinate variables) and `data_vars`: for an array `{ dims, attrs, dtype, shape, file }`, for a scalar
`{ dims: [], attrs, dtype, value }`, in declaration order, indented by two spaces. JSON has no NaN: a NaN or infinite scalar is
written as `null` by `JSON.stringify`.

**Verified.** A test call of `ds.npz` on Fig. 2 in headless Chromium gave a zip of six members (`y.npy`, `dydt.npy`,
`y_twin.npy`, `M.npy`, `dataset.json`, `README.txt`), each with method 0 and flags `0x0800`. Python's `zipfile.testzip()`
found no CRC error. `numpy.load` (NumPy 2.5.3) opened the file as an `NpzFile` with keys `y`, `dydt`, `y_twin`, `M`,
`dataset.json`, `README.txt`; the arrays loaded as `float64` with the right shapes (`y`: `(4,)`), and the non-`.npy` members
came back as raw bytes. In `y.npy` the header length is 118, so the data starts at byte 128. A real Save on Fig. 1 gave
`fig1-wave-interference-<stamp>.zip` with 14 members (12 arrays, `dataset.json`, `README.txt`), no CRC error, and the README's
Python lines loaded all 12 arrays (`C` and `S` as `<f4` of shape `(162, 360)`) and 38 scalars. The xarray line was not run,
because xarray is not installed here.

## The contract: `Sim.data`

A page opts in by defining `Sim.data` next to its own state and loading `datalog.js` after its own script
([datalog.js:8-26](../../public/scripts/datalog.js#L8-L26)). Keys in the left column are read where shown; the right column says
which pages set them (from the ten `Sim.data = {` blocks).

| Key | Shape | Read at | Set by |
|---|---|---|---|
| `ds` | the dataset | [39](../../public/scripts/datalog.js#L39) | all |
| `kicker` | text above the title (default: the dataset title) | [136](../../public/scripts/datalog.js#L136) | all, not in the comment |
| `file` | base name of saved files | [963](../../public/scripts/datalog.js#L963), [978](../../public/scripts/datalog.js#L978), [1002](../../public/scripts/datalog.js#L1002) | all |
| `playing` | `() → bool` | [759](../../public/scripts/datalog.js#L759), [781](../../public/scripts/datalog.js#L781) | all |
| `play` | `() → void` | [759](../../public/scripts/datalog.js#L759) | all except Fig. 3 |
| `groups` | `[{ title, note, vars }]` | [94](../../public/scripts/datalog.js#L94), [188](../../public/scripts/datalog.js#L188), [766](../../public/scripts/datalog.js#L766) | all |
| `colour` | `{ name: (value, j, i) → [r, g, b] \| null }`, presentation only | [91](../../public/scripts/datalog.js#L91) | all except Figs. 2 and 10 |
| `rowLabel` | `{ dim: (j) → text }` | [399](../../public/scripts/datalog.js#L399), [413](../../public/scripts/datalog.js#L413) | Figs. 2, 3, 5, 6, 7, 8; not in the comment |
| `colLabel` | `{ name: (i) → html }` | [412](../../public/scripts/datalog.js#L412) | Figs. 1, 2; not in the comment |
| `at` | `{ name: (j[, i]) → html }`, a note after a table cell's value | [402](../../public/scripts/datalog.js#L402), [416](../../public/scripts/datalog.js#L416) | Figs. 1, 2; not in the comment |
| `probe` | `(x, y) → ref \| null`, CSS px in `#stage` | [550](../../public/scripts/datalog.js#L550) | all |
| `inspect` | `(ref) → { title, at: {x, y}, rows: [[symbol, value, units, varName, index]] }` | [668](../../public/scripts/datalog.js#L668), [691](../../public/scripts/datalog.js#L691), [802](../../public/scripts/datalog.js#L802) | all |
| `locate` | `(varName, index) → {x, y} \| null` | [676](../../public/scripts/datalog.js#L676) | all |
| `check` | `{ name: (index) → { formula, inputs: [[symbol, value, units, digits]], value } }` | [509](../../public/scripts/datalog.js#L509) | all |
| `drawn` | `{ name: (index) → { what, drawn, expected, ok, note } }` | [523](../../public/scripts/datalog.js#L523) | all |
| `round` | `{ label, time, length, columns, point, mode?, blocked? }` | [97](../../public/scripts/datalog.js#L97) | all (table above) |
| `log` | `{ time, mode, columns }`, used only when `round` is missing | [98](../../public/scripts/datalog.js#L98) | none |
| `about` | HTML paragraph: what still differs between store and picture | [164](../../public/scripts/datalog.js#L164) | all |
| `touchProbe` | | not read | Fig. 8 only ([draw-decompose.html:1402](../../public/simulations/draw-decompose.html#L1402)) |

The ten blocks: [Fig. 1 L798](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L798),
[Fig. 2 L747](../../public/simulations/Double%20Pendulum.html#L747),
[Fig. 3 L829](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L829),
[Fig. 4 L994](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L994),
[Fig. 5 L807](../../public/simulations/water-wave.html#L807),
[Fig. 6 L864](../../public/simulations/wave-interference.html#L864),
[Fig. 7 L1369](../../public/simulations/phasor-sums.html#L1369),
[Fig. 8 L1300](../../public/simulations/draw-decompose.html#L1300),
[Fig. 9 L969](../../public/simulations/driven-oscillator.html#L969),
[Fig. 10 L1048](../../public/simulations/wind-turbine.html#L1048).

## Public interface

| Name | Lines | Arguments | What it does / returns |
|---|---|---|---|
| `Sim.colourMap` | [66-73](../../public/scripts/datalog.js#L66-L73) | `v, lim` | `[r, g, b]` on a diverging scale: $a = v/\text{lim}$ clipped to $[-1, 1]$, $s = |a|^{0.8}$, mixed from the paper colour (255, 250, 243) towards dark (58, 50, 46) for negative or burgundy (122, 31, 43) for positive values. Pages use it in their `colour` functions. |
| `window.__dataPanel` | [1083](../../public/scripts/datalog.js#L1083) | | `{ running(), rounds(), recording() }`: hooks for tests. |
| `Sim.data` | [11-26](../../public/scripts/datalog.js#L11-L26) | | The contract above, provided by the page. |

## Internal functions

| Name | Lines | What it does |
|---|---|---|
| `load`, `store` | [44-45](../../public/scripts/datalog.js#L44-L45) | Read and write `localStorage` under `datapanel.`; silent if storage is blocked. |
| `esc` | [46](../../public/scripts/datalog.js#L46) | Escapes `&`, `<`, `>`. |
| `plain` | [47](../../public/scripts/datalog.js#L47) | HTML symbol to text: `<sub>x</sub>` → `_x`, `<sup>x</sup>` → `^x`, tags removed. |
| `grouped` | [48-52](../../public/scripts/datalog.js#L48-L52) | Integer with a space every three digits when longer than four digits. |
| `num` | [53-60](../../public/scripts/datalog.js#L53-L60) | Display text of any value: `—` for missing or non-finite, `True`/`False`, grouped integers, else `Sim.fmt` with 4 decimals by default. |
| `sci` | [61](../../public/scripts/datalog.js#L61) | Exponent notation with 2 decimals. |
| `textOn` | [62](../../public/scripts/datalog.js#L62) | Dark or light text on a coloured cell (luminance threshold 150). |
| `safe` | [63](../../public/scripts/datalog.js#L63) | Runs a function; returns the fallback if it throws. Every call into page code goes through it. |
| `clock` | [64](../../public/scripts/datalog.js#L64) | Wall-clock time `HH:MM:SS`. |
| `V`, `A`, `sym`, `digitsOf`, `unitOf` | [77-81](../../public/scripts/datalog.js#L77-L81) | Variable record, attributes, symbol, decimals (default 4), units. |
| `kindOf`, `typeLabel`, `shapeLabel` | [82-88](../../public/scripts/datalog.js#L82-L88) | `scalar`/`vector`/`matrix`, type text, shape text. |
| `rows2`, `cols2`, `colourFn`, `isNumScalar` | [89-92](../../public/scripts/datalog.js#L89-L92) | 2-D sizes; the page's colour function; whether a scalar is `float`, `int` or `bool`. |
| `R` (IIFE) | [97-100](../../public/scripts/datalog.js#L97-L100) | Fallback round: ten seconds of `log` columns. |
| `timeNow`, `timeSym`, `timeUnit`, `timeText`, `timeHTML` | [102-107](../../public/scripts/datalog.js#L102-L107) | The round's time variable and its display. |
| `palette`, `tok` | [178-184](../../public/scripts/datalog.js#L178-L184) | Colours from the panel's CSS tokens, cached. |
| `stats` | [212-219](../../public/scripts/datalog.js#L212-L219) | Min, max, mean of an array, cached by version. |
| `describe` | [220-232](../../public/scripts/datalog.js#L220-L232) | Value cell and shape of one ledger row. |
| `drawThumb` | [234-278](../../public/scripts/datalog.js#L234-L278) | 128 × 34 px line or heat map. |
| `paintVars` | [279-291](../../public/scripts/datalog.js#L279-L291) | Repaints ledger rows that changed. |
| `paintInstant` | [293-298](../../public/scripts/datalog.js#L293-L298) | The "Values at …" line. |
| `catchNow` | [299-304](../../public/scripts/datalog.js#L299-L304) | Catches a new instant. |
| `makeGrid` | [307-371](../../public/scripts/datalog.js#L307-L371) | Virtual table; inner `sizeTo`, `layout`, `fill`, `paintGrid`, `mark`, `onPoint` ([313-362](../../public/scripts/datalog.js#L313-L362)). |
| `takeSnap`, `snapStats` | [374-384](../../public/scripts/datalog.js#L374-L384) | Copy of the arrays at one instant, and its statistics. |
| `checkButton` | [385-387](../../public/scripts/datalog.js#L385-L387) | A "Check" button for one element. |
| `gridSource` | [388-420](../../public/scripts/datalog.js#L388-L420) | Adapts a 1-D group or a 2-D array to the table. |
| `paintArray`, `openArray` | [421-460](../../public/scripts/datalog.js#L421-L460) | Array view header and table. |
| `openCheck`, `agreement`, `runCheck` | [479-535](../../public/scripts/datalog.js#L479-L535) | Check view. |
| `stageXY`, `refAt`, `setRead` | [547-565](../../public/scripts/datalog.js#L547-L565) | Pointer position in the figure; probe with rings; Read on/off. |
| `fitOverlay`, `pinAt`, `own`, `up` | [595-635](../../public/scripts/datalog.js#L595-L635) | Overlay sizing; pinning; capturing the gesture; end of drag. |
| `touched`, `wipe`, `drawRing`, `drawPin`, `clearOverlay` | [641-661](../../public/scripts/datalog.js#L641-L661) | Overlay drawing with dirty rectangles. |
| `paintProbe` | [663-687](../../public/scripts/datalog.js#L663-L687) | Marker every frame; words at most every 250 ms. |
| `rowsKey`, `paintStrip` | [688-736](../../public/scripts/datalog.js#L688-L736) | The strip and the "Pinned point" table. |
| `roundLength`, `describeRound`, `scalarNames` | [747-754](../../public/scripts/datalog.js#L747-L754) | Round length (default 10), the Record box text, numeric scalars. |
| `startRound`, `progress`, `recordFrame`, `finishRound` | [755-842](../../public/scripts/datalog.js#L755-L842) | Recording. |
| `seriesRange`, `drawChart` | [845-880](../../public/scripts/datalog.js#L845-L880) | Range without NaN; one chart with optional cursor. |
| `renderRounds` | [881-940](../../public/scripts/datalog.js#L881-L940) | Rounds view; inner `readout`, `drawAll`, `pick`. |
| `roundCsv`, `download`, `stamp`, `readme` | [941-998](../../public/scripts/datalog.js#L941-L998) | Files. |
| `show`, `setOpen` | [1007-1027](../../public/scripts/datalog.js#L1007-L1027) | Switch view; open or close the panel. |
| `paintState`, `paint` | [1046-1055](../../public/scripts/datalog.js#L1046-L1055) | The "one instant / live / recording" label; repaint of the open view. |
| `wanted`, `kick`, `frame` | [1059-1067](../../public/scripts/datalog.js#L1059-L1067) | The on-demand loop. |
| `soon` | [1080](../../public/scripts/datalog.js#L1080) | Refreshes the round description once per frame after any input or click. |

## State it keeps

- `localStorage`: `datapanel.open` (`'1'`/`'0'`), `datapanel.live` (`'1'`/`'0'`), `datapanel.tab` (`'vars'`/`'rounds'`)
  ([datalog.js:43](../../public/scripts/datalog.js#L43), [1014](../../public/scripts/datalog.js#L1014),
  [1024](../../public/scripts/datalog.js#L1024), [1040](../../public/scripts/datalog.js#L1040)). The keys are the same for every
  page, so the choice carries from one figure to the next.
- In memory: `isOpen`, `view`, `liveOn` ([1006](../../public/scripts/datalog.js#L1006)); `caught` (time and reason of the
  instant, [292](../../public/scripts/datalog.js#L292)); `current`, `snap`, `grid` (open table, [373](../../public/scripts/datalog.js#L373));
  `checking` ([478](../../public/scripts/datalog.js#L478)); `held = { ref, cell }` and `probe` (Read values state,
  [541-542](../../public/scripts/datalog.js#L541-L542)); `rounds` (at most 5), `roundNo`, `rec` (the recording),
  `sel` ([743](../../public/scripts/datalog.js#L743)); `running` ([1058](../../public/scripts/datalog.js#L1058)); `statCache`.
  Rounds are lost on reload.
- DOM attributes and classes written: `body.dp-open`; `aria-expanded` on the tab; `aria-hidden` and `inert` on the closed panel
  ([1018-1027](../../public/scripts/datalog.js#L1018-L1027)); `#stage.dp-reading` while reading
  ([561](../../public/scripts/datalog.js#L561)); `aria-pressed` on the Read button; `.dp-tab--away` while scrolling down on a
  phone ([122-129](../../public/scripts/datalog.js#L122-L129)); `.dp-rec.is-rec` while recording.
- DOM read: `#stage`, the `.stage__cap` inside `#stage`'s parent ([588](../../public/scripts/datalog.js#L588)), CSS tokens `--accent`,
  `--ink`, `--ink-3`, `--rule`, `--muted`, `--card-soft` ([182](../../public/scripts/datalog.js#L182)).

## Timing and events

| What | Rate | Where |
|---|---|---|
| Panel loop | one animation frame while `wanted()`; none otherwise | [1059-1067](../../public/scripts/datalog.js#L1059-L1067) |
| Live: ledger values | every frame | [1053](../../public/scripts/datalog.js#L1053) |
| Live: thumbnails | at most every 250 ms, only after a version change | [285](../../public/scripts/datalog.js#L285) |
| Read values: marker | every frame | [671-674](../../public/scripts/datalog.js#L671-L674) |
| Read values: words | at most every 250 ms (4 per second; measured 3.7) | [686](../../public/scripts/datalog.js#L686) |
| Outline before a click | after 300 ms of rest | [631](../../public/scripts/datalog.js#L631) |
| Table cell shown in the figure | 600 ms after a hover, 3000 ms after a click | [456](../../public/scripts/datalog.js#L456) |
| Recording: samples | every frame or every $L/600$, at most 600 | [797-798](../../public/scripts/datalog.js#L797-L798) |
| Recording: progress bar | every 125 ms (8 per second) | [813](../../public/scripts/datalog.js#L813) |
| First instant | two animation frames after load | [1077](../../public/scripts/datalog.js#L1077) |
| Round description | at most once per frame, after an `input` or `click` anywhere | [1079-1082](../../public/scripts/datalog.js#L1079-L1082) |
| Object URL of a download | revoked after 4 s | [955](../../public/scripts/datalog.js#L955) |

Listeners: `window` `scroll` (passive) for the phone pill; `pointerdown`, `pointermove`, `pointerup`, `pointercancel` and
`click`, `mousedown`, `mouseup`, `dblclick`, `contextmenu` on `#stage` in the capture phase, all inactive unless Read values is
on; `pointerleave` on `#stage`; `keydown` on `document` (Esc stops reading) and on the panel (Esc closes it); clicks on the
tab, close button, tabs, Catch now, Live, Record, Save and inside the panes; `pointermove`/`pointerdown`/`pointerleave` on the
round charts; `visibilitychange` (restarts the loop when the page shows again); `input` and `click` on `document` in the
capture phase for `soon()`; `ResizeObserver` on `#stage` and on the table.

## Contracts with other files

- **`dataset.js`**: the store and its fields `title`, `dims`, `vars`, `order`, methods `get`, `dtype`, `along`, `has`, `npz`
  and the `Dataset` constructor for round archives ([dataset.md](dataset.md)).
- **`sim.js`**: `Sim.fmt` for every number ([datalog.js:59](../../public/scripts/datalog.js#L59)); `readPixel` and
  `isBurgundy` are used by the `drawn` functions of Figs. 9 and 10 ([sim.md](sim.md)).
- **The page**: `Sim.data` (above), `#stage` with a sibling `.stage__cap`, and the CSS tokens. Each page's documentation
  lists its probe, checks and read-backs ([../simulations/](../simulations/)).
- **`styles/data.css`**: every `dp-*`, `dg__*` class ([../styles.md](../styles.md)).
- **`catalog.js`** advertises the panel's tools (`data`, `read`, `round`, `check`) in `SIM_TOOLS` ([catalog.md](catalog.md)).

## How to change it safely

- Keep the panel a reader. A number that the panel needs and the store lacks belongs in the page, written into the store at the
  line that computes it (CLAUDE.md, "A data table is a pipeline").
- Keep calls into page code inside `safe()`: a throwing `check` or `inspect` must not stop the loop or the page.
- Keep `wanted()` honest. Anything that starts per-frame work must be covered by it, and must stop when its condition ends;
  check with `__dataPanel.running()` that the loop is off when the panel is idle.
- Keep the Read values listeners in the capture phase and keep the `if (probe.on)` guard first, or the figure stops behaving as
  if the file were absent.
- Text that changes while a figure runs: at most 4 rewrites per second (the 250 ms at line 686). Measure after a change: what
  shows during a pointer sweep, how much of the figure the marker covers, how often the strip text changes.
- If you add a key to `Sim.data`, add it to the contract comment at the top of the file, which pages and maintainers read first.
- After changing the archive, re-run the Python check: `zipfile.ZipFile(f).testzip()` returns `None`, `numpy.load(f)` lists the
  arrays, `dataset.json` loads.

## Notes for maintainers

1. The contract comment ([datalog.js:11-26](../../public/scripts/datalog.js#L11-L26)) omits four keys the code reads and the
   pages set: `kicker` ([136](../../public/scripts/datalog.js#L136)), `rowLabel` ([399](../../public/scripts/datalog.js#L399)),
   `colLabel` ([412](../../public/scripts/datalog.js#L412)) and `at` ([402](../../public/scripts/datalog.js#L402)).
2. Fig. 8 sets `Sim.data.touchProbe` ([draw-decompose.html:1402](../../public/simulations/draw-decompose.html#L1402)); nothing
   reads it.
3. The fallback to `Sim.data.log` ([datalog.js:97-100](../../public/scripts/datalog.js#L97-L100)) is dead: all ten pages define
   `round`.
4. The README's Python opens `'<file>.zip'` ([datalog.js:988](../../public/scripts/datalog.js#L988)), but the saved file is
   named `<file>-<stamp>.zip` ([datalog.js:1002](../../public/scripts/datalog.js#L1002)) or `<file>-round-<n>-<stamp>.zip`
   ([datalog.js:972](../../public/scripts/datalog.js#L972)); the reader must rename the file or edit the line.
5. `paintStrip(force)` never uses its parameter ([datalog.js:689](../../public/scripts/datalog.js#L689)).
6. In sampled mode the 600-sample cap is reached one frame before the end of the round, so the sample at the round's end is
   not stored: on Fig. 2 the last of 600 samples sits at 9.983 s of a 10 s round
   ([datalog.js:797-798](../../public/scripts/datalog.js#L797-L798), [814](../../public/scripts/datalog.js#L814)).
7. Hovering a cell of an array table, without a click, draws a ring on the running figure for 0.6 s
   ([datalog.js:363](../../public/scripts/datalog.js#L363), [456](../../public/scripts/datalog.js#L456)). The pointer crosses the
   table, not the figure, but the figure changes. CLAUDE.md asks that nothing on a running figure react to the pointer merely
   crossing; whether this case is meant to be covered is not determined from the code.
8. Pressing Esc while focus is inside the panel and Read values is on does two things at once: it closes the panel
   ([datalog.js:1030](../../public/scripts/datalog.js#L1030)) and stops reading ([datalog.js:638](../../public/scripts/datalog.js#L638)).
9. AGENTS.md says the load order holds for "all eight figures"; it now holds for all ten pages (load-order table in
   [sim.md](sim.md#load-order-on-the-pages)).
