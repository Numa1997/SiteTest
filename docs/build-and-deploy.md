# Build files, tests and deployment

## The repository and the app are one tree

The website runs as the AppDeploy app **`numa-koudsie-website-0cyj78`** ("Numa Koudsie website"), live at
<https://numa-koudsie-website-0cyj78.v2.appdeploy.ai>. AppDeploy stores the source of each deployed version (its *stored
snapshot*). This repository holds that same source, file for file and at the same paths, plus three things that are not part
of the app: `README.md`, `docs/` and `tools/`.

The live app is the deliverable; the repository is its documented copy. A change is made and checked in the app first, then
the same files are copied here at the same paths, the documentation is brought up to date, and the change is committed.

Checked on 14 October 2026 against stored version `1792010233353`: the app lists 238 files (`src_glob`), the repository
holds the same 238 paths; `vite.config.ts` was restored to the app's version, and `tests/tests.json` here is newer than the
app's (see below). Sampled files served by the live site are byte-identical to the repository (fonts, thumbnails, KaTeX,
the study PDF and ZIP, `fold.css`, `robots.txt`); the HTML pages differ only by what the platform injects (next section).

## What happens on a deploy

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

### What the platform changes on the way (observed)

| Change | Effect | How the site copes |
|---|---|---|
| Stored source is reformatted with Prettier (a code formatter). | Line breaks and indentation of stored files can differ from what was uploaded. | Base every diff on the stored snapshot (`src_read`), not on an older local copy. |
| Served HTML gets an overlay script, a `preconnect` line and touch icons injected into `<head>`. | A served page is longer than its source; `</head>` moves. | Nothing to do. Compare served HTML with the source line by line, ignoring the injected lines. |
| A relative stylesheet link in a deployed HTML file (`./assets/…`, and since October 2026 `./static/…`) is rewritten to the site root. | The stylesheet is not found (403) and the page shows unstyled. | The two project copies add their stylesheet with a one-line script instead of a `<link>` ([portfolios.md](portfolios.md)). |
| Unicode escapes in served JavaScript are written out as characters; CSV line endings are normalised. | Served `.js` and `.csv` files can differ byte-wise from the source while behaving the same. | Compare such files by content, not bytes. |
| A folder address (`…/rotor-pendula/`) answers 403. | Links to folders fail. | Always link to `…/index.html`. |
| A file removed with `deletePaths` is gone from the stored source but still answers 200 for a while (seen for the old copy bundles after version `1792109157210`). | A stale address keeps working, so a missing link is not caught by the live site. | Check deletions with `src_glob`, not with a fetch; nothing links to the old hashed names. |

## Build files at the root

These files come from AppDeploy's static-site template (`"name": "html-static-app"`). Only part of them affects the site.

| File | What it does here |
|---|---|
| [`index.html`](../index.html) | The home page, and Vite's entry page. Documented in [pages.md](pages.md). |
| [`package.json`](../package.json) | Declares the build: `vite build` (also `vite` for a development server and `vite preview`). Dependencies: Vite 6, TypeScript 5.7, Tailwind CSS 3.4 with PostCSS and Autoprefixer, `lucide` (icons) and an optional Rollup binary for Linux. The site uses none of Tailwind, TypeScript or lucide (next rows); Vite is the only one that matters. |
| [`vite.config.ts`](../vite.config.ts) | `base: './'` makes every address in the build relative, so the site works from any folder. `outDir` and `sourcemap` follow the platform's environment variables. `maxParallelFileOps: 128` lets Rollup copy many files at once. |
| [`tsconfig.json`](../tsconfig.json) | TypeScript settings for `src/`. Strict mode, no output (`noEmit`): Vite compiles, TypeScript only checks. |
| [`tailwind.config.js`](../tailwind.config.js), [`postcss.config.js`](../postcss.config.js) | Tailwind would scan `index.html` and `src/` for utility classes, and PostCSS would run Tailwind and Autoprefixer over CSS that Vite processes. |
| [`src/main.ts`](../src/main.ts), [`src/styles.css`](../src/styles.css) | The template's script entry (it only imports the stylesheet) and the three Tailwind directives. **Unused:** `index.html` does not load `src/main.ts` (`grep -n 'main.ts' index.html` finds nothing), so neither file reaches the site, and Tailwind's classes are never generated. They are kept because the app's stored source has them; removing them is a change to make in the app first. |

## `tests/tests.json` · the platform's QA scenarios

