# Build files, tests and deployment

## Where the site runs

One source, two places (Cloudflare since 20 October 2026; GitHub Pages kept as a backup by Numa's decision of 29 October 2026). The
third row, the AppDeploy app, is history: AppDeploy reports it deleted on 29 October 2026 ([appdeploy-app.md](appdeploy-app.md)).

| | Address | Built from | How it is deployed |
|---|---|---|---|
| **Phyein Usul**, primary | <https://phyeinusul.com> | this repository's `main` | `npm run build`, then `npx wrangler deploy` (Cloudflare Worker `phyein-usul`, settings in `wrangler.jsonc`), run by Cloudflare Workers Builds on every push or merge to `main` since 21 October 2026: [usul.md](usul.md) |
| GitHub Pages, backup | <https://numa1997.github.io/SiteTest/> | this repository's `main`, as it is (no Vite build) | GitHub's "pages build and deployment" on every push to `main`: [usul.md](usul.md#github-pages) |
| AppDeploy app `numa-koudsie-website-0cyj78` | <https://numa-koudsie-website-0cyj78.v2.appdeploy.ai> | its own stored copy, v65, equal to commit `5c7ba7f`; deleted by 29 October 2026 (the address answers 404) | through AppDeploy's MCP server (below), only on Numa's request: [appdeploy-app.md](appdeploy-app.md) |

The repository comes first: a change is made and checked here, the documentation is brought up to date, the change is
committed on a branch, and it reaches Cloudflare when it is merged into `main`, which happens only on Numa's word. `README.md`,
`docs/` and `tools/` are not served by Cloudflare or AppDeploy; GitHub Pages serves the whole repository as it is.

Until 20 October 2026 the order was the other way round: the AppDeploy app was the deliverable and this repository its copy.
AppDeploy stores the source of each deployed version (its *stored snapshot*). Checked on 14 October 2026 against stored version `1792010233353`: the app lists 238 files (`src_glob`), the repository
holds the same 238 paths; `vite.config.ts` was restored to the app's version, and `tests/tests.json` here is newer than the
app's (see below). Sampled files served by the live site are byte-identical to the repository (fonts, thumbnails, KaTeX,
the study PDF and ZIP, `fold.css`, `robots.txt`); the HTML pages differ only by what the platform injects (next section).

## What happens on an AppDeploy deploy

This section and the next describe the AppDeploy app only. On Cloudflare the build is the same `vite build`, and
`dist/` is served exactly as built: no overlay, no rewritten links, no QA run ([usul.md](usul.md)).

1. **Upload.** The files are sent to AppDeploy through its MCP server (the only interface it offers; it signs in with
   Google, Apple or X, and has no key for unattended scripts). Many or binary files go through `upload_assets`: it returns a
   one-time address, the files are sent there in one multipart `PUT` with a JSON manifest, and the returned upload id is
   passed to `deploy_app`.
2. **Build.** The platform runs the build of `package.json` (`vite build`). Vite treats the root `index.html` as the entry
   page and copies everything under `public/` unchanged into the output folder (`dist/`, or the folder named by
   `APPDEPLOY_VITE_OUT_DIR`). So `public/simulations/water-wave.html` is served at `/simulations/water-wave.html`, and every
   page and script under `public/` reaches the browser exactly as written.
3. **QA.** The platform runs its own black-box tests against the live app, written in `tests/tests.json` (below).
4. **Status.** `get_app_status` reports `deploying`, then `ready` or `failed`, with QA results and runtime errors.
   `get_app_versions` lists earlier versions; `apply_app_version` rolls back to one.

### What AppDeploy changes on the way (observed)

