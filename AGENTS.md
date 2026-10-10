# Claude version — ownership and update notes

This is the Claude copy of Numa Koudsie's physics portfolio: AppDeploy app `numa-koudsie-website-0cyj78`.
Owner: Numa. Changes need Numa's explicit request.

Out of bounds for writes: the GitHub source `Numa1997/SiteTest`, the ChatGPT version `numa-physics-lab-chatgpt-k0ixwk`
(its earlier copy `sitetest-chatgpt-r14hvr` was deleted), and the unrelated app `physik-radar-xvy59b`. This is a project instruction, not a technical access control.

Layout (GitHub Pages serves the repository root as-is, so every asset lives at the root): `index.html`; `styles/site.css` and `styles/sim.css`;
`scripts/sim.js` (shared helpers, openable derivation cards, walkthrough engine);
`scripts/walk/<key>.js` ("From symbols to code", one file per page, chosen by the page's `data-walk` key:
each equation paired with the page's own code lines; keep the excerpts identical to the page code when either
changes; live values come from `Sim.live()` in each page); `simulations/*.html` (eight pages).
AppDeploy reformats stored source with Prettier; base any diff on the stored snapshot (`src_read`).
Static site only: no backend, database, login, AI or scheduled jobs.
