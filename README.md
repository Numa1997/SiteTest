# Phyein Usul · Numa Koudsie's physics website — source and documentation

This repository is the source of Numa Koudsie's physics website, **Phyein Usul**: eleven interactive simulations, each with a
lecture note and a data panel, four research projects, and a CV, in English, German and Arabic. One source, three places where it runs:

| | Address | Built from | Doc |
|---|---|---|---|
| **Phyein Usul** (primary, since 20 October 2026) | **<https://phyeinusul.com>** | this repository's `main`, served by Cloudflare | [docs/usul.md](docs/usul.md) |
| GitHub Pages (backup, kept on since Numa's decision of 29 October 2026) | <https://numa1997.github.io/SiteTest/> | `main` as it is, without the Vite build (see the doc) | [docs/usul.md](docs/usul.md#github-pages) |
| The AppDeploy app `numa-koudsie-website-0cyj78` (kept as it is) | <https://numa-koudsie-website-0cyj78.v2.appdeploy.ai> | its own stored copy, equal to `main` at `5c7ba7f` | [docs/appdeploy-app.md](docs/appdeploy-app.md) |

Beside the site's files, `docs/` explains every file and every script and how they work.

## What is where

| Path | What it holds | Explained in |
|---|---|---|
| `index.html` | The home page. | [docs/pages.md](docs/pages.md) |
| `public/simulations/` | The eleven simulation pages, one self-contained HTML file each. | [docs/simulations/](docs/simulations/) |
| `public/simulations.html`, `public/portfolios.html` | The simulations catalog and the Portfolios page. | [docs/pages.md](docs/pages.md) |
| `public/scripts/` | Shared JavaScript: helpers, data store, data panel, folds, the catalog registry, and the walkthroughs in `walk/`. | [docs/scripts/](docs/scripts/) |
| `public/styles/` | The eight stylesheets, and the right-to-left copies `*.rtl.css` that `tools/i18n/build.py` writes for the Arabic pages. | [docs/styles.md](docs/styles.md) |
| `public/vendor/katex/`, `public/fonts/`, `public/images/` | The maths typesetter, the typefaces (Latin Modern, IBM Plex, Instrument Serif, all served by the site itself), the thumbnails in `images/sims/` and the logo `images/phyein-usul-mark.svg`. | [docs/assets.md](docs/assets.md) |
| `public/portfolios/` | The four research projects, each generated from its source in `portfolios-src/` and never edited by hand: Droplet Collection, Rotor Pendula, the Hydraulic Press Study and Iron, Cotton and the Head (the last two also in German and Arabic, `de.html`, `ar.html`). | [docs/portfolios.md](docs/portfolios.md) |
| `portfolios-src/droplets/`, `portfolios-src/rotor-pendula/` | The sources of Droplet Collection and Rotor Pendula (since 23 October 2026; before, copies of their AppDeploy apps): texts, models, generators and checks. Not served. | [docs/portfolios.md](docs/portfolios.md) |
| `portfolios-src/hydraulics/` | The Hydraulic Press Study's source: its three pages, the textbook's sources, the generator and its checks. Not served. | [docs/portfolios.md](docs/portfolios.md#the-hydraulic-press-study-hydraulics) |
| `portfolios-src/impact/` | Source of Iron, Cotton and the Head: the model, the page template, the English, German and Arabic texts, the generator and its checks. Not served. | [docs/portfolios.md](docs/portfolios.md#iron-cotton-and-the-head-impact) |
| `public/de/`, `public/ar/`, `i18n/`, `tools/i18n/` | The German and Arabic pages, written by `tools/i18n/build.py` from the English pages and the tables in `i18n/<lang>/` (since 23 October 2026; never edited by hand). | [docs/i18n.md](docs/i18n.md) |
| `notes/` | Work records of the lecture-note rewrites and studies (plans, checks, reviews), and the house standard `notes/STANDARD.md`. Not served. | [docs/notes.md](docs/notes.md) |
| `package.json`, `vite.config.ts`, `tsconfig.json`, `tailwind.config.js`, `postcss.config.js`, `src/` | Build files (Vite; first from AppDeploy's template). | [docs/build-and-deploy.md](docs/build-and-deploy.md) |
| `public/_headers`, `wrangler.jsonc` | Cloudflare's security headers and deployment settings for phyeinusul.com. | [docs/usul.md](docs/usul.md) |
| `tests/tests.json` | The test scenarios AppDeploy runs after each deploy of the app. | [docs/build-and-deploy.md](docs/build-and-deploy.md) |
| `AGENTS.md`, `CLAUDE.md` | The maintainer's summary, and how an AI assistant is to work on the project. | [docs/build-and-deploy.md](docs/build-and-deploy.md) |
| `docs/` | This documentation. [docs/files.md](docs/files.md) lists every file with what it is. | — |
| `tools/` | Scripts for maintaining the repository. | [docs/files.md](docs/files.md) |

## Reading order

1. [docs/architecture.md](docs/architecture.md): the map. How pages, shared scripts, the data store, the data panel and
   the folds fit together.
2. One simulation, for example [Fig. 2, the double pendulum](docs/simulations/fig02-double-pendulum.md): the physics, the
   numerical method, every function, the controls, what goes into the data store.
3. The shared scripts it uses: [sim.js](docs/scripts/sim.md), [dataset.js](docs/scripts/dataset.md),
   [datalog.js](docs/scripts/datalog.md), [fold.js](docs/scripts/fold.md), [the walkthroughs](docs/scripts/walk.md).
4. [docs/files.md](docs/files.md) whenever you meet a file and want to know what it is.

## The simulations

| Fig. | Title | Page | Explained in |
|---|---|---|---|
| 1 | Wave Interference | [`Circular Wave Interference Visualization.html`](public/simulations/Circular%20Wave%20Interference%20Visualization.html) | [fig01-wave-sources.md](docs/simulations/fig01-wave-sources.md) |
| 2 | Double Pendulum | [`Double Pendulum.html`](public/simulations/Double%20Pendulum.html) | [fig02-double-pendulum.md](docs/simulations/fig02-double-pendulum.md) |
| 3 | Double-Slit Interference | [`Interactive Double-Slit Experiment Visualization.html`](public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html) | [fig03-double-slit.md](docs/simulations/fig03-double-slit.md) |
| 4 | Transverse & Longitudinal | [`Transverse and longitudinal waves.html`](public/simulations/Transverse%20and%20longitudinal%20waves.html) | [fig04-transverse-longitudinal.md](docs/simulations/fig04-transverse-longitudinal.md) |
| 5 | Circular Water Waves | [`water-wave.html`](public/simulations/water-wave.html) | [fig05-water-wave.md](docs/simulations/fig05-water-wave.md) |
| 6 | Wave Interference Simulator | [`wave-interference.html`](public/simulations/wave-interference.html) | [fig06-wave-bench.md](docs/simulations/fig06-wave-bench.md) |
| 7 | Phasor Sums | [`phasor-sums.html`](public/simulations/phasor-sums.html) | [fig07-phasor-sums.md](docs/simulations/fig07-phasor-sums.md) |
| 8 | Draw & Decompose | [`draw-decompose.html`](public/simulations/draw-decompose.html) | [fig08-draw-decompose.md](docs/simulations/fig08-draw-decompose.md) |
| 9 | Driven Oscillator | [`driven-oscillator.html`](public/simulations/driven-oscillator.html) | [fig09-driven-oscillator.md](docs/simulations/fig09-driven-oscillator.md) |
| 10 | Wind Turbine Control | [`wind-turbine.html`](public/simulations/wind-turbine.html) | [fig10-wind-turbine.md](docs/simulations/fig10-wind-turbine.md) |
| 11 | Double Pendulum under Control | [`pendulum-control.html`](public/simulations/pendulum-control.html) | [fig11-pendulum-control.md](docs/simulations/fig11-pendulum-control.md) |

## Running the site on your own computer

The pages are static files, so any file server will do. The home page sits at the root and everything else under
`public/`, the way the build lays them side by side; put them together in one folder first:

```bash
mkdir -p /tmp/site
cp -r public/. /tmp/site/
cp index.html /tmp/site/
python3 -m http.server 8000 -d /tmp/site
```

Then open <http://localhost:8000/>. Opening the HTML files directly from disk is not enough: links from the home page
expect the other pages beside it, and the pages load the shared fonts, scripts and the KaTeX files from the site root.
This recipe was checked on 14 October 2026 (the site had 13 pages then): all 13 pages load in headless Chromium with no script errors, no maths errors,
no broken links or images and no sideways scroll, on a desktop and a phone-sized window.

Or build it as Cloudflare serves it: `npm install`, `npm run build`, then `npx wrangler dev` (see [docs/usul.md](docs/usul.md)).

## How a change travels

The repository comes first (since 20 October 2026). A change is made here, built and checked in a browser, the pages of
`docs/` that describe it are brought up to date, `python3 tools/inventory.py` rewrites the file list, the change is
committed on a branch and merged into `main` on Numa's word; Cloudflare Workers Builds then builds and publishes it to
phyeinusul.com by itself (since 21 October 2026; [docs/usul.md](docs/usul.md)), and GitHub Pages republishes `main` as a backup. The AppDeploy app gets
the same files only when Numa asks ([docs/appdeploy-app.md](docs/appdeploy-app.md)); how AppDeploy builds and alters a
deploy is in [docs/build-and-deploy.md](docs/build-and-deploy.md).

The [theory readability audit](docs/research-theory-audit.md) records the selective teaching revisions to the ten lecture notes and both research projects, with the mathematical corrections and verification scope.
