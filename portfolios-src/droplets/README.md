# Droplet Collection: the source

Lecture notes and simulations on how cloud droplets become rain, rebuilt from Numa Koudsie's Bachelor thesis, *Collisional Ice
Multiplication Processes in Clouds* (Leipzig, 2022). This folder is the only source. The build script writes the page the site
serves: [`public/portfolios/droplet-collection/index.html`](../../public/portfolios/droplet-collection/index.html), one
self-contained HTML file. The record of how each model level was argued, attacked and checked is in
[`notes/droplets/`](../../notes/droplets/).

## Layout

| Path | What it is |
|---|---|
| `physics.cjs` | The model: air, fall speeds (Stokes, Beard 1976), droplet trajectories and collision efficiencies, coalescence, the kernel, the collection equation (two-bin scheme), the thesis's bookkeeping (GCE), Golovin's exact solution, the exact stochastic process (Gillespie with class majorants), the turbulence factor (Ayala et al. 2008), the energy ledger, maximum-entropy comparison and vapour ripening (L8), and a cloud with a shape: super-droplets moved by the fall speed, an overturning cell and a stochastic element (L10). The code between `/*PHYSICS-BEGIN*/` and `/*PHYSICS-END*/` runs in the page and in Node. |
| `chart.cjs` | House-style SVG line charts (between `CHART-BEGIN` and `CHART-END`), used by the figures and by the page. |
| `app.js` | The page's own script: tabs and hash routes (`#sim`, `#book`, `#problems`, `#checks`, and any element id such as `#ch3` or `#fig-5-2`), the five simulation panels. Panels 4 and 3 write every number they compute into one store (the site's `scripts/dataset.js`, `Sim.cloudStore`) at the line that computes it; the readouts beside the cloud read the store. |
| `datahooks.js` | The site's data panel for panels 4 and 3 (`Sim.data` for `scripts/datalog.js`): what lies under a click on the cloud, every value recomputed from stored inputs, read-backs from the picture, the water and drop-number books, one round = five cloud-minutes. Inlined by the build after `app.js`; the served page also loads `sim.js`, `dataset.js`, `datalog.js`, `paper.css` and `data.css` from the site. |
| `template.html` | The page: house design (reading-room CSS), tabs, placeholders the build fills. |
| `text/` | The words: `sim.src.html`, `book-00` … `book-12` (chapters 0–12), `book-99` (appendix A), `problems.src.html`, `checks.src.html`. HTML with TeX maths (`$…$`, `$$…\tag{n}$$`). |
| `data/` | Numbers the model's run tools wrote: `etab_warm.json` (efficiency table, 64 × 40), `etab_split.json` (the same with the two flow limits apart), `hall1980.json` (Hall's table, OCR reading), `warm.json`, `stochastic.json`, `bridge.json`, `cold.json`, `energy.json` (L8, `run_energy.cjs`), `ripening.json` (L8b, `run_ripening.cjs`), `cloud.json` (L10, `run_cloud.cjs CASE …` then `--merge`, about 1.5 h on 4 cores). |
| `tools/` | `build.py` (the build), `figs.cjs` (the 25 figures), `katex_render.cjs` and `package.json` (KaTeX 0.16.11 at build time), and the run tools that write `data/`: `gen_tables.cjs`, `run_warm.cjs`, `run_golovin.cjs`, `run_stochastic.cjs`, `run_bridge.cjs`, `run_cold.cjs`, `run_energy.cjs`, `run_ripening.cjs`, `run_cloud.cjs`, `test_gillespie.cjs`, `tail_resolution.cjs`. |
| `derive/` | Derivations and the numbers behind the Gate 1 contracts (SymPy, Wolfram, Node), level by level. |
| `checks/` | `check_physics.py` (independent Python: constants retyped, SciPy, SymPy), `check_numbers.cjs` (every number quoted in the text, recomputed and found near its anchor), `check_browser.py` (Playwright at 360, 390, 1024, 1440 px), `model_dump.cjs` (helper of `check_physics.py`). |

## Build and check

```sh
cd portfolios-src/droplets
(cd tools && npm ci)                     # KaTeX for build-time typesetting, once
python3 tools/build.py --site            # writes public/portfolios/droplet-collection/index.html and its four plates in fig/
python3 tools/build.py                   # a standalone copy in out/ (not committed)
node checks/check_numbers.cjs            # 235 numbers, about four minutes: NUMBER CHECK PASS
python3 checks/check_physics.py          # 14 checks, about three minutes: PHYSICS CHECK PASS
python3 -m http.server 8771 --directory ../../public &
python3 checks/check_browser.py http://localhost:8771/portfolios/droplet-collection/index.html <screenshot folder>
```

Data files are rewritten only by their run tools (for example `node tools/run_warm.cjs --json`), never by hand. After a change to
the model, rerun the tools whose data it affects, rebuild, and run the three checks.

## Rules this source keeps

- Every number in the text comes from the model or from a data file the model wrote, and `check_numbers.cjs` finds it.
- Nothing on a running figure reacts to the pointer crossing it; the panels change only on a click, a slider release or a button.
- Explanations are lecture notes: an everyday picture first, then the model, then the mathematics, with the model's own numbers.
- Fonts: titles Instrument Serif, text IBM Plex Sans, labels IBM Plex Mono, served from the site's `fonts/`.
