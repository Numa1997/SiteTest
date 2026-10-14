# Claude version — ownership and update notes

This is the Claude copy of Numa Koudsie's physics portfolio: AppDeploy app `numa-koudsie-website-0cyj78`.
Owner: Numa. Changes need Numa's explicit request.

Out of bounds for writes: the GitHub source `Numa1997/SiteTest`, the ChatGPT version `numa-physics-lab-chatgpt-k0ixwk`
(its earlier copy `sitetest-chatgpt-r14hvr` was deleted), and the unrelated app `physik-radar-xvy59b`. This is a project instruction, not a technical access control.

Layout (GitHub Pages serves the repository root as-is, so every asset lives at the root): `index.html`; `styles/site.css` and `styles/sim.css`;
`scripts/theme.js` (light/dark theme: stored choice else system setting, toggle buttons, `themechange` event; loaded in the home page head and by `sim.js`; in dark mode the simulation figures stay light paper plates);
`scripts/sim.js` (shared helpers, openable derivation cards, walkthrough engine);
`scripts/walk/<key>.js` ("From symbols to code", one file per page, chosen by the page's `data-walk` key:
each equation paired with the page's own code lines; keep the excerpts identical to the page code when either
changes; live values come from `Sim.live()` in each page); `simulations/*.html` (eight pages).
Simulations page: `simulations.html` lists every simulation as a card (thumbnail, the question it answers, model, method, what the reader
sets, concepts) in one grid ordered by field, with a search and field and year chips; the view lives in the address (`?q=&field=&stage=`).
It draws itself from the registry `scripts/catalog.js` (`SIMULATIONS`, `SIM_FIELDS`, `SIM_TOOLS`) with `styles/catalog.css`; thumbnails are
`images/sims/<id>.webp`, 800 × 500 px stills of each page's main figure. To add a simulation: its page in `simulations/`, one entry in
`SIMULATIONS` (and its field in `SIM_FIELDS` if new), its thumbnail (a missing one shows the Fig. number instead), and its number in the
hand-written Fig. links at the top of every simulation page. Simulation pages link back to `simulations.html`; the home page keeps its plates
and links to the catalog from the hero button, the section intro and a button under the plates.
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
