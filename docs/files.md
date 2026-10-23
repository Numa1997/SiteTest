# Every file

Written by [`tools/inventory.py`](../tools/inventory.py) from the files in the repository; do not edit by hand.
Run `python3 tools/inventory.py` after adding, removing or changing files, and `python3 tools/inventory.py --check`
to confirm that every file is described. Sizes are those of the files when the list was written.

736 files, 27.3 MB in all. Runs of more than 12 similar files are folded; open them to see each file.

| Folder | Files |
|---|---|
| [Repository root](#repository-root) | 11 |
| [Pages under public/](#pages-under-public) | 4 |
| [German pages (generated)](#german-pages-generated) | 3 |
| [Arabic pages (generated)](#arabic-pages-generated) | 3 |
| [Simulation pages](#simulation-pages) | 10 |
| [Walkthroughs](#walkthroughs) | 10 |
| [Shared scripts](#shared-scripts) | 7 |
| [Stylesheets](#stylesheets) | 15 |
| [KaTeX](#katex) | 24 |
| [Latin Modern](#latin-modern) | 5 |
| [IBM Plex, Instrument Serif, and the Arabic faces](#ibm-plex-instrument-serif-and-the-arabic-faces) | 61 |
| [Thumbnails](#thumbnails) | 10 |
| [Logo](#logo) | 1 |
| [Project copy: Droplet Collection](#project-copy-droplet-collection) | 11 |
| [Project copy: Rotor Pendula](#project-copy-rotor-pendula) | 84 |
| [Project copy: Hydraulic Press Study](#project-copy-hydraulic-press-study) | 6 |
| [Iron, Cotton and the Head](#iron-cotton-and-the-head) | 6 |
| [Source of the Hydraulic Press Study (not served)](#source-of-the-hydraulic-press-study-not-served) | 37 |
| [Source of Iron, Cotton and the Head (not served)](#source-of-iron-cotton-and-the-head-not-served) | 18 |
| [Source of the Rotor Pendula notes (not served)](#source-of-the-rotor-pendula-notes-not-served) | 20 |
| [Source of the Droplet Collection study (not served)](#source-of-the-droplet-collection-study-not-served) | 65 |
| [Template sources](#template-sources) | 2 |
| [Platform tests](#platform-tests) | 1 |
| [Documentation](#documentation) | 30 |
| [Tools](#tools) | 4 |
| [Translation tables](#translation-tables) | 8 |
| [Agents of the lecture-note review](#agents-of-the-lecture-note-review) | 4 |
| [Working notes of the Rotor Pendula study](#working-notes-of-the-rotor-pendula-study) | 47 |
| [Working notes of the Droplet Collection study](#working-notes-of-the-droplet-collection-study) | 113 |
| [Record of the lecture-note review](#record-of-the-lecture-note-review) | 116 |

## Repository root

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`.gitignore`](../.gitignore) | 39 B | Files git leaves out: Python caches, node_modules, build output. | [files.md](files.md) |
| [`AGENTS.md`](../AGENTS.md) | 12.8 kB | The maintainer's summary: ownership, layout, design rules, folds, the data pipeline, platform quirks. | [build-and-deploy.md](build-and-deploy.md) |
| [`CLAUDE.md`](../CLAUDE.md) | 4.3 kB | How Numa expects an AI assistant to work on the project. | [build-and-deploy.md](build-and-deploy.md) |
| [`README.md`](../README.md) | 7.7 kB | Start here: what the project is, how the files fit together, where each one is explained. | [README.md](../README.md) |
| [`index.html`](../index.html) | 48.2 kB | The home page: CV, research, simulation plates, index; also the build entry page. | [pages.md](pages.md) |
| [`package.json`](../package.json) | 479 B | Build declaration: vite build; template dependencies. | [build-and-deploy.md](build-and-deploy.md) |
| [`postcss.config.js`](../postcss.config.js) | 81 B | PostCSS settings (template; unused by the site). | [build-and-deploy.md](build-and-deploy.md) |
| [`tailwind.config.js`](../tailwind.config.js) | 155 B | Tailwind settings (template; unused by the site). | [build-and-deploy.md](build-and-deploy.md) |
| [`tsconfig.json`](../tsconfig.json) | 485 B | TypeScript settings for src/ (template; unused by the site). | [build-and-deploy.md](build-and-deploy.md) |
| [`vite.config.ts`](../vite.config.ts) | 310 B | Vite settings: relative base, output folder from the platform. | [build-and-deploy.md](build-and-deploy.md) |
| [`wrangler.jsonc`](../wrangler.jsonc) | 486 B | Cloudflare settings: the Worker phyein-usul, the dist/ folder, the custom domains phyeinusul.com and www. | [usul.md](usul.md) |

## Pages under public/

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/_headers`](../public/_headers) | 516 B | Security response headers Cloudflare sets on every file of phyeinusul.com; read by Cloudflare, never served. | [usul.md](usul.md) |
| [`public/portfolios.html`](../public/portfolios.html) | 40.6 kB | The Portfolios page: the two research projects. | [pages.md](pages.md) |
| [`public/robots.txt`](../public/robots.txt) | 58 B | Instructions for search-engine crawlers. | [pages.md](pages.md) |
| [`public/simulations.html`](../public/simulations.html) | 20.7 kB | The simulations catalog: one titled fold card per simulation, search and chips. | [pages.md](pages.md) |

## German pages (generated)

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/de/index.html`](../public/de/index.html) | 47.3 kB | German index.html, generated by tools/i18n/build.py; do not edit. | [i18n.md](i18n.md) |
| [`public/de/portfolios.html`](../public/de/portfolios.html) | 43.2 kB | German portfolios.html, generated by tools/i18n/build.py; do not edit. | [i18n.md](i18n.md) |
| [`public/de/simulations.html`](../public/de/simulations.html) | 20.8 kB | German simulations.html, generated by tools/i18n/build.py; do not edit. | [i18n.md](i18n.md) |

## Arabic pages (generated)

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/ar/index.html`](../public/ar/index.html) | 49.7 kB | Arabic index.html, generated by tools/i18n/build.py; do not edit. | [i18n.md](i18n.md) |
| [`public/ar/portfolios.html`](../public/ar/portfolios.html) | 51.5 kB | Arabic portfolios.html, generated by tools/i18n/build.py; do not edit. | [i18n.md](i18n.md) |
| [`public/ar/simulations.html`](../public/ar/simulations.html) | 21.7 kB | Arabic simulations.html, generated by tools/i18n/build.py; do not edit. | [i18n.md](i18n.md) |

## Simulation pages

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/simulations/Circular Wave Interference Visualization.html`](../public/simulations/Circular%20Wave%20Interference%20Visualization.html) | 193.2 kB | Fig. 1 · Wave Interference: the simulation, its data panel, walkthrough and lecture note. | [fig01-wave-sources.md](simulations/fig01-wave-sources.md) |
| [`public/simulations/Double Pendulum.html`](../public/simulations/Double%20Pendulum.html) | 128.9 kB | Fig. 2 · Double Pendulum: the simulation, its data panel, walkthrough and lecture note. | [fig02-double-pendulum.md](simulations/fig02-double-pendulum.md) |
| [`public/simulations/Interactive Double-Slit Experiment Visualization.html`](../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html) | 173.9 kB | Fig. 3 · Double-Slit Interference: the simulation, its data panel, walkthrough and lecture note. | [fig03-double-slit.md](simulations/fig03-double-slit.md) |
| [`public/simulations/Transverse and longitudinal waves.html`](../public/simulations/Transverse%20and%20longitudinal%20waves.html) | 202.1 kB | Fig. 4 · Transverse & Longitudinal: the simulation, its data panel, walkthrough and lecture note. | [fig04-transverse-longitudinal.md](simulations/fig04-transverse-longitudinal.md) |
| [`public/simulations/draw-decompose.html`](../public/simulations/draw-decompose.html) | 216.3 kB | Fig. 8 · Draw & Decompose: the simulation, its data panel, walkthrough and lecture note. | [fig08-draw-decompose.md](simulations/fig08-draw-decompose.md) |
| [`public/simulations/driven-oscillator.html`](../public/simulations/driven-oscillator.html) | 183.3 kB | Fig. 9 · Driven Oscillator: the simulation, its data panel, walkthrough and lecture note. | [fig09-driven-oscillator.md](simulations/fig09-driven-oscillator.md) |
| [`public/simulations/phasor-sums.html`](../public/simulations/phasor-sums.html) | 262.8 kB | Fig. 7 · Phasor Sums: the simulation, its data panel, walkthrough and lecture note. | [fig07-phasor-sums.md](simulations/fig07-phasor-sums.md) |
| [`public/simulations/water-wave.html`](../public/simulations/water-wave.html) | 163.6 kB | Fig. 5 · Circular Water Waves: the simulation, its data panel, walkthrough and lecture note. | [fig05-water-wave.md](simulations/fig05-water-wave.md) |
| [`public/simulations/wave-interference.html`](../public/simulations/wave-interference.html) | 170.5 kB | Fig. 6 · Wave Interference Simulator: the simulation, its data panel, walkthrough and lecture note. | [fig06-wave-bench.md](simulations/fig06-wave-bench.md) |
| [`public/simulations/wind-turbine.html`](../public/simulations/wind-turbine.html) | 184.7 kB | Fig. 10 · Wind Turbine Control: the simulation, its data panel, walkthrough and lecture note. | [fig10-wind-turbine.md](simulations/fig10-wind-turbine.md) |

## Walkthroughs

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/scripts/walk/bench.js`](../public/scripts/walk/bench.js) | 31.9 kB | "From symbols to code" for Fig. 6 · Wave Interference Simulator. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/circles.js`](../public/scripts/walk/circles.js) | 18.6 kB | "From symbols to code" for Fig. 1 · Wave Interference. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/dft.js`](../public/scripts/walk/dft.js) | 24.4 kB | "From symbols to code" for Fig. 8 · Draw & Decompose. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/driven.js`](../public/scripts/walk/driven.js) | 33.0 kB | "From symbols to code" for Fig. 9 · Driven Oscillator. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/pendulum.js`](../public/scripts/walk/pendulum.js) | 30.2 kB | "From symbols to code" for Fig. 2 · Double Pendulum. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/phasors.js`](../public/scripts/walk/phasors.js) | 33.0 kB | "From symbols to code" for Fig. 7 · Phasor Sums. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/slit.js`](../public/scripts/walk/slit.js) | 23.6 kB | "From symbols to code" for Fig. 3 · Double-Slit Interference. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/tl.js`](../public/scripts/walk/tl.js) | 23.6 kB | "From symbols to code" for Fig. 4 · Transverse & Longitudinal. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/turbine.js`](../public/scripts/walk/turbine.js) | 34.4 kB | "From symbols to code" for Fig. 10 · Wind Turbine Control. | [walk.md](scripts/walk.md) |
| [`public/scripts/walk/water.js`](../public/scripts/walk/water.js) | 22.6 kB | "From symbols to code" for Fig. 5 · Circular Water Waves. | [walk.md](scripts/walk.md) |

## Shared scripts

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/scripts/catalog.js`](../public/scripts/catalog.js) | 14.2 kB | The registry of simulations (SIMULATIONS, SIM_FIELDS, SIM_TOOLS) that the catalog page draws. | [catalog.md](scripts/catalog.md) |
| [`public/scripts/datalog.js`](../public/scripts/datalog.js) | 77.7 kB | The data panel: variables, Read values, Check, Record one round, Save (.npz + CSV). | [datalog.md](scripts/datalog.md) |
| [`public/scripts/dataset.js`](../public/scripts/dataset.js) | 8.6 kB | Sim.dataset(): the one named data store each simulation writes its numbers into. | [dataset.md](scripts/dataset.md) |
| [`public/scripts/fold.js`](../public/scripts/fold.js) | 24.5 kB | Fold-out sections on every page: pinned header bands, remembered state, Expand/Collapse all. | [fold.md](scripts/fold.md) |
| [`public/scripts/i18n/strings-ar.js`](../public/scripts/i18n/strings-ar.js) | 19.7 kB | The Arabic string table the scripts read through T(), generated; do not edit. | [i18n.md](i18n.md) |
| [`public/scripts/i18n/strings-de.js`](../public/scripts/i18n/strings-de.js) | 15.5 kB | The German string table the scripts read through T(), generated; do not edit. | [i18n.md](i18n.md) |
| [`public/scripts/sim.js`](../public/scripts/sim.js) | 27.2 kB | Shared helpers of the simulation pages: KaTeX typesetting of the notes, the walkthrough engine. | [sim.md](scripts/sim.md) |

## Stylesheets

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/styles/catalog.css`](../public/styles/catalog.css) | 11.5 kB | The catalog entries (paper abstracts) on the simulations page. | [styles.md](styles.md) |
| [`public/styles/catalog.rtl.css`](../public/styles/catalog.rtl.css) | 11.7 kB | catalog.css with left and right exchanged, for the Arabic pages; generated with rtlcss, do not edit. | [styles.md](styles.md) |
| [`public/styles/data.css`](../public/styles/data.css) | 31.1 kB | The data panel and the Read values strip. | [styles.md](styles.md) |
| [`public/styles/data.rtl.css`](../public/styles/data.rtl.css) | 31.3 kB | data.css with left and right exchanged, for the Arabic pages; generated with rtlcss, do not edit. | [styles.md](styles.md) |
| [`public/styles/fold.css`](../public/styles/fold.css) | 10.6 kB | The fold-out sections: cards, header bands, toggles, Expand/Collapse all. | [styles.md](styles.md) |
| [`public/styles/fold.rtl.css`](../public/styles/fold.rtl.css) | 10.8 kB | fold.css with left and right exchanged, for the Arabic pages; generated with rtlcss, do not edit. | [styles.md](styles.md) |
| [`public/styles/i18n.css`](../public/styles/i18n.css) | 3.8 kB | Language switch, Arabic fonts and the few right-to-left rules of the translated pages. | [styles.md](styles.md) |
| [`public/styles/paper.css`](../public/styles/paper.css) | 8.8 kB | Lecture notes set like LaTeX: Latin Modern, numbered equations, figures, abstract box. | [styles.md](styles.md) |
| [`public/styles/paper.rtl.css`](../public/styles/paper.rtl.css) | 9.0 kB | paper.css with left and right exchanged, for the Arabic pages; generated with rtlcss, do not edit. | [styles.md](styles.md) |
| [`public/styles/portfolio.css`](../public/styles/portfolio.css) | 6.1 kB | The project cards and figure plates of the Portfolios page. | [styles.md](styles.md) |
| [`public/styles/portfolio.rtl.css`](../public/styles/portfolio.rtl.css) | 6.3 kB | portfolio.css with left and right exchanged, for the Arabic pages; generated with rtlcss, do not edit. | [styles.md](styles.md) |
| [`public/styles/sim.css`](../public/styles/sim.css) | 18.4 kB | Design of the simulation pages: stage, controls, readouts, walkthrough; imports paper.css and KaTeX. | [styles.md](styles.md) |
| [`public/styles/sim.rtl.css`](../public/styles/sim.rtl.css) | 18.5 kB | sim.css with left and right exchanged, for the Arabic pages; generated with rtlcss, do not edit. | [styles.md](styles.md) |
| [`public/styles/site.css`](../public/styles/site.css) | 17.0 kB | Design of the home, catalog and Portfolios pages: tokens, top bar, sections, cards. | [styles.md](styles.md) |
| [`public/styles/site.rtl.css`](../public/styles/site.rtl.css) | 17.2 kB | site.css with left and right exchanged, for the Arabic pages; generated with rtlcss, do not edit. | [styles.md](styles.md) |

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

## IBM Plex, Instrument Serif, and the Arabic faces

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/fonts/OFL-Amiri.txt`](../public/fonts/OFL-Amiri.txt) | 4.4 kB | Licence of Amiri (SIL Open Font License 1.1). | [assets.md](assets.md) |
| [`public/fonts/OFL-IBM-Plex.txt`](../public/fonts/OFL-IBM-Plex.txt) | 4.5 kB | Licence of IBM Plex (SIL Open Font License 1.1). | [assets.md](assets.md) |
| [`public/fonts/OFL-Instrument-Serif.txt`](../public/fonts/OFL-Instrument-Serif.txt) | 4.4 kB | Licence of Instrument Serif (SIL Open Font License 1.1). | [assets.md](assets.md) |
| [`public/fonts/OFL-Noto-Naskh-Arabic.txt`](../public/fonts/OFL-Noto-Naskh-Arabic.txt) | 4.4 kB | Licence of Noto Naskh Arabic (SIL Open Font License 1.1). | [assets.md](assets.md) |
| [`public/fonts/amiri/amiri-400-arabic.woff2`](../public/fonts/amiri/amiri-400-arabic.woff2) | 107.5 kB | Amiri 400, cut to the Arabic blocks. | [assets.md](assets.md) |
| [`public/fonts/amiri/amiri-700-arabic.woff2`](../public/fonts/amiri/amiri-700-arabic.woff2) | 108.4 kB | Amiri 700, cut to the Arabic blocks. | [assets.md](assets.md) |
| [`public/fonts/arabic.css`](../public/fonts/arabic.css) | 1.4 kB | Amiri and Noto Naskh Arabic, served by the site itself: the @font-face rules of the Arabic pages. | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-mono/ibm-plex-mono-400-cyrillic-ext.woff2`](../public/fonts/ibm-plex-mono/ibm-plex-mono-400-cyrillic-ext.woff2) | 6.9 kB | A face of IBM Plex Mono for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-mono/ibm-plex-mono-400-cyrillic.woff2`](../public/fonts/ibm-plex-mono/ibm-plex-mono-400-cyrillic.woff2) | 8.4 kB | A face of IBM Plex Mono for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-mono/ibm-plex-mono-400-latin-ext.woff2`](../public/fonts/ibm-plex-mono/ibm-plex-mono-400-latin-ext.woff2) | 13.3 kB | A face of IBM Plex Mono for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-mono/ibm-plex-mono-400-latin.woff2`](../public/fonts/ibm-plex-mono/ibm-plex-mono-400-latin.woff2) | 14.7 kB | A face of IBM Plex Mono for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-mono/ibm-plex-mono-400-vietnamese.woff2`](../public/fonts/ibm-plex-mono/ibm-plex-mono-400-vietnamese.woff2) | 5.9 kB | A face of IBM Plex Mono for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-mono/ibm-plex-mono-500-cyrillic-ext.woff2`](../public/fonts/ibm-plex-mono/ibm-plex-mono-500-cyrillic-ext.woff2) | 7.0 kB | A face of IBM Plex Mono for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-mono/ibm-plex-mono-500-cyrillic.woff2`](../public/fonts/ibm-plex-mono/ibm-plex-mono-500-cyrillic.woff2) | 8.5 kB | A face of IBM Plex Mono for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-mono/ibm-plex-mono-500-latin-ext.woff2`](../public/fonts/ibm-plex-mono/ibm-plex-mono-500-latin-ext.woff2) | 13.4 kB | A face of IBM Plex Mono for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-mono/ibm-plex-mono-500-latin.woff2`](../public/fonts/ibm-plex-mono/ibm-plex-mono-500-latin.woff2) | 14.9 kB | A face of IBM Plex Mono for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-mono/ibm-plex-mono-500-vietnamese.woff2`](../public/fonts/ibm-plex-mono/ibm-plex-mono-500-vietnamese.woff2) | 6.0 kB | A face of IBM Plex Mono for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400-cyrillic-ext.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400-cyrillic-ext.woff2) | 23.6 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400-cyrillic.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400-cyrillic.woff2) | 29.5 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400-greek.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400-greek.woff2) | 19.5 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400-latin-ext.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400-latin-ext.woff2) | 31.0 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400-latin.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400-latin.woff2) | 45.7 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400-vietnamese.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400-vietnamese.woff2) | 13.2 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400i-cyrillic-ext.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400i-cyrillic-ext.woff2) | 13.4 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400i-cyrillic.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400i-cyrillic.woff2) | 16.1 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400i-greek.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400i-greek.woff2) | 10.6 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400i-latin-ext.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400i-latin-ext.woff2) | 17.0 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400i-latin.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400i-latin.woff2) | 24.4 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-sans/ibm-plex-sans-400i-vietnamese.woff2`](../public/fonts/ibm-plex-sans/ibm-plex-sans-400i-vietnamese.woff2) | 8.7 kB | A face of IBM Plex Sans for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |

<details><summary>25 files: A face of IBM Plex Serif for one script range (name: weight, i for italic, range).</summary>

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-400-cyrillic-ext.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-400-cyrillic-ext.woff2) | 8.9 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-400-cyrillic.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-400-cyrillic.woff2) | 12.3 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-400-latin-ext.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-400-latin-ext.woff2) | 15.5 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-400-latin.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-400-latin.woff2) | 19.6 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-400-vietnamese.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-400-vietnamese.woff2) | 6.2 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-400i-cyrillic-ext.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-400i-cyrillic-ext.woff2) | 10.1 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-400i-cyrillic.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-400i-cyrillic.woff2) | 14.2 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-400i-latin-ext.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-400i-latin-ext.woff2) | 16.3 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-400i-latin.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-400i-latin.woff2) | 20.9 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-400i-vietnamese.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-400i-vietnamese.woff2) | 6.4 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-500-cyrillic-ext.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-500-cyrillic-ext.woff2) | 8.7 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-500-cyrillic.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-500-cyrillic.woff2) | 12.1 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-500-latin-ext.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-500-latin-ext.woff2) | 15.5 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-500-latin.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-500-latin.woff2) | 20.3 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-500-vietnamese.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-500-vietnamese.woff2) | 6.2 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-600-cyrillic-ext.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-600-cyrillic-ext.woff2) | 8.7 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-600-cyrillic.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-600-cyrillic.woff2) | 12.2 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-600-latin-ext.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-600-latin-ext.woff2) | 15.6 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-600-latin.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-600-latin.woff2) | 20.5 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-600-vietnamese.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-600-vietnamese.woff2) | 6.3 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-700-cyrillic-ext.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-700-cyrillic-ext.woff2) | 8.7 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-700-cyrillic.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-700-cyrillic.woff2) | 12.0 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-700-latin-ext.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-700-latin-ext.woff2) | 15.6 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-700-latin.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-700-latin.woff2) | 19.9 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/ibm-plex-serif/ibm-plex-serif-700-vietnamese.woff2`](../public/fonts/ibm-plex-serif/ibm-plex-serif-700-vietnamese.woff2) | 6.4 kB | A face of IBM Plex Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |

</details>

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/fonts/instrument-plex.css`](../public/fonts/instrument-plex.css) | 14.1 kB | Instrument Serif, IBM Plex Sans and Mono, served by the site itself: the @font-face rules sim.css, catalog.css and the project copies import. | [assets.md](assets.md) |
| [`public/fonts/instrument-serif/instrument-serif-400-latin-ext.woff2`](../public/fonts/instrument-serif/instrument-serif-400-latin-ext.woff2) | 11.6 kB | A face of Instrument Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/instrument-serif/instrument-serif-400-latin.woff2`](../public/fonts/instrument-serif/instrument-serif-400-latin.woff2) | 21.0 kB | A face of Instrument Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/instrument-serif/instrument-serif-400i-latin-ext.woff2`](../public/fonts/instrument-serif/instrument-serif-400i-latin-ext.woff2) | 12.4 kB | A face of Instrument Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/instrument-serif/instrument-serif-400i-latin.woff2`](../public/fonts/instrument-serif/instrument-serif-400i-latin.woff2) | 22.1 kB | A face of Instrument Serif for one script range (name: weight, i for italic, range). | [assets.md](assets.md) |
| [`public/fonts/noto-naskh-arabic/noto-naskh-arabic-wght-arabic.woff2`](../public/fonts/noto-naskh-arabic/noto-naskh-arabic-wght-arabic.woff2) | 88.2 kB | Noto Naskh Arabic, variable weight 400 to 700, cut to the Arabic blocks. | [assets.md](assets.md) |
| [`public/fonts/plex.css`](../public/fonts/plex.css) | 21.3 kB | IBM Plex Mono, Sans and Serif, served by the site itself: the @font-face rules site.css imports. | [assets.md](assets.md) |

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

## Logo

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/images/phyein-usul-mark.svg`](../public/images/phyein-usul-mark.svg) | 178.4 kB | The Phyein Usul logo: above the name on the home page, linking home in the top bar of the other pages. | [assets.md](assets.md) |

## Project copy: Droplet Collection

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/portfolios/droplet-collection/fig/c1_ice.svg`](../public/portfolios/droplet-collection/fig/c1_ice.svg) | 86.8 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/ecoll_map.svg`](../public/portfolios/droplet-collection/fig/ecoll_map.svg) | 75.7 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/fallspeed_gk.svg`](../public/portfolios/droplet-collection/fig/fallspeed_gk.svg) | 57.1 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/golovin.svg`](../public/portfolios/droplet-collection/fig/golovin.svg) | 56.2 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/plate-efficiency.svg`](../public/portfolios/droplet-collection/fig/plate-efficiency.svg) | 8.9 kB | Plate of the Portfolios page article (efficiency), written by the Droplet Collection build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/plate-fallspeed.svg`](../public/portfolios/droplet-collection/fig/plate-fallspeed.svg) | 9.4 kB | Plate of the Portfolios page article (fallspeed), written by the Droplet Collection build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/plate-first.svg`](../public/portfolios/droplet-collection/fig/plate-first.svg) | 40.9 kB | Plate of the Portfolios page article (first), written by the Droplet Collection build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/plate-warm.svg`](../public/portfolios/droplet-collection/fig/plate-warm.svg) | 24.3 kB | Plate of the Portfolios page article (warm), written by the Droplet Collection build. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/w2_rain.svg`](../public/portfolios/droplet-collection/fig/w2_rain.svg) | 45.0 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/fig/w2_spectra.svg`](../public/portfolios/droplet-collection/fig/w2_spectra.svg) | 74.0 kB | A vector figure of the project. | [portfolios.md](portfolios.md) |
| [`public/portfolios/droplet-collection/index.html`](../public/portfolios/droplet-collection/index.html) | 984.4 kB | Entry page of the project copy: module script and stylesheet loader. | [portfolios.md](portfolios.md) |

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
| [`public/portfolios/rotor-pendula/index.html`](../public/portfolios/rotor-pendula/index.html) | 1.3 kB | Entry page of the project copy: module script and stylesheet loader. | [portfolios.md](portfolios.md) |

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
| [`public/portfolios/rotor-pendula/static/index-CNYGhWdg.css`](../public/portfolios/rotor-pendula/static/index-CNYGhWdg.css) | 65.3 kB | The project's stylesheet, built. | [portfolios.md](portfolios.md) |
| [`public/portfolios/rotor-pendula/static/index-CsGEKbO8.js`](../public/portfolios/rotor-pendula/static/index-CsGEKbO8.js) | 1.01 MB | The whole project application, built and minified. | [portfolios.md](portfolios.md) |
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

## Project copy: Hydraulic Press Study

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/portfolios/hydraulics/LICENSE-fonts.txt`](../public/portfolios/hydraulics/LICENSE-fonts.txt) | 8.5 kB | Licences of the fonts embedded in the study (OFL 1.1; MIT for KaTeX). | [portfolios.md](portfolios.md) |
| [`public/portfolios/hydraulics/fig/01_press.webp`](../public/portfolios/hydraulics/fig/01_press.webp) | 30.4 kB | Plate 1 of the study on the Portfolios page, 600 px high. | [portfolios.md](portfolios.md) |
| [`public/portfolios/hydraulics/fig/02_traces.webp`](../public/portfolios/hydraulics/fig/02_traces.webp) | 31.2 kB | Plate 2 of the study on the Portfolios page, 600 px high. | [portfolios.md](portfolios.md) |
| [`public/portfolios/hydraulics/fig/03_loop.webp`](../public/portfolios/hydraulics/fig/03_loop.webp) | 36.8 kB | Plate 3 of the study on the Portfolios page, 600 px high. | [portfolios.md](portfolios.md) |
| [`public/portfolios/hydraulics/fig/04_map.webp`](../public/portfolios/hydraulics/fig/04_map.webp) | 36.1 kB | Plate 4 of the study on the Portfolios page, 600 px high. | [portfolios.md](portfolios.md) |
| [`public/portfolios/hydraulics/index.html`](../public/portfolios/hydraulics/index.html) | 5.16 MB | The whole Hydraulic Press Study: tab bar and three embedded pages, generated from portfolios-src/hydraulics/. | [portfolios.md](portfolios.md) |

