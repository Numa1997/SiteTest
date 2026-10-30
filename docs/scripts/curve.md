# public/scripts/curve.js

| | |
|---|---|
| File | [public/scripts/curve.js](../../public/scripts/curve.js), 491 lines, 36.1 kB (36 062 bytes) |
| Loaded by | Fig. 1 (`Circular Wave Interference Visualization.html`, line 508, right after `dataset.js`), and its German and Arabic pages; more figures follow one at a time |
| Defines | `Sim.curve(opts)` on `window.Sim` ([curve.js:98](../../public/scripts/curve.js#L98)) |
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
by itself" ([curve.js:203-224](../../public/scripts/curve.js#L203-L224)):

- **Curve**: a list in two parts, the page's own examples first (each with the symbol of the knob it moves), then the
  shapes for any knob, then "Your own curve" ([curve.js:228-243](../../public/scripts/curve.js#L228-L243)).
- **Knob it moves**: the slider the curve drives. An example sets it; for a shape the reader chooses.
- One paragraph on why this curve, with its formula in burgundy mono (`.curve__f`).
- **The chart**: a white plate 132 px high. The curve is drawn from the stored samples `cv_pq`, the dot every frame
  ([curve.js:326-360](../../public/scripts/curve.js#L326-L360)).
- **From a, To b, Time T**: number boxes kept inside the slider's range, T between 1 and 600 s; **Repeat**.
- **Play curve** / **Stop**, and a status line rewritten at most four times a second, like the data panel's: the knob's
  value, the time of the run, and one fact from the page (on Fig. 1, the number of calm lines)
  ([curve.js:307-320](../../public/scripts/curve.js#L307-L320)).

Play curve sets the knob to p(0) at once and starts the page's clock if it was paused
([curve.js:168-176](../../public/scripts/curve.js#L168-L176)). At the end of a run the knob stays at p(T), or the run
starts again with Repeat. Changing the curve or the knob stops a run; editing your own points, a, b or T while it runs
does not.

## The shapes

u = t/T is the fraction of the run done, a the value at the start, b at the end ([curve.js:38-59](../../public/scripts/curve.js#L38-L59)).

| Key | Name | p(u) | Source and check |
|---|---|---|---|
| `line` | Straight ramp | a + (b − a) u | — |
| `jerk` | Smooth S-curve (minimum jerk) | a + (b − a)(10u³ − 15u⁴ + 6u⁵) | T. Flash and N. Hogan, J. Neurosci. 5 (1985) 1688–1703: their minimum-jerk solution x = x₀ + (x₀ − x_f)(15τ⁴ − 6τ⁵ − 10τ³), read from the paper's PDF through Firecrawl (the journal refuses plain fetches). Same polynomial, checked in Wolfram; zero rate and acceleration at both ends; sixth derivative zero (the Euler–Lagrange condition of least integrated squared jerk); peak rate 15/8 of the mean, at u = ½. |
| `exp` | Exponential sweep | a (b/a)^u, a and b of one sign | A. Farina, "Impulse response measurements", 23rd Nordic Sound Symposium, Bolkesjø, 2007, eq. (18), read in the PDF from angelofarina.it: s(t) = sin[ω₁T/ln(ω₂/ω₁) · (e^{(t/T) ln(ω₂/ω₁)} − 1)]. Its instantaneous frequency, the time derivative of the phase, is ω₁ (ω₂/ω₁)^{t/T} (Wolfram). Farina's AES paper 5093 (2000) is only listed here, not read: the download timed out. |
| `inv` | Steady in 1/p | 1 / (1/a + (1/b − 1/a) u) | 1/p linear in u (Wolfram). Not offered as a shape for any knob; a page uses it in an example. |
| `tri` | There and back | a + (b − a)(1 − \|2u − 1\|) | — |
| `swell` | Swell and return | a + (b − a)(1 − cos 2πu)/2 | — |
| `own` | Your own curve | monotone cubic Hermite through the reader's points | Method of F. N. Fritsch and R. E. Carlson, SIAM J. Numer. Anal. 17 (1980) 238–246, implemented from the step-by-step statement in Wikipedia's "Monotone cubic interpolation" and checked against the SLATEC routine PCHIM's documentation (NIST GAMS), which cites the paper. The paper itself is behind SIAM's paywall and was not read. |

**Your own curve** ([curve.js:64-88](../../public/scripts/curve.js#L64-L88), [255-259](../../public/scripts/curve.js#L255-L259), [363-426](../../public/scripts/curve.js#L363-L426)).
Choosing it, or clicking or dragging on the chart of any other curve, turns the curve on screen into five points
(u = 0, ¼, ½, ¾, 1) that the reader edits. A click adds a point, a drag moves it, a double-click removes it; the first and
last points move only up and down; keys ← → choose a point, ↑ ↓ move it by 1 % of the range (10 % with Shift), Delete
removes it. The slopes at the points are Fritsch–Carlson's: the mean of the two neighbouring secants, zero where the data
turn, and each pair (α, β) = (m_k, m_{k+1})/δ_k pulled back inside the circle α² + β² ≤ 9. Each piece is then the cubic
Hermite polynomial with h₀₀ = 2s³ − 3s² + 1, h₁₀ = s³ − 2s² + s, h₀₁ = −2s³ + 3s², h₁₁ = s³ − s² (the four end conditions
checked in Wolfram). Every piece is monotone, so the curve never leaves the range of its two neighbouring points and the knob
never leaves the range the reader set. Tested on 17 117 random point sets: no overshoot, every point passed through exactly,
every piece monotone (scratch test `curvetest.js`, run with Node on the functions copied from the file).

## The knob's steps

A slider moves in steps. `snap()` ([curve.js:91-96](../../public/scripts/curve.js#L91-L96)) puts the curve's value on the
slider's steps counted from its minimum, inside its range, and writes it with as many decimals as the step has, so
16 + 397 · 0.1 is stored as 55.7. The slider is set to that value, so the store, the slider and the simulation agree
exactly in every browser (a test DOM that does not snap range inputs showed that leaving it to the browser does not). The
page's physics runs on this snapped value, `cv_set`; the curve's own value is `cv_p`.

## What it writes into the store

Declared in `declare()` ([curve.js:108-128](../../public/scripts/curve.js#L108-L128)), re-declared with the knob's units when
the knob changes (re-declaring keeps the data: [dataset.js:45-56](../../public/scripts/dataset.js#L45-L56)).

| Name | Shape | Meaning | Written in |
|---|---|---|---|
| `cv_on`, `cv_knob`, `cv_name`, `cv_formula`, `cv_loop` | scalars | whether a run is on, the knob, the curve, its formula, Repeat | `begin()`, `end()`, `resample()` |
| `cv_a`, `cv_b`, `cv_T` | scalars | value at u = 0, at u = 1 (at the turn for There and back and Swell), duration in s | `resample()` |
| `cv_t`, `cv_u`, `cv_p`, `cv_set`, `cv_runs` | scalars | time of the run on the page clock, u = t/T, the curve's value, the slider's value, runs finished | `step()` ([curve.js:183-200](../../public/scripts/curve.js#L183-L200)) |
| `cv_tq`, `cv_pq` | over `cq` (201) | the curve sampled for its chart, t = qT/200 | `resample()` ([curve.js:146-156](../../public/scripts/curve.js#L146-L156)) |
| `cv_ku`, `cv_kp`, `cv_km` | over `ck` (number of points) | your points and the Fritsch–Carlson slopes at them | `storePoints()` ([curve.js:137-145](../../public/scripts/curve.js#L137-L145)) |

The chart draws only from `cv_tq`, `cv_pq`, `cv_u` and `cv_p`.

## The data panel

`curve.extend(Sim.data)` ([curve.js:450-478](../../public/scripts/curve.js#L450-L478)) adds:

- a group (and, on a page with a ledger, a section) "Parameter curve" with all eighteen variables;
- **Check** for `cv_u` (t/T), `cv_p` (the shape's formula from the stored a, b and u, or Fritsch–Carlson again from the
  stored points), `cv_set` (the snapping formula from the stored p and the slider's min and step), `cv_tq`, `cv_pq` (each
  sample recomputed) and `cv_km` (the slopes recomputed from the stored points);
- **read-backs** for `cv_p` (the chart's pixel at the dot must be burgundy, alpha first, through `Sim.readPixel`) and
  `cv_set` (the slider's position must equal the stored value).

`curve.round(spec)` ([curve.js:479-488](../../public/scripts/curve.js#L479-L488)) wraps the page's round: while a curve
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
- **Not tested in a real browser.** The session's hook refused headless Chromium ("Browser automation detected", then
  "Opening a browser is almost never needed"). Pixels, layout, the read-back of the dot and the Arabic right-to-left
  layout of the status line are therefore unmeasured.
