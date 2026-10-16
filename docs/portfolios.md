# The two research projects: `public/portfolios/`

The Portfolios page ([`public/portfolios.html`](../public/portfolios.html), described in [pages.md](pages.md)) presents two
long research projects. Each one is its own AppDeploy app with its own source. This website carries only a **built copy** of
each one, so that a reader can open it here without leaving the site:

| Folder | Built from the app | What it is |
|---|---|---|
| [`public/portfolios/droplet-collection/`](../public/portfolios/droplet-collection/) | `droplet-collection-yl7l26` | Numa's Bachelor thesis (Leipzig) on how cloud droplets grow into rain by gravitational collection, remodelled: derivations, a solver of the stochastic collection equation that runs in the browser, results and checks. |
| [`public/portfolios/rotor-pendula/`](../public/portfolios/rotor-pendula/) | `rotor-pendula-gafw0f` | Sol's corrected study of a pendulum riding on a wind-turbine blade, built as a sensor power supply: derivation from the Lagrangian, an in-browser solver, results, checks, and a Report page whose tables are rebuilt from the study's data. |

**The source code of these two apps is not in this repository.** It lives in their AppDeploy apps (readable there with
`src_read`). What is here is the output of their build (`vite build`): one HTML file, one JavaScript bundle, one stylesheet,
one Web Worker, the KaTeX fonts, and the figures and files they link to. Minified bundles are not meant to be read or edited
by hand: to change a project, change its app, rebuild, and copy the build here again (the procedure is at the end of this page).

## How a copy works

Picture a sealed parcel: everything the project needs is inside its folder, and it touches the rest of the site in only two
places, the links into it from `portfolios.html` and its one link back out.

