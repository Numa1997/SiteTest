# The four research projects: `public/portfolios/`

The Portfolios page ([`public/portfolios.html`](../public/portfolios.html), described in [pages.md](pages.md)) presents four
research projects; the fourth, Iron, Cotton and the Head, is described [at the end](#iron-cotton-and-the-head-impact). The first two are each their own AppDeploy app with its own source; the third, the Hydraulic Press
Study, is generated from its own GitHub repository ([below](#the-hydraulic-press-study-hydraulics)). This website carries only
a **built copy** of each one, so that a reader can open it here without leaving the site:

| Folder | Built from the app | What it is |
|---|---|---|
| [`public/portfolios/droplet-collection/`](../public/portfolios/droplet-collection/) | its source in [`portfolios-src/droplets/`](../portfolios-src/droplets/) (since 23 October 2026; before, the app `droplet-collection-yl7l26`) | Numa's Bachelor thesis (Leipzig) on how cloud droplets grow into rain, rebuilt as lecture notes: ten chapters from one drop to ice, three simulations running in the browser, worked problems and checks. One self-contained page ([below](#droplet-collection-droplet-collection-since-23-october-2026)). |
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
   - (Droplet Collection used `#/`, `#/theory`, `#/results`, `#/simulate`, `#/checks` until 23 October 2026; it is now one
     generated page, described [below](#droplet-collection-droplet-collection-since-23-october-2026).)
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

### `droplet-collection/`

Since 23 October 2026 the copy is generated from [`portfolios-src/droplets/`](../portfolios-src/droplets/); see
[below](#droplet-collection-droplet-collection-since-23-october-2026). What sits in the folder:

| Path | What it is |
|---|---|
| `index.html` | The whole project in one file, written by `portfolios-src/droplets/tools/build.py --site`: the lecture notes (maths typeset at build time with KaTeX 0.16.11), the model, the three simulations, the figures as inline SVG. It loads the site's `fonts/instrument-plex.css` and `vendor/katex/katex.min.css`. |
| `fig/plate-fallspeed.svg`, `fig/plate-efficiency.svg`, `fig/plate-warm.svg`, `fig/plate-first.svg` | The four plates of the Portfolios page article, written by the same build from the same figures as the notes. |
| `fig/c1_ice.svg`, `fig/ecoll_map.svg`, `fig/fallspeed_gk.svg`, `fig/golovin.svg`, `fig/w2_rain.svg`, `fig/w2_spectra.svg`, `static/` | Left over from the app copy. `index.html` no longer loads `static/`; the German and Arabic Portfolios pages still show the old `fig/` plates until the i18n generator is run again (`tools/i18n/build.py`), so they stay for now. |

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

### The data panel of the two simulations (since 23 October 2026)

The ideal press and the servo press each carry the site's data panel ([scripts/datalog.md](scripts/datalog.md)), the same one as
the ten simulations and Iron, Cotton and the Head. Each page is its own source, so the store and the panel's hooks are written into
it, after the page's user-interface code: `declareStore()`, `storeRun()` (and on the servo page `storeAnalysis()`), `setNow()` and
`Sim.data`.

**Loading the shared files from inside a frame.** Each page sits in an `iframe srcdoc`, whose address for relative links is the
study's own (`portfolios/hydraulics/index.html`), so `../../scripts/…` reaches the site's `sim.js`, `dataset.js`, `datalog.js` and
`../../styles/…` its `paper.css` and `data.css`. A three-line loader in each page chooses the folder: two levels up when the
address ends in `/portfolios/hydraulics/…`, `../../public/` when the page is opened from `portfolios-src/hydraulics/` on disk, and
nothing elsewhere (the `blob:` fallback frame), where the page runs as before without a panel. The scripts are written into the page
with `document.write` while it is being read, so they keep their order: `sim.js`, `dataset.js`, the page, `datalog.js`. `sim.js`
loads a walkthrough only for an element that names one in `data-walk`, so the ideal press's chart `canvas#walk` (the pressure walk)
no longer makes it request `walk/null.js`.

**What is stored.** Ideal press (92 variables): the seven sliders, the eleven constants of `CONST`, ten numbers of `makeModel()`
(areas, the lever $r$, $F_{1,\min}$, the level stiffness $k$, $\mu'$, $\mu(0)$), the run's results (outcome, departure, stroke stop,
impact speed and lost energy, highest and lowest pressure, the two self-tests), the 18 recorded series over one sample per 1 ms plus
$x_2 = r x$, $F_2 = p_2 A_2$ and Pascal's $F_1/r$, the sample on screen, and the drawing (scale, origin, piston rows, dial radius,
centres, full scales and the five needle angles). Servo press: the sixteen sliders, the constants of `C0`, thirteen numbers of
`makePlant()`, the cycle's results, the 28 recorded series per controller sample plus the two summed losses shown in the tiles, and for
each loop the margins, the operating point, the frequency response (500 frequencies: $|L|$, dB, phase, Nyquist real and imaginary
parts) and the open- and closed-loop poles with their frequencies and damping ratios, the sample on screen and the drawing (scale,
dial centres, radius, full scales, the five needle angles).

**What reads it.** The scene, the dials, the plots, the readouts, the status lines and chips, and on the servo page the Bode and Nyquist
plots and the tables of margins and poles read the store's arrays and values (the z-plane plot draws the same closed-loop poles from
the analysis result the store was filled from); the arithmetic left in the drawing turns metres, pascals and
newtons into pixels and display units. The servo page's nine worked solutions compute their own small figures when opened; those
numbers are not in the store, and the panel's paragraph says so.

**Check.** A slider value against the slider; a constant against the code; a derived value from its formula with the stored inputs;
every recorded series and every result by running `simulate()` again from the stored parameters (ideal press: a few milliseconds;
servo press: the whole cycle and both analyses on this page, 1.6 s in Node, cached by the parameters); the drawing numbers from the
layout formula and the stored inputs. **Read-back:** the five needles of each dial strip (a dark pixel 0.45 r from the hub along the
stored angle) and, on the ideal press, the lower edges of both pistons at their stored rows. **Read values:** a click on a dial pins
its value and needle angle, on a piston (ideal) or the ram and platen (servo) pins the motion, pressures and forces of the sample on
screen, on the oil (ideal) pins the pressure there and its parts. **One round** is one run (ideal) or one press cycle (servo), from
$t = 0$; Record plays it from the start.

**The ideal press's pressure probe now needs a click.** It used to follow the mouse across the running figure, against the site's rule
that nothing on a running figure reacts to a pointer merely crossing it; a click or tap places it, a click outside the oil removes it.

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

### The data panel of the study

Since 23 October 2026 both pages carry the site's data panel, the same one as the ten simulations
([scripts/datalog.md](scripts/datalog.md)). Picture an assistant beside the drop with a notebook: the run is computed once, and
every number of it is written into one store, a dataset in the sense of [scripts/dataset.md](scripts/dataset.md); the drawing, the
gauges, the readouts, the plots and the energy bars only read that store, and the panel shows it, checks it and saves it.

**What loads.** The pages load the shared files from the site, no copies: `../../styles/paper.css` (for Latin Modern in the
panel's symbols) and `../../styles/data.css` in the head; at the end of the body `../../scripts/sim.js`, `../../scripts/dataset.js`,
the page script, and `../../scripts/datalog.js` last. `sim.js` does no harm here: it defines `window.Sim`, adds an error banner if a
script fails, and would load KaTeX for a figure caption with mathematics; the study's caption has none, and since this change
`sim.js` loads KaTeX on a page without a lecture note only when a caption contains `\(` (measured: the page requests
`paper.css`, `data.css`, `sim.js`, `dataset.js`, `datalog.js` and fonts, nothing else). The study defines the panel's colour and
font tokens in its own palette (`--accent` is the study's wine, `--sans` IBM Plex Sans, also on the Arabic page), and its element
rules for `h2`, `h3`, `p`, `button` and `canvas` are written as `:where(…:not(.dp *))`, so they no longer reach into the panel.

**Where the code is.** The store is declared in `declare()` and filled in `record()` in
[`template.html`](../portfolios-src/impact/template.html); the panel's hooks (`probe`, `inspect`, `locate`, `check`, `drawn`,
`round`, `about`) are in [`datahooks.js`](../portfolios-src/impact/datahooks.js), which `build.py` inserts after the page script.
The canvas sits in `figure.stage > div#stage`, with the caption `figcaption.stage__cap` that receives the Read values switch.

**The store.** Six dimensions: `n` (5751 samples: every 1 ms to 2.5 s, every 2 ms to 9 s), `p_iron` (91 atoms), `p_cot` (612
beads), `b_iron` (240 bonds), `b_cot` (1196 bonds: 594 stretch springs along the fibres, 602 junctions) and `c` (47 checkpoints).
The groups of the panel:

| Group | What it holds |
|---|---|
| Parameters | the 35 constants of `P`, as scalars |
| Derived physics | particles and bonds of each ball, particle mass $M/N$, skin contact $m\omega_c^2$ and $2\zeta_c m\omega_c$, iron's Morse $\alpha = \alpha r_0/a$ and $D = k/2\alpha^2$, the junction's $\alpha_j$ and $D_j$, the zero of height energy, $E_0$, $t^* = \sqrt{2h/g}$, $v^* = \sqrt{2gh}$, $Mg$ |
| Solver | samples, checkpoint spacing, samples computed, frame steps, compute time, done |
| Results | first touch, peak force, weight (mean reading from 4 s to 9 s), its distance from $Mg$, largest gap in the energy books |
| Stored run | per sample: `ts`, `nstep`; for each ball the positions `x`, `y` and speeds `sp` of every particle (float32), plate position `yp` and velocity `vp`, scale reading `F`, peak hold `Fmax`, the six energy terms `KE`, `PE`, `El`, `Eh`, `Qb` (heat in the ball), `Qh` (heat in the head), the bars `Ein` and `Esum`, the gap `books` and the running weight `W` |
| Shape of the balls | bond lists `bi`, `bj`, rest lengths `l0`, cotton's bond kinds and fibre of each bead |
| Checkpoints | every 125 samples, the full state of each ball (positions, velocities, plate, peak hold, heat, first touch, which bonds hold) and the step count |
| Playback | `t_play`, `i_now`, `t_now`, `slow`, `playing`, and for each ball the reading, peak, weight, kitchen-scale masses $F_\text{peak}/g$ and $W/g$, plate position, kinetic energy and books gap of the sample on screen |
| Drawing | canvas size and device pixel ratio, ruler, scene top and bottom, column width and centres, the scale $s$ in px/m, the camera height, the gain $G = 10$ of the plate travel and the extra offset $(G-1)y_p$, the plate's screen row, the gauge radius and centre, the two needle angles, the gauge's full scale |

Every variable has a symbol, units where it has any, a long name, `computed_in` and digits. Positions and speeds are float32: the
cotton ball alone holds $612 \times 5751 \times 3$ of them, 42 MB as float32 and 84 MB as float64; everything else is float64.

**What each Check recomputes.** A constant against `P`; a derived value from its formula with the stored inputs; counts, bond lists,
rest lengths and the zero of height energy from a second build by `makeIron()` or `makeCotton()`. A position, speed, plate state,
peak or energy term at sample $n$ by rerunning the same `step()` on a separately built ball, from the checkpoint before $n$ (never
from $n$ itself) to $n$; the first checkpoint is checked by stepping a fresh build from $t = 0$, so the chain is anchored at the
start. The step counts by adding the sub-steps $\Delta t/5$ again exactly as the model does. The scale reading as
$F = -k_h y_p$ from the stored plate position; the bars as $E_\text{in} = E_0 - V_n$ and $E_\text{now} = K + E_\text{el} +
E_\text{head} + Q_\text{ball} + Q_\text{head}$; the books gap as their difference; the weight as the mean of the stored readings;
every drawing number from the stored drawing inputs. A rerun takes at most 1250 steps (0.67 s for cotton and 0.09 s for iron,
measured in Node).

**What each read-back reads.** The plate: two columns near its ends are scanned row by row for the plate's fill colour, which must
begin half the outline below `plate_px`; the black needle: a dark pixel 0.3 R from the hub along the stored angle; the red peak
needle: its tip, 6.5 px inside the rim, which the black needle never covers; a particle at the sample on screen: the dark atom disc
or the pale bead core at the position worked out from the stored drawing variables; the scale reading of sample $n$: the wine
(iron) or blue (cotton) curve of the whole-run plot. Values not drawn at the moment (another sample, a part outside the scene,
cotton's curve under iron's) give "not in the picture at the moment".

**Read values.** A click on an atom or a bead pins it: sample, time, $x$, $y$, speed (and the fibre of a bead). A click on a gauge,
a digital panel or a plate pins that ball's scale: reading, peak, weight, plate position, needle angle. **One round** is one drop,
$t = 0$ to 9 s of the stored run; Record starts a new drop from $t = 0$ (the first frame of a drop advances nothing, so the round
begins exactly at 0), refuses while a drop is under way, and follows the iron scale unless another point is pinned.

**What differs between store and picture**, said in the panel's paragraph: the plate travel, and the ball resting on it, are drawn
ten times larger than computed; the camera follows the lowest iron atom for both columns; bond colours are worked out at drawing
time from the stored positions; cotton fibres are smooth curves through the beads; the gauges have a square-root dial; the weight
shows from 6.5 s.

**The panel's words are English on the Arabic page too**, set left to right (`lang="en" dir="ltr"` on the panel, the tab, the strip
and the switch, written by `datalog.js`), until the panel gets its string table.

**Measured** (23 October 2026, headless Chromium, built site): English page at 1100 and 1600 px, Arabic page at 390 px
(`portfolios-src/impact/checks/data_panel.cjs`): no script errors, no sideways scroll; 190 variables, each with symbol,
long name, `computed_in` and digits, each in one of nine groups; Check on every scalar and on six indices of every array: 406
identical, 34 agreeing to 7 or 8 figures (the float32 positions and speeds), 18 undefined on both sides (the weight before 4 s),
0 differing, all 458 in 7.1 s; every read-back at the moment of impact (t = 1.452 s) shows its value (atoms, bead, both needles, both
peak needles, both plates, both curves), and cotton's curve, where the iron curve covers it, reads "not in the picture at the
moment"; Read values: a pointer swept across the figure paints 0 overlay pixels with the switch off and on, a click pins an atom, a
bead or a scale, the strip sits directly under the figure (no overlap), its values change 4 times a second (12 batches in 3 s); one
round, 0 to 9 s, records every frame (349 to 486 samples at real speed) with no undefined value at the followed scale; Save gives a
51.6 MB zip that `zipfile.testzip()` accepts and NumPy reads (`x_cot` float32 5751 × 612, `F_iron` float64 5751, 73 members,
units in `dataset.json`); with the panel closed `__dataPanel.running()` is false. The run itself gives the documented numbers: iron
638.6 N, cotton 188.0 N, weights 9.810 N and 9.810 N, first touch 1.428 s, books closed to 0.21 J and 0.51 J. Computing the run
takes 9 % longer than before the store (123 s against 113 s in this container's headless Chromium, which has no GPU).



## Droplet Collection: `droplet-collection/` (since 23 October 2026)

The project was rebuilt from first principles as lecture notes; the app copy it replaces is described in the sections above as it
was. Source, build and checks are in [`portfolios-src/droplets/README.md`](../portfolios-src/droplets/README.md); the record of
how each model level was argued, attacked by an independent reviewer and checked is in [`notes/droplets/`](../notes/droplets/)
(`status.md` first).

- **One page, four tabs.** `index.html` holds the tabs Simulation (`#sim`), Lecture notes (`#book`), Problems (`#problems`) and
  Checks (`#checks`); any element id also works as an address (`#ch3`, `#fig-5-2`, `#eq-6.1`), opening its tab. The Portfolios
  page links to `#book`, `#sim`, `#checks` and to four figures.
- **The model runs in the page.** The code between `/*PHYSICS-BEGIN*/` and `/*PHYSICS-END*/` of `physics.cjs` is inlined; the
  same code runs in Node for the run tools and the checks. The three panels (collection equation in a box, droplet trajectories,
  an exact random cloud) change only on a click, a slider release or a button; nothing reacts to the pointer crossing a figure.
- **Every quoted number is checked.** `checks/check_numbers.cjs` recomputes 141 numbers from the model and finds each in the text
  near its anchor; `checks/check_physics.py` recomputes the physics independently in Python (12 checks); `checks/check_browser.py`
  opens every tab at 360, 390, 1024 and 1440 px and counts KaTeX errors, page errors and horizontal overflow.
- **The ladder.** L0 one collector (chapter 1); L1 fall speed (2); L2 collision efficiency (3); L3 coalescence (4); L4 the
  collection equation (5); L5 the exact random process and the first drizzle (6); L6 turbulence, decided by a number (7); L7 ice (8).
