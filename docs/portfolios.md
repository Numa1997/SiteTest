# The four research projects: `public/portfolios/`

The Portfolios page ([`public/portfolios.html`](../public/portfolios.html), described in [pages.md](pages.md)) presents four
research projects; the fourth, Iron, Cotton and the Head, is described [at the end](#iron-cotton-and-the-head-impact). The first two are each their own AppDeploy app with its own source; the third, the Hydraulic Press
Study, is generated from its own GitHub repository ([below](#the-hydraulic-press-study-hydraulics)). This website carries only
a **built copy** of each one, so that a reader can open it here without leaving the site:

| Folder | Built from the app | What it is |
|---|---|---|
| [`public/portfolios/droplet-collection/`](../public/portfolios/droplet-collection/) | `droplet-collection-yl7l26` | Numa's Bachelor thesis (Leipzig) on how cloud droplets grow into rain by gravitational collection, remodelled: derivations, a solver of the stochastic collection equation that runs in the browser, results and checks. |
| [`public/portfolios/rotor-pendula/`](../public/portfolios/rotor-pendula/) | `rotor-pendula-gafw0f` | Sol's corrected study of a pendulum riding on a wind-turbine blade, built as a sensor power supply: derivation from the Lagrangian, an in-browser solver, results, checks, and a Report page whose tables are rebuilt from the study's data. |
| [`public/portfolios/hydraulics/`](../public/portfolios/hydraulics/) | its source in [`portfolios-src/hydraulics/`](../portfolios-src/hydraulics/) (not an app) | A servo-hydraulic press under digital control, from first principles: the animated press with its PID controller, loop analysis (Bode, Nyquist, z-plane), Pascal's ideal press, and a 23-chapter text deriving every equation. One self-contained page. |

**The source code of the first two apps is not in this repository.** It lives in their AppDeploy apps (readable there with
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
   ([portfolios.html:191](../public/portfolios.html#L191)). The AppDeploy server used to answer a bare folder address such as
   `portfolios/rotor-pendula/` with 403 (forbidden). Measured on 20 October 2026, both hosts serve the copy there (AppDeploy
   200; Cloudflare 200, and Cloudflare redirects `…/index.html` to the folder with a 307, the browser keeping the `#/route`), so
   the links that name the file work on both.
2. **The solver runs off the main thread.** Each bundle starts a Web Worker (`static/worker-<hash>.js`). This is a second
   JavaScript thread that integrates the equations while the page stays responsive, like a second person doing the arithmetic
   while the first keeps talking. Droplet Collection's worker (130 kB) carries the collection-equation solver; Rotor Pendula's
   (4.5 kB) carries the pendulum integrator.
3. **The stylesheet is added by a script.** In both `index.html` files the stylesheet is not a `<link>` tag but a one-line
   script that creates the `<link>` when the page runs
   ([droplet-collection/index.html:14](../public/portfolios/droplet-collection/index.html#L14),
   [rotor-pendula/index.html:14](../public/portfolios/rotor-pendula/index.html#L14)). The reason is a platform quirk:
   when AppDeploy deploys an HTML file, it rewrites a relative stylesheet address such as `./static/index-<hash>.css` into an
   address at the site root, where the file does not exist (403), and the copy shows unstyled. The platform does not touch
   scripts, so a script that adds the same link at run time survives. Seen for `./assets/…` and, since October 2026, for
   `./static/…`. Cloudflare serves the files unchanged (measured on 20 October 2026: the copy's `index.html` byte for byte), so
   there the loader is not needed but does no harm.
4. **The build folder is `static/`, not Vite's default `assets/`.** All file names inside carry a content hash
   (`index-CsGEKbO8.js`): a new build gives new names, so a browser never mixes an old cached file with a new page.
5. **The way back.** Each bundle contains one link to `../../portfolios.html`, the Portfolios page of this site.
6. **No backend.** The copies are built without the apps' saved runs or server functions: the Saved runs page and the Save
   button are removed (neither bundle has a `/runs` route or the words "Saved runs"), and Rotor Pendula's Simulate page says
   that saving runs to a shared list is part of the standalone app; Droplet Collection's Simulate page has no such sentence.
   Neither bundle calls a server: no `XMLHttpRequest`, `WebSocket` or AppDeploy client is in them, and the one global
   `fetch` is Vite's module-preload helper, which loads the copy's own `static/` files (the other `fetch(` are KaTeX's
   parser), so a copy works the same on phyeinusul.com and on AppDeploy. What they keep in the browser is
   only the reader's theme and closed folds in `localStorage` (`droplet.theme`, `droplet.closed`, `rotor.theme`,
   `rotor.closed`). Everything a copy shows is computed in the browser or read from the files beside it. (Found with
   `grep -o` on the two `static/index-*.js`; the apps' own source, and so their Saved runs backend, is not in this repository
   and was not checked.)
7. **Fonts and policy from the website.** The stylesheet's first rule imports the fonts from the website's own folder
   (`@import"../../../fonts/instrument-plex.css"`), not from Google Fonts, and `index.html` carries the website's security
   policy and referrer rule on lines 5–6, right after its charset line ([build-and-deploy.md](build-and-deploy.md#security)).
   Both were patched into the built files on 16 October 2026, so the hashes in the two stylesheet names no longer match their
   content; nothing depends on that. On phyeinusul.com the HTTP headers of [`public/_headers`](../public/_headers) also apply to
   the copies (its rule `/*` covers every path; measured on `/portfolios/rotor-pendula/`).

## Files in each copy

### `droplet-collection/` (69 files)

| Path | What it is |
|---|---|
| `index.html` | The entry page: the security policy and referrer rule, title, description, the module script, the stylesheet loader. |
| `static/index-DGIxitSc.js` | The whole application (React, KaTeX 0.16.47, the pages Overview, Theory, Results, Simulate, Checks), minified, 841 kB. |
| `static/index-CGriahzx.css` | Its stylesheet (the house design and the KaTeX styles; fonts imported from `../../../fonts/instrument-plex.css`), 61 kB. |
| `static/worker-ClooJ8Gk.js` | The Web Worker: the solver of the stochastic collection equation, 131 kB. |
| `static/KaTeX_*.{woff2,woff,ttf}` | 59 font files of KaTeX, the maths typesetter, each in up to three formats (the bundle names them; the browser picks the first format it supports, in practice woff2). |
| `fig/c1_ice.svg`, `fig/ecoll_map.svg`, `fig/fallspeed_gk.svg`, `fig/golovin.svg`, `fig/w2_rain.svg`, `fig/w2_spectra.svg` | Vector figures of the project. Four of them also appear as plates on the Portfolios page ([portfolios.html:129–141](../public/portfolios.html#L129-L141)). |

### `rotor-pendula/` (84 files)

| Path | What it is |
|---|---|
| `index.html` | The entry page, as in the other copy. |
| `static/index-CsGEKbO8.js` | The whole application, including the Report page, minified, 1.01 MB. |
| `static/index-CNYGhWdg.css` | Its stylesheet (fonts imported as in the other copy), 65 kB. |
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

## The Hydraulic Press Study: `hydraulics/`

Unlike the other two, this project is not a Vite build of an app. It is one self-contained HTML page, generated from its
source, which lives in this repository in [`portfolios-src/hydraulics/`](../portfolios-src/hydraulics/) (its
[`README.md`](../portfolios-src/hydraulics/README.md) describes it). Vite neither builds nor serves that folder. The study was
written in the repository `Numa1997/Gergi-s-vision` and moved here on 21 October 2026, so that the whole site has one
repository.

**What the reader gets.** A tab bar with three tabs: the servo-hydraulic press (pump, four-way servo valve, two metres of hose,
differential cylinder and specimen under a PID controller sampled every 1 ms, animated, every setting recomputable, with
time traces, Bode, Nyquist and z-plane plots and nine worked solutions), Pascal's ideal press, and *Hydraulics from First
Principles*, a 23-chapter text with 63 numbered equations. `index.html#servo`, `#ideal` and `#theory` open a tab directly;
the Portfolios page links to those three addresses.

**How the page works.** Picture three finished pages packed into one envelope. Each of the three pages is stored inside
`index.html` unchanged, as a JSON string, and shown in its own frame (`<iframe srcdoc>`, with a `blob:` frame as the fallback),
so their styles, element ids and scripts cannot collide. A small script added to each embedded page turns the links between
them into tab switches. Everything is inline: the scripts, the styles, the fonts of the three pages and KaTeX's fonts (as
`data:` addresses; the text's maths is typeset when the page is generated, so no KaTeX runs in the browser). The page loads
nothing but `../../fonts/instrument-plex.css` for its tab bar, and makes no request outside the site.

**Its security policy has two additions.** The page carries the website's policy and referrer rule after its charset line,
taken from the root `index.html`, as every page does. The servo press runs its solver in a Web Worker that it builds from text
at run time, so this one page adds `'unsafe-eval'` to `script-src` (for `new Function`) and `blob:` to `worker-src` (the worker
is started from a `blob:` address). A policy in a `meta` tag governs only the page that carries it, and the frames inherit
it, so no other page of the site is affected. The response headers of [`public/_headers`](../public/_headers) apply as to
every page; `X-Frame-Options: SAMEORIGIN` does not stop the page's own frames, which are same-origin.

**Files.**

| Path | What it is |
|---|---|
| `index.html` | The whole study, 5.09 MB: the tab bar and the three embedded pages. |
| `LICENSE-fonts.txt` | The licences of the fonts embedded in the study (SIL Open Font License 1.1 for IBM Plex and Instrument Serif; MIT for KaTeX's fonts). |
| `fig/01_press.webp` … `fig/04_map.webp` | The four plates of the Portfolios page (part 3.3), screenshots of the study at 600 px height: the press mid-cycle, the six time traces, Bode and Nyquist, and the block map of chapter 0. |

**How to update it.** Change the study in `portfolios-src/hydraulics/`, then, from that folder:

~~~bash
(cd tools && npm ci)                       # KaTeX 0.16.11 for the theory page, once
python3 tools/build_theory.py              # only if theory/*.src.html changed
python3 tools/build_combined.py --site     # writes ../../public/portfolios/hydraulics/index.html and LICENSE-fonts.txt
python3 check_physics.py && python3 check_control.py                          # the physics against independent Python models
node tools/check_theory_numbers.js ../../public/portfolios/hydraulics/index.html   # 52 numbers in the text against the models
~~~

The folder has its own `package.json` only to say `"type": "commonjs"`: the site's root `package.json` declares ES modules,
and the study's Node scripts are CommonJS. Then build this site, serve `dist/` (for example `python3 -m http.server` in it)
and run, from that folder, `python3 tools/check_combined.py http://localhost:<port>/portfolios/hydraulics/index.html` (33 checks in a real browser:
each tab complete, Play and the sliders working, links switching tabs, no script error, nothing scrolling sideways at 360 to
1440 px). `--site` takes the policy from this repository's `index.html`, the tab icon from `portfolios.html` and the fonts from
`public/fonts/instrument-plex.css`, so a change to those reaches the study on its next generation. The plates are not
regenerated automatically; retake them when the pictures change.

**Verified on 21 October 2026**, with the copy served from this repository's build under its own policy: 33 of 33 browser
checks, 52 of 52 theory numbers, no request outside the site, the tab bar in the site's own Instrument Serif and IBM Plex Sans.

## How to update a copy of an app

1. Change the project in its own app (`droplet-collection-yl7l26` or `rotor-pendula-gafw0f`) and check it there.
2. Make a website variant of its source, outside the app: remove the Saved runs page, its route and link, and the Save
   button with its server call; add the back link `← Numa Koudsie · Portfolios` to `../../portfolios.html` in the top bar;
   add ` · Numa Koudsie` to the page title. Build that variant with a separate Vite configuration that sets `base: './'` and
   `build.assetsDir: 'static'` (the apps' own `vite.config.ts` keeps Vite's default `assets/`). The repeatable helper is [tools/make_portfolio_copy.py](../tools/make_portfolio_copy.py):

   ~~~bash
   python3 tools/make_portfolio_copy.py /absolute/app-source /absolute/new-workdir
   ~~~

   The two copies now in this repository were not made by the present version of the helper: its Simulate note ("This
   website copy runs in your browser. Saving named runs is available in the standalone project.") and its back-link class
   `back-site` are in neither bundle. The source must have its existing dependencies available. The helper makes an isolated source copy, removes the saved-run route and controls, retains solver error messages, adds the backlink and title suffix, builds with a separate Vite configuration, patches the stylesheet loader, points the stylesheet's font import at the website's `fonts/` and adds the website's security policy and referrer rule (taken from `index.html`). It stops if the app loads other Google fonts than `public/fonts/instrument-plex.css` holds. It installs nothing. The output is `new-workdir/dist/`; the standalone app is not edited.
   Build with the KaTeX version the deployed app uses (0.16.47 today; it is the `content` of the `.katex-version` rule in the
   app's served CSS). The apps have no lockfile, so a fresh `node_modules` can bring a different KaTeX, which changes the
   hidden MathML that screen readers use and the spacing of multi-line equations while the visible maths looks the same
   (seen on 15 October 2026 with 0.16.11).
3. Replace the folder here with the new build output (delete the old `static/` first, because the hashed names change).
4. The helper has already replaced the stylesheet `<link>` of `dist/index.html` with the loader script. If you built
   without it, replace the line `<link rel="stylesheet" crossorigin href="./static/index-<hash>.css">` with the one-line
   loader script used now, with the new hash:
   `<script>(function(){var l=document.createElement('link');l.rel='stylesheet';l.href='./static/index-<hash>.css';document.head.appendChild(l)})();</script>`
   It has also replaced the stylesheet's `@import"https://fonts.googleapis.com/…"` with `@import"../../../fonts/instrument-plex.css"`
   and added lines 5–6 of the root `index.html` (the security policy and referrer rule) after the charset line of `dist/index.html`.
   Without these the copy would send every visitor's address to Google, and the website's policy would not cover it.
5. Keep the links in `public/portfolios.html` pointing at `index.html#/…`, never at a folder.
6. Deploy the website and open every route of the copy on the live site, https://phyeinusul.com ([usul.md](usul.md); the
   AppDeploy app only on Numa's request, [appdeploy-app.md](appdeploy-app.md)): the page must be styled (the stylesheet loaded
   with status 200), and the maths typeset.

## Notes for maintainers

- The KaTeX fonts are shipped four times on this site: once in `public/vendor/katex/fonts/` (20 woff2 files, 0.26 MB, for
  the simulation pages), embedded as `data:` addresses in the Hydraulic Press Study, and once inside each app copy's `static/` (59 files in woff2, woff and ttf; 2.1 MB for the two copies
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

## Iron, Cotton and the Head: `impact/`

Two pages, generated from [`portfolios-src/impact/`](../portfolios-src/impact/) (its [README](../portfolios-src/impact/README.md)
lists every file) by `python3 portfolios-src/impact/build.py --site`. Never edit the two pages by hand.

| Path | What it is |
|---|---|
| `impact/index.html` | The study in English: two balls of 1 kg, iron and cotton, dropped from 10 m onto a head drawn as a plate on a spring and damper, which is also the scale. A peak-hold force gauge and a digital panel under each ball, force curves, energy books, seven sections of derivations and a table of every parameter. |
| `impact/ar.html` | The same study written in Arabic, right to left, set in Amiri and Noto Naskh Arabic ([assets.md](assets.md#arabic-faces-added-22-october-2026-on-numas-request)). |
| `impact/fig/01_impact.webp` … `04_weight.webp` | The four plates of the Portfolios entry, screenshots of the English page. |

**How a page works.** The model (`physics.js`, copied into the page between `/*PHYSICS-BEGIN*/` and `/*PHYSICS-END*/`) runs once
when the page opens, in slices of 14 ms so the page stays usable, and stores every particle's position every 1 ms up to 2.5 s and
every 2 ms after that; the animation only plays the stored run back, as Figs. 9 and 10 do. Each page carries the site's security
policy and referrer rule after its charset line, loads only `../../fonts/instrument-plex.css` (and `arabic.css` on the Arabic page),
makes no request outside the site, and links back to `../../portfolios.html`. The pages need no `'unsafe-eval'` and no worker.

**What was checked** (22 October 2026, headless Chromium on the built site, `checks/site_check.cjs`): both pages at 1100 and
390 px, no script errors, no failed or outside requests, no sideways scroll; iron peaks at 638.6 N, cotton at 188.0 N, both
scales settle at 9.81 N; the first touch at 1.428 s equals √(2h/g); the energy books close to 0.21 J (iron) and 0.51 J (cotton) out
of about 98 J (`checks/energy_books.cjs`); halving the time step changes the peaks by 0.0 % (iron) and 1.5 % (cotton)
(`checks/step_size.cjs`).

