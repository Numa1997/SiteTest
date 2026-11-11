# The site's own pages: home, simulations catalog, Portfolios, robots.txt

Five files make the frame around the twelve simulation pages:

| File | Served at | Lines | What it is |
|---|---|---|---|
| [`index.html`](../index.html) | `/` | 1547 | The home page: the Phyein Usul logo and note, CV, projects, ten figure plates (one per simulation), a live double pendulum. |
| [`public/simulations.html`](../public/simulations.html) | `/simulations.html` | 212 | The catalog: one fold card per simulation, no search and no chips since 3 November 2026. |
| [`public/portfolios.html`](../public/portfolios.html) | `/portfolios.html` | 472 | The Projects page (address `portfolios.html`, kept so old links work): the Bachelor thesis and four studies, and the links into their pages. |
| [`public/lucretius.html`](../public/lucretius.html) | `/lucretius.html` | 177 | The poem page (10 November 2026): Lucretius I 146–224 as 20 verses in English, German and Arabic; see the last section. |
| [`public/robots.txt`](../public/robots.txt) | `/robots.txt` | 4 | Rules for search-engine crawlers. |

The build copies everything under `public/` to the site root, so a page under `public/` links to `styles/…` and
`scripts/…` without a `public/` prefix (see [build-and-deploy.md](build-and-deploy.md)). The same folder also holds
[`public/_headers`](../public/_headers), which is not a page: Cloudflare reads it for the security headers and never serves it
(measured: `/_headers` answers 404; [usul.md](usul.md)).

Checked on 20 October 2026 on Cloudflare (https://phyeinusul.com and
www.phyeinusul.com, [usul.md](usul.md)): the three HTML pages, the seven stylesheets and `robots.txt` are served byte for byte as
in the repository, with nothing injected. Until 31 October 2026 Cloudflare answered an address ending in `.html` with a 307
redirect to the same address without it (`/simulations.html` → `/simulations`, `/index.html` → `/`), one round trip on every
click. Since then it serves `x.html` at once (`"html_handling": "none"` in `wrangler.jsonc`), and serves each page at its short
address too (`/simulations`, `/`, `/ar/`), through `public/_redirects`, written by `tools/redirects.py`
([performance.md](performance.md), change 6). The address bar now shows the `.html` address after a click.

