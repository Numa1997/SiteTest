# public/scripts/sim.js

| | |
|---|---|
| File | [public/scripts/sim.js](../../public/scripts/sim.js), 429 lines, 20.9 kB (20 925 bytes) |
| Loaded by | the ten simulation pages in `public/simulations/`, as the second shared script, after `fold.js` and before `dataset.js` (table below); the two pages of Iron, Cotton and the Head (`portfolios/impact/index.html`, `ar.html`), first, before `dataset.js`, for the data panel ([portfolios.md](../portfolios.md#the-data-panel-of-the-study)); and the ideal and servo presses inside the Hydraulic Press Study's frames ([portfolios.md](../portfolios.md#the-data-panel-of-the-two-simulations-since-23-october-2026)). No other page loads it. A walkthrough is loaded only for an element `#walk` that names one in `data-walk`. |
| Defines | `window.Sim` ([sim.js:415](../../public/scripts/sim.js#L415)), a fresh object with 12 members |
| Reads | `window.WALK` ([sim.js:409](../../public/scripts/sim.js#L409)), `window.Fold` ([sim.js:328](../../public/scripts/sim.js#L328)), `window.Sim.live` ([sim.js:315](../../public/scripts/sim.js#L315)), `window.renderMathInElement` from KaTeX ([sim.js:355](../../public/scripts/sim.js#L355)) |
| Emits | the DOM event `typeset` on `document` ([sim.js:366](../../public/scripts/sim.js#L366), [sim.js:397](../../public/scripts/sim.js#L397)) |

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
| 1 | [Circular Wave Interference Visualization.html](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L505) | L505 | L506 | L507 | L508 | L904 |
| 2 | [Double Pendulum.html](../../public/simulations/Double%20Pendulum.html#L389) | L389 | L390 | L391 | L392 | L867 |
| 3 | [Interactive Double-Slit Experiment Visualization.html](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L546) | L546 | L547 | L548 | L549 | L945 |
| 4 | [Transverse and longitudinal waves.html](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L732) | L732 | L733 | L734 | L735 | L1083 |
| 5 | [water-wave.html](../../public/simulations/water-wave.html#L563) | L563 | L564 | L565 | L566 | L888 |
| 6 | [wave-interference.html](../../public/simulations/wave-interference.html#L489) | L489 | L490 | L491 | L492 | L974 |
| 7 | [phasor-sums.html](../../public/simulations/phasor-sums.html#L660) | L660 | L661 | L662 | L663 | L1476 |
| 8 | [draw-decompose.html](../../public/simulations/draw-decompose.html#L618) | L618 | L619 | L620 | L621 | L1413 |
| 9 | [driven-oscillator.html](../../public/simulations/driven-oscillator.html#L466) | L466 | L467 | L468 | L469 | L1110 |
| 10 | [wind-turbine.html](../../public/simulations/wind-turbine.html#L547) | L547 | L548 | L549 | L550 | L1168 |

The scripts are plain `<script src>` tags at the end of the body, so they run while the document is still loading. That is
why `sim.js` defers its own start to `DOMContentLoaded` ([sim.js:412](../../public/scripts/sim.js#L412)), and why
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
   ([sim.js:230](../../public/scripts/sim.js#L230)).
4. It schedules `boot()` for `DOMContentLoaded` ([sim.js:412-413](../../public/scripts/sim.js#L412-L413)).
5. It assigns `window.Sim` ([sim.js:415-428](../../public/scripts/sim.js#L415-L428)). This replaces any earlier `Sim` object,
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
  rule in CLAUDE.md requires. `isBurgundy` is the retained accent-colour test: red is 40 above green, 30 above blue, and below 215.
- **Sliders.** `slider(id)` binds an `<input type="range">` and its optional `<output id="<id>-out">`, writes the filled
  fraction of the track into the CSS variable `--p`, and calls `onInput` with the new number
  ([sim.js:152-173](../../public/scripts/sim.js#L152-L173)).
- **The clock.** Think of a stopwatch that only advances while it runs. `clock(tick)` starts one `requestAnimationFrame`
  loop and calls `tick(dt, t)` every frame ([sim.js:176-197](../../public/scripts/sim.js#L176-L197)). The step `dt` is the
  real time since the last frame in seconds, but never more than 0.05 s ([sim.js:179](../../public/scripts/sim.js#L179)), so a
  tab that was hidden for a minute does not make the simulation jump a minute ahead. While paused, `tick` still runs every
  frame but with `dt = 0` and `t` does not grow ([sim.js:181-183](../../public/scripts/sim.js#L181-L183)); the page can still
  redraw. The clock starts paused when the reader's system asks for reduced motion
  ([sim.js:177](../../public/scripts/sim.js#L177)). `playButton` ties a button to a clock: its label reads Pause while
  playing and Play while paused ([sim.js:199-207](../../public/scripts/sim.js#L199-L207)).
- **Numbers.** `fmt(v, digits)` is `toFixed` with a typographic minus sign (U+2212) and never prints `-0.00`
  ([sim.js:210-214](../../public/scripts/sim.js#L210-L214)).

### At `DOMContentLoaded`: `boot()`

`boot()` ([sim.js:402-411](../../public/scripts/sim.js#L402-L411)) runs two steps in order.

1. `typeset()` ([sim.js:339-382](../../public/scripts/sim.js#L339-L382)) sets the mathematics.
   - It collects every `.paper` (the lecture note) and every `.stage__cap` and `.formula` (figure captions)
     ([sim.js:340](../../public/scripts/sim.js#L340)). With no paper but captions, `mathIn` sets only the captions, and since 23 October 2026 only if a caption contains `\(`, so a
     page without mathematics in its captions (the impact study) loads no KaTeX
     ([sim.js:342](../../public/scripts/sim.js#L342), [sim.js:391-400](../../public/scripts/sim.js#L391-L400)).
   - It adds a "Skip to the lecture note" link at the top of the body ([sim.js:343-347](../../public/scripts/sim.js#L343-L347)).
   - It loads `vendor/katex/katex.min.js`, then `vendor/katex/contrib/auto-render.min.js`, one after the other, from `ROOT`
     ([sim.js:352-353](../../public/scripts/sim.js#L352-L353)). `load()` calls the next step on success and on failure alike
     ([sim.js:332-338](../../public/scripts/sim.js#L332-L338)).
   - In each paper, KaTeX's auto-render replaces `\[ … \]` by display mathematics and `\( … \)` by inline mathematics,
     skips elements with class `notex`, and does not stop on a bad formula (`throwOnError: false`)
     ([sim.js:356-362](../../public/scripts/sim.js#L356-L362)). Captions get inline mathematics only, and the root element gets
     the class `tex-ready` ([sim.js:385-390](../../public/scripts/sim.js#L385-L390)).
   - Each paper gets the class `is-typeset` ([sim.js:348-350](../../public/scripts/sim.js#L348-L350)). The stylesheet hides
     the paper body until then ([paper.css:24](../../public/styles/paper.css#L24)), so the reader never sees raw TeX. If
     KaTeX has not arrived after 4 s the paper is shown anyway ([sim.js:351](../../public/scripts/sim.js#L351)).
   - It then fires `typeset` on `document` ([sim.js:366](../../public/scripts/sim.js#L366)). `fold.js` listens for it to
     re-aim a `#hash` link, because the page grew taller ([fold.js:402](../../public/scripts/fold.js#L402)).
   - Independently, an `IntersectionObserver` marks the contents-list link of the section being read with `is-here`. A
     section counts as "being read" while it crosses the band from 20 % to 30 % of the window height, the margins
     `-20% 0px -70% 0px` ([sim.js:370-381](../../public/scripts/sim.js#L370-L381)).
2. The walkthrough. If the page has `#walk`, `boot()` appends a script tag for `../scripts/walk/<data-walk>.js` and, once it
   has loaded, calls `walkthrough(window.WALK[<key>])` ([sim.js:404-410](../../public/scripts/sim.js#L404-L410)). The engine is
   described in [walk.md](walk.md); in short:
   - it writes the section's HTML: heading, intro, a "Hold the numbers" switch, a numbered step list and one card
     ([sim.js:250-254](../../public/scripts/sim.js#L250-L254));
   - `show(i)` fills the card with the step's title, place in the code, formula, note, code excerpt and a symbol table
     whose "Now" column is empty at first ([sim.js:283-307](../../public/scripts/sim.js#L283-L307));
   - `update()` fills the "Now" column from `Sim.live()` every 200 ms ([sim.js:318-326](../../public/scripts/sim.js#L318-L326));
   - finally it hands the section to `Fold.walk` so it becomes a fold ([sim.js:328](../../public/scripts/sim.js#L328)).

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
| `Sim.onResize` | [141-149](../../public/scripts/sim.js#L141-L149) | `el, fn` | Calls `fn` 80 ms after the element stops changing size (`ResizeObserver`; window `resize` as a fallback). |
| `Sim.slider` | [152-173](../../public/scripts/sim.js#L152-L173) | `id, { format, onInput }` | `{ el, value (getter), set(v), paint() }`. `set` does not call `onInput`. |
| `Sim.clock` | [176-197](../../public/scripts/sim.js#L176-L197) | `tick(dt, t)` | `{ playing (getter), set(p), toggle(), onChange(fn) }`. |
| `Sim.playButton` | [199-207](../../public/scripts/sim.js#L199-L207) | `button, clock` | Binds the button to the clock and keeps its label in step. |
| `Sim.fmt` | [210-214](../../public/scripts/sim.js#L210-L214) | `v, digits` | String with fixed decimals and a typographic minus. |
| `Sim.showError` | [217-229](../../public/scripts/sim.js#L217-L229) | `message` | Inserts `#sim-error` ("This simulation stopped. … Reload the page to try again.") at the top of `<main>`, once per page. |

Which page uses which helper (occurrences of `Sim.<name>` counted with grep in the ten pages): every page uses `Sim.theme`,
`Sim.slider` and `Sim.clock`; every page except Fig. 3, which draws SVG, uses `Sim.canvas2d`, `Sim.onResize`,
`Sim.playButton` and `Sim.fmt`; `Sim.tex` is used by Figs. 5, 6, 8, 9 and 10; `Sim.ticks`, `Sim.readPixel` and
`Sim.isBurgundy` by Figs. 9 and 10 only; no page calls `Sim.showError` directly.

## Internal functions

| Name | Lines | What it does |
|---|---|---|
| `ROOT` (IIFE) | [26-29](../../public/scripts/sim.js#L26-L29) | Site root from `document.currentScript.src`. |
| `texRuns` | [53-88](../../public/scripts/sim.js#L53-L88) | Splits a label into runs `{ t, lv, up }`: text, level (−1 sub, 0, +1 super), upright or italic. |
| `font` (in `tex`) | [92-95](../../public/scripts/sim.js#L92-L95) | CSS font string for one run; upright runs fall back to `KaTeX_Main`, italic runs to `KaTeX_Math`. |
| `paint` (in `slider`) | [157-161](../../public/scripts/sim.js#L157-L161) | Writes `--p` and the `<output>` text. |
| `frame` (in `clock`) | [178-185](../../public/scripts/sim.js#L178-L185) | One animation frame: computes `dt`, advances `t`, calls `tick`, requests the next frame. |
| `paint` (in `playButton`) | [200-203](../../public/scripts/sim.js#L200-L203) | Sets the label and `aria-pressed`. |
| `esc` | [233](../../public/scripts/sim.js#L233) | Escapes `&`, `<`, `>`. |
| `markup` | [236-244](../../public/scripts/sim.js#L236-L244) | Turns each `⟦key\|text⟧` into `<span class="k" data-k="key" tabindex="0">text</span>`; escapes the text in between when asked. |
| `walkthrough` | [246-329](../../public/scripts/sim.js#L246-L329) | Builds and runs the "From symbols to code" section. |
| `light` (in `walkthrough`) | [278-282](../../public/scripts/sim.js#L278-L282) | Toggles `is-lit` on every element of the card with the same `data-k`. |
| `show` (in `walkthrough`) | [283-307](../../public/scripts/sim.js#L283-L307) | Renders step `i` and forces one update of the "Now" column. |
| `read` (in `walkthrough`) | [314-316](../../public/scripts/sim.js#L314-L316) | Calls `Sim.live()`; returns `{}` if it is missing or throws. |
| `update` (in `walkthrough`) | [318-325](../../public/scripts/sim.js#L318-L325) | Writes each `[data-v]` cell from the live (or held) values; a missing key shows `—`. |
| `load` | [332-338](../../public/scripts/sim.js#L332-L338) | Appends a script to `<head>`; calls `done` on load or error. |
| `typeset` | [339-382](../../public/scripts/sim.js#L339-L382) | KaTeX for papers and captions, skip link, contents highlighter. |
| `show` (in `typeset`) | [348-350](../../public/scripts/sim.js#L348-L350) | Adds `is-typeset` to every paper. |
| `renderCaps` | [385-390](../../public/scripts/sim.js#L385-L390) | Inline mathematics in captions; adds `tex-ready` to `<html>`. |
| `mathIn` | [391-400](../../public/scripts/sim.js#L391-L400) | Captions only (no paper on the page); 4 s fallback for `tex-ready`. |
| `boot` | [402-411](../../public/scripts/sim.js#L402-L411) | `typeset()` and the walkthrough loader. |

## State it keeps

- Module constants: `theme`, `ROOT`, `TEX_FAMILY`, `TEX_UPRIGHT` ([sim.js:51-52](../../public/scripts/sim.js#L51-L52)), the
  regular expression `MARK` ([sim.js:234](../../public/scripts/sim.js#L234)), whose `lastIndex` is reset before each use
  ([sim.js:238](../../public/scripts/sim.js#L238)).
- Per clock: `playing`, `last` (last frame time stamp), `t` (accumulated play time in s), `listeners`
  ([sim.js:177](../../public/scripts/sim.js#L177)).
- Per walkthrough: `cur` (current step), `held`, `snap` (the frozen values) ([sim.js:249](../../public/scripts/sim.js#L249),
  [sim.js:256](../../public/scripts/sim.js#L256)).
- No `localStorage` or `sessionStorage`.
- DOM it writes: the canvas bitmap size; `style="--p: …"` on sliders; button text and `aria-pressed`; `#sim-error`;
  `a.skip-link` at the top of `<body>`; class `is-typeset` on `.paper`; class `tex-ready` on `<html>`; class `is-here` on
  contents links; the whole content of `#walk`, class `is-held` on it, class `is-lit` on marked spans and table rows,
  `aria-selected` on step buttons.
- DOM it reads: `#walk[data-walk]`, `.paper`, `.paper[id]`, `.stage__cap`, `.formula`, `.paper__toc a[href^="#"]`, `main`.

## Timing and events

| What | Rate or delay | Where |
|---|---|---|
| Each `Sim.clock` | one `requestAnimationFrame` loop, every display frame, forever; `dt ≤ 0.05 s` | [sim.js:178-186](../../public/scripts/sim.js#L178-L186) |
| `Sim.onResize` | 80 ms after the last size change | [sim.js:145](../../public/scripts/sim.js#L145) |
| Walkthrough "Now" column | every 200 ms (5 rewrites per second), for the life of the page | [sim.js:326](../../public/scripts/sim.js#L326) |
| Paper shown without KaTeX | after 4000 ms | [sim.js:351](../../public/scripts/sim.js#L351), [sim.js:392](../../public/scripts/sim.js#L392) |
| `typeset` event | once, after both KaTeX scripts have loaded or failed | [sim.js:366](../../public/scripts/sim.js#L366) |

Listeners: `window` `error` ([sim.js:230](../../public/scripts/sim.js#L230)); `DOMContentLoaded`
([sim.js:412](../../public/scripts/sim.js#L412)); `input` on each slider ([sim.js:162](../../public/scripts/sim.js#L162));
`click` on play buttons ([sim.js:204](../../public/scripts/sim.js#L204)); in the walkthrough: `change` on Hold
([sim.js:257](../../public/scripts/sim.js#L257)), `click` and `keydown` on each step button (arrow keys, Home, End;
[sim.js:265-274](../../public/scripts/sim.js#L265-L274)), `mouseover`/`focusin` and `mouseout`/`focusout` on the card
([sim.js:308-313](../../public/scripts/sim.js#L308-L313)), `click` on Previous and Next
([sim.js:303-305](../../public/scripts/sim.js#L303-L305)).

## Contracts with other files

- **Simulation pages** provide `<section class="walk" id="walk" data-walk="<key>">`, an `article.paper` with `\( \)` and
  `\[ \]`, captions `.stage__cap`, and a function `Sim.live()` that returns an object of display strings keyed by the
  walkthrough's symbol keys (for example [Double Pendulum.html:684](../../public/simulations/Double%20Pendulum.html#L684)).
  See [walk.md](walk.md).
- **`walk/<key>.js`** must define `window.WALK[<key>]` ([walk.md](walk.md)).
- **`fold.js`** must load before `sim.js` so that `window.Fold` exists when the walkthrough calls `Fold.walk`
  ([sim.js:328](../../public/scripts/sim.js#L328), [fold.js:342](../../public/scripts/fold.js#L342)); it listens for
  `typeset` ([fold.js:402](../../public/scripts/fold.js#L402)). See [fold.md](fold.md).
- **`dataset.js`** adds `Sim.dataset` and **`datalog.js`** adds `Sim.colourMap` to the object made here
  ([dataset.js:17](../../public/scripts/dataset.js#L17), [datalog.js:71](../../public/scripts/datalog.js#L71)); both must
  load after `sim.js`. `datalog.js` uses `Sim.fmt` for every number it prints
  ([datalog.js:63](../../public/scripts/datalog.js#L63)). See [dataset.md](dataset.md) and [datalog.md](datalog.md).
- **KaTeX** files are self-hosted: [vendor/katex/katex.min.js](../../public/vendor/katex/katex.min.js) and
  [vendor/katex/contrib/auto-render.min.js](../../public/vendor/katex/contrib/auto-render.min.js). The KaTeX stylesheet comes
  through `sim.css` ([sim.css:8](../../public/styles/sim.css#L8)).
- **Styles**: `.walk__*`, `.k`, `.is-lit`, `.is-held` ([sim.css:137-172](../../public/styles/sim.css#L137-L172)),
  `.sim-error` ([sim.css:132](../../public/styles/sim.css#L132)), `.skip-link`
  ([sim.css:191](../../public/styles/sim.css#L191)), `html:not(.tex-ready) .stage__cap .tx`
  ([sim.css:228](../../public/styles/sim.css#L228)), `.paper__toc a.is-here`
  ([paper.css:38](../../public/styles/paper.css#L38)). See [../styles.md](../styles.md).

## How to change it safely

- Keep the load order `fold.js` → `sim.js` → `dataset.js` → page script → `datalog.js`. [Line 415](../../public/scripts/sim.js#L415) creates `Sim` afresh, so
  anything attached to `Sim` before it is lost.
- Adding a helper: define it inside the IIFE and add it to the object at [lines 415-428](../../public/scripts/sim.js#L415-L428). Removing or renaming one: grep the
  ten pages first (the counts above).
- `readPixel` must keep refusing transparent pixels ([line 130](../../public/scripts/sim.js#L130)); the Check of Figs. 9 and 10 relies on it to tell "drawn" from
  "not drawn".
- `tex()` understands only `_{…}`, `^{…}` and `\mathrm{…}` without nested braces. A label with nesting needs a parser
  change, not a different string.
- The walkthrough HTML ([lines 250-302](../../public/scripts/sim.js#L250-L302)) is styled by `sim.css`; class names are a contract with the stylesheet. The step and
  symbol fields are inserted as HTML except `where`, the code excerpt `code` (escaped around its marks by `markup(st.code, true)`)
  and the code column of `syms`, which are escaped ([sim.js:290](../../public/scripts/sim.js#L290),
  [sim.js:295](../../public/scripts/sim.js#L295), [sim.js:298](../../public/scripts/sim.js#L298)).
- After a change, open all ten pages and check: no banner, the lecture note typeset, every "Now" cell filled (a missing key
  shows `—`), the walkthrough folds. A headless check of all ten pages (Chromium, 1.5 s after load) found no page errors
  and a `Sim.live()` value for every symbol key of every walkthrough.

## Notes for maintainers

1. Fixed on 2026-10-15: the unused derivation-card builder, boot call and unused selectors were removed; active equation and walkthrough styles remain (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
2. Fixed on 2026-10-15: the unused isInk helper and export were removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
3. The walkthrough file is loaded from the relative path `'../scripts/walk/'` ([sim.js:408](../../public/scripts/sim.js#L408)),
   while KaTeX uses `ROOT` ([sim.js:352](../../public/scripts/sim.js#L352)). A page that is not exactly one folder below
   `public/` would fail to load its walkthrough.
4. The header comment ([sim.js:1-2](../../public/scripts/sim.js#L1-L2)) lists only the helpers, not the typesetting and the
   walkthrough engine that make up half the file.
5. `playButton` sets `aria-pressed="true"` while the clock is paused and the label reads "Play"
   ([sim.js:201-202](../../public/scripts/sim.js#L201-L202)), so a screen reader announces "Play, pressed" while nothing
   plays. Whether this is intended is not determined from the code.
6. The `error` listener ([sim.js:230](../../public/scripts/sim.js#L230)) reacts to any uncaught error on the page, also one
   thrown by `datalog.js` or a walkthrough file, and always says "This simulation stopped", even if the animation goes on.
7. The "Now" column is rewritten every 200 ms ([sim.js:326](../../public/scripts/sim.js#L326)), 5 times a second, and the
   interval keeps running while the walkthrough is folded away. CLAUDE.md asks for "about 4 per second" for readouts of a
   running figure; this column sits outside the figure, so the rule may not apply.

## The Algebra column is typeset (21 October 2026)

`algebra(math)` in `sim.js` splits a step's `math` field at each `<br>`, translates each line from the light HTML it is written in (`<sub>`, `<sup>`, Unicode symbols, upright `<span style="font-style: normal">` words) to TeX with `htmlToTex()`, and typesets it with KaTeX, the same mathematics as the lecture note. A mark `⟦key|…⟧` becomes `\htmlClass{k}{\htmlData{k=key}{…}}`, so hovering still lights the formula, the code and the table together. A line KaTeX cannot read stays as written. The walkthrough is drawn again when KaTeX has loaded (the `typeset` event). Checked on all ten pages: 270 of 270 lines typeset, no sideways scroll at 390 px.
