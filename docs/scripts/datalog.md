# public/scripts/datalog.js

| | |
|---|---|
| File | [public/scripts/datalog.js](../../public/scripts/datalog.js), 1089 lines, 77.2 kB (77 171 bytes) |
| Loaded by | the ten simulation pages, last, after the page's own script (line numbers in the load-order table of [sim.md](sim.md#load-order-on-the-pages)); styles in [styles/data.css](../../public/styles/data.css), linked in each page's head (for example [Double Pendulum.html:12](../../public/simulations/Double%20Pendulum.html#L12)) |
| Reads | `Sim.data` (the page's contract, below) and through it the page's dataset ([datalog.js:43-44](../../public/scripts/datalog.js#L43-L44)) |
| Defines | `Sim.colourMap` ([datalog.js:71](../../public/scripts/datalog.js#L71)), `window.__dataPanel` ([datalog.js:1092](../../public/scripts/datalog.js#L1092)) |
| Adds to the page | `button.dp-tab` and `aside#data-panel.dp` at the end of `<body>` ([datalog.js:171-172](../../public/scripts/datalog.js#L171-L172)); `canvas.dp-overlay` inside `#stage`, `div.dp-read` right after `#stage`, `button.dp-readbtn` in the figure caption ([datalog.js:571-593](../../public/scripts/datalog.js#L571-L593)) |

`datalog.js` is the data panel: a variable explorer in the manner of Spyder's, fed by the page's one store
([dataset.md](dataset.md)). It shows every variable at one caught instant (Variables), repaints them every frame only when
the reader switches Live on, opens arrays as tables copied at one instant, lets the reader pin a point of the figure and read
its values (Read values), checks any value three ways (Check: stored, recomputed, read back from the picture), records one
round of the running simulation (Record), and saves everything as a NumPy archive with CSV and a README (Save). It never
computes physics and never writes to the store. When nobody is looking it does no work at all
([datalog.js:1-40](../../public/scripts/datalog.js#L1-L40)).

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
   ([datalog.js:43-44](../../public/scripts/datalog.js#L43-L44)).
2. It defines its helpers and `Sim.colourMap` ([datalog.js:47-78](../../public/scripts/datalog.js#L47-L78)), then reads the
   store through short accessors `V`, `A`, `sym`, `digitsOf`, `unitOf` ([datalog.js:81-96](../../public/scripts/datalog.js#L81-L96)).
3. It lists the variables to show: the names in `Sim.data.groups`, in order, that exist in the store
   ([datalog.js:97-98](../../public/scripts/datalog.js#L97-L98)).
4. It reads what one round is, `R` ([datalog.js:101-104](../../public/scripts/datalog.js#L101-L104)), the time variable `TV`
   ([datalog.js:105](../../public/scripts/datalog.js#L105)) and the round's chart columns, the numeric scalars of
   `round.columns` other than time ([datalog.js:112](../../public/scripts/datalog.js#L112)).
5. It builds the tab button and the panel: header (kicker, Save, Close, title), the Record box, two tabs (Variables, Rounds),
   four panes (`vars`, `array`, `check`, `rounds`) and an explanation "How the numbers and the picture are tied" that ends with
   the page's own `about` paragraph ([datalog.js:121-169](../../public/scripts/datalog.js#L121-L169)).
6. It writes the Variables ledger once ([datalog.js:191-213](../../public/scripts/datalog.js#L191-L213)).
7. If the page has `#stage` and `Sim.data` has `probe` and `inspect`, it adds the Read values button, the overlay canvas and
   the strip, with their pointer listeners ([datalog.js:570-643](../../public/scripts/datalog.js#L570-L643)).
8. It restores the reader's choices from `localStorage` and opens the panel if it was open last time, or, the first time, if
   the window is at least 1500 px wide ([datalog.js:1079-1084](../../public/scripts/datalog.js#L1079-L1084)).
9. Two animation frames later, after the simulation has drawn twice, it catches the first instant, so the ledger shows a real
   frame and not the empty start ([datalog.js:1086](../../public/scripts/datalog.js#L1086)).

### The loop that runs only when needed

The panel has one `requestAnimationFrame` loop, and it runs only while `wanted()` is true: a round is recording, Read values
is on with a pin or an outline showing, a table cell's position is being shown in the figure, the panel is open with Live on,
or a marker still has to be wiped ([datalog.js:1068](../../public/scripts/datalog.js#L1068)). Any action that may need it calls
`kick()`, which starts the loop if it is not running ([datalog.js:1069](../../public/scripts/datalog.js#L1069)). Each frame does,
in order: record one sample, draw the probe overlay, repaint the open view if Live is on, and either request the next frame or
stop and wipe the overlay ([datalog.js:1070-1076](../../public/scripts/datalog.js#L1070-L1076)).

Animation-frame callbacks run in the order they were requested. The page's clock requests its next frame inside its own
callback ([sim.js:185](../../public/scripts/sim.js#L185)), before any later `kick()` can, so in every frame the panel reads
the store after the simulation has written it, as the comment says ([datalog.js:1066](../../public/scripts/datalog.js#L1066)).

Measured in headless Chromium on Fig. 2 (window 1600 × 1000, panel open at load): with Live off and Read values off,
`__dataPanel.running()` is `false`; with Read values switched on but nothing pinned, it is still `false`.

### Variables: one caught instant

Each group becomes a numbered section; each variable a row with its symbol, long name, value, a type label (`array of
float64`, or the scalar type), its shape (`q 4 × …`) and its variable name with `computed_in`
([datalog.js:192-206](../../public/scripts/datalog.js#L192-L206)). A scalar row ends in a Check button; an array row shows a
128 × 34 px thumbnail (a line for 1-D, a heat map for 2-D) and its range, and opens as a table
([datalog.js:224-282](../../public/scripts/datalog.js#L224-L282)). The heat map uses the page's `colour` function for that
variable or else `Sim.colourMap` with a symmetric limit $\max(|\min|, |\max|)$ ([datalog.js:249-253](../../public/scripts/datalog.js#L249-L253)).
Min, max and mean skip NaN and infinite values and are cached until the variable's version changes
([datalog.js:216-223](../../public/scripts/datalog.js#L216-L223)).

`catchNow(why)` records the time and the reason, re-copies an open table, re-runs an open Check and repaints
([datalog.js:303-308](../../public/scripts/datalog.js#L303-L308)). It is called when the panel opens, on Catch now, when Live is
switched off, and at the end of a round ([datalog.js:1034](../../public/scripts/datalog.js#L1034),
[1046](../../public/scripts/datalog.js#L1046), [1050](../../public/scripts/datalog.js#L1050),
[846](../../public/scripts/datalog.js#L846)). The line above the ledger says which instant is shown, for example
"Values at t = 3.41 s · caught when the panel opened" ([datalog.js:297-302](../../public/scripts/datalog.js#L297-L302)).
With Live on, `paint(false)` runs every frame: values every frame, thumbnails at most every 250 ms and only when the version
moved ([datalog.js:283-295](../../public/scripts/datalog.js#L283-L295)).

### Arrays as tables

Opening an array copies it (`slice()`) at one instant, so every cell shows the same frame
([datalog.js:378-383](../../public/scripts/datalog.js#L378-L383)). A 2-D variable is shown as rows × columns. A 1-D variable is
shown together with every other 1-D variable over the same dimension, coordinates first, one column each, from `ds.along`
([datalog.js:379](../../public/scripts/datalog.js#L379), [dataset.js:102](../../public/scripts/dataset.js#L102)). Above the table:
shape, min, max and mean, or the list of variables along the dimension, and "Copied at t = …"
([datalog.js:425-439](../../public/scripts/datalog.js#L425-L439)).

The table is virtual: only the cells inside the scrolled window exist in the DOM. Cells are 74 × 28 px (108 px wide for 1-D),
the row header 56 px (64 px for 1-D), the column header 32 px ([datalog.js:312](../../public/scripts/datalog.js#L312),
[datalog.js:397](../../public/scripts/datalog.js#L397)). On every scroll or resize `layout()` works out the first and last
visible row and column, rebuilds only if that window changed, and `fill()` writes a cell's text and background only when
they changed ([datalog.js:322-349](../../public/scripts/datalog.js#L322-L349)). Measured on Fig. 1 (window 1600 × 1000): the
162 × 360 array `C`, 58 320 numbers, was shown with 80 cell elements and 18 header elements, 104 elements in the whole table.

Pointing at a cell (mouse over or click) shows its index and value with a Check button under the table and, if the page has
`locate`, marks where that element is drawn in the figure with a ring: for 0.6 s after a hover, 3 s after a click or tap
([datalog.js:359-366](../../public/scripts/datalog.js#L359-L366), [datalog.js:457-461](../../public/scripts/datalog.js#L457-L461),
[datalog.js:679-689](../../public/scripts/datalog.js#L679-L689)).

### Read values

Off, the figure behaves as if this file were absent. On, the gesture belongs to the reading: the panel's listeners run in the
capture phase and stop the event before the page's own handlers see it, so a click does not add a source or start a drawing
([datalog.js:618-641](../../public/scripts/datalog.js#L618-L641)).

- **Pin.** A press asks the page's `probe(x, y)` what lies under the pointer. If nothing does, it tries 8 points on a ring
  12 px out, then 8 on a ring 22 px out, so a finger finds a small moving object ([datalog.js:553-559](../../public/scripts/datalog.js#L553-L559)).
  A drag keeps re-pinning ([datalog.js:629](../../public/scripts/datalog.js#L629)). A press on empty space says "Nothing to pin
  there" ([datalog.js:700](../../public/scripts/datalog.js#L700)).
- **Marker.** Every frame the overlay is wiped and the pin is drawn at `inspect(ref).at`, so it rides on the moving object: a
  ring of radius 11 px with a light halo and four ticks out to 18 px ([datalog.js:652-660](../../public/scripts/datalog.js#L652-L660),
  [datalog.js:675-678](../../public/scripts/datalog.js#L675-L678)). Only the rectangles drawn last frame are cleared, unless
  there are more than six ([datalog.js:644-650](../../public/scripts/datalog.js#L644-L650)).
- **Words.** The title and values go into a strip under the figure, between the figure and its caption, so they never cover
  it ([datalog.js:576-583](../../public/scripts/datalog.js#L576-L583)). They are rewritten at most every 250 ms
  ([datalog.js:690](../../public/scripts/datalog.js#L690)); the row structure is rebuilt only when the list of rows changes,
  otherwise only changed numbers are written ([datalog.js:705-717](../../public/scripts/datalog.js#L705-L717)). Each value that
  names a dataset variable is a button that opens Check. The same values appear in the panel under "Pinned point"
  ([datalog.js:720-739](../../public/scripts/datalog.js#L720-L739)).
- **Outline before a click.** With a mouse, moving shows nothing. Resting 0.3 s outlines, with a thin dark ring of radius 9 px,
  what a click would pin ([datalog.js:630-635](../../public/scripts/datalog.js#L630-L635), [datalog.js:671-674](../../public/scripts/datalog.js#L671-L674)).
- **Stop.** The button again, or Esc ([datalog.js:594](../../public/scripts/datalog.js#L594), [datalog.js:642](../../public/scripts/datalog.js#L642)).

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

`openCheck(name, idx)` shows one value of one variable ([datalog.js:483-491](../../public/scripts/datalog.js#L483-L491)), and
`runCheck()` writes three sections, all from the same frame ([datalog.js:500-539](../../public/scripts/datalog.js#L500-L539)):

1. **Stored in the dataset**: the value, its variable name and index, type, `computed_in`, `updates`, `formula`.
2. **Recomputed now, from the stored inputs**: the page's `check[name](idx)` returns a formula, a table of inputs and a value;
   `agreement()` compares it with the stored value ([datalog.js:492-499](../../public/scripts/datalog.js#L492-L499)). With
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

A round is what the page says it is, in `Sim.data.round` ([datalog.js:25-27](../../public/scripts/datalog.js#L25-L27)):

| Fig. | One round | Time variable | Mode | Can be blocked | Line |
|---|---|---|---|---|---|
| 1 | one period of the sources, $T$ | `t` | sampled | no | [L892](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L892) |
| 2 | ten seconds of simulated motion | `t` | sampled | no | [L851](../../public/simulations/Double%20Pendulum.html#L851) |
| 3 | ten seconds of slider changes | `wall` | `'change'` | no | [L910](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L910) |
| 4 | one period, $T$ | `t` | sampled | no | [L1072](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1072) |
| 5 | one period, $T$ | `t` | sampled | no | [L878](../../public/simulations/water-wave.html#L878) |
| 6 | one repeat of the pattern, at most 20 s | `t` | sampled | no | [L951](../../public/simulations/wave-interference.html#L951) |
| 7 | one full figure (or part of it) in phasor time | `t` | sampled | yes, in the final-shape view | [L1462](../../public/simulations/phasor-sums.html#L1462) |
| 8 | one loop of the circles | `t` | sampled | yes, until a shape is decomposed | [L1398](../../public/simulations/draw-decompose.html#L1398) |
| 9 | one drive period $1/f$ of the stored run | `t_play` | sampled | yes, near the end of the run | [L1093](../../public/simulations/driven-oscillator.html#L1093) |
| 10 | one rotor turn of the stored run | `t_play` | sampled | yes, near the end of the run | [L1138](../../public/simulations/wind-turbine.html#L1138) |

`startRound()` ([datalog.js:761-784](../../public/scripts/datalog.js#L761-L784)) refuses with the page's reason if `blocked`
returns one; the idle description keeps the reason visible and progress shows it if a round later becomes blocked, presses Play if the simulation is paused, chooses the point to follow (the pinned point, else `round.point()`),
and prepares one buffer per numeric scalar of the whole store (`scalarNames()`, every scalar of type `float`, `int` or
`bool`), one per row of the followed point, and two for time. It also notes the first group's scalars as the round's
parameters. In sampled mode the target spacing is the round length over 600; the final slot is reserved for the ending frame. In change mode it is zero and the 600-change cap is unchanged.

`recordFrame()` runs once per frame while recording ([datalog.js:793-823](../../public/scripts/datalog.js#L793-L823)). It reads
the time variable (or `performance.now()` if there is none, [datalog.js:106](../../public/scripts/datalog.js#L106)); the first
frame sets $t_0$, and the elapsed time is $t - t_0$. A frame is taken when

- sampled mode: it is the first, or at least $0.999 \cdot L/600$ after the last taken one, or the round has ended (within 10⁻⁹ s);
- change mode: the joined values of `round.columns` differ from the last frame's.

At most 600 samples are taken; sampled rounds reserve slot 600 for the ending frame (`MAXS`, [datalog.js:747](../../public/scripts/datalog.js#L747)). A taken frame stores $t$, the
elapsed time, every numeric scalar (booleans as 1 or 0, anything else not numeric as NaN), and each row of the followed point,
or NaN when the page's rows for that point changed shape ([datalog.js:807-815](../../public/scripts/datalog.js#L807-L815)). The
progress bar is repainted every 125 ms ([datalog.js:819-821](../../public/scripts/datalog.js#L819-L821)). The round ends when
the elapsed time reaches $L$ (or, in change mode, at 600 samples), when Stop is pressed, or when time runs backwards because
the page restarted ("the clock was reset", [datalog.js:798](../../public/scripts/datalog.js#L798)). A round with fewer than two
samples is dropped with a message ([datalog.js:831](../../public/scripts/datalog.js#L831)).

`finishRound()` turns the buffers into `Float64Array` series: time first, then one per chart column, then one per row of the
followed point, keyed `<variable>[_<index>]_at_point` ([datalog.js:824-850](../../public/scripts/datalog.js#L824-L850)). The
last five rounds are kept ([datalog.js:842](../../public/scripts/datalog.js#L842)); the panel opens on the Rounds tab. Each
round shows: chips to switch rounds, the parameters at the start, one chart per quantity that changed (black lines for the
followed point, burgundy for the rest), one line for quantities that stayed constant or were undefined, and a collapsible
table of every sample ([datalog.js:889-924](../../public/scripts/datalog.js#L889-L924)). Pointing at a chart draws a cursor on
every chart at the nearest sample and lists all values at it ([datalog.js:935-947](../../public/scripts/datalog.js#L935-L947)).

Measured on Fig. 2: a 10 s round gave 600 samples from 601 frames, 15 series (time, 7 columns, 7 rows of the followed bob) and
52 recorded scalars after adding the twin screen coordinates; a controlled 60 Hz run now keeps the ending sample at 10.000000000000776 s (the 7.8 × 10⁻¹³ s gap is float64 accumulation).

### Save: what goes into the files

| Button | File name | Contents | Lines |
|---|---|---|---|
| Save (panel header) | `<file>-<stamp>.zip` | the store via `ds.npz`: one `.npy` per array, `dataset.json`; then `round-<n>.csv` for each kept round and `README.txt` | [1007-1012](../../public/scripts/datalog.js#L1007-L1012) |
| Save this round | `<file>-round-<n>-<stamp>.zip` | a new dataset with dimension `sample`, coordinate `time_into_round`, one `float64` variable per series and per recorded scalar, attributes (page, round label, samples, frames, time caught, time variable, followed point, `start_<parameter>`); plus `round.csv` and `README.txt` | [972-982](../../public/scripts/datalog.js#L972-L982) |
| CSV | `<file>-round-<n>-<stamp>.csv` | the round as CSV | [971](../../public/scripts/datalog.js#L971) |

`<file>` is `Sim.data.file` (for example `fig2-double-pendulum`, [Double Pendulum.html:769](../../public/simulations/Double%20Pendulum.html#L769));
`<stamp>` is the UTC time as `YYYY-MM-DDTHH-MM-SS` ([datalog.js:965](../../public/scripts/datalog.js#L965)). The download goes
through a temporary object URL that is revoked after 4 s ([datalog.js:956-964](../../public/scripts/datalog.js#L956-L964)).

The CSV ([datalog.js:949-955](../../public/scripts/datalog.js#L949-L955)) has the header `sample,time_into_round,` then the series
keys, then every other recorded scalar; one row per sample, numbers written with `String(v)` (full double precision), NaN as an
empty cell, `\n` line ends. Units are not in the CSV; they are in the round archive's `dataset.json`.

The actual filename is generated once and passed to both the README and the download, for the store and for an individual round.

The README ([datalog.js:986-1006](../../public/scripts/datalog.js#L986-L1006)) names the page and the time, explains the layout and
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
([datalog.js:8-30](../../public/scripts/datalog.js#L8-L30)). Keys in the left column are read where shown; the right column says
which pages set them (from the ten `Sim.data = {` blocks).

| Key | Shape | Read at | Set by |
|---|---|---|---|
| `ds` | the dataset | [43](../../public/scripts/datalog.js#L43) | all |
| `kicker` | text above the title (default: the dataset title) | [140](../../public/scripts/datalog.js#L140) | all, not in the comment |
| `file` | base name of saved files | [971](../../public/scripts/datalog.js#L971), [980](../../public/scripts/datalog.js#L980), [1008](../../public/scripts/datalog.js#L1008) | all |
| `playing` | `() → bool` | [765](../../public/scripts/datalog.js#L765), [787](../../public/scripts/datalog.js#L787) | all |
| `play` | `() → void` | [765](../../public/scripts/datalog.js#L765) | all except Fig. 3 |
| `groups` | `[{ title, note, vars }]` | [98](../../public/scripts/datalog.js#L98), [192](../../public/scripts/datalog.js#L192), [772](../../public/scripts/datalog.js#L772) | all |
| `colour` | `{ name: (value, j, i) → [r, g, b] \| null }`, presentation only | [95](../../public/scripts/datalog.js#L95) | all except Figs. 2 and 10 |
| `rowLabel` | `{ dim: (j) → text }` | [403](../../public/scripts/datalog.js#L403), [417](../../public/scripts/datalog.js#L417) | Figs. 2, 3, 5, 6, 7, 8; not in the comment |
| `colLabel` | `{ name: (i) → html }` | [416](../../public/scripts/datalog.js#L416) | Figs. 1, 2; not in the comment |
| `at` | `{ name: (j[, i]) → html }`, a note after a table cell's value | [406](../../public/scripts/datalog.js#L406), [420](../../public/scripts/datalog.js#L420) | Figs. 1, 2; not in the comment |
| `probe` | `(x, y) → ref \| null`, CSS px in `#stage` | [554](../../public/scripts/datalog.js#L554) | all |
| `inspect` | `(ref) → { title, at: {x, y}, rows: [[symbol, value, units, varName, index]] }` | [672](../../public/scripts/datalog.js#L672), [695](../../public/scripts/datalog.js#L695), [810](../../public/scripts/datalog.js#L810) | all |
| `locate` | `(varName, index) → {x, y} \| null` | [680](../../public/scripts/datalog.js#L680) | all |
| `check` | `{ name: (index) → { formula, inputs: [[symbol, value, units, digits]], value } }` | [513](../../public/scripts/datalog.js#L513) | all |
| `drawn` | `{ name: (index) → { what, drawn, expected, ok, note } }` | [527](../../public/scripts/datalog.js#L527) | all |
| `round` | `{ label, time, length, columns, point, mode?, blocked? }` | [101](../../public/scripts/datalog.js#L101) | all (table above) |
| `log` | `{ time, mode, columns }`, used only when `round` is missing | [102](../../public/scripts/datalog.js#L102) | none |
| `about` | HTML paragraph: what still differs between store and picture | [168](../../public/scripts/datalog.js#L168) | all |
| `touchProbe` | | not read | Fig. 8 only ([draw-decompose.html:1402](../../public/simulations/draw-decompose.html#L1402)) |

The ten blocks: [Fig. 1 L798](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L798),
[Fig. 2 L747](../../public/simulations/Double%20Pendulum.html#L768),
[Fig. 3 L829](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L829),
[Fig. 4 L994](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L995),
[Fig. 5 L807](../../public/simulations/water-wave.html#L810),
[Fig. 6 L864](../../public/simulations/wave-interference.html#L868),
[Fig. 7 L1369](../../public/simulations/phasor-sums.html#L1369),
[Fig. 8 L1300](../../public/simulations/draw-decompose.html#L1300),
[Fig. 9 L969](../../public/simulations/driven-oscillator.html#L969),
[Fig. 10 L1048](../../public/simulations/wind-turbine.html#L1048).

## Public interface

| Name | Lines | Arguments | What it does / returns |
|---|---|---|---|
| `Sim.colourMap` | [70-77](../../public/scripts/datalog.js#L70-L77) | `v, lim` | `[r, g, b]` on a diverging scale: $a = v/\text{lim}$ clipped to $[-1, 1]$, $s = |a|^{0.8}$, mixed from the paper colour (255, 250, 243) towards dark (58, 50, 46) for negative or burgundy (122, 31, 43) for positive values. Pages use it in their `colour` functions. |
| `window.__dataPanel` | [1092](../../public/scripts/datalog.js#L1092) | | `{ running(), rounds(), recording() }`: hooks for tests. |
| `Sim.data` | [11-30](../../public/scripts/datalog.js#L11-L30) | | The contract above, provided by the page. |

## Internal functions

| Name | Lines | What it does |
|---|---|---|
| `load`, `store` | [48-49](../../public/scripts/datalog.js#L48-L49) | Read and write `localStorage` under `datapanel.`; silent if storage is blocked. |
| `esc` | [50](../../public/scripts/datalog.js#L50) | Escapes `&`, `<`, `>`. |
| `plain` | [51](../../public/scripts/datalog.js#L51) | HTML symbol to text: `<sub>x</sub>` → `_x`, `<sup>x</sup>` → `^x`, tags removed. |
| `grouped` | [52-56](../../public/scripts/datalog.js#L52-L56) | Integer with a space every three digits when longer than four digits. |
| `num` | [57-64](../../public/scripts/datalog.js#L57-L64) | Display text of any value: `—` for missing or non-finite, `True`/`False`, grouped integers, else `Sim.fmt` with 4 decimals by default. |
| `sci` | [65](../../public/scripts/datalog.js#L65) | Exponent notation with 2 decimals. |
| `textOn` | [66](../../public/scripts/datalog.js#L66) | Dark or light text on a coloured cell (luminance threshold 150). |
| `safe` | [67](../../public/scripts/datalog.js#L67) | Runs a function; returns the fallback if it throws. Every call into page code goes through it. |
| `clock` | [68](../../public/scripts/datalog.js#L68) | Wall-clock time `HH:MM:SS`. |
| `V`, `A`, `sym`, `digitsOf`, `unitOf` | [81-85](../../public/scripts/datalog.js#L81-L85) | Variable record, attributes, symbol, decimals (default 4), units. |
| `kindOf`, `typeLabel`, `shapeLabel` | [86-92](../../public/scripts/datalog.js#L86-L92) | `scalar`/`vector`/`matrix`, type text, shape text. |
| `rows2`, `cols2`, `colourFn`, `isNumScalar` | [93-96](../../public/scripts/datalog.js#L93-L96) | 2-D sizes; the page's colour function; whether a scalar is `float`, `int` or `bool`. |
| `R` (IIFE) | [101-104](../../public/scripts/datalog.js#L101-L104) | Fallback round: ten seconds of `log` columns. |
| `timeNow`, `timeSym`, `timeUnit`, `timeText`, `timeHTML` | [106-111](../../public/scripts/datalog.js#L106-L111) | The round's time variable and its display. |
| `palette`, `tok` | [182-188](../../public/scripts/datalog.js#L182-L188) | Colours from the panel's CSS tokens, cached. |
| `stats` | [216-223](../../public/scripts/datalog.js#L216-L223) | Min, max, mean of an array, cached by version. |
| `describe` | [224-236](../../public/scripts/datalog.js#L224-L236) | Value cell and shape of one ledger row. |
| `drawThumb` | [238-282](../../public/scripts/datalog.js#L238-L282) | 128 × 34 px line or heat map. |
| `paintVars` | [283-295](../../public/scripts/datalog.js#L283-L295) | Repaints ledger rows that changed. |
| `paintInstant` | [297-302](../../public/scripts/datalog.js#L297-L302) | The "Values at …" line. |
| `catchNow` | [303-308](../../public/scripts/datalog.js#L303-L308) | Catches a new instant. |
| `makeGrid` | [311-375](../../public/scripts/datalog.js#L311-L375) | Virtual table; inner `sizeTo`, `layout`, `fill`, `paintGrid`, `mark`, `onPoint` ([317-366](../../public/scripts/datalog.js#L317-L366)). |
| `takeSnap`, `snapStats` | [378-388](../../public/scripts/datalog.js#L378-L388) | Copy of the arrays at one instant, and its statistics. |
| `checkButton` | [389-391](../../public/scripts/datalog.js#L389-L391) | A "Check" button for one element. |
| `gridSource` | [392-424](../../public/scripts/datalog.js#L392-L424) | Adapts a 1-D group or a 2-D array to the table. |
| `paintArray`, `openArray` | [425-464](../../public/scripts/datalog.js#L425-L464) | Array view header and table. |
| `openCheck`, `agreement`, `runCheck` | [483-539](../../public/scripts/datalog.js#L483-L539) | Check view. |
| `stageXY`, `refAt`, `setRead` | [551-569](../../public/scripts/datalog.js#L551-L569) | Pointer position in the figure; probe with rings; Read on/off. |
| `fitOverlay`, `pinAt`, `own`, `up` | [599-639](../../public/scripts/datalog.js#L599-L639) | Overlay sizing; pinning; capturing the gesture; end of drag. |
| `touched`, `wipe`, `drawRing`, `drawPin`, `clearOverlay` | [645-665](../../public/scripts/datalog.js#L645-L665) | Overlay drawing with dirty rectangles. |
| `paintProbe` | [667-691](../../public/scripts/datalog.js#L667-L691) | Marker every frame; words at most every 250 ms. |
| `rowsKey`, `paintStrip` | [692-740](../../public/scripts/datalog.js#L692-L740) | The strip and the "Pinned point" table. |
| `roundLength`, `describeRound`, `scalarNames` | [751-760](../../public/scripts/datalog.js#L751-L760) | Round length (default 10), the Record box text, numeric scalars. |
| `startRound`, `progress`, `recordFrame`, `finishRound` | [761-850](../../public/scripts/datalog.js#L761-L850) | Recording. |
| `seriesRange`, `drawChart` | [853-888](../../public/scripts/datalog.js#L853-L888) | Range without NaN; one chart with optional cursor. |
| `renderRounds` | [889-948](../../public/scripts/datalog.js#L889-L948) | Rounds view; inner `readout`, `drawAll`, `pick`. |
| `roundCsv`, `download`, `stamp`, `readme(what, filename)` | [949-1006](../../public/scripts/datalog.js#L949-L1006) | Files. |
| `show`, `setOpen` | [1016-1036](../../public/scripts/datalog.js#L1016-L1036) | Switch view; open or close the panel. |
| `paintState`, `paint` | [1055-1064](../../public/scripts/datalog.js#L1055-L1064) | The "one instant / live / recording" label; repaint of the open view. |
| `wanted`, `kick`, `frame` | [1068-1076](../../public/scripts/datalog.js#L1068-L1076) | The on-demand loop. |
| `soon` | [1089](../../public/scripts/datalog.js#L1089) | Refreshes the round description once per frame after any input or click. |

## State it keeps

- `localStorage`: `datapanel.open` (`'1'`/`'0'`), `datapanel.live` (`'1'`/`'0'`), `datapanel.tab` (`'vars'`/`'rounds'`)
  ([datalog.js:47](../../public/scripts/datalog.js#L47), [1023](../../public/scripts/datalog.js#L1023),
  [1033](../../public/scripts/datalog.js#L1033), [1049](../../public/scripts/datalog.js#L1049)). The keys are the same for every
  page, so the choice carries from one figure to the next.
- In memory: `isOpen`, `view`, `liveOn` ([1015](../../public/scripts/datalog.js#L1015)); `caught` (time and reason of the
  instant, [296](../../public/scripts/datalog.js#L296)); `current`, `snap`, `grid` (open table, [377](../../public/scripts/datalog.js#L377));
  `checking` ([482](../../public/scripts/datalog.js#L482)); `held = { ref, cell }` and `probe` (Read values state,
  [545-546](../../public/scripts/datalog.js#L545-L546)); `rounds` (at most 5), `roundNo`, `rec` (the recording),
  `sel` ([747](../../public/scripts/datalog.js#L747)); `running` ([1067](../../public/scripts/datalog.js#L1067)); `statCache`.
  Rounds are lost on reload.
- DOM attributes and classes written: `body.dp-open`; `aria-expanded` on the tab; `aria-hidden` and `inert` on the closed panel
  ([1027-1036](../../public/scripts/datalog.js#L1027-L1036)); `#stage.dp-reading` while reading
  ([565](../../public/scripts/datalog.js#L565)); `aria-pressed` on the Read button; `.dp-tab--away` while scrolling down on a
  phone ([126-133](../../public/scripts/datalog.js#L126-L133)); `.dp-rec.is-rec` while recording.
- DOM read: `#stage`, the `.stage__cap` inside `#stage`'s parent ([592](../../public/scripts/datalog.js#L592)), CSS tokens `--accent`,
  `--ink`, `--ink-3`, `--rule`, `--muted`, `--card-soft` ([186](../../public/scripts/datalog.js#L186)).

## Timing and events

| What | Rate | Where |
|---|---|---|
| Panel loop | one animation frame while `wanted()`; none otherwise | [1068-1076](../../public/scripts/datalog.js#L1068-L1076) |
| Live: ledger values | every frame | [1062](../../public/scripts/datalog.js#L1062) |
| Live: thumbnails | at most every 250 ms, only after a version change | [289](../../public/scripts/datalog.js#L289) |
| Read values: marker | every frame | [675-678](../../public/scripts/datalog.js#L675-L678) |
| Read values: words | at most every 250 ms (4 per second; measured 3.7) | [690](../../public/scripts/datalog.js#L690) |
| Outline before a click | after 300 ms of rest | [635](../../public/scripts/datalog.js#L635) |
| Table cell shown in the figure | 600 ms after a hover, 3000 ms after a click | [460](../../public/scripts/datalog.js#L460) |
| Recording: samples | every frame or every $L/600$, at most 600 | [804-805](../../public/scripts/datalog.js#L804-L805) |
| Recording: progress bar | every 125 ms (8 per second) | [821](../../public/scripts/datalog.js#L821) |
| First instant | two animation frames after load | [1086](../../public/scripts/datalog.js#L1086) |
| Round description | at most once per frame, after an `input` or `click` anywhere | [1088-1091](../../public/scripts/datalog.js#L1088-L1091) |
| Object URL of a download | revoked after 4 s | [963](../../public/scripts/datalog.js#L963) |

Listeners: `window` `scroll` (passive) for the phone pill; `pointerdown`, `pointermove`, `pointerup`, `pointercancel` and
`click`, `mousedown`, `mouseup`, `dblclick`, `contextmenu` on `#stage` in the capture phase, all inactive unless Read values is
on; `pointerleave` on `#stage`; `keydown` on `document` (Esc stops reading) and on the panel (Esc closes it); clicks on the
tab, close button, tabs, Catch now, Live, Record, Save and inside the panes; `pointermove`/`pointerdown`/`pointerleave` on the
round charts; `visibilitychange` (restarts the loop when the page shows again); `input` and `click` on `document` in the
capture phase for `soon()`; `ResizeObserver` on `#stage` and on the table.

## Contracts with other files

- **`dataset.js`**: the store and its fields `title`, `dims`, `vars`, `order`, methods `get`, `dtype`, `along`, `has`, `npz`
  and the `Dataset` constructor for round archives ([dataset.md](dataset.md)).
- **`sim.js`**: `Sim.fmt` for every number ([datalog.js:63](../../public/scripts/datalog.js#L63)); `readPixel` and
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

1. Fixed on 2026-10-15: the contract documents kicker, rowLabel, colLabel and at (commit `:/^Batch C: align walkthroughs and metadata; verify excerpts and stored values$`).
2. Fig. 8 sets `Sim.data.touchProbe` ([draw-decompose.html:1402](../../public/simulations/draw-decompose.html#L1402)); nothing
   reads it.
3. The fallback to `Sim.data.log` ([datalog.js:101-104](../../public/scripts/datalog.js#L101-L104)) is dead: all ten pages define
   `round`.
4. Fixed on 2026-10-15: store and round READMEs open the exact timestamped download filename; CRC and NumPy array shapes validate (commit `:/^Batch A: fix simulation and recording faults; verify in Chromium$`).
5. `paintStrip(force)` never uses its parameter ([datalog.js:693](../../public/scripts/datalog.js#L693)).
6. Fixed on 2026-10-15: sampled rounds reserve the final slot; the 600-sample, 10 s test retains its ending frame instead of stopping at 9.983 s (commit `:/^Batch A: fix simulation and recording faults; verify in Chromium$`).
7. Hovering a cell of an array table, without a click, draws a ring on the running figure for 0.6 s
   ([datalog.js:367](../../public/scripts/datalog.js#L367), [460](../../public/scripts/datalog.js#L460)). The pointer crosses the
   table, not the figure, but the figure changes. CLAUDE.md asks that nothing on a running figure react to the pointer merely
   crossing; whether this case is meant to be covered is not determined from the code.
8. Pressing Esc while focus is inside the panel and Read values is on does two things at once: it closes the panel
   ([datalog.js:1039](../../public/scripts/datalog.js#L1039)) and stops reading ([datalog.js:642](../../public/scripts/datalog.js#L642)).
9. AGENTS.md said the load order holds for "all eight figures"; it holds for all ten pages (load-order table in
   [sim.md](sim.md#load-order-on-the-pages)). Corrected to "all ten figures" on 14 October 2026.
