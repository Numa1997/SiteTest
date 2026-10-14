# Numa Koudsie website — ownership and update notes

This is Numa Koudsie's physics website: AppDeploy app `numa-koudsie-website-0cyj78`, display name "Numa Koudsie website".
Owner: Numa. Changes need Numa's explicit request.

The GitHub repository `Numa1997/SiteTest` is this app's copy: its root holds everything under `public/` plus `index.html`, and GitHub
Pages serves it as-is. Change the app first, then copy the change there, only when Numa asks.
Out of bounds for writes: the ChatGPT version `numa-physics-lab-chatgpt-k0ixwk` (its earlier copy `sitetest-chatgpt-r14hvr` was deleted)
and the unrelated app `physik-radar-xvy59b`. This is a project instruction, not a technical access control.

Layout (GitHub Pages serves the repository root as-is, so every asset lives at the root): `index.html`; `styles/site.css` and `styles/sim.css`;
`scripts/sim.js` (shared helpers, lecture-note typesetting, walkthrough engine);
`scripts/walk/<key>.js` ("From symbols to code", one file per page, chosen by the page's `data-walk` key:
each equation paired with the page's own code lines; keep the excerpts identical to the page code when either
changes; live values come from `Sim.live()` in each page); `simulations/*.html` (ten pages).
Simulations page: `simulations.html` lists every simulation as a paper abstract (thumbnail with a numbered caption, field and year,
summary, the key equation typeset by KaTeX, model, method, what the reader sets, concepts, links to the figure and to its lecture note) in
one grid in figure order, with a search and field and year chips; the view lives in the address (`?q=&field=&stage=`). It draws itself from
the registry `scripts/catalog.js` (`SIMULATIONS`, `SIM_FIELDS`, `SIM_TOOLS`) with `styles/catalog.css`; thumbnails are
`images/sims/<id>.webp`, 800 × 500 px stills of each page's main figure. To add a simulation: its page in `simulations/`, one entry in
`SIMULATIONS` (and its field in `SIM_FIELDS` if new), its thumbnail (a missing one shows the Fig. number instead), and its number in the
hand-written Fig. links at the top of every simulation page. Simulation pages link back to `simulations.html`; the home page keeps its plates
and links to the catalog from the hero button, the section intro and a button under the plates.
Design: the house design of `DESIGN.md` in the app `droplet-collection-yl7l26` (the reference; read it before changing styles): Instrument
Serif titles at weight 400 only, IBM Plex Sans text, IBM Plex Mono labels, every box outlined, no card shadows. Explanations are lecture
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
`portfolios/droplet-collection/` (app `droplet-collection-yl7l26`) and `portfolios/rotor-pendula/` (app `rotor-pendula-gafw0f`). Each is
the Vite build of its app without saved runs and backend (hash routes; link to `portfolios/<name>/index.html#/…`, since folder addresses
return 403), with a back link to `../../portfolios.html`. Their build folder is `static/`, not `assets/`. AppDeploy rewrites a relative
stylesheet link in a deployed HTML file to the site root (seen for `./assets/…` and, since October 2026, `./static/…`: both give 403), so
after building, replace the `<link rel="stylesheet" href="./static/….css">` in the copy's `index.html` with a short script that adds
the same link at run time (the platform leaves scripts alone); without it the copy shows unstyled. Their source stays in their apps;
rebuild there, copy the build folder here, then patch the stylesheet link.
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
after its own script (all eight figures). `Sim.live()` reads the store too. Keep the taps where the page computes a value; keep the
walkthrough excerpts untouched (insert after a quoted line, never inside a quoted pair).
How Numa expects Claude to work (persistence, plain language, build when clear) is in CLAUDE.md.
AppDeploy reformats stored source with Prettier; base any diff on the stored snapshot (`src_read`).
Static site only: no backend, database, login, AI or scheduled jobs.
