# Stylesheets: `public/styles/`

Eight stylesheets, plain CSS with no build step: the files are served as written (measured on 20 October 2026: all seven of
that day are byte-identical on the live site, <https://phyeinusul.com>). The eighth, `i18n.css`, came with the German and
Arabic pages (23 October 2026); `tools/i18n/build.py` writes a right-to-left copy `<name>.rtl.css` of seven of them for the
Arabic pages, never edited by hand ([i18n.md](i18n.md)).

| File | Lines | Loaded by | Job |
|---|---|---|---|
| [`site.css`](../public/styles/site.css) | 887 | home, catalog, Portfolios | Tokens, base type, the home page (hero, timeline, plates), footer. |
| [`sim.css`](../public/styles/sim.css) | 232 | the eleven simulation pages | Tokens again, the figure, controls, readouts, walkthrough; imports KaTeX's CSS and `paper.css`. |
| [`paper.css`](../public/styles/paper.css) | 118 | simulation pages (through `sim.css`), catalog, Portfolios | Lecture notes set like LaTeX: Latin Modern, numbered equations, figures, boxes. |
| [`catalog.css`](../public/styles/catalog.css) | 574 | catalog, Portfolios | Top bar, masthead, search bar, chips, catalog entries; switches titles to Instrument Serif. |
| [`data.css`](../public/styles/data.css) | 455 | the eleven simulation pages | The data panel (a bookkeeper's ledger) and the Read values strip ([scripts/datalog.md](scripts/datalog.md)). |
| [`fold.css`](../public/styles/fold.css) | 168 | every page | Fold cards, header bands, toggles, Expand / Collapse all ([scripts/fold.md](scripts/fold.md)). |
| [`portfolio.css`](../public/styles/portfolio.css) | 292 | Portfolios | The project cards. |
| [`i18n.css`](../public/styles/i18n.css) | 59 | home, catalog, Portfolios, the eleven simulation pages | The language switch and what the German and Arabic pages need (for example the Arabic title faces). |

The pages that use them are described in [pages.md](pages.md); the fonts and KaTeX files in [assets.md](assets.md).

## Design rules

The house design, as the stylesheets implement it ([AGENTS.md](../AGENTS.md), "Design"):

- **Titles** in Instrument Serif, at weight 400 only (the font request asks for no other weight, [catalog.css:7](../public/styles/catalog.css#L7);
  a bold title would be a synthetic one).
- **Text** in IBM Plex Sans; **labels** (kickers, figure numbers, units, counts) in IBM Plex Mono, often small capitals
  by `text-transform: uppercase` and wide letter spacing.
- **Every box outlined** with a 1 px line; a wine edge (2–4 px) marks a box that holds something special (an equation, the
  abstract, an exercise). **No card shadows.**
  The Rotor Pendula study (`portfolios-src/rotor-pendula/`, its own stylesheets) goes further: every box there carries a
  left edge, coloured by what it holds ([portfolios.md, Boxes and their edges](portfolios.md#rotor-pendula-rotor-pendula)).
- **Lecture notes** set like a LaTeX document: prose and symbols in Latin Modern Roman, mathematics by KaTeX, numbered
  equations on a pale ground, figures on white plates with "Figure n" captions.
- **Colours**: paper `#f5f1ea`, ink `#1c1518`, one accent, the wine `#7a1f2b`. No colour coding of sections.

### Where the fonts come from

| Family | Source | Declared in |
|---|---|---|
| Instrument Serif (normal, italic) | self-hosted, `public/fonts/instrument-serif/`, by CSS `@import` of `fonts/instrument-plex.css` | [catalog.css:7](../public/styles/catalog.css#L7), [sim.css:7](../public/styles/sim.css#L7) |
| IBM Plex Sans (400, 500, 600, 400 italic), IBM Plex Mono (400, 500) | self-hosted, `public/fonts/ibm-plex-sans/` and `ibm-plex-mono/`, by CSS `@import` of `fonts/plex.css` or `fonts/instrument-plex.css` | [site.css:5](../public/styles/site.css#L5), [catalog.css:7](../public/styles/catalog.css#L7), [sim.css:7](../public/styles/sim.css#L7) |
| IBM Plex Serif (400–700, 400 italic) | self-hosted, `public/fonts/ibm-plex-serif/`, by CSS `@import` of `fonts/plex.css` | [site.css:5](../public/styles/site.css#L5) only |
| Latin Modern Roman (regular, italic, bold, bold italic) | self-hosted, `public/fonts/lm/lmroman10-*.woff2` (GUST font licence beside them) | `@font-face` at [paper.css:9–12](../public/styles/paper.css#L9-L12) |
| KaTeX_Main, KaTeX_Math and 18 more | self-hosted, `public/vendor/katex/fonts/*.woff2` (KaTeX 0.16.11, woff2 only) | 20 `@font-face` rules in `vendor/katex/katex.min.css`, loaded by `<link>` ([simulations.html:16](../public/simulations.html#L16), [portfolios.html:16](../public/portfolios.html#L16)) or `@import` ([sim.css:8](../public/styles/sim.css#L8)) |

Until 16 October 2026 these three families came from Google Fonts, so every visit sent the visitor's address to Google. They are
now served by the site itself: `fonts/plex.css` and `fonts/instrument-plex.css` are copies of the two Google Fonts stylesheets the
site used, with the same files and the same `unicode-range` subsets, pointing at the `.woff2` files beside them
([assets.md](assets.md#publicfonts--ibm-plex-and-instrument-serif-55-files-078-mb)). Measured in Chromium on all 15 pages before and
after the change: the same font renders every sampled element. The browser finds the font CSS only after it has fetched `site.css`,
`catalog.css` or `sim.css`, one round trip later than a `<link>` would; the security policy forbids loading fonts from any other site
([build-and-deploy.md](build-and-deploy.md#security)).

The four font stacks are tokens: `--serif`, `--sans`, `--mono` (site.css and sim.css) and `--tex` (paper.css). `--tex` is
`'Latin Modern Roman', 'KaTeX_Math', 'Times New Roman', serif` ([paper.css:15–16](../public/styles/paper.css#L15-L16)): Latin
Modern's text fonts have no Greek, so a Greek letter typed in the prose falls through to KaTeX's maths italic.

### How far each page follows the rules (measured in Chromium at 1280 px)

| Page | Titles | Shadows found |
|---|---|---|
| Home | IBM Plex Serif **600**: the `h1`, five `h2`, 21 `h3` | `.figure` (`--shadow`), `.project` and `.plate` (`--shadow-sm`), each open section card (fold.css) |
| Catalog | Instrument Serif 400 everywhere | none while the titles are closed; each open title card (fold.css) |
| Portfolios | Instrument Serif 400 everywhere | each open project card (fold.css) |
| A simulation page (Fig. 5) | Instrument Serif 400 everywhere | `.stage`, `.panel`, open lecture-note sections and the walkthrough (fold.css), `.walk__card`, the data tab and panel |

The departures are listed under [Notes for maintainers](#notes-for-maintainers).

**The Phyein Usul mark** ([assets.md](assets.md#publicimagesphyein-usul-marksvg--the-phyein-usul-logo-1-file-018-mb)) has no
rule in any stylesheet: every page sizes and places it with inline `style` attributes. On the home page it is a 217 × 120 image
link to `index.html` above the name, with a 14 px note in `var(--muted)` under it ("Phyein Usul · φύειν أصول, roots that grow. …")
([index.html:31–32](../index.html#L31-L32)). In the top bar of the catalog, Portfolios and the eleven simulation pages it is an
87 × 48 image link to the home page, set before the back link in a `span` with `display: inline-flex` and a 14 px gap
([simulations.html:33](../public/simulations.html#L33), [portfolios.html:35](../public/portfolios.html#L35),
[water-wave.html:18](../public/simulations/water-wave.html#L18)). Its strokes are `#7a1f2b` and `#4d0f18`, the values of
`--accent` and `--accent-dark`, written into the SVG itself.

## Load order and the cascade

When two rules have equal specificity the later file wins, so the order of the `<link>` tags is part of the design:

| Page | Order |
|---|---|
| [`index.html:15–15`](../index.html#L15-L15) | `site.css`, `fold.css` |
| [`simulations.html:15–18`](../public/simulations.html#L15-L18) | `site.css`, `katex.min.css`, `paper.css`, `catalog.css`, `fold.css` |
| [`portfolios.html:15–19`](../public/portfolios.html#L15-L19) | `site.css`, `katex.min.css`, `paper.css`, `catalog.css`, `portfolio.css`, `fold.css` |
| each simulation page, lines 11–13 (e.g. [water-wave.html:11–12](../public/simulations/water-wave.html#L11-L12)) | `sim.css` (which first imports the fonts, `katex.min.css` and `paper.css`), `data.css`, `fold.css` |

Three consequences:

- On the catalog and Portfolios pages `catalog.css` comes after `site.css` and redefines `--serif` as Instrument Serif
  ([catalog.css:9–11](../public/styles/catalog.css#L9-L11)), so every rule of `site.css` and `paper.css` that uses
  `var(--serif)` switches font there. The home page does not load `catalog.css` and keeps IBM Plex Serif.
- `fold.css` is always last. Its rules for the site's own structures ([fold.css:105–168](../public/styles/fold.css#L105-L168))
  override the page stylesheet once fold.js has turned a block into a fold.
- `paper.css`, `catalog.css`, `portfolio.css`, `data.css` and `fold.css` define almost no colours of their own: they read the
  tokens of `site.css` or `sim.css`.

`i18n.css` comes after `fold.css` on the three English pages and on every German and Arabic page: the language switch, the
Arabic fonts and the few right-to-left rules. Arabic pages load mirrored copies (`site.rtl.css`, `fold.rtl.css`,
`catalog.rtl.css`, `portfolio.rtl.css`, `paper.rtl.css`, `sim.rtl.css`, `data.rtl.css`) in place of the originals, made by
`tools/i18n/build.py` with rtlcss; edit the original and run the generator, never the copy ([i18n.md](i18n.md#right-to-left)).

## Design tokens

CSS custom properties, all on `:root` unless noted.

| Token | Value | Defined in | Meaning |
|---|---|---|---|
| `--paper` | `#f5f1ea` | [site.css:8](../public/styles/site.css#L8), [sim.css:12](../public/styles/sim.css#L12) | Page background. |
| `--card` | `#fffaf3` | [site.css:9](../public/styles/site.css#L9), [sim.css:13](../public/styles/sim.css#L13) | Card and panel ground. |
| `--card-soft` | `#fbf6ee` | [site.css:10](../public/styles/site.css#L10), [sim.css:14](../public/styles/sim.css#L14) | A softer ground (readouts, hover). |
| `--ink`, `--ink-2`, `--ink-3` | `#1c1518`, `#3a322e`, `#5a504b` | [site.css:11–13](../public/styles/site.css#L11-L13), [sim.css:15–17](../public/styles/sim.css#L15-L17) | Text, from strongest to weakest. |
| `--muted` | `#8b8079` | [site.css:14](../public/styles/site.css#L14), [sim.css:18](../public/styles/sim.css#L18) | Labels and captions. |
| `--rule`, `--rule-soft` | `#d9d0c2`, `#e6dfd2` | [site.css:15–16](../public/styles/site.css#L15-L16), [sim.css:19–20](../public/styles/sim.css#L19-L20) | Lines. |
| `--accent` | `#7a1f2b` | [site.css:17](../public/styles/site.css#L17), [sim.css:21](../public/styles/sim.css#L21) | The wine accent. |
| `--accent-dark`, `--accent-rose` | `#4d0f18`, `#e2a2aa` | [site.css:18–19](../public/styles/site.css#L18-L19), [sim.css:22–23](../public/styles/sim.css#L22-L23) | Hover state; selection and soft strokes. |
| `--tan`, `--tan-ink` | `#efe4c8`, `#7a4b12` | [site.css:20–21](../public/styles/site.css#L20-L21), [sim.css:24–25](../public/styles/sim.css#L24-L25) | Tags, "try this" boxes, exercise edge. |
| `--serif` | IBM Plex Serif stack (site.css); Instrument Serif stack (sim.css, catalog.css) | [site.css:22](../public/styles/site.css#L22), [sim.css:26](../public/styles/sim.css#L26), [catalog.css:10](../public/styles/catalog.css#L10) | Title face. |
| `--sans`, `--mono` | IBM Plex Sans stack, IBM Plex Mono stack | [site.css:23–24](../public/styles/site.css#L23-L24), [sim.css:27–28](../public/styles/sim.css#L27-L28) | Text and label faces. |
| `--grid` | two 1 px wine lines at 7.5 % opacity | [site.css:25–27](../public/styles/site.css#L25-L27), [sim.css:29](../public/styles/sim.css#L29) | Graph-paper background of figures. |
| `--shadow`, `--shadow-sm` | `0 14px 40px rgba(60,40,20,.12)`, `0 1px 2px rgba(60,40,20,.05)` | [site.css:28–29](../public/styles/site.css#L28-L29), [sim.css:30–31](../public/styles/sim.css#L30-L31) | Shadows (see the design rules). |
| `--tex` | Latin Modern stack | [paper.css:16](../public/styles/paper.css#L16) | Lecture-note prose and symbols. |
| `--line-strong` | `#cdc1ae` | [paper.css:17](../public/styles/paper.css#L17) | Outline of boxes and plates. |
| `--quote` | `#fbf6ee` | [paper.css:18](../public/styles/paper.css#L18) | Ground of display equations. |
| `--plate` | `#fff` | [paper.css:19](../public/styles/paper.css#L19) | Ground of figure plates. |
| `--fold-accent`, `--fold-card`, `--fold-line` | `var(--accent, #7a1f2b)`, `var(--card, #fffaf3)`, `var(--line-strong, #cdc1ae)` | [fold.css:6–8](../public/styles/fold.css#L6-L8) | The fold's colours, with fallbacks for pages without the tokens. |
| `--fold-tint`, `--fold-tint-2`, `--fold-soft-line` | the accent mixed into the card at 5 %, 3 %, 28 % (`color-mix`) | [fold.css:9–11](../public/styles/fold.css#L9-L11) | Header band grounds, the open card's outline. |
| `--fold-top` | `0px`, then set by fold.js | [fold.css:12](../public/styles/fold.css#L12), [fold.js:297](../public/scripts/fold.js#L297) | Height of a sticky full-width page bar; headers pin below it. |
| `--fold-open`, `--fold-close`, `--fold-ease` | `320ms`, `240ms`, `cubic-bezier(0.4,0,0.2,1)` | set by [fold.js:21–23](../public/scripts/fold.js#L21-L23) | One clock for fold, chevron and scroll. |
| `--head-h` | a section header's height, set per section | [fold.js:204–206](../public/scripts/fold.js#L204-L206) | Where level-2 headers pin. |
| `--dp-w` | `600px`; `640px` from 1500 px | [data.css:7–8](../public/styles/data.css#L7-L8) | Data panel width. |
| `--p`, `--c` | `50%`, `var(--accent)` on each range input | [sim.css:88](../public/styles/sim.css#L88); `--p` set by [sim.js:159](../public/scripts/sim.js#L159) | Slider fill up to the thumb. |
| `--ar`, `--ar-m` | per figure, inline `style` | e.g. [water-wave.html:45](../public/simulations/water-wave.html#L45) | Figure aspect ratio, wide and at 900 px or less. |
| `--d` | `(i mod 5) × 80 ms` per `.reveal` | [index.html:1216](../index.html#L1216) | Fade-in delay on the home page. |

Five formerly undefined tokens were replaced with their unchanged fallback colours: `--on-accent` (`#fff`, in catalog.css and
data.css), `--tag-soft` (`#f0eae0`, data.css), `--tan-line` (`#e3cfa3`, [data.css:294](../public/styles/data.css#L294)),
`--bar-bg` ([catalog.css:114](../public/styles/catalog.css#L114)) and `--accent-glow`
([catalog.css:155](../public/styles/catalog.css#L155)).

---

## `site.css` · the home page and the shared base

**Loaded by** [index.html:15](../index.html#L15), [simulations.html:15](../public/simulations.html#L15),
[portfolios.html:15](../public/portfolios.html#L15). Depends on no other file. On the catalog and Portfolios pages it supplies
the tokens, base type, links and the `footer`; `catalog.css` changes `--serif` after it.

| Purpose | Selectors | Lines |
|---|---|---|
| Fonts and tokens | `@import`, `:root` | [6–30](../public/styles/site.css#L6-L30) |
| Base | `box-sizing`; `html` (paper ground, `scroll-behavior: smooth`, `scroll-padding-top: 24px`); `body` (Plex Sans 16 px / 1.6); `h1, h2, h3` in `--serif` (no weight given, so the browser's bold applies unless a rule sets one); `p`, `a`, `::selection`, `ul` reset | [32–85](../public/styles/site.css#L32-L85) |
| Utilities | `.skip-link`, `.mono`, `.tag`, `.tag--soft` | [86–123](../public/styles/site.css#L86-L123) |
| Hero | `.hero` (two columns 1.15 : 0.85), `.hero__name` (60–124 px, weight 600), `.hero__tag` (serif italic), `.hero__meta`, `.hero__cta`; staggered `rise` animation | [126–180](../public/styles/site.css#L126-L180) |
| Buttons | `.btn` (wine, white text, lifts 1 px and gains a shadow on hover), `.btn--ghost` | [181–216](../public/styles/site.css#L181-L216) |
| Hero figure | `.figure`, `.figure__stage` (aspect 1 : 1.02, `--grid` at 24 px), `.figure__cap` | [218–272](../public/styles/site.css#L218-L272) |
| Layout and index | `.layout` (260 px + content, 64 px gap; 300 px and 56 px from 981 px), `.index` (sticky at 28 px), `.index a.active` | [275–330](../public/styles/site.css#L275-L330) |
| Sections | `.section` (104 px top padding), `.section h2` (32–46 px, weight 600, wine bar `::before` that widens from 40 to 96 px on `.is-visible`), `.section__intro` | [332–362](../public/styles/site.css#L332-L362) |
| Timeline (Positions) | `.timeline`, `.timeline__line` (grows over 1.8 s), `.entry` with its dot `::before`, `.entry--current` (pulsing `halo`), `.entry__when`, `.entry h3`, `.entry__org`, `.bullets` | [365–458](../public/styles/site.css#L365-L458) |
| Ledger (Education) | `.ledger`, `.row` (150 px date column), `.row__when`, `.row__org`, `.row__note` | [461–497](../public/styles/site.css#L461-L497) |
| Research cards | `.projects` (two columns, one at 980 px and below), `.project` (flat outlined card with a wine top edge), `.project__status`, linked title, `.project__summary`, `.project__open` | [500–560](../public/styles/site.css#L500-L560) |
| Plates | `.plates` (two columns), `.plate`, `.plate__fig` (156 px, `--grid` at 20 px), the SVG stroke classes `.ink .acc .soft .grey .acc-fill .grey-fill`, `.plate__body`, `.plate__num`, `.plate__tags`, `.plate__launch`, `.plates__more` | [550–678](../public/styles/site.css#L550-L678) |
| Skills | `.skills` (two columns of `dt` 128 px + `dd`), `.lvl` | [681–712](../public/styles/site.css#L681-L712) |
| Footer | `footer` (mono 11 px, both ends justified) | [715–730](../public/styles/site.css#L715-L730) |
| Motion | `@keyframes rise`, `fade`, `halo`; `.js .reveal` (hidden and 18 px low until `.is-visible`, delayed by `--d`) | [733–769](../public/styles/site.css#L733-L769) |

**Breakpoints.**

| Width | What changes | Lines |
|---|---|---|
| ≤ 980 px | Hero one column (figure at most 540 px wide); layout one column; the index becomes a full-width sticky bar at the top (translucent paper, blurred, links in a row that scrolls sideways, active link underlined); sections 64 px apart; research, plates and skills one column; ledger rows one column. | [772–841](../public/styles/site.css#L772-L841) |
| ≤ 480 px | Name at 56 px; skill rows stack. | [842–850](../public/styles/site.css#L842-L850) |
| reduced motion | No smooth scrolling, no hero animation, no halo, reveals shown at once. | [851–873](../public/styles/site.css#L851-L873) |

**Print** ([874–887](../public/styles/site.css#L874-L887)): hides `.index`, `.skip-link`, `.btn` and the hero `.figure`;
white page; no minimum hero height.

**After fold.js.** On the home page every `.section` becomes a fold, and [fold.css:123–127](../public/styles/fold.css#L123-L127)
removes its 104 px top padding, sets the `h2` to 26–34 px and hides the wine bar. The `.index` keeps `padding-top: 104px`; the
Expand / Collapse pair gets a 104 px top margin to match it ([fold.css:124](../public/styles/fold.css#L124)).

## `sim.css` · the simulation pages

**Loaded by** the eleven pages in `public/simulations/`, line 11 of each. It begins by importing the fonts
([7](../public/styles/sim.css#L7)), KaTeX's stylesheet ([8](../public/styles/sim.css#L8)) and `paper.css`
([9](../public/styles/sim.css#L9)), so a simulation page needs only this `<link>` for type and notes. Its tokens
([11–32](../public/styles/sim.css#L11-L32)) repeat `site.css` value for value except `--serif`, which is Instrument Serif;
`h1, h2, h3` are weight 400 ([37](../public/styles/sim.css#L37)).

| Purpose | Selectors | Lines |
|---|---|---|
| Base | box-sizing, `html`, `body`, headings, links, focus ring for links, buttons and inputs | [34–43](../public/styles/sim.css#L34-L43) |
| Top bar | `.sim-top`, `.sim-nav` (the Fig. 1–11 links; `aria-current="page"` outlined in wine) | [46–53](../public/styles/sim.css#L46-L53) |
| Page head | `.sim`, `.sim__head`, `.sim__num`, `h1` (38–66 px), `.sim__lede` (Latin Modern italic) | [56–61](../public/styles/sim.css#L56-L61) |
| Figure and panel grid | `.sim__grid` (figure + 320 px panel), `.stack` | [63–64](../public/styles/sim.css#L63-L64) |
| Figure | `.stage`, `.stage__canvas` (aspect `--ar`, graph paper), `.stage__cap` (Latin Modern caption, mono figure number, tabular digits) | [67–74](../public/styles/sim.css#L67-L74) |
| Controls | `.panel`, `.panel__group`, `.panel__label`, `.ctl`, `.ctl__row`, `.ctl output`, `.actions` | [77–85](../public/styles/sim.css#L77-L85) |
| Sliders | `input[type=range]` for WebKit and Firefox: 4 px track filled to `--p`, 16 px thumb | [88–95](../public/styles/sim.css#L88-L95) |
| Buttons | `.btn`, `.btn--ghost`, `.btn[disabled]` | [98–102](../public/styles/sim.css#L98-L102) |
| Switches | `.switch` (34 × 20 px toggle drawn from a checkbox) | [105–109](../public/styles/sim.css#L105-L109) |
| Readouts and legend | `.readouts` (two-column `dl`), `.legend`, swatches `.sw`, `.sw--dot/ink/rose/tan/dash`, `.colorbar`, `.colorbar-labels` | [112–129](../public/styles/sim.css#L112-L129) |
| Equation and error blocks | `.eq` is used by the walkthrough; `.sim-error` remains for errors; `@keyframes open` for the walkthrough card. | [131–134](../public/styles/sim.css#L131-L134) |
| Walkthrough | `.walk`, `.walk__head`, `.walk__frame` (220 px step list + card), `.walk__steps` buttons, `.walk__card`, `.walk__code pre` (ink ground), highlighted symbols `.k` / `.k.is-lit`, `.walk__table` with a pulsing "now" dot, `.walk__val`, `.walk__nav` ([scripts/walk.md](scripts/walk.md)) | [137–176](../public/styles/sim.css#L137-L176) |
| Skip link, footer, keyframes | `.skip-link`, `.sim-foot`, `rise`, `fade` | [191–192](../public/styles/sim.css#L191-L192), [205–210](../public/styles/sim.css#L205-L210) |
| Caption maths | `html:not(.tex-ready) .stage__cap .tx` hidden until KaTeX has set it (sim.js adds `tex-ready`, at the latest after 4 s, [sim.js:492–495](../public/scripts/sim.js#L492-L495)) | [228–229](../public/styles/sim.css#L228-L229) |

**Breakpoints.**

| Width | What changes | Lines |
|---|---|---|
| ≤ 900 px | Figure and panel stack; figures switch to `--ar-m`; walkthrough steps become a sideways-scrolling row above the card. | [177–182](../public/styles/sim.css#L177-L182), [213–216](../public/styles/sim.css#L213-L216) |
| ≤ 560 px | 16 px side padding; tighter cards and panel. | [183–185](../public/styles/sim.css#L183-L185), [217–222](../public/styles/sim.css#L217-L222) |
| reduced motion | No card, walkthrough or head animations. | [186–188](../public/styles/sim.css#L186-L188), [223–225](../public/styles/sim.css#L223-L225) |

**Print** ([193–202](../public/styles/sim.css#L193-L202)): hides the figure navigation, panel, walkthrough controls and the figure caption; one column; no shadows; boxes not split across pages; code on a light
ground.

## `paper.css` · the lecture notes

**Loaded by** [simulations.html:17](../public/simulations.html#L17), [portfolios.html:17](../public/portfolios.html#L17), and
through [sim.css:9](../public/styles/sim.css#L9) on every simulation page. It defines Latin Modern and four tokens, and reads
`--serif`, `--mono`, `--accent`, `--card`, `--ink…`, `--muted`, `--rule` and `--tan-ink` from the page's base sheet. The
catalog and Portfolios pages use its fonts and tokens (`--tex`, `--line-strong`, `--quote`), and Portfolios also
`.pfig__plate` and `.pfig__n`; the rest serves `<article class="paper" id="paper">` on the simulation pages, which sim.js typesets ([scripts/sim.md](scripts/sim.md)).

| Purpose | Selectors | Lines |
|---|---|---|
| Fonts and tokens | four `@font-face`, `--tex`, `--line-strong`, `--quote`, `--plate` | [9–20](../public/styles/paper.css#L9-L20) |
| The note's frame | `.paper` (its body hidden until `.is-typeset`, so raw TeX never flashes), `.paper__head`, `.paper__kicker`, `.paper__title`, `.paper__by`, `.paper__abstract` (4 px wine edge) | [23–30](../public/styles/paper.css#L23-L30) |
| Contents column | `.paper__grid` (210 px + 760 px), `.paper__toc` (sticky; `.is-here` marks the current section) | [32–38](../public/styles/paper.css#L32-L38) |
| Running text | `.paper__body` (Latin Modern 18 px / 1.72, hyphenation), lists | [41–50](../public/styles/paper.css#L41-L50) |
| Sections | `.psec`, `.psec > h3`, `.psec__n` (filled wine badge), `.psec h4`, `.psub__n`, `.psec__lead` | [51–57](../public/styles/paper.css#L51-L57) |
| Mathematics | `.paper .katex` at 1.06 em, `.katex-display` (quote ground, 2 px wine edge, scrolls sideways; room for the equation number), `.eqnote` | [60–67](../public/styles/paper.css#L60-L67) |
| Figures | `.pfig`, `.pfig__plate` (white, outlined, 12 px padding), `.pfig__row`, `figcaption`, `.pfig__n`; text classes inside inline SVG: `.m` (maths italic), `.mu` (upright), `.tick`, `.lbl`, `.acc` | [70–83](../public/styles/paper.css#L70-L83) |
| Boxes | `.pbox`, `.pbox__t`, `.pbox--ex` (exercise: tan edge), `.star` | [86–91](../public/styles/paper.css#L86-L91) |
| Tables and references | `.ptab`, `.prefs` | [94–98](../public/styles/paper.css#L94-L98) |

**Breakpoints.** ≤ 960 px: contents above the text, laid out in columns of at least 220 px
([100–104](../public/styles/paper.css#L100-L104)). ≤ 640 px: smaller abstract, body (17 px) and headings, two-figure rows stack
([105–113](../public/styles/paper.css#L105-L113)).

**Print** ([114–118](../public/styles/paper.css#L114-L118)): no contents column, one column, and the body is shown even if
KaTeX never ran.

## `catalog.css` · the catalog and the shared masthead

**Loaded by** [simulations.html:18](../public/simulations.html#L18) and [portfolios.html:18](../public/portfolios.html#L18),
after `site.css` and `paper.css` ([catalog.css:3](../public/styles/catalog.css#L3)). It needs `--line-strong`, `--quote` and
`--tex` from `paper.css` and the colour tokens from `site.css`. The Portfolios page uses its top bar, masthead and
`--serif`.

| Purpose | Selectors | Lines |
|---|---|---|
| Fonts, title face | `@import` (Instrument Serif, Plex Sans, Plex Mono), `--serif` | [8–11](../public/styles/catalog.css#L8-L11) |
| Accessibility | `.visually-hidden` (the search label) | [13–20](../public/styles/catalog.css#L13-L20) |
| Top bar | `.cat-top`, its `nav` | [23–46](../public/styles/catalog.css#L23-L46) |
| Masthead | `.cat`, `.cat__head` (text + stats), `.cat__kicker`, `h1` (56–104 px, weight 400), `.cat__lede`, `.cat__stats` | [49–105](../public/styles/catalog.css#L49-L105) |
| Search bar | `.cat__bar` (sticky, translucent, a grid with areas `search stage count` / `field field field`), `.cat__search` (icon, input, `kbd` hint hidden while typing), `.cat__filters` (`display: contents`), `.cat__chips`, `#fields`, `#stages`, `.chip` (pill; `aria-pressed="true"` turns it ink), `.chip small` (count), `.cat__count` | [108–229](../public/styles/catalog.css#L108-L229) |
| Entries | `.cat__list` (two-column grid), `.entry` (outlined card), `.entry__fig`, `.entry__plate` (8 : 5, white, outlined), `.entry__ph` (the "Fig. n" stand-in under the image), `.entry__cap`, `.entry__body`, `.entry__kicker`, `.entry h3`, `.entry__abs`, `.entry__eq` (hidden until `.is-typeset`), `.entry__facts`, `.entry__tags`, `.entry__foot`, `.entry__open`, `.entry__note` | [232–408](../public/styles/catalog.css#L232-L408) |
| Empty state | `.cat__empty` (dashed outline), its button | [411–429](../public/styles/catalog.css#L411-L429) |
| The four parts | `.cat__anatomy`, `.cat__parts` (two columns, one at 640 px and below; no native markers, margin or padding), `.cat__parts > li` (20 px padding; 18 px vertically and 16 px horizontally on phones; 3 px wine top edge) | [432–475](../public/styles/catalog.css#L432-L475) |
| No-JS notice | `.cat-error` | [480–484](../public/styles/catalog.css#L480-L484) |

**Breakpoints.**

| Width | What changes | Lines |
|---|---|---|
| ≤ 860 px | Masthead one column; list one column. | [487–495](../public/styles/catalog.css#L487-L495) |
| ≤ 640 px | 16 px side padding; the bar becomes `search count` over one sideways-scrolling row of all chips, the year chips after a thin line; smaller stats, lede and entry text; facts stack; parts one column; footer padding. | [496–566](../public/styles/catalog.css#L496-L566) |
| no hover (touch) | The `/` hint is hidden. | [567–574](../public/styles/catalog.css#L567-L574) |

No print rules.

**After fold.js.** On the catalog the list is a column of fold cards, and [fold.css:152–168](../public/styles/fold.css#L152-L168)
takes over: `.cat__list--sorted` becomes a flex column, the entry loses its own frame and lays out figure and caption left,
text right (one column at 860 px and below), its `h3` is hidden, and the timeline dot that `site.css` gives every `.entry`
is removed.

## `data.css` · the data panel

**Loaded by** the eleven simulation pages, line 12 of each, after `sim.css`. It uses the tokens of `sim.css`, `--tex` from
`paper.css`, and literal colours formerly supplied by three undefined-token fallbacks ([data.css:5](../public/styles/data.css#L5)). What the panel does
is in [scripts/datalog.md](scripts/datalog.md). Since 24 October 2026 it styles the panel as a bookkeeper: a headline of live
numbers, a toolbar, one table in causal sections and the books. On Arabic pages `data.rtl.css` (made by `rtlcss`) mirrors it,
except the alignment of numbers, which is marked `/*rtl:ignore*/` so the decimal points still line up.

| Purpose | Selectors | Lines |
|---|---|---|
| Width | `--dp-w` | [7–8](../public/styles/data.css#L7-L8) |
| The "Data" tab | `.dp-tab` (fixed to the right edge, vertical text) | [10–22](../public/styles/data.css#L10-L22) |
| The panel | `.dp` (fixed, slides in from the right; `.dp-open` on the page shows it; `container: dp`, so the table can fold by the panel's own width), `.dp__head`, `.dp__title`, `.dp__state` (pulsing dot while live or recording), `.dp__icon` | [24–54](../public/styles/data.css#L24-L54) |
| Headline | `.dp-hl` (grid of cards `.dp-hl__i`: symbol, word, value in Plex Mono, sparkline canvas `.dp-hl__sp`), `.dp-bk` (the books' summary: `is-ok`, `is-bad`, `is-na`) | [56–75](../public/styles/data.css#L56-L75) |
| Toolbar | `.dp-rec` (toolbar, round description and progress), `.dp-tools`, `.dp-tool` (`--rec` solid burgundy; `aria-pressed` for Read values), `.dp-rec__bar` | [77–97](../public/styles/data.css#L77-L97) |
| Tabs and panes | `.dp__tabs`, `.dp__count`, `.dp__body`, `.dp__pane` | [99–109](../public/styles/data.css#L99-L109) |
| Buttons | `.dp-btn`, `.dp-back`, `.dp-chk` (and its check states `is-ok` tan, `is-bad` burgundy, `is-in`/`is-na` dashed), `.dp-live` (switch) | [111–131](../public/styles/data.css#L111-L131) |
| Ledger | `.dp-instant`, `.dp-probe` (the pinned point, only while pinned), `.dp-tbl` (sticky header row; columns `.c-sym`, `.c-mean` with `.dp-f` formula, `.c-val` with `.vi`/`.vf` around the decimal point and `--frac` per section, `.c-unit`, `.c-d` (`is-up`, `is-dn`), `.c-how` with `.dp-how--set/formula/run`, `.c-chk`), row states `is-blink0/1` (one soft flash), `is-cause`, `is-effect`, `is-open`; sections `.dp-sec`, `.dp-sec__hd`, `is-folded`; array rows `.dp-r--arr` with `.dp-spk`, `.dp-cur`, `.dp-exp`; the opened array `.dp-x`, the detail row `.dp-dt` | [133–217](../public/styles/data.css#L133-L217) |
| Books | `.dp-books`, `.dp-book` (rows with sign `.b-sg`, closing line `.b-total` under a rule), `.dp-book__res` (three residual figures), `.dp-book__v` verdict | [219–241](../public/styles/data.css#L219-L241) |
| An opened array | `.dp-arr__stats`, `.dp-arr__snap`, `.dp-arr__probe`, `.dg` grid with sticky row and column headers, `.dg__c.is-hot` | [243–268](../public/styles/data.css#L243-L268) |
| Check view | `.dp-check` (stored value, formula with inputs, pixel), `.dp-check__verdict.is-ok/.is-bad/.is-na` (match, mismatch, nothing drawn to read back) | [270–297](../public/styles/data.css#L270-L297) |
| Rounds | `.dp-empty`, `.dp-rd` (chips, charts `.dp-ch`, still values, table `.dp-rd__tbl`) | [299–340](../public/styles/data.css#L299-L340) |
| Read values | `canvas.dp-overlay` (marker layer, no pointer events), `.dp-reading` (crosshair, no text selection), `.dp-readbtn` (the caption switch), `.dp-read` (the strip under the figure) | [342–368](../public/styles/data.css#L342-L368) |
| Explanation | `.dp-about` (`details` at the foot) | [370–378](../public/styles/data.css#L370-L378) |

**Breakpoints.**

| Width | What changes | Lines |
|---|---|---|
| ≥ 1500 px | Panel 640 px wide. | [8](../public/styles/data.css#L8) |
| ≥ 1360 px | While open, the page gets right padding of the panel's width instead of being covered. | [382–384](../public/styles/data.css#L382-L384) |
| ≤ 640 px | The panel becomes a bottom sheet 88 % of the screen high; the tab a pill at the bottom right that slides away (`.dp-tab--away`); the headline in three columns without words, smaller sparklines; Save as an icon; the round description hidden except while recording or while it holds the reason a round cannot start (`:has(.dp-rec__why)`); tighter tabs, charts and padding. The Read values strip gets tighter too. | [365–368](../public/styles/data.css#L365-L368), [386–433](../public/styles/data.css#L386-L433) |
| panel < 540 px | A container query on the panel: the table keeps symbol, value, unit and Δ; meaning, how and check fold into a detail row opened by a tap; the books' table drops the meaning. Holds on a phone and in any narrow window. | [435–445](../public/styles/data.css#L435-L445) |
| reduced motion | No slide, no pulsing, no progress animation, no row flash. | [446–451](../public/styles/data.css#L446-L451) |

**Print** ([452–455](../public/styles/data.css#L452-L455)): panel and tab hidden, no padding for them.

## `fold.css` · fold-out sections

**Loaded by** every page and always last: [index.html:15](../index.html#L15), [simulations.html:15](../public/simulations.html#L15),
[portfolios.html:19](../public/portfolios.html#L19), line 13 of each simulation page. The classes it styles are created by
`scripts/fold.js` ([scripts/fold.md](scripts/fold.md)); without JavaScript none of them exist and the file has no effect.
Its tokens fall back to fixed colours, so it works on the home page, which has no `--line-strong`.

| Purpose | Selectors | Lines |
|---|---|---|
| Tokens | `--fold-*` | [5–13](../public/styles/fold.css#L5-L13) |
| Level 1, the section card | `.fsec` (outlined, 4 px wine left edge, 10 px corners; open: soft outline and a shadow), `.fs-head` (tinted band; sticky at `--fold-top` while open), `.fs-main`, `.fs-side`, `.fs-counts`, `.fs-num` (wine badge) | [16–42](../public/styles/fold.css#L16-L42) |
| Toggle | `.fs-toggle` (36 px round button, filled wine when open), `.chev` (turns 180° when open) | [44–54](../public/styles/fold.css#L44-L54) |
| The body | `.fold` (a one-row grid whose row goes from `1fr` to `0fr`, so the body animates to its own height), `.fold-i` (`overflow: clip`, so headers inside can still stick), `.fs-body`; `.fold-no-anim` switches all transitions off | [57–63](../public/styles/fold.css#L57-L63) |
| Level 2, a part | `.fsub` (8 px corners; header pins at `--fold-top + --head-h`) | [66–71](../public/styles/fold.css#L66-L71) |
| Expand all / Collapse all | `.fold-tools`, `.fold-tool` (pills) | [74–79](../public/styles/fold.css#L74-L79) |
| Card details | `.fs-more` (More / Less) | [82–86](../public/styles/fold.css#L82-L86) |
| Lecture notes | `.paper .psec.fsec`, its `h3` (26–34 px), `.psec__n`, `.ppart` | [108–114](../public/styles/fold.css#L108-L114), [148–150](../public/styles/fold.css#L148-L150) |
| Walkthrough | `.walk.fsec` and its `h2` | [117–120](../public/styles/fold.css#L117-L120) |
| Home page | `.section.fsec`, `.content > .fold-tools`, the section `h2` | [123–127](../public/styles/fold.css#L123-L127), [139–141](../public/styles/fold.css#L139-L141) |
| Portfolios | `.proj.fsec` (`overflow: clip` instead of `hidden`, so the header can stick), `h2.fs-title`, `.proj__part.fsub`, the part's paragraphs and note | [130–137](../public/styles/fold.css#L130-L137) |
| Catalog | `.entry__foot .fs-more`, `.fold-tools:has(+ #catalog)`, `.cat__list--sorted`, `.simfold` and its entry layout | [144–147](../public/styles/fold.css#L144-L147), [152–168](../public/styles/fold.css#L152-L168) |

**Breakpoints.** ≤ 720 px: smaller header, toggle and body padding ([88–94](../public/styles/fold.css#L88-L94)). ≤ 980 px: the
home page's tools get a 48 px top margin instead of 104 px ([139–141](../public/styles/fold.css#L139-L141)). ≤ 860 px: catalog
entries one column ([163–167](../public/styles/fold.css#L163-L167)). Reduced motion: transitions of 0.01 ms
([95–97](../public/styles/fold.css#L95-L97)).

**Print** ([98–103](../public/styles/fold.css#L98-L103)): toggles, tools and More buttons hidden, every body open, headers
not sticky. fold.js also opens every fold and card before printing and restores them after
([fold.js:277–288](../public/scripts/fold.js#L277-L288)).

## `portfolio.css` · the project cards

**Loaded by** [portfolios.html:19](../public/portfolios.html#L19), after `catalog.css` and before `fold.css`. It defines no
tokens; it reads `--card`, `--accent`, `--line-strong`, `--quote`, `--serif`, `--tex`, `--mono`, `--sans` and the ink tokens.

| Purpose | Selectors | Lines |
|---|---|---|
| The card | `.proj` (outlined, 4 px wine left edge) | [7–14](../public/styles/portfolio.css#L7-L14) |
| Band | `.proj__band` (accent mixed 7 % into the card), `.proj__num`, the band's `p` and last `span` | [15–45](../public/styles/portfolio.css#L15-L45) |
| Head | `.proj__body`, `.proj__head` (text + tally), `.proj h2` (36–54 px), `.proj__sub`, `.proj__abs` (Latin Modern 18 px) | [46–71](../public/styles/portfolio.css#L46-L71) |
| Buttons | `.proj__actions`, `.proj__btn` (wine, arrow `→`), `.proj__btn--ghost` | [72–108](../public/styles/portfolio.css#L72-L108) |
| Key figures | `.proj__tally` (two columns with thin lines), `dt` (36 px serif), `dt.is-new` (wine), `dd` (mono) | [111–142](../public/styles/portfolio.css#L111-L142) |
| Maths size | `.proj .katex` at 1.06 em, level with Latin Modern | [145–147](../public/styles/portfolio.css#L145-L147) |
| Parts | `.proj__part`, its `h3` and `.psub__n`, `.proj__part > p` | [149–170](../public/styles/portfolio.css#L149-L170) |
| Lists and figures | `.proj__changes` (numbered 01, 02 … by a CSS counter, two columns), `.proj__figs` (two columns; plates from `paper.css`), `.proj__pages` (five columns; `.proj__pages--3`, three, for a project with three pages), `.proj__note` | [171–259](../public/styles/portfolio.css#L171-L259) |

**Breakpoints.** ≤ 1000 px: page links two per row ([261–265](../public/styles/portfolio.css#L261-L265)). ≤ 860 px: head,
changes and figures one column ([266–272](../public/styles/portfolio.css#L266-L272)). ≤ 640 px: 16 px padding, smaller numbers
and text, page links one column ([273–292](../public/styles/portfolio.css#L273-L292)). No print rules.

**After fold.js.** fold.js removes `.proj__band` and the `h2` and builds a fold header in their place (measured: no band left
with JavaScript on). So the band rules and `.proj h2` apply only without JavaScript. The paragraphs and note of a part move into
`.fs-body`, where `.proj__part > p` and `.proj__part > .proj__note` no longer match; [fold.css:136–137](../public/styles/fold.css#L136-L137)
repeats those two rules for the folded layout. Keep each pair in step.

---

## `src/styles.css` · not used

[`src/styles.css`](../src/styles.css) holds the three Tailwind directives and a placeholder comment. Its only importer is
[`src/main.ts:1`](../src/main.ts#L1), and no page loads `src/main.ts`: `index.html` has no module script
(its only scripts are [index.html:21–23](../index.html#L21-L23), [621](../index.html#L621) and
[622–1253](../index.html#L622-L1253)), and a search of the repository for `main.ts` finds only that file's own line. On the live
site <https://phyeinusul.com> `/src/main.ts` answers 404 (measured 20 October 2026). The file comes from the Vite template; see
[build-and-deploy.md](build-and-deploy.md#build-files-at-the-root).

---

## Notes for maintainers

1. **The home page breaks the house design.** It loads only `site.css`, whose `--serif` is IBM Plex Serif
   ([site.css:22](../public/styles/site.css#L22); the header comment at [site.css:3](../public/styles/site.css#L3) says so) and
   whose titles are weight 600 ([138](../public/styles/site.css#L138), [336](../public/styles/site.css#L336),
   [423](../public/styles/site.css#L423), [483](../public/styles/site.css#L483), [523](../public/styles/site.css#L523),
   [622](../public/styles/site.css#L622)). Its cards carry shadows ([222](../public/styles/site.css#L222),
   [562](../public/styles/site.css#L562), [562](../public/styles/site.css#L562); hover shadows at
   [203](../public/styles/site.css#L203), [222](../public/styles/site.css#L222), [570](../public/styles/site.css#L570)).
   When this note was written, AGENTS.md and CLAUDE.md asked for titles at weight 400 only. Since Numa's decision of
   20 October 2026 ([minor-issues-report.md](minor-issues-report.md)) they say what the code does: Instrument Serif at weight
   400 on the simulation, catalog and Portfolios pages, IBM Plex Serif at weight 600 on the home page alone (AGENTS.md, "Design";
   CLAUDE.md, "Design and explanations"). `catalog.css` redefines `--serif` as Instrument Serif after `site.css`
   ([catalog.css:9–11](../public/styles/catalog.css#L9-L11)), so `--serif` is IBM Plex Serif only on the home page and
   Instrument Serif on the other thirteen pages (catalog, Portfolios, eleven simulations).
2. **Shadows elsewhere, against the "no card shadows" comments** in [paper.css:7](../public/styles/paper.css#L7),
   [catalog.css:5](../public/styles/catalog.css#L5) and [portfolio.css:5](../public/styles/portfolio.css#L5): every open fold card
   ([fold.css:25](../public/styles/fold.css#L25)), the simulation figure and panel ([sim.css:67](../public/styles/sim.css#L67),
   [77](../public/styles/sim.css#L77)), the walkthrough card
   ([sim.css:149](../public/styles/sim.css#L149)), the data tab and panel ([data.css:17](../public/styles/data.css#L17),
   [31](../public/styles/data.css#L31)). Measured on the Portfolios page and on Fig. 5.
3. **`sim.css` repeats the tokens of `site.css`** ([sim.css:11–32](../public/styles/sim.css#L11-L32) against
   [site.css:7–30](../public/styles/site.css#L7-L30)); a colour change must be made in both.
4. Fixed on 2026-10-15: globally unused note/derivation selectors, `.sc`, `.pbox--star` and `.cat__intro` were removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)). The claim that `.eq` is unused was not reproduced: sim.js generates `class="eq walk__eq"`, and the embedded rotor project also uses it. `.eq` and the walkthrough’s `open` animation remain. Cross-file catalog overrides and the protected home wine-bar rule remain.
5. Fixed on 2026-10-15: the overridden fold display/top and phone title font-size declarations were removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
6. Fixed on 2026-10-15: the five undefined tokens were replaced with their existing fallback values; compared colours are unchanged (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
7. Fixed on 2026-10-15: an empty sorted catalog has display none and zero top margin (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
8. Fixed on 2026-10-15: the fold-tools breakpoint matches the 980 px home breakpoint; at 970 px the margin is 48 px (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
9. **One class name, two meanings.** `.entry` is a timeline entry in `site.css` ([390–437](../public/styles/site.css#L390-L437))
   and a catalog entry in `catalog.css` ([241](../public/styles/catalog.css#L241)); on the catalog page the timeline dot and
   hover colour apply to catalog entries until [fold.css:168](../public/styles/fold.css#L168) removes the dot. Likewise `site.css`'s
   `.tag` ([103–115](../public/styles/site.css#L103-L115)) would also style KaTeX's equation numbers (class `tag`) on a page that
   loads both; no such page has a numbered equation today.
10. **IBM Plex Sans and Mono are declared twice** on the catalog and Portfolios pages: `site.css` imports `fonts/plex.css` and
    `catalog.css` imports `fonts/instrument-plex.css`, and both declare those faces ([site.css:5](../public/styles/site.css#L5),
    [catalog.css:7](../public/styles/catalog.css#L7)); each of those faces appears twice in `document.fonts`. Both declarations
    point at the same files in `fonts/`.
11. Fixed on 2026-10-15: the check view has a third verdict, `.dp-check__verdict.is-na`
    ([data.css:302](../public/styles/data.css#L302)): muted ink on the soft card colour inside a dashed outline, for a read-back
    that finds nothing drawn at the moment. Before, such a case fell to the burgundy `.is-bad` (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).

## Home page proportions · 28 October 2026

`site.css`, line-neutral: the hero, the layout and the footer are at most 1100 px wide (were 1180); the index column is 260 px
(was 200) with a 64 px gap; its links are IBM Plex Sans 16 px in sentence case with 9 px rows (were IBM Plex Mono 11 px,
uppercase, tracked), the active one in wine at weight 500; on phones the index bar's links are 14 px. The bullet lines
(`.bullets li`) and project summaries are 16 px (were 14.5 and 15 px). Prose is capped at 34 em, section introductions at
30 em. Measured by `node notes/home/measure.cjs` (serve `dist/`): at 1440 px the longest line of prose fell from 101 to 72
characters (median 46), in German 71, in Arabic 79; no sideways scroll at 1920, 1440, 1280, 1024 or 390 px.

The index is a panel from 981 px wide (`site.css`, appended after `.content`), after side navigations collected by
navbar.gallery and Awwwards (oversized type, line icons, a bar that tracks reading, primary and secondary groups): an ink
panel (#1c1518, radius 18 px), entries in IBM Plex Sans 500 at 20 px, each with a Lucide line icon inlined in `index.html`
(briefcase, graduation cap, flask, atom, wrench; folder and file for Portfolios and CV); the section on screen is a wine pill,
and a pale bar along its foot fills as the reader moves through that section (`--p`, set by a short script on the line that
loads fold.js, once per animation frame while scrolling). Portfolios and CV come last, at 16 px, under a thin rule (CSS
`order`). On phones the index stays a scrolling bar, its links at 15 px with their icons.
