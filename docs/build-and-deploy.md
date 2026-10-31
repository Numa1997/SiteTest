# Build files and deployment

## Where the site runs

One source, two places: Cloudflare (since 20 October 2026) and GitHub Pages, kept as a backup by Numa's decision of
29 October 2026.

| | Address | Built from | How it is deployed |
|---|---|---|---|
| **Phyein Usul**, primary | <https://phyeinusul.com> | this repository's `main` | `npm run build`, then `npx wrangler deploy` (Cloudflare Worker `phyein-usul`, settings in `wrangler.jsonc`), run by Cloudflare Workers Builds on every push or merge to `main` since 21 October 2026: [usul.md](usul.md) |
| GitHub Pages, backup | <https://numa1997.github.io/SiteTest/> | this repository's `main`, as it is (no Vite build) | GitHub's "pages build and deployment" on every push to `main`: [usul.md](usul.md#github-pages) |

The repository comes first: a change is made and checked here, the documentation is brought up to date, the change is
committed on a branch, and it reaches Cloudflare when it is merged into `main`, which happens only on Numa's word. `README.md`,
`docs/` and `tools/` are not served by Cloudflare; GitHub Pages serves the whole repository as it is.

## The build

`npm run build` runs `vite build`. Vite treats the root `index.html` as the entry page and copies everything under `public/`
unchanged into the output folder (`dist/`, or the folder named by the environment variable `OUT_DIR`). So
`public/simulations/water-wave.html` is served at `/simulations/water-wave.html`, and every page and script under `public/`
reaches the browser exactly as written. Cloudflare serves `dist/` as built ([usul.md](usul.md)).

## Security