## Iron, Cotton and the Head

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`public/portfolios/impact/ar.html`](../public/portfolios/impact/ar.html) | 135.8 kB | Iron, Cotton and the Head in Arabic, generated from portfolios-src/impact/ by build.py --site. | [portfolios.md](portfolios.md) |
| [`public/portfolios/impact/fig/01_impact.webp`](../public/portfolios/impact/fig/01_impact.webp) | 16.9 kB | Plate 1 of the study on the Portfolios page, a screenshot of its English page, 600 px high. | [portfolios.md](portfolios.md) |
| [`public/portfolios/impact/fig/02_force.webp`](../public/portfolios/impact/fig/02_force.webp) | 19.5 kB | Plate 2 of the study on the Portfolios page, a screenshot of its English page, 600 px high. | [portfolios.md](portfolios.md) |
| [`public/portfolios/impact/fig/03_energy.webp`](../public/portfolios/impact/fig/03_energy.webp) | 20.2 kB | Plate 3 of the study on the Portfolios page, a screenshot of its English page, 600 px high. | [portfolios.md](portfolios.md) |
| [`public/portfolios/impact/fig/04_weight.webp`](../public/portfolios/impact/fig/04_weight.webp) | 18.2 kB | Plate 4 of the study on the Portfolios page, a screenshot of its English page, 600 px high. | [portfolios.md](portfolios.md) |
| [`public/portfolios/impact/index.html`](../public/portfolios/impact/index.html) | 124.1 kB | Iron, Cotton and the Head in English, generated from portfolios-src/impact/ by build.py --site. | [portfolios.md](portfolios.md) |

