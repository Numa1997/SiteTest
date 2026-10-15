# Every file

Written by [`tools/inventory.py`](../tools/inventory.py) from the files in the repository; do not edit by hand.
Run `python3 tools/inventory.py` after adding, removing or changing files, and `python3 tools/inventory.py --check`
to confirm that every file is described. Sizes are those of the files when the list was written.

265 files, 10.8 MB in all. Runs of more than 12 similar files are folded; open them to see each file.

| Folder | Files |
|---|---|
| [Repository root](#repository-root) | 10 |
| [Pages under public/](#pages-under-public) | 3 |
| [Simulation pages](#simulation-pages) | 10 |
| [Walkthroughs](#walkthroughs) | 10 |
| [Shared scripts](#shared-scripts) | 5 |
| [Stylesheets](#stylesheets) | 7 |
| [KaTeX](#katex) | 24 |
| [Latin Modern](#latin-modern) | 5 |
| [Thumbnails](#thumbnails) | 10 |
| [Project copy: Droplet Collection](#project-copy-droplet-collection) | 69 |
| [Project copy: Rotor Pendula](#project-copy-rotor-pendula) | 84 |
| [Template sources](#template-sources) | 2 |
| [Platform tests](#platform-tests) | 1 |
| [Documentation](#documentation) | 24 |
| [Tools](#tools) | 1 |

## Repository root

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`.gitignore`](../.gitignore) | 39 B | Files git leaves out: Python caches, node_modules, build output. | [files.md](files.md) |
| [`AGENTS.md`](../AGENTS.md) | 8.5 kB | The maintainer's summary: ownership, layout, design rules, folds, the data pipeline, platform quirks. | [build-and-deploy.md](build-and-deploy.md) |
| [`CLAUDE.md`](../CLAUDE.md) | 4.2 kB | How Numa expects an AI assistant to work on the project. | [build-and-deploy.md](build-and-deploy.md) |
| [`README.md`](../README.md) | 6.1 kB | Start here: what the project is, how the files fit together, where each one is explained. | [README.md](../README.md) |
| [`index.html`](../index.html) | 46.4 kB | The home page: CV, research, simulation plates, index; also the build entry page. | [pages.md](pages.md) |
| [`package.json`](../package.json) | 479 B | Build declaration: vite build; template dependencies. | [build-and-deploy.md](build-and-deploy.md) |
| [`postcss.config.js`](../postcss.config.js) | 81 B | PostCSS settings (template; unused by the site). | [build-and-deploy.md](build-and-deploy.md) |
| [`tailwind.config.js`](../tailwind.config.js) | 155 B | Tailwind settings (template; unused by the site). | [build-and-deploy.md](build-and-deploy.md) |
| [`tsconfig.json`](../tsconfig.json) | 485 B | TypeScript settings for src/ (template; unused by the site). | [build-and-deploy.md](build-and-deploy.md) |
| [`vite.config.ts`](../vite.config.ts) | 310 B | Vite settings: relative base, output folder from the platform. | [build-and-deploy.md](build-and-deploy.md) |

## Pages under public/

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/portfolios.html`](../public/portfolios.html) | 22.0 kB | The Portfolios page: the two research projects. | [pages.md](pages.md) |
| [`public/robots.txt`](../public/robots.txt) | 58 B | Instructions for search-engine crawlers. | [pages.md](pages.md) |
| [`public/simulations.html`](../public/simulations.html) | 18.4 kB | The simulations catalog: one titled fold card per simulation, search and chips. | [pages.md](pages.md) |

## Simulation pages

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/simulations/Circular Wave Interference Visualization.html`](../public/simulations/Circular%20Wave%20Interference%20Visualization.html) | 188.9 kB | Fig. 1 · Wave Interference: the simulation, its data panel, walkthrough and lecture note. | [fig01-wave-sources.md](simulations/fig01-wave-sources.md) |
| [`public/simulations/Double Pendulum.html`](../public/simulations/Double%20Pendulum.html) | 100.7 kB | Fig. 2 · Double Pendulum: the simulation, its data panel, walkthrough and lecture note. | [fig02-double-pendulum.md](simulations/fig02-double-pendulum.md) |
| [`public/simulations/Interactive Double-Slit Experiment Visualization.html`](../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html) | 166.6 kB | Fig. 3 · Double-Slit Interference: the simulation, its data panel, walkthrough and lecture note. | [fig03-double-slit.md](simulations/fig03-double-slit.md) |
| [`public/simulations/Transverse and longitudinal waves.html`](../public/simulations/Transverse%20and%20longitudinal%20waves.html) | 197.9 kB | Fig. 4 · Transverse & Longitudinal: the simulation, its data panel, walkthrough and lecture note. | [fig04-transverse-longitudinal.md](simulations/fig04-transverse-longitudinal.md) |
| [`public/simulations/draw-decompose.html`](../public/simulations/draw-decompose.html) | 213.1 kB | Fig. 8 · Draw & Decompose: the simulation, its data panel, walkthrough and lecture note. | [fig08-draw-decompose.md](simulations/fig08-draw-decompose.md) |
| [`public/simulations/driven-oscillator.html`](../public/simulations/driven-oscillator.html) | 178.7 kB | Fig. 9 · Driven Oscillator: the simulation, its data panel, walkthrough and lecture note. | [fig09-driven-oscillator.md](simulations/fig09-driven-oscillator.md) |
| [`public/simulations/phasor-sums.html`](../public/simulations/phasor-sums.html) | 259.8 kB | Fig. 7 · Phasor Sums: the simulation, its data panel, walkthrough and lecture note. | [fig07-phasor-sums.md](simulations/fig07-phasor-sums.md) |
| [`public/simulations/water-wave.html`](../public/simulations/water-wave.html) | 159.7 kB | Fig. 5 · Circular Water Waves: the simulation, its data panel, walkthrough and lecture note. | [fig05-water-wave.md](simulations/fig05-water-wave.md) |
| [`public/simulations/wave-interference.html`](../public/simulations/wave-interference.html) | 166.4 kB | Fig. 6 · Wave Interference Simulator: the simulation, its data panel, walkthrough and lecture note. | [fig06-wave-bench.md](simulations/fig06-wave-bench.md) |
| [`public/simulations/wind-turbine.html`](../public/simulations/wind-turbine.html) | 174.6 kB | Fig. 10 · Wind Turbine Control: the simulation, its data panel, walkthrough and lecture note. | [fig10-wind-turbine.md](simulations/fig10-wind-turbine.md) |

## Walkthroughs

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/scripts/walk/bench.js`](../public/scripts/walk/bench.js) | 9.1 kB | "From symbols to code" for Fig. 6 · Wave Interference Simulator. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/circles.js`](../public/scripts/walk/circles.js) | 6.7 kB | "From symbols to code" for Fig. 1 · Wave Interference. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/dft.js`](../public/scripts/walk/dft.js) | 6.3 kB | "From symbols to code" for Fig. 8 · Draw & Decompose. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/driven.js`](../public/scripts/walk/driven.js) | 7.6 kB | "From symbols to code" for Fig. 9 · Driven Oscillator. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/pendulum.js`](../public/scripts/walk/pendulum.js) | 10.8 kB | "From symbols to code" for Fig. 2 · Double Pendulum. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/phasors.js`](../public/scripts/walk/phasors.js) | 8.1 kB | "From symbols to code" for Fig. 7 · Phasor Sums. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/slit.js`](../public/scripts/walk/slit.js) | 8.1 kB | "From symbols to code" for Fig. 3 · Double-Slit Interference. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/tl.js`](../public/scripts/walk/tl.js) | 7.5 kB | "From symbols to code" for Fig. 4 · Transverse & Longitudinal. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/turbine.js`](../public/scripts/walk/turbine.js) | 8.3 kB | "From symbols to code" for Fig. 10 · Wind Turbine Control. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/water.js`](../public/scripts/walk/water.js) | 7.5 kB | "From symbols to code" for Fig. 5 · Circular Water Waves. | [walk.md](scripts/walk.md) |

## Shared scripts

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/scripts/catalog.js`](../public/scripts/catalog.js) | 14.1 kB | The registry of simulations (SIMULATIONS, SIM_FIELDS, SIM_TOOLS) that the catalog page draws. | [catalog.md](scripts/catalog.md) |
| [`public/scripts/datalog.js`](../public/scripts/datalog.js) | 77.2 kB | The data panel: variables, Read values, Check, Record one round, Save (.npz + CSV). | [datalog.md](scripts/datalog.md) |
| [`public/scripts/dataset.js`](../public/scripts/dataset.js) | 9.1 kB | Sim.dataset(): the one named data store each simulation writes its numbers into. | [dataset.md](scripts/dataset.md) |
| [`public/scripts/fold.js`](../public/scripts/fold.js) | 24.0 kB | Fold-out sections on every page: pinned header bands, remembered state, Expand/Collapse all. | [fold.md](scripts/fold.md) |
| [`public/scripts/sim.js`](../public/scripts/sim.js) | 24.6 kB | Shared helpers of the simulation pages: KaTeX typesetting of the notes, the walkthrough engine. | [sim.md](scripts/sim.md) |

## Stylesheets

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/styles/catalog.css`](../public/styles/catalog.css) | 11.9 kB | The catalog entries (paper abstracts) on the simulations page. | [styles.md](styles.md) |
| [`public/styles/data.css`](../public/styles/data.css) | 31.3 kB | The data panel and the Read values strip. | [styles.md](styles.md) |
| [`public/styles/fold.css`](../public/styles/fold.css) | 10.7 kB | The fold-out sections: cards, header bands, toggles, Expand/Collapse all. | [styles.md](styles.md) |
| [`public/styles/paper.css`](../public/styles/paper.css) | 8.9 kB | Lecture notes set like LaTeX: Latin Modern, numbered equations, figures, abstract box. | [styles.md](styles.md) |
| [`public/styles/portfolio.css`](../public/styles/portfolio.css) | 6.0 kB | The project cards and figure plates of the Portfolios page. | [styles.md](styles.md) |
| [`public/styles/sim.css`](../public/styles/sim.css) | 25.0 kB | Design of the simulation pages: stage, controls, readouts, walkthrough; imports paper.css and KaTeX. | [styles.md](styles.md) |
| [`public/styles/site.css`](../public/styles/site.css) | 17.2 kB | Design of the home, catalog and Portfolios pages: tokens, top bar, sections, cards. | [styles.md](styles.md) |

## KaTeX

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/vendor/katex/LICENSE`](../public/vendor/katex/LICENSE) | 1.1 kB | MIT licence of KaTeX. | [assets.md](assets.md) |
| [`public/vendor/katex/contrib/auto-render.min.js`](../public/vendor/katex/contrib/auto-render.min.js) | 3.5 kB | KaTeX extension that typesets every \( \) and \[ \] in a part of the page. | [assets.md](assets.md) |

<details><summary>20 files: A KaTeX typeface (woff2).</summary>

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/vendor/katex/fonts/KaTeX_AMS-Regular.woff2`](../public/vendor/katex/fonts/KaTeX_AMS-Regular.woff2) | 28.1 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Caligraphic-Bold.woff2`](../public/vendor/katex/fonts/KaTeX_Caligraphic-Bold.woff2) | 6.9 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Caligraphic-Regular.woff2`](../public/vendor/katex/fonts/KaTeX_Caligraphic-Regular.woff2) | 6.9 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Fraktur-Bold.woff2`](../public/vendor/katex/fonts/KaTeX_Fraktur-Bold.woff2) | 11.3 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Fraktur-Regular.woff2`](../public/vendor/katex/fonts/KaTeX_Fraktur-Regular.woff2) | 11.3 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Main-Bold.woff2`](../public/vendor/katex/fonts/KaTeX_Main-Bold.woff2) | 25.3 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Main-BoldItalic.woff2`](../public/vendor/katex/fonts/KaTeX_Main-BoldItalic.woff2) | 16.8 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Main-Italic.woff2`](../public/vendor/katex/fonts/KaTeX_Main-Italic.woff2) | 17.0 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Main-Regular.woff2`](../public/vendor/katex/fonts/KaTeX_Main-Regular.woff2) | 26.3 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Math-BoldItalic.woff2`](../public/vendor/katex/fonts/KaTeX_Math-BoldItalic.woff2) | 16.4 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Math-Italic.woff2`](../public/vendor/katex/fonts/KaTeX_Math-Italic.woff2) | 16.4 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_SansSerif-Bold.woff2`](../public/vendor/katex/fonts/KaTeX_SansSerif-Bold.woff2) | 12.2 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_SansSerif-Italic.woff2`](../public/vendor/katex/fonts/KaTeX_SansSerif-Italic.woff2) | 12.0 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_SansSerif-Regular.woff2`](../public/vendor/katex/fonts/KaTeX_SansSerif-Regular.woff2) | 10.3 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Script-Regular.woff2`](../public/vendor/katex/fonts/KaTeX_Script-Regular.woff2) | 9.6 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Size1-Regular.woff2`](../public/vendor/katex/fonts/KaTeX_Size1-Regular.woff2) | 5.5 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Size2-Regular.woff2`](../public/vendor/katex/fonts/KaTeX_Size2-Regular.woff2) | 5.2 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Size3-Regular.woff2`](../public/vendor/katex/fonts/KaTeX_Size3-Regular.woff2) | 3.6 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Size4-Regular.woff2`](../public/vendor/katex/fonts/KaTeX_Size4-Regular.woff2) | 4.9 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |
| [`public/vendor/katex/fonts/KaTeX_Typewriter-Regular.woff2`](../public/vendor/katex/fonts/KaTeX_Typewriter-Regular.woff2) | 13.6 kB | A KaTeX typeface (woff2). | [assets.md](assets.md) |

