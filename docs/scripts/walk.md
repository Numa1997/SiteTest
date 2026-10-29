# public/scripts/walk/*.js

| | |
|---|---|
| Files | eleven files in [public/scripts/walk/](../../public/scripts/walk/), 147 to 350 lines and 15.3 to 32.9 kB each, 2 611 lines and 296 kB in all (measured 29 October 2026 with `wc -lc public/scripts/walk/*.js`; the per-file table at the end gives the sizes of 15 October) |
| Loaded by | `sim.js`, not by a `<script>` tag: once the page has loaded, `boot()` appends `../scripts/walk/<key>.js`, where `<key>` is the `data-walk` attribute of `#walk` ([sim.js:507-513](../../public/scripts/sim.js#L507-L513)); on a German or Arabic page `scripts/walk/<lang>/<key>.js`, written by `tools/i18n/build.py` ([i18n.md](../i18n.md)) |
| Defines | `window.WALK` (created if missing) and one entry `window.WALK.<key>` per file |
| Rendered by | `walkthrough()` in [sim.js:323-408](../../public/scripts/sim.js#L323-L408), described in [sim.md](sim.md) |

Each file holds the "From symbols to code" walkthrough of one simulation page: a short introduction and six to eight steps,
each pairing an equation with the exact lines of the page's own code that compute it, plus a table of the symbols with their
value in the running simulation now. The files hold data only; `sim.js` turns them into the section, and the page supplies the
live values through `Sim.live()`. The physics of each step is that of the page's lecture note, documented per page in
[../simulations/](../simulations/).

## The shared format

Every file follows the same pattern ([pendulum.js:5-29](../../public/scripts/walk/pendulum.js#L5-L29)):

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
| `intro` | string | the paragraph under the heading "From symbols to code" ([sim.js:328](../../public/scripts/sim.js#L328)) | no, HTML |
| `steps[].title` | string | the step's button in the list ("01 …") and the card heading ([sim.js:341](../../public/scripts/sim.js#L341), [sim.js:372](../../public/scripts/sim.js#L372)) | no, HTML |
| `steps[].where` | string | where in the page's code the lines are, under the heading ([sim.js:372](../../public/scripts/sim.js#L372)) | yes, plain text |
| `steps[].math` | string with marks | the "Algebra" column ([sim.js:374](../../public/scripts/sim.js#L374)) | no, HTML (`<sub>`, `<sup>`, `<b>`, `<br>`) |
| `steps[].note` | string | the paragraph under the formula ([sim.js:374](../../public/scripts/sim.js#L374)) | no, HTML |
| `steps[].code` | template literal with marks | the "Code · as written in this page" column, in `<pre><code>` ([sim.js:375](../../public/scripts/sim.js#L375)) | yes, plain text; line breaks kept |
| `steps[].syms` | array of `[key, symbol, inCode, meaning]` | one table row each: Symbol, In code, Now, Meaning ([sim.js:366-369](../../public/scripts/sim.js#L366-L369)) | `inCode` escaped; `symbol` and `meaning` HTML |

### The marks `⟦key|text⟧`

A mark ties one quantity together across the three places it appears. `markup()` finds every `⟦key|text⟧` with the regular
expression `/⟦([A-Za-z0-9_]+)\|([^⟧]*)⟧/g` and replaces it by `<span class="k" data-k="key" tabindex="0">text</span>`
([sim.js:234-244](../../public/scripts/sim.js#L234-L244)). The key is letters, digits and underscores; the text may be anything
except `⟧`. In `code` the text inside and between the marks is escaped; in `math` it is not, so a formula can carry HTML. Each
table row carries the same `data-k` as its key ([sim.js:367](../../public/scripts/sim.js#L367)).

When the pointer is over, or the keyboard focus is on, anything with a `data-k` in the card, every element of the card with the
same key gets the class `is-lit`: the symbol in the formula, the expression in the code and the table row light up together
([sim.js:355-359](../../public/scripts/sim.js#L355-L359), [sim.js:385-390](../../public/scripts/sim.js#L385-L390);
styles at [sim.css:160-164](../../public/styles/sim.css#L160-L164)). A mark whose key has no table row in that step lights only
the formula and the code; this happens in 35 of the 127 steps (counted 29 October 2026; for example `X` in
[bench.js:198](../../public/scripts/walk/bench.js#L198), `k2`, `k3`, `k4` in [pendulum.js:138](../../public/scripts/walk/pendulum.js#L138),
`A` in [circles.js:69](../../public/scripts/walk/circles.js#L69)).
Across the eleven files there are 905 marks in `math` and `code` (counted 29 October 2026, after one quoted line of Fig. 7 was removed; 326 in the ten files of 15 October).

### Elisions in the code

A line that is only `...` stands for page lines left out; `...` inside a line stands for part of a line left out. Everything
else is copied from the page character for character, without the page's indentation.

## How `sim.js` renders a walkthrough

1. **Load.** At `DOMContentLoaded`, `boot()` reads `#walk[data-walk]`, appends a `<script charset="utf-8">` for
   `../scripts/walk/<key>.js` to the body, and on its `load` event calls `walkthrough(window.WALK[key])`
   ([sim.js:507-513](../../public/scripts/sim.js#L507-L513)). If the entry is missing, nothing is drawn
   ([sim.js:325](../../public/scripts/sim.js#L325)).
2. **Frame.** It writes the heading, the intro, the "Hold the numbers" switch, the step list (`role="tablist"`) and an empty card
   (`role="tabpanel"`) into `#walk` ([sim.js:327-331](../../public/scripts/sim.js#L327-L331)). Each step becomes a button
   numbered `01`, `02`, … ([sim.js:339-353](../../public/scripts/sim.js#L339-L353)). Arrow keys move to the previous or next
   step, Home and End to the first and last ([sim.js:343-351](../../public/scripts/sim.js#L343-L351)).
3. **One step.** `show(i)` marks the selected button, writes the card ("Step i of n", title, `where`, Algebra column with the
   formula and note, Code column, the symbol table, Previous and Next) and fills the "Now" column at once
   ([sim.js:360-384](../../public/scripts/sim.js#L360-L384)). It starts at step 1 ([sim.js:404](../../public/scripts/sim.js#L404)).
4. **The "Now" column.** Every 200 ms, `update()` calls `Sim.live()` and writes, into each cell `td[data-v="<key>"]`, the value
   for that key; a key the page does not return shows `—`, and an error in `Sim.live()` is caught and shows `—` everywhere
   ([sim.js:391-403](../../public/scripts/sim.js#L391-L403)). `Sim.live()` is defined by each page next to its own state and
   returns ready-formatted strings with units, read from the page's dataset; for example
   `t1: f4(ds.get('th1'), 'rad')` in [Double Pendulum.html:746-758](../../public/simulations/Double%20Pendulum.html#L746-L758)
   (dataset: [dataset.md](dataset.md)).
5. **Hold the numbers.** Switching it on takes one snapshot of `Sim.live()` and stops the updates; every step then shows that
   same frozen instant, so the reader can compare steps at one moment. Switching it off resumes the updates
   ([sim.js:334-338](../../public/scripts/sim.js#L334-L338), [sim.js:395-397](../../public/scripts/sim.js#L395-L397)).
6. **Fold.** Finally `Fold.walk(#walk)` makes the section a level-1 fold whose counts line reads "N steps · each formula beside
   the code that computes it and its value now" ([sim.js:407](../../public/scripts/sim.js#L407),
   [fold.js:342-350](../../public/scripts/fold.js#L342-L350); [fold.md](fold.md)).

Measured in headless Chromium, 1.5 s after load, on all ten pages of the time (before Fig. 11): the walkthrough drew the expected number of steps, became a
fold, and `Sim.live()` returned a value for every symbol key used in any step of that page's file (19 to 30 keys per page), so no
"Now" cell stayed at `—`.

## The rule: excerpts stay identical to the page code

The Code column promises "as written in this page" ([sim.js:375](../../public/scripts/sim.js#L375)). AGENTS.md states the rule:
keep the excerpts identical to the page code when either changes. In practice:

- When you edit a page line that a walkthrough quotes, edit the excerpt in the same change, and the reverse.
- New code in the page (for example a write into the dataset) goes after a quoted line, never between two lines that an
  excerpt quotes together (AGENTS.md).
- `where` names the function and place; keep it true when code moves.
- The keys in `syms` must be keys that the page's `Sim.live()` returns. A renamed key in either file shows `—`.

Measured on 15 October 2026: with the marks removed, the 267 non-empty code lines of the ten files contain 41 lines that are
only `...` and 226 lines of code. Two of these have an inline `...` that stands between fragments of one page line:
[bench.js:101](../../public/scripts/walk/bench.js#L101) leaves out the last field, `colour: …`, of the `return { … }` in `lines()`
([wave-interference.html:738](../../public/simulations/wave-interference.html#L738)), and
[slit.js:164](../../public/scripts/walk/slit.js#L164) the end of the "Destructive" verdict line, before its semicolon
([Interactive Double-Slit Experiment Visualization.html:759](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L759)).
Searching each of the 226 in its page (each fragment between elisions in order, on one page line), all 226 are found
verbatim.

A check like this one can be re-run with a few lines of Node: evaluate each walk file with a stub `window`, strip the marks
with `/⟦[A-Za-z0-9_]+\|([^⟧]*)⟧/g → '$1'`, split each code line on `...`, and look for the fragments in order on one line of
the page whose `data-walk` names the file.

## Writing a new walkthrough

1. Create `public/scripts/walk/<key>.js` with `window.WALK = window.WALK || {};` and `window.WALK.<key> = { intro, steps }`.
2. In the page, put `<section class="walk" id="walk" data-walk="<key>" aria-label="From symbols to code"></section>` where the
   walkthrough belongs (as in [Double Pendulum.html:443](../../public/simulations/Double%20Pendulum.html#L443)).
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

## The eleven files

In figure order. Lines are those of the step's `title`.

| Fig. | File (definition line) | Key | Page (`data-walk` line) | Lines / kB | Steps | Step titles |
|---|---|---|---|---|---|---|
| 1 | [circles.js](../../public/scripts/walk/circles.js#L7) | `circles` | [Circular Wave Interference Visualization.html](../../public/simulations/Circular%20Wave%20Interference%20Visualization.html#L498) | 178 / 18.6 | 9 | [1 The state: sources, sliders and one phase](../../public/scripts/walk/circles.js#L11) · [2 Distance from a source to a grid point](../../public/scripts/walk/circles.js#L32) · [3 One ring: its phase kr and its height a](../../public/scripts/walk/circles.js#L53) · [4 Adding the rings: a sum of arrows](../../public/scripts/walk/circles.js#L69) · [5 The speed of each ring](../../public/scripts/walk/circles.js#L90) · [6 Two maps and a turning phase](../../public/scripts/walk/circles.js#L103) · [7 The clock, and when the maps are rebuilt](../../public/scripts/walk/circles.js#L122) · [8 The grid the maps live on](../../public/scripts/walk/circles.js#L139) · [9 A number becomes a colour](../../public/scripts/walk/circles.js#L152) |
| 2 | [pendulum.js](../../public/scripts/walk/pendulum.js#L7) | `pendulum` | [Double Pendulum.html](../../public/simulations/Double%20Pendulum.html#L443) | 224 / 30.2 | 13 | [1 The fixed numbers and the starting state](../../public/scripts/walk/pendulum.js#L11) · [2 Where the bobs are](../../public/scripts/walk/pendulum.js#L31) · [3 Kinetic and potential energy](../../public/scripts/walk/pendulum.js#L44) · [4 Generalised momenta and the matrix of (8)](../../public/scripts/walk/pendulum.js#L61) · [5 The angle between the rods and the shared denominator](../../public/scripts/walk/pendulum.js#L79) · [6 The upper angular acceleration α₁](../../public/scripts/walk/pendulum.js#L94) · [7 The lower angular acceleration α₂ and the whole right-hand side](../../public/scripts/walk/pendulum.js#L108) · [8 The chaos twin and the distance d(t)](../../public/scripts/walk/pendulum.js#L123) · [9 One Runge–Kutta step](../../public/scripts/walk/pendulum.js#L138) · [10 How many steps each frame takes](../../public/scripts/walk/pendulum.js#L156) · [11 Energy drift as the accuracy check](../../public/scripts/walk/pendulum.js#L177) · [12 From metres to pixels](../../public/scripts/walk/pendulum.js#L191) · [13 Bob sizes and the fading trail](../../public/scripts/walk/pendulum.js#L208) |
| 3 | [slit.js](../../public/scripts/walk/slit.js#L7) | `slit` | [Interactive Double-Slit Experiment Visualization.html](../../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L539) | 227 / 23.6 | 11 | [1 Where the slits and P sit · (1)](../../public/scripts/walk/slit.js#L11) · [2 Two path lengths · (2)](../../public/scripts/walk/slit.js#L35) · [3 The exact path difference · (3)](../../public/scripts/walk/slit.js#L50) · [4 The far-field shortcut · (4)](../../public/scripts/walk/slit.js#L66) · [5 The phase difference · (6)](../../public/scripts/walk/slit.js#L82) · [6 Brightness · (7)](../../public/scripts/walk/slit.js#L102) · [7 Bright and dark directions · (8), (9)](../../public/scripts/walk/slit.js#L114) · [8 The point Q: one δs, three ways](../../public/scripts/walk/slit.js#L136) · [9 The verdict under the readouts](../../public/scripts/walk/slit.js#L158) · [10 The intensity plot: 301 directions](../../public/scripts/walk/slit.js#L175) · [11 The moving wavelets](../../public/scripts/walk/slit.js#L206) |
| 4 | [tl.js](../../public/scripts/walk/tl.js#L18) | `tl` | [Transverse and longitudinal waves.html](../../public/simulations/Transverse%20and%20longitudinal%20waves.html#L725) | 226 / 23.6 | 11 | [1 The medium, its particles and the starting state](../../public/scripts/walk/tl.js#L22) · [2 Equation (1): one formula for every particle](../../public/scripts/walk/tl.js#L41) · [3 Equation (2): the pattern moves at v, and so do the crests](../../public/scripts/walk/tl.js#L61) · [4 Equation (3): how fast each particle moves](../../public/scripts/walk/tl.js#L81) · [5 Equations (5) and (9): the wave equation that (1) solves](../../public/scripts/walk/tl.js#L96) · [6 Equation (10): positions and density in the lower row](../../public/scripts/walk/tl.js#L112) · [7 Equation (11): where the compressions are](../../public/scripts/walk/tl.js#L130) · [8 Equation (12): the cap on the lower amplitude](../../public/scripts/walk/tl.js#L143) · [9 Equation (16): the clock advances the phase](../../public/scripts/walk/tl.js#L161) · [10 Equation (17): pixels of the medium into screen pixels](../../public/scripts/walk/tl.js#L175) · [11 The curve and the shading: where the picture differs from the numbers](../../public/scripts/walk/tl.js#L200) |
| 5 | [water.js](../../public/scripts/walk/water.js#L7) | `water` | [water-wave.html](../../public/simulations/water-wave.html#L557) | 216 / 22.6 | 12 | [1 What the page keeps: λ, a and the phase ωt](../../public/scripts/walk/water.js#L11) · [2 Gravity fixes the frequency: ω² = gk (13)](../../public/scripts/walk/water.js#L30) · [3 Phase speed and period (14)](../../public/scripts/walk/water.js#L47) · [4 Group speed: half the phase speed (15)](../../public/scripts/walk/water.js#L65) · [5 The velocity under the wave (16)](../../public/scripts/walk/water.js#L76) · [6 Every parcel runs on a circle (17)](../../public/scripts/walk/water.js#L92) · [7 The circles shrink with depth (18)](../../public/scripts/walk/water.js#L109) · [8 The surface is the top row of parcels (19)](../../public/scripts/walk/water.js#L128) · [9 The amplitude cap that keeps (19) from folding](../../public/scripts/walk/water.js#L144) · [10 Stokes drift: stored, not drawn (21)](../../public/scripts/walk/water.js#L161) · [11 The clock: only the phase is stepped (22)](../../public/scripts/walk/water.js#L176) · [12 From field pixels to screen pixels (23)](../../public/scripts/walk/water.js#L192) |
| 6 | [bench.js](../../public/scripts/walk/bench.js#L7) | `bench` | [wave-interference.html](../../public/simulations/wave-interference.html#L482) | 260 / 31.9 | 13 | [1 The state: four numbers per wave](../../public/scripts/walk/bench.js#L11) · [2 One wave: equation (1)](../../public/scripts/walk/bench.js#L42) · [3 Wavenumber, frequency and speed: equation (2)](../../public/scripts/walk/bench.js#L58) · [4 Waves simply add: equations (3) and (4)](../../public/scripts/walk/bench.js#L75) · [5 Two waves of one frequency: phasors, equations (5) and (6)](../../public/scripts/walk/bench.js#L94) · [6 Beats: equations (7), (8) and (9)](../../public/scripts/walk/bench.js#L110) · [7 A square wave from four sines: equations (10) and (11)](../../public/scripts/walk/bench.js#L126) · [8 The spectrum: equation (17)](../../public/scripts/walk/bench.js#L140) · [9 A ceiling that always holds: equation (19)](../../public/scripts/walk/bench.js#L159) · [10 The clock: t in equation (1)](../../public/scripts/walk/bench.js#L182) · [11 Sampling the view: one point per screen pixel](../../public/scripts/walk/bench.js#L198) · [12 From the medium to the screen: equation (20)](../../public/scripts/walk/bench.js#L217) · [13 The spectrum on screen](../../public/scripts/walk/bench.js#L243) |
| 7 | [phasors.js](../../public/scripts/walk/phasors.js#L6) | `phasors` | [phasor-sums.html](../../public/simulations/phasor-sums.html#L653) | 350 / 32.9 | 13 | [1 The state: a list of circles](../../public/scripts/walk/phasors.js#L10) · [2 One arm: a phasor](../../public/scripts/walk/phasors.js#L45) · [3 Tip to tail: the sum](../../public/scripts/walk/phasors.js#L67) · [4 When the curve closes](../../public/scripts/walk/phasors.js#L90) · [5 Rotational symmetry](../../public/scripts/walk/phasors.js#L117) · [6 The average size: Parseval](../../public/scripts/walk/phasors.js#L129) · [7 The clock: nothing is integrated](../../public/scripts/walk/phasors.js#L143) · [8 The final shape: the curve sampled at once](../../public/scripts/walk/phasors.js#L170) · [9 Morphing is a low-pass filter](../../public/scripts/walk/phasors.js#L197) · [10 The scale: fitting the curve into the canvas](../../public/scripts/walk/phasors.js#L223) · [11 Equation to screen: arms, circles, trail, pen](../../public/scripts/walk/phasors.js#L253) · [12 Auto Dance: sound into three levels and a beat](../../public/scripts/walk/phasors.js#L284) · [13 Auto Dance: levels into radii](../../public/scripts/walk/phasors.js#L323) |
| 8 | [dft.js](../../public/scripts/walk/dft.js#L6) | `dft` | [draw-decompose.html](../../public/simulations/draw-decompose.html#L611) | 212 / 24.4 | 9 | [1 The stroke, resampled at equal arc length](../../public/scripts/walk/dft.js#L10) · [2 Centring: c₀ and the mean squared radius](../../public/scripts/walk/dft.js#L37) · [3 Each circle is an average: the sums (4) and (7)](../../public/scripts/walk/dft.js#L56) · [4 One circle per coefficient, sorted by size](../../public/scripts/walk/dft.js#L79) · [5 Parseval: the share the K circles carry](../../public/scripts/walk/dft.js#L100) · [6 The error, predicted and measured: equation (9)](../../public/scripts/walk/dft.js#L117) · [7 The clock and the chain: equation (15)](../../public/scripts/walk/dft.js#L138) · [8 From units to pixels: equation (16)](../../public/scripts/walk/dft.js#L162) · [9 What is drawn: trail, circles and Fig. 8b](../../public/scripts/walk/dft.js#L187) |
| 9 | [driven.js](../../public/scripts/walk/driven.js#L13) | `driven` | [driven-oscillator.html](../../public/simulations/driven-oscillator.html#L591) | 290 / 38.9 | 14 | [1 The state and the start](../../public/scripts/walk/driven.js#L17) · [2 Equation (1): Newton’s second law](../../public/scripts/walk/driven.js#L32) · [3 Equation (2): from the sliders to k, c and Ω](../../public/scripts/walk/driven.js#L47) · [4 Equations (3) and (4): the steady state](../../public/scripts/walk/driven.js#L60) · [5 Equation (5): the exact motion from rest](../../public/scripts/walk/driven.js#L78) · [6 Equations (6) and (6a): the quality factor and the peak](../../public/scripts/walk/driven.js#L94) · [7 Equation (7): the transfer function and the Bode plot](../../public/scripts/walk/driven.js#L106) · [8 The fourth-order Runge–Kutta step (§8)](../../public/scripts/walk/driven.js#L128) · [9 Equation (8): where the energy goes](../../public/scripts/walk/driven.js#L150) · [10 Store every tenth state, and grade it against (5)](../../public/scripts/walk/driven.js#L167) · [11 Playback reads one stored row (§8)](../../public/scripts/walk/driven.js#L192) · [12 Closing the loop: the controller’s force and where the block comes to rest (§10)](../../public/scripts/walk/driven.js#L214) · [13 On screen: the coil, the forces and the block (§9, §12)](../../public/scripts/walk/driven.js#L242) · [14 On screen: the energy bars and the window chart (§12)](../../public/scripts/walk/driven.js#L269) |
| 10 | [turbine.js](../../public/scripts/walk/turbine.js#L7) | `turbine` | [wind-turbine.html](../../public/simulations/wind-turbine.html#L540) | 281 / 34.4 | 13 | [1 Power and torque of the wind · (1), (2)](../../public/scripts/walk/turbine.js#L11) · [2 Tip-speed ratio and the power coefficient · (5)](../../public/scripts/walk/turbine.js#L28) · [3 The best ratio, below the Betz limit · (4)](../../public/scripts/walk/turbine.js#L47) · [4 Newton’s second law for the rotor · (6)](../../public/scripts/walk/turbine.js#L64) · [5 The energy balance · (7)](../../public/scripts/walk/turbine.js#L83) · [6 Follow the wind: the optimal-torque law · (8)](../../public/scripts/walk/turbine.js#L107) · [7 Hold speed: the PI law · (9)](../../public/scripts/walk/turbine.js#L126) · [8 Choosing the gains · (10)](../../public/scripts/walk/turbine.js#L146) · [9 The wind, a known function of time](../../public/scripts/walk/turbine.js#L162) · [10 The start and one RK4 step](../../public/scripts/walk/turbine.js#L187) · [11 Store every second state](../../public/scripts/walk/turbine.js#L215) · [12 Play: the rotor draws a stored row](../../public/scripts/walk/turbine.js#L239) · [13 The charts and the c<sub>p</sub> figure](../../public/scripts/walk/turbine.js#L262) |
| 11 | [pendcontrol.js](../../public/scripts/walk/pendcontrol.js#L13) | `pendcontrol` | [pendulum-control.html](../../public/simulations/pendulum-control.html#L411) | 147 / 15.3 | 9 | [1 Equation (1): the coordinates and the strut](../../public/scripts/walk/pendcontrol.js#L17) · [2 Equations (5) and (6): Lagrange’s equations, solved for the accelerations](../../public/scripts/walk/pendcontrol.js#L36) · [3 Equations (2) and (3): the energy](../../public/scripts/walk/pendcontrol.js#L51) · [4 Equation (7): the rest the controller aims at](../../public/scripts/walk/pendcontrol.js#L63) · [5 Equations (9) and (10): the linear model and the controllability test](../../public/scripts/walk/pendcontrol.js#L76) · [6 Equations (12)–(14): the Riccati equation and the gains](../../public/scripts/walk/pendcontrol.js#L89) · [7 Equation (11): the control law](../../public/scripts/walk/pendcontrol.js#L103) · [8 Runge–Kutta, with the energy books carried along](../../public/scripts/walk/pendcontrol.js#L118) · [9 Solve first, store, then play](../../public/scripts/walk/pendcontrol.js#L131) |

In all: 127 steps (measured 29 October 2026). The header comments of [circles.js](../../public/scripts/walk/circles.js#L1), [tl.js](../../public/scripts/walk/tl.js#L1),
[dft.js](../../public/scripts/walk/dft.js#L1) and [phasors.js](../../public/scripts/walk/phasors.js#L1) name their figure; the other seven carry the same general comment
([pendulum.js:1-4](../../public/scripts/walk/pendulum.js#L1-L4)).

## Notes for maintainers

1. Fixed on 2026-10-15: the transverse excerpt quotes the complete source line, without the invented comment (commit [43d8238](https://github.com/Numa1997/SiteTest/commit/43d82383f4294428a1cf027f2727644ccf7dc8a5)).
2. On an English page the file is loaded from the relative path `../scripts/walk/` ([sim.js:511](../../public/scripts/sim.js#L511)), so a
   page that is not one folder below `public/` could not use a walkthrough without changing `sim.js`; a translated page loads
   `scripts/walk/<lang>/` from `ROOT` (see [sim.md](sim.md)).
3. The "Now" column is refreshed every 200 ms, 5 times a second, as long as the page is open, also while the walkthrough is
   folded away ([sim.js:403](../../public/scripts/sim.js#L403)).
4. `note` is inserted as HTML without `markup()` ([sim.js:374](../../public/scripts/sim.js#L374)), so a mark written in a note is
   not turned into a span and shows on the page as raw text. On 15 October one note had one (step 6 of `tl`); on 29 October 2026
   no note holds a mark.
