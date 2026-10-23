# Phyein Usul (Numa Koudsie's physics website) — ownership and update notes

This is Numa Koudsie's physics website, Phyein Usul. Owner: Numa. Changes need Numa's explicit request.

The GitHub repository `Numa1997/SiteTest` is its source: `index.html` and `public/` are the site; `README.md`, `docs/` (what every file
and script is and how it works) and `tools/` sit beside them. It runs in two places:
- Primary, since 20 October 2026: <https://phyeinusul.com> (and www), Cloudflare Worker `phyein-usul`, static assets only, built from
  `main` (`npm run build`, then `npx wrangler deploy`; settings in `wrangler.jsonc`). See `docs/usul.md`.
- The AppDeploy app `numa-koudsie-website-0cyj78` ("Numa Koudsie website"), kept as it is at v65 (equal to commit `5c7ba7f`); it is
  updated only on Numa's request. See `docs/appdeploy-app.md`.
No GitHub Pages (Numa's decision, 14 October 2026). Change the repository first, build and check it, update the `docs/` pages that
describe the change, and run `python3 tools/inventory.py` (it rewrites `docs/files.md` and fails if a file is undescribed); deploying
to Cloudflare or AppDeploy happens only when Numa asks.
Out of bounds for writes: the ChatGPT version `numa-physics-lab-chatgpt-k0ixwk` (its earlier copy `sitetest-chatgpt-r14hvr` was deleted)
and the unrelated app `physik-radar-xvy59b`. This is a project instruction, not a technical access control.

Layout (paths below are under `public/`, which the build serves at the site root; `index.html` and the build files sit at the root): `index.html`; `styles/site.css` and `styles/sim.css`;
`images/phyein-usul-mark.svg` (the logo: above the name with a short note on the home page, and linking home in the top bar of
the catalog, Portfolios and every simulation page); `_headers` (Cloudflare's response headers); `scripts/sim.js` (shared helpers, lecture-note typesetting, walkthrough engine);
`scripts/walk/<key>.js` ("From symbols to code", one file per page, chosen by the page's `data-walk` key:
each equation paired with the page's own code lines; keep the excerpts identical to the page code when either
changes; live values come from `Sim.live()` in each page); `simulations/*.html` (ten pages).
Folds: `scripts/fold.js` + `styles/fold.css`, the fold-out mechanism of Physik Radar and the project apps, in one colour (no colour
coding). Level 1 is a section card with a header band (number, title, a line of counts, round toggle) that pins to the top of the window
while open; level 2 is a part inside it, pinned under its section's band; cards keep details behind More / Less. It turns, at load:
each lecture-note section `.psec` (and each `h4` part in it), the walkthrough `#walk` (called by `sim.js` once drawn), the home page
sections, each Portfolios project and its numbered parts. The simulations list is one card per simulation, titled with its name and
numbered by its figure, in figure order; it opens as a column of closed titles, and a search or chip opens what it finds without changing
what the reader chose. Numa's choice: no sorting into fields or course years until the library is large. Elsewhere everything starts open. What a reader opens or closes is remembered per page in localStorage; Expand all / Collapse all act without animation; a link into a
closed fold opens it first and lands below the pinned headers; printing opens everything. A page bar that sticks across the whole width
(the home index on phones) carries `data-fold-bar`, so the headers pin below it. Without JavaScript every page reads fully open.
Simulations page: `simulations.html` lists every simulation as one fold card, in one column in figure order (see Folds above); an open card
shows its paper abstract (thumbnail with a numbered caption, field and year, summary, the key equation typeset by KaTeX, model, method,
what the reader sets, concepts, links to the figure and to its lecture note). A search and field and year chips filter the list; the view
lives in the address (`?q=&field=&stage=`). It draws itself from
the registry `scripts/catalog.js` (`SIMULATIONS`, `SIM_FIELDS`, `SIM_TOOLS`) with `styles/catalog.css`; thumbnails are
`images/sims/<id>.webp`, 800 × 500 px stills of each page's main figure. To add a simulation: its page in `simulations/`, one entry in
`SIMULATIONS` (and its field in `SIM_FIELDS` if new), its thumbnail (a missing one shows the Fig. number instead), and its number in the
hand-written Fig. links at the top of every simulation page. Simulation pages link back to `simulations.html`; the home page keeps its plates
and links to the catalog from the hero button, the section intro and a button under the plates.
Design: the house design of `DESIGN.md` in the app `droplet-collection-yl7l26` (the reference; read it before changing styles): titles in
Instrument Serif at weight 400 on the simulation, catalog and Portfolios pages (`styles/sim.css`, `styles/catalog.css`), and in IBM Plex
Serif at weight 600 on the home page alone (`styles/site.css`); IBM Plex Sans text, IBM Plex Mono labels, every box outlined, no card shadows. Accent wine `#7a1f2b`. Explanations are lecture
notes set like the house LaTeX write-up: `styles/paper.css` (prose and symbols in Latin Modern Roman, self-hosted in `fonts/lm/`, token
`--tex`; mathematics by KaTeX 0.16.11, self-hosted in `vendor/katex/`, woff2 only; abstract box, wine section badges, numbered display
equations on the quote ground, figures on white plates with "Figure n" captions, exercise boxes). Each simulation page ends with
`<article class="paper" id="paper">`: motivation, model, derivation (★ marks the heavier parts), numerical method, what is on screen,
limits and further reading; `sim.js` loads KaTeX and typesets `\( … \)` and `\[ … \]` in every `.paper`. No question-and-answer format.
Plotted figures in the notes are inline SVG made with the house chart style (white plate, clipped plot, Plex Mono ticks) from the page's own
formulas; every number in a note comes from a computation or the page code.
Figs. 9 (driven oscillator) and 10 (wind turbine control) solve the whole run first (RK4), store every sample in the dataset, then play the
stored samples back; nothing is integrated while the reader watches.
Portfolios: `portfolios.html` introduces long research projects; each lives as a static copy under `portfolios/<name>/`:
`portfolios/droplet-collection/` (app `droplet-collection-yl7l26`), `portfolios/rotor-pendula/` (app `rotor-pendula-gafw0f`) and
`portfolios/hydraulics/` (the Hydraulic Press Study: one self-contained page with three tabs, `#servo`, `#ideal`, `#theory`, generated by
`python3 portfolios-src/hydraulics/tools/build_combined.py --site` from its source in `portfolios-src/hydraulics/` (not served), never edited by hand; see
docs/portfolios.md) and `portfolios/impact/` (Iron, Cotton and the Head: `index.html` in English and `ar.html` in Arabic, written by
`python3 portfolios-src/impact/build.py --site` from `portfolios-src/impact/`, never edited by hand; the Arabic page alone links
`fonts/arabic.css`, Amiri and Noto Naskh Arabic under the OFL, added on Numa's request on 22 October 2026; see
docs/portfolios.md). The first two are each
the Vite build of its app without saved runs and backend (hash routes; link to `portfolios/<name>/index.html#/…`: folder addresses
returned 403 on AppDeploy until mid-October 2026; on 20 October both hosts serve them), with a back link to `../../portfolios.html`. Their build folder is `static/`, not `assets/`. AppDeploy rewrites a relative
stylesheet link in a deployed HTML file to the site root (seen for `./assets/…` and, since October 2026, `./static/…`: both give 403), so
after building, replace the `<link rel="stylesheet" href="./static/….css">` in the copy's `index.html` with a short script that adds
the same link at run time (the platform leaves scripts alone); without it the copy shows unstyled. Their source stays in their apps;
rebuild there, copy the build folder here, then patch the stylesheet link. Build the copies with the KaTeX version the apps use
(0.16.47; the apps have no lockfile), or their hidden MathML and equation spacing drift from the apps'.
Data panel, a pipeline in three files. `scripts/dataset.js`: `Sim.dataset()` gives a page one named store (dims, typed-array variables,
scalars, attrs; the shape of an xarray/NetCDF dataset) and the page writes every number into it at the line that computes it, every frame,
overwriting the last frame; nothing is recomputed for display. `scripts/datalog.js` + `styles/data.css`: the panel, which only reads the
store and does no work unless asked (no loop while closed, while open with Live off, or when nothing is pointed at). Variables: a ledger of
every quantity at one caught instant (Catch now; Live repaints every frame, opt-in); arrays open as tables copied at one instant. Read values:
a switch in each figure's caption, off by default (a hover readout over the running figure proved disruptive and was removed); while on, a click
or tap pins the object under it (rings up to 22 px around the point), a drag moves the pin, the page's own pointer actions are held back,
the marker follows the object every frame and its values sit in a strip under the figure, rewritten 4 times a second. Check: stored
value, the formula recomputed from the stored inputs, the pixel or SVG element read back from the picture, at one frame. Record one round:
`Sim.data.round` says what a round is (one period, one loop, ten seconds); every frame of it is copied (all scalars and the pinned point,
at most 600 samples), then shown as charts and a table and saved as .npz + CSV; at most five rounds are kept. Save: the store as .npz +
dataset.json + the rounds as CSV + README. The contract is at the top of datalog.js. A page loads dataset.js after sim.js and datalog.js
after its own script (all ten figures, and the two pages of Iron, Cotton and the Head, whose hooks are in
`portfolios-src/impact/datahooks.js`). `Sim.live()` reads the store too. Keep the taps where the page computes a value; keep the
walkthrough excerpts untouched (insert after a quoted line, never inside a quoted pair).
How Numa expects Claude to work (persistence, plain language, build when clear) is in CLAUDE.md.
For the AppDeploy app only: AppDeploy reformats stored source with Prettier; base any diff against the app on its stored snapshot (`src_read`).
Security (October 2026): every page, the portfolio copies included, opens its head with the charset line, then a Content-Security-Policy meta tag and `<meta name="referrer" content="strict-origin-when-cross-origin">`. The policy admits the site's own files and AppDeploy's injected overlay (script from v2.appdeploy.ai, beacons to api-v2.appdeploy.ai, images from appdeploy.ai, the one install-prompt file on unpkg.com) and nothing else; inline scripts stay allowed because every page keeps its code inline and AppDeploy injects inline scripts when it serves a page. The Hydraulic Press Study's page alone adds `'unsafe-eval'` to `script-src` and `blob:` to `worker-src` (its solver worker is built at run time from a `blob:` address); a meta policy binds only its own page. A new page copies both meta tags; a new outside resource needs its origin added to the policy in every page. Fonts are self-hosted in `fonts/` (`plex.css`, `instrument-plex.css`, and `arabic.css` for Arabic pages only; IBM Plex and Instrument Serif under the SIL Open Font License, `fonts/OFL-*.txt`), the same files Google Fonts serves: never link fonts.googleapis.com again, it sends every visitor's address to Google. After copying a portfolio build, replace its `@import"https://fonts.googleapis.com/…"` with `@import"../../../fonts/instrument-plex.css"` and add the two meta tags. Response headers: on phyeinusul.com they come from `public/_headers` (nosniff, framing only by the site itself, referrer, permissions, opener isolation, HSTS for one year; see `docs/usul.md`); on the AppDeploy app they are AppDeploy's and cannot be set. The policy's AppDeploy origins are unused on Cloudflare and harmless.
