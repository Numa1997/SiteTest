# Fonts, maths and pictures: `public/vendor/`, `public/fonts/`, `public/images/`

These folders hold files the site uses but does not compute: a maths typesetter, one typeface, and ten still pictures.
None of them is edited by hand.

## `public/vendor/katex/` · the maths typesetter (24 files, 0.56 MB)

KaTeX turns LaTeX written in a page, such as `\( \omega_0 = \sqrt{k/m} \)`, into typeset mathematics in the browser, the way
LaTeX would print it on paper. It is fast because it lays out the formula once, with HTML and CSS, without waiting for the
page to finish loading. Version **0.16.11** (the string `version:"0.16.11"` in `katex.min.js`).

| File | What it is |
|---|---|
| `katex.min.js` | The typesetter itself (275 kB). Defines the global `katex`. |
| `contrib/auto-render.min.js` | The KaTeX extension that walks a part of the page and typesets every `\( … \)` (inline) and `\[ … \]` (display) it finds. Defines `renderMathInElement`. |
| `katex.min.css` | Sizes and positions of every glyph, and the `@font-face` rules for the fonts below. Reduced to woff2 only: its 20 `url(…)` entries all point at `.woff2` files (`grep -o 'url([^)]*)' public/vendor/katex/katex.min.css`). |
| `fonts/KaTeX_*.woff2` | The 20 KaTeX typefaces (Main, Math, AMS, Size1–4, Caligraphic, Fraktur, SansSerif, Script, Typewriter, in their weights). woff2 is the compressed web-font format every current browser reads. |
| `LICENSE` | MIT licence, © Khan Academy and contributors. It allows copying and serving these files with the licence kept beside them. |

**Who uses it.** The simulation pages do not list the KaTeX scripts in their HTML. `public/scripts/sim.js` loads them on
demand: first `katex.min.js`, then `auto-render.min.js`, then typesets every lecture note `.paper` on the page
([sim.js:352–353](../public/scripts/sim.js#L352-L353), and again at [sim.js:393–394](../public/scripts/sim.js#L393-L394); see
[scripts/sim.md](scripts/sim.md)). Their KaTeX stylesheet arrives through `public/styles/sim.css`, which imports it
([sim.css:8](../public/styles/sim.css#L8)). `public/simulations.html` links the stylesheet in its `<head>`
([simulations.html:16](../public/simulations.html#L16)) and loads `katex.min.js` at the end of the body
([simulations.html:125](../public/simulations.html#L125)); `public/portfolios.html` does the same and also loads
`auto-render.min.js` ([portfolios.html:16](../public/portfolios.html#L16), [268–269](../public/portfolios.html#L268)).
The home page `index.html` does not use KaTeX.

**Why it is self-hosted** rather than loaded from a public server: the pages then work offline from a saved copy, and they
do not depend on a third party being reachable. The two project copies under `public/portfolios/` carry their own KaTeX
inside their bundles ([portfolios.md](portfolios.md)).

**To upgrade:** replace all four parts together (`katex.min.js`, `katex.min.css`, `contrib/auto-render.min.js`, `fonts/`) from
the same release, cut the CSS down to woff2 again, and check a page with many equations (for example Fig. 2) for unchanged
equation numbers and spacing.

## `public/fonts/lm/` · Latin Modern Roman (5 files, 0.13 MB)

Latin Modern is the typeface of LaTeX documents: the look of a physics textbook or a thesis. The site sets its lecture notes
in it, so they read like the house LaTeX write-up.

| File | Face |
|---|---|
| `lmroman10-regular.woff2` | upright, weight 400 |
| `lmroman10-italic.woff2` | italic, weight 400 |
| `lmroman10-bold.woff2` | upright, weight 700 |
| `lmroman10-bolditalic.woff2` | italic, weight 700 |
| `GUST-FONT-LICENSE.TXT` | The GUST Font License 1.0 (Polish TeX Users Group), under which Latin Modern may be copied and served. |

They are declared as the family `'Latin Modern Roman'` by four `@font-face` rules in
[`public/styles/paper.css:9–12`](../public/styles/paper.css#L9), with `font-display: swap` (text shows at once in a fallback
serif and switches when the font arrives). See [styles.md](styles.md) for where the family is used.

The other three typefaces of the house design (Instrument Serif for titles, IBM Plex Sans for text, IBM Plex Mono for labels)
are not in this repository. The stylesheets fetch them from Google Fonts with an `@import` on their first lines
([site.css:5](../public/styles/site.css#L5), [sim.css:7](../public/styles/sim.css#L7),
[catalog.css:7](../public/styles/catalog.css#L7)); see [styles.md](styles.md).

## `public/images/sims/` · the ten thumbnails (10 files, 0.19 MB)

One still picture per simulation, used by the simulations catalog (`public/simulations.html`) and named after the catalog id
in `public/scripts/catalog.js`:

| File | Simulation |
|---|---|
| `wave-sources.webp` | Fig. 1, Wave Interference |
| `double-pendulum.webp` | Fig. 2, Double Pendulum |
| `double-slit.webp` | Fig. 3, Double-Slit Interference |
| `transverse-longitudinal.webp` | Fig. 4, Transverse & Longitudinal |
| `water-wave.webp` | Fig. 5, Circular Water Waves |
| `wave-bench.webp` | Fig. 6, Wave Interference Simulator |
| `phasor-sums.webp` | Fig. 7, Phasor Sums |
| `draw-decompose.webp` | Fig. 8, Draw & Decompose |
| `driven-oscillator.webp` | Fig. 9, Driven Oscillator |
| `wind-turbine.webp` | Fig. 10, Wind Turbine Control |

All ten are lossy WebP, 800 × 500 px (read from the files' VP8 headers). Each is a screenshot of the page's own main figure
(the element `.stage__canvas`), taken in headless Chromium at a 1440 × 900 window with device scale 2 after the simulation had
run for some seconds, then scaled to 800 × 500. The screenshot script lives in the working session for now and is to be added
to this repository. If a thumbnail is missing, the catalog shows the figure number in its place
([scripts/catalog.md](scripts/catalog.md)).

**To renew one:** run the page, take a screenshot of `.stage__canvas` at a moment that shows what the simulation is about,
scale it to 800 × 500 px, save it as WebP under the same name.

Fig. 8 was renewed on 15 October 2026 from the current stage, including the TeX Re z / Im z labels and scale.