</details>

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/vendor/katex/katex.min.css`](../public/vendor/katex/katex.min.css) | 21.3 kB | KaTeX glyph layout and font rules (woff2 only). | [assets.md](assets.md) |
| [`public/vendor/katex/katex.min.js`](../public/vendor/katex/katex.min.js) | 275.4 kB | KaTeX 0.16.11, the maths typesetter. | [assets.md](assets.md) |

## Latin Modern

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/fonts/lm/GUST-FONT-LICENSE.TXT`](../public/fonts/lm/GUST-FONT-LICENSE.TXT) | 1.4 kB | Licence of Latin Modern (GUST Font License 1.0). | [assets.md](assets.md) |
| [`public/fonts/lm/lmroman10-bold.woff2`](../public/fonts/lm/lmroman10-bold.woff2) | 29.6 kB | A face of Latin Modern Roman, the typeface of the lecture notes. | [assets.md](assets.md) |
| [`public/fonts/lm/lmroman10-bolditalic.woff2`](../public/fonts/lm/lmroman10-bolditalic.woff2) | 32.3 kB | A face of Latin Modern Roman, the typeface of the lecture notes. | [assets.md](assets.md) |
| [`public/fonts/lm/lmroman10-italic.woff2`](../public/fonts/lm/lmroman10-italic.woff2) | 32.5 kB | A face of Latin Modern Roman, the typeface of the lecture notes. | [assets.md](assets.md) |
| [`public/fonts/lm/lmroman10-regular.woff2`](../public/fonts/lm/lmroman10-regular.woff2) | 30.4 kB | A face of Latin Modern Roman, the typeface of the lecture notes. | [assets.md](assets.md) |

