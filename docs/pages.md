# The site's own pages: home, simulations catalog, Portfolios, robots.txt

Four files make the frame around the eleven simulation pages:

| File | Served at | Lines | What it is |
|---|---|---|---|
| [`index.html`](../index.html) | `/` | 1255 | The home page: the Phyein Usul logo and note, CV, research, eight figure plates, a live double pendulum. |
| [`public/simulations.html`](../public/simulations.html) | `/simulations.html` | 354 | The catalog: one fold card per simulation, search, field and year chips. |
| [`public/portfolios.html`](../public/portfolios.html) | `/portfolios.html` | 439 | The four research projects and the links into their pages. |
| [`public/robots.txt`](../public/robots.txt) | `/robots.txt` | 4 | Rules for search-engine crawlers. |

The build copies everything under `public/` to the site root, so a page under `public/` links to `styles/…` and
`scripts/…` without a `public/` prefix (see [build-and-deploy.md](build-and-deploy.md)). The same folder also holds
[`public/_headers`](../public/_headers), which is not a page: Cloudflare reads it for the security headers and never serves it
(measured: `/_headers` answers 404); AppDeploy ignores it ([usul.md](usul.md)).

The site runs in two places. Checked on 14 October 2026 on the AppDeploy app
(https://numa-koudsie-website-0cyj78.v2.appdeploy.ai, [appdeploy-app.md](appdeploy-app.md)): it serves `/styles/site.css` and
the six other stylesheets and `robots.txt` byte for byte as in the repository; the three HTML pages differ only by lines the
platform injects into `<head>` (an overlay script, `og:`/`twitter:` meta tags, and on the home page also a web-app manifest and
a service-worker registration). That app is older than the repository: on 20 October 2026 its home page has no logo and no
hero note, and it sends none of the `_headers` headers. Checked on 20 October 2026 on Cloudflare (https://phyeinusul.com and
www.phyeinusul.com, [usul.md](usul.md)): the three HTML pages, the seven stylesheets and `robots.txt` are served byte for byte as
in the repository, with nothing injected. Cloudflare answers an address ending in `.html` with a 307 redirect to the same
address without it (`/simulations.html` → `/simulations`, `/index.html` → `/`), so on that host the pages' own addresses carry
no `.html`.

Related pages: the fold mechanism is in [scripts/fold.md](scripts/fold.md), the registry the catalog draws from in
[scripts/catalog.md](scripts/catalog.md), the stylesheets in [styles.md](styles.md), the project copies in
[portfolios.md](portfolios.md), fonts and KaTeX in [assets.md](assets.md).

## What the three HTML pages share

| Part | Home | Catalog | Portfolios |
|---|---|---|---|
| `<html class="no-js">`, switched to `js` by a one-line script in `<head>` | [2](../index.html#L2), [21–23](../index.html#L21-L23) | [2](../public/simulations.html#L2), [24–26](../public/simulations.html#L24-L26) | [2](../public/portfolios.html#L2), [26–28](../public/portfolios.html#L26-L28) |
| `theme-color` `#f5f1ea` (the paper colour `--paper`) | [14](../index.html#L14) | [14](../public/simulations.html#L14) | [14](../public/portfolios.html#L14) |
| Security policy and referrer rule, right after the charset line ([build-and-deploy.md](build-and-deploy.md#security)) | [5–6](../index.html#L5-L6) | [5–6](../public/simulations.html#L5-L6) | [5–6](../public/portfolios.html#L5-L6) |
| Favicon: an inline SVG, a wine square with a letter | "N" [17–20](../index.html#L17-L20) | "NK" [20–23](../public/simulations.html#L20-L23) | "NK" [22–25](../public/portfolios.html#L22-L25) |
| Skip link (`.skip-link`) | to `#main` [27](../index.html#L27) | to `#catalog` [30](../public/simulations.html#L30) | to `#projects` [32](../public/portfolios.html#L32) |
| Phyein Usul logo [`images/phyein-usul-mark.svg`](../public/images/phyein-usul-mark.svg) in an `a` to `index.html` (the eleven simulation pages carry the same 87 × 48 logo in their top bar, linking to `../index.html`) | top of the hero, 217 × 120 [31](../index.html#L31) | top bar, 87 × 48 [33](../public/simulations.html#L33) | top bar, 87 × 48 [35](../public/portfolios.html#L35) |
| `scripts/fold.js` at the end of `<body>` | [619](../index.html#L619) | [124](../public/simulations.html#L124) | [420](../public/portfolios.html#L420) |
| Footer: © line and "Back to top" | [614–616](../index.html#L614-L616) | [119–122](../public/simulations.html#L119-L122) | [415–418](../public/portfolios.html#L415-L418) |

The `js` class matters for one thing: [site.css:756–766](../public/styles/site.css#L756-L766) hides `.reveal` blocks
only under `.js`, so without JavaScript nothing waits for a fade-in.

`fold.js` runs its `boot()` at `DOMContentLoaded` ([fold.js:404–411](../public/scripts/fold.js#L404-L411)). Each page's
inline script sits after it and runs during parsing, so the inline script always runs first and fold.js then reshapes the
finished DOM. What a reader opens or closes is stored in `localStorage` under `fold:` plus the path
([fold.js:61](../public/scripts/fold.js#L61)); measured keys on AppDeploy: `fold:/` for the home page and
`fold:/simulations.html`. On phyeinusul.com the path has no `.html` (see above), so the catalog's key there is
`fold:/simulations`; the two hosts are different origins and never share stored choices anyway.

**German and Arabic.** Each of the three pages also exists at `de/…` and `ar/…`, generated from it by `tools/i18n/build.py`
([i18n.md](i18n.md)). In the English source this adds two things, each on a line that already existed so no line number above
moves: the `hreflang` alternates after the `theme-color` meta (line 14) and the language switch (English · Deutsch · العربية),
in the home page after the skip link (line 27, top right) and on the catalog and Portfolios pages at the end of the top-bar nav
(lines 38 and 40), both filled in between `<!--I18N-…-->` markers by the generator; and `styles/i18n.css` after `fold.css`.
Words that the inline scripts write go through `T('…')` and `i18n/<lang>/strings.json`.

---

## 1. `index.html` · the home page

**Purpose.** A one-page CV in the look of a physics journal: the Phyein Usul logo and a short note on what the site is, name
and tagline, a live double pendulum (Fig. 0), positions,
education, research projects, eight simulation plates and skills. It is the entry page of the site and of the Vite build.

### Head

| Lines | Item |
|---|---|
| [5–6](../index.html#L5-L6) | Security policy and referrer rule ([build-and-deploy.md](build-and-deploy.md#security)) |
| [8](../index.html#L8) | `<title>` "Numa Koudsie · Notebook" |
| [9–13](../index.html#L9-L13) | `description`, `author`, `theme-color` |
| [15](../index.html#L15) | `styles/site.css` (tokens, layout, hero, timeline, plates; imports the self-hosted IBM Plex from `fonts/plex.css`) |
| [16](../index.html#L16) | `styles/fold.css` (the fold cards) |
| [21–23](../index.html#L21-L23) | `className = 'js'` |

Scripts, in load order, at the end of `<body>`: `scripts/fold.js` ([625](../index.html#L625)), then the inline script
([622–1253](../index.html#L622-L1253)). No KaTeX, no `paper.css`: the home page has no mathematics typeset.

Fonts as measured in Chromium: IBM Plex Sans 400/500, IBM Plex Mono 400/500, IBM Plex Serif 600 (titles) and 400 italic (the
tagline). All come from this site: the `@import` in [site.css:5](../public/styles/site.css#L5) loads `fonts/plex.css`, which points at
the files in `fonts/ibm-plex-*/` ([assets.md](assets.md#publicfonts--ibm-plex-and-instrument-serif-55-files-078-mb)).

### Body, section by section

**Hero** `header.hero#top` ([29–61](../index.html#L29-L61)), a two-column grid ([site.css:126–135](../public/styles/site.css#L126-L135)):

- `.hero__text`: first the logo, an `a[href="index.html"]` around `img` `images/phyein-usul-mark.svg` at 217 × 120 css px
  ([31](../index.html#L31)), then a `p` with the note "Phyein Usul · φύειν أصول, roots that grow. A personal website and an
  archive: my work, notes and simulations kept in one place, the older pieces beside what grew from them."
  ([32](../index.html#L32)); both are styled inline, not in `site.css`. Then
  `h1.hero__name` with two `span`s and the wine `.dot` ([33–35](../index.html#L33-L35)); `.hero__tag` ([36–40](../index.html#L36-L40));
  `.hero__meta` with place, e-mail and GitHub ([41–47](../index.html#L41-L47)); `.hero__cta` with three buttons: `See positions`
  (`#positions`), `Open the simulations` (`simulations.html`), `Research portfolios` (`portfolios.html`) ([48–52](../index.html#L48-L52)).
- `figure.figure` ([54–60](../index.html#L54-L60)): `canvas#pendulum` inside `.figure__stage`, caption "Fig. 0 · double pendulum ·
  RK4 · live" and `button#pendulum-reset`.

**Layout** `div.layout` ([63–618](../index.html#L63-L618)): a 260 px column for the index and the content column, 64 px apart
([site.css:278–285](../public/styles/site.css#L278-L285)); from 981 px wide, 300 px and 56 px, at most 1160 px in all
([site.css:330](../public/styles/site.css#L330)). Measured 29 October 2026.

- `nav.index[data-fold-bar]` ([64–75](../index.html#L64-L75)): links to the five sections and `portfolios.html` ("Portfolios ↗").
  On wide screens it sticks 28 px from the top as a side column; at 980 px and below it becomes a full-width bar at the top
  ([site.css:787–797](../public/styles/site.css#L787-L797)). The attribute `data-fold-bar` lets fold.js measure it: measured
  `--fold-top` is 0 px at 1280 px (the side column does not count, [fold.js:295](../public/scripts/fold.js#L295)) and 49 px at
  900 and 390 px, so open section headers pin below the bar.
- `main.content#main` ([77–613](../index.html#L77-L613)) holds five `section.section` elements, each with an `id` and an `h2`:

| Section | Lines | Structure (classes a maintainer edits) | fold.js counts line |
|---|---|---|---|
| `#positions` "Positions" | [78–202](../index.html#L78-L202) | `.timeline` with `.timeline__line` (the wine line that grows) and seven `article.entry.reveal`: `.entry__when` (dates, optional `.tag` "current", `.tag.tag--soft`), `h3`, `.entry__org`, `ul.bullets`. The current one also has `.entry--current` (filled pulsing dot). | "7 roles" (`article.entry`) |
| `#education` "Education" | [204–233](../index.html#L204-L233) | `.ledger` with three `.row.reveal`: `.row__when`, `h3`, `.row__org`, optional `.row__note` | "3 qualifications" (`h3`) |
| `#research` "Research projects" | [235–280](../index.html#L235-L280) | `.section__intro` linking to Portfolios, `.projects` with four `article.project.reveal`: Droplet Collection, Rotor Pendula, Hydraulic Press Study, and Iron, Cotton and the Head. Each has a field label, linked title, summary and direct project link; then a `Portfolios →` button in `p.plates__more` | "4 projects" (`article`) |
| `#simulations` "Interactive physics simulations" | [277–572](../index.html#L277-L572) | `.section__intro`, `.plates` with eight `article.plate.reveal` (Figs. 1–8), then `All simulations →` | "8 figures" (`article`) |
| `#skills` "Skills & languages" | [574–612](../index.html#L574-L612) | `dl.skills`, seven `div.reveal` each with `dt` and `dd`; language levels in `span.lvl` | "7 areas" (`dt`) |

A plate ([e.g. 287–321](../index.html#L287-L321)) is `article.plate.reveal` > `div.plate__fig[data-sketch="…"]` (empty in the
HTML; the inline script draws an SVG into it) and `div.plate__body` > `p.plate__num` "Fig. n", `h3 > a` (opens the page in a new
tab), a paragraph, `.plate__tags` (three `span.tag.tag--soft`), and `a.plate__launch` "Launch". The hrefs carry the file names
with spaces as written; the browser encodes them (measured: `simulations/Circular%20Wave%20Interference%20Visualization.html`).

**What fold.js does here.** `home()` ([fold.js:353–372](../public/scripts/fold.js#L353-L372)) runs when the page has
`main .section[id]` and `.layout`. For each section it puts a two-digit number badge `span.fs-num` ("01" … "05") into the
`h2`, counts the section's items as in the table above, and calls `make()` to turn the section into a level-1 fold: the `h2`
moves into a header band `.fs-head`, everything else into `.fold > .fold-i > .fs-body`. A count that starts with "0 " is
left out. The "Expand all / Collapse all" pair goes before the first section ([fold.js:371](../public/scripts/fold.js#L371)).
All sections start open. Measured at 1280 px: five folds `positions` … `skills`, all open, with the counts listed above.
Clicking an index link opens its section first and scrolls it below the pinned header (fold.js click handler,
[fold.js:264–273](../public/scripts/fold.js#L264-L273)).

**Footer** ([616–619](../index.html#L616-L619)): "© 2026 Numa Koudsie" and `#top`.

### The inline script

One function expression wraps everything ([623–1252](../index.html#L623-L1252)). It has three independent parts.

**Fig. 0, the live double pendulum** ([628–837](../index.html#L628-L837)). The everyday picture: a pendulum hanging from the
bob of another pendulum; let it go from high up and it swings wildly, never retracing its path. The model: two point masses on
massless rigid rods, no friction, angles $\theta_1, \theta_2$ measured from the downward vertical. The code uses
$g = 9.81\ \mathrm{m/s^2}$, $m_1 = m_2 = 1\ \mathrm{kg}$, $l_1 = l_2 = 1\ \mathrm{m}$ ([634–638](../index.html#L634-L638)) and
evaluates, with $\Delta = \theta_1 - \theta_2$ and $D = 2m_1 + m_2 - m_2\cos 2\Delta$,

$$\ddot\theta_1 = \frac{-g(2m_1+m_2)\sin\theta_1 - m_2 g\sin(\theta_1 - 2\theta_2) - 2\sin\Delta\, m_2\left(\dot\theta_2^2 l_2 + \dot\theta_1^2 l_1\cos\Delta\right)}{l_1 D}$$

$$\ddot\theta_2 = \frac{2\sin\Delta\left(\dot\theta_1^2 l_1 (m_1+m_2) + g(m_1+m_2)\cos\theta_1 + \dot\theta_2^2 l_2 m_2\cos\Delta\right)}{l_2 D}$$

These are the equations of motion that follow from the Lagrangian of the double pendulum; their derivation and the full
simulation are on the Fig. 2 page ([simulations/fig02-double-pendulum.md](simulations/fig02-double-pendulum.md)). The state
$(\theta_1, \theta_2, \dot\theta_1, \dot\theta_2)$ is advanced by classical fourth-order Runge–Kutta with a fixed step
$h = 2.5\ \mathrm{ms}$. Measured with a copy of `deriv` and `rk4`: over 60 s of simulated time the total energy drifts by at most
$8.3\times10^{-7}$ of $(m_1+m_2)g l_1 + m_2 g l_2 = 29.43\ \mathrm{J}$ for five starts across the random range, so the trail
the reader sees is the motion of the model, not an artefact of the step.

| Function | Lines | What it does |
|---|---|---|
| `reduced` (value) | [624–626](../index.html#L624-L626) | True when the reader asks for reduced motion (`prefers-reduced-motion`). |
| `deriv(s)` | [655–678](../index.html#L655-L678) | The right-hand side above: returns $(\dot\theta_1, \dot\theta_2, \ddot\theta_1, \ddot\theta_2)$. |
| `rk4(s, h)` | [679–695](../index.html#L679-L695) | One RK4 step of size `h` seconds: four slopes, weighted 1, 2, 2, 1. |
| `pos(s)` | [696–705](../index.html#L696-L705) | Pixel positions of both bobs: pivot `(ox, oy)`, `scale` pixels per metre, $x = \sin\theta$, $y = \cos\theta$ (screen y points down). |
| `resize()` | [706–721](../index.html#L706-L721) | Sizes the canvas and the off-screen trail canvas to the CSS size times the device pixel ratio (capped at 2). Pivot at the centre, 36 % down; `scale` = 0.24 × the smaller side. |
| `reset()` | [722–731](../index.html#L722-L731) | New random start at rest: $\theta_1 \in [112°, 157°]$, $\theta_2 \in [135°, 207°]$ (from `Math.PI * (0.62 + 0.25 r)` and `Math.PI * (0.75 + 0.4 r)`); clears the trail. |
| `step(n, h)` | [732–747](../index.html#L732-L747) | Takes `n` RK4 steps and draws each move of the lower bob as a short wine segment (`rgba(122, 31, 43, 0.85)`, 1.4 px) on the trail canvas. |
| `fadeTrace(a)` | [748–754](../index.html#L748-L754) | Erases a fraction `a` of the trail with `destination-out`, so old trail fades. |
| `draw()` | [755–778](../index.html#L755-L778) | Clears, copies the trail, draws the rods (ink, 2.2 px), the grey pivot (3.5 px) and the wine bobs (7 and 9 px radius). |
| `frame(ts)` | [779–792](../index.html#L779-L792) | The animation loop, below. |
| `start()` | [793–798](../index.html#L793-L798) | Start the `requestAnimationFrame` loop; visibility gates the work. |
| start-up | [800–818](../index.html#L800-L818) | `resize()`, `reset()`. With reduced motion: 2600 steps of 3.5 ms (9.1 s) and one still picture, no loop. Otherwise 560 steps of 2.5 ms (1.4 s) so the trail is not empty, then `start()`; pauses while the tab is hidden (`visibilitychange`) or the canvas is off screen (`IntersectionObserver`). |
| resize handler | [819–827](../index.html#L819-L827) | 120 ms after the last resize: `resize()`, clear the trail, `draw()`. |
| reset button | [828–836](../index.html#L828-L836) | `reset()`, then the 9.1 s pre-run if motion is reduced, then `draw()`. |

The frame loop in order ([779–792](../index.html#L779-L792)): the real time since the last frame `dt` is capped at 50 ms (so
a stalled tab does not jump); simulated time `dt × SPEED` with `SPEED = 0.8` (the pendulum runs at 80 % of real speed) is added
to an accumulator; the whole number of 2.5 ms steps it holds is taken (at 60 frames per second that is 5 or 6 steps); the trail
fades by `1 − 0.99^(dt·60)`, which removes 1 % per 1/60 s whatever the frame rate (the trail halves in 69 frames, 1.15 s); then
`draw()`.

**Plate sketches** ([839–1198](../index.html#L839-L1198)). Each `div.plate__fig[data-sketch]` gets a small static SVG
(`viewBox="0 0 200 110"`). Colours come from classes styled in [site.css:590–607](../public/styles/site.css#L590-L607):
`ink`, `acc` (wine), `soft` (rose), `grey`, `acc-fill`, `grey-fill`.

| Function | Lines | What it draws |
|---|---|---|
| `sine(x0, x1, y, amp, wl, ph, st)` | [840–847](../index.html#L840-L847) | SVG path of a sine curve sampled every `st` units. |
| `svg(inner)` | [848–854](../index.html#L848-L854) | Wraps the markup in the 200 × 110 `<svg>`. |
| `sketches.interference` | [856–881](../index.html#L856-L881) | Two sources at (62, 104) and (138, 104), ten rings each, fading outward. |
| `sketches.pendulum` | [882–892](../index.html#L882-L892) | A drawn double pendulum with a dashed rose trail. |
| `sketches.doubleslit` | [893–934](../index.html#L893-L934) | Plane wavefronts, a barrier with two slits at x = 66, half-circle wavelets, and 13 screen bars of height $\propto \cos^2(0.9 i)\,e^{-\lvert i\rvert/6}$. |
| `sketches.wavetypes` | [935–954](../index.html#L935-L954) | A transverse sine (top) and 22 dots bunched by a sine (bottom): compressions. |
| `sketches.waterwave` | [955–978](../index.html#L955-L978) | Seven rings round the centre and seven small orbits with a particle on each. |
| `sketches.simulator` | [979–1009](../index.html#L979-L1009) | Two sines of wavelength 70 and 29 (top) and their sum (bottom). |
| `sketches.phasors` | [1010–1091](../index.html#L1010-L1091) | The rose $z(t) = A e^{i(4t - \pi/2)} + A e^{i(-2t + \pi/2)}$, $A = 21$, with its two arms at $t = 0.3$. |
| `sketches.fourier` | [1092–1190](../index.html#L1092-L1190) | The heart $x = 16\sin^3 u$, $y = 13\cos u - 5\cos 2u - 2\cos 3u - \cos 4u$ from its exact Fourier coefficients (the comment at 1096–1097 is correct: summing the eight terms gives back both formulas), three epicycles, and the spectrum $\lvert c_k\rvert$ for $k = -4 \dots 4$. |
| fill loop | [1192–1198](../index.html#L1192-L1198) | For each `.plate__fig[data-sketch]`, looks up the function by name and sets `innerHTML`; an unknown name leaves the plate blank. |

**Reveal on scroll and the active index link** ([1200–1251](../index.html#L1200-L1251)).

| Part | Lines | What it does |
|---|---|---|
| `io` observer | [1204–1214](../index.html#L1204-L1214) | When 10 % of an observed element is visible, adds `is-visible` once and stops watching it. |
| stagger | [1215–1218](../index.html#L1215-L1218) | Each `.reveal` gets `--d = (i mod 5) × 80 ms`, the delay its fade uses ([site.css:760–761](../public/styles/site.css#L760-L761)). |
| blocks | [1219–1221](../index.html#L1219-L1221) | `.section` and `.timeline` also get `is-visible`: the timeline line grows to full height in 1.8 s ([site.css:378–389](../public/styles/site.css#L378-L389)). |
| `nav` observer | [1223–1243](../index.html#L1223-L1243) | `rootMargin: '-30% 0px -60% 0px'` watches a band 30–40 % down the window; the section crossing it marks its `.index` link `active`. Only links starting with `#` take part. |
| fallback | [1244–1251](../index.html#L1244-L1251) | Without `IntersectionObserver`, everything is made visible at once. |

### Without JavaScript

Measured with scripting off: the root keeps `no-js`, `.reveal` blocks show at full opacity, no folds are made, the five
sections read as plain sections with their `h2` and wine bar, the index links are ordinary anchors, the hero canvas and
the eight plate figures stay empty (only the grid background shows), and everything else is complete.

### How to change it

- **Add a position.** Copy one `article.entry.reveal` inside `#positions .timeline` ([83–200](../index.html#L83-L200)).
  The list runs by end date, newest first, with the current position on top. For a current post add `entry--current` and
  `<span class="tag">current</span>`; for a label such as "during studies" add `<span class="tag tag--soft">`. The fold
  count ("n roles") updates itself.
- **Add an education row.** Copy a `.row.reveal` in `.ledger` ([207–231](../index.html#L207-L231)); `.row__note` is optional.
- **Add a research project.** Copy an `article.project.reveal` in `.projects` ([247–270](../index.html#L247-L270)); the grid
  has two columns ([site.css](../public/styles/site.css)), one at 980 px and below. Keep its title, summary and project link consistent with the actual portfolio. A finished long
  project belongs on the Portfolios page; also update the intro sentence at [237–245](../index.html#L237-L245).
- **Add a plate.** Copy an `article.plate.reveal` in `.plates` ([287–565](../index.html#L287-L565)), set `p.plate__num`, both
  hrefs and the three tags, and give `.plate__fig` a `data-sketch` name. Add a function of that name to `sketches`
  ([855–1191](../index.html#L855-L1191)) returning `svg(…)`; use the classes `ink`, `acc`, `soft`, `grey`, `acc-fill`,
  `grey-fill`. Plates are written by hand: they do not read [catalog.js](../public/scripts/catalog.js), and their titles
  differ from the catalog titles (for example "Wave Interference – Multiple Sources" against "Wave Interference").
- **Add a skill row.** Copy a `div.reveal` in `dl.skills` ([577–610](../index.html#L577-L610)).
- **Add a section.** Give it `class="section"`, an `id` and an `h2`, add its link to `nav.index`, and, for a counts line,
  a rule in `units` ([fold.js:356–362](../public/scripts/fold.js#L356-L362)); without one the header shows no counts.

---

## 2. `public/simulations.html` · the catalog

**Purpose.** The list of every simulation. It opens as a column of eleven closed titles, "01 Wave Interference" to
"10 Wind Turbine Control", in figure order. A title opens to a paper abstract: thumbnail, field and year, summary, the key
equation set by KaTeX, and links to the figure and to its lecture note. A search and two rows of chips narrow the list; the
view is kept in the address. Everything is drawn from the registry [`scripts/catalog.js`](../public/scripts/catalog.js)
(documented in [scripts/catalog.md](scripts/catalog.md)).

### Head

| Lines | Item |
|---|---|
| [5–6](../public/simulations.html#L5-L6) | Security policy and referrer rule |
| [8](../public/simulations.html#L8) | `<title>` "Simulations · Numa Koudsie" |
| [15](../public/simulations.html#L15) | `styles/site.css`: tokens, base, footer, and the IBM Plex `@import` |
| [16](../public/simulations.html#L16) | `vendor/katex/katex.min.css` (KaTeX 0.16.11, woff2 fonts only) |
| [17](../public/simulations.html#L17) | `styles/paper.css`: Latin Modern `@font-face`, `--tex`, `--line-strong`, `--quote` |
| [18](../public/simulations.html#L18) | `styles/catalog.css`: the page itself; switches `--serif` to Instrument Serif |
| [19](../public/simulations.html#L19) | `styles/fold.css`: folds, and the one-column card layout ([fold.css:152–168](../public/styles/fold.css#L152-L168)) |

Scripts at the end of `<body>`, in order: `scripts/fold.js` ([124](../public/simulations.html#L124)), `scripts/catalog.js`
([125](../public/simulations.html#L125)), `vendor/katex/katex.min.js` ([126](../public/simulations.html#L126)), the inline
script ([127–352](../public/simulations.html#L127-L352)). Fonts loaded, measured: Instrument Serif 400, IBM Plex Sans 400/500,
IBM Plex Mono 400/500, Latin Modern Roman 400 and 400 italic, and the KaTeX faces the ten equations need.

### Body

| Lines | Element | Role |
|---|---|---|
| [32–41](../public/simulations.html#L32-L41) | `header.cat-top` | The Phyein Usul logo (`images/phyein-usul-mark.svg`, 87 × 48, linking to `index.html`) and "← Numa Koudsie" in one `span` ([33](../public/simulations.html#L33)), and links to home sections and Portfolios. |
| [43–117](../public/simulations.html#L43-L117) | `main.cat` | The page column (max 1240 px). |
| [44–55](../public/simulations.html#L44-L55) | `.cat__head` | `.cat__kicker`, `h1` "Simulations.", `.cat__lede`, and `ul#stats` (filled by `stats()`). |
| [57–72](../public/simulations.html#L57-L72) | `.cat__bar[role=search][data-fold-bar]` | Sticky search bar: `input#q` (with a visually hidden label and a `/` key hint), `#fields` and `#stages` chip groups, `p#count` (`aria-live="polite"`). Measured height 104 px at 1280 px, 140 px at 900 px, 102 px at 390 px; fold.js uses it as `--fold-top`, so open titles pin below it. |
| [74–79](../public/simulations.html#L74-L79) | `noscript` | "This catalog needs JavaScript", with a link to the home page plates. |
| [81](../public/simulations.html#L81) | `div#catalog.cat__list.cat__list--sorted` | The list; filled by `render()`. |
| [83–86](../public/simulations.html#L83-L86) | `p#empty` (hidden) | "No simulation matches `b#empty-q`" and `button#clear` "Show all simulations". |
| [88–116](../public/simulations.html#L88-L116) | `section.cat__anatomy` | Static: "Every simulation, the same four parts" (figure, lecture note, walkthrough, data panel) in `ol.cat__parts[role=list]`. Only the in-card labels 01–04 are visible; native list markers and indentation are reset. Two columns, one at 640 px and below. |
| [119–122](../public/simulations.html#L119-L122) | `footer` | Links home and to Portfolios; `a#to-top`. |

**The markup one simulation becomes.** `cards()` and `entry()` build, for a registry entry `s`:

```
section.simfold#simulation-<id>  [data-counts = subject, data-label = title]     cards()  234–240
  h2.fs-title > span.fs-num "01" + title                      (moved into the fold header by fold.js)
  article.entry#sim-<id>  [data-card, data-sim, data-collapsed]                   entry()  200–229
    a.entry__fig > span.entry__plate > span.entry__ph "Fig. n" + img (images/sims/<id>.webp, 800 × 500, lazy)
    p.entry__cap   "Figure n" + subject
    div.entry__body
      p.entry__kicker   field name · first/second year
      h3 > a            title (hidden by fold.css:162; the fold header already shows it)
      p.entry__abs      summary
      div.entry__eq[data-tex]                                  (typeset by typeset())
      div.fold[data-open][inert] > div.fold-i > div.entry__more      the details behind More / Less
        dl.entry__facts   model · method · you set
        ul.entry__tags    up to six concepts
      div.entry__foot   a.entry__open "Open Fig. n" · a.entry__note "Read the lecture note" (#paper) · button.fs-more
```

There are two levels of opening. The **title fold** (the `section`) is a level-1 fold made by `Fold.make`
([245](../public/simulations.html#L245)); it starts closed, and fold.js remembers each reader's choice in `localStorage`
(measured on AppDeploy: `fold:/simulations.html` → `{"simulation-double-pendulum":1}` after opening Fig. 2). The **card details** (the
`article`, a `[data-card]`) open with More / Less ([fold.js:209–224](../public/scripts/fold.js#L209-L224)); the page keeps
that choice in `openCards` while the reader stays ([141](../public/simulations.html#L141)), across redraws, but not across a
reload (measured).

A search or a chip opens every title it finds without touching the stored choices: `folds()` passes `forceOpen` while any
filter is set ([265](../public/simulations.html#L265)). Clearing the filters shows the reader's own choices again.

### The inline script

| Function | Lines | What it does |
|---|---|---|
| set-up | [130–141](../public/simulations.html#L130-L141) | Copies `window.SIMULATIONS` to `SIMS`, reads `SIM_FIELDS` into `FIELDS`, defines `STAGES` ('1' first year, '2' second year), the shortcut `$`, the elements `q`, `list`, `count`, `empty`, `state = { q, field, stage }` and `openCards`. |
| `esc(s)` | [143–147](../public/simulations.html#L143-L147) | Escapes `& < > " '` for HTML. |
| `fold(s)` (text) | [149–154](../public/simulations.html#L149-L154) | Folds text for search (not related to `window.Fold`): lower case; Greek letters to their names (`λ` → "lambda", 12 symbols in `GREEK`); accents removed (Unicode NFD, then the combining marks U+0300–U+036F stripped); apostrophes removed; en and em dashes to `-`. So "huygens" finds "Huygens’" and "lambda" finds "λ". |
| `fieldOf(id)` | [155–158](../public/simulations.html#L155-L158) | The `SIM_FIELDS` entry for an id, or a stand-in named by the id. |
| haystack | [162–162](../public/simulations.html#L162-L162) | Builds `s._hay` once per entry: title, "fig n", "fig. n", subject, summary, model, method, controls, concepts and the field's name, folded. The TeX equation is not searched. |
| sort | [164](../public/simulations.html#L164) | Figure order (`a.fig - b.fig`). |
| `matches(s, terms, ignore)` | [166–171](../public/simulations.html#L166-L171) | True if `s` passes the field and stage filters (one of them can be ignored, for the chip counts) and every search term occurs in `_hay` as a substring (all terms must match). |
| `terms()` | [172–174](../public/simulations.html#L172-L174) | The folded search text split on white space. |
| `stats()` | [176–184](../public/simulations.html#L176-L184) | Fills `#stats`: number of simulations, of distinct fields, of course years (measured: 10, 6, 2). |
| `chips(el, items, key, all)` | [185–199](../public/simulations.html#L185-L199) | Builds one `button.chip[data-<key>]` per item plus an "All…" chip with an empty id, each with an empty `small` for its count. A click sets the filter, or clears it if that chip was already on, then `render(true)`. |
| `entry(s)` | [201–230](../public/simulations.html#L201-L230) | The `article` markup above; `encodeURI(s.file)` for the links. |
| `cards(shown)` | [235–241](../public/simulations.html#L235-L241) | Wraps each entry in its `section.simfold` with the numbered title. |
| `folds(filtering)` | [242–247](../public/simulations.html#L242-L247) | `Fold.make(section, { level: 1, head: [h2], counts: subject, label: title, defaultOpen: false, forceOpen: filtering })` for each card. Does nothing if fold.js is missing. |
| `typeset()` | [249–259](../public/simulations.html#L249-L259) | Renders each `.entry__eq` with `katex.render` in display mode (`throwOnError: false`); without KaTeX, or on an error, shows the TeX source. Adds `is-typeset`, which makes the box visible ([catalog.css:342–344](../public/styles/catalog.css#L342-L344)). |
| `render(fromUser)` | [261–290](../public/simulations.html#L261-L290) | The one redraw, in this order: filter `SIMS`; replace the list's HTML; `folds()`; `typeset()`; remove any thumbnail that fails to load, so the "Fig. n" placeholder under it shows; set each chip's `aria-pressed` and its count (how many would show if that chip were chosen, with the other filter and the search kept); write "10 shown" or "n of 10 shown"; show or hide `#empty` and word its message; save the view to the address if the reader caused the redraw. Measured: about 10 ms per redraw of all ten cards in headless Chromium. |
| `load()` | [293–302](../public/simulations.html#L293-L302) | Reads `?q=&field=&stage=` from the address. A field that is not in `SIM_FIELDS`, or a stage other than '1' or '2', is dropped. Puts `q` into the search box. |
| `save()` | [303–310](../public/simulations.html#L303-L310) | Writes the view back with `history.replaceState` (no new history entry), keeping the `#hash`. Only `q` is URI-encoded; field and stage are known ids. An empty view gives a clean address. |
| search input | [312–316](../public/simulations.html#L312-L316) | Waits 120 ms after the last key, then sets `state.q` (trimmed) and redraws. |
| Escape in the box | [317–319](../public/simulations.html#L317-L319) | Clears a non-empty search. |
| `/` anywhere | [320–326](../public/simulations.html#L320-L326) | Focuses the search, unless a modifier is held or the focus is already in a text field. |
| `#clear` | [327–332](../public/simulations.html#L327-L332) | Resets all three filters and focuses the search. |
| `#to-top` | [333–336](../public/simulations.html#L333-L336) | Scrolls to the top (the page has no element `#top`). |
| start-up | [338–350](../public/simulations.html#L338-L350) | Chips only for fields and stages that occur in `SIMS`; hooks `Fold.onCard` (record More / Less in `openCards`) and `Fold.onAll` (Expand all / Collapse all also opens or closes every card's details); `Fold.tools(list, 'before')` puts Expand all / Collapse all just above the list; then `stats()`, `load()`, `render(false)`. Last, `window.__catalog = { count, state, render }`, a handle for checking the page from the console; no file in the repository reads it. |

**The address.** Measured: opening `simulations.html?q=chaos&field=mechanics&stage=2` fills the box with "chaos", presses the
Mechanics chip, shows "1 of 10 shown" and opens the Double Pendulum title; typing "fourier" and pressing Mathematical methods
gives `?q=fourier&field=methods`; pressing that chip again gives `?q=fourier`. A deep link such as
`simulations.html#simulation-wind-turbine` opens that title on arrival (fold.js `openTo`), and fold.js stores it as opened.

**Registry fields the page reads**: `id`, `fig`, `title`, `file`, `field`, `stage`, `subject`, `summary`, `equation`,
`model`, `method`, `controls`, `concepts`, and `name` from `SIM_FIELDS`. It does not read `has`, `added`, `SIM_TOOLS` or a
field's `blurb`.

### Without JavaScript

Measured with scripting off: the `noscript` message shows; the stats, chips, count and list stay empty; the header, the
search box (inert), the "four parts" section and the footer show. The registry needs JavaScript; the page has no static
fallback list.

### How to change it

- **Add a simulation**: one entry in `SIMULATIONS` and a thumbnail; nothing in this page changes. The steps are in
  [scripts/catalog.md](scripts/catalog.md).
- **Add a field**: an entry in `SIM_FIELDS`; its chip appears once a simulation uses it ([339](../public/simulations.html#L339)).
- **Add a course year**: extend `STAGES` ([132–135](../public/simulations.html#L132-L135)) and the wording in `entry()`
  ([202](../public/simulations.html#L202)) and in the empty message ([287](../public/simulations.html#L287)), which know only
  years 1 and 2.
- **Change what a card shows**: edit `entry()`; keep `data-card`, the inner `.fold` and `button.fs-more`, which fold.js
  needs for More / Less, and keep the section's `id` (`simulation-<id>`), under which a reader's choice is stored.
- **Change the anatomy text**: plain HTML at [88–116](../public/simulations.html#L88-L116).

---

## 3. `public/portfolios.html` · the research projects

**Purpose.** Introduces the four long projects, each with an abstract, four key numbers, four numbered parts and links into
its own pages. The projects themselves are pages generated from their sources in `portfolios-src/` into
`public/portfolios/<name>/` ([portfolios.md](portfolios.md)).

### Head

Security policy and referrer rule ([5–6](../public/portfolios.html#L5-L6)), `<title>` "Portfolios · Numa Koudsie"
([8](../public/portfolios.html#L8)). Stylesheets in order
([15–21](../public/portfolios.html#L15-L21)): `site.css`, `katex.min.css`, `paper.css`, `catalog.css` (top bar, masthead,
`--serif`), `portfolio.css` (the project cards), `fold.css`, and `fonts/arabic.css` for the two Arabic labels of project 04. Scripts at the end of `<body>`: `scripts/fold.js`
([420](../public/portfolios.html#L420)), `vendor/katex/katex.min.js` ([421](../public/portfolios.html#L421)),
`vendor/katex/contrib/auto-render.min.js` ([422](../public/portfolios.html#L422)), the inline script
([423–437](../public/portfolios.html#L423-L437)).

### Body

- `header.cat-top` ([34–43](../public/portfolios.html#L34-L43)), as on the catalog (logo and "← Numa Koudsie" at
  [35](../public/portfolios.html#L35)), with Simulations instead of Portfolios.
- `main.cat#projects` ([45–413](../public/portfolios.html#L45-L413)). Its `.cat__head` has an inline style for one column
  ([46](../public/portfolios.html#L46)), since there is no stats box; kicker, `h1` "Portfolios.", lede.
- Three `article.proj` with the same structure:

| Part | Droplet Collection | Rotor Pendula | Hydraulic Press Study |
|---|---|---|---|
| `article.proj#…[aria-labelledby]` | `#droplet-collection` [59–150](../public/portfolios.html#L59-L150) | `#rotor-pendula` [152–222](../public/portfolios.html#L152-L222) | `#hydraulic-press` [224–320](../public/portfolios.html#L224-L320) |
| `.proj__band`: `span.proj__num`, a `p`, a last `span` | "01", thesis line, topics [60–64](../public/portfolios.html#L60-L64) | "02" [153–157](../public/portfolios.html#L153-L157) | "03" [225–229](../public/portfolios.html#L225-L229) |
| `.proj__head`: `h2#…-title`, `.proj__sub`, `.proj__abs`, `.proj__actions` (`a.proj__btn`, `a.proj__btn--ghost`) | [66–86](../public/portfolios.html#L66-L86) | [159–179](../public/portfolios.html#L159-L179) | [231–252](../public/portfolios.html#L231-L252) |
| `dl.proj__tally`: four `div > dt + dd`; `dt.is-new` is wine | [87–92](../public/portfolios.html#L87-L92) | [181–186](../public/portfolios.html#L181-L186) | [253–258](../public/portfolios.html#L253-L258) |
| `section.proj__part` 1: text | 1.1 "The cloud and the three questions" [95–105](../public/portfolios.html#L95-L105) | 2.1 "The answer in five lines" (`ol.proj__changes`) [189–198](../public/portfolios.html#L189-L198) | 3.1 "One press cycle, 4.4 seconds" (`ol.proj__changes`) [261–269](../public/portfolios.html#L261-L269) |
| part 2 | 1.2 "What the rebuild found" (`ol.proj__changes`) [107–116](../public/portfolios.html#L107-L116) | 2.2 "What was checked" [200–210](../public/portfolios.html#L200-L210) | 3.2 "What the model keeps" [271–286](../public/portfolios.html#L271-L286) |
| part 3: `.proj__figs`, four `figure > a.pfig__plate > img` + `figcaption` with `span.pfig__n` | [118–138](../public/portfolios.html#L118-L138) | none (removed 23 October 2026) | [288–308](../public/portfolios.html#L288-L308) |
| part 4: `ul.proj__pages` and `p.proj__note` | four pages, no note [140–148](../public/portfolios.html#L140-L148) | two pages, 2.3 [212–220](../public/portfolios.html#L212-L220) | three pages, `ul.proj__pages.proj__pages--3` [310–318](../public/portfolios.html#L310-L318) |

A fourth `article.proj#iron-cotton` (Iron, Cotton and the Head, [portfolios.html:322–412](../public/portfolios.html#L322-L412),
added 22 October 2026) has the same parts: band "04", head with two buttons (the English page and, in Arabic, the Arabic page),
tally ([350–355](../public/portfolios.html#L350-L355)), 4.1 "One drop, 9 seconds" (`ol.proj__changes`, [358–366](../public/portfolios.html#L358-L366)),
4.2 "What the model keeps" ([368–379](../public/portfolios.html#L368-L379)), 4.3 four figures ([381–401](../public/portfolios.html#L381-L401)) and
4.4 two pages in a plain `ul.proj__pages` ([403–410](../public/portfolios.html#L403-L410)); the Arabic item carries `lang="ar" dir="rtl"`.

Each part's `h3` carries an `id` (`dc-cloud`, `dc-changes`, … `rp-pages`, … `hp-pages`, … `ic-pages`) and a `span.psub__n` number.

**Links into the copies.** Every link goes to `portfolios/<name>/index.html` or `portfolios/<name>/index.html#/<route>`
(for Rotor Pendula since 23 October 2026: `index.html` and `index.html#sim`), never to the folder: the copies are single-page apps with hash routes, and AppDeploy used to answer a folder address with
403 ([AGENTS.md:55–56](../AGENTS.md#L55-L56), which still says so). Measured on 20 October 2026, both hosts answer `portfolios/rotor-pendula/` with
the copy (AppDeploy 200; Cloudflare 200, and it redirects `…/index.html` there with a 307, keeping the `#/route`), so the file
links work everywhere. No project uses app routes any more (both app copies were replaced by generated pages on 23 October 2026). The Hydraulic Press Study is not an app with routes but one page
with three tabs; its links use `portfolios/hydraulics/index.html#servo`, `#ideal` and `#theory`, which its tab bar reads on
load ([portfolios.md](portfolios.md#the-hydraulic-press-study-hydraulics)). All three copies link back with `href="../../portfolios.html"`, and so do the two pages of Iron, Cotton and the Head (`portfolios/impact/index.html`, `ar.html`), which also link to each other.
The figure images come from each copy's `fig/` folder (for example
[`portfolios/droplet-collection/fig/plate-fallspeed.svg`](../public/portfolios/droplet-collection/fig/plate-fallspeed.svg), written by the
Droplet Collection build). Droplet Collection, since 23 October 2026 one generated page like the Hydraulic Press Study, is linked at
`#book`, `#sim`, `#checks` and at four figure ids (`#fig-2-1`, `#fig-3-2`, `#fig-5-2`, `#fig-6-1`), which open their tab
([portfolios.md](portfolios.md#droplet-collection-droplet-collection-since-23-october-2026)).

**Image sizes.** Every one of the twelve figure `img` tags carries `width` and `height` in CSS px: the picture's own proportions at a
height of 300 px, rounded to whole pixels. The browser uses them to reserve the right box before the picture arrives; the
stylesheet then sets `width: 100%; height: auto` ([portfolio.css:210–214](../public/styles/portfolio.css#L210-L214)). Without
the stylesheet the picture shows at exactly these sizes. Droplet Collection
([portfolios.html:122](../public/portfolios.html#L122), [126](../public/portfolios.html#L126),
[130](../public/portfolios.html#L130), [134](../public/portfolios.html#L134)), since 23 October 2026 the four plates written by its
build, all with the `viewBox` of the notes' charts:

| Picture | SVG `viewBox` (px) | `width` × `height` (css px) | Ratio error from rounding |
|---|---|---|---|
| `plate-fallspeed.svg`, `plate-efficiency.svg`, `plate-warm.svg`, `plate-first.svg` | 600 × 330 | 545 × 300 | −0.08 % |

Rotor Pendula's article has no figures since 23 October 2026.
The Hydraulic Press Study's four are WebP screenshots of its own page, stored 600 px high for sharp display on high-density
screens: 420, 462, 748 and 631 × 300 ([292](../public/portfolios.html#L292), [296](../public/portfolios.html#L296),
[300](../public/portfolios.html#L300), [304](../public/portfolios.html#L304)).
Iron, Cotton and the Head's four are WebP screenshots of its English page made by `portfolios-src/impact/checks/plates.cjs`, stored
600 px high: 409, 626, 734 and 409 × 300 ([385](../public/portfolios.html#L385), [389](../public/portfolios.html#L389),
[393](../public/portfolios.html#L393), [397](../public/portfolios.html#L397)).

**What fold.js does here.** `portfolios()` ([fold.js:375–396](../public/scripts/fold.js#L375-L396)): every `.proj__part`
becomes a level-2 fold with its `h3` as header and gets the id `<project id>-part-<n>` when it has none (measured:
`droplet-collection-part-1` … `-4`, `rotor-pendula-part-1` … `-4`, `hydraulic-press-part-1` … `-4`). Then the band and the `h2` are removed and replaced by a
new `h2.fs-title` with the same id (`dc-title`, `rp-title`, `hp-title`) and the number badge; the band's `p` and last `span` become the
fold's counts line ("Bachelor thesis, Leipzig 2022 · remodelled · cloud physics · …"). The project becomes a level-1 fold;
Expand all / Collapse all goes before the first project. All start open.

### The inline script

| Function | Lines | What it does |
|---|---|---|
| maths | [426–431](../public/portfolios.html#L426-L431) | `renderMathInElement` (KaTeX auto-render) over `#projects`, with `\[ … \]` for display and `\( … \)` for inline maths, `throwOnError: false`. Measured: 33 formulas typeset. It runs before fold.js reshapes the page, so the folds hold typeset maths. |
| `#to-top` | [432–435](../public/portfolios.html#L432-L435) | Scrolls to the top (there is no `#top` element). |

### Without JavaScript

Measured with scripting off: all three projects read in full with their bands, numbers, figures and links; no folds; the maths
shows as TeX source between `\(` and `\)` (eight such formulas in part 1.1 alone).

### How to add a project

1. Put the static copy under `public/portfolios/<name>/` as described in [portfolios.md](portfolios.md) (build folder
   `static/`, stylesheet added by script, back link `../../portfolios.html`).
2. Copy one `article.proj` block; give it a new `id` and `aria-labelledby`, a new `h2` id, `span.proj__num` "04", the band's
   `p` and last `span` (they become the counts line), the abstract, the four `dt`/`dd` pairs and the buttons.
3. Number the parts `3.1`, `3.2`, … in `span.psub__n`; give each `h3` an `id` and the `section` an `aria-labelledby`.
4. Link only to `portfolios/<name>/index.html#/<route>` and take figures from `portfolios/<name>/fig/`; give each `img` the
   `width` and `height` of the picture's own proportions in CSS px, at a height of 300, never the raw `viewBox` numbers
   (see **Image sizes** above).
5. Update the page `description` ([11](../public/portfolios.html#L11)) and the home page's research intro
   ([index.html:237–245](../index.html#L237-L245)), which name the projects.

`.proj__pages` lays out five links per row ([portfolio.css:220–227](../public/styles/portfolio.css#L220-L227)); a sixth
wraps to a second row, as Rotor Pendula's does. A project with three pages adds `proj__pages--3`
([portfolio.css:228–231](../public/styles/portfolio.css#L228-L231)), which fills the row with three; the narrow-screen
rules after it still take over.

---

## 4. `public/robots.txt`

| Line | Content | Meaning |
|---|---|---|
| [1](../public/robots.txt#L1) | `# Numa Koudsie · physics website` | Comment. |
| [3](../public/robots.txt#L3) | `User-agent: *` | The rules below apply to every crawler. |
| [4](../public/robots.txt#L4) | `Allow: /` | Everything may be crawled, including the project copies and their study files. |

There is no `Sitemap:` line. Measured: `/robots.txt` answers 200 as `text/plain`, 58 bytes, identical to the file, on
AppDeploy and (20 October 2026) on phyeinusul.com. To keep a path out of search engines, add a `Disallow: /path` line under `User-agent: *`.

---

## Notes for maintainers

1. **Home page shadows depart from the house design; its title face is now a stated exception.** AGENTS.md
   ([41–43](../AGENTS.md#L41-L43)) and CLAUDE.md ([46–47](../CLAUDE.md#L46-L47)) ask, since 20 October 2026, for titles in
   Instrument Serif at weight 400 on the simulation, catalog and Portfolios pages and in IBM Plex Serif at weight 600 on the
   home page alone; AGENTS.md also asks for no card shadows. The home page loads only `site.css`, whose `--serif` is
   IBM Plex Serif ([site.css:22](../public/styles/site.css#L22)) and whose titles are weight 600
   ([site.css:138](../public/styles/site.css#L138), [336](../public/styles/site.css#L336),
   [423](../public/styles/site.css#L423)). Measured: `h1`, five `h2` and 21 `h3` in IBM Plex Serif 600, as the rule now says; box shadows on
   `.figure`, `.project` and `.plate`, against it. The catalog and Portfolios pages use Instrument Serif 400 (measured; `catalog.css` sets `--serif` to Instrument Serif,
   [catalog.css:10](../public/styles/catalog.css#L10)).
2. **The home page shows eight figures, the site has eleven.** The plates stop at Fig. 8 ([290–570](../index.html#L290-L570));
   Figs. 9, 10 and 11 are only in the catalog ([catalog.js:183–233](../public/scripts/catalog.js#L183-L233)). The section intro says
   the simulations page "lists them all by field, with the question each one answers"
   ([index.html:283–284](../index.html#L283-L284)); the catalog now lists them in figure order without grouping
   ([simulations.html:232–234](../public/simulations.html#L232-L234)), and catalog entries have no question field.
3. Fixed on 2026-10-15: the unused home stop function and its write-only request id were removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
4. **The catalog's `noscript` points to the home page for the list** ([simulations.html:76–77](../public/simulations.html#L76-L77)),
   which has only Figs. 1–8.
5. Fixed on 2026-10-15: the permanently hidden catalog intro and its CSS were removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
6. **`window.__catalog.state` goes stale** after "Show all simulations": the `#clear` handler assigns a new object to `state`
   ([simulations.html:328](../public/simulations.html#L328)) while `__catalog` keeps the first one
   ([350](../public/simulations.html#L350)). Measured: after clearing `?q=zzzz`, `__catalog.state.q` still reads "zzzz". Nothing
   in the repository reads `__catalog`.
7. **The catalog QA scenario did not match the page.** It expected ten open entries on arrival; the cards open as closed
   titles ([simulations.html:245](../public/simulations.html#L245), `defaultOpen: false`). Rewritten on 14 October 2026
   ([tests.json:33](../tests/tests.json#L33)) and deployed to the app. Still open: the home page scenario
   ([tests.json:17](../tests/tests.json#L17)) depends on there being exactly eight plates.
8. **AGENTS.md contradicted itself on the catalog layout:** its Simulations-page paragraph said "in one grid", while the Folds
   paragraph ([27–29](../AGENTS.md#L27-L29)) and the code ([fold.css:153](../public/styles/fold.css#L153)) give one column of
   fold cards. Corrected on 14 October 2026 ([AGENTS.md:32–35](../AGENTS.md#L32-L35)).
9. Fixed on 2026-10-15: the four Droplet Collection image attributes use integer ratios exactly equal to their SVG viewBoxes (commit [74ef7d9](https://github.com/Numa1997/SiteTest/commit/74ef7d94571f467f31d2289be6c9668b6809a09f)).
   That fix copied the viewBox numbers times 1000 (for example 400520 × 188969), so with no stylesheet the pictures came out
   295 522 to 405 740 px wide. Replaced by note 11.
10. **Two favicons.** The home page draws "N" ([index.html:19](../index.html#L19)), the other two pages a bold "NK"
    ([simulations.html:22](../public/simulations.html#L22), [portfolios.html:24](../public/portfolios.html#L24)).
11. Fixed on 2026-10-15: the four Droplet Collection images carry `width` × `height` of 636 × 300, 419 × 300, 580 × 300 and
    470 × 300 css px, the SVGs' proportions (those plates were replaced on 23 October 2026 by the rebuild's four, same rule; table
    under **Image sizes**). Before, they were the `viewBox` numbers times 1000 (400520 × 188969 and the like), which made the pictures
    295 522 to 405 740 px wide when no stylesheet loads (audit repair, commit [32c240c](https://github.com/Numa1997/SiteTest/commit/32c240c52fd0535d39a0cef608dc404cf4219484)).

## CV page (`public/cv/`)

`public/cv/index.html` is served at <https://phyeinusul.com/cv/>, a link made to send on its own. It shows both pages of the CV
(German, then English) as images, `cv-de.webp` and `cv-en.webp` (rendered at 170 dpi from the PDF with `pdftoppm`), so it reads on
any phone, and offers the PDF itself, `Numa_Koudsie_CV.pdf`, to open or download. The top bar of the home page index, the simulations catalog and the Portfolios page links to it (German "Lebenslauf", Arabic "السيرة الذاتية"); simulation pages keep their figure bar only. To update the CV:
replace the PDF, re-render the two images (`pdftoppm -r 170 -png Numa_Koudsie_CV.pdf p`, then save each as WebP), build and deploy.
English only; it is not in the translation build.
