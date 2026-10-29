# public/scripts/catalog.js

| | |
|---|---|
| File | [public/scripts/catalog.js](../../public/scripts/catalog.js), 218 lines, 14.2 kB (14 170 bytes) |
| Loaded by | [simulations.html:124](../../public/simulations.html#L124) only, after `fold.js` (L123) and before `vendor/katex/katex.min.js` (L125) and the page's inline script (L126-351) |
| Defines | `window.SIM_TOOLS` ([catalog.js:26](../../public/scripts/catalog.js#L26)), `window.SIM_FIELDS` ([catalog.js:35](../../public/scripts/catalog.js#L35)), `window.SIMULATIONS` ([catalog.js:46](../../public/scripts/catalog.js#L46)) |
| Reads | nothing |

`catalog.js` is the registry of the simulations: one entry per simulation page with everything the simulations list shows
about it (figure number, title, file, field, course year, abstract, key equation, model, method, controls, concepts). It holds
data only. `simulations.html` draws its whole list, its search and its filter chips from it, in figure order
([catalog.js:1-5](../../public/scripts/catalog.js#L1-L5)).

## How it works

The file is one IIFE that assigns three globals and returns ([catalog.js:23-218](../../public/scripts/catalog.js#L23-L218)).
There is no logic apart from the constant `ALL`, the list of all six tool names, which every entry uses as its `has`
([catalog.js:44](../../public/scripts/catalog.js#L44)).

### `SIMULATIONS`: the entries

The field list is documented in the file's header ([catalog.js:7-22](../../public/scripts/catalog.js#L7-L22)). The table adds
how `simulations.html` uses each field.

| Field | Type | Meaning | Used by `simulations.html` |
|---|---|---|---|
| `id` | string | short name; also the thumbnail name `images/sims/<id>.webp` | thumbnail path ([L207](../../public/simulations.html#L207)); card ids `sim-<id>` and `simulation-<id>`, which are also the keys under which `fold.js` remembers a card as open or closed ([L204](../../public/simulations.html#L204), [L236](../../public/simulations.html#L236)); key of `openCards` ([L342](../../public/simulations.html#L342)) |
| `fig` | number | figure number as printed on the page; the list is sorted by it | sort ([L163](../../public/simulations.html#L163)); search words `fig N`, `fig. N` ([L159](../../public/simulations.html#L159)); "Figure N" caption, "Fig. N" placeholder, "Open Fig. N" link, two-digit fold number ([L206-L208](../../public/simulations.html#L206-L208), [L224](../../public/simulations.html#L224), [L237](../../public/simulations.html#L237)) |
| `title` | string | the page's `h1` without the final dot | fold title and `data-label`, card heading, search ([L236-L237](../../public/simulations.html#L236-L237), [L211](../../public/simulations.html#L211)) |
| `file` | string | path from `public/`; the lecture note is `file + '#paper'` | links, passed through `encodeURI` so spaces become `%20` ([L201](../../public/simulations.html#L201), [L225](../../public/simulations.html#L225)) |
| `field` | string | an `id` from `SIM_FIELDS` | field chip filter ([L166](../../public/simulations.html#L166)); field name in the kicker line and in the search text ([L210](../../public/simulations.html#L210), [L160](../../public/simulations.html#L160)) |
| `stage` | number | course year the figure is written for: 1 first, 2 second | year chip filter, compared as a string ([L167](../../public/simulations.html#L167)); "first year", "second year", or "year N" in the kicker ([L202](../../public/simulations.html#L202)) |
| `subject` | string | the subject line under the figure number on the page | the fold's counts line ([L236](../../public/simulations.html#L236)); caption, first letter capitalised ([L208](../../public/simulations.html#L208)); search |
| `summary` | string | two or three sentences, the abstract of the lecture note | abstract paragraph ([L212](../../public/simulations.html#L212)); search |
| `equation` | string | the key equation in TeX, display style | `data-tex`, rendered by `katex.render` with `displayMode: true`; on failure shown as plain text ([L213](../../public/simulations.html#L213), [L248-L258](../../public/simulations.html#L248-L258)) |
| `model` | string | the equations the figure is built on, in words | "model" in the details ([L216](../../public/simulations.html#L216)); search |
| `method` | string | how the page computes them | "method" ([L217](../../public/simulations.html#L217)); search |
| `controls` | string | what the reader sets | "you set" ([L218](../../public/simulations.html#L218)); search |
| `concepts` | array of strings | search words and tags | the first six as tags ([L221](../../public/simulations.html#L221)); all in the search ([L160](../../public/simulations.html#L160)) |
| `has` | array of `SIM_TOOLS` keys | which shared tools the page carries | not read |
| `added` | `YYYY-MM-DD` | date first published | not read |

The eleven entries, in the order of the array, which is also figure order:

| Fig. | `id` | `title` | `file` | `field` | `stage` | `added` | Line |
|---|---|---|---|---|---|---|---|
| 1 | `wave-sources` | Wave Interference | `simulations/Circular Wave Interference Visualization.html` | optics | 1 | 2026-10-06 | [47](../../public/scripts/catalog.js#L47) |
| 2 | `double-pendulum` | Double Pendulum | `simulations/Double Pendulum.html` | mechanics | 2 | 2026-10-06 | [64](../../public/scripts/catalog.js#L64) |
| 3 | `double-slit` | Double-Slit Interference | `simulations/Interactive Double-Slit Experiment Visualization.html` | optics | 1 | 2026-10-06 | [81](../../public/scripts/catalog.js#L81) |
| 4 | `transverse-longitudinal` | Transverse & Longitudinal | `simulations/Transverse and longitudinal waves.html` | waves | 1 | 2026-10-06 | [98](../../public/scripts/catalog.js#L98) |
| 5 | `water-wave` | Circular Water Waves | `simulations/water-wave.html` | fluids | 2 | 2026-10-06 | [115](../../public/scripts/catalog.js#L115) |
| 6 | `wave-bench` | Wave Interference Simulator | `simulations/wave-interference.html` | waves | 1 | 2026-10-06 | [132](../../public/scripts/catalog.js#L132) |
| 7 | `phasor-sums` | Phasor Sums | `simulations/phasor-sums.html` | methods | 2 | 2026-10-06 | [149](../../public/scripts/catalog.js#L149) |
| 8 | `draw-decompose` | Draw & Decompose | `simulations/draw-decompose.html` | methods | 2 | 2026-10-06 | [166](../../public/scripts/catalog.js#L166) |
| 9 | `driven-oscillator` | Driven Oscillator | `simulations/driven-oscillator.html` | control | 1 | 2026-10-14 | [183](../../public/scripts/catalog.js#L183) |
| 10 | `wind-turbine` | Wind Turbine Control | `simulations/wind-turbine.html` | control | 2 | 2026-10-14 | [200](../../public/scripts/catalog.js#L200) |
| 11 | `pendulum-control` | Double Pendulum under Control | `simulations/pendulum-control.html` | control | 2 | 2026-10-24 | [217](../../public/scripts/catalog.js#L217) |

Every entry has `has: ALL`. All eleven thumbnails exist in [public/images/sims/](../../public/images/sims/).

### `SIM_FIELDS`

Six fields, each `{ id, name, blurb }` ([catalog.js:35-42](../../public/scripts/catalog.js#L35-L42)): `mechanics` Mechanics,
`waves` Oscillations and waves, `fluids` Fluids, `optics` Wave optics, `methods` Mathematical methods, `control` Control
systems. The order of this array is the order of the field chips. `name` is shown; `blurb` is not shown anywhere: the paragraph
the former hidden `#intro` element was removed; the registry metadata is retained.

### `SIM_TOOLS`

Six short descriptions keyed `derivation`, `walkthrough`, `data`, `read`, `round`, `check` ([catalog.js:26-33](../../public/scripts/catalog.js#L26-L33)).
No file reads them (grep over `index.html`, `public/*.html`, `public/simulations/*.html`, `public/scripts/*.js`).

## How `simulations.html` uses the registry

The inline script ([simulations.html:126-351](../../public/simulations.html#L126-L351)) runs once, at the end of the body:

1. **Copy and index.** It copies `SIMULATIONS` into `SIMS` and builds for each entry a lower-case search text `_hay` from title,
   `fig N`, `fig. N`, subject, summary, model, method, controls, concepts and field name ([L129](../../public/simulations.html#L129),
   [L158-L161](../../public/simulations.html#L158-L161)). The copy is shallow, so `_hay` is written onto the shared entry objects.
   It sorts by `fig` ([L163](../../public/simulations.html#L163)).
   On a German or Arabic page `_hay` also holds the translated words (`T(s.title)` and so on), so a search finds both.
2. **Search text folding.** `fold(s)` ([L148-L153](../../public/simulations.html#L148-L153)) lowers the case, replaces the Greek
   letters λ θ ω φ ψ α γ δ ζ σ τ and ∇ by their names, strips accents (Unicode NFD, then the combining marks U+0300 to U+036F),
   drops apostrophes ’ and ', and turns en and em dashes into hyphens. So "lambda" finds "λ" and "Huygens" finds "Huygens’". The
   query is folded the same way and split on spaces; an entry matches when every word is a substring of its `_hay`
   ([L165-L173](../../public/simulations.html#L165-L173)).
3. **Chips.** The field chips list only the `SIM_FIELDS` that some entry uses, after an "All fields" chip; the year chips list
   the hard-coded `STAGES` 1 and 2 that some entry uses, after "Any year" ([L131-L134](../../public/simulations.html#L131-L134),
   [L337-L340](../../public/simulations.html#L337-L340)). A chip toggles its filter ([L192-L195](../../public/simulations.html#L192-L195)).
   Each chip shows how many entries would match with the search and the other filter, ignoring its own
   ([L270-L281](../../public/simulations.html#L270-L281)).
4. **Draw.** `render()` ([L260-L289](../../public/simulations.html#L260-L289)) filters, writes one `section.simfold` per match
   (title with the two-digit figure number; inside it the `article.entry[data-card]` with thumbnail, caption, kicker, title,
   abstract, equation, details behind More / Less, and links), makes each section a fold with `Fold.make`, typesets the
   equations with KaTeX, and removes any thumbnail that fails to load, which leaves the "Fig. N" placeholder
   ([L266-L268](../../public/simulations.html#L266-L268)). The folds are closed by default and forced open while a search or chip
   filters, without changing what the reader chose ([L241-L246](../../public/simulations.html#L241-L246); [fold.md](fold.md)).
   It updates the chip counts, "N shown" or "N of 10 shown", and the "No simulation matches …" message.
5. **More / Less.** Which cards show their details is kept in `openCards` so a redraw keeps it; `Fold.onCard` and `Fold.onAll`
   keep it up to date ([L140](../../public/simulations.html#L140), [L341-L345](../../public/simulations.html#L341-L345)). It is not
   stored between visits.
6. **Address.** The view lives in the address as `?q=…&field=…&stage=…`. `load()` reads it at start and drops a `field` or
   `stage` that does not exist; `save()` writes it with `history.replaceState` after each change by the reader, keeping the hash
   ([L292-L309](../../public/simulations.html#L292-L309)).
7. **Keys.** Typing in the search redraws 120 ms after the last key; Esc clears it; `/` anywhere outside a text field focuses it
   ([L311-L325](../../public/simulations.html#L311-L325)). "Show all simulations" resets everything ([L326-L331](../../public/simulations.html#L326-L331)).
8. **Statistics.** The header counts simulations, fields and course years ([L175-L183](../../public/simulations.html#L175-L183)).

`window.__catalog = { count, state, render }` exposes the state for tests ([L349](../../public/simulations.html#L349)). The page
itself is documented in [../pages.md](../pages.md).

Measured in headless Chromium: the page opens with 10 closed folds and the Expand all / Collapse all buttons right before
`#catalog`; with `?q=chaos` it shows "1 of 10 shown", that one fold open, and the field chips read Mechanics 1 and every other
field 0.

## Public interface

| Name | Lines | Shape | What it is |
|---|---|---|---|
| `window.SIM_TOOLS` | [26-33](../../public/scripts/catalog.js#L26-L33) | `{ key: description }` | The shared tools a page can carry. |
| `window.SIM_FIELDS` | [35-42](../../public/scripts/catalog.js#L35-L42) | `[{ id, name, blurb }]` | Fields, in chip order. |
| `window.SIMULATIONS` | [46-217](../../public/scripts/catalog.js#L46-L217) | `[entry]` | One entry per simulation (fields above). |

## Internal functions

None. The only internal name is the constant `ALL` ([catalog.js:44](../../public/scripts/catalog.js#L44)).

## State it keeps

Only the three globals. No storage, no DOM, no listeners, no timers.

## Timing and events

None.

## Contracts with other files

- **`simulations.html`** reads all three globals at the start of its inline script
  ([simulations.html:129-130](../../public/simulations.html#L129-L130)) and must load `catalog.js` before it.
- **Thumbnails** `public/images/sims/<id>.webp`, 800 × 500 px, stills of the page's main figure (AGENTS.md;
  [catalog.js:4](../../public/scripts/catalog.js#L4)).
- **Simulation pages**: `file` must match the page's file name; `fig`, `title` and `subject` should match the figure number,
  `h1` and subject line printed on the page ([catalog.js:9-14](../../public/scripts/catalog.js#L9-L14)). Each page's own
  documentation links back to its entry ([../simulations/](../simulations/)).
- **`fold.js`** provides the folds and More / Less on the list ([fold.md](fold.md)).

## How to add a simulation

1. Write the page in `public/simulations/` (see an existing page and [../simulations/](../simulations/)).
2. Add one entry to `SIMULATIONS` with every field above, at its place in figure order; `fig` decides the order on screen in any
   case ([simulations.html:163](../../public/simulations.html#L163)).
3. If its field is new, add it to `SIM_FIELDS`; its chip appears by itself.
4. Add the thumbnail `public/images/sims/<id>.webp`, 800 × 500 px. Without it the card shows "Fig. N" in its place.
5. Add the new number to the hand-written figure links at the top of every simulation page, for example
   [Double Pendulum.html:19-31](../../public/simulations/Double%20Pendulum.html#L19-L31) (AGENTS.md).
6. Check: the list shows the entry at its place, the search finds it by title and by a concept, the chips count it, the
   equation typesets, both links open.

A `stage` other than 1 or 2 needs a change in `simulations.html` too: see note 3.

## Notes for maintainers

1. `SIM_TOOLS` ([catalog.js:26-33](../../public/scripts/catalog.js#L26-L33)) and the entry fields `has` and `added` are not read
   by any file. The header says `has` refers to `SIM_TOOLS` ([catalog.js:21](../../public/scripts/catalog.js#L21)); nothing
   displays either.
2. Fixed on 2026-10-15: the unused hidden intro was removed; blurb metadata remains available for a future content decision (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
3. Fixed on 2026-10-15: the header identifies the catalog-page changes needed for a new course year (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
4. The page's search index `_hay` is written onto the shared `SIMULATIONS` objects ([simulations.html:158-161](../../public/simulations.html#L158-L161)),
   because `slice()` copies only the array. Harmless today, since nothing else reads the registry.