## Thumbnails

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/images/sims/double-pendulum.webp`](../public/images/sims/double-pendulum.webp) | 12.5 kB | Thumbnail of Fig. 2 · Double Pendulum, 800 × 500 px. | [assets.md](assets.md) |
| [`public/images/sims/double-slit.webp`](../public/images/sims/double-slit.webp) | 33.4 kB | Thumbnail of Fig. 3 · Double-Slit Interference, 800 × 500 px. | [assets.md](assets.md) |
| [`public/images/sims/draw-decompose.webp`](../public/images/sims/draw-decompose.webp) | 16.2 kB | Thumbnail of Fig. 8 · Draw & Decompose, 800 × 500 px. | [assets.md](assets.md) |
| [`public/images/sims/driven-oscillator.webp`](../public/images/sims/driven-oscillator.webp) | 23.7 kB | Thumbnail of Fig. 9 · Driven Oscillator, 800 × 500 px. | [assets.md](assets.md) |
| [`public/images/sims/phasor-sums.webp`](../public/images/sims/phasor-sums.webp) | 12.2 kB | Thumbnail of Fig. 7 · Phasor Sums, 800 × 500 px. | [assets.md](assets.md) |
| [`public/images/sims/transverse-longitudinal.webp`](../public/images/sims/transverse-longitudinal.webp) | 11.8 kB | Thumbnail of Fig. 4 · Transverse & Longitudinal, 800 × 500 px. | [assets.md](assets.md) |
| [`public/images/sims/water-wave.webp`](../public/images/sims/water-wave.webp) | 15.0 kB | Thumbnail of Fig. 5 · Circular Water Waves, 800 × 500 px. | [assets.md](assets.md) |
| [`public/images/sims/wave-bench.webp`](../public/images/sims/wave-bench.webp) | 18.0 kB | Thumbnail of Fig. 6 · Wave Interference Simulator, 800 × 500 px. | [assets.md](assets.md) |
| [`public/images/sims/wave-sources.webp`](../public/images/sims/wave-sources.webp) | 36.5 kB | Thumbnail of Fig. 1 · Wave Interference, 800 × 500 px. | [assets.md](assets.md) |
| [`public/images/sims/wind-turbine.webp`](../public/images/sims/wind-turbine.webp) | 15.4 kB | Thumbnail of Fig. 10 · Wind Turbine Control, 800 × 500 px. | [assets.md](assets.md) |

## Project copy: Droplet Collection

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/portfolios/droplet-collection/fig/c1_ice.svg`](../public/portfolios/droplet-collection/fig/c1_ice.svg) | 86.8 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/ecoll_map.svg`](../public/portfolios/droplet-collection/fig/ecoll_map.svg) | 75.7 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/fallspeed_gk.svg`](../public/portfolios/droplet-collection/fig/fallspeed_gk.svg) | 57.1 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/golovin.svg`](../public/portfolios/droplet-collection/fig/golovin.svg) | 56.2 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/w2_rain.svg`](../public/portfolios/droplet-collection/fig/w2_rain.svg) | 45.0 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/w2_spectra.svg`](../public/portfolios/droplet-collection/fig/w2_spectra.svg) | 74.0 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/index.html`](../public/portfolios/droplet-collection/index.html) | 734 B | Entry page of the project copy: module script and stylesheet loader. | [portfolios.md](portfolios.md) |

