# Fig. 6 · Wave Interference Simulator

| | |
|---|---|
| Page | [public/simulations/wave-interference.html](../../public/simulations/wave-interference.html) (966 lines, 166 361 bytes) |
| Walkthrough | [public/scripts/walk/bench.js](../../public/scripts/walk/bench.js) (127 lines, key `bench`) |
| Thumbnail | [public/images/sims/wave-bench.webp](../../public/images/sims/wave-bench.webp) (800 × 500 px, 18 kB) |
| Catalog entry | [public/scripts/catalog.js#L132](../../public/scripts/catalog.js#L132) (lines 132–148, `id: 'wave-bench'`, `fig: 6`) |

A workbench for adding waves. The upper canvas has two panels: the sum of all waves on top, drawn in ink with a pale burgundy
fill down to the axis, and below it each wave on its own in its own colour
([wave-interference.html:56-64](../../public/simulations/wave-interference.html#L56-L64), [:674-714](../../public/simulations/wave-interference.html#L674-L714)).
A second canvas, Fig. 6b, is the amplitude spectrum: one vertical stem per distinct frequency
([:65-73](../../public/simulations/wave-interference.html#L65-L73)). The reader adds up to six waves, each with its own card of
four sliders (amplitude, frequency, phase, speed), removes them with ×, or loads one of three presets: one wave, beats, square
wave ([:76-101](../../public/simulations/wave-interference.html#L76-L101), [:591-620](../../public/simulations/wave-interference.html#L591-L620)).
Three readouts give the number of waves, the sum of amplitudes and the largest $|y|$ on screen. Below the figures come the
lecture note and the walkthrough "From symbols to code".

Lengths are pixels of the medium: the view always spans 800 px of it, whatever the screen size
([:496](../../public/simulations/wave-interference.html#L496)); "css px" means a screen pixel. Line links of the form `:NNN`
point into `wave-interference.html`.

## The physics in one picture

**Everyday picture.** Two guitar strings that are nearly in tune swell and fade together: beats. A noise-cancelling headphone
plays the noise upside down, and the two add to almost nothing. A synthesizer mixes pure tones; the ear takes a mixture apart
into its frequencies (note Section 01, [:127-134](../../public/simulations/wave-interference.html#L127-L134)).

**Model.** Each wave is a sine travelling along a one-dimensional medium, such as a long taut string. The wave equation is
linear, so the medium carries the sum of the waves (note Section 03). Giving the waves different speeds imitates a dispersive
medium (note Section 03, [:195](../../public/simulations/wave-interference.html#L195)). The note then derives beats and the
envelope speed (Section 04), the square wave's Fourier series and the Gibbs overshoot (Section 05), and the line spectrum with
Parseval's theorem (Section 06).

**What the code evaluates.** Wave $i$ has amplitude $A_i$ (px), "Frequency" $f_i$ (cycles per 200 px; hertz only at speed 1),
phase $\varphi_i$ (rad) and speed factor $s_i$ (dimensionless). At position $X$ (px, 0 to 800) and time $t$ (s)
([:622](../../public/simulations/wave-interference.html#L622)):

$$y_i(X, t) = A_i \sin\left(2\pi f_i \left(\frac{X}{200} - s_i t\right) + \varphi_i\right)$$

The stored derived quantities are the wave number, angular frequency, wavelength, phase speed and the frequency $\nu_i$ heard at
a fixed point ([:664](../../public/simulations/wave-interference.html#L664)):

$$k_i = \frac{2\pi f_i}{200}\ \mathrm{rad/px}, \quad \omega_i = 2\pi f_i s_i\ \mathrm{rad/s}, \quad \lambda_i = \frac{200}{f_i}\ \mathrm{px}, \quad v_i = 200\,s_i\ \mathrm{px/s}, \quad \nu_i = f_i s_i\ \mathrm{Hz}$$

with $\nu_i$ rounded to $10^{-6}$ Hz, so that equal frequencies compare equal. The sum and its largest value over the $M + 1$
samples $X_j = 800\,j/M$ of the current frame are ([:695-697](../../public/simulations/wave-interference.html#L695-L697)):

$$y(X, t) = \sum_i y_i(X, t), \qquad \text{peak} = \max_j |y(X_j, t)| \le \sum_i A_i .$$

For waves 1 and 2 the page stores the beat length and the envelope speed
([:669-670](../../public/simulations/wave-interference.html#L669-L670)), defined only when $f_1 \ne f_2$:

$$\lambda_\text{beat} = \frac{200}{|f_1 - f_2|}\ \mathrm{px}, \qquad v_\text{env} = 200\,\frac{f_1 s_1 - f_2 s_2}{f_1 - f_2}\ \mathrm{px/s} .$$

The spectrum groups the waves by $\nu$. Waves with the same $\nu$ add as phasors (arrows of length $A_i$ at angle $\varphi_i$);
the stem height is the length of the summed arrow, and at $\nu = 0$ the constant displacement at $X = 0$
([:727-739](../../public/simulations/wave-interference.html#L727-L739)):

$$C_\nu = \left|\sum_{i:\ \nu_i = \nu} A_i\,e^{\mathrm{i}\varphi_i}\right| \ (\nu > 0), \qquad C_0 = \left|\sum_{i:\ \nu_i = 0} A_i \sin\varphi_i\right| .$$

## How the code computes it

**State.** One inline script, an immediately invoked function
([:492-973](../../public/simulations/wave-interference.html#L492-L973)). Constants `WORLD_W = 800`, `MAX_WAVES = 6`, `FMAX = 3`
(top of the Frequency slider), `NUMAX = 6` (right end of the spectrum axis, $3 \times$ the top Speed of 2)
([:496](../../public/simulations/wave-interference.html#L496)), and six wave colours `COLOURS`
([:497](../../public/simulations/wave-interference.html#L497)). Two canvas wrappers, `box` for the plot and `spec` for the
spectrum ([:501-502](../../public/simulations/wave-interference.html#L501-L502), [sim.js:32-46](../../public/scripts/sim.js#L32-L46)).
The model state is the array `waves` of objects `{ id, colour, A, f, phi, s }`, the running id `uid`, the time `simT` (s), the
last `peak`, and `frames`, `fps` ([:504](../../public/simulations/wave-interference.html#L504),
[:570-577](../../public/simulations/wave-interference.html#L570-L577)). The slider callbacks write straight into a wave object
([:610-613](../../public/simulations/wave-interference.html#L610-L613)); everything else is recomputed from `waves` each frame.

**Numerical method.** None in the sense of an integrator: the formula above gives every wave at every place and time, so the
page evaluates it directly. Only the time accumulates, `simT += dt`
([:824](../../public/simulations/wave-interference.html#L824)), with $\Delta t$ from `Sim.clock`: real time between frames,
capped at 0.05 s, zero while paused ([sim.js:179-181](../../public/scripts/sim.js#L179-L181)). The values are exact to double
precision; the only approximation is drawing the curve as straight segments between samples (note Section 07,
[:448](../../public/simulations/wave-interference.html#L448)).

**Sampling.** One sample per css px column of the plot: `samples = max(2, round(right - left))`, with `left = 44` and
`right = w - 14`, so $M = w - 58$ ([:652](../../public/simulations/wave-interference.html#L652),
[:654](../../public/simulations/wave-interference.html#L654)). Sample $j$ sits at medium position $X_j = 800\,j/M$ and screen
column $44 + j$ ([:684-686](../../public/simulations/wave-interference.html#L684-L686)). Measured in headless Chromium: a
1440 × 900 window gives a plot 770 × 481 css px, $M$ = 712 and $\Delta X$ = 1.124 px; a 390 × 844 window gives 356 × 392,
$M$ = 298 and $\Delta X$ = 2.685 px.

**The frame loop, in order.** The clock callback ([:823-833](../../public/simulations/wave-interference.html#L823-L833)) runs
on every animation frame, playing or paused:

1. `simT += dt`, update the frame-rate average, increment frames, write `t`, `dt`, `fps`, `frames`, `playing` into the store
   ([:824-826](../../public/simulations/wave-interference.html#L824-L826)).
2. `draw()` ([:651-724](../../public/simulations/wave-interference.html#L651-L724)):
   1. Layout: margins 44 (left), 14 (right and bottom), 30 (top), a 44 css px gap between panels; the sum panel takes 56 % of
      the remaining height ([:652-653](../../public/simulations/wave-interference.html#L652-L653)).
   2. Sample count and the two vertical ranges `sumRange = nice(Σ A)` and `compRange = nice(max A)`, where
      `nice(v) = max(20, 10 ⌈v/10⌉)` ([:624](../../public/simulations/wave-interference.html#L624),
      [:654-656](../../public/simulations/wave-interference.html#L654-L656)). The sum's range is never below $\sum A_i$, so the
      sum cannot leave its panel.
   3. Resize the dimensions `wave` and `x`, fetch the arrays ([:657-660](../../public/simulations/wave-interference.html#L657-L660)).
   4. Per wave: copy $A, f, \varphi, s$ into the store, compute $k, \omega, \lambda, v, \nu$ and the value at the centre of the
      view, $y_i(400)$ ([:661-666](../../public/simulations/wave-interference.html#L661-L666)); then the scalars $M$, $\Delta X$,
      $R$, $R_\text{c}$, $\sum A$, $y(400)$, $y_1(400)$, beat length, envelope speed and the layout
      ([:667-671](../../public/simulations/wave-interference.html#L667-L671)).
   5. Clear; draw the two panels with grid lines at $0, \pm R/2, \pm R$ and their labels, `panel()`
      ([:672-676](../../public/simulations/wave-interference.html#L672-L676)).
   6. Components: for each wave and sample, evaluate $y_i$, convert to screen height
      `mid2 - y / compRange * hComp / 2`, store `y_comp` and `py_comp`, stroke 1.6 css px in the wave's colour
      ([:679-689](../../public/simulations/wave-interference.html#L679-L689)).
   7. Sum: for each sample add all waves, track the peak, convert with `sumRange`, store `X`, `y_sum`, `py_sum`; fill to the axis
      at 9 % burgundy, stroke 2.3 css px in ink; with no waves write the sample coordinates, zero sum and axis heights without drawing a sum curve ([:692-714](../../public/simulations/wave-interference.html#L692-L714)).
   8. Store `peak` and `ratio`; mark the arrays changed ([:721-723](../../public/simulations/wave-interference.html#L721-L723)).
3. `drawSpectrum()` ([:740-782](../../public/simulations/wave-interference.html#L740-L782)): axis from 0 to 6 Hz with ticks
   every 0.5 Hz and labels every 1 Hz, the axis name "ν / Hz"; `lines()` groups the waves; each stem is drawn from the base to
   `base - C / amax * (base - 14)` with a dot of radius 4.5 css px, where `amax = max(40, tallest stem)`; a stem shared by
   several waves is drawn in ink ([:737](../../public/simulations/wave-interference.html#L737)).
4. Every eighth frame, rewrite the "Sum of amplitudes" readout from the stored `sum_A` and the "Peak |y|" readout
   ([:829-832](../../public/simulations/wave-interference.html#L829-L832)).

Adding, removing and presets are events, not frame work: `add()`, `remove()` and `preset()` change `waves` and call `render()`,
which rebuilds every card from scratch, binds new sliders, writes `N` into the store and updates the wave count readout and the
caption ([:567-620](../../public/simulations/wave-interference.html#L567-L620), [:784-794](../../public/simulations/wave-interference.html#L784-L794)).

**Cost, precomputation and caching.** No caching: every frame re-evaluates every wave at every sample. `y()` is called twice per
component sample ([:684-685](../../public/simulations/wave-interference.html#L684-L685)) and once more per wave in the sum loop,
so a frame makes $3N(M+1)$ sine calls: 8 556 for the Square wave preset ($N$ = 4) at $M$ = 712, as the note states
([:445](../../public/simulations/wave-interference.html#L445)). The spectrum is redrawn every frame although it changes only
with the sliders. The store's typed arrays are reused while their sizes stay the same
([dataset.js:64-70](../../public/scripts/dataset.js#L64-L70)).

## Function map

Line numbers link into `wave-interference.html`.

| Function | Lines | What it does |
|---|---|---|
| `nextColour()` | [559-565](../../public/simulations/wave-interference.html#L559-L565) | First colour of `COLOURS` not yet used by a wave. |
| `add(p)` | [567-579](../../public/simulations/wave-interference.html#L567-L579) | Appends a wave (defaults A = 20, f = 1, φ = 0, s = 1) unless six exist; calls `render()`. |
| `remove(id)` | [581-584](../../public/simulations/wave-interference.html#L581-L584) | Drops a wave by id; calls `render()`. |
| `field(w)` | [586-589](../../public/simulations/wave-interference.html#L586-L589) | HTML of one labelled range input with its `<output>`. |
| `render()` | [591-620](../../public/simulations/wave-interference.html#L591-L620) | Rebuilds the wave cards, binds × and the four sliders, disables Add at six, stores `N`, writes `r-n` and `cap-n`. |
| `y(w, X)` | [622](../../public/simulations/wave-interference.html#L622) | One wave at position X and the current `simT`. |
| `nice(v)` | [624](../../public/simulations/wave-interference.html#L624) | Axis range: `max(20, ceil(v / 10) * 10)`. |
| `panel(top, height, range, title, left, right, formula)` | [626-649](../../public/simulations/wave-interference.html#L626-L649) | Title, formula (via `Sim.tex`), five grid lines and three tick labels of one panel; returns its axis height `mid`. |
| `draw()` | [651-724](../../public/simulations/wave-interference.html#L651-L724) | One frame of the plot; writes all per-wave, sampled and layout values. |
| `lines()` | [727-739](../../public/simulations/wave-interference.html#L727-L739) | Groups waves by ν and sums their phasors; returns `{ nu, A, colour }` per stem. |
| `drawSpectrum()` | [740-782](../../public/simulations/wave-interference.html#L740-L782) | One frame of the spectrum; writes `nu_line`, `A_line`, `x_line`, `y_line`, `amax`. |
| `preset(items)` | [784-788](../../public/simulations/wave-interference.html#L784-L788) | Replaces all waves with the given list, colours in order. |
| button handlers | [789-794](../../public/simulations/wave-interference.html#L789-L794) | One wave, Beats, Square wave, Add wave +. |
| `Sim.live` | [797-821](../../public/simulations/wave-interference.html#L797-L821) | Live values for the walkthrough, read from the store. |
| clock callback `(dt)` | [823-833](../../public/simulations/wave-interference.html#L823-L833) | Advances `simT`; calls `draw()`, `drawSpectrum()`; readouts every 8th frame, `r-sum` from the stored `sum_A`. `Sim.playButton` binds Pause at [834](../../public/simulations/wave-interference.html#L834). |
| `pixelAt(c, bx, x, y)` | [839](../../public/simulations/wave-interference.html#L839) | The device pixel containing a css point (floor, not round). |
| `rgbText(px)` | [840](../../public/simulations/wave-interference.html#L840) | Pixel as text; "nothing (transparent)" at alpha 0. |
| `lum(px)` | [841](../../public/simulations/wave-interference.html#L841) | Luminance of a pixel. |
| `waveOf(q)`, `sampleOf(q)` | [842](../../public/simulations/wave-interference.html#L842), [845](../../public/simulations/wave-interference.html#L845) | Wave and sample of a flat index into `wave × x`. |
| `onStroke(arr, i, off)` | [844](../../public/simulations/wave-interference.html#L844) | Where to read a stroke back; at the two ends, the midpoint of the end segment. |
| `waveInputs(wi)` | [846](../../public/simulations/wave-interference.html#L846) | Stored A, f, s, φ, t of one wave, for a check. |
| `yAt(wi, X)` | [847](../../public/simulations/wave-interference.html#L847) | The wave formula again, from stored inputs only (for checks). |
| `niceOf(v)` | [848](../../public/simulations/wave-interference.html#L848) | `nice()` again, for checks. |
| `sumA()` | [849](../../public/simulations/wave-interference.html#L849) | Σ A from the stored `A`. |
| `linesNow()` | [850-860](../../public/simulations/wave-interference.html#L850-L860) | `lines()` again, from the stored `nu`, `A`, `phi`. |
| `benchRound()` | [862-867](../../public/simulations/wave-interference.html#L862-L867) | Length of one round: 1 000 000 / gcd of the stored ν in units of 10⁻⁶ Hz, at most 20 s; 5 s if all ν are 0. |
| `Sim.data.playing`, `.play` | [870](../../public/simulations/wave-interference.html#L870), [963](../../public/simulations/wave-interference.html#L963) | Clock state; start the clock before a round. |
| `Sim.data.rowLabel.wave` | [879](../../public/simulations/wave-interference.html#L879) | Row names "w1", "w2", … |
| `Sim.data.colour.*` | [880-884](../../public/simulations/wave-interference.html#L880-L884) | Shading of `y_comp`, `y_400` (scale $A_i$) and `y_sum` (scale Σ A) with `Sim.colourMap`. |
| `Sim.data.probe(x, y)` | [885-894](../../public/simulations/wave-interference.html#L885-L894) | Sample column under the point; nearest curve (sum or a component) within 14 css px vertically. |
| `Sim.data.inspect(ref)` | [895-901](../../public/simulations/wave-interference.html#L895-L901) | Rows for a pinned point of the sum (X, Σ y, y px) or of a wave (X, $y_i$, A, f, φ, s, y px). |
| `Sim.data.locate(name, idx)` | [902-910](../../public/simulations/wave-interference.html#L902-L910) | Where a cell is drawn: a sample of a curve, or the middle sample of a wave; `null` for spectrum rows. |
| `Sim.data.check.*` | [911-945](../../public/simulations/wave-interference.html#L911-L945) | For 33 variables: formula, stored inputs, recomputed value. |
| `Sim.data.drawn.*` | [946-960](../../public/simulations/wave-interference.html#L946-L960) | Read-backs for `sum_A` (the visible `r-sum` readout), `py_sum` (ink, luminance < 150; `ok: null` when there are no waves, [948](../../public/simulations/wave-interference.html#L948)), `py_comp` (alpha first, then the wave RGB or a stored crossing within 2 css px) and `y_line` (the stem's dot). |
| `Sim.data.round.label` | [961](../../public/simulations/wave-interference.html#L961) | "one repeat of the pattern, … s" or "twenty seconds of the pattern, 20.00 s". |
| `Sim.data.round.point` | [962](../../public/simulations/wave-interference.html#L962) | The sum at the middle sample. |
| start-up | [967-971](../../public/simulations/wave-interference.html#L967-L971) | One default wave, a first draw of both canvases, resize observers for both. |

## Controls

| Control | Element id | Range / default | What it changes in the code |
|---|---|---|---|
| Pause / Play | `play` | playing at load, unless the reader prefers reduced motion ([sim.js:177](../../public/scripts/sim.js#L177)) | `clk.toggle` via `Sim.playButton` ([:834](../../public/simulations/wave-interference.html#L834)). |
| Add wave + | `add` | up to 6 waves | `add()` with defaults A = 20 px, f = 1, φ = 0, s = 1; disabled at six ([:615](../../public/simulations/wave-interference.html#L615)). |
| One wave | `p-one` | — | `preset([{ A: 20, f: 1 }])` ([:789](../../public/simulations/wave-interference.html#L789)). |
| Beats | `p-beats` | — | Two waves, A = 18 px, f = 1 and 1.25 ([:790](../../public/simulations/wave-interference.html#L790)). |
| Square wave | `p-square` | — | Four waves, n = 1, 3, 5, 7: A = round(30/n, 0.1) = 30, 10, 6, 4.3 px; f = 0.4 n ([:791-793](../../public/simulations/wave-interference.html#L791-L793)). |
| Amplitude (per card) | `w<id>A` | 0–40 px, step 1, default 20 ([:603](../../public/simulations/wave-interference.html#L603)) | `w.A` ([:610](../../public/simulations/wave-interference.html#L610)). |
| Frequency (per card) | `w<id>f` | 0.1–3 "Hz", step 0.05, default 1 ([:604](../../public/simulations/wave-interference.html#L604)) | `w.f` ([:611](../../public/simulations/wave-interference.html#L611)). |
| Phase (per card) | `w<id>p` | 0–6.28 rad, step 0.05, default 0, shown as a multiple of π ([:605](../../public/simulations/wave-interference.html#L605), [:612](../../public/simulations/wave-interference.html#L612)) | `w.phi`. |
| Speed (per card) | `w<id>s` | 0–2, step 0.05, default 1 ([:606](../../public/simulations/wave-interference.html#L606)) | `w.s` ([:613](../../public/simulations/wave-interference.html#L613)). |
| Remove × (per card) | none; class `wave__x` | — | `remove(w.id)` ([:609](../../public/simulations/wave-interference.html#L609)). |
| Read values | added by datalog.js into the plot's caption | off | Pins a point of a curve; see [datalog.md](../scripts/datalog.md). |

The card ids use the wave's running `id`, which only grows ([:571](../../public/simulations/wave-interference.html#L571),
[:598](../../public/simulations/wave-interference.html#L598)); the heading "Wave n" uses the card's position. The page starts
with wave id 1; pressing Square wave then makes ids 2–5, so the fourth card's amplitude slider is `w5A` (measured). The Frequency slider is labelled in hertz, but it is $f_i$,
which equals the frequency at a fixed point only at Speed 1 (note Section 02,
[:146](../../public/simulations/wave-interference.html#L146)).

## What the page writes into the data store

The store is created at [:507](../../public/simulations/wave-interference.html#L507):
`Sim.dataset({ title: 'Wave interference bench', attrs: { figure: 6, page, WORLD_W: 800, MAX_WAVES: 6, FMAX: 3, NUMAX: 6,
px_per_wavelength_unit: 200, left: 44, top1: 30, gap: 44, length_unit } })`. How the store works is in
[dataset.md](../scripts/dataset.md).

**Dimensions.** `wave` (number of waves), `x` (samples, $M + 1$), `line` (spectrum stems), declared with length 0
([:510](../../public/simulations/wave-interference.html#L510), [:530](../../public/simulations/wave-interference.html#L530),
[:536](../../public/simulations/wave-interference.html#L536)) and resized every frame
([:658](../../public/simulations/wave-interference.html#L658), [:762](../../public/simulations/wave-interference.html#L762)).

**Arrays** (Float64Array, written every frame):

| Name | Dims | Declared | Written | Meaning |
|---|---|---|---|---|
| `A`, `f`, `phi`, `s` | wave | [511-514](../../public/simulations/wave-interference.html#L511-L514) | [663](../../public/simulations/wave-interference.html#L663) | the card values |
| `k`, `omega`, `lam`, `v`, `nu` | wave | [515-519](../../public/simulations/wave-interference.html#L515-L519) | [664](../../public/simulations/wave-interference.html#L664) | rad/px, rad/s, px, px/s, Hz |
| `y_400` | wave | [520](../../public/simulations/wave-interference.html#L520) | [665](../../public/simulations/wave-interference.html#L665) | each wave at X = 400 px |
| `X` (coordinate) | x | [531](../../public/simulations/wave-interference.html#L531) | [699](../../public/simulations/wave-interference.html#L699) | sample positions, px |
| `y_comp`, `py_comp` | wave × x | [532](../../public/simulations/wave-interference.html#L532), [534](../../public/simulations/wave-interference.html#L534) | [685](../../public/simulations/wave-interference.html#L685) | each wave at each sample, px; its screen height, css px |
| `y_sum`, `py_sum` | x | [533](../../public/simulations/wave-interference.html#L533), [535](../../public/simulations/wave-interference.html#L535) | [699](../../public/simulations/wave-interference.html#L699) | the sum, px; its screen height, css px |
| `nu_line`, `A_line`, `x_line`, `y_line` | line | [537-541](../../public/simulations/wave-interference.html#L537-L541) | [767](../../public/simulations/wave-interference.html#L767) | stem frequency (Hz), height (px), screen position (css px) |

`wave × x` arrays are row-major, one row per wave: sample $j$ of wave $i$ is at index $i(M+1) + j$
([:685](../../public/simulations/wave-interference.html#L685)).

**Scalars.**

| Written in | Line | Variables |
|---|---|---|
| `render()` (on add, remove, preset) | [617](../../public/simulations/wave-interference.html#L617) | `N` |
| `draw()` | [667](../../public/simulations/wave-interference.html#L667) | `sum_A` = Σ Aᵢ in px, the largest possible sum (declared at [521](../../public/simulations/wave-interference.html#L521)). The `r-sum` readout shows it ([830](../../public/simulations/wave-interference.html#L830)) and `ratio` divides by it ([721](../../public/simulations/wave-interference.html#L721)); neither adds the amplitudes again. |
| `draw()` | [667-671](../../public/simulations/wave-interference.html#L667-L671) | `M`, `dX`, `R`, `Rc`, `y_sum_400`, `y1_400`, `bl`, `venv`, `box_w`, `box_h`, `right`, `hSum`, `top2`, `hComp` |
| `draw()` | [676](../../public/simulations/wave-interference.html#L676), [721](../../public/simulations/wave-interference.html#L721) | `mid1`, `mid2`; `peak`, `ratio` |
| `drawSpectrum()` | [764](../../public/simulations/wave-interference.html#L764) | `amax`, `spec_w`, `spec_h` |
| clock callback | [826](../../public/simulations/wave-interference.html#L826) | `t`, `dt`, `fps`, `frames`, `playing` |

Declarations are at [:508-509](../../public/simulations/wave-interference.html#L508-L509),
[:521-529](../../public/simulations/wave-interference.html#L521-L529) and
[:539-557](../../public/simulations/wave-interference.html#L539-L557). `bl` and `venv` are `NaN` unless there are two waves
with $f_1 \ne f_2$.

**One round** (`Sim.data.round`, [:961-962](../../public/simulations/wave-interference.html#L961-L962)): the time variable is
`t`; the length is `benchRound()`, the time after which the pattern at a fixed point repeats, $1/\gcd(\nu_i)$ with the $\nu_i$
retained at their stored 10⁻⁶ Hz precision, capped at 20 s ([:862-867](../../public/simulations/wave-interference.html#L862-L867)). For the Square
wave preset it is 2.50 s (measured). The chart columns are `sum_A`, `peak`, `ratio`, `y_sum_400`, `y1_400`; the point followed
is the sum at the middle sample, unless the reader pinned another. The panel samples every numeric scalar at most 600 times
in the round ([datalog.js:744](../../public/scripts/datalog.js#L744), [datalog.js:773](../../public/scripts/datalog.js#L773)).

**The panel hooks.** `Sim.data` ([:868-965](../../public/simulations/wave-interference.html#L868-L965)) sets
`kicker: 'Fig. 6 · data'`, `file: 'fig6-wave-bench'`, six groups (Waves, The sum, Time, Sampled curves, Spectrum, Drawing),
the checks, the read-backs and the `about` paragraph. The contract is at
[datalog.js:8-30](../../public/scripts/datalog.js#L8-L30). Read values works on the plot only: datalog.js attaches it to the
element `#stage` ([datalog.js:542](../../public/scripts/datalog.js#L542)), which is the plot; the spectrum's stems are checked
from the table, with the `y_line` read-back.

**`Sim.live()`** ([:797-821](../../public/simulations/wave-interference.html#L797-L821)) reads only the store and returns, for
the walkthrough's "Now" column: `N`, `sum` (y at X = 400), `pk`, `sA`, `ratio`, `M`, `dX`, `R`, `Rc`, `An` and `fn` (all
amplitudes and frequencies), `fmax`; for wave 1 `A`, `f`, `s`, `phi` (in units of π), `k`, `w` (ω), `lam`, `v`, `y1`, `hl`
(ν₁); and `bl`, `venv`, or "needs two waves with different f". With no waves the per-wave keys read "no waves". The walkthrough
polls it every 200 ms ([sim.js:314-326](../../public/scripts/sim.js#L314-L326)).

**Three-way check, measured.** Square wave preset, paused, 1440 × 900 window, sample 356 (X = 400.0 px): stored `y_sum` =
23.816154399757014 px and the value recomputed by `check.y_sum` from the stored `y_comp` are identical; stored `py_sum` =
96.36117283084565 css px equals its recomputation from `mid1`, `R`, `hSum`; the pixel read back at (400.0, 96.4) css px is
rgb(28, 21, 24), the ink `#1c1518` of the sum stroke ([sim.js:10](../../public/scripts/sim.js#L10)). `y_comp` of wave 1 at the
same sample is identical to `yAt`.

**Read-back with no waves.** With an empty bench nothing is drawn in the top panel but its grid and the faint zero line, and
`py_sum` holds the height of that line (`mid1`). The read-back then returns `ok: null` with "no sum curve: the bench has no
waves" ([:948](../../public/simulations/wave-interference.html#L948)), and the panel shows the neutral verdict "Not in the picture at the moment, so there is nothing to
read back." ([datalog.js:529](../../public/scripts/datalog.js#L529)). Before, it read the pixel on the zero line, drawn in
rgba(90, 80, 75, 0.45) ([:640](../../public/simulations/wave-interference.html#L640)); that pixel is dark enough for the luminance test, so the check passed on a line that
is not the sum curve.

## Page structure

**Head** ([:3-27](../../public/simulations/wave-interference.html#L3-L27)): title, description, theme colour; preconnects to
Google Fonts; `../styles/sim.css`, `../styles/data.css`, `../styles/fold.css`; an inline SVG favicon; and a page-specific
`<style>` for the wave cards: `.waves`, `.wave` with a left border in the wave's colour `--c`, `.wave__head`, `.wave__x`,
`.wave__ctl` (two columns of sliders), `.empty` ([:15-26](../../public/simulations/wave-interference.html#L15-L26)). See
[styles.md](../styles.md).

**Body.**

- Top bar with the catalog link and the Fig. 1–10 links, Fig. 6 marked `aria-current`
  ([:29-44](../../public/simulations/wave-interference.html#L29-L44)).
- Heading: "Fig. 6 · superposition · Fourier analysis", the h1 and the lede
  ([:48-52](../../public/simulations/wave-interference.html#L48-L52)).
- Two figures stacked in `.stack` ([:55-74](../../public/simulations/wave-interference.html#L55-L74)): the plot `#stage`
  (aspect 16 / 10, or 1 / 1.1 below 900 px viewport width), canvas `#plot`, caption with the formula and the wave count
  `#cap-n`; the spectrum `#stage-spec` (16 / 4.2, or 16 / 7), canvas `#spec`, caption "ν from 0 to 6 Hz". The narrow-screen
  ratio is applied by [sim.css:215](../../public/styles/sim.css#L215).
- The control panel: Run, Presets, the cards container `#waves`, readouts `#r-n`, `#r-sum`, `#r-peak`
  ([:76-101](../../public/simulations/wave-interference.html#L76-L101)).
- The lecture note `<article class="paper" id="paper">` ([:104-479](../../public/simulations/wave-interference.html#L104-L479)),
  "Adding waves: beats, square waves and the spectrum". Nine sections, 20 numbered equations (1)–(20), four inline SVG
  figures, one theorem box, two exercises, one table and two "Checked by" notes:

| § | id | Title | Line | Contents |
|---|---|---|---|---|
| 01 | `p-sound` | Many sounds, one eardrum | [127](../../public/simulations/wave-interference.html#L127) | the everyday picture |
| 02 | `p-model` | The model | [136](../../public/simulations/wave-interference.html#L136) | eqs. (1)–(2); Figure 1, one component ([149-185](../../public/simulations/wave-interference.html#L149-L185)) |
| 03 | `p-super` | Waves simply add | [188](../../public/simulations/wave-interference.html#L188) | eqs. (3)–(6); phasors; Figure 2 ([202-241](../../public/simulations/wave-interference.html#L202-L241)) |
| 04 | `p-beat` | Beats | [244](../../public/simulations/wave-interference.html#L244) | eqs. (7)–(9); Figure 3, the Beats preset at X = 400 px ([252-301](../../public/simulations/wave-interference.html#L252-L301)); 4.1 envelope speed ★; Exercise 4.1 ([306](../../public/simulations/wave-interference.html#L306)) |
| 05 | `p-fourier` | A square wave from sines | [312](../../public/simulations/wave-interference.html#L312) | eqs. (10)–(16); box Fourier's theorem ([320](../../public/simulations/wave-interference.html#L320)); Figure 4, partial sums ([325-390](../../public/simulations/wave-interference.html#L325-L390)); 5.1 Fourier coefficients ★; 5.2 Gibbs overshoot ★ with its table ([406](../../public/simulations/wave-interference.html#L406)) |
| 06 | `p-spectrum` | The spectrum | [419](../../public/simulations/wave-interference.html#L419) | eqs. (17)–(19); Parseval; Exercise 6.1 ([433](../../public/simulations/wave-interference.html#L433)) |
| 07 | `p-numerics` | Computing the curves | [439](../../public/simulations/wave-interference.html#L439) | the per-frame computation, sample counts, chord error |
| 08 | `p-screen` | From the medium to the screen | [451](../../public/simulations/wave-interference.html#L451) | eq. (20), the screen mapping and the spectrum axis |
| 09 | `p-limits` | What the model leaves out | [460](../../public/simulations/wave-interference.html#L460) | nonlinearity, real dispersion, finite listening time; further reading ([469](../../public/simulations/wave-interference.html#L469)) |

- The walkthrough host `<section class="walk" id="walk" data-walk="bench">`
  ([:481](../../public/simulations/wave-interference.html#L481)), filled by `sim.js` from `../scripts/walk/bench.js`
  ([sim.js:402-411](../../public/scripts/sim.js#L402-L411)); see [walk.md](../scripts/walk.md). Eight steps: one component and
  its sliders; sampling the view; superposition as a plain sum; fitting the curves into their panels; the Beats preset; the
  Square wave preset; the spectrum; the bound $|\sum y_i| \le \sum A_i$ ([bench.js:7-123](../../public/scripts/walk/bench.js#L7-L123)).
- Footer, then the scripts in load order: `fold.js`, `sim.js`, `dataset.js`, the inline script, `datalog.js`
  ([:489-492](../../public/simulations/wave-interference.html#L489-L492), [:974](../../public/simulations/wave-interference.html#L974)).
  See [fold.md](../scripts/fold.md) and [sim.md](../scripts/sim.md).

## Where the drawing and the store differ

- **Straight segments.** The curves join the $M + 1$ stored points with straight lines, one per css px column, and the canvas
  smooths the strokes (the page's `about`, [:964](../../public/simulations/wave-interference.html#L964)). A chord cuts under a
  crest by about $A k^2 \Delta X^2 / 8$: 0.06 px in a wide window and 0.32 px on a phone for the shortest wave at full
  amplitude, so the peak readout can fall slightly short of the true crest (note Section 07,
  [:448](../../public/simulations/wave-interference.html#L448)).
- **Readouts lag and round.** The readouts are rewritten every 8th frame and show one decimal; the store is rewritten every
  frame at full precision ([:829-832](../../public/simulations/wave-interference.html#L829-L832),
  [:964](../../public/simulations/wave-interference.html#L964)).
- **Amplitude slider rounds.** The Amplitude slider moves in whole px, so the Square preset's 4.3 px shows as 4 px on its card,
  while the wave, Σ A = 50.3 px and the store keep 4.3 px (note Section 08,
  [:457](../../public/simulations/wave-interference.html#L457); measured: the card's slider reads 4).
- **The spectrum is not measured from the curve.** It is computed from the card values at $X = 0$ (note Section 09,
  [:466](../../public/simulations/wave-interference.html#L466)); stems of several waves are drawn in ink, others in the wave's
  colour ([:737](../../public/simulations/wave-interference.html#L737)).
- **Unequal scales.** Each panel has its own vertical range, and vertical and horizontal pixels differ: for the Square preset
  in a wide window 1 px of displacement is drawn 1.83 css px tall, 1 px along the medium 0.89 css px wide (note Section 08,
  [:455](../../public/simulations/wave-interference.html#L455)).
- **Overlapping curves.** Where two component curves cross, the one drawn last covers the other
  ([:949](../../public/simulations/wave-interference.html#L949)).

## How to change it safely

- **Layout numbers are repeated.** `left = 44` appears in `draw()` ([:652](../../public/simulations/wave-interference.html#L652)),
  `drawSpectrum()` ([:741](../../public/simulations/wave-interference.html#L741)) and as `LEFT` for the hooks
  ([:837](../../public/simulations/wave-interference.html#L837)); the margins 14, 30, 44, the share 0.56, the spectrum's
  `base = h - 24`, top 14 and minimum scale 40 appear in the code, in the `formula` strings
  ([:528-553](../../public/simulations/wave-interference.html#L528-L553)), in the store attributes
  ([:507](../../public/simulations/wave-interference.html#L507)), in the checks
  ([:925-944](../../public/simulations/wave-interference.html#L925-L944)) and in note Sections 07–08. Change them together.
- **The wave formula exists twice on purpose.** `y()` draws ([:622](../../public/simulations/wave-interference.html#L622));
  `yAt()` recomputes from stored inputs for the checks ([:847](../../public/simulations/wave-interference.html#L847)). The same
  holds for `nice`/`niceOf` and `lines`/`linesNow`. A change to the model must go into both, into the `formula` strings
  ([:520](../../public/simulations/wave-interference.html#L520), [:532](../../public/simulations/wave-interference.html#L532)),
  into note eq. (1) and into walkthrough step 1.
- **The ν rounding** to $10^{-6}$ Hz appears in `draw()` ([:664](../../public/simulations/wave-interference.html#L664)),
  `lines()` ([:730](../../public/simulations/wave-interference.html#L730)) and `check.nu`
  ([:916](../../public/simulations/wave-interference.html#L916)); if they differ, the stems and the check disagree.
- **Ranges are linked.** `NUMAX = 6` is `FMAX` × the top Speed 2; raising either slider's top needs a new `NUMAX`, a new
  spectrum caption ([:71](../../public/simulations/wave-interference.html#L71)) and note Section 08. `MAX_WAVES` matches the six
  `COLOURS` and the note's "up to six waves" ([:133](../../public/simulations/wave-interference.html#L133)).
- **Preset values are quoted** by the note (Beats at [:251](../../public/simulations/wave-interference.html#L251), Square wave at
  [:315](../../public/simulations/wave-interference.html#L315), the peaks 27.9, 28.0 and 41.7 px of Exercise 6.1) and by
  walkthrough steps 5–6. Recompute them if a preset changes.
- **Walkthrough excerpts.** `bench.js` quotes these page lines: 622, 624, 654, 655, 656, 684, 695-698, 727, 729, 730, 734
  (abridged with "..."), 739, 787, 789, 827 and 828 (checked by script). Keep them identical or edit `bench.js` in the same
  change; insert new store writes after a quoted line, never inside a quoted group ([AGENTS.md](../../AGENTS.md)).
- **Write where you compute** and declare a `check` that uses stored inputs only, as for Fig. 5; `Sim.live` must only read.
- **Re-test** in a real browser: load Square wave in a 1440 × 900 window and confirm $M$ = 712, $R$ = 60 px, `hSum` = 220.08,
  peak 27.91 px and a round of 2.50 s; pause and check `y_sum`, `py_sum` and `y_comp` at the middle sample (stored, recomputed
  and read back should agree); load Beats, set Wave 2's Speed to 0.50 and confirm $v_\text{env}$ = −300 px/s (Exercise 4.1);
  remove every wave and add one again; step through the eight walkthrough steps.

## Notes for maintainers

1. Fixed on 2026-10-15: an empty bench rewrites X, y_sum = 0 and py_sum = mid1 instead of retaining the preceding curve (commit [9d3175f](https://github.com/Numa1997/SiteTest/commit/9d3175f2cf50d0ad3f8792f1ee173e8ce56bab53)).
2. Fixed on 2026-10-15: the repeat uses every stored ν digit; ν = (1, 0.9975) Hz gives the 20 s cap (commit [9d3175f](https://github.com/Numa1997/SiteTest/commit/9d3175f2cf50d0ad3f8792f1ee173e8ce56bab53)).
3. Fixed on 2026-10-15: the note describes the current 0–6 Hz caption (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
4. Fixed on 2026-10-15: the Beats and Square excerpts preserve their source line layout (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
5. Fixed on 2026-10-15: the amplitude readout reads sum_A (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
6. Fixed on 2026-10-15: component readback checks alpha and the wave colour, accepting other colours only at stored crossings; white now fails (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
7. Fixed on 2026-10-15: frames is incremented before storage (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
8. Fixed on 2026-10-15: the Square preset stores 0.4, 1.2, 2 and 2.8 without extra decimal tails (commit [ce3bfc4](https://github.com/Numa1997/SiteTest/commit/ce3bfc439ce40b3e8b6bd7f59af2af9404bd4997)).
9. Fixed on 2026-10-15: with no waves, `drawn.py_sum` returns `ok: null` ("no sum curve: the bench has no waves",
   [:948](../../public/simulations/wave-interference.html#L948)) and the panel shows "not in the picture" instead of passing on the faint zero line (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).


## Teaching revision · 15 October 2026

Parseval and the 95% value measure mean-square displacement. String energy also weights each squared amplitude by frequency squared. The note qualifies envelope motion versus physical energy or information transport. Simulation code, inline styles and figure SVGs match the latest live baseline. See the [theory audit](../research-theory-audit.md).