| Change | Effect | How the site copes |
|---|---|---|
| Stored source is reformatted with Prettier (a code formatter). | Line breaks and indentation of stored files can differ from what was uploaded. | Base every diff on the stored snapshot (`src_read`), not on an older local copy. |
| Served HTML gets AppDeploy's overlay (an inline bootstrap script and `https://v2.appdeploy.ai/shared/js/overlay.js`, placed before `<html>`), a `preconnect` line, touch icons, social-media `meta` tags and a link to a web-app manifest; the home page also gets a script that registers a Firebase push-notification service worker (`/sw.js`). | A served page is longer than its source; `</head>` moves. The overlay sends request timings to `api-v2.appdeploy.ai` and, on phones, offers an install prompt loaded from unpkg.com. The manifest link is relative (`./manifest.json`), so on sub-pages it points at a missing file and phones log a 403 (measured 16 October 2026; nothing visible). | The security policy admits exactly these ([Security](#security)). Compare served HTML with the source line by line, ignoring the injected lines. |
| A relative stylesheet link in a deployed HTML file (`./assets/…`, and since October 2026 `./static/…`) is rewritten to the site root. | The stylesheet is not found (403) and the page shows unstyled. | The two project copies add their stylesheet with a one-line script instead of a `<link>` ([portfolios.md](portfolios.md)). |
| Unicode escapes in served JavaScript are written out as characters; CSV line endings are normalised. | Served `.js` and `.csv` files can differ byte-wise from the source while behaving the same. | Compare such files by content, not bytes. |
| A folder address (`…/rotor-pendula/`) answered 403 until mid-October 2026; on 16 October it answered 200 with the folder's `index.html`. | Links to folders may fail again if the platform changes back. | Always link to `…/index.html`. |
| A file removed with `deletePaths` is gone from the stored source but still answers 200 for a while (seen for the old copy bundles after version `1792109157210`). | A stale address keeps working, so a missing link is not caught by the live site. | Check deletions with `src_glob`, not with a fetch; nothing links to the old hashed names. |

## Security

