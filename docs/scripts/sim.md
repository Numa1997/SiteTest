# public/scripts/sim.js

| | |
|---|---|
| File | [public/scripts/sim.js](../../public/scripts/sim.js), 505 lines, 24.6 kB (24 559 bytes) |
| Loaded by | the ten simulation pages in `public/simulations/`, as the second shared script, after `fold.js` and before `dataset.js` (table below). No other page loads it. |
| Defines | `window.Sim` ([sim.js:490](../../public/scripts/sim.js#L490)), a fresh object with 13 members |
| Reads | `window.WALK` ([sim.js:484](../../public/scripts/sim.js#L484)), `window.Fold` ([sim.js:402](../../public/scripts/sim.js#L402)), `window.Sim.live` ([sim.js:389](../../public/scripts/sim.js#L389)), `window.renderMathInElement` from KaTeX ([sim.js:429](../../public/scripts/sim.js#L429)) |
| Emits | the DOM event `typeset` on `document` ([sim.js:440](../../public/scripts/sim.js#L440), [sim.js:471](../../public/scripts/sim.js#L471)) |

`sim.js` is the toolbox every simulation page stands on. It gives the page a colour palette, canvases that stay sharp on
high-density screens, labels set like typeset mathematics, axis ticks, a pixel read-back for the data panel's Check,
styled sliders and a clock that can pause. When the page has finished loading it does three more things on its own: it
typesets the lecture note with KaTeX, it loads the page's walkthrough file and builds the "From symbols to code" section,
and it shows a visible error banner if any script on the page throws.

## Load order on the pages

Every simulation page loads the shared scripts at the end of `<body>`, in this order. The page's own inline script sits
between `dataset.js` and `datalog.js`.

| Fig. | Page | `fold.js` | `sim.js` | `dataset.js` | page script | `datalog.js` |
|---|---|---|---|---|---|---|
| 1 | [Circular Wave Interference Visualization.html](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L505) | L505 | L506 | L507 | L508 | L903 |
| 2 | [Double Pendulum.html](../../public/simulations/Double%20Pendulum.html#L389) | L389 | L390 | L391 | L392 | L841 |
| 3 | [Interactive Double-Slit Experiment Visualization.html](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L546) | L546 | L547 | L548 | L549 | L917 |
| 4 | [Transverse and longitudinal waves.html](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L731) | L731 | L732 | L733 | L734 | L1081 |
| 5 | [water-wave.html](../../public/simulations/water-wave.html#L563) | L563 | L564 | L565 | L566 | L885 |
| 6 | [wave-interference.html](../../public/simulations/wave-interference.html#L489) | L489 | L490 | L491 | L492 | L960 |
| 7 | [phasor-sums.html](../../public/simulations/phasor-sums.html#L659) | L659 | L660 | L661 | L662 | L1475 |
| 8 | [draw-decompose.html](../../public/simulations/draw-decompose.html#L617) | L617 | L618 | L619 | L620 | L1413 |
| 9 | [driven-oscillator.html](../../public/simulations/driven-oscillator.html#L462) | L462 | L463 | L464 | L465 | L1106 |
| 10 | [wind-turbine.html](../../public/simulations/wind-turbine.html#L547) | L547 | L548 | L549 | L550 | L1152 |

The scripts are plain `<script src>` tags at the end of the body, so they run while the document is still loading. That is
why `sim.js` defers its own start to `DOMContentLoaded` ([sim.js:487](../../public/scripts/sim.js#L487)), and why
`fold.js`, which registered its start first ([fold.js:411](../../public/scripts/fold.js#L411)), folds the lecture note
before `sim.js` typesets it.

## How it works

### When the file runs (synchronously, while the page loads)

1. It defines the palette `theme` ([sim.js:6-23](../../public/scripts/sim.js#L6-L23)): the site colours as hex strings and
   two canvas fonts, IBM Plex Mono for labels and italic Latin Modern Roman for symbols.
2. It finds the site root `ROOT` from its own address: the `src` of the running script with `scripts/sim.js` cut off
   ([sim.js:26-29](../../public/scripts/sim.js#L26-L29)). If the browser cannot say which script is running, it falls back to
   `'../'`. KaTeX is later loaded from this root.
3. It installs a `window` `error` listener that turns the first uncaught error into a banner
   ([sim.js:231](../../public/scripts/sim.js#L231)).
4. It schedules `boot()` for `DOMContentLoaded` ([sim.js:487-488](../../public/scripts/sim.js#L487-L488)).
5. It assigns `window.Sim` ([sim.js:490-504](../../public/scripts/sim.js#L490-L504)). This replaces any earlier `Sim` object,
   so anything that wants to add to `Sim` (`dataset.js`, `datalog.js`, the page) must run after this file.

The page's own script then runs and uses the helpers: it sizes its canvases, wires its sliders, starts its clock.

### The helpers, as a page uses them

- **Sharp canvases.** A screen with a device pixel ratio of 2 has four physical pixels under each CSS pixel. `canvas2d`
  sizes the canvas bitmap to the CSS box times that ratio and scales the drawing context by the same factor, so the page
  draws in CSS pixels and the result is sharp ([sim.js:32-46](../../public/scripts/sim.js#L32-L46)). The ratio is capped at 2
  ([sim.js:37](../../public/scripts/sim.js#L37)) to bound the cost of large canvases.
- **Typeset labels on a canvas.** `tex(ctx, 'c_{p}', x, y)` draws a label the way the lecture notes set it. `texRuns`
  splits the string into runs: plain text, a subscript `_{…}`, a superscript `^{…}`, or upright text `\mathrm{…}`
  ([sim.js:53-77](../../public/scripts/sim.js#L53-L77)). Each run is then split again into letters, which are set in
  italic, and everything else (digits, signs, capital Greek), which stays upright; a subscript of two or more Latin letters is
  a word and stays upright ([sim.js:79-86](../../public/scripts/sim.js#L79-L86)). Sub- and superscripts are drawn at 0.7 of
  the size, shifted down by 0.28 or up by 0.4 of the size ([sim.js:94](../../public/scripts/sim.js#L94),
  [sim.js:105](../../public/scripts/sim.js#L105)). The parser finds the first `}` after the opening brace, so braces cannot
  nest ([sim.js:68](../../public/scripts/sim.js#L68)).
- **Axis ticks.** `ticks(lo, hi, n)` divides the range by `n` (default 4), rounds that raw step to 1, 2, 5 or 10 times a
  power of ten, and lists the multiples of the step inside the range, with the number of decimals the step needs
  ([sim.js:113-118](../../public/scripts/sim.js#L113-L118)).
- **Pixel read-back.** `readPixel(box, x, y, r, test)` reads the canvas in a square that reaches $r$ CSS pixels to each side of
  $(x, y)$ (rounded to device pixels) and returns the pixel nearest the centre that is not transparent and passes `test`
  ([sim.js:122-138](../../public/scripts/sim.js#L122-L138)). A transparent pixel never passes
  ([sim.js:130](../../public/scripts/sim.js#L130)): the read-back first asks whether anything was drawn there, as the house
  rule in CLAUDE.md requires. `isBurgundy` and `isInk` are two ready-made tests: the accent colour (red channel 40 above green,
  30 above blue, below 215) and dark ink (alpha above 140, luminance below 110)
  ([sim.js:139-140](../../public/scripts/sim.js#L139-L140)).
- **Sliders.** `slider(id)` binds an `<input type="range">` and its optional `<output id="<id>-out">`, writes the filled
  fraction of the track into the CSS variable `--p`, and calls `onInput` with the new number
  ([sim.js:153-174](../../public/scripts/sim.js#L153-L174)).
- **The clock.** Think of a stopwatch that only advances while it runs. `clock(tick)` starts one `requestAnimationFrame`
  loop and calls `tick(dt, t)` every frame ([sim.js:177-198](../../public/scripts/sim.js#L177-L198)). The step `dt` is the
  real time since the last frame in seconds, but never more than 0.05 s ([sim.js:180](../../public/scripts/sim.js#L180)), so a
  tab that was hidden for a minute does not make the simulation jump a minute ahead. While paused, `tick` still runs every
  frame but with `dt = 0` and `t` does not grow ([sim.js:182-184](../../public/scripts/sim.js#L182-L184)); the page can still
  redraw. The clock starts paused when the reader's system asks for reduced motion
  ([sim.js:178](../../public/scripts/sim.js#L178)). `playButton` ties a button to a clock: its label reads Pause while
  playing and Play while paused ([sim.js:200-208](../../public/scripts/sim.js#L200-L208)).
- **Numbers.** `fmt(v, digits)` is `toFixed` with a typographic minus sign (U+2212) and never prints `-0.00`
  ([sim.js:211-215](../../public/scripts/sim.js#L211-L215)).

### At `DOMContentLoaded`: `boot()`

`boot()` ([sim.js:476-486](../../public/scripts/sim.js#L476-L486)) runs three steps in order.

1. `cards()` ([sim.js:234-304](../../public/scripts/sim.js#L234-L304)) would turn an `article.step` derivation inside a
   `.deriv` block into `<details>` cards. No page has a `.deriv` block, so it returns at once
   ([sim.js:236](../../public/scripts/sim.js#L236)); see the notes below.
2. `typeset()` ([sim.js:413-456](../../public/scripts/sim.js#L413-L456)) sets the mathematics.
   - It collects every `.paper` (the lecture note) and every `.stage__cap` and `.formula` (figure captions)
     ([sim.js:414](../../public/scripts/sim.js#L414)). With no paper but captions, `mathIn` sets only the captions
     ([sim.js:416](../../public/scripts/sim.js#L416), [sim.js:465-474](../../public/scripts/sim.js#L465-L474)).
   - It adds a "Skip to the lecture note" link at the top of the body ([sim.js:417-421](../../public/scripts/sim.js#L417-L421)).
   - It loads `vendor/katex/katex.min.js`, then `vendor/katex/contrib/auto-render.min.js`, one after the other, from `ROOT`
     ([sim.js:426-427](../../public/scripts/sim.js#L426-L427)). `load()` calls the next step on success and on failure alike
     ([sim.js:406-412](../../public/scripts/sim.js#L406-L412)).
   - In each paper, KaTeX's auto-render replaces `\[ … \]` by display mathematics and `\( … \)` by inline mathematics,
     skips elements with class `notex`, and does not stop on a bad formula (`throwOnError: false`)
     ([sim.js:430-436](../../public/scripts/sim.js#L430-L436)). Captions get inline mathematics only, and the root element gets
     the class `tex-ready` ([sim.js:459-464](../../public/scripts/sim.js#L459-L464)).
   - Each paper gets the class `is-typeset` ([sim.js:422-424](../../public/scripts/sim.js#L422-L424)). The stylesheet hides
     the paper body until then ([paper.css:24](../../public/styles/paper.css#L24)), so the reader never sees raw TeX. If
     KaTeX has not arrived after 4 s the paper is shown anyway ([sim.js:425](../../public/scripts/sim.js#L425)).
   - It then fires `typeset` on `document` ([sim.js:440](../../public/scripts/sim.js#L440)). `fold.js` listens for it to
     re-aim a `#hash` link, because the page grew taller ([fold.js:402](../../public/scripts/fold.js#L402)).
   - Independently, an `IntersectionObserver` marks the contents-list link of the section being read with `is-here`. A
     section counts as "being read" while it crosses the band from 20 % to 30 % of the window height, the margins
     `-20% 0px -70% 0px` ([sim.js:444-455](../../public/scripts/sim.js#L444-L455)).
3. The walkthrough. If the page has `#walk`, `boot()` appends a script tag for `../scripts/walk/<data-walk>.js` and, once it
   has loaded, calls `walkthrough(window.WALK[<key>])` ([sim.js:479-485](../../public/scripts/sim.js#L479-L485)). The engine is
   described in [walk.md](walk.md); in short:
   - it writes the section's HTML: heading, intro, a "Hold the numbers" switch, a numbered step list and one card
     ([sim.js:324-328](../../public/scripts/sim.js#L324-L328));
   - `show(i)` fills the card with the step's title, place in the code, formula, note, code excerpt and a symbol table
     whose "Now" column is empty at first ([sim.js:357-381](../../public/scripts/sim.js#L357-L381));
   - `update()` fills the "Now" column from `Sim.live()` every 200 ms ([sim.js:392-400](../../public/scripts/sim.js#L392-L400));
   - finally it hands the section to `Fold.walk` so it becomes a fold ([sim.js:402](../../public/scripts/sim.js#L402)).

## Public interface

| Name | Lines | Arguments | What it does / returns |
|---|---|---|---|
| `Sim.theme` | [6-23](../../public/scripts/sim.js#L6-L23) | none | Object of colours (`paper`, `card`, `cardSoft`, `ink`, `ink2`, `ink3`, `muted`, `rule`, `ruleSoft`, `accent`, `accentDark`, `rose`, `tan`, `tanInk`) and two canvas font strings (`mono`, `serif`). |
| `Sim.canvas2d` | [32-46](../../public/scripts/sim.js#L32-L46) | `canvas` element | Returns `box = { canvas, ctx, w, h, dpr, fit }`, already fitted. `w`, `h` are the CSS size in px. |
| `box.fit` | [35-44](../../public/scripts/sim.js#L35-L44) | none | Re-reads the CSS box, resizes the bitmap to `w·dpr × h·dpr`, resets the transform. Returns `box`. Resizing clears the canvas. |
| `Sim.tex` | [89-110](../../public/scripts/sim.js#L89-L110) | `ctx, s, x, y, o` with `o.size` (default 15 px), `o.align` (`'left'`, `'center'`, `'right'`), `o.baseline`, `o.color`, `o.upright`, `o.measure` | Draws the label and returns its width in CSS px; with `o.measure` only measures. Restores the caller's font, alignment and colour. |
| `Sim.ticks` | [113-118](../../public/scripts/sim.js#L113-L118) | `lo, hi, n` | `{ step, values, digits }`. |
| `Sim.readPixel` | [122-138](../../public/scripts/sim.js#L122-L138) | `box, x, y, r, test` (x, y, r in CSS px) | `{ found, rgba, dist, text }`: the nearest non-transparent passing pixel within `r`, its distance in CSS px, and a sentence such as `rgb(122, 31, 43), 1.5 px away` or `nothing (transparent)`. |
| `Sim.isBurgundy` | [139](../../public/scripts/sim.js#L139) | `rgba` array | True for the accent colour family. |
| `Sim.isInk` | [140](../../public/scripts/sim.js#L140) | `rgba` array | True for dark, mostly opaque pixels. |
| `Sim.onResize` | [142-150](../../public/scripts/sim.js#L142-L150) | `el, fn` | Calls `fn` 80 ms after the element stops changing size (`ResizeObserver`; window `resize` as a fallback). |
| `Sim.slider` | [153-174](../../public/scripts/sim.js#L153-L174) | `id, { format, onInput }` | `{ el, value (getter), set(v), paint() }`. `set` does not call `onInput`. |
| `Sim.clock` | [177-198](../../public/scripts/sim.js#L177-L198) | `tick(dt, t)` | `{ playing (getter), set(p), toggle(), onChange(fn) }`. |
| `Sim.playButton` | [200-208](../../public/scripts/sim.js#L200-L208) | `button, clock` | Binds the button to the clock and keeps its label in step. |
| `Sim.fmt` | [211-215](../../public/scripts/sim.js#L211-L215) | `v, digits` | String with fixed decimals and a typographic minus. |
| `Sim.showError` | [218-230](../../public/scripts/sim.js#L218-L230) | `message` | Inserts `#sim-error` ("This simulation stopped. … Reload the page to try again.") at the top of `<main>`, once per page. |

Which page uses which helper (occurrences of `Sim.<name>` counted with grep in the ten pages): every page uses `Sim.theme`,
`Sim.slider` and `Sim.clock`; every page except Fig. 3, which draws SVG, uses `Sim.canvas2d`, `Sim.onResize`,
`Sim.playButton` and `Sim.fmt`; `Sim.tex` is used by Figs. 5, 6, 8, 9 and 10; `Sim.ticks`, `Sim.readPixel` and
`Sim.isBurgundy` by Figs. 9 and 10 only; no page calls `Sim.isInk` or `Sim.showError`.

## Internal functions

| Name | Lines | What it does |
|---|---|---|
| `ROOT` (IIFE) | [26-29](../../public/scripts/sim.js#L26-L29) | Site root from `document.currentScript.src`. |
| `texRuns` | [53-88](../../public/scripts/sim.js#L53-L88) | Splits a label into runs `{ t, lv, up }`: text, level (−1 sub, 0, +1 super), upright or italic. |
| `font` (in `tex`) | [92-95](../../public/scripts/sim.js#L92-L95) | CSS font string for one run; upright runs fall back to `KaTeX_Main`, italic runs to `KaTeX_Math`. |
| `paint` (in `slider`) | [158-162](../../public/scripts/sim.js#L158-L162) | Writes `--p` and the `<output>` text. |
| `frame` (in `clock`) | [179-186](../../public/scripts/sim.js#L179-L186) | One animation frame: computes `dt`, advances `t`, calls `tick`, requests the next frame. |
| `paint` (in `playButton`) | [201-204](../../public/scripts/sim.js#L201-L204) | Sets the label and `aria-pressed`. |
| `cards` | [234-304](../../public/scripts/sim.js#L234-L304) | Derivation cards for `.deriv` (unused, see notes). |
| `openTarget` (in `cards`) | [295-298](../../public/scripts/sim.js#L295-L298) | Opens the `<details>` a hash points to. |
| `esc` | [307](../../public/scripts/sim.js#L307) | Escapes `&`, `<`, `>`. |
| `markup` | [310-318](../../public/scripts/sim.js#L310-L318) | Turns each `⟦key\|text⟧` into `<span class="k" data-k="key" tabindex="0">text</span>`; escapes the text in between when asked. |
| `walkthrough` | [320-403](../../public/scripts/sim.js#L320-L403) | Builds and runs the "From symbols to code" section. |
| `light` (in `walkthrough`) | [352-356](../../public/scripts/sim.js#L352-L356) | Toggles `is-lit` on every element of the card with the same `data-k`. |
| `show` (in `walkthrough`) | [357-381](../../public/scripts/sim.js#L357-L381) | Renders step `i` and forces one update of the "Now" column. |
| `read` (in `walkthrough`) | [388-390](../../public/scripts/sim.js#L388-L390) | Calls `Sim.live()`; returns `{}` if it is missing or throws. |
| `update` (in `walkthrough`) | [392-399](../../public/scripts/sim.js#L392-L399) | Writes each `[data-v]` cell from the live (or held) values; a missing key shows `—`. |
| `load` | [406-412](../../public/scripts/sim.js#L406-L412) | Appends a script to `<head>`; calls `done` on load or error. |
| `typeset` | [413-456](../../public/scripts/sim.js#L413-L456) | KaTeX for papers and captions, skip link, contents highlighter. |
| `show` (in `typeset`) | [422-424](../../public/scripts/sim.js#L422-L424) | Adds `is-typeset` to every paper. |
| `renderCaps` | [459-464](../../public/scripts/sim.js#L459-L464) | Inline mathematics in captions; adds `tex-ready` to `<html>`. |
| `mathIn` | [465-474](../../public/scripts/sim.js#L465-L474) | Captions only (no paper on the page); 4 s fallback for `tex-ready`. |
| `boot` | [476-486](../../public/scripts/sim.js#L476-L486) | `cards()`, `typeset()`, walkthrough loader. |

## State it keeps

- Module constants: `theme`, `ROOT`, `TEX_FAMILY`, `TEX_UPRIGHT` ([sim.js:51-52](../../public/scripts/sim.js#L51-L52)), the
  regular expression `MARK` ([sim.js:308](../../public/scripts/sim.js#L308)), whose `lastIndex` is reset before each use
  ([sim.js:312](../../public/scripts/sim.js#L312)).
- Per clock: `playing`, `last` (last frame time stamp), `t` (accumulated play time in s), `listeners`
  ([sim.js:178](../../public/scripts/sim.js#L178)).
- Per walkthrough: `cur` (current step), `held`, `snap` (the frozen values) ([sim.js:323](../../public/scripts/sim.js#L323),
  [sim.js:330](../../public/scripts/sim.js#L330)).
- No `localStorage` or `sessionStorage`.
- DOM it writes: the canvas bitmap size; `style="--p: …"` on sliders; button text and `aria-pressed`; `#sim-error`;
  `a.skip-link` at the top of `<body>`; class `is-typeset` on `.paper`; class `tex-ready` on `<html>`; class `is-here` on
  contents links; the whole content of `#walk`, class `is-held` on it, class `is-lit` on marked spans and table rows,
  `aria-selected` on step buttons.
- DOM it reads: `#walk[data-walk]`, `.paper`, `.paper[id]`, `.stage__cap`, `.formula`, `.paper__toc a[href^="#"]`, `main`,
  `.deriv`, `.deriv__head`, `article.step`.

## Timing and events

| What | Rate or delay | Where |
|---|---|---|
| Each `Sim.clock` | one `requestAnimationFrame` loop, every display frame, forever; `dt ≤ 0.05 s` | [sim.js:179-187](../../public/scripts/sim.js#L179-L187) |
| `Sim.onResize` | 80 ms after the last size change | [sim.js:146](../../public/scripts/sim.js#L146) |
| Walkthrough "Now" column | every 200 ms (5 rewrites per second), for the life of the page | [sim.js:400](../../public/scripts/sim.js#L400) |
| Paper shown without KaTeX | after 4000 ms | [sim.js:425](../../public/scripts/sim.js#L425), [sim.js:466](../../public/scripts/sim.js#L466) |
| `typeset` event | once, after both KaTeX scripts have loaded or failed | [sim.js:440](../../public/scripts/sim.js#L440) |

Listeners: `window` `error` ([sim.js:231](../../public/scripts/sim.js#L231)); `DOMContentLoaded`
([sim.js:487](../../public/scripts/sim.js#L487)); `input` on each slider ([sim.js:163](../../public/scripts/sim.js#L163));
`click` on play buttons ([sim.js:205](../../public/scripts/sim.js#L205)); in the walkthrough: `change` on Hold
([sim.js:331](../../public/scripts/sim.js#L331)), `click` and `keydown` on each step button (arrow keys, Home, End;
[sim.js:339-348](../../public/scripts/sim.js#L339-L348)), `mouseover`/`focusin` and `mouseout`/`focusout` on the card
([sim.js:382-387](../../public/scripts/sim.js#L382-L387)), `click` on Previous and Next
([sim.js:377-379](../../public/scripts/sim.js#L377-L379)).

## Contracts with other files

- **Simulation pages** provide `<section class="walk" id="walk" data-walk="<key>">`, an `article.paper` with `\( \)` and
  `\[ \]`, captions `.stage__cap`, and a function `Sim.live()` that returns an object of display strings keyed by the
  walkthrough's symbol keys (for example [Double Pendulum.html:684](../../public/simulations/Double%20Pendulum.html#L684)).
  See [walk.md](walk.md).
- **`walk/<key>.js`** must define `window.WALK[<key>]` ([walk.md](walk.md)).
- **`fold.js`** must load before `sim.js` so that `window.Fold` exists when the walkthrough calls `Fold.walk`
  ([sim.js:402](../../public/scripts/sim.js#L402), [fold.js:342](../../public/scripts/fold.js#L342)); it listens for
  `typeset` ([fold.js:402](../../public/scripts/fold.js#L402)). See [fold.md](fold.md).
- **`dataset.js`** adds `Sim.dataset` and **`datalog.js`** adds `Sim.colourMap` to the object made here
  ([dataset.js:17](../../public/scripts/dataset.js#L17), [datalog.js:71](../../public/scripts/datalog.js#L71)); both must
  load after `sim.js`. `datalog.js` uses `Sim.fmt` for every number it prints
  ([datalog.js:63](../../public/scripts/datalog.js#L63)). See [dataset.md](dataset.md) and [datalog.md](datalog.md).
- **KaTeX** files are self-hosted: [vendor/katex/katex.min.js](../../public/vendor/katex/katex.min.js) and
  [vendor/katex/contrib/auto-render.min.js](../../public/vendor/katex/contrib/auto-render.min.js). The KaTeX stylesheet comes
  through `sim.css` ([sim.css:8](../../public/styles/sim.css#L8)).
- **Styles**: `.walk__*`, `.k`, `.is-lit`, `.is-held` ([sim.css:206-241](../../public/styles/sim.css#L206-L241)),
  `.sim-error` ([sim.css:172](../../public/styles/sim.css#L172)), `.skip-link`
  ([sim.css:265](../../public/styles/sim.css#L265)), `html:not(.tex-ready) .stage__cap .tx`
  ([sim.css:303](../../public/styles/sim.css#L303)), `.paper__toc a.is-here`
  ([paper.css:38](../../public/styles/paper.css#L38)). See [../styles.md](../styles.md).

## How to change it safely

- Keep the load order `fold.js` → `sim.js` → `dataset.js` → page script → `datalog.js`. Line 490 creates `Sim` afresh, so
  anything attached to `Sim` before it is lost.
- Adding a helper: define it inside the IIFE and add it to the object at lines 490-504. Removing or renaming one: grep the
  ten pages first (the counts above).
- `readPixel` must keep refusing transparent pixels (line 130); the Check of Figs. 9 and 10 relies on it to tell "drawn" from
  "not drawn".
- `tex()` understands only `_{…}`, `^{…}` and `\mathrm{…}` without nested braces. A label with nesting needs a parser
  change, not a different string.
- The walkthrough HTML (lines 324-376) is styled by `sim.css`; class names are a contract with the stylesheet. The step and
  symbol fields are inserted as HTML except `where` and the code column of `syms`, which are escaped
  ([sim.js:364](../../public/scripts/sim.js#L364), [sim.js:369](../../public/scripts/sim.js#L369)).
- After a change, open all ten pages and check: no banner, the lecture note typeset, every "Now" cell filled (a missing key
  shows `—`), the walkthrough folds. A headless check of all ten pages (Chromium, 1.5 s after load) found no page errors
  and a `Sim.live()` value for every symbol key of every walkthrough.

## Notes for maintainers

1. `cards()` ([sim.js:234-304](../../public/scripts/sim.js#L234-L304)) is dead code: no page in `index.html`,
   `public/*.html` or `public/simulations/*.html` contains `class="deriv`. `sim.css` still has 36 lines mentioning `.deriv`,
   `.card__sum` or `.sub__sum`.
2. `Sim.isInk` ([sim.js:140](../../public/scripts/sim.js#L140)) is exported but no page uses it; `Sim.showError` is only
   called by this file's own `error` listener.
3. The walkthrough file is loaded from the relative path `'../scripts/walk/'` ([sim.js:483](../../public/scripts/sim.js#L483)),
   while KaTeX uses `ROOT` ([sim.js:426](../../public/scripts/sim.js#L426)). A page that is not exactly one folder below
   `public/` would fail to load its walkthrough.
4. The header comment ([sim.js:1-2](../../public/scripts/sim.js#L1-L2)) lists only the helpers, not the typesetting and the
   walkthrough engine that make up half the file.
5. `playButton` sets `aria-pressed="true"` while the clock is paused and the label reads "Play"
   ([sim.js:202-203](../../public/scripts/sim.js#L202-L203)), so a screen reader announces "Play, pressed" while nothing
   plays. Whether this is intended is not determined from the code.
6. The `error` listener ([sim.js:231](../../public/scripts/sim.js#L231)) reacts to any uncaught error on the page, also one
   thrown by `datalog.js` or a walkthrough file, and always says "This simulation stopped", even if the animation goes on.
7. The "Now" column is rewritten every 200 ms ([sim.js:400](../../public/scripts/sim.js#L400)), 5 times a second, and the
   interval keeps running while the walkthrough is folded away. CLAUDE.md asks for "about 4 per second" for readouts of a
   running figure; this column sits outside the figure, so the rule may not apply.