<details><summary>59 files: A KaTeX font inside the project build.</summary>

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/portfolios/droplet-collection/static/KaTeX_AMS-Regular-BQhdFMY1.woff2`](../public/portfolios/droplet-collection/static/KaTeX_AMS-Regular-BQhdFMY1.woff2) | 28.1 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_AMS-Regular-DMm9YOAa.woff`](../public/portfolios/droplet-collection/static/KaTeX_AMS-Regular-DMm9YOAa.woff) | 33.5 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_AMS-Regular-DRggAlZN.ttf`](../public/portfolios/droplet-collection/static/KaTeX_AMS-Regular-DRggAlZN.ttf) | 63.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Bold-ATXxdsX0.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Bold-ATXxdsX0.ttf) | 12.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Bold-BEiXGLvX.woff`](../public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Bold-BEiXGLvX.woff) | 7.7 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Bold-Dq_IR9rO.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Bold-Dq_IR9rO.woff2) | 6.9 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Regular-CTRA-rTL.woff`](../public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Regular-CTRA-rTL.woff) | 7.7 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Regular-Di6jR-x-.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Regular-Di6jR-x-.woff2) | 6.9 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Regular-wX97UBjC.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Caligraphic-Regular-wX97UBjC.ttf) | 12.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Fraktur-Bold-BdnERNNW.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Fraktur-Bold-BdnERNNW.ttf) | 19.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Fraktur-Bold-BsDP51OF.woff`](../public/portfolios/droplet-collection/static/KaTeX_Fraktur-Bold-BsDP51OF.woff) | 13.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Fraktur-Bold-CL6g_b3V.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Fraktur-Bold-CL6g_b3V.woff2) | 11.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Fraktur-Regular-CB_wures.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Fraktur-Regular-CB_wures.ttf) | 19.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Fraktur-Regular-CTYiF6lA.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Fraktur-Regular-CTYiF6lA.woff2) | 11.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Fraktur-Regular-Dxdc4cR9.woff`](../public/portfolios/droplet-collection/static/KaTeX_Fraktur-Regular-Dxdc4cR9.woff) | 13.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-Bold-Cx986IdX.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Main-Bold-Cx986IdX.woff2) | 25.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-Bold-Jm3AIy58.woff`](../public/portfolios/droplet-collection/static/KaTeX_Main-Bold-Jm3AIy58.woff) | 29.9 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-Bold-waoOVXN0.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Main-Bold-waoOVXN0.ttf) | 51.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-BoldItalic-DxDJ3AOS.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Main-BoldItalic-DxDJ3AOS.woff2) | 16.8 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-BoldItalic-DzxPMmG6.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Main-BoldItalic-DzxPMmG6.ttf) | 33.0 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-BoldItalic-SpSLRI95.woff`](../public/portfolios/droplet-collection/static/KaTeX_Main-BoldItalic-SpSLRI95.woff) | 19.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-Italic-3WenGoN9.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Main-Italic-3WenGoN9.ttf) | 33.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-Italic-BMLOBm91.woff`](../public/portfolios/droplet-collection/static/KaTeX_Main-Italic-BMLOBm91.woff) | 19.7 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-Italic-NWA7e6Wa.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Main-Italic-NWA7e6Wa.woff2) | 17.0 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-Regular-B22Nviop.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Main-Regular-B22Nviop.woff2) | 26.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-Regular-Dr94JaBh.woff`](../public/portfolios/droplet-collection/static/KaTeX_Main-Regular-Dr94JaBh.woff) | 30.8 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Main-Regular-ypZvNtVU.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Main-Regular-ypZvNtVU.ttf) | 53.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Math-BoldItalic-B3XSjfu4.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Math-BoldItalic-B3XSjfu4.ttf) | 31.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Math-BoldItalic-CZnvNsCZ.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Math-BoldItalic-CZnvNsCZ.woff2) | 16.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Math-BoldItalic-iY-2wyZ7.woff`](../public/portfolios/droplet-collection/static/KaTeX_Math-BoldItalic-iY-2wyZ7.woff) | 18.7 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Math-Italic-DA0__PXp.woff`](../public/portfolios/droplet-collection/static/KaTeX_Math-Italic-DA0__PXp.woff) | 18.7 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Math-Italic-flOr_0UB.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Math-Italic-flOr_0UB.ttf) | 31.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Math-Italic-t53AETM-.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Math-Italic-t53AETM-.woff2) | 16.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_SansSerif-Bold-CFMepnvq.ttf`](../public/portfolios/droplet-collection/static/KaTeX_SansSerif-Bold-CFMepnvq.ttf) | 24.5 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_SansSerif-Bold-D1sUS0GD.woff2`](../public/portfolios/droplet-collection/static/KaTeX_SansSerif-Bold-D1sUS0GD.woff2) | 12.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_SansSerif-Bold-DbIhKOiC.woff`](../public/portfolios/droplet-collection/static/KaTeX_SansSerif-Bold-DbIhKOiC.woff) | 14.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_SansSerif-Italic-C3H0VqGB.woff2`](../public/portfolios/droplet-collection/static/KaTeX_SansSerif-Italic-C3H0VqGB.woff2) | 12.0 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_SansSerif-Italic-DN2j7dab.woff`](../public/portfolios/droplet-collection/static/KaTeX_SansSerif-Italic-DN2j7dab.woff) | 14.1 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_SansSerif-Italic-YYjJ1zSn.ttf`](../public/portfolios/droplet-collection/static/KaTeX_SansSerif-Italic-YYjJ1zSn.ttf) | 22.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_SansSerif-Regular-BNo7hRIc.ttf`](../public/portfolios/droplet-collection/static/KaTeX_SansSerif-Regular-BNo7hRIc.ttf) | 19.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_SansSerif-Regular-CS6fqUqJ.woff`](../public/portfolios/droplet-collection/static/KaTeX_SansSerif-Regular-CS6fqUqJ.woff) | 12.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_SansSerif-Regular-DDBCnlJ7.woff2`](../public/portfolios/droplet-collection/static/KaTeX_SansSerif-Regular-DDBCnlJ7.woff2) | 10.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Script-Regular-C5JkGWo-.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Script-Regular-C5JkGWo-.ttf) | 16.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Script-Regular-D3wIWfF6.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Script-Regular-D3wIWfF6.woff2) | 9.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Script-Regular-D5yQViql.woff`](../public/portfolios/droplet-collection/static/KaTeX_Script-Regular-D5yQViql.woff) | 10.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Size1-Regular-C195tn64.woff`](../public/portfolios/droplet-collection/static/KaTeX_Size1-Regular-C195tn64.woff) | 6.5 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Size1-Regular-Dbsnue_I.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Size1-Regular-Dbsnue_I.ttf) | 12.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Size1-Regular-mCD8mA8B.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Size1-Regular-mCD8mA8B.woff2) | 5.5 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Size2-Regular-B7gKUWhC.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Size2-Regular-B7gKUWhC.ttf) | 11.5 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Size2-Regular-Dy4dx90m.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Size2-Regular-Dy4dx90m.woff2) | 5.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Size2-Regular-oD1tc_U0.woff`](../public/portfolios/droplet-collection/static/KaTeX_Size2-Regular-oD1tc_U0.woff) | 6.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Size3-Regular-CTq5MqoE.woff`](../public/portfolios/droplet-collection/static/KaTeX_Size3-Regular-CTq5MqoE.woff) | 4.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Size3-Regular-DgpXs0kz.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Size3-Regular-DgpXs0kz.ttf) | 7.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Size4-Regular-BF-4gkZK.woff`](../public/portfolios/droplet-collection/static/KaTeX_Size4-Regular-BF-4gkZK.woff) | 6.0 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Size4-Regular-DWFBv043.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Size4-Regular-DWFBv043.ttf) | 10.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Size4-Regular-Dl5lxZxV.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Size4-Regular-Dl5lxZxV.woff2) | 4.9 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Typewriter-Regular-C0xS9mPB.woff`](../public/portfolios/droplet-collection/static/KaTeX_Typewriter-Regular-C0xS9mPB.woff) | 16.0 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Typewriter-Regular-CO6r4hn1.woff2`](../public/portfolios/droplet-collection/static/KaTeX_Typewriter-Regular-CO6r4hn1.woff2) | 13.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/KaTeX_Typewriter-Regular-D3Ib7_Hf.ttf`](../public/portfolios/droplet-collection/static/KaTeX_Typewriter-Regular-D3Ib7_Hf.ttf) | 27.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |

</details>

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/portfolios/droplet-collection/static/index-CGriahzx.css`](../public/portfolios/droplet-collection/static/index-CGriahzx.css) | 60.7 kB | The project's stylesheet, built. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/index-DOoZ3Yi-.js`](../public/portfolios/droplet-collection/static/index-DOoZ3Yi-.js) | 837.0 kB | The whole project application, built and minified. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/static/worker-ClooJ8Gk.js`](../public/portfolios/droplet-collection/static/worker-ClooJ8Gk.js) | 130.6 kB | The project's Web Worker: its solver, off the main thread. | [portfolios.md](portfolios.md) |

## Project copy: Rotor Pendula

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/portfolios/rotor-pendula/fig/01_geometry.svg`](../public/portfolios/rotor-pendula/fig/01_geometry.svg) | 7.6 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/fig/02_mapping_power.svg`](../public/portfolios/rotor-pendula/fig/02_mapping_power.svg) | 33.7 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/fig/03_topology.svg`](../public/portfolios/rotor-pendula/fig/03_topology.svg) | 39.7 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/fig/04_geometry_ratios.svg`](../public/portfolios/rotor-pendula/fig/04_geometry_ratios.svg) | 16.9 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/fig/05_chaos.svg`](../public/portfolios/rotor-pendula/fig/05_chaos.svg) | 35.5 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/fig/06_sections.svg`](../public/portfolios/rotor-pendula/fig/06_sections.svg) | 133.8 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/fig/07_sensor_range.svg`](../public/portfolios/rotor-pendula/fig/07_sensor_range.svg) | 23.0 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/index.html`](../public/portfolios/rotor-pendula/index.html) | 737 B | Entry page of the project copy: module script and stylesheet loader. | [portfolios.md](portfolios.md) |

<details><summary>59 files: A KaTeX font inside the project build.</summary>

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/portfolios/rotor-pendula/static/KaTeX_AMS-Regular-BQhdFMY1.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_AMS-Regular-BQhdFMY1.woff2) | 28.1 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_AMS-Regular-DMm9YOAa.woff`](../public/portfolios/rotor-pendula/static/KaTeX_AMS-Regular-DMm9YOAa.woff) | 33.5 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_AMS-Regular-DRggAlZN.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_AMS-Regular-DRggAlZN.ttf) | 63.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Bold-ATXxdsX0.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Bold-ATXxdsX0.ttf) | 12.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Bold-BEiXGLvX.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Bold-BEiXGLvX.woff) | 7.7 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Bold-Dq_IR9rO.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Bold-Dq_IR9rO.woff2) | 6.9 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Regular-CTRA-rTL.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Regular-CTRA-rTL.woff) | 7.7 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Regular-Di6jR-x-.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Regular-Di6jR-x-.woff2) | 6.9 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Regular-wX97UBjC.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Caligraphic-Regular-wX97UBjC.ttf) | 12.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Bold-BdnERNNW.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Bold-BdnERNNW.ttf) | 19.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Bold-BsDP51OF.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Bold-BsDP51OF.woff) | 13.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Bold-CL6g_b3V.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Bold-CL6g_b3V.woff2) | 11.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Regular-CB_wures.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Regular-CB_wures.ttf) | 19.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Regular-CTYiF6lA.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Regular-CTYiF6lA.woff2) | 11.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Regular-Dxdc4cR9.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Fraktur-Regular-Dxdc4cR9.woff) | 13.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-Bold-Cx986IdX.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Main-Bold-Cx986IdX.woff2) | 25.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-Bold-Jm3AIy58.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Main-Bold-Jm3AIy58.woff) | 29.9 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-Bold-waoOVXN0.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Main-Bold-waoOVXN0.ttf) | 51.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-BoldItalic-DxDJ3AOS.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Main-BoldItalic-DxDJ3AOS.woff2) | 16.8 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-BoldItalic-DzxPMmG6.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Main-BoldItalic-DzxPMmG6.ttf) | 33.0 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-BoldItalic-SpSLRI95.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Main-BoldItalic-SpSLRI95.woff) | 19.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-Italic-3WenGoN9.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Main-Italic-3WenGoN9.ttf) | 33.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-Italic-BMLOBm91.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Main-Italic-BMLOBm91.woff) | 19.7 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-Italic-NWA7e6Wa.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Main-Italic-NWA7e6Wa.woff2) | 17.0 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-Regular-B22Nviop.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Main-Regular-B22Nviop.woff2) | 26.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-Regular-Dr94JaBh.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Main-Regular-Dr94JaBh.woff) | 30.8 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Main-Regular-ypZvNtVU.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Main-Regular-ypZvNtVU.ttf) | 53.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Math-BoldItalic-B3XSjfu4.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Math-BoldItalic-B3XSjfu4.ttf) | 31.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Math-BoldItalic-CZnvNsCZ.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Math-BoldItalic-CZnvNsCZ.woff2) | 16.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Math-BoldItalic-iY-2wyZ7.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Math-BoldItalic-iY-2wyZ7.woff) | 18.7 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Math-Italic-DA0__PXp.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Math-Italic-DA0__PXp.woff) | 18.7 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Math-Italic-flOr_0UB.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Math-Italic-flOr_0UB.ttf) | 31.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Math-Italic-t53AETM-.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Math-Italic-t53AETM-.woff2) | 16.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Bold-CFMepnvq.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Bold-CFMepnvq.ttf) | 24.5 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Bold-D1sUS0GD.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Bold-D1sUS0GD.woff2) | 12.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Bold-DbIhKOiC.woff`](../public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Bold-DbIhKOiC.woff) | 14.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Italic-C3H0VqGB.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Italic-C3H0VqGB.woff2) | 12.0 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Italic-DN2j7dab.woff`](../public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Italic-DN2j7dab.woff) | 14.1 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Italic-YYjJ1zSn.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Italic-YYjJ1zSn.ttf) | 22.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Regular-BNo7hRIc.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Regular-BNo7hRIc.ttf) | 19.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Regular-CS6fqUqJ.woff`](../public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Regular-CS6fqUqJ.woff) | 12.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Regular-DDBCnlJ7.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_SansSerif-Regular-DDBCnlJ7.woff2) | 10.3 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Script-Regular-C5JkGWo-.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Script-Regular-C5JkGWo-.ttf) | 16.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Script-Regular-D3wIWfF6.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Script-Regular-D3wIWfF6.woff2) | 9.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Script-Regular-D5yQViql.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Script-Regular-D5yQViql.woff) | 10.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Size1-Regular-C195tn64.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Size1-Regular-C195tn64.woff) | 6.5 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Size1-Regular-Dbsnue_I.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Size1-Regular-Dbsnue_I.ttf) | 12.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Size1-Regular-mCD8mA8B.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Size1-Regular-mCD8mA8B.woff2) | 5.5 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Size2-Regular-B7gKUWhC.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Size2-Regular-B7gKUWhC.ttf) | 11.5 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Size2-Regular-Dy4dx90m.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Size2-Regular-Dy4dx90m.woff2) | 5.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Size2-Regular-oD1tc_U0.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Size2-Regular-oD1tc_U0.woff) | 6.2 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Size3-Regular-CTq5MqoE.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Size3-Regular-CTq5MqoE.woff) | 4.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Size3-Regular-DgpXs0kz.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Size3-Regular-DgpXs0kz.ttf) | 7.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Size4-Regular-BF-4gkZK.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Size4-Regular-BF-4gkZK.woff) | 6.0 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Size4-Regular-DWFBv043.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Size4-Regular-DWFBv043.ttf) | 10.4 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Size4-Regular-Dl5lxZxV.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Size4-Regular-Dl5lxZxV.woff2) | 4.9 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Typewriter-Regular-C0xS9mPB.woff`](../public/portfolios/rotor-pendula/static/KaTeX_Typewriter-Regular-C0xS9mPB.woff) | 16.0 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Typewriter-Regular-CO6r4hn1.woff2`](../public/portfolios/rotor-pendula/static/KaTeX_Typewriter-Regular-CO6r4hn1.woff2) | 13.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/KaTeX_Typewriter-Regular-D3Ib7_Hf.ttf`](../public/portfolios/rotor-pendula/static/KaTeX_Typewriter-Regular-D3Ib7_Hf.ttf) | 27.6 kB | A KaTeX font inside the project build. | [portfolios.md](portfolios.md) |