Since 16 October 2026 (app version `1792151590518`) every page, the project pages included, carries two `meta` tags right
after its charset line (lines 5 and 6, for example [index.html:5–6](../index.html#L5-L6)). Two studies differ: the Hydraulic
Press Study (`portfolios/hydraulics/index.html`, added 21 October 2026, and its `de.html` and `ar.html`) and Rotor Pendula
(`portfolios/rotor-pendula/index.html`, generated since 23 October 2026) add `'unsafe-eval'` to `script-src` and `blob:` to
`worker-src`, because their solver runs in a Web Worker built at run time and started from a `blob:` address; a policy in a
`meta` tag binds only the page that carries it ([portfolios.md](portfolios.md#the-hydraulic-press-study-hydraulics)). Fig. 7,
`simulations/phasor-sums.html`, adds `media-src 'self' blob:` (since 29 October 2026): Auto Dance plays the audio file the
reader picks from a `blob:` address, which `default-src 'self'` refused, so before that Auto Dance heard nothing:

- a **Content-Security-Policy**: a list, read by the visitor's browser, of the only places the page may load code, styles, fonts,
  images and data from. Anything else is refused before it runs;
- a **referrer rule** (`strict-origin-when-cross-origin`): a site the reader follows a link to learns only that the visit came
  from this site, not from which page.

The policy, one directive per row:

| Directive | Allows | Why |
|---|---|---|
| `default-src` | `'self'` | Whatever no row below names may come only from this site. |
| `script-src` | `'self' 'unsafe-inline' https://v2.appdeploy.ai` and one file on unpkg.com | The site's scripts; code written inside the pages (every page keeps its code inline, and AppDeploy injects inline scripts when it serves a page); AppDeploy's overlay; the install-prompt library the overlay loads on phones, exactly one file, which the overlay checks against a SHA-384 fingerprint. |
| `style-src` | `'self' 'unsafe-inline'` | The stylesheets; inline styles (KaTeX writes them, and so does the overlay). |
| `img-src` | `'self' data: blob: https://appdeploy.ai` | Images of the site, the inline SVG favicons (`data:`), canvas exports (`blob:`), the overlay's icons. |
| `font-src` | `'self' data:` | The self-hosted fonts ([assets.md](assets.md)); the fonts that the Hydraulic Press Study and Rotor Pendula carry inline as `data:` addresses (until 23 October 2026 also one font in the app copies' stylesheets). |
| `connect-src` | `'self' https://api-v2.appdeploy.ai` | Requests for the site's own files (the former app copies loaded their data this way; the generated project pages fetch nothing, checked 29 October 2026); the overlay's timing reports. |
| `worker-src` | `'self'` | AppDeploy's service worker (the solver workers of the Hydraulic Press Study and Rotor Pendula start from `blob:` addresses, which their own policy adds). |
| `manifest-src` | `'self'` | The web-app manifest AppDeploy links. |
| `object-src` | `'none'` | No plugins. |
| `base-uri` | `'self'` | A slipped-in `<base>` tag cannot redirect the page's relative links to another site. |
| `form-action` | `'self'` | No form can send what a reader types to another site. |
| `upgrade-insecure-requests` | | Any `http://` address in a page is fetched as `https://`. |

The full policy as it stands in every page (except the two studies and Fig. 7 above, and the CV page `cv/index.html`, whose stricter policy
allows no inline script and no AppDeploy origin and which has no referrer tag; checked 29 October 2026):

```
default-src 'self'; script-src 'self' 'unsafe-inline' https://v2.appdeploy.ai https://unpkg.com/@khmyznikov/pwa-install@0.6.3/dist/pwa-install.bundle.js; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https://appdeploy.ai; font-src 'self' data:; connect-src 'self' https://api-v2.appdeploy.ai; worker-src 'self'; manifest-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests
```

**What it does and does not do.** It stops code and data from any other site: an injected `<script src="https://…">` would not
load, and nothing the page knows could be sent elsewhere. It does not stop code written inside a page (`'unsafe-inline'`); that
door is closed a different way: no reader input ever reaches a page as HTML. The catalog's search text is written with
`textContent` ([simulations.html:286](../public/simulations.html#L286)), its field and year filters must match a
fixed list, and the `#…` part of an address is only used to look up an element by its `id` ([fold.js:260–263](../public/scripts/fold.js#L260-L263)). Checked by reading every place the pages take input from the address, on 16 October 2026.

**Outside the AppDeploy app's reach** (on phyeinusul.com these are set: `public/_headers`, see [usul.md](usul.md#security)). Response headers (`Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, a
policy sent as a header) are set by the server, and AppDeploy serves the files from Amazon S3 through CloudFront with no
setting for them (as of October 2026). A policy in a `meta` tag cannot forbid framing (`frame-ancestors` is ignored there), so
another site can still show these pages inside a frame. The site's source files are not served (`AGENTS.md`, `package.json`,
source maps: 403), and plain `http://` is redirected to `https://` (301). (The GitHub Pages backup, by contrast, serves every file of the
repository, `AGENTS.md` included: status 200 on 29 October 2026. The repository is public anyway; [usul.md](usul.md#github-pages).) The strongest protection of all is not in the code:
whoever signs in to the AppDeploy account can replace the app, and whoever signs in to the Cloudflare account or can push to this
repository can replace phyeinusul.com, so those accounts and their e-mail need two-step sign-in.

On phyeinusul.com the AppDeploy addresses in the policy are unused (nothing injects the overlay there), so they allow nothing that
loads; they stay so that one page works on both hosts.

**How it was tested.** On 16 October 2026, in headless Chromium, on all 15 pages of the time (51 HTML pages on 29 October), desktop and a phone profile, before and after
the deploy: no request refused by the policy, no script error, no request to Google, and, read from Chromium's own font
report, the same font for every sampled text element (83 to 413 per page) as with the Google-hosted fonts. To check the live
site by hand (while the app existed): `curl -s https://numa-koudsie-website-0cyj78.v2.appdeploy.ai/ | grep -c Content-Security-Policy` printed `1`; in the
browser's developer tools, the Network tab shows no request to `fonts.googleapis.com`.

**Rules for later changes.**
1. A new page copies lines 5–6 of any page. On phyeinusul.com, `public/_headers` covers it by itself (`/*`).
2. A new outside resource (a script, a font, an image from another site) needs its origin added to the policy in all 15 pages,
   and [tools/make_portfolio_copy.py](../tools/make_portfolio_copy.py) takes the policy from `index.html`. Without it the browser
   refuses the resource and logs a `Refused to load` error.
3. Never link Google Fonts again; refresh the self-hosted copies instead ([assets.md](assets.md)).
4. If AppDeploy changes its overlay (a new address, a new version of the install prompt), the browser console of the live site
   shows a `Refused to load` error naming the address; add it to the policy.

## Build files at the root

These files come from AppDeploy's static-site template (`"name": "html-static-app"`). Only part of them affects the site.

| File | What it does here |
|---|---|
| [`index.html`](../index.html) | The home page, and Vite's entry page. Documented in [pages.md](pages.md). |
| [`package.json`](../package.json) | Declares the build: `vite build` (also `vite` for a development server and `vite preview`). Dependencies: Vite 6, TypeScript 5.7, Tailwind CSS 3.4 with PostCSS and Autoprefixer, `lucide` (icons) and an optional Rollup binary for Linux. The site uses none of Tailwind, TypeScript or lucide (next rows); Vite is the only one that matters. |
| [`vite.config.ts`](../vite.config.ts) | `base: './'` makes every address in the build relative, so the site works from any folder. `outDir` and `sourcemap` follow the platform's environment variables. `maxParallelFileOps: 128` lets Rollup copy many files at once. |
| [`tsconfig.json`](../tsconfig.json) | TypeScript settings for `src/`. Strict mode, no output (`noEmit`): Vite compiles, TypeScript only checks. |
| [`tailwind.config.js`](../tailwind.config.js), [`postcss.config.js`](../postcss.config.js) | Tailwind would scan `index.html` and `src/` for utility classes, and PostCSS would run Tailwind and Autoprefixer over CSS that Vite processes. |
| [`src/main.ts`](../src/main.ts), [`src/styles.css`](../src/styles.css) | The template's script entry (it only imports the stylesheet) and the three Tailwind directives. **Unused:** `index.html` does not load `src/main.ts` (`grep -n 'main.ts' index.html` finds nothing), so neither file reaches the site, and Tailwind's classes are never generated. They are kept because the AppDeploy app's stored source has them and its build expects them. |

## `tests/tests.json` · the platform's QA scenarios

A list of seventeen test scenarios written in plain language (AppDeploy only; Cloudflare runs no tests). After each deploy, AppDeploy's QA agent opens the live site in a
browser and follows them, the way a person would. Each scenario has:

| Field | Meaning |
|---|---|
| `name` | One-line title. |
| `sanity` | `true` only for the critical home workflow run first. |
| `viewport` | `desktop` or `mobile`. |
| `covers` | The features the scenario touches. |
| `description` | What is being verified. |
| `steps` | What to click or type, in order. |
| `expected` | What must be on screen at the end. |

The scenarios cover: the home page and its index; the simulations catalog (order, field chip, search, links both
ways); the double pendulum's controls and chaos twin; the double slit's Greek letters and path difference; the wave
workbench on a phone; the Fig. 1 data panel (variables, an array as a table, one recorded round); the Fig. 2 data panel
(state vector, energy); Fig. 6 Read values with the three-way check and the dataset download; the data sheet on a phone
(Fig. 5); Fig. 9 solving before playing and its lecture note; Fig. 10 re-solving after a controller change; the Portfolios
page and the droplet copy; the exact wave-bench repeat and empty sum; the zero-speed phasor recording guard and recovery; the
home fold tools at the intermediate breakpoint; stored results driving the visible values; and the shared tools after the
unused-code cleanup.

**Brought up to date on 14 October 2026.** The app's stored `tests/tests.json` was an older version: its first scenario
looked for a footer reading "Claude version", while the footer reads "© 2026 Numa Koudsie"
([index.html:617](../index.html#L617), which since reads "© 2026 Numa Koudsie · Built with Claude (Anthropic) · …"); and the second scenario expected the catalog to open with ten full entries, while its
cards now open as closed titles that a chip or a search opens. Both scenarios now describe the site as it is; the second was
followed step by step in headless Chromium before it was written down (ten closed titles and "10 shown"; the chip Wave optics
opens Figs. 1 and 3 with picture, equation and button, "2 of 10 shown"; the search "runge" opens Fig. 2 alone; the links go
there and back). The same file was deployed to the app.

## `AGENTS.md` and `CLAUDE.md`

Both live at the root of this repository (and of the AppDeploy app); neither is served to readers.
[`AGENTS.md`](../AGENTS.md) is the maintainer's summary of the project: what may be changed, the layout, the design rules,
the fold mechanism, the data pipeline, the AppDeploy quirks, the security rules, where the site runs. [`CLAUDE.md`](../CLAUDE.md) records how Numa expects an AI
assistant to work on the project: persistence, plain language, the repository as the source of the live site, data tables as a pipeline,
the house design and the lecture-note style.

## Minor-fix batch A · 15 October 2026

Deployed stored version `1792048596599`, then copied the same eleven files here. All ten Batch A faults were reproduced before editing. The live site passed the numerical and pixel checks at 1440 × 900 and 390 × 844, including the 960 × 900 hidden-layer case. The 600-sample test retains the end frame; archive READMEs name their own downloads and arrays and CRCs load correctly. The first QA scenario is unchanged; fifteen scenarios use only the home workflow as sanity. Evidence: [minor-issues-report.md](minor-issues-report.md).

Batch B, 15 October 2026: deployed snapshot 1792051419526. Targeted local and live Chromium checks and all 26 page/viewport checks passed; platform frontend/network error lists were empty. The suite has 15 scenarios with the original home scenario unchanged.

Batch C, 15 October 2026: all targeted excerpts match complete source lines or explicitly mark omissions. Local and live Chromium checks pass at both requested sizes. The Fourier sample/coefficient array hashes are unchanged; effective morph alpha now reads 1.00 when smoothing is off.

Batch D, 15 October 2026: stored-value and actual DOM/SVG/pixel checks pass locally and live at both requested viewports. The Square preset is exact at its intended decimal values, and an opaque white canvas no longer passes a component-wave readback.

Batch E, 15 October 2026: global rg included all pages, scripts and embedded project bundles. At 1440 × 900 and 390 × 844, 26 visible-element comparisons of 11 style properties and all stored typed-array hashes match before cleanup. Local and live smoke, exports and round endpoint pass; Batch D stored-value readbacks also pass after cleanup locally. One live fold-shadow comparison needed a settled-transition recheck, which matched. No package was installed. Five batches were deployed separately and pushed to the session branch; GitHub Pages was not changed.

Audit repairs, 15–16 October 2026: Droplet Collection v11 (`1792108231309`) and Rotor Pendula v5 (`1792108602425`) went out through the deploy tool's inline diffs, with no front-end or network errors reported by the platform's QA. The website update that carries the four corrected notes and the copies rebuilt on KaTeX 0.16.47 is stored version `1792109157210` (v63), sent as one upload of ten files and four deletions. See [research-theory-audit.md](research-theory-audit.md).

Second repairs of the theory revision, 16 October 2026: Droplet Collection v12 (`1792111079794`), Rotor Pendula v6 (`1792111084380`) and the website v64 (`1792111100165`: eight notes and both copies rebuilt), each through one upload. The platform's QA reported no front-end or network errors.

