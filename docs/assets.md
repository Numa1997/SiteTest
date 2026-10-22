# Fonts, maths and pictures: `public/vendor/`, `public/fonts/`, `public/images/`

These folders hold files the site uses but does not compute: a maths typesetter, the typefaces, ten still pictures and the
Phyein Usul logo. None of them is edited by hand.

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
`auto-render.min.js` ([portfolios.html:16](../public/portfolios.html#L16), [459–460](../public/portfolios.html#L459-L460)).
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

## `public/fonts/` · IBM Plex and Instrument Serif (55 files, 0.78 MB)

The other typefaces of the house design: Instrument Serif for titles, IBM Plex Sans for text, IBM Plex Mono for labels, and IBM
Plex Serif for the titles of the home page. Until 16 October 2026 the site fetched them from Google Fonts, so every visit sent the
visitor's address to Google. Since then the site serves them itself, and the security policy refuses fonts from any other site
([build-and-deploy.md](build-and-deploy.md#security)).

| File | What it is |
|---|---|
| `plex.css` | 59 `@font-face` rules: IBM Plex Mono 400 and 500, Plex Sans 400, 500, 600 and 400 italic, Plex Serif 400, 500, 600, 700 and 400 italic. Imported by [site.css:5](../public/styles/site.css#L5). |
| `instrument-plex.css` | 38 `@font-face` rules: Instrument Serif 400 and 400 italic, Plex Sans and Plex Mono as above. Imported by [sim.css:7](../public/styles/sim.css#L7), [catalog.css:7](../public/styles/catalog.css#L7) and the stylesheets of the two project copies ([portfolios.md](portfolios.md)). |
| `ibm-plex-mono/`, `ibm-plex-sans/`, `ibm-plex-serif/`, `instrument-serif/` | 51 `.woff2` files (0.74 MB), named family, weight (`i` for italic) and script range, for example `ibm-plex-sans-400i-greek.woff2`. |
| `OFL-IBM-Plex.txt`, `OFL-Instrument-Serif.txt` | The SIL Open Font License 1.1, under which both families may be copied and served. |

The two stylesheets are copies of the two Google Fonts stylesheets the site used, with the same files and the same rules; only
the addresses point here. Each face is cut by alphabet: the `unicode-range` of a rule names the characters its file covers
(latin, latin-ext, greek, cyrillic, cyrillic-ext, vietnamese), and the browser downloads a file only when the page shows one of
those characters. A page in English with Greek symbols therefore loads the latin file and, if a Plex face must draw a Greek letter,
the greek one. Measured in Chromium: 6 to 22 faces load per page.

### Arabic faces (added 22 October 2026, on Numa's request)

The Arabic page of the iron-versus-cotton study (`portfolios/impact/ar.html`) needs Arabic letters, which IBM Plex and
Instrument Serif do not have. Numa asked for formal Arabic faces instead of IBM Plex Sans Arabic, so two were added. They are
the only fonts outside the house set, and only Arabic pages use them.

| File | What it is |
|---|---|
| `arabic.css` | 3 `@font-face` rules: Amiri 400 and 700 (titles), Noto Naskh Arabic as one variable face, weights 400 to 700 (text). Linked by [portfolios/impact/ar.html](../public/portfolios/impact/ar.html) and by [portfolios.html](../public/portfolios.html) for the two Arabic labels of project 04; its `unicode-range` means only pages that show Arabic letters download a file. |
| `amiri/amiri-400-arabic.woff2`, `amiri/amiri-700-arabic.woff2` | Amiri by Khaled Hosny, a classical Naskh, 105 and 106 kB. |
| `noto-naskh-arabic/noto-naskh-arabic-wght-arabic.woff2` | Noto Naskh Arabic by Google, variable weight, 86 kB. |
| `OFL-Amiri.txt`, `OFL-Noto-Naskh-Arabic.txt` | Their SIL Open Font License 1.1. |

Source: the TrueType files in `github.com/google/fonts` (`ofl/amiri`, `ofl/notonaskharabic`), cut with fontTools' `pyftsubset`
to the Arabic blocks (U+0600–06FF, U+0750–077F, U+0870–08FF, U+FB50–FDFF, U+FE70–FEFC and the joiners), all OpenType
features kept, saved as woff2. Each rule's `unicode-range` names the same blocks, so Latin letters and digits on the Arabic
page still come from IBM Plex.

**To refresh:** fetch the two stylesheet addresses (written at the top of each `.css` file) with the User-Agent of a current
browser (Google sends `.woff2` only to browsers that announce support), download every file they name, and point the `url(…)`
of each rule at the local name. Keep the rules and their order unchanged, so the pages render the same.

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

## `public/images/phyein-usul-mark.svg` · the Phyein Usul logo (1 file, 0.18 MB)

The mark of Phyein Usul (φύειν أصول, "roots that grow"): a fractal source with roots fading to the left and branches growing to
the right. It is a plain SVG of 1 738 paths, `viewBox="104 0 452 250"`, in the two wines `#7a1f2b` and `#4d0f18` (the values of
`--accent` and `--accent-dark`) on a transparent ground, with `role="img"` and `aria-label="Phyein Usul"`.

| Where | Size | Line |
|---|---|---|
| Home page, above the name, followed by a short note ("Phyein Usul · φύειν أصول, roots that grow. A personal website and an archive: …") | 217 × 120 | [index.html:31–32](../index.html#L31-L32) |
| Top bar of the catalog and of Portfolios, a link to the home page before "← Numa Koudsie" | 87 × 48 | [simulations.html:33](../public/simulations.html#L33), [portfolios.html:35](../public/portfolios.html#L35) |
| Top bar of each of the ten simulation pages, a link to `../index.html` before "← All simulations" | 87 × 48 | for example [water-wave.html:18](../public/simulations/water-wave.html#L18) |

No stylesheet styles it: size, spacing and the surrounding `inline-flex` span are inline `style` attributes on each page
([styles.md](styles.md#design-rules)).
