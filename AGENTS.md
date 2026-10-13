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
Data panel: `scripts/datalog.js` + `styles/data.css` give a page a Spyder-style side panel (Variables: name, type, size, value of every
quantity, live; any array opens as a table that draws only the cells in view; Log: one row per 0.1 s of play time, capped).
A page opts in by defining `Sim.data` next to its own state and loading both files (Fig. 1 so far).
How Numa expects Claude to work (persistence, plain language, build when clear) is in CLAUDE.md.
AppDeploy reformats stored source with Prettier; base any diff on the stored snapshot (`src_read`).
Static site only: no backend, database, login, AI or scheduled jobs.