Related pages: the fold mechanism is in [scripts/fold.md](scripts/fold.md), the registry the catalog draws from in
[scripts/catalog.md](scripts/catalog.md), the stylesheets in [styles.md](styles.md), the research projects in
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
| `scripts/fold.js` at the end of `<body>` | [723](../index.html#L691) | [124](../public/simulations.html#L124) | [420](../public/portfolios.html#L453) |
| Footer: © line and "Back to top" | [718–721](../index.html#L686-L689) | [119–122](../public/simulations.html#L119-L122) | [415–418](../public/portfolios.html#L448-L451) |

The `js` class matters for one thing: [site.css:756–766](../public/styles/site.css#L756-L766) hides `.reveal` blocks
only under `.js`, so without JavaScript nothing waits for a fade-in.

`fold.js` runs its `boot()` at `DOMContentLoaded` ([fold.js:404–411](../public/scripts/fold.js#L404-L411)). Each page's
inline script sits after it and runs during parsing, so the inline script always runs first and fold.js then reshapes the
finished DOM. Every page arrives with its cards closed (since 3 November 2026, at Numa's request): what a reader opens or
closes lasts for that visit only, and the choices earlier versions kept in `localStorage` (`fold:` plus the path) are removed
([fold.js:60-72](../public/scripts/fold.js#L60-L72)). A link into a card still opens it.

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
education, projects, eleven simulation plates and skills. It is the entry page of the site and of the Vite build.

### Head

| Lines | Item |
|---|---|
| [5–6](../index.html#L5-L6) | Security policy and referrer rule ([build-and-deploy.md](build-and-deploy.md#security)) |
| [8](../index.html#L8) | `<title>` "Numa Koudsie · Notebook" |
| [9–13](../index.html#L9-L13) | `description`, `author`, `theme-color` |
| [15](../index.html#L15) | `styles/site.css` (tokens, layout, hero, timeline, plates; imports the self-hosted IBM Plex from `fonts/plex.css`) |
| [15](../index.html#L15) | `styles/fold.css` (the fold cards) |
| [21–23](../index.html#L21-L23) | `className = 'js'` |

Scripts, in load order, at the end of `<body>`: `scripts/fold.js` ([723](../index.html#L691)), then the inline script
([724–1424](../index.html#L692-L1392)). No KaTeX, no `paper.css`: the home page has no mathematics typeset.

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
  (`#positions`), `Open the simulations` (`simulations.html`), `Open the projects` (`portfolios.html`) ([48–52](../index.html#L48-L52)).
- `figure.figure` ([54–60](../index.html#L54-L60)): `canvas#pendulum` inside `.figure__stage`, caption "Fig. 0 · double pendulum ·
  RK4 · live" and `button#pendulum-reset`.

**Layout** `div.layout` ([63–720](../index.html#L63-L688)): a 260 px column for the index and the content column, 64 px apart
([site.css:278–285](../public/styles/site.css#L278-L285)); from 981 px wide, 300 px and 56 px, at most 1160 px in all
([site.css:330](../public/styles/site.css#L330)). Measured 29 October 2026.

- `nav.index[data-fold-bar]` ([64–75](../index.html#L64-L75)): links to the five sections ("Projects" is `#research`) and `portfolios.html` ("All projects ↗").
  On wide screens it sticks 28 px from the top as a side column; at 980 px and below it becomes a full-width bar at the top
  ([site.css:787–797](../public/styles/site.css#L787-L797)). The attribute `data-fold-bar` lets fold.js measure it: measured
  `--fold-top` is 0 px at 1280 px (the side column does not count, [fold.js:295](../public/scripts/fold.js#L295)) and 49 px at
  900 and 390 px, so open section headers pin below the bar.
- `main.content#main` ([77–715](../index.html#L77-L683)) holds five `section.section` elements, each with an `id` and an `h2`:

| Section | Lines | Structure (classes a maintainer edits) | fold.js counts line |
|---|---|---|---|
| `#positions` "Positions" | [78–202](../index.html#L78-L202) | `.timeline` with `.timeline__line` (the wine line that grows) and seven `article.entry.reveal`: `.entry__when` (dates, optional `.tag` "current", `.tag.tag--soft`), `h3`, `.entry__org`, `ul.bullets`. The current one also has `.entry--current` (filled pulsing dot). | "7 roles" (`article.entry`) |
| `#education` "Education" | [204–233](../index.html#L204-L233) | `.ledger` with three `.row.reveal`: `.row__when`, `h3`, `.row__org`, optional `.row__note` | "3 qualifications" (`h3`) |
| `#research` "Projects" | [235–280](../index.html#L235-L280) | `.section__intro` linking to the Projects page, `.projects` with four `article.project.reveal`: Droplet Collection, Rotor Pendula, Hydraulic Press Study, and Iron, Cotton and the Head. Each has a field label that starts with its kind ("Bachelor thesis" or "Study"), linked title, summary and direct project link; then an `All projects →` button in `p.plates__more` | "4 projects" (`article`) |
| `#simulations` "Interactive physics simulations" | [277–674](../index.html#L277-L642) | `.section__intro`, `.plates` with eleven `article.plate.reveal` (Figs. 1–11, every simulation in the catalog) as a sideways shelf, its controls `.shelf-nav` ([663–668](../index.html#L631-L636)), then `All simulations →` | "11 figures" (`article`) |
| `#skills` "Skills & languages" | [676–714](../index.html#L644-L682) | `dl.skills`, seven `div.reveal` each with `dt` and `dd`; language levels in `span.lvl` | "7 areas" (`dt`) |

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

**Footer** ([718–721](../index.html#L686-L689)): "© 2026 Numa Koudsie" and `#top`.

### The inline script

One function expression wraps everything ([725–1423](../index.html#L693-L1391)). It has three independent parts.

**Fig. 0, the live double pendulum** ([730–939](../index.html#L698-L907)). The everyday picture: a pendulum hanging from the
bob of another pendulum; let it go from high up and it swings wildly, never retracing its path. The model: two point masses on
massless rigid rods, no friction, angles $\theta_1, \theta_2$ measured from the downward vertical. The code uses
$g = 9.81\ \mathrm{m/s^2}$, $m_1 = m_2 = 1\ \mathrm{kg}$, $l_1 = l_2 = 1\ \mathrm{m}$ ([736–740](../index.html#L704-L708)) and
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
| `reduced` (value) | [726–728](../index.html#L694-L696) | True when the reader asks for reduced motion (`prefers-reduced-motion`). |
| `deriv(s)` | [757–780](../index.html#L725-L748) | The right-hand side above: returns $(\dot\theta_1, \dot\theta_2, \ddot\theta_1, \ddot\theta_2)$. |
| `rk4(s, h)` | [781–797](../index.html#L749-L765) | One RK4 step of size `h` seconds: four slopes, weighted 1, 2, 2, 1. |
| `pos(s)` | [798–807](../index.html#L766-L775) | Pixel positions of both bobs: pivot `(ox, oy)`, `scale` pixels per metre, $x = \sin\theta$, $y = \cos\theta$ (screen y points down). |
| `resize()` | [808–823](../index.html#L776-L791) | Sizes the canvas and the off-screen trail canvas to the CSS size times the device pixel ratio (capped at 2). Pivot at the centre, 36 % down; `scale` = 0.24 × the smaller side. |
| `reset()` | [824–833](../index.html#L792-L801) | New random start at rest: $\theta_1 \in [112°, 157°]$, $\theta_2 \in [135°, 207°]$ (from `Math.PI * (0.62 + 0.25 r)` and `Math.PI * (0.75 + 0.4 r)`); clears the trail. |
| `step(n, h)` | [834–849](../index.html#L802-L817) | Takes `n` RK4 steps and draws each move of the lower bob as a short wine segment (`rgba(122, 31, 43, 0.85)`, 1.4 px) on the trail canvas. |
| `fadeTrace(a)` | [850–856](../index.html#L818-L824) | Erases a fraction `a` of the trail with `destination-out`, so old trail fades. |
| `draw()` | [857–880](../index.html#L825-L848) | Clears, copies the trail, draws the rods (ink, 2.2 px), the grey pivot (3.5 px) and the wine bobs (7 and 9 px radius). |
| `frame(ts)` | [881–894](../index.html#L849-L862) | The animation loop, below. |
| `start()` | [895–900](../index.html#L863-L868) | Start the `requestAnimationFrame` loop; visibility gates the work. |
| start-up | [902–920](../index.html#L870-L888) | `resize()`, `reset()`. With reduced motion: 2600 steps of 3.5 ms (9.1 s) and one still picture, no loop. Otherwise 560 steps of 2.5 ms (1.4 s) so the trail is not empty, then `start()`; pauses while the tab is hidden (`visibilitychange`) or the canvas is off screen (`IntersectionObserver`). |
| resize handler | [921–929](../index.html#L889-L897) | 120 ms after the last resize: `resize()`, clear the trail, `draw()`. |
| reset button | [930–938](../index.html#L898-L906) | `reset()`, then the 9.1 s pre-run if motion is reduced, then `draw()`. |

The frame loop in order ([881–894](../index.html#L849-L862)): the real time since the last frame `dt` is capped at 50 ms (so
a stalled tab does not jump); simulated time `dt × SPEED` with `SPEED = 0.8` (the pendulum runs at 80 % of real speed) is added
to an accumulator; the whole number of 2.5 ms steps it holds is taken (at 60 frames per second that is 5 or 6 steps); the trail
fades by `1 − 0.99^(dt·60)`, which removes 1 % per 1/60 s whatever the frame rate (the trail halves in 69 frames, 1.15 s); then
`draw()`.

**Plate sketches** ([941–1369](../index.html#L909-L1337)). Each `div.plate__fig[data-sketch]` gets a small static SVG
(`viewBox="0 0 200 110"`). Colours come from classes styled in [site.css:590–607](../public/styles/site.css#L590-L607):
`ink`, `acc` (wine), `soft` (rose), `grey`, `acc-fill`, `grey-fill`.

| Function | Lines | What it draws |
|---|---|---|
| `sine(x0, x1, y, amp, wl, ph, st)` | [942–949](../index.html#L910-L917) | SVG path of a sine curve sampled every `st` units. |
| `svg(inner)` | [950–956](../index.html#L918-L924) | Wraps the markup in the 200 × 110 `<svg>`. |
| `sketches.interference` | [958–983](../index.html#L926-L951) | Two sources at (62, 104) and (138, 104), ten rings each, fading outward. |
| `sketches.pendulum` | [984–994](../index.html#L952-L962) | A drawn double pendulum with a dashed rose trail. |
| `sketches.doubleslit` | [995–1036](../index.html#L963-L1004) | Plane wavefronts, a barrier with two slits at x = 66, half-circle wavelets, and 13 screen bars of height $\propto \cos^2(0.9 i)\,e^{-\lvert i\rvert/6}$. |
| `sketches.wavetypes` | [1037–1056](../index.html#L1005-L1024) | A transverse sine (top) and 22 dots bunched by a sine (bottom): compressions. |
| `sketches.waterwave` | [1057–1080](../index.html#L1025-L1048) | Seven rings round the centre and seven small orbits with a particle on each. |
| `sketches.simulator` | [1081–1111](../index.html#L1049-L1079) | Two sines of wavelength 70 and 29 (top) and their sum (bottom). |
| `sketches.phasors` | [1112–1193](../index.html#L1080-L1161) | The rose $z(t) = A e^{i(4t - \pi/2)} + A e^{i(-2t + \pi/2)}$, $A = 21$, with its two arms at $t = 0.3$. |
| `sketches.fourier` | [1194–1292](../index.html#L1162-L1260) | The heart $x = 16\sin^3 u$, $y = 13\cos u - 5\cos 2u - 2\cos 3u - \cos 4u$ from its exact Fourier coefficients (the comment at 1189–1190 is correct: summing the eight terms gives back both formulas), three epicycles, and the spectrum $\lvert c_k\rvert$ for $k = -4 \dots 4$. |
| `sketches.oscillator` | [1293–1316](../index.html#L1261-L1284) | The amplitude $1/\sqrt{(1-r^2)^2 + (2\zeta r)^2}$ of a driven oscillator against $r = f/f_0$ from 0 to 2.5, for $\zeta = 0.1$ (wine) and $0.3$ (rose), cut at 5.6, a dashed line at resonance, and a mass on a spring with an arrow for the force. |
| `sketches.turbine` | [1317–1341](../index.html#L1285-L1309) | A three-blade rotor in wind, and Heier's power coefficient $c_p(\lambda) = 0.5176\,(116/\lambda_i - 5)\,e^{-21/\lambda_i} + 0.0068\,\lambda$, $1/\lambda_i = 1/\lambda - 0.035$, the simulation's eq. (5) (maximum 0.480 at $\lambda = 8.1$), for $\lambda$ from 0.5 to 12.5, its maximum marked, under the Betz limit 16/27 (dashed). |
| `sketches.pendctl` | [1342–1361](../index.html#L1310-L1329) | A double pendulum from a fixed pivot with a dashed trail, its lower ball tied by a zigzag spring (the strut) to a cart on a rail, and an arrow for the force on the cart. |
| fill loop | [1363–1369](../index.html#L1331-L1337) | For each `.plate__fig[data-sketch]`, looks up the function by name and sets `innerHTML`; an unknown name leaves the plate blank. |

**The plates as a shelf** ([1425–1577](../index.html#L1393-L1545), styles at the end of
[site.css:888–1169](../public/styles/site.css#L888-L1169); since 2 November 2026). The eleven plates sit in one row
that scrolls sideways and snaps plate by plate (CSS `scroll-snap-type: x mandatory`): 3 in view when the row is wider than
760 px, 2 down to 561 px, and on a phone one plate at 82 % of the row with the edge of the next. Measured in Chromium: 218 px
plates in a 691 px row at 1440 px, 232 of 731 at 820 px, 244 of 301 at 390 px; the page never scrolls sideways. Inside the
shelf the plates are smaller (figure 128 px, title 19 px, text 13.5 px).

The script wraps the row in `div.shelf` and puts a **rail** on its end edge (the right; the left in Arabic): a pill with one
8 px dot per plate, wine with a soft ring for the plates in view (at least 60 % showing, read by an `IntersectionObserver`
with the row as root). The dots never change size, so they cannot move under a finger. Running the mouse along the rail, or
pressing it and sliding a finger (scrubbing, as on the page dots of a phone's home screen; `touch-action: none` keeps the
page still, measured 0 px of page scroll during a scrub), picks the dot nearest the pointer: the dots swell by
$1 + 1.1\,e^{-(d/20\,\text{px})^2}$ at distance $d$, a bubble (`.shelf__tip`) beside the rail shows that plate's sketch,
number and title, the row jumps to that plate without animation (smooth steps lag under a fast scrub), the plate gets a
wine edge (`.is-picked`), and phones that allow it give a 4 ms tick. Each dot is also a button: a click or keyboard focus
brings its plate smoothly. Below the row, arrows move by as many plates as are in view, disabled at either end, around a
counter "1–3 / 11" (`.shelf__dots`, empty, is the spacer between them). The row fades 40 px of the edge already passed and
56 px of the edge still to come (`--fade-l`, `--fade-r` on a mask; `/*rtl:ignore*/` keeps the gradient physical, and the
script swaps the sides in Arabic). It also marks plates in view `is-visible`, since the page's reveal observer cannot see
plates clipped by the row. Without JavaScript the rail and arrows are absent and the row is a plain sideways scroll with
its scrollbar; in print the plates fall back to two columns. The arrows' labels are translated pieces; the dots and the
bubble take their words from each plate's "Fig. n" and title.

**Reveal on scroll and the active index link** ([1371–1422](../index.html#L1339-L1390)).

| Part | Lines | What it does |
|---|---|---|
| `io` observer | [1375–1385](../index.html#L1343-L1353) | When 10 % of an observed element is visible, adds `is-visible` once and stops watching it. |
| stagger | [1386–1389](../index.html#L1354-L1357) | Each `.reveal` gets `--d = (i mod 5) × 80 ms`, the delay its fade uses ([site.css:760–761](../public/styles/site.css#L760-L761)). |
| blocks | [1390–1392](../index.html#L1358-L1360) | `.section` and `.timeline` also get `is-visible`: the timeline line grows to full height in 1.8 s ([site.css:378–389](../public/styles/site.css#L378-L389)). |
| `nav` observer | [1394–1414](../index.html#L1362-L1382) | `rootMargin: '-30% 0px -60% 0px'` watches a band 30–40 % down the window; the section crossing it marks its `.index` link `active`. Only links starting with `#` take part. |
| fallback | [1415–1422](../index.html#L1383-L1390) | Without `IntersectionObserver`, everything is made visible at once. |

### Without JavaScript

Measured with scripting off: the root keeps `no-js`, `.reveal` blocks show at full opacity, no folds are made, the five
sections read as plain sections with their `h2` and wine bar, the index links are ordinary anchors, the hero canvas and
the eleven plate figures stay empty (only the grid background shows), and everything else is complete.

### How to change it

- **Add a position.** Copy one `article.entry.reveal` inside `#positions .timeline` ([83–200](../index.html#L83-L200)).
  The list runs by end date, newest first, with the current position on top. For a current post add `entry--current` and
  `<span class="tag">current</span>`; for a label such as "during studies" add `<span class="tag tag--soft">`. The fold
  count ("n roles") updates itself.
- **Add an education row.** Copy a `.row.reveal` in `.ledger` ([207–231](../index.html#L207-L231)); `.row__note` is optional.
- **Add a research project.** Copy an `article.project.reveal` in `.projects` ([247–270](../index.html#L247-L270)); the grid
  has two columns ([site.css](../public/styles/site.css)), one at 980 px and below. Keep its title, summary and project link consistent with the actual portfolio. A finished long
  project belongs on the Projects page (`portfolios.html`); label it "Bachelor thesis", "Study" or what it is, not "research" unless it is; also update the intro sentence at [237–245](../index.html#L237-L245).
- **Add a plate.** (The shelf picks it up: one more dot on the rail, the counter counts it.) Copy an `article.plate.reveal` in `.plates` ([287–661](../index.html#L287-L629)), set `p.plate__num`, both
  hrefs and the three tags, and give `.plate__fig` a `data-sketch` name. Add a function of that name to `sketches`
  ([957–1361](../index.html#L925-L1329)) returning `svg(…)`; use the classes `ink`, `acc`, `soft`, `grey`, `acc-fill`,
  `grey-fill`. Plates are written by hand: they do not read [catalog.js](../public/scripts/catalog.js), and their titles
  differ from the catalog titles (for example "Wave Interference – Multiple Sources" against "Wave Interference").
- **Add a skill row.** Copy a `div.reveal` in `dl.skills` ([679–712](../index.html#L647-L680)).
- **Add a section.** Give it `class="section"`, an `id` and an `h2`, add its link to `nav.index`, and, for a counts line,
  a rule in `units` ([fold.js:356–362](../public/scripts/fold.js#L356-L362)); without one the header shows no counts.

---

## 2. `public/simulations.html` · the catalog

**Purpose.** The list of every simulation. It opens as a column of twelve closed titles, "01 Wave Interference" to
"12 A Pint of Stout on a Suspension" (added 5 November 2026; earlier "11 Balancing Two Rods on a Cart"), in figure order (the old Fig. 11 became a project on 3 November 2026 and a new Fig. 11 took its place), under Expand all / Collapse all. A title opens to a paper abstract: thumbnail, field
and year, summary, the key equation set by KaTeX, and links to the figure and to its lecture note. Since 3 November 2026 there
is no search, no field or year chips, no "n shown" counter and no numbers line (removed at Numa's request; the address takes no
`?q=&field=&stage=` any more). Everything is drawn from the registry [`scripts/catalog.js`](../public/scripts/catalog.js)
(documented in [scripts/catalog.md](scripts/catalog.md)).

### Body

| Lines | Element | Role |
|---|---|---|
| [32–41](../public/simulations.html#L32-L41) | `header.cat-top` | The Phyein Usul logo (linking to `index.html`), "← Numa Koudsie", the site index and the language switch. |
| [43–94](../public/simulations.html#L43-L94) | `main.cat` | The page column (max 1240 px). |
| [44–54](../public/simulations.html#L44-L54) | `.cat__head` | `.cat__kicker`, `h1` "Simulations.", `.cat__lede`. |
| [56–61](../public/simulations.html#L56-L61) | `noscript` | "This catalog needs JavaScript", with a link to the home page plates. |
| [63](../public/simulations.html#L63) | `div#catalog.cat__list.cat__list--sorted` | The list; filled by `render()`. Expand all / Collapse all go just above it (`Fold.tools`). |
| [65–93](../public/simulations.html#L65-L93) | `section.cat__anatomy` | Static: "Every simulation, the same four parts" (figure, lecture note, walkthrough, data panel). |
| [96–99](../public/simulations.html#L96-L99) | `footer` | Links home and to Projects; `a#to-top`. |

Scripts at the end of `<body>`, in order: `scripts/fold.js` ([101](../public/simulations.html#L101)), `scripts/catalog.js` ([102](../public/simulations.html#L102)),
`vendor/katex/katex.min.js` ([103](../public/simulations.html#L103)), the inline script ([104–210](../public/simulations.html#L104-L210)).

**The markup one simulation becomes.** `cards()` and `entry()` build, for a registry entry `s`:

```
section.simfold#simulation-<id>  [data-counts = subject, data-label = title]     cards()  162–167
  h2.fs-title > span.fs-num "01" + title                      (moved into the fold header by fold.js)
  article.entry#sim-<id>  [data-card, data-sim, data-collapsed]                   entry()  128–157
    a.entry__fig > span.entry__plate > span.entry__ph "Fig. n" + img (images/sims/<id>.webp, 800 × 500, lazy)
    p.entry__cap   "Figure n" + subject
    div.entry__body
      p.entry__kicker   field name · first/second year
      h3 > a            title (hidden by fold.css; the fold header already shows it)
      p.entry__abs      summary
      div.entry__eq[data-tex]                                  (typeset by typeset())
      div.fold[data-open][inert] > div.fold-i > div.entry__more      the details behind More / Less
        dl.entry__facts   model · method · you set
        ul.entry__tags    up to six concepts
      div.entry__foot   a.entry__open "Open Fig. n" · a.entry__note "Read the lecture note" (#paper) · button.fs-more
```

Two levels of opening: the **title fold** (the `section`, a level-1 fold made by `Fold.make`, [169–174](../public/simulations.html#L169-L174)) starts closed on
every visit (fold.js keeps choices for the visit only); the **card details** (the `article`, a `[data-card]`) open with
More / Less ([fold.js:209–224](../public/scripts/fold.js#L209-L224)).

### The inline script

| Function | Lines | What it does |
|---|---|---|
| set-up | [105–113](../public/simulations.html#L105-L113) | The translation helper `T`; copies `window.SIMULATIONS` to `SIMS` and `SIM_FIELDS` to `FIELDS`; `openCards`. |
| `esc(s)` | [115–119](../public/simulations.html#L115-L119) | Escapes `& < > " '` for HTML. |
| `fieldOf(id)` | [120–123](../public/simulations.html#L120-L123) | The `SIM_FIELDS` entry for an id, or a stand-in named by the id. |
| sort | [125](../public/simulations.html#L125) | Figure order (`a.fig - b.fig`). |
| `entry(s)` | [128–157](../public/simulations.html#L128-L157) | The `article` markup above; `encodeURI(s.file)` for the links. |
| `cards(shown)` | [162–167](../public/simulations.html#L162-L167) | Wraps each entry in its `section.simfold` with the numbered title. |
| `folds()` | [169–174](../public/simulations.html#L169-L174) | `Fold.make(section, { level: 1, head: [h2], counts: subject, label: title, defaultOpen: false })` for each title. |
| `typeset()` | [176–186](../public/simulations.html#L176-L186) | Renders each `.entry__eq` with `katex.render` in display mode; without KaTeX, shows the TeX. |
| `render()` | [188–195](../public/simulations.html#L188-L195) | Draws the whole list once: HTML, folds, equations; removes a thumbnail that fails to load. |
| `#to-top` | [197–200](../public/simulations.html#L197-L200) | Scrolls to the top. |
| start-up | [202–208](../public/simulations.html#L202-L208) | Hooks `Fold.onCard` and `Fold.onAll`, puts Expand all / Collapse all above the list, draws, then marks the page `cat-drawn` (catalog.css shows what follows the list only then). |

**Registry fields the page reads**: `id`, `fig`, `title`, `file`, `field`, `stage`, `subject`, `summary`, `equation`,
`model`, `method`, `controls`, `concepts`, and `name` from `SIM_FIELDS`.

### Without JavaScript

The `noscript` message shows; the list stays empty; the header, the "four parts" section and the footer show.

### How to change it

- **Add a simulation**: one entry in `SIMULATIONS` and a thumbnail; nothing in this page changes. The steps are in
  [scripts/catalog.md](scripts/catalog.md).
- **Change what a card shows**: edit `entry()`; keep `data-card`, the inner `.fold` and `button.fs-more`, which fold.js
  needs for More / Less.
- **Change the anatomy text**: plain HTML at [65–93](../public/simulations.html#L65-L93).

---

## 3. `public/portfolios.html` · the research projects

**Purpose.** Introduces the four long projects, each with an abstract, four key numbers, numbered parts (four each, three for
Rotor Pendula, counted 29 October 2026) and links into its own pages. The projects themselves are pages generated from their sources in `portfolios-src/` into
`public/portfolios/<name>/` ([portfolios.md](portfolios.md)).

### Head

Security policy and referrer rule ([5–6](../public/portfolios.html#L5-L6)), `<title>` "Portfolios · Numa Koudsie"
([8](../public/portfolios.html#L8)). Stylesheets in order
([15–22](../public/portfolios.html#L15-L22)): `site.css`, `katex.min.css`, `paper.css`, `catalog.css` (top bar, masthead,
`--serif`), `portfolio.css` (the project cards), `fold.css`, `i18n.css` (the language switch), and `fonts/arabic.css` for the two Arabic labels of project 04. Scripts at the end of `<body>`: `scripts/fold.js`
([420](../public/portfolios.html#L453)), `vendor/katex/katex.min.js` ([421](../public/portfolios.html#L454)),
`vendor/katex/contrib/auto-render.min.js` ([422](../public/portfolios.html#L455)), the inline script
([423–437](../public/portfolios.html#L456-L470)).

### Body

- `header.cat-top` ([34–43](../public/portfolios.html#L34-L43)), as on the catalog (logo and "← Numa Koudsie" at
  [35](../public/portfolios.html#L35)), with Simulations instead of Portfolios.
- `main.cat#projects` ([45–413](../public/portfolios.html#L45-L446)). Its `.cat__head` has an inline style for one column
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

**Links into the projects** (counted 29 October 2026). Every link names the file, never the folder:
`portfolios/droplet-collection/index.html#book`, `#sim`, `#problems`, `#checks` and four `#fig-…` figures;
`portfolios/rotor-pendula/index.html` with `#notes`, `#sim` and `#wind`; `portfolios/hydraulics/index.html#servo`, `#ideal`
and `#theory`; `portfolios/impact/index.html`, `de.html` and `ar.html`. Each page reads its tab or anchor from the address on
load ([portfolios.md](portfolios.md)). Cloudflare serves `…/index.html` itself since 31 October 2026, and the folder address through `public/_redirects`, so both
forms of the link work (until then it redirected `…/index.html` to the folder with a 307, keeping the fragment). The English pages of the four projects link back with
`href="../../portfolios.html"`; their German and Arabic pages link back to the Portfolios page in their own language.
The figure images come from each project's `fig/` folder (for example
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
| maths | [426–431](../public/portfolios.html#L459-L464) | `renderMathInElement` (KaTeX auto-render) over `#projects`, with `\[ … \]` for display and `\( … \)` for inline maths, `throwOnError: false`. Measured: 33 formulas typeset. It runs before fold.js reshapes the page, so the folds hold typeset maths. |
| `#to-top` | [432–435](../public/portfolios.html#L465-L468) | Scrolls to the top (there is no `#top` element). |

### Without JavaScript

Measured with scripting off, when the page had three projects: all three read in full with their bands, numbers, figures and links; no folds; the maths
shows as TeX source between `\(` and `\)` (eight such formulas in part 1.1 alone).

### How to add a project

1. Generate the project's page into `public/portfolios/<name>/` from its source in `portfolios-src/<name>/`, as the four
   projects are ([portfolios.md](portfolios.md)): one self-contained page with the site's two meta tags, its fonts from
   `fonts/`, and a back link to `../../portfolios.html`. (Until 23 October 2026 two projects were copies of app builds,
   with a `static/` folder and a stylesheet added by script.)
2. Copy one `article.proj` block; give it a new `id` and `aria-labelledby`, a new `h2` id, `span.proj__num` "05", the band's
   `p` and last `span` (they become the counts line), the abstract, the four `dt`/`dd` pairs and the buttons.
3. Number the parts `5.1`, `5.2`, … in `span.psub__n`; give each `h3` an `id` and the `section` an `aria-labelledby`.
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
| [4](../public/robots.txt#L4) | `Allow: /` | Everything may be crawled, including the project pages and their study files. |

There is no `Sitemap:` line. Measured: `/robots.txt` answers 200 as `text/plain`, 58 bytes, identical to the file, on
phyeinusul.com (20 October 2026). To keep a path out of search engines, add a `Disallow: /path` line under `User-agent: *`.

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
2. **The home page shows eight figures, the site has eleven.** The plates stop at Fig. 8 ([290–672](../index.html#L290-L640));
   Figs. 9, 10 and 11 are only in the catalog ([catalog.js:183–233](../public/scripts/catalog.js#L183-L217)). The section intro says
   the simulations page "lists them all by field, with the question each one answers"
   ([index.html:283–284](../index.html#L283-L284)); the catalog now lists them in figure order without grouping
   ([simulations.html:158–161](../public/simulations.html#L158-L161)), and catalog entries have no question field.
3. Fixed on 2026-10-15: the unused home stop function and its write-only request id were removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
4. **The catalog's `noscript` points to the home page for the list** ([simulations.html:57–60](../public/simulations.html#L57-L60)),
   which has only Figs. 1–8.
5. Fixed on 2026-10-15: the permanently hidden catalog intro and its CSS were removed (commit [8982ed3](https://github.com/Numa1997/SiteTest/commit/8982ed35e78161ea7cdd82ae1794f44ccfe39f3c)).
6. Fixed on 2026-11-03: the stale `window.__catalog.state` went with the search, which was removed at Numa's request.
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


## Lucretius beside the name, and the smaller title (5 November 2026)

Numa: the quote belongs in the first screen, next to the name; the name was too big ("narcissistic vibes") and the page should be
called something like a notebook or a work and study archive. The hero now reads: the logo and the Phyein Usul note; the name as a
small line (`p.hero__who`, IBM Plex Serif 600, 17–21 px); the title "Work and study archive." (`h1.hero__name`, 32–56 px, was the name
at 52–124 px); the tag, contacts and buttons as before. The right column (`div.hero__side`) holds, between `<!--LUCRETIUS-->` markers,
Lucretius I 146–158 as an inscription (Instrument Serif, a wine rule on its left, a one-line caption) above the live pendulum, whose
stage is 4 : 3 there. Each of the four sentences (`p.lq-s`, `translate="no"`, `lang="la"`) shows, on a resting mouse (150 ms; 70 ms
from one sentence to the next; hidden 240 ms after leaving), a tap or keyboard focus, one card with its published translation: Leonard
(1916) on the English page, Diels (1924) on the German page, and on the Arabic page (since 10 November 2026) an Arabic translation
made for this site, since 11 November 2026 from Leonard's English (`notes/lucretius/poem-ar-146-158.json`; the card says it is not a published translation, the only
published one, Cairo 2018, being under copyright), with the source of the Latin under it; on desktop the card rises beside the verse
(left of it where the text is; right of it on the mirrored Arabic page), otherwise just below the sentence; a click pins it, Esc or a
second click closes it. Written by `notes/lucretius/make_home.py` from `notes/lucretius/poem-146-224.json` and the Arabic file.
Measured on the built site: at 1366 × 768, 1440 × 900 and 1920 × 1080, in English, German and Arabic, the quote and the buttons are in
the first screen, no errors, no sideways scroll; on a phone the quote follows the buttons.

## The poem page, `lucretius.html` (10 November 2026, rebuilt 11 November 2026)

Numa: a button on the home page to the whole poem, on a page of its own. On 11 November 2026 he set its form: one language per page,
the way every page of the site works (an English page with a German and an Arabic version), only the poem, no Latin (it stands on the
home page), no languages side by side, decorated, the verses well separated. The home band has, under its caption, a link "Read lines
146–224 in English, German and Arabic →" (`p.lq-all`). The page (`public/lucretius.html`, with `/de/` and `/ar/` versions made by
`tools/i18n/build.py`, which lists it in `PAGES`, and short addresses in `public/_redirects`) carries William Ellery Leonard's English
verse (1916); the German page carries Hermann Diels (1924) and the Arabic page the Arabic made for this site. **How the three texts
get there:** each of the 20 verses is one translatable piece, `<p class="lp__v">`, its lines parted by `<br>`; `make_page.py` writes
the English page and puts, under the key of each English verse, Diels' verse into `i18n/de/lucretius.html.json` and the Arabic verse
into `i18n/ar/lucretius.html.json`, from `poem-146-224.json` and the two Arabic files, so nothing is retyped and the generator
treats the poem like any other text. The credit under the title is a piece too ("English verse by William Ellery Leonard, 1916" →
"Deutsche Verse von Hermann Diels, 1924" → the Arabic credit), and so is the book title (German: Diels' own, "Von der Natur").

The poem is set as the leaf of a book (`article.lp-book`, 760 px, a wine frame with a second line outside it and an eight-pointed
star, a khatam, on each corner): the poet's name, the title in Instrument Serif, book and lines, the credit, an ornament of stars and
quatrefoils, then the 20 verses (`section.lp`, address `#l146` and so on). Above every verse a heading (`h2.lp__n`): rule, lozenge,
rule, star, the line numbers of the Latin in the accent colour, star, rule, lozenge, rule. The verses are in Instrument Serif, 23 px
(19.5 px on a phone), the first with a wine drop capital; on the Arabic page in Noto Naskh Arabic, 23 px on a 2.05 line, right to
left, without the capital, and the title in Amiri. A closing ornament ends the leaf; the sources follow below it. All ornaments are
inline SVG in the accent colour. Do not edit `public/lucretius.html` by hand: run `notes/lucretius/make_page.py`, then
`tools/i18n/build.py`. The Arabic (`poem-ar-146-158.json`, `poem-ar-159-224.json`, sixth version, README) follows Leonard's English
verse by verse, is not a published translation, has no second reader, and the page says so in its source notes.
Measured on the built site: English, German and Arabic at 1280 and 390 px: 20 verses, each page holds only its own language (0 Arabic
letters in the English and German verses, 0 Latin letters in the Arabic ones), no pending piece, no errors, no sideways scroll; the
four home cards fit in all three languages.