## Source of the Hydraulic Press Study (not served)

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`portfolios-src/hydraulics/.gitignore`](../portfolios-src/hydraulics/.gitignore) | 148 B | Keeps the files the checks and the standalone build write out of git. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/README.md`](../portfolios-src/hydraulics/README.md) | 5.8 kB | The study's source: what it is, how the served page is generated, the four checks. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/check_control.py`](../portfolios-src/hydraulics/check_control.py) | 17.2 kB | Checks the servo press's physics and loop analysis against an independent SciPy/SymPy model. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/check_physics.py`](../portfolios-src/hydraulics/check_physics.py) | 12.6 kB | Checks the ideal press's physics against an independent Python model. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/dump_control.js`](../portfolios-src/hydraulics/dump_control.js) | 2.2 kB | Runs the servo press page's physics block in Node for its check script. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/dump_runs.js`](../portfolios-src/hydraulics/dump_runs.js) | 1.6 kB | Runs the ideal press page's physics block in Node for its check script. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/fonts/LICENSE-fonts.txt`](../portfolios-src/hydraulics/fonts/LICENSE-fonts.txt) | 8.5 kB | Licences of the embedded fonts (OFL 1.1; MIT for KaTeX). | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/fonts/fonts-embedded.css`](../portfolios-src/hydraulics/fonts/fonts-embedded.css) | 233.7 kB | The @font-face rules of the study, fonts as data: addresses. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/fonts/fonts-linked.css`](../portfolios-src/hydraulics/fonts/fonts-linked.css) | 3.2 kB | The @font-face rules of the study, fonts linked as files. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/fonts/ibm-plex-mono-400-normal-latin.woff2`](../portfolios-src/hydraulics/fonts/ibm-plex-mono-400-normal-latin.woff2) | 14.7 kB | A subset of IBM Plex Sans, IBM Plex Mono or Instrument Serif embedded in the study. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/fonts/ibm-plex-mono-500-normal-latin.woff2`](../portfolios-src/hydraulics/fonts/ibm-plex-mono-500-normal-latin.woff2) | 14.9 kB | A subset of IBM Plex Sans, IBM Plex Mono or Instrument Serif embedded in the study. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/fonts/ibm-plex-sans-400-600-normal-greek.woff2`](../portfolios-src/hydraulics/fonts/ibm-plex-sans-400-600-normal-greek.woff2) | 19.5 kB | A subset of IBM Plex Sans, IBM Plex Mono or Instrument Serif embedded in the study. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/fonts/ibm-plex-sans-400-600-normal-latin.woff2`](../portfolios-src/hydraulics/fonts/ibm-plex-sans-400-600-normal-latin.woff2) | 45.7 kB | A subset of IBM Plex Sans, IBM Plex Mono or Instrument Serif embedded in the study. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/fonts/ibm-plex-sans-400-italic-greek.woff2`](../portfolios-src/hydraulics/fonts/ibm-plex-sans-400-italic-greek.woff2) | 10.6 kB | A subset of IBM Plex Sans, IBM Plex Mono or Instrument Serif embedded in the study. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/fonts/ibm-plex-sans-400-italic-latin.woff2`](../portfolios-src/hydraulics/fonts/ibm-plex-sans-400-italic-latin.woff2) | 24.4 kB | A subset of IBM Plex Sans, IBM Plex Mono or Instrument Serif embedded in the study. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/fonts/instrument-serif-400-italic-latin.woff2`](../portfolios-src/hydraulics/fonts/instrument-serif-400-italic-latin.woff2) | 22.1 kB | A subset of IBM Plex Sans, IBM Plex Mono or Instrument Serif embedded in the study. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/fonts/instrument-serif-400-normal-latin.woff2`](../portfolios-src/hydraulics/fonts/instrument-serif-400-normal-latin.woff2) | 21.0 kB | A subset of IBM Plex Sans, IBM Plex Mono or Instrument Serif embedded in the study. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/hydraulic.html`](../portfolios-src/hydraulics/hydraulic.html) | 694.9 kB | Pascal's ideal press, animated from its Lagrangian. Edited directly. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/hydraulic_control.html`](../portfolios-src/hydraulics/hydraulic_control.html) | 1.03 MB | The servo press: animation, controller, gauges, time traces, loop analysis, worked solutions. Edited directly. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/hydraulic_theory.html`](../portfolios-src/hydraulics/hydraulic_theory.html) | 2.64 MB | Hydraulics from First Principles, the 23-chapter text; generated by tools/build_theory.py. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/package.json`](../portfolios-src/hydraulics/package.json) | 174 B | Declares the study's Node scripts CommonJS (the site root declares ES modules). | [portfolios.md](portfolios.md) |
| [`portfolios-src/hydraulics/theory/00_map.src.html`](../portfolios-src/hydraulics/theory/00_map.src.html) | 21.6 kB | Source of the text, part 00 (map): HTML with LaTeX maths. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/theory/01_ideal.src.html`](../portfolios-src/hydraulics/theory/01_ideal.src.html) | 23.5 kB | Source of the text, part 01 (ideal): HTML with LaTeX maths. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/theory/02_servo.src.html`](../portfolios-src/hydraulics/theory/02_servo.src.html) | 46.1 kB | Source of the text, part 02 (servo): HTML with LaTeX maths. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/theory/03_control.src.html`](../portfolios-src/hydraulics/theory/03_control.src.html) | 53.3 kB | Source of the text, part 03 (control): HTML with LaTeX maths. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/build_combined.py`](../portfolios-src/hydraulics/tools/build_combined.py) | 13.0 kB | Generates public/portfolios/hydraulics/index.html from the three pages (--site). | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/build_fonts.py`](../portfolios-src/hydraulics/tools/build_fonts.py) | 9.7 kB | Downloads the font subsets in fonts/ and writes their @font-face rules. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/build_theory.py`](../portfolios-src/hydraulics/tools/build_theory.py) | 6.9 kB | Builds hydraulic_theory.html from theory/*.src.html, typesetting every formula with KaTeX. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/check_combined.py`](../portfolios-src/hydraulics/tools/check_combined.py) | 10.2 kB | Browser check of the served page: 33 checks of completeness, working controls, links, layout. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/check_data_panel.cjs`](../portfolios-src/hydraulics/tools/check_data_panel.cjs) | 5.0 kB | Checks the data panel inside the ideal and servo frames in a real browser. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/check_theory_numbers.js`](../portfolios-src/hydraulics/tools/check_theory_numbers.js) | 11.0 kB | Recomputes the 52 numbers the text quotes from the page's models. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/katex_render.js`](../portfolios-src/hydraulics/tools/katex_render.js) | 613 B | Typesets one batch of formulas with KaTeX for the build scripts. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/package-lock.json`](../portfolios-src/hydraulics/tools/package-lock.json) | 1.1 kB | Pins KaTeX 0.16.11 for the build scripts (lockfile). | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/package.json`](../portfolios-src/hydraulics/tools/package.json) | 207 B | Pins KaTeX 0.16.11 for the build scripts. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/page_equations.py`](../portfolios-src/hydraulics/tools/page_equations.py) | 8.8 kB | The TeX of the equation blocks on the two simulation pages. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/render_page_math.py`](../portfolios-src/hydraulics/tools/render_page_math.py) | 3.3 kB | Typesets the equation blocks inside the two simulation pages. | [README.md](../portfolios-src/hydraulics/README.md) |
| [`portfolios-src/hydraulics/tools/theory_template.html`](../portfolios-src/hydraulics/tools/theory_template.html) | 15.9 kB | The page the text is set into. | [README.md](../portfolios-src/hydraulics/README.md) |