</details>

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/portfolios/rotor-pendula/static/index-CNYGhWdg.css`](../public/portfolios/rotor-pendula/static/index-CNYGhWdg.css) | 65.5 kB | The project's stylesheet, built. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/index-CRh2Uwlk.js`](../public/portfolios/rotor-pendula/static/index-CRh2Uwlk.js) | 999.5 kB | The whole project application, built and minified. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/worker-hcWKavQc.js`](../public/portfolios/rotor-pendula/static/worker-hcWKavQc.js) | 4.5 kB | The project's Web Worker: its solver, off the main thread. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/CHANGES.md`](../public/portfolios/rotor-pendula/study/CHANGES.md) | 3.1 kB | The corrections C1–C14, old → new. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/FILE_INVENTORY.csv`](../public/portfolios/rotor-pendula/study/FILE_INVENTORY.csv) | 6.6 kB | Every file of the full delivery with its size. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/README.md`](../public/portfolios/rotor-pendula/study/README.md) | 412 B | Where to start reading the study. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/STATUS.md`](../public/portfolios/rotor-pendula/study/STATUS.md) | 1.8 kB | What the study computed, derived, did not measure, and assumes. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/code/README.md`](../public/portfolios/rotor-pendula/study/code/README.md) | 4.3 kB | How to regenerate the study, command by command. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/code/requirements.txt`](../public/portfolios/rotor-pendula/study/code/requirements.txt) | 64 B | The pinned Python packages. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/data/all_results.json`](../public/portfolios/rotor-pendula/study/data/all_results.json) | 318.1 kB | All 160 cases with full parameters. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/data/audit.json`](../public/portfolios/rotor-pendula/study/data/audit.json) | 5.4 kB | Audit numbers: RK4 cross-checks, energy identity, sensor budget. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/data/summary.csv`](../public/portfolios/rotor-pendula/study/data/summary.csv) | 64.3 kB | One row per computed case. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/report.pdf`](../public/portfolios/rotor-pendula/study/report.pdf) | 202.1 kB | Sol's 14-page corrected report. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/report.tex`](../public/portfolios/rotor-pendula/study/report.tex) | 35.7 kB | LaTeX source of the report. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/sources/README.md`](../public/portfolios/rotor-pendula/study/sources/README.md) | 2.9 kB | The two datasheets behind the sensor budget, with checksums. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/sources/access.json`](../public/portfolios/rotor-pendula/study/sources/access.json) | 484 B | The same two sources as data. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/study/wind_pendulum.zip`](../public/portfolios/rotor-pendula/study/wind_pendulum.zip) | 1.40 MB | The complete delivery: code, data, figures, fonts, sources. | [portfolios.md](portfolios.md) |

## Template sources

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`src/main.ts`](../src/main.ts) | 23 B | Template script entry; index.html does not load it. | [build-and-deploy.md](build-and-deploy.md) |
| [`src/styles.css`](../src/styles.css) | 73 B | Template Tailwind directives; unused. | [build-and-deploy.md](build-and-deploy.md) |

## Platform tests

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`tests/tests.json`](../tests/tests.json) | 15.3 kB | Plain-language test scenarios run by the platform's QA after each deploy. | [build-and-deploy.md](build-and-deploy.md) |

## Documentation

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`docs/architecture.md`](architecture.md) | 7.2 kB | Documentation: How the site fits together. | [architecture.md](architecture.md) |
| [`docs/assets.md`](assets.md) | 6.1 kB | Documentation: Fonts, maths and pictures: `public/vendor/`, `public/fonts/`, `public/images/`. | [assets.md](assets.md) |
| [`docs/build-and-deploy.md`](build-and-deploy.md) | 8.9 kB | Documentation: Build files, tests and deployment. | [build-and-deploy.md](build-and-deploy.md) |
| [`docs/files.md`](files.md) | this file | This list. Written by tools/inventory.py; do not edit by hand. | [files.md](files.md) |
| [`docs/minor-issues-report.md`](minor-issues-report.md) | 3.3 kB | Documentation: Minor issues · verification report. | [minor-issues-report.md](minor-issues-report.md) |
| [`docs/pages.md`](pages.md) | 42.7 kB | Documentation: The site's own pages: home, simulations catalog, Portfolios, robots.txt. | [pages.md](pages.md) |
| [`docs/portfolios.md`](portfolios.md) | 10.5 kB | Documentation: The two research projects: `public/portfolios/`. | [portfolios.md](portfolios.md) |
| [`docs/scripts/catalog.md`](scripts/catalog.md) | 15.2 kB | Documentation: public/scripts/catalog.js. | [catalog.md](scripts/catalog.md) |
| [`docs/scripts/datalog.md`](scripts/datalog.md) | 44.6 kB | Documentation: public/scripts/datalog.js. | [datalog.md](scripts/datalog.md) |
| [`docs/scripts/dataset.md`](scripts/dataset.md) | 17.7 kB | Documentation: public/scripts/dataset.js. | [dataset.md](scripts/dataset.md) |
| [`docs/scripts/fold.md`](scripts/fold.md) | 21.8 kB | Documentation: public/scripts/fold.js. | [fold.md](scripts/fold.md) |
| [`docs/scripts/sim.md`](scripts/sim.md) | 25.8 kB | Documentation: public/scripts/sim.js. | [sim.md](scripts/sim.md) |
| [`docs/scripts/walk.md`](scripts/walk.md) | 19.4 kB | Documentation: public/scripts/walk/*.js. | [walk.md](scripts/walk.md) |
| [`docs/simulations/fig01-wave-sources.md`](simulations/fig01-wave-sources.md) | 47.9 kB | Documentation: Fig. 1 · Wave Interference. | [fig01-wave-sources.md](simulations/fig01-wave-sources.md) |
| [`docs/simulations/fig02-double-pendulum.md`](simulations/fig02-double-pendulum.md) | 43.9 kB | Documentation: Fig. 2 · Double Pendulum. | [fig02-double-pendulum.md](simulations/fig02-double-pendulum.md) |
| [`docs/simulations/fig03-double-slit.md`](simulations/fig03-double-slit.md) | 36.4 kB | Documentation: Fig. 3 · Double-Slit Interference. | [fig03-double-slit.md](simulations/fig03-double-slit.md) |
| [`docs/simulations/fig04-transverse-longitudinal.md`](simulations/fig04-transverse-longitudinal.md) | 33.5 kB | Documentation: Fig. 4 · Transverse and Longitudinal Waves. | [fig04-transverse-longitudinal.md](simulations/fig04-transverse-longitudinal.md) |
| [`docs/simulations/fig05-water-wave.md`](simulations/fig05-water-wave.md) | 32.9 kB | Documentation: Fig. 5 · Circular Water Waves. | [fig05-water-wave.md](simulations/fig05-water-wave.md) |
| [`docs/simulations/fig06-wave-bench.md`](simulations/fig06-wave-bench.md) | 38.4 kB | Documentation: Fig. 6 · Wave Interference Simulator. | [fig06-wave-bench.md](simulations/fig06-wave-bench.md) |
| [`docs/simulations/fig07-phasor-sums.md`](simulations/fig07-phasor-sums.md) | 36.7 kB | Documentation: Fig. 7 · Phasor Sums. | [fig07-phasor-sums.md](simulations/fig07-phasor-sums.md) |
| [`docs/simulations/fig08-draw-decompose.md`](simulations/fig08-draw-decompose.md) | 32.9 kB | Documentation: Fig. 8 · Draw & Decompose. | [fig08-draw-decompose.md](simulations/fig08-draw-decompose.md) |
| [`docs/simulations/fig09-driven-oscillator.md`](simulations/fig09-driven-oscillator.md) | 37.8 kB | Documentation: Fig. 9 · Driven Oscillator. | [fig09-driven-oscillator.md](simulations/fig09-driven-oscillator.md) |
| [`docs/simulations/fig10-wind-turbine.md`](simulations/fig10-wind-turbine.md) | 41.9 kB | Documentation: Fig. 10 · Wind Turbine Control. | [fig10-wind-turbine.md](simulations/fig10-wind-turbine.md) |
| [`docs/styles.md`](styles.md) | 40.4 kB | Documentation: Stylesheets: `public/styles/`. | [styles.md](styles.md) |

## Tools

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`tools/inventory.py`](../tools/inventory.py) | 16.1 kB | Writes docs/files.md and checks that every file in the repository is described. | [files.md](files.md) |
