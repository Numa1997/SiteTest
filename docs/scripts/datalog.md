# public/scripts/datalog.js

| | |
|---|---|
| File | [public/scripts/datalog.js](../../public/scripts/datalog.js), 1090 lines, 77.4 kB (77 425 bytes) |
| Loaded by | the ten simulation pages, the two pages of Iron, Cotton and the Head (`portfolios/impact/index.html`, `ar.html`), the ideal and servo presses of the Hydraulic Press Study and Droplet Collection (`portfolios/droplet-collection/index.html`, for panels 4 and 3), last, after the page's own script (line numbers in the load-order table of [sim.md](sim.md#load-order-on-the-pages)); styles in [styles/data.css](../../public/styles/data.css), linked in each page's head (for example [Double Pendulum.html:12](../../public/simulations/Double%20Pendulum.html#L12)) |
| Reads | `Sim.data` (the page's contract, below) and through it the page's dataset ([datalog.js:43-44](../../public/scripts/datalog.js#L43-L44)) |
| Defines | `Sim.colourMap` ([datalog.js:71](../../public/scripts/datalog.js#L71)), `window.__dataPanel` ([datalog.js:1089](../../public/scripts/datalog.js#L1089)) |
| Adds to the page | `button.dp-tab` and `aside#data-panel.dp` at the end of `<body>` ([datalog.js:168-169](../../public/scripts/datalog.js#L168-L169)); `canvas.dp-overlay` inside `#stage`, `div.dp-read` right after `#stage`, `button.dp-readbtn` in the figure caption ([datalog.js:568-590](../../public/scripts/datalog.js#L568-L590)) |

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
4. It reads what one round is, `R` ([datalog.js:101-101](../../public/scripts/datalog.js#L101-L101)), the time variable `TV`
   ([datalog.js:102](../../public/scripts/datalog.js#L102)) and the round's chart columns, the numeric scalars of
   `round.columns` other than time ([datalog.js:109](../../public/scripts/datalog.js#L109)).
5. It builds the tab button and the panel: header (kicker, Save, Close, title), the Record box, two tabs (Variables, Rounds),
   four panes (`vars`, `array`, `check`, `rounds`) and an explanation "How the numbers and the picture are tied" that ends with
   the page's own `about` paragraph ([datalog.js:118-166](../../public/scripts/datalog.js#L118-L166)).
6. It writes the Variables ledger once ([datalog.js:188-210](../../public/scripts/datalog.js#L188-L210)).
7. If the page has `#stage` and `Sim.data` has `probe` and `inspect`, it adds the Read values button, the overlay canvas and
   the strip, with their pointer listeners ([datalog.js:567-640](../../public/scripts/datalog.js#L567-L640)).
8. It restores the reader's choices from `localStorage` and opens the panel if it was open last time, or, the first time, if
   the window is at least 1500 px wide ([datalog.js:1076-1081](../../public/scripts/datalog.js#L1076-L1081)).
9. Two animation frames later, after the simulation has drawn twice, it catches the first instant, so the ledger shows a real
   frame and not the empty start ([datalog.js:1083](../../public/scripts/datalog.js#L1083)).

### The loop that runs only when needed

The panel has one `requestAnimationFrame` loop, and it runs only while `wanted()` is true: a round is recording, Read values
is on with a pin or an outline showing, a table cell's position is being shown in the figure, the panel is open with Live on,
or a marker still has to be wiped ([datalog.js:1065](../../public/scripts/datalog.js#L1065)). Any action that may need it calls
`kick()`, which starts the loop if it is not running ([datalog.js:1066](../../public/scripts/datalog.js#L1066)). Each frame does,
in order: record one sample, draw the probe overlay, repaint the open view if Live is on, and either request the next frame or
stop and wipe the overlay ([datalog.js:1067-1073](../../public/scripts/datalog.js#L1067-L1073)).

Animation-frame callbacks run in the order they were requested. The page's clock requests its next frame inside its own
callback ([sim.js:184](../../public/scripts/sim.js#L184)), before any later `kick()` can, so in every frame the panel reads
the store after the simulation has written it, as the comment says ([datalog.js:1063](../../public/scripts/datalog.js#L1063)).

Measured in headless Chromium on Fig. 2 (window 1600 × 1000, panel open at load): with Live off and Read values off,
`__dataPanel.running()` is `false`; with Read values switched on but nothing pinned, it is still `false`.

### Variables: one caught instant

Each group becomes a numbered section; each variable a row with its symbol, long name, value, a type label (`array of
float64`, or the scalar type), its shape (`q 4 × …`) and its variable name with `computed_in`
([datalog.js:189-203](../../public/scripts/datalog.js#L189-L203)). A scalar row ends in a Check button; an array row shows a
128 × 34 px thumbnail (a line for 1-D, a heat map for 2-D) and its range, and opens as a table
([datalog.js:221-279](../../public/scripts/datalog.js#L221-L279)). The heat map uses the page's `colour` function for that
variable or else `Sim.colourMap` with a symmetric limit $\max(|\min|, |\max|)$ ([datalog.js:246-250](../../public/scripts/datalog.js#L246-L250)).
Min, max and mean skip NaN and infinite values and are cached until the variable's version changes
([datalog.js:213-220](../../public/scripts/datalog.js#L213-L220)).

`catchNow(why)` records the time and the reason, re-copies an open table, re-runs an open Check and repaints
([datalog.js:300-305](../../public/scripts/datalog.js#L300-L305)). It is called when the panel opens, on Catch now, when Live is
switched off, and at the end of a round ([datalog.js:1031](../../public/scripts/datalog.js#L1031),
[1043](../../public/scripts/datalog.js#L1043), [1047](../../public/scripts/datalog.js#L1047),
[843](../../public/scripts/datalog.js#L843)). The line above the ledger says which instant is shown, for example
"Values at t = 3.41 s · caught when the panel opened" ([datalog.js:294-299](../../public/scripts/datalog.js#L294-L299)).
With Live on, `paint(false)` runs every frame: values every frame, thumbnails at most every 250 ms and only when the version
moved ([datalog.js:280-292](../../public/scripts/datalog.js#L280-L292)).

### Arrays as tables

Opening an array copies it (`slice()`) at one instant, so every cell shows the same frame
([datalog.js:375-380](../../public/scripts/datalog.js#L375-L380)). A 2-D variable is shown as rows × columns. A 1-D variable is
shown together with every other 1-D variable over the same dimension, coordinates first, one column each, from `ds.along`
([datalog.js:376](../../public/scripts/datalog.js#L376), [dataset.js:93](../../public/scripts/dataset.js#L93)). Above the table:
shape, min, max and mean, or the list of variables along the dimension, and "Copied at t = …"
([datalog.js:422-436](../../public/scripts/datalog.js#L422-L436)).

The table is virtual: only the cells inside the scrolled window exist in the DOM. Cells are 74 × 28 px (108 px wide for 1-D),
the row header 56 px (64 px for 1-D), the column header 32 px ([datalog.js:309](../../public/scripts/datalog.js#L309),
[datalog.js:394](../../public/scripts/datalog.js#L394)). On every scroll or resize `layout()` works out the first and last
visible row and column, rebuilds only if that window changed, and `fill()` writes a cell's text and background only when
they changed ([datalog.js:319-346](../../public/scripts/datalog.js#L319-L346)). Measured on Fig. 1 (window 1600 × 1000): the
162 × 360 array `C`, 58 320 numbers, was shown with 80 cell elements and 18 header elements, 104 elements in the whole table.

Pointing at a cell (mouse over or click) shows its index and value with a Check button under the table and, if the page has
`locate`, marks where that element is drawn in the figure with a ring: for 0.6 s after a hover, 3 s after a click or tap
([datalog.js:356-363](../../public/scripts/datalog.js#L356-L363), [datalog.js:454-458](../../public/scripts/datalog.js#L454-L458),
[datalog.js:676-686](../../public/scripts/datalog.js#L676-L686)).

### Read values

Off, the figure behaves as if this file were absent. On, the gesture belongs to the reading: the panel's listeners run in the
capture phase and stop the event before the page's own handlers see it, so a click does not add a source or start a drawing
([datalog.js:615-638](../../public/scripts/datalog.js#L615-L638)).

- **Pin.** A press asks the page's `probe(x, y)` what lies under the pointer. If nothing does, it tries 8 points on a ring
  12 px out, then 8 on a ring 22 px out, so a finger finds a small moving object ([datalog.js:550-556](../../public/scripts/datalog.js#L550-L556)).
  A drag keeps re-pinning ([datalog.js:626](../../public/scripts/datalog.js#L626)). A press on empty space says "Nothing to pin
  there" ([datalog.js:697](../../public/scripts/datalog.js#L697)).
- **Marker.** Every frame the overlay is wiped and the pin is drawn at `inspect(ref).at`, so it rides on the moving object: a
  ring of radius 11 px with a light halo and four ticks out to 18 px ([datalog.js:649-657](../../public/scripts/datalog.js#L649-L657),
  [datalog.js:672-675](../../public/scripts/datalog.js#L672-L675)). Only the rectangles drawn last frame are cleared, unless
  there are more than six ([datalog.js:641-647](../../public/scripts/datalog.js#L641-L647)).
- **Words.** The title and values go into a strip under the figure, between the figure and its caption, so they never cover
  it ([datalog.js:573-580](../../public/scripts/datalog.js#L573-L580)). They are rewritten at most every 250 ms
  ([datalog.js:687](../../public/scripts/datalog.js#L687)); the row structure is rebuilt only when the list of rows changes,
  otherwise only changed numbers are written ([datalog.js:702-714](../../public/scripts/datalog.js#L702-L714)). Each value that
  names a dataset variable is a button that opens Check. The same values appear in the panel under "Pinned point"
  ([datalog.js:717-736](../../public/scripts/datalog.js#L717-L736)).
- **Outline before a click.** With a mouse, moving shows nothing. Resting 0.3 s outlines, with a thin dark ring of radius 9 px,
  what a click would pin ([datalog.js:627-632](../../public/scripts/datalog.js#L627-L632), [datalog.js:668-671](../../public/scripts/datalog.js#L668-L671)).
- **Stop.** The button again, or Esc ([datalog.js:591](../../public/scripts/datalog.js#L591), [datalog.js:639](../../public/scripts/datalog.js#L639)).

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

`openCheck(name, idx)` shows one value of one variable ([datalog.js:480-488](../../public/scripts/datalog.js#L480-L488)), and
`runCheck()` writes three sections, all from the same frame ([datalog.js:497-536](../../public/scripts/datalog.js#L497-L536)):

1. **Stored in the dataset**: the value, its variable name and index, type, `computed_in`, `updates`, `formula`.
2. **Recomputed now, from the stored inputs**: the page's `check[name](idx)` returns a formula, a table of inputs and a value;
   `agreement()` compares it with the stored value ([datalog.js:489-496](../../public/scripts/datalog.js#L489-L496)). With
   $d = |\text{stored} - \text{recomputed}|$ and $s = \max(|\text{stored}|, |\text{recomputed}|)$, the two agree when
   $$d \le 2\times10^{-6}\,s + 10^{-7}$$
   for a `float32` array and
   $$d \le 10^{-9}\,s + 10^{-12}$$
   otherwise. The verdict says "identical" when $d = 0$, otherwise "agree to $n$ significant figures; the rest is float32
   storage" (or "rounding"), with $n = \lfloor -\log_{10}(d/s) \rfloor$; a larger gap reads "DIFFER by …". Strings and
   booleans are compared as text; two non-finite values are "both undefined now". Without a `check` entry the section shows the
   attribute `source` or says the value is an input read from a control.
3. **Read back from the picture**: the page's `drawn[name](idx)` returns what it read (a pixel colour, an SVG attribute),
   what the store predicts, `ok` and a note. `ok` has three values ([datalog.js:529](../../public/scripts/datalog.js#L529)):
   `true` gives a drawn tick (`CHK`, an inline SVG, [datalog.js:114](../../public/scripts/datalog.js#L114)) and "The picture shows
   this value." on tan (`is-ok`); `false` gives "✕ The picture does not match." in white on the
   burgundy accent (`is-bad`); `null` means the value is not in the picture at the moment, for example a curve that is not drawn because there
   is nothing to draw. Then the verdict is neutral, without a mark: "Not in the picture at the moment, so there is nothing to
   read back.", in muted ink inside a dashed outline (`is-na`, [data.css:220](../../public/styles/data.css#L220)). Only `null`
   itself counts; a missing `ok` is falsy and reads as a mismatch. Without a `drawn` entry, the section shows `drawn_note` or
   says the value enters the picture only through arrays computed from it.

Measured on Fig. 2: the denominator `den` (stored 3.3590 kg, recomputed 3.358995) and the energy `E` (18.305709 J) are
"identical"; the bob position `x2_px` (332.6 css px) is "identical" and "The picture shows this value."

### Record one round

A round is what the page says it is, in `Sim.data.round` ([datalog.js:25-27](../../public/scripts/datalog.js#L25-L27)):

| Fig. | One round | Time variable | Mode | Can be blocked | Line |
|---|---|---|---|---|---|
| 1 | one period of the sources, $T$ | `t` | sampled | no | [L893](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L893) |
| 2 | ten seconds of simulated motion | `t` | sampled | no | [L851](../../public/simulations/Double%20Pendulum.html#L851) |
| 3 | ten seconds of slider changes | `wall` | `'change'` | no | [L938](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L938) |
| 4 | one period, $T$ | `t` | sampled | no | [L1073](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L1073) |
| 5 | one period, $T$ | `t` | sampled | no | [L878](../../public/simulations/water-wave.html#L878) |
| 6 | one repeat of the pattern, at most 20 s | `t` | sampled | no | [L961](../../public/simulations/wave-interference.html#L961) |
| 7 | one full figure (or part of it) in phasor time | `t` | sampled | yes, in the final-shape view | [L1463](../../public/simulations/phasor-sums.html#L1463) |
| 8 | one loop of the circles | `t` | sampled | yes, until a shape is decomposed | [L1399](../../public/simulations/draw-decompose.html#L1399) |
| 9 | one drive period $1/f$ of the stored run | `t_play` | sampled | yes, near the end of the run | [L1909](../../public/simulations/driven-oscillator.html#L1909) |
| 10 | one rotor turn of the stored run | `t_play` | sampled | yes, near the end of the run | [L1154](../../public/simulations/wind-turbine.html#L1154) |
| Portfolios 03, ideal press | one run, $t = 0$ to its end; Record plays it from $t = 0$ | `tView` | sampled | yes, while the run plays | `Sim.data` in [hydraulic.html](../../portfolios-src/hydraulics/hydraulic.html) |
| Portfolios 03, servo press | one press cycle, $t = 0$ to its end | `tView` | sampled | yes, before the first cycle arrives and while it plays | `Sim.data` in [hydraulic_control.html](../../portfolios-src/hydraulics/hydraulic_control.html) |
| Droplet Collection, panel 4 (a cloud with a shape) | five cloud-minutes, $t$ to $t + 300$ s; Record presses Start if the cloud is paused; the followed point is the largest drop | `t` | sampled | yes, in the last five minutes before the cloud stops at 45 min | `Sim.data` in [datahooks.js](../../portfolios-src/droplets/datahooks.js), store written in [app.js](../../portfolios-src/droplets/app.js) |
| Portfolios 04 (Iron, Cotton and the Head) | one drop, $t = 0$ to 9 s of the stored run; Record starts a new drop from $t = 0$ | `t_play` | sampled | yes, while a drop is under way | [index.html L989](../../public/portfolios/impact/index.html#L989), [ar.html](../../public/portfolios/impact/ar.html); source [datahooks.js](../../portfolios-src/impact/datahooks.js) |

While no round is running, `describeRound()` ([datalog.js:749-756](../../public/scripts/datalog.js#L749-L756)) writes the Record
box text: "One round = …", then a longer sentence in `span.dp-more-txt`, which phones hide
([data.css:326](../../public/styles/data.css#L326)). When the page's `blocked()` gives a reason, it follows, after a space, in its
own `span.dp-rec__why` ("**Not now.** …", [datalog.js:754](../../public/scripts/datalog.js#L754)). That span has no CSS rule, so
the reason shows on phones too.

`startRound()` ([datalog.js:758-781](../../public/scripts/datalog.js#L758-L781)) refuses with the page's reason if `blocked`
returns one ([761](../../public/scripts/datalog.js#L761)). If a round becomes blocked while it records, the progress line shows
the reason ("**Waiting.**", [785-786](../../public/scripts/datalog.js#L785-L786)). Otherwise it presses Play if the simulation
is paused, chooses the point to follow (the pinned point, else `round.point()`), and prepares one buffer per numeric scalar of the whole store (`scalarNames()`, every scalar of type `float`, `int` or
`bool`), one per row of the followed point, and two for time. It also notes the first group's scalars as the round's
parameters. In sampled mode the target spacing is the round length over 600; the final slot is reserved for the ending frame. In change mode it is zero and the 600-change cap is unchanged.

`recordFrame()` runs once per frame while recording ([datalog.js:790-820](../../public/scripts/datalog.js#L790-L820)). It reads
the time variable (or `performance.now()` if there is none, [datalog.js:103](../../public/scripts/datalog.js#L103)); the first
frame sets $t_0$, and the elapsed time is $t - t_0$. A frame is taken when

- sampled mode: it is the first, or at least $0.999 \cdot L/600$ after the last taken one, or the round has ended (within 10⁻⁹ s);
- change mode: the joined values of `round.columns` differ from the last frame's.

At most 600 samples are taken; sampled rounds reserve slot 600 for the ending frame (`MAXS`, [datalog.js:744](../../public/scripts/datalog.js#L744)). A taken frame stores $t$, the
elapsed time, every numeric scalar (booleans as 1 or 0, anything else not numeric as NaN), and each row of the followed point,
or NaN when the page's rows for that point changed shape ([datalog.js:804-812](../../public/scripts/datalog.js#L804-L812)). A row is matched by its label and
variable name, not by its index (since 23 October 2026): on a stored run the followed point's index moves with the playback (Figs. 9, 10, the impact
study), and matching the index as well made every sample after the first NaN. The series keeps the index of the first sample in its name. The
progress bar is repainted every 125 ms ([datalog.js:816-818](../../public/scripts/datalog.js#L816-L818)). The round ends when
the elapsed time reaches $L$ (or, in change mode, at 600 samples), when Stop is pressed, or when time runs backwards because
the page restarted ("the clock was reset", [datalog.js:795](../../public/scripts/datalog.js#L795)). A round with fewer than two
samples is dropped with a message ([datalog.js:828](../../public/scripts/datalog.js#L828)).

`finishRound()` turns the buffers into `Float64Array` series: time first, then one per chart column, then one per row of the
followed point, keyed `<variable>[_<index>]_at_point` ([datalog.js:821-847](../../public/scripts/datalog.js#L821-L847)). The
last five rounds are kept ([datalog.js:839](../../public/scripts/datalog.js#L839)); the panel opens on the Rounds tab. Each
round shows: chips to switch rounds, the parameters at the start, one chart per quantity that changed (black lines for the
followed point, burgundy for the rest), one line for quantities that stayed constant or were undefined, and a collapsible
table of every sample ([datalog.js:886-921](../../public/scripts/datalog.js#L886-L921)). Pointing at a chart draws a cursor on
every chart at the nearest sample and lists all values at it ([datalog.js:932-944](../../public/scripts/datalog.js#L932-L944)).

Measured on Fig. 2: a 10 s round gave 600 samples from 601 frames, 15 series (time, 7 columns, 7 rows of the followed bob) and
52 recorded scalars after adding the twin screen coordinates; a controlled 60 Hz run now keeps the ending sample at 10.000000000000776 s (the 7.8 × 10⁻¹³ s gap is float64 accumulation).

### Save: what goes into the files

| Button | File name | Contents | Lines |
|---|---|---|---|
| Save (panel header) | `<file>-<stamp>.zip` | the store via `ds.npz`: one `.npy` per array, `dataset.json`; then `round-<n>.csv` for each kept round and `README.txt` | [1004-1009](../../public/scripts/datalog.js#L1004-L1009) |
| Save this round | `<file>-round-<n>-<stamp>.zip` | a new dataset with dimension `sample`, coordinate `time_into_round`, one `float64` variable per series and per recorded scalar, attributes (page, round label, samples, frames, time caught, time variable, followed point, `start_<parameter>`); plus `round.csv` and `README.txt` | [969-979](../../public/scripts/datalog.js#L969-L979) |
| CSV | `<file>-round-<n>-<stamp>.csv` | the round as CSV | [968](../../public/scripts/datalog.js#L968) |

`<file>` is `Sim.data.file` (for example `fig2-double-pendulum`, [Double Pendulum.html:769](../../public/simulations/Double%20Pendulum.html#L769));
`<stamp>` is the UTC time as `YYYY-MM-DDTHH-MM-SS` ([datalog.js:962](../../public/scripts/datalog.js#L962)). The download goes
through a temporary object URL that is revoked after 4 s ([datalog.js:953-961](../../public/scripts/datalog.js#L953-L961)).

The CSV ([datalog.js:946-952](../../public/scripts/datalog.js#L946-L952)) has the header `sample,time_into_round,` then the series
keys, then every other recorded scalar; one row per sample, numbers written with `String(v)` (full double precision), NaN as an
empty cell, `\n` line ends. Units are not in the CSV; they are in the round archive's `dataset.json`.

The actual filename is generated once and passed to both the README and the download, for the store and for an individual round.

The README ([datalog.js:983-1003](../../public/scripts/datalog.js#L983-L1003)) names the page and the time, explains the layout and
gives Python to load the archive with `zipfile`, `json` and NumPy, and to build an xarray `Dataset`.

### The .npz writer, byte by byte

The writer lives in `dataset.js` ([dataset.js:103-172](../../public/scripts/dataset.js#L103-L172)); the panel is its only caller.
An `.npz` is nothing but a zip archive whose members are `.npy` files. This one is written by hand, uncompressed, so it needs
no library.

**One `.npy` file per array** (`npy`, [dataset.js:105-118](../../public/scripts/dataset.js#L105-L118)), NumPy format version 1.0:

| Bytes | Content |
|---|---|
| 0-5 | magic string `\x93NUMPY` ([dataset.js:112](../../public/scripts/dataset.js#L112)) |
| 6-7 | version 1, 0 |
| 8-9 | header length $h$, unsigned 16-bit little-endian ([dataset.js:113-114](../../public/scripts/dataset.js#L113-L114)) |
| 10 … 9 + h | an ASCII Python dictionary, for example `{'descr': '<f8', 'fortran_order': False, 'shape': (4,), }`, padded with spaces and ended by `\n` ([dataset.js:107-110](../../public/scripts/dataset.js#L107-L110)) |
| 10 + h … | the array's raw bytes, copied from memory ([dataset.js:116](../../public/scripts/dataset.js#L116)) |

- `descr` is the type from the `DTYPES` table, for example `<f8` for `Float64Array` ([dataset.md](dataset.md#types)).
- `fortran_order: False` says the bytes are in C (row-major) order, which is how the store keeps 2-D arrays: the last index
  runs fastest.
- `shape` comes from the variable's dimensions; a 1-D shape gets the trailing comma Python needs for a one-element tuple
  ([dataset.js:107](../../public/scripts/dataset.js#L107)).
- The padding makes the data start on a multiple of 64 bytes: the number of spaces is
  $(64 - (10 + \ell + 1) \bmod 64) \bmod 64$, where $\ell$ is the dictionary's length and the $+1$ is the final newline
  ([dataset.js:108](../../public/scripts/dataset.js#L108)).

**The zip** (`zip`, [dataset.js:134-151](../../public/scripts/dataset.js#L134-L151)). For each member, in order: a 30-byte local
header, the UTF-8 name, the data. Then a 46-byte central-directory record plus name per member, then a 22-byte end record. All
integers are little-endian ([dataset.js:136-137](../../public/scripts/dataset.js#L136-L137)).

| Record | Fields as written |
|---|---|
| Local header ([L142](../../public/scripts/dataset.js#L142)) | signature `50 4B 03 04`; version needed 20 (zip 2.0); flags `0x0800` (bit 11: the name is UTF-8); method 0 (stored, no compression); DOS time; DOS date; CRC-32; compressed size = uncompressed size = data length; name length; extra length 0 |
| Central record ([L144](../../public/scripts/dataset.js#L144)) | signature `50 4B 01 02`; version made by 20; version needed 20; flags `0x0800`; method 0; time; date; CRC-32; both sizes; name length; extra, comment, disk number, internal and external attributes all 0; offset of the local header |
| End record ([L149](../../public/scripts/dataset.js#L149)) | signature `50 4B 05 06`; disk numbers 0; number of entries (twice); size of the central directory; its offset; comment length 0 |

- The CRC-32 uses the reflected polynomial `0xEDB88320` with a 256-entry table built once; the register starts at
  `0xFFFFFFFF` and is inverted at the end ([dataset.js:119-132](../../public/scripts/dataset.js#L119-L132)).
- The DOS time is $2048\,h + 32\,m + \lfloor s/2 \rfloor$ and the DOS date $512\,(y - 1980) + 32\,M + d$, from the browser's
  local clock, the same for all members ([dataset.js:138-139](../../public/scripts/dataset.js#L138-L139)).
- Member order: the arrays in declaration order, `dataset.json`, then the extra files ([dataset.js:154-170](../../public/scripts/dataset.js#L154-L170)).

**`dataset.json`** ([dataset.js:153-169](../../public/scripts/dataset.js#L153-L169)) holds `title`, `attrs`, `dims`, `coords`
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
| `kicker` | text above the title (default: the dataset title) | [137](../../public/scripts/datalog.js#L137) | all |
| `file` | base name of saved files | [968](../../public/scripts/datalog.js#L968), [977](../../public/scripts/datalog.js#L977), [1005](../../public/scripts/datalog.js#L1005) | all |
| `playing` | `() → bool` | [762](../../public/scripts/datalog.js#L762), [784](../../public/scripts/datalog.js#L784) | all |
| `play` | `() → void` | [762](../../public/scripts/datalog.js#L762) | all except Fig. 3 |
| `groups` | `[{ title, note, vars }]` | [98](../../public/scripts/datalog.js#L98), [189](../../public/scripts/datalog.js#L189), [769](../../public/scripts/datalog.js#L769) | all |
| `colour` | `{ name: (value, j, i) → [r, g, b] \| null }`, presentation only | [95](../../public/scripts/datalog.js#L95) | all except Figs. 2 and 10 |
| `rowLabel` | `{ dim: (j) → text }` | [400](../../public/scripts/datalog.js#L400), [414](../../public/scripts/datalog.js#L414) | Figs. 2, 3, 5, 6, 7, 8 |
| `colLabel` | `{ name: (i) → html }` | [413](../../public/scripts/datalog.js#L413) | Figs. 1, 2 |
| `at` | `{ name: (j[, i]) → html }`, a note after a table cell's value | [403](../../public/scripts/datalog.js#L403), [417](../../public/scripts/datalog.js#L417) | Figs. 1, 2 |
| `probe` | `(x, y) → ref \| null`, CSS px in `#stage` | [551](../../public/scripts/datalog.js#L551) | all |
| `inspect` | `(ref) → { title, at: {x, y}, rows: [[symbol, value, units, varName, index]] }` | [669](../../public/scripts/datalog.js#L669), [692](../../public/scripts/datalog.js#L692), [807](../../public/scripts/datalog.js#L807) | all |
| `locate` | `(varName, index) → {x, y} \| null` | [677](../../public/scripts/datalog.js#L677) | all |
| `check` | `{ name: (index) → { formula, inputs: [[symbol, value, units, digits]], value } }` | [510](../../public/scripts/datalog.js#L510) | all |
| `drawn` | `{ name: (index) → { what, drawn, expected, ok, note } }`; `ok` is `true`, `false` or `null` (nothing drawn to read back now) | [524](../../public/scripts/datalog.js#L524), [529](../../public/scripts/datalog.js#L529) | all |
| `round` | `{ label, time, length, columns, point, mode?, blocked? }` | [101](../../public/scripts/datalog.js#L101) | all (table above) |
| `about` | HTML paragraph: what still differs between store and picture | [165](../../public/scripts/datalog.js#L165) | all |

The ten blocks: [Fig. 1 L798](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L798),
[Fig. 2 L768](../../public/simulations/Double%20Pendulum.html#L768),
[Fig. 3 L849](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L849),
[Fig. 4 L996](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L996),
[Fig. 5 L810](../../public/simulations/water-wave.html#L810),
[Fig. 6 L868](../../public/simulations/wave-interference.html#L868),
[Fig. 7 L1370](../../public/simulations/phasor-sums.html#L1370),
[Fig. 8 L1301](../../public/simulations/draw-decompose.html#L1301),
[Fig. 9 L1686](../../public/simulations/driven-oscillator.html#L1686),
[Fig. 10 L1054](../../public/simulations/wind-turbine.html#L1054).

## Public interface

| Name | Lines | Arguments | What it does / returns |
|---|---|---|---|
| `Sim.colourMap` | [70-77](../../public/scripts/datalog.js#L70-L77) | `v, lim` | `[r, g, b]` on a diverging scale: $a = v/\text{lim}$ clipped to $[-1, 1]$, $s = |a|^{0.8}$, mixed from the paper colour (255, 250, 243) towards dark (58, 50, 46) for negative or burgundy (122, 31, 43) for positive values. Pages use it in their `colour` functions. |
| `window.__dataPanel` | [1089](../../public/scripts/datalog.js#L1089) | | `{ running(), rounds(), recording() }`: hooks for tests. |
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
| `R` | [101-101](../../public/scripts/datalog.js#L101-L101) | The page’s required `spec.round`. |
| `timeNow`, `timeSym`, `timeUnit`, `timeText`, `timeHTML` | [103-108](../../public/scripts/datalog.js#L103-L108) | The round's time variable and its display. |
| `palette`, `tok` | [179-185](../../public/scripts/datalog.js#L179-L185) | Colours from the panel's CSS tokens, cached. |
| `stats` | [213-220](../../public/scripts/datalog.js#L213-L220) | Min, max, mean of an array, cached by version. |
| `describe` | [221-233](../../public/scripts/datalog.js#L221-L233) | Value cell and shape of one ledger row. |
| `drawThumb` | [235-279](../../public/scripts/datalog.js#L235-L279) | 128 × 34 px line or heat map. |
| `paintVars` | [280-292](../../public/scripts/datalog.js#L280-L292) | Repaints ledger rows that changed. |
| `paintInstant` | [294-299](../../public/scripts/datalog.js#L294-L299) | The "Values at …" line. |
| `catchNow` | [300-305](../../public/scripts/datalog.js#L300-L305) | Catches a new instant. |
| `makeGrid` | [308-372](../../public/scripts/datalog.js#L308-L372) | Virtual table; inner `sizeTo`, `layout`, `fill`, `paintGrid`, `mark`, `onPoint` ([314-363](../../public/scripts/datalog.js#L314-L363)). |
| `takeSnap`, `snapStats` | [375-385](../../public/scripts/datalog.js#L375-L385) | Copy of the arrays at one instant, and its statistics. |
| `checkButton` | [386-388](../../public/scripts/datalog.js#L386-L388) | A "Check" button for one element. |
| `gridSource` | [389-421](../../public/scripts/datalog.js#L389-L421) | Adapts a 1-D group or a 2-D array to the table. |
| `paintArray`, `openArray` | [422-461](../../public/scripts/datalog.js#L422-L461) | Array view header and table. |
| `openCheck`, `agreement`, `runCheck` | [480-536](../../public/scripts/datalog.js#L480-L536) | Check view. |
| `stageXY`, `refAt`, `setRead` | [548-566](../../public/scripts/datalog.js#L548-L566) | Pointer position in the figure; probe with rings; Read on/off. |
| `fitOverlay`, `pinAt`, `own`, `up` | [596-636](../../public/scripts/datalog.js#L596-L636) | Overlay sizing; pinning; capturing the gesture; end of drag. |
| `touched`, `wipe`, `drawRing`, `drawPin`, `clearOverlay` | [642-662](../../public/scripts/datalog.js#L642-L662) | Overlay drawing with dirty rectangles. |
| `paintProbe` | [664-688](../../public/scripts/datalog.js#L664-L688) | Marker every frame; words at most every 250 ms. |
| `rowsKey`, `paintStrip` | [689-737](../../public/scripts/datalog.js#L689-L737) | The strip and the "Pinned point" table. |
| `roundLength`, `describeRound`, `scalarNames` | [748-757](../../public/scripts/datalog.js#L748-L757) | Round length (default 10), the Record box text, numeric scalars. |
| `startRound`, `progress`, `recordFrame`, `finishRound` | [758-847](../../public/scripts/datalog.js#L758-L847) | Recording. |
| `seriesRange`, `drawChart` | [850-885](../../public/scripts/datalog.js#L850-L885) | Range without NaN; one chart with optional cursor. |
| `renderRounds` | [886-945](../../public/scripts/datalog.js#L886-L945) | Rounds view; inner `readout`, `drawAll`, `pick`. |
| `roundCsv`, `download`, `stamp`, `readme(what, filename)` | [946-1003](../../public/scripts/datalog.js#L946-L1003) | Files. |
| `show`, `setOpen` | [1013-1033](../../public/scripts/datalog.js#L1013-L1033) | Switch view; open or close the panel. |
| `paintState`, `paint` | [1052-1061](../../public/scripts/datalog.js#L1052-L1061) | The "one instant / live / recording" label; repaint of the open view. |
| `wanted`, `kick`, `frame` | [1065-1073](../../public/scripts/datalog.js#L1065-L1073) | The on-demand loop. |
| `soon` | [1086](../../public/scripts/datalog.js#L1086) | Refreshes the round description once per frame after any input or click. |

## State it keeps

- `localStorage`: `datapanel.open` (`'1'`/`'0'`), `datapanel.live` (`'1'`/`'0'`), `datapanel.tab` (`'vars'`/`'rounds'`)
  ([datalog.js:47](../../public/scripts/datalog.js#L47), [1020](../../public/scripts/datalog.js#L1020),
  [1030](../../public/scripts/datalog.js#L1030), [1046](../../public/scripts/datalog.js#L1046)). The keys are the same for every
  page, so the choice carries from one figure to the next.
- In memory: `isOpen`, `view`, `liveOn` ([1012](../../public/scripts/datalog.js#L1012)); `caught` (time and reason of the
  instant, [293](../../public/scripts/datalog.js#L293)); `current`, `snap`, `grid` (open table, [374](../../public/scripts/datalog.js#L374));
  `checking` ([479](../../public/scripts/datalog.js#L479)); `held = { ref, cell }` and `probe` (Read values state,
  [542-543](../../public/scripts/datalog.js#L542-L543)); `rounds` (at most 5), `roundNo`, `rec` (the recording),
  `sel` ([744](../../public/scripts/datalog.js#L744)); `running` ([1064](../../public/scripts/datalog.js#L1064)); `statCache`.
  Rounds are lost on reload.
- DOM attributes and classes written: `lang="en"` and `dir="ltr"` on the tab, the panel and the strip, `lang="en"` on the Read
  values switch ([datalog.js:120](../../public/scripts/datalog.js#L120), [134](../../public/scripts/datalog.js#L134),
  [575](../../public/scripts/datalog.js#L575), [585](../../public/scripts/datalog.js#L585)): the panel's words are English, so on a page in another
  language (the Arabic page of Iron, Cotton and the Head) they keep their language and read left to right; `body.dp-open`; `aria-expanded` on the tab; `aria-hidden` and `inert` on the closed panel
  ([1024-1033](../../public/scripts/datalog.js#L1024-L1033)); `#stage.dp-reading` while reading
  ([562](../../public/scripts/datalog.js#L562)); `aria-pressed` on the Read button; `.dp-tab--away` while scrolling down on a
  phone ([123-130](../../public/scripts/datalog.js#L123-L130)); `.dp-rec.is-rec` while recording.
- DOM read: `#stage`, the `.stage__cap` inside `#stage`'s parent ([589](../../public/scripts/datalog.js#L589)), CSS tokens `--accent`,
  `--ink`, `--ink-3`, `--rule`, `--muted`, `--card-soft` ([183](../../public/scripts/datalog.js#L183)).

## Timing and events

| What | Rate | Where |
|---|---|---|
| Panel loop | one animation frame while `wanted()`; none otherwise | [1065-1073](../../public/scripts/datalog.js#L1065-L1073) |
| Live: ledger values | every frame | [1059](../../public/scripts/datalog.js#L1059) |
| Live: thumbnails | at most every 250 ms, only after a version change | [286](../../public/scripts/datalog.js#L286) |
| Read values: marker | every frame | [672-675](../../public/scripts/datalog.js#L672-L675) |
| Read values: words | at most every 250 ms (4 per second; measured 3.7) | [687](../../public/scripts/datalog.js#L687) |
| Outline before a click | after 300 ms of rest | [632](../../public/scripts/datalog.js#L632) |
| Table cell shown in the figure | 600 ms after a hover, 3000 ms after a click | [457](../../public/scripts/datalog.js#L457) |
| Recording: samples | every frame or every $L/600$, at most 600 | [801-802](../../public/scripts/datalog.js#L801-L802) |
| Recording: progress bar | every 125 ms (8 per second) | [818](../../public/scripts/datalog.js#L818) |
| First instant | two animation frames after load | [1083](../../public/scripts/datalog.js#L1083) |
| Round description | at most once per frame, after an `input` or `click` anywhere | [1085-1088](../../public/scripts/datalog.js#L1085-L1088) |
| Object URL of a download | revoked after 4 s | [960](../../public/scripts/datalog.js#L960) |

Listeners: `window` `scroll` (passive) for the phone pill; `pointerdown`, `pointermove`, `pointerup`, `pointercancel` and
`click`, `mousedown`, `mouseup`, `dblclick`, `contextmenu` on `#stage` in the capture phase, all inactive unless Read values is
on; `pointerleave` on `#stage`; `keydown` on `document` (Esc stops reading) and on the panel (Esc closes it); clicks on the
tab, close button, tabs, Catch now, Live, Record, Save and inside the panes; `pointermove`/`pointerdown`/`pointerleave` on the
round charts; `visibilitychange` (restarts the loop when the page shows again); `input` and `click` on `document` in the
capture phase for `soon()`; `ResizeObserver` on `#stage` and on the table.

## Contracts with other files

- **`dataset.js`**: the store and its fields `title`, `dims`, `vars`, `order`, methods `get`, `dtype`, `along`, `npz`; for a
  round archive, `Sim.dataset` and the new store's `dim`, `coord`, `var`, `set`, `has` and `npz`
  ([datalog.js:970-978](../../public/scripts/datalog.js#L970-L978); [dataset.md](dataset.md)).
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
- Text that changes while a figure runs: at most 4 rewrites per second (the 250 ms at [line 687](../../public/scripts/datalog.js#L687)). Measure after a change: what
  shows during a pointer sweep, how much of the figure the marker covers, how often the strip text changes.
- If you add a key to `Sim.data`, add it to the contract comment at the top of the file, which pages and maintainers read first.
- After changing the archive, re-run the Python check: `zipfile.ZipFile(f).testzip()` returns `None`, `numpy.load(f)` lists the
  arrays, `dataset.json` loads.

## Notes for maintainers

1. Fixed on 2026-10-15: the contract documents kicker, rowLabel, colLabel and at (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
2. Fixed on 2026-10-15: the unused touchProbe hook was removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
3. Fixed on 2026-10-15: every page supplies round; the unused log fallback was removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
4. Fixed on 2026-10-15: store and round READMEs open the exact timestamped download filename; CRC and NumPy array shapes validate (commit [9d3175f](https://github.com/Numa1997/SiteTest/commit/9d3175f2cf50d0ad3f8792f1ee173e8ce56bab53)).
5. Fixed on 2026-10-15: paintStrip no longer takes an unused argument (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
6. Fixed on 2026-10-15: sampled rounds reserve the final slot; the 600-sample, 10 s test retains its ending frame instead of stopping at 9.983 s (commit [9d3175f](https://github.com/Numa1997/SiteTest/commit/9d3175f2cf50d0ad3f8792f1ee173e8ce56bab53)).
7. Hovering a cell of an array table, without a click, draws a ring on the running figure for 0.6 s
   ([datalog.js:364](../../public/scripts/datalog.js#L364), [457](../../public/scripts/datalog.js#L457)). The pointer crosses the
   table, not the figure, but the figure changes. CLAUDE.md asks that nothing on a running figure react to the pointer merely
   crossing; whether this case is meant to be covered is not determined from the code.
8. Pressing Esc while focus is inside the panel and Read values is on does two things at once: it closes the panel
   ([datalog.js:1036](../../public/scripts/datalog.js#L1036)) and stops reading ([datalog.js:639](../../public/scripts/datalog.js#L639)).
9. AGENTS.md said the load order holds for "all eight figures"; it holds for all ten pages (load-order table in
   [sim.md](sim.md#load-order-on-the-pages)). Corrected to "all ten figures" on 14 October 2026.
10. Fixed on 2026-10-15: a read-back that returns `ok: null` gets a neutral verdict, "Not in the picture at the moment, so
    there is nothing to read back." (class `is-na`), instead of a burgundy ✕ ([datalog.js:529](../../public/scripts/datalog.js#L529)).
    Figs. 3, 6 and 10 return `null` when the value has nothing drawn (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
11. Fixed on 2026-10-15: the reason a round cannot start (`Sim.data.round.blocked`) sits in `span.dp-rec__why`, after a space,
    and shows on phones too; it used to sit inside `.dp-more-txt`, which is hidden at 640 px and below
    ([datalog.js:754](../../public/scripts/datalog.js#L754)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