A list of fourteen test scenarios written in plain language. After each deploy, AppDeploy's QA agent opens the live site in a
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

The fifteen scenarios cover: the home page and its index; the simulations catalog (order, field chip, search, links both
ways); the double pendulum's controls and chaos twin; the double slit's Greek letters and path difference; the wave
workbench on a phone; the Fig. 1 data panel (variables, an array as a table, one recorded round); the Fig. 2 data panel
(state vector, energy); Fig. 6 Read values with the three-way check and the dataset download; the data sheet on a phone
(Fig. 5); Fig. 9 solving before playing and its lecture note; Fig. 10 re-solving after a controller change; the Portfolios
page and the droplet copy; the exact wave-bench repeat and empty sum; and the zero-speed phasor recording guard and recovery.

**Brought up to date on 14 October 2026.** The app's stored `tests/tests.json` was an older version: its first scenario
looked for a footer reading "Claude version", while the footer reads "© 2026 Numa Koudsie"
([index.html:618](../index.html#L618)); and the second scenario expected the catalog to open with ten full entries, while its
cards now open as closed titles that a chip or a search opens. Both scenarios now describe the site as it is; the second was
followed step by step in headless Chromium before it was written down (ten closed titles and "10 shown"; the chip Wave optics
opens Figs. 1 and 3 with picture, equation and button, "2 of 10 shown"; the search "runge" opens Fig. 2 alone; the links go
there and back). The same file was deployed to the app.

## `AGENTS.md` and `CLAUDE.md`

Both live at the root of the app and of this repository; neither is served to readers.
[`AGENTS.md`](../AGENTS.md) is the maintainer's summary of the project: what may be changed, the layout, the design rules,
the fold mechanism, the data pipeline, the platform quirks. [`CLAUDE.md`](../CLAUDE.md) records how Numa expects an AI
assistant to work on the project: persistence, plain language, the app before the repository, data tables as a pipeline,
the house design and the lecture-note style.

## Minor-fix batch A · 15 October 2026

Deployed stored version `1792048596599`, then copied the same eleven files here. All ten Batch A faults were reproduced before editing. The live site passed the numerical and pixel checks at 1440 × 900 and 390 × 844, including the 960 × 900 hidden-layer case. The 600-sample test retains the end frame; archive READMEs name their own downloads and arrays and CRCs load correctly. The first QA scenario is unchanged; fifteen scenarios use only the home workflow as sanity. Evidence: [minor-issues-report.md](minor-issues-report.md).

Batch B, 15 October 2026: deployed snapshot 1792051419526. Targeted local and live Chromium checks and all 26 page/viewport checks passed; platform frontend/network error lists were empty. The suite has 15 scenarios with the original home scenario unchanged.

Batch C, 15 October 2026: all targeted excerpts match complete source lines or explicitly mark omissions. Local and live Chromium checks pass at both requested sizes. The Fourier sample/coefficient array hashes are unchanged; effective morph alpha now reads 1.00 when smoothing is off.

Batch D, 15 October 2026: stored-value and actual DOM/SVG/pixel checks pass locally and live at both requested viewports. The Square preset is exact at its intended decimal values, and an opaque white canvas no longer passes a component-wave readback.

Batch E, 15 October 2026: global rg included all pages, scripts and embedded project bundles. At 1440 × 900 and 390 × 844, 26 visible-element comparisons of 11 style properties and all stored typed-array hashes match before cleanup. Local and live smoke, exports and round endpoint pass; Batch D stored-value readbacks also pass after cleanup locally. One live fold-shadow comparison needed a settled-transition recheck, which matched. No package was installed. Five batches were deployed separately and pushed to the session branch; GitHub Pages was not changed.

Audit repairs, 15–16 October 2026: Droplet Collection v11 (`1792108231309`) and Rotor Pendula v5 (`1792108602425`) went out through the deploy tool's inline diffs, with no front-end or network errors reported by the platform's QA. The website update that carries the four corrected notes and the copies rebuilt on KaTeX 0.16.47 is stored version `1792109157210` (v63), sent as one upload of ten files and four deletions. See [research-theory-audit.md](research-theory-audit.md).

Second repairs of the theory revision, 16 October 2026: Droplet Collection v12 (`1792111079794`), Rotor Pendula v6 (`1792111084380`) and the website v64 (`1792111100165`: eight notes and both copies rebuilt), each through one upload. The platform's QA reported no front-end or network errors.
