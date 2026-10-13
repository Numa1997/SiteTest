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
Data panel, a pipeline in three files. `scripts/dataset.js`: `Sim.dataset()` gives a page one named store (dims, typed-array variables,
scalars, attrs; the shape of an xarray/NetCDF dataset) and the page writes every number into it at the line that computes it, every frame;
nothing is recomputed for display. `scripts/datalog.js` + `styles/data.css`: the panel, which only reads the store (Variables: name, type,
shape, value, live; any array opens as a table; Probe: point at the figure to read the stored values there, with a marker; Check: for any
value, the stored number, the formula recomputed from the stored inputs, and the pixel or SVG element read back from the picture, with the
agreement stated; Log: one row per 0.1 s; Save: NumPy .npz + dataset.json + log.csv + README). A page opts in by defining `Sim.data`
(the contract is documented at the top of datalog.js: groups, probe/inspect/locate, check, drawn, log, about) next to its own state and loading
dataset.js after sim.js and datalog.js after its own script (all eight figures). `Sim.live()` reads the store too. Keep the taps where the
page computes a value; keep the walkthrough excerpts untouched (insert after a quoted line, never inside a quoted pair).
How Numa expects Claude to work (persistence, plain language, build when clear) is in CLAUDE.md.
AppDeploy reformats stored source with Prettier; base any diff on the stored snapshot (`src_read`).
Static site only: no backend, database, login, AI or scheduled jobs.
