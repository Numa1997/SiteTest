# public/scripts/curve.js

| | |
|---|---|
| File | [public/scripts/curve.js](../../public/scripts/curve.js), 603 lines  46.9 kB (46 930 bytes) |
| Loaded by | the simulation pages that have a parameter curve, right after `dataset.js` on the same line: Fig. 1 (line 508), Fig. 2 (`Double Pendulum.html`, 453), Fig. 3 (`Interactive Double-Slit Experiment Visualization.html`, 549), Fig. 4 (`Transverse and longitudinal waves.html`, 735), Fig. 5 (`water-wave.html`, 567), Fig. 6 (`wave-interference.html`, 492), Fig. 7 (`phasor-sums.html`, 663), Fig. 8 (`draw-decompose.html`, 621), Fig. 9 (`driven-oscillator.html`, 601), Fig. 10 (`wind-turbine.html`, 550), Fig. 11 (`pendulum-control.html`, 421): all eleven; and their German and Arabic pages |
| Defines | `Sim.curve(opts)` on `window.Sim` ([curve.js:154](../../public/scripts/curve.js#L154)); `Sim.curve.value`, `Sim.curve.fn`, `Sim.curve.loosen` ([curve.js:600-602](../../public/scripts/curve.js#L600-L602)) |
| Uses | `Sim.theme`, `Sim.fmt`, `Sim.canvas2d`, `Sim.onResize`, `Sim.readPixel`, `Sim.isBurgundy` ([sim.md](sim.md)); the page's dataset ([dataset.md](dataset.md)); `_t()` for every word |
| Since | 30 October 2026, on Numa's request: "a curve to change the parameters and watch the animation unfold as the parameter changes", with an option for one's own curve and well-known example curves |

`curve.js` gives a simulation a knob that turns by itself. The reader picks a curve p(t) and one of the page's sliders;
while the simulation plays, the slider follows the curve exactly as if a hand moved it. The page hears an ordinary `input`
event and answers as it always does, so nothing in the page's physics changes. The curve's time runs on the page's own
clock: it advances by the same Δt as the simulation and stops when the page is paused. A hand on the slider stops the curve.

## The picture

A record player's tone arm, but for a knob: a cam (the curve) turns under a follower (the slider), and whatever the
follower is linked to (the wavelength, the damping) moves with it. The chart in the panel is the cam drawn flat: time
across, the knob's value up, a burgundy dot where the follower is now.

## What the reader sees

A group in the control panel, after the page's own sliders (on Fig. 1 after "Waves"), labelled "Curve · a knob that moves
by itself" ([curve.js:309-324](../../public/scripts/curve.js#L309-L324)):

- **Curve**: a list in two parts, the page's own examples first (each with the symbol of the knob it moves), then the
  shapes for any knob, then "Your own curve" ([curve.js:330-345](../../public/scripts/curve.js#L330-L345)).
- **Knob it moves**: the slider the curve drives. An example sets it; for a shape the reader chooses.
- Why this curve: its first sentence, with the rest folded behind it (a `<details>` the reader opens), and the formula in
  burgundy mono (`.curve__f`) always shown. Folding kept the chart near the top: the group on Fig. 1 went from 726 to
  576 px high at 1440 px wide.
- **The chart**: a white plate 132 px high. The curve is drawn from the stored samples `cv_pq`, the dot every frame
  ([curve.js:432-466](../../public/scripts/curve.js#L432-L466)).
- **From a, To b, Time T**: number boxes kept inside the slider's range, T between 1 and 600 s; **Repeat**.
- **Play curve** / **Stop**, and a status line rewritten at most four times a second, like the data panel's: the knob's
  value, the time of the run, and one fact from the page (on Fig. 1, the number of calm lines)
  ([curve.js:412-426](../../public/scripts/curve.js#L412-L426)).

Play curve sets the knob to p(0) at once and starts the page's clock if it was paused
([curve.js:246-264](../../public/scripts/curve.js#L246-L264)). At the end of a run the knob stays at p(T), or the run
starts again with Repeat. Changing the curve or the knob stops a run; editing your own points, a, b or T while it runs
does not.

## Options a page can give

- A knob's `format(v)` shows its value in the page's own way: Fig. 2's mass slider is on a log scale, ln(m₂/m₁), and shows
  the ratio (1/9.97 … 9.97) in the status line and on the chart.
- A knob's `live(v)` is called instead of the page's `input` handler, for a value the page can change while it runs when a
  hand on the slider would restart the motion (Fig. 2's mass: [fig02-double-pendulum.md](../simulations/fig02-double-pendulum.md)).
  The slider is still moved and painted; a hand on it still restarts the page and stops the curve.
- An example's `set: { id: value }` puts other sliders to those values when the run starts, through their own `input`
  handlers (Fig. 3's examples fix b, d, λ or α first, so that the numbers in their explanations hold); for a checkbox it
  ticks (true) or clears (false) it and fires `change`.
- An example's `press: [selector, …]` clicks those buttons first, before `set`: Figs. 6, 7 and 8 press their presets.
- A knob's `slider` need not come from `Sim.slider`: any object with `el` (`min`, `max`, `step`, `value`, `dispatchEvent`,
  `addEventListener`, and `node()`, which returns the input as it is now), `value`, `set(v)` and `paint()` will do. Figs. 6
  and 7 wrap the sliders of a card that is rebuilt at every preset (`w2knob`, `c2knob`).
- A knob's `steps: true` keeps it on the slider's own steps (below).

## The shapes

u = t/T is the fraction of the run done, a the value at the start, b at the end ([curve.js:62-89](../../public/scripts/curve.js#L62-L89)).

| Key | Name | p(u) | Source and check |
|---|---|---|---|
| `line` | Straight ramp | a + (b − a) u | — |
| `jerk` | Smooth S-curve (minimum jerk) | a + (b − a)(10u³ − 15u⁴ + 6u⁵) | T. Flash and N. Hogan, J. Neurosci. 5 (1985) 1688–1703: their minimum-jerk solution x = x₀ + (x₀ − x_f)(15τ⁴ − 6τ⁵ − 10τ³), read from the paper's PDF through Firecrawl (the journal refuses plain fetches). Same polynomial, checked in Wolfram; zero rate and acceleration at both ends; sixth derivative zero (the Euler–Lagrange condition of least integrated squared jerk); peak rate 15/8 of the mean, at u = ½. |
| `exp` | Exponential sweep | a (b/a)^u, a and b of one sign | A. Farina, "Impulse response measurements", 23rd Nordic Sound Symposium, Bolkesjø, 2007, eq. (18), read in the PDF from angelofarina.it: s(t) = sin[ω₁T/ln(ω₂/ω₁) · (e^{(t/T) ln(ω₂/ω₁)} − 1)]. Its instantaneous frequency, the time derivative of the phase, is ω₁ (ω₂/ω₁)^{t/T} (Wolfram). Farina's AES paper 5093 (2000) is only listed here, not read: the download timed out. |
| `inv` | Steady in 1/p | 1 / (1/a + (1/b − 1/a) u) | 1/p linear in u (Wolfram). Not offered as a shape for any knob; a page uses it in an example. |
| `tri` | There and back | a + (b − a)(1 − \|2u − 1\|) | — |
| `swell` | Swell and return | a + (b − a)(1 − cos 2πu)/2 | — |
| `own` | Your own curve | monotone cubic Hermite through the reader's points | Method of F. N. Fritsch and R. E. Carlson, SIAM J. Numer. Anal. 17 (1980) 238–246, implemented from the step-by-step statement in Wikipedia's "Monotone cubic interpolation" and checked against the SLATEC routine PCHIM's documentation (NIST GAMS), which cites the paper. The paper itself is behind SIAM's paywall and was not read. |

**Your own curve** ([curve.js:94-118](../../public/scripts/curve.js#L94-L118), [360-364](../../public/scripts/curve.js#L360-L364), [471-532](../../public/scripts/curve.js#L471-L532)).
Choosing it, or clicking or dragging on the chart of any other curve, turns the curve on screen into five points
(u = 0, ¼, ½, ¾, 1) that the reader edits. A click adds a point, a drag moves it, a double-click removes it; the first and
last points move only up and down; keys ← → choose a point, ↑ ↓ move it by 1 % of the range (10 % with Shift), Delete
removes it. The slopes at the points are Fritsch–Carlson's: the mean of the two neighbouring secants, zero where the data
turn, and each pair (α, β) = (m_k, m_{k+1})/δ_k pulled back inside the circle α² + β² ≤ 9. Each piece is then the cubic
Hermite polynomial with h₀₀ = 2s³ − 3s² + 1, h₁₀ = s³ − 2s² + s, h₀₁ = −2s³ + 3s², h₁₁ = s³ − s² (the four end conditions
checked in Wolfram). Every piece is monotone, so the curve never leaves the range of its two neighbouring points and the knob
never leaves the range the reader set. Tested on 17 117 random point sets: no overshoot, every point passed through exactly,
every piece monotone (scratch test `curvetest.js`, run with Node on the functions copied from the file).

## Exact values on the slider · 30 October 2026

The slider takes the curve's exact value, not the nearest of its steps (Numa, 30 October 2026: "we need them to look good,
and we need them to be real"). Until then `snap()` put every value on the slider's steps, so a knob with coarse steps moved
in visible jumps: 25 of the 33 continuous knobs of the eleven pages stepped 1.9–11.2 px at a time (step × 280 px / range,
from each slider's range and step read in Chromium), and on Figs. 9–11 the slider showed the solver's value only to half a
step.

Now `apply()` ([curve.js:234-245](../../public/scripts/curve.js#L234-L245)) calls `loosen()` ([curve.js:138-152](../../public/scripts/curve.js#L138-L152)): the slider's step becomes `any`, its own step is kept in
`data-cv-step`, and the value set is p(u) itself, kept inside the slider's range (`inside()`). The first hand on the slider
(a press, or a key that moves it: arrows, Page Up and Down, Home, End) puts the step back and, if that moves the value onto
a step, fires `input`, so the page hears where the slider now stands; a hand still stops a running curve. `cv_set` is the
slider's value read back after it is set, so the store, the slider and the simulation agree exactly. Measured in headless
Chromium on every frame of a 4 s straight ramp, on every knob of the eleven pages (scratch test `smooth.js`):
|`cv_set` − p| ≤ 3.4 × 10⁻¹³ on every continuous knob (the round trip of a double through the input's text), the
slider's read-back passed on every frame, and the thumb moved on every frame by the curve's own rate, 1.4–2.1 px at the
test's frame rate. A second test (`handtest.js`) left λ at 50.123 px (Fig. 1), f₂ at 1.637 Hz (Fig. 6) and v at
9.876 m/s (Fig. 10): an arrow key put each back on its steps (50.2 px, 1.70 Hz, 10.0 m/s), the page heard it, and on
Fig. 10 the running curve stopped.

A knob marked `steps: true` keeps to the slider's steps through `snap()` ([curve.js:128-133](../../public/scripts/curve.js#L128-L133)), which counts the steps from the
minimum and writes the value with as many decimals as the step has (16 + 397 · 0.1 is stored as 55.7): the counts (Fig. 4's
particles, Fig. 5's layers and parcels per layer, Fig. 8's circles K), which really move in whole steps, and Fig. 7's ω₂,
whose period and symmetry are computed from 100 ω as an integer ([fig07-phasor-sums.md](../simulations/fig07-phasor-sums.md));
its steps are 0.04 px apart on the slider. Measured the same way, ω₂ stays within 0.003 rad/s of p(u) and moves on every
frame.

`Sim.curve.loosen(el)` does the same for a slider a page moves by code with an exact value: Fig. 5's Frequency slider under
deep-water dispersion, and the Phase sliders that keep Wave 2 (Fig. 6) and Circle 2 (Fig. 7) continuous. Seven slider
labels printed the raw value (`v + ' px'`), which under a curve read like "36.1039222 px"; they now round to the slider's
own resolution (Figs. 1, 3, 4, 5, 6 and 8; the walkthroughs that quote those lines were updated, and still find the same
754 of 759 lines). The "Done" message no longer doubles the units of a knob that formats its own value ("1.64 Hz Hz").

## What it writes into the store

Declared in `declare()` ([curve.js:167-187](../../public/scripts/curve.js#L167-L187)), re-declared with the knob's units when
the knob changes (re-declaring keeps the data: [dataset.js:45-56](../../public/scripts/dataset.js#L45-L56)).

| Name | Shape | Meaning | Written in |
|---|---|---|---|
| `cv_on`, `cv_knob`, `cv_name`, `cv_formula`, `cv_loop` | scalars | whether a run is on, the knob, the curve, its formula, Repeat | `begin()`, `end()`, `resample()` |
| `cv_a`, `cv_b`, `cv_T` | scalars | value at u = 0, at u = 1 (at the turn for There and back and Swell), duration in s | `resample()` |
| `cv_t`, `cv_u`, `cv_p`, `cv_set`, `cv_runs` | scalars | time of the run on the page clock, u = t/T, the curve's value, the slider's value, runs finished | `step()` ([curve.js:274-291](../../public/scripts/curve.js#L274-L291)), `apply()` ([curve.js:234-245](../../public/scripts/curve.js#L234-L245)) |
| `cv_tq`, `cv_pq` | over `cq` (201) | the curve sampled for its chart, t = qT/200 | `resample()` ([curve.js:205-215](../../public/scripts/curve.js#L205-L215)) |
| `cv_ku`, `cv_kp`, `cv_km` | over `ck` (number of points) | your points and the Fritsch–Carlson slopes at them | `storePoints()` ([curve.js:196-204](../../public/scripts/curve.js#L196-L204)) |

The chart draws only from `cv_tq`, `cv_pq`, `cv_u` and `cv_p`.

## The data panel

`curve.extend(Sim.data)` ([curve.js:556-585](../../public/scripts/curve.js#L556-L585)) adds:

- a group (and, on a page with a ledger, a section) "Parameter curve" with all eighteen variables;
- **Check** for `cv_u` (t/T), `cv_p` (the shape's formula from the stored a, b and u, or Fritsch–Carlson again from the
  stored points), `cv_set` (p kept inside the slider's range, or on a knob with `steps` the snapping formula from the stored p and the slider's min and step), `cv_tq`, `cv_pq` (each
  sample recomputed) and `cv_km` (the slopes recomputed from the stored points);
- **read-backs** for `cv_p` (the chart's pixel at the dot must be burgundy, alpha first, through `Sim.readPixel`) and
  `cv_set` (the slider's position must equal the stored value).

`curve.round(spec)` ([curve.js:586-595](../../public/scripts/curve.js#L586-L595)) wraps the page's round: while a curve
runs, one recorded round is the rest of the run (length T − t, its label names the curve and its ends), and the recorded
columns gain `cv_p` and `cv_set`. Record pressed during a run therefore catches the parameter and the page's response side by
side. Otherwise the round is the page's own.

## Words

Every word goes through `_t()`. `tools/i18n/build.py` collects them from this file (its `SCRIPTS` list, and its rule for
the data panel's `long_name` words), so `--check` fails until German and Arabic exist. The 93 strings of 30 October 2026
(engine and Fig. 1) are in `i18n/de/strings.json` and `i18n/ar/strings.json`; terms follow [../glossary.md](../glossary.md)
and the Fig. 1 note (ruhige Linien / الخطوط الهادئة, Regler / المنزلق, Speicher / المخزن).

## How it was tested (30 October 2026)

- Wolfram Language: the Farina derivative, the Flash–Hogan polynomial, the Hermite basis, the 1/p form.
- Node: 17 117 random own-curve point sets; the shapes at their ends and midpoints.
- jsdom 24.1.3 (installed in the session's scratchpad, not in the repository) with Fig. 1's real scripts and a canvas that
  draws nothing: 36 checks pass, among them p(t) against its formula, slider = store = simulation, every new Check against
  the store, a hand stopping the curve, the round becoming the rest of the run, a click adding a point; the German and
  Arabic pages show no English in the tool and no page errors.
- Headless Chromium (allowed by Numa later on 30 October 2026), Figs. 1–3 at 1440 × 900 and Figs. 1 and 3 (Arabic) at
  390 × 844: no page errors, the curve's checks `cv_u`, `cv_p`, `cv_set` agree with the store, the chart's dot reads back
  burgundy rgb(122, 31, 43), the slider shows the stored value, no sideways scroll. The screenshots showed two faults, now
  fixed: the explanations pushed the chart down (now folded), and in Arabic the status line was reordered by the
  right-to-left layout. The status line is now kept left to right like the readouts (`styles/i18n.css`, a rule in `sim.css`
  would have been flipped by rtlcss), and the Arabic strings for "of", "at" and "run" carry left-to-right marks so the
  numbers keep their places. Script: `curvecheck.js` in the session's scratchpad.

## Pages that solve first (Figs. 9, 10 and 11)

These pages never integrate while the reader watches, so a curve cannot move their sliders frame by frame. Play curve
hands the whole curve to the page instead, frozen at that moment, and the page solves its run with it. The research for
the three pages proposed three hand-overs; the engine offers all three, built so that each page's own tests pass
unchanged ([curve.js header](../../public/scripts/curve.js), `described()`, `frozen()`, `resched()`, `playAt()`):

- `knob.schedule(fn, name)` (Figs. 9 and 11): `fn(t)` is the curve at run time t (a before the run, b after it, or the next
  run with Repeat) and carries its description as properties (knob, shape, name, a, b, T, loop, ku, kp, km; `fn.fn` is
  itself). Called at Play curve, again after an edit while it runs (one more solve), and with `(null, 'stop' | 'hand')`
  when Stop, a new curve or a hand on the slider ends it. The page decides what that means (Fig. 11: Stop re-solves from
  the state on screen; a hand marks the run stale).
- `opts.solve(sc)` and `opts.ended(msg)` (Fig. 10): `sc` is the same description as plain data (Fig. 10 stores and compares
  it as JSON; JSON of a function is nothing, which is why the two forms exist), with `curve.params()` and
  `curve.playAt(t)`, which shows the curve at the time of the frame on screen.
- `opts.time()` (Figs. 9 and 11): the run time of the stored sample on screen; the curve's time follows the playback, so a
  seek moves the dot too.
- On such a knob the slider shows the curve's exact value, the value the solver used, with no `input` event, so the run on
  screen is never marked stale by the curve. (Until the exact values above, the slider showed it on its steps, both ends of
  a `schedule` knob's curve were put on the steps, and `knob.min`/`knob.max` let Fig. 10's wind curve run past the
  slider's 11 m/s while the slider waited at its end. Numa: "We do things correctly or we don't do them": the wind slider
  now runs to 14 m/s and the curve's range is the slider's.)
- `opts.shapes` adds a page's own shapes (Fig. 11's step and input shapers); the engine itself now has `gust` and `rise`,
  the IEC 61400-1 operating gust and the half-cosine rise of its coherent gust, offered only through Fig. 10's examples.
- `curve.stop(msg)`, `curve.at(t)` (the curve read back from the store, for checks), `Sim.curve.value(sc, t)` and
  `Sim.curve.fn(sc)` (a frozen curve evaluated by a solver or a check).

Two faults surfaced while uniting them and are fixed: a function's own `name` is read-only, so the description is put on
`fn` with `Object.defineProperty`; and Fig. 10's identity test (its built-in gust against the curve gust, b = 9.11 m/s)
failed while both ends were snapped to the slider's 0.1 m/s steps; no end is snapped now.