1. **One page, many views.** Each copy is a single-page application written in React. The browser loads
   `index.html`, which loads one JavaScript module (`static/index-<hash>.js`). That module draws every view of the project into
   `<div id="root">`. The view to show is chosen by the part of the address after `#`, the **hash route**:
   - Droplet Collection: `#/` (Overview), `#/theory`, `#/results`, `#/simulate`, `#/checks`;
   - Rotor Pendula: `#/` (Overview), `#/theory`, `#/results`, `#/simulate`, `#/checks`, `#/report`.

   (Found with `grep -o 'path:"/[a-z-]*"' public/portfolios/*/static/index-*.js`.) Hash routes are used because the server
   only ever serves the one file `index.html`; everything after `#` stays in the browser. Links from `portfolios.html` therefore
   always name the file, as in `portfolios/rotor-pendula/index.html#/report`
   ([portfolios.html:190](../public/portfolios.html#L190)). A link to the bare folder `portfolios/rotor-pendula/` would fail:
   the AppDeploy server answers folder addresses with 403 (forbidden).
2. **The solver runs off the main thread.** Each bundle starts a Web Worker (`static/worker-<hash>.js`). This is a second
   JavaScript thread that integrates the equations while the page stays responsive, like a second person doing the arithmetic
   while the first keeps talking. Droplet Collection's worker (130 kB) carries the collection-equation solver; Rotor Pendula's
   (4.5 kB) carries the pendulum integrator.
3. **The stylesheet is added by a script.** In both `index.html` files the stylesheet is not a `<link>` tag but a one-line
   script that creates the `<link>` when the page runs
   ([droplet-collection/index.html:12](../public/portfolios/droplet-collection/index.html#L12),
   [rotor-pendula/index.html:12](../public/portfolios/rotor-pendula/index.html#L12)). The reason is a platform quirk:
   when AppDeploy deploys an HTML file, it rewrites a relative stylesheet address such as `./static/index-<hash>.css` into an
   address at the site root, where the file does not exist (403), and the copy shows unstyled. The platform does not touch
   scripts, so a script that adds the same link at run time survives. Seen for `./assets/…` and, since October 2026, for
   `./static/…`.
4. **The build folder is `static/`, not Vite's default `assets/`.** All file names inside carry a content hash
   (`index-CsGEKbO8.js`): a new build gives new names, so a browser never mixes an old cached file with a new page.
5. **The way back.** Each bundle contains one link to `../../portfolios.html`, the Portfolios page of this site.
6. **No backend.** The copies are built without the apps' saved runs or server functions: the Saved runs page and the Save
   button are removed, and the Simulate page says that saving belongs to the standalone app. Everything a copy shows is
   computed in the browser or read from the files beside it.

## Files in each copy

### `droplet-collection/` (69 files)

| Path | What it is |
|---|---|
| `index.html` | The entry page: title, description, the module script, the stylesheet loader. |
| `static/index-DGIxitSc.js` | The whole application (React, KaTeX 0.16.47, the pages Overview, Theory, Results, Simulate, Checks), minified, 841 kB. |
| `static/index-CGriahzx.css` | Its stylesheet (the house design and the KaTeX styles), 61 kB. |
| `static/worker-ClooJ8Gk.js` | The Web Worker: the solver of the stochastic collection equation, 131 kB. |
| `static/KaTeX_*.{woff2,woff,ttf}` | 59 font files of KaTeX, the maths typesetter, each in up to three formats (the bundle names them; the browser picks the first format it supports, in practice woff2). |
| `fig/c1_ice.svg`, `fig/ecoll_map.svg`, `fig/fallspeed_gk.svg`, `fig/golovin.svg`, `fig/w2_rain.svg`, `fig/w2_spectra.svg` | Vector figures of the project. Four of them also appear as plates on the Portfolios page ([portfolios.html:128–140](../public/portfolios.html#L128-L140)). |

### `rotor-pendula/` (84 files)

| Path | What it is |
|---|---|
| `index.html` | The entry page. |
| `static/index-CsGEKbO8.js` | The whole application, including the Report page, minified, 1.01 MB. |
| `static/index-CNYGhWdg.css` | Its stylesheet, 65 kB. |
| `static/worker-hcWKavQc.js` | The Web Worker: the pendulum integrator, 4.5 kB. |
| `static/KaTeX_*` | The same 59 KaTeX font files. |
| `fig/01_geometry.svg` … `fig/07_sensor_range.svg` | Seven vector figures of the study (geometry, power at the 18 mountings, generator topologies, geometry ratios, chaos scan, Poincaré sections, sensor range). |
| `study/` | Sol's delivered study, offered for download on the Report page; listed below. |

**`rotor-pendula/study/`** is the study as Sol delivered it, after correction:

| Path | What it is |
|---|---|
| `study/report.pdf` | The 14-page corrected report (XeLaTeX), 202 kB. |
| `study/report.tex` | Its LaTeX source. |
| `study/wind_pendulum.zip` | The complete delivery, 1.4 MB, 189 entries: code, data (111 nonlinear run metadata files, 49 linear evaluations), figures, fonts, sources, the report. Byte-identical to the file the live app serves. |
| `study/README.md` | Where to start: the report, then `code/README.md`. |
| `study/STATUS.md` | What was computed, what was derived, what was *not* measured (five legacy cases), and the stated model limits. |
| `study/CHANGES.md` | The fourteen corrections C1–C14 to the first delivery, each with old → new values (for example the rotor radius 0.7 m → 5.347606 m). |
| `study/FILE_INVENTORY.csv` | Every file of the full delivery with its size in bytes (181 rows). |
| `study/code/README.md` | Exact regeneration: Python 3.12 with numpy, scipy, matplotlib, fontTools; the commands in order, from `anchors.py` to `package.py`. |
| `study/code/requirements.txt` | The four pinned packages. |
| `study/data/summary.csv` | One row per computed case (study, rotor speed Ω in rad/s, pivot radius in m, masses in kg, damping c in N m s/rad, mean power in W, Lyapunov exponent in 1/s, regime, dimensionless groups …). The Report page's tables are rebuilt from this and the next two files. |
| `study/data/all_results.json` | The same 160 cases with their full parameters. |
| `study/data/audit.json` | The audit numbers: RK4 cross-checks, the C12 topology values, similarity checks, the energy identity, the sensor budget, the unmeasured legacy cases, the historical turbine correction. |
| `study/sources/README.md` | The two datasheets used for the sensor budget (ADXL362 accelerometer, CC2652R radio chip): addresses, SHA-256 checksums, the pages and values used, and the assumed duty cycle. The PDFs themselves are not included. |
| `study/sources/access.json` | The same two sources as data: address, bytes, SHA-256, access date, HTTP status. |

## How to update a copy

1. Change the project in its own app (`droplet-collection-yl7l26` or `rotor-pendula-gafw0f`) and check it there.
2. Make a website variant of its source, outside the app: remove the Saved runs page, its route and link, and the Save
   button with its server call; add the back link `← Numa Koudsie · Portfolios` to `../../portfolios.html` in the top bar;
   add ` · Numa Koudsie` to the page title. Build that variant with a separate Vite configuration that sets `base: './'` and
   `build.assetsDir: 'static'` (the apps' own `vite.config.ts` keeps Vite's default `assets/`). The repeatable helper is [tools/make_portfolio_copy.py](../tools/make_portfolio_copy.py):

   ~~~bash
   python3 tools/make_portfolio_copy.py /absolute/app-source /absolute/new-workdir
   ~~~

   The source must have its existing dependencies available. The helper makes an isolated source copy, removes the saved-run route and controls, retains solver error messages, adds the backlink and title suffix, builds with a separate Vite configuration and patches the stylesheet loader. It installs nothing. The output is `new-workdir/dist/`; the standalone app is not edited.
   Build with the KaTeX version the deployed app uses (0.16.47 today; it is the `content` of the `.katex-version` rule in the
   app's served CSS). The apps have no lockfile, so a fresh `node_modules` can bring a different KaTeX, which changes the
   hidden MathML that screen readers use and the spacing of multi-line equations while the visible maths looks the same
   (seen on 15 October 2026 with 0.16.11).
3. Replace the folder here with the new build output (delete the old `static/` first, because the hashed names change).
4. The helper has already replaced the stylesheet `<link>` of `dist/index.html` with the loader script. If you built
   without it, replace the line `<link rel="stylesheet" crossorigin href="./static/index-<hash>.css">` with the one-line
   loader script used now, with the new hash:
   `<script>(function(){var l=document.createElement('link');l.rel='stylesheet';l.href='./static/index-<hash>.css';document.head.appendChild(l)})();</script>`
5. Keep the links in `public/portfolios.html` pointing at `index.html#/…`, never at a folder.
6. Deploy the website and open every route of the copy on the live site: the page must be styled (the stylesheet loaded
   with status 200), and the maths typeset.

## Notes for maintainers

- The KaTeX fonts are shipped three times on this site: once in `public/vendor/katex/fonts/` (20 woff2 files, 0.26 MB, for
  the simulation pages) and once inside each copy's `static/` (59 files in woff2, woff and ttf; 2.1 MB for the two copies
  together, measured with `du -cb public/portfolios/*/static/KaTeX_*`). They are kept because each copy must work as a sealed
  parcel; sharing them would tie the copies to this site's folder layout.


## Theory readability revision · 15 October 2026

Both project apps were revised and verified before these copies were rebuilt. Droplet Collection now separates swept volume, event rate, population change and diagnostics, and corrects the interpretation of its L1 spectrum error. Rotor Pendula explains torque signs, moving-pivot kinetic energy, conservative gravity work, weak forcing versus small angle, and the range of the damping optimum. Its Report page identifies the added explanatory prose; the downloadable PDF, source and ZIP remain the original study record.

The two worker bundles retain their previous names and bytes: neither numerical solver nor stored data changed. Both native apps and both website copies passed desktop and phone reading checks, including chapter jumps, keyboard disclosures, retained typeset maths and simulation presets. The complete review is [research-theory-audit.md](research-theory-audit.md).


## Rebuilt on KaTeX 0.16.47 · 16 October 2026

The copies above were rebuilt from the apps after the repairs of the independent audit
([research-theory-audit.md](research-theory-audit.md), second part), with the KaTeX version of the native apps, 0.16.47,
instead of the 0.16.11 of the 15 October build. The worker bundles, the figures and the study files are unchanged, and the
stylesheets came back with their earlier hashes (`index-CGriahzx.css`, `index-CNYGhWdg.css`): only the application bundles
changed. They were rebuilt once more the same day, after the second repairs of the wording (`index-DGIxitSc.js`, `index-CsGEKbO8.js`).
