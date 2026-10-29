# public/scripts/datalog.js

| | |
|---|---|
| File | [public/scripts/datalog.js](../../public/scripts/datalog.js), 1422 lines, 104.5 kB (104 474 bytes) |
| Loaded by | the eleven simulation pages, the two pages of Iron, Cotton and the Head (`portfolios/impact/index.html`, `ar.html`), the ideal and servo presses of the Hydraulic Press Study and Droplet Collection (`portfolios/droplet-collection/index.html`, for panels 4 and 3), last, after the page's own script (line numbers in the load-order table of [sim.md](sim.md#load-order-on-the-pages)); Figs. 9, 10 and 11 load their ledger, [scripts/ledger/](../../public/scripts/ledger/), just before it, on the same line ([driven-oscillator.html:1930](../../public/simulations/driven-oscillator.html#L1930), [wind-turbine.html:1168](../../public/simulations/wind-turbine.html#L1168), [pendulum-control.html:1347](../../public/simulations/pendulum-control.html#L1347)); styles in [styles/data.css](../../public/styles/data.css), linked in each page's head (for example [Double Pendulum.html:12](../../public/simulations/Double%20Pendulum.html#L12)) |
| Reads | `Sim.data` (the page's contract, below) and through it the page's dataset ([datalog.js:66-67](../../public/scripts/datalog.js#L66-L67)) |
| Defines | `Sim.colourMap` ([datalog.js:103](../../public/scripts/datalog.js#L103)), `window.__dataPanel` ([datalog.js:1421](../../public/scripts/datalog.js#L1421)) |
| Adds to the page | `button.dp-tab` and `aside#data-panel.dp` at the end of `<body>` ([datalog.js:232-233](../../public/scripts/datalog.js#L232-L233)); `canvas.dp-overlay` inside `#stage`, `div.dp-read` right after `#stage`, `button.dp-readbtn` in the figure caption ([datalog.js:874-897](../../public/scripts/datalog.js#L874-L897)) |

`datalog.js` is the data panel, designed as a bookkeeper beside a running machine (skill `phyein-usul-bookkeeper`; redesign
of 24 October 2026). On top, the few numbers the animation is about, live, each with a sparkline. Below them, every other
number of the page's one store ([dataset.md](dataset.md)) in a table, in the order of cause: what the reader sets, what follows
from it, the state now, the stored run, the solver, the drawing. Last, the books: the quantities that must balance, added up
with their signs, with the residual stored by the page and added again by the panel. An array is one row with a sparkline that
opens in place into its own table. The tools sit in one toolbar under the headline: Record one round, Read values (pin a
point of the figure), Live (on by default; off holds one instant, and Catch now catches another) and Save (a NumPy archive with
CSV and a README). Check, beside every scalar, shows three answers from one frame: stored, recomputed from the stored inputs,
read back from the picture. The panel never computes physics and never writes to the store. When it is closed it does no work
at all ([datalog.js:1-63](../../public/scripts/datalog.js#L1-L63)).

## How it works

### The picture

Think of a bookkeeper who sits beside the experiment with a ledger. The first lines of the ledger, in large figures, are the
dials the experiment is about, and beside each a short strip of chart paper that keeps scrolling. Below, every other dial is
entered in columns, in the order in which one causes the next: the knobs you set, the constants worked out from them, the
state now, the full record of the run, the solver's notes, the draughtsman's scales. Every quarter of a second the
bookkeeper rewrites the figures that moved, writes beside each by how much it moved, and taps once on a line that has just
started to move; a line that did not move is left alone, so the eye finds the movement. When you turn a knob, the bookkeeper
underlines it and every line that depends on it. At the foot of the page are the books: energy in, minus energy lost, must
equal the energy stored, and the bookkeeper writes down by how much they miss. Close the ledger, and the bookkeeper stops.

### Start-up, in source order

1. If the page did not define `Sim.data` with a `ds`, the file returns and the page has no panel
   ([datalog.js:66-67](../../public/scripts/datalog.js#L66-L67)).
2. It defines its helpers (among them `sciHTML`, a small number as 2.1×10⁻⁹) and `Sim.colourMap`
   ([datalog.js:70-110](../../public/scripts/datalog.js#L70-L110)), takes the page's language and direction from `<html>`
   ([datalog.js:111](../../public/scripts/datalog.js#L111)), then reads the store through short accessors `V`, `A`, `sym`,
   `digitsOf`, `unitOf` ([datalog.js:114-129](../../public/scripts/datalog.js#L114-L129)).
3. It reads the ledger, `Sim.data.ledger`, if the page declares one, and merges its `check` entries into `Sim.data.check`
   where the page has none ([datalog.js:132-133](../../public/scripts/datalog.js#L132-L133)). The sections are the ledger's
   `sections`, or else the page's `groups`, each with only the names that exist in the store; with a ledger, every stored variable
   that no section names is put in a last, folded section "Everything else", so nothing is hidden
   ([datalog.js:135-143](../../public/scripts/datalog.js#L135-L143)). It takes the headline (at most 7 scalars) and the books whose
   rows all exist ([datalog.js:144-145](../../public/scripts/datalog.js#L144-L145)), and turns `deps` into the dependents of each
   input, following inputs of inputs ([datalog.js:148-156](../../public/scripts/datalog.js#L148-L156)).
4. It reads what one round is, `R` ([datalog.js:158](../../public/scripts/datalog.js#L158)), the time variable `TV`
   ([datalog.js:159](../../public/scripts/datalog.js#L159)) and the round's chart columns, the numeric scalars of
   `round.columns` other than time ([datalog.js:166](../../public/scripts/datalog.js#L166)).
5. It builds the tab button and the panel: header (kicker, state, Close, title), the headline with the books' summary, the
   toolbar with the round's description and progress, two tabs (Ledger, Rounds), three panes (`vars`, `check`, `rounds`) and
   an explanation "How the numbers and the picture are tied" that ends with the page's own `about` paragraph
   ([datalog.js:176-230](../../public/scripts/datalog.js#L176-L230)). The tab, the panel and the Read values strip take the
   page's `lang` and `dir`, so on an Arabic page the panel runs right to left.
6. It writes the ledger table and the books once ([datalog.js:253-303](../../public/scripts/datalog.js#L253-L303)).
7. If the page has `#stage` and `Sim.data` has `probe` and `inspect`, it adds the Read values button, the overlay canvas and
   the strip, with their pointer listeners, and shows Read values in the toolbar
   ([datalog.js:874-949](../../public/scripts/datalog.js#L874-L949)).
8. It restores the reader's choices from `localStorage` and opens the panel if it was open last time, or, the first time, if
   the window is at least 1500 px wide ([datalog.js:1409-1413](../../public/scripts/datalog.js#L1409-L1413)).
9. Two animation frames later, after the simulation has drawn twice, it catches the first instant and starts the loop
   ([datalog.js:1415](../../public/scripts/datalog.js#L1415)).

### The loop that runs only when needed

The panel has one `requestAnimationFrame` loop, and it runs only while `wanted()` is true: a round is recording, Read values
is on with a pin or an outline showing, a table cell's position is being shown in the figure, a marker still has to be wiped,
or the panel is open with Live on and the simulation is playing, a pointer is held down, or a reader's action happened less
than 1.5 s ago ([datalog.js:1389-1392](../../public/scripts/datalog.js#L1389-L1392)). The last case lets the ledger follow a
slider, a Solve or a drag while the clock stands still: `input`, `change`, `click`, `keydown` and `pointerdown` anywhere call
`poke()` ([datalog.js:1404-1408](../../public/scripts/datalog.js#L1404-L1408)). Any action that may need the loop calls `kick()`
([datalog.js:1393](../../public/scripts/datalog.js#L1393)). Each frame does, in order: record one sample, draw the probe overlay,
and, if the panel is open and live, feed and draw the headline's sparklines and the dots on the arrays on screen, and rewrite
the words if 250 ms have passed since the last rewrite; then it requests the next frame, or stops, wipes the overlay and paints
once more so the ledger shows the last state ([datalog.js:1394-1401](../../public/scripts/datalog.js#L1394-L1401)). Closing the
panel also cancels a table cell's marker in the figure ([datalog.js:1340](../../public/scripts/datalog.js#L1340)).

Animation-frame callbacks run in the order they were requested. The page's clock requests its next frame inside its own
callback ([sim.js:184](../../public/scripts/sim.js#L184)), before any later `kick()` can, so in every frame the panel reads
the store after the simulation has written it.

Measured in headless Chromium (Chromium of Playwright 1.56, `chromium_headless_shell-1243`) on 24 October 2026, on Figs. 2, 6,
9 and 10 in English, German and Arabic at 1440, 1100 and 390 px: with the panel closed `__dataPanel.running()` is `false`;
with it open and the simulation playing, the panel's words changed in 11 or 12 batches in 3 s, at most 4 in any one second.

### The headline

The page's `ledger.headline` names 3 to 7 scalars; each becomes a card with its symbol, a short word, the value in IBM Plex
Mono, its unit and a sparkline ([datalog.js:191-196](../../public/scripts/datalog.js#L191-L196)). Every frame `feedHeads()` appends
the value if it or the time changed, keeping the last 360 frames (`ledger.window`), and `drawHeads()` draws the line, a zero
line if the range crosses zero, and a dot on the newest value, redrawing a card only when its data or width changed
([datalog.js:426-462](../../public/scripts/datalog.js#L426-L462)). The numbers themselves are rewritten with the rest of the words,
at most four times a second ([datalog.js:463-469](../../public/scripts/datalog.js#L463-L469)). The sparkline's horizontal axis
is frames, not time, so a drag with the clock stopped still shows. Under the cards, one button sums up the books, for example
"Books ✓ energy balances to 2.7×10⁻¹³ ✓ Newton balances to 7.1×10⁻⁵ of the flows"; it scrolls to them
([datalog.js:486-510](../../public/scripts/datalog.js#L486-L510)).

### The ledger table

One `<table>` with header cells: Symbol, Meaning, Value now, Unit, Δ, Obtained, Check ([datalog.js:259-264](../../public/scripts/datalog.js#L259-L264)).
Each section is a `<tbody>` whose first row is its numbered title, a count of rows and its note; a click folds or opens it, and
the choice is kept per page in `localStorage` ([datalog.js:265-284](../../public/scripts/datalog.js#L265-L284),
[datalog.js:770-775](../../public/scripts/datalog.js#L770-L775)). In a row:

- **Meaning**: the variable's `long_name`, and its `formula` under it in the lecture-note font ([datalog.js:255-258](../../public/scripts/datalog.js#L255-L258)).
- **Value now**, aligned on the decimal point: the value is split into the part before the point and the part from it, and the
  second part sits in a box of fixed width per section, as wide as the most decimals in that section
  ([datalog.js:253](../../public/scripts/datalog.js#L253), [datalog.js:325-337](../../public/scripts/datalog.js#L325-L337)). Words
  (`True`, `stable focus`) and values in scientific notation (attribute `sci`) skip that box.
- **Δ**: when the text of a value changed since the last rewrite, the signed difference, burgundy when it grew and brown when it
  fell; it fades after 1.5 s without change. A row that starts to move after standing still blinks once (a background flash of
  0.9 s, by alternating two animation classes so no layout is forced); a row that keeps moving only updates its Δ
  ([datalog.js:522-552](../../public/scripts/datalog.js#L522-L552)).
- **Obtained**: set by you, constant, formula, stored run, solver or drawing; the section's `how`, or `ledger.how[name]`, or
  "formula" when the variable has one ([datalog.js:134](../../public/scripts/datalog.js#L134), [datalog.js:146](../../public/scripts/datalog.js#L146)).
- **Check**: the button that opens Check. Once a second the panel compares each scalar's stored value with its `check` formula
  at index 0 and marks the button: tan with a tick when they agree, burgundy when they differ, dashed when the value is an
  input with nothing to recompute or is not defined now ([datalog.js:511-520](../../public/scripts/datalog.js#L511-L520),
  [datalog.js:549](../../public/scripts/datalog.js#L549)). The read-back from the picture runs only when Check is opened.

Rows in folded sections are not painted at all. The instant line above the table says "Live · t = 3.13 s · numbers rewritten
four times a second", or "Held at t = …" with the reason when Live is off ([datalog.js:553-559](../../public/scripts/datalog.js#L553-L559)).
`catchNow(why)` records the time and the reason, re-copies an open array, re-runs an open Check and repaints; it is called when
the panel opens, on Catch now, when Live is switched off, and at the end of a round
([datalog.js:560-566](../../public/scripts/datalog.js#L560-L566)).

**Cause and effect.** When a control with an `id` moves and the panel is open, `markFrom` marks the input's row (a burgundy bar
and tint) and every row whose inputs, followed back through `ledger.deps`, reach it (tan), for 2 s; a folded section with a
marked row has its title marked ([datalog.js:569-583](../../public/scripts/datalog.js#L569-L583)). The control is found by
`ledger.controls[id]`, or by a variable of the same name as its `id`. Measured on Fig. 9: moving ζ marks its own row and 27
rows; moving k marks 32; on Fig. 10 moving v₀ marks 4.

**Narrow panels.** When the panel is narrower than 540 px (a container query on `.dp`, so it holds on a phone and in a narrow
window alike), the table keeps Symbol, Value now, Unit and Δ; a tap on a row opens a detail row with the meaning, the formula,
how it is obtained, the variable's name and a Check button ([datalog.js:749-761](../../public/scripts/datalog.js#L749-L761)).

**Right to left.** The panel takes `dir="rtl"` on an Arabic page, so the columns run from the right; the value, unit and Δ
cells, the headline's numbers and every time stamp are `dir="ltr"`, and the alignment of numbers is kept out of the mirrored
stylesheet (`/*rtl:ignore*/` in `data.css`), so the decimal points still line up.

### The books

Each entry of `ledger.books` is a small account: its rows with their signs, a closing line (`total`), and under them three
figures: the residual added by this panel, $r = \sum_k s_k x_k - x_\text{total}$ with $s_k = \pm 1$; the residual the page
stored where it computes it (`residual`); and the relative residual $|r| / (\sum_k |x_k| + |x_\text{total}|)$, measured against
the flows through the account ([datalog.js:477-484](../../public/scripts/datalog.js#L477-L484)). The verdict says "Balanced"
when the relative residual is within `tol`, and whether the page's residual and the panel's sum agree, to $10^{-12}$ of the
flows. While the page's `paused()` gives a reason (Fig. 9: a hand holds the block, or the run blew up), the account says so
instead of a verdict ([datalog.js:486-507](../../public/scripts/datalog.js#L486-L507)).

The two sums are the fourth proof of the pipeline (Numa's choice of 24 October 2026, option 3 of the design): the page's
residual shows what the simulation stored; the panel's sum shows that the rows on screen add up to it.

| Fig. | Book | Rows | Closing line | Tolerance | Measured (relative) |
|---|---|---|---|---|---|
| 9 | Energy | E(0) + W<sub>in</sub> − W<sub>loss</sub> | E | 10⁻⁶ | 1.5 to 3.8 × 10⁻¹³ |
| 9 | Newton’s second law | F + F<sub>c</sub> + F<sub>k</sub> | m a, a from the stored velocities by a central difference | 10⁻² | 2.9 to 8.0 × 10⁻⁵ |
| 10 | Energy | K(0) + E<sub>aero</sub> − E<sub>gen</sub> | K = ½ J ω² | 10⁻⁶ | 1.2 to 1.5 × 10⁻¹³ |

The energy books balance to rounding because the pages integrate the work and the heat in the same RK4 step as the motion. The
Newton book misses by the error of the central difference, of order $(\Omega\,\Delta t)^2 / 6$ with $\Delta t = 10$ ms. Fig. 10
has no force book: the step and gust winds make the rotor's acceleration jump, and a difference across a jump misses by half
the jump.

### Arrays

An array is one row: its meaning and shape, a 72 × 22 px sparkline (a line for 1-D, a heat map for 2-D, from the page's
`colour` function or `Sim.colourMap`), and, where `ledger.current` names the index shown now, a dot on that element and its
value ([datalog.js:338-413](../../public/scripts/datalog.js#L338-L413)). The picture is cached and redrawn at most every 250 ms,
and only when the array's version moved; the dot is drawn every frame, only for rows on screen (an `IntersectionObserver`,
[datalog.js:415-420](../../public/scripts/datalog.js#L415-L420)). Min, max and mean skip NaN and infinite values and are cached
by version ([datalog.js:316-323](../../public/scripts/datalog.js#L316-L323)).

A click (or Enter) opens the row in place into its own table, one at a time ([datalog.js:715-746](../../public/scripts/datalog.js#L715-L746)).
Opening copies the array (`slice()`) at one instant, so every cell shows the same frame; a 2-D variable is shown as rows ×
columns, a 1-D variable together with every other 1-D variable over the same dimension, coordinates first
([datalog.js:652-657](../../public/scripts/datalog.js#L652-L657), [dataset.js:93](../../public/scripts/dataset.js#L93)). Above
the table: shape, min, max and mean, or the list of variables along the dimension, "Copied at t = …" and Copy again
([datalog.js:699-714](../../public/scripts/datalog.js#L699-L714)); while Live is on, a new solve (a new version) copies again.

The table is virtual: only the cells inside the scrolled window exist in the DOM. Cells are 74 × 28 px (108 px wide for 1-D),
the row header 56 px (64 px for 1-D), the column header 32 px ([datalog.js:586](../../public/scripts/datalog.js#L586),
[datalog.js:671](../../public/scripts/datalog.js#L671)). On every scroll or resize `layout()` works out the first and last
visible row and column, rebuilds only if that window changed, and `fill()` writes a cell's text and background only when
they changed ([datalog.js:596-623](../../public/scripts/datalog.js#L596-L623)). Measured on Fig. 1 before the redesign (window
1600 × 1000): the 162 × 360 array `C`, 58 320 numbers, was shown with 80 cell elements and 18 header elements.

Pointing at a cell (mouse over or click) shows its index and value with a Check button under the table and, if the page has
`locate`, marks where that element is drawn in the figure with a ring: for 0.6 s after a hover, 3 s after a click or tap
([datalog.js:633-640](../../public/scripts/datalog.js#L633-L640), [datalog.js:739-744](../../public/scripts/datalog.js#L739-L744),
[datalog.js:985-995](../../public/scripts/datalog.js#L985-L995)).

### Read values

Off, the figure behaves as if this file were absent. On, the gesture belongs to the reading: the panel's listeners run in the
capture phase and stop the event before the page's own handlers see it, so a click does not add a source or start a drawing
([datalog.js:924-947](../../public/scripts/datalog.js#L924-L947)).

- **Pin.** A press asks the page's `probe(x, y)` what lies under the pointer. If nothing does, it tries 8 points on a ring
  12 px out, then 8 on a ring 22 px out, so a finger finds a small moving object ([datalog.js:856-862](../../public/scripts/datalog.js#L856-L862)).
  A drag keeps re-pinning ([datalog.js:935](../../public/scripts/datalog.js#L935)). A press on empty space says "Nothing to pin
  there" ([datalog.js:1006](../../public/scripts/datalog.js#L1006)).
- **Marker.** Every frame the overlay is wiped and the pin is drawn at `inspect(ref).at`, so it rides on the moving object: a
  ring of radius 11 px with a light halo and four ticks out to 18 px ([datalog.js:958-966](../../public/scripts/datalog.js#L958-L966),
  [datalog.js:981-984](../../public/scripts/datalog.js#L981-L984)). Only the rectangles drawn last frame are cleared, unless
  there are more than six ([datalog.js:950-956](../../public/scripts/datalog.js#L950-L956)).
- **Words.** The title and values go into a strip under the figure, between the figure and its caption, so they never cover
  it ([datalog.js:880-887](../../public/scripts/datalog.js#L880-L887)). They are rewritten at most every 250 ms
  ([datalog.js:996](../../public/scripts/datalog.js#L996)); the row structure is rebuilt only when the list of rows changes,
  otherwise only changed numbers are written ([datalog.js:1011-1023](../../public/scripts/datalog.js#L1011-L1023)). Each value that
  names a dataset variable is a button that opens Check. The same values appear in the panel, in a "Pinned point" box above the ledger that shows only while a point is pinned
  ([datalog.js:1027-1044](../../public/scripts/datalog.js#L1027-L1044)).
- **Outline before a click.** With a mouse, moving shows nothing. Resting 0.3 s outlines, with a thin dark ring of radius 9 px,
  what a click would pin ([datalog.js:936-941](../../public/scripts/datalog.js#L936-L941), [datalog.js:977-980](../../public/scripts/datalog.js#L977-L980)).
- **Stop.** The button again, or Esc ([datalog.js:898](../../public/scripts/datalog.js#L898), [datalog.js:948](../../public/scripts/datalog.js#L948)).

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

`openCheck(name, idx)` shows one value of one variable ([datalog.js:787-795](../../public/scripts/datalog.js#L787-L795)), and
`runCheck()` writes three sections, all from the same frame ([datalog.js:804-843](../../public/scripts/datalog.js#L804-L843)):

1. **Stored in the dataset**: the value, its variable name and index, type, `computed_in`, `updates`, `formula`.
2. **Recomputed now, from the stored inputs**: the page's `check[name](idx)` returns a formula, a table of inputs and a value;
   `agreement()` compares it with the stored value ([datalog.js:796-803](../../public/scripts/datalog.js#L796-L803)). With
   $d = |\text{stored} - \text{recomputed}|$ and $s = \max(|\text{stored}|, |\text{recomputed}|)$, the two agree when
   $$d \le 2\times10^{-6}\,s + 10^{-7}$$
   for a `float32` array and
   $$d \le 10^{-9}\,s + 10^{-12}$$
   otherwise. The verdict says "identical" when $d = 0$, otherwise "agree to $n$ significant figures; the rest is float32
   storage" (or "rounding"), with $n = \lfloor -\log_{10}(d/s) \rfloor$; a larger gap reads "DIFFER by …". Strings and
   booleans are compared as text; two non-finite values are "both undefined now". Without a `check` entry the section shows the
   attribute `source` or says the value is an input read from a control.
3. **Read back from the picture**: the page's `drawn[name](idx)` returns what it read (a pixel colour, an SVG attribute),
   what the store predicts, `ok` and a note. `ok` has three values ([datalog.js:836](../../public/scripts/datalog.js#L836)):
   `true` gives a drawn tick (`CHK`, an inline SVG, [datalog.js:171](../../public/scripts/datalog.js#L171)) and "The picture shows
   this value." on tan (`is-ok`); `false` gives "✕ The picture does not match." in white on the
   burgundy accent (`is-bad`); `null` means the value is not in the picture at the moment, for example a curve that is not drawn because there
   is nothing to draw. Then the verdict is neutral, without a mark: "Not in the picture at the moment, so there is nothing to
   read back.", in muted ink inside a dashed outline (`is-na`, [data.css:296](../../public/styles/data.css#L296)). Only `null`
   itself counts; a missing `ok` is falsy and reads as a mismatch. Without a `drawn` entry, the section shows `drawn_note` or
   says the value enters the picture only through arrays computed from it.

Measured on Fig. 2: the denominator `den` (stored 3.3590 kg, recomputed 3.358995) and the energy `E` (18.305709 J) are
"identical"; the bob position `x2_px` (332.6 css px) is "identical" and "The picture shows this value."

### Record one round

A round is what the page says it is, in `Sim.data.round` ([datalog.js:27-29](../../public/scripts/datalog.js#L27-L29)):

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
| 11 | two seconds of the stored run | `t_play` | sampled | yes, in the last two seconds of the run | [L1330](../../public/simulations/pendulum-control.html#L1330) |
| Portfolios 02 (Rotor Pendula) | one turn of the rotor in the stored record, $T = 2\pi/\Omega$ | `t_now` | sampled | yes, when less than one turn of the record is left before the playback loops | `Sim.data` in [rotor_sim.html](../../portfolios-src/rotor-pendula/rotor_sim.html) |
| Portfolios 02 (Rotor Pendula, wind tab) | one turn of the rotor at the steady speed of the mean wind, $2\pi/\Omega_0$ | `t` | live | while the wind is still being synthesised | `Sim.data` in [rotor_wind.html](../../portfolios-src/rotor-pendula/rotor_wind.html) |
| Portfolios 03, ideal press | one run, $t = 0$ to its end; Record plays it from $t = 0$ | `tView` | sampled | yes, while the run plays | `Sim.data` in [hydraulic.html](../../portfolios-src/hydraulics/hydraulic.html) |
| Portfolios 03, servo press | one press cycle, $t = 0$ to its end | `tView` | sampled | yes, before the first cycle arrives and while it plays | `Sim.data` in [hydraulic_control.html](../../portfolios-src/hydraulics/hydraulic_control.html) |
| Droplet Collection, panel 4 (a cloud with a shape) | five cloud-minutes, $t$ to $t + 300$ s; Record presses Start if the cloud is paused; the followed point is the largest drop | `t` | sampled | yes, in the last five minutes before the cloud stops at 45 min | `Sim.data` in [datahooks.js](../../portfolios-src/droplets/datahooks.js), store written in [app.js](../../portfolios-src/droplets/app.js) |
| Portfolios 04 (Iron, Cotton and the Head) | one drop, $t = 0$ to 9 s of the stored run; Record starts a new drop from $t = 0$ | `t_play` | sampled | yes, while a drop is under way | [index.html L989](../../public/portfolios/impact/index.html#L989), [ar.html](../../public/portfolios/impact/ar.html); source [datahooks.js](../../portfolios-src/impact/datahooks.js) |

While no round is running, `describeRound()` ([datalog.js:1057-1064](../../public/scripts/datalog.js#L1057-L1064)) writes the line
under the toolbar: "One round = …", then a longer sentence in `span.dp-more-txt`, which phones hide
([data.css:412](../../public/styles/data.css#L412)). When the page's `blocked()` gives a reason, it follows, after a space, in its
own `span.dp-rec__why` ("**Not now.** …", [datalog.js:1062](../../public/scripts/datalog.js#L1062)). On a phone the whole line is
hidden to save height, except while a round records or while it holds such a reason
([data.css:410-411](../../public/styles/data.css#L410-L411)), so the reason still shows on phones.

`startRound()` ([datalog.js:1066-1089](../../public/scripts/datalog.js#L1066-L1089)) refuses with the page's reason if `blocked`
returns one ([1069](../../public/scripts/datalog.js#L1069)). If a round becomes blocked while it records, the progress line shows
the reason ("**Waiting.**", [1093-1094](../../public/scripts/datalog.js#L1093-L1094)). Otherwise it presses Play if the simulation
is paused, chooses the point to follow (the pinned point, else `round.point()`), and prepares one buffer per numeric scalar of the whole store (`scalarNames()`, every scalar of type `float`, `int` or
`bool`), one per row of the followed point, and two for time. It also notes the first section's scalars as the round's
parameters. In sampled mode the target spacing is the round length over 600; the final slot is reserved for the ending frame. In change mode it is zero and the 600-change cap is unchanged.

`recordFrame()` runs once per frame while recording ([datalog.js:1098-1128](../../public/scripts/datalog.js#L1098-L1128)). It reads
the time variable (or `performance.now()` if there is none, [datalog.js:103](../../public/scripts/datalog.js#L103)); the first
frame sets $t_0$, and the elapsed time is $t - t_0$. A frame is taken when

- sampled mode: it is the first, or at least $0.999 \cdot L/600$ after the last taken one, or the round has ended (within 10⁻⁹ s);
- change mode: the joined values of `round.columns` differ from the last frame's.

At most 600 samples are taken; sampled rounds reserve slot 600 for the ending frame (`MAXS`, [datalog.js:1052](../../public/scripts/datalog.js#L1052)). A taken frame stores $t$, the
elapsed time, every numeric scalar (booleans as 1 or 0, anything else not numeric as NaN), and each row of the followed point,
or NaN when the page's rows for that point changed shape ([datalog.js:1112-1120](../../public/scripts/datalog.js#L1112-L1120)). A row is matched by its label and
variable name, not by its index (since 23 October 2026): on a stored run the followed point's index moves with the playback (Figs. 9, 10, the impact
study), and matching the index as well made every sample after the first NaN. The series keeps the index of the first sample in its name. The
progress bar is repainted every 125 ms ([datalog.js:1124-1126](../../public/scripts/datalog.js#L1124-L1126)). The round ends when
the elapsed time reaches $L$ (or, in change mode, at 600 samples), when Stop is pressed, or when time runs backwards because
the page restarted ("the clock was reset", [datalog.js:1103](../../public/scripts/datalog.js#L1103)). A round with fewer than two
samples is dropped with a message ([datalog.js:1136](../../public/scripts/datalog.js#L1136)).

`finishRound()` turns the buffers into `Float64Array` series: time first, then one per chart column, then one per row of the
followed point, keyed `<variable>[_<index>]_at_point` ([datalog.js:1129-1155](../../public/scripts/datalog.js#L1129-L1155)). The
last five rounds are kept ([datalog.js:1147](../../public/scripts/datalog.js#L1147)); the panel opens on the Rounds tab. Each
round shows: chips to switch rounds, the parameters at the start, one chart per quantity that changed (black lines for the
followed point, burgundy for the rest), one line for quantities that stayed constant or were undefined, and a collapsible
table of every sample ([datalog.js:1194-1229](../../public/scripts/datalog.js#L1194-L1229)). Pointing at a chart draws a cursor on
every chart at the nearest sample and lists all values at it ([datalog.js:1240-1252](../../public/scripts/datalog.js#L1240-L1252)).

Measured on Fig. 2: a 10 s round gave 600 samples from 601 frames, 15 series (time, 7 columns, 7 rows of the followed bob) and
52 recorded scalars after adding the twin screen coordinates; a controlled 60 Hz run now keeps the ending sample at 10.000000000000776 s (the 7.8 × 10⁻¹³ s gap is float64 accumulation).

### Save: what goes into the files

| Button | File name | Contents | Lines |
|---|---|---|---|
| Save (toolbar) | `<file>-<stamp>.zip` | the store via `ds.npz`: one `.npy` per array, `dataset.json`; then `round-<n>.csv` for each kept round and `README.txt` | [1312-1317](../../public/scripts/datalog.js#L1312-L1317) |
| Save this round | `<file>-round-<n>-<stamp>.zip` | a new dataset with dimension `sample`, coordinate `time_into_round`, one `float64` variable per series and per recorded scalar, attributes (page, round label, samples, frames, time caught, time variable, followed point, `start_<parameter>`); plus `round.csv` and `README.txt` | [1277-1287](../../public/scripts/datalog.js#L1277-L1287) |
| CSV | `<file>-round-<n>-<stamp>.csv` | the round as CSV | [1276](../../public/scripts/datalog.js#L1276) |

`<file>` is `Sim.data.file` (for example `fig2-double-pendulum`, [Double Pendulum.html:769](../../public/simulations/Double%20Pendulum.html#L769));
`<stamp>` is the UTC time as `YYYY-MM-DDTHH-MM-SS` ([datalog.js:1270](../../public/scripts/datalog.js#L1270)). The download goes
through a temporary object URL that is revoked after 4 s ([datalog.js:1261-1269](../../public/scripts/datalog.js#L1261-L1269)).

The CSV ([datalog.js:1254-1260](../../public/scripts/datalog.js#L1254-L1260)) has the header `sample,time_into_round,` then the series
keys, then every other recorded scalar; one row per sample, numbers written with `String(v)` (full double precision), NaN as an
empty cell, `\n` line ends. Units are not in the CSV; they are in the round archive's `dataset.json`.

The actual filename is generated once and passed to both the README and the download, for the store and for an individual round.

The README ([datalog.js:1291-1311](../../public/scripts/datalog.js#L1291-L1311)) names the page and the time, explains the layout and
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
([datalog.js:9-49](../../public/scripts/datalog.js#L9-L49)). Keys in the left column are read where shown; the right column says
which pages set them (from the `Sim.data = {` blocks of the ten pages of 14 October 2026; Fig. 11, added 24 October, has one too).

| Key | Shape | Read at | Set by |
|---|---|---|---|
| `ds` | the dataset | [66](../../public/scripts/datalog.js#L66) | all |
| `kicker` | text above the title (default: the dataset title) | [202](../../public/scripts/datalog.js#L202) | all |
| `file` | base name of saved files | [1276](../../public/scripts/datalog.js#L1276), [1285](../../public/scripts/datalog.js#L1285), [1313](../../public/scripts/datalog.js#L1313) | all |
| `playing` | `() → bool` | [1366](../../public/scripts/datalog.js#L1366), [1070](../../public/scripts/datalog.js#L1070), [1092](../../public/scripts/datalog.js#L1092) | all |
| `play` | `() → void` | [1070](../../public/scripts/datalog.js#L1070) | all except Fig. 3 |
| `groups` | `[{ title, note, vars }]`; the sections when there is no `ledger` | [135](../../public/scripts/datalog.js#L135) | all |
| `ledger` | the bookkeeper's layout, below | [132](../../public/scripts/datalog.js#L132) | Figs. 9, 10 and 11 and Rotor Pendula, from [scripts/ledger/](../../public/scripts/ledger/); Droplet Collection, in [datahooks.js](../../portfolios-src/droplets/datahooks.js) |
| `colour` | `{ name: (value, j, i) → [r, g, b] \| null }`, presentation only | [128](../../public/scripts/datalog.js#L128) | all except Figs. 2 and 10 |
| `rowLabel` | `{ dim: (j) → text }` | [677](../../public/scripts/datalog.js#L677), [691](../../public/scripts/datalog.js#L691) | Figs. 2, 3, 5, 6, 7, 8 |
| `colLabel` | `{ name: (i) → html }` | [690](../../public/scripts/datalog.js#L690) | Figs. 1, 2 |
| `at` | `{ name: (j[, i]) → html }`, a note after a table cell's value | [680](../../public/scripts/datalog.js#L680), [694](../../public/scripts/datalog.js#L694) | Figs. 1, 2 |
| `probe` | `(x, y) → ref \| null`, CSS px in `#stage` | [857](../../public/scripts/datalog.js#L857) | all |
| `inspect` | `(ref) → { title, at: {x, y}, rows: [[symbol, value, units, varName, index]] }` | [978](../../public/scripts/datalog.js#L978), [1001](../../public/scripts/datalog.js#L1001), [1071](../../public/scripts/datalog.js#L1071) | all |
| `locate` | `(varName, index) → {x, y} \| null` | [985](../../public/scripts/datalog.js#L985) | all |
| `check` | `{ name: (index) → { formula, inputs: [[symbol, value, units, digits]], value } }` | [513](../../public/scripts/datalog.js#L513), [817](../../public/scripts/datalog.js#L817) | all |
| `drawn` | `{ name: (index) → { what, drawn, expected, ok, note } }`; `ok` is `true`, `false` or `null` (nothing drawn to read back now) | [831](../../public/scripts/datalog.js#L831) | all |
| `round` | `{ label, time, length, columns, point, mode?, blocked? }` | [158](../../public/scripts/datalog.js#L158) | all (table above) |
| `about` | HTML paragraph: what still differs between store and picture | [229](../../public/scripts/datalog.js#L229) | all |

### `Sim.data.ledger`

The field the redesign added. A page without it falls back to its `groups`, with no headline and no books, so no page broke
while the others are converted. Figs. 9, 10 and 11 keep their ledger in a file of its own, `scripts/ledger/<page>.js`, loaded
between the page's script and `datalog.js` on the line that loaded `datalog.js`, so no line of the page moved (the docs cite the
pages by line number). A ledger file only names variables and adds checks; it computes nothing for display. Rotor Pendula's
simulation loads [scripts/ledger/rotor-pendula.js](../../public/scripts/ledger/rotor-pendula.js) the same way, and its wind tab [scripts/ledger/rotor-wind.js](../../public/scripts/ledger/rotor-wind.js), from its source
`portfolios-src/rotor-pendula/rotor_sim.html` (see [portfolios.md](../portfolios.md#rotor-pendula-rotor-pendula)). Droplet Collection,
generated by its build, keeps its ledger at the end of its hooks (`portfolios-src/droplets/datahooks.js`).

| Field | Shape | Read at |
|---|---|---|
| `headline` | `[{ v: name, title: 'short word' }]`, 3 to 7 scalars | [144](../../public/scripts/datalog.js#L144) |
| `window` | frames a headline sparkline keeps (default 360) | [425](../../public/scripts/datalog.js#L425) |
| `sections` | `[{ title, note, vars, how, folded }]`, in causal order; `how` is `set`, `constant`, `formula`, `run`, `solver` or `drawing` | [135](../../public/scripts/datalog.js#L135) |
| `how` | `{ name: kind }`, overrides the section's kind | [146](../../public/scripts/datalog.js#L146) |
| `books` | `[{ title, short, note, rows: [[±1, name]], total, residual, tol, paused }]`; the page stores `residual` = rows − total; `paused() → reason \| null` | [145](../../public/scripts/datalog.js#L145), [477](../../public/scripts/datalog.js#L477) |
| `deps` | `{ name: [input names] }`, which inputs each derived variable uses | [148](../../public/scripts/datalog.js#L148) |
| `controls` | `{ elementId: name }`, where a control's `id` is not its variable's name (Fig. 9: `kspring` → `k`; Fig. 10: `rpm` → `rpm_ref`) | [580](../../public/scripts/datalog.js#L580) |
| `current` | `{ dimension: name }`, the index of the element shown now (`n: 'i_now'`) | [385](../../public/scripts/datalog.js#L385) |
| `check` | more `check` entries, used where the page has none | [133](../../public/scripts/datalog.js#L133) |

The two ledgers, as designed on paper before the code:

| | Fig. 9, driven oscillator | Fig. 10, wind turbine |
|---|---|---|
| Headline | x, ẋ, F, u, E, W<sub>in</sub>, W<sub>loss</sub> | v, n<sub>rot</sub>, λ, c<sub>p</sub>, P<sub>gen</sub>, E<sub>gen</sub> |
| Sections | What you set · What follows from it · The state now · The stored run · The previous run (folded) · Curves of the figures (folded) · Solver (folded) · Drawing (folded) | What you set · The turbine · What follows from it · The state now · The stored run · Over the whole run · Power curve (folded) · Solver (folded) · Drawing (folded) |
| Books | Energy; Newton’s second law | Energy |
| New stored values | `as`, `E0`, `ma_now`, `bal_now`, `fres_now` | `Eas`, `Ea_now`, `Eg_now`, `K_now`, `K0`, `ebal_now` |
| New checks (ledger file) | the 16 numbers copied from the run (x = x<sub>n</sub> at n = n<sub>now</sub>, or "from the drag" while held), `as`, `ma_now`, `E0`, `bal_now`, `fres_now`, `stable`, `fp_kind` | the 8 numbers copied from the run, `K_now`, `K0`, `ebal_now` |

The ten blocks: [Fig. 1 L798](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L798),
[Fig. 2 L768](../../public/simulations/Double%20Pendulum.html#L768),
[Fig. 3 L849](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L849),
[Fig. 4 L996](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L996),
[Fig. 5 L810](../../public/simulations/water-wave.html#L810),
[Fig. 6 L868](../../public/simulations/wave-interference.html#L868),
[Fig. 7 L1370](../../public/simulations/phasor-sums.html#L1370),
[Fig. 8 L1301](../../public/simulations/draw-decompose.html#L1301),
[Fig. 9 L1690](../../public/simulations/driven-oscillator.html#L1690),
[Fig. 10 L1056](../../public/simulations/wind-turbine.html#L1056).

## Public interface

| Name | Lines | Arguments | What it does / returns |
|---|---|---|---|
| `Sim.colourMap` | [103-110](../../public/scripts/datalog.js#L103-L110) | `v, lim` | `[r, g, b]` on a diverging scale: $a = v/\text{lim}$ clipped to $[-1, 1]$, $s = |a|^{0.8}$, mixed from the paper colour (255, 250, 243) towards dark (58, 50, 46) for negative or burgundy (122, 31, 43) for positive values. Pages use it in their `colour` functions. |
| `window.__dataPanel` | [1421](../../public/scripts/datalog.js#L1421) | | `{ running(), rounds(), recording() }`: hooks for tests. |
| `Sim.data` | [11-49](../../public/scripts/datalog.js#L11-L49) | | The contract above, provided by the page. |

## Internal functions

| Name | Lines | What it does |
|---|---|---|
| `load`, `store` | [71-72](../../public/scripts/datalog.js#L71-L72) | Read and write `localStorage` under `datapanel.`; silent if storage is blocked. |
| `esc`, `plain`, `grouped`, `num`, `sci` | [73-88](../../public/scripts/datalog.js#L73-L88) | Escaping; HTML symbol to text; grouped integers; display text of any value; exponent text. |
| `sciHTML` | [90-97](../../public/scripts/datalog.js#L90-L97) | A small number as 2.1×10<sup>−9</sup>, or in plain decimals between 10⁻² and 10⁴. |
| `textOn`, `safe`, `clock` | [98-100](../../public/scripts/datalog.js#L98-L100) | Text colour on a cell; run page code without letting it throw; wall-clock time. |
| `V`, `A`, `sym`, `digitsOf`, `unitOf`, `kindOf`, `typeLabel`, `shapeLabel`, `rows2`, `cols2`, `colourFn`, `isNumScalar` | [114-129](../../public/scripts/datalog.js#L114-L129) | Reading the store. |
| `howOf` | [146](../../public/scripts/datalog.js#L146) | How a variable is obtained. |
| `timeNow`, `timeSym`, `timeUnit`, `timeText`, `timeHTML` | [160-165](../../public/scripts/datalog.js#L160-L165) | The round's time variable and its display (`timeHTML` left to right). |
| `palette` | [243-249](../../public/scripts/datalog.js#L243-L249) | Colours from the panel's CSS tokens, cached. |
| `fracOf`, `checkBtnHTML`, `meaningHTML` | [253-258](../../public/scripts/datalog.js#L253-L258) | Decimal box width of a group of rows; a Check button; the Meaning cell. |
| `folded`, `stats` | [313-323](../../public/scripts/datalog.js#L313-L323) | Whether a section is folded; min, max, mean cached by version. |
| `parts`, `setParts` | [325-337](../../public/scripts/datalog.js#L325-L337) | A value as the two halves of a decimal-aligned cell, and writing them only when they changed. |
| `drawThumb`, `currentIndex`, `drawSpark` | [338-413](../../public/scripts/datalog.js#L338-L413) | An array's picture; the element shown now; the cached picture plus that element's dot. |
| `feedHeads`, `drawHeads`, `paintHeads` | [426-469](../../public/scripts/datalog.js#L426-L469) | The headline: buffers, sparklines, numbers. |
| `sum`, `setH`, `paintBooks` | [477-507](../../public/scripts/datalog.js#L477-L507) | The books: residuals and verdicts, and the summary under the headline. |
| `checkState` | [512-520](../../public/scripts/datalog.js#L512-L520) | Stored against recomputed, for the Check column. |
| `paintLedger`, `paintInstant`, `catchNow` | [522-566](../../public/scripts/datalog.js#L522-L566) | The table's words, Δ and blink; the instant line; catching an instant. |
| `markFrom` | [569-577](../../public/scripts/datalog.js#L569-L577) | Cause and effect after a control moves. |
| `makeGrid` | [585-649](../../public/scripts/datalog.js#L585-L649) | Virtual table; inner `sizeTo`, `layout`, `fill`, `paintGrid`, `mark`, `onPoint`. |
| `takeSnap`, `snapStats`, `checkButton`, `gridSource`, `paintArray` | [652-714](../../public/scripts/datalog.js#L652-L714) | An array copied at one instant, and its table. |
| `closeArray`, `openArray`, `toggleDetail`, `narrow` | [715-761](../../public/scripts/datalog.js#L715-L761) | An array row opening in place; the detail row on a narrow panel. |
| `openCheck`, `agreement`, `runCheck` | [787-843](../../public/scripts/datalog.js#L787-L843) | Check view. |
| `stageXY`, `refAt`, `setRead` | [854-873](../../public/scripts/datalog.js#L854-L873) | Pointer position in the figure; probe with rings; Read on/off (both buttons). |
| `touched`, `wipe`, `drawRing`, `drawPin`, `clearOverlay`, `paintProbe` | [951-997](../../public/scripts/datalog.js#L951-L997) | Overlay drawing; marker every frame, words at most every 250 ms. |
| `rowsKey`, `paintStrip` | [998-1045](../../public/scripts/datalog.js#L998-L1045) | The strip under the figure and the "Pinned point" box, which shows only while a point is pinned. |
| `roundLength`, `describeRound`, `scalarNames`, `startRound`, `progress`, `recordFrame`, `finishRound` | [1056-1155](../../public/scripts/datalog.js#L1056-L1155) | Recording. |
| `seriesRange`, `drawChart`, `renderRounds` | [1158-1253](../../public/scripts/datalog.js#L1158-L1253) | The Rounds view. |
| `roundCsv`, `download`, `stamp`, `readme` | [1254-1311](../../public/scripts/datalog.js#L1254-L1311) | Files. |
| `show`, `setOpen`, `setLive` | [1321-1358](../../public/scripts/datalog.js#L1321-L1358) | Switch view; open or close the panel; Live on or off. |
| `playingNow`, `paintState`, `paint`, `everyFrame` | [1366-1385](../../public/scripts/datalog.js#L1366-L1385) | The clock; the state label; the four-times-a-second words; the every-frame pictures. |
| `wanted`, `kick`, `frame`, `poke` | [1389-1404](../../public/scripts/datalog.js#L1389-L1404) | The on-demand loop. |
| `soon` | [1418](../../public/scripts/datalog.js#L1418) | Refreshes the round description once per frame after any input or click. |

## State it keeps

- `localStorage`: `datapanel.open` (`'1'`/`'0'`), `datapanel.hold` (`'1'` when the reader switched Live off; Live is on by
  default), `datapanel.tab` (`'vars'`/`'rounds'`), and `datapanel.fold.<path>`, one `'1'`/`'0'` per section of that page
  ([datalog.js:1338](../../public/scripts/datalog.js#L1338), [1357](../../public/scripts/datalog.js#L1357),
  [1328](../../public/scripts/datalog.js#L1328), [770](../../public/scripts/datalog.js#L770)). `open`, `hold` and `tab` are the
  same for every page, so the choice carries from one figure to the next. The `datapanel.live` key of the earlier panel is no
  longer read.
- In memory: `isOpen`, `view`, `liveOn` ([1320](../../public/scripts/datalog.js#L1320)); `caught`
  ([559](../../public/scripts/datalog.js#L559)); `cells`, one record per row with its last text, value, Δ time and blink phase
  ([306-312](../../public/scripts/datalog.js#L306-L312)); `hl`, the headline's buffers ([421](../../public/scripts/datalog.js#L421));
  `current`, `snap`, `grid`, `openRow` (the open array, [651](../../public/scripts/datalog.js#L651)); `openDetail`; `marks`;
  `checking`; `held = { ref, cell }` and `probe` (Read values state, [849-850](../../public/scripts/datalog.js#L849-L850));
  `rounds` (at most 5), `roundNo`, `rec`, `sel` ([1052](../../public/scripts/datalog.js#L1052)); `running`, `pokeUntil`,
  `pressed` ([1388](../../public/scripts/datalog.js#L1388)); `statCache`. Rounds are lost on reload.
- DOM attributes and classes written: the page's `lang` and `dir` on the tab, the panel and the strip; `dir="ltr"` on every
  number; `body.dp-open`; `aria-expanded` on the tab and on array rows; `aria-hidden` and `inert` on the closed panel;
  `#stage.dp-reading` while reading; `aria-pressed` on both Read values buttons; `.dp-tab--away` while scrolling down on a
  phone; `.dp-rec.is-rec` while recording; on rows `is-blink0`/`is-blink1`, `is-cause`, `is-effect`, `is-open`; on sections
  `is-folded`, `is-effect`; on Check buttons `is-ok`, `is-bad`, `is-in`, `is-na`.
- DOM read: `#stage`, the `.stage__cap` inside `#stage`'s parent, `<html lang dir>`, the CSS tokens `--accent`, `--ink`,
  `--ink-3`, `--rule`, `--muted`, `--card-soft`.

## Timing and events

| What | Rate | Where |
|---|---|---|
| Panel loop | one animation frame while `wanted()`; none otherwise, and never while the panel is closed and nothing is recorded or pinned | [1389-1401](../../public/scripts/datalog.js#L1389-L1401) |
| Live: the panel's words (values, Δ, headline numbers, books, instant line) | at most every 250 ms (measured: at most 4 in any second) | [1397](../../public/scripts/datalog.js#L1397) |
| Live: headline sparklines, dots on the arrays on screen | every frame | [1381-1385](../../public/scripts/datalog.js#L1381-L1385) |
| Array pictures | at most every 250 ms, only after a version change | [393-398](../../public/scripts/datalog.js#L393-L398) |
| Check column | once a second | [524-525](../../public/scripts/datalog.js#L524-L525) |
| Δ fades | 1.5 s after the last change | [546](../../public/scripts/datalog.js#L546) |
| Rows marked after a control moves | 2 s | [576](../../public/scripts/datalog.js#L576) |
| Loop after a reader's action with the clock stopped | 1.5 s | [1404](../../public/scripts/datalog.js#L1404) |
| Read values: marker | every frame | [981-984](../../public/scripts/datalog.js#L981-L984) |
| Read values: words | at most every 250 ms | [996](../../public/scripts/datalog.js#L996) |
| Outline before a click | after 300 ms of rest | [941](../../public/scripts/datalog.js#L941) |
| Table cell shown in the figure | 600 ms after a hover, 3000 ms after a click; cancelled when the panel closes | [742](../../public/scripts/datalog.js#L742), [1340](../../public/scripts/datalog.js#L1340) |
| Recording: samples | every frame or every $L/600$, at most 600 | [1109](../../public/scripts/datalog.js#L1109) |
| Recording: progress bar | every 125 ms (8 per second) | [1126](../../public/scripts/datalog.js#L1126) |
| First instant | two animation frames after load | [1415](../../public/scripts/datalog.js#L1415) |
| Round description | at most once per frame, after an `input` or `click` anywhere | [1417-1420](../../public/scripts/datalog.js#L1417-L1420) |
| Object URL of a download | revoked after 4 s | [1268](../../public/scripts/datalog.js#L1268) |

Listeners: `window` `scroll` (passive) for the phone pill; `pointerdown`, `pointermove`, `pointerup`, `pointercancel` and
`click`, `mousedown`, `mouseup`, `dblclick`, `contextmenu` on `#stage` in the capture phase, all inactive unless Read values is
on; `pointerleave` on `#stage`; `keydown` on `document` (Esc stops reading) and on the panel (Esc closes it); clicks on the
tab, close button, tabs, toolbar and inside the panes; `pointermove`/`pointerdown`/`pointerleave` on the round charts;
`visibilitychange`; on `document` in the capture phase `input` (cause and effect, round description), and `input`, `change`,
`click`, `keydown`, `pointerdown` (`poke`); `pointerup`, `pointercancel` on `window`; `ResizeObserver` on `#stage` and on an open
array's table; an `IntersectionObserver` on the array rows.

## Contracts with other files

- **`dataset.js`**: the store and its fields `title`, `dims`, `vars`, `order`, methods `get`, `dtype`, `along`, `npz`; for a
  round archive, `Sim.dataset` and the new store's `dim`, `coord`, `var`, `set`, `has` and `npz`
  ([datalog.js:970-978](../../public/scripts/datalog.js#L970-L978); [dataset.md](dataset.md)).
- **`sim.js`**: `Sim.fmt` for every number ([datalog.js:86](../../public/scripts/datalog.js#L86)); `readPixel` and
  `isBurgundy` are used by the `drawn` functions of Figs. 9, 10 and 11 ([sim.md](sim.md)).
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
- Text that changes while a figure runs: at most 4 rewrites per second (the 250 ms at [line 1397](../../public/scripts/datalog.js#L1397) for the ledger and [line 996](../../public/scripts/datalog.js#L996) for the strip). Measure after a change: what
  shows during a pointer sweep, how much of the figure the marker covers, how often the strip text changes.
- If you add a key to `Sim.data`, add it to the contract comment at the top of the file, which pages and maintainers read first.
- A number the ledger shows belongs to the store; a ledger file (`scripts/ledger/<page>.js`) only names variables, orders
  them and adds checks. A book's residual is stored by the page where it computes the rows; the panel adds them again only to
  prove the two agree.
- Keep new words in `T('…')` literals and run `python3 tools/i18n/build.py --check`: it reads `datalog.js`, the pages and the
  ledger files (`long_name`, `title`, `note`, `short`, `about`, `kicker`).
- Keep the alignment of numbers out of the mirrored stylesheet (`/*rtl:ignore*/`), or the decimal points part on Arabic
  pages.
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
   ([datalog.js:641](../../public/scripts/datalog.js#L641), [742](../../public/scripts/datalog.js#L742)). The pointer crosses the
   table, not the figure, but the figure changes. CLAUDE.md asks that nothing on a running figure react to the pointer merely
   crossing; whether this case is meant to be covered is not determined from the code.
8. Pressing Esc while focus is inside the panel and Read values is on does two things at once: it closes the panel
   ([datalog.js:1345](../../public/scripts/datalog.js#L1345)) and stops reading ([datalog.js:948](../../public/scripts/datalog.js#L948)).
9. AGENTS.md said the load order holds for "all eight figures"; it holds for all ten pages (load-order table in
   [sim.md](sim.md#load-order-on-the-pages)). Corrected to "all ten figures" on 14 October 2026.
10. Fixed on 2026-10-15: a read-back that returns `ok: null` gets a neutral verdict, "Not in the picture at the moment, so
    there is nothing to read back." (class `is-na`), instead of a burgundy ✕ ([datalog.js:836](../../public/scripts/datalog.js#L836)).
    Figs. 3, 6 and 10 return `null` when the value has nothing drawn (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
11. Fixed on 2026-10-15: the reason a round cannot start (`Sim.data.round.blocked`) sits in `span.dp-rec__why`, after a space,
    and shows on phones too; it used to sit inside `.dp-more-txt`, which is hidden at 640 px and below
    ([datalog.js:1062](../../public/scripts/datalog.js#L1062)) (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).
12. Redesigned on 24 October 2026 as a bookkeeper (skill `phyein-usul-bookkeeper`): a headline of live numbers, one table in
    causal sections with values aligned on the decimal point and a Δ column, the books with two residuals, arrays opening in
    place, Live on by default, cause-and-effect marks, the panel in the page's language and direction. It replaces the column of
    cards under a Record box and a "Pinned point" box, which held one instant until Live was switched on. Figs. 9 and 10 are
    the pilots; a page without `ledger` shows its groups in the new table.
13. Every page's `source` attribute (147 in all) is shown in Check through `T()` ([datalog.js:828](../../public/scripts/datalog.js#L828)),
    but `tools/i18n/build.py` does not collect `source:` yet, so on the German and Arabic pages these notes are still English.
    Left for the conversion of the other pages, where each page's notes are translated with its ledger.