## Source of Iron, Cotton and the Head (not served)

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`portfolios-src/impact/.gitignore`](../portfolios-src/impact/.gitignore) | 11 B | Keeps the stand-alone build (out/) and screenshots out of git. | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/README.md`](../portfolios-src/impact/README.md) | 2.8 kB | The study's source: every file, how the two pages are generated, the checks. | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/build.py`](../portfolios-src/impact/build.py) | 7.5 kB | Generates public/portfolios/impact/index.html and ar.html (--site), or stand-alone pages in out/. | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/checks/data_panel.cjs`](../portfolios-src/impact/checks/data_panel.cjs) | 10.1 kB | Check script data_panel (see the README). | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/checks/energy_books.cjs`](../portfolios-src/impact/checks/energy_books.cjs) | 1.1 kB | Check script energy_books (see the README). | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/checks/plate3.cjs`](../portfolios-src/impact/checks/plate3.cjs) | 699 B | Check script plate3 (see the README). | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/checks/plates.cjs`](../portfolios-src/impact/checks/plates.cjs) | 1.2 kB | Check script plates (see the README). | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/checks/portfolio_page.cjs`](../portfolios-src/impact/checks/portfolio_page.cjs) | 1.4 kB | Check script portfolio_page (see the README). | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/checks/site_check.cjs`](../portfolios-src/impact/checks/site_check.cjs) | 1.8 kB | Check script site_check (see the README). | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/checks/step_size.cjs`](../portfolios-src/impact/checks/step_size.cjs) | 323 B | Check script step_size (see the README). | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/checks/walkthrough.cjs`](../portfolios-src/impact/checks/walkthrough.cjs) | 1.9 kB | Check script walkthrough (see the README). | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/checks/weights.cjs`](../portfolios-src/impact/checks/weights.cjs) | 588 B | Check script weights (see the README). | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/datahooks.js`](../portfolios-src/impact/datahooks.js) | 29.6 kB | The data panel's hooks for the study (Sim.data: Read values, Check, read-back, one round = one drop). | [portfolios.md](portfolios.md) |
| [`portfolios-src/impact/physics.cjs`](../portfolios-src/impact/physics.cjs) | 10.6 kB | The model: Morse-bonded iron, fibre-network cotton, the head and scale, energy books (.cjs: the same file for the Node checks). | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/physics.js`](../portfolios-src/impact/physics.js) | 10.6 kB | The model: Morse-bonded iron, fibre-network cotton, the head and scale, energy books (.cjs: the same file for the Node checks). | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/template.html`](../portfolios-src/impact/template.html) | 50.9 kB | The page template: layout, the store filled by record(), drawing, playback, gauges, plots. | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/text_ar.py`](../portfolios-src/impact/text_ar.py) | 40.8 kB | Every word of the Arabic page. | [README.md](../portfolios-src/impact/README.md) |
| [`portfolios-src/impact/text_en.py`](../portfolios-src/impact/text_en.py) | 30.4 kB | Every word of the English page. | [README.md](../portfolios-src/impact/README.md) |

## Source of the Rotor Pendula notes (not served)

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`portfolios-src/rotor-pendula/fonts/LICENSE-fonts.txt`](../portfolios-src/rotor-pendula/fonts/LICENSE-fonts.txt) | 8.5 kB | Fonts of the Rotor Pendula notes build: LICENSE-fonts.txt. | [LICENSE-fonts.txt](../portfolios-src/rotor-pendula/fonts/LICENSE-fonts.txt) |
| [`portfolios-src/rotor-pendula/fonts/fonts-embedded.css`](../portfolios-src/rotor-pendula/fonts/fonts-embedded.css) | 233.7 kB | Fonts of the Rotor Pendula notes build: fonts-embedded.css. | [fonts-embedded.css](../portfolios-src/rotor-pendula/fonts/fonts-embedded.css) |
| [`portfolios-src/rotor-pendula/fonts/fonts-linked.css`](../portfolios-src/rotor-pendula/fonts/fonts-linked.css) | 3.2 kB | Fonts of the Rotor Pendula notes build: fonts-linked.css. | [fonts-linked.css](../portfolios-src/rotor-pendula/fonts/fonts-linked.css) |
| [`portfolios-src/rotor-pendula/fonts/ibm-plex-mono-400-normal-latin.woff2`](../portfolios-src/rotor-pendula/fonts/ibm-plex-mono-400-normal-latin.woff2) | 14.7 kB | Self-hosted font for the Rotor Pendula notes build: ibm-plex-mono-400-normal-latin.woff2. | [ibm-plex-mono-400-normal-latin.woff2](../portfolios-src/rotor-pendula/fonts/ibm-plex-mono-400-normal-latin.woff2) |
| [`portfolios-src/rotor-pendula/fonts/ibm-plex-mono-500-normal-latin.woff2`](../portfolios-src/rotor-pendula/fonts/ibm-plex-mono-500-normal-latin.woff2) | 14.9 kB | Self-hosted font for the Rotor Pendula notes build: ibm-plex-mono-500-normal-latin.woff2. | [ibm-plex-mono-500-normal-latin.woff2](../portfolios-src/rotor-pendula/fonts/ibm-plex-mono-500-normal-latin.woff2) |
| [`portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-600-normal-greek.woff2`](../portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-600-normal-greek.woff2) | 19.5 kB | Self-hosted font for the Rotor Pendula notes build: ibm-plex-sans-400-600-normal-greek.woff2. | [ibm-plex-sans-400-600-normal-greek.woff2](../portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-600-normal-greek.woff2) |
| [`portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-600-normal-latin.woff2`](../portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-600-normal-latin.woff2) | 45.7 kB | Self-hosted font for the Rotor Pendula notes build: ibm-plex-sans-400-600-normal-latin.woff2. | [ibm-plex-sans-400-600-normal-latin.woff2](../portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-600-normal-latin.woff2) |
| [`portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-italic-greek.woff2`](../portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-italic-greek.woff2) | 10.6 kB | Self-hosted font for the Rotor Pendula notes build: ibm-plex-sans-400-italic-greek.woff2. | [ibm-plex-sans-400-italic-greek.woff2](../portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-italic-greek.woff2) |
| [`portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-italic-latin.woff2`](../portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-italic-latin.woff2) | 24.4 kB | Self-hosted font for the Rotor Pendula notes build: ibm-plex-sans-400-italic-latin.woff2. | [ibm-plex-sans-400-italic-latin.woff2](../portfolios-src/rotor-pendula/fonts/ibm-plex-sans-400-italic-latin.woff2) |
| [`portfolios-src/rotor-pendula/fonts/instrument-serif-400-italic-latin.woff2`](../portfolios-src/rotor-pendula/fonts/instrument-serif-400-italic-latin.woff2) | 22.1 kB | Self-hosted font for the Rotor Pendula notes build: instrument-serif-400-italic-latin.woff2. | [instrument-serif-400-italic-latin.woff2](../portfolios-src/rotor-pendula/fonts/instrument-serif-400-italic-latin.woff2) |
| [`portfolios-src/rotor-pendula/fonts/instrument-serif-400-normal-latin.woff2`](../portfolios-src/rotor-pendula/fonts/instrument-serif-400-normal-latin.woff2) | 21.0 kB | Self-hosted font for the Rotor Pendula notes build: instrument-serif-400-normal-latin.woff2. | [instrument-serif-400-normal-latin.woff2](../portfolios-src/rotor-pendula/fonts/instrument-serif-400-normal-latin.woff2) |
| [`portfolios-src/rotor-pendula/tools/build_combined.py`](../portfolios-src/rotor-pendula/tools/build_combined.py) | 13.0 kB | Build and check tool of the Rotor Pendula notes, adapted from the Hydraulic Press Study's tools: build_combined.py. | [build_combined.py](../portfolios-src/rotor-pendula/tools/build_combined.py) |
| [`portfolios-src/rotor-pendula/tools/build_fonts.py`](../portfolios-src/rotor-pendula/tools/build_fonts.py) | 9.7 kB | Build and check tool of the Rotor Pendula notes, adapted from the Hydraulic Press Study's tools: build_fonts.py. | [build_fonts.py](../portfolios-src/rotor-pendula/tools/build_fonts.py) |
| [`portfolios-src/rotor-pendula/tools/build_theory.py`](../portfolios-src/rotor-pendula/tools/build_theory.py) | 6.9 kB | Build and check tool of the Rotor Pendula notes, adapted from the Hydraulic Press Study's tools: build_theory.py. | [build_theory.py](../portfolios-src/rotor-pendula/tools/build_theory.py) |
| [`portfolios-src/rotor-pendula/tools/check_combined.py`](../portfolios-src/rotor-pendula/tools/check_combined.py) | 10.2 kB | Build and check tool of the Rotor Pendula notes, adapted from the Hydraulic Press Study's tools: check_combined.py. | [check_combined.py](../portfolios-src/rotor-pendula/tools/check_combined.py) |
| [`portfolios-src/rotor-pendula/tools/check_theory_numbers.js`](../portfolios-src/rotor-pendula/tools/check_theory_numbers.js) | 11.0 kB | Build and check tool of the Rotor Pendula notes, adapted from the Hydraulic Press Study's tools: check_theory_numbers.js. | [check_theory_numbers.js](../portfolios-src/rotor-pendula/tools/check_theory_numbers.js) |
| [`portfolios-src/rotor-pendula/tools/katex_render.js`](../portfolios-src/rotor-pendula/tools/katex_render.js) | 613 B | Build and check tool of the Rotor Pendula notes, adapted from the Hydraulic Press Study's tools: katex_render.js. | [katex_render.js](../portfolios-src/rotor-pendula/tools/katex_render.js) |
| [`portfolios-src/rotor-pendula/tools/package-lock.json`](../portfolios-src/rotor-pendula/tools/package-lock.json) | 1.1 kB | Build and check tool of the Rotor Pendula notes, adapted from the Hydraulic Press Study's tools: package-lock.json. | [package-lock.json](../portfolios-src/rotor-pendula/tools/package-lock.json) |
| [`portfolios-src/rotor-pendula/tools/package.json`](../portfolios-src/rotor-pendula/tools/package.json) | 207 B | Build and check tool of the Rotor Pendula notes, adapted from the Hydraulic Press Study's tools: package.json. | [package.json](../portfolios-src/rotor-pendula/tools/package.json) |
| [`portfolios-src/rotor-pendula/tools/theory_template.html`](../portfolios-src/rotor-pendula/tools/theory_template.html) | 15.7 kB | Build and check tool of the Rotor Pendula notes, adapted from the Hydraulic Press Study's tools: theory_template.html. | [theory_template.html](../portfolios-src/rotor-pendula/tools/theory_template.html) |

## Source of the Droplet Collection study (not served)

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`portfolios-src/droplets/.gitignore`](../portfolios-src/droplets/.gitignore) | 5 B | Keeps the stand-alone build (out/) out of git. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/README.md`](../portfolios-src/droplets/README.md) | 4.1 kB | The study's source: every folder, how the served page is built, the three checks. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/app.js`](../portfolios-src/droplets/app.js) | 12.8 kB | The page's script: tabs, hash routes, the three simulation panels. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/chart.cjs`](../portfolios-src/droplets/chart.cjs) | 7.7 kB | House-style SVG line charts for the figures and the page. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/checks/check_browser.py`](../portfolios-src/droplets/checks/check_browser.py) | 2.6 kB | Check: check_browser.py (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/checks/check_numbers.cjs`](../portfolios-src/droplets/checks/check_numbers.cjs) | 31.9 kB | Check: check_numbers.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/checks/check_physics.py`](../portfolios-src/droplets/checks/check_physics.py) | 15.4 kB | Check: check_physics.py (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/checks/model_dump.cjs`](../portfolios-src/droplets/checks/model_dump.cjs) | 2.8 kB | Check: model_dump.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/data/bridge.json`](../portfolios-src/droplets/data/bridge.json) | 56.1 kB | Data written by the model's run tools: bridge.json. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/data/cold.json`](../portfolios-src/droplets/data/cold.json) | 482 B | Data written by the model's run tools: cold.json. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/data/etab_split.json`](../portfolios-src/droplets/data/etab_split.json) | 181.9 kB | Data written by the model's run tools: etab_split.json. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/data/etab_warm.json`](../portfolios-src/droplets/data/etab_warm.json) | 23.4 kB | Data written by the model's run tools: etab_warm.json. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/data/hall1980.json`](../portfolios-src/droplets/data/hall1980.json) | 1.7 kB | Data written by the model's run tools: hall1980.json. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/data/stochastic.json`](../portfolios-src/droplets/data/stochastic.json) | 399.3 kB | Data written by the model's run tools: stochastic.json. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/data/warm.json`](../portfolios-src/droplets/data/warm.json) | 158.4 kB | Data written by the model's run tools: warm.json. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/derive/L0_numbers.py`](../portfolios-src/droplets/derive/L0_numbers.py) | 2.2 kB | Derivation or number script behind a Gate 1 contract: L0_numbers.py. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L0_population.py`](../portfolios-src/droplets/derive/L0_population.py) | 4.7 kB | Derivation or number script behind a Gate 1 contract: L0_population.py. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L0_r2.py`](../portfolios-src/droplets/derive/L0_r2.py) | 3.4 kB | Derivation or number script behind a Gate 1 contract: L0_r2.py. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L0_r3.cjs`](../portfolios-src/droplets/derive/L0_r3.cjs) | 4.7 kB | Derivation or number script behind a Gate 1 contract: L0_r3.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L0_sympy.py`](../portfolios-src/droplets/derive/L0_sympy.py) | 2.0 kB | Derivation or number script behind a Gate 1 contract: L0_sympy.py. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L0_wolfram.md`](../portfolios-src/droplets/derive/L0_wolfram.md) | 1.4 kB | Derivation or number script behind a Gate 1 contract: L0_wolfram.md. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L1_beard.py`](../portfolios-src/droplets/derive/L1_beard.py) | 2.9 kB | Derivation or number script behind a Gate 1 contract: L1_beard.py. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L1_r2.py`](../portfolios-src/droplets/derive/L1_r2.py) | 8.6 kB | Derivation or number script behind a Gate 1 contract: L1_r2.py. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L1_stokes_sympy.py`](../portfolios-src/droplets/derive/L1_stokes_sympy.py) | 1.6 kB | Derivation or number script behind a Gate 1 contract: L1_stokes_sympy.py. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L2_cross.cjs`](../portfolios-src/droplets/derive/L2_cross.cjs) | 2.0 kB | Derivation or number script behind a Gate 1 contract: L2_cross.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L2_langmuir.cjs`](../portfolios-src/droplets/derive/L2_langmuir.cjs) | 982 B | Derivation or number script behind a Gate 1 contract: L2_langmuir.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L2_numbers.cjs`](../portfolios-src/droplets/derive/L2_numbers.cjs) | 2.0 kB | Derivation or number script behind a Gate 1 contract: L2_numbers.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L2_pairs.cjs`](../portfolios-src/droplets/derive/L2_pairs.cjs) | 1.5 kB | Derivation or number script behind a Gate 1 contract: L2_pairs.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L2_r2.cjs`](../portfolios-src/droplets/derive/L2_r2.cjs) | 3.1 kB | Derivation or number script behind a Gate 1 contract: L2_r2.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L2_scan.cjs`](../portfolios-src/droplets/derive/L2_scan.cjs) | 714 B | Derivation or number script behind a Gate 1 contract: L2_scan.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L2_trace.cjs`](../portfolios-src/droplets/derive/L2_trace.cjs) | 1.8 kB | Derivation or number script behind a Gate 1 contract: L2_trace.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L2_traj.cjs`](../portfolios-src/droplets/derive/L2_traj.cjs) | 8.0 kB | Derivation or number script behind a Gate 1 contract: L2_traj.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L3_coal.py`](../portfolios-src/droplets/derive/L3_coal.py) | 1.2 kB | Derivation or number script behind a Gate 1 contract: L3_coal.py. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L4_conv.cjs`](../portfolios-src/droplets/derive/L4_conv.cjs) | 1.7 kB | Derivation or number script behind a Gate 1 contract: L4_conv.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L5_tail.cjs`](../portfolios-src/droplets/derive/L5_tail.cjs) | 1.2 kB | Derivation or number script behind a Gate 1 contract: L5_tail.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/L6_ayala.py`](../portfolios-src/droplets/derive/L6_ayala.py) | 1.1 kB | Derivation or number script behind a Gate 1 contract: L6_ayala.py. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/derive/beard.cjs`](../portfolios-src/droplets/derive/beard.cjs) | 1.4 kB | Derivation or number script behind a Gate 1 contract: beard.cjs. | [status.md](../notes/droplets/status.md) |
| [`portfolios-src/droplets/physics.cjs`](../portfolios-src/droplets/physics.cjs) | 36.5 kB | The model, L0 to L7: fall speeds, trajectories, kernel, collection equation, exact stochastic process, turbulence (runs in the page and in Node). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/template.html`](../portfolios-src/droplets/template.html) | 12.9 kB | The page template: house design, tabs, placeholders filled by the build. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/book-00.src.html`](../portfolios-src/droplets/text/book-00.src.html) | 3.9 kB | Lecture notes, chapter 0. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/book-01.src.html`](../portfolios-src/droplets/text/book-01.src.html) | 5.5 kB | Lecture notes, chapter 1. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/book-02.src.html`](../portfolios-src/droplets/text/book-02.src.html) | 7.7 kB | Lecture notes, chapter 2. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/book-03.src.html`](../portfolios-src/droplets/text/book-03.src.html) | 9.4 kB | Lecture notes, chapter 3. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/book-04.src.html`](../portfolios-src/droplets/text/book-04.src.html) | 4.1 kB | Lecture notes, chapter 4. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/book-05.src.html`](../portfolios-src/droplets/text/book-05.src.html) | 7.9 kB | Lecture notes, chapter 5. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/book-06.src.html`](../portfolios-src/droplets/text/book-06.src.html) | 8.0 kB | Lecture notes, chapter 6. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/book-07.src.html`](../portfolios-src/droplets/text/book-07.src.html) | 3.7 kB | Lecture notes, chapter 7. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/book-08.src.html`](../portfolios-src/droplets/text/book-08.src.html) | 7.0 kB | Lecture notes, chapter 8. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/book-09.src.html`](../portfolios-src/droplets/text/book-09.src.html) | 6.6 kB | Lecture notes, chapter 9 and appendix A. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/checks.src.html`](../portfolios-src/droplets/text/checks.src.html) | 5.8 kB | Words of the checks tab. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/problems.src.html`](../portfolios-src/droplets/text/problems.src.html) | 4.4 kB | Words of the problems tab. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/text/sim.src.html`](../portfolios-src/droplets/text/sim.src.html) | 3.8 kB | Words of the sim tab. | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/build.py`](../portfolios-src/droplets/tools/build.py) | 10.6 kB | Build or run tool: build.py (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/figs.cjs`](../portfolios-src/droplets/tools/figs.cjs) | 11.0 kB | Build or run tool: figs.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/gen_tables.cjs`](../portfolios-src/droplets/tools/gen_tables.cjs) | 1.0 kB | Build or run tool: gen_tables.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/katex_render.cjs`](../portfolios-src/droplets/tools/katex_render.cjs) | 606 B | Build or run tool: katex_render.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/package-lock.json`](../portfolios-src/droplets/tools/package-lock.json) | 1.1 kB | Build or run tool: package-lock.json (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/package.json`](../portfolios-src/droplets/tools/package.json) | 207 B | Build or run tool: package.json (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/run_bridge.cjs`](../portfolios-src/droplets/tools/run_bridge.cjs) | 1.3 kB | Build or run tool: run_bridge.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/run_cold.cjs`](../portfolios-src/droplets/tools/run_cold.cjs) | 5.5 kB | Build or run tool: run_cold.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/run_golovin.cjs`](../portfolios-src/droplets/tools/run_golovin.cjs) | 2.7 kB | Build or run tool: run_golovin.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/run_stochastic.cjs`](../portfolios-src/droplets/tools/run_stochastic.cjs) | 2.3 kB | Build or run tool: run_stochastic.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/run_warm.cjs`](../portfolios-src/droplets/tools/run_warm.cjs) | 3.2 kB | Build or run tool: run_warm.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/tail_resolution.cjs`](../portfolios-src/droplets/tools/tail_resolution.cjs) | 1.2 kB | Build or run tool: tail_resolution.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |
| [`portfolios-src/droplets/tools/test_gillespie.cjs`](../portfolios-src/droplets/tools/test_gillespie.cjs) | 1.6 kB | Build or run tool: test_gillespie.cjs (see the README). | [README.md](../portfolios-src/droplets/README.md) |

