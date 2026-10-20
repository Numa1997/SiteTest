# public/scripts/walk/*.js

| | |
|---|---|
| Files | ten files in [public/scripts/walk/](../../public/scripts/walk/), 109 to 137 lines and 6.4 to 10.9 kB each, 1 199 lines and 80.3 kB in all (table at the end) |
| Loaded by | `sim.js`, not by a `<script>` tag: once the page has loaded, `boot()` appends `../scripts/walk/<key>.js`, where `<key>` is the `data-walk` attribute of `#walk` ([sim.js:404-410](../../public/scripts/sim.js#L404-L410)) |
| Defines | `window.WALK` (created if missing) and one entry `window.WALK.<key>` per file |
| Rendered by | `walkthrough()` in [sim.js:246-329](../../public/scripts/sim.js#L246-L329), described in [sim.md](sim.md) |

Each file holds the "From symbols to code" walkthrough of one simulation page: a short introduction and six to eight steps,
each pairing an equation with the exact lines of the page's own code that compute it, plus a table of the symbols with their
value in the running simulation now. The files hold data only; `sim.js` turns them into the section, and the page supplies the
live values through `Sim.live()`. The physics of each step is that of the page's lecture note, documented per page in
[../simulations/](../simulations/).

## The shared format

Every file follows the same pattern ([pendulum.js:5-22](../../public/scripts/walk/pendulum.js#L5-L22)):

```js
window.WALK = window.WALK || {};
window.WALK.pendulum = {
    intro: 'Eight steps from the Lagrangian to the dots on the screen. …',
    steps: [
        {
            title: 'The state vector',
            where: 'restart() — the initial condition',
            math: '⟦s|<b>s</b>⟧ = (⟦t1|θ<sub>1</sub>⟧, ⟦t2|θ<sub>2</sub>⟧, ⟦o1|ω<sub>1</sub>⟧, ⟦o2|ω<sub>2</sub>⟧)',
            note: 'Two second-order equations become four first-order ones: …',
            code: `⟦s|state⟧ = [⟦t1|th1.value * Math.PI / 180⟧, ⟦t2|th2.value * Math.PI / 180⟧, ⟦o1|w1.value⟧, ⟦o2|w2.value⟧];`,
            syms: [
                ['t1', 'θ<sub>1</sub>', 'state[0]', 'upper rod angle, rad'],
                …
            ]
        },
        …
    ]
};
```

| Field | Type | Shown as | Escaped? |
|---|---|---|---|
| `intro` | string | the paragraph under the heading "From symbols to code" ([sim.js:251](../../public/scripts/sim.js#L251)) | no, HTML |
| `steps[].title` | string | the step's button in the list ("01 …") and the card heading ([sim.js:264](../../public/scripts/sim.js#L264), [sim.js:295](../../public/scripts/sim.js#L295)) | no, HTML |
| `steps[].where` | string | where in the page's code the lines are, under the heading ([sim.js:295](../../public/scripts/sim.js#L295)) | yes, plain text |
| `steps[].math` | string with marks | the "Algebra" column ([sim.js:297](../../public/scripts/sim.js#L297)) | no, HTML (`<sub>`, `<sup>`, `<b>`, `<br>`) |
| `steps[].note` | string | the paragraph under the formula ([sim.js:297](../../public/scripts/sim.js#L297)) | no, HTML |
| `steps[].code` | template literal with marks | the "Code · as written in this page" column, in `<pre><code>` ([sim.js:298](../../public/scripts/sim.js#L298)) | yes, plain text; line breaks kept |
| `steps[].syms` | array of `[key, symbol, inCode, meaning]` | one table row each: Symbol, In code, Now, Meaning ([sim.js:289-292](../../public/scripts/sim.js#L289-L292)) | `inCode` escaped; `symbol` and `meaning` HTML |

### The marks `⟦key|text⟧`

A mark ties one quantity together across the three places it appears. `markup()` finds every `⟦key|text⟧` with the regular
expression `/⟦([A-Za-z0-9_]+)\|([^⟧]*)⟧/g` and replaces it by `<span class="k" data-k="key" tabindex="0">text</span>`
([sim.js:234-244](../../public/scripts/sim.js#L234-L244)). The key is letters, digits and underscores; the text may be anything
except `⟧`. In `code` the text inside and between the marks is escaped; in `math` it is not, so a formula can carry HTML. Each
table row carries the same `data-k` as its key ([sim.js:290](../../public/scripts/sim.js#L290)).

When the pointer is over, or the keyboard focus is on, anything with a `data-k` in the card, every element of the card with the
same key gets the class `is-lit`: the symbol in the formula, the expression in the code and the table row light up together
([sim.js:278-282](../../public/scripts/sim.js#L278-L282), [sim.js:308-313](../../public/scripts/sim.js#L308-L313);
styles at [sim.css:160-164](../../public/styles/sim.css#L160-L164)). A mark whose key has no table row in that step lights only
the formula and the code; this happens in five steps (for example `X` in [bench.js:29](../../public/scripts/walk/bench.js#L29),
`k2`, `k3`, `k4` in [pendulum.js:65](../../public/scripts/walk/pendulum.js#L65), `S1` in [slit.js:11](../../public/scripts/walk/slit.js#L11)).
Across the ten files there are 326 marks in `math` and `code`.

### Elisions in the code

A line that is only `...` stands for page lines left out; `...` inside a line stands for part of a line left out. Everything
else is copied from the page character for character, without the page's indentation.

## How `sim.js` renders a walkthrough

1. **Load.** At `DOMContentLoaded`, `boot()` reads `#walk[data-walk]`, appends a `<script charset="utf-8">` for
   `../scripts/walk/<key>.js` to the body, and on its `load` event calls `walkthrough(window.WALK[key])`
   ([sim.js:404-410](../../public/scripts/sim.js#L404-L410)). If the entry is missing, nothing is drawn
   ([sim.js:248](../../public/scripts/sim.js#L248)).
2. **Frame.** It writes the heading, the intro, the "Hold the numbers" switch, the step list (`role="tablist"`) and an empty card
   (`role="tabpanel"`) into `#walk` ([sim.js:250-254](../../public/scripts/sim.js#L250-L254)). Each step becomes a button
   numbered `01`, `02`, … ([sim.js:262-276](../../public/scripts/sim.js#L262-L276)). Arrow keys move to the previous or next
   step, Home and End to the first and last ([sim.js:266-274](../../public/scripts/sim.js#L266-L274)).
3. **One step.** `show(i)` marks the selected button, writes the card ("Step i of n", title, `where`, Algebra column with the
   formula and note, Code column, the symbol table, Previous and Next) and fills the "Now" column at once
   ([sim.js:283-307](../../public/scripts/sim.js#L283-L307)). It starts at step 1 ([sim.js:327](../../public/scripts/sim.js#L327)).
4. **The "Now" column.** Every 200 ms, `update()` calls `Sim.live()` and writes, into each cell `td[data-v="<key>"]`, the value
   for that key; a key the page does not return shows `—`, and an error in `Sim.live()` is caught and shows `—` everywhere
   ([sim.js:314-326](../../public/scripts/sim.js#L314-L326)). `Sim.live()` is defined by each page next to its own state and
   returns ready-formatted strings with units, read from the page's dataset; for example
   `t1: f4(ds.get('th1'), 'rad')` in [Double Pendulum.html:684-696](../../public/simulations/Double%20Pendulum.html#L684-L696)
   (dataset: [dataset.md](dataset.md)).
5. **Hold the numbers.** Switching it on takes one snapshot of `Sim.live()` and stops the updates; every step then shows that
   same frozen instant, so the reader can compare steps at one moment. Switching it off resumes the updates
   ([sim.js:257-261](../../public/scripts/sim.js#L257-L261), [sim.js:318-320](../../public/scripts/sim.js#L318-L320)).
6. **Fold.** Finally `Fold.walk(#walk)` makes the section a level-1 fold whose counts line reads "N steps · each formula beside
   the code that computes it and its value now" ([sim.js:328](../../public/scripts/sim.js#L328),
   [fold.js:342-350](../../public/scripts/fold.js#L342-L350); [fold.md](fold.md)).

Measured in headless Chromium, 1.5 s after load, on all ten pages: the walkthrough drew the expected number of steps, became a
fold, and `Sim.live()` returned a value for every symbol key used in any step of that page's file (19 to 30 keys per page), so no
"Now" cell stayed at `—`.

## The rule: excerpts stay identical to the page code

The Code column promises "as written in this page" ([sim.js:298](../../public/scripts/sim.js#L298)). AGENTS.md states the rule:
keep the excerpts identical to the page code when either changes. In practice:

- When you edit a page line that a walkthrough quotes, edit the excerpt in the same change, and the reverse.
- New code in the page (for example a write into the dataset) goes after a quoted line, never between two lines that an
  excerpt quotes together (AGENTS.md).
- `where` names the function and place; keep it true when code moves.
- The keys in `syms` must be keys that the page's `Sim.live()` returns. A renamed key in either file shows `—`.

Measured on 15 October 2026: with the marks removed, the 267 non-empty code lines of the ten files contain 41 lines that are
only `...` and 226 lines of code. Two of these have an inline `...` that stands between fragments of one page line:
[bench.js:101](../../public/scripts/walk/bench.js#L101) leaves out the last field, `colour: …`, of the `return { … }` in `lines()`
([wave-interference.html:737](../../public/simulations/wave-interference.html#L737)), and
[slit.js:110](../../public/scripts/walk/slit.js#L110) the end of the "Destructive" verdict line, before its semicolon
([Interactive Double-Slit Experiment Visualization.html:759](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L759)).
Searching each of the 226 in its page (each fragment between elisions in order, on one page line), all 226 are found
verbatim.

A check like this one can be re-run with a few lines of Node: evaluate each walk file with a stub `window`, strip the marks
with `/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g → '$1'`, split each code line on `...`, and look for the fragments in order on one line of
the page whose `data-walk` names the file.

## Writing a new walkthrough

1. Create `public/scripts/walk/<key>.js` with `window.WALK = window.WALK || {};` and `window.WALK.<key> = { intro, steps }`.
2. In the page, put `<section class="walk" id="walk" data-walk="<key>" aria-label="From symbols to code"></section>` where the
   walkthrough belongs (as in [Double Pendulum.html:381](../../public/simulations/Double%20Pendulum.html#L381)).
3. In the page script, define `Sim.live = function () { return { <key>: '<formatted value with unit>', … }; }`, reading every
   value from the dataset, never recomputing it.
4. Copy code lines from the page; use `...` for what you leave out; put a mark around each quantity in the formula and the
   code, and give it a row in `syms`.
5. Open the page: every step shows, every "Now" cell fills, hovering a symbol lights it in all three places.

## Contracts with other files

- **`sim.js`**: loads the file, reads `window.WALK[key]`, renders it, calls `Sim.live()` ([sim.md](sim.md)).
- **The page**: the `#walk[data-walk]` section, `Sim.live()`, and the code the excerpts quote. Each page's documentation lists
  what its `Sim.live()` returns ([../simulations/](../simulations/)).
- **`fold.js`**: folds the section ([fold.md](fold.md)).
- **`sim.css`**: the classes `walk__*`, `k`, `is-lit`, `is-held` ([sim.css:137-172](../../public/styles/sim.css#L137-L172);
  [../styles.md](../styles.md)).

## The ten files

In figure order. Lines are those of the step's `title`.

| Fig. | File (definition line) | Key | Page (`data-walk` line) | Lines / kB | Steps | Step titles |
|---|---|---|---|---|---|---|
| 1 | [circles.js](../../public/scripts/walk/circles.js#L7) | `circles` | [Circular Wave Interference Visualization.html](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L497) | 110 / 6.7 | 7 | [1 Wave number and damping](../../public/scripts/walk/circles.js#L11) · [2 Distance from a source to a grid point](../../public/scripts/walk/circles.js#L26) · [3 Amplitude and phase from one source](../../public/scripts/walk/circles.js#L42) · [4 Two maps that hold all of space](../../public/scripts/walk/circles.js#L54) · [5 The field at this instant](../../public/scripts/walk/circles.js#L66) · [6 The clock](../../public/scripts/walk/circles.js#L81) · [7 A number becomes a colour](../../public/scripts/walk/circles.js#L95) |
| 2 | [pendulum.js](../../public/scripts/walk/pendulum.js#L7) | `pendulum` | [Double Pendulum.html](../../public/simulations/Double%20Pendulum.html#L381) | 137 / 10.9 | 8 | [1 The state vector](../../public/scripts/walk/pendulum.js#L11) · [2 Angle difference and the shared denominator](../../public/scripts/walk/pendulum.js#L24) · [3 Upper angular acceleration α₁](../../public/scripts/walk/pendulum.js#L37) · [4 Lower angular acceleration α₂](../../public/scripts/walk/pendulum.js#L51) · [5 One Runge–Kutta 4 step](../../public/scripts/walk/pendulum.js#L65) · [6 How many steps per frame](../../public/scripts/walk/pendulum.js#L83) · [7 Energy as the accuracy check](../../public/scripts/walk/pendulum.js#L103) · [8 From angles to pixels](../../public/scripts/walk/pendulum.js#L122) |
| 3 | [slit.js](../../public/scripts/walk/slit.js#L7) | `slit` | [Interactive Double-Slit Experiment Visualization.html](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L538) | 118 / 8.1 | 7 | [1 Where everything sits](../../public/scripts/walk/slit.js#L11) · [2 Two paths and their exact difference](../../public/scripts/walk/slit.js#L26) · [3 The burgundy bar: point Q](../../public/scripts/walk/slit.js#L42) · [4 Phase difference and brightness](../../public/scripts/walk/slit.js#L55) · [5 Far field: the textbook curve](../../public/scripts/walk/slit.js#L71) · [6 Fringe orders on the pattern](../../public/scripts/walk/slit.js#L88) · [7 The verdict line](../../public/scripts/walk/slit.js#L104) |
| 4 | [tl.js](../../public/scripts/walk/tl.js#L7) | `tl` | [Transverse and longitudinal waves.html](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L724) | 110 / 7.5 | 7 | [1 One wave function for both rows](../../public/scripts/walk/tl.js#L11) · [2 The transverse row](../../public/scripts/walk/tl.js#L30) · [3 Where the crests are](../../public/scripts/walk/tl.js#L45) · [4 The longitudinal row](../../public/scripts/walk/tl.js#L57) · [5 Why the amplitude is capped](../../public/scripts/walk/tl.js#L71) · [6 Compressions and their shading](../../public/scripts/walk/tl.js#L82) · [7 World pixels into screen pixels](../../public/scripts/walk/tl.js#L97) |
| 5 | [water.js](../../public/scripts/walk/water.js#L7) | `water` | [water-wave.html](../../public/simulations/water-wave.html#L555) | 116 / 7.5 | 7 | [1 Pixels into metres, then ω² = gk](../../public/scripts/walk/water.js#L11) · [2 Phase speed and period](../../public/scripts/walk/water.js#L27) · [3 One parcel, one circle](../../public/scripts/walk/water.js#L42) · [4 Orbits shrink with depth](../../public/scripts/walk/water.js#L57) · [5 The surface is the top layer of parcels](../../public/scripts/walk/water.js#L72) · [6 Steepness limit](../../public/scripts/walk/water.js#L87) · [7 The clock and the picture](../../public/scripts/walk/water.js#L101) |
| 6 | [bench.js](../../public/scripts/walk/bench.js#L7) | `bench` | [wave-interference.html](../../public/simulations/wave-interference.html#L481) | 123 / 9.0 | 8 | [1 One component, and what its sliders mean](../../public/scripts/walk/bench.js#L11) · [2 Sampling the view](../../public/scripts/walk/bench.js#L29) · [3 Superposition is a plain sum](../../public/scripts/walk/bench.js#L42) · [4 Fitting the curves into their panels](../../public/scripts/walk/bench.js#L56) · [5 Beats preset](../../public/scripts/walk/bench.js#L71) · [6 Square-wave preset](../../public/scripts/walk/bench.js#L82) · [7 The spectrum](../../public/scripts/walk/bench.js#L93) · [8 A bound that always holds](../../public/scripts/walk/bench.js#L110) |
| 7 | [phasors.js](../../public/scripts/walk/phasors.js#L6) | `phasors` | [phasor-sums.html](../../public/simulations/phasor-sums.html#L652) | 134 / 8.2 | 8 | [1 One arm: a phasor](../../public/scripts/walk/phasors.js#L10) · [2 Tip to tail: the sum](../../public/scripts/walk/phasors.js#L28) · [3 The clock](../../public/scripts/walk/phasors.js#L43) · [4 When the curve closes](../../public/scripts/walk/phasors.js#L58) · [5 Rotational symmetry](../../public/scripts/walk/phasors.js#L74) · [6 Average size: Parseval](../../public/scripts/walk/phasors.js#L86) · [7 Final shape and morphing](../../public/scripts/walk/phasors.js#L98) · [8 Auto Dance: sound into radii](../../public/scripts/walk/phasors.js#L114) |
| 8 | [dft.js](../../public/scripts/walk/dft.js#L6) | `dft` | [draw-decompose.html](../../public/simulations/draw-decompose.html#L610) | 109 / 6.4 | 6 | [1 Equal arc length](../../public/scripts/walk/dft.js#L10) · [2 Remove the centre](../../public/scripts/walk/dft.js#L25) · [3 One coefficient](../../public/scripts/walk/dft.js#L41) · [4 Radius, phase and sorting](../../public/scripts/walk/dft.js#L58) · [5 Circles redraw the shape](../../public/scripts/walk/dft.js#L73) · [6 The check: Parseval](../../public/scripts/walk/dft.js#L91) |
| 9 | [driven.js](../../public/scripts/walk/driven.js#L7) | `driven` | [driven-oscillator.html](../../public/simulations/driven-oscillator.html#L458) | 121 / 7.6 | 7 | [1 From the sliders to k, c and Ω](../../public/scripts/walk/driven.js#L11) · [2 Newton’s second law, solved for the acceleration](../../public/scripts/walk/driven.js#L24) · [3 One Runge–Kutta step](../../public/scripts/walk/driven.js#L38) · [4 Store every tenth state](../../public/scripts/walk/driven.js#L55) · [5 Energy bookkeeping](../../public/scripts/walk/driven.js#L74) · [6 The exact answer, to measure the error](../../public/scripts/walk/driven.js#L89) · [7 Playback picks a stored sample](../../public/scripts/walk/driven.js#L104) |
| 10 | [turbine.js](../../public/scripts/walk/turbine.js#L7) | `turbine` | [wind-turbine.html](../../public/simulations/wind-turbine.html#L539) | 121 / 8.4 | 7 | [1 How much of the wind the blades catch](../../public/scripts/walk/turbine.js#L11) · [2 The torque of the wind](../../public/scripts/walk/turbine.js#L30) · [3 The controller sets the generator torque](../../public/scripts/walk/turbine.js#L44) · [4 Tuning the PI controller](../../public/scripts/walk/turbine.js#L61) · [5 Newton’s law for a rotation, stepped with RK4](../../public/scripts/walk/turbine.js#L74) · [6 Store every second state](../../public/scripts/walk/turbine.js#L94) · [7 Playback draws a stored sample](../../public/scripts/walk/turbine.js#L108) |

In all: 72 steps. The header comments of [dft.js:1-3](../../public/scripts/walk/dft.js#L1-L3) and
[phasors.js:1-3](../../public/scripts/walk/phasors.js#L1-L3) name their figure; the other eight carry the same general comment
([pendulum.js:1-4](../../public/scripts/walk/pendulum.js#L1-L4)).

## Notes for maintainers

1. Fixed on 2026-10-15: the transverse excerpt quotes the complete source line, without the invented comment (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
2. Because the file is loaded from the relative path `../scripts/walk/` ([sim.js:408](../../public/scripts/sim.js#L408)), a page
   that is not one folder below `public/` could not use a walkthrough without changing `sim.js` (see [sim.md](sim.md)).
3. The "Now" column is refreshed every 200 ms, 5 times a second, as long as the page is open, also while the walkthrough is
   folded away ([sim.js:326](../../public/scripts/sim.js#L326)).
4. `note` is inserted as HTML without `markup()` ([sim.js:297](../../public/scripts/sim.js#L297)), so a mark written in a note is
   not turned into a span and shows on the page as raw text. One note has one: step 6 of `tl`,
   `⟦comp|max(0, −cos(kX − ωt))⟧` ([tl.js:85](../../public/scripts/walk/tl.js#L85)). It is not counted among the 326 marks.