Every page, the project pages included, carries two `meta` tags right after its charset line (lines 5 and 6, for example
[index.html:5–6](../index.html#L5-L6)). Two studies differ: the Hydraulic Press Study (`portfolios/hydraulics/index.html`, and
its `de.html` and `ar.html`) and Rotor Pendula (`portfolios/rotor-pendula/index.html`) add `'unsafe-eval'` to `script-src` and
`blob:` to `worker-src`, because their solver runs in a Web Worker built at run time and started from a `blob:` address; a
policy in a `meta` tag binds only the page that carries it ([portfolios.md](portfolios.md#the-hydraulic-press-study-hydraulics)):

- a **Content-Security-Policy**: a list, read by the visitor's browser, of the only places the page may load code, styles, fonts,
  images and data from. Anything else is refused before it runs;
- a **referrer rule** (`strict-origin-when-cross-origin`): a site the reader follows a link to learns only that the visit came
  from this site, not from which page.

The policy, one directive per row:

| Directive | Allows | Why |
|---|---|---|
| `default-src` | `'self'` | Whatever no row below names may come only from this site. |
| `script-src` | `'self' 'unsafe-inline'` | The site's scripts, and code written inside the pages (every page keeps its code inline). |
| `style-src` | `'self' 'unsafe-inline'` | The stylesheets; inline styles (KaTeX writes them). |
| `img-src` | `'self' data: blob:` | Images of the site, the inline SVG favicons (`data:`), canvas exports (`blob:`). |
| `font-src` | `'self' data:` | The self-hosted fonts ([assets.md](assets.md)). `data:` stays allowed for fonts carried inline as `data:` addresses (the standalone copies of the Hydraulic Press Study and Rotor Pendula; since 31 October 2026 their site pages link the site's font files instead, [portfolios.md](portfolios.md)). |
| `connect-src` | `'self'` | Requests for the site's own files. |
| `worker-src` | `'self'` | Workers from the site (the solver workers of the Hydraulic Press Study and Rotor Pendula start from `blob:` addresses, which their own policy adds). |
| `object-src` | `'none'` | No plugins. |
| `base-uri` | `'self'` | A slipped-in `<base>` tag cannot redirect the page's relative links to another site. |
| `form-action` | `'self'` | No form can send what a reader types to another site. |
| `upgrade-insecure-requests` | | Any `http://` address in a page is fetched as `https://`. |

The full policy as it stands in every page (except the two studies above and the CV page `cv/index.html`, whose stricter
policy allows no inline script and which has no referrer tag):

```
default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests
```

**What it does and does not do.** It stops code and data from any other site: an injected `<script src="https://…">` would not
load, and nothing the page knows could be sent elsewhere. It does not stop code written inside a page (`'unsafe-inline'`); that
door is closed a different way: no reader input ever reaches a page as HTML. The catalog's search text is written with
`textContent` ([simulations.html:286](../public/simulations.html#L286)), its field and year filters must match a
fixed list, and the `#…` part of an address is only used to look up an element by its `id` ([fold.js:260–263](../public/scripts/fold.js#L260-L263)).

**Response headers** (framing, nosniff, referrer, permissions, opener isolation, HSTS) come from `public/_headers`, which
Cloudflare reads and never serves ([usul.md](usul.md#security)). The site's source files are not served on phyeinusul.com.
(The GitHub Pages backup, by contrast, serves every file of the repository, `AGENTS.md` included; the repository is public
anyway: [usul.md](usul.md#github-pages).) Whoever signs in to the Cloudflare account or can push to this repository can replace
phyeinusul.com, so those accounts and their e-mail need two-step sign-in.

**How it is tested.** In headless Chromium, on every page, desktop and a phone profile: no request refused by the policy, no
script error, no request to Google (`node notes/verify.mjs dist` covers the eleven simulations). In the browser's developer
tools, the Network tab shows no request to `fonts.googleapis.com`.

**Rules for later changes.**
1. A new page copies lines 5–6 of any page. `public/_headers` covers it by itself (`/*`).
2. A new outside resource (a script, a font, an image from another site) needs its origin added to the policy in every page; the
   portfolio generators take the policy from `index.html`. Without it the browser refuses the resource and logs a
   `Refused to load` error.
3. Never link Google Fonts again; refresh the self-hosted copies instead ([assets.md](assets.md)).

## Build files at the root

These files come from a Vite static-site template (`"name": "html-static-app"`). Only part of them affects the site.

| File | What it does here |
|---|---|
| [`index.html`](../index.html) | The home page, and Vite's entry page. Documented in [pages.md](pages.md). |
| [`package.json`](../package.json) | Declares the build: `vite build` (also `vite` for a development server and `vite preview`). Dependencies: Vite 6, TypeScript 5.7, Tailwind CSS 3.4 with PostCSS and Autoprefixer, `lucide` (icons) and an optional Rollup binary for Linux. The site uses none of Tailwind, TypeScript or lucide (next rows); Vite is the only one that matters. |
| [`vite.config.ts`](../vite.config.ts) | `base: './'` makes every address in the build relative, so the site works from any folder. `outDir` is `dist/` unless `OUT_DIR` names another folder; no source maps. `maxParallelFileOps: 128` lets Rollup copy many files at once. |
| [`tsconfig.json`](../tsconfig.json) | TypeScript settings for `src/`. Strict mode, no output (`noEmit`): Vite compiles, TypeScript only checks. |
| [`tailwind.config.js`](../tailwind.config.js), [`postcss.config.js`](../postcss.config.js) | Tailwind would scan `index.html` and `src/` for utility classes, and PostCSS would run Tailwind and Autoprefixer over CSS that Vite processes. |
| [`src/main.ts`](../src/main.ts), [`src/styles.css`](../src/styles.css) | The template's script entry (it only imports the stylesheet) and the three Tailwind directives. **Unused:** `index.html` does not load `src/main.ts` (`grep -n 'main.ts' index.html` finds nothing), so neither file reaches the site, and Tailwind's classes are never generated. |

## `AGENTS.md` and `CLAUDE.md`

Both live at the root of this repository; neither is served on phyeinusul.com.
[`AGENTS.md`](../AGENTS.md) is the maintainer's summary of the project: what may be changed, the layout, the design rules,
the fold mechanism, the data pipeline, the security rules, where the site runs. [`CLAUDE.md`](../CLAUDE.md) records how Numa expects an AI
assistant to work on the project: persistence, plain language, the repository as the source of the live site, data tables as a pipeline,
the house design and the lecture-note style.