## Template sources

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`src/main.ts`](../src/main.ts) | 23 B | Template script entry; index.html does not load it. | [build-and-deploy.md](build-and-deploy.md) |
| [`src/styles.css`](../src/styles.css) | 73 B | Template Tailwind directives; unused. | [build-and-deploy.md](build-and-deploy.md) |

## Platform tests

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`tests/tests.json`](../tests/tests.json) | 17.1 kB | Plain-language test scenarios run by the platform's QA after each deploy. | [build-and-deploy.md](build-and-deploy.md) |

## Documentation

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`docs/appdeploy-app.md`](appdeploy-app.md) | 2.5 kB | Documentation: The AppDeploy app · numa-koudsie-website-0cyj78. | [appdeploy-app.md](appdeploy-app.md) |
| [`docs/architecture.md`](architecture.md) | 7.9 kB | Documentation: How the site fits together. | [architecture.md](architecture.md) |
| [`docs/assets.md`](assets.md) | 10.8 kB | Documentation: Fonts, maths and pictures: `public/vendor/`, `public/fonts/`, `public/images/`. | [assets.md](assets.md) |
| [`docs/build-and-deploy.md`](build-and-deploy.md) | 19.0 kB | Documentation: Build files, tests and deployment. | [build-and-deploy.md](build-and-deploy.md) |
| [`docs/files.md`](files.md) | this file | This list. Written by tools/inventory.py; do not edit by hand. | [files.md](files.md) |
| [`docs/glossary.md`](glossary.md) | 7.7 kB | Documentation: Glossary: English, German, Arabic. | [glossary.md](glossary.md) |
| [`docs/i18n.md`](i18n.md) | 8.7 kB | Documentation: The site in German and Arabic: `tools/i18n/`, `i18n/`, `public/de/`, `public/ar/`. | [i18n.md](i18n.md) |
| [`docs/minor-issues-report.md`](minor-issues-report.md) | 19.9 kB | Documentation: Minor issues · final verification report. | [minor-issues-report.md](minor-issues-report.md) |
| [`docs/notes.md`](notes.md) | 3.7 kB | Documentation: The lecture-note review: `notes/` and `.claude/agents/`. | [notes.md](notes.md) |
| [`docs/pages.md`](pages.md) | 51.9 kB | Documentation: The site's own pages: home, simulations catalog, Portfolios, robots.txt. | [pages.md](pages.md) |
| [`docs/portfolios.md`](portfolios.md) | 39.5 kB | Documentation: The four research projects: `public/portfolios/`. | [portfolios.md](portfolios.md) |
| [`docs/research-theory-audit.md`](research-theory-audit.md) | 29.1 kB | Documentation: Readability audit: Droplet Collection and Rotor Pendula. | [research-theory-audit.md](research-theory-audit.md) |
| [`docs/scripts/catalog.md`](scripts/catalog.md) | 15.1 kB | Documentation: public/scripts/catalog.js. | [catalog.md](scripts/catalog.md) |
| [`docs/scripts/datalog.md`](scripts/datalog.md) | 48.6 kB | Documentation: public/scripts/datalog.js. | [datalog.md](scripts/datalog.md) |
| [`docs/scripts/dataset.md`](scripts/dataset.md) | 17.0 kB | Documentation: public/scripts/dataset.js. | [dataset.md](scripts/dataset.md) |
| [`docs/scripts/fold.md`](scripts/fold.md) | 22.6 kB | Documentation: public/scripts/fold.js. | [fold.md](scripts/fold.md) |
| [`docs/scripts/sim.md`](scripts/sim.md) | 26.6 kB | Documentation: public/scripts/sim.js. | [sim.md](scripts/sim.md) |
| [`docs/scripts/walk.md`](scripts/walk.md) | 19.9 kB | Documentation: public/scripts/walk/*.js. | [walk.md](scripts/walk.md) |
| [`docs/simulations/fig01-wave-sources.md`](simulations/fig01-wave-sources.md) | 50.0 kB | Documentation: Fig. 1 · Wave Interference. | [fig01-wave-sources.md](simulations/fig01-wave-sources.md) |
| [`docs/simulations/fig02-double-pendulum.md`](simulations/fig02-double-pendulum.md) | 49.6 kB | Documentation: Fig. 2 · Double Pendulum. | [fig02-double-pendulum.md](simulations/fig02-double-pendulum.md) |
| [`docs/simulations/fig03-double-slit.md`](simulations/fig03-double-slit.md) | 44.3 kB | Documentation: Fig. 3 · Double-Slit Interference. | [fig03-double-slit.md](simulations/fig03-double-slit.md) |
| [`docs/simulations/fig04-transverse-longitudinal.md`](simulations/fig04-transverse-longitudinal.md) | 39.6 kB | Documentation: Fig. 4 · Transverse and Longitudinal Waves. | [fig04-transverse-longitudinal.md](simulations/fig04-transverse-longitudinal.md) |
| [`docs/simulations/fig05-water-wave.md`](simulations/fig05-water-wave.md) | 35.8 kB | Documentation: Fig. 5 · Circular Water Waves. | [fig05-water-wave.md](simulations/fig05-water-wave.md) |
| [`docs/simulations/fig06-wave-bench.md`](simulations/fig06-wave-bench.md) | 42.7 kB | Documentation: Fig. 6 · Wave Interference Simulator. | [fig06-wave-bench.md](simulations/fig06-wave-bench.md) |
| [`docs/simulations/fig07-phasor-sums.md`](simulations/fig07-phasor-sums.md) | 41.7 kB | Documentation: Fig. 7 · Phasor Sums. | [fig07-phasor-sums.md](simulations/fig07-phasor-sums.md) |
| [`docs/simulations/fig08-draw-decompose.md`](simulations/fig08-draw-decompose.md) | 34.8 kB | Documentation: Fig. 8 · Draw & Decompose. | [fig08-draw-decompose.md](simulations/fig08-draw-decompose.md) |
| [`docs/simulations/fig09-driven-oscillator.md`](simulations/fig09-driven-oscillator.md) | 42.4 kB | Documentation: Fig. 9 · Driven Oscillator. | [fig09-driven-oscillator.md](simulations/fig09-driven-oscillator.md) |
| [`docs/simulations/fig10-wind-turbine.md`](simulations/fig10-wind-turbine.md) | 50.9 kB | Documentation: Fig. 10 · Wind Turbine Control. | [fig10-wind-turbine.md](simulations/fig10-wind-turbine.md) |
| [`docs/styles.md`](styles.md) | 42.7 kB | Documentation: Stylesheets: `public/styles/`. | [styles.md](styles.md) |
| [`docs/usul.md`](usul.md) | 6.2 kB | Documentation: Phyein Usul · the website at phyeinusul.com. | [usul.md](usul.md) |

## Tools

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`tools/i18n/build.py`](../tools/i18n/build.py) | 17.7 kB | Writes the German and Arabic pages, the script strings and the mirrored stylesheets from the English pages and the tables; --check fails on anything untranslated. | [i18n.md](i18n.md) |
| [`tools/i18n/fill.py`](../tools/i18n/fill.py) | 1.3 kB | Stores translations into a page table, recording the English each one was made from. | [i18n.md](i18n.md) |
| [`tools/inventory.py`](../tools/inventory.py) | 36.5 kB | Writes docs/files.md and checks that every file in the repository is described. | [files.md](files.md) |
| [`tools/make_portfolio_copy.py`](../tools/make_portfolio_copy.py) | 4.4 kB | Builds a browser-only website copy of a research app from its source, without changing the app or installing dependencies. | [portfolios.md](portfolios.md) |

## Translation tables

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`i18n/ar/index.html.json`](../i18n/ar/index.html.json) | 21.9 kB | Arabic table of index.html: per piece, the English it was translated from and the translation. | [i18n.md](i18n.md) |
| [`i18n/ar/portfolios.html.json`](../i18n/ar/portfolios.html.json) | 60.5 kB | Arabic table of portfolios.html: per piece, the English it was translated from and the translation. | [i18n.md](i18n.md) |
| [`i18n/ar/simulations.html.json`](../i18n/ar/simulations.html.json) | 6.6 kB | Arabic table of simulations.html: per piece, the English it was translated from and the translation. | [i18n.md](i18n.md) |
| [`i18n/ar/strings.json`](../i18n/ar/strings.json) | 19.6 kB | Arabic words of the scripts and of the catalog, with plural forms. | [i18n.md](i18n.md) |
| [`i18n/de/index.html.json`](../i18n/de/index.html.json) | 19.6 kB | German table of index.html: per piece, the English it was translated from and the translation. | [i18n.md](i18n.md) |
| [`i18n/de/portfolios.html.json`](../i18n/de/portfolios.html.json) | 53.0 kB | German table of portfolios.html: per piece, the English it was translated from and the translation. | [i18n.md](i18n.md) |
| [`i18n/de/simulations.html.json`](../i18n/de/simulations.html.json) | 5.8 kB | German table of simulations.html: per piece, the English it was translated from and the translation. | [i18n.md](i18n.md) |
| [`i18n/de/strings.json`](../i18n/de/strings.json) | 15.4 kB | German words of the scripts and of the catalog, with plural forms. | [i18n.md](i18n.md) |

## Agents of the lecture-note review

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`.claude/agents/derivation-checker.md`](../.claude/agents/derivation-checker.md) | 863 B | Claude Code agent definition: derivation-checker, one role of the lecture-note review. | [notes.md](notes.md) |
| [`.claude/agents/physics-teacher.md`](../.claude/agents/physics-teacher.md) | 1.5 kB | Claude Code agent definition: physics-teacher, one role of the lecture-note review. | [notes.md](notes.md) |
| [`.claude/agents/referee.md`](../.claude/agents/referee.md) | 760 B | Claude Code agent definition: referee, one role of the lecture-note review. | [notes.md](notes.md) |
| [`.claude/agents/walkthrough-keeper.md`](../.claude/agents/walkthrough-keeper.md) | 614 B | Claude Code agent definition: walkthrough-keeper, one role of the lecture-note review. | [notes.md](notes.md) |

## Working notes of the Rotor Pendula study

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`notes/rotor-pendula/baseline/checks.html`](../notes/rotor-pendula/baseline/checks.html) | 14.3 kB | Text of the checks page of the published Rotor Pendula app, kept as the baseline the study starts from. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/baseline/overview.html`](../notes/rotor-pendula/baseline/overview.html) | 5.7 kB | Text of the overview page of the published Rotor Pendula app, kept as the baseline the study starts from. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/baseline/report.html`](../notes/rotor-pendula/baseline/report.html) | 70.3 kB | Text of the report page of the published Rotor Pendula app, kept as the baseline the study starts from. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/baseline/results.html`](../notes/rotor-pendula/baseline/results.html) | 11.5 kB | Text of the results page of the published Rotor Pendula app, kept as the baseline the study starts from. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/baseline/simulate.html`](../notes/rotor-pendula/baseline/simulate.html) | 4.7 kB | Text of the simulate page of the published Rotor Pendula app, kept as the baseline the study starts from. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/baseline/theory.html`](../notes/rotor-pendula/baseline/theory.html) | 83.0 kB | Text of the theory page of the published Rotor Pendula app, kept as the baseline the study starts from. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/brief.md`](../notes/rotor-pendula/brief.md) | 19.8 kB | The brief of the Rotor Pendula study: question, method and gates, for an agent working in a loop. | [brief.md](../notes/rotor-pendula/brief.md) |
| [`notes/rotor-pendula/contract-L0.md`](../notes/rotor-pendula/contract-L0.md) | 11.5 kB | Gate 1 contract of model level L0: question, model, assumptions with their numbers, checks. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/contract-L1.md`](../notes/rotor-pendula/contract-L1.md) | 6.5 kB | Gate 1 contract of model level L1: question, model, assumptions with their numbers, checks. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/contract-L2.md`](../notes/rotor-pendula/contract-L2.md) | 7.3 kB | Gate 1 contract of model level L2: question, model, assumptions with their numbers, checks. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L0_r2.py`](../notes/rotor-pendula/derive/L0_r2.py) | 3.4 kB | Derivation or computation script of the study, L0_r2.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L0_single.py`](../notes/rotor-pendula/derive/L0_single.py) | 4.8 kB | Derivation or computation script of the study, L0_single.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L0_table.py`](../notes/rotor-pendula/derive/L0_table.py) | 5.8 kB | Derivation or computation script of the study, L0_table.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L1_chaos.json`](../notes/rotor-pendula/derive/L1_chaos.json) | 3.5 kB | Saved output of L1_chaos.py (numbers). | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L1_chaos.log`](../notes/rotor-pendula/derive/L1_chaos.log) | 1.3 kB | Saved output of L1_chaos.py (log). | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L1_chaos.py`](../notes/rotor-pendula/derive/L1_chaos.py) | 2.6 kB | Derivation or computation script of the study, L1_chaos.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L1_double.py`](../notes/rotor-pendula/derive/L1_double.py) | 7.5 kB | Derivation or computation script of the study, L1_double.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L1_engine_check.log`](../notes/rotor-pendula/derive/L1_engine_check.log) | 3.2 kB | Saved output of L1_engine_check.py (log). | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L1_engine_check.py`](../notes/rotor-pendula/derive/L1_engine_check.py) | 8.0 kB | Derivation or computation script of the study, L1_engine_check.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L1_map.json`](../notes/rotor-pendula/derive/L1_map.json) | 57.9 kB | Saved output of L1_map.py (numbers). | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L1_map.log`](../notes/rotor-pendula/derive/L1_map.log) | 2.6 kB | Saved output of L1_map.py (log). | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L1_map.py`](../notes/rotor-pendula/derive/L1_map.py) | 4.0 kB | Derivation or computation script of the study, L1_map.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L1_mountings.json`](../notes/rotor-pendula/derive/L1_mountings.json) | 5.9 kB | Saved output of L1_mountings.py (numbers). | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L2_run.json`](../notes/rotor-pendula/derive/L2_run.json) | 10.7 kB | Saved output of L2_run.py (numbers). | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L2_run.log`](../notes/rotor-pendula/derive/L2_run.log) | 1.1 kB | Saved output of L2_run.py (log). | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L2_run.py`](../notes/rotor-pendula/derive/L2_run.py) | 5.0 kB | Derivation or computation script of the study, L2_run.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/L2_scales.py`](../notes/rotor-pendula/derive/L2_scales.py) | 3.4 kB | Derivation or computation script of the study, L2_scales.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/data/Cp_Ct_Cq.NREL5MW.txt`](../notes/rotor-pendula/derive/data/Cp_Ct_Cq.NREL5MW.txt) | 33.1 kB | Cited data of the NREL 5-MW reference turbine: Cp_Ct_Cq.NREL5MW.txt. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/data/NRELOffshrBsline5MW_Blade.dat`](../notes/rotor-pendula/derive/data/NRELOffshrBsline5MW_Blade.dat) | 8.0 kB | Cited data of the NREL 5-MW reference turbine: NRELOffshrBsline5MW_Blade.dat. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/engine.py`](../notes/rotor-pendula/derive/engine.py) | 7.6 kB | Derivation or computation script of the study, engine.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/fermi.py`](../notes/rotor-pendula/derive/fermi.py) | 3.1 kB | Derivation or computation script of the study, fermi.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/mc_full.log`](../notes/rotor-pendula/derive/mc_full.log) | 2.2 kB | Saved output of mc_full.py (log). | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/mc_quick.log`](../notes/rotor-pendula/derive/mc_quick.log) | 2.2 kB | Saved output of mc_quick.py (log). | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/nrel5mw.py`](../notes/rotor-pendula/derive/nrel5mw.py) | 7.3 kB | Derivation or computation script of the study, nrel5mw.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/power_theorem.py`](../notes/rotor-pendula/derive/power_theorem.py) | 7.0 kB | Derivation or computation script of the study, power_theorem.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/power_theorem_mc.py`](../notes/rotor-pendula/derive/power_theorem_mc.py) | 6.4 kB | Derivation or computation script of the study, power_theorem_mc.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/scales.py`](../notes/rotor-pendula/derive/scales.py) | 2.7 kB | Derivation or computation script of the study, scales.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/derive/turbulence.py`](../notes/rotor-pendula/derive/turbulence.py) | 5.2 kB | Derivation or computation script of the study, turbulence.py: prints PASS/FAIL and exits 1 on a failure. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/done.md`](../notes/rotor-pendula/done.md) | 2.5 kB | Definition of done of the Rotor Pendula study, as a checklist; only Numa may change it. | [done.md](../notes/rotor-pendula/done.md) |
| [`notes/rotor-pendula/dossier-edgewise.md`](../notes/rotor-pendula/dossier-edgewise.md) | 33.9 kB | Scout dossier on edgewise: primary sources read for the study. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/dossier-harvesting.md`](../notes/rotor-pendula/dossier-harvesting.md) | 33.8 kB | Scout dossier on harvesting: primary sources read for the study. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/dossier-turbine.md`](../notes/rotor-pendula/dossier-turbine.md) | 54.8 kB | Scout dossier on turbine: primary sources read for the study. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/handoff-prompt.md`](../notes/rotor-pendula/handoff-prompt.md) | 11.7 kB | Prompt for handing the Rotor Pendula study to another agent. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/review-prompt.md`](../notes/rotor-pendula/review-prompt.md) | 3.6 kB | Prompt for an independent reviewer of the Rotor Pendula study. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/skeptic-G1-L0-r1.md`](../notes/rotor-pendula/skeptic-G1-L0-r1.md) | 17.4 kB | Blind skeptic report, gate 1, level L0, round 1. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/skeptic-G1-L2-r1.md`](../notes/rotor-pendula/skeptic-G1-L2-r1.md) | 17.5 kB | Blind skeptic report, gate 1, level L2, round 1. | [status.md](../notes/rotor-pendula/status.md) |
| [`notes/rotor-pendula/status.md`](../notes/rotor-pendula/status.md) | 10.0 kB | Status of the Rotor Pendula study: queue, done list with evidence, decisions for Numa. Read first. | [status.md](../notes/rotor-pendula/status.md) |

## Working notes of the Droplet Collection study

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`notes/droplets/baseline/checks.html`](../notes/droplets/baseline/checks.html) | 6.8 kB | Text of the checks page of the published Droplet Collection app, kept as the baseline the study starts from. | [brief.md](../notes/droplets/brief.md) |
| [`notes/droplets/baseline/overview.html`](../notes/droplets/baseline/overview.html) | 4.2 kB | Text of the overview page of the published Droplet Collection app, kept as the baseline the study starts from. | [brief.md](../notes/droplets/brief.md) |
| [`notes/droplets/baseline/results.html`](../notes/droplets/baseline/results.html) | 5.6 kB | Text of the results page of the published Droplet Collection app, kept as the baseline the study starts from. | [brief.md](../notes/droplets/brief.md) |
| [`notes/droplets/baseline/simulate.html`](../notes/droplets/baseline/simulate.html) | 2.0 kB | Text of the simulate page of the published Droplet Collection app, kept as the baseline the study starts from. | [brief.md](../notes/droplets/brief.md) |
| [`notes/droplets/baseline/theory.html`](../notes/droplets/baseline/theory.html) | 105.7 kB | Text of the theory page of the published Droplet Collection app, kept as the baseline the study starts from. | [brief.md](../notes/droplets/brief.md) |
| [`notes/droplets/brief.md`](../notes/droplets/brief.md) | 17.8 kB | The brief of the Droplet Collection study: question, method and gates, for an agent working in a loop. | [brief.md](../notes/droplets/brief.md) |
| [`notes/droplets/check-L0.md`](../notes/droplets/check-L0.md) | 4.2 kB | Gate 2 check of level L0: each equation re-derived by two routes. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/check-L1.md`](../notes/droplets/check-L1.md) | 6.7 kB | Gate 2 check of level L1: each equation re-derived by two routes. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/check-L2.md`](../notes/droplets/check-L2.md) | 7.7 kB | Gate 2 check of level L2: each equation re-derived by two routes. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/check-L3.md`](../notes/droplets/check-L3.md) | 4.1 kB | Gate 2 check of level L3: each equation re-derived by two routes. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/check-L4.md`](../notes/droplets/check-L4.md) | 6.2 kB | Gate 2 check of level L4: each equation re-derived by two routes. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/check-L5.md`](../notes/droplets/check-L5.md) | 6.5 kB | Gate 2 check of level L5: each equation re-derived by two routes. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/check-L6.md`](../notes/droplets/check-L6.md) | 5.8 kB | Gate 2 check of level L6: each equation re-derived by two routes. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/check-L7.md`](../notes/droplets/check-L7.md) | 6.6 kB | Gate 2 check of level L7: each equation re-derived by two routes. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/contract-L0.md`](../notes/droplets/contract-L0.md) | 25.2 kB | Gate 1 contract of model level L0: question, picture, model, assumptions with their numbers, predictions, answers to the skeptic. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/contract-L1.md`](../notes/droplets/contract-L1.md) | 18.6 kB | Gate 1 contract of model level L1: question, picture, model, assumptions with their numbers, predictions, answers to the skeptic. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/contract-L2.md`](../notes/droplets/contract-L2.md) | 20.0 kB | Gate 1 contract of model level L2: question, picture, model, assumptions with their numbers, predictions, answers to the skeptic. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/contract-L3.md`](../notes/droplets/contract-L3.md) | 7.1 kB | Gate 1 contract of model level L3: question, picture, model, assumptions with their numbers, predictions, answers to the skeptic. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/contract-L4.md`](../notes/droplets/contract-L4.md) | 14.5 kB | Gate 1 contract of model level L4: question, picture, model, assumptions with their numbers, predictions, answers to the skeptic. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/contract-L5.md`](../notes/droplets/contract-L5.md) | 14.5 kB | Gate 1 contract of model level L5: question, picture, model, assumptions with their numbers, predictions, answers to the skeptic. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/contract-L6.md`](../notes/droplets/contract-L6.md) | 4.1 kB | Gate 1 contract of model level L6: question, picture, model, assumptions with their numbers, predictions, answers to the skeptic. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/contract-L7.md`](../notes/droplets/contract-L7.md) | 6.1 kB | Gate 1 contract of model level L7: question, picture, model, assumptions with their numbers, predictions, answers to the skeptic. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/done.md`](../notes/droplets/done.md) | 1.7 kB | Definition of done of the Droplet Collection study, as a checklist; only Numa may change it. | [done.md](../notes/droplets/done.md) |
| [`notes/droplets/dossier-coalescence-turbulence.md`](../notes/droplets/dossier-coalescence-turbulence.md) | 26.2 kB | Scout dossier on coalescence-turbulence: primary sources read for the study. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/dossier-fallspeed-efficiency.md`](../notes/droplets/dossier-fallspeed-efficiency.md) | 38.0 kB | Scout dossier on fallspeed-efficiency: primary sources read for the study. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/dossier-ice.md`](../notes/droplets/dossier-ice.md) | 34.2 kB | Scout dossier on ice: primary sources read for the study. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/dossier-stochastic.md`](../notes/droplets/dossier-stochastic.md) | 59.4 kB | Scout dossier on stochastic: primary sources read for the study. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L0_model_crosscheck.cjs`](../notes/droplets/gate2/L0_model_crosscheck.cjs) | 844 B | Gate 2 checker script or output: L0_model_crosscheck.cjs. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L0_model_crosscheck.out.txt`](../notes/droplets/gate2/L0_model_crosscheck.out.txt) | 338 B | Gate 2 checker script or output: L0_model_crosscheck.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L0_route1_sympy.out.txt`](../notes/droplets/gate2/L0_route1_sympy.out.txt) | 2.1 kB | Gate 2 checker script or output: L0_route1_sympy.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L0_route1_sympy.py`](../notes/droplets/gate2/L0_route1_sympy.py) | 4.3 kB | Gate 2 checker script or output: L0_route1_sympy.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L0_route2.wl`](../notes/droplets/gate2/L0_route2.wl) | 1.4 kB | Gate 2 checker script or output: L0_route2.wl. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L0_route2_numeric.out.txt`](../notes/droplets/gate2/L0_route2_numeric.out.txt) | 1.6 kB | Gate 2 checker script or output: L0_route2_numeric.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L0_route2_numeric.py`](../notes/droplets/gate2/L0_route2_numeric.py) | 4.1 kB | Gate 2 checker script or output: L0_route2_numeric.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L0_route2_wolfram.out.txt`](../notes/droplets/gate2/L0_route2_wolfram.out.txt) | 624 B | Gate 2 checker script or output: L0_route2_wolfram.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_collector_time.cjs`](../notes/droplets/gate2/L1_collector_time.cjs) | 1.1 kB | Gate 2 checker script or output: L1_collector_time.cjs. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_collector_time.out.txt`](../notes/droplets/gate2/L1_collector_time.out.txt) | 130 B | Gate 2 checker script or output: L1_collector_time.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_model_dump.cjs`](../notes/droplets/gate2/L1_model_dump.cjs) | 564 B | Gate 2 checker script or output: L1_model_dump.cjs. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_model_dump.json`](../notes/droplets/gate2/L1_model_dump.json) | 2.0 kB | Gate 2 checker script or output: L1_model_dump.json. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_route1_sympy.out.txt`](../notes/droplets/gate2/L1_route1_sympy.out.txt) | 3.1 kB | Gate 2 checker script or output: L1_route1_sympy.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_route1_sympy.py`](../notes/droplets/gate2/L1_route1_sympy.py) | 8.4 kB | Gate 2 checker script or output: L1_route1_sympy.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_route2.wl`](../notes/droplets/gate2/L1_route2.wl) | 3.8 kB | Gate 2 checker script or output: L1_route2.wl. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_route2_dragcurve.out.txt`](../notes/droplets/gate2/L1_route2_dragcurve.out.txt) | 4.1 kB | Gate 2 checker script or output: L1_route2_dragcurve.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_route2_dragcurve.py`](../notes/droplets/gate2/L1_route2_dragcurve.py) | 3.7 kB | Gate 2 checker script or output: L1_route2_dragcurve.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_route2_numeric.out.txt`](../notes/droplets/gate2/L1_route2_numeric.out.txt) | 1.5 kB | Gate 2 checker script or output: L1_route2_numeric.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_route2_numeric.py`](../notes/droplets/gate2/L1_route2_numeric.py) | 4.6 kB | Gate 2 checker script or output: L1_route2_numeric.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L1_route2_wolfram.out.txt`](../notes/droplets/gate2/L1_route2_wolfram.out.txt) | 1.1 kB | Gate 2 checker script or output: L1_route2_wolfram.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_model_crosscheck.cjs`](../notes/droplets/gate2/L2_model_crosscheck.cjs) | 779 B | Gate 2 checker script or output: L2_model_crosscheck.cjs. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_model_crosscheck.out.txt`](../notes/droplets/gate2/L2_model_crosscheck.out.txt) | 430 B | Gate 2 checker script or output: L2_model_crosscheck.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_route1_sympy.out.txt`](../notes/droplets/gate2/L2_route1_sympy.out.txt) | 3.9 kB | Gate 2 checker script or output: L2_route1_sympy.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_route1_sympy.py`](../notes/droplets/gate2/L2_route1_sympy.py) | 7.6 kB | Gate 2 checker script or output: L2_route1_sympy.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_route2.wl`](../notes/droplets/gate2/L2_route2.wl) | 1.5 kB | Gate 2 checker script or output: L2_route2.wl. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_route2_numeric.out.txt`](../notes/droplets/gate2/L2_route2_numeric.out.txt) | 2.6 kB | Gate 2 checker script or output: L2_route2_numeric.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_route2_numeric.py`](../notes/droplets/gate2/L2_route2_numeric.py) | 7.6 kB | Gate 2 checker script or output: L2_route2_numeric.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_route2_wolfram.out.txt`](../notes/droplets/gate2/L2_route2_wolfram.out.txt) | 1.7 kB | Gate 2 checker script or output: L2_route2_wolfram.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_zconv.cjs`](../notes/droplets/gate2/L2_zconv.cjs) | 416 B | Gate 2 checker script or output: L2_zconv.cjs. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_zconv.out.txt`](../notes/droplets/gate2/L2_zconv.out.txt) | 294 B | Gate 2 checker script or output: L2_zconv.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_zconv.py`](../notes/droplets/gate2/L2_zconv.py) | 768 B | Gate 2 checker script or output: L2_zconv.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L2_zconv_py.out.txt`](../notes/droplets/gate2/L2_zconv_py.out.txt) | 664 B | Gate 2 checker script or output: L2_zconv_py.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L3_diameter_variant.cjs`](../notes/droplets/gate2/L3_diameter_variant.cjs) | 411 B | Gate 2 checker script or output: L3_diameter_variant.cjs. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L3_diameter_variant.out.txt`](../notes/droplets/gate2/L3_diameter_variant.out.txt) | 86 B | Gate 2 checker script or output: L3_diameter_variant.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L3_model_dump.cjs`](../notes/droplets/gate2/L3_model_dump.cjs) | 535 B | Gate 2 checker script or output: L3_model_dump.cjs. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L3_model_dump.json`](../notes/droplets/gate2/L3_model_dump.json) | 1.0 kB | Gate 2 checker script or output: L3_model_dump.json. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L3_route1_sympy.out.txt`](../notes/droplets/gate2/L3_route1_sympy.out.txt) | 1.9 kB | Gate 2 checker script or output: L3_route1_sympy.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L3_route1_sympy.py`](../notes/droplets/gate2/L3_route1_sympy.py) | 3.7 kB | Gate 2 checker script or output: L3_route1_sympy.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L3_route2.wl`](../notes/droplets/gate2/L3_route2.wl) | 1.3 kB | Gate 2 checker script or output: L3_route2.wl. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L3_route2_numeric.out.txt`](../notes/droplets/gate2/L3_route2_numeric.out.txt) | 2.4 kB | Gate 2 checker script or output: L3_route2_numeric.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L3_route2_numeric.py`](../notes/droplets/gate2/L3_route2_numeric.py) | 2.9 kB | Gate 2 checker script or output: L3_route2_numeric.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L3_route2_wolfram.out.txt`](../notes/droplets/gate2/L3_route2_wolfram.out.txt) | 587 B | Gate 2 checker script or output: L3_route2_wolfram.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L4_golovin_dump.cjs`](../notes/droplets/gate2/L4_golovin_dump.cjs) | 809 B | Gate 2 checker script or output: L4_golovin_dump.cjs. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L4_golovin_dump.json`](../notes/droplets/gate2/L4_golovin_dump.json) | 2.2 kB | Gate 2 checker script or output: L4_golovin_dump.json. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L4_lognormal.out.txt`](../notes/droplets/gate2/L4_lognormal.out.txt) | 824 B | Gate 2 checker script or output: L4_lognormal.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L4_lognormal.py`](../notes/droplets/gate2/L4_lognormal.py) | 2.0 kB | Gate 2 checker script or output: L4_lognormal.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L4_route1_sympy.out.txt`](../notes/droplets/gate2/L4_route1_sympy.out.txt) | 3.5 kB | Gate 2 checker script or output: L4_route1_sympy.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L4_route1_sympy.py`](../notes/droplets/gate2/L4_route1_sympy.py) | 6.8 kB | Gate 2 checker script or output: L4_route1_sympy.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L4_route2.wl`](../notes/droplets/gate2/L4_route2.wl) | 1.9 kB | Gate 2 checker script or output: L4_route2.wl. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L4_route2_numeric.out.txt`](../notes/droplets/gate2/L4_route2_numeric.out.txt) | 3.6 kB | Gate 2 checker script or output: L4_route2_numeric.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L4_route2_numeric.py`](../notes/droplets/gate2/L4_route2_numeric.py) | 4.9 kB | Gate 2 checker script or output: L4_route2_numeric.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L4_route2_wolfram.out.txt`](../notes/droplets/gate2/L4_route2_wolfram.out.txt) | 826 B | Gate 2 checker script or output: L4_route2_wolfram.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L5_route1_sympy.out.txt`](../notes/droplets/gate2/L5_route1_sympy.out.txt) | 2.6 kB | Gate 2 checker script or output: L5_route1_sympy.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L5_route1_sympy.py`](../notes/droplets/gate2/L5_route1_sympy.py) | 4.3 kB | Gate 2 checker script or output: L5_route1_sympy.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L5_route2.wl`](../notes/droplets/gate2/L5_route2.wl) | 1.3 kB | Gate 2 checker script or output: L5_route2.wl. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L5_route2_numeric.out.txt`](../notes/droplets/gate2/L5_route2_numeric.out.txt) | 5.2 kB | Gate 2 checker script or output: L5_route2_numeric.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L5_route2_numeric.py`](../notes/droplets/gate2/L5_route2_numeric.py) | 10.2 kB | Gate 2 checker script or output: L5_route2_numeric.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L5_route2_wolfram.out.txt`](../notes/droplets/gate2/L5_route2_wolfram.out.txt) | 803 B | Gate 2 checker script or output: L5_route2_wolfram.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L6_model_dump.cjs`](../notes/droplets/gate2/L6_model_dump.cjs) | 1.0 kB | Gate 2 checker script or output: L6_model_dump.cjs. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L6_model_dump.json`](../notes/droplets/gate2/L6_model_dump.json) | 1.3 kB | Gate 2 checker script or output: L6_model_dump.json. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L6_route1_sympy.out.txt`](../notes/droplets/gate2/L6_route1_sympy.out.txt) | 2.2 kB | Gate 2 checker script or output: L6_route1_sympy.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L6_route1_sympy.py`](../notes/droplets/gate2/L6_route1_sympy.py) | 4.3 kB | Gate 2 checker script or output: L6_route1_sympy.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L6_route2.wl`](../notes/droplets/gate2/L6_route2.wl) | 1.1 kB | Gate 2 checker script or output: L6_route2.wl. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L6_route2_numeric.out.txt`](../notes/droplets/gate2/L6_route2_numeric.out.txt) | 3.4 kB | Gate 2 checker script or output: L6_route2_numeric.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L6_route2_numeric.py`](../notes/droplets/gate2/L6_route2_numeric.py) | 4.8 kB | Gate 2 checker script or output: L6_route2_numeric.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L6_route2_wolfram.out.txt`](../notes/droplets/gate2/L6_route2_wolfram.out.txt) | 482 B | Gate 2 checker script or output: L6_route2_wolfram.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L7_route1_sympy.out.txt`](../notes/droplets/gate2/L7_route1_sympy.out.txt) | 3.0 kB | Gate 2 checker script or output: L7_route1_sympy.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L7_route1_sympy.py`](../notes/droplets/gate2/L7_route1_sympy.py) | 5.4 kB | Gate 2 checker script or output: L7_route1_sympy.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L7_route2.wl`](../notes/droplets/gate2/L7_route2.wl) | 1.3 kB | Gate 2 checker script or output: L7_route2.wl. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L7_route2_numeric.out.txt`](../notes/droplets/gate2/L7_route2_numeric.out.txt) | 3.0 kB | Gate 2 checker script or output: L7_route2_numeric.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L7_route2_numeric.py`](../notes/droplets/gate2/L7_route2_numeric.py) | 5.8 kB | Gate 2 checker script or output: L7_route2_numeric.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/L7_route2_wolfram.out.txt`](../notes/droplets/gate2/L7_route2_wolfram.out.txt) | 502 B | Gate 2 checker script or output: L7_route2_wolfram.out.txt. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate2/dims.py`](../notes/droplets/gate2/dims.py) | 1.1 kB | Gate 2 checker script or output: dims.py. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/gate3-answers-r1.md`](../notes/droplets/gate3-answers-r1.md) | 3.3 kB | Answers to the Gate 3 skeptic, round 1. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/skeptic-G1-L0-r1.md`](../notes/droplets/skeptic-G1-L0-r1.md) | 15.3 kB | Blind skeptic report, gate 1, level L0, round 1. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/skeptic-G1-L0-r2.md`](../notes/droplets/skeptic-G1-L0-r2.md) | 19.4 kB | Blind skeptic report, gate 1, level L0, round 2. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/skeptic-G1-L0-r3.md`](../notes/droplets/skeptic-G1-L0-r3.md) | 15.4 kB | Blind skeptic report, gate 1, level L0, round 3. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/skeptic-G1-L1-r1.md`](../notes/droplets/skeptic-G1-L1-r1.md) | 17.3 kB | Blind skeptic report, gate 1, level L1, round 1. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/skeptic-G1-L1-r2.md`](../notes/droplets/skeptic-G1-L1-r2.md) | 19.3 kB | Blind skeptic report, gate 1, level L1, round 2. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/skeptic-G1-L1-r3.md`](../notes/droplets/skeptic-G1-L1-r3.md) | 17.2 kB | Blind skeptic report, gate 1, level L1, round 3. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/skeptic-G1-L2-r1.md`](../notes/droplets/skeptic-G1-L2-r1.md) | 18.2 kB | Blind skeptic report, gate 1, level L2, round 1. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/skeptic-G1-L2-r2.md`](../notes/droplets/skeptic-G1-L2-r2.md) | 17.5 kB | Blind skeptic report, gate 1, level L2, round 2. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/skeptic-G1-L3L6L7-r1.md`](../notes/droplets/skeptic-G1-L3L6L7-r1.md) | 29.2 kB | Blind skeptic report, gate 1, level L3L6L7, round 1. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/skeptic-G1-L4L5-r1.md`](../notes/droplets/skeptic-G1-L4L5-r1.md) | 21.5 kB | Blind skeptic report, gate 1, level L4L5, round 1. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/skeptic-G3-r1.md`](../notes/droplets/skeptic-G3-r1.md) | 25.8 kB | Blind skeptic report, gate 3: r1. | [status.md](../notes/droplets/status.md) |
| [`notes/droplets/status.md`](../notes/droplets/status.md) | 10.8 kB | Status of the Droplet Collection study: Fermi estimate, queue, done list with evidence, decisions for Numa. Read first. | [status.md](../notes/droplets/status.md) |

## Record of the lecture-note review

| File | Size | What it is | Explained in |
|---|---|---|---|
| [`notes/.gitignore`](../notes/.gitignore) | 118 B | Keeps the review's screenshots out of the repository. | [notes.md](notes.md) |
| [`notes/STANDARD.md`](../notes/STANDARD.md) | 8.6 kB | The standard the lecture notes are judged against, and Numa's verdicts. | [notes.md](notes.md) |
| [`notes/STATUS.md`](../notes/STATUS.md) | 2.3 kB | Status of the lecture-note review, one row per figure. | [notes.md](notes.md) |
| [`notes/fig01/check-out.txt`](../notes/fig01/check-out.txt) | 2.2 kB | Fig. 1: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig01/check.md`](../notes/fig01/check.md) | 23.9 kB | Fig. 1: the derivation checker's table of equations and numbers. | [notes.md](notes.md) |
| [`notes/fig01/check.py`](../notes/fig01/check.py) | 6.3 kB | Fig. 1: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig01/measure-out.json`](../notes/fig01/measure-out.json) | 2.1 kB | Fig. 1: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig01/measure.cjs`](../notes/fig01/measure.cjs) | 7.5 kB | Fig. 1: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig01/plan.md`](../notes/fig01/plan.md) | 7.0 kB | Fig. 1: the teacher's verdict on each section of the note, and what it changed. | [notes.md](notes.md) |
| [`notes/fig01/referee.md`](../notes/fig01/referee.md) | 15.7 kB | Fig. 1: the blind referee's report on the note. | [notes.md](notes.md) |
| [`notes/fig01/render-check.cjs`](../notes/fig01/render-check.cjs) | 4.2 kB | Fig. 1: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig01/serve.cjs`](../notes/fig01/serve.cjs) | 1.0 kB | Fig. 1: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig01/walk.md`](../notes/fig01/walk.md) | 24.7 kB | Fig. 1: the walkthrough check and its proposed fixes. | [notes.md](notes.md) |
| [`notes/fig02/check-round2.md`](../notes/fig02/check-round2.md) | 21.4 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/check.md`](../notes/fig02/check.md) | 21.5 kB | Fig. 2: the derivation checker's table of equations and numbers. | [notes.md](notes.md) |
| [`notes/fig02/chromium.cjs`](../notes/fig02/chromium.cjs) | 7.6 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/derive.py`](../notes/fig02/derive.py) | 3.6 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/eq9_check.py`](../notes/fig02/eq9_check.py) | 1.2 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/fig3_svg_points.json`](../notes/fig02/fig3_svg_points.json) | 12.5 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/fit.cjs`](../notes/fig02/fit.cjs) | 2.4 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/lyap_long.cjs`](../notes/fig02/lyap_long.cjs) | 2.3 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/measure-out.json`](../notes/fig02/measure-out.json) | 2.6 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/measure.cjs`](../notes/fig02/measure.cjs) | 7.2 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/measure2.cjs`](../notes/fig02/measure2.cjs) | 4.1 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/measure3.cjs`](../notes/fig02/measure3.cjs) | 3.6 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/modes.cjs`](../notes/fig02/modes.cjs) | 1.6 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/overflow.cjs`](../notes/fig02/overflow.cjs) | 1.2 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/plan.md`](../notes/fig02/plan.md) | 6.7 kB | Fig. 2: the teacher's verdict on each section of the note, and what it changed. | [notes.md](notes.md) |
| [`notes/fig02/referee-round2.md`](../notes/fig02/referee-round2.md) | 27.4 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig02/referee.md`](../notes/fig02/referee.md) | 14.4 kB | Fig. 2: the blind referee's report on the note. | [notes.md](notes.md) |
| [`notes/fig02/walk.md`](../notes/fig02/walk.md) | 19.4 kB | Fig. 2: the walkthrough check and its proposed fixes. | [notes.md](notes.md) |
| [`notes/fig02/where.cjs`](../notes/fig02/where.cjs) | 3.1 kB | Fig. 2: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig03/check.cjs`](../notes/fig03/check.cjs) | 5.4 kB | Fig. 3: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig03/check.md`](../notes/fig03/check.md) | 23.4 kB | Fig. 3: the derivation checker's table of equations and numbers. | [notes.md](notes.md) |
| [`notes/fig03/measure-out.json`](../notes/fig03/measure-out.json) | 6.9 kB | Fig. 3: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig03/measure.cjs`](../notes/fig03/measure.cjs) | 8.6 kB | Fig. 3: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig03/plan.md`](../notes/fig03/plan.md) | 8.8 kB | Fig. 3: the teacher's verdict on each section of the note, and what it changed. | [notes.md](notes.md) |
| [`notes/fig03/referee.md`](../notes/fig03/referee.md) | 11.8 kB | Fig. 3: the blind referee's report on the note. | [notes.md](notes.md) |
| [`notes/fig03/walk.md`](../notes/fig03/walk.md) | 15.7 kB | Fig. 3: the walkthrough check and its proposed fixes. | [notes.md](notes.md) |
| [`notes/fig04/check.md`](../notes/fig04/check.md) | 20.1 kB | Fig. 4: the derivation checker's table of equations and numbers. | [notes.md](notes.md) |
| [`notes/fig04/derive.py`](../notes/fig04/derive.py) | 2.3 kB | Fig. 4: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig04/measure-out.json`](../notes/fig04/measure-out.json) | 2.7 kB | Fig. 4: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig04/measure.cjs`](../notes/fig04/measure.cjs) | 12.0 kB | Fig. 4: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig04/plan.md`](../notes/fig04/plan.md) | 5.8 kB | Fig. 4: the teacher's verdict on each section of the note, and what it changed. | [notes.md](notes.md) |
| [`notes/fig04/referee.md`](../notes/fig04/referee.md) | 16.6 kB | Fig. 4: the blind referee's report on the note. | [notes.md](notes.md) |
| [`notes/fig04/verify.cjs`](../notes/fig04/verify.cjs) | 4.8 kB | Fig. 4: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig04/walk.md`](../notes/fig04/walk.md) | 11.3 kB | Fig. 4: the walkthrough check and its proposed fixes. | [notes.md](notes.md) |
| [`notes/fig05/check.md`](../notes/fig05/check.md) | 25.0 kB | Fig. 5: the derivation checker's table of equations and numbers. | [notes.md](notes.md) |
| [`notes/fig05/derive.py`](../notes/fig05/derive.py) | 4.3 kB | Fig. 5: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig05/fig4_rk4.py`](../notes/fig05/fig4_rk4.py) | 2.0 kB | Fig. 5: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig05/measure-after.json`](../notes/fig05/measure-after.json) | 5.7 kB | Fig. 5: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig05/measure-before.json`](../notes/fig05/measure-before.json) | 4.7 kB | Fig. 5: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig05/measure.cjs`](../notes/fig05/measure.cjs) | 5.9 kB | Fig. 5: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig05/plan.md`](../notes/fig05/plan.md) | 6.3 kB | Fig. 5: the teacher's verdict on each section of the note, and what it changed. | [notes.md](notes.md) |
| [`notes/fig05/referee.md`](../notes/fig05/referee.md) | 14.6 kB | Fig. 5: the blind referee's report on the note. | [notes.md](notes.md) |
| [`notes/fig05/walk.md`](../notes/fig05/walk.md) | 17.7 kB | Fig. 5: the walkthrough check and its proposed fixes. | [notes.md](notes.md) |
| [`notes/fig06/check.md`](../notes/fig06/check.md) | 22.0 kB | Fig. 6: the derivation checker's table of equations and numbers. | [notes.md](notes.md) |
| [`notes/fig06/check.py`](../notes/fig06/check.py) | 3.9 kB | Fig. 6: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig06/measure-after.json`](../notes/fig06/measure-after.json) | 4.8 kB | Fig. 6: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig06/measure-before.json`](../notes/fig06/measure-before.json) | 4.1 kB | Fig. 6: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig06/measure.cjs`](../notes/fig06/measure.cjs) | 6.8 kB | Fig. 6: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig06/plan.md`](../notes/fig06/plan.md) | 7.4 kB | Fig. 6: the teacher's verdict on each section of the note, and what it changed. | [notes.md](notes.md) |
| [`notes/fig06/referee.md`](../notes/fig06/referee.md) | 13.9 kB | Fig. 6: the blind referee's report on the note. | [notes.md](notes.md) |
| [`notes/fig06/serve.cjs`](../notes/fig06/serve.cjs) | 1.0 kB | Fig. 6: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig06/walk.md`](../notes/fig06/walk.md) | 11.4 kB | Fig. 6: the walkthrough check and its proposed fixes. | [notes.md](notes.md) |
| [`notes/fig07/angle_rounding.py`](../notes/fig07/angle_rounding.py) | 736 B | Fig. 7: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig07/check-after.json`](../notes/fig07/check-after.json) | 3.0 kB | Fig. 7: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig07/check-baseline.json`](../notes/fig07/check-baseline.json) | 2.3 kB | Fig. 7: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig07/check.cjs`](../notes/fig07/check.cjs) | 3.8 kB | Fig. 7: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig07/check.md`](../notes/fig07/check.md) | 27.0 kB | Fig. 7: the derivation checker's table of equations and numbers. | [notes.md](notes.md) |
| [`notes/fig07/numbers.cjs`](../notes/fig07/numbers.cjs) | 2.5 kB | Fig. 7: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig07/plan.md`](../notes/fig07/plan.md) | 6.4 kB | Fig. 7: the teacher's verdict on each section of the note, and what it changed. | [notes.md](notes.md) |
| [`notes/fig07/record_rate.cjs`](../notes/fig07/record_rate.cjs) | 1.2 kB | Fig. 7: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig07/referee.md`](../notes/fig07/referee.md) | 15.9 kB | Fig. 7: the blind referee's report on the note. | [notes.md](notes.md) |
| [`notes/fig07/serve.cjs`](../notes/fig07/serve.cjs) | 1.1 kB | Fig. 7: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig07/shots.cjs`](../notes/fig07/shots.cjs) | 1.8 kB | Fig. 7: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig07/walk.md`](../notes/fig07/walk.md) | 11.7 kB | Fig. 7: the walkthrough check and its proposed fixes. | [notes.md](notes.md) |
| [`notes/fig08/analyse-out.json`](../notes/fig08/analyse-out.json) | 11.8 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/analyse.cjs`](../notes/fig08/analyse.cjs) | 3.9 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/analyse2-out.json`](../notes/fig08/analyse2-out.json) | 539 B | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/analyse2.cjs`](../notes/fig08/analyse2.cjs) | 1.5 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/check.md`](../notes/fig08/check.md) | 27.9 kB | Fig. 8: the derivation checker's table of equations and numbers. | [notes.md](notes.md) |
| [`notes/fig08/eight_exact.cjs`](../notes/fig08/eight_exact.cjs) | 1.3 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/measure-out.json`](../notes/fig08/measure-out.json) | 1.9 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/measure.cjs`](../notes/fig08/measure.cjs) | 5.8 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/overshoot-out.json`](../notes/fig08/overshoot-out.json) | 2.1 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/overshoot.cjs`](../notes/fig08/overshoot.cjs) | 2.1 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/pagecode.cjs`](../notes/fig08/pagecode.cjs) | 3.0 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/plan.md`](../notes/fig08/plan.md) | 7.1 kB | Fig. 8: the teacher's verdict on each section of the note, and what it changed. | [notes.md](notes.md) |
| [`notes/fig08/referee.md`](../notes/fig08/referee.md) | 12.8 kB | Fig. 8: the blind referee's report on the note. | [notes.md](notes.md) |
| [`notes/fig08/shots.cjs`](../notes/fig08/shots.cjs) | 2.1 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/timing.cjs`](../notes/fig08/timing.cjs) | 1.7 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/verify.cjs`](../notes/fig08/verify.cjs) | 5.0 kB | Fig. 8: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig08/walk.md`](../notes/fig08/walk.md) | 16.5 kB | Fig. 8: the walkthrough check and its proposed fixes. | [notes.md](notes.md) |
| [`notes/fig09/check.md`](../notes/fig09/check.md) | 22.1 kB | Fig. 9: the derivation checker's table of equations and numbers. | [notes.md](notes.md) |
| [`notes/fig09/derive.py`](../notes/fig09/derive.py) | 3.2 kB | Fig. 9: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig09/measure-before.json`](../notes/fig09/measure-before.json) | 4.7 kB | Fig. 9: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig09/measure-out.json`](../notes/fig09/measure-out.json) | 5.5 kB | Fig. 9: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig09/measure.cjs`](../notes/fig09/measure.cjs) | 7.2 kB | Fig. 9: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig09/physics.cjs`](../notes/fig09/physics.cjs) | 5.3 kB | Fig. 9: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig09/plan.md`](../notes/fig09/plan.md) | 9.1 kB | Fig. 9: the teacher's verdict on each section of the note, and what it changed. | [notes.md](notes.md) |
| [`notes/fig09/referee.md`](../notes/fig09/referee.md) | 13.2 kB | Fig. 9: the blind referee's report on the note. | [notes.md](notes.md) |
| [`notes/fig09/shift_doc_links.py`](../notes/fig09/shift_doc_links.py) | 1.3 kB | Fig. 9: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig09/tick_overlap.cjs`](../notes/fig09/tick_overlap.cjs) | 2.3 kB | Fig. 9: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig09/walk.md`](../notes/fig09/walk.md) | 16.1 kB | Fig. 9: the walkthrough check and its proposed fixes. | [notes.md](notes.md) |
| [`notes/fig10/check.md`](../notes/fig10/check.md) | 25.4 kB | Fig. 10: the derivation checker's table of equations and numbers. | [notes.md](notes.md) |
| [`notes/fig10/cp_checks.cjs`](../notes/fig10/cp_checks.cjs) | 3.7 kB | Fig. 10: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig10/measure-out.json`](../notes/fig10/measure-out.json) | 9.5 kB | Fig. 10: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig10/measure.cjs`](../notes/fig10/measure.cjs) | 5.7 kB | Fig. 10: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig10/plan.md`](../notes/fig10/plan.md) | 6.0 kB | Fig. 10: the teacher's verdict on each section of the note, and what it changed. | [notes.md](notes.md) |
| [`notes/fig10/referee.md`](../notes/fig10/referee.md) | 14.9 kB | Fig. 10: the blind referee's report on the note. | [notes.md](notes.md) |
| [`notes/fig10/verify-out.json`](../notes/fig10/verify-out.json) | 855 B | Fig. 10: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig10/verify.cjs`](../notes/fig10/verify.cjs) | 4.9 kB | Fig. 10: a measuring script of the review, or its saved output. | [notes.md](notes.md) |
| [`notes/fig10/walk.md`](../notes/fig10/walk.md) | 14.7 kB | Fig. 10: the walkthrough check and its proposed fixes. | [notes.md](notes.md) |
| [`notes/verify.mjs`](../notes/verify.mjs) | 4.5 kB | Checks the ten simulation pages in headless Chromium at desktop and phone size. | [notes.md](notes.md) |
| [`notes/walkcheck.cjs`](../notes/walkcheck.cjs) | 1.7 kB | Searches every quoted code line of the ten walkthroughs in its page. | [notes.md](notes.md) |
